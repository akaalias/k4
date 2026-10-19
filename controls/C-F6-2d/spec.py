"""Positive control for F6/2 (issue #73): a move, then a Berlin-clock key schedule (0091).
0091 ran 27,000+ distinct routes under 12 conventions and, for a move then a clock schedule read at the carved places,
filtered every start minute of 36 clock families (5 readings x 7 steps, plus the time digits) check by check (no full
match on K4); here the planted reading, step, start, shift, route and convention must reach all 24 checks and come back
as a candidate that reads the planted text. 0091's encrypt() is a stub, so the plant makes its own ciphertext with
0091's own clock_value() and moves."""
import sys

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F6/2"
EXPERIMENT = "0091"
WHAT = "Keyword columnar under SHADOW (forward), then the clock's hour plus minute from 07:17 in 5-minute steps plus 3 read at the carved places, plain KRYPTOS / cipher standard, Vigenere, on English from Carter"
NAME, STEP, T0, C0, WORD = "hour plus minute", 5, 437, 3, "SHADOW"


def plant():
    a = sys.modules["attack"]
    sigma = a.perm_of(lambda s: a.columnar_transposition_encrypt(s, list(a.keyword_sequence(WORD))))
    where = [0] * 97
    for j, i in enumerate(sigma):
        where[i] = j
    pt = english_plant(7410)
    moved = [""] * 97
    for i, j in enumerate(where):
        moved[j] = pt[i]
    ct = "".join(STD[(KRY.index(ch) + a.clock_value(NAME, T0 + STEP * j) + C0) % 26] for j, ch in enumerate(moved))
    return {"plaintext": pt, "key": (f"keyword {WORD}", NAME, STEP, T0, C0, "vig/kry/std", "move then change"), "ciphertext": ct}


def found(result, plant):
    b = result.get("bounds", {}).get("move_then_change", {})
    hit = [c for c in result.get("candidates", []) if c["plaintext"] == plant["plaintext"]
           and c["key"].startswith(f"move then change: clock {NAME} step {STEP} ") and c["key"].endswith("vig/kry/std")]
    return bool(hit), (f"move then change: full matches {b.get('k4_full')}, deepest {b.get('k4_best_depth')}, copies' deepest "
                       f"{b.get('controls_best_depth')}; the planted schedule as a candidate: {bool(hit)}")
