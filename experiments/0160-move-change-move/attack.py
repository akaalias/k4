"""Experiment 0160 (F6.6). See program.md for the contract."""

EXPERIMENT = {
    "slug": "move-change-move",
    "title": "F6.6: move, change, move again: a grid reading or K3's rule, then a repeating key on the table, then a second move, every pair from a library of 950 moves",
    "family": "6-transposition-then-tableau",
    "parent": "0080-key-on-both-sides-of-the-move",
    "changed": (
        "F6.6 (pivot audit, issue #55, D4; directions.md type 1, 'move, change, move again'). 0080 tested key-move-key; "
        "the move-key-move sandwich was dropped after P3. Here: the message moved by M1, enciphered by a repeating key on "
        "the standard or KRYPTOS table, then moved by M2. The key's slots follow M1's places, the carved letters sit at "
        "M2(M1). Library: the four column readings (0134's) at every width 2-96 and K3's rule i -> b i mod 97 for every "
        "multiplier b, each forwards and inverted: 950 moves, every ordered pair (902,500), compiled, exact; ten scrambled "
        "coppers."
    ),
    "hypothesis_expert": (
        "C1(a) and C1(c) (Sanborn, CNN 2005: 'a matrix code... double matrixes and triple matrixes... then went back to "
        "this table', knowledge/sources/cnn-2005-sanborn-interview-transcript.txt), C2(a) (K3's rule), C20(a) ('layer "
        "two'). Model: c_{M2(M1(i))} = T(p_i, k[M1(i) mod p]) for one of 8 table classes (plain and cipher alphabets "
        "standard or KRYPTOS, Beaufort or not), p 1-26. A period is live if no slot holds two different forced key "
        "letters. Statistic fixed before the run (0134's): cells (p) where K4's live count is above every copper's, "
        "against each copper's count against the rest; K4's settings live below 20 listed."
    ),
    "hypothesis_eli5": (
        "Write the message in a grid and copy it out, encipher it with a repeating secret word on the sculpture's table, "
        "then write the result in a grid again and copy it out once more. We try every pair of grid readings and K3's own "
        "counting rule as the two moves, with secret words of 1 to 26 letters, against the 24 known letters and "
        "scrambled copies of the carved text."
    ),
    "prediction": "Nothing live below key length 20 beyond the coppers' rate; K4 above every copper in no more cells than the null's maximum. Zero candidates.",
    "method": (
        "1. Build the 950 moves (where-maps). "
        "2. For each ordered pair: the slot of each known letter (M1's place mod p) and its carved letter (at M2(M1)). "
        "3. Compiled: per class and text, live periods 1-26; counts. "
        "4. K4 against the coppers with the fixed statistic."
    ),
    "walkthrough": (
        "1. Write the 97 letters in rows of 9 and copy them out down the columns (move 1). "
        "2. Encipher the moved text with a repeating word on the sculpture's table. "
        "3. Write that in rows of 13 and copy it out up the columns (move 2): this is the carved text. "
        "4. Follow each known letter: its key slot is its place after move 1, mod the word length; its carved letter is at its place after move 2. "
        "5. Two known letters in one slot must force the same key letter. Repeat for every pair of moves and every length."
    ),
}

import ctypes
import random
import time
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
N_CONTROLS = 10
READINGS = ("cw", "ccw", "col", "colr")

