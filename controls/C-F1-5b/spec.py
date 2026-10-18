"""Positive control for F1/5 (issue #73): ciphertext autokey on alphabets keyword-mixed from the vocabulary.
0025 tested 63 x 63 vocabulary alphabet pairs, three key alphabets, three modes and lags 1-96; a setting with
no mismatch on 12 or more known places is a survivor. The planted setting must be among them. 0025 ran 46
minutes on K4 without checking the clock, so this control gets a longer budget."""
from kryptos.alphabets import keyword_mixed
from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.plants import english_plant

ITEM = "F1/5"
EXPERIMENT = "0025"
WHAT = "Ciphertext autokey, lag 13, plain SHADOW-mixed, cipher COMPASS-mixed, key letters on the standard order, variant Beaufort, random primer, on English from Carter"
BUDGET = 4200


def plant():
    return {"plaintext": english_plant(7322),
            "key": {"pa": keyword_mixed("SHADOW"), "ca": keyword_mixed("COMPASS"), "ka": STD, "m": "varbeau", "lag": 13, "primer": "LIGHTANDSHADE", "kind": "ciphertext"}}


def found(result, plant):
    hit = [c for c in result.get("candidates", []) if c["key"].get("kind") == "ciphertext" and c["key"]["lag"] == 13
           and c["plaintext"][13:] == plant["plaintext"][13:]]
    return bool(hit), f"ciphertext-autokey survivors {result.get('bounds', {}).get('ciphertext_autokey_survivors')}; with the planted lag and text: {len(hit)}"
