"""Experiment 0236. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f13-one-free-alphabet-ciphertext-only-power-first",
    "title": "F13.4c: one free alphabet with a periodic key (Quagmire III, both forms), lengths 1-19, from the ciphertext alone: power on planted messages first, then K4 against 50 climbed shuffles in the lengths the plants decide",
    "family": "13-ciphertext-only",
    "parent": "0234-f13-periodic-key-on-the-sculptures-tables-ciphertext-only",
    "changed": (
        "F13.4c (issue #85). F1.5's design 2 (0140's compiled parallel tempering) is run with no known letter: every key "
        "slot free, no check-keeping, the alphabet and key climbed together by quadgrams, a second form (added) beside "
        "0140's Beaufort. A probe before this run (one tempering run per plant) read 54 of 97 letters of a plant at "
        "length 5 and nothing at 10 or 15, so power comes first, in the same run: 8 plants at each of the lengths 2-8, "
        "10, 13, 16, 19 (no known words; half X stops; half each form), each against 6 own shuffles climbed the same way "
        "(null 1/7), 3 tempering runs per text, best reading rescored by MIX8m. Then K4 and 50 shuffles at every length "
        "1-19 in both forms; the statistic is the largest z-score over the cells the plants decide (6 of 8). Cost stated "
        "before the run: 616 + 1,938 climbs x about 10 s, about 7 core-hours."
    ),
    "hypothesis_expert": (
        "F1.1 (Quagmire III with an unknown order: K1-K2's system with Sanborn's 'slightly different' chart, C27(c)) "
        "read without the 24 known letters: the hedge for A1/A2 on the family closed exactly at 1-22, 24, 25 (0119) and "
        "reopened at Beaufort 23 and 26 (0228, 0229). F13.1 puts one free alphabet decidable by quadgrams to length 19 "
        "(80 bits for the alphabet plus 4.7 per key letter, under 173), which is necessary, not sufficient: a climb must "
        "also find the key, and with no known letter design 2 has no anchor. Pre-registered: a cell (length, form) is "
        "decided when the planted length bracketing it from above found at least 6 of 8 (lengths below the shortest "
        "failing planted length); S = max z over decided cells against 50 shuffles; K4 flags at p < 0.05. If no length "
        "is decided the item is blocked by power with the numbers."
    ),
    "hypothesis_eli5": (
        "The same as before, but now the table's alphabet is also unknown: any of the 400 million million million million "
        "orders of the 26 letters. Without the clue words the computer has to guess the alphabet and the secret word "
        "together from how English the result looks. First we find out, with hidden test messages, up to what word length "
        "that can work at all; only there do we compare K4 with shuffles of itself."
    ),
    "prediction": (
        "Plants found at lengths 2-4, some at 5-6, none from 8: the decided range ends near 5. K4 inside its shuffles in "
        "that range (p above 0.05). F13.4c closed for the short lengths, blocked from about 6 by power."
    ),
    "method": (
        "1. Plants: Carter's held-out last 20% (clean or X stops), a random alphabet, key and form, lengths 2-8, 10, 13, "
        "16, 19; 8 per length; 6 own shuffles each. "
        "2. Every text climbed at its length and form: 3 runs of 0140's parallel tempering (16 replicas x 625 rounds x "
        "1,000 moves), no known letter, the best reading rescored by MIX8m (0233). "
        "3. A plant is found when its score is above all 6 own shuffles'. A cell is decided below the first planted "
        "length under 6 of 8. "
        "4. K4 and 50 shuffles of K4 at every length 1-19 and both forms, climbed the same way; S = max z over decided "
        "cells; K4 ranked. "
        "5. K4's best reading per decided cell submitted (key: alphabet, form, shifts) for the harness's gates."
    ),
    "walkthrough": (
        "1. Hide a test message under a shuffled alphabet and a short repeating key. "
        "2. Let the computer swap alphabet letters and change key letters, keeping changes that make the text read more "
        "like English, with some randomness to escape dead ends. "
        "3. Do the same to six shuffles of the hidden message's letters; if the message scores above all six, it was found. "
        "4. Repeat at longer keys until test messages stop being found. "
        "5. Only at the key lengths where they are found, compare K4 with 50 shuffles of itself."
    ),
    "expected_minutes": 60,
}

import ctypes
import importlib.util
import os
import random
import subprocess
import sys
import tempfile
import time
import types
from pathlib import Path

import numpy as np

N = 97
ROOT = Path(__file__).resolve().parent
STD = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
FORMS = ("beaufort", "added")
PLANT_LENGTHS = (2, 3, 4, 5, 6, 7, 8, 10, 13, 16, 19)
PLANTS_PER_LENGTH, OWN_COPIES = 8, 6
K4_LENGTHS = range(1, 20)
N_COPIES = 50
RUNS = 3
PT_R, PT_ROUNDS, PT_MOVES, PT_T0, PT_T1 = 16, 625, 1000, 0.1, 0.002     # 0140's design 2
LAM_Q = 0.55
SEED = 236
_G = {}

C_SOURCE = r"""
// Beaufort-form one-alphabet climb with known-letter-preserving moves. p_i = a[(k[i mod L] - x[c_i]) mod 26].
#include <math.h>
#include <string.h>
#include <stdint.h>

