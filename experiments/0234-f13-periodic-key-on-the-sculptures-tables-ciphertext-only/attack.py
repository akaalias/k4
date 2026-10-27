"""Experiment 0234. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f13-periodic-key-on-the-sculptures-tables-ciphertext-only",
    "title": "F13.4a: a periodic key on the sculpture's 8 table classes, key lengths 1-36, solved from the ciphertext alone (quadgram climb, MIX8m rescoring), K4 against 200 climbed shuffles, plants at seven lengths",
    "family": "13-ciphertext-only",
    "parent": "0233-f13-how-many-bits-per-letter-each-english-judge-extracts",
    "changed": (
        "F13.4a (issue #85), the first ciphertext-only solve. 0005 closed this cell exactly with the 24 known letters "
        "(lengths 1-26 and 30-52 dead on all 8 classes); here the known letters are not read. For each of the 8 classes "
        "(plain and cipher alphabets standard or KRYPTOS, added or Beaufort form; the key alphabet drops out) and each key "
        "length 1-36, a compiled coordinate-ascent climb on the shifts (30 restarts) maximizes the quadgram score; the "
        "288 best readings are rescored by MIX8m, F13.3's out-of-domain model (1.95 bits per letter). Per length the best "
        "reading over the classes; the text's statistic is its largest z-score over the lengths against K4's 200 climbed "
        "shuffles. Plants (Carter's held-out last 20%, half with X stops, no known word) at lengths 5, 10, 15, 20, 26, 30 "
        "and 36, 8 each, each against 10 own climbed shuffles."
    ),
    "hypothesis_expert": (
        "F1 with the sculpture's tables (K1, K2: Quagmire III on KRYPTOS with PALIMPSEST and ABSCISSA; 01-facts.md) is the "
        "first family in rank; C8(a), C27(c), C28. Every verdict on it rests on the known letters sitting at 22-34 and "
        "64-74 of the final text, letter for letter (A2) and without slips (A1). F13.1 (reports/f13-solvability-map.md) "
        "puts a periodic key on a fixed table decidable by English alone to length 36 (125 bits at 26, under the 173 the "
        "quadgram scorer carries; 189 with MIX8m, 0233). The classic hand method (Stein; Friedman's Military "
        "Cryptanalysis) is exactly this: one shift per column, chosen by how well the decryption reads. Pre-registered: "
        "one statistic per text, S = max over L of (best MIX8m log-probability at L minus the shuffles' mean at L) / their "
        "sd; K4 flags at p < 0.05 against 200 shuffles (one test). Power per planted length: found when S is above all 10 "
        "own copies' S (null 1/11); a length is decided when at least 6 of its 8 plants are found (0120's bar as used by "
        "A6.2). The item closes for the lengths decided and is blocked above, by the measured power."
    ),
    "hypothesis_eli5": (
        "The first two messages on the sculpture were made with its table and a repeating secret word. If K4 were made the "
        "same way, a codebreaker could recover the word without knowing any of the message, by trying every shift for "
        "each letter of the word and keeping the ones that make the text read best, as people did by hand a century ago. "
        "We do that for every word length up to 36 and for all eight ways of using the sculpture's two alphabets, never "
        "looking at the clue words, and compare K4 with 200 shuffles of its own letters treated the same way. Hidden test "
        "messages tell us up to what length this can work."
    ),
    "prediction": (
        "Plants found 8 of 8 at lengths 5-15, most at 20, falling to a few at 30-36 (columns of 2-3 letters): decided to "
        "about 20-26. K4's statistic inside its shuffles (p above 0.05), its best readings English-like junk with no "
        "known letter in place beyond chance (the harness's gate 2 on the 36 submitted readings: at most 3 of 24). "
        "So F13.4a closes for the decided lengths and is blocked above them."
    ),
    "method": (
        "1. Texts: K4; 200 shuffles of K4; 56 plants (lengths 5, 10, 15, 20, 26, 30, 36; 8 each, 4 clean and 4 with X "
        "stops; random class and shifts) and 10 shuffles of each plant: 817 texts. "
        "2. Per text, per class (8) and length (1-36): coordinate ascent on the shifts, 30 random restarts, each pass "
        "trying all 26 shifts of every column in random order, scored by the harness's quadgram table. "
        "3. The 288 best readings rescored by MIX8m (0233: KN8 on the manuals mixed with the quadgram table, weight 0.55); "
        "per length the best over classes. "
        "4. z per length against K4's shuffles; S = the largest z; K4 ranked among its shuffles; each plant among its "
        "own copies. "
        "5. K4's best reading at each length submitted as a candidate (key: class and shifts), so the harness checks the "
        "known letters only after the search; gate 4's controls are the shuffles' best readings, scored as the harness scores."
    ),
    "walkthrough": (
        "1. Guess a key length, say 7, and write the carved letters in 7 columns. "
        "2. Pick one of the eight ways of using the sculpture's table. "
        "3. For column 1 try all 26 shifts and keep the one that makes the whole text read best; then column 2, and so on, "
        "going round until nothing improves. "
        "4. Start again from a few random keys and keep the best reading. "
        "5. Do it for every length up to 36 and every way of using the table, and compare K4's best with the best that "
        "shuffles of K4's letters reach."
    ),
    "expected_minutes": 15,
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
CLASSES = [(pa, ca, form) for pa in ("std", "kry") for ca in ("std", "kry") for form in ("vig", "beau")]
ALPHA = {"std": STD, "kry": KRY}
LENGTHS = range(1, 37)
RESTARTS = 30
N_COPIES = 200
PLANT_LENGTHS = (5, 10, 15, 20, 26, 30, 36)
PLANTS_PER_LENGTH, OWN_COPIES = 8, 10
LAM_Q = 0.55              # MIX8m's weight on the quadgram table (0233's validation)
SEED = 234
_G = {}

C_SOURCE = r"""
#include <stdint.h>
static uint64_t s_;
static inline uint64_t rnd(void){ s_ ^= s_ << 13; s_ ^= s_ >> 7; s_ ^= s_ << 17; return s_; }
static double score(const double* tab, const int* p, int n){
  double t = 0; for (int i = 0; i + 3 < n; i++) t += tab[((p[i]*26 + p[i+1])*26 + p[i+2])*26 + p[i+3]]; return t; }
