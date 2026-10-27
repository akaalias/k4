"""Experiment 0237. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f13-a-move-and-the-sculptures-table-ciphertext-only",
    "title": "F13.4d: every move of the type-1 library (27,852), before or after a periodic key on the sculpture's 8 table classes, key lengths 1-20, from the ciphertext alone; F6.1's free alphabet after a move blocked by 0236's power",
    "family": "13-ciphertext-only",
    "parent": "0234-f13-periodic-key-on-the-sculptures-tables-ciphertext-only",
    "changed": (
        "F13.4d (issue #85). 0234 solved the sculpture's tables with no move from the ciphertext alone; here every move of "
        "0129's type-1 library (K3's rule at every shift, quarter turns, columnar and double turns at every width, the "
        "keyword columnars of the vocabulary; forward and inverse) is put before (A: move, then the table) or after (B: "
        "the table, then the move) the periodic key, key lengths 1-20, 8 table classes. A climb per setting is about 12 "
        "hours per text, so: for A the column statistics do not depend on the move, so each column's shift comes from one "
        "letter-frequency screen per class and length and every move is then scored by quadgrams; for B each move is "
        "undone first and then screened. The 30 best settings per order and length get 0234's coordinate-ascent climb "
        "(the move held) and MIX8m rescoring. Statistic, copies and plants as 0234. F6.1 (one free alphabet after a move) "
        "is not run: 0236 found one free alphabet cannot be recovered from the ciphertext alone beyond length 5 with no "
        "move at all, and 27,852 moves only add alternatives. Cost stated before the run: 541 texts x about 25 s, about "
        "4 core-hours."
    ),
    "hypothesis_expert": (
        "F6 (Sanborn's 'matrix codes... then went back to this table', C1(a); K3's rule, C2(a)) read without the known "
        "letters: the hedge for A2 (the known letters defined on an intermediate text) and A1 on the family ranked second. "
        "F13.1 puts a move and a fixed-table key decidable by quadgrams (log2 27,852 = 14.8 bits for the move, 3 for the "
        "class and order, 4.7 per key letter: 112 bits at 20, under MIX8m's 189). Pre-registered: S = max over (order, "
        "length) of the z-score of the best MIX8m log-probability against K4's 100 climbed shuffles; K4 flags at p < "
        "0.05; plants at lengths 3, 5, 8, 12, 20 (half each order, random move and class), each against 10 own shuffles; "
        "a length is decided at 6 of 8. The item closes for the decided lengths and is blocked above."
    ),
    "hypothesis_eli5": (
        "Sanborn said he scrambled with 'matrix codes' and then used the table. Here the scramble is any of 27,852 grid "
        "moves we have listed, done before or after the table with a repeating secret word, and the whole thing is solved "
        "from the carved letters alone. For each guess of the scramble and the word length, the quick letter-count test "
        "picks each column's shift; the most English-looking guesses are then improved and compared with shuffles of K4."
    ),
    "prediction": (
        "Plants found at 3 and 5 (8/8), most at 8, few at 12, none at 20: decided to about 8. K4 inside its shuffles "
        "(p above 0.05), its readings at most 4-5 known letters. F13.4d closes for the short lengths, blocked above; F6.1 "
        "blocked by 0236."
    ),
    "method": (
        "1. Moves: 0129's route_library (forward and inverse, distinct), rebuilt here from the vocabulary. "
        "2. Order A: per class and length, each column's shift by English letter frequency on the carved text; the "
        "decryption read through each move (letter i of the message is carved at where[i]) and scored by quadgrams. "
        "Order B: each move undone on the carved text, then each column's shift by letter frequency, and the reading "
        "scored by quadgrams. The 30 best (move, class) per order and length kept (C). "
        "3. Those climbed by coordinate ascent on the shifts, the move held (screen's shifts and 5 random starts); "
        "rescored by MIX8m (0233); per order and length the best. "
        "4. S = max z over the 40 cells against K4's 100 shuffles; K4 ranked; each plant against 10 own shuffles. "
        "5. K4's best reading per cell submitted (key: move, order, class, shifts)."
    ),
    "walkthrough": (
        "1. Pick a grid move from the list, for instance K3's rule or a keyword columnar. "
        "2. Either undo the move on the carved letters first (table last) or keep it for the end (table first). "
        "3. Write the letters in as many columns as the key is long and choose each column's shift by letter counts. "
        "4. Read the result in the message's order and score it as English. "
        "5. Keep the best guesses, improve their shifts, and compare K4's best with what shuffles of K4 reach."
    ),
    "expected_minutes": 30,
}

import ctypes
import importlib.util
import os
import random
import subprocess
import sys
import tempfile
import time
import types
from pathlib import Path

import numpy as np

N = 97
ROOT = Path(__file__).resolve().parent
STD = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KRY = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
ALPHA = {"std": STD, "kry": KRY}
CLASSES = [(pa, ca, form) for pa in ("std", "kry") for ca in ("std", "kry") for form in ("vig", "beau")]
ORDERS = ("A", "B")          # A: move, then the table; B: the table, then the move
LMAX, TOPK, RESTARTS = 20, 30, 5
N_COPIES = 100
PLANT_LENGTHS = (3, 5, 8, 12, 20)
PLANTS_PER_LENGTH, OWN_COPIES = 8, 10
LAM_Q = 0.55
SEED = 237
EXTRA = ["EGYPT", "CAIRO", "LUXOR", "WALL", "NOVEMBER", "MESSAGE", "DELIVER", "DELIVERING", "TRANSMIT"]
_G = {}

C_SOURCE = r"""
#include <stdint.h>
#include <string.h>
static uint64_t s_;
static inline uint64_t rnd(void){ s_ ^= s_ << 13; s_ ^= s_ >> 7; s_ ^= s_ << 17; return s_; }
static inline double q4(const double* tab, const int* p, int n){
  double t = 0; for (int i = 0; i + 3 < n; i++) t += tab[((p[i]*26 + p[i+1])*26 + p[i+2])*26 + p[i+3]]; return t; }
