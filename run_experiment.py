#!/usr/bin/env python3
"""The frozen harness. Runs attack.py once under a time budget, applies the
gates, scores survivors, decides keep or revert against the champion, and
writes the experiment record. The agent runs this and never edits it.

Usage: python run_experiment.py [--budget SECONDS (default: no limit)] [--no-commit]
Start it with tools/start_experiment.sh so it runs outside any session's time limit.
"""
import argparse
import json
import os
import shutil
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from kryptos import facts, checkpoint
from kryptos.gates import run_gates, crib_hits, undetermined, readings_before, resubmitted
from kryptos.scorer import fitness, english_score, free_text, loss, key_bits_of
import phase as phaseclock

ROOT = Path(__file__).resolve().parent
EXPERIMENTS = ROOT / "experiments"
RESULTS = ROOT / "results.tsv"
CHAMPION = ROOT / "champion.json"
ATTACK = ROOT / "attack.py"

COMPUTE = ROOT / "data" / "compute.json"   # {"where": "modal"} or {"where": "local"}; tools/compute.sh sets it
LOCAL_FALLBACK_WORKERS = 4                # when Modal cannot run the search (issue #99)


def compute_where():
    try:
        return json.loads(COMPUTE.read_text()).get("where", "local")
    except (OSError, ValueError):
        return "local"


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


def unfinished_folder(attack_bytes):
    """A folder a stopped run left behind (no result.json) for this same attack.py: the rerun takes its number."""
    for p in sorted(EXPERIMENTS.iterdir(), reverse=True):
        if p.is_dir() and p.name[:4].isdigit() and not (p / "result.json").exists():
            a = p / "attack.py"
            if a.exists() and a.read_bytes() == attack_bytes:
                return p
    return None


_child = [None]
_stopping = [False]


def _stop(signum, frame):
    """Stopped from outside (tools/stop_experiment.sh, issue #104): stop the whole search, its workers and any
    Modal app with it, then exit. The checkpoint file keeps what was finished; the folder stays for the rerun."""
    if _stopping[0]:                  # the signal can arrive twice (uv passes it on too)
        return
    _stopping[0] = True
    proc = _child[0]
    if proc is not None:
        # Not proc.wait(): the interrupted main code may be inside it, holding its lock.
        try:
            os.killpg(proc.pid, signal.SIGTERM)   # remote_run stops its Modal app on SIGTERM
            deadline = time.time() + 60
            while time.time() < deadline and os.waitpid(proc.pid, os.WNOHANG)[0] != proc.pid:
                time.sleep(0.2)
        except (ProcessLookupError, ChildProcessError):
            pass
        try:
            os.killpg(proc.pid, signal.SIGKILL)   # anything left in the group
        except (ProcessLookupError, PermissionError):
            pass
    print(f"run_experiment: stopped (signal {signum}); finished units are kept in data/checkpoints/", flush=True)
    sys.exit(128 + signum)


def run_child(cmd, timeout=None, env=None):
    """subprocess.run in its own process group, so a stop or a timeout ends every process the search started."""
    proc = subprocess.Popen(cmd, cwd=ROOT, env=env, start_new_session=True)
    _child[0] = proc
    try:
        return proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        proc.wait()
        raise
    finally:
        _child[0] = None


def load_champion():
    return json.loads(CHAMPION.read_text()) if CHAMPION.exists() else None


