"""Positive control for F1.8 (issue #73): Carter's book as a running key on one unknown alphabet (0154).
0154 decided exactly, for every offset of Carter vol. 1 forward and backward and three forms, whether any one
alphabet fits the 24 known letters (compiled solver); on K4 none did. The planted offset must fit.
0154's encrypt() is a stub, so the plant makes its own ciphertext from the same letters of the book."""
import random
import re

from kryptos.plants import english_plant

ITEM = "F1.8"
EXPERIMENT = "0154"
WHAT = "Running key from Carter vol. 1 forward at offset 200,000, added form, one random alphabet on both sides, on English from Carter"
OFF = 200000


def plant():
    carter = re.sub("[^A-Z]", "", open("knowledge/sources/carter-1923-tomb-of-tutankhamen-vol1.txt", errors="ignore").read().upper())
    rng = random.Random(7382)
    al = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"); rng.shuffle(al)
    pos = {c: i for i, c in enumerate(al)}
    pt = english_plant(7382)
    ct = "".join(al[(pos[p] + pos[carter[OFF + i]]) % 26] for i, p in enumerate(pt))
    return {"plaintext": pt, "key": ("".join(al), "carter fwd", OFF, "V"), "ciphertext": ct}


def found(result, plant):
    b = result.get("bounds", {})
    fl = b.get("k4_fit_list", [])
    ok = str(OFF) in str(fl)
    return ok, f"fits on the plant {b.get('k4_fits_total')}, copies {b.get('controls_fits_total')}; offset {OFF} listed: {ok}; list {str(fl)[:200]}"
