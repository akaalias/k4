"""Experiment 0192 (F11.4). See program.md for the contract."""

EXPERIMENT = {
    "slug": "friedman-keyed-alphabet-box",
    "title": "F11.4: Friedman's keyed alphabet box (MC III 35b): the alphabet written n times into a rectangle as wide as a keyword, read out in the keyword's column order as the key stream; every dictionary keyword: exact",
    "family": "11-agency-hand-systems",
    "parent": "0191-cia-key-box-running-key",
    "changed": (
        "F11.4. Friedman, Military Cryptanalytics III par. 35b (report reports/Scheidt patents and field ciphers.md, "
        "issue #9): a keyword's numerical order is used as a columnar key on a rectangle holding the normal alphabet "
        "repeated an agreed number of times; the column read becomes the key stream. Here: the standard or KRYPTOS "
        "alphabet repeated 1-8 times, every distinct column order of the dictionary and vocabulary words of 2-32 letters, "
        "the stream used cyclically from every start, 8 table rules (Vigenere, Beaufort, variant, Bury's reciprocal on "
        "standard or KRYPTOS numbering); each setting checks all 24 known letters (compiled). K4 against 10 shuffled "
        "copies; plants. A free table (the report's partition test) is not run."
    ),
    "hypothesis_expert": (
        "A9, F11: a keyword-only key stream from Friedman's training texts, the kind of rule a CIA cryptographer of "
        "Scheidt's generation learned; 'a matrix, then the table' (C1). Model: stream s = columnar_read(alphabet^n, "
        "keyword order), k_i = s[(o + i) mod 26n], c = T(p, k). Statistic: fitting settings, K4 against copies."
    ),
    "hypothesis_eli5": (
        "Friedman taught a way to make a long key from one word: write the alphabet several times into a grid as wide as "
        "the word, then copy the columns out in the word's alphabetical order. That jumbled alphabet is the key. Only the "
        "word and the number of repeats need remembering. We try every dictionary word."
    ),
    "prediction": "No setting fits all 24 known letters on K4 or on the copies; plants are found. Zero candidates.",
    "method": (
        "1. Every distinct column order from dictionary and vocabulary words of 2-32 letters. "
        "2. For each order, alphabet (standard, KRYPTOS) and n = 1-8: the stream. "
        "3. Every start and table rule: all 24 known letters must agree (compiled). "
        "4. K4 against 10 shuffled copies; two plants."
    ),
    "walkthrough": (
        "1. Take the word BERLIN: its letters in alphabetical order number B1 E2 I3 L4 N5 R6... as columns. "
        "2. Write ABCDEFGHIJKLMNOPQRSTUVWXYZ four times into rows of 6. "
        "3. Copy out column 1 (under B), then column 2 (under E), and so on: that is the key. "
        "4. Start it anywhere; on the sculpture's table, each known letter needs one key letter at its place. "
        "5. One disagreement ends the setting. Every word, repeat count, start and table; then scrambled copies."
    ),
}

import ctypes
import os
import random
import subprocess
import tempfile
import time
from pathlib import Path

from kryptos.facts import KNOWN, STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N_CONTROLS = 10
NMIN, NMAX = 1, 8
PLACES = sorted(KNOWN)
ROOT = Path(__file__).resolve().parent
if not (ROOT / "kryptos").exists():
    ROOT = Path.cwd()

C_SOURCE = r"""
// Friedman's keyed alphabet box: alphabet AL (26 letter numbers) written n times row by row into width w, columns
// read top-down in the order ord[0..w-1]; the stream (26n letters) used cyclically from start o as the key.
// kv[(r*NT + t)*24 + e]: key letter needed at known place e for rule r, text t. Counts fits per text.
static int KP[24];
void set_places(const int *kp) { for (int e = 0; e < 24; e++) KP[e] = kp[e]; }
void scan(const int *ords, const int *ws, int nwords, const int *AL, int nmin, int nmax, const int *kv, int nrules, int nt,
          long *fits, long *settings, int *hit, int cap, int *nhit) {
    int stream[26 * 16];
    for (int k = 0; k < nwords; k++) {
        const int *ord = ords + 32 * k; int w = ws[k];
        for (int n = nmin; n <= nmax; n++) {
            int L = 26 * n, R = (L + w - 1) / w, m = 0;
            for (int j = 0; j < w; j++) { int c = ord[j]; for (int r = 0; r < R; r++) { int cell = r * w + c; if (cell < L) stream[m++] = AL[cell % 26]; } }
            for (int o = 0; o < L; o++) {
                (*settings) += nrules;
                for (int r = 0; r < nrules; r++) for (int t = 0; t < nt; t++) {
                    const int *K = kv + (r * nt + t) * 24;
                    int e = 0;
                    while (e < 24 && stream[(o + KP[e]) % L] == K[e]) e++;
                    if (e == 24) { fits[t]++; if (t == 0 && *nhit < cap) { hit[4 * *nhit] = k; hit[4 * *nhit + 1] = n; hit[4 * *nhit + 2] = o; hit[4 * *nhit + 3] = r; (*nhit)++; } }
                }
            }
        }
    }
}
"""


