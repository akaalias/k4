"""Positive control for F1.6 (issue #73): one carved letter wrong, through trifid (0151).
0151 ran 0040's exact trifid solver (periods 2-15, every offset, a free 27-symbol cube) on all 5,044 single-letter
variants of the copper; K4 gave no consistent cube. Here a trifid text is planted with 0040's own encrypt (period
7, offset 0) and one carved letter at a known place miscut; the restoring variant must give a consistent cube.
0151's encrypt() is a stub; the plant uses 0040's."""
import importlib.util
import random

from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.plants import english_plant

ITEM = "F1.6"
EXPERIMENT = "0151"
WHAT = "Trifid, random cube of the 26 letters and ?, period 7, offset 0 (0040's encrypt), then the carved letter at place 28 miscut, on English from Carter"
PLACE = 28


def plant():
    spec = importlib.util.spec_from_file_location("m040p", "experiments/0040-trifid-free-cubes-by-constraint-propagation-rerun/attack.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    pt = english_plant(7374)
    rng = random.Random(7374)
    while True:
        cube = list(m.SYMBOLS); rng.shuffle(cube); cube = "".join(cube)
        ct = m.encrypt(pt, {"cube": cube, "period": 7, "offset": 0})
        if "?" not in ct:
            break
    ct = list(ct)
    true = ct[PLACE - 1]
    ct[PLACE - 1] = STD[(STD.index(true) + 5) % 26]
    return {"plaintext": pt, "key": (cube, 7, 0, f"place {PLACE} miscut"), "ciphertext": "".join(ct), "true": true}


def found(result, plant):
    b = result.get("bounds", {})
    want = f"sub {PLACE} {plant['ciphertext'][PLACE - 1]}->{plant['true']}"
    hit = [t for t in b.get("trifid_consistent", []) if t["variant"] == want and t["period"] == 7 and t["offset"] == 0]
    return bool(hit), f"trifid consistent {b.get('n_trifid_consistent')}; '{want}' at period 7: {bool(hit)}"
