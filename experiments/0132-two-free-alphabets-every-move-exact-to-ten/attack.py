"""Experiment 0132. See program.md for the contract."""

EXPERIMENT = {
    "slug": "two-free-alphabets-every-move-exact-to-ten",
    "title": "Two alphabets in unknown orders (Quagmire IV) after or before every move of the type-1 library: exact at key lengths 1-10 on K4 and ten coppers, the per-slot test at 11-26",
    "family": "6-transposition-then-tableau",
    "parent": "0131-two-free-alphabets-after-every-move-exact",
    "changed": (
        "F6.2, second attempt. 0131 ran the exact two-alphabet decider at every key length and ran out of its budget "
        "after 10,625 of 27,852 moves with no copper comparison done (incomplete; item left open). Timing since: the "
        "decider costs about 4 ms per move for lengths 1-10 in both orders but 0.2 s at 11-12 and more above, where 97-99% "
        "of settings that pass the per-slot test fit anyway (0131: 7,072 of 7,152 at 26). So here: exact decision at "
        "lengths 1-10, both orders, every move, on K4 and on ten scrambled coppers; at 11-26 the per-slot test (exact as a "
        "refutation: a setting failing it is dead) on every move and text, and the full decider on K4 for 300 sampled "
        "moves to state the fit rate."
    ),
    "hypothesis_expert": (
        "C1(a) (Sanborn, CNN 2005, knowledge/sources/cnn-2005-sanborn-interview-transcript.txt: 'I used a matrix code... "
        "and then went back to this table to do the ultimate'), C27(c) (a table 'slightly different from the one on "
        "Kryptos'), C2(a). Model: the type-1 library (27,852 maps, as 0097 and 0129) and Quagmire IV: C(c) = P(m) + "
        "k[slot], P and C independent unknown bijections, slot = carved place (order A: move, then table) or message "
        "place (order B: table, then move). The Beaufort form is the same family with P reflected; a key alphabet drops "
        "out. Exact decision as 0123 (mod 13 and mod 2, each alphabet one-to-one; enumerate at rank <= 5, else depth-first "
        "search, 200,000 nodes, 'undecided' reported); every fit re-checked. The per-slot test (within a slot, known to "
        "carved must be one-to-one) is implied by the model. 0100 and 0102 found Quagmire IV at period 3 after a move "
        "marginal (12 distinct check sets against 0-11, p about 0.24 after selection) under 0097's relaxation; this run "
        "decides period 3 exactly on all moves and ten coppers."
    ),
    "hypothesis_eli5": (
        "The table may use one scrambled alphabet to look up the message letter and a second one to write the carved "
        "letter. For every one of about 28,000 ways of moving the letters, before or after the table, and every key "
        "length up to 10, arithmetic on the 24 known letters decides whether any such pair of alphabets could work. For "
        "longer keys almost everything that passes a quick check fits, so the quick check is used there. Scrambled "
        "copies of the carved text go through the same test."
    ),
    "prediction": (
        "K4's fits per (order, length) at 1-10, and its per-slot survivors at 11-26, lie at the coppers' rate: K4 is above "
        "all ten coppers in no more of the 52 cells than the most any single copper manages against the rest. Period 3 "
        "after a move (0131 found 6 fits on part of the library) is inside the coppers' range. On the K4 sample at 11-26, "
        "at least 90% of per-slot survivors fit. A K4 count beyond the null stops the queue. Zero candidates."
    ),
    "method": (
        "1. Build the 27,852 moves. "
        "2. For each move, order and key length, write the 24 equations; apply the per-slot test. "
        "3. Lengths 1-10: decide the survivors exactly, on K4 and ten scrambled coppers, every move. "
        "4. Lengths 11-26: count per-slot survivors on every text; on K4 for 300 sampled moves, decide them exactly. "
        "5. Per cell (order, length), K4 against the coppers; cells where K4 is above every copper, against each copper "
        "against the rest. 6. Validate on planted Quagmire IV texts."
    ),
    "walkthrough": (
        "1. Pick a move, say a clockwise quarter turn of a grid 7 wide, and write where each known letter lands in the carved text. "
        "2. Pick a key length, say 9, and an order: each known letter's slot is its landing place mod 9 (move first) or its message place mod 9 (table first). "
        "3. Write one line per known letter: place of the carved letter in the cipher alphabet = place of the known letter in the plain alphabet + key value of the slot. "
        "4. If one slot has the same known letter under two carved letters, or two known letters under one carved letter, stop: dead. "
        "5. Otherwise solve the lines mod 13 and mod 2; if two letters of one alphabet are always forced onto one place, dead. "
        "6. Else look for two alphabets and a key that satisfy every line; if found, check it: the setting fits. "
        "7. Repeat for every move, both orders and key lengths 1-10, and on scrambled copies; for longer keys stop at step 4."
    ),
}

