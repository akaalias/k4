"""Experiment 0222. See program.md for the contract."""

EXPERIMENT = {
    "slug": "rejudge-the-sampled-verdicts-completed-periodic-keys",
    "title": "A6.1, part 2: the completed periodic keys of 0034, 0035 and 0048 (lengths 27-29 on the sculpture's and the puzzle words' tables, and 0034's 53-95) rejudged blind: K4's saved readings against the same frozen searches' readings on 10 copies each",
    "family": "1-keyed-periodic",
    "parent": "0221-rejudge-the-sampled-verdicts-free-alphabets-and-running-english",
    "changed": (
        "A6.1 (Stage 2, step 4, issue #84), the second group of sampled verdicts. 0034 (one periodic key on the standard "
        "and KRYPTOS tables, 24 conventions, periods 27-29 and 53-95 every third), 0035 (27-29, one side keyword-mixed "
        "from the vocabulary) and 0048 (27-29, both sides keyword-mixed) completed the free key slots by a quadgram climb "
        "and compared K4's best with shuffled K4 by quadgram. Their copies were never kept, and their runs stopped on the "
        "clock, so they cannot be replayed letter for letter; but 0216 ran each frozen search unchanged on 10 fresh plain "
        "shuffles (tools/a13_check.py pass1-regen, seed 1300) and kept every reading (reports/a13-structure-data/"
        "pass1_copies.json). Here K4's saved readings and those copies' readings go to the judge in one blind call per "
        "experiment. 0037's sampled triples are not rejudged: F6.3b's close rests on 0158's exact count."
    ),
    "hypothesis_expert": (
        "A6 (knowledge/12-assumptions.md); C27(c) and C5 for the tables (the keyword-mixed alphabets of 0035 and 0048), "
        "C19 for the judge's tolerance of X stops. Cells: 0034 at 27-29 (3 readings per text), 0034 at 53-95 (15 readings; "
        "already blocked by 0136's bound, judged for the record), 0035 at 27-29 (3), 0048 at 27-29 (3). Statistic per cell: "
        "the judge's (j3, Sonnet 5.5) best score over a text's readings; K4 counts only strictly above all 10 copies' bests; "
        "None as not found. Every reading of every text is sent (no quadgram cut, the same for K4 and copies). Four cells, "
        "chance about 4/11 = 0.36 cells with K4 above every copy; a flag needs p < 0.05/4, 80 copies, so a K4 above every "
        "copy here is a candidate to replicate on that cell against fresh copies, not a result."
    ),
    "hypothesis_eli5": (
        "Three old experiments filled in long keys so that the carved letters read as much like English as possible, and "
        "compared the result with the same trick on scrambled copies using a simple letter-statistics score. That score is "
        "poor at telling damaged English from English-looking junk. Here the judge, a language model that reads one text "
        "at a time without knowing where it came from, reads the carved letters' readings and the copies' readings."
    ),
    "prediction": (
        "K4 above every copy in no cell (chance 0.36). The copies' best judge scores are 20-50 at 53-95, where the climb "
        "fills 47-71 free letters with English-like fragments, and under 20 at 27-29, where only 3-5 letters are free. "
        "Zero candidates pass gate 4."
    ),
    "method": (
        "1. K4: the 24-of-24 readings saved in 0034 (18), 0035 (3), 0048 (3) raw.json. "
        "2. Copies: the readings of the same frozen searches on 10 plain shuffles each, from pass1_copies.json. "
        "3. One judge call per experiment on all of K4's and the copies' readings; per text and cell, the best score. "
        "4. K4 counts only strictly above every copy's best."
    ),
    "walkthrough": (
        "1. Take 0035's three readings of K4, one per key length 27, 28 and 29. "
        "2. Take the same search's three readings of each of 10 scrambled copies. "
        "3. Hide the 24 known letters and give all 33 readings to the judge one at a time, unlabelled. "
        "4. Keep each text's best score. "
        "5. K4 wins only if its best is above all 10 copies' bests."
    ),
}

import importlib.util
import json
from pathlib import Path

N = 97
ROOT = Path(__file__).resolve().parent
EXPS = ("0034", "0035", "0048")
PASS1 = ROOT / "reports/a13-structure-data/pass1_copies.json"
_MODS = {}


def _folder(e):
    return next((ROOT / "experiments").glob(f"{e}-*"))


def _load(e):
    if e not in _MODS:
        import sys
        spec = importlib.util.spec_from_file_location(f"frozen{e}", _folder(e) / "attack.py")
        m = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = m
        spec.loader.exec_module(m)
        _MODS[e] = m
    return _MODS[e]


