"""Experiment: F16.1b-s-r. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f16.1b-s-r-length-19-one-slip-from-two-keyword-alphabets",
    "title": "F16.1b-s-r: 0282's edge at key length 19 (K4 one slip from fitting two dictionary keyword alphabets): the count against 1,000 fresh shuffles and against stand-ins that keep the R-to-P repeat at 28 and 66; K4's one-slip settings read with the key free against 1,000 copies that keep the 20 official places; plants with one slip",
    "family": "16-simple-hand-methods",
    "parent": "0282-f16.1b-s-two-dictionary-keyword-alphabets-with-slips",
    "changed": (
        "F16.1b-s-r (issue #123). 0282 found K4 fitting a pair of dictionary keyword alphabets at key length 19 in 200 of "
        "210 drop sets of one or two of the 20 official letters, its 20 shuffles in at most 39 (p 0.048, both forms). "
        "Here, length 19 only: (1) the same count for 1,000 fresh shuffles, for 300 stand-ins that keep the carved "
        "letters at 28 and 66 (R to P twice, 38 = 2 x 19 apart: one of the nine checks at 19 is then free, as on K4), "
        "and for 300 that also keep 32 and 70 (A to K, C to M: the same shift on the plain table); (2) every setting K4 "
        "fits with one letter dropped, the key free (a chart key, #124): the 11 forced key letters read 33 unknown "
        "letters in three runs of 11; quadgram score of the best setting against the same settings on 1,000 copies "
        "that keep the 20 official places and shuffle the other 77; the judge on the tops. Strength aimed at: sampled."
    ),
    "hypothesis_expert": (
        "C27(c) and C1(c) (two keyword-mixed alphabets, Quagmire IV, a repeating key), C17 and A1 (one enciphering slip, "
        "as K2 has; 12-assumptions.md), the revised criteria (#124: a chart key, a named slip). Cipher: c = CA[PA^-1(p) + "
        "k_(i mod 19)] (added) or CA[k - PA^-1(p)] (Beaufort), PA and CA keyword alphabets of 208,064 dictionary and puzzle "
        "words, key free. At length 19 the official runs 26-34 and 64-72 share key slots 6-14 (nine checks), 73 and 74 sit "
        "alone in slots 15 and 16. A true period-19 system predicts the R/P repeat at 28 and 66 (same slot, same plain "
        "letter). 0123/0124 put the repeat at about 1 in 40 by chance; 0148 found K1/K2's own tables one slip (at 33) from "
        "fitting, with a decider too weak to read it. Tests: counts (drop sets with a fitting pair, per form; one-slip "
        "settings) against plain shuffles (replication of 0282) and against repeat-keeping stand-ins (the fair null: is "
        "there more than the repeat?); readings (max over K4's one-slip settings of the mean log10 quadgram probability "
        "over the three 11-letter runs at places 7-17, 45-55, 83-93) against kept-place copies under the same settings. "
        "Flag lines, set before the run: counts against the repeat-keeping stand-ins p < 0.01; reading p < 0.01. "
        "Plants: English with the known words, two random keyword alphabets, a random 19-letter key, one slip at a "
        "paired official place; found when the planted pair is listed, ranks first among the plant's settings and beats "
        "every one of the plant's 1,000 kept-place copies."
    ),
    "hypothesis_eli5": (
        "With a key 19 letters long, the two known stretches of K4 sit exactly under the same key letters, and K4 comes "
        "within one wrong letter of fitting a cipher built from two keyword alphabets (an alphabet that starts with a "
        "word and goes on with the unused letters). Scrambled copies rarely come that close. Part of the reason is known: "
        "the letter R turns into P at two places 38 apart. We check whether there is more to it than that, and we read "
        "the letters each near-fit would give, against scrambled copies read the same way."
    ),
    "prediction": (
        "Against plain shuffles K4's count stays rare (p between 0.01 and 0.06); against stand-ins that keep the R/P "
        "repeat it is ordinary (p above 0.05). K4's best one-slip reading scores inside its kept-place copies (p above "
        "0.05) and the judge gives it no more than the copies' tops. Plants found at least 6 of 8. No candidate (8 of 19 "
        "key letters stay open)."
    ),
    "method": (
        "1. 0282's pair index (0275's, 0244's alphabets), key length 19 only, for each text and each of the 210 drop sets "
        "of one or two official letters: the number of fitting alphabet pairs per form; one-letter drops listed. "
        "2. Texts: K4; 1,000 shuffles; 300 shuffles keeping the carved letters at 28, 66; 300 keeping 28, 66, 32, 70; 8 plants. "
        "3. Counts: drop sets fitting per form, one-slip settings; p of K4 against each set of stand-ins. "
        "4. Readings: for each one-slip setting (form, alphabets, dropped place) the key letter of each slot 6-16 from the "
        "remaining known letter there; decrypt places 7-17, 45-55, 83-93; score by quadgrams. K4's best against the best "
        "of each of 1,000 kept-place copies (20 official places kept, 77 shuffled) under the same settings. "
        "5. Judge: K4's top 5 readings and the top reading of each of the first 100 kept-place copies, one call, '?' for open letters. "
        "6. Plants: the same, each against its own 1,000 kept-place copies."
    ),
    "walkthrough": (
        "1. Write K4 in rows of 19: places 26-34 fall under places 64-72, column for column. "
        "2. Pick two keyword alphabets, say one from FOREST for the cipher side and one from BINDERY for the plain side. "
        "3. In each column the two known pairs must need the same key letter; count the columns where they do not. "
        "4. If exactly one column fails, call one of its two carved letters a slip and take the key letter from the other. "
        "5. Columns 7-17 now have key letters: decrypt the three other rows of those columns (places 7-17, 45-55, 83-93). "
        "6. Score those 33 letters as English; repeat for every pair of alphabets that comes this close. "
        "7. Do the same on copies of K4 whose other 77 letters are shuffled, and compare the best scores."
    ),
    "expected_minutes": 130,
}

import itertools
import multiprocessing as mp
import os
import random
import sys
import types
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
N = 97
L = 19
OFFICIAL = tuple(range(26, 35)) + tuple(range(64, 75))
N_SHUF, N_RP, N_RPAM = 1000, 300, 300
N_KEPT = 1000
N_PLANTS = 8
SEED = 16400
RUNS = ((7, 17), (45, 55), (83, 93))            # places read, 1-based, slots 6-16
LIST_CAP = 4000
N_JUDGE_COPIES = 100
_G = {}


def A282():
    """0282's attack.py, unchanged (it loads 0275's, which loads 0244's)."""
    if "a" not in _G:
        import importlib.util
        path = next((ROOT / "experiments").glob("0282-*")) / "attack.py"
        spec = importlib.util.spec_from_file_location("frozen0282", path)
        a = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = a
        spec.loader.exec_module(a)
        a.ROOT = ROOT
        _G["a"] = a
    return _G["a"]


