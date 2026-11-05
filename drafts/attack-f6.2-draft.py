"""Experiment (F6.2 lengths 3-10, draft). See program.md for the contract."""

EXPERIMENT = {
    "slug": "f6.2-two-free-alphabets-around-every-move-lengths-3-10-decided-by-four-runs",
    "title": "F6.2: two free alphabets after or before every type-1 move, key lengths 3-10, every setting K4 fits decided by D1b's four-run decider against kept-place copies, with 20 shuffled stand-ins through the same procedure",
    "family": "6-move-then-table",
    "parent": "0267-f1.4-two-alphabet-residue-decided-by-four-runs-with-stand-ins",
    "changed": (
        "D2's last cell (#77): F6.2 waited for a two-alphabet decider (D1b, 0257: four runs qualify). 0267's two-alphabet "
        "climb (0144's tempering on any slot map) is patched once more to read the message in moved order, as 0252 did for "
        "one alphabet, and every (move, order, length 3-10) that fits K4 exactly on two free alphabets (0133: 42,644) is "
        "decided against kept-place copies climbed one at a time (stop at the first at or above K4, at most 12). Twenty full "
        "shuffles of K4 go through the same procedure on 100 of their own fitting settings."
    ),
    "hypothesis_expert": (
        "F6.2 (C1(a): 'a matrix code... then went back to this table'; C27(c): a 'slightly different' tableau on both sides): "
        "a type-1 move of 0129's library (27,852) before or after a Quagmire IV with both alphabets unknown and a periodic "
        "key of length 3-10 (the added and Beaufort forms are one on two free alphabets). 0131-0133 found K4 fits at the "
        "copies' rate from length 3 (move then table) and 4 (table then move): the known letters cannot decide these settings "
        "and English must. Decider: D1b's four runs of 0144's tempering from the exact witness (0128's two-alphabet decider), "
        "patched only to read each carved letter's key slot and message place from the setting; self-checked against 0144 "
        "on the identity move. Lengths 11-14 (about 100,000 per-slot survivors, about $160 on AWS) and 15-26 (0136's bound) "
        "are not run here. Clue entries C1(a), C27(c), C11."
    ),
    "hypothesis_eli5": (
        "Sanborn said he wrote the message into a grid and read it out another way, then used the cipher table. With two "
        "scrambled alphabets of his own in the table and a short key word, about 43,000 such recipes agree with the 24 known "
        "letters. For each one we search for the most English-looking reading of K4 and of scrambled copies; twenty scrambled "
        "stand-ins for K4 go through the very same test so we know what 'K4 wins often' would mean."
    ),
    "prediction": (
        "K4's rate of settings above all 12 copies inside the 20 stand-ins' spread (p above 0.05); plants found about half "
        "(0267: 12 of 24; 0270: 11 of 24); no reading English. Zero candidates."
    ),
    "method": (
        "1. Settings: 0129's 27,852 moves x order (A move then table, B table then move) x key length 3-10; each decided "
        "exactly on K4 by 0128's two-alphabet decider through the move (the 24 known places' carved places and slots); the "
        "fitting ones are K4's cell, with their witnesses. Checked against 0133's counts per order and length. "
        "2. Per setting (one job, own seed): four runs of the patched climb on K4 from the witness, then kept-place copies "
        "(the carved letters at the 24 landing places kept, the other 73 shuffled) climbed the same way one at a time until "
        "one reaches K4, at most 12. "
        "3. Stand-ins: 20 full shuffles of K4 (seed 2720), each with its own fitting settings found the same way, 100 drawn "
        "and decided alike. "
        "4. Plants: 12 clean and 12 Sanborn-style messages on settings K4 fits, two random alphabets and a random key; found "
        "if above all 12 own copies. "
        "5. Verdict: K4's share of settings above all 12 copies, ranked among the stand-ins' shares."
    ),
    "walkthrough": (
        "1. Pick a recipe: write the message in rows of 9, read the columns in a key word's order, then encipher on a table "
        "with two unknown alphabets and a 7-letter key. "
        "2. Follow each of the 24 known letters to its carved place and key slot. "
        "3. Check that some pair of alphabets makes every two known letters in one slot agree. "
        "4. Search alphabet pairs and keys for the most English-looking reading of K4, reading the message in its moved order. "
        "5. Shuffle the 73 carved letters that no known letter lands on and search the copy the same way; stop when a copy "
        "reads as well as K4, at most 12 copies. "
        "6. Do steps 4-5 for every recipe K4 fits and for twenty scrambled stand-ins; compare how often each wins all 12."
    ),
    "expected_minutes": 7000,
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
LENGTHS = range(3, 11)
RUNS = 4
BASE = 12
PLANTS = 24
STAND_INS, PER_STAND_IN = 20, 100
SEED = 2720
BLOCK = 200                 # routes per scan job
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


# ---- 0144's two-alphabet tempering, patched for a slot and a message place per carved letter ----
PATCHES = [
    ("static int NCH, CH[64][4],", "static int SLOT[128], MPOS[128];\nstatic int NCH, CH[64][4],", 1),
    ("pt[i] = pinv[((y[26 + C[i]] - k[i % L]) % 26 + 26) % 26];", "pt[MPOS[i]] = pinv[((y[26 + C[i]] - k[SLOT[i]]) % 26 + 26) % 26];", 1),
    ("int s = kpos[j] % l, c = ct[kpos[j]], p = klet[j];", "int s = SLOT[kpos[j]], c = ct[kpos[j]], p = klet[j];", 1),
]
EXTRA = "\nvoid set_geom(const int *s, const int *m, int n) { for (int i = 0; i < n; i++) { SLOT[i] = s[i]; MPOS[i] = m[i]; } }\n"


def glib():
    if "g" not in _MODS:
        import subprocess
        import tempfile
        m = _load("0144")
        m.lib()
        src = m.C_SOURCE4
        for old, new, count in PATCHES:
            assert src.count(old) == count, (old, src.count(old))
            src = src.replace(old, new)
        src += EXTRA
        d = tempfile.mkdtemp(prefix="k4_f62_")
        open(os.path.join(d, "g.c"), "w").write(src)
        subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", os.path.join(d, "g.so"), os.path.join(d, "g.c")],
                       check=True, capture_output=True)
        L_ = ctypes.CDLL(os.path.join(d, "g.so"))
        L_.ptemper.restype = ctypes.c_double
        L_.ptemper.argtypes = m.lib4().ptemper.argtypes
        _MODS["g"] = L_
    return _MODS["g"]


