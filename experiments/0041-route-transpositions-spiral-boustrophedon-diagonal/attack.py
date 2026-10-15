"""Experiment 0041. See program.md for the contract."""

EXPERIMENT = {
    "slug": "route-transpositions-spiral-boustrophedon-diagonal",
    "title": "Routes beyond columns: spirals, snakes and diagonals through a grid, tested in both orders",
    "family": "6-transposition-then-tableau",
    "parent": "0016-routes-then-tableau-forced-key-english",
    "changed": "The route set is the one gap the columnar experiments left: writing in rows and reading out along a spiral, a snake (alternate rows reversed), or diagonals, at every width. Each route is tested before the tableau, as in experiments 6 and 16, and after a substitution, as in experiment 19.",
    "hypothesis_expert": (
        "Experiments 6, 8, 16, 26 and 37 covered columnar, keyed columnar, rotation and affine routes; 19 "
        "covered substitution then those routes. The classical route transpositions of the manuals, spiral "
        "inward and outward from each corner in either turn, boustrophedon by rows and by columns, and the "
        "two diagonal zigzags, at widths 2-48 (about 700 routes), remain. Two tests per route. Before a "
        "periodic tableau: the forced key letters at the crib landing places give the live periods by the "
        "divisor rule and the forced key at live periods up to 40 is scored as English, 8 conventions, with "
        "ten full-size shuffled controls. After any one-to-one substitution: the 24 crib images must never "
        "put two different plaintext letters on one carved letter, as in experiment 19, with ten shuffles. "
        "Bounds: complete for these route families at these widths, both orders."
    ),
    "hypothesis_eli5": (
        "So far the grids were read out by columns. The old manuals also read them out in a spiral from a "
        "corner, in a snake that turns at the end of each row, or along diagonals. We try all of those, at "
        "every width, and ask the two questions as before: if the scramble came first, could a short secret "
        "word on the table then explain the carved letters; and if the letters were swapped first and "
        "scrambled after, do the 24 known letters ever land without clashing."
    ),
    "prediction": (
        "Before the tableau: smallest live period 22 to 24, forced keys inside the range of the shuffled "
        "controls. After a substitution: no route passes the one-to-one test, and no shuffle does either. "
        "No candidate."
    ),
    "method": (
        "1. Build the routes as permutations of 97 positions: for each width, spirals from four corners in "
        "two turns inward, boustrophedon by rows and by columns, and the two diagonal zigzags; each also "
        "inverted. 2. Test one, before the tableau: send the cribs through, force key letters under 8 "
        "conventions, live periods by the divisor rule, score the forced key at live periods up to 40. "
        "3. Test two, after a substitution: check the crib images for clashes. 4. Ten shuffles for each test."
    ),
    "walkthrough": (
        "1. Width 10: write the 97 positions in rows of 10. 2. Spiral: start at the top left, read along the "
        "top row, down the right edge, back along the bottom, up the left edge, then inward. 3. Note where "
        "position 22, the E of EAST, comes out, and where each of the other known letters comes out. "
        "4. Before-the-table test: the carved letter at each landing place and the known letter force a key "
        "letter; landing places a multiple of p apart must agree. 5. After-a-swap test: if the carved letter "
        "at E's landing place also sits at the landing place of a different known letter, the route is dead "
        "for any letter swap. 6. Snake and diagonals the same way, at every width."
    ),
}

import random
from kryptos.alphabets import key_letter_for

N = 97
MAXP = 40
DIVISORS = {d: [k for k in range(1, d + 1) if d % k == 0] for d in range(1, N + 1)}
CONVS = [(pa, ca, "kry", m) for pa in ("std", "kry") for ca in ("std", "kry") for m in ("vig", "beau")]


def grid_cells(w):
    rows = (N + w - 1) // w
    return [[(r * w + c) if r * w + c < N else None for c in range(w)] for r in range(rows)]


def spiral(w, corner, clockwise):
    g = grid_cells(w); R, C = len(g), w
    top, left, bottom, right = 0, 0, R - 1, C - 1
    order = []
    # generic clockwise spiral from top-left; other corners by flipping the grid
    def flip(cells):
        if corner in ("tr", "br"):
            cells = [row[::-1] for row in cells]
        if corner in ("bl", "br"):
            cells = cells[::-1]
        return cells
    g = flip(g)
    if not clockwise:
        g = [list(x) for x in zip(*g)]          # transpose turns the spiral the other way
        R, C = len(g), len(g[0]); top, left, bottom, right = 0, 0, R - 1, C - 1
    while top <= bottom and left <= right:
        for c in range(left, right + 1): order.append(g[top][c])
        for r in range(top + 1, bottom + 1): order.append(g[r][right])
        if top < bottom:
            for c in range(right - 1, left - 1, -1): order.append(g[bottom][c])
        if left < right:
            for r in range(bottom - 1, top, -1): order.append(g[r][left])
        top += 1; bottom -= 1; left += 1; right -= 1
    return [x for x in order if x is not None]


def snake_rows(w):
    g = grid_cells(w); out = []
    for r, row in enumerate(g):
        out += row if r % 2 == 0 else row[::-1]
    return [x for x in out if x is not None]


def snake_cols(w):
    g = grid_cells(w); R, C = len(g), w; out = []
    for c in range(C):
        col = [g[r][c] for r in range(R)]
        out += col if c % 2 == 0 else col[::-1]
    return [x for x in out if x is not None]


