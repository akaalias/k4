"""Experiment 0241. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f13-a-puzzle-word-plus-a-dictionary-word-ciphertext-only",
    "title": "F13.4f, part 1: two key words added, one from the puzzle and one from the whole dictionary (0115's space), solved from the ciphertext alone: every puzzle word, start and rule subtracted, every dictionary rotation scored per column, the best read by quadgrams and MIX8m; K4 against 100 shuffles, plants at four word lengths",
    "family": "13-ciphertext-only",
    "parent": "0234-f13-periodic-key-on-the-sculptures-tables-ciphertext-only",
    "changed": (
        "F13.4f (issue #85), part 1. 0115 closed this space exactly with the 24 known letters, which force the second "
        "word letter by letter (a lookup). Here the known letters are not read. For each of 24 rules (Vigenere, Beaufort "
        "or variant; plain, cipher and key alphabets standard or KRYPTOS), each puzzle word (0115's 171) and start "
        "(1,085 pairs), the puzzle word's stream is subtracted; what is left is a periodic key of the dictionary word's "
        "length n (3-24). Every rotation of every dictionary word of that length (2,248,310 rotations in all) is scored "
        "exactly by the English letter frequencies of the columns it decrypts (compiled, with early abandon), the 10 best "
        "per setting and length read in full by quadgrams, the 10 best per length over all settings rescored by MIX8m "
        "(0233). Statistic, copies and plants as 0234: max z over n against K4's 100 climbed shuffles; plants at n = 5, "
        "10, 15, 20, 8 each, each against 10 own shuffles."
    ),
    "hypothesis_expert": (
        "F3 (two-part key with a combiner; Scheidt's 'key word/s', C5; his key-splitting habit, 03-scheidt-said.md) and "
        "C20(a) 'layer two' as a second pass with a second word: the table applied twice with words of lengths m and n is "
        "one key k_i = a[(i + o1) mod m] + b[(i + o2) mod n]. 0115 killed it exactly for every puzzle word and every "
        "dictionary word of 3-24 letters, but only if the known letters sit where stated, letter for letter, with no slip "
        "(A1, A2); F13 is the hedge that never reads them. F13.1 (reports/f13-solvability-map.md): the space is about "
        "24 x 1,085 x 2.2 million, 35 bits, far under the 173 that 97 letters carry by quadgrams, so it is decidable in "
        "principle; the question is whether a search can reach it. Subtracting the puzzle word leaves a periodic key, and "
        "a dictionary word scored per column by letter counts is the Friedman hand method with the key restricted to "
        "words. Pre-registered: S = max over n of (best MIX8m at n minus the shuffles' mean at n) / their sd; K4 flags at "
        "p < 0.05 against 100 shuffles (one test). A plant is found when its S is above all 10 own shuffles' S (null "
        "1/11); a length is decided when at least 6 of its 8 plants are found."
    ),
    "hypothesis_eli5": (
        "Using the sculpture's table twice, first with a word from the puzzle (like KRYPTOS or ABSCISSA) and then with any "
        "English word, is the same as using one key made by adding the two words. Earlier we used the known clue words "
        "to work out the second word directly. Here we pretend we know no clue word: for every puzzle word we take its "
        "effect off, then try every English word, from every starting letter, and keep the ones whose letters come out "
        "with English letter frequencies, then read the best in full. K4 is compared with shuffles of its own letters "
        "treated the same way, and hidden test messages tell us how long a second word this can still find."
    ),
    "prediction": (
        "Plants found 8 of 8 at n = 5 and 10, most at 15, fewer at 20 (columns of about 5 letters, where the per-column "
        "screen loses the true word among 2 million): decided to about n = 15. K4 inside its shuffles (p above 0.05), its "
        "readings English-like junk with at most 3-4 of 24 known letters in place (harness gate 2). F13.4f part 1 closes "
        "for the decided lengths and is blocked above them."
    ),
    "method": (
        "1. Texts: K4; 100 shuffles of K4; 32 plants (n = 5, 10, 15, 20; 8 each, half with X stops; random rule, puzzle "
        "word, start, dictionary word and rotation; Carter's held-out last 20%, no known word) and 10 shuffles of each: "
        "453 texts. "
        "2. Per text, rule (24) and puzzle word and start (1,085): x_i = the carved letter with the puzzle word's stream "
        "taken off. Per n = 3-24: a 26 x n table of column scores (sum of English log letter frequencies of the letters "
        "each shift gives); every dictionary rotation of length n scored as the sum of its letters' column scores, with "
        "early abandon against the 10th best; the 10 best read in full and scored by the harness's quadgram table. "
        "3. Per n, the 10 best readings over all settings rescored by MIX8m; the best kept. "
        "4. z per n against K4's shuffles; S = the largest z; K4 ranked among its shuffles; each plant among its own copies. "
        "5. K4's best reading at each n submitted (key: rule, the two words and starts); gate 4's controls are the "
        "shuffles' best readings, scored as the harness scores."
    ),
    "walkthrough": (
        "1. Pick a rule (say Vigenere on the KRYPTOS table), a puzzle word (ABSCISSA) and where it starts (its first A at place 1). "
        "2. Write ABSCISSA repeated under the carved letters and take it off each letter on the table: the text that remains has a single repeating key word left in it. "
        "3. Guess that word's length, say 9, and write the remaining text in 9 columns. "
        "4. For each column and each of the 26 shifts, note how English the column's letters look by their frequencies. "
        "5. For every 9-letter English word, read from every starting letter, add up its letters' column scores; keep the 10 best. "
        "6. Read those in full and keep the most English; do this for every puzzle word, start, rule and length, and compare K4's best with what shuffles of K4 reach."
    ),
    "expected_minutes": 200,
}

import ctypes
import importlib.util
import json
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
MODES = {"vig": (1, -1), "beau": (-1, 1), "var": (1, 1)}   # p = PA[s*c + t*(a + b)]
RULES = [(m, pa, ca, ka) for m in MODES for pa in ALPHA for ca in ALPHA for ka in ALPHA]
NS = list(range(3, 25))
TOPK, TOPQ = 10, 10
N_COPIES = 100
PLANT_NS = (5, 10, 15, 20)
PLANTS_PER_N, OWN_COPIES = 8, 10
LAM_Q = 0.55              # MIX8m's weight on the quadgram table (0233's validation)
SEED = 241
_G = {}

# English letter frequencies (per cent), for the per-column screen
FREQ = [8.17, 1.49, 2.78, 4.25, 12.70, 2.23, 2.02, 6.09, 6.97, 0.15, 0.77, 4.03, 2.41, 6.75, 7.51, 1.93, 0.10, 5.99,
        6.33, 9.06, 2.76, 0.98, 2.36, 0.15, 1.97, 0.07]

SPACED = (
    "BETWEEN SUBTLE SHADING AND THE ABSENCE OF LIGHT LIES THE NUANCE OF IQLUSION "
    "IT WAS TOTALLY INVISIBLE HOWS THAT POSSIBLE THEY USED THE EARTHS MAGNETIC FIELD X THE INFORMATION WAS GATHERED AND "
    "TRANSMITTED UNDERGRUUND TO AN UNKNOWN LOCATION X DOES LANGLEY KNOW ABOUT THIS THEY SHOULD ITS BURIED OUT THERE "
    "SOMEWHERE X WHO KNOWS THE EXACT LOCATION ONLY WW THIS WAS HIS LAST MESSAGE X THIRTY EIGHT DEGREES FIFTY SEVEN "
    "MINUTES SIX POINT FIVE SECONDS NORTH SEVENTY SEVEN DEGREES EIGHT MINUTES FORTY FOUR SECONDS WEST ID BY ROWS "
    "SLOWLY DESPARATLY SLOWLY THE REMAINS OF PASSAGE DEBRIS THAT ENCUMBERED THE LOWER PART OF THE DOORWAY WAS REMOVED "
    "WITH TREMBLING HANDS I MADE A TINY BREACH IN THE UPPER LEFT HAND CORNER AND THEN WIDENING THE HOLE A LITTLE I "
    "INSERTED THE CANDLE AND PEERED IN THE HOT AIR ESCAPING FROM THE CHAMBER CAUSED THE FLAME TO FLICKER BUT PRESENTLY "
    "DETAILS OF THE ROOM WITHIN EMERGED FROM THE MIST X CAN YOU SEE ANYTHING Q"
)
EXTRA = ["EGYPT", "CAIRO", "LUXOR", "WALL", "NOVEMBER", "MESSAGE", "DELIVER", "DELIVERING", "TRANSMIT", "LAYERTWO",
         "WONDERFULTHINGS", "BERLINWALL", "WELTZEITUHR", "ALEXANDERPLATZ", "SHADOWFORCES", "LUCIDMEMORY"]

C_SOURCE = r"""
#include <stdint.h>
#include <string.h>
/* One text, one rule, one puzzle-word stream already folded into x[i] (0..25).
   For every n in ns: column table, scan every rotation (values in the key numbering), keep the topk by column score,
   read those in full and keep, per n, the topq by quadgrams across calls (arrays persist in the caller). */
