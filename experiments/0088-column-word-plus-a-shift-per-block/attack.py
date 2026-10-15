"""Experiment 0088. See program.md for the contract."""

EXPERIMENT = {
    "slug": "column-word-plus-a-shift-per-block",
    "title": "A key word over the columns plus a shift that changes every m letters, the carved lines of 31 among them",
    "family": "3-two-component-key",
    "parent": "0087-column-word-plus-row-word",
    "changed": "0087 tied the second shift to the rows of the same grid. Here the second shift changes every m letters for any m from 2 to 50 and any starting offset, independent of the column word's length w (2-31). Among these is the sculpture's own layout: K4 starts four letters before the end of a 31-letter carved line and fills three more, so a shift per carved line is m = 31 with offset 27. Doublets still pile up by column wherever the block shift stays constant.",
    "hypothesis_expert": (
        "Type 2 of directions.md, continued from 0087: the doublet-column mechanism key = a[j mod w] + b[(j + o) div m] "
        "with the block length m free of w (a slowly changing tableau row, a new row of the table every m letters, or a "
        "new shift per line of text). C27(b) (the BERLIN worksheet laid out on 31-character lines he counted on; "
        "01-facts.md: K4 fills the last four characters of K3's eleventh line and three full 31-character lines), the "
        "prior-work database ('the literal physical artifacts (the 31-character carved lines...) have not been used as a "
        "route or grid in any published attempt'), C5(b), C8(a), C11a. One alphabet (standard or KRYPTOS), sign +1 or -1, "
        "no move. Each known letter is an edge between column slot j mod w and block slot (j + o) div m; consistency by "
        "spanning tree. Bounds: w = 2-31, m = 2-50, o = 0..m-1 (the column key's own offset is a relabelling and drops "
        "out). Exact; ten shuffled coppers."
    ),
    "hypothesis_eli5": (
        "Keep the column word of experiment 87, but let the second shift change every so many letters, not at the end "
        "of each row: for instance once per carved line of the sculpture, which holds 31 letters. Within a stretch "
        "where the second shift stays the same, doubled letters can still only appear in certain columns of the word. "
        "The 24 known letters test every word length, stretch length and starting point exactly."
    ),
    "prediction": (
        "No combination with three or more checks survives on K4 beyond the shuffled-copper rate; the carved-line case "
        "(m = 31, offset 27) is dead at every word length. Zero candidates."
    ),
    "method": (
        "1. For each word length w, block length m and offset o, give each known letter its column slot and block slot. "
        "2. Grow a spanning tree over the slots and test the other known letters, on both alphabets and both signs. 3. "
        "Count consistent combinations by number of checks on K4 and ten shuffled coppers. 4. Print K4's survivors with "
        "three or more checks and the carved-line case."
    ),
    "walkthrough": (
        "1. On the sculpture K4 begins four letters before the end of a 31-letter carved line, so its places 1-4 end one line, 5-35 fill the next, 36-66 the next and 67-97 the last. 2. Take a key word of 7 letters over the columns (place p uses letter (p - 1) mod 7) plus one shift for each carved line. 3. Places 22 and 29 both use column 0 and both lie on the line of places 5-35, so they need the same total key. 4. On the sculpture's alphabet with Vigenere, F - E = 1 at place 22 and R - T = 23 at place 29: different, so a 7-letter word with one shift per carved line is dead on this table. 5. Repeat for every word length 2-31, every stretch length 2-50 and starting point, both tables and signs, and ten scrambled coppers."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
ALPH = {"std": STD, "kry": KRY}
N_CONTROLS = 10


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
    places = sorted(known)
    pidx = [p - 1 for p in places]
    rng = random.Random(88)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    vals = {}
    for an in ALPH:
        A = {c: i for i, c in enumerate(ALPH[an])}
        P = [A[known[p]] for p in places]
        for s in (1, -1):
            for t, txt in enumerate(texts):
                vals[(an, s, t)] = [(A[txt[j]] - s * P[e]) % 26 for e, j in enumerate(pidx)]
    counts = [dict() for _ in texts]
    tested = {}
    k4_hits, carved = [], {}
    n_struct = 0
    for w in range(2, 32):
        us = [j % w for j in pidx]
        for m in range(2, 51):
            for o in range(m):
                ws = [(j + o) // m for j in pidx]
                chks = checks_for(us, ws, w)
                c = len(chks)
                if c == 0:
                    continue
                n_struct += 1
                tested[c] = tested.get(c, 0) + 1
                for (an, s, t), v in vals.items():
                    ok = all(sum(sg * v[f] for f, sg in chk) % 26 == 0 for chk in chks)
                    if m == 31 and o == 27 and t == 0:
                        carved.setdefault(w, {"checks": c, "consistent": []})
                        if ok:
                            carved[w]["consistent"].append(f"{an} s={s}")
                    if ok:
                        counts[t][c] = counts[t].get(c, 0) + 1
                        if t == 0 and c >= 3:
                            k4_hits.append({"w": w, "m": m, "offset": o, "alphabet": an, "sign": s, "checks": c})
    at_least = lambda d, c0: sum(v for c, v in d.items() if c >= c0)
    k4_ge = {c0: at_least(counts[0], c0) for c0 in range(1, 9)}
    ctl_ge = {c0: [at_least(counts[t], c0) for t in range(1, len(texts))] for c0 in range(1, 9)}
    outside = [c0 for c0 in range(1, 9) if not (min(ctl_ge[c0]) <= k4_ge[c0] <= max(ctl_ge[c0]))]
    bounds = {
        "family": "key = a[j mod w] + b[(j + o) div m], one alphabet, either sign, no move",
        "w": [2, 31], "m": [2, 50], "offsets": "all 0..m-1", "structures_with_checks": n_struct,
        "structures_by_checks": dict(sorted(tested.items())),
        "carved_lines_m31_o27": {w: carved[w] for w in sorted(carved)},
        "k4_at_least": k4_ge, "controls_at_least": ctl_ge, "check_levels_outside_control_range": outside,
        "k4_survivors_3_plus": k4_hits[:40], "n_k4_3_plus": len(k4_hits),
        "controls": f"{N_CONTROLS} shuffled coppers (seed 88), identical search",
    }
    alive = [w for w, r in carved.items() if r["consistent"]]
    notes = (f"{n_struct:,} (w, m, offset) structures x 4 cases. K4 consistent with >= c checks, c = 1..8: "
             f"{[k4_ge[c] for c in range(1, 9)]}; controls max {[max(ctl_ge[c]) for c in range(1, 9)]}, min "
             f"{[min(ctl_ge[c]) for c in range(1, 9)]}. Outside: {outside}. Carved lines (m = 31, offset 27): widths alive "
             f"{alive or 'none'}. K4 survivors with 3+ checks: {len(k4_hits)}.")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    I = {c: i for i, c in enumerate(KRY)}
    lines = ["the carved lines: K4 starts 4 letters before the end of a 31-letter line (offset 27)",
             "line 1: places 1-4, line 2: 5-35, line 3: 36-66, line 4: 67-97", "",
             "word of length 7 over the columns, one shift per carved line; sculpture's alphabet, s = +1", "",
             "place  known  copper  column  line  copper - known"]
    for p in (22, 29, 64, 71):
        lines.append(f"{p:>5}  {known[p]:>5}  {ct[p - 1]:>6}  {(p - 1) % 7:>6}  {(p - 1 + 27) // 31 + 1:>4}  {(I[ct[p - 1]] - I[known[p]]) % 26:>4}")
    places = sorted(known)
    us = [(p - 1) % 7 for p in places]; ws = [(p - 1 + 27) // 31 for p in places]
    lines.append("")
    lines.append(f"7 column slots, {len(set(ws))} line slots, 24 known letters: {len(checks_for(us, ws, 7))} checks")
    return "\n".join(lines)
