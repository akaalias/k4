"""Experiment 0009. See program.md for the contract."""

EXPERIMENT = {
    "slug": "forced-key-stretches-read-as-english",
    "title": "Do the two crib runs force a readable key, with the copper exact or off by one letter?",
    "family": "1-keyed-periodic",
    "parent": "0005-quagmire-period-sweep-forced-keys",
    "changed": "Instead of matching forced key fragments against a word list, score them as English. Add the one-letter-error parameter: a letter inserted or deleted at every position.",
    "hypothesis_expert": (
        "Under any periodic tableau whose period the cribs allow (27 and above, 0005), EASTNORTHEAST at "
        "22-34 forces 13 consecutive key letters and BERLINCLOCK at 64-74 forces 11, under each of the 24 "
        "conventions. If the key is a word or phrase, as Scheidt insists (C5, C6), those stretches must "
        "read as English. Schridde 2017 found them gibberish under the plain tableau; 0005 matched them "
        "against 62 vocabulary words and K1-K3 windows only. This experiment scores every stretch by "
        "quadgram log-probability per letter and compares it with the distribution of random strings and "
        "of true English windows of the same length from K1-K3. Then the one-letter-error parameter "
        "(family G, C17, C18, the K2 precedent): a letter inserted or deleted at each of 97 positions "
        "shifts the ciphertext under every crib past that point by one, giving new stretches. Expected "
        "under the null: the best of about 9,400 stretches sits around two standard deviations above the "
        "random mean and well below the English mean. Bounds: all 24 conventions, exact copper and every "
        "single insertion or deletion, both crib runs, keys at any period of 27 or more."
    ),
    "hypothesis_eli5": (
        "If the fourth message used a secret word with the sculpture's table, the 13 known letters of "
        "EASTNORTHEAST pin down 13 letters of that secret word in a row, and BERLINCLOCK pins down 11 "
        "more. A secret word made of English should look like English in those stretches. We read them "
        "off under every way the table can be used and ask a simple question: does any stretch look like "
        "English rather than noise? We also allow for the sculptor having dropped or added one letter "
        "somewhere, as he did in the second message, which would shift everything after that point by one."
    ),
    "prediction": (
        "No forced stretch scores as well as a typical English window of its length. The best stretch "
        "scores below -4.5 per quadgram, against about -3.6 for English and about -6.5 for noise. "
        "Allowing one inserted or deleted letter does not change that. Zero candidates pass."
    ),
    "method": (
        "1. For each convention, force the key letter at each crib position from the plaintext and the "
        "ciphertext letter. 2. Join the forced letters of positions 22-34 into a 13-letter stretch and "
        "64-74 into an 11-letter stretch. 3. Score each stretch by mean log10 quadgram probability. "
        "4. Repeat with the ciphertext altered by one deleted letter at each position, then by one "
        "inserted blank at each position, which shifts every crib beyond that point. 5. Calibrate: score "
        "all 13- and 11-letter windows of the K1-K3 plaintexts, and 20,000 random strings. 6. Report "
        "the best stretches with their z-scores against both distributions."
    ),
    "walkthrough": (
        "1. Take the convention: plaintext and key on the sculpture's alphabet, Vigenere. 2. Position 22 "
        "is plaintext E, ciphertext F. In the sculpture's alphabet E is index 10 and F is index 11, so the "
        "key letter has index 1: R. 3. Position 23 is A against L: A is 7, L is 18, key index 11: D. "
        "4. Carry on through position 34 to get 13 key letters in a row. 5. Read them aloud. A real key "
        "word gives something like a word; noise gives something like RDQXJ. 6. Score it by counting how "
        "common each run of four letters is in English. 7. Now suppose the sculptor dropped a letter "
        "somewhere before position 22: shift the ciphertext one place and repeat. 8. The best stretch "
        "across all of this is the answer; compare it with real English windows of the same length."
    ),
}

import random
from kryptos.alphabets import conventions, key_letter_for, encrypt_letter
from kryptos.facts import load_k1, load_k2, load_k3

RUNS = [(22, 34), (64, 74)]


def letters(s):
    return "".join(c for c in s if "A" <= c <= "Z")


