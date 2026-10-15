"""Experiment 0087. See program.md for the contract."""

EXPERIMENT = {
    "slug": "column-word-plus-row-word",
    "title": "A key word over the columns and a second key over the rows: the message in rows of seven, each letter shifted by its column's letter and its row's letter",
    "family": "3-two-component-key",
    "parent": "0032-row-keyed-grids-one-key-letter-per-row",
    "changed": "0032 gave each row of the grid one key letter; repeating keys give each column one. Here both at once: the key at a place is its column's letter of one word plus its row's letter of a second key, on a grid of width 2-48. Within a row the row letter cancels, so a column whose letter steps against its neighbour's makes doubled letters in that column only: the one construction found here that lines doublets up in sevens by design. Tested exactly from the 24 known letters, on the copper as carved and after each of 0080's 26,000 moves (keyed columns read the right way, issue #26), in both orders.",
    "hypothesis_expert": (
        "Type 2 of directions.md ('7-block constructions... keyed by KRYPTOS or another 7-letter word'), the prior-work "
        "database's seven-based sub-variant 4 ('KRYPTOS as a numeric key for something other than column order or an "
        "additive key: row order in a 14x7, or a per-row shift of a width-7 grid (Bean-style row shifts)'). Mechanism for "
        "the width-7 doublet column (0056, 0065): with key a[j mod w] + b[j div w], two adjacent letters in one row share "
        "b, so C[j] = C[j+1] iff P[j+1] - P[j] = a[c] - a[c+1], which depends only on the column c; doublets collect in "
        "the columns where a steps, i.e. at fixed residues mod w. Clues C5(b) ('key word/s'), C8(a) (KRYPTOS as the K4 "
        "key in a new way), C1(a) and C3 ('matrix', 'spatial systems'), C11a ('interval 7'). Model on one alphabet A "
        "(standard or KRYPTOS), sign s = +1 or -1 (s = -1 when exactly one of the two keys is applied Beaufort-wise): "
        "C[j] = s P + a[col] + b[row]; each known letter is an edge between column slot and row slot, consistency by "
        "spanning tree, checks = edges - (slots touched - components). Grid positions are carved places (move, then "
        "grid key: order A) or message places (grid key, then move: order B). Moves: none, plus 0080's set (K3 rule, one "
        "or two quarter turns, plain and keyword columnar, forward and inverse; keyword columnar now read in true key "
        "order). Widths 2-48, rows as many as needed (the row key is free, so a repeating row word is a special case). "
        "Exact; ten shuffled coppers through the identical search."
    ),
    "hypothesis_eli5": (
        "Write the message in rows of seven under KRYPTOS. Shift each letter along the table by its column's letter of "
        "KRYPTOS, and also by a letter chosen for its row from a second key. It is easy to do by hand and needs two key "
        "words, as Scheidt said. It also explains an oddity: inside a row the row's shift is the same for both letters "
        "of a pair, so doubled letters can only appear where two neighbouring column letters differ in a particular "
        "way, and they pile up in the same column, as five of K4's six doubled letters do. The 24 known letters test "
        "every width exactly, with and without a scrambling step before or after."
    ),
    "prediction": (
        "On the copper as carved (no move), no width passes all its checks; width 7 has about 14 checks and fails. After "
        "moves, consistent settings at every number of checks lie inside the range of the ten shuffled coppers, and no "
        "setting with five or more checks survives on K4. Zero candidates."
    ),
    "method": (
        "1. For each width, assign every known letter its column slot and row slot (by carved place or by message "
        "place). 2. Grow a spanning tree over the slots and test every other known letter against it, on both alphabets "
        "and both signs. 3. Do this with no move and after each of 0080's moves, in both orders. 4. Count consistent "
        "settings by number of checks on K4 and ten shuffled coppers. 5. Print K4's settings with five or more checks, "
        "with the slot letters they fix."
    ),
    "walkthrough": (
        "1. Write the copper in rows of 7. Place 22 is in row 3, column 0; place 23 in row 3, column 1; places 29 and 30 in row 4, columns 0 and 1. 2. On the sculpture's alphabet with Vigenere, copper minus message gives the key at each place: F - E = 1 at 22, L - A = 10 at 23, R - T = 23 at 29, N - H = 5 at 30. 3. Each key is a column letter plus a row letter. Places 22 and 23 share their row, so their difference, 1 - 10 = 17, is the difference of the column letters 0 and 1. 4. Places 29 and 30 share the next row and the same two columns, so 23 - 5 = 18 must be the same difference. 5. 17 is not 18: width 7 with this table is dead, whatever the two key words are. 6. Width 7 has 14 such checks in all; test every width 2-48, both tables and signs, with no move and after each of 0080's moves in both orders, and on ten scrambled coppers."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.alphabets import numeric_order
from kryptos.ciphers import columnar_transposition_encrypt, columnar_transposition_decrypt

N = 97
WIDTHS = range(2, 49)
ALPH = {"std": STD, "kry": KRY}
N_CONTROLS = 10


def perm_of(fn):
    """sigma with out[j] = in[sigma[j]] for a string transform fn."""
    idx = "".join(chr(0x100 + i) for i in range(N))
    return [ord(ch) - 0x100 for ch in fn(idx)]


def rot_cw(s, w):
    """Rows of w, columns read bottom-up, left column first (a quarter turn clockwise)."""
    rows = [s[i:i + w] for i in range(0, len(s), w)]
    return "".join(r[c] for c in range(w) for r in reversed(rows) if c < len(r))


def rot_ccw(s, w):
    """Rows of w, columns read top-down, right column first (a quarter turn anticlockwise)."""
    rows = [s[i:i + w] for i in range(0, len(s), w)]
    return "".join(r[c] for c in reversed(range(w)) for r in rows if c < len(r))


def route_specs(vocab):
    for b in range(1, N):
        for a in range(N):
            yield {"kind": "k3rule", "a": a, "b": b}
    for w in range(2, N):
        for turn in ("cw", "ccw"):
            for d in ("fwd", "inv"):
                yield {"kind": "turn", "w": w, "turn": turn, "dir": d}
        for rtl in (False, True):
            for d in ("fwd", "inv"):
                yield {"kind": "columnar", "w": w, "rtl": rtl, "dir": d}
    for w1 in range(2, N):
        for w2 in range(2, N):
            for d in ("fwd", "inv"):
                yield {"kind": "turn2", "w1": w1, "w2": w2, "dir": d}
    for word in vocab:
        if 2 <= len(word) <= 40:
            for d in ("fwd", "inv"):
                yield {"kind": "keyed", "word": word, "dir": d}


def forward_fn(spec):
    k = spec["kind"]
    if k == "k3rule":
        a, b = spec["a"], spec["b"]

        def f(s):
            out = [""] * N
            for i in range(N):
                out[(a + b * i) % N] = s[i]
            return "".join(out)
        return f
    if k == "turn":
        r = rot_cw if spec["turn"] == "cw" else rot_ccw
        return lambda s, w=spec["w"]: r(s, w)
    if k == "turn2":
        return lambda s, a=spec["w1"], b=spec["w2"]: rot_cw(rot_cw(s, a), b)
    if k == "columnar":
        o = list(range(spec["w"]))[::-1] if spec["rtl"] else list(range(spec["w"]))
        return lambda s, o=o: columnar_transposition_encrypt(s, o)
    rank = numeric_order(spec["word"])
    o = sorted(range(len(rank)), key=lambda c: rank[c])          # true keyword reading (issue #26)
    return lambda s, o=o: columnar_transposition_encrypt(s, o)


def where_of(spec):
    """where[i] = place in the moved text of letter i of the changed message (0-indexed)."""
    sigma = perm_of(forward_fn(spec))          # moved[j] = changed[sigma[j]]
    if spec.get("dir", "fwd") == "inv":       # the inverse move: moved[sigma[j]] = changed[j]
        return list(sigma)
    w = [0] * N
    for j, i in enumerate(sigma):
        w[i] = j
    return w


def move(spec, s):
    w = where_of(spec)
    out = [""] * N
    for i, ch in enumerate(s):
        out[w[i]] = ch
    return "".join(out)


def unmove(spec, s):
    w = where_of(spec)
    return "".join(s[w[i]] for i in range(N))


def checks_for(us, ws, p1):
    """Spanning tree over key slots. Edge e joins first-key slot us[e] and second-key slot p1 + ws[e]. Returns the
    list of cycle checks, each a list of (edge, sign): sum of sign * value[edge] must be 0 mod 26."""
    adj = {}
    for e, (u, w) in enumerate(zip(us, ws)):
        adj.setdefault(u, []).append((p1 + w, e, 1))
        adj.setdefault(p1 + w, []).append((u, e, -1))
    pot = {}
    tree = set()
    checks = []
    for root in adj:
        if root in pot:
            continue
        pot[root] = ()
        stack = [root]
        while stack:
            x = stack.pop()
            for y, e, sg in adj[x]:
                # relation: pot[first] - pot[second] = value[e]; from x to y: pot[y] = pot[x] - sg*value[e]
                if y not in pot:
                    pot[y] = pot[x] + ((e, -sg),)
                    tree.add(e)
                    stack.append(y)
    for e, (u, w) in enumerate(zip(us, ws)):
        if e in tree:
            continue
        # pot[u] - pot[p1+w] - value[e] == 0
        chk = list(pot[u]) + [(f, -s) for f, s in pot[p1 + w]] + [(e, -1)]
        acc = {}
        for f, s in chk:
            acc[f] = acc.get(f, 0) + s
        checks.append([(f, s) for f, s in acc.items() if s])
    return checks


def solve_keys(us, ws, vals, p1, p2):
    """Key slot values (first key a, second key b) from a consistent system; None for slots no known letter fixes.
    Each component's free shift is set so that its smallest first-key slot is 0."""
    adj = {}
    for e, (u, w) in enumerate(zip(us, ws)):
        adj.setdefault(u, []).append((p1 + w, vals[e], 1))
        adj.setdefault(p1 + w, []).append((u, vals[e], -1))
    pot = {}
    for root in sorted(adj):
        if root in pot:
            continue
        pot[root] = 0
        stack = [root]
        while stack:
            x = stack.pop()
            for y, v, sg in adj[x]:
                if y not in pot:
                    pot[y] = (pot[x] - sg * v) % 26
                    stack.append(y)
    a = [pot.get(u) for u in range(p1)]
    b = [None if (p1 + w) not in pot else (-pot[p1 + w]) % 26 for w in range(p2)]   # pot of a second-key slot is -b
    return a, b



def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    vocab = list(ctx.vocabulary)
    places = sorted(known)
    pidx = [p - 1 for p in places]
    rng = random.Random(87)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    variants = [(an, s) for an in ALPH for s in (1, -1)]
    assert plant_check(known)
    seen, routes = set(), [({"kind": "none"}, tuple(range(N)))]
    seen.add(tuple(range(N)))
    for spec in route_specs(vocab):
        w = tuple(where_of(spec))
        if w not in seen:
            seen.add(w); routes.append((spec, w))
    counts = [dict() for _ in texts]
    tested = {}
    none_result = {}
    k4_hits = []
    n_struct = 0
    stopped = None
    for ri, (spec, wh) in enumerate(routes):
        if ctx.time_left() < 60:
            stopped = ri
            break
        land = [wh[i] for i in pidx]
        vals = {}
        for an, s in variants:
            A = {c: i for i, c in enumerate(ALPH[an])}
            P = [A[known[p]] for p in places]
            for t, txt in enumerate(texts):
                vals[(an, s, t)] = [(A[txt[j]] - s * P[e]) % 26 for e, j in enumerate(land)]
        for order, pos in (("A", land), ("B", pidx)):
            if spec["kind"] == "none" and order == "B":
                continue
            for w in WIDTHS:
                us = [x % w for x in pos]
                ws = [x // w for x in pos]
                chks = checks_for(us, ws, w)
                c = len(chks)
                if c == 0:
                    continue
                n_struct += 1
                tested[c] = tested.get(c, 0) + 1
                for (an, s, t), v in vals.items():
                    ok = True
                    for chk in chks:
                        if sum(sg * v[f] for f, sg in chk) % 26:
                            ok = False
                            break
                    if spec["kind"] == "none" and t == 0:
                        none_result.setdefault(w, {"checks": c, "consistent": []})
                        if ok:
                            none_result[w]["consistent"].append(f"{an} s={s}")
                    if ok:
                        counts[t][c] = counts[t].get(c, 0) + 1
                        if t == 0 and c >= 5:
                            a, b = solve_keys(us, ws, v, w, max(ws) + 1)
                            k4_hits.append({"route": spec, "order": order, "width": w, "alphabet": an, "sign": s, "checks": c,
                                            "column_key": a, "row_key": b})
    maxc = max(tested) if tested else 0
    at_least = lambda d, c0: sum(v for c, v in d.items() if c >= c0)
    k4_ge = {c0: at_least(counts[0], c0) for c0 in range(1, 9)}
    ctl_ge = {c0: [at_least(counts[t], c0) for t in range(1, len(texts))] for c0 in range(1, 9)}
    outside = [c0 for c0 in range(1, 9) if not (min(ctl_ge[c0]) <= k4_ge[c0] <= max(ctl_ge[c0]))]
    bounds = {
        "family": "key = column letter of one key + row letter of another on a grid of width 2-48, no move or after/before 0080's moves",
        "distinct_routes": len(routes), "routes_done": stopped if stopped is not None else len(routes),
        "widths": [WIDTHS[0], WIDTHS[-1]], "cases_per_structure": "alphabet std or KRYPTOS x sign +1/-1 = 4",
        "no_move_by_width": {w: none_result[w] for w in sorted(none_result)},
        "structures_with_checks": n_struct, "structures_by_checks": dict(sorted(tested.items())),
        "k4_at_least": k4_ge, "controls_at_least": ctl_ge, "check_levels_outside_control_range": outside,
        "k4_cases_with_5_or_more_checks": k4_hits[:40], "n_k4_cases_5_plus": len(k4_hits),
        "controls": f"{N_CONTROLS} shuffled coppers (seed 87), identical search",
    }
    none_alive = [w for w, r in none_result.items() if r["consistent"]]
    notes = (f"No move: widths consistent on K4: {none_alive or 'none'} (width 7 has {none_result.get(7, {}).get('checks')} checks). "
             f"With moves: {len(routes):,} routes x widths 2-48 x 2 orders, {n_struct:,} structures x 4 cases. K4 consistent with "
             f">= c checks, c = 1..8: {[k4_ge[c] for c in range(1, 9)]}; controls max {[max(ctl_ge[c]) for c in range(1, 9)]}, min "
             f"{[min(ctl_ge[c]) for c in range(1, 9)]}. Levels outside the control range: {outside}. K4 cases with 5+ checks: {len(k4_hits)}."
             + (f" Stopped at route {stopped} for time." if stopped is not None else ""))
    return {"candidates": [], "bounds": bounds, "notes": notes}


def plant_check(known):
    """A planted text keyed by KRYPTOS over the columns of rows of 7 and a random row key must pass at width 7."""
    rng = random.Random(3)
    pt = [rng.choice(STD) for _ in range(N)]
    for p, c in known.items():
        pt[p - 1] = c
    I = {c: i for i, c in enumerate(KRY)}
    a = [I[c] for c in "KRYPTOS"]
    b = [rng.randrange(26) for _ in range(14)]
    ctxt = "".join(KRY[(I[ch] + a[j % 7] + b[j // 7]) % 26] for j, ch in enumerate(pt))
    places = sorted(known)
    v = [(I[ctxt[p - 1]] - I[known[p]]) % 26 for p in places]
    us = [(p - 1) % 7 for p in places]; ws = [(p - 1) // 7 for p in places]
    return all(sum(sg * v[f] for f, sg in chk) % 26 == 0 for chk in checks_for(us, ws, 7))


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    I = {c: i for i, c in enumerate(KRY)}
    lines = ["no move; rows of 7; key = column letter + row letter; sculpture's alphabet, s = +1", "",
             "place  known  copper  column  row  copper - known = column + row"]
    for p in (22, 23, 29, 30, 64, 65, 71, 72):
        lines.append(f"{p:>5}  {known[p]:>5}  {ct[p - 1]:>6}  {(p - 1) % 7:>6}  {(p - 1) // 7:>3}  {(I[ct[p - 1]] - I[known[p]]) % 26:>4}")
    places = sorted(known)
    us = [(p - 1) % 7 for p in places]; ws = [(p - 1) // 7 for p in places]
    lines.append("")
    lines.append(f"24 known letters, 7 column slots and {len(set(ws))} row slots: {len(checks_for(us, ws, 7))} checks")
    lines.append("places 22 and 29 share column 0; places 23 and 30 share column 1; 22, 23 share row 3; 29, 30 share row 4:")
    v = {p: (I[ct[p - 1]] - I[known[p]]) % 26 for p in (22, 23, 29, 30)}
    lines.append(f"  (22) - (23) must equal (29) - (30): {v[22]} - {v[23]} = {(v[22] - v[23]) % 26}, {v[29]} - {v[30]} = {(v[29] - v[30]) % 26}")
    return "\n".join(lines)
