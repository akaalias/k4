"""Experiment 0065. See program.md for the contract."""

EXPERIMENT = {
    "slug": "constructions-that-line-up-doublets-in-sevens",
    "title": "Which ways of making a cipher put the doubled letters in one column of seven?",
    "family": "7-construction-simulation",
    "parent": "0062-which-constructions-make-the-width-fingerprints",
    "changed": "Experiment 62 found no recipe that makes the copper's doublet column at width 7. This tries recipes built specifically to line doublets up in sevens: a key that feeds on the previous carved letter plus a repeating key of 7, a key with two equal neighbouring letters, the same reshuffle applied to every block of 7, and a key of 28 with a pattern every 7.",
    "hypothesis_expert": (
        "Family 7 (Oranchak's construction simulation), aimed at the width-7 doublet column that 0056 "
        "showed is real (five of six doublets at 0-based positions 18, 25, 32, 46, 67, all 4 mod 7). A "
        "ciphertext doublet c[i] = c[i+1] needs a mechanism tied to i mod 7. Candidates: (1) ciphertext "
        "autokey at lag 1 plus a period-7 key, c[i] = p[i] + k[i mod 7] + c[i-1]: a doublet appears exactly "
        "when p[i+1] = -k[(i+1) mod 7], so one column fires on a frequent plaintext letter; periods 14 and 28 "
        "for comparison. (2) plaintext autokey at lag 1 plus a period-7 key. (3) a period-7 key with two "
        "equal neighbouring letters, which passes plaintext doublets through in one column only. (4) a "
        "period-7 Vigenere and one fixed reshuffle of every block of 7, in either order. (5) a period-28 key "
        "whose steps at slots 4-5, 11-12, 18-19, 25-26 are equal (28 survives the crib sweep). (6) a "
        "period-7 Vigenere read out in columns of 7 from a width-14 grid. Plaintexts: 97-letter windows of "
        "Carter's Tomb of Tut-ankh-Amen and K1-K3 (C7(d)). 4,000 samples per recipe, KRYPTOS alphabet, "
        "random keys. Statistic as in 0056 and 0062: at least 4 doublets with at most one outside the "
        "fullest column of 7. Calibrations: random letters and shuffles of K4. Clue entries: C11a "
        "('interval 7'), C1(a)."
    ),
    "hypothesis_eli5": (
        "Five of the copper's six doubled letters sit in the same column when the carved letters are "
        "written in rows of seven, and experiment 56 showed that is no accident. We make thousands of fake "
        "coppers from real English with recipes that have a seven built in, and count how often each recipe "
        "puts the doublets in one column. The most promising recipe is an autokey cipher that feeds on the "
        "previous carved letter, combined with a repeating secret word of seven letters. Random letters and "
        "scrambled copies of the copper show how often the pattern turns up by luck."
    ),
    "prediction": (
        "The ciphertext autokey at lag 1 with a period-7 key makes the doublet column in more than 5% of "
        "samples, at least ten times the calibrations (which stay below 0.5%). The key with two equal "
        "neighbouring letters makes it rarely (below 2%), because English doublets are few. The block "
        "reshuffles, the structured key of 28 and the width-14 read-out stay within twice the calibration rate."
    ),
    "method": (
        "1. Draw 97-letter English windows. 2. Encipher each with each recipe and a fresh random key. "
        "3. Find the doublets and write the text in rows of 7; note whether at least four doublets fall in "
        "one column with at most one elsewhere. 4. Count the share of samples with the mark, and the mean "
        "number of doublets. 5. Compare with random letters and shuffled K4."
    ),
    "walkthrough": (
        "1. Take a 97-letter stretch of Carter's book and a random secret word of 7 letters. "
        "2. Encipher the first letter on the sculpture's table with the first key letter. "
        "3. For each later letter, add its key letter and also the previous carved letter, counted along "
        "the sculpture's alphabet KRYPTOSABCDEFGHIJLMNQUVWXZ, and write the result. "
        "4. A letter repeats its neighbour exactly when the plaintext letter plus its key letter counts to "
        "26, back to K: A is 7th from K (counting K as 0) and N is 19th, so with key letter A in slot 5, "
        "every N in slot 5 makes a doublet. "
        "5. Write the result in rows of 7 and look for a column holding most of the doublets. "
        "6. Repeat four thousand times per recipe and count."
    ),
}

import random
from collections import Counter
from pathlib import Path
from kryptos.facts import KRYPTOS_ALPHABET as KRY, load_k1, load_k2, load_k3
from kryptos.ciphers import columnar_transposition_encrypt

N = 97
ROOT = Path(__file__).resolve().parent
IDX = {c: i for i, c in enumerate(KRY)}


def letters(s):
    return "".join(c for c in s.upper() if "A" <= c <= "Z")


def encrypt(plaintext, key):
    return plaintext


def doublets(t):
    return [i for i in range(len(t) - 1) if t[i] == t[i + 1]]


