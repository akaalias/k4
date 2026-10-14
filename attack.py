"""Experiment 0011. See program.md for the contract."""

EXPERIMENT = {
    "slug": "progressive-key-period-sweep",
    "title": "A progressive key: the key word steps forward on every repeat, which revives the short periods",
    "family": "1-keyed-periodic",
    "parent": "0005-quagmire-period-sweep-forced-keys",
    "changed": "The periodic key gains a progression: on each repeat, or on each letter, every key letter moves a fixed number of places along the key alphabet. Periods 1 to 26 and 30 to 52, dead under a plain periodic key, are back in play.",
    "hypothesis_expert": (
        "Progressive-key Vigenere is in every hand-cipher manual Scheidt taught from (Friedman's Military "
        "Cryptanalysis, Part II; C5, C6): key index at position i is base[i mod P] plus d times the repeat "
        "number, or plus d times i for the letter-wise form. 0005 excluded periods 1-26 and 30-52 for d = 0 "
        "only. Here d runs 0-25, P 1-97, both progression forms, under the 24 conventions. For each "
        "combination the crib at position i forces base[(i mod P)] after the progression is subtracted; "
        "a conflict kills it. Survivors at P up to 30 get their forced base fragment matched against the "
        "vocabulary and K1-K3 windows; each match is decrypted and submitted. Stein's I.C. peak at 13 "
        "(C28) is a specific target: period 13 with any step. Bounds: complete for progressive periodic "
        "tableau systems under the stated conventions, periods and steps."
    ),
    "hypothesis_eli5": (
        "A repeating secret word was ruled out at most lengths because two known letters that would share "
        "the same letter of the word disagreed. But an old trick fixes that: each time the secret word "
        "repeats, every letter of it slides forward by a fixed amount. Then the two known letters no "
        "longer need to agree, they need to differ by that slide. We try every word length and every "
        "slide and ask which combinations the 24 known letters allow, and whether any of the puzzle's "
        "words fits what they force."
    ),
    "prediction": (
        "Most (period, step) pairs below 27 still die, because the cribs collide many times and a single "
        "step cannot reconcile them all. A scatter of survivors appears at periods 13 to 26 for some "
        "step under some convention, consistent with chance. No forced fragment matches a vocabulary "
        "word or K1-K3 window; zero candidates pass."
    ),
    "method": (
        "1. For each convention, period P, step d and progression form, compute for each crib the forced "
        "key index, subtract the progression, and reduce to the base slot. 2. A slot forced to two different "
        "letters kills the combination. 3. Count survivors per period. 4. For survivors with P up to 30, "
        "match the forced base fragment against the vocabulary and all K1-K3 windows of length P; decrypt "
        "and submit any match. 5. Record the survivor map by period and step."
    ),
    "walkthrough": (
        "1. Choose period 13 and step 1, per-repeat form, with the sculpture's alphabet throughout and "
        "Vigenere. 2. Position 22 is in repeat 1 (positions 14 to 26), slot 8. Its forced key letter, from "
        "E and F, is R, index 1 in KRYPTOS; subtract one step for repeat 1: index 0, K. 3. Position 35 "
        "would be slot 8 of repeat 2, but it is not a crib. Position 74, the K of CLOCK, is repeat 5, slot 8: "
        "its forced key letter K against ciphertext K is index 0; subtract 5 steps: index 21. 4. Slot 8 is "
        "now forced to two different letters, so period 13 with step 1 is dead under this convention. "
        "5. Try the other 25 steps and the other 23 conventions. 6. A survivor gives a pattern of forced "
        "base letters with blanks; slide the puzzle's words across it."
    ),
}

from kryptos.alphabets import ALPHABETS, conventions, key_letter_for, decrypt_letter, encrypt_letter
from kryptos.facts import load_k1, load_k2, load_k3

N = 97
MAX_KEY_PERIOD = 30


def letters(s):
    return "".join(c for c in s if "A" <= c <= "Z")


