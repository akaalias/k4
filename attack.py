"""Experiment 0214. See program.md for the contract."""

EXPERIMENT = {
    "slug": "a-move-then-the-table-with-two-slips",
    "title": "A1.5: a move, then the table (and the reverse), over every dictionary-keyed columnar, Myszkowski, double columnar, rail fence, AMSCO and type-1 route, with a repeating key of length 1-26 on the sculpture's tables and up to two of the 24 known letters carved wrong; exact, judged against scrambled copies, with planted slipped messages",
    "family": "6-transposition-then-tableau",
    "parent": "0110-keyword-columnar-from-the-whole-dictionary",
    "changed": (
        "A1.5 (Stage 2, step 2, issue #76). 0110-0114 and the type-1 library (0080-0129) required all 24 known letters to "
        "agree with one repeating key after or before the move (nothing below key length 21-22). k = 1 was run as 'one "
        "carved letter wrong' (0093); slipped columns are F6.21. Here k = 2: the union of 0110's keyword columnar, 0111's "
        "Myszkowski, 0112's double columnar, 0113's rail fence and redefence, 0114's AMSCO (all from the whole dictionary) "
        "and 0129's type-1 library, deduplicated by where the known letters land, both orders, 8 table classes, key lengths "
        "1-26, compiled with an exact early exit; K4 against 20 scrambled copies; readings that keep 3 or more checks "
        "to quadgrams and the blind judge; three planted messages with two slips each."
    ),
    "hypothesis_expert": (
        "C1(a) (Sanborn, CNN 2005: 'I used a matrix code... double matrixes and triple matrixes... then went back to this "
        "table'), C11 ('the other 91 characters and their proper order'), A1 (knowledge/12-assumptions.md), C27(a). Model: "
        "a transposition w (message place i to carved place w(i)) and a periodic key k of length L on the table, plain and "
        "cipher alphabets standard or KRYPTOS, added or Beaufort form (8 classes; the key alphabet drops out). Order A, move "
        "then table: the key runs along the carved places, slot w(q) mod L; order B, table then move: slot q mod L, carved "
        "letter at w(q). Each known letter forces a key value in its slot; the least number of slips is 24 minus the sum "
        "over slots of the most common forced value's count, at most 2 here (17.5 bits to name). Cost estimated before the "
        "run: about 1.8 million route maps x 2 orders x 8 classes x 26 lengths per text, compiled. Statistic: per order "
        "and length, the number of (route, class) cells with 0, 1, 2 slips, K4 against each copy; the shortest length that "
        "fits; the judge's best on readings keeping 3 or more checks."
    ),
    "hypothesis_eli5": (
        "Sanborn described writing the message into a grid, reading it out in another order, and then using the table with "
        "a key word. Experiments 110-114 tried every such grid keyed by any dictionary word, before and after the table, and "
        "found nothing with all 24 known letters right. If he slipped at two of those places, that test would have missed "
        "it. Here we allow two wrong, on the carving and on scrambled copies, and hide three messages of our own made that "
        "way, slips included, to check the search finds them."
    ),
    "prediction": (
        "With two slips the shortest key length that fits K4 drops from 21-22 to about 17-19, as on the copies; K4 above "
        "every copy in no more (order, length) cells than a copy is above the rest; nothing judged above every copy. The "
        "three plants are found. Zero candidates pass gate 4."
    ),
    "method": (
        "1. Build every route map of 0110-0114 and the type-1 library; keep one per distinct landing of the 24 known "
        "places. 2. Compiled: for each route, class, order and key length, add the known places one by one into their slots "
        "and count slips (a place whose forced value is not its slot's most common so far); stop at 3. 3. Count cells by "
        "slips, K4 and 20 copies. 4. For cells keeping 3 or more checks, enumerate the key choices and read; each text's top "
        "5 by quadgrams and every reading at or above -5.0 go to the judge in one call. 5. Plants and their own copies "
        "through the same search."
    ),
    "walkthrough": (
        "1. Write the message into a grid under a key word and read the columns out in the word's order. "
        "2. Choose a key length, say 11, and a table; each known letter now sits at a new carved place, and its key letter is read off the table from the carved letter. "
        "3. Known letters in the same slot of the key must give the same key letter. "
        "4. Count how many would have to be slips; keep the setting if 2 or fewer. "
        "5. Read the message back through the key and the grid, and do the same on scrambled copies of the carving."
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

from kryptos.alphabets import decrypt_letter, encrypt_letter, key_letter_for
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
ROOT = Path(__file__).resolve().parent
if not (ROOT / "experiments").exists():
    ROOT = Path.cwd()
PMAX = 26
KMAX = 2
RMIN = 3
CUT = -5.0
TOPJ = 5
N_COPIES = 20
N_PLANT_COPIES = 5
CLASSES = [(pa, ca, m) for pa in ("std", "kry") for ca in ("std", "kry") for m in ("vig", "beau")]
AL = {"std": STD, "kry": KRY}


def _load(prefix):
    d = sorted((ROOT / "experiments").glob(prefix + "-*"))[0]
    spec = importlib.util.spec_from_file_location(f"exp{prefix}", d / "attack.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def route_maps(vocab):
    """Yield (family, name, where) for 0110-0114's route sets and 0129's type-1 library, forward and inverse."""
    m110, m111, m113, m114, m129 = _load("0110"), _load("0111"), _load("0113"), _load("0114"), _load("0129")
    words = [w.strip().upper() for w in (ROOT / "kryptos" / "data" / "words.txt").read_text().split()]

    def both(fam, name, wh):
        inv = [0] * N
        for i, j in enumerate(wh):
            inv[j] = i
        yield fam, name, wh
        yield fam, name + " inverse", inv
    seqs = {}
    for w in words:
        if 2 <= len(w) <= 30 and w.isalpha():
            for s in (tuple(m110.keyword_sequence(w)), tuple(m110.full_sequence(w))):
                if len(s) >= 2 and s not in seqs and s != tuple(range(len(s))):
                    seqs[s] = w
    for s, w in seqs.items():
        wh = m110.where_columnar(s)
        yield from both("0110 keyword columnar", w, wh)
        yield from both("0112 double columnar", w, [wh[wh[i]] for i in range(N)])
    mys = {}
    for w in words:
        if 3 <= len(w) <= 30 and w.isalpha() and len(set(w)) < len(w):
            mys.setdefault(m111.myszkowski_key(w), w)
    for s, w in mys.items():
        yield from both("0111 Myszkowski", w, m111.where_myszkowski(s))
    for r in range(2, 49):
        for off in range(2 * r - 2):
            orders = itertools.permutations(range(r)) if r <= 6 else [tuple(range(r)), tuple(range(r))[::-1]]
            for order in orders:
                yield from both("0113 rail fence", f"{r} rails offset {off} order {order}", m113.where_rails(r, off, order))
    am = {}
    for w in words:
        if 3 <= len(w) <= 30 and w.isalpha():
            for s in (tuple(m110.keyword_sequence(w)), tuple(m110.full_sequence(w))):
                if 3 <= len(s) <= 15:
                    for first in (1, 2):
                        am.setdefault((s, first), w)
    for (s, first), w in am.items():
        yield from both("0114 AMSCO", f"{w} first {first}", m114.where_amsco(s, first))
    for name, wh in m129.route_library(vocab):
        yield "type-1 library", name, list(wh)


C_SRC = r"""
static int md(int x){ x%=26; return x<0?x+26:x; }
/* lands: nr x 24 carved places (0-based) of the known letters; text 97 letters;
   pidx[24] message places (0-based); P[2][24] plain index of each known letter in std / kry; C[2][26] letter -> index.
   counts[2 orders][27 lengths][3 slips] summed over routes and classes; hits (route, class, order, L, d). */
long run_mv(int nr,const int*lands,const int*text,const int*pidx,const int*P,const int*C,int rmin,
            long*counts,long maxh,int*hits){
  long nh=0; int f[24]; int cnt[27*26]; int mm[27]; int seen[27];
  for(int r=0;r<nr;r++){ const int*land=lands+24*r;
    for(int c=0;c<8;c++){ int pa=c>>2, ca=(c>>1)&1, beau=c&1;
      for(int e=0;e<24;e++){ int cv=C[ca*26+text[land[e]]], pv=P[pa*24+e]; f[e]= beau? md(cv+pv) : md(cv-pv); }
      for(int o=0;o<2;o++){
        for(int L=1;L<=26;L++){
          int d=0,nslots=0;
          for(int s=0;s<L;s++){ mm[s]=0; seen[s]=0; }
          for(int e=0;e<24;e++){ int pos=o==0?land[e]:pidx[e]; int s=pos%L; int idx=s*26+f[e];
            if(!seen[s]){ seen[s]=1; nslots++; for(int v=0;v<26;v++) cnt[s*26+v]=0; }
            cnt[idx]++; if(cnt[idx]>mm[s]) mm[s]=cnt[idx]; else { d++; if(d>2) break; } }
          if(d<=2){ counts[(o*27+L)*3+d]++; int checks=24-nslots;
            if(checks-d>=rmin && nh<maxh){ int*h=hits+5*nh; h[0]=r;h[1]=c;h[2]=o;h[3]=L;h[4]=d; nh++; } } } } } }
  return nh; }
"""
_LIB = None
_KEEP = []


def lib():
    global _LIB
    if _LIB is None:
        d = tempfile.mkdtemp(prefix="k4_mv_")
        src, so = os.path.join(d, "mv.c"), os.path.join(d, "mv.so")
        Path(src).write_text(C_SRC)
        subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", so, src], check=True, capture_output=True)
        _LIB = ctypes.CDLL(so)
        P_, ci, cl = ctypes.POINTER, ctypes.c_int, ctypes.c_long
        _LIB.run_mv.restype = cl
        _LIB.run_mv.argtypes = [ci, P_(ci), P_(ci), P_(ci), P_(ci), P_(ci), ci, P_(cl), cl, P_(ci)]
    return _LIB


def I(a):
    buf = array("i", a)
    _KEEP.append(buf)
    return (ctypes.c_int * len(buf)).from_buffer(buf)


_STATE = {}


def settings_for(text, known, where, cls, o, L, kmax):
    """Key choices for one cell with at most kmax slips (as 0207's enumeration)."""
    pa, ca, m = cls
    slots = {}
    for q in sorted(known):
        j = where[q - 1]
        v = STD.index(key_letter_for(known[q], text[j], pa, ca, "std", m))
        slots.setdefault((j if o == 0 else q - 1) % L, []).append((q, v))
    opts = [(s, [(v, [q for q, w in eqs if w != v]) for v in sorted({w for _, w in eqs})]) for s, eqs in sorted(slots.items())]
    out = []

    def dfs(k, d, key, sl):
        if k == len(opts):
            out.append((d, dict(key), list(sl))); return
        s, ch = opts[k]
        for v, bad in ch:
            if d + len(bad) <= kmax:
                key[s] = v
                dfs(k + 1, d + len(bad), key, sl + bad)
        key.pop(s, None)
    dfs(0, 0, {}, [])
    return out


def reading(text, where, cls, o, L, key):
    pa, ca, m = cls
    out = []
    for i in range(N):
        j = where[i]
        s = (j if o == 0 else i) % L
        out.append(decrypt_letter(text[j], STD[key[s]], pa, ca, "std", m) if s in key else "?")
    return "".join(out)


def one_text(t):
    lands, routes, known = _STATE["lands"], _STATE["routes"], _STATE["known"]
    kq = sorted(known)
    P = [STD.index(known[q]) for q in kq] + [KRY.index(known[q]) for q in kq]
    C = [STD.index(c) for c in STD] + [KRY.index(c) for c in STD]
    cl = ctypes.c_long
    counts = (cl * (2 * 27 * 3))()
    maxh = 300000
    hits = (ctypes.c_int * (5 * maxh))()
    nh = lib().run_mv(len(routes), lands, I([ord(c) - 65 for c in t]), I([q - 1 for q in kq]), I(P), I(C), RMIN, counts, maxh, hits)
    recs = []
    for i in range(nh):
        r, c, o, L, d = (hits[5 * i + k] for k in range(5))
        where = routes[r][2]
        for dd, key, sl in settings_for(t, known, where, CLASSES[c], o, L, KMAX):
            if dd == d:
                recs.append({"r": r, "c": c, "o": o, "L": L, "d": d, "key": key, "slips": sl, "reading": reading(t, where, CLASSES[c], o, L, key)})
    cnt = {o: {L: [counts[(o * 27 + L) * 3 + d] for d in range(3)] for L in range(1, 27)} for o in (0, 1)}
    return {"counts": cnt, "recs": recs, "capped": nh >= maxh}


def mv_encrypt(pt, where, cls, o, key):
    pa, ca, m = cls
    L = len(key)
    if o == 0:
        moved = [""] * N
        for i in range(N):
            moved[where[i]] = pt[i]
        return "".join(encrypt_letter(moved[j], key[j % L], pa, ca, "std", m) for j in range(N))
    out = [""] * N
    for i in range(N):
        out[where[i]] = encrypt_letter(pt[i], key[i % L], pa, ca, "std", m)
    return "".join(out)


def encrypt(plaintext, key):
    out = list(mv_encrypt(plaintext, key["where"], tuple(key["cls"]), key["order"], key["key"]))
    for q, ch in key.get("slips", []):
        out[q - 1] = ch
    return "".join(out)


def shuffled(text, seed):
    l_ = list(text)
    random.Random(seed).shuffle(l_)
    return "".join(l_)


def run(ctx):
    from kryptos.plants import english_plant
    known = ctx.KNOWN
    kq = sorted(known)
    routes, seen, fams = [], set(), {}
    lands = array("i")
    for fam, name, wh in route_maps(ctx.vocabulary):
        land = tuple(wh[q - 1] for q in kq)
        fams[fam] = fams.get(fam, 0) + 1
        if land in seen:
            continue
        seen.add(land)
        routes.append((fam, name, wh))
        lands.extend(land)
    _KEEP.append(lands)
    _STATE["lands"] = (ctypes.c_int * len(lands)).from_buffer(lands)
    _STATE["routes"], _STATE["known"] = routes, known
    by_name = {(f, n): i for i, (f, n, _) in enumerate(routes)}
    # plants: route, class, order, key length, two slips at checked known places
    plants = []
    specs = [(2141, "0110 keyword columnar", 11, ("kry", "kry", "vig"), 0),
             (2142, "0114 AMSCO", 9, ("std", "kry", "beau"), 1),
             (2143, "0113 rail fence", 13, ("kry", "std", "vig"), 0)]
    for seed, fam, L, cls, o in specs:
        rng = random.Random(seed)
        cand = [i for i, (f, n, _) in enumerate(routes) if f == fam]
        r = cand[rng.randrange(len(cand))]
        where = routes[r][2]
        pt = english_plant(seed)
        key = "".join(rng.choice(STD) for _ in range(L))
        ct = list(mv_encrypt(pt, where, cls, o, key))
        slots = {}
        for q in kq:
            slots.setdefault((where[q - 1] if o == 0 else q - 1) % L, []).append(q)
        checked = [q for s_, qs in slots.items() if len(qs) >= 2 for q in qs]
        places = sorted(rng.sample(checked, 2))
        for q in places:
            j = where[q - 1]
            ct[j] = rng.choice([x for x in STD if x != ct[j]])
        plants.append({"seed": seed, "r": r, "route": f"{fam}: {routes[r][1]}", "L": L, "cls": cls, "o": o, "slips": places, "pt": pt, "ct": "".join(ct)})
    texts = []
    for j, p in enumerate(plants):
        texts.append((f"plant{j + 1}", p["ct"]))
        texts += [(f"plant{j + 1}-copy{i + 1}", shuffled(p["ct"], p["seed"] * 100 + i)) for i in range(N_PLANT_COPIES)]
    texts.append(("K4", ctx.K4))
    texts += [(f"copy{i + 1}", shuffled(ctx.K4, 2150 + i)) for i in range(N_COPIES)]
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
        good = [r for r in res[name]["recs"] if r["r"] == p["r"] and CLASSES[r["c"]] == p["cls"] and r["o"] == p["o"] and r["L"] == p["L"]
                and all(c == "?" or c == p["pt"][i] or (i + 1) in known for i, c in enumerate(r["reading"]))]
        best = max(good, key=lambda r: (r.get("judge") or -1)) if good else None
        own = [jbest(f"{name}-copy{i + 1}") for i in range(N_PLANT_COPIES)]
        own_bar = max([x for x in own if x is not None], default=None)
        hj = best.get("judge") if best else None
        plant_out.append({"seed": p["seed"], "route": p["route"], "L": p["L"], "cls": "/".join(p["cls"]), "order": "AB"[p["o"]], "slips": p["slips"],
                          "planted_setting_found": bool(good), "slips_named": best["slips"] if best else None,
                          "quad": round(best["quad"], 3) if best else None, "judge": hj, "own_copies_judge_best": own,
                          "found": bool(best) and hj is not None and (own_bar is None or hj > own_bar)})
    copies = [n for n, _ in texts if n.startswith("copy") and n in res]
    k4 = res["K4"]
    copies_j = [jbest(n) for n in copies]
    bar = max([x for x in copies_j if x is not None], default=None)
    by = {}
    for o in (0, 1):
        for L in range(1, 27):
            by[f"{'AB'[o]}{L}"] = {"k4": k4["counts"][o][L], "copies_min": [min(res[n]["counts"][o][L][d] for n in copies) for d in range(3)],
                                    "copies_max": [max(res[n]["counts"][o][L][d] for n in copies) for d in range(3)]}
    tot = lambda n, o, L: sum(res[n]["counts"][o][L])  # noqa: E731
    above = [f"{'AB'[o]}{L}" for o in (0, 1) for L in range(1, 27) if tot("K4", o, L) > max(tot(n, o, L) for n in copies)]
    null = [sum(1 for o in (0, 1) for L in range(1, 27) if tot(n, o, L) > max(tot(x, o, L) for x in ["K4"] + copies if x != n)) for n in copies]
    shortest = {n: {"AB"[o]: [next((L for L in range(1, 27) if sum(res[n]["counts"][o][L][:d + 1])), None) for d in range(3)] for o in (0, 1)} for n in ["K4"] + copies}
    cands = []
    for r in sorted(k4["recs"], key=lambda r: (-(r.get("judge") or -1), -r["quad"]))[:10]:
        where = routes[r["r"]][2]
        L = r["L"]
        key = "".join(STD[r["key"].get(s, 0)] for s in range(L))
        pt = reading(ctx.K4, where, CLASSES[r["c"]], r["o"], L, {s: STD.index(key[s]) for s in range(L)})
        pt = "".join(known.get(i + 1, ch) for i, ch in enumerate(pt))
        kd = {"where": where, "cls": CLASSES[r["c"]], "order": r["o"], "key": key}
        re_ = encrypt(pt, kd)
        kd["slips"] = [[i + 1, ctx.K4[i]] for i in range(N) if re_[i] != ctx.K4[i]]
        cands.append({"plaintext": pt, "key": kd, "key_bits": 4.7 * L + 20 + 9.3 * len(kd["slips"]),
                      "key_description": f"{routes[r['r']][0]}: {routes[r['r']][1]}, order {'AB'[r['o']]}, key length {L}, {'/'.join(CLASSES[r['c']])}, slips {r['slips']}; open slots filled with A",
                      "notes": f"judge {r.get('judge')}, quadgram {r['quad']:.3f}"})
    return {
        "candidates": cands,
        "controls": [max([r["quad"] for r in res[n]["recs"]], default=-9.0) for n in copies],
        "bounds": {
            "family": "a move then the table and the reverse, 0110-0114 and the type-1 library, periodic key 1-26 on 8 table classes, 0-2 known letters slipped (A1.5)",
            "route_maps_by_family": fams, "distinct_landings": len(routes), "orders": "A move then table, B table then move",
            "classes": 8, "key_lengths": "1-26", "slips": "0-2 at the known places",
            "by_order_and_length": by, "k4_above_every_copy": above, "copies_above_rest": null,
            "shortest_length_by_slips": shortest,
            "readings": {"k4": len(k4["recs"]), "copies": [len(res[n]["recs"]) for n in copies]},
            "capped": [n for n, v in res.items() if v["capped"]],
            "judge": {"sent": len(order), "none": sum(1 for v in verdicts.values() if v["score"] is None), "cut": CUT,
                      "rule": f"each text's top {TOPJ} readings by quadgrams and every reading at or above {CUT}; one call"},
            "k4_judge_best": jbest("K4"), "copies_judge_best": copies_j,
            "k4_readings_above_every_copy": sum(1 for r in k4["recs"] if r.get("judge") is not None and bar is not None and r["judge"] > bar),
            "k4_top": [{"reading": r["reading"], "judge": r.get("judge"), "quad": round(r["quad"], 3), "route": f"{routes[r['r']][0]}: {routes[r['r']][1]}",
                        "order": "AB"[r["o"]], "L": r["L"], "class": "/".join(CLASSES[r["c"]])} for r in sorted(k4["recs"], key=lambda r: -(r.get("judge") or -1))[:5]],
            "plants": plant_out,
            "slip_cost_bits": {"2": 17.5},
            "controls": f"{N_COPIES} shuffled copies (seeds 2150-2169); each plant against {N_PLANT_COPIES} shuffles of its own ciphertext",
            "exhaustive": "yes",
        },
        "notes": (f"{len(routes):,} distinct landings; K4 shortest length with <= 2 slips A {shortest['K4']['A'][2]}, B {shortest['K4']['B'][2]}; "
                  f"K4 above every copy in {len(above)} cells (copies {min(null)}-{max(null)}); judge sent {len(order)}, K4 best {jbest('K4')}, copies best {bar}; "
                  f"plants found {[p['found'] for p in plant_out]}"),
    }


def worked_example(ctx, key):
    m110 = _load("0110")
    seq = m110.keyword_sequence("PYRAMID")
    where = m110.where_columnar(seq)
    L, cls = 11, ("kry", "kry", "vig")
    lines = [f"keyword columnar PYRAMID (move first), then the KRYPTOS table, key length {L}: key letter forced at each known place", ""]
    slots = {}
    for q in sorted(ctx.KNOWN):
        j = where[q - 1]
        k = key_letter_for(ctx.KNOWN[q], ctx.K4[j], "kry", "kry", "std", "vig")
        slots.setdefault(j % L, []).append(f"{q}{ctx.KNOWN[q]}@{j + 1}:{k}")
    need = 0
    for s in sorted(slots):
        ks = [x[-1] for x in slots[s]]
        need += len(ks) - max(ks.count(v) for v in set(ks))
        lines.append(f"  slot {s:>2}: " + "  ".join(slots[s]))
    lines += ["", f"slips needed: {need} (2 allowed)"]
    return "\n".join(lines)