RT_SOURCE = r"""
// F6.3b: three matrix stages (rows of w, columns read one of four ways), every reading triple except all-cw,
// widths 2-96 with at least one width >= 25; forward and inverse; then (A) or before (B) a periodic key 1-26 on
// 8 classes of the standard/KRYPTOS tables. Counts live (order, period) settings per text, deduplicated by the
// full permutation within one first stage.
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define N 97
#define PMAX 26
#define NW 95          // widths 2..96
#define NR 4           // readings cw, ccw, col, colr

static int WH[NW][NR][N];          // where-map of one stage
static int T;                      // texts
static int CI[2][16][N];           // carved letter index under std (0) / kry (1), per text
static int PI[2][24];              // known letter index under std / kry
static int PIDX[24];               // known message places (0-based)
static int PB[PMAX + 1][24][2], NPB[PMAX + 1];   // order B pairs, fixed

void set_tables(const int *wh, int t, const int *ci, const int *pi, const int *pidx) {
    memcpy(WH, wh, sizeof WH);
    T = t;
    for (int a = 0; a < 2; a++) for (int x = 0; x < t; x++) for (int j = 0; j < N; j++) CI[a][x][j] = ci[(a * t + x) * N + j];
    for (int a = 0; a < 2; a++) for (int e = 0; e < 24; e++) PI[a][e] = pi[a * 24 + e];
    for (int e = 0; e < 24; e++) PIDX[e] = pidx[e];
    for (int p = 1; p <= PMAX; p++) {
        int last[PMAX]; for (int s = 0; s < p; s++) last[s] = -1;
        NPB[p] = 0;
        for (int e = 0; e < 24; e++) { int s = PIDX[e] % p; if (last[s] >= 0) { PB[p][NPB[p]][0] = last[s]; PB[p][NPB[p]][1] = e; NPB[p]++; } last[s] = e; }
    }
}

static void test_route(const int *wh, long *live, long *low, long *k4low, int *k4low_ex, int *nex, int ex_cap,
                       int r1, int w1, int r2, int w2, int r3, int w3, int dir) {
    int land[24];
    for (int e = 0; e < 24; e++) land[e] = wh[PIDX[e]];
    static int PA[PMAX + 1][24][2]; int NPA[PMAX + 1];
    for (int p = 1; p <= PMAX; p++) {
        int last[PMAX]; for (int s = 0; s < p; s++) last[s] = -1;
        NPA[p] = 0;
        for (int e = 0; e < 24; e++) { int s = land[e] % p; if (last[s] >= 0) { PA[p][NPA[p]][0] = last[s]; PA[p][NPA[p]][1] = e; NPA[p]++; } last[s] = e; }
    }
    for (int pa = 0; pa < 2; pa++) for (int ca = 0; ca < 2; ca++) for (int beau = 0; beau < 2; beau++) {
        for (int t = 0; t < T; t++) {
            int f[24];
            for (int e = 0; e < 24; e++) {
                int c = CI[ca][t][land[e]], pp = PI[pa][e];
                f[e] = beau ? (c + pp) % 26 : ((c - pp) % 26 + 26) % 26;
            }
            for (int o = 0; o < 2; o++) {
                int first = 0;
                for (int p = 1; p <= PMAX; p++) {
                    int n = o == 0 ? NPA[p] : NPB[p], ok = 1;
                    for (int q = 0; q < n; q++) {
                        int a = o == 0 ? PA[p][q][0] : PB[p][q][0], b = o == 0 ? PA[p][q][1] : PB[p][q][1];
                        if (f[a] != f[b]) { ok = 0; break; }
                    }
                    if (ok) { live[(o * T + t) * (PMAX + 1) + p]++; if (!first) first = p; }
                }
                if (first && first < 20) {
                    low[o * T + t]++;
                    if (t == 0) {
                        k4low[0]++;
                        if (*nex < ex_cap) {
                            int *x = k4low_ex + 11 * (*nex);
                            x[0] = r1; x[1] = w1; x[2] = r2; x[3] = w2; x[4] = r3; x[5] = w3; x[6] = dir; x[7] = o;
                            x[8] = pa * 4 + ca * 2 + beau; x[9] = first; x[10] = 0;
                            (*nex)++;
                        }
                    }
                }
            }
        }
    }
}


// test a batch of where-maps (n x 97); each map is one route (already deduplicated by the caller)
void test_maps(const int *maps, int n, long *live, long *low, long *k4low, int *ex, int *nex, int ex_cap) {
    for (int r = 0; r < n; r++) test_route(maps + 97 * r, live, low, k4low, ex, nex, ex_cap, r, 0, 0, 0, 0, 0, 0);
}

static void test_route2(const int *whs, const int *whc, long *live, long *low, long *k4low, int *k4low_ex, int *nex, int ex_cap,
                       int r1, int w1, int r2, int w2, int r3, int w3, int dir) {
    int land[24], landc[24];
    for (int e = 0; e < 24; e++) { land[e] = whs[PIDX[e]]; landc[e] = whc[PIDX[e]]; }
    static int PA[PMAX + 1][24][2]; int NPA[PMAX + 1];
    for (int p = 1; p <= PMAX; p++) {
        int last[PMAX]; for (int s = 0; s < p; s++) last[s] = -1;
        NPA[p] = 0;
        for (int e = 0; e < 24; e++) { int s = land[e] % p; if (last[s] >= 0) { PA[p][NPA[p]][0] = last[s]; PA[p][NPA[p]][1] = e; NPA[p]++; } last[s] = e; }
    }
    for (int pa = 0; pa < 2; pa++) for (int ca = 0; ca < 2; ca++) for (int beau = 0; beau < 2; beau++) {
        for (int t = 0; t < T; t++) {
            int f[24];
            for (int e = 0; e < 24; e++) {
                int c = CI[ca][t][landc[e]], pp = PI[pa][e];
                f[e] = beau ? (c + pp) % 26 : ((c - pp) % 26 + 26) % 26;
            }
            for (int o = 0; o < 2; o++) {
                int first = 0;
                for (int p = 1; p <= PMAX; p++) {
                    int n = o == 0 ? NPA[p] : NPB[p], ok = 1;
                    for (int q = 0; q < n; q++) {
                        int a = o == 0 ? PA[p][q][0] : PB[p][q][0], b = o == 0 ? PA[p][q][1] : PB[p][q][1];
                        if (f[a] != f[b]) { ok = 0; break; }
                    }
                    if (ok) { live[(o * T + t) * (PMAX + 1) + p]++; if (!first) first = p; }
                }
                if (first && first < 20) {
                    low[o * T + t]++;
                    if (t == 0) {
                        k4low[0]++;
                        if (*nex < ex_cap) {
                            int *x = k4low_ex + 11 * (*nex);
                            x[0] = r1; x[1] = w1; x[2] = r2; x[3] = w2; x[4] = r3; x[5] = w3; x[6] = dir; x[7] = o;
                            x[8] = pa * 4 + ca * 2 + beau; x[9] = first; x[10] = 0;
                            (*nex)++;
                        }
                    }
                }
            }
        }
    }
}



// move-key-move: slots follow the first map, carved letters the second (composed) map; only order A is meaningful
void test_pairs(const int *mslot, const int *mcarv, int n, long *live, long *low, long *k4low, int *ex, int *nex, int ex_cap) {
    for (int r = 0; r < n; r++) test_route2(mslot + 97 * r, mcarv + 97 * r, live, low, k4low, ex, nex, ex_cap, r, 0, 0, 0, 0, 0, 0);
}
"""


