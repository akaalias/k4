"""Experiment 0135. See program.md for the contract."""

EXPERIMENT = {
    "slug": "hand-padding-at-every-grid-stage",
    "title": "Hand padding at each grid stage: the blank cells in any of eight places, dropped or carried as fillers into the next grid, one or two stages, then or before a repeating key on the table",
    "family": "6-transposition-then-tableau",
    "parent": "0082-where-the-blanks-go-in-the-grid",
    "changed": (
        "F6.4 (padding applied separately at each grid stage; nulls dropped between griddings). 0082 tried blanks at the "
        "start of the first row or the end of the last, and carried as fillers, for one and two clockwise turns and "
        "short-row-on-top columnar. The list of hand rules (NOTEBOOK 2026-10-16) adds six places for the blank cells: "
        "start of the last row, end of the first row, and down the first or last column from the top or from the "
        "bottom; each grid of a two-stage move chooses its own place, its own reading (clockwise turn, or Sanborn's "
        "rows-then-columns-down) and whether the first grid's blanks vanish or travel as filler letters to be struck "
        "out at the end. One stage: 8 places x 4 readings x widths 2-96. Two stages: (8 places x 2 readings x widths "
        "2-48)^2 x drop or keep."
    ),
    "hypothesis_expert": (
        "C1(a) (Sanborn, CNN 2005, knowledge/sources/cnn-2005-sanborn-interview-transcript.txt: 'you write a line of "
        "plain text out, right, in successive rows. And then basically you write it going from top to bottom... double "
        "matrixes and triple matrixes'), C2(a), C17(b) ('whether it's 97, whether it's 100... I seem to like to "
        "manipulate the information'). 97 is prime, so every hand grid has h w - 97 blank cells; research note "
        "combined_methods_and_sevens.md: classical practice leaves the last row short, completes with nulls, or fixes "
        "blank cells; every coded search pads once at the ends (gap 6: per-stage padding). Places for b blanks: end of "
        "the last row (P1, covered by 0008), start of the first row (P2, 0082), start of the last row (P3), end of the "
        "first row (P4), last column from the top (P5) or bottom (P6), first column from the top (P7) or bottom (P8); "
        "column places need b <= h. Readings: cw (left column first, bottom up: the K3 turn), col (left first, top "
        "down: Sanborn's matrix code); for one stage also ccw and colr. Keep mode: the first grid's blank cells are read "
        "out as filler letters and fill cells of the second grid, all fillers struck out at the end. Key: periodic "
        "tableau 1-26 after (order A) or before (order B) the move, 8 classes of standard/KRYPTOS plain and cipher "
        "alphabets and Beaufort-or-not; a period is live if no slot holds two different forced key letters. Exact; ten "
        "scrambled coppers."
    ),
    "hypothesis_eli5": (
        "97 letters never fill a grid exactly, so a person writing them in rows leaves a few empty squares somewhere: at "
        "the end, at the start, or down one side. With two grids, the empty squares of the first can disappear or be "
        "copied along as dummy letters and crossed out at the end. We try every such choice, for one and two grids, "
        "each followed or preceded by a repeating secret word on the sculpture's tables, and check them against the 24 "
        "known letters and scrambled copies of the carved text."
    ),
    "prediction": (
        "As in 0082 and 0083: nothing live below period 20 beyond the coppers' rate, and K4 above every copper in no more "
        "(order, period) cells than the most any single copper manages against the rest. A K4 count beyond that null "
        "stops the queue for a replication. Zero candidates."
    ),
    "method": (
        "1. For every width, reading and place of the blanks, the where-map of one stage (keep mode: fillers counted). "
        "2. Compose every pair at widths 2-48 (both readings, all places, drop or keep), forward and inverse; skip repeats. "
        "3. For each route, class and text, the key letter each known letter forces at its slot. "
        "4. Period p (1-26) is live in an order if no slot holds two different forced letters. "
        "5. Count live settings per period on K4 and ten scrambled coppers; compare cell by cell; list K4's live settings below 20."
    ),
    "walkthrough": (
        "1. Write the 97 letters in rows of 8: 13 rows hold 104 squares, so 7 stay empty; leave them at the bottom of the last column and the six above it (place P6). "
        "2. Read the columns left first, top to bottom (Sanborn's matrix), and copy each empty square out as a dummy letter (keep): 104 symbols, the E of place 22 now 68th among the real letters. "
        "3. (In drop mode the empty squares are simply skipped.) "
        "4. Write the 104 symbols in rows of 9: 12 rows hold 108 squares, so leave the first 4 squares of the top row empty (P2); read the columns from the bottom up, left first (a quarter turn), and strike out every dummy: the E lands at place 90, where the copper has U. "
        "5. Note where each known letter has landed and the carved letter there; with a key of length p on the table, two known letters in one slot must force the same key letter. "
        "6. Repeat for every place, reading, width, drop or keep, the key before or after, and on scrambled copies."
    ),
}

