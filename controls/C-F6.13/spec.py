"""Positive control for F6.13 (issue #73): Chiffre XIII's five-row mask, then its period-5 shifted mixed alphabet (0166).
0166 built every mask (rows 2 and 4 at every split, row 4 at every cyclic shift) for 6,296 keys of 24-31 letters
(2,248,512 masks) and decided the published substitution on one unknown alphabet exactly, both shift directions; on K4
and every copy no mask was consistent with 3+ checks. The planted mask must be listed in k4_top (masks with 6+ checks,
the 20 with most checks) with its key, row lengths, shift and direction, and the K4 count with 4+ checks must exceed
every copy's. 0166's encrypt() is a stub, so the plant makes its own ciphertext."""
import random
import sys

from kryptos.facts import KNOWN, STANDARD_ALPHABET as STD
from kryptos.plants import english_plant

ITEM = "F6.13"
EXPERIMENT = "0166"
WHAT = "Chiffre XIII mask under the 27-letter K2 window IEDOUTTHERESOMEWHEREXWHOKNO, row 2 of 6 letters, row 4 of 10 at shift 11, then plain A-Z over a random mixed alphabet, rows shifted +1 by carved place mod 5, on English from Carter"
KEY, L2, S4, SIGN = "IEDOUTTHERESOMEWHEREXWHOKNO", 6, 11, 1


def wheremap():
    a = sys.modules["attack"]
    return a.where(a.xiii(KEY, L2, S4))


def plant():
    rng = random.Random(7461)
    pt = english_plant(7461)
    X = list(STD); rng.shuffle(X)
    wh = wheremap()
    y = [None] * 97
    for i, ch in enumerate(pt):
        y[wh[i]] = ch
    ct = "".join(X[(STD.index(y[j]) + SIGN * (j % 5)) % 26] for j in range(97))
    cells = {(STD.index(KNOWN[q]) + SIGN * (wh[q - 1] % 5)) % 26 for q in KNOWN}
    return {"plaintext": pt, "key": (KEY, L2, S4, SIGN, "".join(X)), "ciphertext": ct, "checks": 24 - len(cells)}


def found(result, plant):
    r = result.get("bounds", {}).get("items", {}).get("F6.13 Chiffre XIII", {})
    hit = [x for x in r.get("k4_top", []) if (x.get("key"), x.get("row2"), x.get("shift4"), x.get("sign")) == (KEY, L2, S4, SIGN)]
    g = r.get("consistent_ge", {}).get("4", {})
    above = g.get("k4", 0) > max(g.get("coppers") or [0])
    return bool(hit) and above, (f"planted mask listed: {hit[0] if hit else None} (expected {plant['checks']} checks); "
                                 f"consistent with 4+ checks K4 {g.get('k4')}, copies {min(g.get('coppers') or [0])}-{max(g.get('coppers') or [0])}")
