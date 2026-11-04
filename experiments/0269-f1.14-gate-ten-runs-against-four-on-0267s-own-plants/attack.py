"""Experiment 0269. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f1.14-gate-ten-runs-against-four-on-0267s-own-plants",
    "title": "F1.14's gate: 0267's 24 plants (hand key schedules on two free alphabets) and 12 kept-place copies each, climbed ten times, power after r runs for r = 1-10",
    "family": "1-keyed-periodic",
    "parent": "0267-f1.4-two-alphabet-residue-decided-by-four-runs-with-stand-ins",
    "changed": (
        "F1.14 (rerun of F1.4's two-alphabet residue at ten runs) waits on this gate: does ten runs lift 0267's plants by 3 "
        "or more of 24 over four? 0267's plants are regenerated exactly (its frozen setting scan and plant draws), and each "
        "plant and 12 kept-place copies (from the plant's own witness, as 0267) are climbed with ten independent runs of "
        "0267's generalised tempering, every run's best kept, as D1b (0257) did for periodic keys."
    ),
    "hypothesis_expert": (
        "0267 found 12 of 24 plants (8 clean, 4 Sanborn-style) with D1b's four runs on hand key schedules (0128's skip, "
        "stutter, back and forth, triangle, square, restart per line) over two free alphabets (Quagmire IV), against D1b's "
        "66 of 96 for periodic keys at 13 and 16. The settings here have up to 31 slots, so the climb has more key letters "
        "to find and may profit more from extra runs than D1b measured (+5 of 96 from four to ten). The gate set in F1.14's "
        "row: run F1.14 (about $25 on AWS) only if ten runs find at least 3 more of these 24 than four. Clue entries C20(d), "
        "C27(c)."
    ),
    "hypothesis_eli5": (
        "Last run, our search found only half of the test messages we hid, in a version of the cipher where Sanborn steps "
        "through his key word with a twist and uses two scrambled alphabets. Searching each text ten times instead of four "
        "might find more. Before paying for the full ten-times rerun, we check on the same 24 hidden messages whether ten "
        "searches find at least three more than four."
    ),
    "prediction": (
        "Four runs find 11-13 of 24 (0267: 12); ten runs find 1-3 more (D1b's +5 of 96 scaled, a little more for the longer "
        "keys). Gate likely not met. Zero candidates."
    ),
    "method": (
        "1. 0267's run() steps 1-2 unchanged from its frozen attack.py: every 0128 schedule decided exactly on K4 on two free "
        "alphabets (4,706 fit), then its 24 plants (12 clean, 12 Sanborn-style) drawn on fitting settings with its seed, each "
        "with an exact witness. "
        "2. Per plant: the plant and 12 kept-place copies of its ciphertext, each climbed with 10 independent runs of 0267's "
        "climb (one run per seed), every run's best score kept. "
        "3. Found after r runs: the plant's best of runs 1..r above all 12 copies' bests of runs 1..r. "
        "4. Gate: found(10) - found(4) >= 3."
    ),
    "walkthrough": (
        "1. Take one of 0267's hidden test messages, enciphered with a skipping key schedule and two scrambled alphabets. "
        "2. Make 12 copies with the 73 letters at unknown places shuffled. "
        "3. Search each of the 13 texts ten separate times for its most English-looking reading; write down each search's best. "
        "4. For r = 1 to 10, compare the message's best of its first r searches with each copy's best of its first r. "
        "5. Count the messages that beat all 12 copies at r = 4 and at r = 10."
    ),
    "expected_minutes": 45,
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
RUNS = 10
N_OWN = 12
GATE = 3
_MODS = {}


def M():
    """0267's attack, frozen."""
    if "m" not in _MODS:
        path = next((ROOT / "experiments").glob("0267-*")) / "attack.py"
        spec = importlib.util.spec_from_file_location("frozen0267", path)
        m = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = m
        spec.loader.exec_module(m)
        m.ROOT = ROOT
        _MODS["m"] = m
    return _MODS["m"]


