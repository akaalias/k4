"""Positive control for F3/2 (issue #73): a word plus digits from the story (0038).
0038 (the same code as 0024, with 17 digit readings of dates and counts instead of 0024's coordinates) took every
reading at every alignment and sign, let the 24 known letters force the word at lengths 2-30 on 8 table rules, and
submitted every fully forced word found among the puzzle words or K1-K3's stretches; K4 gave none. Here the planted
word, reading, alignment and sign must come back as a candidate reading the planted text. Candidates are listed up to
50; K4 had 0. The attack's own encrypt() makes the ciphertext."""
from kryptos.plants import english_plant

ITEM = "F3/2"
EXPERIMENT = "0038"
WHAT = ("PALIMPSEST minus the digits of 9 Nov 1989 (9111989) from the 4th digit (offset 3, sign -1); word read on the "
        "KRYPTOS order; plain KRYPTOS, cipher standard, Beaufort; on English from Carter")
KEY = {"word": "PALIMPSEST", "digits": "9111989", "o": 3, "s": -1, "ka": "kry", "pa": "kry", "ca": "std", "m": "beau"}


def plant():
    return {"plaintext": english_plant(7535), "key": KEY}


def found(result, plant):
    b = result.get("bounds", {})
    hit = [c for c in result.get("candidates", []) if c["plaintext"] == plant["plaintext"]
           and all(c["key"][k] == KEY[k] for k in ("word", "digits", "o", "s"))]
    return bool(hit), (f"matches {b.get('vocab_matches')} (first 50 listed); shortest surviving word length "
                       f"{b.get('shortest_surviving_word_length')}; candidates with the planted word, digits, offset and sign: {len(hit)}")
