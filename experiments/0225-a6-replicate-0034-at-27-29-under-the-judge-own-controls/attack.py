"""Experiment 0225. See program.md for the contract."""

EXPERIMENT = {
    "slug": "a6-replicate-0034-at-27-29-under-the-judge-own-controls",
    "title": "A6.1, replication: 0034's completed periodic keys at lengths 27-29, where K4's best judged reading (8) led all 10 copies (best 7), against fresh copies of the same frozen search until one reaches 8 or 80 stay below",
    "family": "1-keyed-periodic",
    "parent": "0224-a6-replicate-0034-at-27-29-under-the-judge",
    "changed": (
        "Rerun of 0224 with gate 4 given the 0034 search's own copies (0216's 10, pass1_copies.json, 30 readings at 27-29) "
        "as well as the fresh ones: 0224 gave it only its 8 fresh copies, and K4's period-29 reading (-6.709), below 0216's "
        "copies (best -6.627) and failed in 0222, was kept against them (issue #88's error again). Same seeds; the "
        "replication is unchanged. "
        "A6.1 (Stage 2, step 4, issue #84), the candidate 0222 left (0223 is a mistaken duplicate of 0222: the new code "
        "was not written before the run). 0222 judged K4's saved readings of 0034, 0035 and 0048 against 0216's "
        "regenerated copies: in the cell 0034 at 27-29 K4's best (8 of 100) was above every one of 10 copies (4-7), the "
        "only one of 4 cells where it led (chance 0.36). Pre-registered rule (program.md): a candidate is replicated on "
        "that cell alone against fresh copies, enough for the corrected p (0.05 / 4: 80 copies all below K4), before "
        "anything else. Fresh plain shuffles (seed 4222), 0034's frozen sweep unchanged at periods 27, 28, 29 (the cell's "
        "three readings per text: 24 conventions, 20 restarts each), eight at a time, judged after each batch."
    ),
    "hypothesis_expert": (
        "A6 (knowledge/12-assumptions.md). Cipher: one periodic key on the standard or KRYPTOS tables, 24 conventions, key "
        "lengths 27-29 (C1(c), C27(c): the K1/K2 tableau system at the only lengths 1-52 the known letters leave alive for "
        "it; 0005), the 3-5 free key slots completed by a quadgram climb (0034). Statistic: the judge's best score (j3, "
        "Sonnet 5.5) over a text's three readings. K4: 8 ('? LEVES SIT MILAN BAC ? AT ? OF ?'). With 3-5 free slots each "
        "reading is fixed but for 9-15 letters, so a score of 8 means a few short words, inside what the bench calls "
        "chance (20 = a few short words). Sequential: a fresh copy at or above 8 ends it (not a flag); 80 copies all below "
        "K4 is a flag (p < 0.0125 corrected for the 4 cells of 0222)."
    ),
    "hypothesis_eli5": (
        "One old search, rerun on scrambled copies of the carving, gave readings the judge scored a little below the "
        "carving's reading (7 against 8 out of 100, both near the bottom of the scale). That is probably luck. The honest "
        "check is to scramble again and again, run the same search, and see how soon a scrambled copy does as well."
    ),
    "prediction": (
        "A fresh copy scores 8 or more within the first two batches (16 copies): the 10 copies of 0222 already reached 7 "
        "twice, and the judge's scores at this end of the scale move in steps of 2-4. Not a flag. Zero candidates pass gate 4."
    ),
    "method": (
        "1. Fresh copies: plain shuffles of K4 from random.Random(4222), a search seed each, as tools/a13_check.py's pass "
        "1 drew them. "
        "2. Each through 0034's frozen sweep at periods 27, 28, 29 (24 conventions, 20 restarts), best reading per period. "
        "3. Eight copies at a time on eight cores; the batch's 24 readings judged in one call; each copy's best. "
        "4. Stop at the first copy at or above 8 (not a flag), at 80 copies all below (a flag), or at the clock (unresolved, "
        "with p at most 1/(copies + 11))."
    ),
    "walkthrough": (
        "1. Scramble the 97 carved letters. "
        "2. For key lengths 27, 28 and 29, fix the key letters the known words force, and choose the 3-5 free ones so the "
        "rest reads as much like English as possible. "
        "3. Hide the known words and give the three readings to the judge. "
        "4. If the best scores 8 or more, the carving's lead was luck: stop. "
        "5. Otherwise scramble again; 80 scrambles in a row below 8 would be a signal."
    ),
}

import importlib.util
import json
import random
import time
from pathlib import Path

N = 97
ROOT = Path(__file__).resolve().parent
K4_VALUE = 8
N_FLAG = 80
BATCH = 8
PERIODS = [27, 28, 29]
_MODS = {}


def _load(e):
    if e not in _MODS:
        import sys
        path = next((ROOT / "experiments").glob(f"{e}-*")) / "attack.py"
        spec = importlib.util.spec_from_file_location(f"frozen{e}", path)
        m = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = m
        spec.loader.exec_module(m)
        _MODS[e] = m
    return _MODS[e]


