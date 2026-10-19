"""Positive control for F6/1 (issue #73): the same keyword columnar twice, then a periodic key (0112).
0112 ran every dictionary word's column order applied twice (459,267 routes with inverses) with a periodic key 1-26
after or before on 8 tableau classes, and listed K4's settings live below 20 (none); here the planted double columnar,
order A, class kry/std Beaufort, period 6 must be listed, with period 6's count above every copy.
The list holds the first 40 settings; copies have 0-4 below 20. 0112's encrypt() is a stub, so the plant makes its own
ciphertext."""
import random
import sys

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F6/1"
EXPERIMENT = "0112"
WHAT = "Keyword columnar under CAMPFIRE applied twice (width 8, forward), then a random period-6 key, plain KRYPTOS / cipher standard, Beaufort, key after the move, on English from Carter"
WORD, L = "CAMPFIRE", 6


def double(seq):
    w1 = sys.modules["attack"].where_columnar(seq)
    return [w1[w1[i]] for i in range(97)]


def route(e):
    a = sys.modules["attack"]
    for seq in (a.keyword_sequence(e["word"]), a.full_sequence(e["word"])):
        if len(seq) == e["width"]:
            wh = double(seq)
            if e["dir"] == "inverse":
                inv = [0] * 97
                for i, j in enumerate(wh):
                    inv[j] = i
                wh = inv
            return wh
    return None


def plant():
    rng = random.Random(7406)
    wh = double(sys.modules["attack"].keyword_sequence(WORD))
    k = [rng.randrange(26) for _ in range(L)]
    pt = english_plant(7406)
    moved = [""] * 97
    for i, j in enumerate(wh):
        moved[j] = pt[i]
    ct = "".join(STD[(k[j % L] - KRY.index(ch)) % 26] for j, ch in enumerate(moved))
    return {"plaintext": pt, "key": (WORD, "twice", "order A", "kry/std beau", k), "ciphertext": ct, "where": wh}


def found(result, plant):
    b = result.get("bounds", {})
    hit = [e for e in b.get("k4_live_below_20", []) if e["order"] == "A" and e["class"] == "kry/std/beau"
           and e["period"] == L and route(e) == plant["where"]]
    n, mx = b.get("k4_live_by_period", {}).get("A", [0] * 26)[L - 1], b.get("controls_live_by_period_max", {}).get("A", [0] * 26)[L - 1]
    return bool(hit) and n > mx, (f"settings live below 20: {b.get('n_k4_live_below_20')}; the planted double columnar at {L}, order A: {bool(hit)}; "
                                  f"live at {L}: {n}, copies' max {mx}")
