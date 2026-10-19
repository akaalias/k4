"""Positive control for F6.7 (issue #73): change, move, change with the two keys on different tables (0161).
0161 took 844 moves and, for standard then KRYPTOS or the reverse with 4 sign settings, keys of lengths 2-14 before
and after the move, decided each setting exactly over the one-to-one links and listed K4's 20 settings with the most
checks (K4 at the copies' rate at every level 1-8). Here the planted move, table order and signs, and key lengths 5
and 6 must be listed with all their checks (14 here, above any level the copies reach in the recorded table).
0161's encrypt() is a stub, so the plant makes its own ciphertext with 0161's own library()."""
import random
import sys

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY, KNOWN
from kryptos.plants import english_plant

ITEM = "F6.7"
EXPERIMENT = "0161"
WHAT = "A random length-5 key on the KRYPTOS table subtracted, then rows of 17 turned anticlockwise, then a random length-6 key added on the standard table, on English from Carter"
MOVE, M, NN, TABLES = "ccw17", 5, 6, "kry then std, signs -1+1"


def checks(ct, m):
    a = sys.modules["attack"]
    F, G = a.link_tables(KRY, STD, -1, 1)
    places = sorted(KNOWN)
    land = [m[q - 1] for q in places]
    links = [((q - 1) % M, land[e] % NN, STD.index(KNOWN[q]), STD.index(ct[land[e]])) for e, q in enumerate(places)]
    return a.decide(links, F, G)


def plant():
    m = dict(sys.modules["attack"].library())[MOVE]
    rng = random.Random(7419)
    k1 = [rng.randrange(26) for _ in range(M)]
    k2 = [rng.randrange(26) for _ in range(NN)]
    pt = english_plant(7419)
    y = [KRY[(KRY.index(ch) - k1[i % M]) % 26] for i, ch in enumerate(pt)]
    moved = [""] * 97
    for i, j in enumerate(m):
        moved[j] = y[i]
    ct = "".join(STD[(STD.index(ch) + k2[j % NN]) % 26] for j, ch in enumerate(moved))
    return {"plaintext": pt, "key": (k1, MOVE, k2, TABLES), "ciphertext": ct}


def found(result, plant):
    b = result.get("bounds", {})
    lib = dict(sys.modules["attack"].library())
    c = checks(plant["ciphertext"], lib[MOVE])
    hit = [e for e in b.get("k4_top", []) if lib[e["move"]] == lib[MOVE] and e["tables"] == TABLES
           and e["m"] == M and e["n"] == NN and e["checks"] == c]
    lvl8 = b.get("consistent_by_checks", {}).get(8, {})
    return bool(hit) and c > 8, (f"the planted setting with {c} checks in the top list: {bool(hit)}; top checks "
                                 f"{[e['checks'] for e in b.get('k4_top', [])[:5]]}; copies at 8 checks {lvl8.get('coppers_min')}-{lvl8.get('coppers_max')}")
