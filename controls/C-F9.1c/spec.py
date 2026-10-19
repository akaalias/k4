"""Positive control for F9.1 (issue #73): a one-to-one substitution, then a Nihilist transposition (0198, 0167's library).
0198 reran 0167's compiled builder (10 x 10 square, three blanks at eight places, every key of 10!, read by rows or
columns, forward and inverse) with the one-to-one test, and reports survivors per text. Here sigma(plaintext) is put
through one of those routes; 0167's library must count a survivor on the planted text, above every shuffled copy,
with all 80 jobs done. Counts only, so the planted route is not named. 0198's encrypt() is a stub, so the plant
makes its own ciphertext with 0167's own reference()."""
import random
import sys

from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.plants import english_plant

ITEM = "F9.1"
EXPERIMENT = "0198"
PLACE, READ = 3, 1
LIB = "0167 Nihilist"
WHAT = "Random one-to-one substitution, then a Nihilist transposition on the 10 x 10 square, blanks at the end of the first row (place 3), a random key order, read by columns, forward, on English from Carter"


def plant():
    m = sys.modules["attack"].load("0167")
    rng = random.Random(7634)
    sig = list(STD); rng.shuffle(sig)
    perm = list(range(10)); rng.shuffle(perm)
    wh = m.reference(perm, PLACE, READ)
    pt = english_plant(7634)
    ct = [""] * 97
    for i, ch in enumerate(pt):
        ct[wh[i]] = sig[STD.index(ch)]
    return {"plaintext": pt, "key": ("".join(sig), perm, f"place {PLACE}", "columns", "forward"), "ciphertext": "".join(ct)}


def found(result, plant):
    v = result.get("bounds", {}).get("per_library", {}).get(LIB, {})
    k4, cp = v.get("k4", 0), v.get("copies", [])
    full = v.get("jobs_done") == v.get("jobs_total")
    return k4 >= 1 and k4 > max(cp or [0]) and full, f"{LIB}: survivors planted {k4}, copies {cp}, jobs {v.get('jobs_done')}/{v.get('jobs_total')}"