def key_letter_at(key, i, P, d, form, ka):
    A = ALPHABETS[ka]
    base = A.index(key[i % P])
    shift = d * (i // P) if form == "per-repeat" else d * i
    return A[(base + shift) % 26]


def encrypt(plaintext, key):
    pa, ca, ka, m, k, d, form = key["pa"], key["ca"], key["ka"], key["m"], key["key"], key["step"], key["form"]
    P = len(k)
    return "".join(encrypt_letter(p, key_letter_at(k, i, P, d, form, ka), pa, ca, ka, m) for i, p in enumerate(plaintext))


def decrypt(ciphertext, key):
    pa, ca, ka, m, k, d, form = key["pa"], key["ca"], key["ka"], key["m"], key["key"], key["step"], key["form"]
    P = len(k)
    return "".join(decrypt_letter(c, key_letter_at(k, i, P, d, form, ka), pa, ca, ka, m) for i, c in enumerate(ciphertext))


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    vocab = list(ctx.vocabulary)
    texts = [letters(load_k1()["plaintext"]), letters(load_k2()["plaintext_as_carved"]), letters(load_k3()["plaintext"])]
    convs = list(conventions())
    crib_pos = sorted(known)
    forced_idx = {}
    for conv in convs:
        pa, ca, ka, m = conv
        A = ALPHABETS[ka]
        forced_idx[conv] = {pos: A.index(key_letter_for(known[pos], ct[pos - 1], pa, ca, ka, m)) for pos in crib_pos}
    survivors = {}   # (form, P, d) -> number of conventions surviving
    frag_matches = []
    candidates = []
    checked = 0
    for form in ("per-repeat", "per-letter"):
        for P in range(1, N + 1):
            for d in range(26):
                alive = 0
                for conv in convs:
                    pa, ca, ka, m = conv
                    A = ALPHABETS[ka]
                    base = {}
                    ok = True
                    for pos in crib_pos:
                        i = pos - 1
                        shift = d * (i // P) if form == "per-repeat" else d * i
                        b = (forced_idx[conv][pos] - shift) % 26
                        slot = i % P
                        if slot in base and base[slot] != b:
                            ok = False; break
                        base[slot] = b
                    checked += 1
                    if not ok:
                        continue
                    alive += 1
                    if P <= MAX_KEY_PERIOD:
                        pool = set(w for w in vocab if len(w) == P)
                        for t in texts:
                            for s0 in range(0, len(t) - P + 1):
                                pool.add(t[s0:s0 + P])
                        for kw in pool:
                            if all(A.index(kw[s]) == b for s, b in base.items()):
                                key = {"pa": pa, "ca": ca, "ka": ka, "m": m, "key": kw, "step": d, "form": form}
                                frag_matches.append((form, P, d, kw, conv))
                                candidates.append({"plaintext": decrypt(ct, key), "key": key, "key_bits": 4.7 * P + 5,
                                                   "key_description": f"period {P} key {kw} step {d} {form}; {pa}/{ca}/{ka} {m}"})
                if alive:
                    survivors[(form, P, d)] = alive
    per_period = {}
    for (form, P, d), a in survivors.items():
        per_period.setdefault(P, {"per-repeat": 0, "per-letter": 0})[form] += 1
    short = {P: v for P, v in sorted(per_period.items()) if P <= 30}
    p13 = {f"{form} step {d}": a for (form, P, d), a in sorted(survivors.items()) if P == 13}
    return {
        "candidates": candidates[:50],
        "bounds": {"family": "progressive-key periodic tableau, separate alphabets", "conventions": 24,
                   "periods": "1-97", "steps": "0-25", "forms": ["per-repeat", "per-letter"],
                   "combinations_checked": checked,
                   "surviving_steps_by_period_up_to_30": {str(P): v for P, v in short.items()},
                   "period_13_survivors": p13,
                   "periods_with_no_survivor_any_step": [P for P in range(1, N + 1) if P not in per_period],
                   "fragment_matches": len(frag_matches),
                   "key_pool": f"vocabulary words and K1-K3 windows of length P for P <= {MAX_KEY_PERIOD}"},
        "notes": f"{checked} (form, period, step, convention) combinations; {len(frag_matches)} fragment matches submitted.",
    }


def worked_example(ctx, key):
    A = ALPHABETS["kry"]
    lines = ["period 13, step 1, per-repeat; plain/cipher/key all on the KRYPTOS alphabet, Vigenere", "",
             "pos  plain  cipher  forced key  index  repeat  minus step  base slot"]
    for pos in (22, 23, 24, 25, 26, 64, 65, 74):
        p, c = ctx.KNOWN[pos], ctx.K4[pos - 1]
        k = key_letter_for(p, c, "kry", "kry", "kry", "vig")
        idx = A.index(k); i = pos - 1; rep = i // 13; b = (idx - rep) % 26
        lines.append(f"{pos:>3}    {p}      {c}        {k}        {idx:>2}      {rep}        {b:>2} ({A[b]})     {i % 13}")
    lines.append("")
    lines.append("positions 22 and 74 share slot 8; their base letters must agree for period 13 step 1 to live.")
    return "\n".join(lines)
