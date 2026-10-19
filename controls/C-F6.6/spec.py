"""Positive control for F6.6 (issue #73): move, change, move again (0160).
0160 took 844 moves (the four column readings at widths 2-96 and K3's rule at every multiplier, forward and inverted)
and every ordered pair around a periodic key 1-26 on 8 tableau classes, the key slot set by the first move; K4's
shortest live key was 20, copies 18. Here the planted pair, class kry/std Beaufort, period 9 must be among the 40
lowest-period settings listed, and K4's place must stand above every copy at period 9.
0160's encrypt() is a stub, so the plant makes its own ciphertext with 0160's own library()."""
import random
import sys

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F6.6"
EXPERIMENT = "0160"
WHAT = "Rows of 11 read right first bottom up, then a random period-9 key, plain KRYPTOS / cipher standard, Beaufort, then K3's rule with multiplier 30, on English from Carter"
M1, M2, L = "colr11", "k3x30", 9


def maps():
    return dict(sys.modules["attack"].library())


def plant():
    lib = maps()
    m1, m2 = lib[M1], lib[M2]
    rng = random.Random(7418)
    k = [rng.randrange(26) for _ in range(L)]
    pt = english_plant(7418)
    s1 = [""] * 97
    for i, j in enumerate(m1):
        s1[j] = pt[i]
    ct = [""] * 97
    for j, ch in enumerate(s1):
        ct[m2[j]] = STD[(k[j % L] - KRY.index(ch)) % 26]
    return {"plaintext": pt, "key": (M1, "kry/std beau", k, M2), "ciphertext": "".join(ct)}


def found(result, plant):
    b = result.get("bounds", {})
    lib = maps()
    want = (lib[M1], [lib[M2][j] for j in lib[M1]])
    hit = [e for e in b.get("k4_live_below_20", []) if e["class"] == "kry/std/beau" and e["period"] == L
           and (lib[e["moves"][0]], [lib[e["moves"][1]][j] for j in lib[e["moves"][0]]]) == want]
    above = L in b.get("cells_k4_above_every_copper", [])
    return bool(hit) and above, (f"shortest live {b.get('k4_shortest_live')}, copies {b.get('coppers_shortest_live')}; the planted pair at {L}: "
                                 f"{bool(hit)}; {L} above every copy: {above}")
