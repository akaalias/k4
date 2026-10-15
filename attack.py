"""Experiment 0040. See program.md for the contract."""

EXPERIMENT = {
    "slug": "trifid-free-cubes-by-constraint-propagation-rerun",
    "title": "Trifid with a free cube: the 24 known letters as equations on the cube's coordinates, solved exactly",
    "family": "4-visual-spatial",
    "parent": "0039-trifid-free-cubes-by-constraint-propagation",
    "changed": "Rerun of experiment 39, whose summary line crashed when no cube survived, so its record carries an error instead of a result; the solver and bounds are unchanged. Experiment 33 searched free cubes by trial and error and plateaued at 17 of 24. Here the cube is not searched but solved: every known letter ties three cube coordinates to three carved letters' coordinates, the ties are merged, and the remaining freedom is enumerated under the rule that all 27 symbols have different addresses.",
    "hypothesis_expert": (
        "Trifid over 27 symbols (A-Z and '?') with period p: the three coordinate rows of a block are "
        "concatenated and regrouped, so the k-th coordinate of ciphertext letter j equals coordinate m div p "
        "of plaintext letter m mod p, with m = 3j + k. Each known plaintext letter therefore gives three "
        "equalities between coordinate variables of symbols, 81 variables in all; a union-find merges them "
        "into classes, and the bijection, 27 distinct triples with each axis value used exactly nine times, "
        "is enforced by backtracking over class values with counting prunes. Every surviving cube decrypts "
        "the text with all 24 known letters right by construction, so the English score of the other 73 "
        "letters decides, against the same procedure on shuffled K4. Periods 2-15, every alignment. A "
        "planted trifid text must be recovered exactly. Bounds: complete for trifid with any cube at periods "
        "2-15, within the node cap of the search."
    ),
    "hypothesis_eli5": (
        "In trifid every letter has a three-digit address in a 27-seat cube, and the cipher shuffles the "
        "digits of a few letters at a time. Experiment 33 tried to find the cube by guessing and nudging, "
        "and could not. This time we do algebra instead: each known letter says 'this carved letter's first "
        "digit equals that message letter's second digit', and so on. Chaining all those equalities leaves "
        "only a little freedom, and the rule that no two letters share an address closes most of it. Every "
        "cube that survives is tried, and the one whose message reads most like English wins, if any does."
    ),
    "prediction": (
        "At every period and alignment the equalities either contradict the bijection or leave a handful "
        "of cubes, none of whose decryptions read better than -5.5 per quadgram; shuffled K4 behaves the "
        "same. Zero candidates pass."
    ),
    "method": (
        "1. For each period and alignment, list the blocks and, for every known plaintext letter in a "
        "block, the three coordinate equalities it implies. 2. Merge equalities with union-find over the "
        "81 coordinate variables. 3. Backtrack over the classes' values in {0,1,2}, pruning when two symbols "
        "would share an address or an axis value would exceed nine symbols. 4. Decrypt the text under each "
        "surviving cube, score the free letters as English, keep the best. 5. Repeat on two shuffles."
    ),
    "walkthrough": (
        "1. Period 5, blocks from position 1: the block 21-25 holds the known letters E A S T at 22-25. "
        "2. Carved letters of that block: J Q S S E, each with a three-digit address. 3. The rule says: the "
        "first digit of J is the first digit of the block's first letter, the second digit of J is the first "
        "digit of its second letter E, the third digit of J the first digit of A, and so on round the block. "
        "4. Write each such tie as 'this digit equals that digit'. 5. Chain the ties: if J's second digit "
        "equals E's first, and E's first equals K's third, then J's second equals K's third. 6. Give each "
        "chain a value 0, 1 or 2 so that no two letters end with the same address. 7. Decrypt and read."
    ),
}

import random

N = 97
SYMBOLS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ?"
NODE_CAP = 3000000
SOL_CAP = 5000


