"""Experiment 0171 (F12.5). See program.md for the contract."""

EXPERIMENT = {
    "slug": "two-parts-with-their-own-keys",
    "title": "F12.5: K4 as two parts with their own repeating keys, split between the two known runs, on the sculpture's tables: exact, with the checks each part leaves",
    "family": "12-steins-way",
    "parent": "0005-quagmire-period-sweep-forced-keys",
    "changed": (
        "F12.5 (assumption A7: one key for the whole text). Stein found K1 and K2 used different keys in different parts "
        "of the panel. F12.2 and F12.4 found no break inside K4, so the split is at the known stretches: a first part "
        "holding EASTNORTHEAST and a second holding BERLINCLOCK, each with its own repeating key of length 1-26 on one of "
        "the 8 standard/KRYPTOS table classes. With separate keys the split point does not matter for consistency (a key's "
        "slots inside one run depend only on distances), and each run checks only keys shorter than itself: 13 letters "
        "check lengths 1-12, 11 letters check 1-10. The checks each length leaves are stated; ten scrambled coppers."
    ),
    "hypothesis_expert": (
        "Assumption A7 (knowledge/12-assumptions.md, for information), Stein 1999 (parts with their own keys: ABSCISSA "
        "and PALIMPSEST), C5(b) ('key word/s'). Model: c_i = T(p_i, k1[i mod a]) for i in part 1, T(p_i, k2[(i - s) mod b]) "
        "in part 2, T one of 8 classes (plain and cipher alphabets standard or KRYPTOS, Beaufort or not). Checks for part "
        "1 at length a: 13 - (distinct slots of places 22-34 mod a); part 2: 11 - (distinct slots of 64-74 mod b). A length "
        "is live if no slot holds two different forced key letters. Statistic: live (class, length) cells per part with at "
        "least one check, K4 against the coppers' range."
    ),
    "hypothesis_eli5": (
        "K1 and K2 used different secret words. Perhaps K4's two halves did too: one word for the part with EAST "
        "NORTHEAST, another for the part with BERLIN CLOCK. Then each known word can only test its own half's secret "
        "word, and only word lengths shorter than itself. We check every length that can be checked, on the sculpture's "
        "tables, and on scrambled copies."
    ),
    "prediction": "No length below 11-13 is live on K4 in either part at more than the coppers' rate (the periodic sweep 0005 already fails at these lengths with one key; separate keys loosen it only by the cross-run checks). Zero candidates.",
    "method": (
        "1. For each text, table class and part: the forced key value at each known place of that part. "
        "2. For lengths 1-12 (part 1) and 1-10 (part 2): live if each slot holds one value; count checks. "
        "3. Compare live cells on K4 with ten coppers."
    ),
    "walkthrough": (
        "1. Take EASTNORTHEAST at places 22-34 and a first secret word of length 5. "
        "2. Places 22 and 27 share a slot (27 - 22 = 5): on the table, E over F and O over Q must ask for the same key letter. "
        "3. Check every pair five apart inside the run, and the same for every length up to 12. "
        "4. Do the same for BERLINCLOCK with the second word, lengths up to 10. "
        "5. Repeat on scrambled copies."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N_CONTROLS = 10
ALPH = {"std": STD, "kry": KRY}
RUNS = {"part 1 (EASTNORTHEAST, 22-34)": (22, "EASTNORTHEAST"), "part 2 (BERLINCLOCK, 64-74)": (64, "BERLINCLOCK")}


def live_cells(text):
    out = {}
    for name, (start, word) in RUNS.items():
        for pa in ALPH:
            for ca in ALPH:
                for beau in (False, True):
                    P = {c: i for i, c in enumerate(ALPH[pa])}; C = {c: i for i, c in enumerate(ALPH[ca])}
                    f = [((C[text[start - 1 + j]] + P[ch]) if beau else (C[text[start - 1 + j]] - P[ch])) % 26 for j, ch in enumerate(word)]
                    for L in range(1, len(word)):
                        slots, ok = {}, True
                        for j in range(len(word)):
                            if slots.setdefault(j % L, f[j]) != f[j]:
                                ok = False
                                break
                        checks = len(word) - len({j % L for j in range(len(word))})
                        out[(name, f"{pa}/{ca}/{'beau' if beau else 'vig-var'}", L)] = (ok, checks)
    return out


def run(ctx):
    ct = ctx.K4
    rng = random.Random(1615)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    res = [live_cells(t) for t in texts]
    summary = {}
    for name, (start, word) in RUNS.items():
        k4 = sorted({L for (n, c, L), (ok, ch) in res[0].items() if n == name and ok and ch >= 1})
        cnt = [sum(1 for (n, c, L), (ok, ch) in r.items() if n == name and ok and ch >= 1) for r in res]
        summary[name] = {"k4_live_lengths": k4, "k4_live_cells": cnt[0], "coppers_live_cells": cnt[1:],
                         "checks_by_length": {L: len(word) - L for L in range(1, len(word))}}
    k4_live = [{"part": n, "class": c, "length": L, "checks": ch} for (n, c, L), (ok, ch) in res[0].items() if ok and ch >= 1]
    bounds = {"family": "two parts with separate repeating keys (split between the runs), standard/KRYPTOS tables, lengths up to the run length - 1",
              "summary": summary, "k4_live": k4_live, "controls": f"{N_CONTROLS} shuffled coppers (seed 1615)", "exhaustive": True}
    notes = "; ".join(f"{k}: K4 live lengths {v['k4_live_lengths']} ({v['k4_live_cells']} cells), coppers {min(v['coppers_live_cells'])}-{max(v['coppers_live_cells'])}" for k, v in summary.items())
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct = ctx.K4
    lines = ["part 1, sculpture's table (KRYPTOS alphabets), Vigenere: key value forced at each place of EASTNORTHEAST", ""]
    for j, ch in enumerate("EASTNORTHEAST"):
        q = 22 + j
        lines.append(f"place {q}: {ch} under {ct[q - 1]} -> key {(KRY.index(ct[q - 1]) - KRY.index(ch)) % 26:2d}, slot at length 5: {j % 5}")
    return "\n".join(lines)
