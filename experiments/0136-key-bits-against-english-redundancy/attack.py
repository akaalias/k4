"""Experiment 0136. See program.md for the contract."""

EXPERIMENT = {
    "slug": "key-bits-against-english-redundancy",
    "title": "Which undecided cells could any English test decide? Each blocked cell's key, in bits, against what 73 unknown letters of English can carry",
    "family": "1-keyed-periodic",
    "parent": "0120-one-free-alphabet-english-climb-at-23-and-26",
    "changed": (
        "F1.5, step 1 (exact). 0120's climb failed to recover planted texts, and every cell blocked for that reason "
        "(F1.1 Beaufort 23 and 26, F1.2's eight lengths, F1.4 on free alphabets, plaintext autokey at lags 53-96, F6.1, "
        "F6.2, F8's undecided Hill settings) was blocked by the climb's failure, not by a property of the cell. Here each "
        "cell's key is counted in bits and set against the redundancy of the 73 unknown letters: the harness's own "
        "quadgram model, measured on held-out English, and Shannon's two estimates for English. A cell whose key, after "
        "the 24 known letters, is larger than what 73 letters of English can pin down is blocked for good, with a number."
    ),
    "hypothesis_expert": (
        "No clue reading is tested; the experiment exists to turn the shared blocker of seven items into numbers (P6, "
        "issue #50). Unicity argument (Shannon 1949; Deavours 1977, cited by Bean, knowledge/sources/bean-2021-"
        "cryptodiagnosis-of-k4.txt, for Gromark's 48-letter unicity point): if a cell's key has H bits (uniform over a "
        "space of 2^H, after removing the symmetries that give the same decryption), about 2^(H - 24 log2 26) keys fit the "
        "24 known letters, and a test with redundancy D bits per letter on the 73 unknown letters expects 2^(R - 73 D) "
        "false keys to read as English as well as the true one, R = H - 112.8. R < 73 D is necessary for any English test "
        "to decide the cell; it is not sufficient for a search to find the key. Three values of D: (q) the harness's "
        "quadgram model, D = log2 26 minus its cross-entropy on held-out English (Carter's book, which is not the "
        "table's source; and the K1-K3 plaintexts), measured here; (S1) Shannon 1951 (Bell System Technical Journal 30, "
        "50-64), upper estimate 1.3 bits per character of 27-symbol text, about 1.6 bits per letter once spaces are "
        "dropped (5.5 characters per 4.5 letters), D = 3.1; (S0) his lower estimate 0.6 bits per character, about 0.73 per "
        "letter, D = 4.0: the most any English test could extract. Key bits per cell: a free alphabet log2 26! = 88.4; "
        "the affine re-labellings x -> m x + t of alphabet places (12 x 26, one alphabet; 12 x 26 x 26 for two) give the "
        "same decryption and are removed; a key letter 4.70; a choice among N options log2 N (27,852 type-1 moves, 5,054 "
        "hand-schedule partitions, 8 tables); a Hill matrix log2 |GL_n(Z26)| = log2 |GL_n(Z2)| + log2 |GL_n(Z13)|. "
        "Cells: F1.1 one free alphabet Beaufort L 23, 26; F1.2 two free alphabets L 8, 13, 16, 19, 20, 23, 24, 26; F1.4 "
        "hand schedules on one or two free alphabets, keyword 2-31; plaintext autokey lags 53-96 on the 8 standard/KRYPTOS "
        "tables; F6.1 one free alphabet with a move, L 6-26; F6.2 two free alphabets with a move, L 3-26; F8 5x5 affine "
        "Hill and 4x4 Hill plus a periodic key 1-26."
    ),
    "hypothesis_eli5": (
        "Some of the cipher settings we have tested cannot be ruled in or out by the 24 known letters alone: they fit "
        "the known letters, but so do scrambled copies of the carved text. Only the other 73 letters reading as English "
        "could tell a true setting from a false one. English is predictable, and that predictability is a fixed amount "
        "of information per letter. A setting with a very large secret (a scrambled alphabet plus a long key) has so "
        "many versions that some false version will read as English by luck, and then no test can pick the true one. "
        "Here we count, for each undecided setting, how big its secret is in bits, and compare it with how much 73 "
        "letters of English can say. Settings whose secret is too big are closed as undecidable for good."
    ),
    "prediction": (
        "A scratch check before this was written put the quadgram model's cross-entropy on Carter at 2.86 bits per "
        "letter, so D(q) about 1.8 and 73 letters carry about 134 bits. Then: F1.1 at 23 and 26 (R about 75 and 90) lie "
        "under every bound; F1.2 lies under the quadgram bound at 8, 13 and 16 and over it from 19 up, under Shannon's at "
        "every length; plaintext autokey lags 53-96 lie over the quadgram bound at every lag, and over even Shannon's "
        "lower estimate from about lag 86; F6.1 under the quadgram bound at every length; F6.2 under it to about length "
        "14; the 5x5 affine Hill and 4x4 Hill with any key up to 26 under it. So step 1 blocks for good only the long "
        "autokey lags, and step 2 (a climb with power) is what decides the rest. Zero candidates."
    ),
    "method": (
        "1. Measure the quadgram model's cross-entropy on held-out English: Carter's book (letters only) and the K1-K3 "
        "plaintexts; also the spread over 73-letter windows. "
        "2. For each blocked cell, count its key in bits, with the symmetries removed. "
        "3. Subtract the 112.8 bits the 24 known letters fix: the residual R. "
        "4. Compare R with 73 D for D from the quadgram model and from Shannon's two estimates. "
        "5. Classify each cell: decidable by the quadgram test in principle, only by a better English model, or by none."
    ),
    "walkthrough": (
        "1. Take one cell: one scrambled alphabet used on both sides, Beaufort form, a repeating key of 23 letters. "
        "2. Count the alphabet: 26! orders is 88.4 bits; relabelling its places by x -> m x + t (12 x 26 = 312 ways) gives the same decryption, so 88.4 - 8.3 = 80.1 bits. "
        "3. Count the key: 23 letters at 4.70 bits each, 108.1 bits. Total 188.2 bits. "
        "4. The 24 known letters each fix one letter in 26, 4.70 bits each, 112.8 bits: 75.4 bits of the secret are still open. "
        "5. Measure how much a letter of English tells the quadgram scorer: 4.70 bits minus its cross-entropy (about 2.9) is about 1.8 bits; 73 letters carry about 134 bits. "
        "6. 75.4 is less than 134, so a true answer of this kind would stand out from the false ones in principle; whether a search can find it is a separate question. "
        "7. Repeat for every blocked cell; a cell whose open bits exceed even Shannon's most generous figure for English is closed as undecidable."
    ),
}

