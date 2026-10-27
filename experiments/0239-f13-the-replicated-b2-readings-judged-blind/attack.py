"""Experiment 0239. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f13-the-replicated-b2-readings-judged-blind",
    "title": "F13.4d follow-up: 0238's replicated cell (table, then a move, key length 2) regenerated for K4 and its 300 shuffles and judged blind: words, or statistics of the carved order?",
    "family": "13-ciphertext-only",
    "parent": "0238-f13-replicate-k4-table-then-move-length-2-against-fresh-shuffles",
    "changed": (
        "0237 flagged K4 at table-then-move, key length 2 (p 0.0099 against 100 shuffles) and 0238 replicated it (p 0.023 "
        "against 300 fresh shuffles; in that cell 1 of 300 at or above). K4's reading there is junk with 3 of 24 known "
        "letters in place; its move reads the carved text down a width-19 grid. Here 0238's search is rerun with the same "
        "seeds for lengths 1-2 only, which reproduces the length-2 readings exactly, and K4's and the 300 shuffles' best "
        "B2 readings go to the blind judge in one call (F13.3: the judge reads the survivors)."
    ),
    "hypothesis_expert": (
        "The excess is measured by MIX8m, a letter n-gram model; K4's carved order is known to be non-random at widths 7 "
        "and 21 (0056: corrected p 0.005 and 0.010), and a move that reads it at width 19 can turn such structure into "
        "n-gram-friendly letter pairs without any words. If the judge, which reads for words in order and ignores n-gram "
        "texture (reports/judge-bench.md: it beats 4-gram soup, 0233), puts K4's reading above all but 5% of the "
        "shuffles' readings, the excess is word-level: a lead for A2 (the known letters defined on an intermediate text). "
        "Otherwise it is recorded as one more statistic of the carved order and F13.4d closes on 0237's power. "
        "Pre-registered: word-level when K4's judge score has at most 15 of 300 shuffles at or above it; None counts as 0."
    ),
    "hypothesis_eli5": (
        "K4 really did score better than its shuffles in one setting, twice. But the scorer counts letter patterns, not "
        "words, and K4's letters are known to sit in slightly unusual patterns. So we show K4's reading and the 300 "
        "shuffles' readings to the language-model judge, blind, and ask whether any of them contains English words."
    ),
    "prediction": (
        "The judge scores K4's reading low (under 20) and inside the shuffles' (most 0-20): not word-level. F13.4d closed "
        "for lengths 1-12 with the B2 excess written down as a statistic of the carved order."
    ),
    "method": (
        "1. 0238's attack with lengths 1-2 only (seeds unchanged, so the length-2 screens and climbs are identical). "
        "2. K4's and each shuffle's best reading at B2. "
        "3. All 301 to the judge in one call, blind; K4's rank."
    ),
    "walkthrough": (
        "1. Rebuild the same readings as before for K4 and its 300 shuffles. "
        "2. Show all 301, one at a time and unlabelled, to the judge, who scores how much reads as English. "
        "3. If K4's reading is not among the top 5%, the excess was letter texture, not words."
    ),
    "expected_minutes": 10,
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
LMAX, TOPK, RESTARTS = 2, 30, 5
N_COPIES = 300
PLANT_LENGTHS = ()
PLANTS_PER_LENGTH, OWN_COPIES = 8, 10
LAM_Q = 0.55
SEED = 238
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
    b2 = cells.index(("B", 2))
    texts_b2 = [res["k4"][("B", 2)][1]] + [res[f"copy{i}"][("B", 2)][1] for i in range(N_COPIES)]
    jr = ctx.judge(texts_b2)
    js = [(r["score"] if r and r.get("score") is not None else 0) for r in jr]
    n_none = sum(1 for r in jr if not r or r.get("score") is None)
    judge_ge = sum(1 for x in js[1:] if x >= js[0])
    word_level = judge_ge <= 15
    b2_rank = int(sum(1 for i in range(N_COPIES) if cop[i, b2] >= res["k4"][("B", 2)][0]))
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
        "judge_k4_b2": js[0], "judge_reading_k4": jr[0].get("reading") if jr[0] else None,
        "judge_copies_at_or_above": judge_ge, "judge_copies_max": max(js[1:]), "judge_copies_median": float(np.median(js[1:])),
        "judge_none": n_none, "word_level": word_level, "judge_calls": len(texts_b2),
        "replicated": p_k4 < 0.05, "b2_copies_at_or_above": b2_rank, "replicating": "0237 (S 5.05 at B2, p 0.0099 against 100)",
        "plant_power": power, "plant_exact_recovery": recovered, "decided_lengths_at_6_of_8": decided,
        "k4_best_reading": {"cell": f"{c_k4[0]}{c_k4[1]}", "reading": res["k4"][c_k4][1], "move": _G["names"][res["k4"][c_k4][2]]},
        "f6_1": "blocked: 0236 found one free alphabet cannot be recovered from the ciphertext alone beyond length 5 with no move",
        "expected_total_time": "541 texts x about 25 s = about 4 core-hours",
        "exhaustive": False, "compute_seconds": round(time.time() - t0),
    }
    notes = (f"judge: K4's B2 reading {js[0]}, shuffles at or above {judge_ge} of {N_COPIES} (max {max(js[1:])}): "
             f"{'WORD-LEVEL' if word_level else 'not word-level'}; " f"K4 statistic {s_k4:.2f} at {c_k4[0]}{c_k4[1]}, p {p_k4:.3f} against {N_COPIES} shuffles; plant power "
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
