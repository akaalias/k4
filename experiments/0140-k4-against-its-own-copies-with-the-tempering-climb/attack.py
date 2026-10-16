"""Experiment 0140. See program.md for the contract."""

EXPERIMENT = {
    "slug": "k4-against-its-own-copies-with-the-tempering-climb",
    "title": "F1.1 decided with F1.5's design 2: K4 against 12 scrambled copies of itself at key length 23 (one free alphabet, Beaufort form); design 2's power at length 26",
    "family": "1-keyed-periodic",
    "parent": "0139-parallel-tempering-climb-against-own-copies",
    "changed": (
        "F1.5 step 3 and F1.1. Design 2 (0139) noticed planted English against shuffles of itself 6 times in 8. Here it "
        "runs on K4 and on 12 shuffles of K4 that fit length 23 exactly, the like-for-like comparison 0138 showed is "
        "needed, so F1.1's Beaufort-23 cell gets a verdict at stated power. In the same run, design 2's power at length 26 "
        "(one check) is measured as in 0139: 6 planted texts, each against 6 fitting shuffles of itself."
    ),
    "hypothesis_expert": (
        "C27(c) (a tableau 'slightly different from the one on Kryptos', clue register), C1(b) (the table alone). Model as "
        "0137: one unknown alphabet on both sides, Beaufort form x(c_i) + x(p_i) = k[i mod L], L 23 (7 checks) and 26 (1 "
        "check), the only (form, length) pairs 0119 left. Search: 0139's compiled parallel tempering in the set where every "
        "check holds (10 runs x 16 replicas x 625 rounds x 1,000 moves, T 0.1 -> 0.002), full-text quadgram mean. L23: K4 and "
        "12 shuffles of K4 that fit exactly (0119's decider, seed 140). Measured power (0139): a planted Beaufort-23 text "
        "beat all 6 of its own shuffles 6 times in 8; against 12 the power is lower, about 0.5-0.75. Verdict rule fixed "
        "before the run: K4 above all 12 of its copies stops the queue for a replication with fresh copies; otherwise the "
        "cell is closed, sampled at the stated power (false alarm rate 1/13). L26 power: 6 plants (seed 1400) x 6 own "
        "fitting shuffles; bar 5 of 6; if met, K4 at 26 is the next run, otherwise the 26 cell stays blocked."
    ),
    "hypothesis_eli5": (
        "We finally have a search that, on planted messages, tells hidden English from its own scrambled letters about "
        "three times in four for one kind of cipher (one scrambled alphabet, a 23-letter key, used the Beaufort way). Now "
        "it runs on the carved text itself, against scrambled copies of the carved text. If the carved text were this "
        "kind of cipher, the search would usually rank it first. We also check whether the search works for a 26-letter "
        "key, where the known letters give only one check."
    ),
    "prediction": (
        "K4 is not above all 12 of its copies at length 23 (inside the range), so F1.1 Beaufort 23 closes, sampled at "
        "power about 0.6. At 26, fewer than 5 of 6 planted texts beat all their own copies (one check gives the climb "
        "little to hold), so the 26 cell stays blocked. No reading. One candidate (K4's best at 23) carried to the gates "
        "with its copies as controls; it will not pass."
    ),
    "method": (
        "1. Draw 12 shuffles of K4 that fit length 23 exactly; draw 6 planted texts at length 26 and 6 fitting shuffles "
        "of each. "
        "2. Run 0139's search on all 55 texts at equal effort. "
        "3. L23: K4's rank among its 12 copies. L26: plants beating all their own copies. "
        "4. Return K4's best L23 reading with the copies' English scores (free letters) as controls."
    ),
    "walkthrough": (
        "1. Write K4 in rows of 23; each column is one key slot; seven columns hold two known letters. "
        "2. Run sixteen searches side by side over alphabets that keep those seven pairs consistent, swapping states between bold and cautious searches, and keep the best English score. "
        "3. Shuffle K4's letters into 12 new orders that could still give the 24 known letters, and run the same search on each. "
        "4. If K4 were English enciphered this way, it would usually come first; if it comes anywhere inside the pack, this cell is closed at the measured strength. "
        "5. Do the same check of strength at 26 letters on planted English."
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
    from kryptos.scorer import english_score, free_text
    ct, known = ctx.K4, ctx.KNOWN
    m0120 = load_0120()
    rng = random.Random(140)
    lib()
    deadline = ctx.deadline - 120
    jobs, truth = [], {}
    assert m0120.decide(m0120.equations(ct, known, 23), "B")[0] == "fit"
    jobs.append(("k4", 23, 0, ct, None, rng.randrange(10 ** 9), deadline))
    got = 0
    while got < N_K4_COPPERS:
        sh = list(ct); rng.shuffle(sh); sh = "".join(sh)
        if m0120.decide(m0120.equations(sh, known, 23), "B", rng)[0] == "fit":
            jobs.append(("copper", 23, got, sh, None, rng.randrange(10 ** 9), deadline)); got += 1
    prng = random.Random(1400)
    for i, (pc, pt) in enumerate(m0120.make_plants(known, 26, prng, N_PLANTS26)):
        truth[i] = (pt, english_score(pt))
        jobs.append(("plant", 26, i, pc, pt, prng.randrange(10 ** 9), deadline))
        g = 0
        while g < N_OWN:
            sh = list(pc); prng.shuffle(sh); sh = "".join(sh)
            if m0120.decide(m0120.equations(sh, known, 26), "B", prng)[0] == "fit":
                jobs.append(("own", 26, i * 100 + g, sh, None, prng.randrange(10 ** 9), deadline)); g += 1
    jobs.sort(key=lambda j: j[0] != "k4")
    if getattr(sys.modules.get(__name__), "_job", None) is not _job:
        m = types.ModuleType(__name__); m.__dict__.update(globals()); sys.modules[__name__] = m
    with mp.get_context("fork").Pool(8) as pool:
        res = pool.map(_job, jobs, chunksize=1)
    k4, cop, plants, own = None, [], {}, {i: [] for i in range(N_PLANTS26)}
    done_all, all_ok = [], True
    for kind, L_, idx, sc, pt, alpha, k, agree, done, ok in res:
        done_all.append(done); all_ok = all_ok and ok
        if kind == "k4":
            k4 = {"score": round(sc, 4), "plaintext": pt, "alphabet": alpha, "key": k, "english_free": round(english_score(free_text(pt)), 4), "runs": done}
        elif kind == "copper":
            cop.append({"score": round(sc, 4), "english_free": round(english_score(free_text(pt)), 4), "runs": done})
        elif kind == "plant":
            plants[idx] = {"score": round(sc, 4), "letters_right": agree, "true_score": round(truth[idx][1], 4), "runs": done}
        else:
            own[idx // 100].append(round(sc, 4))
    cs = sorted(c["score"] for c in cop)
    k4_rank = 1 + sum(1 for c in cs if c > k4["score"])
    rows = []
    for i in range(N_PLANTS26):
        p = plants[i]; o = sorted(own[i])
        p.update({"own_coppers": o, "rank_among_own": 1 + sum(1 for x in o if x > p["score"]), "found_own": p["score"] > max(o),
                  "recovered": (p["letters_right"] or 0) >= 90})
        rows.append(p)
    found26 = sum(1 for p in rows if p["found_own"])
    stop = k4_rank == 1
    bounds = {
        "family": "one unknown alphabet on both sides, Beaufort form, no move: K4 at key length 23 against its own copies; design 2's power at 26",
        "search": f"parallel tempering (0139), {PT_RUNS} runs x {PT_R} replicas x {PT_ROUNDS} rounds x {PT_MOVES} moves per text, T {PT_T0}->{T1}",
        "not_exhaustive": True,
        "runs_done": {"min": min(done_all), "max": max(done_all)}, "c_decryption_checked": all_ok,
        "L23": {"k4": k4, "coppers": cs, "k4_rank_of_13": k4_rank, "k4_above_all_copies": stop,
                "power_measured_0139": "6 of 8 planted texts beat all 6 own copies", "false_alarm_rate": round(1 / 13, 3)},
        "L26_power": {"plants": N_PLANTS26, "own_coppers_per_plant": N_OWN, "found": found26, "bar": f">= {BAR26} of {N_PLANTS26}",
                      "passes_bar": found26 >= BAR26, "null_expected": round(N_PLANTS26 / (N_OWN + 1), 2), "rows": rows},
        "stop_queue": stop,
        "controls": f"{N_K4_COPPERS} shuffles of K4 that fit length 23 exactly (0119's decider, seed 140); at 26 each plant's own fitting shuffles (seed 1400)",
    }
    cands = [{"plaintext": k4["plaintext"], "key": {"alphabet": k4["alphabet"], "shifts": k4["key"], "form": "beaufort"},
              "key_description": f"Beaufort form, one alphabet {k4['alphabet']} on both sides, key length 23",
              "notes": "best of design 2 on K4"}]
    notes = (f"L23: K4 {k4['score']:.3f}, rank {k4_rank} of 13 among its own copies ({cs[0]:.3f} to {cs[-1]:.3f}); stop queue {stop}. "
             f"L26 power: {found26}/{N_PLANTS26} plants beat all {N_OWN} own copies (null {N_PLANTS26 / (N_OWN + 1):.2f}, bar {BAR26}).")
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
