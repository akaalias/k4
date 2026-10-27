"""Experiment 0229. See program.md for the contract."""

EXPERIMENT = {
    "slug": "d1-one-free-alphabet-power-per-run-with-enough-plants",
    "title": "D1: design 2's power per run for one free alphabet, bounded with enough plants: 24 clean and 24 Sanborn-style plants at F1.1's Beaufort lengths 23 and 26, every run's best recorded",
    "family": "1-keyed-periodic",
    "parent": "0228-d1-design-2s-power-against-its-budget",
    "changed": (
        "D1 (issue #77), second measurement. 0228 found that one full tempering run matched ten at L23 (clean 6/8, messy "
        "7/12) but its reference power did not replicate (messy 6/12 against 0226's 10/12): 5-12 plants are too few. Here "
        "one free alphabet only (F1.1, Beaufort form), at both sampled lengths 23 and 26, with 24 clean and 24 "
        "Sanborn-style plants per length, 6 own copies each, full-length runs, every run's best recorded."
    ),
    "hypothesis_expert": (
        "F1.5 design 2 (0139-0142) closed F1.1's Beaufort lengths 23 (7 checks) and 26 (1 check) on power 6/8 and 5/6 "
        "measured with clean Carter; A6.2 (0226) and D1 (0228) redrew Sanborn-style power at 23 as 10/12 and 6/12, and "
        "L23 was reopened. Two questions on one set of climbs: (1) design 2's ten-run power at 23 and 26 on clean and on "
        "Sanborn-style text (judge bench classes xstops, k123, sub3; A6, C19, C17), with 24 plants each, enough for a 95% "
        "interval of about +-0.18; (2) the power of the first r runs, r = 1-10, against the ten-run power: the cut D1 "
        "needs. Sequential copies (stop at the first copy that beats the target) are exact and give x3.17. "
        "Pre-registered: D1 is reached for one free alphabet when the cheapest r whose power is at least the ten-run power "
        "on both classes at both lengths gives 10 x 3.17 / r >= 10, i.e. r <= 3. The ten-run power is also each cell's "
        "power for its verdict: a cell whose pooled Sanborn-style power (with 0226 and 0228 at 23) is under its stated bar "
        "(23: 6/8; 26: 5/6) stays or goes open."
    ),
    "hypothesis_eli5": (
        "Our best tool for the hardest cases seemed to work as well with one long search as with ten, which would make it "
        "ten times cheaper; but the hidden-message tests behind that used too few messages to be sure, and a second try "
        "found fewer of them than the first. Here we hide 96 test messages, half clean book English and half written the "
        "way Sanborn writes, and count how many the tool finds after one search, two, and so on up to ten."
    ),
    "prediction": (
        "Ten-run power at 23: clean about 0.70, Sanborn-style about 0.60; at 26 (one check) a little lower, about 0.6 and "
        "0.5. The first run reaches the ten-run power within one plant at both lengths, so r = 1 or 2 qualifies: D1 reached "
        "for one free alphabet (16-32 times cheaper). L23 stays open (pooled Sanborn-style under 6/8); L26 goes open too. "
        "Zero candidates."
    ),
    "method": (
        "1. Per length (23, 26): 24 clean plants (0120's make_plants rule) and 24 Sanborn-style (0226's class texts: L23 "
        "arms 0 and 1, L26 arms 2 and 0, so 8 xstops, 8 K1-K3 windows, 8 with three letters changed), each enciphered in "
        "the Beaufort form with a random alphabet and key; 6 own copies each, shuffles that 0120's exact decider fits at "
        "that length. "
        "2. Every text climbed with 0140's compiled tempering, unchanged: 10 runs of 16 replicas x 625 rounds x 1000 "
        "moves, each run's best score and time recorded. "
        "3. Power at r = 1-10 by length and class: a plant is found at r when the best of its first r runs is strictly "
        "above the best of the first r runs of each own copy (null 1/7)."
    ),
    "walkthrough": (
        "1. Hide a test message under a shuffled alphabet and a key of 23 (or 26) numbers, Beaufort form. "
        "2. Make six scrambled copies of its ciphertext that the same key length still fits. "
        "3. Run the tempering search ten times on each of the seven texts, writing down the best score after each run. "
        "4. After run r, is the hidden message's best above all six copies' bests? "
        "5. Over 96 hidden messages, the share found after r runs is the tool's power at that cost."
    ),
    "expected_minutes": 240,
}

