"""Experiment 0249. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f14-puzzle-keyword-alphabets-around-a-move-with-a-key-word",
    "title": "F14.6b: keyword alphabets from the puzzle words around every move of the type-1 library (either order), the key a word of any length 1-26; every setting decided exactly by the known letters, the key words looked up; K4 against 30 shuffles, 8 plants",
    "family": "14-scheidt-mask-keyed-by-words",
    "parent": "0129-one-free-alphabet-after-every-move-exact",
    "changed": (
        "F14.6b (issue #93; reports/f14.6-grammar.md form 10). 0129 and 0130 put one free alphabet (any of 26!) around "
        "every type-1 move and found fits from key length 6 at the copies' rate, undecidable. Here the alphabets are the "
        "keyword alphabets of the 170 puzzle words (plain side, cipher side or both; with the standard or KRYPTOS alphabet "
        "on the other side), plus the four standard/KRYPTOS pairs: 854 tables x 2 forms x 27,852 moves x 2 orders x key "
        "lengths 1-26, each decided exactly by the 24 known letters (the same-slot places must ask the same key value; "
        "packed as bit masks per move). Every surviving setting's forced key is then checked against every dictionary "
        "and puzzle word of the length, every start, numbered on standard, KRYPTOS, the plain or the cipher alphabet, "
        "any shift, in the Vigenere, variant and Beaufort readings."
    ),
    "hypothesis_expert": (
        "C1(a) (Sanborn, CNN 2005: 'I used a matrix code, and then... went back to this table'), C4(a) (Scheidt's mask as a "
        "keyword alphabet), C5 ('key word/s'), C27(c) (a 'slightly different' table). The mask (a keyword alphabet), K3's "
        "matrix and K1/K2's table in one procedure of three hand steps, every key from the puzzle's own words. A free "
        "alphabet leaves these cells undecided (0129, 0130; F6.1 blocked by cost); 170 alphabets are under 8 bits, so the "
        "known letters decide. Pre-registered: no setting fits K4 beyond the shuffles' counts, per order and key length "
        "(52 cells; flag at p < 0.05/52 against 30 shuffles: unreachable, so a cell above every shuffle is a candidate to "
        "replicate); no key word fits K4. A plant (Carter, random puzzle table, move, order and dictionary key word) is "
        "found when its setting survives and its key word comes back."
    ),
    "hypothesis_eli5": (
        "Three hand steps the creators taught each other: scramble the alphabet with a word, shuffle the letters through "
        "a grid as in the third section, then use the table with a key word. We try every grid shuffle in our library, "
        "every alphabet made from a word of the puzzle, and every key length, and the clue words tell us exactly which "
        "combinations are possible. For those we check whether the key is an English word."
    ),
    "prediction": "K4 fits at the shuffles' rate in every cell (few settings below length 16); no key word on K4; plants 8 of 8.",
    "method": (
        "1. Moves: 0129's type-1 library (27,852 distinct, from its frozen route_library). Orders: A (move, then the table: "
        "slot = landing place mod L) and B (table, then the move: slot = message place mod L). "
        "2. Tables: for each puzzle keyword alphabet W, (W, W), (W, std), (std, W), (W, KRY), (KRY, W); plus std/KRY pairs. "
        "Forms: added (Vigenere and variant agree on consistency) and Beaufort. "
        "3. Per text, table and form: forced key value at each known place for every move at once; the pairs of known "
        "places that disagree packed as bits; a (move, order, L) setting survives if no disagreeing pair shares a slot. "
        "4. Survivors: key words of length L (dictionary 3-24, puzzle 2-30) matched at the covered slots up to a shift, "
        "four numberings, three readings. "
        "5. K4 and 30 shuffles; 8 plants with their own known letters; K4's key-word fits decrypted and submitted."
    ),
    "walkthrough": (
        "1. Take a puzzle word, say SHADOW, and write its keyword alphabet: SHADOWBCEFGIJKLMNPQRTUVXYZ. "
        "2. Take a move, say a quarter turn of a grid 7 wide, and find where each known letter lands in the carved text. "
        "3. Take a key length, say 11: each known letter's key slot is its landing place mod 11. "
        "4. On the table with SHADOW's alphabet, work out the key value each known letter needs; two in one slot must agree. "
        "5. If all agree, read the key letters off the slots and look for an English word that gives them from some start."
    ),
    "expected_minutes": 40,
}

import importlib.util
import json
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
LMAX = 26
N_COPIES = 30
PLANTS = 8
SEED = 249
_G = {}


def frozen(tag):
    path = next((ROOT / "experiments").glob(f"{tag}-*")) / "attack.py"
    spec = importlib.util.spec_from_file_location(f"frozen{tag}", path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    m.ROOT = ROOT
    return m


def keyed(word):
    seen = []
    for c in word:
        if c not in seen:
            seen.append(c)
    return "".join(seen) + "".join(c for c in STD if c not in seen)


def alpha(a):
    return STD if a == "std" else KRY if a == "kry" else a


def moves(vocabulary):
    if "lib" not in _G:
        _G["lib"] = frozen("0129").route_library(vocabulary)
    return _G["lib"]


# ---- the cipher --------------------------------------------------------------------------------------
def kvals(key, n=N):
    KA = alpha({"plain": key["pa"], "cipher": key["ca"]}.get(key["ka"], key["ka"]))
    w, o = key["word"], key["start"]
    v = [(KA.index(w[(i + o) % len(w)]) + key["shift"]) % 26 for i in range(n)]
    return [(-x) % 26 for x in v] if key["mode"] == "var" else v


def table_enc(pt, key):
    PA, CA, k = alpha(key["pa"]), alpha(key["ca"]), kvals(key, len(pt))
    if key["mode"] == "beau":
        return "".join(CA[(k[i] - PA.index(p)) % 26] for i, p in enumerate(pt))
    return "".join(CA[(PA.index(p) + k[i]) % 26] for i, p in enumerate(pt))


def table_dec(ct, key):
    PA, CA, k = alpha(key["pa"]), alpha(key["ca"]), kvals(key, len(ct))
    if key["mode"] == "beau":
        return "".join(PA[(k[i] - CA.index(c)) % 26] for i, c in enumerate(ct))
    return "".join(PA[(CA.index(c) - k[i]) % 26] for i, c in enumerate(ct))


def where_of(key):
    if "where" in key:
        return list(key["where"])
    return list(dict(_G["lib"])[key["move"]]) if "lib" in _G else None


def encrypt(plaintext, key):
    w = where_of(key)
    if key["order"] == "A":                          # move, then the table
        moved = [""] * N
        for i, ch in enumerate(plaintext):
            moved[w[i]] = ch
        return table_enc("".join(moved), key)
    y = table_enc(plaintext, key)                    # the table, then the move
    out = [""] * N
    for i, ch in enumerate(y):
        out[w[i]] = ch
    return "".join(out)


def decrypt(ct, key):
    w = where_of(key)
    if key["order"] == "A":
        z = table_dec(ct, key)
        return "".join(z[w[i]] for i in range(N))
    return table_dec("".join(ct[w[i]] for i in range(N)), key)


# ---- the search --------------------------------------------------------------------------------------
def prepare(vocabulary, known):
    lib = moves(vocabulary)
    places = sorted(known)
    W = np.array([t for _, t in lib], dtype=np.int32)                 # (nm, 97) where[i]
    LAND = W[:, np.array(places) - 1]                                  # (nm, 24) carved index of each known letter
    pairs = [(a, b) for a in range(24) for b in range(a + 1, 24)]
    PA_, PB_ = np.array([a for a, _ in pairs]), np.array([b for _, b in pairs])
    pad = 320 - len(pairs)

    def pack(boolmat):
        x = np.packbits(np.concatenate([boolmat, np.zeros((boolmat.shape[0], pad), dtype=bool)], axis=1), axis=1)
        return x.view(np.uint64)
    SA = {L: pack((LAND[:, PA_] % L) == (LAND[:, PB_] % L)) for L in range(1, LMAX + 1)}
    qidx = np.array(places) - 1
    SB = {L: pack(((qidx[PA_] % L) == (qidx[PB_] % L))[None, :]) for L in range(1, LMAX + 1)}
    puzzle = sorted({w.upper() for w in vocabulary if w.isalpha() and len(w) >= 2} |
                    set(frozen("0115").SPACED.split()) | set(frozen("0115").EXTRA))
    puzzle = [w for w in puzzle if len(w) >= 2]
    tables = []
    for w in puzzle:
        a = keyed(w)
        if a in (STD, KRY) or any(t[2] == a for t in tables):
            continue
        for pa, ca in ((a, a), (a, "std"), ("std", a), (a, "kry"), ("kry", a)):
            tables.append((pa, ca, a, w))
    for pa in ("std", "kry"):
        for ca in ("std", "kry"):
            tables.append((pa, ca, None, None))
    words = [x.strip().upper() for x in (ROOT / "kryptos" / "data" / "words.txt").read_text().split()]
    rots = {}
    for w in [x for x in words if x.isalpha() and 3 <= len(x) <= 24] + puzzle:
        if len(w) <= LMAX:
            for r in range(len(w)):
                rots.setdefault(len(w), {}).setdefault(w[r:] + w[:r], (w, r))
    _G.update(places=places, LAND=LAND, PA_=PA_, PB_=PB_, SA=SA, SB=SB, pack=pack, tables=tables, puzzle=puzzle,
              rots={L: (list(d.values()), np.array([[ord(c) - 65 for c in s] for s in d], dtype=np.int16)) for L, d in rots.items()})


def key_word_hits(Kvals, slots, L, pa, ca, form):
    """Kvals: forced key value per known place (added form: c - p; Beaufort: c + p); slots per known place."""
    if L not in _G["rots"]:
        return []
    srcs, M = _G["rots"][L]
    cov = {}
    for e, s_ in enumerate(slots):
        cov.setdefault(int(s_), int(Kvals[e]))
    cs = sorted(cov)
    sub = M[:, cs]
    hits = []
    readings = ("vig", "var") if form == "added" else ("beau",)
    for mode in readings:
        target = np.array([cov[s_] for s_ in cs]) % 26
        if mode == "var":
            target = (-target) % 26
        d = (target - target[0]) % 26
        for ka in ("std", "kry", "plain", "cipher"):
            A = alpha({"plain": pa, "cipher": ca}.get(ka, ka))
            lut = np.array([A.index(c) for c in STD], dtype=np.int16)
            v = lut[sub]
            dv = (v - v[:, :1]) % 26
            for h in np.nonzero((dv == d).all(axis=1))[0][:5]:
                w, r = srcs[h]
                hits.append({"mode": mode, "ka": ka, "word": w, "start": r,
                             "shift": int((target[0] - v[h, 0]) % 26), "L": L})
    return hits


def search(text, known):
    LAND, PA_, PB_, SA, SB, pack = _G["LAND"], _G["PA_"], _G["PB_"], _G["SA"], _G["SB"], _G["pack"]
    places = _G["places"]
    nm = LAND.shape[0]
    tcodes = np.array([ord(c) - 65 for c in text])
    CL = tcodes[LAND]                                                  # carved letter at each landing (nm, 24)
    P = np.array([ord(known[q]) - 65 for q in places])
    surv = {(o, L): 0 for o in "AB" for L in range(1, LMAX + 1)}
    hits = []
    for pa, ca, a, w in _G["tables"]:
        PAs, CAs = alpha(pa), alpha(ca)
        pp = np.array([PAs.index(STD[x]) for x in range(26)])[P]
        cpos = np.array([CAs.index(STD[x]) for x in range(26)])[CL]
        for form in ("added", "beaufort"):
            K = (cpos - pp[None, :]) % 26 if form == "added" else (cpos + pp[None, :]) % 26
            D = pack(K[:, PA_] != K[:, PB_])
            for o in "AB":
                for L in range(1, LMAX + 1):
                    S = SA[L] if o == "A" else SB[L]
                    ok = ~((D & S) != 0).any(axis=1)
                    idx = np.nonzero(ok)[0]
                    if len(idx) == 0:
                        continue
                    surv[(o, L)] += len(idx)
                    for m in idx:
                        slots = (LAND[m] % L) if o == "A" else ((np.array(places) - 1) % L)
                        for h in key_word_hits(K[m], slots, L, pa, ca, form):
                            hits.append({"pa": pa, "ca": ca, "order": o, "move_index": int(m), **h})
    return {"survivors": {f"{o}{L}": v for (o, L), v in surv.items()}, "hits": hits}


def _job(args):
    tid, text, known = args
    return tid, search(text, known)


def full_key(h):
    lib = _G["lib"]
    return {"pa": h["pa"], "ca": h["ca"], "mode": h["mode"], "ka": h["ka"], "word": h["word"], "start": h["start"],
            "shift": h["shift"], "order": h["order"], "move": lib[h["move_index"]][0], "where": list(lib[h["move_index"]][1])}


def key_slot_start(h, L):
    return h


def run(ctx):
    import multiprocessing as mp
    t0 = time.time()
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    k4, known = ctx.K4, ctx.KNOWN
    prepare(ctx.vocabulary, known)
    lib = _G["lib"]
    k1 = json.loads((ROOT / "data" / "k1.json").read_text())
    rng = random.Random(SEED)
    texts = [("k4", k4, known)]
    for i in range(N_COPIES):
        s_ = list(k4); rng.shuffle(s_); texts.append((f"copy{i}", "".join(s_), known))
    carter = "".join(c for c in (ROOT / "knowledge" / "sources" / "carter-1923-tomb-of-tutankhamen-vol1.txt").read_text(errors="ignore").upper() if "A" <= c <= "Z")
    plants = {}
    tabs = [t for t in _G["tables"] if t[2] is not None]
    for j in range(PLANTS):
        o_ = rng.randrange(len(carter) // 2, len(carter) - N)
        pt = carter[o_:o_ + N]
        pa, ca, a, w = rng.choice(tabs)
        L = rng.randrange(5, 25)
        srcs, _ = _G["rots"][L]
        word, r = srcs[rng.randrange(len(srcs))]
        mi = rng.randrange(len(lib))
        key = {"pa": pa, "ca": ca, "mode": rng.choice(("vig", "var", "beau")), "ka": rng.choice(("std", "kry", "plain", "cipher")),
               "word": word, "start": r, "shift": rng.randrange(26), "order": rng.choice("AB"), "move": lib[mi][0], "where": list(lib[mi][1])}
        pc = encrypt(pt, key)
        assert decrypt(pc, key) == pt
        pid = f"plant{j}"
        plants[pid] = {"key": key, "pt": pt, "ct": pc, "L": L}
        texts.append((pid, pc, {q: pt[q - 1] for q in known}))
    res = {}
    workers = int(os.environ.get("K4_WORKERS", 8))
    ctx.progress(0, len(texts), "texts searched")
    with mp.get_context("fork").Pool(workers) as pool:
        for tid, out in pool.imap_unordered(_job, texts, chunksize=1):
            res[tid] = out
            ctx.progress(len(res), len(texts), "texts searched")
    cells = {}
    above = []
    for o in "AB":
        for L in range(1, LMAX + 1):
            k = res["k4"]["survivors"][f"{o}{L}"]
            c = [res[f"copy{i}"]["survivors"][f"{o}{L}"] for i in range(N_COPIES)]
            cells[f"{o}{L}"] = {"k4": k, "copies_median": float(np.median(c)), "copies_max": max(c)}
            if k > max(c):
                above.append(f"{o}{L}")
    found = {}
    for pid, p in plants.items():
        k_ = p["key"]
        ok = False
        for h in res[pid]["hits"]:
            if h["order"] == k_["order"] and h["pa"] == k_["pa"] and h["ca"] == k_["ca"] and h["word"] == k_["word"]:
                if decrypt(p["ct"], full_key(h)) == p["pt"]:
                    ok = True; break
        found[pid] = ok
    cands = [{"plaintext": decrypt(k4, full_key(h)), "key": full_key(h)} for h in res["k4"]["hits"][:100]]
    from kryptos.scorer import free_text
    controls = []
    for i in range(N_COPIES):
        hs = res[f"copy{i}"]["hits"][:20]
        if hs:
            controls.append(max(ctx.english_score(free_text(decrypt(texts[1 + i][1], full_key(h)))) for h in hs))
    bounds = {
        "item": "F14.6b", "moves": len(lib), "tables": len(_G["tables"]), "puzzle_words": len(_G["puzzle"]),
        "settings_per_text": len(lib) * len(_G["tables"]) * 2 * 2 * LMAX,
        "survivors_by_order_and_length": cells, "cells_k4_above_every_copy": above,
        "key_word_hits": {"k4": len(res["k4"]["hits"]), "copies": [len(res[f"copy{i}"]["hits"]) for i in range(N_COPIES)]},
        "plants_found": sum(found.values()), "plants": PLANTS, "plant_detail": {k: {"found": v, "L": plants[k]["L"], "order": plants[k]["key"]["order"], "word": plants[k]["key"]["word"]} for k, v in found.items()},
        "texts": len(texts), "copies": N_COPIES, "exhaustive": True, "compute_seconds": round(time.time() - t0),
    }
    notes = (f"{bounds['settings_per_text']:,} settings per text; key-word hits K4 {bounds['key_word_hits']['k4']}, shuffles max "
             f"{max(bounds['key_word_hits']['copies'])}; cells with K4 above every shuffle {len(above)} of 52; plants {bounds['plants_found']}/{PLANTS}")
    out = {"candidates": cands, "bounds": bounds, "notes": notes}
    if len(controls) >= 10:
        out["controls"] = controls
    return out


def worked_example(ctx, key):
    known, ct = ctx.KNOWN, ctx.K4
    a = keyed("SHADOW")
    lines = [f"SHADOW's keyword alphabet {a} on both sides, added form, no move, key length 11:", "",
             "place  known  carved  key value  slot"]
    for q in (22, 23, 24, 25, 33, 34, 66, 67):
        lines.append(f"{q:>5}  {known[q]:>5}  {ct[q - 1]:>6}  {(a.index(ct[q - 1]) - a.index(known[q])) % 26:>9}  {(q - 1) % 11:>4}")
    lines += ["", "Places in the same slot must ask the same key value; with a move, the slot is the landing place mod 11."]
    return "\n".join(lines)
