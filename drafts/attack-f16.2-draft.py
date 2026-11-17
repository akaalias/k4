"""Experiment: F16.2. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f16.2-a-book-plus-a-keyword",
    "title": "F16.2: a passage of a named text under the message plus a short repeated word on top, on the plain and KRYPTOS tables, Vigenere and Beaufort with the text added or taken away, every offset and direction, word lengths 1-16, decided exactly on the 24 and on the 20 official known letters with up to two slips (lengths 1-12); K4 against 20 shuffles, plants",
    "family": "16-simple-hand-methods",
    "parent": "0210-running-keys-with-slips-at-known-places",
    "changed": (
        "F16.2 (issue #123). 0210 tested the named texts as a running key alone; 0117 and 0211 added a one-letter shift. "
        "Here the running key carries a repeated word of length 1-16 on top: the forced key at the known places, minus "
        "the text letter there, must repeat with the word's period. Texts: 0210's (K1-K3 plain and cipher, Carter vol. 1, "
        "the tableau by rows and columns, the Morse, the right panel, Sanborn's 1989 letter, the 1991 Cryptogram, the 2025 "
        "open letter) plus eleven new ones (Carter vols. 2-3, KJV Genesis and John, the Declaration, the Constitution, "
        "Gettysburg, Poe's Gold-Bug, Kennedy 1963 and Reagan 1987 in Berlin, the National Security Act 1947), forward and "
        "backward, every cyclic offset."
    ),
    "hypothesis_expert": (
        "C7, C9 (earlier text as key or instructions), C5 (Scheidt: 'executed years later when used with the correct key "
        "word/s', 03-scheidt-said.md), C3 (Scheidt's split keys: a book and a word as two parts combined, Family C in "
        "06-hypotheses.md); Sanborn's NYPVTT=BERLIN one-to-one (C-dinner 2011, 02-sanborn-said.md). Model: two additive "
        "stages on one table (standard or KRYPTOS alphabet on both sides, letters numbered in it): c = p + t_{o+i} + w_{i "
        "mod L} (Vigenere) or c = t_{o+i} + w_{i mod L} - p (Beaufort), with the text added or subtracted (s = +/-1; "
        "variant forms coincide with these because the word is free). At each known place the forced key K_q (c - p or "
        "c + p) minus s t_{o+q-1} must equal w at slot (q-1) mod L. Exact: per offset and slot, the slips needed are the "
        "places outside the slot's most common residue; a setting fits at k when they total k or less. Known letters: all "
        "24, and the 20 official ones (EAST second-hand, #124). Chance per setting at length L with c covered slots and "
        "n known places: 26^-(n - c - k) times the choice of slips; on 24 letters at L <= 12 with 2 slips, about 10^-3 "
        "fits per run; on 20 letters fits by chance appear from about L = 10 and are compared with the shuffles."
    ),
    "hypothesis_eli5": (
        "A book cipher with a twist: write a passage of a known text under the message, add it letter by letter on the "
        "table, then add a short word repeated over and over. Experiment 210 tried the passages alone; here we add the "
        "repeated word, every length up to 16, for every starting place in twenty-odd texts Sanborn might have used, "
        "allowing two slips, on the carving and on scrambled copies."
    ),
    "prediction": (
        "On 24 letters no setting fits K4 or any shuffle at word lengths 1-12 with up to 2 slips, nor at 13-16 with none; "
        "plants found 6 of 6 (their setting fits and their shuffles have no fit at its length). On 20 letters fits appear "
        "from about length 10 on K4 and shuffles alike, counts inside the shuffles; their readings judged no better than "
        "the shuffles'. Zero candidates beyond K4's 20-letter fits, which fail at EAST if EAST holds."
    ),
    "method": (
        "1. Texts: letters only, forward and backward, cyclic. 2. For each table (standard, KRYPTOS), form (Vigenere, "
        "Beaufort) and sign of the text: the forced key at each known place, minus the text letter at every offset (a "
        "matrix offsets x places). 3. For each word length 1-16: per slot, places outside the slot's most common value "
        "are slips; keep settings with 2 or fewer at lengths 1-12, none at 13-16. 4. The same for 20 shuffles of K4 and "
        "for 6 planted messages and their own 5 shuffles. 5. Each fit's reading (the word fixed where the known places "
        "reach) to quadgrams; the best of each text and every reading above -5.0 to the judge, all in one call."
    ),
    "walkthrough": (
        "1. Write K4, and under it a passage of the Gettysburg Address from some letter on. "
        "2. On the plain table, at each known place, find the key letter that turns the known letter into the carved one. "
        "3. Subtract the Gettysburg letter under it: what is left is the repeated word's letter for that place. "
        "4. Choose a word length, say 5, and group the known places by place mod 5. "
        "5. Within each group the leftover letters must agree, except at most two slips overall. "
        "6. If they do, read the word's letters off the groups and decrypt the rest of K4 with text plus word. "
        "7. Repeat for every starting letter, both directions, every text, both tables, and on scrambled copies."
    ),
    "expected_minutes": 60,
}

import importlib.util
import math
import multiprocessing as mp
import os
import random
import sys
import types
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
N = 97
STD = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KRY = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
OFFICIAL = tuple(range(26, 35)) + tuple(range(64, 75))
LMAX, LSLIP, KMAX = 16, 12, 2
N_COPIES = 20
N_PLANT_COPIES = 5
SEED = 16300
NEW_SOURCES = ["carter-1927-tomb-of-tutankhamen-vol2", "carter-1933-tomb-of-tutankhamen-vol3", "kjv-genesis", "kjv-john",
               "declaration-of-independence-1776", "us-constitution-1787", "gettysburg-address-1863", "poe-1843-the-gold-bug",
               "kennedy-1963-ich-bin-ein-berliner", "reagan-1987-brandenburg-gate", "national-security-act-1947"]
TABLES = {"std": STD, "kry": KRY}
COMBOS = [(tb, form, s) for tb in TABLES for form in ("vig", "beau") for s in (1, -1)]
PLANTS = [(16301, "gettysburg-address-1863 fwd", ("std", "vig", 1), 5, 0), (16302, "K1+K2+K3 plain fwd", ("kry", "vig", 1), 7, 1),
          (16303, "carter vol1 bwd", ("std", "beau", -1), 11, 2), (16304, "reagan-1987-brandenburg-gate fwd", ("kry", "beau", 1), 3, 2),
          (16305, "kjv-genesis fwd", ("std", "vig", -1), 14, 0), (16306, "poe-1843-the-gold-bug bwd", ("kry", "vig", 1), 9, 1)]
JUDGE_CUT = -5.0
TOPJ = 3
_G = {}


def letters(s):
    return "".join(c for c in s.upper() if "A" <= c <= "Z")


def sources():
    """0210's texts (its sources(), unchanged) plus the eleven F16.2 adds, forward and backward."""
    path = next((ROOT / "experiments").glob("0210-*")) / "attack.py"
    spec = importlib.util.spec_from_file_location("frozen0210", path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    m.ROOT = ROOT
    out = {k: v[1] for k, v in m.sources().items()}
    for name in NEW_SOURCES:
        t = (ROOT / "knowledge" / "sources" / f"{name}.txt").read_text(errors="ignore")
        t = t.split("\n\n", 1)[1]                           # drop our two-line provenance header
        s = letters(t)
        out[name + " fwd"] = s
        out[name + " bwd"] = s[::-1]
    return out


def forced(text, known, tb, form):
    A = TABLES[tb]
    out = []
    for q in sorted(known):
        c, p = A.index(text[q - 1]), A.index(known[q])
        out.append((c - p) % 26 if form == "vig" else (c + p) % 26)
    return np.array(out, dtype=np.int16)


def scan_text(text, known, srcs_idx, collect=True):
    """All settings fitting with <= KMAX slips (L <= LSLIP) or none (L > LSLIP).
    -> list of (source, offset, table, form, sign, L, slips, word (dict slot->value))."""
    Q = sorted(known)
    qi = np.array([q - 1 for q in Q])
    fits = []
    for name, S_by_tb in srcs_idx.items():
        n = len(S_by_tb["std"])
        offs = np.arange(n)
        idx = (offs[:, None] + qi[None, :]) % n                       # offsets x places
        for tb, form, sgn in COMBOS:
            K = forced(text, known, tb, form)
            R = (K[None, :] - sgn * S_by_tb[tb][idx]) % 26             # residue = word letter wanted
            R = R.astype(np.int8)
            for L in range(1, LMAX + 1):
                kmax = KMAX if L <= LSLIP else 0
                slots = {}
                for j, q in enumerate(Q):
                    slots.setdefault((q - 1) % L, []).append(j)
                need = np.zeros(n, dtype=np.int16)
                for js in slots.values():
                    if len(js) == 1:
                        continue
                    sub = R[:, js]
                    best = np.zeros(n, dtype=np.int16)
                    for a in range(len(js)):
                        best = np.maximum(best, (sub == sub[:, a:a + 1]).sum(axis=1).astype(np.int16))
                    need += len(js) - best
                    if kmax == 0:
                        pass
                hit = np.nonzero(need <= kmax)[0]
                for o in hit:
                    fits.append((name, int(o), tb, form, sgn, L, int(need[o])))
    return fits


def word_of(text, known, S_by_tb, o, tb, form, sgn, L):
    """The word's value per slot: the most common residue among the slot's known places; None where no place."""
    Q = sorted(known)
    n = len(S_by_tb["std"])
    K = forced(text, known, tb, form)
    w = {}
    for j, q in enumerate(Q):
        w.setdefault((q - 1) % L, []).append(int((K[j] - sgn * S_by_tb[tb][(o + q - 1) % n]) % 26))
    return {s: max(set(v), key=v.count) for s, v in w.items()}


def reading(text, S_by_tb, o, tb, form, sgn, L, w):
    A = TABLES[tb]
    n = len(S_by_tb["std"])
    out = []
    for i in range(N):
        s = i % L
        if s not in w:
            out.append("?")
            continue
        k = (sgn * int(S_by_tb[tb][(o + i) % n]) + w[s]) % 26
        c = A.index(text[i])
        out.append(A[(c - k) % 26] if form == "vig" else A[(k - c) % 26])
    return "".join(out)


def encipher(pt, S, o, tb, form, sgn, word):
    A = TABLES[tb]
    n = len(S)
    out = []
    for i, ch in enumerate(pt):
        k = (sgn * A.index(S[(o + i) % n]) + A.index(word[i % len(word)])) % 26
        p = A.index(ch)
        out.append(A[(p + k) % 26] if form == "vig" else A[(k - p) % 26])
    return "".join(out)


def _job(args):
    tid, text, kname = args
    known = _G["known"][kname]
    fits = scan_text(text, known, _G["srcs_idx"])
    return tid, kname, fits


def shuffled(text, seed):
    l_ = list(text)
    random.Random(seed).shuffle(l_)
    return "".join(l_)


def run(ctx):
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    from kryptos.plants import english_plant
    from kryptos.scorer import free_text
    srcs = sources()
    srcs_idx = {name: {tb: np.array([TABLES[tb].index(c) for c in s], dtype=np.int16) for tb in TABLES} for name, s in srcs.items()}
    _G["srcs_idx"] = srcs_idx
    k24 = dict(ctx.KNOWN)
    k20 = {q: k24[q] for q in OFFICIAL}
    _G["known"] = {"k24": k24, "k20": k20}
    # self-check: K1 is the zero text with PALIMPSEST on the KRYPTOS table, Vigenere
    import json
    k1 = json.loads((ROOT / "data" / "k1.json").read_text())
    pt1 = k1["plaintext"]; ct1 = k1["ciphertext"][:len(pt1)]
    assert encipher(pt1, "K", 0, "kry", "vig", 1, "PALIMPSEST") == ct1, "K1 self-check failed"
    texts = [("K4", ctx.K4)] + [(f"copy{i}", shuffled(ctx.K4, SEED + i)) for i in range(N_COPIES)]
    plants = []
    for seed, sname, (tb, form, sgn), L, k in PLANTS:
        rng = random.Random(seed)
        pt = english_plant(seed)
        S = srcs[sname]
        o = rng.randrange(len(S))
        word = "".join(rng.choice(STD) for _ in range(L))
        ct = list(encipher(pt, S, o, tb, form, sgn, word))
        places = sorted(rng.sample(sorted(OFFICIAL), k)) if k else []
        for q in places:
            ct[q - 1] = rng.choice([c for c in STD if c != ct[q - 1]])
        ct = "".join(ct)
        plants.append({"seed": seed, "source": sname, "offset": o, "table": tb, "form": form, "sign": sgn, "L": L, "k": k,
                       "slips": places, "word": word, "pt": pt, "ct": ct})
        texts.append((f"plant{seed}", ct))
        texts += [(f"plant{seed}_c{i}", shuffled(ct, seed * 100 + i)) for i in range(N_PLANT_COPIES)]
    jobs = [(tid, t, kn) for tid, t in texts for kn in ("k24", "k20")]
    saved = getattr(ctx, "saved", {}) or {}
    res = {}
    for tid, t, kn in jobs:
        if f"{tid}|{kn}" in saved:
            res[(tid, kn)] = [tuple(x) for x in saved[f"{tid}|{kn}"]]
    todo = [j for j in jobs if (j[0], j[2]) not in res]
    W = int(os.environ.get("K4_WORKERS", 8))
    ctx.progress(len(res), len(jobs), "texts x known sets")
    with mp.get_context("fork").Pool(W) as pool:
        for tid, kn, fits in pool.imap_unordered(_job, todo, chunksize=1):
            fits = fits[:20000]
            res[(tid, kn)] = fits
            ctx.save(f"{tid}|{kn}", [list(x) for x in fits])
            ctx.progress(len(res), len(jobs), "texts x known sets")
    tmap = dict(texts)

    def count_by_L(fits):
        c = [0] * (LMAX + 1)
        for f in fits:
            c[f[5]] += 1
        return c[1:]

    # readings and quadgrams
    recs = {}
    for (tid, kn), fits in res.items():
        if tid.startswith("plant") and "_c" not in tid:
            pass
        rr = []
        for f in fits[:3000]:
            name, o, tb, form, sgn, L, need = f
            known = _G["known"][kn]
            w = word_of(tmap[tid], known, srcs_idx[name], o, tb, form, sgn, L)
            r = reading(tmap[tid], srcs_idx[name], o, tb, form, sgn, L, w)
            free = "".join(c for i, c in enumerate(r, start=1) if i not in known and c != "?")
            rr.append({"fit": list(f), "reading": r, "word": "".join(TABLES[tb][w[s]] if s in w else "?" for s in range(L)),
                       "quad": round(ctx.english_score(free), 3) if len(free) >= 20 else -9.0})
        recs[(tid, kn)] = rr
    to_judge = set()
    for (tid, kn), rr in recs.items():
        if tid.startswith("plant"):
            continue
        top = sorted(rr, key=lambda r: -r["quad"])[:TOPJ]
        for r in top + [r for r in rr if r["quad"] >= JUDGE_CUT]:
            to_judge.add(r["reading"])
    order = sorted(to_judge)[:2500]
    verdicts = dict(zip(order, ctx.judge(order))) if order else {}
    none_count = sum(1 for v in verdicts.values() if v is None or v.get("score") is None)
    for rr in recs.values():
        for r in rr:
            v = verdicts.get(r["reading"])
            r["judge"] = v["score"] if v else None

    def jbest(tid, kn):
        sc = [r["judge"] for r in recs[(tid, kn)] if r.get("judge") is not None]
        return max(sc) if sc else None
    summary = {}
    for kn in ("k24", "k20"):
        k4c = count_by_L(res[("K4", kn)])
        cc = [count_by_L(res[(f"copy{i}", kn)]) for i in range(N_COPIES)]
        per_L = {}
        for L in range(1, LMAX + 1):
            cv = [c[L - 1] for c in cc]
            per_L[L] = {"k4": k4c[L - 1], "copies_median": float(np.median(cv)), "copies_max": max(cv),
                        "at_or_above": sum(1 for x in cv if x >= k4c[L - 1]),
                        "p": round((1 + sum(1 for x in cv if x >= k4c[L - 1])) / (N_COPIES + 1), 3) if k4c[L - 1] else None}
        cjb = [jbest(f"copy{i}", kn) for i in range(N_COPIES)]
        summary[kn] = {"per_length": per_L, "k4_total": sum(k4c), "copies_total": [sum(c) for c in cc],
                       "k4_judge_best": jbest("K4", kn), "copies_judge_best": cjb,
                       "k4_above_every_copy_at_judge": (jbest("K4", kn) is not None and all(x is None or jbest("K4", kn) > x for x in cjb)),
                       "k4_top": sorted(recs[("K4", kn)], key=lambda r: -(r["judge"] if r.get("judge") is not None else -1 + r["quad"] / 100))[:10]}
    plant_out = []
    for p in plants:
        for kn in ("k24", "k20"):
            fits = res[(f"plant{p['seed']}", kn)]
            hit = [f for f in fits if f[0] == p["source"] and f[1] == p["offset"] and (f[2], f[3], f[4]) == (p["table"], p["form"], p["sign"]) and f[5] == p["L"]]
            own = [sum(1 for f in res[(f"plant{p['seed']}_c{i}", kn)] if f[5] == p["L"]) for i in range(N_PLANT_COPIES)]
            rr = [r for r in recs[(f"plant{p['seed']}", kn)] if r["fit"][:6] == [p["source"], p["offset"], p["table"], p["form"], p["sign"], p["L"]]]
            right = None
            if rr:
                r = rr[0]["reading"]
                right = sum(1 for i, c in enumerate(r) if c == p["pt"][i]) / sum(1 for c in r if c != "?")
            plant_out.append({"seed": p["seed"], "known": kn, "source": p["source"], "L": p["L"], "k": p["k"], "slips": p["slips"],
                              "planted_setting_fits": bool(hit), "reading_right_fraction": right,
                              "own_copies_fits_at_L": own, "found": bool(hit) and max(own) == 0})
    cands = []
    for r in summary["k24"]["k4_top"][:20]:
        name, o, tb, form, sgn, L, need = r["fit"]
        if "?" in r["reading"]:
            continue
        cands.append({"plaintext": r["reading"], "key": {"source": name, "offset": o, "table": tb, "form": form, "sign": sgn,
                                                         "word": r["word"]}, "notes": f"judge {r.get('judge')}, quad {r['quad']}, slips {need}"})
    total_letters = sum(len(s) for s in srcs.values())
    return {
        "candidates": cands,
        "bounds": {
            "item": "F16.2", "sources": {k: len(v) for k, v in srcs.items()}, "source_letters_both_directions": total_letters,
            "tables": list(TABLES), "forms": "Vigenere (c = p + s t + w) and Beaufort (c = s t + w - p), s = +1 or -1; variant forms coincide",
            "word_lengths": [1, LMAX], "slips": f"0-{KMAX} at lengths 1-{LSLIP}, 0 at {LSLIP + 1}-{LMAX}",
            "settings_per_text": total_letters * len(COMBOS) * LMAX,
            "known_sets": {"k24": "all 24", "k20": "the 20 official (26-34, 64-74)"},
            "summary": summary, "plants": plant_out,
            "plants_found": {kn: sum(1 for p in plant_out if p["known"] == kn and p["found"]) for kn in ("k24", "k20")},
            "judge": {"sent": len(order), "none": none_count, "cut": JUDGE_CUT, "rule": f"each text's top {TOPJ} by quadgrams and every reading at or above {JUDGE_CUT}; plants not sent"},
            "controls": f"{N_COPIES} shuffles of K4 (seeds {SEED}-{SEED + N_COPIES - 1}); each plant against {N_PLANT_COPIES} shuffles of its own",
            "exhaustive": "yes: every cyclic offset of every source, both directions; fits capped at 20,000 per text and known set (reported)",
            "aws_cost_estimate_dollars": 1.0,
        },
        "notes": (f"k24: K4 fits {summary['k24']['k4_total']} (copies {min(summary['k24']['copies_total'])}-{max(summary['k24']['copies_total'])}), "
                  f"judge K4 {summary['k24']['k4_judge_best']} vs copies' best {max([x for x in summary['k24']['copies_judge_best'] if x is not None] or [None])}; "
                  f"k20: K4 fits {summary['k20']['k4_total']} (copies {min(summary['k20']['copies_total'])}-{max(summary['k20']['copies_total'])}), "
                  f"judge K4 {summary['k20']['k4_judge_best']} vs copies' best {max([x for x in summary['k20']['copies_judge_best'] if x is not None] or [None])}; "
                  f"plants found {[(p['seed'], p['known'], p['found']) for p in plant_out]}"),
    }


def encrypt(plaintext, key):
    srcs = sources()
    return encipher(plaintext, srcs[key["source"]], key["offset"], key["table"], key["form"], key["sign"], key["word"])


def worked_example(ctx, key):
    srcs = sources()
    S = srcs["gettysburg-address-1863 fwd"]
    lines = ["plain table, Vigenere: the forced key at each known place minus the Gettysburg letter under it, offset 0", "",
             "place  known  carved  key  text  word letter"]
    for q in (26, 27, 28, 64, 65, 66):
        c, p = STD.index(ctx.K4[q - 1]), STD.index(ctx.KNOWN[q])
        k = (c - p) % 26
        t = STD.index(S[q - 1])
        lines.append(f"{q:>5}  {ctx.KNOWN[q]:>5}  {ctx.K4[q - 1]:>6}  {STD[k]:>3}  {S[q - 1]:>4}  {STD[(k - t) % 26]:>11}")
    lines += ["", "For a word of length L the word letters at places equal mod L must agree (two slips allowed at L <= 12)."]
    return "\n".join(lines)
