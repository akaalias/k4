"""Experiment 0257. See program.md for the contract."""

EXPERIMENT = {
    "slug": "d1b-two-free-alphabets-power-per-run-at-13-and-16",
    "title": "D1b: design 2's power per run for two free alphabets (Quagmire IV), 24 clean and 24 Sanborn-style plants at F1.2's sampled lengths 13 and 16, every run's best recorded",
    "family": "1-keyed-periodic",
    "parent": "0229-d1-one-free-alphabet-power-per-run-with-enough-plants",
    "changed": (
        "D1b (issue #77). 0229 measured design 2's power per run for one free alphabet and D1 qualified a one-run decider "
        "(Alexis, 2026-10-28, #100). Here the same measurement for two free alphabets with 0144's compiled tempering, unchanged: "
        "F1.2's sampled lengths 13 and 16, 24 clean and 24 Sanborn-style plants each, 6 kept-place copies per plant, ten "
        "full runs per text with each run's best recorded. Two lengths so the power can be checked for sameness across the "
        "class before one measured power is used for every two-alphabet setting (F1.4's 1,346 two-alphabet settings, F1.2 13)."
    ),
    "hypothesis_expert": (
        "F1.5 design 2 (0143, 0144, 0146) closed F1.2's lengths 8, 13 and 16 on power from 4-5 clean plants each; 0226 and "
        "0228 redrew L13 on Sanborn-style plants (9/12, 8/12) and on clean ones (2/5): two-alphabet power is in doubt and "
        "rests on too few plants. Two questions on one set of climbs, as 0229 for one alphabet: (1) design 2's ten-run power "
        "at 13 and 16 on clean and Sanborn-style text (judge bench classes xstops, k123, sub3; A6, C17, C19), 24 plants per "
        "class and length; (2) the power of the first r runs, r = 1-10. D1's rule (Alexis, #100): a cheaper decider "
        "qualifies when its power pooled over the cells (here 96 plants) is within 5 of the reference on the same plants. "
        "Sameness: the one-run power at 13 and at 16 within 5 of 48 of each other. Clue entries C27(c) (two alphabets: "
        "Sanborn's 'slightly different' tableau on both sides)."
    ),
    "hypothesis_eli5": (
        "For the hardest version of the cipher, with two scrambled alphabets, our search tool's success rate was measured on "
        "only a handful of hidden test messages, and the counts disagreed between tries. Here we hide 96 test messages, half "
        "plain book English and half written Sanborn's way, and count how many the tool finds after one search, two, and so "
        "on up to ten. If one search finds about as many as ten, the tool becomes about thirty times cheaper, and two thousand "
        "untested settings come within reach."
    ),
    "prediction": (
        "Ten-run power at 13 about 0.6 clean and 0.6 Sanborn-style, at 16 a little higher (fewer checks keep less of the "
        "copies' freedom out, but longer columns read better). As for one alphabet, power flat in the number of runs: one "
        "run within 5 of 96 of ten, so a one-run decider qualifies for two alphabets; 13 and 16 within 5 of 48. Zero candidates."
    ),
    "method": (
        "1. Per length (13, 16): 24 clean plants (0144's plant4: a Carter window with the known words, two random alphabets, a "
        "random key) and 24 Sanborn-style (0226's class texts, two arms: 8 xstops, 8 K1-K3 windows, 8 with three letters "
        "changed), each with an exact witness (0123's decider through 0144's witness4, 20 s alarm, redrawn if slow). "
        "2. Six own copies per plant: the carved letters at the 24 known places kept, the other 73 shuffled (0143's copies, fit "
        "by construction), started from the plant's witness. "
        "3. Every text climbed by 0144's compiled tempering, unchanged: 10 runs of 16 replicas x 625 rounds x 1000 moves, each "
        "run's best recorded. "
        "4. Power at r = 1-10 by length and class: a plant is found at r when the best of its first r runs is strictly above the "
        "best of the first r runs of each own copy (null 1/7)."
    ),
    "walkthrough": (
        "1. Hide a test message under two shuffled alphabets (one for plain letters, one for cipher letters) and a key of 13 "
        "(or 16) numbers. "
        "2. Make six scrambled copies of its ciphertext that keep the carved letters at the 24 known places. "
        "3. Run the tempering search ten times on each of the seven texts, writing down the best score after each run. "
        "4. After run r, is the hidden message's best above all six copies' bests? "
        "5. Over 96 hidden messages, the share found after r runs is the tool's power at that cost."
    ),
    "expected_minutes": 90,
}

import ctypes
import importlib.util
import random
import signal
import time
from pathlib import Path

