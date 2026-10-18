"""Positive control for F1/3 (issue #73): a periodic key on a table keyword-mixed from any dictionary word.
0109 tested 208,062 dictionary alphabets in 10 side classes, periods 1-26, and listed every setting alive
below period 20; here the planted word's alphabet, sides and period must be listed alive. 0109's encrypt()
is a stub, so the plant makes its own ciphertext."""
import random

from kryptos.plants import english_plant

ITEM = "F1/3"
EXPERIMENT = "0109"
WHAT = "Periodic tableau with the MOUNTAIN-mixed alphabet on both sides, added form, period 11 with random shifts, on English from Carter"
P = 11


def keyed(word):
    seen = []
    for c in word:
        if c not in seen:
            seen.append(c)
    return "".join(seen) + "".join(c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if c not in seen)


def plant():
    rng = random.Random(7315)
    pt = english_plant(7315)
    a = keyed("MOUNTAIN")
    k = [rng.randrange(26) for _ in range(P)]
    ct = "".join(a[(a.index(ch) + k[i % P]) % 26] for i, ch in enumerate(pt))
    return {"plaintext": pt, "key": ("MOUNTAIN", "both sides", "added", k), "ciphertext": ct}


def found(result, plant):
    b = result.get("bounds", {})
    live = b.get("k4_live_below_20", [])
    hit = [e for e in live if keyed(e["word"]) == keyed("MOUNTAIN") and e["plain"] == "W" and e["cipher"] == "W"
           and not e["beaufort"] and e["period"] == P]
    return bool(hit), f"settings alive below 20 on the plant: {b.get('n_k4_live_below_20')}; smallest live period {b.get('k4_smallest_live_period')}; the planted one listed: {bool(hit)}"
