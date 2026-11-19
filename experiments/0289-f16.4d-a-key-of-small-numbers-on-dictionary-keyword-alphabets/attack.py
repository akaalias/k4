"""Experiment: F16.4d. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f16.4d-a-key-of-small-numbers-on-dictionary-keyword-alphabets",
    "title": "F16.4d: a key of small numbers on keyword alphabets: every pair of dictionary keyword alphabets (208,064 each side, the plain and KRYPTOS alphabets among them) under which every known place needs a key inside ten neighbouring values (the digits 0-9, or ten values from any start), with up to 2 slips; K4 against 50 shuffles; the forced digits of K4's fits read for a period or a known number",
    "family": "16-simple-hand-methods",
    "parent": "0288-f16.4a-what-carries-the-small-shifts-line-or-letter",
    "changed": (
        "F16.4d (issue #123). 0288 found the small shifts go with the plaintext letter, not the carved line, so by the "
        "rule set before that run the alphabets come first. New here: no period is assumed. For each ordered pair of "
        "alphabets (plain side, cipher side) from the 208,064 of 0244 and each form, the key each known place forces "
        "is computed and the table is listed when all of them (but at most 2) lie in the digits 0-9 (literal), or in "
        "ten neighbouring values from any start (a digit added to one fixed letter). On the 20 official letters and "
        "on all 24. Strength aimed at: exact for the list and the counts; the verdict on K4 is a count against "
        "shuffles plus a reading of the forced digits."
    ),
    "hypothesis_expert": (
        "Bean 2021, section 2.3 (bean-2021-cryptodiagnosis-of-k4.txt, Tables 2 and 3; Materna 2020): the images of a "
        "repeated plaintext letter are close, 'the cipher alphabet is near the standard A-Z alphabet, perhaps based on "
        "a keyword', with a small numeric key; C27(b), C5(a) (a key word sets the alphabet), C23(b) (the K2 "
        "coordinates as digits). Arithmetic, so by rule 7 of order-of-work.md it needs its reason: a key of digits is "
        "what small shifts would be the trace of, and 0286-0288 replicated them. Model: c = C[(P(p) + k) mod 26] "
        "(Vigenere), k = P(p) - C(c) (variant) or k = P(p) + C(c) (Beaufort), P and C keyword-mixed alphabets of any "
        "dictionary word (kryptos.alphabets.keyword_mixed), k in 0-9 at every place, no period. Space: 208,064^2 = "
        "4.3 x 10^10 pairs x 2 key rules x 26 starts. Gromark with a free alphabet (0069, 0076, 0195, 0262) and "
        "periodic keys on these pairs (0244) are closed; digits beside a word were 0024, 0038, 0175. Chance: "
        "(10/26)^24 = 1.1 x 10^-10 per pair, rule and start, so about 14 literal fits per text by chance and several "
        "hundred with a free start: a fit is not a result. What would be: K4's count far above its shuffles (it is "
        "expected somewhat above, since the closeness is replicated), a fit whose forced digits repeat with a period "
        "or continue a known number, or a fit inside a much narrower window (five values or fewer has chance below "
        "10^-6 over the whole space). The 73 other letters cannot be read from a fit alone: ten choices per letter "
        "(3.3 bits) exceed what English decides (0136: 1.78 bits per letter)."
    ),
    "hypothesis_eli5": (
        "K4's known letters often sit only a step or two from the carved letters. One simple way to get that: mix the "
        "alphabet with a key word, then move each letter on by a small number, a digit from a date or a coordinate. "
        "We try every dictionary word as the key word for the message alphabet and for the carved alphabet and list "
        "the pairs under which every known letter needs only a digit from 0 to 9. Scrambled copies of K4 show how "
        "many such pairs turn up by luck."
    ),
    "prediction": (
        "K4 has literal fits at no slip, about as many as chance gives (5-40), and is above the median shuffle but "
        "not above all 50 in most cells. No fit's digits repeat with a period or match a known number. No fit needs "
        "a window narrower than 8 values. Plants: the planted table is listed 8 of 8."
    ),
    "method": (
        "1. Build the 208,064 keyword alphabets. 2. Per text, drop alphabets that cannot fit on their own side "
        "whatever the other side is (two known places with the same carved letter force a difference that depends on "
        "the plain alphabet only; the same for a repeated plaintext letter and the cipher alphabet), allowing 2 slips. "
        "3. For every remaining pair and both key rules, run through the known places keeping, for each of the 26 "
        "starts at once, whether 0, 1 or 2 places have fallen outside the ten values (bit masks, compiled C, early "
        "exit); the 20 official places first, then EAST. 4. Count per cell (20 or 24 letters; literal Vigenere, "
        "variant, Beaufort; free start; slips 0, 1, 2); list the literal fits and the no-slip free-start fits. "
        "5. K4, 50 shuffles (known letters kept in place), 8 plants (random dictionary alphabets, random digits, two "
        "with a slip). 6. For K4's fits: the narrowest window, a period 1-26, a known number (the K2 coordinates, "
        "dates, pi, e)."
    ),
    "walkthrough": (
        "1. Write a key word, then the rest of the alphabet after it: that is the message alphabet. Do the same with a second word for the carved alphabet. "
        "2. For place 26, find N in the message alphabet and Q in the carved alphabet and count the steps from one to the other. "
        "3. Do this for all 24 known places. "
        "4. If every count is a digit from 0 to 9, the pair of words is a fit; write the 24 digits down. "
        "5. Look at the digits: do they repeat, or spell a date or a coordinate? "
        "6. Do the same on scrambled copies of K4 to see how many fits luck gives."
    ),
    "expected_minutes": 60,
}

import ctypes
import multiprocessing as mp
import os
import random
import subprocess
import sys
import tempfile
import types
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
STD = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KRY = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
SEED = 16404
N_SHUF = 50
N_PLANTS = 8
CHUNKS = 64
CAP = 300000
W = 10
OFFICIAL = list(range(26, 35)) + list(range(64, 75))
EAST = [22, 23, 24, 25]
PLACES = OFFICIAL + EAST
KINDS = ("vig_literal", "variant_literal", "beaufort_literal", "vig_any_start", "beaufort_any_start")
_G = {}

C_SOURCE = r"""
#include <stdint.h>
#define FULL 0x3FFFFFFu
static uint32_t MASK[26];
static int ready = 0;
static void init(int w){
  for(int k=0;k<26;k++){ uint32_t m=0; for(int d=0;d<w;d++){ int o=((k-d)%26+26)%26; m|=1u<<o; } MASK[k]=m; }
  ready=1;
}
static inline int smin_bit(uint32_t m0,uint32_t m1,uint32_t m2,int bit){
  uint32_t b=1u<<bit; if(m0&b) return 0; if(m1&b) return 1; if(m2&b) return 2; return 3;
}
/* A: nA rows of n24 plain-side positions; B: nB rows of n24 cipher-side positions.
   counts[set(2)][kind(5)][smin(3)]; out rows: ia, ib, form, set, m0, m1, m2 */