def rt_build(texts, known_list):
    import ctypes, os, subprocess, tempfile
    from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
    d = tempfile.mkdtemp(prefix="k4_rt_")
    src, so = os.path.join(d, "rt.c"), os.path.join(d, "rt.so")
    open(src, "w").write(RT_SOURCE)
    subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", so, src], check=True, capture_output=True)
    lib = ctypes.CDLL(so)
    wh = [0] * (95 * 4 * 97)            # unused stage table (the route tester takes whole maps)
    ci = []
    for A in (STD, KRY):
        for t in texts:
            ci += [A.index(ch) for ch in t]
    pi = [STD.index(a) for _, a in known_list] + [KRY.index(a) for _, a in known_list]
    pidx = [q - 1 for q, _ in known_list]
    I = lambda v: (ctypes.c_int * len(v))(*v)
    lib.set_tables(I(wh), len(texts), I(ci), I(pi), I(pidx))
    return lib


def rt_reference(wh, texts, known_list, o, t):
    """Python count of live periods 1-26 for one route, order o (0: route then key; 1: key then route), text t."""
    from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
    kp = [q for q, _ in known_list]
    land = [wh[q - 1] for q in kp]
    cnt = [0] * 27
    for pa in (STD, KRY):
        for ca in (STD, KRY):
            for beau in (0, 1):
                f = [((ca.index(texts[t][j]) + pa.index(a)) if beau else (ca.index(texts[t][j]) - pa.index(a))) % 26 for j, (_, a) in zip(land, known_list)]
                for p in range(1, 27):
                    slots, ok = {}, True
                    for e in range(24):
                        s_ = (land[e] if o == 0 else kp[e] - 1) % p
                        if slots.setdefault(s_, f[e]) != f[e]:
                            ok = False
                            break
                    cnt[p] += ok
    return cnt


