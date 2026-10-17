"""Experiment 0184 (F4.1). See program.md for the contract."""

EXPERIMENT = {
    "slug": "routes-along-the-plate-layout",
    "title": "F4.1: routes that follow the copper's physical layout (K4's four lines starting after K3's tail and the ?, the lower plate, the whole left side), then or before a repeating key: exact",
    "family": "4-sanborn-visual",
    "parent": "0092-grid-paths-then-tableau",
    "changed": (
        "F4.1. 0092 tested grid paths on rectangles of chosen widths with K4 starting at a corner. On the copper, K4 does "
        "not start at a corner: it occupies the last four 31-character lines of the lower-left plate, its first row "
        "holding only OBKR at columns 28-31 after K3's last letters and the ?. The plates' lines are ragged (29-33 "
        "characters; transcript in knowledge/01-facts.md). Routes are built on three physical grids: K4's own four lines, "
        "the lower plate's 14 lines, and the left side's 28 lines; for each, rows or columns from each corner, straight "
        "or back and forth, diagonals both ways, and spirals both ways; K4's letters are taken in the order a route "
        "visits K4's cells. Each route and its inverse, then (A) or before (B) a repeating key 1-26 on 8 table classes "
        "(F6's compiled tester); K4 against 15 shuffled copies."
    ),
    "hypothesis_expert": (
        "C3 (Sanborn's sculptural, visual habits), C1 ('matrix codes'), F4 ('Sanborn's visual systems'); the 31-letter "
        "lines as a grid (knowledge/04-structure.md). Model: message written along a route over the plate's cells, carved "
        "row by row (or the reverse), with a periodic tableau key before or after. Statistic: 0134's fixed statistic "
        "(cells (order, period) where K4 is live in more routes than every copy, against each copy's count against the "
        "rest), and the shortest live period."
    ),
    "hypothesis_eli5": (
        "On the copper, K4 starts near the end of a line, right after K3 and a question mark, and runs on for three full "
        "lines. If Sanborn wrote his message into that physical shape along some path, down the columns, back and forth, "
        "round in a spiral, the carved order would follow from it. We try every such path on the real layout, with a "
        "repeating secret word before or after, and compare with scrambled copies."
    ),
    "prediction": "No route gives K4 a live period below the copies'; the cells where K4 leads stay inside the copies' range. Zero candidates.",
    "method": (
        "1. Lay out the 28 lines of the left side from the transcript; K4's cells are the last 97. "
        "2. For each grid (K4's lines, lower plate, whole side) and route: the order in which K4's cells are visited. "
        "3. Each route as a where-map and its inverse, deduplicated. "
        "4. F6's compiled tester: live (order, period) settings per text; K4 against 15 shuffled copies."
    ),
    "walkthrough": (
        "1. Draw K4 on the copper: OBKR at the end of a line, then three lines of 31. "
        "2. Read its cells down the columns, left to right: column 1 gives the 2nd, 3rd and 4th lines' first letters, and so on; the column under O, B, K, R has four letters. "
        "3. That order says where each message letter was carved. "
        "4. Undo it and test every repeating key length 1-26 on the sculpture's tables against the 24 known letters. "
        "5. Same for every route and grid, and on scrambled copies."
    ),
}

import time

from kryptos.facts import KNOWN

N_CONTROLS = 15
LINES = [32, 31, 31, 30, 31, 32, 31, 31, 32, 31, 30, 31, 31, 31, 32, 30, 31, 30, 32, 30, 32, 31, 33, 29, 31, 31, 31, 31]

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


def grid(first_line):
    """Cells (row, col) of lines first_line..27; K4 = the last 97 cells (row-major)."""
    cells = [(r, c) for r in range(first_line, 28) for c in range(LINES[r])]
    k4 = cells[-97:]
    return cells, k4


