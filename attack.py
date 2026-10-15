"""Experiment 0049. See program.md for the contract."""

EXPERIMENT = {
    "slug": "structured-long-keys-at-surviving-periods",
    "title": "Long keys with a shape: two puzzle words joined, a word and its mirror, a word doubled, at the periods the cribs allow",
    "family": "1-keyed-periodic",
    "parent": "0005-quagmire-period-sweep-forced-keys",
    "changed": "Experiment 5 matched the forced key fragments at periods 27 to 29 against single vocabulary words and K1-K3 windows. A 27 to 29 letter key is unlikely to be one word; here it is built from two: joined, joined with a separator letter, a word followed by its mirror, or a word doubled. The forced fragments are matched exactly under the standard, KRYPTOS and vocabulary-mixed alphabets.",
    "hypothesis_expert": (
        "Periods 27-29 survive the crib sweep under every alphabet pair (0005, 0020), and their forced key "
        "fragments read as noise (0009, 0010), which rules out an English phrase as key but not a key made of "
        "two puzzle words with no English transition, or a word and its reverse (Sanborn's mirrors, C3), or "
        "a doubled word. Key shapes: X+Y, X+c+Y for a separator letter c, X+reverse(X), X+X, X+reverse(Y), "
        "over the 62-word vocabulary and its K1-K3 windows, kept when the length is 27, 28 or 29. Under each "
        "plain-cipher alphabet pair (standard, KRYPTOS, 61 keyword mixings) and mode, the 24 forced key "
        "indices are compared with the key read in the standard, KRYPTOS or the plain alphabet; a match "
        "decrypts and submits. About 20,000 key shapes x 12,000 alphabet classes, exact. Bounds: complete for "
        "these shapes and alphabets."
    ),
    "hypothesis_eli5": (
        "A secret word of 27 to 29 letters is probably not one word. It could be two of the puzzle's words "
        "joined, a word followed by itself, or a word followed by its mirror image. Each such key fixes the "
        "24 letters that the known letters demand, so we simply build every key of that kind and check it "
        "against the 24 demands, on the sculpture's table and on tables rebuilt from the puzzle's words."
    ),
    "prediction": (
        "No shaped key of length 27 to 29 matches all 24 forced letters under any alphabet pair and mode. "
        "Zero candidates pass."
    ),
    "method": (
        "1. Build the shaped keys of length 27-29 from the vocabulary. 2. For each plain and cipher alphabet "
        "and mode, compute the 24 forced key indices and their slots at each period. 3. For each key, read "
        "it in each key alphabet as indices and compare at the forced slots; count mismatches. 4. Decrypt "
        "and submit exact matches; report the fewest mismatches."
    ),
    "walkthrough": (
        "1. Join BERLIN and ALEXANDERPLATZ: BERLINALEXANDERPLATZ is 20 letters, too short; join "
        "WILLIAMWEBSTER and PALIMPSEST: 24, too short; join TUTANKHAMUN and SHADOWFORCES: 23. 2. Keep the "
        "pairs that reach 27, 28 or 29 letters, such as DIGITALINTERPRETATION joined with EGYPT. 3. On the "
        "sculpture's table with Vigenere, position 22 forces key letter R at slot 21 of a 27-letter key; "
        "position 23 forces D at slot 22, and so on for all 24 known letters. 4. Compare the joined key's "
        "letters at those slots; one mismatch and the key is out. 5. Repeat for every pair, every mirror and "
        "every doubling, under every table."
    ),
}

from kryptos.alphabets import keyword_mixed
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY, load_k1, load_k2, load_k3

N = 97
PERIODS = (27, 28, 29)
MODES_KEY = {"vig": lambda p, c: (c - p) % 26, "beau": lambda p, c: (c + p) % 26, "varbeau": lambda p, c: (p - c) % 26}
MODES_DEC = {"vig": lambda c, k: (c - k) % 26, "beau": lambda c, k: (k - c) % 26, "varbeau": lambda c, k: (c + k) % 26}
MODES_ENC = {"vig": lambda p, k: (p + k) % 26, "beau": lambda p, k: (k - p) % 26, "varbeau": lambda p, k: (p - k) % 26}


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


def shaped_keys(vocab):
    words = sorted(set(w for w in vocab if 2 <= len(w) <= 27))
    keys = {}
    for x in words:
        for y in words:
            for shape, k in (("joined", x + y), ("mirror", x + y[::-1])):
                if len(k) in PERIODS:
                    keys.setdefault(k, f"{shape} {x}+{y}")
            for c in "XQ":
                k = x + c + y
                if len(k) in PERIODS:
                    keys.setdefault(k, f"joined with {c} {x}+{y}")
        for shape, k in (("doubled", x + x), ("own mirror", x + x[::-1])):
            if len(k) in PERIODS:
                keys.setdefault(k, f"{shape} {x}")
    return keys


