"""Experiment 0064. See program.md for the contract."""

EXPERIMENT = {
    "slug": "ciphertext-autokey-k1-k3-word-alphabets",
    "title": "The scrambled text as its own key, on tables rebuilt from the solved messages' words",
    "family": "1-keyed-periodic",
    "parent": "0025-autokeys-with-mixed-alphabets",
    "changed": "Experiment 25 tested the cipher that feeds on its own output on tables rebuilt from the puzzle's vocabulary. Experiment 62 then showed this recipe is the one that makes the copper's width-21 mark. Here the tables come from every word of the solved messages and Sanborn's 2025 letter, at every distance, with scrambled coppers as the control.",
    "hypothesis_expert": (
        "Ciphertext autokey, key letter = carved letter L back read in the key alphabet, lags 1-95, plain "
        "and cipher alphabets from the 102-alphabet pool of 0053 (K1-K3 plaintext words, C13/C14 words, "
        "standard, KRYPTOS), key alphabet standard, KRYPTOS, the plain alphabet or the cipher alphabet, "
        "three modes. Each crib at place i > L requires a specific key letter, hence a specific carved letter "
        "at i - L; the count of satisfied cribs per lag is exact and needs no primer. Motivation: 0062 found "
        "ciphertext autokey at lag 21 the only generator that raises the width-21 repeats (0056). Report the "
        "fewest mismatches over all settings against ten shuffled coppers. Bounds: complete for this pool."
    ),
    "hypothesis_eli5": (
        "In this cipher each letter is hidden using the hidden letter some fixed distance earlier, so once "
        "it starts it needs no secret word at all. Each of the 24 known letters then tells us exactly which "
        "carved letter must sit that distance before it. We check every distance from 1 to 95 on tables "
        "rebuilt from every word of the solved messages, and count how close any of them comes, compared "
        "with scrambled copies of the copper."
    ),
    "prediction": (
        "No setting satisfies every crib past the starter; the fewest mismatches is about the same on K4 as "
        "on the shuffles (several). Zero candidates."
    ),
    "method": (
        "1. Build the alphabet pool. 2. For each plain, cipher and key alphabet and mode, find the carved "
        "letter each crib requires L places back. 3. For each lag, count satisfied and violated cribs using "
        "the positions of each letter on the copper. 4. Keep the fewest violations. 5. Repeat on ten "
        "shuffles."
    ),
    "walkthrough": (
        "1. Take SHADING for the message alphabet, INVISIBLE for the carved alphabet and KRYPTOS for the key "
        "alphabet, with Vigenere. 2. Place 22 holds E (9 in SHADING) under carved F (10 in INVISIBLE), so the "
        "key letter there is the one at index 1 of KRYPTOS: R. 3. At distance 21 the key letter is the carved "
        "letter at place 1, which is O, not R, so place 22 fails at lag 21. 4. At distance 10 the key letter "
        "would be the carved letter at place 12, L, which also fails. 5. Count the failures over all known "
        "places past the starter, for every distance and table."
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



INV = {"vig": lambda c, k: (c - k) % 26, "beau": lambda c, k: (k - c) % 26, "varbeau": lambda c, k: (c + k) % 26}


def encrypt(plaintext, key):
    A, C, K, m, L, primer = key["pa"], key["ca"], key["ka"], key["m"], key["lag"], key["primer"]
    out = []
    for i, p in enumerate(plaintext):
        k = primer[i] if i < L else out[i - L]
        out.append(C[ENC[m](A.index(p), K.index(k))])
    return "".join(out)


def scan(ct, crib, pool):
    where = {}
    for j, ch in enumerate(ct):
        where.setdefault(ch, []).append(j)
    best = (99, None)
    full = []
    for pn, A in pool.items():
        for cn, C in pool.items():
            kas = {"std": STD, "kry": KRY, "plain": A, "cipher": C}
            for m, f in MODES.items():
                need = [(q - 1, f(A.index(p), C.index(ct[q - 1]))) for q, p in crib]
                for kn, K in kas.items():
                    hits = [0] * 96
                    for i, k in need:
                        for j in where.get(K[k], ()):
                            if j < i:
                                hits[i - j] += 1
                    for L in range(1, 96):
                        n = sum(1 for i, _ in need if i >= L)
                        if n < 6:
                            continue
                        mm = n - hits[L]
                        if mm < best[0]:
                            best = (mm, (pn, cn, kn, m, L, n))
                        if mm == 0:
                            full.append((pn, cn, kn, m, L, n))
    return best, full


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    crib = sorted(known.items())
    pool, words = word_pool(ctx.vocabulary)
    best, full = scan(ct, crib, pool)
    rng = random.Random(64)
    ctl = []
    for _ in range(10):
        sh = list(ct); rng.shuffle(sh)
        b, _ = scan("".join(sh), crib, pool)
        ctl.append(b[0])
        if ctx.time_left() < 120:
            break
    return {
        "candidates": [],
        "bounds": {"family": "ciphertext autokey on K1-K3-word and C13/C14-word alphabets", "alphabets": len(pool),
                   "key_alphabets": "standard, KRYPTOS, plain, cipher", "modes": 3, "lags": "1-95 (at least 6 cribs past the primer)",
                   "fewest_mismatches": best[0], "best_setting": None if not best[1] else dict(zip(["plain", "cipher", "key", "mode", "lag", "cribs_checked"], best[1])),
                   "full_matches": len(full), "control_fewest_mismatches": ctl},
        "notes": f"Fewest mismatches over all settings: {best[0]} ({best[1]}); ten shuffled coppers: {sorted(ctl)}. Full matches: {len(full)}.",
    }


def worked_example(ctx, key):
    A, C = keyword_mixed("SHADING"), keyword_mixed("INVISIBLE")
    lines = ["place  plain  carved  key letter needed (KRYPTOS)  carved 21 back"]
    for q in (22, 23, 24, 25):
        k = (C.index(ctx.K4[q - 1]) - A.index(ctx.KNOWN[q])) % 26
        lines.append(f"{q:>5}    {ctx.KNOWN[q]}      {ctx.K4[q - 1]}               {KRY[k]}                    {ctx.K4[q - 22]}")
    return "\n".join(lines)
