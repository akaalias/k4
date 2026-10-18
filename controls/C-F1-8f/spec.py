"""Positive control for F1/8 (issue #73): Sanborn's own letters as a running key (0078).
0078 counted mismatches at the 24 known places for every offset of three letters by Sanborn, forward and reversed,
under 390 table setups, and lists every setting within three mismatches; the planted one must be listed with 0.
0078's encrypt() is a stub, so the plant makes its own ciphertext."""
import sys

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F1/8"
EXPERIMENT = "0078"
WHAT = "Running key from Sanborn's 1989 letter, forward, offset 900, plain standard / cipher KRYPTOS / key standard, Vigenere, on English from Carter"


def plant():
    text = sys.modules["attack"].sources()["letter 1989"]
    pt = english_plant(7336)
    ct = "".join(KRY[(STD.index(p) + STD.index(text[(900 + i) % len(text)])) % 26] for i, p in enumerate(pt))
    return {"plaintext": pt, "key": ("letter 1989", "forwards", 900, "std/kry/std/vig"), "ciphertext": ct}


def found(result, plant):
    b = result.get("bounds", {})
    hit = [e for e in b.get("k4_within_3", []) if e["source"] == "letter 1989" and e["direction"] == "forwards" and e["offset"] == 900
           and e["setup"] == "std/kry/std/vig" and e["mismatches"] == 0]
    return bool(hit), f"fewest mismatches {b.get('k4_fewest_mismatches')}, within 3: {b.get('k4_within_3_count')}, the planted setting at 0: {bool(hit)}; copies fewest {b.get('controls_fewest')}"