def _period(label):
    return int(label.split()[1].rstrip(","))


def cell_of(e, P):
    return f"{e} P27-29" if P <= 29 else f"{e} P53-95"


def _s(v):
    return -1 if v is None else v


def run(ctx):
    from kryptos.scorer import english_score, free_text
    p1 = json.loads(PASS1.read_text())
    by_cell, calls, controls, cands = {}, 0, [], []
    for e in EXPS:
        raw = json.loads((_folder(e) / "raw.json").read_text())
        k4 = [(_period(c["key_description"]), c["plaintext"]) for c in raw["candidates"] if "?" not in c["plaintext"]]
        copies = {}
        for key, v in p1.items():
            if key.startswith(e + "/"):
                copies[int(key.split("/")[1])] = [(_period(lab), t) for lab, t in v["rows"]]
        texts, owner = [], []
        for P, t in k4:
            texts.append(t); owner.append(("k4", P))
        for g in sorted(copies):
            for P, t in copies[g]:
                texts.append(t); owner.append((g, P))
                controls.append(english_score(free_text(t)))
        v = ctx.judge(texts)
        calls += len(texts)
        best = {}
        for (who, P), x in zip(owner, v):
            c = cell_of(e, P)
            cur = best.setdefault(c, {}).get(who)
            if cur is None or _s(x["score"]) > _s(cur[0]):
                best[c][who] = (x["score"], x["reading"])
        nones = sum(1 for x in v if x["score"] is None)
        for c, b in best.items():
            k4s = b["k4"][0]
            cs = [b[g][0] for g in sorted(copies) if g in b]
            top = max(_s(x) for x in cs)
            by_cell[c] = {"k4_judge": k4s, "k4_judge_reading": b["k4"][1], "copies_best": cs, "copies_max": top,
                          "k4_above_every_copy": k4s is not None and k4s > top,
                          "k4_rank": 1 + sum(1 for x in cs if _s(x) >= _s(k4s)), "n_copies": len(cs),
                          "readings_per_text": sum(1 for w, P in owner if w == "k4" and cell_of(e, P) == c),
                          "judge_none_in_call": nones}
        for P, t in k4:
            c = next(cc for cc in raw["candidates"] if cc["plaintext"] == t)
            cands.append({"plaintext": t, "key": {"exp": e, "key": c["key"]},
                          "key_description": f"saved reading of {e}: " + c.get("key_description", "")[:100],
                          "notes": f"A6.1: cell {cell_of(e, P)}, K4 best judge {by_cell[cell_of(e, P)]['k4_judge']}"})
    flagged = [c for c, r in by_cell.items() if r["k4_above_every_copy"]]
    bounds = {
        "item": "A6.1 (part 2)", "experiments": list(EXPS), "cells": len(by_cell), "flag_level": "p < 0.05 / 4; needs 80 copies",
        "copies": "0216's regeneration (tools/a13_check.py pass1-regen, seed 1300): each frozen search unchanged on 10 plain shuffles",
        "by_cell": by_cell, "k4_above_every_copy_cells": flagged, "chance_expected": round(4 / 11, 2),
        "judge_texts_sent": calls, "judge_calls_estimated": 264, "quadgram_cut": "none: every reading of K4 and of the copies sent",
        "not_rejudged": {"0037": "F6.3b's close rests on 0158's exact count (105.5 million routes); 0037 kept no reading"},
        "controls": "quadgram scores of every copy reading of the three searches (pass1_copies.json); each K4 reading faces its own experiment's copies among them (issue #88)",
        "exhaustive": False,
    }
    notes = "; ".join(f"{c}: K4 {r['k4_judge']}, copies best {r['copies_max']} (rank {r['k4_rank']} of {r['n_copies'] + 1})"
                      for c, r in by_cell.items())
    return {"candidates": cands, "bounds": bounds, "notes": notes, "controls": controls}


def encrypt(plaintext, key):
    """The frozen experiment's own encrypt (0034, 0035, 0048: a periodic key on the stated tables)."""
    return _load(key["exp"]).encrypt(plaintext, key["key"])


def worked_example(ctx, key):
    from kryptos.judge import mask
    raw = json.loads((_folder("0035") / "raw.json").read_text())
    c = raw["candidates"][0]
    return "\n".join([f"0035's reading of K4 ({c['key_description'][:70]}):", f"  reading      {c['plaintext']}",
                      f"  judge sees   {mask(c['plaintext'])}", "",
                      "  the judge reads it among 30 readings of 10 scrambled copies by the same search, one at a time, unlabelled."])
