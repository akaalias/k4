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
from kryptos.scorer import fitness, english_score, free_text, loss
import phase as phaseclock

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
    ap.add_argument("--rerender", action="store_true", help="rebuild all experiment.md files and exit")
    args = ap.parse_args()
    if args.rerender:
        rerender(); return

    meta = load_experiment_meta()
    exp_id = next_id()
    tag = f"{exp_id:04d}-{meta['slug']}"
    outdir = EXPERIMENTS / tag
    outdir.mkdir(parents=True)
    shutil.copy(ATTACK, outdir / "attack.py")
    raw_path = outdir / "raw.json"

    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    t0 = time.time()
    phases = phaseclock.close(now=t0)
    if not phases:
        prev = sorted(EXPERIMENTS.glob("*/result.json"))
        if prev:
            prev_end = json.loads(prev[-1].read_text()).get("ended_epoch")
            if prev_end:
                phases["unattributed"] = max(0.0, t0 - prev_end)
    status = "ran"
    try:
        subprocess.run([sys.executable, str(ROOT / "_runner.py"), str(ATTACK), str(raw_path), str(args.budget)],
                       timeout=args.budget + 60, check=False, cwd=ROOT)
    except subprocess.TimeoutExpired:
        status = "timeout"
    seconds = time.time() - t0
    phases["run"] = seconds
    t_record = time.time()
    raw = json.loads(raw_path.read_text()) if raw_path.exists() else {"candidates": [], "bounds": {}, "error": "no output", "worked_example": "", "notes": ""}
    if raw.get("error"):
        status = "error"

    # Gate and score
    scored = []
    for c in raw["candidates"]:
        g = run_gates(c["plaintext"], c.get("reencrypted"))
        row = {**c, "gate_passed": g.passed, "failed_at": g.failed_at, "crib_hits": g.crib_hits,
               "crib_words": g.crib_words, "gate_details": g.details, "english_free": None, "fitness": None,
               "loss": None}
        if g.failed_at in (None, "cribs"):  # valid candidates get a loss; invalid ones do not
            row["loss"] = loss(c["plaintext"], c["key_bits"], g.crib_hits)
        if g.passed:
            row["english_free"] = english_score(free_text(c["plaintext"]))
            row["fitness"] = fitness(c["plaintext"], c["key_bits"])
        scored.append(row)
    passed = [r for r in scored if r["gate_passed"]]
    passed.sort(key=lambda r: r["loss"])          # one number everywhere: lowest loss wins
    best = passed[0] if passed else None
    best_hits = max((r["crib_hits"] for r in scored), default=0)
    best_words = max(scored, key=lambda r: r["crib_hits"])["crib_words"] if scored else {}
    losses = [r["loss"] for r in scored if r["loss"] is not None]
    best_loss = min(losses) if losses else None

    champion = load_champion()
    if best and (champion is None or best["loss"] < champion.get("loss", float("inf"))):
        decision = "kept"
        CHAMPION.write_text(json.dumps({"experiment": tag, "loss": best["loss"], "fitness": best["fitness"],
                                        "plaintext": best["plaintext"], "key": best["key"],
                                        "key_description": best["key_description"]}, indent=1))
    else:
        decision = "reverted"
    if status in ("timeout", "error"):
        decision = status

    phases["record"] = time.time() - t_record
    phases = {k: round(v, 1) for k, v in phases.items()}
    result = {
        "id": exp_id, "tag": tag, "started": started, "seconds": round(seconds, 1), "status": status,
        "phases": phases, "ended_epoch": time.time(),
        "decision": decision, "decision_rule": "loss", "n_candidates": len(scored), "n_passed": len(passed),
        "best_crib_hits": best_hits, "best_crib_words": best_words, "best_fitness": best["fitness"] if best else None,
        "best_loss": best_loss,
        "champion_before": champion, "bounds": raw.get("bounds", {}), "notes": raw.get("notes", ""),
        "error": raw.get("error"), "candidates": scored[:20],
    }
    (outdir / "result.json").write_text(json.dumps(result, indent=1))
    (outdir / "worked_example.txt").write_text(raw.get("worked_example", "") or "")
    (outdir / "experiment.md").write_text(render_md(meta, result, raw))

    if not RESULTS.exists():
        RESULTS.write_text("id\ttag\tfamily\tparent\tdecision\tn_candidates\tn_passed\tbest_crib_hits\tbest_loss\tbest_fitness\tseconds\tphases\n")
    with RESULTS.open("a") as f:
        ph = " ".join(f"{k}={v:.0f}" for k, v in phases.items())
        f.write(f"{exp_id:04d}\t{tag}\t{meta['family']}\t{meta['parent'] or '-'}\t{decision}\t{len(scored)}\t{len(passed)}\t{best_hits}\t{'' if best_loss is None else f'{best_loss:.3f}'}\t{'' if best is None else f'{best['fitness']:.4f}'}\t{seconds:.0f}\t{ph}\n")

    print(f"[{tag}] decision={decision} candidates={len(scored)} passed={len(passed)} best_crib_hits={best_hits}/24"
          f" best_fitness={best['fitness'] if best else None} seconds={seconds:.0f}")
    if result["error"]:
        print(result["error"])

    if not args.no_commit:
        subprocess.run(["git", "add", str(outdir), str(RESULTS), str(CHAMPION) if CHAMPION.exists() else str(RESULTS)], cwd=ROOT, check=False)
        subprocess.run(["git", "commit", "-q", "-m", f"exp {tag}: {decision} ({len(passed)}/{len(scored)} passed gates, best cribs {best_hits}/24)\n\n{meta['title']}\nFamily: {meta['family']}\nParent: {meta['parent'] or '-'}\nChanged: {meta['changed']}"], cwd=ROOT, check=False)


