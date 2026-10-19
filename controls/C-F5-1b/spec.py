"""Positive control for F5/1 (issue #73): Gromark on the puzzle's alphabets, bases 2-9 (0028).
0028 is 0013's search with bases 2 to 9 (every forced shift must be below the base); same alphabet pool, modes and
two-term rules up to lag 12, survivors extended and submitted. Here a base-8 plant must come back as a submitted
candidate with the planted rule, base and alphabets, decrypting to the planted text. Candidates are cut at 50 in
plain-alphabet order; the plant uses the standard plain alphabet, which comes first."""
import random

from kryptos.alphabets import keyword_mixed
from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.plants import english_plant

ITEM = "F5/1"
EXPERIMENT = "0028"
WHAT = "Gromark base 8, rule k[i]=k[i-5]+k[i-2], random 5-digit primer, plain standard / cipher SHADOW keyword-mixed, Beaufort, on English from Carter"
A, B, BASE = 5, 2, 8


def plant():
    rng = random.Random(7611)
    primer = [rng.randrange(BASE) for _ in range(A)]
    key = {"pa": STD, "ca": keyword_mixed("SHADOW"), "m": "beau", "a": A, "b": B, "base": BASE, "primer": primer}
    return {"plaintext": english_plant(7611), "key": key}


def found(result, plant):
    k = plant["key"]
    hit = [c for c in result.get("candidates", []) if c["key"]["pa"] == k["pa"] and c["key"]["ca"] == k["ca"] and c["key"]["m"] == k["m"]
           and (c["key"]["a"], c["key"]["b"], c["key"]["base"]) == (A, B, BASE) and c["plaintext"] == plant["plaintext"]]
    b = result.get("bounds", {})
    return bool(hit), f"survivors {b.get('n_survivors')}, consistent with the second run {b.get('n_survivors_consistent_with_second_run')}; planted rule, base and alphabets decrypting to the plant: {bool(hit)}"
