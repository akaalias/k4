"""Experiment 0254. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f1.4-replicate-the-excess-with-fresh-copies-and-null-targets",
    "title": "F1.4: replicate 0253's excess (K4 above all 12 copies in 299 of 2,093 settings, chance 161): K4 on 400 of its settings with fresh copies, four shuffled stand-ins for K4 through the same procedure, and the 25 strongest of K4's 66 settings above all 100 against 100 fresh copies",
    "family": "1-keyed-periodic",
    "parent": "0253-f1.4-one-alphabet-residue-decided-by-the-one-run-decider",
    "changed": (
        "F1.4, replication (program.md: a result outside the copies' range stops the queue). 0253 found K4 above all 12 of "
        "its own copies in 299 of 2,093 settings (chance 161, binomial p 1e-24) and above all 100 in 66 (chance 21), with "
        "junk readings and the excess spread over the whole cell (K4 beat its first copy in 61% of settings, not 50%). "
        "Before reading it as K4's, test the procedure: (A) K4 on 400 of its fitting settings drawn at random, fresh seeds "
        "and copies; (B) four shuffles of K4 stand in for K4: each gets its own fitting settings (the same exact decider over "
        "the same schedule list), 400 drawn at random, and the identical decision; (C) the 25 strongest of K4's 66 settings "
        "above all 100 (all that 0253's record lists), each against 100 fresh copies. The selection of settings by the target, and the copies being fitting shuffles, are the "
        "same in A and B, so B is the procedure's own null."
    ),
    "hypothesis_expert": (
        "F1.4 (a keyed table with a hand key schedule, one free alphabet on both sides, Beaufort or added; C20(d), C27(c)). "
        "0253 decided each of K4's 2,093 fitting settings with D1's one-run decider (0140's tempering generalised to slot "
        "maps, 0252) against fitting shuffles climbed one at a time. The per-setting null (1/13 above all 12) assumes K4 "
        "and a fitting shuffle are exchangeable once both fit. They may not be: the setting list was filtered by K4 (a "
        "setting that K4 fits may fit it more loosely than a random fitting shuffle), and a fitting shuffle may keep fewer "
        "free alphabet letters. If the stand-ins (B) show the same excess as K4 (A), the excess belongs to the procedure "
        "and 0253's verdict must be read against B's rate, not 1/13; if B sits at 1/13 and A replicates, the excess is K4's "
        "and is chased (C says whether particular settings carry it)."
    ),
    "hypothesis_eli5": (
        "Yesterday's test said K4 reads more like English than its scrambled copies far more often than chance allows, but "
        "its best readings are gibberish. Before believing it, we check the test itself: we pretend four scrambled copies "
        "of K4 are the real thing and put each through exactly the same procedure. If they also 'beat their copies' too "
        "often, the test is biased, not K4 special."
    ),
    "prediction": (
        "B shows an excess like A's (stand-ins above all 12 copies in about 12-15% of their settings, against 7.7% for a fair "
        "test), so the excess belongs to the procedure; A replicates 0253's rate (about 14%); C: K4 above all 100 fresh "
        "copies in a few of the 25, well under 25 but above the 1% a fair test gives. Zero candidates."
    ),
    "method": (
        "1. Targets: K4 and four shuffles of K4 (seed 2541). For each target, every setting of 0252's list (0128's schedules "
        "at slot counts 2-31, back and forth, both forms) is decided exactly; the target's fitting settings are its cell. "
        "2. A and B: 400 settings drawn at random from each target's cell (seed per target); per setting 0253's decide(): "
        "one tempering run on the target, then fitting shuffles of the target climbed one at a time, stop at the first at "
        "or above, at most 12 (no escalation). Count settings where the target is above all 12. "
        "3. C: the 25 settings 0253's record lists (the strongest of the 66 where K4 was above all 100), each with 100 fresh fitting copies (decide with escalation, new seeds). "
        "4. Verdict, pre-registered: the procedure's null rate is the stand-ins' pooled rate p_B; K4's A rate against p_B by a "
        "two-proportion test; if p_B is within 2 points of K4's, the excess is the procedure's."
    ),
    "walkthrough": (
        "1. Shuffle K4's letters to make a stand-in. "
        "2. Find every key-stepping rule that the stand-in fits with some alphabet (the 24 known letters agree), as was done for K4. "
        "3. Pick 400 of those rules at random. For each, search for the stand-in's most English-looking reading, then make "
        "scrambled copies of the stand-in that fit the same rule and search them one at a time until one reads as well. "
        "4. Count the rules where the stand-in beat 12 copies. "
        "5. A fair test gives about 1 in 13. Do the same for K4 and compare."
    ),
    "expected_minutes": 120,
}

import importlib.util
import os
import random
import sys
import time
import types
from pathlib import Path

N = 97
ROOT = Path(__file__).resolve().parent
N_STANDIN = 4
SAMPLE = 400
SEED = 2541
_MODS = {}


def A():
    """0253's attack, frozen: decide() and the 0252 module behind it."""
    if "a" not in _MODS:
        path = next((ROOT / "experiments").glob("0253-*")) / "attack.py"
        spec = importlib.util.spec_from_file_location("frozen0253", path)
        a = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = a
        spec.loader.exec_module(a)
        a.ROOT = ROOT
        _MODS["a"] = a
    return _MODS["a"]


