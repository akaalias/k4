"""Experiment 0268. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f15.3-do-the-drafts-help-the-climb-find-held-out-plants",
    "title": "F15.3: held-out drafts planted under two free alphabets at key lengths 13 and 20, each climbed with English alone and with English mixed with the drafts' quadgrams, against 12 kept-place copies climbed the same way",
    "family": "15-content-from-k1-k3",
    "parent": "0257-d1b-two-free-alphabets-power-per-run-at-13-and-16",
    "changed": (
        "F15.3, power first (issue #118). 0257's harness (0144's compiled two-alphabet tempering, D1b's four runs, kept-place "
        "copies) with two changes: the plants are the 24 held-out drafts of F15.2 (written by another model and prompt, never "
        "in the prior), and every text is climbed under two score tables, English quadgrams (today's decider) and English "
        "mixed half and half with the quadgrams of the 329 corpus drafts (the draft prior). A third table (a fifth drafts) is "
        "reported, not used for the verdict."
    ),
    "hypothesis_expert": (
        "F1.2's two-free-alphabet cells (Quagmire IV) at 13 and 20 are blocked for lack of checks: the 24 known letters fit "
        "copies as often as K4, and English alone finds about two thirds of plants (0257: 66 of 96 at four runs). If K4's "
        "plaintext is Sanborn's own prose on the subjects he named (reports/f15.1-content-model.md: a paced location, a meeting "
        "at the World Clock, the crowds of 1989, two breaches, light and shadow, K3 continued, a pointer onward), a score that "
        "knows that vocabulary should pull the climb towards the planted reading and away from English-like junk, and so find "
        "more plants against copies climbed with the same score. The prior is a quadgram table: log10 of 0.5 P_english(q) + "
        "0.5 P_drafts(q), P_drafts from every quadgram of the 329 corpus drafts that touches a free place. Held-out drafts "
        "are never in it. Clue entries: C2 (instructions in the earlier text), C20(a) (K4 comes back to the first part), "
        "C27(c) (two alphabets)."
    ),
    "hypothesis_eli5": (
        "We wrote about 350 guesses at what K4 might say, based on the first three messages and on what Sanborn has said about "
        "it. Here we test whether those guesses help our search at all before using them on K4. We hide 24 other guesses, "
        "written separately, as secret messages, and see how often the search finds each one when it knows only English, and "
        "how often when it also knows the guesses' typical words. If the guesses do not help by at least two hidden messages "
        "in twelve, we drop the idea."
    ),
    "prediction": (
        "English alone finds about 14-17 of 24 (0257's rate); the draft prior finds 2-5 more, because the held-out drafts share "
        "the corpus's subject words (CROWDS, PACES, SHADOW, MESSAGE). Copies climbed with the prior also score higher, so the "
        "gain is smaller than the gain in letters right. Pre-registered verdict: the bar (4 more of 24, the row's 2 of 12) "
        "is met or not; under it, F15.4-F15.6 close as weak."
    ),
    "method": (
        "1. Plants: the first 24 held-out drafts of data/drafts/drafts.jsonl, 12 at key length 13 and 12 at 20 (alternating), "
        "each enciphered on two random alphabets and a random key (seeded), with an exact witness (0123's decider through 0144's "
        "witness4). "
        "2. Copies: 12 per plant, the 73 free places shuffled, the 24 known places kept. "
        "3. Tables: E (English quadgrams, 0144's), D50 (log10 of 0.5 English + 0.5 drafts), D20 (0.8 English + 0.2 drafts). "
        "4. Every text (24 plants and 288 copies) climbed under each table: four runs of 0144's tempering from the witness. "
        "5. Found: the plant's best above all 12 of its copies' bests under the same table. Also letters right. "
        "6. Verdict: found(D50) - found(E) over 24, bar 4."
    ),
    "walkthrough": (
        "1. Take a guessed K4 text no search has seen, for example one written by a different model. "
        "2. Encipher it with two scrambled alphabets and a 13-letter key. "
        "3. Make 12 copies of the ciphertext with the 73 letters at unknown places shuffled. "
        "4. Search each for the most English-looking reading with the 24 known letters held in place. "
        "5. Search them again with a score that also rewards the four-letter pieces common in the other guesses. "
        "6. Under each score, the plant is found if its best beats all 12 copies' bests. "
        "7. Count found plants under each score; the drafts help if the second count is at least four higher over 24 plants."
    ),
    "expected_minutes": 60,
}

import ctypes
import importlib.util
import json
import math
import os
import random
import signal
import sys
import time
import types
from pathlib import Path

N = 97
ROOT = Path(__file__).resolve().parent
LENGTHS = (13, 20)
PLANTS = 24
N_OWN = 12
RUNS = 4
ROUNDS = 625
SEED = 2680 + 268
TABLES = {"E": 1.0, "D50": 0.5, "D20": 0.8}       # weight of English in the mix
BAR = 4
_MODS = {}
_TAB = {}


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


def drafts():
    rows = [json.loads(x) for x in (ROOT / "data" / "drafts" / "drafts.jsonl").read_text().splitlines()]
    return [r for r in rows if r["set"] == "corpus"], [r for r in rows if r["set"] == "heldout"]


def tables():
    """The three score tables, as 0144's C code reads them (26^4 log10 probabilities)."""
    if _TAB:
        return _TAB
    from kryptos.facts import KNOWN
    from kryptos.scorer import _table
    logs, floor = _table()
    corpus, _ = drafts()
    free = set(i for i in range(N) if (i + 1) not in KNOWN)
    cnt = {}
    for r in corpus:
        t = r["text"]
        for j in range(N - 3):
            if free & {j, j + 1, j + 2, j + 3}:
                cnt[t[j:j + 4]] = cnt.get(t[j:j + 4], 0) + 1
    tot = sum(cnt.values())
    idx = lambda q: ((ord(q[0]) - 65) * 26 + ord(q[1]) - 65) * 676 + (ord(q[2]) - 65) * 26 + ord(q[3]) - 65
    pe = [10 ** floor] * 26 ** 4
    for q, v in logs.items():
        if len(q) == 4 and q.isalpha() and q.isupper():
            pe[idx(q)] = 10 ** v
    pd = [0.0] * 26 ** 4
    for q, v in cnt.items():
        pd[idx(q)] = v / tot
    for name, w in TABLES.items():
        _TAB[name] = (ctypes.c_double * 26 ** 4)(*[math.log10(w * a + (1 - w) * b) for a, b in zip(pe, pd)])
    _TAB["_info"] = {"draft_quadgrams": tot, "distinct": len(cnt)}
    return _TAB


