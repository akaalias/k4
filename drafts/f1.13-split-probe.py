"""F1.13 desk probe (2026-10-31): the split climb of drafts/F1.13-design.md on 0256's plants.

Stage A climbs the pairing y = x mod 13 (two letters per residue) by parallel tempering on a surrogate score
(per quadgram window, log10 of the summed English probability over the 16 letter expansions of its four pair
classes: an upper bound on any reading the pairing allows), with a fixed penalty per known place whose mod-13
check fails. Stage B enumerates the 2^13 parities exactly for the best distinct pairings and scores each full
reading as 0256 does (mean log10 quadgram from place L+1). A plant counts as reached if the best exact score is
at least the true reading's score (minus 1e-9), and as read if the reading equals the plant from place L+1.

Usage: uv run python drafts/f1.13-split-probe.py [ct|pt] [n_plants] [R ROUNDS M]
Ciphertext autokey only for now (pt: chains, to add if ct meets the bar).
"""
import ctypes
import importlib.util
import os
import random
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
N = 97

C_SRC = r"""
#include <stdint.h>
#include <math.h>
#include <string.h>
static const double *TAB; static double *PROB;
static int N, L, FORM, C[128], NK, KP[24], KL[24];
static uint64_t RS;
static inline uint64_t rnd(void) { RS ^= RS << 13; RS ^= RS >> 7; RS ^= RS << 17; return RS; }
static inline int md(int v, int m) { v %= m; return v < 0 ? v + m : v; }
static inline int dec(int c, int k, int m) { return FORM == 0 ? md(c - k, m) : FORM == 1 ? md(k - c, m) : md(c + k, m); }
int setup(const double *tab, double *prob, const int *ct, int n, int l, int form, const int *kp, const int *kl, int nk) {
    TAB = tab; PROB = prob; N = n; L = l; FORM = form; NK = nk;
    for (int i = 0; i < n; i++) C[i] = ct[i];
    for (int j = 0; j < nk; j++) { KP[j] = kp[j]; KL[j] = kl[j]; }
    return 0;
}
/* stage A: y[letter] in Z13, mem[r][0..1] the two letters on residue r */
static int badA(const int *y) {
    int b = 0;
    for (int j = 0; j < NK; j++) { int q = KP[j]; if (q >= L && dec(y[C[q]], y[C[q - L]], 13) != y[KL[j]]) b++; }
    return b;
}
static double scoreA(const int *y, int mem[13][2]) {
    int r[128]; double s = 0; int n = 0;
    for (int i = L; i < N; i++) r[i] = dec(y[C[i]], y[C[i - L]], 13);
    for (int i = L; i + 3 < N; i++) {
        double t = 0;
        const int *a = mem[r[i]], *b = mem[r[i + 1]], *c = mem[r[i + 2]], *d = mem[r[i + 3]];
        for (int p = 0; p < 2; p++) for (int q = 0; q < 2; q++) for (int u = 0; u < 2; u++) {
            int base = ((a[p] * 26 + b[q]) * 26 + c[u]) * 26;
            t += PROB[base + d[0]] + PROB[base + d[1]];
        }
        s += log10(t); n++;
    }
    return n ? s / n : -99;
}
/* stage B: every parity choice for pairing y; best exact score with every checkable known place right */
double stageB(const int *y, int *bp, int *bx) {
    int mem[13][2], cnt[13] = {0};
    for (int i = 0; i < 26; i++) mem[y[i]][cnt[y[i]]++] = i;
    double best = -99; int x[26], inv[26], pt[128];
    for (int bits = 0; bits < 8192; bits++) {
        for (int r = 0; r < 13; r++) {
            int b = (bits >> r) & 1;               /* parity of mem[r][0] */
            int v0 = (r % 2 == b) ? r : r + 13, v1 = (v0 == r) ? r + 13 : r;
            x[mem[r][0]] = v0; x[mem[r][1]] = v1;
        }
        int ok = 1;
        for (int j = 0; j < NK && ok; j++) { int q = KP[j]; if (q >= L && dec(x[C[q]], x[C[q - L]], 26) != x[KL[j]]) ok = 0; }
        if (!ok) continue;
        for (int i = 0; i < 26; i++) inv[x[i]] = i;
        for (int i = L; i < N; i++) pt[i] = inv[dec(x[C[i]], x[C[i - L]], 26)];
        double s = 0; int n = 0;
        for (int i = L; i + 3 < N; i++) { s += TAB[((pt[i] * 26 + pt[i + 1]) * 26 + pt[i + 2]) * 26 + pt[i + 3]]; n++; }
        s = n ? s / n : -99;
        if (s > best) { best = s; for (int i = 0; i < N; i++) bp[i] = i < L ? -1 : pt[i]; for (int i = 0; i < 26; i++) bx[i] = x[i]; }
    }
    return best;
}
/* exact score of a full alphabet x (for the plant's true reading) */
double exact(const int *x, int *bp) {
    int inv[26], pt[128]; for (int i = 0; i < 26; i++) inv[x[i]] = i;
    for (int i = L; i < N; i++) pt[i] = inv[dec(x[C[i]], x[C[i - L]], 26)];
    double s = 0; int n = 0;
    for (int i = L; i + 3 < N; i++) { s += TAB[((pt[i] * 26 + pt[i + 1]) * 26 + pt[i + 2]) * 26 + pt[i + 3]]; n++; }
    for (int i = 0; i < N; i++) bp[i] = i < L ? -1 : pt[i];
    return n ? s / n : -99;
}
double surrogate(const int *y) {
    int mem[13][2], cnt[13] = {0};
    for (int i = 0; i < 26; i++) mem[y[i]][cnt[y[i]]++] = i;
    return scoreA(y, mem);
}
/* tempering over pairings; keeps the TOPK best distinct zero-bad pairings by surrogate in top (TOPK x 26), returns count */
#define TOPK 64
static int TOP[TOPK][26]; static double TOPS[TOPK]; static int NTOP;
static void push(const int *y, double s) {
    for (int k = 0; k < NTOP; k++) if (!memcmp(TOP[k], y, sizeof(int) * 26)) return;
    if (NTOP < TOPK) { memcpy(TOP[NTOP], y, sizeof(int) * 26); TOPS[NTOP++] = s; return; }
    int w = 0; for (int k = 1; k < NTOP; k++) if (TOPS[k] < TOPS[w]) w = k;
    if (s > TOPS[w]) { memcpy(TOP[w], y, sizeof(int) * 26); TOPS[w] = s; }
}
int climbA(uint64_t seed, int R, int ROUNDS, int M, double t0, double t1, double pen, int *out, double *outs) {
    RS = seed * 2862933555777941757ULL + 3037000493ULL; if (!RS) RS = 1;
    static int Y[32][26], MEM[32][13][2]; double CUR[32], T[32]; NTOP = 0;
    for (int j = 0; j < R; j++) {
        T[j] = R > 1 ? t0 * pow(t1 / t0, (double)j / (R - 1)) : t1;
        int perm[26]; for (int i = 0; i < 26; i++) perm[i] = i;
        for (int t = 25; t > 0; t--) { int a = rnd() % (t + 1), z = perm[a]; perm[a] = perm[t]; perm[t] = z; }
        for (int i = 0; i < 26; i++) { Y[j][perm[i]] = i % 13; MEM[j][i % 13][i / 13] = perm[i]; }
        CUR[j] = scoreA(Y[j], MEM[j]) - pen * badA(Y[j]);
    }
    for (int round = 0; round < ROUNDS; round++) {
        for (int j = 0; j < R; j++) {
            int *y = Y[j];
            for (int m = 0; m < M; m++) {
                int a = rnd() % 26, b = rnd() % 26; if (y[a] == y[b]) continue;
                int ra = y[a], rb = y[b], ia = MEM[j][ra][0] == a ? 0 : 1, ib = MEM[j][rb][0] == b ? 0 : 1;
                y[a] = rb; y[b] = ra; MEM[j][ra][ia] = b; MEM[j][rb][ib] = a;
                int nb = badA(y);
                double sc = scoreA(y, MEM[j]) - pen * nb;
                if (sc >= CUR[j] || exp((sc - CUR[j]) / T[j]) * 4294967296.0 > (double)(rnd() & 0xffffffffULL)) {
                    CUR[j] = sc;
                    if (nb == 0 && (NTOP < TOPK || sc > TOPS[0] - 1.0)) push(y, sc);
                } else { y[a] = ra; y[b] = rb; MEM[j][ra][ia] = a; MEM[j][rb][ib] = b; }
            }
        }
        for (int j = 0; j + 1 < R; j++) {
            double d = (CUR[j + 1] - CUR[j]) * (1.0 / T[j] - 1.0 / T[j + 1]);
            if (d >= 0 || exp(d) * 4294967296.0 > (double)(rnd() & 0xffffffffULL)) {
                int tmp[26], tm[13][2]; double c;
                memcpy(tmp, Y[j], sizeof tmp); memcpy(Y[j], Y[j + 1], sizeof tmp); memcpy(Y[j + 1], tmp, sizeof tmp);
                memcpy(tm, MEM[j], sizeof tm); memcpy(MEM[j], MEM[j + 1], sizeof tm); memcpy(MEM[j + 1], tm, sizeof tm);
                c = CUR[j]; CUR[j] = CUR[j + 1]; CUR[j + 1] = c;
            }
        }
    }
    for (int k = 0; k < NTOP; k++) { memcpy(out + 26 * k, TOP[k], sizeof(int) * 26); outs[k] = TOPS[k]; }
    return NTOP;
}

/* exact objective for a pairing: GF(2) elimination of the parity checks, every consistent parity choice decoded
   and scored; returns the best score minus pen x (failed mod-13 checks + inconsistent parity rows) */
static int SOLX[26];
static double evalE(const int *y, int mem[13][2], double pen, int *nbad_out, int *xbest) {
    int t[26];
    for (int r = 0; r < 13; r++) { t[mem[r][0]] = 0; t[mem[r][1]] = 1; }
    int bad13 = 0, rows[24], rhs[24], nr = 0;
    for (int j = 0; j < NK; j++) {
        int q = KP[j]; if (q < L) continue;
        int c = C[q], k = C[q - L], p = KL[j];
        if (dec(y[c], y[k], 13) != y[p]) { bad13++; continue; }
        int m = (1 << y[c]) ^ (1 << y[k]) ^ (1 << y[p]);
        rows[nr] = m; rhs[nr] = t[c] ^ t[k] ^ t[p]; nr++;
    }
    /* eliminate */
    int piv[13], prow[13], np = 0, incons = 0;
    for (int i = 0; i < nr; i++) {
        int m = rows[i], h = rhs[i];
        for (int a = 0; a < np; a++) if (m >> piv[a] & 1) { m ^= prow[a]; h ^= (prow[a] >> 16) & 1; }
        m &= 0xffff;
        if (!m) { if (h) incons++; continue; }
        int b = __builtin_ctz(m);
        for (int a = 0; a < np; a++) if (prow[a] >> b & 1) { prow[a] ^= m | (h << 16); }
        piv[np] = b; prow[np++] = m | (h << 16);
    }
    int isp[13] = {0}; for (int a = 0; a < np; a++) isp[piv[a]] = 1;
    int fr[13], nf = 0; for (int r = 0; r < 13; r++) if (!isp[r]) fr[nf++] = r;
    double best = -99; int x[26], inv[26], pt[128];
    for (int s = 0; s < (1 << nf); s++) {
        int bits = 0;
        for (int f = 0; f < nf; f++) if (s >> f & 1) bits |= 1 << fr[f];
        for (int a = 0; a < np; a++) {          /* pivot bit = rhs xor (free bits in its row) */
            int m = prow[a] & 0xffff, h = (prow[a] >> 16) & 1;
            h ^= __builtin_parity((m & ~(1 << piv[a])) & bits);
            if (h) bits |= 1 << piv[a];
        }
        for (int r = 0; r < 13; r++) {
            int b = (bits >> r) & 1, v0 = (r % 2 == b) ? r : r + 13;
            x[mem[r][0]] = v0; x[mem[r][1]] = v0 == r ? r + 13 : r;
        }
        for (int i = 0; i < 26; i++) inv[x[i]] = i;
        for (int i = L; i < N; i++) pt[i] = inv[dec(x[C[i]], x[C[i - L]], 26)];
        double sc = 0; int n = 0;
        for (int i = L; i + 3 < N; i++) { sc += TAB[((pt[i] * 26 + pt[i + 1]) * 26 + pt[i + 2]) * 26 + pt[i + 3]]; n++; }
        sc = n ? sc / n : -99;
        if (sc > best) { best = sc; if (xbest) memcpy(xbest, x, sizeof x); }
    }
    *nbad_out = bad13 + incons;
    return best - pen * (bad13 + incons);
}
double climbE(uint64_t seed, int R, int ROUNDS, int M, double t0, double t1, double pen, int *bx) {
    RS = seed * 2862933555777941757ULL + 3037000493ULL; if (!RS) RS = 1;
    static int Y[32][26], MEM[32][13][2]; double CUR[32], T[32], best = -99; int nb, xb[26];
    for (int j = 0; j < R; j++) {
        T[j] = R > 1 ? t0 * pow(t1 / t0, (double)j / (R - 1)) : t1;
        int perm[26]; for (int i = 0; i < 26; i++) perm[i] = i;
        for (int t = 25; t > 0; t--) { int a = rnd() % (t + 1), z = perm[a]; perm[a] = perm[t]; perm[t] = z; }
        for (int i = 0; i < 26; i++) { Y[j][perm[i]] = i % 13; MEM[j][i % 13][i / 13] = perm[i]; }
        CUR[j] = evalE(Y[j], MEM[j], pen, &nb, xb);
    }
    for (int round = 0; round < ROUNDS; round++) {
        for (int j = 0; j < R; j++) {
            int *y = Y[j];
            for (int m = 0; m < M; m++) {
                int a = rnd() % 26, b = rnd() % 26; if (y[a] == y[b]) continue;
                int ra = y[a], rb = y[b], ia = MEM[j][ra][0] == a ? 0 : 1, ib = MEM[j][rb][0] == b ? 0 : 1;
                y[a] = rb; y[b] = ra; MEM[j][ra][ia] = b; MEM[j][rb][ib] = a;
                double sc = evalE(y, MEM[j], pen, &nb, xb);
                if (sc >= CUR[j] || exp((sc - CUR[j]) / T[j]) * 4294967296.0 > (double)(rnd() & 0xffffffffULL)) {
                    CUR[j] = sc;
                    if (nb == 0 && sc > best) { best = sc; memcpy(bx, xb, sizeof xb); }
                } else { y[a] = ra; y[b] = rb; MEM[j][ra][ia] = a; MEM[j][rb][ib] = b; }
            }
        }
        for (int j = 0; j + 1 < R; j++) {
            double d = (CUR[j + 1] - CUR[j]) * (1.0 / T[j] - 1.0 / T[j + 1]);
            if (d >= 0 || exp(d) * 4294967296.0 > (double)(rnd() & 0xffffffffULL)) {
                int tmp[26], tm[13][2]; double c;
                memcpy(tmp, Y[j], sizeof tmp); memcpy(Y[j], Y[j + 1], sizeof tmp); memcpy(Y[j + 1], tmp, sizeof tmp);
                memcpy(tm, MEM[j], sizeof tm); memcpy(MEM[j], MEM[j + 1], sizeof tm); memcpy(MEM[j + 1], tm, sizeof tm);
                c = CUR[j]; CUR[j] = CUR[j + 1]; CUR[j + 1] = c;
            }
        }
    }
    return best;
}
"""


