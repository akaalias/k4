"""Experiment 0209. See program.md for the contract."""

EXPERIMENT = {
    "slug": "two-free-alphabets-with-slips-at-known-places",
    "title": "A1.2, step 3: two alphabets in unknown orders (Quagmire IV), a repeating key of length 1-26, with up to three of the 24 known letters carved wrong, decided exactly, against scrambled copies, with planted slipped messages",
    "family": "1-keyed-periodic",
    "parent": "0123-two-free-alphabets-exact-at-every-key-length",
    "changed": (
        "A1.2 (Stage 2, step 2, issue #76), last part: two free alphabets, run because the cost allows (about 1 s per "
        "length per text). 0123 decided every key length 1-26 exactly with all 24 known letters required (K4 fits at 8, 13, "
        "16, 19, 20, 23, 24, 26; dead at the rest). Here 1-3 of the 24 equations may be dropped as slips: 0123's exact "
        "decider, unchanged, on every drop set (2,325 per length, supersets of a fitting set skipped), K4 against 20 "
        "scrambled copies, planted slipped messages in the same run (three pre-registered at lengths 4, 5, 7; three more at 3 and 9 added after a dry run showed copies fit at 4-8, to locate the reach). 0208 found the reach of one free alphabet near "
        "length 9; two alphabets have 25 more free places, so the reach is expected lower."
    ),
    "hypothesis_expert": (
        "A1 (knowledge/12-assumptions.md); C27(c) (Sanborn's own tableau 'slightly different', 02-sanborn-said.md), C27(a) "
        "(the PALIMPCEST slip), Sanborn 2005 'Saying I was sloppy is a good way of saying it', Scheidt 2015 on Jim's "
        "encoding errors (03-scheidt-said.md). Model as 0123: two unknown bijections P, C from letters to Z26 (plain and "
        "cipher sides), key k of length L: C(c_i) = P(p_i) + k[i mod L] (the Beaufort form is the same family with P "
        "negated). A slip at known place q removes its equation. For every set D of 0-3 known places decide exactly "
        "(0123's decide(two=True), witness re-checked) whether alphabets and key satisfy the rest. Count minimal fitting "
        "sets per length by size, K4 against each copy. Where K4 fits, the reading is undetermined (two free alphabets), so "
        "the judge cannot read it; only F1.5's decider could, and two alphabets are above 0136's English bound from length "
        "19. Cost of naming the slips: 17.5 bits for 2, 25.1 for 3."
    ),
    "hypothesis_eli5": (
        "The same question as experiment 208, with one more freedom: the alphabet used to look up the message letter and "
        "the one used to write the carved letter may be two different scrambles. That is so much freedom that scrambled "
        "copies of the carving often fit already; we want to know up to which word length a search allowing two or three "
        "slips can still tell anything apart, and whether the carving fits anywhere the copies do not."
    ),
    "prediction": (
        "K4 has no fitting pair of alphabets at lengths 1-4 even with 3 slips; from about 5 the copies fit as well, and "
        "K4 fits where they do, inside their range (K4 above every copy in no more cells than a copy is above the rest). "
        "A plant at length 4 with 2 slips is found; plants at 5 and 7 with 3 slips may not be told from their copies (the "
        "reach). Zero candidates."
    ),
    "method": (
        "1. For each text and key length L 1-26: the 24 equations (slot, known letter, carved letter). 2. Decide the system "
        "with no drop, then every drop set of 1, 2, 3 known places, skipping supersets of a set already fitting. 3. Count "
        "the minimal fitting sets by size; record undecided ones. 4. K4 and 20 copies on every length; three planted "
        "messages and 10 copies of each on their own length. 5. Compare K4's count with the copies' per length and per k."
    ),
    "walkthrough": (
        "1. Choose a key length, say 4, and write the 24 known places with their slot (place mod 4). "
        "2. For each place write: position of the carved letter in the cipher alphabet = position of the known letter in the plain alphabet + key value of the slot. "
        "3. Cross out up to three of the 24 places, as if Sanborn had slipped there. "
        "4. Try to place the letters in two alphabets and choose key values so every remaining line holds, backing up when two letters of one alphabet need the same position. "
        "5. If it works, the length fits with those slips; if every branch backs up, it does not. "
        "6. Repeat for every choice of crossed-out places, every length, and on scrambled copies."
    ),
}

import itertools
import random
import multiprocessing as mp
import sys
import types
from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.facts import KNOWN as _KNOWN

N = 97
LMAX = 26
FORMS = ("V",)
KMAX = 3
N_COPIES = 20
N_PLANT_COPIES = 10
PLANTS = [(2091, 4, "V", 2), (2092, 5, "V", 3), (2093, 7, "V", 3),  # pre-registered
          (2094, 3, "V", 2), (2095, 3, "V", 3), (2096, 9, "V", 3)]  # added after the dry run, to locate the reach


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



