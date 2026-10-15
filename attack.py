"""Experiment 0022. See program.md for the contract."""

EXPERIMENT = {
    "slug": "porta-halves-and-period-sweep",
    "title": "Porta: the reciprocal half-alphabet tableau, which the 24 conventions never covered",
    "family": "1-keyed-periodic",
    "parent": "0020-short-periods-mixed-alphabets-consistency",
    "changed": "A different tableau. Porta splits the alphabet into two halves and always sends a letter to the other half; the key letter chooses one of 13 reciprocal alphabets. Tested with the alphabet in standard, KRYPTOS and every vocabulary-mixed order.",
    "hypothesis_expert": (
        "Porta (1563; in Friedman and Hitt, so in what Scheidt taught, C5) is reciprocal: with the alphabet "
        "A split into halves H1 and H2, key letter k selects j = index(k) div 2, and p in H1 at index i goes to "
        "H2[(i + j) mod 13], p in H2 at index i goes to H1[(i - j) mod 13]. Our 24 conventions are Vigenere, "
        "Beaufort and variant Beaufort over full alphabets and do not contain it. Two tests. First the "
        "halves: every crib plaintext letter must sit in the opposite half from its ciphertext letter; under "
        "the standard order E and F are both in A-M, so standard Porta dies at position 22 at once, and each "
        "of the 248 vocabulary-mixed orders passes with chance 2 to the minus 24. Second, for any order that "
        "passes, the forced j at each crib position gives a period sweep 1-52 by the divisor rule, with the "
        "forced key fragment matched against the vocabulary. Both the ACA direction and its mirror are "
        "tried. Bounds: complete for Porta over this alphabet pool."
    ),
    "hypothesis_eli5": (
        "Porta is an old cipher that cuts the alphabet in two halves and always swaps a letter into the "
        "other half: a letter from the first half always lands in the second, and back. That gives a quick "
        "check: every known letter must have been swapped across the halves. With the ordinary alphabet, E "
        "and its carved partner F are both in the first half, so Porta fails at the very first known letter. "
        "But if the alphabet was first reordered by a secret word, the halves change, so we try every "
        "reordering the puzzle's words allow."
    ),
    "prediction": (
        "No alphabet order passes the halves test for all 24 cribs; the best passes about 18 of 24. So no "
        "period sweep runs and zero candidates pass."
    ),
    "method": (
        "1. Build the alphabet pool. 2. For each order, split into halves and count crib positions whose "
        "plaintext and ciphertext letters are in the same half. 3. For any order with zero such positions, "
        "derive the forced alphabet number j at each crib and sweep periods 1-52 by the divisor rule in "
        "both directions. 4. Match forced fragments against the vocabulary; decrypt and submit matches."
    ),
    "walkthrough": (
        "1. Write the alphabet in two rows: A to M above, N to Z below. 2. Position 22 is plaintext E and "
        "carved F; both are in the top row. 3. In Porta a top-row letter always becomes a bottom-row letter, "
        "so this cannot be Porta on the plain alphabet. 4. Now reorder the alphabet by a word, say "
        "PALIMPSEST: PALIMSETBCDFG above, HJKNOQRUVWXYZ below. 5. E and F are again both above: dead. "
        "6. Try every reordering the puzzle's words give; a reordering that separates all 24 pairs would "
        "then get its key letters worked out one position at a time."
    ),
}

from kryptos.alphabets import keyword_mixed, columnar_mixed, keyed_columnar_mixed, alternate_vertical_mixed
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY, load_k1, load_k2, load_k3

N = 97
MIX = {"keyword": keyword_mixed, "columnar": columnar_mixed, "keyed_columnar": keyed_columnar_mixed, "alt_vertical": alternate_vertical_mixed}
DIVISORS = {d: [k for k in range(1, d + 1) if d % k == 0 and k <= 52] for d in range(1, N + 1)}


def letters(s):
    return "".join(c for c in s if "A" <= c <= "Z")


def pool_of(vocab):
    pool = {"std": STD, "kry": KRY}
    for w in vocab:
        if len(set(w)) >= 3:
            for mname, fn in MIX.items():
                pool[f"{w}/{mname}"] = fn(w)
    seen, out = {}, {}
    for name, A in pool.items():
        if A not in seen:
            seen[A] = name; out[name] = A
    return out


