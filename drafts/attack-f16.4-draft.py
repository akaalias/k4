"""Experiment: F16.4. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f16.4-small-shifts-per-crib-and-carved-line-pre-registered",
    "title": "F16.4: small shifts at the known places, per crib run and per carved line, maximised over the plain and KRYPTOS tables and both forms, a statistic fixed before looking; K4 against 10,000 shuffles",
    "family": "16-simple-hand-methods",
    "parent": "0029-small-shift-keys-closeness-under-all-alphabets",
    "changed": (
        "F16.4 (issue #123). 0029 tested Bean's closeness by the largest shift over all 24 known places, which one far "
        "letter spoils; the step-back review saw that under the plain table EASTNORTHEAST forces BLZCDCYYGCKAZ, 10 of 13 "
        "shifts within 3. Here the statistic counts shifts within 3 in groups (each crib run, each word, each carved "
        "line's share of the known places, all 24, the 20 official), scores each count by its binomial tail at 7/26, and "
        "takes the best over groups, tables and forms; the same maximum on 10,000 shuffles of K4 gives the p."
    ),
    "hypothesis_expert": (
        "Bean's closeness (04-structure.md, 'The minor differences'; Materna; bean-2018-kryptos-thoughts.txt): the carved "
        "letter sits near the known letter on the standard alphabet, read by Bean as a cipher alphabet near the standard "
        "one (Gromark-like). A Gronsfeld key of small digits, or a key that changes by carved line (C27(b), the 31-letter "
        "lines of the BERLIN chart; Sanborn's 'positioning'), would leave runs of small shifts. Definition, fixed before "
        "any count: forced key k = A_c(c) - A_p(p) (Vigenere) or A_c(c) + A_p(p) (Beaufort), mod 26 as -13..12, tables "
        "(A_p, A_c) in {standard, KRYPTOS}^2; a shift is small when |k| <= 3 (chance 7/26). Groups: 22-34, 64-74, each "
        "word (EAST, NORTHEAST, BERLIN, CLOCK), carved lines 2 (22-34), 3 (64-66) and 4 (67-74), all 24, the 20 official. "
        "Score per group: -log10 P(Binomial(n, 7/26) >= count). T = max over 8 table-form pairs x 10 groups. p = share of "
        "10,000 shuffles with T at or above K4's. Flag at p < 0.01: then rows for line-keyed schemes."
    ),
    "hypothesis_eli5": (
        "Under the plain Vigenere table, most of EASTNORTHEAST's letters sit only one to three places from the carved "
        "letters above them. That could mean a key of small numbers, or one that changes line by line on the copper. We "
        "fix one measure of 'how many small shifts in a group' before looking, take its best value on K4, and see how "
        "often scrambled copies of K4 do as well."
    ),
    "prediction": (
        "K4's T comes from 22-34 under the plain table (10 of 13 small); the shuffles reach it often enough that p is "
        "above 0.01 (the closeness is one of many patterns a 97-letter text can show somewhere). No candidates."
    ),
    "method": (
        "1. For each of the 8 table-form pairs, the forced key at the 24 known places, as -13..12. 2. Count |k| <= 3 in "
        "each of the 10 groups; score by the binomial tail at 7/26. 3. T = the best score. 4. The same on 10,000 "
        "shuffles of K4 (seed 16400). 5. p = (1 + shuffles at or above) / 10,001. 6. Report the best group, table and "
        "form for K4, and the per-group p's as diagnostics only."
    ),
    "walkthrough": (
        "1. Under each known letter of EASTNORTHEAST write the carved letter above it. "
        "2. Count how many alphabet steps separate them (E to F is 1, A to L is 11, S to R is -1). "
        "3. Mark the steps of size 3 or less: 10 of the 13. "
        "4. Ask how likely 10 or more of 13 is when each has a 7 in 26 chance: about 1 in 5,000. "
        "5. Do the same for every group, table and form, keep the best, and compare with scrambled copies of K4 treated the same way."
    ),
    "expected_minutes": 3,
}

import math
import random

import numpy as np

STD = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KRY = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
N_SHUF = 10000
SEED = 16400
GROUPS = {"run 22-34": range(22, 35), "run 64-74": range(64, 75), "EAST": range(22, 26), "NORTHEAST": range(26, 35),
          "BERLIN": range(64, 70), "CLOCK": range(70, 75), "line 2 (22-34)": range(22, 35), "line 3 (64-66)": range(64, 67),
          "line 4 (67-74)": range(67, 75), "all 24": None, "official 20": "official"}
TABLES = {"std": STD, "kry": KRY}


def tail(n, k, q=7 / 26):
    return sum(math.comb(n, j) * q ** j * (1 - q) ** (n - j) for j in range(k, n + 1))


def setup(known):
    Q = sorted(known)
    groups = {}
    for g, r in GROUPS.items():
        if r is None:
            idx = list(range(len(Q)))
        elif r == "official":
            idx = [i for i, q in enumerate(Q) if not 22 <= q <= 25]
        else:
            idx = [i for i, q in enumerate(Q) if q in r]
        groups[g] = idx
    groups.pop("line 2 (22-34)")      # identical to run 22-34; kept once
    score = {(len(ix), k): -math.log10(tail(len(ix), k)) for ix in groups.values() for k in range(len(ix) + 1)}
    return Q, groups, score


def T_of(text, known, Q, groups, score):
    best, arg = -1.0, None
    p = np.array([[TABLES[t].index(known[q]) for q in Q] for t in TABLES])
    c = np.array([[TABLES[t].index(text[q - 1]) for q in Q] for t in TABLES])
    for ia, a in enumerate(TABLES):
        for ib, b in enumerate(TABLES):
            for form in ("vig", "beau"):
                k = (c[ib] - p[ia]) % 26 if form == "vig" else (c[ib] + p[ia]) % 26
                small = (np.minimum(k, 26 - k) <= 3)
                for g, ix in groups.items():
                    n = int(small[ix].sum())
                    s = score[(len(ix), n)]
                    if s > best:
                        best, arg = s, (a, b, form, g, n, len(ix))
    return best, arg


def run(ctx):
    known = ctx.KNOWN
    Q, groups, score = setup(known)
    k4T, k4arg = T_of(ctx.K4, known, Q, groups, score)
    rng = random.Random(SEED)
    sh = list(ctx.K4)
    Ts = []
    per_group_null = {g: [] for g in groups}
    for i in range(N_SHUF):
        rng.shuffle(sh)
        t = "".join(sh)
        Ts.append(T_of(t, known, Q, groups, score)[0])
        if i % 500 == 0:
            ctx.progress(i, N_SHUF, "shuffles")
    ctx.progress(N_SHUF, N_SHUF, "shuffles")
    at = sum(1 for x in Ts if x >= k4T - 1e-12)
    p = (1 + at) / (N_SHUF + 1)
    # diagnostics: K4's best per group (over tables and forms)
    diag = {}
    for g, ix in groups.items():
        one = {g: ix}
        b, a = T_of(ctx.K4, known, Q, one, score)
        diag[g] = {"best_score": round(b, 3), "table_form_count": a}
    return {
        "candidates": [],
        "bounds": {
            "item": "F16.4", "statistic": "T = max over (plain table, cipher table) in {std, KRYPTOS}^2, form in {Vigenere, Beaufort}, group in 10 groups of -log10 P(Binomial(n, 7/26) >= count of |k| <= 3)",
            "groups": {g: [Q[i] for i in ix] for g, ix in groups.items()},
            "k4_T": round(k4T, 4), "k4_argmax": k4arg, "shuffles": N_SHUF, "shuffles_at_or_above": at, "p": round(p, 5),
            "flag_line": 0.01, "flag": p < 0.01,
            "shuffle_T_quantiles": {q: round(float(np.quantile(Ts, q)), 3) for q in (0.5, 0.9, 0.99, 0.999)},
            "k4_per_group": diag, "controls": f"{N_SHUF} shuffles of K4, seed {SEED}", "exhaustive": True,
            "aws_cost_estimate_dollars": 0.02,
        },
        "notes": f"K4 T {k4T:.3f} from {k4arg}; {at} of {N_SHUF} shuffles at or above, p {p:.4f} (flag below 0.01: {p < 0.01})",
    }


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    lines = ["plain table, Vigenere: shift = carved - known, as -13..12", "", "place known carved shift small"]
    for q in range(22, 35):
        k = (STD.index(ctx.K4[q - 1]) - STD.index(ctx.KNOWN[q])) % 26
        s = k if k <= 12 else k - 26
        lines.append(f"{q:>5} {ctx.KNOWN[q]:>5} {ctx.K4[q - 1]:>6} {s:>5}  {'yes' if abs(s) <= 3 else ''}")
    n = sum(1 for q in range(22, 35) if min((STD.index(ctx.K4[q - 1]) - STD.index(ctx.KNOWN[q])) % 26, (STD.index(ctx.KNOWN[q]) - STD.index(ctx.K4[q - 1])) % 26) <= 3)
    lines.append(f"\n{n} of 13 small; P(>= {n} of 13 at 7/26) = {tail(13, n):.2e}")
    return "\n".join(lines)