DROPS = [D for k in (1, 2) for D in itertools.combinations(OFFICIAL, k)]


def job(args):
    """One text: fitting pairs per drop set and form at length 19; the one-letter drops listed."""
    tid, text, known = args
    a = A282()
    counts = {"added": [], "beaufort": []}
    listed = []
    for D in DROPS:
        kn = {q: c for q, c in known.items() if q not in D}
        fs, _ = a.pairs_capped(kn, text, L)
        for fm, (n, P, C) in fs.items():
            counts[fm].append(int(n))
            if len(D) == 1 and P is not None and len(listed) < LIST_CAP:
                listed.extend([fm, D[0], int(p), int(c)] for p, c in zip(P[:LIST_CAP], C[:LIST_CAP]))
    return tid, {"counts": counts, "listed": listed[:LIST_CAP]}


def shuffle_keeping(text, keep, rng):
    idx = [i for i in range(N) if (i + 1) not in keep]
    letters = [text[i] for i in idx]
    rng.shuffle(letters)
    out = list(text)
    for i, c in zip(idx, letters):
        out[i] = c
    return "".join(out)


def quad_table():
    from kryptos.scorer import _table
    logs, floor = _table()
    t = np.full(26 ** 4, floor, dtype=np.float64)
    for k, v in logs.items():
        if len(k) == 4 and k.isalpha():
            i = 0
            for ch in k:
                i = i * 26 + ord(ch) - 65
            t[i] = v
    return t


def key_slots(setting, text, known):
    """The forced key value per slot (6-16) for a one-slip setting: from the slot's first remaining known place."""
    fm, q, pa, ca = setting
    pos = A282().F().frozen()._G["pos"]
    k = {}
    for x in sorted(known):
        if x == q:
            continue
        s = (x - 1) % L
        if s in k:
            continue
        cc, pp = int(pos[ca, ord(text[x - 1]) - 65]), int(pos[pa, ord(known[x]) - 65])
        k[s] = (cc - pp) % 26 if fm == "added" else (cc + pp) % 26
    return k