def encrypt(plaintext, key):
    pa, ca, ka, m, k = key["pa"], key["ca"], key["ka"], key["m"], key["key"]
    return "".join(encrypt_letter(p, k[i % len(k)], pa, ca, ka, m) for i, p in enumerate(plaintext))


def variants(ct):
    """The copper as carved, then with one letter deleted at each position, then with one
    blank inserted at each position. A blank pairs with nothing, so the crib there is skipped."""
    yield "exact", ct
    for i in range(len(ct)):
        yield f"deleted {i+1}", ct[:i] + ct[i + 1:] + "-"
    for i in range(len(ct) + 1):
        yield f"inserted before {i+1}", ct[:i] + "-" + ct[i:]


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    score = ctx.english_score
    texts = letters(load_k1()["plaintext"]) + letters(load_k2()["plaintext_as_carved"]) + letters(load_k3()["plaintext"])
    convs = list(conventions())
    results = []
    for vname, c in variants(ct):
        for conv in convs:
            pa, ca, ka, m = conv
            for lo, hi in RUNS:
                forced = []
                for pos in range(lo, hi + 1):
                    cc = c[pos - 1]
                    if cc == "-":
                        continue
                    forced.append(key_letter_for(known[pos], cc, pa, ca, ka, m))
                stretch = "".join(forced)
                results.append((score(stretch), stretch, vname, "/".join(conv), f"{lo}-{hi}"))
    results.sort(reverse=True)
    rng = random.Random(4)

    def dist(xs):
        n = len(xs); mu = sum(xs) / n; sd = (sum((x - mu) ** 2 for x in xs) / n) ** 0.5
        return mu, sd

    eng13 = [score(texts[i:i + 13]) for i in range(len(texts) - 12)]
    eng11 = [score(texts[i:i + 11]) for i in range(len(texts) - 10)]
    rnd13 = [score("".join(rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(13))) for _ in range(20000)]
    rnd11 = [score("".join(rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(11))) for _ in range(20000)]
    cal = {"english_13": dist(eng13), "english_11": dist(eng11), "random_13": dist(rnd13), "random_11": dist(rnd11)}
    best = results[0]
    exact_best = max(r for r in results if r[2] == "exact")

    def z(r):
        n = 13 if r[4] == "22-34" else 11
        mu_e, sd_e = cal[f"english_{n}"]; mu_r, sd_r = cal[f"random_{n}"]
        return {"score": round(r[0], 3), "stretch": r[1], "copper": r[2], "convention": r[3], "run": r[4],
                "z_vs_random": round((r[0] - mu_r) / sd_r, 2), "z_vs_english": round((r[0] - mu_e) / sd_e, 2)}

    return {
        "candidates": [],
        "bounds": {"family": "periodic tableau, separate alphabets, period 27+; forced key stretches scored as English",
                   "conventions": 24, "copper_variants": 1 + 97 + 98, "stretches_scored": len(results),
                   "calibration_mean_sd": {k: (round(a, 3), round(b, 3)) for k, (a, b) in cal.items()},
                   "best_overall": z(best), "best_exact_copper": z(exact_best),
                   "top_ten": [z(r) for r in results[:10]],
                   "exact_copper_all_24": [z(r) for r in results if r[2] == "exact"]},
        "notes": "Diagnostic: no full key is implied, so no candidates. The verdict is the gap between the best stretch and the English distribution.",
    }


def worked_example(ctx, key):
    lines = ["forced key stretch under EASTNORTHEAST, convention kry/std/kry Vigenere, exact copper", ""]
    lines.append("pos  plain  cipher  key letter")
    out = []
    for pos in range(22, 35):
        p, c = ctx.KNOWN[pos], ctx.K4[pos - 1]
        k = key_letter_for(p, c, "kry", "std", "kry", "vig")
        out.append(k)
        lines.append(f"{pos:>3}    {p}      {c}       {k}")
    lines.append("")
    lines.append("stretch: " + "".join(out) + f"   score {ctx.english_score(''.join(out)):.2f} per quadgram (English about -3.6, noise about -6.5)")
    return "\n".join(lines)
