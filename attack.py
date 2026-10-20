"""Experiment 0211. See program.md for the contract."""

EXPERIMENT = {
    "slug": "running-keys-through-the-shifts-and-moves-with-slips",
    "title": "A1.3, with moves: 0117's running keys from the sculpture's texts and Carter, plus any constant shift of the table, with or without every type-1 move, either order, allowing up to three of the 24 known letters to be slips, exact, against scrambled copies, with planted slipped messages",
    "family": "1-keyed-periodic",
    "parent": "0117-running-keys-through-all-the-shifts",
    "changed": (
        "A1.3 (Stage 2, step 2, issue #76), the part 0210 left out: 0117 required all 24 known letters (change then move: "
        "the 23 key differences matched by hash; move then change: a pair index filtered check by check, deepest 8 of 24). "
        "Here both orders allow up to 3 failed checks: change then move by a pigeonhole index (4 blocks of 6 known places; "
        "3 slips leave one block whole, whose 5 key differences are looked up), move then change by 4 disjoint pairs of "
        "known places (3 slips leave one pair whole, looked up by its key difference at its gap). Both compiled; same "
        "sources, numberings, 12 conventions and 0117's route library unchanged; K4 against 10 scrambled copies; two "
        "planted messages (one per order) with 3 and 2 slips."
    ),
    "hypothesis_expert": (
        "C2(b) (Sanborn 2003: 'surprised that no one had tried recovering the original matrix and running it through all "
        "the possible shifts'), C6(a) (keys concealed at the sculpture), C1(a) (a matrix stage), with A1 "
        "(knowledge/12-assumptions.md) and C27(a) (the PALIMPCEST slip). Model as 0117: c = E(p, y[o + i] + s) for a key text "
        "y numbered on the standard or KRYPTOS alphabet, offset o, constant s 0-25, E one of 12 conventions (Vigenere, "
        "Beaufort, variant; plain and cipher alphabets standard or KRYPTOS); with a type-1 move before the table (move then "
        "change: key aligned to carved places) or after it (change then move: key aligned to message places); key texts "
        "the carved tableau (rows, rows with index, columns), the Morse (carved, reversed order), the four ciphertexts, "
        "K1-K3 plaintexts, Sanborn's 1989 letter, the 1991 dedication texts, the 2025 open letter, forward and backward, "
        "every cyclic offset; Carter's book in the change-then-move order only (as 0117). A slip at known place q makes "
        "its equation fail; settings with at most 3 failures are counted, K4 against each copy. Chance of any setting "
        "with 3 or fewer slips on a text: about 10^-15 (change then move, 4 x 10^11 trials) and 10^-17 (move then change), "
        "so the 24 checks decide at k <= 3."
    ),
    "hypothesis_eli5": (
        "Experiment 117 took the sculpture's own texts as a long key, let the whole table slide by any of 26 places, and "
        "tried it with and without the grid scrambles of experiments 80-83. Nothing gave the 24 known letters. Here the "
        "same search allows Sanborn up to three slips at those 24 places, on the carving and on scrambled copies, with two "
        "messages of our own hidden the same way, slips included, to check the search finds them."
    ),
    "prediction": (
        "No setting with 3 or fewer slips on K4 or on any copy, in either order. Both planted messages are found at their "
        "own route, convention, key text, offset and shift, with exactly their slips. Zero candidates on K4."
    ),
    "method": (
        "1. Build 0117's key texts (both numberings) and route library. 2. Change then move: index every offset of every "
        "key text by the 5 key differences inside each of 4 blocks of 6 known places; for each route, convention and text, "
        "compute the key each known place needs and look up its block differences; check every offset found on all 24 "
        "places with the shift its clean block gives. 3. Move then change: for 4 disjoint pairs of known places, the moved "
        "places' gap and needed key difference are looked up in a per-gap index of each key text; check every offset found "
        "on all 24. 4. Keep settings with at most 3 failures. 5. K4, 10 copies, two plants with 5 copies each."
    ),
    "walkthrough": (
        "1. Take the four ciphertexts as the key text, from some offset, and the KRYPTOS table with Vigenere. "
        "2. At each known place, the key needed is the carved letter minus the known letter, and the key text offers its own letter. "
        "3. With a constant shift, needed minus offered must come out the same at every known place. "
        "4. Allow up to 3 places where it does not: those would be Sanborn's slips. "
        "5. Slide the offset, and repeat for every text, rule, and every grid scramble before or after the table."
    ),
}

