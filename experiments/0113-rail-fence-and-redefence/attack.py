"""Experiment 0113. See program.md for the contract."""

EXPERIMENT = {
    "slug": "rail-fence-and-redefence",
    "title": "The rail fence and the redefence (rails read in any order), with a repeating key before or after",
    "family": "6-transposition-then-tableau",
    "parent": "0092-plaintext-written-along-a-path",
    "changed": "The rail fence, writing the message in a zigzag over r rails and reading rail by rail, is the oldest hand transposition and is in none of the route sets so far. Here every rail count 2-48 and every start phase, with the rails read top to bottom, bottom to top, or (up to 6 rails) in every order (the redefence), forward and inverse, with a repeating key of length 1-26 after or before.",
    "hypothesis_expert": (
        "Type 1 and type 4 (a hand route as the masking step, C4; 'double matrixes', C1). Routes: zigzag over r = 2-48 "
        "rails, start phase 0 to 2r-3 (the first letter on any rail, going down or up), rails read in order or reversed, "
        "and for r <= 6 in all r! orders (redefence); forward and inverse, deduplicated. Key: periodic 1-26 after the move "
        "(slot = carved place mod p) or before it, 8 tableau classes, exact by slot agreement. Ten shuffled coppers."
    ),
    "hypothesis_eli5": (
        "The rail fence is a schoolbook way to scramble letters: write the message in a zigzag down and up over a few "
        "lines, like a fence, then read each line in turn. Here we try every number of lines up to 48, every starting "
        "point of the zigzag, and for up to six lines every order of reading them, with a short repeating secret word on "
        "the table before or after, against the 24 known letters."
    ),
    "prediction": "Nothing consistent below period 20; counts inside the coppers' range, give or take one period. Zero candidates.",
    "method": (
        "1. Build every rail setting and its move; drop repeats. 2. Test periods 1-26 in both orders and 8 classes by "
        "slot agreement. 3. Count per period on K4 and ten shuffled coppers."
    ),
    "walkthrough": (
        "1. Write the message on 3 rails: letter 1 on rail 1, 2 on rail 2, 3 on rail 3, 4 on rail 2, 5 on rail 1, and so on. "
        "2. Read rail 1 left to right, then rail 2, then rail 3. "
        "3. Each known letter lands at a new place; with a key of length p after the move, letters sharing a slot must agree. "
        "4. Repeat for every rail count, start, rail order, key length and rule, and with the key before the move."
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


def rail_of(i, r, off):
    """Rail of message letter i on a zigzag of r rails started at phase off."""
    cyc = 2 * r - 2
    k = (i + off) % cyc
    return k if k < r else cyc - k


def where_rails(r, off, order):
    """Write along the zigzag, read rail by rail in the given order, left to right."""
    rails = [rail_of(i, r, off) for i in range(N)]
    out = [i for rail in order for i in range(N) if rails[i] == rail]
    wh = [0] * N
    for j, i in enumerate(out):
        wh[i] = j
    return wh


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    places = sorted(known)
    pidx = [p - 1 for p in places]
    rng = random.Random(113)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    T = len(texts)
    classes = [(pa, ca, beau) for pa in ALPH for ca in ALPH for beau in (False, True)]
    CI = {an: [[{c: i for i, c in enumerate(ALPH[an])}[ch] for ch in t] for t in texts] for an in ALPH}
    PI = {an: [{c: i for i, c in enumerate(ALPH[an])}[known[p]] for p in places] for an in ALPH}
    pairsB = {p: slot_pairs([i % p for i in pidx]) for p in range(1, PMAX + 1)}
    from itertools import permutations
    seqs = {}
    for r in range(2, 49):
        for off in range(2 * r - 2):
            orders = permutations(range(r)) if r <= 6 else [tuple(range(r)), tuple(range(r))[::-1]]
            for order in orders:
                seqs[(r, off, tuple(order))] = f"{r} rails, offset {off}, rails read {[x + 1 for x in order]}"
    words = []
    seen = set()
    n_routes = n_dupes = 0
    k4_low = []
    live = {o: [[0] * (PMAX + 1) for _ in range(T)] for o in "AB"}
    for seq, word in seqs.items():
        wh = where_rails(*seq)
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
                            k4_low.append({"rails": word, "width": seq[0], "dir": d or "forward", "order": o,
                                           "class": f"{pa}/{ca}/{'beau' if beau else 'vig-var'}", "period": first})
        if ctx.time_left() < 60:
            break
    outside = {o: [p for p in range(1, PMAX + 1)
                   if not (min(live[o][t][p] for t in range(1, T)) <= live[o][0][p] <= max(live[o][t][p] for t in range(1, T)))]
               for o in "AB"}
    bounds = {
        "family": "rail fence (any start phase) and redefence (rails in any order up to 6 rails), then or before a periodic tableau key",
        "rail_settings": len(seqs), "distinct_routes": n_routes, "duplicates_skipped": n_dupes,
        "periods": [1, PMAX], "classes": 8,
        "k4_live_by_period": {o: live[o][0][1:] for o in "AB"},
        "controls_live_by_period_min": {o: [min(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in "AB"},
        "controls_live_by_period_max": {o: [max(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in "AB"},
        "periods_outside_control_range": outside,
        "k4_live_below_20": k4_low[:40], "n_k4_live_below_20": len(k4_low),
        "controls": f"{N_CONTROLS} shuffled coppers (seed 113), identical search",
    }
    notes = (f"{len(seqs):,} rail settings, {n_routes:,} distinct routes x 8 classes x 2 orders, "
             f"periods 1-26. K4 live below 20: {len(k4_low)}. Outside the control range: {outside}.")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    wh = where_rails(3, 0, (0, 1, 2))
    lines = ["rail fence of 3 rails from the top: rails 1 2 3 2 1 2 3 ..., read rail 1, then 2, then 3", "",
             "place  letter  rail  lands at  copper there"]
    for q in (22, 23, 24, 25, 64):
        lines.append(f"{q:>5}  {known[q]:>6}  {rail_of(q - 1, 3, 0) + 1:>4}  {wh[q - 1] + 1:>8}  {ct[wh[q - 1]]:>12}")
    return "\n".join(lines)
