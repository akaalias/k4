"""Frozen library for the Kryptos K4 autoresearch loop.

Nothing in this package is edited by the loop agent. It holds the facts
(ciphertext, cribs, alphabets, K1-K3 ground truth), the cipher primitives
that are verified against K1-K3, the hard gates, and the scorer.
"""
from .facts import K4, CRIBS, KNOWN, KRYPTOS_ALPHABET, STANDARD_ALPHABET, load_k1, load_k2, load_k3
from .ciphers import keyed_vigenere_encrypt, keyed_vigenere_decrypt, tableau_rows
from .gates import run_gates, crib_hits, GateResult
from .scorer import english_score, fitness, key_bits_for_words

__all__ = [
    "K4", "CRIBS", "KNOWN", "KRYPTOS_ALPHABET", "STANDARD_ALPHABET",
    "load_k1", "load_k2", "load_k3",
    "keyed_vigenere_encrypt", "keyed_vigenere_decrypt", "tableau_rows",
    "run_gates", "crib_hits", "GateResult",
    "english_score", "fitness", "key_bits_for_words",
]