import ctypes
import json
import math
import multiprocessing as mp
import os
import random
import subprocess
import sys
import tempfile
import types
from pathlib import Path
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY, load_k1, load_k2, load_k3
from kryptos.ciphers import tableau_rows, columnar_transposition_encrypt
from kryptos.alphabets import numeric_order

N = 97
N_COPIES = 10
N_PLANT_COPIES = 5
KMAX = 3
ROOT = Path(__file__).resolve().parent
if not (ROOT / "knowledge").exists():
    ROOT = Path.cwd()
AL = {"std": STD, "kry": KRY}
IDX = {k: {c: i for i, c in enumerate(a)} for k, a in AL.items()}
EXTRA = ["EGYPT", "CAIRO", "LUXOR", "WALL", "NOVEMBER", "MESSAGE", "DELIVER", "DELIVERING", "TRANSMIT"]
MODE_N = {"vig": 0, "beau": 1, "varb": 2}


def letters(s):
    return "".join(c for c in s.upper() if "A" <= c <= "Z")


def sources():
    site = json.loads((ROOT / "data" / "site_texts.json").read_text())
    rows = tableau_rows(carved=True)
    src = {}
    src["tableau rows"] = "".join(rows)
    src["tableau rows with index column"] = "".join(STD[i] + r for i, r in enumerate(rows))
    width = max(len(r) for r in rows)
    src["tableau columns"] = "".join(r[c] for c in range(width) for r in rows if c < len(r))
    morse = [letters(m) for m in site["morse"]]
    src["morse as carved"] = "".join(morse)
    src["morse reversed order"] = "".join(reversed(morse))
    k1, k2, k3 = load_k1(), load_k2(), load_k3()
    k4 = letters((ROOT / "data" / "k4.txt").read_text())
    src["panel ciphertexts K1-K4"] = letters(k1["ciphertext"]) + letters(k2["ciphertext_as_carved"]) + letters(k3["ciphertext"]) + k4
    src["K1-K3 plaintexts"] = letters(k1["plaintext"]) + letters(k2["plaintext_as_carved"]) + letters(k3["plaintext"])
    t = (ROOT / "knowledge" / "sources" / "sanborn-1989-letter-and-webster-1990-cryptogram.txt").read_text(errors="ignore")
    a = t.index("Dear Agency Employees"); b = t.index("Sincerely, Jim Sanborn") + len("Sincerely, Jim Sanborn")
    c = t.index("Remarks by William H. Webster")
    o = (ROOT / "knowledge" / "sources" / "openletter-2025.txt").read_text(errors="ignore")
    oa = o.index("Dear Kryptos fans"); ob = o.index("Jim Sanborn", o.index("All the best")) + len("Jim Sanborn")
    src["Sanborn 1989 letter"] = letters(t[a:b])
    src["1991 dedication texts"] = letters(t[c:])
    src["2025 open letter"] = letters(o[oa:ob])
    out = {}
    for name, s in src.items():
        out[name + " fwd"] = s
        out[name + " bwd"] = s[::-1]
    carter = letters((ROOT / "knowledge" / "sources" / "carter-1923-tomb-of-tutankhamen-vol1.txt").read_text(errors="ignore"))
    big = {"Carter vol 1 fwd": carter, "Carter vol 1 bwd": carter[::-1]}
    return out, big


def perm_of(fn):
    idx = "".join(chr(0x100 + i) for i in range(N))
    return [ord(ch) - 0x100 for ch in fn(idx)]


def rot_cw(s, w):
    rows = [s[i:i + w] for i in range(0, len(s), w)]
    return "".join(r[c] for c in range(w) for r in reversed(rows) if c < len(r))


def rot_ccw(s, w):
    rows = [s[i:i + w] for i in range(0, len(s), w)]
    return "".join(r[c] for c in reversed(range(w)) for r in rows if c < len(r))


def keyword_sequence(word):
    rank = numeric_order(word)
    return sorted(range(len(rank)), key=lambda c: rank[c])


def full_sequence(word):
    w = [c for c in word.upper() if c.isalpha()]
    return sorted(range(len(w)), key=lambda c: (w[c], c))