import ctypes
import importlib.util
import random
import time
from pathlib import Path

N = 97
ROOT = Path(__file__).resolve().parent
ROUNDS = (625,)
LENGTHS = ("23", "26")
PLANTS = 24
RUNS = 10
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
            m.ROOT = ROOT          # as when it ran: paths from the repository, not its own folder (0218's error)
        _MODS[e] = m
    return _MODS[e]


def runs_scores(arm, text, seed, rounds, y0):
    """Each tempering run's best score, with its wall time: 0140's climb at key length int(arm), unchanged."""
    from kryptos.facts import KNOWN
    m = _MODS["0140"]
    L_ = m.lib()
    L = int(arm)
    kp = sorted(KNOWN)
    CT = (ctypes.c_int * N)(*[ord(ch) - 65 for ch in text])
    KP = (ctypes.c_int * 24)(*[q - 1 for q in kp])
    KL = (ctypes.c_int * 24)(*[ord(KNOWN[q]) - 65 for q in kp])
    L_.setup(m._LIB["tab"], CT, N, L, KP, KL, 24)
    out = []
    for r in range(RUNS):
        t0 = time.time()
        bp = (ctypes.c_int * 128)(); bx = (ctypes.c_int * 52)(); bk = (ctypes.c_int * 64)()
        sc = L_.ptemper(seed * 100003 + r, 1, m.PT_R, rounds, m.PT_MOVES, m.PT_T0, m.T1, bp, bx, bk)
        out.append((round(sc, 5), round(time.time() - t0, 2)))
    return out


def _job(args):
    arm, kind, idx, text, seed, rounds, y0 = args
    return arm, kind, idx, rounds, runs_scores(arm, text, seed, rounds, y0)


def build(ctx):
    """-> jobs and the plants' metadata; plants and copies made as 0139 (clean) and 0226 (classes)."""
    known = ctx.KNOWN
    m40, m26 = _load("0140"), _load("0226")
    m20 = m40.load_0120()
    m40.lib()
    texts, meta = [], {}
    arms = {"23": (0, 1), "26": (2, 0)}
    for L in LENGTHS:
        rng = random.Random(2290 + int(L))
        plants = [("clean", pt, pc) for pc, pt in m20.make_plants(known, int(L), rng, PLANTS)]
        for a in arms[L]:
            for cls, pt in m26.class_texts(rng, a):
                alpha = list(ctx.STANDARD_ALPHABET); rng.shuffle(alpha); alpha = "".join(alpha)
                k = [rng.randrange(26) for _ in range(int(L))]
                plants.append((cls, pt, m20.beaufort_encrypt(pt, alpha, k)))
        for i, (cls, pt, pc) in enumerate(plants):
            assert m20.decide(m20.equations(pc, known, int(L)), "B", rng)[0] == "fit"
            meta[(L, i)] = {"cls": cls, "pt": pt}
            texts.append((L, "plant", i, pc, rng.randrange(10 ** 9), None))
            g = 0
            while g < N_OWN:
                sh = list(pc); rng.shuffle(sh); sh = "".join(sh)
                if m20.decide(m20.equations(sh, known, int(L)), "B", rng)[0] == "fit":
                    texts.append((L, "own", i * 100 + g, sh, rng.randrange(10 ** 9), None)); g += 1
    jobs = [(a, k, i, t, s, 625, y0) for (a, k, i, t, s, y0) in texts]
    return jobs, meta


def power(res, meta, arm, rounds, r, cls=None):
    plants = {i: s for (a, k, i, rd), s in res.items() if a == arm and k == "plant" and rd == rounds}
    found = 0
    of = 0
    for i, s in plants.items():
        if cls and (meta[(arm, i)]["cls"] == "clean") != (cls == "clean"):
            continue
        own = [res[(arm, "own", i * 100 + g, rounds)] for g in range(N_OWN)]
        best = max(x[0] for x in s[:r])
        found += best > max(max(x[0] for x in o[:r]) for o in own)
        of += 1
    return found, of


