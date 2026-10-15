"""Experiment 0075. See program.md for the contract."""

EXPERIMENT = {
    "slug": "doublets-as-nulls",
    "title": "Are the doubled letters fillers? Three of them carry known letters; the other three are struck out",
    "family": "2-masked-then-keyed",
    "parent": "0057-letter-nulls-outside-the-cribs",
    "changed": "The six doublets are the copper's strangest local feature. A doubled letter could be a filler, a letter written twice or a null. Three of them sit inside the known stretches and carry different known letters, so they cannot be fillers. The other three, BB, SS and ZZ, are struck out one letter each, in every combination, and the shorter text is tested with a repeating key, the self-feeding autokey, and both.",
    "hypothesis_expert": (
        "Family 2, nulls tied to a visible feature (C17(b), C18(a): 'a bit of stego', a working text of other "
        "than 97 letters; C11: 'the other 91 characters'). Structural part: the doublets QQ (26-27), SS "
        "(33-34) and TT (68-69) carry the known pairs N,O; S,T; I,N, so neither letter of any of them can be "
        "a null, a repeated letter or filler, and any reading of the 6 doublets as 6 nulls (97 - 6 = 91) is "
        "dead. Search part: one letter of BB (19-20), SS (43-44) and ZZ (47-48), in each of the 7 non-empty "
        "combinations, removed as a null; the cribs keep their carved letters and move to the reduced "
        "positions. A null before both cribs (BB) leaves every periodic test unchanged and matters only for "
        "the autokey; nulls between the cribs (43, 47) change the cross-crib distances. Systems on each "
        "reduced text: periodic key, periods 1-52; ciphertext autokey with a constant, every lag; autokey plus "
        "a periodic key up to 26; plain, cipher and key alphabets standard or KRYPTOS, Vigenere or Beaufort, "
        "either sign. Controls: ten shuffled coppers with the same positions removed."
    ),
    "hypothesis_eli5": (
        "The copper has six places where a letter repeats its neighbour. One idea is that some of these are "
        "fillers, letters added to pad the text. Three of them sit inside EASTNORTHEAST and BERLINCLOCK, and "
        "each of their two letters stands for a different known letter, so they cannot be padding. The other "
        "three, BB, SS and ZZ, could be. We strike out one letter of each, in every combination, and test the "
        "shorter text with the simplest ciphers, against scrambled coppers treated the same way."
    ),
    "prediction": (
        "No combination makes a periodic key of period 24 or less consistent; the autokey forms have no "
        "survivor with three or more checks beyond the controls. Zero candidates pass."
    ),
    "method": (
        "1. List the 7 combinations of nulls from BB, SS (43-44) and ZZ. 2. Remove them and move each known "
        "letter to its reduced place. 3. Run the periodic consistency test at every period up to 52, and the "
        "autokey tests at every lag. 4. Repeat on ten shuffled coppers with the same places removed."
    ),
    "walkthrough": (
        "1. Strike out the S at place 43 as a null. 2. Every carved letter after it moves one place left: the "
        "B of BERLIN, carved N at place 64, becomes place 63 of the 96-letter text. 3. Places 22 and 64 were "
        "42 apart; now they are 41 apart, so under a periodic key they share a slot at different periods than "
        "before. 4. Places 22 and 29 are both before the null and stay 7 apart. 5. Run the periodic test on "
        "the 96 letters as usual. 6. Repeat for every combination of nulls."
    ),
}

import random
from itertools import combinations
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
PMAX = 52
ALPH = {"std": STD, "kry": KRY}
NULL_CANDIDATES = [19, 43, 47]          # carved places: one letter of BB, SS, ZZ


def reduce(ct, known, nulls):
    keep = [q for q in range(1, N + 1) if q not in nulls]
    newpos = {q: k for k, q in enumerate(keep)}      # 0-based reduced index
    text = "".join(ct[q - 1] for q in keep)
    kn = [(newpos[q], p) for q, p in sorted(known.items())]
    return text, kn


def classes():
    for pa in ALPH:
        for ca in ALPH:
            for ka in ALPH:
                for mode in ("vig", "beau"):
                    for s in (1, -1):
                        yield pa, ca, ka, mode, s