def _fit_job(args):
    group, items, text = args
    return A().M()._f14_job((group, items, text))


def _job(args):
    key, text, st, seed, esc = args
    return key, A().decide(text, st, seed, esc)


def cell_for(text, f14, pool, W):
    jobs = [(g, items[i::W * 4], text) for g, items in f14.items() for i in range(W * 4)]
    got = sorted(x for g, lst in pool.imap_unordered(_fit_job, jobs) for x in [(g, it) for it in lst])
    fit, seen = [], set()
    for g, (name, slot, n, form) in got:
        if (slot, form) not in seen:
            seen.add((slot, form)); fit.append((g, name, (slot, tuple(range(N)), n, form)))
    return fit


def run(ctx):
    import json
    import multiprocessing as mp
    from math import sqrt
    t0 = time.time()
    W = int(os.environ.get("K4_WORKERS", 8))
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    a = A(); m = a.M()
    m._load("0140"); m._load("0128"); m._load("0129"); m.glib()
    k4 = ctx.K4
    rng = random.Random(SEED)
    targets = [("k4", k4)] + [(f"standin{i}", "".join(rng.sample(k4, N))) for i in range(N_STANDIN)]
    f14 = m.f14_settings()
    cells = {}
    with mp.get_context("fork").Pool(W) as pool:
        for tid, t in targets:
            cells[tid] = cell_for(t, f14, pool, W)
    work = []
    for ti, (tid, t) in enumerate(targets):
        r = random.Random(SEED * 10 + ti)
        pick = sorted(r.sample(range(len(cells[tid])), min(SAMPLE, len(cells[tid]))))
        for i in pick:
            work.append((f"{tid}:{i}", t, cells[tid][i][2], 300000 + ti * 10000 + i, False))
    prev = json.loads((next((ROOT / "experiments").glob("0253-*")) / "result.json").read_text())["bounds"]["top_settings"]
    k4_index = {(name, form): i for i, (g, name, st) in enumerate(cells["k4"]) for form in [st[3]]}
    top = [k4_index[(t["setting"], t["form"])] for t in prev if t["above"] >= 100]
    for i in top:
        work.append((f"C:{i}", k4, cells["k4"][i][2], 500000 + i, True))
    saved = getattr(ctx, "saved", {}) or {}
    res = {w[0]: saved[w[0]] for w in work if w[0] in saved}        # units an earlier run of this attack.py finished (#105)
    todo = [w for w in work if w[0] not in res]
    ctx.progress(len(res), len(work), "settings")
    with mp.get_context("fork").Pool(W) as pool:
        for key, out in pool.imap_unordered(_job, todo, chunksize=1):
            res[key] = out
            ctx.save(key, out)
            ctx.progress(len(res), len(work), "settings")

    def rate(tid):
        ks = [k for k in res if k.startswith(tid + ":")]
        hit = sum(1 for k in ks if res[k]["above"] >= 12)
        first = sum(1 for k in ks if res[k]["above"] >= 1)
        return {"cell_size": len(cells[tid]), "sampled": len(ks), "above_all_12": hit, "rate": round(hit / len(ks), 4),
                "beat_first_copy": first, "beat_first_rate": round(first / len(ks), 4),
                "mean_copies_climbed": round(sum(len(res[k]["copies"]) for k in ks) / len(ks), 2)}
    per = {tid: rate(tid) for tid, _ in targets}
    nb = sum(per[t]["sampled"] for t in per if t != "k4"); hb = sum(per[t]["above_all_12"] for t in per if t != "k4")
    pB = hb / nb
    nA, hA = per["k4"]["sampled"], per["k4"]["above_all_12"]
    pA = hA / nA
    pp = (hA + hb) / (nA + nb)
    z = (pA - pB) / sqrt(pp * (1 - pp) * (1 / nA + 1 / nb)) if 0 < pp < 1 else 0.0
    c_above = sum(1 for i in top if res[f"C:{i}"]["above"] >= 100)
    c_list = sorted(({"setting": cells["k4"][i][1], "form": cells["k4"][i][2][3], "above": res[f"C:{i}"]["above"],
                      "score": res[f"C:{i}"]["score"]} for i in top), key=lambda d: -d["above"])
    verdict = ("procedure" if abs(pA - pB) <= 0.02 or pB >= 0.11 else
               "k4" if pB < 0.10 and z > 3 else "unclear")
    bounds = {
        "item": "F1.4 replication of 0253's excess",
        "decider": "0253's decide(), imported unchanged: one tempering run on the target, fitting shuffles climbed one at a time, at most 12 (A, B), escalated to 100 (C)",
        "targets": {tid: per[tid] for tid in per}, "fair_rate_12": round(1 / 13, 4),
        "standins_pooled": {"sampled": nb, "above_all_12": hb, "rate": round(pB, 4)},
        "k4_rate": round(pA, 4), "two_proportion_z_k4_vs_standins": round(z, 2), "verdict": verdict,
        "C_top_settings": {"count": len(top), "above_all_100_fresh": c_above, "fair_expected": round(len(top) / 101, 2), "each": c_list},
        "core_seconds": round(sum(v["secs"] for v in res.values())), "compute_seconds": round(time.time() - t0),
        "exhaustive": False,
        "modal_cost_estimate": "5 x 400 settings x about 5 climbs + 25 x about 100 climbs, about 17 s each: about 210,000 core-seconds, about $3.5 of Modal credit (credit left about $17 after the margin)",
    }
    notes = (f"0253 replication: K4 above all 12 in {hA}/{nA} ({pA:.3f}); stand-ins {hb}/{nb} ({pB:.3f}); fair 0.077; "
             f"z {z:.2f}; verdict: {verdict}. C: {c_above} of {len(top)} top settings above all 100 fresh copies.")
    controls = [c for k, v in res.items() if k.startswith("k4:") for c in v["copies"]][:2000]
    return {"candidates": [], "bounds": bounds, "notes": notes, "controls": controls}


def encrypt(plaintext, key):
    """No candidate is submitted."""
    return A().encrypt(plaintext, key)


def worked_example(ctx, key):
    return "\n".join([
        "Replication of 0253: is the excess K4's or the test's?", "",
        "  target      its fitting settings   400 drawn   above all 12 copies",
        "  K4          2,093                   400         ?   (0253: 14.3%)",
        "  stand-in 1  its own                 400         ?",
        "  ... four stand-ins (shuffles of K4), the same procedure", "",
        "  a fair test gives 1 in 13 (7.7%) for every target."])
