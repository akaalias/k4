"""Experiment 0166 (F6.12, F6.13, F6.15). See program.md for the contract."""

EXPERIMENT = {
    "slug": "eva-chiffre-xiii-yar",
    "title": "F6.12, F6.13, F6.15: the Czech EVA double triangle and Chiffre XIII's five-row mask with its period-5 table, and the YAR '1-2-3' orderings, then the table",
    "family": "6-transposition-then-tableau",
    "parent": "0164-disrupted-triangle-interrupted-trapezoid",
    "changed": (
        "Three items, one run, a verdict each. F6.12 EVA (Czech exile, WWII, type TT): the text written into a triangle "
        "growing by two cells a row (ten rows under 19 columns for 97 letters, three cells empty), copied out by the "
        "19-letter key's numbering, written into a second such triangle and copied out again under the same numbering; "
        "keys: 19-letter windows of the K1-K3 plaintexts, 19-letter dictionary words, pairs of puzzle words totalling 19; "
        "then a repeating key 1-26 on the standard or KRYPTOS table. F6.13 Chiffre XIII (type TS): five rows as wide as "
        "the key (24-31 letters: K1-K3 windows and puzzle phrases), rows 1, 3, 5 full, row 2 left-aligned and row 4 at "
        "every cyclic shift, their lengths every split of what is left of 97, columns read in key order; then the "
        "published substitution: plain A-Z over one unknown mixed alphabet, rows shifted by one and used in turn "
        "(position mod 5), either shift direction, decided exactly (the unknown alphabet's cells are forced one by one). "
        "F6.15: Sanborn's reported '1-2-3' spacing of the raised YAR as orderings: letters taken by counting 1, 2, 3 places "
        "in turn around the remaining text (every order of 1, 2, 3), and the same with 4, 5, 7 (Y, A, R's places in "
        "ENDYAHR), then the table. Ten scrambled coppers."
    ),
    "hypothesis_expert": (
        "C1(a) ('double matrixes'), C22(d) (YAR's '1-2-3' spacing, clue register), C5; sources: foreign_agent_hand_systems.md "
        "section 4 (scz.bplaced.net §10.1: EVA, Chiffre XIII; the XIII substitution checked there on the published "
        "example), reports/Scheidt patents and field ciphers.md. Where the sources leave a rule open (XIII's partial-row "
        "lengths and row 4's shift; EVA's blank cells) every choice is enumerated; this is stated as a parametric family, "
        "not the documented one. Periodic-key items: orders A and B, 8 classes, 0134's statistic. XIII: a route is "
        "consistent if the forced cells M[(p + r) mod 26] = c (or p - r) are one-to-one; statistic: consistent routes with "
        "at least 4 checks, K4 against the coppers' range."
    ),
    "hypothesis_eli5": (
        "Two ciphers of the Czech exiles in London: EVA wrote the message into a triangle twice over, and Chiffre XIII "
        "wrote it into five rows of a keyword's width, two of them short, then enciphered it with five shifted rows of one "
        "scrambled alphabet used in turn. Both are hand ciphers keyed by a sentence. And a third idea: Sanborn's raised "
        "letters YAR, reportedly spaced '1-2-3', as a way of counting off letters. Each is tested against the 24 known "
        "letters and scrambled copies."
    ),
    "prediction": "EVA and YAR: nothing below key length 20 beyond the coppers' rate. XIII: consistent routes at the coppers' rate. Zero candidates.",
    "method": (
        "1. Keys: K1-K3 windows of 19 and 24-31 letters, 19-letter dictionary words, puzzle-word pairs. "
        "2. EVA and YAR routes through the compiled periodic-key test (orders A, B, 8 classes). "
        "3. XIII: each mask route; the 24 forced cells of the unknown alphabet checked for one-to-one, both shift directions; counts by checks. "
        "4. K4 against the coppers per item."
    ),
    "walkthrough": (
        "1. EVA: write the 97 letters into rows of 1, 3, 5, ... cells, centred under 19 columns; copy out by the key's numbering; write into a second triangle; copy out again. "
        "2. XIII: write into five rows of the key's width, rows 2 and 4 short (row 4 shifted), copy out by the key's numbering; then encipher letter 1 with row 1 of the shifted alphabet, letter 2 with row 2, ..., letter 6 with row 1 again. "
        "3. Each known letter then forces one cell of the unknown alphabet; two known letters forcing different letters into one cell, or one letter into two cells, rule the setting out. "
        "4. YAR: count 1, 2, 3, 1, 2, 3 around the text, taking each letter counted to, until all are taken. "
        "5. Repeat for every key and choice, and on scrambled copies."
    ),
}