import random
import time
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
PMAX = 26
ALPH = {"std": STD, "kry": KRY}
N_CONTROLS = 10
READINGS = ("cw", "ccw", "col", "colr")
R2 = ("cw", "col")
W2MAX = 48
WORKERS = 5


NULL = -1
PLACES = ("P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8")


def blank_cells(n, w, place):
    """Set of (row, col) left empty when n tokens are written in rows of w, or None if the place cannot hold them."""
    h = -(-n // w)
    b = h * w - n
    if b == 0:
        return set()
    if place == "P1":
        return {(h - 1, c) for c in range(w - b, w)}
    if place == "P2":
        return {(0, c) for c in range(b)}
    if place == "P3":
        return {(h - 1, c) for c in range(b)}
    if place == "P4":
        return {(0, c) for c in range(w - b, w)}
    if b > h:
        return None
    col = w - 1 if place in ("P5", "P6") else 0
    rows = range(b) if place in ("P5", "P7") else range(h - b, h)
    return {(r, col) for r in rows}


def stage(tokens, w, r, place="P1", keep=False):
    """Write tokens in rows of w around the blank cells, read the columns (cw: left first, bottom up; ccw: right
    first, top down; col: left first, top down; colr: right first, bottom up). keep: blanks come out as NULL."""
    n = len(tokens)
    h = -(-n // w)
    blanks = blank_cells(n, w, place)
    if blanks is None:
        return None
    grid, it = {}, iter(tokens)
    for rr in range(h):
        for c in range(w):
            if (rr, c) not in blanks:
                grid[(rr, c)] = next(it)
    cols = range(w) if r in ("cw", "col") else range(w - 1, -1, -1)
    rows = range(h - 1, -1, -1) if r in ("cw", "colr") else range(h)
    out = []
    for c in cols:
        for rr in rows:
            if (rr, c) in grid:
                out.append(grid[(rr, c)])
            elif keep:
                out.append(NULL)
    return out


def where_from(order_tokens):
    """where-map (carved place of each message place) from the final token order, fillers struck out."""
    seq = [t for t in order_tokens if t != NULL]
    wh = [0] * N
    for j, i in enumerate(seq):
        wh[i] = j
    return wh


def slot_pairs(slots):
    last, prs = {}, []
    for e, s in enumerate(slots):
        if s in last:
            prs.append((last[s], e))
        last[s] = e
    return prs


def routes_for(first):
    """first = (r1, place1, w1). One stage alone (every reading), then two stages at widths 2-48 with readings cw/col,
    every place, drop or keep."""
    r1, p1, w1 = first
    s1 = stage(list(range(N)), w1, r1, p1)
    if s1 is not None:
        yield (r1, p1, w1), where_from(s1)
    if w1 > W2MAX or r1 not in R2:
        return
    for keep in (False, True):
        s1k = stage(list(range(N)), w1, r1, p1, keep)
        if s1k is None:
            continue
        for r2 in R2:
            for p2 in PLACES:
                for w2 in range(2, W2MAX + 1):
                    s2 = stage(s1k, w2, r2, p2)
                    if s2 is not None:
                        yield (r1, p1, w1, "keep" if keep else "drop", r2, p2, w2), where_from(s2)


def count(firsts, texts, known_list, deadline, q):
    T = len(texts)
    classes = [(pa, ca, beau) for pa in ALPH for ca in ALPH for beau in (False, True)]
    CI = {an: [[ALPH[an].index(ch) for ch in t] for t in texts] for an in ALPH}
    PI = {an: [ALPH[an].index(a) for _, a in known_list] for an in ALPH}
    pidx = [qq - 1 for qq, _ in known_list]
    pairsB = {p: slot_pairs([i % p for i in pidx]) for p in range(1, PMAX + 1)}
    live = {o: [[0] * (PMAX + 1) for _ in range(T)] for o in "AB"}
    low = {o: [0] * T for o in "AB"}
    k4_low = []
    n_routes = n_dupes = 0
    done_firsts = []
    for first in firsts:
        if time.time() > deadline:
            break
        seen = set()
        for name, fwd in routes_for(first):
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
                                    k4_low.append({"route": name, "dir": d, "order": o,
                                                   "class": f"{pa}/{ca}/{'beau' if beau else 'vig-var'}", "period": first_live})
        done_firsts.append(first)
    q.put({"live": live, "low": low, "k4_low": k4_low, "n_routes": n_routes, "n_dupes": n_dupes, "done": done_firsts})


def plant_ok(known_list):
    """A planted text (col 8 P6 keep, then cw 9 P2, then a KRYPTOS-table key of length 11) must leave period 11 live in
    order A, and encrypt() must reproduce it."""
    rng = random.Random(5)
    pt = [rng.choice(STD) for _ in range(N)]
    for qq, a in known_list:
        pt[qq - 1] = a
    wh = where_from(stage(stage(list(range(N)), 8, "col", "P6", True), 9, "cw", "P2"))
    moved = [""] * N
    for i in range(N):
        moved[wh[i]] = pt[i]
    key = [rng.randrange(26) for _ in range(11)]
    ctxt = "".join(KRY[(KRY.index(ch) + key[j % 11]) % 26] for j, ch in enumerate(moved))
    slots = {}
    for qq, a in known_list:
        j = wh[qq - 1]
        v = (KRY.index(ctxt[j]) - KRY.index(a)) % 26
        if slots.setdefault(j % 11, v) != v:
            return False
    k = {"stages": [(8, "col", "P6", True), (9, "cw", "P2", False)], "order": "A", "alphabet": "KRY", "key": key}
    return encrypt("".join(pt), k) == ctxt


def run(ctx):
    import multiprocessing as mp
    ct, known = ctx.K4, ctx.KNOWN
    known_list = [(qq, known[qq]) for qq in sorted(known)]
    assert plant_ok(known_list)
    rng = random.Random(134)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    firsts = [(r, p, w) for w in range(2, N) for r in READINGS for p in PLACES]
    # heavy first stages (cw/col at w <= 48 carry the doubles) spread evenly
    heavy = [f for f in firsts if f[2] <= W2MAX and f[0] in R2]; light = [f for f in firsts if f not in heavy]
    rng.shuffle(heavy); rng.shuffle(light)
    order = heavy + light
    deadline = time.time() + ctx.time_left() - 90
    mpc = mp.get_context("fork")
    q = mpc.Queue()
    procs = [mpc.Process(target=count, args=(order[i::WORKERS], texts, known_list, deadline, q)) for i in range(WORKERS)]
    for p in procs:
        p.start()
    parts = [q.get() for _ in procs]
    for p in procs:
        p.join()
    T = len(texts)
    live = {o: [[sum(pt["live"][o][t][p] for pt in parts) for p in range(PMAX + 1)] for t in range(T)] for o in "AB"}
    low = {o: [sum(pt["low"][o][t] for pt in parts) for t in range(T)] for o in "AB"}
    k4_low = [x for pt in parts for x in pt["k4_low"]]
    n_routes = sum(pt["n_routes"] for pt in parts)
    done = [f for pt in parts for f in pt["done"]]
    cells = [(o, p) for o in "AB" for p in range(1, PMAX + 1)]

    def above_rest(t):
        return [(o, p) for o, p in cells if live[o][t][p] > max(live[o][u][p] for u in range(T) if u != t)]
    k4_above = above_rest(0)
    null_above = [len(above_rest(t)) for t in range(1, T)]
    stop = len(k4_above) > max(null_above)
    bounds = {
        "family": "hand padding per grid stage: blank cells in one of eight places, dropped or carried as fillers; one or two stages; then or before a periodic tableau key",
        "places": {"P1": "end of last row", "P2": "start of first row", "P3": "start of last row", "P4": "end of first row", "P5": "last column from the top", "P6": "last column from the bottom", "P7": "first column from the top", "P8": "first column from the bottom"},
        "readings": {"cw": "left column first, bottom up", "ccw": "right first, top down", "col": "left first, top down", "colr": "right first, bottom up"},
        "singles": "8 places x 4 readings x widths 2-96", "doubles": "(8 places x readings cw/col x widths 2-48)^2 x drop/keep",
        "first_stages_done": len(done), "first_stages_total": len(firsts),
        "distinct_routes": n_routes, "duplicates_skipped_within_share": sum(pt["n_dupes"] for pt in parts),
        "periods": [1, PMAX], "classes": 8,
        "k4_live_by_period": {o: live[o][0][1:] for o in "AB"},
        "controls_live_by_period_min": {o: [min(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in "AB"},
        "controls_live_by_period_max": {o: [max(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in "AB"},
        "k4_settings_live_below_20": {o: low[o][0] for o in "AB"}, "controls_settings_live_below_20": {o: low[o][1:] for o in "AB"},
        "k4_live_below_20": sorted(k4_low, key=lambda x: x["period"])[:40],
        "cells_k4_above_every_copper": k4_above, "null_cells_above_rest_per_copper": null_above, "stop_queue": stop,
        "controls": f"{N_CONTROLS} shuffled coppers (seed 134), identical search",
        "order_A": "stages, then key (slot = landing place mod p)", "order_B": "key, then stages (slot = message place mod p)",
    }
    notes = (f"{n_routes:,} routes ({len(done)} of {len(firsts)} first stages) x 8 classes x 2 orders, periods 1-26. K4 settings "
             f"live below 20: {low['A'][0]} (A), {low['B'][0]} (B); coppers A {min(low['A'][1:])}-{max(low['A'][1:])}, "
             f"B {min(low['B'][1:])}-{max(low['B'][1:])}. K4 above every copper in {len(k4_above)} of 52 cells; null "
             f"{min(null_above)}-{max(null_above)}. Stop queue: {stop}.")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    """key: {'stages': [(w, reading, place, keep), ...], 'order': 'A' (stages then table) or 'B', 'alphabet': 'STD' or
    'KRY', 'key': list of shifts}; Vigenere on one alphabet; fillers struck out at the end."""
    alpha = KRY if key["alphabet"] == "KRY" else STD
    k = key["key"]

    def table(s):
        return "".join(alpha[(alpha.index(ch) + k[i % len(k)]) % 26] for i, ch in enumerate(s))

    def move(s):
        toks = list(range(len(s)))
        for w, r, p, keep in key["stages"]:
            toks = stage(toks, w, r, p, keep)
        return "".join(s[t] for t in toks if t != NULL)
    return table(move(plaintext)) if key["order"] == "A" else move(table(plaintext))


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    s1 = stage(list(range(N)), 8, "col", "P6", True)
    w1 = where_from(s1)
    wh = where_from(stage(s1, 9, "cw", "P2"))
    lines = ["rows of 8, blanks down the last column from the bottom, read down the columns left first, blanks kept as dummies;",
             "then rows of 9, blanks at the start of the first row, read up the columns left first; dummies struck out", "",
             "place  letter  after grid 1  after grid 2  copper there"]
    for qq in (22, 23, 24, 64, 65, 74):
        lines.append(f"{qq:>5}  {known[qq]:>6}  {w1[qq - 1] + 1:>12}  {wh[qq - 1] + 1:>12}  {ct[wh[qq - 1]]:>12}")
    return "\n".join(lines)
