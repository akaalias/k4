"""Experiment 0219. See program.md for the contract."""

EXPERIMENT = {
    "slug": "rejudge-the-sampled-verdicts-free-alphabets-and-running-english",
    "title": "A6.1, part 1: the sampled verdicts of 0120, 0125, 0140, 0142, 0144 and 0146 rerun unchanged from their frozen searches, with every best reading (K4's, the copies', the plants') read by the blind judge instead of quadgrams",
    "family": "1-keyed-periodic",
    "parent": "0140-k4-against-its-own-copies-with-the-tempering-climb",
    "changed": (
        "A6.1 (Stage 2, step 4, issue #84). Every sampled close in F1 compared K4's climbed reading with the copies' "
        "climbed readings by quadgram score, and the judge bench (reports/judge-bench.md) shows quadgrams find none of the "
        "damaged classes against English-like junk, which is what a climb returns on a copy. Here the six verdicts of F1.1 "
        "(0120 at 23 and 26, 0140 at 23, 0142 at 26), F1.2 (0144 at 13 and 16, 0146 at 8) and F1.3 (0125) are rejudged: "
        "each frozen attack.py is run unchanged with its own seeds (nothing was saved but K4's reading and the copies' "
        "scores), its process pool intercepted to keep every job's reading, K4's reading checked against the record, and "
        "K4's, the copies' and the in-run plants' best readings read by the judge, one blind call per verdict."
    ),
    "hypothesis_expert": (
        "A6 and A13 (knowledge/12-assumptions.md): the sampled closes of F1.1 (one free alphabet, Beaufort form, key "
        "lengths 23 and 26: 0120, 0140, 0142), F1.2 (two free alphabets, lengths 8, 13, 16: 0144, 0146) and F1.3 (a running "
        "key from an unknown English text on the 208,062 dictionary tables: 0125) rest on the quadgram mean of a climbed "
        "reading. C5 and C27(c) (a keyed alphabet 'slightly different' from KRYPTOS, the K1/K2 system) are the clues those "
        "closes read; C19 (X stops, Scheidt 2015) and the bench's damaged classes are why the score is in doubt. Statistic "
        "per verdict: the judge's score (j3, Sonnet 5.5, kryptos/judge.py) of K4's best reading against the best of each "
        "copy's, copies made by the frozen code (0119's exact decider for 0120/0140/0142, kept-place shuffles for "
        "0144/0146, plain shuffles for 0125), K4 counting only strictly above every copy, None as not found. 0125's "
        "reading is the forced running-key stretch (24 letters at 22-34 and 64-74), shown to the judge at places 35-47 "
        "and 49-59 with '?' elsewhere so its masking of the known places does not hide it. Eight cells; chance puts K4 "
        "above all 12 (50) copies with p = 1/13 (1/51) each, about 0.6 cells in all; a cell flags at p < 0.05 / 8, which "
        "needs 160 copies: a K4 above every copy here is a candidate for that replication, not a result."
    ),
    "hypothesis_eli5": (
        "Several earlier experiments could not decide a question exactly, so they let a computer adjust the key for the "
        "best-looking English on the carved letters and on scrambled copies of them, and compared the two with a simple "
        "letter-statistics score. That score turned out to be poor at spotting damaged English, with missing words, X's "
        "between words or a few wrong letters. Here we rerun those same searches exactly as they were and let the judge, "
        "a language model that reads one text at a time without knowing where it came from, score the carved letters' "
        "reading and the copies' readings side by side."
    ),
    "prediction": (
        "K4's reading scores above every copy's in none of the 8 cells (chance expects 0.6). K4's six saved readings are "
        "reproduced exactly. The judge finds at most as many of 0120's and 0140's planted texts as quadgrams did (0120: 3 "
        "of 6 at 23, 1 of 6 at 26; 0140: 5 of 6), because their climbed readings are only a third right (29-43 of 97 "
        "letters), and at least the 11 of 0125's 20 planted running keys that quadgrams found. Zero candidates pass gate 4."
    ),
    "method": (
        "1. For 0142, 0146, 0125, 0140, 0144, 0120 in that order: load the frozen attack.py and call its run() with the "
        "harness's context and a far deadline (every original run finished all its restarts), the process pool replaced by "
        "one that runs the same jobs and keeps each job and result. "
        "2. Check K4's reading equals the record's, and the copies' quadgram scores equal the record's. "
        "3. Per verdict, one judge call on K4's best reading and every copy's; per plant group, one call on the plants' "
        "readings and their own copies'. "
        "4. K4 counts only strictly above every copy; a plant counts as found by the judge strictly above every copy it "
        "was compared with in its experiment (0120: K4's copies at its length; 0140: its own six; 0125: the 50 copies)."
    ),
    "walkthrough": (
        "1. Take one earlier verdict, say 0140: K4 and 12 scrambled copies, each with a key climbed for English. "
        "2. Rerun that exact search, same random seeds, so every reading comes out as it did. "
        "3. Check that K4's reading is letter for letter the one in 0140's record. "
        "4. Hide the 24 known letters in each reading and give the 13 readings to the judge one at a time, unlabelled. "
        "5. K4 wins the cell only if its score is above all 12 copies' scores."
    ),
}