def routes():
    if "lib" not in _MODS:
        from kryptos.facts import load_vocabulary
        _MODS["lib"] = _load("0129").route_library(load_vocabulary())
    return _MODS["lib"]


def geom(r, o, L):
    """slot[j], mpos[j] per carved place; land[e] = carved place of the e-th known place (sorted)."""
    from kryptos.facts import KNOWN
    where = tuple(range(N)) if r == -1 else routes()[r][1]
    slot, mpos = [0] * N, [0] * N
    for i in range(N):
        j = where[i]
        mpos[j] = i
        slot[j] = j % L if o == "A" else i % L
    land = [where[q - 1] for q in sorted(KNOWN)]
    return slot, mpos, land


def climb(text, g, n, seed, y0, runs=RUNS, rounds=None):
    from kryptos.facts import KNOWN
    m = _MODS["0144"]
    L_ = glib()
    slot, mpos, land = g
    kp = sorted(KNOWN)
    CT = (ctypes.c_int * N)(*[ord(ch) - 65 for ch in text])
    KP = (ctypes.c_int * 24)(*land)
    KL = (ctypes.c_int * 24)(*[ord(KNOWN[q]) - 65 for q in kp])
    L_.set_geom((ctypes.c_int * N)(*slot), (ctypes.c_int * N)(*mpos), N)
    L_.setup(m._LIB["tab"], CT, N, n, KP, KL, 24)
    L_.set_start((ctypes.c_int * 52)(*y0))
    best = (-99.0, "?" * N)
    for r in range(runs):
        bp = (ctypes.c_int * 128)(); by = (ctypes.c_int * 52)(); bk = (ctypes.c_int * 64)()
        sc = L_.ptemper(seed * 100003 + r, 1, m.PT_R, rounds or m.PT_ROUNDS, m.PT_MOVES, m.PT_T0, m.T1, bp, by, bk)
        if sc > best[0]:
            best = (round(sc, 5), "".join(chr(65 + bp[i]) if 0 <= bp[i] < 26 else "?" for i in range(N)))
    return best


