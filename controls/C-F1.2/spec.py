"""Positive control for F1.2 (issue #73): two unknown alphabets (Quagmire IV), the exact search (0123).
0123 decided exactly for every key length 1-26 whether any pair of alphabets fits the 24 known letters, and found
none at 1-7, 9-12, 14, 15, 17, 18, 21, 22, 25 on K4; here it must find the planted length 10 fitting."""
import random

from kryptos.plants import english_plant

ITEM = "F1.2"
EXPERIMENT = "0123"
WHAT = "Quagmire IV, two random alphabets, key length 10 with random shifts, on English from Carter"
L = 10


def plant():
    rng = random.Random(7351)
    pa = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"); rng.shuffle(pa)
    ca = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"); rng.shuffle(ca)
    return {"plaintext": english_plant(7351), "key": {"plain": "".join(pa), "cipher": "".join(ca), "shifts": [rng.randrange(26) for _ in range(L)]}}


def found(result, plant):
    b = result.get("bounds", {})
    fits = b.get("k4_fits", [])
    return L in fits, f"lengths that fit the plant: {fits}; undecided {b.get('k4_undecided')}"