typedef struct { double u; int m, c; } item;
static void push(item* h, int* cnt, int K, double u, int m, int c){
  if (*cnt < K){ int i = (*cnt)++; h[i].u = u; h[i].m = m; h[i].c = c;
    while (i > 0){ int q = (i-1)/2; if (h[q].u <= h[i].u) break; item t = h[q]; h[q] = h[i]; h[i] = t; i = q; } return; }
  if (u <= h[0].u) return;
  h[0].u = u; h[0].m = m; h[0].c = c; int i = 0;
  for (;;){ int l = 2*i+1, r = l+1, mm = i; if (l < K && h[l].u < h[mm].u) mm = l; if (r < K && h[r].u < h[mm].u) mm = r;
    if (mm == i) break; item t = h[mm]; h[mm] = h[i]; h[i] = t; i = mm; }
}
/* best shift per column by letter log-frequency; dec[v*26+c] = plain letter */
static void colopt(const int* x, int n, int L, const int* dec, const double* lf, int* sh){
  for (int j = 0; j < L; j++){ double best = -1e300; int bv = 0;
    for (int v = 0; v < 26; v++){ double t = 0; for (int i = j; i < n; i += L) t += lf[dec[v*26 + x[i]]]; if (t > best){ best = t; bv = v; } }
    sh[j] = bv; }
}
/* order A (0) or B (1); wheres: M x n; decs: 8 x 676; out: Lmax x K (score, move, class) */
void screen(int order, const int* ct, int n, const int* wheres, int M, const int* decs, int ncls, const double* lf,
            const double* tab, int Lmax, int K, double* ou, int* om, int* oc){
  static item heaps[64][256]; int cnt[64]; memset(cnt, 0, sizeof cnt);
  int q[128], p[128], t[128], sh[128];
  for (int c = 0; c < ncls; c++){
    const int* dec = decs + 676*c;
    for (int L = 1; L <= Lmax; L++){
      if (order == 0){
        colopt(ct, n, L, dec, lf, sh);
        for (int i = 0; i < n; i++) q[i] = dec[sh[i % L]*26 + ct[i]];
        for (int m = 0; m < M; m++){
          const int* w = wheres + n*m;
          for (int i = 0; i < n; i++) p[i] = q[w[i]];
          push(heaps[L], &cnt[L], K, q4(tab, p, n), m, c);
        }
      } else {
        for (int m = 0; m < M; m++){
          const int* w = wheres + n*m;
          for (int i = 0; i < n; i++) t[i] = ct[w[i]];
          colopt(t, n, L, dec, lf, sh);
          for (int i = 0; i < n; i++) p[i] = dec[sh[i % L]*26 + t[i]];
          push(heaps[L], &cnt[L], K, q4(tab, p, n), m, c);
        }
      }
    }
  }
  for (int L = 1; L <= Lmax; L++) for (int k = 0; k < K; k++){
    int ok = k < cnt[L]; ou[(L-1)*K + k] = ok ? heaps[L][k].u : -1e300; om[(L-1)*K + k] = ok ? heaps[L][k].m : -1; oc[(L-1)*K + k] = ok ? heaps[L][k].c : -1; }
}
/* coordinate ascent on the shifts; order A reads the decryption through the move, order B climbs the unmoved text */
double climb(int order, const double* tab, const int* dec, const int* x, const int* w, int n, int L, int restarts,
             uint64_t seed, const int* init, int* best){
  s_ = seed * 2654435761ULL + 88172645463325252ULL; if (!s_) s_ = 1;
  int s[128], q[128], p[128], ord[128]; double bestsc = -1e300;
  #define READ() do { for (int i = 0; i < n; i++) p[i] = order == 0 ? q[w[i]] : q[i]; } while (0)
  for (int r = 0; r <= restarts; r++){
    for (int j = 0; j < L; j++) s[j] = r == 0 ? init[j] : (int)(rnd() % 26);
    for (int i = 0; i < n; i++) q[i] = dec[s[i % L]*26 + x[i]];
    READ(); double cur = q4(tab, p, n);
    int improved = 1;
    while (improved){
      improved = 0;
      for (int j = 0; j < L; j++) ord[j] = j;
      for (int j = L - 1; j > 0; j--){ int k = rnd() % (j + 1); int tt = ord[j]; ord[j] = ord[k]; ord[k] = tt; }
      for (int jj = 0; jj < L; jj++){
        int j = ord[jj], bv = s[j]; double bs = cur;
        for (int v = 0; v < 26; v++){
          if (v == s[j]) continue;
          for (int i = j; i < n; i += L) q[i] = dec[v*26 + x[i]];
          READ(); double sc = q4(tab, p, n);
          if (sc > bs + 1e-12){ bs = sc; bv = v; }
        }
        for (int i = j; i < n; i += L) q[i] = dec[bv*26 + x[i]];
        if (bv != s[j]){ s[j] = bv; cur = bs; improved = 1; }
      }
    }
    if (cur > bestsc){ bestsc = cur; for (int j = 0; j < L; j++) best[j] = s[j]; }
  }
  return bestsc;
}
"""


# ---- the move library (0129's route_library, rebuilt) -----------------------------------------
def numeric_order(word):
    k = "".join(dict.fromkeys(word))
    order = sorted(range(len(k)), key=lambda i: (k[i], i))
    rank = [0] * len(k)
    for n, i in enumerate(order):
        rank[i] = n
    return rank


def columnar(s, order):
    w = len(order)
    rows = [s[i:i + w] for i in range(0, len(s), w)]
    return "".join(r[c] for c in order for r in rows if c < len(r))


def rot_cw(s, w):
    rows = [s[i:i + w] for i in range(0, len(s), w)]
    return "".join(r[c] for c in range(w) for r in reversed(rows) if c < len(r))


def rot_ccw(s, w):
    rows = [s[i:i + w] for i in range(0, len(s), w)]
    return "".join(r[c] for c in reversed(range(w)) for r in rows if c < len(r))


def route_fns(vocab):
    for b in range(1, N):
        for a in range(N):
            def f(s, a=a, b=b):
                out = [""] * N
                for i in range(N):
                    out[(a + b * i) % N] = s[i]
                return "".join(out)
            yield f"K3 rule a={a} b={b}", f
    for w in range(2, N):
        yield f"turn cw {w}", (lambda s, w=w: rot_cw(s, w))
        yield f"turn ccw {w}", (lambda s, w=w: rot_ccw(s, w))
        yield f"columnar {w}", (lambda s, o=list(range(w)): columnar(s, o))
        yield f"columnar rtl {w}", (lambda s, o=list(range(w))[::-1]: columnar(s, o))
    for w1 in range(2, N):
        for w2 in range(2, N):
            yield f"two turns cw {w1},{w2}", (lambda s, a=w1, b=w2: rot_cw(rot_cw(s, a), b))
    words = sorted({w for w in vocab if 2 <= len(w) <= 30} | set(EXTRA))
    for word in words:
        rank = numeric_order(word)
        kw = sorted(range(len(rank)), key=lambda c: rank[c])
        lw = [c for c in word.upper() if c.isalpha()]
        full = sorted(range(len(lw)), key=lambda c: (lw[c], c))
        for how, seq in (("repeats dropped", kw), ("full word", full)):
            if len(seq) >= 2:
                yield f"keyword {word} ({how})", (lambda s, o=list(seq): columnar(s, o))


def route_library(vocab):
    """Distinct 'where' maps (where[i] = place in the moved text of letter i), forward and inverse."""
    seen, lib = set(), []
    idx = "".join(chr(0x100 + i) for i in range(N))
    for name, f in route_fns(vocab):
        sigma = [ord(ch) - 0x100 for ch in f(idx)]
        fwd = [0] * N
        for j, i in enumerate(sigma):
            fwd[i] = j
        for tag, w in ((name, fwd), (name + " inverse", sigma)):
            t = tuple(w)
            if t not in seen:
                seen.add(t); lib.append((tag, t))
    return lib


# ---- the cipher ---------------------------------------------------------------------------------
def dec_table(pa, ca, form):
    P, Cc = ALPHA[pa], ALPHA[ca]
    t = np.zeros(676, dtype=np.int32)
    for v in range(26):
        for c in range(26):
            x = Cc.index(STD[c])
            t[v * 26 + c] = STD.index(P[(x - v) % 26 if form == "vig" else (v - x) % 26])
    return t


def periodic(text, cls, shifts):
    P, Cc = ALPHA[cls[0]], ALPHA[cls[1]]
    return "".join(Cc[(P.index(ch) + shifts[i % len(shifts)]) % 26] if cls[2] == "vig" else Cc[(shifts[i % len(shifts)] - P.index(ch)) % 26]
                   for i, ch in enumerate(text))


def encrypt(plaintext, key):
    w, cls, sh = key["where"], tuple(key["class"]), key["shifts"]
    if key["order"] == "A":
        moved = [""] * N
        for i, ch in enumerate(plaintext):
            moved[w[i]] = ch
        return periodic("".join(moved), cls, sh)
    t = periodic(plaintext, cls, sh)
    out = [""] * N
    for i, ch in enumerate(t):
        out[w[i]] = ch
    return "".join(out)


def decrypt(ct, order, w, cls, shifts):
    d = dec_table(*cls)
    if order == "A":
        q = [d[shifts[i % len(shifts)] * 26 + STD.index(c)] for i, c in enumerate(ct)]
        return "".join(STD[q[w[i]]] for i in range(N))
    t = [STD.index(ct[w[i]]) for i in range(N)]
    return "".join(STD[d[shifts[i % len(shifts)] * 26 + x]] for i, x in enumerate(t))


# ---- compiled code and models ---------------------------------------------------------------------
def P(x, t):
    return x.ctypes.data_as(ctypes.POINTER(t))


def lib():
    if "lib" not in _G:
        d = tempfile.mkdtemp(prefix="k4_0237_")
        src, so = os.path.join(d, "m.c"), os.path.join(d, "m.so")
        open(src, "w").write(C_SOURCE)
        subprocess.run(["cc", "-O3", "-shared", "-fPIC", "-o", so, src], check=True, capture_output=True)
        L_ = ctypes.CDLL(so)
        dp, ip = ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_int)
        L_.screen.restype = None
        L_.screen.argtypes = [ctypes.c_int, ip, ctypes.c_int, ip, ctypes.c_int, ip, ctypes.c_int, dp, dp, ctypes.c_int,
                              ctypes.c_int, dp, ip, ip]
        L_.climb.restype = ctypes.c_double
        L_.climb.argtypes = [ctypes.c_int, dp, ip, ip, ip, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint64, ip, ip]
        sys.path.insert(0, str(ROOT))
        from kryptos.scorer import _table
        logs, floor = _table()
        tab = np.full(26 ** 4, floor)
        for q, v in logs.items():
            if len(q) == 4 and q.isalpha() and q.isupper():
                tab[((ord(q[0]) - 65) * 26 + ord(q[1]) - 65) * 676 + (ord(q[2]) - 65) * 26 + ord(q[3]) - 65] = v
        _G["tab"] = np.ascontiguousarray(tab, dtype=np.float64)
        _G["decs"] = np.ascontiguousarray(np.concatenate([dec_table(*c) for c in CLASSES]).astype(np.int32))
        _G["lib"] = L_
    return _G["lib"]


def models():
    if "m233" not in _G:
        path = next((ROOT / "experiments").glob("0233-*")) / "attack.py"
        spec = importlib.util.spec_from_file_location("frozen0233", path)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        m.ROOT, m.SRC = ROOT, ROOT / "knowledge" / "sources"
        m.CARTER = m.SRC / "carter-1923-tomb-of-tutankhamen-vol1.txt"
        C = m.corpus()
        codes = np.array([STD.index(c) + 1 for c in C["train_manuals"]], dtype=np.int64)
        f = np.bincount(codes - 1, minlength=26) + 1.0
        _G.update(m233=m, Q=m.quadgram_model(), KN8m=m.KN.from_text(codes, 8), corpus=C,
                  lf=np.ascontiguousarray(np.log2(f / f.sum()), dtype=np.float64))
    return _G["m233"]


def mix8m(texts):
    m = _G["m233"]
    return np.log2(LAM_Q * m.per_letter_probs(_G["Q"], texts) + (1 - LAM_Q) * m.per_letter_probs(_G["KN8m"], texts)).sum(axis=1)


def solve(text, seed):
    """-> {(order, L): (MIX8m log2 prob, reading, move index, class index, shifts)}."""
    L_ = lib()
    W = _G["W"]; M = W.shape[0]
    ct = np.ascontiguousarray(np.array([STD.index(c) for c in text], dtype=np.int32))
    found = []
    for oi, order in enumerate(ORDERS):
        ou = np.zeros(LMAX * TOPK); om = np.zeros(LMAX * TOPK, dtype=np.int32); oc = np.zeros(LMAX * TOPK, dtype=np.int32)
        L_.screen(oi, P(ct, ctypes.c_int), N, P(W, ctypes.c_int), M, P(_G["decs"], ctypes.c_int), len(CLASSES),
                  P(_G["lf"], ctypes.c_double), P(_G["tab"], ctypes.c_double), LMAX, TOPK, P(ou, ctypes.c_double),
                  P(om, ctypes.c_int), P(oc, ctypes.c_int))
        for L in range(1, LMAX + 1):
            for k in range(TOPK):
                m, c = int(om[(L - 1) * TOPK + k]), int(oc[(L - 1) * TOPK + k])
                if m < 0:
                    continue
                w = np.ascontiguousarray(W[m])
                dec = np.ascontiguousarray(_G["decs"][676 * c:676 * (c + 1)])
                x = ct if order == "A" else np.ascontiguousarray(ct[w])
                lf = _G["lf"]
                init = [max(range(26), key=lambda v: sum(lf[dec[v * 26 + x[i]]] for i in range(j, N, L))) for j in range(L)]
                best = (ctypes.c_int * L)()
                L_.climb(oi, P(_G["tab"], ctypes.c_double), P(dec, ctypes.c_int), P(x, ctypes.c_int), P(w, ctypes.c_int), N, L,
                         RESTARTS, seed * 1009 + oi * 50021 + L * 101 + k, (ctypes.c_int * L)(*init), best)
                sh = list(best)
                found.append((order, L, m, c, sh, decrypt(text, order, W[m], CLASSES[c], sh)))
    sc = mix8m([f[5] for f in found])
    out = {}
    for (order, L, m, c, sh, rd), s in zip(found, sc):
        if (order, L) not in out or s > out[(order, L)][0]:
            out[(order, L)] = (float(s), rd, m, c, sh)
    return out


def _job(args):
    tid, text, seed = args
    return tid, solve(text, seed)


# ---- run -------------------------------------------------------------------------------------------
def run(ctx):
    import multiprocessing as mp
    t0 = time.time()
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    library = route_library(ctx.vocabulary)
    _G["names"] = [n for n, _ in library]
    _G["W"] = np.ascontiguousarray(np.array([w for _, w in library], dtype=np.int32))
    lib(); models()
    rng = random.Random(SEED)
    # self-checks: both orders round-trip; K3's rule at its own shift is in the library
    pt = _G["corpus"]["test"][:N]
    for order in ORDERS:
        m = rng.randrange(len(library))
        key = {"order": order, "where": library[m][1], "class": CLASSES[3], "shifts": [3, 1, 4, 1, 5]}
        assert decrypt(encrypt(pt, key), order, library[m][1], CLASSES[3], key["shifts"]) == pt
    k4 = ctx.K4
    texts = [("k4", k4, rng.randrange(10 ** 9))]
    for i in range(N_COPIES):
        s = list(k4); rng.shuffle(s); texts.append((f"copy{i}", "".join(s), rng.randrange(10 ** 9)))
    C = _G["corpus"]
    plants = {}
    for L in PLANT_LENGTHS:
        for j in range(PLANTS_PER_LENGTH):
            src = C["test"] if j % 2 == 0 else C["test_xs"]
            o = rng.randrange(0, len(src) - N)
            p = src[o:o + N]
            order = ORDERS[(j // 2) % 2]
            m = rng.randrange(len(library)); c = rng.randrange(len(CLASSES))
            key = {"order": order, "where": library[m][1], "class": CLASSES[c], "shifts": [rng.randrange(26) for _ in range(L)]}
            pc = encrypt(p, key)
            pid = f"plant{L}_{j}"
            plants[pid] = {"L": L, "order": order, "pt": p, "move": m}
            texts.append((pid, pc, rng.randrange(10 ** 9)))
            for g in range(OWN_COPIES):
                s = list(pc); rng.shuffle(s); texts.append((f"{pid}_own{g}", "".join(s), rng.randrange(10 ** 9)))
    res = {}
    workers = int(os.environ.get("K4_WORKERS", 8))
    ctx.progress(0, len(texts), "texts solved")
    with mp.get_context("fork").Pool(workers) as pool:
        for tid, out in pool.imap_unordered(_job, texts, chunksize=1):
            res[tid] = out
            ctx.progress(len(res), len(texts), "texts solved")
    cells = [(o, L) for o in ORDERS for L in range(1, LMAX + 1)]
    cop = np.array([[res[f"copy{i}"][c][0] for c in cells] for i in range(N_COPIES)])
    mu, sd = cop.mean(axis=0), cop.std(axis=0) + 1e-9

    def S(tid):
        z = (np.array([res[tid][c][0] for c in cells]) - mu) / sd
        return float(z.max()), cells[int(z.argmax())]
    s_k4, c_k4 = S("k4")
    s_cop = [S(f"copy{i}")[0] for i in range(N_COPIES)]
    p_k4 = (1 + sum(1 for x in s_cop if x >= s_k4)) / (N_COPIES + 1)
    rank = {f"{o}{L}": int(sum(1 for i in range(N_COPIES) if cop[i, k] >= res["k4"][(o, L)][0])) for k, (o, L) in enumerate(cells)}
    power, recovered = {}, {}
    for L in PLANT_LENGTHS:
        f = rec = 0
        for j in range(PLANTS_PER_LENGTH):
            pid = f"plant{L}_{j}"
            f += S(pid)[0] > max(S(f"{pid}_own{g}")[0] for g in range(OWN_COPIES))
            rec += res[pid][(plants[pid]["order"], L)][1] == plants[pid]["pt"]
        power[L] = [f, PLANTS_PER_LENGTH]; recovered[L] = [rec, PLANTS_PER_LENGTH]
    decided = [L for L in PLANT_LENGTHS if power[L][0] >= 6]
    cands = []
    for (o, L) in cells:
        s, rd, m, c, sh = res["k4"][(o, L)]
        cands.append({"plaintext": rd, "key": {"order": o, "move": _G["names"][m], "where": list(library[m][1]),
                                               "class": list(CLASSES[c]), "shifts": sh}})
    from kryptos.scorer import free_text      # gate 4's controls only, after the search
    controls = [max(ctx.english_score(free_text(res[f"copy{i}"][c][1])) for c in cells) for i in range(N_COPIES)]
    bounds = {
        "item": "F13.4d", "search_reads_known_letters": False, "moves": len(library), "orders": ["A move-then-table", "B table-then-move"],
        "classes": [f"{a}/{b}/{c}" for a, b, c in CLASSES], "key_lengths": [1, LMAX],
        "screen": f"per-column letter-frequency shifts, every move scored by quadgrams; {TOPK} best per order and length",
        "climb": f"coordinate ascent, move held, screen's shifts and {RESTARTS} random starts; MIX8m rescoring",
        "texts": len(texts), "k4_copies": N_COPIES,
        "k4_statistic": round(s_k4, 3), "k4_best_cell": f"{c_k4[0]}{c_k4[1]}", "k4_p": round(p_k4, 4),
        "copies_statistic_max": round(max(s_cop), 3), "copies_statistic_median": round(float(np.median(s_cop)), 3),
        "k4_rank_per_cell_copies_at_or_above": rank,
        "plant_power": power, "plant_exact_recovery": recovered, "decided_lengths_at_6_of_8": decided,
        "k4_best_reading": {"cell": f"{c_k4[0]}{c_k4[1]}", "reading": res["k4"][c_k4][1], "move": _G["names"][res["k4"][c_k4][2]]},
        "f6_1": "blocked: 0236 found one free alphabet cannot be recovered from the ciphertext alone beyond length 5 with no move",
        "expected_total_time": "541 texts x about 25 s = about 4 core-hours",
        "exhaustive": False, "compute_seconds": round(time.time() - t0),
    }
    notes = (f"K4 statistic {s_k4:.2f} at {c_k4[0]}{c_k4[1]}, p {p_k4:.3f} against {N_COPIES} shuffles; plant power "
             + ", ".join(f"L{L} {v[0]}/{v[1]}" for L, v in power.items()) + f"; decided lengths {decided}")
    return {"candidates": cands, "bounds": bounds, "notes": notes, "controls": controls}


def worked_example(ctx, key):
    library = route_library(ctx.vocabulary)
    names = [n for n, _ in library]
    m = names.index("K3 rule a=0 b=7")
    pt = ("THEHOTAIRESCAPINGFROMTHECHAMBERCAUSEDTHEFLAMETOFLICKERBUTPRESENTLYDETAILSOFTHEROOMWITHINEMERGED" * 2)[:N]
    k = {"order": "A", "where": library[m][1], "class": ("kry", "kry", "vig"), "shifts": [KRY.index(c) for c in "SHADOW"]}
    ct = encrypt(pt, k)
    return "\n".join([
        "Order A on a planted message: K3's rule with step 7 (letter i goes to place 7i mod 97), then the KRYPTOS table with SHADOW:", "",
        f"  message   {pt}", f"  carved    {ct}",
        f"  undone    {decrypt(ct, 'A', library[m][1], ('kry', 'kry', 'vig'), k['shifts'])}", "",
        f"The search tries all {len(library):,} moves in both orders, every length 1-20 and the 8 ways of using the table."])
