"""Positive control for F3/4 (issue #73): column word plus row key, after one of 0080's moves (0087).
0087 tested key = column key + row key on grids of width 2-48 (one alphabet, either sign), with no move and after or
before each of 27,754 distinct moves, exactly by the cycle checks the 24 known letters give, against 10 shuffled
copies; K4 had no case with 5 or more checks. (Its own plant_check covers only the no-move case at width 7, by the
same check arithmetic.) Here the key is applied first (order B: grid of the plaintext places) and K3's rule then moves
the letters; the planted route, order, width, alphabet and sign must be listed among the cases with 5 or more checks
(listed up to 40; K4 had 0, so a cut-off is unlikely). 0087's encrypt() is a stub, so the plant makes its own
ciphertext with the snapshot's move()."""
import random
import sys

from kryptos.facts import KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F3/4"
EXPERIMENT = "0087"
WHAT = ("Rows of 8 on the KRYPTOS table, s = +1: random column key (8) + random row key (13) on the plaintext places, then "
        "K3's rule a=10, b=3 moves the letters; on English from Carter")
W = 8
ROUTE = {"kind": "k3rule", "a": 10, "b": 3}


def plant():
    rng = random.Random(7540)
    a = [rng.randrange(26) for _ in range(W)]
    b = [rng.randrange(26) for _ in range(13)]
    pt = english_plant(7540)
    changed = "".join(KRY[(KRY.index(ch) + a[i % W] + b[i // W]) % 26] for i, ch in enumerate(pt))
    ct = sys.modules["attack"].move(ROUTE, changed)
    return {"plaintext": pt, "key": (ROUTE, "order B", W, "kry", 1, a, b), "ciphertext": ct}


def found(result, plant):
    b = result.get("bounds", {})
    hits = b.get("k4_cases_with_5_or_more_checks", [])
    ok = [h for h in hits if h["route"] == ROUTE and h["order"] == "B" and h["width"] == W and h["alphabet"] == "kry" and h["sign"] == 1]
    return bool(ok), (f"cases with 5+ checks {b.get('n_k4_cases_5_plus')} (40 listed), copies at 5+ {b.get('controls_at_least', {}).get(5)}; "
                      f"the planted route/order/width: {bool(ok)}; routes done {b.get('routes_done')} of {b.get('distinct_routes')}")
