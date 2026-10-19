"""Positive control for F8/1 (issue #73): Hill with keyword numberings (0044; 0055 runs the identical run() on
other numberings). 0044 is 0015's exact solver over 124 vocabulary keyword numberings. Here a 3x3 text is planted
under the ABSCISSA keyword numbering, 1-based, matrix decrypting (P = M C); the planted setting must be submitted
with the planted plaintext. Candidates are cut at 50 in numbering order: ABSCISSA1 is the 8th numbering, and on
K4 the first seven gave about a dozen submissions (0015: 2 over four numberings), so it is well inside the cut."""
import random
import sys

from kryptos.plants import english_plant

ITEM = "F8/1"
EXPERIMENT = "0044"
WHAT = "Hill 3x3 plain, numbering by the ABSCISSA keyword alphabet 1-based, blocks from place 2 (alignment 1), matrix decrypts (P = M C), random invertible M, on English from Carter"
KEY = {"numbering": "ABSCISSA1", "n": 3, "offset": 1, "direction": "dec", "v": None}


def plant():
    a = sys.modules["attack"]
    rng = random.Random(7602)
    while True:
        M = [[rng.randrange(26) for _ in range(3)] for _ in range(3)]
        if a.inverse(M) is not None:
            break
    return {"plaintext": english_plant(7602), "key": dict(KEY, M=M)}


def found(result, plant):
    k = plant["key"]
    hit = [c for c in result.get("candidates", []) if c["plaintext"] == plant["plaintext"]
           and all(c["key"].get(f) == k[f] for f in ("numbering", "n", "offset", "direction"))]
    return bool(hit), f"{result.get('notes', '')}; planted 3x3 ABSCISSA1 offset 1 dec submitted with the planted text: {bool(hit)}"
