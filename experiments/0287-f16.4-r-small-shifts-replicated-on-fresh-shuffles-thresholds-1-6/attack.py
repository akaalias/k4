"""Experiment: F16.4. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f16.4-r-small-shifts-replicated-on-fresh-shuffles-thresholds-1-6",
    "title": "F16.4-r: 0286's small-shift flag (10 of 13 shifts within 3 at 22-34 on the plain table, p 0.0065) on 100,000 fresh shuffles, and the same statistic maximised over the thresholds 1-6 as well, since the threshold 3 was picked after the review had seen K4's shifts",
    "family": "16-simple-hand-methods",
    "parent": "0286-f16.4-small-shifts-per-crib-and-carved-line-pre-registered",
    "changed": (
        "F16.4-r (issue #123). 0286's statistic T crossed its line (p 0.0065 < 0.01, 64 of 10,000 shuffles). A result "
        "outside the copies stops the queue and is replicated first. Two changes: (1) the same T against 100,000 fresh "
        "shuffles (new seeds), on all 24 letters and on the 20 official letters alone; (2) T* = the same maximum taken "
        "over the thresholds |k| <= 1..6 as well (each scored by its own binomial tail at (2t+1)/26), for K4 and for "
        "every shuffle: the threshold 3 was chosen by the step-back review after it had seen BLZCDCYYGCKAZ, so T's p is "
        "too small by the choice of threshold, and T* pays for that choice. Strength aimed at: sampled, 100,000 shuffles."
    ),
    "hypothesis_expert": (
        "Bean's closeness (04-structure.md, 'The minor differences'; bean-2018-kryptos-thoughts.txt), C27(b) (carved "
        "lines), as 0286. Forced key k = A_c(c) - A_p(p) (Vigenere) or A_c(c) + A_p(p) (Beaufort) as -13..12, tables in "
        "{standard, KRYPTOS}^2, groups as 0286 (the two runs, the four words, carved lines 3 and 4, all 24, the 20 "
        "official). T (threshold 3) and T* (thresholds 1-6). Null: shuffles of the 97 carved letters with the known "
        "letters kept where they are. Lines fixed before the run: T replicates if p < 0.01 on the fresh shuffles; the "
        "flag stands as a lead only if T*'s p is also below 0.01; between the two it is recorded as 'at the edge, "
        "threshold-dependent' and the line-keyed rows are still added (run more experiments, #100) with that label."
    ),
    "hypothesis_eli5": (
        "The first test found that K4's known letters near EASTNORTHEAST sit unusually close to the carved letters, "
        "closer than all but 64 of 10,000 scrambled copies. But the cut-off for 'close' (three steps) was chosen after "
        "looking at K4. Here we repeat the count on 100,000 new scrambled copies and also let every copy pick its own "
        "best cut-off from one to six steps, which is the fair comparison."
    ),
    "prediction": (
        "T replicates (p between 0.004 and 0.01 on 100,000 shuffles). T* is weaker: p between 0.01 and 0.05, so the "
        "flag is threshold-dependent. On the 20 official letters alone (NORTHEAST 7 of 9) p is above 0.05."
    ),
    "method": (
        "1. For each of the 8 table-form pairs, the forced key at the known places, as a distance 0-13 from zero. "
        "2. For each threshold t in 1-6 and each of the 10 groups, count distances <= t and score the count by the "
        "binomial tail at (2t+1)/26. 3. T = best score at t = 3; T* = best score over t = 1-6. 4. K4 and 100,000 "
        "shuffles (200 jobs of 500, each its own seed), on the 24 and on the 20 official letters. 5. p = (1 + shuffles "
        "at or above) / 100,001. 6. Plants as 0286: five messages (four with small shifts, one without), each against "
        "2,000 own shuffles on T*."
    ),
    "walkthrough": (
        "1. Under each known letter of EASTNORTHEAST write the carved letter above it. "
        "2. Count the alphabet steps between them (E to F is 1, A to L is 11, S to R is 1 back). "
        "3. For a cut-off of 3 steps, 10 of the 13 are close; for 2 steps, 9; for 1 step, 4. "
        "4. Work out how surprising each count is when letters fall by chance, and keep the most surprising. "
        "5. Do exactly the same on scrambled copies of K4 and count how many are at least as surprising."
    ),
    "expected_minutes": 5,
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
SEED = 16450                      # 0286 used 16400
THRESH = (1, 2, 3, 4, 5, 6)
GROUPS = {"run 22-34": range(22, 35), "run 64-74": range(64, 75), "EAST": range(22, 26), "NORTHEAST": range(26, 35),
          "BERLIN": range(64, 70), "CLOCK": range(70, 75), "line 3 (64-66)": range(64, 67),
          "line 4 (67-74)": range(67, 75), "all 24": None, "official 20": "official"}
TABLES = {"std": STD, "kry": KRY}
_G = {}


def tail(n, k, q):
    return sum(math.comb(n, j) * q ** j * (1 - q) ** (n - j) for j in range(k, n + 1))


def setup(known, official_only=False):
    Q = sorted(q for q in known if not (official_only and 22 <= q <= 25))
    groups = {}
    for g, r in GROUPS.items():
        if r is None:
            idx = list(range(len(Q)))
        elif r == "official":
            idx = [i for i, q in enumerate(Q) if not 22 <= q <= 25]
        else:
            idx = [i for i, q in enumerate(Q) if q in r]
        if idx:
            groups[g] = idx
    if official_only:                 # without EAST: run 22-34 is NORTHEAST, all = official 20
        groups.pop("run 22-34", None); groups.pop("all 24", None)
    score = {(len(ix), k, t): -math.log10(tail(len(ix), k, (2 * t + 1) / 26)) for ix in groups.values() for k in range(len(ix) + 1) for t in THRESH}
    return Q, groups, score


def T_of(text, known, Q, groups, score):
    """-> (T at threshold 3, its argmax, T* over thresholds 1-6, its argmax)."""
    b3, a3, bs, as_ = -1.0, None, -1.0, None
    p = np.array([[TABLES[t].index(known[q]) for q in Q] for t in TABLES])
    c = np.array([[TABLES[t].index(text[q - 1]) for q in Q] for t in TABLES])
    for ia, a in enumerate(TABLES):
        for ib, b in enumerate(TABLES):
            for form in ("vig", "beau"):
                k = (c[ib] - p[ia]) % 26 if form == "vig" else (c[ib] + p[ia]) % 26
                dist = np.minimum(k, 26 - k)
                for t in THRESH:
                    small = dist <= t
                    for g, ix in groups.items():
                        n = int(small[ix].sum())
                        s = score[(len(ix), n, t)]
                        if s > bs:
                            bs, as_ = s, (a, b, form, g, n, len(ix), t)
                        if t == 3 and s > b3:
                            b3, a3 = s, (a, b, form, g, n, len(ix), t)
    return b3, a3, bs, as_


def _job(j):
    rng = random.Random(SEED * 1000 + j)
    out = {}
    for kn in ("k24", "k20"):
        known, Q, groups, score = _G[kn]
        sh = list(_G["K4"])
        t3, ts = [], []
        for _ in range(PER_JOB):
            rng.shuffle(sh)
            r = T_of("".join(sh), known, Q, groups, score)
            t3.append(round(r[0], 6)); ts.append(round(r[2], 6))
        out[kn] = {"T": t3, "Tstar": ts}
    return j, out


def run(ctx):
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    known = dict(ctx.KNOWN)
    _G["K4"] = ctx.K4
    for kn, off in (("k24", False), ("k20", True)):
        Q, groups, score = setup(known, off)
        _G[kn] = (known, Q, groups, score)
    k4 = {kn: T_of(ctx.K4, *_G[kn]) for kn in ("k24", "k20")}
    # self-check against 0286: T on the 24 letters is 10 of 13 at 22-34, plain table, Vigenere, score 3.607
    assert k4["k24"][1][:6] == ("std", "std", "vig", "run 22-34", 10, 13) and abs(k4["k24"][0] - 3.607) < 1e-3, k4["k24"]
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
    for kn in ("k24", "k20"):
        T = np.array([x for j in range(N_JOBS) for x in res[j][kn]["T"]])
        S = np.array([x for j in range(N_JOBS) for x in res[j][kn]["Tstar"]])
        a3 = int((T >= k4[kn][0] - 1e-9).sum()); a_s = int((S >= k4[kn][2] - 1e-9).sum())
        summ[kn] = {"k4_T": round(k4[kn][0], 4), "k4_T_argmax": k4[kn][1], "T_at_or_above": a3, "p_T": round((1 + a3) / (n + 1), 6),
                    "k4_Tstar": round(k4[kn][2], 4), "k4_Tstar_argmax": k4[kn][3], "Tstar_at_or_above": a_s, "p_Tstar": round((1 + a_s) / (n + 1), 6),
                    "T_quantiles": {str(q): round(float(np.quantile(T, q)), 3) for q in (0.5, 0.9, 0.99, 0.999)},
                    "Tstar_quantiles": {str(q): round(float(np.quantile(S, q)), 3) for q in (0.5, 0.9, 0.99, 0.999)}}
    # K4's counts at 22-34 on the plain table per threshold (diagnostic)
    kq = [(STD.index(ctx.K4[q - 1]) - STD.index(known[q])) % 26 for q in range(22, 35)]
    per_t = {str(t): sum(1 for k in kq if min(k, 26 - k) <= t) for t in THRESH}
    # plants, as 0286, judged on T*
    from kryptos.plants import english_plant
    plant_specs = [("std", "vig", "all", "small digits 0-3, period 7, plain table, whole text"),
                   ("kry", "vig", "all", "small digits 0-3, period 5, KRYPTOS table, whole text"),
                   ("std", "vig", "line2", "small digits on carved line 2 (places 5-35) only, a random key elsewhere"),
                   ("std", "beau", "line4", "Beaufort, small key values on carved line 4 (places 67-97) only"),
                   ("std", "vig", "none", "a random key everywhere (must not be found)")]
    plants = []
    Q, groups, score = _G["k24"][1:]
    for j, (tb, form, where, what) in enumerate(plant_specs):
        prng = random.Random(SEED + 100 + j)
        pt = english_plant(SEED + 100 + j)
        A = TABLES[tb]
        per = [prng.randrange(0, 4) for _ in range(7 if j != 1 else 5)]
        out = []
        for i, ch in enumerate(pt):
            q = i + 1
            small_here = where == "all" or (where == "line2" and 5 <= q <= 35) or (where == "line4" and q >= 67)
            k = per[i % len(per)] if small_here else prng.randrange(26)
            pv = A.index(ch)
            out.append(A[(pv + k) % 26] if form == "vig" else A[(k - pv) % 26])
        ct = "".join(out)
        pk = {q: pt[q - 1] for q in Q}
        pr = T_of(ct, pk, Q, groups, score)
        shp = list(ct)
        pTs = []
        for _ in range(2000):
            prng.shuffle(shp)
            pTs.append(T_of("".join(shp), pk, Q, groups, score)[2])
        pp = (1 + sum(1 for x in pTs if x >= pr[2] - 1e-9)) / 2001
        plants.append({"what": what, "Tstar": round(pr[2], 3), "argmax": pr[3], "p": round(pp, 4), "found": pp < 0.01, "should_be_found": where != "none"})
    plants_ok = sum(1 for x in plants if x["found"] == x["should_be_found"])
    s24 = summ["k24"]
    verdict = ("replicated on both statistics" if s24["p_T"] < 0.01 and s24["p_Tstar"] < 0.01 else
               "at the edge, threshold-dependent" if s24["p_T"] < 0.01 else "not replicated")
    return {
        "candidates": [],
        "bounds": {
            "item": "F16.4-r", "shuffles": n, "seeds": f"{SEED * 1000}..{SEED * 1000 + N_JOBS - 1}", "thresholds": list(THRESH),
            "statistics": "T: 0286's (threshold 3). T*: the same maximum over thresholds 1-6, each count scored by its binomial tail at (2t+1)/26",
            "summary": summ, "k4_small_counts_22_34_plain_table": per_t, "k4_shifts_22_34_plain_table": [k if k <= 12 else k - 26 for k in kq],
            "lines": "T replicates below 0.01; a lead only if T* is below 0.01 too", "verdict": verdict,
            "plants": plants, "plants_as_expected": f"{plants_ok} of {len(plants)}",
            "controls": f"{n} shuffles of K4 with the known letters kept in place", "exhaustive": True, "aws_cost_estimate_dollars": 0.05,
        },
        "notes": (f"24 letters: T p {s24['p_T']} ({s24['T_at_or_above']} of {n}), T* {s24['k4_Tstar']} from {s24['k4_Tstar_argmax']} p {s24['p_Tstar']} ({s24['Tstar_at_or_above']}); "
                  f"20 official: T p {summ['k20']['p_T']}, T* p {summ['k20']['p_Tstar']}; verdict: {verdict}; plants as expected {plants_ok}/{len(plants)}"),
    }


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    lines = ["plain table, Vigenere: shift = carved - known, as -13..12", "", "place known carved shift"]
    ks = []
    for q in range(22, 35):
        k = (STD.index(ctx.K4[q - 1]) - STD.index(ctx.KNOWN[q])) % 26
        s = k if k <= 12 else k - 26
        ks.append(abs(s))
        lines.append(f"{q:>5} {ctx.KNOWN[q]:>5} {ctx.K4[q - 1]:>6} {s:>5}")
    lines.append("")
    for t in THRESH:
        n = sum(1 for x in ks if x <= t)
        lines.append(f"within {t}: {n} of 13; P(>= {n} of 13 at {2 * t + 1}/26) = {tail(13, n, (2 * t + 1) / 26):.2e}")
    return "\n".join(lines)
