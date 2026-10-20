"""Experiment 0212. See program.md for the contract."""

EXPERIMENT = {
    "slug": "ciphertext-autokey-and-progressive-key-with-slips",
    "title": "A1.4, part 1: ciphertext autokey on every keyword table tried so far, every lag, with up to two of the 24 known letters carved wrong or one skipped step in the chain; and the progressive key on the sculpture's tables with up to two slips; exact, judged against scrambled copies, with planted slipped messages",
    "family": "1-keyed-periodic",
    "parent": "0064-ciphertext-autokey-k1-k3-word-alphabets",
    "changed": (
        "A1.4 (Stage 2, step 2, issue #76), first part. 0002, 0025, 0064, 0071 and 0072 required every known letter past "
        "the primer to agree with ciphertext autokey (0064's fewest was 3 mismatches on K4, 2-3 on copies); 0011 required "
        "all 24 for the progressive key. Here: (a) ciphertext autokey on the union of their tables (about 550,000 table "
        "setups), every lag 1-96, with up to 2 failed checks (a slip at a known place stays put: the next key letter is "
        "the letter he carved); (b) one skipped or repeated step in the autokey chain (from some known place on the lag is "
        "one more or one less), at every place, as its own setting; (c) the progressive key (0011) on the 8 table classes, "
        "periods 1-52, steps 1-25, both forms, up to 2 slips. Compiled for (a) and (b). Readings of settings that keep at "
        "least 3 checks go to quadgrams and the blind judge with the copies'. Plants for each part in the same run."
    ),
    "hypothesis_expert": (
        "A1 (knowledge/12-assumptions.md); C11a (NSA 1992: 'plain-text auto-key'; the NSA analyst 2007 tested both "
        "autokeys), C5(a) (a key word and a hand schedule), C27(a) (Sanborn's PALIMPCEST slip), Sanborn 2005 'Saying I was "
        "sloppy is a good way of saying it'. Ciphertext autokey: c_i = C[E(P(p_i), K(c_{i-L}))], P, C, K alphabets from "
        "0025's 63 (standard, KRYPTOS, vocabulary keyword), 0064's K1-K3 and C13/C14 words, 0072's compass words (pairs "
        "of any two; key alphabet standard, KRYPTOS, plain or cipher), and 0071's 925 near-KRYPTOS alphabets (with "
        "themselves or the standard alphabet); Vigenere, Beaufort, variant. Every known place q > L is a check; a slip at a "
        "known place fails only its own check, because the following key letters are the carved ones. A skipped step: the "
        "key for every known place from the e-th on is the carved letter L + 1 (or L - 1) back. Progressive key: key value "
        "at place i = w[i mod P] + d i (per letter) or + d floor(i / P) (per repeat), 8 table classes (the key alphabet "
        "drops out; variant Beaufort is a negated step). Counted: settings with 0, 1, 2 failed checks per lag (per period "
        "and step), K4 against 20 copies. Slip cost: 9.3 bits for 1, 17.5 for 2; a skipped step about log2(24 x 2) = 5.6 "
        "bits. Where 2 or fewer checks would remain the known letters decide nothing and the cell is counted only."
    ),
    "hypothesis_eli5": (
        "In an autokey cipher the key keeps growing out of the message itself: after a few starting letters, each new key "
        "letter is a letter already enciphered. Done by hand, one slip is easy: a wrong letter at one place, or losing "
        "your place in the chain and carrying on one letter off. Earlier experiments threw away any setting that missed "
        "even one known letter. Here we allow two wrong letters, or one lost place, on the carving and on scrambled "
        "copies, and we hide messages of our own made with such slips to check they are found. The same for the "
        "progressive key, whose key word shifts one step further along the table after every letter or every round."
    ),
    "prediction": (
        "Ciphertext autokey: at lags with 8 or more checks no setting with 2 slips or one skipped step on K4, at the "
        "copies' rate elsewhere; nothing judged above every copy. Progressive key: nothing below period 24 with 2 slips "
        "(as 0207 for the plain periodic key). All plants found. Zero candidates pass gate 4."
    ),
    "method": (
        "1. Build the tables. 2. For each table setup and text: the key index each known place needs. 3. For each lag: "
        "compare with the key letter the carved text offers L back, count failures, keep up to 2; for each skipped step "
        "(lag L before the e-th known place, L + 1 or L - 1 from it), keep only exact fits. 4. Progressive key: per class, "
        "period, step and form, the forced base values per slot; enumerate settings with up to 2 slips. 5. Count by lag "
        "and slips, K4 against 20 copies. 6. Readings of settings keeping 3 or more checks: each text's best by quadgrams "
        "and every one at or above -5.0 go to the judge, all texts in one call. 7. Plants and their own copies through "
        "the same search."
    ),
    "walkthrough": (
        "1. Write K4 and, under each letter, the carved letter L places before it: that is the autokey's key. "
        "2. At each of the 24 known places, look up on the table what the known letter and that key letter give. "
        "3. Count the places where it is not the carved letter: up to 2 are allowed as slips. "
        "4. For a lost place: from one known letter on, take the key from L + 1 (or L - 1) places back instead, and require every place to agree. "
        "5. Read the message wherever the key is known, and do the same on scrambled copies of the carving. "
        "6. For the progressive key, write the key word under the text, add d to every key letter's place on the table for every letter (or every round), and count the slips the same way."
    ),
}

