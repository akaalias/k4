"""Experiment 0159 (F6.5). See program.md for the contract."""

EXPERIMENT = {
    "slug": "compass-directions-as-reading-routes",
    "title": "F6.5: the message written in rows and read off along a compass direction (each of the 16 points, and east then east-northeast or northeast in two stages), then or before a repeating key on the table",
    "family": "6-transposition-then-tableau",
    "parent": "0134-mixed-matrix-readings-two-and-three-stages",
    "changed": (
        "F6.5 (added 2026-10-16, A14(a)). The known words are directions; read as instructions (C16(c)), they could name "
        "the route by which the grid is copied out. Routes: the 97 letters written in rows of w (2-96), read along lines "
        "parallel to one of the 16 compass points (the eight half-points as steps of one row and two columns), lines taken "
        "in either order; and two such stages in sequence for every ordered pair of E, ENE and NE at widths 2-48 ('east, "
        "then northeast'). Forward and inverse. Then a periodic key 1-26 on the standard or KRYPTOS tables in either order, "
        "decided exactly as 0134, against ten scrambled coppers."
    ),
    "hypothesis_expert": (
        "C16(c) ('The final passage will lead in several directions. The word directions is, I use intentionally', 2010, "
        "knowledge/sources/nyt-2010-berlin-clue.txt), C1(a) (rows written, columns read: the matrix code, "
        "knowledge/sources/cnn-2005-sanborn-interview-transcript.txt), C3(a) (spatial systems). Route: cell (r, c) holds "
        "message place r w + c; direction (dr, dc) in {N (-1,0), NNE (-2,1), NE (-1,1), ENE (-1,2), E (0,1), ESE (1,2), SE "
        "(1,1), SSE (2,1), S, SSW, SW, WSW, W, WNW, NW, NNW (negatives)}; lines are the classes of dc r - dr c, read in "
        "increasing projection dr r + dc c, lines in increasing or decreasing class. Singles: 16 x 2 x widths 2-96. "
        "Doubles: (E, ENE, NE)^2 ordered x line orders x widths 2-48 each. Forward and inverse, duplicates removed. Key: "
        "periodic tableau 1-26 after (A) or before (B), 8 classes; a period is live if no slot holds two different forced "
        "letters. Statistic fixed before the run (0134's): cells where K4's live count is above every copper's, against "
        "each copper's count against the rest."
    ),
    "hypothesis_eli5": (
        "The two clue words are directions: east, northeast. Perhaps they also say how the letters were moved: write the "
        "message in rows, then copy it out travelling east-northeast across the grid, or any other compass direction. We "
        "try every compass direction, every row width, and two-step versions (east, then northeast), each followed or "
        "preceded by a repeating secret word on the sculpture's tables, and check them against the 24 known letters and "
        "scrambled copies of the carved text."
    ),
    "prediction": (
        "As in 0134: nothing live below key length 20 beyond the coppers' rate; K4 above every copper in no more cells "
        "than the most any copper manages against the rest. Zero candidates."
    ),
    "method": (
        "1. Build every route: singles and doubles as stated, forward and inverse; remove duplicates. "
        "2. For each route, class and text, the key letter each known letter forces at its slot (order A: landing place "
        "mod p; order B: message place mod p). "
        "3. Count live periods 1-26 per order on K4 and ten coppers; list K4's settings live below 20. "
        "4. Compare cell by cell with the fixed statistic."
    ),
    "walkthrough": (
        "1. Write the 97 letters in rows of 10. "
        "2. Travel east-northeast: one row up, two columns right. Every line of cells in that direction is read from its lower-left end. "
        "3. Take the lines in order, starting from the top-left corner, and copy each out: that is the moved text. "
        "4. Note where each of the 24 known letters lands and the carved letter there. "
        "5. With a key of length p on the table, two known letters landing a multiple of p apart must force the same key letter. "
        "6. Repeat for every direction, width and order, the key before or after, and on scrambled copies."
    ),
}

import random
import time
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
PMAX = 26
ALPH = {"std": STD, "kry": KRY}
N_CONTROLS = 10
WORKERS = 8
DIRS = {"N": (-1, 0), "NNE": (-2, 1), "NE": (-1, 1), "ENE": (-1, 2), "E": (0, 1), "ESE": (1, 2), "SE": (1, 1), "SSE": (2, 1),
        "S": (1, 0), "SSW": (2, -1), "SW": (1, -1), "WSW": (1, -2), "W": (0, -1), "WNW": (-1, -2), "NW": (-1, -1), "NNW": (-2, -1)}
