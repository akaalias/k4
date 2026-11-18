"""Experiment: F16.3. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f16.3-keyword-alphabets-mixed-in-a-grid-at-dictionary-scale",
    "title": "F16.3: keyword alphabets mixed in a grid (the keyword, the rest of the alphabet in rows under it, read off by columns straight or in keyword order) for every dictionary word, paired with each other and with the straight keyword alphabets, a repeating key of length 1-24, the key free; fits and key words on the 24 and the 20 official letters; K4 against 20 shuffles, plants",
    "family": "16-simple-hand-methods",
    "parent": "0275-f16.1b-two-dictionary-keyword-alphabets-on-the-20-official-letters",
    "changed": (
        "F16.3 (issue #123). 0244 and 0275 paired straight keyword alphabets (the word, then the unused letters in "
        "order) for 208,064 dictionary and puzzle words; grid mixings were tried for about 250 puzzle words only (0010, "
        "0020). Here each word also gives two transposition-mixed alphabets, the US Army way (Friedman, Military "
        "Cryptanalysis I; Elementary Military Cryptography): write the keyword without repeats, the rest of the alphabet "
        "in rows under it, and read off by columns, left to right or in the alphabetical order of the keyword's letters. "
        "All three kinds are paired with each other (plain side and cipher side) through 0282's capped pair index, key "
        "lengths 1-24, both forms. Reported: fitting pairs against shuffles (the key free, #124) and key words for the "
        "forced key (lengths 3-23), which is not a gate."
    ),
    "hypothesis_expert": (
        "C27(c) (a tableau 'slightly different from the one on Kryptos'), C1(c), C4(a) (a keyword alphabet as the mask), "
        "C5 ('key word/s'), A16 (hand systems of 1890-1945 that Scheidt taught). Cipher: Quagmire IV, c = CA[PA^-1(p) + "
        "k_(i mod L)] (added) or CA[k - PA^-1(p)] (Beaufort), PA and CA each one of: the straight keyword alphabet, the "
        "grid alphabet read by columns left to right, the grid alphabet read in keyword order; key numbering standard, "
        "KRYPTOS, the plain or the cipher alphabet (0244's). Exact: 0244's same-slot index (two known places in one key "
        "slot must need the same key value) on all 24 known letters and on the 20 official ones. Sanborn puts 'matrix "
        "codes' among the parts already cracked (2009 oral history, knowledge/sources/aaa-oral-history-2009-kryptos.md), "
        "so the grid is a weaker lead; it is the Army's standard way to mix an alphabet all the same. A fit count cannot "
        "pick out a planted answer when the key is free (0274: 0 of 6), so the count is compared with the shuffles and "
        "the key-word check carries the power: plants are found by their key word."
    ),
    "hypothesis_eli5": (
        "The alphabet on the Kryptos table starts with KRYPTOS and goes on with the unused letters. The Army taught a "
        "second way to scramble an alphabet from a word: write the word, write the rest of the alphabet in rows under "
        "it, and read down the columns. We build such alphabets from every dictionary word, try every pair of them as "
        "the two sides of the table with a repeating key, and count the fits on the carving and on scrambled copies."
    ),
    "prediction": (
        "No key word for the forced key on K4 or any shuffle; fitting-pair counts inside the shuffles in every cell "
        "(the 19 cells aside, where 0282 saw the R/P repeat); plants found by their key word at least 10 of 12. No "
        "candidates."
    ),
    "method": (
        "1. For each word of 4 or more letters: its straight keyword alphabet and its two grid alphabets; duplicates "
        "dropped. 2. 0244's pair index over all of them (0282's capped version: cells with more than 5 million fitting "
        "pairs are counted, not listed). 3. For each text and each set of known letters (24, 20), key lengths 1-24, both "
        "forms: the number of fitting pairs; where listed, 0275's key-word screen and 0244's matcher. 4. K4, 20 shuffles, "
        "12 plants (grid alphabets on at least one side, a dictionary key word of 5-14 letters). 5. p per cell; plants "
        "found by their key word."
    ),
    "walkthrough": (
        "1. Write KRYPTOS; under it write the rest of the alphabet in rows of seven: ABCDEFG, HIJLMNQ, UVWXZ. "
        "2. Read down the columns from the left: KAHU RBIV YCJW PDLX TEMZ OFN SGQ. That is one grid alphabet. "
        "3. Read the columns in the alphabetical order of K, R, Y, P, T, O, S instead: KAHU OFN PDLX RBIV SGQ TEMZ YCJW. That is the other. "
        "4. Take one such alphabet for the plain side of the table and one for the cipher side. "
        "5. For a key length, say 7, two known places 7 apart must need the same key letter; check every such pair. "
        "6. Count the alphabet pairs that pass, for the carving and for scrambled copies."
    ),
    "expected_minutes": 90,
}

import multiprocessing as mp
import os
import random
import sys
import types
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
N = 97
STD = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
OFFICIAL = tuple(range(26, 35)) + tuple(range(64, 75))
LCOUNT = 24
N_COPIES = 20
N_PLANTS = 12
SEED = 16300 + 30
_G = {}


def A282():
    if "a" not in _G:
        import importlib.util
        path = next((ROOT / "experiments").glob("0282-*")) / "attack.py"
        spec = importlib.util.spec_from_file_location("frozen0282", path)
        a = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = a
        spec.loader.exec_module(a)
        a.ROOT = ROOT
        a.LCOUNT = LCOUNT
        _G["a"] = a
    return _G["a"]


def grid_alphabets(word):
    """The keyword without repeats, the rest of the alphabet in rows under it; read by columns left to right, and in
    the alphabetical order of the keyword's letters. -> (straight columns, keyword order)"""
    kw = "".join(dict.fromkeys(word))
    rest = "".join(c for c in STD if c not in kw)
    n = len(kw)
    cols = [kw[j] + rest[j::n] for j in range(n)]
    return "".join(cols), "".join(cols[j] for j in sorted(range(n), key=lambda j: kw[j]))