static uint64_t s64;
static inline uint64_t rnd(void) { s64 ^= s64 << 13; s64 ^= s64 >> 7; s64 ^= s64 << 17; return s64; }
static inline int rint26(int n) { return (int)(rnd() % (uint64_t)n); }
static inline double runif(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }

static int NCH, CH[64][4], NREP, REPS[32], REPC[32], REPP[32], NFREE, FREE[32], L, N, C[128], INCH[26];
static const double *TAB; static int FORM;  /* 0 Beaufort p = a[k - x[c]], 1 added p = a[x[c] - k] */

static int checks_ok(const int *x) {
    for (int j = 0; j < NCH; j++) if (((x[CH[j][0]] + x[CH[j][1]] - x[CH[j][2]] - x[CH[j][3]]) % 26 + 26) % 26) return 0;
    return 1;
}

static double decode_score(const int *x, const int *kf, int *pt) {
    int inv[26], k[64];
    for (int le = 0; le < 26; le++) inv[x[le]] = le;
    for (int j = 0; j < NREP; j++) k[REPS[j]] = (x[REPC[j]] + x[REPP[j]]) % 26;
    for (int j = 0; j < NFREE; j++) k[FREE[j]] = kf[j];
    for (int i = 0; i < N; i++) pt[i] = FORM ? inv[((x[C[i]] - k[i % L]) % 26 + 26) % 26] : inv[((k[i % L] - x[C[i]]) % 26 + 26) % 26];
    double t = 0;
    for (int j = 0; j < N - 3; j++) t += TAB[((pt[j] * 26 + pt[j + 1]) * 26 + pt[j + 2]) * 26 + pt[j + 3]];
    return t / (N - 3);
}

static int ORD[26], USED[26]; static long NODES;
static int dfs_assign(int *x, int oi) {
    if (oi == 26) return 1;
    if (++NODES > 3000) return 0;
    int le = ORD[oi], vals[26], nv = 0;
    for (int v = 0; v < 26; v++) if (!USED[v]) vals[nv++] = v;
    for (int i = nv - 1; i > 0; i--) { int j = rint26(i + 1); int t = vals[i]; vals[i] = vals[j]; vals[j] = t; }
    for (int vi = 0; vi < nv; vi++) {
        x[le] = vals[vi];
        int good = 1;
        for (int j = 0; j < NCH && good; j++) {
            int a = x[CH[j][0]], b = x[CH[j][1]], c = x[CH[j][2]], d = x[CH[j][3]];
            if (a < 0 || b < 0 || c < 0 || d < 0) continue;
            if (((a + b - c - d) % 26 + 26) % 26) good = 0;
        }
        if (good) {
            USED[vals[vi]] = 1;
            if (dfs_assign(x, oi + 1)) return 1;
            USED[vals[vi]] = 0;
        }
    }
    x[le] = -1;
    return 0;
}

