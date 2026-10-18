"""Positive control for F1/4 (issue #73): a progressive key on alphabets keyword-mixed from the vocabulary.
0042 tested every pair of 63 vocabulary alphabets, three modes, periods 1-30, steps 1-25 (per repeat), and
matched each survivor's base key against the vocabulary and K1-K3 windows; the planted key must come back."""
from kryptos.alphabets import keyword_mixed
from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.plants import english_plant

ITEM = "F1/4"
EXPERIMENT = "0042"
WHAT = "Progressive key, plain alphabet LODESTONE-mixed, cipher alphabet CARTER-mixed, Beaufort, key WEBSTER (period 7, standard order) advanced 5 at every repeat, on English from Carter"


def plant():
    return {"plaintext": english_plant(7317),
            "key": {"pa": keyword_mixed("LODESTONE"), "ca": keyword_mixed("CARTER"), "m": "beau", "key": [STD.index(c) for c in "WEBSTER"], "step": 5}}


def found(result, plant):
    hit = [c for c in result.get("candidates", []) if c["plaintext"] == plant["plaintext"]]
    return bool(hit), f"candidates with the planted text: {len(hit)} of {len(result.get('candidates', []))}; " + (hit[0]["key_description"] if hit else "")
