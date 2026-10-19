"""Positive control for F9.1 (issue #73): a one-to-one substitution, then a mixed matrix triple (0198, 0158's library).
0198 reran 0158's compiled builder (three stages of rows-of-w read one of four ways, widths 2-96, forward and inverse)
with its per-route test swapped for the one-to-one test, and reports survivors per text. Here sigma(plaintext) is put
through one of those triples; 0158's library must count a survivor on the planted text, above every shuffled copy,
with every first stage done. 0198 reports counts only, so the planted route is not named. 0198's encrypt() is a stub,
so the plant makes its own ciphertext with 0158's own where_of()."""
import random
import sys

from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.plants import english_plant

ITEM = "F9.1"
EXPERIMENT = "0198"
ROUTE = (("col", 30), ("colr", 9), ("ccw", 41))
LIB = "0158 mixed matrix triples"
WHAT = "Random one-to-one substitution, then rows of 30 read by columns, rows of 9 read right to left bottom up, rows of 41 read anticlockwise (0158's stages, forward), on English from Carter"


def plant():
    m = sys.modules["attack"].load("0158")
    rng = random.Random(7632)
    sig = list(STD); rng.shuffle(sig)
    pt = english_plant(7632)
    (r1, w1), (r2, w2), (r3, w3) = ROUTE
    a, b, c = m.where_of(w1, r1), m.where_of(w2, r2), m.where_of(w3, r3)
    wh = [c[b[a[i]]] for i in range(97)]
    ct = [""] * 97
    for i, ch in enumerate(pt):
        ct[wh[i]] = sig[STD.index(ch)]
    return {"plaintext": pt, "key": ("".join(sig), ROUTE, "forward"), "ciphertext": "".join(ct)}


def found(result, plant):
    v = result.get("bounds", {}).get("per_library", {}).get(LIB, {})
    k4, cp = v.get("k4", 0), v.get("copies", [])
    full = v.get("first_stages_done") == v.get("first_stages_total")
    return k4 >= 1 and k4 > max(cp or [0]) and full, f"{LIB}: survivors planted {k4}, copies {cp}, first stages {v.get('first_stages_done')}/{v.get('first_stages_total')}"
