"""Positive control for F6/3 (issue #73): mixed column readings, two and three stages, then a periodic key (0134).
0134 ran every pair of the four column readings (cw, ccw, col, colr) at widths 2-96 and every mixed triple at widths
2-24, forward and inverse, with a periodic key 1-26 after or before on 8 tableau classes, and listed K4's settings live
below 20 (none); here the planted triple, order A, class std/std, period 10 must be listed and K4's place must stand
above every copy at period 10. The list is the 40 lowest periods; copies had 0-1 below 20, so the plant is not cut off.
0134's encrypt() is real (one alphabet, Vigenere), and makes the planted ciphertext."""
import random
import sys

from kryptos.plants import english_plant

ITEM = "F6/3"
EXPERIMENT = "0134"
WHAT = "Rows of 9 read by columns left first top down, then rows of 13 turned anticlockwise, then rows of 6 read right first bottom up (forward), then a random period-10 key on the standard table, Vigenere, key after the move, on English from Carter"
STAGES, L = [(9, "col"), (13, "ccw"), (6, "colr")], 10


def route(name, d):
    wo = sys.modules["attack"].where_of
    wh = list(range(97))
    for r, w in zip(name[0::2], name[1::2]):
        m = wo(w, r)
        wh = [m[j] for j in wh]
    if d == "inv":
        inv = [0] * 97
        for i, j in enumerate(wh):
            inv[j] = i
        wh = inv
    return wh


def plant():
    rng = random.Random(7412)
    k = [rng.randrange(26) for _ in range(L)]
    name = tuple(x for w, r in STAGES for x in (r, w))
    return {"plaintext": english_plant(7412), "key": {"stages": STAGES, "order": "A", "alphabet": "STD", "key": k},
            "where": route(name, "fwd")}


def found(result, plant):
    b = result.get("bounds", {})
    hit = [e for e in b.get("k4_live_below_20", []) if e["order"] == "A" and e["class"] == "std/std/vig-var"
           and e["period"] == L and route(tuple(e["route"]), e["dir"]) == plant["where"]]
    above = ("A", L) in [tuple(c) for c in b.get("cells_k4_above_every_copper", [])]
    return bool(hit) and above, (f"settings live below 20: {b.get('k4_settings_live_below_20')}; the planted triple at {L}, order A: {bool(hit)}; "
                                 f"A{L} above every copy: {above}; first stages done {b.get('first_stages_done')} of {b.get('first_stages_total')}")
