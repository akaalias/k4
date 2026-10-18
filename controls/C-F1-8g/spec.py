"""Positive control for F1/8 (issue #73): the sculpture's running keys on an unknown alphabet (0098).
0098 decided exactly, for every offset of 26 sculpture and Sanborn texts and three rules, whether any one mixed
alphabet (Quagmire III, any of 26! orders) fits the 24 known letters; the planted setting must be consistent.
0098's encrypt() is a stub, so the plant makes its own ciphertext."""
import random
import sys

from kryptos.plants import english_plant

ITEM = "F1/8"
EXPERIMENT = "0098"
WHAT = "Running key from the K1-K3 plaintexts, forward, offset 200, on a random alphabet used for plain, cipher and key (Quagmire III, Vigenere), on English from Carter"


def plant():
    rng = random.Random(7337)
    X = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"); rng.shuffle(X)
    srcs, _ = sys.modules["attack"].sources()
    s = srcs["K1-K3 plaintexts fwd"]
    pt = english_plant(7337)
    ct = "".join(X[(X.index(p) + X.index(s[(200 + i) % len(s)])) % 26] for i, p in enumerate(pt))
    return {"plaintext": pt, "key": ("".join(X), "K1-K3 plaintexts fwd", 200, "vig"), "ciphertext": ct}


def found(result, plant):
    b = result.get("bounds", {})
    hit = [e for e in b.get("k4_consistent_settings", []) if e["source"] == "K1-K3 plaintexts fwd" and e["offset"] == 200 and e["rule"] == "vig"]
    return bool(hit), f"consistent settings on the plant {b.get('k4_consistent')}, copies {b.get('controls_consistent')}; the planted one: {bool(hit)}"
