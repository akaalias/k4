"""Positive control for F6.9 (issue #73): plaintext autokey before 0084's double columnar routes (0163), the second kind.
0163 tested 3,284,523 routes x lags 1-96 x 2 tables x 3 rules for both autokeys after or before the move, and reported
per kind the survivors with 5+ checks and the most checks any K4 survivor had. Plaintext autokey before the move is
checked only where the key's place is itself known: at lag 5 that is 14 checks, so the planted setting must be the
survivor with 14 checks (chance 26^-14 per setting, about 2e9 settings). The copies reach 0-480 at 5+ checks, so found
reads the most-checks survivor. 0163's encrypt() is a stub, so the plant makes its own ciphertext."""
import random
import sys

from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.plants import english_plant

ITEM = "F6.9"
EXPERIMENT = "0163"
WHAT = "Plaintext autokey at lag 5 on the standard table, Beaufort (c = k - p), random primer; then rows of LANGLEY's width read by its numbering, then rows of 7 read in column order 2 5 0 6 3 1 4, inverse map; on English from Carter"
L = 5
PERM = (2, 5, 0, 6, 3, 1, 4)


def route():
    a = sys.modules["attack"]
    rows = [list(range(97))[i:i + 7] for i in range(0, 97, 7)]
    seq = [r[c] for c in PERM for r in rows if c < len(r)]
    w7, wk = a.where(seq), a.where(a.keyed_columnar(list(range(97)), "LANGLEY"))
    c2 = [w7[wk[i]] for i in range(97)]            # 0163's composition with the second stage first
    inv = [0] * 97
    for i, j in enumerate(c2):
        inv[j] = i
    return inv                                      # and its inverse, as 0163 also tests


def plant():
    rng = random.Random(7464)
    pt = english_plant(7464)
    M = route()
    primer = [rng.randrange(26) for _ in range(L)]
    e = [STD[((primer[i] if i < L else STD.index(pt[i - L])) - STD.index(ch)) % 26] for i, ch in enumerate(pt)]
    c = [None] * 97
    for i, ch in enumerate(e):
        c[M[i]] = ch
    return {"plaintext": pt, "key": ("B plaintext autokey", "lag", L, "standard", "Beaufort", primer, "LANGLEY then", PERM, "inverse"),
            "ciphertext": "".join(c), "checks": 14}


def found(result, plant):
    s = result.get("bounds", {}).get("summary", {}).get("B plaintext autokey", {})
    top = s.get("k4_max_checks_survivor", 0)
    return top == plant["checks"], (f"B plaintext autokey: most checks on a survivor {top} (planted setting {plant['checks']}); "
                                    f">=5 checks {s.get('k4_ge5')} (copies {min(s.get('coppers_ge5') or [0])}-{max(s.get('coppers_ge5') or [0])})")
