"""Experiment 0164 (F6.11, F6.16, F6.17). See program.md for the contract."""

EXPERIMENT = {
    "slug": "disrupted-triangle-interrupted-trapezoid",
    "title": "F6.11, F6.16, F6.17: keyword-disrupted and triangle columnar, interrupted-key columnar and trapezoid transpositions, every dictionary keyword, then or before a repeating key on the table",
    "family": "6-transposition-then-tableau",
    "parent": "0110-true-keyword-columnar-from-the-dictionary",
    "changed": (
        "Three items from the field manuals, one run, a verdict each. F6.11: Rijmenants's keyword-disrupted columnar (each "
        "row filled up to a triangle that starts at the column of the next key number and moves one column right per row; "
        "triangle cells filled afterwards; columns read in key order) and TM 32-220 par. 87's triangle (rows of 1, 3, 5... "
        "cells centred under 19 columns, ten rows, three blank cells at the end or the start, the keyword repeated to 19 "
        "letters and numbered). F6.16: TM 32-220 par. 89c-e's interrupted-key columnar (rows only as long as the next number "
        "of the keyword's numbering, or, for puzzle words of nine letters or more, the next nonzero digit of 1/d for d 3-99). F6.17: par. 86's trapezoid (base = the "
        "keyword's length, rows one shorter going up on the right or on the left, the fewest blank cells at the end). Keys: "
        "every dictionary word and puzzle word of 4-24 letters, deduplicated by numbering. Then a repeating key 1-26 on the "
        "standard or KRYPTOS table after or before; compiled; ten scrambled coppers."
    ),
    "hypothesis_expert": (
        "C1(a) (matrix codes), C5 (keyword-only hand systems); sources: TM 32-220 pars. 86, 87, 89 (research_notes/Scheidt "
        "patents and field ciphers/addendum_downloaded_manuals.md, figures partly garbled, rules read from the text) and "
        "Rijmenants's Hand Ciphers (foreign_agent_hand_systems.md section 5). Where the sources leave a choice open, both "
        "readings are run (triangle blanks at end or start; trapezoid shrinking on either side). Key numbering: letters "
        "ranked alphabetically, ties left to right. Periodic key: order A (after) or B (before), 8 classes (plain and "
        "cipher standard or KRYPTOS, Beaufort or not). Statistic fixed before the run (0134's), per item."
    ),
    "hypothesis_eli5": (
        "Army manuals and agent ciphers describe ways of writing a message into odd-shaped grids before copying it out "
        "by keyword-ordered columns: grids with triangular holes filled last, triangles that grow two letters per row, "
        "rows cut short at lengths the keyword gives, and trapezoids. Each needs only a keyword. We build all of them "
        "for every dictionary word and test each with a repeating secret word on the sculpture's table."
    ),
    "prediction": "For each item, nothing live below key length 20 beyond the coppers' rate, and K4 above every copper in no more cells than the null's maximum. Zero candidates.",
    "method": (
        "1. Keywords: dictionary and puzzle words of 4-24 letters, one per distinct numbering. "
        "2. Per item, build the routes (where-maps) in the workers; forward and inverse. "
        "3. Compiled periodic-key test, orders A and B, 8 classes, K4 and 10 coppers; the fixed statistic per item."
    ),
    "walkthrough": (
        "1. Triangle: ten rows of 1, 3, 5, ..., 19 cells, centred; write the 97 letters row by row, three cells left empty. "
        "2. Repeat the keyword to 19 letters, number the letters alphabetically, and copy out the columns in that order, top to bottom. "
        "3. Disrupted: in a grid as wide as the keyword, leave a triangle empty from the column of key number 1, one column narrower each row; fill the rest, then the triangle; copy out by key order. "
        "4. Interrupted: cut each row short at the next number of the keyword's numbering. Trapezoid: each row one cell shorter going up. "
        "5. Then a repeating key on the table; check the known letters for every key length, and on scrambled copies."
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


def routes_for(item, words):
    out = []
    for wd in words:
        try:
            if item == "F6.11 disrupted":
                seqs = [("", disrupted(wd))]
            elif item == "F6.11 triangle":
                seqs = [("end", triangle(wd, blanks="end")), ("start", triangle(wd, blanks="start"))]
            elif item == "F6.16 interrupted":
                num = [0] * len(wd)
                for r, i in enumerate(numeric_order(wd)):
                    num[i] = r + 1
                seqs = [("num", interrupted(wd, num))]
                if len(wd) >= 9 and wd in PUZZLE:
                    seqs += [(f"1/{d}", interrupted(wd, frac_digits(d))) for d in range(3, 100)]
            else:
                b = len(wd)
                seqs = []
                for h in range(2, b + 1):
                    cells = h * b - h * (h - 1) // 2
                    if cells >= N:
                        for side in ("right", "left"):
                            s_ = trapezoid(wd, h, side)
                            if s_:
                                seqs.append((f"h{h} {side}", s_))
                        break
        except Exception:
            continue
        for tag, s_ in seqs:
            if s_ is not None and len(s_) == N and sorted(s_) == list(range(N)):
                out.append((f"{wd} {tag}".strip(), where(s_)))
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


ITEMS = ("F6.11 disrupted", "F6.11 triangle", "F6.16 interrupted", "F6.17 trapezoid")


def run(ctx):
    import multiprocessing as mp
    import sys
    import types
    ct, known = ctx.K4, ctx.KNOWN
    known_list = [(q, known[q]) for q in sorted(known)]
    # each builder is a permutation of the 97 places
    for item in ITEMS:
        r = routes_for(item, ["KRYPTOSABSCISSA"])
        assert r and all(sorted(m) == list(range(N)) for _, m in r), item
    words = keywords(ctx.vocabulary)
    rng = random.Random(1610)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    # the compiled tester against Python on a few routes
    sample = routes_for("F6.11 triangle", ["PALIMPSEST", "BERLINCLOCK"]) + routes_for("F6.17 trapezoid", ["UNDERGROUND"])
    rt_run_check = rt_build(texts, known_list)
    for name, m in sample[:3]:
        live = (ctypes.c_long * (2 * len(texts) * 27))(); low = (ctypes.c_long * (2 * len(texts)))(); k4l = (ctypes.c_long * 1)()
        ex = (ctypes.c_int * 11)(); nex = ctypes.c_int(0)
        rt_run_check.test_maps((ctypes.c_int * 97)(*m), 1, live, low, k4l, ex, ctypes.byref(nex), 0)
        for o in (0, 1):
            assert [live[(o * len(texts) + 0) * 27 + p] for p in range(1, 27)] == rt_reference(m, texts, known_list, o, 0)[1:]
    if getattr(sys.modules.get(__name__), "gen_worker", None) is not gen_worker:
        mod = types.ModuleType(__name__); mod.__dict__.update(globals()); sys.modules[__name__] = mod
    res = {}
    t0 = time.time()
    with mp.get_context("fork").Pool(WORKERS) as pool:
        for item in ITEMS:
            if ctx.time_left() < 240:
                res[item] = {"skipped": "time"}
                continue
            res[item] = run_item(item, words, texts, known_list, pool)
    bounds = {"family": "keyword-shaped transpositions from TM 32-220 and Rijmenants (disrupted, triangle, interrupted, trapezoid), then or before a periodic key",
              "keywords": len(words), "items": res, "seconds": round(time.time() - t0),
              "controls": f"{N_CONTROLS} shuffled coppers (seed 1610)", "exhaustive": "exact per item done"}
    notes = "; ".join(f"{k}: {v.get('routes', 0):,} routes, shortest live A {v.get('k4_shortest_live', {}).get('A')} B {v.get('k4_shortest_live', {}).get('B')}, K4 above every copper {len(v.get('cells_k4_above_every_copper', []))} (null max {max(v.get('null_cells_above_rest_per_copper', [0]))})" for k, v in res.items())
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
