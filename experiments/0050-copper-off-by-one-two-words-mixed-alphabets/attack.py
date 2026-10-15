"""Experiment 0050. See program.md for the contract."""

EXPERIMENT = {
    "slug": "copper-off-by-one-two-words-mixed-alphabets",
    "title": "The copper off by one letter, through the two-word test on tables rebuilt from the puzzle's words",
    "family": "3-two-component-key",
    "parent": "0043-two-keywords-two-passes-mixed-alphabets",
    "changed": "Experiment 43 ran the exact two-word test on the carved text under 63 x 63 vocabulary alphabets and found nothing below a total length of 22. Experiment 31 ran the same test with one carved letter deleted or one unknown inserted anywhere, but only under the standard and KRYPTOS orders. Here the two parameters are combined: every one-letter variant of the copper, every vocabulary alphabet pair, total length up to 22, with a shuffled copper run through the same sweep as the control.",
    "hypothesis_expert": (
        "K2 carries a known carving error (C14), so the K4 copper may be off by one letter, which shifts "
        "every later crib against a periodic key. The two-word composition t[i] = x[i mod a] + s y[i mod b] "
        "mod 26 (0014) is exact: 24 crib equations in a + b - 1 unknowns, so each (a, b) has 25 - a - b "
        "redundant checks at 1/26 each. Variants: the carved text, a letter deleted at each of 97 places, an "
        "unknown inserted before each of 98 places; variants that touch no crib collapse to the carved case, "
        "leaving about 50 distinct crib tuples, since every slip before the first crib shifts the cribs the same way. Under 63 x 63 keyword-mixed plain and cipher alphabets, "
        "both modes, both signs, length pairs with a < b, a + b <= 22 and lcm outside the dead periods: "
        "about 22 million union-find cases. Chance survival at a + b = 22 is 26^-3 per case, so a couple "
        "of hundred chance survivors at 22, a handful at 21, at most one at 20 and none below. A shuffled copper "
        "through the same sweep gives the control counts. Survivors with at most three free components "
        "are enumerated and their words matched against the vocabulary and K1-K3 windows. Bounds: complete "
        "for one error anywhere, these alphabets and these lengths."
    ),
    "hypothesis_eli5": (
        "The second message on the sculpture has a carving mistake, so the fourth might too: one letter "
        "missing or one letter too many. That would throw off every test that counts positions. Experiment "
        "31 tried every such slip on the sculpture's own table; experiment 43 tried two secret words on "
        "tables rebuilt from the puzzle's words but with the copper taken as exact. Here both are allowed at "
        "once. A scrambled copy of the copper gets the same treatment so we know what luck alone produces."
    ),
    "prediction": (
        "No variant survives with a + b at or below 19 under any alphabet pair. Survivors at 20 to 22 "
        "appear in the same numbers on the copper and on its shuffle, and none yields a word from the "
        "vocabulary or K1-K3. Zero candidates pass."
    ),
    "method": (
        "1. Build the variants and group them by the crib tuple they produce. 2. Build the alphabet pool. "
        "3. For each distinct crib tuple, alphabet pair, mode, length pair and sign, add the crib equations "
        "to a weighted union-find; reject on contradiction. 4. Count survivors by a + b and by variant. "
        "5. Enumerate survivors with at most three components and match the words. 6. Repeat on a shuffled "
        "copper with the same variants as the control."
    ),
    "walkthrough": (
        "1. Suppose the carved letter at place 41 is spurious: delete it, so the copper letter under "
        "plaintext place 64 (B of BERLIN) is now the one carved at 65. 2. Rebuild the message alphabet "
        "from PALIMPSEST and the carved alphabet from ABSCISSA. 3. Lengths 7 and 8, Vigenere both passes: "
        "place 22 still needs the total that sends E to F, 5; place 64 now needs the total that sends B "
        "to the letter carved at 65. 4. Slots: place 22 uses slot 0 of the 7-word and slot 5 of the "
        "8-word; place 29 uses slots 0 and 4; subtract and y5 - y4 is fixed. 5. Walk all 24 places; one "
        "loop that fails to close kills this variant, pair of lengths and pair of alphabets. 6. Do the "
        "same for every deletion, every insertion, every alphabet pair and every pair of lengths."
    ),
}