PAIR_DIRS = ("E", "ENE", "NE")
W1MAX, W2MAX = 96, 48


def reading(n, w, d, rev):
    """Message places in the order read: rows of w, lines parallel to direction d, lines by class (rev: descending)."""
    dr, dc = DIRS[d]
    cells = [(i // w, i % w, i) for i in range(n)]
    lines = {}
    for r, c, i in cells:
        lines.setdefault(dc * r - dr * c, []).append((dr * r + dc * c, i))
    out = []
    for key in sorted(lines, reverse=rev):
        out.extend(i for _, i in sorted(lines[key]))
    return out


def where(seq):
    wh = [0] * len(seq)
    for j, i in enumerate(seq):
        wh[i] = j
    return wh


def stage_text(s, w, d, rev):
    return [s[i] for i in reading(len(s), w, d, rev)]


def all_routes():
    routes = {}
    for d in DIRS:
        for rev in (False, True):
            for w in range(2, W1MAX + 1):
                wh = where(reading(N, w, d, rev))
                routes.setdefault(tuple(wh), ("single", d, rev, w))
    for d1 in PAIR_DIRS:
        for d2 in PAIR_DIRS:
            for r1 in (False, True):
                for r2 in (False, True):
                    for w1 in range(2, W2MAX + 1):
                        a = where(reading(N, w1, d1, r1))
                        for w2 in range(2, W2MAX + 1):
                            b = where(reading(N, w2, d2, r2))
                            routes.setdefault(tuple(b[a[i]] for i in range(N)), ("double", d1, r1, w1, d2, r2, w2))
    out = []
    seen = set()
    for wh, name in routes.items():
        for dirn, m in (("fwd", wh), ("inv", tuple(where(list(wh))))):
            if m in seen:
                continue
            seen.add(m)
            out.append((name, dirn, m))
    return out


def slot_pairs(slots):
    last, prs = {}, []
    for e, s in enumerate(slots):
        if s in last:
            prs.append((last[s], e))
        last[s] = e
    return prs


def count(args):
    routes, texts, known_list = args
    T = len(texts)
    classes = [(pa, ca, beau) for pa in ALPH for ca in ALPH for beau in (False, True)]
    CI = {an: [[ALPH[an].index(ch) for ch in t] for t in texts] for an in ALPH}
    PI = {an: [ALPH[an].index(a) for _, a in known_list] for an in ALPH}
    pidx = [qq - 1 for qq, _ in known_list]
    pairsB = {p: slot_pairs([i % p for i in pidx]) for p in range(1, PMAX + 1)}
    live = {o: [[0] * (PMAX + 1) for _ in range(T)] for o in "AB"}
    low = {o: [0] * T for o in "AB"}
    k4_low = []
    for name, d, wh in routes:
        land = [wh[i] for i in pidx]
        pairsA = {p: slot_pairs([j % p for j in land]) for p in range(1, PMAX + 1)}
        for pa, ca, beau in classes:
            P = PI[pa]
            for t in range(T):
                C = CI[ca][t]
                f = [(C[j] + P[e]) % 26 if beau else (C[j] - P[e]) % 26 for e, j in enumerate(land)]
                for o, prs_by in (("A", pairsA), ("B", pairsB)):
                    first_live = None
                    Lc = live[o][t]
                    for p in range(1, PMAX + 1):
                        for a, b in prs_by[p]:
                            if f[a] != f[b]:
                                break
                        else:
                            Lc[p] += 1
                            if first_live is None:
                                first_live = p
                    if first_live is not None and first_live < 20:
                        low[o][t] += 1
                        if t == 0:
                            k4_low.append({"route": list(map(str, name)), "dir": d, "order": o,
                                           "class": f"{pa}/{ca}/{'beau' if beau else 'vig-var'}", "period": first_live})
    return {"live": live, "low": low, "k4_low": k4_low}


def run(ctx):
    import multiprocessing as mp
    import sys
    import types
    ct, known = ctx.K4, ctx.KNOWN
    known_list = [(qq, known[qq]) for qq in sorted(known)]
    # the composed where-map must equal running the stages in sequence
    pt = [chr(65 + random.Random(5).randrange(26)) for _ in range(N)]
    a, b = where(reading(N, 10, "E", False)), where(reading(N, 7, "ENE", True))
    moved = [""] * N
    for i in range(N):
        moved[b[a[i]]] = pt[i]
    assert stage_text(stage_text(pt, 10, "E", False), 7, "ENE", True) == moved
    assert reading(N, 10, "E", False) == list(range(N))
    routes = all_routes()
    rng = random.Random(1365)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    T = len(texts)
    shares = [(routes[i::WORKERS], texts, known_list) for i in range(WORKERS)]
    if getattr(sys.modules.get(__name__), "count", None) is not count:
        m = types.ModuleType(__name__); m.__dict__.update(globals()); sys.modules[__name__] = m
    with mp.get_context("fork").Pool(WORKERS) as pool:
        parts = pool.map(count, shares, chunksize=1)
    live = {o: [[sum(pt_["live"][o][t][p] for pt_ in parts) for p in range(PMAX + 1)] for t in range(T)] for o in "AB"}
    low = {o: [sum(pt_["low"][o][t] for pt_ in parts) for t in range(T)] for o in "AB"}
    k4_low = [x for pt_ in parts for x in pt_["k4_low"]]
    cells = [(o, p) for o in "AB" for p in range(1, PMAX + 1)]

    def above_rest(t):
        return [(o, p) for o, p in cells if live[o][t][p] > max(live[o][u][p] for u in range(T) if u != t)]
    k4_above = above_rest(0)
    null_above = [len(above_rest(t)) for t in range(1, T)]
    stop = len(k4_above) > max(null_above)
    first = {o: next((p for p in range(1, PMAX + 1) if live[o][0][p]), None) for o in "AB"}
    cfirst = {o: min(next((p for p in range(1, PMAX + 1) if live[o][t][p]), 99) for t in range(1, T)) for o in "AB"}
    bounds = {
        "family": "compass-direction reading routes (16 points, either line order, widths 2-96; E/ENE/NE pairs at widths 2-48), then or before a periodic tableau key",
        "directions": {k: list(v) for k, v in DIRS.items()},
        "distinct_routes": len(routes), "periods": [1, PMAX], "classes": 8,
        "k4_live_by_period": {o: live[o][0][1:] for o in "AB"},
        "controls_live_by_period_min": {o: [min(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in "AB"},
        "controls_live_by_period_max": {o: [max(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in "AB"},
        "k4_shortest_live": first, "coppers_shortest_live": cfirst,
        "k4_settings_live_below_20": {o: low[o][0] for o in "AB"}, "controls_settings_live_below_20": {o: low[o][1:] for o in "AB"},
        "k4_live_below_20": sorted(k4_low, key=lambda x: x["period"])[:40],
        "cells_k4_above_every_copper": k4_above, "null_cells_above_rest_per_copper": null_above, "stop_queue": stop,
        "controls": f"{N_CONTROLS} shuffled coppers (seed 1365), identical search",
        "exhaustive": True,
    }
    notes = (f"{len(routes):,} distinct routes x 8 classes x 2 orders, periods 1-26. Shortest live on K4: A {first['A']}, B {first['B']}; "
             f"coppers A {cfirst['A']}, B {cfirst['B']}. K4 settings live below 20: A {low['A'][0]}, B {low['B'][0]}. "
             f"K4 above every copper in {len(k4_above)} of 52 cells; null {min(null_above)}-{max(null_above)}. Stop queue: {stop}.")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    """key: {'stages': [(w, direction, rev), ...], 'order': 'A' or 'B', 'alphabet': 'STD'/'KRY', 'key': shifts}."""
    alpha = KRY if key["alphabet"] == "KRY" else STD
    k = key["key"]

    def table(s):
        return "".join(alpha[(alpha.index(ch) + k[i % len(k)]) % 26] for i, ch in enumerate(s))

    def move(s):
        s = list(s)
        for w, d, rev in key["stages"]:
            s = stage_text(s, w, d, rev)
        return "".join(s)
    return table(move(plaintext)) if key["order"] == "A" else move(table(plaintext))


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    seq = reading(N, 10, "ENE", False)
    wh = where(seq)
    lines = ["rows of 10, read east-northeast (one row up, two columns right), lines from the top-left corner", "",
             "first 20 message places read: " + " ".join(str(i + 1) for i in seq[:20]), "",
             "place  letter  lands at  copper there"]
    for q in (22, 23, 24, 64, 65, 74):
        lines.append(f"{q:5d}  {known[q]:>6}  {wh[q - 1] + 1:8d}  {ct[wh[q - 1]]:>12}")
    return "\n".join(lines)
