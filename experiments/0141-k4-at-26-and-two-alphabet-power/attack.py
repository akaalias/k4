"""Experiment 0141. See program.md for the contract."""

EXPERIMENT = {
    "slug": "k4-at-26-and-two-alphabet-power",
    "title": "F1.1 at key length 26 decided with design 2 (K4 against its own copies); design 2 carried to two free alphabets (Quagmire IV) and its power measured at F1.2's lengths 8, 13 and 16",
    "family": "1-keyed-periodic",
    "parent": "0140-k4-against-its-own-copies-with-the-tempering-climb",
    "changed": (
        "F1.1 Beaufort 26 and F1.2. 0140 found design 2 has power at length 26 too (5 of 6 planted texts beat all their own "
        "copies), so K4 at 26 now runs against 12 fitting shuffles of itself. In the same run design 2 is carried to two "
        "independent alphabets (Quagmire IV: C(c) = P(p) + k), the case F1.2 leaves at lengths 8, 13 and 16 under 0136's "
        "bound: compiled tempering over both alphabets, every move keeping the known-letter checks, each run started from an "
        "exact witness (0123's decider) randomised by 400 check-keeping swaps; power measured on planted texts against their "
        "own fitting shuffles."
    ),
    "hypothesis_expert": (
        "C27(c), C1(b). L26 one alphabet, Beaufort form (1 check), as 0140 (seed 141): K4 vs 12 shuffles of K4 fitting at "
        "26; measured power 5 of 6 at 6 copies (0140); rule fixed before the run: K4 above all 12 stops the queue for "
        "replication, otherwise the cell closes sampled at that power. Quagmire IV (0123's model, two unknown bijections P "
        "and C, key length L): 0136 bounds the open bits at 89, 112 and 126 for L 8, 13, 16 against 130 of quadgram "
        "evidence; checks 16, 11, 8. Search: replica exchange, 16 replicas, T 0.1 -> 0.002, 10 runs x 625 rounds x 1,000 "
        "moves per text (0139's effort); moves swap two places in one alphabet, repaired by a second swap when a check "
        "breaks. Power: 4 planted texts per length (Carter windows, seed 1411), each against 5 shuffles of itself fitting "
        "that length (0123's decider); null 1/6 per plant; bar fixed before the run: at least 3 of 4 beat all their own "
        "copies. A length that passes gets K4 against its own copies in the next run; one that fails stays blocked."
    ),
    "hypothesis_eli5": (
        "Two pieces. First, the carved text is run through the new search for a scrambled alphabet with a 26-letter key, "
        "against scrambled copies of itself. Second, the search is extended to two scrambled alphabets, one for the "
        "message and one for the carved letters, and tested on planted English at the three key lengths where English "
        "could in principle decide, before it is allowed to judge the carved text."
    ),
    "prediction": (
        "K4 inside its copies at 26 (cell closes at power about 0.8). Two alphabets: power falls with the number of checks "
        "and the doubled alphabet freedom: at least 3 of 4 at length 8 (16 checks), fewer than 3 at 13 and 16. No reading."
    ),
    "method": (
        "1. Draw 12 shuffles of K4 fitting at 26 (one alphabet, Beaufort form); 4 planted Quagmire IV texts at each of 8, "
        "13, 16 and 5 fitting shuffles of each. "
        "2. One-alphabet texts: 0139's search. Two-alphabet texts: the same search over both alphabets from a witness start; "
        "the compiled decryption checked against Python on every text. "
        "3. L26: K4's rank. Two alphabets: plants beating all their own copies per length."
    ),
    "walkthrough": (
        "1. Two alphabets: number the message letters by one scrambled order and the carved letters by another; carved place = message place + key value. "
        "2. Two known letters under one key letter must give the same difference, carved place minus message place: at length 8 sixteen such checks. "
        "3. Find one pair of orders that satisfies every check exactly, then shuffle it by swaps that keep the checks. "
        "4. Run sixteen searches side by side over pairs of orders that keep the checks, scoring the whole text as English. "
        "5. Do the same on planted English and on shuffles of it; count how often the planted text wins."
    ),
}

