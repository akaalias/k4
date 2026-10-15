"""Experiment 0086. See program.md for the contract."""

EXPERIMENT = {
    "slug": "the-question-mark-as-the-98th-cell",
    "title": "The ? before OBKR as the 98th letter: a full 7 x 14 grid, turned so the ? comes out first, with an autokey or a repeating key",
    "family": "6-transposition-then-tableau",
    "parent": "0082-where-the-blanks-go-in-the-grid",
    "changed": "With the carved ? counted, K4 has 98 symbols, which fill a 7 x 14 grid exactly. Here the message plus a ? somewhere in it is written into a grid of 98 cells and read out from any corner, once or twice, by K3's rule on 98, or by a seven-column shuffle in any of its 5,040 orders; the reading must bring the ? to the front, where it is carved. The 97 letters are then keyed by a repeating key, or by the plaintext or ciphertext autokey, which the padded-grid searches never paired with the 98-cell grid.",
    "hypothesis_expert": (
        "Type 2 of directions.md, the prior-work database's seven-based sub-variant 2 ('a 7x14 grid of 98 (with ?) under "
        "a K3-style rotation plus a non-periodic key (autokey, progressive); padded rotations were tested only with "
        "periodic keys', nitsuah). Clues C18(b) (Scheidt 2004-5, 'I think there are 98 characters left'; a 98-character "
        "working text including ?), C17(c) (the ? counts), C1(a) and C2(a) (the K3 move; K3's 336 letters fill 24 x 14 "
        "and 8 x 42 exactly, so a full grid is Sanborn's habit), and the width-7 doublet column (0056). Model: the 97 "
        "plaintext letters with a ? inserted at some symbol position q (98 symbols); a move T on 98 cells; the carved "
        "text is ? followed by the 97 letters, so T must send q to position 0, which fixes q for each T. Moves: one grid "
        "of width 2-97 (ragged bottom row) read from any of four corners (columns left to right bottom-up, right to left "
        "top-down, left to right top-down, right to left bottom-up), forward and inverse; two such grids at every width "
        "pair and reading pair, forward and inverse (repeating key only); K3's rule a + b i mod 98 for b prime to 98; "
        "seven-column shuffles in all 5,040 orders, forward and inverse. Keys on the 97 letters: periodic tableau key "
        "1-26 after the move (slot = carved letter position mod p), before it (slot = plaintext letter position mod p), "
        "or before it with the ? taking a slot (slot = symbol position mod p), 8 classes; plaintext and ciphertext "
        "autokey, lags 1-96, one alphabet throughout, three modes, after or before the move (not with two-grid moves "
        "at widths that do not divide 98). Exact; ten shuffled coppers (the 97 letters shuffled, the ? kept first)."
    ),
    "hypothesis_eli5": (
        "On the sculpture a question mark sits just before K4. Counted with it, K4 has 98 symbols, and 98 fills a grid "
        "of 7 by 14 exactly, the way the third message's 336 letters filled its grid. Perhaps the question mark was part "
        "of the message, the grid was turned so that it came out first, and the letters were then keyed. We try every "
        "grid and every way of reading it out that puts the question mark in front, with a repeating secret word or an "
        "autokey, and the same on ten scrambled coppers."
    ),
    "prediction": (
        "Nothing live below period 22 for the repeating keys beyond the shuffled-copper rate; no autokey setting passes "
        "five checks; counts at every level inside the control range, give or take the spread at the lowest levels. "
        "Zero candidates."
    ),
    "method": (
        "1. Build every move on 98 cells and find the ? position it brings to the front. 2. Turn it into a reordering "
        "of the 97 letters. 3. Test a repeating key of length 1-26 in three placements by the forced-letter slots. 4. For "
        "the one-grid moves, full two-grid moves, K3's rule and the seven-column shuffles, test the plaintext and "
        "ciphertext autokeys at every lag on either side. 5. Count survivors on K4 and ten shuffled coppers; list K4's "
        "survivors below period 20 or with four or more checks, with the ? position."
    ),
    "walkthrough": (
        "1. Put a ? at the end of the message: 98 symbols. 2. Write them in rows of 14: seven full rows, no blank cell. 3. Read the columns from right to left, each from the bottom up. The first cell read is the last one, the ?, so it is carved first, as on the sculpture. 4. Place 22, the E of EAST, is in row 1, column 7. Columns 13 to 8 give 42 symbols; column 7 read from the bottom reaches row 1 at its sixth cell, symbol 48, which is carved letter 47 once the ? is set aside. 5. Key the 97 letters with a repeating key or an autokey; each known letter and the copper letter where it landed tie the key, and the ties must agree. 6. Repeat for every grid width, reading corner, second grid, K3's rule on 98, every order of seven columns, every key, and ten scrambled coppers."
    ),
}