static int init_try(int *x) {
    // letters in checks first (random order among them), then the rest; depth-first with random values
    int n = 0;
    for (int i = 0; i < 26; i++) { x[i] = -1; USED[i] = 0; }
    int a[26], na = 0, b[26], nb = 0;
    for (int le = 0; le < 26; le++) { if (INCH[le]) a[na++] = le; else b[nb++] = le; }
    for (int i = na - 1; i > 0; i--) { int j = rint26(i + 1); int t = a[i]; a[i] = a[j]; a[j] = t; }
    for (int i = nb - 1; i > 0; i--) { int j = rint26(i + 1); int t = b[i]; b[i] = b[j]; b[j] = t; }
    for (int i = 0; i < na; i++) ORD[n++] = a[i];
    for (int i = 0; i < nb; i++) ORD[n++] = b[i];
    NODES = 0;
    return dfs_assign(x, 0);
}
static int init(int *x) {
    for (int t = 0; t < 100000; t++) if (init_try(x)) return 1;
    return 0;
}

// one feasible move; returns number of swaps applied (0, 1 or 2), swaps recorded in sw
static int fswap(int *x, int sw[2][2]) {
    for (int t = 0; t < 50; t++) {
        int l1 = rint26(26), l2 = rint26(25); if (l2 >= l1) l2++;
        int tmp = x[l1]; x[l1] = x[l2]; x[l2] = tmp;
        if ((!INCH[l1] && !INCH[l2]) || checks_ok(x)) { sw[0][0] = l1; sw[0][1] = l2; return 1; }
        int cand[26] = {0};
        for (int j = 0; j < NCH; j++)
            if (((x[CH[j][0]] + x[CH[j][1]] - x[CH[j][2]] - x[CH[j][3]]) % 26 + 26) % 26)
                for (int q = 0; q < 4; q++) cand[CH[j][q]] = 1;
        int opts[700][2], no = 0;
        for (int m1 = 0; m1 < 26; m1++) {
            if (!cand[m1]) continue;
            for (int m2 = 0; m2 < 26; m2++) {
                if (m2 == m1 || (cand[m2] && m2 < m1)) continue;
                int u = x[m1]; x[m1] = x[m2]; x[m2] = u;
                if (checks_ok(x)) { opts[no][0] = m1; opts[no][1] = m2; no++; }
                u = x[m1]; x[m1] = x[m2]; x[m2] = u;
            }
        }
        if (no) {
            int r = rint26(no), m1 = opts[r][0], m2 = opts[r][1];
            int u = x[m1]; x[m1] = x[m2]; x[m2] = u;
            sw[0][0] = l1; sw[0][1] = l2; sw[1][0] = m1; sw[1][1] = m2; return 2;
        }
        tmp = x[l1]; x[l1] = x[l2]; x[l2] = tmp;
    }
    return 0;
}

// setup: ct (N ints), known: npos positions (0-based) and letters; returns 0 on success
int setup(const double *tab, const int *ct, int n, int l, const int *kpos, const int *klet, int nk, int form) {
    FORM = form; TAB = tab; N = n; L = l; NCH = 0; NREP = 0; NFREE = 0;
    for (int i = 0; i < n; i++) C[i] = ct[i];
    int first[64]; for (int s = 0; s < l; s++) first[s] = -1;
    for (int le = 0; le < 26; le++) INCH[le] = 0;
    for (int j = 0; j < nk; j++) {
        int s = kpos[j] % l, c = ct[kpos[j]], p = klet[j];
        if (first[s] < 0) { first[s] = j; REPS[NREP] = s; REPC[NREP] = c; REPP[NREP] = p; NREP++; }
        else {
            int j0 = first[s];
            CH[NCH][0] = ct[kpos[j0]]; CH[NCH][1] = klet[j0]; CH[NCH][2] = c; CH[NCH][3] = p;
            for (int q = 0; q < 4; q++) INCH[CH[NCH][q]] = 1;
            NCH++;
        }
    }
    for (int s = 0; s < l; s++) if (first[s] < 0) FREE[NFREE++] = s;
    return 0;
}

