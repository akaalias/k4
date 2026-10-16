"""Experiment 0123. See program.md for the contract."""

EXPERIMENT = {
    "slug": "two-free-alphabets-exact-at-every-key-length",
    "title": "Two alphabets in unknown orders, one for the message and one for the carved letters (Quagmire IV), no move: which key lengths 1-26 can any pair fit, and is that unusual against scrambled coppers?",
    "family": "1-keyed-periodic",
    "parent": "0119-one-free-alphabet-exact-at-every-key-length",
    "changed": (
        "F1.2. 0097 tested two unknown alphabets only at key lengths 3, 7 and 21, by a relaxation. Here every length 1-26 "
        "is decided exactly with 0119's method generalised to two independent alphabets (each one-to-one), on K4 and 100 "
        "scrambled coppers. Power is stated before running: at each length, the share of coppers on which the exact test "
        "fails is the test's power to reject a random text there; lengths where K4 fits are then compared with that rate."
    ),
    "hypothesis_expert": (
        "C27(c) (Sanborn's 'slightly different' tableau), C1(b). Model: plain alphabet P and cipher alphabet C, unknown "
        "bijections letters -> Z26, key k of length L: C(c_i) = P(p_i) + k[i mod L] (Quagmire IV; the Beaufort form "
        "C(c) = k - P(p) is the same family with P reflected, so one form covers both; a key alphabet drops out). 24 linear "
        "equations over Z26; exact decision by CRT: solve mod 13 and mod 2, each alphabet's letters at most two per residue "
        "class mod 13 with each pair differing mod 2; refute at once on forced coincidences; otherwise enumerate the mod-13 "
        "letter space up to the two translations and scaling (rank <= 5) or search it depth first with pruning, a node "
        "limit reporting 'undecided'. The generalised decider agreed with 0119's on 780 one-alphabet cases and recovered "
        "planted Quagmire IV texts at lengths 3-26 in a dry run, which also showed K4 fitting at lengths 8, 13, 16, 19, 20, "
        "23, 24 and 26. Power and copper comparison are what this run adds. Two alphabets have more freedom than one, so "
        "where both K4 and most coppers fit, 0120's finding (a climb on one alphabet already has weak power at 23 and none "
        "at 26) means an English climb here could not decide; such lengths are recorded blocked, not run weakly."
    ),
    "hypothesis_eli5": (
        "K1 and K2 used one scrambled alphabet for the whole table. A variant uses two: one scrambled order to look up the "
        "message letter and another to write the carved letter. With both orders unknown there are vastly more tables. "
        "For each key length 1 to 26 we ask, by exact arithmetic on the 24 known letters, whether any pair of orders and "
        "any key could produce them, and how often the same is true of scrambled copies of the carved text."
    ),
    "prediction": (
        "Power: the exact test rejects nearly all coppers (at least 90%) at lengths 1-7 and fewer than half at lengths "
        "with 7 or fewer checks (17, 18, 23-26). K4's 8 fitting lengths lie inside the middle 90% of the coppers' counts, "
        "and at every length where K4 fits at least 5% of coppers fit too; if K4 fits at a length where fewer than 5% of "
        "coppers do (length 8, 16 checks, is the candidate), that is outside the range and stops the queue for a "
        "replication. Zero candidates."
    ),
    "method": (
        "1. For each key length 1-26 write the 24 equations. 2. Decide exactly whether a pair of one-to-one alphabets and a "
        "key satisfy them; re-check every witness. 3. Do the same on 100 scrambled coppers (seed 121). 4. Report per length "
        "the checks, K4's verdict, the share of coppers that fit (the power is one minus that share), and K4's count of "
        "fitting lengths against the coppers'."
    ),
    "walkthrough": (
        "1. Choose a key length, say 8, and group the known places by slot (place mod 8). "
        "2. For each known place write: place of the carved letter in the cipher alphabet = place of the known letter in the plain alphabet + key value of the slot. "
        "3. Two known places in one slot give one check with the key removed: C(c1) - P(p1) = C(c2) - P(p2). "
        "4. If one slot holds the same known letter over two different carved letters, those carved letters would share a place: dead. "
        "5. Otherwise solve the checks modulo 13 and modulo 2 and search the solutions for one where each alphabet keeps its letters apart. "
        "6. Repeat for every length 1-26 and for 100 scrambled copies of the carved text."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD

N = 97
LMAX = 26
N_CONTROLS = 100
ENUM_MAX_RANK = 5
NODE_LIMIT = 200000


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
NODE_LIMIT = 200000


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




def check_witness(eqs, w):
    x, k = w
    for f in ("P", "C"):
        vals = [v for a, v in x.items() if a[0] == f]
        if len(set(vals)) != len(vals):
            return False
    return all((x[("C", c)] - (x[("P", p)] + k[s])) % 26 == 0 for s, p, c in eqs)


def planted(L, rng):
    from kryptos.facts import KNOWN
    P = list(range(26)); C = list(range(26)); rng.shuffle(P); rng.shuffle(C)
    Cinv = {v: i for i, v in enumerate(C)}
    key = [rng.randrange(26) for _ in range(L)]
    pt = [rng.randrange(26) for _ in range(N)]
    for q, ch in KNOWN.items():
        pt[q - 1] = ord(ch) - 65
    return "".join(chr(65 + Cinv[(P[p] + key[i % L]) % 26]) for i, p in enumerate(pt))


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    rng = random.Random(121)
    for L in range(1, LMAX + 1):
        for _ in range(3):
            t = planted(L, rng)
            st, w = decide(equations(t, known, L), "V", rng, two=True)
            assert st == "fit" and check_witness(equations(t, known, L), w), (L, st)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    fit = [[False] * (LMAX + 1) for _ in texts]
    und = [[] for _ in texts]
    witness = {}
    for t, txt in enumerate(texts):
        for L in range(1, LMAX + 1):
            eqs = equations(txt, known, L)
            st, w = decide(eqs, "V", rng, two=True)
            if st == "undecided":
                und[t].append(L)
            if st == "fit":
                assert check_witness(eqs, w)
                fit[t][L] = True
                if t == 0:
                    pl = {f: "".join(chr(65 + a[1]) for a, v in sorted(w[0].items(), key=lambda kv: kv[1]) if a[0] == f) for f in ("P", "C")}
                    witness[str(L)] = {"plain_letters_in_place_order": pl["P"], "cipher_letters_in_place_order": pl["C"],
                                       "key": [w[1].get(s) for s in range(L)]}
        if ctx.time_left() < 60:
            break
    nc = len(texts) - 1
    checks = {L: 24 - len({(q - 1) % L for q in known}) for L in range(1, LMAX + 1)}
    share = [sum(fit[t][L] for t in range(1, len(texts))) / nc for L in range(1, LMAX + 1)]
    k4_fit = [L for L in range(1, LMAX + 1) if fit[0][L]]
    n_k4 = len(k4_fit)
    n_ctrl = sorted(sum(fit[t][1:]) for t in range(1, len(texts)))
    pct = (n_ctrl[int(0.05 * nc)], n_ctrl[int(0.95 * nc) - 1])
    unusual = [L for L in k4_fit if share[L - 1] < 0.05]
    bounds = {
        "family": "two unknown alphabets (Quagmire IV, any pair of 26! orders), periodic key, no move",
        "key_lengths": [1, LMAX], "exhaustive": "exact decision per length (witness re-checked)",
        "checks_by_length": checks, "k4_fits": k4_fit, "k4_dead": [L for L in range(1, LMAX + 1) if not fit[0][L]],
        "copper_share_fitting_by_length": share, "power_by_length": [round(1 - x, 2) for x in share],
        "k4_fitting_lengths": n_k4, "coppers_fitting_lengths_sorted": n_ctrl, "coppers_5th_95th": pct,
        "k4_fits_where_under_5pct_of_coppers_fit": unusual,
        "k4_undecided": und[0], "controls_undecided_total": sum(len(u) for u in und[1:]), "texts_done": t + 1,
        "k4_witnesses": witness,
        "controls": f"{N_CONTROLS} shuffled coppers (seed 121), identical test",
    }
    notes = (f"K4 fits at {k4_fit} ({n_k4} lengths); coppers 5th-95th {pct}; share of coppers fitting where K4 fits: "
             f"{ {L: share[L - 1] for L in k4_fit} }; unusual: {unusual}.")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    pa, ca, shifts = key["plain"], key["cipher"], key["shifts"]
    return "".join(ca[(pa.index(ch) + shifts[i % len(shifts)]) % 26] for i, ch in enumerate(plaintext))


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    lines = []
    for L in (8, 9):
        eqs = equations(ct, known, L)
        lines.append(f"key length {L}: known letters by slot (place mod {L})")
        groups = {}
        for q in sorted(known):
            groups.setdefault((q - 1) % L, []).append(f"{known[q]}->{ct[q - 1]} ({q})")
        for s_ in sorted(groups):
            lines.append(f"  slot {s_}: " + ", ".join(groups[s_]))
        st, w = decide(eqs, "V", two=True)
        if st == "fit":
            for f, name in (("P", "plain"), ("C", "cipher")):
                lines.append(f"  {name} alphabet places: " + " ".join(f"{chr(65 + a[1])}={v}" for a, v in sorted(w[0].items(), key=lambda kv: kv[1]) if a[0] == f))
            lines.append(f"  key: {[w[1].get(s_) for s_ in range(L)]}")
        else:
            lines.append(f"  {st}: no pair of alphabets fits")
        lines.append("")
    return "\n".join(lines)
