"""Experiment 0070. See program.md for the contract."""

EXPERIMENT = {
    "slug": "reshuffle-every-block-of-seven-and-the-table",
    "title": "Every block of seven letters reshuffled the same way, before or after the table",
    "family": "6-transposition-then-tableau",
    "parent": "0006-columnar-then-tableau-period-survival",
    "changed": "The copper's doublets line up in sevens. Experiment 6 tested columnar routes, which read a grid down its columns. This tests the other way a grid of seven can be used: each row of seven letters reshuffled by the same order and read across, before or after a repeating secret word on the table, for all 5,040 orders.",
    "hypothesis_expert": (
        "Family 6 re-entered with a stated reason (it had rested after eleven reverts): the width-7 "
        "doublet column (0056, real at corrected p 0.005) is a period-7 positional trace, and the one "
        "width-7 transposition not yet tested is the block permutation, write in rows of 7 and permute the "
        "letters within every row by one fixed order (a 'matrix' in the C1(a) sense; also the "
        "one-row-at-a-time reading of C27(a)), which keeps each letter in its row of seven. 0006 covered "
        "columnar read-outs only. Orders: (A) periodic tableau then block permutation, (B) block permutation "
        "then periodic tableau. All 5,040 permutations of 7 (the last block of 6 keeps the relative order of "
        "its letters), periods 1-52, plain and cipher alphabets standard or KRYPTOS, Vigenere or Beaufort "
        "(8 classes; the key alphabet drops out of a consistency test, and variant Beaufort equals Vigenere "
        "here). A (permutation, class, period) survives if every key slot's forced values agree. Ten "
        "shuffled coppers through the same sweep. Clue entries: C1(a), C11a ('interval 7'), C27(a)."
    ),
    "hypothesis_eli5": (
        "Five of the six doubled letters fall in the same column when the copper is written in rows of "
        "seven. One simple way to leave such a trace is to write the message in rows of seven and shuffle "
        "the letters inside every row in the same order, then encipher with a repeating secret word, or the "
        "other way round. There are only 5,040 orders for seven letters, so we try them all with every "
        "length of secret word up to 52 and see whether any fits the 24 known letters better than "
        "scrambled coppers do."
    ),
    "prediction": (
        "In both orders, no permutation makes any period up to 26 consistent under any class, except where "
        "the shuffled coppers do the same at a similar rate; periods 27-29 stay consistent as always. No "
        "period is singled out at multiples of 7. Zero candidates pass."
    ),
    "method": (
        "1. For each order of seven, map each known place to the carved place it lands on. 2. For each "
        "class, compute the key value each known letter forces, and its slot: the plaintext place in order "
        "A, the carved place in order B. 3. For each period up to 52, check that each slot's values agree. "
        "4. Count consistent cases per period, and the smallest consistent period. 5. Repeat on ten shuffled "
        "coppers."
    ),
    "walkthrough": (
        "1. Take the order that reverses every row of seven, and order A: encipher first, then reverse each "
        "row. 2. Place 22 is the first letter of its row, so after reversing it is carved at place 28, P. "
        "3. Known E over carved P, on the sculpture's alphabet with Vigenere, needs key letter M, in slot 0 of "
        "a 7-letter word. 4. Place 29 is also first in its row, carved at place 35, O; known T over O needs R, "
        "also slot 0. 5. M and R disagree, so this order with a 7-letter word is dead. 6. Repeat for all "
        "5,040 orders, both ways round, every word length and way of using the table."
    ),
}

import random
from itertools import permutations
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
ALPH = {"std": STD, "kry": KRY}
PMAX = 52


def landing(perm):
    """dest[i] = carved index of plaintext index i when each block of 7 is permuted: output[j] = block[perm[j]]
    (the last block of 6 keeps perm's order restricted to its offsets)."""
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
            for mode in ("vig", "beau"):
                yield pa, ca, mode


def sweep(ct, known, ctx, deadline):
    items = sorted(known.items())
    counts = {"A": [0] * (PMAX + 1), "B": [0] * (PMAX + 1)}
    minimal = {"A": [], "B": []}
    cases = 0
    cls = list(classes())
    idx = {n: {c: i for i, c in enumerate(a)} for n, a in ALPH.items()}
    for perm in permutations(range(7)):
        dest = landing(perm)
        for pa, ca, mode in cls:
            PI, CI = idx[pa], idx[ca]
            for order in ("A", "B"):
                eqs = []
                for pos, p in items:
                    i = pos - 1; j = dest[i]
                    t = (CI[ct[j]] - PI[p]) % 26 if mode == "vig" else (CI[ct[j]] + PI[p]) % 26
                    eqs.append((i if order == "A" else j, t))
                smallest = None
                for P in range(1, PMAX + 1):
                    cases += 1
                    slot = {}
                    ok = True
                    for s_, t in eqs:
                        if slot.setdefault(s_ % P, t) != t:
                            ok = False; break
                    if ok:
                        counts[order][P] += 1
                        if smallest is None:
                            smallest = P
                if smallest is not None and smallest <= 26:
                    minimal[order].append({"perm": list(perm), "class": f"{pa}/{ca}/{mode}", "period": smallest})
        if ctx.time_left() < deadline:
            return counts, minimal, cases, False
    return counts, minimal, cases, True


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    t0 = ctx.time_left()
    counts, minimal, cases, complete = sweep(ct, known, ctx, t0 * 0.6)
    rng = random.Random(70)
    ctrl = []
    for _ in range(10):
        sh = list(ct); rng.shuffle(sh)
        c2, m2, n2, comp = sweep("".join(sh), known, ctx, 25)
        ctrl.append({"counts": c2, "le26": {o: len(m2[o]) for o in m2}, "complete": comp})
        if ctx.time_left() < 30:
            break
    def summary(cn):
        return {o: {str(P): cn[o][P] for P in range(1, PMAX + 1) if cn[o][P]} for o in cn}
    return {
        "candidates": [],
        "bounds": {"family": "block-of-7 permutation before or after a periodic tableau", "permutations": 5040, "periods": f"1-{PMAX}",
                   "classes": 8, "cases": cases, "complete": complete,
                   "k4_consistent_by_period": summary(counts), "k4_smallest_period_le26": {o: minimal[o][:30] for o in minimal},
                   "k4_le26_counts": {o: len(minimal[o]) for o in minimal},
                   "controls": [{"le26": c["le26"], "complete": c["complete"], "consistent_by_period": summary(c["counts"])} for c in ctrl]},
        "notes": f"{cases:,} cases ({'complete' if complete else 'stopped early'}). Cases whose smallest consistent period is 26 or less: K4 A {len(minimal['A'])}, B {len(minimal['B'])}; controls A {[c['le26']['A'] for c in ctrl]}, B {[c['le26']['B'] for c in ctrl]}.",
    }


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    I = {c: i for i, c in enumerate(KRY)}
    dest = landing((6, 5, 4, 3, 2, 1, 0))
    ct, kn = ctx.K4, ctx.KNOWN
    lines = ["every row of seven reversed, after a 7-letter key; sculpture's alphabet, Vigenere", "", "place  carved at  carved  known  key  slot"]
    for pos in (22, 29, 23, 30):
        j = dest[pos - 1]
        lines.append(f"{pos:>5}  {j + 1:>8}  {ct[j]:>6}  {kn[pos]:>5}  {KRY[(I[ct[j]] - I[kn[pos]]) % 26]:>3}  {(pos - 1) % 7:>4}")
    return "\n".join(lines)
