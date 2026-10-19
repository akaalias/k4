"""Positive control for F4/2 (issue #73): the plates as a running key by position, straight or folded (0089).
0089 laid the tableau plates and the cipher plates over K4's place on the screen (25 line windows, straight or
folded, column shifts -4 to 4, 12 conventions) and listed every overlay giving all 24 known letters as a candidate
with its decryption; here the planted overlay must be listed and read the planted message wherever it gives a key.
0089 first asserts that the copper it is given is K4 as carved on the lower-left plate; that K4 self-check is
skipped by PATCH, the search is unchanged. 0089's encrypt() is a stub, so the plant makes its own ciphertext (at the
few places the overlay gives no key letter, a random letter)."""
import random
import sys

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F4/2"
EXPERIMENT = "0089"
WHAT = "The cipher plates as key, window from source line 20 of 28 (the lower-left plate's 6th line laid over K4's first line), folded, column shift +1, Beaufort with key letters on KRYPTOS / table on standard, on English from Carter"
PATCH = [('    assert "".join(LOWER_LEFT[10][27:]) + "".join(LOWER_LEFT[11:]) == ct\n', '')]
SRC, D0, FOLD, S, CONV = "cipher", 19, True, 1, ("beau", "kry", "std")


def keys():
    a = sys.modules["attack"]
    cells = a.k4_cells()
    lines = (a.UPPER_LEFT + a.LOWER_LEFT) if SRC == "cipher" else None
    out = []
    for p in range(1, 98):
        i, c = cells[p - 1]
        line = lines[D0 + (i - 10)]
        col = (32 - c if FOLD else c) + S
        out.append(line[col - 1] if 1 <= col <= len(line) and line[col - 1].isalpha() else None)
    return out


def plant():
    a = sys.modules["attack"]
    rng = random.Random(7559)
    pt = english_plant(7559)
    mode, ka, ta = CONV
    AL = {"std": STD, "kry": KRY}
    ks = keys()
    ct = "".join(AL[ta][a.enc(mode, AL[ta].index(ch), AL[ka].index(k))] if k else STD[rng.randrange(26)] for ch, k in zip(pt, ks))
    return {"plaintext": pt, "key": (SRC, D0 + 1, "folded" if FOLD else "straight", S, "/".join(CONV)), "ciphertext": ct}


def found(result, plant):
    want = f"screen overlay {SRC} line {D0 + 1} {'folded' if FOLD else 'straight'} shift {S} {'/'.join(CONV)}"
    pt = plant["plaintext"]
    hit = [c for c in result.get("candidates", []) if c["key"] == want and all(x == "?" or x == y for x, y in zip(c["plaintext"], pt))]
    b = result.get("bounds", {})
    return bool(hit), f"overlays with all 24: {b.get('full_24')} (copies best {b.get('controls_best_hits')}); the planted overlay reading the message: {bool(hit)}"