def route_fns(vocab):
    for b in range(1, N):
        for a in range(N):
            def f(s, a=a, b=b):
                out = [""] * N
                for i in range(N):
                    out[(a + b * i) % N] = s[i]
                return "".join(out)
            yield f"K3 rule a={a} b={b}", f
    for w in range(2, N):
        yield f"turn cw {w}", (lambda s, w=w: rot_cw(s, w))
        yield f"turn ccw {w}", (lambda s, w=w: rot_ccw(s, w))
        yield f"columnar {w}", (lambda s, o=list(range(w)): columnar_transposition_encrypt(s, o))
        yield f"columnar rtl {w}", (lambda s, o=list(range(w))[::-1]: columnar_transposition_encrypt(s, o))
    for w1 in range(2, N):
        for w2 in range(2, N):
            yield f"two turns cw {w1},{w2}", (lambda s, a=w1, b=w2: rot_cw(rot_cw(s, a), b))
    words = sorted({w for w in vocab if 2 <= len(w) <= 30} | set(EXTRA))
    for word in words:
        for how, seq in (("repeats dropped", keyword_sequence(word)), ("full word", full_sequence(word))):
            if len(seq) >= 2:
                yield f"keyword {word} ({how})", (lambda s, o=list(seq): columnar_transposition_encrypt(s, o))


def route_library(vocab):
    """Distinct 'where' maps (where[i] = place in the moved text of letter i), forward and inverse."""
    seen, lib = set(), []
    for name, f in route_fns(vocab):
        sigma = perm_of(f)                    # moved[j] = orig[sigma[j]]
        fwd = [0] * N
        for j, i in enumerate(sigma):
            fwd[i] = j
        for tag, w in ((name, fwd), (name + " inverse", sigma)):
            t = tuple(w)
            if t not in seen:
                seen.add(t); lib.append((tag, t))
    return lib


def enc(mode, p, k):
    return {"vig": (p + k) % 26, "beau": (k - p) % 26, "varb": (p - k) % 26}[mode]


def key_for(mode, p, c):
    """k with enc(mode, p, k) = c."""
    return {"vig": (c - p) % 26, "beau": (c + p) % 26, "varb": (p - c) % 26}[mode]


def dec(mode, c, k):
    return {"vig": (c - k) % 26, "beau": (k - c) % 26, "varb": (c + k) % 26}[mode]


CONVS = [(m, pa, ca) for m in ("vig", "beau", "varb") for pa in ("std", "kry") for ca in ("std", "kry")]


