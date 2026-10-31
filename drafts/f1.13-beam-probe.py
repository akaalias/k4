"""F1.13 desk probe (2026-10-31): a constructive beam search for plaintext autokey on one free alphabet.

The 24 known places form two contiguous runs (22-34, 64-74). Plaintext autokey links place i to i-L (the key at i is
the plain letter at i-L), so one step from a run decodes a whole run L places away, forward (p_i from p_(i-L) and the
carved letter at i) or backward (p_i is the key at i+L, from p_(i+L) and the carved letter there). The beam decodes
places in that breadth-first order, assigning alphabet values only when a step needs them (the value of a carved
letter, the letter holding a value): every branch is a partial bijection. A place reached twice is a check, which
forces or kills a value. Partial readings are scored by English letter probabilities given the decoded letters to the
left (from the quadgram table: 4-, 3-, 2-, 1-gram backoff). Complete readings are rescored as 0256 scores them.

Usage: uv run python drafts/f1.13-beam-probe.py BEAM i [i ...]   (0256's pt plant indices)
"""
import ctypes
import importlib.util
import os
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
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdio.h>
typedef struct St_ { signed char x[26], inv[26], p[97]; double s; } St;
static const double *Q4; static double *C1, *C2, *C3;   /* log10 P(d|abc), P(c|ab) as log10 joint ratios, etc. */
static double *L1, *L2, *L3, *L4;                       /* log10 joint probabilities of 1..4-grams */
static int N, L, FORM, C[128], KNOWNL[128];
static int NAP, APA[64];   /* known places a with a+L also known: relations no step visits */
static int NSTEP, SPOS[256], SDIR[256];
static inline int md(int v) { v %= 26; return v < 0 ? v + 26 : v; }
static inline int dec(int c, int k) { return FORM == 0 ? md(c - k) : FORM == 1 ? md(k - c) : md(c + k); }   /* value of p from c, key k */
static inline int keyof(int c, int p) { return FORM == 0 ? md(c - p) : FORM == 1 ? md(p + c) : md(p - c); } /* key value from c, p */
static inline int encv(int p, int k) { return FORM == 0 ? md(p + k) : FORM == 1 ? md(k - p) : md(p - k); }  /* value of c from p, k */
int setup(const double *l4, int n, int l, int form, const int *ct, const int *known) {
    N = n; L = l; FORM = form;
    for (int i = 0; i < n; i++) { C[i] = ct[i]; KNOWNL[i] = known[i]; }
    static double a1[26], a2[676], a3[17576]; static double *a4;
    a4 = (double *)l4;
    for (int i = 0; i < 17576; i++) a3[i] = 0; for (int i = 0; i < 676; i++) a2[i] = 0; for (int i = 0; i < 26; i++) a1[i] = 0;
    for (int i = 0; i < 456976; i++) { double p = pow(10, a4[i]); a3[i / 26] += p; a2[i / 676] += p; a1[i / 17576] += p; }
    static double b1[26], b2[676], b3[17576];
    for (int i = 0; i < 26; i++) b1[i] = log10(a1[i]);
    for (int i = 0; i < 676; i++) b2[i] = log10(a2[i]);
    for (int i = 0; i < 17576; i++) b3[i] = log10(a3[i]);
    L1 = b1; L2 = b2; L3 = b3; L4 = a4;
    NAP = 0; for (int a = 0; a + L < n; a++) if (known[a] >= 0 && known[a + L] >= 0) APA[NAP++] = a;
    /* breadth-first order of places from the known ones */
    int dec_[128] = {0}; for (int i = 0; i < n; i++) dec_[i] = known[i] >= 0;
    NSTEP = 0;
    for (;;) {   /* greedy: places that close a check first (both chain neighbours decoded), then contiguity */
        int bi = -1, bs = -1, bd = 0;
        for (int i = 0; i < n; i++) if (!dec_[i]) {
            int f = i - L >= 0 && dec_[i - L], b = i + L < n && dec_[i + L];
            if (!f && !b) continue;
            int sc = (f && b ? 4 : 0) + (i >= 1 && dec_[i - 1] ? 2 : 0) + (i + 1 < n && dec_[i + 1] ? 1 : 0);
            if (sc > bs) { bs = sc; bi = i; bd = f ? 1 : -1; }
        }
        if (bi < 0) {
            int f = -1; for (int i = 0; i < n; i++) if (!dec_[i]) { f = i; break; }
            if (f < 0) break;
            SPOS[NSTEP] = f; SDIR[NSTEP++] = 0; dec_[f] = 1; continue;
        }
        SPOS[NSTEP] = bi; SDIR[NSTEP++] = bd; dec_[bi] = 1;
    }
    int left = 0; for (int i = 0; i < n; i++) left += !dec_[i];
    return left;   /* places never reached (chains without a known letter) */
}
static double cond(const signed char *p, int i, int let) {
    /* log10 P(let | up to three decoded letters immediately left of i) */
    int a = i >= 1 ? p[i - 1] : -1, b = i >= 2 ? p[i - 2] : -1, c = i >= 3 ? p[i - 3] : -1;
    if (a >= 0 && b >= 0 && c >= 0) { int k = (c * 26 + b) * 26 + a; return L4[k * 26 + let] - L3[k]; }
    if (a >= 0 && b >= 0) { int k = b * 26 + a; return L3[k * 26 + let] - L2[k]; }
    if (a >= 0) return L2[a * 26 + let] - L1[a];
    return L1[let];
}
static inline int assign(struct St_ *s, int let, int v);
   /* known places a with a+L also known: relations no step visits */
