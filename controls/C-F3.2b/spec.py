"""Positive control for F3.2 (issue #73): a word plus a per-place number from the plate layout (0175).
0175's own plant (a Morse reading repeated under the text, + SHADOW) went through its scan() and was found, but only
for the readings that repeat ('rep'); its three per-place readings (each K4 letter's line or column on the plate)
take a different branch of scan(). Here the plant uses one of them, and the planted word must come back as a
dictionary hit with the planted rule, sign and lettering, and its candidate must read the planted text (hits listed
up to 40, candidates from the first 20; K4 had 0). The attack's own encrypt() makes the ciphertext."""
from kryptos.plants import english_plant

ITEM = "F3.2"
EXPERIMENT = "0175"
WHAT = ("LANTERN on the KRYPTOS order minus the column of each K4 letter on the plate; plain standard, cipher KRYPTOS, "
        "Beaufort; on English from Carter")
KEY = {"reading": "column of each K4 letter on the plate", "lettering": "kry", "word": "LANTERN", "rotation": 0,
       "rule": "beau/std/kry", "align": 0, "sign": -1}


def plant():
    return {"plaintext": english_plant(7545), "key": KEY}


def found(result, plant):
    b = result.get("bounds", {})
    hits = [h for h in b.get("k4_hits", []) if h["reading"] == KEY["reading"] and h["rule"] == KEY["rule"] and h["sign"] == KEY["sign"]
            and h["lettering"] == "kry" and (h["word"][h["rotation"]:] + h["word"][:h["rotation"]]) == "LANTERN"]
    reads = [c for c in result.get("candidates", []) if c["plaintext"] == plant["plaintext"]]
    return bool(hits) and bool(reads), f"dictionary hits {b.get('dictionary_hits')}; the planted one: {bool(hits)}; candidates reading the plant: {len(reads)}"
