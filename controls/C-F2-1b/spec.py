"""Positive control for F2/1 (issue #73): every copy of one carved letter outside the known runs is a null (0057).
0057 struck out, for each letter and pair of letters, every copy outside the runs, and found the smallest period
the 24 known letters leave consistent on 4 table pairs x 3 modes; here the planted null letter must give the
planted period. Only nulls between the runs (35-63) move one known run against the other, so the nulls are drawn
there (nulls before or after both runs change nothing a periodic key can see). The null letter is one the enciphered message does not
use outside the runs, so striking every copy removes exactly the nulls. The plaintext gives the message in carved
places; its letters at the null places are not sent. 0057's encrypt() is a stub, so the plant makes its own
ciphertext."""
import random

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F2/1"
EXPERIMENT = "0057"
WHAT = "Six nulls at random places between the known runs (35-63), all one letter, then Vigenere on plain KRYPTOS / cipher standard, period 8 with random shifts, on English from Carter"
P = 8
RANGES = set(range(22, 35)) | set(range(64, 75))


def plant():
    rng = random.Random(7551)
    pt = english_plant(7551)
    outside = [i for i in range(1, 98) if i not in RANGES]
    while True:
        nulls = set(rng.sample(range(35, 64), 6))
        k = [rng.randrange(26) for _ in range(P)]
        ct, j = [], 0
        for i in range(1, 98):
            if i in nulls:
                ct.append(None)
                continue
            ct.append(STD[(KRY.index(pt[i - 1]) + k[j % P]) % 26])
            j += 1
        used = {ct[i - 1] for i in outside if i not in nulls}
        free = [c for c in STD if c not in used]
        if free:
            break
    nl = free[0]
    ct = "".join(nl if c is None else c for c in ct)
    return {"plaintext": pt, "key": (f"nulls {nl} at {sorted(nulls)}", "vig/kry/std", k), "ciphertext": ct, "null": nl}


def found(result, plant):
    rows = result.get("bounds", {}).get("masks_below_26", [])
    hit = [r for r in rows if r["letters"] == plant["null"] and r["period"] == P]
    return bool(hit), f"masks below 26: {rows[:5]}; the null letter {plant['null']} at period {P}: {bool(hit)}"
