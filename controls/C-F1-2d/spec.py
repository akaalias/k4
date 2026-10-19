"""Positive control for F1/2 (issue #73): a long period inside 53-97, 80, on the standard and KRYPTOS tables (0034).
0034 climbed the free key slots toward English at 27-29 and 53-95 (every third) under all 24 conventions and ran
shuffled copies at 27-29, 53, 60, 70, 80, 97. Identification as in C-F1-2b: the planted period scores above the
run's own shuffled copies at that period (the reading cannot be recovered with 56 free slots), by more than any unplanted
period beats its copies in the same run. First judged without that last condition (result.passed-1.json): margin
0.027 at 80 while the unplanted 53 beat its copies by 0.12; re-judged 2026-10-19."""
import random

from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.plants import english_plant

ITEM = "F1/2"
EXPERIMENT = "0034"
WHAT = "Periodic tableau, standard plain and cipher alphabets, KRYPTOS key alphabet, Beaufort, period 80 with a random key, on English from Carter"
P = 80
BUDGET = 3600   # shared machine; 0034 stops its sweep by the clock and needs 300 s left for its copies


def plant():
    rng = random.Random(7319)
    return {"plaintext": english_plant(7319),
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
