"""Positive control for F6/1 (issue #73): Myszkowski keyed by the dictionary, before or after a periodic key (0111).
0111 ran Myszkowski under every dictionary word with a repeated letter (171,995 keys), forward and inverse, with a
periodic key 1-26 after or before on 8 tableau classes, and listed K4's settings live below 20 (none); here the planted
key before the move (order B), class kry/kry, period 10 must be listed with the planted Myszkowski key, and period 10's
count must stand above every copy. The list holds the first 40 settings; copies have 0-3 below 20.
0111's encrypt() is a stub, so the plant makes its own ciphertext."""
import random
import sys

from kryptos.facts import KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F6/1"
EXPERIMENT = "0111"
WHAT = "A random period-10 key on the KRYPTOS table, Vigenere, then Myszkowski under BALLOON (forward), key before the move, on English from Carter"
WORD, L = "BALLOON", 10


def route(e):
    a = sys.modules["attack"]
    wh = a.where_myszkowski(a.myszkowski_key(e["word"]))
    if e["dir"] == "inverse":
        inv = [0] * 97
        for i, j in enumerate(wh):
            inv[j] = i
        wh = inv
    return wh


def plant():
    rng = random.Random(7405)
    a = sys.modules["attack"]
    wh = a.where_myszkowski(a.myszkowski_key(WORD))
    k = [rng.randrange(26) for _ in range(L)]
    pt = english_plant(7405)
    ct = [""] * 97
    for i, ch in enumerate(pt):
        ct[wh[i]] = KRY[(KRY.index(ch) + k[i % L]) % 26]
    return {"plaintext": pt, "key": (WORD, "order B", "kry/kry vig", k), "ciphertext": "".join(ct), "where": wh}


def found(result, plant):
    b = result.get("bounds", {})
    hit = [e for e in b.get("k4_live_below_20", []) if e["order"] == "B" and e["class"] == "kry/kry/vig-var"
           and e["period"] == L and route(e) == plant["where"]]
    n, mx = b.get("k4_live_by_period", {}).get("B", [0] * 26)[L - 1], b.get("controls_live_by_period_max", {}).get("B", [0] * 26)[L - 1]
    return bool(hit) and n > mx, (f"settings live below 20: {b.get('n_k4_live_below_20')}; the planted Myszkowski key at {L}, order B: {bool(hit)}; "
                                  f"live at {L}: {n}, copies' max {mx}")
