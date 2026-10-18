"""Positive control for F1/8 (issue #73): K1-K3 running keys on vocabulary-mixed alphabets (0045).
0045 tried every offset of the K1-K3 plaintexts and ciphertexts under 63 x 63 vocabulary alphabet pairs, two key
alphabets and three modes; the planted text must come back."""
from kryptos.alphabets import keyword_mixed
from kryptos.facts import KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F1/8"
EXPERIMENT = "0045"
WHAT = "Running key from K2's ciphertext, backward, offset 77, plain ORDINATE-mixed, cipher MAGNETIC-mixed, key letters on KRYPTOS, Vigenere, on English from Carter"


def plant():
    return {"plaintext": english_plant(7334),
            "key": {"source": "K2 cipher bwd", "offset": 77, "pa": keyword_mixed("ORDINATE"), "ca": keyword_mixed("MAGNETIC"), "ka": KRY, "m": "vig"}}


def found(result, plant):
    hit = [c for c in result.get("candidates", []) if c["plaintext"] == plant["plaintext"]]
    b = result.get("bounds", {})
    return bool(hit), f"survivors {b.get('survivors')}; the planted text among them: {bool(hit)}; stopped by clock: {b.get('stopped_by_clock')}"
