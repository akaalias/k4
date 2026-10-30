"""Experiment (F1.4 two-alphabet residue, draft). See program.md for the contract."""

EXPERIMENT = {
    "slug": "f1.4-two-alphabet-residue-decided-by-four-runs-with-stand-ins",
    "title": "F1.4: every hand key schedule K4 fits on two free alphabets, each decided by D1b's four-run decider against kept-place copies one at a time, with 20 shuffled stand-ins through the same procedure",
    "family": "1-keyed-periodic",
    "parent": "0253-f1.4-one-alphabet-residue-decided-by-the-one-run-decider",
    "changed": (
        "F1.4, the two-alphabet residue, which waited for D1b. 0253-0255 decided the one-alphabet residue (K4 inside 40 "
        "stand-ins, p 0.51). D1b (0257) qualified four runs of 0144's two-alphabet tempering (66 of 96 plants against ten "
        "runs' 71). Here 0144's climb is generalised to any slot map (the change 0252 made to 0140's), every 0128 schedule "
        "that fits K4 on two free alphabets (4,706 slot maps; the 1,346 in the record were distinct partitions of the 24 known places) is decided with it against kept-place copies climbed one at a time (stop at the "
        "first at or above K4, at most 12), and 20 stand-ins (K4 with its 73 unknown places shuffled, so the same settings "
        "fit) go through the same procedure on 60 settings each: the verdict is K4's rate against theirs (0254's lesson)."
    ),
    "hypothesis_expert": (
        "F1.4: a keyed table with a hand key schedule (C20(d): tableau rows as keys; 0126-0128's schedules: a key letter "
        "skipped every m letters, stutter, back and forth, triangle, square, a restart per carved line), on two free "
        "alphabets (Quagmire IV with unknown orders: Sanborn's 'slightly different' tableau on both sides, C27(c)). The "
        "added and Beaufort forms are one on two free alphabets (reverse the cipher alphabet). 0128 found the fitting "
        "settings at the copies' rate, so the 24 known letters cannot decide them and English must. Decider: D1b's four "
        "runs of 0144's tempering (16 x 625 x 1000) from the exact witness (0128's two-alphabet decider), patched only to "
        "read the key slot of each carved letter from the schedule; self-checked against 0144's library on periodic slot "
        "maps. Copies keep the carved letters at the 24 known places (same equations, same freedom; 0143, 0257). "
        "Clue entries: C20(d), C27(c), C5(a)."
    ),
    "hypothesis_eli5": (
        "Sanborn may have stepped through his key word with a twist (skipping a letter now and then, going back and "
        "forth) and used two scrambled alphabets of his own, one for the message and one for the cipher. About five thousand "
        "such twists agree with the 24 known letters, so those letters cannot tell them apart. For each one we search for "
        "the most English-looking reading of K4 and do the same on scrambled copies; to know what 'K4 wins often' means, "
        "twenty scrambled stand-ins for K4 go through the very same test."
    ),
    "prediction": (
        "K4's rate of settings above all 12 copies inside the 20 stand-ins' spread (p above 0.05); plants (24, on settings "
        "K4 fits) found above all 12 own copies about 14 of 24; no reading English. Zero candidates."
    ),
    "method": (
        "1. Settings: 0252's f14_settings() (every 0128 schedule at every slot count 2-31, deduplicated); each decided on K4 "
        "by 0128's exact two-alphabet decider; the fitting ones are the cell (undecided ones counted). "
        "2. Per setting (one job, own seed): K4 climbed with four runs of the generalised tempering from the exact witness; "
        "then kept-place copies (the 73 unknown places shuffled) climbed the same way one at a time, stopping at the first "
        "at or above K4, at most 12. "
        "3. Stand-ins: 20 kept-place shuffles of K4 (seed 2630), each decided the same way on 60 settings drawn from the "
        "cell. "
        "4. Plants: 12 clean and 12 Sanborn-style messages on settings drawn from the cell, two random alphabets and key; "
        "found if above all 12 own copies. "
        "5. Verdict: K4's share of settings above all 12 copies, ranked among the stand-ins' shares."
    ),
    "walkthrough": (
        "1. Pick a schedule, say: a key of 11 letters, skip one key letter after every 7 carved letters. "
        "2. Write the key slot under each of the 97 carved letters. "
        "3. With two unknown alphabets, two known letters in one slot must satisfy C(c1) - P(p1) = C(c2) - P(p2); check "
        "that some pair of alphabets satisfies all of them. "
        "4. Search alphabet pairs and keys for the most English-looking reading of K4, four times. "
        "5. Shuffle the 73 letters at unknown places (the known places keep their carved letters, so step 3 still holds) "
        "and search the copy the same way; stop when a copy reads as well as K4, at most 12 copies. "
        "6. Do steps 4-5 for every schedule, and for 20 shuffled stand-ins of K4; compare how often K4 wins all 12 with "
        "how often the stand-ins do."
    ),
    "expected_minutes": 6000,
}

