"""Experiment: F16.1a. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f16.1a-one-free-alphabet-on-the-20-official-letters",
    "title": "F16.1a: one alphabet in an unknown order on both sides of the table, a repeating key of length 1-26, decided exactly on the 20 official known letters (EAST at 22-25 set aside), with up to two slips; K4 against 200 shuffles, with planted messages",
    "family": "16-simple-hand-methods",
    "parent": "0208-one-free-alphabet-with-slips-at-known-places",
    "changed": (
        "F16.1 (issue #123), first part: 0119's and 0208's exact decider, imported unchanged from 0208's attack.py, run "
        "on the 20 letters Sanborn released himself (NORTHEAST 26-34, BERLIN 64-69, CLOCK 70-74). EAST (22-25) is "
        "second-hand (#124) and every exact test so far required it. Drop sets of 0-2 of the 20 places; K4 against 200 "
        "shuffles (0208: 20); the same decider on K4's 24 letters in the same run, to list the cells only EAST closed."
    ),
    "hypothesis_expert": (
        "F1 (one keyed stage, no move), C27(c) and C27(a) as in 0208; criteria revised 2026-11-17 (#124): EAST was "
        "confirmed privately in 2020 and reported second-hand, the other 20 letters are Sanborn's own published clues "
        "(01-facts.md, 'The four clues'). Model as 0119: one unknown bijection A from letters to Z26 used on the plain "
        "and the cipher side (Quagmire III, the K1/K2 system with the alphabet free); key k of length L 1-26; form V: "
        "A(c_i) = A(p_i) + k[i mod L]; form B: A(c_i) = k[i mod L] - A(p_i). The constraint: the 20 equations at 26-34 "
        "and 64-74, with any 0, 1 or 2 of them dropped as slips (A1), decided exactly by 0119's decide() (CRT mod 13 x "
        "mod 2, enumeration or pruned search, witness re-checked). 20 letters give about 94 bits of checks against a "
        "key of L x 4.7 bits plus an alphabet of 88 bits, so fits are expected to begin near L = 1-2 shorter than "
        "with 24 letters; the question is whether K4 fits more, or shorter, than its shuffles."
    ),
    "hypothesis_eli5": (
        "Every exact test so far needed all 24 known letters, including EAST, which Sanborn confirmed only in a private "
        "email that others passed on. If EAST were wrong, those tests could have thrown the answer away. Here we repeat "
        "the test for the K1/K2 kind of cipher, with the alphabet in any order and any repeating key, using only the 20 "
        "letters Sanborn published himself, and allowing up to two of them to be carved wrong. We do the same on 200 "
        "scrambled copies of the carving, to see whether the carving fits more often than chance."
    ),
    "prediction": (
        "K4 fits at more cells than with 24 letters (with 24, at no slip only B23 and B26), but its counts sit inside the "
        "200 shuffles on all five pre-registered statistics (p above 0.01 each): the shortest fitting length per form at "
        "no slip, and the number of fitting cells at 0, at most 1 and at most 2 slips. Plants at lengths 7 and 11-12 are "
        "found (their planted slips fit and their count beats their own 20 copies); the long plant at 20 is not "
        "(the reach). Zero candidates: a free alphabet leaves the reading undetermined."
    ),
    "method": (
        "1. For each text, key length L 1-26 and form V or B: the 20 equations (slot, known letter, carved letter) at "
        "26-34 and 64-74. 2. Decide with no drop, then every drop set of 1 and 2 places, skipping supersets of a set "
        "that already fits. 3. Count minimal fitting sets by size. 4. K4 and 200 shuffles; K4 also on all 24 letters, "
        "to list cells only EAST closed. 5. Six planted messages (free alphabet, known key, 0-2 slips at official "
        "places), each against 20 shuffles of its own ciphertext. 6. Five pre-registered statistics, one-sided "
        "empirical p against the shuffles, Bonferroni at 0.05/5 = 0.01."
    ),
    "walkthrough": (
        "1. Write K4 and mark only the 20 places of NORTHEAST, BERLIN and CLOCK; leave 22-25 unmarked. "
        "2. Choose a key length, say 11, and give each marked place its slot: place minus 1, mod 11. "
        "3. For each marked place write one line: the carved letter's place in the secret alphabet equals the key value of its slot minus the known letter's place (the Beaufort form). "
        "4. Try to give every letter a different place in the alphabet and every slot a key value so all 20 lines hold, backing up when two letters would need the same place. "
        "5. If an assignment holds every line, length 11 fits; if every branch backs up, it does not. "
        "6. Cross out one or two lines as slips and try again. "
        "7. Do the same on scrambled copies of K4 and compare how often each fits."
    ),
    "expected_minutes": 20,
}

import itertools
import math
import multiprocessing as mp
import os
import random
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STD = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LMAX = 26
FORMS = ("V", "B")
KMAX = 2
N_COPIES = 200
N_PLANT_COPIES = 20
SEED = 16100
OFFICIAL = tuple(range(26, 35)) + tuple(range(64, 75))
PLANTS = [(16101, 7, "V", 0), (16102, 7, "B", 1), (16103, 11, "B", 2), (16104, 12, "V", 2),
          (16105, 16, "V", 1), (16106, 20, "B", 0)]
_G = {}


def frozen():
    """0208's attack.py, unchanged (its decide() is 0119's)."""
    if "m" not in _G:
        import importlib.util
        path = next((ROOT / "experiments").glob("0208-*")) / "attack.py"
        spec = importlib.util.spec_from_file_location("frozen0208", path)
        m = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = m
        spec.loader.exec_module(m)
        _G["m"] = m
    return _G["m"]


def known20(known):
    return {q: known[q] for q in OFFICIAL}


def cell(args):
    """Minimal fitting drop sets (tuples of known places) for one text, length and form, on the given known places."""
    text, known, L, form = args
    m = frozen()
    Q = sorted(known)
    eqs = m.equations(text, known, L)
    fits, und = [], []
    for k in range(KMAX + 1):
        for D in itertools.combinations(range(len(Q)), k):
            Ds = set(D)
            if any(set(F) <= Ds for F in fits):
                continue
            e = [x for i, x in enumerate(eqs) if i not in Ds]
            st, w = m.decide(e, form)
            if st == "fit":
                assert m.check_witness(e, form, w)
                fits.append(D)
            elif st == "undecided":
                und.append(D)
    return {"fits": [[Q[i] for i in D] for D in fits], "undecided": [[Q[i] for i in D] for D in und]}


def text_job(args):
    """Every (L, form) cell for one text: {cell: by_k counts, plus K4's sets}."""
    name, text, known, keep_sets = args
    out = {}
    for L in range(1, LMAX + 1):
        for form in FORMS:
            r = cell((text, known, L, form))
            c = [0] * (KMAX + 1)
            for D in r["fits"]:
                c[len(D)] += 1
            out[f"{form}{L}"] = {"c": c, "u": len(r["undecided"])}
            if keep_sets:
                out[f"{form}{L}"]["sets"] = r["fits"]
    return name, out


def shuffled(text, seed):
    l_ = list(text)
    random.Random(seed).shuffle(l_)
    return "".join(l_)


def make_plant(seed, L, form, k, known):
    from kryptos.plants import english_plant
    rng = random.Random(seed)
    pt = english_plant(seed)
    order = list(range(26)); rng.shuffle(order)
    inv = {v: i for i, v in enumerate(order)}
    key = [rng.randrange(26) for _ in range(L)]
    sgn = 1 if form == "V" else -1
    ct = [chr(65 + inv[(sgn * order[ord(p) - 65] + key[i % L]) % 26]) for i, p in enumerate(pt)]
    slots = {}
    for q in OFFICIAL:
        slots.setdefault((q - 1) % L, []).append(q)
    checked = [s for s, qs in slots.items() if len(qs) >= 2]
    rng.shuffle(checked)
    places = sorted(rng.choice(slots[s]) for s in checked[:k])
    for q in places:
        ct[q - 1] = rng.choice([c for c in STD if c != ct[q - 1]])
    alpha = "".join(sorted(STD, key=lambda c: order[ord(c) - 65]))
    return pt, "".join(ct), alpha, key, places


def run(ctx):
    me = sys.modules.get(__name__)
    if getattr(me, "text_job", None) is not text_job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    m = frozen()
    K4 = ctx.K4
    k24 = dict(ctx.KNOWN)
    k20 = known20(k24)
    assert len(k20) == 20 and len(k24) == 24
    # 0208 reproduced: K4's minimal fitting sets on 24 letters at length 7, form V, none; B23 fits with no slip
    assert m.decide(m.equations(K4, k24, 23), "B")[0] == "fit"
    assert m.decide(m.equations(K4, k24, 7), "V")[0] == "dead"
    jobs = [("k4_20", K4, k20, True), ("k4_24", K4, k24, True)]
    jobs += [(f"copy{i}", shuffled(K4, SEED + i), k20, False) for i in range(N_COPIES)]
    plants = []
    for seed, L, form, k in PLANTS:
        pt, ct, alpha, key, places = make_plant(seed, L, form, k, k24)
        plants.append({"seed": seed, "L": L, "form": form, "k": k, "ct": ct, "alpha": alpha, "key": key, "slips": places})
        jobs.append((f"plant{seed}", ct, k20, True))
        jobs += [(f"plant{seed}_c{i}", shuffled(ct, seed * 100 + i), k20, False) for i in range(N_PLANT_COPIES)]
    saved = getattr(ctx, "saved", {}) or {}
    res = {j[0]: saved[j[0]] for j in jobs if j[0] in saved}
    todo = [j for j in jobs if j[0] not in res]
    W = int(os.environ.get("K4_WORKERS", 8))
    ctx.progress(len(res), len(jobs), "texts")
    with mp.get_context("fork").Pool(W) as pool:
        for name, out in pool.imap_unordered(text_job, todo, chunksize=1):
            res[name] = out
            ctx.save(name, out)
            ctx.progress(len(res), len(jobs), "texts")

    cells = [f"{f}{L}" for L in range(1, LMAX + 1) for f in FORMS]

    def stats(r):
        s = {}
        for f in FORMS:
            s[f"shortest_{f}_k0"] = next((L for L in range(1, LMAX + 1) if r[f"{f}{L}"]["c"][0]), 99)
        for k in range(KMAX + 1):
            s[f"cells_fit_k{k}"] = sum(1 for c in cells if sum(r[c]["c"][:k + 1]))
        return s

    k4s = stats(res["k4_20"])
    cps = [stats(res[f"copy{i}"]) for i in range(N_COPIES)]
    prereg = {}
    for key_, v in k4s.items():
        if key_.startswith("shortest"):
            n = sum(1 for c in cps if c[key_] <= v)          # K4 short is the interesting side
        else:
            n = sum(1 for c in cps if c[key_] >= v)          # K4 fitting more is the interesting side
        prereg[key_] = {"k4": v, "copies_min": min(c[key_] for c in cps), "copies_median": sorted(c[key_] for c in cps)[N_COPIES // 2],
                        "copies_max": max(c[key_] for c in cps), "copies_as_extreme": n, "p": round((1 + n) / (N_COPIES + 1), 4),
                        "flag": (1 + n) / (N_COPIES + 1) < 0.01}
    per_cell = {}
    only_east = []
    for c in cells:
        a, b = res["k4_20"][c], res["k4_24"][c]
        cop = [res[f"copy{i}"][c]["c"] for i in range(N_COPIES)]
        per_cell[c] = {"k4_20": a["c"], "k4_24": b["c"], "k4_20_sets": a["sets"][:30],
                       "copies_fitting_at_k_or_less": [sum(1 for x in cop if sum(x[:k + 1])) for k in range(KMAX + 1)],
                       "undecided_k4": a["u"], "undecided_copies": sum(res[f"copy{i}"][c]["u"] for i in range(N_COPIES))}
        for k in range(KMAX + 1):
            if sum(a["c"][:k + 1]) and not sum(b["c"][:k + 1]):
                only_east.append({"cell": c, "k": k, "k4_minimal_sets": [D for D in a["sets"] if len(D) <= k][:10],
                                  "copies_fitting_at_k_or_less": per_cell[c]["copies_fitting_at_k_or_less"][k]})
                break
    plant_out = []
    for p in plants:
        r = res[f"plant{p['seed']}"][f"{p['form']}{p['L']}"]
        own = [res[f"plant{p['seed']}_c{i}"][f"{p['form']}{p['L']}"]["c"] for i in range(N_PLANT_COPIES)]
        fit = any(set(D) <= set(p["slips"]) for D in r["sets"])
        tot = sum(r["c"][:p["k"] + 1])
        own_tot = [sum(o[:p["k"] + 1]) for o in own]
        plant_out.append({"seed": p["seed"], "L": p["L"], "form": p["form"], "k": p["k"], "slips": p["slips"],
                          "planted_slips_fit": fit, "count_at_k": tot, "own_copies_fitting_at_k": sum(1 for x in own_tot if x),
                          "own_copies_max": max(own_tot), "found": bool(fit and tot > max(own_tot))})
    flagged = [k for k, v in prereg.items() if v["flag"]]
    und_total = sum(v["u"] for r in res.values() for v in r.values())
    return {
        "candidates": [],
        "bounds": {
            "family": "one unknown alphabet on both sides (Quagmire III), periodic key 1-26, forms V and B, on the 20 official known letters (26-34, 64-74), 0-2 slips (F16.1a)",
            "known_places": list(OFFICIAL), "key_lengths": [1, LMAX], "slips": [0, KMAX],
            "drop_sets": "every set of 0-2 of the 20 places (211 per cell), supersets of a fitting set skipped; 0119's decide() via 0208's attack.py unchanged",
            "slip_cost_bits": {k: round(4.7 * k + math.log2(math.comb(20, k)), 1) for k in (1, 2)},
            "preregistered": prereg, "flagged": flagged,
            "cells": per_cell,
            "only_east_closed": only_east,
            "plants": plant_out,
            "undecided_drop_sets_total": und_total,
            "controls": f"{N_COPIES} shuffles of K4 (seeds {SEED}-{SEED + N_COPIES - 1}); each plant against {N_PLANT_COPIES} shuffles of its own ciphertext",
            "exhaustive": "yes: exact per drop set; undecided sets counted",
            "judge": "not called: where a free alphabet fits, the alphabet and so the reading are undetermined",
            "modal_cost_estimate_dollars": 0,
            "aws_cost_estimate_dollars": 0.2,
        },
        "notes": (f"pre-registered flags {flagged or 'none'}; K4 {k4s}; cells only EAST closed: "
                  f"{[(o['cell'], o['k']) for o in only_east]}; plants found {[p['found'] for p in plant_out]}; undecided {und_total}"),
    }


def encrypt(plaintext, key):
    """Quagmire III with slips: key = {alphabet, shifts, form, slips [[place, carved letter]]}."""
    alpha, shifts, form = key["alphabet"], key["shifts"], key.get("form", "V")
    pos = {ch: i for i, ch in enumerate(alpha)}
    sgn = 1 if form == "V" else -1
    out = [alpha[(sgn * pos[ch] + shifts[i % len(shifts)]) % 26] for i, ch in enumerate(plaintext)]
    for q, ch in key.get("slips", []):
        out[q - 1] = ch
    return "".join(out)


def worked_example(ctx, key):
    m = frozen()
    k20 = known20(ctx.KNOWN)
    lines = ["Beaufort form: A(carved) = k[slot] - A(known), on the 20 official letters", ""]
    for L in (7, 11, 23):
        a = m.decide(m.equations(ctx.K4, k20, L), "B")[0]
        b = m.decide(m.equations(ctx.K4, ctx.KNOWN, L), "B")[0]
        lines.append(f"  length {L:2d}: 20 letters {a:4s}   24 letters {b}")
    lines.append("")
    lines.append("(With EAST set aside, fewer lines must hold, so more lengths fit; the shuffles say whether K4 fits more than chance.)")
    return "\n".join(lines)
