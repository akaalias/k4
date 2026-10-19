"""Positive control for F6.3b (issue #73): mixed triples of the four column readings at widths 25-96 (0158).
0158 ran every mixed reading triple with at least one width 25-96 (105,548,253 distinct routes, compiled), forward and
inverse, with a periodic key 1-26 after or before on 8 tableau classes; K4's shortest live key was 18 after the move,
as the copies. Here the planted triple, key before the move (order B), class kry/kry, period 8 must be among the 40
lowest-period settings listed, and K4's place must stand above every copy at period 8. Copies' shortest live keys were
17-19, so nothing below 8 can push the plant off the list. 0158's encrypt() is real and makes the planted ciphertext."""
import random
import sys

from kryptos.plants import english_plant

ITEM = "F6.3b"
EXPERIMENT = "0158"
WHAT = "A random period-8 key on the KRYPTOS table, Vigenere, then rows of 40 read right first bottom up, rows of 7 turned clockwise, rows of 31 turned anticlockwise (forward), key before the move, on English from Carter"
STAGES, L = [(40, "colr"), (7, "cw"), (31, "ccw")], 8


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
    rng = random.Random(7413)
    k = [rng.randrange(26) for _ in range(L)]
    name = [x for w, r in STAGES for x in (r, w)]
    return {"plaintext": english_plant(7413), "key": {"stages": STAGES, "order": "B", "alphabet": "KRY", "key": k},
            "where": route(name, "fwd")}


def found(result, plant):
    b = result.get("bounds", {})
    hit = [e for e in b.get("k4_live_below_20", []) if e["order"] == "B" and e["class"] == "kry/kry/vig-var"
           and e["period"] == L and route(e["route"], e["dir"]) == plant["where"]]
    above = ("B", L) in [tuple(c) for c in b.get("cells_k4_above_every_copper", [])]
    return bool(hit) and above, (f"shortest live {b.get('k4_shortest_live')}, copies {b.get('coppers_shortest_live')}; the planted triple at {L}, "
                                 f"order B: {bool(hit)}; B{L} above every copy: {above}; first stages done {b.get('first_stages_done')} of {b.get('first_stages_total')}")