import ctypes
import importlib.util
import os
import random
import sys
import time
import types
from pathlib import Path

N = 97
ROOT = Path(__file__).resolve().parent
RUNS = 4                 # D1b (0257): four runs qualify for two free alphabets
BASE = 12
PLANTS = 24
STAND_INS, PER_STAND_IN = 20, 60
SEED = 2630
_MODS = {}


def _load(e):
    if e not in _MODS:
        path = next((ROOT / "experiments").glob(f"{e}-*")) / "attack.py"
        spec = importlib.util.spec_from_file_location(f"frozen{e}", path)
        m = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = m
        spec.loader.exec_module(m)
        if hasattr(m, "ROOT"):
            m.ROOT = ROOT
        _MODS[e] = m
    return _MODS[e]


# ---- 0144's two-alphabet tempering, patched to read a slot per carved letter ----

PATCHES = [
    ("static int NCH, CH[64][4],", "static int SLOT[128];\nstatic int NCH, CH[64][4],", 1),
    ("pt[i] = pinv[((y[26 + C[i]] - k[i % L]) % 26 + 26) % 26];", "pt[i] = pinv[((y[26 + C[i]] - k[SLOT[i]]) % 26 + 26) % 26];", 1),
    ("int s = kpos[j] % l, c = ct[kpos[j]], p = klet[j];", "int s = SLOT[kpos[j]], c = ct[kpos[j]], p = klet[j];", 1),
]
EXTRA = "\nvoid set_slot(const int *s, int n) { for (int i = 0; i < n; i++) SLOT[i] = s[i]; }\n"


def glib():
    if "g" not in _MODS:
        import subprocess
        import tempfile
        m = _load("0144")
        m.lib()                                  # 0144's quadgram table
        src = m.C_SOURCE4
        for old, new, count in PATCHES:
            assert src.count(old) == count, (old, src.count(old))
            src = src.replace(old, new)
        src += EXTRA
        d = tempfile.mkdtemp(prefix="k4_f14two_")
        open(os.path.join(d, "g.c"), "w").write(src)
        subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", os.path.join(d, "g.so"), os.path.join(d, "g.c")],
                       check=True, capture_output=True)
        L_ = ctypes.CDLL(os.path.join(d, "g.so"))
        L_.ptemper.restype = ctypes.c_double
        L_.ptemper.argtypes = m.lib4().ptemper.argtypes
        _MODS["g"] = L_
    return _MODS["g"]


def _arrays(text):
    from kryptos.facts import KNOWN
    kp = sorted(KNOWN)
    return ((ctypes.c_int * N)(*[ord(ch) - 65 for ch in text]), (ctypes.c_int * 24)(*[q - 1 for q in kp]),
            (ctypes.c_int * 24)(*[ord(KNOWN[q]) - 65 for q in kp]))


def climb(text, slot, n, seed, y0, runs=RUNS, rounds=None):
    """Best of `runs` tempering runs on slot map `slot` (n slots), started from witness y0: (score, reading)."""
    m = _MODS["0144"]
    L_ = glib()
    CT, KP, KL = _arrays(text)
    L_.set_slot((ctypes.c_int * N)(*slot), N)
    L_.setup(m._LIB["tab"], CT, N, n, KP, KL, 24)
    L_.set_start((ctypes.c_int * 52)(*y0))
    best = (-99.0, "?" * N)
    for r in range(runs):
        bp = (ctypes.c_int * 128)(); by = (ctypes.c_int * 52)(); bk = (ctypes.c_int * 64)()
        sc = L_.ptemper(seed * 100003 + r, 1, m.PT_R, rounds or m.PT_ROUNDS, m.PT_MOVES, m.PT_T0, m.T1, bp, by, bk)
        if sc > best[0]:
            best = (round(sc, 5), "".join(chr(65 + bp[i]) if 0 <= bp[i] < 26 else "?" for i in range(N)))
    return best