def plants_of_0267(ctx, pool, W):
    """0267's run() steps 1-2, line for line: the fitting settings, then the plants."""
    m = M()
    m44, m52 = m._load("0144"), m._load("0252")
    m._load("0128"); m44.lib(); m.glib()
    m20, m26 = m._load("0140").load_0120(), m._load("0226")
    k4 = ctx.K4
    rng = random.Random(m.SEED)
    items, seen = [], set()
    for g, lst in m52.f14_settings().items():
        for name, slot, n in lst:
            if slot not in seen:
                seen.add(slot); items.append((name, slot, n))
    chunks = [(i, items[i::W * 4], k4) for i in range(W * 4)]
    decided = [x for lst in pool.imap_unordered(m._fit_job, chunks) for x in lst]
    decided.sort(key=lambda x: x[0])
    fit = [(name, slot, n) for name, slot, n, s, _w in decided if s == "fit"]
    per = {13: None, 16: None}
    for L in per:
        while not isinstance(per[L], list):
            per[L] = m.witness(k4, [i % L for i in range(N)], rng)
    texts = [("clean", pt) for _, pt in m20.make_plants(ctx.KNOWN, 10, rng, m.PLANTS // 2)]
    for a in (0, 1, 2):
        texts += m26.class_texts(rng, a)[:m.PLANTS // 6]
    plants = []
    for idx, (cls, pt) in enumerate(texts):
        while True:
            fi = rng.randrange(len(fit))
            name, slot, n = fit[fi]
            P = list(range(26)); C = list(range(26)); rng.shuffle(P); rng.shuffle(C)
            key = [rng.randrange(26) for _ in range(n)]
            pc = m.encipher(pt, slot, P, C, key)
            y0 = m.witness(pc, slot, rng)
            if isinstance(y0, list):
                break
        plants.append({"idx": idx, "cls": cls, "setting": name, "pt": pt, "pc": pc, "slot": slot, "n": n, "y0": y0})
    return len(fit), plants


def _job(args):
    key, text, slot, n, seed, y0 = args
    m = M()
    t0 = time.time()
    out = []
    for r in range(RUNS):
        sc, rd = m.climb(text, slot, n, seed * 1000 + r, y0, runs=1)
        out.append([sc, rd])
    return key, {"runs": out, "secs": round(time.time() - t0, 1)}


def run(ctx):
    import multiprocessing as mp
    t_start = time.time()
    W = int(os.environ.get("K4_WORKERS", 8))
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    m = M()
    m._load("0144").lib(); m.glib()
    with mp.get_context("fork").Pool(W) as pool:
        nfit, plants = plants_of_0267(ctx, pool, W)
    import json
    raw = json.loads((next((ROOT / "experiments").glob("0267-*")) / "raw.json").read_text())
    each67 = (raw.get("bounds") or raw["result"]["bounds"])["plants"]["each"]
    match = sum(each67[str(p["idx"])]["setting"] == p["setting"] for p in plants)
    assert nfit == 4706 and match == len(plants), ("0267's plants not reproduced", nfit, match)
    jobs = []
    for p in plants:
        rng = random.Random(26900 + p["idx"])
        jobs.append((f"plant:{p['idx']}", p["pc"], p["slot"], p["n"], rng.randrange(10 ** 6), p["y0"]))
        for g in range(N_OWN):
            jobs.append((f"own:{p['idx']}:{g}", M().kept_place(p["pc"], rng), p["slot"], p["n"], rng.randrange(10 ** 6), p["y0"]))
    saved = getattr(ctx, "saved", {}) or {}
    res = {j[0]: saved[j[0]] for j in jobs if j[0] in saved}
    todo = [j for j in jobs if j[0] not in res]
    ctx.progress(len(res), len(jobs), "texts")
    with mp.get_context("fork").Pool(W) as pool:
        for key, out in pool.imap_unordered(_job, todo, chunksize=1):
            res[key] = out
            ctx.save(key, out)
            ctx.progress(len(res), len(jobs), "texts")

    def best(key, r):
        return max(x[0] for x in res[key]["runs"][:r])

    power, each = {}, {}
    for r in range(1, RUNS + 1):
        f = {"clean": 0, "sanborn": 0}
        for p in plants:
            ok = best(f"plant:{p['idx']}", r) > max(best(f"own:{p['idx']}:{g}", r) for g in range(N_OWN))
            f["clean" if p["cls"] == "clean" else "sanborn"] += ok
        power[r] = {**f, "total": f["clean"] + f["sanborn"]}
    for p in plants:
        k = f"plant:{p['idx']}"
        rd = max(res[k]["runs"], key=lambda x: x[0])[1]
        each[p["idx"]] = {"cls": p["cls"], "setting": p["setting"], "slots": p["n"],
                          "found_at_4": best(k, 4) > max(best(f"own:{p['idx']}:{g}", 4) for g in range(N_OWN)),
                          "found_at_10": best(k, 10) > max(best(f"own:{p['idx']}:{g}", 10) for g in range(N_OWN)),
                          "letters_right_10": sum(a == b for a, b in zip(rd, p["pt"]))}
    gain = power[10]["total"] - power[4]["total"]
    met = gain >= GATE
    bounds = {
        "item": "F1.14 gate", "settings_fit_k4": nfit, "plants_match_0267_settings": match, "plants": len(plants), "own_copies": N_OWN, "null_per_plant": "1/13",
        "decider": "0267's climb (0144's tempering generalised to any slot map, 16 x 625 x 1000 per run) from the plant's exact witness",
        "runs": RUNS, "power_by_runs": power, "gain_10_over_4": gain, "gate": GATE, "gate_met": met,
        "record_0267_plants": "8/12 clean, 4/12 Sanborn-style at four runs, copies one at a time",
        "each": each, "texts": len(jobs), "core_seconds": round(sum(v["secs"] for v in res.values())),
        "compute_seconds": round(time.time() - t_start), "resumed_units": len(jobs) - len(todo), "exhaustive": False,
        "cost_estimate": "312 texts x 10 runs x about 13 s = about 11 core-hours, plus 0267's setting scan; on AWS about 30 min, about $0.30",
    }
    notes = (f"F1.14 gate: 0267's plants found after 4 runs {power[4]['total']}/24, after 10 {power[10]['total']}/24 "
             f"(gain {gain}, gate {GATE}: {'met, run F1.14' if met else 'not met, F1.14 closed'}); power by runs "
             f"{[power[r]['total'] for r in range(1, RUNS + 1)]}.")
    controls = [max(x[0] for x in v["runs"]) for k, v in res.items() if k.startswith("own:")]
    return {"candidates": [], "bounds": bounds, "notes": notes, "controls": controls}


def encrypt(plaintext, key):
    """No candidate is submitted."""
    return plaintext


def worked_example(ctx, key):
    return "\n".join([
        "F1.14's gate: does searching ten times instead of four find more hidden messages?", "",
        "  one hidden message and its 12 shuffled copies, each searched ten times; best of the first r searches:",
        "  found at r when the message's best beats all 12 copies' bests.",
        "  24 messages (0267's own); run the full rerun only if r = 10 finds at least 3 more than r = 4."])