C_SRC = r"""
#include <stdlib.h>
#include <string.h>
static int md(int x){ x%=26; return x<0?x+26:x; }
static int keyfor(int m,int p,int c){ return m==0?md(c-p):(m==1?md(c+p):md(p-c)); }

/* key texts: concatenated y (0-25), starts, lens. */
static int NF; static const int *Y; static const long *ST; static const int *LN;
void set_keys(int nf, const int *y, const long *st, const int *ln){ NF=nf; Y=y; ST=st; LN=ln; }

/* change then move: index of (code, f, o) for the 4 blocks of 6 known places (positions kp, fixed). */
static long *IX[4]; static long NIX; static int KP[24];
static int cmp(const void*a,const void*b){ long x=*(const long*)a,y=*(const long*)b; return x<y?-1:x>y; }
static long code_at(int f,long o,int b){ const int *y=Y+ST[f]; int L=LN[f]; long c=0; int y0=y[(o+KP[6*b])%L];
  for(int j=1;j<6;j++){ c=c*26+md(y[(o+KP[6*b+j])%L]-y0);} return c; }
void build_cm(int nfcm, const int *kp){ /* only the first nfcm key texts (all, incl. Carter) */
  memcpy(KP,kp,24*sizeof(int)); NIX=0; for(int f=0;f<nfcm;f++) NIX+=LN[f];
  for(int b=0;b<4;b++){ IX[b]=(long*)malloc(sizeof(long)*NIX); long n=0;
    for(int f=0;f<nfcm;f++) for(long o=0;o<LN[f];o++){ long c=code_at(f,o,b); IX[b][n++]=(c<<26)|((long)f<<20)|o; }
    qsort(IX[b],NIX,sizeof(long),cmp); } }

/* move then change: per key text, per gap g in -96..96, offsets u sorted by d = y[u+g]-y[u]. */
static int NFMC; static int **GI; static int **GS; /* GI[f*193+g+96] offsets, GS[...] 27 starts */
void build_mc(int nfmc){ NFMC=nfmc; GI=(int**)malloc(sizeof(int*)*nfmc*193); GS=(int**)malloc(sizeof(int*)*nfmc*193);
  for(int f=0;f<nfmc;f++){ const int *y=Y+ST[f]; int L=LN[f];
    for(int g=-96;g<=96;g++){ int *cnt=(int*)calloc(27,sizeof(int)); int *off=(int*)malloc(sizeof(int)*L);
      for(int u=0;u<L;u++){ int d=md(y[((u+g)%L+L)%L]-y[u]); cnt[d+1]++; }
      for(int d=0;d<26;d++) cnt[d+1]+=cnt[d];
      int *pos=(int*)malloc(sizeof(int)*27); memcpy(pos,cnt,27*sizeof(int));
      for(int u=0;u<L;u++){ int d=md(y[((u+g)%L+L)%L]-y[u]); off[pos[d]++]=u; }
      free(pos); GI[f*193+g+96]=off; GS[f*193+g+96]=cnt; } } }

/* one text against every route and convention.
   text[97]; known[24] letters; kpos[24] 0-based places; routes nr x 97 (where[i]);
   conv 12 x (mode, pa idx table 26, ca idx table 26) as convm[12], pat[12*26], cat[12*26];
   counts out[2*4]; hits out up to maxh x 8 (order, route, conv, f, o, s, mism, unused). */
long run_text(const int *text,const int *known,const int *kpos,int nr,const int *routes,
              const int *convm,const int *pat,const int *cat,int nfmc,
              long *counts,int maxh,long *hits){
  long nh=0; int T[24], kp[24];
  for(int r=0;r<nr;r++){ const int *w=routes+97*r;
    for(int c=0;c<12;c++){ int m=convm[c];
      for(int e=0;e<24;e++) T[e]=keyfor(m,pat[c*26+known[e]],cat[c*26+text[w[kpos[e]]]]);
      /* change then move: key at message places */
      long seen_n=0;
      for(int b=0;b<4;b++){ long code=0; for(int j=1;j<6;j++) code=code*26+md(T[6*b+j]-T[6*b]);
        long lo=0,hi=NIX; long key=code<<26; while(lo<hi){ long mid=(lo+hi)/2; if(IX[b][mid]<key) lo=mid+1; else hi=mid; }
        for(long i=lo;i<NIX && (IX[b][i]>>26)==code;i++){ int f=(IX[b][i]>>20)&63; long o=IX[b][i]&((1<<20)-1);
          int dup=0; for(int b2=0;b2<b;b2++) if(code_at(f,o,b2)==({long cc=0; for(int j=1;j<6;j++) cc=cc*26+md(T[6*b2+j]-T[6*b2]); cc;})){dup=1;break;}
          if(dup) continue;
          const int *y=Y+ST[f]; int L=LN[f]; int s=md(T[6*b]-y[(o+KP[6*b])%L]); int mm=0;
          for(int e=0;e<24 && mm<=3;e++) if(md(y[(o+KP[e])%L]+s)!=T[e]) mm++;
          if(mm<=3){ counts[0*4+mm]++; if(nh<maxh){ long *h=hits+8*nh; h[0]=0;h[1]=r;h[2]=c;h[3]=f;h[4]=o;h[5]=s;h[6]=mm; nh++; } } } }
      /* move then change: key at carved places */
      for(int e=0;e<24;e++) kp[e]=w[kpos[e]];
      for(int f=0;f<nfmc;f++){ const int *y=Y+ST[f]; int L=LN[f];
        for(int pr=0;pr<4;pr++){ int e0=2*pr,e1=2*pr+1; int g=kp[e1]-kp[e0]; int d=md(T[e1]-T[e0]);
          const int *off=GI[f*193+g+96]; const int *cs=GS[f*193+g+96];
          for(int i=cs[d];i<cs[d+1];i++){ int u=off[i]; long o=((u-kp[e0])%L+L)%L; int s=md(T[e0]-y[u]);
            int dup=0; for(int p2=0;p2<pr;p2++){ int a=2*p2,bb=2*p2+1;
              if(md(y[(o+kp[bb])%L]-y[(o+kp[a])%L])==md(T[bb]-T[a])){dup=1;break;} }
            if(dup) continue;
            int mm=0; for(int e=0;e<24 && mm<=3;e++) if(md(y[(o+kp[e])%L]+s)!=T[e]) mm++;
            if(mm<=3){ counts[1*4+mm]++; if(nh<maxh){ long *h=hits+8*nh; h[0]=1;h[1]=r;h[2]=c;h[3]=f;h[4]=o;h[5]=s;h[6]=mm; nh++; } } } } } } }
  return nh; }
"""

