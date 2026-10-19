"""Positive control for F8/1 (issue #73): plain Hill solved from the crib blocks (0015).
0015 solves the matrix exactly (mod 13 and mod 2) from the whole crib blocks for sizes 2-4, four numberings, every
alignment, both directions, plain and affine, and submits the decryption of every consistent invertible solution.
Here a 3x3 text is planted (7 whole crib blocks against 3 needed: 4 checks); the planted setting must be submitted
with the planted plaintext. Candidates are cut at 50 in numbering order; std0 is the first numbering, so the plant
cannot be cut off."""
import random
import sys

from kryptos.plants import english_plant

ITEM = "F8/1"
EXPERIMENT = "0015"
WHAT = "Hill 3x3 plain, numbering A=0 standard, blocks from place 2 (alignment 1), matrix encrypts (C = M P), random invertible M, on English from Carter"
KEY = {"numbering": "std0", "n": 3, "offset": 1, "direction": "enc", "v": None}


def plant():
    a = sys.modules["attack"]
    rng = random.Random(7600)
    while True:
        M = [[rng.randrange(26) for _ in range(3)] for _ in range(3)]
        if a.inverse(M) is not None:
            break
    return {"plaintext": english_plant(7600), "key": dict(KEY, M=M)}


def found(result, plant):
    k = plant["key"]
    hit = [c for c in result.get("candidates", []) if c["plaintext"] == plant["plaintext"]
           and all(c["key"].get(f) == k[f] for f in ("numbering", "n", "offset", "direction"))]
    b = result.get("bounds", {})
    return bool(hit), f"consistent settings {len(b.get('settings_consistent_on_all_crib_blocks', []))}; planted 3x3 std0 offset 1 enc submitted with the planted text: {bool(hit)}"