def read_runs(setting, kslots, T):
    """T: texts as an int array (n x 97). -> letters (n x 33) of the three runs under the setting."""
    fm, q, pa, ca = setting
    m = A282().F().frozen()
    pos = m._G["pos"]
    PA = np.array([ord(c) - 65 for c in m._G["A"][pa]], dtype=np.int64)
    out = []
    for lo, hi in RUNS:
        for place in range(lo, hi + 1):
            kv = kslots[(place - 1) % L]
            cc = pos[ca, T[:, place - 1]].astype(np.int64)
            out.append(PA[(cc - kv) % 26] if fm == "added" else PA[(kv - cc) % 26])
    return np.stack(out, axis=1)


def score_runs(R, qt):
    """Mean log10 quadgram probability over the 24 quadgrams inside the three runs of 11."""
    s = np.zeros(R.shape[0])
    for r in range(3):
        b = R[:, r * 11:(r + 1) * 11]
        for i in range(8):
            s += qt[((b[:, i] * 26 + b[:, i + 1]) * 26 + b[:, i + 2]) * 26 + b[:, i + 3]]
    return s / 24.0


def reading_string(setting, kslots, text):
    fm, q, pa, ca = setting
    m = A282().F().frozen()
    pos, PAs = m._G["pos"], m._G["A"][pa]
    out = []
    for i in range(N):
        s = i % L
        if s not in kslots:
            out.append("?")
            continue
        cc = int(pos[ca, ord(text[i]) - 65])
        out.append(PAs[(cc - kslots[s]) % 26] if fm == "added" else PAs[(kslots[s] - cc) % 26])
    return "".join(out)


def to_arr(texts):
    return np.array([[ord(c) - 65 for c in t] for t in texts], dtype=np.int64)


def read_test(text, known, settings, qt, seed):
    """Best run score over the settings for the text and for N_KEPT kept-place copies. -> dict."""
    rng = random.Random(seed)
    copies = [shuffle_keeping(text, set(OFFICIAL), rng) for _ in range(N_KEPT)]
    T = to_arr([text] + copies)
    best = np.full(T.shape[0], -99.0)
    per = []
    for st in settings:
        ks = key_slots(st, text, known)
        sc = score_runs(read_runs(st, ks, T), qt)
        best = np.maximum(best, sc)
        per.append(float(sc[0]))
    return {"own": per, "own_best": float(best[0]) if settings else None, "copies_best": [float(x) for x in best[1:]],
            "copies": copies}


