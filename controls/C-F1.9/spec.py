"""Positive control for F1.9 (issue #73): the per-repeat progressive key, Beaufort form, on a dictionary table (0155).
C-F1-4c planted 0155's per-letter form (added, both sides keyword-mixed); this plants the other branch of the same
search: per-repeat ('step per cycle'), Beaufort form, keyword-mixed plain side against the standard cipher side.
The planted period must be live and stand above every copy. 0155's encrypt() is a stub, so the plant makes its own
ciphertext."""
import random

from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.plants import english_plant

ITEM = "F1.9"
EXPERIMENT = "0155"
WHAT = "Per-repeat progressive key, plain LANTERN-mixed / cipher standard, Beaufort form, period 11 with random shifts, step 7 per pass of the key, on English from Carter"
L, S = 11, 7


def keyed(word):
    seen = []
    for c in word:
        if c not in seen:
            seen.append(c)
    return "".join(seen) + "".join(c for c in STD if c not in seen)


def plant():
    rng = random.Random(7391)
    pt = english_plant(7391)
    pa = keyed("LANTERN")
    w = [rng.randrange(26) for _ in range(L)]
    ct = "".join(STD[(w[i % L] + S * (i // L) - pa.index(ch)) % 26] for i, ch in enumerate(pt))
    return {"plaintext": pt, "key": ("LANTERN", "plain side", "Beaufort", w, "step per pass", S), "ciphertext": ct}


def found(result, plant):
    b = result.get("bounds", {})
    live = b.get("k4_live_by_period", {}).get("repeat", [])
    n = live[L - 1] if len(live) >= L else 0
    above = f"repeat:{L}" in b.get("cells_k4_above_every_copper", [])
    return n > 0 and above, f"per-repeat settings live at {L}: {n}; shortest live {b.get('k4_shortest_live')}; above every copy: {above}"