import math
import re

N = 97
LOG26 = math.log2(26)
FIXED = 24 * LOG26                      # bits the 24 known letters fix
ALPHA = math.log2(math.factorial(26))   # a free alphabet
SYM1 = math.log2(12 * 26)               # affine relabelling of one alphabet's places
SYM2 = math.log2(12 * 26 * 26)          # two alphabets: common multiplier, two translations
MOVES = 27852                           # the type-1 library (0129-0133)
PARTITIONS = 3729 + 1325                # hand-schedule groupings (0127, 0128)
CARTER = "knowledge/sources/carter-1923-tomb-of-tutankhamen-vol1.txt"


def gl_bits(n):
    """log2 |GL_n(Z26)| = log2 |GL_n(Z2)| + log2 |GL_n(Z13)|."""
    tot = 0.0
    for q in (2, 13):
        tot += sum(math.log2(q ** n - q ** i) for i in range(n))
    return tot


def cond_model():
    from kryptos.scorer import _table
    logs, floor = _table()
    P = {k: 10 ** v for k, v in logs.items()}
    tri = {}
    for k, v in P.items():
        tri[k[:3]] = tri.get(k[:3], 0.0) + v
    fl = 10 ** floor
    return P, tri, fl


def bits_per_letter(text, model):
    """Cross-entropy of the quadgram model (conditional on the three letters before), bits per letter."""
    P, tri, fl = model
    s = 0.0
    for i in range(3, len(text)):
        q = text[i - 3:i + 1]
        s -= math.log2(P.get(q, fl) / (tri.get(q[:3], 0.0) + 26 * fl))
    return s / (len(text) - 3)


