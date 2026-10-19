"""Positive control for F2/1 (issue #73): one letter of a carved doublet is a null (0075).
0075 dropped each combination of the doublet places 19, 43, 47 and counted the periods 1-26 the known letters
leave consistent (and autokeys), against 10 shuffled copies; here the null is planted at 43 as a repeat of the
letter before it, and with 43 dropped the planted period must be the smallest live one and the live count must
stand above every copy. The plaintext gives the message in carved places; its letter at 43 is not sent. 0075's
encrypt() is a stub, so the plant makes its own ciphertext."""
import random

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F2/1"
EXPERIMENT = "0075"
WHAT = "A null at carved place 43 repeating the letter at 42, then Beaufort on plain standard / cipher KRYPTOS, period 11 with random shifts, on English from Carter"
P, NULL = 11, 43


def plant():
    rng = random.Random(7553)
    pt = english_plant(7553)
    k = [rng.randrange(26) for _ in range(P)]
    ct, j = [], 0
    for i in range(1, 98):
        if i == NULL:
            ct.append(ct[-1])
            continue
        ct.append(KRY[(k[j % P] - STD.index(pt[i - 1])) % 26])
        j += 1
    return {"plaintext": pt, "key": (f"null at {NULL}", "beau/std/kry", k), "ciphertext": "".join(ct)}


def found(result, plant):
    rows = [r for r in result.get("bounds", {}).get("results", []) if r["nulls"] == [NULL]]
    if not rows:
        return False, "no row for the null at 43"
    r = rows[0]
    ok = r["smallest_period"] == P and r["periodic_le26"] > max(r["controls"]["periodic_le26"])
    return ok, f"null at 43: smallest period {r['smallest_period']}, live P<=26 {r['periodic_le26']}, copies {r['controls']['periodic_le26']}"
