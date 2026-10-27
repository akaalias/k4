"""Experiment 0235. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f13-periodic-key-on-dictionary-keyword-tables-ciphertext-only",
    "title": "F13.4b: a periodic key on 2.08 million dictionary keyword tables, key lengths 1-26, from the ciphertext alone: an exact per-column frequency screen of every table, then quadgram climbs and MIX8m on the best 50 per length",
    "family": "13-ciphertext-only",
    "parent": "0234-f13-periodic-key-on-the-sculptures-tables-ciphertext-only",
    "changed": (
        "F13.4b (issue #85). 0234 solved the sculpture's 8 table classes from the ciphertext alone; here the tables are "
        "0109's: every distinct keyword-mixed alphabet from the dictionary's words of 4 letters or more (208,062), on the "
        "plain side, the cipher side or both, against the standard or KRYPTOS alphabet (5 pairings), added or Beaufort "
        "form: 2,080,620 tables, key lengths 1-26. A climb per table is about 45 hours per text, so two stages: (1) for "
        "every table and length, each column's best shift by English letter frequencies, which is exact per column "
        "(compiled, about a minute per text), the 50 best tables per length kept; (2) for those, 0234's coordinate-ascent "
        "climb on quadgrams from the frequency optimum and 9 random starts, the best readings rescored by MIX8m (F13.3). "
        "Statistic, copies and plants as 0234 (K4 against 100 climbed shuffles; 40 plants at lengths 5-26 on random "
        "dictionary tables, each against 10 own shuffles). Cost stated before the run: 541 texts x about 70 s, about "
        "10.5 core-hours."
    ),
    "hypothesis_expert": (
        "F1 on dictionary keyword tables (0109: exact with the known letters, nothing below 26) read without them: the "
        "hedge for A1 and A2 on the table family Sanborn's K1-K2 belong to, with C27(c) (his chart 'slightly different "
        "from the one on Kryptos') and C5 (key word/s) read as a keyword-mixed alphabet. F13.1 puts the cell at 143 bits "
        "at length 26 (122 for the key, 20.3 for the 2.08 million tables), under MIX8m's 189. The frequency screen is "
        "the hand method's first step (each column's shift by letter counts; Friedman, Military Cryptanalysis I) and is "
        "exact per column; it loses the true table when columns are short, which the plants measure. Pre-registered: "
        "one statistic per text, S = max over L of the z-score of the best MIX8m log-probability at L against the "
        "shuffles; K4 flags at p < 0.05 against 100 shuffles; a planted length is decided when at least 6 of its 8 plants "
        "are above all 10 own shuffles. The item closes for the decided lengths and is blocked above them."
    ),
    "hypothesis_eli5": (
        "Like the last run, but the table is built from an ordinary English word instead of KRYPTOS: any of 208,062 "
        "words, used on either side. Too many tables to try the full method on each, so first every table gets the "
        "quick hand test (for each column of the secret word, which shift gives the most common English letters), and "
        "only the 50 best tables for each word length get the full treatment. Hidden test messages, made with random "
        "dictionary tables, tell us up to what length this still finds the answer."
    ),
    "prediction": (
        "Plants found 8 of 8 at length 5, most at 10, few at 15-26: the frequency screen needs columns of 7 letters or "
        "more to keep the true table among 2 million, so decided to about 10. K4 inside its shuffles (p above 0.05); its "
        "26 readings put at most 4-5 known letters in place. F13.4b closes for the short lengths and is blocked above."
    ),
    "method": (
        "1. Tables: 0109's 208,062 alphabets x 5 pairings (W/W, W/standard, standard/W, W/KRYPTOS, KRYPTOS/W) x 2 forms. "
        "2. Screen (C): per text, table and length 1-26, the sum over columns of the best shift's English letter "
        "log-frequency; the 50 best tables per length kept. "
        "3. Climb: for each kept table, coordinate ascent on the shifts by quadgrams from the screen's shifts and from 9 "
        "random starts; the best reading per table rescored by MIX8m (0233's weight 0.55); per length the best. "
        "4. S = max over lengths of the z-score against K4's 100 shuffles; K4 ranked; each plant against its 10 own "
        "shuffles. "
        "5. K4's best reading at each length submitted (key: the two alphabets, the form, the shifts); gate 4's controls "
        "are the shuffles' best readings scored as the harness scores."
    ),
    "walkthrough": (
        "1. Build a table from a word, say HYDRAULIC: HYDRAULICBEFGJKMNOPQSTVWXZ. "
        "2. Guess a key length and write the carved letters in that many columns. "
        "3. For each column, try all 26 shifts and keep the one whose letters are most like English (many E, T, A; few "
        "Q, Z). "
        "4. Do this for every word in the dictionary and keep the 50 tables that look best. "
        "5. For those, improve the shifts by how well the whole text reads, and compare K4's best with what shuffles of "
        "K4 reach."
    ),
    "expected_minutes": 75,
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
SIDES = ("W/W", "W/STD", "STD/W", "W/KRY", "KRY/W")
LMAX, TOPK = 26, 50
RESTARTS = 9
N_COPIES = 100
PLANT_LENGTHS = (5, 10, 15, 20, 26)
PLANTS_PER_LENGTH, OWN_COPIES = 8, 10
LAM_Q = 0.55
SEED = 235
_G = {}

C_SOURCE = r"""
#include <stdint.h>
#include <string.h>
static uint64_t s_;
static inline uint64_t rnd(void){ s_ ^= s_ << 13; s_ ^= s_ >> 7; s_ ^= s_ << 17; return s_; }
static double qscore(const double* tab, const int* p, int n){
  double t = 0; for (int i = 0; i + 3 < n; i++) t += tab[((p[i]*26 + p[i+1])*26 + p[i+2])*26 + p[i+3]]; return t; }
