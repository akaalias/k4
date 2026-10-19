"""Positive control for F6/1 (issue #73): K3's rule with every shift, then a periodic key (0008).
0008 ran plaintext[i] = inter[(a + b i) mod 97] for all 9,312 (a, b), forward and inverse, and the double rotations,
before a periodic key under 24 conventions, and slid the vocabulary and K1-K3 windows over every live period up to 30;
here it must return the planted rule and key word as a candidate that decrypts to the planted text. Candidates are
cut at 50; K4 gave 0 matches, so noise does not crowd the plant out."""
from kryptos.plants import english_plant

ITEM = "F6/1"
EXPERIMENT = "0008"
WHAT = "K3's rule with a=40, b=23 (forward), then the KRYPTOS table, Vigenere, key LODESTONE (period 9), on English from Carter"
KEY = {"route": {"kind": "affine", "a": 40, "b": 23, "dir": "fwd"}, "pa": "kry", "ca": "kry", "ka": "kry", "m": "vig", "key": "LODESTONE"}


def plant():
    return {"plaintext": english_plant(7401), "key": KEY}


def found(result, plant):
    cands = result.get("candidates", [])
    hit = [c for c in cands if c["key"]["route"] == KEY["route"] and c["key"]["key"] == "LODESTONE" and c["plaintext"] == plant["plaintext"]]
    return bool(hit), f"vocabulary matches {result.get('bounds', {}).get('vocab_matches')}; candidates {len(cands)}; the planted rule and key: {bool(hit)}"
