"""Positive control for F3/1 (issue #73): two puzzle words in two passes on tables from the solved messages' words (0059).
0059 ran 0014's exact linear test (length pairs with a + b <= 24) on plain and cipher tables keyword-mixed from every
word of K1-K3 and Sanborn's letter not already in 0043's pool, and submitted every solution whose first or second
word is a puzzle word or a stretch of K1-K3; K4 gave none. (0043 is the same code on the vocabulary's tables; one
control covers the code.) Here the planted pair must come back as a candidate that reads the planted text.
Candidates are listed up to 50; K4 had 0, so a cut-off is unlikely; found() says how many there were.
The attack's own encrypt() makes the ciphertext."""
from kryptos.alphabets import keyword_mixed
from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.plants import english_plant

ITEM = "F3/1"
EXPERIMENT = "0059"
WHAT = ("Plain table SHADING-mixed, cipher table CANDLE-mixed (both K1-K3 words), Vigenere, EGYPT (5) + UNDERGROUND (11) "
        "numbered on the standard order, combined period 55; on English from Carter")
X, Y = "EGYPT", "UNDERGROUND"


def plant():
    key = {"pa": keyword_mixed("SHADING"), "ca": keyword_mixed("CANDLE"), "m": "vig",
           "X": [STD.index(c) for c in X], "Y": [STD.index(c) for c in Y], "s": 1}
    return {"plaintext": english_plant(7532), "key": key}


def found(result, plant):
    b = result.get("bounds", {})
    hit = [c for c in result.get("candidates", []) if c["plaintext"] == plant["plaintext"]
           and "".join(STD[v] for v in c["key"]["X"]) == X and "".join(STD[v] for v in c["key"]["Y"]) == Y]
    return bool(hit), f"word matches {b.get('vocab_matches')} (first 50 listed); candidates with the planted pair and text: {len(hit)}"
