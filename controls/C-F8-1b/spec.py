"""Positive control for F8/1 (issue #73): chained Hill (0036).
0036 solves ciphertext feedback, plaintext feedback, summed input and paired matrices exactly from the whole crib
blocks (sizes 2-4, four numberings, every alignment) and submits every decryption with all 24 known letters. Here a
2x2 ciphertext-feedback text is planted (c_k = M p_k + c_(k-1), 11 whole crib blocks); the planted setting must be
submitted with the planted plaintext. Candidates are cut at 50 in numbering order; std0 is the first numbering."""
import random
import sys

from kryptos.plants import english_plant

ITEM = "F8/1"
EXPERIMENT = "0036"
WHAT = "Hill 2x2 with ciphertext feedback (c_k = M p_k + c_(k-1)), numbering A=0 standard, blocks from place 2 (alignment 1), random invertible M, on English from Carter"
KEY = {"numbering": "std0", "n": 2, "offset": 1, "variant": "chain-c"}


def plant():
    a = sys.modules["attack"]
    rng = random.Random(7601)
    while True:
        M = [[rng.randrange(26) for _ in range(2)] for _ in range(2)]
        if a.inverse(M) is not None:
            break
    return {"plaintext": english_plant(7601), "key": dict(KEY, M=M)}


def found(result, plant):
    k = plant["key"]
    hit = [c for c in result.get("candidates", []) if c["plaintext"] == plant["plaintext"]
           and all(c["key"].get(f) == k[f] for f in ("numbering", "n", "offset", "variant"))]
    return bool(hit), f"full hits {len(result.get('candidates', []))}; planted chain-c 2x2 std0 offset 1 with the planted text: {bool(hit)}"
