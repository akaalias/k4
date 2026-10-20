"""Experiment 0213. See program.md for the contract."""

EXPERIMENT = {
    "slug": "plaintext-autokey-with-slips-and-a-lost-step",
    "title": "A1.4, part 2: plaintext autokey on the sculpture's and the vocabulary's tables, lags 1-52, with up to two carved slips breaking the chain, or one lost step that runs on through it; exact, the readings judged against scrambled copies, with planted slipped messages",
    "family": "1-keyed-periodic",
    "parent": "0025-autokey-keyword-mixed-alphabets",
    "changed": (
        "A1.4 (Stage 2, step 2, issue #76), second part. 0003, 0012 and 0025 chained plaintext autokey from the known "
        "letters with no slip: lags 1-25 and 30-52 dead, 26-29 noise by quadgrams. In plaintext autokey a wrong carved "
        "letter does not change the message but breaks our derivation through it, so (a) every lag 1-52 is rerun allowing up "
        "to 2 breaks (slips anywhere in the chain, the known places included); (b) one lost step (from some place on, the "
        "key is the message letter L + 1 or L - 1 back), at every place, as its own setting: everything after it shifts; "
        "(c) at lags 26-29, where the known letters give 0-1 checks, every table's reading is scored and the best go to the "
        "blind judge, which reads past a slip that garbles the rest of a chain (bench class 'half'). 35,721 table setups "
        "(0025's), compiled; K4 against 20 scrambled copies; three planted messages."
    ),
    "hypothesis_expert": (
        "A1 (knowledge/12-assumptions.md); C11a (NSA 1992: 'plain-text auto-key (if a high-frequency letter is assigned "
        "0)'; NSA 2007 tested it without cribs), C27(a), Sanborn 2005 'Saying I was sloppy'. Model: c_i = C[E(P(p_i), "
        "K(p_{i-L}))] after a primer of L letters; P, C from 0025's 63 alphabets (standard, KRYPTOS, vocabulary keyword), "
        "K standard, KRYPTOS or the plain alphabet; Vigenere, Beaufort, variant. Each equation links p_i and p_{i-L} by a "
        "bijection, so the message splits into L chains; two known letters in one chain must agree through every carved "
        "letter between them. A slip at place j cuts the chain at j: the least number of cuts is the number of disagreeing "
        "neighbouring known pairs, at most 2 here (17.5 bits to name). A lost step at j: p_i keyed by p_{i-L-1} or "
        "p_{i-L+1} from j on, which joins the chains differently (a forest; known letters in one tree must agree), j = "
        "2-74, about 7 bits. Readings: every letter whose chain holds a known letter. Counted per lag, K4 against each copy; "
        "readings keeping 3 or more checks, and at 26-29 the best by quadgrams of every text, go to the judge in one call."
    ),
    "hypothesis_eli5": (
        "In a plaintext autokey the message is its own key: each letter is enciphered with the message letter L places "
        "before it. The known words then let us work out letters further along the message, one step at a time, like a "
        "chain. One wrongly carved letter breaks the chain there, and a hand slip that loses one step shifts everything "
        "after it. Earlier experiments allowed neither. Here we allow two broken links, or one lost step anywhere, on the "
        "carving and on scrambled copies, and a language model reads what comes out, blind to which is which."
    ),
    "prediction": (
        "No lag below 26 fits K4 with 2 breaks or one lost step where it keeps 3 or more checks beyond the copies' rate; "
        "at 26-29 K4's best reading is judged inside the copies'. All three plants found. Zero candidates pass gate 4."
    ),
    "method": (
        "1. For each table setup, lag and text, walk every chain between neighbouring known letters and count the pairs "
        "that disagree; keep up to 2. 2. For each lost step (lag L before place j, L + 1 or L - 1 from it), walk each known "
        "letter to the root of its tree and require known letters sharing a root to agree. 3. At lags 26-29, derive every "
        "reading and score it by quadgrams in the same compiled pass. 4. Readings to quadgrams; each text's 5 best and every "
        "reading at or above -5.0 to the judge, all texts in one call. 5. Counts per lag, K4 against 20 copies; plants and "
        "their own copies through the same search."
    ),
    "walkthrough": (
        "1. Choose a lag, say 12, and a table. "
        "2. Known place 22 (E) and place 34 (T) are 12 apart: the carved letter at 34 and E as its key must give T on the table. "
        "3. Work along each chain of places 12 apart, from one known letter to the next, and mark the pairs that disagree. "
        "4. Each disagreeing pair needs one carved slip somewhere between them; allow up to two. "
        "5. For a lost step, from some place on use the letter 13 (or 11) back as the key instead, and require every pair to agree. "
        "6. Read every letter a known letter reaches through its chain, and compare with scrambled copies."
    ),
}

