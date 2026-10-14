#!/usr/bin/env python3
"""The frozen harness. Runs attack.py once under a time budget, applies the
gates, scores survivors, decides keep or revert against the champion, and
writes the experiment record. The agent runs this and never edits it.

Usage: python run_experiment.py [--budget SECONDS] [--no-commit]
"""
import argparse
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from kryptos import facts
from kryptos.gates import run_gates, crib_hits
from kryptos.scorer import fitness, english_score, free_text

ROOT = Path(__file__).resolve().parent
EXPERIMENTS = ROOT / "experiments"
RESULTS = ROOT / "results.tsv"
CHAMPION = ROOT / "champion.json"
ATTACK = ROOT / "attack.py"

REQUIRED = ["slug", "title", "family", "parent", "changed", "hypothesis_expert",
            "hypothesis_eli5", "prediction", "method", "walkthrough"]


def load_experiment_meta():
    import importlib.util
    spec = importlib.util.spec_from_file_location("attack_meta", ATTACK)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    meta = dict(mod.EXPERIMENT)
    missing = [k for k in REQUIRED if k != "parent" and not meta.get(k)]
    if "parent" not in meta:
        missing.append("parent")
    if missing:
        sys.exit(f"attack.py EXPERIMENT is missing: {missing}")
    return meta


def next_id():
    ids = [int(p.name[:4]) for p in EXPERIMENTS.iterdir() if p.is_dir() and p.name[:4].isdigit()]
    return max(ids, default=0) + 1


def load_champion():
    return json.loads(CHAMPION.read_text()) if CHAMPION.exists() else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget", type=float, default=1800.0, help="seconds (default 30 min)")
    ap.add_argument("--no-commit", action="store_true")
    args = ap.parse_args()

    meta = load_experiment_meta()
    exp_id = next_id()
    tag = f"{exp_id:04d}-{meta['slug']}"
    outdir = EXPERIMENTS / tag
    outdir.mkdir(parents=True)
    shutil.copy(ATTACK, outdir / "attack.py")
    raw_path = outdir / "raw.json"

    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    t0 = time.time()
    status = "ran"
    try:
        subprocess.run([sys.executable, str(ROOT / "_runner.py"), str(ATTACK), str(raw_path), str(args.budget)],
                       timeout=args.budget + 60, check=False, cwd=ROOT)
    except subprocess.TimeoutExpired:
        status = "timeout"
    seconds = time.time() - t0
    raw = json.loads(raw_path.read_text()) if raw_path.exists() else {"candidates": [], "bounds": {}, "error": "no output", "worked_example": "", "notes": ""}
    if raw.get("error"):
        status = "error"

    # Gate and score
    scored = []
    for c in raw["candidates"]:
        g = run_gates(c["plaintext"], c.get("reencrypted"))
        row = {**c, "gate_passed": g.passed, "failed_at": g.failed_at, "crib_hits": g.crib_hits,
               "gate_details": g.details, "english_free": None, "fitness": None}
        if g.passed:
            row["english_free"] = english_score(free_text(c["plaintext"]))
            row["fitness"] = fitness(c["plaintext"], c["key_bits"])
        scored.append(row)
    passed = [r for r in scored if r["gate_passed"]]
    passed.sort(key=lambda r: r["fitness"], reverse=True)
    best = passed[0] if passed else None
    best_hits = max((r["crib_hits"] for r in scored), default=0)

    champion = load_champion()
    if best and (champion is None or best["fitness"] > champion["fitness"]):
        decision = "kept"
        CHAMPION.write_text(json.dumps({"experiment": tag, "fitness": best["fitness"],
                                        "plaintext": best["plaintext"], "key": best["key"],
                                        "key_description": best["key_description"]}, indent=1))
    else:
        decision = "reverted"
    if status in ("timeout", "error"):
        decision = status

    result = {
        "id": exp_id, "tag": tag, "started": started, "seconds": round(seconds, 1), "status": status,
        "decision": decision, "n_candidates": len(scored), "n_passed": len(passed),
        "best_crib_hits": best_hits, "best_fitness": best["fitness"] if best else None,
        "champion_before": champion, "bounds": raw.get("bounds", {}), "notes": raw.get("notes", ""),
        "error": raw.get("error"), "candidates": scored[:20],
    }
    (outdir / "result.json").write_text(json.dumps(result, indent=1))
    (outdir / "worked_example.txt").write_text(raw.get("worked_example", "") or "")
    (outdir / "experiment.md").write_text(render_md(meta, result, raw))

    if not RESULTS.exists():
        RESULTS.write_text("id\ttag\tfamily\tparent\tdecision\tn_candidates\tn_passed\tbest_crib_hits\tbest_fitness\tseconds\n")
    with RESULTS.open("a") as f:
        f.write(f"{exp_id:04d}\t{tag}\t{meta['family']}\t{meta['parent'] or '-'}\t{decision}\t{len(scored)}\t{len(passed)}\t{best_hits}\t{'' if best is None else f'{best['fitness']:.4f}'}\t{seconds:.0f}\n")

    print(f"[{tag}] decision={decision} candidates={len(scored)} passed={len(passed)} best_crib_hits={best_hits}/24"
          f" best_fitness={best['fitness'] if best else None} seconds={seconds:.0f}")
    if result["error"]:
        print(result["error"])

    if not args.no_commit:
        subprocess.run(["git", "add", str(outdir), str(RESULTS), str(CHAMPION) if CHAMPION.exists() else str(RESULTS)], cwd=ROOT, check=False)
        subprocess.run(["git", "commit", "-q", "-m", f"exp {tag}: {decision} ({len(passed)}/{len(scored)} passed gates, best cribs {best_hits}/24)\n\n{meta['title']}\nFamily: {meta['family']}\nParent: {meta['parent'] or '-'}\nChanged: {meta['changed']}"], cwd=ROOT, check=False)


