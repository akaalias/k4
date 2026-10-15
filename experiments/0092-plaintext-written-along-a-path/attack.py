"""Experiment 0092. See program.md for the contract."""

EXPERIMENT = {
    "slug": "plaintext-written-along-a-path",
    "title": "The message written into a grid along one path and read out along another (snake, spiral, diagonal), with a repeating key before or after",
    "family": "2-masked-plaintext",
    "parent": "0023-masks-reversal-and-nulls-then-tableau",
    "changed": "0023, 0057 and 0074 masked the message without moving letters across a grid. 0080-0083 moved them by K3's rule, quarter turns and column reading only. Here the message is written into a grid of width 2-96 along one of 30 hand paths (rows, snake rows, columns, snake columns, spirals from each corner either way, diagonals, snake diagonals, each forwards or backwards) and read out along another, 900 path pairs per width.",
    "hypothesis_expert": (
        "Type 4 of directions.md, open item 'plaintext written in boustrophedon, spiral or columns'. Scheidt: he 'masked "
        "the English language' before the keyed step (C2, C3); Sanborn: 'double matrixes... then went back to this "
        "table' (C1), visual systems (family 4). Grid of width w = 2-96 filled to 97 cells in row order, the last row "
        "short; a path is an order of its cells: rows, snake rows, columns, snake columns, spirals inward from each corner "
        "clockwise or anticlockwise, anti-diagonals and snake anti-diagonals, main diagonals, and each of these reversed (30 "
        "paths). Route: write along path X, read along path Y, X != Y; deduplicated with inverses. Key: one repeating key, "
        "period 1-26, after the move (slot = carved place mod p) or before it (slot = message place mod p), 8 consistency "
        "classes of the tableau (plain and cipher alphabets standard or KRYPTOS, Beaufort or not). Exact by slot "
        "agreement; ten shuffled coppers set the chance level per period."
    ),
    "hypothesis_eli5": (
        "One way to hide the shape of English is to write the message into a grid in an odd order, snaking back and "
        "forth, spiralling in from a corner, or along the diagonals, and then copy it out in another order. After that "
        "the letters go through the table with a short secret word. We try 30 such paths for writing and 30 for reading "
        "at every grid width, with secret words of up to 26 letters, and check each against the 24 known letters."
    ),
    "prediction": (
        "No route makes a repeating key of length 20 or less consistent; at every period the count of consistent "
        "(route, class) settings on K4 lies inside the range of the ten shuffled coppers, give or take one period by "
        "chance. Zero candidates."
    ),
    "method": (
        "1. For each width, build the grid's cells and the 30 paths. 2. For each pair of paths, compute where each message "
        "letter lands; drop repeats and inverses. 3. For each route and class, compute the key value forced at each known "
        "letter and test, for each period, whether known letters sharing a key slot agree, both orders. 4. Repeat on ten "
        "shuffled coppers. 5. List K4's settings consistent below period 20."
    ),
    "walkthrough": (
        "1. Write the message into rows of 10 letters, snaking: row 1 left to right, row 2 right to left, and so on. "
        "2. Read it out by columns, top to bottom. 3. Each known letter, say E at place 22, now sits at a new place j. "
        "4. With a secret word of length p after the move, the key letter at j is letter j mod p of the word; it must turn E into the carved letter at j. "
        "5. Known letters landing on the same key letter must agree. 6. Repeat for every pair of paths, width, word length up to 26 and table rule, and with the key used before the move."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
PMAX = 26
ALPH = {"std": STD, "kry": KRY}
N_CONTROLS = 10


def cells(w):
    return [(i // w, i % w) for i in range(N)]


def paths(w):
    """30 orders of the 97 cells of a width-w grid (last row short)."""
    cs = cells(w)
    have = set(cs)
    h = -(-N // w)
    out = {}
    out["rows"] = list(cs)
    out["snake rows"] = [(r, c if r % 2 == 0 else w - 1 - c) for r in range(h) for c in range(w) if (r, c if r % 2 == 0 else w - 1 - c) in have]
    out["columns"] = [(r, c) for c in range(w) for r in range(h) if (r, c) in have]
    out["snake columns"] = [(r if c % 2 == 0 else h - 1 - r, c) for c in range(w) for r in range(h) if (r if c % 2 == 0 else h - 1 - r, c) in have]

    def cw_spiral(hh, ww):
        top, bot, left, right = 0, hh - 1, 0, ww - 1
        seq = []
        while top <= bot and left <= right:
            for c in range(left, right + 1):
                seq.append((top, c))
            for r in range(top + 1, bot + 1):
                seq.append((r, right))
            if top < bot:
                for c in range(right - 1, left - 1, -1):
                    seq.append((bot, c))
            if left < right:
                for r in range(bot - 1, top, -1):
                    seq.append((r, left))
            top += 1; bot -= 1; left += 1; right -= 1
        return seq

    def spiral(corner, cw):
        # clockwise from the top-left goes right first; anticlockwise from the top-left goes down first (the transpose)
        fr, fc = corner
        base_cw = cw if fr == fc else not cw          # one mirror reverses the sense of turning, two do not
        seq = cw_spiral(h, w) if base_cw else [(r, c) for c, r in cw_spiral(w, h)]
        mapped = [((h - 1 - r) if fr else r, (w - 1 - c) if fc else c) for r, c in seq]
        return [x for x in mapped if x in have]
    for corner in ((0, 0), (0, 1), (1, 0), (1, 1)):
        for cw in (True, False):
            out[f"spiral {'bottom' if corner[0] else 'top'}-{'right' if corner[1] else 'left'} {'cw' if cw else 'ccw'}"] = spiral(corner, cw)
    out["anti-diagonals"] = sorted(cs, key=lambda x: (x[0] + x[1], x[0]))
    out["snake anti-diagonals"] = sorted(cs, key=lambda x: (x[0] + x[1], x[0] if (x[0] + x[1]) % 2 == 0 else -x[0]))
    out["diagonals"] = sorted(cs, key=lambda x: (x[1] - x[0], x[0]))
    for k in list(out):
        out[k + " reversed"] = out[k][::-1]
    for k, v in out.items():
        assert len(v) == N and len(set(v)) == N, (w, k)
    return out


def slot_pairs(slots):
    last, prs = {}, []
    for e, s in enumerate(slots):
        if s in last:
            prs.append((last[s], e))
        last[s] = e
    return prs


def route(write, read):
    """where[i]: place in the read-out text of message letter i."""
    pos = {cell: j for j, cell in enumerate(read)}
    return [pos[write[i]] for i in range(N)]


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    places = sorted(known)
    pidx = [p - 1 for p in places]
    rng = random.Random(92)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    T = len(texts)
    classes = [(pa, ca, beau) for pa in ALPH for ca in ALPH for beau in (False, True)]
    CI = {an: [[{c: i for i, c in enumerate(ALPH[an])}[ch] for ch in t] for t in texts] for an in ALPH}
    PI = {an: [{c: i for i, c in enumerate(ALPH[an])}[known[p]] for p in places] for an in ALPH}
    pairsB = {p: slot_pairs([i % p for i in pidx]) for p in range(1, PMAX + 1)}
    assert plant_check(known)
    live = {o: [[0] * (PMAX + 1) for _ in range(T)] for o in "AB"}
    k4_low, seen = [], set()
    n_routes = n_dupes = 0
    for w in range(2, N):
        P = paths(w)
        names = list(P)
        for a in names:
            for b in names:
                if a == b:
                    continue
                wh = route(P[a], P[b])
                inv = [0] * N
                for i, j in enumerate(wh):
                    inv[j] = i
                for d, r in (("", wh), (" inverse", inv)):
                    key = tuple(r)
                    if key in seen or key == tuple(range(N)):
                        n_dupes += 1
                        continue
                    seen.add(key)
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
                                    k4_low.append({"width": w, "write": a, "read": b + d, "order": o,
                                                   "class": f"{pa}/{ca}/{'beau' if beau else 'vig-var'}", "period": first})
    outside = {o: [p for p in range(1, PMAX + 1)
                   if not (min(live[o][t][p] for t in range(1, T)) <= live[o][0][p] <= max(live[o][t][p] for t in range(1, T)))]
               for o in "AB"}
    bounds = {
        "family": "write along one of 30 grid paths, read along another, widths 2-96, then or before a periodic tableau key",
        "paths": 30, "widths": [2, 96], "distinct_routes": n_routes, "duplicates_skipped": n_dupes,
        "periods": [1, PMAX], "classes": 8,
        "k4_live_by_period": {o: live[o][0][1:] for o in "AB"},
        "controls_live_by_period_min": {o: [min(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in "AB"},
        "controls_live_by_period_max": {o: [max(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in "AB"},
        "periods_outside_control_range": outside,
        "k4_live_below_20": k4_low[:40], "n_k4_live_below_20": len(k4_low),
        "controls": f"{N_CONTROLS} shuffled coppers (seed 92), identical search",
        "order_A": "move, then key (slot = carved place mod p)", "order_B": "key, then move (slot = message place mod p)",
    }
    notes = (f"{n_routes:,} distinct path-pair routes ({n_dupes:,} repeats skipped) x 8 classes x 2 orders, periods 1-26. "
             f"K4 live below period 20: {len(k4_low)}. Periods where K4 is outside the control range: {outside}.")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def plant_check(known):
    """A planted text written in snake rows of 10 and read by columns, then a period-11 key, must pass."""
    rng = random.Random(5)
    pt = [rng.choice(STD) for _ in range(N)]
    for p, c in known.items():
        pt[p - 1] = c
    P = paths(10)
    wh = route(P["snake rows"], P["columns"])
    moved = [""] * N
    for i in range(N):
        moved[wh[i]] = pt[i]
    key = [rng.randrange(26) for _ in range(11)]
    I = {c: i for i, c in enumerate(KRY)}
    ctxt = [KRY[(I[ch] + key[j % 11]) % 26] for j, ch in enumerate(moved)]
    slots = {}
    for p in known:
        j = wh[p - 1]
        v = (I[ctxt[j]] - I[known[p]]) % 26
        if slots.setdefault(j % 11, v) != v:
            return False
    return True


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    P = paths(10)
    wh = route(P["snake rows"], P["columns"])
    lines = ["write in snake rows of 10, read by columns: where the first known letters land", "",
             "place  letter  grid cell (row, col)  lands at  copper there"]
    for p in (22, 23, 24, 25, 64):
        r, c = P["snake rows"][p - 1]
        lines.append(f"{p:>5}  {known[p]:>6}  {f'({r + 1}, {c + 1})':>20}  {wh[p - 1] + 1:>8}  {ct[wh[p - 1]]:>12}")
    return "\n".join(lines)