double climb(const double* tab, const int* dec, const int* ct, int n, int L, int restarts, uint64_t seed, int* best){
  s_ = seed * 2654435761ULL + 88172645463325252ULL; if (!s_) s_ = 1;
  int s[128], p[128], ord[128]; double bestsc = -1e300;
  for (int r = 0; r < restarts; r++){
    for (int j = 0; j < L; j++) s[j] = rnd() % 26;
    for (int i = 0; i < n; i++) p[i] = dec[s[i % L]*26 + ct[i]];
    double cur = score(tab, p, n);
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
          double sc = score(tab, p, n);
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
"""


# ---- the cipher -----------------------------------------------------------------------------
def dec_table(pa, ca, form):
    """dec[v*26 + c] = plaintext letter (standard index) for carved letter c (standard index) under shift v."""
    P, Cc = ALPHA[pa], ALPHA[ca]
    t = np.zeros(26 * 26, dtype=np.int32)
    for v in range(26):
        for c in range(26):
            x = Cc.index(STD[c])
            t[v * 26 + c] = STD.index(P[(x - v) % 26 if form == "vig" else (v - x) % 26])
    return t


def encrypt(plaintext, key):
    P, Cc, sh = ALPHA[key["pa"]], ALPHA[key["ca"]], key["shifts"]
    out = []
    for i, ch in enumerate(plaintext):
        x, v = P.index(ch), sh[i % len(sh)]
        out.append(Cc[(x + v) % 26] if key["form"] == "vig" else Cc[(v - x) % 26])
    return "".join(out)


def decrypt(ct, cls, shifts):
    d = dec_table(*cls)
    return "".join(STD[d[shifts[i % len(shifts)] * 26 + STD.index(c)]] for i, c in enumerate(ct))


# ---- compiled climb and models ---------------------------------------------------------------
def lib():
    if "lib" not in _G:
        d = tempfile.mkdtemp(prefix="k4_0234_")
        src, so = os.path.join(d, "climb.c"), os.path.join(d, "climb.so")
        open(src, "w").write(C_SOURCE)
        subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", so, src], check=True, capture_output=True)
        L_ = ctypes.CDLL(so)
        L_.climb.restype = ctypes.c_double
        L_.climb.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int),
                             ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint64, ctypes.POINTER(ctypes.c_int)]
        sys.path.insert(0, str(ROOT))
        from kryptos.scorer import _table
        logs, floor = _table()
        tab = np.full(26 ** 4, floor)
        for q, v in logs.items():
            if len(q) == 4 and q.isalpha() and q.isupper():
                tab[((ord(q[0]) - 65) * 26 + ord(q[1]) - 65) * 676 + (ord(q[2]) - 65) * 26 + ord(q[3]) - 65] = v
        _G["tab"] = np.ascontiguousarray(tab, dtype=np.float64)
        _G["decs"] = [np.ascontiguousarray(dec_table(*c)) for c in CLASSES]
        _G["lib"] = L_
    return _G["lib"]


def models():
    """F13.3's MIX8m: the quadgram table and Kneser-Ney order 8 on the manuals (no Carter), from 0233's frozen code."""
    if "m233" not in _G:
        path = next((ROOT / "experiments").glob("0233-*")) / "attack.py"
        spec = importlib.util.spec_from_file_location("frozen0233", path)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        m.ROOT, m.SRC = ROOT, ROOT / "knowledge" / "sources"
        m.CARTER = m.SRC / "carter-1923-tomb-of-tutankhamen-vol1.txt"
        C = m.corpus()
        codes = np.array([STD.index(c) + 1 for c in C["train_manuals"]], dtype=np.int64)
        _G.update(m233=m, Q=m.quadgram_model(), KN8m=m.KN.from_text(codes, 8), corpus=C)
    return _G["m233"]


def mix8m(texts):
    m = _G["m233"]
    return np.log2(LAM_Q * m.per_letter_probs(_G["Q"], texts) + (1 - LAM_Q) * m.per_letter_probs(_G["KN8m"], texts)).sum(axis=1)


def solve(text, seed):
    """-> {L: (MIX8m log2 prob, reading, class index, shifts)} for every length: the best over the 8 classes."""
    L_ = lib()
    tab = _G["tab"].ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    ct = (ctypes.c_int * N)(*[STD.index(c) for c in text])
    found = []
    for ci, d in enumerate(_G["decs"]):
        dp = d.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
        for L in LENGTHS:
            best = (ctypes.c_int * L)()
            L_.climb(tab, dp, ct, N, L, RESTARTS, seed * 1009 + ci * 97 + L, best)
            sh = list(best)
            found.append((L, ci, sh, decrypt(text, CLASSES[ci], sh)))
    sc = mix8m([f[3] for f in found])
    out = {}
    for (L, ci, sh, rd), s in zip(found, sc):
        if L not in out or s > out[L][0]:
            out[L] = (float(s), rd, ci, sh)
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
    lib(); models()
    k4 = ctx.K4
    # self-check: K1 through the class (kry, kry, vig) with PALIMPSEST
    import json
    k1 = json.loads((ROOT / "data" / "k1.json").read_text())
    key = {"pa": "kry", "ca": "kry", "form": "vig", "shifts": [KRY.index(c) for c in k1["key"]]}
    assert encrypt(k1["plaintext"], key) == k1["ciphertext"][:len(k1["plaintext"])]
    assert decrypt(k1["ciphertext"][:len(k1["plaintext"])], ("kry", "kry", "vig"), key["shifts"]) == k1["plaintext"]
    rng = random.Random(SEED)
    texts = [("k4", k4, rng.randrange(10 ** 9))]
    for i in range(N_COPIES):
        s = list(k4); rng.shuffle(s); texts.append((f"copy{i}", "".join(s), rng.randrange(10 ** 9)))
    C = _G["corpus"]
    plants = {}
    for L in PLANT_LENGTHS:
        for j in range(PLANTS_PER_LENGTH):
            src = C["test"] if j % 2 == 0 else C["test_xs"]
            o = rng.randrange(0, len(src) - N)
            pt = src[o:o + N]
            ci = rng.randrange(len(CLASSES))
            pa, ca, form = CLASSES[ci]
            sh = [rng.randrange(26) for _ in range(L)]
            pc = encrypt(pt, {"pa": pa, "ca": ca, "form": form, "shifts": sh})
            pid = f"plant{L}_{j}"
            plants[pid] = {"L": L, "pt": pt, "class": ci, "shifts": sh, "kind": "clean" if j % 2 == 0 else "xstops"}
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
    Ls = list(LENGTHS)
    cop = np.array([[res[f"copy{i}"][L][0] for L in Ls] for i in range(N_COPIES)])
    mu, sd = cop.mean(axis=0), cop.std(axis=0) + 1e-9

    def S(tid):
        z = (np.array([res[tid][L][0] for L in Ls]) - mu) / sd
        return float(z.max()), Ls[int(z.argmax())]
    s_k4, l_k4 = S("k4")
    s_cop = [S(f"copy{i}")[0] for i in range(N_COPIES)]
    p_k4 = (1 + sum(1 for x in s_cop if x >= s_k4)) / (N_COPIES + 1)
    per_length_rank = {L: int(sum(1 for i in range(N_COPIES) if cop[i, L - 1] >= res["k4"][L][0])) for L in Ls}
    power, recovered = {}, {}
    for L in PLANT_LENGTHS:
        f = rec = 0
        for j in range(PLANTS_PER_LENGTH):
            pid = f"plant{L}_{j}"
            sp = S(pid)[0]
            own = [S(f"{pid}_own{g}")[0] for g in range(OWN_COPIES)]
            f += sp > max(own)
            rec += res[pid][L][1] == plants[pid]["pt"]
        power[L] = [f, PLANTS_PER_LENGTH]; recovered[L] = [rec, PLANTS_PER_LENGTH]
    decided = [L for L in PLANT_LENGTHS if power[L][0] >= 6]
    # candidates: K4's best reading at each length; the harness checks the known letters after the search
    cands = [{"plaintext": res["k4"][L][1],
              "key": {"pa": CLASSES[res["k4"][L][2]][0], "ca": CLASSES[res["k4"][L][2]][1], "form": CLASSES[res["k4"][L][2]][2],
                      "shifts": res["k4"][L][3]}} for L in Ls]
    # gate 4 controls, after the search: each shuffle's best reading, scored as the harness scores a candidate
    from kryptos.scorer import free_text
    controls = [max(ctx.english_score(free_text(res[f"copy{i}"][L][1])) for L in Ls) for i in range(N_COPIES)]
    bounds = {
        "item": "F13.4a", "search_reads_known_letters": False,
        "classes": [f"{a}/{b}/{c}" for a, b, c in CLASSES], "key_lengths": [1, 36], "restarts": RESTARTS,
        "climb": "coordinate ascent on the shifts, quadgram table; best per (class, length) rescored by MIX8m (0233)",
        "texts": len(texts), "k4_copies": N_COPIES,
        "k4_statistic": round(s_k4, 3), "k4_best_length": l_k4, "k4_p": round(p_k4, 4),
        "copies_statistic_max": round(max(s_cop), 3), "copies_statistic_median": round(float(np.median(s_cop)), 3),
        "k4_rank_per_length_copies_at_or_above": per_length_rank,
        "plant_power": power, "plant_exact_recovery": recovered, "decided_lengths_at_6_of_8": decided,
        "k4_best_readings": {L: res["k4"][L][1] for L in (l_k4, 7, 10)},
        "exhaustive": False, "compute_seconds": round(time.time() - t0),
    }
    notes = (f"K4 statistic {s_k4:.2f} at length {l_k4}, p {p_k4:.3f} against {N_COPIES} shuffles; plant power "
             + ", ".join(f"L{L} {v[0]}/{v[1]}" for L, v in power.items()) + f"; decided lengths {decided}")
    return {"candidates": cands, "bounds": bounds, "notes": notes, "controls": controls}


def worked_example(ctx, key):
    lib()
    ct = "".join(c for c in __import__("json").loads((ROOT / "data" / "k1.json").read_text())["ciphertext"] if c.isalpha())[:63]
    L_ = _G["lib"]
    d = _G["decs"][CLASSES.index(("kry", "kry", "vig"))]
    best = (ctypes.c_int * 10)()
    c_ = (ctypes.c_int * len(ct))(*[STD.index(c) for c in ct])
    L_.climb(_G["tab"].ctypes.data_as(ctypes.POINTER(ctypes.c_double)), d.ctypes.data_as(ctypes.POINTER(ctypes.c_int)),
             c_, len(ct), 10, RESTARTS, 1, best)
    sh = list(best)
    return "\n".join([
        "The same climb on K1's 63 carved letters, key length 10, the KRYPTOS table, no known letter:", "",
        "  shifts found  " + "".join(KRY[v] for v in sh),
        "  reading       " + decrypt(ct, ("kry", "kry", "vig"), sh), "",
        "On K4 the climb runs for every length 1-36 and all 8 ways of using the table, and K4's best is compared with",
        "the best that 200 shuffles of K4's letters reach."])