long long scan(const uint8_t *A,int nA,const uint8_t *B,int nB,int n20,int n24,int w,
               long long *counts,int32_t *out,int cap){
  if(!ready) init(w);
  long long nout=0;
  for(int ia=0;ia<nA;ia++){
    const uint8_t *a=A+(long long)ia*n24;
    for(int ib=0;ib<nB;ib++){
      const uint8_t *b=B+(long long)ib*n24;
      for(int form=0;form<2;form++){
        uint32_t m0=FULL,m1=0,m2=0; int i=0;
        for(;i<n20;i++){
          int k = form==0 ? (b[i]+26-a[i])%26 : (b[i]+a[i])%26;
          uint32_t M=MASK[k], nM=~M;
          m2=(m2&M)|(m1&nM); m1=(m1&M)|(m0&nM); m0&=M;
          if(!(m0|m1|m2)) break;
        }
        if(i<n20) continue;
        for(int set=0;set<2;set++){
          if(set==1){
            for(;i<n24;i++){
              int k = form==0 ? (b[i]+26-a[i])%26 : (b[i]+a[i])%26;
              uint32_t M=MASK[k], nM=~M;
              m2=(m2&M)|(m1&nM); m1=(m1&M)|(m0&nM); m0&=M;
              if(!(m0|m1|m2)) break;
            }
            if(i<n24) break;
          }
          int rec=0;
          int sa = m0?0:(m1?1:2);
          counts[(set*5 + (form==0?3:4))*3 + sa]++;
          if(sa==0 && set==1) rec=1;
          if(form==0){
            int s=smin_bit(m0,m1,m2,0); if(s<3){ counts[(set*5+0)*3+s]++; if(set==1||s==0) rec=1; }
            s=smin_bit(m0,m1,m2,(26-(w-1))%26); if(s<3){ counts[(set*5+1)*3+s]++; if(set==1||s==0) rec=1; }
          } else {
            int s=smin_bit(m0,m1,m2,0); if(s<3){ counts[(set*5+2)*3+s]++; if(set==1||s==0) rec=1; }
          }
          if(rec && nout<cap){
            int32_t *o=out+nout*7; o[0]=ia;o[1]=ib;o[2]=form;o[3]=set;o[4]=(int32_t)m0;o[5]=(int32_t)m1;o[6]=(int32_t)m2; nout++;
          } else if(rec) nout++;
        }
      }
    }
  }
  return nout;
}
"""


def build():
    d = tempfile.mkdtemp(prefix="k4_f164d_")
    src, so = os.path.join(d, "c.c"), os.path.join(d, "c.so")
    open(src, "w").write(C_SOURCE)
    subprocess.run(["cc", "-O3", "-shared", "-fPIC", "-o", so, src], check=True, capture_output=True)
    return so


def alphabets():
    from kryptos.alphabets import keyword_mixed
    ws = [w.strip().upper() for w in (ROOT / "kryptos" / "data" / "words.txt").read_text().split()]
    seen = {STD: "(plain)", KRY: "KRYPTOS"}
    for w in ws:
        if w.isalpha():
            a = keyword_mixed(w)
            if a not in seen:
                seen[a] = w
    alphas = list(seen)
    pos = np.zeros((len(alphas), 26), dtype=np.uint8)
    arr = np.frombuffer("".join(alphas).encode(), dtype=np.uint8).reshape(len(alphas), 26) - 65
    rows = np.repeat(np.arange(len(alphas)), 26)
    pos[rows, arr.ravel()] = np.tile(np.arange(26, dtype=np.uint8), len(alphas))
    return alphas, [seen[a] for a in alphas], pos


def side_drops(vals, letters, n):
    """vals: N x n positions on this side; letters: the other side's letter at each place. Fewest places to
    drop so that, in every group of places sharing the other side's letter, the positions fit in W values."""
    drops = np.zeros(vals.shape[0], dtype=np.int16)
    groups = {}
    for i in range(n):
        groups.setdefault(letters[i], []).append(i)
    for g in groups.values():
        if len(g) < 2:
            continue
        v = vals[:, g].astype(np.int16)
        best = np.zeros(vals.shape[0], dtype=np.int16)
        for j in range(len(g)):
            cnt = (((v - v[:, [j]]) % 26) < W).sum(axis=1)
            best = np.maximum(best, cnt)
        drops += len(g) - best
    return drops


