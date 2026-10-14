"""Crib-consistency sweep for periodic additive ciphers over a fixed alphabet.

For each period L and each mode, check whether the 24 known (plaintext,
ciphertext) pairs can be explained by a key that repeats every L letters.
Positions congruent mod L must imply the same key letter.

This is the loop's first unit test and the reason the loop refuses to spend
time on periods 1-26 and 30-52 for single-alphabet additive systems.
"""
from .facts import K4, KNOWN, KRYPTOS_ALPHABET, STANDARD_ALPHABET

MODES = {
    "vigenere": lambda p, c: (c - p) % 26,
    "beaufort": lambda p, c: (c + p) % 26,
    "variant_beaufort": lambda p, c: (p - c) % 26,
}
ALPHABETS = {"standard": STANDARD_ALPHABET, "kryptos": KRYPTOS_ALPHABET}


def consistent_periods(alphabet: str, mode) -> list[int]:
    ok = []
    for L in range(1, 98):
        slots = {}
        good = True
        for pos, p in KNOWN.items():
            k = mode(alphabet.index(p), alphabet.index(K4[pos - 1]))
            slot = (pos - 1) % L
            if slot in slots and slots[slot] != k:
                good = False
                break
            slots[slot] = k
        if good:
            ok.append(L)
    return ok


def sweep() -> dict[tuple[str, str], list[int]]:
    return {(an, mn): consistent_periods(A, f) for an, A in ALPHABETS.items() for mn, f in MODES.items()}


def implied_key_fragment(alphabet: str, mode) -> str:
    """The key letters the cribs force at each crib position, '.' elsewhere."""
    return "".join(
        alphabet[mode(alphabet.index(KNOWN[p]), alphabet.index(K4[p - 1]))] if p in KNOWN else "."
        for p in range(1, 98)
    )


if __name__ == "__main__":
    for (an, mn), periods in sweep().items():
        print(f"{an:9s} {mn:17s} consistent periods: {periods}")
    for an, A in ALPHABETS.items():
        for mn, f in MODES.items():
            print(f"{an:9s} {mn:17s} {implied_key_fragment(A, f)}")
