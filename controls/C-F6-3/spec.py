"""Positive control for F6/3 (issue #73): three clockwise quarter turns, then or before a periodic key (0083).
0083 ran every triple of clockwise quarter turns at widths 2-96 (1,714,024 distinct routes), forward and inverse, with
a periodic key 1-26 after or before on 8 tableau classes, and listed K4's settings live below 20 (one, at 18); here the
planted triple with the key before the turns (order B), class kry/std, period 9 must be listed, with period 9's count
above every shuffled copy. The list holds the first 40 settings; copies had none below 20.
0083's encrypt() is a stub, so the plant makes its own ciphertext with 0083's own turn_perm()."""
import random
import sys

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F6/3"
EXPERIMENT = "0083"
WHAT = "A random period-9 key, plain KRYPTOS / cipher standard, Vigenere, then clockwise quarter turns in rows of 11, 7 and 15 (forward), key before the turns, on English from Carter"
WIDTHS, L = (11, 7, 15), 9


def route(widths, d):
    tp = sys.modules["attack"].turn_perm
    a, b, c = (tp(w) for w in widths)
    wh = [c[b[a[i]]] for i in range(97)]
    if d == "inv":
        inv = [0] * 97
        for i, j in enumerate(wh):
            inv[j] = i
        wh = inv
    return wh


def plant():
    rng = random.Random(7411)
    wh = route(WIDTHS, "fwd")
    k = [rng.randrange(26) for _ in range(L)]
    pt = english_plant(7411)
    ct = [""] * 97
    for i, ch in enumerate(pt):
        ct[wh[i]] = STD[(KRY.index(ch) + k[i % L]) % 26]
    return {"plaintext": pt, "key": ("cw 11, cw 7, cw 15", "order B", "kry/std vig", k), "ciphertext": "".join(ct), "where": wh}


def found(result, plant):
    b = result.get("bounds", {})
    hit = [e for e in b.get("k4_live_below_20", []) if e["order"] == "B" and e["class"] == "kry/std/vig-var"
           and e["period"] == L and route(e["widths"], e["dir"]) == plant["where"]]
    n, mx = b.get("k4_live_by_period", {}).get("B", [0] * 26)[L - 1], b.get("controls_live_by_period_max", {}).get("B", [0] * 26)[L - 1]
    return bool(hit) and n > mx, (f"settings live below 20: {b.get('n_k4_live_below_20')}; the planted triple at {L}, order B: {bool(hit)}; "
                                  f"live at {L}: {n}, copies' max {mx}; stopped at {b.get('stopped_at')}")