import random
import time
from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.ciphers import columnar_transposition_encrypt
from kryptos.alphabets import numeric_order

N = 97
LMAX = 26
FORMS = ("IV",)
ORDERS = ("A", "B")
LEXACT = 10
K4_LONG_SAMPLE = 300
N_CONTROLS = 10
SAMPLE = 700
WORKERS = 5
EXTRA = ["EGYPT", "CAIRO", "LUXOR", "WALL", "NOVEMBER", "MESSAGE", "DELIVER", "DELIVERING", "TRANSMIT"]
CELLS = [(o, f, L) for o in ORDERS for f in FORMS for L in range(1, LMAX + 1)]


# ---- exact decider, from 0119 ----

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
NODE_LIMIT = 40000


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


def l1_ok(eqs):
    f, g = {}, {}
    for s, a, c in eqs:
        if f.setdefault((s, a), c) != c or g.setdefault((s, c), a) != a:
            return False
    return True



# ---- the type-1 move library, from 0097 ----

def perm_of(fn):
    idx = "".join(chr(0x100 + i) for i in range(N))
    return [ord(ch) - 0x100 for ch in fn(idx)]


def rot_cw(s, w):
    rows = [s[i:i + w] for i in range(0, len(s), w)]
    return "".join(r[c] for c in range(w) for r in reversed(rows) if c < len(r))


def rot_ccw(s, w):
    rows = [s[i:i + w] for i in range(0, len(s), w)]
    return "".join(r[c] for c in reversed(range(w)) for r in rows if c < len(r))


def keyword_sequence(word):
    rank = numeric_order(word)
    return sorted(range(len(rank)), key=lambda c: rank[c])


def full_sequence(word):
    w = [c for c in word.upper() if c.isalpha()]
    return sorted(range(len(w)), key=lambda c: (w[c], c))


def route_fns(vocab):
    for b in range(1, N):
        for a in range(N):
            def f(s, a=a, b=b):
                out = [""] * N
                for i in range(N):
                    out[(a + b * i) % N] = s[i]
                return "".join(out)
            yield f"K3 rule a={a} b={b}", f
    for w in range(2, N):
        yield f"turn cw {w}", (lambda s, w=w: rot_cw(s, w))
        yield f"turn ccw {w}", (lambda s, w=w: rot_ccw(s, w))
        yield f"columnar {w}", (lambda s, o=list(range(w)): columnar_transposition_encrypt(s, o))
        yield f"columnar rtl {w}", (lambda s, o=list(range(w))[::-1]: columnar_transposition_encrypt(s, o))
    for w1 in range(2, N):
        for w2 in range(2, N):
            yield f"two turns cw {w1},{w2}", (lambda s, a=w1, b=w2: rot_cw(rot_cw(s, a), b))
    words = sorted({w for w in vocab if 2 <= len(w) <= 30} | set(EXTRA))
    for word in words:
        for how, seq in (("repeats dropped", keyword_sequence(word)), ("full word", full_sequence(word))):
            if len(seq) >= 2:
                yield f"keyword {word} ({how})", (lambda s, o=list(seq): columnar_transposition_encrypt(s, o))


def route_library(vocab):
    """Distinct 'where' maps (where[i] = place in the moved text of letter i), forward and inverse."""
    seen, lib = set(), []
    for name, f in route_fns(vocab):
        sigma = perm_of(f)                    # moved[j] = orig[sigma[j]]
        fwd = [0] * N
        for j, i in enumerate(sigma):
            fwd[i] = j
        for tag, w in ((name, fwd), (name + " inverse", sigma)):
            t = tuple(w)
            if t not in seen:
                seen.add(t); lib.append((tag, t))
    return lib




def setting_eqs(text, known_list, land, o, L):
    """(slot, plain index, cipher index) for the 24 known letters under a move (land = carved place of each)."""
    return [((land[e] if o == "A" else q - 1) % L, a, ord(text[land[e]]) - 65) for e, (q, a) in enumerate(known_list)]


def job(text, known_list, where, rng, long=False):
    """Status per cell for one text and one move: 0 per-slot dead, 1 dead, 2 fit, 3 undecided, 4 per-slot survivor
    not decided (lengths above LEXACT unless long)."""
    land = [where[q - 1] for q, _ in known_list]
    out = bytearray(len(CELLS))
    for ci, (o, form, L) in enumerate(CELLS):
        eqs = setting_eqs(text, known_list, land, o, L)
        if not l1_ok(eqs):
            continue
        if L > LEXACT and not long:
            out[ci] = 4
            continue
        st, w = decide(eqs, "V", rng, two=True)
        if st == "fit":
            assert check_witness(eqs, w)
            out[ci] = 2
        else:
            out[ci] = 1 if st == "dead" else 3
    return bytes(out)


