"""Experiment 0187 (F10.1). See program.md for the contract."""

EXPERIMENT = {
    "slug": "chaocipher-keyword-left-wheels",
    "title": "F10.1: Chaocipher with the left (cipher) wheel started from any keyword-mixed alphabet at any rotation and the right (plain) wheel free: exact",
    "family": "10-self-changing-alphabets",
    "parent": "0119-one-free-alphabet-exact",
    "changed": (
        "F10.1, first family run. Counting checks first: in Chaocipher both wheels turn by the same amount, the place of "
        "the carved letter on the left wheel, and the left wheel's moves depend only on carved letters. So once the left "
        "wheel's start is fixed, the whole motion is fixed by the carved text, and each known letter says which letter "
        "stands at one place of the right wheel's start. The 24 known letters (13 different) then give 11 equalities "
        "plus distinctness on a right wheel that is otherwise free: a strong exact test. A free left wheel (26!, about "
        "88 bits) cannot be searched; every keyword-mixed alphabet from the dictionary and the vocabulary (208,627 "
        "distinct alphabets) at all 26 rotations can: 5.4 million left wheels, K4 and 10 shuffled copies, compiled."
    ),
    "hypothesis_expert": (
        "A10 (alphabets that change after every letter; knowledge/12-assumptions.md, for information); Chaocipher, J. F. "
        "Byrne 1918, offered to US agencies, method published 2010 (Rubin). Model: left wheel L (cipher), right wheel R "
        "(plain), zenith 0, nadir 13; encipher p as L[i] where R[i] = p; then L turned by i and its place-1 letter moved "
        "to the nadir, R turned by i + 1 and its place-2 letter moved to the nadir. Given L0, every i_t is fixed by the "
        "carved text, R_t[j] = R0[sigma_t(j)], and a known p_t requires R0[sigma_t(i_t)] = p_t. Statistic: consistent "
        "left wheels, K4 against 10 copies; plants as builder checks; implementation checked on Byrne's published test "
        "vector."
    ),
    "hypothesis_eli5": (
        "Chaocipher uses two alphabet wheels that are shuffled a little after every letter, so the same letter almost "
        "never turns into the same code letter twice. A neat property: how the wheels move depends only on the code "
        "letters, which we can all read on the copper. So if we guess how the cipher wheel started, the 24 known letters "
        "tell us exactly where letters must sit on the other wheel, and contradictions show at once. We try every "
        "starting cipher wheel made from an English word, at every turn."
    ),
    "prediction": "No keyword-started left wheel is consistent on K4 or on the copies (11 equalities each); plants are found. Zero candidates.",
    "method": (
        "1. Check the implementation on Byrne's test vector (WELLDONEISBETTERTHANWELLSAID). "
        "2. Build every distinct keyword-mixed alphabet from the dictionary and the vocabulary. "
        "3. For each alphabet and rotation as the left wheel's start, run the wheels along each text to the last known "
        "place, collecting the right wheel's forced letters; stop at the first contradiction. "
        "4. Count consistent wheels on K4, 10 copies and 3 planted texts."
    ),
    "walkthrough": (
        "1. Start the left wheel as the alphabet mixed from, say, BERLIN, turned 5 places. "
        "2. Find the carved O on it: its place i says how far both wheels turn; do the same for every carved letter in order. "
        "3. At place 22 the carved F sits at some place i on the left wheel; the known E must sit at place i of the right "
        "wheel at that moment, which traces back to one place of the right wheel's start. "
        "4. Every known letter fixes one place of the right wheel's start; two Es must trace back to the same place, two "
        "different letters to different places. "
        "5. One contradiction rules the starting wheel out."
    ),
}

import ctypes
import os
import random
import subprocess
import tempfile
import time
from pathlib import Path

from kryptos.facts import KNOWN
from kryptos.alphabets import keyword_mixed

N_CONTROLS = 10
A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PLACES = sorted(KNOWN)
ROOT = Path(__file__).resolve().parent
if not (ROOT / "kryptos").exists():
    ROOT = Path.cwd()

