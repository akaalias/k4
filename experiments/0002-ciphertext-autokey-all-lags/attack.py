"""Experiment 0002. See program.md for the contract."""

EXPERIMENT = {
    "slug": "ciphertext-autokey-all-lags",
    "title": "Ciphertext autokey is decided by the cribs at every lag and convention",
    "family": "1-keyed-periodic",
    "parent": None,
    "changed": "New root. Replaces keyword search with a decidable test the cribs settle outright.",
    "hypothesis_expert": (
        "K4 is a ciphertext-autokey cipher: after a primer of length L, each key letter is the "
        "ciphertext letter L positions earlier, so c[i] = f(p[i], c[i-L]). The NSA tested this "
        "against the interval-7 property in 2007 without cribs (knowledge/05-attacks.md). With 24 "
        "known plaintext letters the test is exact: at every crib position i > L both p[i] and "
        "c[i-L] are known, so the convention either reproduces c[i] or it does not. We test all "
        "24 conventions in kryptos.alphabets (plain, cipher and key alphabet each standard or "
        "KRYPTOS; Vigenere, Beaufort, variant Beaufort) at every lag 1 to 96. A convention and lag "
        "that fits all checkable cribs decrypts positions L+1 to 97 with no key at all. Clue "
        "register: C4(d) is not touched; this tests the NSA's own first hypothesis. Bounds: "
        "complete for this family under these conventions."
    ),
    "hypothesis_eli5": (
        "In an autokey cipher the secret word only covers the first few letters. After that, the "
        "scrambled message itself becomes the key: to hide the twentieth letter you use the "
        "scrambled letter a fixed distance back. Because we know the scrambled text and we know 24 "
        "letters of the real message, we can check every possible distance back. If one works, "
        "most of the message falls out with no secret word at all. If none works, this whole kind "
        "of cipher is off the table for good."
    ),
    "prediction": "No convention and lag reproduces all checkable cribs; zero candidates pass the crib gate. The family is excluded, not merely unexplored.",
    "method": (
        "For each convention and each lag L in 1..96: for every crib position i with i > L, "
        "compute f(p[i], c[i-L]) and compare with c[i]. Record the number of checks and mismatches. "
        "For any (convention, L) with zero mismatches, decrypt positions L+1..97 from the ciphertext, "
        "fill positions 1..L with the crib letters where known and A elsewhere, and submit as a "
        "candidate with key_bits = 4.7*L for the primer."
    ),
    "walkthrough": (
        "1. Write the ciphertext in a row and number it 1 to 97. 2. Pick a distance, say 7. 3. Go "
        "to position 64, where the plaintext is B. Look seven back: position 57 is D. 4. Under the "
        "sculpture's alphabet KRYPTOSABCDEFGHIJLMNQUVWXZ, B is at 8 and D is at 10; add them, 18, "
        "and read the 18th letter, M. 5. The carved letter at 64 is N, not M, so distance 7 under "
        "this convention is wrong. 6. Repeat for every crib position, every distance, and every "
        "way of indexing the alphabets. One surviving distance would decrypt the rest by itself."
    ),
}

from kryptos.alphabets import conventions, encrypt_letter, decrypt_letter


def encrypt(plaintext, key):
    pa, ca, ka, m, L, primer = key["pa"], key["ca"], key["ka"], key["m"], key["lag"], key["primer"]
    out = []
    for i, p in enumerate(plaintext):
        k = primer[i] if i < L else out[i - L]
        out.append(encrypt_letter(p, k, pa, ca, ka, m))
    return "".join(out)


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    survivors, checked = [], 0
    for conv in conventions():
        pa, ca, ka, m = conv
        for L in range(1, 97):
            checks = mism = 0
            for pos, p in known.items():
                if pos > L:
                    checks += 1
                    if encrypt_letter(p, ct[pos - 1 - L], pa, ca, ka, m) != ct[pos - 1]:
                        mism += 1
            checked += 1
            if checks and mism == 0:
                survivors.append((conv, L, checks))
    candidates = []
    for conv, L, checks in survivors:
        pa, ca, ka, m = conv
        pt = []
        for i in range(97):
            if i < L:
                pt.append(known.get(i + 1, "A"))
            else:
                pt.append(decrypt_letter(ct[i], ct[i - L], pa, ca, ka, m))
        primer = "".join(pt[:L])
        key = {"pa": pa, "ca": ca, "ka": ka, "m": m, "lag": L, "primer": primer}
        candidates.append({"plaintext": "".join(pt), "key": key, "key_bits": 4.7 * L,
                           "key_description": f"ciphertext autokey lag {L}, {pa}/{ca}/{ka} {m}, primer {primer}",
                           "notes": f"{checks} crib checks passed"})
    return {
        "candidates": candidates,
        "bounds": {"family": "ciphertext autokey", "conventions": 24, "lags": "1-96",
                   "pairs_tested": checked, "survivors": len(survivors),
                   "decidability": "exact at every crib position i > lag"},
        "notes": "A survivor must also reproduce the cribs inside the primer region, which the gate checks.",
    }


def worked_example(ctx, key):
    A = ctx.KRYPTOS_ALPHABET
    lines = ["ciphertext autokey, lag 7, all alphabets KRYPTOS, Vigenere", f"alphabet: {A}", ""]
    lines.append("pos  plain  key=c[pos-7]  idx(p)+idx(k)  predicted  carved")
    for pos in (64, 65, 66, 67, 68, 69):
        p = ctx.KNOWN[pos]; k = ctx.K4[pos - 1 - 7]
        n = (A.index(p) + A.index(k)) % 26
        lines.append(f"{pos:>3}    {p}      {k}             {A.index(p):>2}+{A.index(k):<2}        {A[n]}        {ctx.K4[pos-1]}  {'ok' if A[n]==ctx.K4[pos-1] else 'x'}")
    return "\n".join(lines)
