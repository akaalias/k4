"""Experiment 0053. See program.md for the contract."""

EXPERIMENT = {
    "slug": "periodic-tableau-k1-k3-word-alphabets",
    "title": "The repeating secret word again, on tables rebuilt from the words of the solved messages",
    "family": "1-keyed-periodic",
    "parent": "0020-short-periods-mixed-alphabets-consistency",
    "changed": "Experiments 20 and 48 rebuilt the table's alphabets only from the puzzle's own vocabulary list. Here the alphabets are rebuilt from every word of the three solved messages and from the words Sanborn's 2025 letter points at (EGYPT, WALL, CAIRO, MESSAGE, DELIVER and others), and the crib test is rerun at every period from 1 to 52, with shuffled copies of the copper as the control.",
    "hypothesis_expert": (
        "Periodic tableau with separate plain and cipher alphabets (Quagmire family), alphabets keyword-mixed "
        "from words outside the 62-word vocabulary: every distinct word of the K1-K3 plaintexts with at "
        "least three distinct letters (C7, C30: earlier text may carry the key) and the C13/C14 words "
        "EGYPT, CAIRO, LUXOR, WALL, NOVEMBER, MESSAGE, DELIVER, DELIVERING, TRANSMIT, plus standard and "
        "KRYPTOS. For each plain-cipher pair and mode (Vigenere, Beaufort, variant Beaufort) the 24 cribs "
        "force 24 key indices; period P is consistent when every two cribs sharing a slot force the same "
        "index. Count consistent (pair, mode) cases per period on K4 and on ten shuffles of the copper with "
        "the same pool. At consistent periods up to 29, read the forced slots in the standard, KRYPTOS and "
        "plain alphabets and match against every word and every K1-K3 window of that length; a full match "
        "decrypts and submits. Bounds: complete for this pool and periods 1-52."
    ),
    "hypothesis_eli5": (
        "The first two messages used the sculpture's table with a secret word repeated over and over. "
        "The table itself can be rebuilt from a word, and so far we rebuilt it only from the puzzle's own "
        "word list. The solved messages are full of other words, and Sanborn's last letter mentions Egypt "
        "and a message being delivered, so we rebuild the table from all of those and ask again, for every "
        "length of secret word up to 52, whether the 24 known letters can agree. Scrambled copies of the "
        "copper get the same test, so we can tell real agreement from luck."
    ),
    "prediction": (
        "Periods 1-26 and 30-52 are consistent on K4 no more often than on the shuffles (near zero below "
        "21); 27-29 are consistent for most pairs, as before, and no forced fragment matches a word or a "
        "K1-K3 window. Zero candidates."
    ),
    "method": (
        "1. Build the word pool and its keyword alphabets, dropping duplicates and those already in the "
        "vocabulary pool. 2. For every plain and cipher alphabet and mode, compute the 24 forced key indices. "
        "3. For each period, check the slot-sharing pairs. 4. Repeat on ten shuffles. 5. At consistent periods "
        "up to 29, match forced fragments against words and K1-K3 windows; decrypt and submit matches."
    ),
    "walkthrough": (
        "1. Take the word SHADING from K1 and build its alphabet: SHADINGBCEFJKLMOPQRTUVWXYZ. 2. Take "
        "INVISIBLE from K2 for the carved letters: INVSBLEACDFGHJKMOPQRTUWXYZ. 3. Place 22 holds E under "
        "carved F: counting from 0, E is 9 in the first alphabet and F is 10 in the second, so "
        "Vigenere needs key 1. 4. With a secret word of 7 letters, places 22 and 29 share a slot, so place "
        "29 (T under carved R) must also need key 1. 5. T is 19 in the first alphabet and R is 19 in the "
        "second, so it needs 0: a contradiction, and length 7 is dead for this pair. 6. Repeat for every "
        "pair, mode and length."
    ),
}

import random
from kryptos.alphabets import keyword_mixed
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

SPACED = (
    "BETWEEN SUBTLE SHADING AND THE ABSENCE OF LIGHT LIES THE NUANCE OF IQLUSION "
    "IT WAS TOTALLY INVISIBLE HOWS THAT POSSIBLE THEY USED THE EARTHS MAGNETIC FIELD X THE INFORMATION WAS GATHERED AND "
    "TRANSMITTED UNDERGRUUND TO AN UNKNOWN LOCATION X DOES LANGLEY KNOW ABOUT THIS THEY SHOULD ITS BURIED OUT THERE "
    "SOMEWHERE X WHO KNOWS THE EXACT LOCATION ONLY WW THIS WAS HIS LAST MESSAGE X THIRTY EIGHT DEGREES FIFTY SEVEN "
    "MINUTES SIX POINT FIVE SECONDS NORTH SEVENTY SEVEN DEGREES EIGHT MINUTES FORTY FOUR SECONDS WEST ID BY ROWS "
    "SLOWLY DESPARATLY SLOWLY THE REMAINS OF PASSAGE DEBRIS THAT ENCUMBERED THE LOWER PART OF THE DOORWAY WAS REMOVED "
    "WITH TREMBLING HANDS I MADE A TINY BREACH IN THE UPPER LEFT HAND CORNER AND THEN WIDENING THE HOLE A LITTLE I "
    "INSERTED THE CANDLE AND PEERED IN THE HOT AIR ESCAPING FROM THE CHAMBER CAUSED THE FLAME TO FLICKER BUT PRESENTLY "
    "DETAILS OF THE ROOM WITHIN EMERGED FROM THE MIST X CAN YOU SEE ANYTHING Q"
)
EXTRA = ["EGYPT", "CAIRO", "LUXOR", "WALL", "NOVEMBER", "MESSAGE", "DELIVER", "DELIVERING", "TRANSMIT"]
MODES = {"vig": lambda p, c: (c - p) % 26, "beau": lambda p, c: (c + p) % 26, "varbeau": lambda p, c: (p - c) % 26}
DEC = {"vig": lambda c, k: (c - k) % 26, "beau": lambda c, k: (k - c) % 26, "varbeau": lambda c, k: (c + k) % 26}
ENC = {"vig": lambda p, k: (p + k) % 26, "beau": lambda p, k: (k - p) % 26, "varbeau": lambda p, k: (p - k) % 26}