def encrypt(plaintext, key):
    pa, ca, m, k = key["pa"], key["ca"], key["m"], key["key"]   # key as index list
    f = MODES_ENC[m]
    return "".join(ca[f(pa.index(p), k[i % len(k)])] for i, p in enumerate(plaintext))


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    vocab = list(ctx.vocabulary)
    pool = pool_of(vocab)
    keys = shaped_keys(vocab)
    crib = sorted(known.items())
    key_alphas = {"std": STD, "kry": KRY}
    # key indices under each key alphabet, grouped by length
    by_len = {P: [] for P in PERIODS}
    for k, desc in keys.items():
        by_len[len(k)].append((k, desc, {kn: [A.index(ch) for ch in k] for kn, A in key_alphas.items()}))
    best, candidates = [], []
    trials = 0
    for pname, pa in pool.items():
        pidx = {ch: i for i, ch in enumerate(pa)}
        for cname, ca in pool.items():
            cidx = {ch: i for i, ch in enumerate(ca)}
            for m, f in MODES_KEY.items():
                forced = [(pos - 1, f(pidx[p], cidx[ct[pos - 1]])) for pos, p in crib]
                for P in PERIODS:
                    slots = [(i % P, v) for i, v in forced]
                    for k, desc, idx_by in by_len[P]:
                        for kn in ("std", "kry", "plain"):
                            kidx = idx_by[kn] if kn in idx_by else [pidx[ch] for ch in k]
                            trials += 1
                            mism = sum(1 for s_, v in slots if kidx[s_] != v)
                            if mism <= 3 and (len(best) < 15 or mism < best[-1][0]):
                                best.append((mism, k, desc, pname, cname, kn, m)); best.sort(); best = best[:15]
                            if mism == 0:
                                fd = MODES_DEC[m]
                                pt = "".join(pa[fd(cidx[c], kidx[i % P])] for i, c in enumerate(ct))
                                candidates.append({"plaintext": pt, "key": {"pa": pa, "ca": ca, "m": m, "key": kidx}, "key_bits": 4.7 * 12,
                                                   "key_description": f"{desc} = {k}; plain {pname}, cipher {cname}, key on {kn}, {m}"})
            if ctx.time_left() < 60:
                break
        if ctx.time_left() < 60:
            break
    return {
        "candidates": candidates[:50],
        "bounds": {"family": "shaped keys of length 27-29 from the vocabulary, periodic tableau, vocabulary-mixed alphabets", "keys": len(keys),
                   "keys_by_length": {str(P): len(by_len[P]) for P in PERIODS}, "alphabets": len(pool), "trials": trials,
                   "fewest_mismatches": best[0][0] if best else "more than 3",
                   "nearest": [{"mismatches": a, "key": k, "shape": d, "plain": p, "cipher": c, "key_alphabet": kn, "mode": m} for a, k, d, p, c, kn, m in best],
                   "survivors": len(candidates)},
        "notes": f"{len(keys)} shaped keys x {len(pool)}^2 alphabet pairs x 3 modes x 3 key readings: {trials} trials; fewest mismatches {best[0][0] if best else 'more than 3'}; {len(candidates)} exact matches.",
    }


def worked_example(ctx, key):
    k = "DIGITALINTERPRETATION" + "EGYPT"
    lines = [f"key {k}, length {len(k)}: a 26-letter join falls short of 27, so it is not tried; take instead", ""]
    keys = shaped_keys(["KRYPTOS", "PALIMPSEST", "ABSCISSA", "WILLIAMWEBSTER", "DIGITALINTERPRETATION", "SHADOWFORCES", "LUCIDMEMORY", "TUTANKHAMUN", "ALEXANDERPLATZ", "BERLINCLOCK", "WELTZEITUHR", "CARNARVON"])
    k, desc = next(iter(keys.items()))
    lines.append(f"{desc}: {k} ({len(k)} letters)")
    lines.append("")
    lines.append("sculpture's alphabet throughout, Vigenere: forced key letters at the first slots")
    for pos in (22, 23, 24, 25):
        f = MODES_KEY["vig"]; v = f(KRY.index(ctx.KNOWN[pos]), KRY.index(ctx.K4[pos - 1]))
        lines.append(f"pos {pos}: slot {(pos - 1) % len(k)} must be {KRY[v]}; the key has {k[(pos - 1) % len(k)]}")
    return "\n".join(lines)