N = 97
ROOT = Path(__file__).resolve().parent
LENGTHS = ("13", "16")
ARMS = {"13": (0, 1), "16": (2, 0)}
PLANTS = 24
RUNS = 10
ROUNDS = 625
N_OWN = 6
_MODS = {}


def _load(e):
    if e not in _MODS:
        import sys
        path = next((ROOT / "experiments").glob(f"{e}-*")) / "attack.py"
        spec = importlib.util.spec_from_file_location(f"frozen{e}", path)
        m = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = m
        spec.loader.exec_module(m)
        if hasattr(m, "ROOT"):
            m.ROOT = ROOT
        _MODS[e] = m
    return _MODS[e]


class _Slow(Exception):
    pass


def _witness(m44, m23, pc, known, L, rng, secs=20):
    """0144's witness under an alarm (0226's rule): 0123's search can run for minutes on some keys."""
    def _raise(*_):
        raise _Slow()
    old = signal.signal(signal.SIGALRM, _raise)
    signal.alarm(secs)
    try:
        return m44.witness4(pc, known, L, rng, m23)
    except _Slow:
        return None
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)


def runs_scores(L, text, seed, y0):
    """Each tempering run's best score and wall time: 0144's two-alphabet climb, unchanged."""
    from kryptos.facts import KNOWN
    m = _load("0144")
    L_ = m.lib4()
    kp = sorted(KNOWN)
    CT = (ctypes.c_int * N)(*[ord(ch) - 65 for ch in text])
    KP = (ctypes.c_int * 24)(*[q - 1 for q in kp])
    KL = (ctypes.c_int * 24)(*[ord(KNOWN[q]) - 65 for q in kp])
    L_.setup(m._LIB["tab"], CT, N, L, KP, KL, 24)
    L_.set_start((ctypes.c_int * 52)(*y0))
    out = []
    for r in range(RUNS):
        t0 = time.time()
        bp = (ctypes.c_int * 128)(); bx = (ctypes.c_int * 52)(); bk = (ctypes.c_int * 64)()
        sc = L_.ptemper(seed * 100003 + r, 1, m.PT_R, ROUNDS, m.PT_MOVES, m.PT_T0, m.T1, bp, bx, bk)
        out.append([round(sc, 5), round(time.time() - t0, 2)])
    return out


def _job(args):
    key, L, text, seed, y0 = args
    return key, runs_scores(L, text, seed, y0)


def build(ctx):
    known = ctx.KNOWN
    m44, m26 = _load("0144"), _load("0226")
    m23 = m44.load_0123()
    m44.lib(); m44.lib4()
    kidx = set(q - 1 for q in known)
    free = [j for j in range(N) if j not in kidx]
    jobs, meta = [], {}
    for Ls in LENGTHS:
        L = int(Ls)
        rng = random.Random(2550 + L)
        plants = []
        while len(plants) < PLANTS:
            pc, pt = m44.plant4(L, rng, known)
            y0 = _witness(m44, m23, pc, known, L, rng)
            if y0 is not None:
                plants.append(("clean", pt, pc, y0))
        for a in ARMS[Ls]:
            for cls, pt in m26.class_texts(rng, a):
                y0 = None
                while y0 is None:
                    P = list(range(26)); C = list(range(26)); rng.shuffle(P); rng.shuffle(C)
                    Ci = {v: j for j, v in enumerate(C)}
                    k = [rng.randrange(26) for _ in range(L)]
                    pc = "".join(chr(65 + Ci[(P[ord(ch) - 65] + k[j % L]) % 26]) for j, ch in enumerate(pt))
                    y0 = _witness(m44, m23, pc, known, L, rng)
                plants.append((cls, pt, pc, y0))
        for i, (cls, pt, pc, y0) in enumerate(plants):
            meta[(Ls, i)] = {"cls": cls}
            jobs.append((f"{Ls}:plant:{i}", L, pc, rng.randrange(10 ** 9), y0))
            for g in range(N_OWN):
                letters = [pc[j] for j in free]; rng.shuffle(letters)
                cp = list(pc)
                for j, ch in zip(free, letters):
                    cp[j] = ch
                jobs.append((f"{Ls}:own:{i * 100 + g}", L, "".join(cp), rng.randrange(10 ** 9), y0))
    return jobs, meta


def power(res, meta, Ls, r, cls=None):
    found = of = 0
    for (a, i), v in meta.items():
        if a != Ls or (cls and (v["cls"] == "clean") != (cls == "clean")):
            continue
        best = max(x[0] for x in res[f"{Ls}:plant:{i}"][:r])
        own = [max(x[0] for x in res[f"{Ls}:own:{i * 100 + g}"][:r]) for g in range(N_OWN)]
        found += best > max(own)
        of += 1
    return [found, of]