_LIB = None
_STATE = {}


def lib():
    global _LIB
    if _LIB is None:
        d = tempfile.mkdtemp(prefix="k4_rk_")
        src, so = os.path.join(d, "rk.c"), os.path.join(d, "rk.so")
        Path(src).write_text(C_SRC)
        subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", so, src], check=True, capture_output=True)
        _LIB = ctypes.CDLL(so)
        _LIB.run_text.restype = ctypes.c_long
    return _LIB


def I(a):
    return (ctypes.c_int * len(a))(*a)


def setup_state(keytexts_cm, n_mc, lib_routes, known):
    """keytexts_cm: list of (name, numbers); the first n_mc are the move-then-change texts (no Carter)."""
    L = lib()
    y = []; st = []; ln = []
    for _, v in keytexts_cm:
        st.append(len(y)); ln.append(len(v)); y.extend(v)
    _STATE["y"] = I(y); _STATE["st"] = (ctypes.c_long * len(st))(*st); _STATE["ln"] = I(ln)
    L.set_keys(len(ln), _STATE["y"], _STATE["st"], _STATE["ln"])
    kpos = [q - 1 for q in sorted(known)]
    _STATE["kpos"] = I(kpos)
    L.build_cm(len(ln), _STATE["kpos"])
    L.build_mc(n_mc)
    routes = []
    for _, w in lib_routes:
        routes.extend(w)
    _STATE["routes"] = I(routes); _STATE["nr"] = len(lib_routes); _STATE["nmc"] = n_mc
    _STATE["known"] = I([ord(known[q]) - 65 for q in sorted(known)])
    convm, pat, cat = [], [], []
    for mode, pa, ca in CONVS:
        convm.append(MODE_N[mode]); pat.extend(IDX[pa][c] for c in STD); cat.extend(IDX[ca][c] for c in STD)
    _STATE["convm"], _STATE["pat"], _STATE["cat"] = I(convm), I(pat), I(cat)


def one_text(text):
    L = lib()
    counts = (ctypes.c_long * 8)()
    maxh = 200
    hits = (ctypes.c_long * (8 * maxh))()
    nh = L.run_text(I([ord(c) - 65 for c in text]), _STATE["known"], _STATE["kpos"], _STATE["nr"], _STATE["routes"],
                    _STATE["convm"], _STATE["pat"], _STATE["cat"], _STATE["nmc"], counts, maxh, hits)
    return list(counts), [tuple(hits[8 * i + j] for j in range(7)) for i in range(nh)]


def shuffled(text, seed):
    l_ = list(text)
    random.Random(seed).shuffle(l_)
    return "".join(l_)


def apply(order, text_letters, where, y, o, s, conv):
    """Encrypt 97 plaintext letters: order 0 change then move, 1 move then change. Returns the carved text."""
    mode, pa, ca = conv
    P, C = IDX[pa], AL[ca]
    L = len(y)
    if order == 0:
        ch = [C[enc(mode, P[p], (y[(o + i) % L] + s) % 26)] for i, p in enumerate(text_letters)]
        out = [""] * N
        for i in range(N):
            out[where[i]] = ch[i]
        return "".join(out)
    moved = [""] * N
    for i in range(N):
        moved[where[i]] = text_letters[i]
    return "".join(C[enc(mode, P[p], (y[(o + j) % L] + s) % 26)] for j, p in enumerate(moved))


def encrypt(plaintext, key):
    """key: order (0 change then move, 1 move then change), where (97 places), key text numbers y, offset, shift,
    convention (mode, pa, ca), slips [[place, carved letter]]."""
    out = list(apply(key["order"], plaintext, key["where"], key["y"], key["offset"], key["shift"], tuple(key["conv"])))
    for q, ch in key.get("slips", []):
        out[q - 1] = ch
    return "".join(out)


