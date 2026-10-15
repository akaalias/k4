"""Experiment 0110. See program.md for the contract."""

EXPERIMENT = {
    "slug": "keyword-columnar-from-the-whole-dictionary",
    "title": "A column shuffle keyed by any English word, with a repeating key before or after",
    "family": "6-transposition-then-tableau",
    "parent": "0085-true-keyword-columnar-rerun",
    "changed": "0085 tested true keyword columnar (issue #26) with the puzzle's own 201 words. Here the column key is any word of the project dictionary (233,000 words, read with repeated letters dropped and as the whole word with ties left to right), every distinct column order once, forward and inverse, with a repeating key of length 1-26 after or before the shuffle.",
    "hypothesis_expert": (
        "Type 1 (C1, 'double matrixes... then went back to this table'); K3's NSA route is a keyword columnar by "
        "KRYPTOS (01-facts.md). Column orders: keyword_sequence (repeats dropped, alphabetical order of the key letters, "
        "ties left to right) and full_sequence (whole word) from every dictionary word of 2-30 letters, deduplicated "
        "(the same order from different words counts once), each as a single columnar transposition, forward and inverse. "
        "Key: periodic 1-26 after the move (slot = carved place mod p) or before it, 8 tableau classes, exact by slot "
        "agreement. Ten shuffled coppers."
    ),
    "hypothesis_eli5": (
        "A classic way to move letters: write the message under a secret word in rows, then read the columns in the "
        "alphabetical order of the word's letters. Experiment 85 tried the puzzle's own words. Here every word in an "
        "English dictionary is tried as the column word, followed or preceded by a short repeating secret word on the "
        "table, against the 24 known letters."
    ),
    "prediction": (
        "Nothing consistent below period 20; counts at every period inside the coppers' range, give or take one. Zero candidates."
    ),
    "method": (
        "1. Turn every dictionary word into its two column orders and drop repeats. 2. For each order, build the move "
        "and its inverse. 3. For each move and class, compute the key values at the known letters and test periods 1-26 "
        "in both orders. 4. Count settings per period on K4 and ten shuffled coppers."
    ),
    "walkthrough": (
        "1. Take the word SHADOW: alphabetical order A D H O S W gives the reading order of columns 3, 4, 2, 5, 1, 6. "
        "2. Write the 97 letters in rows of 6 and read the columns in that order. "
        "3. Each known letter lands at a new place j; with a key of length p after the move, its key letter is slot j mod p. "
        "4. Known letters on the same slot must agree. 5. Repeat for every word, key length and rule, and with the key before the move."
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


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    places = sorted(known)
    pidx = [p - 1 for p in places]
    rng = random.Random(110)
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
        if not (2 <= len(w) <= 30 and w.isalpha()):
            continue
        for s in (tuple(keyword_sequence(w)), tuple(full_sequence(w))):
            if len(s) >= 2 and s not in seqs and s != tuple(range(len(s))):
                seqs[s] = w
    seen = set()
    n_routes = n_dupes = 0
    k4_low = []
    live = {o: [[0] * (PMAX + 1) for _ in range(T)] for o in "AB"}
    for seq, word in seqs.items():
        wh = where_columnar(seq)
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
        "family": "true-keyword columnar from every dictionary word, then or before a periodic tableau key",
        "words": len(words), "distinct_column_orders": len(seqs), "distinct_routes": n_routes, "duplicates_skipped": n_dupes,
        "periods": [1, PMAX], "classes": 8,
        "k4_live_by_period": {o: live[o][0][1:] for o in "AB"},
        "controls_live_by_period_min": {o: [min(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in "AB"},
        "controls_live_by_period_max": {o: [max(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in "AB"},
        "periods_outside_control_range": outside,
        "k4_live_below_20": k4_low[:40], "n_k4_live_below_20": len(k4_low),
        "controls": f"{N_CONTROLS} shuffled coppers (seed 110), identical search",
    }
    notes = (f"{len(seqs):,} distinct column orders from {len(words):,} words, {n_routes:,} routes x 8 classes x 2 orders, "
             f"periods 1-26. K4 live below 20: {len(k4_low)}. Outside the control range: {outside}.")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    seq = keyword_sequence("SHADOW")
    wh = where_columnar(seq)
    lines = [f"SHADOW: columns read in the order {[c + 1 for c in seq]}", "",
             "place  letter  lands at  copper there"]
    for q in (22, 23, 24, 25, 64):
        lines.append(f"{q:>5}  {known[q]:>6}  {wh[q - 1] + 1:>8}  {ct[wh[q - 1]]:>12}")
    return "\n".join(lines)
