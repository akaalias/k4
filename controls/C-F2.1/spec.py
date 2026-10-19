"""Positive control for F2.1 (issue #73): letter nulls, then a period 24 or 25 key, read for words (0181).
0181 struck out every copy of one or two letters outside the known runs, kept the settings at periods 24 and 25
that the known letters leave consistent, and read the forced plaintext outside the runs for dictionary words of 6+
letters; here the planted null letter, rule and period must be kept and its forced reading must be the planted
message and hold a word. The nulls are drawn between the runs (35-63); the null letter is one the enciphered
message does not use outside the runs. The plaintext gives the message in carved places; its letters at the null
places are not sent. 0181's encrypt() is a stub, so the plant makes its own ciphertext."""
import random

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F2.1"
EXPERIMENT = "0181"
WHAT = "Five nulls at random places between the known runs, all one letter, then Vigenere on plain standard / cipher KRYPTOS, period 24 with random shifts, on English from Carter"
P = 24
RANGES = set(range(22, 35)) | set(range(64, 75))


def plant():
    rng = random.Random(7555)
    pt = english_plant(7555)
    outside = [i for i in range(1, 98) if i not in RANGES]
    while True:
        nulls = set(rng.sample(range(35, 64), 5))
        k = [rng.randrange(26) for _ in range(P)]
        ct, j = [], 0
        for i in range(1, 98):
            if i in nulls:
                ct.append(None)
                continue
            ct.append(KRY[(STD.index(pt[i - 1]) + k[j % P]) % 26])
            j += 1
        free = [c for c in STD if c not in {ct[i - 1] for i in outside if i not in nulls}]
        if free:
            break
    nl = free[0]
    ct = "".join(nl if c is None else c for c in ct)
    msg = "".join(pt[i - 1] for i in range(1, 98) if i not in nulls)
    return {"plaintext": pt, "key": (f"nulls {nl} at {sorted(nulls)}", "vig/std/kry", k), "ciphertext": ct, "null": nl, "message": msg}


def found(result, plant):
    b = result.get("bounds", {})
    msg = plant["message"]
    hit = [e for e in b.get("k4_examples", []) if e["mask"] == plant["null"] and e["rule"] == "vig/std/kry" and e["P"] == P
           and all(f == "." or f == m for f, m in zip(e["forced"], msg))]
    return bool(hit), (f"fitting settings {b.get('fitting_settings', {}).get('k4')}, with a word {b.get('settings_with_a_word', {}).get('k4')} "
                       f"(copies {b.get('settings_with_a_word', {}).get('copies')}); the planted null {plant['null']} at {P} reading the message: "
                       f"{[(e['longest'], e['words']) for e in hit]}")
