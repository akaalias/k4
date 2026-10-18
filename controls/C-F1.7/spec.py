"""Positive control for F1.7 (issue #73): autokey on one unknown alphabet, no move (0149).
0149 decided exactly, for ciphertext and plaintext autokey, three forms and every lag 1-96, whether any one
alphabet fits the 24 known letters; on K4 the added-form ciphertext autokey fits only at lags 37 and up. Here it
must fit at the planted lag 9. Enciphered with 0149's own encipher(); its encrypt() is a stub."""
import random
import sys

from kryptos.plants import english_plant

ITEM = "F1.7"
EXPERIMENT = "0149"
WHAT = "Ciphertext autokey, added form, lag 9, random alphabet on both sides, random primer, on English from Carter"
L = 9


def plant():
    rng = random.Random(7381)
    al = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"); rng.shuffle(al); al = "".join(al)
    primer = [rng.choice(al) for _ in range(L)]
    pt = english_plant(7381)
    ct = sys.modules["attack"].encipher(pt, al, L, "ct", "V", primer)
    return {"plaintext": pt, "key": (al, L, "ct", "V", "".join(primer)), "ciphertext": ct}


def found(result, plant):
    s = result.get("bounds", {}).get("summary", {}).get("ct/V", {})
    lags = s.get("k4_fit_lags", [])
    return L in lags, f"ciphertext autokey, added form: lags that fit the plant {lags[:20]}{'...' if len(lags) > 20 else ''}"
