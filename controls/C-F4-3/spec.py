"""Positive control for F4/3 (issue #73): K4 read from behind the screen (0108).
0108 took the three mirror readings of K4's carved lines (each line reversed, line order reversed, both), with the
periodic table before or after the reading, and counted live periods 1-26 on 8 table classes against 10 shuffled
copies, listing each class's smallest live period below 20; here the planted class must be listed at the planted
period and that period must carry more live settings than every copy. 0108's encrypt() is a stub, so the plant
makes its own ciphertext."""
import random
import sys

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F4/3"
EXPERIMENT = "0108"
WHAT = "Each carved line reversed (read from behind), the table along the copper as carved (read then table), Beaufort with plain KRYPTOS / cipher standard, period 11 with random shifts, on English from Carter"
ORDER, PLACEMENT, P, CLASS = "lines reversed (from behind)", "read then table", 11, "kry/std/beau"


def plant():
    a = sys.modules["attack"]
    rng = random.Random(7560)
    pt = english_plant(7560)
    seq = a.orders()[ORDER]
    at = {i: seq.index(i) for i in range(97)}
    k = [rng.randrange(26) for _ in range(P)]
    ct = [None] * 97
    for i, ch in enumerate(pt):
        j = at[i]
        ct[j] = STD[(k[j % P] - KRY.index(ch)) % 26]
    return {"plaintext": pt, "key": (ORDER, PLACEMENT, CLASS, k), "ciphertext": "".join(ct)}


def found(result, plant):
    r = result.get("bounds", {}).get("results", {}).get(f"{ORDER}, {PLACEMENT}", {})
    rows = [x for x in r.get("k4_smallest_period_rows", []) if x["class"] == CLASS and x["period"] == P]
    live = r.get("k4_live_by_period", [0] * 26)[P - 1]
    cmax = r.get("controls_live_max", [0] * 26)[P - 1]
    return bool(rows) and live > cmax, f"{ORDER}, {PLACEMENT}: {CLASS} smallest live {P}: {bool(rows)}; live at {P} {live}, copies max {cmax}"
