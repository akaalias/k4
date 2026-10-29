"""Experiment F5.2 rerun (draft). See program.md for the contract."""

EXPERIMENT = {
    "slug": "f5.2-gromark-free-alphabet-base-26-lag-6-and-longer-lags",
    "title": "F5.2: Gromark on a free mixed alphabet, the rules 0195 left for cost: three-term base 26 to lag 6, three-term lag 7 in bases 2-16, two-term base 26 lags 6-7, two-term lags 7-8 in bases 2-16, base 10 lags 9-10: exact",
    "family": "5-gromark",
    "parent": "0195-gromark-free-alphabet-other-bases",
    "changed": (
        "F5.2, reopened by D2 (0252): 0195 left three-term base 26 at lag 6 (3.1 billion primers) and longer two-term "
        "lags blocked under the old 30-minute budget; issue #96 removed the time limit. Same compiled exact test as 0195 "
        "(equal known letters fix digit differences, then the one-to-one check on the free alphabet), now split by the "
        "primer's last digit so the work spreads over any number of workers; the rule set widened to every rule up to "
        "about 2.3 x 10^11 primers in total."
    ),
    "hypothesis_expert": (
        "C22(a) (YAR as a Gromark primer; base 26 lets a letter primer be read directly as digits), C4(b) (Scheidt's "
        "other bases), F5. Model as 0107/0195: d[i] = sum of d[i - lag] over the rule's two or three lags mod B, the primer "
        "the first max(lag) digits, four forms M[P+d]=c, M[P-d]=c, M[C-d]=p, M[C+d]=p with M a free alphabet. Exhaustive "
        "over primers. Statistic: consistent (rule, primer, form) settings, K4 against 10 shuffled copies; three plants."
    ),
    "hypothesis_eli5": (
        "A Gromark key is a run of digits that grows by adding earlier digits together, from a few starting digits. "
        "Some longer versions, and the version that counts in 26s (one digit per letter), were never tried because they "
        "took too long. Now there is no time limit, so every starting run is tried for each of them, with any scrambled "
        "alphabet, to see whether any fits the 24 known letters."
    ),
    "prediction": "No setting consistent on K4 or the copies (as 0195); every plant found. Zero candidates.",
    "method": (
        "1. For each base, rule and form: equal letters among the known places fix digit differences (or kill the form). "
        "2. Every primer, split by its last digit into one job per (rule, digit): the digit stream to place 74, the "
        "pair checks, then the one-to-one check. "
        "3. K4, 10 shuffled copies (0195's seed) and 3 planted texts in the same scan."
    ),
    "walkthrough": (
        "1. Base 26, rule 'add the digits 1, 3 and 6 places back', primer of 6 digits 0-25 (a six-letter word read A=0). "
        "2. Grow the digit stream to place 74. "
        "3. Places 26 and 27 carve Q twice from N and O: in form M[P+d]=c, N + d26 and O + d27 must be the same slot, "
        "so d26 - d27 must be 1 (or -25). "
        "4. A survivor must give one-to-one slots for all 24 known letters. "
        "5. Every primer, rule and form; then the scrambled copies."
    ),
    "expected_minutes": 120,
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
long scan(int B, int nl, const int *lags, long *counts, long *firsts, int cap, int *nfirst, int top) {
    int c = 0; for (int j = 0; j < nl; j++) if (lags[j] > c) c = lags[j];
    int d[128], pr[16]; memset(pr, 0, sizeof pr); pr[c - 1] = top;
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
        while (i < c - 1 && ++pr[i] == B) { pr[i] = 0; i++; }
        if (i == c - 1) break;
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
    so, texts, B, lags, top = args
    lib = ctypes.CDLL(so)
    lib.scan.restype = ctypes.c_long
    lib.reset()
    lib.set_idx(I([q - 1 for q, _ in ITEMS]))
    for t, text in enumerate(texts):
        load(lib, t, text, B)
    cnt = (ctypes.c_long * 16)(); fs = (ctypes.c_long * 20)(); nf = ctypes.c_int(0)
    n = lib.scan(B, len(lags), I(lags), cnt, fs, 20, ctypes.byref(nf), top)
    return B, lags, top, n, list(cnt)[:len(texts)], [fs[j] for j in range(nf.value)]


def jobs():
    """The rules 0195 left: three-term base 26 to lag 6; three-term lag 7 in bases 2-16; two-term base 26 lags 6-7;
    two-term lags 7-8 in bases 2-9, 11-16; two-term base 10 lags 9-10."""
    from itertools import combinations
    out = []
    for r in combinations(range(1, 6), 2):
        out.append((26, list(r) + [6]))
    for B in range(2, 17):
        for r in combinations(range(1, 7), 2):
            out.append((B, list(r) + [7]))
    for b in (6, 7):
        for a in range(1, b):
            out.append((26, [a, b]))
    for B in list(range(2, 10)) + list(range(11, 17)):
        for b in (7, 8):
            for a in range(1, b):
                out.append((B, [a, b]))
    for b in (9, 10):
        for a in range(1, b):
            out.append((10, [a, b]))
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
    for B, lags in ((26, [1, 3, 6]), (16, [2, 8]), (26, [2, 7])):
        M = list(STD); rng.shuffle(M)
        primer = [rng.randrange(B) for _ in range(max(lags))]
        texts.append(encipher(PLANT_P, M, B, lags, primer))
        plants.append({"base": B, "lags": lags, "primer": primer})
    J = jobs()
    import sys, types
    mod = sys.modules.get(__name__)
    if getattr(mod, "job", None) is not job:
        m = types.ModuleType(__name__); m.__dict__.update(globals()); sys.modules[__name__] = m
    W = int(os.environ.get("K4_WORKERS", 8))
    work = [(so, texts, B, lags, top) for B, lags in J for top in range(B)]
    work.sort(key=lambda w: -(w[2] ** (max(w[3]) - 1)))          # largest jobs first
    saved = getattr(ctx, "saved", {}) or {}
    def ukey(B, lags, top):
        return f"{B}:{'-'.join(map(str, lags))}:{top}"
    res = [tuple(saved[ukey(w[2], w[3], w[4])]) for w in work if ukey(w[2], w[3], w[4]) in saved]
    todo = [w for w in work if ukey(w[2], w[3], w[4]) not in saved]
    ctx.progress(len(res), len(work), "rule slices")
    with mp.get_context("fork").Pool(W) as pool:
        for r in pool.imap_unordered(job, todo, chunksize=1):
            res.append(r)
            ctx.save(ukey(r[0], r[1], r[2]), list(r))
            ctx.progress(len(res), len(work), "rule slices")
    nc = 1 + N_CONTROLS
    tot = [0] * len(texts)
    primers = 0
    k4 = []
    per_base = {}
    for B, lags, top, n, cnt, fs in res:
        primers += n
        for t in range(len(texts)):
            tot[t] += cnt[t]
        pb = per_base.setdefault(B, {"rules": 0, "primers": 0, "k4": 0})
        pb["rules"] += top == 0; pb["primers"] += n; pb["k4"] += cnt[0]
        for x in fs:
            k4.append({"base": B, "lags": lags, "top_digit": top, "primer_index_below_top": x // 4, "form": FORMS[x % 4]})
    bounds = {
        "family": "Gromark, free mixed alphabet, the rules 0195 left: three-term base 26 lag 6; three-term lag 7 in bases 2-16; two-term base 26 lags 6-7; two-term lags 7-8 in bases 2-9, 11-16; two-term base 10 lags 9-10; four forms; exact",
        "rule_jobs": len(J), "primers": primers, "per_base": per_base,
        "consistent": {"k4": tot[0], "copies": tot[1:nc], "plants": tot[nc:]}, "plants": plants, "k4_consistent": k4[:20],
        "not_covered": "three-term lag 8 and beyond; two-term base 26 lag 8 and beyond (26^8 = 2.1e11 primers per rule); two-term lags beyond 8 outside base 10",
        "copies": f"{N_CONTROLS} shuffled copies (seed 1940)", "seconds": round(time.time() - t0), "exhaustive": True,
        "cost_estimate": "2.34e11 primers at about 2.4 million per core-second with 14 texts (desk timing 2026-10-29): about 27 core-hours, about 1 h on 32 cores, about $1.5 of Modal credit",
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
