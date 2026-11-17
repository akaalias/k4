"""Experiment: F16.1a-r2. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f16.1a-r2-0280s-two-edge-settings-on-fresh-copies",
    "title": "F16.1a-r2: 0280's two settings where K4 beat 100 fitting copies (V10 with slips at 73-74, B10 with a slip at 69), each on 1,000 fresh fitting copies with one fresh climb for K4; flag below 0.001",
    "family": "16-simple-hand-methods",
    "parent": "0280-f16.1a-r-the-cells-only-east-closed-by-the-one-run-decider",
    "changed": (
        "F16.1a-r2 (issue #123): replication of 0280's two edge settings. 0280's attack.py imported unchanged for its "
        "witness and climb; K4 climbed once with a new seed, then 1,000 shuffles of K4 that fit the same setting on the "
        "same known letters, each climbed once with its own seed (no stopping rule)."
    ),
    "hypothesis_expert": (
        "As 0280 (F1.1/F1.6 without EAST, Quagmire III with a free alphabet, C27(c)); a result outside its copies is "
        "replicated against fresh controls before anything else (program.md). Pre-registered: per setting, p = (1 + "
        "fresh copies scoring at or above K4's fresh climb) / 1,001; a flag needs p below 0.05/49 = 0.001 (49 settings "
        "were looked at in 0280), so at most 0 copies at or above. Readings in 0280 were not English, so the expectation "
        "is chance."
    ),
    "hypothesis_eli5": (
        "In experiment 280 the carving's best message beat 100 scrambled copies at two settings, which by luck happens "
        "about once in ten runs of that size. Here each of the two gets a new search and 1,000 new copies."
    ),
    "prediction": "Both settings p above 0.001 (most likely above 0.05); K4's fresh reading not English. No candidates.",
    "method": (
        "1. The two settings from 0280's record, with their known letters (the 20 official ones less the slips). "
        "2. K4: one climb, seed 16120 + setting. 3. 1,000 fitting shuffles per setting (seeds 16130+), one climb each. "
        "4. p per setting; flag below 0.001."
    ),
    "walkthrough": (
        "1. Fix the setting: key length 10, the added form, the letters at 73 and 74 treated as slips. "
        "2. Search once for the most English message K4 gives under it. "
        "3. Make 1,000 scrambles of K4 that fit the same setting and search each once. "
        "4. Count the scrambles whose message reads at least as well as K4's."
    ),
    "expected_minutes": 20,
}

import os
import random
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent
N = 97
N_COPIES = 1000
TARGETS = [("V10", [73, 74]), ("B10", [69])]
_MODS = {}


def R():
    if "r" not in _MODS:
        import importlib.util
        path = next((ROOT / "experiments").glob("0280-*")) / "attack.py"
        spec = importlib.util.spec_from_file_location("frozen0280", path)
        m = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = m
        spec.loader.exec_module(m)
        m.ROOT = ROOT
        _MODS["r"] = m
    return _MODS["r"]


def _job(args):
    tag, text, st, known, seed = args
    r = R()
    known = {int(q): c for q, c in known.items()}
    rng = random.Random(seed)
    if text is None:                                     # a fresh fitting copy
        sh = list(_MODS["k4"])
        for _ in range(200000):
            rng.shuffle(sh)
            w = r.witness("".join(sh), st, known, rng)
            if w is not None:
                break
        else:
            return tag, None
        text = "".join(sh)
    else:
        w = r.witness(text, st, known, random.Random(1))
    sc, reading = r.climb(text, st, rng.randrange(10 ** 9), known, w)
    return tag, {"score": sc, "reading": reading}


def run(ctx):
    import multiprocessing as mp
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    r = R(); m = r.M()
    m._load("0140"); m._load("0128"); m._load("0129"); m.glib()
    _MODS["k4"] = ctx.K4
    sets = {(s["cell"], tuple(s["slips"])): s for s in r.settings_from_0274(ctx.KNOWN)}
    work = []
    for i, (cell, slips) in enumerate(TARGETS):
        s = sets[(cell, tuple(slips))]
        kn = {str(q): c for q, c in s["known"].items()}
        work.append(((i, "k4"), ctx.K4, s["st"], kn, 16120 + i))
        work += [((i, j), None, s["st"], kn, 16130 + 10000 * i + j) for j in range(N_COPIES)]
    saved = getattr(ctx, "saved", {}) or {}
    res = {w[0]: saved[f"{w[0][0]}:{w[0][1]}"] for w in work if f"{w[0][0]}:{w[0][1]}" in saved}
    todo = [w for w in work if w[0] not in res]
    W = int(os.environ.get("K4_WORKERS", 8))
    ctx.progress(len(res), len(work), "climbs")
    with mp.get_context("fork").Pool(W) as pool:
        for tag, out in pool.imap_unordered(_job, todo, chunksize=4):
            res[tag] = out
            ctx.save(f"{tag[0]}:{tag[1]}", out)
            ctx.progress(len(res), len(work), "climbs")
    out = {}
    for i, (cell, slips) in enumerate(TARGETS):
        k = res[(i, "k4")]
        cs = [res[(i, j)]["score"] for j in range(N_COPIES) if res[(i, j)]]
        at = sum(1 for c in cs if c >= k["score"])
        p = (1 + at) / (len(cs) + 1)
        out[f"{cell} {slips}"] = {"k4_score": k["score"], "k4_reading": k["reading"], "copies": len(cs), "at_or_above": at,
                                  "p": round(p, 5), "flag": p < 0.001, "copies_max": max(cs), "copies_median": sorted(cs)[len(cs) // 2],
                                  "lost_copies": N_COPIES - len(cs)}
    flags = [k for k, v in out.items() if v["flag"]]
    return {"candidates": [], "bounds": {"item": "F16.1a-r2", "settings": out, "flag_line": 0.001, "flagged": flags,
                                         "decider": "0280's witness and climb (0252's generalised 0140 tempering), one climb per text",
                                         "exhaustive": True, "aws_cost_estimate_dollars": 0.2},
            "notes": "; ".join(f"{k}: K4 {v['k4_score']}, {v['at_or_above']} of {v['copies']} fresh copies at or above, p {v['p']}" for k, v in out.items()),
            "controls": [res[(0, j)]["score"] for j in range(N_COPIES) if res[(0, j)]][:1000]}


def encrypt(plaintext, key):
    return R().encrypt(plaintext, key)


def worked_example(ctx, key):
    return "\n".join(["F16.1a-r2: two settings from 0280, one fresh search for K4 each, 1,000 fresh fitting copies each.", "",
                      "  V10, slips at 73 and 74: 0280's K4 reading CDKLDCBCBETHBTROYGINFOLLK... beat 100 copies",
                      "  B10, slip at 69:         0280's K4 reading XTWAILFLONYSDTOOIMIKCOLAN... beat 100 copies",
                      "  flag only if no fresh copy reads as well (p < 0.001, for the 49 settings 0280 looked at)"])