def self_check(ctx, y0):
    """On periodic slot maps the patched library gives 0144's own scores on the same seeds."""
    m = _MODS["0144"]
    out = []
    for L in (13, 16):
        CT, KP, KL = _arrays(ctx.K4)
        L0 = m.lib4()
        L0.setup(m._LIB["tab"], CT, N, L, KP, KL, 24)
        L0.set_start((ctypes.c_int * 52)(*y0[L]))
        bp = (ctypes.c_int * 128)(); by = (ctypes.c_int * 52)(); bk = (ctypes.c_int * 64)()
        a = round(L0.ptemper(7 * 100003, 1, m.PT_R, 40, m.PT_MOVES, m.PT_T0, m.T1, bp, by, bk), 5)
        b = climb(ctx.K4, [i % L for i in range(N)], L, 7, y0[L], runs=1, rounds=40)[0]
        out.append((L, a, b))
        assert a == b, (L, a, b)
    return out


# ---- the exact two-alphabet decider on a slot map ----

def eqs_of(text, slot):
    from kryptos.facts import KNOWN
    return [(slot[q - 1], ord(KNOWN[q]) - 65, ord(text[q - 1]) - 65) for q in sorted(KNOWN)]


def witness(text, slot, rng):
    """0128's exact two-alphabet decision; a full 52-place start (plain then cipher) if it fits, else the status."""
    st, w = _load("0128").decide(eqs_of(text, slot), "V", rng, two=True)
    if st != "fit":
        return st
    x, _k = w
    y = [-1] * 52
    for (f, le), v in x.items():
        y[(0 if f == "P" else 26) + le] = v
    for g in (0, 26):
        free = [v for v in range(26) if v not in y[g:g + 26]]
        rng.shuffle(free)
        for i in range(g, g + 26):
            if y[i] < 0:
                y[i] = free.pop()
    return y


def kept_place(text, rng):
    from kryptos.facts import KNOWN
    kidx = {q - 1 for q in KNOWN}
    free = [j for j in range(N) if j not in kidx]
    letters = [text[j] for j in free]
    rng.shuffle(letters)
    out = list(text)
    for j, ch in zip(free, letters):
        out[j] = ch
    return "".join(out)


def encipher(pt, slot, P, C, key):
    """C(c) = P(p) + key[slot]; P, C: letter -> place."""
    Ci = {v: i for i, v in enumerate(C)}
    return "".join(chr(65 + Ci[(P[ord(ch) - 65] + key[slot[i]]) % 26]) for i, ch in enumerate(pt))


# ---- workers ----

def _fit_job(args):
    lo, items, k4 = args
    rng = random.Random(lo)
    out = []
    for name, slot, n in items:
        w = witness(k4, slot, rng)
        out.append((name, slot, n, w if isinstance(w, str) else "fit", None if isinstance(w, str) else w))
    return out


def decide(text, slot, n, seed, y0):
    """K4 (or a stand-in, or a plant) climbed once (four runs), then kept-place copies one at a time until one reaches it."""
    rng = random.Random(seed)
    t0 = time.time()
    score, reading = climb(text, slot, n, rng.randrange(10 ** 9), y0)
    copies = []
    while len(copies) < BASE:
        cs = climb(kept_place(text, rng), slot, n, rng.randrange(10 ** 9), y0)[0]
        copies.append(cs)
        if cs >= score:
            break
    above = len(copies) if all(c < score for c in copies) else len(copies) - 1
    return {"score": score, "reading": reading, "copies": copies, "above": above, "secs": round(time.time() - t0, 1)}


def _job(args):
    key, text, slot, n, seed, y0 = args
    return key, decide(text, slot, n, seed, y0)


