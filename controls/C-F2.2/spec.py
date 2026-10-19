"""Positive control for F2.2 (issue #73): nulls placed by a rule, which a repeating key sees only as the gap (0182).
0182 tested every gap d = 0-29 (nulls between place 35 and 63), repeating and progressive keys of length 1-26 on
12 table rules, against 20 shuffled copies; here the planted gap must carry more live cells than every copy and its
smallest repeating key must be the planted length, shorter than any copy's at that gap (gaps 15 and 23 also give
length 8: a period-8 key cannot tell d from d + 8). Nulls follow a rule: one after every third message letter
between the runs (22 letters and 7 nulls fill places 35-63), and two before the first run; the key does not step on
a null. The plaintext gives the message in carved places; its letters at the null places are not sent. 0182's
encrypt() is a stub, so the plant makes its own ciphertext."""
import random

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F2.2"
EXPERIMENT = "0182"
WHAT = "Two nulls before the first run and one after every third message letter between the runs (gap d = 7), then Beaufort on plain KRYPTOS / cipher standard, repeating key of length 8 with random shifts, on English from Carter"
L, D = 8, 7


def plant():
    rng = random.Random(7556)
    pt = english_plant(7556)
    nulls = {5, 13}
    n = 0
    for i in range(35, 64):
        if n == 3:
            nulls.add(i)
            n = 0
        else:
            n += 1
    assert len([i for i in nulls if 35 <= i <= 63]) == D
    k = [rng.randrange(26) for _ in range(L)]
    ct, j = [], 0
    for i in range(1, 98):
        if i in nulls:
            ct.append(STD[rng.randrange(26)])
            continue
        ct.append(STD[(k[j % L] - KRY.index(pt[i - 1])) % 26])
        j += 1
    return {"plaintext": pt, "key": (f"nulls at {sorted(nulls)}", "beau/kry/std", k), "ciphertext": "".join(ct)}


def found(result, plant):
    g = result.get("bounds", {}).get("per_gap", {}).get(D, {})
    cs = [x for x in g.get("copies_smallest_repeating", []) if x is not None]
    ok = g.get("k4_live", 0) > g.get("copies_max", 0) and g.get("k4_smallest_repeating") == L and all(x > L for x in cs)
    return ok, (f"gap {D}: live {g.get('k4_live')} (copies {g.get('copies_min')}-{g.get('copies_max')}), smallest repeating key "
                f"{g.get('k4_smallest_repeating')} (copies' shortest {min(cs, default=None)}); gaps above every copy {result.get('bounds', {}).get('gaps_k4_above_every_copy')}")
