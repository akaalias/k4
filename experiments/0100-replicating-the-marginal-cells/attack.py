"""Experiment 0100. See program.md for the contract."""

EXPERIMENT = {
    "slug": "replicating-the-marginal-cells",
    "title": "The three marginal excesses of experiments 92, 93 and 97, recounted as distinct check sets against fifty fresh scrambled coppers",
    "family": "6-transposition-then-tableau",
    "parent": "0097-free-mixed-alphabets-after-a-move",
    "changed": "0092, 0093 and 0097 each left one cell where K4 sat at or just above the top of ten scrambled coppers: path routes at periods 22-23, one-miss periodic keys at period 22, and the free Quagmire IV at period 3 after a move. Ten controls cannot tell a 1-in-11 event from a signal. Here exactly those cells are recounted, with look-alike routes collapsed into distinct check sets, against fifty new coppers, and each gets an empirical p-value.",
    "hypothesis_expert": (
        "A replication, not a new search. Cells, fixed before the run from the records: (1) 0092, write along one of 30 "
        "grid paths and read along another, periodic key after the move, periods 22 and 23, distinct (check pairs, "
        "class) sets; (2) 0093, type-1 library, periodic key after the move with at most one known letter set aside, "
        "period 22, distinct (slot partition, class) sets; (3) 0097, type-1 library plus no move, Quagmire IV with "
        "unknown alphabets, key after the move, period 3, distinct canonical equation sets. Statistic: K4's count and "
        "the fraction of 50 shuffled coppers (seed 100) whose count is at least K4's. With three cells and four counts "
        "the multiple-comparison threshold is about p < 0.0125 for any one of them."
    ),
    "hypothesis_eli5": (
        "Three times tonight K4 scored a little higher than all ten scrambled copies of itself. With only ten copies, "
        "that happens by luck about one time in eleven, so it proves nothing. Here we redo exactly those three counts "
        "against fifty fresh scrambled copies and count, for each, how many copies do at least as well as K4."
    ),
    "prediction": (
        "Every cell has an empirical p above 0.05 against the fifty fresh coppers: the excesses were luck. Zero candidates."
    ),
    "method": (
        "1. Rebuild the route sets of 0092 and of the type-1 library. 2. For each cell, compute the distinct check sets "
        "consistent on K4 and on fifty shuffled coppers. 3. Report K4's count, the coppers' range and mean, and the "
        "fraction of coppers at or above K4."
    ),
    "walkthrough": (
        "1. Take one cell, say Quagmire IV at period 3 after a move. "
        "2. For every move, write the 24 equations and keep the move if some pair of alphabets fits. "
        "3. Moves that give the same equations up to relabelling the key slots count once. "
        "4. Do the same on fifty scrambled copies of K4. "
        "5. The share of copies with at least K4's count is the chance of K4's result by luck."
    ),
}

import random
from math import gcd
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.ciphers import columnar_transposition_encrypt
from kryptos.alphabets import numeric_order

N = 97
N_CONTROLS = 50
ALPH = {"std": STD, "kry": KRY}
EXTRA = ["EGYPT", "CAIRO", "LUXOR", "WALL", "NOVEMBER", "MESSAGE", "DELIVER", "DELIVERING", "TRANSMIT"]


