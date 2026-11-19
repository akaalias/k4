"""Experiment: F16.4a. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f16.4a-what-carries-the-small-shifts-line-or-letter",
    "title": "F16.4a: what carries K4's small shifts (0286, 0287): the plaintext letter (Bean's grouping: the known letters that are in KRYPTOS, or the late half of the alphabet), the carved line with those letters held apart, or a free offset per carved line; each statistic against 100,000 shuffles",
    "family": "16-simple-hand-methods",
    "parent": "0287-f16.4-r-small-shifts-replicated-on-fresh-shuffles-thresholds-1-6",
    "changed": (
        "F16.4a (issue #123). 0287 replicated the small shifts at 22-34 (p 0.004-0.008). Seven of the ten known "
        "plaintext letters that are in KRYPTOS sit in 22-34, so 'by line' and 'by letter' are confounded. Three "
        "statistics, each the best binomial score over the 8 table-form pairs and the cut-offs 1-6, as 0287's T*: "
        "(1) CLASS: groups by plaintext letter (in KRYPTOS: 10 places; not: 14; N-Z: 12; A-M: 12); (2) APART: the line "
        "with the letters held apart (22-34 without its KRYPTOS letters: 6 places) and the letters with the line held "
        "apart (the KRYPTOS letters outside 22-34: 3 places), scored separately; (3) OFFSET: shifts within the cut-off "
        "of some offset 0-25, on line 3 (64-66), line 4 (67-74) and 64-74. Strength aimed at: sampled."
    ),
    "hypothesis_expert": (
        "Bean's closeness (04-structure.md, 'The minor differences': for the ten known plaintext letters in KRYPTOS the "
        "carved letter is within 2 of it in 9, summing to 21; bean-2018-kryptos-thoughts.txt), C27(b) (carved lines). A "
        "shift that depends on the letter is what a keyword-mixed alphabet set against the plain one leaves (letters "
        "after the keyword's letters barely move); a shift that depends on the place is what a key of small steps on "
        "one line, or a small-step key plus an offset per line, leaves. Forced key k as 0287. Null: shuffles of the 97 "
        "carved letters, known letters kept. Seen at the desk before this run, so descriptive, not tests: CLASS's "
        "KRYPTOS group (9 of 10 within 2) and APART's raw counts (3 of 6 within 3; 2 of 3 within 2). OFFSET was looked "
        "at by hand for the plain table only. Lines: each statistic's p against 100,000 shuffles; below 0.01 counts as "
        "carrying the pattern. The row that follows depends on which does: CLASS only: alphabets (F16.4d first); "
        "APART's line part or OFFSET: line-keyed schemes (F16.4b, F16.4c)."
    ),
    "hypothesis_eli5": (
        "K4's known letters near EASTNORTHEAST sit close to the carved letters. That stretch also holds most of the "
        "known S, T, O and R. So is it the place that makes the letters close, or the letters themselves? We count "
        "closeness for the same letters elsewhere, and for other letters in the same stretch, and check whether the "
        "second stretch (BERLINCLOCK) is close once a fixed number of steps is taken off, each against scrambled copies."
    ),
    "prediction": (
        "CLASS is the strongest (p below 0.002), by its KRYPTOS group. APART: the line without those letters is "
        "ordinary (p above 0.05); the letters outside the line cannot reach a small p with 3 places. OFFSET ordinary "
        "(p above 0.05). So the pattern goes with the letters, not the line."
    ),
    "method": (
        "1. For each of the 8 table-form pairs the forced key at the 24 known places. 2. CLASS, APART (two parts), "
        "OFFSET as defined, each the best -log10 binomial tail over tables, cut-offs 1-6 (and offsets 0-25 for OFFSET) "
        "and its groups. 3. K4 and 100,000 shuffles (200 jobs of 500, own seeds). 4. Sixteen plants (four of each kind), each against 2,000 own "
        "shuffles: a small-step key on carved line 2 only; a dictionary keyword alphabet on the plain side with a "
        "small-step key; a small-step key plus an offset per carved line; a random key."
    ),
    "walkthrough": (
        "1. List the known places whose message letter is one of K, R, Y, P, T, O, S: ten of the 24. "
        "2. For each, count the alphabet steps to the carved letter above it; nine are 2 or fewer. "
        "3. Do the same for the six places of 22-34 whose letter is not one of those (E, A, N, H, E, A). "
        "4. For BERLINCLOCK, try taking the same number of steps off every shift and count the small ones left. "
        "5. Score each count by how rare it is by chance; repeat on scrambled copies and compare."
    ),
    "expected_minutes": 6,
}

import math
import multiprocessing as mp
import os
import random
import sys
import types

import numpy as np

STD = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KRY = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
N_JOBS = 200
PER_JOB = 500
SEED = 16470
THRESH = (1, 2, 3, 4, 5, 6)
TABLES = {"std": STD, "kry": KRY}
STATS = ("CLASS", "APART_line", "APART_letters", "OFFSET")
_G = {}


def tail(n, k, q):
    return sum(math.comb(n, j) * q ** j * (1 - q) ** (n - j) for j in range(k, n + 1))


def setup(known):
    Q = sorted(known)
    ix = lambda f: [i for i, q in enumerate(Q) if f(q)]
    inkry = lambda q: known[q] in "KRYPTOS"
    groups = {
        "CLASS": {"in KRYPTOS": ix(inkry), "not in KRYPTOS": ix(lambda q: not inkry(q)),
                  "N-Z": ix(lambda q: known[q] >= "N"), "A-M": ix(lambda q: known[q] < "N")},
        "APART_line": {"22-34 without KRYPTOS letters": ix(lambda q: q <= 34 and not inkry(q))},
        "APART_letters": {"KRYPTOS letters outside 22-34": ix(lambda q: q > 34 and inkry(q))},
        "OFFSET": {"line 3 (64-66)": ix(lambda q: 64 <= q <= 66), "line 4 (67-74)": ix(lambda q: 67 <= q <= 74), "run 64-74": ix(lambda q: q >= 64)},
    }
    sizes = {len(v) for g in groups.values() for v in g.values()}
    score = {(n, k, t): -math.log10(tail(n, k, (2 * t + 1) / 26)) for n in sizes for k in range(n + 1) for t in THRESH}
    return Q, groups, score


def stats_of(text, known, Q, groups, score):
    """-> {stat: (best score, argmax)}"""
    best = {s: (-1.0, None) for s in STATS}
    p = np.array([[TABLES[t].index(known[q]) for q in Q] for t in TABLES])
    c = np.array([[TABLES[t].index(text[q - 1]) for q in Q] for t in TABLES])
    for ia, a in enumerate(TABLES):
        for ib, b in enumerate(TABLES):
            for form in ("vig", "beau"):
                k = (c[ib] - p[ia]) % 26 if form == "vig" else (c[ib] + p[ia]) % 26
                dist = np.minimum(k, 26 - k)
                for t in THRESH:
                    small = dist <= t
                    for st in ("CLASS", "APART_line", "APART_letters"):
                        for g, ix in groups[st].items():
                            n = int(small[ix].sum())
                            s = score[(len(ix), n, t)]
                            if s > best[st][0]:
                                best[st] = (s, (a, b, form, g, n, len(ix), t))
                for g, ix in groups["OFFSET"].items():
                    kk = k[ix]
                    d = (kk[None, :] - np.arange(26)[:, None]) % 26
                    d = np.minimum(d, 26 - d)                      # 26 offsets x places
                    for t in THRESH:
                        cnt = (d <= t).sum(axis=1)
                        o = int(cnt.argmax()); n = int(cnt[o])
                        s = score[(len(ix), n, t)]
                        if s > best["OFFSET"][0]:
                            best["OFFSET"] = (s, (a, b, form, g, n, len(ix), t, o))
    return best


def _job(j):
    rng = random.Random(SEED * 1000 + j)
    known, Q, groups, score = _G["cfg"]
    sh = list(_G["K4"])
    out = {s: [] for s in STATS}
    for _ in range(PER_JOB):
        rng.shuffle(sh)
        r = stats_of("".join(sh), known, Q, groups, score)
        for s in STATS:
            out[s].append(round(r[s][0], 6))
    return j, out


def make_plant(j, kind, ws):
    from kryptos.plants import english_plant
    prng = random.Random(SEED + 100 + j)
    pt = english_plant(SEED + 100 + j)
    per = [prng.randrange(0, 4) for _ in range(7)]
    offs = {1: 0, 2: 0, 3: prng.randrange(4, 23), 4: prng.randrange(4, 23)}
    PA = STD
    word = None
    if kind == "alphabet":
        word = prng.choice([w for w in ws if 8 <= len(w) <= 12])
        seen = []
        for ch in word + STD:
            if ch not in seen:
                seen.append(ch)
        PA = "".join(seen)
    out = []
    for i, ch in enumerate(pt):
        q = i + 1
        line = 1 if q <= 4 else 2 if q <= 35 else 3 if q <= 66 else 4
        if kind == "line2":
            k = per[i % 7] if line == 2 else prng.randrange(26)
        elif kind == "offsets":
            k = per[i % 7] + offs[line]
        elif kind == "alphabet":
            k = per[i % 7]
        else:
            k = prng.randrange(26)
        out.append(STD[(PA.index(ch) + k) % 26])
    return pt, "".join(out), {"kind": kind, "word": word, "offsets": offs if kind == "offsets" else None}


def run(ctx):
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    known = dict(ctx.KNOWN)
    Q, groups, score = setup(known)
    _G["K4"] = ctx.K4
    _G["cfg"] = (known, Q, groups, score)
    k4 = stats_of(ctx.K4, known, Q, groups, score)
    # self-check: Bean's count, 9 of the 10 KRYPTOS letters within 2 on the plain table
    kq = {q: (STD.index(ctx.K4[q - 1]) - STD.index(known[q])) % 26 for q in Q}
    assert sum(1 for q in Q if known[q] in "KRYPTOS" and min(kq[q], 26 - kq[q]) <= 2) == 9
    saved = getattr(ctx, "saved", {}) or {}
    res = {int(k): v for k, v in saved.items()}
    todo = [j for j in range(N_JOBS) if j not in res]
    ctx.progress(len(res), N_JOBS, "jobs of 500 shuffles")
    W = int(os.environ.get("K4_WORKERS", 8))
    with mp.get_context("fork").Pool(W) as pool:
        for j, out in pool.imap_unordered(_job, todo, chunksize=1):
            res[j] = out
            ctx.save(str(j), out)
            ctx.progress(len(res), N_JOBS, "jobs of 500 shuffles")
    n = N_JOBS * PER_JOB
    summ = {}
    for s in STATS:
        v = np.array([x for j in range(N_JOBS) for x in res[j][s]])
        at = int((v >= k4[s][0] - 1e-9).sum())
        summ[s] = {"k4": round(k4[s][0], 4), "k4_argmax": k4[s][1], "at_or_above": at, "p": round((1 + at) / (n + 1), 6),
                   "quantiles": {str(q): round(float(np.quantile(v, q)), 3) for q in (0.5, 0.9, 0.99, 0.999)}}
    # plants
    ws = [w.strip().upper() for w in (ROOT / "kryptos" / "data" / "words.txt").read_text().split()]
    ws = [w for w in ws if w.isalpha()]
    expect = {"line2": ("APART_line",), "alphabet": ("CLASS",), "offsets": ("OFFSET",), "random": ()}
    plants = []
    for j, kind in enumerate(("line2", "alphabet", "offsets", "random") * 4):
        pt, ct, info = make_plant(j, kind, ws)
        pk = {q: pt[q - 1] for q in Q}
        pQ, pg, psc = setup(pk)
        pr = stats_of(ct, pk, pQ, pg, psc)
        prng = random.Random(SEED + 500 + j)
        shp = list(ct)
        null = {s: [] for s in STATS}
        for _ in range(2000):
            prng.shuffle(shp)
            r = stats_of("".join(shp), pk, pQ, pg, psc)
            for s in STATS:
                null[s].append(r[s][0])
        pp = {s: round((1 + sum(1 for x in null[s] if x >= pr[s][0] - 1e-9)) / 2001, 4) for s in STATS}
        flagged = [s for s in STATS if pp[s] < 0.01]
        ok = all(s in flagged for s in expect[kind]) and (kind != "random" or not flagged)
        plants.append({**info, "p": pp, "flagged": flagged, "expected": list(expect[kind]), "as_expected": ok,
                       "sizes": {s: {g: len(ix) for g, ix in pg[s].items()} for s in STATS}})
        ctx.progress(N_JOBS, N_JOBS, f"plant {j + 1} of 16")
    ok = sum(1 for x in plants if x["as_expected"])
    carried = [s for s in STATS if summ[s]["p"] < 0.01]
    return {
        "candidates": [],
        "bounds": {
            "item": "F16.4a", "shuffles": n, "thresholds": list(THRESH), "tables": "standard and KRYPTOS, plain and cipher side; Vigenere and Beaufort (8)",
            "groups": {s: {g: [Q[i] for i in ix] for g, ix in groups[s].items()} for s in STATS},
            "summary": summ, "carried_by": carried, "line": "p < 0.01 per statistic (three questions: 0.0033 if corrected)",
            "seen_before_the_run": "CLASS's KRYPTOS group (9 of 10 within 2) and APART's raw counts on the plain table",
            "plants": plants, "plants_as_expected": f"{ok} of {len(plants)}",
            "controls": f"{n} shuffles of K4 with the known letters kept in place", "exhaustive": True, "aws_cost_estimate_dollars": 0.05,
        },
        "notes": ("; ".join(f"{s}: K4 {summ[s]['k4']} {summ[s]['k4_argmax']} p {summ[s]['p']}" for s in STATS)
                  + f"; carried by {carried}; plants as expected {ok}/{len(plants)}"),
    }


ROOT = __import__("pathlib").Path(__file__).resolve().parent


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    lines = ["plain table, Vigenere: shift = carved - known, as -13..12", "", "place known carved shift  in KRYPTOS"]
    for q in sorted(ctx.KNOWN):
        k = (STD.index(ctx.K4[q - 1]) - STD.index(ctx.KNOWN[q])) % 26
        s = k if k <= 12 else k - 26
        lines.append(f"{q:>5} {ctx.KNOWN[q]:>5} {ctx.K4[q - 1]:>6} {s:>5}  {'yes' if ctx.KNOWN[q] in 'KRYPTOS' else ''}")
    return "\n".join(lines)
