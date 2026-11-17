"""Experiment: F16.6-r. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f16.6-r-amsco-period-23-read-as-a-chart-key",
    "title": "F16.6-r: AMSCO at period 23 with the key free (a chart key): the readings of K4's 21 fitting settings, the letters each fixes, against the readings of the 200 shuffles' fitting settings, count-matched; quadgrams, then the blind judge",
    "family": "16-simple-hand-methods",
    "parent": "0266-f6.22c-amsco-period-23-forced-keys-against-a-count-matched-null",
    "changed": (
        "F16.6-r (issue #123). 0263-0266 asked whether the forced key at AMSCO period 23 is a word or English (it is not); "
        "under the revised criteria (#124) the key may come from a chart, so the question becomes the reading. 0263's "
        "routes, classes and search are imported unchanged (its settings()); every text's fitting settings at 23 are "
        "kept with the key letters they force, and each is decrypted wherever its slots are fixed."
    ),
    "hypothesis_expert": (
        "F6 (C1(a): 'a matrix code, and then... this table'; AMSCO, an irregular columnar from the field manuals) with "
        "the key from a chart (#124; Sanborn's archive holds hand-drawn coding charts). 0114 found K4 fitting 15 distinct "
        "check sets at period 23 against 1-9 on 10 coppers; 0263 replicated the count (21 settings; 4 of 200 fresh "
        "shuffles at or above, p 0.025); 0266's count-matched null on the forced keys p 0.06. Model: plaintext moved by "
        "an AMSCO route (0114's keyword and full sequences, both directions), then a period-23 key on the standard or "
        "KRYPTOS tables, Vigenere or Beaufort; the 24 known letters fix the key at the slots they land in, so the reading "
        "is fixed wherever the route puts a letter in a fixed slot. Pre-registered statistic: the best quadgram score "
        "(per letter, known places excluded, at least 30 letters fixed) over a text's settings; K4's best of 21 against "
        "10,000 draws of 21 settings from the pooled shuffle settings (count-matched, as 0266); flag at p < 0.05. "
        "Secondary: K4's top 5 and each shuffle's best read by the blind judge in one call."
    ),
    "hypothesis_eli5": (
        "With one particular way of shuffling the message (AMSCO) followed by the table with a 23-letter key, the carving "
        "fits more ways than most scrambled copies do. Earlier tests asked whether the key spelled anything; it does not. "
        "But the key might have come from a chart. So we read the messages those fits give and ask whether the carving's "
        "read better than the copies'."
    ),
    "prediction": (
        "K4's best reading inside the count-matched null (p above 0.05), not English to the judge; the plant (0263's "
        "AMSCO plant) found with its reading near Carter's text. No candidates (readings are partly undetermined)."
    ),
    "method": (
        "1. 0263's routes (891,360) and 8 classes, period 23, on K4, 200 shuffles (0263's seed) and 0263's plant. "
        "2. Keep every fitting setting with its forced slot values. 3. Decrypt each where fixed. 4. Quadgram score per "
        "reading; statistic as pre-registered. 5. Judge K4's top 5 and each shuffle's best."
    ),
    "walkthrough": (
        "1. Take one of K4's 21 settings: an AMSCO route and a table. "
        "2. Put each known letter back through the route to its carved place and find the key letter its slot (place mod 23) needs. "
        "3. For every other carved place whose slot is fixed, decrypt it and carry the letter back to its message place. "
        "4. Read the message with the unfixed places left blank; score how English it is. "
        "5. Do the same for every fitting setting of every scrambled copy and compare the best."
    ),
    "expected_minutes": 30,
}

import importlib.util
import multiprocessing as mp
import os
import random
import sys
import time
import types
from pathlib import Path

import numpy as np

N = 97
ROOT = Path(__file__).resolve().parent
P = 23
N_SHUFFLES = 200
N_DRAWS = 10000
MIN_FIXED = 30
_MODS = {}


def _load(e):
    if e not in _MODS:
        path = next((ROOT / "experiments").glob(f"{e}-*")) / "attack.py"
        spec = importlib.util.spec_from_file_location(f"frozen{e}", path)
        m = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = m
        spec.loader.exec_module(m)
        if hasattr(m, "ROOT"):
            m.ROOT = ROOT
        _MODS[e] = m
    return _MODS[e]


def _job(args):
    lo, hi = args
    G = _MODS["G"]
    routes, CI, PI, pidx, classes = G["routes"], G["CI"], G["PI"], G["pidx"], G["classes"]
    out = []
    for ri in range(lo, hi):
        r = routes[ri][4]
        land = np.array([r[i] for i in pidx])
        last, prs = {}, []
        for e, j in enumerate(land):
            s = j % P
            if s in last:
                prs.append((last[s], e))
            last[s] = e
        for ci, (pa, ca, beau) in enumerate(classes):
            C = CI[ca][:, land]
            f = (C + PI[pa]) % 26 if beau else (C - PI[pa]) % 26
            ok = np.ones(C.shape[0], dtype=bool)
            for x, y in prs:
                ok &= f[:, x] == f[:, y]
            for t in np.nonzero(ok)[0]:
                out.append((int(t), ri, ci, {int(land[e] % P): int(f[t, e]) for e in range(len(land))}))
    return out


def reading(text, route, cls, slots, ALPH):
    pa, ca, beau = cls
    A, Cc = ALPH[pa], ALPH[ca]
    out = []
    for i in range(N):
        j = route[i]
        s = j % P
        if s not in slots:
            out.append("?")
            continue
        c = Cc.index(text[j])
        out.append(A[(slots[s] - c) % 26] if beau else A[(c - slots[s]) % 26])
    return "".join(out)


def run(ctx):
    t0 = time.time()
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    m63 = _load("0263")
    from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
    from kryptos.plants import english_plant
    ALPH = {"std": STD, "kry": KRY}
    known = ctx.KNOWN
    places = sorted(known)
    pidx = [p - 1 for p in places]
    routes = m63.settings()
    classes = [(pa, ca, beau) for pa in ALPH for ca in ALPH for beau in (False, True)]
    k4 = ctx.K4
    rng = random.Random(2620)
    texts = [k4] + ["".join(rng.sample(k4, N)) for _ in range(N_SHUFFLES)]
    # 0263's plant, rebuilt with its seeds
    srcs = m63._load("0210").sources()
    k3 = srcs["K3 plain fwd"][1]
    prng = random.Random(2621)
    pt = english_plant(2622)
    pr = prng.randrange(len(routes)); pa, ca, beau = classes[prng.randrange(len(classes))]
    off = prng.randrange(len(k3) - 23)
    keyw = k3[off:off + 23]
    kn = prng.choice(("std", "kry"))
    kv = [ALPH[kn].index(ch) for ch in keyw]
    wh = routes[pr][4]
    moved = [""] * N
    for i, ch in enumerate(pt):
        moved[wh[i]] = ch
    pc = "".join(ALPH[ca][(kv[j % 23] - ALPH[pa].index(ch)) % 26] if beau else ALPH[ca][(ALPH[pa].index(ch) + kv[j % 23]) % 26]
                 for j, ch in enumerate(moved))
    texts.append(pc)
    CI = {an: np.array([[ALPH[an].index(ch) for ch in t] for t in texts], dtype=np.int64) for an in ALPH}
    PI = {an: np.array([ALPH[an].index(known[p]) for p in places], dtype=np.int64) for an in ALPH}
    _MODS["G"] = {"routes": routes, "CI": CI, "PI": PI, "pidx": pidx, "classes": classes}
    W = int(os.environ.get("K4_WORKERS", 8))
    step = max(1, len(routes) // (W * 8))
    chunks = [(i, min(i + step, len(routes))) for i in range(0, len(routes), step)]
    live = []
    ctx.progress(0, len(chunks), "route chunks")
    with mp.get_context("fork").Pool(W) as pool:
        for k, out in enumerate(pool.imap_unordered(_job, chunks)):
            live += out
            ctx.progress(k + 1, len(chunks), "route chunks")
    recs = {}
    for t, ri, ci, slots in live:
        r = reading(texts[t], routes[ri][4], classes[ci], slots, ALPH)
        free = "".join(c for i, c in enumerate(r, start=1) if i not in known and c != "?")
        q = ctx.english_score(free) if len(free) >= MIN_FIXED else None
        recs.setdefault(t, []).append({"route": list(routes[ri][:4]), "class": "/".join(map(str, classes[ci])), "reading": r,
                                       "fixed": len(free), "quad": q})
    ns = len(texts) - 1
    k4r = recs.get(0, [])
    best = lambda rs: max([x["quad"] for x in rs if x["quad"] is not None] or [-99.0])
    k4best = best(k4r)
    pool_ = [x for t in range(1, ns) for x in recs.get(t, [])]
    drng = random.Random(16600)
    n = len(k4r)
    draws = [best(drng.sample(pool_, n)) for _ in range(N_DRAWS)] if len(pool_) >= n and n else []
    p = (1 + sum(1 for d in draws if d >= k4best)) / (len(draws) + 1) if draws else None
    # judge: K4's top 5 and each shuffle's best, blind, one call
    k4top = sorted([x for x in k4r if x["quad"] is not None], key=lambda x: -x["quad"])[:5]
    sh_best = {}
    for t in range(1, ns):
        rs = [x for x in recs.get(t, []) if x["quad"] is not None]
        if rs:
            sh_best[t] = max(rs, key=lambda x: x["quad"])
    order = sorted({x["reading"] for x in k4top} | {x["reading"] for x in sh_best.values()})
    verdicts = dict(zip(order, ctx.judge(order))) if order else {}
    js = lambda r: (verdicts.get(r) or {}).get("score")
    for x in k4top:
        x["judge"] = js(x["reading"])
    jk4 = max([x["judge"] for x in k4top if x["judge"] is not None] or [None]) if k4top else None
    jsh = [js(x["reading"]) for x in sh_best.values()]
    jsh = [x for x in jsh if x is not None]
    # plant
    prs_ = recs.get(ns, [])
    ptrue = [x for x in prs_ if x["route"] == list(routes[pr][:4]) and x["class"] == "/".join(map(str, (pa, ca, beau)))]
    pright = None
    if ptrue:
        r = ptrue[0]["reading"]
        pright = sum(1 for i, c in enumerate(r) if c == pt[i]) / max(1, sum(1 for c in r if c != "?"))
    return {"candidates": [], "bounds": {
        "item": "F16.6-r", "routes": len(routes), "classes": len(classes), "period": P,
        "k4_settings": n, "shuffle_settings_pooled": len(pool_), "shuffles": N_SHUFFLES,
        "statistic": f"best quadgram per letter over a text's settings (known places excluded, at least {MIN_FIXED} letters fixed)",
        "k4_best": k4best, "count_matched_draws": len(draws), "p": round(p, 4) if p is not None else None, "flag": bool(p is not None and p < 0.05),
        "null_median": float(np.median(draws)) if draws else None,
        "judge": {"sent": len(order), "k4_best": jk4, "shuffles_best_max": max(jsh, default=None),
                  "shuffles_best_median": float(np.median(jsh)) if jsh else None,
                  "k4_above_every_shuffle": bool(jk4 is not None and all(jk4 > y for y in jsh))},
        "k4_top5": k4top, "plant": {"live": bool(ptrue), "right_fraction_of_fixed": pright},
        "exhaustive": True, "compute_seconds": round(time.time() - t0), "aws_cost_estimate_dollars": 0.2},
        "notes": f"K4 {n} settings, best quadgram {k4best:.3f}; count-matched p {p}; judge K4 {jk4} vs shuffles' best max {max(jsh, default=None)}; plant live {bool(ptrue)}, right {pright}"}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    return "\n".join(["F16.6-r: AMSCO route, then a 23-letter key from a chart (any letters).", "",
                      "  the 24 known letters fix the key in the slots they land in (carved place mod 23)",
                      "  every other carved letter in a fixed slot can be decrypted and carried back through the route",
                      "  the message is read with the rest left blank, and scored against scrambled copies' messages"])