def col_mark(t):
    dbl = doublets(t)
    if len(dbl) < 4:
        return False
    top = max(Counter(i % 7 for i in dbl).values())
    return len(dbl) - top <= 1 and top >= 4


def vig(pt, key):
    return "".join(KRY[(IDX[p] + key[i % len(key)]) % 26] for i, p in enumerate(pt))


def ct_auto_periodic(pt, key, rng):
    out, prev = [], rng.randrange(26)
    for i, p in enumerate(pt):
        c = (IDX[p] + key[i % len(key)] + prev) % 26
        out.append(KRY[c]); prev = c
    return "".join(out)


def pt_auto_periodic(pt, key, rng):
    prev = rng.randrange(26)
    out = []
    for i, p in enumerate(pt):
        out.append(KRY[(IDX[p] + key[i % len(key)] + prev) % 26]); prev = IDX[p]
    return "".join(out)


def block_perm(t, perm):
    out = []
    for b in range(0, len(t), 7):
        blk = t[b:b + 7]
        if len(blk) == 7:
            out.append("".join(blk[perm[j]] for j in range(7)))
        else:
            out.append(blk)
    return "".join(out)


def rk(rng, n):
    return [rng.randrange(26) for _ in range(n)]


def generators():
    g = {}
    for P in (7, 14, 28):
        g[f"ciphertext autokey lag 1 plus a period-{P} key"] = lambda pt, rng, P=P: ct_auto_periodic(pt, rk(rng, P), rng)
    g["plaintext autokey lag 1 plus a period-7 key"] = lambda pt, rng: pt_auto_periodic(pt, rk(rng, 7), rng)

    def eqpair(pt, rng):
        k = rk(rng, 7); j = rng.randrange(7); k[(j + 1) % 7] = k[j]
        return vig(pt, k)
    g["period-7 key with two equal neighbouring letters"] = eqpair
    g["period-7 Vigenere, then one reshuffle of every block of 7"] = lambda pt, rng: block_perm(vig(pt, rk(rng, 7)), rng.sample(range(7), 7))
    g["one reshuffle of every block of 7, then period-7 Vigenere"] = lambda pt, rng: vig(block_perm(pt, rng.sample(range(7), 7)), rk(rng, 7))

    def k28(pt, rng):
        k = rk(rng, 28); d = rng.randrange(26)
        for s in (4, 11, 18, 25):
            k[s + 1] = (k[s] + d) % 26
        return vig(pt, k)
    g["period-28 key with the same step at slots 4-5, 11-12, 18-19, 25-26"] = k28
    g["period-7 Vigenere read out in columns of 7 (width-14 grid)"] = lambda pt, rng: columnar_transposition_encrypt(vig(pt, rk(rng, 7)), rng.sample(range(14), 14))
    return g


def run(ctx):
    ct = ctx.K4
    carter = letters((ROOT / "knowledge" / "sources" / "carter-1923-tomb-of-tutankhamen-vol1.txt").read_text(errors="ignore"))
    k123 = letters(load_k1()["plaintext"] + load_k2()["plaintext_as_carved"] + load_k3()["plaintext"])
    source = carter + k123
    rng = random.Random(65)
    S = 4000
    gens = generators()
    gens["calibration: random letters"] = lambda pt, rng: "".join(rng.choice(KRY) for _ in range(N))
    gens["calibration: shuffled K4"] = lambda pt, rng: "".join(rng.sample(ct, N))
    table = {}
    for name, g in gens.items():
        hits, nd = 0, 0
        for _ in range(S):
            i = rng.randrange(0, len(source) - N)
            t = g(source[i:i + N], rng)
            hits += col_mark(t); nd += len(doublets(t))
        table[name] = {"column": round(hits / S, 4), "mean_doublets": round(nd / S, 2)}
        if ctx.time_left() < 120:
            break
    order = sorted(table.items(), key=lambda kv: -kv[1]["column"])
    return {
        "candidates": [],
        "bounds": {"family": "construction simulation for the width-7 doublet column", "samples_per_recipe": S,
                   "k4": {"column": col_mark(ct), "doublets": len(doublets(ct))},
                   "plaintext_source": f"Carter vol. 1 ({len(carter):,} letters) and K1-K3", "rates": table},
        "notes": "Doublet-column rate (mean doublets): " + "; ".join(f"{k}: {v['column']:.4f} ({v['mean_doublets']})" for k, v in order) + ".",
    }


def worked_example(ctx, key):
    rng = random.Random(1)
    pt = "SLOWLYDESPARATLYSLOWLYTHEREMAINSOFPASSAGEDEBRIS"
    k = [IDX[c] for c in "KRYPTOS"]
    t = ct_auto_periodic(pt, k, rng)
    return f"plaintext {pt}\nkey KRYPTOS repeating, plus the previous carved letter\ncarved   {t}\ndoublets at 0-based {doublets(t)}; mod 7 {[i % 7 for i in doublets(t)]}"
