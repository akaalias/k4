"""Experiment 0228. See program.md for the contract."""

EXPERIMENT = {
    "slug": "d1-design-2s-power-against-its-budget",
    "title": "D1: design 2's power against its budget: the tempering climb at full length and at a tenth, every number of runs 1-10, on clean and Sanborn-style plants at F1.1 L23 and F1.2 L13, each against its own copies",
    "family": "1-keyed-periodic",
    "parent": "0226-a6-the-climbs-power-on-sanborn-style-plaintext",
    "changed": (
        "D1 (issue #77), first measurement. Design 2 (F1.5) costs 20-30 min per setting: 10 independent tempering runs "
        "(16 replicas x 625 rounds x 1000 moves) on K4, 12 copies and a power test. Two cuts are measured here on the "
        "same plants: fewer runs (each run's best is recorded, so power at 1-10 runs comes from one pass) and runs a tenth "
        "as long (62 rounds, a second pass). Plants: clean Carter (0139's and 0143's rule) and A6.2's Sanborn-style "
        "classes (0226), at F1.1's Beaufort L23 (0140's compiled climb) and F1.2's L13 (0144's)."
    ),
    "hypothesis_expert": (
        "F1.5 design 2 (parallel tempering in the set of keys that keep the 24 known letters; 0139-0146) decided F1.1 L23, "
        "L26 and F1.2 L8, L13, L16 at measured power; F1.4's free-alphabet residue (about 1,900 settings), F1.7's fitting "
        "lags (about 100), F6.1 (about 443,000) and F6.2 3-14 are blocked by its cost. A tempering run either reaches the "
        "basin of the planted reading or not; if most plants are found in the first runs, or in short runs, the decider "
        "can be cut without losing power. Separately and exactly, copies can be climbed one at a time, stopping at the "
        "first that beats the target: the decision 'target above every copy' is unchanged, and under the null the target "
        "is exchangeable with its copies, so the expected number climbed is H_12 = 3.1 instead of 12 (no run needed; "
        "stated here). Test: per plant, found at budget (rounds, r) when the best of its first r runs is strictly above "
        "the best of the first r runs of each of its 6 own copies (null 1/7). Pre-registered: the reference is the full "
        "budget (625 rounds, 10 runs) measured in this run; a cheaper budget qualifies when its power is at least the "
        "reference's on clean and on Sanborn-style plants at both lengths; D1 is reached when the cheapest qualifying "
        "budget times the sequential-copies factor is at least ten times cheaper per setting. Also reported: design 2's "
        "power on 12 fresh Sanborn-style plants at L13, beside 0226's 9 of 12 (the reopened F1.2 L13 cell)."
    ),
    "hypothesis_eli5": (
        "The best tool we have for judging the hardest cases is slow: for each setting it runs ten long searches on K4 "
        "and on a dozen scrambled copies. Here we hide test messages, run the tool, and note after every one of the ten "
        "searches, and with searches a tenth as long, whether the hidden message was already picked out. If it usually "
        "is, the tool can be made much cheaper without missing more, and settings we had to skip for cost can be judged."
    ),
    "prediction": (
        "Power saturates early: at full length 3 runs reach the reference power at L23 and 5 at L13; runs a tenth as long "
        "lose power (about two thirds of the reference at L23, half at L13). With sequential copies, 3 full runs give "
        "about 3.3 x 3.1 = 10 times cheaper per setting at L23: D1 reached at L23, not at L13. Design 2 on fresh "
        "Sanborn-style plants at L13: 9-11 of 12. Zero candidates."
    ),
    "method": (
        "1. L23: 8 clean plants (0120's make_plants rule) and 12 Sanborn-style (0226's class texts, arm 0: 4 xstops, 4 "
        "K1-K3 windows, 4 with three letters changed), each enciphered in the Beaufort form with a random alphabet and key "
        "of 23; 6 own copies each, shuffles that 0120's exact decider fits at 23. "
        "2. L13: 5 clean plants (0144's plant4) and 12 Sanborn-style (arm 1), two random alphabets and a key of 13; witness "
        "from 0123's decider under a 20 s alarm (0226's rule); 6 kept-place copies each, the plant's witness as start. "
        "3. Every text climbed twice with 0140's and 0144's compiled tempering, same replicas, moves and temperatures: 10 "
        "runs of 625 rounds and 10 runs of 62 rounds, each run's best score recorded with its wall time. "
        "4. Power at every (rounds, r), r = 1-10, by class and length; cost per text from the measured times."
    ),
    "walkthrough": (
        "1. Hide a test message under a shuffled alphabet and a key of 23 numbers. "
        "2. Make six scrambled copies of its ciphertext that the same key length still fits. "
        "3. Run the tempering search ten times on each of the seven texts, writing down the best score after each run. "
        "4. After run 1, is the hidden message's best above all six copies' bests? After run 2? ... After run 10? "
        "5. Repeat with runs a tenth as long. "
        "6. Over many hidden messages, the share found after r runs is the tool's power at that budget."
    ),
    "expected_minutes": 100,
}

