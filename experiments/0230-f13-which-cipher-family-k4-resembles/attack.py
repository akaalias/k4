"""Experiment 0230. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f13-which-cipher-family-k4-resembles",
    "title": "F13.2: a classifier trained on 17 cipher families' own 97-letter ciphertexts (no known words), its power on held-out texts, and K4 named against 2,000 shuffles of itself",
    "family": "13-ciphertext-only",
    "parent": "0168-k4-statistics-against-a-thousand-shuffles",
    "changed": (
        "F13.2 (issue #85), the first F13 run. 0168 measured K4 on 71 statistics one at a time against shuffles and found "
        "nothing outside them; F7 (0018, 0027) built ciphers by family and compared single statistics. Here the statistics "
        "are combined: 17 generators (one per family or cell of the map, keys drawn at random inside each family's space, "
        "plaintext from Carter's book with no known word, half of it Sanborn-style) make 4,000 ciphertexts each; every text "
        "is measured by 0168's 71 statistics, A13's 14 tests and 70 classic cipher-identification statistics (kappa at "
        "shifts 1-60, digraphic and even-pair I.C., delta I.C., repeats); a multinomial logistic classifier is trained on "
        "3,000 per family and its power measured on 1,000 held-out per family, written from the other end of the book. "
        "Then K4's posterior for each family is ranked against 2,000 shuffles of K4, which keep its letter counts, so a "
        "family is named only for structure beyond the counts. The search never reads the 24 known letters."
    ),
    "hypothesis_expert": (
        "Cipher-type identification (the ACA's and NCID's practice; Sinkov's statistics) asks which generator a ciphertext "
        "is typical of. F13.1 (reports/f13-solvability-map.md) lists the families English alone could decide; F13.2 asks "
        "whether K4's own statistics point at any of them, without the known letters. Classes: monoalphabetic, columnar "
        "transposition (width 2-30), substitution then transposition (F9), periodic key on any of six alphabet pairs "
        "(standard, KRYPTOS, mixed; Quagmire I-IV) in three forms at lengths 2-12, 13-26 and 27-60 (F1, F1.1, F1.2), "
        "progressive key (F1.9), ciphertext and plaintext autokey with primers 1-30 (F1.7), running key from English (F1.3), "
        "Gromark base 10 (F5), Hill 2x2 and 3x3, plain or affine (F8), trifid 27-cell cube with no 27th symbol in the output "
        "(F4), Chaocipher (F10.1), a move then the table and the table then a move (F6), and uniform random letters (the "
        "one-time pad, the null). Features: 0168's 71 (segment chi-squares, I.C. at 1-48 alphabets, repeats at widths 7, 21, "
        "31: the width-7 doublet column and width-21 repeats among them, 04-structure.md), A13's 14 (tools/a13_structure.py), "
        "and 70 more. Tests C4(a)-(b) (a mask leaves a type signature?), C1(a) (move then table), C11a ('interval 7') and "
        "F7's fingerprints as features rather than single tests. Pre-registered: 34 cells (17 families x two feature sets: "
        "the item's named 85 and all 155); K4 names a family when its posterior for that family is above all but a share "
        "p < 0.05/34 = 0.00147 of 2,000 shuffles of K4, and that family's positive control (12 held-out plants per family, "
        "each against 1,000 of its own shuffles, the same rule) finds at least 6 of 12. A named family is a candidate, "
        "replicated with a retrained classifier and fresh shuffles before anything else."
    ),
    "hypothesis_eli5": (
        "Before attacking a cipher, codebreakers often ask what kind it is: some kinds leave fingerprints, such as letters "
        "repeating at a fixed spacing. Here we build a sorting machine (a classifier): we make 4,000 fake K4s with each of 17 "
        "kinds of cipher, measure 155 things about each, and teach the machine to tell the kinds apart. We test it on fakes "
        "it has never seen, to know how often it is right, and then show it K4. Because K4's letter counts alone could "
        "fool it, K4 counts as looking like a kind only if it looks more like that kind than 2,000 shuffles of its own "
        "letters do."
    ),
    "prediction": (
        "Held-out accuracy well above chance (1/17) overall, near 100% for monoalphabetic, transposition, substitution "
        "then transposition and Hill; high for short periodic keys; but the flat families (long periodic keys, running key, "
        "autokeys, Gromark, Chaocipher, the move-and-table pairs, random letters) confused with each other near chance among "
        "themselves. K4 is put among the flat families; against its shuffles no family is named (p above 0.00147 in all "
        "34 cells). Plants of the distinctive families are found against their own shuffles; plants of the flat families "
        "are not. Zero candidates."
    ),
    "method": (
        "1. Plaintexts: 97-letter windows of Carter's Tomb of Tut-ankh-Amen (the plants' source), half clean, half "
        "Sanborn-style (full stops as X, three letters changed); training from the first 80% of the book, held-out texts "
        "and plants from the last 20%. No known word is written in. "
        "2. 17 generators, keys at random inside each family's space; 3,000 training and 1,000 held-out texts per family, "
        "in jobs of 100 with their own seeds. "
        "3. 155 features per text: 0168's all_stats (frozen), A13's battery, and kappa at shifts 1-60, digraphic and "
        "even-pair I.C., delta I.C. on both alphabets, doublets, longest repeat, distinct letters, top count, English "
        "letter log-likelihood. "
        "4. Multinomial logistic regression (numpy, L2 1e-3, Adam 3,000 steps, standardized features), one on the named "
        "85 features and one on all 155. Power: held-out confusion matrix, recall per family, AUC of each family against "
        "random letters. "
        "5. K4 and 2,000 shuffles of K4 through both models; per family the share of shuffles at or above K4's posterior. "
        "6. Positive control: 12 held-out plants per family, each against 1,000 of its own shuffles, the same rule."
    ),
    "walkthrough": (
        "1. Take 97 letters of English and encipher them with one kind of cipher and a random key. "
        "2. Measure the result: how evenly letters are spread, how often a letter recurs 1, 2, 3 ... 60 places later, "
        "repeated pairs and triples, doublets. "
        "3. Do this thousands of times for each of 17 kinds, and fit weights that turn the measurements into a guess of "
        "the kind. "
        "4. Check the guesses on fresh fakes: the share right is the machine's power. "
        "5. Measure K4 and 2,000 shuffles of K4's letters; a kind is named only if K4 scores higher for it than nearly every "
        "shuffle."
    ),
    "expected_minutes": 25,
}

import importlib.util
import math
import os
import random
import re
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np

N = 97
ROOT = Path(__file__).resolve().parent
STD = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KRY = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
CARTER = ROOT / "knowledge" / "sources" / "carter-1923-tomb-of-tutankhamen-vol1.txt"
N_TRAIN, N_TEST, CHUNK = 3000, 1000, 100
N_K4_SHUF = 2000
PC_PLANTS, PC_SHUF = 12, 1000
LAM, STEPS, LR = 1e-3, 3000, 0.05
SEED = 230
_G = {}


# ---- sources ------------------------------------------------------------------------
def sources():
    """Carter's letters, clean and Sanborn-style (full stops as X), split 80/20 by position."""
    if "src" not in _G:
        raw = CARTER.read_text(errors="ignore")
        body = raw[len(raw) // 20: -len(raw) // 20]
        clean = re.sub("[^A-Z]", "", body.upper())
        xs = re.sub("[^A-Z]", "", body.upper().replace(".", "X"))
        _G["src"] = {s: {"train": t[: int(len(t) * 0.8)], "test": t[int(len(t) * 0.8):]} for s, t in (("clean", clean), ("xstops", xs))}
    return _G["src"]


def plaintext(rng, split):
    src = sources()
    kind = "clean" if rng.random() < 0.5 else "xstops"
    t = src[kind][split]
    o = rng.randrange(0, len(t) - N)
    p = list(t[o:o + N])
    if kind == "xstops":
        for q in rng.sample(range(N), 3):
            p[q] = rng.choice(STD)
    return "".join(p)


def english_key(rng, split):
    t = sources()["clean"][split]
    o = rng.randrange(0, len(t) - N)
    return [STD.index(ch) for ch in t[o:o + N]]


# ---- generators ---------------------------------------------------------------------
def mixed(rng):
    a = list(STD); rng.shuffle(a); return "".join(a)


def tables(rng):
    m1, m2 = mixed(rng), mixed(rng)
    pa, ca = rng.choice([(STD, STD), (KRY, KRY), (m1, m1), (STD, m1), (m1, STD), (m1, m2)])
    return pa, ca


def substitute(pt, keys, pa, ca, form):
    out = []
    for p, k in zip(pt, keys):
        x = pa.index(p)
        out.append(ca[(x + k) % 26 if form == "vig" else (k - x) % 26 if form == "beau" else (x - k) % 26])
    return "".join(out)


def periodic(rng, pt, lo, hi):
    L = rng.randint(lo, hi); key = [rng.randrange(26) for _ in range(L)]
    pa, ca = tables(rng)
    return substitute(pt, [key[i % L] for i in range(N)], pa, ca, rng.choice(("vig", "beau", "var")))


def columnar(pt, order):
    w = len(order)
    cols = [pt[j::w] for j in range(w)]
    return "".join(cols[j] for j in order)


def rand_columnar(rng, pt):
    w = rng.randint(2, 30); order = list(range(w)); rng.shuffle(order)
    return columnar(pt, order)


def g_mono(rng, pt):
    ca = mixed(rng)
    return "".join(ca[STD.index(p)] for p in pt)


def g_progressive(rng, pt):
    P, d = rng.randint(3, 13), rng.randint(1, 25); key = [rng.randrange(26) for _ in range(P)]
    pa, ca = tables(rng)
    return substitute(pt, [key[i % P] + d * (i // P) for i in range(N)], pa, ca, rng.choice(("vig", "beau", "var")))


def autokey(pt, primer, pa, ca, mode):
    L, out, keys = len(primer), [], []
    for i, p in enumerate(pt):
        if i < L:
            k = primer[i]
        else:
            k = ca.index(out[i - L]) if mode == "ct" else pa.index(pt[i - L])
        out.append(ca[(pa.index(p) + k) % 26])
    return "".join(out)


def g_ct_autokey(rng, pt):
    pa, ca = tables(rng)
    return autokey(pt, [rng.randrange(26) for _ in range(rng.randint(1, 30))], pa, ca, "ct")


def g_pt_autokey(rng, pt):
    pa, ca = tables(rng)
    return autokey(pt, [rng.randrange(26) for _ in range(rng.randint(1, 30))], pa, ca, "pt")


def g_running(rng, pt, split):
    pa, ca = tables(rng)
    return substitute(pt, english_key(rng, split), pa, ca, rng.choice(("vig", "beau", "var")))


def g_gromark(rng, pt):
    k = [rng.randrange(10) for _ in range(5)]
    while len(k) < N:
        k.append((k[-5] + k[-4]) % 10)
    ca = mixed(rng)
    return "".join(ca[(STD.index(p) + k[i]) % 26] for i, p in enumerate(pt))


def det(M):
    if len(M) == 2:
        return (M[0][0] * M[1][1] - M[0][1] * M[1][0]) % 26
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0])) % 26


def inverse(M):
    n, d = len(M), det(M)
    di = pow(d, -1, 26)
    if n == 2:
        adj = [[M[1][1], -M[0][1]], [-M[1][0], M[0][0]]]
    else:
        adj = [[0] * 3 for _ in range(3)]
        for r in range(3):
            for c in range(3):
                m = [[M[i][j] for j in range(3) if j != c] for i in range(3) if i != r]
                adj[c][r] = (-1) ** (r + c) * (m[0][0] * m[1][1] - m[0][1] * m[1][0])
    return [[(di * adj[r][c]) % 26 for c in range(n)] for r in range(n)]


def hill(pt, M, b, off):
    n, out = len(M), list(pt)
    for i in range(off, N - n + 1, n):
        blk = [STD.index(pt[i + j]) for j in range(n)]
        for r in range(n):
            out[i + r] = STD[(sum(M[r][k] * blk[k] for k in range(n)) + b[r]) % 26]
    return "".join(out)


def g_hill(rng, pt):
    n = rng.choice((2, 3))
    while True:
        M = [[rng.randrange(26) for _ in range(n)] for _ in range(n)]
        if det(M) % 2 and det(M) % 13:
            break
    b = [rng.randrange(26) for _ in range(n)] if rng.random() < 0.5 else [0] * n
    return hill(pt, M, b, rng.randrange(n))


def trifid(pt, cube, P, decrypt=False):
    pos = {ch: (i // 9, (i // 3) % 3, i % 3) for i, ch in enumerate(cube)}
    out = []
    for g in range(0, len(pt), P):
        grp = pt[g:g + P]
        co = [pos[ch] for ch in grp]
        if not decrypt:
            seq = [c[0] for c in co] + [c[1] for c in co] + [c[2] for c in co]
        else:
            flat = [x for c in co for x in c]
            m = len(grp)
            seq = [v for t in zip(flat[:m], flat[m:2 * m], flat[2 * m:]) for v in t]
        out += [cube[seq[i] * 9 + seq[i + 1] * 3 + seq[i + 2]] for i in range(0, len(seq), 3)]
    return "".join(out)


def g_trifid(rng, pt):
    while True:
        cube = list(STD + "#"); rng.shuffle(cube); cube = "".join(cube)
        c = trifid(pt, cube, rng.randint(2, 15))
        if "#" not in c:
            return c


def chaocipher(pt, left, right):
    left, right, out = list(left), list(right), []
    for p in pt:
        i = right.index(p)
        c = left[i]
        out.append(c)
        left = left[i:] + left[:i]
        x = left.pop(1); left.insert(13, x)
        right = right[i:] + right[:i]
        right = right[1:] + right[:1]
        x = right.pop(2); right.insert(13, x)
    return "".join(out)


def g_chaocipher(rng, pt):
    return chaocipher(pt, mixed(rng), mixed(rng))


def g_move_then_table(rng, pt):
    return periodic(rng, rand_columnar(rng, pt), 2, 26)


def g_table_then_move(rng, pt):
    return rand_columnar(rng, periodic(rng, pt, 2, 26))


GENS = [
    ("monoalphabetic", lambda r, p, s: g_mono(r, p)),
    ("transposition", lambda r, p, s: rand_columnar(r, p)),
    ("substitution then move", lambda r, p, s: rand_columnar(r, g_mono(r, p))),
    ("periodic 2-12", lambda r, p, s: periodic(r, p, 2, 12)),
    ("periodic 13-26", lambda r, p, s: periodic(r, p, 13, 26)),
    ("periodic 27-60", lambda r, p, s: periodic(r, p, 27, 60)),
    ("progressive key", lambda r, p, s: g_progressive(r, p)),
    ("ciphertext autokey", lambda r, p, s: g_ct_autokey(r, p)),
    ("plaintext autokey", lambda r, p, s: g_pt_autokey(r, p)),
    ("running key", lambda r, p, s: g_running(r, p, s)),
    ("Gromark", lambda r, p, s: g_gromark(r, p)),
    ("Hill", lambda r, p, s: g_hill(r, p)),
    ("trifid", lambda r, p, s: g_trifid(r, p)),
    ("Chaocipher", lambda r, p, s: g_chaocipher(r, p)),
    ("move then table", lambda r, p, s: g_move_then_table(r, p)),
    ("table then move", lambda r, p, s: g_table_then_move(r, p)),
    ("random letters", lambda r, p, s: "".join(r.choice(STD) for _ in range(N))),
]
K = len(GENS)
N_CELLS = 2 * K
ALPHA = 0.05 / N_CELLS


# ---- features -----------------------------------------------------------------------
def _load():
    if "m168" not in _G:
        path = next((ROOT / "experiments").glob("0168-*")) / "attack.py"
        spec = importlib.util.spec_from_file_location("frozen0168", path)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        _G["m168"] = m
        if str(ROOT / "tools") not in sys.path:
            sys.path.insert(0, str(ROOT / "tools"))
        if str(ROOT) not in sys.path:
            sys.path.insert(0, str(ROOT))
        import a13_structure
        _G["a13"] = a13_structure
        _G["eng"] = np.log(np.maximum(a13_structure.carter_stats()[0], 1e-4))
    return _G["m168"], _G["a13"]


def ic(seq):
    c = Counter(seq); n = len(seq)
    return sum(v * (v - 1) for v in c.values()) / (n * (n - 1)) if n > 1 else 0.0


def extended(ct):
    x = np.array([ord(ch) - 65 for ch in ct])
    out = [float((x[:-s] == x[s:]).mean()) for s in range(1, 61)]
    out.append(ic([ct[i:i + 2] for i in range(N - 1)]) * 26)
    out.append((ic([ct[i:i + 2] for i in range(0, N - 1, 2)]) + ic([ct[i:i + 2] for i in range(1, N - 1, 2)])) * 13)
    for alpha in (STD, KRY):
        y = [alpha.index(ch) for ch in ct]
        out.append(ic([(y[i + 1] - y[i]) % 26 for i in range(N - 1)]))
    out.append(float(sum(1 for i in range(N - 1) if ct[i] == ct[i + 1])))
    lr = 0
    for L in range(2, 20):
        seen = Counter(ct[i:i + L] for i in range(N - L + 1))
        if max(seen.values()) > 1:
            lr = L
        else:
            break
    out.append(float(lr))
    c = Counter(ct)
    out.append(float(len(c)))
    out.append(float(max(c.values())))
    cnt = np.bincount(x, minlength=26)
    out.append(float((cnt * _G["eng"]).sum() / N))
    out.append(float(sum(1 for v in c.values() if v == 1)))
    return out


NAMED = 85


def features(ct):
    m168, a13 = _load()
    v = list(m168.all_stats(ct).values())
    b = a13.battery(ct)
    v += [max(b[t], -5.0) if math.isfinite(b[t]) else -5.0 for t in a13.TESTS]
    return np.array(v + extended(ct), dtype=float)


# ---- jobs ---------------------------------------------------------------------------
def make_text(cls, split, seed):
    rng = random.Random(seed)
    return GENS[cls][1](rng, plaintext(rng, split), split)


def _feat_job(args):
    cls, split, chunk = args
    rows = []
    for j in range(CHUNK):
        seed = SEED * 10 ** 7 + cls * 10 ** 5 + (0 if split == "train" else 5 * 10 ** 4) + chunk * CHUNK + j
        rows.append(features(make_text(cls, split, seed)))
    return cls, split, chunk, np.array(rows)


def posterior(F):
    out = []
    for name, cols in (("named", slice(0, NAMED)), ("all", slice(None))):
        mu, sd, W, b = _G["model"][name]
        Z = (F[:, cols] - mu) / sd
        L = Z @ W + b
        L -= L.max(axis=1, keepdims=True)
        P = np.exp(L); P /= P.sum(axis=1, keepdims=True)
        out.append(P)
    return np.stack(out)          # (2, n, K)


def shuffle_feats(text, n, seed):
    rng = random.Random(seed)
    rows = []
    for _ in range(n):
        s = list(text); rng.shuffle(s); rows.append(features("".join(s)))
    return np.array(rows)


def _pc_job(args):
    cls, i = args
    seed = SEED * 10 ** 7 + 9 * 10 ** 6 + cls * 1000 + i
    pt_ct = make_text(cls, "test", seed)
    P0 = posterior(features(pt_ct)[None, :])[:, 0, cls]
    Ps = posterior(shuffle_feats(pt_ct, PC_SHUF, seed + 1))[:, :, cls]
    ge = (Ps >= P0[:, None]).sum(axis=1)
    return cls, i, [(int(g) + 1) / (PC_SHUF + 1) for g in ge], [float(p) for p in P0]


def _k4_job(args):
    text, chunk, n = args
    return chunk, posterior(shuffle_feats(text, n, SEED * 10 ** 7 + 8 * 10 ** 6 + chunk))


# ---- classifier ---------------------------------------------------------------------
def fit(X, y, seed):
    mu, sd = X.mean(axis=0), X.std(axis=0)
    sd[sd < 1e-9] = 1.0
    Z = (X - mu) / sd
    n, d = Z.shape
    rng = np.random.default_rng(seed)
    W, b = rng.normal(0, 0.01, (d, K)), np.zeros(K)
    Y = np.eye(K)[y]
    mW, vW, mb, vb = np.zeros_like(W), np.zeros_like(W), np.zeros(K), np.zeros(K)
    for t in range(1, STEPS + 1):
        L = Z @ W + b
        L -= L.max(axis=1, keepdims=True)
        P = np.exp(L); P /= P.sum(axis=1, keepdims=True)
        G = (P - Y) / n
        gW, gb = Z.T @ G + LAM * W, G.sum(axis=0)
        mW = 0.9 * mW + 0.1 * gW; vW = 0.999 * vW + 0.001 * gW ** 2
        mb = 0.9 * mb + 0.1 * gb; vb = 0.999 * vb + 0.001 * gb ** 2
        W -= LR * (mW / (1 - 0.9 ** t)) / (np.sqrt(vW / (1 - 0.999 ** t)) + 1e-8)
        b -= LR * (mb / (1 - 0.9 ** t)) / (np.sqrt(vb / (1 - 0.999 ** t)) + 1e-8)
    return mu, sd, W, b


def auc(pos, neg):
    allv = np.concatenate([pos, neg])
    ranks = allv.argsort().argsort() + 1.0
    return float((ranks[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))


# ---- self-checks --------------------------------------------------------------------
def verify():
    """New primitives checked before use: K1 through the periodic substitution on the KRYPTOS table; Rubin's
    Chaocipher test vector; columnar, Hill and trifid by round trips."""
    import json
    k1 = json.loads((ROOT / "data" / "k1.json").read_text())
    key = [KRY.index(ch) for ch in k1["key"]]
    pt = k1["plaintext"]
    assert substitute(pt, [key[i % len(key)] for i in range(len(pt))], KRY, KRY, "vig") == k1["ciphertext"][:len(pt)]
    assert chaocipher("WELLDONEISBETTERTHANWELLSAID", "HXUCZVAMDSLKPEFJRIGTWOBNYQ",
                      "PTLNBQDEOYSFAVZKGJRIHWXUMC") == "OAHQHCNYNXTSZJRRHJBYHQKSOUJY"
    rng = random.Random(1)
    p = plaintext(rng, "train")
    order = list(range(9)); rng.shuffle(order)
    c = columnar(p, order)
    assert sorted(c) == sorted(p) and c != p
    for n in (2, 3):
        while True:
            M = [[rng.randrange(26) for _ in range(n)] for _ in range(n)]
            if det(M) % 2 and det(M) % 13:
                break
        Mi = inverse(M)
        b = [rng.randrange(26) for _ in range(n)]
        enc = hill(p, M, b, 1)
        back = hill("".join(STD[(STD.index(ch) - (b[(i - 1) % n] if 1 <= i < 1 + n * ((N - 1) // n) else 0)) % 26] for i, ch in enumerate(enc)), Mi, [0] * n, 1)
        assert back == p, n
    cube = list(STD + "#"); rng.shuffle(cube); cube = "".join(cube)
    for P in (2, 5, 7, 15):
        assert trifid(trifid(p, cube, P), cube, P, decrypt=True) == p
    return "K1 reproduced by the periodic substitution (KRYPTOS table, PALIMPSEST); Chaocipher matches Rubin's vector; columnar, Hill 2x2/3x3 affine and trifid round-trip"


# ---- run ----------------------------------------------------------------------------
def run(ctx):
    import multiprocessing as mp
    t0 = time.time()
    k4 = ctx.K4
    checked = verify()
    _load()
    workers = int(os.environ.get("K4_WORKERS", 8))
    jobs = [(c, "train", j) for c in range(K) for j in range(N_TRAIN // CHUNK)] + \
           [(c, "test", j) for c in range(K) for j in range(N_TEST // CHUNK)]
    total = len(jobs) + K * PC_PLANTS + N_K4_SHUF // CHUNK
    done = 0
    ctx.progress(0, total, "texts, plants, shuffles")
    Xtr, ytr, Xte, yte = {}, {}, {}, {}
    with mp.get_context("fork").Pool(workers) as pool:
        for cls, split, chunk, F in pool.imap_unordered(_feat_job, jobs, chunksize=1):
            (Xtr if split == "train" else Xte)[(cls, chunk)] = F
            done += 1
            ctx.progress(done, total, "texts")
    keys_tr, keys_te = sorted(Xtr), sorted(Xte)
    X = np.vstack([Xtr[k] for k in keys_tr]); y = np.concatenate([[k[0]] * CHUNK for k in keys_tr])
    XT = np.vstack([Xte[k] for k in keys_te]); yT = np.concatenate([[k[0]] * CHUNK for k in keys_te])
    assert np.isfinite(X).all() and np.isfinite(XT).all()
    _G["model"] = {"named": fit(X[:, :NAMED], y, SEED), "all": fit(X, y, SEED + 1)}
    PT = posterior(XT)
    power = {}
    names = [g[0] for g in GENS]
    rnd = K - 1
    for mi, mname in enumerate(("named", "all")):
        pred = PT[mi].argmax(axis=1)
        conf = np.zeros((K, K), dtype=int)
        for a, b in zip(yT, pred):
            conf[a, b] += 1
        recall = {names[c]: round(float(conf[c, c] / conf[c].sum()), 3) for c in range(K)}
        lr = np.log(PT[mi] + 1e-300)
        aucs = {names[c]: round(auc((lr[:, c] - lr[:, rnd])[yT == c], (lr[:, c] - lr[:, rnd])[yT == rnd]), 3) for c in range(K - 1)}
        trp = _G["model"][mname]
        Ptr = posterior(X)[mi].argmax(axis=1)
        power[mname] = {"held_out_accuracy": round(float((pred == yT).mean()), 3),
                        "train_accuracy": round(float((Ptr == y).mean()), 3),
                        "recall": recall, "auc_against_random_letters": aucs,
                        "confusion": {names[c]: {names[d]: int(conf[c, d]) for d in range(K) if conf[c, d]} for c in range(K)}}
    # K4 and its shuffles
    P4 = posterior(features(k4)[None, :])[:, 0, :]
    pc_jobs = [(c, i) for c in range(K) for i in range(PC_PLANTS)]
    k4_jobs = [(k4, j, CHUNK) for j in range(N_K4_SHUF // CHUNK)]
    shuf, pcs = [], {}
    with mp.get_context("fork").Pool(workers) as pool:
        for chunk, P in pool.imap_unordered(_k4_job, k4_jobs, chunksize=1):
            shuf.append((chunk, P)); done += 1
            ctx.progress(done, total, "K4 shuffles")
        for cls, i, ps, p0 in pool.imap_unordered(_pc_job, pc_jobs, chunksize=1):
            pcs[(cls, i)] = (ps, p0); done += 1
            ctx.progress(done, total, "plants against their shuffles")
    S = np.concatenate([P for _, P in sorted(shuf, key=lambda t: t[0])], axis=1)   # (2, 2000, K)
    k4_cells, named = {}, []
    for mi, mname in enumerate(("named", "all")):
        for c in range(K):
            ge = int((S[mi, :, c] >= P4[mi, c]).sum())
            p = (ge + 1) / (N_K4_SHUF + 1)
            found = sum(1 for i in range(PC_PLANTS) if pcs[(c, i)][0][mi] < ALPHA)
            k4_cells[f"{mname}/{names[c]}"] = {"k4_posterior": round(float(P4[mi, c]), 4),
                                               "shuffles_mean": round(float(S[mi, :, c].mean()), 4),
                                               "shuffles_at_or_above": ge, "p": round(p, 5),
                                               "plants_found": [found, PC_PLANTS]}
            if p < ALPHA and found >= PC_PLANTS // 2:
                named.append(f"{mname}/{names[c]}")
    k4_top = {m: sorted(((names[c], round(float(P4[mi, c]), 3)) for c in range(K)), key=lambda t: -t[1])[:4]
              for mi, m in enumerate(("named", "all"))}
    shuf_top = {m: Counter(names[int(c)] for c in S[mi].argmax(axis=1)).most_common(5) for mi, m in enumerate(("named", "all"))}
    min_p = min(v["p"] for v in k4_cells.values())
    bounds = {
        "item": "F13.2", "search_reads_known_letters": False, "self_check": checked,
        "families": names, "texts_per_family": {"train": N_TRAIN, "held_out": N_TEST},
        "plaintext": "Carter 1923, half clean, half full stops as X with three letters changed; train first 80%, held-out last 20%; no known words",
        "features": {"named (0168's 71 + A13's 14)": NAMED, "all (plus 70 classic identification statistics)": X.shape[1]},
        "classifier": f"multinomial logistic, L2 {LAM}, Adam {STEPS} steps, standardized",
        "chance_accuracy": round(1 / K, 3), "power": power,
        "k4_top_posteriors": k4_top, "k4_shuffles_argmax": shuf_top,
        "cells": N_CELLS, "alpha_per_cell": round(ALPHA, 5), "k4_shuffles": N_K4_SHUF,
        "positive_control": f"{PC_PLANTS} held-out plants per family, each against {PC_SHUF} own shuffles, the K4 rule",
        "k4_cells": k4_cells, "named_families": named, "smallest_p": min_p,
        "exhaustive": False, "compute_seconds": round(time.time() - t0),
    }
    notes = (f"held-out accuracy named {power['named']['held_out_accuracy']}, all {power['all']['held_out_accuracy']} "
             f"(chance {round(1 / K, 3)}); K4 top (all): {k4_top['all'][:2]}; families named against shuffles: {named or 'none'} "
             f"(smallest p {min_p}, alpha {round(ALPHA, 5)})")
    return {"candidates": [], "bounds": bounds, "notes": notes, "controls": []}


def encrypt(plaintext, key):
    """No candidate is submitted; a periodic substitution for completeness (key: {'shifts': [...], 'form': ...})."""
    s = key.get("shifts", [0])
    return substitute(plaintext, [s[i % len(s)] for i in range(len(plaintext))], STD, STD, key.get("form", "vig"))


def worked_example(ctx, key):
    _load()
    k4 = ctx.K4
    e = extended(k4)
    return "\n".join([
        "F13.2 measures a ciphertext and asks which kind of cipher made it. For K4 (no known letter read):", "",
        f"  index of coincidence          {ic(k4):.4f}   (random letters 0.0385, English 0.066)",
        f"  kappa at shifts 1-10          " + " ".join(f"{v:.3f}" for v in e[:10]),
        f"  doublets {int(e[64])}, longest repeat {int(e[65])}, distinct letters {int(e[66])}", "",
        "Each of 17 cipher kinds makes 4,000 such texts; a classifier learns the kinds from 155 such numbers,",
        "is scored on texts it never saw, then reads K4 and 2,000 shuffles of K4's letters."])
