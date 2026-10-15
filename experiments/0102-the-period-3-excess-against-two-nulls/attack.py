"""Experiment 0102. See program.md for the contract."""

EXPERIMENT = {
    "slug": "the-period-3-excess-against-two-nulls",
    "title": "The period-3 free-alphabet excess, against 400 scrambled coppers and 400 that keep K4's width-21 columns",
    "family": "6-transposition-then-tableau",
    "parent": "0100-replicating-the-marginal-cells",
    "changed": "0100 left one cell above all 50 coppers: Quagmire IV at period 3 after a move, 12 distinct equation sets against 0-11. Here the four period-3 cells (one alphabet or a pair, key after or before the move) are counted against 400 plain shuffles, with a look-elsewhere correction across the four, and against 400 copies of K4 whose 21-wide grid has its columns shuffled, which keeps every pair of letters 21 apart and so K4's width-21 repeats.",
    "hypothesis_expert": (
        "Follow-up of 0097 and 0100. Mechanism to test: carved places 21 apart share a key slot mod 3, and K4 has 11 "
        "repeated letter pairs 21 apart (0056), so a period-3 key after a move may fit K4 more often for that reason "
        "alone. Null A: 400 letter shuffles (seed 102). Null B: 400 column permutations of K4 written 21 wide, the "
        "13 columns of the short last row permuted among themselves and the other 8 among themselves, so every vertical "
        "pair is kept. Cells: Quagmire III or IV, key after (A) or before (B) the move, period 3; type-1 library plus no "
        "move; distinct canonical equation sets; linear test mod 2 and mod 13 as in 0097. Report K4's p under each null "
        "and, under null A, the share of shuffles whose smallest p over the four cells is at most K4's."
    ),
    "hypothesis_eli5": (
        "In experiment 100 one count stayed higher on K4 than on fifty scrambled copies. K4 has a known oddity: letters "
        "21 places apart repeat in pairs more than chance. Because 21 is a multiple of 3, that oddity could raise this "
        "count by itself. So we compare K4 with 400 ordinary scrambles and with 400 scrambles that keep "
        "the oddity, by moving whole columns of a 21-wide grid around."
    ),
    "prediction": (
        "Under plain shuffles K4's cell is near p 0.02, with a look-elsewhere p above 0.05; under the column permutations "
        "K4 is unremarkable (p above 0.2), so the excess comes from the width-21 repeats. Zero candidates."
    ),
    "method": (
        "1. Build the type-1 library and the two nulls. 2. For each text, route and order, test the free-alphabet filter "
        "and the linear test at period 3 for both models, collecting distinct equation sets. 3. Compute K4's p per cell "
        "under each null and the look-elsewhere p under null A."
    ),
    "walkthrough": (
        "1. Write K4 in rows of 21; the last row has 13 letters. "
        "2. Shuffle the first 13 columns among themselves and the last 8 among themselves; every pair of letters 21 apart stays a pair. "
        "3. For each move, test whether some pair of alphabets with a 3-letter key fits the 24 known letters, and collect the distinct ways it fits. "
        "4. Compare K4's count with the counts on these copies and on ordinary scrambles."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.ciphers import columnar_transposition_encrypt
from kryptos.alphabets import numeric_order

N = 97
N_NULL = 400
EXTRA = ["EGYPT", "CAIRO", "LUXOR", "WALL", "NOVEMBER", "MESSAGE", "DELIVER", "DELIVERING", "TRANSMIT"]


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


def nullspace_signatures(rows, nv, q):
    """rows: list of {var: coef}. Returns, for each variable, the tuple of its values over a nullspace basis mod q."""
    M = [[r.get(v, 0) % q for v in range(nv)] for r in rows]
    piv = []
    r = 0
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
    return sig


def l1_ok(pairs_by_slot):
    f, g = {}, {}
    for s, a, c in pairs_by_slot:
        if f.setdefault((s, a), c) != c or g.setdefault((s, c), a) != a:
            return False
    return True


def l2_ok(eqs, same_alphabet):
    """eqs: list of (slot, plain letter, cipher letter). index_C(c) - index_P(a) - k[slot] = 0."""
    var = {}

    def v(name):
        if name not in var:
            var[name] = len(var)
        return var[name]
    rows = []
    for s, a, c in eqs:
        pc = v(("A", c)) if same_alphabet else v(("C", c))
        pp = v(("A", a)) if same_alphabet else v(("P", a))
        pk = v(("k", s))
        r = {}
        r[pc] = r.get(pc, 0) + 1
        r[pp] = r.get(pp, 0) - 1
        r[pk] = r.get(pk, 0) - 1
        rows.append({x: y for x, y in r.items() if y})
    nv = len(var)
    s2 = nullspace_signatures(rows, nv, 2)
    s13 = nullspace_signatures(rows, nv, 13)
    fam = {}
    for name, i in var.items():
        if name[0] != "k":
            fam.setdefault(name[0], []).append(i)
    for members in fam.values():
        by13 = {}
        for i in members:
            by13.setdefault(s13[i], []).append(i)
        for grp in by13.values():
            if len(grp) > 2:
                return False
            if len(grp) == 2 and s2[grp[0]] == s2[grp[1]]:
                return False
    return True


def nullspace_signatures(rows, nv, q):
    """rows: list of {var: coef}. Returns, for each variable, the tuple of its values over a nullspace basis mod q."""
    M = [[r.get(v, 0) % q for v in range(nv)] for r in rows]
    piv = []
    r = 0
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
    return sig


def l1_ok(pairs_by_slot):
    f, g = {}, {}
    for s, a, c in pairs_by_slot:
        if f.setdefault((s, a), c) != c or g.setdefault((s, c), a) != a:
            return False
    return True


def l2_ok(eqs, same_alphabet):
    """eqs: list of (slot, plain letter, cipher letter). index_C(c) - index_P(a) - k[slot] = 0."""
    var = {}

    def v(name):
        if name not in var:
            var[name] = len(var)
        return var[name]
    rows = []
    for s, a, c in eqs:
        pc = v(("A", c)) if same_alphabet else v(("C", c))
        pp = v(("A", a)) if same_alphabet else v(("P", a))
        pk = v(("k", s))
        r = {}
        r[pc] = r.get(pc, 0) + 1
        r[pp] = r.get(pp, 0) - 1
        r[pk] = r.get(pk, 0) - 1
        rows.append({x: y for x, y in r.items() if y})
    nv = len(var)
    s2 = nullspace_signatures(rows, nv, 2)
    s13 = nullspace_signatures(rows, nv, 13)
    fam = {}
    for name, i in var.items():
        if name[0] != "k":
            fam.setdefault(name[0], []).append(i)
    for members in fam.values():
        by13 = {}
        for i in members:
            by13.setdefault(s13[i], []).append(i)
        for grp in by13.values():
            if len(grp) > 2:
                return False
            if len(grp) == 2 and s2[grp[0]] == s2[grp[1]]:
                return False
    return True


def canon(eqs):
    m, out = {}, []
    for s, a, c in eqs:
        m.setdefault(s, len(m)); out.append((m[s], a, c))
    return tuple(sorted(out))


def column_permuted(ct, rng):
    rows = [ct[i:i + 21] for i in range(0, N, 21)]
    a = rng.sample(range(13), 13); b = [13 + x for x in rng.sample(range(8), 8)]
    order = a + b
    out = []
    for r in rows:
        out.append("".join(r[order[c]] if order[c] < len(r) else "" for c in range(len(r))))
    s = "".join(out)
    assert len(s) == N
    return s


def rep21(t):
    v = [t[i] + t[i + 21] for i in range(len(t) - 21)]
    return len(v) - len(set(v))


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    places = sorted(known)
    pidx = [p - 1 for p in places]
    rng = random.Random(102)
    nullA = ["".join(rng.sample(ct, N)) for _ in range(N_NULL)]
    nullB = [column_permuted(ct, rng) for _ in range(N_NULL)]
    assert all(rep21(t) == rep21(ct) for t in nullB[:50])
    texts = [ct] + nullA + nullB
    T = len(texts)
    lib = route_library(ctx.vocabulary) + [("no move", tuple(range(N)))]
    cells = [(m, o) for m in ("III", "IV") for o in "AB"]
    sets = {c: [set() for _ in range(T)] for c in cells}
    done = 0
    for tag, where in lib:
        land = [where[i] for i in pidx]
        slotA = [j % 3 for j in land]; slotB = [i % 3 for i in pidx]
        for t in range(T):
            txt = texts[t]
            cs = [txt[j] for j in land]
            for o, sl in (("A", slotA), ("B", slotB)):
                eqs = [(sl[e], known[places[e]], cs[e]) for e in range(24)]
                if not l1_ok(eqs):
                    continue
                if not l2_ok(eqs, False):
                    continue
                key = canon(eqs)
                sets[("IV", o)][t].add(key)
                if l2_ok(eqs, True):
                    sets[("III", o)][t].add(key)
        done += 1
        if ctx.time_left() < 60:
            break
    res = {}
    pk = {}
    for c in cells:
        cnt = [len(s) for s in sets[c]]
        k = cnt[0]; A = cnt[1:1 + N_NULL]; B = cnt[1 + N_NULL:]
        pA = sum(1 for x in A if x >= k) / len(A); pB = sum(1 for x in B if x >= k) / len(B)
        res[f"{c[0]} {c[1]}"] = {"k4": k, "nullA_mean": round(sum(A) / len(A), 2), "nullA_max": max(A), "p_nullA": pA,
                                 "nullB_mean": round(sum(B) / len(B), 2), "nullB_max": max(B), "p_nullB": pB}
        pk[c] = (k, A)
    # look-elsewhere under null A: for each shuffle, its smallest p over the four cells, against the other shuffles
    def p_of(x, A):
        return sum(1 for y in A if y >= x) / len(A)
    k4_min = min(p_of(pk[c][0], pk[c][1]) for c in cells)
    sh_min = [min(p_of(pk[c][1][i], pk[c][1]) for c in cells) for i in range(N_NULL)]
    p_le = sum(1 for x in sh_min if x <= k4_min) / N_NULL
    bounds = {"family": "period-3 free-alphabet cells against two nulls", "routes_done": done, "routes": len(lib),
              "nullA": f"{N_NULL} letter shuffles (seed 102)", "nullB": f"{N_NULL} column permutations of K4 at width 21 (keep all 76 vertical pairs)",
              "cells": res, "k4_smallest_p_nullA": k4_min, "look_elsewhere_p_nullA": p_le}
    notes = ("; ".join(f"{k}: K4 {v['k4']}, shuffles mean {v['nullA_mean']} max {v['nullA_max']} p {v['p_nullA']:.3f}, "
                       f"21-column permutations mean {v['nullB_mean']} max {v['nullB_max']} p {v['p_nullB']:.3f}" for k, v in res.items())
             + f". Look-elsewhere over the four cells under shuffles: p {p_le:.3f}.")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct = ctx.K4
    rng = random.Random(1)
    t = column_permuted(ct, rng)
    lines = ["K4 in rows of 21, and one copy with its columns shuffled (13 short-row columns among themselves, 8 among themselves)", ""]
    lines += ["  " + ct[i:i + 21] for i in range(0, N, 21)]
    lines += [""] + ["  " + t[i:i + 21] for i in range(0, N, 21)]
    lines += ["", f"letter pairs 21 apart that repeat: K4 {rep21(ct)}, the copy {rep21(t)}"]
    return "\n".join(lines)