PLANTS = [  # (seed, order, route name prefix, key text, numbering, conv, slips)
    (2111, 0, "keyword KRYPTOS (repeats dropped)", "Carter vol 1 fwd", "kry", ("vig", "kry", "kry"), 3),
    (2112, 1, "turn cw 9", "panel ciphertexts K1-K4 fwd", "std", ("beau", "std", "kry"), 2),
]


def run(ctx):
    known = ctx.KNOWN
    lib_routes = route_library(ctx.vocabulary)
    srcs, big = sources()
    mc_texts = [(f"{n} [{ka}]", [IDX[ka][c] for c in s]) for n, s in srcs.items() for ka in ("std", "kry")]
    cm_extra = [(f"{n} [{ka}]", [IDX[ka][c] for c in s]) for n, s in big.items() for ka in ("std", "kry")]
    keytexts = mc_texts + cm_extra
    names = [n for n, _ in keytexts]
    setup_state(keytexts, len(mc_texts), lib_routes, known)
    route_idx = {name: i for i, (name, _) in enumerate(lib_routes)}
    # plants
    plants = []
    for seed, order, rname, kt, ka, conv, k in PLANTS:
        from kryptos.plants import english_plant
        rng = random.Random(seed)
        pt = english_plant(seed)
        r = route_idx[rname]
        f = names.index(f"{kt} [{ka}]")
        y = keytexts[f][1]
        o, s = rng.randrange(len(y)), rng.randrange(26)
        ct = list(apply(order, pt, lib_routes[r][1], y, o, s, conv))
        places = sorted(rng.sample(sorted(known), k))
        where = lib_routes[r][1]
        for q in places:  # the known letter at message place q is carved at where[q - 1] in either order
            j = where[q - 1]
            ct[j] = rng.choice([c for c in STD if c != ct[j]])
        plants.append({"seed": seed, "order": order, "route": rname, "r": r, "keytext": f"{kt} [{ka}]", "f": f, "offset": o,
                       "shift": s, "conv": "/".join(conv), "c": CONVS.index(conv), "k": k, "slips": places, "ct": "".join(ct), "pt": pt})
    texts = []
    for p in plants:  # each plant, then its own copies
        texts += [p["ct"]] + [shuffled(p["ct"], p["seed"] * 100 + i) for i in range(N_PLANT_COPIES)]
    n_pl = len(texts)
    texts += [ctx.K4] + [shuffled(ctx.K4, 2120 + i) for i in range(N_COPIES)]
    if getattr(sys.modules.get(__name__), "one_text", None) is not one_text:
        mod = types.ModuleType(__name__); mod.__dict__.update(globals()); sys.modules[__name__] = mod
    out = [None] * len(texts)
    with mp.get_context("fork").Pool(8) as pool:
        it = pool.imap(one_text, texts)
        for i in range(len(texts)):
            out[i] = it.next()
            if ctx.time_left() < 60:
                pool.terminate()
                break
    plant_out = []
    for j, p in enumerate(plants):
        res = out[j * (N_PLANT_COPIES + 1)]
        own = [out[j * (N_PLANT_COPIES + 1) + 1 + i] for i in range(N_PLANT_COPIES)]
        if res is None or any(x is None for x in own):
            plant_out.append({"seed": p["seed"], "found": False, "note": "not run"}); continue
        hit = [h for h in res[1] if h[0] == p["order"] and h[2] == p["c"] and h[3] == p["f"] and h[4] == p["offset"] and h[5] == p["shift"]]
        hit_route = [h for h in hit if h[1] == p["r"]]
        plant_out.append({"seed": p["seed"], "order": ["change then move", "move then change"][p["order"]], "route": p["route"],
                          "keytext": p["keytext"], "offset": p["offset"], "shift": p["shift"], "conv": p["conv"], "k": p["k"],
                          "slips": p["slips"], "settings_by_order_and_slips": res[0],
                          "planted_found": bool(hit_route), "planted_mismatches": hit_route[0][6] if hit_route else None,
                          "same_reading_routes": len(hit), "own_copies_settings": [sum(x[0]) for x in own],
                          "found": bool(hit_route and hit_route[0][6] == p["k"] and all(sum(x[0]) == 0 for x in own))})
    k4 = out[n_pl]
    copies = [x for x in out[n_pl + 1:] if x is not None]
    # readings of K4's settings (if any) to the judge
    k4_hits = []
    cands = []
    if k4 and k4[1]:
        reads = []
        for h in k4[1]:
            order, r, c, f, o, s, mm = h
            where = lib_routes[r][1]; y = keytexts[f][1]; mode, pa, ca = CONVS[c]
            P, C = AL[pa], IDX[ca]
            Lk = len(y)
            if order == 0:
                inv = [0] * N
                for i in range(N):
                    inv[where[i]] = i
                pt = "".join(P[dec(mode, C[ctx.K4[where[i]]], (y[(o + i) % Lk] + s) % 26)] for i in range(N))
            else:
                moved = [P[dec(mode, C[ctx.K4[j]], (y[(o + j) % Lk] + s) % 26)] for j in range(N)]
                pt = "".join(moved[where[i]] for i in range(N))
            reads.append(pt)
            k4_hits.append({"order": order, "route": lib_routes[r][0], "conv": "/".join(CONVS[c]), "keytext": names[f], "offset": o, "shift": s, "slips": mm, "reading": pt})
        v = ctx.judge(sorted(set(reads)))
        vd = dict(zip(sorted(set(reads)), v))
        for kh in k4_hits:
            kh["judge"] = vd[kh["reading"]]["score"]
    tot_cm = sum(len(v) for _, v in keytexts)
    tot_mc = sum(len(v) for _, v in mc_texts)
    trials_cm = len(lib_routes) * len(CONVS) * 26 * tot_cm
    trials_mc = len(lib_routes) * len(CONVS) * 26 * tot_mc
    return {
        "candidates": cands,
        "bounds": {
            "family": "0117's running keys plus a constant shift, with or without a type-1 move, either order, 0-3 known letters slipped (A1.3)",
            "routes_distinct": len(lib_routes), "conventions": len(CONVS), "shifts": 26,
            "key_texts": {"change_then_move": len(keytexts), "move_then_change": len(mc_texts), "letters_cm": tot_cm, "letters_mc": tot_mc},
            "trials": {"change_then_move": trials_cm, "move_then_change": trials_mc},
            "chance_settings_with_3_or_fewer_slips": {"change_then_move": f"{trials_cm / 26 * math.comb(24, 3) * 26 ** -20:.1e}",
                                                       "move_then_change": f"{trials_mc / 26 * math.comb(24, 3) * 26 ** -20:.1e}"},
            "method": "change then move: 4 blocks of 6 known places, key differences indexed; move then change: 4 disjoint pairs, per-gap difference index; compiled; every hit checked on all 24",
            "k4_settings_by_order_and_slips": k4[0] if k4 else None,
            "copies_settings_by_order_and_slips": [x[0] for x in copies], "copies_done": len(copies),
            "k4_hits": k4_hits[:20],
            "plants": plant_out,
            "slip_cost_bits": {k: round(4.7 * k + math.log2(math.comb(24, k)), 1) for k in (1, 2, 3)},
            "controls": f"{N_COPIES} shuffled copies (seeds 2120-2129); each plant against {N_PLANT_COPIES} shuffles of its own ciphertext",
            "exhaustive": "yes",
        },
        "notes": (f"K4 settings with <= 3 slips (change-then-move 0-3, move-then-change 0-3): {k4[0] if k4 else None}; copies "
                  f"{[sum(x[0]) for x in copies]}; plants found {[p['found'] for p in plant_out]}"),
    }


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    srcs, _ = sources()
    s = srcs["panel ciphertexts K1-K4 fwd"]
    Ix = IDX["kry"]
    lines = ["key text: the four ciphertexts as one panel, offset 0; KRYPTOS table, Vigenere, no move", "",
             "place  known  carved  needed  offered  needed - offered"]
    diffs = []
    for q in sorted(known):
        need = (Ix[ct[q - 1]] - Ix[known[q]]) % 26
        off = Ix[s[q - 1]]
        diffs.append((need - off) % 26)
        if q in (22, 23, 24, 25, 64, 65, 74):
            lines.append(f"{q:>5}  {known[q]:>5}  {ct[q - 1]:>6}  {need:>6}  {off:>7}  {(need - off) % 26:>15}")
    best = max(diffs.count(v) for v in set(diffs))
    lines += ["", f"the most common value of the last column covers {best} of 24 places; a shift with 3 slips needs 21"]
    return "\n".join(lines)