def run(ctx):
    me = sys.modules.get(__name__)
    if getattr(me, "job", None) is not job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    from kryptos.plants import english_plant
    a = A282(); f = a.F(); m = f.frozen()
    f.setup(ctx.vocabulary)
    A, names = m._G["A"], m._G["names"]
    k20 = {q: ctx.KNOWN[q] for q in OFFICIAL}
    rng = random.Random(SEED)
    texts = [("k4", ctx.K4, k20)]
    texts += [(f"sh{i}", shuffle_keeping(ctx.K4, set(), rng), k20) for i in range(N_SHUF)]
    texts += [(f"rp{i}", shuffle_keeping(ctx.K4, {28, 66}, rng), k20) for i in range(N_RP)]
    texts += [(f"rpam{i}", shuffle_keeping(ctx.K4, {28, 66, 32, 70}, rng), k20) for i in range(N_RPAM)]
    plants = {}
    paired = [q for q in OFFICIAL if q <= 72]
    for j in range(N_PLANTS):
        pt = english_plant(SEED + 100 + j)
        pa, ca = rng.randrange(2, len(A)), rng.randrange(2, len(A))
        fm = rng.choice(("added", "beaufort"))
        kv = [rng.randrange(26) for _ in range(L)]
        PA, CA = A[pa], A[ca]
        ct = [CA[(PA.index(p) + kv[i % L]) % 26] if fm == "added" else CA[(kv[i % L] - PA.index(p)) % 26] for i, p in enumerate(pt)]
        q = rng.choice(paired)
        ct[q - 1] = rng.choice([c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if c != ct[q - 1]])
        pid = f"plant{j}"
        plants[pid] = {"pt": pt, "pa": pa, "ca": ca, "form": fm, "slip": q, "ct": "".join(ct), "known": {x: pt[x - 1] for x in OFFICIAL}}
        texts.append((pid, "".join(ct), plants[pid]["known"]))
    saved = getattr(ctx, "saved", {}) or {}
    res = {tid: saved[tid] for tid, _, _ in texts if tid in saved}
    todo = [t for t in texts if t[0] not in res]
    todo.sort(key=lambda t: not (t[0] == "k4" or t[0].startswith("plant")))
    W = int(os.environ.get("K4_WORKERS", 8))
    ctx.progress(len(res), len(texts), "texts")
    with mp.get_context("fork").Pool(W) as pool:
        for tid, out in pool.imap_unordered(job, todo, chunksize=1):
            res[tid] = out
            ctx.save(tid, out)
            ctx.progress(len(res), len(texts), "texts")

    # ---- counts -------------------------------------------------------------------------------------
    def stats(tid):
        c = res[tid]["counts"]
        return {"drop_sets_added": sum(1 for x in c["added"] if x), "drop_sets_beaufort": sum(1 for x in c["beaufort"] if x),
                "single_drops_fitting": sum(1 for fm in c for x in c[fm][:len(OFFICIAL)] if x),
                "one_slip_settings": sum(x for fm in c for x in c[fm][:len(OFFICIAL)])}
    k4s = stats("k4")
    counts = {"k4": k4s}
    for grp, n in (("sh", N_SHUF), ("rp", N_RP), ("rpam", N_RPAM)):
        ss = [stats(f"{grp}{i}") for i in range(n)]
        counts[grp] = {}
        for key in k4s:
            v = [s[key] for s in ss]
            counts[grp][key] = {"median": float(np.median(v)), "max": max(v), "at_or_above": sum(1 for x in v if x >= k4s[key]),
                                "p": round((1 + sum(1 for x in v if x >= k4s[key])) / (n + 1), 4)}

    # ---- readings -----------------------------------------------------------------------------------
    qt = quad_table()
    tmap = {tid: (t, kn) for tid, t, kn in texts}

    def settings_of(tid):
        return [tuple(x) for x in res[tid]["listed"] if x[1] <= 72]       # 73 and 74 have no partner: no key letter left
    k4set = settings_of("k4")
    rt = read_test(ctx.K4, k20, k4set, qt, SEED + 1)
    order = sorted(range(len(k4set)), key=lambda i: -rt["own"][i])
    k4_top = []
    for i in order[:10]:
        st = k4set[i]
        ks = key_slots(st, ctx.K4, k20)
        k4_top.append({"form": st[0], "slip_at": st[1], "plain_alphabet": names[st[2]], "cipher_alphabet": names[st[3]],
                       "score": round(rt["own"][i], 3), "reading": reading_string(st, ks, ctx.K4)})
    at_or_above = sum(1 for x in rt["copies_best"] if x >= rt["own_best"]) if k4set else None
    # the judge: K4's top 5 and the top reading of the first 100 kept-place copies
    copy_tops = []
    for cpy in rt["copies"][:N_JUDGE_COPIES]:
        T = to_arr([cpy])
        best, bst = -99.0, None
        for st in k4set:
            ks = key_slots(st, ctx.K4, k20)
            sc = float(score_runs(read_runs(st, ks, T), qt)[0])
            if sc > best:
                best, bst = sc, (st, ks)
        copy_tops.append(reading_string(bst[0], bst[1], cpy) if bst else None)
    to_judge = [r["reading"] for r in k4_top[:5]] + [r for r in copy_tops if r]
    verdicts = ctx.judge(to_judge) if to_judge else []
    js = [v.get("score") if v else None for v in verdicts]
    k4_j = [x for x in js[:min(5, len(k4_top))] if x is not None]
    cp_j = [x for x in js[min(5, len(k4_top)):] if x is not None]
    for r, x in zip(k4_top[:5], js):
        r["judge"] = x

    # ---- plants -------------------------------------------------------------------------------------
    plant_out = []
    for pid, p in plants.items():
        sts = settings_of(pid)
        prt = read_test(p["ct"], p["known"], sts, qt, SEED + 10 + int(pid[5:]))
        partner = p["slip"] + 38 if p["slip"] <= 34 else p["slip"] - 38
        idx = [i for i, st in enumerate(sts) if st[0] == p["form"] and st[2] == p["pa"] and st[3] == p["ca"] and st[1] == p["slip"]]
        listed = bool(idx)
        own = prt["own"][idx[0]] if idx else None
        first = listed and own >= max(prt["own"]) - 1e-12
        beats = listed and own > max(prt["copies_best"])
        exact = None
        if idx:
            st = sts[idx[0]]
            r = reading_string(st, key_slots(st, p["ct"], p["known"]), p["ct"])
            exact = sum(1 for i, c in enumerate(r) if c != "?" and c == p["pt"][i]) / sum(1 for c in r if c != "?")
        plant_out.append({"plant": pid, "form": p["form"], "slip": p["slip"], "partner": partner, "settings": len(sts), "listed": listed,
                          "reading_right_fraction": exact, "score": own, "ranks_first": bool(first),
                          "copies_best_max": max(prt["copies_best"]) if sts else None, "found": bool(first and beats)})
    found = sum(p["found"] for p in plant_out)
    read_p = round((1 + at_or_above) / (N_KEPT + 1), 4) if k4set else None
    bounds = {
        "item": "F16.1b-s-r", "key_length": L, "known_places": list(OFFICIAL), "drop_sets": len(DROPS),
        "alphabets_each_side": len(A), "counts": counts,
        "count_flag_line": "p < 0.01 against the stand-ins that keep 28 and 66 (rp)",
        "reading": {"k4_one_slip_settings": len(k4set), "letters_read": 33, "runs": [list(r) for r in RUNS],
                    "k4_best": rt["own_best"], "copies": N_KEPT, "copies_best_median": float(np.median(rt["copies_best"])) if k4set else None,
                    "copies_best_max": max(rt["copies_best"]) if k4set else None, "at_or_above": at_or_above, "p": read_p,
                    "flag_line": "p < 0.01", "k4_top": k4_top},
        "judge": {"sent": len(to_judge), "none": sum(1 for x in js if x is None), "k4_top5": js[:min(5, len(k4_top))],
                  "k4_best": max(k4_j) if k4_j else None, "copies_best": max(cp_j) if cp_j else None,
                  "k4_above_every_copy": bool(k4_j and cp_j and max(k4_j) > max(cp_j))},
        "plants": plant_out, "plants_found": found, "plants_total": N_PLANTS,
        "not_covered": "settings needing two slips (pair drops) are counted, not read; 8 of 19 key letters stay open in every reading",
        "controls": f"{N_SHUF} plain shuffles, {N_RP} keeping 28 and 66, {N_RPAM} keeping 28, 66, 32, 70 (counts); {N_KEPT} kept-place copies (readings)",
        "exhaustive": "yes at key length 19 for the 210 drop sets; readings sampled against copies",
        "aws_cost_estimate_dollars": 1.3,
    }
    return {"candidates": [], "bounds": bounds,
            "notes": (f"counts: K4 {k4s}; p against plain shuffles {counts['sh']['drop_sets_added']['p']}/{counts['sh']['drop_sets_beaufort']['p']}, "
                      f"against R/P-keeping stand-ins {counts['rp']['drop_sets_added']['p']}/{counts['rp']['drop_sets_beaufort']['p']}; "
                      f"reading: K4 best {rt['own_best']}, {at_or_above} of {N_KEPT} kept-place copies at or above (p {read_p}); "
                      f"judge K4 {max(k4_j) if k4_j else None} vs copies {max(cp_j) if cp_j else None}; plants {found}/{N_PLANTS}")}


