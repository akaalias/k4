"""Experiment 0130. See program.md for the contract."""

EXPERIMENT = {
    "slug": "one-free-alphabet-before-every-move-exact",
    "title": "A table built on one alphabet in an unknown order, then every move of the type-1 library, key lengths 1-26, decided exactly",
    "family": "6-transposition-then-tableau",
    "parent": "0129-one-free-alphabet-after-every-move-exact",
    "changed": (
        "F6.1 (one free alphabet after or before each move), order B (the table, then the move), the half 0129 left "
        "because both orders do not fit one 30-minute budget. 0097 tested this only with a relaxation "
        "that can refute but not confirm, at key lengths 3, 7 and 21, and only in the added (Vigenere-like) form; that "
        "made it weak. Here 0119's exact decider (mod 13 and mod 2, exhaustive where the solution space is small, a "
        "depth-first search with a node limit elsewhere, every fit re-checked) runs on every one of the 27,852 moves, "
        "key lengths 1-26, both table forms (added and Beaufort). Controls: 12 scrambled coppers on a fixed "
        "sample of 800 moves, with K4 counted on the same sample."
    ),
    "hypothesis_expert": (
        "C1(a) (Sanborn, CNN 2005, knowledge/sources/cnn-2005-sanborn-interview-transcript.txt: 'I used a matrix code, "
        "and then we can possibly use this code to decipher with... double matrixes and triple matrixes... and then went "
        "back to this table to do the ultimate'), C27(c) (his table 'slightly different from the one on Kryptos'), C2(a). "
        "Model: plaintext p moved by a permutation pi of the type-1 library (K3's rule a + b i mod 97 at all 9,312 "
        "settings, one quarter turn cw/ccw at widths 2-96, two cw turns at every width pair, plain columnar both ways, "
        "keyed columnar from the vocabulary and theme words, each forward and inverse: 27,852 distinct maps, as 0097), "
        "and one unknown bijection A on both sides of a periodic table with key k of length L. Order B only (table, "
        "then move): A(c_pi(i)) = s A(p_i) + k[i mod L], slot = message place i; order A was 0129. "
        "Form V: s = +1 (Quagmire III with free order; variant Beaufort is V with k negated); form B: s = -1 (Beaufort). "
        "The 24 known letters give 24 equations over Z26; exact decision as 0119 (refute when two letters coincide mod 13 "
        "and mod 2, or three mod 13; enumerate the mod-13 space up to scaling at rank <= 5; else 300 random points as a "
        "witness hunt, then depth-first search with pruning, 200,000 nodes, 'undecided' reported). A per-slot filter "
        "(each slot one-to-one) runs first; it is implied by the model, so it loses nothing. Zekios (2026, research note "
        "combined_methods_and_sevens.md) did any-alphabet keys only to period 12 and only for double rotations."
    ),
    "hypothesis_eli5": (
        "Sanborn said he wrote the message into a grid and read it out another way (a 'matrix'), then used the big "
        "lettered table. Earlier tests fixed the table's alphabet to the plain A-Z or the KRYPTOS one. Here the table's "
        "scrambled alphabet may be any of the possible orders, and for each of about 28,000 ways of moving the letters, "
        "each key length up to 26 and two ways of reading the table, arithmetic on the 24 known letters decides whether "
        "any alphabet and key could work at all. We do the same on scrambled copies of the carved text to see how often "
        "that happens by chance."
    ),
    "prediction": (
        "K4 has fitting settings at key lengths of about 7 and up in both forms, at the rate of the scrambled "
        "coppers: in no more cells (form, length) is K4 above all 12 coppers than the most any single copper "
        "manages against the rest. Key lengths 1-5 have no fit (a dry run on 1,000 moves found the first fits at 6). If K4 beats that null count, the queue "
        "stops for a replication (cells where K4 fits and no copper does are listed, and count in it). Zero candidates; fits that "
        "remain are at the coppers' rate and only an English climb could judge them, which 0120 found powerless, so "
        "they are blocked, not open."
    ),
    "method": (
        "1. Build the 27,852 moves of the type-1 library. "
        "2. For each move, key length 1-26 and form, write the 24 equations (slot, known letter, carved letter at "
        "the place the move sends it). "
        "3. Drop settings that fail the per-slot test; decide the rest exactly (dead, fit with a re-checked witness, or "
        "undecided at the node limit). "
        "4. The same on 12 scrambled coppers over a fixed random sample of 800 moves. "
        "5. Per cell (form, length): K4's fits on the sample against the coppers'; count cells where K4 is above "
        "every copper and compare with the same count for each copper against the rest. "
        "6. Validate on planted texts (random move, form, length, alphabet and key must decide 'fit')."
    ),
    "walkthrough": (
        "1. Pick a move, say a clockwise quarter turn of a grid 7 wide, and write where each of the 24 known letters lands in the carved text. "
        "2. Pick a key length, say 9, and the order 'table first': each known letter's slot is its own place in the message mod 9. "
        "3. Write one line per known letter: place-in-alphabet of the carved letter there = place of the known letter + key value of the slot (all unknown). "
        "4. If two known letters in one slot sit under the same carved letter but differ, or the same known letter under two carved letters, stop: dead. "
        "5. Otherwise solve the 24 lines mod 13 and mod 2; if two different letters are always forced onto the same place, dead. "
        "6. Else look for one alphabet and key that satisfy every line; if found, check it, and the setting fits. "
        "7. Repeat for every move, key lengths 1-26, the Beaufort form (carved place = key minus known place), and on scrambled copies."
    ),
}

