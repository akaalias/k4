"""Experiment: F16.4b-r. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f16.4b-r-0290s-two-edge-cells-on-10000-fresh-shuffles",
    "title": "F16.4b-r: 0290's two edge cells (a key restarted at each carved line with an offset per line, added form, key lengths 21 and 23: K4 4 and 2 fitting pairs of keyword alphabets, 50 shuffles at most 2 and 1) on 10,000 fresh shuffles; K4's pairs listed with the letters they fix",
    "family": "16-simple-hand-methods",
    "parent": "0290-f16.4b-line-keyed-schemes-on-dictionary-keyword-alphabets",
    "changed": (
        "F16.4b-r (issue #123). 0290 left K4 above all 50 shuffles in two distinct cells of 312. By the text-level "
        "null that is ordinary (14 of 50 shuffles do as well against the others), but a result that beats its copies "
        "gets a replication. Same exact count as 0290 (its frozen structure() and alphabets()), only these two "
        "cells, on 10,000 fresh shuffles (new seeds). Lines set before the run: a cell replicates if at most 1 of "
        "10,000 shuffles has K4's count or more (p below 0.05/312 = 0.00016). Also: K4's pairs with their key words' "
        "alphabets and the letters each fixes (descriptive). Strength aimed at: sampled, 10,000 shuffles."
    ),
    "hypothesis_expert": (
        "C27(b). Model as 0290's BOTH: k = key[column in the carved line mod L] + offset[line], lines at K4 places "
        "1-4, 5-35, 36-66, 67-97; Quagmire IV on two dictionary keyword alphabets (208,064 each side), added form "
        "k = C(c) - P(p); 8 independent checks at L = 21 and at 23, so a random pair fits with chance 26^-8 and a "
        "text expects 0.2 fitting pairs; counts are clumped because neighbouring words give near-equal alphabets. "
        "0290: no forced key is a word in these cells."
    ),
    "hypothesis_eli5": (
        "In the last run K4 had a few more fitting alphabet pairs than any of 50 scrambled copies in two corners of "
        "a table of 312. With that many corners, some will stand out by luck. Here we count the same two corners on "
        "10,000 new scrambled copies to see how rare K4's counts really are."
    ),
    "prediction": (
        "Not replicated: at L 21 between 20 and 300 of 10,000 shuffles have 4 or more pairs; at L 23 between 100 and "
        "1,500 have 2 or more. K4's pairs come from neighbouring words (one clump) and their fixed letters are not English."
    ),
    "method": (
        "1. 0290's checks for the two cells; the plain-side numbers of every alphabet once (the known letters do not "
        "move). 2. Per text the cipher-side numbers, counted by value; the fit count is the number of matching pairs. "
        "3. K4, 10,000 shuffles (200 jobs of 50, own seeds), 4 plants. 4. K4's pairs: words, forced key, and the "
        "plaintext at every place whose key slot and line offset the known letters fix."
    ),
    "walkthrough": (
        "1. Write K4 in its carved lines and a key of 21 letters under each line, starting again at each line's first letter. "
        "2. Allow each line its own extra shift. "
        "3. For a pair of keyword alphabets, work out the key letter each known place forces. "
        "4. The pair fits if known places under the same key letter agree once the line shifts are taken off. "
        "5. Count the fitting pairs for K4 and for each scrambled copy."
    ),
    "expected_minutes": 12,
}

import importlib.util
import multiprocessing as mp
import os
import random
import sys
import types
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
CELLS = (("both", 21), ("both", 23))
N_JOBS, PER_JOB = 200, 50
SEED = 16491
LINE = 0.05 / 312
_G = {}


def frozen():
    path = ROOT / "experiments" / "0290-f16.4b-line-keyed-schemes-on-dictionary-keyword-alphabets" / "attack.py"
    spec = importlib.util.spec_from_file_location("frozen0290", path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    mod.ROOT = ROOT
    return mod


def pack(vecs):
    """rows of numbers 0-25 -> one integer each (base 26)"""
    out = np.zeros(vecs.shape[0], dtype=np.uint64)
    for j in range(vecs.shape[1]):
        out = out * np.uint64(26) + vecs[:, j].astype(np.uint64)
    return out


def setup(known):
    mod = _G["mod"]
    places = sorted(known)
    col = {q: e for e, q in enumerate(places)}
    pv = _G["pos"][:, [ord(known[q]) - 65 for q in places]]
    cells = {}
    for model, L in CELLS:
        checks, anchored = mod.structure(L, model, places)
        cells[(model, L)] = {"checks": checks, "anchored": anchored, "pkey": pack(mod.combo(pv, checks, col))}
    return places, col, cells


def count(text, cfg, want_pairs=False):
    mod = _G["mod"]
    places, col, cells = cfg
    cv = _G["pos"][:, [ord(text[q - 1]) - 65 for q in places]]
    out = {}
    for (model, L), c in cells.items():
        ckey = pack(mod.combo(cv, c["checks"], col))
        vals, cnt = np.unique(ckey, return_counts=True)
        idx = np.searchsorted(vals, c["pkey"])
        idx[idx >= len(vals)] = 0
        hit = vals[idx] == c["pkey"]
        n = int(cnt[idx][hit].sum())
        if want_pairs:
            pairs = []
            for p_a in np.nonzero(hit)[0]:
                for c_a in np.nonzero(ckey == c["pkey"][p_a])[0]:
                    pairs.append((int(p_a), int(c_a)))
            out[(model, L)] = (n, pairs)
        else:
            out[(model, L)] = n
    return out


def _job(j):
    rng = random.Random(SEED * 1000 + j)
    sh = list(_G["K4"])
    res = []
    for _ in range(PER_JOB):
        rng.shuffle(sh)
        r = count("".join(sh), _G["cfg"])
        res.append([r[c] for c in CELLS])
    return j, res


def partial(text, known, model, L, p_a, c_a, cell):
    """the forced key per anchored slot, each line's offset where fixed, and the letters they decide"""
    mod = _G["mod"]
    A, pos = _G["A"], _G["pos"]
    PA, CA = A[p_a], A[c_a]
    kq = {q: (int(pos[c_a, ord(text[q - 1]) - 65]) - int(pos[p_a, ord(known[q]) - 65])) % 26 for q in known}
    key = {s: sum(cf * kq[q] for q, cf in e.items()) % 26 for s, e in cell["anchored"].items()}
    off = {}
    for q in sorted(known):
        s = mod.slot_of(q, L, model)
        if s in key:
            o = (kq[q] - key[s]) % 26
            assert off.setdefault(mod.line_of(q), o) == o
    out = []
    for q in range(1, 98):
        s, l = mod.slot_of(q, L, model), mod.line_of(q)
        if s in key and l in off:
            out.append(PA[(CA.index(text[q - 1]) - key[s] - off[l]) % 26])
        else:
            out.append("?")
    return "".join(out), "".join(chr(65 + key[s]) if s in key else "?" for s in range(L)), off


