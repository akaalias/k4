"""Experiment 0148. See program.md for the contract."""

EXPERIMENT = {
    "slug": "k1-k2-system-with-a-slip-at-33",
    "title": "F1.6, the revived cell: K1 and K2's own system (one free alphabet, added form) at key length 19 with the carved S at place 33 taken as a slip; design 2's power on planted texts and K4 against its copies",
    "family": "1-keyed-periodic",
    "parent": "0147-one-carved-letter-wrong-through-the-free-alphabet-tests",
    "changed": (
        "F1.6. 0147 found that replacing the carved S at 33 (S under S) revives K1 and K2's system with a free alphabet at "
        "key length 19, for 25 of the possible replacements, the one cell where K4 stood above every scrambled copy in "
        "that model (25 against at most 23; inside the multiple-comparison null overall). The exact test cannot judge it "
        "further. Here place 33's carved letter is treated as unknown (its equation dropped, the message letter S kept), "
        "and 0139's English decider, rewritten for the added form, judges the cell: power on 5 planted texts against "
        "copies of themselves, and K4 against 12 copies of itself, in one run."
    ),
    "hypothesis_expert": (
        "C17(b), family G (a slip of the chisel, as K2's dropped letter and UNDERGRUUND), C27(c), C1(b): K1 and K2 are "
        "Quagmire III on the KRYPTOS alphabet (knowledge/01-facts.md); with a free alphabet the added form x(c) = x(p) + "
        "k[i mod L] dies at every length 1-26 only because S under S (33) and K under K (74) force key 0 in shared slots "
        "(0119). Model here: same, L 19, place 33's carved letter unknown (23 equations; its message letter is S). "
        "Search: 0139's compiled parallel tempering, check-keeping moves, added form, 10 runs x 16 replicas x 625 rounds x "
        "1,000 moves per text. Power: 5 planted texts (Carter windows, random alphabet and key, added form, the carved "
        "letter at 33 then replaced by a random other letter; seed 148), each against 4 kept-place copies (carved letters "
        "kept at the 24 known places, other 73 shuffled; seed 1481); bar fixed before the run: at least 4 of 5 beat all "
        "their copies (luck 0.2 each). K4 against 12 kept-place copies (seed 1482); K4 above all 12 stops the queue for a "
        "replication; otherwise, if the bar is met, the cell closes sampled at that power, and if not, it stays blocked."
    ),
    "hypothesis_eli5": (
        "K1 and K2 were made with the table and a scrambled alphabet; the same method on K4 is ruled out only because "
        "two carved letters equal the message letters above them. If the S at place 33 is a slip of the chisel, the "
        "method comes back to life at a key length of 19. We let the search that tells hidden English from scrambled "
        "letters judge that one case, after checking on planted messages that it can."
    ),
    "prediction": (
        "The decider has power here (at least 4 of 5 planted texts beat their copies: 23 equations, 4 checks); K4 sits "
        "inside its 12 copies, so the cell closes. No reading."
    ),
    "method": (
        "1. Compile the added-form search; check its decryption against Python. "
        "2. 5 planted texts with a slip at 33, 4 kept-place copies each; K4 and 12 kept-place copies. "
        "3. The search on all 38 texts, place 33 left out of the equations and read as S. "
        "4. Plants beating all their copies; K4's rank among its copies."
    ),
    "walkthrough": (
        "1. Write K4 in rows of 19; each column is one key slot. "
        "2. Leave place 33 out: its carved S is taken as a slip. "
        "3. For every other known letter: place(carved) = place(known) + key value of its column, in one unknown alphabet. "
        "4. Search alphabets that keep these equations, sixteen searches side by side, scoring the whole text as English, with S at 33. "
        "5. Do the same on copies of K4 that keep the known places' carved letters and shuffle the rest, and on planted English."
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
N_PLANTS = 5
RESTARTS = 1000
ITERS = 100000
CHUNK = 50
T0, T1 = 0.05, 0.002
FOUND_BAR = 9
SLIP = 33
OVR = {33: "S"}
N_K4_COPPERS = 12
N_PLANTS26 = 6
BAR26 = 5
N_OWN = 4
OWN_BAR = 4
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
static int SG = 1, NOVR = 0, OVRP[32], OVRL[32];
void set_form(int sg, int n, const int *op, const int *ol) { SG = sg; NOVR = n; for (int i = 0; i < n; i++) { OVRP[i] = op[i]; OVRL[i] = ol[i]; } }

static int checks_ok(const int *x) {
    for (int j = 0; j < NCH; j++) if (((x[CH[j][0]] + SG * x[CH[j][1]] - x[CH[j][2]] - SG * x[CH[j][3]]) % 26 + 26) % 26) return 0;
    return 1;
}

static double decode_score(const int *x, const int *kf, int *pt) {
    int inv[26], k[64];
    for (int le = 0; le < 26; le++) inv[x[le]] = le;
    for (int j = 0; j < NREP; j++) k[REPS[j]] = ((x[REPC[j]] + SG * x[REPP[j]]) % 26 + 26) % 26;
    for (int j = 0; j < NFREE; j++) k[FREE[j]] = kf[j];
    for (int i = 0; i < N; i++) pt[i] = inv[((SG * (k[i % L] - x[C[i]])) % 26 + 26) % 26];
    for (int j = 0; j < NOVR; j++) pt[OVRP[j]] = OVRL[j];
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
            if (((a + SG * b - c - SG * d) % 26 + 26) % 26) good = 0;
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
            if (((x[CH[j][0]] + SG * x[CH[j][1]] - x[CH[j][2]] - SG * x[CH[j][3]]) % 26 + 26) % 26)
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
            for (int j = 0; j < NREP; j++) k[REPS[j]] = ((rx[REPC[j]] + SG * rx[REPP[j]]) % 26 + 26) % 26;
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
                        for (int j = 0; j < NREP; j++) k[REPS[j]] = ((x[REPC[j]] + SG * x[REPP[j]]) % 26 + 26) % 26;
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
    KP = (ctypes.c_int * 24)(*([q - 1 for q in kp] + [0] * (24 - len(kp))))
    KL = (ctypes.c_int * 24)(*([ord(known[q]) - 65 for q in kp] + [0] * (24 - len(kp))))
    L_.setup(_LIB["tab"], CT, N, L, KP, KL, len(kp))
    OP = [q - 1 for q in OVR]; OL = [ord(OVR[q]) - 65 for q in OVR]
    L_.set_form(-1, len(OP), (ctypes.c_int * 8)(*(OP + [0] * (8 - len(OP)))), (ctypes.c_int * 8)(*(OL + [0] * (8 - len(OL)))))
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


def added_decrypt(ct, alpha, k):
    pos = {ch: i for i, ch in enumerate(alpha)}
    out = [alpha[(pos[ch] - k[i % len(k)]) % 26] for i, ch in enumerate(ct)]
    for q, a in OVR.items():
        out[q - 1] = a
    return "".join(out)


def added_encrypt(pt, alpha, k):
    pos = {ch: i for i, ch in enumerate(alpha)}
    return "".join(alpha[(pos[ch] + k[i % len(k)]) % 26] for i, ch in enumerate(pt))


def beaufort_decrypt(ct, alpha, k):
    pos = {ch: i for i, ch in enumerate(alpha)}
    return "".join(alpha[(k[i % len(k)] - pos[ch]) % 26] for i, ch in enumerate(ct))


def beaufort_encrypt(pt, alpha, k):
    pos = {ch: i for i, ch in enumerate(alpha)}
    return "".join(alpha[(k[i % len(k)] - pos[ch]) % 26] for i, ch in enumerate(pt))


def _job(args):
    kind, L, idx, text, truth, seed, deadline = args
    from kryptos.facts import KNOWN
    kn = {q: a for q, a in KNOWN.items() if q != SLIP}
    sc, pt, alpha, k, done = climb_text(text, kn, L, seed, RESTARTS, deadline)
    agree = sum(1 for a_, b_ in zip(pt, truth) if a_ == b_) if (pt and truth) else None
    ok = (pt is not None and added_decrypt(text, alpha, k) == pt)
    return kind, L, idx, sc, pt, alpha, k, agree, done, ok


def run(ctx):
    import multiprocessing as mp
    import sys
    import types
    import re
    from kryptos.scorer import english_score, free_text
    from kryptos.facts import STANDARD_ALPHABET as STD
    ct, known = ctx.K4, ctx.KNOWN
    lib()
    deadline = ctx.deadline - 90
    L = 19
    kidx = set(q - 1 for q in known)
    free = [i for i in range(N) if i not in kidx]

    def kept_copy(text, r):
        letters = [text[j] for j in free]; r.shuffle(letters)
        cp = list(text)
        for j, ch in zip(free, letters):
            cp[j] = ch
        return "".join(cp)
    src = re.sub("[^A-Z]", "", open(load_0120().CARTER, errors="ignore").read().upper())
    prng, crng, krng = random.Random(148), random.Random(1481), random.Random(1482)
    jobs, truth = [], {}
    for i in range(N_PLANTS):
        s0 = prng.randrange(20000, len(src) - 200)
        pt = list(src[s0:s0 + N])
        for q, a in known.items():
            pt[q - 1] = a
        pt = "".join(pt)
        al = list(STD); prng.shuffle(al); al = "".join(al)
        k = [prng.randrange(26) for _ in range(L)]
        pc = list(added_encrypt(pt, al, k))
        pc[SLIP - 1] = prng.choice([c for c in STD if c != pc[SLIP - 1]])
        pc = "".join(pc)
        assert added_decrypt(pc, al, k) == pt
        truth[i] = pt
        jobs.append(("plant", L, i, pc, pt, prng.randrange(10 ** 9), deadline))
        for g in range(N_OWN):
            jobs.append(("own", L, i * 100 + g, kept_copy(pc, crng), None, crng.randrange(10 ** 9), deadline))
    jobs.append(("k4", L, 0, ct, None, krng.randrange(10 ** 9), deadline))
    for g in range(N_K4_COPPERS):
        jobs.append(("copper", L, g, kept_copy(ct, krng), None, krng.randrange(10 ** 9), deadline))
    if getattr(sys.modules.get(__name__), "_job", None) is not _job:
        m = types.ModuleType(__name__); m.__dict__.update(globals()); sys.modules[__name__] = m
    with mp.get_context("fork").Pool(8) as pool:
        res = pool.map(_job, jobs, chunksize=1)
    plants, own, k4, cop = {}, {i: [] for i in range(N_PLANTS)}, None, []
    done_all, all_ok = [], True
    for kind, L_, idx, sc, pt, alpha, k, agree, done, ok in res:
        done_all.append(done); all_ok = all_ok and ok
        if kind == "plant":
            plants[idx] = {"score": round(sc, 4), "letters_right": agree}
        elif kind == "own":
            own[idx // 100].append(round(sc, 4))
        elif kind == "k4":
            k4 = {"score": round(sc, 4), "plaintext": pt, "alphabet": alpha, "key": k, "english_free": round(english_score(free_text(pt)), 4)}
        else:
            cop.append({"score": round(sc, 4), "english_free": round(english_score(free_text(pt)), 4)})
    rows = []
    for i in range(N_PLANTS):
        p = plants[i]; o = sorted(own[i])
        p.update({"own_copies": o, "rank_among_own": 1 + sum(1 for x in o if x > p["score"]), "found_own": p["score"] > max(o),
                  "recovered": (p["letters_right"] or 0) >= 90})
        rows.append(p)
    found = sum(1 for p in rows if p["found_own"])
    cs = sorted(c["score"] for c in cop)
    rank = 1 + sum(1 for c in cs if c > k4["score"])
    stop = rank == 1
    bounds = {
        "family": "one free alphabet, added form (K1/K2's system), key length 19, carved letter at place 33 taken as a slip (equation dropped, S kept)",
        "search": f"parallel tempering (0139) in the added form, {PT_RUNS} runs x {PT_R} replicas x {PT_ROUNDS} rounds x {PT_MOVES} moves per text",
        "not_exhaustive": True, "runs_done": {"min": min(done_all), "max": max(done_all)}, "c_decryption_checked": all_ok,
        "power": {"plants": N_PLANTS, "copies_each": N_OWN, "found": found, "bar": f">= {OWN_BAR} of {N_PLANTS}", "passes_bar": found >= OWN_BAR,
                  "null_expected": round(N_PLANTS / (N_OWN + 1), 2), "rows": rows},
        "k4": k4, "k4_copies": cs, "k4_rank_of_13": rank, "stop_queue": stop,
        "controls": "kept-place copies (carved letters kept at the 24 known places, other 73 shuffled): 4 per plant (seed 1481), 12 for K4 (seed 1482)",
    }
    notes = f"power {found}/{N_PLANTS} (bar {OWN_BAR}, null {N_PLANTS / (N_OWN + 1):.2f}); K4 {k4['score']:.3f} rank {rank} of 13 ({cs[0]:.3f} to {cs[-1]:.3f}); stop {stop}"
    cands = [{"plaintext": k4["plaintext"], "key": {"alphabet": k4["alphabet"], "shifts": k4["key"], "form": "added", "slip": SLIP},
              "key_description": f"added form, one alphabet {k4['alphabet']}, key length 19, carved letter at 33 read as a slip", "notes": "best of design 2 on K4"}]
    return {"candidates": cands, "bounds": bounds, "notes": notes, "controls": [c["english_free"] for c in cop]}


def encrypt(plaintext, key):
    """Added form on one alphabet; the carved letter at the slip place is the copper's (its equation was dropped)."""
    from kryptos.facts import K4
    out = list(added_encrypt(plaintext, key["alphabet"], key["shifts"]))
    out[key.get("slip", SLIP) - 1] = K4[key.get("slip", SLIP) - 1]
    return "".join(out)


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