def prepare(text, known):
    """-> A rows (plain side), their alphabet ids, B rows, ids; filtered on the 20 official places."""
    pos = _G["pos"]
    pl = [ord(known[q]) - 65 for q in PLACES]
    cl = [ord(text[q - 1]) - 65 for q in PLACES]
    Aall = pos[:, pl]
    Ball = pos[:, cl]
    n20 = len(OFFICIAL)
    keepA = np.nonzero(side_drops(Aall, cl, n20) <= 2)[0]
    keepB = np.nonzero(side_drops(Ball, pl, n20) <= 2)[0]
    return np.ascontiguousarray(Aall[keepA]), keepA, np.ascontiguousarray(Ball[keepB]), keepB


def _lib():
    if "lib" not in _G:
        lib = ctypes.CDLL(_G["so"])
        lib.scan.restype = ctypes.c_longlong
        lib.scan.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int,
                             ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int]
        _G["lib"] = lib
    return _G["lib"]


def scan(A, B, cap=CAP):
    lib = _lib()
    counts = np.zeros(30, dtype=np.int64)
    out = np.zeros((cap, 7), dtype=np.int32)
    n = lib.scan(A.ctypes.data, A.shape[0], B.ctypes.data, B.shape[0], len(OFFICIAL), len(PLACES), W,
                 counts.ctypes.data, out.ctypes.data, cap)
    return counts, out[:min(n, cap)].copy(), int(n)


