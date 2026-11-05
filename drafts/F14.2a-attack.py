"""Experiment 0272. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f14.2a-0271s-flawed-settings-decided-in-full",
    "title": "F14.2a: 0271's 41,986 settings where repeated known letters filled the first checks, decided in full (repeated-letter checks tested directly, the index on informative checks only), K4 against the same 50 shuffles, plants on those settings",
    "family": "14-scheidt-mask-keyed-by-words",
    "parent": "0271-f14.2-a-remembered-route-plus-two-dictionary-keyword-alphabets",
    "changed": (
        "F14.2a, the rerun of 0271's flaw. 0271 keyed its alphabet-pair index on the first six same-slot checks. A check whose two "
        "known letters are the same (E with E) has gap 0 on every plain alphabet, so it holds for every pair when the carved letters "
        "are equal and for none when they differ: it carries no information about the alphabets. Where three or more of the first six "
        "were such checks, the index keyed on three or fewer informative checks, more than LIST_CAP (2 million) pairs passed, and 0271 "
        "counted them without testing the remaining checks and never ran the key-word step. Here: repeated-letter checks are tested "
        "directly (equal carved letters, else no pair fits), the index is keyed on the first six informative checks, the rest are "
        "verified, then 0271's key-word step unchanged. Only the 41,986 affected settings (text-independent: the first six checks "
        "hold three or more repeats) are run; 0271's code is used unchanged for everything else, from its frozen attack.py."
    ),
    "hypothesis_expert": (
        "F14 (Scheidt's mask keyed by words; C4(a), C5; 03-scheidt-said.md 'masked the English language', 'executed with the correct "
        "key word/s') with Sanborn's matrix step (C1(a): 'I used a matrix code, and then... this [tableau]'): a type-1 move of 0129's "
        "library before or after a Quagmire IV table whose alphabets are dictionary keyword alphabets, keyed by a repeating word. "
        "0271 searched all 1,448,304 (move, order, key length) settings but, through the flaw above, left 41,986 of its 1,363,532 "
        "listed settings undecided; a true setting always passes its repeated-letter checks, so it is exactly where the flaw "
        "would hide the answer. These settings are decided here as 0271 decided the rest: pairs of the 208,064 alphabets (0244's "
        "list: 0109's dictionary keyword alphabets plus standard and KRYPTOS) fitting every check exactly; where 5 or more checks "
        "are informative (38,203 settings; chance pairs 4.3 x 10^10 / 26^c per form), every fitted pair's forced key matched "
        "against every rotation of every dictionary and puzzle word of the key's length, numbered on standard or KRYPTOS (or the "
        "pair's own alphabets when 20 or fewer fit), any shift; settings with 4 or fewer informative checks (3,783) counted only, as "
        "0271 counted its few-check settings. Prior attempts (reports/Kryptos K4 prior attempts database.md): a move with two "
        "dictionary keyword alphabets is not covered anywhere. Clue entries C1(a), C4(a), C5, C27(c)."
    ),
    "hypothesis_eli5": (
        "The last run tested about 1.4 million recipes: shuffle the message through a grid, then encipher it with a table whose two "
        "alphabets are scrambled by English words and a key word. A shortcut in the code skipped about 3 in 100 recipes: those where "
        "the first known letters to be compared were the same letter twice, which says nothing about the alphabets. The true recipe "
        "would always pass those comparisons, so it could have hidden there. This run tests exactly those recipes, comparing only "
        "the letters that say something, on K4 and the same 50 scrambled copies."
    ),
    "prediction": (
        "No key word on K4; K4's fitting-setting counts per (order, length, form) inside the 50 shuffles' range; K4's A10 setting "
        "(route 'two turns cw 17,95 inverse') fits no pair once its 11 informative checks are all tested; plants on these settings "
        "missed by 0271's code and found by this one. Zero candidates kept."
    ),
    "method": (
        "1. Settings: every (move, order, key length) of 0271 with 5 or more same-slot checks whose first six checks hold three or "
        "more with equal known letters: 41,986, the same for every text. "
        "2. Per text and setting: a repeated-letter check needs equal carved letters, else no pair fits; the informative checks "
        "(different known letters) are keyed into 0271's index (first six), the rest verified on the candidate pairs. "
        "3. Settings with 5+ informative checks: fitted pairs listed and 0271's key-word step run on them; 4 or fewer: pairs counted. "
        "4. Texts: K4 and 0271's 50 shuffles (seed 1420, the same texts). Plants: 12 English messages with the known words, "
        "enciphered on random settings of this list (5+ informative checks) with two random dictionary alphabets and a dictionary "
        "key word, 4 per length band 6-10, 11-18, 19-24 where the list has them; each searched with 0271's code and with this one. "
        "5. Self-checks: on 300 random unaffected settings the fixed test gives 0271's counts on K4 and two shuffles; K1 through "
        "the identity move. "
        "6. Verdict: K4's fitting settings and key-word matches per (order, length, form) ranked among the shuffles; key-word "
        "readings submitted as candidates."
    ),
    "walkthrough": (
        "1. Take one recipe: a grid move, before or after the table, and a key length. "
        "2. Follow the 24 known letters to their carved places and key slots. "
        "3. Two known letters in one slot that are the same letter (E and E) must sit over the same carved letter; if not, the "
        "recipe is out for every alphabet. "
        "4. Two different known letters in one slot must be as far apart on the plain alphabet as their carved letters are on the "
        "cipher alphabet: use only these to pair up the word-scrambled alphabets. "
        "5. For each pair that passes every comparison, read off the key and look for a word that gives it. "
        "6. Repeat for the 50 scrambled copies and compare."
    ),
    "expected_minutes": 30,
}

import os
import random
import sys
import time
import types
from pathlib import Path

import numpy as np

N = 97
ROOT = Path(__file__).resolve().parent
SEED = 1420
N_COPIES = 50
BLOCK = 300                   # settings per job
PLANT_BANDS = ((6, 10), (11, 18), (19, 24))
PLANTS_PER_BAND = 4
N_SELFCHECK = 300
_G = {}


def frozen():
    """0271's attack.py, unchanged."""
    if "m" not in _G:
        import importlib.util
        path = next((ROOT / "experiments").glob("0271-*")) / "attack.py"
        spec = importlib.util.spec_from_file_location("frozen0271", path)
        m = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = m
        spec.loader.exec_module(m)
        m.ROOT = ROOT
        _G["m"] = m
    return _G["m"]


