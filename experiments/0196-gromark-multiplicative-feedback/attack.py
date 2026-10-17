"""Experiment 0197 (F5.1). See program.md for the contract."""

EXPERIMENT = {
    "slug": "gromark-multiplicative-feedback",
    "title": "F5.1: Gromark with multiplicative feedback (each digit the product of two earlier ones) on a free mixed alphabet, bases 2-16 and 26, every primer: exact; YAR as a primer by subsumption",
    "family": "5-gromark",
    "parent": "0195-gromark-free-alphabet-other-bases",
    "changed": (
        "F5.1. Every Gromark rule tested so far adds earlier digits. Here d[i] = d[i-a] * d[i-b] mod B, 1 <= a < b <= 6, "
        "every primer, bases 2-16 (base 26 with b <= 5: lag 6 is 1.5 billion primers), four forms, a free mixed alphabet, "
        "with 0195's compiled decider in product mode. YAR as a primer (Y A R as 24 0 17 in base 26, or any digits) is one "
        "of the primers every exhaustive sweep already enumerates (0076 two-term base 26, 0195 three-term base 26), so it "
        "is closed by subsumption."
    ),
    "hypothesis_expert": (
        "F5.1 (low value: no creator remark points here), C22(a) (YAR as a primer). Model as 0107/0195 with the "
        "recurrence multiplicative. Statistic: consistent (rule, primer, form) settings, K4 against 10 copies; plants."
    ),
    "hypothesis_eli5": (
        "A variation of the Gromark key: each new digit is the product, not the sum, of two earlier digits. We try every "
        "base from 2 to 16 and 26, every pair of earlier positions up to six back, every set of starting digits, with any "
        "mixed alphabet."
    ),
    "prediction": "No setting consistent on K4 or the copies. Zero candidates.",
    "method": (
        "1. For each base, rule and form: equal-letter pairs fix digit differences (or kill the form). "
        "2. Every primer (compiled, 4 processes), product recurrence, pair checks, then the one-to-one check. "
        "3. K4, 10 shuffled copies, 2 planted texts."
    ),
    "walkthrough": (
        "1. Base 10, rule 'multiply the digits 2 and 5 places back', primer of 5 digits. "
        "2. The digit stream often collapses to zeros; then the key is constant and K4's three different carved letters "
        "under the known E rule it out at once. "
        "3. Otherwise the same checks as the additive Gromark: equal known letters must land on equal slots. "
        "4. Every primer, rule, base and form; then scrambled copies."
    ),
}

import ctypes
import os
import random
import subprocess
import tempfile
import time

from kryptos.facts import KNOWN, STANDARD_ALPHABET as STD

N_CONTROLS = 10
FORMS = ("M[P+d]=c", "M[P-d]=c", "M[C-d]=p", "M[C+d]=p")
ITEMS = sorted(KNOWN.items())

