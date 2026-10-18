"""Positive control for F1/8 (issue #73): the sculpture's running keys plus a constant shift, no move (0117).
0117 matched the key differences forced at the 24 known places against every offset of the sculpture's,
Sanborn's and Carter's texts (change, then a type-1 move whose library includes the identity, K3's rule with
a=0, b=1), 12 conventions; the planted text, offset and convention must be a full hit with no move.
0117's encrypt() is a stub, so the plant makes its own ciphertext."""
import sys

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F1/8"
EXPERIMENT = "0117"
WHAT = "Running key from the K1-K3 plaintexts, forward, offset 50, numbered on the standard order, plus a constant shift of 7, plain standard / cipher KRYPTOS, Vigenere, no move, on English from Carter"


def plant():
    srcs, _ = sys.modules["attack"].sources()
    y = [STD.index(c) for c in srcs["K1-K3 plaintexts fwd"]]
    pt = english_plant(7338)
    ct = "".join(KRY[(STD.index(p) + y[(50 + i) % len(y)] + 7) % 26] for i, p in enumerate(pt))
    return {"plaintext": pt, "key": ("K1-K3 plaintexts fwd [std]", 50, "shift 7", "vig/std/kry", "no move"), "ciphertext": ct}


def found(result, plant):
    a = result.get("bounds", {}).get("change_then_move", {})
    hits = a.get("k4_full_hits", [])
    ok = [h for h in hits if h[0].startswith("K3 rule a=0 b=1") and h[1] == "vig/std/kry"
          and any(tuple(x) == ("K1-K3 plaintexts fwd [std]", 50) for x in h[3])]
    return bool(ok), f"full hits (change then move) {a.get('k4_full')}, copies {a.get('controls_full')}; the planted one with no move: {bool(ok)}"
