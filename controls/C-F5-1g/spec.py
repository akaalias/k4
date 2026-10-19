"""Positive control for F5/1 (issue #73): three-term base-10 Gromark on a free alphabet (0107).
0107 enumerates every primer of every rule d[i] = d[i-a] + d[i-b] + d[i-c] mod 10 (1 <= a < b < c <= 6) with 0069's
exact free-alphabet test in four forms, K4 against ten shuffled copies. Its own plant_check feeds one primer to the
tester directly, not through the enumeration, so it is not an own plant. Here the planted rule, primer and form must
be listed among the consistent settings (first 20 kept; nothing is consistent on K4 or the copies). 0107's encrypt()
is a stub, so the plant makes its own ciphertext."""
import random

from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.plants import english_plant

ITEM = "F5/1"
EXPERIMENT = "0107"
WHAT = "Three-term Gromark base 10, rule d[i]=d[i-2]+d[i-3]+d[i-5], random 5-digit primer, random alphabet, form M[C+d]=p, on English from Carter"
RULE = (2, 3, 5)


def plant():
    rng = random.Random(7616)
    M = list(STD); rng.shuffle(M)
    d = [rng.randrange(10) for _ in range(RULE[2])]
    primer = "".join(map(str, d))
    while len(d) < 97:
        d.append(sum(d[-lag] for lag in RULE) % 10)
    pt = english_plant(7616)
    # form M[C+d]=p: the plaintext letter sits at slot (C + d) of M, so C = M.index(p) - d in the standard order
    ct = "".join(STD[(M.index(ch) - d[i]) % 26] for i, ch in enumerate(pt))
    return {"plaintext": pt, "key": ("".join(M), f"rule {RULE}", f"primer {primer}", "M[C+d]=p"), "ciphertext": ct, "primer": primer}


def found(result, plant):
    b = result.get("bounds", {})
    hit = [h for h in b.get("k4_consistent", []) if list(h["rule"]) == list(RULE) and h["primer"] == plant["primer"] and h["form"] == "M[C+d]=p"]
    return bool(hit), f"consistent primers {b.get('k4_count')} (copies {b.get('control_counts')}); planted rule {RULE}, primer {plant['primer']}, M[C+d]=p listed: {bool(hit)}"
