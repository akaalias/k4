"""Positive control for F1.4 (issue #73): the skip schedule on the standard and KRYPTOS tables (0127).
0127 tested the 3,729 slot partitions of the skip schedule (one key letter skipped every m letters) on 8
standard/KRYPTOS tables exactly, against 30 shuffled copies; the planted schedule must give consistent partitions
above every copy. 0127's encrypt() is a stub, so the plant makes its own ciphertext."""
import random

from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.plants import english_plant

ITEM = "F1.4"
EXPERIMENT = "0127"
WHAT = "Skip schedule, one key letter skipped every 5 letters (m=5, phi=2), random 7-letter key, standard table, Beaufort, on English from Carter"


def plant():
    rng = random.Random(7362)
    k = [rng.randrange(26) for _ in range(7)]
    pt = english_plant(7362)
    ct = "".join(STD[(k[(i + (i + 2) // 5) % 7] - STD.index(ch)) % 26] for i, ch in enumerate(pt))
    return {"plaintext": pt, "key": ("skip m=5 phi=2 n=7", k, "std/std beaufort"), "ciphertext": ct}


def found(result, plant):
    s = result.get("bounds", {}).get("summary", {}).get("tables", {})
    ok = s.get("k4", 0) >= 1 and s.get("k4", 0) > s.get("coppers_max", 0)
    return ok, f"skip partitions consistent on the tables: plant {s.get('k4')}, copies {s.get('coppers_min')}-{s.get('coppers_max')}"
