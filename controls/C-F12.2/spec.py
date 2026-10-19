"""Positive control for F12.2 (issue #73): K4's statistics against 1,000 shuffles (0168), the I.C. by number of alphabets.
0168 computed 71 statistics fixed before the run (segment tables, the average I.C. for 1-48 alphabets, repeats at
widths 7, 21, 31) and counted as real only a value outside every one of 1,000 letter-preserving shuffles; nothing on
K4 was. Here the text carries the structure the I.C. curve is meant to see, a repeating key of 7 (Stein's own
reading of K1 and K2), so the I.C. at 7 alphabets must stand above every shuffle. The seed was not chosen by
outcome (the first unused one of the block). 0168's encrypt() is a stub, so the plant makes its own ciphertext."""
import random

from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.plants import english_plant

ITEM = "F12.2"
EXPERIMENT = "0168"
WHAT = "Vigenere on the standard table, random key of length 7, on English from Carter: the I.C. at 7 alphabets must stand above all 1,000 shuffles"
L = 7
SEED = 7506


def plant():
    rng = random.Random(SEED)
    k = [rng.randrange(26) for _ in range(L)]
    pt = english_plant(SEED)
    ct = "".join(STD[(STD.index(ch) + k[i % L]) % 26] for i, ch in enumerate(pt))
    return {"plaintext": pt, "key": ("vig std", k), "ciphertext": ct}


def found(result, plant):
    rows = {r["statistic"]: r for r in result.get("bounds", {}).get("all", [])}
    r = rows.get(f"I.C. at {L} alphabets", {})
    ok = bool(r.get("outside_every_shuffle")) and r.get("k4", 0) > r.get("shuffles_max", 1)
    outs = [o["statistic"] for o in result.get("bounds", {}).get("outside_every_shuffle", [])]
    return ok, f"I.C. at {L}: plant {r.get('k4')}, shuffles {r.get('shuffles_min')}-{r.get('shuffles_max')}, p {r.get('p_two_sided')}; outside every shuffle: {outs}"