C_SOURCE = r"""
// Chaocipher (Byrne 1918, method published 2010). Left wheel = cipher alphabet, right wheel = plain alphabet, zenith 0,
// nadir 13. After each letter both wheels turn by the same amount i (the place of the carved letter on the left wheel),
// the right one a step further, then each takes out one letter (left: place 1, right: place 2) and puts it at the nadir.
// So given the left wheel's start, every move is fixed by the carved text, and each known letter p at step t says:
// R0[ridx_t[i_t]] = p. Consistent iff those assignments form a partial one-to-one map.
#include <string.h>
static int CT[16][97], NT, KP[24], KL[24], LAST;
static int ISK[97], KIDX[97];
void set_texts(int nt, const int *ct, const int *kp, const int *kl) {
    NT = nt;
    for (int t = 0; t < nt; t++) for (int j = 0; j < 97; j++) CT[t][j] = ct[t * 97 + j];
    for (int j = 0; j < 97; j++) { ISK[j] = 0; KIDX[j] = -1; }
    LAST = 0;
    for (int e = 0; e < 24; e++) { KP[e] = kp[e]; KL[e] = kl[e]; ISK[kp[e]] = 1; KIDX[kp[e]] = e; if (kp[e] > LAST) LAST = kp[e]; }
}
static inline void permute(int *w, int rot, int ext) {
    int tmp[26];
    for (int j = 0; j < 26; j++) tmp[j] = w[(j + rot) % 26];
    int x = tmp[ext];
    for (int j = ext; j < 13; j++) tmp[j] = tmp[j + 1];
    tmp[13] = x;
    memcpy(w, tmp, sizeof tmp);
}
// returns 1 if consistent for text t; fills r0 (letter at each R0 index, -1 unknown) if r0 != 0
int test(int t, const int *L0, int *r0out) {
    int L[26], pos[26], R[26], r0[26], used[26];
    memcpy(L, L0, sizeof L);
    for (int j = 0; j < 26; j++) { R[j] = j; r0[j] = -1; used[j] = 0; }
    for (int s = 0; s <= LAST; s++) {
        for (int j = 0; j < 26; j++) pos[L[j]] = j;
        int i = pos[CT[t][s]];
        if (ISK[s]) {
            int idx = R[i], p = KL[KIDX[s]];
            if (r0[idx] < 0) { if (used[p]) return 0; r0[idx] = p; used[p] = 1; }
            else if (r0[idx] != p) return 0;
        }
        permute(L, i, 1);
        permute(R, (i + 1) % 26, 2);
    }
    if (r0out) memcpy(r0out, r0, sizeof r0);
    return 1;
}
// many left wheels: returns count consistent per text, writes indices of consistent wheels for text 0 (cap)
void scan(const int *wheels, int n, long *counts, int *hits, int cap, int *nhit) {
    for (int w = 0; w < n; w++) {
        for (int t = 0; t < NT; t++) {
            if (test(t, wheels + 26 * w, 0)) { counts[t]++; if (t == 0 && *nhit < cap) hits[(*nhit)++] = w; }
        }
    }
}
// full encipher / decipher for checks
void crypt(const int *L0, const int *R0, const int *in, int n, int dec, int *out) {
    int L[26], R[26], pl[26], pr[26];
    memcpy(L, L0, sizeof L); memcpy(R, R0, sizeof R);
    for (int s = 0; s < n; s++) {
        for (int j = 0; j < 26; j++) { pl[L[j]] = j; pr[R[j]] = j; }
        int i = dec ? pl[in[s]] : pr[in[s]];
        out[s] = dec ? R[i] : L[i];
        permute(L, i, 1);
        permute(R, (i + 1) % 26, 2);
    }
}
// every rotation of each alphabet as the left wheel's start
void scan_rot(const int *alph, int n, long *counts, int *hits, int cap, int *nhit) {
    int w[26];
    for (int a = 0; a < n; a++) {
        for (int r = 0; r < 26; r++) {
            for (int j = 0; j < 26; j++) w[j] = alph[26 * a + (j + r) % 26];
            for (int t = 0; t < NT; t++) {
                if (test(t, w, 0)) { counts[t]++; if (t == 0 && *nhit < cap) { hits[2 * (*nhit)] = a; hits[2 * (*nhit) + 1] = r; (*nhit)++; } }
            }
        }
    }
}
"""


def build():
    d = tempfile.mkdtemp(prefix="k4_chao_")
    src, so = os.path.join(d, "c.c"), os.path.join(d, "c.so")
    open(src, "w").write(C_SOURCE)
    subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", so, src], check=True, capture_output=True)
    return ctypes.CDLL(so)


def I(v):
    return (ctypes.c_int * len(v))(*v)


