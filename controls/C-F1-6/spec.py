"""Positive control for F1/6 (issue #73): plaintext autokey (0003's check).
0003 tested every lag 1-96 under 24 conventions wherever two known letters stand a lag apart; the planted lag
must come out consistent in some convention and not excluded."""
from kryptos.plants import english_plant

ITEM = "F1/6"
EXPERIMENT = "0003"
WHAT = "Plaintext autokey, lag 9, plain standard / cipher standard / key KRYPTOS, variant Beaufort, primer SANDSTORM, on English from Carter"
KEY = {"pa": "std", "ca": "std", "ka": "kry", "m": "varbeau", "lag": 9, "primer": "SANDSTORM"}


def plant():
    return {"plaintext": english_plant(7325), "key": KEY}


def found(result, plant):
    b = result.get("bounds", {})
    cons = b.get("lags_consistent_some_conventions", {})
    ok = (9 in cons or "9" in cons) and 9 not in b.get("lags_excluded_all_conventions", [])
    return ok, f"lags consistent on the plant: {cons}"