def cells():
    out = []
    one = ALPHA - SYM1
    two = 2 * ALPHA - SYM2
    for L in (23, 26):
        out.append(("F1.1", f"one free alphabet, Beaufort form, key length {L}", one + L * LOG26))
    for L in (8, 13, 16, 19, 20, 23, 24, 26):
        out.append(("F1.2", f"two free alphabets, key length {L}", two + L * LOG26))
    for n in (5, 10, 15, 20, 26, 31):
        out.append(("F1.4", f"hand schedule, one free alphabet, keyword of {n}", one + 1 + math.log2(PARTITIONS) + n * LOG26))
        out.append(("F1.4", f"hand schedule, two free alphabets, keyword of {n}", two + math.log2(PARTITIONS) + n * LOG26))
    for L in range(53, 97):
        out.append(("F1 autokey", f"plaintext autokey, lag {L}, one of 8 tables", 3 + L * LOG26))
    for L in (6, 10, 14, 18, 22, 26):
        out.append(("F6.1", f"one free alphabet with one of {MOVES:,} moves, either order, key length {L}", one + 2 + math.log2(MOVES) + L * LOG26))
    for L in (3, 6, 10, 12, 14, 15, 18, 22, 26):
        out.append(("F6.2", f"two free alphabets with one of {MOVES:,} moves, either order, key length {L}", two + 1 + math.log2(MOVES) + L * LOG26))
    out.append(("F8", "5x5 affine Hill, four numberings", gl_bits(5) + 5 * LOG26 + 2))
    for L in (1, 8, 13, 20, 26):
        out.append(("F8", f"4x4 Hill with a periodic key of {L}, either order, four numberings", gl_bits(4) + L * LOG26 + 3))
    return out