def load(e):
    path = next((ROOT / "experiments").glob(f"{e}-*")) / "attack.py"
    spec = importlib.util.spec_from_file_location(f"frozen{e}", path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    if hasattr(m, "ROOT"):
        m.ROOT = ROOT
    return m


def lib():
    d = tempfile.mkdtemp(prefix="k4_f113_")
    open(os.path.join(d, "a.c"), "w").write(C_SRC)
    subprocess.run(["cc", "-O3", "-shared", "-fPIC", "-o", os.path.join(d, "a.so"), os.path.join(d, "a.c"), "-lm"], check=True)
    L_ = ctypes.CDLL(os.path.join(d, "a.so"))
    for f in ("stageB", "exact", "surrogate", "climbE"):
        getattr(L_, f).restype = ctypes.c_double
    L_.climbE.argtypes = [ctypes.c_uint64, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double,
                          ctypes.c_double, ctypes.POINTER(ctypes.c_int)]
    L_.climbA.argtypes = [ctypes.c_uint64, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double,
                          ctypes.c_double, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_double)]
    from kryptos.scorer import _table
    logs, floor = _table()
    tab = [floor] * (26 ** 4)
    for q, v in logs.items():
        if len(q) == 4 and q.isalpha() and q.isupper():
            tab[((ord(q[0]) - 65) * 26 + ord(q[1]) - 65) * 676 + (ord(q[2]) - 65) * 26 + ord(q[3]) - 65] = v
    T = (ctypes.c_double * len(tab))(*tab)
    P = (ctypes.c_double * len(tab))(*[10 ** v for v in tab])
    return L_, T, P


