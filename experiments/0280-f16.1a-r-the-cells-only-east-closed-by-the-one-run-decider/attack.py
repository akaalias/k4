"""Experiment: F16.1a-r. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f16.1a-r-the-cells-only-east-closed-by-the-one-run-decider",
    "title": "F16.1a-r: the free-alphabet cells only EAST closed (0274: K4 fits on the 20 official letters at key lengths 6-26, 0-2 slips), each decided by D1's one-run English decider: K4 climbed once, then fitting shuffles one at a time (at most 12, or 100 while K4 keeps winning); 24 plants",
    "family": "16-simple-hand-methods",
    "parent": "0253-f1.4-one-alphabet-residue-decided-by-the-one-run-decider",
    "changed": (
        "F16.1a-r (issue #123): the settings come from 0274 (one free alphabet, periodic key, every minimal set of 0-2 "
        "slipped places where K4 fits the 20 official letters and not the 24); the decider is 0253's (0252's generalised "
        "0140 tempering climb, copies drawn as shuffles that fit the same setting exactly), with the known letters the "
        "setting's own (the 20 official ones minus its slips, nk passed to the climb) instead of the 24. EAST's places "
        "(22-25) are read, not fixed."
    ),
    "hypothesis_expert": (
        "F1.1/F1.6 with EAST set aside (#124): Quagmire III with an unknown alphabet (C27(c)), Beaufort or added, key "
        "length L. 0274 found 20 (cell, slip count) pairs where some alphabet satisfies the 20 official equations (less "
        "the slipped ones) on K4 though none satisfies all 24; 0136: a free alphabet leaves about 88 bits the known "
        "letters cannot fix, so English decides. D1 (0228, 0229; Alexis 2026-10-28, #100): one tempering run with copies "
        "climbed one at a time qualifies for one free alphabet. Per setting the null is that K4 beats all 12 fitting "
        "copies with probability 1/13; the verdict is the count against Binomial(n, 1/13) and, per setting, K4 above "
        "100 copies at 1/101."
    ),
    "hypothesis_eli5": (
        "Without EAST, the K1/K2 kind of cipher with a scrambled alphabet fits the carving at a few key lengths where it "
        "did not before. Those fits cannot be told apart by the known letters alone, so we let a search build the most "
        "English-looking message for each, and do the same on scrambled copies that fit the same way. If the carving's "
        "message reads better than the copies' more often than chance, that length is worth a closer look."
    ),
    "prediction": (
        "K4 beats all 12 copies in about n/13 settings (no excess beyond the binomial 1% tail) and all 100 in none or one; "
        "plants (clean Carter, and Sanborn-style X stops, K1-K3 windows, three changed letters) found about 2 in 3 at "
        "these lengths (fewer at 22-26). Zero candidates: the verdict is the count."
    ),
    "method": (
        "1. Settings: every (L, form, slipped places) from 0274's record where K4 fits on 20 letters and the cell is "
        "listed as only EAST closed, at its minimal slip count. 2. For each: the known letters are the 20 official ones "
        "less the slipped places. 3. Climb K4 once (0140's tempering, 16 x 625 x 1000, 0252's slot-map version); then "
        "shuffles of K4 that fit the setting exactly, climbed one at a time, stop at the first at or above K4; at most "
        "12, 100 while K4 beats all. 4. Plants: 12 clean, 12 Sanborn-style, on settings drawn from the list, slips "
        "planted where the setting has them; found when above all 12 own copies. 5. Count against Binomial(n, 1/13)."
    ),
    "walkthrough": (
        "1. Take one setting, say Beaufort, key length 11, no slip. "
        "2. Let a search choose the scrambled alphabet and the 11 key letters to make K4's message as English as possible while NORTHEAST, BERLIN and CLOCK stay in place. "
        "3. Scramble K4's letters until the scramble also fits length 11 with some alphabet; run the same search on it. "
        "4. If the scramble reads as well as K4, stop: K4 is not special at this setting. "
        "5. If K4 beats 12 scrambles in a row, it is unusual at the 1 in 13 level; go on to 100. "
        "6. Do this for every setting and count the wins."
    ),
    "expected_minutes": 40,
}

import ctypes
import json
import os
import random
import sys
import time
import types
from pathlib import Path

N = 97
ROOT = Path(__file__).resolve().parent
OFFICIAL = tuple(range(26, 35)) + tuple(range(64, 75))
BASE, ESC = 12, 100
PLANTS = 12
_MODS = {}


def M():
    """0252's attack.py, unchanged (it loads 0140, 0128, 0129)."""
    if "m" not in _MODS:
        import importlib.util
        path = next((ROOT / "experiments").glob("0252-*")) / "attack.py"
        spec = importlib.util.spec_from_file_location("frozen0252", path)
        m = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = m
        spec.loader.exec_module(m)
        m.ROOT = ROOT
        _MODS["m"] = m
    return _MODS["m"]


