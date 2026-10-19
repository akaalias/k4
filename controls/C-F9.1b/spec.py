"""Positive control for F9.1 (issue #73): a one-to-one substitution, then a triple with a keyword columnar (0198, 0162's
library). 0198 reran 0162's compiled builder (triples of rows-of-w readings at widths 2-24 and keyword columnars, at
least one keyed, forward and inverse) with the one-to-one test, and reports survivors per text. Here sigma(plaintext)
is put through one of those triples; 0162's library must count a survivor on the planted text, above every shuffled
copy, with every first stage done. Counts only, so the planted route is not named. 0198's encrypt() is a stub, so the
plant makes its own ciphertext with 0162's own stages()."""
import random
import sys

from kryptos.facts import STANDARD_ALPHABET as STD, load_vocabulary
from kryptos.plants import english_plant

ITEM = "F9.1"
EXPERIMENT = "0198"
ROUTE = ("col11", "key:PALIMPSEST", "ccw7")
LIB = "0162 keyword triples"
WHAT = "Random one-to-one substitution, then rows of 11 read by columns, a PALIMPSEST keyword columnar, rows of 7 read anticlockwise (0162's stages, forward), on English from Carter"


def plant():
    m = sys.modules["attack"].load("0162")
    st = {name: wh for name, wh, _ in m.stages(load_vocabulary())}
    a, b, c = (st[x] for x in ROUTE)
    wh = [c[b[a[i]]] for i in range(97)]
    rng = random.Random(7633)
    sig = list(STD); rng.shuffle(sig)
    pt = english_plant(7633)
    ct = [""] * 97
    for i, ch in enumerate(pt):
        ct[wh[i]] = sig[STD.index(ch)]
    return {"plaintext": pt, "key": ("".join(sig), ROUTE, "forward"), "ciphertext": "".join(ct)}


def found(result, plant):
    v = result.get("bounds", {}).get("per_library", {}).get(LIB, {})
    k4, cp = v.get("k4", 0), v.get("copies", [])
    full = v.get("first_stages_done") == v.get("first_stages_total")
    return k4 >= 1 and k4 > max(cp or [0]) and full, f"{LIB}: survivors planted {k4}, copies {cp}, first stages {v.get('first_stages_done')}/{v.get('first_stages_total')}"