static double quad(const double* tab, const int* p, int n){
  double t = 0; for (int i = 0; i + 3 < n; i++) t += tab[((p[i]*26 + p[i+1])*26 + p[i+2])*26 + p[i+3]]; return t; }

void scan(const double* tab, const double* U, const int* pa, const int* x, int t, int nlen,
          const int* ns, int nns, const unsigned char* const* rots, const long* nrot, int topk,
          int topq, double* qs, long* qrot, int* qtag, int tag, long* work){
  double LL[24*26], sm[25], ks[64]; long kr[64]; int p[128];
  for (int a = 0; a < nns; a++){
    int n = ns[a];
    for (int j = 0; j < n; j++) for (int v = 0; v < 26; v++){
      double s = 0; for (int i = j; i < nlen; i += n){ int q = (x[i] + t*v) % 26; if (q < 0) q += 26; s += U[pa[q]]; }
      LL[j*26 + v] = s; }
    sm[n] = 0;
    for (int j = n - 1; j >= 0; j--){ double m = -1e300; for (int v = 0; v < 26; v++) if (LL[j*26+v] > m) m = LL[j*26+v]; sm[j] = sm[j+1] + m; }
    int kn = 0; double thr = -1e300; int kmin = 0;
    const unsigned char* R = rots[a]; long nr = nrot[a];
    for (long r = 0; r < nr; r++){
      const unsigned char* w = R + r*n; double acc = 0; int j = 0;
      for (; j < n; j++){ acc += LL[j*26 + w[j]]; if (acc + sm[j+1] <= thr) break; }
      if (j < n) continue;
      if (kn < topk){ ks[kn] = acc; kr[kn] = r; kn++;
        if (kn == topk){ kmin = 0; for (int q = 1; q < kn; q++) if (ks[q] < ks[kmin]) kmin = q; thr = ks[kmin]; } }
      else if (acc > thr){ ks[kmin] = acc; kr[kmin] = r; kmin = 0; for (int q = 1; q < kn; q++) if (ks[q] < ks[kmin]) kmin = q; thr = ks[kmin]; }
    }
    work[a] += nr;
    for (int k = 0; k < kn; k++){
      const unsigned char* w = R + kr[k]*n;
      for (int i = 0; i < nlen; i++){ int q = (x[i] + t*w[i % n]) % 26; if (q < 0) q += 26; p[i] = pa[q]; }
      double s = quad(tab, p, nlen);
      double* Q = qs + a*topq; long* QR = qrot + a*topq; int* QT = qtag + a*topq;
      int mi = 0; for (int q = 1; q < topq; q++) if (Q[q] < Q[mi]) mi = q;
      if (s > Q[mi]){ Q[mi] = s; QR[mi] = kr[k]; QT[mi] = tag; }
    }
  }
}
"""


# ---- word lists and the cipher -----------------------------------------------------------------
def puzzle_words(vocabulary):
    return sorted({w for w in SPACED.split() if len(w) >= 2} | {w.upper() for w in vocabulary if 2 <= len(w) <= 30}
                  | set(EXTRA))


def rotations():
    """{n: list of distinct rotation strings} from every dictionary word of 3-24 letters (as 0115)."""
    words = [w.strip().upper() for w in (ROOT / "kryptos" / "data" / "words.txt").read_text().split()]
    rots = {n: {} for n in NS}
    for w in words:
        if 3 <= len(w) <= 24 and w.isalpha():
            s = rots[len(w)]
            for r in range(len(w)):
                s.setdefault(w[r:] + w[:r], (w, r))
    return rots


def keystream(key):
    KA = ALPHA[key["ka"]]
    w1, o1, w2, o2 = key["word1"], key["start1"], key["word2"], key["start2"]
    return [(KA.index(w1[(i + o1) % len(w1)]) + KA.index(w2[(i + o2) % len(w2)])) % 26 for i in range(N)]


def encrypt(plaintext, key):
    PA, CA = ALPHA[key["pa"]], ALPHA[key["ca"]]
    s, t = MODES[key["mode"]]
    k = keystream(key)
    # p = PA[s*c + t*k]  =>  c = s*(p - t*k)   (s = +-1)
    return "".join(CA[(s * (PA.index(ch) - t * k[i])) % 26] for i, ch in enumerate(plaintext))


def decrypt(ct, key):
    PA, CA = ALPHA[key["pa"]], ALPHA[key["ca"]]
    s, t = MODES[key["mode"]]
    k = keystream(key)
    return "".join(PA[(s * CA.index(ch) + t * k[i]) % 26] for i, ch in enumerate(ct))


# ---- compiled scan and models -------------------------------------------------------------------
def lib():
    if "lib" not in _G:
        d = tempfile.mkdtemp(prefix="k4_0241_")
        src, so = os.path.join(d, "scan.c"), os.path.join(d, "scan.so")
        open(src, "w").write(C_SOURCE)
        subprocess.run(["cc", "-O3", "-shared", "-fPIC", "-o", so, src], check=True, capture_output=True)
        L_ = ctypes.CDLL(so)
        L_.scan.restype = None
        sys.path.insert(0, str(ROOT))
        from kryptos.scorer import _table
        logs, floor = _table()
        tab = np.full(26 ** 4, floor)
        for q, v in logs.items():
            if len(q) == 4 and q.isalpha() and q.isupper():
                tab[((ord(q[0]) - 65) * 26 + ord(q[1]) - 65) * 676 + (ord(q[2]) - 65) * 26 + ord(q[3]) - 65] = v
        _G["tab"] = np.ascontiguousarray(tab, dtype=np.float64)
        f = np.array(FREQ) / sum(FREQ)
        _G["U"] = np.ascontiguousarray(np.log(f), dtype=np.float64)
        _G["lib"] = L_
    return _G["lib"]


def build_rotations():
    """Flat uint8 arrays of rotation values per n and key numbering, built once before the workers fork."""
    if "rot" not in _G:
        rots = rotations()
        _G["rot_strings"] = {n: list(rots[n].keys()) for n in NS}
        _G["rot_src"] = {n: list(rots[n].values()) for n in NS}
        arr = {}
        for ka, A in ALPHA.items():
            lut = np.zeros(128, dtype=np.uint8)
            for i, c in enumerate(A):
                lut[ord(c)] = i
            for n in NS:
                b = np.frombuffer("".join(_G["rot_strings"][n]).encode(), dtype=np.uint8)
                arr[(ka, n)] = np.ascontiguousarray(lut[b])
        _G["rot"] = arr
    return _G["rot"]


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


def solve(text, settings=None):
    """-> {n: (MIX8m log2 prob, reading, key)}: the best over every rule, puzzle word and start, and rotation."""
    L_ = lib()
    words = _G["puzzle"]
    tab = _G["tab"].ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    U = _G["U"].ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    nns = len(NS)
    ns = (ctypes.c_int * nns)(*NS)
    qs = np.full(nns * TOPQ, -1e300); qrot = np.zeros(nns * TOPQ, dtype=np.int64); qtag = np.full(nns * TOPQ, -1, dtype=np.int32)
    work = np.zeros(nns, dtype=np.int64)
    P = lambda a, ct_: a.ctypes.data_as(ctypes.POINTER(ct_))
    tags = []
    for ri, (mode, pa, ca, ka) in enumerate(RULES):
        s, t = MODES[mode]
        PAi = (ctypes.c_int * 26)(*[STD.index(ch) for ch in ALPHA[pa]])
        KA = ALPHA[ka]
        cv = [ALPHA[ca].index(ch) for ch in text]
        rp = (ctypes.POINTER(ctypes.c_ubyte) * nns)(*[_G["rot"][(ka, n)].ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte)) for n in NS])
        nrot = (ctypes.c_long * nns)(*[len(_G["rot_strings"][n]) for n in NS])
        for wi, w1 in enumerate(words):
            a = [KA.index(ch) for ch in w1]
            for o1 in range(len(w1)):
                if settings is not None and (ri, wi, o1) not in settings:
                    continue
                x = (ctypes.c_int * N)(*[(s * cv[i] + t * a[(i + o1) % len(w1)]) % 26 for i in range(N)])
                L_.scan(tab, U, PAi, x, t, N, ns, nns, rp, nrot, TOPK, TOPQ, P(qs, ctypes.c_double), P(qrot, ctypes.c_long),
                        P(qtag, ctypes.c_int), len(tags), P(work, ctypes.c_long))
                tags.append((ri, wi, o1))
    found = []
    for ai, n in enumerate(NS):
        for q in range(TOPQ):
            tg = int(qtag[ai * TOPQ + q])
            if tg < 0:
                continue
            ri, wi, o1 = tags[tg]
            mode, pa, ca, ka = RULES[ri]
            w2, o2 = _G["rot_src"][n][int(qrot[ai * TOPQ + q])]
            key = {"mode": mode, "pa": pa, "ca": ca, "ka": ka, "word1": words[wi], "start1": o1, "word2": w2, "start2": o2}
            found.append((n, key, decrypt(text, key)))
    sc = mix8m([f[2] for f in found])
    out = {}
    for (n, key, rd), v in zip(found, sc):
        if n not in out or v > out[n][0]:
            out[n] = (float(v), rd, key)
    return out, int(work.sum())


def _job(args):
    tid, text = args
    return tid, solve(text)


# ---- run -------------------------------------------------------------------------------------------
def run(ctx):
    import multiprocessing as mp
    t0 = time.time()
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    lib(); models(); build_rotations()
    _G["puzzle"] = puzzle_words(ctx.vocabulary)
    k4 = ctx.K4
    # self-check of the cipher on K1: KRYPTOS tables, Vigenere, PALIMPSEST plus a word of K's (value 0 on KRYPTOS)
    k1 = json.loads((ROOT / "data" / "k1.json").read_text())
    pt1 = k1["plaintext"]; ct1 = k1["ciphertext"][:len(pt1)]
    key1 = {"mode": "vig", "pa": "kry", "ca": "kry", "ka": "kry", "word1": "PALIMPSEST", "start1": 0, "word2": "KKK", "start2": 0}
    assert encrypt(pt1[:N], key1) == ct1[:N] and decrypt(ct1[:N], key1) == pt1[:N], "K1 self-check failed"
    # self-check of the compiled scan: a planted text must come back with its own key when given its setting only
    rng = random.Random(SEED)
    C = _G["corpus"]
    words = _G["puzzle"]
    n_settings = len(RULES) * sum(len(w) for w in words)
    texts = [("k4", k4)]
    for i in range(N_COPIES):
        s = list(k4); rng.shuffle(s); texts.append((f"copy{i}", "".join(s)))
    plants = {}
    for n in PLANT_NS:
        for j in range(PLANTS_PER_N):
            src = C["test"] if j % 2 == 0 else C["test_xs"]
            o = rng.randrange(0, len(src) - N)
            pt = src[o:o + N]
            mode, pa, ca, ka = RULES[rng.randrange(len(RULES))]
            w1 = rng.choice(words)
            w2, _ = _G["rot_src"][n][rng.randrange(len(_G["rot_src"][n]))]
            key = {"mode": mode, "pa": pa, "ca": ca, "ka": ka, "word1": w1, "start1": rng.randrange(len(w1)),
                   "word2": w2, "start2": rng.randrange(n)}
            pc = encrypt(pt, key)
            assert decrypt(pc, key) == pt
            pid = f"plant{n}_{j}"
            plants[pid] = {"n": n, "pt": pt, "key": key, "kind": "clean" if j % 2 == 0 else "xstops"}
            texts.append((pid, pc))
            for g in range(OWN_COPIES):
                s = list(pc); rng.shuffle(s); texts.append((f"{pid}_own{g}", "".join(s)))
    p0 = plants["plant10_0"]; k0 = p0["key"]
    ri0 = RULES.index((k0["mode"], k0["pa"], k0["ca"], k0["ka"]))
    one, _ = solve(texts[[t for t, _ in texts].index("plant10_0")][1], settings={(ri0, words.index(k0["word1"]), k0["start1"])})
    selfcheck = {"plant": "plant10_0", "key": k0, "reading_at_10_is_plant": one[10][1] == p0["pt"]}

    res, work = {}, 0
    workers = int(os.environ.get("K4_WORKERS", 8))
    ctx.progress(0, len(texts), "texts solved")
    with mp.get_context("fork").Pool(workers) as pool:
        for tid, (out, wk) in pool.imap_unordered(_job, texts, chunksize=1):
            res[tid] = out; work += wk
            ctx.progress(len(res), len(texts), "texts solved")
    cop = np.array([[res[f"copy{i}"][n][0] for n in NS] for i in range(N_COPIES)])
    mu, sd = cop.mean(axis=0), cop.std(axis=0) + 1e-9

    def S(tid):
        z = (np.array([res[tid][n][0] for n in NS]) - mu) / sd
        return float(z.max()), NS[int(z.argmax())]
    s_k4, n_k4 = S("k4")
    s_cop = [S(f"copy{i}")[0] for i in range(N_COPIES)]
    p_k4 = (1 + sum(1 for x in s_cop if x >= s_k4)) / (N_COPIES + 1)
    per_n_rank = {n: int(sum(1 for i in range(N_COPIES) if cop[i, a] >= res["k4"][n][0])) for a, n in enumerate(NS)}
    power, recovered, plant_detail = {}, {}, {}
    for n in PLANT_NS:
        f = rec = 0
        for j in range(PLANTS_PER_N):
            pid = f"plant{n}_{j}"
            sp, nb = S(pid)
            own = [S(f"{pid}_own{g}")[0] for g in range(OWN_COPIES)]
            ok = sp > max(own)
            exact = res[pid][n][1] == plants[pid]["pt"]
            f += ok; rec += exact
            plant_detail[pid] = {"kind": plants[pid]["kind"], "S": round(sp, 2), "own_max": round(max(own), 2), "found": ok,
                                 "read_exactly_at_n": exact, "true_word2": plants[pid]["key"]["word2"],
                                 "word2_found_at_n": res[pid][n][2]["word2"]}
        power[n] = [f, PLANTS_PER_N]; recovered[n] = [rec, PLANTS_PER_N]
    decided = [n for n in PLANT_NS if power[n][0] >= 6]
    cands = [{"plaintext": res["k4"][n][1], "key": res["k4"][n][2]} for n in NS]
    from kryptos.scorer import free_text
    controls = [max(ctx.english_score(free_text(res[f"copy{i}"][n][1])) for n in NS) for i in range(N_COPIES)]
    bounds = {
        "item": "F13.4f part 1", "search_reads_known_letters": False,
        "rules": len(RULES), "puzzle_words": len(words), "puzzle_word_starts": sum(len(w) for w in words),
        "settings_per_text": n_settings, "second_word_lengths": [NS[0], NS[-1]],
        "dictionary_rotations": {n: len(_G["rot_strings"][n]) for n in NS},
        "rotations_scored_per_text_exhaustive": work // max(1, len(texts)),
        "screen": f"per-column English letter frequencies, exact over every rotation (early abandon only drops rotations that cannot reach the top {TOPK}); top {TOPK} per setting and n read by quadgrams; top {TOPQ} per n rescored by MIX8m (0233)",
        "texts": len(texts), "k4_copies": N_COPIES,
        "k4_statistic": round(s_k4, 3), "k4_best_n": n_k4, "k4_p": round(p_k4, 4),
        "copies_statistic_max": round(max(s_cop), 3), "copies_statistic_median": round(float(np.median(s_cop)), 3),
        "k4_rank_per_n_copies_at_or_above": per_n_rank,
        "plant_power": power, "plant_exact_recovery": recovered, "decided_n_at_6_of_8": decided, "plants": plant_detail,
        "scan_selfcheck": selfcheck,
        "k4_best_readings": {n: [res["k4"][n][1], res["k4"][n][2]] for n in sorted({n_k4, 7, 10})},
        "exhaustive": "the screen is exhaustive over the stated space; the readings kept per setting are its top 10",
        "expected_total": "about 14 core-minutes per text x 453 texts = about 106 core-hours, about 3.3 h on 32 cores (stated before the run)",
        "compute_seconds": round(time.time() - t0),
    }
    notes = (f"K4 statistic {s_k4:.2f} at n {n_k4}, p {p_k4:.3f} against {N_COPIES} shuffles; plant power "
             + ", ".join(f"n{n} {v[0]}/{v[1]}" for n, v in power.items()) + f"; decided n {decided}; "
             f"{n_settings:,} settings x {sum(len(_G['rot_strings'][n]) for n in NS):,} rotations per text")
    return {"candidates": cands, "bounds": bounds, "notes": notes, "controls": controls}


def worked_example(ctx, key):
    key = key if isinstance(key, dict) and "word1" in key else {"mode": "vig", "pa": "kry", "ca": "kry", "ka": "kry",
                                                               "word1": "ABSCISSA", "start1": 0, "word2": "SHADOW", "start2": 0}
    KA = ALPHA[key["ka"]]
    ct = ctx.K4
    s, t = MODES[key["mode"]]
    x = [(s * ALPHA[key["ca"]].index(c) + t * KA.index(key["word1"][(i + key["start1"]) % len(key["word1"])])) % 26
         for i, c in enumerate(ct)]
    rem = "".join(STD[v] for v in x)
    rd = decrypt(ct, key)
    return "\n".join([
        f"Rule {key['mode']} on plain {key['pa']}, cipher {key['ca']}, key letters numbered on {key['ka']}; "
        f"first word {key['word1']} from {key['start1']}, second {key['word2']} from {key['start2']}", "",
        "  carved            " + ct[:48],
        "  first word        " + "".join(key["word1"][(i + key["start1"]) % len(key["word1"])] for i in range(48)),
        "  first word off    " + rem[:48],
        "  second word       " + "".join(key["word2"][(i + key["start2"]) % len(key["word2"])] for i in range(48)),
        "  reading           " + rd[:48], "",
        "The search never reads the known letters: the second word is chosen by how English its columns look."])
