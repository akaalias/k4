"""Positive control for F1/1 (issue #73): a periodic key on the standard or KRYPTOS tables.
0005 swept every period 1-97 under all 24 conventions and slid every vocabulary word over each survivor's
forced key; here it must leave the planted period alive and return the planted key word as a candidate."""
from kryptos.plants import english_plant

ITEM = "F1/1"
EXPERIMENT = "0005"
WHAT = "Quagmire III on the KRYPTOS table (K1's system), key PALIMPSEST (period 10), on English from Carter"
KEY = {"pa": "kry", "ca": "kry", "ka": "kry", "m": "vig", "key": "PALIMPSEST"}


def plant():
    return {"plaintext": english_plant(7311), "key": KEY}


def found(result, plant):
    b = result.get("bounds", {})
    alive = 10 in b.get("periods_surviving_some_convention", [])
    hit = [c for c in result.get("candidates", []) if c["plaintext"] == plant["plaintext"] and c["key"]["key"] == "PALIMPSEST"]
    return alive and bool(hit), f"period 10 alive: {alive}; candidates with the planted key and text: {len(hit)} of {len(result.get('candidates', []))}"
