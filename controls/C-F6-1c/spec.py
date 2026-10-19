"""Positive control for F6/1 (issue #73): two quarter turns in mixed senses, then a periodic key (0099).
0099 ran every cw-ccw, ccw-cw and ccw-ccw pair of quarter turns at widths 2-96 (cw-cw done before), forward and
inverse, with a periodic key 1-26 after or before on 8 tableau classes, and listed K4's settings live below 20 (none);
here the planted turns, order A, class kry/kry and period 7 must be listed, with period 7's count above every copy.
The list holds the first 40 settings; copies have 0-3 below 20. 0099's encrypt() is a stub, so the plant makes its own
ciphertext."""
import random
import re
import sys

from kryptos.facts import KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F6/1"
EXPERIMENT = "0099"
WHAT = "A clockwise quarter turn in rows of 9, then an anticlockwise one in rows of 12 (forward), then a random period-7 key on the KRYPTOS table, Vigenere, key after the move, on English from Carter"
L = 7


def route(e):
    m = re.fullmatch(r"(cw|ccw) (\d+), (cw|ccw) (\d+)( inverse)?", e["turns"])
    wh = sys.modules["attack"].where_of_turns([(int(m[2]), m[1]), (int(m[4]), m[3])])
    if m[5]:
        inv = [0] * 97
        for i, j in enumerate(wh):
            inv[j] = i
        wh = inv
    return wh


def plant():
    rng = random.Random(7402)
    wh = sys.modules["attack"].where_of_turns([(9, "cw"), (12, "ccw")])
    k = [rng.randrange(26) for _ in range(L)]
    pt = english_plant(7402)
    moved = [""] * 97
    for i, j in enumerate(wh):
        moved[j] = pt[i]
    ct = "".join(KRY[(KRY.index(ch) + k[j % L]) % 26] for j, ch in enumerate(moved))
    return {"plaintext": pt, "key": ("cw 9, ccw 12", "order A", "kry/kry vig", k), "ciphertext": ct, "where": wh}


def found(result, plant):
    b = result.get("bounds", {})
    hit = [e for e in b.get("k4_live_below_20", []) if e["order"] == "A" and e["class"] == "kry/kry/vig-var"
           and e["period"] == L and route(e) == plant["where"]]
    n, mx = b.get("k4_live_by_period", {}).get("A", [0] * 26)[L - 1], b.get("controls_live_max", {}).get("A", [0] * 26)[L - 1]
    return bool(hit) and n > mx, (f"settings live below 20: {b.get('n_k4_live_below_20')}; the planted turns at {L}, order A: {bool(hit)}; "
                                  f"live at {L}: {n}, copies' max {mx}")
