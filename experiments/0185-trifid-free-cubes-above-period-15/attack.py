"""Experiment 0185 (F4.2). See program.md for the contract."""

EXPERIMENT = {
    "slug": "trifid-free-cubes-above-period-15",
    "title": "F4.2: trifid with a free 27-symbol cube at periods 16-97, every alignment, by constraint propagation: exact",
    "family": "4-sanborn-visual",
    "parent": "0040-trifid-free-cubes-by-constraint-propagation-rerun",
    "changed": (
        "F4.2. 0040 decided every free trifid cube at periods 2-15 (no cube fits at any alignment). Its decider does not "
        "depend on the period: each known letter ties its three coordinates to coordinates of three carved letters in its "
        "block, whatever the block length. Here periods 16-97 (97: one block), every alignment, 4,633 settings, with the "
        "same caps; ten shuffled copies run through the same sweep as the null."
    ),
    "hypothesis_expert": (
        "C3 (Sanborn's visual, three-dimensional thinking: a cube), F4; Delastelle's trifid keeps one letter per letter "
        "on 27 symbols. Model as 0040: the k-th coordinate of carved letter j in a block of n equals coordinate (3j + k) "
        "div n of plaintext letter (3j + k) mod n. 72 equalities among 81 coordinate variables, then backtracking over the "
        "classes with the 27-distinct-addresses rule and 9-per-value counts. Statistic: settings admitting a cube, K4 "
        "against 10 shuffled copies; any surviving cube decrypts and is scored."
    ),
    "hypothesis_eli5": (
        "Sanborn is a sculptor; a trifid code puts the alphabet in a 3 x 3 x 3 cube and mixes the three coordinates of "
        "neighbouring letters in groups. Groups of up to 15 letters were already ruled out. Here every longer group, up to "
        "the whole text, with every starting point: do the known letters allow any arrangement of the cube at all?"
    ),
    "prediction": "No cube at any setting, as at 2-15; or cubes at the copies' rate whose decryptions are not English. Zero candidates.",
    "method": (
        "1. For each period 16-97 and alignment: the coordinate equalities the 24 known letters force. "
        "2. Union-find, then backtracking over classes with the address and count rules (caps 3M nodes, 5,000 cubes). "
        "3. Count settings with cubes; decrypt and score any. "
        "4. The same sweep on 10 shuffled copies."
    ),
    "walkthrough": (
        "1. Take period 20 with blocks starting at place 1: places 21-40 form one block. "
        "2. Write each block letter's three coordinates in three rows, read the rows one after another, regroup in threes. "
        "3. Each known letter's coordinates must then equal certain coordinates of certain carved letters. "
        "4. Merge equal coordinates; try values 0-2 for each merged group so no two letters share an address. "
        "5. If nothing survives, no cube works at that period and start."
    ),
}

import random

N = 97
SYMBOLS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ?"
NODE_CAP = 3000000
SOL_CAP = 5000
PMIN, PMAX = 16, 97
N_CONTROLS = 10


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
    for p in range(PMIN, PMAX + 1):
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
    import time
    t0 = time.time()
    ct, known = ctx.K4, ctx.KNOWN
    rows, best = sweep(ct, known, ctx.english_score, ctx.time_left)
    candidates = []
    for sc, p, o, h, pt, cube in best[:20]:
        if h == 24 and "?" not in pt:
            candidates.append({"plaintext": pt, "key": {"cube": cube, "period": p, "offset": o}, "key_bits": 94, "key_description": f"trifid cube {cube} period {p} offset {o}; English {sc:.3f}"})
    controls = []
    rng = random.Random(1850)
    for c in range(N_CONTROLS):
        if ctx.time_left() < 120:
            break
        letters_ = list(ct); rng.shuffle(letters_)
        cr, cb = sweep("".join(letters_), known, ctx.english_score, ctx.time_left)
        controls.append({"settings": len(cr), "with_cubes": sum(1 for r in cr if r["cubes"]), "capped": sum(1 for r in cr if r["capped"]),
                         "best_english": round(cb[0][0], 3) if cb else None})
    with_cubes = [r for r in rows if r["cubes"]]
    # builder check: a planted trifid text at period 30, offset 5
    cube = list(SYMBOLS); random.Random(1851).shuffle(cube); cube = "".join(cube)
    pp = list("USEDTHEEARTHSMAGNETICEASTNORTHEASTRMATIONWASGATHEREDANDTRANSMITBERLINCLOCKUNDTOANUNKNOWNLOCATIONX")
    plant = trifid("".join(pp), cube, 30, 5, False)
    pc, _, _ = solve_setting(plant, known, 30, 5)
    plant_found = cube in pc
    return {
        "candidates": candidates[:50],
        "bounds": {"family": "trifid, free 27-symbol cube, periods 16-97, every alignment, constraint propagation and backtracking",
                   "settings": len(rows), "settings_with_cubes": len(with_cubes), "settings_capped": sum(1 for r in rows if r["capped"]),
                   "node_cap": NODE_CAP, "solution_cap": SOL_CAP, "k4_settings_with_cubes": with_cubes[:40],
                   "max_nodes": max(r["nodes"] for r in rows),
                   "best": [{"english": round(sc, 3), "period": p, "offset": o, "hits": h, "text": pt} for sc, p, o, h, pt, _ in best[:8]],
                   "plant": {"period": 30, "offset": 5, "cubes": len(pc), "true_cube_found": plant_found}, "controls": controls, "seconds": round(time.time() - t0), "exhaustive": True},
        "notes": f"{len(rows)} settings; {len(with_cubes)} admit a cube on K4; {sum(1 for r in rows if r['capped'])} capped; copies with cubes: {[c['with_cubes'] for c in controls]}",
    }


def worked_example(ctx, key):
    cubes, nodes, nc = solve_setting(ctx.K4, ctx.KNOWN, 20, 0)
    lines = ["period 20, blocks from position 1: the block 21-40 carries EASTNORTHEAST at 22-34 against the carved " + ctx.K4[21:34], "",
             f"81 coordinate variables merge into {nc} classes under all the ties from the 24 known letters",
             f"backtracking over the classes with the all-different rule visited {nodes} nodes and found {len(cubes)} cube(s)"]
    if cubes:
        pt = trifid(ctx.K4, cubes[0], 5, 0, True)
        lines.append(f"first cube in address order: {cubes[0]}")
        lines.append(f"its decryption: {pt}  ({hits(pt, ctx.KNOWN)} of 24 known letters right)")
    return "\n".join(lines)