import ctypes
import importlib.util
import random
import signal
import time
from pathlib import Path

N = 97
ROOT = Path(__file__).resolve().parent
ROUNDS = (625, 62)
RUNS = 10
N_OWN = 6
CLEAN = {"23": 8, "13": 5}
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


class _Slow(Exception):
    pass


def _witness(m44, m23, pc, known, rng, secs=20):
    """0144's witness under an alarm (0226's rule): 0123's search can run for minutes on some keys."""
    def _raise(*_):
        raise _Slow()
    old = signal.signal(signal.SIGALRM, _raise)
    signal.alarm(secs)
    try:
        return m44.witness4(pc, known, 13, rng, m23)
    except _Slow:
        return None
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)


def runs_scores(arm, text, seed, rounds, y0):
    """Each tempering run's best score, with its wall time: 0140's climb (arm 23) or 0144's (arm 13), unchanged
    but for the number of rounds."""
    from kryptos.facts import KNOWN
    m = _MODS["0140"] if arm == "23" else _MODS["0144"]
    L_ = m.lib() if arm == "23" else m.lib4()
    L = 23 if arm == "23" else 13
    kp = sorted(KNOWN)
    CT = (ctypes.c_int * N)(*[ord(ch) - 65 for ch in text])
    KP = (ctypes.c_int * 24)(*[q - 1 for q in kp])
    KL = (ctypes.c_int * 24)(*[ord(KNOWN[q]) - 65 for q in kp])
    L_.setup(m._LIB["tab"], CT, N, L, KP, KL, 24)
    if arm == "13":
        L_.set_start((ctypes.c_int * 52)(*y0))
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
    """-> jobs and the plants' metadata; plants and copies made exactly as 0139/0143 (clean) and 0226 (classes)."""
    known = ctx.KNOWN
    m40, m44, m26 = _load("0140"), _load("0144"), _load("0226")
    m20, m23 = m40.load_0120(), m44.load_0123()
    m40.lib(); m44.lib(); m44.lib4()
    texts, meta = [], {}
    rng = random.Random(2280)
    plants23 = [("clean", pt, pc) for pc, pt in m20.make_plants(known, 23, rng, CLEAN["23"])]
    for cls, pt in m26.class_texts(rng, 0):
        alpha = list(ctx.STANDARD_ALPHABET); rng.shuffle(alpha); alpha = "".join(alpha)
        k = [rng.randrange(26) for _ in range(23)]
        plants23.append((cls, pt, m20.beaufort_encrypt(pt, alpha, k)))
    for i, (cls, pt, pc) in enumerate(plants23):
        assert m20.decide(m20.equations(pc, known, 23), "B", rng)[0] == "fit"
        meta[("23", i)] = {"cls": cls, "pt": pt}
        texts.append(("23", "plant", i, pc, rng.randrange(10 ** 9), None))
        g = 0
        while g < N_OWN:
            sh = list(pc); rng.shuffle(sh); sh = "".join(sh)
            if m20.decide(m20.equations(sh, known, 23), "B", rng)[0] == "fit":
                texts.append(("23", "own", i * 100 + g, sh, rng.randrange(10 ** 9), None)); g += 1
    rng = random.Random(2281)
    kidx = set(q - 1 for q in known)
    free = [j for j in range(N) if j not in kidx]
    plants13 = []
    for _ in range(CLEAN["13"]):
        while True:
            pc, pt = m44.plant4(13, rng, known)
            y0 = _witness(m44, m23, pc, known, rng)
            if y0 is not None:
                break
        plants13.append(("clean", pt, pc, y0))
    for cls, pt in m26.class_texts(rng, 1):
        y0 = None
        while y0 is None:
            P = list(range(26)); C = list(range(26)); rng.shuffle(P); rng.shuffle(C)
            Ci = {v: j for j, v in enumerate(C)}
            k = [rng.randrange(26) for _ in range(13)]
            pc = "".join(chr(65 + Ci[(P[ord(ch) - 65] + k[j % 13]) % 26]) for j, ch in enumerate(pt))
            for _ in range(5):
                y0 = _witness(m44, m23, pc, known, rng)
                if y0 is not None:
                    break
        plants13.append((cls, pt, pc, y0))
    for i, (cls, pt, pc, y0) in enumerate(plants13):
        meta[("13", i)] = {"cls": cls, "pt": pt}
        texts.append(("13", "plant", i, pc, rng.randrange(10 ** 9), y0))
        for g in range(N_OWN):
            letters = [pc[j] for j in free]; rng.shuffle(letters)
            cp = list(pc)
            for j, ch in zip(free, letters):
                cp[j] = ch
            texts.append(("13", "own", i * 100 + g, "".join(cp), rng.randrange(10 ** 9), y0))
    jobs = [(a, k, i, t, s, rounds, y0) for rounds in ROUNDS for (a, k, i, t, s, y0) in texts]
    jobs.sort(key=lambda j: (j[0] != "13", j[5] != 625))      # the long L13 climbs first, so the pool ends evenly
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
    for arm in ("23", "13"):
        for rounds in ROUNDS:
            for r in range(1, RUNS + 1):
                c = power(res, meta, arm, rounds, r, "clean")
                m = power(res, meta, arm, rounds, r, "messy")
                table[f"{arm}/{rounds}/{r}"] = {"clean": c, "messy": m, "cost": round(rounds * r / (625 * RUNS), 4)}
    ref = {arm: table[f"{arm}/625/{RUNS}"] for arm in ("23", "13")}

    def ok(arm, key):
        t = table[key]
        return all(t[c][0] * ref[arm][c][1] >= ref[arm][c][0] * t[c][1] for c in ("clean", "messy"))
    budgets = sorted({(rounds, r) for rounds in ROUNDS for r in range(1, RUNS + 1)}, key=lambda b: b[0] * b[1])
    qualifying = [b for b in budgets if all(ok(arm, f"{arm}/{b[0]}/{b[1]}") for arm in ("23", "13"))]
    cheapest = qualifying[0] if qualifying else None
    seq = sum(1 / (j + 1) for j in range(12))
    full_factor = (1 + 12) / (1 + seq)
    times = {}
    for (arm, kind, idx, rounds), s in res.items():
        times.setdefault(f"{arm}/{rounds}", []).append(sum(x[1] for x in s))
    by_class = {}
    for arm in ("23", "13"):
        for cls in ("clean", "xstops", "k123", "sub3"):
            ids = [i for (a, i), v in meta.items() if a == arm and v["cls"] == cls]
            f = 0
            for i in ids:
                own = [res[(arm, "own", i * 100 + g, 625)] for g in range(N_OWN)]
                f += max(x[0] for x in res[(arm, "plant", i, 625)]) > max(max(x[0] for x in o) for o in own)
            by_class[f"{arm}/{cls}"] = [f, len(ids)]
    factor = None if cheapest is None else round(full_factor * (625 * RUNS) / (cheapest[0] * cheapest[1]), 1)
    bounds = {
        "item": "D1", "decider": "F1.5 design 2: 0140's (L23, one alphabet, Beaufort) and 0144's (L13, two alphabets) compiled tempering",
        "plants": {"23": {"clean": CLEAN["23"], "sanborn_style": 12}, "13": {"clean": CLEAN["13"], "sanborn_style": 12}},
        "own_copies": N_OWN, "null_per_plant": "1/7", "rounds": list(ROUNDS), "runs": RUNS,
        "reference": {arm: ref[arm] for arm in ref}, "power_table": table, "power_by_class_full_budget": by_class,
        "qualifying_budgets": [list(b) for b in qualifying], "cheapest_qualifying": cheapest,
        "sequential_copies_factor": round(full_factor, 2),
        "sequential_copies_note": "exact: stop climbing copies at the first that beats the target; same decision; expected copies under the null H_12 = 3.10",
        "cost_factor_per_setting": factor, "d1_reached": bool(factor and factor >= 10),
        "seconds_per_text": {k: round(sum(v) / len(v), 1) for k, v in times.items()},
        "f12_l13_sanborn_style_full_budget": table[f"13/625/{RUNS}"]["messy"], "f12_l13_with_0226": "0226: 9 of 12",
        "texts": len(jobs) // 2, "climbs": len(jobs), "compute_seconds": round(time.time() - t_start), "exhaustive": False,
        "expected_total_time": "about 47,700 core-seconds (140 texts at about 121 s for L23, 119 at about 259 s for L13, both passes), 100 min on 8 cores",
    }
    notes = (f"reference power L23 clean {ref['23']['clean']}, messy {ref['23']['messy']}; L13 clean {ref['13']['clean']}, "
             f"messy {ref['13']['messy']}; cheapest qualifying budget {cheapest}; per-setting factor with sequential copies {factor}")
    controls = [max(x[0] for x in s) for (a, k, i, rd), s in res.items() if k == "own" and rd == 625]
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
