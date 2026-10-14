"""English scorer with a key-length penalty.

english_score(text): mean log10 quadgram probability per quadgram, from the
practicalcryptography.com English quadgram table. Fluent English scores
around -3.5; random letters around -6.5 or worse.

fitness(plaintext, key_bits): english score over the 73 free letters minus
key_bits / 97. One bit of key costs the same as one unit of per-letter
English on a 97-letter text, so a key as long as the message cannot buy
its way to a good score. Calibrated in tests/test_scorer.py against K1-K3.
"""
import math
from functools import lru_cache
from pathlib import Path
from .facts import KNOWN

_QG = Path(__file__).resolve().parent / "data" / "english_quadgrams.txt"


@lru_cache(maxsize=1)
def _table():
    counts = {}
    total = 0
    for line in _QG.read_text().splitlines():
        k, v = line.split()
        counts[k] = int(v)
        total += int(v)
    logs = {k: math.log10(v / total) for k, v in counts.items()}
    floor = math.log10(0.01 / total)
    return logs, floor


def english_score(text: str) -> float:
    """Mean log10 quadgram probability. Higher is more English. Text must be A-Z."""
    logs, floor = _table()
    if len(text) < 4:
        return floor
    s = 0.0
    n = 0
    for i in range(len(text) - 3):
        s += logs.get(text[i : i + 4], floor)
        n += 1
    return s / n


def free_text(plaintext: str) -> str:
    """The 73 letters not pinned by cribs, in order (gaps are concatenated;
    this slightly rewards boundary quadgrams, which is acceptable noise)."""
    return "".join(ch for i, ch in enumerate(plaintext, start=1) if i not in KNOWN)


def key_bits_for_words(*words: str) -> float:
    """Entropy estimate for a key made of English words: 4.7 bits per letter.
    Use this when the key is a keyword or phrase."""
    return 4.7 * sum(len(w) for w in words)


def fitness(plaintext: str, key_bits: float) -> float:
    return english_score(free_text(plaintext)) - key_bits / 97.0


# Loss: lower is better, 0 means solved. Lexicographic by construction: one missed
# crib letter costs 10, more than any English deficit or key cost can add.
ENGLISH_TARGET = -3.6      # mean log10 quadgram score of the K1-K3 plaintexts, roughly
MEMORABLE_BITS = 60.0      # about twelve letters of English words


def loss(plaintext: str, key_bits: float, crib_hits: int) -> float:
    misses = 24 - crib_hits
    english = english_score(free_text(plaintext))
    deficit = max(0.0, ENGLISH_TARGET - english)
    key_cost = max(0.0, key_bits - MEMORABLE_BITS) / MEMORABLE_BITS
    return 10.0 * misses + deficit + key_cost
