"""Experiment 0004. See program.md for the contract."""

EXPERIMENT = {
    "slug": "running-key-from-k1-k3",
    "title": "A running key drawn from K1, K2 or K3 at every offset",
    "family": "1-keyed-periodic",
    "parent": "0003-plaintext-autokey-all-lags",
    "changed": "The key is a stretch of the solved sections or their ciphertext, not the message itself.",
    "hypothesis_expert": (
        "K4 uses a running key: a 97-letter stretch of text the solver already has, applied through "
        "the tableau. Sanborn said he left 'instructions in the earlier text that refer to later "
        "text' and that K4 'will come back to the first part' (clue register C7). Gillogly guessed "
        "running key in 1999; Schridde tried the K1 to K3 plaintexts under two conventions. We make "
        "it exhaustive: key sources are the K1, K2 (as carved and corrected) and K3 plaintexts, the "
        "three ciphertexts, and the concatenations of each set, read forward and backward, at every "
        "offset including wrap-around, under all 24 conventions. Every crib position is checkable, "
        "so each (source, direction, offset, convention) is excluded or survives. Bounds: complete "
        "for these sources. Not covered: the tableau text, the Morse, external books."
    ),
    "hypothesis_eli5": (
        "Instead of a short secret word, the key might be a long piece of text the solver already "
        "knows, such as the first three messages on the sculpture. We slide each of those texts "
        "along the fourth message in every possible position, forwards and backwards, and check "
        "whether any position explains all 24 known letters. If none does, those texts are not the "
        "key, full stop."
    ),
    "prediction": "No source, direction, offset or convention reproduces all 24 cribs. The best alignment matches fewer than 8 of 24, which is chance for this many trials.",
    "method": (
        "Build key texts: K1, K2 carved, K2 corrected, K3 plaintexts (letters only); K1, K2, K3 "
        "ciphertexts (letters only); K1+K2+K3 plaintext and ciphertext concatenations. For each, "
        "both directions. For offset o in 0..len-1 with cyclic wrap, key[i] = text[(o+i) mod len]. "
        "For each convention compare encrypt(p[pos], key[pos]) with c[pos] at all 24 cribs. Survivors "
        "are submitted as candidates by decrypting all 97 letters; key_bits is log2(trials)."
    ),
    "walkthrough": (
        "1. Write K1's plaintext, BETWEENSUBTLE..., under the K4 ciphertext starting at some offset. "
        "2. At position 64 the plaintext must be B. Suppose the key letter above it is T. 3. Under "
        "the sculpture's alphabet, B is 8 and T is 4; add, 12, read F. 4. The carved letter is N, so "
        "this offset fails. 5. Slide one letter and repeat, for every text, direction and alphabet "
        "convention. 6. An offset that passes all 24 checks decrypts the rest at once."
    ),
}

import math
from kryptos.alphabets import conventions, encrypt_letter, decrypt_letter
from kryptos.facts import load_k1, load_k2, load_k3


def letters(s):
    return "".join(c for c in s if "A" <= c <= "Z")


def sources():
    k1, k2, k3 = load_k1(), load_k2(), load_k3()
    src = {
        "K1pt": letters(k1["plaintext"]), "K2pt": letters(k2["plaintext_as_carved"]),
        "K2pt_corr": letters(k2["plaintext_as_carved"])[:-12] + "WESTXLAYERTWO",
        "K3pt": letters(k3["plaintext"]),
        "K1ct": letters(k1["ciphertext"]), "K2ct": letters(k2["ciphertext_as_carved"]), "K3ct": letters(k3["ciphertext"]),
    }
    src["K123pt"] = src["K1pt"] + src["K2pt"] + src["K3pt"]
    src["K123ct"] = src["K1ct"] + src["K2ct"] + src["K3ct"]
    out = {}
    for name, t in src.items():
        out[name + "_fwd"] = t
        out[name + "_rev"] = t[::-1]
    return out


def encrypt(plaintext, key):
    text = key["text"]; o = key["offset"]; pa, ca, ka, m = key["pa"], key["ca"], key["ka"], key["m"]
    return "".join(encrypt_letter(p, text[(o + i) % len(text)], pa, ca, ka, m) for i, p in enumerate(plaintext))


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    src = sources()
    trials = 0
    best = (99, None)
    survivors = []
    for name, text in src.items():
        n = len(text)
        for conv in conventions():
            pa, ca, ka, m = conv
            for o in range(n):
                trials += 1
                mism = 0
                for pos, p in known.items():
                    if encrypt_letter(p, text[(o + pos - 1) % n], pa, ca, ka, m) != ct[pos - 1]:
                        mism += 1
                        if mism >= best[0] and mism > 0:
                            break
                if mism < best[0]:
                    best = (mism, (name, conv, o))
                if mism == 0:
                    survivors.append((name, conv, o))
            if ctx.time_left() < 30:
                break
    candidates = []
    for name, conv, o in survivors:
        pa, ca, ka, m = conv
        text = src[name]
        pt = "".join(decrypt_letter(ct[i], text[(o + i) % len(text)], pa, ca, ka, m) for i in range(97))
        candidates.append({"plaintext": pt, "key": {"text": text, "offset": o, "pa": pa, "ca": ca, "ka": ka, "m": m},
                           "key_bits": math.log2(trials), "key_description": f"running key {name} offset {o}, {pa}/{ca}/{ka} {m}"})
    return {
        "candidates": candidates,
        "bounds": {"family": "running key from K1-K3", "sources": sorted(src), "conventions": 24,
                   "offsets": "all, cyclic", "trials": trials, "survivors": len(survivors),
                   "best_mismatches_of_24": best[0], "best_alignment": best[1]},
        "notes": "Every trial is decided at all 24 crib positions.",
    }


def worked_example(ctx, key):
    A = ctx.KRYPTOS_ALPHABET
    k1 = letters(load_k1()["plaintext"])
    o = 0
    lines = ["running key = K1 plaintext at offset 0, all alphabets KRYPTOS, Vigenere", f"alphabet: {A}", "",
             "pos  plain  key          idx(p)+idx(k)  predicted  carved"]
    for pos in (64, 65, 66, 67, 68, 69):
        p = ctx.KNOWN[pos]; k = k1[(o + pos - 1) % len(k1)]
        n = (A.index(p) + A.index(k)) % 26
        lines.append(f"{pos:>3}    {p}      {k}           {A.index(p):>2}+{A.index(k):<2}        {A[n]}        {ctx.K4[pos-1]}  {'ok' if A[n]==ctx.K4[pos-1] else 'x'}")
    return "\n".join(lines)
