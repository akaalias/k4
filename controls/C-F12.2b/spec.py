"""Positive control for F12.2 (issue #73): K4's statistics against 1,000 shuffles (0168), the segment tables.
0168's segment statistics (chi-square of the segment-by-letter table for 8 fixed cuttings) are meant to see a text
whose parts use different keys (the break F12.5 would split at). Here the two halves (1-48, 49-97) are each a
simple shift of English by a different amount, so the cutting at 48/49 must stand above every shuffle. The seed was
not chosen by outcome. 0168's encrypt() is a stub, so the plant makes its own ciphertext."""
import random

from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.plants import english_plant

ITEM = "F12.2"
EXPERIMENT = "0168"
WHAT = ("Places 1-48 and 49-97 each shifted by its own random amount on the standard table (two Caesar keys), on English "
        "from Carter: the segment table for halves at 48/49 must stand above all 1,000 shuffles")
SEED = 7507
STAT = "segments: halves at 48/49"


def plant():
    rng = random.Random(SEED)
    s1 = rng.randrange(26)
    s2 = (s1 + rng.randrange(1, 26)) % 26
    pt = english_plant(SEED)
    ct = "".join(STD[(STD.index(ch) + (s1 if i < 48 else s2)) % 26] for i, ch in enumerate(pt))
    return {"plaintext": pt, "key": ("shift 1-48", s1, "shift 49-97", s2), "ciphertext": ct}


def found(result, plant):
    rows = {r["statistic"]: r for r in result.get("bounds", {}).get("all", [])}
    r = rows.get(STAT, {})
    ok = bool(r.get("outside_every_shuffle")) and r.get("k4", 0) > r.get("shuffles_max", 1e9)
    outs = [o["statistic"] for o in result.get("bounds", {}).get("outside_every_shuffle", [])]
    return ok, f"{STAT}: plant {r.get('k4')}, shuffles {r.get('shuffles_min')}-{r.get('shuffles_max')}, p {r.get('p_two_sided')}; outside every shuffle: {outs}"
