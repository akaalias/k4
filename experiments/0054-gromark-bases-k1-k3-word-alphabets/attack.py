"""Experiment 0054. See program.md for the contract."""

EXPERIMENT = {
    "slug": "gromark-bases-k1-k3-word-alphabets",
    "title": "Number keys that grow by a rule, on tables rebuilt from the words of the solved messages",
    "family": "5-gromark",
    "parent": "0028-gromark-small-bases-two-to-nine",
    "changed": "Experiments 13, 28 and 46 tested Gromark keys, a string of digits that grows by adding earlier digits, on tables rebuilt from the puzzle's vocabulary. Here the tables come from every word of the solved messages and Sanborn's 2025 letter, and the test asks first how small a number base the 24 known letters allow, then whether any growth rule fits.",
    "hypothesis_expert": (
        "Gromark and its generalisations: the key is a digit stream in base B with k[i] = k[i-a] + k[i-b] "
        "mod B (a > b >= 1, a up to 13), applied as an additive shift through a plain and a cipher alphabet "
        "(C22(a) reads the raised YAR as such a primer). Every forced shift must be a digit below B, so the "
        "largest of the 24 forced shifts bounds B from below for each plain-cipher pair and mode. Pool: the "
        "102 alphabets of 0053 (K1-K3 plaintext words and the C13/C14 words, plus standard and KRYPTOS), "
        "three modes. Report the smallest admissible base over all 10,404 pairs, against ten shuffled "
        "coppers; for every pair admissible at B <= 15, test every rule (a, b) on all crib triples where "
        "positions i, i-a and i-b are all known. Bounds: exact for these alphabets."
    ),
    "hypothesis_eli5": (
        "In a Gromark cipher the secret is a short string of digits that grows by itself: each new digit is "
        "the sum of two earlier ones, keeping only the last digit. Each known letter tells us how far the "
        "table had to shift it, and with ordinary digits no shift can be bigger than 9. So the biggest "
        "shift the known letters demand says how large the number system must be. We work that out for "
        "tables rebuilt from every word of the solved messages, and check scrambled copies of the copper "
        "the same way."
    ),
    "prediction": (
        "No pair admits base 10: the smallest admissible base is about 18 to 20 on K4, as on the shuffles. "
        "No pair admits a base of 15 or less, so no growth rule needs testing. Zero candidates."
    ),
    "method": (
        "1. Build the alphabet pool as in experiment 53. 2. For each plain and cipher alphabet and mode, "
        "compute the 24 forced shifts and their maximum. 3. Record the smallest maximum, the smallest "
        "admissible base. 4. Repeat on ten shuffles. 5. For pairs admissible at 15 or less, test every "
        "two-term rule on the crib triples."
    ),
    "walkthrough": (
        "1. Take SHADING for the message alphabet and INVISIBLE for the carved one. 2. Place 22: E is 9, "
        "carved F is 10, a shift of 1. 3. Place 23: A is 2, carved L is 5, a shift of 3. 4. Place 24: S is 0, "
        "carved R is 19, a shift of 19. 5. A shift of 19 cannot be a single digit, so this pair of tables "
        "needs a number base of at least 20 and an ordinary Gromark is out. 6. Do the same for every pair "
        "and every way of using the table, and keep the smallest such base."
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
    return "".join(ca[ENC[m](pa.index(p), k[i])] for i, p in enumerate(plaintext))


def min_base(ct, crib, pool):
    idx = {n: {ch: i for i, ch in enumerate(A)} for n, A in pool.items()}
    best, small = 99, []
    for pn in pool:
        pi = idx[pn]
        for cn in pool:
            ci = idx[cn]
            for m, f in MODES.items():
                forced = [f(pi[p], ci[ct[pos - 1]]) for pos, p in crib]
                mx = max(forced)
                if mx + 1 < best:
                    best = mx + 1
                if mx + 1 <= 15:
                    small.append((pn, cn, m, forced))
    return best, small


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    crib = sorted(known.items())
    pool, words = word_pool(ctx.vocabulary)
    best, small = min_base(ct, crib, pool)
    rng = random.Random(54)
    ctl = []
    for _ in range(10):
        sh = list(ct); rng.shuffle(sh)
        b, _ = min_base("".join(sh), crib, pool)
        ctl.append(b)
    rule_hits = 0
    pos_of = {pos: k for k, (pos, _) in enumerate(crib)}
    for pn, cn, m, forced in small:
        B = max(forced) + 1
        for base in range(B, 16):
            for a in range(2, 14):
                for b in range(1, a):
                    ok, checks = True, 0
                    for pos, _ in crib:
                        if pos - a in pos_of and pos - b in pos_of:
                            checks += 1
                            if (forced[pos_of[pos - a]] + forced[pos_of[pos - b]]) % base != forced[pos_of[pos]]:
                                ok = False; break
                    if ok and checks:
                        rule_hits += 1
    return {
        "candidates": [],
        "bounds": {"family": "Gromark-type digit keys, k[i] = k[i-a] + k[i-b] mod B, on K1-K3-word and C13/C14-word alphabets",
                   "alphabets": len(pool), "pairs": len(pool) ** 2, "modes": 3,
                   "smallest_admissible_base_k4": best, "smallest_admissible_base_controls": ctl,
                   "pairs_admissible_at_15_or_less": len(small), "rules_consistent": rule_hits},
        "notes": f"Smallest base any pair admits on K4: {best}; on ten shuffles: {sorted(ctl)}. Pairs admissible at base 15 or less: {len(small)}; consistent rules among them: {rule_hits}.",
    }


def worked_example(ctx, key):
    A, B = keyword_mixed("SHADING"), keyword_mixed("INVISIBLE")
    lines = [f"plain  {A}", f"cipher {B}", "", "place  plain  carved  shift (Vigenere)"]
    for pos in (22, 23, 24, 25, 26):
        p, c = ctx.KNOWN[pos], ctx.K4[pos - 1]
        lines.append(f"{pos:>5}    {p}      {c}      {(B.index(c) - A.index(p)) % 26:>2}")
    return "\n".join(lines)