def run(ctx):
    import json
    model = cond_model()
    src = re.sub("[^A-Z]", "", open(CARTER, errors="ignore").read().upper())
    h_carter = bits_per_letter(src, model)
    k_texts = []
    for f in ("k1", "k2", "k3"):
        d = json.load(open(f"data/{f}.json"))
        pt = d.get("plaintext") or d.get("plaintext_as_carved") or ""
        k_texts.append(re.sub("[^A-Z]", "", pt.upper()))
    h_k = bits_per_letter("".join(k_texts), model)
    # spread over 73-letter windows (the evidence a true text would carry varies with the text)
    wins = []
    for s0 in range(1000, len(src) - 80, 2003):
        wins.append(bits_per_letter(src[s0:s0 + 76], model))     # 73 predicted letters after a 3-letter start
    wins.sort()
    D = {
        "q": LOG26 - h_carter,
        "q10": LOG26 - wins[int(0.9 * len(wins))],              # a text at the 10th percentile of predictability
        "S1": LOG26 - 1.3 * 5.5 / 4.5,
        "S0": LOG26 - 0.6 * 5.5 / 4.5,
    }
    rows = []
    for item, what, h in cells():
        R = h - FIXED
        cls = ("quadgram" if R < 73 * D["q"] else "better model" if R < 73 * D["S0"] else "none")
        rows.append({"item": item, "cell": what, "key_bits": round(h, 1), "open_bits": round(R, 1),
                     "margin_q": round(73 * D["q"] - R, 1), "margin_S1": round(73 * D["S1"] - R, 1),
                     "margin_S0": round(73 * D["S0"] - R, 1), "decidable_by": cls,
                     "letters_needed_q": round(max(R, 0) / D["q"], 1)})
    lag_q = [r for r in rows if r["item"] == "F1 autokey" and r["decidable_by"] == "quadgram"]
    lag_none = [int(r["cell"].split("lag ")[1].split(",")[0]) for r in rows if r["item"] == "F1 autokey" and r["decidable_by"] == "none"]
    lag_s1 = [int(r["cell"].split("lag ")[1].split(",")[0]) for r in rows if r["item"] == "F1 autokey" and r["margin_S1"] < 0]
    bounds = {
        "family": "bound, not a search: key bits of every blocked cell against the redundancy of 73 letters of English",
        "quadgram_cross_entropy_bits_per_letter": {"carter_book": round(h_carter, 3), "k1_k3_plaintexts": round(h_k, 3),
                                                   "carter_73_letter_windows": {"n": len(wins), "median": round(wins[len(wins) // 2], 3),
                                                                                "p10_least_predictable": round(wins[int(0.9 * len(wins))], 3),
                                                                                "p90_most_predictable": round(wins[int(0.1 * len(wins))], 3)}},
        "redundancy_bits_per_letter": {k: round(v, 3) for k, v in D.items()},
        "evidence_in_73_letters_bits": {k: round(73 * v, 1) for k, v in D.items()},
        "known_letters_fix_bits": round(FIXED, 1),
        "symmetries_removed_bits": {"one alphabet": round(SYM1, 2), "two alphabets": round(SYM2, 2)},
        "gl_bits": {"4x4": round(gl_bits(4), 1), "5x5": round(gl_bits(5), 1)},
        "cells": rows,
        "autokey_lags": {"quadgram_decidable": [int(r["cell"].split("lag ")[1].split(",")[0]) for r in lag_q],
                         "over_shannon_upper_estimate": lag_s1, "over_every_estimate": lag_none},
        "rule": "decidable by an English test with redundancy D only if open bits < 73 D (necessary, not sufficient for a search)",
        "exhaustive": True,
    }
    notes = (f"quadgram cross-entropy {h_carter:.3f} bits/letter on Carter ({h_k:.3f} on K1-K3), D(q) {D['q']:.2f}, "
             f"73 letters carry {73 * D['q']:.0f} bits (S1 {73 * D['S1']:.0f}, S0 {73 * D['S0']:.0f}); "
             f"cells by decider: " + ", ".join(f"{c} {sum(1 for r in rows if r['decidable_by'] == c)}" for c in ("quadgram", "better model", "none")))
    return {"candidates": [], "bounds": bounds, "notes": notes, "controls": []}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    one = ALPHA - SYM1
    h = one + 23 * LOG26
    model = cond_model()
    src = re.sub("[^A-Z]", "", open(CARTER, errors="ignore").read().upper())
    hq = bits_per_letter(src, model)
    dq = LOG26 - hq
    lines = [
        "cell: one unknown alphabet on both sides, Beaufort form, repeating key of 23 letters (F1.1)",
        "",
        f"  alphabet          log2 26!            = {ALPHA:6.1f} bits",
        f"  same decryption   x -> m x + t, 312   = -{SYM1:5.1f}",
        f"  key               23 x 4.70           = {23 * LOG26:6.1f}",
        f"  total                                 = {h:6.1f}",
        f"  24 known letters  24 x 4.70           = -{FIXED:5.1f}",
        f"  still open                            = {h - FIXED:6.1f} bits",
        "",
        f"  quadgram scorer: cross-entropy {hq:.2f} bits/letter on Carter, so {LOG26:.2f} - {hq:.2f} = {dq:.2f} bits of evidence per letter",
        f"  73 unknown letters x {dq:.2f}           = {73 * dq:6.1f} bits",
        "",
        f"  {h - FIXED:.1f} < {73 * dq:.1f}: decidable in principle by the quadgram test (margin {73 * dq - (h - FIXED):.1f} bits)",
        "",
        "  plaintext autokey at lag 86 on a fixed table: 86 x 4.70 + 3 = 407.2 bits, open 294.4,",
        f"  more than 73 letters carry even at Shannon's lowest entropy ({73 * (LOG26 - 0.6 * 5.5 / 4.5):.0f} bits): no English test can decide it",
    ]
    return "\n".join(lines)
