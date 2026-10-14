"""Experiment 0014. See program.md for the contract."""

EXPERIMENT = {
    "slug": "two-keywords-two-passes-linear",
    "title": "Two key words, two passes through the tableau: the cribs as linear equations mod 26",
    "family": "3-two-component-key",
    "parent": None,
    "changed": "New root in family 3. The key is the sum of two short repeating keys, one per pass, so the 24 cribs become linear equations in a + b unknowns and consistency is decided exactly.",
    "hypothesis_expert": (
        "Scheidt's habit of combining two key components (knowledge/people/scheidt.md, C6) and Sanborn's "
        "'double' (C1 reading c, composed tableau passes) suggest two keywords X and Y applied in two "
        "passes. Two passes through the same tableau compose to one periodic key t[i] = x[i mod a] + s y[i mod b] "
        "mod 26 with s = +1 or -1 depending on the modes, of period lcm(a, b). 0005 excluded periods 1-26 and "
        "30-52, so only pairs with lcm in {27, 28, 29} or 53 and above remain; within them the question is "
        "whether the forced total key factors into two short words. For each pair 2 <= a < b <= 30, each "
        "plain and cipher alphabet in {standard, KRYPTOS}, each sign of the plaintext (Vigenere-like or "
        "Beaufort-like) and each s, the 24 forced values give 24 equations x_u - y'_v = t over Z26, checked "
        "by a weighted union-find; with a + b - 1 effective unknowns there are 25 - a - b redundant checks, "
        "each passing by chance with probability 1/26. Survivors are enumerated (26 to the power of the "
        "number of components) and X, Y matched against the vocabulary and K1-K3 windows under both key "
        "alphabets and both signs; matches are decrypted and submitted. Bounds: complete for two-pass "
        "periodic keys with lengths 2-30 under the standard and KRYPTOS alphabets."
    ),
    "hypothesis_eli5": (
        "Suppose the artist ran the message through the sculpture's table twice, with a different secret "
        "word each time. Two pushes along the alphabet add up to one push, so the two words act like one "
        "long key made by adding them letter by letter. The 24 known letters give 24 facts about that sum. "
        "If the two words are short, say 7 and 8 letters, 24 facts are more than enough to tell whether "
        "any pair of words can produce them, and if so, what the words are. We check every pair of "
        "lengths and read off the words where the facts agree."
    ),
    "prediction": (
        "Length pairs with a + b above about 20 survive by chance under some settings, because they have "
        "few redundant checks. Pairs with a + b of 15 or less survive in at most a handful of settings. "
        "No surviving pair yields X or Y in the vocabulary or K1-K3 windows; zero candidates pass."
    ),
    "method": (
        "1. For each plain alphabet, cipher alphabet and plaintext sign, compute the forced total key value "
        "t at each crib position. 2. For each length pair (a, b) with lcm not in 1-26 or 30-52, and each "
        "sign s, build nodes for the a slots of X and the b slots of Y and add the edge x[i mod a] - s y[i mod b] = t[i] "
        "for each crib. 3. Reject on any inconsistent cycle. 4. Count components; enumerate the free values "
        "when there are at most three components. 5. Match X and Y against the vocabulary and K1-K3 windows "
        "under the standard and KRYPTOS key alphabets; decrypt and submit matches."
    ),
    "walkthrough": (
        "1. Take lengths 7 and 8 and the KRYPTOS alphabet for everything, Vigenere both passes. 2. Position 22 "
        "needs a total key letter that sends E to F: R, index 1. Position 22 uses slot 0 of the 7-letter word "
        "(21 mod 7) and slot 5 of the 8-letter word (21 mod 8), so x0 + y5 = 1. 3. Position 29 uses slot 0 "
        "again and slot 4: x0 + y4 = its forced value. 4. Subtract: y5 - y4 is now fixed. 5. Walk all 24 "
        "positions this way; every slot gets tied to the others through shared positions. 6. When a loop "
        "closes, the values must agree, or the pair 7 and 8 is dead. 7. If they all agree, pick x0 freely; "
        "every other letter follows. 8. Twenty-six choices of x0 give twenty-six word pairs; see whether "
        "either word is one the puzzle knows."
    ),
}

from math import lcm
from kryptos.alphabets import ALPHABETS, key_letter_for, encrypt_letter, decrypt_letter
from kryptos.facts import load_k1, load_k2, load_k3

N = 97
MAXLEN = 30
DEAD_PERIODS = set(range(1, 27)) | set(range(30, 53))


def letters(s):
    return "".join(c for c in s if "A" <= c <= "Z")


def encrypt(plaintext, key):
    pa, ca, ka, m1, m2, X, Y = key["pa"], key["ca"], key["ka"], key["m1"], key["m2"], key["X"], key["Y"]
    mid = "".join(encrypt_letter(p, X[i % len(X)], pa, ca, ka, m1) for i, p in enumerate(plaintext))
    # second pass reads the first pass's output on the cipher alphabet as its plaintext
    return "".join(encrypt_letter(c, Y[i % len(Y)], ca, ca, ka, m2) for i, c in enumerate(mid))


