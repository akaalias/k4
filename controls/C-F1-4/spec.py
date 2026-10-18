"""Positive control for F1/4 (issue #73): a progressive key on the standard and KRYPTOS tables.
0011 swept every period 1-97, step 0-25, both forms and 24 conventions, and slid the vocabulary and K1-K3
windows over each survivor's base key; here the planted key word must come back as a candidate."""
from kryptos.plants import english_plant

ITEM = "F1/4"
EXPERIMENT = "0011"
WHAT = "Progressive key on the KRYPTOS table throughout, Vigenere, key ABSCISSA (period 8) advanced 3 places at every repeat, on English from Carter"
KEY = {"pa": "kry", "ca": "kry", "ka": "kry", "m": "vig", "key": "ABSCISSA", "step": 3, "form": "per-repeat"}


def plant():
    return {"plaintext": english_plant(7316), "key": KEY}


def found(result, plant):
    hit = [c for c in result.get("candidates", []) if c["plaintext"] == plant["plaintext"] and c["key"]["key"] == "ABSCISSA" and c["key"]["step"] == 3]
    return bool(hit), f"candidates with the planted key, step and text: {len(hit)} of {len(result.get('candidates', []))}"
