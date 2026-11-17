"""Experiment 0274. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f14.5b-the-question-mark-as-k4s-98th-letter-under-every-move-and-two-keyword-alphabets",
    "title": "F14.5b: the ? as K4's first cipher letter (98 letters, Scheidt's '98 characters left'), every move of 0129's library rebuilt for 98 letters, two dictionary keyword alphabets and a key word, three plaintext alignments; K4 against 20 shuffles",
    "family": "14-scheidt-mask-keyed-by-words",
    "parent": "0272-f14.2a-0271s-flawed-settings-decided-in-full",
    "changed": (
        "F14.5b: F14.2 (0271 with 0272's fix) on a 98-letter stream. 0247 ran F14.5 for F14.1, where only the alignment of the "
        "known places matters; under a move the whole geometry changes with the length, so 0129's route library is rebuilt for "
        "98 letters (K3's rule only where the step is prime to 98) and the carved '?' is the first letter of the enciphered "
        "stream, its value unknown: a known letter whose move lands there is dropped. Three alignments of the 98-letter "
        "plaintext (0-indexed): EASTNORTHEAST at 21 and BERLINCLOCK at 63 (the extra plaintext letter after 74), 21 and 64 (between "
        "the runs), 22 and 64 (before 22: letter for letter with the stream, as A2 reads with the ? counted). The general case, "
        "any carved letter lost under a move, is about 50 times larger and is F14.5c."
    ),
    "hypothesis_expert": (
        "C18(b) (03-scheidt-said.md: Scheidt, 2005, 'I think there are 98 characters left'): a 98-character working text "
        "including the '?' carved between K3 and K4. 0086 tested it as a 98-cell grid turned so the ? comes out first, with "
        "periodic or autokey keys; 0247 as one lost letter under F14.1 (no move). Here with F14's keyed mask and Sanborn's "
        "matrix step (C1(a), C4(a), C5, C27(c)): any type-1 move of 0129's families over 98 letters (K3 rule a + b i mod 98 for "
        "b prime to 98, one and two rotations, plain and reversed columnar, keyword columnar from the vocabulary; forward and "
        "inverse), before (A) or after (B) a Quagmire IV table on two of 0244's 208,064 dictionary keyword alphabets, key "
        "lengths 1-26, added or Beaufort, keyed by a word. Every alphabet pair tested exactly against the same-slot checks "
        "(repeated known letters as equal carved letters, the index on informative checks; 0272), key words matched as 0271. "
        "Prior attempts (reports/Kryptos K4 prior attempts database.md): the ? as a cipher letter has been tried with "
        "Vigenere and transposition guesses, never with keyword alphabets after a move."
    ),
    "hypothesis_eli5": (
        "Scheidt once said there were 98 characters left, but K4 has 97 letters. One reading: the question mark carved just "
        "before K4 is really its first letter, a letter we cannot read. This run repeats the big search of the last runs (shuffle "
        "the message through a grid, then a table with two word-scrambled alphabets and a key word) as if the message were 98 "
        "letters long with that unknown letter first, and compares K4 with 20 scrambled copies."
    ),
    "prediction": (
        "No key word on K4 in any alignment; K4's fitting-setting counts per (order, length, form, alignment) inside the 20 "
        "shuffles' range at about the chance rate; plants (98-letter English with the ? first, through these settings) "
        "found 11/12 or 12/12 (0271's key-word step keeps the first 20 word hits per numbering, so a short key with many colliding words can hide the true word: desk 11/12, the miss at length 8). Zero candidates (a 98-letter reading cannot pass the 97-letter gate; any key word on K4 is reported in "
        "bounds and stops the queue)."
    ),
    "method": (
        "1. Moves: 0129's route families rebuilt at 98 letters, forward and inverse, duplicates and non-permutations removed. "
        "2. Stream: '?' + the 97 carved letters; the ? is unknown. "
        "3. Setting: move, order (A move then table, B table then move), key length 1-26, alignment (3). Each known plaintext "
        "letter lands at a stream place; one landing on the ? is dropped; key slot = landing mod L (A) or plaintext place mod L (B). "
        "4. Same-slot checks: repeated known letters need equal carved letters; the rest pair up the 208,064 keyword alphabets "
        "through 0271's index (first six informative checks), verified on the rest. "
        "5. Settings with 5+ informative checks: fitted pairs listed and 0271's key-word step run (every dictionary and puzzle "
        "word of the length, every start, standard or KRYPTOS numbering or the pair's own, any shift); fewer: counted. "
        "6. Texts: K4 and 20 shuffles (seed 1450), each with the ? first. "
        "7. Plants: 12 English texts of 98 letters with the known words at a random alignment, enciphered on random settings "
        "(5+ informative checks) with two random dictionary alphabets and a dictionary key word; the first stream letter "
        "replaced by the ?; found if the search lists the true pair and a key word that decrypts to the plant."
    ),
    "walkthrough": (
        "1. Write the ? and the 97 carved letters in a row: 98 letters, the first unknown. "
        "2. Pick a grid move for 98 letters (for example: write in rows of 14, read the columns), the order, a key length and "
        "where the known words sit in the 98-letter message. "
        "3. Follow each known letter through the move to its place in the row; if it lands on the ?, skip it. "
        "4. Group the known letters by key slot; two equal known letters in one slot need equal carved letters. "
        "5. Two different known letters in one slot must be as far apart on the plain alphabet as their carved letters on "
        "the cipher alphabet: use these to find every pair of word-scrambled alphabets that fits. "
        "6. For each fitting pair, read off the key at the slots and look for a word that gives it. "
        "7. Repeat for 20 scrambled copies and compare."
    ),
    "expected_minutes": 230,
}

import os
import random
import sys
import time
import types
from pathlib import Path

import numpy as np

N = 98
ROOT = Path(__file__).resolve().parent
SEED = 1450
N_COPIES = 20
BLOCK = 25                    # routes per job
LCOUNT = 26
ALIGN = {0: (0, 0), 1: (0, 1), 2: (1, 1)}   # shift of EASTNORTHEAST's and BERLINCLOCK's plaintext places
PLANT_BANDS = ((6, 10), (11, 18), (19, 24))
PLANTS_PER_BAND = 4
_G = {}


def _load(tag, name, path=None):
    import importlib.util
    if name not in _G:
        path = path or next((ROOT / "experiments").glob(f"{tag}-*")) / "attack.py"
        spec = importlib.util.spec_from_file_location(name, path)
        m = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = m
        spec.loader.exec_module(m)
        if hasattr(m, "ROOT"):
            m.ROOT = ROOT
        _G[name] = m
    return _G[name]


def f72():
    return _load("0272", "frozen0272")


def f71():
    return f72().frozen()


def routes98(vocab):
    """0129's route families at 98 letters, forward and inverse; non-permutations (K3 rule with a step not prime to 98) dropped."""
    if "lib" not in _G:
        m = _load("0129", "lib98_0129")
        m.N = N
        seen, lib, bad = set(), [], 0
        for name, fn in m.route_fns(vocab):
            sigma = m.perm_of(fn)
            if len(sigma) != N or sorted(sigma) != list(range(N)):
                bad += 1
                continue
            fwd = [0] * N
            for j, i in enumerate(sigma):
                fwd[i] = j
            for tag, w in ((name, fwd), (name + " inverse", sigma)):
                t = tuple(w)
                if t not in seen:
                    seen.add(t); lib.append((tag, t))
        _G["lib"], _G["lib_bad"] = lib, bad
    return _G["lib"]


