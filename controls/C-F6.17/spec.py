"""Positive control for F6.17 (issue #73): the trapezoid transposition (0164).
0164 built trapezoids (base = keyword length, rows one shorter going up on either side, fewest blanks: 89,708 routes)
and tested a repeating key 1-26 after or before on 8 classes against 10 shuffled copies; K4's shortest live was 26 /
25. Here WONDERFULTHINGS (9 rows, the fewest that hold 97) shrinking on the left, a period-10 key before; found
requires the planted route by name, order, class and first live period in k4_live_below_20 (the first 20 entries by
period; K4 had none below 20, so only a planted period this short can lead it), and the planted cell above every copy.
0164's encrypt() is a stub, so the plant makes its own ciphertext."""
import random
import sys

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F6.17"
EXPERIMENT = "0164"
WHAT = "A random 10-letter repeating key on the KRYPTOS table (Vigenere), then the TM 32-220 trapezoid under WONDERFULTHINGS (base 15, 9 rows shrinking on the left), on English from Carter"
SEED, L, ORDER, PA, CA, BEAU = 7454, 10, "B", KRY, KRY, 0
CLS = "kry/kry/vig-var"
RUN_ITEM = "F6.17 trapezoid"
ROUTE = "WONDERFULTHINGS h9 left fwd"


def wheremap():
    a = sys.modules["attack"]
    return a.where(a.trapezoid("WONDERFULTHINGS", 9, "left"))


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
