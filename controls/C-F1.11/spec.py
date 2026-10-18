"""Positive control for F1.11 (issue #73): a split key phrase (EMC par. 59d) (0157).
0157 tried 29,880 phrases (puzzle-word pairs and K1-K3 word runs split at each boundary), 3 numberings and 3 rules,
and decrypts every full hit; the planted phrase must come back with the planted text."""
from kryptos.plants import english_plant

ITEM = "F1.11"
EXPERIMENT = "0157"
WHAT = "Split key phrase TREMBLING / HANDS (K3's words): plain alphabet TREMBLING-mixed, cipher HANDS-mixed, key TREMBLINGHANDS numbered on the plain alphabet, Beaufort, on English from Carter"


def plant():
    return {"plaintext": english_plant(7384), "key": {"plain": "TREMBLING", "cipher": "HANDS", "numbering": "P", "rule": "beau"}}


def found(result, plant):
    b = result.get("bounds", {})
    hit = [c for c in result.get("candidates", []) if c["plaintext"] == plant["plaintext"]]
    return bool(hit), f"full hits {b.get('k4_full_hits')} (copies {b.get('controls_full_hits')}); the planted text among the candidates: {bool(hit)}"
