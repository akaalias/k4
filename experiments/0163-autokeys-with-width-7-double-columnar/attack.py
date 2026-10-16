"""Experiment 0163 (F6.9). See program.md for the contract."""

EXPERIMENT = {
    "slug": "autokeys-with-width-7-double-columnar",
    "title": "F6.9: ciphertext and plaintext autokey, every lag, joined to 0084's double columnar routes (one stage of width 7 in all 5,040 orders), either order, on the sculpture's tables",
    "family": "6-transposition-then-tableau",
    "parent": "0084-width-7-double-columnar",
    "changed": (
        "F6.9 (pivot audit, issue #55, D11). 0084 joined double columnar routes with one stage of width 7 in all 5,040 "
        "column orders to a repeating key; 0081 joined autokeys to the type-1 library. Here the two meet: the same "
        "routes (a width-7 stage in every order, the other a plain columnar of width 2-30 or a puzzle-word columnar, either "
        "first, forward and inverse, deduplicated) with ciphertext or plaintext autokey at every lag 1-96, the autokey "
        "after the move (on the moved stream) or before it, one alphabet throughout (standard or KRYPTOS), three rules. "
        "On a fixed table every check is a direct comparison; compiled; ten scrambled coppers."
    ),
    "hypothesis_expert": (
        "C11a (NSA 1992: 'plain-text auto-key' and 'interval 7', knowledge/sources/nsa-foia-1992-2014-blackvault-"
        "compilation.txt), C8(a) (KRYPTOS's seven letters as a column key), directions.md type 2 (sevens: the width-7 "
        "doublet column, 0056). Model: A move then autokey: c_j = T(y_j, k_j), k_j = c_{j-L} (ciphertext) or y_{j-L} "
        "(plaintext); B autokey then move: e_i = T(p_i, k_i), k_i = e_{i-L} or p_{i-L}, c_{M(i)} = e_i. Checks: every known "
        "letter whose key letter is known (always for ciphertext autokey past the primer; for plaintext autokey when the "
        "key's place is a known letter). A setting survives if every check agrees. Statistic fixed before the run (0081's): "
        "survivors with five or more checks per (kind, order), K4 against the coppers' range."
    ),
    "hypothesis_eli5": (
        "An autokey cipher uses the message, or the enciphered text, as its own key, a fixed number of letters back. "
        "Here it is combined with a double grid move in which one grid is seven wide (KRYPTOS has seven letters, and "
        "K4's doubled letters line up in sevens), in every column order. On the sculpture's tables each known letter "
        "can be checked directly, for every distance back, on the carved text and scrambled copies."
    ),
    "prediction": "Survivors with five or more checks at the coppers' rate in every kind and order (0081 found none with five on the type-1 library). Zero candidates.",
    "method": (
        "1. Stage maps: the 5,040 width-7 orders; second stages plain columnar 2-30 and puzzle-word columnar. "
        "2. Compiled: compose both orders, forward and inverse, deduplicate; for each route, lag, table and rule, the four autokey forms; count survivors by checks. "
        "3. K4 against the coppers."
    ),
    "walkthrough": (
        "1. Write the message in rows of 7 and read the columns in some order, say 3 1 6 0 4 2 5; then write it in rows of 12 and read down the columns. "
        "2. Encipher the moved text by ciphertext autokey at lag 8: each letter's key is the carved letter 8 places before. "
        "3. At each known letter's landing place, look up the carved letter there and the one 8 before: the table says which message letter that pair gives; it must be the known letter. "
        "4. Repeat for every order, width, lag, table and form, and on scrambled copies."
    ),
}

import ctypes
import itertools
import os
import random
import subprocess
import tempfile
import time
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
N_CONTROLS = 10
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
// Autokey with a transposition, fixed tables. For each route (where-map M: message place i -> carved place M[i]),
// lag L 1-96, table class and kind/order, count how many known letters are checked and whether all agree.
//   order A (move, then autokey on the moved stream y): carved c_j = T(y_j, key_j)
//      ct kind: key_j = c_{j-L}      -> check at landing j = M(i) if j - L >= 0: T^-1(c_j, c_{j-L}) == p_i
//      pt kind: key_j = y_{j-L}      -> check if j - L is the landing of a known letter
//   order B (autokey on the message, then move): e_i = T(p_i, key_i), c_{M(i)} = e_i
//      ct kind: key_i = e_{i-L} = c_{M(i-L)}  -> check if i - L >= 0
//      pt kind: key_i = p_{i-L}               -> check if i - L is a known place
// Table: one alphabet A (std or KRY) for plain, cipher and key letters; rule V: c = p + k, B: c = k - p, R: c = p - k.
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#define N 97