def _job(args):
    tid, chunk = args
    if _G.get("cur", (None,))[0] != tid:
        text, known = _G["texts"][tid]
        _G["cur"] = (tid, prepare(text, known))
    A, idA, B, idB = _G["cur"][1]
    lo = A.shape[0] * chunk // CHUNKS
    hi = A.shape[0] * (chunk + 1) // CHUNKS
    counts, out, n = scan(A[lo:hi], B)
    out[:, 0] = idA[lo + out[:, 0]]
    out[:, 1] = idB[out[:, 1]]
    return tid, chunk, counts.tolist(), out.tolist(), n, (A.shape[0], B.shape[0])


def forced(text, known, ia, ib, form, places=PLACES):
    pos = _G["pos"]
    ks = []
    for q in places:
        a = int(pos[ia, ord(known[q]) - 65]); b = int(pos[ib, ord(text[q - 1]) - 65])
        ks.append((b - a) % 26 if form == 0 else (b + a) % 26)
    return ks


def narrowest(ks):
    """smallest number of neighbouring values (cyclic) that holds every k, and its start"""
    best = (27, 0)
    for o in set(ks):
        w = max((k - o) % 26 for k in ks) + 1
        if w < best[0]:
            best = (w, o)
    return best


def period_of(digs, places):
    for L in range(1, 27):
        slot = {}
        if all(slot.setdefault(q % L, d) == d for q, d in zip(places, digs)):
            return L
    return None


NUMBERS = {
    "K2 coordinates 38 57 6.5 77 8 44": "385765778844",
    "K2 coordinates, padded 38 57 06.5 77 08 44": "38570657708 44".replace(" ", ""),
    "pi": "31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679",
    "e": "27182818284590452353602874713526624977572470936999595749669676277240766303535475945713821785251664274",
    "9 November 1989": "9111989", "1989-11-09": "19891109", "November 3 1990": "1131990", "1990-11-03": "19901103",
    "1986 1989": "19861989", "1/7": "142857",
}