def encrypt(plaintext, key):
    PA, CA, kv, fm = key["pa"], key["ca"], key["k"], key["form"]
    out = [CA[(PA.index(p) + kv[i % len(kv)]) % 26] if fm == "added" else CA[(kv[i % len(kv)] - PA.index(p)) % 26] for i, p in enumerate(plaintext)]
    for q, ch in key.get("slips", []):
        out[q - 1] = ch
    return "".join(out)


def worked_example(ctx, key):
    lines = ["K4 in rows of 19: the official runs 26-34 and 64-72 share columns 7-15", "",
             "column  place  known  carved   place  known  carved   shift on the plain table (carved - known)"]
    S = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for q in range(26, 35):
        r = q + 38
        d1 = (S.index(ctx.K4[q - 1]) - S.index(ctx.KNOWN[q])) % 26
        d2 = (S.index(ctx.K4[r - 1]) - S.index(ctx.KNOWN[r])) % 26
        lines.append(f"{(q - 1) % L + 1:>6}  {q:>5}  {ctx.KNOWN[q]:>5}  {ctx.K4[q - 1]:>6}   {r:>5}  {ctx.KNOWN[r]:>5}  {ctx.K4[r - 1]:>6}   {d1:>2} and {d2:>2}{'   equal' if d1 == d2 else ''}")
    lines += ["", "Places 28 and 66 both turn R into P; 32 and 70 share the shift 10 (A to K, C to M)."]
    return "\n".join(lines)