class WUF:
    """Weighted union-find over Z26: maintains v[node] - v[root] = w[node]."""
    def __init__(self, n):
        self.p = list(range(n)); self.w = [0] * n
    def find(self, x):
        if self.p[x] == x:
            return x, 0
        r, wr = self.find(self.p[x])
        self.w[x] = (self.w[x] + wr) % 26
        self.p[x] = r
        return r, self.w[x]
    def union(self, x, y, d):
        """Impose v[x] - v[y] = d. Returns False on contradiction."""
        rx, wx = self.find(x); ry, wy = self.find(y)
        if rx == ry:
            return (wx - wy) % 26 == d % 26
        # v[x] = wx + v[rx]; v[y] = wy + v[ry]; want v[x] - v[y] = d  =>  v[rx] - v[ry] = d - wx + wy
        self.p[rx] = ry; self.w[rx] = (d - wx + wy) % 26
        return True


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    vocab = set(ctx.vocabulary)
    texts = [letters(load_k1()["plaintext"]), letters(load_k2()["plaintext_as_carved"]), letters(load_k3()["plaintext"])]
    crib_pos = sorted(known)
    pairs = [(a, b) for a in range(2, MAXLEN + 1) for b in range(a + 1, MAXLEN + 1) if lcm(a, b) not in DEAD_PERIODS]
    survivors, candidates = [], []
    n_cases = 0
    pool_cache = {}

    def pool(L):
        if L not in pool_cache:
            s = {w for w in vocab if len(w) == L}
            for t in texts:
                for i in range(0, len(t) - L + 1):
                    s.add(t[i:i + L])
            pool_cache[L] = s
        return pool_cache[L]

    for pa in ("std", "kry"):
        for ca in ("std", "kry"):
            for psign in ("vig", "beau"):           # total key under Vigenere or Beaufort reading
                t = {pos: ALPHABETS["std"].index(key_letter_for(known[pos], ct[pos - 1], pa, ca, "std", psign)) for pos in crib_pos}
                for a, b in pairs:
                    for s in (1, -1):
                        n_cases += 1
                        uf = WUF(a + b)
                        ok = True
                        for pos in crib_pos:
                            i = pos - 1
                            # x[i%a] + s*y[i%b] = t  =>  x_u - y'_v = t with y' = -s*y
                            if not uf.union(i % a, a + (i % b), t[pos]):
                                ok = False; break
                        if not ok:
                            continue
                        roots = sorted({uf.find(n)[0] for n in range(a + b)})
                        comps = len(roots)
                        rec = {"a": a, "b": b, "pa": pa, "ca": ca, "plain_sign": psign, "s": s, "components": comps,
                               "redundant_checks": 24 - (a + b - comps)}
                        survivors.append(rec)
                        if comps > 3:
                            continue
                        # enumerate: value of each node = w[node] + v[root]
                        import itertools
                        for vals in itertools.product(range(26), repeat=comps):
                            v = dict(zip(roots, vals))
                            xs = [(uf.find(n)[1] + v[uf.find(n)[0]]) % 26 for n in range(a)]
                            ys = [(-s * (uf.find(n)[1] + v[uf.find(n)[0]])) % 26 for n in range(a, a + b)]
                            for ka in ("std", "kry"):
                                A = ALPHABETS[ka]
                                X = "".join(A[x] for x in xs); Y = "".join(A[y] for y in ys)
                                hitX, hitY = X in pool(a), Y in pool(b)
                                if hitX or hitY:
                                    STD = ALPHABETS["std"]
                                    total = [STD[(xs[i % a] + s * ys[i % b]) % 26] for i in range(N)]
                                    pt = "".join(decrypt_letter(ct[i], total[i], pa, ca, "std", psign) for i in range(N))
                                    candidates.append({"plaintext": pt, "key": {"pa": pa, "ca": ca, "ka": ka, "m1": psign, "m2": "vig" if s == 1 else "varbeau", "X": X, "Y": Y},
                                                       "key_bits": 4.7 * (a + b), "key_description": f"X={X} Y={Y} ({a},{b}) {pa}/{ca}/{ka} {psign}, s={s}; vocab hit {'X' if hitX else ''}{'Y' if hitY else ''}"})
        if ctx.time_left() < 20:
            break
    by_sum = {}
    for r in survivors:
        by_sum.setdefault(r["a"] + r["b"], 0); by_sum[r["a"] + r["b"]] += 1
    small = sorted([r for r in survivors if r["a"] + r["b"] <= 15], key=lambda r: (r["a"] + r["b"], r["a"]))
    return {
        "candidates": candidates[:50],
        "bounds": {"family": "two periodic keys composed through two tableau passes", "lengths": f"2 <= a < b <= {MAXLEN}, lcm outside 1-26 and 30-52",
                   "pairs": len(pairs), "alphabets": "plain and cipher in {std, kry}; key words read in std or kry", "cases": n_cases,
                   "survivors": len(survivors), "survivors_by_a_plus_b": {str(k): v for k, v in sorted(by_sum.items())},
                   "smallest_surviving_pairs": small[:20], "vocab_or_k1k3_matches": len(candidates)},
        "notes": f"{n_cases} cases; {len(survivors)} consistent; {len(candidates)} word matches submitted.",
    }


def worked_example(ctx, key):
    A = ALPHABETS["kry"]
    lines = ["lengths 7 and 8, KRYPTOS alphabet throughout, Vigenere both passes: equations from the first cribs", "",
             "pos  plain  cipher  total key  index  x slot (pos-1 mod 7)  y slot (pos-1 mod 8)"]
    for pos in (22, 23, 24, 29, 30, 64, 65):
        p, c = ctx.KNOWN[pos], ctx.K4[pos - 1]
        k = key_letter_for(p, c, "kry", "kry", "kry", "vig")
        lines.append(f"{pos:>3}    {p}      {c}        {k}        {A.index(k):>2}           {(pos-1)%7}                    {(pos-1)%8}")
    lines.append("")
    lines.append("positions 22 and 29 share x slot 0, so y5 - y4 equals the difference of their totals; the chain of such ties must close consistently.")
    return "\n".join(lines)
