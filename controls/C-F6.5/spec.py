"""Positive control for F6.5 (issue #73): direction words as routes through the grid (0159).
0159 read the grid along each of the 16 compass points at every width (lines either way) and along every pair of
E/ENE/NE readings at widths 2-48, forward and inverse, with a periodic key 1-26 after or before on 8 tableau classes;
K4's shortest live key was 21 after, 25 before, as the copies. Here the planted ENE-then-NE route with the key before
it (order B), class kry/kry, period 8 must be among the 40 lowest-period settings listed, and K4's place must stand
above every copy at period 8. 0159's encrypt() is real and makes the planted ciphertext."""
import random
import sys

from kryptos.plants import english_plant

ITEM = "F6.5"
EXPERIMENT = "0159"
WHAT = "A random period-8 key on the KRYPTOS table, Vigenere, then the text read east-northeast in rows of 11, then northeast in rows of 9 with the lines in reverse order, key before the move, on English from Carter"
STAGES, L = [(11, "ENE", False), (9, "NE", True)], 8


def route(name, d):
    a = sys.modules["attack"]
    wh = list(range(97))
    stages = [(name[1], name[2] == "True", int(name[3]))]
    if name[0] == "double":
        stages.append((name[4], name[5] == "True", int(name[6])))
    for dd, rev, w in stages:
        m = a.where(a.reading(97, w, dd, rev))
        wh = [m[j] for j in wh]
    if d == "inv":
        wh = a.where(wh)
    return wh


def plant():
    rng = random.Random(7417)
    k = [rng.randrange(26) for _ in range(L)]
    return {"plaintext": english_plant(7417), "key": {"stages": STAGES, "order": "B", "alphabet": "KRY", "key": k},
            "where": route(["double", "ENE", "False", "11", "NE", "True", "9"], "fwd")}


def found(result, plant):
    b = result.get("bounds", {})
    hit = [e for e in b.get("k4_live_below_20", []) if e["order"] == "B" and e["class"] == "kry/kry/vig-var"
           and e["period"] == L and route(e["route"], e["dir"]) == plant["where"]]
    above = ("B", L) in [tuple(c) for c in b.get("cells_k4_above_every_copper", [])]
    return bool(hit) and above, (f"shortest live {b.get('k4_shortest_live')}, copies {b.get('coppers_shortest_live')}; the planted route at {L}, "
                                 f"order B: {bool(hit)}; B{L} above every copy: {above}")
