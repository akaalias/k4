"""Experiment 0059. See program.md for the contract."""

EXPERIMENT = {
    "slug": "two-keywords-two-passes-k1-k3-word-alphabets",
    "title": "Two secret words in two passes, on tables rebuilt from the solved messages' words",
    "family": "3-two-component-key",
    "parent": "0043-two-keywords-two-passes-mixed-alphabets",
    "changed": "Experiment 43 ran the exact two-word test on tables rebuilt from the puzzle's vocabulary. Here the tables come from every word of the three solved messages and of Sanborn's 2025 letter, with the same lengths and the same exact test.",
    "hypothesis_expert": (
        "Two periodic keys composed through two tableau passes, t[i] = x[i mod a] + s y[i mod b] mod 26 "
        "(0014, Scheidt's combined keys, family 3), with plain and cipher alphabets keyword-mixed from the "
        "K1-K3 plaintext words and the C13/C14 words (102 alphabets with standard and KRYPTOS), both "
        "plaintext signs, both combiner signs, every length pair a < b with a + b <= 24 and lcm outside the "
        "dead periods. Weighted union-find over the 24 crib equations; a + b - 1 unknowns leave 25 - a - b "
        "redundant checks. Survivors with at most three free components are enumerated and their words "
        "matched against the vocabulary, the word pool and K1-K3 windows. Bounds: complete for these "
        "alphabets and lengths."
    ),
    "hypothesis_eli5": (
        "Two short secret words used one after the other on the table act like one longer secret word "
        "with a pattern. Experiment 43 asked whether any two words could explain the 24 known letters on "
        "tables rebuilt from the puzzle's word list, and none could below a combined length of 22. Here the "
        "tables come from every word of the solved messages instead, and the question is asked again for "
        "every pair of lengths that leaves spare known letters to check."
    ),
    "prediction": (
        "No length pair with a + b below 21 survives under any alphabet pair; survivors at 21-24 appear at "
        "chance rates, none spelling a known word. Zero candidates."
    ),
    "method": (
        "1. Build the alphabet pool. 2. For each plain and cipher alphabet and sign, compute the forced total "
        "at each crib. 3. For each length pair and combiner sign, add the 24 difference constraints to a "
        "weighted union-find; reject on contradiction. 4. Count survivors by a + b. 5. Enumerate survivors "
        "with at most three components and match words."
    ),
    "walkthrough": (
        "1. Build the message alphabet from SHADING and the carved alphabet from INVISIBLE. 2. Lengths 7 and "
        "8, Vigenere both passes: place 22 needs a total key that sends E (9 in the first alphabet) to F (10 "
        "in the second): 1. 3. Place 22 uses slot 0 of the 7-letter word and slot 5 of the 8-letter word, so "
        "x0 + y5 = 1. 4. Place 29 uses slot 0 and slot 4: x0 + y4 equals its own total, so y5 - y4 is fixed. "
        "5. Walk all 24 places; every loop must close. 6. One contradiction kills this pair of lengths for "
        "this pair of alphabets."
    ),
}

from math import lcm
from itertools import product
from kryptos.alphabets import keyword_mixed
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY, load_k1, load_k2, load_k3

N = 97
DEAD_PERIODS = set(range(1, 27)) | set(range(30, 53))
MAXSUM = 24
MODES_KEY = {"vig": lambda p, c: (c - p) % 26, "beau": lambda p, c: (c + p) % 26}
MODES_DEC = {"vig": lambda c, k: (c - k) % 26, "beau": lambda c, k: (k - c) % 26}
MODES_ENC = {"vig": lambda p, k: (p + k) % 26, "beau": lambda p, k: (k - p) % 26}


def letters(s):
    return "".join(c for c in s if "A" <= c <= "Z")


