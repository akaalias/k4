"""Experiment 0217. See program.md for the contract."""

EXPERIMENT = {
    "slug": "a13-the-backwards-reading-of-0034-against-more-fresh-copies",
    "title": "A13.3, replication: 0034's saved readings read backwards, the one candidate 0216 left unresolved, against more fresh copies of the same search, with reversed messages planted through 0034's own climb",
    "family": "1-keyed-periodic",
    "parent": "0216-a13-the-saved-readings-against-their-own-search-on-fresh-copies-rerun",
    "changed": (
        "A13.3 (Stage 2, step 3, issue #75), the replication 0216 began and its clock cut short. 0216 found K4 above "
        "every copy in 2 of 112 cells; 0034/eng_keep_nth met a fresh copy at copy 6, but 0034/eng_reverse (K4 -5.458, "
        "the best of its 18 readings read backwards, from period 71) stayed above all 8 fresh copies drawn before the "
        "clock (and all 10 of pass 1). Here the same pre-registered sequence continues: fresh copies 8 onward of seed "
        "'3113', each a plain shuffle run through 0034's frozen sweep unchanged (24 conventions, periods 27-29 and "
        "53-95 every third, 20 restarts), eight at a time, until one copy's best backwards score is at or above K4's "
        "(not a flag), or the clock (unresolved, with its p bound). New: reversed messages planted under 0034's own "
        "method at period 71 and climbed by its own climb, to say whether this cell can see a reversal at all."
    ),
    "hypothesis_expert": (
        "A13 (knowledge/12-assumptions.md), C4(a) (Scheidt 2005, 2015: 'I masked the English language'; a plaintext "
        "transform before the keyed stage), reading: the mask is a reversal of the message, the simplest move-only mask "
        "(0023 closed it exactly for short periodic keys; here the long periods 53-95 where the known letters leave "
        "47-71 free key slots). Cipher: one periodic tableau key on the standard or KRYPTOS alphabets, 24 conventions, "
        "periods 27-29 and 53-95 every third (0034's space), free slots completed by a forward quadgram climb. Statistic: "
        "eng_reverse (tools/a13_structure.py), the quadgram score of the reading written backwards, best over a text's 18 "
        "readings. The cell was one of 112 pre-registered in reports/a13-structure-check.md (flag at p < 0.05/112, all of "
        "2,242 fresh copies below K4). K4's two best backwards readings (periods 71 and 77, -5.458 and -5.525) both "
        "exceed every copy's best so far (-5.553), which is why it needs fresh copies, not argument. Plants measure "
        "power: a forward climb pulls the free letters toward forward English, so a reversed message may be destroyed "
        "by the very search that should reveal it."
    ),
    "hypothesis_eli5": (
        "An old search (0034) produced 18 readings of K4 with every known letter in place and threw them away as "
        "gibberish. One of them reads a little better backwards than any reading the same search made from scrambled "
        "copies of the carving, which could mean Sanborn wrote his message backwards before enciphering it, or could be "
        "luck. Luck is tested the only honest way: run the same search on more scrambled copies until one of them "
        "reads as well backwards. We also hide some backwards messages of our own and see whether this search and "
        "test would notice them."
    ),
    "prediction": (
        "A fresh copy reaches K4's backwards score within the 40 or so copies the clock allows (K4 has led 18 copies, "
        "which luck alone does about one time in 19), so the cell is not a flag and A13.3 closes with no flag. "
        "The reversed plants are found 0 or 1 times in 4: the forward climb overwrites the free letters, so the "
        "backwards test on this search has little power, and a 'nothing found' here says little about reversal. "
        "Zero candidates pass gate 4."
    ),
    "method": (
        "1. K4: 0034's 18 saved readings (24 of 24 known letters), each re-enciphered by 0034's frozen encrypt; the best "
        "backwards score. "
        "2. Reversed plants: four messages from Carter's 1923 book, written backwards, the 24 known letters set after "
        "the reversal, enciphered under 0034's method with a random convention and a random period-71 key; each climbed "
        "by 0034's frozen sweep at period 71 only (a slice: one period of its 18, which can only lower the plant's best); "
        "found when its best backwards score is above every 0034 copy's. "
        "3. Fresh copies 8 onward of seed '3113' (copies 0-7 were 0216's), 0034's sweep unchanged, eight at a time on "
        "eight cores, until one copy is at or above K4, or 2,242 copies all below (a flag), or the clock. "
        "4. Verdict: caught (not a flag; A13.3 closes), or unresolved with p at most 1/(copies + 1)."
    ),
    "walkthrough": (
        "1. Take 0034's reading at period 71 with all 24 known letters in place. "
        "2. Write it backwards and score the backwards text for English: -5.458. "
        "3. Scramble the carved letters, run 0034's search on the scramble, and do the same with each of its 18 "
        "readings; keep its best backwards score. "
        "4. If that score reaches -5.458, K4's lead was luck: stop. "
        "5. If not, scramble again and repeat; 2,242 scrambles in a row below K4 would be a real signal. "
        "6. Separately, write a known message backwards, encipher it the 0034 way, run the search, and see whether "
        "the backwards score finds it."
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
E = "0034"
TEST = "eng_reverse"
PASS1 = ROOT / "reports" / "a13-structure-data" / "pass1_copies.json"
FIRST_FRESH = 8      # 0216 drew copies 0-7 of this sequence
N_FLAG = 2242        # copies all below K4 for p = 1/2243 < 0.05/112
PLANT_P = 71
N_PLANTS = 4
MARGIN = 900


def a13():
    import tools.a13_check as a
    return a


def rep_copy(i):
    """Fresh copy i, built as 0216's rep_copy built 0034's (plain shuffle, seed '3113')."""
    from kryptos.facts import K4
    rng = random.Random(f"3113/{E}/{i}")
    sh = list(K4); rng.shuffle(sh)
    return (E, i, "".join(sh), rng.randrange(10 ** 9))


def best_test(rows):
    a = a13()
    vals = [a.battery(r)[TEST] for _, r in rows if r and a.fits24(r)]
    return max(vals) if vals else None


def _carter():
    src = (ROOT / "knowledge/sources/carter-1923-tomb-of-tutankhamen-vol1.txt").read_text(errors="ignore").upper()
    return re.sub("[^A-Z]", "", src)


def reversed_plant(rng):
    from kryptos.facts import KNOWN
    letters = _carter()
    s0 = rng.randrange(20000, len(letters) - 200)
    t = list(letters[s0:s0 + N][::-1])
    for q, ch in KNOWN.items():
        t[q - 1] = ch
    return "".join(t)


def plant_job(args):
    idx, ct, seed = args
    from kryptos.alphabets import conventions
    from kryptos.facts import KNOWN
    from kryptos.scorer import english_score
    m = a13().mod(E)
    res = m.sweep(ct, KNOWN, list(conventions()), english_score, random.Random(seed), m.RESTARTS, lambda: 10 ** 9, [PLANT_P])
    best = max(res, key=lambda r: r[0]) if res else None
    return idx, ([(f"period {PLANT_P}", best[3])] if best else [])


def _any(args):
    if args[0] == "plant":
        return plant_job(args[1])
    return a13().p1_job(args[1])


def run(ctx):
    a = a13()
    from kryptos.alphabets import ALPHABETS, conventions
    from kryptos.scorer import english_score, free_text
    t0 = time.time()
    if getattr(sys.modules.get(__name__), "_any", None) is not _any:  # make the pool's pickles resolve
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    m = a.mod(E)

    # 1. K4's saved readings
    d = next((ROOT / "experiments").glob(f"{E}-*"))
    rows = [c for c in json.loads((d / "raw.json").read_text())["candidates"] if a.fits24(c["plaintext"])]
    reenc = all(m.encrypt(c["plaintext"], c["key"]) == ctx.K4 for c in rows)
    k4_vals = sorted(((a.battery(c["plaintext"])[TEST], c) for c in rows), key=lambda t: -t[0])
    k4 = k4_vals[0][0]

    # the copies so far: pass 1's ten
    p1 = json.loads(PASS1.read_text())
    p1_vals, controls = [], []
    for key, v in p1.items():
        if key.startswith(E + "/"):
            p1_vals.append(best_test(v["rows"]))
            controls.append(max(english_score(free_text(r)) for _, r in v["rows"] if r and a.fits24(r)))
    copies_max = max(p1_vals)

    with get_context("fork").Pool(8) as pool:
        # 2. reversed plants through 0034's own climb at period 71
        prng = random.Random(2170)
        convs = list(conventions())
        pjobs, truths, settings = [], {}, {}
        for i in range(N_PLANTS):
            pt = reversed_plant(prng)
            pa, ca, ka, md = prng.choice(convs)
            key = "".join(prng.choice(ALPHABETS[ka]) for _ in range(PLANT_P))
            ct = m.encrypt(pt, {"pa": pa, "ca": ca, "ka": ka, "m": md, "key": key})
            truths[i], settings[i] = pt, f"{pa}/{ca}/{ka}/{md}"
            pjobs.append(("plant", (i, ct, prng.randrange(10 ** 9))))
        plants = []
        for idx, prow in pool.map(_any, pjobs, chunksize=1):
            v = best_test(prow)
            truth = truths[idx]
            plants.append({"i": idx, "convention": settings[idx], "reading_value": v,
                           "plaintext_value": a.battery(truth)[TEST], "letters_right": sum(x == y for x, y in zip(prow[0][1], truth)) if prow else 0,
                           "found": bool(v is not None and v > copies_max), "reading": prow[0][1] if prow else None})
        t_plants = time.time() - t0

        # 3. fresh copies, eight at a time, until one is at or above K4
        fresh, first_at, fmax, per_copy, i = [], None, -math.inf, 3800.0, FIRST_FRESH
        while first_at is None and len(fresh) < N_FLAG:
            if ctx.time_left() < MARGIN + 1.3 * per_copy:
                break
            tb = time.time()
            res = sorted(pool.map(_any, [("p1", rep_copy(i + j)) for j in range(8)], chunksize=1), key=lambda r: r[1])
            per_copy = time.time() - tb
            for _, idx, crows, secs in res:
                v = best_test(crows)
                if v is None:
                    continue
                fresh.append({"copy": idx, TEST: v, "seconds": round(secs, 1)})
                controls.append(max(english_score(free_text(r)) for _, r in crows if r and a.fits24(r)))
                fmax = max(fmax, v)
                if v >= k4 and first_at is None:
                    first_at = idx
            i += 8

    n_rep = 8 + len(fresh)  # 0216's eight fresh copies, all below, then these
    if first_at is not None:
        verdict, p = "not a flag", None
    elif len(fresh) + 8 >= N_FLAG:
        verdict, p = "FLAG", 1 / (n_rep + 1)
    else:
        verdict, p = "unresolved", 1 / (n_rep + 10 + 1)
    found = sum(pl["found"] for pl in plants)

    cands = [{"plaintext": c["plaintext"], "key": {"exp": E, "key": c["key"]}, "key_bits": c.get("key_bits", 0.0),
              "key_description": f"0034's saved reading, backwards score {v:.3f}: " + c.get("key_description", "")[:100],
              "notes": "A13.3 replication: K4's best backwards readings"} for v, c in k4_vals[:3]]
    bounds = {
        "item": "A13.3", "cell": f"{E}/{TEST}", "pre_registered": "2026-10-21, reports/a13-structure-check.md; replication rule in 0216",
        "k4_value": k4, "k4_period": k4_vals[0][1]["key_description"][:10], "k4_readings": len(rows), "k4_reencrypt_ok": reenc,
        "k4_second": k4_vals[1][0],
        "pass1_copies": len(p1_vals), "pass1_max": copies_max,
        "fresh_in_0216": 8, "fresh_in_0216_max": -5.556524387129956,
        "fresh_here": len(fresh), "fresh_here_first_index": FIRST_FRESH, "fresh_here_max": fmax,
        "first_copy_at_or_above": first_at, "verdict": verdict, "p_bound_if_unresolved": p,
        "fresh_values": fresh,
        "search": "0034's frozen sweep unchanged: 24 conventions, periods 27-29 and 53-95 every third, 20 restarts, forward quadgram climb of the free slots",
        "plants": plants, "plants_found": f"{found} of {len(plants)}",
        "plant_design": f"Carter 1923 written backwards, 24 known letters set after the reversal, random convention, random period-{PLANT_P} key; climbed by 0034's sweep at period {PLANT_P} only (sliced); found = best backwards score above every pass-1 copy's ({copies_max:.3f})",
        "plant_seconds": round(t_plants, 1),
        "seconds": round(time.time() - t0, 1),
    }
    notes = (f"0034/eng_reverse: K4 {k4:.3f}; {len(fresh)} more fresh copies (max {fmax:.3f}); "
             f"first at or above: {first_at}; verdict {verdict}. Reversed plants found {found} of {len(plants)}.")
    return {"candidates": cands, "controls": controls, "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    """0034's frozen encrypt."""
    return a13().mod(key["exp"]).encrypt(plaintext, key["key"])


def worked_example(ctx, key):
    a = a13()
    d = next((ROOT / "experiments").glob(f"{E}-*"))
    rows = [c for c in json.loads((d / "raw.json").read_text())["candidates"] if a.fits24(c["plaintext"])]
    v, c = max(((a.battery(c["plaintext"])[TEST], c) for c in rows), key=lambda t: t[0])
    return "\n".join([f"0034's reading, {c['key_description'][:10]}: {c['plaintext']}",
                      f"written backwards:            {c['plaintext'][::-1]}",
                      f"English score of the backwards text: {v:.3f}",
                      "a fresh scrambled copy through the same search counts against it when its best backwards score is at or above this"])
