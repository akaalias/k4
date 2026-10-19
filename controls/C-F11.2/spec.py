"""Positive control for F11.2 (issue #73): poem code, a double columnar keyed by words of a memorized text (0190).
0190 built 3,063 phrase keys (1-6 consecutive words of K1-K3 and the Morse, the same key twice or split in two),
made each double transposition (forward and inverse), then (A) or before (B) a periodic key 1-26 on 8 table
classes, against 15 shuffled copies; it lists settings whose smallest live period is below 20 and the (order,
period) cells where the text stands above every copy. Here the planted key, in order B, must be listed at its
class and period, and that cell must stand above every copy. Repeated permutations are skipped under the first
name, so found() compares permutations. 0190's encrypt() is a stub, so the plant makes its own ciphertext."""
import random
import sys

from kryptos.facts import KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F11.2"
EXPERIMENT = "0190"
WHAT = "Periodic key first (order B: Beaufort on the KRYPTOS table along the message, period 7 with random shifts), then the double columnar keyed by K2 words 20-23 split after 2 (0190's double_map), on English from Carter"
P = 7


def plant():
    a = sys.modules["attack"]
    K = a.keys()
    name, k1, k2 = [x for x in K if x[0].startswith("K2 words 20-23 split after 2")][0]
    m = a.double_map(k1, k2)
    rng = random.Random(7565)
    pt = english_plant(7565)
    k = [rng.randrange(26) for _ in range(P)]
    ct = [None] * 97
    for i, ch in enumerate(pt):
        ct[m[i]] = KRY[(k[i % P] - KRY.index(ch)) % 26]
    return {"plaintext": pt, "key": (name, k1, k2, "order B", "kry/kry/beau", k), "ciphertext": "".join(ct), "map": m}


def found(result, plant):
    a = sys.modules["attack"]
    b = result.get("bounds", {})
    M = dict(a.dedupe([(n, a.double_map(x, y)) for n, x, y in a.keys()]))
    hit = [e for e in b.get("k4_live_below_20", []) if e["order"] == "B" and e["class"] == "kry/kry/beau" and e["period"] == P
           and M.get(e["route"]) == plant["map"]]
    above = ("B", P) in [tuple(x) for x in b.get("cells_k4_above_every_copper", [])]
    return bool(hit) and above, f"planted key listed at {P}, order B: {[e['route'] for e in hit][:3]}; cell (B, {P}) above every copy: {above}"
