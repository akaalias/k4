"""Experiment 0253. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f1.4-one-alphabet-residue-decided-by-the-one-run-decider",
    "title": "F1.4: every hand key schedule K4 fits on one free alphabet (2,093 settings, both forms), each decided by D1's one-run decider against copies climbed one at a time",
    "family": "1-keyed-periodic",
    "parent": "0252-d2-one-run-decider-power-and-cost-on-schedules-and-moves",
    "changed": (
        "F1.4, the one-alphabet residue reopened by D2 (0252). 0252 measured the one-run decider's power on F1.4's "
        "schedules (37 of 48 per group against 6 own copies) and costed the residue at about 41 core-hours. Here every "
        "one of the 2,093 (schedule, slot count, form) settings K4 fits is decided: K4 is climbed once, then shuffles that "
        "the exact decider also fits at that setting are climbed one at a time until one reaches K4's score, up to 12; "
        "where K4 beats all 12 the copies go on to 100. 24 plants (12 clean, 12 Sanborn-style) on settings K4 fits go "
        "through the same decision in the same run."
    ),
    "hypothesis_expert": (
        "F1.4: a keyed table with a hand key schedule other than a plain repeat (C20(d): tableau rows as keys; the "
        "schedules of 0126-0128: one key letter skipped every m letters, stutter, back and forth, triangle, square, a "
        "restart per carved line), with one free alphabet on both sides (Quagmire III with an unknown order, Sanborn's "
        "'slightly different' tableau, C27(c)), Beaufort or added form. 0127/0128 closed the standard and KRYPTOS tables "
        "exactly; on a free alphabet K4 fits 2,093 settings at the copies' rate (0252's exact recount: 2,016 skip "
        "schedules, 77 others), each with its 24 known letters satisfied by some alphabet, so the known letters cannot "
        "decide them and English must. The decider is 0140's tempering climb (one run, 16 x 625 x 1000) generalised to any "
        "slot map (0252, identical to 0140 on plain periodic keys), with copies drawn as shuffles the exact decider fits "
        "at the same setting, so K4 and its copies have the same freedom. Clue entries: C20(d), C27(c), C5(a)."
    ),
    "hypothesis_eli5": (
        "Sanborn may have used the cipher table with a twist in how he stepped through the key word (skipping a letter "
        "now and then, going back and forth) and with his own scrambled alphabet. About two thousand such twists are "
        "consistent with the 24 known letters, so those letters cannot tell them apart. For each one we search for the "
        "most English-looking reading of K4 and do the same on scrambled copies of K4 that fit the same twist equally "
        "well; a real answer should read better than all its copies."
    ),
    "prediction": (
        "No setting stands out: the number of settings where K4 beats all 12 copies is within the binomial range for "
        "1/13 (about 161 of 2,093, sd about 12; anything above 186 is an excess to chase), and the settings where K4 "
        "beats 100 copies are about 1 in 101 (about 21, at most about 30). Plants found (above all 12 own copies) about "
        "16 of 24 (0252's 37 of 48 against 6 copies, lower against 12). Zero candidates returned (see notes)."
    ),
    "method": (
        "1. Settings: 0252's f14_settings() (every 0128 schedule at every slot count 2-31, as a slot map over the 97 places, "
        "deduplicated), both forms, each decided exactly on K4 by 0128's decide(); the fitting ones are the cell. "
        "2. Per setting (one job, seeded by its index): climb K4 once with 0252's climb(); then draw shuffles of K4 until "
        "one fits the setting exactly, climb it, and stop at the first copy whose best is at or above K4's; at most 12 "
        "copies, and where K4 is above all 12, go on to at most 100. Record K4's score, reading, and the number of copies "
        "it stayed above. "
        "3. Plants: 12 clean (Carter windows, 0120's rule) and 12 Sanborn-style (0226's classes), each on a setting drawn "
        "from the cell, random alphabet and key, decided by the same job without the escalation; found if above all 12. "
        "4. Verdict: the count of settings where K4 beats all 12 against Binomial(n, 1/13); settings above 100 copies "
        "listed with their readings and known letters, to be chased in a row of their own if the count is in excess."
    ),
    "walkthrough": (
        "1. Pick a schedule, say: key of 11 letters, skip one key letter after every 7 carved letters. "
        "2. Write the key slot under each of the 97 carved letters. "
        "3. Check with the 24 known letters that some alphabet makes them agree (two known places in one slot must "
        "differ by the same amount on the alphabet). "
        "4. Search alphabets and keys for the most English-looking reading of K4 under that slot map. "
        "5. Shuffle K4's letters until the shuffle also passes step 3, and search it the same way. "
        "6. If the shuffle reads as well as K4, stop: K4 is ordinary there. Otherwise shuffle again, up to 12 times "
        "(100 if K4 keeps winning). "
        "7. Count how often K4 won all 12; chance alone gives about one setting in 13."
    ),
    "expected_minutes": 180,
}

import os
import random
import time
from pathlib import Path

N = 97
ROOT = Path(__file__).resolve().parent
BASE, ESC = 12, 100
PLANTS = 12
_MODS = {}


def M():
    if "m" not in _MODS:
        import importlib.util
        import sys
        path = next((ROOT / "experiments").glob("0252-*")) / "attack.py"
        spec = importlib.util.spec_from_file_location("frozen0252", path)
        m = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = m
        spec.loader.exec_module(m)
        m.ROOT = ROOT
        _MODS["m"] = m
    return _MODS["m"]


def _fit_job(args):
    group, items, k4 = args
    return M()._f14_job((group, items, k4))


def decide(text, st, seed, esc):
    """One run on text, then fitting shuffles one at a time until one reaches it. -> dict."""
    m = M()
    rng = random.Random(seed)
    w = m.witness(text, st, random.Random(1))
    t0 = time.time()
    score, _, reading = m.climb(text, st, rng.randrange(10 ** 9), w)
    copies, tries, lost = [], 0, 0
    limit = BASE
    while len(copies) < limit:
        sh = list(text)
        ok = None
        for _ in range(200000):
            rng.shuffle(sh); tries += 1
            cw = m.witness("".join(sh), st, rng)
            if cw is not None:
                ok = ("".join(sh), cw)
                break
        if ok is None:
            lost += 1
            break
        cs = m.climb(ok[0], st, rng.randrange(10 ** 9), ok[1])[0]
        copies.append(cs)
        if cs >= score:
            break
        if len(copies) == BASE and esc:
            limit = ESC
    above = len(copies) if all(c < score for c in copies) else len(copies) - 1
    return {"score": score, "reading": reading, "copies": copies, "above": above,
            "tries": tries, "lost": lost, "secs": round(time.time() - t0, 1)}


def _job(args):
    key, text, st, seed, esc = args
    return key, decide(text, st, seed, esc)


def run(ctx):
    import multiprocessing as mp
    import sys
    import types
    from math import exp, lgamma, log
    t_start = time.time()
    W = int(os.environ.get("K4_WORKERS", 8))
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    m = M()
    m._load("0140"); m._load("0128"); m._load("0129"); m.glib()
    check = m.self_check(ctx)
    m20, m26 = m._load("0140").load_0120(), m._load("0226")
    k4 = ctx.K4

    # 1. settings K4 fits (exact), deduplicated across groups
    f14 = m.f14_settings()
    jobs = [(g, items[i::W * 4], k4) for g, items in f14.items() for i in range(W * 4)]
    fit, seen = [], set()
    with mp.get_context("fork").Pool(W) as pool:
        got = sorted(x for g, lst in pool.imap_unordered(_fit_job, jobs) for x in [(g, it) for it in lst])
    for g, (name, slot, n, form) in got:
        if (slot, form) not in seen:
            seen.add((slot, form)); fit.append((g, name, (slot, tuple(range(N)), n, form)))
    ctx.progress(0, len(fit) + 2 * PLANTS, "settings")

    # 2. plants on settings drawn from the cell
    rng = random.Random(2530)
    prng = random.Random(2531)
    texts = [("clean", pt) for _, pt in m20.make_plants(ctx.KNOWN, 10, rng, PLANTS)]
    for a in (0, 1, 2):
        texts += m26.class_texts(rng, a)[:PLANTS // 3]
    plants, pmeta = [], {}
    for idx, (cls, pt) in enumerate(texts):
        g, name, st = fit[prng.randrange(len(fit))]
        order = list(range(26)); prng.shuffle(order)
        key = [prng.randrange(26) for _ in range(st[2])]
        pc = m.encipher(pt, st, order, key)
        assert m.decipher(pc, st, order, key) == pt and m.fits(pc, st, prng), (idx, name)
        pmeta[idx] = {"cls": cls, "setting": name, "form": st[3], "pt": pt}
        plants.append((("plant", idx), pc, st, 900000 + idx, False))

    # 3. every setting, K4 and plants in one pool
    work = plants + [(("k4", i), k4, st, 1000 + i, True) for i, (g, name, st) in enumerate(fit)]
    res = {}
    with mp.get_context("fork").Pool(W) as pool:
        for key, out in pool.imap_unordered(_job, work, chunksize=1):
            res[key] = out
            ctx.progress(len(res), len(work), "settings")

    # 4. verdicts
    found = {}
    for idx, v in pmeta.items():
        r = res[("plant", idx)]
        v.update(found=r["above"] >= BASE, above=r["above"], score=r["score"],
                 letters_right=sum(a == b for a, b in zip(r["reading"], v.pop("pt"))))
        found.setdefault(v["cls"] if v["cls"] == "clean" else "sanborn", []).append(v["found"])
    n = len(fit)
    k12 = sum(1 for i in range(n) if res[("k4", i)]["above"] >= BASE)
    k100 = sum(1 for i in range(n) if res[("k4", i)]["above"] >= ESC)
    q12, q100 = 1 / (BASE + 1), 1 / (ESC + 1)
    def tail(k, q):
        return sum(exp(lgamma(n + 1) - lgamma(j + 1) - lgamma(n - j + 1) + j * log(q) + (n - j) * log(1 - q))
                   for j in range(k, n + 1))
    p12, p100 = tail(k12, q12), tail(k100, q100)
    hist = {}
    for i in range(n):
        a = res[("k4", i)]["above"]
        b = "0" if a == 0 else "1-11" if a < BASE else "12-99" if a < ESC else "100"
        hist[b] = hist.get(b, 0) + 1
    top = sorted(range(n), key=lambda i: (-res[("k4", i)]["above"], -res[("k4", i)]["score"]))[:25]
    top_list = []
    for i in top:
        g, name, st = fit[i]
        r = res[("k4", i)]
        top_list.append({"group": g, "setting": name, "form": st[3], "slots": st[2], "above": r["above"],
                         "copies_climbed": len(r["copies"]), "score": r["score"], "copies_max": max(r["copies"]) if r["copies"] else None,
                         "reading": r["reading"], "known_in_place": sum(r["reading"][q - 1] == c for q, c in ctx.KNOWN.items())})
    secs = [r["secs"] for r in res.values()]
    climbs = sum(1 + len(r["copies"]) for r in res.values())
    bounds = {
        "item": "F1.4 (one free alphabet residue, reopened by D2/0252)",
        "decider": "D1's one-run decider: 0140's tempering (16 x 625 x 1000) generalised to any slot map (0252); copies = shuffles the exact decider fits at the same setting, climbed one at a time, stop at the first at or above K4, at most 12, escalated to 100 where K4 beats all 12",
        "self_check_against_0140": check,
        "settings_listed": {g: len(v) for g, v in f14.items()}, "k4_fitting_settings": n,
        "k4_fitting_by_group": {g: sum(1 for x in fit if x[0] == g) for g in f14},
        "k4_above_all_12": k12, "expected_by_chance_12": round(n * q12, 1), "binomial_p_12": p12,
        "k4_above_all_100": k100, "expected_by_chance_100": round(n * q100, 1), "binomial_p_100": p100,
        "k4_copies_beaten_histogram": hist,
        "settings_with_copy_generation_failure": sum(1 for i in range(n) if res[("k4", i)]["lost"]),
        "top_settings": top_list,
        "plants": {"clean_found": [sum(found.get("clean", [])), len(found.get("clean", []))],
                   "sanborn_found": [sum(found.get("sanborn", [])), len(found.get("sanborn", []))],
                   "null_per_plant": "1/13", "each": pmeta},
        "climbs": climbs, "core_seconds": round(sum(secs)), "compute_seconds": round(time.time() - t_start),
        "exhaustive": True, "exhaustive_over": "every setting of 0128's schedules (slot counts 2-31) K4 fits on one free alphabet, both forms; each decided at one-run power",
        "expected_total_time": "about 2,093 x (1 + 3.1) + 21 x 26 + 24 x 13 climbs, about 9,500 at about 17 core-s: about 45 core-hours, 2-3 h on 32 cores",
    }
    notes = (f"F1.4 one-alphabet residue: {n} settings; K4 above all 12 copies in {k12} (chance {n / 13:.0f}, p {p12:.3g}), "
             f"above all 100 in {k100} (chance {n / 101:.1f}, p {p100:.3g}); plants found clean {bounds['plants']['clean_found']}, "
             f"Sanborn-style {bounds['plants']['sanborn_found']}. No candidate returned: a per-setting reading above its own "
             f"copies is expected about {n / 13:.0f} times by chance, so gate 4 on one setting's copies would not account for "
             f"the {n} settings searched; the verdict is the count, and the top readings are in bounds.")
    controls = [c for i in range(n) for c in res[("k4", i)]["copies"]][:2000]
    return {"candidates": [], "bounds": bounds, "notes": notes, "controls": controls}


def encrypt(plaintext, key):
    """No candidate is submitted. key = {'slot': [...], 'mpos': [...], 'n': n, 'form': 'V'|'B', 'order': [...], 'key': [...]}."""
    st = (tuple(key["slot"]), tuple(key["mpos"]), key["n"], key["form"])
    return M().encipher(plaintext, st, key["order"], key["key"])


def worked_example(ctx, key):
    return "\n".join([
        "F1.4: one free alphabet under a hand key schedule, decided setting by setting.", "",
        "  setting      skip one key letter every 7 letters, 11 key letters",
        "  slot map     place 1 2 3 4 5 6 7 8 9 ...",
        "  key letter         1 2 3 4 5 6 8 9 10 ... (letter 7 skipped)", "",
        "  K4 gets one tempering search under that slot map; then scrambled copies that fit the same 24 checks",
        "  get one each, one at a time, until a copy reads as well as K4 (at most 12, or 100 if K4 keeps winning).",
        "  Chance alone lets K4 win all 12 in about 1 setting of 13."])
