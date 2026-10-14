"""Cipher primitives verified against K1-K3 (see tests/).

These are the building blocks an attack may call. They are intentionally
small and explicit so that a worked example can be rendered from them.
"""
from .facts import KRYPTOS_ALPHABET, STANDARD_ALPHABET


def keyed_vigenere_encrypt(plaintext: str, key: str, alphabet: str = KRYPTOS_ALPHABET,
                           passthrough: str = "?") -> str:
    """Quagmire-III style Vigenere over a single keyed alphabet.

    c = A[(A.index(p) + A.index(k)) mod 26]. Characters in `passthrough`
    are copied unchanged and do not consume a key letter (this is what the
    carved K2 does with its three '?').
    """
    out = []
    j = 0
    for p in plaintext:
        if p in passthrough:
            out.append(p)
            continue
        k = key[j % len(key)]
        out.append(alphabet[(alphabet.index(p) + alphabet.index(k)) % 26])
        j += 1
    return "".join(out)


def keyed_vigenere_decrypt(ciphertext: str, key: str, alphabet: str = KRYPTOS_ALPHABET,
                           passthrough: str = "?") -> str:
    out = []
    j = 0
    for c in ciphertext:
        if c in passthrough:
            out.append(c)
            continue
        k = key[j % len(key)]
        out.append(alphabet[(alphabet.index(c) - alphabet.index(k)) % 26])
        j += 1
    return "".join(out)


def tableau_rows(alphabet: str = KRYPTOS_ALPHABET, carved: bool = False):
    """The sculpture's tableau: 26 rows, each a left-shift of the keyed alphabet,
    followed by the first four letters again (30 letters per row as carved).
    With carved=True, row N (index 13) gets the extra L at its end."""
    rows = []
    for i in range(26):
        shifted = alphabet[i:] + alphabet[:i]
        row = shifted + shifted[:4]
        if carved and STANDARD_ALPHABET[i] == "N":
            row += "L"
        rows.append(row)
    return rows


def columnar_transposition_encrypt(plaintext: str, order: list[int]) -> str:
    """Write plaintext in rows of len(order), read columns in the given order.
    `order` is a permutation of range(len(order)); column order[0] is read first."""
    w = len(order)
    rows = [plaintext[i : i + w] for i in range(0, len(plaintext), w)]
    out = []
    for col in order:
        for r in rows:
            if col < len(r):
                out.append(r[col])
    return "".join(out)


def columnar_transposition_decrypt(ciphertext: str, order: list[int]) -> str:
    w = len(order)
    n = len(ciphertext)
    full_rows, rem = divmod(n, w)
    col_len = {col: full_rows + (1 if col < rem else 0) for col in range(w)}
    cols = {}
    i = 0
    for col in order:
        cols[col] = ciphertext[i : i + col_len[col]]
        i += col_len[col]
    out = []
    for r in range(full_rows + (1 if rem else 0)):
        for col in range(w):
            if r < col_len[col]:
                out.append(cols[col][r])
    return "".join(out)


def k3_formula_decrypt(ciphertext: str, a: int = 191, b: int = 192) -> str:
    """Stehle's rule for K3: plaintext[i] = ciphertext[(a + b*i) mod n]."""
    n = len(ciphertext)
    return "".join(ciphertext[(a + b * i) % n] for i in range(n))


def k3_formula_encrypt(plaintext: str, a: int = 191, b: int = 192) -> str:
    n = len(plaintext)
    out = [""] * n
    for i in range(n):
        out[(a + b * i) % n] = plaintext[i]
    return "".join(out)