import random
from math import lcm
from itertools import product
from kryptos.alphabets import keyword_mixed
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY, load_k1, load_k2, load_k3

DEAD_PERIODS = set(range(1, 27)) | set(range(30, 53))
MAXSUM = 22
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


def variants(ct):
    yield "carved", ct
    for i in range(len(ct)):
        yield f"deleted {i+1}", ct[:i] + ct[i + 1:]
    for i in range(len(ct) + 1):
        yield f"inserted before {i+1}", ct[:i] + "-" + ct[i:]


def crib_tuples(ct, known):
    """Distinct (plaintext position, carved letter) tuples over the variants, with the variant names."""
    groups = {}
    for name, v in variants(ct):
        t = tuple((pos, v[pos - 1]) for pos, p in sorted(known.items()) if pos - 1 < len(v) and v[pos - 1] != "-")
        groups.setdefault(t, []).append(name)
    return groups


def encrypt(plaintext, key):
    pa, ca, m, X, Y, s = key["pa"], key["ca"], key["m"], key["X"], key["Y"], key["s"]
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


def sweep(ct, known, pool, pairs, ctx, deadline_frac, label):
    groups = crib_tuples(ct, known)
    index = {n: {ch: i for i, ch in enumerate(A)} for n, A in pool.items()}
    survivors, cases = [], 0
    stopped = False
    for t, names in groups.items():
        cribs = [(pos, known[pos], c) for pos, c in t]
        for pname, pa in pool.items():
            pidx = index[pname]
            for cname, ca in pool.items():
                cidx = index[cname]
                for m, f in MODES_KEY.items():
                    tv = [(pos - 1, f(pidx[p], cidx[c])) for pos, p, c in cribs]
                    for a, b in pairs:
                        for s in (1, -1):
                            cases += 1
                            uf = WUF(a + b); ok = True
                            for i, v in tv:
                                if not uf.union(i % a, a + (i % b), v):
                                    ok = False; break
                            if ok:
                                roots = sorted({uf.find(n)[0] for n in range(a + b)})
                                survivors.append({"sum": a + b, "a": a, "b": b, "plain": pname, "cipher": cname, "mode": m, "s": s,
                                                  "components": len(roots), "variants": names, "uf": uf, "roots": roots, "cribs": len(cribs)})
            if ctx.time_left() < deadline_frac:
                stopped = True; break
        if stopped:
            break
    return groups, survivors, cases, stopped


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    vocab = set(ctx.vocabulary)
    pool = pool_of(vocab)
    texts = [letters(load_k1()["plaintext"]), letters(load_k2()["plaintext_as_carved"]), letters(load_k3()["plaintext"])]
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

    total = ctx.time_left()
    groups, survivors, cases, stopped = sweep(ct, known, pool, pairs, ctx, total * 0.45, "copper")
    candidates = []
    for r in survivors:
        if r["components"] > 3:
            continue
        uf, roots, a, b, s = r["uf"], r["roots"], r["a"], r["b"], r["s"]
        pa, ca = pool[r["plain"]], pool[r["cipher"]]
        cidx = {ch: i for i, ch in enumerate(ca)}
        for vals in product(range(26), repeat=len(roots)):
            v = dict(zip(roots, vals))
            xs = [(uf.find(n)[1] + v[uf.find(n)[0]]) % 26 for n in range(a)]
            ys = [(-s * (uf.find(n)[1] + v[uf.find(n)[0]])) % 26 for n in range(a, a + b)]
            for ka_name in ("std", "kry"):
                A = pool[ka_name]
                X = "".join(A[x] for x in xs); Y = "".join(A[y] for y in ys)
                if X in wordpool(a) or Y in wordpool(b):
                    vname = r["variants"][0]
                    vct = dict(variants(ct))[vname]
                    pt = "".join(pa[MODES_DEC[r["mode"]](cidx[c], (xs[i % a] + s * ys[i % b]) % 26)] if c != "-" else "?" for i, c in enumerate(vct))
                    candidates.append({"plaintext": pt, "key": {"pa": pa, "ca": ca, "m": r["mode"], "X": xs, "Y": ys, "s": s}, "key_bits": 4.7 * (a + b),
                                       "key_description": f"X={X} Y={Y} ({a},{b}) plain {r['plain']} cipher {r['cipher']} {r['mode']} s={s}; copper {vname}"})
    for r in survivors:
        r.pop("uf"); r.pop("roots")
    by_sum = {}
    for r in survivors:
        by_sum[r["sum"]] = by_sum.get(r["sum"], 0) + 1
    # control: the carved letters shuffled, same variants, same sweep
    rng = random.Random(50)
    sh = list(ct); rng.shuffle(sh); sh = "".join(sh)
    c_groups, c_surv, c_cases, c_stopped = sweep(sh, known, pool, pairs, ctx, 45, "shuffled")
    c_by_sum = {}
    for r in c_surv:
        c_by_sum[r["sum"]] = c_by_sum.get(r["sum"], 0) + 1
    smallest = sorted(survivors, key=lambda r: (r["sum"], r["components"]))[:12]
    return {
        "candidates": candidates[:50],
        "bounds": {"family": "one-letter error (insert or delete anywhere) x two words a + b <= 22 x keyword-mixed alphabet pairs",
                   "variants": 1 + 97 + 98, "distinct_crib_tuples": len(groups), "alphabets": len(pool), "length_pairs": len(pairs),
                   "cases": cases, "stopped_early": stopped, "survivors": len(survivors),
                   "survivors_by_a_plus_b": {str(k): v for k, v in sorted(by_sum.items())},
                   "smallest_surviving_sum": min(by_sum) if by_sum else None,
                   "smallest_survivors": [{k: v for k, v in r.items() if k != "variants"} | {"variant": r["variants"][0]} for r in smallest],
                   "control": {"cases": c_cases, "stopped_early": c_stopped, "survivors": len(c_surv),
                               "survivors_by_a_plus_b": {str(k): v for k, v in sorted(c_by_sum.items())},
                               "smallest_surviving_sum": min(c_by_sum) if c_by_sum else None},
                   "vocab_matches": len(candidates)},
        "notes": (f"{len(groups)} distinct crib tuples from 196 variants; {cases} cases{' (stopped early)' if stopped else ''}; {len(survivors)} consistent, "
                  f"by sum {dict(sorted(by_sum.items()))}; shuffled copper: {c_cases} cases, {len(c_surv)} consistent, by sum {dict(sorted(c_by_sum.items()))}; "
                  f"{len(candidates)} word matches."),
    }


def worked_example(ctx, key):
    ct = ctx.K4
    v = ct[:40] + ct[41:]
    pa, ca = keyword_mixed("PALIMPSEST"), keyword_mixed("ABSCISSA")
    lines = ["variant: the carved letter at 41 deleted", f"plain {pa}", f"cipher {ca}", "", "lengths 7 and 8, Vigenere: totals and slots", "", "pos  plain  carved  total  x slot  y slot"]
    for pos in (22, 23, 29, 30, 64, 65):
        p, c = ctx.KNOWN[pos], v[pos - 1]
        lines.append(f"{pos:>3}    {p}      {c}      {(ca.index(c) - pa.index(p)) % 26:>2}      {(pos-1) % 7}       {(pos-1) % 8}")
    lines.append("")
    lines.append("places 64 and later now read the letter carved one place further along")
    return "\n".join(lines)
