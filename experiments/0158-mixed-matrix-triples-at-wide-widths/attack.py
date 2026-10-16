"""Experiment 0158 (F6.3b). See program.md for the contract."""

EXPERIMENT = {
    "slug": "mixed-matrix-triples-at-wide-widths",
    "title": "F6.3b: every mixed triple of matrix readings with a width of 25 or more, enumerated exactly, then or before a repeating key on the table",
    "family": "6-transposition-then-tableau",
    "parent": "0134-mixed-matrix-readings-two-and-three-stages",
    "changed": (
        "F6.3b. 0134 enumerated every triple of the four column readings at widths 2-24 and every pair at 2-96; triples "
        "with any width from 25 to 96 rested on 0037's sample of 200,000. Here they are enumerated exactly: 63 reading "
        "triples (all-clockwise is 0083) x every width triple in 2-96 with at least one width of 25 or more, forward and "
        "inverse, deduplicated within each first stage. The count (about 95 million distinct routes on 11 texts) does not "
        "fit Python in 30 minutes, so the inner loop is compiled C, written out and compiled by this file and checked "
        "inside the run against a Python reference on random routes."
    ),
    "hypothesis_expert": (
        "C1(a) (Sanborn, CNN 2005, knowledge/sources/cnn-2005-sanborn-interview-transcript.txt: 'you write a line of plain "
        "text out, right, in successive rows. And then basically you write it going from top to bottom... sometimes I used "
        "double matrixes and triple matrixes... and then went back to this table'), C2(a), C11. Stage: write the 97 symbols "
        "in rows of w (last row short) and read the columns one of four ways: cw (left column first, bottom up: the K3 "
        "turn), ccw (right first, top down), col (left first, top down: Sanborn's description), colr (right first, bottom "
        "up). Three stages, widths w1, w2, w3 in 2-96, at least one >= 25 (0134 did all <= 24), 63 reading triples; the "
        "composed permutation and its inverse. Key: periodic tableau 1-26 after (order A, slot = landing place mod p) or "
        "before (order B, slot = message place mod p), 8 classes (plain and cipher alphabets standard or KRYPTOS, "
        "Beaufort or not); a period is live if no slot holds two different forced key letters. Exact. Ten scrambled "
        "coppers (seed 133, as 0134); statistic fixed before the run: cells (order, period) where K4's live count is above "
        "every copper's, against the same count for each copper against the rest."
    ),
    "hypothesis_eli5": (
        "Sanborn described writing the message in rows and copying it out down the columns, sometimes two or three times, "
        "before using the table. We already tried every way of doing that three times with rows up to 24 letters wide. "
        "Here we try every three-step combination where at least one of the grids is wider, 25 to 96 letters, which "
        "gives about 95 million different scrambles. After each one, a repeating secret word of 1 to 26 letters on the "
        "sculpture's tables either has to fit the 24 known letters or it does not, and we compare how often that "
        "happens with scrambled copies of the carved text."
    ),
    "prediction": (
        "As in 0134 and 0083: no key shorter than 20 fits K4 after any route in either order beyond what the coppers "
        "show, and K4 is above every copper in no more cells than the most any copper manages against the rest. A K4 "
        "count outside that null stops the queue for a replication. Zero candidates."
    ),
    "method": (
        "1. Build the where-map of one stage for every width 2-96 and reading. "
        "2. Compile the C counter; check it against a Python reference on 25 random routes (every order, period, class "
        "and text). "
        "3. For each first stage (reading, width), compose every second and third stage with at least one width >= 25, "
        "skip all-clockwise, forward and inverse; skip permutations already seen within that first stage. "
        "4. For each route, class and text: the forced key letter at each known letter's slot; period p live if no slot "
        "holds two different letters; count per (order, period, text); list K4's settings live below 20. "
        "5. Compare K4 with the ten coppers cell by cell."
    ),
    "walkthrough": (
        "1. Write the 97 letters in rows of 30: three full rows and a row of 7. "
        "2. Read the columns left first, top to bottom (Sanborn's matrix). "
        "3. Write the result in rows of 9 and read the columns right first, bottom up. "
        "4. Write that in rows of 41 and read the columns left first, bottom up (a quarter turn). "
        "5. Note where each of the 24 known letters has landed and the carved letter there. "
        "6. With a repeating key of length p on the table, two known letters whose landing places differ by a multiple of p use the same key letter, so they must force the same one. "
        "7. Do this for every reading and width of the three grids, the key before or after, and on scrambled copies."
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
PMAX = 26
READINGS = ("cw", "ccw", "col", "colr")
WMAX = 96
W_DONE = 24
N_CONTROLS = 10
WORKERS = 8
EX_CAP = 200

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

// hash set for one first stage
static uint64_t *HS; static size_t HCAP;
static int hs_add(uint64_t h) {
    if (!h) h = 1;
    size_t i = h & (HCAP - 1);
    while (HS[i]) { if (HS[i] == h) return 0; i = (i + 1) & (HCAP - 1); }
    HS[i] = h; return 1;
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

// one first stage (r1, w1 index); returns counts through the output arrays
void run_first(int r1, int i1, int w3min_all, long *live, long *low, long *k4low, int *ex, int *nex, int ex_cap,
               long *n_routes, long *n_dupes) {
    HCAP = 1 << 22; HS = calloc(HCAP, sizeof(uint64_t));
    int m[N], c[N], inv[N];
    const int *a = WH[i1][r1];
    for (int r2 = 0; r2 < NR; r2++) for (int i2 = 0; i2 < NW; i2++) {
        const int *b = WH[i2][r2];
        for (int i = 0; i < N; i++) m[i] = b[a[i]];
        for (int r3 = 0; r3 < NR; r3++) {
            if (r1 == 0 && r2 == 0 && r3 == 0) continue;           // all-cw triples: 0083
            for (int i3 = 0; i3 < NW; i3++) {
                int w1 = i1 + 2, w2 = i2 + 2, w3 = i3 + 2;
                if (w1 <= w3min_all && w2 <= w3min_all && w3 <= w3min_all) continue;   // all <= 24: 0134
                const int *cc = WH[i3][r3];
                for (int i = 0; i < N; i++) c[i] = cc[m[i]];
                for (int i = 0; i < N; i++) inv[c[i]] = i;
                for (int d = 0; d < 2; d++) {
                    const int *wh = d ? inv : c;
                    uint64_t h = 1469598103934665603ull;
                    for (int i = 0; i < N; i++) { h ^= (uint64_t)wh[i]; h *= 1099511628211ull; }
                    if (!hs_add(h)) { (*n_dupes)++; continue; }
                    (*n_routes)++;
                    test_route(wh, live, low, k4low, ex, nex, ex_cap, r1, w1, r2, w2, r3, w3, d);
                }
            }
        }
    }
    free(HS);
}

// verification: live counts for a single route (r, width index pairs), all texts
void one_route(int r1, int i1, int r2, int i2, int r3, int i3, int dir, long *live, long *low) {
    int m[N], c[N], inv[N]; long k4low = 0; int ex[11], nex = 0;
    const int *a = WH[i1][r1], *b = WH[i2][r2], *cc = WH[i3][r3];
    for (int i = 0; i < N; i++) m[i] = b[a[i]];
    for (int i = 0; i < N; i++) c[i] = cc[m[i]];
    for (int i = 0; i < N; i++) inv[c[i]] = i;
    test_route(dir ? inv : c, live, low, &k4low, ex, &nex, 0, r1, i1 + 2, r2, i2 + 2, r3, i3 + 2, dir);
}
"""


def stage(tokens, w, r):
    """Write tokens in rows of w (last row short), read the columns: cw = left first, bottom up; ccw = right first,
    top down; col = left first, top down; colr = right first, bottom up (0134's definition)."""
    rows = [tokens[i:i + w] for i in range(0, len(tokens), w)]
    cols = range(w) if r in ("cw", "col") else range(w - 1, -1, -1)
    up = r in ("cw", "colr")
    out = []
    for c in cols:
        rr = reversed(rows) if up else rows
        out.extend(row[c] for row in rr if c < len(row))
    return out


def where_of(w, r):
    sigma = stage(list(range(N)), w, r)
    wh = [0] * N
    for j, i in enumerate(sigma):
        wh[i] = j
    return wh


def build(texts, known_list):
    d = tempfile.mkdtemp(prefix="k4_f63b_")
    src, so = os.path.join(d, "tri.c"), os.path.join(d, "tri.so")
    open(src, "w").write(C_SOURCE)
    subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", so, src], check=True, capture_output=True)
    lib = ctypes.CDLL(so)
    wh = []
    for w in range(2, WMAX + 1):
        for r in READINGS:
            wh += where_of(w, r)
    ci = []
    for A in (STD, KRY):
        for t in texts:
            ci += [A.index(ch) for ch in t]
    pi = [STD.index(a) for _, a in known_list] + [KRY.index(a) for _, a in known_list]
    pidx = [q - 1 for q, _ in known_list]
    I = lambda v: (ctypes.c_int * len(v))(*v)
    lib.set_tables(I(wh), len(texts), I(ci), I(pi), I(pidx))
    return lib


def reference(route, d, texts, known_list):
    """Python count of live periods for one route: {(order, text): [count by period 0..26]}."""
    (r1, w1), (r2, w2), (r3, w3) = route
    a, b, c = where_of(w1, r1), where_of(w2, r2), where_of(w3, r3)
    wh = [c[b[a[i]]] for i in range(N)]
    if d:
        inv = [0] * N
        for i, j in enumerate(wh):
            inv[j] = i
        wh = inv
    kp = [q for q, _ in known_list]
    land = [wh[q - 1] for q in kp]
    out = {}
    for o in (0, 1):
        for t, txt in enumerate(texts):
            cnt = [0] * (PMAX + 1)
            for pa in (STD, KRY):
                for ca in (STD, KRY):
                    for beau in (0, 1):
                        f = [((ca.index(txt[j]) + pa.index(a)) if beau else (ca.index(txt[j]) - pa.index(a))) % 26
                             for j, (_, a) in zip(land, known_list)]
                        for p in range(1, PMAX + 1):
                            slots, ok = {}, True
                            for e in range(24):
                                s_ = (land[e] if o == 0 else kp[e] - 1) % p
                                if slots.setdefault(s_, f[e]) != f[e]:
                                    ok = False
                                    break
                            cnt[p] += ok
            out[(o, t)] = cnt
    return out


def _worker(args):
    firsts, texts, known_list, deadline = args
    lib = build(texts, known_list)
    T = len(texts)
    live = (ctypes.c_long * (2 * T * (PMAX + 1)))()
    low = (ctypes.c_long * (2 * T))()
    k4l = (ctypes.c_long * 1)()
    ex = (ctypes.c_int * (11 * EX_CAP))()
    nex = ctypes.c_int(0)
    nr, nd = ctypes.c_long(0), ctypes.c_long(0)
    done = []
    for r1, w1 in firsts:
        if time.time() > deadline:
            break
        lib.run_first(READINGS.index(r1), w1 - 2, W_DONE, live, low, k4l, ex, ctypes.byref(nex), EX_CAP,
                      ctypes.byref(nr), ctypes.byref(nd))
        done.append((r1, w1))
    return {"live": list(live), "low": list(low), "k4low": k4l[0], "ex": list(ex)[:11 * nex.value],
            "n_routes": nr.value, "n_dupes": nd.value, "done": done}


def run(ctx):
    import multiprocessing as mp
    import sys
    import types
    ct, known = ctx.K4, ctx.KNOWN
    known_list = [(q, known[q]) for q in sorted(known)]
    rng = random.Random(133)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    T = len(texts)
    # check the compiled counter against Python on random routes
    lib = build(texts, known_list)
    vr = random.Random(1393)
    for _ in range(25):
        route = [(vr.choice(READINGS), vr.randrange(2, WMAX + 1)) for _ in range(3)]
        d = vr.randrange(2)
        live = (ctypes.c_long * (2 * T * (PMAX + 1)))(); low = (ctypes.c_long * (2 * T))()
        lib.one_route(*[v for (r, w) in route for v in (READINGS.index(r), w - 2)], d, live, low)
        ref = reference(route, d, texts, known_list)
        for (o, t), cnt in ref.items():
            assert [live[(o * T + t) * (PMAX + 1) + p] for p in range(1, PMAX + 1)] == cnt[1:], (route, d, o, t)
    # the stage composition must equal running the stages in sequence
    pt = [chr(65 + vr.randrange(26)) for _ in range(N)]
    st = [(30, "col"), (9, "colr"), (41, "cw")]
    a, b, c = (where_of(w, r) for w, r in st)
    moved = [""] * N
    for i in range(N):
        moved[c[b[a[i]]]] = pt[i]
    assert stage(stage(stage(pt, 30, "col"), 9, "colr"), 41, "cw") == moved
    firsts = [(r, w) for w in range(2, WMAX + 1) for r in READINGS]
    rng.shuffle(firsts)
    deadline = time.time() + ctx.time_left() - 90
    shares = [(firsts[i::WORKERS], texts, known_list, deadline) for i in range(WORKERS)]
    if getattr(sys.modules.get(__name__), "_worker", None) is not _worker:
        m = types.ModuleType(__name__); m.__dict__.update(globals()); sys.modules[__name__] = m
    with mp.get_context("fork").Pool(WORKERS) as pool:
        parts = pool.map(_worker, shares, chunksize=1)
    live = [[[sum(pt_["live"][(o * T + t) * (PMAX + 1) + p] for pt_ in parts) for p in range(PMAX + 1)] for t in range(T)] for o in (0, 1)]
    low = [[sum(pt_["low"][o * T + t] for pt_ in parts) for t in range(T)] for o in (0, 1)]
    n_routes = sum(pt_["n_routes"] for pt_ in parts)
    done = [f for pt_ in parts for f in pt_["done"]]
    ex = []
    for pt_ in parts:
        e = pt_["ex"]
        for j in range(0, len(e), 11):
            x = e[j:j + 11]
            cls = x[8]
            ex.append({"route": [READINGS[x[0]], x[1], READINGS[x[2]], x[3], READINGS[x[4]], x[5]], "dir": "inv" if x[6] else "fwd",
                       "order": "AB"[x[7]], "class": f"{('std', 'kry')[cls >> 2]}/{('std', 'kry')[(cls >> 1) & 1]}/{'beau' if cls & 1 else 'vig-var'}",
                       "period": x[9]})
    cells = [(o, p) for o in (0, 1) for p in range(1, PMAX + 1)]

    def above_rest(t):
        return [("AB"[o], p) for o, p in cells if live[o][t][p] > max(live[o][u][p] for u in range(T) if u != t)]
    k4_above = above_rest(0)
    null_above = [len(above_rest(t)) for t in range(1, T)]
    stop = len(k4_above) > max(null_above)
    first_live = {"AB"[o]: next((p for p in range(1, PMAX + 1) if live[o][0][p]), None) for o in (0, 1)}
    cop_first = {"AB"[o]: min((next((p for p in range(1, PMAX + 1) if live[o][t][p]), 99) for t in range(1, T))) for o in (0, 1)}
    bounds = {
        "family": "three matrix stages (rows of w, columns read in one of four ways), at least one width 25-96, then or before a periodic tableau key",
        "readings": {"cw": "left column first, bottom up", "ccw": "right first, top down", "col": "left first, top down", "colr": "right first, bottom up"},
        "triples": "63 reading triples (all-cw skipped, 0083) x width triples in 2-96 with max >= 25 (all <= 24 was 0134), forward and inverse",
        "first_stages_done": len(done), "first_stages_total": len(firsts),
        "distinct_routes": n_routes, "duplicates_skipped_within_first_stage": sum(pt_["n_dupes"] for pt_ in parts),
        "periods": [1, PMAX], "classes": 8, "c_counter_checked_against_python": "25 random routes x 2 orders x 11 texts, all equal",
        "k4_live_by_period": {"AB"[o]: live[o][0][1:] for o in (0, 1)},
        "controls_live_by_period_min": {"AB"[o]: [min(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in (0, 1)},
        "controls_live_by_period_max": {"AB"[o]: [max(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in (0, 1)},
        "k4_shortest_live": first_live, "coppers_shortest_live": cop_first,
        "k4_settings_live_below_20": {"AB"[o]: low[o][0] for o in (0, 1)}, "controls_settings_live_below_20": {"AB"[o]: low[o][1:] for o in (0, 1)},
        "k4_live_below_20": sorted(ex, key=lambda x: x["period"])[:40],
        "cells_k4_above_every_copper": k4_above, "null_cells_above_rest_per_copper": null_above, "stop_queue": stop,
        "controls": f"{N_CONTROLS} shuffled coppers (seed 133, as 0134), identical search",
        "order_A": "stages, then key (slot = landing place mod p)", "order_B": "key, then stages (slot = message place mod p)",
    }
    notes = (f"{n_routes:,} distinct routes ({len(done)} of {len(firsts)} first stages) x 8 classes x 2 orders, periods 1-26. "
             f"Shortest live key on K4: A {first_live['A']}, B {first_live['B']}; coppers A {cop_first['A']}, B {cop_first['B']}. "
             f"K4 settings live below 20: A {low[0][0]}, B {low[1][0]}. K4 above every copper in {len(k4_above)} of 52 cells; "
             f"null {min(null_above)}-{max(null_above)}. Stop queue: {stop}.")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    """key: {'stages': [(w, reading), ...], 'order': 'A' (stages then table) or 'B', 'alphabet': 'STD' or 'KRY',
    'key': list of shifts}; Vigenere on one alphabet."""
    alpha = KRY if key["alphabet"] == "KRY" else STD
    k = key["key"]

    def table(s):
        return "".join(alpha[(alpha.index(ch) + k[i % len(k)]) % 26] for i, ch in enumerate(s))

    def move(s):
        s = list(s)
        for w, r in key["stages"]:
            s = stage(s, w, r)
        return "".join(s)
    return table(move(plaintext)) if key["order"] == "A" else move(table(plaintext))


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    st = [(30, "col"), (9, "colr"), (41, "cw")]
    W = [where_of(w, r) for w, r in st]
    lines = ["three matrix stages: rows of 30 read down the columns, left first; rows of 9 read up, right first; rows of 41 read up, left first",
             "", "place  letter  after 1  after 2  after 3  copper there"]
    for qq in (22, 23, 24, 64, 65, 74):
        a = W[0][qq - 1]; b = W[1][a]; c = W[2][b]
        lines.append(f"{qq:5d}  {known[qq]:>6}  {a + 1:7d}  {b + 1:7d}  {c + 1:7d}  {ct[c]:>12}")
    lines += ["", "with a key of length p on the table, known letters whose final places differ by a multiple of p share a key letter"]
    return "\n".join(lines)