import ctypes
import os
import random
import subprocess
import tempfile
import time

N = 97
LENGTHS = (23, 26)
N_CONTROLS = 12
N_PLANTS = 8
RESTARTS = 1000
ITERS = 100000
CHUNK = 50
T0, T1 = 0.05, 0.002
FOUND_BAR = 9
N_K4_COPPERS = 12
Q4_LENGTHS = (8, 13, 16)
Q4_PLANTS = 4
Q4_OWN = 5
Q4_BAR = 3
P0123 = "experiments/0123-two-free-alphabets-exact-at-every-key-length/attack.py"
N_PLANTS26 = 6
BAR26 = 5
N_OWN = 6
OWN_BAR = 6
R0137 = "experiments/0137-free-alphabet-climb-that-keeps-the-known-letters/result.json"
P0120 = "experiments/0120-one-free-alphabet-english-climb-at-23-and-26/attack.py"

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
static const double *TAB;

static int checks_ok(const int *x) {
    for (int j = 0; j < NCH; j++) if (((x[CH[j][0]] + x[CH[j][1]] - x[CH[j][2]] - x[CH[j][3]]) % 26 + 26) % 26) return 0;
    return 1;
}

static double decode_score(const int *x, const int *kf, int *pt) {
    int inv[26], k[64];
    for (int le = 0; le < 26; le++) inv[x[le]] = le;
    for (int j = 0; j < NREP; j++) k[REPS[j]] = (x[REPC[j]] + x[REPP[j]]) % 26;
    for (int j = 0; j < NFREE; j++) k[FREE[j]] = kf[j];
    for (int i = 0; i < N; i++) pt[i] = inv[((k[i % L] - x[C[i]]) % 26 + 26) % 26];
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
int setup(const double *tab, const int *ct, int n, int l, const int *kpos, const int *klet, int nk) {
    TAB = tab; N = n; L = l; NCH = 0; NREP = 0; NFREE = 0;
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


C_SOURCE4 = r"""
// Two-alphabet (Quagmire IV) climb with known-letter-preserving moves.
// Variables y[0..25] = plain-alphabet places P(letter), y[26..51] = cipher-alphabet places C(letter).
// Encryption C(c_i) = P(p_i) + k[i mod L]; decryption p_i = P^-1[(C(c_i) - k) mod 26].
// Check (two known letters in one slot): C(c1) - P(p1) - C(c2) + P(p2) = 0 mod 26.
#include <math.h>
#include <string.h>
#include <stdint.h>

static uint64_t s64;
static inline uint64_t rnd(void) { s64 ^= s64 << 13; s64 ^= s64 >> 7; s64 ^= s64 << 17; return s64; }
static inline int rint26(int n) { return (int)(rnd() % (uint64_t)n); }
static inline double runif(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }

static int NCH, CH[64][4], NREP, REPS[32], REPC[32], REPP[32], NFREE, FREE[32], L, N, C[128], INCH[52];
static const double *TAB;

static inline int chk(const int *y, int j) {
    return ((y[CH[j][0]] - y[CH[j][1]] - y[CH[j][2]] + y[CH[j][3]]) % 26 + 26) % 26;
}
static int checks_ok(const int *y) { for (int j = 0; j < NCH; j++) if (chk(y, j)) return 0; return 1; }

static double decode_score(const int *y, const int *kf, int *pt) {
    int pinv[26], k[64];
    for (int le = 0; le < 26; le++) pinv[y[le]] = le;
    for (int j = 0; j < NREP; j++) k[REPS[j]] = ((y[26 + REPC[j]] - y[REPP[j]]) % 26 + 26) % 26;
    for (int j = 0; j < NFREE; j++) k[FREE[j]] = kf[j];
    for (int i = 0; i < N; i++) pt[i] = pinv[((y[26 + C[i]] - k[i % L]) % 26 + 26) % 26];
    double t = 0;
    for (int j = 0; j < N - 3; j++) t += TAB[((pt[j] * 26 + pt[j + 1]) * 26 + pt[j + 2]) * 26 + pt[j + 3]];
    return t / (N - 3);
}

static int ORD[52], USED[2][26]; static long NODES;
static int dfs_assign(int *y, int oi) {
    if (oi == 52) return 1;
    if (++NODES > 5000) return 0;
    int v_ = ORD[oi], g = v_ >= 26, vals[26], nv = 0;
    for (int v = 0; v < 26; v++) if (!USED[g][v]) vals[nv++] = v;
    for (int i = nv - 1; i > 0; i--) { int j = rint26(i + 1); int t = vals[i]; vals[i] = vals[j]; vals[j] = t; }
    for (int vi = 0; vi < nv; vi++) {
        y[v_] = vals[vi];
        int good = 1;
        for (int j = 0; j < NCH && good; j++) {
            if (y[CH[j][0]] < 0 || y[CH[j][1]] < 0 || y[CH[j][2]] < 0 || y[CH[j][3]] < 0) continue;
            if (chk(y, j)) good = 0;
        }
        if (good) {
            USED[g][vals[vi]] = 1;
            if (dfs_assign(y, oi + 1)) return 1;
            USED[g][vals[vi]] = 0;
        }
    }
    y[v_] = -1;
    return 0;
}
static int init_try(int *y) {
    int n = 0, a[52], na = 0, b[52], nb = 0;
    for (int i = 0; i < 52; i++) y[i] = -1;
    for (int i = 0; i < 26; i++) { USED[0][i] = 0; USED[1][i] = 0; }
    for (int v = 0; v < 52; v++) { if (INCH[v]) a[na++] = v; else b[nb++] = v; }
    for (int i = na - 1; i > 0; i--) { int j = rint26(i + 1); int t = a[i]; a[i] = a[j]; a[j] = t; }
    for (int i = nb - 1; i > 0; i--) { int j = rint26(i + 1); int t = b[i]; b[i] = b[j]; b[j] = t; }
    for (int i = 0; i < na; i++) ORD[n++] = a[i];
    for (int i = 0; i < nb; i++) ORD[n++] = b[i];
    NODES = 0;
    return dfs_assign(y, 0);
}
static int START[52], HAVE_START = 0;
static int fswap(int *y, int sw[2][2]);
void set_start(const int *y0) { for (int i = 0; i < 52; i++) START[i] = y0[i]; HAVE_START = 1; }
static int init(int *y) {
    if (HAVE_START) {
        int sw[2][2];
        memcpy(y, START, 52 * sizeof(int));
        for (int t = 0; t < 400; t++) fswap(y, sw);
        return checks_ok(y);
    }
    for (int t = 0; t < 100000; t++) if (init_try(y)) return 1;
    return 0;
}

// one feasible move: swap two places within one alphabet, repaired by a second swap (either alphabet) if needed
static int fswap(int *y, int sw[2][2]) {
    for (int t = 0; t < 50; t++) {
        int g = rint26(2) * 26;
        int l1 = g + rint26(26), l2 = g + rint26(25); if (l2 >= l1) l2++;
        int tmp = y[l1]; y[l1] = y[l2]; y[l2] = tmp;
        if ((!INCH[l1] && !INCH[l2]) || checks_ok(y)) { sw[0][0] = l1; sw[0][1] = l2; return 1; }
        int cand[52] = {0};
        for (int j = 0; j < NCH; j++) if (chk(y, j)) for (int q = 0; q < 4; q++) cand[CH[j][q]] = 1;
        static int opts[3000][2]; int no = 0;
        for (int m1 = 0; m1 < 52; m1++) {
            if (!cand[m1]) continue;
            int gb = m1 >= 26 ? 26 : 0;
            for (int m2 = gb; m2 < gb + 26; m2++) {
                if (m2 == m1 || (cand[m2] && m2 < m1)) continue;
                int u = y[m1]; y[m1] = y[m2]; y[m2] = u;
                if (checks_ok(y) && no < 3000) { opts[no][0] = m1; opts[no][1] = m2; no++; }
                u = y[m1]; y[m1] = y[m2]; y[m2] = u;
            }
        }
        if (no) {
            int r = rint26(no), m1 = opts[r][0], m2 = opts[r][1];
            int u = y[m1]; y[m1] = y[m2]; y[m2] = u;
            sw[0][0] = l1; sw[0][1] = l2; sw[1][0] = m1; sw[1][1] = m2; return 2;
        }
        tmp = y[l1]; y[l1] = y[l2]; y[l2] = tmp;
    }
    return 0;
}

int setup(const double *tab, const int *ct, int n, int l, const int *kpos, const int *klet, int nk) {
    HAVE_START = 0; TAB = tab; N = n; L = l; NCH = 0; NREP = 0; NFREE = 0;
    for (int i = 0; i < n; i++) C[i] = ct[i];
    int first[64]; for (int s = 0; s < l; s++) first[s] = -1;
    for (int v = 0; v < 52; v++) INCH[v] = 0;
    for (int j = 0; j < nk; j++) {
        int s = kpos[j] % l, c = ct[kpos[j]], p = klet[j];
        if (first[s] < 0) { first[s] = j; REPS[NREP] = s; REPC[NREP] = c; REPP[NREP] = p; NREP++; }
        else {
            int j0 = first[s];
            CH[NCH][0] = 26 + ct[kpos[j0]]; CH[NCH][1] = klet[j0]; CH[NCH][2] = 26 + c; CH[NCH][3] = p;
            for (int q = 0; q < 4; q++) INCH[CH[NCH][q]] = 1;
            NCH++;
        }
    }
    for (int s = 0; s < l; s++) if (first[s] < 0) FREE[NFREE++] = s;
    return NCH;
}

// best_y: 52 places (plain then cipher); best_k: L key values
double climb(uint64_t seed, int restarts, int iters, double T0, double T1, int *best_pt, int *best_y, int *best_k,
             double *per_restart) {
    s64 = seed * 2654435761u + 88172645463325252ull;
    double best = -99;
    int y[52], kf[32], pt[128], sw[2][2];
    for (int r = 0; r < restarts; r++) {
        if (!init(y)) { if (per_restart) per_restart[r] = -99; continue; }
        for (int j = 0; j < NFREE; j++) kf[j] = rint26(26);
        double cur = decode_score(y, kf, pt), rb = cur;
        int ry[52], rk[32];
        memcpy(ry, y, sizeof y); memcpy(rk, kf, sizeof kf);
        for (int it = 0; it < iters; it++) {
            double T = T0 * pow(T1 / T0, (double)it / iters);
            if (NFREE && runif() < 0.1) {
                int j = rint26(NFREE), old = kf[j]; kf[j] = rint26(26);
                double nw = decode_score(y, kf, pt);
                if (nw >= cur || runif() < exp((nw - cur) / T)) cur = nw; else kf[j] = old;
            } else {
                int ns = fswap(y, sw);
                if (!ns) continue;
                double nw = decode_score(y, kf, pt);
                if (nw >= cur || runif() < exp((nw - cur) / T)) cur = nw;
                else for (int q = ns - 1; q >= 0; q--) { int u = y[sw[q][0]]; y[sw[q][0]] = y[sw[q][1]]; y[sw[q][1]] = u; }
            }
            if (cur > rb) { rb = cur; memcpy(ry, y, sizeof y); memcpy(rk, kf, sizeof kf); }
        }
        if (per_restart) per_restart[r] = rb;
        if (rb > best) {
            best = rb;
            decode_score(ry, rk, best_pt);
            memcpy(best_y, ry, sizeof ry);
            int k[64];
            for (int j = 0; j < NREP; j++) k[REPS[j]] = ((ry[26 + REPC[j]] - ry[REPP[j]]) % 26 + 26) % 26;
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
    static int X[64][52], KF[64][32]; double CUR[64], TT[64];
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
                        best = cur; decode_score(x, kf, best_pt); memcpy(best_x, x, 52 * sizeof(int));
                        int k[64];
                        for (int j = 0; j < NREP; j++) k[REPS[j]] = ((x[26 + REPC[j]] - x[REPP[j]]) % 26 + 26) % 26;
                        for (int j = 0; j < NFREE; j++) k[FREE[j]] = kf[j];
                        for (int s = 0; s < L; s++) best_k[s] = k[s];
                    }
                }
                CUR[q] = cur;
            }
            for (int q = (rd & 1); q + 1 < R; q += 2) {
                double d = (CUR[q + 1] - CUR[q]) * (1.0 / TT[q] - 1.0 / TT[q + 1]);
                if (d >= 0 || runif() < exp(d)) {
                    int tx[52], tk[32]; double tc = CUR[q];
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


def load_0120():
    """0119's exact decider, 0120's plant generator and Beaufort cipher, from 0120's frozen snapshot."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("a0120", P0120)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


_LIB = {}


def lib():
    if "lib" not in _LIB:
        d = tempfile.mkdtemp(prefix="k4_0137_")
        src = os.path.join(d, "climb.c")
        so = os.path.join(d, "climb.so")
        open(src, "w").write(C_SOURCE)
        subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", so, src], check=True, capture_output=True)
        L_ = ctypes.CDLL(so)
        L_.ptemper.restype = ctypes.c_double
        L_.ptemper.argtypes = [ctypes.c_uint64, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double,
                               ctypes.c_double, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
        from kryptos.scorer import _table
        logs, floor = _table()
        tab = [floor] * (26 ** 4)
        for q, v in logs.items():
            if len(q) == 4 and q.isalpha() and q.isupper():
                tab[((ord(q[0]) - 65) * 26 + ord(q[1]) - 65) * 676 + (ord(q[2]) - 65) * 26 + ord(q[3]) - 65] = v
        _LIB["tab"] = (ctypes.c_double * len(tab))(*tab)
        _LIB["lib"] = L_
    return _LIB["lib"]


PT_RUNS, PT_R, PT_ROUNDS, PT_MOVES, PT_T0 = 10, 16, 625, 1000, 0.1


def climb_text(text, known, L, seed, restarts, deadline):
    """Parallel tempering, PT_RUNS runs; return (best score, plaintext, alphabet, key, runs done)."""
    L_ = lib()
    kp = sorted(known)
    CT = (ctypes.c_int * N)(*[ord(ch) - 65 for ch in text])
    KP = (ctypes.c_int * 24)(*[q - 1 for q in kp])
    KL = (ctypes.c_int * 24)(*[ord(known[q]) - 65 for q in kp])
    L_.setup(_LIB["tab"], CT, N, L, KP, KL, 24)
    best = (-99.0, None, None, None)
    done = 0
    while done < PT_RUNS and time.time() < deadline:
        bp = (ctypes.c_int * 128)(); bx = (ctypes.c_int * 26)(); bk = (ctypes.c_int * 64)()
        sc = L_.ptemper(seed * 100003 + done, 1, PT_R, PT_ROUNDS, PT_MOVES, PT_T0, T1, bp, bx, bk)
        done += 1
        if sc > best[0]:
            alpha = [""] * 26
            for le in range(26):
                alpha[bx[le]] = chr(65 + le)
            best = (sc, "".join(chr(65 + bp[i]) for i in range(N)), "".join(alpha), [bk[s] for s in range(L)])
    return best + (done,)


def lib4():
    if "lib4" not in _LIB:
        lib()
        d = tempfile.mkdtemp(prefix="k4_0141_")
        src, so = os.path.join(d, "q4.c"), os.path.join(d, "q4.so")
        open(src, "w").write(C_SOURCE4)
        subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", so, src], check=True, capture_output=True)
        L_ = ctypes.CDLL(so)
        L_.ptemper.restype = ctypes.c_double
        L_.ptemper.argtypes = [ctypes.c_uint64, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double,
                               ctypes.c_double, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
        _LIB["lib4"] = L_
    return _LIB["lib4"]


def load_0123():
    import importlib.util
    spec = importlib.util.spec_from_file_location("a0123", P0123)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def plant4(L, rng, known):
    import re
    src = re.sub("[^A-Z]", "", open(load_0120().CARTER, errors="ignore").read().upper())
    s0 = rng.randrange(20000, len(src) - 200)
    pt = list(src[s0:s0 + N])
    for q, ch in known.items():
        pt[q - 1] = ch
    P = list(range(26)); C = list(range(26)); rng.shuffle(P); rng.shuffle(C)
    Ci = {v: i for i, v in enumerate(C)}
    k = [rng.randrange(26) for _ in range(L)]
    return "".join(chr(65 + Ci[(P[ord(ch) - 65] + k[i % L]) % 26]) for i, ch in enumerate(pt)), "".join(pt)


def witness4(text, known, L, rng, m0123):
    st, w = m0123.decide(m0123.equations(text, known, L), "V", rng, two=True)
    if st != "fit":
        return None
    x, k = w
    y = [-1] * 52
    for (f, le), v in x.items():
        y[(0 if f == "P" else 26) + le] = v
    for g in (0, 26):
        free = [v for v in range(26) if v not in y[g:g + 26]]
        rng.shuffle(free)
        for i in range(g, g + 26):
            if y[i] < 0:
                y[i] = free.pop()
    return y


def climb4(text, known, L, seed, y0, deadline):
    L_ = lib4()
    kp = sorted(known)
    CT = (ctypes.c_int * N)(*[ord(ch) - 65 for ch in text])
    KP = (ctypes.c_int * 24)(*[q - 1 for q in kp])
    KL = (ctypes.c_int * 24)(*[ord(known[q]) - 65 for q in kp])
    L_.setup(_LIB["tab"], CT, N, L, KP, KL, 24)
    L_.set_start((ctypes.c_int * 52)(*y0))
    best = (-99.0, None, None)
    done = 0
    while done < PT_RUNS and time.time() < deadline:
        bp = (ctypes.c_int * 128)(); by = (ctypes.c_int * 52)(); bk = (ctypes.c_int * 64)()
        sc = L_.ptemper(seed * 100003 + done, 1, PT_R, PT_ROUNDS, PT_MOVES, PT_T0, T1, bp, by, bk)
        done += 1
        if sc > best[0]:
            best = (sc, "".join(chr(65 + bp[i]) for i in range(N)), ([by[i] for i in range(52)], [bk[s] for s in range(L)]))
    sc, pt, (y, k) = best
    Pi = {y[le]: le for le in range(26)}
    ok = "".join(chr(65 + Pi[(y[26 + ord(ch) - 65] - k[i % L]) % 26]) for i, ch in enumerate(text)) == pt
    return sc, pt, done, ok


def _job4(args):
    kind, L, idx, text, truth, seed, deadline, y0 = args
    from kryptos.facts import KNOWN
    sc, pt, done, ok = climb4(text, KNOWN, L, seed, y0, deadline)
    agree = sum(1 for a_, b_ in zip(pt, truth) if a_ == b_) if (pt and truth) else None
    return kind, L, idx, sc, pt, None, None, agree, done, ok


def _any(args):
    return _job4(args) if len(args) == 8 else _job(args)


def beaufort_decrypt(ct, alpha, k):
    pos = {ch: i for i, ch in enumerate(alpha)}
    return "".join(alpha[(k[i % len(k)] - pos[ch]) % 26] for i, ch in enumerate(ct))


def beaufort_encrypt(pt, alpha, k):
    pos = {ch: i for i, ch in enumerate(alpha)}
    return "".join(alpha[(k[i % len(k)] - pos[ch]) % 26] for i, ch in enumerate(pt))


def _job(args):
    kind, L, idx, text, truth, seed, deadline = args
    from kryptos.facts import KNOWN
    sc, pt, alpha, k, done = climb_text(text, KNOWN, L, seed, RESTARTS, deadline)
    agree = sum(1 for a_, b_ in zip(pt, truth) if a_ == b_) if (pt and truth) else None
    ok = (pt is not None and beaufort_decrypt(text, alpha, k) == pt)
    return kind, L, idx, sc, pt, alpha, k, agree, done, ok


def run(ctx):
    import multiprocessing as mp
    import sys
    import types
    from kryptos.scorer import english_score, free_text
    ct, known = ctx.K4, ctx.KNOWN
    m0120, m0123 = load_0120(), load_0123()
    lib(); lib4()
    rng = random.Random(141)
    deadline = ctx.deadline - 120
    jobs = []
    assert m0120.decide(m0120.equations(ct, known, 26), "B")[0] == "fit"
    jobs.append(("k4", 26, 0, ct, None, rng.randrange(10 ** 9), deadline))
    got = 0
    while got < N_K4_COPPERS:
        sh = list(ct); rng.shuffle(sh); sh = "".join(sh)
        if m0120.decide(m0120.equations(sh, known, 26), "B", rng)[0] == "fit":
            jobs.append(("copper", 26, got, sh, None, rng.randrange(10 ** 9), deadline)); got += 1
    prng = random.Random(1411)
    for L in Q4_LENGTHS:
        for i in range(Q4_PLANTS):
            pc, pt = plant4(L, prng, known)
            y0 = witness4(pc, known, L, prng, m0123)
            assert y0 is not None
            jobs.append(("plant4", L, i, pc, pt, prng.randrange(10 ** 9), deadline, y0))
            g = 0
            while g < Q4_OWN:
                sh = list(pc); prng.shuffle(sh); sh = "".join(sh)
                y = witness4(sh, known, L, prng, m0123)
                if y is not None:
                    jobs.append(("own4", L, i * 100 + g, sh, None, prng.randrange(10 ** 9), deadline, y)); g += 1
    jobs.sort(key=lambda j: (j[0] != "k4", len(j) == 8))
    if getattr(sys.modules.get(__name__), "_any", None) is not _any:
        m = types.ModuleType(__name__); m.__dict__.update(globals()); sys.modules[__name__] = m
    with mp.get_context("fork").Pool(8) as pool:
        res = pool.map(_any, jobs, chunksize=1)
    k4, cop = None, []
    plants = {L: {} for L in Q4_LENGTHS}; own = {L: {i: [] for i in range(Q4_PLANTS)} for L in Q4_LENGTHS}
    done_all, all_ok = [], True
    for kind, L, idx, sc, pt, alpha, k, agree, done, ok in res:
        done_all.append(done); all_ok = all_ok and ok
        if kind == "k4":
            k4 = {"score": round(sc, 4), "plaintext": pt, "alphabet": alpha, "key": k, "english_free": round(english_score(free_text(pt)), 4)}
        elif kind == "copper":
            cop.append({"score": round(sc, 4), "english_free": round(english_score(free_text(pt)), 4)})
        elif kind == "plant4":
            plants[L][idx] = {"score": round(sc, 4), "letters_right": agree}
        else:
            own[L][idx // 100].append(round(sc, 4))
    cs = sorted(c["score"] for c in cop)
    k4_rank = 1 + sum(1 for c in cs if c > k4["score"])
    q4 = {}
    for L in Q4_LENGTHS:
        rows = []
        for i in range(Q4_PLANTS):
            p = plants[L][i]; o = sorted(own[L][i])
            p.update({"own_coppers": o, "rank_among_own": 1 + sum(1 for x in o if x > p["score"]), "found_own": p["score"] > max(o)})
            rows.append(p)
        f = sum(1 for p in rows if p["found_own"])
        q4[str(L)] = {"found": f, "passes_bar": f >= Q4_BAR, "rows": rows, "checks": 24 - len({(q - 1) % L for q in known})}
    stop = k4_rank == 1
    bounds = {
        "family": "L26 one alphabet Beaufort: K4 vs its own copies; two free alphabets (Quagmire IV) at 8, 13, 16: power of design 2",
        "search": f"parallel tempering, {PT_RUNS} runs x {PT_R} replicas x {PT_ROUNDS} rounds x {PT_MOVES} moves per text, T {PT_T0}->{T1}; two-alphabet runs start from an exact witness (0123) randomised by 400 check-keeping swaps",
        "not_exhaustive": True, "runs_done": {"min": min(done_all), "max": max(done_all)}, "c_decryption_checked": all_ok,
        "L26": {"k4": k4, "coppers": cs, "k4_rank_of_13": k4_rank, "k4_above_all_copies": stop,
                "power_measured_0140": "5 of 6 planted texts beat all 6 own copies"},
        "quagmire_iv_power": q4, "q4_bar": f">= {Q4_BAR} of {Q4_PLANTS} plants beat all {Q4_OWN} own copies (null {Q4_PLANTS / (Q4_OWN + 1):.2f})",
        "stop_queue": stop,
        "controls": "12 shuffles of K4 fitting at 26 (seed 141); per plant, own fitting shuffles (seed 1411)",
    }
    cands = [{"plaintext": k4["plaintext"], "key": {"alphabet": k4["alphabet"], "shifts": k4["key"], "form": "beaufort"},
              "key_description": f"Beaufort form, one alphabet {k4['alphabet']} on both sides, key length 26", "notes": "best of design 2 on K4 at 26"}]
    notes = (f"L26: K4 {k4['score']:.3f}, rank {k4_rank} of 13 ({cs[0]:.3f} to {cs[-1]:.3f}); stop {stop}. Quagmire IV power: "
             + ", ".join(f"L{L} {q4[str(L)]['found']}/{Q4_PLANTS}" for L in Q4_LENGTHS))
    return {"candidates": cands, "bounds": bounds, "notes": notes, "controls": [c["english_free"] for c in cop]}


def encrypt(plaintext, key):
    """Beaufort form on one alphabet: carved place = key value minus message place, mod 26."""
    return beaufort_encrypt(plaintext, key["alphabet"], key["shifts"])


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    L = 23
    lines = [f"key length {L}, Beaufort form: K4 in rows of {L}; each column is one key slot", ""]
    for r in range(0, N, L):
        lines.append("  " + " ".join(ct[r:r + L]))
    slots = {}
    for q in sorted(known):
        slots.setdefault((q - 1) % L, []).append(q)
    lines += ["", "the seven checks every move keeps (place(carved) + place(known) equal within a column):"]
    for s_, qs in sorted(slots.items()):
        if len(qs) > 1:
            lines.append(f"  column {s_}: " + " = ".join(f"{ct[q - 1]}+{known[q]} ({q})" for q in qs))
    if key:
        alpha, k = key["alphabet"], key["shifts"]
        pos = {ch: i for i, ch in enumerate(alpha)}
        lines += ["", f"best alphabet on K4: {alpha}", f"key values: {k}"]
        for q in (22, 64):
            s_ = (q - 1) % len(k)
            lines.append(f"place {q}: carved {ct[q - 1]} at {pos[ct[q - 1]]}, key {k[s_]}: {k[s_]} - {pos[ct[q - 1]]} = "
                         f"{(k[s_] - pos[ct[q - 1]]) % 26} -> {alpha[(k[s_] - pos[ct[q - 1]]) % 26]}")
    return "\n".join(lines)
