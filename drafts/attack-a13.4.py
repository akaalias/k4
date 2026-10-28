"""Experiment 0218. See program.md for the contract."""

EXPERIMENT = {
    "slug": "a13-the-slipped-readings-through-the-structure-battery",
    "title": "A13.4: every 24-of-24 reading of 0207, 0212, 0213 and 0214 (A1's slipped searches) regenerated with their frozen searches for K4 and the same 20 scrambled copies, through the 14-test structure battery, with masked plants through 0207's search",
    "family": "1-keyed-periodic",
    "parent": "0217-a13-the-backwards-reading-of-0034-against-more-fresh-copies",
    "changed": (
        "A13.4 (Stage 2, step 3, issue #75). Since 2026-10-18 four experiments kept K4 readings with all 24 known letters "
        "in place: 0207 (periodic key on the sculpture's tables, up to 3 slips), 0212 (ciphertext autokey and progressive "
        "key, 2 slips or a lost step), 0213 (plaintext autokey, 2 broken links or a lost step) and 0214 (a move then the "
        "table, 2 slips). None kept its copies' readings. Here each frozen attack.py's own per-text search is called on K4 "
        "and on the same 20 seeded copies it used (tools/a13_check.py's pass 4), every reading it returns goes through "
        "the battery, and K4 is ranked per experiment and test. Pre-registered 2026-10-21 in "
        "reports/a13-structure-check.md: 56 cells, flag at p < 0.05/56, candidates replicated sequentially (seeds 4113 on). "
        "New in this run: masked planted messages with slips through 0207's search."
    ),
    "hypothesis_expert": (
        "A13 with A1 (knowledge/12-assumptions.md): a masked plaintext (C4(a), Scheidt's 'I masked the English language'; "
        "C19, X and Q stops) enciphered with a slip or two (C17(b), Sanborn's 'sloppy'). The readings are those A1's exact "
        "searches let through: 0207 (8 table classes, key lengths 1-26, k <= 3), 0212 (ciphertext autokey on 487,734 table "
        "setups, k <= 2 or a lost step; progressive key, k <= 2), 0213 (plaintext autokey lags 1-52, 2 breaks or a lost "
        "step), 0214 (1,847,590 landings of 0110-0114 and the type-1 library, both orders, k <= 2). Statistic: per "
        "experiment and test, the best value over a text's readings ('?' read as unknown, the 24 known letters set as the "
        "candidates set them); K4's rank among its 20 copies, ties against K4. 0199, 0201-0206 and 0208-0211 kept no K4 "
        "reading (nothing fits K4, or a free alphabet leaves it undetermined): noted, not rerun."
    ),
    "hypothesis_eli5": (
        "The searches that allowed for one or two enciphering mistakes produced readings with every known letter right "
        "but gibberish elsewhere. If the message was disguised before it was enciphered, the right one would look like "
        "gibberish too. We rerun those searches exactly, on the carving and on the same scrambled copies they used, and "
        "test every reading for 14 kinds of hidden pattern; the carving counts only if it beats all the copies. We also "
        "hide disguised messages with mistakes of our own and check the tests notice them."
    ),
    "prediction": (
        "K4 strictly above every copy in about 56/21 = 2.7 cells, none replicating; no flag. Every saved K4 candidate of "
        "the four experiments is among the regenerated readings. The masked plants through 0207 are found by their "
        "mask's own test in most cases, because 0207's readings at lengths 13 and 20 are fixed by the known letters and "
        "the planted reading itself is among them. Zero candidates pass gate 4."
    ),
    "method": (
        "1. For 0207, 0212, 0213, 0214: rebuild the frozen search's state as its run() does, call its per-text search on "
        "K4 and its 20 copies (its own shuffled, its own seeds), keep every reading. "
        "2. Check every saved K4 candidate is among K4's regenerated readings. "
        "3. Battery on every reading; per text and test the best value; rank K4. "
        "4. A cell where K4 is strictly above every copy is a candidate: fresh copies (the experiment's shuffled, seeds "
        "4113 on) eight at a time until one is at or above K4 (not a flag), 1,123 all below (a flag), or the clock. "
        "5. Plants: three per mask (none, reversal, X between words, X every kth letter), Carter 1923 masked then the "
        "known letters set, enciphered by 0207's own plant routine with 2 slips at lengths 13 and 20; found when the "
        "mask's own test on the plant's readings is strictly above every one of K4's 20 copies."
    ),
    "walkthrough": (
        "1. Rerun one of the slip searches, say 0207, on the carving: every key length 1-26 and table, up to three "
        "known letters allowed wrong. "
        "2. Keep every reading it lets through. "
        "3. Score each reading on 14 pattern tests and keep the best value per test. "
        "4. Do the same on the 20 scrambled copies 0207 used. "
        "5. On each test, see whether the carving beats all 20 copies; about three of the 56 comparisons will by luck, "
        "so each that does is rerun against fresh copies until one catches up."
    ),
}

