"""Positive control for F10.2 (issue #73): Wheatstone cryptograph, the inner ring advanced by the plaintext (0188).
0188 ran 8 variants (outer ring standard or KRYPTOS, blank first or last, hands forward or backward) and, for each,
tested every word-mixed inner ring (keyword alphabets of the dictionary and vocabulary) against the steps the two
known runs force, on K4 and 20 shuffled copies; it lists the word-mixed rings consistent on K4. 0188's own plants
were tested against only the planted ring and 2,000 others at the planted variant, not through the main loop, so
they are not cited; here the planted ring and variant must be listed by the full search. 0188's encrypt() is a
stub; the plant uses 0188's own encipher()."""
import sys

from kryptos.alphabets import keyword_mixed
from kryptos.plants import english_plant

ITEM = "F10.2"
EXPERIMENT = "0188"
WHAT = "Wheatstone cryptograph, outer ring KRYPTOS order with the blank last, hands backward, inner ring mixed from PYRAMID, hand starting at 341 steps, on English from Carter"
VAR, WORD, S0 = ("kry", "last", "bwd"), "PYRAMID", 341


def plant():
    a = sys.modules["attack"]
    inner = keyword_mixed(WORD)
    pt = english_plant(7564)
    return {"plaintext": pt, "key": (VAR, inner, S0), "ciphertext": a.encipher(pt, VAR, inner, S0), "inner": inner}


def found(result, plant):
    b = result.get("bounds", {})
    hit = [h for h in b.get("k4_mixed_hits", []) if h["variant"] == "/".join(VAR) and h["inner"] == plant["inner"]]
    m = b.get("mixed_ring_consistent", {})
    return bool(hit), (f"word-mixed rings consistent {m.get('k4')} (copies max {max(m.get('copies', [0]) or [0])}); the planted "
                       f"PYRAMID ring at {'/'.join(VAR)} listed: {bool(hit)}; free-ring offsets {b.get('free_ring_consistent_offsets', {}).get('k4')}")