def cell(args):
    """Minimal fitting drop sets (as tuples of known places) for one text, length and form."""
    text, L, form = args
    known = _KNOWN
    Q = sorted(known)
    eqs = equations(text, known, L)
    fits, und, nd = [], [], 0
    for k in range(KMAX + 1):
        for D in itertools.combinations(range(24), k):
            Ds = set(D)
            if any(set(F) <= Ds for F in fits):
                continue
            e = [x for i, x in enumerate(eqs) if i not in Ds]
            st, w = decide(e, form, two=True)
            nd += 1
            if st == "fit":
                assert check_witness(e, w)
                fits.append(D)
            elif st == "undecided":
                und.append(D)
    return {"fits": [tuple(Q[i] for i in D) for D in fits], "undecided": [tuple(Q[i] for i in D) for D in und], "decided": nd}


def by_k(fits):
    out = [0] * (KMAX + 1)
    for D in fits:
        out[len(D)] += 1
    return out


def shuffled(text, seed):
    l_ = list(text)
    random.Random(seed).shuffle(l_)
    return "".join(l_)


def make_plant(seed, L, form, k):
    from kryptos.plants import english_plant
    rng = random.Random(seed)
    pt = english_plant(seed)
    order = list(range(26)); rng.shuffle(order)
    corder = list(range(26)); rng.shuffle(corder)
    inv = {v: i for i, v in enumerate(corder)}
    key = [rng.randrange(26) for _ in range(L)]
    ct = [chr(65 + inv[(order[ord(p) - 65] + key[i % L]) % 26]) for i, p in enumerate(pt)]
    slots = {}
    for q in sorted(_KNOWN):
        slots.setdefault((q - 1) % L, []).append(q)
    checked = [s for s, qs in slots.items() if len(qs) >= 2]
    rng.shuffle(checked)
    places = sorted(rng.choice(slots[s]) for s in checked[:k])
    for q in places:
        ct[q - 1] = rng.choice([c for c in STD if c != ct[q - 1]])
    alpha = "".join(sorted(STD, key=lambda c: order[ord(c) - 65])) + "/" + "".join(sorted(STD, key=lambda c: corder[ord(c) - 65]))
    return pt, "".join(ct), alpha, key, places