import ctypes
import multiprocessing as mp
import sys
import types
from array import array
import importlib.util
import os
import random
import subprocess
import tempfile
from pathlib import Path

from kryptos.alphabets import keyword_mixed, decrypt_letter, key_letter_for, encrypt_letter
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
ROOT = Path(__file__).resolve().parent
if not (ROOT / "experiments").exists():
    ROOT = Path.cwd()
KMAX = 2
RMIN = 3
CUT = -5.0
N_COPIES = 20
N_PLANT_COPIES = 5
MODES = ("vig", "beau", "varbeau")
MODE_N = {"vig": 0, "beau": 1, "varbeau": 2}
DEC = {"vig": lambda c, k: (c - k) % 26, "beau": lambda c, k: (k - c) % 26, "varbeau": lambda c, k: (c + k) % 26}
ENC = {"vig": lambda p, k: (p + k) % 26, "beau": lambda p, k: (k - p) % 26, "varbeau": lambda p, k: (p - k) % 26}


def _load(prefix):
    d = sorted((ROOT / "experiments").glob(prefix + "-*"))[0]
    spec = importlib.util.spec_from_file_location(f"exp{prefix}", d / "attack.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def table_setups(vocab):
    """(name, pa, ca, ka, mode): the union of 0025, 0064, 0071, 0072's tables."""
    words = {"std": STD, "kry": KRY}
    for name, A in _load("0045").pool_of(vocab).items():          # 0025's 63: std, kry, vocabulary keyword alphabets
        words.setdefault(name, A)
    p64, _ = _load("0064").word_pool(vocab)                       # K1-K3 and C13/C14 words
    for name, A in p64.items():
        words.setdefault(name, A)
    for name, A in _load("0072").pool().items():                   # compass points and the 2025 letter's words
        words.setdefault(name, A)
    uniq = {}
    for name, A in words.items():
        uniq.setdefault(A, name)
    W = [(n, A) for A, n in uniq.items()]
    out, seen = [], set()

    def add(pn, pa, cn, ca, kn, ka, m):
        key = (pa, ca, ka, m)
        if key not in seen:
            seen.add(key); out.append((f"{pn}|{cn}|{kn}|{m}", pa, ca, ka, m))
    for pn, pa in W:
        for cn, ca in W:
            for kn, ka in (("std", STD), ("kry", KRY), ("plain", pa), ("cipher", ca)):
                for m in MODES:
                    add(pn, pa, cn, ca, kn, ka, m)
    for V, vn in _load("0071").variants().items():                 # 925 near-KRYPTOS alphabets
        for pn, pa, cn, ca in ((vn, V, vn, V), ("std", STD, vn, V), (vn, V, "std", STD)):
            for kn, ka in (("std", STD), ("kry", KRY), ("variant", V)):
                for m in MODES:
                    add(pn, pa, cn, ca, kn, ka, m)
    return out


C_SRC = r"""
static int md(int x){ x%=26; return x<0?x+26:x; }
static int keyfor(int m,int p,int c){ return m==0?md(c-p):(m==1?md(c+p):md(p-c)); }
long run_ca(int ns,const int*PI,const int*CI,const int*KI,const int*M,const int*text,const int*kl,const int*kq,
            long*counts,long*skip,int rmin,long maxh,int*hits){
  long nh=0; int need[24];
  for(int s=0;s<ns;s++){
    const int*pi=PI+26*s,*ci=CI+26*s,*ki=KI+26*s; int m=M[s];
    for(int e=0;e<24;e++) need[e]=keyfor(m,pi[kl[e]],ci[text[kq[e]-1]]);
    for(int L=1;L<=96;L++){
      int n=0,mm=0;
      for(int e=0;e<24;e++){ int q=kq[e]; if(q-L<1) continue; n++; if(ki[text[q-L-1]]!=need[e]){ mm++; if(mm>2) break; } }
      if(mm<=2){ counts[L*3+mm]++; if(n-mm>=rmin && nh<maxh){ int*h=hits+5*nh; h[0]=s;h[1]=L;h[2]=mm;h[3]=-1;h[4]=-1; nh++; } }
      for(int di=0;di<2;di++){ int L2=di==0?L+1:L-1; if(L2<1||L2>96) continue;
        for(int e0=1;e0<24;e0++){ int n2=0,bad=0;
          for(int e=0;e<24;e++){ int q=kq[e]; int lg=e<e0?L:L2; if(q-lg<1) continue; n2++; if(ki[text[q-lg-1]]!=need[e]){bad=1;break;} }
          if(!bad && n2>0){ skip[L*2+di]++; if(n2>=rmin && nh<maxh){ int*h=hits+5*nh; h[0]=s;h[1]=L;h[2]=0;h[3]=di;h[4]=e0; nh++; } } } } } }
  return nh; }
"""
_LIB = None


def lib():
    global _LIB
    if _LIB is None:
        d = tempfile.mkdtemp(prefix="k4_ca_")
        src, so = os.path.join(d, "ca.c"), os.path.join(d, "ca.so")
        Path(src).write_text(C_SRC)
        subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", so, src], check=True, capture_output=True)
        _LIB = ctypes.CDLL(so)
        _LIB.run_ca.restype = ctypes.c_long
        P = ctypes.POINTER
        _LIB.run_ca.argtypes = [ctypes.c_int, P(ctypes.c_int), P(ctypes.c_int), P(ctypes.c_int), P(ctypes.c_int), P(ctypes.c_int),
                                P(ctypes.c_int), P(ctypes.c_int), P(ctypes.c_long), P(ctypes.c_long), ctypes.c_int, ctypes.c_long,
                                P(ctypes.c_int)]
    return _LIB


_KEEP = []


def I(a):
    """A C int array backed by an array.array (no argument unpacking: these run to millions of entries)."""
    buf = array("i", a)
    _KEEP.append(buf)
    return (ctypes.c_int * len(buf)).from_buffer(buf)


class CA:
    def __init__(self, setups, known):
        self.setups = setups
        self.PI = I([x for _, pa, _, _, _ in setups for x in [pa.index(c) for c in STD]])
        self.CI = I([x for _, _, ca, _, _ in setups for x in [ca.index(c) for c in STD]])
        self.KI = I([x for _, _, _, ka, _ in setups for x in [ka.index(c) for c in STD]])
        self.M = I([MODE_N[m] for *_, m in setups])
        self.kq = sorted(known)
        self.kl = I([ord(known[q]) - 65 for q in self.kq])
        self.kqI = I(self.kq)

    def run(self, text):
        counts = (ctypes.c_long * (97 * 3))()
        skip = (ctypes.c_long * (97 * 2))()
        maxh = 400000
        hits = (ctypes.c_int * (5 * maxh))()
        nh = lib().run_ca(len(self.setups), self.PI, self.CI, self.KI, self.M, I([ord(c) - 65 for c in text]), self.kl, self.kqI,
                          counts, skip, RMIN, maxh, hits)
        return ({L: [counts[L * 3 + d] for d in range(3)] for L in range(1, 97)},
                {L: [skip[L * 2], skip[L * 2 + 1]] for L in range(1, 97)},
                [tuple(hits[5 * i + j] for j in range(5)) for i in range(nh)], nh >= maxh)

    def reading(self, text, h):
        s, L, d, di, e0 = h
        _, pa, ca, ka, m = self.setups[s]
        out = []
        for i in range(N):              # 0-based
            lg = L
            if di >= 0:
                j_prev, j = self.kq[e0 - 1] - 1, self.kq[e0] - 1
                if i >= j:
                    lg = L + 1 if di == 0 else L - 1
                elif i > j_prev:
                    out.append("?"); continue
            if i - lg < 0:
                out.append("?"); continue
            out.append(pa[DEC[m](ca.index(text[i]), ka.index(text[i - lg]))])
        return "".join(out)


def ca_encrypt(pt, pa, ca, ka, m, L, primer, skip=None, slipped=None):
    """skip: (place j 0-based, new lag) from j on. slipped: {place j 0-based: letter written instead}; the chain goes on
    from the letter written, as it would by hand."""
    out = []
    for i, p in enumerate(pt):
        lg = skip[1] if skip and i >= skip[0] else L
        k = primer[i] if i < lg else out[i - lg]
        out.append(ca[ENC[m](pa.index(p), ka.index(k))])
        if slipped and i in slipped:
            out[i] = slipped[i]
    return "".join(out)


# ---- progressive key on the 8 table classes (0011), as 0207's slot enumeration
CLASSES = [(pa, ca, m) for pa in ("std", "kry") for ca in ("std", "kry") for m in ("vig", "beau")]


def prog_settings(text, known, P, d, form, cls, kmax=KMAX):
    pa, ca, m = cls
    slots = {}
    for q in sorted(known):
        i = q - 1
        v = STD.index(key_letter_for(known[q], text[i], pa, ca, "std", m))
        sh = d * i if form == "per-letter" else d * (i // P)
        slots.setdefault(i % P, []).append((q, (v - sh) % 26))
    opts = [(s, [(v, [q for q, w in eqs if w != v]) for v in sorted({w for _, w in eqs})]) for s, eqs in sorted(slots.items())]
    out = []

    def dfs(k, dd, key, slipped):
        if k == len(opts):
            out.append((dd, dict(key), list(slipped))); return
        s, ch = opts[k]
        for v, bad in ch:
            if dd + len(bad) <= kmax:
                key[s] = v
                dfs(k + 1, dd + len(bad), key, slipped + bad)
        key.pop(s, None)
    dfs(0, 0, {}, [])
    return out, 24 - len(slots)


def prog_reading(text, P, d, form, cls, key):
    pa, ca, m = cls
    out = []
    for i in range(N):
        if i % P not in key:
            out.append("?"); continue
        sh = d * i if form == "per-letter" else d * (i // P)
        out.append(decrypt_letter(text[i], STD[(key[i % P] + sh) % 26], pa, ca, "std", m))
    return "".join(out)


def prog_encrypt(pt, P, d, form, cls, base):
    pa, ca, m = cls
    return "".join(encrypt_letter(p, STD[(base[i % P] + (d * i if form == "per-letter" else d * (i // P))) % 26], pa, ca, "std", m)
                   for i, p in enumerate(pt))


def prog_search(text, known):
    counts, recs = {}, []
    for form in ("per-letter", "per-repeat"):
        for P in range(1, 53):
            for d in range(1, 26):
                for cls in CLASSES:
                    sets, checks = prog_settings(text, known, P, d, form, cls)
                    for dd, key, slipped in sets:
                        counts.setdefault(f"{form}|{P}", [0] * (KMAX + 1))[dd] += 1
                        if checks - dd >= RMIN:
                            recs.append({"kind": "prog", "form": form, "P": P, "d": d, "cls": cls, "dd": dd, "key": key,
                                         "slips": slipped, "reading": prog_reading(text, P, d, form, cls, key)})
    return counts, recs


def encrypt(plaintext, key):
    if key["kind"] == "prog":
        P, d, form, cls, base = key["P"], key["d"], key["form"], tuple(key["cls"]), key["base"]
        out = list(prog_encrypt(plaintext, P, d, form, cls, {i: base[i] for i in range(P)}))
    else:
        sk = (key["skip_at"], key["skip_lag"]) if key.get("skip_at") is not None else None
        out = list(ca_encrypt(plaintext, key["pa"], key["ca"], key["ka"], key["m"], key["lag"], key["primer"], sk))
    for q, ch in key.get("slips", []):
        out[q - 1] = ch
    return "".join(out)


_STATE = {}


def one_text(t):
    ca, known = _STATE["ca"], _STATE["known"]
    cnt, skp, hits, capped = ca.run(t)
    recs = [{"kind": "ca", "h": h, "reading": ca.reading(t, h)} for h in hits]
    pc, precs = prog_search(t, known)
    return {"ca_counts": cnt, "skip_counts": skp, "capped": capped, "prog_counts": pc, "recs": recs + precs}


def shuffled(text, seed):
    l_ = list(text)
    random.Random(seed).shuffle(l_)
    return "".join(l_)


def run(ctx):
    from kryptos.plants import english_plant
    known = ctx.KNOWN
    setups = table_setups(list(ctx.vocabulary))
    ca = CA(setups, known)
    sidx = {(pa, ca_, ka, m): i for i, (_, pa, ca_, ka, m) in enumerate(setups)}
    kq = sorted(known)
    # ---- plants
    plants = []
    sh = keyword_mixed("SHADOW")
    specs = [
        ("ca", 2121, dict(pa=sh, ca=KRY, ka=STD, m="vig", L=9), 2, None),
        ("ca", 2122, dict(pa=STD, ca=STD, ka=KRY, m="beau", L=60), 2, None),
        ("ca", 2123, dict(pa=KRY, ca=KRY, ka=KRY, m="vig", L=15), 0, (63, 16)),   # one step repeated from place 64 on
        ("prog", 2124, dict(P=11, d=3, form="per-letter", cls=("kry", "kry", "vig")), 2, None),
        ("prog", 2125, dict(P=20, d=5, form="per-repeat", cls=("std", "kry", "beau")), 2, None),
    ]
    for kind, seed, prm, k, skip in specs:
        rng = random.Random(seed)
        pt = english_plant(seed)
        if kind == "ca":
            primer = "".join(rng.choice(STD) for _ in range(prm["L"] + 1))
            clean = ca_encrypt(pt, prm["pa"], prm["ca"], prm["ka"], prm["m"], prm["L"], primer, skip)
            checked = [q for q in kq if q > prm["L"]]
            places = sorted(rng.sample(checked, k)) if k else []
            wrong = {q - 1: rng.choice([c for c in STD if c != clean[q - 1]]) for q in places}
            ct = list(ca_encrypt(pt, prm["pa"], prm["ca"], prm["ka"], prm["m"], prm["L"], primer, skip, wrong))
        else:
            base = {i: rng.randrange(26) for i in range(prm["P"])}
            ct = list(prog_encrypt(pt, prm["P"], prm["d"], prm["form"], prm["cls"], base))
            slots = {}
            for q in kq:
                slots.setdefault((q - 1) % prm["P"], []).append(q)
            checked = [q for s_, qs in slots.items() if len(qs) >= 2 for q in qs]
            places = sorted(rng.sample(checked, k)) if k else []
            for q in places:
                ct[q - 1] = rng.choice([c for c in STD if c != ct[q - 1]])
        plants.append({"kind": kind, "seed": seed, "prm": prm, "k": k, "skip": skip, "slips": places, "pt": pt, "ct": "".join(ct)})
    # ---- texts: plants and their copies first, then K4 and its copies
    texts = []
    for j, p in enumerate(plants):
        texts.append((f"plant{j + 1}", p["ct"]))
        texts += [(f"plant{j + 1}-copy{i + 1}", shuffled(p["ct"], p["seed"] * 100 + i)) for i in range(N_PLANT_COPIES)]
    texts.append(("K4", ctx.K4))
    texts += [(f"copy{i + 1}", shuffled(ctx.K4, 2130 + i)) for i in range(N_COPIES)]
    _STATE["ca"], _STATE["known"] = ca, known
    if getattr(sys.modules.get(__name__), "one_text", None) is not one_text:
        mod = types.ModuleType(__name__); mod.__dict__.update(globals()); sys.modules[__name__] = mod
    res = {}
    with mp.get_context("fork").Pool(8) as pool:
        it = pool.imap(one_text, [t for _, t in texts])
        for name, _ in texts:
            res[name] = it.next()
            if ctx.time_left() < 240:
                pool.terminate()
                break
    # ---- quadgrams, then the judge: each text's best and everything at or above CUT, one call

    def quad(r):
        return ctx.english_score("".join(c for i, c in enumerate(r, start=1) if i not in known and c != "?"))
    to_judge = set()
    for name, v in res.items():
        for r in v["recs"]:
            r["quad"] = quad(r["reading"])
        if v["recs"]:
            best = max(v["recs"], key=lambda r: r["quad"])
            for r in v["recs"]:
                if r is best or r["quad"] >= CUT:
                    r["judged"] = True; to_judge.add(r["reading"])
    order = sorted(to_judge)
    verdicts = dict(zip(order, ctx.judge(order))) if order else {}
    none_n = sum(1 for v in verdicts.values() if v["score"] is None)
    for v in res.values():
        for r in v["recs"]:
            if r.get("judged"):
                r["judge"] = verdicts[r["reading"]]["score"]

    def jbest(name):
        sc = [r["judge"] for r in res[name]["recs"] if r.get("judge") is not None]
        return max(sc) if sc else None
    # ---- plants found?
    plant_out = []
    for j, p in enumerate(plants):
        name = f"plant{j + 1}"
        if name not in res:
            plant_out.append({"seed": p["seed"], "found": False}); continue
        recs = res[name]["recs"]
        prm = p["prm"]
        if p["kind"] == "ca":
            s_ = sidx.get((prm["pa"], prm["ca"], prm["ka"], prm["m"]))
            if p["skip"]:
                e0 = next(e for e, q in enumerate(kq) if q - 1 >= p["skip"][0])
                want = lambda r: r["kind"] == "ca" and r["h"][0] == s_ and r["h"][1] == prm["L"] and r["h"][3] == 0 and r["h"][4] == e0  # noqa: E731
            else:
                want = lambda r: r["kind"] == "ca" and r["h"][0] == s_ and r["h"][1] == prm["L"] and r["h"][2] == p["k"] and r["h"][3] == -1  # noqa: E731
        else:
            want = lambda r: r["kind"] == "prog" and r["P"] == prm["P"] and r["d"] == prm["d"] and r["form"] == prm["form"] and r["cls"] == prm["cls"] and r["dd"] == p["k"]  # noqa: E731
        hits = [r for r in recs if want(r) and all(c == "?" or c == p["pt"][i] or (i + 1) in known for i, c in enumerate(r["reading"]))]
        own = [jbest(f"{name}-copy{i + 1}") for i in range(N_PLANT_COPIES)]
        own_bar = max([x for x in own if x is not None], default=None)
        hj = hits[0].get("judge") if hits else None
        desc = {k_: v for k_, v in prm.items() if k_ not in ("pa", "ca", "ka")}
        plant_out.append({"kind": p["kind"], "seed": p["seed"], "params": desc, "k": p["k"], "skip": p["skip"], "slips": p["slips"],
                          "planted_setting_found": bool(hits), "quad": round(hits[0]["quad"], 3) if hits else None, "judge": hj,
                          "own_copies_judge_best": own,
                          "found": bool(hits) and hj is not None and (own_bar is None or hj > own_bar)})
    # ---- K4 against the copies
    copies = [n for n, _ in texts if n.startswith("copy") and n in res]
    k4 = res["K4"]
    copies_j = [jbest(n) for n in copies]
    bar = max([x for x in copies_j if x is not None], default=None)
    k4_above = [r for r in k4["recs"] if r.get("judge") is not None and bar is not None and r["judge"] > bar]
    nchecks = {L: sum(1 for q in kq if q > L) for L in range(1, 97)}
    ca_tab = {}
    for L in range(1, 97):
        ca_tab[str(L)] = {"checks": nchecks[L], "k4": k4["ca_counts"][L], "copies_max": [max(res[n]["ca_counts"][L][d] for n in copies) for d in range(3)],
                          "copies_min": [min(res[n]["ca_counts"][L][d] for n in copies) for d in range(3)],
                          "skip_k4": k4["skip_counts"][L], "skip_copies_max": [max(res[n]["skip_counts"][L][x] for n in copies) for x in range(2)]}
    above_cells = [L for L in range(1, 97) if sum(k4["ca_counts"][L]) > max(sum(res[n]["ca_counts"][L]) for n in copies)]
    null_cells = []
    for n in copies:
        others = [x for x in ["K4"] + copies if x != n]
        null_cells.append(sum(1 for L in range(1, 97) if sum(res[n]["ca_counts"][L]) > max(sum(res[o]["ca_counts"][L]) for o in others)))
    shortest = {n: next((L for L in range(1, 97) if sum(res[n]["ca_counts"][L])), None) for n in ["K4"] + copies}
    shortest_skip = {n: next((L for L in range(1, 97) if sum(res[n]["skip_counts"][L])), None) for n in ["K4"] + copies}
    prog_short = {}
    for n in ["K4"] + copies:
        prog_short[n] = {f: next((P for P in range(1, 53) if sum(res[n]["prog_counts"].get(f"{f}|{P}", [0]))), None) for f in ("per-letter", "per-repeat")}
    cands = []
    for r in sorted(k4["recs"], key=lambda r: (-(r.get("judge") or -1), -r["quad"]))[:20]:
        if r["kind"] != "ca":
            continue
        s_, L, dd, di, e0 = r["h"]
        _, pa, ca_, ka, m = setups[s_]
        pt = "".join(known.get(i + 1, ("A" if c == "?" else c)) for i, c in enumerate(r["reading"]))
        sk = None
        if di >= 0:
            sk = (kq[e0] - 1, L + 1 if di == 0 else L - 1)
        primer = ctx.K4[:max(L, sk[1] if sk else 0) + 1]
        key = {"kind": "ca", "pa": pa, "ca": ca_, "ka": ka, "m": m, "lag": L, "primer": primer,
               "skip_at": sk[0] if sk else None, "skip_lag": sk[1] if sk else None}
        re_ = encrypt(pt, key)
        key["slips"] = [[i + 1, ctx.K4[i]] for i in range(N) if re_[i] != ctx.K4[i]]
        cands.append({"plaintext": pt, "key": key, "key_bits": 4.7 * (L + 1) + 9.3 * len(key["slips"]),
                      "key_description": f"ciphertext autokey lag {L}, {setups[s_][0]}, {dd} slips at known places, skip {sk}; free letters filled with A",
                      "notes": f"judge {r.get('judge')}, quadgram {r['quad']:.3f}"})
    return {
        "candidates": cands[:10],
        "controls": [max([quad(r["reading"]) for r in res[n]["recs"]], default=-9.0) for n in copies],
        "bounds": {
            "family": "ciphertext autokey (union of 0025/0064/0071/0072 tables) and progressive key (0011), 0-2 known letters slipped, or one skipped step (A1.4)",
            "ca_table_setups": len(setups), "ca_lags": "1-96", "skip": "lag L before the e-th known place, L+1 or L-1 from it, e = 2-24, exact fit",
            "prog": "8 table classes, periods 1-52, steps 1-25, per letter and per repeat",
            "slips": f"0-{KMAX} at known places", "readings_judged_when_checks_left": f">= {RMIN}",
            "ca_by_lag": ca_tab, "ca_k4_above_every_copy_lags": above_cells, "ca_copies_above_rest": null_cells,
            "ca_shortest_lag_fitting": shortest, "skip_shortest_lag_fitting": shortest_skip,
            "prog_shortest_period": prog_short,
            "prog_k4_counts": {k_: v for k_, v in k4["prog_counts"].items() if sum(v)},
            "capped_texts": [n for n, v in res.items() if v["capped"]],
            "readings": {"k4": len(k4["recs"]), "copies": [len(res[n]["recs"]) for n in copies]},
            "judge": {"sent": len(order), "none": none_n, "cut": CUT},
            "k4_judge_best": jbest("K4"), "copies_judge_best": copies_j, "k4_readings_above_every_copy": len(k4_above),
            "k4_top": [{"reading": r["reading"], "judge": r.get("judge"), "quad": round(r["quad"], 3),
                        "setting": (setups[r["h"][0]][0], r["h"][1:]) if r["kind"] == "ca" else (r["form"], r["P"], r["d"], r["cls"])}
                       for r in sorted(k4["recs"], key=lambda r: -(r.get("judge") or -1))[:5]],
            "plants": plant_out,
            "slip_cost_bits": {"1": 9.3, "2": 17.5, "skip": 5.6},
            "controls": f"{N_COPIES} shuffled copies (seeds 2130-2149); each plant against {N_PLANT_COPIES} shuffles of its own ciphertext",
            "exhaustive": "yes",
        },
        "notes": (f"{len(setups):,} autokey table setups; K4 shortest fitting lag with <= 2 slips {shortest['K4']}, copies "
                  f"{sorted(v for k_, v in shortest.items() if k_ != 'K4' and v)}; judge sent {len(order)}, K4 best {jbest('K4')}, "
                  f"copies best {bar}; plants found {[p['found'] for p in plant_out]}"),
    }


def worked_example(ctx, key):
    known, ct = ctx.KNOWN, ctx.K4
    L = 9
    lines = [f"ciphertext autokey, lag {L}, KRYPTOS table, Vigenere: the key for each known place is the carved letter {L} before it", "",
             "place  known  key(carved L back)  gives  carved"]
    miss = 0
    for q in sorted(known):
        k = ct[q - L - 1]
        g = encrypt_letter(known[q], k, "kry", "kry", "kry", "vig")
        miss += g != ct[q - 1]
        if q in (22, 23, 24, 25, 64, 65, 66):
            lines.append(f"{q:>5}  {known[q]:>5}  {k:>18}  {g:>5}  {ct[q - 1]:>6}{'' if g == ct[q - 1] else '   x'}")
    lines += ["", f"failed checks: {miss} of 24 (2 allowed as slips)"]
    return "\n".join(lines)
