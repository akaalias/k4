"""Experiment 0126. See program.md for the contract."""

EXPERIMENT = {
    "slug": "hand-key-schedules-listed-and-tested",
    "title": "Hand key schedules: the tableau rows as keys ('layer two'), a keyword stepped by skip, stutter, back-and-forth, triangle and square rules, and restarted at each carved line; each tested exactly on fixed, free and paired alphabets",
    "family": "1-keyed-periodic",
    "parent": "0101-interrupted-key",
    "changed": (
        "F1.4. The list of hand schedules is written first (C20(c)-(e) and the hand rules a person with a keyword and a "
        "pencil would use), then each is tested exactly. Covered before and not rerun: Berlin clock (0079), Carter dates "
        "(0038), progressive per repeat (0011, 0042), restart at each word (0101), autokeys (0002, 0003, 0012, 0118), the "
        "second plate and the sculpture's texts as running keys (C20(c): 0017, 0090, 0117), a shift per carved line plus "
        "a word (0088). K5 as key (C20(e)) is blocked: no text. New here: (A) C20(d) the tableau rows as fixed keys; (B) "
        "skip one keyword letter every m letters; (C) each keyword letter used r times; (D) the keyword forward then "
        "backward; (E) the keyword indexed by triangle or square numbers; (F) the keyword restarted at each carved line of "
        "the plate. B-F with an unknown keyword of length 2-31 on 8 standard/KRYPTOS tables, one free alphabet (both "
        "forms) and two free alphabets."
    ),
    "hypothesis_expert": (
        "C20(c)-(e) ('layer two': the second plate, the tableau's row two, K5), C5 (simple, remembered, keyed by word/s), "
        "C3(a) (the plate as grid). Model for B-F: key value at message place i (0-based) = W[f(i) mod n] for an unknown "
        "keyword W of length n: B f = i + floor((i + phi)/m), m 2-30; C f = floor((i + phi)/r), r 2-6; D W then W reversed "
        "(period 2n or 2n-2, end letters repeated or not); E f = T(i + phi) = (i + phi)(i + phi + 1)/2 or (i + phi)^2; F f = "
        "column on the carved line minus 1 (K4 fills columns 28-31 of line 11, then lines 12-14), counted from the line "
        "start or from K4's first letter; phi over its whole range; n 2-26 (2-31 for F). Each setting partitions the 24 "
        "known places into slots; distinct partitions are tested once. Tests: (i) 8 tables (plain and cipher standard or "
        "KRYPTOS, Vigenere or Beaufort): all key values in a slot equal; (ii) one free alphabet, forms V and B, and (iii) "
        "two free alphabets, by 0119/0123's exact decider (CRT mod 13 and 2, witness re-checked). Count consistent "
        "partitions with at least one check, per schedule and test, on K4 and 10 shuffled coppers (seed 126). (A): the 26 "
        "carved tableau rows (30 letters plus the extra L) with and without the index letter, as repeating keys from every "
        "start, key letters on the standard or KRYPTOS order, 8 tables: count known letters reproduced."
    ),
    "hypothesis_eli5": (
        "Someone enciphering by hand with a key word has simple ways to use it besides repeating it: skip a letter now "
        "and then, use each letter twice, go back and forth through the word, jump ahead by growing steps, or start the "
        "word again at the start of each carved line. Or, reading 'layer two' literally, use the second row of the big "
        "table on the sculpture as the key. We list these rules, then check each against the 24 known letters, with "
        "the sculpture's table, a plain table, and tables in any order at all."
    ),
    "prediction": (
        "No schedule fits on the standard or KRYPTOS tables with at least three checks, and the tableau rows reproduce at "
        "most 7 of 24 known letters, as on coppers. On free alphabets, consistent counts lie inside the coppers' range for "
        "every schedule and test, give or take one cell in the roughly 20 compared (chance). Any cell outside the range "
        "with K4 high is replicated before anything else."
    ),
    "method": (
        "1. Build each schedule's settings and the slot partition of the 24 known places it gives; keep distinct "
        "partitions. 2. For each partition and text (K4 and 10 coppers), test the 8 tables, one free alphabet (V, B) and "
        "two free alphabets exactly. 3. Count consistent partitions with at least one check. 4. Tableau rows as fixed keys: "
        "best count of known letters reproduced. 5. Compare K4 with the coppers' range."
    ),
    "walkthrough": (
        "1. Take a key word of n letters, unknown, say n = 7, and a rule, say 'skip one key letter every 5 letters'. "
        "2. Walk along K4 writing under each place the number of the key letter it uses: 0 1 2 3 4, then skip, 6 0 1 2 3, then skip, and so on, counting modulo 7. "
        "3. Known places with the same number must have the same key value. "
        "4. With the sculpture's table, key value = place of the carved letter minus place of the known letter in KRYPTOS order; compare. "
        "5. With an unknown table, solve for whether any alphabet makes them agree. "
        "6. Repeat for every rule, every n, every starting phase, and on scrambled copies of K4."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
N_CONTROLS = 10
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


def run(ctx):
    ct = ctx.K4
    rng = random.Random(126)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    parts = partitions()
    tests = ("tables", "free V", "free B", "two free")
    counts = {fam: {t: [0] * len(texts) for t in tests} for fam in parts}
    k4_live = []
    n_parts = {}
    for fam, pp in parts.items():
        good = [p for p in pp if 24 - len(set(p)) >= 1]          # at least one check
        n_parts[fam] = {"distinct": len(pp), "with_checks": len(good)}
        for p in good:
            for t, txt in enumerate(texts):
                tb = any(table_ok(txt, p))
                e = eqs_of(txt, p)
                fv = decide(e, "V")[0] == "fit"
                fb = decide(e, "B")[0] == "fit"
                tw = decide(e, "V", two=True)[0] == "fit"
                for name, ok in (("tables", tb), ("free V", fv), ("free B", fb), ("two free", tw)):
                    if ok:
                        counts[fam][name][t] += 1
                        if t == 0 and name == "tables":
                            k4_live.append({"family": fam, "setting": pp[p], "checks": 24 - len(set(p))})
            if ctx.time_left() < 120:
                break
    cells = {}
    outside = []
    for fam in parts:
        for name in tests:
            v = counts[fam][name]
            lo, hi = min(v[1:]), max(v[1:])
            cells[f"{fam} | {name}"] = {"k4": v[0], "coppers": [lo, hi]}
            if not lo <= v[0] <= hi:
                outside.append(f"{fam} | {name}: K4 {v[0]} vs {lo}-{hi}")
    tk = tableau_keys()
    fixed_k4 = max(fixed_hits(ct, k) for _, k in tk)
    fixed_ctrl = [max(fixed_hits(txt, k) for _, k in tk) for txt in texts[1:4]]
    bounds = {
        "family": "hand key schedules with an unknown keyword (skip, stutter, back and forth, triangle, square, line restart), and the tableau rows as keys",
        "partitions": n_parts, "cells": cells, "outside_copper_range": outside,
        "k4_consistent_on_standard_or_kryptos_tables": sorted(k4_live, key=lambda r: -r["checks"])[:30],
        "n_k4_consistent_on_tables": len(k4_live),
        "tableau_rows_as_keys": {"keys": len(tk), "starts": "every", "tables": 16,
                                 "k4_best_hits": fixed_k4, "coppers_best_hits_first_3": fixed_ctrl},
        "covered_elsewhere": {"Berlin clock": "0079", "Carter dates": "0038", "progressive": "0011, 0042",
                              "restart per word": "0101", "autokey": "0002, 0003, 0012, 0118",
                              "C20(c) second plate / sculpture texts": "0017, 0090, 0117", "shift per carved line": "0088"},
        "blocked": {"C20(e) K5 as key": "no text"},
        "controls": f"{N_CONTROLS} shuffled coppers (seed 126), identical tests",
    }
    notes = (f"Outside the copper range: {outside or 'none'}. K4 consistent on std/KRYPTOS tables: {len(k4_live)} partitions "
             f"(max checks {max([r['checks'] for r in k4_live], default=0)}). Tableau rows as keys: K4 best {fixed_k4}/24, "
             f"coppers {fixed_ctrl}.")
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
