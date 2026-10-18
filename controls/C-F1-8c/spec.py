"""Positive control for F1/8 (issue #73): Carter's book as a running key (0021).
0021 tried every offset of Carter vol. 1 forward and backward under 24 conventions; the planted text must come
back. The plant's own English comes from another part of the same book (kryptos.plants)."""
from kryptos.plants import english_plant

ITEM = "F1/8"
EXPERIMENT = "0021"
WHAT = "Running key from Carter vol. 1 read backward, offset 123,456, plain KRYPTOS / cipher KRYPTOS / key standard, variant Beaufort, on English from Carter"


def plant():
    return {"plaintext": english_plant(7333), "key": {"source": "carter vol1 bwd", "offset": 123456, "pa": "kry", "ca": "kry", "ka": "std", "m": "varbeau"}}


def found(result, plant):
    hit = [c for c in result.get("candidates", []) if c["plaintext"] == plant["plaintext"]]
    return bool(hit), f"survivors {result.get('bounds', {}).get('survivors')}; the planted text among them: {bool(hit)}"
