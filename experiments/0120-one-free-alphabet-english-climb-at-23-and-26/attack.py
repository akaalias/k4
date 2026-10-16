"""Experiment 0120. See program.md for the contract."""

EXPERIMENT = {
    "slug": "one-free-alphabet-english-climb-at-23-and-26",
    "title": "The two key lengths a free alphabet survives (Beaufort form, 23 and 26): climb the alphabet toward English with the 24 known letters fixed, against scrambled coppers at equal effort",
    "family": "1-keyed-periodic",
    "parent": "0119-one-free-alphabet-exact-at-every-key-length",
    "changed": (
        "F1.1, second step (English climb). 0119 left one unknown alphabet on both sides alive only in the Beaufort form "
        "at key lengths 23 (7 checks) and 26 (1 check). Consistency cannot decide those, so here the alphabet and the free "
        "key values are climbed by simulated annealing toward English on the 73 unknown letters, with the 24 known letters "
        "held by a penalty that must reach zero. The same climb, same effort, runs on 12 scrambled coppers per length that "
        "also fit at that length (drawn by 0119's exact test), and on 6 planted English texts per length to measure power."
    ),
    "hypothesis_expert": (
        "C27(c) (a tableau 'slightly different from the one on Kryptos'), C1(b) (the table alone). Model: one unknown "
        "bijection A on both sides, key k of length L in {23, 26}, Beaufort form A(c_i) = k[i mod L] - A(p_i) (decryption "
        "p_i = A^-1(k[i mod L] - A(c_i))); the 0119 exact test shows only these two (form, length) pairs admit any alphabet "
        "for 1-26. Given A, the key at every slot holding a known letter is forced (majority value; disagreements are "
        "violations); the remaining slots (6 at 23, 3 at 26) are free. Search: simulated annealing over A (swap two letters' "
        "places) and the free key values, objective = mean log10 quadgram score of the 73 non-crib letters (the harness's "
        "english_score of free_text) minus 1.0 per violation, linear cooling from 0.05 to 0.002, 20 restarts of 200,000 "
        "moves; only zero-violation states count. These settings were chosen in dry runs on planted texts before the run "
        "(penalty 0.4 and hotter schedules did worse); in those dry runs no setting got a planted text back, and the climb "
        "could not even return to the true alphabet from two swaps away, because one swap changes letters in every slot "
        "and the forced key values with them. Controls: shuffles of K4 that fit exactly at the same length and form (0119's decider), 12 per length, "
        "same restarts and iterations. Power: 6 planted texts per length, 97-letter windows of Carter's Tomb of "
        "Tut-ankh-Amen vol. 1 (knowledge/sources) with EASTNORTHEAST and BERLINCLOCK written in at 22 and 64, enciphered "
        "under a random alphabet and key of that length; a plant counts as found when the climb's best scores above every "
        "copper at that length. A key from such a climb costs about 88 bits for the alphabet plus 4.7 per key letter."
    ),
    "hypothesis_eli5": (
        "The last experiment showed that with one scrambled alphabet on both sides of the table, only two key lengths, 23 "
        "and 26, can produce the 24 known letters at all, and only with the table used the Beaufort way (key minus "
        "letter). For those two lengths we now let a computer shuffle the alphabet and the key bit by bit, keeping the "
        "known letters right, and push the other 73 letters toward English. A climb like this always makes some "
        "English-looking fragments, so the same climb is run on scrambled copies of the carved text; K4 only counts if it "
        "does better than all of them. To know whether the climb could find a real answer, we also hide real English "
        "under random alphabets and see whether the climb digs it out."
    ),
    "prediction": (
        "Power: the climb finds at least 4 of 6 planted texts at length 23 (best score above every copper) and at least 3 "
        "of 6 at 26. K4: its best zero-violation score lies inside the range of the 12 coppers at both lengths, so F1.1 "
        "closes as sampled at stated power. If plants are found in fewer than half the trials at a length, that length is "
        "recorded as not decidable by this climb and the item stays open there. A K4 score above every copper stops the "
        "queue for a replication against fresh coppers."
    ),
    "method": (
        "1. Draw 12 shuffles of K4 that fit at length 23 in the Beaufort form and 12 that fit at 26 (exact test from 0119). "
        "2. Build 6 planted texts per length from Carter's English. 3. For K4, each copper and each plant, run the same "
        "annealing climb (restarts x iterations fixed in the bounds) over the alphabet and the free key values, the known "
        "letters held by a penalty. 4. Keep the best zero-violation English score per text. 5. Compare K4 with the coppers "
        "per length; report the plants found and how many of their letters the climb got right."
    ),
    "walkthrough": (
        "1. Take key length 23 and write K4 in rows of 23, so each column is one key slot. "
        "2. Guess an order for the alphabet (26 letters in some sequence) and number its places 0-25. "
        "3. In a column holding a known letter, the key value is (place of the carved letter + place of the known letter) mod 26; every known letter in that column must give the same value. "
        "4. In the six columns with no known letter, guess a key value. "
        "5. Decipher every letter: known-letter place = key value minus carved-letter place, mod 26, read back through the alphabet. "
        "6. Score the 73 unknown letters by how English their four-letter groups are. "
        "7. Swap two letters of the alphabet or change one free key value; keep the change if the score improves (sometimes even if not, less often as the search cools); repeat many thousands of times. "
        "8. Do exactly the same with scrambled copies of K4 and with hidden English, and compare the best scores."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD

N = 97
LMAX = 26
FORMS = ("V", "B")
LENGTHS = (23, 26)
N_CONTROLS = 12
N_PLANTS = 6
RESTARTS = 20
ITERS = 200000
PENALTY = 1.0
T0, T1 = 0.05, 0.002


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


CARTER = "knowledge/sources/carter-1923-tomb-of-tutankhamen-vol1.txt"


def quad_table():
    from kryptos.scorer import _table
    logs, floor = _table()
    tab = [floor] * (26 ** 4)
    for q, v in logs.items():
        if len(q) == 4 and q.isalpha() and q.isupper():
            tab[((ord(q[0]) - 65) * 26 + ord(q[1]) - 65) * 676 + (ord(q[2]) - 65) * 26 + ord(q[3]) - 65] = v
    return tab, floor


def climb(text, known, L, seed, restarts=RESTARTS, iters=ITERS, init=None):
    """Simulated annealing over the alphabet (place of each letter) and the free key values, Beaufort form:
    p_i = a[(k[i mod L] - x[c_i]) mod 26]. Objective: mean quadgram log10 over the 73 free letters minus PENALTY per
    known letter whose slot's majority key disagrees. Returns the best zero-violation state found."""
    import math
    rng = random.Random(seed)
    tab, _ = quad_table()
    c = [ord(ch) - 65 for ch in text]
    free_pos = [i for i in range(N) if (i + 1) not in known]
    kn = [(q - 1, ord(known[q]) - 65) for q in sorted(known)]
    slot_kn = {}
    for i, p in kn:
        slot_kn.setdefault(i % L, []).append((c[i], p))
    free_slots = [s_ for s_ in range(L) if s_ not in slot_kn]
    nq = len(free_pos) - 3

    def evaluate(x, a, kf):
        k = [0] * L
        viol = 0
        for s_, lst in slot_kn.items():
            vals = [(x[ci] + x[pi]) % 26 for ci, pi in lst]
            if len(vals) == 1:
                k[s_] = vals[0]
            else:
                best = max(set(vals), key=vals.count)
                k[s_] = best
                viol += sum(1 for v in vals if v != best)
        for j, s_ in enumerate(free_slots):
            k[s_] = kf[j]
        pt = [a[(k[i % L] - x[c[i]]) % 26] for i in free_pos]
        sc = 0.0
        for j in range(nq):
            sc += tab[((pt[j] * 26 + pt[j + 1]) * 26 + pt[j + 2]) * 26 + pt[j + 3]]
        return sc / nq - PENALTY * viol, viol, k

    best = (-99.0, None, None, None)
    for _ in range(restarts):
        a = list(range(26)); rng.shuffle(a)               # a[place] = letter
        if init:                                          # validation only: start from a given alphabet
            a = [ord(ch) - 65 for ch in init]
        x = [0] * 26
        for pl, le in enumerate(a):
            x[le] = pl
        kf = [rng.randrange(26) for _ in free_slots]
        cur, viol, k = evaluate(x, a, kf)
        for it in range(iters):
            T = T0 + (T1 - T0) * it / iters
            if free_slots and rng.random() < 0.1:
                j = rng.randrange(len(free_slots)); old = kf[j]; kf[j] = rng.randrange(26)
                new, v2, k2 = evaluate(x, a, kf)
                if new >= cur or rng.random() < math.exp((new - cur) / T):
                    cur, viol, k = new, v2, k2
                else:
                    kf[j] = old
            else:
                l1, l2 = rng.sample(range(26), 2)
                p1, p2 = x[l1], x[l2]
                x[l1], x[l2] = p2, p1; a[p1], a[p2] = l2, l1
                new, v2, k2 = evaluate(x, a, kf)
                if new >= cur or rng.random() < math.exp((new - cur) / T):
                    cur, viol, k = new, v2, k2
                else:
                    x[l1], x[l2] = p1, p2; a[p1], a[p2] = l1, l2
            if viol == 0 and cur > best[0]:
                best = (cur, "".join(chr(65 + le) for le in a), list(k), None)
    if best[1] is None:
        return best
    alpha, k = best[1], best[2]
    pos = {ch: i for i, ch in enumerate(alpha)}
    pt = "".join(alpha[(k[i % L] - pos[text[i]]) % 26] for i in range(N))
    return (best[0], alpha, k, pt)


def beaufort_encrypt(pt, alpha, k):
    pos = {ch: i for i, ch in enumerate(alpha)}
    return "".join(alpha[(k[i % len(k)] - pos[ch]) % 26] for i, ch in enumerate(pt))


def make_plants(known, L, rng, n, with_key=False):
    import re
    src = re.sub("[^A-Z]", "", open(CARTER, errors="ignore").read().upper())
    out = []
    for _ in range(n):
        s0 = rng.randrange(20000, len(src) - 200)
        pt = list(src[s0:s0 + N])
        for q, ch in known.items():
            pt[q - 1] = ch
        pt = "".join(pt)
        alpha = list(STD); rng.shuffle(alpha); alpha = "".join(alpha)
        k = [rng.randrange(26) for _ in range(L)]
        out.append((beaufort_encrypt(pt, alpha, k), pt) + ((alpha, k) if with_key else ()))
    return out


def _job(args):
    kind, L, idx, text, truth, seed = args
    from kryptos.facts import KNOWN
    sc, alpha, k, pt = climb(text, KNOWN, L, seed)
    agree = sum(1 for a_, b_ in zip(pt, truth) if a_ == b_) if (pt and truth) else None
    return kind, L, idx, sc, alpha, k, pt, agree


def run(ctx):
    import multiprocessing as mp
    from kryptos.scorer import english_score, free_text
    ct, known = ctx.K4, ctx.KNOWN
    rng = random.Random(120)
    jobs = []
    truth_scores = {}
    for L in LENGTHS:
        assert decide(equations(ct, known, L), "B")[0] == "fit"
        jobs.append(("k4", L, 0, ct, None, rng.randrange(10 ** 9)))
        got = 0
        while got < N_CONTROLS:
            sh = list(ct); rng.shuffle(sh); sh = "".join(sh)
            if decide(equations(sh, known, L), "B", rng)[0] == "fit":
                jobs.append(("copper", L, got, sh, None, rng.randrange(10 ** 9))); got += 1
        for i, (pc, pt) in enumerate(make_plants(known, L, rng, N_PLANTS)):
            truth_scores[(L, i)] = english_score(free_text(pt))
            jobs.append(("plant", L, i, pc, pt, rng.randrange(10 ** 9)))
    jobs.sort(key=lambda j: j[0] != "k4")
    import sys, types                    # the harness loads this file without registering it; pickling _job needs that
    if getattr(sys.modules.get(__name__), "_job", None) is not _job:
        m = types.ModuleType(__name__); m.__dict__.update(globals()); sys.modules[__name__] = m
    with mp.get_context("fork").Pool(8) as pool:
        res = pool.map(_job, jobs, chunksize=1)
    out = {L: {"k4": None, "copper": [], "plant": []} for L in LENGTHS}
    cands = []
    for kind, L, idx, sc, alpha, k, pt, agree in res:
        # re-score with the harness's own function
        es = english_score(free_text(pt)) if pt else None
        if kind == "k4":
            out[L]["k4"] = {"score": es, "plaintext": pt, "alphabet": alpha, "key": k}
            if pt:
                cands.append({"plaintext": pt, "key": {"alphabet": alpha, "shifts": k, "form": "beaufort"},
                              "key_description": f"Beaufort form, one alphabet {alpha} on both sides, key length {L}",
                              "notes": f"length {L}, climbed"})
        elif kind == "copper":
            out[L]["copper"].append(es)
        else:
            out[L]["plant"].append({"score": es, "truth": truth_scores[(L, idx)], "letters_right": agree,
                                    "found": None})
    summary = {}
    for L in LENGTHS:
        cs = [x for x in out[L]["copper"] if x is not None]
        top = max(cs) if cs else None
        for pl in out[L]["plant"]:
            pl["found"] = (pl["score"] is not None and top is not None and pl["score"] > top)
        k4s = out[L]["k4"]["score"]
        summary[L] = {"k4": k4s, "coppers_min": min(cs) if cs else None, "coppers_max": top,
                      "k4_above_all_coppers": (k4s is not None and top is not None and k4s > top),
                      "plants_found": sum(1 for pl in out[L]["plant"] if pl["found"]),
                      "plants_letters_right": [pl["letters_right"] for pl in out[L]["plant"]],
                      "plants_scores": [round(pl["score"], 3) if pl["score"] else None for pl in out[L]["plant"]],
                      "plants_true_scores": [round(pl["truth"], 3) for pl in out[L]["plant"]]}
    controls = []
    for L in LENGTHS:
        controls += [x for x in out[L]["copper"] if x is not None]
    bounds = {
        "family": "one unknown alphabet on both sides, Beaufort form, periodic key 23 or 26, no move (the only pairs 0119 left)",
        "search": f"simulated annealing, {RESTARTS} restarts x {ITERS:,} moves per text, penalty {PENALTY} per known-letter violation, T {T0}->{T1}",
        "not_exhaustive": True,
        "coppers_per_length": N_CONTROLS, "plants_per_length": N_PLANTS,
        "summary": {str(L): v for L, v in summary.items()},
        "coppers_scores": {str(L): [round(x, 3) for x in out[L]["copper"] if x is not None] for L in LENGTHS},
        "k4_best": {str(L): out[L]["k4"] for L in LENGTHS},
        "controls": f"{N_CONTROLS} shuffled coppers per length that fit exactly at that length and form (seed 120), identical climb",
    }
    notes = "; ".join(f"L{L}: K4 {summary[L]['k4']:.3f}, coppers {summary[L]['coppers_min']:.3f} to {summary[L]['coppers_max']:.3f}, "
                      f"plants found {summary[L]['plants_found']}/{N_PLANTS} (letters right {summary[L]['plants_letters_right']})"
                      for L in LENGTHS)
    return {"candidates": cands, "bounds": bounds, "notes": notes, "controls": controls}


def encrypt(plaintext, key):
    """Beaufort form on one alphabet: carved place = key value minus message place, mod 26."""
    return beaufort_encrypt(plaintext, key["alphabet"], key["shifts"])


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    L = 23
    lines = [f"key length {L}, Beaufort form: K4 in rows of {L}; each column is one key slot", ""]
    for r in range(0, N, L):
        lines.append("  " + " ".join(ct[r:r + L]))
    lines.append("")
    slots = {}
    for q in sorted(known):
        slots.setdefault((q - 1) % L, []).append(q)
    shared = {s_: qs for s_, qs in slots.items() if len(qs) > 1}
    lines.append("columns holding two known letters (each gives one check: place(c1)+place(p1) = place(c2)+place(p2)):")
    for s_, qs in sorted(shared.items()):
        lines.append(f"  column {s_}: " + ", ".join(f"{known[q]} under {ct[q - 1]} ({q})" for q in qs))
    if key:
        alpha, k = key["alphabet"], key["shifts"]
        pos = {ch: i for i, ch in enumerate(alpha)}
        lines += ["", f"best climbed alphabet: {alpha}", f"key values: {k}"]
        q = 22
        lines.append(f"place 22: carved {ct[21]} at {pos[ct[21]]}, key {k[21 % L]}: {k[21 % L]} - {pos[ct[21]]} = "
                     f"{(k[21 % L] - pos[ct[21]]) % 26} -> {alpha[(k[21 % L] - pos[ct[21]]) % 26]}")
    return "\n".join(lines)
