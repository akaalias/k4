"""Experiment 0193 (F8.1). See program.md for the contract."""

EXPERIMENT = {
    "slug": "hill-2x2-unknown-numbering",
    "title": "F8.1: Hill 2x2 with an unknown one-to-one letter numbering (any of 26!), every invertible matrix, both alignments: exact; 3x3 counted and blocked",
    "family": "8-hill",
    "parent": "0116-hill-plus-periodic-key",
    "changed": (
        "F8.1. Earlier Hill tests fixed the numbering (4 standard, 126 vocabulary, 200 K1-K3 words; 0015, 0044, 0055). "
        "Here the numbering is free. Counting first: at either alignment 11 digraphs of K4 lie wholly inside the known "
        "runs, 22 linear equations mod 26 (about 103 bits) in the numbers of 20-21 letters (79-81 bits) and the 4 matrix "
        "entries (17 bits): a surplus of 5-7 bits, so an exact test has power. For 3x3, 6-7 trigraphs give 18-21 "
        "equations against 76-81 + 41 bits: 21-32 bits short, no checks, blocked. For each of the 157,248 invertible 2x2 "
        "matrices and each alignment, a depth-first search with propagation looks for a one-to-one numbering satisfying "
        "all 22 equations (compiled). K4 against 5 shuffled copies (each takes minutes); plants with random numberings."
    ),
    "hypothesis_expert": (
        "C21(a) (the HILL column of the tableau), F8. Model: x a one-to-one map letters -> Z26; for each aligned block, "
        "(x[c1], x[c2]) = M (x[p1], x[p2]) mod 26 with M invertible. Encryption and decryption matrices, row and column "
        "conventions are all covered by enumerating every invertible M. Statistic: matrices admitting a numbering, K4 "
        "against 5 copies; expected on a random text about 2^-5 to 2^-7 per alignment in total."
    ),
    "hypothesis_eli5": (
        "The tableau's last column spells HILL, the name of a cipher that mixes letters in pairs with a little matrix of "
        "numbers. It was tried with the usual ways of numbering the letters. Here the numbering itself is a secret: any "
        "order of the alphabet. The known words still give enough pairs to decide it exactly, for every possible matrix."
    ),
    "prediction": "No matrix admits a numbering on K4 at either alignment; copies mostly none; plants found. Zero candidates.",
    "method": (
        "1. For each alignment: the digraphs wholly inside the known runs (11 each). "
        "2. For each invertible 2x2 matrix: two equations per digraph; search for a one-to-one numbering with "
        "propagation (node limit 200,000, undecided counted). "
        "3. K4, 5 shuffled copies, 3 planted Hill texts with random numberings and matrices."
    ),
    "walkthrough": (
        "1. Pair the message from place 1: places 21-22 are not both known, 23-24 (A S) are, over the carved L R. "
        "2. With matrix (a b; c d): a*n(A) + b*n(S) = n(L) and c*n(A) + d*n(S) = n(R), where n is the secret numbering. "
        "3. Eleven such pairs give 22 equations; choosing numbers for two or three letters forces the rest. "
        "4. If no one-to-one numbering survives, that matrix is out. "
        "5. All 157,248 invertible matrices, both pairings, K4 and scrambled copies."
    ),
}

import ctypes
import os
import random
import subprocess
import tempfile
import time

from kryptos.facts import KNOWN

N_CONTROLS = 5
LIMIT = 200000

