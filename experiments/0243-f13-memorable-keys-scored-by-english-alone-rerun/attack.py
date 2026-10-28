"""Experiment 0243. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f13-memorable-keys-scored-by-english-alone-rerun",
    "title": "F13.5: memorable keys scored by English alone: key words, keyword tables, running keys from the named texts, autokey primers and keyword columnars from the source list, through the methods already built, no known letter read; K4 against 100 shuffles, plants per method",
    "family": "13-ciphertext-only",
    "parent": "0242-f13-memorable-keys-scored-by-english-alone",
    "changed": (
        "F13.5 (issue #85); reruns 0242, which errored drawing a running-key plant from a named text shorter than 97 letters (plants now draw only from texts longer than 97; the search still reads every text). Every earlier key-source search (0004-0021, 0045-0053, 0109, 0115, 0117, 0154, 0210) decided "
        "by the 24 known letters. Here the same memorable keys are read with no known letter: five methods, every key "
        "from the source order (program.md: K1-K3 words, the sculpture's texts, the Morse, Carter, then the dictionary), "
        "every reading scored exhaustively by quadgrams, the 20 best per method rescored by MIX8m (0233). A: a periodic "
        "key word (every puzzle word and every dictionary word of 3-24 letters, every start) on the 24 rules of the "
        "sculpture's tables. B: keyword-mixed tables from the puzzle words (one side or both) with a puzzle key word. C: "
        "a running key from 0210's named texts, every offset, both directions, on the 24 rules. D: plaintext and "
        "ciphertext autokey primed by any puzzle or dictionary word, on the 24 rules. E: a keyword columnar keyed by a "
        "puzzle word, before or after the table with a puzzle key word. Statistic: max z over the five methods against "
        "K4's 100 shuffles; plants (8 per method, keys drawn from the same sources) each against 10 own shuffles."
    ),
    "hypothesis_expert": (
        "C5 ('simple, can be remembered, executed with the correct key word/s'), C6(a) (keys concealed at the sculpture), "
        "C7(a) (K1-K3 words as keys), C25(a) (the Morse words), C20(a) (layer two). Each method was closed exactly with "
        "the known letters (0005, 0009-0011, 0020, 0053, 0109, 0115, 0117, 0154, 0210; autokeys 0002, 0003, 0025, 0064; "
        "keyword columnars 0110-0114). Those verdicts stand only if the 24 letters sit where stated, letter for letter, "
        "without slips (A1, A2) and the plaintext is not masked out of their places. F13.5 is that hedge: the key space is "
        "at most about 30 bits per method (log2 of 54 million settings), far under what 97 letters of English carry, and "
        "every setting is read, so where the known letters are exact this adds nothing; it decides only the cases where "
        "they are not. Pre-registered: S = max over the five methods of (best MIX8m minus the shuffles' mean) / their sd; "
        "K4 flags at p < 0.05 against 100 shuffles (one test); a plant is found when its S is above all 10 own shuffles' "
        "S; a method is decided when at least 6 of its 8 plants are found."
    ),
    "hypothesis_eli5": (
        "The creators said the key could be remembered: a word, or a passage of a known text. Earlier runs checked every "
        "such key against the clue words. Here we check them again without looking at the clue words at all: every key "
        "word, every passage of the sculpture's texts and Carter's book, every keyword-scrambled table, read in full and "
        "kept only if the result reads as English. K4 is compared with shuffles of its own letters treated the same way, "
        "and hidden test messages made with keys from the same lists show whether a right key would stand out."
    ),
    "prediction": (
        "Plants found 8 of 8 in every method (the keys are read exhaustively, so the true key's reading is scored "
        "directly). K4 inside its shuffles (p above 0.05), its readings junk with at most 3-4 of 24 known letters in "
        "place (harness gate 2). F13.5 closes as exact over the stated key lists."
    ),
    "method": (
        "1. Key lists: 0115's 171 puzzle words (every start), the 234,288-word dictionary (lengths 3-24, every start: "
        "2,241,060 rotations), keyword-mixed alphabets of the puzzle words, 0210's named texts both ways. "
        "2. Every setting decrypted in compiled code and scored by the harness's quadgram table; the 20 best per method "
        "kept, rescored by MIX8m. "
        "3. Texts: K4, 100 shuffles, 40 plants (8 per method, half with X stops, Carter's held-out text, keys drawn from "
        "the lists) and 10 shuffles of each. "
        "4. z per method against K4's shuffles; S = the largest z; K4 ranked; each plant among its own copies. "
        "5. K4's best reading per method submitted; gate 4's controls are the shuffles' best readings."
    ),
    "walkthrough": (
        "1. Take a key from the list, say the word ABSCISSA from its third letter, and a way of using the sculpture's table. "
        "2. Decipher all 97 carved letters with it. "
        "3. Score the result by how often its four-letter groups occur in English. "
        "4. Do this for every key word and start, every passage of the named texts, every keyword table and every way of using the table; keep the best. "
        "5. Do the same on shuffles of K4 and compare."
    ),
    "expected_minutes": 30,
}

import ctypes
import importlib.util
import json
import os
import random
import re
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
MODES = {"vig": (1, -1), "beau": (-1, 1), "var": (1, 1)}   # p = PA[s*c + t*k]
RULES = [(m, pa, ca, ka) for m in MODES for pa in ("std", "kry") for ca in ("std", "kry") for ka in ("std", "kry")]
METHODS = ("A", "B", "C", "D", "E")
TOPQ = 20
N_COPIES = 100
PLANTS_PER_METHOD, OWN_COPIES = 8, 10
LAM_Q = 0.55
SEED = 242
_G = {}

C_SOURCE = r"""
#include <string.h>
static double quad(const double* tab, const int* p, int n){
  double t = 0; for (int i = 0; i + 3 < n; i++) t += tab[((p[i]*26 + p[i+1])*26 + p[i+2])*26 + p[i+3]]; return t; }