// restarts x anneals; returns best score; writes best plaintext (N ints), alphabet places x (26) and key (L)
double climb(uint64_t seed, int restarts, int iters, double T0, double T1, int *best_pt, int *best_x, int *best_k,
             double *per_restart) {
    s64 = seed * 2654435761u + 88172645463325252ull;
    double best = -99;
    int x[26], kf[32], pt[128], sw[2][2];
    for (int r = 0; r < restarts; r++) {
        if (!init(x)) { if (per_restart) per_restart[r] = -99; continue; }
        for (int j = 0; j < NFREE; j++) kf[j] = rint26(26);
        double cur = decode_score(x, kf, pt), rb = cur;
        int rx[26], rk[32];
        memcpy(rx, x, sizeof x); memcpy(rk, kf, sizeof kf);
        for (int it = 0; it < iters; it++) {
            double T = T0 * pow(T1 / T0, (double)it / iters);
            if (NFREE && runif() < 0.1) {
                int j = rint26(NFREE), old = kf[j]; kf[j] = rint26(26);
                double nw = decode_score(x, kf, pt);
                if (nw >= cur || runif() < exp((nw - cur) / T)) cur = nw; else kf[j] = old;
            } else {
                int ns = fswap(x, sw);
                if (!ns) continue;
                double nw = decode_score(x, kf, pt);
                if (nw >= cur || runif() < exp((nw - cur) / T)) cur = nw;
                else for (int q = ns - 1; q >= 0; q--) { int u = x[sw[q][0]]; x[sw[q][0]] = x[sw[q][1]]; x[sw[q][1]] = u; }
            }
            if (cur > rb) { rb = cur; memcpy(rx, x, sizeof x); memcpy(rk, kf, sizeof kf); }
        }
        if (per_restart) per_restart[r] = rb;
        if (rb > best) {
            best = rb;
            decode_score(rx, rk, best_pt);
            memcpy(best_x, rx, sizeof rx);
            int k[64];
            for (int j = 0; j < NREP; j++) k[REPS[j]] = (rx[REPC[j]] + rx[REPP[j]]) % 26;
            for (int j = 0; j < NFREE; j++) k[FREE[j]] = rk[j];
            for (int s = 0; s < L; s++) best_k[s] = k[s];
        }
    }
    return best;
}

