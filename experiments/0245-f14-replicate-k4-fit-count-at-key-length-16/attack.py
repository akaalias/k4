"""Experiment 0245. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f14-replicate-k4-fit-count-at-key-length-16",
    "title": "F14.1 replication: K4's 5 fitting dictionary alphabet pairs at key length 16 (added form) against 1,000 fresh shuffles, counted as pairs and as distinct cipher alphabets",
    "family": "14-scheidt-mask-keyed-by-words",
    "parent": "0244-f14-two-dictionary-keyword-alphabets-and-a-key-word",
    "changed": (
        "Replication only (program.md: a result outside the copies' range is replicated against fresh controls before "
        "anything else). 0244's search unchanged, run at key length 16 alone, both forms, on K4 and 1,000 fresh shuffles "
        "(seed 245). In 0244 K4 had 5 fitting pairs at 16/added, the 50 copies at most 4; the 5 share two cipher alphabets "
        "(AEOLOTROPISM four times), so the count is also taken as distinct cipher alphabets."
    ),
    "hypothesis_expert": (
        "F14.1 (0244): two dictionary keyword alphabets with a free periodic key, exact. One of 52 (length, form) cells "
        "had K4 above all 50 copies in its fit count (5 against 4), with readings below the copies' best by English "
        "(-7.91 against -7.63). Pre-registered: the cell flags only if K4's count is reached by fewer than 5% of 1,000 "
        "fresh shuffles after the 52-cell correction, p < 0.05/52 = 0.00096, on either count."
    ),
    "hypothesis_eli5": (
        "In the last test K4 had slightly more matching alphabet pairs at one key length than any of 50 shuffled copies. "
        "That happens by luck now and then when many lengths are looked at, so we count again on 1,000 new shuffles to "
        "see how unusual it really is."
    ),
    "prediction": "Several percent of fresh shuffles reach 5 or more pairs at 16/added: p well above 0.001, not a flag.",
    "method": (
        "1. 0244's index search at key length 16, both forms, no key-word step needed (16-letter keys are fully forced). "
        "2. K4 and 1,000 fresh shuffles; per text the number of fitting pairs and of distinct cipher alphabets among them. "
        "3. p = (1 + shuffles at or above K4) / 1,001, per count; flag below 0.00096."
    ),
    "walkthrough": (
        "1. Take K4 and shuffle its letters, 1,000 times. "
        "2. For each, file every cipher alphabet by the gaps that key length 16 asks for, and look up every plain alphabet. "
        "3. Count the matching pairs, and the different cipher alphabets among them. "
        "4. See how many shuffles reach K4's counts."
    ),
    "expected_minutes": 10,
}

import os
import random
import sys
import time
import types
from pathlib import Path

import numpy as np

N = 97
ROOT = Path(__file__).resolve().parent
STD = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KRY = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
LMAX, LCOUNT = 24, 26          # key-word checks to 24 (longest dictionary word); 25-26 counted only
N_COPIES = 1000
PLANT_LS = (19, 20, 21, 22, 23, 24)
PLANTS_PER_L = 2
SEED = 245
_G = {}
ONLY_L = (16,)


def keyed(word):
    seen = []
    for c in word:
        if c not in seen:
            seen.append(c)
    return "".join(seen) + "".join(c for c in STD if c not in seen)


def alphabets():
    words = [w.strip().upper() for w in (ROOT / "kryptos" / "data" / "words.txt").read_text().split()]
    alphas = {STD: "std", KRY: "KRYPTOS"}
    for w in words:
        if len(w) >= 4 and w.isalpha():
            alphas.setdefault(keyed(w), w)
    names = list(alphas.values())
    A = list(alphas.keys())
    pos = np.zeros((len(A), 26), dtype=np.int16)          # pos[a, letter] = place of letter in alphabet a
    for i, a in enumerate(A):
        for j, c in enumerate(a):
            pos[i, ord(c) - 65] = j
    return A, names, pos


def key_words(vocabulary):
    words = [w.strip().upper() for w in (ROOT / "kryptos" / "data" / "words.txt").read_text().split()]
    puzzle = sorted({w.upper() for w in vocabulary if w.isalpha()})
    rots = {}
    for w in [x for x in words if x.isalpha() and 3 <= len(x) <= LMAX] + [x for x in puzzle if 2 <= len(x) <= LMAX]:
        s = rots.setdefault(len(w), {})
        for r in range(len(w)):
            s.setdefault(w[r:] + w[:r], (w, r))
    return {L: (list(d.keys()), list(d.values())) for L, d in rots.items()}


def slots_of(L, places):
    sl = {}
    for q in places:
        sl.setdefault((q - 1) % L, []).append(q)
    return sl


# ---- the cipher (Quagmire IV with a key word) -------------------------------------------------------
def kvals(key):
    KA = {"std": STD, "kry": KRY, "plain": key["pa"], "cipher": key["ca"]}[key["ka"]]
    w, o = key["word"], key["start"]
    return [(KA.index(w[(i + o) % len(w)]) + key["shift"]) % 26 for i in range(N)]


def encrypt(plaintext, key):
    PA, CA, k = key["pa"], key["ca"], kvals(key)
    if key["form"] == "added":
        return "".join(CA[(PA.index(p) + k[i]) % 26] for i, p in enumerate(plaintext))
    return "".join(CA[(k[i] - PA.index(p)) % 26] for i, p in enumerate(plaintext))


def decrypt(ct, key):
    PA, CA, k = key["pa"], key["ca"], kvals(key)
    if key["form"] == "added":
        return "".join(PA[(CA.index(c) - k[i]) % 26] for i, c in enumerate(ct))
    return "".join(PA[(k[i] - CA.index(c)) % 26] for i, c in enumerate(ct))


# ---- the search --------------------------------------------------------------------------------------
def search(text, known):
    """-> per (L, form): number of fitting pairs; key-word matches (L <= 24) with their keys."""
    A, pos = _G["A"], _G["pos"]
    places = sorted(known)
    out = {"fits": {}, "matches": [], "full": []}
    ci = np.array([ord(text[q - 1]) - 65 for q in places])
    pi = np.array([ord(known[q]) - 65 for q in places])
    pl_index = {q: e for e, q in enumerate(places)}
    for L in ONLY_L:
        sl = slots_of(L, places)
        pairs = [(v[0], u) for v in sl.values() for u in v[1:]]
        a_idx = np.array([pl_index[x] for x, _ in pairs], dtype=int)
        b_idx = np.array([pl_index[y] for _, y in pairs], dtype=int)
        cvec = (pos[:, ci[a_idx]] - pos[:, ci[b_idx]]) % 26
        pvec = (pos[:, pi[a_idx]] - pos[:, pi[b_idx]]) % 26
        cidx = {}
        for a, kb in enumerate(r.tobytes() for r in cvec.astype(np.uint8)):
            cidx.setdefault(kb, []).append(a)
        cover = sorted(sl)
        first = {s: sl[s][0] for s in cover}
        for form in ("added", "beaufort"):
            pv = pvec if form == "added" else (-pvec) % 26
            pk = [r.tobytes() for r in pv.astype(np.uint8)]
            if L > LMAX:
                out["fits"][(L, form)] = int(sum(len(cidx.get(kb, ())) for kb in pk))   # counts only
                continue
            n = 0
            for p_a, kb in enumerate(pk):
                partners = cidx.get(kb)
                if not partners:
                    continue
                n += len(partners)
                for c_a in partners:
                    match_key_word(L, form, p_a, c_a, cover, first, text, known, out)
                    if len(cover) == L and len(out["full"]) < 400:
                        out["full"].append(full_reading(L, form, p_a, c_a, cover, first, text, known))
            out["fits"][(L, form)] = n
    return out


def match_key_word(L, form, p_a, c_a, cover, first, text, known, out):
    """Forced key value per covered slot; does any word rotation of length L give it, up to a shift?"""
    if L not in _G["rots"]:
        return
    A, pos = _G["A"], _G["pos"]
    k = []
    for s in cover:
        q = first[s]
        c, p = int(pos[c_a, ord(text[q - 1]) - 65]), int(pos[p_a, ord(known[q]) - 65])
        k.append((c - p) % 26 if form == "added" else (c + p) % 26)
    k = np.array(k)
    d = (k - k[0]) % 26
    strs, src = _G["rots"][L]
    sub = _G["rotmat"][L][:, cover]
    for ka in ("std", "kry", "plain", "cipher"):
        lut = {"std": _G["lut_std"], "kry": _G["lut_kry"], "plain": pos[p_a], "cipher": pos[c_a]}[ka]
        v = lut[sub]
        dv = (v - v[:, :1]) % 26
        for h in np.nonzero((dv == d).all(axis=1))[0][:20]:
            w, r = src[h]
            out["matches"].append({"L": L, "form": form, "pa": A[p_a], "ca": A[c_a], "pa_word": _G["names"][p_a],
                                   "ca_word": _G["names"][c_a], "ka": ka, "word": w, "start": r,
                                   "shift": int((k[0] - v[h, 0]) % 26)})


def full_reading(L, form, p_a, c_a, cover, first, text, known):
    """Every key slot holds a known place: the pair fixes the key (in standard numbering) and so the whole reading."""
    A, pos = _G["A"], _G["pos"]
    kv = [0] * L
    for s in cover:
        q = first[s]
        c, p = int(pos[c_a, ord(text[q - 1]) - 65]), int(pos[p_a, ord(known[q]) - 65])
        kv[s] = (c - p) % 26 if form == "added" else (c + p) % 26
    key = {"pa": A[p_a], "ca": A[c_a], "form": form, "ka": "std", "word": "".join(STD[v] for v in kv), "start": 0, "shift": 0,
           "pa_word": _G["names"][p_a], "ca_word": _G["names"][c_a]}
    return {"L": L, "key": key, "reading": decrypt(text, key)}


def _job(args):
    tid, text, known = args
    return tid, search(text, known)


def key_of(m):
    return {x: m[x] for x in ("pa", "ca", "form", "ka", "word", "start", "shift")}


def run(ctx):
    import multiprocessing as mp
    t0 = time.time()
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    A, names, pos = alphabets()
    _G.update(A=A, names=names, pos=pos, rots=key_words(ctx.vocabulary))
    _G["rotmat"] = {L: np.array([[ord(c) - 65 for c in s] for s in strs], dtype=np.int16) for L, (strs, _) in _G["rots"].items()}
    _G["lut_std"] = np.arange(26, dtype=np.int16)
    _G["lut_kry"] = np.array([KRY.index(c) for c in STD], dtype=np.int16)
    k4, known = ctx.K4, ctx.KNOWN
    rng = random.Random(SEED)
    texts = [("k4", k4, known)]
    for i in range(N_COPIES):
        s = list(k4); rng.shuffle(s); texts.append((f"copy{i}", "".join(s), known))
    res = {}
    workers = int(os.environ.get("K4_WORKERS", 8))
    ctx.progress(0, len(texts), "texts searched")
    with mp.get_context("fork").Pool(workers) as pool:
        for tid, out in pool.imap_unordered(_job, texts, chunksize=4):
            res[tid] = out
            ctx.progress(len(res), len(texts), "texts searched")

    def counts(tid, form):
        fl = [f for f in res[tid]["full"] if f["key"]["form"] == form]
        return res[tid]["fits"][(16, form)], len({f["key"]["ca"] for f in fl})
    out = {}
    for form in ("added", "beaufort"):
        kp, kc = counts("k4", form)
        cp = [counts(f"copy{i}", form) for i in range(N_COPIES)]
        out[form] = {"k4_pairs": kp, "k4_distinct_cipher_alphabets": kc,
                     "p_pairs": round((1 + sum(1 for x in cp if x[0] >= kp)) / (N_COPIES + 1), 5),
                     "p_distinct": round((1 + sum(1 for x in cp if x[1] >= kc)) / (N_COPIES + 1), 5),
                     "copies_with_any": sum(1 for x in cp if x[0]), "copies_max_pairs": max(x[0] for x in cp),
                     "copies_pairs_histogram": {str(v): sum(1 for x in cp if x[0] == v) for v in sorted({x[0] for x in cp})}}
    alpha = 0.05 / 52
    flag = out["added"]["p_pairs"] < alpha and out["added"]["p_distinct"] < alpha
    from kryptos.scorer import free_text
    cands = [{"plaintext": f["reading"], "key": {x: f["key"][x] for x in ("pa", "ca", "form", "ka", "word", "start", "shift")}} for f in res["k4"]["full"]]
    controls = []
    for i in range(N_COPIES):
        sc = [ctx.english_score(free_text(f["reading"])) for f in res[f"copy{i}"]["full"]]
        if sc:
            controls.append(max(sc))
    bounds = {"item": "F14.1 replication", "key_length": 16, "copies": N_COPIES, "seed": SEED, "alpha_corrected": round(alpha, 6),
              "cells": out, "flag": flag, "alphabets": len(A), "compute_seconds": round(time.time() - t0),
              "k4_readings": [[f["key"]["pa_word"], f["key"]["ca_word"], f["reading"]] for f in res["k4"]["full"]]}
    notes = (f"16/added: K4 {out['added']['k4_pairs']} pairs ({out['added']['k4_distinct_cipher_alphabets']} cipher alphabets), "
             f"p {out['added']['p_pairs']} / {out['added']['p_distinct']} against {N_COPIES} fresh shuffles; flag {flag}")
    return {"candidates": cands, "bounds": bounds, "notes": notes, "controls": controls}


def worked_example(ctx, key):
    known, ct = ctx.KNOWN, ctx.K4
    L = 19
    sl = slots_of(L, sorted(known))
    lines = [f"Key length {L}: known places in the same key slot, and what they ask of the two alphabets (added form)", "",
             "places   known  carved   the gap on the cipher alphabet must equal the gap on the plain alphabet"]
    for s, v in sorted(sl.items()):
        for u in v[1:]:
            lines.append(f"{v[0]:>3},{u:<3}   {known[v[0]]}{known[u]}     {ct[v[0] - 1]}{ct[u - 1]}       gap({ct[v[0] - 1]} to {ct[u - 1]}) on the cipher alphabet = gap({known[v[0]]} to {known[u]}) on the plain alphabet")
    lines += ["", "Every cipher alphabet is filed by its gaps; every plain alphabet looks up the gaps it needs."]
    return "\n".join(lines)
