"""Experiment 0038. See program.md for the contract."""

EXPERIMENT = {
    "slug": "keyword-plus-dates-and-counts-from-the-story",
    "title": "A key word plus a number from the sculpture's own story: dates, the Morse counts, and 97 itself as the second component",
    "family": "3-two-component-key",
    "parent": "0024-keyword-plus-k2-coordinate-digits",
    "changed": "Same exact test as experiment 24, with the digit stream drawn from the sculpture's story instead of the K2 coordinates: the dedication date, the fall of the Wall, Carter's discovery, the Morse padding counts, the letter counts of the four parts, and 1990 itself.",
    "hypothesis_expert": (
        "Experiment 24 killed a word plus the K2 coordinate digits under every reading. Scheidt's two-component "
        "habit (C6) admits any memorable number as the second component, and Sanborn's own anchors are dates and "
        "counts: the dedication on 3 November 1990, the Wall's fall on 9 November 1989, his Egypt trip of 1986, "
        "Carter's breach on 26 November 1922 (C13, C7), the Morse messages' E-padding counts 5, 10, 1, 7, 9 "
        "(C25), the four parts' letter counts 63, 372, 337, 97, and 97 and 98 alone (C17). Each reading, in "
        "day-month-year and year-month-day forms, is a repeating digit key d; the word key x of length 2-30 "
        "then satisfies x[i mod a] = t[i] - s d[(i + o) mod L] mod 26 at every crib, with 24 - a redundant "
        "checks. Standard or KRYPTOS alphabets, both plaintext signs, both s, every alignment; survivors have "
        "their forced word matched against the vocabulary and K1-K3 windows and scored as English against ten "
        "shuffled controls. Bounds: complete for these seventeen digit readings."
    ),
    "hypothesis_eli5": (
        "Experiment 24 tried adding the map coordinates to a secret word. The sculpture's story has other "
        "numbers a person would remember: the day it was unveiled, the day the Berlin Wall fell, the day "
        "Carter broke into the tomb, the little counts hidden in the Morse code outside, and the number 97 "
        "itself. We add each of these to an unknown secret word, letter by letter, and let the 24 known "
        "letters tell us what the word would have to be. If two tellings disagree, that number is out."
    ),
    "prediction": (
        "No word length under 24 survives for any reading, alignment or sign; survivors from 24 up are chance "
        "and their forced words are noise against the shuffled controls. Zero candidates pass."
    ),
    "method": (
        "1. List the digit readings. 2. For each alphabet pair and plaintext sign, compute the forced total "
        "key index at each crib. 3. For each reading, alignment, sign s and word length a, subtract the digit "
        "term and reduce to the word slot; reject on any disagreement. 4. For survivors, read the word in "
        "the standard and KRYPTOS alphabets, match it against the vocabulary and K1-K3 windows, and score it "
        "as English. 5. Repeat the scoring on ten shuffles of K4."
    ),
    "walkthrough": (
        "1. Read the coordinates as the digits 3 8 5 7 6 5 7 7 8 4 4 and repeat them under the message. "
        "2. Position 22 is E against the carved F; under the sculpture's alphabet with Vigenere the total key "
        "letter is R, index 1. 3. The digit under position 22 at alignment 0 is the 22nd digit, 3; subtract it: "
        "index 24 is the word letter for slot 21 mod a. 4. With a 7-letter word that is slot 0. 5. Position 29 "
        "also uses slot 0: do the same there; the two values must agree. 6. Go through all 24 known letters; "
        "one disagreement kills this length and alignment. 7. A survivor's forced letters spell the word; "
        "see whether it is one the puzzle knows."
    ),
}

import random
from kryptos.alphabets import ALPHABETS, key_letter_for, decrypt_letter, encrypt_letter
from kryptos.facts import load_k1, load_k2, load_k3

N = 97
READINGS = {
    "dedication 3 Nov 1990, dmy": "3111990", "dedication, ymd": "19901103", "dedication, dmy padded": "03111990",
    "Wall fell 9 Nov 1989, dmy": "9111989", "Wall, ymd": "19891109",
    "Carter breach 26 Nov 1922, dmy": "26111922", "Carter, ymd": "19221126",
    "1990": "1990", "1989": "1989", "1986": "1986", "1922": "1922",
    "Morse E-padding counts 5 10 1 7 9": "510179", "Morse counts reversed": "971015",
    "letter counts 63 372 337 97": "6337233797", "97": "97", "98": "98", "97 and 24 known": "9724",
}
STD = ALPHABETS["std"]


def letters(s):
    return "".join(c for c in s if "A" <= c <= "Z")


def total_key(i, key):
    a = len(key["word"]); d = key["digits"]; L = len(d)
    x = ALPHABETS[key["ka"]].index(key["word"][i % a])
    return (x + key["s"] * int(d[(i + key["o"]) % L])) % 26


def encrypt(plaintext, key):
    pa, ca, m = key["pa"], key["ca"], key["m"]
    return "".join(encrypt_letter(p, STD[total_key(i, key)], pa, ca, "std", m) for i, p in enumerate(plaintext))


