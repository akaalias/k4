"""Positive control for F6.14 (issue #73): the Nihilist transposition on a 10 x 10 square with three blanks (0167).
0167 ran all 10! keys x 8 blank places x row or column reading x both directions (116,121,600 routes) with a repeating
key 1-26 after or before on 8 table classes, against 10 shuffled copies; K4's shortest live key was 20 after, 24 before.
The planted setting (blank place, key's first element, reading, direction, order, class, period) must be listed in
k4_live_below_20 (the first 40 entries by period; K4 had none below 20) and its cell must stand above every copy.
0167's encrypt() is a stub, so the plant makes its own ciphertext."""
import random
import sys

from kryptos.facts import KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F6.14"
EXPERIMENT = "0167"
WHAT = "Nihilist transposition, key 6 2 9 0 4 8 1 7 3 5 for rows and columns, blanks at the start of the last row (place 2), read by columns; then a random 7-letter repeating key on the KRYPTOS table (Beaufort), on English from Carter"
PERM, PLACE, READ, L = [6, 2, 9, 0, 4, 8, 1, 7, 3, 5], 2, 1, 7


def plant():
    rng = random.Random(7462)
    pt = english_plant(7462)
    wh = sys.modules["attack"].reference(PERM, PLACE, READ)
    k = [rng.randrange(26) for _ in range(L)]
    y = [None] * 97
    for i, ch in enumerate(pt):
        y[wh[i]] = ch
    ct = "".join(KRY[(k[j % L] - KRY.index(y[j])) % 26] for j in range(97))
    return {"plaintext": pt, "key": (PERM, PLACE, "columns", "A", "kry/kry/beau", k), "ciphertext": ct}


def found(result, plant):
    b = result.get("bounds", {})
    want = {"place": PLACE, "first": PERM[0], "read": "columns", "dir": "fwd", "order": "A", "class": "kry/kry/beau", "period": L}
    hit = [x for x in b.get("k4_live_below_20", []) if all(x.get(k) == v for k, v in want.items())]
    above = ("A", L) in [tuple(c) for c in b.get("cells_k4_above_every_copper", [])]
    return bool(hit) and above, (f"planted setting listed below 20: {bool(hit)}; cell A{L} above every copy: {above}; "
                                 f"shortest live {b.get('k4_shortest_live')}, copies {b.get('coppers_shortest_live')}; jobs {b.get('jobs_done')}/{b.get('jobs_total')}")