def build():
    d = tempfile.mkdtemp(prefix="k4_abox_")
    src, so = os.path.join(d, "c.c"), os.path.join(d, "c.so")
    open(src, "w").write(C_SOURCE)
    subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", so, src], check=True, capture_output=True)
    return ctypes.CDLL(so)


def I(v):
    return (ctypes.c_int * len(v))(*v)


def number_key(key):
    return sorted(range(len(key)), key=lambda i: (key[i], i))


def rules():
    return [(a, f) for a in ("std", "kry") for f in ("vig", "beau", "var", "recip25")]


def needed(text, rule):
    A = STD if rule[0] == "std" else KRY
    out = []
    for q in PLACES:
        p, c = A.index(KNOWN[q]), A.index(text[q - 1])
        k = {"vig": (c - p) % 26, "beau": (c + p) % 26, "var": (p - c) % 26, "recip25": (25 - p - c) % 26}[rule[1]]
        out.append(STD.index(A[k]))
    return out


def stream(order, alph, n):
    w, L = len(order), 26 * n
    R = -(-L // w)
    return "".join(alph[(r * w + c) % 26] for c in order for r in range(R) if r * w + c < L)


def encipher(p, ks, rule, o):
    A = STD if rule[0] == "std" else KRY
    out = []
    for i, ch in enumerate(p):
        x = A.index(ch); kk = A.index(ks[(o + i) % len(ks)])
        out.append(A[{"vig": (x + kk) % 26, "beau": (kk - x) % 26, "var": (x - kk) % 26, "recip25": (25 - x - kk) % 26}[rule[1]]])
    return "".join(out)


def run(ctx):
    t0 = time.time()
    lib = build()
    lib.set_places(I([q - 1 for q in PLACES]))
    ct = ctx.K4
    words = [w.strip().upper() for w in (ROOT / "kryptos" / "data" / "words.txt").read_text().split()]
    words += [w.upper() for w in ctx.vocabulary if w.isalpha()]
    orders = {}
    for w in words:
        if w.isalpha() and 2 <= len(w) <= 32:
            orders.setdefault(tuple(number_key(w)), w)
    olist = list(orders)
    rng = random.Random(1920)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    PLANT_P = "USEDTHEEARTHSMAGNETICEASTNORTHEASTRMATIONWASGATHEREDANDTRANSMITBERLINCLOCKUNDTOANUNKNOWNLOCATIONX"
    plants = []
    for k, (alph, n, ri) in enumerate(((KRY, 4, 1), (STD, 6, 7))):
        oi = rng.randrange(len(olist)); o = rng.randrange(26 * n)
        texts.append(encipher(PLANT_P, stream(olist[oi], alph, n), rules()[ri], o))
        plants.append({"keyword": orders[olist[oi]], "alphabet": "kry" if alph == KRY else "std", "n": n, "start": o, "rule": "/".join(rules()[ri])})
    nt = len(texts)
    R = rules()
    kv = I([v for r in R for t in texts for v in needed(t, r)])
    flat = []
    for o in olist:
        flat += list(o) + [0] * (32 - len(o))
    ORD, WS = I(flat), I([len(o) for o in olist])
    out = {}
    k4hits = []
    for aname, alph in (("std", STD), ("kry", KRY)):
        fits = (ctypes.c_long * nt)(); settings = ctypes.c_long(0)
        hit = (ctypes.c_int * 400)(); nh = ctypes.c_int(0)
        lib.scan(ORD, WS, len(olist), I([STD.index(c) for c in alph]), NMIN, NMAX, kv, len(R), nt, fits, ctypes.byref(settings), hit, 100, ctypes.byref(nh))
        out[aname] = {"settings": settings.value, "fits": list(fits)}
        for j in range(nh.value):
            k4hits.append({"box": aname, "keyword": orders[olist[hit[4 * j]]], "n": hit[4 * j + 1], "start": hit[4 * j + 2], "rule": "/".join(R[hit[4 * j + 3]])})
    nc = 1 + N_CONTROLS
    fits_all = [out["std"]["fits"][t] + out["kry"]["fits"][t] for t in range(nt)]
    bounds = {
        "family": "Friedman's keyed alphabet box (MC III 35b): alphabet (std/KRYPTOS) x n (1-8) by rows, read by keyword column order, every dictionary keyword, every start, 8 tables, exact",
        "column_orders": len(olist), "settings_per_text": out["std"]["settings"] + out["kry"]["settings"],
        "fits": {"k4": fits_all[0], "copies": fits_all[1:nc], "plants": fits_all[nc:]},
        "plants": plants, "k4_hits": k4hits[:30],
        "copies": f"{N_CONTROLS} shuffled copies (seed 1920)", "seconds": round(time.time() - t0), "exhaustive": True,
    }
    notes = (f"{len(olist):,} column orders; fits K4 {fits_all[0]} (copies {min(fits_all[1:nc])}-{max(fits_all[1:nc])}); plants {fits_all[nc:]}")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    s = stream(number_key("BERLIN"), STD, 4)
    return "BERLIN, the alphabet four times in rows of 6, columns read in BERLIN's order: " + s
