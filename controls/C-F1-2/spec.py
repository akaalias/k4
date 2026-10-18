"""Positive control for F1/2 (issue #73): periods 27-29 on alphabet pairs keyword-mixed from the vocabulary.
0048 climbed the free key slots toward English for every pair, period and mode; here the climb at the planted
period must return the planted text and score it above the run's own shuffled copy."""
import random

from kryptos.alphabets import keyword_mixed
from kryptos.plants import english_plant

ITEM = "F1/2"
EXPERIMENT = "0048"
WHAT = "Periodic tableau, plain alphabet SHADOW-mixed, cipher alphabet LODESTONE-mixed, Vigenere, period 28 with random shifts, on English from Carter"
P = 28
BUDGET = 3600   # the machine is shared; the sweep stops by the clock, so give it the wall time it had on K4


def plant():
    rng = random.Random(7312)
    return {"plaintext": english_plant(7312),
            "key": {"pa": keyword_mixed("SHADOW"), "ca": keyword_mixed("LODESTONE"), "m": "vig", "key": [rng.randrange(26) for _ in range(P)]}}


def found(result, plant):
    b = result.get("bounds", {})
    best = b.get("best_by_period", {}).get(str(P))
    if not best:
        return False, "no climb at the planted period"
    same = sum(a == c for a, c in zip(best["text"], plant["plaintext"]))
    ctl = b.get("shuffled_k4_best_by_period", {})
    top = max(ctl.values()) if ctl else None
    ok = same >= 95 and top is not None and best["english"] > top
    return ok, f"best at {P}: {best['plain']}/{best['cipher']}/{best['mode']}, {same}/97 letters of the plant, English {best['english']} against shuffled copy best {top}"
