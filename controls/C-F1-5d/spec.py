"""Positive control for F1/5 (issue #73): ciphertext autokey continuing the carved stream from K3 (0118).
0118 keyed each K4 letter by the carved letter `lag` places earlier in the whole left side (K1-K3, then K4
itself), lags 1-200, 12 rules, and counted known letters recovered; the planted lag and rule must recover 24.
0118 locates K4 on its own copy of the plate by the string ?OBKR and asserts that the plate ends with the text
it is given. The planted copper is therefore written onto that copy of the plate (lines 11-14 of the lower-left
plate), and the plant's first four letters are chosen so the planted copper begins OBKR as the carved one does.
The method is not touched. 0118's encrypt() is a stub, so the plant makes its own ciphertext."""
import sys

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F1/5"
EXPERIMENT = "0118"
WHAT = "Ciphertext autokey on the carved stream (letters only), lag 40, plain standard, cipher KRYPTOS, Vigenere, on English from Carter with its first four letters set so the copper begins OBKR"
LAG = 40


def plant():
    atk = sys.modules["attack"]
    pre = "".join(atk.UPPER_LEFT + atk.LOWER_LEFT)
    pre = pre[:pre.index("?OBKR")].replace("?", "")
    pt = list(english_plant(7324))
    out = []
    for i in range(97):
        k = (pre + "".join(out))[len(pre) + i - LAG]
        if i < 4:   # choose the plaintext letter that makes O, B, K, R
            v = (KRY.index("OBKR"[i]) - KRY.index(k)) % 26
            pt[i] = STD[v]
        out.append(KRY[(STD.index(pt[i]) + KRY.index(k)) % 26])
    ct = "".join(out)
    ll = list(atk.LOWER_LEFT)
    ll[10] = ll[10][:-4] + ct[:4]
    ll[11], ll[12], ll[13] = ct[4:35], ct[35:66], ct[66:97]
    atk.LOWER_LEFT = ll
    return {"plaintext": "".join(pt), "key": ("letters only", LAG, "vig", "std", "kry"), "ciphertext": ct}


def found(result, plant):
    b = result.get("bounds", {})
    full = [f for f in b.get("k4_full", []) if f[0] == "letters only" and f[1] == LAG and tuple(f[2:]) == ("vig", "std", "kry")]
    return bool(full), f"full matches {len(b.get('k4_full', []))}, the planted one among them: {bool(full)}; best {b.get('k4_best_lag_hits')}/24, copies {b.get('controls_best_lag_hits')}"
