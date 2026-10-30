"""Experiment 0261. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f1.12-three-measured-power-cells-against-100-copies-with-second-deciders",
    "title": "F1.12: F1.1 Beaufort 23 and 26 and F1.2 at 13, K4 against 100 of its own copies with the one-run decider, then MIX8m and the blind judge as second deciders",
    "family": "1-keyed-periodic",
    "parent": "0229-d1-one-free-alphabet-power-per-run-with-enough-plants",
    "changed": (
        "F1.12 (Alexis, 2026-10-28, #100: close at stated power and still rerun, so a missed lead gets a second chance). "
        "The three cells closed at measured power on 2026-10-28 had K4 ranked among 12 copies only (9th, 12th and 13th of "
        "13). Here each cell's K4 is ranked among 100 of its own copies, each climbed with the one-run decider (D1: one "
        "tempering run, 0140's climb for one alphabet; 0144's for two, with as many runs as D1b qualifies); the best "
        "readings then rescored by MIX8m (0233) and read by the blind judge, K4 and copies together. 8 plants per cell in the same run."
    ),
    "hypothesis_expert": (
        "F1.1 (Quagmire III with an unknown order, Beaufort form) at key lengths 23 (7 checks) and 26 (1 check), and F1.2 "
        "(Quagmire IV, two unknown alphabets) at 13 (11 checks): the known letters leave thousands of alphabets, so English "
        "decides. Design 2 (0139-0146) put K4 9th, 12th and 13th of 13; D1 (0228, 0229) and A6.2 (0226) measured power "
        "on clean and Sanborn-style plants: L23 33/40 and 32/48, L26 13/24 and 17/24, L13 7/10 and 17/24. With 100 copies "
        "K4's rank is measured to 1%; MIX8m (1.95 bits per letter against the quadgrams' 1.75) and the judge (which reads "
        "telegraphese and abbreviated English, 0251) are second deciders that do not share the climb's score. Clue entries "
        "C27(c), C5(a); A6, A13."
    ),
    "hypothesis_eli5": (
        "Three versions of the cipher table with a scrambled alphabet were closed after K4 read no better than 12 scrambled "
        "copies of itself. Twelve is a small crowd. Here K4 faces 100 copies in each, and two more readers judge the "
        "results: a stronger statistical model of English, and a language model that reads for words."
    ),
    "prediction": (
        "K4 inside its copies in all three cells on all three deciders: rank by the climb's score within the middle 90%, "
        "MIX8m and judge ranks likewise; no cell with K4 above all 100. Plants found about as D1 measured (5-7 of 8)."
    ),
    "method": (
        "1. Cells: (one alphabet, Beaufort, 23), (one alphabet, Beaufort, 26), (two alphabets, 13). "
        "2. Copies: one alphabet, shuffles of K4 that 0120's exact decider fits at that length (as 0140); two alphabets, "
        "kept-place copies (the carved letters at the 24 known places kept, the other 73 shuffled, as 0144), started from K4's witness. "
        "3. Every text climbed with the one-run decider (RUNS_ONE runs of 0140's tempering; RUNS_TWO of 0144's), its best "
        "reading kept. "
        "4. Deciders: the climb's quadgram score; MIX8m on the reading; the blind judge on K4's and the 100 copies' readings in "
        "one call per cell. K4's rank among its copies on each. "
        "5. Plants: 4 clean and 4 Sanborn-style per cell, 6 own copies, through the same climb; found when above all own copies."
    ),
    "walkthrough": (
        "1. Take one cell, say a scrambled alphabet on both sides of the table with a key of 23 letters, Beaufort form. "
        "2. Search for the alphabet and key that make K4 read most like English while keeping the 24 known letters. "
        "3. Make 100 scrambled copies of K4 that fit the same 24 letters equally well and search each the same way. "
        "4. Rank K4's best reading among the 100 copies' by the search's score, by a stronger English model, and by a "
        "language model reading for words. "
        "5. A real answer should come out on top on all three."
    ),
    "expected_minutes": 30,
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
CELLS = (("1.1-B23", "one", 23), ("1.1-B26", "one", 26), ("1.2-13", "two", 13))
N_COPIES = 100
PLANTS, OWN = 8, 6
RUNS_ONE = 1               # D1 (Alexis, #100): one run qualifies for one free alphabet
RUNS_TWO = 4               # D1b (0257): four runs qualify for two free alphabets (66 of 96 against ten runs' 71), one does not (63)
SEED = 2580
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


def climb(kind, L, text, seed, y0):
    """Best of the decider's runs: (quadgram score, reading)."""
    from kryptos.facts import KNOWN
    kp = sorted(KNOWN)
    CT = (ctypes.c_int * N)(*[ord(ch) - 65 for ch in text])
    KP = (ctypes.c_int * 24)(*[q - 1 for q in kp])
    KL = (ctypes.c_int * 24)(*[ord(KNOWN[q]) - 65 for q in kp])
    if kind == "one":
        m = _load("0140"); L_ = m.lib(); runs = RUNS_ONE
        L_.setup(m._LIB["tab"], CT, N, L, KP, KL, 24)
    else:
        m = _load("0144"); L_ = m.lib4(); runs = RUNS_TWO
        L_.setup(m._LIB["tab"], CT, N, L, KP, KL, 24)
        L_.set_start((ctypes.c_int * 52)(*y0))
    best = (-99.0, "?" * N)
    for r in range(runs):
        bp = (ctypes.c_int * 128)(); bx = (ctypes.c_int * 52)(); bk = (ctypes.c_int * 64)()
        sc = L_.ptemper(seed * 100003 + r, 1, m.PT_R, m.PT_ROUNDS, m.PT_MOVES, m.PT_T0, m.T1, bp, bx, bk)
        if sc > best[0]:
            best = (round(sc, 5), "".join(chr(65 + bp[i]) if 0 <= bp[i] < 26 else "?" for i in range(N)))
    return list(best)


