"""Positive control for F3/3 (issue #73): a word plus the misspelt or raised letters (0061).
0061 counted, exactly, how many of the 24 known letters each setting reproduces (every puzzle word plus or minus every
ordering of QUA, LOE, QUAE, LOEE, YAR and DYAHR, 4 tables x 3 modes x 2 letterings) and reported the best; K4's best
was 8/24, copies 7-11. Here the planted setting must reach 24/24 and the attack's one candidate (the best setting)
must read the planted text. The attack's own encrypt() makes the ciphertext."""
from kryptos.facts import KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F3/3"
EXPERIMENT = "0061"
WHAT = ("INVISIBLE minus UQEA (an ordering of QUAE), both on the KRYPTOS order; plain standard, cipher KRYPTOS, Beaufort; "
        "on English from Carter")
W, S, SGN = "INVISIBLE", "UQEA", -1


def plant():
    k = [(KRY.index(W[i % len(W)]) + SGN * KRY.index(S[i % len(S)])) % 26 for i in range(97)]
    return {"plaintext": english_plant(7538), "key": {"pa": "std", "ca": "kry", "m": "beau", "k": k}}


def found(result, plant):
    b = result.get("bounds", {})
    c = result.get("candidates", [])
    ok = b.get("best_hits") == 24 and bool(c) and c[0]["plaintext"] == plant["plaintext"]
    return ok, f"best {b.get('best_hits')}/24 at {b.get('best_setting')}; copies best {b.get('control_best_hits')}; candidate reads the plant: {bool(c) and c[0]['plaintext'] == plant['plaintext']}"
