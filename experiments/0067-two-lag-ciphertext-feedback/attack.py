"""Experiment 0067. See program.md for the contract."""

EXPERIMENT = {
    "slug": "two-lag-ciphertext-feedback",
    "title": "Two earlier carved letters as the key at once, with or without a short repeating word",
    "family": "1-keyed-periodic",
    "parent": "0066-ciphertext-autokey-plus-a-repeating-key",
    "changed": "Experiment 66 used one earlier carved letter as the key. The two fingerprints point at two different distances, 1 and 21, so here the key is the sum or difference of two earlier carved letters at any pair of distances, a letter-for-letter cousin of the Gromark, optionally with a repeating word of up to 30 letters on top.",
    "hypothesis_expert": (
        "Family 1 (ciphertext feedback), extending 0066 to two lags: T[i] = s1*A(c[i-a]) + s2*A(c[i-b]) + "
        "k[i mod P], 1 <= a < b <= 74, s1, s2 = +1 or -1, P = 1..30 (P = 1 is a constant shift, which includes "
        "no extra key), plain, cipher and key alphabets standard or KRYPTOS, Vigenere or Beaufort (16 "
        "classes; variant Beaufort is the all-minus sign). This is a lagged-Fibonacci (Gromark-like) feedback "
        "on letters rather than digits; a = 1, b = 21 would produce both the width-7 column mechanism of "
        "0065 and the width-21 repeats of 0062 in one stage. Because the carved text is known, the feedback "
        "subtracts out and each crib with i >= b gives an exact equation on the periodic key. 2,701 lag "
        "pairs x 4 signs x 16 classes x 30 periods = 5.2 million cases. Survivors are tallied by redundant "
        "checks against ten shuffled coppers through the same sweep; forced fragments matched against words. "
        "Clue entries: C11a, C4(b) (Scheidt's 'base' remark read as a running numerical key), C22(a) (a "
        "Gromark-style generator)."
    ),
    "hypothesis_eli5": (
        "The copper's two oddities are tied to the distances 1 and 21. A cipher whose key is made from two "
        "earlier carved letters, one just before and one 21 back, would leave both marks. We try every pair "
        "of distances, adding or subtracting each letter, with or without a short repeating secret word on "
        "top. Because every carved letter is visible, each of the 24 known letters gives an exact yes or "
        "no. Scrambled coppers through the same test show how many yeses luck gives."
    ),
    "prediction": (
        "No case with three or more redundant checks survives, including a = 1, b = 21 under every sign, "
        "class and period. With no extra key (P = 1) nothing survives at all. Survivors with one or two checks "
        "occur at the shuffled-copper rate; no fragment matches a word. Zero candidates pass."
    ),
    "method": (
        "1. For each pair of distances, signs and way of using the table, subtract the two earlier carved "
        "letters from the total key at each known place past the larger distance. 2. For each word length up "
        "to 30, check that places sharing a slot agree. 3. Tally consistent cases by redundant checks. "
        "4. Repeat on ten shuffled coppers. 5. Match forced fragments against words."
    ),
    "walkthrough": (
        "1. Count letters along KRYPTOSABCDEFGHIJLMNQUVWXZ from K = 0, and take distances 1 and 21, both "
        "added, with no extra word beyond a constant. 2. Place 22: carved F (12), known E (11), previous "
        "carved W (23), carved 21 back O (5): the constant is 12 - 11 - 23 - 5 = -27, which is 25, Z. "
        "3. Place 23: carved L (17), known A (7), previous carved F (12), carved 21 back B (8): 17 - 7 - 12 - 8 "
        "= -10, which is 16, J. 4. Z and J disagree, so this pair of distances with a constant is dead under "
        "this way of using the table. 5. With a 2-letter repeating word instead of a constant, places 22 "
        "and 24 would have to agree, and so on. 6. Repeat for every pair, sign, word length and way of using "
        "the table."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY, load_k1, load_k2, load_k3

N = 97
ALPH = {"std": STD, "kry": KRY}
PMAX = 30


def letters(s):
    return "".join(c for c in s.upper() if "A" <= c <= "Z")


def classes():
    for pa in ALPH:
        for ca in ALPH:
            for ka in ALPH:
                for mode in ("vig", "beau"):
                    yield pa, ca, ka, mode


def build_pairs(crib):
    """For each period P and minimum index b: pairs of crib indices that share a slot (each vs the first
    in its slot), restricted to cribs at index >= b."""
    out = {}
    pos = [i for i, _ in crib]
    for P in range(1, PMAX + 1):
        for b in range(1, 75):
            first, pairs, eq = {}, [], 0
            for x, i in enumerate(pos):
                if i < b:
                    continue
                eq += 1
                j = i % P
                if j in first:
                    pairs.append((first[j], x))
                else:
                    first[j] = x
            out[(P, b)] = (pairs, eq)
    return out


def sweep(ct, known, pairs_tab, ctx, deadline, collect=False):
    crib = sorted((pos - 1, p) for pos, p in known.items())
    tally, surv, cases = {}, [], 0
    for cl in classes():
        pa, ca, ka, mode = cl
        PI = {c: i for i, c in enumerate(ALPH[pa])}; CI = {c: i for i, c in enumerate(ALPH[ca])}; KI = {c: i for i, c in enumerate(ALPH[ka])}
        T = [((CI[ct[i]] - PI[p]) if mode == "vig" else (CI[ct[i]] + PI[p])) % 26 for i, p in crib]
        for a in range(1, 74):
            for b in range(a + 1, 75):
                for s1 in (1, -1):
                    for s2 in (1, -1):
                        d = [((T[x] - s1 * KI[ct[i - a]] - s2 * KI[ct[i - b]]) % 26) if i >= b else None for x, (i, _) in enumerate(crib)]
                        for P in range(1, PMAX + 1):
                            pairs, eq = pairs_tab[(P, b)]
                            if not pairs:
                                continue
                            cases += 1
                            ok = True
                            for x, y in pairs:
                                if d[x] != d[y]:
                                    ok = False; break
                            if ok:
                                checks = len(pairs)
                                key = min(checks, 6)
                                tally[key] = tally.get(key, 0) + 1
                                if collect and (checks >= 2 or (a == 1 and b == 21)):
                                    surv.append({"a": a, "b": b, "signs": [s1, s2], "period": P, "class": "/".join(cl), "checks": checks})
            if ctx.time_left() < deadline:
                return tally, surv, cases, False
    return tally, surv, cases, True


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    crib = sorted((pos - 1, p) for pos, p in known.items())
    pt = build_pairs(crib)
    t0 = ctx.time_left()
    tally, surv, cases, complete = sweep(ct, known, pt, ctx, t0 * 0.55, collect=True)
    rng = random.Random(67)
    ctrl = []
    for r in range(10):
        sh = list(ct); rng.shuffle(sh)
        t, _, c2, comp2 = sweep("".join(sh), known, pt, ctx, 25)
        ctrl.append((t, c2, comp2))
        if ctx.time_left() < 30:
            break
    keys = sorted(set(tally) | {k for t, _, _ in ctrl for k in t})
    table = {f"checks {k}{'+' if k == 6 else ''}": {"k4": tally.get(k, 0), "controls": [t.get(k, 0) for t, _, _ in ctrl]} for k in keys}
    a1b21 = [s for s in surv if s["a"] == 1 and s["b"] == 21]
    return {
        "candidates": [],
        "bounds": {"family": "two-lag ciphertext feedback plus a periodic key", "lag_pairs": "1 <= a < b <= 74", "signs": 4,
                   "periods": f"1-{PMAX}", "classes": 16, "cases": cases, "complete": complete,
                   "controls": [{"cases": c2, "complete": comp2} for _, c2, comp2 in ctrl],
                   "survivors_by_checks": table, "survivors_2plus_checks": [s for s in surv if s["checks"] >= 2][:40],
                   "a1_b21_survivors": a1b21[:20]},
        "notes": f"{cases} cases ({'complete' if complete else 'stopped early'}). Survivors by checks, K4 (controls min-max): " + "; ".join(
            f"{k}: {v['k4']} ({min(v['controls']) if v['controls'] else '-'}-{max(v['controls']) if v['controls'] else '-'})" for k, v in table.items())
            + f". Lags 1 and 21: {len(a1b21)} survivors.",
    }


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    I = {c: i for i, c in enumerate(KRY)}
    ct, kn = ctx.K4, ctx.KNOWN
    lines = ["distances 1 and 21, both added, sculpture's alphabet throughout, Vigenere", "", "place  known  carved  1 back  21 back  constant"]
    for pos in (22, 23, 24, 25):
        k = (I[ct[pos - 1]] - I[kn[pos]] - I[ct[pos - 2]] - I[ct[pos - 22]]) % 26
        lines.append(f"{pos:>5}  {kn[pos]:>5}  {ct[pos - 1]:>6}  {ct[pos - 2]:>6}  {ct[pos - 22]:>7}  {KRY[k]:>8}")
    return "\n".join(lines)
