"""Experiment 0134. See program.md for the contract."""

EXPERIMENT = {
    "slug": "mixed-matrix-readings-two-and-three-stages",
    "title": "Two and three matrix stages in mixed readings (turn either way, Sanborn's rows-then-columns-down, and its reverse), then or before a repeating key on the table",
    "family": "6-transposition-then-tableau",
    "parent": "0083-every-triple-grid-turn",
    "changed": (
        "F6.3 (mixed three-stage routes), exhaustive at small widths. 0083 closed three clockwise quarter turns at every "
        "width 2-96; 0099 two turns in mixed senses; 0037 only sampled mixed triples. Here each stage writes the text in "
        "rows of w (last row short) and reads the columns in one of four ways: left column first bottom-up (clockwise "
        "turn), right column first top-down (anticlockwise turn), left column first top-down (Sanborn's own description "
        "of a matrix code, plain columnar) or right column first bottom-up. Every ordered pair of readings at widths "
        "2-96, and every ordered triple at widths 2-24 (the all-clockwise triples are 0083's and skipped), forward and "
        "inverse, then or before a periodic key 1-26 on the standard or KRYPTOS tables (8 classes)."
    ),
    "hypothesis_expert": (
        "C1(a) (Sanborn, CNN 2005, knowledge/sources/cnn-2005-sanborn-interview-transcript.txt: matrix codes are 'a "
        "very specific type of encoding system, in which you basically take a piece of paper, and you write a line of "
        "plain text out, right, in successive rows. And then basically you write it going from top to bottom instead of "
        "left to right... sometimes I used double matrixes and triple matrixes... and then went back to this table'), "
        "C2(a) (the K3 matrix and 'all the possible shifts'). Route space: stage(w, r) for w = 2-96 and r in {cw, ccw, "
        "col, colr}; doubles: 16 reading pairs x 95^2 widths; triples: 63 reading triples (all-cw excluded) x 23^3 widths "
        "2-24; forward and inverse; duplicates removed within each worker's share (first stage), so a few cross-share "
        "duplicates count twice on K4 and coppers alike. Key: periodic tableau 1-26 after the move (slot = landing place, "
        "order A) or before (slot = message place, order B), plain and cipher alphabets standard or KRYPTOS, Vigenere/"
        "variant or Beaufort (8 distinct classes, as 0006 showed). A period is live if no two known letters in one slot "
        "force different key letters. Exact. Research note combined_methods_and_sevens.md: every public search stops at "
        "two stages. The research note's per-stage padding is F6.4, not here."
    ),
    "hypothesis_eli5": (
        "Sanborn described his 'matrix codes': write the message in rows on paper, then copy it out going down the "
        "columns; and he said he sometimes did this two or three times before using the table. There are four natural "
        "ways to copy out the columns (left or right column first, going down or up). We try every combination of two "
        "such steps at every grid width, and of three steps at widths up to 24, each followed or preceded by a "
        "repeating secret word on the sculpture's tables, and check them against the 24 known letters and against "
        "scrambled copies of the carved text."
    ),
    "prediction": (
        "As for one, two and three clockwise turns (0008, 0083, 0099): nothing live below period 20 beyond the coppers' "
        "rate, and K4 above every copper in no more (order, period) cells than the most any single copper manages "
        "against the rest. A K4 count beyond that null stops the queue for a replication. Zero candidates."
    ),
    "method": (
        "1. Compute the where-map of every stage (width 2-96, four readings). "
        "2. Compose every pair, and every triple at widths 2-24, forward and inverse; skip repeats. "
        "3. For each route, class and text, the key letter each known letter forces at its slot. "
        "4. Period p (1-26) is live in an order if no slot holds two different forced letters. "
        "5. Count live settings per period on K4 and ten scrambled coppers; compare cell by cell; list K4's live settings below 20."
    ),
    "walkthrough": (
        "1. Write the message in rows of 7 on squared paper. "
        "2. Copy it out column by column, left column first, top to bottom (Sanborn's matrix code). "
        "3. Write that result in rows of 9 and copy it out right column first, bottom to top. "
        "4. Write that in rows of 5 and copy it out left column first, bottom to top (a quarter turn). "
        "5. Note where each of the 24 known letters has landed and the carved letter there. "
        "6. With a repeating key of length p on the table, each known letter forces one key letter in its slot (landing place mod p); two that share a slot must agree, or p is dead. "
        "7. Repeat for every combination of readings and widths, the key before or after, and on scrambled copies."
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
W2MAX = 96
W3MAX = 24
WORKERS = 5


def stage(tokens, w, r):
    """Write tokens in rows of w (last row short), read the columns: cw = left first, bottom up; ccw = right first,
    top down; col = left first, top down; colr = right first, bottom up."""
    rows = [tokens[i:i + w] for i in range(0, len(tokens), w)]
    cols = range(w) if r in ("cw", "col") else range(w - 1, -1, -1)
    up = r in ("cw", "colr")
    out = []
    for c in cols:
        rr = reversed(rows) if up else rows
        out.extend(row[c] for row in rr if c < len(row))
    return out


def where_of(w, r):
    sigma = stage(list(range(N)), w, r)
    wh = [0] * N
    for j, i in enumerate(sigma):
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
    """All routes whose first stage is `first` = (r1, w1): doubles at widths 2-96, triples at 2-24."""
    r1, w1 = first
    W = WH
    a = W[(w1, r1)]
    for r2 in READINGS:
        for w2 in range(2, W2MAX + 1):
            b = W[(w2, r2)]
            m = [b[a[i]] for i in range(N)]
            yield (r1, w1, r2, w2), m
            if w1 <= W3MAX and w2 <= W3MAX:
                for r3 in READINGS:
                    if r1 == r2 == r3 == "cw":
                        continue
                    for w3 in range(2, W3MAX + 1):
                        c = W[(w3, r3)]
                        yield (r1, w1, r2, w2, r3, w3), [c[m[i]] for i in range(N)]


WH = {}


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
    """A planted text (col 7, colr 9, cw 5, then a KRYPTOS-table key of length 11) must leave period 11 live in order A."""
    rng = random.Random(5)
    pt = [rng.choice(STD) for _ in range(N)]
    for qq, a in known_list:
        pt[qq - 1] = a
    a_, b_, c_ = where_of(7, "col"), where_of(9, "colr"), where_of(5, "cw")
    wh = [c_[b_[a_[i]]] for i in range(N)]
    moved = [""] * N
    for i in range(N):
        moved[wh[i]] = pt[i]
    # the composed map must equal applying the stages in sequence
    assert stage(stage(stage(pt, 7, "col"), 9, "colr"), 5, "cw") == moved
    key = [rng.randrange(26) for _ in range(11)]
    ctxt = "".join(KRY[(KRY.index(ch) + key[j % 11]) % 26] for j, ch in enumerate(moved))
    slots = {}
    for qq, a in known_list:
        j = wh[qq - 1]
        v = (KRY.index(ctxt[j]) - KRY.index(a)) % 26
        if slots.setdefault(j % 11, v) != v:
            return False
    return encrypt("".join(pt), {"stages": [(7, "col"), (9, "colr"), (5, "cw")], "order": "A", "alphabet": "KRY", "key": key}) == ctxt


def run(ctx):
    import multiprocessing as mp
    ct, known = ctx.K4, ctx.KNOWN
    known_list = [(qq, known[qq]) for qq in sorted(known)]
    for w in range(2, N):
        for r in READINGS:
            WH[(w, r)] = where_of(w, r)
    assert plant_ok(known_list)
    rng = random.Random(133)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    firsts = [(r, w) for w in range(2, W2MAX + 1) for r in READINGS]
    # heavy first stages (w <= 24 carry the triples) spread evenly
    heavy = [f for f in firsts if f[1] <= W3MAX]; light = [f for f in firsts if f[1] > W3MAX]
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
        "family": "two or three matrix stages (rows of w, columns read in one of four ways), then or before a periodic tableau key",
        "readings": {"cw": "left column first, bottom up", "ccw": "right first, top down", "col": "left first, top down", "colr": "right first, bottom up"},
        "doubles": "16 reading pairs x widths 2-96 each", "triples": "63 reading triples (all-cw skipped, 0083) x widths 2-24 each",
        "first_stages_done": len(done), "first_stages_total": len(firsts),
        "distinct_routes": n_routes, "duplicates_skipped_within_share": sum(pt["n_dupes"] for pt in parts),
        "periods": [1, PMAX], "classes": 8,
        "k4_live_by_period": {o: live[o][0][1:] for o in "AB"},
        "controls_live_by_period_min": {o: [min(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in "AB"},
        "controls_live_by_period_max": {o: [max(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in "AB"},
        "k4_settings_live_below_20": {o: low[o][0] for o in "AB"}, "controls_settings_live_below_20": {o: low[o][1:] for o in "AB"},
        "k4_live_below_20": sorted(k4_low, key=lambda x: x["period"])[:40],
        "cells_k4_above_every_copper": k4_above, "null_cells_above_rest_per_copper": null_above, "stop_queue": stop,
        "controls": f"{N_CONTROLS} shuffled coppers (seed 133), identical search",
        "order_A": "stages, then key (slot = landing place mod p)", "order_B": "key, then stages (slot = message place mod p)",
    }
    notes = (f"{n_routes:,} routes ({len(done)} of {len(firsts)} first stages) x 8 classes x 2 orders, periods 1-26. K4 settings "
             f"live below 20: {low['A'][0]} (A), {low['B'][0]} (B); coppers A {min(low['A'][1:])}-{max(low['A'][1:])}, "
             f"B {min(low['B'][1:])}-{max(low['B'][1:])}. K4 above every copper in {len(k4_above)} of 52 cells; null "
             f"{min(null_above)}-{max(null_above)}. Stop queue: {stop}.")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    """key: {'stages': [(w, reading), ...], 'order': 'A' (stages then table) or 'B', 'alphabet': 'STD' or 'KRY',
    'key': list of shifts}; Vigenere on one alphabet."""
    alpha = KRY if key["alphabet"] == "KRY" else STD
    k = key["key"]

    def table(s):
        return "".join(alpha[(alpha.index(ch) + k[i % len(k)]) % 26] for i, ch in enumerate(s))

    def move(s):
        s = list(s)
        for w, r in key["stages"]:
            s = stage(s, w, r)
        return "".join(s)
    return table(move(plaintext)) if key["order"] == "A" else move(table(plaintext))


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    st = [(7, "col"), (9, "colr"), (5, "cw")]
    W = [where_of(w, r) for w, r in st]
    lines = ["three matrix stages: rows of 7 read down the columns left first; rows of 9 read up, right first; rows of 5 read up, left first",
             "", "place  letter  after 1  after 2  after 3  copper there"]
    for qq in (22, 23, 24, 64, 65, 74):
        a = W[0][qq - 1]; b = W[1][a]; c = W[2][b]
        lines.append(f"{qq:>5}  {known[qq]:>6}  {a + 1:>7}  {b + 1:>7}  {c + 1:>7}  {ct[c]:>12}")
    return "\n".join(lines)