def encrypt(plaintext, key):
    return frozen().encrypt(plaintext, key)


def decrypt(ct, key):
    return frozen().decrypt(ct, key)


def split_checks(pairs):
    """0271's checks split into repeated-letter checks (same known letter) and informative ones."""
    KL = frozen()._G["KL"]
    eq = [(a, b) for a, b in pairs if KL[a] == KL[b]]
    inf = [(a, b) for a, b in pairs if KL[a] != KL[b]]
    return eq, inf


def affected(pairs):
    """0271's flaw: three or more repeated-letter checks among the first KMAX, so the index keyed on 3 or fewer informative ones."""
    m = frozen()
    if len(pairs) < m.MIN_LIST:
        return False
    KL = m._G["KL"]
    return sum(KL[a] != KL[b] for a, b in pairs[:m.KMAX]) <= 3


def settings_list():
    m = frozen()
    lib = m.routes()
    out = []
    for r in range(len(lib)):
        for o in "AB":
            for L in range(1, m.LCOUNT + 1):
                pairs, land, first = m.checks_of(lib[r][1], o, L)
                if affected(pairs):
                    out.append((r, o, L))
    return out


def fixed_fits(cl, eq, inf, idx, form):
    """Every check tested: repeated-letter checks need equal carved letters; the index runs on informative checks."""
    m = frozen()
    for a, b in eq:
        if cl[a] != cl[b]:
            return 0, None, False
    if not inf:
        return m._G["NA"] ** 2, None, False
    k = min(len(inf), m.KMAX)
    ck = m.cipher_key(cl, inf, k)
    n, lst = m.fits(cl, inf, idx, ck, form)
    capped = len(inf) >= m.MIN_LIST and n > 0 and lst is None
    return n, lst, capped


