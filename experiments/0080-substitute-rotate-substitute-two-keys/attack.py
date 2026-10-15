"""Experiment 0080. See program.md for the contract."""

EXPERIMENT = {
    "slug": "substitute-rotate-substitute-two-keys",
    "title": "Change, turn, change again: a repeating key on the table, a K3-style grid turn, then a second repeating key, solved exactly",
    "family": "6-transposition-then-tableau",
    "parent": "0008-k3-formula-all-shifts-then-tableau",
    "changed": "0008 and the public searches (keithadler, nitsuah, Zekios) put one repeating key on one side of a K3-style turn. Here there is a key on both sides: the message is changed on the table with one repeating word, the letters are moved by a grid turn (or K3's every-n-th rule, or a column shuffle), and the moved text is changed again with a second repeating word. With both alphabets the same, the 24 known letters give 24 linear equations in the two keys, which are solved exactly for every route and every pair of key lengths 2-14.",
    "hypothesis_expert": (
        "Type 1 of directions.md, gap a3 of the prior-work database (reports/Kryptos K4 prior attempts database.md: "
        "'rotation sandwiched between two different tableau keys... Zekios's stacked-key search used columnar 2-7 and "
        "width-21 routes, not rotations'). Clues C1(a) and C1(c) read together (02-sanborn-said.md, CNN 2005: 'double "
        "matrixes and triple matrixes... and then went back to this table'), C2(a) (the K3 matrix and its 'shifts'), "
        "C5(b) ('key word/s', two words) and C20(a) (LAYER TWO). Model: X[i] = P[i] (+) a[i mod p1] on alphabet A; Y = "
        "route(X); C[j] = Y[j] (+) b[j mod p2] on the same alphabet A, each stage Vigenere, Beaufort or variant. "
        "Composed, C[pi(i)] = s P[i] + a'[i mod p1] + b'[pi(i) mod p2] (mod 26, indices on A) with s = -1 when exactly "
        "one stage is Beaufort, so the key alphabets drop out and four cases remain: A standard or KRYPTOS, s = +1 or -1. "
        "Each known letter is one edge between key slot a_u and key slot b_w carrying the value C - sP; the system is "
        "consistent iff every cycle of that bipartite graph sums to zero, checked by a spanning tree; the number of "
        "independent checks is edges minus (slots touched minus components). Routes (deduplicated on where the 24 known "
        "places land): K3's rule pi(i) = a + b i mod 97, all 9,312; one quarter turn, clockwise or anticlockwise, at "
        "widths 2-96, each forward and inverse; two clockwise quarter turns at every width pair 2-96, forward and "
        "inverse; plain columnar at widths 2-96 in both reading directions, forward and inverse; keyed columnar from "
        "every vocabulary word, forward and inverse. Key lengths p1, p2 = 2-14. Exact; ten shuffled coppers through "
        "the identical search give the chance rate at each number of checks. Bound left open: the two stages on "
        "different alphabets (not linear), key lengths above 14, nulls or padding (gap a1)."
    ),
    "hypothesis_eli5": (
        "The first two messages were made by shifting letters along the sculpture's table with a repeating secret "
        "word; the third was made by writing the letters in a grid and turning it. Sanborn said he used 'double and "
        "triple matrixes' and 'then went back to this table'. Here we try the sandwich: shift with one secret word, "
        "turn the grid, shift again with a second secret word. That sounds like too many unknowns, but every known "
        "letter of the message ties one letter of the first word to one letter of the second, and those ties must "
        "agree with each other. We check every grid turn and every pair of word lengths from 2 to 14, exactly, and do "
        "the same on ten scrambled copies of the copper to see how often agreement happens by luck."
    ),
    "prediction": (
        "At every number of checks K4's count of consistent cases lies inside the range of the ten shuffled coppers. "
        "No case on K4 survives seven or more independent checks. Zero candidates."
    ),
    "method": (
        "1. Build the routes and keep one per distinct landing pattern of the 24 known places. 2. For each route, "
        "each alphabet and each sign, compute the edge values C at the landing place minus s times the known letter. "
        "3. For each pair of key lengths, join slot i mod p1 of the first key to slot (landing place) mod p2 of the "
        "second key for every known letter, grow a spanning tree, and test every other edge against the tree. 4. "
        "Count consistent cases by number of checks. 5. Repeat on ten shuffled coppers. 6. Print any K4 case with "
        "five or more checks, with its key slots and the letters they fix."
    ),
    "walkthrough": (
        "1. Write the message in rows of 7 and turn the grid a quarter clockwise: read each column from the bottom "
        "up, left column first. Counting from 0, place 22 (the E of EAST) is letter 21, in row 3, column 0, and comes out "
        "as letter 10 of the turned text (place 11). 2. Take a first key of length 2 and a second of length 3. Letter "
        "21 uses slot 21 mod 2 = 1 of the first key; its new position 10 uses slot 10 mod 3 = 1 of the second. 3. On "
        "the sculpture's alphabet, the copper letter at place 11, U, minus E gives the sum of those two key letters: "
        "U - E = 10. 4. Every known letter gives "
        "such a sum for one slot of each key: 24 sums for 2 + 3 slots. 5. Five slots need four sums to fix them (one "
        "is a free shift between the keys); the other twenty sums are checks. 6. Go through the sums and see whether "
        "they agree; one disagreement kills this turn and these key lengths. 7. Repeat for every turn, rule and pair "
        "of lengths, and on ten scrambled coppers."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.alphabets import numeric_order
from kryptos.ciphers import columnar_transposition_encrypt, columnar_transposition_decrypt

N = 97
PERIODS = range(2, 15)
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
    o = numeric_order(spec["word"])
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
    places = sorted(known)                       # 1-indexed plaintext places of the 24 known letters
    pidx = [p - 1 for p in places]
    rng = random.Random(80)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    variants = [(an, s) for an in ALPH for s in (1, -1)]
    # self-checks: the route machinery inverts, and K3's rule reproduces the library's K3 decryption
    from kryptos.facts import load_k3
    from kryptos.ciphers import k3_formula_decrypt
    k3 = load_k3()
    assert k3_formula_decrypt(k3["ciphertext"]) == k3["plaintext"]
    for spec in ({"kind": "turn2", "w1": 7, "w2": 9, "dir": "fwd"}, {"kind": "turn", "w": 8, "turn": "ccw", "dir": "inv"},
                 {"kind": "keyed", "word": "KRYPTOS", "dir": "fwd"}, {"kind": "k3rule", "a": 5, "b": 7}):
        assert unmove(spec, move(spec, ct)) == ct

    seen = set()
    routes = []
    n_specs = 0
    for spec in route_specs(vocab):
        n_specs += 1
        w = where_of(spec)
        key = tuple(w[i] for i in pidx)
        if key in seen:
            continue
        seen.add(key)
        routes.append((spec, key))

    # counts[t][c] = consistent cases with c checks on text t (t = 0 is K4)
    counts = [dict() for _ in texts]
    tested = {}                                  # c -> structures with c checks (per alphabet/sign case: x4)
    k4_hits = []
    n_struct = 0
    stopped = None
    for ri, (spec, land) in enumerate(routes):
        if ctx.time_left() < 60:
            stopped = ri
            break
        vals = {}
        for an, s in variants:
            A = {c: i for i, c in enumerate(ALPH[an])}
            P = [A[known[p]] for p in places]
            for t, txt in enumerate(texts):
                vals[(an, s, t)] = [(A[txt[j]] - s * P[e]) % 26 for e, j in enumerate(land)]
        for p1 in PERIODS:
            us = [i % p1 for i in pidx]
            for p2 in PERIODS:
                ws = [j % p2 for j in land]
                chks = checks_for(us, ws, p1)
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
                    if ok:
                        counts[t][c] = counts[t].get(c, 0) + 1
                        if t == 0 and c >= 5:
                            a, b = solve_keys(us, ws, v, p1, p2)
                            k4_hits.append({"route": spec, "p1": p1, "p2": p2, "alphabet": an, "sign": s, "checks": c,
                                            "first_key": a, "second_key": b})
    maxc = max(tested) if tested else 0
    k4 = {c: counts[0].get(c, 0) for c in range(1, maxc + 1)}
    ctl = {c: [counts[t].get(c, 0) for t in range(1, len(texts))] for c in range(1, maxc + 1)}
    at_least = lambda d, c0: sum(v for c, v in d.items() if c >= c0)
    k4_ge = {c0: at_least(counts[0], c0) for c0 in range(1, 9)}
    ctl_ge = {c0: [at_least(counts[t], c0) for t in range(1, len(texts))] for c0 in range(1, 9)}
    outside = [c for c in range(1, maxc + 1) if not (min(ctl[c]) <= k4[c] <= max(ctl[c]))]
    bounds = {
        "family": "substitute, move, substitute: two repeating keys on one alphabet around a route, solved exactly",
        "route_specs": n_specs, "distinct_routes": len(routes), "routes_done": stopped if stopped is not None else len(routes),
        "route_kinds": "K3 rule a + b i mod 97 (9,312); one quarter turn cw/ccw widths 2-96 fwd/inv; two cw quarter turns "
                       "widths 2-96 x 2-96 fwd/inv; plain columnar widths 2-96 both directions fwd/inv; keyed columnar from "
                       f"{len(vocab)} vocabulary words fwd/inv",
        "key_lengths": [PERIODS[0], PERIODS[-1]], "cases_per_structure": "alphabet std or KRYPTOS x sign +1/-1 = 4",
        "structures_with_checks": n_struct, "structures_by_checks": dict(sorted(tested.items())),
        "k4_consistent_by_checks": k4, "controls_consistent_by_checks": ctl,
        "k4_at_least": k4_ge, "controls_at_least": ctl_ge,
        "check_levels_outside_control_range": outside,
        "k4_cases_with_5_or_more_checks": k4_hits[:40], "n_k4_cases_5_plus": len(k4_hits),
        "controls": f"{N_CONTROLS} shuffled coppers (seed 80), identical search",
    }
    notes = (f"{len(routes):,} distinct routes from {n_specs:,} specs, {n_struct:,} route x key-length structures with at "
             f"least one check, x4 cases. K4 consistent cases with at least c checks, c = 1..8: "
             f"{[k4_ge[c] for c in range(1, 9)]}; controls max: {[max(ctl_ge[c]) for c in range(1, 9)]}; "
             f"controls min: {[min(ctl_ge[c]) for c in range(1, 9)]}. Levels outside the control range: {outside}. "
             f"K4 cases with 5+ checks: {len(k4_hits)}." + (f" Stopped at route {stopped} for time." if stopped is not None else ""))
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    A = ALPH[key["alphabet"]]
    I = {c: i for i, c in enumerate(A)}
    a, b, m1, m2 = key["a"], key["b"], key["m1"], key["m2"]
    f = {"vig": lambda x, k: (x + k) % 26, "beau": lambda x, k: (k - x) % 26, "var": lambda x, k: (x - k) % 26}
    x = "".join(A[f[m1](I[p], a[i % len(a)])] for i, p in enumerate(plaintext))
    y = move(key["route"], x)
    return "".join(A[f[m2](I[c], b[j % len(b)])] for j, c in enumerate(y))


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    spec = {"kind": "turn", "w": 7, "turn": "cw", "dir": "fwd"}
    w = where_of(spec)
    I = {c: i for i, c in enumerate(KRY)}
    lines = ["one quarter turn clockwise at width 7; first key length 2, second key length 3; sculpture's alphabet, s = +1",
             "", "place  known  new place  copper there  first slot  second slot  sum of the two key letters"]
    for p in (22, 23, 24, 25, 26, 27):
        j = w[p - 1]
        lines.append(f"{p:>5}  {known[p]:>5}  {j + 1:>9}  {ct[j]:>12}  {(p - 1) % 2:>10}  {j % 3:>11}  "
                     f"{ct[j]}-{known[p]} = {(I[ct[j]] - I[known[p]]) % 26}")
    us = [(p - 1) % 2 for p in sorted(known)]
    ws = [w[p - 1] % 3 for p in sorted(known)]
    lines.append("")
    lines.append(f"24 sums over 2 + 3 slots: {len(checks_for(us, ws, 2))} independent checks")
    return "\n".join(lines)
