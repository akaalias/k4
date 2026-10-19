"""Positive control for F4.2 (issue #73): trifid with a free cube at periods above 15 (0185).
0185 solved every period 16-97 at every alignment (4,633 settings) for all consistent 27-symbol cubes and kept the
best English per setting as candidates. 0185's own plant (period 30, offset 5) went straight to solve_setting at the
known setting, not through the sweep, so it is not cited; here the planted text goes through the whole sweep, and
the planted setting must admit cubes (0185's verdict is that no setting does on K4). Whether a candidate reads the
planted message is reported, not required: a live setting can hold more than the solution cap (5,000) of cubes.
The cube is redrawn until the ciphertext carries no ?."""
import random
import sys

from kryptos.plants import english_plant

ITEM = "F4.2"
EXPERIMENT = "0185"
WHAT = "Trifid with a random cube of the 26 letters and ?, period 23, blocks from offset 9 (0185's encrypt), on English from Carter"
P, O = 23, 9


def plant():
    a = sys.modules["attack"]
    rng = random.Random(7562)
    pt = english_plant(7562)
    while True:
        cube = list(a.SYMBOLS); rng.shuffle(cube); cube = "".join(cube)
        if "?" not in a.trifid(pt, cube, P, O, False):
            return {"plaintext": pt, "key": {"cube": cube, "period": P, "offset": O}}


def found(result, plant):
    b = result.get("bounds", {})
    row = [r for r in b.get("k4_settings_with_cubes", []) if r["period"] == P and r["offset"] == O]
    hit = [c for c in result.get("candidates", []) if c["key"]["period"] == P and c["key"]["offset"] == O and c["plaintext"] == plant["plaintext"]]
    return bool(row) and row[0]["cubes"] > 0, (f"settings with cubes {b.get('settings_with_cubes')} (copies {[c['with_cubes'] for c in b.get('controls', [])]}); "
                       f"at period {P} offset {O}: {row[0]['cubes'] if row else None} cubes; candidate reading the planted message: {bool(hit)}")