import random
import time
from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.ciphers import columnar_transposition_encrypt
from kryptos.alphabets import numeric_order

N = 97
LMAX = 26
FORMS = ("V", "B")
ORDERS = ("B",)
N_CONTROLS = 12
SAMPLE = 800
WORKERS = 6
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
PRETRY = 0


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
    if rank > ENUM_MAX_RANK and rng is not None:
        # cheap witness hunt first (new in 0129): random points of the mod-13 space; a hit is a re-checked fit,
        # a miss decides nothing and the exact search below runs as in 0119
        for _ in range(PRETRY):
            w = test_u([rng.randrange(13) for _ in range(rank)])
            if w:
                return ("fit", w)
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


def job(text, known_list, where, rng):
    """Status per cell for one text and one move: 0 per-slot dead, 1 dead, 2 fit, 3 undecided."""
    land = [where[q - 1] for q, _ in known_list]
    out = bytearray(len(CELLS))
    for ci, (o, form, L) in enumerate(CELLS):
        eqs = setting_eqs(text, known_list, land, o, L)
        if not l1_ok(eqs):
            continue
        st, w = decide(eqs, form, rng)
        if st == "fit":
            assert check_witness(eqs, form, w)
            out[ci] = 2
        else:
            out[ci] = 1 if st == "dead" else 3
    return bytes(out)


def worker(jobs, texts, known_list, lib, deadline, seed, q):
    rng = random.Random(seed)
    res = {}
    for t, r in jobs:
        if time.time() > deadline:
            break
        res[(t, r)] = job(texts[t], known_list, lib[r][1], rng)
    q.put(res)


