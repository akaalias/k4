"""Positive control for F1/5 (issue #73): ciphertext autokey on the standard and KRYPTOS tables.
0002 checked every lag 1-96 under all 24 conventions exactly at every known place past the lag; the planted
lag and convention must survive and decrypt to the planted text past the primer."""
from kryptos.plants import english_plant

ITEM = "F1/5"
EXPERIMENT = "0002"
WHAT = "Ciphertext autokey, lag 5, plain standard / cipher KRYPTOS / key KRYPTOS, Beaufort, primer QUIET, on English from Carter"
KEY = {"pa": "std", "ca": "kry", "ka": "kry", "m": "beau", "lag": 5, "primer": "QUIET"}


def plant():
    return {"plaintext": english_plant(7321), "key": KEY}


def found(result, plant):
    hit = [c for c in result.get("candidates", []) if c["key"]["lag"] == 5 and c["plaintext"][5:] == plant["plaintext"][5:]]
    return bool(hit), f"survivors {result.get('bounds', {}).get('survivors')}; with the planted lag and text past the primer: {len(hit)}"
