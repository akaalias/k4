"""Experiment 0061. See program.md for the contract."""

EXPERIMENT = {
    "slug": "keyword-plus-misspelling-letters",
    "title": "A puzzle word plus the misspelled letters as a second, short secret word",
    "family": "3-two-component-key",
    "parent": "0024-keyword-plus-k2-coordinate-digits",
    "changed": "Experiments 24 and 38 added the K2 coordinates or numbers from the story to a puzzle word. Sanborn said the misspellings matter for their orientation, so here the second part is made of letters instead: the wrong letters Q, U and A from IQLUSION, UNDERGRUUND and DESPARATLY, the right letters L, O and E, the raised YAR, and their reorderings, added to every puzzle word and every word of the solved messages.",
    "hypothesis_expert": (
        "C10(a) and C22: the misspelt letters (Q in IQLUSION, U in UNDERGRUUND, A in DESPARATLY, and the "
        "dropped E of DESPERATELY) and the raised YAR as key material. Two-component key k[i] = W[i mod a] + "
        "s S[i mod b] (family 3, Scheidt's combined keys), W any vocabulary word or K1-K3/C13/C14 word, S "
        "every ordering of QUA, LOE, QUAE, LOEE and YAR, and DYAHR in carved order, s = +1 or -1; letters "
        "read as indices on the standard or KRYPTOS order; plain and cipher alphabets standard or KRYPTOS; "
        "Vigenere, Beaufort, variant Beaufort. The key is fully determined, so each setting decrypts and the "
        "24 cribs are counted exactly. Control: the best count on ten shuffled coppers under the same "
        "settings. Bounds: complete for these words, orderings and conventions."
    ),
    "hypothesis_eli5": (
        "Sanborn misspelled three words on purpose and said the misspellings matter. The wrong letters are "
        "Q, U and A; the right ones would be L, O and E. A few letters on the sculpture are also raised, "
        "spelling YAR. Here those letters become a second, very short secret word, added on top of a "
        "longer word from the puzzle or the solved messages, and the two together are used on the table. "
        "With both words fixed there is nothing to guess, so we simply count how many of the 24 known "
        "letters come out right, and compare with scrambled copies of the copper."
    ),
    "prediction": (
        "No setting recovers more than about 8 of the 24 known letters, the same as on the shuffles. Zero "
        "candidates pass."
    ),
    "method": (
        "1. List the long words and the short-key orderings. 2. For each convention, compute the key index "
        "each crib requires. 3. For each word, ordering, sign and key alphabet, form the key at the crib "
        "places and count matches. 4. Decrypt the best settings and submit any with all 24. 5. Repeat the "
        "count on ten shuffles."
    ),
    "walkthrough": (
        "1. Take the word KRYPTOS and the short key QUA, on the standard alphabet: K=10, R=17, Y=24, P=15, "
        "T=19, O=14, S=18 and Q=16, U=20, A=0. 2. Place 22 uses letter 21 mod 7 = 0 of KRYPTOS, K=10, and "
        "letter 21 mod 3 = 0 of QUA, Q=16: the key is 10 + 16 = 26 = 0. 3. Under plain Vigenere on the "
        "standard alphabet the carved F at place 22 then reads F - 0 = F. 4. The message has E there, so "
        "this setting misses place 22. 5. Count the misses over all 24 known places, then do the same for "
        "every word, short key, sign and table."
    ),
}

import random
from itertools import permutations
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

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

ALPHAS = {"std": STD, "kry": KRY}
MODES = {"vig": lambda p, c: (c - p) % 26, "beau": lambda p, c: (c + p) % 26, "varbeau": lambda p, c: (p - c) % 26}
DEC = {"vig": lambda c, k: (c - k) % 26, "beau": lambda c, k: (k - c) % 26, "varbeau": lambda c, k: (c + k) % 26}
ENC = {"vig": lambda p, k: (p + k) % 26, "beau": lambda p, k: (k - p) % 26, "varbeau": lambda p, k: (p - k) % 26}


def short_keys():
    out = set()
    for base in ("QUA", "LOE", "QUAE", "LOEE", "YAR"):
        out |= {"".join(p) for p in permutations(base)}
    out.add("DYAHR")
    return sorted(out)


