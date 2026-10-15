"""Experiment 0082. See program.md for the contract."""

EXPERIMENT = {
    "slug": "where-the-blanks-go-in-the-grid",
    "title": "The grid by hand: blank cells at the top, or filler letters carried through the second turn, then a repeating key",
    "family": "6-transposition-then-tableau",
    "parent": "0008-k3-formula-all-shifts-then-tableau",
    "changed": "97 letters never fill a grid, so a hand turn leaves blank cells. The coded searches (0008, keithadler, nitsuah) put them only at the end of the last row and drop them at once. Here the blanks sit at the start of the first row (the short row at the top), or the second grid is filled with the first grid's blank cells still in it as filler letters that are struck out only at the end, for one and two quarter turns at every width and for column shuffles, each joined to a repeating key on the table before or after the move.",
    "hypothesis_expert": (
        "Type 1 of directions.md, gap a1 of the prior-work database ('rotation with per-stage padding (nulls dropped "
        "between the two griddings), the short row at the top, or blanks in key-determined cells... all coded searches pad "
        "once, at the ends'). Clues C1(a) (02-sanborn-said.md, CNN 2005, 'double matrixes and triple matrixes'), C2(a) "
        "(the K3 matrix and its shifts; K3's 336 letters fill 24 x 14 and 8 x 42 exactly, K4's 97 fill nothing), C17(b) "
        "('whether it's 97, whether it's 100... I seem to like to manipulate the information'). Grid of width w and h = "
        "ceil(n/w) rows; the h w - n blank cells are the first cells of the top row ('top') or the last of the bottom "
        "row ('bottom', the covered case). A quarter turn reads columns bottom-up, left first (cw) or top-down, right "
        "first (ccw). Two turns: the first grid's blank cells either vanish ('drop') or travel as filler letters into "
        "the second grid and are struck out at the end ('keep'). New routes: one turn cw or ccw with blanks on top, "
        "widths 2-96; two cw turns at every width pair 2-96 with blanks top or bottom in each grid and drop or keep (seven "
        "of the eight combinations; bottom-bottom-drop is 0008's); plain columnar (both directions) and vocabulary-keyed "
        "columnar with the short row on top; all forward and inverse, deduplicated. Key: a periodic tableau key of "
        "period 1-26 after the move (key slot = landing place mod p) or before it (slot = place mod p), 8 distinct "
        "classes of plain and cipher alphabet and Beaufort-or-not. A period is live if no two known letters in one slot "
        "force different key letters. Exact; ten shuffled coppers through the identical search."
    ),
    "hypothesis_eli5": (
        "The third message was scrambled by writing it in a grid and turning the grid. Its 336 letters fill a 24 by 14 "
        "grid exactly. K4's 97 letters fill no grid, so someone working by hand has to leave some squares empty, or "
        "fill them with dummy letters. Computer searches so far always left the empty squares at the very end. A "
        "person might leave them at the start instead, or carry the dummy letters into a second grid and strike them "
        "out only at the end. Each choice moves the letters differently. We try them all, joined to a repeating "
        "secret word on the table, and see whether any lets a short word fit the 24 known letters."
    ),
    "prediction": (
        "No route, order and class has a live period below 20 on K4 beyond what the ten shuffled coppers show; the count "
        "of live settings at every period 1-26 lies inside the control range, give or take the spread at 25-26. Zero "
        "candidates."
    ),
    "method": (
        "1. Build every route: write the 97 places into the grid with the blanks on top or below, turn, and for two turns "
        "either drop the blanks or carry them as fillers into the second grid. 2. Keep one route per distinct reordering. "
        "3. For each route, class and text, compute the key letter each known letter forces at its landing place. 4. For "
        "each period 1-26 and each order, the period is live if no slot holds two different forced letters. 5. Count live "
        "settings per period on K4 and on ten shuffled coppers. 6. List K4's live settings at periods below 20."
    ),
    "walkthrough": (
        "1. Write the 97 places in rows of 10. Ten rows hold 100 cells, so 3 stay blank; put them at the start of the top row, so place 1 sits in column 3. 2. Turn the grid a quarter clockwise: read each column from the bottom up, left column first, skipping blanks. Columns 0-2 give 9 letters each and column 3 gives 10, so column 4 starts at letter 38. 3. Place 22 is in row 2, column 4, the eighth letter read from the bottom of that column: it lands at place 45. With the blanks at the end instead it would land at 18. 4. The repeating key letter at the landing place must turn E into the copper letter there; work out that key letter for all 24 known letters. 5. For a key of length p, two known letters whose landing places differ by a multiple of p use the same key letter; if they need different ones, p is dead. 6. Repeat for every width, blank placement, second turn, filler choice and order, and on ten scrambled coppers."
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


def columnar(tokens, order, top):
    """Write in rows under the key with the short row on top (top=True), read columns in key order, top-down."""
    w = len(order)
    rows = grid(tokens, w, top)
    out = []
    for c in sorted(range(w), key=lambda c: order[c]):
        for r in rows:
            if r[c] is not None:
                out.append(r[c])
    return out


def forward(spec, tokens):
    k = spec["kind"]
    if k == "turn1":
        return turn(tokens, spec["w"], True, spec["way"])
    if k == "turn2":
        mid = turn(tokens, spec["w1"], spec["top1"], "cw", fill=spec["keep"])
        return [t for t in turn(mid, spec["w2"], spec["top2"], "cw") if t != NULL]
    if k == "columnar":
        order = list(range(spec["w"]))
        return columnar(tokens, order[::-1] if spec["rtl"] else order, True)
    return columnar(tokens, numeric_order(spec["word"]), True)


def where_of(spec):
    sigma = forward(spec, list(range(N)))       # moved[j] = message[sigma[j]]
    assert sorted(sigma) == list(range(N))
    if spec["dir"] == "inv":
        return list(sigma)
    w = [0] * N
    for j, i in enumerate(sigma):
        w[i] = j
    return w


def route_specs(vocab):
    for w in range(2, N):
        for way in ("cw", "ccw"):
            for d in ("fwd", "inv"):
                yield {"kind": "turn1", "w": w, "way": way, "dir": d}
        for rtl in (False, True):
            for d in ("fwd", "inv"):
                yield {"kind": "columnar", "w": w, "rtl": rtl, "dir": d}
    for word in vocab:
        if 2 <= len(word) <= 40:
            for d in ("fwd", "inv"):
                yield {"kind": "keyed", "word": word, "dir": d}
    for w1 in range(2, N):
        for w2 in range(2, N):
            for top1 in (False, True):
                for top2 in (False, True):
                    for keep in (False, True):
                        if not (top1 or top2 or keep):
                            continue                     # 0008's case
                        for d in ("fwd", "inv"):
                            yield {"kind": "turn2", "w1": w1, "w2": w2, "top1": top1, "top2": top2, "keep": keep, "dir": d}


def slot_pairs(slots):
    """Consecutive pairs of known letters sharing a slot."""
    last, prs = {}, []
    for e, s in enumerate(slots):
        if s in last:
            prs.append((last[s], e))
        last[s] = e
    return prs


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    vocab = list(ctx.vocabulary)
    places = sorted(known)
    pidx = [p - 1 for p in places]
    rng = random.Random(82)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    T = len(texts)
    classes = [(pa, ca, beau) for pa in ALPH for ca in ALPH for beau in (False, True)]
    CI = {an: [[{c: i for i, c in enumerate(ALPH[an])}[ch] for ch in t] for t in texts] for an in ALPH}
    PI = {an: [{c: i for i, c in enumerate(ALPH[an])}[known[p]] for p in places] for an in ALPH}
    planted = plant_check(known)
    pairsB = {p: slot_pairs([i % p for i in pidx]) for p in range(1, PMAX + 1)}

    seen, routes, n_specs = set(), [], 0
    for spec in route_specs(vocab):
        n_specs += 1
        w = tuple(where_of(spec))
        if w in seen:
            continue
        seen.add(w)
        routes.append((spec, w))
    live = {o: [[0] * (PMAX + 1) for _ in range(T)] for o in "AB"}      # live[o][t][p]
    minp = {o: [dict() for _ in range(T)] for o in "AB"}                # smallest live period histogram
    k4_low = []
    stopped = None
    for ri, (spec, w) in enumerate(routes):
        if ri % 200 == 0 and ctx.time_left() < 60:
            stopped = ri
            break
        land = [w[i] for i in pidx]
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
                        k4_low.append({"route": spec, "order": o, "class": f"{pa}/{ca}/{'beau' if beau else 'vig-var'}", "period": first})
    outside = {}
    for o in "AB":
        bad = [p for p in range(1, PMAX + 1) if not (min(live[o][t][p] for t in range(1, T)) <= live[o][0][p] <= max(live[o][t][p] for t in range(1, T)))]
        outside[o] = bad
    bounds = {
        "family": "hand-padded grid turns and short-row-on-top columnar, joined to a periodic tableau key before or after",
        "route_specs": n_specs, "distinct_routes": len(routes), "routes_done": stopped if stopped is not None else len(routes),
        "periods": [1, PMAX], "classes": 8, "planted_check": planted,
        "k4_live_by_period": {o: live[o][0][1:] for o in "AB"},
        "controls_live_by_period_min": {o: [min(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in "AB"},
        "controls_live_by_period_max": {o: [max(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in "AB"},
        "k4_smallest_live_period_histogram": {o: dict(sorted(minp[o][0].items())) for o in "AB"},
        "periods_outside_control_range": outside,
        "k4_live_below_20": k4_low[:40], "n_k4_live_below_20": len(k4_low),
        "controls_live_below_20": [sum(v for p, v in minp[o][t].items() if 0 < p < 20) for o in "AB" for t in range(1, T)],
        "controls": f"{N_CONTROLS} shuffled coppers (seed 82), identical search",
        "order_A": "move, then key (slot = landing place mod p)", "order_B": "key, then move (slot = place mod p)",
    }
    notes = (f"{len(routes):,} distinct routes from {n_specs:,} specs x 8 classes x 2 orders, periods 1-26. K4 live settings "
             f"below period 20: {len(k4_low)}; per control (A then B): {bounds['controls_live_below_20']}. Periods where K4 "
             f"is outside the control range: {outside}. Planted text found: {planted}."
             + (f" Stopped at route {stopped} for time." if stopped is not None else ""))
    return {"candidates": [], "bounds": bounds, "notes": notes}


def plant_check(known):
    """A planted text through a padded two-turn route and a period-11 key must leave period 11 live."""
    rng = random.Random(5)
    pt = [rng.choice(STD) for _ in range(N)]
    for p, c in known.items():
        pt[p - 1] = c
    spec = {"kind": "turn2", "w1": 8, "w2": 13, "top1": True, "top2": False, "keep": True, "dir": "fwd"}
    w = where_of(spec)
    moved = [""] * N
    for i in range(N):
        moved[w[i]] = pt[i]
    key = [rng.randrange(26) for _ in range(11)]
    I = {c: i for i, c in enumerate(KRY)}
    ctxt = [KRY[(I[ch] + key[j % 11]) % 26] for j, ch in enumerate(moved)]
    f = {w[p - 1]: (I[ctxt[w[p - 1]]] - I[known[p]]) % 26 for p in known}
    slots = {}
    for j, v in f.items():
        if slots.setdefault(j % 11, v) != v:
            return False
    return True


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    rows = grid(list(range(N)), 10, True)
    lines = ["width 10, 97 letters: 10 rows, 3 blank cells at the start of the top row ('.' = blank, numbers = places)", ""]
    for r in rows[:3]:
        lines.append(" ".join(" ." if t is None else f"{t + 1:>2}" for t in r))
    lines.append(" ...")
    lines.append(" ".join(f"{t + 1:>2}" for t in rows[-1]))
    spec = {"kind": "turn1", "w": 10, "way": "cw", "dir": "fwd"}
    w = where_of(spec)
    spec_b = {"kind": "turn2", "w1": 10, "w2": 10, "top1": False, "top2": False, "keep": False, "dir": "fwd"}
    lines.append("")
    lines.append("one turn clockwise (columns bottom-up, left first): where the known letters land")
    lines.append("place  letter  blanks on top  blanks at the end")
    from itertools import islice
    def bottom_where():
        sig = turn(list(range(N)), 10, False)
        ww = [0] * N
        for j, i in enumerate(sig):
            ww[i] = j
        return ww
    wb = bottom_where()
    for p in (22, 23, 64, 65):
        lines.append(f"{p:>5}  {known[p]:>6}  {w[p - 1] + 1:>13}  {wb[p - 1] + 1:>16}")
    return "\n".join(lines)