import ctypes
import importlib.util
import itertools
import multiprocessing as mp
import os
import random
import subprocess
import sys
import tempfile
import types
from array import array
from pathlib import Path

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
ROOT = Path(__file__).resolve().parent
if not (ROOT / "experiments").exists():
    ROOT = Path.cwd()
KMAX = 2
RMIN = 3
CUT = -5.0
TOPC = 20
TOPJ = 5
N_COPIES = 20
N_PLANT_COPIES = 5
MODES = ("vig", "beau", "varbeau")
MODE_N = {"vig": 0, "beau": 1, "varbeau": 2}
ENC = {"vig": lambda p, k: (p + k) % 26, "beau": lambda p, k: (k - p) % 26, "varbeau": lambda p, k: (p - k) % 26}
DEC = {"vig": lambda c, k: (c - k) % 26, "beau": lambda c, k: (k - c) % 26, "varbeau": lambda c, k: (c + k) % 26}
NEED = {"vig": lambda p, c: (c - p) % 26, "beau": lambda p, c: (c + p) % 26, "varbeau": lambda p, c: (p - c) % 26}


def _load(prefix):
    d = sorted((ROOT / "experiments").glob(prefix + "-*"))[0]
    spec = importlib.util.spec_from_file_location(f"exp{prefix}", d / "attack.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def table_setups(vocab):
    """0025's: plain and cipher alphabet from the 63 (standard, KRYPTOS, vocabulary keyword), key standard, KRYPTOS or plain."""
    pool = _load("0045").pool_of(vocab)
    out, seen = [], set()
    for pn, pa in pool.items():
        for cn, ca in pool.items():
            for kn, ka in (("std", STD), ("kry", KRY), ("plain", pa)):
                for m in MODES:
                    if (pa, ca, ka, m) not in seen:
                        seen.add((pa, ca, ka, m)); out.append((f"{pn}|{cn}|{kn}|{m}", pa, ca, ka, m))
    return out


C_SRC = r"""
static int md(int x){ x%=26; return x<0?x+26:x; }
static inline int fwd(int m,const int*pinv,const int*ci,const int*ki,int c,int x){ int k=ki[x],v=ci[c]; v= m==0?md(v-k):(m==1?md(k-v):md(v+k)); return pinv[v]; }
static inline int bwd(int m,const int*pi,const int*ci,const int*kinv,int c,int p){ int v= m==0?md(ci[c]-pi[p]):(m==1?md(ci[c]+pi[p]):md(pi[p]-ci[c])); return kinv[v]; }
static const float *QG; static float QFLOOR;
void set_qg(const float*q,float fl){ QG=q; QFLOOR=fl; }
static float quad(const int*r,const int*isknown){ int buf[97],n=0; for(int i=0;i<97;i++) if(!isknown[i] && r[i]>=0) buf[n++]=r[i];
  if(n<4) return QFLOOR; double s=0; for(int i=0;i+3<n;i++) s+=QG[((buf[i]*26+buf[i+1])*26+buf[i+2])*26+buf[i+3]]; return (float)(s/(n-3)); }
long run_pa(int ns,const int*PI,const int*CI,const int*KI,const int*PINV,const int*KINV,const int*M,
            const int*text,const int*kq,const int*kl,const int*isknown,int rmin,float cut,
            long*counts,long*skip,long maxh,int*hits,long*nb_out,long maxb,int*bulk){
  long nh=0,nb=0; int root[98];
  for(int s=0;s<ns;s++){
    const int*pi=PI+26*s,*ci=CI+26*s,*ki=KI+26*s,*pinv=PINV+26*s,*kinv=KINV+26*s; int m=M[s];
    for(int L=1;L<=52;L++){
      int d=0,pairs=0;
      for(int e=0;e<24 && d<=2;e++){ int a=kq[e]; int f2=-1; for(int f=e+1;f<24;f++) if((kq[f]-a)%L==0){ f2=f; break; }
        if(f2<0) continue; pairs++; int b=kq[f2]; int x=kl[e]; for(int i=a+L;i<=b;i+=L) x=fwd(m,pinv,ci,ki,text[i-1],x);
        if(x!=kl[f2]) d++; }
      if(d<=2){ counts[L*3+d]++; if(pairs-d>=rmin && nh<maxh){ int*h=hits+5*nh; h[0]=s;h[1]=L;h[2]=d;h[3]=-1;h[4]=-1; nh++; } }
      if(L>=26 && L<=29 && d==0){ int r[97]; for(int i=0;i<97;i++) r[i]=-1;
        for(int e=0;e<24;e++) r[kq[e]-1]=kl[e];
        for(int e=0;e<24;e++){ int q=kq[e]; int x=kl[e];
          for(int i=q+L;i<=97;i+=L){ if(isknown[i-1]) break; x=fwd(m,pinv,ci,ki,text[i-1],x); r[i-1]=x; }
          x=kl[e]; for(int i=q;i-L>=1;i-=L){ if(isknown[i-L-1]) break; x=bwd(m,pi,ci,kinv,text[i-1],x); r[i-L-1]=x; } }
        float sc=quad(r,isknown);
        if(nb<maxb){ int*b=bulk+3*nb; b[0]=s;b[1]=L;b[2]=(int)(sc*1000); nb++; } }
      for(int di=0;di<2;di++){ int L2=di==0?L+1:L-1; if(L2<1) continue;
        for(int j=2;j<=74;j++){
          for(int i=0;i<98;i++) root[i]=-1;
          int ok=1,checks=0;
          for(int e=0;e<24 && ok;e++){ int i=kq[e]; int x=kl[e];
            while(1){ int lg=i>=j?L2:L; int par=i-lg; if(par<1) break; x=bwd(m,pi,ci,kinv,text[i-1],x); i=par; }
            if(root[i]<0){ root[i]=x; } else { checks++; if(root[i]!=x) ok=0; } }
          if(ok && checks>0){ skip[L*2+di]++; if(checks>=rmin && nh<maxh){ int*h=hits+5*nh; h[0]=s;h[1]=L;h[2]=0;h[3]=di;h[4]=j; nh++; } } } } } }
  *nb_out=nb; return nh; }
"""
_LIB = None
_KEEP = []


def lib():
    global _LIB
    if _LIB is None:
        d = tempfile.mkdtemp(prefix="k4_pa_")
        src, so = os.path.join(d, "pa.c"), os.path.join(d, "pa.so")
        Path(src).write_text(C_SRC)
        subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", so, src], check=True, capture_output=True)
        _LIB = ctypes.CDLL(so)
        P, ci, cl = ctypes.POINTER, ctypes.c_int, ctypes.c_long
        _LIB.run_pa.restype = cl
        _LIB.run_pa.argtypes = [ci] + [P(ci)] * 10 + [ci, ctypes.c_float, P(cl), P(cl), cl, P(ci), P(cl), cl, P(ci)]
        _LIB.set_qg.argtypes = [P(ctypes.c_float), ctypes.c_float]
    return _LIB


def I(a, typ="i", ct=ctypes.c_int):
    buf = array(typ, a)
    _KEEP.append(buf)
    return (ct * len(buf)).from_buffer(buf)


class PA:
    def __init__(self, setups, known):
        from kryptos.scorer import _table
        logs, floor = _table()
        q = [floor] * (26 ** 4)
        for k, v in logs.items():
            a, b, c, d = (ord(x) - 65 for x in k)
            q[((a * 26 + b) * 26 + c) * 26 + d] = v
        self.qg = I(q, "f", ctypes.c_float)
        self.floor = floor
        self.setups = setups
        self.PI = I([pa.index(c) for _, pa, _, _, _ in setups for c in STD])
        self.CI = I([ca.index(c) for _, _, ca, _, _ in setups for c in STD])
        self.KI = I([ka.index(c) for _, _, _, ka, _ in setups for c in STD])
        self.PINV = I([ord(pa[i]) - 65 for _, pa, _, _, _ in setups for i in range(26)])
        self.KINV = I([ord(ka[i]) - 65 for _, _, _, ka, _ in setups for i in range(26)])
        self.M = I([MODE_N[m] for *_, m in setups])
        self.known = known
        self.kq = sorted(known)
        self.kqI = I(self.kq)
        self.klI = I([ord(known[q]) - 65 for q in self.kq])
        self.isk = I([1 if i + 1 in known else 0 for i in range(N)])

    def run(self, text):
        lib().set_qg(self.qg, self.floor)
        cl = ctypes.c_long
        counts = (cl * (53 * 3))(); skip = (cl * (53 * 2))()
        maxh, maxb = 200000, 400000
        hits = (ctypes.c_int * (5 * maxh))(); bulk = (ctypes.c_int * (3 * maxb))(); nb = cl(0)
        nh = lib().run_pa(len(self.setups), self.PI, self.CI, self.KI, self.PINV, self.KINV, self.M, I([ord(c) - 65 for c in text]),
                          self.kqI, self.klI, self.isk, RMIN, ctypes.c_float(CUT), counts, skip, maxh, hits, ctypes.byref(nb), maxb, bulk)
        H = [tuple(hits[5 * i + j] for j in range(5)) for i in range(nh)]
        B = [(bulk[3 * i], bulk[3 * i + 1], bulk[3 * i + 2] / 1000) for i in range(nb.value)]
        return ({L: [counts[L * 3 + d] for d in range(3)] for L in range(1, 53)},
                {L: [skip[L * 2], skip[L * 2 + 1]] for L in range(1, 53)}, H, B, nh >= maxh or nb.value >= maxb)

    def fwd(self, s, c, x):
        _, pa, ca, ka, m = self.setups[s]
        return pa[DEC[m](ca.index(c), ka.index(x))]

    def bwd(self, s, c, p):
        _, pa, ca, ka, m = self.setups[s]
        return ka[NEED[m](pa.index(p), ca.index(c))]

    def reading_chain(self, text, s, L, cuts=()):
        """Derive along each chain from its known letters; a cut at place j stops the walk through j."""
        r = ["?"] * N
        for q in self.kq:
            r[q - 1] = self.known[q]
        for q in self.kq:
            x = self.known[q]
            i = q + L
            while i <= N and i not in self.known and i not in cuts:
                x = self.fwd(s, text[i - 1], x); r[i - 1] = x; i += L
            x = self.known[q]; i = q
            while i - L >= 1 and (i - L) not in self.known and i not in cuts:
                x = self.bwd(s, text[i - 1], x); r[i - L - 1] = x; i -= L
        return "".join(r)

    def reading_skip(self, text, s, L, L2, j):
        """Lost step: lag L before place j, L2 from j on. Derive from every known letter over its tree."""
        lag = lambda i: L2 if i >= j else L  # noqa: E731
        children = {}
        for i in range(1, N + 1):
            p = i - lag(i)
            if p >= 1:
                children.setdefault(p, []).append(i)
        r = {q: self.known[q] for q in self.kq}
        stack = list(self.kq)
        while stack:
            i = stack.pop()
            p = i - lag(i)
            if p >= 1 and p not in r:
                r[p] = self.bwd(s, text[i - 1], r[i]); stack.append(p)
            for c in children.get(i, []):
                if c not in r:
                    r[c] = self.fwd(s, text[c - 1], r[i]); stack.append(c)
        return "".join(r.get(i, "?") for i in range(1, N + 1))


def pa_encrypt(pt, pa, ca, ka, m, L, primer, skip=None):
    out = []
    for i, p in enumerate(pt):
        lg = skip[1] if skip and i >= skip[0] else L
        k = primer[i] if i < lg else pt[i - lg]
        out.append(ca[ENC[m](pa.index(p), ka.index(k))])
    return "".join(out)


def encrypt(plaintext, key):
    sk = (key["skip_at"], key["skip_lag"]) if key.get("skip_at") is not None else None
    out = list(pa_encrypt(plaintext, key["pa"], key["ca"], key["ka"], key["m"], key["lag"], key["primer"], sk))
    for q, ch in key.get("slips", []):
        out[q - 1] = ch
    return "".join(out)


_STATE = {}


def one_text(t):
    pa = _STATE["pa"]
    cnt, skp, H, B, capped = pa.run(t)
    recs = []
    for h in H:
        s, L, d, di, j = h
        if di < 0:
            if d == 0:
                recs.append({"kind": "chain", "s": s, "L": L, "d": 0, "cuts": [], "reading": pa.reading_chain(t, s, L)})
            else:
                bad = []
                for e, a in enumerate(pa.kq):
                    b = next((q for q in pa.kq[e + 1:] if (q - a) % L == 0), None)
                    if b is None:
                        continue
                    x = pa.known[a]
                    for i in range(a + L, b + 1, L):
                        x = pa.fwd(s, t[i - 1], x)
                    if x != pa.known[b]:
                        bad.append(list(range(a + L, b + 1, L)))
                for cuts in itertools.product(*bad):
                    recs.append({"kind": "chain", "s": s, "L": L, "d": d, "cuts": list(cuts), "reading": pa.reading_chain(t, s, L, set(cuts))})
        else:
            L2 = L + 1 if di == 0 else L - 1
            recs.append({"kind": "skip", "s": s, "L": L, "L2": L2, "j": j, "reading": pa.reading_skip(t, s, L, L2, j)})
    B.sort(key=lambda b: -b[2])
    for s, L, sc in [b for b in B if b[2] >= CUT] + B[:TOPC]:
        recs.append({"kind": "bulk", "s": s, "L": L, "d": 0, "cuts": [], "reading": pa.reading_chain(t, s, L), "bulk_quad": sc})
    seen, uniq = set(), []
    for r in recs:
        k_ = (r["kind"], r["s"], r["L"], tuple(r.get("cuts", [])), r.get("j"), r.get("L2"))
        if k_ not in seen:
            seen.add(k_); uniq.append(r)
    return {"counts": cnt, "skip": skp, "recs": uniq, "capped": capped, "bulk_n": len(B)}


def shuffled(text, seed):
    l_ = list(text)
    random.Random(seed).shuffle(l_)
    return "".join(l_)


def run(ctx):
    from kryptos.plants import english_plant
    known = ctx.KNOWN
    setups = table_setups(list(ctx.vocabulary))
    pa = PA(setups, known)
    sidx = {(a, b, c, d): i for i, (_, a, b, c, d) in enumerate(setups)}
    kq = sorted(known)
    plants = []
    specs = [  # (seed, (pa, ca, ka, m), L, slips, lost step (place 0-based, new lag))
        (2131, (STD, KRY, KRY, "vig"), 12, 2, None),
        (2132, (KRY, KRY, KRY, "beau"), 20, 0, (49, 21)),
        (2133, (KRY, STD, STD, "varbeau"), 8, 1, None),
    ]
    for seed, (a, b, c, m), L, k, skip in specs:
        rng = random.Random(seed)
        pt = english_plant(seed)
        primer = "".join(rng.choice(STD) for _ in range(L + 2))
        ct = list(pa_encrypt(pt, a, b, c, m, L, primer, skip))
        inner = sorted({i for e, q in enumerate(kq) for q2 in kq[e + 1:] if (q2 - q) % L == 0 for i in range(q + L, q2 + 1, L)})
        places = sorted(rng.sample(inner, k)) if k else []
        if seed == 2133:  # one slip that runs on: past the last known letter of its chain (69 -> 77 -> 85 -> 93)
            places = [77]
        for q in places:
            ct[q - 1] = rng.choice([x for x in STD if x != ct[q - 1]])
        plants.append({"seed": seed, "setup": sidx[(a, b, c, m)], "L": L, "k": len(places), "skip": skip, "slips": places, "pt": pt, "ct": "".join(ct)})
    texts = []
    for j, p in enumerate(plants):
        texts.append((f"plant{j + 1}", p["ct"]))
        texts += [(f"plant{j + 1}-copy{i + 1}", shuffled(p["ct"], p["seed"] * 100 + i)) for i in range(N_PLANT_COPIES)]
    texts.append(("K4", ctx.K4))
    texts += [(f"copy{i + 1}", shuffled(ctx.K4, 2140 + i)) for i in range(N_COPIES)]
    _STATE["pa"] = pa
    if getattr(sys.modules.get(__name__), "one_text", None) is not one_text:
        mod = types.ModuleType(__name__); mod.__dict__.update(globals()); sys.modules[__name__] = mod
    res = {}
    with mp.get_context("fork").Pool(8) as pool:
        it = pool.imap(one_text, [t for _, t in texts])
        for name, _ in texts:
            res[name] = it.next()
            if ctx.time_left() < 300:
                pool.terminate()
                break

    def quad(r):
        return ctx.english_score("".join(c for i, c in enumerate(r, start=1) if i not in known and c != "?"))
    to_judge = set()
    for v in res.values():
        for r in v["recs"]:
            r["quad"] = quad(r["reading"])
        top = sorted(v["recs"], key=lambda r: -r["quad"])[:TOPJ]
        for r in top + [r for r in v["recs"] if r["quad"] >= CUT]:
            to_judge.add(r["reading"])
    order = sorted(to_judge)
    verdicts = dict(zip(order, ctx.judge(order))) if order else {}
    for v in res.values():
        for r in v["recs"]:
            if r["reading"] in verdicts:
                r["judge"] = verdicts[r["reading"]]["score"]

    def jbest(name):
        sc = [r["judge"] for r in res[name]["recs"] if r.get("judge") is not None]
        return max(sc) if sc else None
    plant_out = []
    for j, p in enumerate(plants):
        name = f"plant{j + 1}"
        if name not in res:
            plant_out.append({"seed": p["seed"], "found": False}); continue
        if p["skip"]:
            want = lambda r: r["kind"] == "skip" and r["s"] == p["setup"] and r["L"] == p["L"] and r["L2"] == p["skip"][1]  # noqa: E731
        else:
            want = lambda r: r["kind"] in ("chain", "bulk") and r["s"] == p["setup"] and r["L"] == p["L"]  # noqa: E731
        wrong = lambda r: sum(1 for i, c in enumerate(r["reading"]) if c != "?" and (i + 1) not in known and c != p["pt"][i])  # noqa: E731
        good = [r for r in res[name]["recs"] if want(r) and wrong(r) <= 3]
        best = max(good, key=lambda r: (r.get("judge") or -1)) if good else None
        own = [jbest(f"{name}-copy{i + 1}") for i in range(N_PLANT_COPIES)]
        own_bar = max([x for x in own if x is not None], default=None)
        hj = best.get("judge") if best else None
        plant_out.append({"seed": p["seed"], "L": p["L"], "k": p["k"], "skip": p["skip"], "slips": p["slips"],
                          "planted_setting_found": bool(good), "wrong_letters_in_reading": wrong(best) if best else None,
                          "quad": round(best["quad"], 3) if best else None, "judge": hj, "own_copies_judge_best": own,
                          "found": bool(best) and hj is not None and (own_bar is None or hj > own_bar)})
    copies = [n for n, _ in texts if n.startswith("copy") and n in res]
    k4 = res["K4"]
    copies_j = [jbest(n) for n in copies]
    bar = max([x for x in copies_j if x is not None], default=None)
    by_lag = {}
    for L in range(1, 53):
        by_lag[str(L)] = {"k4": k4["counts"][L], "copies_max": [max(res[n]["counts"][L][d] for n in copies) for d in range(3)],
                          "copies_min": [min(res[n]["counts"][L][d] for n in copies) for d in range(3)],
                          "skip_k4": k4["skip"][L], "skip_copies_max": [max(res[n]["skip"][L][x] for n in copies) for x in range(2)]}
    tot = lambda n, L: sum(res[n]["counts"][L]) + sum(res[n]["skip"][L])  # noqa: E731
    above = [L for L in range(1, 53) if tot("K4", L) > max(tot(n, L) for n in copies)]
    null = [sum(1 for L in range(1, 53) if tot(n, L) > max(tot(o, L) for o in ["K4"] + copies if o != n)) for n in copies]
    shortest = {n: next((L for L in range(1, 53) if sum(res[n]["counts"][L])), None) for n in ["K4"] + copies}
    shortest_skip = {n: next((L for L in range(1, 53) if sum(res[n]["skip"][L])), None) for n in ["K4"] + copies}
    cands = []
    for r in sorted(k4["recs"], key=lambda r: (-(r.get("judge") or -1), -r["quad"]))[:10]:
        _, a, b, c, m = setups[r["s"]]
        L = r["L"]
        pt = "".join(known.get(i + 1, ("A" if ch == "?" else ch)) for i, ch in enumerate(r["reading"]))
        sk = (r["j"] - 1, r["L2"]) if r["kind"] == "skip" else None
        key = {"pa": a, "ca": b, "ka": c, "m": m, "lag": L, "primer": "A" * (max(L, r.get("L2", 0)) + 1),
               "skip_at": sk[0] if sk else None, "skip_lag": sk[1] if sk else None}
        re_ = encrypt(pt, key)
        key["slips"] = [[i + 1, ctx.K4[i]] for i in range(N) if re_[i] != ctx.K4[i]]
        cands.append({"plaintext": pt, "key": key, "key_bits": 4.7 * L + 9.3 * len(key["slips"]),
                      "key_description": f"plaintext autokey lag {L}, {setups[r['s']][0]}, {r['kind']}, cuts {r.get('cuts')}, lost step {sk}; unknown letters filled with A, every disagreeing carved letter named as a slip",
                      "notes": f"judge {r.get('judge')}, quadgram {r['quad']:.3f}"})
    return {
        "candidates": cands,
        "controls": [max([r["quad"] for r in res[n]["recs"]], default=-9.0) for n in copies],
        "bounds": {
            "family": "plaintext autokey on 0025's tables, lags 1-52, up to 2 chain breaks (slips) or one lost step (A1.4)",
            "table_setups": len(setups), "lags": "1-52 (53-96 blocked by 0136's bound)",
            "breaks": "0-2 anywhere in a chain between neighbouring known letters (known places included)",
            "lost_step": "lag L before place j, L+1 or L-1 from j on, j = 2-74; known letters in one tree must agree",
            "bulk": f"lags 26-29 with no break: every table's reading scored by quadgrams; the top {TOPC} and all at or above {CUT} per text to the judge",
            "by_lag": by_lag, "k4_above_every_copy_lags": above, "copies_above_rest": null,
            "shortest_lag_with_breaks": shortest, "shortest_lag_lost_step": shortest_skip,
            "readings": {"k4": len(k4["recs"]), "copies": [len(res[n]["recs"]) for n in copies]},
            "capped": [n for n, v in res.items() if v["capped"]],
            "judge": {"sent": len(order), "none": sum(1 for v in verdicts.values() if v["score"] is None), "cut": CUT,
                      "rule": f"each text's top {TOPJ} readings by quadgrams and every reading at or above {CUT}; one call"},
            "k4_judge_best": jbest("K4"), "copies_judge_best": copies_j,
            "k4_readings_above_every_copy": sum(1 for r in k4["recs"] if r.get("judge") is not None and bar is not None and r["judge"] > bar),
            "k4_top": [{"reading": r["reading"], "judge": r.get("judge"), "quad": round(r["quad"], 3), "kind": r["kind"], "setup": setups[r["s"]][0], "L": r["L"]}
                       for r in sorted(k4["recs"], key=lambda r: -(r.get("judge") or -1))[:5]],
            "plants": plant_out,
            "slip_cost_bits": {"1": 9.3, "2": 17.5, "lost step": 7.2},
            "controls": f"{N_COPIES} shuffled copies (seeds 2140-2159); each plant against {N_PLANT_COPIES} shuffles of its own ciphertext",
            "exhaustive": "yes",
        },
        "notes": (f"{len(setups):,} tables x lags 1-52; K4 shortest lag with <= 2 breaks {shortest['K4']}, lost step {shortest_skip['K4']}; "
                  f"copies {sorted(v for k_, v in shortest.items() if k_ != 'K4' and v)}; judge sent {len(order)}, K4 best {jbest('K4')}, copies best {bar}; "
                  f"plants found {[p['found'] for p in plant_out]}"),
    }


def worked_example(ctx, key):
    known, ct = ctx.KNOWN, ctx.K4
    L = 12
    lines = [f"plaintext autokey, lag {L}, KRYPTOS table, Vigenere: chains of places {L} apart, walked from one known letter to the next", ""]
    I_ = {c: i for i, c in enumerate(KRY)}
    bad = 0
    for e, a in enumerate(sorted(known)):
        b = next((q for q in sorted(known)[e + 1:] if (q - a) % L == 0), None)
        if b is None:
            continue
        x = known[a]
        for i in range(a + L, b + 1, L):
            x = KRY[(I_[ct[i - 1]] - I_[x]) % 26]
        bad += x != known[b]
        if len(lines) < 10:
            lines.append(f"  {a} {known[a]} -> {b}: the chain gives {x}, known {known[b]}{'' if x == known[b] else '   break needed'}")
    lines += ["", f"breaks needed at lag {L}: {bad} (2 allowed)"]
    return "\n".join(lines)