def search(text, settings, cache, word_cache):
    m = frozen()
    lib = m.routes()
    tix = np.array([ord(c) - 65 for c in text])
    out = {"fits": {}, "settings_listed": {}, "settings_with_fit": {}, "few_settings": {}, "few_fits": {},
           "matches": [], "capped": 0}
    for s in settings:
        r, o, L = s
        if s not in cache:
            pairs, land, first = m.checks_of(lib[r][1], o, L)
            eq, inf = split_checks(pairs)
            cache[s] = (eq, inf, land, first, {f: m.plain_index(inf, f) if inf else None for f in "VB"})
        eq, inf, land, first, idx = cache[s]
        cl = tix[land]
        cover = sorted(first)
        for form in "VB":
            n, lst, capped = fixed_fits(cl, eq, inf, idx[form], form)
            c = f"{o}{L}{form}"
            out["fits"][c] = out["fits"].get(c, 0) + n
            out["capped"] += capped
            if len(inf) >= m.MIN_LIST:
                out["settings_listed"][c] = out["settings_listed"].get(c, 0) + 1
                out["settings_with_fit"][c] = out["settings_with_fit"].get(c, 0) + (n > 0)
                if lst is not None and n and L <= m.LMAX and len(cover) >= 3 and L in m._G["rots"]:
                    m.key_words(lst[0], lst[1], cl, first, cover, L, form, word_cache, text, s, out)
            else:
                out["few_settings"][c] = out["few_settings"].get(c, 0) + 1
                out["few_fits"][c] = out["few_fits"].get(c, 0) + n
    return out


def _job(args):
    b, settings, texts = args
    t0 = time.time()
    cache, word_cache = {}, {}
    res = {}
    for tid, text in texts:
        o = search(text, settings, cache, word_cache)
        o["n_matches"] = len(o["matches"])
        o["matches"] = o["matches"][:200]
        res[tid] = o
        if len(word_cache) > 200:
            word_cache.clear()
    return b, {"res": res, "secs": round(time.time() - t0, 1)}


def make_plants(rng, settings):
    from kryptos.plants import english_plant
    m = frozen()
    A, lib = m._G["A"], m.routes()
    plants = []
    for lo, hi in PLANT_BANDS:
        pool = []
        for s in settings:
            if lo <= s[2] <= hi and s[2] in m._G["rots"]:
                pairs, land, first = m.checks_of(lib[s[0]][1], s[1], s[2])
                if len(split_checks(pairs)[1]) >= m.MIN_LIST and len(first) >= 3:
                    pool.append(s)
        for _ in range(min(PLANTS_PER_BAND, len(pool))):
            r, o, L = pool[rng.randrange(len(pool))]
            strs, src = m._G["rots"][L]
            w = src[rng.randrange(len(src))]
            key = {"route": r, "o": o, "L": L, "form": rng.choice("VB"), "pa": A[rng.randrange(2, len(A))],
                   "ca": A[rng.randrange(2, len(A))], "ka": rng.choice(("std", "kry")), "word": w[0], "start": w[1],
                   "shift": rng.randrange(26)}
            pt = english_plant(rng.randrange(10 ** 9))
            pc = encrypt(pt, key)
            assert decrypt(pc, key) == pt
            plants.append({"key": key, "pt": pt, "ct": pc})
    return plants