def coords_of(cube):
    to, frm = {}, {}
    for i, ch in enumerate(cube):
        t = (i // 9, (i // 3) % 3, i % 3); to[ch] = t; frm[t] = ch
    return to, frm


def blocks(p, o):
    out = []
    if o:
        out.append((0, o))
    i = o
    while i < N:
        out.append((i, min(i + p, N))); i += p
    return [(s, e) for s, e in out if e - s >= 2]


def trifid(text, cube, p, o, decrypt):
    to, frm = coords_of(cube)
    out = list(text)
    for s, e in blocks(p, o):
        blk = text[s:e]; n = len(blk)
        if not decrypt:
            rows = [[to[ch][k] for ch in blk] for k in range(3)]
            digits = rows[0] + rows[1] + rows[2]
            out[s:e] = [frm[tuple(digits[3 * j:3 * j + 3])] for j in range(n)]
        else:
            digits = [d for ch in blk for d in to[ch]]
            rows = [digits[0:n], digits[n:2 * n], digits[2 * n:3 * n]]
            out[s:e] = [frm[(rows[0][j], rows[1][j], rows[2][j])] for j in range(n)]
    return "".join(out)


def encrypt(plaintext, key):
    return trifid(plaintext, key["cube"], key["period"], key["offset"], False)


class UF:
    def __init__(self, n):
        self.p = list(range(n))
    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]; x = self.p[x]
        return x
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[ra] = rb


def var(sym, k):
    return SYMBOLS.index(sym) * 3 + k


