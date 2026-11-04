"""Experiment (F14.2, draft). See program.md for the contract."""

EXPERIMENT = {
    "slug": "f14.2-a-remembered-route-plus-two-dictionary-keyword-alphabets",
    "title": "F14.2: every type-1 move of 0129's library (27,852), both orders, key lengths 1-26, then a table with two dictionary keyword alphabets (208,064 each, standard and KRYPTOS among them) and a repeating key word; K4 against 50 shuffles, plants",
    "family": "14-scheidt-mask-keyed-by-words",
    "parent": "0244-f14-two-dictionary-keyword-alphabets-and-a-key-word",
    "changed": (
        "F14.2, the full run Alexis decided (#102). 0244's exact pair index (every plain and cipher keyword alphabet matched "
        "through the differences the known letters force) run after or before every move of 0129's type-1 library, at every "
        "key length 1-26, both forms. Faster than the design's estimate: which known places share a key slot depends only on "
        "the setting, so the plain-side index is built once per setting and K4 and its 50 shuffles are looked up in it; a "
        "difference table D[x, y] over all alphabets makes each check one contiguous row. Checked: with the identity move it "
        "reproduces 0244's fit counts on K4 (desk, 2026-11-04)."
    ),
    "hypothesis_expert": (
        "F14 (Scheidt's mask keyed by words; C4(a), C5; 03-scheidt-said.md 'masked the English language', 'executed with the "
        "correct key word/s') with Sanborn's matrix step first or last (C1(a): 'I used a matrix code, and then... this "
        "[tableau]'; 'double matrixes'): a remembered route (keyword columnar, K3's rule, turns, rail fence, grid paths: "
        "0129's 27,852 distinct moves and their inverses) and a Quagmire IV table whose alphabets are keyword alphabets from "
        "the dictionary, keyed by a repeating word. F6.1 and F6.2 decided free alphabets around these moves at the copies' "
        "rate; keyword alphabets cost about 35 bits for the pair, so the known letters decide them where 5 or more same-slot "
        "checks fall (chance pairs 4.3 x 10^10 / 26^c per form: 3,600 at c = 5, 140 at 6, 5 at 7, 0.2 at 8). A fitted pair "
        "forces the key at the covered slots; a dictionary or puzzle word of length L (any rotation, numbered on standard or "
        "KRYPTOS, any shift) must give it. Settings with 4 or fewer checks are counted only (chance pairs 10^5 and more). "
        "Clue entries C1(a), C4(a), C5, C27(c)."
    ),
    "hypothesis_eli5": (
        "Sanborn said he wrote the message into a grid and read it out another way, then used the cipher table. Scheidt said "
        "the English was disguised first, and that the system is worked with key words. Here the grid step is any of about "
        "28,000 ways of reading a grid, and both alphabets of the table are scrambled by English words. For each recipe, the "
        "24 known letters tell us exactly which pairs of word-scrambled alphabets could work; then we check whether the key "
        "they force is a word. Fifty scrambled copies of K4 go through the same test, so we know how many matches chance gives."
    ),
    "prediction": (
        "K4's fitting pairs and key-word matches per (order, key length) inside the 50 shuffles' range; plants found at every "
        "band; no reading English. Zero candidates kept."
    ),
    "method": (
        "1. Settings: 0129's route library (27,852 moves) x order (A move then table, B table then move) x key length 1-26; "
        "for each, the 24 known places' carved places and key slots, and the same-slot checks (first place of a slot against "
        "each other). "
        "2. Per setting and form, the plain-side key of every alphabet on the first min(c, 6) checks, sorted; per text, the "
        "cipher-side keys looked up (a bitmap first, then exact), the remaining checks verified on the candidate pairs. "
        "c <= 4: the number of fitting pairs counted exactly, not listed. "
        "3. Key word (L <= 24, 3 or more covered slots): each fitted pair's forced key differences matched against every "
        "rotation of every dictionary and puzzle word of length L, numbered on standard or KRYPTOS (and on the pair's own "
        "alphabets when 20 or fewer pairs fit); a match fixes the whole key and so the reading. "
        "4. Texts: K4 and 50 shuffles (seed 1420), every setting; 12 plants (English with the known words, a random move, "
        "order, two dictionary alphabets and a dictionary key word; 4 in each length band 6-10, 11-18, 19-24, on settings "
        "with 5 or more checks), each searched at its own setting with the same code. "
        "5. Verdict: K4's fitting pairs (settings with 5+ checks) and key-word matches per (order, length) ranked among the "
        "shuffles; K4's key-word readings submitted as candidates, the shuffles' best as controls."
    ),
    "walkthrough": (
        "1. Write the message in rows of 9 and read the columns in a key word's order (one of the moves). "
        "2. For a key length, say 12, follow each of the 24 known letters to its carved place and its key slot. "
        "3. Two known letters in one slot must be the same distance apart on the plain alphabet as their carved letters are "
        "on the cipher alphabet. "
        "4. File every word-scrambled alphabet by those distances, plain side and cipher side, and pair up the matching files. "
        "5. For each matching pair, read off the key letters the known letters force and look for a word that gives them. "
        "6. Do the same for 50 scrambled copies of K4 and compare the counts."
    ),
    "expected_minutes": 300,
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
LMAX, LCOUNT = 24, 26
KMAX = 6
MIN_LIST = 5                 # checks at which pairs are listed (and key words matched); fewer: counted only
N_COPIES = 50
SEED = 1420
BLOCK = 40                   # routes per job
PLANT_BANDS = ((6, 10), (11, 18), (19, 24))
PLANTS_PER_BAND = 4
MASK = (1 << 24) - 1
LIST_CAP = 2_000_000
POW = (26 ** np.arange(KMAX + 1)).astype(np.int64)
_G = {}


def _load(e):
    import importlib.util
    key = f"m{e}"
    if key not in _G:
        path = next((ROOT / "experiments").glob(f"{e}-*")) / "attack.py"
        spec = importlib.util.spec_from_file_location(f"frozen{e}", path)
        m = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = m
        spec.loader.exec_module(m)
        if hasattr(m, "ROOT"):
            m.ROOT = ROOT
        _G[key] = m
    return _G[key]


def routes():
    if "lib" not in _G:
        from kryptos.facts import load_vocabulary
        _G["lib"] = _load("0129").route_library(load_vocabulary())
    return _G["lib"]


def setup(vocabulary):
    """Alphabets, the difference tables and the key-word rotations; built once in the parent, shared by fork."""
    m44 = _load("0244")
    A, names, pos = m44.alphabets()
    pos = pos.astype(np.int16)
    NA = len(A)
    D = np.empty((676, NA), np.uint8)
    for x in range(26):
        for y in range(26):
            D[x * 26 + y] = ((pos[:, x] - pos[:, y]) % 26).astype(np.uint8)
    DN = ((-D.astype(np.int16)) % 26).astype(np.uint8)
    rots = m44.key_words(vocabulary)
    rotmat = {L: np.array([[ord(c) - 65 for c in s] for s in strs], dtype=np.int16) for L, (strs, _) in rots.items()}
    _G.update(A=A, names=names, pos=pos, NA=NA, D=D, DN=DN, rots=rots, rotmat=rotmat,
              lut={"std": np.arange(26, dtype=np.int16), "kry": np.array([KRY.index(c) for c in STD], dtype=np.int16)})
    from kryptos.facts import KNOWN
    _G["KP"] = sorted(KNOWN)
    _G["KL"] = np.array([ord(KNOWN[q]) - 65 for q in _G["KP"]])


# ---- the cipher ----------------------------------------------------------------------------------------
def geometry(where, o, L):
    """slot[j] and mpos[j] for every carved place j (0252's move_setting)."""
    slot, mpos = [0] * N, [0] * N
    for i in range(N):
        j = where[i]
        mpos[j] = i
        slot[j] = j % L if o == "A" else i % L
    return slot, mpos


def kvals(key):
    KA = {"std": STD, "kry": KRY, "plain": key["pa"], "cipher": key["ca"]}[key["ka"]]
    w, s0 = key["word"], key["start"]
    return [(KA.index(w[(s + s0) % len(w)]) + key["shift"]) % 26 for s in range(key["L"])]


def where_of(r):
    return tuple(range(N)) if r == -1 else routes()[r][1]


def encrypt(plaintext, key):
    where = where_of(key["route"])
    slot, mpos = geometry(where, key["o"], key["L"])
    PA, CA, k = key["pa"], key["ca"], kvals(key)
    out = []
    for j in range(N):
        p = PA.index(plaintext[mpos[j]])
        out.append(CA[(p + k[slot[j]]) % 26] if key["form"] == "V" else CA[(k[slot[j]] - p) % 26])
    return "".join(out)


def decrypt(ct, key):
    where = where_of(key["route"])
    slot, mpos = geometry(where, key["o"], key["L"])
    PA, CA, k = key["pa"], key["ca"], kvals(key)
    pt = [""] * N
    for j in range(N):
        c = CA.index(ct[j])
        pt[mpos[j]] = PA[(c - k[slot[j]]) % 26] if key["form"] == "V" else PA[(k[slot[j]] - c) % 26]
    return "".join(pt)


# ---- the search ------------------------------------------------------------------------------------------
def checks_of(where, o, L):
    KP = _G["KP"]
    land = [where[q - 1] for q in KP]
    slot = [(land[e] % L) if o == "A" else ((q - 1) % L) for e, q in enumerate(KP)]
    groups = {}
    for e, s in enumerate(slot):
        groups.setdefault(s, []).append(e)
    pairs = [(g[0], u) for g in groups.values() for u in g[1:]]
    first = {s: g[0] for s, g in groups.items()}
    return pairs, np.array(land), first


def plain_index(pairs, form):
    KL, NA = _G["KL"], _G["NA"]
    T = _G["DN"] if form == "B" else _G["D"]
    k = min(len(pairs), KMAX)
    key = np.zeros(NA, np.int64)
    for j, (a, b) in enumerate(pairs[:k]):
        key += T[KL[a] * 26 + KL[b]].astype(np.int64) * POW[j]
    order = np.argsort(key, kind="stable")
    sk = key[order]
    bm = np.zeros(MASK + 1, bool)
    bm[sk & MASK] = True
    return sk, order, bm, k


def cipher_key(cl, pairs, k):
    D, NA = _G["D"], _G["NA"]
    key = np.zeros(NA, np.int64)
    for j, (a, b) in enumerate(pairs[:k]):
        key += D[cl[a] * 26 + cl[b]].astype(np.int64) * POW[j]
    return key


def fits(cl, pairs, idx, ck, form):
    """Count (c < MIN_LIST) or list (cipher, plain) alphabet pairs satisfying every check."""
    sk, order, bm, k = idx
    if len(pairs) < MIN_LIST:
        lo = np.searchsorted(sk, ck, "left"); hi = np.searchsorted(sk, ck, "right")
        return int((hi - lo).sum()), None
    cand = np.nonzero(bm[ck & MASK])[0]
    if len(cand) == 0:
        return 0, None
    lo = np.searchsorted(sk, ck[cand], "left"); hi = np.searchsorted(sk, ck[cand], "right")
    n = hi - lo
    tot = int(n.sum())
    if tot == 0:
        return 0, None
    if tot > LIST_CAP:                       # checks that carry no information (equal gaps on both sides): count only
        lo = np.searchsorted(sk, ck, "left"); hi = np.searchsorted(sk, ck, "right")
        return int((hi - lo).sum()), None
    ci = np.repeat(cand, n)
    pi = order[np.repeat(lo, n) + np.arange(tot) - np.repeat(np.cumsum(n) - n, n)]
    if len(pairs) > k:
        D, KL = _G["D"], _G["KL"]
        T = _G["DN"] if form == "B" else D
        ok = np.ones(tot, bool)
        for a, b in pairs[k:]:
            ok &= D[cl[a] * 26 + cl[b]][ci] == T[KL[a] * 26 + KL[b]][pi]
        ci, pi = ci[ok], pi[ok]
    return len(ci), (ci, pi)


def word_index(L, cover, numbering, cache):
    """Rotations of length-L words, keyed by their value differences at the covered slots (first 12)."""
    ck = (L, tuple(cover), numbering)
    if ck not in cache:
        rot = _G["lut"][numbering][_G["rotmat"][L][:, cover]]
        d = (rot[:, 1:] - rot[:, :1]) % 26
        m = min(d.shape[1], 12)
        key = (d[:, :m].astype(np.int64) * POW13[:m]).sum(axis=1)
        o = np.argsort(key, kind="stable")
        cache[ck] = (key[o], o, d)
    return cache[ck]


POW13 = (26 ** np.arange(13)).astype(np.int64)


def key_words(ci, pi, cl, first, cover, L, form, cache, text, setting, out):
    """Forced key at the covered slots for every fitted pair; any word rotation that gives it, up to a shift."""
    pos, KL = _G["pos"], _G["KL"]
    reps = [first[s] for s in cover]
    cvals = pos[ci][:, cl[reps]].astype(np.int16)
    pvals = pos[pi][:, KL[reps]].astype(np.int16)
    kf = (cvals - pvals) % 26 if form == "V" else (cvals + pvals) % 26
    d = (kf[:, 1:] - kf[:, :1]) % 26
    m = min(d.shape[1], 12)
    pk = (d[:, :m].astype(np.int64) * POW13[:m]).sum(axis=1)
    strs, src = _G["rots"][L]
    nums = ["std", "kry"] + (["plain", "cipher"] if len(ci) <= 20 else [])
    for numbering in nums:
        if numbering in ("std", "kry"):
            wk, wo, wd = word_index(L, cover, numbering, cache)
            lo = np.searchsorted(wk, pk, "left"); hi = np.searchsorted(wk, pk, "right")
            hits = [(i, wo[h]) for i in np.nonzero(hi > lo)[0] for h in range(lo[i], hi[i])]
            hits = [(i, w) for i, w in hits if (wd[w] == d[i]).all()]
            for i, w in hits[:20]:
                rot = _G["lut"][numbering][_G["rotmat"][L][w, cover[0]]]
                _record(out, setting, form, ci[i], pi[i], numbering, src[w], int((kf[i, 0] - rot) % 26), text)
        else:
            for i in range(len(ci)):
                lut = pos[pi[i]] if numbering == "plain" else pos[ci[i]]
                rot = lut[_G["rotmat"][L][:, cover]]
                dv = (rot[:, 1:] - rot[:, :1]) % 26
                for w in np.nonzero((dv == d[i]).all(axis=1))[0][:20]:
                    _record(out, setting, form, ci[i], pi[i], numbering, src[w], int((kf[i, 0] - rot[w, 0]) % 26), text)


def _record(out, setting, form, ci, pi, numbering, wsrc, shift, text):
    r, o, L = setting
    A = _G["A"]
    key = {"route": r, "o": o, "L": L, "form": form, "pa": A[pi], "ca": A[ci], "ka": numbering,
           "word": wsrc[0], "start": wsrc[1], "shift": shift}
    out["matches"].append(key)


def search_settings(text, settings, plain_cache, word_cache):
    """One text over a list of settings; per (o, L, form) counts, and key-word matches."""
    tix = np.array([ord(c) - 65 for c in text])
    out = {"fits": {}, "listed_fits": {}, "settings_listed": {}, "settings_with_fit": {}, "matches": []}
    lib = routes()
    for (r, o, L) in settings:
        pairs, land, first = plain_cache[(r, o, L)][:3]
        if not pairs:
            continue
        cl = tix[land]
        k = min(len(pairs), KMAX)
        ck = cipher_key(cl, pairs, k)
        cover = sorted(first)
        for form in "VB":
            idx = plain_cache[(r, o, L)][3][form]
            n, lst = fits(cl, pairs, idx, ck, form)
            c = (o, L, form)
            out["fits"][c] = out["fits"].get(c, 0) + n
            if len(pairs) >= MIN_LIST:
                out["settings_listed"][c] = out["settings_listed"].get(c, 0) + 1
                out["listed_fits"][c] = out["listed_fits"].get(c, 0) + n
                out["settings_with_fit"][c] = out["settings_with_fit"].get(c, 0) + (n > 0)
                if lst is not None and n and L <= LMAX and len(cover) >= 3 and L in _G["rots"]:
                    key_words(lst[0], lst[1], cl, first, cover, L, form, word_cache, text, (r, o, L), out)
    return out


def _job(args):
    """One block of routes, every text: the plain-side indexes are built once per setting and shared."""
    b, r0, r1, texts = args
    t0 = time.time()
    lib = routes()
    settings = [(r, o, L) for r in range(r0, r1) for o in "AB" for L in range(1, LCOUNT + 1)]
    res = {tid: {"fits": {}, "listed_fits": {}, "settings_listed": {}, "settings_with_fit": {}, "matches": []} for tid, _ in texts}
    word_cache = {}
    for s in settings:
        r, o, L = s
        pairs, land, first = checks_of(lib[r][1], o, L)
        if not pairs:
            continue
        pc = {(r, o, L): (pairs, land, first, {f: plain_index(pairs, f) for f in "VB"})}
        for tid, text in texts:
            out = search_settings(text, [s], pc, word_cache)
            acc = res[tid]
            for fld in ("fits", "listed_fits", "settings_listed", "settings_with_fit"):
                for c, v in out[fld].items():
                    kk = f"{c[0]}{c[1]}{c[2]}"
                    acc[fld][kk] = acc[fld].get(kk, 0) + v
            acc["matches"] += out["matches"][:200 - len(acc["matches"])]
            acc.setdefault("n_matches", 0)
            acc["n_matches"] = acc.get("n_matches", 0) + len(out["matches"])
        if len(word_cache) > 200:
            word_cache.clear()
    return b, {"res": res, "secs": round(time.time() - t0, 1)}


def make_plants(rng, vocabulary):
    from kryptos.plants import english_plant
    A, lib = _G["A"], routes()
    plants = []
    for lo, hi in PLANT_BANDS:
        while sum(1 for p in plants if lo <= p["key"]["L"] <= hi) < PLANTS_PER_BAND:
            L = rng.randint(lo, hi)
            r, o = rng.randrange(len(lib)), rng.choice("AB")
            pairs, land, first = checks_of(lib[r][1], o, L)
            if len(pairs) < MIN_LIST or len(first) < 3 or L not in _G["rots"]:
                continue
            strs, src = _G["rots"][L]
            w = src[rng.randrange(len(src))]
            key = {"route": r, "o": o, "L": L, "form": rng.choice("VB"), "pa": A[rng.randrange(2, len(A))],
                   "ca": A[rng.randrange(2, len(A))], "ka": rng.choice(("std", "kry")), "word": w[0], "start": w[1],
                   "shift": rng.randrange(26)}
            pt = english_plant(rng.randrange(10 ** 9))
            pc = encrypt(pt, key)
            assert decrypt(pc, key) == pt
            plants.append({"key": key, "pt": pt, "ct": pc})
    return plants


def run(ctx):
    import json
    import multiprocessing as mp
    t_start = time.time()
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    setup(ctx.vocabulary)
    lib = routes()
    k4, known = ctx.K4, ctx.KNOWN
    # self-checks: K1 through the identity move; the identity move reproduces 0244's fit counts on K4
    k1 = json.loads((ROOT / "data" / "k1.json").read_text())
    pt1 = k1["plaintext"]; ct1 = k1["ciphertext"][:len(pt1)]
    key1 = {"route": -1, "o": "A", "L": 10, "form": "V", "pa": KRY, "ca": KRY, "ka": "kry", "word": "PALIMPSEST", "start": 0, "shift": 0}
    assert encrypt(pt1 + "A" * (N - len(pt1)), key1)[:len(pt1)] == ct1, "K1 self-check failed"
    rec = json.loads((next((ROOT / "experiments").glob("0244-*")) / "raw.json").read_text())["bounds"]["fitting_pairs_k4_and_copies"]
    selfcheck = {}
    for L in (16, 19, 23):
        pairs, land, first = checks_of(tuple(range(N)), "A", L)
        cl = np.array([ord(c) - 65 for c in k4])[land]
        ck = cipher_key(cl, pairs, min(len(pairs), KMAX))
        for form, f44 in (("V", "added"), ("B", "beaufort")):
            got = fits(cl, pairs, plain_index(pairs, form), ck, form)[0]
            selfcheck[f"{L}/{form}"] = [got, rec[f"{L}/{f44}"]["k4"]]
            assert got == rec[f"{L}/{f44}"]["k4"], selfcheck
    rng = random.Random(SEED)
    texts = [("k4", k4)]
    for i in range(N_COPIES):
        s = list(k4); rng.shuffle(s); texts.append((f"copy{i}", "".join(s)))
    plants = make_plants(rng, ctx.vocabulary)
    # plants: each searched at its own setting with the same code
    pfound = []
    for p in plants:
        k = p["key"]
        pairs, land, first = checks_of(lib[k["route"]][1], k["o"], k["L"])
        pc = {(k["route"], k["o"], k["L"]): (pairs, land, first, {f: plain_index(pairs, f) for f in "VB"})}
        out = search_settings(p["ct"], [(k["route"], k["o"], k["L"])], pc, {})
        hit = any(m["pa"] == k["pa"] and m["ca"] == k["ca"] and m["form"] == k["form"] and decrypt(p["ct"], m) == p["pt"]
                  for m in out["matches"])
        pfound.append({"L": k["L"], "o": k["o"], "route": lib[k["route"]][0], "checks": len(pairs), "found": hit,
                       "matches_at_setting": len(out["matches"])})
    # the main search
    jobs = [(b, r0, min(len(lib), r0 + BLOCK), texts) for b, r0 in enumerate(range(0, len(lib), BLOCK))]
    saved = getattr(ctx, "saved", {}) or {}
    res = {str(j[0]): saved[str(j[0])] for j in jobs if str(j[0]) in saved}
    todo = [j for j in jobs if str(j[0]) not in res]
    W = int(os.environ.get("K4_WORKERS", 8))
    ctx.progress(len(res), len(jobs), "route blocks")
    with mp.get_context("fork").Pool(W) as pool:
        for b, out in pool.imap_unordered(_job, todo, chunksize=1):
            res[str(b)] = out
            ctx.save(str(b), out)
            ctx.progress(len(res), len(jobs), "route blocks")
    # totals per text
    tot = {tid: {"fits": {}, "listed_fits": {}, "settings_listed": {}, "settings_with_fit": {}, "matches": [], "n_matches": 0} for tid, _ in texts}
    for v in res.values():
        for tid, acc in v["res"].items():
            for fld in ("fits", "listed_fits", "settings_listed", "settings_with_fit"):
                for c, x in acc[fld].items():
                    tot[tid][fld][c] = tot[tid][fld].get(c, 0) + x
            tot[tid]["n_matches"] += acc.get("n_matches", 0)
            tot[tid]["matches"] += acc["matches"][:max(0, 400 - len(tot[tid]["matches"]))]
    classes = sorted({c for t in tot.values() for c in t["listed_fits"]}, key=lambda c: (c[0], int(c[1:-1]), c[-1]))
    table = {}
    for c in classes:
        kv = tot["k4"]["settings_with_fit"].get(c, 0)
        cv = [tot[f"copy{i}"]["settings_with_fit"].get(c, 0) for i in range(N_COPIES)]
        table[c] = {"settings_listed": tot["k4"]["settings_listed"].get(c, 0), "k4_settings_with_fit": kv,
                    "copies_median": float(np.median(cv)), "copies_max": max(cv),
                    "p_at_or_above": round((1 + sum(x >= kv for x in cv)) / (N_COPIES + 1), 3)}
    km = tot["k4"]["n_matches"]
    cm = [tot[f"copy{i}"]["n_matches"] for i in range(N_COPIES)]
    from kryptos.scorer import free_text
    cands = []
    for m in tot["k4"]["matches"][:200]:
        pt = decrypt(k4, m)
        cands.append({"plaintext": pt, "key": m, "_score": ctx.english_score(free_text(pt))})
    cands.sort(key=lambda x: -x["_score"])
    controls = []
    for i in range(N_COPIES):
        sc = [ctx.english_score(free_text(decrypt(texts[1 + i][1], m))) for m in tot[f"copy{i}"]["matches"][:100]]
        if sc:
            controls.append(max(sc))
    minp = min((v["p_at_or_above"] for v in table.values() if v["k4_settings_with_fit"] > 0), default=None)
    bounds = {
        "item": "F14.2", "routes": len(lib), "orders": ["A move then table", "B table then move"], "key_lengths": [1, LCOUNT],
        "forms": ["added", "Beaufort"], "alphabets": _G["NA"], "alphabet_pairs_per_setting_and_form": _G["NA"] ** 2,
        "settings_per_text": len(lib) * 2 * LCOUNT, "listed_at_checks": MIN_LIST,
        "settings_listed_k4": sum(tot["k4"]["settings_listed"].values()) // 2,
        "key_word_lengths": [1, LMAX], "key_numbering": "standard or KRYPTOS (and the pair's own alphabets when 20 or fewer pairs fit), any shift",
        "self_check_identity_vs_0244": selfcheck, "per_class": table, "smallest_class_p": minp, "classes": len(table),
        "key_word_matches": {"k4": km, "copies_median": float(np.median(cm)), "copies_max": max(cm),
                             "p_at_or_above": round((1 + sum(x >= km for x in cm)) / (N_COPIES + 1), 3)},
        "k4_best_readings": [[round(c["_score"], 3), c["plaintext"], c["key"]] for c in cands[:10]],
        "plants": pfound, "plants_found": sum(p["found"] for p in pfound), "plants_total": len(pfound),
        "texts": len(texts), "exhaustive": True,
        "core_seconds": round(sum(v["secs"] for v in res.values())), "compute_seconds": round(time.time() - t_start),
        "resumed_units": len(jobs) - len(todo),
        "cost_estimate": "1.45 million settings x 51 texts, about 0.2 s per setting for all texts and both forms (desk 2026-11-04) plus the key-word step: about 80-120 core-hours; AWS 32 cores about 3-4 h, about $2-3",
    }
    notes = (f"F14.2: {len(lib)} moves x 2 orders x 26 lengths x 2 forms, 208,064^2 keyword alphabet pairs each; key-word matches "
             f"K4 {km}, copies median {np.median(cm)}, max {max(cm)}; smallest per-class p {minp} over {len(table)} classes; "
             f"plants found {bounds['plants_found']}/{len(pfound)}.")
    out = {"candidates": [{"plaintext": c["plaintext"], "key": c["key"]} for c in cands], "bounds": bounds, "notes": notes}
    if len(controls) >= 10:
        out["controls"] = controls
    return out


def worked_example(ctx, key):
    return "\n".join([
        "F14.2: a remembered route, then a table with two word-scrambled alphabets and a key word.", "",
        "  move       write the message in rows, read the columns in a key word's order (one of 27,852 moves)",
        "  checks     two known letters that share a key slot after the move: their gap on the plain alphabet",
        "             equals their carved letters' gap on the cipher alphabet (added form)",
        "  index      every keyword alphabet filed by its gaps, plain side and cipher side; matching files pair up",
        "  key word   the pair forces the key at the covered slots; a word of the key's length must give it",
        "  50 scrambled copies of K4 through the same steps give chance's counts."])