def planted(where, o, form, L, rng):
    """A random message with the known letters in place, moved and enciphered under a random alphabet and key."""
    from kryptos.facts import KNOWN
    order = list(range(26)); rng.shuffle(order)            # order[letter] = place
    inv = {v: i for i, v in enumerate(order)}
    key = [rng.randrange(26) for _ in range(L)]
    sgn = 1 if form == "V" else -1
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
    rng = random.Random(129)
    # validation: planted texts fit at their own setting
    for L, o, form in ((5, "B", "V"), (9, "B", "B"), (14, "B", "B"), (21, "B", "V"), (3, "B", "V"), (7, "B", "B")):
        tag, where = lib[rng.randrange(len(lib))]
        t = planted(where, o, form, L, rng)
        st = job(t, known_list, where, rng)[CELLS.index((o, form, L))]
        assert st == 2, (tag, o, form, L, st)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    sample = sorted(rng.sample(range(len(lib)), SAMPLE))
    jobs = [(0, r) for r in range(len(lib))] + [(t, r) for t in range(1, len(texts)) for r in sample]
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
    # K4 over the whole library
    k4_done = [r for r in range(len(lib)) if (0, r) in res]
    k4_fit = {c: 0 for c in CELLS}
    k4_und = {c: 0 for c in CELLS}
    k4_l1 = {c: 0 for c in CELLS}
    fits_low = []
    for r in k4_done:
        st = res[(0, r)]
        for ci, c in enumerate(CELLS):
            k4_l1[c] += st[ci] > 0
            k4_fit[c] += st[ci] == 2
            k4_und[c] += st[ci] == 3
            if st[ci] == 2 and c[2] <= 8:
                fits_low.append({"route": lib[r][0], "order": c[0], "form": c[1], "L": c[2]})
    # sample comparison: only moves done for every text
    samp = [r for r in sample if all((t, r) in res for t in range(len(texts)))]
    cnt = [[sum(res[(t, r)][ci] == 2 for r in samp) for ci in range(len(CELLS))] for t in range(len(texts))]
    und = [sum(res[(t, r)][ci] == 3 for r in samp for ci in range(len(CELLS))) for t in range(len(texts))]

    def above_rest(t):
        return [ci for ci in range(len(CELLS))
                if cnt[t][ci] > max(cnt[u][ci] for u in range(len(texts)) if u != t)]
    k4_above = above_rest(0)
    null_above = [len(above_rest(t)) for t in range(1, len(texts))]
    no_copper_fits = [CELLS[ci] for ci in range(len(CELLS))
                      if cnt[0][ci] > 0 and all(cnt[t][ci] == 0 for t in range(1, len(texts)))]
    stop = len(k4_above) > max(null_above)

    def by_len(d, o, f):
        return [d[(o, f, L)] for L in range(1, LMAX + 1)]
    summary = {}
    for o in ORDERS:
        for f in FORMS:
            cis = [CELLS.index((o, f, L)) for L in range(1, LMAX + 1)]
            summary[f"{o}{f}"] = {
                "k4_fits_full_library_by_L": by_len(k4_fit, o, f),
                "k4_per_slot_survivors_by_L": by_len(k4_l1, o, f),
                "k4_undecided_by_L": by_len(k4_und, o, f),
                "k4_fits_sample_by_L": [cnt[0][ci] for ci in cis],
                "coppers_fits_sample_min_by_L": [min(cnt[t][ci] for t in range(1, len(texts))) for ci in cis],
                "coppers_fits_sample_max_by_L": [max(cnt[t][ci] for t in range(1, len(texts))) for ci in cis],
                "smallest_L_with_k4_fit": next((L for L in range(1, LMAX + 1) if k4_fit[(o, f, L)]), None),
            }
    bounds = {
        "family": "one unknown alphabet on both sides (Quagmire III / Beaufort with a free order), periodic key 1-26, before a type-1 move (order B)",
        "moves": len(lib), "k4_moves_done": len(k4_done),
        "cells": "order B (table, then move) x 2 forms x key lengths 1-26",
        "exhaustive": "exact decision per setting (0119's decider; undecided counted where the node limit was hit)",
        "summary": summary,
        "k4_fits_at_L_le_8": fits_low[:60], "n_k4_fits_at_L_le_8": len(fits_low),
        "controls": f"{N_CONTROLS} shuffled coppers (seed 129) on {len(samp)} sampled moves; K4 on the same sample",
        "cells_k4_above_every_copper": [CELLS[ci] for ci in k4_above],
        "null_cells_above_rest_per_copper": null_above,
        "cells_k4_fits_no_copper_does": no_copper_fits,
        "undecided_sample_k4_and_coppers": und,
        "stop_queue": stop,
        "plants": "6 planted texts (random move, order B, form, length 3-21) all decided 'fit'",
    }
    low = {k: v["smallest_L_with_k4_fit"] for k, v in summary.items()}
    notes = (f"K4 on {len(k4_done):,} of {len(lib):,} moves; smallest key length with a fit {low}; fits at L<=8: "
             f"{len(fits_low)}. Sample of {len(samp)} moves: K4 above every copper in {len(k4_above)} of {len(CELLS)} "
             f"cells, coppers against the rest {min(null_above)}-{max(null_above)}; cells where only K4 fits: "
             f"{no_copper_fits}. Stop queue: {stop}.")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    """key: {'where': carved place of each message letter, 'order': 'A' or 'B', 'form': 'V' or 'B',
    'alphabet': 26 letters in place order, 'shifts': list}."""
    alpha, sh, where = key["alphabet"], key["shifts"], key["where"]
    pos = {ch: i for i, ch in enumerate(alpha)}
    sgn = 1 if key["form"] == "V" else -1
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
    lines = [f"the table, key length 9, then move: {tag} (write in rows of 7, read the columns bottom to top)", "",
             "place  known  lands at  carved  slot (message place mod 9)"]
    for (q, a), j in zip(known_list, land):
        lines.append(f"{q:5d}  {chr(65 + a):>5}  {j + 1:8d}  {ct[j]:>6}  {(q - 1) % 9:4d}")
    for form in FORMS:
        eqs = setting_eqs(ct, known_list, land, "B", 9)
        if not l1_ok(eqs):
            lines.append(f"form {form}: a slot sends one known letter to two carved letters (or two to one): dead")
            continue
        st, w = decide(eqs, form, random.Random(1))
        if st == "fit":
            order = sorted(w[0].items(), key=lambda kv: kv[1])
            lines.append(f"form {form}: fits; places " + " ".join(f"{chr(65 + a)}={v}" for a, v in order)
                         + f"; key {[w[1].get(s) for s in range(9)]}")
        else:
            lines.append(f"form {form}: {'no alphabet fits' if st == 'dead' else 'undecided'}")
    return "\n".join(lines)