def _job(args):
    idx, text, seed = args
    from kryptos.alphabets import conventions
    from kryptos.facts import KNOWN
    from kryptos.scorer import english_score
    m = _MODS["0034"]
    res = m.sweep(text, KNOWN, list(conventions()), english_score, random.Random(seed), m.RESTARTS, lambda: 10 ** 9, PERIODS)
    best = {}
    for sc, P, conv, pt, key, nfree in res:
        if P not in best or sc > best[P][0]:
            best[P] = (sc, pt)
    return idx, [(P, best[P][1], best[P][0]) for P in sorted(best)]


def _s(v):
    return -1 if v is None else v


def run(ctx):
    import multiprocessing as mp
    import sys
    import types
    from kryptos.scorer import english_score, free_text
    _load("0034")
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    rng = random.Random(4222)
    copies, first, controls, calls = [], None, [], 0
    t0 = time.time()
    with mp.get_context("fork").Pool(BATCH) as pool:
        while first is None and len(copies) < N_FLAG and ctx.time_left() > 600:
            jobs = []
            for _ in range(BATCH):
                sh = list(ctx.K4); rng.shuffle(sh)
                jobs.append((len(copies) + len(jobs), "".join(sh), rng.randrange(10 ** 9)))
            res = pool.map(_job, jobs, chunksize=1)
            texts = [pt for _, rows in res for _, pt, _ in rows]
            v = ctx.judge(texts)
            calls += len(texts)
            k = 0
            for idx, rows in res:
                sc = [v[k + j]["score"] for j in range(len(rows))]
                k += len(rows)
                best = max(_s(x) for x in sc)
                copies.append({"copy": idx, "best": best, "by_period": {str(P): s for (P, _, _), s in zip(rows, sc)},
                               "none": sum(1 for x in sc if x is None),
                               "best_reading": rows[max(range(len(rows)), key=lambda j: _s(sc[j]))][1]})
                controls += [english_score(free_text(pt)) for _, pt, _ in rows]
                if first is None and best >= K4_VALUE:
                    first = idx
    verdict = "not a flag" if first is not None else ("FLAG" if len(copies) >= N_FLAG else "unresolved")
    # gate 4: the 0034 search's copies from 0216 (pass1_copies.json) as well as the fresh ones (issue #88: never fewer than 0222 used)
    p1 = json.loads((ROOT / "reports/a13-structure-data/pass1_copies.json").read_text())
    controls += [english_score(free_text(t)) for k_, v_ in p1.items() if k_.startswith("0034/")
                 for lab, t in v_["rows"] if int(lab.split()[1]) in PERIODS]
    # K4's own readings, re-submitted against these copies (each faces its own search's copies, issue #88)
    raw = json.loads((next((ROOT / "experiments").glob("0034-*")) / "raw.json").read_text())
    cands = []
    for c in raw["candidates"]:
        if int(c["key_description"].split()[1]) in PERIODS:
            cands.append({"plaintext": c["plaintext"], "key": {"exp": "0034", "key": c["key"]},
                          "key_description": "saved reading of 0034: " + c["key_description"][:100],
                          "notes": "A6.1 replication of 0034 at 27-29"})
    bounds = {
        "item": "A6.1 (replication of 0222's cell 0034 P27-29)", "k4_value": K4_VALUE,
        "copies_in_0222": "10, best 4-7 (0216's regeneration)", "fresh_seed": 4222,
        "search": "0034's frozen sweep at periods 27, 28, 29: 24 conventions, 20 restarts, quadgram climb of the 3-5 free slots",
        "fresh_copies": len(copies), "first_copy_at_or_above": first, "verdict": verdict,
        "p_bound_if_unresolved": None if first is not None else round(1 / (len(copies) + 11), 4),
        "flag_rule": "80 fresh copies all below K4 (p < 0.05/4)", "copies": copies,
        "judge_texts_sent": calls, "judge_calls_estimated": "24 per batch, at most 240",
        "judge_none": sum(c["none"] for c in copies), "seconds": round(time.time() - t0),
        "controls": "quadgram scores of the 0034 search's readings at 27-29 on 0216's 10 copies and on the fresh copies (issue #88)", "exhaustive": False,
    }
    notes = f"{verdict}: {len(copies)} fresh copies, first at or above K4's 8: copy {first}; copies' best scores {[c['best'] for c in copies]}"
    return {"candidates": cands, "bounds": bounds, "notes": notes, "controls": controls}


def encrypt(plaintext, key):
    """0034's own encrypt: a periodic key on the stated tables."""
    return _load(key["exp"]).encrypt(plaintext, key["key"])


def worked_example(ctx, key):
    raw = json.loads((next((ROOT / "experiments").glob("0034-*")) / "raw.json").read_text())
    from kryptos.judge import mask
    c = next(c for c in raw["candidates"] if c["key_description"].startswith("period 27"))
    return "\n".join(["0034's reading of K4 at key length 27 (3 free key slots climbed):", f"  reading      {c['plaintext']}",
                      f"  judge sees   {mask(c['plaintext'])}", "",
                      "K4's best of its three readings (27, 28, 29) scored 8; a fresh copy's three readings by the same search must reach 8."])