def cells(w):
    return [(i // w, i % w) for i in range(N)]


def paths(w):
    """30 orders of the 97 cells of a width-w grid (last row short)."""
    cs = cells(w)
    have = set(cs)
    h = -(-N // w)
    out = {}
    out["rows"] = list(cs)
    out["snake rows"] = [(r, c if r % 2 == 0 else w - 1 - c) for r in range(h) for c in range(w) if (r, c if r % 2 == 0 else w - 1 - c) in have]
    out["columns"] = [(r, c) for c in range(w) for r in range(h) if (r, c) in have]
    out["snake columns"] = [(r if c % 2 == 0 else h - 1 - r, c) for c in range(w) for r in range(h) if (r if c % 2 == 0 else h - 1 - r, c) in have]

    def cw_spiral(hh, ww):
        top, bot, left, right = 0, hh - 1, 0, ww - 1
        seq = []
        while top <= bot and left <= right:
            for c in range(left, right + 1):
                seq.append((top, c))
            for r in range(top + 1, bot + 1):
                seq.append((r, right))
            if top < bot:
                for c in range(right - 1, left - 1, -1):
                    seq.append((bot, c))
            if left < right:
                for r in range(bot - 1, top, -1):
                    seq.append((r, left))
            top += 1; bot -= 1; left += 1; right -= 1
        return seq

    def spiral(corner, cw):
        # clockwise from the top-left goes right first; anticlockwise from the top-left goes down first (the transpose)
        fr, fc = corner
        base_cw = cw if fr == fc else not cw          # one mirror reverses the sense of turning, two do not
        seq = cw_spiral(h, w) if base_cw else [(r, c) for c, r in cw_spiral(w, h)]
        mapped = [((h - 1 - r) if fr else r, (w - 1 - c) if fc else c) for r, c in seq]
        return [x for x in mapped if x in have]
    for corner in ((0, 0), (0, 1), (1, 0), (1, 1)):
        for cw in (True, False):
            out[f"spiral {'bottom' if corner[0] else 'top'}-{'right' if corner[1] else 'left'} {'cw' if cw else 'ccw'}"] = spiral(corner, cw)
    out["anti-diagonals"] = sorted(cs, key=lambda x: (x[0] + x[1], x[0]))
    out["snake anti-diagonals"] = sorted(cs, key=lambda x: (x[0] + x[1], x[0] if (x[0] + x[1]) % 2 == 0 else -x[0]))
    out["diagonals"] = sorted(cs, key=lambda x: (x[1] - x[0], x[0]))
    for k in list(out):
        out[k + " reversed"] = out[k][::-1]
    for k, v in out.items():
        assert len(v) == N and len(set(v)) == N, (w, k)
    return out


def slot_pairs(slots):
    last, prs = {}, []
    for e, s in enumerate(slots):
        if s in last:
            prs.append((last[s], e))
        last[s] = e
    return prs


def route(write, read):
    """where[i]: place in the read-out text of message letter i."""
    pos = {cell: j for j, cell in enumerate(read)}
    return [pos[write[i]] for i in range(N)]


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


def partition(slots):
    g = {}
    for e, s in enumerate(slots):
        g.setdefault(s, []).append(e)
    return frozenset(tuple(v) for v in g.values() if len(v) > 1)


def misses(f, slots):
    groups = {}
    for e, s in enumerate(slots):
        groups.setdefault(s, []).append(f[e])
    m = 0
    for vals in groups.values():
        if len(vals) > 1:
            cnt = {}
            for v in vals:
                cnt[v] = cnt.get(v, 0) + 1
            m += len(vals) - max(cnt.values())
            if m > 1:
                return 2
    return m


def canon(eqs):
    m, out = {}, []
    for s, a, c in eqs:
        m.setdefault(s, len(m)); out.append((m[s], a, c))
    return tuple(sorted(out))


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    places = sorted(known)
    pidx = [p - 1 for p in places]
    rng = random.Random(100)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    T = len(texts)
    classes = [(pa, ca, beau) for pa in ALPH for ca in ALPH for beau in (False, True)]
    CI = {an: [[{c: i for i, c in enumerate(ALPH[an])}[ch] for ch in t] for t in texts] for an in ALPH}
    PI = {an: [{c: i for i, c in enumerate(ALPH[an])}[known[p]] for p in places] for an in ALPH}

    def fvals(land, cls, t):
        pa, ca, beau = cls
        C = CI[ca][t]; Pv = PI[pa]
        return [(C[j] + Pv[e]) % 26 if beau else (C[j] - Pv[e]) % 26 for e, j in enumerate(land)]

    # cell 1: 0092 path routes, key after the move, periods 22 and 23
    c1 = {p: [set() for _ in range(T)] for p in (22, 23)}
    seen = set()
    for w in range(2, N):
        P = paths(w)
        names = list(P)
        for a in names:
            for b in names:
                if a == b:
                    continue
                wh = route(P[a], P[b])
                inv = [0] * N
                for i, j in enumerate(wh):
                    inv[j] = i
                for r in (wh, inv):
                    key = tuple(r)
                    if key in seen or key == tuple(range(N)):
                        continue
                    seen.add(key)
                    land = [r[i] for i in pidx]
                    prs = {p: slot_pairs([j % p for j in land]) for p in (22, 23)}
                    for cls in classes:
                        for t in range(T):
                            f = fvals(land, cls, t)
                            for p in (22, 23):
                                if all(f[x] == f[y] for x, y in prs[p]):
                                    c1[p][t].add((frozenset(prs[p]), cls))
    n92 = len(seen)
    # cells 2 and 3: the type-1 library
    lib = route_library(ctx.vocabulary)
    c2 = [set() for _ in range(T)]
    c3 = [set() for _ in range(T)]
    for tag, where in lib + [("no move", tuple(range(N)))]:
        land = [where[i] for i in pidx]
        sl22 = [j % 22 for j in land]
        part = partition(sl22)
        if tag != "no move":
            for cls in classes:
                for t in range(T):
                    if misses(fvals(land, cls, t), sl22) <= 1:
                        c2[t].add((part, cls))
        for t in range(T):
            eqs = [(land[e] % 3, known[places[e]], texts[t][land[e]]) for e in range(24)]
            if l1_ok(eqs) and l2_ok(eqs, False):
                c3[t].add(canon(eqs))
        if ctx.time_left() < 60:
            break
    def summary(counts):
        k = counts[0]; ctl = counts[1:]
        return {"k4": k, "controls_min": min(ctl), "controls_max": max(ctl), "controls_mean": round(sum(ctl) / len(ctl), 2),
                "p_at_least_k4": round(sum(1 for x in ctl if x >= k) / len(ctl), 3)}
    cells = {
        "0092 paths, after the move, period 22": summary([len(s) for s in c1[22]]),
        "0092 paths, after the move, period 23": summary([len(s) for s in c1[23]]),
        "0093 one miss, after the move, period 22": summary([len(s) for s in c2]),
        "0097 Quagmire IV, after the move, period 3": summary([len(s) for s in c3]),
    }
    bounds = {"family": "replication of marginal cells with fresh controls", "controls": f"{N_CONTROLS} shuffled coppers (seed 100)",
              "path_routes": n92, "library_routes": len(lib), "cells": cells,
              "threshold_note": "four counts: p < 0.0125 would be needed for any one to stand"}
    notes = "; ".join(f"{k}: K4 {v['k4']}, coppers {v['controls_min']}-{v['controls_max']} (mean {v['controls_mean']}), p {v['p_at_least_k4']}" for k, v in cells.items()) + "."
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    lines = ["the four counts replicated, with what ten coppers showed in the original runs", "",
             "0092  paths, after the move, period 22: K4 13 distinct check sets, ten coppers 8-15",
             "0092  paths, after the move, period 23: K4 88, ten coppers 74-98",
             "0093  one miss, after the move, period 22: K4 980 settings, ten coppers 526-859",
             "0097  Quagmire IV, after the move, period 3: K4 12 distinct equation sets, ten coppers 1-11",
             "", "here: the same counts as distinct sets, against fifty new coppers"]
    return "\n".join(lines)
