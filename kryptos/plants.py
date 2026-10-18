"""Planted messages for positive controls (issue #73): 97 letters of plain English with the known words
in their places, as K4's plaintext would have them."""
import random
import re
from functools import lru_cache
from pathlib import Path

from kryptos.facts import KNOWN

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "knowledge/sources/carter-1923-tomb-of-tutankhamen-vol1.txt"


@lru_cache(maxsize=1)
def _letters():
    text = SOURCE.read_text(errors="ignore")
    body = text[len(text) // 20: -len(text) // 20]  # skip front and back matter
    return re.sub("[^A-Z]", "", body.upper())


def english_plant(seed):
    """97 letters of Carter's narrative from a seeded offset, with EASTNORTHEAST at 22-34 and
    BERLINCLOCK at 64-74 written over it. Same seed, same text."""
    src = _letters()
    o = random.Random(seed).randrange(0, len(src) - 97)
    p = list(src[o:o + 97])
    for q, ch in KNOWN.items():
        p[q - 1] = ch
    return "".join(p)


def has_known(plaintext):
    return len(plaintext) == 97 and all(plaintext[q - 1] == ch for q, ch in KNOWN.items())