def porta_letter(p, j, A, mirror=False):
    h1, h2 = A[:13], A[13:]
    if p in h1:
        i = h1.index(p)
        return h2[(i - j) % 13] if mirror else h2[(i + j) % 13]
    i = h2.index(p)
    return h1[(i + j) % 13] if mirror else h1[(i - j) % 13]


def forced_j(p, c, A, mirror=False):
    """The alphabet number j (0-12) that sends p to c, or None if p and c share a half."""
    h1, h2 = A[:13], A[13:]
    if p in h1 and c in h2:
        return ((h2.index(c) - h1.index(p)) * (-1 if mirror else 1)) % 13
    if p in h2 and c in h1:
        return ((h2.index(p) - h1.index(c)) * (-1 if mirror else 1)) % 13
    return None


def encrypt(plaintext, key):
    A, k, mirror = key["alphabet"], key["key"], key["mirror"]
    return "".join(porta_letter(p, A.index(k[i % len(k)]) // 2, A, mirror) for i, p in enumerate(plaintext))


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    vocab = list(ctx.vocabulary)
    pool = pool_of(vocab)
    texts = [letters(load_k1()["plaintext"]), letters(load_k2()["plaintext_as_carved"]), letters(load_k3()["plaintext"])]
    crib_pos = sorted(known)
    halves = []
    passing = []
    for name, A in pool.items():
        h1 = set(A[:13])
        same = sum(1 for pos in crib_pos if (known[pos] in h1) == (ct[pos - 1] in h1))
        halves.append((same, name))
        if same == 0:
            passing.append(name)
    halves.sort()
    survivors, candidates = [], []
    for name in passing:
        A = pool[name]
        for mirror in (False, True):
            forced = [(pos - 1, forced_j(known[pos], ct[pos - 1], A, mirror)) for pos in crib_pos]
            dead = set()
            for x in range(24):
                for y in range(x + 1, 24):
                    if forced[x][1] != forced[y][1]:
                        dead.update(DIVISORS[abs(forced[x][0] - forced[y][0])])
            for P in range(1, 53):
                if P in dead:
                    continue
                slots = {i % P: j for i, j in forced}
                survivors.append({"alphabet": name, "mirror": mirror, "period": P})
                if P <= 30:
                    wordpool = set(w for w in vocab if len(w) == P)
                    for t in texts:
                        for i in range(0, len(t) - P + 1):
                            wordpool.add(t[i:i + P])
                    for kw in wordpool:
                        if all(A.index(kw[s]) // 2 == j for s, j in slots.items()):
                            key = {"alphabet": A, "key": kw, "mirror": mirror}
                            pt = encrypt(ct, key)   # Porta is reciprocal: decrypting is encrypting again
                            candidates.append({"plaintext": pt, "key": key, "key_bits": 4.7 * P + 8, "key_description": f"Porta key {kw} on {name}{' mirrored' if mirror else ''}"})
    return {
        "candidates": candidates[:50],
        "bounds": {"family": "Porta over standard, KRYPTOS and vocabulary-mixed alphabet orders", "alphabets": len(pool),
                   "halves_test": "crib positions whose plaintext and ciphertext share a half; zero required",
                   "best_orders": [{"same_half_positions": a, "alphabet": b} for a, b in halves[:10]],
                   "orders_passing_halves": passing, "period_survivors": survivors[:40], "n_period_survivors": len(survivors),
                   "vocab_matches": len(candidates)},
        "notes": f"{len(pool)} alphabet orders; {len(passing)} pass the halves test (best has {halves[0][0]} same-half positions); {len(survivors)} (order, direction, period) survivors; {len(candidates)} matches.",
    }


def worked_example(ctx, key):
    lines = ["halves test on the standard order: A-M above, N-Z below", "", "pos  plain  half   carved  half   swapped across?"]
    h1 = set(STD[:13])
    for pos in (22, 23, 24, 25, 26, 64, 65, 66):
        p, c = ctx.KNOWN[pos], ctx.K4[pos - 1]
        lines.append(f"{pos:>3}    {p}    {'top' if p in h1 else 'bottom':<6}   {c}    {'top' if c in h1 else 'bottom':<6}   {'yes' if (p in h1) != (c in h1) else 'NO'}")
    return "\n".join(lines)
