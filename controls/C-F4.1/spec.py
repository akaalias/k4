"""Positive control for F4.1 (issue #73): a route over the plates' physical layout, then a periodic key (0184).
0184 read K4's cells along 73 routes over three grids of the copper's lines (K4's four lines, the lower plate, the
whole left side), forward and inverse, then (A) or before (B) a periodic key 1-26 on 8 table classes, against 15
shuffled copies; it lists settings whose smallest live period is below 20 and the (order, period) cells where the
text stands above every copy. Here the planted route must be listed at its order, class and period, and that cell
must stand above every copy. Repeated permutations are skipped by 0184 under the first name, so found() compares
the listed route's permutation with the planted one. 0184's encrypt() is a stub, so the plant makes its own
ciphertext."""
import random
import sys

from kryptos.facts import KRYPTOS_ALPHABET as KRY, STANDARD_ALPHABET as STD
from kryptos.plants import english_plant

ITEM = "F4.1"
EXPERIMENT = "0184"
WHAT = "The lower plate's cells read in a clockwise spiral from the top left (message letter i carved at the i-th K4 cell met), then (order A) Vigenere with plain standard / cipher KRYPTOS along the carved text, period 13 with random shifts, on English from Carter"
GRID, FIRST, ROUTE, P = "lower plate", 14, "spiral from top-left clockwise", 13


def maps():
    a = sys.modules["attack"]
    named = []
    for gname, first in (("K4's four lines", 24), ("lower plate", 14), ("whole left side", 0)):
        cells, k4 = a.grid(first)
        carved = {cell: i for i, cell in enumerate(k4)}
        for rname, seq in a.routes(cells).items():
            named.append((f"{gname}: {rname}", [carved[x] for x in seq if x in carved]))
    return dict(a.dedupe(named))


def plant():
    a = sys.modules["attack"]
    cells, k4 = a.grid(FIRST)
    carved = {cell: i for i, cell in enumerate(k4)}
    m = [carved[x] for x in a.routes(cells)[ROUTE] if x in carved]
    rng = random.Random(7561)
    pt = english_plant(7561)
    k = [rng.randrange(26) for _ in range(P)]
    ct = [None] * 97
    for i, ch in enumerate(pt):
        j = m[i]
        ct[j] = KRY[(STD.index(ch) + k[j % P]) % 26]
    return {"plaintext": pt, "key": (f"{GRID}: {ROUTE}", "order A", "std/kry/vig-var", k), "ciphertext": "".join(ct), "map": m}


def found(result, plant):
    b = result.get("bounds", {})
    M = maps()
    hit = [e for e in b.get("k4_live_below_20", []) if e["order"] == "A" and e["class"] == "std/kry/vig-var" and e["period"] == P
           and M.get(e["route"]) == plant["map"]]
    above = ("A", P) in [tuple(x) for x in b.get("cells_k4_above_every_copper", [])]
    return bool(hit) and above, f"planted route listed at {P}, order A: {[e['route'] for e in hit]}; cell (A, {P}) above every copy: {above}"
