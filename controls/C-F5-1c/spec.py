"""Positive control for F5/1 (issue #73): two- and three-term Gromark on the puzzle's alphabets, bases 16-26 (0046).
0046 is 0013's search with three-term rules k[i] = k[i-a] + k[i-b] + k[i-c] added (lags up to 13) and bases 16-26
as each alphabet triple allows. Here a base-20 three-term plant must come back as a submitted candidate with the
planted rule, base and alphabets, decrypting to the planted text. Candidates are cut at 50 in plain-alphabet order;
the plant uses the standard plain alphabet, which comes first."""
import random

from kryptos.alphabets import keyword_mixed
from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.plants import english_plant

ITEM = "F5/1"
EXPERIMENT = "0046"
WHAT = "Gromark base 20, rule k[i]=k[i-9]+k[i-5]+k[i-2], random 9-digit primer, plain standard / cipher BERLIN keyword-mixed, variant Beaufort, on English from Carter"
RULE, BASE = [9, 5, 2], 20


def plant():
    rng = random.Random(7612)
    primer = [rng.randrange(BASE) for _ in range(RULE[0])]
    key = {"pa": STD, "ca": keyword_mixed("BERLIN"), "m": "varbeau", "rule": RULE, "base": BASE, "primer": primer}
    return {"plaintext": english_plant(7612), "key": key}


def found(result, plant):
    k = plant["key"]
    hit = [c for c in result.get("candidates", []) if c["key"]["pa"] == k["pa"] and c["key"]["ca"] == k["ca"] and c["key"]["m"] == k["m"]
           and list(c["key"]["rule"]) == RULE and c["key"]["base"] == BASE and c["plaintext"] == plant["plaintext"]]
    b = result.get("bounds", {})
    return bool(hit), f"survivors {b.get('n_survivors')}, consistent with the second run {b.get('n_survivors_consistent_with_second_run')}; planted rule, base and alphabets decrypting to the plant: {bool(hit)}"
