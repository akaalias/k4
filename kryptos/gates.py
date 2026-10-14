"""Hard gates. A candidate that fails a gate is never scored on English."""
from dataclasses import dataclass, field
from .facts import K4, KNOWN, CRIBS


@dataclass
class GateResult:
    passed: bool
    failed_at: str | None
    crib_hits: int
    details: dict = field(default_factory=dict)
    crib_words: dict = field(default_factory=dict)  # word -> (hits, length)


def crib_hits(plaintext: str) -> int:
    """How many of the 24 known letters are in place. Diagnostic only."""
    return sum(1 for pos, ch in KNOWN.items() if pos - 1 < len(plaintext) and plaintext[pos - 1] == ch)


def crib_words(plaintext: str) -> dict:
    """Per clue word: (letters matched, word length). EAST, NORTHEAST, BERLIN, CLOCK."""
    out = {}
    for start, word in CRIBS:
        hits = sum(1 for i, ch in enumerate(word) if start - 1 + i < len(plaintext) and plaintext[start - 1 + i] == ch)
        out[word] = (hits, len(word))
    return out


def run_gates(plaintext: str, reencrypted: str | None) -> GateResult:
    """Gates in order: length, alphabet, cribs, re-encryption.

    `reencrypted` is the attack's forward encryption of `plaintext` under its
    stated key. It must equal K4 exactly. Pass None to skip (the result is
    then marked as not fully gated)."""
    hits = crib_hits(plaintext) if plaintext else 0
    words = crib_words(plaintext) if plaintext else {}
    if len(plaintext) != 97:
        return GateResult(False, "length", hits, {"length": len(plaintext)}, words)
    if not all("A" <= c <= "Z" for c in plaintext):
        return GateResult(False, "alphabet", hits, {}, words)
    if hits != 24:
        missing = [(p, KNOWN[p], plaintext[p - 1]) for p in sorted(KNOWN) if plaintext[p - 1] != KNOWN[p]]
        return GateResult(False, "cribs", hits, {"mismatches": missing}, words)
    if reencrypted is None:
        return GateResult(False, "reencryption_missing", hits, {}, words)
    if reencrypted != K4:
        diff = [i + 1 for i, (a, b) in enumerate(zip(reencrypted, K4)) if a != b]
        return GateResult(False, "reencryption", hits, {"diff_positions": diff[:20], "n_diff": len(diff)}, words)
    return GateResult(True, None, hits, {}, words)
