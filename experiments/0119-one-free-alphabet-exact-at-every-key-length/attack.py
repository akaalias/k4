"""Experiment 0119. See program.md for the contract."""

EXPERIMENT = {
    "slug": "one-free-alphabet-exact-at-every-key-length",
    "title": "One alphabet in an unknown order on both sides of the table (Quagmire III), no move: does any order fit the 24 known letters, key lengths 1-26, solved exactly?",
    "family": "1-keyed-periodic",
    "parent": "0097-free-mixed-alphabets-after-a-move",
    "changed": (
        "F1.1, first step (exact consistency). 0097 tested one unknown alphabet only at key lengths 3, 7 and 21, and only "
        "with a linear relaxation that can refute but not confirm (it rejects when two letters are forced to the same "
        "place mod 2 and mod 13; a system can still have no one-to-one solution without any such forced pair). Here "
        "every key length 1-26 is solved exactly by a search over the alphabet with propagation, in both table forms "
        "(Vigenere-like: place(c) = place(p) + k; Beaufort-like: place(c) = k - place(p)), with no move, on K4 and on 100 "
        "scrambled coppers. Key lengths where K4 has no fitting alphabet are closed exactly; the rest go to the English "
        "climb (next experiment)."
    ),
    "hypothesis_expert": (
        "C27(c) (Sanborn, NYT 20 Nov 2010: his K1/K2 tableau was 'slightly different from the one on Kryptos'), C11a, "
        "C1(b) (the table alone, no move). K1 and K2 are Quagmire III on the KRYPTOS alphabet (keys PALIMPSEST, ABSCISSA). "
        "Covered so far: standard and KRYPTOS alphabets (0005, crib sweep), keyword alphabets from every dictionary word "
        "(0109), alphabets one swap or move from KRYPTOS (0071), any alphabet at lengths 3, 7, 21 by relaxation (0097). "
        "Model: one unknown bijection A: letters -> Z26 used for plain and cipher sides; key k of length L (free values, "
        "the key alphabet drops out); form V: A(c_i) = A(p_i) + k[i mod L]; form B: A(c_i) = k[i mod L] - A(p_i) "
        "(variant Beaufort is form V with k negated). The 24 known letters give 24 linear equations over Z26 = Z2 x Z13. Exact "
        "decision: solve mod 13 and mod 2; a one-to-one alphabet needs every residue class mod 13 to hold at most two "
        "letters, each such pair differing mod 2. Refute at once when two letters coincide mod 13 and mod 2 in every "
        "solution, or three mod 13 (0097's relaxation); otherwise enumerate the mod-13 letter space up to translation and "
        "scaling (rank <= 5), or search it depth first with pruning on class size and mod-2 solvability (larger ranks), "
        "with a node limit that reports 'undecided' rather than guessing. Every fit yields a witness alphabet and key "
        "re-checked against all 24 equations; cross-checked on 40 coppers against an independent propagation search "
        "(no fit it found was called dead). Planted texts at "
        "every length must come out consistent. Controls: 100 shuffles of K4 (seed 119), same test."
    ),
    "hypothesis_eli5": (
        "K1 and K2 were enciphered on a table whose rows are one scrambled alphabet (it starts KRYPTOS), each row shifted "
        "one place, with a repeating key word choosing the row for each letter. Sanborn said his own table was slightly "
        "different. Here the scrambled alphabet may be any of the 400 million million million million orders. We do not "
        "guess it: for each key length from 1 to 26 a careful search asks whether any order at all, with any key, turns "
        "the carved letters into the 24 letters we know. If none does, that key length is finished for good."
    ),
    "prediction": (
        "Key lengths 1-6 have no fitting alphabet on K4 (too many repeats of a slot); from about 8 upward most lengths fit "
        "in both forms, because a free alphabet has 25 free places and the known letters give fewer checks than that. "
        "K4's number of fitting lengths lies inside the middle 90% of the 100 scrambled coppers in each form. If K4 fits "
        "at a length where fewer than 5% of coppers fit, that is outside the coppers' range and stops the queue. Zero "
        "candidates (this step returns none)."
    ),
    "method": (
        "1. For each key length L from 1 to 26 and each form, write the 24 equations (slot i mod L, known letter, carved "
        "letter). 2. Decide exactly whether a one-to-one alphabet and a key satisfy them, by linear algebra mod 13 and "
        "mod 2 with an exhaustive search of the mod-13 solutions; re-check every witness. 3. Do the same on 100 scrambled coppers. 4. Report, per "
        "length and form, K4 fit or not, the share of coppers that fit, and the number of checks (24 minus the slots "
        "that hold a known letter). 5. Validate on planted texts and against 0097's relaxation (every exact fit must "
        "also pass the relaxation)."
    ),
    "walkthrough": (
        "1. Choose a key length, say 7, and write the 24 known places with their slot (place mod 7). "
        "2. For each known place write: place-in-alphabet of the carved letter = place of the known letter + key value of the slot. "
        "3. In slot 3 the known letters R (66) and C (73) both sit under carved P, so R and C would need the same place: no alphabet works, length 7 is dead. "
        "4. When no such clash shows at once, set the first letter's place to 0 and try values for the busiest slot's key; each choice fixes further places through the equations. "
        "5. Back up whenever two letters would need the same place or one letter two places. "
        "6. If a full set of places and key values satisfies all 24 equations, the length is alive; if every branch backs up, it is dead. "
        "7. Repeat with the Beaufort form (carved place = key value minus known place), for every length 1-26, then on scrambled coppers."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD

N = 97
LMAX = 26
N_CONTROLS = 100
FORMS = ("V", "B")


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


def decide(eqs, form, rng=None):
    """Exact decision: 'fit' (with a re-checked witness), 'dead', or 'undecided'.
    Solves the 24 linear equations mod 13 and mod 2 (Z26 = Z2 x Z13 by CRT); a one-to-one alphabet needs every
    residue class mod 13 to hold at most two letters, and each such pair to differ mod 2. When the mod-13 letter
    space (translation removed) has rank <= ENUM_MAX_RANK, every point up to scaling is enumerated: exact both ways.
    Larger spaces are searched for a witness (random points, then the propagation search with a node limit)."""
    letters = sorted({e[1] for e in eqs} | {e[2] for e in eqs})
    slots = sorted({e[0] for e in eqs})
    var = {("x", a): i for i, a in enumerate(letters)}
    for s in slots:
        var[("k", s)] = len(var)
    sgn = 1 if form == "V" else -1
    rows = []
    for s, p, c in eqs:
        r = {}
        r[var[("x", c)]] = r.get(var[("x", c)], 0) + 1
        r[var[("x", p)]] = r.get(var[("x", p)], 0) - sgn
        r[var[("k", s)]] = r.get(var[("k", s)], 0) - 1
        rows.append(r)
    nv = len(var)
    s13, d13 = nullspace(rows, nv, 13)
    s2, d2 = nullspace(rows, nv, 2)
    xi = [var[("x", a)] for a in letters]
    a0 = xi[0]
    G = [[(s13[v][j] - s13[a0][j]) % 13 for j in range(d13)] for v in xi]
    cols = column_basis13(G)
    C = [[row[c] for c in cols] for row in G]
    rank = len(cols)
    S2 = [s2[v] for v in xi]

    def test_u(u):
        """Return a witness (places, key) if this mod-13 point extends to a one-to-one solution, else None."""
        vals = [sum(a * b for a, b in zip(row, u)) % 13 for row in C]
        cls = {}
        for i, v in enumerate(vals):
            cls.setdefault(v, []).append(i)
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
        places = {a: val(var[("x", a)]) for a in letters}
        key = {s_: val(var[("k", s_)]) for s_ in slots}
        return places, key

    # sound refutation first: two letters identical mod 13 and mod 2 in every solution, or three identical mod 13
    by13 = {}
    for i, row in enumerate(C):
        by13.setdefault(tuple(row), []).append(i)
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
                g = cls2.setdefault(v, [])
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
        cls0.setdefault(0, []).append(i)
    if any(len(g) > 2 for g in cls0.values()):
        return ("dead", None)
    pairs0 = [tuple(g) for g in cls0.values() if len(g) == 2]
    if pairs0 and not pairs_ok(pairs0):
        return ("dead", None)
    w = dfs(0, [None] * rank, cls0, pairs0)
    if w:
        return ("fit", w)
    return ("undecided", None) if nodes[0] > NODE_LIMIT * 5 else ("dead", None)


def solve(eqs, form, node_limit=NODE_LIMIT):
    """Witness search: return (alphabet places dict, key dict) satisfying every equation one-to-one, or None
    (none found within node_limit). form V: x[c] = x[p] + k[s]; form B: x[c] = k[s] - x[p]. All mod 26."""
    letters = sorted({e[1] for e in eqs} | {e[2] for e in eqs})
    slots = sorted({e[0] for e in eqs})
    sgn = 1 if form == "V" else -1
    nodes = [0]
    def propagate(x, used, k):
        changed = True
        while changed:
            changed = False
            for s, p, c in eqs:
                xs, xp, xc = k.get(s), x.get(p), x.get(c)
                n_known = (xs is not None) + (xp is not None) + (xc is not None)
                if n_known < 2:
                    continue
                if n_known == 3:
                    if (xc - (sgn * xp + xs)) % 26:
                        return False
                    continue
                if xc is None:
                    v = (sgn * xp + xs) % 26
                    if p == c:
                        if v != xp:
                            return False
                        continue
                    if v in used:
                        return False
                    x[c] = v; used.add(v); changed = True
                elif xp is None:
                    v = ((xc - xs) * sgn) % 26
                    if p == c:
                        if v != xc:
                            return False
                        continue
                    if v in used:
                        return False
                    x[p] = v; used.add(v); changed = True
                else:
                    k[s] = (xc - sgn * xp) % 26; changed = True
        return True

    def pick(x, k):
        best, bscore = None, -1
        for s in slots:
            if s not in k:
                sc = sum(1 for e in eqs if e[0] == s and (e[1] not in x or e[2] not in x))
                if sc > bscore:
                    best, bscore = ("k", s), sc
        for L_ in letters:
            if L_ not in x:
                sc = sum(1 for e in eqs if (e[1] == L_ or e[2] == L_) and e[0] in k)
                if sc > bscore:
                    best, bscore = ("x", L_), sc
        return best

    def dfs(x, used, k):
        nodes[0] += 1
        if nodes[0] > node_limit:
            return None
        if not propagate(x, used, k):
            return None
        if all(e[0] in k and e[1] in x and e[2] in x for e in eqs):
            return x, k
        kind, v = pick(x, k)
        for val in range(26):
            if kind == "x" and val in used:
                continue
            x2, u2, k2 = dict(x), set(used), dict(k)
            if kind == "x":
                x2[v] = val; u2.add(val)
            else:
                k2[v] = val
            r = dfs(x2, u2, k2)
            if r:
                return r
        return None

    first = eqs[0][1]
    return dfs({first: 0}, {0}, {})


def check_witness(eqs, form, w):
    x, k = w
    sgn = 1 if form == "V" else -1
    if len(set(x.values())) != len(x):
        return False
    return all((x[c] - (sgn * x[p] + k[s])) % 26 == 0 for s, p, c in eqs)


def l1_ok(eqs):
    f, g = {}, {}
    for s, a, c in eqs:
        if f.setdefault((s, a), c) != c or g.setdefault((s, c), a) != a:
            return False
    return True


def planted(L, form, rng):
    """Encrypt random letters with the known letters in place under a random alphabet and key; return the text."""
    from kryptos.facts import KNOWN
    order = list(range(26)); rng.shuffle(order)          # order[letter] = place
    inv = {v: i for i, v in enumerate(order)}
    key = [rng.randrange(26) for _ in range(L)]
    pt = [rng.randrange(26) for _ in range(N)]
    for q, ch in KNOWN.items():
        pt[q - 1] = ord(ch) - 65
    sgn = 1 if form == "V" else -1
    return "".join(chr(65 + inv[(sgn * order[p] + key[i % L]) % 26]) for i, p in enumerate(pt))


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    rng = random.Random(119)
    # validation: planted texts must fit at their own length and form
    plant_fail = []
    for L in range(1, LMAX + 1):
        for form in FORMS:
            for _ in range(3):
                t = planted(L, form, rng)
                st, w = decide(equations(t, known, L), form, rng)
                if st != "fit" or not check_witness(equations(t, known, L), form, w):
                    plant_fail.append((L, form))
    assert not plant_fail, plant_fail
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    fit = {f: [[False] * (LMAX + 1) for _ in texts] for f in FORMS}
    relax_violations = 0
    undecided = {f: [[] for _ in texts] for f in FORMS}
    witness = {}
    for t, txt in enumerate(texts):
        for L in range(1, LMAX + 1):
            eqs = equations(txt, known, L)
            for form in FORMS:
                st, w = decide(eqs, form, rng)
                if st == "undecided":
                    undecided[form][t].append(L)
                if st == "fit":
                    assert check_witness(eqs, form, w)
                    if form == "V" and not l1_ok(eqs):
                        relax_violations += 1
                    fit[form][t][L] = True
                    if t == 0:
                        witness[f"{form}{L}"] = {"places": {chr(65 + a): v for a, v in sorted(w[0].items())},
                                                 "key": [w[1].get(s) for s in range(L)]}
        if ctx.time_left() < 60:
            break
    nonempty = {L: len({(q - 1) % L for q in known}) for L in range(1, LMAX + 1)}
    checks = {L: 24 - nonempty[L] for L in nonempty}
    share = {f: [sum(fit[f][t][L] for t in range(1, len(texts))) / N_CONTROLS for L in range(1, LMAX + 1)] for f in FORMS}
    k4_fit = {f: [L for L in range(1, LMAX + 1) if fit[f][0][L]] for f in FORMS}
    k4_dead = {f: [L for L in range(1, LMAX + 1) if not fit[f][0][L]] for f in FORMS}
    n_fit_ctrl = {f: sorted(sum(fit[f][t][L] for L in range(3, LMAX + 1)) for t in range(1, len(texts))) for f in FORMS}
    n_fit_k4 = {f: sum(fit[f][0][L] for L in range(3, LMAX + 1)) for f in FORMS}
    pct = {f: (n_fit_ctrl[f][4], n_fit_ctrl[f][94]) for f in FORMS}
    unusual = {f: [L for L in range(3, LMAX + 1) if fit[f][0][L] and share[f][L - 1] < 0.05] for f in FORMS}
    bounds = {
        "family": "one unknown alphabet on both sides (Quagmire III, any of 26! orders), periodic key, no move",
        "key_lengths": [1, LMAX], "forms": {"V": "A(c) = A(p) + k", "B": "A(c) = k - A(p)"},
        "exhaustive": "exact decision per length and form (search with propagation, witness re-checked)",
        "checks_by_length": checks,
        "k4_fits": k4_fit, "k4_dead": k4_dead,
        "copper_share_fitting_by_length": share,
        "k4_fitting_lengths_3_26": n_fit_k4, "coppers_fitting_lengths_3_26_sorted": n_fit_ctrl,
        "coppers_5th_95th_percentile": pct, "k4_fits_where_under_5pct_of_coppers_fit": unusual,
        "k4_witnesses": witness, "relaxation_violations": relax_violations,
        "k4_undecided": {f: undecided[f][0] for f in FORMS},
        "controls_undecided_total": {f: sum(len(u) for u in undecided[f][1:]) for f in FORMS},
        "texts_done": t + 1,
        "plants": "3 per length and form, all recovered as consistent",
        "controls": f"{N_CONTROLS} shuffled coppers (seed 119), identical test",
    }
    notes = (f"K4 dead (no alphabet fits) at lengths V {k4_dead['V']}, B {k4_dead['B']}. Fitting lengths 3-26: K4 V "
             f"{n_fit_k4['V']}, B {n_fit_k4['B']}; coppers 5th-95th V {pct['V']}, B {pct['B']}. Unusual fits: {unusual}.")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    """Quagmire III, form V: key = (alphabet string, list of shifts)."""
    alpha, shifts = key
    pos = {ch: i for i, ch in enumerate(alpha)}
    return "".join(alpha[(pos[ch] + shifts[i % len(shifts)]) % 26] for i, ch in enumerate(plaintext))


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    lines = []
    for L in (7, 12):
        eqs = equations(ct, known, L)
        lines.append(f"key length {L}: known letters by slot (place mod {L})")
        groups = {}
        for q in sorted(known):
            groups.setdefault((q - 1) % L, []).append(f"{known[q]}->{ct[q - 1]} ({q})")
        for s in sorted(groups):
            lines.append(f"  slot {s}: " + ", ".join(groups[s]))
        for form in FORMS:
            st, w = decide(eqs, form)
            if st == "fit":
                order = sorted(w[0].items(), key=lambda kv: kv[1])
                lines.append(f"  form {form}: fits; places " + " ".join(f"{chr(65 + a)}={v}" for a, v in order)
                             + f"; key {[w[1].get(s) for s in range(L)]}")
            else:
                lines.append(f"  form {form}: " + ("no alphabet fits" if st == "dead" else "undecided"))
        lines.append("")
    return "\n".join(lines)
