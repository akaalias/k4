"""Positive control for F2/1 (issue #73): an affine (decimated-alphabet) mask before a periodic key (0074).
0074 counted, for 110 pairings of a decimated alphabet with the standard, KRYPTOS or itself, the periods 1-52 the
known letters leave consistent, against 10 shuffled copies, and read the forced keys at periods up to 29 for words;
here the planted period must be live above every copy, and the planted key word must come back from the planted
pairing. 0074's encrypt() is a stub, so the plant makes its own ciphertext."""
from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.plants import english_plant

ITEM = "F2/1"
EXPERIMENT = "0074"
WHAT = "Message on the standard alphabet decimated by 7, carved on the standard alphabet, Vigenere, key LODESTONE (period 9), on English from Carter"
P, WORD = 9, "LODESTONE"


def plant():
    pa = "".join(STD[(7 * i) % 26] for i in range(26))
    pt = english_plant(7552)
    ct = "".join(STD[(pa.index(ch) + STD.index(WORD[i % P])) % 26] for i, ch in enumerate(pt))
    return {"plaintext": pt, "key": ("stdx7/std", "vig", WORD), "ciphertext": ct}


def found(result, plant):
    b = result.get("bounds", {})
    row = b.get("periodic_consistent_by_period", {}).get(str(P), {"k4": 0, "controls": [0]})
    above = row["k4"] > 0 and row["k4"] > max(row["controls"])
    word = [h for h in b.get("word_matches", []) if h["pairing"] == "stdx7/std" and h["mode"] == "vig" and h["period"] == P and WORD in h["run"]]
    return above and bool(word), f"period {P}: live {row['k4']}, copies {row['controls']}; LODESTONE read from stdx7/std at {P}: {bool(word)}"
