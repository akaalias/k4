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


# ---- the key's size, counted by the harness (decided 2026-10-15, issue #23) -------------------
# The harness counts a key's size itself from the key an attack hands back, under fixed rules,
# and charges it in the loss. It is not a gate: a gate on key size was tried and dropped the same
# day, because K1-K3's short keywords are too thin a basis for a hard limit on K4's key, and a
# long key can still have a short description (a running key from a named book). The guard
# against keys fitted to the answer is the shuffled-copper baseline gate in run_experiment.py.
BITS_PER_LETTER = 4.7          # an arbitrary letter: log2(26)
_MODE_FIELDS = {"m", "mode", "kind", "conv", "convention", "direction", "variant", "form"}


WORDS_FILE = Path(__file__).resolve().parent / "data" / "words.txt"


@lru_cache(maxsize=1)
def _dictionary():
    words = set(WORDS_FILE.read_text().split()) if WORDS_FILE.exists() else set()
    from .facts import load_vocabulary
    vocab = {w.upper() for w in load_vocabulary()}
    return words, vocab


def _words_cost(s: str):
    """Bits to name s as at most four words: log2(len(vocabulary)) per puzzle word, log2(len(
    dictionary)) per other dictionary word; None if s is not such a phrase."""
    words, vocab = _dictionary()
    vb, db = math.log2(max(2, len(vocab))), math.log2(max(2, len(words)))
    best = [0.0] + [None] * len(s)
    count = [0] + [0] * len(s)
    for i in range(1, len(s) + 1):
        for j in range(max(0, i - 25), i - 1):
            if best[j] is None or count[j] >= 4:
                continue
            w = s[j:i]
            c = vb if w in vocab else (db if w in words else None)
            if c is not None and (best[i] is None or best[j] + c < best[i]):
                best[i], count[i] = best[j] + c, count[j] + 1
    return best[len(s)]


def key_bits_of(key) -> float:
    """The length of the key's description in bits, counted from its contents.

    A key is charged for what it takes to write it down, not for how many letters it spreads
    over. Rules: a string of capital letters (or a list of numbers 0-25 read as letters) costs,
    if it is a phrase of up to four words, log2 of the puzzle vocabulary per puzzle word and
    log2 of the dictionary per other word, and otherwise 4.7 bits per letter, as arbitrary
    letters; a 26-letter alphabet costs nothing if standard, the word KRYPTOS for the KRYPTOS
    order, its keyword if keyword-mixed from a puzzle word, and log2(26!) = 88 bits otherwise,
    once however often it is used; lowercase names stand for alphabets ('std', 'kry') or for a
    named text (6.6 bits); mode and convention fields cost 2 bits; nested lists (matrices)
    count every entry at 4.7 bits; any other number costs log2 of its size, at least log2(97)
    for a place or offset. A running key from a named book at an offset is therefore cheap,
    and 74 letters chosen to fit the known letters are expensive."""
    from .facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY, load_vocabulary
    from .alphabets import keyword_mixed
    seen_alphabets = set()
    mixed = {}

    def letters_cost(s):
        c = _words_cost(s)
        return c if c is not None else BITS_PER_LETTER * len(s)

    def alphabet_cost(a):
        if a in seen_alphabets:
            return 0.0
        seen_alphabets.add(a)
        if a == STD:
            return 0.0
        if a == KRY:
            return letters_cost("KRYPTOS")
        if not mixed:
            for w in load_vocabulary():
                mixed.setdefault(keyword_mixed(w), w.upper())
        if a in mixed:
            return letters_cost(mixed[a])
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
                return letters_cost(v)
            return math.log2(97) if v else 0.0
        if isinstance(v, bool) or v is None:
            return 0.0
        if isinstance(v, (list, tuple)):
            if v and all(isinstance(x, int) and not isinstance(x, bool) and 0 <= x < 26 for x in v):
                return letters_cost("".join(STD[x] for x in v))
            return sum(walk(x) for x in v)
        if isinstance(v, int):
            return math.log2(max(97, abs(v) + 1))
        return 0.0

    return walk(key)
