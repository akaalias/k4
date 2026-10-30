"""Experiment 0266. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f6.22c-amsco-period-23-forced-keys-against-a-count-matched-null",
    "title": "F6.22c: K4's best forced period-23 AMSCO key against the best of 21 settings drawn from the shuffles' own (a count-matched null), and per setting",
    "family": "6-move-then-table",
    "parent": "0265-f6.22b-amsco-period-23-forced-keys-by-english-likelihood-gaps-allowed",
    "changed": (
        "F6.22c, the chase of 0265 (Alexis, #100: a result that beats its copies at the edge gets a row). 0265: K4's best "
        "forced key -11.9 bits (below zero: less English than random letters), above 195 of the 200 shuffles' bests "
        "(p 0.03), every planted key +9 to +37. K4 has 21 agreeing settings where the median shuffle has 8, so its best is "
        "taken over more keys. Here the same scores per setting (unchanged), and K4's best of 21 against the best of 21 "
        "drawn from the pooled settings of the 200 shuffles (20,000 draws), K4's per-setting scores against the pool, and "
        "the shuffles with at least 21 settings."
    ),
    "hypothesis_expert": (
        "F6 (C1(a): a matrix code, then the table). AMSCO keyed by a dictionary word (0114's 891,360 routes, 3-15 columns), "
        "then a period-23 key on the sculpture's 8 table classes. With 24 known letters on 23 slots the key is almost "
        "fully forced in every agreeing setting, so a key drawn from any English text (C7(a), C5: a phrase as key; F1.3's "
        "test on this move) shows as English letters in slot order. Statistic: per text, the highest English log-likelihood "
        "ratio of a forced key (bits against random letters, each forced letter conditioned on the forced letters before it "
        "in its run, slots 1-23 in order, no wrap), over its agreeing settings and two numberings. Power: 20 plants "
        "(Carter messages, random route and class, a 23-letter window of English as key)."
    ),
    "hypothesis_eli5": (
        "K4's best 23-letter key reads less like English than random letters do, yet it beat most scrambled copies' best "
        "keys. K4 fits this cipher in 21 ways where a typical copy fits in 8, and the best of 21 tries is naturally higher "
        "than the best of 8. Here K4 is compared with the best of 21 keys drawn from the copies' own, so both get the same "
        "number of tries."
    ),
    "prediction": (
        "Count-matched: K4's best of 21 inside the null (p above 0.05); K4's per-setting scores as the pool's (rank-sum "
        "p above 0.05). If K4 still beats the count-matched null, a row to look at its top keys by eye and by the judge. "
        "Zero candidates."
    ),
    "method": (
        "1. 0263's exact count at period 23, unchanged, for K4, its 200 shuffles (seed 2620) and 20 plants, every agreeing "
        "setting kept with its forced shifts per slot. "
        "2. Each forced key written as letters in slot order on the standard and on the KRYPTOS alphabet, '?' where no "
        "known letter reaches; scored by its log-likelihood ratio, English against random letters, in bits: each forced "
        "letter's probability given the up to three forced letters before it in its run, from the quadgram table. "
        "3. Per setting the better of its two numberings. K4's best of its 21 against the best of 21 drawn without "
        "replacement from the 200 shuffles' pooled settings (20,000 draws, seed 2661); K4's per-setting scores against the "
        "pool by rank sum; the shuffles with at least 21 settings, their bests. Plants as 0265. "
        "4. K4's forced keys listed in full."
    ),
    "walkthrough": (
        "1. Take one of K4's agreeing settings: an AMSCO grid keyed by a word, then the table with a 23-letter key. "
        "2. Undo the grid for the 24 known places: each lands on a carved place, whose number mod 23 is its key slot. "
        "3. The key letter at that slot is the carved letter minus the known letter on the table (plus, for Beaufort). "
        "4. Write the 23 slots in order, '?' where nothing lands, and score each run of letters for how much more likely it is "
        "as English than as random letters. "
        "5. Do the same for every agreeing setting of each scrambled copy, and compare the best scores."
    ),
    "expected_minutes": 5,
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
PERIODS = (23,)
N_SHUFFLES = 200
N_PLANTS = 20
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


def settings():
    """0114's routes, deduplicated in its order: [(word, width, first, dir, where)]."""
    m = _load("0114")
    words = [w.strip().upper() for w in (ROOT / "kryptos" / "data" / "words.txt").read_text().split()]
    seqs = {}
    for w in words:
        if not (3 <= len(w) <= 30 and w.isalpha()):
            continue
        for s in (tuple(m.keyword_sequence(w)), tuple(m.full_sequence(w))):
            if 3 <= len(s) <= 15:
                for first in (1, 2):
                    if (s, first) not in seqs:
                        seqs[(s, first)] = w
    seen, out = set(), []
    for (seq, first), word in seqs.items():
        wh = m.where_amsco(seq, first)
        inv = [0] * N
        for i, j in enumerate(wh):
            inv[j] = i
        for d, r in (("forward", wh), ("inverse", inv)):
            t = tuple(r)
            if t in seen:
                continue
            seen.add(t)
            out.append((word, len(seq), first, d, t))
    return out


