"""Experiment 0264. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f6.22b-amsco-period-23-forced-keys-read-for-english",
    "title": "F6.22b: the keys K4's AMSCO settings force at period 23, read for English (quadgrams), against the best forced key of each of 200 shuffles; 20 planted running-key messages for power",
    "family": "6-move-then-table",
    "parent": "0263-f6-amsco-period-23-excess-against-200-shuffles-and-named-keys",
    "changed": (
        "F6.22b, the chase of 0263 (Alexis, 2026-10-28, #100: a result that beats its copies, even at the edge, gets a row). "
        "0263 put K4's count of agreeing AMSCO settings at period 23 in the top 2.5% of 200 shuffles (21; 4 of 200 at or "
        "above) and found no forced key that is a passage of a named text. A count is a property of a text; what would "
        "single out a message is its key. Here every setting that agrees at 23, for K4, the same 200 shuffles (seed 2620) "
        "and 20 plants, has its forced key (up to 23 letters, numbered on the standard or KRYPTOS alphabet) scored for "
        "English by quadgrams, as a running key from any English text would score; K4's best against the shuffles' bests."
    ),
    "hypothesis_expert": (
        "F6 (C1(a): a matrix code, then the table). AMSCO keyed by a dictionary word (0114's 891,360 routes, 3-15 columns), "
        "then a period-23 key on the sculpture's 8 table classes. With 24 known letters on 23 slots the key is almost "
        "fully forced in every agreeing setting, so a key drawn from any English text (C7(a), C5: a phrase as key; F1.3's "
        "test on this move) shows as English letters in slot order. Statistic: per text, the highest mean quadgram score "
        "over the 4-grams fully forced (slots 1-23, no wrap), over its agreeing settings and two numberings. Power: 20 plants "
        "(Carter messages, random route and class, a 23-letter window of English as key)."
    ),
    "hypothesis_eli5": (
        "K4 fits a two-step cipher (a grid shuffle, then the table with a 23-letter key) in more ways than most scrambled "
        "copies do. For each way it fits, the known letters spell out almost the whole 23-letter key. If Sanborn took his "
        "key from a book or a sentence, that key should read like English; here we check whether K4's keys read more like "
        "English than the keys scrambled copies are forced to."
    ),
    "prediction": (
        "K4's best forced key inside the 200 shuffles' bests (p above 0.05), its letters no English; most planted keys "
        "above every shuffle (power at least 15 of 20). Zero candidates."
    ),
    "method": (
        "1. 0263's exact count at period 23, unchanged, for K4, its 200 shuffles (seed 2620) and 20 plants, every agreeing "
        "setting kept with its forced shifts per slot. "
        "2. Each forced key written as letters in slot order on the standard and on the KRYPTOS alphabet, '?' where no "
        "known letter reaches; scored by the mean log quadgram over the 4-grams with all four letters forced (at least 8). "
        "3. Per text the best score over its settings and numberings; K4's rank among the 200 shuffles'; a plant is found "
        "when its best is above every shuffle's. "
        "4. K4's forced keys listed in full."
    ),
    "walkthrough": (
        "1. Take one of K4's agreeing settings: an AMSCO grid keyed by a word, then the table with a 23-letter key. "
        "2. Undo the grid for the 24 known places: each lands on a carved place, whose number mod 23 is its key slot. "
        "3. The key letter at that slot is the carved letter minus the known letter on the table (plus, for Beaufort). "
        "4. Write the 23 slots in order, '?' where nothing lands, and score the runs of four letters for English. "
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
MIN_GRAMS = 8
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

    def keyscore(slots, an):
        letters = "".join(ALPH[an][slots[s]] if s in slots else "?" for s in range(23))
        grams = [letters[i:i + 4] for i in range(20) if "?" not in letters[i:i + 4]]
        if len(grams) < MIN_GRAMS:
            return None, letters
        return sum(logs.get(q, floor) for q in grams) / len(grams), letters
    best = [(-99.0, None) for _ in texts]
    k4_keys = []
    for t, ri, ci, slots in live:
        for an in ALPH:
            sc, letters = keyscore(slots, an)
            if t == 0:
                k4_keys.append({"route": routes[ri][:4], "class": "/".join(map(str, classes[ci])), "numbering": an, "key": letters,
                                "score": None if sc is None else round(sc, 3)})
            if sc is not None and sc > best[t][0]:
                best[t] = (sc, letters)
    nS = N_SHUFFLES
    cop = [best[t][0] for t in range(1, nS + 1)]
    k4b = best[0][0]
    at_or_above = sum(1 for v in cop if v >= k4b)
    p = (at_or_above + 1) / (nS + 1)
    pres = []
    for i, pl in enumerate(plants):
        t = nS + 1 + i
        pl.update(best=round(best[t][0], 3), best_key=best[t][1], found=best[t][0] > max(cop), live=int(counts[0][t]))
        pres.append(pl["found"])
    k4_keys.sort(key=lambda d: -(d["score"] if d["score"] is not None else -99))
    srt = sorted(cop)
    bounds = {
        "item": "F6.22b (chase of 0263's AMSCO period-23 count)",
        "routes": len(routes), "classes": len(classes), "period": 23, "order": "A (move, then the table)",
        "agreeing_settings": {"k4": int(counts[0][0]), "copies_min_median_max": [int(counts[0][1:nS + 1].min()), float(np.median(counts[0][1:nS + 1])), int(counts[0][1:nS + 1].max())]},
        "statistic": f"per text: best mean log10 quadgram of a forced key (slots 1-23 in order, no wrap, standard or KRYPTOS numbering, at least {MIN_GRAMS} fully forced 4-grams) over its agreeing settings",
        "k4_best": round(k4b, 3), "k4_best_key": best[0][1], "copies_best_min_median_max": [round(srt[0], 3), round(srt[nS // 2], 3), round(srt[-1], 3)],
        "copies_at_or_above": at_or_above, "p": round(p, 4), "k4_forced_keys": k4_keys,
        "plants": {"found": sum(pres), "of": len(pres), "each": plants},
        "copies": f"{N_SHUFFLES} fresh shuffles (seed 2620, as 0263)", "exhaustive": True,
        "compute_seconds": round(time.time() - t0),
        "modal_cost_estimate": "as 0263 (65 s on 32 cores, $0.03) plus key scoring: about $0.05",
    }
    notes = (f"F6.22b: K4's best forced key at 23 scores {k4b:.2f} ({best[0][1]}); 200 shuffles' bests {srt[0]:.2f} to {srt[-1]:.2f}, "
             f"{at_or_above} at or above K4 (p {p:.3f}); plants found {sum(pres)} of {len(pres)}")
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
