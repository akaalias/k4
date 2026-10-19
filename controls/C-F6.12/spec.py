"""Positive control for F6.12 (issue #73): the EVA double triangle (0166).
0166 ran the double triangle for 1,920 19-letter keys (K1-K3 windows, dictionary words, puzzle-word pairs: 3,840
routes) and tested a repeating key 1-26 after or before on 8 classes against 10 shuffled copies; K4 had nothing live
after the move and 25 before. Here a K3 window as the key, a period-12 key after; found requires the planted route by
name, order, class and first live period in k4_live_below_20 (the first 20 entries by period; K4 had none below 20, so
only a planted period this short can lead it), and the planted cell above every copy.
0166's encrypt() is a stub, so the plant makes its own ciphertext."""
import random
import sys

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F6.12"
EXPERIMENT = "0166"
WHAT = "EVA double triangle under the K3 window ETOFLICKERBUTPRESEN, then a random 12-letter repeating key on the KRYPTOS table (Vigenere), on English from Carter"
SEED, L, ORDER, PA, CA, BEAU = 7459, 12, "A", KRY, KRY, 0
CLS = "kry/kry/vig-var"
RUN_ITEM = "F6.12 EVA"
ROUTE = "ETOFLICKERBUTPRESEN fwd"


def wheremap():
    a = sys.modules["attack"]
    return a.where(a.eva("ETOFLICKERBUTPRESEN"))


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