static int anchorchecks(St *s) {
    for (int k = 0; k < NAP; k++) {
        int a = APA[k], b = a + L, ka = s->x[s->p[a]], pb = s->x[s->p[b]];
        if (ka < 0 || pb < 0) continue;
        if (!assign(s, C[b], encv(pb, ka))) return 0;
    }
    return 1;
}
/* every relation (a, a+L) with both plain letters decoded: verify, or force the carved letter's value; repeat until
   nothing changes (a forced value can enable another relation) */
static int fullchecks(St *s) {
    for (int changed = 1; changed;) {
        changed = 0;
        for (int a = 0; a + L < N; a++) {
            int b = a + L; if (s->p[a] < 0 || s->p[b] < 0) continue;
            int ka = s->x[s->p[a]], pb = s->x[s->p[b]], cv = s->x[C[b]];
            if (ka >= 0 && pb >= 0) {
                int need = encv(pb, ka);
                if (cv >= 0) { if (cv != need) return 0; }
                else { if (s->inv[need] >= 0) return 0; s->x[C[b]] = need; s->inv[need] = C[b]; changed = 1; }
            } else if (ka >= 0 && cv >= 0) {          /* p[b]'s letter must hold dec(cv, ka) */
                int v = dec(cv, ka);
                if (s->inv[v] >= 0) { if (s->inv[v] != s->p[b]) return 0; }
                else { s->x[s->p[b]] = v; s->inv[v] = s->p[b]; changed = 1; }
            } else if (pb >= 0 && cv >= 0) {          /* p[a]'s letter must hold the key value */
                int v = keyof(cv, pb);
                if (s->inv[v] >= 0) { if (s->inv[v] != s->p[a]) return 0; }
                else { s->x[s->p[a]] = v; s->inv[v] = s->p[a]; changed = 1; }
            }
        }
    }
    return 1;
}
static St *NEXT; static int NN, CAP;
static void heap_push(const St *s) {   /* min-heap on s, keep the CAP best */
    if (NN < CAP) {
        int i = NN++; NEXT[i] = *s;
        while (i > 0) { int up = (i - 1) / 2; if (NEXT[up].s <= NEXT[i].s) break; St t = NEXT[up]; NEXT[up] = NEXT[i]; NEXT[i] = t; i = up; }
        return;
    }
    if (s->s <= NEXT[0].s) return;
    NEXT[0] = *s; int i = 0;
    for (;;) { int l = 2 * i + 1, r = l + 1, m = i;
        if (l < NN && NEXT[l].s < NEXT[m].s) m = l; if (r < NN && NEXT[r].s < NEXT[m].s) m = r;
        if (m == i) break; St t = NEXT[m]; NEXT[m] = NEXT[i]; NEXT[i] = t; i = m; }
}
static inline int assign(struct St_ *s, int let, int v) {   /* 1 if consistent (assigning if needed) */
    if (s->x[let] >= 0) return s->x[let] == v;
    if (s->inv[v] >= 0) return 0;
    s->x[let] = v; s->inv[v] = let; return 1;
}
/* after p[i] is set: every relation (i, i+L) and (i-L, i) with both plain letters decoded must hold */
static int checks(St *s, int i) {
    for (int t = 0; t < 2; t++) {
        int a = t == 0 ? i - L : i, b = a + L;          /* key p[a] enciphers p[b] into C[b] */
        if (a < 0 || b >= N || s->p[a] < 0 || s->p[b] < 0) continue;
        int ka = s->x[s->p[a]], pb = s->x[s->p[b]];
        if (ka < 0 || pb < 0) continue;
        if (!assign(s, C[b], encv(pb, ka))) return 0;
    }
    return 1;
}
static void place_letter(St *s, int i, int v) {    /* p[i] has value v: branch over the letter holding v */
    if (s->inv[v] >= 0) {
        int let = s->inv[v];
        if (KNOWNL[i] >= 0 && KNOWNL[i] != let) return;
        St t = *s; t.p[i] = let; t.s += cond(t.p, i, let);
        if (fullchecks(&t)) heap_push(&t);
        return;
    }
    for (int let = 0; let < 26; let++) {
        if (s->x[let] >= 0) continue;
        if (KNOWNL[i] >= 0 && KNOWNL[i] != let) continue;
        St t = *s; t.x[let] = v; t.inv[v] = let; t.p[i] = let; t.s += cond(t.p, i, let);
        if (fullchecks(&t)) heap_push(&t);
    }
}
static void expand(const St *s, int step) {
    int i = SPOS[step], dir = SDIR[step];
    if (dir == 0) {                       /* a chain with no known letter: its first letter is free */
        for (int let = 0; let < 26; let++) {
            St t = *s; t.p[i] = let; t.s += cond(t.p, i, let);
            if (fullchecks(&t)) heap_push(&t);
        }
        return;
    }
    int src = dir > 0 ? i - L : i + L, cc = dir > 0 ? C[i] : C[i + L], ks = s->p[src];
    /* values needed: x of the decoded neighbour, x of the carved letter */
    int vk0 = s->x[ks], vc0 = s->x[cc];
    for (int vk = (vk0 >= 0 ? vk0 : 0); vk < (vk0 >= 0 ? vk0 + 1 : 26); vk++) {
        St a = *s;
        if (vk0 < 0 && !assign(&a, ks, vk)) continue;
        int vc1 = a.x[cc];
        for (int vc = (vc1 >= 0 ? vc1 : 0); vc < (vc1 >= 0 ? vc1 + 1 : 26); vc++) {
            St b = a;
            if (vc1 < 0 && !assign(&b, cc, vc)) continue;
            int v = dir > 0 ? dec(vc, vk) : keyof(vc, vk);
            place_letter(&b, i, v);
        }
    }
    (void)vc0;
}
static double fullscore(const signed char *p) {
    double s = 0; int n = 0;
    for (int i = 0; i + 3 < N; i++) { if (p[i] < 0 || p[i+1] < 0 || p[i+2] < 0 || p[i+3] < 0) return -99; s += L4[((p[i] * 26 + p[i + 1]) * 26 + p[i + 2]) * 26 + p[i + 3]]; n++; }
    return s / n;
}
/* returns the best full score; its reading in out (-1 open) and alphabet in xo; *nfinal = beam states at the end */
double beam(int B, int *out, int *xo, int *nfinal, const int *seedx) {
    St *cur = malloc(sizeof(St) * B), *nxt = malloc(sizeof(St) * B);
    int nc = 1;
    memset(&cur[0], -1, sizeof(St)); cur[0].s = 0;
    for (int i = 0; i < N; i++) cur[0].p[i] = KNOWNL[i] >= 0 ? KNOWNL[i] : -1;
    for (int i = 0; i < 26; i++) if (seedx[i] >= 0) { cur[0].x[i] = seedx[i]; cur[0].inv[seedx[i]] = i; }
    for (int step = 0; step < NSTEP; step++) {
        NEXT = nxt; NN = 0; CAP = B;
        for (int k = 0; k < nc; k++) expand(&cur[k], step);
        St *t = cur; cur = nxt; nxt = t; nc = NN;
        if (getenv("BEAMDBG")) fprintf(stderr, "step %d pos %d dir %d states %d best %.2f\n", step, SPOS[step], SDIR[step], nc, nc ? cur[0].s : 0.0);
        if (!nc) break;
    }
    double best = -99; int bi = -1;
    for (int k = 0; k < nc; k++) { double f = fullscore(cur[k].p); if (f > best) { best = f; bi = k; } }
    if (bi >= 0) { for (int i = 0; i < N; i++) out[i] = cur[bi].p[i]; for (int i = 0; i < 26; i++) xo[i] = cur[bi].x[i]; }
    *nfinal = nc;
    free(cur); free(nxt);
    return best;
}
"""


def main():
    B = int(sys.argv[1])
    idxs = [int(v) for v in sys.argv[2:]]
    spec = importlib.util.spec_from_file_location("probe", ROOT / "drafts" / "f1.13-split-probe.py")
    P = importlib.util.module_from_spec(spec); spec.loader.exec_module(P)
    from kryptos.facts import KNOWN
    from kryptos.scorer import _table, english_score
    d = tempfile.mkdtemp(prefix="k4_f113b_")
    open(os.path.join(d, "a.c"), "w").write(C_SRC)
    subprocess.run(["cc", "-O3", "-shared", "-fPIC", "-o", os.path.join(d, "a.so"), os.path.join(d, "a.c"), "-lm"], check=True)
    lib = ctypes.CDLL(os.path.join(d, "a.so"))
    lib.beam.restype = ctypes.c_double
    logs, floor = _table()
    tab = [floor] * (26 ** 4)
    for q, v in logs.items():
        if len(q) == 4 and q.isalpha() and q.isupper():
            tab[((ord(q[0]) - 65) * 26 + ord(q[1]) - 65) * 676 + (ord(q[2]) - 65) * 26 + ord(q[3]) - 65] = v
    T = (ctypes.c_double * len(tab))(*tab)
    plants, expect = P.plants_0256("pt")
    known = [-1] * N
    for q, c in KNOWN.items():
        known[q - 1] = ord(c) - 65
    for i in idxs:
        pl = plants[i]
        _, form, L = pl["cell"]
        left = lib.setup(T, N, L, ("V", "B", "R").index(form), (ctypes.c_int * N)(*[ord(c) - 65 for c in pl["ct"]]), (ctypes.c_int * N)(*known))
        t0 = time.time()
        out, xo, nf = (ctypes.c_int * N)(), (ctypes.c_int * 26)(), ctypes.c_int()
        seed = [-1] * 26
        if os.environ.get("SEEDTRUE"):
            k = int(os.environ["SEEDTRUE"])          # give the beam the true values of the first k letters
            for le in range(k):
                seed[le] = pl["alpha"].index(chr(65 + le))
        sc = lib.beam(B, out, xo, ctypes.byref(nf), (ctypes.c_int * 26)(*seed))
        rd = "".join("?" if out[j] < 0 else chr(65 + out[j]) for j in range(N))
        right = sum(a == b for a, b in zip(rd, pl["pt"]))
        print(f"pt/{i:2d} {pl['cls']:7s} {'/'.join(map(str, pl['cell'])):8s} unreached {left} true {english_score(pl['pt']):.3f} "
              f"beam {sc:.3f} letters {right}/97 final {nf.value} | 0256 {expect[f'pt/{i}']['score']} | {time.time() - t0:.0f}s", flush=True)
        # verify: the reading re-enciphers to the carved text at every place from L on, under the alphabet found
        x = list(xo); free = [v for v in range(26) if v not in x]
        x = [v if v >= 0 else free.pop() for v in x]
        ok = "?" not in rd and all(
            [lambda p, k: (p + k) % 26, lambda p, k: (k - p) % 26, lambda p, k: (p - k) % 26][("V", "B", "R").index(form)](
                x[ord(rd[j]) - 65], x[ord(rd[j - L]) - 65]) == x[ord(pl["ct"][j]) - 65] for j in range(L, N))
        print("   ", rd, "re-enciphers" if ok else "DOES NOT re-encipher")


if __name__ == "__main__":
    main()