def render_md(meta, result, raw):
    cands = result["candidates"]
    rows = "\n".join(
        f"| {i+1} | {'pass' if c['gate_passed'] else c['failed_at']} | {c['crib_hits']}/24 | "
        f"{'' if c['fitness'] is None else f'{c['fitness']:.3f}'} | `{c['plaintext']}` | {c['key_description']} |"
        for i, c in enumerate(cands[:10])
    ) or "| - | no candidates | | | | |"
    bounds = json.dumps(result["bounds"], indent=1) if result["bounds"] else "(none recorded)"
    return f"""# {result['tag']}: {meta['title']}

**Family:** {meta['family']}  
**Parent:** {meta['parent'] or 'none (root)'}  
**Decision:** {result['decision']}  
**Run:** {result['started']}, {result['seconds']} s, status {result['status']}

## Lineage

Inherits from {meta['parent'] or 'nothing; this is a root experiment'}. What changed: {meta['changed']}

## Hypothesis (domain expert)

{meta['hypothesis_expert']}

## Prediction

{meta['prediction']}

## Method

{meta['method']}

## Result

Candidates returned: {result['n_candidates']}. Passed all gates: {result['n_passed']}. Best crib hits among all candidates: {result['best_crib_hits']}/24.
Best fitness: {result['best_fitness']}. Champion before this run: {(result['champion_before'] or {}).get('experiment', 'none')}.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
{rows}

### Bounds searched (the negative result this experiment leaves behind)

```
{bounds}
```

{('Notes: ' + result['notes']) if result['notes'] else ''}
{('Error:\n```\n' + result['error'] + '\n```') if result['error'] else ''}

## Walkthrough (standalone)

{meta['walkthrough']}

## Worked example (generated)

```
{raw.get('worked_example', '')}
```

## ELI5

{meta['hypothesis_eli5']}
"""


if __name__ == "__main__":
    main()
