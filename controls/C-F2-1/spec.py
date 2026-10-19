"""Positive control for F2/1 (issue #73): nulls at a regular spacing before a periodic tableau (0023).
0023 moved the known letters by each of 0023's masks (reversal, a null before every k-th letter, k nulls first),
found the periods each convention leaves live, and slid the vocabulary and K1-K3 over each live forced key; here
the planted mask, convention and key word must come back as a candidate that reads the planted message."""
from kryptos.plants import english_plant

ITEM = "F2/1"
EXPERIMENT = "0023"
WHAT = "A null before every 7th letter (phase 3), then Beaufort with plain KRYPTOS / cipher standard / key KRYPTOS alphabets, key LODESTONE (period 9), on English from Carter"
MASK = {"rev": False, "k": 7, "phase": 3, "prefix": 0}
KEY = {"mask": MASK, "pa": "kry", "ca": "std", "ka": "kry", "m": "beau", "key": "LODESTONE"}


def plant():
    return {"plaintext": english_plant(7550), "key": KEY}


def found(result, plant):
    import sys
    pm = sys.modules["attack"].position_map(MASK)
    pt = plant["plaintext"]
    hit = [c for c in result.get("candidates", []) if c["key"] == KEY and all(c["plaintext"][i] == pt[i] for i in pm)]
    return bool(hit), (f"vocabulary matches {result.get('bounds', {}).get('vocab_matches')}; the planted mask, convention and "
                       f"LODESTONE reading the planted message: {bool(hit)} (of {len(result.get('candidates', []))} candidates listed)")
