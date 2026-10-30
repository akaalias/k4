"""Experiment (F6.1 lengths 6-10, draft). See program.md for the contract."""

EXPERIMENT = {
    "slug": "f6.1-free-alphabet-around-every-move-lengths-6-10-with-stand-ins",
    "title": "F6.1: one free alphabet after or before every type-1 move, key lengths 6-10, every setting K4 fits decided by D1's one-run decider, with 10 shuffled stand-ins through the same procedure",
    "family": "6-move-then-table",
    "parent": "0253-f1.4-one-alphabet-residue-decided-by-the-one-run-decider",
    "changed": (
        "F6.1 at lengths 6-10, reopened by D2 (0252: 7,443 settings, one-run power 31 of 48 on plants drawn from K4's own "
        "fitting settings). 0253's decide() unchanged (one tempering run of 0252's climb on K4, then shuffles the exact "
        "decider fits at the same setting climbed one at a time, stop at the first at or above, at most 12; no escalation, "
        "so K4 and the stand-ins are decided alike), now on 0129's move library: every (move, order, length 6-10, form) "
        "that fits K4. Ten full shuffles of K4 stand in for it (0254/0255: a count over settings needs texts put through "
        "the whole procedure), each on 300 of its own fitting settings."
    ),
    "hypothesis_expert": (
        "F6.1 (C1(a): 'a matrix code... then went back to this table'; C27(c): a 'slightly different' tableau): one free "
        "alphabet on both sides (Quagmire III with an unknown order), a periodic key of length 6-10, after or before one "
        "move of 0129's type-1 library (27,852 routes: columnar, keyword columnar, K3's rule, turns, rail fence, grid "
        "paths...), Beaufort or added form. 0129/0130 found no fit below 6 and fits from 6 at the copies' rate, so the "
        "known letters cannot decide these settings and English must. Decider: D1's one run of 0140's tempering "
        "generalised to any slot map and reading order (0252), copies fitted exactly at the same setting (0253). Clue "
        "entries C1(a), C27(c), C11."
    ),
    "hypothesis_eli5": (
        "Sanborn said he wrote the message into a grid, read it out another way, and then used the cipher table. With his "
        "own scrambled alphabet in the table and a short key word, thousands of such recipes agree with the 24 known "
        "letters. For each one we search for the most English-looking reading of K4 and do the same on scrambled copies; "
        "ten scrambled stand-ins for K4 go through the very same test, so we know what 'K4 wins often' would mean."
    ),
    "prediction": (
        "K4's rate of settings above all 12 copies inside the 10 stand-ins' spread (p above 0.1); plants (24, on settings "
        "K4 fits) found about 14 of 24; no reading English. Zero candidates."
    ),
    "method": (
        "1. Settings: 0129's route library (27,852 moves) x order (A move then table, B table then move) x key length 6-10 "
        "x form (added, Beaufort); each decided exactly on K4 by 0252's fits(); the fitting ones are K4's cell. "
        "2. Per setting (one job, own seed): 0253's decide() without escalation: one tempering run on K4, then shuffles "
        "that fit the same setting climbed one at a time until one reaches K4, at most 12. "
        "3. Stand-ins: 10 shuffles of K4 (seed 2680), each with its own fitting settings found the same way, 300 drawn "
        "and decided alike. "
        "4. Plants: 12 clean and 12 Sanborn-style messages on settings K4 fits, random alphabet and key; found if above all 12. "
        "5. Verdict: K4's share of settings above all 12 copies, ranked among the stand-ins' shares."
    ),
    "walkthrough": (
        "1. Pick a recipe: write the message in rows of 9 and read the columns in the order of a key word (the move), then "
        "encipher on the table with an unknown scrambled alphabet and a 7-letter key. "
        "2. Undo the move on paper for the 24 known letters: each lands on a carved place and a key slot. "
        "3. Check that some alphabet makes every pair of known letters in one slot agree. "
        "4. Search alphabets and keys for the most English-looking reading of K4 under the recipe. "
        "5. Shuffle K4 until the shuffle also passes step 3, search it the same way; stop when a shuffle reads as well as "
        "K4, at most 12 shuffles. "
        "6. Do steps 4-5 for every recipe K4 fits, and for ten scrambled stand-ins of K4; compare how often each wins all 12."
    ),
    "expected_minutes": 5000,
}

import importlib.util
import os
import random
import sys
import time
import types
from pathlib import Path

N = 97
ROOT = Path(__file__).resolve().parent
LENGTHS = (6, 7, 8, 9, 10)
BASE = 12
PLANTS = 24
N_STANDIN, SAMPLE = 10, 300
SEED = 2680
_MODS = {}