def run(ctx):
    known = ctx.KNOWN
    texts = [ctx.K4] + [shuffled(ctx.K4, 2100 + i) for i in range(N_COPIES)]
    plants = []
    for seed, L, form, k in PLANTS:
        pt, ct, alpha, key, places = make_plant(seed, L, form, k)
        plants.append({"seed": seed, "L": L, "form": form, "k": k, "ct": ct, "alpha": alpha, "key": key, "slips": places,
                       "copies": [shuffled(ct, seed * 100 + i) for i in range(N_PLANT_COPIES)]})
    tasks = []
    for p in plants:  # plants first, so the clock never cuts them
        tasks.append(("P", p["seed"], -1, (p["ct"], p["L"], p["form"])))
        for i, c in enumerate(p["copies"]):
            tasks.append(("P", p["seed"], i, (c, p["L"], p["form"])))
    for t, txt in enumerate(texts):
        for L in range(1, LMAX + 1):
            for form in FORMS:
                tasks.append(("T", t, None, (txt, L, form)))
    if getattr(sys.modules.get(__name__), "cell", None) is not cell:
        mod = types.ModuleType(__name__); mod.__dict__.update(globals()); sys.modules[__name__] = mod
    results = {}
    with mp.get_context("fork").Pool(8) as pool:
        it = pool.imap(cell, [x[3] for x in tasks], chunksize=1)
        for tk, r in zip(tasks, it):
            results[tk[:3] + (tk[3][1], tk[3][2])] = r
            if ctx.time_left() < 120:
                pool.terminate()
                break
    # K4 and copies per cell
    cells = {}
    above, null_above = [], [0] * N_COPIES
    for L in range(1, LMAX + 1):
        for form in FORMS:
            rows = [results.get(("T", t, None, L, form)) for t in range(len(texts))]
            if any(r is None for r in rows):
                continue
            cnt = [by_k(r["fits"]) for r in rows]
            und = [len(r["undecided"]) for r in rows]
            k4, cps = cnt[0], cnt[1:]
            cells[f"{form}{L}"] = {"k4": k4, "copies_min": [min(c[k] for c in cps) for k in range(KMAX + 1)],
                                   "copies_max": [max(c[k] for c in cps) for k in range(KMAX + 1)],
                                   "copies_fitting_at_k_or_less": [sum(1 for c in cps if sum(c[:k + 1])) for k in range(KMAX + 1)],
                                   "k4_undecided": und[0], "copies_undecided": sum(und[1:]),
                                   "k4_sets": [list(D) for D in rows[0]["fits"]][:40]}
            tot = [sum(c) for c in cnt]
            if tot[0] > max(tot[1:]):
                above.append(f"{form}{L}")
            for i in range(N_COPIES):
                others = [tot[j] for j in range(len(tot)) if j != i + 1]
                if tot[i + 1] > max(others):
                    null_above[i] += 1
    def shortest(t, k):
        out = {}
        for form in FORMS:
            out[form] = next((L for L in range(1, LMAX + 1) if (r := results.get(("T", t, None, L, form))) and sum(by_k(r["fits"])[:k + 1])), None)
        return out
    plant_out = []
    for p in plants:
        r = results.get(("P", p["seed"], -1, p["L"], p["form"]))
        own = [results.get(("P", p["seed"], i, p["L"], p["form"])) for i in range(N_PLANT_COPIES)]
        if r is None or any(o is None for o in own):
            plant_out.append({"seed": p["seed"], "found": False, "note": "not run (clock)"})
            continue
        planted_fits = tuple(p["slips"]) in [tuple(D) for D in r["fits"]] or any(set(D) <= set(p["slips"]) for D in r["fits"])
        own_tot = [sum(by_k(o["fits"])[:p["k"] + 1]) for o in own]
        tot = sum(by_k(r["fits"])[:p["k"] + 1])
        plant_out.append({"seed": p["seed"], "key_length": p["L"], "form": p["form"], "k": p["k"], "slips": p["slips"],
                          "alphabet": p["alpha"], "minimal_fits_by_k": by_k(r["fits"]),
                          "planted_slips_fit": planted_fits, "exact_planted_set_minimal": tuple(p["slips"]) in [tuple(D) for D in r["fits"]],
                          "count_at_k": tot, "own_copies_count_at_k": own_tot,
                          "found": bool(planted_fits and tot > max(own_tot))})
    done = sum(1 for k in results if k[0] == "T")
    import math
    return {
        "candidates": [],
        "bounds": {
            "family": "two unknown alphabets (Quagmire IV), periodic key 1-26, with 0-3 known letters slipped (A1.2)",
            "key_lengths": [1, LMAX], "forms": {"V": "C(c) = P(p) + k (Beaufort is the same family with P negated)"},
            "drop_sets": "every set of 0-3 of the 24 known places (2,325 per cell), supersets of a fitting set skipped; 0123's decide(two=True) unchanged",
            "slip_cost_bits": {k: round(4.7 * k + math.log2(math.comb(24, k)), 1) for k in (1, 2, 3)},
            "cells": cells,
            "k4_above_every_copy": above, "copies_above_the_rest_cells": null_above,
            "shortest_fitting_length": {f"k{k}": {"K4": shortest(0, k), "copies": [shortest(t, k) for t in range(1, len(texts))]} for k in range(KMAX + 1)},
            "plants": plant_out,
            "judge": "not called: where two free alphabets fit, both are undetermined and so is the reading; F1.5's decider only below 0136's bound (length 19)",
            "texts_done": f"{done} of {len(texts) * LMAX * len(FORMS)} cells",
            "controls": f"{N_COPIES} shuffled copies (seeds 2100-2119); each plant against {N_PLANT_COPIES} shuffles of its own ciphertext",
            "exhaustive": "yes (exact per drop set; undecided sets counted)",
        },
        "notes": f"K4 above every copy in {len(above)} cells {above}; copies above the rest {min(null_above)}-{max(null_above)}; plants found {[p['found'] for p in plant_out]}",
    }


def encrypt(plaintext, key):
    """Quagmire IV with slips: key = {plain, cipher (alphabet strings), shifts, slips [[place, carved letter]]}."""
    pp = {ch: i for i, ch in enumerate(key["plain"])}
    out = [key["cipher"][(pp[ch] + key["shifts"][i % len(key["shifts"])]) % 26] for i, ch in enumerate(plaintext)]
    for q, ch in key.get("slips", []):
        out[q - 1] = ch
    return "".join(out)


def worked_example(ctx, key):
    L = 4
    eqs = equations(ctx.K4, ctx.KNOWN, L)
    lines = [f"key length {L}, two free alphabets: C(carved) = P(known) + k[slot]", ""]
    Q = sorted(ctx.KNOWN)
    for D in ((), (66,), (66, 73), (28, 66, 73)):
        idx = [Q.index(q) for q in D]
        e = [x for i, x in enumerate(eqs) if i not in idx]
        st, _ = decide(e, "V", two=True)
        lines.append(f"  slips at {list(D) or 'none'}: {st}")
    return "\n".join(lines)
