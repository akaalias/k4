"""Experiment 0216. See program.md for the contract."""

EXPERIMENT = {
    "slug": "a13-the-saved-readings-against-their-own-search-on-fresh-copies-rerun",
    "title": "A13.3: the 31 saved 24-of-24 readings of eight experiments put through the 14-test structure battery, against the same experiments' frozen searches run unchanged on fresh scrambled copies, with masked plants through two of the climbs",
    "family": "1-keyed-periodic",
    "parent": "0140-k4-against-its-own-copies-with-the-tempering-climb",
    "changed": (
        "A13.3 (Stage 2, step 3, issue #75). The 31 readings that put all 24 known letters in place and were saved in "
        "raw.json (0034: 18, 0035: 3, 0048: 3, 0120: 2, 0137: 2, 0140, 0142, 0148: 1 each) were thrown away on their "
        "quadgram score. Here they go through tools/a13_structure.py's 14 tests, each against the same experiment's "
        "frozen attack.py run unchanged on fresh copies built as that experiment built them (tools/a13_check.py "
        "pass1-regen, seed 1300, begun 2026-10-21 and finished 2026-10-24 before this run). Pre-registered "
        "2026-10-21 in reports/a13-structure-check.md: 112 cells, flag at p < 0.05/112, candidates replicated "
        "sequentially on fresh copies (seed 3113). New in this run: masked planted messages through 0140's and 0142's "
        "climbs, to say what a 'nothing found' means for climbed readings. Rerun of 0215, which errored: the copy tool gave "
        "0148's climb all 24 known letters where 0148 drops the one at place 33, so its copies had no reading; the tool is "
        "fixed and 0148's 12 copies regenerated."
    ),
    "hypothesis_expert": (
        "A13 (knowledge/12-assumptions.md): if the English was masked before the keyed stage (C4(a), Scheidt 2005 and "
        "2015: 'I masked the English language', 'more than one stage'; C19, X and Q as stops), the right decryption "
        "is masked English and its quadgram score sits with the copies'. The readings tested are the climbed "
        "completions of F1's sampled cells: 0034 (periodic key 27-29 and 53-95 on standard/KRYPTOS tables, 24 "
        "conventions), 0035 and 0048 (27-29, keyword-mixed tables), 0120, 0137, 0140, 0142 (one free alphabet, "
        "Beaufort form, 23 and 26) and 0148 (K1/K2's added form, length 19, slip at 33). Statistic: for each "
        "experiment and test, the best value over a text's readings; K4's rank among the copies' (ties against K4). "
        "Copies: plain shuffles (0034, 0035, 0048; 10 each), shuffles passing 0119's exact decider at the length "
        "(0120, 0137, 0140, 0142; 12 each), shuffles of the 73 unknown places (0148; 12). A cell is a candidate when "
        "K4 is strictly above every copy (chance about 112/12 = 9); a flag needs p < 0.00045, all of 2,242 copies "
        "below K4. Power: A13.1 (power.json) against flat noise; against climbed copies it is unmeasured, so "
        "masked plants (reversal, X between words, X every kth letter, and unmasked) are enciphered under 0140's and "
        "0142's own method and climbed by their frozen search."
    ),
    "hypothesis_eli5": (
        "Some earlier searches produced readings with all 24 known letters right but the rest gibberish, and threw "
        "them away because they did not look like English. If Sanborn disguised the English before enciphering it "
        "(writing it backwards, or with X between words), the right reading would look like gibberish too. Here we "
        "test those saved readings for 14 kinds of hidden pattern, and run the very same searches on scrambled "
        "copies of the carving to see how much pattern luck alone produces. We also hide a few disguised messages "
        "of our own, run the same searches on them, and check whether the pattern tests would have noticed."
    ),
    "prediction": (
        "K4 is strictly above every copy in about 9 of 112 cells (chance), and none of those replicates: every "
        "candidate meets a fresh copy at or above K4 within a few dozen copies. No flag. The masked plants through "
        "the climbs are found less often than A13.1's flat-noise rate: the climb pulls a reversed or X-spaced "
        "message toward forward English junk, so most masked plants are not found by their own test. Zero "
        "candidates pass gate 4."
    ),
    "method": (
        "1. K4: every saved reading with 24 of 24 known letters in the eight experiments' raw.json, through the "
        "battery; per experiment and test, the best value. "
        "2. Copies: the readings in reports/a13-structure-data/pass1_copies.json (any job still missing is run here, "
        "same seeds), through the battery the same way. "
        "3. Rank K4 per cell; a cell where K4 is strictly above every copy is a candidate. "
        "4. Replication, per experiment with candidates: fresh copies built the experiment's way (seed '3113'), its "
        "frozen search, eight at a time, until every candidate test has met a copy at or above K4 (not a flag), or "
        "2,242 copies all below (a flag), or the clock (unresolved, reported with its p). "
        "5. Plants: three per mask (none, reversal, X between words, X every kth letter), Carter 1923 with the 24 "
        "known letters set after masking, enciphered with a random alphabet and key under 0142's (length 26) and "
        "0140's (length 23) Beaufort form, climbed by their frozen search; found when the mask's own test is above "
        "every one of that experiment's 12 copies."
    ),
    "walkthrough": (
        "1. Take one saved reading, say 0142's, with all 24 known letters in place. "
        "2. Score it on each of 14 pattern tests: read backwards, every nth letter, X as a word space, letter "
        "counts in any order, and so on. "
        "3. Scramble the carved letters twelve times, keeping only scrambles the same search can fit, and run the "
        "same search on each. "
        "4. Score each scramble's reading on the same 14 tests. "
        "5. On each test, see whether the carving's reading beats all twelve scrambles; with 112 such comparisons "
        "about nine will by luck, so each one that does is rerun against fresh scrambles until one catches up."
    ),
}