def extended_alphabets(m):
    """0244's straight keyword alphabets plus both grid alphabets of every word. Same return shape as m.alphabets()."""
    A0, names0, _ = m._alphabets_0244()
    alphas = dict(zip(A0, names0))
    words = [w.strip().upper() for w in (ROOT / "kryptos" / "data" / "words.txt").read_text().split()]
    for w in ["KRYPTOS"] + [w for w in words if len(w) >= 4 and w.isalpha()]:
        g1, g2 = grid_alphabets(w)
        alphas.setdefault(g1, w + "/grid")
        alphas.setdefault(g2, w + "/grid-keyed")
    A = list(alphas.keys())
    names = list(alphas.values())
    pos = np.zeros((len(A), 26), dtype=np.int16)
    for i, al in enumerate(A):
        for j, c in enumerate(al):
            pos[i, ord(c) - 65] = j
    return A, names, pos


def setup(vocabulary):
    a = A282(); f = a.F(); m = f.frozen()
    if not hasattr(m, "_alphabets_0244"):
        m._alphabets_0244 = m.alphabets
        m.alphabets = lambda: extended_alphabets(m)
    f.setup(vocabulary)
    return a, f, m


def job(args):
    tid, kname, text, known = args
    a = A282()
    _, _, res = a.job((tid, text, known, ()))
    return tid, kname, res