def run(ctx):
    import multiprocessing as mp
    t_start = time.time()
    W = int(os.environ.get("K4_WORKERS", 8))
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    m44, m52 = _load("0144"), _load("0252")
    _load("0128"); m44.lib(); glib()
    m20, m26 = _load("0140").load_0120(), _load("0226")
    k4 = ctx.K4
    rng = random.Random(SEED)

    # 1. settings K4 fits on two free alphabets (exact), deduplicated by slot map
    items, seen = [], set()
    for g, lst in m52.f14_settings().items():
        for name, slot, n in lst:
            if slot not in seen:
                seen.add(slot); items.append((name, slot, n))
    chunks = [(i, items[i::W * 4], k4) for i in range(W * 4)]
    with mp.get_context("fork").Pool(W) as pool:
        decided = [x for lst in pool.imap_unordered(_fit_job, chunks) for x in lst]
    decided.sort(key=lambda x: x[0])
    status = {}
    for *_, s, _w in decided:
        status[s] = status.get(s, 0) + 1
    fit = [(name, slot, n) for name, slot, n, s, _w in decided if s == "fit"]
    y = {i: w for i, w in enumerate(w for *_, s, w in decided if s == "fit")}
    per = {13: None, 16: None}
    for L in per:
        while not isinstance(per[L], list):
            per[L] = witness(k4, [i % L for i in range(N)], rng)
    check = self_check(ctx, per)

    # 2. plants on settings drawn from the cell
    texts = [("clean", pt) for _, pt in m20.make_plants(ctx.KNOWN, 10, rng, PLANTS // 2)]
    for a in (0, 1, 2):
        texts += m26.class_texts(rng, a)[:PLANTS // 6]
    plants, pmeta = [], {}
    for idx, (cls, pt) in enumerate(texts):
        while True:
            fi = rng.randrange(len(fit))
            name, slot, n = fit[fi]
            P = list(range(26)); C = list(range(26)); rng.shuffle(P); rng.shuffle(C)
            key = [rng.randrange(26) for _ in range(n)]
            pc = encipher(pt, slot, P, C, key)
            y0 = witness(pc, slot, rng)
            if isinstance(y0, list):
                break
        pmeta[idx] = {"cls": cls, "setting": name, "pt": pt}
        plants.append((("plant", idx), pc, slot, n, 900000 + idx, y0))

    # 3. stand-ins: kept-place shuffles of K4 (the same 24 checks, so the same settings fit)
    srng = random.Random(SEED + 1)
    stand = []
    for s in range(STAND_INS):
        t = kept_place(k4, srng)
        for fi in srng.sample(range(len(fit)), min(PER_STAND_IN, len(fit))):
            name, slot, n = fit[fi]
            stand.append(((f"s{s}", fi), t, slot, n, 500000 + 1000 * s + fi, y[fi]))
    work = plants + [(("k4", i), k4, slot, n, 1000 + i, y[i]) for i, (name, slot, n) in enumerate(fit)] + stand
    random.Random(SEED + 2).shuffle(work)        # interleave so no group is starved

    res = {}
    saved = getattr(ctx, "saved", {}) or {}
    for key, *_ in work:                          # units an earlier run of this attack.py finished (#105)
        if f"{key[0]}:{key[1]}" in saved:
            res[key] = saved[f"{key[0]}:{key[1]}"]
    todo = [w for w in work if w[0] not in res]
    ctx.progress(len(res), len(work), "settings")
    with mp.get_context("fork").Pool(W) as pool:
        for key, out in pool.imap_unordered(_job, todo, chunksize=1):
            res[key] = out
            ctx.save(f"{key[0]}:{key[1]}", out)
            ctx.progress(len(res), len(work), "settings")

    # 4. verdicts
    found = {}
    for idx, v in pmeta.items():
        r = res[("plant", idx)]
        v.update(found=r["above"] >= BASE, above=r["above"], score=r["score"],
                 letters_right=sum(a == b for a, b in zip(r["reading"], v.pop("pt"))))
        found.setdefault("clean" if v["cls"] == "clean" else "sanborn", []).append(v["found"])
    n = len(fit)
    k12 = [i for i in range(n) if res[("k4", i)]["above"] >= BASE]
    k4_rate = len(k12) / n
    srates = {}
    for s in range(STAND_INS):
        rs = [r for (a, b), r in res.items() if a == f"s{s}"]
        srates[f"s{s}"] = round(sum(r["above"] >= BASE for r in rs) / len(rs), 4)
    at_or_above = sum(1 for v in srates.values() if v >= k4_rate)
    p = (at_or_above + 1) / (STAND_INS + 1)
    top = sorted(range(n), key=lambda i: (-res[("k4", i)]["above"], -res[("k4", i)]["score"]))[:20]
    top_list = [{"setting": fit[i][0], "slots": fit[i][2], "above": res[("k4", i)]["above"], "score": res[("k4", i)]["score"],
                 "copies_max": max(res[("k4", i)]["copies"]), "reading": res[("k4", i)]["reading"],
                 "known_in_place": sum(res[("k4", i)]["reading"][q - 1] == c for q, c in ctx.KNOWN.items())} for i in top]
    secs = [r["secs"] for r in res.values()]
    climbs = sum(1 + len(r["copies"]) for r in res.values())
    bounds = {
        "item": "F1.4 (two free alphabets residue, after D1b)",
        "decider": f"D1b's four-run decider: {RUNS} runs of 0144's tempering (16 x 625 x 1000) generalised to any slot map, from 0128's exact two-alphabet witness; copies keep the carved letters at the 24 known places and shuffle the other 73, climbed one at a time, stop at the first at or above, at most {BASE}",
        "self_check_against_0144": check,
        "settings_listed": len(items), "decider_status": status, "k4_fitting_settings": n,
        "k4_above_all_12": len(k12), "k4_rate": round(k4_rate, 4), "chance_if_independent": round(1 / (BASE + 1), 4),
        "stand_ins": {"n": STAND_INS, "settings_each": PER_STAND_IN, "rates": srates, "at_or_above_k4": at_or_above, "p": round(p, 4),
                      "how": "K4 with its 73 unknown places shuffled (seed 2631): the same 24 checks, so every setting fits; each decided as K4 on 60 settings drawn from the cell"},
        "top_settings": top_list,
        "plants": {"clean_found": [sum(found.get("clean", [])), len(found.get("clean", []))],
                   "sanborn_found": [sum(found.get("sanborn", [])), len(found.get("sanborn", []))],
                   "null_per_plant": "1/13", "each": pmeta},
        "climbs": climbs, "runs_per_climb": RUNS, "core_seconds": round(sum(secs)), "compute_seconds": round(time.time() - t_start),
        "exhaustive": True, "exhaustive_over": "every setting of 0128's schedules (slot counts 2-31) K4 fits on two free alphabets; each decided at D1b's four-run power",
        "resumed_units": len(work) - len(todo),
        "cost_estimate": "4,706 settings (desk count 2026-10-30; the 1,346 in the record counted distinct partitions of the 24 known places, 0127/0128, not slot maps over all 97 places, which is what a climb reads) x about 16.4 runs (4 for K4 plus about 3.1 copies of 4, H_12) plus 20 x 60 stand-in settings and 24 plants: about 98,000 tempering runs at 12-15 core-s (desk timing on the loaded laptop, 12.2 s): about 330-410 core-hours; about $5.6 on Modal, above the credit left, so on the laptop: several days",
    }
    notes = (f"F1.4 two-alphabet residue: {n} settings; K4 above all 12 kept-place copies in {len(k12)} ({100 * k4_rate:.1f}%); "
             f"20 stand-ins {100 * min(srates.values()):.1f}-{100 * max(srates.values()):.1f}%, {at_or_above} at or above K4 (p {p:.2f}); "
             f"plants clean {bounds['plants']['clean_found']}, Sanborn-style {bounds['plants']['sanborn_found']}.")
    controls = [c for i in range(n) for c in res[("k4", i)]["copies"]][:2000]
    return {"candidates": [], "bounds": bounds, "notes": notes, "controls": controls}


def encrypt(plaintext, key):
    """No candidate is submitted. key = {'slot': [...], 'P': [...], 'C': [...], 'key': [...]}."""
    return encipher(plaintext, key["slot"], key["P"], key["C"], key["key"])


def worked_example(ctx, key):
    return "\n".join([
        "F1.4: two free alphabets under a hand key schedule, decided setting by setting.", "",
        "  setting      skip one key letter every 7 letters, 11 key letters",
        "  slot map     place 1 2 3 4 5 6 7 8 9 ...",
        "  key letter         1 2 3 4 5 6 8 9 10 ... (letter 7 skipped)",
        "  cipher       C(carved) = P(plain) + key[slot], P and C two unknown alphabets", "",
        "  K4 gets four tempering searches under that slot map; then copies that keep the carved letters at the 24 known",
        "  places (so they fit the same checks) get the same, one at a time, until a copy reads as well as K4 (at most 12).",
        "  20 shuffled stand-ins for K4 go through the same test: K4's rate of wins must stand out from theirs."])
