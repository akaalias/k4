"""Positive control for F6.8 (issue #73): three-stage routes with a keyword columnar stage (0162).
0162 took 131 keyword columnars (puzzle and K1-K3 words) and 92 plain readings (widths 2-24) and ran every triple with
at least one keyword stage (20,370,476 routes, compiled), forward and inverse, with a periodic key 1-26 after or before
on 8 tableau classes; K4's shortest live key was 20 after, 24 before, as the copies. Here the planted triple, order A,
class std/kry, period 7 must be among the 40 lowest-period settings listed, and K4's place must stand above every copy
at period 7. 0162's encrypt() is a stub, so the plant makes its own ciphertext with 0162's own stages()."""
import random
import sys

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY, load_vocabulary
from kryptos.plants import english_plant

ITEM = "F6.8"
EXPERIMENT = "0162"
WHAT = "Rows of 9 turned clockwise, then keyword columnar under SHADOW, then rows of 13 read by columns left first top down (forward), then a random period-7 key, plain standard / cipher KRYPTOS, Vigenere, on English from Carter"
NAMES, L = ("cw9", "key:SHADOW", "col13"), 7


def route(names, d):
    st = {n: m for n, m, _ in sys.modules["attack"].stages(load_vocabulary())}
    wh = list(range(97))
    for n in names:
        wh = [st[n][j] for j in wh]
    if d == "inv":
        inv = [0] * 97
        for i, j in enumerate(wh):
            inv[j] = i
        wh = inv
    return wh


def plant():
    wh = route(NAMES, "fwd")
    rng = random.Random(7420)
    k = [rng.randrange(26) for _ in range(L)]
    pt = english_plant(7420)
    moved = [""] * 97
    for i, j in enumerate(wh):
        moved[j] = pt[i]
    ct = "".join(KRY[(STD.index(ch) + k[j % L]) % 26] for j, ch in enumerate(moved))
    return {"plaintext": pt, "key": (NAMES, "order A", "std/kry vig", k), "ciphertext": ct, "where": wh}


def found(result, plant):
    b = result.get("bounds", {})
    hit = [e for e in b.get("k4_live_below_20", []) if e["order"] == "A" and e["class"] == "std/kry/vig-var"
           and e["period"] == L and route(e["stages"], e["dir"]) == plant["where"]]
    above = ("A", L) in [tuple(c) for c in b.get("cells_k4_above_every_copper", [])]
    return bool(hit) and above, (f"shortest live {b.get('k4_shortest_live')}, copies {b.get('coppers_shortest_live')}; the planted triple at {L}, "
                                 f"order A: {bool(hit)}; A{L} above every copy: {above}; first stages done {b.get('first_stages_done')} of {b.get('first_stages_total')}")
