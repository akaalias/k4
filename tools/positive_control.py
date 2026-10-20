"""Positive controls for closed items (assumption A3, issue #73).

A closed item rests on an experiment whose search found nothing on K4. A control plants a message made
with that item's own method and a key inside its space, runs the experiment's saved attack.py unchanged
on the planted ciphertext, and checks that the plant is found. A control that fails reopens the item.

Each control is a folder controls/<ID>/ with a spec.py the loop writes:

    ITEM = "F1.1"                 # the order-of-work item
    EXPERIMENT = "0119"           # the experiment whose search closed it
    WHAT = "one sentence: the method and the planted key"
    BUDGET = 1800                 # seconds, optional (default 1800, the experiments' own budget)
    PATCH = [(old, new)]          # optional: exact replacements in the snapshot, only for lines that pin K4 itself
                                  # (an assert of K4's recorded result); recorded in result.json

    def plant():                  # -> {"plaintext": ..., "key": ...} and optionally "ciphertext"
        ...                       #    without "ciphertext", the attack's own encrypt(plaintext, key) makes it
    def found(result, plant):     # result: what attack.run returned on the planted text
        ...                       # -> (True/False, "why, in one line")

kryptos.plants.english_plant(seed) gives 97 letters of English with the known words in place.

    uv run python tools/positive_control.py controls/C-F1.1            # run one, write result.json
    uv run python tools/positive_control.py controls/C-F1.1 --budget 300

Writes controls/<ID>/result.json and a row in controls.tsv (one row per control, replaced on rerun).
The attack runs in a child process with forked workers, so a pool inside the attack sees the saved
attack.py, not the one at the repository root.
"""
import argparse
import csv
import importlib.util
import json
import multiprocessing as mp
import subprocess
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from types import ModuleType, SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
TSV = ROOT / "controls.tsv"
COLS = ["id", "item", "experiment", "passed", "seconds", "why", "what", "date"]


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def load_attack(path, patches=()):
    """Load a saved attack.py as the harness ran it: from the repository root. Older snapshots find their
    data files next to their own __file__ (data/, knowledge/sources/), so __file__ is set to ROOT/attack.py;
    tracebacks still name the snapshot.

    patches: the spec's optional PATCH, a list of (old, new) exact replacements in the snapshot's source. Only for
    lines that pin K4 itself (an assert that K4 gives its recorded result), never the search; each must match
    exactly once, and every patch is written into result.json."""
    src = Path(path).read_text()
    for old, new in patches:
        if src.count(old) != 1:
            raise ValueError(f"PATCH must match the snapshot exactly once, matched {src.count(old)} times: {old!r}")
        src = src.replace(old, new)
    mod = ModuleType("attack")
    mod.__file__ = str(ROOT / "attack.py")
    sys.modules["attack"] = mod
    exec(compile(src, str(path), "exec"), mod.__dict__)
    return mod


def snapshot(exp):
    hits = sorted(ROOT.glob(f"experiments/{exp}-*/attack.py"))
    if not hits:
        raise SystemExit(f"no experiment {exp}")
    return hits[0]


def child(spec_dir, out_path, budget):
    """Run in the child: make the planted ciphertext, run the attack on it, judge, write JSON."""
    mp.set_start_method("fork", force=True)
    from kryptos import facts, ciphers, scorer, plants
    t0 = time.time()
    out = {"error": None}
    try:
        spec = load(Path(spec_dir) / "spec.py", "control_spec")
        patches = list(getattr(spec, "PATCH", []))
        out["patches"] = patches
        attack = load_attack(snapshot(spec.EXPERIMENT), patches)
        p = spec.plant()
        if not plants.has_known(p["plaintext"]):
            raise ValueError("the planted plaintext does not carry the 24 known letters in place")
        ct = p.get("ciphertext") or attack.encrypt(p["plaintext"], p["key"])
        if len(ct) != 97 or not ct.isalpha() or not ct.isupper():
            raise ValueError(f"planted ciphertext is not 97 capital letters: {ct!r}")
        if ct == facts.K4:
            raise ValueError("the planted ciphertext is K4 itself")
        out["plant"] = {"plaintext": p["plaintext"], "key": repr(p["key"]), "ciphertext": ct}
        ctx = SimpleNamespace(
            K4=ct, KNOWN=facts.KNOWN, CRIBS=facts.CRIBS,
            KRYPTOS_ALPHABET=facts.KRYPTOS_ALPHABET, STANDARD_ALPHABET=facts.STANDARD_ALPHABET,
            vocabulary=facts.load_vocabulary(), ciphers=ciphers, english_score=scorer.english_score,
            deadline=t0 + budget, time_left=lambda: (t0 + budget) - time.time(),
            judge=lambda texts: __import__("kryptos.judge", fromlist=["judge"]).judge(texts),
        )
        res = attack.run(ctx) or {}
        ok, why = spec.found(res, p)
        out.update(passed=bool(ok), why=str(why), bounds=res.get("bounds", {}), notes=res.get("notes", ""),
                   candidates=[{k: c.get(k) for k in ("plaintext", "key", "notes")} for c in res.get("candidates", [])[:20]])
        for c in out["candidates"]:
            c["key"] = repr(c["key"])
    except Exception:  # noqa: BLE001
        out["error"] = traceback.format_exc()
        out["passed"] = False
        out["why"] = "error: " + out["error"].strip().splitlines()[-1]
    out["seconds"] = round(time.time() - t0, 1)
    Path(out_path).write_text(json.dumps(out, indent=1, default=str))


def write_row(row):
    rows = []
    if TSV.exists():
        with TSV.open() as f:
            rows = [r for r in csv.DictReader(f, delimiter="\t") if r["id"] != row["id"]]
    rows.append(row)
    rows.sort(key=lambda r: r["id"])
    with TSV.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec_dir")
    ap.add_argument("--budget", type=float)
    ap.add_argument("--child", nargs=2, metavar=("OUT", "BUDGET"), help=argparse.SUPPRESS)
    a = ap.parse_args()
    d = Path(a.spec_dir).resolve()
    if a.child:
        child(d, a.child[0], float(a.child[1]))
        return
    spec = load(d / "spec.py", "control_spec")
    budget = a.budget or getattr(spec, "BUDGET", 1800)
    out = d / "result.json"
    t0 = time.time()
    try:
        subprocess.run([sys.executable, __file__, str(d), "--child", str(out), str(budget)], cwd=ROOT,
                       timeout=budget + 120, check=False)
    except subprocess.TimeoutExpired:
        out.write_text(json.dumps({"passed": False, "why": f"timed out after {budget:.0f} s", "error": "timeout"}))
    r = json.loads(out.read_text()) if out.exists() else {"passed": False, "why": "no output"}
    row = {"id": d.name, "item": spec.ITEM, "experiment": spec.EXPERIMENT, "passed": "yes" if r.get("passed") else "no",
           "seconds": f"{time.time() - t0:.0f}", "why": r.get("why", "").replace("\t", " ").replace("\n", " "),
           "what": getattr(spec, "WHAT", "").replace("\t", " "), "date": datetime.now(timezone.utc).strftime("%Y-%m-%d")}
    write_row(row)
    print(f"{row['id']} ({row['item']}, experiment {row['experiment']}): {'PASSED' if r.get('passed') else 'FAILED'}: {row['why']}")


if __name__ == "__main__":
    main()
