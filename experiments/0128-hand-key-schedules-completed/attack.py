"""Experiment 0128. See program.md for the contract."""

EXPERIMENT = {
    "slug": "hand-key-schedules-completed",
    "title": "The hand schedules 0126 never reached: stutter, back and forth, triangle and square steps, restart at each carved line, and the tableau rows as keys, tested exactly against 30 coppers",
    "family": "1-keyed-periodic",
    "parent": "0127-skip-schedule-two-alphabets-replication",
    "changed": (
        "F1.4, completion. 0126 ran out of its time budget inside the skip schedule, so schedules C (stutter), D (back and "
        "forth), E (triangle, square) and F (restart per carved line) were never tested (their zeros in 0126 mean untested), "
        "and the tableau rows as fixed keys (A) were compared with only 3 coppers. Here all 1,325 distinct partitions of C-F "
        "on K4 and 30 shuffles (seed 128), the four exact tests of 0126/0127, coverage recorded; and A against all 30."
    ),
    "hypothesis_expert": (
        "C20(c)-(e), C5, C3(a). Models as written in 0126: C f = floor((i + phi)/r), r 2-6; D keyword forward then backward, "
        "ends repeated or not, n 2-26, every phase; E f = T(i + phi) or (i + phi)^2 mod n, phi 0-96; F f = column on the "
        "carved line minus 1 (K4 fills columns 28-31 of line 11, then lines 12-14), from the line start or from K4's first "
        "letter, n 2-31. Key value at place i = W[f(i) mod n], W unknown. Exact tests per distinct partition of the 24 known "
        "places: 8 standard/KRYPTOS tables; one free alphabet V and B; two free alphabets (CRT decider, node limit "
        "100,000, undecided counted). A: 26 carved tableau rows with and without the index letter as repeating keys from "
        "every start, 16 table settings, known letters reproduced."
    ),
    "hypothesis_eli5": (
        "The rest of the list of hand rules for using a key word (use each letter twice or more, go back and forth "
        "through the word, jump by growing steps, start again at each carved line), and the rows of the sculpture's big "
        "table as keys, each checked exactly against the 24 known letters and against thirty scrambled copies."
    ),
    "prediction": (
        "No partition of C-F is consistent on the standard or KRYPTOS tables with K4; on free alphabets K4's counts lie "
        "inside the 30 coppers' range in all 16 cells, give or take one; the tableau rows reproduce at most 7 of 24, as "
        "on the coppers. A cell with K4 above every copper is replicated first."
    ),
    "method": (
        "1. Distinct partitions of schedules C-F. 2. For K4 and 30 shuffles, the four exact tests on each. 3. Counts per "
        "schedule and test, K4's rank. 4. Tableau rows as keys, best known letters reproduced, K4 and every copper."
    ),
    "walkthrough": (
        "1. Take a 6-letter key word and the rule 'use each key letter twice': key letter numbers 0 0 1 1 2 2 3 3 4 4 5 5, then again. "
        "2. Group the known places by key letter number. "
        "3. On the sculpture's table, every group must share one key value (carved place minus known place in KRYPTOS order). "
        "4. With unknown tables, ask whether any alphabet or pair of alphabets makes every group agree. "
        "5. Repeat for every rule in the list and on thirty scrambled copies of K4."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
N_CONTROLS = 30
ENUM_MAX_RANK = 5
NODE_LIMIT = 20000


def equations(text, known, L):
    """(slot, plain index, cipher index) for every known place, as letter numbers 0-25."""
    return [((q - 1) % L, ord(known[q]) - 65, ord(text[q - 1]) - 65) for q in sorted(known)]


def nullspace(rows, nv, q):
    """Basis of the solution space of rows (list of {var: coef}) mod prime q, as sig[var] = tuple over basis."""
    M = [[r.get(v, 0) % q for v in range(nv)] for r in rows]
    piv, r = [], 0
    for c in range(nv):
        pr = next((i for i in range(r, len(M)) if M[i][c]), None)
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        inv = pow(M[r][c], q - 2, q)
        M[r] = [(x * inv) % q for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [(a - f * b) % q for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == len(M):
            break
    pset = set(piv)
    free = [c for c in range(nv) if c not in pset]
    sig = {}
    for v in range(nv):
        if v in pset:
            row = M[piv.index(v)]
            sig[v] = tuple((-row[f]) % q for f in free)
        else:
            sig[v] = tuple(1 if f == v else 0 for f in free)
    return sig, len(free)


def gf2_solve(rows, rhs, d):
    """A t in GF(2)^d with rows[i].t = rhs[i] for all i, or None."""
    M = [list(r) + [b] for r, b in zip(rows, rhs)]
    r, piv = 0, []
    for c in range(d):
        pr = next((i for i in range(r, len(M)) if M[i][c]), None)
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        for i in range(len(M)):
            if i != r and M[i][c]:
                M[i] = [a ^ b for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
    if any(not any(row[:d]) and row[d] for row in M):
        return None
    t = [0] * d
    for i, c in enumerate(piv):
        t[c] = M[i][d]
    return t


def column_basis13(G):
    """Indices of a maximal set of independent columns of G (rows = letters) mod 13."""
    if not G:
        return []
    ncol = len(G[0])
    chosen, red = [], []          # red: reduced copies of chosen columns, for independence test
    for c in range(ncol):
        v = [row[c] % 13 for row in G]
        for piv, w in red:
            if v[piv]:
                f = v[piv]
                v = [(a - f * b) % 13 for a, b in zip(v, w)]
        nz = next((i for i, x in enumerate(v) if x), None)
        if nz is not None:
            inv = pow(v[nz], 11, 13)
            v = [(x * inv) % 13 for x in v]
            red.append((nz, v)); chosen.append(c)
    return chosen


ENUM_MAX_RANK = 5
NODE_LIMIT = 20000


def decide(eqs, form, rng=None, two=False):
    """Exact decision: 'fit' (with a re-checked witness), 'dead', or 'undecided'.
    Solves the 24 linear equations mod 13 and mod 2 (Z26 = Z2 x Z13 by CRT); a one-to-one alphabet needs every
    residue class mod 13 to hold at most two letters, and each such pair to differ mod 2. When the mod-13 letter
    space (translation removed) has rank <= ENUM_MAX_RANK, every point up to scaling is enumerated: exact both ways.
    Larger spaces are searched for a witness (random points, then the propagation search with a node limit)."""
    if two:     # Quagmire IV: plain and cipher alphabets independent
        letters = sorted({("P", e[1]) for e in eqs} | {("C", e[2]) for e in eqs})
    else:
        letters = sorted({("x", e[1]) for e in eqs} | {("x", e[2]) for e in eqs})
    slots = sorted({e[0] for e in eqs})
    var = {a: i for i, a in enumerate(letters)}
    PF, CF = ("P", "C") if two else ("x", "x")
    for s in slots:
        var[("k", s)] = len(var)
    sgn = 1 if form == "V" else -1
    rows = []
    for s, p, c in eqs:
        r = {}
        r[var[(CF, c)]] = r.get(var[(CF, c)], 0) + 1
        r[var[(PF, p)]] = r.get(var[(PF, p)], 0) - sgn
        r[var[("k", s)]] = r.get(var[("k", s)], 0) - 1
        rows.append(r)
    nv = len(var)
    s13, d13 = nullspace(rows, nv, 13)
    s2, d2 = nullspace(rows, nv, 2)
    xi = [var[a] for a in letters]
    fam = [a[0] for a in letters]
    base = {}
    for a in letters:
        base.setdefault(a[0], var[a])
    G = [[(s13[var[a]][j] - s13[base[a[0]]][j]) % 13 for j in range(d13)] for a in letters]
    cols = column_basis13(G)
    C = [[row[c] for c in cols] for row in G]
    rank = len(cols)
    S2 = [s2[v] for v in xi]

    def test_u(u):
        """Return a witness (places, key) if this mod-13 point extends to a one-to-one solution, else None."""
        vals = [sum(a * b for a, b in zip(row, u)) % 13 for row in C]
        cls = {}
        for i, v in enumerate(vals):
            cls.setdefault((fam[i], v), []).append(i)
        pairs = []
        for g in cls.values():
            if len(g) > 2:
                return None
            if len(g) == 2:
                pairs.append(g)
        prow = [tuple(a ^ b for a, b in zip(S2[i], S2[j])) for i, j in pairs]
        t2 = gf2_solve(prow, [1] * len(pairs), d2) if pairs else [0] * d2
        if t2 is None:
            return None
        t13 = [0] * d13
        for c, uc in zip(cols, u):
            t13[c] = uc
        def val(v):
            a13 = sum(x * y for x, y in zip(s13[v], t13)) % 13
            a2 = sum(x * y for x, y in zip(s2[v], t2)) % 2
            return next(z for z in range(26) if z % 13 == a13 and z % 2 == a2)
        places = {a: val(var[a]) for a in letters}
        key = {s_: val(var[("k", s_)]) for s_ in slots}
        return places, key

    # sound refutation first: two letters identical mod 13 and mod 2 in every solution, or three identical mod 13
    by13 = {}
    for i, row in enumerate(C):
        by13.setdefault((fam[i], tuple(row)), []).append(i)
    for g in by13.values():
        if len(g) > 2 or (len(g) == 2 and S2[g[0]] == S2[g[1]]):
            return ("dead", None)
    if rank <= ENUM_MAX_RANK:
        # every u up to a nonzero scalar: first nonzero coordinate equal to 1
        def reps(r):
            if r == 0:
                yield ()
                return
            for lead in range(r):
                for tail in __import__("itertools").product(range(13), repeat=r - lead - 1):
                    yield (0,) * lead + (1,) + tail
            yield (0,) * r
        for u in reps(rank):
            w = test_u(u)
            if w:
                return ("fit", w)
        return ("dead", None)
    # exact depth-first search over the mod-13 space: change variables so that `rank` pivot letters carry the free
    # values directly; every other letter is a fixed combination of them. Assign pivot values one at a time; a letter
    # is placed as soon as its combination is complete; prune when a residue class gets a third letter or the pairs so
    # far cannot all differ mod 2.
    n = len(C)
    piv_rows = []
    basis = []                      # reduced copies for independence
    for i in range(n):
        v = list(C[i])
        for pc, w_ in basis:
            if v[pc]:
                f = v[pc]
                v = [(x - f * y) % 13 for x, y in zip(v, w_)]
        nz = next((j for j, x in enumerate(v) if x), None)
        if nz is not None:
            inv = pow(v[nz], 11, 13)
            basis.append((nz, [(x * inv) % 13 for x in v])); piv_rows.append(i)
        if len(piv_rows) == rank:
            break
    B = [C[i] for i in piv_rows]                      # rank x rank, invertible: w = B u
    # inverse of B mod 13
    Mx = [list(B[i]) + [1 if j == i else 0 for j in range(rank)] for i in range(rank)]
    for c in range(rank):
        pr = next(i for i in range(c, rank) if Mx[i][c])
        Mx[c], Mx[pr] = Mx[pr], Mx[c]
        inv = pow(Mx[c][c], 11, 13)
        Mx[c] = [(x * inv) % 13 for x in Mx[c]]
        for i in range(rank):
            if i != c and Mx[i][c]:
                f = Mx[i][c]
                Mx[i] = [(x - f * y) % 13 for x, y in zip(Mx[i], Mx[c])]
    Binv = [row[rank:] for row in Mx]
    # letter i value = C[i] . u = C[i] . Binv . w = D[i] . w
    D = [[sum(C[i][k] * Binv[k][j] for k in range(rank)) % 13 for j in range(rank)] for i in range(n)]
    # order pivots greedily so that dependents complete early
    order, remaining = [], list(range(rank))
    while remaining:
        best = max(remaining, key=lambda j: sum(1 for i in range(n) if D[i][j] and all(
            D[i][q] == 0 or q in order or q == j for q in range(rank))))
        order.append(best); remaining.remove(best)
    complete_at = {}
    for i in range(n):
        need = [order.index(q) for q in range(rank) if D[i][q]]
        complete_at.setdefault(max(need) if need else -1, []).append(i)
    nodes = [0]
    found = [None]

    def pairs_ok(pairs):
        prow = [tuple(a ^ b for a, b in zip(S2[i], S2[j])) for i, j in pairs]
        return gf2_solve(prow, [1] * len(pairs), d2) is not None

    def dfs(depth, wvals, cls, pairs):
        nodes[0] += 1
        if nodes[0] > NODE_LIMIT * 5:
            return None
        if depth == rank:
            u = [sum(Binv[k][j] * wvals[j] for j in range(rank)) % 13 for k in range(rank)]
            return test_u(u)
        q = order[depth]
        vals_try = range(13) if depth > 0 else (0, 1)     # scaling symmetry: first pivot 0 or 1
        for val in vals_try:
            wvals[q] = val
            newly = complete_at.get(depth, [])
            cls2 = {k: list(v) for k, v in cls.items()}
            pairs2 = list(pairs)
            ok = True
            for i in newly:
                v = sum(D[i][j] * wvals[j] for j in range(rank) if D[i][j]) % 13
                g = cls2.setdefault((fam[i], v), [])
                if len(g) == 2:
                    ok = False; break
                if g:
                    pairs2.append((g[0], i))
                g.append(i)
            if ok and len(pairs2) > len(pairs) and not pairs_ok(pairs2):
                ok = False
            if ok:
                r = dfs(depth + 1, wvals, cls2, pairs2)
                if r:
                    return r
                if nodes[0] > NODE_LIMIT * 5:
                    return None
        wvals[q] = None
        return None

    cls0 = {}
    for i in complete_at.get(-1, []):
        cls0.setdefault((fam[i], 0), []).append(i)
    if any(len(g) > 2 for g in cls0.values()):
        return ("dead", None)
    pairs0 = [tuple(g) for g in cls0.values() if len(g) == 2]
    if pairs0 and not pairs_ok(pairs0):
        return ("dead", None)
    w = dfs(0, [None] * rank, cls0, pairs0)
    if w:
        return ("fit", w)
    return ("undecided", None) if nodes[0] > NODE_LIMIT * 5 else ("dead", None)




# ---------------- schedules ----------------
def col_on_plate(i):
    """0-based message place -> 0-based column on its carved line (K4 starts at column 28 of line 11)."""
    return (i + 27) % 31


def schedules():
    """Yield (family, setting, f) with f(i) the key-letter counter for 0-based place i (taken mod n later)."""
    for m in range(2, 31):
        for phi in range(m):
            yield "B skip", f"m={m} phi={phi}", (lambda i, m=m, phi=phi: i + (i + phi) // m)
    for r in range(2, 7):
        for phi in range(r):
            yield "C stutter", f"r={r} phi={phi}", (lambda i, r=r, phi=phi: (i + phi) // r)
    for phi in range(97):
        yield "E triangle", f"phi={phi}", (lambda i, phi=phi: (i + phi) * (i + phi + 1) // 2)
        yield "E square", f"phi={phi}", (lambda i, phi=phi: (i + phi) ** 2)
    yield "F line restart", "from line start", col_on_plate
    yield "F line restart", "from K4's first letter", (lambda i: i if i < 4 else col_on_plate(i))


def back_and_forth(n, repeat_ends):
    seq = list(range(n)) + (list(range(n - 1, -1, -1)) if repeat_ends else list(range(n - 2, 0, -1)))
    return seq


def partitions():
    """Distinct slot partitions of the 24 known places per schedule family: {family: {partition: example setting}}."""
    from kryptos.facts import KNOWN
    qs = [q - 1 for q in sorted(KNOWN)]
    out = {}

    def canon(labels):
        m, t = {}, []
        for x in labels:
            m.setdefault(x, len(m)); t.append(m[x])
        return tuple(t)
    for fam, setting, f in schedules():
        nmax = 31 if fam.startswith("F") else 26
        for n in range(2, nmax + 1):
            p = canon([f(i) % n for i in qs])
            out.setdefault(fam, {}).setdefault(p, f"{setting} n={n}")
    for n in range(2, 27):
        for ends in (True, False):
            seq = back_and_forth(n, ends)
            if len(seq) < 2:
                continue
            for phi in range(len(seq)):
                p = canon([seq[(i + phi) % len(seq)] for i in qs])
                out.setdefault("D back and forth", {}).setdefault(p, f"n={n} ends={'repeated' if ends else 'once'} phi={phi}")
    return out


def table_ok(text, part):
    """8 standard/KRYPTOS tables: list of bools, all key values in a slot equal."""
    from kryptos.facts import KNOWN
    qs = sorted(KNOWN)
    res = []
    for pa in (STD, KRY):
        for ca in (STD, KRY):
            for beau in (False, True):
                slot = {}
                ok = True
                for lab, q in zip(part, qs):
                    c, p = ca.index(text[q - 1]), pa.index(KNOWN[q])
                    v = (c + p) % 26 if beau else (c - p) % 26
                    if slot.setdefault(lab, v) != v:
                        ok = False; break
                res.append(ok)
    return res


def eqs_of(text, part):
    from kryptos.facts import KNOWN
    qs = sorted(KNOWN)
    return [(lab, ord(KNOWN[q]) - 65, ord(text[q - 1]) - 65) for lab, q in zip(part, qs)]


def tableau_keys():
    from kryptos.ciphers import tableau_rows
    rows = tableau_rows(carved=True)
    out = []
    for r, row in enumerate(rows):
        for idx in (False, True):
            k = (STD[r] + row) if idx else row
            out.append((f"row {r + 1}{' with index letter' if idx else ''}", k))
    return out


def fixed_hits(text, key):
    from kryptos.facts import KNOWN
    best = 0
    for pa in (STD, KRY):
        for ca in (STD, KRY):
            for ka in (STD, KRY):
                for beau in (False, True):
                    for off in range(len(key)):
                        h = 0
                        for q, ch in KNOWN.items():
                            kv = ka.index(key[(q - 1 + off) % len(key)])
                            c = (kv - pa.index(ch)) % 26 if beau else (pa.index(ch) + kv) % 26
                            h += ca[c] == text[q - 1]
                        best = max(best, h)
    return best


def _text_job(args):
    t, txt, parts = args
    from kryptos.facts import KNOWN
    qs = sorted(KNOWN)
    i28, i66 = qs.index(28), qs.index(66)
    cnt = {"tables": 0, "free V": 0, "free B": 0, "two free": 0, "two free with 28,66 together": 0, "undecided": 0, "done": 0}
    for p in parts:
        cnt["done"] += 1
        if any(table_ok(txt, p)):
            cnt["tables"] += 1
        e = eqs_of(txt, p)
        for name, form, two in (("free V", "V", False), ("free B", "B", False), ("two free", "V", True)):
            st = decide(e, form, two=two)[0]
            cnt["undecided"] += st == "undecided"
            if st == "fit":
                cnt[name] += 1
                if two and p[i28] == p[i66]:
                    cnt["two free with 28,66 together"] += 1
    return t, cnt


def run(ctx):
    import multiprocessing as mp
    import sys, types
    ct = ctx.K4
    rng = random.Random(128)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    allp = partitions()
    fams = [f for f in allp if not f.startswith("B")]
    if getattr(sys.modules.get(__name__), "_text_job", None) is not _text_job:
        m = types.ModuleType(__name__); m.__dict__.update(globals()); sys.modules[__name__] = m
    summary, coverage, undec = {}, {}, {}
    with mp.get_context("fork").Pool(8) as pool:
        for fam in fams:
            parts = [p for p in allp[fam] if 24 - len(set(p)) >= 1]
            res = dict(pool.map(_text_job, [(t, txt, parts) for t, txt in enumerate(texts)], chunksize=1))
            coverage[fam] = {"partitions": len(parts), "k4_done": res[0]["done"], "coppers_min_done": min(res[t]["done"] for t in range(1, len(texts)))}
            undec[fam] = {"k4": res[0]["undecided"], "coppers_total": sum(res[t]["undecided"] for t in range(1, len(texts)))}
            for name in ("tables", "free V", "free B", "two free"):
                vals = [res[t][name] for t in range(1, len(texts))]
                summary[f"{fam} | {name}"] = {"k4": res[0][name], "coppers_min": min(vals), "coppers_max": max(vals),
                                              "k4_rank": 1 + sum(1 for v in vals if v > res[0][name])}
        tk = tableau_keys()
        fixed = pool.map(_fixed_job, [(txt, tk) for txt in texts], chunksize=1)
    outside = [k for k, v in summary.items() if not v["coppers_min"] <= v["k4"] <= v["coppers_max"]]
    bounds = {
        "family": "hand key schedules C-F (stutter, back and forth, triangle, square, restart per carved line), unknown keyword, 4 exact tests; tableau rows as fixed keys",
        "coverage": coverage, "undecided": undec, "summary": summary, "outside_copper_range": outside,
        "tableau_rows_as_keys": {"keys": len(tk), "k4_best_hits": fixed[0], "coppers_best_hits": sorted(fixed[1:])},
        "controls": f"{N_CONTROLS} shuffled coppers (seed 128), identical tests",
    }
    notes = (f"Outside the copper range: {outside or 'none'}. Tables consistent on K4: "
             f"{ {k: v['k4'] for k, v in summary.items() if k.endswith('tables')} }. Tableau rows: K4 {fixed[0]}/24, coppers "
             f"{min(fixed[1:])}-{max(fixed[1:])}.")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def _fixed_job(args):
    txt, tk = args
    return max(fixed_hits(txt, k) for _, k in tk)


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    from kryptos.facts import KNOWN
    ct = ctx.K4
    n, m = 7, 5
    f = lambda i: (i + i // m) % n
    lines = [f"skip schedule: key word of {n} letters, one key letter skipped every {m} letters; KRYPTOS on both sides, Vigenere", "",
             "place  known  carved  key letter no.  key value"]
    slots = {}
    for q in sorted(KNOWN):
        v = (KRY.index(ct[q - 1]) - KRY.index(KNOWN[q])) % 26
        slots.setdefault(f(q - 1), []).append(v)
        lines.append(f"{q:5d}  {KNOWN[q]:>5}  {ct[q - 1]:>6}  {f(q - 1):14d}  {v:9d}")
    clash = [s for s, vs in slots.items() if len(set(vs)) > 1]
    lines += ["", f"key letter numbers with clashing values: {sorted(clash)}: dead"]
    return "\n".join(lines)
