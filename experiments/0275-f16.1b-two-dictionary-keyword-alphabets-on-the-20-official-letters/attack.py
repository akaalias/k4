"""Experiment: F16.1b. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f16.1b-two-dictionary-keyword-alphabets-on-the-20-official-letters",
    "title": "F16.1b: two keyword alphabets from the whole dictionary, one on each side of the table, a repeating key (free, then a key word), on the 20 official known letters (EAST set aside): every pair of 208,064 alphabets through 0244's exact index, key lengths 1-26, both forms; K4 against 50 shuffles, 12 plants",
    "family": "16-simple-hand-methods",
    "parent": "0244-f14-two-dictionary-keyword-alphabets-and-a-key-word",
    "changed": (
        "F16.1 (issue #123), second part: 0244's search on the 20 letters Sanborn published himself (26-34, 64-74). "
        "The alphabets, the pair index and the key-word matcher are imported from 0244's attack.py unchanged. New: the "
        "fitting pairs are first screened for a key word by a vectorised hash of the forced key (every rotation of every "
        "dictionary and puzzle word, numbered on the standard, KRYPTOS, plain or cipher alphabet, any shift), and every "
        "hit is confirmed by 0244's own match_key_word; key words checked to length 23 (0244: 24), lengths 24-26 counted "
        "only, because without EAST length 24 has about 3 x 10^9 fitting pairs on K4."
    ),
    "hypothesis_expert": (
        "As 0244: Scheidt's mask in its keyed form (C4(a), C5; 03-scheidt-said.md), a keyword monoalphabet before a keyed "
        "tableau, one Quagmire IV with the plain alphabet the mask's and the cipher alphabet the table's, both keyword-mixed "
        "from any dictionary word of 4+ letters (or standard, KRYPTOS), key free or a word. Criteria revised 2026-11-17 (#124): "
        "EAST (22-25) is second-hand, so the known letters are the 20 official ones. Constraint: at key length L, places in "
        "the same slot give one equation each; four fewer known letters remove the checks EAST gave, so pairs fit from "
        "about L = 14 (0244: 16 on K4) and the count rises steeply. Two tests: (a) fitting-pair counts per length and form "
        "against 50 shuffles (counts only; the key is free, a chart key under #124); (b) a key word (dictionary or puzzle, "
        "any rotation, numbering and shift) for the forced key at lengths 3-23, where chance matches stay far below one "
        "per text because the 20 places cover 9-17 slots."
    ),
    "hypothesis_eli5": (
        "Sanborn may have scrambled the alphabet on each side of his table with a different word, then used a repeating "
        "key word. Experiment 244 tried every pair of dictionary words for the two alphabets and found nothing, but it "
        "relied on EAST, which Sanborn confirmed only privately. Here we use only the 20 letters he published, try every "
        "pair again, and ask whether the key the known letters force is itself a word, on the carving and on 50 scrambled "
        "copies of it."
    ),
    "prediction": (
        "No key word on K4 at any length 3-23 (shuffles: none or almost none). Fitting-pair counts per length and form "
        "inside the shuffles' range (K4 at or below the median in most cells; no cell where K4 beats all 50 by more than "
        "chance across 52 cells). Plants found 12 of 12 (their true pair fits and their key word is recovered). Candidates "
        "only if a key word fits: none expected."
    ),
    "method": (
        "1. Build 0244's 208,064 keyword alphabets and its rotation lists of every dictionary and puzzle word of 3-24 "
        "letters. 2. For each text, key length 1-26 and form: 0244's pair index over the 20 known places gives every "
        "(plain, cipher) alphabet pair that fits. 3. For lengths up to 23: the forced key on the covered slots, hashed "
        "against every word rotation in each numbering (standard, KRYPTOS: by differences; plain, cipher: by letters, for "
        "each of 26 first letters); every hit confirmed by 0244's match_key_word. 4. K4, 50 shuffles, 12 plants (Carter's "
        "text, two random dictionary alphabets, a random dictionary key word, at lengths 16-23). 5. Compare counts and "
        "matches with the shuffles."
    ),
    "walkthrough": (
        "1. Pick two words, say SHADOW and LUCID, and write the keyword alphabets SHADOWBCEF... and LUCIDABEFG... "
        "2. Choose a key length, say 16, and give each of the 20 known places its slot (place minus 1, mod 16). "
        "3. For two known places in the same slot, the key is the same, so the cipher-alphabet distance between their two carved letters must equal the plain-alphabet distance between their two known letters. "
        "4. If every such pair agrees, the alphabet pair fits length 16. "
        "5. Read off the key letter each slot needs and see whether the letters spell a word, in some rotation and numbering. "
        "6. Do the same on scrambled copies of the carving and compare."
    ),
    "expected_minutes": 40,
}

import multiprocessing as mp
import os
import random
import sys
import time
import types
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
N = 97
OFFICIAL = tuple(range(26, 35)) + tuple(range(64, 75))
LCOUNT, WMAX = 26, 23
N_COPIES = 50
PLANT_LS = (16, 18, 20, 21, 22, 23)
PLANTS_PER_L = 2
SEED = 16200
CHUNK = 200000
_G = {}


def frozen():
    """0244's attack.py, unchanged."""
    if "m" not in _G:
        import importlib.util
        path = next((ROOT / "experiments").glob("0244-*")) / "attack.py"
        spec = importlib.util.spec_from_file_location("frozen0244", path)
        m = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = m
        spec.loader.exec_module(m)
        m.ROOT = ROOT
        _G["m"] = m
    return _G["m"]


