"""Experiment 0273. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f14.2b-0272s-edge-cell-a25-on-2000-fresh-shuffles",
    "title": "F14.2b: 0272's edge cell (move then table, key length 25, settings with 4 or fewer informative checks) on K4 against 2,000 fresh shuffles",
    "family": "14-scheidt-mask-keyed-by-words",
    "parent": "0272-f14.2a-0271s-flawed-settings-decided-in-full",
    "changed": (
        "F14.2b, the chase of 0272's one edge cell. In 0272 the count-only class A25 Beaufort (order A: the move first, then the "
        "table; key length 25; 295 settings whose same-slot checks hold 4 or fewer between different known letters) gave K4 "
        "3,718,027 fitting alphabet pairs against a shuffle median of 0 and max 3,444,844 (p 0.02 of 76 cells, corrected line "
        "0.00066). Same settings, same exact test (0272's code, frozen), on K4 and 2,000 fresh shuffles (seed 2272, not 0271's), "
        "both forms; which setting carries K4's count, and how many of its checks are repeated-letter checks."
    ),
    "hypothesis_expert": (
        "F14 (C4(a), C5; 03-scheidt-said.md 'masked the English language', 'executed with the correct key word/s') with "
        "Sanborn's matrix step (C1(a)): a type-1 move of 0129's library, then a Quagmire IV table on two dictionary keyword "
        "alphabets (0244's 208,064), key length 25. At 4 or fewer informative checks the 24 known letters cannot pick an "
        "alphabet pair (4.3 x 10^10 / 26^c pairs fit by chance) and no dictionary word is 25 letters long, so 0271 and 0272 only "
        "counted pairs. A setting's count is non-zero only if its repeated-letter checks hold (two equal known letters in one key "
        "slot over equal carved letters), so the count measures how often K4's carved letters repeat where a move's slots put "
        "repeated known letters. Pre-registered: the primary statistic is K4's A25 Beaufort pair count, ranked among 2,000 "
        "fresh shuffles; it flags only at p below 0.05 / 76 = 0.00066 (0272's 76 cells). Secondary, reported: A25 added, and "
        "the number of A25 settings with any fit, both forms."
    ),
    "hypothesis_eli5": (
        "The last run found one small corner where the real carved text did a little better than all 50 scrambled copies: "
        "recipes with a key 25 letters long, where the known words give too few comparisons to pick the alphabets, so the run "
        "only counted how many alphabet pairs fit. One corner in 76 beating 50 copies happens by chance about once in a run. "
        "This run tests that corner alone against 2,000 new scrambled copies, enough to tell chance from a real signal."
    ),
    "prediction": (
        "K4's A25 Beaufort count is not unusual against 2,000 fresh shuffles: p above 0.00066 (expected near 0.02-0.05, the "
        "rate at which shuffles pass a setting's repeated-letter checks). Plants on these settings pass their own setting 12/12."
    ),
    "method": (
        "1. Settings: 0272's list restricted to order A, key length 25, 4 or fewer informative checks (295). "
        "2. Texts: K4 and 2,000 shuffles of it (seed 2272). "
        "3. Per text, setting and form: repeated-letter checks need equal carved letters; if they hold, the informative checks "
        "count the fitting pairs among 208,064 x 208,064 keyword alphabets exactly (0271's index, as 0272). "
        "4. Per text: total pairs and settings with a fit, per form. "
        "5. p = (1 + shuffles at or above K4) / 2,001. "
        "6. Plants: 12 English messages with the known words, enciphered on random settings of the 295 with two random "
        "dictionary keyword alphabets, a random 25-letter key and a random form; found if their own setting counts a fit "
        "and the true pair satisfies every check."
    ),
    "walkthrough": (
        "1. Take one recipe: a grid move, then the table, key length 25. "
        "2. Follow the 24 known letters to their carved places and key slots. "
        "3. Where two equal known letters (two E's) share a slot, their carved letters must be equal; if not, the recipe is out. "
        "4. Count the alphabet pairs that put every other pair of known letters in a shared slot the right distance apart. "
        "5. Do the same on 2,000 scrambled copies of the carved text. "
        "6. Count how many copies reach K4's total."
    ),
    "expected_minutes": 10,
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
SEED = 2272
N_COPIES = 2000
TEXTS_PER_JOB = 25
N_PLANTS = 12
N_CELLS = 76
_G = {}


def frozen():
    """0272's attack.py, unchanged (it loads 0271's)."""
    if "m" not in _G:
        import importlib.util
        path = next((ROOT / "experiments").glob("0272-*")) / "attack.py"
        spec = importlib.util.spec_from_file_location("frozen0272", path)
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


def cell_settings():
    m = frozen(); f = m.frozen()
    lib = f.routes()
    out = []
    for s in m.settings_list():
        if s[1] == "A" and s[2] == 25:
            pairs = f.checks_of(lib[s[0]][1], "A", 25)[0]
            if len(m.split_checks(pairs)[1]) < f.MIN_LIST:
                out.append(s)
    return out


def geo():
    """Per setting: land, repeated-letter checks, informative checks (built once in the parent, shared by fork)."""
    if "geo" not in _G:
        m = frozen(); f = m.frozen(); lib = f.routes()
        g = []
        for s in _G["settings"]:
            pairs, land, first = f.checks_of(lib[s[0]][1], "A", 25)
            eq, inf = m.split_checks(pairs)
            g.append((s, land, eq, inf))
        _G["geo"] = g
    return _G["geo"]


def count_texts(texts):
    """Every text over every cell setting: pairs per form and settings with a fit; index built only when a text needs it."""
    m = frozen()
    tix = [(tid, np.array([ord(c) - 65 for c in t])) for tid, t in texts]
    out = {tid: {"V": 0, "B": 0, "setV": 0, "setB": 0, "hits": []} for tid, _ in texts}
    for s, land, eq, inf in geo():
        live = [(tid, t[land]) for tid, t in tix if all(t[land][a] == t[land][b] for a, b in eq)]
        if not live:
            continue
        idx = {f: m.frozen().plain_index(inf, f) if inf else None for f in "VB"}
        for tid, cl in live:
            for form in "VB":
                n = m.fixed_fits(cl, eq, inf, idx[form], form)[0]
                out[tid][form] += n
                out[tid]["set" + form] += n > 0
                if n and tid == "k4":
                    out[tid]["hits"].append({"route": int(s[0]), "form": form, "pairs": int(n), "checks": len(eq) + len(inf),
                                             "repeated": len(eq), "informative": len(inf)})
    return out


def _job(args):
    b, texts = args
    t0 = time.time()
    return b, {"res": count_texts(texts), "secs": round(time.time() - t0, 1)}


def run(ctx):
    import json
    import multiprocessing as mp
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    m = frozen(); f = m.frozen()
    f.setup(ctx.vocabulary)
    lib = f.routes()
    k4 = ctx.K4
    k1 = json.loads((ROOT / "data" / "k1.json").read_text())
    pt1 = k1["plaintext"]; ct1 = k1["ciphertext"][:len(pt1)]
    key1 = {"route": -1, "o": "A", "L": 10, "form": "V", "pa": f.KRY, "ca": f.KRY, "ka": "kry", "word": "PALIMPSEST", "start": 0, "shift": 0}
    assert encrypt(pt1 + "A" * (N - len(pt1)), key1)[:len(pt1)] == ct1, "K1 self-check failed"
    _G["settings"] = cell_settings()
    geo()
    ctx.progress(0, 1, "settings listed")
    # 0272's own K4 count must be reproduced
    k4c = count_texts([("k4", k4)])["k4"]
    rec = json.loads((next((ROOT / "experiments").glob("0272-*")) / "result.json").read_text())["bounds"]["few_informative_counted"]
    assert k4c["B"] == rec["A25B"]["k4_pairs"] and k4c["V"] == rec["A25V"]["k4_pairs"], ("0272 not reproduced", k4c, rec["A25B"], rec["A25V"])
    rng = random.Random(SEED)
    texts = []
    for i in range(N_COPIES):
        s = list(k4); rng.shuffle(s); texts.append((f"copy{i}", "".join(s)))
    jobs = [(b, texts[a:a + TEXTS_PER_JOB]) for b, a in enumerate(range(0, N_COPIES, TEXTS_PER_JOB))]
    saved = getattr(ctx, "saved", {}) or {}
    res = {str(j[0]): saved[str(j[0])] for j in jobs if str(j[0]) in saved}
    todo = [j for j in jobs if str(j[0]) not in res]
    W = int(os.environ.get("K4_WORKERS", 8))
    ctx.progress(len(res), len(jobs), "shuffle blocks")
    with mp.get_context("fork").Pool(W) as pool:
        for b, out in pool.imap_unordered(_job, todo, chunksize=1):
            res[str(b)] = out
            ctx.save(str(b), out)
            ctx.progress(len(res), len(jobs), "shuffle blocks")
    cop = {}
    for v in res.values():
        cop.update(v["res"])
    assert len(cop) == N_COPIES

    def stat(key):
        kv = k4c[key]
        cv = np.array([cop[f"copy{i}"][key] for i in range(N_COPIES)])
        return {"k4": int(kv), "copies_nonzero": int((cv > 0).sum()), "copies_median": float(np.median(cv)),
                "copies_max": int(cv.max()), "at_or_above": int((cv >= kv).sum()),
                "p": round((1 + int((cv >= kv).sum())) / (N_COPIES + 1), 5)}
    st = {k: stat(k) for k in ("B", "V", "setB", "setV")}
    # plants
    prng = random.Random(SEED + 1)
    from kryptos.plants import english_plant
    A = f._G["A"]
    plants = []
    for _ in range(N_PLANTS):
        s = _G["settings"][prng.randrange(len(_G["settings"]))]
        key = {"route": s[0], "o": "A", "L": 25, "form": prng.choice("VB"), "pa": A[prng.randrange(2, len(A))],
               "ca": A[prng.randrange(2, len(A))], "ka": "std",
               "word": "".join(chr(65 + prng.randrange(26)) for _ in range(25)), "start": 0, "shift": 0}
        pt = english_plant(prng.randrange(10 ** 9))
        ct = encrypt(pt, key)
        assert decrypt(ct, key) == pt
        pairs, land, first = f.checks_of(lib[s[0]][1], "A", 25)
        eq, inf = m.split_checks(pairs)
        cl = np.array([ord(c) - 65 for c in ct])[land]
        n = m.fixed_fits(cl, eq, inf, f.plain_index(inf, key["form"]) if inf else None, key["form"])[0]
        ci, pi = A.index(key["ca"]), A.index(key["pa"])
        D, KL = f._G["D"], f._G["KL"]
        T = f._G["DN"] if key["form"] == "B" else D
        true_ok = all(D[cl[a] * 26 + cl[b]][ci] == T[KL[a] * 26 + KL[b]][pi] for a, b in pairs)
        plants.append({"route": lib[s[0]][0], "form": key["form"], "pairs_counted": int(n), "true_pair_fits": bool(true_ok),
                       "found": bool(n > 0 and true_ok)})
    hits = [{**h, "route_name": lib[h["route"]][0]} for h in k4c["hits"]]
    flag = st["B"]["p"] < 0.05 / N_CELLS
    bounds = {
        "item": "F14.2b", "cell": "order A (move then table), key length 25, 4 or fewer informative checks",
        "settings": len(_G["settings"]), "alphabets": f._G["NA"], "pairs_per_setting_and_form": f._G["NA"] ** 2,
        "texts": 1 + N_COPIES, "shuffle_seed": SEED, "exhaustive": True,
        "k4_reproduces_0272": True, "primary_A25_Beaufort_pairs": st["B"], "A25_added_pairs": st["V"],
        "settings_with_fit_Beaufort": st["setB"], "settings_with_fit_added": st["setV"],
        "corrected_line": round(0.05 / N_CELLS, 5), "flag": bool(flag), "k4_settings_with_fit": hits,
        "plants": plants, "plants_found": sum(p["found"] for p in plants), "plants_total": len(plants),
        "core_seconds": round(sum(v["secs"] for v in res.values())), "resumed_units": len(jobs) - len(todo),
        "cost_estimate": "295 settings x 2,001 texts, the index built only where repeated-letter checks hold: minutes on 32 cores, under $0.10",
    }
    notes = (f"F14.2b: A25 Beaufort pairs K4 {st['B']['k4']:,}, {st['B']['at_or_above']} of 2,000 fresh shuffles at or above "
             f"(p {st['B']['p']}; line {0.05 / N_CELLS:.5f}; flag {flag}); A25 added p {st['V']['p']}; settings with a fit "
             f"(Beaufort) K4 {st['setB']['k4']}, p {st['setB']['p']}. K4's fitting settings: {hits}. Plants {bounds['plants_found']}/{len(plants)}.")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def worked_example(ctx, key):
    return "\n".join([
        "F14.2b: one cell of 0272, against 2,000 fresh shuffles.", "",
        "  cell       a grid move, then the table, key length 25; 295 settings with 4 or fewer informative checks",
        "  repeats    two known E's in one key slot must sit over one carved letter, or the setting is out",
        "  count      the alphabet pairs that fit every other check, exactly, out of 208,064 x 208,064",
        "  verdict    K4's total ranked among the 2,000 shuffles' totals; a flag needs p below 0.05 / 76"])