import json
import math
import random
import sys
import time
import types
from multiprocessing import get_context
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

N = 97
EXPS = ("0207", "0212", "0213", "0214")
OUT = ROOT / "reports" / "a13-structure-data" / "pass4.json"
CELLS = 14 * len(EXPS)
P_FLAG = 0.05 / CELLS
N_FLAG = 1123
REP_SEED = 4113
MASKS = ("none", "reversal", "X spaces", "X every kth")
TARGET = {"none": "eng_base", "reversal": "eng_reverse", "X spaces": "sep_words", "X every kth": "sep_regular"}
PLANT_SET = ((13, ("kry", "kry", "vig")), (20, ("std", "kry", "beau")))
N_PER_MASK = 3
_STATE = {}


def a13():
    import tools.a13_check as a
    return a


def readings_job(args):
    """(experiment, tag, text) -> best battery values over every reading the frozen search returns."""
    e, tag, text = args
    a = a13()
    t0 = time.time()
    rd = a.p4_readings(e, text)
    best = {t: -math.inf for t in a.TESTS}
    for s in rd:
        for t, v in a.battery(s).items():
            best[t] = max(best[t], v)
    return e, tag, len(rd), best, round(time.time() - t0, 1), (rd if tag == "k4" else None)


def _masked(mask, rng):
    import importlib.util
    spec = importlib.util.spec_from_file_location("a0216", next((ROOT / "experiments").glob("0216-*")) / "attack.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.masked_plant(mask, rng)


def run(ctx):
    a = a13()
    t_start = time.time()
    if getattr(sys.modules.get(__name__), "readings_job", None) is not readings_job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    res, saved_ok, secs = {}, {}, {}
    k4_readings = {}
    for e in EXPS:
        a.p4_setup(e)  # before the fork: every worker inherits the state
        m = a._p4_mod(e)
        texts = [("k4", ctx.K4)] + [(f"copy{i}", m.shuffled(ctx.K4, a.P4[e] + i)) for i in range(a.P4_COPIES)]
        with get_context("fork").Pool(8) as pool:
            out = pool.map(readings_job, [(e, tag, t) for tag, t in texts], chunksize=1)
        res[e] = {tag: {"n": n, "best": best} for _, tag, n, best, s, _r in out}
        secs[e] = sum(s for *_x, s, _r in out) / len(out)
        k4_readings[e] = next(r for _, tag, *_x, r in out if tag == "k4")
        raw = json.loads((next((ROOT / "experiments").glob(f"{e}-*")) / "raw.json").read_text())
        rs = set(k4_readings[e])
        saved = [c["plaintext"] for c in raw.get("candidates", []) if a.fits24(c["plaintext"])]
        saved_ok[e] = f"{sum(1 for s in saved if s.replace('?', '.') in rs)} of {len(saved)}"
    OUT.write_text(json.dumps(res, indent=0, default=float))

    cells, cand = {}, []
    for e in EXPS:
        kv_all = res[e]["k4"]["best"]
        cs = [v["best"] for tag, v in res[e].items() if tag != "k4"]
        for t in a.TESTS:
            vals = [c[t] for c in cs]
            kv = kv_all[t]
            above = sum(1 for v in vals if v >= kv) if kv > -math.inf else len(vals)
            cells[f"{e}/{t}"] = {"k4": kv, "copies_min": min(vals), "copies_max": max(vals), "rank": 1 + above, "candidate": above == 0}
            if above == 0:
                cand.append((e, t))

    # plants through 0207's own routine, masked
    m7 = a._p4_mod("0207")
    prng = random.Random(2160)
    copies_best_0207 = [v["best"] for tag, v in res["0207"].items() if tag != "k4"]
    plants = []
    for L, cls in PLANT_SET:
        for mask in MASKS:
            for i in range(N_PER_MASK):
                pt = _masked(mask, prng)
                key = "".join(prng.choice(m7.STD) for _ in range(L))
                ct = list(m7.encrypt(pt, {"pa": cls[0], "ca": cls[1], "m": cls[2], "key": key}))
                slots = m7.forced("".join(ct), ctx.KNOWN, L, cls)
                checked = [s for s, eq in slots.items() if len(eq) >= 2]
                prng.shuffle(checked)
                places = [prng.choice([q for q, _ in slots[s]]) for s in checked[:2]]
                for q in places:
                    ct[q - 1] = prng.choice([c for c in m7.STD if c != ct[q - 1]])
                ct = "".join(ct)
                _, _, n, best, _, _ = readings_job(("0207", "plant", ct))
                rd = set(a.p4_readings("0207", ct))
                t = TARGET[mask]
                cmax = max(c[t] for c in copies_best_0207)
                plants.append({"L": L, "cls": list(cls), "mask": mask, "i": i, "slips": sorted(places), "test": t,
                               "value": best[t], "copies_max": cmax, "found": best[t] > cmax,
                               "planted_reading_among_readings": pt in rd, "n_readings": n})

    # sequential replication
    rep = {}
    by_e = {}
    for e, t in cand:
        by_e.setdefault(e, []).append(t)
    for e in sorted(by_e, key=lambda e: secs[e]):
        a.p4_setup(e)
        m = a._p4_mod(e)
        open_t = {t: {"k4": res[e]["k4"]["best"][t], "copies": 0, "first": None, "max": -math.inf} for t in by_e[e]}
        i = 0
        with get_context("fork").Pool(8) as pool:
            while any(v["first"] is None for v in open_t.values()) and i < N_FLAG:
                if ctx.time_left() < 600 + 2 * secs[e]:
                    break
                batch = [(e, f"rep{i + j}", m.shuffled(ctx.K4, REP_SEED + i + j)) for j in range(8)]
                for _, tag, n, best, s, _r in sorted(pool.map(readings_job, batch, chunksize=1), key=lambda r: int(r[1][3:])):
                    for t, v in open_t.items():
                        if v["first"] is not None:
                            continue
                        v["copies"] += 1
                        v["max"] = max(v["max"], best[t])
                        if best[t] >= v["k4"]:
                            v["first"] = int(tag[3:]) + 1
                i += 8
        for t, v in open_t.items():
            verdict = "not a flag" if v["first"] is not None else ("FLAG" if v["copies"] >= N_FLAG else "unresolved")
            rep[f"{e}/{t}"] = {"k4": v["k4"], "fresh_copies": v["copies"], "first_copy_at_or_above": v["first"],
                               "fresh_max": v["max"], "verdict": verdict,
                               "p_bound": None if v["first"] is not None else 1 / (v["copies"] + 1)}

    flags = [c for c, v in rep.items() if v["verdict"] == "FLAG"]
    unresolved = [c for c, v in rep.items() if v["verdict"] == "unresolved"]
    found = {f"L{L} {mk}": f"{sum(p['found'] for p in plants if p['L'] == L and p['mask'] == mk)} of {N_PER_MASK}" for L, _ in PLANT_SET for mk in MASKS}
    cands = []
    for e in EXPS:
        raw = json.loads((next((ROOT / "experiments").glob(f"{e}-*")) / "raw.json").read_text())
        for c in [c for c in raw.get("candidates", []) if a.fits24(c["plaintext"])][:3]:
            cands.append({"plaintext": c["plaintext"], "key": {"exp": e, "key": c["key"]}, "key_bits": c.get("key_bits", 0.0),
                          "key_description": f"saved reading of {e}: " + c.get("key_description", "")[:120],
                          "notes": f"A13.4: {e}'s saved 24-of-24 reading, through the battery"})
    from kryptos.scorer import english_score, free_text
    controls = []
    for e in ("0207",):
        raw = json.loads((next((ROOT / "experiments").glob(f"{e}-*")) / "result.json").read_text())
        controls = [float(x) for x in raw.get("controls", [])]
    bounds = {
        "item": "A13.4", "pre_registered": "2026-10-21, reports/a13-structure-check.md",
        "tests": a.TESTS, "experiments": list(EXPS), "cells": CELLS, "p_flag": P_FLAG,
        "kept_no_k4_reading": "0199, 0201-0206, 0208-0211 (no setting fits K4, or a free alphabet leaves the reading undetermined); 0200 errored",
        "readings_per_text": {e: {"k4": res[e]["k4"]["n"], "copies_min": min(v["n"] for t, v in res[e].items() if t != "k4"),
                                  "copies_max": max(v["n"] for t, v in res[e].items() if t != "k4")} for e in EXPS},
        "saved_k4_candidates_regenerated": saved_ok, "text_seconds_mean": {e: round(secs[e], 1) for e in EXPS},
        "cells_table": cells, "candidates": [f"{e}/{t}" for e, t in cand],
        "candidates_expected_by_chance": round(CELLS / (a.P4_COPIES + 1), 2),
        "replication": rep, "flags": flags, "unresolved": unresolved,
        "plants": plants, "plants_found": found,
        "plant_design": f"{N_PER_MASK} per mask at each of {[p[0] for p in PLANT_SET]}, 0207's plant routine (2 slips at checked slots), masked Carter with the known letters set; found = the mask's test strictly above all 20 of K4's copies",
        "controls": "0207's own controls (its copies' best quadgram scores)",
        "seconds": round(time.time() - t_start, 1),
    }
    notes = (f"{len(cand)} candidate cells of {CELLS} (chance {CELLS / 21:.1f}); replication: "
             f"{sum(1 for v in rep.values() if v['verdict'] == 'not a flag')} not a flag, {len(unresolved)} unresolved, {len(flags)} flags. "
             f"Saved K4 candidates regenerated: {saved_ok}. Plants found: {found}.")
    return {"candidates": cands, "controls": controls, "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return a13()._p4_mod(key["exp"]).encrypt(plaintext, key["key"])


def worked_example(ctx, key):
    a = a13()
    e = key["exp"] if key else "0207"
    raw = json.loads((next((ROOT / "experiments").glob(f"{e}-*")) / "raw.json").read_text())
    c = next(c for c in raw["candidates"] if a.fits24(c["plaintext"]))
    r = c["plaintext"].replace("?", ".")
    b = a.battery(r)
    lines = [f"{e}'s saved reading ({c.get('key_description', '')[:90]}):", f"  {r}", "battery (higher = more structure):"]
    lines += [f"  {t:15s} {b[t]:.3f}" if b[t] > -math.inf else f"  {t:15s} none" for t in a.TESTS]
    return "\n".join(lines)