def setup(vocabulary):
    m = frozen()
    A, names, pos = m.alphabets()
    m._G.update(A=A, names=names, pos=pos, rots=m.key_words(vocabulary))
    m._G["rotmat"] = {L: np.array([[ord(c) - 65 for c in s] for s in strs], dtype=np.int16) for L, (strs, _) in m._G["rots"].items()}
    m._G["lut_std"] = np.arange(26, dtype=np.int16)
    m._G["lut_kry"] = np.array([m.KRY.index(c) for c in m.STD], dtype=np.int16)
    _G["letters"] = np.array([[ord(c) - 65 for c in a] for a in A], dtype=np.int16)    # letters[a, place] = letter
    _G["coef"] = np.random.default_rng(16201).integers(1, 2 ** 62, size=32, dtype=np.uint64)
    _G["rothash"] = {}


def h64(M):
    """Row hash of a small-int matrix (wrapping uint64)."""
    c = _G["coef"][:M.shape[1]]
    return ((M.astype(np.uint64) + np.uint64(1)) * c).sum(axis=1, dtype=np.uint64)


def rot_hashes(L, cover):
    """Per numbering: hashes of each rotation's covered-slot pattern (std/kry: differences; letters for plain/cipher)."""
    key = (L, tuple(cover))
    if key not in _G["rothash"]:
        m = frozen()
        R = m._G["rotmat"][L][:, cover]
        out = {}
        for ka, lut in (("std", m._G["lut_std"]), ("kry", m._G["lut_kry"])):
            v = lut[R]
            out[ka] = np.unique(h64((v - v[:, :1]) % 26))
        out["letters"] = np.unique(h64(R))
        _G["rothash"][key] = out
    return _G["rothash"][key]


def pairs_for(text, known, L, places, ci, pi, pl_index):
    """0244's index, returning the fitting pairs as arrays (and the count)."""
    m = frozen()
    pos = m._G["pos"]
    sl = m.slots_of(L, places)
    prs = [(v[0], u) for v in sl.values() for u in v[1:]]
    out = {}
    if not prs:
        n = len(pos) ** 2
        return {f: (n, None, None) for f in ("added", "beaufort")}, sl
    a_idx = np.array([pl_index[x] for x, _ in prs], dtype=int)
    b_idx = np.array([pl_index[y] for _, y in prs], dtype=int)
    cvec = (pos[:, ci[a_idx]] - pos[:, ci[b_idx]]) % 26
    pvec = (pos[:, pi[a_idx]] - pos[:, pi[b_idx]]) % 26
    cidx = {}
    for a, kb in enumerate(r.tobytes() for r in cvec.astype(np.uint8)):
        cidx.setdefault(kb, []).append(a)
    for form in ("added", "beaufort"):
        pv = pvec if form == "added" else (-pvec) % 26
        pk = [r.tobytes() for r in pv.astype(np.uint8)]
        if L > WMAX:
            out[form] = (int(sum(len(cidx.get(kb, ())) for kb in pk)), None, None)
            continue
        P, C = [], []
        for p_a, kb in enumerate(pk):
            partners = cidx.get(kb)
            if partners:
                P.extend([p_a] * len(partners)); C.extend(partners)
        out[form] = (len(P), np.array(P, dtype=np.int64), np.array(C, dtype=np.int64))
    return out, sl