def diagonals(w, zigzag):
    g = grid_cells(w); R, C = len(g), w; out = []
    for d in range(R + C - 1):
        cells = [g[r][d - r] for r in range(R) if 0 <= d - r < C]
        if zigzag and d % 2:
            cells = cells[::-1]
        out += cells
    return [x for x in out if x is not None]


def route_set():
    routes = []
    for w in range(2, 49):
        for corner in ("tl", "tr", "bl", "br"):
            for cw in (True, False):
                routes.append((f"spiral w={w} from {corner} {'cw' if cw else 'ccw'}", spiral(w, corner, cw)))
        routes.append((f"snake rows w={w}", snake_rows(w)))
        routes.append((f"snake columns w={w}", snake_cols(w)))
        routes.append((f"diagonals w={w}", diagonals(w, False)))
        routes.append((f"diagonal zigzag w={w}", diagonals(w, True)))
    # each order list means out[j] = in[order[j]]; add inverses
    inv = []
    for name, order in routes:
        where = [0] * N
        for j, i in enumerate(order): where[i] = j
        inv.append((name + " inv", where))
    return routes + inv


def encrypt(plaintext, key):
    raise NotImplementedError("diagnostic experiment: no full key is implied, so no candidate is submitted")


def runs_in_slots(slots, P):
    filled = [slots.get(s) for s in range(P)]
    start = 0 if all(filled) else next(i for i in range(P) if filled[i] is None)
    out, cur = [], []
    for k in range(1, P + 1):
        ch = filled[(start + k) % P]
        if ch is None:
            if len(cur) >= 5: out.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    if len(cur) >= 5: out.append("".join(cur))
    return out


def test_before(ct, known, routes, score):
    crib_pos = sorted(known)
    best, hist = [], {}
    for name, order in routes:
        where = {order[j]: j for j in range(N)}
        inter = [where[p - 1] for p in crib_pos]
        for conv in CONVS:
            pa, ca, ka, m = conv
            forced = [key_letter_for(known[p], ct[j], pa, ca, ka, m) for p, j in zip(crib_pos, inter)]
            dead = set()
            for a in range(24):
                for b in range(a + 1, 24):
                    if forced[a] != forced[b]:
                        dead.update(DIVISORS[abs(inter[a] - inter[b])])
            minp = next(P for P in range(1, N + 1) if P not in dead)
            hist[minp] = hist.get(minp, 0) + 1
            for P in range(2, MAXP + 1):
                if P in dead:
                    continue
                slots = {j % P: l for j, l in zip(inter, forced)}
                runs = runs_in_slots(slots, P)
                qs = sum(len(r) - 3 for r in runs)
                if qs < 4:
                    continue
                sc = sum(score(r) * (len(r) - 3) for r in runs) / qs
                if len(best) < 10 or sc > best[-1][0]:
                    best.append((sc, name, "/".join(conv), P, runs)); best.sort(reverse=True); best = best[:10]
    return best, hist


def test_after(ct, known, routes):
    """Substitution then route: the carved letter at each crib's landing place is its image; one carved
    letter cannot be the image of two different plaintext letters."""
    survivors = []
    for name, order in routes:
        where = {order[j]: j for j in range(N)}
        src = {}
        ok = True
        for pos, p in known.items():
            c = ct[where[pos - 1]]
            if c in src and src[c] != p:
                ok = False; break
            src[c] = p
        if ok:
            survivors.append(name)
    return survivors


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    routes = route_set()
    best, hist = test_before(ct, known, routes, ctx.english_score)
    after = test_after(ct, known, routes)
    ctrl_before, ctrl_after, ctrl_minp = [], [], []
    for seed in range(10):
        if ctx.time_left() < 120:
            break
        letters_ = list(ct); random.Random(seed).shuffle(letters_); sct = "".join(letters_)
        b, h = test_before(sct, known, routes, ctx.english_score)
        ctrl_before.append(round(b[0][0], 3) if b else None); ctrl_minp.append(min(h))
        ctrl_after.append(len(test_after(sct, known, routes)))
    return {
        "candidates": [],
        "bounds": {"family": "route transpositions (spiral, snake, diagonal), widths 2-48, forward and inverse; before a periodic tableau and after a substitution",
                   "routes": len(routes), "conventions_before": len(CONVS),
                   "before_smallest_live_period": min(hist), "before_min_period_histogram": {str(k): v for k, v in sorted(hist.items())[:10]},
                   "before_best": [{"score": round(sc, 3), "route": nm, "convention": cv, "period": P, "runs": rs} for sc, nm, cv, P, rs in best],
                   "before_shuffled_best": ctrl_before, "before_shuffled_smallest_period": ctrl_minp,
                   "after_survivors": after, "after_shuffled_survivor_counts": ctrl_after},
        "notes": f"{len(routes)} routes. Before the tableau: smallest live period {min(hist)}, best forced key {best[0][0]:.3f} vs shuffled {ctrl_before}. After a substitution: {len(after)} routes pass the one-to-one test vs shuffled {ctrl_after}.",
    }


def worked_example(ctx, key):
    order = spiral(10, "tl", True)
    where = {order[j]: j for j in range(N)}
    lines = ["route: rows of 10, read out in a clockwise spiral from the top left", "", "first twelve positions read out: " + " ".join(str(i + 1) for i in order[:12]), "", "plain pos  letter  lands at  carved there"]
    for pos in (22, 23, 24, 64, 65, 66):
        j = where[pos - 1]
        lines.append(f"{pos:>9}    {ctx.KNOWN[pos]}       {j+1:>3}        {ctx.K4[j]}")
    return "\n".join(lines)