def rt_worker(args):
    import ctypes
    batch, texts, known_list = args
    lib = rt_build(texts, known_list)
    T = len(texts)
    live = (ctypes.c_long * (2 * T * 27))(); low = (ctypes.c_long * (2 * T))(); k4l = (ctypes.c_long * 1)()
    ex = (ctypes.c_int * (11 * 200))(); nex = ctypes.c_int(0)
    flat = [v for _, m in batch for v in m]
    lib.test_maps((ctypes.c_int * len(flat))(*flat), len(batch), live, low, k4l, ex, ctypes.byref(nex), 200)
    exl = []
    for j in range(nex.value):
        x = list(ex[11 * j: 11 * j + 11])
        cls = x[8]
        exl.append({"route": batch[x[0]][0], "order": "AB"[x[7]], "class": f"{('std', 'kry')[cls >> 2]}/{('std', 'kry')[(cls >> 1) & 1]}/{'beau' if cls & 1 else 'vig-var'}", "period": x[9]})
    return list(live), list(low), exl


def rt_run(named_maps, texts, known_list, workers=8, batch=2000):
    """Test every (name, where-map) route; return live counts and the fixed statistic (0134's)."""
    import multiprocessing as mp, sys, types
    T = len(texts)
    # check the compiled tester against Python on a few routes
    lib = rt_build(texts, known_list)
    import ctypes, random as _r
    vr = _r.Random(7)
    for name, m in vr.sample(named_maps, min(5, len(named_maps))):
        live = (ctypes.c_long * (2 * T * 27))(); low = (ctypes.c_long * (2 * T))(); k4l = (ctypes.c_long * 1)()
        ex = (ctypes.c_int * 11)(); nex = ctypes.c_int(0)
        lib.test_maps((ctypes.c_int * 97)(*m), 1, live, low, k4l, ex, ctypes.byref(nex), 0)
        for o in (0, 1):
            for t in (0, 1):
                assert [live[(o * T + t) * 27 + p] for p in range(1, 27)] == rt_reference(m, texts, known_list, o, t)[1:], name
    jobs = [(named_maps[i:i + batch], texts, known_list) for i in range(0, len(named_maps), batch)]
    mod = sys.modules.get(__name__)
    if getattr(mod, "rt_worker", None) is not rt_worker:
        m = types.ModuleType(__name__); m.__dict__.update(globals()); sys.modules[__name__] = m
    with mp.get_context("fork").Pool(workers) as pool:
        parts = pool.map(rt_worker, jobs, chunksize=1)
    live = [[[sum(p[0][(o * T + t) * 27 + L] for p in parts) for L in range(27)] for t in range(T)] for o in (0, 1)]
    low = [[sum(p[1][o * T + t] for p in parts) for t in range(T)] for o in (0, 1)]
    ex = [x for p in parts for x in p[2]]
    cells = [(o, L) for o in (0, 1) for L in range(1, 27)]

    def above(t):
        return [("AB"[o], L) for o, L in cells if live[o][t][L] > max(live[o][u][L] for u in range(T) if u != t)]
    k4_above = above(0)
    null = [len(above(t)) for t in range(1, T)]
    first = {"AB"[o]: next((L for L in range(1, 27) if live[o][0][L]), None) for o in (0, 1)}
    cfirst = {"AB"[o]: min(next((L for L in range(1, 27) if live[o][t][L]), 99) for t in range(1, T)) for o in (0, 1)}
    return {"routes": len(named_maps), "k4_live_by_period": {"AB"[o]: live[o][0][1:] for o in (0, 1)},
            "controls_live_by_period_min": {"AB"[o]: [min(live[o][t][L] for t in range(1, T)) for L in range(1, 27)] for o in (0, 1)},
            "controls_live_by_period_max": {"AB"[o]: [max(live[o][t][L] for t in range(1, T)) for L in range(1, 27)] for o in (0, 1)},
            "k4_shortest_live": first, "coppers_shortest_live": cfirst,
            "k4_settings_live_below_20": {"AB"[o]: low[o][0] for o in (0, 1)}, "controls_settings_live_below_20": {"AB"[o]: low[o][1:] for o in (0, 1)},
            "k4_live_below_20": sorted(ex, key=lambda x: x["period"])[:40],
            "cells_k4_above_every_copper": k4_above, "null_cells_above_rest_per_copper": null,
            "stop_queue": len(k4_above) > max(null)}


