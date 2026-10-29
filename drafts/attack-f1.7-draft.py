"""Experiment (F1.7, D2). See program.md for the contract."""

EXPERIMENT = {
    "slug": "f1.7-autokey-on-one-free-alphabet-decided-by-an-english-climb",
    "title": "F1.7 and D2: autokey on one free alphabet, every lag K4 fits (ciphertext and plaintext autokey, three forms), each decided by an alphabet climb against copies climbed one at a time",
    "family": "1-keyed-periodic",
    "parent": "0149-autokey-on-one-unknown-alphabet",
    "changed": (
        "F1.7 (D2's last re-cost, issue #77). 0149 decided autokey on one unknown alphabet exactly and left the lags K4 "
        "fits (103 cells over ciphertext/plaintext autokey and three forms) blocked by cost at F1.5's design-2 decider "
        "(about an hour per cell). Under autokey the key is the text itself, so the alphabet alone (plus, for plaintext "
        "autokey, one primer letter per chain the known letters do not reach) fixes the reading: a climb over the "
        "alphabet is much cheaper than design 2's alphabet-and-key tempering. Here that climb is written (compiled), "
        "its power measured on plants drawn from K4's own fitting cells, and every one of K4's cells decided against "
        "copies climbed one at a time, in the same run."
    ),
    "hypothesis_expert": (
        "C11a (NSA 1992: 'plain-text auto-key'; NSA 2007: plaintext and ciphertext autokey tried without cribs), C27(c) "
        "(any alphabet), C1(b). Model as 0149: x a bijection letters -> Z26; forms V x(c) = x(p) + x(k), B x(c) = x(k) - "
        "x(p), R x(c) = x(p) - x(k); k_i = c_{i-L} (ciphertext autokey) or p_{i-L} (plaintext autokey), primer free. "
        "Ciphertext autokey: the reading at places L+1..97 is fixed by x alone, the first L letters by single-use primer "
        "letters (open: not scored). Plaintext autokey: a chain i, i+L, i+2L... is fixed by x and its first letter; a chain "
        "holding a known place has that letter forced (back-propagated), the others are free and climbed. The full chain "
        "condition is enforced (0149's equations used only adjacent known pairs), so a cell 0149 called fit may turn out "
        "dead here; that is reported. Copies: shuffles of the text that 0149's exact decider fits in the same cell."
    ),
    "hypothesis_eli5": (
        "In an autokey cipher the message (or the ciphertext) becomes its own key after a short starter. With a "
        "scrambled alphabet nobody knows, about a hundred settings agree with the 24 known letters. For each we search "
        "for the scrambled alphabet that makes K4 read most like English, and do the same on scrambled copies of K4 "
        "that agree with the known letters equally well. The real answer should read better than all its copies."
    ),
    "prediction": (
        "Low power, measured: ciphertext-autokey plants found at most 1 in 4 (the desk climbs never reached a plant's own "
        "score there); plaintext-autokey plants about 1 in 3 overall, better at short lags where the checks pin the alphabet. "
        "Some of 0149's 103 cells die under the full chain equations. K4 inside its copies: cells beating all 12 copies within "
        "the binomial range for 1/13. Zero candidates."
    ),
    "method": (
        "1. Cells: every (kind, form, lag) where K4 fits the exact decider, now with plaintext autokey's chains in full "
        "(consecutive known places of one chain linked through the carved letters between them; 0149 used only pairs L apart), "
        "solved by 0149's exact solver. "
        "2. Per cell (one job, own seed): climb K4 once; then draw shuffles of K4 that fit the same cell, climb each, stop at "
        "the first at or above K4; at most 12, escalated to 100 where K4 beats all 12. "
        "3. Climb: plaintext autokey at lags up to 12, check-keeping tempering from the exact witness with repair swaps (0139's "
        "move); every other cell, tempering with a fixed penalty per known letter out of place, recording only states with all 24 in place. "
        "Ciphertext autokey readings are scored on places L+1 to 97 (the first L come from single-use primer letters). "
        "4. Plants: per kind 12 clean and 12 Sanborn-style messages enciphered on cells drawn from K4's, through the same decision without escalation; power per kind and per climb. "
        "5. Verdict: cells where K4 beats all 12 copies against Binomial(n, 1/13); the top readings listed."
    ),
    "walkthrough": (
        "1. Pick a cell: plaintext autokey, Beaufort form, lag 33, with an unknown scrambled alphabet. "
        "2. In that system each plain letter becomes the key 33 places later, so once the alphabet is fixed, a chain of places 33 apart is fixed by its first letter. "
        "3. Chains holding a known letter are fixed by it; the others get a free starting letter. "
        "4. Search alphabets (and free starts) for the most English-looking reading that keeps all 24 known letters. "
        "5. Shuffle K4 until a shuffle also fits the cell, and search it the same way; repeat up to 12 times, stopping when a shuffle reads as well as K4. "
        "6. Count the cells where K4 beat all 12; chance gives about one in 13."
    ),
    "expected_minutes": 60,
}