def A():
    """0253's attack, frozen: decide() and the 0252 module behind it."""
    if "a" not in _MODS:
        path = next((ROOT / "experiments").glob("0253-*")) / "attack.py"
        spec = importlib.util.spec_from_file_location("frozen0253", path)
        a = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = a
        spec.loader.exec_module(a)
        a.ROOT = ROOT
        _MODS["a"] = a
    return _MODS["a"]


def _fit_job(args):
    lo, hi, text = args
    m = A().M()
    lib = _MODS["lib"]
    rng = random.Random(lo)
    out = []
    for r in range(lo, hi):
        for o in "AB":
            for L in LENGTHS:
                for form in "VB":
                    if m.fits(text, m.move_setting(lib[r][1], o, L, form), rng):
                        out.append((r, o, L, form))
    return out


def _job(args):
    key, text, st, seed = args
    return key, A().decide(text, st, seed, False)


def cell_for(text, pool, W):
    lib = _MODS["lib"]
    step = max(1, len(lib) // (W * 16))
    jobs = [(lo, min(len(lib), lo + step), text) for lo in range(0, len(lib), step)]
    return sorted(x for lst in pool.imap_unordered(_fit_job, jobs) for x in lst)


def run(ctx):
    import multiprocessing as mp
    t0 = time.time()
    W = int(os.environ.get("K4_WORKERS", 8))
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    a = A(); m = a.M()
    m._load("0140"); m._load("0128"); m._load("0129"); m.glib()
    check = m.self_check(ctx)
    _MODS["lib"] = m._load("0129").route_library(ctx.vocabulary)
    lib = _MODS["lib"]
    m20, m26 = m._load("0140").load_0120(), m._load("0226")
    k4 = ctx.K4
    rng = random.Random(SEED)
    targets = [("k4", k4)] + [(f"standin{i}", "".join(rng.sample(k4, N))) for i in range(N_STANDIN)]

    # 1. each target's fitting settings (exact); saved per target so a resume skips the scan
    saved = getattr(ctx, "saved", {}) or {}
    cells = {}
    with mp.get_context("fork").Pool(W) as pool:
        for tid, t in targets:
            if f"cell:{tid}" in saved:
                cells[tid] = [tuple(x) for x in saved[f"cell:{tid}"]]
            else:
                cells[tid] = cell_for(t, pool, W)
                ctx.save(f"cell:{tid}", [list(x) for x in cells[tid]])
            ctx.progress(len(cells), len(targets), "cells scanned")

    def st_of(s):
        r, o, L, form = s
        return m.move_setting(lib[r][1], o, L, form)

    def name_of(s):
        r, o, L, form = s
        return f"{lib[r][0]} order {o} L={L} {form}"

    # 2. plants on settings K4 fits
    prng = random.Random(SEED + 1)
    texts = [("clean", pt) for _, pt in m20.make_plants(ctx.KNOWN, 10, prng, PLANTS // 2)]
    for arm in (0, 1, 2):
        texts += m26.class_texts(prng, arm)[:PLANTS // 6]
    plants, pmeta = [], {}
    for idx, (cls, pt) in enumerate(texts):
        s = cells["k4"][prng.randrange(len(cells["k4"]))]
        st = st_of(s)
        order = list(range(26)); prng.shuffle(order)
        key = [prng.randrange(26) for _ in range(st[2])]
        pc = m.encipher(pt, st, order, key)
        assert m.decipher(pc, st, order, key) == pt and m.fits(pc, st, prng), (idx, name_of(s))
        pmeta[idx] = {"cls": cls, "setting": name_of(s), "pt": pt}
        plants.append((f"plant:{idx}", pc, st, 900000 + idx))

    # 3. every K4 setting, 300 per stand-in, the plants
    work = list(plants)
    work += [(f"k4:{i}", k4, st_of(s), 1000 + i) for i, s in enumerate(cells["k4"])]
    for ti, (tid, t) in enumerate(targets[1:], start=1):
        r = random.Random(SEED * 10 + ti)
        for i in sorted(r.sample(range(len(cells[tid])), min(SAMPLE, len(cells[tid])))):
            work.append((f"{tid}:{i}", t, st_of(cells[tid][i]), 300000 + ti * 100000 + i))
    random.Random(SEED + 2).shuffle(work)        # interleave so no group is starved
    res = {w[0]: saved[w[0]] for w in work if w[0] in saved}        # units an earlier run of this attack.py finished (#105)
    todo = [w for w in work if w[0] not in res]
    ctx.progress(len(res), len(work), "settings")
    with mp.get_context("fork").Pool(W) as pool:
        for key, out in pool.imap_unordered(_job, todo, chunksize=1):
            res[key] = out
            ctx.save(key, out)
            ctx.progress(len(res), len(work), "settings")

    # 4. verdicts
    found = {}
    for idx, v in pmeta.items():
        r = res[f"plant:{idx}"]
        v.update(found=r["above"] >= BASE, above=r["above"], score=r["score"],
                 letters_right=sum(x == y for x, y in zip(r["reading"], v.pop("pt"))))
        found.setdefault("clean" if v["cls"] == "clean" else "sanborn", []).append(v["found"])

    def rate(tid):
        ks = [k for k in res if k.startswith(tid + ":")]
        hit = sum(1 for k in ks if res[k]["above"] >= BASE)
        first = sum(1 for k in ks if res[k]["above"] >= 1)
        return {"cell_size": len(cells[tid]), "decided": len(ks), "above_all_12": hit, "rate": round(hit / len(ks), 4),
                "beat_first_rate": round(first / len(ks), 4), "lost_copies": sum(1 for k in ks if res[k]["lost"])}
    per = {tid: rate(tid) for tid, _ in targets}
    sr = [per[t]["rate"] for t in per if t != "k4"]
    kr = per["k4"]["rate"]
    ge = sum(1 for x in sr if x >= kr)
    p = (1 + ge) / (len(sr) + 1)
    n = len(cells["k4"])
    top = sorted(range(n), key=lambda i: (-res[f"k4:{i}"]["above"], -res[f"k4:{i}"]["score"]))[:20]
    top_list = [{"setting": name_of(cells["k4"][i]), "above": res[f"k4:{i}"]["above"], "score": res[f"k4:{i}"]["score"],
                 "reading": res[f"k4:{i}"]["reading"],
                 "known_in_place": sum(res[f"k4:{i}"]["reading"][q - 1] == c for q, c in ctx.KNOWN.items())} for i in top]
    by = {}
    for (r_, o, L, form) in cells["k4"]:
        by[f"{o}{form}{L}"] = by.get(f"{o}{form}{L}", 0) + 1
    bounds = {
        "item": "F6.1 lengths 6-10 (reopened by D2, 0252)",
        "decider": "0253's decide() unchanged, without escalation: one run of 0252's generalised tempering (16 x 625 x 1000) on the target, then shuffles the exact decider fits at the same setting, climbed one at a time, stop at the first at or above, at most 12",
        "self_check_against_0140": check,
        "library": len(lib), "lengths": list(LENGTHS), "orders": ["A move then table", "B table then move"], "forms": ["added", "Beaufort"],
        "settings_listed": len(lib) * 2 * len(LENGTHS) * 2, "k4_fitting_settings": n, "k4_fitting_by_order_form_length": by,
        "targets": per, "k4_rate": kr, "standins_rates": sr, "standins_at_or_above_k4": ge, "p": round(p, 4),
        "fair_rate_if_independent": round(1 / (BASE + 1), 4),
        "top_settings": top_list,
        "plants": {"clean_found": [sum(found.get("clean", [])), len(found.get("clean", []))],
                   "sanborn_found": [sum(found.get("sanborn", [])), len(found.get("sanborn", []))], "each": pmeta},
        "core_seconds": round(sum(v["secs"] for v in res.values())), "compute_seconds": round(time.time() - t0),
        "exhaustive": True, "exhaustive_over": "every type-1 move of 0129's library, both orders, key lengths 6-10, both forms, that K4 fits on one free alphabet; each decided at D1's one-run power",
        "resumed_units": len(work) - len(todo),
        "cost_estimate": "about 7,443 K4 settings (0252) and 3,000 stand-in settings x about 4.1 one-run climbs (H_12 copies) at 17-25 core-s, plus 11 exact scans of the library (about 18 core-minutes each) and 24 plants: about 230-300 core-hours; about $11 on Modal, above the credit left, so on the laptop: several days",
    }
    notes = (f"F6.1 lengths 6-10: {n} settings fit K4; K4 above all 12 copies in {per['k4']['above_all_12']} ({100 * kr:.1f}%); "
             f"10 stand-ins {100 * min(sr):.1f}-{100 * max(sr):.1f}%, {ge} at or above K4 (p {p:.2f}); plants clean "
             f"{bounds['plants']['clean_found']}, Sanborn-style {bounds['plants']['sanborn_found']}.")
    controls = [c for k, v in res.items() if k.startswith("k4:") for c in v["copies"]][:2000]
    return {"candidates": [], "bounds": bounds, "notes": notes, "controls": controls}


def encrypt(plaintext, key):
    """No candidate is submitted."""
    return A().encrypt(plaintext, key)


def worked_example(ctx, key):
    return "\n".join([
        "F6.1: one free alphabet around a move, key lengths 6-10, decided setting by setting.", "",
        "  setting      columns of a 9-wide grid read in key-word order, then the table, key length 7, Beaufort",
        "  slot map     each carved letter's key slot and message place follow from the move",
        "  K4 gets one tempering search under that setting; shuffles of K4 that fit the same 24 checks get the same,",
        "  one at a time, until a shuffle reads as well as K4 (at most 12).",
        "  Ten shuffled stand-ins for K4 go through the whole procedure: K4's rate of wins must stand out from theirs."])
