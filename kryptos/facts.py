"""Frozen facts. Loaded from data/ so the files stay the single source of truth."""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"

STANDARD_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KRYPTOS_ALPHABET = "KRYPTOSABCDEFGHIJLMNQUVWXZ"

K4 = (DATA / "k4.txt").read_text().strip()
assert len(K4) == 97, "K4 must be 97 letters"

_cribs = json.loads((DATA / "cribs.json").read_text())["cribs"]
CRIBS = [(c["start"], c["plaintext"]) for c in _cribs]

# KNOWN: 1-indexed position -> plaintext letter, for all 24 crib letters
KNOWN = {}
for start, word in CRIBS:
    for i, ch in enumerate(word):
        KNOWN[start + i] = ch
assert len(KNOWN) == 24

for c in _cribs:
    s = c["start"]
    assert K4[s - 1 : s - 1 + len(c["plaintext"])] == c["ciphertext"], c


def load_k1():
    return json.loads((DATA / "k1.json").read_text())


def load_k2():
    return json.loads((DATA / "k2.json").read_text())


def load_k3():
    return json.loads((DATA / "k3.json").read_text())


def load_vocabulary():
    return [w.strip() for w in (DATA / "vocabulary.txt").read_text().splitlines() if w.strip()]