double climb(const double* tab, const int* dec, const int* ct, int n, int L, int restarts, uint64_t seed, const int* init, int* best){
  s_ = seed * 2654435761ULL + 88172645463325252ULL; if (!s_) s_ = 1;
  int s[128], p[128], ord[128]; double bestsc = -1e300;
  for (int r = 0; r <= restarts; r++){
    for (int j = 0; j < L; j++) s[j] = r == 0 ? init[j] : (int)(rnd() % 26);
    for (int i = 0; i < n; i++) p[i] = dec[s[i % L]*26 + ct[i]];
    double cur = qscore(tab, p, n);
    int improved = 1;
    while (improved){
      improved = 0;
      for (int j = 0; j < L; j++) ord[j] = j;
      for (int j = L - 1; j > 0; j--){ int k = rnd() % (j + 1); int t = ord[j]; ord[j] = ord[k]; ord[k] = t; }
      for (int jj = 0; jj < L; jj++){
        int j = ord[jj], bv = s[j]; double bs = cur;
        for (int v = 0; v < 26; v++){
          if (v == s[j]) continue;
          for (int i = j; i < n; i += L) p[i] = dec[v*26 + ct[i]];
          double sc = qscore(tab, p, n);
          if (sc > bs + 1e-12){ bs = sc; bv = v; }
        }
        for (int i = j; i < n; i += L) p[i] = dec[bv*26 + ct[i]];
        if (bv != s[j]){ s[j] = bv; cur = bs; improved = 1; }
      }
    }
    if (cur > bestsc){ bestsc = cur; for (int j = 0; j < L; j++) best[j] = s[j]; }
  }
  return bestsc;
}
typedef struct { double u; int id; } item;
static void push(item* h, int* cnt, int K, double u, int id){
  if (*cnt < K){ int i = (*cnt)++; h[i].u = u; h[i].id = id;
    while (i > 0){ int q = (i-1)/2; if (h[q].u <= h[i].u) break; item t = h[q]; h[q] = h[i]; h[i] = t; i = q; } return; }
  if (u <= h[0].u) return;
  h[0].u = u; h[0].id = id; int i = 0;
  for (;;){ int l = 2*i+1, r = l+1, m = i; if (l < K && h[l].u < h[m].u) m = l; if (r < K && h[r].u < h[m].u) m = r;
    if (m == i) break; item t = h[m]; h[m] = h[i]; h[i] = t; i = m; }
}
/* every table (alphabet a, pairing side 0-4, form 0 added / 1 Beaufort), every length 1..Lmax: the sum over columns
   of the best shift's English letter log-frequency; the K best per length. id = (a*5 + side)*2 + form */
