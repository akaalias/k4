"""Positive control for F3.6 (issue #73): the Weltzeituhr ring turning through the text as a per-place offset (0179).
0179's own plant (a 'rep' reading, one zone per letter, + SHADOW) went through its scan() and was found; its 48
per-place readings (the ring turning one zone every 24 or every 4 letters, from each start) take a different branch
of scan(). Here the plant uses one of them, and the planted word must come back as a dictionary hit with the planted
reading, rule and sign, and its candidate must read the planted text (hits listed up to 40, candidates from the first
20; K4 had 0). The attack's own encrypt() makes the ciphertext."""
from kryptos.plants import english_plant

ITEM = "F3.6"
EXPERIMENT = "0179"
WHAT = ("WINDMILL on the standard order plus the ring turning one zone every 4 letters from start 5; plain KRYPTOS, "
        "cipher KRYPTOS, Vigenere; on English from Carter")
KEY = {"reading": "ring turns one zone every 4 letters (97 over 24 zones), start 5", "lettering": "std", "word": "WINDMILL",
       "rotation": 0, "rule": "vig/kry/kry", "align": 0, "sign": 1}


def plant():
    return {"plaintext": english_plant(7546), "key": KEY}


def found(result, plant):
    b = result.get("bounds", {})
    hits = [h for h in b.get("k4_hits", []) if h["reading"] == KEY["reading"] and h["rule"] == KEY["rule"] and h["sign"] == 1
            and h["lettering"] == "std" and (h["word"][h["rotation"]:] + h["word"][:h["rotation"]]) == "WINDMILL"]
    reads = [c for c in result.get("candidates", []) if c["plaintext"] == plant["plaintext"]]
    return bool(hits) and bool(reads), f"dictionary hits {b.get('dictionary_hits')}; the planted one: {bool(hits)}; candidates reading the plant: {len(reads)}"
