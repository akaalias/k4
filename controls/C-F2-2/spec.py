"""Positive control for F2/2 (issue #73): the message written along one grid path and read along another (0092).
0092 tried every pair of its 30 paths at widths 2-96 (43,579 distinct routes and inverses), then (A) or before (B)
a periodic key 1-26 on 8 table classes, and listed every route whose smallest live period is below 20; here the
planted route must be listed with its order, class and period. The listing may name another path pair giving the
same permutation (0092 skips repeats), so found() compares permutations, not names. 0092's encrypt() is a stub, so
the plant makes its own ciphertext."""
import random
import sys

from kryptos.facts import KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F2/2"
EXPERIMENT = "0092"
WHAT = "Written in a clockwise spiral from the top left of a width-8 grid, read off by columns, then (order A) Vigenere on the KRYPTOS table, period 11 with random shifts, on English from Carter"
W, WRITE, READ, P = 8, "spiral top-left cw", "columns", 11


def plant():
    a = sys.modules["attack"]
    rng = random.Random(7554)
    pt = english_plant(7554)
    G = a.paths(W)
    wh = a.route(G[WRITE], G[READ])
    k = [rng.randrange(26) for _ in range(P)]
    ct = [None] * 97
    for i, ch in enumerate(pt):
        j = wh[i]
        ct[j] = KRY[(KRY.index(ch) + k[j % P]) % 26]
    return {"plaintext": pt, "key": (W, WRITE, READ, "order A", "kry/kry/vig-var", k), "ciphertext": "".join(ct), "route": wh}


def found(result, plant):
    a = sys.modules["attack"]
    b = result.get("bounds", {})
    hit = []
    for e in b.get("k4_live_below_20", []):
        if e["order"] != "A" or e["class"] != "kry/kry/vig-var" or e["period"] != P:
            continue
        G = a.paths(e["width"])
        inv = e["read"].endswith(" inverse")
        r = a.route(G[e["write"]], G[e["read"][:-8] if inv else e["read"]])
        if inv:
            r2 = [0] * 97
            for i, j in enumerate(r):
                r2[j] = i
            r = r2
        if r == plant["route"]:
            hit.append(e)
    return bool(hit), f"K4-side routes live below 20: {b.get('n_k4_live_below_20')}; the planted route at {P}, order A: {hit[:1]}"
