"""Positive control for F1/6 (issue #73): plaintext autokey chained from the known letters (0012).
0012 propagated forced letters from the cribs at every lag 1-96 under 24 conventions; at lags up to 13 a crib
run forces the whole text, which is submitted as a candidate. The planted text must come back whole."""
from kryptos.plants import english_plant

ITEM = "F1/6"
EXPERIMENT = "0012"
WHAT = "Plaintext autokey, lag 9, plain standard / cipher standard / key KRYPTOS, variant Beaufort, primer SANDSTORM, on English from Carter"
KEY = {"pa": "std", "ca": "std", "ka": "kry", "m": "varbeau", "lag": 9, "primer": "SANDSTORM"}


def plant():
    return {"plaintext": english_plant(7325), "key": KEY}


def found(result, plant):
    hit = [c for c in result.get("candidates", []) if c["plaintext"] == plant["plaintext"] and c["key"]["lag"] == 9]
    return bool(hit), f"fully forced candidates {result.get('bounds', {}).get('fully_forced_candidates')}; the planted text at lag 9: {bool(hit)}"