static void keep(double s, int tag, long item, double* Q, int* QT, long* QI, int topq){
  int mi = 0; for (int q = 1; q < topq; q++) if (Q[q] < Q[mi]) mi = q;
  if (s > Q[mi]){ Q[mi] = s; QT[mi] = tag; QI[mi] = item; } }
/* z_i = PA[(x_i + t*k_i) mod 26]; reading p_j = z[order[j]] */
static inline int md(int v){ v %= 26; return v < 0 ? v + 26 : v; }
void periodic(const double* tab, const int* pa, const int* x, int t, const int* order, int n,
              const unsigned char* rots, long nrot, int L, double* Q, int* QT, long* QI, int topq, int tag){
  int z[128], p[128];
  for (long r = 0; r < nrot; r++){ const unsigned char* w = rots + r*L;
    for (int i = 0; i < n; i++) z[i] = pa[md(x[i] + t*w[i % L])];
    for (int j = 0; j < n; j++) p[j] = z[order[j]];
    keep(quad(tab, p, n), tag, r, Q, QT, QI, topq); } }
void running(const double* tab, const int* pa, const int* x, int t, int n, const unsigned char* src, long len,
             double* Q, int* QT, long* QI, int topq, int tag){
  int p[128];
  for (long o = 0; o + n <= len; o++){ for (int i = 0; i < n; i++) p[i] = pa[md(x[i] + t*src[o + i])];
    keep(quad(tab, p, n), tag, o, Q, QT, QI, topq); } }
/* autokey: kind 0 plaintext (k_i = kv_of_std[p_{i-L}]), kind 1 ciphertext (k_i = cK[i-L]); primers flat, plen each */
void autokey(const double* tab, const int* pa, const int* kvstd, const int* x, const int* cK, int t, int n,
             const unsigned char* prim, long np, int L, int kind, double* Q, int* QT, long* QI, int topq, int tag){
  int p[128];
  for (long r = 0; r < np; r++){ const unsigned char* w = prim + r*L;
    for (int i = 0; i < n; i++){ int k = i < L ? w[i] : (kind == 0 ? kvstd[p[i - L]] : cK[i - L]); p[i] = pa[md(x[i] + t*k)]; }
    keep(quad(tab, p, n), tag, r, Q, QT, QI, topq); } }