def worker(jobs, texts, known_list, lib, deadline, seed, q):
    rng = random.Random(seed)
    res = {}
    for t, r, long in jobs:
        if time.time() > deadline:
            break
        res[(t, r, long)] = job(texts[t], known_list, lib[r][1], rng, long)
    q.put(res)


def planted(where, o, form, L, rng):
    """A random message with the known letters in place, moved and enciphered under a random alphabet and key."""
    from kryptos.facts import KNOWN
    order = list(range(26)); rng.shuffle(order)            # plain alphabet: order[letter] = place
    corder = list(range(26)); rng.shuffle(corder)          # cipher alphabet
    inv = {v: i for i, v in enumerate(corder)}
    key = [rng.randrange(26) for _ in range(L)]
    sgn = 1
    pt = [rng.randrange(26) for _ in range(N)]
    for q, ch in KNOWN.items():
        pt[q - 1] = ord(ch) - 65
    if o == "A":
        moved = [0] * N
        for i in range(N):
            moved[where[i]] = pt[i]
        ct = [inv[(sgn * order[m] + key[j % L]) % 26] for j, m in enumerate(moved)]
    else:
        sub = [inv[(sgn * order[p] + key[i % L]) % 26] for i, p in enumerate(pt)]
        ct = [0] * N
        for i in range(N):
            ct[where[i]] = sub[i]
    return "".join(chr(65 + x) for x in ct)


