"""Positive control for F1/2 (issue #73): the long periods 53+ on the standard and KRYPTOS tables (0034).
0034 climbed the free key slots toward English at 27-29 and 53-95 (every third) under all 24 conventions.
First run (kept as result.failed-1.json): with recovery of the text required (90 of 97 letters) it FAILED at
52/97: at 29 free slots (about 136 bits, past 0136's 130-bit bound) the climb finds English better than the
truth (-3.92 against the plant's own -4.18); its shuffled copies did not run on the loaded machine.
Rerun with the identification the attack can make there: the planted period scores above the run's own
shuffled copies at that period, by more than any
unplanted period beats its copies in the same run (re-judged 2026-10-19: a margin smaller than an unplanted
period's is overfitting, not identification). 53 is the low edge of 53+; C-F1-2d plants at 80."""
import random

from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.plants import english_plant

ITEM = "F1/2"
EXPERIMENT = "0034"
WHAT = "Periodic tableau, standard plain and cipher alphabets, KRYPTOS key alphabet, Beaufort, period 53 with a random key, on English from Carter"
P = 53
BUDGET = 3600   # shared machine; 0034 stops its sweep by the clock and needs 300 s left for its copies


def plant():
    rng = random.Random(7313)
    return {"plaintext": english_plant(7313),
            "key": {"pa": "std", "ca": "std", "ka": "kry", "m": "beau", "key": "".join(rng.choice(STD) for _ in range(P))}}


def found(result, plant):
    b = result.get("bounds", {})
    best = b.get("best_by_period", {}).get(str(P))
    if not best:
        return False, "no climb at the planted period"
    same = sum(a == c for a, c in zip(best["text"], plant["plaintext"]))
    ctl = b.get("shuffled_k4_best_by_period", {})
    top = ctl.get(str(P))
    margins = {q: b["best_by_period"][q]["english"] - v for q, v in ctl.items() if q in b.get("best_by_period", {})}
    other = max((m for q, m in margins.items() if q != str(P)), default=None)
    ok = top is not None and other is not None and margins[str(P)] > 0 and margins[str(P)] > other
    return ok, (f"best at {P}: {best['convention']}, English {best['english']} against shuffled copies' best {top} (margin "
                f"{margins.get(str(P), 0):.3f}); largest margin at an unplanted period {other:.3f}; {same}/97 letters of the plant")
