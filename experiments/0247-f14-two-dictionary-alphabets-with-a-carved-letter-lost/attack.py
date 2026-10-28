"""Experiment 0247. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f14-two-dictionary-alphabets-with-a-carved-letter-lost",
    "title": "F14.5: 0244's two dictionary keyword alphabets and key word, with one carved letter lost (Scheidt's '98 characters'): the 23 distinct places a lost letter changes the key's alignment, every alphabet pair, key lengths 1-26; K4 against 20 shuffles per variant, a planted lost-letter message per variant",
    "family": "14-scheidt-mask-keyed-by-words",
    "parent": "0244-f14-two-dictionary-keyword-alphabets-and-a-key-word",
    "changed": (
        "F14.5 (issue #93). Scheidt, 2005: 'I think there are 98 characters left' (C18(b)); A4, F1.6 and 0086 did this "
        "for earlier key sources. The enciphering ran over 98 letters and one carved letter was lost: the key index of a "
        "carved place at or after the loss is one more than its place. The known words stay where Sanborn put them on "
        "the copper. With a free key only the alignment between known places matters, so a loss before 22 or after 74 "
        "(and a '?' counted before OBKR) changes nothing that 0244 did not test; a loss at 23-34 or 65-74 splits a known "
        "run, and any loss at 35-64 moves BERLINCLOCK's key slots by one against EASTNORTHEAST's: 23 distinct variants. "
        "0244's exact index search and key-word check run unchanged on each, with the key index shifted."
    ),
    "hypothesis_expert": (
        "C18(b) and C17 (Scheidt 2005 '98 characters left'; Sanborn 'whether it's 97, whether it's 100'; K2 lost a letter "
        "for visual balance, 01-facts.md), F14.1's keyed mask (C4(a), C5). A lost letter misaligns the key from that "
        "place on, which can hide a fitting key from every exact test run on the 97 as carved (A1, A4). Pre-registered: "
        "in no variant does K4 match a key word; fitting-pair counts as the copies'. A plant (98-letter Carter, two "
        "random dictionary alphabets, a random dictionary key word of 16-24 letters, one carved letter dropped at the "
        "variant's place) is found when its true alphabets and key word are recovered under its own variant."
    ),
    "hypothesis_eli5": (
        "One of the creators once said there were 98 characters, not 97. If Sanborn dropped one letter when cutting the "
        "copper, as he did in an earlier section, then from that letter on the secret key would be off by one step, and "
        "every exact test so far would have missed it. We rerun the two-scrambled-alphabets test for every place where a "
        "lost letter would change anything."
    ),
    "prediction": "No key word on K4 in any of the 23 variants; fitting pairs at the copies' rate; plants found 23 of 23.",
    "method": (
        "1. Variants: a letter lost at carved place j = 23..34, 35 (standing for 35-64), 65..74; key index of carved "
        "place q is q for q < j and q + 1 from j on. "
        "2. For each variant: 0244's search (208,064 keyword alphabets, every ordered pair matched through the gap index, "
        "key lengths 1-26, both forms; key words of length L from the dictionary and the puzzle, 4 numberings, any shift). "
        "3. K4 and 20 shuffles per variant; one plant per variant (98 letters enciphered, the letter at j dropped). "
        "4. Any K4 key-word match decrypted with its variant and submitted."
    ),
    "walkthrough": (
        "1. Suppose Sanborn enciphered 98 letters and left one out when cutting, say between EASTNORTHEAST and BERLINCLOCK. "
        "2. Then the key letter under each letter of BERLINCLOCK is the one for the next place. "
        "3. Shift BERLINCLOCK's key places by one and rerun the alphabet-pair lookup of 0244. "
        "4. Do the same for a letter lost inside either known word, at each of its places. "
        "5. Compare K4 with shuffles treated the same way, and check that planted messages with a lost letter are found."
    ),
    "expected_minutes": 20,
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
N_COPIES = 20
PLANT_LS = (19, 20, 21, 22, 23, 24)
PLANTS_PER_L = 2
SEED = 247
_G = {}
VARIANTS = list(range(23, 35)) + [35] + list(range(65, 75))


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


def kidx(q, skip):
    """Key index (0-based) of carved place q when a carved letter was lost at place skip (None: none lost)."""
    return q - 1 + (1 if skip is not None and q >= skip else 0)


def slots_of(L, places, skip=None):
    sl = {}
    for q in places:
        sl.setdefault(kidx(q, skip) % L, []).append(q)
    return sl


# ---- the cipher (Quagmire IV with a key word) -------------------------------------------------------
def kvals(key):
    KA = {"std": STD, "kry": KRY, "plain": key["pa"], "cipher": key["ca"]}[key["ka"]]
    w, o, skip = key["word"], key["start"], key.get("lost_at")
    return [(KA.index(w[(kidx(i + 1, skip) + o) % len(w)]) + key["shift"]) % 26 for i in range(N)]


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
def search(text, known, skip=None):
    """-> per (L, form): number of fitting pairs; key-word matches (L <= 24) with their keys."""
    A, pos = _G["A"], _G["pos"]
    places = sorted(known)
    out = {"fits": {}, "matches": [], "full": []}
    ci = np.array([ord(text[q - 1]) - 65 for q in places])
    pi = np.array([ord(known[q]) - 65 for q in places])
    pl_index = {q: e for e, q in enumerate(places)}
    for L in range(1, LCOUNT + 1):
        sl = slots_of(L, places, skip)
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
                    match_key_word(L, form, p_a, c_a, cover, first, text, known, out, skip)
            out["fits"][(L, form)] = n
    return out


def match_key_word(L, form, p_a, c_a, cover, first, text, known, out, skip=None):
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
                                   "shift": int((k[0] - v[h, 0]) % 26), "lost_at": skip})


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
    tid, text, known, skip = args
    return tid, search(text, known, skip)


def key_of(m):
    return {x: m[x] for x in ("pa", "ca", "form", "ka", "word", "start", "shift", "lost_at")}


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
    carter = "".join(c for c in (ROOT / "knowledge" / "sources" / "carter-1923-tomb-of-tutankhamen-vol1.txt").read_text(errors="ignore").upper() if "A" <= c <= "Z")
    texts, plants = [], {}
    for j in VARIANTS:
        texts.append((f"k4@{j}", k4, known, j))
        for i in range(N_COPIES):
            s_ = list(k4); rng.shuffle(s_); texts.append((f"copy{i}@{j}", "".join(s_), known, j))
        # plant: 98 letters enciphered on key indices 0..97, the carved letter at place j dropped
        L = rng.randrange(16, 25)
        strs, src = _G["rots"][L]
        o = rng.randrange(len(carter) // 2, len(carter) - 99)
        pt98 = carter[o:o + 98]
        pa, ca = A[rng.randrange(2, len(A))], A[rng.randrange(2, len(A))]
        w, r = src[rng.randrange(len(src))]
        key = {"pa": pa, "ca": ca, "form": rng.choice(("added", "beaufort")), "ka": rng.choice(("std", "kry", "plain", "cipher")),
               "word": w, "start": r, "shift": rng.randrange(26), "lost_at": None}
        KA = {"std": STD, "kry": KRY, "plain": pa, "cipher": ca}[key["ka"]]
        k98 = [(KA.index(w[(i + r) % L]) + key["shift"]) % 26 for i in range(98)]
        c98 = "".join(ca[(pa.index(ch) + k98[i]) % 26] if key["form"] == "added" else ca[(k98[i] - pa.index(ch)) % 26] for i, ch in enumerate(pt98))
        carved = c98[:j - 1] + c98[j:]
        pk = {q: pt98[kidx(q, j)] for q in known}
        key["lost_at"] = j
        pid = f"plant@{j}"
        plants[pid] = {"j": j, "L": L, "key": key, "carved": carved, "pt98": pt98}
        texts.append((pid, carved, pk, j))
    res = {}
    workers = int(os.environ.get("K4_WORKERS", 8))
    ctx.progress(0, len(texts), "texts searched")
    with mp.get_context("fork").Pool(workers) as pool:
        for tid, out in pool.imap_unordered(_job, texts, chunksize=1):
            res[tid] = out
            ctx.progress(len(res), len(texts), "texts searched")
    text_of = {t[0]: t[1] for t in texts}
    per_variant = {}
    for j in VARIANTS:
        km_k4 = len(res[f"k4@{j}"]["matches"])
        km_cop = [len(res[f"copy{i}@{j}"]["matches"]) for i in range(N_COPIES)]
        above = [f"{L}/{f}" for L in range(1, LCOUNT + 1) for f in ("added", "beaufort")
                 if res[f"k4@{j}"]["fits"][(L, f)] > max(res[f"copy{i}@{j}"]["fits"][(L, f)] for i in range(N_COPIES))]
        first = next((L for L in range(1, LCOUNT + 1) if res[f"k4@{j}"]["fits"][(L, "added")] or res[f"k4@{j}"]["fits"][(L, "beaufort")]), None)
        p = plants[f"plant@{j}"]; k = p["key"]
        found = any(m["L"] == p["L"] and m["form"] == k["form"] and m["pa"] == k["pa"] and m["ca"] == k["ca"] and m["word"] == k["word"]
                    for m in res[f"plant@{j}"]["matches"])
        per_variant[j] = {"k4_key_word_matches": km_k4, "copies_key_word_matches_max": max(km_cop),
                          "k4_first_fitting_length": first, "cells_k4_above_every_copy": above,
                          "plant_found": bool(found), "plant_L": p["L"], "plant_word": k["word"]}
    cands = []
    for j in VARIANTS:
        for m in res[f"k4@{j}"]["matches"][:50]:
            cands.append({"plaintext": decrypt(k4, key_of(m)), "key": key_of(m)})
    from kryptos.scorer import free_text
    controls = []
    for j in VARIANTS:
        for i in range(N_COPIES):
            ms = res[f"copy{i}@{j}"]["matches"]
            if ms:
                controls.append(max(ctx.english_score(free_text(decrypt(text_of[f"copy{i}@{j}"], key_of(m)))) for m in ms[:20]))
    n_above = sum(len(v["cells_k4_above_every_copy"]) for v in per_variant.values())
    bounds = {
        "item": "F14.5 (F14.1's half)", "variants": VARIANTS, "variant_meaning": "a carved letter lost at place j; 35 stands for any place 35-64",
        "alphabets": len(A), "key_lengths": [1, LCOUNT], "copies_per_variant": N_COPIES, "texts": len(texts),
        "per_variant": per_variant, "k4_key_word_matches_total": sum(v["k4_key_word_matches"] for v in per_variant.values()),
        "plants_found": sum(v["plant_found"] for v in per_variant.values()), "plants_total": len(VARIANTS),
        "cells_k4_above_every_copy": n_above, "cells": len(VARIANTS) * LCOUNT * 2,
        "subsumed_by_0244": "a '?' counted before OBKR, or a letter lost before 22 or after 74: every known place shifts alike, which a free key absorbs",
        "exhaustive": True, "compute_seconds": round(time.time() - t0),
    }
    notes = (f"23 lost-letter variants x 4.3e10 alphabet pairs x lengths 1-26: K4 key-word matches {bounds['k4_key_word_matches_total']}; "
             f"cells with K4 above all {N_COPIES} copies {n_above} of {bounds['cells']}; plants found {bounds['plants_found']}/23")
    out = {"candidates": cands, "bounds": bounds, "notes": notes}
    if len(controls) >= 10:
        out["controls"] = controls
    return out


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
