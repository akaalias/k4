"""Experiment: F16.4b. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f16.4b-line-keyed-schemes-on-dictionary-keyword-alphabets",
    "title": "F16.4b: a key that knows the carved lines: a repeating key of 1-26 with its own offset on each carved line, restarted at each line, or both, on every pair of dictionary keyword alphabets (208,064 each side, plain and KRYPTOS among them), both forms; exact fit counts against 50 shuffles, the forced key looked up as a word",
    "family": "16-simple-hand-methods",
    "parent": "0244-f14-two-dictionary-keyword-alphabets-and-a-key-word",
    "changed": (
        "F16.4b (issue #123). 0288 found no sign of the carved line in the small shifts (p 0.20, 0.28), so this row "
        "runs without a lead behind it (run more experiments, #100). 0244's exact pair index, with the same-slot "
        "checks replaced by the checks a line-keyed key leaves: (1) OFFSET: key[(q-1) mod L] plus an unknown offset "
        "per carved line (K4 places 1-4, 5-35, 36-66, 67-97); (2) RESTART: the key begins again at each carved line, "
        "no offset; (3) BOTH. Each check is a signed sum of forced keys that must be zero, and still splits into a "
        "cipher-side and a plain-side number, so the index works unchanged. On the 24 and on the 20 official "
        "letters. Before: 0088 (a shift per line plus a column word) and 0128 (restart per line), plain and KRYPTOS "
        "tables only. Strength aimed at: exact."
    ),
    "hypothesis_expert": (
        "C27(b) (the BERLIN chart's 31-character lines he counted on), A7 (one procedure for all 97 letters), C5(a). "
        "Quagmire IV with dictionary keyword alphabets P and C (kryptos.alphabets.keyword_mixed; 4.3 x 10^10 ordered "
        "pairs per form), added form k = C(c) - P(p) and Beaufort k = C(c) + P(p). Known places by carved line: "
        "22-34 on line 2, 64-66 on line 3, 67-74 on line 4. The consistency checks are the cycles of the graph "
        "whose nodes are key slots and lines and whose edges are known places; with E independent checks a random "
        "pair fits with chance 26^-E, so the space is decided where E is about 8 or more and counted elsewhere. "
        "Where 10,000 pairs or fewer fit, the forced key (relative to line 2's offset) is looked up among every "
        "rotation of every dictionary and puzzle word of the length, numbered on the standard, KRYPTOS, plain or "
        "cipher alphabet, any shift. Prediction basis: 0244 and 0275 found no key word with a plain repeating key."
    ),
    "hypothesis_eli5": (
        "Sanborn worked on charts with the text in lines of 31 letters. Perhaps the key word started again on each "
        "carved line, or each line was slid by its own amount. We test both on every pair of alphabets made from "
        "dictionary words and ask whether the key the known letters force is ever a word."
    ),
    "prediction": (
        "No key word on K4 or any shuffle. K4's fit counts inside its shuffles: cells where K4 is above all 50 no "
        "more than a shuffle shows against the other 49. Plants found 12 of 12."
    ),
    "method": (
        "1. For each model and key length, the known places as edges between key slots and carved lines; a spanning "
        "forest gives each slot's key as a signed sum of forced keys, and every other edge a check. 2. For every "
        "alphabet the checks' cipher-side and plain-side numbers; pairs with equal numbers fit (index, exact). "
        "3. Count per cell; where at most 10,000 pairs fit, read the forced key and look it up as a word. 4. K4, 50 "
        "shuffles, 12 plants (random dictionary alphabets and key word, key lengths 7-14, the three models)."
    ),
    "walkthrough": (
        "1. Write K4 in its carved lines and mark the known letters: 22-34 on the second line, 64-66 on the third, 67-74 on the fourth. "
        "2. Choose a key length, say 9, and write the key under each line, starting again at each line's first letter. "
        "3. Two known letters under the same key letter must give the same key: for a pair of alphabets, that is a check. "
        "4. With an offset per line, compare differences instead: two pairs of known letters that straddle the same two lines must differ by the same amount. "
        "5. Keep the alphabet pairs that pass every check and read the key they force; look it up in the dictionary."
    ),
    "expected_minutes": 20,
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
STD = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KRY = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
LMAX_L = 26
WORD_MAX = 24
N_COPIES = 50
LIST_CAP = 10000
SEED = 16402
MODELS = ("offset", "restart", "both")
LINE_START = {1: -26, 2: 5, 3: 36, 4: 67}     # K4 place of each carved line's first column (line 1: ?OBKR ends it)
OFFICIAL = set(range(26, 35)) | set(range(64, 75))
PLANT_SPECS = [(m, L) for m in MODELS for L in (7, 9, 12, 14)]
_G = {}


def keyed(word):
    seen = []
    for c in word:
        if c not in seen:
            seen.append(c)
    return "".join(seen) + "".join(c for c in STD if c not in seen)


def alphabets():
    words = [w.strip().upper() for w in (ROOT / "kryptos" / "data" / "words.txt").read_text().split()]
    alphas = {STD: "std", KRY: "KRYPTOS"}
    for w in words:
        if len(w) >= 4 and w.isalpha():
            alphas.setdefault(keyed(w), w)
    names = list(alphas.values())
    A = list(alphas.keys())
    arr = np.frombuffer("".join(A).encode(), dtype=np.uint8).reshape(len(A), 26) - 65
    pos = np.zeros((len(A), 26), dtype=np.int16)
    pos[np.repeat(np.arange(len(A)), 26), arr.ravel()] = np.tile(np.arange(26, dtype=np.int16), len(A))
    return A, names, pos


def key_words(vocabulary):
    words = [w.strip().upper() for w in (ROOT / "kryptos" / "data" / "words.txt").read_text().split()]
    puzzle = sorted({w.upper() for w in vocabulary if w.isalpha()})
    rots = {}
    for w in [x for x in words if x.isalpha() and 3 <= len(x) <= WORD_MAX] + [x for x in puzzle if 2 <= len(x) <= WORD_MAX]:
        s = rots.setdefault(len(w), {})
        for r in range(len(w)):
            s.setdefault(w[r:] + w[:r], (w, r))
    return {L: (list(d.keys()), list(d.values())) for L, d in rots.items()}


def line_of(q):
    return 1 if q <= 4 else 2 if q <= 35 else 3 if q <= 66 else 4


def slot_of(q, L, model):
    return ((q - 1) if model == "offset" else (q - LINE_START[line_of(q)])) % L


def node_of(q, model):
    return 0 if model == "restart" else line_of(q)


def structure(L, model, places):
    """-> checks (each a dict place -> coefficient, the signed sum of forced keys must be 0 mod 26) and
    anchored (slot -> dict place -> coefficient: the slot's key relative to line 2's offset)."""
    edges = [(("s", slot_of(q, L, model)), ("l", node_of(q, model)), q) for q in places]
    adj = {}
    for s, l, q in edges:
        adj.setdefault(s, []).append((l, q)); adj.setdefault(l, []).append((s, q))
    expr, used, checks, anchored_nodes = {}, set(), [], set()
    root0 = ("l", 0 if model == "restart" else 2)
    roots = [root0] + sorted(n for n in adj if n[0] == "l" and n != root0) + sorted(n for n in adj if n[0] == "s")
    for root in roots:
        if root in expr or root not in adj:
            continue
        expr[root] = {}
        stack = [root]
        comp = [root]
        while stack:
            u = stack.pop()
            for v, q in adj[u]:
                if q in used:
                    continue
                used.add(q)
                # k_q = expr[slot] + expr[line]
                if v not in expr:
                    e = {q: 1}
                    for qq, cf in expr[u].items():
                        e[qq] = e.get(qq, 0) - cf
                    expr[v] = e; stack.append(v); comp.append(v)
                else:
                    e = {q: 1}
                    for qq, cf in expr[u].items():
                        e[qq] = e.get(qq, 0) - cf
                    for qq, cf in expr[v].items():
                        e[qq] = e.get(qq, 0) - cf
                    e = {qq: cf for qq, cf in e.items() if cf % 26}
                    if e:
                        checks.append(e)
        if root == root0:
            anchored_nodes = set(comp)
    anchored = {n[1]: expr[n] for n in anchored_nodes if n[0] == "s"}
    return checks, anchored


def combo(vals, exprs, col):
    """vals: N x 24 positions; exprs: list of dict place->coef -> N x len(exprs), mod 26"""
    out = np.zeros((vals.shape[0], len(exprs)), dtype=np.int16)
    for j, e in enumerate(exprs):
        for q, cf in e.items():
            out[:, j] += cf * vals[:, col[q]]
    return out % 26


def kstream(key):
    KA = {"std": STD, "kry": KRY, "plain": key["pa"], "cipher": key["ca"]}[key["ka"]]
    w, L = key["word"], len(key["word"])
    off = key.get("offsets", {})
    return [(KA.index(w[slot_of(q, L, key["model"])]) + key["shift"] + (off.get(str(line_of(q)), 0) if key["model"] != "restart" else 0)) % 26
            for q in range(1, N + 1)]


def encrypt(plaintext, key):
    PA, CA, k = key["pa"], key["ca"], kstream(key)
    if key["form"] == "added":
        return "".join(CA[(PA.index(p) + k[i]) % 26] for i, p in enumerate(plaintext))
    return "".join(CA[(k[i] - PA.index(p)) % 26] for i, p in enumerate(plaintext))


def decrypt(ct, key):
    PA, CA, k = key["pa"], key["ca"], kstream(key)
    if key["form"] == "added":
        return "".join(PA[(CA.index(c) - k[i]) % 26] for i, c in enumerate(ct))
    return "".join(PA[(k[i] - CA.index(c)) % 26] for i, c in enumerate(ct))


def search(text, known, sets):
    A, pos = _G["A"], _G["pos"]
    out = {"fits": {}, "matches": [], "uncounted_words": []}
    for sname, places in sets:
        col = {q: e for e, q in enumerate(places)}
        cv = pos[:, [ord(text[q - 1]) - 65 for q in places]]
        pv = pos[:, [ord(known[q]) - 65 for q in places]]
        for model in MODELS:
            for L in range(1, LMAX_L + 1):
                checks, anchored = _G["struct"][(sname, model, L)]
                cover = sorted(anchored)
                if not checks:
                    for form in ("added", "beaufort"):
                        out["fits"][(sname, model, L, form)] = len(A) ** 2
                    continue
                cvec = combo(cv, checks, col).astype(np.uint8)
                pvec = combo(pv, checks, col)
                cidx = {}
                for a, kb in enumerate(r.tobytes() for r in cvec):
                    cidx.setdefault(kb, []).append(a)
                sizes = {kb: len(v) for kb, v in cidx.items()}
                for form in ("added", "beaufort"):
                    pk = [r.tobytes() for r in (pvec if form == "added" else (-pvec) % 26).astype(np.uint8)]
                    n = int(sum(sizes.get(kb, 0) for kb in pk))
                    out["fits"][(sname, model, L, form)] = n
                    if n == 0 or L not in _G["rots"] or len(cover) < 3:
                        continue
                    if n > LIST_CAP:
                        out["uncounted_words"].append((sname, model, L, form, n))
                        continue
                    aexpr = [anchored[s] for s in cover]
                    for p_a, kb in enumerate(pk):
                        for c_a in cidx.get(kb, ()):
                            kq = {q: (int(cv[c_a, col[q]]) - int(pv[p_a, col[q]])) % 26 if form == "added"
                                  else (int(cv[c_a, col[q]]) + int(pv[p_a, col[q]])) % 26 for q in places}
                            k = np.array([sum(cf * kq[q] for q, cf in e.items()) % 26 for e in aexpr])
                            match_key_word(sname, model, L, form, p_a, c_a, cover, k, out)
    return out


def match_key_word(sname, model, L, form, p_a, c_a, cover, k, out):
    A, pos = _G["A"], _G["pos"]
    d = (k - k[0]) % 26
    strs, src = _G["rots"][L]
    sub = _G["rotmat"][L][:, cover]
    for ka in ("std", "kry", "plain", "cipher"):
        lut = {"std": _G["lut_std"], "kry": _G["lut_kry"], "plain": pos[p_a], "cipher": pos[c_a]}[ka]
        v = lut[sub]
        dv = (v - v[:, :1]) % 26
        for h in np.nonzero((dv == d).all(axis=1))[0][:20]:
            w, r = src[h]
            out["matches"].append({"set": sname, "model": model, "L": L, "form": form, "pa": A[p_a], "ca": A[c_a],
                                   "pa_word": _G["names"][p_a], "ca_word": _G["names"][c_a], "ka": ka, "word": w, "start": r,
                                   "slots_checked": len(cover), "shift": int((k[0] - v[h, 0]) % 26)})


def _job(args):
    tid, text, known, sets = args
    return tid, search(text, known, sets)


def run(ctx):
    import multiprocessing as mp
    t0 = time.time()
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    A, names, pos = alphabets()
    _G.update(A=A, names=names, pos=pos, rots=key_words(ctx.vocabulary))
    _G["rotmat"] = {L: np.array([[ord(c) - 65 for c in s] for s in strs], dtype=np.int16) for L, (strs, _) in _G["rots"].items()}
    _G["lut_std"] = np.arange(26, dtype=np.int16)
    _G["lut_kry"] = np.array([KRY.index(c) for c in STD], dtype=np.int16)
    k4, known = ctx.K4, dict(ctx.KNOWN)
    p24 = sorted(known); p20 = sorted(q for q in known if q in OFFICIAL)
    sets = [("24", p24), ("20", p20)]
    _G["struct"] = {(sn, m, L): structure(L, m, pl) for sn, pl in sets for m in MODELS for L in range(1, LMAX_L + 1)}
    n_checks = {f"{sn}/{m}/{L}": len(_G["struct"][(sn, m, L)][0]) for sn, _ in sets for m in MODELS for L in range(1, LMAX_L + 1)}
    # self-check of the structure: a random key stream of each model satisfies every check; a random stream does not
    rng = random.Random(SEED)
    for (sn, m, L), (checks, anchored) in _G["struct"].items():
        key = [rng.randrange(26) for _ in range(L)]; off = {1: rng.randrange(26), 2: rng.randrange(26), 3: rng.randrange(26), 4: rng.randrange(26)}
        ks = {q: (key[slot_of(q, L, m)] + (off[line_of(q)] if m != "restart" else 0)) % 26 for q in p24}
        assert all(sum(cf * ks[q] for q, cf in e.items()) % 26 == 0 for e in checks), (sn, m, L)
        base = off[2] if m != "restart" else 0
        assert all((sum(cf * ks[q] for q, cf in e.items()) - key[s] - base) % 26 == 0 for s, e in anchored.items()), (sn, m, L)
    texts = [("k4", k4, known, sets)]
    for i in range(N_COPIES):
        s = list(k4); random.Random(SEED * 100 + i).shuffle(s); texts.append((f"copy{i}", "".join(s), known, sets))
    from kryptos.plants import english_plant
    plants = {}
    for j, (model, L) in enumerate(PLANT_SPECS):
        prng = random.Random(SEED + 500 + j)
        pt = english_plant(SEED + 500 + j)
        strs, src = _G["rots"][L]
        w, r = src[prng.randrange(len(src))]
        key = {"pa": A[prng.randrange(2, len(A))], "ca": A[prng.randrange(2, len(A))], "form": prng.choice(("added", "beaufort")),
               "ka": prng.choice(("std", "kry", "plain", "cipher")), "word": w, "shift": prng.randrange(26), "model": model,
               "offsets": {str(l): prng.randrange(26) for l in (1, 2, 3, 4)}}
        ct = encrypt(pt, key)
        assert decrypt(ct, key) == pt
        pid = f"plant{j}"
        plants[pid] = {"key": key, "pt": pt, "L": L}
        texts.append((pid, ct, {q: pt[q - 1] for q in p24}, [("24", p24)]))
    saved = getattr(ctx, "saved", {}) or {}
    res = {}
    for tid, v in saved.items():
        res[tid] = {"fits": {tuple(k.split("|")[:3]) + (k.split("|")[3],): n for k, n in v["fits"].items()}, "matches": v["matches"], "uncounted_words": v["uncounted_words"]}
        res[tid]["fits"] = {(a, b, int(c), d): n for (a, b, c, d), n in res[tid]["fits"].items()}
    todo = [t for t in texts if t[0] not in res]
    workers = int(os.environ.get("K4_WORKERS", 8))
    ctx.progress(len(res), len(texts), "texts searched")
    with mp.get_context("fork").Pool(workers) as pool:
        for tid, out in pool.imap_unordered(_job, todo, chunksize=1):
            res[tid] = out
            ctx.save(tid, {"fits": {"|".join(str(x) for x in k): n for k, n in out["fits"].items()}, "matches": out["matches"],
                           "uncounted_words": [list(x) for x in out["uncounted_words"]]})
            ctx.progress(len(res), len(texts), "texts searched")
    copies = [res[f"copy{i}"] for i in range(N_COPIES)]
    cells, above = {}, []
    keys = [(sn, m, L, f) for sn, _ in sets for m in MODELS for L in range(1, LMAX_L + 1) for f in ("added", "beaufort")]
    for kk in keys:
        k4n = res["k4"]["fits"][kk]
        cv = sorted(c["fits"][kk] for c in copies)
        ge = sum(1 for x in cv if x >= k4n)
        cells["/".join(str(x) for x in kk)] = {"k4": k4n, "copies_min_median_max": [cv[0], cv[len(cv) // 2], cv[-1]], "copies_at_or_above": ge,
                                                "checks": n_checks[f"{kk[0]}/{kk[1]}/{kk[2]}"]}
        if ge == 0 and k4n > 0:
            above.append("/".join(str(x) for x in kk))
    null = []
    for i, c in enumerate(copies):
        null.append(sum(1 for kk in keys if c["fits"][kk] > 0 and all(o["fits"][kk] < c["fits"][kk] for j, o in enumerate(copies) if j != i)))
    shortest = {}
    for sn, _ in sets:
        for m in MODELS:
            def first(r):
                return next((L for L in range(1, LMAX_L + 1) if r["fits"][(sn, m, L, "added")] or r["fits"][(sn, m, L, "beaufort")]), None)
            cs = sorted(first(c) or 99 for c in copies)
            shortest[f"{sn}/{m}"] = {"k4": first(res["k4"]), "copies_min_median_max": [cs[0], cs[len(cs) // 2], cs[-1]]}
    found = {}
    for pid, p in plants.items():
        k = p["key"]
        hit = [m for m in res[pid]["matches"] if m["model"] == k["model"] and m["L"] == p["L"] and m["form"] == k["form"]
               and m["pa"] == k["pa"] and m["ca"] == k["ca"] and m["word"][m["start"]:] + m["word"][:m["start"]] == k["word"] and m["ka"] == k["ka"]]
        found[pid] = {"model": k["model"], "L": p["L"], "form": k["form"], "word": k["word"], "found": bool(hit),
                      "fits_in_its_cell": res[pid]["fits"][("24", k["model"], p["L"], k["form"])], "matches_all_cells": len(res[pid]["matches"]),
                      "checks": n_checks[f"24/{k['model']}/{p['L']}"]}
    n_found = sum(1 for v in found.values() if v["found"])
    km = {"k4": len(res["k4"]["matches"]), "copies": sorted(len(c["matches"]) for c in copies)}
    bounds = {
        "item": "F16.4b", "alphabets": len(A), "alphabet_pairs_per_form": len(A) ** 2, "models": list(MODELS), "key_lengths": [1, LMAX_L],
        "lines": "K4 places 1-4, 5-35, 36-66, 67-97", "checks_per_cell": n_checks,
        "cells": cells, "cells_looked_at": len(keys), "cells_k4_above_all_copies": above,
        "null_cells_above_all_others_per_copy": sorted(null),
        "shortest_fitting_length": shortest,
        "key_word_matches": km, "k4_matches": res["k4"]["matches"][:50],
        "k4_cells_over_the_list_cap": [list(x) for x in res["k4"]["uncounted_words"]], "list_cap": LIST_CAP,
        "plants": found, "plants_found": f"{n_found} of {len(found)}",
        "controls": f"{N_COPIES} shuffles of K4 with the known letters kept in place", "exhaustive": True,
        "compute_seconds": round(time.time() - t0), "aws_cost_estimate_dollars": 0.2,
        "not_covered": "key words where more than 10,000 alphabet pairs fit (listed); line offsets with a non-repeating key; lines other than the carved ones",
    }
    notes = (f"key-word matches K4 {km['k4']}, copies max {km['copies'][-1]}; cells K4 above all copies {len(above)} of {len(keys)} "
             f"(a copy against the others: median {sorted(null)[len(null) // 2]}, max {max(null)}); plants {n_found}/{len(found)}")
    # a restart-model match fixes every letter (no offsets): those are candidates; the copies' best are the controls
    from kryptos.scorer import free_text

    def readings(text, matches):
        out = []
        for m in matches[:50]:
            if m["model"] != "restart":
                continue
            key = {"pa": m["pa"], "ca": m["ca"], "form": m["form"], "ka": m["ka"], "shift": m["shift"], "model": "restart",
                   "word": m["word"][m["start"]:] + m["word"][:m["start"]]}
            out.append((decrypt(text, key), key))
        return out
    cands = [{"plaintext": pt, "key": key} for pt, key in readings(k4, res["k4"]["matches"])]
    controls = []
    for i in range(N_COPIES):
        sc = [ctx.english_score(free_text(pt)) for pt, _ in readings(texts[1 + i][1], copies[i]["matches"])]
        controls.append(max(sc) if sc else -10.0)
    return {"candidates": cands, "controls": controls, "bounds": bounds, "notes": notes}


def worked_example(ctx, key):
    lines = ["key length 9, restart at each carved line: the key letter each known place falls under", "", "place line column slot known carved"]
    for q in sorted(ctx.KNOWN):
        lines.append(f"{q:>5} {line_of(q):>4} {q - LINE_START[line_of(q)]:>6} {slot_of(q, 9, 'restart'):>4} {ctx.KNOWN[q]:>5} {ctx.K4[q - 1]:>6}")
    return "\n".join(lines)
