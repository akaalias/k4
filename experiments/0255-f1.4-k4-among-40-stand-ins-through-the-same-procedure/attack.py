"""Experiment 0255. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f1.4-k4-among-40-stand-ins-through-the-same-procedure",
    "title": "F1.4: K4's rate of beating its copies ranked among 40 shuffled stand-ins, each on 80 of its own fitting key schedules through 0253's procedure",
    "family": "1-keyed-periodic",
    "parent": "0254-f1.4-replicate-the-excess-with-fresh-copies-and-null-targets",
    "changed": (
        "F1.4, second replication of 0253's excess. 0254 found K4 above all 12 copies in 13.3% of its schedules (0253: "
        "14.3%), but four shuffled stand-ins through the identical procedure gave 10.2%, 7.2%, 1.5% and 17.5%: the rate "
        "belongs to the text and is shared across its schedules, so the per-schedule null (1 in 13) is wrong and 0253's "
        "binomial p meaningless. The pre-registered verdict was 'unclear' (pooled stand-ins 9.1%, z 2.47). Here the "
        "procedure's null is measured as a distribution over texts: 40 stand-ins and K4, 80 fitting schedules each, fresh seeds."
    ),
    "hypothesis_expert": (
        "F1.4 (one free alphabet, hand key schedules; C20(d), C27(c)), decided by 0253's decide() (one tempering run on the "
        "target, fitting shuffles climbed one at a time, at most 12). The quantity is each text's rate of beating all 12 "
        "copies over its own fitting schedules. If K4 carries a message under some schedule, its rate is lifted only near "
        "that schedule; if the rate reflects how a text's letters sit at the 24 known places (shared by all schedules), "
        "stand-ins vary as much as K4. K4's rank among 41 texts gives p to 1/41."
    ),
    "hypothesis_eli5": (
        "The test said K4 beats its scrambled copies more often than chance, but four scrambled copies of K4 put through the "
        "same test ranged from far below to above K4. Here 40 of them go through it beside K4, so we can see where K4 falls "
        "among texts that certainly hide no message."
    ),
    "prediction": (
        "K4's rate inside the stand-ins' spread: rank between 5th and 30th of 41 (one-sided p above 0.1); the stand-ins' rates "
        "spread with a standard deviation of about 5 points around 9%. Zero candidates."
    ),
    "method": (
        "1. Targets: K4 and 40 shuffles of K4 (seed 2551). Each target's cell: every schedule of 0252's list it fits exactly. "
        "2. 80 schedules drawn at random from each cell; per schedule 0253's decide() without escalation. "
        "3. Each target's rate (above all 12) and its rate of beating the first copy; K4's rank among the 41 on each, "
        "one-sided p = (1 + stand-ins at or above K4) / 41. A lead only if p is at most 1/41 on the rate."
    ),
    "walkthrough": (
        "1. Shuffle K4's letters 40 times to make 40 stand-ins. "
        "2. For each, find the key-stepping rules it fits with some alphabet, and pick 80 at random. "
        "3. For each rule, search for the stand-in's most English-looking reading, then search scrambled copies of it that "
        "fit the same rule, one at a time, until one reads as well (at most 12). "
        "4. Each stand-in's share of rules where it beat all 12 is its rate. Do the same for K4. "
        "5. Where does K4's rate fall among the 40?"
    ),
    "expected_minutes": 150,
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
N_STANDIN = 40
SAMPLE = 80
SEED = 2551
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
    sr = [per[t]["rate"] for t in per if t != "k4"]
    sf = [per[t]["beat_first_rate"] for t in per if t != "k4"]
    kr, kf = per["k4"]["rate"], per["k4"]["beat_first_rate"]
    ge_r = sum(1 for x in sr if x >= kr); ge_f = sum(1 for x in sf if x >= kf)
    p_r, p_f = (1 + ge_r) / (len(sr) + 1), (1 + ge_f) / (len(sf) + 1)
    mean = sum(sr) / len(sr); sd = (sum((x - mean) ** 2 for x in sr) / (len(sr) - 1)) ** 0.5
    bounds = {
        "item": "F1.4, K4 among 40 stand-ins (second replication of 0253's excess)",
        "decider": "0253's decide(), imported unchanged: one tempering run on the target, fitting shuffles climbed one at a time, at most 12",
        "targets": per, "schedules_per_target": SAMPLE, "fair_rate_12": round(1 / 13, 4),
        "k4_rate": kr, "standins_rate_mean": round(mean, 4), "standins_rate_sd": round(sd, 4),
        "standins_rate_min_max": [min(sr), max(sr)], "standins_at_or_above_k4_rate": ge_r, "p_rate": round(p_r, 4),
        "k4_beat_first_rate": kf, "standins_at_or_above_k4_beat_first": ge_f, "p_beat_first": round(p_f, 4),
        "lead": p_r <= 1 / 41,
        "core_seconds": round(sum(v["secs"] for v in res.values())), "compute_seconds": round(time.time() - t0),
        "exhaustive": False,
        "modal_cost_estimate": "41 targets x 80 schedules x about 4 climbs x about 17 s: about 223,000 core-seconds, about $3.5 of Modal credit (credit left about $15 after the margin)",
    }
    notes = (f"K4 among 40 stand-ins: K4 rate {kr:.3f}, stand-ins mean {mean:.3f} (sd {sd:.3f}, range {min(sr):.3f}-{max(sr):.3f}); "
             f"{ge_r} of 40 at or above K4, p {p_r:.3f}; beat-first rate p {p_f:.3f}. {'LEAD' if p_r <= 1 / 41 else 'K4 inside its stand-ins'}.")
    controls = [c for k, v in res.items() if k.startswith("k4:") for c in v["copies"]][:2000]
    return {"candidates": [], "bounds": bounds, "notes": notes, "controls": controls}


def encrypt(plaintext, key):
    """No candidate is submitted."""
    return A().encrypt(plaintext, key)


def worked_example(ctx, key):
    return "\n".join([
        "K4 among 40 stand-ins: where does its rate fall?", "",
        "  target       fitting schedules   80 drawn   above all 12 copies",
        "  K4           2,093               80         ?   (0253: 14.3%, 0254: 13.3%)",
        "  stand-in 1   its own             80         ?",
        "  ... 40 stand-ins (shuffles of K4), the same procedure", "",
        "  K4's rank among the 41 texts is the verdict."])
