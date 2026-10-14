"""Keyword-mixed alphabets, the eight Friedman/Hitt mixings, and the generalised
tableau substitution with separate plain, cipher and key alphabets (Quagmire I-IV).

A "convention" names which alphabet indexes the plaintext, which indexes the
ciphertext, and which indexes the key letter, plus the arithmetic mode.
"""
from .facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY


def dedupe(word: str) -> str:
    seen, out = set(), []
    for ch in word.upper():
        if "A" <= ch <= "Z" and ch not in seen:
            seen.add(ch); out.append(ch)
    return "".join(out)


def keyword_mixed(word: str) -> str:
    """HYDRAULICBEFGJKMNOPQSTVWXZ for HYDRAULIC. KRYPTOS gives the sculpture's alphabet."""
    k = dedupe(word)
    return k + "".join(c for c in STD if c not in k)


def _block(word: str):
    k = dedupe(word)
    rest = [c for c in STD if c not in k]
    w = len(k)
    rows = [list(k)]
    while rest:
        rows.append(rest[:w]); rest = rest[w:]
    return rows, w


def columnar_mixed(word: str) -> str:
    """Simple columnar: write keyword then the rest in rows under it, read down columns left to right."""
    rows, w = _block(word)
    return "".join(r[c] for c in range(w) for r in rows if c < len(r))


def numeric_order(word: str):
    k = dedupe(word)
    order = sorted(range(len(k)), key=lambda i: (k[i], i))
    rank = [0] * len(k)
    for n, i in enumerate(order):
        rank[i] = n
    return rank


def keyed_columnar_mixed(word: str) -> str:
    """Numerically keyed columnar: columns read in alphabetical order of the keyword letters."""
    rows, w = _block(word)
    cols = sorted(range(w), key=lambda c: (dedupe(word)[c], c))
    return "".join(r[c] for c in cols for r in rows if c < len(r))


def alternate_vertical_mixed(word: str) -> str:
    rows, w = _block(word)
    out = []
    for c in range(w):
        col = [r[c] for r in rows if c < len(r)]
        out += col if c % 2 == 0 else col[::-1]
    return "".join(out)


MIXINGS = {
    "keyword": keyword_mixed,
    "columnar": columnar_mixed,
    "keyed_columnar": keyed_columnar_mixed,
    "alt_vertical": alternate_vertical_mixed,
}

ALPHABETS = {"std": STD, "kry": KRY}

MODES = {
    # returns ciphertext index given plaintext index and key index
    "vig": lambda p, k: (p + k) % 26,
    "beau": lambda p, k: (k - p) % 26,
    "varbeau": lambda p, k: (p - k) % 26,
}
INV = {
    "vig": lambda c, k: (c - k) % 26,
    "beau": lambda c, k: (k - c) % 26,
    "varbeau": lambda c, k: (c + k) % 26,
}


def conventions():
    """All 24 combinations of plain alphabet, cipher alphabet, key alphabet and mode."""
    for pa in ALPHABETS:
        for ca in ALPHABETS:
            for ka in ALPHABETS:
                for m in MODES:
                    yield (pa, ca, ka, m)


def encrypt_letter(p, k, pa, ca, ka, m):
    return ALPHABETS[ca][MODES[m](ALPHABETS[pa].index(p), ALPHABETS[ka].index(k))]


def decrypt_letter(c, k, pa, ca, ka, m):
    return ALPHABETS[pa][INV[m](ALPHABETS[ca].index(c), ALPHABETS[ka].index(k))]


def key_letter_for(p, c, pa, ca, ka, m):
    """The key letter that maps p to c under the convention (inverting from a crib)."""
    pi, ci = ALPHABETS[pa].index(p), ALPHABETS[ca].index(c)
    if m == "vig":
        ki = (ci - pi) % 26
    elif m == "beau":
        ki = (ci + pi) % 26
    else:
        ki = (pi - ci) % 26
    return ALPHABETS[ka][ki]
