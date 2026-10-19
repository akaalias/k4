"""Positive control for F4/1 (issue #73): trifid with a free cube, periods 2-15 (0040).
0040 solved every period 2-15 at every alignment for all 27-symbol cubes consistent with the known letters
(constraint propagation and backtracking), decrypted K4 with each and kept the best English per setting as
candidates; 0040's verdict is that no setting admits a cube on K4, so here the planted setting must admit cubes.
Whether a candidate reads the planted message is reported, not required: a live setting can hold more than the
solution cap (5,000) of cubes, and the true one need not be among those kept.
The cube is redrawn until the ciphertext carries no ?, which a carved text could not."""
import random
import sys

from kryptos.plants import english_plant

ITEM = "F4/1"
EXPERIMENT = "0040"
WHAT = "Trifid with a random cube of the 26 letters and ?, period 11, blocks from offset 4 (0040's encrypt), on English from Carter"
P, O = 11, 4


def plant():
    a = sys.modules["attack"]
    rng = random.Random(7558)
    pt = english_plant(7558)
    while True:
        cube = list(a.SYMBOLS); rng.shuffle(cube); cube = "".join(cube)
        if "?" not in a.trifid(pt, cube, P, O, False):
            return {"plaintext": pt, "key": {"cube": cube, "period": P, "offset": O}}


def found(result, plant):
    b = result.get("bounds", {})
    row = [r for r in b.get("per_setting", []) if r["period"] == P and r["offset"] == O]
    hit = [c for c in result.get("candidates", []) if c["key"]["period"] == P and c["key"]["offset"] == O and c["plaintext"] == plant["plaintext"]]
    return bool(row) and row[0]["cubes"] > 0, (f"settings with cubes {b.get('settings_with_cubes')}; at period {P} offset {O}: "
                       f"{row[0]['cubes'] if row else None} cubes; candidate reading the planted message: {bool(hit)}")
