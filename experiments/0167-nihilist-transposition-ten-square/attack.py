"""Experiment 0167 (F6.14). See program.md for the contract."""

EXPERIMENT = {
    "slug": "nihilist-transposition-ten-square",
    "title": "F6.14: the Nihilist transposition on a 10 x 10 square with three blank cells, one key of every order for rows and columns, then or before a repeating key on the table",
    "family": "6-transposition-then-tableau",
    "parent": "0135-hand-padding-at-every-grid-stage",
    "changed": (
        "F6.14. The Nihilist transposition writes the text into a full square and reorders its rows and its columns by "
        "one key, then reads it off by rows (or by columns). 97 is prime, so the square is 10 x 10 with three blank "
        "cells, placed at each of F6.4's eight spots (end or start of the first or last row, top or bottom of the first "
        "or last column). Every one of the 10! = 3,628,800 key orders, both readings, forward and inverse: 116 million "
        "routes, compiled (the route builder checked against Python on 200 random settings), then a repeating key 1-26 "
        "on the standard or KRYPTOS table after or before. Ten scrambled coppers."
    ),
    "hypothesis_expert": (
        "C1(a) ('matrix code'), C17(b) (padding); source: reports/Scheidt patents and field ciphers.md and "
        "foreign_agent_hand_systems.md (ACA's Nihilist transposition: one key for rows and columns of a complete square; "
        "attribution to Russian Nihilists doubtful). Model: cell (r, c) of message place i (row-wise, blanks skipped) "
        "moves to (pi^-1(r), pi^-1(c)); read row-wise (or column-wise) skipping blanks. Periodic key: order A or B, 8 "
        "classes, a period live if no slot holds two different forced letters; 0134's statistic."
    ),
    "hypothesis_eli5": (
        "Write the message into a 10 by 10 square (three squares left empty, since 97 is three short of 100), then "
        "rearrange the rows and the columns in the same order, given by a key, and copy the square out. We try every "
        "possible order of the ten rows and columns, every place for the empty squares and both ways of copying out, "
        "each with a repeating secret word on the sculpture's table, against the 24 known letters and scrambled copies."
    ),
    "prediction": "Nothing live below key length 20 beyond the coppers' rate; K4 above every copper in no more cells than the null's maximum. Zero candidates.",
    "method": (
        "1. Compile the builder and the periodic-key test; check the builder against Python. "
        "2. For each blank place and each first key element (80 jobs): every remaining order (Heap's algorithm), both readings, forward and inverse. "
        "3. Counts per order, period and text; the fixed statistic."
    ),
    "walkthrough": (
        "1. Write the 97 letters into a 10 x 10 square row by row, leaving the last three squares empty. "
        "2. Take a key order of the ten rows and columns, say 3 7 0 9 1 5 2 8 4 6: row 3 becomes the first row, row 7 the second, and the columns likewise. "
        "3. Copy the square out row by row, skipping the empty squares. "
        "4. Note where each known letter lands; with a repeating key of length p on the table, two known letters landing a multiple of p apart must force the same key letter. "
        "5. Repeat for every order, place of the empty squares and reading, and on scrambled copies."
    ),
}

import ctypes
import os
import random
import subprocess
import tempfile
import time
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
N_CONTROLS = 10
WORKERS = 8
PL = [[(9, 7), (9, 8), (9, 9)], [(0, 0), (0, 1), (0, 2)], [(9, 0), (9, 1), (9, 2)], [(0, 7), (0, 8), (0, 9)],
      [(0, 9), (1, 9), (2, 9)], [(7, 9), (8, 9), (9, 9)], [(0, 0), (1, 0), (2, 0)], [(7, 0), (8, 0), (9, 0)]]