def steps(text):
    """Put each numbered step on its own line so markdown renders a real list.
    Splits only on the next expected step number, so '25.' inside a sentence stays put."""
    import re as _re
    t = " ".join(text.split())
    k = 1
    out = []
    pos = 0
    while True:
        m = _re.search(rf"(?<!\d){k}\.\s+", t[pos:])
        if not m:
            break
        if k > 1:
            out.append(t[pos:pos + m.start()].strip())
        pos += m.end()
        k += 1
    if k == 1:
        return t
    out.append(t[pos:].strip())
    return "\n".join(f"{i}. {s}" for i, s in enumerate(out, start=1))


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
**Time by phase:** {', '.join(f"{k} {v:.0f} s" for k, v in result['phases'].items()) or 'not recorded'}

## In plain words

{meta['hypothesis_eli5']}

## Walkthrough, by hand

{steps(meta['walkthrough'])}

## Worked example (generated)

```
{raw.get('worked_example', '')}
```

## Lineage

Inherits from {meta['parent'] or 'nothing; this is a root experiment'}. What changed: {meta['changed']}

## Hypothesis (domain expert)

{meta['hypothesis_expert']}

## Prediction

{meta['prediction']}

## Method

{steps(meta['method'])}

## Result

Candidates returned: {result['n_candidates']}. Passed all gates: {result['n_passed']}. Best crib hits among all candidates: {result['best_crib_hits']}/24
({', '.join(f"{w} {h}/{n}" for w, (h, n) in result.get('best_crib_words', {}).items()) or 'no candidates'}).
Best loss: {result['best_loss']} (0 is solved; 10 per missed crib letter). Best fitness: {result['best_fitness']}. Champion before this run: {(result['champion_before'] or {}).get('experiment', 'none')}.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
{rows}

### Bounds searched (the negative result this experiment leaves behind)

```
{bounds}
```

{('Notes: ' + result['notes']) if result['notes'] else ''}
{('Error:\n```\n' + result['error'] + '\n```') if result['error'] else ''}

"""


def rerender():
    """Rebuild every experiment.md from its snapshot attack.py, result.json and raw.json."""
    import importlib.util
    for d in sorted(EXPERIMENTS.iterdir()):
        if not (d / "result.json").exists():
            continue
        spec = importlib.util.spec_from_file_location("attack_snap", d / "attack.py")
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        meta = dict(mod.EXPERIMENT)
        result = json.loads((d / "result.json").read_text())
        result.setdefault("phases", {"run": result.get("seconds", 0)})
        raw = json.loads((d / "raw.json").read_text()) if (d / "raw.json").exists() else {}
        (d / "experiment.md").write_text(render_md(meta, result, raw))
        print("re-rendered", d.name)


if __name__ == "__main__":
    main()