import ctypes
import os
import random
import subprocess
import tempfile
import time
from pathlib import Path

N = 97
ROOT = Path(__file__).resolve().parent
BASE, ESC = 12, 100
PLANTS = 12                      # per kind and class: 12 clean + 12 Sanborn-style per kind
RESTARTS, MOVES, T0, T1 = 20, 500000, 0.15, 0.003
MODE, PT_R, PT_ROUNDS, PT_MOVES = "keep", 16, 300, 1000
K_R, K_ROUNDS, K_MOVES, K_T0, K_T1 = 16, 300, 1000, 0.1, 0.002   # check-keeping tempering, 0140's temperatures
PEN = 0.04                       # "sa" only: per known place out of place, raised 50-fold through each run
PT_PEN = 0.6                     # "pt": fixed penalty per known place out of place (desk tests 2026-10-29: 0.2 loses the check-keeping states, 2.0 no better)
SHORT = 12                       # plaintext autokey at lags up to SHORT: check-keeping tempering ("keep"); every other cell "pt"
_MODS = {}

C_SOURCE = r"""
#include <stdint.h>
#include <math.h>
static const double *TAB; static int N, L, KIND, FORM, C[128], NK, KP[24], KL[24], FIRSTK[128], S, KIDX[128];
static uint64_t RS;
static inline uint64_t rnd(void) { RS ^= RS << 13; RS ^= RS >> 7; RS ^= RS << 17; return RS; }
static inline int md(int v) { v %= 26; return v < 0 ? v + 26 : v; }
static inline int dec(int c, int k) { return FORM == 0 ? md(c - k) : FORM == 1 ? md(k - c) : md(c + k); }
static inline int keyof(int c, int p) { return FORM == 0 ? md(c - p) : FORM == 1 ? md(p + c) : md(p - c); }
int setup(const double *tab, const int *ct, int n, int l, int kind, int form, const int *kp, const int *kl, int nk) {
    TAB = tab; N = n; L = l; KIND = kind; FORM = form; NK = nk;
    for (int i = 0; i < n; i++) C[i] = ct[i];
    for (int i = 0; i < 128; i++) KIDX[i] = -1;
    for (int j = 0; j < nk; j++) { KP[j] = kp[j]; KL[j] = kl[j]; KIDX[kp[j]] = j; }
    for (int r = 0; r < l; r++) FIRSTK[r] = -1;
    if (kind == 1) for (int j = 0; j < nk; j++) { int r = kp[j] % l; if (FIRSTK[r] < 0 || kp[j] < kp[FIRSTK[r]]) FIRSTK[r] = j; }
    S = kind == 0 ? l : 0;
    return 0;
}
// fill pt (-1 where open); return the number of known places out of place
static int decode(const int *x, const int *inv, const int *prim, int *pt) {
    if (KIND == 0) {
        for (int i = 0; i < L && i < N; i++) pt[i] = -1;
        for (int i = L; i < N; i++) pt[i] = inv[dec(x[C[i]], x[C[i - L]])];
    } else {
        for (int r = 0; r < L && r < N; r++) {
            if (FIRSTK[r] < 0) { pt[r] = prim[r]; continue; }
            int q = KP[FIRSTK[r]], v = x[KL[FIRSTK[r]]];
            while (q >= L) { v = keyof(x[C[q]], v); q -= L; }
            pt[r] = inv[v];
        }
        for (int i = L; i < N; i++) pt[i] = inv[dec(x[C[i]], x[pt[i - L]])];
    }
    int bad = 0;
    for (int j = 0; j < NK; j++) if (pt[KP[j]] >= 0 && pt[KP[j]] != KL[j]) bad++;
    return bad;
}
// the number of known places out of place, without decoding the rest (for the check-keeping moves)
static int nbad(const int *x) {
    int bad = 0;
    if (KIND == 0) {
        for (int j = 0; j < NK; j++) { int q = KP[j]; if (q >= L && dec(x[C[q]], x[C[q - L]]) != x[KL[j]]) bad++; }
        return bad;
    }
    for (int j = 0; j < NK; j++) {               // walk each chain from its first known place to the later ones
        int q = KP[j], r = q % L;
        if (FIRSTK[r] != j) continue;
        int v = x[KL[j]];
        for (int i = q + L; i < N; i += L) {
            v = dec(x[C[i]], v);
            if (KIDX[i] >= 0 && v != x[KL[KIDX[i]]]) bad++;
        }
    }
    return bad;
}
static double score(const int *pt) {
    double s = 0; int n = 0;
    for (int i = S; i + 3 < N; i++) { s += TAB[((pt[i] * 26 + pt[i + 1]) * 26 + pt[i + 2]) * 26 + pt[i + 3]]; n++; }
    return n ? s / n : -99;
}
// R restarts of M moves from the start alphabet w (letter -> value); returns the best mean score among states with
// every known place right (or -99 if none), its reading in bp (-1 open), its alphabet in bx
double climb(uint64_t seed, const int *w, int R, int M, double t0, double t1, double pen, int *bp, int *bx) {
    RS = seed * 2862933555777941757ULL + 3037000493ULL; if (!RS) RS = 1;
    double best = -99; int pt[128];
    int nfree = 0, fr[64];
    if (KIND == 1) for (int r = 0; r < L; r++) if (FIRSTK[r] < 0) fr[nfree++] = r;
    for (int run = 0; run < R; run++) {
        int x[26], inv[26], prim[64];
        for (int i = 0; i < 26; i++) x[i] = w[i];
        if (run > 0) for (int t = 25; t > 0; t--) { int a = rnd() % (t + 1), z = x[a]; x[a] = x[t]; x[t] = z; }
        for (int i = 0; i < 26; i++) inv[x[i]] = i;
        for (int r = 0; r < L && r < 64; r++) prim[r] = rnd() % 26;
        int bad = decode(x, inv, prim, pt);
        double pen_now = pen;
        double cur = score(pt) - pen_now * bad;
        for (int m = 0; m < M; m++) {
            double T = t0 + (t1 - t0) * m / M;
            if ((m & 1023) == 0) { double np = pen * pow(50.0, (double)m / M); cur += (pen_now - np) * bad; pen_now = np; }
            int mv = (nfree && (rnd() % 5 == 0)) ? 1 : 0, a = 0, b = 0, old = 0, r = 0;
            if (mv == 0) { a = rnd() % 26; b = rnd() % 26; if (a == b) continue; int z = x[a]; x[a] = x[b]; x[b] = z; inv[x[a]] = a; inv[x[b]] = b; }
            else { r = fr[rnd() % nfree]; old = prim[r]; prim[r] = rnd() % 26; }
            int nb = decode(x, inv, prim, pt);
            double sc = score(pt) - pen_now * nb;
            if (sc >= cur || exp((sc - cur) / T) * 4294967296.0 > (double)(rnd() & 0xffffffffULL)) {
                cur = sc; bad = nb;
                if (nb == 0 && sc > best) { best = sc; for (int i = 0; i < N; i++) bp[i] = pt[i]; for (int i = 0; i < 26; i++) bx[i] = x[i]; }
            } else if (mv == 0) { int z = x[a]; x[a] = x[b]; x[b] = z; inv[x[a]] = a; inv[x[b]] = b; }
            else prim[r] = old;
        }
    }
    return best;
}
// parallel tempering: R replicas at geometric temperatures t0 > ... > t1, ROUNDS rounds of M moves each, then swaps
double ptemper(uint64_t seed, const int *w, int R, int ROUNDS, int M, double t0, double t1, double pen, int *bp, int *bx) {
    RS = seed * 2862933555777941757ULL + 3037000493ULL; if (!RS) RS = 1;
    static int X[32][26], INV[32][26], PR[32][64], PT[128];
    double CUR[32], T[32], best = -99;
    int nfree = 0, fr[64];
    if (KIND == 1) for (int r = 0; r < L; r++) if (FIRSTK[r] < 0) fr[nfree++] = r;
    for (int j = 0; j < R; j++) {
        T[j] = R > 1 ? t0 * pow(t1 / t0, (double)j / (R - 1)) : t1;
        for (int i = 0; i < 26; i++) X[j][i] = w[i];
        if (j > 0) for (int t = 25; t > 0; t--) { int a = rnd() % (t + 1), z = X[j][a]; X[j][a] = X[j][t]; X[j][t] = z; }
        for (int i = 0; i < 26; i++) INV[j][X[j][i]] = i;
        for (int r = 0; r < L && r < 64; r++) PR[j][r] = rnd() % 26;
        int nb = decode(X[j], INV[j], PR[j], PT);
        CUR[j] = score(PT) - pen * nb;
    }
    for (int round = 0; round < ROUNDS; round++) {
        for (int j = 0; j < R; j++) {
            int *x = X[j], *inv = INV[j], *prim = PR[j];
            for (int m = 0; m < M; m++) {
                int mv = (nfree && (rnd() % 5 == 0)) ? 1 : 0, a = 0, b = 0, old = 0, r = 0;
                if (mv == 0) { a = rnd() % 26; b = rnd() % 26; if (a == b) continue; int z = x[a]; x[a] = x[b]; x[b] = z; inv[x[a]] = a; inv[x[b]] = b; }
                else { r = fr[rnd() % nfree]; old = prim[r]; prim[r] = rnd() % 26; }
                int nb = decode(x, inv, prim, PT);
                double sc = score(PT) - pen * nb;
                if (sc >= CUR[j] || exp((sc - CUR[j]) / T[j]) * 4294967296.0 > (double)(rnd() & 0xffffffffULL)) {
                    CUR[j] = sc;
                    if (nb == 0 && sc > best) { best = sc; for (int i = 0; i < N; i++) bp[i] = PT[i]; for (int i = 0; i < 26; i++) bx[i] = x[i]; }
                } else if (mv == 0) { int z = x[a]; x[a] = x[b]; x[b] = z; inv[x[a]] = a; inv[x[b]] = b; }
                else prim[r] = old;
            }
        }
        for (int j = 0; j + 1 < R; j++) {
            double d = (CUR[j + 1] - CUR[j]) * (1.0 / T[j] - 1.0 / T[j + 1]);
            if (d >= 0 || exp(d) * 4294967296.0 > (double)(rnd() & 0xffffffffULL)) {
                int tmp[26]; double c;
                for (int i = 0; i < 26; i++) { tmp[i] = X[j][i]; X[j][i] = X[j + 1][i]; X[j + 1][i] = tmp[i]; }
                for (int i = 0; i < 26; i++) { tmp[i] = INV[j][i]; INV[j][i] = INV[j + 1][i]; INV[j + 1][i] = tmp[i]; }
                for (int i = 0; i < 64; i++) { int z = PR[j][i]; PR[j][i] = PR[j + 1][i]; PR[j + 1][i] = z; }
                c = CUR[j]; CUR[j] = CUR[j + 1]; CUR[j + 1] = c;
            }
        }
    }
    return best;
}
// check-keeping tempering (as 0139/0140): each replica first reaches a state with every known place right (annealing
// on the count of known places out of place, from the witness or a shuffle), then moves are accepted only if every
// known place stays right; Metropolis on the quadgram mean, replica swaps between neighbouring temperatures.
// Returns the best score among kept states (-99 if no replica reached one), its reading and alphabet.
double keep(uint64_t seed, const int *w, int R, int ROUNDS, int M, double t0, double t1, int *bp, int *bx, int *nlive) {
    RS = seed * 2862933555777941757ULL + 3037000493ULL; if (!RS) RS = 1;
    static int X[32][26], INV[32][26], PR[32][64], PT[128], LIVE[32];
    double CUR[32], T[32], best = -99;
    int nfree = 0, fr[64], live = 0;
    if (KIND == 1) for (int r = 0; r < L; r++) if (FIRSTK[r] < 0) fr[nfree++] = r;
    for (int j = 0; j < R; j++) {
        T[j] = R > 1 ? t0 * pow(t1 / t0, (double)j / (R - 1)) : t1;
        int *x = X[j], *inv = INV[j], *prim = PR[j];
        for (int i = 0; i < 26; i++) x[i] = w[i];
        for (int i = 0; i < 26; i++) inv[x[i]] = i;
        for (int r = 0; r < L && r < 64; r++) prim[r] = rnd() % 26;
        int bad = decode(x, inv, prim, PT);
        for (int m = 0; m < 400000 && bad > 0; m++) {
            int a = rnd() % 26, b = rnd() % 26; if (a == b) continue;
            int z = x[a]; x[a] = x[b]; x[b] = z; inv[x[a]] = a; inv[x[b]] = b;
            int nb = decode(x, inv, prim, PT);
            if (nb <= bad || exp(-(nb - bad) / 0.4) * 4294967296.0 > (double)(rnd() & 0xffffffffULL)) bad = nb;
            else { z = x[a]; x[a] = x[b]; x[b] = z; inv[x[a]] = a; inv[x[b]] = b; }
        }
        LIVE[j] = bad == 0; live += LIVE[j];
        CUR[j] = bad == 0 ? score(PT) : -99;
        if (bad == 0 && CUR[j] > best) { best = CUR[j]; for (int i = 0; i < N; i++) bp[i] = PT[i]; for (int i = 0; i < 26; i++) bx[i] = x[i]; }
    }
    *nlive = live;
    if (!live) return -99;
    for (int j = 0; j < R; j++) if (!LIVE[j]) {          // dead replicas copy a live one
        int s = j; while (!LIVE[s]) s = (s + 1) % R;
        for (int i = 0; i < 26; i++) { X[j][i] = X[s][i]; INV[j][i] = INV[s][i]; }
        for (int i = 0; i < 64; i++) PR[j][i] = PR[s][i];
        CUR[j] = CUR[s];
    }
    for (int round = 0; round < ROUNDS; round++) {
        for (int j = 0; j < R; j++) {
            int *x = X[j], *inv = INV[j], *prim = PR[j];
            for (int m = 0; m < M; m++) {
                int mv = (nfree && (rnd() % 5 == 0)) ? 1 : 0, a = 0, b = 0, a2 = -1, b2 = -1, old = 0, r = 0, z;
                if (mv == 0) {
                    a = rnd() % 26; b = rnd() % 26; if (a == b) continue;
                    z = x[a]; x[a] = x[b]; x[b] = z;
                    if (nbad(x)) {                     // repair: a second swap that restores every check (as 0139)
                        int opts[325][2], no = 0;
                        for (int m1 = 0; m1 < 26; m1++) for (int m2 = m1 + 1; m2 < 26; m2++) {
                            z = x[m1]; x[m1] = x[m2]; x[m2] = z;
                            if (!nbad(x)) { opts[no][0] = m1; opts[no][1] = m2; no++; }
                            z = x[m1]; x[m1] = x[m2]; x[m2] = z;
                        }
                        if (!no) { z = x[a]; x[a] = x[b]; x[b] = z; continue; }
                        int pick = rnd() % no; a2 = opts[pick][0]; b2 = opts[pick][1];
                        z = x[a2]; x[a2] = x[b2]; x[b2] = z;
                    }
                    for (int i = 0; i < 26; i++) inv[x[i]] = i;
                }
                else { r = fr[rnd() % nfree]; old = prim[r]; prim[r] = rnd() % 26; }
                int nb = decode(x, inv, prim, PT);
                double sc = nb ? -1e9 : score(PT);
                if (nb == 0 && (sc >= CUR[j] || exp((sc - CUR[j]) / T[j]) * 4294967296.0 > (double)(rnd() & 0xffffffffULL))) {
                    CUR[j] = sc;
                    if (sc > best) { best = sc; for (int i = 0; i < N; i++) bp[i] = PT[i]; for (int i = 0; i < 26; i++) bx[i] = x[i]; }
                } else if (mv == 0) {
                    if (a2 >= 0) { z = x[a2]; x[a2] = x[b2]; x[b2] = z; }
                    z = x[a]; x[a] = x[b]; x[b] = z;
                    for (int i = 0; i < 26; i++) inv[x[i]] = i;
                }
                else prim[r] = old;
            }
        }
        for (int j = 0; j + 1 < R; j++) {
            double dd = (CUR[j + 1] - CUR[j]) * (1.0 / T[j] - 1.0 / T[j + 1]);
            if (dd >= 0 || exp(dd) * 4294967296.0 > (double)(rnd() & 0xffffffffULL)) {
                int tmp[26]; double c;
                for (int i = 0; i < 26; i++) { tmp[i] = X[j][i]; X[j][i] = X[j + 1][i]; X[j + 1][i] = tmp[i]; }
                for (int i = 0; i < 26; i++) { tmp[i] = INV[j][i]; INV[j][i] = INV[j + 1][i]; INV[j + 1][i] = tmp[i]; }
                for (int i = 0; i < 64; i++) { int z = PR[j][i]; PR[j][i] = PR[j + 1][i]; PR[j + 1][i] = z; }
                c = CUR[j]; CUR[j] = CUR[j + 1]; CUR[j + 1] = c;
            }
        }
    }
    return best;
}
"""


