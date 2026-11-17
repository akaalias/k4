"""Experiment: F16.1b-s. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f16.1b-s-two-dictionary-keyword-alphabets-with-slips",
    "title": "F16.1b-s: 0275 (two dictionary keyword alphabets, every pair, key lengths 1-26, the 20 official letters) with one or two of the 20 known letters slipped: every drop set, the key word screened where the fitting pairs can be listed; K4 against 20 shuffles, 6 plants with slips",
    "family": "16-simple-hand-methods",
    "parent": "0275-f16.1b-two-dictionary-keyword-alphabets-on-the-20-official-letters",
    "changed": (
        "F16.1b-s (issue #123): 0275's search, imported unchanged (0244's index and matcher, 0275's hash screen), run on "
        "the 20 official letters less each set of 1 or 2 places (20 + 190 drop sets). Where a length and form has more "
        "than 5 million fitting pairs the pairs are counted, not listed, and the key word is not checked there (the reach, "
        "reported per cell)."
    ),
    "hypothesis_expert": (
        "As 0275 and 0244 (C4(a), C5; Quagmire IV with two keyword-mixed alphabets from the dictionary and a key word), "
        "with A1's slip at a known place (Sanborn 2005, 'Saying I was sloppy'; K2's carved errors, 01-facts.md) and "
        "EAST set aside (#124). A slip at known place q removes q's equation; the key word still has to match the forced "
        "key on every slot the remaining places cover. With 18 or 19 places the slots covered at lengths 3-16 still leave "
        "word matches far below one per text by chance; at the long lengths the fitting pairs run to billions and only "
        "counts are possible."
    ),
    "hypothesis_eli5": (
        "Experiment 275 tried every pair of dictionary-word alphabets with a key word on the 20 letters Sanborn published. "
        "If he miscopied one or two of those letters, it would have missed. Here we drop each one and each pair in turn "
        "and look again for a key word."
    ),
    "prediction": (
        "No key word on K4 at any drop set where the screen reaches; shuffles the same; plants (one or two slips) found "
        "6 of 6; fit counts inside the shuffles. Zero candidates unless a key word fits."
    ),
    "method": (
        "1. 0275's alphabets and word rotations. 2. For each text and each drop set of 1 or 2 of the 20 places: 0244's "
        "pair index over the remaining places, lengths 1-26, both forms; pairs listed when 5 million or fewer, then 0275's "
        "screen and 0244's matcher. 3. K4, 20 shuffles, 6 plants (two random dictionary alphabets, a dictionary key word, "
        "1 or 2 letters changed at official places). 4. Matches and counts against the shuffles."
    ),
    "walkthrough": (
        "1. Strike out one of the 20 known letters, say the K at 74, as a slip. "
        "2. Repeat 0275's test on the other 19: for each pair of word alphabets, the same-slot distances must agree. "
        "3. Read the key letters the pair forces and look for a word. "
        "4. Do this for each letter struck out, and each pair struck out, on the carving and on scrambled copies."
    ),
    "expected_minutes": 150,
}

import itertools
import multiprocessing as mp
import os
import random
import sys
import time
import types
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
N = 97
OFFICIAL = tuple(range(26, 35)) + tuple(range(64, 75))
LCOUNT, WMAX = 26, 23
CAP = 5_000_000
N_COPIES = 20
SEED = 16250
_G = {}


def F():
    """0275's attack.py, unchanged (it loads 0244's)."""
    if "f" not in _G:
        import importlib.util
        path = next((ROOT / "experiments").glob("0275-*")) / "attack.py"
        spec = importlib.util.spec_from_file_location("frozen0275", path)
        m = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = m
        spec.loader.exec_module(m)
        m.ROOT = ROOT
        _G["f"] = m
    return _G["f"]


def pairs_capped(known, text, L):
    f = F(); m = f.frozen()
    pos = m._G["pos"]
    places = sorted(known)
    pl_index = {q: e for e, q in enumerate(places)}
    ci = np.array([ord(text[q - 1]) - 65 for q in places])
    pi = np.array([ord(known[q]) - 65 for q in places])
    sl = m.slots_of(L, places)
    prs = [(v[0], u) for v in sl.values() for u in v[1:]]
    out = {}
    if not prs:
        return {fm: (len(pos) ** 2, None, None) for fm in ("added", "beaufort")}, sl
    a_idx = np.array([pl_index[x] for x, _ in prs]); b_idx = np.array([pl_index[y] for _, y in prs])
    cvec = (pos[:, ci[a_idx]] - pos[:, ci[b_idx]]) % 26
    pvec = (pos[:, pi[a_idx]] - pos[:, pi[b_idx]]) % 26
    cidx = {}
    for a, kb in enumerate(r.tobytes() for r in cvec.astype(np.uint8)):
        cidx.setdefault(kb, []).append(a)
    for fm in ("added", "beaufort"):
        pv = pvec if fm == "added" else (-pvec) % 26
        pk = [r.tobytes() for r in pv.astype(np.uint8)]
        n = int(sum(len(cidx.get(kb, ())) for kb in pk))
        if L > WMAX or n > CAP:
            out[fm] = (n, None, None)
            continue
        P, C = [], []
        for p_a, kb in enumerate(pk):
            partners = cidx.get(kb)
            if partners:
                P.extend([p_a] * len(partners)); C.extend(partners)
        out[fm] = (n, np.array(P, dtype=np.int64), np.array(C, dtype=np.int64))
    return out, sl


def job(args):
    tid, text, known, D = args
    f = F(); m = f.frozen()
    kn = {q: c for q, c in known.items() if q not in D}
    res = {"fits": {}, "unscreened": [], "matches": []}
    for L in range(1, LCOUNT + 1):
        fs, sl = pairs_capped(kn, text, L)
        cover = sorted(sl); first = {s: sl[s][0] for s in cover}
        for fm, (n, P, C) in fs.items():
            res["fits"][f"{L}/{fm}"] = n
            if P is None:
                if n and L <= WMAX:
                    res["unscreened"].append(f"{L}/{fm}")
                continue
            hits = f.word_hits(L, fm, P, C, cover, first, text, kn)
            out = {"matches": []}
            for i in hits[:5000]:
                m.match_key_word(L, fm, int(P[i]), int(C[i]), cover, first, text, kn, out)
            for x in out["matches"][:50]:
                x["drop"] = list(D)
                res["matches"].append(x)
    return tid, list(D), res


def run(ctx):
    me = sys.modules.get(__name__)
    if getattr(me, "job", None) is not job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    t0 = time.time()
    f = F(); m = f.frozen()
    f.setup(ctx.vocabulary)
    A = m._G["A"]
    k20 = {q: ctx.KNOWN[q] for q in OFFICIAL}
    rng = random.Random(SEED)
    texts = [("k4", ctx.K4, k20)]
    for i in range(N_COPIES):
        s = list(ctx.K4); rng.shuffle(s); texts.append((f"copy{i}", "".join(s), k20))
    carter = "".join(c for c in (ROOT / "knowledge" / "sources" / "carter-1923-tomb-of-tutankhamen-vol1.txt").read_text(errors="ignore").upper() if "A" <= c <= "Z")
    plants = {}
    for j, (L, k) in enumerate(((14, 1), (16, 2), (18, 1), (20, 2), (21, 1), (22, 2))):
        strs, src = m._G["rots"][L]
        o = rng.randrange(len(carter) // 2, len(carter) - N)
        pt = carter[o:o + N]
        w, r = src[rng.randrange(len(src))]
        key = {"pa": A[rng.randrange(2, len(A))], "ca": A[rng.randrange(2, len(A))], "form": rng.choice(("added", "beaufort")),
               "ka": rng.choice(("std", "kry", "plain", "cipher")), "word": w, "start": r, "shift": rng.randrange(26)}
        ct = list(m.encrypt(pt, key))
        D = sorted(rng.sample(OFFICIAL, k))
        for q in D:
            ct[q - 1] = rng.choice([c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if c != ct[q - 1]])
        pid = f"plant{j}"
        plants[pid] = {"L": L, "key": key, "slips": D, "pt": pt}
        texts.append((pid, "".join(ct), {q: pt[q - 1] for q in OFFICIAL}))
    drops = [D for k in (1, 2) for D in itertools.combinations(OFFICIAL, k)]
    work = [(tid, t, kn, D) for tid, t, kn in texts for D in drops]
    saved = getattr(ctx, "saved", {}) or {}
    res = {}
    for tid, t, kn, D in work:
        key = f"{tid}|{'-'.join(map(str, D))}"
        if key in saved:
            res[key] = saved[key]
    todo = [w for w in work if f"{w[0]}|{'-'.join(map(str, w[3]))}" not in res]
    todo.sort(key=lambda w: w[0] != "k4")
    W = int(os.environ.get("K4_WORKERS", 8))
    ctx.progress(len(res), len(work), "texts x drop sets")
    with mp.get_context("fork").Pool(W) as pool:
        for tid, D, out in pool.imap_unordered(job, todo, chunksize=1):
            key = f"{tid}|{'-'.join(map(str, D))}"
            res[key] = out
            ctx.save(key, out)
            ctx.progress(len(res), len(work), "texts x drop sets")

    def of(tid):
        return [v for k, v in res.items() if k.split("|")[0] == tid]
    k4m = [x for v in of("k4") for x in v["matches"]]
    cm = [sum(len(v["matches"]) for v in of(f"copy{i}")) for i in range(N_COPIES)]
    cells = [f"{L}/{fm}" for L in range(1, LCOUNT + 1) for fm in ("added", "beaufort")]
    fits = {}
    for c in cells:
        kv = sum(1 for v in of("k4") if v["fits"][c])
        cv = [sum(1 for v in of(f"copy{i}") if v["fits"][c]) for i in range(N_COPIES)]
        fits[c] = {"k4_drop_sets_fitting": kv, "copies_median": float(np.median(cv)), "copies_max": max(cv),
                   "p": round((1 + sum(1 for x in cv if x >= kv)) / (N_COPIES + 1), 3) if kv else None,
                   "k4_unscreened_drop_sets": sum(1 for v in of("k4") if c in v["unscreened"])}
    found = {}
    for pid, p in plants.items():
        k = p["key"]
        hit = any(x["L"] == p["L"] and x["pa"] == k["pa"] and x["ca"] == k["ca"] and x["form"] == k["form"]
                  and sum(a == b for a, b in zip(m.decrypt(texts[[t[0] for t in texts].index(pid)][1], m.key_of(x)), p["pt"])) >= N - 2
                  for v in of(pid) for x in v["matches"])
        found[pid] = {"L": p["L"], "slips": p["slips"], "found": bool(hit)}
    cands = [{"plaintext": m.decrypt(ctx.K4, m.key_of(x)), "key": {**m.key_of(x), "slips_dropped": x["drop"]}} for x in k4m[:100]]
    bounds = {"item": "F16.1b-s", "drop_sets": len(drops), "known_places": list(OFFICIAL), "cap_pairs_listed": CAP,
              "key_word_check_lengths": [3, WMAX], "fitting": fits,
              "key_word_matches": {"k4": len(k4m), "copies": cm}, "k4_matches": k4m[:50],
              "plants": found, "plants_found": sum(v["found"] for v in found.values()),
              "copies": N_COPIES, "compute_seconds": round(time.time() - t0), "exhaustive": "yes where pairs are listed; cells above the cap counted only (k4_unscreened_drop_sets)",
              "aws_cost_estimate_dollars": 2.0}
    return {"candidates": cands, "bounds": bounds,
            "notes": f"{len(drops)} drop sets; key-word matches K4 {len(k4m)}, copies max {max(cm)}; plants {bounds['plants_found']}/{len(found)}"}


def encrypt(plaintext, key):
    out = list(F().frozen().encrypt(plaintext, {k: v for k, v in key.items() if k != "slips_dropped"}))
    return "".join(out)


def worked_example(ctx, key):
    return F().worked_example(ctx, key)
