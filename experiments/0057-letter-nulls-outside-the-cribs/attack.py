"""Experiment 0057. See program.md for the contract."""

EXPERIMENT = {
    "slug": "letter-nulls-outside-the-cribs",
    "title": "Filler letters chosen by letter: drop every copy of one or two letters, then the repeating secret word",
    "family": "2-masked-then-keyed",
    "parent": "0023-masks-reversal-and-nulls-then-tableau",
    "changed": "Experiment 23 removed filler letters at regular spacings. Here the filler is chosen by letter instead: every copy of one letter, or of a pair of letters, is struck out wherever it falls outside the two known stretches, the known letters move to their new places, and the repeating-secret-word test is run at every length.",
    "hypothesis_expert": (
        "C4 masking and C18 ('a bit of stego', 98 characters) allow nulls; a null letter that is a real "
        "letter chosen by rule is listed open in families.md. Model: every occurrence of a null letter (each "
        "of 26) or of a null pair (325) is removed from the carved text outside the crib ranges 22-34 and "
        "64-74 (a null inside a range would contradict Sanborn's positions), shifting the cribs' plaintext "
        "indices by the nulls before them; the rest is a periodic tableau text. Test periods 1-52 under the "
        "plain and cipher alphabets standard and KRYPTOS and three modes (the key alphabet drops out of "
        "consistency, 0006), exactly. Control: for each mask, ten masks removing the same number of letters "
        "at random positions outside the ranges. Bounds: complete for 351 letter masks and periods 1-52."
    ),
    "hypothesis_eli5": (
        "A message can be padded with filler letters that the reader is told to ignore, for example every "
        "Q. Experiment 23 tried filler at regular spacing. Here the filler is every copy of one letter, or "
        "of two letters, outside the known stretches. Striking them out moves the known letters to new "
        "places, and we ask again whether a repeating secret word of any length could fit them. Random "
        "strike-outs of the same size are the control."
    ),
    "prediction": (
        "No letter mask makes any period below 26 consistent more often than random strike-outs do; the "
        "smallest consistent period stays in the high twenties. Zero candidates."
    ),
    "method": (
        "1. For each letter and pair of letters, strike every copy outside places 22-34 and 64-74. 2. Shift "
        "the known places by the strike-outs before them. 3. For each period 1-52, alphabet pair and mode, "
        "check that known letters sharing a key slot force the same key letter. 4. Record the smallest "
        "consistent period. 5. Repeat with random strike-outs of the same count."
    ),
    "walkthrough": (
        "1. Take Q as the filler. 2. Q appears at places 26, 27, 39 and 42; 26 and 27 lie inside "
        "EASTNORTHEAST, so only 39 and 42 are struck. 3. No known letter lies before place 39, so "
        "EASTNORTHEAST stays at 22-34; BERLINCLOCK, after two strike-outs, now sits at 62-72. 4. With a "
        "secret word of 7 letters, place 22 (E under F) and place 29 (T under R) share a slot and must "
        "force the same key letter on the sculpture's table. 5. They do not, so 7 is dead for this filler. "
        "6. Repeat for every length, table and filler."
    ),
}

import random
from itertools import combinations
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

ALPHAS = {"std": STD, "kry": KRY}
MODES = {"vig": lambda p, c: (c - p) % 26, "beau": lambda p, c: (c + p) % 26, "varbeau": lambda p, c: (p - c) % 26}
RANGES = set(range(22, 35)) | set(range(64, 75))


def encrypt(plaintext, key):
    return plaintext


def smallest_period(ct, known, removed):
    """removed: set of 1-based carved places struck out (none inside the crib ranges)."""
    shift = {}
    gone = 0
    for i in range(1, len(ct) + 1):
        if i in removed:
            gone += 1
        else:
            shift[i] = i - gone
    crib = [(shift[pos], p, ct[pos - 1]) for pos, p in sorted(known.items())]
    best = None
    for pa in ALPHAS.values():
        for ca in ALPHAS.values():
            for f in MODES.values():
                forced = [(q, f(pa.index(p), ca.index(c))) for q, p, c in crib]
                for P in range(1, 53):
                    if best is not None and P >= best:
                        break
                    slot = {}
                    ok = True
                    for q, v in forced:
                        s_ = (q - 1) % P
                        if slot.setdefault(s_, v) != v:
                            ok = False; break
                    if ok:
                        best = P; break
    return best


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    outside = [i for i in range(1, len(ct) + 1) if i not in RANGES]
    masks = [(L,) for L in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"] + list(combinations("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 2))
    rng = random.Random(57)
    res, ctl = [], []
    for m in masks:
        removed = {i for i in outside if ct[i - 1] in m}
        sp = smallest_period(ct, known, removed)
        res.append(("".join(m), len(removed), sp))
        for _ in range(10):
            r = set(rng.sample(outside, len(removed)))
            ctl.append(smallest_period(ct, known, r))
        if ctx.time_left() < 120:
            break
    hist = {}
    for _, _, sp in res:
        hist[sp] = hist.get(sp, 0) + 1
    chist = {}
    for sp in ctl:
        chist[sp] = chist.get(sp, 0) + 1
    low = sorted([r for r in res if r[2] is not None and r[2] < 26], key=lambda r: r[2])
    return {
        "candidates": [],
        "bounds": {"family": "null letters (every copy of one or two letters outside the crib ranges), then periodic tableau",
                   "masks": len(res), "controls_per_mask": 10, "periods": "1-52", "alphabet_pairs": 4, "modes": 3,
                   "smallest_period_histogram": {str(k): v for k, v in sorted(hist.items(), key=lambda kv: (kv[0] is None, kv[0] or 0))},
                   "control_histogram_per_10": {str(k): round(v / 10, 1) for k, v in sorted(chist.items(), key=lambda kv: (kv[0] is None, kv[0] or 0))},
                   "masks_below_26": [{"letters": a, "struck": n, "period": p} for a, n, p in low[:20]]},
        "notes": (f"{len(res)} letter masks; smallest consistent period per mask: {dict(sorted(hist.items(), key=lambda kv: (kv[0] is None, kv[0] or 0)))}; "
                  f"random strike-outs of the same size (per 10): {dict((k, round(v / 10, 1)) for k, v in sorted(chist.items(), key=lambda kv: (kv[0] is None, kv[0] or 0)))}. Masks below 26: {len(low)}."),
    }


def worked_example(ctx, key):
    ct = ctx.K4
    qs = [i + 1 for i, c in enumerate(ct) if c == "Q"]
    struck = [i for i in qs if i not in RANGES]
    return f"Q at {qs}; struck outside the crib ranges: {struck}; BERLINCLOCK moves from 64-74 to {64 - len(struck)}-{74 - len(struck)}"