class _Slow(Exception):
    pass


def _witness(m44, m23, pc, known, L, rng, secs=20):
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


def climb(L, text, seed, y0, tab):
    """0144's two-alphabet tempering, unchanged, under the given table: best (score, reading) of RUNS runs."""
    from kryptos.facts import KNOWN
    m = _load("0144")
    L_ = m.lib4()
    kp = sorted(KNOWN)
    CT = (ctypes.c_int * N)(*[ord(ch) - 65 for ch in text])
    KP = (ctypes.c_int * 24)(*[q - 1 for q in kp])
    KL = (ctypes.c_int * 24)(*[ord(KNOWN[q]) - 65 for q in kp])
    L_.setup(tables()[tab], CT, N, L, KP, KL, 24)
    L_.set_start((ctypes.c_int * 52)(*y0))
    best = (-99.0, None)
    for r in range(RUNS):
        bp = (ctypes.c_int * 128)(); bx = (ctypes.c_int * 52)(); bk = (ctypes.c_int * 64)()
        sc = L_.ptemper(seed * 100003 + r, 1, m.PT_R, ROUNDS, m.PT_MOVES, m.PT_T0, m.T1, bp, bx, bk)
        if sc > best[0]:
            best = (round(sc, 5), "".join(chr(65 + bp[i]) for i in range(N)))
    return best


def _job(args):
    key, L, text, seed, y0 = args
    t0 = time.time()
    out = {t: climb(L, text, seed, y0, t) for t in TABLES}
    return key, {"res": out, "secs": round(time.time() - t0, 1)}


def build(ctx):
    known = ctx.KNOWN
    m44 = _load("0144")
    m23 = m44.load_0123()
    m44.lib(); m44.lib4()
    free = [j for j in range(N) if (j + 1) not in known]
    _, held = drafts()
    held = held[:PLANTS]
    jobs, meta = [], {}
    for i, r in enumerate(held):
        L = LENGTHS[i % 2]
        rng = random.Random(SEED * 1000 + i)
        pt = r["text"]
        y0 = None
        while y0 is None:
            P = list(range(26)); C = list(range(26)); rng.shuffle(P); rng.shuffle(C)
            Ci = {v: j for j, v in enumerate(C)}
            k = [rng.randrange(26) for _ in range(L)]
            pc = "".join(chr(65 + Ci[(P[ord(ch) - 65] + k[j % L]) % 26]) for j, ch in enumerate(pt))
            y0 = _witness(m44, m23, pc, known, L, rng)
        meta[i] = {"draft": r["id"], "hyp": r["hyp"], "L": L, "pt": pt}
        jobs.append((f"plant:{i}", L, pc, rng.randrange(10 ** 9), y0))
        for g in range(N_OWN):
            letters = [pc[j] for j in free]; rng.shuffle(letters)
            cp = list(pc)
            for j, ch in zip(free, letters):
                cp[j] = ch
            jobs.append((f"own:{i}:{g}", L, "".join(cp), rng.randrange(10 ** 9), y0))
    return jobs, meta