def run(ctx):
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    mod = frozen()
    A, names, pos = mod.alphabets()
    known = dict(ctx.KNOWN)
    _G.update(mod=mod, A=A, pos=pos, K4=ctx.K4)
    cfg = setup(known)
    _G["cfg"] = cfg
    k4 = count(ctx.K4, cfg, want_pairs=True)
    k4n = {c: k4[c][0] for c in CELLS}
    assert [k4n[c] for c in CELLS] == [4, 2], k4n          # 0290's counts
    k4pairs = {}
    for (model, L) in CELLS:
        rows = []
        for p_a, c_a in k4[(model, L)][1]:
            reading, key, off = partial(ctx.K4, known, model, L, p_a, c_a, cfg[2][(model, L)])
            assert all(reading[q - 1] == known[q] for q in known)
            det = "".join(ch for i, ch in enumerate(reading, start=1) if ch != "?" and i not in known)
            rows.append({"plain_word": names[p_a], "cipher_word": names[c_a], "key_from_line_2": key, "line_offsets": {str(k): v for k, v in off.items()},
                         "reading": reading, "letters_fixed": sum(1 for ch in reading if ch != "?"),
                         "english_of_fixed_unknown_letters": round(ctx.english_score(det), 3) if len(det) >= 4 else None})
        k4pairs[f"{model}/{L}"] = rows
    # plants: each fits its own cell, and the planted pair is among the fitting pairs
    from kryptos.plants import english_plant
    plants = []
    for j, (model, L) in enumerate(CELLS * 2):
        prng = random.Random(SEED + 300 + j)
        pt = english_plant(SEED + 300 + j)
        ia, ib = prng.randrange(2, len(A)), prng.randrange(2, len(A))
        key = {"pa": A[ia], "ca": A[ib], "form": "added", "ka": "std", "word": "".join(chr(65 + prng.randrange(26)) for _ in range(L)),
               "shift": 0, "model": model, "offsets": {str(l): prng.randrange(26) for l in (1, 2, 3, 4)}}
        ct = mod.encrypt(pt, key)
        pk = {q: pt[q - 1] for q in known}
        pcfg = setup(pk)
        r = count(ct, pcfg, want_pairs=True)[(model, L)]
        ok = (ia, ib) in r[1]
        read = partial(ct, pk, model, L, ia, ib, pcfg[2][(model, L)])[0] if ok else ""
        right = sum(1 for a, b in zip(read, pt) if a == b)
        plants.append({"cell": f"{model}/{L}", "fits": r[0], "planted_pair_listed": ok, "letters_fixed": sum(1 for ch in read if ch != "?"), "letters_right": right})
    saved = getattr(ctx, "saved", {}) or {}
    res = {int(k): v for k, v in saved.items()}
    todo = [j for j in range(N_JOBS) if j not in res]
    ctx.progress(len(res), N_JOBS, "jobs of 50 shuffles")
    with mp.get_context("fork").Pool(int(os.environ.get("K4_WORKERS", 8))) as pool:
        for j, out in pool.imap_unordered(_job, todo, chunksize=1):
            res[j] = out
            ctx.save(str(j), out)
            ctx.progress(len(res), N_JOBS, "jobs of 50 shuffles")
    n = N_JOBS * PER_JOB
    summ = {}
    for i, c in enumerate(CELLS):
        v = np.array([row[i] for j in range(N_JOBS) for row in res[j]])
        ge = int((v >= k4n[c]).sum())
        hist = {str(x): int((v == x).sum()) for x in sorted(set(v.tolist()))[:12]}
        summ[f"{c[0]}/{c[1]}"] = {"k4": k4n[c], "shuffles_at_or_above": ge, "p": round((1 + ge) / (n + 1), 5), "replicated": bool((1 + ge) / (n + 1) < LINE),
                                 "shuffles_with_any": int((v > 0).sum()), "shuffle_max": int(v.max()), "histogram_low": hist}
    n_ok = sum(1 for p in plants if p["planted_pair_listed"])
    return {
        "candidates": [],
        "bounds": {
            "item": "F16.4b-r", "cells": [f"{m}/{L}/added" for m, L in CELLS], "alphabets": len(A), "shuffles": n, "line": round(LINE, 5),
            "summary": summ, "k4_pairs": k4pairs, "plants": plants, "plants_found": f"{n_ok} of {len(plants)}",
            "controls": f"{n} fresh shuffles of K4 with the known letters kept in place, the same count", "exhaustive": True,
            "aws_cost_estimate_dollars": 0.15,
        },
        "notes": "; ".join(f"{k}: K4 {v['k4']}, {v['shuffles_at_or_above']} of {n} shuffles at or above, p {v['p']}, replicated {v['replicated']}" for k, v in summ.items())
                 + f"; plants {n_ok}/{len(plants)}",
    }


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    mod = frozen()
    lines = ["key length 21, restarted at each carved line, an offset per line: slot and line of each known place", "", "place line column slot known carved"]
    for q in sorted(ctx.KNOWN):
        lines.append(f"{q:>5} {mod.line_of(q):>4} {q - mod.LINE_START[mod.line_of(q)]:>6} {mod.slot_of(q, 21, 'both'):>4} {ctx.KNOWN[q]:>5} {ctx.K4[q - 1]:>6}")
    return "\n".join(lines)
