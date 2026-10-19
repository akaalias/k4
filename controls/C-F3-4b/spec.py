"""Positive control for F3/4 (issue #73): column word plus a shift per block (0088).
0088 tested key = a[j mod w] + b[(j + o) div m] (w 2-31, m 2-50, every offset; one alphabet, either sign) exactly by
the cycle checks of the 24 known letters, against 10 shuffled copies; K4 had no structure with 3 or more checks.
Here the planted structure must be listed among the survivors with 3 or more checks (listed up to 40; K4 had 0).
0088's encrypt() is a stub, so the plant makes its own ciphertext."""
import random

from kryptos.facts import KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F3/4"
EXPERIMENT = "0088"
WHAT = ("Column key of 6 + one shift per block of 12 letters (offset 4), KRYPTOS table, s = -1 (c = -p + key); random keys; "
        "on English from Carter")
W, M, O, S = 6, 12, 4, -1


def plant():
    rng = random.Random(7541)
    a = [rng.randrange(26) for _ in range(W)]
    b = [rng.randrange(26) for _ in range((96 + O) // M + 1)]
    pt = english_plant(7541)
    ct = "".join(KRY[(S * KRY.index(ch) + a[j % W] + b[(j + O) // M]) % 26] for j, ch in enumerate(pt))
    return {"plaintext": pt, "key": ("w", W, "m", M, "o", O, "kry", S, a, b), "ciphertext": ct}


def found(result, plant):
    b = result.get("bounds", {})
    ok = [h for h in b.get("k4_survivors_3_plus", []) if (h["w"], h["m"], h["offset"], h["alphabet"], h["sign"]) == (W, M, O, "kry", S)]
    return bool(ok), f"survivors with 3+ checks {b.get('n_k4_3_plus')} (40 listed); the planted structure: {ok[:1]}"