C_SOURCE = r"""
// Gromark on a free mixed alphabet, base B: digits d[i] = sum of d[i - lag_j] (2 or 3 lags) mod B, primer = first
// c digits (every primer enumerated). Four forms: slot = (base_k + s*d[idx_k]) mod 26 must biject with the letter
// at each known place. Per text and form: pairs (k, l, diff) with d_k - d_l == diff (same letter), then full check.
#include <string.h>
#define MAXT 16
static int NT, IDX[24], TOP;
static int NPAIR[MAXT][4], PK[MAXT][4][300], PL[MAXT][4][300], PD[MAXT][4][300], ALIVE[MAXT][4];
static int BASE[MAXT][4][24], SGN[MAXT][4], LET[MAXT][4][24];
void set_idx(const int *idx) { TOP = 0; for (int e = 0; e < 24; e++) { IDX[e] = idx[e]; if (idx[e] > TOP) TOP = idx[e]; } }
void set_text(int t, int f, int alive, const int *base, int sgn, const int *let, int np, const int *pk, const int *pl, const int *pd) {
    if (t + 1 > NT) NT = t + 1;
    ALIVE[t][f] = alive; SGN[t][f] = sgn; NPAIR[t][f] = np;
    for (int e = 0; e < 24; e++) { BASE[t][f][e] = base[e]; LET[t][f][e] = let[e]; }
    for (int j = 0; j < np; j++) { PK[t][f][j] = pk[j]; PL[t][f][j] = pl[j]; PD[t][f][j] = pd[j]; }
}
void reset(void) { NT = 0; }
// returns primers tried; counts[t] fits; first K4 fits recorded
long scan(int B, int nl, const int *lags, long *counts, long *firsts, int cap, int *nfirst, int mul) {
    int c = 0; for (int j = 0; j < nl; j++) if (lags[j] > c) c = lags[j];
    int d[128], pr[16]; memset(pr, 0, sizeof pr);
    long n = 0;
    while (1) {
        for (int i = 0; i < c; i++) d[i] = pr[i];
        for (int i = c; i <= TOP; i++) { int s = mul ? 1 : 0; for (int j = 0; j < nl; j++) s = mul ? (s * d[i - lags[j]]) % B : s + d[i - lags[j]]; d[i] = s % B; }
        for (int t = 0; t < NT; t++) for (int f = 0; f < 4; f++) {
            if (!ALIVE[t][f]) continue;
            int ok = 1;
            for (int j = 0; j < NPAIR[t][f]; j++) if (d[IDX[PK[t][f][j]]] - d[IDX[PL[t][f][j]]] != PD[t][f][j]) { ok = 0; break; }
            if (!ok) continue;
            int s2l[26], l2s[26]; for (int x = 0; x < 26; x++) { s2l[x] = -1; l2s[x] = -1; }
            for (int e = 0; e < 24 && ok; e++) {
                int slot = ((BASE[t][f][e] + SGN[t][f] * d[IDX[e]]) % 26 + 26) % 26, L = LET[t][f][e];
                if (s2l[slot] < 0 && l2s[L] < 0) { s2l[slot] = L; l2s[L] = slot; }
                else if (s2l[slot] != L || l2s[L] != slot) ok = 0;
            }
            if (ok) { counts[t]++; if (t == 0 && *nfirst < cap) firsts[(*nfirst)++] = n * 4 + f; }
        }
        n++;
        int i = 0;
        while (i < c && ++pr[i] == B) { pr[i] = 0; i++; }
        if (i == c) break;
    }
    return n;
}
"""

SO = None


def build():
    d = tempfile.mkdtemp(prefix="k4_grom_")
    src, so = os.path.join(d, "c.c"), os.path.join(d, "c.so")
    open(src, "w").write(C_SOURCE)
    subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", so, src], check=True, capture_output=True)
    return so


def I(v):
    return (ctypes.c_int * len(v))(*v)


def load(lib, t, text, B):
    for f in range(4):
        rows = []
        for q, p in ITEMS:
            c = text[q - 1]
            rows.append({0: (STD.index(p), 1, c), 1: (STD.index(p), -1, c), 2: (STD.index(c), -1, p), 3: (STD.index(c), 1, p)}[f])
        pk, pl, pd = [], [], []
        alive = 1
        for k in range(24):
            for l in range(k + 1, 24):
                if rows[k][2] == rows[l][2]:
                    need = (rows[k][1] * (rows[l][0] - rows[k][0])) % 26
                    cands = [x for x in (need, need - 26) if -(B - 1) <= x <= B - 1]
                    if not cands:
                        alive = 0
                    elif len(cands) == 1:
                        pk.append(k); pl.append(l); pd.append(cands[0])
        lib.set_text(t, f, alive, I([r[0] for r in rows]), rows[0][1], I([ord(r[2]) - 65 for r in rows]), len(pk), I(pk or [0]), I(pl or [0]), I(pd or [0]))


