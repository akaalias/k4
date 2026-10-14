"""Experiment 0005. See program.md for the contract."""

EXPERIMENT = {
    "slug": "quagmire-period-sweep-forced-keys",
    "title": "Periodic keyed tableau with separate alphabets: which periods survive, and what key they force",
    "family": "1-keyed-periodic",
    "parent": "0004-running-key-from-k1-k3",
    "changed": "Periodic key instead of running key; plain, cipher and key alphabets may differ (Quagmire I to IV).",
    "hypothesis_expert": (
        "K4 is a periodic tableau cipher like K1 and K2 but with a period the cribs allow and possibly "
        "different alphabets for plaintext, ciphertext and key (Quagmire I, II, III, IV under the "
        "ACA names). kryptos.cribsweep showed that for single-alphabet additive systems only periods "
        "27, 28, 29 and 53 to 97 survive; nobody has published the same sweep for separate alphabets "
        "(knowledge/05-attacks.md, open). For each of the 24 conventions and each period 1 to 97 we "
        "derive the key letter forced at every crib position and test whether positions congruent "
        "modulo the period agree. For each surviving (convention, period) we record the forced key "
        "fragment, then score it two ways: does any vocabulary word or K1 to K3 phrase of that length "
        "contain the fragment at the forced slots, and if so submit the decryption. Clue register "
        "C5(a), C8(a). Bounds: complete for periodic single-key tableau systems under these 24 "
        "conventions and all periods."
    ),
    "hypothesis_eli5": (
        "The first two messages used a repeating secret word and the table on the sculpture. We ask: "
        "if the fourth message used the same trick with a longer secret word, how long could that "
        "word be? The 24 known letters tell us which lengths are impossible, because two letters "
        "that would use the same letter of the secret word must agree. For the lengths that survive, "
        "the known letters also tell us some letters of the secret word, so we check whether any "
        "word from the puzzle's own world fits those letters."
    ),
    "prediction": "Periods 1 to 26 and 30 to 52 are excluded under every convention, as in the single-alphabet sweep. Surviving periods force key fragments that match no vocabulary word. Zero candidates pass.",
    "method": (
        "For convention (pa, ca, ka, m) and period P: forced[slot] = key_letter_for(p, c) for each crib; "
        "a conflict at any slot excludes (convention, P). For survivors, build the fragment pattern "
        "of length P with forced letters and wildcards, and match it against every word and phrase in "
        "data/vocabulary.txt plus the K1 to K3 plaintexts as sliding windows of length P. Each match "
        "yields a full key; decrypt and submit."
    ),
    "walkthrough": (
        "1. Choose a period, say 28, and a convention: plaintext on the sculpture's alphabet, "
        "ciphertext on the standard one, key on the sculpture's, Vigenere. 2. Position 22 is "
        "plaintext E, ciphertext F; the key letter that does that is forced. Position 50 would use "
        "the same key slot, but 50 is not a crib, so no conflict. 3. Positions 26 and 54: 54 is not "
        "a crib either. 4. Positions 64 and 36: neither pair conflicts. 5. Collect the forced letters "
        "into a 28-slot pattern with blanks. 6. Slide every word and phrase from the puzzle's "
        "vocabulary across the pattern. 7. A fit gives the whole key; decrypt and check the cribs."
    ),
}

from kryptos.alphabets import conventions, key_letter_for, decrypt_letter, encrypt_letter
from kryptos.facts import load_k1, load_k2, load_k3


def letters(s):
    return "".join(c for c in s if "A" <= c <= "Z")


def encrypt(plaintext, key):
    pa, ca, ka, m, k = key["pa"], key["ca"], key["ka"], key["m"], key["key"]
    return "".join(encrypt_letter(p, k[i % len(k)], pa, ca, ka, m) for i, p in enumerate(plaintext))


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    vocab = list(ctx.vocabulary)
    texts = [letters(load_k1()["plaintext"]), letters(load_k2()["plaintext_as_carved"]), letters(load_k3()["plaintext"])]
    survivors = {}
    excluded_periods_all = []
    for P in range(1, 98):
        alive = 0
        for conv in conventions():
            pa, ca, ka, m = conv
            forced = {}
            ok = True
            for pos, p in known.items():
                k = key_letter_for(p, ct[pos - 1], pa, ca, ka, m)
                slot = (pos - 1) % P
                if slot in forced and forced[slot] != k:
                    ok = False; break
                forced[slot] = k
            if ok:
                alive += 1
                survivors[(conv, P)] = forced
        if alive == 0:
            excluded_periods_all.append(P)
    candidates = []
    matches = []
    for (conv, P), forced in survivors.items():
        pa, ca, ka, m = conv
        # candidate keys of length P from vocabulary words and K1-K3 windows
        pool = set(w for w in vocab if len(w) == P)
        for t in texts:
            for i in range(0, len(t) - P + 1):
                pool.add(t[i:i + P])
        for kw in pool:
            if all(kw[s] == l for s, l in forced.items()):
                matches.append((conv, P, kw))
                pt = "".join(decrypt_letter(ct[i], kw[i % P], pa, ca, ka, m) for i in range(97))
                candidates.append({"plaintext": pt, "key": {"pa": pa, "ca": ca, "ka": ka, "m": m, "key": kw},
                                   "key_bits": 4.7 * P, "key_description": f"period {P} key {kw}, {pa}/{ca}/{ka} {m}"})
    surviving_periods = sorted({P for (_, P) in survivors})
    return {
        "candidates": candidates[:50],
        "bounds": {"family": "periodic tableau, separate alphabets (Quagmire I-IV)", "conventions": 24,
                   "periods": "1-97", "periods_excluded_all_conventions": excluded_periods_all,
                   "periods_surviving_some_convention": surviving_periods,
                   "survivor_pairs": len(survivors), "vocab_matches": len(matches),
                   "key_pool": "vocabulary words of length P plus all length-P windows of K1-K3 plaintexts"},
        "notes": f"{len(matches)} forced-fragment matches submitted as candidates.",
    }


def worked_example(ctx, key):
    from kryptos.alphabets import key_letter_for as klf
    lines = ["forced key letters, period 28, plain kry / cipher std / key kry, Vigenere", ""]
    lines.append("pos  plain  cipher  slot(pos-1 mod 28)  forced key letter")
    for pos in (22, 23, 24, 25, 26, 64, 65, 66):
        p = ctx.KNOWN[pos]; c = ctx.K4[pos - 1]
        lines.append(f"{pos:>3}    {p}      {c}        {(pos-1)%28:>2}                 {klf(p, c, 'kry', 'std', 'kry', 'vig')}")
    return "\n".join(lines)