SPACED = (
    "BETWEEN SUBTLE SHADING AND THE ABSENCE OF LIGHT LIES THE NUANCE OF IQLUSION "
    "IT WAS TOTALLY INVISIBLE HOWS THAT POSSIBLE THEY USED THE EARTHS MAGNETIC FIELD X THE INFORMATION WAS GATHERED AND "
    "TRANSMITTED UNDERGRUUND TO AN UNKNOWN LOCATION X DOES LANGLEY KNOW ABOUT THIS THEY SHOULD ITS BURIED OUT THERE "
    "SOMEWHERE X WHO KNOWS THE EXACT LOCATION ONLY WW THIS WAS HIS LAST MESSAGE X THIRTY EIGHT DEGREES FIFTY SEVEN "
    "MINUTES SIX POINT FIVE SECONDS NORTH SEVENTY SEVEN DEGREES EIGHT MINUTES FORTY FOUR SECONDS WEST ID BY ROWS "
    "SLOWLY DESPARATLY SLOWLY THE REMAINS OF PASSAGE DEBRIS THAT ENCUMBERED THE LOWER PART OF THE DOORWAY WAS REMOVED "
    "WITH TREMBLING HANDS I MADE A TINY BREACH IN THE UPPER LEFT HAND CORNER AND THEN WIDENING THE HOLE A LITTLE I "
    "INSERTED THE CANDLE AND PEERED IN THE HOT AIR ESCAPING FROM THE CHAMBER CAUSED THE FLAME TO FLICKER BUT PRESENTLY "
    "DETAILS OF THE ROOM WITHIN EMERGED FROM THE MIST X CAN YOU SEE ANYTHING Q"
)
EXTRA = ["EGYPT", "CAIRO", "LUXOR", "WALL", "NOVEMBER", "MESSAGE", "DELIVER", "DELIVERING", "TRANSMIT"]


def pool_of(vocab):
    words = sorted({w for w in SPACED.split() if len(set(w)) >= 3} | set(EXTRA))
    seen = {STD, KRY} | {keyword_mixed(w) for w in vocab if len(set(w)) >= 3}
    pool = {"std": STD, "kry": KRY}
    for w in words:
        A = keyword_mixed(w)
        if A not in seen:
            seen.add(A); pool[f"{w}/keyword"] = A
    return pool


def encrypt(plaintext, key):
    pa, ca, m, X, Y, s = key["pa"], key["ca"], key["m"], key["X"], key["Y"], key["s"]   # X, Y as index lists
    f = MODES_ENC[m]
    return "".join(ca[f(pa.index(p), (X[i % len(X)] + s * Y[i % len(Y)]) % 26)] for i, p in enumerate(plaintext))


