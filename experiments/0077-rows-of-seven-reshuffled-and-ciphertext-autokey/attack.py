"""Experiment 0077. See program.md for the contract."""

EXPERIMENT = {
    "slug": "rows-of-seven-reshuffled-and-ciphertext-autokey",
    "title": "Both fingerprints at once: every row of seven reshuffled, and the self-feeding autokey at every distance",
    "family": "1-keyed-periodic",
    "parent": "0070-reshuffle-every-block-of-seven-and-the-table",
    "changed": "Experiment 70 joined the block-of-seven reshuffle to a repeating key, and experiment 63 joined column routes to the self-feeding autokey. The two fingerprints suggest a seven-wide stage and a feedback stage at distance 21, so this joins the block-of-seven reshuffle, all 5,040 orders, to the self-feeding autokey at every distance, in both orders.",
    "hypothesis_expert": (
        "Family 1 (ciphertext feedback) with a block transposition, chosen to explain both fingerprints in "
        "one construction: the block-of-7 permutation leaves a period-7 positional trace (the doublet "
        "column, 0056), and ciphertext autokey at lag 21 is the only generator that made the width-21 "
        "repeats (0062). Orders: (A) ciphertext autokey, then every block of 7 permuted by one fixed order; "
        "(B) the plaintext's blocks permuted, then ciphertext autokey. Autokey with a constant shift, "
        "T[j] = s*A(c[j-L]) + k0, L = 1-96; 5,040 orders (the last block of 6 keeps the order restricted to its "
        "offsets); plain, cipher and key alphabets standard or KRYPTOS, Vigenere or Beaufort, sign +1 or -1 "
        "(32 classes): 31 million cases, each an exact check of the residuals at the known places past the "
        "lag. Ten shuffled coppers through the same sweep. Clue entries: C1(a), C11a, C27(a)."
    ),
    "hypothesis_eli5": (
        "The copper carries a mark tied to seven and a mark tied to twenty-one. A seven-letter reshuffle of "
        "every row could leave the first, and the autokey that feeds on carved letters 21 places back could "
        "leave the second. Here the two are joined, in either order, for every one of the 5,040 ways of "
        "reshuffling seven letters and every feeding distance, and the 24 known letters give an exact yes "
        "or no each time. Scrambled coppers through the same test show how many yeses luck gives."
    ),
    "prediction": (
        "No (order, distance, class) case survives with three or more redundant checks beyond the "
        "shuffled-copper range, in either order; lag 21 has no case with more than two checks. Zero "
        "candidates pass."
    ),
    "method": (
        "1. For each order of seven, compute where each known place lands. 2. Order A: undo the reshuffle on "
        "the copper and run the autokey test on the result. Order B: run the autokey test on the copper with "
        "the known letters at their landing places. 3. For each lag and class, check the residuals agree; "
        "tally survivors by redundant checks. 4. Repeat on ten shuffled coppers."
    ),
    "walkthrough": (
        "1. Take the order that reverses every row of seven, and order A: autokey first, then reverse each "
        "row. 2. Undo it: reverse each row of seven of the copper, giving XOURKBO SBLUHGO WBBFILO PQQVRLF ... "
        "3. Lag 21, sculpture's alphabet from K = 0, Vigenere. Place 22: the unreversed letter P (3) minus "
        "known E (11) is 18; the letter 21 back is X (24); residual 18 - 24 = 20. 4. Place 23: Q (20) minus "
        "A (7) is 13; 21 back O (5); residual 8. 5. 20 and 8 disagree: dead. 6. Repeat for every order, lag, "
        "class and both ways round."
    ),
}

import random
from itertools import permutations
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
ALPH = {"std": STD, "kry": KRY}


def landing(perm):
    dest = [0] * N
    for b in range(0, N, 7):
        size = min(7, N - b)
        order = [o for o in perm if o < size]
        for j, o in enumerate(order):
            dest[b + o] = b + j
    return dest


