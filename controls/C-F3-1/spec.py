"""Positive control for F3/1 (issue #73): a puzzle word plus any dictionary word, added (0115).
0115 took every puzzle word at every start, let the 24 known letters force the second word at lengths 3-24 on
18 table rules, and looked the forced word up among all rotations of the dictionary; K4 gave no hit. Here the
planted puzzle word, start and dictionary word must come back as a hit, and its candidate must read the planted
text. 0115's encrypt() is a stub, so the plant makes its own ciphertext."""
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F3/1"
EXPERIMENT = "0115"
WHAT = ("Key = PALIMPSEST from its 5th letter (start 4) + LANTERN (dictionary, length 7), both numbered on the KRYPTOS "
        "order; plain standard, cipher KRYPTOS, Vigenere; on English from Carter")
W1, O1, W2 = "PALIMPSEST", 4, "LANTERN"


def plant():
    pt = english_plant(7530)
    ct = "".join(KRY[(STD.index(ch) + KRY.index(W1[(i + O1) % len(W1)]) + KRY.index(W2[i % len(W2)])) % 26]
                 for i, ch in enumerate(pt))
    return {"plaintext": pt, "key": (W1, O1, W2, "vig/std/kry/kry"), "ciphertext": ct}


def found(result, plant):
    b = result.get("bounds", {})
    hits = [h for h in b.get("k4_hits", []) if h["word1"] == W1 and h["start1"] == O1 and h["n"] == len(W2)
            and h["key2"] == W2 and h["rule"] == "vig/std/kry/kry"]
    reads = [c for c in result.get("candidates", []) if c["plaintext"] == plant["plaintext"]]
    return bool(hits) and bool(reads), (f"dictionary hits {b.get('n_k4_hits')} (copies {b.get('controls_hits')}); the planted "
                                        f"pair among the listed hits: {bool(hits)}; candidates reading the plant: {len(reads)}")