def known98(a):
    """Plaintext places (0-indexed, 98 letters) of the 24 known letters, in 0271's order (sorted carved place)."""
    s1, s2 = ALIGN[a]
    KP = f71()._G["KP"]
    return [q - 1 + (s1 if q <= 34 else s2) for q in KP]


def checks98(where, o, L, a):
    P = known98(a)
    land = np.array([where[p] for p in P])
    groups = {}
    for e, p in enumerate(P):
        if land[e] == 0:                     # lands on the ?: no carved letter
            continue
        s = (land[e] % L) if o == "A" else (p % L)
        groups.setdefault(s, []).append(e)
    pairs = [(g[0], u) for g in groups.values() for u in g[1:]]
    first = {s: g[0] for s, g in groups.items()}
    return pairs, land, first


def geometry(where, o, L):
    slot, mpos = [0] * N, [0] * N
    for p in range(N):
        t = where[p]
        mpos[t] = p
        slot[t] = t % L if o == "A" else p % L
    return slot, mpos


def encrypt(plaintext, key):
    """98 letters in, 98-letter stream out (its first letter is the one carved as ?)."""
    where = _G["lib"][key["route"]][1]
    slot, mpos = geometry(where, key["o"], key["L"])
    PA, CA, k = key["pa"], key["ca"], f71().kvals(key)
    out = []
    for t in range(N):
        p = PA.index(plaintext[mpos[t]])
        out.append(CA[(p + k[slot[t]]) % 26] if key["form"] == "V" else CA[(k[slot[t]] - p) % 26])
    return "".join(out)


