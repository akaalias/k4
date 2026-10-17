"""Experiment 0195 (F5.2). See program.md for the contract."""

EXPERIMENT = {
    "slug": "gromark-free-alphabet-other-bases",
    "title": "F5.2: Gromark on a free mixed alphabet: three-term rules in bases 2-9, 11-16 and 26, and two-term rules with longer lags (base 10 to 8, other bases to 6): exact",
    "family": "5-gromark",
    "parent": "0107-three-term-gromark-with-a-free-alphabet",
    "changed": (
        "F5.2. 0107 closed three-term Gromark on a free alphabet in base 10 (lags up to 6); two-term free-alphabet rules "
        "were closed to lag 6 in base 10 and lag 5 in other bases (0069, 0076). Here, with 0107's decider compiled: "
        "three-term rules d[i] = d[i-a] + d[i-b] + d[i-c] mod B, 1 <= a < b < c <= 6, every primer, in bases 2-9 and "
        "11-16 (base 26 to c = 5; c = 6 there is 3 billion primers, blocked by cost); two-term rules with b = 7, 8 in base "
        "10 and b = 6 in bases 2-9, 11-16. Four forms (M[P+d]=c, M[P-d]=c, M[C-d]=p, M[C+d]=p), M a free alphabet; same "
        "known letters fix digit differences, then the partial one-to-one check. K4 against 10 shuffled copies; plants."
    ),
    "hypothesis_expert": (
        "C22(a) (YAR as a Gromark primer), C4(b) ('base 16', non-standard bases; Scheidt), F5. Model as 0107 with base B "
        "and the rule's lags. Exhaustive over primers. Statistic: consistent (rule, primer, form) settings, K4 against "
        "copies."
    ),
    "hypothesis_eli5": (
        "A Gromark key is a run of digits that grows by adding earlier digits together. Scheidt mentioned other number "
        "bases. We try the three-term and longer two-term rules in every base from 2 to 16 and 26, every starting "
        "digits, with any mixed alphabet, and see whether any fits the 24 known letters."
    ),
    "prediction": "No setting consistent on K4 or the copies, as in 0107; plants found. Zero candidates.",
    "method": (
        "1. For each base, rule and form: equal-letter pairs among the known letters fix digit differences (or kill the form). "
        "2. Every primer (compiled, 4 processes): the digit stream to place 74, the pair checks, then the one-to-one check. "
        "3. K4, 10 shuffled copies, 2 planted texts."
    ),
    "walkthrough": (
        "1. Base 16, rule 'add the digits 1, 3 and 6 places back', primer of 6 hex digits. "
        "2. Places 26 and 27 carve Q twice from N and O: in form M[P+d]=c, N + d26 and O + d27 must be the same slot. "
        "3. So d26 - d27 must be exactly 1; most primers fail here at once. "
        "4. A survivor must give one-to-one slots for all 24 known letters. "
        "5. Every primer, rule, base and form; then scrambled copies."
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
long scan(int B, int nl, const int *lags, long *counts, long *firsts, int cap, int *nfirst) {
    int c = 0; for (int j = 0; j < nl; j++) if (lags[j] > c) c = lags[j];
    int d[128], pr[16]; memset(pr, 0, sizeof pr);
    long n = 0;
    while (1) {
        for (int i = 0; i < c; i++) d[i] = pr[i];
        for (int i = c; i <= TOP; i++) { int s = 0; for (int j = 0; j < nl; j++) s += d[i - lags[j]]; d[i] = s % B; }
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
    n = lib.scan(B, len(lags), I(lags), cnt, fs, 20, ctypes.byref(nf))
    return B, lags, n, list(cnt)[:len(texts)], [fs[j] for j in range(nf.value)]


def jobs():
    out = []
    three = [(a, b, c) for c in range(3, 7) for b in range(2, c) for a in range(1, b)]
    for B in list(range(2, 10)) + list(range(11, 17)) + [26]:
        for r in three:
            if B == 26 and r[2] == 6:
                continue
            out.append((B, list(r)))
    for b in (7, 8):
        for a in range(1, b):
            out.append((10, [a, b]))
    for B in list(range(2, 10)) + list(range(11, 17)):
        for a in range(1, 6):
            out.append((B, [a, 6]))
    return out


def encipher(p, M, B, lags, primer):
    d = list(primer)
    for i in range(len(primer), len(p)):
        d.append(sum(d[i - l] for l in lags) % B)
    return "".join(M[(STD.index(ch) + d[i]) % 26] for i, ch in enumerate(p))


def run(ctx):
    import multiprocessing as mp
    t0 = time.time()
    so = build()
    ct = ctx.K4
    rng = random.Random(1940)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    PLANT_P = "USEDTHEEARTHSMAGNETICEASTNORTHEASTRMATIONWASGATHEREDANDTRANSMITBERLINCLOCKUNDTOANUNKNOWNLOCATIONX"
    plants = []
    for B, lags in ((16, [1, 3, 6]), (10, [2, 7])):
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
        "family": "Gromark, free mixed alphabet: three-term bases 2-9, 11-16 (lags to 6), 26 (lags to 5); two-term base 10 lags 7-8, bases 2-9, 11-16 lag 6; four forms; exact",
        "rule_jobs": len(J), "primers": primers, "per_base": per_base,
        "consistent": {"k4": tot[0], "copies": tot[1:nc], "plants": tot[nc:]}, "plants": plants, "k4_consistent": k4[:20],
        "blocked": "three-term base 26 with lag 6 (3.1 billion primers); two-term other bases beyond lag 6",
        "copies": f"{N_CONTROLS} shuffled copies (seed 1940)", "seconds": round(time.time() - t0), "exhaustive": True,
    }
    notes = f"{primers:,} primers x 4 forms; consistent K4 {tot[0]} (copies {min(tot[1:nc])}-{max(tot[1:nc])}); plants {tot[nc:]}"
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    B, lags, primer = 16, [1, 3, 6], [1, 2, 3, 4, 5, 6]
    d = list(primer)
    for i in range(6, 40):
        d.append(sum(d[i - l] for l in lags) % B)
    return ("base 16, each digit the sum of the digits 1, 3 and 6 places back, primer 1 2 3 4 5 6:" + chr(10) + " ".join(map(str, d[:34])) + chr(10) +
            f"places 26 and 27 (N, O over Q, Q), form M[P+d]=c: need d26 - d27 = 1; here {d[25]} - {d[26]} = {d[25] - d[26]}")