def run(ctx):
    import multiprocessing as mp
    t_start = time.time()
    tables()
    jobs, meta = build(ctx)
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    saved = getattr(ctx, "saved", {}) or {}
    res = {j[0]: saved[j[0]] for j in jobs if j[0] in saved}
    todo = [j for j in jobs if j[0] not in res]
    W = int(os.environ.get("K4_WORKERS", 8))
    ctx.progress(len(res), len(jobs), "texts")
    with mp.get_context("fork").Pool(W) as pool:
        for key, s in pool.imap_unordered(_job, todo, chunksize=1):
            res[key] = s
            ctx.save(key, s)
            ctx.progress(len(res), len(jobs), "texts")

    found = {t: {L: 0 for L in LENGTHS} for t in TABLES}
    each = {}
    for i, v in meta.items():
        row = {"draft": v["draft"], "hyp": v["hyp"], "L": v["L"]}
        for t in TABLES:
            sc, rd = res[f"plant:{i}"]["res"][t]
            own = [res[f"own:{i}:{g}"]["res"][t][0] for g in range(N_OWN)]
            f = sc > max(own)
            found[t][v["L"]] += f
            row[t] = {"found": f, "above": sum(sc > o for o in own), "score": sc,
                      "letters_right": sum(a == b for a, b in zip(rd, v["pt"])), "reading": rd}
        each[i] = row
    tot = {t: sum(found[t].values()) for t in TABLES}
    gain = tot["D50"] - tot["E"]
    lr = {t: round(sum(each[i][t]["letters_right"] for i in each) / len(each), 1) for t in TABLES}
    met = gain >= BAR
    info = _TAB["_info"]
    bounds = {
        "item": "F15.3 (power first)", "cells": "F1.2 two free alphabets (Quagmire IV), key lengths 13 and 20",
        "decider": "0144's compiled tempering unchanged (16 x 625 x 1000), D1b's four runs, from the exact witness",
        "plants": f"{len(meta)} held-out drafts (claude-sonnet-5-5, prompt h1; never in the prior), alternating 13 and 20",
        "own_copies": N_OWN, "null_per_plant": "1/13", "copies": "kept-place: the 24 known places kept, the 73 others shuffled",
        "tables": {"E": "English quadgrams (0144's)", "D50": "log10(0.5 P_eng + 0.5 P_drafts)", "D20": "log10(0.8 P_eng + 0.2 P_drafts)"},
        "draft_prior": f"{info['draft_quadgrams']} quadgrams ({info['distinct']} distinct) from the 329 corpus drafts, windows touching a free place",
        "found_by_table_and_length": found, "found_by_table": tot, "gain_D50_over_E": gain, "bar": BAR, "bar_met": met,
        "mean_letters_right_by_table": lr, "each": each,
        "texts": len(jobs), "climbs": len(jobs) * len(TABLES), "runs_per_climb": RUNS,
        "core_seconds": round(sum(v["secs"] for v in res.values())), "compute_seconds": round(time.time() - t_start),
        "resumed_units": len(jobs) - len(todo), "exhaustive": False,
        "cost_estimate": "312 texts x 3 tables x 4 runs x about 18 s: about 19 core-hours; on AWS 32 cores about 40 min, about $0.40",
    }
    notes = (f"F15.3: plants found against 12 own copies, English {tot['E']}/24, drafts 50% {tot['D50']}/24, drafts 20% "
             f"{tot['D20']}/24; gain {gain} against the bar {BAR}: {'met' if met else 'not met'}. Letters right "
             f"{lr['E']}, {lr['D50']}, {lr['D20']}.")
    controls = [res[k]["res"]["E"][0] for k in res if k.startswith("own:")]
    return {"candidates": [], "bounds": bounds, "notes": notes, "controls": controls}


def encrypt(plaintext, key):
    """No candidate is submitted."""
    return plaintext


def worked_example(ctx, key):
    return "\n".join([
        "F15.3 asks whether guessed texts help the search. For one hidden test message and its 12 shuffled copies:", "",
        "  score E     English four-letter pieces only            plant best vs copies' bests",
        "  score D50   half English, half the guesses' pieces     plant best vs copies' bests",
        "  found when the plant beats all 12 copies under the same score.", "",
        "24 test messages written by another model; the guesses help if D50 finds at least 4 more than E."])