import random
from itertools import permutations
from math import gcd
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.ciphers import columnar_transposition_encrypt

N = 97
M = 98
PMAX = 26
LAGS = range(1, N)
ALPH = {"std": STD, "kry": KRY}
N_CONTROLS = 10
MODES = {"vig": (-1, 1), "beau": (1, -1), "var": (1, 1)}
READS = ("cw", "ccw", "down", "upr")


def read_grid(n, w, how):
    """Order in which the cells 0..n-1 of rows of w (ragged bottom row) are read out."""
    h = -(-n // w)
    cols = range(w) if how in ("cw", "down") else range(w - 1, -1, -1)
    up = how in ("cw", "upr")
    out = []
    for c in cols:
        rows = range(h - 1, -1, -1) if up else range(h)
        for r in rows:
            i = r * w + c
            if i < n:
                out.append(i)
    return out


def where98_from_sigma(sigma):
    w = [0] * M
    for j, i in enumerate(sigma):
        w[i] = j
    return w


def to97(w98):
    """The ? sits at q, the symbol sent to 0. Letter i of the message is symbol i (i < q) or i + 1; it lands at carved letter w98[s] - 1."""
    q = w98.index(0)
    return q, tuple(w98[i if i < q else i + 1] - 1 for i in range(N))


def moves():
    """Yield (name, where98, autokey_too)."""
    for w in range(2, M):
        for how in READS:
            sig = read_grid(M, w, how)
            fw = where98_from_sigma(sig)
            yield (f"one grid w={w} {how}", fw, True)
            yield (f"one grid w={w} {how} inverse", list(sig), True)
    for b in range(1, M):
        if gcd(b, M) != 1:
            continue
        for a in range(M):
            yield (f"K3 rule a={a} b={b}", [(a + b * i) % M for i in range(M)], True)
    idx = "".join(chr(0x100 + i) for i in range(M))
    for seq in permutations(range(7)):
        out = columnar_transposition_encrypt(idx, list(seq))
        sig = [ord(ch) - 0x100 for ch in out]
        yield (f"seven columns {''.join(map(str, seq))}", where98_from_sigma(sig), True)
        yield (f"seven columns {''.join(map(str, seq))} inverse", sig, True)
    single = {(w, how): where98_from_sigma(read_grid(M, w, how)) for w in range(2, M) for how in READS}
    for (w1, h1), A1 in single.items():
        for (w2, h2), A2 in single.items():
            fw = [A2[A1[i]] for i in range(M)]
            inv = [0] * M
            for i, j in enumerate(fw):
                inv[j] = i
            full = M % w1 == 0 and M % w2 == 0
            yield (f"two grids w={w1} {h1} then w={w2} {h2}", fw, full)
            yield (f"two grids w={w1} {h1} then w={w2} {h2} inverse", inv, full)


def slot_pairs(slots):
    last, prs = {}, []
    for e, s in enumerate(slots):
        if s in last:
            prs.append((last[s], e))
        last[s] = e
    return prs


def ct_dec(mode, c, k):
    return {"vig": (c - k) % 26, "beau": (k - c) % 26, "var": (c + k) % 26}[mode]


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    places = sorted(known)
    pidx = [p - 1 for p in places]
    rng = random.Random(86)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    T = len(texts)
    assert read_grid(14, 7, "cw") == [7, 0, 8, 1, 9, 2, 10, 3, 11, 4, 12, 5, 13, 6]
    classes = [(pa, ca, beau) for pa in ALPH for ca in ALPH for beau in (False, True)]
    CI = {an: [[{c: i for i, c in enumerate(ALPH[an])}[ch] for ch in t] for t in texts] for an in ALPH}
    PI = {an: [{c: i for i, c in enumerate(ALPH[an])}[known[p]] for p in places] for an in ALPH}
    G = [[[[((CI[ca][t][j] + PI[pa][e]) if beau else (CI[ca][t][j] - PI[pa][e])) % 26 for j in range(N)]
           for e in range(24)] for t in range(T)] for pa, ca, beau in classes]
    pairsB = [None] + [slot_pairs([i % p for i in pidx]) for p in range(1, PMAX + 1)]
    live = {o: [[0] * (PMAX + 1) for _ in range(T)] for o in ("A", "B", "B98")}
    low = []
    convs = [(an, m) for an in ALPH for m in MODES]
    TI, KI = CI, PI
    counts = {(k, o): [dict() for _ in range(T)] for k in ("ptak", "ctak") for o in "AB"}
    hits = []
    pairsB_ak = {}
    for L in LAGS:
        last, prs = {}, []
        for e, i in enumerate(pidx):
            r = i % L
            if r in last:
                prs.append((last[r], e))
            last[r] = e
        prs.sort(key=lambda pr: pidx[pr[1]] - pidx[pr[0]])
        pairsB_ak[L] = prs
    seen = set()
    n_routes = n_ak = 0
    qhist = {}
    stopped = None
    for spec, w98, ak in moves():
        if n_routes % 500 == 0 and ctx.time_left() < 60:
            stopped = spec
            break
        q, w = to97(w98)
        if w in seen:
            continue
        seen.add(w)
        n_routes += 1
        land = [w[i] for i in pidx]
        sym = [i if i < q else i + 1 for i in pidx]
        pairsA = [None] + [slot_pairs([j % p for j in land]) for p in range(1, PMAX + 1)]
        pairsS = [None] + [slot_pairs([s % p for s in sym]) for p in range(1, PMAX + 1)]
        for ci in range(8):
            for t in range(T):
                g = G[ci][t]
                f = [g[e][land[e]] for e in range(24)]
                for o, prs_by in (("A", pairsA), ("B", pairsB), ("B98", pairsS)):
                    Lv = live[o][t]
                    for p in range(1, PMAX + 1):
                        for a, b in prs_by[p]:
                            if f[a] != f[b]:
                                break
                        else:
                            Lv[p] += 1
                            if t == 0 and p < 20:
                                low.append({"route": spec, "q": q, "order": o, "class": ci, "period": p})
                                qhist[q] = qhist.get(q, 0) + 1
        if not ak:
            continue
        n_ak += 1
        landord = sorted(range(24), key=lambda e: land[e])
        for an, mode in convs:
            sig, tau = MODES[mode]
            KIa = KI[an]
            for t in range(T):
                C = TI[an][t]
                X = [C[w[i]] for i in range(N)]
                for L in LAGS:
                    # ---- plaintext autokey, order A: known Z at landing places, chain through C
                    last, prs = {}, []
                    for e in landord:
                        r = land[e] % L
                        if r in last:
                            prs.append((last[r], e))
                        last[r] = e
                    if prs:
                        ok = True
                        for e1, e2 in prs:
                            z, j, j2 = KIa[e1], land[e1] + L, land[e2]
                            while j <= j2:
                                z = (sig * z + tau * C[j]) % 26; j += L
                            if z != KIa[e2]:
                                ok = False; break
                        if ok:
                            c = len(prs); d = counts[("ptak", "A")][t]; d[c] = d.get(c, 0) + 1
                            if t == 0 and c >= 4:
                                hits.append({"kind": "plaintext autokey", "order": "A", "route": spec, "alphabet": an, "mode": mode, "lag": L, "checks": c})
                    # ---- plaintext autokey, order B: known Z in place, chain through X
                    prs = pairsB_ak[L]
                    if prs:
                        ok = True
                        for e1, e2 in prs:
                            z, j, j2 = KIa[e1], pidx[e1] + L, pidx[e2]
                            while j <= j2:
                                z = (sig * z + tau * X[j]) % 26; j += L
                            if z != KIa[e2]:
                                ok = False; break
                        if ok:
                            c = len(prs); d = counts[("ptak", "B")][t]; d[c] = d.get(c, 0) + 1
                            if t == 0 and c >= 4:
                                hits.append({"kind": "plaintext autokey", "order": "B", "route": spec, "alphabet": an, "mode": mode, "lag": L, "checks": c})
                    # ---- ciphertext autokey, order A: Z[j] = dec(C[j], C[j-L]) at landing places
                    c = 0; ok = True
                    for e in range(24):
                        j = land[e]
                        if j >= L:
                            if ct_dec(mode, C[j], C[j - L]) != KIa[e]:
                                ok = False; break
                            c += 1
                    if ok and c:
                        d = counts[("ctak", "A")][t]; d[c] = d.get(c, 0) + 1
                        if t == 0 and c >= 4:
                            hits.append({"kind": "ciphertext autokey", "order": "A", "route": spec, "alphabet": an, "mode": mode, "lag": L, "checks": c})
                    # ---- ciphertext autokey, order B: P[i] = dec(X[i], X[i-L]) in place
                    c = 0; ok = True
                    for e in range(24):
                        i = pidx[e]
                        if i >= L:
                            if ct_dec(mode, X[i], X[i - L]) != KIa[e]:
                                ok = False; break
                            c += 1
                    if ok and c:
                        d = counts[("ctak", "B")][t]; d[c] = d.get(c, 0) + 1
                        if t == 0 and c >= 4:
                            hits.append({"kind": "ciphertext autokey", "order": "B", "route": spec, "alphabet": an, "mode": mode, "lag": L, "checks": c})
    summary, outside = {}, []
    for (kind, order), per in counts.items():
        ge = lambda d, c0: sum(v for c, v in d.items() if c >= c0)
        k4 = {c0: ge(per[0], c0) for c0 in range(1, 7)}
        ctl = {c0: [ge(per[t], c0) for t in range(1, T)] for c0 in range(1, 7)}
        out = [c0 for c0 in range(1, 7) if not (min(ctl[c0]) <= k4[c0] <= max(ctl[c0]))]
        if out:
            outside.append(f"{kind} {order}: {out}")
        summary[f"{kind} order {order}"] = {"k4_at_least_c": k4, "controls_at_least_c": ctl}
    orders = ("A", "B", "B98")
    p_out = {o: [p for p in range(1, PMAX + 1) if not (min(live[o][t][p] for t in range(1, T)) <= live[o][0][p] <= max(live[o][t][p] for t in range(1, T)))] for o in orders}
    for h in low:
        c = classes[h["class"]]
        h["class"] = f"{c[0]}/{c[1]}/{'beau' if c[2] else 'vig-var'}"
    bounds = {
        "family": "98 cells with the ? sent to the front: grids, K3 rule mod 98, seven-column shuffles; periodic key or autokey on the 97 letters",
        "distinct_routes": n_routes, "routes_with_autokey": n_ak, "stopped_at": stopped,
        "periodic": {"k4_live_by_period": {o: live[o][0][1:] for o in orders},
                     "controls_min": {o: [min(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in orders},
                     "controls_max": {o: [max(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in orders},
                     "periods_outside_control_range": p_out, "k4_live_below_20": low[:40], "n_k4_live_below_20": len(low),
                     "controls_live_below_20": {o: [sum(live[o][t][p] for p in range(1, 20)) for t in range(1, T)] for o in orders}},
        "autokey": {"by_kind_and_order": summary, "levels_outside_control_range": outside,
                    "k4_settings_with_4_plus_checks": hits[:40], "n_k4_4_plus": len(hits)},
        "orders": {"A": "move, then key (slot = carved letter position)", "B": "key, then move (slot = letter position)",
                   "B98": "key, then move, the ? taking a key slot (slot = symbol position)"},
        "controls": f"{N_CONTROLS} shuffled coppers (seed 86), the ? kept in front, identical search",
    }
    line = "; ".join(f"{k}: K4 >=1..6 {[v['k4_at_least_c'][c] for c in range(1, 7)]}, controls max "
                     f"{[max(v['controls_at_least_c'][c]) for c in range(1, 7)]}" for k, v in summary.items())
    notes = (f"{n_routes:,} distinct 98-cell routes ({n_ak:,} with autokeys). Periodic: K4 live below 20: {len(low)}; controls "
             f"{bounds['periodic']['controls_live_below_20']}; periods outside the control range {p_out}. Autokey: {line}. "
             f"Outside: {outside or 'none'}. K4 autokey settings with 4+ checks: {len(hits)}."
             + (f" Stopped at {stopped} for time." if stopped else ""))
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    lines = ["98 cells in rows of 14 (7 rows, full), read right to left, each column bottom-up: the first cell read is the last one,",
             "so the ? must be the last symbol of the message (q = 97) to be carved first.", ""]
    sig = read_grid(M, 14, "upr")
    w98 = where98_from_sigma(sig)
    q, w = to97(w98)
    lines.append(f"? position in the message: {q}")
    lines.append("place  letter  row  column  carved place")
    for p in (22, 23, 64, 65, 74):
        i = p - 1
        lines.append(f"{p:>5}  {known[p]:>6}  {i // 14:>3}  {i % 14:>6}  {w[i] + 1:>12}  ({ct[w[i]]})")
    return "\n".join(lines)
