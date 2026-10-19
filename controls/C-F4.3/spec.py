"""Positive control for F4.3 (issue #73): the places of the sculpture's physical anomalies as a key (0186).
0186 read the anomalies (the ?s, K2's missing S, the raised YAR, the extra L, the odd lines) as 22 number
sequences, added or subtracted each at every alignment to an unknown word of length 1-24 on 12 table rules, and
listed every setting whose forced word (length 4+) is a dictionary word or a rotation of one. 0186's own plant
(SHADOW on the first reading) went through the same scan but with only its one reading and one rule, so it is not
cited; here the planted text goes through the whole scan, and the planted reading, rule, alignment, sign and word
must be listed and give the planted message as a candidate."""
from kryptos.plants import english_plant

ITEM = "F4.3"
EXPERIMENT = "0186"
WHAT = "The gaps between the anomaly places (126, 62, 139, 11, 1, 2, 330), aligned from the fourth, subtracted from the word LANTERN (length 7, standard lettering), Beaufort with plain standard / cipher KRYPTOS, on English from Carter"
READING = "gaps between anomaly places"
KEY = {"reading": READING, "lettering": "std", "word": "LANTERN", "rotation": 0, "rule": "beau/std/kry", "align": 3, "sign": -1}


def plant():
    return {"plaintext": english_plant(7563), "key": KEY}


def found(result, plant):
    b = result.get("bounds", {})
    hits = [h for h in b.get("k4_hits", []) if h["reading"] == READING and h["rule"] == KEY["rule"] and h["align"] == KEY["align"]
            and h["sign"] == KEY["sign"] and h["lettering"] == "std" and h["word"] == "LANTERN" and h["a"] == 7]
    cand = [c for c in result.get("candidates", []) if c["plaintext"] == plant["plaintext"]]
    return bool(hits) and bool(cand), (f"dictionary hits {b.get('dictionary_hits', {}).get('k4')} (copies max "
                                       f"{max(b.get('dictionary_hits', {}).get('coppers', [0]))}); planted setting listed: {bool(hits)}; "
                                       f"candidate reading the planted message: {bool(cand)}")