import importlib.util
import multiprocessing
import time
from pathlib import Path
from types import SimpleNamespace

N = 97
ROOT = Path(__file__).resolve().parent
ORDER = ("0142", "0146", "0125", "0140", "0144", "0120")


def _load(e):
    path = next((ROOT / "experiments").glob(f"{e}-*")) / "attack.py"
    spec = importlib.util.spec_from_file_location(f"frozen{e}", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m, path.parent


class _CapPool:
    """A fork pool that runs the frozen jobs unchanged and keeps (job, result) pairs."""
    def __init__(self, real, n, box):
        self.p, self.box = real("fork").Pool(n), box

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return self.p.__exit__(*a)

    def map(self, fn, jobs, chunksize=1):
        jobs = list(jobs)
        res = self.p.map(fn, jobs, chunksize)
        self.box.append((jobs, res))
        return res


def run_frozen(e, ctx):
    m, folder = _load(e)
    box = []
    real = multiprocessing.get_context

    class _Ctx:
        def Pool(self, n):
            return _CapPool(real, n, box)

    multiprocessing.get_context = lambda kind=None: _Ctx() if kind == "fork" else real(kind)
    try:
        far = SimpleNamespace(**vars(ctx))
        far.deadline = time.time() + 10 ** 6
        far.time_left = lambda: far.deadline - time.time()
        t0 = time.time()
        out = m.run(far)
        secs = time.time() - t0
    finally:
        multiprocessing.get_context = real
    jobs, res = box[-1]
    import json
    saved = json.loads((folder / "raw.json").read_text())["bounds"]
    return out, jobs, res, saved, secs


def window_text(w):
    """0125's 24-letter forced stretch, shown at places 35-47 and 49-59 so the judge's masking of 22-34 and 64-74 cannot hide it."""
    return "?" * 34 + w[:13] + "?" + w[13:] + "?" * (N - 34 - 25)


def gather(e, out, jobs, res, saved):
    """-> list of verdict cells and plant groups, each {name, k4, copies[]} or {name, plants[(text, [own texts])]}, and checks."""
    cells, groups, checks = [], [], {}
    if e == "0125":
        k4 = next(r for r in res if r[0] == "k4")
        cop = [r for r in res if r[0] == "copper"]
        pl = [r for r in res if r[0] == "plant"]
        checks["k4_reading_reproduced"] = list(k4[3]) == list(saved["k4"]["reading"])
        checks["copies_scores_reproduced"] = sorted(round(r[2], 4) for r in cop) == sorted(c["score"] for c in saved["coppers"])
        cw = [window_text(r[3][4]) for r in cop]
        cells.append({"name": "0125 running key", "k4": window_text(k4[3][4]), "copies": cw, "k4_quad": k4[2],
                      "copies_quad": [r[2] for r in cop]})
        groups.append({"name": "0125 plants", "against": "the 50 copies",
                       "plants": [(window_text(r[3][4]), r[3][4] == r[6]) for r in pl], "own": None, "shared": cw})
        return cells, groups, checks
    if e == "0120":
        for L in (23, 26):
            k4 = next(r for r in res if r[0] == "k4" and r[1] == L)
            cop = [r for r in res if r[0] == "copper" and r[1] == L]
            pl = [r for r in res if r[0] == "plant" and r[1] == L]
            checks[f"k4_reading_reproduced_{L}"] = k4[6] == saved["k4_best"][str(L)]["plaintext"]
            cells.append({"name": f"0120 L{L}", "k4": k4[6], "copies": [r[6] for r in cop],
                          "cand": (k4[6], k4[4], k4[5], L)})
            groups.append({"name": f"0120 plants L{L}", "against": f"K4's 12 copies at {L}",
                           "plants": [(r[6], r[7]) for r in pl], "own": None, "shared": [r[6] for r in cop]})
        return cells, groups, checks
    # 0140, 0142, 0144, 0146: (kind, L, idx, sc, pt, alpha, k, agree, done, ok)
    checks["runs_done"] = sorted({r[8] for r in res})
    checks["decryption_checked"] = all(r[9] for r in res)
    lengths = sorted({r[1] for r in res if r[0] == "k4"})
    for L in lengths:
        k4 = next(r for r in res if r[0] == "k4" and r[1] == L)
        cop = [r for r in res if r[0] in ("copper", "copy") and r[1] == L]
        if e == "0140":
            want = saved["L23"]["k4"]["plaintext"]; want_c = saved["L23"]["coppers"]
        elif e == "0142":
            want = saved["L26"]["k4"]["plaintext"]; want_c = saved["L26"]["coppers"]
        else:
            want = saved["by_length"][str(L)]["k4"]["plaintext"]; want_c = saved["by_length"][str(L)]["copies"]
        checks[f"k4_reading_reproduced_{L}"] = k4[4] == want
        checks[f"copies_scores_reproduced_{L}"] = sorted(round(r[3], 4) for r in cop) == sorted(want_c)
        cells.append({"name": f"{e} L{L}", "k4": k4[4], "copies": [r[4] for r in cop],
                      "cand": (k4[4], k4[5], k4[6], L) if k4[5] else None})
    if e == "0140":
        pl = sorted((r for r in res if r[0] == "plant"), key=lambda r: r[2])
        own = {}
        for r in res:
            if r[0] == "own":
                own.setdefault(r[2] // 100, []).append(r[4])
        groups.append({"name": "0140 plants L26", "against": "their own 6 fitting shuffles each",
                       "plants": [(r[4], r[7]) for r in pl], "own": [own[r[2]] for r in pl], "shared": None})
    return cells, groups, checks


def _s(v):
    return -1 if v is None else v


def run(ctx):
    report, cells_out, groups_out, controls, cands = {}, [], [], [], []
    calls = 0
    for e in ORDER:
        out, jobs, res, saved, secs = run_frozen(e, ctx)
        cells, groups, checks = gather(e, out, jobs, res, saved)
        report[e] = {"seconds": round(secs), "jobs": len(jobs), "checks": checks}
        for c in cells:
            texts = [c["k4"]] + c["copies"]
            v = ctx.judge(texts)
            calls += len(texts)
            k4s = v[0]["score"]
            cs = [x["score"] for x in v[1:]]
            top = max((_s(x) for x in cs), default=-1)
            row = {"cell": c["name"], "k4_judge": k4s, "k4_judge_reading": v[0]["reading"], "copies_judge": cs,
                   "copies_best": top, "k4_above_every_copy": k4s is not None and k4s > top,
                   "k4_rank": 1 + sum(1 for x in cs if _s(x) >= _s(k4s)), "n_copies": len(cs),
                   "none": sum(1 for x in v if x["score"] is None), "k4_reading": c["k4"]}
            cells_out.append(row)
            if c.get("cand"):
                pt, alpha, k, L = c["cand"]
                cands.append({"plaintext": pt, "key": {"alphabet": alpha, "shifts": list(k), "form": "beaufort"},
                              "key_description": f"Beaufort form, one alphabet {alpha} on both sides, key length {L} ({c['name']})",
                              "notes": f"judge {k4s}, copies' best {top}"})
        for g in groups:
            plant_texts = [p for p, _ in g["plants"]]
            if g["own"] is not None:
                texts = plant_texts + [t for o in g["own"] for t in o]
            else:
                texts = plant_texts + g["shared"]
            v = ctx.judge(texts)
            calls += len(texts)
            sc = [x["score"] for x in v]
            ps = sc[:len(plant_texts)]
            if g["own"] is not None:
                found, k = [], len(plant_texts)
                for i, o in enumerate(g["own"]):
                    bar = max(_s(x) for x in sc[k:k + len(o)]); k += len(o)
                    found.append(ps[i] is not None and ps[i] > bar)
            else:
                bar = max(_s(x) for x in sc[len(plant_texts):])
                found = [p is not None and p > bar for p in ps]
            groups_out.append({"group": g["name"], "against": g["against"], "plants_judge": ps, "found": sum(found),
                               "of": len(found), "plant_detail": [d for _, d in g["plants"]],
                               "none": sum(1 for x in sc if x is None)})
    k4_flags = [c for c in cells_out if c["k4_above_every_copy"]]
    bounds = {
        "family": "rejudging F1.1, F1.2, F1.3's sampled verdicts with the blind judge (A6.1, part 1)",
        "verdicts": ORDER, "cells": len(cells_out), "flag_level": "p < 0.05 / 8; needs 160 copies per cell",
        "judge_calls_estimated": 216, "judge_texts_sent": calls,
        "runs": report, "by_cell": cells_out, "plants": groups_out,
        "k4_above_every_copy_cells": [c["cell"] for c in k4_flags],
        "chance_expected": round(7 / 13 + 1 / 51, 2),
        "stop_queue_candidates": [c["cell"] for c in k4_flags],
        "controls": "each verdict's own copies, made by its frozen code and seeds (0120: seed 120; 0125: 125; 0140: 140; 0142: 142; 0144: 144; 0146: 146)",
        "exhaustive": False,
    }
    for c in cells_out:
        controls += [x for x in c["copies_judge"] if x is not None]
    notes = "; ".join(f"{c['cell']}: K4 {c['k4_judge']}, copies best {c['copies_best']} (rank {c['k4_rank']} of {c['n_copies'] + 1})"
                      for c in cells_out)
    notes += ". Plants: " + "; ".join(f"{g['group']} {g['found']}/{g['of']}" for g in groups_out)
    return {"candidates": cands, "bounds": bounds, "notes": notes, "controls": controls}


def encrypt(plaintext, key):
    """Beaufort form on one alphabet (0120, 0140, 0142): carved place = key value minus message place, mod 26."""
    alpha, k = key["alphabet"], key["shifts"]
    pos = {ch: i for i, ch in enumerate(alpha)}
    return "".join(alpha[(k[i % len(k)] - pos[ch]) % 26] for i, ch in enumerate(plaintext))


def worked_example(ctx, key):
    lines = ["A6.1 rejudges a climbed reading. 0140's reading of K4 at key length 23 (one alphabet, Beaufort form):", ""]
    import json
    folder = next((ROOT / "experiments").glob("0140-*"))
    b = json.loads((folder / "raw.json").read_text())["bounds"]["L23"]
    pt = b["k4"]["plaintext"]
    from kryptos.judge import mask
    lines += [f"  reading      {pt}", f"  judge sees   {mask(pt)}", "",
              f"  quadgram mean {b['k4']['score']}, rank {b['k4_rank_of_13']} of 13 among its own copies",
              "  the judge reads the same 13 readings, one at a time, unlabelled; K4 must score above all 12 copies."]
    return "\n".join(lines)
