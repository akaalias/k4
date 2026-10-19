"""Positive control for F6/5 (issue #73): one carved letter wrong, through the move library (0093).
0093 ran its type-1 library (K3's rule, quarter turns, two turns, columnar, keyed columnar) with a periodic key 1-26
after or before on 8 tableau classes, allowing one known letter set aside, and listed K4's settings whose first live
period below 14 needs one set aside (at the copies' rate); here a planted route and period-8 key with the carved letter
over the R of BERLIN (place 66) miscut must be listed at period 8 with place 66 set aside, and the one-miss count at 8
must stand above every copy. The list holds the first 40 such settings; K4's own count was at the copies' rate.
0093's encrypt() is a stub, so the plant makes its own ciphertext with 0093's own moves."""
import random
import sys

from kryptos.facts import KRYPTOS_ALPHABET as KRY, load_vocabulary
from kryptos.plants import english_plant

ITEM = "F6/5"
EXPERIMENT = "0093"
WHAT = "An anticlockwise quarter turn in rows of 14 (forward), then a random period-8 key on the KRYPTOS table, Vigenere, then the carved letter over place 66 (R) miscut to another letter, on English from Carter"
W, L, PLACE = 14, 8, 66


def where_of_tag(tag):
    a = sys.modules["attack"]
    base = tag[:-len(" inverse")] if tag.endswith(" inverse") else tag
    for name, f in a.route_fns(load_vocabulary()):
        if name == base:
            sigma = a.perm_of(f)
            if tag.endswith(" inverse"):
                return list(sigma)
            fwd = [0] * 97
            for j, i in enumerate(sigma):
                fwd[i] = j
            return fwd
    return None


def plant():
    rng = random.Random(7414)
    where = where_of_tag(f"turn ccw {W}")
    k = [rng.randrange(26) for _ in range(L)]
    pt = english_plant(7414)
    moved = [""] * 97
    for i, j in enumerate(where):
        moved[j] = pt[i]
    ct = [KRY[(KRY.index(ch) + k[j % L]) % 26] for j, ch in enumerate(moved)]
    j0 = where[PLACE - 1]
    true = ct[j0]
    ct[j0] = KRY[(KRY.index(true) + 5) % 26]
    return {"plaintext": pt, "key": (f"turn ccw {W}", "order A", "kry/kry vig", k, f"carved {j0 + 1} miscut {true}->{ct[j0]}"),
            "ciphertext": "".join(ct), "where": where}


def found(result, plant):
    b = result.get("bounds", {})
    hit = [e for e in b.get("k4_one_miss_below_14", []) if e["order"] == "A" and e["class"] == "kry/kry/vig-var"
           and e["period"] == L and e["set_aside_place"] == PLACE and where_of_tag(e["route"]) == plant["where"]]
    n, mx = b.get("k4_live_one_miss_by_period", {}).get("A", [0] * 26)[L - 1], b.get("controls_one_miss_max", {}).get("A", [0] * 26)[L - 1]
    return bool(hit) and n > mx, (f"one-miss settings below 14: {b.get('n_k4_one_miss_below_14')}; the planted route at {L} with place {PLACE} "
                                  f"set aside: {bool(hit)}; one-miss live at {L}: {n}, copies' max {mx}")