def decrypt(stream, key):
    """98-letter stream (a ? first gives ? at its plaintext place) to plaintext."""
    where = _G["lib"][key["route"]][1]
    slot, mpos = geometry(where, key["o"], key["L"])
    PA, CA, k = key["pa"], key["ca"], f71().kvals(key)
    pt = [""] * N
    for t in range(N):
        if stream[t] == "?":
            pt[mpos[t]] = "?"
            continue
        c = CA.index(stream[t])
        pt[mpos[t]] = PA[(c - k[slot[t]]) % 26] if key["form"] == "V" else PA[(k[slot[t]] - c) % 26]
    return "".join(pt)


def _new_out():
    return {"fits": {}, "settings_listed": {}, "settings_with_fit": {}, "few_settings": {}, "few_fits": {},
            "matches": [], "capped": 0}


def search_many(texts, settings, word_cache):
    """Settings outside, texts inside (one index in memory at a time; 0272)."""
    m72, m = f72(), f71()
    lib = _G["lib"]
    tixs = [(tid, np.array([0 if c == "?" else ord(c) - 65 for c in text]), text) for tid, text in texts]
    outs = {tid: _new_out() for tid, _ in texts}
    for s in settings:
        r, o, L, a = s
        pairs, land, first = checks98(lib[r][1], o, L, a)
        eq, inf = m72.split_checks(pairs)
        idx = {f: m.plain_index(inf, f) if inf else None for f in "VB"}
        cover = sorted(first)
        for tid, tix, text in tixs:
            out = outs[tid]
            cl = tix[land]
            for form in "VB":
                n, lst, capped = m72.fixed_fits(cl, eq, inf, idx[form], form)
                c = f"{o}{L}{form}{a}"
                out["fits"][c] = out["fits"].get(c, 0) + n
                out["capped"] += capped
                if len(inf) >= m.MIN_LIST:
                    out["settings_listed"][c] = out["settings_listed"].get(c, 0) + 1
                    out["settings_with_fit"][c] = out["settings_with_fit"].get(c, 0) + (n > 0)
                    if lst is not None and n and L <= m.LMAX and len(cover) >= 3 and L in m._G["rots"]:
                        n0 = len(out["matches"])
                        m.key_words(lst[0], lst[1], cl, first, cover, L, form, word_cache, text, (r, o, L), out)
                        for x in out["matches"][n0:]:
                            x["a"] = a
                else:
                    out["few_settings"][c] = out["few_settings"].get(c, 0) + 1
                    out["few_fits"][c] = out["few_fits"].get(c, 0) + n
        del idx
        if len(word_cache) > 200:
            word_cache.clear()
    return outs


def settings_of(r0, r1):
    return [(r, o, L, a) for r in range(r0, r1) for o in "AB" for a in ALIGN for L in range(1, LCOUNT + 1)]


def _job(args):
    b, r0, r1, texts = args
    t0 = time.time()
    res = search_many(texts, settings_of(r0, r1), {})
    for o in res.values():
        o["n_matches"] = len(o["matches"])
        o["matches"] = o["matches"][:200]
    return b, {"res": res, "secs": round(time.time() - t0, 1)}


