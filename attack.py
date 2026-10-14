"""attack.py: the only file the loop agent edits.

Contract (the harness relies on exactly these names):

EXPERIMENT  dict with: slug, title, family, parent (tag of the parent experiment
            or None), changed (one line: what this changes vs the parent),
            hypothesis_expert, hypothesis_eli5, prediction, method, walkthrough.
run(ctx)    returns {"candidates": [...], "bounds": {...}, "notes": str}.
            Each candidate: {"plaintext": 97 A-Z letters, "key": json-able,
            "key_bits": float, "key_description": str}. Return before
            ctx.deadline; use ctx.time_left(). Candidates are gated in order:
            length, alphabet, cribs, re-encryption. Only survivors are scored.
            "bounds" must say what was searched so a null result is a bounded
            negative result, not a shrug.
encrypt(plaintext, key)   the forward cipher. The harness re-encrypts every
            candidate with this and requires an exact match with K4.
worked_example(ctx, key)  returns a short text figure: a few letters passing
            through the method, with the tableau row / key letter shown.
            Called with key=None when run() returned no candidates; then show
            the method on a sample.
"""

EXPERIMENT = {
    "slug": "baseline-kryptos-keyword",
    "title": "Baseline: keyed Vigenere over the sculpture's own alphabet with key KRYPTOS",
    "family": "1-keyed-periodic",
    "parent": None,
    "changed": "Root experiment; establishes the pipeline with the most naive attack.",
    "hypothesis_expert": (
        "K4 is a Quagmire-III Vigenere over the KRYPTOS-keyed alphabet, like K1 and K2, "
        "with the sculpture's own name as the keyword. This is the null hypothesis the "
        "community discarded in 1999; it is here to prove the gates and the record format, "
        "and to show the cribs rejecting it."
    ),
    "hypothesis_eli5": (
        "The first two messages on the sculpture were locked with a simple scheme: a secret word "
        "is written over and over under the message, and each pair of letters is looked up in a "
        "table carved on the sculpture. We try the laziest possible secret word, KRYPTOS. We expect "
        "it to fail, and the way it fails tells us the checking machinery works: the 24 letters "
        "Sanborn has revealed will not show up where they should."
    ),
    "prediction": "Fails the crib gate with at most a handful of chance hits out of 24; zero candidates pass.",
    "method": (
        "Decrypt K4 with keyed_vigenere_decrypt(K4, 'KRYPTOS', KRYPTOS_ALPHABET). "
        "Submit that single plaintext as the candidate. Key bits counted as 4.7 per letter."
    ),
    "walkthrough": (
        "Take the keyed alphabet KRYPTOSABCDEFGHIJLMNQUVWXZ. Number its letters 0 to 25. "
        "For each ciphertext letter, find its number, subtract the number of the key letter "
        "beneath it (the key KRYPTOS repeating), wrap around 26, and read off the plaintext "
        "letter at that number. The harness then checks positions 22 to 34 for EASTNORTHEAST "
        "and 64 to 74 for BERLINCLOCK. If they are not there, the hypothesis is dead at that gate."
    ),
}

KEY = "KRYPTOS"


def encrypt(plaintext, key):
    from kryptos.ciphers import keyed_vigenere_encrypt
    return keyed_vigenere_encrypt(plaintext, key)


def run(ctx):
    pt = ctx.ciphers.keyed_vigenere_decrypt(ctx.K4, KEY, ctx.KRYPTOS_ALPHABET)
    return {
        "candidates": [{
            "plaintext": pt,
            "key": KEY,
            "key_bits": 4.7 * len(KEY),
            "key_description": f"keyed Vigenere, alphabet KRYPTOS, keyword {KEY}",
        }],
        "bounds": {"family": "keyed Vigenere over KRYPTOS alphabet", "keys_tried": [KEY], "periods": [7]},
        "notes": "Pipeline check only.",
    }


def worked_example(ctx, key):
    key = key or KEY
    A = ctx.KRYPTOS_ALPHABET
    lines = [f"alphabet: {A}", f"key:      {key} (repeating)", ""]
    lines.append("pos  cipher  key  (c - k) mod 26  plain")
    for i in range(6):
        c = ctx.K4[i]
        k = key[i % len(key)]
        n = (A.index(c) - A.index(k)) % 26
        lines.append(f"{i+1:>3}    {c}      {k}     {A.index(c):>2} - {A.index(k):>2} = {n:>2}     {A[n]}")
    return "\n".join(lines)