import json
import math
import random
import re
import sys
import time
import types
from multiprocessing import get_context
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

N = 97
EXPS = ("0034", "0035", "0048", "0120", "0137", "0140", "0142", "0148")
PASS1 = ROOT / "reports" / "a13-structure-data" / "pass1_copies.json"
CELLS = 14 * len(EXPS)
P_FLAG = 0.05 / CELLS
N_FLAG = 2242  # copies all below K4 needed for p = 1/2243 < 0.05/112
MASKS = ("none", "reversal", "X spaces", "X every kth")
TARGET = {"none": "eng_base", "reversal": "eng_reverse", "X spaces": "sep_words", "X every kth": "sep_regular"}
PLANT_EXPS = (("0142", 26), ("0140", 23))
N_PER_MASK = 3


def a13():
    import tools.a13_check as a
    return a


# ---- copies: the same builders as a13_check.p1_copies, for the replication ---------------------

def rep_copy(e, i):
    """Fresh copy i for experiment e, built as e built its own (seed '3113')."""
    a = a13()
    from kryptos.facts import K4, KNOWN
    rng = random.Random(f"3113/{e}/{i}")

    def shuffled():
        sh = list(K4); rng.shuffle(sh); return "".join(sh)

    def fitting(L):
        m = a.mod("0120")
        while True:
            sh = shuffled()
            if m.decide(m.equations(sh, KNOWN, L), "B", rng)[0] == "fit":
                return sh
    if e in ("0034", "0035", "0048"):
        text = shuffled()
    elif e in ("0120", "0137"):
        text = {23: fitting(23), 26: fitting(26)}
    elif e in ("0140", "0142"):
        text = fitting({"0140": 23, "0142": 26}[e])
    else:
        free = [j for j in range(N) if (j + 1) not in KNOWN]
        cp = list(K4); letters = [K4[j] for j in free]; rng.shuffle(letters)
        for j, ch in zip(free, letters):
            cp[j] = ch
        text = "".join(cp)
    return (e, i, text, rng.randrange(10 ** 9))


def best_stats(readings):
    a = a13()
    bs = [a.battery(r) for r in readings if r and a.fits24(r)]
    if not bs:
        return None
    return {t: max(b[t] for b in bs) for t in a.TESTS}


# ---- plants ------------------------------------------------------------------------------------

def _carter():
    src = (ROOT / "knowledge/sources/carter-1923-tomb-of-tutankhamen-vol1.txt").read_text(errors="ignore").upper()
    words = re.sub("[^A-Z ]", "", re.sub(r"\s+", " ", src)).split()
    return words, "".join(words)


def masked_plant(mask, rng):
    from kryptos.facts import KNOWN
    words, letters = _carter()
    s0 = rng.randrange(20000, len(letters) - 200)
    plain = letters[s0:s0 + N]
    if mask == "none":
        t = plain
    elif mask == "reversal":
        t = plain[::-1]
    elif mask == "X spaces":
        w0 = rng.randrange(5000, len(words) - 100)
        t = "X".join(words[w0:w0 + 40])[:N]
    else:
        k = rng.randrange(5, 12); src = list(plain)
        t = "".join("X" if i % k == k - 1 else src.pop(0) for i in range(N))
    t = list(t)
    for q, ch in KNOWN.items():
        t[q - 1] = ch
    return "".join(t)


def plant_job(args):
    e, L, mask, idx, ct, truth, seed = args
    from kryptos.facts import KNOWN
    m = a13().mod(e)
    sc, pt, alpha, k, done = m.climb_text(ct, KNOWN, L, seed, 1000, time.time() + 10 ** 6)
    return e, L, mask, idx, pt, sum(1 for x, y in zip(pt, truth) if x == y), done


def _any(args):
    if args[0] == "plant":
        return plant_job(args[1])
    return a13().p1_job(args[1])