def make_plants(rng):
    from kryptos.plants import english_plant
    m72, m = f72(), f71()
    A, lib = m._G["A"], _G["lib"]
    plants = []
    for lo, hi in PLANT_BANDS:
        while sum(1 for p in plants if lo <= p["key"]["L"] <= hi) < PLANTS_PER_BAND:
            L = rng.randint(lo, hi)
            r, o, a = rng.randrange(len(lib)), rng.choice("AB"), rng.choice(list(ALIGN))
            pairs, land, first = checks98(lib[r][1], o, L, a)
            if len(m72.split_checks(pairs)[1]) < m.MIN_LIST or len(first) < 3 or L not in m._G["rots"]:
                continue
            strs, src = m._G["rots"][L]
            w = src[rng.randrange(len(src))]
            key = {"route": r, "o": o, "L": L, "a": a, "form": rng.choice("VB"), "pa": A[rng.randrange(2, len(A))],
                   "ca": A[rng.randrange(2, len(A))], "ka": rng.choice(("std", "kry")), "word": w[0], "start": w[1],
                   "shift": rng.randrange(26)}
            p97 = english_plant(rng.randrange(10 ** 9))
            extra = chr(65 + rng.randrange(26))
            ins = {0: 97, 1: 50, 2: 0}[a]          # where the 98th plaintext letter goes
            pt = p97[:ins] + extra + p97[ins:]
            P = known98(a)
            KL = m._G["KL"]
            assert all(pt[p] == chr(65 + KL[e]) for e, p in enumerate(P)), "plant alignment"
            stream = encrypt(pt, key)
            assert decrypt(stream, key) == pt
            plants.append({"key": key, "pt": pt, "stream": stream, "ct": "?" + stream[1:]})
    return plants