C_SOURCE = r"""
// Hill 2x2 with an unknown one-to-one letter numbering x[]: for each aligned block (p1 p2) -> (c1 c2) fully known,
// a*x[p1] + b*x[p2] - x[c1] = 0 and c*x[p1] + d*x[p2] - x[c2] = 0 (mod 26). For each invertible matrix: does some
// numbering satisfy all? Depth-first search with propagation (ternary linear equations, one-to-one), node limit.
#include <string.h>
#define ME 48
static int EV[ME][3], EA[ME][3], NEQ;
static int X[26], USED[26];
static long NODES, LIMIT;
static int BP1[24], BP2[24], BC1[24], BC2[24], NB;

static int propagate(int *trail, int *nt) {
    int changed = 1;
    while (changed) {
        changed = 0;
        for (int e = 0; e < NEQ; e++) {
            int open = -1, nopen = 0, s = 0;
            for (int j = 0; j < 3; j++) {
                if (!EA[e][j]) continue;
                int v = EV[e][j];
                if (X[v] < 0) { if (open != v) { nopen++; open = v; } }
                else s += EA[e][j] * X[v];
            }
            if (nopen == 0) { if (((s % 26) + 26) % 26) return 0; continue; }
            if (nopen > 1) continue;
            int a = 0;
            for (int j = 0; j < 3; j++) if (EA[e][j] && EV[e][j] == open) a += EA[e][j];
            a = ((a % 26) + 26) % 26;
            int sols = 0, last = -1;
            for (int t = 0; t < 26; t++) if (!USED[t] && ((a * t + s) % 26 + 26) % 26 == 0) { sols++; last = t; }
            if (!sols) return 0;
            if (sols == 1) { X[open] = last; USED[last] = 1; trail[(*nt)++] = open; changed = 1; }
        }
    }
    return 1;
}
static int VARS[26], NV;
static int dfs(void) {
    if (++NODES > LIMIT) return -1;
    int trail[26], nt = 0;
    if (!propagate(trail, &nt)) { for (int i = 0; i < nt; i++) { USED[X[trail[i]]] = 0; X[trail[i]] = -1; } return 0; }
    int pick = -1, best = -1;
    for (int i = 0; i < NV; i++) {
        int v = VARS[i];
        if (X[v] >= 0) continue;
        int sc = 0;
        for (int e = 0; e < NEQ; e++) {
            int unk = 0, has = 0;
            for (int j = 0; j < 3; j++) if (EA[e][j]) { if (EV[e][j] == v) has = 1; else if (X[EV[e][j]] < 0) unk++; }
            if (has) sc += unk == 0 ? 4 : unk == 1 ? 2 : 1;
        }
        if (sc > best) { best = sc; pick = v; }
    }
    if (pick < 0) return 1;
    for (int t = 0; t < 26; t++) {
        if (USED[t]) continue;
        X[pick] = t; USED[t] = 1;
        int r = dfs();
        if (r == 1) return 1;
        X[pick] = -1; USED[t] = 0;
        if (r < 0) { for (int i = 0; i < nt; i++) { USED[X[trail[i]]] = 0; X[trail[i]] = -1; } return -1; }
    }
    for (int i = 0; i < nt; i++) { USED[X[trail[i]]] = 0; X[trail[i]] = -1; }
    return 0;
}
static void add_eq(int c0, int v0, int c1, int v1, int c2, int v2) {
    int a[3] = {c0, c1, c2}, v[3] = {v0, v1, v2};
    for (int i = 0; i < 3; i++) for (int j = i + 1; j < 3; j++) if (a[j] && v[j] == v[i]) { a[i] += a[j]; a[j] = 0; }
    int any = 0;
    for (int j = 0; j < 3; j++) { a[j] = ((a[j] % 26) + 26) % 26; EV[NEQ][j] = v[j]; EA[NEQ][j] = a[j]; if (a[j]) any = 1; }
    if (any) NEQ++;
}
void set_blocks(int nb, const int *p1, const int *p2, const int *c1, const int *c2) {
    NB = nb; for (int i = 0; i < nb; i++) { BP1[i] = p1[i]; BP2[i] = p2[i]; BC1[i] = c1[i]; BC2[i] = c2[i]; }
}
// returns 1 fit, 0 dead, -1 undecided; xout gets the numbering
int decide(int a, int b, int c, int d, long limit, int *xout) {
    NEQ = 0;
    for (int i = 0; i < NB; i++) {
        add_eq(a, BP1[i], b, BP2[i], -1, BC1[i]);
        add_eq(c, BP1[i], d, BP2[i], -1, BC2[i]);
    }
    for (int i = 0; i < 26; i++) { X[i] = -1; USED[i] = 0; }
    int seen[26] = {0}; NV = 0;
    for (int e = 0; e < NEQ; e++) for (int j = 0; j < 3; j++) if (EA[e][j] && !seen[EV[e][j]]) { seen[EV[e][j]] = 1; VARS[NV++] = EV[e][j]; }
    NODES = 0; LIMIT = limit;
    int r = dfs();
    if (xout) for (int i = 0; i < 26; i++) xout[i] = X[i];
    return r;
}
// all invertible matrices: counts fit/dead/undecided; fit matrices listed
void scan(long limit, long *counts, int *fitm, int cap, int *nfit, long *maxnodes) {
    for (int a = 0; a < 26; a++) for (int b = 0; b < 26; b++) for (int c = 0; c < 26; c++) for (int d = 0; d < 26; d++) {
        int det = ((a * d - b * c) % 26 + 26) % 26;
        if (det % 2 == 0 || det % 13 == 0) continue;
        int r = decide(a, b, c, d, limit, 0);
        if (NODES > *maxnodes) *maxnodes = NODES;
        if (r == 1) { counts[0]++; if (*nfit < cap) { fitm[4 * *nfit] = a; fitm[4 * *nfit + 1] = b; fitm[4 * *nfit + 2] = c; fitm[4 * *nfit + 3] = d; (*nfit)++; } }
        else if (r == 0) counts[1]++;
        else counts[2]++;
    }
}
"""


def build():
    d = tempfile.mkdtemp(prefix="k4_hill_")
    src, so = os.path.join(d, "c.c"), os.path.join(d, "c.so")
    open(src, "w").write(C_SOURCE)
    subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", so, src], check=True, capture_output=True)
    return so