def sweep(text, kn):
    per, auto, withp = {}, {}, {}
    for pa, ca, ka, mode, s in classes():
        PI = {c: i for i, c in enumerate(ALPH[pa])}; CI = {c: i for i, c in enumerate(ALPH[ca])}; KI = {c: i for i, c in enumerate(ALPH[ka])}
        T = [((CI[text[i]] - PI[p]) if mode == "vig" else (CI[text[i]] + PI[p])) % 26 for i, p in kn]
        if ka == "std" and s == 1:                         # the periodic test does not depend on ka or s
            for P in range(1, PMAX + 1):
                slot = {}; ok = True
                for (i, _), t in zip(kn, T):
                    if slot.setdefault(i % P, t) != t:
                        ok = False; break
                if ok:
                    per[P] = per.get(P, 0) + 1
        for L in range(1, len(text)):
            d = [(i, (t - s * KI[text[i - L]]) % 26) for (i, _), t in zip(kn, T) if i - L >= 0]
            if len(d) < 2:
                continue
            if len({v for _, v in d}) == 1:
                c = min(len(d) - 1, 5); auto[c] = auto.get(c, 0) + 1
            for P in range(2, 27):
                slot = {}; ok = True
                for i, v in d:
                    if slot.setdefault(i % P, v) != v:
                        ok = False; break
                if ok and len(d) - len(slot) >= 1:
                    c = min(len(d) - len(slot), 5); withp[c] = withp.get(c, 0) + 1
    return per, auto, withp


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    inside = [(q, ct[q - 1], known.get(q), known.get(q + 1)) for q in range(1, N) if ct[q - 1] == ct[q] and q in known and q + 1 in known]
    combos = [set(c) for r in (1, 2, 3) for c in combinations(NULL_CANDIDATES, r)]
    rng = random.Random(75)
    shuffles = []
    for _ in range(10):
        sh = list(ct); rng.shuffle(sh); shuffles.append("".join(sh))
    rows = []
    for nulls in combos:
        t, kn = reduce(ct, known, nulls)
        per, auto, withp = sweep(t, kn)
        cper, cauto, cwith = [], [], []
        for sh in shuffles:
            t2, kn2 = reduce(sh, known, nulls)
            a, b, c = sweep(t2, kn2)
            cper.append(sum(v for P, v in a.items() if P <= 26)); cauto.append(sum(v for k, v in b.items() if k >= 2)); cwith.append(sum(v for k, v in c.items() if k >= 3))
        rows.append({"nulls": sorted(nulls), "periodic_le26": sum(v for P, v in per.items() if P <= 26), "smallest_period": min(per) if per else None,
                     "autokey_2plus_checks": sum(v for k, v in auto.items() if k >= 2), "autokey_periodic_3plus": sum(v for k, v in withp.items() if k >= 3),
                     "controls": {"periodic_le26": cper, "autokey_2plus": cauto, "autokey_periodic_3plus": cwith}})
        if ctx.time_left() < 30:
            break
    return {
        "candidates": [],
        "bounds": {"family": "doublet letters as nulls", "inside_crib_doublets": [{"place": q, "carved": c, "known": a + b} for q, c, a, b in inside],
                   "null_combinations": len(combos), "periods": f"1-{PMAX}", "results": rows},
        "notes": f"Doublets inside the cribs carrying two different known letters: {[(q, c * 2, a + b) for q, c, a, b in inside]}, so not nulls. "
                 + "; ".join(f"nulls {r['nulls']}: periodic P<=26 {r['periodic_le26']} (controls {min(r['controls']['periodic_le26'])}-{max(r['controls']['periodic_le26'])}), "
                             f"autokey 2+ checks {r['autokey_2plus_checks']} ({min(r['controls']['autokey_2plus'])}-{max(r['controls']['autokey_2plus'])}), "
                             f"autokey+periodic 3+ {r['autokey_periodic_3plus']} ({min(r['controls']['autokey_periodic_3plus'])}-{max(r['controls']['autokey_periodic_3plus'])})" for r in rows) + ".",
    }


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    t, kn = reduce(ctx.K4, ctx.KNOWN, {43})
    d = dict(kn)
    return (f"null at carved place 43 (S): text of {len(t)} letters\n"
            f"carved place 22 (F, known E) -> reduced place {23 - 1}; carved place 64 (N, known B) -> reduced place {[i for i, p in kn][13] + 1}\n"
            f"distance 22 to 64: 42 before, {[i for i, p in kn][13] - [i for i, p in kn][0]} after")