def search(ct, known, score, vocab, texts, collect):
    crib_pos = sorted(known)
    survivors, best, candidates = [], [], []
    cases = 0
    for pa in ("std", "kry"):
        for ca in ("std", "kry"):
            for m in ("vig", "beau"):
                t = {pos: STD.index(key_letter_for(known[pos], ct[pos - 1], pa, ca, "std", m)) for pos in crib_pos}
                for rname, d in READINGS.items():
                    L = len(d)
                    for o in range(L):
                        for s in (1, -1):
                            for a in range(2, 31):
                                cases += 1
                                slots = {}
                                ok = True
                                for pos in crib_pos:
                                    i = pos - 1
                                    x = (t[pos] - s * int(d[(i + o) % L])) % 26
                                    if (i % a) in slots and slots[i % a] != x:
                                        ok = False; break
                                    slots[i % a] = x
                                if not ok:
                                    continue
                                survivors.append((a, rname, o, s, pa, ca, m))
                                for ka in ("std", "kry"):
                                    A = ALPHABETS[ka]
                                    word = "".join(A[slots[k]] if k in slots else "." for k in range(a))
                                    runs = [r for r in word.split(".") if len(r) >= 5]
                                    if runs:
                                        qs = sum(len(r) - 3 for r in runs)
                                        sc = sum(score(r) * (len(r) - 3) for r in runs) / qs
                                        if len(best) < 15 or sc > best[-1][0]:
                                            best.append((sc, a, rname, o, s, pa, ca, m, ka, word)); best.sort(reverse=True); best = best[:15]
                                    if collect and "." not in word:
                                        pool = set(w for w in vocab if len(w) == a)
                                        for tx in texts:
                                            for i in range(0, len(tx) - a + 1):
                                                pool.add(tx[i:i + a])
                                        if word in pool:
                                            key = {"word": word, "digits": d, "o": o, "s": s, "ka": ka, "pa": pa, "ca": ca, "m": m}
                                            pt = "".join(decrypt_letter(ct[i], STD[total_key(i, key)], pa, ca, "std", m) for i in range(N))
                                            candidates.append({"plaintext": pt, "key": key, "key_bits": 4.7 * a + 10, "key_description": f"word {word} + digits {rname} at {o}, s={s}; {pa}/{ca}/{ka} {m}"})
    return survivors, best, candidates, cases


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    vocab = list(ctx.vocabulary)
    texts = [letters(load_k1()["plaintext"]), letters(load_k2()["plaintext_as_carved"]), letters(load_k3()["plaintext"])]
    survivors, best, candidates, cases = search(ct, known, ctx.english_score, vocab, texts, True)
    nulls = []
    for seed in range(10):
        letters_ = list(ct); random.Random(seed).shuffle(letters_)
        _, nb, _, _ = search("".join(letters_), known, ctx.english_score, vocab, texts, False)
        nulls.append(round(nb[0][0], 3) if nb else None)
    by_len = {}
    for a, *_ in survivors:
        by_len[a] = by_len.get(a, 0) + 1
    return {
        "candidates": candidates[:50],
        "bounds": {"family": "word key plus known digit key (K2 coordinates), additive", "digit_readings": READINGS, "word_lengths": "2-30",
                   "alphabets": "plain and cipher in {std, kry}; word read in std or kry", "cases": cases,
                   "survivors_by_word_length": {str(k): v for k, v in sorted(by_len.items())},
                   "shortest_surviving_word_length": min(by_len) if by_len else None,
                   "best_forced_words": [{"score": round(sc, 3), "length": a, "reading": r, "offset": o, "s": s, "plain": pa, "cipher": ca, "mode": m, "word_alphabet": ka, "word": w} for sc, a, r, o, s, pa, ca, m, ka, w in best],
                   "shuffled_control_best": nulls, "vocab_matches": len(candidates)},
        "notes": f"{cases} cases; shortest surviving word length {min(by_len) if by_len else None}; best forced word {best[0][0]:.3f} vs shuffled best {max(x for x in nulls if x is not None):.3f}; {len(candidates)} matches.",
    }


def worked_example(ctx, key):
    d = READINGS["38 57 65 77 8 44"]
    lines = [f"digits {d} repeated under the message, alignment 0; KRYPTOS alphabet throughout, Vigenere; word length 7", "", "pos  plain  carved  total key  index  digit  word index  slot"]
    for pos in (22, 23, 24, 29, 30, 64):
        p, c = ctx.KNOWN[pos], ctx.K4[pos - 1]
        k = key_letter_for(p, c, "kry", "kry", "std", "vig"); idx = STD.index(k); dg = int(d[(pos - 1) % len(d)])
        lines.append(f"{pos:>3}    {p}      {c}        {k}        {idx:>2}      {dg}       {(idx - dg) % 26:>2}       {(pos-1) % 7}")
    lines.append("")
    lines.append("positions 22 and 29 share slot 0: their word indices must agree, or length 7 is dead at this alignment.")
    return "\n".join(lines)
