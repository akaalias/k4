"""Experiment 0052. See program.md for the contract."""

EXPERIMENT = {
    "slug": "small-alphabet-and-digraph-systems-structural",
    "title": "Ciphers that cannot write all 26 letters, or cannot write an odd number of them",
    "family": "8-hill-and-polygraphic",
    "parent": "0015-hill-solved-from-crib-blocks",
    "changed": "Experiments 15, 36 and 44 tested Hill ciphers. The other classic polygraphic systems, Playfair, two-square, four-square and bifid, work on a 5 by 5 square of 25 letters, and the Berlin World Clock reading of the clock clue suggests a 24-letter ring. Such systems leave a fingerprint in the ciphertext itself: a letter that never appears, or an even length. This checks the fingerprint before any key search.",
    "hypothesis_expert": (
        "Playfair, two-square and four-square encipher digraphs on 5x5 squares (25 symbols, I/J or Q "
        "dropped) and need an even-length text; bifid on a 5x5 square emits only the square's 25 letters; "
        "ADFGX and ADFGVX emit 5 or 6 letters; a cipher on the Weltzeituhr's 24-zone ring (C12b) emits at "
        "most 24 letters. Count the distinct letters of K4 and its length. If all 26 letters occur, every "
        "system whose ciphertext alphabet has at most 25 symbols is excluded, whatever the key; if the "
        "length is odd, every digraphic system without a null is excluded. Ten shuffles of K4 are not "
        "needed: the test is structural and exact."
    ),
    "hypothesis_eli5": (
        "Some famous ciphers use a five-by-five square of letters, which has room for only 25 of the 26, "
        "so one letter can never come out of them. Others swap letters two at a time, so the message they "
        "make always has an even number of letters. The copper has 97 letters, an odd number, and we check "
        "whether every letter of the alphabet appears on it. Either fact rules out a whole group of "
        "ciphers at once, without trying a single secret word."
    ),
    "prediction": (
        "All 26 letters occur in K4 and its length is odd, so Playfair, two-square, four-square, bifid on "
        "5x5, ADFGX, ADFGVX and any 24-letter ring cipher are excluded. Zero candidates."
    ),
    "method": (
        "1. List the distinct letters of K4 and the count of each. 2. Note the length. 3. For each system, "
        "state its output alphabet size and length rule. 4. Mark each system excluded or open. 5. Say "
        "which escape routes remain: a null letter appended, a 6x6 square with digits spelled out, a "
        "26-symbol variant."
    ),
    "walkthrough": (
        "1. Write the 26 letters A to Z in a row. 2. Read the copper's 97 letters and tick each letter as "
        "it appears. 3. J appears at place 41 and I at place 16, so a square that merges I and J cannot "
        "have made this text. 4. Q appears at places 26 and 27, so a square that drops Q cannot either. "
        "5. Every one of the 26 ticks gets ticked, so no 25-letter square made it. 6. Count the letters: "
        "97, an odd number, so no cipher that works two letters at a time made it without an extra letter."
    ),
}

from collections import Counter


def encrypt(plaintext, key):
    return plaintext


def run(ctx):
    ct = ctx.K4
    cnt = Counter(ct)
    systems = [("Playfair", 25, True), ("two-square", 25, True), ("four-square", 25, True), ("bifid 5x5", 25, False),
               ("ADFGX", 5, True), ("ADFGVX", 6, True), ("Weltzeituhr 24-letter ring", 24, False), ("Polybius 5x5 to letters", 25, False)]
    verdict = {}
    for name, size, even in systems:
        reasons = []
        if len(cnt) > size:
            reasons.append(f"emits at most {size} letters; K4 has {len(cnt)}")
        if even and len(ct) % 2:
            reasons.append(f"needs an even length; K4 has {len(ct)}")
        verdict[name] = "excluded: " + "; ".join(reasons) if reasons else "open"
    rarest = sorted(cnt.items(), key=lambda kv: kv[1])[:6]
    return {
        "candidates": [],
        "bounds": {"family": "ciphers with fewer than 26 output symbols or an even-length rule", "distinct_letters": len(cnt),
                   "length": len(ct), "rarest_letters": dict(rarest), "verdicts": verdict,
                   "escape_routes": ["a null letter appended to make the length even (then the 25-letter rule still applies)",
                                     "a 6x6 square with digits written out as words", "a variant on a 26-letter rectangle"]},
        "notes": f"K4 uses all {len(cnt)} letters and has {len(ct)} letters; every listed system is excluded: " + "; ".join(f"{k}" for k, v in verdict.items() if v.startswith("excluded")) + ".",
    }


def worked_example(ctx, key):
    cnt = Counter(ctx.K4)
    return "letter counts on the copper:\n" + "  ".join(f"{ch}{cnt[ch]}" for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ") + f"\nlength {len(ctx.K4)}"