def long_words(vocab):
    return sorted({w for w in vocab if len(w) >= 2} | {w for w in SPACED.split() if len(w) >= 2} | set(EXTRA))


def encrypt(plaintext, key):
    pa, ca, m, k = ALPHAS[key["pa"]], ALPHAS[key["ca"]], key["m"], key["k"]
    return "".join(ca[ENC[m](pa.index(p), k[i])] for i, p in enumerate(plaintext))


def best_counts(ct, crib, words, shorts):
    """Exact count of crib hits for every setting. Hit at crib k iff the short key's letter at
    k's residue equals sgn * (required - word letter); counted per residue with histograms."""
    pos = [p - 1 for p, _ in crib]
    by_len = {}
    for s in shorts:
        by_len.setdefault(len(s), []).append(s)
    best = (0, None)
    for pn, pa in ALPHAS.items():
        for cn, ca in ALPHAS.items():
            for m, f in MODES.items():
                req = [f(pa.index(p), ca.index(ct[q - 1])) for q, p in crib]
                for kn, KA in ALPHAS.items():
                    sidx = {s: [KA.index(ch) for ch in s] for s in shorts}
                    for w in words:
                        W = [KA.index(w[i % len(w)]) for i in pos]
                        for sgn in (1, -1):
                            need = [(sgn * (r - x)) % 26 for r, x in zip(req, W)]
                            for b, group in by_len.items():
                                hist = [[0] * 26 for _ in range(b)]
                                for i, v in zip(pos, need):
                                    hist[i % b][v] += 1
                                for s in group:
                                    si = sidx[s]
                                    h = 0
                                    for r in range(b):
                                        h += hist[r][si[r]]
                                    if h > best[0]:
                                        best = (h, (w, s, sgn, kn, pn, cn, m))
    return best


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    crib = sorted(known.items())
    words, shorts = long_words(ctx.vocabulary), short_keys()
    best = best_counts(ct, crib, words, shorts)
    rng = random.Random(61)
    ctl = []
    for _ in range(10):
        sh = list(ct); rng.shuffle(sh)
        ctl.append(best_counts("".join(sh), crib, words, shorts)[0])
        if ctx.time_left() < 120:
            break
    cands = []
    if best[1]:
        w, s, sgn, kn, pn, cn, m = best[1]
        KA = ALPHAS[kn]
        k = [(KA.index(w[i % len(w)]) + sgn * KA.index(s[i % len(s)])) % 26 for i in range(len(ct))]
        pa, ca = ALPHAS[pn], ALPHAS[cn]
        pt = "".join(pa[DEC[m](ca.index(c), k[i])] for i, c in enumerate(ct))
        cands.append({"plaintext": pt, "key": {"pa": pn, "ca": cn, "m": m, "k": k}, "key_bits": 4.7 * (len(w) + len(s)),
                      "key_description": f"{w} {'+' if sgn > 0 else '-'} {s} on {kn}; plain {pn}, cipher {cn}, {m}"})
    n_set = len(words) * len(shorts) * 2 * 2 * 4 * 3
    return {
        "candidates": cands,
        "bounds": {"family": "two-component key: a word plus a short key from the misspelt or raised letters", "long_words": len(words),
                   "short_keys": len(shorts), "settings": n_set, "best_hits": best[0],
                   "best_setting": None if not best[1] else dict(zip(["word", "short", "sign", "key_alphabet", "plain", "cipher", "mode"], best[1])),
                   "control_best_hits": ctl},
        "notes": f"{n_set:,} settings; best {best[0]}/24 known letters; ten shuffled coppers best {sorted(ctl)}.",
    }


def worked_example(ctx, key):
    w, s = "KRYPTOS", "QUA"
    lines = ["place  word letter  short letter  key  carved  reads  message"]
    for pos in (22, 23, 24, 25):
        i = pos - 1
        k = (STD.index(w[i % 7]) + STD.index(s[i % 3])) % 26
        c = ctx.K4[i]
        lines.append(f"{pos:>5}      {w[i % 7]}            {s[i % 3]}        {k:>2}     {c}      {STD[(STD.index(c) - k) % 26]}      {ctx.KNOWN[pos]}")
    return "\n".join(lines)
