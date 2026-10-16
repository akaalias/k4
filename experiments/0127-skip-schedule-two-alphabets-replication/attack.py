"""Experiment 0127. See program.md for the contract."""

EXPERIMENT = {
    "slug": "skip-schedule-two-alphabets-replication",
    "title": "Replication: the skip schedule on two unknown alphabets, where K4 had more consistent settings than ten coppers (0126), against 30 fresh coppers with every setting covered",
    "family": "1-keyed-periodic",
    "parent": "0126-hand-key-schedules-listed-and-tested",
    "changed": (
        "F1.4, replication (order-of-work rule 5). 0126 ran out of time: the skip schedule (B) was tested on part of its "
        "3,729 distinct partitions and schedules C-F not at all (their zeros mean untested). In what was done, B with two "
        "free alphabets gave K4 461 consistent partitions against 305-449 on ten coppers. Here all 3,729 B partitions "
        "are tested on K4 and 30 fresh shuffles (seed 127), all four tests, with the search's node limit lowered to "
        "100,000 so no case can stall, undecided cases counted, coverage recorded, texts run in parallel."
    ),
    "hypothesis_expert": (
        "Follow-up of 0126 (C20, C5). Same model and exact tests: key value at place i = W[f(i) mod n], f(i) = i + floor((i + "
        "phi)/m), m 2-30, phi 0..m-1, n 2-26; distinct partitions of the 24 known places; tests: 8 standard/KRYPTOS tables, "
        "one free alphabet V and B, two free alphabets (CRT decider of 0119/0123). The partitions are heavily nested "
        "(different m, phi, n giving related slot patterns), so counts are strongly correlated and a single coincidence in "
        "the known letters can lift many at once, as R under P at 28 and 66 did in 0124 (that pair shares a slot whenever "
        "f(65) - f(27) is a multiple of n). Report K4's rank among 30 fresh coppers and, after the run, whether K4's "
        "excess partitions are those that put 28 and 66 in one slot."
    ),
    "hypothesis_eli5": (
        "In the last run, one hand rule (skip a key letter every so often) fitted K4 with two unknown alphabets in more "
        "ways than it fitted ten scrambled copies. That run was cut short, so here the rule is tested completely, against "
        "thirty new scrambled copies, to see whether K4 really stands out."
    ),
    "prediction": (
        "K4's count for B with two free alphabets falls inside the range of 30 fresh coppers (rank no better than 3rd), "
        "so the 0126 excess was the small control set; the standard/KRYPTOS tables give 0 consistent partitions on K4. "
        "If K4 tops all 30, stop and report."
    ),
    "method": (
        "1. Build the 3,729 distinct partitions of the skip schedule. 2. For K4 and 30 shuffles, test each with the 8 "
        "tables, one free alphabet (V, B) and two free alphabets. 3. Count consistent partitions per test; K4's rank. "
        "4. Among K4's two-alphabet partitions, count those with 28 and 66 in one slot, and the same on the coppers."
    ),
    "walkthrough": (
        "1. Take a key word of 7 letters and the rule 'skip one key letter every 5 letters'. "
        "2. Number the key letter each place uses: 0 1 2 3 4, skip 5, 6 0 1 2 3, skip, and so on, modulo 7. "
        "3. Group the known places by that number. "
        "4. Ask whether two unknown alphabets and the word can make every group agree. "
        "5. Do it for every skip interval, phase and word length, on K4 and on thirty scrambled copies, and compare the counts."
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
    rng = random.Random(127)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    parts = [p for p in partitions()["B skip"] if 24 - len(set(p)) >= 1]
    from kryptos.facts import KNOWN
    qs = sorted(KNOWN)
    n_2866 = sum(1 for p in parts if p[qs.index(28)] == p[qs.index(66)])
    if getattr(sys.modules.get(__name__), "_text_job", None) is not _text_job:
        m = types.ModuleType(__name__); m.__dict__.update(globals()); sys.modules[__name__] = m
    with mp.get_context("fork").Pool(8) as pool:
        res = dict(pool.map(_text_job, [(t, txt, parts) for t, txt in enumerate(texts)], chunksize=1))
    k4 = res[0]
    ctrl = [res[t] for t in range(1, len(texts))]
    summary = {}
    for name in ("tables", "free V", "free B", "two free", "two free with 28,66 together"):
        vals = [c[name] for c in ctrl]
        summary[name] = {"k4": k4[name], "coppers_min": min(vals), "coppers_max": max(vals),
                         "k4_rank": 1 + sum(1 for v in vals if v > k4[name]), "coppers": sorted(vals)}
    bounds = {
        "family": "skip schedule (one keyword letter skipped every m letters), unknown keyword, 4 exact tests; replication of 0126",
        "partitions": len(parts), "partitions_with_28_66_together": n_2866,
        "coverage": {"k4": k4["done"], "coppers_min": min(c["done"] for c in ctrl)},
        "undecided": {"k4": k4["undecided"], "coppers_total": sum(c["undecided"] for c in ctrl)},
        "summary": summary,
        "controls": f"{N_CONTROLS} fresh shuffled coppers (seed 127), identical tests",
    }
    tw = summary["two free"]
    notes = (f"B skip, two free alphabets: K4 {tw['k4']}, coppers {tw['coppers_min']}-{tw['coppers_max']}, K4 rank {tw['k4_rank']} "
             f"of {N_CONTROLS + 1}. Tables: K4 {summary['tables']['k4']}. Coverage {k4['done']}/{len(parts)}; undecided K4 {k4['undecided']}.")
    return {"candidates": [], "bounds": bounds, "notes": notes}


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