def word_hits(L, form, P, C, cover, first, text, known):
    """Pairs whose forced key hashes to some word rotation in some numbering (screen only)."""
    m = frozen()
    pos, letters = m._G["pos"], _G["letters"]
    if L not in m._G["rots"] or P is None or not len(P):
        return []
    rh = rot_hashes(L, cover)
    cq = np.array([ord(text[first[s] - 1]) - 65 for s in cover])
    pq = np.array([ord(known[first[s]]) - 65 for s in cover])
    hits = set()
    for a in range(0, len(P), CHUNK):
        Pp, Cc = P[a:a + CHUNK], C[a:a + CHUNK]
        cpos = pos[Cc][:, cq].astype(np.int16)
        ppos = pos[Pp][:, pq].astype(np.int16)
        K = (cpos - ppos) % 26 if form == "added" else (cpos + ppos) % 26
        D = (K - K[:, :1]) % 26
        for ka in ("std", "kry"):
            hh = np.isin(h64(D), rh[ka])
            hits.update(np.nonzero(hh)[0] + a)
        for side, Arr in (("plain", Pp), ("cipher", Cc)):
            for w0 in range(26):
                idx = (pos[Arr, w0][:, None].astype(np.int16) + D) % 26
                Lm = np.take_along_axis(letters[Arr], idx, axis=1)
                hh = np.isin(h64(Lm), rh["letters"])
                hits.update(np.nonzero(hh)[0] + a)
    return sorted(int(i) for i in hits)


def search(args):
    tid, text, known = args
    m = frozen()
    places = sorted(known)
    pl_index = {q: e for e, q in enumerate(places)}
    ci = np.array([ord(text[q - 1]) - 65 for q in places])
    pi = np.array([ord(known[q]) - 65 for q in places])
    res = {"fits": {}, "matches": [], "screen_hits": 0}
    for L in range(1, LCOUNT + 1):
        fs, sl = pairs_for(text, known, L, places, ci, pi, pl_index)
        cover = sorted(sl)
        first = {s: sl[s][0] for s in cover}
        for form, (n, P, C) in fs.items():
            res["fits"][f"{L}/{form}"] = n
            if P is None:
                continue
            hits = word_hits(L, form, P, C, cover, first, text, known)
            res["screen_hits"] += len(hits)
            out = {"matches": []}
            for i in hits[:5000]:
                m.match_key_word(L, form, int(P[i]), int(C[i]), cover, first, text, known, out)
            for x in out["matches"][:200]:
                res["matches"].append(x)
    return tid, res


