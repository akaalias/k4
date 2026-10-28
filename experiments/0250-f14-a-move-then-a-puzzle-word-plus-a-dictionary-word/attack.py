"""Experiment 0250. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f14-a-move-then-a-puzzle-word-plus-a-dictionary-word",
    "title": "F14.6c: every move of the type-1 library (either order), then the sculpture's table with a puzzle word and a dictionary word summed as the key; the known letters force the dictionary word, looked up among every rotation; K4 against 30 shuffles, 8 plants",
    "family": "14-scheidt-mask-keyed-by-words",
    "parent": "0115-a-puzzle-word-plus-any-english-word",
    "changed": (
        "F14.6c (issue #93; reports/f14.6-grammar.md form 9). 0115 summed a puzzle word and a dictionary word with no move; "
        "F6 (0110-0114, 0129) put single keys of length 1-26 after or before every move. The sum of two words repeats only "
        "every lcm(m, n) letters, beyond every F6 length. Here: 27,852 moves x 2 orders x 24 rules x 1,085 puzzle-word "
        "starts (1.45 x 10^9 settings per text); for each, the known letters force the dictionary word at the slots they "
        "cover (bit-packed same-slot checks over all moves at once), and the forced word is looked up among every "
        "rotation of every dictionary word of 3-24 letters."
    ),
    "hypothesis_expert": (
        "C1(a) (Sanborn's matrix, then the table), C5 ('key word/s'), C20(a) ('layer two' as a second pass with a second "
        "word), Scheidt's 'building layers... mix and match'. K3's matrix, then K1/K2's table used twice with two "
        "remembered words. Pre-registered: no setting fits K4 (a hit needs the forced letters to spell a word); hit "
        "counts against 30 shuffles; a plant (Carter, random move, order, rule, puzzle word and dictionary word) is found "
        "when its own keys come back."
    ),
    "hypothesis_eli5": (
        "Shuffle the letters through a grid as in the third section, then use the table twice with two words, one from "
        "the puzzle and one any English word. Using the table twice is the same as using it once with the two words "
        "added. For every grid shuffle and every puzzle word, the clue words tell us exactly what the second word would "
        "have to be; we look it up in the dictionary."
    ),
    "prediction": "No hit on K4; none or almost none on shuffles; plants 8 of 8.",
    "method": (
        "1. Moves: 0129's type-1 library (27,852), orders A (move, then table) and B (table, then move). "
        "2. Rules: 24 (Vigenere, variant, Beaufort; plain, cipher and key alphabets standard or KRYPTOS). "
        "3. For each rule and puzzle-word start: the remainder the dictionary word must supply at each known place, for "
        "every move at once; same-slot agreement packed as bits; per length 3-24 and order, survivors' forced words "
        "looked up among every dictionary rotation (covered slots matched where the known places leave some uncovered). "
        "4. K4 and 30 shuffles; 8 plants with their own known letters; K4's hits decrypted and submitted."
    ),
    "walkthrough": (
        "1. Pick a move, say K3's rule with some numbers, and see where each known letter lands. "
        "2. Pick a rule of the table and a puzzle word with its start, say KRYPTOS from its K. "
        "3. At each known place, the table needs some key letter; take KRYPTOS's letter off it: the rest is the second word's letter. "
        "4. For a second word of length 9, places in the same slot (landing place mod 9) must agree; then read the word off and look it up. "
        "5. Repeat for every move, order, rule, puzzle word and length, and for the shuffles of K4."
    ),
    "expected_minutes": 30,
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
MODES = {"vig": (1, -1), "beau": (-1, 1), "var": (1, 1)}   # p = PA[s*c + t*k]
RULES = [(m, pa, ca, ka) for m in MODES for pa in ("std", "kry") for ca in ("std", "kry") for ka in ("std", "kry")]
NS = list(range(3, 25))
N_COPIES = 30
PLANTS = 8
SEED = 250
_G = {}


def frozen(tag):
    path = next((ROOT / "experiments").glob(f"{tag}-*")) / "attack.py"
    spec = importlib.util.spec_from_file_location(f"frozen{tag}", path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    m.ROOT = ROOT
    return m


def alpha(a):
    return STD if a == "std" else KRY if a == "kry" else a


# ---- the cipher --------------------------------------------------------------------------------------
def keystream(key, n=N):
    KA = alpha(key["ka"])
    return [sum(KA.index(w[(i + o) % len(w)]) for w, o in key["words"]) % 26 for i in range(n)]


def table_enc(pt, key):
    PA, CA = alpha(key["pa"]), alpha(key["ca"])
    s, t = MODES[key["mode"]]
    k = keystream(key, len(pt))
    return "".join(CA[(s * (PA.index(ch) - t * k[i])) % 26] for i, ch in enumerate(pt))


def table_dec(ct, key):
    PA, CA = alpha(key["pa"]), alpha(key["ca"])
    s, t = MODES[key["mode"]]
    k = keystream(key, len(ct))
    return "".join(PA[(s * CA.index(ch) + t * k[i]) % 26] for i, ch in enumerate(ct))


def encrypt(plaintext, key):
    w = list(key["where"])
    if key["order"] == "A":
        moved = [""] * N
        for i, ch in enumerate(plaintext):
            moved[w[i]] = ch
        return table_enc("".join(moved), key)
    y = table_enc(plaintext, key)
    out = [""] * N
    for i, ch in enumerate(y):
        out[w[i]] = ch
    return "".join(out)


def decrypt(ct, key):
    w = list(key["where"])
    if key["order"] == "A":
        z = table_dec(ct, key)
        return "".join(z[w[i]] for i in range(N))
    return table_dec("".join(ct[w[i]] for i in range(N)), key)


# ---- the search --------------------------------------------------------------------------------------
def prepare(vocabulary, known):
    lib = frozen("0129").route_library(vocabulary)
    m115 = frozen("0115")
    puzzle = sorted({w for w in m115.SPACED.split() if len(w) >= 2} | {w for w in vocabulary if 2 <= len(w) <= 30} | set(m115.EXTRA))
    starts = [(w, o) for w in puzzle for o in range(len(w))]
    places = sorted(known)
    W = np.array([t for _, t in lib], dtype=np.int32)
    LAND = W[:, np.array(places) - 1]
    pairs = [(a, b) for a in range(24) for b in range(a + 1, 24)]
    PA_, PB_ = np.array([a for a, _ in pairs]), np.array([b for _, b in pairs])
    pad = 320 - len(pairs)

    def pack(boolmat):
        x = np.packbits(np.concatenate([boolmat, np.zeros((boolmat.shape[0], pad), dtype=bool)], axis=1), axis=1)
        return x.view(np.uint64)
    qidx = np.array(places) - 1
    SA = {n: pack((LAND[:, PA_] % n) == (LAND[:, PB_] % n)) for n in NS}
    SB = {n: pack(((qidx[PA_] % n) == (qidx[PB_] % n))[None, :]) for n in NS}
    words = [x.strip().upper() for x in (ROOT / "kryptos" / "data" / "words.txt").read_text().split()]
    rots = {}
    for w in words:
        if 3 <= len(w) <= 24 and w.isalpha():
            for r in range(len(w)):
                rots.setdefault(len(w), {}).setdefault(w[r:] + w[:r], (w, r))
    S = {ka: np.array([[alpha(ka).index(w[(i + o) % len(w)]) for i in qidx] for w, o in starts], dtype=np.int16) for ka in ("std", "kry")}
    _G.update(lib=lib, starts=starts, puzzle=puzzle, places=places, LAND=LAND, PA_=PA_, PB_=PB_, SA=SA, SB=SB, pack=pack, S=S,
              rotset={n: d for n, d in rots.items()},
              rotmat={n: (list(d.values()), np.array([[ord(c) - 65 for c in k] for k in d], dtype=np.int8)) for n, d in rots.items()})


def lookup(vals, n, KA):
    """vals: {slot: key value}; -> list of (word, rotation) whose rotation gives those letters at those slots."""
    if len(vals) == n:
        k = "".join(KA[vals[s_]] for s_ in range(n))
        h = _G["rotset"][n].get(k)
        return [h] if h else []
    srcs, M = _G["rotmat"][n]
    cs = sorted(vals)
    tgt = np.array([ord(KA[vals[s_]]) - 65 for s_ in cs], dtype=np.int8)
    return [srcs[h] for h in np.nonzero((M[:, cs] == tgt).all(axis=1))[0][:5]]


def search(text, known):
    LAND, PA_, PB_, SA, SB, pack = _G["LAND"], _G["PA_"], _G["PB_"], _G["SA"], _G["SB"], _G["pack"]
    places, starts = _G["places"], _G["starts"]
    qidx = np.array(places) - 1
    tcodes = np.array([ord(c) - 65 for c in text])
    CL = tcodes[LAND]
    P = np.array([ord(known[q]) - 65 for q in places])
    surv = {f"{o}{n}": 0 for o in "AB" for n in NS}
    hits = []
    for mode, pa, ca, ka in RULES:
        PAs, CAs, KA = alpha(pa), alpha(ca), alpha(ka)
        pp = np.array([PAs.index(STD[x]) for x in range(26)])[P]
        cpos = np.array([CAs.index(STD[x]) for x in range(26)])[CL]
        K = {"vig": cpos - pp[None, :], "beau": cpos + pp[None, :], "var": pp[None, :] - cpos}[mode] % 26
        S = _G["S"][ka]
        for si in range(len(starts)):
            w1, o1 = starts[si]
            wv = np.array([KA.index(c) for c in w1], dtype=np.int16)
            # order A: the table runs over carved places, so the puzzle word is read at each known letter's landing place
            RA = (K - wv[(LAND + o1) % len(w1)]) % 26
            RB = (K - S[si][None, :]) % 26
            for o in "AB":
                R = RA if o == "A" else RB
                D = pack(R[:, PA_] != R[:, PB_])
                for n in NS:
                    ok = ~((D & (SA[n] if o == "A" else SB[n])) != 0).any(axis=1)
                    idx = np.nonzero(ok)[0]
                    if len(idx) == 0:
                        continue
                    surv[f"{o}{n}"] += len(idx)
                    for m in idx:
                        sl = (LAND[m] % n) if o == "A" else (qidx % n)
                        vals = {}
                        for e, s_ in enumerate(sl):
                            vals.setdefault(int(s_), int(R[m, e]))
                        for w2, r2 in lookup(vals, n, KA):
                            hits.append({"mode": mode, "pa": pa, "ca": ca, "ka": ka, "order": o, "move_index": int(m),
                                         "words": [list(starts[si]), [w2, r2]]})
    return {"survivors": surv, "hits": hits}


def _job(args):
    tid, text, known = args
    return tid, search(text, known)


def full_key(h):
    lib = _G["lib"]
    return {"mode": h["mode"], "pa": h["pa"], "ca": h["ca"], "ka": h["ka"], "order": h["order"], "words": h["words"],
            "move": lib[h["move_index"]][0], "where": list(lib[h["move_index"]][1])}


def run(ctx):
    import multiprocessing as mp
    t0 = time.time()
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    k4, known = ctx.K4, ctx.KNOWN
    prepare(ctx.vocabulary, known)
    lib, starts = _G["lib"], _G["starts"]
    rng = random.Random(SEED)
    texts = [("k4", k4, known)]
    for i in range(N_COPIES):
        s_ = list(k4); rng.shuffle(s_); texts.append((f"copy{i}", "".join(s_), known))
    carter = "".join(c for c in (ROOT / "knowledge" / "sources" / "carter-1923-tomb-of-tutankhamen-vol1.txt").read_text(errors="ignore").upper() if "A" <= c <= "Z")
    plants = {}
    for j in range(PLANTS):
        o_ = rng.randrange(len(carter) // 2, len(carter) - N)
        pt = carter[o_:o_ + N]
        n = rng.choice(NS)
        srcs, _ = _G["rotmat"][n]
        w2, r2 = srcs[rng.randrange(len(srcs))]
        mi = rng.randrange(len(lib))
        mode, pa, ca, ka = RULES[rng.randrange(len(RULES))]
        key = {"mode": mode, "pa": pa, "ca": ca, "ka": ka, "order": rng.choice("AB"), "words": [list(rng.choice(starts)), [w2, r2]],
               "move": lib[mi][0], "where": list(lib[mi][1])}
        pc = encrypt(pt, key)
        assert decrypt(pc, key) == pt
        pid = f"plant{j}"
        plants[pid] = {"key": key, "pt": pt, "ct": pc, "n": n}
        texts.append((pid, pc, {q: pt[q - 1] for q in known}))
    res = {}
    workers = int(os.environ.get("K4_WORKERS", 8))
    ctx.progress(0, len(texts), "texts searched")
    with mp.get_context("fork").Pool(workers) as pool:
        for tid, out in pool.imap_unordered(_job, texts, chunksize=1):
            res[tid] = out
            ctx.progress(len(res), len(texts), "texts searched")
    cells, above = {}, []
    for c_ in res["k4"]["survivors"]:
        k = res["k4"]["survivors"][c_]; cs = [res[f"copy{i}"]["survivors"][c_] for i in range(N_COPIES)]
        cells[c_] = {"k4": k, "copies_median": float(np.median(cs)), "copies_max": max(cs)}
        if k > max(cs):
            above.append(c_)
    found = {}
    for pid, p in plants.items():
        found[pid] = any(decrypt(p["ct"], full_key(h)) == p["pt"] for h in res[pid]["hits"])
    cands = [{"plaintext": decrypt(k4, full_key(h)), "key": full_key(h)} for h in res["k4"]["hits"][:100]]
    from kryptos.scorer import free_text
    controls = []
    for i in range(N_COPIES):
        hs = res[f"copy{i}"]["hits"][:20]
        if hs:
            controls.append(max(ctx.english_score(free_text(decrypt(texts[1 + i][1], full_key(h)))) for h in hs))
    bounds = {
        "item": "F14.6c", "moves": len(lib), "orders": 2, "rules": len(RULES), "puzzle_word_starts": len(starts),
        "settings_per_text": len(lib) * 2 * len(RULES) * len(starts), "dictionary_word_lengths": [NS[0], NS[-1]],
        "survivors_by_order_and_length": {k: v for k, v in cells.items() if v["k4"] or v["copies_max"]},
        "cells_k4_above_every_copy": above,
        "hits": {"k4": len(res["k4"]["hits"]), "copies": [len(res[f"copy{i}"]["hits"]) for i in range(N_COPIES)]},
        "plants_found": sum(found.values()), "plants": PLANTS,
        "plant_detail": {k: {"found": v, "n": plants[k]["n"], "order": plants[k]["key"]["order"], "words": plants[k]["key"]["words"]} for k, v in found.items()},
        "texts": len(texts), "copies": N_COPIES, "exhaustive": True, "compute_seconds": round(time.time() - t0),
    }
    notes = (f"{bounds['settings_per_text']:,} settings per text; dictionary-word hits K4 {bounds['hits']['k4']}, shuffles max "
             f"{max(bounds['hits']['copies'])}; cells with K4 above every shuffle {len(above)} of {len(cells)}; plants {bounds['plants_found']}/{PLANTS}")
    out = {"candidates": cands, "bounds": bounds, "notes": notes}
    if len(controls) >= 10:
        out["controls"] = controls
    return out


def worked_example(ctx, key):
    known, ct = ctx.KNOWN, ctx.K4
    lines = ["No move, KRYPTOS table (Vigenere), KRYPTOS from K as the puzzle word; the dictionary word's forced letters:", "",
             "place  known  carved  key value  KRYPTOS  second word's letter"]
    for q in (22, 23, 24, 25, 64, 65, 66):
        k = (KRY.index(ct[q - 1]) - KRY.index(known[q])) % 26
        a = KRY.index("KRYPTOS"[(q - 1) % 7])
        lines.append(f"{q:>5}  {known[q]:>5}  {ct[q - 1]:>6}  {k:>9}  {KRY[a]:>7}  {KRY[(k - a) % 26]:>20}")
    lines += ["", "With a move, each known letter's slot is its landing place (order A) or its message place (order B) mod the word length."]
    return "\n".join(lines)