def run(ctx):
    import multiprocessing as mp
    import sys
    import types
    t_start = time.time()
    jobs, meta = build(ctx)
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    res = {}
    ctx.progress(0, len(jobs), "climbs")
    with mp.get_context("fork").Pool(8) as pool:
        for arm, kind, idx, rounds, s in pool.imap_unordered(_job, jobs, chunksize=1):
            res[(arm, kind, idx, rounds)] = s
            ctx.progress(len(res), len(jobs), "climbs")
    table = {}
    for arm in LENGTHS:
        for r in range(1, RUNS + 1):
            table[f"{arm}/{r}"] = {"clean": power(res, meta, arm, 625, r, "clean"), "messy": power(res, meta, arm, 625, r, "messy"),
                                   "cost": round(r / RUNS, 2)}
    ref = {arm: table[f"{arm}/{RUNS}"] for arm in LENGTHS}
    qualifying = [r for r in range(1, RUNS + 1) if all(
        table[f"{arm}/{r}"][c][0] >= ref[arm][c][0] for arm in LENGTHS for c in ("clean", "messy"))]
    cheapest = qualifying[0] if qualifying else None
    seq = sum(1 / (j + 1) for j in range(12))
    full_factor = (1 + 12) / (1 + seq)
    factor = None if cheapest is None else round(full_factor * RUNS / cheapest, 1)
    by_class = {}
    for arm in LENGTHS:
        for cls in ("clean", "xstops", "k123", "sub3"):
            ids = [i for (a, i), v in meta.items() if a == arm and v["cls"] == cls]
            f = 0
            for i in ids:
                own = [res[(arm, "own", i * 100 + g, 625)] for g in range(N_OWN)]
                f += max(x[0] for x in res[(arm, "plant", i, 625)]) > max(max(x[0] for x in o) for o in own)
            by_class[f"{arm}/{cls}"] = [f, len(ids)]
    pooled23 = [ref["23"]["messy"][0] + 10 + 6, ref["23"]["messy"][1] + 24]
    times = [sum(x[1] for x in s) for s in res.values()]
    bounds = {
        "item": "D1", "decider": "F1.5 design 2: 0140's compiled tempering, one free alphabet, Beaufort form, unchanged",
        "lengths": list(LENGTHS), "plants_per_class": PLANTS, "own_copies": N_OWN, "null_per_plant": "1/7",
        "runs": RUNS, "rounds": 625, "reference_ten_runs": ref, "power_table": table, "power_by_class_ten_runs": by_class,
        "qualifying_runs": qualifying, "cheapest_qualifying_runs": cheapest,
        "sequential_copies_factor": round(full_factor, 2), "cost_factor_per_setting": factor,
        "d1_reached_one_alphabet": bool(factor and factor >= 10),
        "pooled_sanborn_style_L23_with_0226_0228": pooled23, "bar_L23": "6/8", "bar_L26": "5/6",
        "seconds_per_text_ten_runs": round(sum(times) / len(times), 1),
        "texts": len(jobs), "compute_seconds": round(time.time() - t_start), "exhaustive": False,
        "expected_total_time": "672 texts at about 168 s (0228's measured L23 time) = about 113,000 core-seconds, 4 h on 8 cores",
    }
    notes = (f"ten-run power L23 clean {ref['23']['clean']}, messy {ref['23']['messy']}; L26 clean {ref['26']['clean']}, "
             f"messy {ref['26']['messy']}; cheapest qualifying runs {cheapest}; factor {factor}")
    controls = [max(x[0] for x in s) for (a, k, i, rd), s in res.items() if k == "own"]
    return {"candidates": [], "bounds": bounds, "notes": notes, "controls": controls}


def encrypt(plaintext, key):
    """No candidate is submitted; Beaufort form on one alphabet for completeness (0140's rule)."""
    return _load("0140").encrypt(plaintext, key)


def worked_example(ctx, key):
    return "\n".join([
        "D1 measures how fast design 2 finds a planted message. For one plant and its six copies:", "",
        "  run          1      2      3   ...   10",
        "  plant      best of runs 1..r",
        "  copies     best of runs 1..r, each",
        "  found at r when the plant's best is above every copy's best.", "",
        "Repeated with runs a tenth as long; power at each budget is the share of plants found."])
