"""Positive control for F5/1 (issue #73): Gromark on alphabets from the K1-K3 words, bases up to 15 (0054).
0054 builds keyword alphabets from every word of the solved messages and Sanborn's 2025 letter (those the vocabulary
had not built), finds the smallest base each (plain, cipher, mode) triple admits from the 24 forced shifts, and for
triples admissible at base 15 or less checks every two-term rule k[i] = k[i-a] + k[i-b] (a up to 13) in each base
up to 15. It reports counts only: the smallest admissible base on K4 and on ten shuffled copies, the number of
admissible triples and of consistent rules. Here the plant's smallest admissible base must be at most its base 12
and below every copy's, and at least one rule must be consistent (the planted one cannot be named from the counts)."""
import random

from kryptos.alphabets import keyword_mixed
from kryptos.facts import KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F5/1"
EXPERIMENT = "0054"
WHAT = "Gromark base 12, rule k[i]=k[i-6]+k[i-4], random 6-digit primer, plain SHADING keyword-mixed / cipher KRYPTOS, Vigenere, on English from Carter"
A, B, BASE = 6, 4, 12


def plant():
    rng = random.Random(7613)
    k = [rng.randrange(BASE) for _ in range(A)]
    while len(k) < 97:
        k.append((k[-A] + k[-B]) % BASE)
    key = {"pa": keyword_mixed("SHADING"), "ca": KRY, "m": "vig", "key": k}
    return {"plaintext": english_plant(7613), "key": key}


def found(result, plant):
    b = result.get("bounds", {})
    best, ctl = b.get("smallest_admissible_base_k4", 99), b.get("smallest_admissible_base_controls", [])
    ok = best <= BASE and best < min(ctl or [0]) and b.get("pairs_admissible_at_15_or_less", 0) >= 1 and b.get("rules_consistent", 0) >= 1
    return ok, f"smallest admissible base {best} (copies {sorted(ctl)}); triples admissible at 15 or less {b.get('pairs_admissible_at_15_or_less')}; consistent rules {b.get('rules_consistent')}"