def eqs_for(text, st, known):
    slot, mpos, n, form = st
    carved = {mp: j for j, mp in enumerate(mpos)}
    return [(slot[carved[q - 1]], ord(known[q]) - 65, ord(text[carved[q - 1]]) - 65) for q in sorted(known)]


def witness(text, st, known, rng=None):
    """0252's witness() on the setting's own known letters."""
    m = M()
    eqs = eqs_for(text, st, known)
    if not m._load("0129").l1_ok(eqs):
        return None
    status, w = m._load("0128").decide(eqs, st[3], rng)
    if status != "fit":
        return None
    w = ({a[1]: v for a, v in w[0].items()}, w[1])
    assert m._load("0129").check_witness(eqs, st[3], w)
    return w


def climb(text, st, seed, known, wit=None):
    """0252's climb() with the known letters given (nk = len(known))."""
    m = M()
    m0140 = m._MODS["0140"]
    L_ = m.glib()
    slot, mpos, n, form = st
    carved = {mp: j for j, mp in enumerate(mpos)}
    kp = sorted(known)
    CT = (ctypes.c_int * N)(*[ord(ch) - 65 for ch in text])
    KP = (ctypes.c_int * 24)(*([carved[q - 1] for q in kp] + [0] * (24 - len(kp))))
    KL = (ctypes.c_int * 24)(*([ord(known[q]) - 65 for q in kp] + [0] * (24 - len(kp))))
    L_.setup2(m0140._LIB["tab"], CT, N, n, (ctypes.c_int * N)(*slot), (ctypes.c_int * N)(*mpos), int(form == "B"), KP, KL, len(kp))
    L_.set_witness((ctypes.c_int * 26)(*(m.full_alphabet(wit, seed) if wit else [0] * 26)), int(bool(wit)))
    bp = (ctypes.c_int * 128)(); bx = (ctypes.c_int * 52)(); bk = (ctypes.c_int * 64)()
    sc = L_.ptemper(seed * 100003, 1, m0140.PT_R, m0140.PT_ROUNDS, m0140.PT_MOVES, m0140.PT_T0, m0140.T1, bp, bx, bk)
    return round(sc, 5), "".join(chr(65 + bp[i]) for i in range(N))


def decide(text, st, known, seed, esc):
    rng = random.Random(seed)
    w = witness(text, st, known, random.Random(1))
    t0 = time.time()
    score, reading = climb(text, st, rng.randrange(10 ** 9), known, w)
    copies, tries, lost = [], 0, 0
    limit = BASE
    while len(copies) < limit:
        sh = list(text)
        ok = None
        for _ in range(200000):
            rng.shuffle(sh); tries += 1
            cw = witness("".join(sh), st, known, rng)
            if cw is not None:
                ok = ("".join(sh), cw)
                break
        if ok is None:
            lost += 1
            break
        cs = climb(ok[0], st, rng.randrange(10 ** 9), known, ok[1])[0]
        copies.append(cs)
        if cs >= score:
            break
        if len(copies) == BASE and esc:
            limit = ESC
    above = len(copies) if all(c < score for c in copies) else len(copies) - 1
    return {"score": score, "reading": reading, "copies": copies, "above": above, "tries": tries, "lost": lost,
            "secs": round(time.time() - t0, 1)}