def self_check(ctx):
    """Identity move, periodic slots: the patched library gives 0144's own scores on the same seeds."""
    m = _MODS["0144"]
    out = []
    rng = random.Random(7)
    for L in (13, 16):
        g = geom(-1, "A", L)
        y0 = None
        while not isinstance(y0, list):
            y0 = witness(ctx.K4, g, rng)
        CT = (ctypes.c_int * N)(*[ord(ch) - 65 for ch in ctx.K4])
        from kryptos.facts import KNOWN
        kp = sorted(KNOWN)
        L0 = m.lib4()
        L0.setup(m._LIB["tab"], CT, N, L, (ctypes.c_int * 24)(*[q - 1 for q in kp]), (ctypes.c_int * 24)(*[ord(KNOWN[q]) - 65 for q in kp]), 24)
        L0.set_start((ctypes.c_int * 52)(*y0))
        bp = (ctypes.c_int * 128)(); by = (ctypes.c_int * 52)(); bk = (ctypes.c_int * 64)()
        a = round(L0.ptemper(7 * 100003, 1, m.PT_R, 40, m.PT_MOVES, m.PT_T0, m.T1, bp, by, bk), 5)
        b = climb(ctx.K4, g, L, 7, y0, runs=1, rounds=40)[0]
        out.append((L, a, b))
        assert a == b, (L, a, b)
    return out


def witness(text, g, rng):
    from kryptos.facts import KNOWN
    slot, mpos, land = g
    eqs = [(slot[land[e]], ord(KNOWN[q]) - 65, ord(text[land[e]]) - 65) for e, q in enumerate(sorted(KNOWN))]
    st, w = _load("0128").decide(eqs, "V", rng, two=True)
    if st != "fit":
        return st
    x, _k = w
    y = [-1] * 52
    for (f, le), v in x.items():
        y[(0 if f == "P" else 26) + le] = v
    for g0 in (0, 26):
        free = [v for v in range(26) if v not in y[g0:g0 + 26]]
        rng.shuffle(free)
        for i in range(g0, g0 + 26):
            if y[i] < 0:
                y[i] = free.pop()
    return y


def kept_place(text, land, rng):
    keep = set(land)
    free = [j for j in range(N) if j not in keep]
    letters = [text[j] for j in free]
    rng.shuffle(letters)
    out = list(text)
    for j, ch in zip(free, letters):
        out[j] = ch
    return "".join(out)


def encipher(pt, g, P, C, key):
    slot, mpos, land = g
    Ci = {v: i for i, v in enumerate(C)}
    return "".join(chr(65 + Ci[(P[ord(pt[mpos[j]]) - 65] + key[slot[j]]) % 26]) for j in range(N))


# ---- workers ----
def _scan_job(args):
    b, r0, r1, text, seed = args
    rng = random.Random(seed)
    fit, st = [], {}
    for r in range(r0, r1):
        for o in "AB":
            for L in LENGTHS:
                w = witness(text, geom(r, o, L), rng)
                if isinstance(w, list):
                    fit.append([r, o, L, w])
                    st["fit"] = st.get("fit", 0) + 1
                else:
                    st[w] = st.get(w, 0) + 1
    return b, {"fit": fit, "status": st}


def decide(text, s, seed):
    r, o, L, y0 = s
    g = geom(r, o, L)
    rng = random.Random(seed)
    t0 = time.time()
    score, reading = climb(text, g, L, rng.randrange(10 ** 9), y0)
    copies = []
    while len(copies) < BASE:
        cs = climb(kept_place(text, g[2], rng), g, L, rng.randrange(10 ** 9), y0)[0]
        copies.append(cs)
        if cs >= score:
            break
    above = len(copies) if all(c < score for c in copies) else len(copies) - 1
    return {"score": score, "reading": reading, "copies": copies, "above": above, "secs": round(time.time() - t0, 1)}


def _job(args):
    key, text, s, seed = args
    return key, decide(text, s, seed)