def run(ctx):
    me = sys.modules.get(__name__)
    if getattr(me, "search", None) is not search:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    import json
    t0 = time.time()
    m = frozen()
    setup(ctx.vocabulary)
    A, names = m._G["A"], m._G["names"]
    k4 = ctx.K4
    k20 = {q: ctx.KNOWN[q] for q in OFFICIAL}
    # self-check: K1 under 0244's cipher
    k1 = json.loads((ROOT / "data" / "k1.json").read_text())
    pt1 = k1["plaintext"]; ct1 = k1["ciphertext"][:len(pt1)]
    key1 = {"pa": m.KRY, "ca": m.KRY, "form": "added", "ka": "kry", "word": "PALIMPSEST", "start": 0, "shift": 0}
    assert m.encrypt(pt1 + "A" * (N - len(pt1)), key1)[:len(pt1)] == ct1, "K1 self-check failed"
    rng = random.Random(SEED)
    texts = [("k4", k4, k20)]
    for i in range(N_COPIES):
        s = list(k4); rng.shuffle(s); texts.append((f"copy{i}", "".join(s), k20))
    carter = "".join(c for c in (ROOT / "knowledge" / "sources" / "carter-1923-tomb-of-tutankhamen-vol1.txt").read_text(errors="ignore").upper() if "A" <= c <= "Z")
    plants = {}
    for L in PLANT_LS:
        strs, src = m._G["rots"][L]
        for j in range(PLANTS_PER_L):
            o = rng.randrange(len(carter) // 2, len(carter) - N)
            pt = carter[o:o + N]
            pa, ca = A[rng.randrange(2, len(A))], A[rng.randrange(2, len(A))]
            w, r = src[rng.randrange(len(src))]
            key = {"pa": pa, "ca": ca, "form": rng.choice(("added", "beaufort")), "ka": rng.choice(("std", "kry", "plain", "cipher")),
                   "word": w, "start": r, "shift": rng.randrange(26)}
            pc = m.encrypt(pt, key)
            assert m.decrypt(pc, key) == pt
            pid = f"plant{L}_{j}"
            plants[pid] = {"L": L, "key": key, "pt": pt, "ct": pc}
            texts.append((pid, pc, {q: pt[q - 1] for q in OFFICIAL}))
    saved = getattr(ctx, "saved", {}) or {}
    res = {t[0]: saved[t[0]] for t in texts if t[0] in saved}
    todo = [t for t in texts if t[0] not in res]
    todo.sort(key=lambda t: t[0] != "k4")
    W = int(os.environ.get("K4_WORKERS", 8))
    ctx.progress(len(res), len(texts), "texts searched")
    with mp.get_context("fork").Pool(W) as pool:
        for tid, out in pool.imap_unordered(search, todo, chunksize=1):
            res[tid] = out
            ctx.save(tid, out)
            ctx.progress(len(res), len(texts), "texts searched")
    cells = [f"{L}/{f}" for L in range(1, LCOUNT + 1) for f in ("added", "beaufort")]
    fits = {}
    above = []
    null_above = [0] * N_COPIES
    for c in cells:
        kv = res["k4"]["fits"][c]
        cv = [res[f"copy{i}"]["fits"][c] for i in range(N_COPIES)]
        fits[c] = {"k4": kv, "copies_median": float(np.median(cv)), "copies_max": max(cv), "copies_with_any": sum(1 for x in cv if x),
                   "at_or_above": sum(1 for x in cv if x >= kv), "p": round((1 + sum(1 for x in cv if x >= kv)) / (N_COPIES + 1), 4)}
        if kv and kv > max(cv):
            above.append(c)
        for i in range(N_COPIES):
            others = [kv] + [cv[j] for j in range(N_COPIES) if j != i]
            if cv[i] and cv[i] > max(others):
                null_above[i] += 1
    km = {"k4": len(res["k4"]["matches"]), "copies": [len(res[f"copy{i}"]["matches"]) for i in range(N_COPIES)]}
    found = {}
    for pid, p in plants.items():
        k = p["key"]
        hit = any(x["L"] == p["L"] and x["form"] == k["form"] and x["pa"] == k["pa"] and x["ca"] == k["ca"]
                  and m.decrypt(p["ct"], m.key_of(x)) == p["pt"] for x in res[pid]["matches"])
        found[pid] = {"L": p["L"], "found": bool(hit), "fits_at_L": res[pid]["fits"][f"{p['L']}/{k['form']}"],
                      "matches": len(res[pid]["matches"]), "key_word": k["word"], "key_numbering": k["ka"],
                      "pa_word": names[A.index(k["pa"])], "ca_word": names[A.index(k["ca"])]}
    cands = [{"plaintext": m.decrypt(k4, m.key_of(x)), "key": m.key_of(x)} for x in res["k4"]["matches"][:200]]
    lowest = next((L for L in range(1, LCOUNT + 1) if res["k4"]["fits"][f"{L}/added"] or res["k4"]["fits"][f"{L}/beaufort"]), None)
    bounds = {
        "item": "F16.1b", "known_places": list(OFFICIAL),
        "alphabets": len(A), "alphabet_pairs_per_form": len(A) ** 2,
        "alphabet_source": "0244's: keyword-mixed alphabet of every dictionary word of 4+ letters plus standard and KRYPTOS",
        "key_lengths": [1, LCOUNT], "key_word_check_lengths": [3, WMAX], "count_only_lengths": [WMAX + 1, LCOUNT],
        "key_numbering": "standard, KRYPTOS, the plain alphabet or the cipher alphabet, any indicator shift 0-25",
        "screen": "64-bit hash of the forced key on covered slots against every rotation (differences for standard/KRYPTOS, letters for each of 26 first letters for plain/cipher); every hit confirmed by 0244's match_key_word",
        "fitting_pairs": fits, "k4_above_every_copy_cells": above, "copies_above_the_rest_cells": {"min": min(null_above), "max": max(null_above)},
        "lowest_length_with_a_fit_k4": lowest,
        "key_word_matches": km, "screen_hits_k4": res["k4"]["screen_hits"],
        "plants": found, "plants_found": sum(v["found"] for v in found.values()), "plants_total": len(found),
        "texts": len(texts), "copies": N_COPIES, "exhaustive": True, "compute_seconds": round(time.time() - t0),
        "aws_cost_estimate_dollars": 0.5,
    }
    notes = (f"20 official letters; K4 first fit at L {lowest}; key-word matches K4 {km['k4']}, copies max {max(km['copies'])}; "
             f"K4 above every copy in {len(above)} of 52 cells {above} (copies {min(null_above)}-{max(null_above)}); "
             f"plants found {bounds['plants_found']}/{len(found)}")
    return {"candidates": cands, "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return frozen().encrypt(plaintext, key)


def worked_example(ctx, key):
    m = frozen()
    L = 16
    places = sorted(OFFICIAL)
    sl = m.slots_of(L, places)
    lines = [f"key length {L}: the 20 official places by slot (place - 1 mod {L}); same-slot places share a key letter", ""]
    for s in sorted(sl):
        qs = sl[s]
        lines.append(f"  slot {s:2d}: " + ", ".join(f"{q} {ctx.KNOWN[q]}->{ctx.K4[q - 1]}" for q in qs))
    lines.append("")
    lines.append("A pair of alphabets fits when, in every slot with two places, the cipher-alphabet distance of the carved letters equals the plain-alphabet distance of the known letters.")
    return "\n".join(lines)