static int T;                    // texts
static int CT[2][16][N];         // carved letters as indices in alphabet a (0 std, 1 kry)
static int KP[24], KL[2][24];    // known places (0-based) and letters per alphabet
static int ISKNOWN[N], KIDX[N];

void set_texts(int t, const int *ct, const int *kp, const int *kl) {
    T = t;
    for (int a = 0; a < 2; a++) for (int x = 0; x < t; x++) for (int j = 0; j < N; j++) CT[a][x][j] = ct[(a * t + x) * N + j];
    for (int j = 0; j < N; j++) { ISKNOWN[j] = 0; KIDX[j] = -1; }
    for (int e = 0; e < 24; e++) { KP[e] = kp[e]; KL[0][e] = kl[e]; KL[1][e] = kl[24 + e]; ISKNOWN[kp[e]] = 1; KIDX[kp[e]] = e; }
}

static inline int dec(int c, int k, int rule) {     // plain index from cipher and key
    if (rule == 0) return ((c - k) % 26 + 26) % 26;
    if (rule == 1) return ((k - c) % 26 + 26) % 26;
    return ((c + k) % 26 + 26) % 26;
}

// counts[t][kind*2+order][checks 0..24] of settings where every checked letter agrees (survivors), all lags/classes
void test_route(const int *M, long *counts, long *best4, int *bestinfo, int route_id) {
    int inv[N], land[24];
    for (int i = 0; i < N; i++) inv[M[i]] = i;
    for (int e = 0; e < 24; e++) land[e] = M[KP[e]];
    for (int t = 0; t < T; t++) {
        for (int a = 0; a < 2; a++) for (int rule = 0; rule < 3; rule++) {
            const int *c = CT[a][t];
            for (int L = 1; L < N; L++) {
                // A, ct
                int chk = 0, ok = 1;
                for (int e = 0; e < 24 && ok; e++) { int j = land[e]; if (j - L < 0) continue; chk++; if (dec(c[j], c[j - L], rule) != KL[a][e]) ok = 0; }
                if (ok) counts[(t * 4 + 0) * 25 + chk]++;
                // A, pt: key y_{j-L} known if j-L is a landing of a known letter
                chk = 0; ok = 1;
                for (int e = 0; e < 24 && ok; e++) {
                    int j = land[e]; if (j - L < 0) continue;
                    int src = inv[j - L]; if (!ISKNOWN[src]) continue;
                    chk++; if (dec(c[j], KL[a][KIDX[src]], rule) != KL[a][e]) ok = 0;
                }
                if (ok) counts[(t * 4 + 1) * 25 + chk]++;
                // B, ct: key_i = c_{M(i-L)}
                chk = 0; ok = 1;
                for (int e = 0; e < 24 && ok; e++) { int i = KP[e]; if (i - L < 0) continue; chk++; if (dec(c[land[e]], c[M[i - L]], rule) != KL[a][e]) ok = 0; }
                if (ok) counts[(t * 4 + 2) * 25 + chk]++;
                // B, pt: key_i = p_{i-L} known if i-L is a known place
                chk = 0; ok = 1;
                for (int e = 0; e < 24 && ok; e++) { int i = KP[e]; if (i - L < 0 || !ISKNOWN[i - L]) continue; chk++; if (dec(c[land[e]], KL[a][KIDX[i - L]], rule) != KL[a][e]) ok = 0; }
                if (ok) counts[(t * 4 + 3) * 25 + chk]++;
            }
        }
    }
}

// width-7 column orders x a second stage, either first, forward and inverse; dedup by hash per call
static uint64_t *HS; static size_t HCAP;
static int hs_add(uint64_t h) { if (!h) h = 1; size_t i = h & (HCAP - 1); while (HS[i]) { if (HS[i] == h) return 0; i = (i + 1) & (HCAP - 1); } HS[i] = h; return 1; }

