"""Positive control for F12.4 (issue #73): the pencil session's six by-eye patterns against 1,000 shuffles (0170).
Observation (3), the number of repeated bigrams, sees letter order that shuffling destroys (a language's common
pairs). Here the text is English under one random mixed alphabet (simple substitution keeps every bigram repeat), so
observation (3) must stand above every shuffle. The seed was not chosen by outcome. 0170's encrypt() is a stub, so
the plant makes its own ciphertext."""
import random

from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.plants import english_plant

ITEM = "F12.4"
EXPERIMENT = "0170"
WHAT = ("Simple substitution, one random mixed alphabet, on English from Carter: observation (3), repeated bigrams, must "
        "stand above all 1,000 shuffles")
SEED = 7511
OBS = "(3) repeated bigrams"


def plant():
    rng = random.Random(SEED)
    x = list(STD); rng.shuffle(x)
    pt = english_plant(SEED)
    return {"plaintext": pt, "key": ("simple substitution", "".join(x)), "ciphertext": "".join(x[STD.index(ch)] for ch in pt)}


def found(result, plant):
    rows = {r["observation"]: r for r in result.get("bounds", {}).get("observations", [])}
    r = rows.get(OBS, {})
    ok = bool(r.get("outside_every_shuffle")) and r.get("k4", 0) > r.get("shuffles_max", 1e9)
    outs = [o["observation"] for o in result.get("bounds", {}).get("outside_every_shuffle", [])]
    return ok, f"{OBS}: plant {r.get('k4')}, shuffles {r.get('shuffles_min')}-{r.get('shuffles_max')}, p {r.get('p_one_sided')}; outside every shuffle: {outs}"
