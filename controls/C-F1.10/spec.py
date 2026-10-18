"""Positive control for F1.10 (issue #73): Friedman's keyword-only key-advance schedules (0156).
0156 indexed, for every dictionary word of 3-20 letters, the key letters each word schedule (run length,
CHRISTMAS, EXTINGUISHER windows) puts at the 24 known places, and looked up the key forced on 12 tables x 2
numberings; on K4 no word fits. The planted word must be found under its schedule and table.
Key stream from 0156's own christmas(); its encrypt() is a stub."""
import sys

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F1.10"
EXPERIMENT = "0156"
WHAT = "CHRISTMAS key-advance schedule on the word GARDENING, plain KRYPTOS / cipher standard, Vigenere, key letters numbered on the standard order, on English from Carter"
WORD = "GARDENING"


def plant():
    ex = sys.modules["attack"].christmas(WORD)
    pt = english_plant(7383)
    ct = "".join(STD[(KRY.index(p) + STD.index(ex[i % len(ex)])) % 26] for i, p in enumerate(pt))
    return {"plaintext": pt, "key": (WORD, "christmas", "kry/std/vig", "std"), "ciphertext": ct}


def found(result, plant):
    hits = result.get("bounds", {}).get("k4_word_hits", {}).get("christmas", [])
    ok = any(h["word"] == WORD and h["table"] == "kry/std/vig" and h["numbering"] == "std" for h in hits)
    return ok, f"christmas-schedule word hits on the plant: {[(h['word'], h['table'], h['numbering']) for h in hits[:5]]}"
