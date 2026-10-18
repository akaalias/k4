"""Positive control for F1.4 (issue #73): hand key schedules on the standard and KRYPTOS tables (0128).
0128 built the slot partitions of the 24 known places for schedules C-F (stutter, back and forth, triangle,
square, restart per carved line) and tested each on 8 standard/KRYPTOS tables exactly, against 30 shuffled
copies; K4 had none consistent on the tables. The planted schedule must give consistent partitions above every
copy. (0126 ran the same schedules first and stopped at its budget; 0127 and 0128 completed it.)
0128's encrypt() is a stub, so the plant makes its own ciphertext."""
import random

from kryptos.facts import KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F1.4"
EXPERIMENT = "0128"
WHAT = "Stutter schedule (each key letter used twice, r=2, phi=0) with a random 6-letter key on the KRYPTOS table, Vigenere, on English from Carter"


def plant():
    rng = random.Random(7361)
    k = [rng.randrange(26) for _ in range(6)]
    pt = english_plant(7361)
    ct = "".join(KRY[(KRY.index(ch) + k[(i // 2) % 6]) % 26] for i, ch in enumerate(pt))
    return {"plaintext": pt, "key": ("stutter r=2 phi=0 n=6", k, "kry/kry vig"), "ciphertext": ct}


def found(result, plant):
    s = result.get("bounds", {}).get("summary", {}).get("C stutter | tables", {})
    ok = s.get("k4", 0) >= 1 and s.get("k4", 0) > s.get("coppers_max", 0)
    return ok, f"stutter partitions consistent on the tables: plant {s.get('k4')}, copies {s.get('coppers_min')}-{s.get('coppers_max')}"
