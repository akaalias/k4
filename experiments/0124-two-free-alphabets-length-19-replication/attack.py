"""Experiment 0124. See program.md for the contract."""

EXPERIMENT = {
    "slug": "two-free-alphabets-length-19-replication",
    "title": "Replication: two unknown alphabets fit K4 at key length 19, where 3 of 100 scrambled coppers fit; against 1,000 fresh coppers, corrected for looking at every length, and against copies that keep the known places' letters",
    "family": "1-keyed-periodic",
    "parent": "0123-two-free-alphabets-exact-at-every-key-length",
    "changed": (
        "F1.2, replication (order-of-work rule 5). 0123 found K4 consistent with Quagmire IV at key length 19 while only 3% "
        "of 100 coppers were. Here: (a) 1,000 fresh shuffles (seed 124), all lengths 1-26, give the share fitting at 19 "
        "and a look-elsewhere p: the share of shuffles whose rarest fitting length is as rare as K4's; (b) 1,000 copies "
        "that keep the 24 carved letters at the known places and shuffle only the other 73 (null B), which isolates "
        "whether the fit comes from the known places themselves."
    ),
    "hypothesis_expert": (
        "Follow-up of 0123 (C27(c), C1(b)). Mechanism to test: at length 19 the known places pair up 38 apart (26-34 with "
        "64-72), nine checks; places 28 and 66 are both R under P, so one check holds for free, and the other eight leave "
        "two free alphabets room to fit. Under null A (letters shuffled) that coincidence is rare. Under null B the "
        "carved letters at the 24 known places are those of K4, so the exact test, which reads only those letters, "
        "returns K4's verdict on every copy: null B is a check that the test depends only on the known places, and the "
        "honest null is A. Prediction is about A with the look-elsewhere correction. Same exact decider as 0123 "
        "(two independent alphabets, CRT mod 13 and mod 2, witness re-checked)."
    ),
    "hypothesis_eli5": (
        "In the last run, two unknown alphabets with a 19-letter key could produce the 24 known letters, which happened "
        "for only 3 of 100 scrambled copies. One reason may be a coincidence in the carved text: two known R's, 38 places "
        "apart, both sit under a carved P. Here we try 1,000 new scrambled copies and ask how often any key length looks "
        "as rare as 19 did, since we looked at 26 lengths and something rare turns up by chance."
    ),
    "prediction": (
        "At length 19 about 2-5% of the 1,000 fresh coppers fit (K4's p near 0.03), but corrected for looking at every "
        "length the p is above 0.2: a copper usually fits at some length that few coppers fit at. So the length-19 fit is "
        "not a signal and F1.2 continues. If the corrected p is below 0.01, stop and report."
    ),
    "method": (
        "1. Draw 1,000 shuffles of K4 (seed 124). 2. For each, decide Quagmire IV consistency at lengths 1-26 exactly. "
        "3. Share fitting per length; K4's p at 19. 4. For K4 and each shuffle, the rarest fitting length's share (shares "
        "estimated from the other shuffles); corrected p = share of shuffles at least as rare as K4. 5. Null B: 200 copies "
        "keeping the known places' carved letters, to confirm the verdict depends only on those."
    ),
    "walkthrough": (
        "1. Write K4 in rows of 19; places 38 apart fall in the same column. "
        "2. Pair the known places that share a column: 26 with 64, 27 with 65, and so on up to 34 with 72. "
        "3. Places 28 and 66 are both R under carved P: whatever the alphabets, that pair agrees by itself. "
        "4. The other eight pairs must each satisfy carved-place minus known-place equal in both, and some pair of alphabets does. "
        "5. Scramble the carved letters, repeat, and count how often a scramble fits at 19, or at any length as rarely."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD

N = 97
LMAX = 26
N_CONTROLS = 1000
N_NULLB = 200
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
    rng = random.Random(124)
    for L in (19, 8, 26):
        t = planted(L, rng)
        st, w = decide(equations(t, known, L), "V", rng, two=True)
        assert st == "fit" and check_witness(equations(t, known, L), w)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    fit = []
    und = 0
    for t, txt in enumerate(texts):
        row = [False] * (LMAX + 1)
        for L in range(1, LMAX + 1):
            eqs = equations(txt, known, L)
            st, w = decide(eqs, "V", rng, two=True)
            und += st == "undecided"
            if st == "fit":
                assert check_witness(eqs, w)
                row[L] = True
        fit.append(row)
        if ctx.time_left() < 120:
            break
    nc = len(fit) - 1
    cnt = [sum(fit[t][L] for t in range(1, nc + 1)) for L in range(LMAX + 1)]
    share = [c / nc for c in cnt]
    p19 = share[19]

    def rarest(t):
        vals = []
        for L in range(1, LMAX + 1):
            if fit[t][L]:
                c = cnt[L] - (1 if t > 0 else 0)            # leave the copper itself out
                vals.append(c / (nc - (1 if t > 0 else 0)))
        return min(vals) if vals else 1.0
    r_k4 = rarest(0)
    r_ctrl = [rarest(t) for t in range(1, nc + 1)]
    p_corr = sum(1 for r in r_ctrl if r <= r_k4) / nc
    # null B: keep the 24 known places' carved letters, shuffle the rest
    kp = {q - 1 for q in known}
    other = [i for i in range(N) if i not in kp]
    nb_same = 0
    for _ in range(N_NULLB):
        letters = [ct[i] for i in other]; rng.shuffle(letters)
        cp = list(ct)
        for i, ch in zip(other, letters):
            cp[i] = ch
        cp = "".join(cp)
        same = all((decide(equations(cp, known, L), "V", rng, two=True)[0] == "fit") == fit[0][L] for L in range(1, LMAX + 1))
        nb_same += same
    bounds = {
        "family": "two unknown alphabets (Quagmire IV), periodic key 1-26, no move: replication of the length-19 fit",
        "fresh_coppers": nc, "seed": 124, "undecided": und,
        "k4_fits": [L for L in range(1, LMAX + 1) if fit[0][L]],
        "copper_share_fitting_by_length": [round(x, 3) for x in share[1:]],
        "k4_p_at_19": p19, "k4_rarest_fitting_share": r_k4,
        "look_elsewhere_p": p_corr,
        "null_b_copies": N_NULLB, "null_b_same_verdict_as_k4_at_every_length": nb_same,
        "controls": f"{nc} fresh shuffled coppers (seed 124); null B {N_NULLB} copies keeping the known places' letters",
    }
    notes = (f"Length 19: {cnt[19]} of {nc} fresh coppers fit (p {p19:.3f}). K4's rarest fitting length share {r_k4:.3f}; "
             f"look-elsewhere p {p_corr:.3f}. Null B: {nb_same}/{N_NULLB} copies give K4's verdict at every length.")
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