def dedupe(named_maps):
    seen, out = set(), []
    for name, m in named_maps:
        for d, mm in (("fwd", m), ("inv", inverse(m))):
            key = bytes(mm)
            if key in seen:
                continue
            seen.add(key)
            out.append((f"{name} {d}", list(mm)))
    return out


def inverse(m):
    inv = [0] * len(m)
    for i, j in enumerate(m):
        inv[j] = i
    return inv



def stage(tokens, w, r):
    rows = [tokens[i:i + w] for i in range(0, len(tokens), w)]
    cols = range(w) if r in ("cw", "col") else range(w - 1, -1, -1)
    up = r in ("cw", "colr")
    out = []
    for c in cols:
        rr = reversed(rows) if up else rows
        out.extend(row[c] for row in rr if c < len(row))
    return out


def where(seq):
    wh = [0] * len(seq)
    for j, i in enumerate(seq):
        wh[i] = j
    return wh


def library():
    lib_ = []
    for w in range(2, N):
        for r in READINGS:
            lib_.append((f"{r}{w}", where(stage(list(range(N)), w, r))))
    for b in range(2, N):
        lib_.append((f"k3x{b}", [(b * i) % N for i in range(N)]))
    out, seen = [], set()
    for name, m in lib_:
        for d, mm in (("", m), ("inv", inverse(m))):
            k = bytes(mm)
            if k not in seen:
                seen.add(k); out.append((name + d, mm))
    return out


def pair_worker(args):
    i0, i1, libm, texts, known_list = args
    lib = rt_build(texts, known_list)
    T = len(texts)
    live = (ctypes.c_long * (2 * T * 27))(); low = (ctypes.c_long * (2 * T))(); k4l = (ctypes.c_long * 1)()
    ex = (ctypes.c_int * (11 * 200))(); nex = ctypes.c_int(0)
    names = []
    for a in range(i0, i1):
        n1, m1 = libm[a]
        slots, carv = [], []
        for n2, m2 in libm:
            slots += m1
            carv += [m2[m1[i]] for i in range(N)]
            names.append((n1, n2))
        n = len(libm)
        e0 = nex.value
        lib.test_pairs((ctypes.c_int * len(slots))(*slots), (ctypes.c_int * len(carv))(*carv), n, live, low, k4l, ex, ctypes.byref(nex), 200)
        for j in range(e0, nex.value):
            ex[11 * j] += (a - i0) * n        # route index within this worker's names
    exl = []
    for j in range(nex.value):
        x = list(ex[11 * j: 11 * j + 11])
        cls = x[8]
        if x[7] == 0:
            exl.append({"moves": list(names[x[0]]), "class": f"{('std', 'kry')[cls >> 2]}/{('std', 'kry')[(cls >> 1) & 1]}/{'beau' if cls & 1 else 'vig-var'}", "period": x[9]})
    return list(live), list(low), exl