def _job(args):
    lo, hi = args
    G = _MODS["G"]
    routes, CI, PI, pidx, classes = G["routes"], G["CI"], G["PI"], G["pidx"], G["classes"]
    T = next(iter(CI.values())).shape[0]
    counts = np.zeros((len(PERIODS), T), dtype=np.int64)
    k4_live = []
    for ri in range(lo, hi):
        r = routes[ri][4]
        land = np.array([r[i] for i in pidx])
        prs = {p: [] for p in PERIODS}
        for p in PERIODS:
            last = {}
            for e, j in enumerate(land):
                s = j % p
                if s in last:
                    prs[p].append((last[s], e))
                last[s] = e
        for ci, (pa, ca, beau) in enumerate(classes):
            C = CI[ca][:, land]
            f = (C + PI[pa]) % 26 if beau else (C - PI[pa]) % 26
            for k, p in enumerate(PERIODS):
                ok = np.ones(T, dtype=bool)
                for x, y in prs[p]:
                    ok &= f[:, x] == f[:, y]
                counts[k] += ok
                for t in np.nonzero(ok)[0]:
                    k4_live.append((int(t), ri, ci, {int(land[e] % 23): int(f[t, e]) for e in range(len(land))}))
    return counts, k4_live


def run(ctx):
    import multiprocessing as mp
    t0 = time.time()
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    m14 = _load("0114")
    from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
    from kryptos.plants import english_plant
    ALPH = {"std": STD, "kry": KRY}
    known = ctx.KNOWN
    places = sorted(known)
    pidx = [p - 1 for p in places]
    routes = settings()
    classes = [(pa, ca, beau) for pa in ALPH for ca in ALPH for beau in (False, True)]
    k4 = ctx.K4
    rng = random.Random(2620)
    texts = [k4] + ["".join(rng.sample(k4, N)) for _ in range(N_SHUFFLES)]
    # plants: Carter messages, a random route and class, a 23-letter window of English as the key
    prng = random.Random(2641)
    plants = []
    for i in range(N_PLANTS):
        pt = english_plant(26400 + i)
        keyw = english_plant(26500 + i)[35:58]
        pr = prng.randrange(len(routes)); pa, ca, beau = classes[prng.randrange(len(classes))]
        kn = prng.choice(("std", "kry"))
        kv = [ALPH[kn].index(ch) for ch in keyw]
        wh = routes[pr][4]
        moved = [""] * N
        for j, ch in enumerate(pt):
            moved[wh[j]] = ch
        pc = "".join(ALPH[ca][(kv[j % 23] - ALPH[pa].index(ch)) % 26] if beau else ALPH[ca][(ALPH[pa].index(ch) + kv[j % 23]) % 26]
                     for j, ch in enumerate(moved))
        texts.append(pc)
        plants.append({"route": routes[pr][:4], "class": f"{pa}/{ca}/{'beau' if beau else 'vig'}", "key": keyw, "numbering": kn})
    CI = {an: np.array([[ALPH[an].index(ch) for ch in t] for t in texts], dtype=np.int64) for an in ALPH}
    PI = {an: np.array([ALPH[an].index(known[p]) for p in places], dtype=np.int64) for an in ALPH}
    _MODS["G"] = {"routes": routes, "CI": CI, "PI": PI, "pidx": pidx, "classes": classes}
    W = int(os.environ.get("K4_WORKERS", 8))
    step = max(1, len(routes) // (W * 8))
    chunks = [(i, min(i + step, len(routes))) for i in range(0, len(routes), step)]
    counts = np.zeros((len(PERIODS), len(texts)), dtype=np.int64)
    live = []
    ctx.progress(0, len(chunks), "route chunks")
    done = 0
    with mp.get_context("fork").Pool(W) as pool:
        for c, kl in pool.imap_unordered(_job, chunks):
            counts += c
            live += kl
            done += 1
            ctx.progress(done, len(chunks), "route chunks")
    from kryptos.scorer import _table
    logs, floor = _table()
    q4 = np.full((26, 26, 26, 26), 10 ** floor)
    for q, v in logs.items():
        if len(q) == 4 and q.isalpha() and q.isupper():
            q4[tuple(ord(ch) - 65 for ch in q)] = 10 ** v
    q4 /= q4.sum()
    p3, p2, p1 = q4.sum(axis=3), q4.sum(axis=(2, 3)), q4.sum(axis=(1, 2, 3))
    L2 = np.log2

    def keyscore(slots, an):
        """Bits by which the forced letters are likelier as English than as random letters, chained within runs."""
        letters = "".join(ALPH[an][slots[s]] if s in slots else "?" for s in range(23))
        tot, run = 0.0, []
        for ch in letters + "?":
            if ch == "?":
                run = []
                continue
            x = ord(ch) - 65
            h = run[-3:]
            if len(h) == 3:
                pr = q4[h[0], h[1], h[2], x] / p3[h[0], h[1], h[2]]
            elif len(h) == 2:
                pr = p3[h[0], h[1], x] / p2[h[0], h[1]]
            elif len(h) == 1:
                pr = p2[h[0], x] / p1[h[0]]
            else:
                pr = p1[x]
            tot += float(L2(pr)) + float(L2(26))
            run.append(x)
        return tot, letters
    best = [(-1e9, None) for _ in texts]
    k4_keys = []
    per = {}
    for t, ri, ci, slots in live:
        per.setdefault(t, []).append(max(keyscore(slots, an)[0] for an in ALPH))
        for an in ALPH:
            sc, letters = keyscore(slots, an)
            if t == 0:
                k4_keys.append({"route": routes[ri][:4], "class": "/".join(map(str, classes[ci])), "numbering": an, "key": letters,
                                "score": round(sc, 2)})
            if sc > best[t][0]:
                best[t] = (sc, letters)
    nS = N_SHUFFLES
    cop = [best[t][0] for t in range(1, nS + 1)]
    k4b = best[0][0]
    at_or_above = sum(1 for v in cop if v >= k4b)
    p = (at_or_above + 1) / (nS + 1)
    pres = []
    for i, pl in enumerate(plants):
        t = nS + 1 + i
        pl.update(best=round(best[t][0], 2), best_key=best[t][1], found=best[t][0] > max(cop), live=int(counts[0][t]))
        pres.append(pl["found"])
    k4_keys.sort(key=lambda d: -d["score"])
    pool = [v for t in range(1, nS + 1) for v in per.get(t, [])]
    k4s = per[0]
    n4 = len(k4s)
    rr = random.Random(2661)
    null = [max(rr.sample(pool, n4)) for _ in range(20000)]
    p_cm = (sum(1 for v in null if v >= max(k4s)) + 1) / (len(null) + 1)
    allv = sorted(k4s + pool)
    rank = {}
    for i, v in enumerate(allv):
        rank.setdefault(v, []).append(i + 1)
    R = sum(sum(rank[v]) / len(rank[v]) for v in k4s)
    m_, n_ = n4, len(pool)
    U = R - m_ * (m_ + 1) / 2
    mu, sd = m_ * n_ / 2, (m_ * n_ * (m_ + n_ + 1) / 12) ** 0.5
    import math
    z = (U - mu) / sd
    p_rs = 0.5 * math.erfc(z / 2 ** 0.5)
    big = sorted(((len(per.get(t, [])), round(max(per[t]), 2)) for t in range(1, nS + 1) if len(per.get(t, [])) >= n4), reverse=True)
    nsrt = sorted(null)
    srt = sorted(cop)
    bounds = {
        "item": "F6.22b (chase of 0263's AMSCO period-23 count)",
        "routes": len(routes), "classes": len(classes), "period": 23, "order": "A (move, then the table)",
        "agreeing_settings": {"k4": int(counts[0][0]), "copies_min_median_max": [int(counts[0][1:nS + 1].min()), float(np.median(counts[0][1:nS + 1])), int(counts[0][1:nS + 1].max())]},
        "statistic": "per text: best English log-likelihood ratio (bits, against random letters) of a forced key, slots 1-23 in order, no wrap, standard or KRYPTOS numbering, each forced letter conditioned on up to three forced letters before it in its run (quadgram table marginals), over its agreeing settings",
        "count_matched": {"k4_settings": n4, "pool_settings": len(pool), "draws": len(null), "k4_best": round(max(k4s), 2),
                          "null_best_of_n_5_50_95": [round(nsrt[len(nsrt) // 20], 2), round(nsrt[len(nsrt) // 2], 2), round(nsrt[len(nsrt) * 19 // 20], 2)],
                          "p": round(p_cm, 4)},
        "per_setting": {"k4_mean": round(sum(k4s) / n4, 2), "pool_mean": round(sum(pool) / len(pool), 2), "rank_sum_z": round(z, 2), "p_one_sided": round(p_rs, 4)},
        "shuffles_with_at_least_k4s_count": big,
        "k4_best": round(k4b, 2), "k4_best_key": best[0][1], "copies_best_min_median_max": [round(srt[0], 2), round(srt[nS // 2], 2), round(srt[-1], 2)],
        "copies_at_or_above": at_or_above, "p": round(p, 4), "k4_forced_keys": k4_keys,
        "plants": {"found": sum(pres), "of": len(pres), "each": plants},
        "copies": f"{N_SHUFFLES} fresh shuffles (seed 2620, as 0263)", "exhaustive": True,
        "compute_seconds": round(time.time() - t0),
        "modal_cost_estimate": "as 0263 (65 s on 32 cores, $0.03) plus key scoring: about $0.05",
    }
    notes = (f"F6.22c: K4's best of {n4} forced keys {max(k4s):.1f} bits against the best of {n4} drawn from the shuffles' {len(pool)} settings: "
             f"p {p_cm:.3f} (null median {nsrt[len(nsrt) // 2]:.1f}); per setting K4 mean {sum(k4s) / n4:.1f} against {sum(pool) / len(pool):.1f} (one-sided p {p_rs:.3f}); "
             f"shuffles with at least {n4} settings: {big}; plants found {sum(pres)} of {len(pres)}")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    """No candidate is submitted."""
    return plaintext


def worked_example(ctx, key):
    return "\n".join([
        "F6.22b: the keys K4's AMSCO settings force at period 23, read for English.", "",
        "  AMSCO keyed by a word, then the table with a 23-letter key: each known letter lands on a carved place p,",
        "  and forces the key letter at slot p mod 23 (carved minus known on the table, or their sum for Beaufort).",
        "  Written in slot order with '?' where nothing lands, a key taken from English text reads as English in runs of four.", "",
        "  per text: the best such key over its agreeing settings; K4's against 200 shuffles'; 20 planted English keys for power."])