void run_second(const int *perm7s, int n7, const int *second, long *counts, long *n_routes, long *n_dupes) {
    HCAP = 1 << 17; HS = calloc(HCAP, sizeof(uint64_t));
    int c2[N], inv[N];
    for (int r = 0; r < n7; r++) {
        const int *a = perm7s + r * N;
        for (int ord = 0; ord < 2; ord++) {
            for (int i = 0; i < N; i++) c2[i] = ord ? a[second[i]] : second[a[i]];
            for (int i = 0; i < N; i++) inv[c2[i]] = i;
            for (int d = 0; d < 2; d++) {
                const int *M = d ? inv : c2;
                uint64_t h = 1469598103934665603ull;
                for (int i = 0; i < N; i++) { h ^= (uint64_t)M[i]; h *= 1099511628211ull; }
                if (!hs_add(h)) { (*n_dupes)++; continue; }
                (*n_routes)++;
                test_route(M, counts, 0, 0, 0);
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




def perm7_maps():
    out = []
    for perm in itertools.permutations(range(7)):
        rows = [list(range(N))[i:i + 7] for i in range(0, N, 7)]
        seq = []
        for col in perm:
            seq.extend(r[col] for r in rows if col < len(r))
        out.append(where(seq))
    return out


def second_stages(vocab):
    out = [(f"col{w}", where(stage(list(range(N)), w, "col"))) for w in range(2, 31)]
    words = sorted({w for w in SPACED.split() if 2 <= len(w) <= 30} | {w.upper() for w in vocab if 2 <= len(w) <= 30} | {w for w in EXTRA if len(w) <= 30})
    seen = {bytes(m) for _, m in out}
    for wd in words:
        if len(set(wd)) < 2:
            continue
        m = where(keyed_columnar(list(range(N)), wd))
        if bytes(m) not in seen:
            seen.add(bytes(m)); out.append((f"key:{wd}", m))
    return out


def build(texts, known_list):
    d = tempfile.mkdtemp(prefix="k4_f69_")
    src, so = os.path.join(d, "a.c"), os.path.join(d, "a.so")
    open(src, "w").write(C_SOURCE)
    subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", so, src], check=True, capture_output=True)
    lib = ctypes.CDLL(so)
    ct = []
    for A in (STD, KRY):
        for t in texts:
            ct += [A.index(ch) for ch in t]
    kp = [q - 1 for q, _ in known_list]
    kl = [STD.index(a) for _, a in known_list] + [KRY.index(a) for _, a in known_list]
    I = lambda v: (ctypes.c_int * len(v))(*v)
    lib.set_texts(len(texts), I(ct), I(kp), I(kl))
    return lib


def reference(M, text, known_list):
    """Python survivors by checks for one route on one text: {kindorder: [count by checks]}."""
    inv = [0] * N
    for i, j in enumerate(M):
        inv[j] = i
    kp = [q - 1 for q, _ in known_list]
    isk = {q - 1: a for q, a in known_list}
    out = [[0] * 25 for _ in range(4)]
    for A in (STD, KRY):
        c = [A.index(ch) for ch in text]
        for rule in range(3):
            dec = lambda cc, k: ((cc - k) if rule == 0 else (k - cc) if rule == 1 else (cc + k)) % 26
            for L in range(1, N):
                res = []
                for kind_order in range(4):
                    chk, ok = 0, True
                    for (q, a), i in zip(known_list, kp):
                        j = M[i]
                        p = A.index(a)
                        if kind_order == 0:
                            if j - L < 0:
                                continue
                            k = c[j - L]
                        elif kind_order == 1:
                            if j - L < 0 or inv[j - L] not in isk:
                                continue
                            k = A.index(isk[inv[j - L]])
                        elif kind_order == 2:
                            if i - L < 0:
                                continue
                            k = c[M[i - L]]
                        else:
                            if i - L < 0 or (i - L) not in isk:
                                continue
                            k = A.index(isk[i - L])
                        chk += 1
                        if dec(c[j], k) != p:
                            ok = False; break
                    if ok:
                        out[kind_order][chk] += 1
    return out


def _worker(args):
    seconds, perms, texts, known_list, deadline = args
    lib = build(texts, known_list)
    T = len(texts)
    counts = (ctypes.c_long * (T * 4 * 25))()
    nr, nd = ctypes.c_long(0), ctypes.c_long(0)
    flat7 = (ctypes.c_int * (len(perms) * N))(*[v for m in perms for v in m])
    done = 0
    for name, sm in seconds:
        if time.time() > deadline:
            break
        lib.run_second(flat7, len(perms), (ctypes.c_int * N)(*sm), counts, ctypes.byref(nr), ctypes.byref(nd))
        done += 1
    return list(counts), nr.value, nd.value, done


def run(ctx):
    import multiprocessing as mp
    import sys
    import types
    ct, known = ctx.K4, ctx.KNOWN
    known_list = [(q, known[q]) for q in sorted(known)]
    perms = perm7_maps()
    seconds = second_stages(ctx.vocabulary)
    rng = random.Random(1609)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    T = len(texts)
    # compiled survivors against Python on a few routes
    lib = build(texts[:2], known_list)
    vr = random.Random(16090)
    for _ in range(3):
        M = vr.choice(perms)
        counts = (ctypes.c_long * (2 * 4 * 25))()
        lib.test_route((ctypes.c_int * N)(*M), counts, None, None, 0)
        ref = reference(M, texts[0], known_list)
        assert [[counts[(0 * 4 + k) * 25 + c] for c in range(25)] for k in range(4)] == ref
    deadline = time.time() + ctx.time_left() - 90
    jobs = [(seconds[i::WORKERS * 2], perms, texts, known_list, deadline) for i in range(WORKERS * 2)]
    if getattr(sys.modules.get(__name__), "_worker", None) is not _worker:
        m = types.ModuleType(__name__); m.__dict__.update(globals()); sys.modules[__name__] = m
    t0 = time.time()
    with mp.get_context("fork").Pool(WORKERS) as pool:
        parts = pool.map(_worker, jobs, chunksize=1)
    cnt = [[[sum(p[0][(t * 4 + k) * 25 + c] for p in parts) for c in range(25)] for k in range(4)] for t in range(T)]
    names = ["A ciphertext autokey", "A plaintext autokey", "B ciphertext autokey", "B plaintext autokey"]
    summ = {}
    for k in range(4):
        ge5 = [sum(cnt[t][k][5:]) for t in range(T)]
        ge4 = [sum(cnt[t][k][4:]) for t in range(T)]
        summ[names[k]] = {"k4_ge5": ge5[0], "coppers_ge5": ge5[1:], "k4_ge4": ge4[0], "coppers_ge4": ge4[1:],
                          "k4_max_checks_survivor": max((c for c in range(25) if cnt[0][k][c]), default=0)}
    bounds = {"family": "ciphertext and plaintext autokey at lags 1-96, one alphabet (std or KRYPTOS), 3 rules, after or before 0084's width-7 double columnar routes",
              "width7_orders": len(perms), "second_stages": len(seconds), "second_stages_done": sum(p[3] for p in parts),
              "distinct_routes": sum(p[1] for p in parts), "duplicates_skipped": sum(p[2] for p in parts),
              "summary": summ, "seconds": round(time.time() - t0),
              "controls": f"{N_CONTROLS} shuffled coppers (seed 1609)", "exhaustive": "exact for every second stage done"}
    notes = "; ".join(f"{k}: >=5 checks K4 {v['k4_ge5']} (coppers {min(v['coppers_ge5'])}-{max(v['coppers_ge5'])})" for k, v in summ.items())
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    perm = (3, 1, 6, 0, 4, 2, 5)
    rows = [list(range(N))[i:i + 7] for i in range(0, N, 7)]
    seq = []
    for col in perm:
        seq.extend(r[col] for r in rows if col < len(r))
    a = where(seq); b = where(stage(list(range(N)), 12, "col"))
    M = [b[a[i]] for i in range(N)]
    lines = ["rows of 7 read in column order 3 1 6 0 4 2 5, then rows of 12 read down; ciphertext autokey at lag 8 after the move", "",
             "place  letter  lands at  carved  carved 8 before"]
    for q in (22, 23, 24, 64, 65):
        j = M[q - 1]
        lines.append(f"{q:5d}  {known[q]:>6}  {j + 1:8d}  {ct[j]:>6}  {ct[j - 8] if j >= 8 else '-':>15}")
    return "\n".join(lines)