def run(ctx):
    me = sys.modules.get(__name__)
    if getattr(me, "job", None) is not job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    assert grid_alphabets("KRYPTOS") == ("KAHURBIVYCJWPDLXTEMZOFNSGQ", "KAHUOFNPDLXRBIVSGQTEMZYCJW")
    a, f, m = setup(ctx.vocabulary)
    A, names = m._G["A"], m._G["names"]
    n_straight = sum(1 for x in names if "/" not in x)
    # self-check: K1 under 0244's cipher with the extended list in place
    import json
    k1 = json.loads((ROOT / "data" / "k1.json").read_text())
    pt1 = k1["plaintext"]; ct1 = k1["ciphertext"][:len(pt1)]
    key1 = {"pa": m.KRY, "ca": m.KRY, "form": "added", "ka": "kry", "word": "PALIMPSEST", "start": 0, "shift": 0}
    assert m.encrypt(pt1 + "A" * (N - len(pt1)), key1)[:len(pt1)] == ct1, "K1 self-check failed"
    k24 = dict(ctx.KNOWN)
    k20 = {q: k24[q] for q in OFFICIAL}
    rng = random.Random(SEED)
    texts = [("k4", ctx.K4, None)]
    for i in range(N_COPIES):
        s = list(ctx.K4); rng.shuffle(s); texts.append((f"copy{i}", "".join(s), None))
    from kryptos.plants import english_plant
    grid_idx = [i for i, x in enumerate(names) if "/" in x]
    plants = {}
    for j in range(N_PLANTS):
        Lk = 5 + j % 10
        strs, src = m._G["rots"][Lk]
        w, r = src[rng.randrange(len(src))]
        pa = rng.choice(grid_idx)
        ca = rng.choice(grid_idx) if j % 2 else rng.randrange(2, len(A))
        if j % 4 == 2:
            pa, ca = ca, pa
        key = {"pa": A[pa], "ca": A[ca], "form": rng.choice(("added", "beaufort")), "ka": rng.choice(("std", "kry", "plain", "cipher")),
               "word": w, "start": r, "shift": rng.randrange(26)}
        pt = english_plant(SEED + 100 + j)
        ct = m.encrypt(pt, key)
        pid = f"plant{j}"
        plants[pid] = {"L": Lk, "key": key, "pt": pt, "names": [names[pa], names[ca]]}
        texts.append((pid, ct, pt))
    work = []
    for tid, t, pt in texts:
        for kname in ("k24", "k20"):
            kn = k24 if kname == "k24" else k20
            if pt is not None:
                kn = {q: pt[q - 1] for q in kn}
            work.append((tid, kname, t, kn))
    saved = getattr(ctx, "saved", {}) or {}
    res = {f"{w[0]}|{w[1]}": saved[f"{w[0]}|{w[1]}"] for w in work if f"{w[0]}|{w[1]}" in saved}
    todo = [w for w in work if f"{w[0]}|{w[1]}" not in res]
    W = int(os.environ.get("K4_WORKERS", 8))
    ctx.progress(len(res), len(work), "texts x known sets")
    with mp.get_context("fork").Pool(W) as pool:
        for tid, kname, out in pool.imap_unordered(job, todo, chunksize=1):
            res[f"{tid}|{kname}"] = out
            ctx.save(f"{tid}|{kname}", out)
            ctx.progress(len(res), len(work), "texts x known sets")
    cells = [f"{L}/{fm}" for L in range(1, LCOUNT + 1) for fm in ("added", "beaufort")]
    summary = {}
    for kname in ("k24", "k20"):
        fits = {}
        for c in cells:
            kv = res[f"k4|{kname}"]["fits"][c]
            cv = [res[f"copy{i}|{kname}"]["fits"][c] for i in range(N_COPIES)]
            if kv or max(cv):
                fits[c] = {"k4": kv, "copies_median": float(np.median(cv)), "copies_max": max(cv), "copies_with_any": sum(1 for x in cv if x),
                           "p": round((1 + sum(1 for x in cv if x >= kv)) / (N_COPIES + 1), 3) if kv else None,
                           "k4_screened": c not in res[f"k4|{kname}"]["unscreened"]}
        k4m = res[f"k4|{kname}"]["matches"]
        summary[kname] = {"fitting_pairs": fits, "k4_first_fit": min([int(c.split("/")[0]) for c, v in fits.items() if v["k4"]] or [None]),
                          "lowest_p": min([v["p"] for v in fits.values() if v["p"] is not None] or [None]),
                          "cells_k4_above_every_copy": [c for c, v in fits.items() if v["k4"] and v["k4"] > v["copies_max"]],
                          "key_word_matches": {"k4": len(k4m), "copies": [len(res[f"copy{i}|{kname}"]["matches"]) for i in range(N_COPIES)]},
                          "k4_matches": k4m[:20], "k4_unscreened_cells": res[f"k4|{kname}"]["unscreened"]}
    found = []
    for pid, p in plants.items():
        k = p["key"]
        ct = next(t for tid, t, _ in texts if tid == pid)
        for kname in ("k24", "k20"):
            hit = any(x["L"] == p["L"] and x["pa"] == k["pa"] and x["ca"] == k["ca"] and x["form"] == k["form"]
                      and sum(c1 == c2 for c1, c2 in zip(m.decrypt(ct, m.key_of(x)), p["pt"])) >= N - 2
                      for x in res[f"{pid}|{kname}"]["matches"])
            found.append({"plant": pid, "known": kname, "L": p["L"], "alphabets": p["names"], "found": bool(hit)})
    cands = []
    for x in summary["k24"]["k4_matches"][:20]:
        cands.append({"plaintext": m.decrypt(ctx.K4, m.key_of(x)), "key": m.key_of(x)})
    controls = [-9.0] * N_COPIES if not any(summary["k24"]["key_word_matches"]["copies"]) else []
    bounds = {"item": "F16.3", "alphabets": len(A), "straight": n_straight, "grid": len(A) - n_straight,
              "pairs": len(A) ** 2, "key_lengths": [1, LCOUNT], "forms": ["added", "beaufort"],
              "known_sets": {"k24": "all 24", "k20": "the 20 official (26-34, 64-74)"},
              "cap_pairs_listed": a.CAP, "key_word_check_lengths": [3, a.WMAX], "summary": summary,
              "plants": found, "plants_found": sum(x["found"] for x in found), "plants_total": len(found),
              "not_covered": "grids read bottom to top or right to left; a grid narrower or wider than the keyword; key lengths 25-26",
              "copies": N_COPIES, "exhaustive": "yes where pairs are listed; cells above the cap counted only",
              "aws_cost_estimate_dollars": 1.0}
    return {"candidates": cands, "controls": controls, "bounds": bounds,
            "notes": (f"{len(A):,} alphabets ({len(A) - n_straight:,} grid); key-word matches k24 K4 {summary['k24']['key_word_matches']['k4']}, "
                      f"k20 K4 {summary['k20']['key_word_matches']['k4']}, copies max {max(summary['k24']['key_word_matches']['copies'] + summary['k20']['key_word_matches']['copies'])}; "
                      f"lowest p k24 {summary['k24']['lowest_p']}, k20 {summary['k20']['lowest_p']}; plants {bounds['plants_found']}/{len(found)}")}


def encrypt(plaintext, key):
    return A282().F().frozen().encrypt(plaintext, key)


def worked_example(ctx, key):
    g1, g2 = grid_alphabets("KRYPTOS")
    return "\n".join(["KRYPTOS in a grid:", "  K R Y P T O S", "  A B C D E F G", "  H I J L M N Q", "  U V W X Z", "",
                      f"read by columns, left to right:  {g1}", f"read in keyword order (K O P R S T Y): {g2}", "",
                      "Each is tried as the plain side and the cipher side of the table, with every other keyword alphabet."])
