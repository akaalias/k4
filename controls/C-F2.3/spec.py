"""Positive control for F2.3 (issue #73): a phrase with repeated letters as the plain strip, so a letter may be
sent from any of its places (homophones that keep the length) (0183).
0183 took 1,196 26-letter phrase windows (K1-K3, the Morse, famous sentences, Carter's book) as the plain strip,
the standard or KRYPTOS order as the cipher strip, two slide forms, and asked which repeating key lengths 1-26 the
known letters leave possible; it counted live cells against 20 shuffled copies and listed the K4 cells by shortest
live length. Here a window drawn from 0183's own list enciphers a message written only in its letters; the planted
cell must be listed live at the planted length, and that length must carry more live cells than every copy. The
message is Carter's narrative with the letters the phrase lacks dropped, then the known words written in. 0183's
encrypt() is a stub; the plant uses 0183's own encipher()."""
import random
import sys

from kryptos.facts import KNOWN
from kryptos.plants import _letters

ITEM = "F2.3"
EXPERIMENT = "0183"
WHAT = "A 26-letter window of 0183's phrase list (drawn by seed) as the plain strip, standard cipher strip, form k-j, a random homophone at each letter, repeating key of length 11 with random shifts, on Carter's narrative in the phrase's letters"
L, STRIP, FORM = 11, "std", "k-j"


def plant():
    a = sys.modules["attack"]
    rng = random.Random(7557)
    PH = a.phrases()
    ph = sorted(PH)[rng.randrange(len(PH))]
    src = "".join(c for c in _letters() if c in set(ph))
    o = rng.randrange(len(src) - 97)
    p = list(src[o:o + 97])
    for q, ch in KNOWN.items():
        p[q - 1] = ch
    pt = "".join(p)
    key = [rng.randrange(26) for _ in range(L)]
    ct = a.encipher(pt, ph, STRIP, FORM, key, rng)
    return {"plaintext": pt, "key": (ph, PH[ph], STRIP, FORM, key), "ciphertext": ct, "phrase": ph}


def found(result, plant):
    b = result.get("bounds", {})
    cell = [z for z in b.get("k4_live_shortest", []) if z["phrase"] == plant["phrase"] and z["strip"] == STRIP and z["form"] == FORM]
    live = bool(cell) and L in cell[0]["lengths"]
    v = b.get("per_length", {}).get(L, {})
    above = v.get("k4", 0) > v.get("copies_max", 0)
    return live and above, (f"planted cell listed: {bool(cell)}, lengths {cell[0]['lengths'] if cell else None}; length {L}: "
                            f"live {v.get('k4')} (copies {v.get('copies_min')}-{v.get('copies_max')})")