def main():
    ap = argparse.ArgumentParser()
    # no time limit by default (Alexis, 2026-10-27, issue #96): a run takes as long as it needs; pass a
    # budget only for a deliberate cap. ctx.time_left() is then infinite and no clock check skips work.
    ap.add_argument("--budget", type=float, default=0.0, help="seconds; 0 (the default) means no limit")
    ap.add_argument("--no-commit", action="store_true")
    ap.add_argument("--rerender", action="store_true", help="rebuild all experiment.md files and exit")
    args = ap.parse_args()
    if args.rerender:
        rerender(); return

    meta = load_experiment_meta()
    for sig in (signal.SIGTERM, signal.SIGHUP, signal.SIGINT):
        signal.signal(sig, _stop)
    resumed = unfinished_folder(ATTACK.read_bytes())
    if resumed:                       # a stopped run of this same attack.py: same number, resumes its checkpoint
        exp_id = int(resumed.name[:4])
        tag = f"{exp_id:04d}-{meta['slug']}"
        if resumed.name != tag:
            resumed.rename(EXPERIMENTS / tag)
        print(f"run_experiment: resuming {tag} ({len(checkpoint.load(checkpoint.path_for(ATTACK)))} units saved)")
    else:
        exp_id = next_id()
        tag = f"{exp_id:04d}-{meta['slug']}"
    outdir = EXPERIMENTS / tag
    outdir.mkdir(parents=True, exist_ok=True)
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
        progress = ROOT / "data" / "experiment-progress.json"     # ctx.progress's file (issue #97)
        progress.unlink(missing_ok=True)
        limited = args.budget > 0
        budget = str(args.budget) if limited else "inf"
        timeout = args.budget + 600 if limited else None
        ran_remote = False
        if compute_where() == "modal":    # issue #99: the search runs on Modal; gates and record stay here
            rc = run_child(["uv", "run", "--with", "modal", "python", str(ROOT / "tools" / "remote_run.py"),
                            str(ATTACK), str(raw_path), budget], timeout=timeout)
            ran_remote = rc == 0
            if not ran_remote:
                print(f"Modal unavailable; running locally on {LOCAL_FALLBACK_WORKERS} workers")
        if not ran_remote:
            env = dict(os.environ)
            if compute_where() == "modal":   # the fallback: fewer workers, so the laptop runs cooler
                env["K4_MAX_WORKERS"] = str(LOCAL_FALLBACK_WORKERS)
            run_child([sys.executable, str(ROOT / "_runner.py"), str(ATTACK), str(raw_path), budget],
                      timeout=timeout, env=env)
    except subprocess.TimeoutExpired:
        status = "timeout"
    seconds = time.time() - t0
    (ROOT / "data" / "experiment-progress.json").unlink(missing_ok=True)
    phases["run"] = seconds
    t_record = time.time()
    raw = json.loads(raw_path.read_text()) if raw_path.exists() else {"candidates": [], "bounds": {}, "error": "no output", "worked_example": "", "notes": ""}
    if raw.get("error"):
        status = "error"

    # Gate and score. Gates in order: length, alphabet, the 24 known letters, re-encryption
    # (kryptos.gates), then the baseline gate decided 2026-10-15 (issue #23): the reading's
    # English score must beat every shuffled-copper control the attack ran with the same method
    # (raw["controls"], at least 10 scores); no controls, no keep. The key's size is counted by
    # the harness (key_bits_of: the length of the key's description) and charged in the loss;
    # it is not a gate.
    controls = [float(x) for x in raw.get("controls", []) if x is not None]
    scored = []
    earlier = readings_before(EXPERIMENTS, exp_id)
    for c in raw["candidates"]:
        g = run_gates(c["plaintext"], c.get("reencrypted"))
        bits = key_bits_of(c.get("key"))      # the harness counts the key's description; the attack's figure is kept for reference
        row = {**c, "key_bits_declared": c.get("key_bits"), "key_bits": bits, "gate_passed": g.passed,
               "failed_at": g.failed_at, "crib_hits": g.crib_hits,
               "crib_words": g.crib_words, "gate_details": g.details, "english_free": None, "fitness": None,
               "loss": None}
        if g.failed_at in (None, "cribs"):  # valid candidates get a loss; invalid ones do not
            row["loss"] = loss(c["plaintext"], bits, g.crib_hits)
        if g.passed and resubmitted(c, exp_id, earlier):   # counts once, where it was found (Alexis 2026-10-27, #94)
            row.update(gate_passed=False, failed_at="resubmitted",
                       gate_details={"rule": "a reading counts only in the search that found it"})
        elif g.passed and undetermined(c):     # a whole reading only (Alexis 2026-10-25, issue #88)
            row.update(gate_passed=False, failed_at="undetermined",
                       gate_details={"open_slots": c.get("open_slots"), "rule": "every letter fixed by the key"})
        elif g.passed:
            row["english_free"] = english_score(free_text(c["plaintext"]))
            row["fitness"] = fitness(c["plaintext"], bits)
            if len(controls) < 10 or row["english_free"] <= max(controls):
                row.update(gate_passed=False, failed_at="baseline",
                           gate_details={"english": round(row["english_free"], 3), "controls": len(controls),
                                         "best_control": round(max(controls), 3) if controls else None})
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

    # readable words: a language model marks the English words in the readings that passed every
    # gate (and the five closest that did not), checked against the dictionary; best effort, never
    # fatal, and it never changes the score or the decision. See tools/readable_words.py.
    try:
        from tools.readable_words import words_for
        pick = [c for c in scored if c.get("gate_passed")]
        pick += sorted([c for c in scored if not c.get("gate_passed") and c.get("loss") is not None], key=lambda c: c["loss"])[:5]
        found = words_for([c["plaintext"] for c in pick if len(c.get("plaintext", "")) == 97])
        for c in scored:
            if c.get("plaintext") in found:
                c["readable_words"] = found[c["plaintext"]]
    except Exception as e:  # noqa: BLE001
        print("readable words skipped:", e)
    phases["record"] = time.time() - t_record
    phases = {k: round(v, 1) for k, v in phases.items()}
    result = {
        "id": exp_id, "tag": tag, "started": started, "seconds": round(seconds, 1), "status": status,
        "phases": phases, "ended_epoch": time.time(),
        "decision": decision, "decision_rule": "loss", "n_candidates": len(scored), "n_passed": len(passed),
        "best_crib_hits": best_hits, "best_crib_words": best_words, "best_fitness": best["fitness"] if best else None,
        "best_loss": best_loss, "gates": "length, alphabet, cribs, reencryption, baseline",
        "controls": controls,
        "champion_before": champion, "bounds": raw.get("bounds", {}), "notes": raw.get("notes", ""), "judge": raw.get("judge"),
        "error": raw.get("error"), "candidates": scored,
    }
    (outdir / "result.json").write_text(json.dumps(result, indent=1))
    (outdir / "worked_example.txt").write_text(raw.get("worked_example", "") or "")
    (outdir / "experiment.md").write_text(render_md(meta, result, raw))
    if status == "ran":               # recorded: the finished units are in the record now (issue #105)
        checkpoint.path_for(ATTACK).unlink(missing_ok=True)

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
        # refresh the public repository and site in the background (tools/publish.py, issue #66)
        (ROOT / "logs").mkdir(exist_ok=True)
        with open(ROOT / "logs" / "publish.log", "a") as log:
            subprocess.Popen(["uv", "run", "python", str(ROOT / "tools" / "publish.py")], cwd=ROOT,
                             stdout=log, stderr=subprocess.STDOUT, start_new_session=True)


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
Best loss: {result['best_loss']} (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: {result['best_fitness']}. Champion before this run: {(result['champion_before'] or {}).get('experiment', 'none')}.

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
