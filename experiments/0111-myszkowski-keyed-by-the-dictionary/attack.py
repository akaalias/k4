"""Experiment 0111. See program.md for the contract."""

EXPERIMENT = {
    "slug": "myszkowski-keyed-by-the-dictionary",
    "title": "A Myszkowski transposition keyed by any English word with a repeated letter, with a repeating key before or after",
    "family": "6-transposition-then-tableau",
    "parent": "0110-keyword-columnar-from-the-whole-dictionary",
    "changed": "Every keyed column shuffle so far broke ties in the key word left to right (or dropped repeated letters). Myszkowski's 1902 variant reads columns that share a key letter together, row by row, which gives a different order whenever the word repeats a letter, as ABSCISSA and PALIMPSEST do. Here every dictionary word with a repeated letter is a Myszkowski key, with a repeating key of length 1-26 after or before the move.",
    "hypothesis_expert": (
        "Type 1, a route family not in any earlier set. ABSCISSA (K2's key) and PALIMPSEST (K1's) both repeat letters "
        "(C7(a)); a Myszkowski key reads the columns of equal rank together across each row. Keys: the rank pattern of "
        "every dictionary word of 3-30 letters with a repeated letter, deduplicated; rows of the word's length, the last "
        "row short; forward and inverse. Key: periodic 1-26 after the move (slot = carved place mod p) or before it, 8 "
        "tableau classes, exact by slot agreement. Ten shuffled coppers."
    ),
    "hypothesis_eli5": (
        "In the usual column shuffle you read the columns in the alphabetical order of a secret word's letters. When the "
        "word has a letter twice, like the two S's of ABSCISSA, Myszkowski's version reads those columns together, "
        "zigzagging across each row. We try every dictionary word with a repeated letter this way, with a short "
        "repeating secret word on the table before or after, against the 24 known letters."
    ),
    "prediction": "Nothing consistent below period 20; counts inside the coppers' range, give or take one period. Zero candidates.",
    "method": (
        "1. Turn every dictionary word with a repeated letter into its Myszkowski rank pattern; drop repeats. 2. Build "
        "the move and its inverse. 3. Test periods 1-26 in both orders and 8 classes by slot agreement. 4. Count per "
        "period on K4 and ten shuffled coppers."
    ),
    "walkthrough": (
        "1. ABSCISSA gives ranks A1 B2 S5 C3 I4 S5 S5 A1. "
        "2. Write the 97 letters in rows of 8. "
        "3. Read rank 1 first: in each row, column 1 then column 8; then rank 2 (column 2) down the rows; and so on, with rank 5 read across columns 3, 6, 7 in each row. "
        "4. Each known letter lands at a new place; with a key of length p after the move, letters sharing a slot must agree. "
        "5. Repeat for every word, key length and rule, and with the key before the move."
    ),
}

import random
from pathlib import Path
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.ciphers import columnar_transposition_encrypt
from kryptos.alphabets import numeric_order

N = 97
PMAX = 26
ALPH = {"std": STD, "kry": KRY}
N_CONTROLS = 10
ROOT = Path(__file__).resolve().parent
if not (ROOT / "kryptos").exists():
    ROOT = Path.cwd()


def keyword_sequence(word):
    rank = numeric_order(word)
    return sorted(range(len(rank)), key=lambda c: rank[c])


def full_sequence(word):
    w = [c for c in word.upper() if c.isalpha()]
    return sorted(range(len(w)), key=lambda c: (w[c], c))


def slot_pairs(slots):
    last, prs = {}, []
    for e, s in enumerate(slots):
        if s in last:
            prs.append((last[s], e))
        last[s] = e
    return prs


def where_columnar(seq):
    idx = "".join(chr(0x100 + i) for i in range(N))
    out = columnar_transposition_encrypt(idx, list(seq))
    w = [0] * N
    for j, ch in enumerate(out):
        w[ord(ch) - 0x100] = j
    return w


def myszkowski_key(word):
    """Rank of each column's letter among the word's distinct letters (repeats share a rank)."""
    order = sorted(set(word))
    return tuple(order.index(c) for c in word)


def myszkowski(text, key):
    """Myszkowski transposition: rows of len(key); ranks read in order; columns of equal rank read row by row, left to right."""
    w = len(key)
    rows = [text[i:i + w] for i in range(0, len(text), w)]
    out = []
    for r in range(max(key) + 1):
        cols = [c for c in range(w) if key[c] == r]
        for row in rows:
            for c in cols:
                if c < len(row):
                    out.append(row[c])
    return out