def routes(cells):
    rows = sorted({r for r, _ in cells}); cols = sorted({c for _, c in cells})
    have = set(cells)
    out = {}
    for rflip in (0, 1):
        for cflip in (0, 1):
            R = rows[::-1] if rflip else rows
            C = cols[::-1] if cflip else cols
            tag = f"{'bottom' if rflip else 'top'}-{'right' if cflip else 'left'}"
            for boust in (0, 1):
                seq = []
                for k, r in enumerate(R):
                    cc = C[::-1] if boust and k % 2 else C
                    seq += [(r, c) for c in cc if (r, c) in have]
                out[f"rows from {tag}{' back and forth' if boust else ''}"] = seq
                seq = []
                for k, c in enumerate(C):
                    rr = R[::-1] if boust and k % 2 else R
                    seq += [(r, c) for r in rr if (r, c) in have]
                out[f"columns from {tag}{' back and forth' if boust else ''}"] = seq
                for anti in (0, 1):
                    seq = []
                    diags = {}
                    for (r, c) in cells:
                        rr = R.index(r); cc_ = C.index(c)
                        diags.setdefault(rr + cc_ if not anti else rr - cc_, []).append((rr, (r, c)))
                    for k, key in enumerate(sorted(diags)):
                        d = sorted(diags[key])
                        if boust and k % 2:
                            d = d[::-1]
                        seq += [x for _, x in d]
                    out[f"{'anti-' if anti else ''}diagonals from {tag}{' back and forth' if boust else ''}"] = seq
            for cw in (0, 1):
                # spiral over the bounding box from this corner, skipping empty cells
                top, bot, left, right = 0, len(rows) - 1, 0, len(cols) - 1
                seq = []
                while top <= bot and left <= right:
                    ring = [(top, c) for c in range(left, right + 1)] + [(r, right) for r in range(top + 1, bot + 1)]
                    if top < bot:
                        ring += [(bot, c) for c in range(right - 1, left - 1, -1)]
                    if left < right:
                        ring += [(r, left) for r in range(bot - 1, top, -1)]
                    if not cw:
                        ring = [ring[0]] + ring[1:][::-1]
                    seq += ring
                    top += 1; bot -= 1; left += 1; right -= 1
                seq = [(R[r] if not rflip else R[r], C[c]) for r, c in seq]
                seq = [x for x in seq if x in have]
                out[f"spiral from {tag} {'clockwise' if cw else 'anticlockwise'}"] = seq
    return out


def run(ctx):
    t0 = time.time()
    ct = ctx.K4
    import random
    rng = random.Random(1840)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    known_list = sorted(KNOWN.items())
    named = []
    sizes = {}
    for gname, first in (("K4's four lines", 24), ("lower plate", 14), ("whole left side", 0)):
        cells, k4 = grid(first)
        carved = {cell: i for i, cell in enumerate(k4)}
        rs = routes(cells)
        n = 0
        for rname, seq in rs.items():
            order = [x for x in seq if x in carved]
            assert len(order) == 97 and len(set(order)) == 97, (gname, rname)
            named.append((f"{gname}: {rname}", [carved[x] for x in order]))
            n += 1
        sizes[gname] = n
    maps = dedupe(named)
    res = rt_run(maps, texts, known_list, workers=4, batch=50)
    bounds = {"family": "routes over the copper's physical layout (K4's lines, lower plate, whole left side), then/before a periodic key 1-26, 8 classes, exact",
              "routes_per_grid": sizes, "maps_after_dedupe": len(maps), **res,
              "copies": f"{N_CONTROLS} shuffled copies (seed 1840)", "seconds": round(time.time() - t0), "exhaustive": True}
    notes = (f"{len(maps)} routes; shortest live K4 A {res['k4_shortest_live']['A']} B {res['k4_shortest_live']['B']} "
             f"(copies {res['coppers_shortest_live']['A']}, {res['coppers_shortest_live']['B']}); K4 above every copy in "
             f"{len(res['cells_k4_above_every_copper'])} of 52 cells (copies {min(res['null_cells_above_rest_per_copper'])}-{max(res['null_cells_above_rest_per_copper'])})")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    cells, k4 = grid(24)
    carved = {cell: i for i, cell in enumerate(k4)}
    seq = routes(cells)["columns from top-left"]
    order = [x for x in seq if x in carved]
    ct = ctx.K4
    return "K4's cells read down the columns from the top left: " + "".join(ct[carved[x]] for x in order)