"""


def letters(s):
    return re.sub("[^A-Z]", "", s.upper())


def alpha(a):
    return STD if a == "std" else KRY if a == "kry" else a


def frozen(tag):
    path = next((ROOT / "experiments").glob(f"{tag}-*")) / "attack.py"
    spec = importlib.util.spec_from_file_location(f"frozen{tag}", path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


# ---- key lists ---------------------------------------------------------------------------------
def key_lists(vocabulary):
    m241 = frozen("0241"); m241.ROOT = ROOT
    from kryptos.alphabets import keyword_mixed
    puzzle = m241.puzzle_words(vocabulary)
    rots = m241.rotations()                                   # dictionary words 3-24, every rotation (0115)
    prot = {}
    for w in puzzle:
        for r in range(len(w)):
            prot.setdefault(len(w), {}).setdefault(w[r:] + w[:r], (w, r))
    dwords = sorted({s for n in rots for s, (w, r) in rots[n].items() if r == 0})
    mixed = {}
    for w in puzzle:
        a = keyword_mixed(w)
        if a not in (STD, KRY):
            mixed.setdefault(a, w)
    m210 = frozen("0210"); m210.ROOT = ROOT
    # 0210's "right panel K1-K4" holds K4's own carved letters: as a running key on K4 (not on its shuffles) it reads
    # all A under Beaufort, so it is left out here (K1-K3's ciphertext stays, as "K1+K2+K3 cipher")
    srcs = {k: s for k, (g, s) in m210.sources().items() if not k.startswith("right panel")}
    return {"puzzle": puzzle, "drot": {n: list(d.items()) for n, d in rots.items()},
            "prot": {n: list(d.items()) for n, d in prot.items()}, "dwords": dwords, "mixed": mixed, "sources": srcs}


def columnar_order(word, n=N):
    """Keyword columnar: rows of len(word) written across, columns read down in key order (ties left to right).
    Returns order with carved[j] = message[order[j]]."""
    w = len(word)
    cols = sorted(range(w), key=lambda c: (word[c], c))
    return [i for c in cols for i in range(c, n, w)]


# ---- the cipher --------------------------------------------------------------------------------
def keystream(key, text):
    """Key value per position (in the key alphabet's numbering) for methods A, B, C, E; D handled in crypt."""
    KA = alpha(key["ka"])
    if key["method"] == "C":
        if "sources" not in _G:
            m210 = frozen("0210"); m210.ROOT = ROOT
            _G["sources"] = {k: v for k, (g, v) in m210.sources().items() if not k.startswith("right panel")}
        s = _G["sources"][key["source"]]
        return [KA.index(ch) for ch in s[key["offset"]:key["offset"] + len(text)]]
    w, o = key["key"], key["start"]
    return [KA.index(w[(i + o) % len(w)]) for i in range(len(text))]


def table_dec(ct, key):
    PA, CA, KA = alpha(key["pa"]), alpha(key["ca"]), alpha(key["ka"])
    s, t = MODES[key["mode"]]
    if key["method"] == "D":
        L, w, out = len(key["key"]), key["key"], []
        for i, ch in enumerate(ct):
            k = KA.index(w[i]) if i < L else (KA.index(out[i - L]) if key["kind"] == "plain" else KA.index(ct[i - L]))
            out.append(PA[(s * CA.index(ch) + t * k) % 26])
        return "".join(out)
    k = keystream(key, ct)
    return "".join(PA[(s * CA.index(ch) + t * k[i]) % 26] for i, ch in enumerate(ct))


def table_enc(pt, key):
    PA, CA, KA = alpha(key["pa"]), alpha(key["ca"]), alpha(key["ka"])
    s, t = MODES[key["mode"]]
    if key["method"] == "D":
        L, w, out = len(key["key"]), key["key"], []
        for i, ch in enumerate(pt):
            k = KA.index(w[i]) if i < L else (KA.index(pt[i - L]) if key["kind"] == "plain" else KA.index(out[i - L]))
            out.append(CA[(s * (PA.index(ch) - t * k)) % 26])
        return "".join(out)
    k = keystream(key, pt)
    return "".join(CA[(s * (PA.index(ch) - t * k[i])) % 26] for i, ch in enumerate(pt))


def encrypt(plaintext, key):
    if key["method"] != "E":
        return table_enc(plaintext, key)
    order = columnar_order(key["columnar"], len(plaintext))
    if key["order"] == "move_then_table":
        return table_enc("".join(plaintext[order[j]] for j in range(len(plaintext))), key)
    y = table_enc(plaintext, key)
    return "".join(y[order[j]] for j in range(len(y)))


def decrypt(ct, key):
    if key["method"] != "E":
        return table_dec(ct, key)
    order = columnar_order(key["columnar"], len(ct))
    out = [""] * len(ct)
    if key["order"] == "move_then_table":
        z = table_dec(ct, key)
        for j in range(len(ct)):
            out[order[j]] = z[j]
        return "".join(out)
    for j in range(len(ct)):
        out[order[j]] = ct[j]
    return table_dec("".join(out), key)


# ---- compiled search -----------------------------------------------------------------------------
def lib():
    if "lib" not in _G:
        d = tempfile.mkdtemp(prefix="k4_0242_")
        src, so = os.path.join(d, "k.c"), os.path.join(d, "k.so")
        open(src, "w").write(C_SOURCE)
        subprocess.run(["cc", "-O3", "-shared", "-fPIC", "-o", so, src], check=True, capture_output=True)
        L_ = ctypes.CDLL(so)
        D, I, LG, P = ctypes.c_double, ctypes.c_int, ctypes.c_long, ctypes.c_void_p
        L_.periodic.argtypes = [P, P, P, I, P, I, P, LG, I, P, P, P, I, I]
        L_.running.argtypes = [P, P, P, I, I, P, LG, P, P, P, I, I]
        L_.autokey.argtypes = [P, P, P, P, P, I, I, P, LG, I, I, P, P, P, I, I]
        for f in ("periodic", "running", "autokey"):
            getattr(L_, f).restype = None
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
    if "m233" not in _G:
        m = frozen("0233")
        m.ROOT, m.SRC = ROOT, ROOT / "knowledge" / "sources"
        m.CARTER = m.SRC / "carter-1923-tomb-of-tutankhamen-vol1.txt"
        C = m.corpus()
        codes = np.array([STD.index(c) + 1 for c in C["train_manuals"]], dtype=np.int64)
        _G.update(m233=m, Q=m.quadgram_model(), KN8m=m.KN.from_text(codes, 8), corpus=C)
    return _G["m233"]


def mix8m(texts):
    m = _G["m233"]
    return np.log2(LAM_Q * m.per_letter_probs(_G["Q"], texts) + (1 - LAM_Q) * m.per_letter_probs(_G["KN8m"], texts)).sum(axis=1)


def prepare(vocabulary):
    """Key lists as flat value arrays per key numbering, built once before the workers fork."""
    K = key_lists(vocabulary)
    _G["lists"] = K
    arr = {}
    for kname in ("std", "kry"):
        KA = alpha(kname)
        lut = np.zeros(128, dtype=np.uint8)
        for i, c in enumerate(KA):
            lut[ord(c)] = i
        conv = lambda strs: np.ascontiguousarray(lut[np.frombuffer("".join(strs).encode(), dtype=np.uint8)]) if strs else np.zeros(1, np.uint8)
        for n, items in K["drot"].items():
            arr[("drot", kname, n)] = conv([s for s, _ in items])
        for n, items in K["prot"].items():
            arr[("prot", kname, n)] = conv([s for s, _ in items])
        for name, s in K["sources"].items():
            arr[("src", kname, name)] = conv([s])
        byl = {}
        for w in K["dwords"] + K["puzzle"]:
            byl.setdefault(len(w), set()).add(w)
        K["primers"] = {n: sorted(v) for n, v in byl.items()}
        for n, ws in K["primers"].items():
            arr[("prim", kname, n)] = conv(ws)
    _G["arr"] = arr
    # E: keyword columnars from the puzzle words (distinct orders)
    orders = {}
    for w in K["puzzle"]:
        o = tuple(columnar_order(w))
        if o != tuple(range(N)):
            orders.setdefault(o, w)
    K["columnars"] = [(w, list(o)) for o, w in orders.items()]
    # B: setups with keyword-mixed tables
    sB = []
    for a in K["mixed"]:
        for pa, ca in ((a, a), (a, "std"), ("std", a), (a, "kry"), ("kry", a)):
            for ka in ("std", "kry"):
                for mode in MODES:
                    sB.append((mode, pa, ca, ka))
    K["setupsB"] = sB


def ptr(a, t):
    return a.ctypes.data_as(ctypes.POINTER(t))


def solve(text):
    """-> {method: (MIX8m, reading, key)}"""
    L_ = lib(); K = _G["lists"]; arr = _G["arr"]
    tab = ptr(_G["tab"], ctypes.c_double)
    cdbl, cint, clong, cub = ctypes.c_double, ctypes.c_int, ctypes.c_long, ctypes.c_ubyte
    Q = {m: (np.full(TOPQ, -1e300), np.full(TOPQ, -1, dtype=np.int32), np.zeros(TOPQ, dtype=np.int64)) for m in METHODS}
    tags = {m: [] for m in METHODS}
    ident = (cint * N)(*range(N))

    def qa(m):
        return ptr(Q[m][0], cdbl), ptr(Q[m][1], cint), ptr(Q[m][2], clong)

    def xs(src_text, mode, ca):
        s, _ = MODES[mode]; CA = alpha(ca)
        return (cint * N)(*[(s * CA.index(ch)) % 26 for ch in src_text])

    def pa_arr(pa):
        return (cint * 26)(*[STD.index(ch) for ch in alpha(pa)])

    def periodic_all(m, setup, x, order, kname, groups, extra):
        mode, pa, ca, ka = setup; t = MODES[mode][1]; P = pa_arr(pa)
        for grp in groups:
            for n in sorted(K[grp]):
                a = arr[(grp, kname, n)]; nr = len(K[grp][n])
                if nr == 0:
                    continue
                tags[m].append((setup, grp, n, extra))
                L_.periodic(tab, P, x, t, order, N, ptr(a, cub), nr, n, *qa(m), TOPQ, len(tags[m]) - 1)

    for setup in RULES:                                         # A: a key word on the sculpture's tables
        mode, pa, ca, ka = setup
        periodic_all("A", setup, xs(text, mode, ca), ident, ka, ("prot", "drot"), None)
    for setup in K["setupsB"]:                                  # B: keyword-mixed tables, a puzzle key word
        mode, pa, ca, ka = setup
        periodic_all("B", setup, xs(text, mode, ca), ident, ka, ("prot",), None)
    for setup in RULES:                                         # C: running key from the named texts
        mode, pa, ca, ka = setup; t = MODES[mode][1]; P = pa_arr(pa); x = xs(text, mode, ca)
        for name in K["sources"]:
            a = arr[("src", ka, name)]
            tags["C"].append((setup, name))
            L_.running(tab, P, x, t, N, ptr(a, cub), len(a), *qa("C"), TOPQ, len(tags["C"]) - 1)
    for setup in RULES:                                         # D: autokeys primed by a word
        mode, pa, ca, ka = setup; s, t = MODES[mode]; P = pa_arr(pa); x = xs(text, mode, ca)
        KA = alpha(ka)
        kvstd = (cint * 26)(*[KA.index(ch) for ch in STD])
        cK = (cint * N)(*[KA.index(ch) for ch in text])
        for kind in (0, 1):
            for n in sorted(K["primers"]):
                if n >= N:
                    continue
                a = arr[("prim", ka, n)]
                tags["D"].append((setup, kind, n))
                L_.autokey(tab, P, kvstd, x, cK, t, N, ptr(a, cub), len(K["primers"][n]), n, kind, *qa("D"), TOPQ, len(tags["D"]) - 1)
    for cw, order in K["columnars"]:                            # E: keyword columnar, either order, puzzle key word
        inv = [0] * N
        for j, i in enumerate(order):
            inv[i] = j
        unmoved = "".join(text[inv[i]] for i in range(N))      # y[order[j]] = ct[j]  =>  y[i] = ct[inv[i]]
        for setup in RULES:
            mode, pa, ca, ka = setup
            periodic_all("E", setup, xs(text, mode, ca), (cint * N)(*inv), ka, ("prot",), (cw, "move_then_table"))
            periodic_all("E", setup, xs(unmoved, mode, ca), ident, ka, ("prot",), (cw, "table_then_move"))
    found = []
    for m in METHODS:
        for q in range(TOPQ):
            tg = int(Q[m][1][q])
            if tg < 0:
                continue
            item = int(Q[m][2][q])
            found.append((m, keyof(m, tags[m][tg], item)))
    reads = [decrypt(text, k) for _, k in found]
    sc = mix8m(reads)
    out = {}
    for (m, k), rd, v in zip(found, reads, sc):
        if m not in out or v > out[m][0]:
            out[m] = (float(v), rd, k)
    return out


def keyof(m, tag, item):
    K = _G["lists"]
    if m in ("A", "B", "E"):
        setup, grp, n, extra = tag
        w, r = K[grp][n][item][1]
        key = {"method": m, "mode": setup[0], "pa": setup[1], "ca": setup[2], "ka": setup[3], "key": w, "start": r}
        if m == "E":
            key.update(columnar=extra[0], order=extra[1])
        return key
    if m == "C":
        setup, name = tag
        return {"method": "C", "mode": setup[0], "pa": setup[1], "ca": setup[2], "ka": setup[3], "source": name, "offset": item}
    setup, kind, n = tag
    return {"method": "D", "mode": setup[0], "pa": setup[1], "ca": setup[2], "ka": setup[3], "kind": ("plain", "cipher")[kind],
            "key": K["primers"][n][item]}


def _job(args):
    tid, text = args
    return tid, solve(text)


# ---- run -------------------------------------------------------------------------------------------
def make_plant_key(m, rng):
    K = _G["lists"]
    rule = RULES[rng.randrange(len(RULES))]
    base = {"method": m, "mode": rule[0], "pa": rule[1], "ca": rule[2], "ka": rule[3]}
    if m == "A":
        grp = "drot" if rng.random() < 0.5 else "prot"
        n = rng.choice(sorted(n for n in K[grp] if K[grp][n]))
        w, r = rng.choice(K[grp][n])[1]
        return {**base, "key": w, "start": r}
    if m == "B":
        mode, pa, ca, ka = K["setupsB"][rng.randrange(len(K["setupsB"]))]
        n = rng.choice(sorted(K["prot"]))
        w, r = rng.choice(K["prot"][n])[1]
        return {"method": "B", "mode": mode, "pa": pa, "ca": ca, "ka": ka, "key": w, "start": r}
    if m == "C":
        name = rng.choice(sorted(k for k, v in K["sources"].items() if len(v) > N))
        return {**base, "source": name, "offset": rng.randrange(len(K["sources"][name]) - N)}
    if m == "D":
        n = rng.choice([n for n in sorted(K["primers"]) if n < 30])
        return {**base, "kind": rng.choice(("plain", "cipher")), "key": rng.choice(K["primers"][n])}
    cw, _ = rng.choice(K["columnars"])
    n = rng.choice(sorted(K["prot"]))
    w, r = rng.choice(K["prot"][n])[1]
    return {**base, "key": w, "start": r, "columnar": cw, "order": rng.choice(("move_then_table", "table_then_move"))}


def run(ctx):
    import multiprocessing as mp
    t0 = time.time()
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    lib(); models(); prepare(ctx.vocabulary)
    _G["sources"] = _G["lists"]["sources"]
    K = _G["lists"]
    k4 = ctx.K4
    # self-checks: K1 through method A's cipher (PALIMPSEST on the KRYPTOS tables); every method round-trips
    k1 = json.loads((ROOT / "data" / "k1.json").read_text())
    pt1 = k1["plaintext"]; ct1 = k1["ciphertext"][:len(pt1)]
    key1 = {"method": "A", "mode": "vig", "pa": "kry", "ca": "kry", "ka": "kry", "key": "PALIMPSEST", "start": 0}
    assert encrypt(pt1, key1) == ct1 and decrypt(ct1, key1) == pt1, "K1 self-check failed"
    rng = random.Random(SEED)
    C = _G["corpus"]
    texts = [("k4", k4)]
    for i in range(N_COPIES):
        s = list(k4); rng.shuffle(s); texts.append((f"copy{i}", "".join(s)))
    plants = {}
    for m in METHODS:
        for j in range(PLANTS_PER_METHOD):
            src = C["test"] if j % 2 == 0 else C["test_xs"]
            o = rng.randrange(0, len(src) - N)
            pt = src[o:o + N]
            key = make_plant_key(m, rng)
            pc = encrypt(pt, key)
            assert decrypt(pc, key) == pt, (m, key)
            pid = f"plant{m}_{j}"
            plants[pid] = {"method": m, "pt": pt, "key": key, "kind": "clean" if j % 2 == 0 else "xstops"}
            texts.append((pid, pc))
            for g in range(OWN_COPIES):
                s = list(pc); rng.shuffle(s); texts.append((f"{pid}_own{g}", "".join(s)))
    res = {}
    workers = int(os.environ.get("K4_WORKERS", 8))
    ctx.progress(0, len(texts), "texts solved")
    with mp.get_context("fork").Pool(workers) as pool:
        for tid, out in pool.imap_unordered(_job, texts, chunksize=1):
            res[tid] = out
            ctx.progress(len(res), len(texts), "texts solved")
    cop = np.array([[res[f"copy{i}"][m][0] for m in METHODS] for i in range(N_COPIES)])
    mu, sd = cop.mean(axis=0), cop.std(axis=0) + 1e-9

    def S(tid):
        z = (np.array([res[tid][m][0] for m in METHODS]) - mu) / sd
        return float(z.max()), METHODS[int(z.argmax())]
    s_k4, m_k4 = S("k4")
    s_cop = [S(f"copy{i}")[0] for i in range(N_COPIES)]
    p_k4 = (1 + sum(1 for x in s_cop if x >= s_k4)) / (N_COPIES + 1)
    per_method_rank = {m: int(sum(1 for i in range(N_COPIES) if cop[i, a] >= res["k4"][m][0])) for a, m in enumerate(METHODS)}
    power, recovered, detail = {}, {}, {}
    for m in METHODS:
        f = rec = 0
        for j in range(PLANTS_PER_METHOD):
            pid = f"plant{m}_{j}"
            sp, mb = S(pid)
            own = [S(f"{pid}_own{g}")[0] for g in range(OWN_COPIES)]
            ok = sp > max(own); exact = res[pid][m][1] == plants[pid]["pt"]
            f += ok; rec += exact
            detail[pid] = {"kind": plants[pid]["kind"], "key": plants[pid]["key"], "S": round(sp, 2), "own_max": round(max(own), 2),
                           "found": ok, "read_exactly": exact}
        power[m] = [f, PLANTS_PER_METHOD]; recovered[m] = [rec, PLANTS_PER_METHOD]
    decided = [m for m in METHODS if power[m][0] >= 6]
    cands = [{"plaintext": res["k4"][m][1], "key": res["k4"][m][2]} for m in METHODS]
    from kryptos.scorer import free_text
    controls = [max(ctx.english_score(free_text(res[f"copy{i}"][m][1])) for m in METHODS) for i in range(N_COPIES)]
    counts = {
        "A": f"24 rules x ({sum(len(v) for v in K['prot'].values()):,} puzzle-word starts + {sum(len(v) for v in K['drot'].values()):,} dictionary rotations)",
        "B": f"{len(K['setupsB']):,} keyword-table setups ({len(K['mixed'])} puzzle alphabets) x {sum(len(v) for v in K['prot'].values()):,} puzzle-word starts",
        "C": f"24 rules x {len(K['sources'])} named texts (both directions), every offset: {sum(max(0, len(s) - N + 1) for s in K['sources'].values()):,} offsets",
        "D": f"24 rules x 2 kinds x {sum(len(v) for n, v in K['primers'].items() if n < N):,} primer words",
        "E": f"{len(K['columnars'])} keyword columnars x 2 orders x 24 rules x {sum(len(v) for v in K['prot'].values()):,} puzzle-word starts",
    }
    bounds = {
        "item": "F13.5", "search_reads_known_letters": False, "methods": counts, "exhaustive": True,
        "scoring": f"every setting read in full and scored by the harness quadgram table; the {TOPQ} best per method rescored by MIX8m (0233)",
        "texts": len(texts), "k4_copies": N_COPIES,
        "k4_statistic": round(s_k4, 3), "k4_best_method": m_k4, "k4_p": round(p_k4, 4),
        "copies_statistic_max": round(max(s_cop), 3), "copies_statistic_median": round(float(np.median(s_cop)), 3),
        "k4_rank_per_method_copies_at_or_above": per_method_rank,
        "plant_power": power, "plant_exact_recovery": recovered, "decided_methods_at_6_of_8": decided, "plants": detail,
        "k4_best_readings": {m: [res["k4"][m][1], res["k4"][m][2]] for m in METHODS},
        "compute_seconds": round(time.time() - t0),
    }
    notes = (f"K4 statistic {s_k4:.2f} (method {m_k4}), p {p_k4:.3f} against {N_COPIES} shuffles; plant power "
             + ", ".join(f"{m} {v[0]}/{v[1]}" for m, v in power.items()) + f"; decided {decided}")
    return {"candidates": cands, "bounds": bounds, "notes": notes, "controls": controls}


def worked_example(ctx, key):
    key = key if isinstance(key, dict) and "method" in key else {"method": "A", "mode": "vig", "pa": "kry", "ca": "kry",
                                                                 "ka": "kry", "key": "ABSCISSA", "start": 2}
    rd = decrypt(ctx.K4, key)
    desc = ", ".join(f"{k} {v}" for k, v in key.items())
    return "\n".join([f"Key: {desc}", "", "  carved   " + ctx.K4[:60], "  reading  " + rd[:60], "",
                      "Every key in the lists is read like this, in full, and scored by English alone; no known letter is read."])