def _load(e):
    if e not in _MODS:
        import importlib.util
        import sys
        path = next((ROOT / "experiments").glob(f"{e}-*")) / "attack.py"
        spec = importlib.util.spec_from_file_location(f"frozen{e}", path)
        m = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = m
        spec.loader.exec_module(m)
        if hasattr(m, "ROOT"):
            m.ROOT = ROOT
        _MODS[e] = m
    return _MODS[e]


def lib():
    if "lib" not in _MODS:
        d = tempfile.mkdtemp(prefix="k4_f17_")
        open(os.path.join(d, "a.c"), "w").write(C_SOURCE)
        subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", os.path.join(d, "a.so"), os.path.join(d, "a.c"), "-lm"],
                       check=True, capture_output=True)
        L_ = ctypes.CDLL(os.path.join(d, "a.so"))
        L_.ptemper.restype = ctypes.c_double
        L_.ptemper.argtypes = [ctypes.c_uint64, ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int, ctypes.c_int,
                               ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
        L_.keep.restype = ctypes.c_double
        L_.keep.argtypes = [ctypes.c_uint64, ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int, ctypes.c_int,
                            ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int),
                            ctypes.POINTER(ctypes.c_int)]
        L_.climb.restype = ctypes.c_double
        L_.climb.argtypes = [ctypes.c_uint64, ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int, ctypes.c_double,
                             ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
        from kryptos.scorer import _table
        logs, floor = _table()
        tab = [floor] * (26 ** 4)
        for q, v in logs.items():
            if len(q) == 4 and q.isalpha() and q.isupper():
                tab[((ord(q[0]) - 65) * 26 + ord(q[1]) - 65) * 676 + (ord(q[2]) - 65) * 26 + ord(q[3]) - 65] = v
        _MODS["tab"] = (ctypes.c_double * len(tab))(*tab)
        _MODS["lib"] = L_
    return _MODS["lib"]


KINDS, FORMS = ("ct", "pt"), ("V", "B", "R")


def full_equations(text, known, L, kind, form):
    """0149's equations, with plaintext autokey's chains in full: between consecutive known places q1 < q2 of one
    chain (q2 = q1 + mL) the values follow v_i = X[c_i] - v_(i-L) (V), v_(i-L) - X[c_i] (B), v_(i-L) + X[c_i] (R), so
    X[p2] is linear in X[p1] and the carved letters at q1+L, ..., q2. Ciphertext autokey is unchanged (each known place
    already gives its own equation). Rows: {letter: coefficient}, sum = 0 mod 26."""
    if kind == "ct":
        return _load("0149").equations(text, known, L, kind, form)
    rows = []
    by = {}
    for q in sorted(known):
        by.setdefault((q - 1) % L, []).append(q - 1)
    for chain in by.values():
        for i1, i2 in zip(chain, chain[1:]):
            r = {}

            def add(v, a):
                r[v] = (r.get(v, 0) + a) % 26
            sign = 1                                  # v_i = sign * v_i1 + sum(coef * X[c])
            terms = []
            i = i1 + L
            while i <= i2:
                c = ord(text[i]) - 65
                if form == "V":
                    terms = [(v, -a) for v, a in terms] + [(c, 1)]; sign = -sign
                elif form == "B":
                    terms = terms + [(c, -1)]
                else:
                    terms = terms + [(c, 1)]
                i += L
            add(ord(known[i2 + 1]) - 65, 1)
            add(ord(known[i1 + 1]) - 65, -sign)
            for v, a in terms:
                add(v, -a)
            rows.append({v: a for v, a in r.items() if a})
    return rows


def witness(text, cell, rng):
    """0149's exact decider; a full alphabet (letter -> value) from its witness, or None if the cell does not fit."""
    from kryptos.facts import KNOWN
    m = _load("0149")
    kind, form, L = cell
    rows = full_equations(text, KNOWN, L, kind, form)
    if not rows:
        return None
    st, x = m.solve(rows)
    if st != "fit":
        return None
    free = [v for v in range(26) if v not in set(x.values())]
    rng.shuffle(free)
    return [x[le] if le in x else free.pop() for le in range(26)]


def climb(text, cell, w, seed):
    from kryptos.facts import KNOWN
    L_ = lib()
    kind, form, L = cell
    kp = sorted(KNOWN)
    L_.setup(_MODS["tab"], (ctypes.c_int * N)(*[ord(c) - 65 for c in text]), N, L, KINDS.index(kind), FORMS.index(form),
             (ctypes.c_int * 24)(*[q - 1 for q in kp]), (ctypes.c_int * 24)(*[ord(KNOWN[q]) - 65 for q in kp]), 24)
    bp, bx = (ctypes.c_int * 128)(), (ctypes.c_int * 26)()
    mode = "keep" if (kind == "pt" and L <= SHORT) else "pt"
    if mode == "keep":
        live = ctypes.c_int()
        sc = L_.keep(seed, (ctypes.c_int * 26)(*w), K_R, K_ROUNDS, K_MOVES, K_T0, K_T1, bp, bx, ctypes.byref(live))
    elif mode == "pt":
        sc = L_.ptemper(seed, (ctypes.c_int * 26)(*w), PT_R, PT_ROUNDS, PT_MOVES, T0, T1, PT_PEN, bp, bx)
    else:
        sc = L_.climb(seed, (ctypes.c_int * 26)(*w), RESTARTS, MOVES, T0, T1, PEN, bp, bx)
    return round(sc, 5), "".join("?" if bp[i] < 0 else chr(65 + bp[i]) for i in range(N))


def decide(text, cell, seed, esc):
    rng = random.Random(seed)
    t0 = time.time()
    w = witness(text, cell, rng)
    score, reading = climb(text, cell, w, rng.randrange(1 << 62))
    copies, lost, limit = [], 0, BASE
    while len(copies) < limit and score > -99:
        sh, cw = list(text), None
        for _ in range(20000):
            rng.shuffle(sh)
            cw = witness("".join(sh), cell, rng)
            if cw is not None:
                break
        if cw is None:
            lost += 1
            break
        cs = climb("".join(sh), cell, cw, rng.randrange(1 << 62))[0]
        copies.append(cs)
        if cs >= score:
            break
        if len(copies) == BASE and esc:
            limit = ESC
    above = len(copies) if all(c < score for c in copies) else len(copies) - 1
    return {"score": score, "reading": reading, "copies": copies, "above": above, "lost": lost, "secs": round(time.time() - t0, 1)}


def _job(args):
    key, text, cell, seed, esc = args
    return key, decide(text, cell, seed, esc)


def _fit_job(args):
    text, cells = args
    rng = random.Random(0)
    return [c for c in cells if witness(text, c, rng) is not None]


def run(ctx):
    import multiprocessing as mp
    import sys
    import types
    from math import exp, lgamma, log
    t_start = time.time()
    W = int(os.environ.get("K4_WORKERS", 8))
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    m49 = _load("0149"); lib()
    m20, m26 = _load("0140").load_0120(), _load("0226")
    k4 = ctx.K4
    cells_all = [(k, f, L) for k in KINDS for f in FORMS for L in range(1, N)]
    with mp.get_context("fork").Pool(W) as pool:
        fit = sorted(c for part in pool.imap_unordered(_fit_job, [(k4, cells_all[i::W * 4]) for i in range(W * 4)]) for c in part)
    rec = _rec("0149")["summary"]
    rec_fit = sorted((k, f, L) for k in KINDS for f in FORMS for L in rec[f"{k}/{f}"]["k4_fit_lags"])
    ctx.progress(0, 1, "settings")

    # plants: per kind 12 clean (Carter windows) and 12 Sanborn-style (0226's three classes, 4 each), on K4's own cells
    rng, prng = random.Random(2540), random.Random(2541)
    STD = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    plants, pmeta = [], {}
    for kind in KINDS:
        cells = [c for c in fit if c[0] == kind]
        texts = [("clean", pt) for _, pt in m20.make_plants(ctx.KNOWN, 10, rng, PLANTS)]
        for a in range(3):
            ct_ = m26.class_texts(rng, a)
            texts += [x for x in ct_ if x[0] == ("xstops", "k123", "sub3")[a]][:PLANTS // 3]
        for idx, (cls, pt) in enumerate(texts):
            for _ in range(1000):
                cell = cells[prng.randrange(len(cells))]
                alpha = list(STD); prng.shuffle(alpha); alpha = "".join(alpha)
                prim = [prng.choice(STD) for _ in range(cell[2])]
                pc = m49.encipher(pt, alpha, cell[2], cell[0], cell[1], prim)
                if witness(pc, cell, prng) is not None:
                    break
            pmeta[(kind, idx)] = {"cls": cls, "cell": "/".join(map(str, cell)), "pt": pt}
            plants.append(((kind, idx), pc, cell, 950000 + len(plants), False))

    work = plants + [(("k4", i), k4, c, 2000 + i, True) for i, c in enumerate(fit)]
    res = {}
    saved = getattr(ctx, "saved", {}) or {}
    for key, *_ in work:                      # units an earlier run of this attack.py finished (#105)
        if f"{key[0]}:{key[1]}" in saved:
            res[key] = saved[f"{key[0]}:{key[1]}"]
    todo = [w for w in work if w[0] not in res]
    ctx.progress(len(res), len(work), "settings")
    with mp.get_context("fork").Pool(W) as pool:
        for key, out in pool.imap_unordered(_job, todo, chunksize=1):
            res[key] = out
            ctx.save(f"{key[0]}:{key[1]}", out)
            ctx.progress(len(res), len(work), "settings")

    power = {}
    for (kind, idx), v in pmeta.items():
        r = res[(kind, idx)]
        S = int(v["cell"].split("/")[2]) if kind == "ct" else 0
        v.update(found=r["score"] > -99 and r["above"] >= BASE, above=r["above"], score=r["score"],
                 letters_right=sum(a == b for a, b in zip(r["reading"][S:], v.pop("pt")[S:])), letters_scored=N - S)
        b = f"{kind}/{'clean' if v['cls'] == 'clean' else 'sanborn'}"
        power.setdefault(b, [0, 0]); power[b][0] += v["found"]; power[b][1] += 1
        lag = int(v["cell"].split("/")[2])
        g = "pt_short_keep" if kind == "pt" and lag <= SHORT else f"{kind}_tempering"
        power.setdefault(g, [0, 0]); power[g][0] += v["found"]; power[g][1] += 1
    n = len(fit)
    q12, q100 = 1 / (BASE + 1), 1 / (ESC + 1)

    def tail(k, q):
        return sum(exp(lgamma(n + 1) - lgamma(j + 1) - lgamma(n - j + 1) + j * log(q) + (n - j) * log(1 - q)) for j in range(k, n + 1))
    valid = [i for i in range(n) if res[("k4", i)]["score"] > -99]
    k12 = sum(1 for i in valid if res[("k4", i)]["above"] >= BASE)
    k100 = sum(1 for i in valid if res[("k4", i)]["above"] >= ESC)
    per_kind = {kind: {"cells": sum(1 for c in fit if c[0] == kind), "no_valid_reading": sum(1 for i in range(n) if fit[i][0] == kind and i not in valid),
                       "above_all_12": sum(1 for i in valid if fit[i][0] == kind and res[("k4", i)]["above"] >= BASE)} for kind in KINDS}
    cells_out = []
    for i in sorted(range(n), key=lambda i: (-res[("k4", i)]["above"], -res[("k4", i)]["score"])):
        r = res[("k4", i)]
        cells_out.append({"cell": "/".join(map(str, fit[i])), "score": r["score"], "above": r["above"], "copies": r["copies"],
                          "reading": r["reading"], "known_in_place": sum(r["reading"][q - 1] == c for q, c in ctx.KNOWN.items())})
    bounds = {
        "item": "F1.7 (D2's last re-cost; the cells decided in the same run)",
        "decider_used": f"plaintext autokey at lags 1-{SHORT}: check-keeping parallel tempering ({K_R} replicas x {K_ROUNDS} rounds x {K_MOVES} moves, T {K_T0}->{K_T1}; every replica starts from the exact solver's witness of the full chain equations; a swap that breaks a check is repaired by a second swap that restores every check, as 0139, or dropped); every other cell: parallel tempering with a fixed penalty {PT_PEN} per known place out of place ({PT_R} replicas x {PT_ROUNDS} rounds x {PT_MOVES} moves, T {T0}->{T1}), only states with every known place right recorded",
        "desk_tests": "2026-10-29, before the run: the draft's annealing ('sa', penalty 0.04 ramped) never reached a state with all 24 in place at plaintext lags 6-12 and left the true alphabet when started on it; the full-chain witness and the check-keeping moves read 2 of 3 plants at lag 6 exactly; on ciphertext autokey (lags 34-70) no variant (sa, keep, tempering at penalties 0.2/0.6/2.0, up to 5x longer) reached the true reading's score (plants -4.2, climbs -5.5 to -6.3): low power is expected there and is measured here",
        "modal_cost_estimate": "about 103 cells x up to 13 climbs plus 48 plants: 'keep' cells about 4 min per climb (10 cells), others about 3 s: about 10-12 core-hours, under $1 of Modal credit",
        "decider_draft": f"compiled annealing over the alphabet (and free plaintext-autokey chain starts): {RESTARTS} restarts x {MOVES} moves, T {T0}->{T1}, penalty per known letter out of place {PEN} raised 50-fold through each run; only states with every known letter in place count; ciphertext autokey scored on places L+1..97 (the first L letters come from single-use primer letters and are open)",
        "copies": "shuffles 0149's exact decider fits in the same cell, climbed one at a time; stop at the first at or above K4, at most 12, escalated to 100 for K4",
        "k4_fitting_cells": n, "matches_0149_record": fit == rec_fit, "fit_0149_record_count": len(rec_fit),
        "per_kind": per_kind, "k4_cells_with_a_valid_reading": len(valid),
        "k4_above_all_12": k12, "expected_12": round(len(valid) * q12, 1), "binomial_p_12": tail(k12, q12) if valid else None,
        "k4_above_all_100": k100, "expected_100": round(len(valid) * q100, 2),
        "plants": {"power": power, "null_per_plant": "1/13", "each": {f"{k[0]}/{k[1]}": v for k, v in pmeta.items()}},
        "cells": cells_out, "core_seconds": round(sum(r["secs"] for r in res.values())), "compute_seconds": round(time.time() - t_start),
        "exhaustive": True, "exhaustive_over": "every (kind, form, lag) cell where K4 fits 0149's exact decider, decided at the measured power",
        "not_covered": "0149's 7 undecided cells (node limit); the move-first version (about 176 million exact searches)",
    }
    notes = (f"F1.7: {n} cells; K4 valid readings {len(valid)}; above all 12 copies in {k12} (chance {len(valid) * q12:.1f}), "
             f"above all 100 in {k100}; plant power " + ", ".join(f"{k} {v[0]}/{v[1]}" for k, v in sorted(power.items())) +
             ". No candidate returned (ciphertext-autokey readings have open primer letters; per-cell copies do not account for the cells searched).")
    controls = [c for i in valid for c in res[("k4", i)]["copies"]][:2000]
    return {"candidates": [], "bounds": bounds, "notes": notes, "controls": controls}


def _rec(e):
    import json
    return json.loads((next((ROOT / "experiments").glob(f"{e}-*")) / "result.json").read_text())["bounds"]


def encrypt(plaintext, key):
    m = _load("0149")
    return m.encipher(plaintext, key["alpha"], key["L"], key["kind"], key["form"], key["primer"])


def worked_example(ctx, key):
    return "\n".join([
        "F1.7: autokey on one unknown alphabet.", "",
        "  ciphertext autokey, lag L: key letter at place i = carved letter at place i - L",
        "  so x(plain_i) = x(carved_i) - x(carved_{i-L}) on the unknown alphabet x: the alphabet alone fixes places L+1..97",
        "  plaintext autokey, lag L: key letter = plain letter L places back; a chain i, i+L, i+2L ... is fixed by x and its first letter", "",
        "  per cell: climb x for the most English reading; climb scrambled copies that fit the same cell; K4 must beat them all."])
