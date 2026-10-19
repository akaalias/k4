"""Positive control for F6.9 (issue #73): ciphertext autokey after 0084's double columnar routes (0163).
0163 tested 3,284,523 routes (a width-7 stage in all 5,040 orders with a second columnar stage) x lags 1-96 x 2 tables
x 3 rules for ciphertext and plaintext autokey after or before the move, and reported per kind the survivors with 5+
checks and the most checks any K4 survivor had. The planted setting must survive with all its checks (22 here); by
chance a setting survives c checks at 26^-c, so with about 2e9 settings nothing else comes near. 0163's ">=5 checks"
count cannot lift one setting above the copies' 0-8, so found reads the most-checks survivor. 0163's encrypt() is a
stub, so the plant makes its own ciphertext."""
import random
import sys

from kryptos.facts import KNOWN, KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F6.9"
EXPERIMENT = "0163"
WHAT = "Rows of 7 read in column order 4 0 6 2 5 1 3, then rows of 12 read down; then ciphertext autokey at lag 8 on the KRYPTOS table, c = p + k, random primer; on English from Carter"
L = 8
PERM = (4, 0, 6, 2, 5, 1, 3)


def route():
    a = sys.modules["attack"]
    rows = [list(range(97))[i:i + 7] for i in range(0, 97, 7)]
    seq = [r[c] for c in PERM for r in rows if c < len(r)]
    w7, w12 = a.where(seq), a.where(a.stage(list(range(97)), 12, "col"))
    return [w12[w7[i]] for i in range(97)]          # 0163's composition, width-7 stage first, forward


def checks(M):
    return sum(1 for q in KNOWN if M[q - 1] - L >= 0)


def plant():
    rng = random.Random(7463)
    pt = english_plant(7463)
    M = route()
    y = [None] * 97
    for i, ch in enumerate(pt):
        y[M[i]] = ch
    primer = [rng.randrange(26) for _ in range(L)]
    c = []
    for j in range(97):
        k = primer[j] if j < L else KRY.index(c[j - L])
        c.append(KRY[(KRY.index(y[j]) + k) % 26])
    return {"plaintext": pt, "key": (PERM, "then col12", "A ciphertext autokey", "lag", L, "KRYPTOS", "V", primer),
            "ciphertext": "".join(c), "checks": checks(M)}


def found(result, plant):
    s = result.get("bounds", {}).get("summary", {}).get("A ciphertext autokey", {})
    top = s.get("k4_max_checks_survivor", 0)
    return top == plant["checks"] and top >= 12, (f"A ciphertext autokey: most checks on a survivor {top} (planted setting {plant['checks']}); "
                                                  f">=5 checks {s.get('k4_ge5')} (copies {min(s.get('coppers_ge5') or [0])}-{max(s.get('coppers_ge5') or [0])})")
