"""Experiment (F6.22, draft). See program.md for the contract."""

EXPERIMENT = {
    "slug": "f6-amsco-period-23-excess-against-200-shuffles-and-named-keys",
    "title": "F6.22: 0114's AMSCO excess at period 23 (K4 21 live settings against 1-15 on 10 shuffles): the same exact count against 200 fresh shuffles, and K4's live settings' forced keys checked against every 23-letter window of the named texts",
    "family": "6-move-then-table",
    "parent": "0114-amsco-keyed-by-the-dictionary",
    "changed": (
        "F6.22 (Alexis, 2026-10-28, #100: a result that beats its copies gets a row to chase it). 0114 counted AMSCO routes "
        "keyed by every dictionary word (3-15 columns, either first cell), then a periodic tableau key on the 8 table "
        "classes: at period 23 with the move first, K4 had 21 consistent settings where its 10 shuffles had 1-15, noted and "
        "not chased. Here the same exact count at periods 22-24 for K4 and 200 fresh shuffles (vectorised over texts, 0114's "
        "routes unchanged), and every setting K4 fits at 23 has its forced key (the shift at each key slot the known letters "
        "reach) compared with every 23-letter window of 0210's named texts, both directions, numbered on the standard and "
        "KRYPTOS alphabets: a period-23 key taken from a text Sanborn had is the only reading these settings could give."
    ),
    "hypothesis_expert": (
        "F6 (C1(a): a matrix code, then the table). AMSCO (cells of one and two letters alternately) keyed by a word, then a "
        "periodic key of period 23 on the sculpture's table classes (standard or KRYPTOS plain and cipher alphabets, Beaufort "
        "or not). A count of consistent settings is a property of a text (0254, 0255: each text has its own level) and a true "
        "setting adds only one, so the count cannot single out a message; what can is the key: a period-23 key forced at the "
        "known slots that matches a window of K1-K3, the sculpture's texts, Carter or Sanborn's letters. Plant: a Carter "
        "message through a random AMSCO route and a 23-letter key from K3's plaintext; its setting must be live and its key "
        "window found."
    ),
    "hypothesis_eli5": (
        "An old run found that K4 fits one kind of two-step cipher (a grid shuffle called AMSCO, then the cipher table with a "
        "23-letter key) in 21 ways where scrambled copies fit in at most 15. That count is more about the letters than about a "
        "message, so we check it against 200 copies, and for each of K4's 21 fits we ask the question that matters: is the "
        "23-letter key it needs a passage from a text Sanborn had to hand?"
    ),
    "prediction": (
        "K4's count at 23 inside the 200 shuffles' range (rank under the top 5%); no forced key matches a named-text window; "
        "the plant's setting live and its key window found. Zero candidates."
    ),
    "method": (
        "1. 0114's settings unchanged: every dictionary word's keyword and full-word column order (3-15 columns), first cell "
        "1 or 2, the route and its inverse, deduplicated. "
        "2. For K4, 200 shuffles (seed 2620) and one plant: per route and table class, the shifts at the 24 known places "
        "(move first: the key slot is the carved place mod p); live at p when every pair of known places in one slot agrees; "
        "counted at p = 22, 23, 24. "
        "3. K4's live settings at 23: the forced shift per slot, matched against every 23-letter window of 0210's named texts "
        "(both directions), key letters numbered on the standard or KRYPTOS alphabet. "
        "4. K4's count ranked among the shuffles'; matches listed."
    ),
    "walkthrough": (
        "1. Write the message into a grid under a keyword, alternating cells of one and two letters (AMSCO), and read the "
        "columns in the keyword's alphabetical order. "
        "2. Encipher the result on the cipher table with a key of 23 letters, repeating. "
        "3. Each known letter then fixes the key letter at its place mod 23; two known letters at the same key place must agree. "
        "4. Count the grid keywords and tables where they all agree, for K4 and for scrambled copies. "
        "5. For K4's agreeing settings, write out the key letters the known letters force and look for them as a passage of 23 "
        "letters in K1-K3, Carter's book or Sanborn's letters."
    ),
    "expected_minutes": 20,
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
PERIODS = (22, 23, 24)
N_SHUFFLES = 200
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
                if p == 23 and ok[0]:
                    k4_live.append((ri, ci, {int(land[e] % 23): int(f[0, e]) for e in range(len(land))}))
    return counts, k4_live


def run(ctx):
    import multiprocessing as mp
    t0 = time.time()
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    m14 = _load("0114"); m10 = _load("0210")
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
    # plant: Carter with the known words, a random route and class, a 23-letter key from K3's plaintext
    srcs = m10.sources()
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
    counts = np.zeros((len(PERIODS), len(texts)), dtype=np.int64)
    k4_live = []
    ctx.progress(0, len(chunks), "route chunks")
    done = 0
    with mp.get_context("fork").Pool(W) as pool:
        for c, kl in pool.imap_unordered(_job, chunks):
            counts += c
            k4_live += kl
            done += 1
            ctx.progress(done, len(chunks), "route chunks")
    # the plant's own setting live, and K4's (and the plant's) forced keys against named-text windows
    def match_windows(slots):
        hits = []
        for name, (grp, s) in srcs.items():
            for an, A in ALPH.items():
                idx = [A.index(ch) for ch in s]
                for o in range(0, len(idx) - 22):
                    if all(idx[o + sl] == v for sl, v in slots.items()):
                        hits.append({"source": name, "numbering": an, "offset": o})
        return hits
    k4_matches = []
    for ri, ci, slots in k4_live:
        h = match_windows(slots)
        if h:
            k4_matches.append({"route": routes[ri][:4], "class": "/".join(map(str, classes[ci])), "hits": h[:5]})
    # the plant's true setting: its forced slots are the key; is it live and matched?
    land = [wh[i] for i in pidx]
    fP = [((ALPH[ca].index(pc[j]) + ALPH[pa].index(known[places[e]])) % 26) if beau else ((ALPH[ca].index(pc[j]) - ALPH[pa].index(known[places[e]])) % 26) for e, j in enumerate(land)]
    pslots = {}
    plant_live = True
    for e, j in enumerate(land):
        s = j % 23
        if s in pslots and pslots[s] != fP[e]:
            plant_live = False
        pslots[s] = fP[e]
    plant_hits = match_windows(pslots)
    plant_found = plant_live and any(h["source"] == "K3 plain fwd" and h["offset"] == off and h["numbering"] == kn for h in plant_hits)
    k23 = counts[PERIODS.index(23)]
    cop = k23[1:N_SHUFFLES + 1]
    rank = {p: {"k4": int(counts[k][0]), "copies_min_median_max": [int(counts[k][1:N_SHUFFLES + 1].min()), float(np.median(counts[k][1:N_SHUFFLES + 1])), int(counts[k][1:N_SHUFFLES + 1].max())],
                "copies_at_or_above": int((counts[k][1:N_SHUFFLES + 1] >= counts[k][0]).sum())} for k, p in enumerate(PERIODS)}
    bounds = {
        "item": "F6.22 (0114's AMSCO excess at period 23)",
        "routes": len(routes), "classes": len(classes), "periods": list(PERIODS), "order": "A (move, then the table)",
        "counts": rank, "k4_live_at_23": len(k4_live), "k4_key_matches": k4_matches, "n_k4_key_matches": len(k4_matches),
        "named_texts": len(srcs), "plant": {"route": routes[pr][:4], "class": f"{pa}/{ca}/{'beau' if beau else 'vig'}", "key": keyw,
                                            "numbering": kn, "live": plant_live, "key_window_found": plant_found},
        "copies": f"{N_SHUFFLES} fresh shuffles (seed 2620)", "exhaustive": True,
        "compute_seconds": round(time.time() - t0),
        "modal_cost_estimate": "891,360 routes x 8 classes, vectorised over 202 texts: about 1-2 core-hours (laptop)",
    }
    notes = (f"F6.22: K4 live at 23 in {int(k23[0])} settings; 200 shuffles {int(cop.min())}-{int(cop.max())} "
             f"(median {np.median(cop):.0f}), {int((cop >= k23[0]).sum())} at or above K4; forced keys matching a named-text window: "
             f"{len(k4_matches)}; plant live {plant_live}, key found {plant_found}")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    """No candidate is submitted."""
    return plaintext


def worked_example(ctx, key):
    return "\n".join([
        "F6.22: AMSCO keyed by a word, then the table with a 23-letter key.", "",
        "  AMSCO: write the message in rows of cells holding 1 and 2 letters alternately, read the columns in keyword order",
        "  the table: each moved letter shifted by the key letter at its place mod 23",
        "  the known letters force the key letter at their places mod 23; two known letters in one key place must agree", "",
        "  count the agreeing settings for K4 and 200 shuffles; for K4's, look for the forced key as a 23-letter passage."])