class WUF:
    def __init__(self, n):
        self.p = list(range(n)); self.w = [0] * n
    def find(self, x):
        if self.p[x] == x: return x, 0
        r, wr = self.find(self.p[x]); self.w[x] = (self.w[x] + wr) % 26; self.p[x] = r
        return r, self.w[x]
    def union(self, x, y, d):
        rx, wx = self.find(x); ry, wy = self.find(y)
        if rx == ry: return (wx - wy) % 26 == d % 26
        self.p[rx] = ry; self.w[rx] = (d - wx + wy) % 26
        return True


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    vocab = set(ctx.vocabulary) | {w for w in SPACED.split() if len(w) >= 2} | set(EXTRA)
    pool = pool_of(set(ctx.vocabulary))
    index = {n: {ch: i for i, ch in enumerate(A)} for n, A in pool.items()}
    texts = [letters(load_k1()["plaintext"]), letters(load_k2()["plaintext_as_carved"]), letters(load_k3()["plaintext"])]
    crib = sorted(known.items())
    pairs = [(a, b) for a in range(2, MAXSUM) for b in range(a + 1, MAXSUM) if a + b <= MAXSUM and lcm(a, b) not in DEAD_PERIODS]
    pool_cache = {}

    def wordpool(L):
        if L not in pool_cache:
            s_ = {w for w in vocab if len(w) == L}
            for t in texts:
                for i in range(0, len(t) - L + 1):
                    s_.add(t[i:i + L])
            pool_cache[L] = s_
        return pool_cache[L]

    survivors, candidates = [], []
    cases = 0
    for pname, pa in pool.items():
        pidx = index[pname]
        for cname, ca in pool.items():
            cidx = index[cname]
            for m, f in MODES_KEY.items():
                t = [f(pidx[p], cidx[ct[pos - 1]]) for pos, p in crib]
                for a, b in pairs:
                    for s in (1, -1):
                        cases += 1
                        uf = WUF(a + b); ok = True
                        for (pos, _), tv in zip(crib, t):
                            i = pos - 1
                            if not uf.union(i % a, a + (i % b), tv):
                                ok = False; break
                        if not ok:
                            continue
                        roots = sorted({uf.find(n)[0] for n in range(a + b)})
                        survivors.append((a + b, a, b, pname, cname, m, s, len(roots)))
                        if len(roots) > 3:
                            continue
                        for vals in product(range(26), repeat=len(roots)):
                            v = dict(zip(roots, vals))
                            xs = [(uf.find(n)[1] + v[uf.find(n)[0]]) % 26 for n in range(a)]
                            ys = [(-s * (uf.find(n)[1] + v[uf.find(n)[0]])) % 26 for n in range(a, a + b)]
                            for ka_name in ("std", "kry"):
                                A = pool[ka_name]
                                X = "".join(A[x] for x in xs); Y = "".join(A[y] for y in ys)
                                if X in wordpool(a) or Y in wordpool(b):
                                    key = {"pa": pa, "ca": ca, "m": m, "X": xs, "Y": ys, "s": s}
                                    pt = "".join(pa[MODES_DEC[m](cidx[c], (xs[i % a] + s * ys[i % b]) % 26)] for i, c in enumerate(ct))
                                    candidates.append({"plaintext": pt, "key": key, "key_bits": 4.7 * (a + b), "key_description": f"X={X} Y={Y} ({a},{b}) plain {pname} cipher {cname} {m} s={s}"})
            if ctx.time_left() < 60:
                break
        if ctx.time_left() < 60:
            break
    by_sum = {}
    for r in survivors:
        by_sum[r[0]] = by_sum.get(r[0], 0) + 1
    return {
        "candidates": candidates[:50],
        "bounds": {"family": "two periodic keys composed through two tableau passes, alphabets from K1-K3 words and C13/C14 words", "alphabets": len(pool), "length_pairs": len(pairs),
                   "cases": cases, "survivors": len(survivors), "survivors_by_a_plus_b": {str(k): v for k, v in sorted(by_sum.items())},
                   "smallest_surviving_sum": min(by_sum) if by_sum else None,
                   "smallest_survivors": [{"a": a, "b": b, "plain": p, "cipher": c, "mode": m, "s": s, "components": k} for _, a, b, p, c, m, s, k in sorted(survivors)[:12]],
                   "vocab_matches": len(candidates)},
        "notes": f"{cases} cases; {len(survivors)} consistent; smallest surviving a + b {min(by_sum) if by_sum else None}; survivors by sum {dict(sorted(by_sum.items()))}; {len(candidates)} word matches.",
    }


def worked_example(ctx, key):
    pa, ca = keyword_mixed("SHADING"), keyword_mixed("INVISIBLE")
    lines = [f"plain {pa}", f"cipher {ca}", "", "lengths 7 and 8, Vigenere: totals and slots", "", "pos  plain  carved  total  x slot  y slot"]
    for pos in (22, 23, 29, 30, 64):
        p, c = ctx.KNOWN[pos], ctx.K4[pos - 1]
        lines.append(f"{pos:>3}    {p}      {c}      {(ca.index(c) - pa.index(p)) % 26:>2}      {(pos-1) % 7}       {(pos-1) % 8}")
    return "\n".join(lines)
