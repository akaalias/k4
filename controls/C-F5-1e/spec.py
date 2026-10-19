"""Positive control for F5/1 (issue #73): base-10 Gromark on a free alphabet (0069).
0069 enumerates every primer of every two-term rule d[i] = d[i-a] + d[i-b] mod 10 (1 <= a < b <= 6) and checks the
24 known letters for a one-to-one mixed alphabet in four forms, K4 against ten shuffled copies. Here the planted
rule, primer and form must be listed among the consistent settings (the list keeps the first 20; on K4 and the
copies nothing is consistent, so the planted one is not crowded out). 0069's encrypt() is a stub, so the plant
makes its own ciphertext."""
import random

from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.plants import english_plant

ITEM = "F5/1"
EXPERIMENT = "0069"
WHAT = "Gromark base 10, rule d[i]=d[i-3]+d[i-5], random 5-digit primer, random alphabet, form M[P+d]=c, on English from Carter"
RULE = (3, 5)


def plant():
    rng = random.Random(7614)
    M = list(STD); rng.shuffle(M)
    d = [rng.randrange(10) for _ in range(RULE[1])]
    primer = "".join(map(str, d))
    while len(d) < 97:
        d.append((d[-RULE[0]] + d[-RULE[1]]) % 10)
    pt = english_plant(7614)
    ct = "".join(M[(STD.index(ch) + d[i]) % 26] for i, ch in enumerate(pt))
    return {"plaintext": pt, "key": ("".join(M), f"rule {RULE}", f"primer {primer}", "M[P+d]=c"), "ciphertext": ct, "primer": primer}


def found(result, plant):
    b = result.get("bounds", {})
    hit = [h for h in b.get("k4_consistent", []) if list(h["rule"]) == list(RULE) and h["primer"] == plant["primer"] and h["form"] == "M[P+d]=c"]
    return bool(hit), f"consistent primers {b.get('k4_count')} (copies {b.get('control_counts')}); planted rule {RULE}, primer {plant['primer']}, M[P+d]=c listed: {bool(hit)}"
