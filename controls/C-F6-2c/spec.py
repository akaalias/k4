"""Positive control for F6/2 (issue #73): a move, then a running key from the sculpture's texts (0090).
0090 ran 27,000+ distinct routes (K3's rule, quarter turns, two turns, columnar, keyed columnar) under 12 conventions
and, for a move then a running key read at the carved places, filtered every offset of the K1-K3 plaintexts, the
tableau, the Morse, the panel ciphertexts and Sanborn's letters check by check (no full match on K4); here the planted
text, offset, route and convention must reach all 24 checks and come back as a candidate that reads the planted text.
0090's encrypt() is a stub, so the plant makes its own ciphertext with 0090's own sources() and moves."""
import sys

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F6/2"
EXPERIMENT = "0090"
WHAT = "An anticlockwise quarter turn in rows of 10 (forward), then a running key from the K1-K3 plaintexts at offset 200 read at the carved places, key letters numbered on the standard order, KRYPTOS table, Vigenere, on English from Carter"
SRC, OFF, W = "K1-K3 plaintexts fwd", 200, 10


def plant():
    a = sys.modules["attack"]
    srcs, _ = a.sources()
    sigma = a.perm_of(lambda s: a.rot_ccw(s, W))
    where = [0] * 97
    for j, i in enumerate(sigma):
        where[i] = j
    pt = english_plant(7409)
    moved = [""] * 97
    for i, j in enumerate(where):
        moved[j] = pt[i]
    key = srcs[SRC][OFF:OFF + 97]
    ct = "".join(KRY[(KRY.index(ch) + STD.index(key[j])) % 26] for j, ch in enumerate(moved))
    return {"plaintext": pt, "key": (f"turn ccw {W}", SRC, OFF, "vig/std/kry", "move then change"), "ciphertext": ct}


def found(result, plant):
    b = result.get("bounds", {}).get("move_then_change", {})
    hit = [c for c in result.get("candidates", []) if c["plaintext"] == plant["plaintext"]
           and c["key"].startswith(f"move then change: {SRC} offset {OFF},") and c["key"].endswith("vig/std/kry")]
    return bool(hit), (f"move then change: full matches {b.get('k4_full')}, deepest {b.get('k4_best_depth')}, copies' deepest "
                       f"{b.get('controls_best_depth')}; the planted text, offset and convention as a candidate: {bool(hit)}")
