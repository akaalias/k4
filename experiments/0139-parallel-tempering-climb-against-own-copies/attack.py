"""Experiment 0139. See program.md for the contract."""

EXPERIMENT = {
    "slug": "parallel-tempering-climb-against-own-copies",
    "title": "F1.5 design 2: parallel tempering in the set that keeps the known letters, measured on planted English against scrambled copies of itself (one free alphabet, Beaufort form, key length 23)",
    "family": "1-keyed-periodic",
    "parent": "0138-climb-power-against-each-plants-own-copies",
    "changed": (
        "F1.5, step 2, design 2. Design 1 (0137) failed its validity check (0138): against shuffles of themselves only 6 of 12 "
        "planted texts beat all six copies (bar 9). The climb never recovers a planted text; the true key is a narrow "
        "basin (about 12 check-keeping swaps wide, dry runs) in a landscape of false optima. Design 2 replaces independent "
        "annealing restarts with parallel tempering: 16 replicas at temperatures 0.1 to 0.002 that exchange states, the "
        "standard remedy for rugged landscapes, at the same compute per text (10 runs x 16 replicas x 625 rounds x 1,000 "
        "moves = 10^8 moves). Bar measured as in 0138, each plant against its own shuffles."
    ),
    "hypothesis_expert": (
        "C27(c), C1(b) as 0137. Cell: one unknown alphabet, Beaufort form, key length 23 (7 checks), 75 open bits against "
        "130 bits of quadgram evidence (0136). Search: replica exchange Monte Carlo over the alphabet in the set where every "
        "known-letter check holds (0137's moves and start), free key values as moves, full-text quadgram mean, geometric "
        "ladder T 0.1 -> 0.002, neighbour exchanges after every round. Dry run on 8 plants before this record (scratch): "
        "no plant recovered, best -4.71 to -4.91, 31-46 letters right. Plants: 8 Carter windows (seed 139, 0120's "
        "generator); own coppers: 6 shuffles of each plant's ciphertext that fit length 23 exactly (0119's decider). Null "
        "rate of a plant beating all 6: 1/7. Bar fixed before the run: design 2 passes if at least 6 of 8 plants beat all "
        "6 of their own coppers. If it fails, F1.5 is blocked by its stop rule (two designs failed; issue #50)."
    ),
    "hypothesis_eli5": (
        "A second way of searching for hidden English under one scrambled alphabet. Instead of starting the search a "
        "thousand times from scratch, sixteen searches run side by side, some bold and some cautious, and swap places "
        "when a bold one finds something promising. We again test it on planted English, comparing each planted message "
        "only with scrambled copies of itself. If it cannot tell them apart well, we stop trying to build such a search "
        "and record the cells as undecidable with today's tools."
    ),
    "prediction": (
        "No plant recovered; fewer than 6 of 8 plants beat all 6 of their own coppers (about the 50% of design 1), so "
        "design 2 fails the bar and F1.5 is blocked by its stop rule. Zero candidates."
    ),
    "method": (
        "1. Draw 8 planted texts at length 23 and 6 fitting shuffles of each. "
        "2. Run the compiled parallel-tempering search on all 56 texts at equal effort. "
        "3. Per plant: found if its best is above all 6 of its own coppers; rank; letters right."
    ),
    "walkthrough": (
        "1. Encipher a passage of English with a random alphabet and a random 23-letter key, the Beaufort way, with the known words in place. "
        "2. Make six shuffles of its carved letters that could still give the known letters. "
        "3. Start sixteen searches on the same text, each at its own boldness (temperature), each moving only between alphabets that keep the known letters right. "
        "4. After every round, let neighbouring searches swap their current alphabets when the cooler one would gain. "
        "5. Keep the best score seen; do the same on the six shuffles. "
        "6. The planted text counts as noticed if it beats all six shuffles; luck gives that one time in seven."
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
    import json
    from kryptos.scorer import english_score
    known = ctx.KNOWN
    m0120 = load_0120()
    L = 23
    rng = random.Random(139)
    lib()
    jobs, truth = [], {}
    deadline = ctx.deadline - 120
    plants = m0120.make_plants(known, L, rng, N_PLANTS)
    tried = 0
    for i, (pc, pt) in enumerate(plants):
        truth[i] = (pt, english_score(pt))
        jobs.append(("plant", L, i, pc, pt, rng.randrange(10 ** 9), deadline))
        got = 0
        while got < N_OWN:
            sh = list(pc); rng.shuffle(sh); sh = "".join(sh); tried += 1
            if m0120.decide(m0120.equations(sh, known, L), "B", rng)[0] == "fit":
                jobs.append(("own", L, i * 100 + got, sh, None, rng.randrange(10 ** 9), deadline)); got += 1
    if getattr(sys.modules.get(__name__), "_job", None) is not _job:
        m = types.ModuleType(__name__); m.__dict__.update(globals()); sys.modules[__name__] = m
    with mp.get_context("fork").Pool(8) as pool:
        res = pool.map(_job, jobs, chunksize=1)
    plant_rec = {}
    own = {i: [] for i in range(N_PLANTS)}
    done_all, all_ok = [], True
    for kind, L_, idx, sc, pt, alpha, k, agree, done, ok in res:
        done_all.append(done); all_ok = all_ok and ok
        if kind == "plant":
            plant_rec[idx] = {"score": round(sc, 4), "letters_right": agree, "true_score": round(truth[idx][1], 4), "restarts": done}
        else:
            own[idx // 100].append(round(sc, 4))
    k4_coppers = json.load(open(R0137))["bounds"]["coppers"]["23"]
    rows = []
    for i in range(N_PLANTS):
        p = plant_rec[i]
        o = sorted(own[i])
        p["own_coppers"] = o
        p["rank_among_own"] = 1 + sum(1 for x in o if x > p["score"])
        p["found_own"] = p["score"] > max(o)
        p["rank_among_k4_coppers_0137"] = 1 + sum(1 for x in k4_coppers if x > p["score"])
        p["recovered"] = (p["letters_right"] or 0) >= 90
        rows.append(p)
    found = sum(1 for p in rows if p["found_own"])
    bounds = {
        "family": "power check of 0137's climb: one unknown alphabet, Beaufort form, key length 23; each plant against shuffles of itself",
        "search": f"parallel tempering, {PT_RUNS} runs x {PT_R} replicas x {PT_ROUNDS} rounds x {PT_MOVES} moves per text, T {PT_T0}->{T1}",
        "plants": N_PLANTS, "own_coppers_per_plant": N_OWN, "shuffles_tried": tried,
        "restarts_done": {"min": min(done_all), "max": max(done_all)}, "c_decryption_checked": all_ok,
        "null_rate_found": round(1 / (N_OWN + 1), 4), "null_expected_found": round(N_PLANTS / (N_OWN + 1), 2),
        "bar": f"design 1's power at 23 stands if >= {OWN_BAR} of {N_PLANTS} plants beat all {N_OWN} of their own coppers",
        "plants_found_against_own": found, "passes_bar": found >= OWN_BAR,
        "plants_recovered": sum(1 for p in rows if p["recovered"]),
        "plants_found_against_0137_k4_coppers": sum(1 for p in rows if p["rank_among_k4_coppers_0137"] == 1),
        "rows": rows,
        "controls": "per plant, 6 shuffles of its own ciphertext that fit length 23 exactly (0119's decider, seed 139)",
    }
    notes = (f"plants beating all {N_OWN} own coppers: {found}/{N_PLANTS} (null {N_PLANTS / (N_OWN + 1):.1f}); "
             f"beating all 0137 K4 coppers: {bounds['plants_found_against_0137_k4_coppers']}/{N_PLANTS}; recovered {bounds['plants_recovered']}; "
             f"bar {'passed' if found >= OWN_BAR else 'failed'}")
    return {"candidates": [], "bounds": bounds, "notes": notes}


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
