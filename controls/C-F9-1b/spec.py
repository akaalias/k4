"""Positive control for F9/1 (issue #73): a one-to-one substitution, then a triple clockwise turn (0106).
0106 ran the one-to-one test (equal known letters on equal carved letters, different on different) over 1.84 million
deduplicated routes: the type-1 library, grid paths, mixed double turns and every triple clockwise turn at widths
2-96. Here the planted triple turn must survive under its own name and its set must count more survivors on the
planted text than on every shuffled copy. 0106 lists the first 20 survivors sorted by letters fixed; the plant fixes
every letter its 13 known letters reach, so it sorts near the top. 0106's encrypt() is a stub, so the plant makes its
own ciphertext."""
import random
import sys

from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.plants import english_plant

ITEM = "F9/1"
EXPERIMENT = "0106"
TURNS = [(23, "cw"), (9, "cw"), (31, "cw")]
TAG = "cw 23, 9, 31"
WHAT = "Random one-to-one substitution, then three clockwise quarter turns at widths 23, 9, 31, on English from Carter"


def plant():
    rng = random.Random(7631)
    sig = list(STD); rng.shuffle(sig)
    pt = english_plant(7631)
    wh = sys.modules["attack"].where_of_turns(TURNS)
    ct = [""] * 97
    for i, ch in enumerate(pt):
        ct[wh[i]] = sig[STD.index(ch)]
    return {"plaintext": pt, "key": ("".join(sig), TAG), "ciphertext": "".join(ct)}


def found(result, plant):
    b = result.get("bounds", {})
    cell = b.get("consistent_by_set", {}).get("triple clockwise turns", {"k4": 0, "controls": []})
    named = [s for s in b.get("k4_survivors", []) if s["set"] == "triple clockwise turns" and s["route"] == TAG]
    ok = bool(named) and cell["k4"] > max(cell["controls"] or [0]) and not b.get("stopped")
    return ok, f"triple turns consistent {cell['k4']} vs copies {cell['controls']}; survivors {b.get('n_k4_survivors')}; '{TAG}' listed: {bool(named)}; stopped {b.get('stopped')}"