C_SOURCE = r"""
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


// Nihilist transposition on a 10 x 10 square with 3 blank cells at one of eight places, one key for rows and
// columns (every permutation of 10), read off by rows (rd 0) or columns (rd 1); forward and inverse maps.
static const int PLACES[8][3][2] = {
    {{9,7},{9,8},{9,9}}, {{0,0},{0,1},{0,2}}, {{9,0},{9,1},{9,2}}, {{0,7},{0,8},{0,9}},
    {{0,9},{1,9},{2,9}}, {{7,9},{8,9},{9,9}}, {{0,0},{1,0},{2,0}}, {{7,0},{8,0},{9,0}}};

static void route_for(const int *pinv, int place, int rd, int *wh) {
    int blank[10][10]; memset(blank, 0, sizeof blank);
    for (int k = 0; k < 3; k++) blank[PLACES[place][k][0]][PLACES[place][k][1]] = 1;
    int bl[3];
    for (int k = 0; k < 3; k++) {
        int r = pinv[PLACES[place][k][0]], c = pinv[PLACES[place][k][1]];
        bl[k] = rd ? c * 10 + r : r * 10 + c;
    }
    int i = 0;
    for (int r = 0; r < 10; r++) for (int c = 0; c < 10; c++) {
        if (blank[r][c]) continue;
        int rr = pinv[r], cc = pinv[c];
        int L = rd ? cc * 10 + rr : rr * 10 + cc;
        int below = 0;
        for (int k = 0; k < 3; k++) if (bl[k] < L) below++;
        wh[i++] = L - below;
    }
}

// all permutations whose first element is `first` (Heap's algorithm over the other 9), one place
void run_place(int first, int place, long *live, long *low, long *k4low, int *ex, int *nex, int ex_cap, long *n_routes) {
    int p[10], c9[9], wh[N], inv[N], pinv[10];
    int rest[9], k = 0;
    for (int v = 0; v < 10; v++) if (v != first) rest[k++] = v;
    for (int j = 0; j < 9; j++) c9[j] = 0;
    int idx = 0;
    while (1) {
        p[0] = first; for (int j = 0; j < 9; j++) p[j + 1] = rest[j];
        for (int j = 0; j < 10; j++) pinv[p[j]] = j;
        for (int rd = 0; rd < 2; rd++) {
            route_for(pinv, place, rd, wh);
            for (int x = 0; x < N; x++) inv[wh[x]] = x;
            test_route(wh, live, low, k4low, ex, nex, ex_cap, place, first, rd, 0, 0, 0, 0);
            test_route(inv, live, low, k4low, ex, nex, ex_cap, place, first, rd, 0, 0, 0, 1);
            (*n_routes) += 2;
        }
        // Heap's algorithm step on rest[0..8]
        while (idx < 9) {
            if (c9[idx] < idx) {
                if (idx % 2 == 0) { int t = rest[0]; rest[0] = rest[idx]; rest[idx] = t; }
                else { int t = rest[c9[idx]]; rest[c9[idx]] = rest[idx]; rest[idx] = t; }
                c9[idx]++; idx = 0; break;
            } else { c9[idx] = 0; idx++; }
        }
        if (idx >= 9) break;
    }
}

int route_one(const int *perm, int place, int rd, int *wh) {
    int pinv[10]; for (int j = 0; j < 10; j++) pinv[perm[j]] = j;
    route_for(pinv, place, rd, wh); return 0;
}
"""


def build(texts, known_list):
    d = tempfile.mkdtemp(prefix="k4_nih_")
    src, so = os.path.join(d, "n.c"), os.path.join(d, "n.so")
    open(src, "w").write(C_SOURCE)
    subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", so, src], check=True, capture_output=True)
    lib = ctypes.CDLL(so)
    ci = []
    for A in (STD, KRY):
        for t in texts:
            ci += [A.index(ch) for ch in t]
    I = lambda v: (ctypes.c_int * len(v))(*v)
    lib.set_tables(I([0] * (95 * 4 * 97)), len(texts), I(ci), I([STD.index(a) for _, a in known_list] + [KRY.index(a) for _, a in known_list]),
                   I([q - 1 for q, _ in known_list]))
    return lib


def reference(perm, place, rd):
    pinv = [0] * 10
    for j, v in enumerate(perm):
        pinv[v] = j
    cells = [(r, c) for r in range(10) for c in range(10) if (r, c) not in PL[place]]
    newpos = [(pinv[r], pinv[c]) for r, c in cells]
    keyf = (lambda t: (t[1], t[0])) if rd else (lambda t: t)
    order = sorted(range(N), key=lambda i: keyf(newpos[i]))
    wh = [0] * N
    for j, i in enumerate(order):
        wh[i] = j
    return wh


