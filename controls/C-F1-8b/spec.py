"""Positive control for F1/8 (issue #73): a running key from the sculpture's own texts (0017).
0017 tried every offset of the carved tableau (rows, columns, with index), the Morse and the right panel,
forward and backward, under 24 conventions; the planted text must come back."""
from kryptos.plants import english_plant

ITEM = "F1/8"
EXPERIMENT = "0017"
WHAT = "Running key from the carved tableau read by rows, forward, offset 200, plain standard / cipher KRYPTOS / key KRYPTOS, Vigenere, on English from Carter"


def plant():
    return {"plaintext": english_plant(7332), "key": {"source": "tableau rows fwd", "offset": 200, "pa": "std", "ca": "kry", "ka": "kry", "m": "vig"}}


def found(result, plant):
    hit = [c for c in result.get("candidates", []) if c["plaintext"] == plant["plaintext"]]
    return bool(hit), f"survivors {result.get('bounds', {}).get('survivors')}; the planted text among them: {bool(hit)}"
