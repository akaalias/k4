"""Positive control for F1/5 (issue #73): ciphertext autokey on alphabets keyword-mixed from K1-K3 words.
0064 counted mismatches at the known places for 102 x 102 alphabet pairs, four key alphabets, three modes and
lags 1-95; the planted setting must give a full match (no mismatch) at the planted lag, where K4 and its copies
give at least two."""
from kryptos.alphabets import keyword_mixed
from kryptos.plants import english_plant

ITEM = "F1/5"
EXPERIMENT = "0064"
WHAT = "Ciphertext autokey, lag 20, plain CHAMBER-mixed, cipher KRYPTOS, key letters on the plain alphabet, Beaufort, random primer, on English from Carter"


def plant():
    A = keyword_mixed("CHAMBER")
    return {"plaintext": english_plant(7323),
            "key": {"pa": A, "ca": "KRYPTOSABCDEFGHIJLMNQUVWXZ", "ka": A, "m": "beau", "lag": 20, "primer": "THEDOORWAYWASREMOVED"}}


def found(result, plant):
    b = result.get("bounds", {})
    best = b.get("best_setting") or {}
    ok = b.get("fewest_mismatches") == 0 and best.get("lag") == 20 and b.get("full_matches", 0) >= 1
    return ok, f"fewest mismatches {b.get('fewest_mismatches')} at {best}; full matches {b.get('full_matches')}; copies {b.get('control_fewest_mismatches')}"