def _job(args):
    key, kind, L, text, seed, y0 = args
    return key, climb(kind, L, text, seed, y0)


def build(ctx):
    known, k4 = ctx.KNOWN, ctx.K4
    m40, m44, m26 = _load("0140"), _load("0144"), _load("0226")
    m20, m23 = m40.load_0120(), m44.load_0123()
    m40.lib(); m44.lib(); m44.lib4()
    m28 = _load("0228")
    kidx = set(q - 1 for q in known)
    free = [j for j in range(N) if j not in kidx]
    jobs, meta = [], {}
    rng = random.Random(SEED)
    for cell, kind, L in CELLS:
        if kind == "one":
            texts = [("k4", k4, None)]
            while len(texts) < N_COPIES + 1:
                sh = "".join(rng.sample(k4, N))
                if m20.decide(m20.equations(sh, known, L), "B", rng)[0] == "fit":
                    texts.append((f"copy{len(texts) - 1}", sh, None))
            plants = [("clean", pt, pc, None) for pc, pt in m20.make_plants(known, L, rng, PLANTS // 2)]
            for cls, pt in m26.class_texts(rng, 0)[::3][:PLANTS // 2]:
                alpha = list(ctx.STANDARD_ALPHABET); rng.shuffle(alpha)
                plants.append((cls, pt, m20.beaufort_encrypt(pt, "".join(alpha), [rng.randrange(26) for _ in range(L)]), None))
        else:
            y4 = None
            while y4 is None:
                y4 = m28._witness(m44, m23, k4, known, rng)
            texts = [("k4", k4, y4)]
            for i in range(N_COPIES):
                letters = [k4[j] for j in free]; rng.shuffle(letters)
                cp = list(k4)
                for j, ch in zip(free, letters):
                    cp[j] = ch
                texts.append((f"copy{i}", "".join(cp), y4))
            plants = []
            while len(plants) < PLANTS // 2:
                pc, pt = m44.plant4(L, rng, known)
                y0 = m28._witness(m44, m23, pc, known, rng)
                if y0 is not None:
                    plants.append(("clean", pt, pc, y0))
            for cls, pt in m26.class_texts(rng, 1)[::3][:PLANTS // 2]:
                y0 = None
                while y0 is None:
                    P = list(range(26)); C = list(range(26)); rng.shuffle(P); rng.shuffle(C)
                    Ci = {v: j for j, v in enumerate(C)}
                    k = [rng.randrange(26) for _ in range(L)]
                    pc = "".join(chr(65 + Ci[(P[ord(ch) - 65] + k[j % L]) % 26]) for j, ch in enumerate(pt))
                    y0 = m28._witness(m44, m23, pc, known, rng)
                plants.append((cls, pt, pc, y0))
        for tid, t, y in texts:
            jobs.append((f"{cell}|{tid}", kind, L, t, rng.randrange(10 ** 9), y))
        for i, (cls, pt, pc, y0) in enumerate(plants):
            meta[(cell, i)] = {"cls": cls, "pt": pt}
            jobs.append((f"{cell}|plant{i}", kind, L, pc, rng.randrange(10 ** 9), y0))
            for g in range(OWN):
                if kind == "one":
                    while True:
                        sh = "".join(rng.sample(pc, N))
                        if m20.decide(m20.equations(sh, known, L), "B", rng)[0] == "fit":
                            break
                else:
                    letters = [pc[j] for j in free]; rng.shuffle(letters)
                    cp = list(pc)
                    for j, ch in zip(free, letters):
                        cp[j] = ch
                    sh = "".join(cp)
                jobs.append((f"{cell}|plant{i}_own{g}", kind, L, sh, rng.randrange(10 ** 9), y0))
    return jobs, meta


def run(ctx):
    import multiprocessing as mp
    t0 = time.time()
    jobs, meta = build(ctx)
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    saved = getattr(ctx, "saved", {}) or {}
    res = {j[0]: saved[j[0]] for j in jobs if j[0] in saved}        # units an earlier run of this attack.py finished (#105)
    todo = [j for j in jobs if j[0] not in res]
    W = int(os.environ.get("K4_WORKERS", 8))
    ctx.progress(len(res), len(jobs), "climbs")
    with mp.get_context("fork").Pool(W) as pool:
        for key, out in pool.imap_unordered(_job, todo, chunksize=1):
            res[key] = out
            ctx.save(key, out)
            ctx.progress(len(res), len(jobs), "climbs")
    m36 = _load("0236"); m36.lib(); m36.models()
    out_cells, judge_calls, judge_none = {}, 0, 0
    for cell, kind, L in CELLS:
        tids = ["k4"] + [f"copy{i}" for i in range(N_COPIES)]
        q = [res[f"{cell}|{t}"][0] for t in tids]
        rd = [res[f"{cell}|{t}"][1] for t in tids]
        mx = [float(x) for x in m36.mix8m(rd)]
        jr = ctx.judge(rd)                       # K4 and its 100 copies in one call, blind (program.md)
        judge_calls += len(rd)
        js = [(r["score"] if r and r.get("score") is not None else 0) for r in jr]
        judge_none += sum(1 for r in jr if not r or r.get("score") is None)
        pf = 0
        for i in range(PLANTS):
            s = res[f"{cell}|plant{i}"][0]
            pf += s > max(res[f"{cell}|plant{i}_own{g}"][0] for g in range(OWN))
        out_cells[cell] = {
            "runs_per_text": RUNS_ONE if kind == "one" else RUNS_TWO,
            "quadgram": {"k4": q[0], "copies_at_or_above": sum(1 for x in q[1:] if x >= q[0])},
            "mix8m": {"k4": round(mx[0], 2), "copies_at_or_above": sum(1 for x in mx[1:] if x >= mx[0])},
            "judge": {"k4": js[0], "copies_at_or_above": sum(1 for x in js[1:] if x >= js[0]), "copies_max": max(js[1:])},
            "k4_reading": rd[0], "k4_known_in_place": sum(rd[0][p - 1] == ch for p, ch in ctx.KNOWN.items()),
            "plants_found": [pf, PLANTS],
            "plants_by_class": {c: sum(1 for i in range(PLANTS) if meta[(cell, i)]["cls"] == c) for c in {v["cls"] for (cc, _), v in meta.items() if cc == cell}},
        }
    top = [c for c, v in out_cells.items() if any(v[d]["copies_at_or_above"] == 0 for d in ("quadgram", "mix8m", "judge"))]
    bounds = {
        "item": "F1.12", "cells": out_cells, "k4_copies_per_cell": N_COPIES,
        "copies": "one alphabet: shuffles 0120's exact decider fits at the length (as 0140); two alphabets: kept-place copies from K4's witness (as 0144)",
        "decider": f"one-run decider: 0140's tempering x {RUNS_ONE} (one alphabet), 0144's x {RUNS_TWO} (two alphabets); second deciders MIX8m (0233) and the blind judge",
        "judge_calls": judge_calls, "judge_none": judge_none,
        "cells_with_k4_above_all_copies_on_some_decider": top,
        "power_reference": "0229 (L23 one run: clean 21-23/24, Sanborn-style 14-16/24; L26 11-18, 11-17), D1b (L13)",
        "compute_seconds": round(time.time() - t0), "exhaustive": False,
        "modal_cost_estimate": "2 x (101 + 56) one-run climbs (about 17 s) and 157 four-run climbs (about 70 s): about 4.5 core-hours, under $1 of Modal credit (about $3.7 left after the margin); the judge 303 calls",
    }
    notes = "F1.12: " + "; ".join(
        f"{c}: K4 quadgram {v['quadgram']['copies_at_or_above']}/100 at or above, MIX8m {v['mix8m']['copies_at_or_above']}, "
        f"judge {v['judge']['copies_at_or_above']} (K4 {v['judge']['k4']}), plants {v['plants_found'][0]}/{PLANTS}"
        for c, v in out_cells.items())
    controls = [res[f"{c}|copy{i}"][0] for c, _, _ in CELLS for i in range(N_COPIES)]
    return {"candidates": [], "bounds": bounds, "notes": notes, "controls": controls}


def encrypt(plaintext, key):
    """No candidate is submitted."""
    return plaintext


def worked_example(ctx, key):
    return "\n".join([
        "F1.12: three cells, K4 against 100 of its own copies, three deciders.", "",
        "  cell            alphabets  key length  checks",
        "  F1.1 B23        one        23          7",
        "  F1.1 B26        one        26          1",
        "  F1.2 13         two        13          11", "",
        "  each text: one tempering run keeping the 24 known letters -> best reading",
        "  rank K4 among its copies by quadgrams, by MIX8m, by the blind judge."])
