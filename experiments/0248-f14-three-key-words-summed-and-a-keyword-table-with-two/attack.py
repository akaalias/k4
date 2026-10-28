"""Experiment 0248. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f14-three-key-words-summed-and-a-keyword-table-with-two",
    "title": "F14.6a: three puzzle key words summed on the sculpture's tables, and a puzzle keyword table with a puzzle word plus a dictionary word summed; the known letters force the last word, looked up among every rotation; K4 against 50 shuffles, plants of both forms",
    "family": "14-scheidt-mask-keyed-by-words",
    "parent": "0115-a-puzzle-word-plus-any-english-word",
    "changed": (
        "F14.6a (issue #93; reports/f14.6-grammar.md forms 8 and 11). 0059 summed two puzzle words, 0115 a puzzle word "
        "and a dictionary word, both on the standard and KRYPTOS tables only. Form 8: three puzzle words (171, every "
        "start) summed, 24 rules; for every pair of the first two (with starts) the 24 known letters force the third at "
        "the slots they cover, looked up among every rotation of every puzzle word of that length (2-30; for lengths with "
        "slots no known place covers, matched on the covered slots). Form 11: a keyword-mixed alphabet from a puzzle word "
        "(170) on the plain side, the cipher side or both, with a puzzle word plus a dictionary word (3-24) summed as the "
        "key: 5,100 table setups x 1,085 puzzle-word starts, the dictionary word forced and looked up as 0115."
    ),
    "hypothesis_expert": (
        "Scheidt: 'building layers... mix and match' (2015), 'key word/s' (C5), keys from parts (his key-splitting habit); "
        "C20(a) 'layer two' as further passes; C4(a) a keyword-alphabet mask. Three passes over the table with three "
        "remembered words is one table with the summed key (period lcm of the lengths, often beyond 97), so no periodic "
        "test sees it, but the known letters force the last word once the others are guessed. Pre-registered: no "
        "setting fits K4 beyond the shuffles' rate (counts of forced-word hits per form, K4 against 50 shuffles, flag at "
        "p < 0.05/2); a fit is decrypted and judged by the gates. A plant of each form (Carter, keys drawn from the same "
        "lists) is found when its own keys come back."
    ),
    "hypothesis_eli5": (
        "Using the sculpture's table three times, each time with a different remembered word, is the same as using it "
        "once with a key made by adding the three words letter by letter. If we guess the first two words, the clue "
        "words tell us exactly what the third must be, so we only need to look it up. We also try a table scrambled by "
        "one puzzle word with a key made of two words. Shuffles of K4 go through the same search."
    ),
    "prediction": "Form 8: no hit on K4, a few or none on shuffles. Form 11: no hit on K4, as the shuffles. Plants 8 of 8 per form.",
    "method": (
        "1. Puzzle words: 0115's 171 (every start: 1,085); keyword alphabets of the puzzle words: 170; dictionary "
        "rotations of 3-24 letters (0115). "
        "2. Form 8: 24 rules (Vigenere, variant, Beaufort; plain, cipher and key alphabets standard or KRYPTOS). For each "
        "rule and each pair of puzzle-word starts, the forced remainder at the 24 known places; for each length 2-30, "
        "slots must agree, and the third word is looked up. "
        "3. Form 11: 5,100 setups (keyword alphabet W on both sides, W with standard or KRYPTOS, either side; 3 rules; key "
        "letters numbered on standard or KRYPTOS); each puzzle-word start; the dictionary word of length 3-24 forced and "
        "looked up. "
        "4. K4 and 50 shuffles; 8 plants per form with their own known letters. "
        "5. K4's hits decrypted in full and submitted."
    ),
    "walkthrough": (
        "1. Pick a rule of the table and two puzzle words with their starting letters, say KRYPTOS from K and ABSCISSA from A. "
        "2. At each known place work out the key letter the table needs, and take off the two words' letters there. "
        "3. What is left at each known place is the third word's letter at that place; places a word-length apart must agree. "
        "4. If they agree for some length, read the third word off and look it up among the puzzle words, from every starting letter. "
        "5. Repeat for every pair, rule and length, and for the shuffles of K4."
    ),
    "expected_minutes": 20,
}

import json
import os
import random
import re
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
N_COPIES = 50
PLANTS = 8
SEED = 248
_G = {}

SPACED = (
    "BETWEEN SUBTLE SHADING AND THE ABSENCE OF LIGHT LIES THE NUANCE OF IQLUSION "
    "IT WAS TOTALLY INVISIBLE HOWS THAT POSSIBLE THEY USED THE EARTHS MAGNETIC FIELD X THE INFORMATION WAS GATHERED AND "
    "TRANSMITTED UNDERGRUUND TO AN UNKNOWN LOCATION X DOES LANGLEY KNOW ABOUT THIS THEY SHOULD ITS BURIED OUT THERE "
    "SOMEWHERE X WHO KNOWS THE EXACT LOCATION ONLY WW THIS WAS HIS LAST MESSAGE X THIRTY EIGHT DEGREES FIFTY SEVEN "
    "MINUTES SIX POINT FIVE SECONDS NORTH SEVENTY SEVEN DEGREES EIGHT MINUTES FORTY FOUR SECONDS WEST ID BY ROWS "
    "SLOWLY DESPARATLY SLOWLY THE REMAINS OF PASSAGE DEBRIS THAT ENCUMBERED THE LOWER PART OF THE DOORWAY WAS REMOVED "
    "WITH TREMBLING HANDS I MADE A TINY BREACH IN THE UPPER LEFT HAND CORNER AND THEN WIDENING THE HOLE A LITTLE I "
    "INSERTED THE CANDLE AND PEERED IN THE HOT AIR ESCAPING FROM THE CHAMBER CAUSED THE FLAME TO FLICKER BUT PRESENTLY "
    "DETAILS OF THE ROOM WITHIN EMERGED FROM THE MIST X CAN YOU SEE ANYTHING Q"
)
EXTRA = ["EGYPT", "CAIRO", "LUXOR", "WALL", "NOVEMBER", "MESSAGE", "DELIVER", "DELIVERING", "TRANSMIT", "LAYERTWO",
         "WONDERFULTHINGS", "BERLINWALL", "WELTZEITUHR", "ALEXANDERPLATZ", "SHADOWFORCES", "LUCIDMEMORY"]


def keyed(word):
    seen = []
    for c in word:
        if c not in seen:
            seen.append(c)
    return "".join(seen) + "".join(c for c in STD if c not in seen)


def lists(vocabulary):
    puzzle = sorted({w for w in SPACED.split() if len(w) >= 2} | {w.upper() for w in vocabulary if 2 <= len(w) <= 30} | set(EXTRA))
    starts = [(w, o) for w in puzzle for o in range(len(w))]
    prot = {}
    for w in puzzle:
        for r in range(len(w)):
            prot.setdefault(len(w), {}).setdefault(w[r:] + w[:r], (w, r))
    words = [w.strip().upper() for w in (ROOT / "kryptos" / "data" / "words.txt").read_text().split()]
    drot = {}
    for w in words:
        if 3 <= len(w) <= 24 and w.isalpha():
            for r in range(len(w)):
                drot.setdefault(len(w), {}).setdefault(w[r:] + w[:r], (w, r))
    mixed = {}
    for w in puzzle:
        a = keyed(w)
        if a not in (STD, KRY):
            mixed.setdefault(a, w)
    return puzzle, starts, prot, drot, mixed


def alpha(a):
    return STD if a == "std" else KRY if a == "kry" else a


# ---- the cipher --------------------------------------------------------------------------------------
def keystream(key, n=N):
    KA = alpha(key["ka"])
    return [sum(KA.index(w[(i + o) % len(w)]) for w, o in key["words"]) % 26 for i in range(n)]


def encrypt(plaintext, key):
    PA, CA = alpha(key["pa"]), alpha(key["ca"])
    s, t = MODES[key["mode"]]
    k = keystream(key, len(plaintext))
    return "".join(CA[(s * (PA.index(ch) - t * k[i])) % 26] for i, ch in enumerate(plaintext))


def decrypt(ct, key):
    PA, CA = alpha(key["pa"]), alpha(key["ca"])
    s, t = MODES[key["mode"]]
    k = keystream(key, len(ct))
    return "".join(PA[(s * CA.index(ch) + t * k[i]) % 26] for i, ch in enumerate(ct))


# ---- the search --------------------------------------------------------------------------------------
def forced(text, known, mode, PA, CA):
    """Key value (in the key alphabet's numbering) the table needs at each known place."""
    out = []
    for q in _G["places"]:
        c, p = CA.index(text[q - 1]), PA.index(known[q])
        out.append({"vig": c - p, "beau": c + p, "var": p - c}[mode] % 26)
    return np.array(out)


def stream_at_places(starts, KA):
    """(len(starts), 24): each word-start's key value at the known places."""
    idx = np.array(_G["places"]) - 1
    return np.array([[KA.index(w[(i + o) % len(w)]) for i in idx] for w, o in starts], dtype=np.int16)


def lookups(R, KA, rot_by_len, lengths):
    """R (rows, 24) forced remainders; -> list of (row, length, (word, rotation)) where the remainder is a word rotation."""
    hits = []
    idx = np.array(_G["places"]) - 1
    for n in lengths:
        if n not in rot_by_len:
            continue
        sl = idx % n
        groups = {}
        for e, s_ in enumerate(sl):
            groups.setdefault(int(s_), []).append(e)
        ok = np.ones(len(R), dtype=bool)
        for es in groups.values():
            for e in es[1:]:
                ok &= R[:, e] == R[:, es[0]]
        rows = np.nonzero(ok)[0]
        if len(rows) == 0:
            continue
        cover = sorted(groups)
        table = rot_by_len[n]
        full = len(cover) == n
        for r in rows:
            vals = {s_: int(R[r, groups[s_][0]]) for s_ in cover}
            if full:
                key = "".join(KA[vals[s_]] for s_ in range(n))
                if key in table:
                    hits.append((int(r), n, table[key]))
            else:
                pat = re.compile("".join(KA[vals[s_]] if s_ in vals else "." for s_ in range(n)))
                for kstr, src in table.items():
                    if pat.fullmatch(kstr):
                        hits.append((int(r), n, src))
    return hits


def search(text, known):
    puzzle, starts, prot, drot, mixed = _G["lists"]
    out = {"form8": [], "form11": []}
    for mode in MODES:                                         # form 8: three puzzle words on the sculpture's tables
        for pa in ("std", "kry"):
            for ca in ("std", "kry"):
                for ka in ("std", "kry"):
                    KA = alpha(ka)
                    K = forced(text, known, mode, alpha(pa), alpha(ca))
                    S = _G["S"][ka]
                    for i1 in range(len(starts)):
                        R = (K[None, :] - S[i1][None, :] - S[i1:]) % 26
                        for r, n, src in lookups(R, KA, _G["prot_k"][ka], range(2, 31)):
                            out["form8"].append({"mode": mode, "pa": pa, "ca": ca, "ka": ka,
                                                 "words": [list(starts[i1]), list(starts[i1 + r]), list(src)]})
    for a in mixed:                                            # form 11: a puzzle keyword table, puzzle + dictionary word
        for pa, ca in ((a, a), (a, "std"), ("std", a), (a, "kry"), ("kry", a)):
            for ka in ("std", "kry"):
                KA = alpha(ka)
                S = _G["S"][ka]
                for mode in MODES:
                    K = forced(text, known, mode, alpha(pa), alpha(ca))
                    R = (K[None, :] - S) % 26
                    for r, n, src in lookups(R, KA, _G["drot_k"][ka], range(3, 25)):
                        out["form11"].append({"mode": mode, "pa": pa, "ca": ca, "ka": ka, "words": [list(starts[r]), list(src)]})
    return out


def _job(args):
    tid, text, known = args
    return tid, search(text, known)


def prepare(vocabulary, known):
    puzzle, starts, prot, drot, mixed = lists(vocabulary)
    _G["lists"] = (puzzle, starts, prot, drot, mixed)
    _G["places"] = sorted(known)
    _G["S"] = {ka: stream_at_places(starts, alpha(ka)) for ka in ("std", "kry")}
    # rotation tables keyed by the rotation's letters (as written in the key alphabet: the letters themselves)
    _G["prot_k"] = {ka: prot for ka in ("std", "kry")}
    _G["drot_k"] = {ka: drot for ka in ("std", "kry")}


def run(ctx):
    import multiprocessing as mp
    t0 = time.time()
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    k4, known = ctx.K4, ctx.KNOWN
    prepare(ctx.vocabulary, known)
    puzzle, starts, prot, drot, mixed = _G["lists"]
    k1 = json.loads((ROOT / "data" / "k1.json").read_text())
    pt1 = k1["plaintext"]; ct1 = k1["ciphertext"][:len(pt1)]
    key1 = {"mode": "vig", "pa": "kry", "ca": "kry", "ka": "kry", "words": [["PALIMPSEST", 0]]}
    assert encrypt(pt1, key1) == ct1 and decrypt(ct1, key1) == pt1, "K1 self-check failed"
    rng = random.Random(SEED)
    texts = [("k4", k4, known)]
    for i in range(N_COPIES):
        s_ = list(k4); rng.shuffle(s_); texts.append((f"copy{i}", "".join(s_), known))
    carter = "".join(c for c in (ROOT / "knowledge" / "sources" / "carter-1923-tomb-of-tutankhamen-vol1.txt").read_text(errors="ignore").upper() if "A" <= c <= "Z")
    plants = {}
    dlist = {n: list(v.values()) for n, v in drot.items()}
    for form in ("form8", "form11"):
        for j in range(PLANTS):
            o = rng.randrange(len(carter) // 2, len(carter) - N)
            pt = carter[o:o + N]
            if form == "form8":
                key = {"mode": rng.choice(list(MODES)), "pa": rng.choice(("std", "kry")), "ca": rng.choice(("std", "kry")),
                       "ka": rng.choice(("std", "kry")), "words": [list(rng.choice(starts)) for _ in range(3)]}
            else:
                a = rng.choice(list(mixed))
                pa, ca = rng.choice(((a, a), (a, "std"), ("std", a), (a, "kry"), ("kry", a)))
                n = rng.randrange(3, 25)
                key = {"mode": rng.choice(list(MODES)), "pa": pa, "ca": ca, "ka": rng.choice(("std", "kry")),
                       "words": [list(rng.choice(starts)), list(rng.choice(dlist[n]))]}
            pc = encrypt(pt, key)
            assert decrypt(pc, key) == pt
            pid = f"{form}_plant{j}"
            plants[pid] = {"form": form, "key": key, "pt": pt, "ct": pc}
            texts.append((pid, pc, {q: pt[q - 1] for q in known}))
    res = {}
    workers = int(os.environ.get("K4_WORKERS", 8))
    ctx.progress(0, len(texts), "texts searched")
    with mp.get_context("fork").Pool(workers) as pool:
        for tid, out in pool.imap_unordered(_job, texts, chunksize=1):
            res[tid] = out
            ctx.progress(len(res), len(texts), "texts searched")
    summary, p = {}, {}
    for form in ("form8", "form11"):
        k = len(res["k4"][form]); c = [len(res[f"copy{i}"][form]) for i in range(N_COPIES)]
        p[form] = (1 + sum(1 for x in c if x >= k)) / (N_COPIES + 1) if k else 1.0
        summary[form] = {"k4_hits": k, "copies_hits_max": max(c), "copies_hits_median": float(np.median(c)),
                         "copies_with_any": sum(1 for x in c if x), "p": round(p[form], 4)}
    found = {}
    for pid, pl in plants.items():
        hit = any(decrypt(pl["ct"], {**h, "words": [tuple(w) for w in h["words"]]}) == pl["pt"] for h in res[pid][pl["form"]])
        found[pid] = bool(hit)
    cands = []
    for form in ("form8", "form11"):
        for h in res["k4"][form][:100]:
            cands.append({"plaintext": decrypt(k4, h), "key": h})
    from kryptos.scorer import free_text
    controls = []
    for i in range(N_COPIES):
        hs = res[f"copy{i}"]["form8"][:20] + res[f"copy{i}"]["form11"][:20]
        if hs:
            controls.append(max(ctx.english_score(free_text(decrypt(texts[1 + i][1], h))) for h in hs))
    bounds = {
        "item": "F14.6a (forms 8 and 11)", "puzzle_words": len(puzzle), "puzzle_word_starts": len(starts),
        "puzzle_alphabets": len(mixed), "form8_settings_per_text": 24 * len(starts) * (len(starts) + 1) // 2,
        "form8_third_word_lengths": [2, 30], "form11_setups": len(mixed) * 5 * 2 * 3, "form11_dictionary_word_lengths": [3, 24],
        "summary": summary, "flag_alpha": 0.025,
        "plants_found": {f: sum(v for k_, v in found.items() if k_.startswith(f)) for f in ("form8", "form11")},
        "plants_per_form": PLANTS, "k4_hits": {f: res["k4"][f][:20] for f in ("form8", "form11")},
        "texts": len(texts), "copies": N_COPIES, "exhaustive": True, "compute_seconds": round(time.time() - t0),
    }
    notes = (f"form 8 (three puzzle words): K4 {summary['form8']['k4_hits']} hits, shuffles max {summary['form8']['copies_hits_max']}; "
             f"form 11 (puzzle table, puzzle + dictionary word): K4 {summary['form11']['k4_hits']}, shuffles max {summary['form11']['copies_hits_max']}; "
             f"plants {bounds['plants_found']}")
    out = {"candidates": cands, "bounds": bounds, "notes": notes}
    if len(controls) >= 10:
        out["controls"] = controls
    return out


def worked_example(ctx, key):
    known, ct = ctx.KNOWN, ctx.K4
    lines = ["Three words summed on the KRYPTOS table (Vigenere): KRYPTOS from K, ABSCISSA from A; the third word forced", "",
             "place  known  carved  key value  KRYPTOS  ABSCISSA  third word's letter"]
    for q in (22, 23, 24, 25, 26, 64, 65):
        k = (KRY.index(ct[q - 1]) - KRY.index(known[q])) % 26
        a = KRY.index("KRYPTOS"[(q - 1) % 7]); b = KRY.index("ABSCISSA"[(q - 1) % 8])
        lines.append(f"{q:>5}  {known[q]:>5}  {ct[q - 1]:>6}  {k:>9}  {KRY[a]:>7}  {KRY[b]:>8}  {KRY[(k - a - b) % 26]:>18}")
    lines += ["", "Places a word-length apart must ask the same letter; the forced word is looked up from every start."]
    return "\n".join(lines)
