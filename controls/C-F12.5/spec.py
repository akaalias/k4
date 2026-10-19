"""Positive control for F12.5 (issue #73): two parts with their own repeating keys, split between the runs (0171).
0171 tested, for each part on its own (EASTNORTHEAST in part 1, BERLINCLOCK in part 2), every key length up to the
run length - 1 on 8 standard/KRYPTOS table classes, exactly, against 10 shuffled copies; no length fit K4 beyond the
copies. Here part 1 (places 1-48) and part 2 (49-97) carry different keys on different tables; each part's planted
class and length must be live with its checks. 0171's encrypt() is a stub, so the plant makes its own ciphertext."""
import random

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F12.5"
EXPERIMENT = "0171"
WHAT = ("Part 1 (places 1-48): Vigenere on the KRYPTOS table, random key of length 5; part 2 (49-97): Beaufort on the "
        "standard table, random key of length 7; on English from Carter")
SPLIT, L1, L2 = 48, 5, 7


def plant():
    rng = random.Random(7520)
    k1 = [rng.randrange(26) for _ in range(L1)]
    k2 = [rng.randrange(26) for _ in range(L2)]
    pt = english_plant(7520)
    ct = [KRY[(KRY.index(ch) + k1[i % L1]) % 26] if i < SPLIT else STD[(k2[i % L2] - STD.index(ch)) % 26]
          for i, ch in enumerate(pt)]
    return {"plaintext": pt, "key": ("split 48/49", "kry/kry vig", k1, "std/std beaufort", k2), "ciphertext": "".join(ct)}


def found(result, plant):
    b = result.get("bounds", {})
    live = {(x["part"], x["class"], x["length"]): x["checks"] for x in b.get("k4_live", [])}
    p1 = live.get(("part 1 (EASTNORTHEAST, 22-34)", "kry/kry/vig-var", L1))
    p2 = live.get(("part 2 (BERLINCLOCK, 64-74)", "std/std/beau", L2))
    s = b.get("summary", {})
    return bool(p1) and bool(p2), (f"part 1 kry/kry/vig-var length {L1} live: {bool(p1)} ({p1} checks); part 2 std/std/beau "
                                   f"length {L2} live: {bool(p2)} ({p2} checks); live lengths "
                                   + "; ".join(f"{k}: {v.get('k4_live_lengths')}" for k, v in s.items()))
