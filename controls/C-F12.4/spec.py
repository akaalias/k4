"""Positive control for F12.4 (issue #73): the pencil session's six by-eye patterns against 1,000 shuffles (0170).
0170 noted six patterns in K4 by eye and kept as real only one beyond every one of 1,000 letter-preserving
shuffles; none was. Observation (4), repeated-bigram spacings divisible by 4, is Kasiski's sign of a key of 4. Here
the text is enciphered with a repeating key of 4, so observation (4) must stand above every shuffle. The seed was not
chosen by outcome. 0170's encrypt() is a stub, so the plant makes its own ciphertext."""
import random

from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.plants import english_plant

ITEM = "F12.4"
EXPERIMENT = "0170"
WHAT = ("Vigenere on the standard table, random key of length 4, on English from Carter: observation (4), repeated-bigram "
        "spacings divisible by 4, must stand above all 1,000 shuffles")
SEED = 7510
OBS = "(4) repeated-bigram spacings divisible by 4"


def plant():
    rng = random.Random(SEED)
    k = [rng.randrange(26) for _ in range(4)]
    pt = english_plant(SEED)
    return {"plaintext": pt, "key": ("vig std", k), "ciphertext": "".join(STD[(STD.index(ch) + k[i % 4]) % 26] for i, ch in enumerate(pt))}


def found(result, plant):
    rows = {r["observation"]: r for r in result.get("bounds", {}).get("observations", [])}
    r = rows.get(OBS, {})
    ok = bool(r.get("outside_every_shuffle")) and r.get("k4", 0) > r.get("shuffles_max", 1e9)
    outs = [o["observation"] for o in result.get("bounds", {}).get("outside_every_shuffle", [])]
    return ok, f"{OBS}: plant {r.get('k4')}, shuffles {r.get('shuffles_min')}-{r.get('shuffles_max')}, p {r.get('p_one_sided')}; outside every shuffle: {outs}"
