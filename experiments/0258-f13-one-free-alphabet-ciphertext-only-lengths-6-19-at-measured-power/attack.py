"""Experiment 0258. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f13-one-free-alphabet-ciphertext-only-lengths-6-19-at-measured-power",
    "title": "F13.4c at key lengths 6-19 (D3): one free alphabet with a periodic key, ciphertext only, K4 against 100 fresh shuffles climbed by 0236's frozen search, closed at the measured power",
    "family": "13-ciphertext-only",
    "parent": "0236-f13-one-free-alphabet-ciphertext-only",
    "changed": (
        "D3 (issue #77, Alexis #100: run power-blocked cells at their measured power). 0236 measured its search's power at "
        "6-19 (plants 2-5 of 8) and climbed K4 there, but decided and recorded K4 only at 1-5, where power was 7-8 of 8. "
        "Here 0236's per-text search, unchanged (imported from its record), on K4 and 100 fresh shuffles at every length "
        "6-19 in both forms, every cell recorded; plants at 6, 7, 8, 10, 13, 16, 19 redrawn in the same run (8 each, 6 own copies)."
    ),
    "hypothesis_expert": (
        "F13.4c: a periodic key on one free alphabet (Quagmire III with an unknown order, both forms), solved from the "
        "ciphertext alone: the search never reads the 24 known letters (program.md, F13); gate 2 checks them at keep time. "
        "0236's design-2 tempering without known letters, 3 runs x 16 replicas x 625 rounds x 1000 moves, MIX8m rescoring "
        "(0233). F13.1 puts one free alphabet with a key within reach of 97 letters to length 19 by quadgrams; 0236 found "
        "the search's power falls from 7/8 at 5 to 2-5/8 at 6-19. Statistic: per cell, K4's MIX8m against the shuffles' "
        "(z); over the 28 cells the largest z against the shuffles' own largest z. Clue entries C27(c), C5(a)."
    ),
    "hypothesis_eli5": (
        "Suppose Sanborn used the cipher table with his own scrambled alphabet and a repeating key of 6 to 19 letters, and "
        "suppose we did not know any of the words he gave away. Our search can still find such messages sometimes, two to "
        "five times in eight. We run it on K4 and on 100 scrambled copies of K4 and ask whether K4 reads better than the "
        "copies. Only after that do we look at whether the known words came out in place."
    ),
    "prediction": (
        "K4 inside its shuffles: largest z over the 28 cells with p above 0.05; no cell where K4 beats all 100. Plant power "
        "as 0236 (2-5 of 8 at 6-19). K4's readings put at most 5 of the 24 known letters in place (harness gate 2)."
    ),
    "method": (
        "1. Texts: K4 and 100 shuffles of K4 (seed 2560). "
        "2. Each text at every key length 6-19 and both forms (Beaufort, added): 0236's climb(), unchanged. "
        "3. Plants: 8 per length at 6, 7, 8, 10, 13, 16, 19 (0236's rule: Carter test windows, half with X stops, a random "
        "alphabet and key, forms alternating), 6 own shuffles each; found when above all its own copies. "
        "4. Per cell: K4's rank among the 100 and its z; the statistic is the largest z, its p from the shuffles' own largest z."
    ),
    "walkthrough": (
        "1. Write a scrambled alphabet and a key of, say, 11 numbers. "
        "2. To read the ciphertext, take each letter's place in the alphabet, subtract the key number for that position "
        "(Beaufort: subtract the place from the key), and read the alphabet at the result. "
        "3. A computer searches alphabets and keys for the most English-looking reading of K4, without looking at the known words. "
        "4. The same search runs on 100 scrambled copies of K4. "
        "5. K4 counts only if it reads better than every copy; then the 24 known letters are checked."
    ),
    "expected_minutes": 30,
}

import importlib.util
import os
import random
import sys
import time
import types
from pathlib import Path

import numpy as np

N = 97
ROOT = Path(__file__).resolve().parent
LENGTHS = range(6, 20)
PLANT_LENGTHS = (6, 7, 8, 10, 13, 16, 19)
PLANTS, OWN = 8, 6
N_COPIES = 100
SEED = 2560
_MODS = {}


def M():
    if "m" not in _MODS:
        path = next((ROOT / "experiments").glob("0236-*")) / "attack.py"
        spec = importlib.util.spec_from_file_location("frozen0236", path)
        m = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = m
        spec.loader.exec_module(m)
        m.ROOT = ROOT
        _MODS["m"] = m
    return _MODS["m"]


def _job(args):
    key, text, L, form, seed = args
    return key, list(M().climb(text, L, form, seed))


def run(ctx):
    import multiprocessing as mp
    t0 = time.time()
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    m = M()
    m.lib(); m.models()
    rng = random.Random(SEED)
    C = m._G["corpus"]
    jobs, plants = [], {}
    for L in PLANT_LENGTHS:
        for j in range(PLANTS):
            src = C["test"] if j % 2 == 0 else C["test_xs"]
            o = rng.randrange(0, len(src) - N)
            pt = src[o:o + N]
            a = list(m.STD); rng.shuffle(a); a = "".join(a)
            form = m.FORMS[(j // 2) % 2]
            key = {"alphabet": a, "form": form, "shifts": [rng.randrange(26) for _ in range(L)]}
            pc = m.encrypt(pt, key)
            pid = f"plant{L}_{j}"
            plants[pid] = {"L": L, "form": form, "pt": pt}
            jobs.append((f"{pid}|{L}|{form}", pc, L, form, rng.randrange(10 ** 9)))
            for g in range(OWN):
                s = list(pc); rng.shuffle(s)
                jobs.append((f"{pid}_own{g}|{L}|{form}", "".join(s), L, form, rng.randrange(10 ** 9)))
    k4 = ctx.K4
    texts = [("k4", k4)] + [(f"copy{i}", "".join(rng.sample(k4, N))) for i in range(N_COPIES)]
    for tid, t in texts:
        for L in LENGTHS:
            for form in m.FORMS:
                jobs.append((f"{tid}|{L}|{form}", t, L, form, rng.randrange(10 ** 9)))
    saved = getattr(ctx, "saved", {}) or {}
    res = {j[0]: saved[j[0]] for j in jobs if j[0] in saved}        # units an earlier run of this attack.py finished (#105)
    todo = [j for j in jobs if j[0] not in res]
    W = int(os.environ.get("K4_WORKERS", 8))
    ctx.progress(len(res), len(jobs), "climbs")
    with mp.get_context("fork").Pool(W) as pool:
        for key, out in pool.imap_unordered(_job, todo, chunksize=1):
            res[key] = out
            ctx.save(key, out)
            ctx.progress(len(res), len(jobs), "climbs")
    power, letters = {}, {}
    for L in PLANT_LENGTHS:
        f, lr = 0, []
        for j in range(PLANTS):
            pid = f"plant{L}_{j}"; form = plants[pid]["form"]
            s = res[f"{pid}|{L}|{form}"][0]
            f += s > max(res[f"{pid}_own{g}|{L}|{form}"][0] for g in range(OWN))
            lr.append(sum(u == v for u, v in zip(res[f"{pid}|{L}|{form}"][1], plants[pid]["pt"])))
        power[L] = [f, PLANTS]; letters[L] = lr
    cells = [(L, f) for L in LENGTHS for f in m.FORMS]
    Mx = np.array([[res[f"copy{i}|{L}|{f}"][0] for (L, f) in cells] for i in range(N_COPIES)])
    mu, sd = Mx.mean(axis=0), Mx.std(axis=0) + 1e-9
    zk = (np.array([res[f"k4|{L}|{f}"][0] for (L, f) in cells]) - mu) / sd
    zc = ((Mx - mu) / sd).max(axis=1)
    s_k4 = float(zk.max())
    p_k4 = (1 + int((zc >= s_k4).sum())) / (N_COPIES + 1)
    rank = {f"{L}/{f}": int((Mx[:, k] >= res[f"k4|{L}|{f}"][0]).sum()) for k, (L, f) in enumerate(cells)}
    best = cells[int(zk.argmax())]
    known_in_place = {f"{L}/{f}": sum(res[f"k4|{L}|{f}"][1][q - 1] == ch for q, ch in ctx.KNOWN.items()) for (L, f) in cells}
    cands = [{"plaintext": res[f"k4|{L}|{f}"][1], "key": {"alphabet": res[f"k4|{L}|{f}"][2], "form": f, "shifts": res[f"k4|{L}|{f}"][3]}}
             for (L, f) in cells]
    from kryptos.scorer import free_text     # gate 4's controls only, after the search
    controls = [max(ctx.english_score(free_text(res[f"copy{i}|{L}|{f}"][1])) for (L, f) in cells) for i in range(N_COPIES)]
    bounds = {
        "item": "F13.4c lengths 6-19 (D3)", "search_reads_known_letters": False, "forms": list(m.FORMS),
        "search": "0236's climb, unchanged (imported): 0140's parallel tempering with no known letter, 3 runs x 16 replicas x 625 rounds x 1000 moves; MIX8m rescoring",
        "k4_copies": N_COPIES, "cells": len(cells), "plant_power": power, "plant_letters_right": letters,
        "k4_z_by_cell": {f"{L}/{f}": round(float(z), 3) for (L, f), z in zip(cells, zk)},
        "k4_copies_at_or_above_by_cell": rank, "k4_cells_above_all_copies": sum(1 for v in rank.values() if v == 0),
        "k4_statistic": round(s_k4, 3), "k4_best_cell": f"{best[0]}/{best[1]}", "k4_p": round(p_k4, 4),
        "k4_known_letters_in_place_by_cell": known_in_place,
        "climbs": len(jobs), "exhaustive": False, "compute_seconds": round(time.time() - t0),
        "modal_cost_estimate": f"{len(jobs)} climbs x about 10 s (0236) = about 9 core-hours, about $0.6 of Modal credit",
    }
    notes = (f"F13.4c 6-19: K4 statistic {s_k4:.2f} at {best[0]}/{best[1]}, p {p_k4:.3f} against {N_COPIES} shuffles; "
             f"cells with K4 above all {bounds['k4_cells_above_all_copies']} of {len(cells)}; plant power "
             + ", ".join(f"L{L} {v[0]}/{v[1]}" for L, v in power.items()))
    return {"candidates": cands, "bounds": bounds, "notes": notes, "controls": controls}


def encrypt(plaintext, key):
    return M().encrypt(plaintext, key)


def worked_example(ctx, key):
    return M().worked_example(ctx, key)
