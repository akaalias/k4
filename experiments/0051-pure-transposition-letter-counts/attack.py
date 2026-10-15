"""Experiment 0051. See program.md for the contract."""

EXPERIMENT = {
    "slug": "pure-transposition-letter-counts",
    "title": "Could K4 be its own letters rearranged? A count of the known letters against the carved ones",
    "family": "6-transposition-then-tableau",
    "parent": "0006-columnar-then-tableau-period-survival",
    "changed": "Every earlier transposition experiment put a substitution (the table) after the reordering. Here the substitution is taken away: if K4 were only a rearrangement of its message, the carved letters would be the message's letters in another order, and the letter counts alone decide it.",
    "hypothesis_expert": (
        "C9(a) reads 'the letters sitting there in plain sight' as a pure transposition: the ciphertext "
        "is a permutation of the plaintext, and C8(d) proposes KRYPTOS as a transposition key. Any "
        "permutation preserves the letter multiset, so the 24 crib letters must be a sub-multiset of the "
        "97 carved letters. Count each crib letter against the copper, for the carved 97, for the 98 "
        "with the K3 question mark (C18), and for each one-letter deletion (the copper with a spurious "
        "letter). If any count fails in every reading, every transposition, keyed or route, single or "
        "double, KRYPTOS-keyed or not, is excluded without enumerating keys. Bounds: exact."
    ),
    "hypothesis_eli5": (
        "If the fourth message were just its own letters shuffled, like an anagram, then every letter of "
        "the message would be somewhere on the copper. We know 24 letters of the message. So we count: "
        "does the copper have enough Es, enough Ns, enough Rs to spell them? One shortfall is enough to rule "
        "out every way of shuffling at once."
    ),
    "prediction": (
        "At least one crib letter is short on the copper in the 97 and 98 readings and under every "
        "one-letter deletion, so pure transposition is excluded; it survives only if one carved letter is "
        "wrong and should be that letter. Zero candidates."
    ),
    "method": (
        "1. Count the 24 known letters by letter. 2. Count the carved letters. 3. List every letter whose "
        "need exceeds its supply. 4. Repeat with the question mark added and with each of the 97 letters "
        "deleted. 5. Say which single carving error, if any, would make the counts possible."
    ),
    "walkthrough": (
        "1. Write out EASTNORTHEAST and BERLINCLOCK. 2. Count the Es: E-A-S-T-N-O-R-T-H-E-A-S-T has two, "
        "B-E-R-L-I-N-C-L-O-C-K has one, so the message needs at least three Es. 3. Count the Es on the "
        "copper: OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR "
        "has two, at places 45 and 92. 4. Two is less than three, so no rearrangement of the copper can put "
        "three Es where the message has them. 5. Check the other letters the same way."
    ),
}

from collections import Counter


def encrypt(plaintext, key):
    return "".join(plaintext[i] for i in key["perm"])


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    need = Counter(known.values())

    def short(text):
        have = Counter(text)
        return {ch: (n, have[ch]) for ch, n in need.items() if n > have[ch]}

    carved = short(ct)
    with_q = short(ct + "?")
    deletions_ok = [i + 1 for i in range(len(ct)) if not short(ct[:i] + ct[i + 1:])]
    # which single replaced letter would fix the counts
    fixes = sorted({(i + 1, ct[i], ch) for i in range(len(ct)) for ch in need
                    if not short(ct[:i] + ch + ct[i + 1:])}, key=lambda t: t[0])
    fix_letters = sorted({ch for _, _, ch in fixes})
    return {
        "candidates": [],
        "bounds": {"family": "pure transposition (any permutation of the 97 carved letters)", "need": dict(need),
                   "short_carved": carved, "short_98_with_question_mark": with_q,
                   "deletions_that_fit": deletions_ok, "replacements_that_fit": len(fixes),
                   "replacement_letters_that_fit": fix_letters,
                   "replacement_examples": [f"place {p}: {a} to {b}" for p, a, b in fixes[:6]]},
        "notes": (f"Crib letters short on the copper: {carved}; with the question mark: {with_q}; one-letter deletions that fit: "
                  f"{len(deletions_ok)}. A single carved letter changed to {', '.join(fix_letters)} would make the counts fit ({len(fixes)} ways)."),
    }


def worked_example(ctx, key):
    need = Counter(ctx.KNOWN.values()); have = Counter(ctx.K4)
    lines = ["letter  needed by the cribs  on the copper"]
    for ch in sorted(need):
        lines.append(f"  {ch}            {need[ch]}                {have[ch]}{'   short' if need[ch] > have[ch] else ''}")
    return "\n".join(lines)