def letters(s):
    return "".join(c for c in s if "A" <= c <= "Z")


def word_pool(vocab):
    words = sorted({w for w in SPACED.split() if len(set(w)) >= 3} | set(EXTRA))
    seen = {STD, KRY} | {keyword_mixed(w) for w in vocab if len(set(w)) >= 3}
    pool = {"std": STD, "kry": KRY}
    for w in words:
        A = keyword_mixed(w)
        if A not in seen:
            seen.add(A); pool[f"{w}/keyword"] = A
    return pool, words


def encrypt(plaintext, key):
    pa, ca, m, k = key["pa"], key["ca"], key["m"], key["key"]
    return "".join(ca[ENC[m](pa.index(p), k[i % len(k)])] for i, p in enumerate(plaintext))


def sweep(ct, crib, pool, periods):
    idx = {n: {ch: i for i, ch in enumerate(A)} for n, A in pool.items()}
    pairs_by_P = {}
    for P in periods:
        pr = []
        first = {}
        for k, (pos, _) in enumerate(crib):
            s_ = (pos - 1) % P
            if s_ in first:
                pr.append((first[s_], k))
            else:
                first[s_] = k
        pairs_by_P[P] = pr
    counts = {P: 0 for P in periods}
    hits = []
    for pn in pool:
        pi = idx[pn]
        for cn in pool:
            ci = idx[cn]
            for m, f in MODES.items():
                forced = [f(pi[p], ci[ct[pos - 1]]) for pos, p in crib]
                for P in periods:
                    if all(forced[a] == forced[b] for a, b in pairs_by_P[P]):
                        counts[P] += 1
                        hits.append((P, pn, cn, m, forced))
    return counts, hits


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    crib = sorted(known.items())
    pool, words = word_pool(ctx.vocabulary)
    periods = list(range(1, 53))
    counts, hits = sweep(ct, crib, pool, periods)
    rng = random.Random(53)
    controls = []
    for _ in range(10):
        sh = list(ct); rng.shuffle(sh)
        c_counts, _ = sweep("".join(sh), crib, pool, periods)
        controls.append(c_counts)
        if ctx.time_left() < 300:
            break
    # word matching at consistent periods up to 29
    texts = [letters(SPACED)]
    allwords = set(words) | set(ctx.vocabulary)
    cands, matches = [], 0
    for P, pn, cn, m, forced in hits:
        if P > 29:
            continue
        slots = {}
        for (pos, _), v in zip(crib, forced):
            slots[(pos - 1) % P] = v
        pool_P = {w for w in allwords if len(w) == P} | {t[i:i + P] for t in texts for i in range(len(t) - P + 1)}
        for kname, KA in (("std", STD), ("kry", KRY), ("plain", pool[pn])):
            for w in pool_P:
                if all(KA.index(w[s_]) == v for s_, v in slots.items()):
                    matches += 1
                    k = [KA.index(ch) for ch in w]
                    pa, ca = pool[pn], pool[cn]
                    pt = "".join(pa[DEC[m](ca.index(c), k[i % P])] for i, c in enumerate(ct))
                    cands.append({"plaintext": pt, "key": {"pa": pa, "ca": ca, "m": m, "key": k}, "key_bits": 4.7 * P,
                                  "key_description": f"period {P} key {w} on {kname}; plain {pn}, cipher {cn}, {m}"})
    ctl = {P: [c.get(P, 0) for c in controls] for P in periods}
    low = [P for P in periods if counts[P] or any(ctl[P])]
    return {
        "candidates": cands[:50],
        "bounds": {"family": "periodic tableau, alphabets keyword-mixed from K1-K3 words and C13/C14 words", "alphabets": len(pool),
                   "pairs": len(pool) ** 2, "modes": 3, "periods": "1-52", "controls": len(controls),
                   "consistent_by_period_k4": {str(P): counts[P] for P in low},
                   "consistent_by_period_controls_mean": {str(P): round(sum(ctl[P]) / max(1, len(controls)), 1) for P in low},
                   "consistent_by_period_controls_max": {str(P): max(ctl[P]) if controls else 0 for P in low},
                   "word_matches": matches},
        "notes": (f"{len(pool)} alphabets, {len(pool) ** 2} pairs, 3 modes, periods 1-52. Consistent cases on K4 by period (shown where K4 or a control has any): "
                  + ", ".join(f"{P}: {counts[P]} (controls mean {sum(ctl[P]) / max(1, len(controls)):.1f}, max {max(ctl[P]) if controls else 0})" for P in low)
                  + f". Word matches: {matches}."),
    }


def worked_example(ctx, key):
    A, B = keyword_mixed("SHADING"), keyword_mixed("INVISIBLE")
    lines = [f"plain  {A}", f"cipher {B}", "", "place  plain  carved  key (Vigenere)  slot at period 7"]
    for pos in (22, 29, 23, 30):
        p, c = ctx.KNOWN[pos], ctx.K4[pos - 1]
        lines.append(f"{pos:>5}    {p}      {c}         {(B.index(c) - A.index(p)) % 26:>2}               {(pos - 1) % 7}")
    return "\n".join(lines)