void screen(const int* alphas, int n_alpha, const int* ct, int n, const double* lf, int Lmax, int K, double* outu, int* outid){
  int STDa[26], KRYa[26], inv[26], invS[26], invK[26]; const char* kry = "KRYPTOSABCDEFGHIJLMNQUVWXZ";
  for (int i = 0; i < 26; i++){ STDa[i] = i; KRYa[i] = kry[i] - 'A'; }
  for (int i = 0; i < 26; i++){ invS[STDa[i]] = i; invK[KRYa[i]] = i; }
  static item heaps[64][1024]; int cnt[64]; memset(cnt, 0, sizeof cnt);
  for (int a = 0; a < n_alpha; a++){
    const int* W = alphas + 26*a;
    for (int i = 0; i < 26; i++) inv[W[i]] = i;
    for (int side = 0; side < 5; side++){
      const int *PA, *CAinv;
      switch (side){ case 0: PA = W; CAinv = inv; break; case 1: PA = W; CAinv = invS; break; case 2: PA = STDa; CAinv = inv; break;
                     case 3: PA = W; CAinv = invK; break; default: PA = KRYa; CAinv = inv; }
      double g[52]; for (int k = 0; k < 52; k++) g[k] = lf[PA[k % 26]];
      int u[128]; for (int i = 0; i < n; i++) u[i] = CAinv[ct[i]];
      for (int form = 0; form < 2; form++){
        int id = (a*5 + side)*2 + form;
        for (int L = 1; L <= Lmax; L++){
          double U = 0;
          for (int j = 0; j < L; j++){
            double best = -1e300;
            for (int s = 0; s < 26; s++){
              double t = 0;
              if (form == 0) for (int i = j; i < n; i += L) t += g[u[i] - s + 26];
              else for (int i = j; i < n; i += L) t += g[s - u[i] + 26];
              if (t > best) best = t;
            }
            U += best;
          }
          push(heaps[L], &cnt[L], K, U, id);
        }
      }
    }
  }
  for (int L = 1; L <= Lmax; L++) for (int k = 0; k < K; k++){
    outu[(L-1)*K + k] = k < cnt[L] ? heaps[L][k].u : -1e300; outid[(L-1)*K + k] = k < cnt[L] ? heaps[L][k].id : -1; }
}
"""


# ---- tables -----------------------------------------------------------------------------------
def keyed(word):
    seen = []
    for c in word:
        if c not in seen:
            seen.append(c)
    return "".join(seen) + "".join(c for c in STD if c not in seen)


def alphabets():
    """0109's list: every distinct keyword-mixed alphabet from the dictionary's words of 4+ letters."""
    if "alphas" not in _G:
        words = [w.strip().upper() for w in (ROOT / "kryptos" / "data" / "words.txt").read_text().split()]
        al = {}
        for w in words:
            if len(w) >= 4 and w.isalpha():
                a = keyed(w)
                if a not in al and a not in (STD, KRY):
                    al[a] = w
        _G["alphas"] = list(al.items())
        _G["A"] = np.ascontiguousarray(np.array([[STD.index(c) for c in a] for a, _ in _G["alphas"]], dtype=np.int32))
    return _G["alphas"]


def table(tid):
    """id -> (plain alphabet, cipher alphabet, form, word)."""
    form, rest = tid % 2, tid // 2
    side, a = rest % 5, rest // 5
    W, word = _G["alphas"][a]
    pa, ca = {0: (W, W), 1: (W, STD), 2: (STD, W), 3: (W, KRY), 4: (KRY, W)}[side]
    return pa, ca, ("vig", "beau")[form], word


def dec_table(pa, ca, form):
    t = np.zeros(26 * 26, dtype=np.int32)
    for v in range(26):
        for c in range(26):
            x = ca.index(STD[c])
            t[v * 26 + c] = STD.index(pa[(x - v) % 26 if form == "vig" else (v - x) % 26])
    return t


def encrypt(plaintext, key):
    P, Cc, sh = key["pa"], key["ca"], key["shifts"]
    out = []
    for i, ch in enumerate(plaintext):
        x, v = P.index(ch), sh[i % len(sh)]
        out.append(Cc[(x + v) % 26] if key["form"] == "vig" else Cc[(v - x) % 26])
    return "".join(out)


def decrypt(ct, pa, ca, form, shifts):
    d = dec_table(pa, ca, form)
    return "".join(STD[d[shifts[i % len(shifts)] * 26 + STD.index(c)]] for i, c in enumerate(ct))


# ---- compiled code and models -----------------------------------------------------------------
def lib():
    if "lib" not in _G:
        d = tempfile.mkdtemp(prefix="k4_0235_")
        src, so = os.path.join(d, "f134b.c"), os.path.join(d, "f134b.so")
        open(src, "w").write(C_SOURCE)
        subprocess.run(["cc", "-O3", "-shared", "-fPIC", "-o", so, src], check=True, capture_output=True)
        L_ = ctypes.CDLL(so)
        dp, ip = ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_int)
        L_.climb.restype = ctypes.c_double
        L_.climb.argtypes = [dp, ip, ip, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint64, ip, ip]
        L_.screen.restype = None
        L_.screen.argtypes = [ip, ctypes.c_int, ip, ctypes.c_int, dp, ctypes.c_int, ctypes.c_int, dp, ip]
        sys.path.insert(0, str(ROOT))
        from kryptos.scorer import _table
        logs, floor = _table()
        tab = np.full(26 ** 4, floor)
        for q, v in logs.items():
            if len(q) == 4 and q.isalpha() and q.isupper():
                tab[((ord(q[0]) - 65) * 26 + ord(q[1]) - 65) * 676 + (ord(q[2]) - 65) * 26 + ord(q[3]) - 65] = v
        _G["tab"] = np.ascontiguousarray(tab, dtype=np.float64)
        _G["lib"] = L_
    return _G["lib"]


def models():
    """F13.3's MIX8m (0233's frozen code) and English letter log-frequencies from its training corpus (no Carter)."""
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


def P(x, t):
    return x.ctypes.data_as(ctypes.POINTER(t))


def column_optimum(text, pa, ca, form, L):
    lf = _G["lf"]
    out = []
    for j in range(L):
        col = text[j::L]
        best = max(range(26), key=lambda v: sum(lf[STD.index(pa[(ca.index(c) - v) % 26 if form == "vig" else (v - ca.index(c)) % 26])] for c in col))
        out.append(best)
    return out


def solve(text, seed):
    """-> {L: (MIX8m log2 prob, reading, table id, shifts)}: the screen, then climbs on the TOPK tables per length."""
    L_ = lib()
    ct = np.ascontiguousarray(np.array([STD.index(c) for c in text], dtype=np.int32))
    ou = np.zeros(LMAX * TOPK); oi = np.zeros(LMAX * TOPK, dtype=np.int32)
    L_.screen(P(_G["A"], ctypes.c_int), len(_G["alphas"]), P(ct, ctypes.c_int), N, P(_G["lf"], ctypes.c_double), LMAX, TOPK,
              P(ou, ctypes.c_double), P(oi, ctypes.c_int))
    found = []
    tab = P(_G["tab"], ctypes.c_double)
    for L in range(1, LMAX + 1):
        for k in range(TOPK):
            tid = int(oi[(L - 1) * TOPK + k])
            if tid < 0:
                continue
            pa, ca, form, _ = table(tid)
            d = np.ascontiguousarray(dec_table(pa, ca, form))
            init = (ctypes.c_int * L)(*column_optimum(text, pa, ca, form, L))
            best = (ctypes.c_int * L)()
            L_.climb(tab, P(d, ctypes.c_int), P(ct, ctypes.c_int), N, L, RESTARTS, seed * 1009 + L * 101 + k, init, best)
            sh = list(best)
            found.append((L, tid, sh, decrypt(text, pa, ca, form, sh)))
    sc = mix8m([f[3] for f in found])
    out = {}
    for (L, tid, sh, rd), s in zip(found, sc):
        if L not in out or s > out[L][0]:
            out[L] = (float(s), rd, tid, sh)
    return out


def _job(args):
    tid, text, seed = args
    return tid, solve(text, seed)


# ---- run ---------------------------------------------------------------------------------------
def run(ctx):
    import multiprocessing as mp
    t0 = time.time()
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    alphabets(); lib(); models()
    k4 = ctx.K4
    # self-checks: K1 under (KRYPTOS table as both alphabets) round-trips; the screen's id decoding matches table()
    import json
    k1 = json.loads((ROOT / "data" / "k1.json").read_text())
    key = {"pa": KRY, "ca": KRY, "form": "vig", "shifts": [KRY.index(c) for c in k1["key"]]}
    assert encrypt(k1["plaintext"], key) == k1["ciphertext"][:len(k1["plaintext"])]
    rng = random.Random(SEED)
    texts = [("k4", k4, rng.randrange(10 ** 9))]
    for i in range(N_COPIES):
        s = list(k4); rng.shuffle(s); texts.append((f"copy{i}", "".join(s), rng.randrange(10 ** 9)))
    C = _G["corpus"]
    n_tables = len(_G["alphas"]) * 10
    plants = {}
    for L in PLANT_LENGTHS:
        for j in range(PLANTS_PER_LENGTH):
            src = C["test"] if j % 2 == 0 else C["test_xs"]
            o = rng.randrange(0, len(src) - N)
            pt = src[o:o + N]
            tid = rng.randrange(n_tables)
            pa, ca, form, word = table(tid)
            sh = [rng.randrange(26) for _ in range(L)]
            pc = encrypt(pt, {"pa": pa, "ca": ca, "form": form, "shifts": sh})
            assert decrypt(pc, pa, ca, form, sh) == pt
            pid = f"plant{L}_{j}"
            plants[pid] = {"L": L, "pt": pt, "table": tid, "word": word, "kind": "clean" if j % 2 == 0 else "xstops"}
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
    Ls = list(range(1, LMAX + 1))
    cop = np.array([[res[f"copy{i}"][L][0] for L in Ls] for i in range(N_COPIES)])
    mu, sd = cop.mean(axis=0), cop.std(axis=0) + 1e-9

    def S(tid):
        z = (np.array([res[tid][L][0] for L in Ls]) - mu) / sd
        return float(z.max()), Ls[int(z.argmax())]
    s_k4, l_k4 = S("k4")
    s_cop = [S(f"copy{i}")[0] for i in range(N_COPIES)]
    p_k4 = (1 + sum(1 for x in s_cop if x >= s_k4)) / (N_COPIES + 1)
    per_length_rank = {L: int(sum(1 for i in range(N_COPIES) if cop[i, L - 1] >= res["k4"][L][0])) for L in Ls}
    power, recovered, table_kept = {}, {}, {}
    for L in PLANT_LENGTHS:
        f = rec = kept = 0
        for j in range(PLANTS_PER_LENGTH):
            pid = f"plant{L}_{j}"
            sp = S(pid)[0]
            own = [S(f"{pid}_own{g}")[0] for g in range(OWN_COPIES)]
            f += sp > max(own)
            rec += res[pid][L][1] == plants[pid]["pt"]
            kept += res[pid][L][2] == plants[pid]["table"]
        power[L] = [f, PLANTS_PER_LENGTH]; recovered[L] = [rec, PLANTS_PER_LENGTH]; table_kept[L] = [kept, PLANTS_PER_LENGTH]
    decided = [L for L in PLANT_LENGTHS if power[L][0] >= 6]

    def key_of(r):
        pa, ca, form, word = table(r[2])
        return {"pa": pa, "ca": ca, "form": form, "shifts": r[3], "word": word}
    cands = [{"plaintext": res["k4"][L][1], "key": key_of(res["k4"][L])} for L in Ls]
    from kryptos.scorer import free_text     # gate 4's controls only, after the search
    controls = [max(ctx.english_score(free_text(res[f"copy{i}"][L][1])) for L in Ls) for i in range(N_COPIES)]
    bounds = {
        "item": "F13.4b", "search_reads_known_letters": False,
        "alphabets": len(_G["alphas"]), "tables": n_tables, "pairings": list(SIDES), "forms": ["added", "Beaufort"],
        "key_lengths": [1, LMAX], "screen": f"per column best shift by English letter frequency, exact; best {TOPK} tables per length",
        "climb": f"coordinate ascent on quadgrams from the screen's shifts and {RESTARTS} random starts; MIX8m rescoring",
        "texts": len(texts), "k4_copies": N_COPIES,
        "k4_statistic": round(s_k4, 3), "k4_best_length": l_k4, "k4_p": round(p_k4, 4),
        "copies_statistic_max": round(max(s_cop), 3), "copies_statistic_median": round(float(np.median(s_cop)), 3),
        "k4_rank_per_length_copies_at_or_above": per_length_rank,
        "plant_power": power, "plant_exact_recovery": recovered, "plant_true_table_best": table_kept,
        "decided_lengths_at_6_of_8": decided,
        "k4_best_readings": {L: {"reading": res["k4"][L][1], "word": table(res["k4"][L][2])[3]} for L in (l_k4, 5, 10)},
        "expected_total_time": "541 texts x about 70 s = about 10.5 core-hours",
        "exhaustive": False, "compute_seconds": round(time.time() - t0),
    }
    notes = (f"K4 statistic {s_k4:.2f} at length {l_k4}, p {p_k4:.3f} against {N_COPIES} shuffles; plant power "
             + ", ".join(f"L{L} {v[0]}/{v[1]}" for L, v in power.items()) + f"; decided lengths {decided}")
    return {"candidates": cands, "bounds": bounds, "notes": notes, "controls": controls}


def worked_example(ctx, key):
    alphabets(); lib(); models()
    pa = keyed("HYDRAULIC")
    pt = "THEHOTAIRESCAPINGFROMTHECHAMBERCAUSEDTHEFLAMETOFLICKER"
    sh = [STD.index(c) for c in "SHADOW"]
    ct = encrypt(pt, {"pa": pa, "ca": STD, "form": "vig", "shifts": sh})
    guess = column_optimum(ct, pa, STD, "vig", 6)
    return "\n".join([
        "The screen's first step on a planted message: plain alphabet HYDRAULIC-mixed, key SHADOW (6), standard cipher alphabet:", "",
        f"  plain alphabet  {pa}",
        f"  carved          {ct}",
        f"  key, true       {''.join(STD[v] for v in sh)}",
        f"  key, by letter counts per column alone: {''.join(STD[v] for v in guess)}",
        f"  reading         {decrypt(ct, pa, STD, 'vig', guess)}", "",
        "Every one of 2.08 million tables gets this step at every key length; the 50 best per length are then climbed."])
