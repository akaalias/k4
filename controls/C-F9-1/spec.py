"""Positive control for F9/1 (issue #73): a one-to-one substitution, then a route from 0019's set.
0019 tested 23,931 routes (plain, keyed and double columnar, double rotations, K3's rule, the identity): the known
letters must land on carved letters one substitution table explains. Here the planted double columnar route must be
among the monoalphabetic survivors. 0019 lists only the first 40 survivor routes; on K4 and its copies there were none,
so a cut-off would show as more than 40 survivors (reported in the line)."""
import random

from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.plants import english_plant

ITEM = "F9/1"
EXPERIMENT = "0019"
ROUTE = "double columnar w=13 then w=8"
WHAT = f"Random one-to-one substitution, then {ROUTE} (0019's encrypt), on English from Carter"


def plant():
    rng = random.Random(7630)
    sig = list(STD); rng.shuffle(sig)
    return {"plaintext": english_plant(7630), "key": {"route": ROUTE, "substitution": dict(zip(STD, sig))}}


def found(result, plant):
    b = result.get("bounds", {})
    mono = b.get("monoalphabetic_survivor_routes", [])
    return ROUTE in mono, f"monoalphabetic survivors {b.get('monoalphabetic_survivors')} (shuffled {[n['monoalphabetic'] for n in b.get('shuffled_k4_survivors', [])]}); planted route among them: {ROUTE in mono}"