def run(ctx):
    a = a13()
    from kryptos.scorer import english_score, free_text
    t_start = time.time()
    if getattr(sys.modules.get(__name__), "_any", None) is not _any:  # make the pool's pickles resolve
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm

    # 1. K4's saved readings, with keys, re-encrypted by their own frozen code
    k4 = {}
    for e in EXPS:
        d = next((ROOT / "experiments").glob(f"{e}-*"))
        raw = json.loads((d / "raw.json").read_text())
        rows = [c for c in raw.get("candidates", []) if a.fits24(c["plaintext"])]
        enc_ok = all(a.mod(e).encrypt(c["plaintext"], c["key"]) == ctx.K4 for c in rows)
        k4[e] = {"rows": rows, "stats": best_stats([c["plaintext"] for c in rows]), "reencrypt_ok": enc_ok}

    # 2. copies: pass1_copies.json, missing jobs run here with the same seeds
    done = json.loads(PASS1.read_text()) if PASS1.exists() else {}
    jobs = [j for j in a.p1_copies() if f"{j[0]}/{j[1]}" not in done]
    missing_at_start = len(jobs)
    if jobs:
        a.mod("0120")
        with get_context("fork").Pool(8) as pool:
            for e, idx, rows, secs in pool.imap_unordered(_any, [("p1", j) for j in jobs]):
                done[f"{e}/{idx}"] = {"rows": rows, "seconds": round(secs, 1)}
                PASS1.write_text(json.dumps(done, indent=0))
    copies = {e: [] for e in EXPS}
    secs = {e: 0.0 for e in EXPS}
    for key, v in done.items():
        e = key.split("/")[0]
        if e in copies:
            s = best_stats([r for _, r in v["rows"]])
            if s:
                copies[e].append({"stats": s, "eng": max(english_score(free_text(r)) for _, r in v["rows"] if r and a.fits24(r))})
            secs[e] += v["seconds"]

    # 3. cells
    cells, cand = {}, []
    for e in EXPS:
        ks, cs = k4[e]["stats"], copies[e]
        if not cs:
            raise RuntimeError(f"{e}: no copy readings")
        for t in a.TESTS:
            vals = [c["stats"][t] for c in cs]
            kv = ks[t]
            at_or_above = sum(1 for v in vals if v >= kv) if kv > -math.inf else len(vals)
            cells[f"{e}/{t}"] = {"k4": kv, "copies_min": min(vals), "copies_max": max(vals), "n": len(vals),
                                 "rank": 1 + at_or_above, "candidate": at_or_above == 0}
            if at_or_above == 0:
                cand.append((e, t))
    expected = sum(1 / (len(copies[e]) + 1) for e in EXPS) * 14

    # 5. sequential replication (after the plants, step 4), per experiment, eight copies at a time
    rep = {}
    by_e = {}
    for e, t in cand:
        by_e.setdefault(e, []).append(t)
    per_copy = {e: secs[e] / max(1, len(copies[e])) for e in EXPS}
    order = sorted(by_e, key=lambda e: per_copy[e])  # cheapest first
    margin = 900  # leave time for the record
    with get_context("fork").Pool(8) as pool:
        # 4. masked plants first through 0142's and 0140's own climbs
        prng = random.Random(2150)
        pjobs, truths = [], {}
        for e, L in PLANT_EXPS:
            m0120 = a.mod("0120")
            for mask in MASKS:
                for i in range(N_PER_MASK):
                    pt = masked_plant(mask, prng)
                    alpha = list(ctx.STANDARD_ALPHABET); prng.shuffle(alpha); alpha = "".join(alpha)
                    key = [prng.randrange(26) for _ in range(L)]
                    ct = m0120.beaufort_encrypt(pt, alpha, key)
                    truths[(e, mask, i)] = pt
                    pjobs.append(("plant", (e, L, mask, i, ct, pt, prng.randrange(10 ** 9))))
        plants = []
        if ctx.time_left() > 600:
            for e, L, mask, i, pt, right, nd in pool.map(_any, pjobs, chunksize=1):
                t = TARGET[mask]
                st = best_stats([pt])
                truth_st = a.battery(truths[(e, mask, i)])
                cmax = max(c["stats"][t] for c in copies[e])
                plants.append({"exp": e, "L": L, "mask": mask, "i": i, "test": t, "reading_value": st[t] if st else None,
                               "plaintext_value": truth_st[t], "copies_max": cmax, "letters_right": right,
                               "found": bool(st and st[t] > cmax), "plaintext_would_be_found": truth_st[t] > cmax,
                               "reading": pt})

        for e in order:
            open_t = {t: {"k4": k4[e]["stats"][t], "copies": 0, "first_at_or_above": None, "max": -math.inf} for t in by_e[e]}
            i = 0
            while any(v["first_at_or_above"] is None for v in open_t.values()) and i < N_FLAG:
                if ctx.time_left() < margin + 1.5 * per_copy[e]:
                    break
                batch = [rep_copy(e, i + j) for j in range(8)]
                res = sorted(pool.map(_any, [("p1", b) for b in batch], chunksize=1), key=lambda r: r[1])
                for _, idx, rows, s_ in res:
                    st = best_stats([r for _, r in rows])
                    for t, v in open_t.items():
                        if v["first_at_or_above"] is not None or st is None:
                            continue
                        v["copies"] += 1
                        v["max"] = max(v["max"], st[t])
                        if st[t] >= v["k4"]:
                            v["first_at_or_above"] = idx + 1
                i += 8
            for t, v in open_t.items():
                n_ = v["copies"]
                if v["first_at_or_above"] is not None:
                    verdict, p = "not a flag", None
                elif n_ >= N_FLAG:
                    verdict, p = "FLAG", 1 / (n_ + 1)
                else:
                    verdict, p = "unresolved", 1 / (n_ + 1)
                rep[f"{e}/{t}"] = {"k4": v["k4"], "fresh_copies": n_, "first_copy_at_or_above": v["first_at_or_above"],
                                   "fresh_max": v["max"], "verdict": verdict, "p_bound_if_unresolved": p}

    flags = [c for c, v in rep.items() if v["verdict"] == "FLAG"]
    unresolved = [c for c, v in rep.items() if v["verdict"] == "unresolved"]
    found = {f"{e} {m}": f"{sum(p['found'] for p in plants if p['exp'] == e and p['mask'] == m)} of "
             f"{sum(1 for p in plants if p['exp'] == e and p['mask'] == m)}" for e, _ in PLANT_EXPS for m in MASKS}

    cands = []
    for e in EXPS:
        for c in k4[e]["rows"][:3]:
            cands.append({"plaintext": c["plaintext"], "key": {"exp": e, "key": c["key"]}, "key_bits": c.get("key_bits", 0.0),
                          "key_description": f"saved reading of {e}: " + c.get("key_description", "")[:120],
                          "notes": f"A13.3: {e}'s saved 24-of-24 reading, through the battery"})
    controls = [c["eng"] for e in EXPS for c in copies[e]]
    bounds = {
        "item": "A13.3", "pre_registered": "2026-10-21, reports/a13-structure-check.md",
        "tests": a.TESTS, "experiments": list(EXPS), "cells": CELLS, "p_flag": P_FLAG,
        "k4_readings": {e: len(k4[e]["rows"]) for e in EXPS},
        "k4_reencrypt_ok": {e: k4[e]["reencrypt_ok"] for e in EXPS},
        "copies": {e: len(copies[e]) for e in EXPS},
        "copy_cpu_seconds_mean": {e: round(per_copy[e], 1) for e in EXPS},
        "copies_regenerated": "tools/a13_check.py pass1-regen, seed 1300: 22 jobs on 2026-10-21, the other 68 on 2026-10-24 before this run",
        "jobs_missing_at_start": missing_at_start,
        "cells_table": cells, "candidates": [f"{e}/{t}" for e, t in cand], "candidates_expected_by_chance": round(expected, 2),
        "replication": rep, "flags": flags, "unresolved": unresolved,
        "plants": plants, "plants_found": found,
        "plant_design": f"{N_PER_MASK} per mask, Carter 1923 with the known letters set after masking, random alphabet and key, Beaufort form; climbed by the frozen climb_text (10 tempering runs); found = the mask's own test strictly above all 12 copies of that experiment",
        "seconds": round(time.time() - t_start, 1),
    }
    notes = (f"{len(cand)} candidate cells of {CELLS} (chance {expected:.1f}); replication: "
             f"{sum(1 for v in rep.values() if v['verdict'] == 'not a flag')} not a flag, {len(unresolved)} unresolved, {len(flags)} flags. "
             f"Plants found by their own test: {found}.")
    return {"candidates": cands, "controls": controls, "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    """Each saved reading re-enciphered by its own experiment's frozen encrypt."""
    return a13().mod(key["exp"]).encrypt(plaintext, key["key"])


def worked_example(ctx, key):
    a = a13()
    e = key["exp"] if key else "0142"
    d = next((ROOT / "experiments").glob(f"{e}-*"))
    raw = json.loads((d / "raw.json").read_text())
    r = next(c["plaintext"] for c in raw["candidates"] if a.fits24(c["plaintext"]))
    b = a.battery(r)
    lines = [f"{e}'s saved reading: {r}", f"backwards:          {r[::-1]}", "battery (higher = more structure):"]
    lines += [f"  {t:15s} {b[t]:.3f}" if b[t] > -math.inf else f"  {t:15s} none" for t in a.TESTS]
    return "\n".join(lines)