def number_match(digs_by_place):
    """the digits at 22-34 as a stretch of a known number, repeated if short; 64-74 must continue it 42 on"""
    run1 = "".join(str(digs_by_place[q]) for q in range(22, 35))
    run2 = "".join(str(digs_by_place[q]) for q in range(64, 75))
    hits = []
    for name, num in NUMBERS.items():
        rep = num * (200 // len(num) + 2) if len(num) < 60 else num
        for rev in (0, 1):
            s = rep[::-1] if rev else rep
            i = s.find(run1)
            while i >= 0:
                if s[i + 42:i + 53] == run2 or len(num) >= 60 and run2 in s:
                    hits.append((name, "reversed" if rev else "forward", i))
                i = s.find(run1, i + 1)
    return hits


def describe(text, known, rows, words):
    """rows: ia, ib, form, set, m0, m1, m2 -> readable fits (24-letter set, no slip) with digits, window, period"""
    out = []
    for ia, ib, form, st, m0, m1, m2 in rows:
        if st != 1 or m0 == 0:
            continue
        ks = forced(text, known, ia, ib, form)
        w, o = narrowest(ks)
        lit = {"vig": bool(m0 & 1), "variant": bool(m0 & (1 << (26 - (W - 1))))} if form == 0 else {"beaufort": bool(m0 & 1)}
        rec = {"plain_word": words[ia], "cipher_word": words[ib], "rule": "Vigenere/variant" if form == 0 else "Beaufort",
               "literal": [k for k, v in lit.items() if v], "narrowest_window": w, "window_start": o,
               "keys_26_34_64_74_22_25": ks}
        digs = None
        if form == 0 and lit.get("vig") or form == 1 and lit.get("beaufort"):
            digs = ks
        elif form == 0 and lit.get("variant"):
            digs = [(-k) % 26 for k in ks]
        if digs is not None:
            byq = dict(zip(PLACES, digs))
            rec["digits_22_34"] = "".join(str(byq[q]) for q in range(22, 35))
            rec["digits_64_74"] = "".join(str(byq[q]) for q in range(64, 75))
            rec["period"] = period_of(digs, PLACES)
            rec["number"] = number_match(byq)
        out.append(rec)
    return out


def make_plant(j, alphas):
    from kryptos.plants import english_plant
    rng = random.Random(SEED + 700 + j)
    pt = english_plant(SEED + 700 + j)
    n = len(alphas)
    ia, ib = rng.randrange(2, n), rng.randrange(2, n)
    if j == 2:
        ib = 0
    if j == 3:
        ia = 0
    rule = ("vig", "vig", "vig", "vig", "variant", "variant", "beaufort", "beaufort")[j]
    P, C = alphas[ia], alphas[ib]
    slip = rng.choice(OFFICIAL) if j in (1, 7) else None
    ct = []
    for i, ch in enumerate(pt):
        k = rng.randrange(10)
        if slip == i + 1:
            k = 15
        a = P.index(ch)
        ct.append(C[(a + k) % 26] if rule == "vig" else C[(a - k) % 26] if rule == "variant" else C[(k - a) % 26])
    return pt, "".join(ct), {"ia": ia, "ib": ib, "rule": rule, "slip_at": slip}


def brute_check(text, known, rng, n=20000, centre=None):
    """the C scan against plain Python on random unfiltered pairs (and literal windows); with a centre, pairs
    of alphabets next to a planted pair in the word list, where fits are common"""
    pos = _G["pos"]
    N = pos.shape[0]
    if centre is None:
        ia = np.array([rng.randrange(N) for _ in range(n)]); ib = np.array([rng.randrange(N) for _ in range(n)])
    else:
        ia = np.array([min(N - 1, max(0, centre[0] + rng.randrange(-40, 41))) for _ in range(n)])
        ib = np.array([min(N - 1, max(0, centre[1] + rng.randrange(-40, 41))) for _ in range(n)])
    pl = [ord(known[q]) - 65 for q in PLACES]; cl = [ord(text[q - 1]) - 65 for q in PLACES]
    A = pos[ia][:, pl].astype(np.int16); B = pos[ib][:, cl].astype(np.int16)
    ref = np.zeros(30, dtype=np.int64)
    for form in (0, 1):
        K = (B - A) % 26 if form == 0 else (B + A) % 26
        for st, m in ((0, len(OFFICIAL)), (1, len(PLACES))):
            miss = np.stack([(((K[:, :m] - o) % 26) >= W).sum(axis=1) for o in range(26)], axis=1)   # n x 26
            sa = miss.min(axis=1)
            for s in (0, 1, 2):
                ref[(st * 5 + (3 if form == 0 else 4)) * 3 + s] += int((sa == s).sum())
                if form == 0:
                    ref[(st * 5 + 0) * 3 + s] += int((miss[:, 0] == s).sum())
                    ref[(st * 5 + 1) * 3 + s] += int((miss[:, 26 - (W - 1)] == s).sum())
                else:
                    ref[(st * 5 + 2) * 3 + s] += int((miss[:, 0] == s).sum())
    got = np.zeros(30, dtype=np.int64)
    for i in range(n):
        c, _, _ = scan(np.ascontiguousarray(pos[ia[i]:ia[i] + 1][:, pl]), np.ascontiguousarray(pos[ib[i]:ib[i] + 1][:, cl]), cap=8)
        got += c
    return bool((ref == got).all()), int(ref.sum())


def run(ctx):
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    known = dict(ctx.KNOWN)
    alphas, words, pos = alphabets()
    _G["pos"] = pos
    _G["so"] = build()
    rng = random.Random(SEED)
    texts = {"K4": (ctx.K4, known)}
    for s in range(N_SHUF):
        sh = list(ctx.K4); random.Random(SEED * 100 + s).shuffle(sh)
        texts[f"shuffle{s:02d}"] = ("".join(sh), known)
    plant_info = {}
    for j in range(N_PLANTS):
        pt, ct, info = make_plant(j, alphas)
        texts[f"plant{j}"] = (ct, {q: pt[q - 1] for q in PLACES})
        plant_info[f"plant{j}"] = info
    _G["texts"] = texts
    ok_brute, n_brute = brute_check(ctx.K4, known, rng)
    assert ok_brute, "C scan disagrees with the Python reference"
    for name in ("plant0", "plant4", "plant6"):
        ok2, n2 = brute_check(*texts[name], rng, n=6000, centre=(plant_info[name]["ia"], plant_info[name]["ib"]))
        assert ok2 and n2 > 0, name
        n_brute += n2
    # the filter must not drop a planted alphabet
    for name, info in plant_info.items():
        A, idA, B, idB = prepare(*texts[name])
        assert info["ia"] in set(idA.tolist()) and info["ib"] in set(idB.tolist()), name

    saved = getattr(ctx, "saved", {}) or {}
    res = dict(saved)
    order = ["K4"] + [f"plant{j}" for j in range(N_PLANTS)] + [f"shuffle{s:02d}" for s in range(N_SHUF)]
    todo = [t for t in order if t not in res]
    ctx.progress(len(res), len(order), "texts")
    Wk = int(os.environ.get("K4_WORKERS", 8))
    part = {}
    with mp.get_context("fork").Pool(Wk) as pool:
        jobs = [(t, c) for t in todo for c in range(CHUNKS)]
        for tid, chunk, counts, out, n, sizes in pool.imap(_job, jobs, chunksize=1):
            p = part.setdefault(tid, {"counts": np.zeros(30, dtype=np.int64), "rows": [], "n": 0, "done": 0, "sizes": sizes})
            p["counts"] += np.array(counts); p["rows"].extend(out); p["n"] += n; p["done"] += 1
            if p["done"] == CHUNKS:
                text, kn = texts[tid]
                rows = p["rows"]
                anyfit = [r for r in rows if r[3] == 1 and r[4] != 0]
                widths = [narrowest(forced(text, kn, r[0], r[1], r[2]))[0] for r in anyfit]
                val = {"counts": p["counts"].tolist(), "listed": p["n"], "capped": p["n"] > len(rows), "sizes": list(p["sizes"]),
                       "min_window": min(widths) if widths else None,
                       "window_hist": {str(w): widths.count(w) for w in sorted(set(widths))}}
                if not tid.startswith("shuffle"):
                    val["rows"] = rows if tid.startswith("plant") else [r for r in rows if r[3] == 1]
                res[tid] = val
                ctx.save(tid, val)
                del part[tid]
                ctx.progress(len(res), len(order), "texts")

    def cell(v, st, kind, s):
        """fits with at most s slips"""
        base = (st * 5 + KINDS.index(kind)) * 3
        return sum(v["counts"][base:base + s + 1])

    cells = {}
    shuf = [res[f"shuffle{s:02d}"] for s in range(N_SHUF)]
    above_all = []
    for st, sname in ((1, "24 letters"), (0, "20 official")):
        for kind in KINDS:
            for s in (0, 1, 2):
                k4 = cell(res["K4"], st, kind, s)
                sv = sorted(cell(v, st, kind, s) for v in shuf)
                ge = sum(1 for x in sv if x >= k4)
                name = f"{sname} | {kind} | up to {s} slips"
                cells[name] = {"K4": k4, "shuffles_min_median_max": [sv[0], sv[len(sv) // 2], sv[-1]], "shuffles_at_or_above": ge,
                               "p": round((1 + ge) / (N_SHUF + 1), 3)}
                if ge == 0:
                    above_all.append(name)
    # stand-in null for 'cells above all': each shuffle against the other 29
    null_counts = []
    for i, v in enumerate(shuf):
        c = 0
        for st in (0, 1):
            for kind in KINDS:
                for s in (0, 1, 2):
                    mine = cell(v, st, kind, s)
                    if all(cell(o, st, kind, s) < mine for j, o in enumerate(shuf) if j != i):
                        c += 1
        null_counts.append(c)
    k4fits = describe(ctx.K4, known, res["K4"]["rows"], words)
    k4fits.sort(key=lambda r: (r["narrowest_window"], not r["literal"]))
    literal = [r for r in k4fits if r["literal"]]
    periodic = [r for r in literal if r.get("period") and r["period"] <= 20]
    numbered = [r for r in literal if r.get("number")]
    # literal fits with 1-2 slips on K4, by table, for the record
    plants = []
    for j in range(N_PLANTS):
        name = f"plant{j}"; info = plant_info[name]; v = res[name]
        form = 1 if info["rule"] == "beaufort" else 0
        bit = {"vig": 0, "variant": 26 - (W - 1), "beaufort": 0}[info["rule"]]
        found = None
        for r in v["rows"]:
            if r[0] == info["ia"] and r[1] == info["ib"] and r[2] == form:
                m = [r[4], r[5], r[6]]
                s = next((i for i in range(3) if m[i] & (1 << bit)), None)
                if s is not None and (found is None or r[3] == 1):
                    found = {"set": "24" if r[3] == 1 else "20", "slips": s}
        kind = {"vig": "vig_literal", "variant": "variant_literal", "beaufort": "beaufort_literal"}[info["rule"]]
        plants.append({"plain_word": words[info["ia"]], "cipher_word": words[info["ib"]], "rule": info["rule"], "slip_at": info["slip_at"],
                       "found": found, "ok": bool(found and found["slips"] == (1 if info["slip_at"] else 0)),
                       "literal_fits_no_slip_24": cell(v, 1, kind, 0), "min_window": v["min_window"], "capped": v["capped"]})
    n_ok = sum(1 for p in plants if p["ok"])
    minw = sorted(v["min_window"] or 27 for v in shuf)
    k4w = res["K4"]["min_window"] or 27
    return {
        "candidates": [],
        "bounds": {
            "item": "F16.4d", "alphabets": len(alphas), "pairs_per_text": len(alphas) ** 2, "rules": "Vigenere/variant (k = C(c) - P(p)), Beaufort (k = C(c) + P(p))",
            "window": W, "slips": "0-2", "after_side_filter": {t: res[t]["sizes"] for t in ("K4", "shuffle00", "plant0")},
            "self_check": f"C scan equals the Python reference on 20,000 random pairs and 18,000 pairs next to three planted pairs ({n_brute} counted fits)",
            "cells": cells, "cells_K4_above_all_shuffles": above_all, "cells_looked_at": len(cells),
            "stand_in_null_cells_above_all_others": sorted(null_counts),
            "K4_fits_no_slip_any_start": len(k4fits), "K4_literal_fits_no_slip": len(literal),
            "K4_literal_periodic": periodic, "K4_literal_known_number": numbered,
            "K4_min_window": k4w, "shuffles_min_window_sorted": minw, "shuffles_min_window_at_or_below_K4": sum(1 for x in minw if x <= k4w),
            "K4_window_hist": res["K4"]["window_hist"],
            "K4_fits_narrowest_first": k4fits[:60], "K4_literal_fits": literal[:200],
            "K4_capped": res["K4"]["capped"], "shuffles_capped": sum(1 for v in shuf if v["capped"]),
            "plants": plants, "plants_found": f"{n_ok} of {N_PLANTS}",
            "controls": f"{N_SHUF} shuffles of K4, known letters kept in place, the same scan", "exhaustive": True,
            "not_covered": "grid-mixed alphabets (F16.3); windows wider than ten; a key that leaves 3 or more known places outside; the 73 unknown letters are not read (ten choices per letter)",
            "aws_cost_estimate_dollars": 1.0,
        },
        "notes": (f"K4: {len(literal)} literal no-slip fits ({len(periodic)} periodic, {len(numbered)} a known number), {len(k4fits)} with any start; "
                  f"narrowest window K4 {k4w}, shuffles {minw[0]}-{minw[-1]}; cells above all {N_SHUF} shuffles: {len(above_all)} of {len(cells)} "
                  f"(a shuffle against the others: {sorted(null_counts)[len(null_counts) // 2]} median, {max(null_counts)} max); plants {n_ok}/{N_PLANTS}"),
    }


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    lines = ["message alphabet: plain A-Z; carved alphabet: plain A-Z; rule: steps from the known letter to the carved one",
             "", "place known carved steps  a digit 0-9?"]
    for q in sorted(ctx.KNOWN):
        k = (STD.index(ctx.K4[q - 1]) - STD.index(ctx.KNOWN[q])) % 26
        lines.append(f"{q:>5} {ctx.KNOWN[q]:>5} {ctx.K4[q - 1]:>6} {k:>5}  {'yes' if k <= 9 else 'no'}")
    return "\n".join(lines)
