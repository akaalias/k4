"""Experiment 0138. See program.md for the contract."""

EXPERIMENT = {
    "slug": "climb-power-against-each-plants-own-copies",
    "title": "F1.5 design 1, checked: is the climb's power at key length 23 about English order? Each planted text against scrambled copies of itself",
    "family": "1-keyed-periodic",
    "parent": "0137-free-alphabet-climb-that-keeps-the-known-letters",
    "changed": (
        "F1.5, validity check of design 1 before its pass at length 23 is used. 0137 counted a planted text as found when its "
        "best climbed score beat every scrambled copy of K4 (10 of 12 at 23). But a planted ciphertext and K4 differ in more "
        "than word order: their letter counts differ (planted ciphertexts average an index of coincidence of 0.039, K4 has "
        "0.036, at the 17th percentile of plants), and shuffles of K4 fit length 23 rarely while shuffles of a plant fit 43% "
        "of the time. Here each of 12 new planted texts is compared only with 6 shuffles of its own letters that fit length 23 "
        "exactly, so the only difference left is the order of the letters. Same climb, same effort as 0137."
    ),
    "hypothesis_expert": (
        "C27(c), C1(b) as 0137. Cell: one unknown alphabet on both sides, Beaufort form, key length 23 (7 checks). Climb: "
        "0137's compiled annealing in the set where every known-letter check holds, 1,000 restarts x 100,000 moves per text, "
        "full-text quadgram mean. Plants: 12 Carter windows (knowledge/sources/carter-1923-tomb-of-tutankhamen-vol1.txt) with "
        "the known letters written in, random alphabet and key (0120's generator, seed 138). Own coppers: for each plant, 6 "
        "shuffles of its ciphertext that fit length 23 exactly (0119's decider). Null: if the climb reads no English order, a "
        "plant beats all 6 of its own coppers with chance 1/7, so about 1.7 of 12. Bar, fixed before the run: design 1's "
        "power at 23 stands if at least 9 of 12 plants beat all 6 of their own coppers; otherwise 0137's pass is withdrawn and "
        "F1.1 Beaufort 23 goes back to blocked. Also reported: each plant's rank among its own coppers and among 0137's K4 "
        "coppers."
    ),
    "hypothesis_eli5": (
        "The last experiment's search seemed able to notice hidden English: planted messages climbed higher than scrambled "
        "copies of the carved text. But the planted messages and the carved text also differ in how often each letter "
        "appears, and that alone might help the search. Here each planted message is compared only with scrambled copies "
        "of itself, which have exactly the same letters in a different order. If the search still picks out the planted "
        "message, it is reading English word order, and its verdict on the carved text can be trusted at that strength."
    ),
    "prediction": (
        "At least 9 of 12 plants beat all 6 of their own coppers (the order of English letters is what the climb reads; "
        "partial correctness, 11-16 of 73 unknown letters right in 0137, needs order). If fewer, the power claimed in 0137 "
        "came from letter counts and F1.1 Beaufort 23 returns to blocked. No plant recovered (90+ letters right). Zero "
        "candidates."
    ),
    "method": (
        "1. Draw 12 planted texts at length 23 (seed 138). "
        "2. For each, shuffle its ciphertext until 6 shuffles fit length 23 exactly (0119's decider). "
        "3. Run 0137's climb on all 84 texts at 0137's effort. "
        "4. Per plant: found if its best is above all 6 of its own coppers; rank among them; rank among 0137's K4 coppers."
    ),
    "walkthrough": (
        "1. Take a passage of English, write EASTNORTHEAST and BERLINCLOCK in at their places, and encipher it with a random alphabet and a random 23-letter key, the Beaufort way. "
        "2. Shuffle its 97 carved letters into a new order; keep the shuffle only if some alphabet and key could still give the 24 known letters at their places. Make six such shuffles. "
        "3. Run the same search on the planted text and on its six shuffles, and note each best score. "
        "4. The planted text counts as noticed if it beats all six; by luck alone that happens one time in seven. "
        "5. Repeat for twelve planted texts."
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
N_PLANTS = 12
RESTARTS = 1000
ITERS = 100000
CHUNK = 50
T0, T1 = 0.05, 0.002
FOUND_BAR = 9
N_OWN = 6
OWN_BAR = 9
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
        L_.climb.restype = ctypes.c_double
        L_.climb.argtypes = [ctypes.c_uint64, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double,
                             ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int),
                             ctypes.POINTER(ctypes.c_double)]
        from kryptos.scorer import _table
        logs, floor = _table()
        tab = [floor] * (26 ** 4)
        for q, v in logs.items():
            if len(q) == 4 and q.isalpha() and q.isupper():
                tab[((ord(q[0]) - 65) * 26 + ord(q[1]) - 65) * 676 + (ord(q[2]) - 65) * 26 + ord(q[3]) - 65] = v
        _LIB["tab"] = (ctypes.c_double * len(tab))(*tab)
        _LIB["lib"] = L_
    return _LIB["lib"]


def climb_text(text, known, L, seed, restarts, deadline):
    """Run restarts in chunks; return (best score, plaintext, alphabet, key, restarts done)."""
    L_ = lib()
    kp = sorted(known)
    CT = (ctypes.c_int * N)(*[ord(ch) - 65 for ch in text])
    KP = (ctypes.c_int * 24)(*[q - 1 for q in kp])
    KL = (ctypes.c_int * 24)(*[ord(known[q]) - 65 for q in kp])
    L_.setup(_LIB["tab"], CT, N, L, KP, KL, 24)
    best = (-99.0, None, None, None)
    done = 0
    while done < restarts and time.time() < deadline:
        bp = (ctypes.c_int * 128)(); bx = (ctypes.c_int * 26)(); bk = (ctypes.c_int * 64)()
        sc = L_.climb(seed * 100003 + done, CHUNK, ITERS, T0, T1, bp, bx, bk, None)
        done += CHUNK
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
    rng = random.Random(138)
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
        "search": f"0137's compiled climb, {RESTARTS} restarts x {ITERS:,} moves per text, T {T0}->{T1}",
        "plants": N_PLANTS, "own_coppers_per_plant": N_OWN, "shuffles_tried": tried,
        "restarts_done": {"min": min(done_all), "max": max(done_all)}, "c_decryption_checked": all_ok,
        "null_rate_found": round(1 / (N_OWN + 1), 4), "null_expected_found": round(N_PLANTS / (N_OWN + 1), 2),
        "bar": f"design 1's power at 23 stands if >= {OWN_BAR} of {N_PLANTS} plants beat all {N_OWN} of their own coppers",
        "plants_found_against_own": found, "passes_bar": found >= OWN_BAR,
        "plants_recovered": sum(1 for p in rows if p["recovered"]),
        "plants_found_against_0137_k4_coppers": sum(1 for p in rows if p["rank_among_k4_coppers_0137"] == 1),
        "rows": rows,
        "controls": "per plant, 6 shuffles of its own ciphertext that fit length 23 exactly (0119's decider, seed 138)",
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