def run(ctx):
    import multiprocessing as mp
    ct, known = ctx.K4, ctx.KNOWN
    known_list = [(q, ord(known[q]) - 65) for q in sorted(known)]
    lib = route_library(ctx.vocabulary)
    rng = random.Random(132)
    for L, o in ((3, "A"), (5, "B"), (7, "A"), (8, "B"), (10, "A"), (14, "B")):
        tag, where = lib[rng.randrange(len(lib))]
        t = planted(where, o, "IV", L, rng)
        st = job(t, known_list, where, rng, long=True)[CELLS.index((o, "IV", L))]
        assert st == 2, (tag, o, L, st)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    long_sample = sorted(rng.sample(range(len(lib)), K4_LONG_SAMPLE))
    jobs = [(t, r, False) for t in range(len(texts)) for r in range(len(lib))] + [(0, r, True) for r in long_sample]
    rng.shuffle(jobs)
    deadline = time.time() + ctx.time_left() - 120
    mpc = mp.get_context("fork")
    q = mpc.Queue()
    procs = [mpc.Process(target=worker, args=(jobs[i::WORKERS], texts, known_list, lib, deadline, 1000 + i, q))
             for i in range(WORKERS)]
    for p in procs:
        p.start()
    res = {}
    for _ in procs:
        res.update(q.get())
    for p in procs:
        p.join()
    T = len(texts)
    done = [r for r in range(len(lib)) if all((t, r, False) in res for t in range(T))]
    nC = len(CELLS)
    # statistic per cell: exact fits at L <= LEXACT, per-slot survivors above
    def stat(t, ci):
        L = CELLS[ci][2]
        want = (2,) if L <= LEXACT else (2, 3, 4)
        return sum(res[(t, r, False)][ci] in want for r in done)
    cnt = [[stat(t, ci) for ci in range(nC)] for t in range(T)]
    und = [sum(res[(t, r, False)][ci] == 3 for r in done for ci in range(nC)) for t in range(T)]

    def above_rest(t):
        return [ci for ci in range(nC) if cnt[t][ci] > max(cnt[u][ci] for u in range(T) if u != t)]
    k4_above = above_rest(0)
    null_above = [len(above_rest(t)) for t in range(1, T)]
    stop = len(k4_above) > max(null_above)
    low_fits = []
    for r in done:
        st = res[(0, r, False)]
        for ci, (o, f, L) in enumerate(CELLS):
            if st[ci] == 2 and L <= 5:
                low_fits.append({"route": lib[r][0], "order": o, "L": L})
    longd = [r for r in long_sample if (0, r, True) in res]
    long_rate = {}
    for o in ORDERS:
        surv = fit = undec = 0
        for r in longd:
            st = res[(0, r, True)]
            for L in range(LEXACT + 1, LMAX + 1):
                x = st[CELLS.index((o, "IV", L))]
                surv += x > 0; fit += x == 2; undec += x == 3
        long_rate[o] = {"per_slot_survivors": surv, "fit": fit, "undecided": undec,
                        "fit_share": round(fit / surv, 4) if surv else None}
    summary = {}
    for o in ORDERS:
        cis = [CELLS.index((o, "IV", L)) for L in range(1, LMAX + 1)]
        summary[o] = {
            "statistic_by_L": "exact fits at 1-10, per-slot survivors at 11-26",
            "k4_by_L": [cnt[0][ci] for ci in cis],
            "coppers_min_by_L": [min(cnt[t][ci] for t in range(1, T)) for ci in cis],
            "coppers_max_by_L": [max(cnt[t][ci] for t in range(1, T)) for ci in cis],
            "smallest_L_with_k4_fit": next((L for L in range(1, LEXACT + 1) if cnt[0][CELLS.index((o, "IV", L))]), None),
        }
    bounds = {
        "family": "two unknown alphabets (Quagmire IV, Beaufort included by reflection), periodic key 1-26, after (A) or before (B) a type-1 move",
        "moves": len(lib), "moves_done_all_texts": len(done),
        "exhaustive": f"exact decision at key lengths 1-{LEXACT} (0123's decider); per-slot refutation at {LEXACT + 1}-26; exact at {LEXACT + 1}-26 on {len(longd)} sampled moves for K4",
        "summary": summary, "k4_long_lengths_fit_rate_on_sample": long_rate,
        "k4_fits_at_L_le_5": low_fits[:60], "n_k4_fits_at_L_le_5": len(low_fits),
        "cells_k4_above_every_copper": [CELLS[ci] for ci in k4_above],
        "null_cells_above_rest_per_copper": null_above, "undecided_k4_and_coppers": und, "stop_queue": stop,
        "controls": f"{N_CONTROLS} shuffled coppers (seed 132), every move",
        "plants": "6 planted Quagmire IV texts (random move, both orders, lengths 3-14) decided 'fit'",
    }
    notes = (f"{len(done):,} of {len(lib):,} moves on K4 and {N_CONTROLS} coppers. Smallest key length with a K4 fit: "
             f"{ {o: summary[o]['smallest_L_with_k4_fit'] for o in ORDERS} }; fits at L<=5: {len(low_fits)}. K4 above every "
             f"copper in {len(k4_above)} of {nC} cells; each copper against the rest {min(null_above)}-{max(null_above)}. "
             f"Long lengths on the K4 sample: {long_rate}. Stop queue: {stop}.")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    """key: {'where': carved place of each message letter, 'order': 'A' or 'B', 'plain_alphabet' and
    'cipher_alphabet': 26 letters each in place order, 'shifts': list}. Quagmire IV: C(c) = P(p) + k."""
    alpha, sh, where = key["cipher_alphabet"], key["shifts"], key["where"]
    pos = {ch: i for i, ch in enumerate(key["plain_alphabet"])}
    sgn = 1
    L = len(sh)
    if key["order"] == "A":
        moved = [""] * len(plaintext)
        for i, ch in enumerate(plaintext):
            moved[where[i]] = ch
        return "".join(alpha[(sgn * pos[ch] + sh[j % L]) % 26] for j, ch in enumerate(moved))
    sub = [alpha[(sgn * pos[ch] + sh[i % L]) % 26] for i, ch in enumerate(plaintext)]
    out = [""] * len(plaintext)
    for i, ch in enumerate(sub):
        out[where[i]] = ch
    return "".join(out)


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    known_list = [(q, ord(known[q]) - 65) for q in sorted(known)]
    where = route_library(ctx.vocabulary)
    tag, wh = next(((t, w) for t, w in where if t == "turn cw 7"), where[0])
    land = [wh[q - 1] for q, _ in known_list]
    lines = [f"move: {tag} (write the message in rows of 7, read the columns bottom to top); then the table, key length 9", "",
             "place  known  lands at  carved  slot (landing place mod 9)"]
    for (q, a), j in zip(known_list, land):
        lines.append(f"{q:5d}  {chr(65 + a):>5}  {j + 1:8d}  {ct[j]:>6}  {j % 9:4d}")
    for form in FORMS:
        eqs = setting_eqs(ct, known_list, land, "A", 9)
        if not l1_ok(eqs):
            lines.append(f"a slot sends one known letter to two carved letters (or two to one): dead")
            continue
        st, w = decide(eqs, "V", random.Random(1), two=True)
        if st == "fit":
            for side, name in (("P", "plain"), ("C", "cipher")):
                order = sorted(((a, v) for a, v in w[0].items() if a[0] == side), key=lambda kv: kv[1])
                lines.append(f"fits; {name} places " + " ".join(f"{chr(65 + a[1])}={v}" for a, v in order))
            lines.append(f"key {[w[1].get(s) for s in range(9)]}")
        else:
            lines.append("no pair of alphabets fits" if st == "dead" else "undecided")
    return "\n".join(lines)