def job(args):
    so, ti, text, a = args
    lib = ctypes.CDLL(so)
    b = blocks(text, a)
    lib.set_blocks(len(b), I([x[0] for x in b]), I([x[1] for x in b]), I([x[2] for x in b]), I([x[3] for x in b]))
    cnt = (ctypes.c_long * 3)(); fm = (ctypes.c_int * 400)(); nf = ctypes.c_int(0); mx = ctypes.c_long(0)
    lib.scan(ctypes.c_long(LIMIT), cnt, fm, 100, ctypes.byref(nf), ctypes.byref(mx))
    return ti, a, list(cnt), len(b), [list(fm[4 * j:4 * j + 4]) for j in range(nf.value)], mx.value


def I(v):
    return (ctypes.c_int * len(v))(*v)


def blocks(text, a):
    out = []
    for st in range(a, 96, 2):
        i, j = st + 1, st + 2
        if i in KNOWN and j in KNOWN:
            out.append((ord(KNOWN[i]) - 65, ord(KNOWN[j]) - 65, ord(text[i - 1]) - 65, ord(text[j - 1]) - 65))
    return out


def encipher(p, M, num, a):
    inv = [0] * 26
    for L, v in enumerate(num):
        inv[v] = L
    out = list(p)
    for st in range(a, len(p) - 1, 2):
        x, y = num[ord(p[st]) - 65], num[ord(p[st + 1]) - 65]
        out[st] = chr(65 + inv[(M[0] * x + M[1] * y) % 26]); out[st + 1] = chr(65 + inv[(M[2] * x + M[3] * y) % 26])
    return "".join(out)


def run(ctx):
    t0 = time.time()
    lib = build()
    ct = ctx.K4
    rng = random.Random(1930)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    PLANT_P = "USEDTHEEARTHSMAGNETICEASTNORTHEASTRMATIONWASGATHEREDANDTRANSMITBERLINCLOCKUNDTOANUNKNOWNLOCATIONX"
    plants = []
    for k in range(3):
        while True:
            M = [rng.randrange(26) for _ in range(4)]
            det = (M[0] * M[3] - M[1] * M[2]) % 26
            if det % 2 and det % 13:
                break
        num = list(range(26)); rng.shuffle(num)
        a = k % 2
        texts.append(encipher(PLANT_P, M, num, a))
        plants.append({"matrix": M, "alignment": a})
    nc = 1 + N_CONTROLS
    import multiprocessing as mp
    so = lib
    with mp.get_context("fork").Pool(4) as pool:
        out = pool.map(job, [(so, ti, t, a) for ti, t in enumerate(texts) for a in (0, 1)], chunksize=1)
    res = [dict() for _ in texts]
    k4_fits = []
    maxn = 0
    for ti, a, cnt, nb, fm, mx in out:
        maxn = max(maxn, mx)
        res[ti][a] = {"fit": cnt[0], "dead": cnt[1], "undecided": cnt[2], "blocks": nb}
        if ti == 0:
            k4_fits += [{"alignment": a, "matrix": m} for m in fm]
        if ti >= nc:
            p = plants[ti - nc]
            if p["alignment"] == a:
                p["true_matrix_fits"] = p["matrix"] in fm
                p["fitting_matrices"] = cnt[0]
    fits = [r[0]["fit"] + r[1]["fit"] for r in res]
    und = [r[0]["undecided"] + r[1]["undecided"] for r in res]
    bounds = {
        "family": "Hill 2x2, any invertible matrix, any one-to-one numbering, alignments 0 and 1, exact",
        "matrices": 157248, "blocks_per_alignment": {a: res[0][a]["blocks"] for a in (0, 1)},
        "fitting_matrices": {"k4": fits[0], "copies": fits[1:nc]}, "undecided": {"k4": und[0], "copies": und[1:nc]},
        "max_nodes": maxn, "k4_fits": k4_fits[:20], "plants": plants,
        "count_3x3": "6-7 trigraphs, 18-21 equations (85-99 bits) against 76-81 bits of numbering and 41 of matrix: 21-32 bits short; blocked",
        "copies": f"{N_CONTROLS} shuffled copies (seed 1930)", "seconds": round(time.time() - t0), "exhaustive": True,
    }
    notes = (f"matrices admitting a numbering: K4 {fits[0]} (copies {min(fits[1:nc])}-{max(fits[1:nc])}); undecided K4 {und[0]}; "
             f"plants: {[(p.get('true_matrix_fits'), p.get('fitting_matrices')) for p in plants]}")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    lines = ["digraphs wholly inside the known runs, pairing from place 1", ""]
    for p1, p2, c1, c2 in blocks(ctx.K4, 0):
        lines.append(f"{chr(65 + p1)}{chr(65 + p2)} -> {chr(65 + c1)}{chr(65 + c2)}")
    return "\n".join(lines)
