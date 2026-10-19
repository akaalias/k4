"""Positive control for F6/2 (issue #73): a move, then plaintext autokey (0081).
0081 joined 27,752 routes (K3's rule, quarter turns, two clockwise turns, columnar, keyed columnar) to plaintext or
ciphertext autokey at lags 1-96 on one alphabet, both orders, and listed K4's settings with 4+ chain checks (4, at the
copies' rate); here the planted route, plaintext autokey after the move (order A), KRYPTOS Vigenere, lag 12 must be
listed with all its checks passing, and its check level must stand above every shuffled copy. The list holds the first
40 settings; K4 had 4. 0081's encrypt() is a stub, so the plant makes its own ciphertext with 0081's own move() and
ptak_encrypt().
First judged (result.failed-1.json) with the wrong keys into 0081's counts ("plaintext autokey order A", integer levels;
0081 writes "ptak order A" and string levels): the plant was listed with 12 checks but its cell read as 0.
Rerun 2026-10-19 with the keys fixed (levels read as int in the run, str in JSON)."""
import random
import sys

from kryptos.facts import KNOWN
from kryptos.plants import english_plant

ITEM = "F6/2"
EXPERIMENT = "0081"
WHAT = "Two clockwise quarter turns in rows of 8 then 11 (forward), then plaintext autokey at lag 12 with a random primer on the KRYPTOS table, Vigenere, on English from Carter"
SPEC, LAG = {"kind": "turn2", "w1": 8, "w2": 11, "dir": "fwd"}, 12


def checks(where):
    land = [where[p - 1] for p in sorted(KNOWN)]
    return 24 - len({j % LAG for j in land})


def plant():
    a = sys.modules["attack"]
    rng = random.Random(7407)
    primer = "".join(rng.choice(a.KRY) for _ in range(LAG))
    pt = english_plant(7407)
    ct = a.ptak_encrypt(a.move(SPEC, pt), primer, LAG, "kry", "vig")
    return {"plaintext": pt, "key": (SPEC, "plaintext autokey after the move", "kry vig", LAG, primer), "ciphertext": ct,
            "where": a.where_of(SPEC)}


def _lv(d, c, default):
    """0081's count tables are keyed by int in the run and by str once written to JSON."""
    return d.get(c, d.get(str(c), default))


def found(result, plant):
    a = sys.modules["attack"]
    b = result.get("bounds", {})
    c = checks(plant["where"])
    hit = [h for h in b.get("k4_settings_with_4_plus_checks", []) if h["kind"] == "plaintext autokey" and h["order"] == "A"
           and h["alphabet"] == "kry" and h["mode"] == "vig" and h["lag"] == LAG and h["checks"] == c
           and a.where_of(h["route"]) == plant["where"]]
    s = b.get("by_kind_and_order", {}).get("ptak order A", {})
    lvl = min(c, 6)
    n, mx = _lv(s.get("k4_at_least_c", {}), lvl, 0), max(_lv(s.get("controls_at_least_c", {}), lvl, [0]))
    return bool(hit) and n > mx, (f"K4 settings with 4+ checks {b.get('n_k4_4_plus')}; the planted route at lag {LAG} with {c} checks: {bool(hit)}; "
                                  f"plaintext autokey A at {lvl}+ checks: plant {n}, copies' max {mx}")