def run(ctx):
    import multiprocessing as mp
    import os
    import sys
    import types
    t_start = time.time()
    jobs, meta = build(ctx)
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    saved = getattr(ctx, "saved", {}) or {}
    res = {j[0]: saved[j[0]] for j in jobs if j[0] in saved}      # units an earlier run of this attack.py finished (#105)
    todo = [j for j in jobs if j[0] not in res]
    W = int(os.environ.get("K4_WORKERS", 8))
    ctx.progress(len(res), len(jobs), "texts")
    with mp.get_context("fork").Pool(W) as pool:
        for key, s in pool.imap_unordered(_job, todo, chunksize=1):
            res[key] = s
            ctx.save(key, s)
            ctx.progress(len(res), len(jobs), "texts")
    table = {}
    for Ls in LENGTHS:
        for r in range(1, RUNS + 1):
            table[f"{Ls}/{r}"] = {"clean": power(res, meta, Ls, r, "clean"), "messy": power(res, meta, Ls, r, "messy")}
    pooled = {r: sum(table[f"{Ls}/{r}"][c][0] for Ls in LENGTHS for c in ("clean", "messy")) for r in range(1, RUNS + 1)}
    ref = pooled[RUNS]
    qualifying = [r for r in range(1, RUNS + 1) if pooled[r] >= ref - 5]
    one = {Ls: table[f"{Ls}/1"]["clean"][0] + table[f"{Ls}/1"]["messy"][0] for Ls in LENGTHS}
    same = abs(one["13"] - one["16"]) <= 5
    by_class = {}
    for Ls in LENGTHS:
        for cls in ("clean", "xstops", "k123", "sub3"):
            ids = [i for (a, i), v in meta.items() if a == Ls and v["cls"] == cls]
            f = 0
            for i in ids:
                own = [max(x[0] for x in res[f"{Ls}:own:{i * 100 + g}"]) for g in range(N_OWN)]
                f += max(x[0] for x in res[f"{Ls}:plant:{i}"]) > max(own)
            by_class[f"{Ls}/{cls}"] = [f, len(ids)]
    times = [sum(x[1] for x in s) for s in res.values()]
    seq = sum(1 / (j + 1) for j in range(12))
    bounds = {
        "item": "D1b", "decider": "F1.5 design 2 for two free alphabets: 0144's compiled tempering (16 replicas x 625 rounds x 1000 moves per run), unchanged",
        "lengths": list(LENGTHS), "plants_per_class": PLANTS, "own_copies": N_OWN, "null_per_plant": "1/7",
        "copies": "kept-place copies (0143): the carved letters at the 24 known places kept, the other 73 shuffled",
        "runs": RUNS, "power_table": table, "pooled_power_by_runs": pooled, "reference_ten_runs_pooled": [ref, 4 * PLANTS],
        "power_by_class_ten_runs": by_class, "qualifying_runs_within_5_of_96": qualifying,
        "one_run_pooled": [pooled[1], 4 * PLANTS], "one_run_by_length": one, "same_power_13_16_within_5": same,
        "d1b_reached_one_run": 1 in qualifying and same,
        "cost_factor_per_setting_one_run": round(10 * (1 + 12) / (1 + seq), 1),
        "seconds_per_text_ten_runs": round(sum(times) / len(times), 1), "texts": len(jobs),
        "compute_seconds": round(time.time() - t_start), "exhaustive": False,
        "modal_cost_estimate": "672 texts x about 207 s (0228's L13 time for ten runs) = about 39 core-hours, about $2 of Modal credit",
    }
    notes = (f"D1b: pooled power by runs {pooled}; one run {pooled[1]}/96 against ten {ref}/96; one run at 13 {one['13']}/48, "
             f"at 16 {one['16']}/48; qualifying runs {qualifying}; one-run decider {'qualifies' if bounds['d1b_reached_one_run'] else 'does not qualify'}")
    controls = [max(x[0] for x in s) for k, s in res.items() if ":own:" in k]
    return {"candidates": [], "bounds": bounds, "notes": notes, "controls": controls}


def encrypt(plaintext, key):
    """No candidate is submitted."""
    return plaintext


def worked_example(ctx, key):
    return "\n".join([
        "D1b measures how fast design 2 finds a planted message under two free alphabets. For one plant and its six copies:", "",
        "  run          1      2      3   ...   10",
        "  plant      best of runs 1..r",
        "  copies     best of runs 1..r, each",
        "  found at r when the plant's best is above every copy's best.", "",
        "Over 96 plants at key lengths 13 and 16: one run qualifies when it finds within 5 of what ten runs find."])
