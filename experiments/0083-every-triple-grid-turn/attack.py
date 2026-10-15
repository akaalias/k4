"""Experiment 0083. See program.md for the contract."""

EXPERIMENT = {
    "slug": "every-triple-grid-turn",
    "title": "Three grid turns in a row at every width, then (or before) a repeating key: the triple matrix, exhaustively",
    "family": "6-transposition-then-tableau",
    "parent": "0037-triple-matrix-routes-sampled-then-tableau",
    "changed": "0037 sampled 200,000 of about 9.4 million triples of stages up to width 30 and scored the forced key as English. Here the triple is K3's own move, a quarter turn, three times, at every width from 2 to 96 in each grid: all 857,375 width triples, forward and inverse, with the exact crib test for a repeating key of length 1-26 on either side of the move.",
    "hypothesis_expert": (
        "Type 1 of directions.md, gap a4 of the prior-work database ('exhaustive triple rotation + tableau: every public "
        "search stops at two stages; 0037 only sampled'). Clue C1(a) (02-sanborn-said.md, CNN 2005: 'sometimes I used "
        "double matrixes and triple matrixes... and then went back to this table to do the ultimate') read literally: "
        "three quarter turns, the K3 move (C2(a); the NSA's double rotation for K3), then the tableau. A turn writes the "
        "text in rows of w (ragged last row) and reads columns bottom-up, left column first. Routes: turn(w3) . turn(w2) . "
        "turn(w1), w1, w2, w3 = 2-96 each (857,375), forward and inverse, deduplicated by a hash of the permutation. Key: "
        "periodic tableau key of period 1-26 after the move (slot = landing place mod p, order A) or before it (slot = "
        "place mod p, order B), 8 distinct classes of plain and cipher alphabet and Beaufort-or-not; a period is live if "
        "no two known letters in one slot force different key letters. Exact; ten shuffled coppers through the identical "
        "search. Left open: triples mixing turns with columnar or keyed stages beyond 0037's sample; anticlockwise turns; "
        "keys longer than 26."
    ),
    "hypothesis_eli5": (
        "Sanborn said he 'sometimes used double matrixes and triple matrixes' and then went back to the table. The third "
        "message was made by writing the letters in a grid and turning it; doing that twice gives the NSA's reading of "
        "it. Three times has never been tried in full. We turn the grid three times, at every possible width each time, "
        "and then ask whether a repeating secret word of up to 26 letters on the table could give the copper's known "
        "letters, with the word applied either after the turns or before them."
    ),
    "prediction": (
        "As for one and two turns (0008) and the sample of triples (0037, smallest live period 20 once, otherwise 23 and "
        "up): no period below 20 is live on K4 beyond the rate on the shuffled coppers, and the count of live settings at "
        "each period 1-26 lies inside the control range, give or take the spread at 25-26. Zero candidates."
    ),
    "method": (
        "1. Compute the quarter-turn permutation once for every width 2-96. 2. Compose every triple, forward and inverse, "
        "and skip repeats. 3. For each route, class and text, compute the key letter each known letter forces at its "
        "landing place. 4. For each period 1-26 and each order, the period is live if no slot holds two different forced "
        "letters. 5. Count live settings per period on K4 and on ten shuffled coppers. 6. List K4's live settings below "
        "period 20."
    ),
    "walkthrough": (
        "1. Write the message in rows of 7 and turn the grid a quarter clockwise: read each column from the bottom up, left column first. The E at place 22 comes out at place 11. 2. Write the result in rows of 9 and turn again: place 11 is in row 1, column 1; column 0 gives 11 letters and column 1 read from the bottom reaches row 1 at its tenth letter, so the E is now at 21. 3. Rows of 13, turn a third time: the E lands at 61, where the copper has N. 4. A repeating key on the table after the turns must turn E into N at place 61; work out that key letter for all 24 known letters. 5. For a key of length p, two known letters whose landing places differ by a multiple of p share a key letter; if they need different ones, p is dead. 6. Repeat for every width triple, both directions, the key before or after the turns, and on ten scrambled coppers."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.alphabets import numeric_order

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


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    places = sorted(known)
    pidx = [p - 1 for p in places]
    rng = random.Random(83)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    T = len(texts)
    classes = [(pa, ca, beau) for pa in ALPH for ca in ALPH for beau in (False, True)]
    CI = {an: [[{c: i for i, c in enumerate(ALPH[an])}[ch] for ch in t] for t in texts] for an in ALPH}
    PI = {an: [{c: i for i, c in enumerate(ALPH[an])}[known[p]] for p in places] for an in ALPH}
    pairsB = {p: slot_pairs([i % p for i in pidx]) for p in range(1, PMAX + 1)}
    TP = {w: turn_perm(w) for w in range(2, N)}
    assert plant_check(known, TP)
    # self-check: composing where-maps equals applying the turns in sequence
    s = list(range(N))
    for w in (7, 9, 13):
        s = turn(s, w, False, "cw")
    comp = [TP[13][TP[9][TP[7][i]]] for i in range(N)]
    assert all(s[comp[i]] == i for i in range(N))

    live = {o: [[0] * (PMAX + 1) for _ in range(T)] for o in "AB"}
    minp = {o: [dict() for _ in range(T)] for o in "AB"}
    k4_low, seen = [], set()
    n_routes = n_dupes = 0
    stopped = None
    for w1 in range(2, N):
        if stopped:
            break
        A1 = TP[w1]
        for w2 in range(2, N):
            if ctx.time_left() < 60:
                stopped = (w1, w2)
                break
            A2 = TP[w2]
            m12 = [A2[A1[i]] for i in range(N)]
            for w3 in range(2, N):
                A3 = TP[w3]
                fwd = [A3[m12[i]] for i in range(N)]
                inv = [0] * N
                for i, j in enumerate(fwd):
                    inv[j] = i
                for d, wh in (("fwd", fwd), ("inv", inv)):
                    h = hash(tuple(wh))
                    if h in seen:
                        n_dupes += 1
                        continue
                    seen.add(h)
                    n_routes += 1
                    land = [wh[i] for i in pidx]
                    pairsA = {p: slot_pairs([j % p for j in land]) for p in range(1, PMAX + 1)}
                    for pa, ca, beau in classes:
                        P = PI[pa]
                        for t in range(T):
                            C = CI[ca][t]
                            f = [(C[j] + P[e]) % 26 if beau else (C[j] - P[e]) % 26 for e, j in enumerate(land)]
                            for o, prs_by in (("A", pairsA), ("B", pairsB)):
                                first = None
                                L = live[o][t]
                                for p in range(1, PMAX + 1):
                                    for a, b in prs_by[p]:
                                        if f[a] != f[b]:
                                            break
                                    else:
                                        L[p] += 1
                                        if first is None:
                                            first = p
                                mp = first or 0
                                minp[o][t][mp] = minp[o][t].get(mp, 0) + 1
                                if t == 0 and first is not None and first < 20:
                                    k4_low.append({"widths": [w1, w2, w3], "dir": d, "order": o,
                                                   "class": f"{pa}/{ca}/{'beau' if beau else 'vig-var'}", "period": first})
    outside = {}
    for o in "AB":
        outside[o] = [p for p in range(1, PMAX + 1) if not (min(live[o][t][p] for t in range(1, T)) <= live[o][0][p] <= max(live[o][t][p] for t in range(1, T)))]
    ctl_low = {o: [sum(v for p, v in minp[o][t].items() if 0 < p < 20) for t in range(1, T)] for o in "AB"}
    bounds = {
        "family": "three clockwise quarter turns at widths 2-96 each, then or before a periodic tableau key",
        "width_triples": 95 ** 3, "distinct_routes": n_routes, "duplicates_skipped": n_dupes,
        "stopped_at": stopped, "periods": [1, PMAX], "classes": 8,
        "k4_live_by_period": {o: live[o][0][1:] for o in "AB"},
        "controls_live_by_period_min": {o: [min(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in "AB"},
        "controls_live_by_period_max": {o: [max(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in "AB"},
        "k4_smallest_live_period_histogram": {o: dict(sorted(minp[o][0].items())) for o in "AB"},
        "periods_outside_control_range": outside,
        "k4_live_below_20": k4_low[:40], "n_k4_live_below_20": len(k4_low), "controls_live_below_20": ctl_low,
        "controls": f"{N_CONTROLS} shuffled coppers (seed 83), identical search",
        "order_A": "turns, then key (slot = landing place mod p)", "order_B": "key, then turns (slot = place mod p)",
    }
    notes = (f"{n_routes:,} distinct triple-turn routes ({n_dupes:,} repeats skipped) x 8 classes x 2 orders, periods 1-26. "
             f"K4 live below period 20: {len(k4_low)}; controls: {ctl_low}. Periods where K4 is outside the control range: "
             f"{outside}." + (f" Stopped at widths {stopped} for time." if stopped else ""))
    return {"candidates": [], "bounds": bounds, "notes": notes}


def plant_check(known, TP):
    rng = random.Random(5)
    pt = [rng.choice(STD) for _ in range(N)]
    for p, c in known.items():
        pt[p - 1] = c
    wh = [TP[11][TP[5][TP[8][i]]] for i in range(N)]
    moved = [""] * N
    for i in range(N):
        moved[wh[i]] = pt[i]
    key = [rng.randrange(26) for _ in range(13)]
    I = {c: i for i, c in enumerate(KRY)}
    ctxt = [KRY[(I[ch] + key[j % 13]) % 26] for j, ch in enumerate(moved)]
    slots = {}
    for p in known:
        j = wh[p - 1]
        v = (I[ctxt[j]] - I[known[p]]) % 26
        if slots.setdefault(j % 13, v) != v:
            return False
    return True


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    TP = {w: turn_perm(w) for w in (7, 9, 13)}
    lines = ["three clockwise quarter turns at widths 7, 9, 13: where the first known letters go", "",
             "place  letter  after 7  after 9  after 13  copper there"]
    for p in (22, 23, 24, 64, 65):
        a = TP[7][p - 1]; b = TP[9][a]; c = TP[13][b]
        lines.append(f"{p:>5}  {known[p]:>6}  {a + 1:>7}  {b + 1:>7}  {c + 1:>8}  {ct[c]:>12}")
    return "\n".join(lines)
