"""Positive control for F1/4 (issue #73): the per-letter progressive key on dictionary tables (F1.9's run).
0155 counted, for 1,040,314 tables x 2 forms x steps 1-25, which periods 1-52 the known letters leave
consistent, against 10 shuffled copies; here the planted period must be live and stand above every copy.
0155's encrypt() is a stub, so the plant makes its own ciphertext."""
import random

from kryptos.plants import english_plant

ITEM = "F1/4"
EXPERIMENT = "0155"
WHAT = "Per-letter progressive key, the GARDEN-mixed alphabet on both sides, added form, period 9 with random shifts, step 4, on English from Carter"
L, S = 9, 4


def keyed(word):
    seen = []
    for c in word:
        if c not in seen:
            seen.append(c)
    return "".join(seen) + "".join(c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if c not in seen)


def plant():
    rng = random.Random(7318)
    pt = english_plant(7318)
    a = keyed("GARDEN")
    k = [rng.randrange(26) for _ in range(L)]
    ct = "".join(a[(a.index(ch) + k[i % L] + S * i) % 26] for i, ch in enumerate(pt))
    return {"plaintext": pt, "key": ("GARDEN", "both sides", "added", k, "step", S, "per-letter"), "ciphertext": ct}


def found(result, plant):
    b = result.get("bounds", {})
    live = b.get("k4_live_by_period", {}).get("letter", [])
    n = live[L - 1] if len(live) >= L else 0
    above = f"letter:{L}" in b.get("cells_k4_above_every_copper", [])
    return n > 0 and above, f"per-letter settings live at {L}: {n}; shortest live {b.get('k4_shortest_live')}; above every copy: {above}"
