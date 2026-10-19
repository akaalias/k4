"""Positive control for F5/1 (issue #73): Gromark on the puzzle's alphabets, base 10 (0013).
0013 computed the 24 forced shifts for every plain alphabet, cipher alphabet and tableau mode drawn from the
standard, KRYPTOS and the four mixings of every vocabulary word, and checked every two-term rule
k[i] = k[i-a] + k[i-b] (1 <= b < a <= 12) in bases 10 and 26 on both crib runs; a survivor is extended to a full
stream and its decryption submitted. Here the planted rule, base and alphabet pair must come back as a submitted
candidate whose decryption is the planted text. Candidates are cut at 50 in plain-alphabet order; the plant uses
the standard plain alphabet, which comes first, so it cannot be cut off by later survivors."""
import random

from kryptos.alphabets import keyword_mixed
from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.plants import english_plant

ITEM = "F5/1"
EXPERIMENT = "0013"
WHAT = "Gromark base 10, rule k[i]=k[i-7]+k[i-3], random 7-digit primer, plain standard / cipher PALIMPSEST keyword-mixed, Vigenere, on English from Carter"
A, B, BASE = 7, 3, 10


def plant():
    rng = random.Random(7610)
    primer = [rng.randrange(BASE) for _ in range(A)]
    key = {"pa": STD, "ca": keyword_mixed("PALIMPSEST"), "m": "vig", "a": A, "b": B, "base": BASE, "primer": primer}
    return {"plaintext": english_plant(7610), "key": key}


def found(result, plant):
    k = plant["key"]
    hit = [c for c in result.get("candidates", []) if c["key"]["pa"] == k["pa"] and c["key"]["ca"] == k["ca"] and c["key"]["m"] == k["m"]
           and (c["key"]["a"], c["key"]["b"], c["key"]["base"]) == (A, B, BASE) and c["plaintext"] == plant["plaintext"]]
    b = result.get("bounds", {})
    return bool(hit), f"survivors {b.get('n_survivors')}, consistent with the second run {b.get('n_survivors_consistent_with_second_run')}; planted rule, base and alphabets decrypting to the plant: {bool(hit)}"
