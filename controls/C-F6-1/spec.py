"""Positive control for F6/1 (issue #73): a keyword columnar from the dictionary, then a periodic key (0110).
0110 took every dictionary word's column order (229,634), forward and inverse, with a periodic key 1-26 after or
before the move on 8 tableau classes, and listed K4's settings live below period 20 (none); here the planted
route, order A (key after the move), class kry/kry and period 8 must be listed, with period 8's count above every
shuffled copy. The list holds the first 40 settings; copies have 0-3 below 20, so the plant is not cut off.
0110's encrypt() is a stub, so the plant makes its own ciphertext."""
import random
import sys

from kryptos.facts import KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F6/1"
EXPERIMENT = "0110"
WHAT = "Keyword columnar under HOSPITAL (width 8, forward), then a random period-8 key on the KRYPTOS table, Vigenere, key after the move, on English from Carter"
WORD, L = "HOSPITAL", 8


def route(e):
    a = sys.modules["attack"]
    for seq in (a.keyword_sequence(e["word"]), a.full_sequence(e["word"])):
        if len(seq) == e["width"]:
            wh = a.where_columnar(seq)
            if e["dir"] == "inverse":
                inv = [0] * 97
                for i, j in enumerate(wh):
                    inv[j] = i
                wh = inv
            return wh
    return None


def plant():
    rng = random.Random(7400)
    wh = sys.modules["attack"].where_columnar(sys.modules["attack"].keyword_sequence(WORD))
    k = [rng.randrange(26) for _ in range(L)]
    pt = english_plant(7400)
    moved = [""] * 97
    for i, j in enumerate(wh):
        moved[j] = pt[i]
    ct = "".join(KRY[(KRY.index(ch) + k[j % L]) % 26] for j, ch in enumerate(moved))
    return {"plaintext": pt, "key": (WORD, "forward", "order A", "kry/kry vig", k), "ciphertext": ct, "where": wh}


def found(result, plant):
    b = result.get("bounds", {})
    low = b.get("k4_live_below_20", [])
    hit = [e for e in low if e["order"] == "A" and e["class"] == "kry/kry/vig-var" and e["period"] == L and route(e) == plant["where"]]
    n, mx = b.get("k4_live_by_period", {}).get("A", [0] * 26)[L - 1], b.get("controls_live_by_period_max", {}).get("A", [0] * 26)[L - 1]
    return bool(hit) and n > mx, (f"settings live below 20: {b.get('n_k4_live_below_20')}; the planted route at {L}, order A: {bool(hit)}; "
                                  f"live at {L}: {n}, copies' max {mx}")
