"""Positive control for F1/8 (issue #73): a running key from K1-K3 on the standard and KRYPTOS tables (0004).
0004 tried every offset of 18 K1-K3 texts (plain and cipher, forward and reversed) under 24 conventions and
decrypts every zero-mismatch setting; the planted text must come back."""
from kryptos.plants import english_plant

ITEM = "F1/8"
EXPERIMENT = "0004"
WHAT = "Running key from K3's plaintext, forward, offset 100, plain KRYPTOS / cipher standard / key standard, Beaufort, on English from Carter"


def plant():
    import sys
    text = sys.modules["attack"].sources()["K3pt_fwd"]
    return {"plaintext": english_plant(7331), "key": {"text": text, "offset": 100, "pa": "kry", "ca": "std", "ka": "std", "m": "beau"}}


def found(result, plant):
    hit = [c for c in result.get("candidates", []) if c["plaintext"] == plant["plaintext"]]
    return bool(hit), f"survivors {result.get('bounds', {}).get('survivors')}; the planted text among them: {bool(hit)}"