def _work(args):
    first, place, texts, known_list, deadline = args
    T = len(texts)
    if time.time() > deadline:
        return [0] * (2 * T * 27), [0] * (2 * T), [], 0, False
    lib = build(texts, known_list)
    live = (ctypes.c_long * (2 * T * 27))(); low = (ctypes.c_long * (2 * T))(); k4l = (ctypes.c_long * 1)()
    ex = (ctypes.c_int * (11 * 50))(); nex = ctypes.c_int(0); nr = ctypes.c_long(0)
    lib.run_place(first, place, live, low, k4l, ex, ctypes.byref(nex), 50, ctypes.byref(nr))
    exl = []
    for j in range(nex.value):
        x = list(ex[11 * j: 11 * j + 11])
        cls = x[8]
        exl.append({"place": x[0], "first": x[1], "read": "columns" if x[2] else "rows", "dir": "inv" if x[6] else "fwd", "order": "AB"[x[7]],
                    "class": f"{('std', 'kry')[cls >> 2]}/{('std', 'kry')[(cls >> 1) & 1]}/{'beau' if cls & 1 else 'vig-var'}", "period": x[9]})
    return list(live), list(low), exl, nr.value, True


def run(ctx):
    import multiprocessing as mp
    import sys
    import types
    ct, known = ctx.K4, ctx.KNOWN
    known_list = [(q, known[q]) for q in sorted(known)]
    lib = build([ct], known_list)
    vr = random.Random(1670)
    for _ in range(200):
        perm = list(range(10)); vr.shuffle(perm); place = vr.randrange(8); rd = vr.randrange(2)
        wh = (ctypes.c_int * N)()
        lib.route_one((ctypes.c_int * 10)(*perm), place, rd, wh)
        assert list(wh) == reference(perm, place, rd)
    rng = random.Random(1670)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    T = len(texts)
    deadline = time.time() + ctx.time_left() - 120
    jobs = [(f, p, texts, known_list, deadline) for p in range(8) for f in range(10)]
    if getattr(sys.modules.get(__name__), "_work", None) is not _work:
        m = types.ModuleType(__name__); m.__dict__.update(globals()); sys.modules[__name__] = m
    t0 = time.time()
    with mp.get_context("fork").Pool(WORKERS) as pool:
        parts = pool.map(_work, jobs, chunksize=1)
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
    bounds = {"family": "Nihilist transposition, 10 x 10 square, three blanks at eight places, one key of every order for rows and columns, read by rows or columns, then or before a periodic key",
              "jobs_done": sum(1 for p in parts if p[4]), "jobs_total": len(jobs), "routes": sum(p[3] for p in parts),
              "builder_checked_against_python": 200,
              "k4_live_by_period": {"AB"[o]: live[o][0][1:] for o in (0, 1)},
              "controls_live_by_period_min": {"AB"[o]: [min(live[o][t][L] for t in range(1, T)) for L in range(1, 27)] for o in (0, 1)},
              "controls_live_by_period_max": {"AB"[o]: [max(live[o][t][L] for t in range(1, T)) for L in range(1, 27)] for o in (0, 1)},
              "k4_shortest_live": first, "coppers_shortest_live": cfirst,
              "k4_settings_live_below_20": {"AB"[o]: low[o][0] for o in (0, 1)}, "controls_settings_live_below_20": {"AB"[o]: low[o][1:] for o in (0, 1)},
              "k4_live_below_20": sorted(ex, key=lambda x: x["period"])[:40],
              "cells_k4_above_every_copper": k4_above, "null_cells_above_rest_per_copper": null, "stop_queue": len(k4_above) > max(null),
              "distinct_routes": sum(p[3] for p in parts), "seconds": round(time.time() - t0),
              "controls": f"{N_CONTROLS} shuffled coppers (seed 1670)", "exhaustive": "every job done is exact"}
    notes = (f"{bounds['routes']:,} routes ({bounds['jobs_done']} of {len(jobs)} jobs): shortest live K4 A {first['A']} B {first['B']} (coppers {cfirst['A']}, {cfirst['B']}); "
             f"K4 above every copper in {len(k4_above)} of 52 cells, null {min(null)}-{max(null)}")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    perm = [3, 7, 0, 9, 1, 5, 2, 8, 4, 6]
    wh = reference(perm, 0, 0)
    lines = ["10 x 10 square, last three cells empty; rows and columns reordered 3 7 0 9 1 5 2 8 4 6; read by rows", "",
             "place  letter  square cell  new cell  lands at  carved"]
    pinv = [0] * 10
    for j, v in enumerate(perm):
        pinv[v] = j
    for q in (22, 23, 24, 64, 65, 74):
        r, c = divmod(q - 1, 10)
        lines.append(f"{q:5d}  {known[q]:>6}  {f'({r},{c})':>11}  {f'({pinv[r]},{pinv[c]})':>8}  {wh[q - 1] + 1:8d}  {ct[wh[q - 1]]:>6}")
    return "\n".join(lines)
