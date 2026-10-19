"""Positive control for F3/1 (issue #73): two puzzle words in two passes on the standard and KRYPTOS tables (0014).
0014 wrote the 24 known letters as linear equations in the two words' letters for every length pair 2 <= a < b <= 30
whose combined period is not already excluded, solved them exactly, and submitted every solution whose first or
second word is a puzzle word or a stretch of K1-K3; K4 gave none. Here the planted pair must come back as a
candidate that reads the planted text. The attack's own encrypt() makes the ciphertext."""
from kryptos.plants import english_plant

ITEM = "F3/1"
EXPERIMENT = "0014"
WHAT = ("Two passes, EGYPT (5) then UNDERGROUND (11), combined period 55; plain standard, cipher KRYPTOS, words read on "
        "the KRYPTOS order, Vigenere both passes; on English from Carter")
KEY = {"pa": "std", "ca": "kry", "ka": "kry", "m1": "vig", "m2": "vig", "X": "EGYPT", "Y": "UNDERGROUND"}


def plant():
    return {"plaintext": english_plant(7531), "key": KEY}


def found(result, plant):
    b = result.get("bounds", {})
    c = result.get("candidates", [])
    hit = [x for x in c if x["plaintext"] == plant["plaintext"] and (x["key"]["X"], x["key"]["Y"]) == (KEY["X"], KEY["Y"])]
    return bool(hit), (f"word matches {b.get('vocab_or_k1k3_matches')} (first 50 listed); candidates with the planted pair "
                       f"and text: {len(hit)}; consistent cases {b.get('survivors')}")
