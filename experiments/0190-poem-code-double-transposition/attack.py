"""Experiment 0190 (F11.2). See program.md for the contract."""

EXPERIMENT = {
    "slug": "poem-code-double-transposition",
    "title": "F11.2: the SOE poem code: a double columnar transposition keyed by consecutive words of K1-K3 and the Morse, then or before a repeating key on the sculpture's tables: exact",
    "family": "11-agency-hand-systems",
    "parent": "0184-routes-along-the-plate-layout",
    "changed": (
        "F11.2. The poem code (SOE, Second World War): the agent takes words from a memorised text, writes them out as one "
        "key, numbers its letters alphabetically (ties left to right) and transposes twice by columns with that number "
        "key. Here the memorised texts are the sculpture's own: the plaintexts of K1, K2 and K3 and the Morse. Keys: every "
        "run of 1-6 consecutive words, 5-40 letters; used for both transpositions, or split into two keys at every word "
        "boundary. Each move and its inverse, then (A) or before (B) a repeating key 1-26 on 8 table classes (F6's "
        "compiled tester); K4 against 15 shuffled copies. 0167-era double columnar tests used dictionary keywords, not "
        "these phrases."
    ),
    "hypothesis_expert": (
        "C5(b) ('key word/s'), A9 (agency hand systems; Scheidt's CIA background), F11; SOE poem code (Marks, Between "
        "Silk and Cyanide). Model: c = T(P2(P1(p))) or P2(P1(T(p))), P1, P2 columnar transpositions keyed by the phrase "
        "numbers, T a periodic tableau key. Statistic: 0134's fixed statistic and the shortest live period, K4 against "
        "copies."
    ),
    "hypothesis_eli5": (
        "British agents in the war carried their keys in their heads: a poem. They picked a few words, wrote them out, "
        "numbered the letters in alphabetical order, and used the numbers to shuffle the message twice through a grid. "
        "Here the 'poem' is the sculpture's own solved text. We try every run of a few consecutive words as the key, "
        "with a repeating secret word on the sculpture's tables before or after."
    ),
    "prediction": "No phrase key gives K4 a live period below the copies'; cells where K4 leads stay inside the copies' range. Zero candidates.",
    "method": (
        "1. Word lists of K1, K2, K3 plaintexts and the Morse. "
        "2. Every run of 1-6 consecutive words of 5-40 letters: its number key; the double columnar move with it twice, "
        "and with the run split in two at every word boundary. "
        "3. Each move and its inverse, deduplicated. "
        "4. F6's compiled tester: live (order, period) per text; K4 against 15 shuffled copies."
    ),
    "walkthrough": (
        "1. Take the words SHADOW FORCES from the Morse: SHADOWFORCES, 12 letters. "
        "2. Number the letters alphabetically, ties left to right: A=1, C=2, D=3, E=4, F=5, H=6, the Os 7 and 8, R=9, the Ss 10 and 11, W=12. "
        "3. Write the message in rows of 12, read the columns in number order; do it again. "
        "4. Undo that, and test a repeating key on the sculpture's tables against the 24 known letters. "
        "5. Every run of words, on K4 and on scrambled copies."
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


def phrase_texts():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parent
    if not (root / "kryptos").exists():
        root = Path.cwd()
    st = json.load(open(root / "data" / "site_texts.json"))
    words = SPACED.split()
    i2 = words.index("IT")                  # K2 begins IT WAS TOTALLY INVISIBLE
    i3 = words.index("SLOWLY")              # K3 begins SLOWLY DESPARATLY SLOWLY
    out = {"K1": words[:i2], "K2": words[i2:i3], "K3": words[i3:],
           "Morse": ["".join(ch for ch in w if ch.isalpha()) for w in " ".join(st["morse"]).upper().split()]}
    return {k: [w for w in v if w] for k, v in out.items()}


def number_key(key):
    order = sorted(range(len(key)), key=lambda i: (key[i], i))
    return order            # columns in reading order


def columnar(n, key):
    """carved position -> message position for one columnar pass (rows of len(key), columns read in key order)."""
    w = len(key)
    out = []
    for col in number_key(key):
        out += [r * w + col for r in range((n - col + w - 1) // w) if r * w + col < n]
    return out


def double_map(k1, k2, n=97):
    c1 = columnar(n, k1)          # after pass 1: position j holds message c1[j]
    c2 = columnar(n, k2)          # after pass 2: position j holds pass-1 position c2[j]
    carved_from = [c1[c2[j]] for j in range(n)]
    M = [0] * n
    for j, i in enumerate(carved_from):
        M[i] = j
    return M


def keys():
    out = []
    for name, words in phrase_texts().items():
        for a in range(len(words)):
            for b in range(a + 1, min(a + 6, len(words)) + 1):
                ws = words[a:b]
                k = "".join(ws)
                if not 5 <= len(k) <= 40:
                    continue
                out.append((f"{name} words {a + 1}-{b} ({' '.join(ws)})", k, k))
                for cut in range(1, len(ws)):
                    x, y = "".join(ws[:cut]), "".join(ws[cut:])
                    if len(x) >= 3 and len(y) >= 3:
                        out.append((f"{name} words {a + 1}-{b} split after {cut}", x, y))
    return out


def run(ctx):
    t0 = time.time()
    ct = ctx.K4
    import random
    rng = random.Random(1900)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    known_list = sorted(KNOWN.items())
    K = keys()
    named = [(name, double_map(k1, k2)) for name, k1, k2 in K]
    for _, m in named[:50]:
        assert sorted(m) == list(range(97))
    maps = dedupe(named)
    res = rt_run(maps, texts, known_list, workers=4, batch=500)
    bounds = {"family": "SOE poem code: double columnar keyed by 1-6 consecutive words of K1-K3 and the Morse (same key twice, or split), then/before a periodic key 1-26, 8 classes, exact",
              "phrase_keys": len(K), "maps_after_dedupe": len(maps), **res,
              "copies": f"{N_CONTROLS} shuffled copies (seed 1900)", "seconds": round(time.time() - t0), "exhaustive": True}
    notes = (f"{len(maps)} moves; shortest live K4 A {res['k4_shortest_live']['A']} B {res['k4_shortest_live']['B']} "
             f"(copies {res['coppers_shortest_live']['A']}, {res['coppers_shortest_live']['B']}); K4 above every copy in "
             f"{len(res['cells_k4_above_every_copper'])} of 52 cells (copies {min(res['null_cells_above_rest_per_copper'])}-{max(res['null_cells_above_rest_per_copper'])})")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    k = "SHADOWFORCES"
    order = number_key(k)
    nums = [0] * len(k)
    for rank, col in enumerate(order, start=1):
        nums[col] = rank
    M = double_map(k, k)
    inv = [0] * 97
    for i, j in enumerate(M):
        inv[j] = i
    return (f"key {k}, column numbers {nums}" + chr(10) +
            "K4 with the double transposition undone: " + "".join(ctx.K4[M[i]] for i in range(97)))
