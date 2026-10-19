"""Positive control for F6/2 (issue #73): ciphertext autokey, then a move (0081, the ciphertext-autokey path).
0081 joined 27,752 routes to plaintext or ciphertext autokey at lags 1-96 on one alphabet, both orders, and listed K4's
settings with 4+ checks (4, at the copies' rate); here a ciphertext autokey before the move (order B), standard table,
Beaufort, lag 5 (all 24 known places checked) must be listed for the planted route, above every shuffled copy at the
top level counted (6+). The list holds the first 40 settings; K4 had 4. 0081's encrypt() is a stub, so the plant makes
its own ciphertext with 0081's own move().
The keys into 0081's counts were fixed before the first run ("ctak order B"; levels int in the run, str in JSON), after C-F6-2's
first judgement read them wrongly."""
import random
import sys

from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.plants import english_plant

ITEM = "F6/2"
EXPERIMENT = "0081"
WHAT = "Ciphertext autokey at lag 5 with a random primer on the standard table, Beaufort, then keyed columnar under KRYPTOS (forward), on English from Carter"
SPEC, LAG = {"kind": "keyed", "word": "KRYPTOS", "dir": "fwd"}, 5


def plant():
    a = sys.modules["attack"]
    rng = random.Random(7408)
    pt = english_plant(7408)
    x = [rng.randrange(26) for _ in range(LAG)]
    x = [STD[(x[i] - STD.index(pt[i])) % 26] for i in range(LAG)]          # primer letters stand in for the first key
    for i in range(LAG, 97):
        x.append(STD[(STD.index(x[i - LAG]) - STD.index(pt[i])) % 26])    # Beaufort: X[i] = X[i-L] - P[i]
    ct = a.move(SPEC, "".join(x))
    return {"plaintext": pt, "key": (SPEC, "ciphertext autokey before the move", "std beau", LAG), "ciphertext": ct,
            "where": a.where_of(SPEC)}


def _lv(d, c, default):
    """0081's count tables are keyed by int in the run and by str once written to JSON."""
    return d.get(c, d.get(str(c), default))


def found(result, plant):
    a = sys.modules["attack"]
    b = result.get("bounds", {})
    hit = [h for h in b.get("k4_settings_with_4_plus_checks", []) if h["kind"] == "ciphertext autokey" and h["order"] == "B"
           and h["alphabet"] == "std" and h["mode"] == "beau" and h["lag"] == LAG and h["checks"] == 24
           and a.where_of(h["route"]) == plant["where"]]
    s = b.get("by_kind_and_order", {}).get("ctak order B", {})
    n, mx = _lv(s.get("k4_at_least_c", {}), 6, 0), max(_lv(s.get("controls_at_least_c", {}), 6, [0]))
    return bool(hit) and n > mx, (f"K4 settings with 4+ checks {b.get('n_k4_4_plus')}; the planted route at lag {LAG} with 24 checks: {bool(hit)}; "
                                  f"ciphertext autokey B at 6+ checks: plant {n}, copies' max {mx}")