def run(ctx):
    import json
    import multiprocessing as mp
    t_start = time.time()
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    m = frozen()
    m.setup(ctx.vocabulary)
    lib = m.routes()
    k4 = ctx.K4
    # K1 through the identity move
    k1 = json.loads((ROOT / "data" / "k1.json").read_text())
    pt1 = k1["plaintext"]; ct1 = k1["ciphertext"][:len(pt1)]
    key1 = {"route": -1, "o": "A", "L": 10, "form": "V", "pa": m.KRY, "ca": m.KRY, "ka": "kry", "word": "PALIMPSEST", "start": 0, "shift": 0}
    assert encrypt(pt1 + "A" * (N - len(pt1)), key1)[:len(pt1)] == ct1, "K1 self-check failed"
    # the same texts as 0271
    rng = random.Random(SEED)
    texts = [("k4", k4)]
    for i in range(N_COPIES):
        s = list(k4); rng.shuffle(s); texts.append((f"copy{i}", "".join(s)))
    settings = settings_list()
    ctx.progress(0, 1, "settings listed")
    sset = set(settings)
    prng = random.Random(SEED + 1)
    # self-check: unaffected listed settings give 0271's counts
    unaff = []
    while len(unaff) < N_SELFCHECK:
        s = (prng.randrange(len(lib)), prng.choice("AB"), prng.randint(1, m.LCOUNT))
        if s in sset:
            continue
        pairs = m.checks_of(lib[s[0]][1], s[1], s[2])[0]
        if len(pairs) >= m.MIN_LIST:
            unaff.append(s)
    sc_ok, sc_n = 0, 0
    for tid, text in texts[:3]:
        tix = np.array([ord(c) - 65 for c in text])
        for s in unaff:
            pairs, land, first = m.checks_of(lib[s[0]][1], s[1], s[2])
            cl = tix[land]
            eq, inf = split_checks(pairs)
            for form in "VB":
                old = m.fits(cl, pairs, m.plain_index(pairs, form), m.cipher_key(cl, pairs, min(len(pairs), m.KMAX)), form)[0]
                new = fixed_fits(cl, eq, inf, m.plain_index(inf, form) if inf else None, form)[0]
                sc_n += 1; sc_ok += old == new
    assert sc_ok == sc_n, f"self-check: {sc_ok}/{sc_n} unaffected settings agree with 0271"
    # K4's A10 setting in 0271
    a10 = {}
    tk4 = np.array([ord(c) - 65 for c in k4])
    for s in settings:
        if s[1] == "A" and s[2] == 10:
            pairs, land, first = m.checks_of(lib[s[0]][1], "A", 10)
            cl = tk4[land]
            eq, inf = split_checks(pairs)
            if any(cl[a] != cl[b] for a, b in eq):
                continue
            for form in "VB":
                old = m.fits(cl, pairs, m.plain_index(pairs, form), m.cipher_key(cl, pairs, min(len(pairs), m.KMAX)), form)[0]
                if old:
                    new = fixed_fits(cl, eq, inf, m.plain_index(inf, form), form)[0]
                    a10[f"{lib[s[0]][0]}/{form}"] = {"checks": len(pairs), "informative": len(inf), "0271_count": old, "fixed_count": new}
    # plants: 0271's code and the fixed one, each at the plant's own setting
    plants = make_plants(prng, settings)
    pfound = []
    for p in plants:
        k = p["key"]
        s = (k["route"], k["o"], k["L"])
        pairs, land, first = m.checks_of(lib[k["route"]][1], k["o"], k["L"])
        pc = {s: (pairs, land, first, {f: m.plain_index(pairs, f) for f in "VB"})}
        old = m.search_settings(p["ct"], [s], pc, {})
        new = search(p["ct"], [s], {}, {})

        def hit(out):
            return any(x["pa"] == k["pa"] and x["ca"] == k["ca"] and x["form"] == k["form"] and decrypt(p["ct"], x) == p["pt"]
                       for x in out["matches"])
        pfound.append({"L": k["L"], "o": k["o"], "route": lib[k["route"]][0], "checks": len(pairs),
                       "informative": len(split_checks(pairs)[1]), "found_0271": hit(old), "found": hit(new)})
    # the main search
    jobs = [(b, settings[a:a + BLOCK], texts) for b, a in enumerate(range(0, len(settings), BLOCK))]
    saved = getattr(ctx, "saved", {}) or {}
    res = {str(j[0]): saved[str(j[0])] for j in jobs if str(j[0]) in saved}
    todo = [j for j in jobs if str(j[0]) not in res]
    W = int(os.environ.get("K4_WORKERS", 8))
    ctx.progress(len(res), len(jobs), "setting blocks")
    with mp.get_context("fork").Pool(W) as pool:
        for b, out in pool.imap_unordered(_job, todo, chunksize=1):
            res[str(b)] = out
            ctx.save(str(b), out)
            ctx.progress(len(res), len(jobs), "setting blocks")
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
        return (c[0], int(c[1:-1]), c[-1])
    table = {}
    for c in sorted({c for t in tot.values() for c in t["settings_listed"]}, key=order):
        kv = tot["k4"]["settings_with_fit"].get(c, 0)
        cv = [tot[f"copy{i}"]["settings_with_fit"].get(c, 0) for i in range(N_COPIES)]
        table[c] = {"settings": tot["k4"]["settings_listed"].get(c, 0), "k4_settings_with_fit": kv,
                    "copies_median": float(np.median(cv)), "copies_max": max(cv),
                    "p_at_or_above": round((1 + sum(x >= kv for x in cv)) / (N_COPIES + 1), 3)}
    few = {}
    for c in sorted({c for t in tot.values() for c in t["few_settings"]}, key=order):
        kv = tot["k4"]["few_fits"].get(c, 0)
        cv = [tot[f"copy{i}"]["few_fits"].get(c, 0) for i in range(N_COPIES)]
        few[c] = {"settings": tot["k4"]["few_settings"].get(c, 0), "k4_pairs": kv, "copies_median": float(np.median(cv)),
                  "copies_max": max(cv), "p_at_or_above": round((1 + sum(x >= kv for x in cv)) / (N_COPIES + 1), 3)}
    km = tot["k4"]["n_matches"]
    cm = [tot[f"copy{i}"]["n_matches"] for i in range(N_COPIES)]
    from kryptos.scorer import free_text
    cands = []
    for x in tot["k4"]["matches"][:200]:
        pt = decrypt(k4, x)
        cands.append({"plaintext": pt, "key": x, "_score": ctx.english_score(free_text(pt))})
    cands.sort(key=lambda x: -x["_score"])
    controls = []
    for i in range(N_COPIES):
        sc = [ctx.english_score(free_text(decrypt(texts[1 + i][1], x))) for x in tot[f"copy{i}"]["matches"][:100]]
        if sc:
            controls.append(max(sc))
    minp = min((v["p_at_or_above"] for v in table.values() if v["k4_settings_with_fit"] > 0), default=None)
    n_inf5 = sum(v["settings"] for v in table.values()) // 2
    bounds = {
        "item": "F14.2a", "settings": len(settings), "settings_5plus_informative": n_inf5,
        "settings_4_or_fewer_informative": len(settings) - n_inf5,
        "of_0271_listed": 1363532, "routes": len(lib), "alphabets": m._G["NA"], "forms": ["added", "Beaufort"],
        "key_word_lengths": [1, m.LMAX],
        "key_numbering": "standard or KRYPTOS (and the pair's own alphabets when 20 or fewer pairs fit), any shift",
        "selfcheck_unaffected_settings_agree": f"{sc_ok}/{sc_n}", "k4_a10_setting_0271_vs_fixed": a10,
        "per_class": table, "few_informative_counted": few, "smallest_class_p": minp, "classes": len(table),
        "capped_settings": {"k4": tot["k4"]["capped"], "copies_max": max(tot[f"copy{i}"]["capped"] for i in range(N_COPIES))},
        "key_word_matches": {"k4": km, "copies_median": float(np.median(cm)), "copies_max": max(cm),
                             "p_at_or_above": round((1 + sum(x >= km for x in cm)) / (N_COPIES + 1), 3)},
        "k4_best_readings": [[round(c["_score"], 3), c["plaintext"], c["key"]] for c in cands[:10]],
        "plants": pfound, "plants_found": sum(p["found"] for p in pfound), "plants_found_by_0271": sum(p["found_0271"] for p in pfound),
        "plants_total": len(pfound), "texts": len(texts), "exhaustive": True,
        "core_seconds": round(sum(v["secs"] for v in res.values())), "compute_seconds": round(time.time() - t_start),
        "resumed_units": len(jobs) - len(todo),
        "cost_estimate": "41,986 settings x 51 texts at 0271's rate (about 0.008 core-s per setting and text) plus one index per setting: about 5-6 core-hours; AWS 32 cores about 15 min, under $0.30",
    }
    notes = (f"F14.2a: 0271's {len(settings):,} flawed settings decided in full ({n_inf5:,} with 5+ informative checks); key-word matches "
             f"K4 {km}, copies median {np.median(cm)}, max {max(cm)}; smallest per-class p {minp} over {len(table)} classes; "
             f"plants found {bounds['plants_found']}/{len(pfound)} (0271's code: {bounds['plants_found_by_0271']}); K4's A10 setting: {a10}.")
    out = {"candidates": [{"plaintext": c["plaintext"], "key": c["key"]} for c in cands], "bounds": bounds, "notes": notes}
    if len(controls) >= 10:
        out["controls"] = controls
    return out


def worked_example(ctx, key):
    return "\n".join([
        "F14.2a: 0271's flawed settings, every check tested.", "",
        "  setting    a grid move, before or after the table, and a key length (41,986 of them)",
        "  repeats    two known E's in one key slot must sit over one carved letter; that holds for every alphabet or none",
        "  index      only checks between different known letters pair up the word-scrambled alphabets",
        "  key word   each fitting pair forces the key; a word of the key's length must give it",
        "  0271 keyed on the first six checks, repeats included: three repeats left too few, and it counted instead of testing."])
