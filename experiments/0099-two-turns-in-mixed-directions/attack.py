"""Experiment 0099. See program.md for the contract."""

EXPERIMENT = {
    "slug": "two-turns-in-mixed-directions",
    "title": "Two quarter turns in mixed directions (clockwise then anticlockwise, and the reverse), with a repeating key",
    "family": "6-transposition-then-tableau",
    "parent": "0083-every-triple-grid-turn",
    "changed": "0080-0083 composed quarter turns in one direction only (clockwise, twice or three times). K3's rotations and Sanborn's 'double matrixes' do not fix the sense of each turn. Here every pair of widths 2-96 is turned clockwise then anticlockwise, anticlockwise then clockwise, and anticlockwise twice, forward and inverse, deduplicated against each other and against the clockwise pairs already tested, with a repeating key of length 1-26 before or after.",
    "hypothesis_expert": (
        "Type 1 of directions.md, closing a gap in 0080 and 0083: the two-turn library held only clockwise-clockwise "
        "pairs. Sanborn: 'double matrixes and triple matrixes... then went back to this table' (C1); K3 is two "
        "rotations of 14 x 24 and 8 x 42 grids (01-facts.md; the Stehle formula). A turn on a ragged grid is not the "
        "reverse of the other turn, so mixed senses give new routes. Routes: turn(w1, d1) then turn(w2, d2), (d1, d2) "
        "in {(cw, ccw), (ccw, cw), (ccw, ccw)}, w1, w2 = 2-96, forward and inverse, minus repeats and minus the "
        "cw-cw set. Key: periodic 1-26 after the move (slot = carved place mod p) or before it, 8 tableau classes, exact "
        "by slot agreement; the excess check counts distinct check sets (the lesson of 0086 and 0092). Ten shuffled coppers."
    ),
    "hypothesis_eli5": (
        "K3 was made by writing the message in a grid, turning the grid a quarter turn, writing it out, and doing that "
        "again with a grid of another width. Experiments 80 and 83 always turned the same way. Here the two turns go "
        "in opposite directions, or both the other way, at every pair of widths, followed or preceded by a short "
        "repeating secret word, and each combination is checked against the 24 known letters."
    ),
    "prediction": (
        "Nothing consistent below period 20; at every period the number of distinct consistent check sets on K4 lies "
        "inside the ten coppers' range, give or take one period. Zero candidates."
    ),
    "method": (
        "1. Build the clockwise-pair set of 0080 to skip. 2. For each sense pair and widths, compose the two turns and "
        "its inverse; drop repeats. 3. For each route and class, compute the key values at the known letters and test "
        "periods 1-26 in both orders. 4. Count settings and distinct check sets per period on K4 and ten shuffled "
        "coppers. 5. List K4's settings below period 20."
    ),
    "walkthrough": (
        "1. Write the 97 letters in rows of 9; read the columns bottom to top, left column first (a clockwise quarter turn). "
        "2. Write the result in rows of 12; read the columns top to bottom, right column first (an anticlockwise quarter turn). "
        "3. Each known letter, say E at place 22, now sits at a new place j. "
        "4. With a key of length p after the move, its key letter is slot j mod p and must turn E into the carved letter at j; letters sharing a slot must agree. "
        "5. Repeat for every pair of widths, the three mixed senses, key lengths 1-26 and table rules, and with the key before the move."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
PMAX = 26
ALPH = {"std": STD, "kry": KRY}
N_CONTROLS = 10
NULL = -1


def grid(tokens, w, top):
    """Rows of the grid as lists of tokens or None for a blank cell."""
    n = len(tokens)
    h = -(-n // w)
    blanks = h * w - n
    cells, it = [], iter(tokens)
    for c in range(h * w):
        blank = c < blanks if top else c >= h * w - blanks
        cells.append(None if blank else next(it))
    return [cells[r * w:(r + 1) * w] for r in range(h)]


def turn(tokens, w, top, way="cw", fill=False):
    """One quarter turn. fill=True: blank cells come out as NULL fillers instead of vanishing."""
    rows = grid(tokens, w, top)
    h = len(rows)
    cols = range(w) if way == "cw" else range(w - 1, -1, -1)
    rr = range(h - 1, -1, -1) if way == "cw" else range(h)
    out = []
    for c in cols:
        for r in rr:
            t = rows[r][c]
            if t is None:
                if fill:
                    out.append(NULL)
            else:
                out.append(t)
    return out


def slot_pairs(slots):
    """Consecutive pairs of known letters sharing a slot."""
    last, prs = {}, []
    for e, s in enumerate(slots):
        if s in last:
            prs.append((last[s], e))
        last[s] = e
    return prs



def turn_perm(w):
    """where-map of one clockwise quarter turn: position of letter i in the turned text."""
    sigma = turn(list(range(N)), w, False, "cw")
    wh = [0] * N
    for j, i in enumerate(sigma):
        wh[i] = j
    return wh


def where_of_turns(seq):
    """seq: list of (width, way). where[i] = place after the turns of message letter i."""
    s = list(range(N))
    for w, way in seq:
        s = turn(s, w, False, way)
    wh = [0] * N
    for j, i in enumerate(s):
        wh[i] = j
    return wh


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    places = sorted(known)
    pidx = [p - 1 for p in places]
    rng = random.Random(99)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    T = len(texts)
    classes = [(pa, ca, beau) for pa in ALPH for ca in ALPH for beau in (False, True)]
    CI = {an: [[{c: i for i, c in enumerate(ALPH[an])}[ch] for ch in t] for t in texts] for an in ALPH}
    PI = {an: [{c: i for i, c in enumerate(ALPH[an])}[known[p]] for p in places] for an in ALPH}
    pairsB = {p: slot_pairs([i % p for i in pidx]) for p in range(1, PMAX + 1)}
    single = {(w, way): where_of_turns([(w, way)]) for w in range(2, N) for way in ("cw", "ccw")}
    seen = set()
    for w1 in range(2, N):
        for w2 in range(2, N):
            a, b = single[(w1, "cw")], single[(w2, "cw")]
            fwd = [b[a[i]] for i in range(N)]
            inv = [0] * N
            for i, j in enumerate(fwd):
                inv[j] = i
            seen.add(tuple(fwd)); seen.add(tuple(inv))
    n_cwcw = len(seen)
    live = {o: [[0] * (PMAX + 1) for _ in range(T)] for o in "AB"}
    dist = {o: [[set() for _ in range(PMAX + 1)] for _ in range(T)] for o in "AB"}
    k4_low = []
    n_routes = n_dupes = 0
    for d1, d2 in (("cw", "ccw"), ("ccw", "cw"), ("ccw", "ccw")):
        for w1 in range(2, N):
            a = single[(w1, d1)]
            for w2 in range(2, N):
                b = single[(w2, d2)]
                fwd = [b[a[i]] for i in range(N)]
                inv = [0] * N
                for i, j in enumerate(fwd):
                    inv[j] = i
                for dname, wh in (("", fwd), (" inverse", inv)):
                    key = tuple(wh)
                    if key in seen:
                        n_dupes += 1
                        continue
                    seen.add(key)
                    n_routes += 1
                    land = [wh[i] for i in pidx]
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
                                    prs = prs_by[p]
                                    for x, y in prs:
                                        if f[x] != f[y]:
                                            break
                                    else:
                                        L[p] += 1
                                        if p <= 24:
                                            dist[o][t][p].add((frozenset(prs), pa, ca, beau))
                                        if first is None:
                                            first = p
                                if t == 0 and first is not None and first < 20:
                                    k4_low.append({"turns": f"{d1} {w1}, {d2} {w2}{dname}", "order": o,
                                                   "class": f"{pa}/{ca}/{'beau' if beau else 'vig-var'}", "period": first})
        if ctx.time_left() < 60:
            break
    D = {o: [[len(dist[o][t][p]) for p in range(PMAX + 1)] for t in range(T)] for o in "AB"}
    out_s = {o: [p for p in range(1, PMAX + 1) if not (min(live[o][t][p] for t in range(1, T)) <= live[o][0][p] <= max(live[o][t][p] for t in range(1, T)))] for o in "AB"}
    out_d = {o: [p for p in range(1, 25) if not (min(D[o][t][p] for t in range(1, T)) <= D[o][0][p] <= max(D[o][t][p] for t in range(1, T)))] for o in "AB"}
    bounds = {
        "family": "two quarter turns in mixed senses at widths 2-96, then or before a periodic tableau key",
        "sense_pairs": ["cw-ccw", "ccw-cw", "ccw-ccw"], "cw_cw_routes_skipped": n_cwcw,
        "distinct_routes": n_routes, "duplicates_skipped": n_dupes, "periods": [1, PMAX], "classes": 8,
        "k4_live_by_period": {o: live[o][0][1:] for o in "AB"},
        "controls_live_min": {o: [min(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in "AB"},
        "controls_live_max": {o: [max(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in "AB"},
        "k4_distinct_check_sets_by_period_to_24": {o: D[o][0][1:25] for o in "AB"},
        "controls_distinct_min": {o: [min(D[o][t][p] for t in range(1, T)) for p in range(1, 25)] for o in "AB"},
        "controls_distinct_max": {o: [max(D[o][t][p] for t in range(1, T)) for p in range(1, 25)] for o in "AB"},
        "periods_outside_by_settings": out_s, "periods_outside_by_distinct_check_sets": out_d,
        "k4_live_below_20": k4_low[:40], "n_k4_live_below_20": len(k4_low),
        "controls": f"{N_CONTROLS} shuffled coppers (seed 99), identical search",
    }
    notes = (f"{n_routes:,} new mixed-sense two-turn routes ({n_dupes:,} repeats and cw-cw routes skipped) x 8 classes x 2 orders, "
             f"periods 1-26. K4 live below 20: {len(k4_low)}. Outside the control range by settings: {out_s}; by distinct "
             f"check sets (periods up to 24): {out_d}.")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    a = where_of_turns([(9, "cw")]); b = where_of_turns([(12, "ccw")])
    lines = ["clockwise turn in rows of 9, then anticlockwise in rows of 12: where the first known letters go", "",
             "place  letter  after cw 9  after ccw 12  copper there"]
    for p in (22, 23, 24, 25, 64):
        x = a[p - 1]; y = b[x]
        lines.append(f"{p:>5}  {known[p]:>6}  {x + 1:>10}  {y + 1:>11}  {ct[y]:>12}")
    return "\n".join(lines)
