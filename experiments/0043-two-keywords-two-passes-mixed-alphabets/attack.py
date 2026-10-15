"""Experiment 0043. See program.md for the contract."""

EXPERIMENT = {
    "slug": "two-keywords-two-passes-mixed-alphabets",
    "title": "Two key words in two passes, on tables rebuilt from the puzzle's words",
    "family": "3-two-component-key",
    "parent": "0014-two-keywords-two-passes-linear",
    "changed": "Experiment 14's exact linear test, with the plain and cipher alphabets drawn from the keyword mixings of every vocabulary word instead of the standard and KRYPTOS orders. Word lengths with a + b up to 24, where the 24 cribs leave at least one redundant check.",
    "hypothesis_expert": (
        "Two passes through the same tableau compose to t[i] = x[i mod a] + s y[i mod b] mod 26 (0014). "
        "Under keyword-mixed plain and cipher alphabets (C5, C29) the forced totals t change, so the "
        "weighted union-find test is rerun over 63 x 63 alphabet pairs, both plaintext signs, both s, and "
        "every length pair with a < b, a + b <= 24 and lcm outside the dead periods. With a + b - 1 "
        "effective unknowns and 24 equations, each case has 25 - a - b redundant checks at 1/26 each; "
        "chance survival per case is below 1/26 and the number of cases is about a million, so a few "
        "thousand chance survivors at a + b = 23 and 24 are expected and none below 20. Survivors are "
        "enumerated and X, Y matched against the vocabulary and K1-K3 windows under both key alphabets. "
        "Bounds: complete for these alphabets and lengths."
    ),
    "hypothesis_eli5": (
        "Experiment 14 asked whether two short secret words, used one after the other on the sculpture's "
        "table, could explain the 24 known letters; none could. The table could have been built from a "
        "different word, which changes every sum, so we rebuild it from each word the puzzle knows and ask "
        "again. Because two words of total length up to 24 leave spare known letters to check against, "
        "every pair of lengths gets a yes or no."
    ),
    "prediction": (
        "No length pair with a + b below 20 survives under any alphabet pair. Survivors at 20 to 24 appear "
        "at chance rates, and none yields a word from the vocabulary or K1-K3. Zero candidates pass."
    ),
    "method": (
        "1. Build the alphabet pool. 2. For each plain and cipher alphabet and plaintext sign, compute the "
        "forced total at each crib. 3. For each length pair and combiner sign, add the 24 difference "
        "constraints to a weighted union-find; reject on contradiction. 4. Count survivors by a + b. "
        "5. Enumerate survivors with at most three components; match X and Y against the vocabulary and "
        "K1-K3 windows; decrypt and submit matches."
    ),
    "walkthrough": (
        "1. Build the alphabet from PALIMPSEST for the message and from ABSCISSA for the carved letters. "
        "2. Lengths 7 and 8, Vigenere both passes: position 22 needs a total key index that sends E, index 6 "
        "in the PALIMPSEST alphabet, to F, index 11 in the ABSCISSA alphabet: 5. 3. Position 22 uses slot 0 "
        "of the 7-letter word and slot 5 of the 8-letter word, so x0 + y5 = 5. 4. Position 29 uses slot 0 "
        "and slot 4: x0 + y4 equals its own total. 5. Subtracting fixes y5 - y4; walk all 24 positions and "
        "every loop must close. 6. A contradiction kills this pair of lengths for this pair of alphabets."
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


def pool_of(vocab):
    pool = {"std": STD, "kry": KRY}
    for w in vocab:
        if len(set(w)) >= 3:
            pool[f"{w}/keyword"] = keyword_mixed(w)
    seen, out = {}, {}
    for name, A in pool.items():
        if A not in seen:
            seen[A] = name; out[name] = A
    return out


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
    vocab = set(ctx.vocabulary)
    pool = pool_of(vocab)
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
        "bounds": {"family": "two periodic keys composed through two tableau passes, keyword-mixed alphabets", "alphabets": len(pool), "length_pairs": len(pairs),
                   "cases": cases, "survivors": len(survivors), "survivors_by_a_plus_b": {str(k): v for k, v in sorted(by_sum.items())},
                   "smallest_surviving_sum": min(by_sum) if by_sum else None,
                   "smallest_survivors": [{"a": a, "b": b, "plain": p, "cipher": c, "mode": m, "s": s, "components": k} for _, a, b, p, c, m, s, k in sorted(survivors)[:12]],
                   "vocab_matches": len(candidates)},
        "notes": f"{cases} cases; {len(survivors)} consistent; smallest surviving a + b {min(by_sum) if by_sum else None}; survivors by sum {dict(sorted(by_sum.items()))}; {len(candidates)} word matches.",
    }


def worked_example(ctx, key):
    pa, ca = keyword_mixed("PALIMPSEST"), keyword_mixed("ABSCISSA")
    lines = [f"plain {pa}", f"cipher {ca}", "", "lengths 7 and 8, Vigenere: totals and slots", "", "pos  plain  carved  total  x slot  y slot"]
    for pos in (22, 23, 29, 30, 64):
        p, c = ctx.KNOWN[pos], ctx.K4[pos - 1]
        lines.append(f"{pos:>3}    {p}      {c}      {(ca.index(c) - pa.index(p)) % 26:>2}      {(pos-1) % 7}       {(pos-1) % 8}")
    return "\n".join(lines)
