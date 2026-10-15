"""Experiment 0114. See program.md for the contract."""

EXPERIMENT = {
    "slug": "amsco-keyed-by-the-dictionary",
    "title": "AMSCO, a column shuffle with cells of one and two letters, keyed by any English word, with a repeating key",
    "family": "6-transposition-then-tableau",
    "parent": "0110-keyword-columnar-from-the-whole-dictionary",
    "changed": "AMSCO (A. M. Scott, 1950s ACA) fills a keyed grid with cells that alternate one and two letters, then reads the columns in key order, so letter pairs travel together. It is in none of the route sets. Here every dictionary word giving 3-15 columns keys it, with either cell size first, forward and inverse, with a repeating key of length 1-26 after or before.",
    "hypothesis_expert": (
        "Type 1, a hand route not tested before. AMSCO: rows of w cells holding alternately 1 and 2 letters, each row "
        "starting with the other size from the row above, the first cell 1 or 2; columns read in true keyword order "
        "(repeats dropped, or the whole word), cells top to bottom; w = 3-15 from every dictionary word; forward and "
        "inverse, deduplicated. Key: periodic 1-26 after (slot = carved place mod p) or before, 8 tableau classes, exact by "
        "slot agreement. Keeping letter pairs together would also keep some English adjacency, as the width-21 repeats "
        "suggest (0018). Ten shuffled coppers."
    ),
    "hypothesis_eli5": (
        "AMSCO is a column shuffle in which the grid's boxes hold one letter, then two, then one, alternating, so some "
        "pairs of letters stay together when the columns are read out under a secret word. We try every dictionary word "
        "as the column word, with a short repeating secret word on the table before or after, against the 24 known letters."
    ),
    "prediction": "Nothing consistent below period 20; counts inside the coppers' range, give or take one period. Zero candidates.",
    "method": (
        "1. Turn every dictionary word into its column orders of 3-15 columns, each with either first cell size. "
        "2. Build the move and its inverse; drop repeats. 3. Test periods 1-26 in both orders and 8 classes. 4. Count "
        "per period on K4 and ten shuffled coppers."
    ),
    "walkthrough": (
        "1. Under SHADOW (6 columns), fill the first row with cells of 1, 2, 1, 2, 1, 2 letters, the second with 2, 1, 2, 1, 2, 1, and so on. "
        "2. Read the columns in the order 3, 4, 2, 5, 1, 6, each column's cells top to bottom. "
        "3. Each known letter lands at a new place; with a key of length p after the move, letters sharing a slot must agree. "
        "4. Repeat for every word, first cell size, key length and rule, and with the key before the move."
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


def amsco_cells(n, w, first):
    """Rows of w cells holding 1 or 2 letters alternately; each row starts with the other size from the row above."""
    cells, i, row, start = [], 0, 0, first
    while i < n:
        size = start
        for c in range(w):
            if i >= n:
                break
            k = min(size, n - i)
            cells.append((row, c, list(range(i, i + k))))
            i += k
            size = 3 - size
        row += 1
        start = 3 - start
    return cells


def where_amsco(order, first):
    cells = amsco_cells(N, len(order), first)
    out = []
    for col in order:
        for row, c, idx in sorted(cells):
            if c == col:
                out.extend(idx)
    wh = [0] * N
    for j, i in enumerate(out):
        wh[i] = j
    return wh


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    places = sorted(known)
    pidx = [p - 1 for p in places]
    rng = random.Random(114)
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
        if not (3 <= len(w) <= 30 and w.isalpha()):
            continue
        for s in (tuple(keyword_sequence(w)), tuple(full_sequence(w))):
            if 3 <= len(s) <= 15:
                for first in (1, 2):
                    if (s, first) not in seqs:
                        seqs[(s, first)] = w
    seen = set()
    n_routes = n_dupes = 0
    k4_low = []
    live = {o: [[0] * (PMAX + 1) for _ in range(T)] for o in "AB"}
    for seq, word in seqs.items():
        wh = where_amsco(*seq)
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
                            k4_low.append({"word": word, "width": len(seq[0]), "first_cell": seq[1], "dir": d or "forward", "order": o,
                                           "class": f"{pa}/{ca}/{'beau' if beau else 'vig-var'}", "period": first})
        if ctx.time_left() < 60:
            break
    outside = {o: [p for p in range(1, PMAX + 1)
                   if not (min(live[o][t][p] for t in range(1, T)) <= live[o][0][p] <= max(live[o][t][p] for t in range(1, T)))]
               for o in "AB"}
    bounds = {
        "family": "AMSCO (cells of 1 and 2 letters) keyed by every dictionary word of 3-15 columns, then or before a periodic tableau key",
        "words": len(words), "distinct_key_and_start_settings": len(seqs), "distinct_routes": n_routes, "duplicates_skipped": n_dupes,
        "periods": [1, PMAX], "classes": 8,
        "k4_live_by_period": {o: live[o][0][1:] for o in "AB"},
        "controls_live_by_period_min": {o: [min(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in "AB"},
        "controls_live_by_period_max": {o: [max(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in "AB"},
        "periods_outside_control_range": outside,
        "k4_live_below_20": k4_low[:40], "n_k4_live_below_20": len(k4_low),
        "controls": f"{N_CONTROLS} shuffled coppers (seed 114), identical search",
    }
    notes = (f"{len(seqs):,} distinct AMSCO settings from {len(words):,} words, {n_routes:,} routes x 8 classes x 2 orders, "
             f"periods 1-26. K4 live below 20: {len(k4_low)}. Outside the control range: {outside}.")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    seq = keyword_sequence("SHADOW")
    wh = where_amsco(tuple(seq), 1)
    cells = amsco_cells(N, 6, 1)
    lines = ["AMSCO under SHADOW, first cell one letter: the first rows of cells (place numbers)", ""]
    for r in range(4):
        lines.append("  " + "  ".join("-".join(str(i + 1) for i in idx) for row, c, idx in cells if row == r))
    lines += ["", f"columns read in the order {[c + 1 for c in seq]}", "place  letter  lands at  copper there"]
    for q in (22, 23, 24, 25, 64):
        lines.append(f"{q:>5}  {known[q]:>6}  {wh[q - 1] + 1:>8}  {ct[wh[q - 1]]:>12}")
    return "\n".join(lines)