// parallel tempering: R replicas at geometric temperatures T0 (hot) .. T1 (cold); each round every replica makes
// `moves` moves, then neighbours try to exchange states; `rounds` rounds; restarts times. Returns the best score.
double ptemper(uint64_t seed, int restarts, int R, int rounds, int moves, double T0, double T1,
               int *best_pt, int *best_x, int *best_k) {
    s64 = seed * 2654435761u + 88172645463325252ull;
    double best = -99;
    static int X[64][26], KF[64][32]; double CUR[64], TT[64];
    int pt[128], sw[2][2];
    for (int r = 0; r < restarts; r++) {
        for (int q = 0; q < R; q++) {
            TT[q] = T0 * pow(T1 / T0, (double)q / (R - 1));
            if (!init(X[q])) return -99;
            for (int j = 0; j < NFREE; j++) KF[q][j] = rint26(26);
            CUR[q] = decode_score(X[q], KF[q], pt);
        }
        for (int rd = 0; rd < rounds; rd++) {
            for (int q = 0; q < R; q++) {
                int *x = X[q], *kf = KF[q]; double cur = CUR[q], T = TT[q];
                for (int it = 0; it < moves; it++) {
                    if (NFREE && runif() < 0.1) {
                        int j = rint26(NFREE), old = kf[j]; kf[j] = rint26(26);
                        double nw = decode_score(x, kf, pt);
                        if (nw >= cur || runif() < exp((nw - cur) / T)) cur = nw; else kf[j] = old;
                    } else {
                        int ns = fswap(x, sw);
                        if (!ns) continue;
                        double nw = decode_score(x, kf, pt);
                        if (nw >= cur || runif() < exp((nw - cur) / T)) cur = nw;
                        else for (int z = ns - 1; z >= 0; z--) { int u = x[sw[z][0]]; x[sw[z][0]] = x[sw[z][1]]; x[sw[z][1]] = u; }
                    }
                    if (cur > best) {
                        best = cur; decode_score(x, kf, best_pt); memcpy(best_x, x, 26 * sizeof(int));
                        int k[64];
                        for (int j = 0; j < NREP; j++) k[REPS[j]] = (x[REPC[j]] + x[REPP[j]]) % 26;
                        for (int j = 0; j < NFREE; j++) k[FREE[j]] = kf[j];
                        for (int s = 0; s < L; s++) best_k[s] = k[s];
                    }
                }
                CUR[q] = cur;
            }
            for (int q = (rd & 1); q + 1 < R; q += 2) {
                double d = (CUR[q + 1] - CUR[q]) * (1.0 / TT[q] - 1.0 / TT[q + 1]);
                if (d >= 0 || runif() < exp(d)) {
                    int tx[26], tk[32]; double tc = CUR[q];
                    memcpy(tx, X[q], sizeof tx); memcpy(X[q], X[q + 1], sizeof tx); memcpy(X[q + 1], tx, sizeof tx);
                    memcpy(tk, KF[q], sizeof tk); memcpy(KF[q], KF[q + 1], sizeof tk); memcpy(KF[q + 1], tk, sizeof tk);
                    CUR[q] = CUR[q + 1]; CUR[q + 1] = tc;
                }
            }
        }
    }
    return best;
}
"""


def lib():
    if "lib" not in _G:
        d = tempfile.mkdtemp(prefix="k4_0236_")
        src, so = os.path.join(d, "pt.c"), os.path.join(d, "pt.so")
        open(src, "w").write(C_SOURCE)
        subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", so, src, "-lm"], check=True, capture_output=True)
        L_ = ctypes.CDLL(so)
        ip = ctypes.POINTER(ctypes.c_int)
        L_.setup.argtypes = [ctypes.POINTER(ctypes.c_double), ip, ctypes.c_int, ctypes.c_int, ip, ip, ctypes.c_int, ctypes.c_int]
        L_.ptemper.restype = ctypes.c_double
        L_.ptemper.argtypes = [ctypes.c_uint64, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double,
                               ctypes.c_double, ip, ip, ip]
        sys.path.insert(0, str(ROOT))
        from kryptos.scorer import _table
        logs, floor = _table()
        tab = [floor] * (26 ** 4)
        for q, v in logs.items():
            if len(q) == 4 and q.isalpha() and q.isupper():
                tab[((ord(q[0]) - 65) * 26 + ord(q[1]) - 65) * 676 + (ord(q[2]) - 65) * 26 + ord(q[3]) - 65] = v
        _G["tab"] = (ctypes.c_double * len(tab))(*tab)
        _G["lib"] = L_
    return _G["lib"]


def models():
    if "m233" not in _G:
        path = next((ROOT / "experiments").glob("0233-*")) / "attack.py"
        spec = importlib.util.spec_from_file_location("frozen0233", path)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        m.ROOT, m.SRC = ROOT, ROOT / "knowledge" / "sources"
        m.CARTER = m.SRC / "carter-1923-tomb-of-tutankhamen-vol1.txt"
        C = m.corpus()
        codes = np.array([STD.index(c) + 1 for c in C["train_manuals"]], dtype=np.int64)
        _G.update(m233=m, Q=m.quadgram_model(), KN8m=m.KN.from_text(codes, 8), corpus=C)
    return _G["m233"]


def mix8m(texts):
    m = _G["m233"]
    return np.log2(LAM_Q * m.per_letter_probs(_G["Q"], texts) + (1 - LAM_Q) * m.per_letter_probs(_G["KN8m"], texts)).sum(axis=1)


def encrypt(plaintext, key):
    """key: alphabet (26 letters; a letter's place is its index), form, shifts. Beaufort c = a[k - x(p)]; added c = a[x(p) + k]."""
    a, sh = key["alphabet"], key["shifts"]
    out = []
    for i, ch in enumerate(plaintext):
        x, k = a.index(ch), sh[i % len(sh)]
        out.append(a[(k - x) % 26] if key["form"] == "beaufort" else a[(x + k) % 26])
    return "".join(out)


def climb(text, L, form, seed):
    """RUNS tempering runs, no known letter; -> (MIX8m log2 prob of the best reading, reading, alphabet, shifts)."""
    L_ = lib()
    CT = (ctypes.c_int * N)(*[ord(c) - 65 for c in text])
    E = (ctypes.c_int * 1)()
    L_.setup(_G["tab"], CT, N, L, E, E, 0, FORMS.index(form))
    best = None
    for r in range(RUNS):
        bp = (ctypes.c_int * 128)(); bx = (ctypes.c_int * 52)(); bk = (ctypes.c_int * 64)()
        sc = L_.ptemper(seed * 100003 + r, 1, PT_R, PT_ROUNDS, PT_MOVES, PT_T0, PT_T1, bp, bx, bk)
        if best is None or sc > best[0]:
            x = list(bx)[:26]
            alpha = [""] * 26
            for le in range(26):
                alpha[x[le]] = STD[le]
            best = (sc, "".join(STD[v] for v in list(bp)[:N]), "".join(alpha), list(bk)[:L])
    return float(mix8m([best[1]])[0]), best[1], best[2], best[3]


def _job(args):
    tid, text, L, form, seed = args
    return tid, L, form, climb(text, L, form, seed)


def run(ctx):
    import multiprocessing as mp
    t0 = time.time()
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    lib(); models()
    rng = random.Random(SEED)
    C = _G["corpus"]
    jobs, plants = [], {}
    for L in PLANT_LENGTHS:
        for j in range(PLANTS_PER_LENGTH):
            src = C["test"] if j % 2 == 0 else C["test_xs"]
            o = rng.randrange(0, len(src) - N)
            pt = src[o:o + N]
            a = list(STD); rng.shuffle(a); a = "".join(a)
            form = FORMS[(j // 2) % 2]
            key = {"alphabet": a, "form": form, "shifts": [rng.randrange(26) for _ in range(L)]}
            pc = encrypt(pt, key)
            pid = f"plant{L}_{j}"
            plants[pid] = {"L": L, "form": form, "pt": pt}
            jobs.append((pid, pc, L, form, rng.randrange(10 ** 9)))
            for g in range(OWN_COPIES):
                s = list(pc); rng.shuffle(s); jobs.append((f"{pid}_own{g}", "".join(s), L, form, rng.randrange(10 ** 9)))
    k4 = ctx.K4
    texts = [("k4", k4)] + [(f"copy{i}", "".join(rng.sample(k4, N))) for i in range(N_COPIES)]
    for tid, t in texts:
        for L in K4_LENGTHS:
            for form in FORMS:
                jobs.append((tid, t, L, form, rng.randrange(10 ** 9)))
    res = {}
    workers = int(os.environ.get("K4_WORKERS", 8))
    ctx.progress(0, len(jobs), "climbs")
    with mp.get_context("fork").Pool(workers) as pool:
        for tid, L, form, out in pool.imap_unordered(_job, jobs, chunksize=1):
            res[(tid, L, form)] = out
            ctx.progress(len(res), len(jobs), "climbs")
    power, letters_right = {}, {}
    for L in PLANT_LENGTHS:
        f, lr = 0, []
        for j in range(PLANTS_PER_LENGTH):
            pid = f"plant{L}_{j}"; form = plants[pid]["form"]
            s = res[(pid, L, form)][0]
            f += s > max(res[(f"{pid}_own{g}", L, form)][0] for g in range(OWN_COPIES))
            lr.append(sum(1 for u, v in zip(res[(pid, L, form)][1], plants[pid]["pt"]) if u == v))
        power[L] = [f, PLANTS_PER_LENGTH]; letters_right[L] = lr
    failing = [L for L in PLANT_LENGTHS if power[L][0] < 6]
    limit = (min(failing) - 1) if failing else max(PLANT_LENGTHS)
    decided = [(L, form) for L in K4_LENGTHS if L <= limit and all(power[q][0] >= 6 for q in PLANT_LENGTHS if q <= L) for form in FORMS]
    k4_cells, s_k4, p_k4 = {}, None, None
    if decided:
        M = np.array([[res[(f"copy{i}", L, f)][0] for (L, f) in decided] for i in range(N_COPIES)])
        mu, sd = M.mean(axis=0), M.std(axis=0) + 1e-9
        zk = (np.array([res[("k4", L, f)][0] for (L, f) in decided]) - mu) / sd
        zc = ((M - mu) / sd).max(axis=1)
        s_k4 = float(zk.max())
        p_k4 = (1 + int((zc >= s_k4).sum())) / (N_COPIES + 1)
        for (L, f), z in zip(decided, zk):
            k4_cells[f"{L}/{f}"] = round(float(z), 3)
    cands = [{"plaintext": res[("k4", L, f)][1], "key": {"alphabet": res[("k4", L, f)][2], "form": f, "shifts": res[("k4", L, f)][3]}}
             for (L, f) in decided] or [{"plaintext": res[("k4", 1, "beaufort")][1],
                                         "key": {"alphabet": res[("k4", 1, "beaufort")][2], "form": "beaufort", "shifts": res[("k4", 1, "beaufort")][3]}}]
    from kryptos.scorer import free_text     # gate 4's controls only, after the search
    cells = decided or [(1, "beaufort")]
    controls = [max(ctx.english_score(free_text(res[(f"copy{i}", L, f)][1])) for (L, f) in cells) for i in range(N_COPIES)]
    bounds = {
        "item": "F13.4c", "search_reads_known_letters": False, "forms": list(FORMS),
        "search": f"0140's parallel tempering, no known letter, {RUNS} runs x {PT_R} replicas x {PT_ROUNDS} rounds x {PT_MOVES} moves; MIX8m rescoring",
        "plant_power": power, "plant_letters_right": letters_right, "decided_up_to_length": limit if decided else 0,
        "decided_cells": [f"{L}/{f}" for (L, f) in decided], "k4_z_by_cell": k4_cells,
        "k4_statistic": s_k4, "k4_p": p_k4, "k4_copies": N_COPIES, "climbs": len(jobs),
        "expected_total_time": "2,554 climbs x about 10 s, about 7 core-hours",
        "exhaustive": False, "compute_seconds": round(time.time() - t0),
    }
    notes = ("plant power " + ", ".join(f"L{L} {v[0]}/8" for L, v in power.items()) +
             (f"; decided to length {limit}; K4 statistic {s_k4:.2f}, p {p_k4:.3f}" if decided else "; no length decided"))
    return {"candidates": cands, "bounds": bounds, "notes": notes, "controls": controls}


def worked_example(ctx, key):
    lib(); models()
    rng = random.Random(5)
    pt = "THEHOTAIRESCAPINGFROMTHECHAMBERCAUSEDTHEFLAMETOFLICKERBUTPRESENTLYDETAILSOFTHEROOMWITHINEMERGED"
    a = list(STD); rng.shuffle(a); a = "".join(a)
    k = {"alphabet": a, "form": "beaufort", "shifts": [rng.randrange(26) for _ in range(3)]}
    ct = encrypt(pt, k)
    s, rd, alpha, sh = climb(ct, 3, "beaufort", 1)
    return "\n".join([
        "A planted message from K3's own words, a shuffled alphabet and a key of 3, Beaufort form, no known letter:", "",
        f"  alphabet, true   {a}", f"  carved           {ct}", f"  alphabet, found  {alpha}", f"  reading          {rd}", "",
        f"  letters right: {sum(1 for u, v in zip(rd, pt) if u == v)} of 97"])