def solve_setting(ct, known, p, o):
    """Returns (cubes, nodes, classes): all cubes consistent with the known letters, up to caps."""
    uf = UF(81)
    for s, e in blocks(p, o):
        n = e - s
        for j in range(n):
            for k in range(3):
                m = 3 * j + k
                pi, pk = m % n, m // n          # plaintext letter index in block, its coordinate
                pos = s + pi + 1
                if pos in known:
                    uf.union(var(ct[s + j], k), var(known[pos], pk))
    roots = sorted({uf.find(v) for v in range(81)})
    cls = {r: i for i, r in enumerate(roots)}
    of = [cls[uf.find(v)] for v in range(81)]       # variable -> class
    nc = len(roots)
    # order classes so that symbols complete early: by first symbol index
    order = sorted(range(nc), key=lambda c: min(v // 3 for v in range(81) if of[v] == c))
    val = [-1] * nc
    axis_count = [[0] * 3 for _ in range(3)]        # per axis, per value: symbols fully assigned on that axis
    used = set()
    sols, nodes = [], 0
    sym_classes = [[of[3 * s + k] for k in range(3)] for s in range(27)]

    def addr(sym):
        t = tuple(val[c] for c in sym_classes[sym])
        return None if -1 in t else t

    def rec(i):
        nonlocal nodes
        nodes += 1
        if nodes > NODE_CAP or len(sols) >= SOL_CAP:
            return
        if i == nc:
            sols.append([SYMBOLS[s] for s in sorted(range(27), key=lambda s: addr(s))]); return
        c = order[i]
        for v in range(3):
            val[c] = v
            ok = True
            touched = []
            for s in range(27):
                if c in sym_classes[s]:
                    a = addr(s)
                    if a is not None:
                        if a in used:
                            ok = False; break
                        used.add(a); touched.append(a)
            if ok:
                # axis count prune: no value on any axis may exceed 9 symbols with that value fixed
                cnt = [[0] * 3 for _ in range(3)]
                for s in range(27):
                    for k in range(3):
                        vv = val[sym_classes[s][k]]
                        if vv >= 0:
                            cnt[k][vv] += 1
                if all(cnt[k][vv] <= 9 for k in range(3) for vv in range(3)):
                    rec(i + 1)
            for a in touched:
                used.discard(a)
            val[c] = -1
            if nodes > NODE_CAP or len(sols) >= SOL_CAP:
                return

    rec(0)
    cubes = []
    for order_syms in sols:
        # the sorted-by-address list is the cube in address order
        cubes.append("".join(order_syms))
    return cubes, nodes, nc


def hits(pt, known):
    return sum(1 for pos, ch in known.items() if pt[pos - 1] == ch)


def sweep(ct, known, score, time_left):
    rows, best = [], []
    for p in range(2, 16):
        for o in range(p):
            if time_left() < 60:
                return rows, best
            cubes, nodes, nc = solve_setting(ct, known, p, o)
            crib_idx = {pos - 1 for pos in known}
            top = None
            for cube in cubes:
                pt = trifid(ct, cube, p, o, True)
                h = hits(pt, known)
                sc = score("".join(ch for i, ch in enumerate(pt) if i not in crib_idx and ch != "?"))
                if top is None or sc > top[0]:
                    top = (sc, h, pt, cube)
            rows.append({"period": p, "offset": o, "classes": nc, "nodes": nodes, "cubes": len(cubes), "capped": nodes > NODE_CAP or len(cubes) >= SOL_CAP,
                         "best_english": None if top is None else round(top[0], 3), "best_hits": None if top is None else top[1]})
            if top:
                best.append((top[0], p, o, top[1], top[2], top[3]))
    best.sort(key=lambda t: -t[0])
    return rows, best


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    rows, best = sweep(ct, known, ctx.english_score, ctx.time_left)
    candidates = []
    for sc, p, o, h, pt, cube in best[:20]:
        if h == 24 and "?" not in pt:
            candidates.append({"plaintext": pt, "key": {"cube": cube, "period": p, "offset": o}, "key_bits": 94, "key_description": f"trifid cube {cube} period {p} offset {o}; English {sc:.3f}"})
    controls = []
    for seed in range(2):
        if ctx.time_left() < 300:
            break
        letters_ = list(ct); random.Random(seed).shuffle(letters_)
        _, cb = sweep("".join(letters_), known, ctx.english_score, ctx.time_left)
        controls.append(round(cb[0][0], 3) if cb else None)
    return {
        "candidates": candidates[:50],
        "bounds": {"family": "trifid, free 27-symbol cube, periods 2-15, every alignment, solved by constraint propagation and backtracking",
                   "settings": len(rows), "settings_with_cubes": sum(1 for r in rows if r["cubes"]), "settings_capped": sum(1 for r in rows if r["capped"]),
                   "node_cap": NODE_CAP, "solution_cap": SOL_CAP, "per_setting": rows,
                   "best": [{"english": round(sc, 3), "period": p, "offset": o, "hits": h, "text": pt} for sc, p, o, h, pt, _ in best[:8]],
                   "shuffled_control_best": controls},
        "notes": f"{len(rows)} settings; {sum(1 for r in rows if r['cubes'])} admit at least one cube; {sum(1 for r in rows if r['capped'])} hit a cap. " + (f"Best English {best[0][0]:.3f} at period {best[0][1]} offset {best[0][2]}" if best else "No cube is consistent with the known letters at any setting") + f"; shuffled K4 {controls}. {len(candidates)} candidates.",
    }


def worked_example(ctx, key):
    cubes, nodes, nc = solve_setting(ctx.K4, ctx.KNOWN, 5, 0)
    lines = ["period 5, blocks from position 1: the block 21-25 carries E A S T at 22-25 against the carved " + ctx.K4[20:25], "",
             f"81 coordinate variables merge into {nc} classes under all the ties from the 24 known letters",
             f"backtracking over the classes with the all-different rule visited {nodes} nodes and found {len(cubes)} cube(s)"]
    if cubes:
        pt = trifid(ctx.K4, cubes[0], 5, 0, True)
        lines.append(f"first cube in address order: {cubes[0]}")
        lines.append(f"its decryption: {pt}  ({hits(pt, ctx.KNOWN)} of 24 known letters right)")
    return "\n".join(lines)
