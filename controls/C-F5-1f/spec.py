"""Positive control for F5/1 (issue #73): two-term Gromark on a free alphabet in bases 2-9, 11-16 and 26 (0076).
0076 is 0069's exact test in other bases (two-term rules up to lag 5, base 26 up to lag 4, every primer, four forms,
free alphabet), K4 against ten shuffled copies. It reports counts per base only. Here the planted base-12 cell must
have at least one consistent primer and more than every copy. 0076's encrypt() is a stub, so the plant makes its
own ciphertext."""
import random

from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.plants import english_plant

ITEM = "F5/1"
EXPERIMENT = "0076"
WHAT = "Gromark base 12, rule d[i]=d[i-2]+d[i-5], random 5-digit primer, random alphabet, form M[P-d]=c, on English from Carter"
BASE, RULE = 12, (2, 5)


def plant():
    rng = random.Random(7615)
    M = list(STD); rng.shuffle(M)
    d = [rng.randrange(BASE) for _ in range(RULE[1])]
    primer = list(d)
    while len(d) < 97:
        d.append((d[-RULE[0]] + d[-RULE[1]]) % BASE)
    pt = english_plant(7615)
    ct = "".join(M[(STD.index(ch) - d[i]) % 26] for i, ch in enumerate(pt))
    return {"plaintext": pt, "key": ("".join(M), f"base {BASE}", f"rule {RULE}", f"primer {primer}", "M[P-d]=c"), "ciphertext": ct}


def found(result, plant):
    e = result.get("bounds", {}).get("by_base", {}).get(str(BASE), {})
    k, c = e.get("k4", 0), e.get("controls", [])
    return k >= 1 and k > max(c or [0]), f"base {BASE}: consistent primers {k}, copies {c}"
