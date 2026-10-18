"""Positive control for F1/2 (issue #73): periodic keys on alphabets keyword-mixed from K1-K3 words.
0053 tested every pair of 102 such alphabets, three modes, periods 1-52, and matched the forced key at
periods up to 29 against every word and K1-K3 window; here the planted key must come back as a candidate."""
from kryptos.alphabets import keyword_mixed
from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.plants import english_plant

ITEM = "F1/2"
EXPERIMENT = "0053"
WHAT = "Periodic tableau, plain alphabet SHADING-mixed, cipher alphabet TREMBLING-mixed, Vigenere, key DESPARATLY (period 10, key letters on the standard order), on English from Carter"


def plant():
    return {"plaintext": english_plant(7314),
            "key": {"pa": keyword_mixed("SHADING"), "ca": keyword_mixed("TREMBLING"), "m": "vig", "key": [STD.index(c) for c in "DESPARATLY"]}}


def found(result, plant):
    hit = [c for c in result.get("candidates", []) if c["plaintext"] == plant["plaintext"]]
    return bool(hit), f"candidates with the planted text: {len(hit)} of {len(result.get('candidates', []))}; " + (hit[0].get("key_description", "") if hit else "")