import ctypes
import random
import time
from pathlib import Path
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
N_CONTROLS = 10
WORKERS = 8
ROOT = Path(__file__).resolve().parent
if not (ROOT / "kryptos").exists():
    ROOT = Path.cwd()
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



def numeric_order(word):
    """Column reading order: columns sorted by (letter, position)."""
    return sorted(range(len(word)), key=lambda i: (word[i], i))


def read_cells(cells, order_cols, w):
    """cells: list of (row, col) in writing order (message place = index). Read columns in order_cols, top to bottom."""
    by_col = {}
    for idx, (r, c) in enumerate(cells):
        by_col.setdefault(c, []).append((r, idx))
    seq = []
    for c in order_cols:
        seq.extend(idx for r, idx in sorted(by_col.get(c, [])))
    return seq


def disrupted(word, n=97):
    """Rijmenants's keyword-disrupted columnar: triangles start at the column of key number 1, 2, ... in successive
    row blocks; each triangle row starts one column further right; non-triangle cells are filled first, then the
    triangle cells, row by row; columns read in key order."""
    w = len(word)
    order = numeric_order(word)
    h = -(-n // w)
    while True:
        tri = set()
        r = 0
        k = 0
        while r < h:
            start = order[k % w]
            t = 0
            while r < h and start + t < w:
                for c in range(start + t, w):
                    tri.add((r, c))
                r += 1
                t += 1
            k += 1
        cells_all = [(r, c) for r in range(h) for c in range(w)]
        first = [x for x in cells_all if x not in tri]
        second = [x for x in cells_all if x in tri]
        if len(first) + len(second) >= n:
            break
        h += 1
    cells = (first + second)[:n]
    return read_cells(cells, order, w)


def triangle(key19, n=97, blanks="end"):
    """TM 32-220 par. 87 triangle: n rows growing by two cells (row r: 2r+1 cells, centred under 2n-1 columns);
    keyword extended by repetition to 2n-1 and numbered; fill rows; read columns in key order."""
    rows = 1
    while rows * rows < n:
        rows += 1
    d = 2 * rows - 1
    cells = []
    for r in range(rows):
        for c in range(rows - 1 - r, rows + r):
            cells.append((r, c))
    if blanks == "end":
        cells = cells[:n]
    else:
        cells = cells[len(cells) - n:]
    key = (key19 * d)[:d]
    return read_cells(cells, numeric_order(key), d)


def interrupted(word, lengths, n=97):
    """Interrupted-key columnar (TM 89c-e): rows of width len(word) filled only to the given lengths (cycled), columns read in key order."""
    w = len(word)
    cells = []
    r = 0
    j = 0
    while len(cells) < n:
        L = min(max(lengths[j % len(lengths)], 1), w)
        for c in range(L):
            if len(cells) < n:
                cells.append((r, c))
        r += 1
        j += 1
    return read_cells(cells, numeric_order(word), w)


def trapezoid(word, h, side, n=97):
    """TM 32-220 par. 86: base = len(word) cells at the bottom, height h, rows shrink by one going up (on the right
    if side == 'right', on the left otherwise); fill rows top to bottom; read columns in key order; blank cells at the end."""
    b = len(word)
    cells = []
    for r in range(h):
        length = b - (h - 1 - r)
        cols = range(0, length) if side == "right" else range(b - length, b)
        cells.extend((r, c) for c in cols)
    if len(cells) < n:
        return None
    cells = cells[:n]
    return read_cells(cells, numeric_order(word), b)


def where(seq):
    wh = [0] * len(seq)
    for j, i in enumerate(seq):
        wh[i] = j
    return wh


def frac_digits(d, length=60):
    digs, r = [], 1 % d
    for _ in range(400):
        r *= 10
        dg, r = divmod(r, d)
        if dg:
            digs.append(dg)
        if len(digs) >= length or r == 0:
            break
    return digs or [1]


PUZZLE = set()


def keywords(vocab):
    PUZZLE.update(w for w in SPACED.split() + [v.upper() for v in vocab] + EXTRA if w.isalpha())
    words = [w.strip().upper() for w in (ROOT / "kryptos" / "data" / "words.txt").read_text().split()]
    words += [w for w in SPACED.split()] + [w.upper() for w in vocab] + EXTRA
    by_order = {}
    for w in [x for x in words if x in PUZZLE] + words:
        if w.isalpha() and 4 <= len(w) <= 24:
            by_order.setdefault(tuple(numeric_order(w)), w)
    return sorted(by_order.values(), key=lambda w: (len(w), w))


def eva(key19, n=97):
    s1 = triangle(key19)
    pos = [0] * n
    for j, i in enumerate(s1):
        pos[i] = j
    s2 = triangle(key19)              # second triangle, same shape and numbering, applied to the first output
    out = [s1[j] for j in s2]
    return out


def xiii(key, l2, s4, n=97):
    w = len(key)
    l4 = n - 3 * w - l2
    cells = []
    for c in range(w):
        cells.append((0, c))
    for c in range(l2):
        cells.append((1, c))
    for c in range(w):
        cells.append((2, c))
    for t in range(l4):
        cells.append((3, (s4 + t) % w))
    for c in range(w):
        cells.append((4, c))
    return read_cells(cells, numeric_order(key), w)


def josephus(counts, n=97):
    rest = list(range(n))
    seq, i, k = [], -1, 0
    while rest:
        i = (i + counts[k % len(counts)]) % len(rest)
        seq.append(rest.pop(i))
        i -= 1
        k += 1
    return seq


def k1k3_text():
    import json
    t = ""
    for f, key in (("k1", "plaintext"), ("k2", "plaintext_as_carved"), ("k3", "plaintext")):
        t += json.load(open(f"data/{f}.json"))[key]
    return "".join(ch for ch in t.upper() if ch.isalpha())


def eva_keys(vocab):
    txt = k1k3_text()
    keys = {txt[i:i + 19] for i in range(len(txt) - 18)}
    words = [w.strip().upper() for w in (ROOT / "kryptos" / "data" / "words.txt").read_text().split()]
    keys |= {w for w in words if len(w) == 19 and w.isalpha()}
    puzzle = sorted({w for w in SPACED.split() + [v.upper() for v in vocab] + EXTRA if w.isalpha()})
    keys |= {a + b for a in puzzle for b in puzzle if len(a) + len(b) == 19}
    by = {}
    for k in sorted(keys):
        by.setdefault(tuple(numeric_order((k * 19)[:19])), k)
    return sorted(by.values())


def xiii_keys(vocab):
    txt = k1k3_text()
    keys = set()
    for w in range(24, 32):
        keys |= {txt[i:i + w] for i in range(len(txt) - w + 1)}
    puzzle = sorted({w for w in SPACED.split() + [v.upper() for v in vocab] + EXTRA if w.isalpha()})
    keys |= {a + b for a in puzzle for b in puzzle if 24 <= len(a) + len(b) <= 31}
    by = {}
    for k in sorted(keys):
        by.setdefault(tuple(numeric_order(k)), k)
    return sorted(by.values())


def routes_for(item, words):
    out = []
    if item == "F6.15 YAR":
        import itertools
        for base in ((1, 2, 3), (4, 5, 7)):
            for perm in set(itertools.permutations(base)):
                out.append(("count " + "-".join(map(str, perm)), where(josephus(perm))))
        return out
    for wd in words:
        if item == "F6.12 EVA":
            s_ = eva(wd)
            if len(s_) == N and sorted(s_) == list(range(N)):
                out.append((wd, where(s_)))
    return out


def gen_worker(args):
    item, words, texts, known_list = args
    maps = routes_for(item, words)
    seen, named = set(), []
    for name, m in maps:
        for d, mm in (("fwd", m), ("inv", inverse(m))):
            k = bytes(mm)
            if k not in seen:
                seen.add(k); named.append((f"{name} {d}", mm))
    if not named:
        T = len(texts)
        return [0] * (2 * T * 27), [0] * (2 * T), [], 0
    live, low, ex = rt_worker((named, texts, known_list))
    return live, low, ex, len(named)


def run_item(item, words, texts, known_list, pool):
    T = len(texts)
    chunks = [words[i::WORKERS * 4] for i in range(WORKERS * 4)]
    parts = pool.map(gen_worker, [(item, c, texts, known_list) for c in chunks], chunksize=1)
    live = [[[sum(p[0][(o * T + t) * 27 + L] for p in parts) for L in range(27)] for t in range(T)] for o in (0, 1)]
    low = [[sum(p[1][o * T + t] for p in parts) for t in range(T)] for o in (0, 1)]
    ex = [x for p in parts for x in p[2]]
    n = sum(p[3] for p in parts)
    cells = [(o, L) for o in (0, 1) for L in range(1, 27)]

    def above(t):
        return [("AB"[o], L) for o, L in cells if live[o][t][L] > max(live[o][u][L] for u in range(T) if u != t)]
    k4_above = above(0)
    null = [len(above(t)) for t in range(1, T)]
    first = {"AB"[o]: next((L for L in range(1, 27) if live[o][0][L]), None) for o in (0, 1)}
    cfirst = {"AB"[o]: min(next((L for L in range(1, 27) if live[o][t][L]), 99) for t in range(1, T)) for o in (0, 1)}
    return {"routes": n, "k4_live_by_period": {"AB"[o]: live[o][0][1:] for o in (0, 1)},
            "controls_live_by_period_min": {"AB"[o]: [min(live[o][t][L] for t in range(1, T)) for L in range(1, 27)] for o in (0, 1)},
            "controls_live_by_period_max": {"AB"[o]: [max(live[o][t][L] for t in range(1, T)) for L in range(1, 27)] for o in (0, 1)},
            "k4_shortest_live": first, "coppers_shortest_live": cfirst,
            "k4_settings_live_below_20": {"AB"[o]: low[o][0] for o in (0, 1)}, "controls_settings_live_below_20": {"AB"[o]: low[o][1:] for o in (0, 1)},
            "k4_live_below_20": sorted(ex, key=lambda x: x["period"])[:20],
            "cells_k4_above_every_copper": k4_above, "null_cells_above_rest_per_copper": null, "stop_queue": len(k4_above) > max(null)}


def xiii_worker(args):
    keys, texts, known_list = args
    from kryptos.facts import STANDARD_ALPHABET as STD
    T = len(texts)
    kp = [q - 1 for q, _ in known_list]
    pl = [STD.index(a) for _, a in known_list]
    counts = [[0] * 25 for _ in range(T)]
    top = []
    nroutes = 0
    for key in keys:
        w = len(key)
        R = N - 3 * w
        for l2 in range(1, min(w, R)):
            l4 = R - l2
            if not (1 <= l4 <= w - 1):
                continue
            for s4 in range(w):
                seq = xiii(key, l2, s4)
                wh = where(seq)
                land = [wh[i] for i in kp]
                nroutes += 1
                for t in range(T):
                    cl = [texts[t][j] for j in land]
                    for sg in (1, -1):
                        cell, let = {}, {}
                        ok = True
                        for e in range(24):
                            idx = (pl[e] + sg * (land[e] % 5)) % 26
                            if cell.setdefault(idx, cl[e]) != cl[e] or let.setdefault(cl[e], idx) != idx:
                                ok = False
                                break
                        if ok:
                            ch = 24 - len(cell)
                            counts[t][ch] += 1
                            if t == 0 and ch >= 6:
                                top.append({"key": key, "row2": l2, "row4": l4, "shift4": s4, "sign": sg, "checks": ch})
    return counts, top, nroutes


ITEMS = ("F6.12 EVA", "F6.15 YAR")


def run(ctx):
    import multiprocessing as mp
    import sys
    import types
    ct, known = ctx.K4, ctx.KNOWN
    known_list = [(q, known[q]) for q in sorted(known)]
    ek = eva_keys(ctx.vocabulary)
    xk = xiii_keys(ctx.vocabulary)
    # builders are permutations
    assert sorted(eva(ek[0])) == list(range(N)) and sorted(josephus((1, 2, 3))) == list(range(N))
    assert sorted(xiii(xk[0], 1, 3)) == list(range(N))
    rng = random.Random(1612)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    T = len(texts)
    if getattr(sys.modules.get(__name__), "gen_worker", None) is not gen_worker:
        mod = types.ModuleType(__name__); mod.__dict__.update(globals()); sys.modules[__name__] = mod
    res = {}
    t0 = time.time()
    with mp.get_context("fork").Pool(WORKERS) as pool:
        res["F6.12 EVA"] = run_item("F6.12 EVA", ek, texts, known_list, pool)
        named = dedupe(routes_for("F6.15 YAR", []))
        res["F6.15 YAR"] = rt_run(named, texts, known_list)
        parts = pool.map(xiii_worker, [(xk[i::WORKERS * 4], texts, known_list) for i in range(WORKERS * 4)], chunksize=1)
    counts = [[sum(p[0][t][c] for p in parts) for c in range(25)] for t in range(T)]
    ge = {k: [sum(counts[t][k:]) for t in range(T)] for k in (3, 4, 5, 6)}
    res["F6.13 Chiffre XIII"] = {"routes": sum(p[2] for p in parts), "keys": len(xk),
                                 "consistent_ge": {str(k): {"k4": v[0], "coppers": v[1:]} for k, v in ge.items()},
                                 "k4_top": sorted([x for p in parts for x in p[1]], key=lambda x: -x["checks"])[:20]}
    bounds = {"family": "EVA double triangle and YAR orderings then or before a periodic key; Chiffre XIII five-row masks then its period-5 shifted unknown alphabet",
              "eva_keys": len(ek), "xiii_keys": len(xk), "items": res, "seconds": round(time.time() - t0),
              "controls": f"{N_CONTROLS} shuffled coppers (seed 1612)", "exhaustive": True}
    x4 = res["F6.13 Chiffre XIII"]["consistent_ge"]["4"]
    notes = (f"EVA: {res['F6.12 EVA']['routes']:,} routes, shortest live A {res['F6.12 EVA']['k4_shortest_live']['A']} B {res['F6.12 EVA']['k4_shortest_live']['B']}; "
             f"YAR: {res['F6.15 YAR']['routes']} routes, shortest live A {res['F6.15 YAR']['k4_shortest_live']['A']} B {res['F6.15 YAR']['k4_shortest_live']['B']}; "
             f"XIII: {res['F6.13 Chiffre XIII']['routes']:,} masks, consistent with >=4 checks K4 {x4['k4']} (coppers {min(x4['coppers'])}-{max(x4['coppers'])})")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    seq = triangle("KRYPTOS")
    wh = where(seq)
    lines = ["triangle: ten rows of 1, 3, ..., 19 cells, centred; key KRYPTOS repeated to 19 letters and numbered; columns read in that order", "",
             "first 20 message places read: " + " ".join(str(i + 1) for i in seq[:20]), "", "place  letter  lands at  carved"]
    for q in (22, 23, 24, 64, 65, 74):
        lines.append(f"{q:5d}  {known[q]:>6}  {wh[q - 1] + 1:8d}  {ct[wh[q - 1]]:>6}")
    return "\n".join(lines)