def run(ctx):
    import multiprocessing as mp
    import sys
    import types
    ct, known = ctx.K4, ctx.KNOWN
    known_list = [(q, known[q]) for q in sorted(known)]
    libm = library()
    # the sandwich: composed carved map equals running move 1, then move 2
    pt = [chr(65 + random.Random(5).randrange(26)) for _ in range(N)]
    a_, b_ = libm[10][1], libm[500][1]
    s1 = [""] * N
    for i in range(N):
        s1[a_[i]] = pt[i]
    s2 = [""] * N
    for j in range(N):
        s2[b_[j]] = s1[j]
    assert all(s2[b_[a_[i]]] == pt[i] for i in range(N))
    rng = random.Random(1606)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    T = len(texts)
    # the compiled pair test on the identity second move must equal the single-route reference (order A)
    lib = rt_build(texts, known_list)
    ident = list(range(N))
    for name, m in libm[:3]:
        live = (ctypes.c_long * (2 * T * 27))(); low = (ctypes.c_long * (2 * T))(); k4l = (ctypes.c_long * 1)()
        ex = (ctypes.c_int * 11)(); nex = ctypes.c_int(0)
        lib.test_pairs((ctypes.c_int * 97)(*m), (ctypes.c_int * 97)(*m), 1, live, low, k4l, ex, ctypes.byref(nex), 0)
        assert [live[(0 * T + 0) * 27 + p] for p in range(1, 27)] == rt_reference(m, texts, known_list, 0, 0)[1:]
    W = 8
    chunk = -(-len(libm) // (W * 4))
    jobs = [(i, min(i + chunk, len(libm)), libm, texts, known_list) for i in range(0, len(libm), chunk)]
    if getattr(sys.modules.get(__name__), "pair_worker", None) is not pair_worker:
        m = types.ModuleType(__name__); m.__dict__.update(globals()); sys.modules[__name__] = m
    t0 = time.time()
    with mp.get_context("fork").Pool(W) as pool:
        parts = pool.map(pair_worker, jobs, chunksize=1)
    live = [[sum(p[0][(0 * T + t) * 27 + L] for p in parts) for L in range(27)] for t in range(T)]
    low = [sum(p[1][0 * T + t] for p in parts) for t in range(T)]
    ex = [x for p in parts for x in p[2]]

    def above(t):
        return [L for L in range(1, 27) if live[t][L] > max(live[u][L] for u in range(T) if u != t)]
    k4_above = above(0)
    null = [len(above(t)) for t in range(1, T)]
    stop = len(k4_above) > max(null)
    first = next((L for L in range(1, 27) if live[0][L]), None)
    cfirst = min(next((L for L in range(1, 27) if live[t][L]), 99) for t in range(1, T))
    bounds = {"family": "move, repeating key on the standard/KRYPTOS table, move again; 950 moves (four column readings at widths 2-96, K3's rule at every multiplier; forwards and inverted), every ordered pair",
              "moves": len(libm), "pairs": len(libm) ** 2, "periods": [1, 26], "classes": 8,
              "k4_live_by_period": live[0][1:], "controls_live_by_period_min": [min(live[t][L] for t in range(1, T)) for L in range(1, 27)],
              "controls_live_by_period_max": [max(live[t][L] for t in range(1, T)) for L in range(1, 27)],
              "k4_shortest_live": first, "coppers_shortest_live": cfirst,
              "k4_settings_live_below_20": low[0], "controls_settings_live_below_20": low[1:], "k4_live_below_20": sorted(ex, key=lambda x: x["period"])[:40],
              "cells_k4_above_every_copper": k4_above, "null_cells_above_rest_per_copper": null, "stop_queue": stop,
              "seconds": round(time.time() - t0), "controls": f"{N_CONTROLS} shuffled coppers (seed 1606)", "exhaustive": True}
    notes = (f"{len(libm) ** 2:,} move pairs x 8 classes, periods 1-26: shortest live on K4 {first} (coppers {cfirst}); live below 20 K4 {low[0]} "
             f"(coppers {min(low[1:])}-{max(low[1:])}); K4 above every copper in {len(k4_above)} of 26 cells, null {min(null)}-{max(null)}; stop {stop}")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    m1 = where(stage(list(range(N)), 9, "col")); m2 = where(stage(list(range(N)), 13, "colr"))
    lines = ["move 1: rows of 9 read down the columns; key on the table; move 2: rows of 13 read up, right first", "",
             "place  letter  after move 1  slot mod 11  carved place  carved"]
    for q in (22, 23, 24, 64, 65, 74):
        j = m1[q - 1]; c = m2[j]
        lines.append(f"{q:5d}  {known[q]:>6}  {j + 1:12d}  {j % 11:11d}  {c + 1:12d}  {ct[c]:>6}")
    return "\n".join(lines)
