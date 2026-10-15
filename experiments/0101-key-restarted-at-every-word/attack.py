"""Experiment 0101. See program.md for the contract."""

EXPERIMENT = {
    "slug": "key-restarted-at-every-word",
    "title": "An interrupted key: the key word starts again at the first letter of every word of the message",
    "family": "1-keyed-periodic",
    "parent": "0001-crib-consistent-periods",
    "changed": "Every periodic test so far ran the key straight through the message. A classical hand variant restarts the key word at each new plaintext word, so the key letter depends on the place inside the word, not in the message. The cribs supply the word breaks (EAST NORTH EAST or EAST NORTHEAST; BERLIN CLOCK or BERLINCLOCK), which makes the test exact.",
    "hypothesis_expert": (
        "Scheidt: 'simple, can be remembered' (C5) and he 'masked the English language' (C4); an interrupted key is a "
        "standard field method (Friedman's 'interrupted key') that hides the period. Model: key letter of a plaintext "
        "letter = keyword[(offset inside its word) mod L], L = 1-26, the keyword restarting at each word; EAST and BERLIN "
        "assumed to start words (E at 22 and B at 64). Segmentations: EAST|NORTH|EAST, EAST|NORTHEAST, EASTNORTHEAST as "
        "one word, crossed with BERLIN|CLOCK and BERLINCLOCK (five splits). Eight tableau classes (standard or KRYPTOS plain and cipher "
        "alphabets, Beaufort or not). Known letters with the same in-word offset mod L must force the same key value. "
        "Ten shuffled coppers."
    ),
    "hypothesis_eli5": (
        "With a secret word as key, one usually runs it along the whole message. A trick to hide the pattern is to start "
        "the secret word again at the beginning of every word of the message. We know where some words begin, because "
        "the known letters spell EAST, NORTH, EAST, BERLIN and CLOCK. So for each length of secret word we can check "
        "whether starting it over at each of those words fits the carved letters."
    ),
    "prediction": (
        "No segmentation, key length or table rule fits all 24 known letters except at key lengths long enough that no "
        "two known letters share a key letter (L at least 9 for the segmentations with NORTHEAST, 6 otherwise); counts at "
        "those lengths match the coppers'. Zero candidates."
    ),
    "method": (
        "1. For each segmentation, give each known letter its offset inside its word. 2. For each key length and class, "
        "compute the forced key value at each known letter and check that letters with equal offset mod L agree. "
        "3. Record the smallest consistent L and the number of checks. 4. Repeat on ten shuffled coppers."
    ),
    "walkthrough": (
        "1. Split the known letters into words: EAST at 22-25, NORTH at 26-30, EAST at 31-34, BERLIN at 64-69, CLOCK at 70-74. "
        "2. Restart the key at each word: E at 22, N at 26, E at 31, B at 64 and C at 70 all take the first key letter. "
        "3. On the sculpture's alphabet with Vigenere, the key letter for E to F at 22 and for N to Q at 26 must then be the same. "
        "4. Do this for each offset, key length 1-26, the other word splits and table rules."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
LMAX = 26
ALPH = {"std": STD, "kry": KRY}
N_CONTROLS = 10

SEGMENTS = {
    "EAST|NORTH|EAST + BERLIN|CLOCK": [(22, 4), (26, 5), (31, 4), (64, 6), (70, 5)],
    "EAST|NORTH|EAST + BERLINCLOCK": [(22, 4), (26, 5), (31, 4), (64, 11)],
    "EAST|NORTHEAST + BERLIN|CLOCK": [(22, 4), (26, 9), (64, 6), (70, 5)],
    "EAST|NORTHEAST + BERLINCLOCK": [(22, 4), (26, 9), (64, 11)],
    "EASTNORTHEAST + BERLIN|CLOCK": [(22, 13), (64, 6), (70, 5)],
}


def offsets(seg):
    off = {}
    for start, n in seg:
        for i in range(n):
            off[start + i] = i
    return off


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    places = sorted(known)
    rng = random.Random(101)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    classes = [(pa, ca, beau) for pa in ALPH for ca in ALPH for beau in (False, True)]
    results = {}
    k4_live = []
    for sname, seg in SEGMENTS.items():
        off = offsets(seg)
        assert sorted(off) == places
        per = []
        for t, txt in enumerate(texts):
            smallest = []
            for pa, ca, beau in classes:
                PI = {c: i for i, c in enumerate(ALPH[pa])}; CI = {c: i for i, c in enumerate(ALPH[ca])}
                f = {q: ((CI[txt[q - 1]] + PI[known[q]]) % 26 if beau else (CI[txt[q - 1]] - PI[known[q]]) % 26) for q in places}
                first = None
                for L in range(1, LMAX + 1):
                    slots, ok, checks = {}, True, 0
                    for q in places:
                        s = off[q] % L
                        if s in slots:
                            checks += 1
                            if slots[s] != f[q]:
                                ok = False; break
                        else:
                            slots[s] = f[q]
                    if ok and checks:
                        if first is None:
                            first = (L, checks)
                        if t == 0:
                            k4_live.append({"segmentation": sname, "class": f"{pa}/{ca}/{'beau' if beau else 'vig-var'}", "L": L, "checks": checks})
                smallest.append(first[0] if first else None)
            per.append(min([x for x in smallest if x] or [None]))
        results[sname] = {"k4_smallest_L_with_checks": per[0], "controls": per[1:]}
    k4_low = [r for r in k4_live if r["checks"] >= 3]
    bounds = {"family": "interrupted key restarting at every plaintext word", "segmentations": list(SEGMENTS),
              "key_lengths": [1, LMAX], "classes": 8, "by_segmentation": results,
              "k4_live_with_3_plus_checks": k4_low[:40], "n_k4_live_with_3_plus_checks": len(k4_low),
              "controls": f"{N_CONTROLS} shuffled coppers (seed 101), identical test"}
    notes = ("Smallest key length consistent with at least one check (None: no length 1-26 fits), K4 vs controls: "
             + "; ".join(f"{k}: {v['k4_smallest_L_with_checks']} vs {v['controls']}" for k, v in results.items())
             + f". K4 settings consistent with 3+ checks: {len(k4_low)}.")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    I = {c: i for i, c in enumerate(KRY)}
    off = offsets(SEGMENTS["EAST|NORTH|EAST + BERLIN|CLOCK"])
    lines = ["words EAST NORTH EAST BERLIN CLOCK, key restarted at each; sculpture's alphabet, Vigenere", "",
             "place  letter  copper  offset in word  key value"]
    for q in sorted(known):
        lines.append(f"{q:>5}  {known[q]:>6}  {ct[q - 1]:>6}  {off[q]:>14}  {(I[ct[q - 1]] - I[known[q]]) % 26:>9}")
    return "\n".join(lines)
