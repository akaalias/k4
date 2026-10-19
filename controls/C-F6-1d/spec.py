"""Positive control for F6/1 (issue #73): rail fence and redefence, then or before a periodic key (0113).
0113 ran rail fences of 2-48 rails at every start phase (rails in any order up to 6 rails), forward and inverse,
with a periodic key 1-26 after or before on 8 tableau classes, and listed K4's settings live below 20 (none); here a
planted redefence with the key before the move (order B), class std/std Beaufort, period 11 must be listed, with
period 11's count above every copy. The list holds the first 40 settings; copies have 0-3 below 20.
0113's encrypt() is a stub, so the plant makes its own ciphertext."""
import random
import re
import sys

from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.plants import english_plant

ITEM = "F6/1"
EXPERIMENT = "0113"
WHAT = "A random period-11 key on the standard table, Beaufort, then a redefence of 5 rails, offset 3, rails read 3-1-5-2-4 (forward), key before the move, on English from Carter"
L, SETTING = 11, (5, 3, (2, 0, 4, 1, 3))


def route(e):
    m = re.fullmatch(r"(\d+) rails, offset (\d+), rails read \[([\d, ]+)\]", e["rails"])
    wh = sys.modules["attack"].where_rails(int(m[1]), int(m[2]), tuple(int(x) - 1 for x in m[3].split(", ")))
    if e["dir"] == "inverse":
        inv = [0] * 97
        for i, j in enumerate(wh):
            inv[j] = i
        wh = inv
    return wh


def plant():
    rng = random.Random(7403)
    wh = sys.modules["attack"].where_rails(*SETTING)
    k = [rng.randrange(26) for _ in range(L)]
    pt = english_plant(7403)
    ct = [""] * 97
    for i, ch in enumerate(pt):
        ct[wh[i]] = STD[(k[i % L] - STD.index(ch)) % 26]
    return {"plaintext": pt, "key": ("5 rails offset 3 read 3-1-5-2-4", "order B", "std/std beau", k), "ciphertext": "".join(ct), "where": wh}


def found(result, plant):
    b = result.get("bounds", {})
    hit = [e for e in b.get("k4_live_below_20", []) if e["order"] == "B" and e["class"] == "std/std/beau"
           and e["period"] == L and route(e) == plant["where"]]
    n, mx = b.get("k4_live_by_period", {}).get("B", [0] * 26)[L - 1], b.get("controls_live_by_period_max", {}).get("B", [0] * 26)[L - 1]
    return bool(hit) and n > mx, (f"settings live below 20: {b.get('n_k4_live_below_20')}; the planted rails at {L}, order B: {bool(hit)}; "
                                  f"live at {L}: {n}, copies' max {mx}")
