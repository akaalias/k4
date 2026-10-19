"""Positive control for F6/1 (issue #73): AMSCO keyed by the dictionary, then a periodic key (0114).
0114 ran AMSCO under every dictionary word's column order of 3-15 columns, first cell of 1 or 2 letters, forward and
inverse, with a periodic key 1-26 after or before on 8 tableau classes, and listed K4's settings live below 20 (none);
here the planted AMSCO, order A, class std/kry Vigenere, period 9 must be listed, with period 9's count above every copy.
The list holds the first 40 settings; copies have 0-4 below 20. 0114's encrypt() is a stub, so the plant makes its
own ciphertext."""
import random
import sys

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F6/1"
EXPERIMENT = "0114"
WHAT = "AMSCO under MIRAGE (6 columns, first cell 2 letters, forward), then a random period-9 key, plain standard / cipher KRYPTOS, Vigenere, key after the move, on English from Carter"
WORD, FIRST, L = "MIRAGE", 2, 9


def route(e):
    a = sys.modules["attack"]
    for seq in (a.keyword_sequence(e["word"]), a.full_sequence(e["word"])):
        if len(seq) == e["width"]:
            wh = a.where_amsco(tuple(seq), e["first_cell"])
            if e["dir"] == "inverse":
                inv = [0] * 97
                for i, j in enumerate(wh):
                    inv[j] = i
                wh = inv
            return wh
    return None


def plant():
    rng = random.Random(7404)
    a = sys.modules["attack"]
    wh = a.where_amsco(tuple(a.keyword_sequence(WORD)), FIRST)
    k = [rng.randrange(26) for _ in range(L)]
    pt = english_plant(7404)
    moved = [""] * 97
    for i, j in enumerate(wh):
        moved[j] = pt[i]
    ct = "".join(KRY[(STD.index(ch) + k[j % L]) % 26] for j, ch in enumerate(moved))
    return {"plaintext": pt, "key": (WORD, "first cell 2", "order A", "std/kry vig", k), "ciphertext": ct, "where": wh}


def found(result, plant):
    b = result.get("bounds", {})
    hit = [e for e in b.get("k4_live_below_20", []) if e["order"] == "A" and e["class"] == "std/kry/vig-var"
           and e["period"] == L and route(e) == plant["where"]]
    n, mx = b.get("k4_live_by_period", {}).get("A", [0] * 26)[L - 1], b.get("controls_live_by_period_max", {}).get("A", [0] * 26)[L - 1]
    return bool(hit) and n > mx, (f"settings live below 20: {b.get('n_k4_live_below_20')}; the planted AMSCO at {L}, order A: {bool(hit)}; "
                                  f"live at {L}: {n}, copies' max {mx}")
