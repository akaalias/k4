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


# ---- the memorable-key gate (decided 2026-10-15, issue #11) ------------------------------------
# A solution needs a key a person could remember and use by hand in 1990. The harness counts the
# key's size itself from the key the attack hands back, under fixed rules, and a key larger than
# MEMORABLE_MAX_BITS fails a gate. The line is calibrated on the solved sections: K1 is the
# KRYPTOS alphabet plus PALIMPSEST, 80 bits; K2 the same alphabet plus ABSCISSA, 71 bits. 100 bits
# allows the KRYPTOS alphabet plus a keyword of up to 14 letters, or about 21 letters of words.
MEMORABLE_MAX_BITS = 100.0
BITS_PER_LETTER = 4.7          # a letter of an English word, roughly
_MODE_FIELDS = {"m", "mode", "kind", "conv", "convention", "direction", "variant", "form"}


def key_bits_of(key) -> float:
    """The size of a key in bits, counted from its contents.

    Rules: a string of capital letters is a word or letter key, 4.7 bits per letter; a list of
    numbers 0-25 is a letter key written as indices, 4.7 each, and nested lists (matrices) count
    every entry; a 26-letter alphabet costs nothing if standard, 7 letters for the KRYPTOS order,
    its keyword's letters if it is keyword-mixed from a vocabulary word, and log2(26!) = 88 bits
    otherwise; each alphabet is charged once however often it is used; lowercase names ('std',
    'kry') stand for those alphabets; mode and convention fields cost 2 bits; any other number
    costs log2 of its size, at least log2(97) for a place or offset."""
    from .facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY, load_vocabulary
    from .alphabets import keyword_mixed
    seen_alphabets = set()
    vocab = None

    def alphabet_cost(a):
        nonlocal vocab
        if a in seen_alphabets:
            return 0.0
        seen_alphabets.add(a)
        if a == STD:
            return 0.0
        if a == KRY:
            return 7 * BITS_PER_LETTER
        if vocab is None:
            vocab = {}
            for w in load_vocabulary():
                vocab.setdefault(keyword_mixed(w), len(dict.fromkeys(w)))
        if a in vocab:
            return vocab[a] * BITS_PER_LETTER
        return 88.4

    def walk(v, field=None):
        if field in _MODE_FIELDS:
            return 2.0
        if isinstance(v, dict):
            return sum(walk(x, k) for k, x in v.items())
        if isinstance(v, str):
            if v in ("std", "standard"):
                return alphabet_cost(STD)
            if v in ("kry", "kryptos"):
                return alphabet_cost(KRY)
            if len(v) == 26 and v.isalpha() and v.isupper() and len(set(v)) == 26:
                return alphabet_cost(v)
            if v.isalpha() and v.isupper():
                return BITS_PER_LETTER * len(v)
            return 0.0
        if isinstance(v, bool) or v is None:
            return 0.0
        if isinstance(v, (list, tuple)):
            if v and all(isinstance(x, int) and 0 <= x < 26 for x in v):
                return BITS_PER_LETTER * len(v)
            return sum(walk(x) for x in v)
        if isinstance(v, int):
            return math.log2(max(97, abs(v) + 1))
        return 0.0

    return walk(key)