def classes():
    for pa in ALPH:
        for ca in ALPH:
            for ka in ALPH:
                for mode in ("vig", "beau"):
                    for s in (1, -1):
                        yield pa, ca, ka, mode, s


def sweep(ct, known, ctx, deadline):
    items = sorted(known.items())
    tally = {"A": {}, "B": {}}
    lag21 = {"A": 0, "B": 0}
    cases = 0
    idx = {n: {c: i for i, c in enumerate(a)} for n, a in ALPH.items()}
    cls = list(classes())
    for perm in permutations(range(7)):
        dest = landing(perm)
        x = [None] * N
        for i in range(N):
            x[i] = ct[dest[i]]                   # order A: undo the reshuffle
        for order in ("A", "B"):
            text = x if order == "A" else ct
            places = [(i if order == "A" else dest[i], p) for i, p in [(pos - 1, p) for pos, p in items]]
            for pa, ca, ka, mode, s in cls:
                PI, CI, KI = idx[pa], idx[ca], idx[ka]
                T = [((CI[text[j]] - PI[p]) if mode == "vig" else (CI[text[j]] + PI[p])) % 26 for j, p in places]
                for L in range(1, 97):
                    cases += 1
                    first = None; m = 0; ok = True
                    for (j, _), t in zip(places, T):
                        if j - L < 0:
                            continue
                        r = (t - s * KI[text[j - L]]) % 26
                        m += 1
                        if first is None:
                            first = r
                        elif r != first:
                            ok = False; break
                    if ok and m >= 2:
                        c = min(m - 1, 5)
                        tally[order][c] = tally[order].get(c, 0) + 1
                        if L == 21 and c >= 3:
                            lag21[order] += 1
        if ctx.time_left() < deadline:
            return tally, lag21, cases, False
    return tally, lag21, cases, True


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    t0 = ctx.time_left()
    tally, lag21, cases, complete = sweep(ct, known, ctx, t0 * 0.7)
    rng = random.Random(77)
    ctrl = []
    for _ in range(10):
        sh = list(ct); rng.shuffle(sh)
        t, l2, c2, comp = sweep("".join(sh), known, ctx, 20)
        ctrl.append((t, comp))
        if ctx.time_left() < 25:
            break
    table = {}
    for o in ("A", "B"):
        keys = sorted(set(tally[o]) | {k for t, _ in ctrl for k in t[o]})
        table[o] = {str(k): {"k4": tally[o].get(k, 0), "controls": [t[o].get(k, 0) for t, _ in ctrl]} for k in keys}
    return {
        "candidates": [],
        "bounds": {"family": "block-of-7 permutation with ciphertext autokey (constant shift), both orders", "permutations": 5040,
                   "lags": "1-96", "classes": 32, "cases": cases, "complete": complete, "controls_complete": [c for _, c in ctrl],
                   "survivors_by_checks": table, "lag21_3plus": lag21},
        "notes": f"{cases:,} cases ({'complete' if complete else 'stopped early'}), {len(ctrl)} controls. " + " ".join(
            f"Order {o}: " + "; ".join(f"{k} checks {v['k4']} ({min(v['controls'])}-{max(v['controls'])})" for k, v in table[o].items()) + "." for o in table)
            + f" Lag 21 with 3+ checks: {lag21}.",
    }


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    I = {c: i for i, c in enumerate(KRY)}
    ct, kn = ctx.K4, ctx.KNOWN
    dest = landing((6, 5, 4, 3, 2, 1, 0))
    x = "".join(ct[dest[i]] for i in range(N))
    lines = ["every row of seven reversed after the autokey; undone: " + x[:35] + "...", "lag 21, sculpture's alphabet, Vigenere", "",
             "place  known  letter  21 back  residual"]
    for pos in (22, 23, 24, 25):
        i = pos - 1
        lines.append(f"{pos:>5}  {kn[pos]:>5}  {x[i]:>6}  {x[i - 21]:>7}  {(I[x[i]] - I[kn[pos]] - I[x[i - 21]]) % 26:>8}")
    return "\n".join(lines)
