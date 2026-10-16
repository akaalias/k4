"""Experiment 0137. See program.md for the contract."""

EXPERIMENT = {
    "slug": "free-alphabet-climb-that-keeps-the-known-letters",
    "title": "F1.5 design 1: a climb that never breaks the 24 known letters, run in compiled code, measured on planted English before K4 (one free alphabet, Beaufort form, key lengths 23 and 26)",
    "family": "1-keyed-periodic",
    "parent": "0120-one-free-alphabet-english-climb-at-23-and-26",
    "changed": (
        "F1.5, step 2, design 1, on F1.1's two cells (Beaufort form, key lengths 23 and 26), which 0136 showed decidable by "
        "the quadgram test in principle (open bits 75 and 90 against 130). Three changes to 0120's climb: (1) every move keeps "
        "the 24 known letters consistent (swap two letters' places; if a check breaks, repair with a second swap chosen among "
        "those that restore every check), so no penalty term and the forced key values move only as the checks allow; (2) "
        "the score is the quadgram mean over all 97 letters with the known letters in place, so the unknown letters next to "
        "the known runs are scored in context; (3) the inner loop is compiled C (written out and compiled by this file, "
        "loaded with ctypes; about 150 times faster than 0120's Python), so each text gets 1,000 restarts of 100,000 moves "
        "instead of 20. Power is measured on 12 planted texts per length before K4's verdict counts."
    ),
    "hypothesis_expert": (
        "C27(c) (a tableau 'slightly different from the one on Kryptos', research_notes/sanborn_charts and the NYT "
        "'Original Decoding Charts' email, knowledge/11-clue-register.md), C1(b) (the table alone). Model as 0120: one "
        "unknown bijection x (letter -> place) on both sides, Beaufort form x(c_i) + x(p_i) = k[i mod L] mod 26, L in "
        "{23, 26}; 0119 left only these (form, length) pairs. Given x, the key at a slot holding a known letter is forced; "
        "the other slots (6 at 23, 3 at 26) are free. Checks: 7 at L 23 (x(c1)+x(p1) = x(c2)+x(p2) for two known letters "
        "in a slot), 1 at L 26. Search: simulated annealing over x restricted to the set where every check holds (start: a "
        "random depth-first assignment that satisfies the checks; move: swap two letters' places, repaired by a second swap "
        "if a check breaks) and over the free key values; objective the mean log10 quadgram over the whole 97-letter text "
        "with the known letters in place; T 0.05 -> 0.002 geometric; 1,000 restarts x 100,000 moves per text. Dry runs on "
        "planted texts before this record (scratch, stated here): started from the true alphabet with k random "
        "check-keeping swaps (free key values true), the climb returned to the exact plaintext for k up to about 12 and "
        "rarely from 15-20; from random starts no restart of 960 (100,000 or 1,000,000 moves) recovered a plant, the best "
        "reaching -4.85 to -5.0 against true scores of -4.1 to -4.4, with 11-16 of the 73 unknown letters right. Bar, set "
        "before the run, stricter than 0120's half because 0120's 3 of 6 at that bar was judged weak: a plant is found if "
        "its best score is above every copper's best at that length; the design passes at a length if at least 9 of 12 "
        "plants are found. Recovery (90 or more of 97 letters right) is reported apart. Key cost of a reading here: 88.4 "
        "bits of alphabet plus 4.7 per key letter."
    ),
    "hypothesis_eli5": (
        "For one kind of cipher (one scrambled alphabet, a repeating key of 23 or 26 letters, used the Beaufort way), "
        "the 24 known letters cannot rule the carved text in or out, but 73 letters of English could, in principle. "
        "An earlier search failed to find hidden English of this kind even when we planted it ourselves. This search "
        "only ever moves between settings that keep the 24 known letters right, reads the whole message including the "
        "known words, and runs about 150 times faster, so it can try 1,000 fresh starts per text. Before believing what "
        "it says about the carved text, we check how often it notices planted messages compared with scrambled copies."
    ),
    "prediction": (
        "No planted text recovered (90+ letters right) at either length, as in the dry runs. Detection only through the "
        "partial correctness the dry runs showed: at 23, fewer than 9 of 12 plants above every copper, so the design fails "
        "the bar; at 26 (one check) fewer still. K4 inside its coppers' range at both lengths. If a length reaches 9 of "
        "12, that length's K4 verdict counts as sampled at the measured power, and a K4 score above every copper stops "
        "the queue for a replication."
    ),
    "method": (
        "1. Compile the C climb; check on a planted text that its plaintext equals a Python Beaufort decryption under the "
        "alphabet and key it returns. "
        "2. Draw 12 shuffles of K4 that fit exactly at each length (0119's decider) and 12 planted texts per length "
        "(Carter windows, known letters written in, random alphabet and key; 0120's generator). "
        "3. For K4, each copper and each plant: 1,000 restarts x 100,000 moves, best score kept, restarts done recorded. "
        "4. Per length: plants found (above every copper), plants recovered, K4 against the coppers. "
        "5. Return K4's best reading per length as a candidate with the coppers' scores as controls."
    ),
    "walkthrough": (
        "1. Write K4 in rows of 23; each column is one key slot. "
        "2. Choose an order for the alphabet that keeps the known letters consistent: in every column holding two known letters, place(carved) + place(known) must come out the same for both. "
        "3. The key value of a column with a known letter is that sum; give the other six columns any value. "
        "4. Decipher every letter: message place = key value minus carved place, mod 26, read back through the alphabet. "
        "5. Score the whole 97 letters, known words included, by how English their four-letter groups are. "
        "6. Swap two letters of the alphabet; if a column's two known letters now disagree, swap another pair that makes every column agree again. "
        "7. Keep the change if the score improves (sometimes even if not, less often as the search cools); repeat 100,000 times, then start again from a new order, 1,000 times. "
        "8. Do the same on scrambled copies of K4 and on planted English, and compare the best scores."
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
    from kryptos.scorer import english_score, free_text
    ct, known = ctx.K4, ctx.KNOWN
    m0120 = load_0120()
    rng = random.Random(137)
    lib()
    # step 1: the compiled climb against a Python decryption on one plant
    (pc, ppt, palpha, pk), = m0120.make_plants(known, 23, random.Random(1370), 1, with_key=True)
    sc0, pt0, al0, k0, _ = climb_text(pc, known, 23, 1, 2 * CHUNK, time.time() + 600)
    assert beaufort_decrypt(pc, al0, k0) == pt0, "C decryption disagrees with Python"
    assert beaufort_decrypt(pc, palpha, pk) == ppt and beaufort_encrypt(ppt, palpha, pk) == pc
    jobs, truth_scores = [], {}
    deadline = ctx.deadline - 120
    for L in LENGTHS:
        assert m0120.decide(m0120.equations(ct, known, L), "B")[0] == "fit"
        jobs.append(("k4", L, 0, ct, None, rng.randrange(10 ** 9), deadline))
        got = 0
        while got < N_CONTROLS:
            sh = list(ct); rng.shuffle(sh); sh = "".join(sh)
            if m0120.decide(m0120.equations(sh, known, L), "B", rng)[0] == "fit":
                jobs.append(("copper", L, got, sh, None, rng.randrange(10 ** 9), deadline)); got += 1
        for i, (pc, pt) in enumerate(m0120.make_plants(known, L, rng, N_PLANTS)):
            truth_scores[(L, i)] = english_score(pt)
            jobs.append(("plant", L, i, pc, pt, rng.randrange(10 ** 9), deadline))
    jobs.sort(key=lambda j: j[0] != "k4")
    if getattr(sys.modules.get(__name__), "_job", None) is not _job:
        m = types.ModuleType(__name__); m.__dict__.update(globals()); sys.modules[__name__] = m
    with mp.get_context("fork").Pool(8) as pool:
        res = pool.map(_job, jobs, chunksize=1)
    out = {L: {"k4": None, "copper": [], "plant": []} for L in LENGTHS}
    cands, controls, all_ok, done_all = [], [], True, []
    for kind, L, idx, sc, pt, alpha, k, agree, done, ok in res:
        all_ok = all_ok and ok
        done_all.append(done)
        rec = {"score": round(sc, 4), "english_free": round(english_score(free_text(pt)), 4) if pt else None, "restarts": done}
        if kind == "k4":
            rec.update({"plaintext": pt, "alphabet": alpha, "key": k})
            out[L]["k4"] = rec
            if pt:
                cands.append({"plaintext": pt, "key": {"alphabet": alpha, "shifts": k, "form": "beaufort"},
                              "key_description": f"Beaufort form, one alphabet {alpha} on both sides, key length {L}",
                              "notes": f"length {L}, best of {done} restarts"})
        elif kind == "copper":
            out[L]["copper"].append(rec)
            if rec["english_free"] is not None:
                controls.append(rec["english_free"])
        else:
            rec.update({"letters_right": agree, "true_score": round(truth_scores[(L, idx)], 4), "plaintext": pt})
            out[L]["plant"].append(rec)
    summary = {}
    for L in LENGTHS:
        cs = [r["score"] for r in out[L]["copper"]]
        top = max(cs)
        for pl in out[L]["plant"]:
            pl["found"] = pl["score"] > top
            pl["recovered"] = (pl["letters_right"] or 0) >= 90
        k4s = out[L]["k4"]["score"]
        found = sum(1 for pl in out[L]["plant"] if pl["found"])
        summary[L] = {"k4": k4s, "coppers_min": min(cs), "coppers_max": top,
                      "k4_rank_among_coppers": 1 + sum(1 for c in cs if c > k4s),
                      "k4_above_all_coppers": k4s > top,
                      "plants_found": found, "plants_recovered": sum(1 for pl in out[L]["plant"] if pl["recovered"]),
                      "passes_bar": found >= FOUND_BAR,
                      "plants_scores": sorted(pl["score"] for pl in out[L]["plant"]),
                      "plants_true_scores": sorted(pl["true_score"] for pl in out[L]["plant"]),
                      "plants_letters_right": [pl["letters_right"] for pl in out[L]["plant"]]}
    bounds = {
        "family": "one unknown alphabet on both sides, Beaufort form, periodic key 23 or 26, no move (F1.1's two cells)",
        "search": f"simulated annealing in the set where every known-letter check holds, compiled C, {RESTARTS} restarts x {ITERS:,} moves per text (chunks of {CHUNK}), T {T0}->{T1} geometric, full-text quadgram mean",
        "not_exhaustive": True,
        "restarts_done": {"min": min(done_all), "max": max(done_all)},
        "c_decryption_checked": all_ok,
        "bar": f"plant found if its best score is above every copper's best; design passes at a length if >= {FOUND_BAR} of {N_PLANTS} found",
        "coppers_per_length": N_CONTROLS, "plants_per_length": N_PLANTS,
        "summary": {str(L): v for L, v in summary.items()},
        "coppers": {str(L): sorted(r["score"] for r in out[L]["copper"]) for L in LENGTHS},
        "k4_best": {str(L): out[L]["k4"] for L in LENGTHS},
        "plants": {str(L): out[L]["plant"] for L in LENGTHS},
        "controls": f"{N_CONTROLS} shuffled coppers per length that fit exactly at that length and form (0119's decider, seed 137), identical climb",
    }
    notes = "; ".join(f"L{L}: K4 {summary[L]['k4']:.3f} (rank {summary[L]['k4_rank_among_coppers']} of 13), coppers {summary[L]['coppers_min']:.3f} to {summary[L]['coppers_max']:.3f}, "
                      f"plants found {summary[L]['plants_found']}/{N_PLANTS}, recovered {summary[L]['plants_recovered']}" for L in LENGTHS)
    return {"candidates": cands, "bounds": bounds, "notes": notes, "controls": controls}


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
