"""Experiment 0244. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f14-two-dictionary-keyword-alphabets-and-a-key-word",
    "title": "F14.1: two different keyword alphabets from the whole dictionary, one on each side of the table, with a repeating key (free, then a key word): every pair of 208,064 alphabets matched exactly through an index, key lengths 1-26, both forms; K4 against 50 shuffles, plants at six lengths",
    "family": "14-scheidt-mask-keyed-by-words",
    "parent": "0109-keyword-tables-from-the-whole-dictionary",
    "changed": (
        "F14.1 (issue #93), the first F14 item. 0109 put one dictionary keyword alphabet on both sides (or one side with "
        "the standard or KRYPTOS alphabet); 0020 paired the 248 puzzle words. Here the plain and cipher alphabets are any "
        "two of the 208,062 dictionary keyword alphabets plus standard and KRYPTOS (4.3 x 10^10 ordered pairs). At key "
        "length L the 24 known letters give checks only between places in the same key slot, and each check splits into a "
        "cipher-side difference (the cipher alphabet's places of the two carved letters) and a plain-side one (the plain "
        "alphabet's places of the two known letters), so every cipher alphabet is indexed by its difference vector and "
        "every plain alphabet looked up: all pairs in about 0.4 million lookups per length and form, exactly. Where pairs "
        "fit, the key letters the known letters force are checked against every dictionary and puzzle word of length L, "
        "every start, key letters numbered on the standard, KRYPTOS, plain or cipher alphabet with any indicator shift."
    ),
    "hypothesis_expert": (
        "Scheidt's mask in its keyed form (C4(a), C5; 03-scheidt-said.md: 'I masked the English language', 'executed "
        "with the correct key word/s', 'building layers... mix and match'): a keyword monoalphabetic substitution before "
        "a keyed tableau, which is one Quagmire IV (plain alphabet = the mask's keyword alphabet, cipher alphabet = the "
        "table's). With free alphabets this is F1.2, consistent at lengths 8, 13, 16, 19, 20, 23, 24, 26 at the copies' "
        "rate (0123, 0124; prior-attempts database: 'satisfiable at random-text rates'), and 0136's bound leaves it to "
        "English. Two keyword alphabets are about 35 bits, not 176, so the known letters decide them: expected chance "
        "fits per form, 4.3 x 10^10 / 26^c with c same-slot checks, are under 0.01 at every length to 22, 5 at 23, 3,600 at "
        "24 (where a key word of 24 letters, 5 in the dictionary, decides), and 2.5 x 10^6 and 1.7 x 10^9 at 25 and 26 "
        "(no dictionary word that long: counted only). Pre-registered: K4 fits no pair at 1-22 or matches no key word at "
        "23-24 beyond the copies' counts; a plant (two random dictionary alphabets and a random dictionary key word) is "
        "found when its true pair fits and its key word is recovered."
    ),
    "hypothesis_eli5": (
        "Scheidt said he first disguised the English, then used the table. A simple way to do both by hand: scramble the "
        "alphabet with one secret word, and set the table's other alphabet with a second word, then use a repeating key "
        "word. That is two scrambled alphabets, which earlier tests left open because there are too many to try one by "
        "one. But if each scrambled alphabet comes from an English word, there are only about 200,000 of each, and the "
        "clue words tell us, for each key length, a few facts that link the two. We file every alphabet by those facts so "
        "that matching pairs fall out of a lookup, then check whether the key the clues force is an English word."
    ),
    "prediction": (
        "K4 fits no alphabet pair at lengths 1-22 (copies: none or almost none); at 23 a handful of pairs on K4 and copies "
        "alike, none with a key word; at 24 thousands of pairs on both, none with a dictionary key word; 25-26 counted, as "
        "the copies. Plants found at every planted length (19, 20, 21, 22, 23, 24). Zero candidates."
    ),
    "method": (
        "1. Alphabets: the keyword-mixed alphabet of every dictionary word of 4+ letters (0109's 208,062 distinct), plus "
        "standard and KRYPTOS. "
        "2. For each text, key length L = 1-26 and form (added: c = CA[p + k]; Beaufort: c = CA[k - p]): the same-slot "
        "pairs of known places; each cipher alphabet's vector of place differences of the carved letters, indexed; each "
        "plain alphabet's vector of the known letters' differences (negated for Beaufort) looked up. 25-26: counts only. "
        "3. For each fitting pair at 1-24: the forced key at the covered slots, checked against every rotation of every "
        "dictionary word (3-24) and puzzle word of length L, key letters numbered on standard, KRYPTOS, the plain or the "
        "cipher alphabet, any shift. "
        "3b. Where every key slot holds a known place (lengths to 13, and 15, 16), a fitting pair fixes the whole key and "
        "reading: those readings are kept for K4 and every copy and scored alike (added after a dry run showed 5 fitting "
        "pairs on K4 at 16 and none on 3 copies). "
        "4. K4 and 50 shuffles (same search); 12 plants (2 per length 19-24) with their own search. "
        "5. Any K4 key-word fit decrypted in full and submitted."
    ),
    "walkthrough": (
        "1. Choose a key length, say 19, and list the pairs of known places 19 apart: places 26 and 64 hold N and B, carved Q and N. "
        "2. In the added form the same key letter took N to Q and B to N, so on the cipher alphabet Q sits as far after N as N sits after B on the plain alphabet. "
        "3. For every cipher alphabet write down how far Q is from N (and the same for every other pair): that is its file number. "
        "4. For every plain alphabet work out the file number it needs and look it up: the alphabets filed there are the only partners. "
        "5. For each partner pair read off the key letters the known letters force and check whether they spell an English word from some starting letter."
    ),
    "expected_minutes": 30,
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
N_COPIES = 50
PLANT_LS = (19, 20, 21, 22, 23, 24)
PLANTS_PER_L = 2
SEED = 244
_G = {}


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
    for L in range(1, LCOUNT + 1):
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
    import json
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
    # self-check: K1 is this cipher with KRYPTOS on both sides, PALIMPSEST numbered on KRYPTOS, added form
    k1 = json.loads((ROOT / "data" / "k1.json").read_text())
    pt1 = k1["plaintext"]; ct1 = k1["ciphertext"][:len(pt1)]
    key1 = {"pa": KRY, "ca": KRY, "form": "added", "ka": "kry", "word": "PALIMPSEST", "start": 0, "shift": 0}
    assert encrypt(pt1 + "A" * (N - len(pt1)), key1)[:len(pt1)] == ct1, "K1 self-check failed"
    rng = random.Random(SEED)
    texts = [("k4", k4, known)]
    for i in range(N_COPIES):
        s = list(k4); rng.shuffle(s); texts.append((f"copy{i}", "".join(s), known))
    # plants: Carter's text; its own letters at the 24 known places play the known words
    carter = "".join(c for c in (ROOT / "knowledge" / "sources" / "carter-1923-tomb-of-tutankhamen-vol1.txt").read_text(errors="ignore").upper() if "A" <= c <= "Z")
    plants = {}
    for L in PLANT_LS:
        strs, src = _G["rots"][L]
        for j in range(PLANTS_PER_L):
            o = rng.randrange(len(carter) // 2, len(carter) - N)
            pt = carter[o:o + N]
            pa, ca = A[rng.randrange(2, len(A))], A[rng.randrange(2, len(A))]
            w, r = src[rng.randrange(len(src))]
            key = {"pa": pa, "ca": ca, "form": rng.choice(("added", "beaufort")), "ka": rng.choice(("std", "kry", "plain", "cipher")),
                   "word": w, "start": r, "shift": rng.randrange(26)}
            pc = encrypt(pt, key)
            assert decrypt(pc, key) == pt
            pid = f"plant{L}_{j}"
            plants[pid] = {"L": L, "key": key, "pt": pt, "ct": pc}
            texts.append((pid, pc, {q: pt[q - 1] for q in known}))
    res = {}
    workers = int(os.environ.get("K4_WORKERS", 8))
    ctx.progress(0, len(texts), "texts searched")
    with mp.get_context("fork").Pool(workers) as pool:
        for tid, out in pool.imap_unordered(_job, texts, chunksize=1):
            res[tid] = out
            ctx.progress(len(res), len(texts), "texts searched")
    fits = {f"{L}/{f}": {"k4": res["k4"]["fits"][(L, f)], "copies_max": max(res[f"copy{i}"]["fits"][(L, f)] for i in range(N_COPIES)),
                         "copies_median": float(np.median([res[f"copy{i}"]["fits"][(L, f)] for i in range(N_COPIES)])),
                         "copies_with_any": sum(1 for i in range(N_COPIES) if res[f"copy{i}"]["fits"][(L, f)])}
            for L in range(1, LCOUNT + 1) for f in ("added", "beaufort")}
    km = {"k4": len(res["k4"]["matches"]), "copies": [len(res[f"copy{i}"]["matches"]) for i in range(N_COPIES)]}
    found = {}
    for pid, p in plants.items():
        k = p["key"]
        hit = any(m["L"] == p["L"] and m["form"] == k["form"] and m["pa"] == k["pa"] and m["ca"] == k["ca"]
                  and decrypt(p["ct"], key_of(m)) == p["pt"] for m in res[pid]["matches"])
        found[pid] = {"L": p["L"], "found": bool(hit), "fits_at_L": res[pid]["fits"][(p["L"], k["form"])],
                      "matches": len(res[pid]["matches"]), "pa_word": names[A.index(k["pa"])], "ca_word": names[A.index(k["ca"])],
                      "key_word": k["word"], "key_numbering": k["ka"]}
    cands = [{"plaintext": decrypt(k4, key_of(m)), "key": key_of(m)} for m in res["k4"]["matches"][:200]]
    # fully fixed readings (every slot covered): K4's as candidates, the copies' as the comparison, scored alike
    from kryptos.scorer import free_text
    strip = lambda k: {x: k[x] for x in ("pa", "ca", "form", "ka", "word", "start", "shift")}
    cands += [{"plaintext": f["reading"], "key": strip(f["key"])} for f in res["k4"]["full"][:200]]
    full_k4 = sorted(((ctx.english_score(free_text(f["reading"])), f["L"], f["key"]["form"], f["key"]["pa_word"], f["key"]["ca_word"], f["reading"])
                      for f in res["k4"]["full"]), reverse=True)
    full_cop = [max([ctx.english_score(free_text(f["reading"])) for f in res[f"copy{i}"]["full"]] or [None]) if res[f"copy{i}"]["full"] else None
                for i in range(N_COPIES)]
    controls = []
    for i in range(N_COPIES):
        sc = [ctx.english_score(free_text(decrypt(texts[1 + i][1], key_of(m)))) for m in res[f"copy{i}"]["matches"][:50]]
        sc += [ctx.english_score(free_text(f["reading"])) for f in res[f"copy{i}"]["full"]]
        if sc:
            controls.append(max(sc))
    lowest_k4 = next((L for L in range(1, LCOUNT + 1) if res["k4"]["fits"][(L, "added")] or res["k4"]["fits"][(L, "beaufort")]), None)
    bounds = {
        "item": "F14.1", "alphabets": len(A), "alphabet_pairs_per_form": len(A) ** 2,
        "alphabet_source": "keyword-mixed alphabet of every dictionary word of 4+ letters (0109) plus standard and KRYPTOS",
        "key_lengths": [1, LCOUNT], "key_word_check_lengths": [1, LMAX],
        "key_word_rotations": {L: len(v[0]) for L, v in sorted(_G["rots"].items())},
        "key_numbering": "standard, KRYPTOS, the plain alphabet or the cipher alphabet, any indicator shift 0-25",
        "fitting_pairs_k4_and_copies": fits, "lowest_length_with_a_fit_k4": lowest_k4,
        "key_word_matches": km,
        "fully_fixed_readings": {"k4_count": len(res["k4"]["full"]), "k4_best": [list(x) for x in full_k4[:10]],
                                 "copies_count": [len(res[f"copy{i}"]["full"]) for i in range(N_COPIES)],
                                 "copies_best_score": full_cop,
                                 "k4_above_every_copy": (bool(full_k4) and all(c is None or full_k4[0][0] > c for c in full_cop))}, "plants": found, "plants_found": sum(v["found"] for v in found.values()), "plants_total": len(found),
        "texts": len(texts), "copies": N_COPIES, "exhaustive": True, "compute_seconds": round(time.time() - t0),
    }
    notes = (f"{len(A):,} alphabets, {len(A) ** 2:,} ordered pairs per form, key lengths 1-{LCOUNT}. K4: first fit at L {lowest_k4}; "
             f"key-word matches K4 {km['k4']}, copies max {max(km['copies'])}; plants found {bounds['plants_found']}/{len(found)}")
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