def where_myszkowski(key):
    out = myszkowski(list(range(N)), key)
    wh = [0] * N
    for j, i in enumerate(out):
        wh[i] = j
    return wh


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    places = sorted(known)
    pidx = [p - 1 for p in places]
    rng = random.Random(111)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    T = len(texts)
    classes = [(pa, ca, beau) for pa in ALPH for ca in ALPH for beau in (False, True)]
    CI = {an: [[{c: i for i, c in enumerate(ALPH[an])}[ch] for ch in t] for t in texts] for an in ALPH}
    PI = {an: [{c: i for i, c in enumerate(ALPH[an])}[known[p]] for p in places] for an in ALPH}
    pairsB = {p: slot_pairs([i % p for i in pidx]) for p in range(1, PMAX + 1)}
    words = [w.strip().upper() for w in (ROOT / "kryptos" / "data" / "words.txt").read_text().split()]
    seqs = {}
    for w in words:
        if not (3 <= len(w) <= 30 and w.isalpha()) or len(set(w)) == len(w):
            continue                                  # Myszkowski differs from plain keyword columnar only with repeats
        s = myszkowski_key(w)
        if s not in seqs:
            seqs[s] = w
    seen = set()
    n_routes = n_dupes = 0
    k4_low = []
    live = {o: [[0] * (PMAX + 1) for _ in range(T)] for o in "AB"}
    for seq, word in seqs.items():
        wh = where_myszkowski(seq)
        inv = [0] * N
        for i, j in enumerate(wh):
            inv[j] = i
        for d, r in (("", wh), (" inverse", inv)):
            h = hash(tuple(r))
            if h in seen:
                n_dupes += 1
                continue
            seen.add(h)
            n_routes += 1
            land = [r[i] for i in pidx]
            pairsA = {p: slot_pairs([j % p for j in land]) for p in range(1, PMAX + 1)}
            for pa, ca, beau in classes:
                Pv = PI[pa]
                for t in range(T):
                    C = CI[ca][t]
                    f = [(C[j] + Pv[e]) % 26 if beau else (C[j] - Pv[e]) % 26 for e, j in enumerate(land)]
                    for o, prs_by in (("A", pairsA), ("B", pairsB)):
                        L = live[o][t]
                        first = None
                        for p in range(1, PMAX + 1):
                            for x, y in prs_by[p]:
                                if f[x] != f[y]:
                                    break
                            else:
                                L[p] += 1
                                if first is None:
                                    first = p
                        if t == 0 and first is not None and first < 20:
                            k4_low.append({"word": word, "width": len(seq), "dir": d or "forward", "order": o,
                                           "class": f"{pa}/{ca}/{'beau' if beau else 'vig-var'}", "period": first})
        if ctx.time_left() < 60:
            break
    outside = {o: [p for p in range(1, PMAX + 1)
                   if not (min(live[o][t][p] for t in range(1, T)) <= live[o][0][p] <= max(live[o][t][p] for t in range(1, T)))]
               for o in "AB"}
    bounds = {
        "family": "Myszkowski transposition keyed by every dictionary word with a repeated letter, then or before a periodic tableau key",
        "words": len(words), "distinct_myszkowski_keys": len(seqs), "distinct_routes": n_routes, "duplicates_skipped": n_dupes,
        "periods": [1, PMAX], "classes": 8,
        "k4_live_by_period": {o: live[o][0][1:] for o in "AB"},
        "controls_live_by_period_min": {o: [min(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in "AB"},
        "controls_live_by_period_max": {o: [max(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in "AB"},
        "periods_outside_control_range": outside,
        "k4_live_below_20": k4_low[:40], "n_k4_live_below_20": len(k4_low),
        "controls": f"{N_CONTROLS} shuffled coppers (seed 111), identical search",
    }
    notes = (f"{len(seqs):,} distinct Myszkowski keys from {len(words):,} words, {n_routes:,} routes x 8 classes x 2 orders, "
             f"periods 1-26. K4 live below 20: {len(k4_low)}. Outside the control range: {outside}.")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    k = myszkowski_key("ABSCISSA")
    wh = where_myszkowski(k)
    lines = ["ABSCISSA as a Myszkowski key: ranks " + str([x + 1 for x in k]) + " (both A's rank 1, the S's rank 5)",
             "columns of equal rank are read together, row by row", "",
             "place  letter  lands at  copper there"]
    for q in (22, 23, 24, 25, 64):
        lines.append(f"{q:>5}  {known[q]:>6}  {wh[q - 1] + 1:>8}  {ct[wh[q - 1]]:>12}")
    return "\n".join(lines)