def run(ctx):
    t0 = time.time()
    lib = build()
    ct = ctx.K4
    # implementation check: Byrne's published test vector
    out = (ctypes.c_int * 28)()
    lib.crypt(I([A.index(c) for c in "HXUCZVAMDSLKPEFJRIGTWOBNYQ"]), I([A.index(c) for c in "PTLNBQDEOYSFAVZKGJRIHWXUMC"]),
              I([A.index(c) for c in "WELLDONEISBETTERTHANWELLSAID"]), 28, 0, out)
    vector_ok = "".join(A[x] for x in out) == "OAHQHCNYNXTSZJRRHJBYHQKSOUJY"
    assert vector_ok
    words = [w.strip().upper() for w in (ROOT / "kryptos" / "data" / "words.txt").read_text().split()]
    words += [w.upper() for w in ctx.vocabulary if w.isalpha()]
    alph = {}
    for w in words:
        if w.isalpha() and len(w) >= 3:
            a = keyword_mixed(w)
            alph.setdefault(a, w)
    for a, w in (("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "(standard)"), ("ZYXWVUTSRQPONMLKJIHGFEDCBA", "(reversed)")):
        alph.setdefault(a, w)
    alist = list(alph)
    rng = random.Random(1870)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    PLANT_P = "USEDTHEEARTHSMAGNETICEASTNORTHEASTRMATIONWASGATHEREDANDTRANSMITBERLINCLOCKUNDTOANUNKNOWNLOCATIONX"
    plants = []
    for k in range(3):
        ai = rng.randrange(len(alist)); r = rng.randrange(26)
        L0 = alist[ai][r:] + alist[ai][:r]
        R0 = list(A); rng.shuffle(R0)
        o = (ctypes.c_int * 97)()
        lib.crypt(I([A.index(c) for c in L0]), I([A.index(c) for c in R0]), I([A.index(c) for c in PLANT_P]), 97, 0, o)
        texts.append("".join(A[x] for x in o))
        plants.append({"keyword": alph[alist[ai]], "rotation": r})
    lib.set_texts(len(texts), I([A.index(c) for t in texts for c in t]), I([q - 1 for q in PLACES]), I([A.index(KNOWN[q]) for q in PLACES]))
    flat = [A.index(c) for a in alist for c in a]
    counts = (ctypes.c_long * len(texts))()
    hits = (ctypes.c_int * 200)(); nh = ctypes.c_int(0)
    lib.scan_rot(I(flat), len(alist), counts, hits, 100, ctypes.byref(nh))
    k4_hits = [{"keyword": alph[alist[hits[2 * j]]], "rotation": hits[2 * j + 1]} for j in range(nh.value)]
    nc = 1 + N_CONTROLS
    bounds = {
        "family": "Chaocipher, left wheel from any keyword-mixed alphabet (dictionary + vocabulary) at any rotation, right wheel free, exact",
        "test_vector_ok": vector_ok, "alphabets": len(alist), "left_wheels": 26 * len(alist),
        "consistent": {"k4": counts[0], "copies": list(counts[1:nc]), "plants": list(counts[nc:])},
        "plants": plants, "k4_hits": k4_hits[:40],
        "checks": "24 known letters, 13 different: 11 equalities on the right wheel's start, plus distinctness",
        "free_left_wheel": "26! starts (about 88 bits) against about 51 bits of checks: not searchable; blocked",
        "copies": f"{N_CONTROLS} shuffled copies (seed 1870)", "seconds": round(time.time() - t0), "exhaustive": True,
    }
    notes = (f"{26 * len(alist):,} left wheels; consistent K4 {counts[0]} (copies {min(counts[1:nc])}-{max(counts[1:nc])}); "
             f"plants {list(counts[nc:])}; Byrne's test vector reproduced")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    L0 = keyword_mixed("BERLIN")
    ct = ctx.K4
    L = [A.index(c) for c in L0]
    lines = [f"left wheel starts as the BERLIN alphabet {L0}", ""]
    for s in range(24):
        i = L.index(A.index(ct[s]))
        lines.append(f"place {s + 1}: carved {ct[s]} at left-wheel place {i}: the left wheel turns by {i}, the right by {i + 1}")
        t = [L[(j + i) % 26] for j in range(26)]
        x = t[1]; t = [t[0]] + t[2:14] + [x] + t[14:]
        L = t
    return "\n".join(lines)