def run(ctx):
    import json
    import multiprocessing as mp
    t_start = time.time()
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    m = f71()
    m.setup(ctx.vocabulary)
    lib = routes98(ctx.vocabulary)
    ctx.progress(0, 1, "routes built")
    k4 = ctx.K4
    # self-checks: the 98-letter library holds the identity and every entry is a permutation; K1 through 0271's primitive
    assert any(w == tuple(range(N)) for _, w in lib), "identity missing"
    assert all(sorted(w) == list(range(N)) for _, w in lib[:2000])
    k1 = json.loads((ROOT / "data" / "k1.json").read_text())
    pt1 = k1["plaintext"]; ct1 = k1["ciphertext"][:len(pt1)]
    key1 = {"route": -1, "o": "A", "L": 10, "form": "V", "pa": m.KRY, "ca": m.KRY, "ka": "kry", "word": "PALIMPSEST", "start": 0, "shift": 0}
    assert m.encrypt(pt1 + "A" * (97 - len(pt1)), key1)[:len(pt1)] == ct1, "K1 self-check failed"
    ident = [i for i, (_, w) in enumerate(lib) if w == tuple(range(N))][0]
    rng = random.Random(SEED)
    texts = [("k4", "?" + k4)]
    for i in range(N_COPIES):
        s = list(k4); rng.shuffle(s); texts.append((f"copy{i}", "?" + "".join(s)))
    plants = make_plants(rng)
    pfound = []
    for p in plants:
        k = p["key"]
        out = search_many([("p", p["ct"])], [(k["route"], k["o"], k["L"], k["a"])], {})["p"]
        hit = any(x["pa"] == k["pa"] and x["ca"] == k["ca"] and x["form"] == k["form"] and x["a"] == k["a"]
                  and decrypt(p["stream"], x) == p["pt"] for x in out["matches"])
        pairs = checks98(lib[k["route"]][1], k["o"], k["L"], k["a"])[0]
        pfound.append({"L": k["L"], "o": k["o"], "a": k["a"], "route": lib[k["route"]][0], "checks": len(pairs),
                       "informative": len(f72().split_checks(pairs)[1]), "found": hit, "matches_at_setting": len(out["matches"])})
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
    flds = ("fits", "settings_listed", "settings_with_fit", "few_settings", "few_fits")
    tot = {tid: {**{f: {} for f in flds}, "matches": [], "n_matches": 0, "capped": 0} for tid, _ in texts}
    for v in res.values():
        for tid, acc in v["res"].items():
            for f in flds:
                for c, x in acc[f].items():
                    tot[tid][f][c] = tot[tid][f].get(c, 0) + x
            tot[tid]["n_matches"] += acc["n_matches"]
            tot[tid]["capped"] += acc["capped"]
            tot[tid]["matches"] += acc["matches"][:max(0, 400 - len(tot[tid]["matches"]))]

    def order(c):
        return (c[0], int(c[1:-2]), c[-2], c[-1])

    def rank(fld_k, fld_n):
        t = {}
        for c in sorted({c for x in tot.values() for c in x[fld_n]}, key=order):
            kv = tot["k4"][fld_k].get(c, 0)
            cv = [tot[f"copy{i}"][fld_k].get(c, 0) for i in range(N_COPIES)]
            t[c] = {"settings": tot["k4"][fld_n].get(c, 0), "k4": kv, "copies_median": float(np.median(cv)),
                    "copies_max": max(cv), "p_at_or_above": round((1 + sum(x >= kv for x in cv)) / (N_COPIES + 1), 3)}
        return t
    table = rank("settings_with_fit", "settings_listed")
    few = rank("few_fits", "few_settings")
    km = tot["k4"]["n_matches"]
    cm = [tot[f"copy{i}"]["n_matches"] for i in range(N_COPIES)]
    k4_readings = []
    for x in tot["k4"]["matches"][:50]:
        k4_readings.append({"key": x, "plaintext98": decrypt("?" + k4, x)})
    minp = min((v["p_at_or_above"] for v in table.values() if v["k4"] > 0), default=None)
    above_all = [c for c, v in {**table, **few}.items() if v["k4"] > v["copies_max"]]
    bounds = {
        "item": "F14.5b", "stream": "the ? then the 97 carved letters; the ? unknown",
        "alignments": {str(a): {"EASTNORTHEAST_from": 21 + s1, "BERLINCLOCK_from": 63 + s2} for a, (s1, s2) in ALIGN.items()},
        "routes": len(lib), "route_functions_dropped_not_permutations": _G["lib_bad"], "identity_route": ident,
        "orders": ["A move then table", "B table then move"], "key_lengths": [1, LCOUNT], "forms": ["added", "Beaufort"],
        "alphabets": m._G["NA"], "alphabet_pairs_per_setting_and_form": m._G["NA"] ** 2,
        "settings_per_text": len(lib) * 2 * LCOUNT * len(ALIGN), "listed_at_informative_checks": m.MIN_LIST,
        "settings_listed_k4": sum(tot["k4"]["settings_listed"].values()) // 2,
        "key_word_lengths": [1, m.LMAX], "key_numbering": "standard or KRYPTOS (and the pair's own alphabets when 20 or fewer pairs fit), any shift",
        "per_class": table, "few_informative_counted": few, "smallest_class_p": minp, "classes": len(table) + len(few),
        "cells_k4_above_every_copy": above_all,
        "capped_settings": {"k4": tot["k4"]["capped"], "copies_max": max(tot[f"copy{i}"]["capped"] for i in range(N_COPIES))},
        "key_word_matches": {"k4": km, "copies_median": float(np.median(cm)), "copies_max": max(cm),
                             "p_at_or_above": round((1 + sum(x >= km for x in cm)) / (N_COPIES + 1), 3)},
        "k4_key_word_readings": k4_readings,
        "plants": pfound, "plants_found": sum(p["found"] for p in pfound), "plants_total": len(pfound),
        "texts": len(texts), "exhaustive": True,
        "core_seconds": round(sum(v["secs"] for v in res.values())), "compute_seconds": round(time.time() - t_start),
        "resumed_units": len(jobs) - len(todo),
        "cost_estimate": "desk 2026-11-17: 18.3 s per route (156 settings x 21 texts) x 23,280 routes = 119 core-hours, about 3.7 h on 32 AWS cores, about $2.30; the general lost letter (F14.5c) about 50 times that",
    }
    notes = (f"F14.5b: the ? as the first of 98 cipher letters, {len(lib):,} moves at 98 letters x 2 orders x lengths 1-26 x 3 "
             f"alignments x 2 forms; key-word matches K4 {km}, copies median {np.median(cm)}, max {max(cm)}; smallest per-class p "
             f"{minp} over {len(table)} listed classes; cells with K4 above every copy: {len(above_all)} of {len(table) + len(few)}; "
             f"plants {bounds['plants_found']}/{len(pfound)}.")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def worked_example(ctx, key):
    return "\n".join([
        "F14.5b: the ? as K4's first letter, 98 letters.", "",
        "  stream     ? O B K R U O X O G H ... K C A R   (98 letters, the first unknown)",
        "  move       one of 0129's grid moves rebuilt for 98 letters, before or after the table",
        "  checks     known letters in one key slot; one that lands on the ? is skipped",
        "  alphabets  every pair of 208,064 word-scrambled alphabets tested exactly",
        "  key word   each fitting pair forces the key; a word of the key's length must give it"])
