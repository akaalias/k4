"""Positive control for F1/8 (issue #73): Carter and the sculpture's texts on one vocabulary-mixed side (0047).
0047 tried every offset of Carter vol. 1 and the sculpture's texts with one alphabet standard or KRYPTOS and the
other from the vocabulary, two key alphabets, three modes; the planted text must come back."""
from kryptos.alphabets import keyword_mixed
from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.plants import english_plant

ITEM = "F1/8"
EXPERIMENT = "0047"
WHAT = "Running key from Carter vol. 1, forward, offset 54,321, plain standard, cipher LANGLEY-mixed, key letters on standard, Beaufort, on English from Carter"


def plant():
    return {"plaintext": english_plant(7335),
            "key": {"source": "carter vol1 fwd", "offset": 54321, "pa": STD, "ca": keyword_mixed("LANGLEY"), "ka": STD, "m": "beau"}}


def found(result, plant):
    hit = [c for c in result.get("candidates", []) if c["plaintext"] == plant["plaintext"]]
    b = result.get("bounds", {})
    return bool(hit), f"survivors {b.get('survivors')}; the planted text among them: {bool(hit)}; stopped by clock: {b.get('stopped_by_clock')}"