def plants_0256(kind_want):
    """0256's plants, regenerated with its seeds and code (same loop over both kinds, so the RNG state matches)."""
    import json
    from kryptos.facts import KNOWN
    m56 = load("0256")
    m49 = m56._load("0149")
    m20, m26 = m56._load("0140").load_0120(), m56._load("0226")
    res = json.loads((next((ROOT / "experiments").glob("0256-*")) / "result.json").read_text())["bounds"]
    fit = sorted(tuple(int(x) if x.isdigit() else x for x in c["cell"].split("/")) for c in res["cells"])
    rng, prng = random.Random(2540), random.Random(2541)
    STD = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    out = []
    for kind in ("ct", "pt"):
        cells = [c for c in fit if c[0] == kind]
        texts = [("clean", pt) for _, pt in m20.make_plants(KNOWN, 10, rng, 12)]
        for a in range(3):
            ct_ = m26.class_texts(rng, a)
            texts += [x for x in ct_ if x[0] == ("xstops", "k123", "sub3")[a]][:12 // 3]
        for idx, (cls, pt) in enumerate(texts):
            for _ in range(1000):
                cell = cells[prng.randrange(len(cells))]
                alpha = list(STD); prng.shuffle(alpha); alpha = "".join(alpha)
                prim = [prng.choice(STD) for _ in range(cell[2])]
                pc = m49.encipher(pt, alpha, cell[2], cell[0], cell[1], prim)
                if m56.witness(pc, cell, prng) is not None:
                    break
            if kind == kind_want:
                out.append({"idx": idx, "cls": cls, "cell": cell, "pt": pt, "ct": pc, "alpha": alpha})
    expect = {f"{k}": v for k, v in res["plants"]["each"].items()}
    return out, expect


def main():
    kind = sys.argv[1] if len(sys.argv) > 1 else "ct"
    nmax = int(sys.argv[2]) if len(sys.argv) > 2 else 24
    global MODE
    MODE = os.environ.get("MODE", "A")
    R, ROUNDS, M = (int(v) for v in sys.argv[3:6]) if len(sys.argv) > 5 else (16, 100, 1000)
    from kryptos.facts import KNOWN
    L_, T, P = lib()
    plants, expect = plants_0256(kind)
    kp = sorted(KNOWN)
    reached = read = 0
    t_all = time.time()
    for pl in plants[:nmax]:
        _, form, L = pl["cell"]
        L_.setup(T, P, (ctypes.c_int * N)(*[ord(c) - 65 for c in pl["ct"]]), N, L, ("V", "B", "R").index(form),
                 (ctypes.c_int * 24)(*[q - 1 for q in kp]), (ctypes.c_int * 24)(*[ord(KNOWN[q]) - 65 for q in kp]), 24)
        xt = [pl["alpha"].index(chr(65 + i)) for i in range(26)]
        bp = (ctypes.c_int * 128)()
        s_true = L_.exact((ctypes.c_int * 26)(*xt), bp)
        yt = [v % 13 for v in xt]
        sur_true = L_.surrogate((ctypes.c_int * 26)(*yt))
        t0 = time.time()
        if MODE == "E":
            bx = (ctypes.c_int * 26)()
            best = L_.climbE(pl["idx"] * 7919 + 1, R, ROUNDS, M, 0.15, 0.003, 0.6, bx)
            tA = time.time() - t0
            brd = None
            if best > -99:
                L_.exact(bx, bp); brd = "".join("?" if bp[j] < 0 else chr(65 + bp[j]) for j in range(N))
            ok = best >= s_true - 1e-9
            same = brd is not None and brd[L:] == pl["pt"][L:]
            right = 0 if brd is None else sum(a == b for a, b in zip(brd[L:], pl["pt"][L:]))
            reached += ok; read += same
            e = expect.get(f"{kind}/{pl['idx']}", {})
            print(f"{kind}/{pl['idx']:2d} {pl['cls']:7s} {'/'.join(map(str, pl['cell'])):8s} true {s_true:.3f} | best {best:.3f} "
                  f"letters {right}/{N - L} | reached {ok} read {same} | 0256 found {e.get('found')} score {e.get('score')} | {tA:.1f}s", flush=True)
            continue
        out, outs = (ctypes.c_int * (64 * 26))(), (ctypes.c_double * 64)()
        k = L_.climbA(pl["idx"] * 7919 + 1, R, ROUNDS, M, 0.15, 0.003, 0.6, out, outs)
        tA = time.time() - t0
        best, brd, sur_best = -99, None, max(outs[i] for i in range(k)) if k else -99
        bx = (ctypes.c_int * 26)()
        true_in_top = False
        for i in range(k):
            y = list(out[26 * i: 26 * i + 26])
            if all(y[a] == y[b] for a in range(26) for b in range(26) if yt[a] == yt[b]):
                true_in_top = True
            s = L_.stageB((ctypes.c_int * 26)(*y), bp, bx)
            if s > best:
                best, brd = s, "".join("?" if bp[j] < 0 else chr(65 + bp[j]) for j in range(N))
        tB = time.time() - t0 - tA
        ok = best >= s_true - 1e-9
        same = brd is not None and brd[L:] == pl["pt"][L:]
        reached += ok; read += same
        e = expect.get(f"{kind}/{pl['idx']}", {})
        print(f"{kind}/{pl['idx']:2d} {pl['cls']:7s} {'/'.join(map(str, pl['cell'])):8s} true {s_true:.3f} sur_true {sur_true:.3f} | "
              f"best {best:.3f} sur_best {sur_best:.3f} top {k} true_in_top {true_in_top} | reached {ok} read {same} | "
              f"0256 found {e.get('found')} score {e.get('score')} | A {tA:.1f}s B {tB:.1f}s", flush=True)
    n = min(nmax, len(plants))
    print(f"\n{kind}: reached {reached}/{n}, read exactly {read}/{n}; settings R {R} ROUNDS {ROUNDS} M {M}; {time.time() - t_all:.0f}s")


if __name__ == "__main__":
    main()
