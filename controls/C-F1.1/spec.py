"""Positive control for F1.1 (issue #73): one unknown alphabet on both sides, added form, key length 9.
0119's exact search found no added-form length that fits K4; here it must find length 9 on a planted text."""
import random

from kryptos.plants import english_plant

ITEM = "F1.1"
EXPERIMENT = "0119"
WHAT = "Quagmire III, added form, a random alphabet, key length 9 with random shifts, on English from Carter"
L = 9


def plant():
    rng = random.Random(7301)
    alpha = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    rng.shuffle(alpha)
    return {"plaintext": english_plant(7301), "key": ("".join(alpha), [rng.randrange(26) for _ in range(L)])}


def found(result, plant):
    fits = result.get("bounds", {}).get("k4_fits", {}).get("V", [])
    return L in fits, f"added-form lengths that fit the planted text: {fits}"