def cell_of(tid, text, pool, W, ctx, saved):
    nb = (len(routes()) + BLOCK - 1) // BLOCK
    fit, status = [], {}
    todo = []
    for b in range(nb):
        k = f"scan:{tid}:{b}"
        if k in saved:
            fit += saved[k]["fit"]
            for s, v in saved[k]["status"].items():
                status[s] = status.get(s, 0) + v
        else:
            todo.append((b, b * BLOCK, min(len(routes()), (b + 1) * BLOCK), text, SEED * 1000 + b))
    for b, out in pool.imap_unordered(_scan_job, todo, chunksize=1):
        ctx.save(f"scan:{tid}:{b}", out)
        fit += out["fit"]
        for s, v in out["status"].items():
            status[s] = status.get(s, 0) + v
    fit.sort(key=lambda x: (x[0], x[1], x[2]))
    return fit, status


def run(ctx):
    import multiprocessing as mp
    t_start = time.time()
    W = int(os.environ.get("K4_WORKERS", 8))
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    _load("0144").lib(); glib(); _load("0128"); routes()
    m20, m26 = _load("0140").load_0120(), _load("0226")
    check = self_check(ctx)
    saved = getattr(ctx, "saved", {}) or {}
    k4 = ctx.K4
    rng = random.Random(SEED)
    targets = [("k4", k4)] + [(f"s{i}", "".join(rng.sample(k4, N))) for i in range(STAND_INS)]
    cells, statuses = {}, {}
    with mp.get_context("fork").Pool(W) as pool:
        for i, (tid, t) in enumerate(targets):
            cells[tid], statuses[tid] = cell_of(tid, t, pool, W, ctx, saved)
            ctx.progress(i + 1, len(targets), "cells scanned")
    fitk = cells["k4"]
    by = {}
    for r, o, L, _ in fitk:
        by[f"{o}{L}"] = by.get(f"{o}{L}", 0) + 1
    rec133 = __import__("json").loads((next((ROOT / "experiments").glob("0133-*")) / "raw.json").read_text())["bounds"]["summary"]
    vs133 = {f"{o}{L}": [by.get(f"{o}{L}", 0), rec133[o]["k4_by_L"][L - 1]] for o in "AB" for L in LENGTHS}

    # plants on settings K4 fits
    prng = random.Random(SEED + 1)
    texts = [("clean", pt) for _, pt in m20.make_plants(ctx.KNOWN, 10, prng, PLANTS // 2)]
    for a in (0, 1, 2):
        texts += m26.class_texts(prng, a)[:PLANTS // 6]
    work, pmeta = [], {}
    for idx, (cls, pt) in enumerate(texts):
        while True:
            r, o, L, _ = fitk[prng.randrange(len(fitk))]
            g = geom(r, o, L)
            P = list(range(26)); C = list(range(26)); prng.shuffle(P); prng.shuffle(C)
            key = [prng.randrange(26) for _ in range(L)]
            pc = encipher(pt, g, P, C, key)
            y0 = witness(pc, g, prng)
            if isinstance(y0, list):
                break
        pmeta[idx] = {"cls": cls, "setting": f"{routes()[r][0]} order {o} L={L}", "pt": pt}
        work.append((f"plant:{idx}", pc, [r, o, L, y0], 900000 + idx))
    work += [(f"k4:{i}", k4, s, 1000 + i) for i, s in enumerate(fitk)]
    for ti, (tid, t) in enumerate(targets[1:], start=1):
        rr = random.Random(SEED * 10 + ti)
        c = cells[tid]
        for i in sorted(rr.sample(range(len(c)), min(PER_STAND_IN, len(c)))):
            work.append((f"{tid}:{i}", t, c[i], 300000 + ti * 100000 + i))
    random.Random(SEED + 2).shuffle(work)
    res = {w[0]: saved[w[0]] for w in work if w[0] in saved}
    todo = [w for w in work if w[0] not in res]
    ctx.progress(len(res), len(work), "settings")
    with mp.get_context("fork").Pool(W) as pool:
        for key, out in pool.imap_unordered(_job, todo, chunksize=1):
            res[key] = out
            ctx.save(key, out)
            ctx.progress(len(res), len(work), "settings")

    found = {}
    for idx, v in pmeta.items():
        r_ = res[f"plant:{idx}"]
        v.update(found=r_["above"] >= BASE, above=r_["above"], score=r_["score"],
                 letters_right=sum(x == y for x, y in zip(r_["reading"], v.pop("pt"))))
        found.setdefault("clean" if v["cls"] == "clean" else "sanborn", []).append(v["found"])

    def rate(tid):
        ks = [k for k in res if k.startswith(tid + ":")]
        hit = sum(1 for k in ks if res[k]["above"] >= BASE)
        return {"cell_size": len(cells[tid]), "decided": len(ks), "above_all_12": hit, "rate": round(hit / len(ks), 4) if ks else None}
    per = {tid: rate(tid) for tid, _ in targets}
    sr = [per[t]["rate"] for t in per if t != "k4" and per[t]["rate"] is not None]
    kr = per["k4"]["rate"]
    ge = sum(1 for x in sr if x >= kr)
    p = (1 + ge) / (len(sr) + 1)
    top = sorted(range(len(fitk)), key=lambda i: (-res[f"k4:{i}"]["above"], -res[f"k4:{i}"]["score"]))[:20]
    top_list = [{"setting": f"{routes()[fitk[i][0]][0]} order {fitk[i][1]} L={fitk[i][2]}", "above": res[f"k4:{i}"]["above"],
                 "score": res[f"k4:{i}"]["score"], "reading": res[f"k4:{i}"]["reading"]} for i in top]
    bounds = {
        "item": "F6.2 lengths 3-10 (D2's re-cost with D1b)",
        "decider": "D1b's four runs of 0144's tempering patched for a slot and a message place per carved letter, from 0128's exact two-alphabet witness; kept-place copies one at a time, at most 12",
        "self_check_against_0144": check, "library": len(routes()), "lengths": list(LENGTHS),
        "settings_listed": len(routes()) * 2 * len(LENGTHS), "k4_status": statuses["k4"], "k4_fitting_settings": len(fitk),
        "k4_fits_by_order_length_vs_0133": vs133, "targets": per, "k4_rate": kr, "standins_rates": sr,
        "standins_at_or_above_k4": ge, "p": round(p, 4), "fair_rate_if_independent": round(1 / (BASE + 1), 4),
        "top_settings": top_list,
        "plants": {"clean_found": [sum(found.get("clean", [])), len(found.get("clean", []))],
                   "sanborn_found": [sum(found.get("sanborn", [])), len(found.get("sanborn", []))], "each": pmeta},
        "core_seconds": round(sum(v["secs"] for v in res.values())), "compute_seconds": round(time.time() - t_start),
        "exhaustive": True, "exhaustive_over": "every type-1 move of 0129's library, both orders, key lengths 3-10, that K4 fits on two free alphabets; each decided at D1b's four-run power",
        "resumed_units": len(work) - len(todo),
        "cost_estimate": "about 42,644 K4 settings (0133) and 2,000 stand-in settings at about 300 core-s each (0267's measured rate): about 3,700 core-hours, about 116 h on AWS c8g.8xlarge, about $70 (several 24-hour machine legs, resumed from the checkpoint)",
    }
    notes = (f"F6.2 lengths 3-10: {len(fitk)} settings fit K4; K4 above all 12 copies in {per['k4']['above_all_12']} ({100 * kr:.1f}%); "
             f"{len(sr)} stand-ins {100 * min(sr):.1f}-{100 * max(sr):.1f}%, {ge} at or above K4 (p {p:.2f}); plants clean "
             f"{bounds['plants']['clean_found']}, Sanborn-style {bounds['plants']['sanborn_found']}.")
    controls = [c for k, v in res.items() if k.startswith("k4:") for c in v["copies"]][:2000]
    return {"candidates": [], "bounds": bounds, "notes": notes, "controls": controls}


def encrypt(plaintext, key):
    """No candidate is submitted."""
    return plaintext


def worked_example(ctx, key):
    return "\n".join([
        "F6.2: two free alphabets around a move, key lengths 3-10, decided setting by setting.", "",
        "  setting      columns of a 9-wide grid read in key-word order, then the table with two unknown alphabets, key length 7",
        "  slot map     each carved letter's key slot and message place follow from the move",
        "  K4 gets four tempering searches under that setting; copies with K4's carved letters at the 24 landing places kept",
        "  and the rest shuffled get the same, one at a time, until one reads as well as K4 (at most 12).",
        "  Twenty shuffled stand-ins for K4 go through the whole procedure: K4's rate of wins must stand out from theirs."])
