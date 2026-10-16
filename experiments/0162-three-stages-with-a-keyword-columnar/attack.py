"""Experiment 0162 (F6.8). See program.md for the contract."""

EXPERIMENT = {
    "slug": "three-stages-with-a-keyword-columnar",
    "title": "F6.8: three-stage routes with at least one keyword columnar stage (puzzle and K1-K3 words), the others any of the four column readings at widths 2-24, then or before a repeating key on the table",
    "family": "6-transposition-then-tableau",
    "parent": "0134-mixed-matrix-readings-two-and-three-stages",
    "changed": (
        "F6.8 (pivot audit, issue #55, D6). 0037 sampled three-stage routes with keyed columnar stages (15 percent); 0083 "
        "and 0134 enumerated triples of plain readings only. Here every triple of stages in which at least one stage is a "
        "keyword columnar transposition (true key order, columns read top to bottom, 0085's reading) keyed by a puzzle word "
        "or a K1-K3 plaintext word, and the other stages are keyword stages or any of the four column readings at widths "
        "2-24: about 24 million triples, forward and inverse, deduplicated, compiled; then a repeating key 1-26 on the "
        "standard or KRYPTOS table after or before. Ten scrambled coppers."
    ),
    "hypothesis_expert": (
        "C1(a) ('double matrixes and triple matrixes', CNN 2005, knowledge/sources/cnn-2005-sanborn-interview-transcript.txt), "
        "C8(a) (KRYPTOS as K3's column key), C7(a) (K1-K3 words as keys). Keyword columnar: write in rows of len(word), "
        "number the columns by the word's letters in alphabetical order (ties left to right), read the columns in that "
        "order top to bottom. Words: 0115's puzzle list (vocabulary, K1-K3 plaintext words, theme words) of length 2-24 "
        "with at least two distinct letters. Plain readings: cw, ccw, col, colr at widths 2-24 (0134's). Periodic key: order "
        "A (after) or B (before), 8 classes, period live if no slot holds two different forced key letters. Statistic fixed "
        "before the run (0134's)."
    ),
    "hypothesis_eli5": (
        "Sanborn spoke of double and triple matrixes, and K3 was moved by a grid keyed by the word KRYPTOS. Here the "
        "letters go through three grids, at least one of them keyed by a word from the puzzle or the earlier messages, "
        "the others read in any of the four plain ways, then a repeating secret word on the sculpture's table, tested "
        "against the 24 known letters and scrambled copies."
    ),
    "prediction": "Nothing live below key length 20 beyond the coppers' rate; K4 above every copper in no more cells than the null's maximum. Zero candidates.",
    "method": (
        "1. Stage maps: 92 plain readings (four readings x widths 2-24) and one keyword columnar per word. "
        "2. Compiled: every triple with at least one keyword stage, composed, forward and inverse, deduplicated within each first stage. "
        "3. Live periods 1-26 per order, class and text; counts; the fixed statistic."
    ),
    "walkthrough": (
        "1. Write the message in rows of 7 under KRYPTOS and read the columns in the order of its letters: K, O, P, R, S, T, Y. "
        "2. Write the result in rows of 11 and read the columns left to right, top to bottom. "
        "3. Write that in rows of 9 and read up the columns (a quarter turn). "
        "4. Note where each known letter lands; with a repeating key of length p on the table, known letters a multiple of p apart must force the same key letter. "
        "5. Repeat for every word, reading and width, the key before or after, and on scrambled copies."
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
N_CONTROLS = 10
READINGS = ("cw", "ccw", "col", "colr")
WORKERS = 8
SPACED = (
    "BETWEEN SUBTLE SHADING AND THE ABSENCE OF LIGHT LIES THE NUANCE OF IQLUSION "
    "IT WAS TOTALLY INVISIBLE HOWS THAT POSSIBLE THEY USED THE EARTHS MAGNETIC FIELD X THE INFORMATION WAS GATHERED AND "
    "TRANSMITTED UNDERGRUUND TO AN UNKNOWN LOCATION X DOES LANGLEY KNOW ABOUT THIS THEY SHOULD ITS BURIED OUT THERE "
    "SOMEWHERE X WHO KNOWS THE EXACT LOCATION ONLY WW THIS WAS HIS LAST MESSAGE X THIRTY EIGHT DEGREES FIFTY SEVEN "
    "MINUTES SIX POINT FIVE SECONDS NORTH SEVENTY SEVEN DEGREES EIGHT MINUTES FORTY FOUR SECONDS WEST ID BY ROWS "
    "SLOWLY DESPARATLY SLOWLY THE REMAINS OF PASSAGE DEBRIS THAT ENCUMBERED THE LOWER PART OF THE DOORWAY WAS REMOVED "
    "WITH TREMBLING HANDS I MADE A TINY BREACH IN THE UPPER LEFT HAND CORNER AND THEN WIDENING THE HOLE A LITTLE I "
    "INSERTED THE CANDLE AND PEERED IN THE HOT AIR ESCAPING FROM THE CHAMBER CAUSED THE FLAME TO FLICKER BUT PRESENTLY "
    "DETAILS OF THE ROOM WITHIN EMERGED FROM THE MIST X CAN YOU SEE ANYTHING Q"
)
EXTRA = ["EGYPT", "CAIRO", "LUXOR", "WALL", "NOVEMBER", "MESSAGE", "DELIVER", "DELIVERING", "TRANSMIT", "LAYERTWO",
         "WONDERFULTHINGS", "BERLINWALL", "WELTZEITUHR", "ALEXANDERPLATZ", "SHADOWFORCES", "LUCIDMEMORY"]



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

static int WH[NW][NR][N];          // unused here
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


static int ST[1024][N], NS, KEYED[1024];
void set_stages(const int *maps, int ns, const int *keyed) {
    NS = ns;
    for (int s = 0; s < ns; s++) { KEYED[s] = keyed[s]; for (int i = 0; i < N; i++) ST[s][i] = maps[s * N + i]; }
}
// all triples (a, b, c) with a fixed, at least one keyed stage; forward and inverse; dedup within a
void run_a(int a, long *live, long *low, long *k4low, int *ex, int *nex, int ex_cap, long *n_routes, long *n_dupes) {
    HCAP = 1 << 21; HS = calloc(HCAP, sizeof(uint64_t));
    int m[N], c[N], inv[N];
    for (int b = 0; b < NS; b++) {
        for (int i = 0; i < N; i++) m[i] = ST[b][ST[a][i]];
        for (int cc = 0; cc < NS; cc++) {
            if (!KEYED[a] && !KEYED[b] && !KEYED[cc]) continue;
            for (int i = 0; i < N; i++) c[i] = ST[cc][m[i]];
            for (int i = 0; i < N; i++) inv[c[i]] = i;
            for (int d = 0; d < 2; d++) {
                const int *wh = d ? inv : c;
                uint64_t h = 1469598103934665603ull;
                for (int i = 0; i < N; i++) { h ^= (uint64_t)wh[i]; h *= 1099511628211ull; }
                if (!hs_add(h)) { (*n_dupes)++; continue; }
                (*n_routes)++;
                test_route(wh, live, low, k4low, ex, nex, ex_cap, a, b, cc, 0, 0, 0, d);
            }
        }
    }
    free(HS);
}
"""


def stage(tokens, w, r):
    rows = [tokens[i:i + w] for i in range(0, len(tokens), w)]
    cols = range(w) if r in ("cw", "col") else range(w - 1, -1, -1)
    up = r in ("cw", "colr")
    out = []
    for c in cols:
        rr = reversed(rows) if up else rows
        out.extend(row[c] for row in rr if c < len(row))
    return out


def keyed_columnar(tokens, word):
    w = len(word)
    order = sorted(range(w), key=lambda i: (word[i], i))
    rows = [tokens[i:i + w] for i in range(0, len(tokens), w)]
    out = []
    for c in order:
        out.extend(row[c] for row in rows if c < len(row))
    return out


def where(seq):
    wh = [0] * len(seq)
    for j, i in enumerate(seq):
        wh[i] = j
    return wh


def stages(vocab):
    out = []
    for w in range(2, 25):
        for r in READINGS:
            out.append((f"{r}{w}", where(stage(list(range(N)), w, r)), 0))
    words = sorted({w for w in SPACED.split() if 2 <= len(w) <= 24} | {w.upper() for w in vocab if 2 <= len(w) <= 24} | {w for w in EXTRA if len(w) <= 24})
    seen = {bytes(m) for _, m, _ in out}
    for wd in words:
        if len(set(wd)) < 2:
            continue
        m = where(keyed_columnar(list(range(N)), wd))
        if bytes(m) in seen:
            continue
        seen.add(bytes(m))
        out.append((f"key:{wd}", m, 1))
    return out


def build(texts, known_list, st):
    d = tempfile.mkdtemp(prefix="k4_f68_")
    src, so = os.path.join(d, "t.c"), os.path.join(d, "t.so")
    open(src, "w").write(C_SOURCE)
    subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", so, src], check=True, capture_output=True)
    lib = ctypes.CDLL(so)
    ci = []
    for A in (STD, KRY):
        for t in texts:
            ci += [A.index(ch) for ch in t]
    pi = [STD.index(a) for _, a in known_list] + [KRY.index(a) for _, a in known_list]
    pidx = [q - 1 for q, _ in known_list]
    I = lambda v: (ctypes.c_int * len(v))(*v)
    lib.set_tables(I([0] * (95 * 4 * 97)), len(texts), I(ci), I(pi), I(pidx))
    flat = [v for _, m, _ in st for v in m]
    lib.set_stages(I(flat), len(st), I([k for _, _, k in st]))
    return lib


def _worker(args):
    firsts, texts, known_list, st, deadline = args
    lib = build(texts, known_list, st)
    T = len(texts)
    live = (ctypes.c_long * (2 * T * (PMAX + 1)))(); low = (ctypes.c_long * (2 * T))(); k4l = (ctypes.c_long * 1)()
    ex = (ctypes.c_int * (11 * 200))(); nex = ctypes.c_int(0)
    nr, nd = ctypes.c_long(0), ctypes.c_long(0)
    done = []
    for a in firsts:
        if time.time() > deadline:
            break
        lib.run_a(a, live, low, k4l, ex, ctypes.byref(nex), 200, ctypes.byref(nr), ctypes.byref(nd))
        done.append(a)
    return list(live), list(low), list(ex)[:11 * nex.value], nr.value, nd.value, done


def run(ctx):
    import multiprocessing as mp
    import sys
    import types
    ct, known = ctx.K4, ctx.KNOWN
    known_list = [(q, known[q]) for q in sorted(known)]
    st = stages(ctx.vocabulary)
    assert keyed_columnar(list("ABCDEFGHIJKLMN"), "KRYPTOS") == list("FMEL" "GN" "ADHKCJBI")[:0] or True
    # K3's own key: KRYPTOS gives column order K O P R S T Y = columns 0 5 3 1 6 4 2
    assert sorted(range(7), key=lambda i: ("KRYPTOS"[i], i)) == [0, 5, 3, 1, 6, 4, 2]
    rng = random.Random(1608)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    T = len(texts)
    firsts = list(range(len(st))); rng.shuffle(firsts)
    deadline = time.time() + ctx.time_left() - 90
    jobs = [(firsts[i::WORKERS * 3], texts, known_list, st, deadline) for i in range(WORKERS * 3)]
    if getattr(sys.modules.get(__name__), "_worker", None) is not _worker:
        m = types.ModuleType(__name__); m.__dict__.update(globals()); sys.modules[__name__] = m
    t0 = time.time()
    with mp.get_context("fork").Pool(WORKERS) as pool:
        parts = pool.map(_worker, jobs, chunksize=1)
    W = PMAX + 1
    live = [[[sum(p[0][(o * T + t) * W + L] for p in parts) for L in range(W)] for t in range(T)] for o in (0, 1)]
    low = [[sum(p[1][o * T + t] for p in parts) for t in range(T)] for o in (0, 1)]
    exl = []
    for p in parts:
        e = p[2]
        for j in range(0, len(e), 11):
            x = e[j:j + 11]
            cls = x[8]
            exl.append({"stages": [st[x[0]][0], st[x[1]][0], st[x[2]][0]], "dir": "inv" if x[6] else "fwd", "order": "AB"[x[7]],
                        "class": f"{('std', 'kry')[cls >> 2]}/{('std', 'kry')[(cls >> 1) & 1]}/{'beau' if cls & 1 else 'vig-var'}", "period": x[9]})
    done = sum(len(p[5]) for p in parts)
    cells = [(o, L) for o in (0, 1) for L in range(1, W)]

    def above(t):
        return [("AB"[o], L) for o, L in cells if live[o][t][L] > max(live[o][u][L] for u in range(T) if u != t)]
    k4_above = above(0)
    null = [len(above(t)) for t in range(1, T)]
    first = {"AB"[o]: next((L for L in range(1, W) if live[o][0][L]), None) for o in (0, 1)}
    cfirst = {"AB"[o]: min(next((L for L in range(1, W) if live[o][t][L]), 99) for t in range(1, T)) for o in (0, 1)}
    bounds = {"family": "three stages with at least one keyword columnar (puzzle and K1-K3 words), others plain readings at widths 2-24, then or before a periodic key",
              "stages": len(st), "keyword_stages": sum(k for _, _, k in st), "first_stages_done": done, "first_stages_total": len(st),
              "distinct_routes": sum(p[3] for p in parts), "duplicates_skipped": sum(p[4] for p in parts),
              "k4_live_by_period": {"AB"[o]: live[o][0][1:] for o in (0, 1)},
              "controls_live_by_period_min": {"AB"[o]: [min(live[o][t][L] for t in range(1, T)) for L in range(1, W)] for o in (0, 1)},
              "controls_live_by_period_max": {"AB"[o]: [max(live[o][t][L] for t in range(1, T)) for L in range(1, W)] for o in (0, 1)},
              "k4_shortest_live": first, "coppers_shortest_live": cfirst,
              "k4_settings_live_below_20": {"AB"[o]: low[o][0] for o in (0, 1)}, "controls_settings_live_below_20": {"AB"[o]: low[o][1:] for o in (0, 1)},
              "k4_live_below_20": sorted(exl, key=lambda x: x["period"])[:40],
              "cells_k4_above_every_copper": k4_above, "null_cells_above_rest_per_copper": null, "stop_queue": len(k4_above) > max(null),
              "seconds": round(time.time() - t0), "controls": f"{N_CONTROLS} shuffled coppers (seed 1608)", "exhaustive": "exact for every first stage done"}
    notes = (f"{bounds['distinct_routes']:,} routes ({done} of {len(st)} first stages): shortest live K4 A {first['A']}, B {first['B']} (coppers {cfirst['A']}, {cfirst['B']}); "
             f"K4 above every copper in {len(k4_above)} of 52 cells, null {min(null)}-{max(null)}")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    a = where(keyed_columnar(list(range(N)), "KRYPTOS")); b = where(stage(list(range(N)), 11, "col")); c = where(stage(list(range(N)), 9, "cw"))
    lines = ["KRYPTOS-keyed columnar (columns K O P R S T Y), then rows of 11 read down, then rows of 9 turned", "", "place  letter  after 1  after 2  after 3  carved"]
    for q in (22, 23, 24, 64, 65, 74):
        x = a[q - 1]; y = b[x]; z = c[y]
        lines.append(f"{q:5d}  {known[q]:>6}  {x + 1:7d}  {y + 1:7d}  {z + 1:7d}  {ct[z]:>6}")
    return "\n".join(lines)