def job(args):
    so, texts, B, lags = args
    lib = ctypes.CDLL(so)
    lib.scan.restype = ctypes.c_long
    lib.reset()
    lib.set_idx(I([q - 1 for q, _ in ITEMS]))
    for t, text in enumerate(texts):
        load(lib, t, text, B)
    cnt = (ctypes.c_long * 16)(); fs = (ctypes.c_long * 20)(); nf = ctypes.c_int(0)
    n = lib.scan(B, len(lags), I(lags), cnt, fs, 20, ctypes.byref(nf), 1)
    return B, lags, n, list(cnt)[:len(texts)], [fs[j] for j in range(nf.value)]


def jobs():
    out = []
    for B in list(range(2, 17)) + [26]:
        for b in range(2, 7):
            if B == 26 and b == 6:
                continue
            for a in range(1, b):
                out.append((B, [a, b]))
    return out


def encipher(p, M, B, lags, primer):
    d = list(primer)
    for i in range(len(primer), len(p)):
        x = 1
        for l in lags:
            x = x * d[i - l] % B
        d.append(x)
    return "".join(M[(STD.index(ch) + d[i]) % 26] for i, ch in enumerate(p))


def run(ctx):
    import multiprocessing as mp
    t0 = time.time()
    so = build()
    ct = ctx.K4
    rng = random.Random(1970)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    PLANT_P = "USEDTHEEARTHSMAGNETICEASTNORTHEASTRMATIONWASGATHEREDANDTRANSMITBERLINCLOCKUNDTOANUNKNOWNLOCATIONX"
    plants = []
    for B, lags in ((13, [1, 4]), (26, [2, 5])):
        M = list(STD); rng.shuffle(M)
        primer = [rng.randrange(B) for _ in range(max(lags))]
        texts.append(encipher(PLANT_P, M, B, lags, primer))
        plants.append({"base": B, "lags": lags, "primer": primer})
    J = jobs()
    import sys, types
    mod = sys.modules.get(__name__)
    if getattr(mod, "job", None) is not job:
        m = types.ModuleType(__name__); m.__dict__.update(globals()); sys.modules[__name__] = m
    with mp.get_context("fork").Pool(4) as pool:
        res = pool.map(job, [(so, texts, B, lags) for B, lags in J], chunksize=1)
    nc = 1 + N_CONTROLS
    tot = [0] * len(texts)
    primers = 0
    k4 = []
    per_base = {}
    for B, lags, n, cnt, fs in res:
        primers += n
        for t in range(len(texts)):
            tot[t] += cnt[t]
        pb = per_base.setdefault(B, {"rules": 0, "primers": 0, "k4": 0})
        pb["rules"] += 1; pb["primers"] += n; pb["k4"] += cnt[0]
        for x in fs:
            k4.append({"base": B, "lags": lags, "primer_index": x // 4, "form": FORMS[x % 4]})
    bounds = {
        "family": "Gromark with multiplicative feedback d[i] = d[i-a] d[i-b] mod B, free mixed alphabet, bases 2-16 (lags to 6) and 26 (lags to 5), four forms, exact",
        "rule_jobs": len(J), "primers": primers, "per_base": per_base,
        "consistent": {"k4": tot[0], "copies": tot[1:nc], "plants": tot[nc:]}, "plants": plants, "k4_consistent": k4[:20],
        "blocked": "base 26 with lag 6 (1.5 billion primers)", "yar_primer": "subsumed: every primer enumerated in 0076 and 0195",
        "copies": f"{N_CONTROLS} shuffled copies (seed 1970)", "seconds": round(time.time() - t0), "exhaustive": True,
    }
    notes = f"{primers:,} primers x 4 forms; consistent K4 {tot[0]} (copies {min(tot[1:nc])}-{max(tot[1:nc])}); plants {tot[nc:]}"
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    B, lags, primer = 10, [2, 5], [3, 7, 9, 1, 4]
    d = list(primer)
    for i in range(5, 40):
        d.append(d[i - 2] * d[i - 5] % B)
    return "base 10, each digit the product of the digits 2 and 5 places back, primer 3 7 9 1 4:" + chr(10) + " ".join(map(str, d[:40]))
