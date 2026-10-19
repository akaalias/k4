"""Positive control for F6.15 (issue #73): the YAR '1-2-3' spacing as a counting-off order (0166).
0166 took letters by counting 1-2-3 and 4-5-7 in every order around the text (24 routes with inverses) and tested a
repeating key 1-26 after or before on 8 classes against 10 shuffled copies; K4 had nothing live after and 26 before.
Here the 5-7-4 count, a period-10 key before; found requires the planted route by name, order, class and first live
period in k4_live_below_20 (the first 40 entries), and the planted cell above every copy.
0166's encrypt() is a stub, so the plant makes its own ciphertext."""
import random
import sys

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F6.15"
EXPERIMENT = "0166"
WHAT = "A random 10-letter repeating key on the standard table (Beaufort), then the letters taken by counting 5, 7, 4 places in turn around the remaining text, on English from Carter"
SEED, L, ORDER, PA, CA, BEAU = 7460, 10, "B", STD, STD, 1
CLS = "std/std/beau"
RUN_ITEM = "F6.15 YAR"
ROUTE = "count 5-7-4 fwd"


def wheremap():
    a = sys.modules["attack"]
    return a.where(a.josephus((5, 7, 4)))


def sub(ch, k):
    return CA[(k - PA.index(ch)) % 26] if BEAU else CA[(PA.index(ch) + k) % 26]


def plant():
    rng = random.Random(SEED)
    pt = english_plant(SEED)
    wh = wheremap()
    k = [rng.randrange(26) for _ in range(L)]
    c = [None] * 97
    if ORDER == "A":                                 # move, then the key by carved place
        y = [None] * 97
        for i, ch in enumerate(pt):
            y[wh[i]] = ch
        c = [sub(y[j], k[j % L]) for j in range(97)]
    else:                                            # the key by message place, then move
        for i, ch in enumerate(pt):
            c[wh[i]] = sub(ch, k[i % L])
    return {"plaintext": pt, "key": (ROUTE, ORDER, CLS, k), "ciphertext": "".join(c)}


def found(result, plant):
    r = result.get("bounds", {}).get("items", {}).get(RUN_ITEM, {})
    hit = [x for x in r.get("k4_live_below_20", []) if (x.get("route"), x.get("order"), x.get("class"), x.get("period")) == (ROUTE, ORDER, CLS, L)]
    above = (ORDER, L) in [tuple(c) for c in r.get("cells_k4_above_every_copper", [])]
    return bool(hit) and above, (f"{RUN_ITEM}: '{ROUTE}' order {ORDER} {CLS} first live at {L} listed: {bool(hit)}; cell {ORDER}{L} above every copy: {above}; "
                                 f"shortest live {r.get('k4_shortest_live')}, copies {r.get('coppers_shortest_live')}")