def _job(args):
    key, text, st, known, seed, esc = args
    known = {int(q): c for q, c in known.items()}
    return key, decide(text, st, known, seed, esc)


def settings_from_0274(K):
    raw = json.loads((next((ROOT / "experiments").glob("0274-*")) / "raw.json").read_text())["bounds"]
    out = []
    for o in raw["only_east_closed"]:
        cell, k = o["cell"], o["k"]
        form, L = cell[0], int(cell[1:])
        sets = [tuple(D) for D in raw["cells"][cell]["k4_20_sets"] if len(D) <= k]
        for D in sets:
            st = (tuple(i % L for i in range(N)), tuple(range(N)), L, form)
            known = {q: K[q] for q in OFFICIAL if q not in D}
            out.append({"cell": cell, "L": L, "form": form, "slips": list(D), "st": st, "known": known})
    return out


def run(ctx):
    import multiprocessing as mp
    from math import exp, lgamma, log
    t_start = time.time()
    W = int(os.environ.get("K4_WORKERS", 8))
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    m = M()
    m._load("0140"); m._load("0128"); m._load("0129"); m.glib()
    check = m.self_check(ctx)
    k4 = ctx.K4
    sets = settings_from_0274(ctx.KNOWN)
    for s in sets:
        assert witness(k4, s["st"], s["known"], random.Random(1)) is not None, (s["cell"], s["slips"])
    # plants
    m20, m26 = m._load("0140").load_0120(), m._load("0226")
    rng = random.Random(16110)
    prng = random.Random(16111)
    texts = [("clean", pt) for _, pt in m20.make_plants(ctx.KNOWN, 10, rng, PLANTS)]
    for a in (0, 1, 2):
        texts += m26.class_texts(rng, a)[:PLANTS // 3]
    work, pmeta = [], {}
    for idx, (cls, pt) in enumerate(texts):
        s = sets[prng.randrange(len(sets))]
        st = s["st"]
        order = list(range(26)); prng.shuffle(order)
        key = [prng.randrange(26) for _ in range(st[2])]
        pc = list(m.encipher(pt, st, order, key))
        for q in s["slips"]:
            pc[q - 1] = prng.choice([c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if c != pc[q - 1]])
        pc = "".join(pc)
        pknown = {q: pt[q - 1] for q in s["known"]}
        assert witness(pc, st, pknown, prng) is not None, (idx, s["cell"])
        pmeta[idx] = {"cls": cls, "cell": s["cell"], "slips": s["slips"], "pt": pt}
        work.append((("plant", idx), pc, st, pknown, 900000 + idx, False))
    work += [(("k4", i), k4, s["st"], s["known"], 1000 + i, True) for i, s in enumerate(sets)]
    res = {}
    saved = getattr(ctx, "saved", {}) or {}
    for key, *_ in work:
        if f"{key[0]}:{key[1]}" in saved:
            res[key] = saved[f"{key[0]}:{key[1]}"]
    todo = [w for w in work if w[0] not in res]
    todo = [(w[0], w[1], w[2], {str(q): c for q, c in w[3].items()}, w[4], w[5]) for w in todo]
    ctx.progress(len(res), len(work), "settings and plants")
    with mp.get_context("fork").Pool(W) as pool:
        for key, out in pool.imap_unordered(_job, todo, chunksize=1):
            res[key] = out
            ctx.save(f"{key[0]}:{key[1]}", out)
            ctx.progress(len(res), len(work), "settings and plants")
    found = {}
    for idx, v in pmeta.items():
        r = res[("plant", idx)]
        pt = v.pop("pt")
        v.update(found=r["above"] >= BASE, above=r["above"], score=r["score"],
                 letters_right=sum(a == b for a, b in zip(r["reading"], pt)))
        found.setdefault("clean" if v["cls"] == "clean" else "sanborn", []).append(v["found"])
    n = len(sets)
    k12 = sum(1 for i in range(n) if res[("k4", i)]["above"] >= BASE)
    k100 = sum(1 for i in range(n) if res[("k4", i)]["above"] >= ESC)
    q12, q100 = 1 / (BASE + 1), 1 / (ESC + 1)

    def tail(k, q):
        return sum(exp(lgamma(n + 1) - lgamma(j + 1) - lgamma(n - j + 1) + j * log(q) + (n - j) * log(1 - q)) for j in range(k, n + 1))
    per = []
    for i, s in enumerate(sets):
        r = res[("k4", i)]
        per.append({"cell": s["cell"], "slips": s["slips"], "above": r["above"], "copies_climbed": len(r["copies"]),
                    "score": r["score"], "copies_max": max(r["copies"]) if r["copies"] else None, "lost": r["lost"],
                    "reading": r["reading"], "east_at_22_25": r["reading"][21:25]})
    per.sort(key=lambda x: (-x["above"], -x["score"]))
    bounds = {
        "item": "F16.1a-r", "settings": n, "cells": sorted({s["cell"] for s in sets}),
        "decider": "0253's: 0252's generalised 0140 tempering (16 x 625 x 1000), copies = shuffles that fit the setting exactly on its own known letters, one at a time, stop at the first at or above K4, at most 12, 100 while K4 wins",
        "self_check_against_0140": check,
        "k4_above_all_12": k12, "expected_by_chance_12": round(n * q12, 2), "binomial_p_12": tail(k12, q12),
        "k4_above_all_100": k100, "expected_by_chance_100": round(n * q100, 2), "binomial_p_100": tail(k100, q100),
        "per_setting": per,
        "plants": {"clean_found": [sum(found.get("clean", [])), len(found.get("clean", []))],
                   "sanborn_found": [sum(found.get("sanborn", [])), len(found.get("sanborn", []))], "each": pmeta},
        "core_seconds": round(sum(r["secs"] for r in res.values())), "compute_seconds": round(time.time() - t_start),
        "exhaustive": True, "exhaustive_over": "every K4 setting 0274 lists as only EAST closed (one free alphabet, periodic key, minimal slip sets on the 20 official letters)",
        "aws_cost_estimate_dollars": 0.5,
    }
    notes = (f"{n} settings in {len(bounds['cells'])} cells; K4 above all 12 copies in {k12} (chance {n * q12:.1f}, p {bounds['binomial_p_12']:.3g}), "
             f"above all 100 in {k100}; plants clean {bounds['plants']['clean_found']}, Sanborn-style {bounds['plants']['sanborn_found']}")
    controls = [c for i in range(n) for c in res[("k4", i)]["copies"]][:2000]
    return {"candidates": [], "bounds": bounds, "notes": notes, "controls": controls}


def encrypt(plaintext, key):
    st = (tuple(key["slot"]), tuple(key["mpos"]), key["n"], key["form"])
    return M().encipher(plaintext, st, key["order"], key["key"])


def worked_example(ctx, key):
    return "\n".join([
        "F16.1a-r: one free alphabet, a periodic key, the 20 official known letters; one setting at a time.", "",
        "  setting      Beaufort, key length 11, no slip (0274: fits on 20 letters, not on 24)",
        "  K4           one tempering search for the most English reading with NORTHEAST, BERLIN, CLOCK in place",
        "  copies       scrambles of K4 that also fit length 11, one search each, until one reads as well as K4",
        "  verdict      K4 beating 12 in a row happens 1 time in 13 by chance; count over all settings"])
