"""Positive control for F1.6 (issue #73): one carved letter wrong, through free-alphabet Gromark (0150).
0150 ran 0069's, 0076's and 0107's exact deciders (every rule, base and primer, four forms, a free alphabet) on
604 one-letter variants of the copper. Here a base-10 Gromark text (rule d[i] = d[i-1] + d[i-5], 0069's space) is
planted and one carved letter at a known place miscut; the variant that restores it must fit under the planted
rule. 0150's encrypt() is a stub, so the plant makes its own ciphertext."""
import random

from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.plants import english_plant

ITEM = "F1.6"
EXPERIMENT = "0150"
WHAT = "Gromark base 10, rule d[i]=d[i-1]+d[i-5], primer 38576, random alphabet, form M[P+d]=c, then the carved letter at place 66 miscut, on English from Carter"
PLACE = 66


def plant():
    rng = random.Random(7372)
    M = list(STD); rng.shuffle(M)
    d = [3, 8, 5, 7, 6]
    while len(d) < 97:
        d.append((d[-1] + d[-5]) % 10)
    pt = english_plant(7372)
    ct = [M[(STD.index(ch) + d[i]) % 26] for i, ch in enumerate(pt)]
    true = ct[PLACE - 1]
    ct[PLACE - 1] = STD[(STD.index(true) + 11) % 26]
    return {"plaintext": pt, "key": ("".join(M), "rule (1,5)", "primer 38576", "M[P+d]=c", f"place {PLACE} miscut"), "ciphertext": "".join(ct), "true": true}


def found(result, plant):
    b = result.get("bounds", {})
    want = f"sub {PLACE} {plant['ciphertext'][PLACE - 1]}->{plant['true']}"
    hit = [f for f in b.get("fits", []) if f["source"] == "0069" and list(f["setting"]) == [1, 5] and any(v[0] == want for v in f["variants"])]
    return bool(hit), f"settings with a fitting variant {b.get('n_settings_with_fit')}; rule (1,5) restored by '{want}': {bool(hit)}"
