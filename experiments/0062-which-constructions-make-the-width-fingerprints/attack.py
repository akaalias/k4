"""Experiment 0062. See program.md for the contract."""

EXPERIMENT = {
    "slug": "which-constructions-make-the-width-fingerprints",
    "title": "Which ways of making a cipher leave the copper's two real fingerprints?",
    "family": "7-construction-simulation",
    "parent": "0056-width-7-and-21-fingerprints-look-elsewhere",
    "changed": "Experiment 56 showed the width-7 doublet column and the width-21 repeats are real, not artefacts of looking at many widths. This builds thousands of fake K4s from English by constructions that carry a 7 or a 21 in their structure, and counts how often each one leaves either fingerprint, or both.",
    "hypothesis_expert": (
        "Construction simulation (family 7, Oranchak's method) aimed at the two features 0056 confirmed: "
        "five of six doublets at one position mod 7, and 11 repeated pairs (c[i], c[i+21]). Plaintexts: "
        "97-letter windows of Carter's Tomb of Tut-ankh-Amen (the K3 source) and the K1-K3 plaintexts. "
        "Generators, each 4,000 samples, random keys, KRYPTOS alphabet: Vigenere at periods 7, 14, 21 and 28; "
        "plaintext autokey at lags 7 and 21 (C11a 'interval 7'); ciphertext autokey at lags 7 and 21; "
        "columnar transposition of width 7 or 21 after a period 27-29 Vigenere; the same transposition "
        "before it; and two calibrations, random letters and shuffles of K4. Statistics as in 0056: the "
        "fullest doublet column at width 7 as a share of doublets (5 of 6 or stronger: at least 4 doublets "
        "and at most one outside the column), and repeats at width 21 >= 11. Report each rate and the joint "
        "rate. Diagnostic: no candidates; the calibrations are the controls."
    ),
    "hypothesis_eli5": (
        "We now know the copper has two genuine oddities tied to the numbers 7 and 21. A good way to find "
        "out what made them is to make fake coppers ourselves, from real English, by different recipes that "
        "involve a 7 or a 21, and see which recipes leave the same marks. Random letters and scrambled "
        "copies of the real copper show how often the marks turn up by accident."
    ),
    "prediction": (
        "No construction leaves both fingerprints in more than 2% of samples. Vigenere or transposition "
        "with a 7 in it raises the doublet column, and those with a 21 raise the repeats, but not together. "
        "The calibrations show both marks below 1%."
    ),
    "method": (
        "1. Draw 97-letter English windows. 2. Encrypt each with each generator and a fresh random key. "
        "3. Compute the doublet column at width 7 and the repeats at width 21. 4. Count the share of samples "
        "with the column, with the repeats, and with both. 5. Compare with the calibrations."
    ),
    "walkthrough": (
        "1. Take a 97-letter stretch of Carter's book. 2. Pick a random secret word of 7 letters and encipher "
        "the stretch on the sculpture's table, letter by letter. 3. Find the doubled letters in the result "
        "and write it in rows of 7: note the fullest column. 4. Count how often a pair of letters 21 places "
        "apart repeats. 5. Do this four thousand times for each recipe and count how often both marks "
        "appear as strongly as on the copper."
    ),
}

import random
from collections import Counter
from pathlib import Path
from kryptos.facts import KRYPTOS_ALPHABET as KRY, load_k1, load_k2, load_k3
from kryptos.ciphers import columnar_transposition_encrypt

N = 97
ROOT = Path(__file__).resolve().parent


def letters(s):
    return "".join(c for c in s.upper() if "A" <= c <= "Z")


def encrypt(plaintext, key):
    return plaintext


def col_mark(t):
    dbl = [i for i in range(N - 1) if t[i] == t[i + 1]]
    if len(dbl) < 4:
        return False
    top = max(Counter(i % 7 for i in dbl).values())
    return len(dbl) - top <= 1 and top >= 4


def rep_mark(t):
    v = [t[i] + t[i + 21] for i in range(N - 21)]
    return len(v) - len(set(v)) >= 11


def vig(pt, key):
    return "".join(KRY[(KRY.index(p) + key[i % len(key)]) % 26] for i, p in enumerate(pt))


def pt_autokey(pt, lag, rng):
    prim = [rng.randrange(26) for _ in range(lag)]
    k = prim + [KRY.index(p) for p in pt]
    return "".join(KRY[(KRY.index(p) + k[i]) % 26] for i, p in enumerate(pt))


def ct_autokey(pt, lag, rng):
    out = []
    prim = [rng.randrange(26) for _ in range(lag)]
    for i, p in enumerate(pt):
        k = prim[i] if i < lag else KRY.index(out[i - lag])
        out.append(KRY[(KRY.index(p) + k) % 26])
    return "".join(out)


def rand_order(rng, w):
    o = list(range(w)); rng.shuffle(o); return o


def generators():
    g = {}
    for P in (7, 14, 21, 28):
        g[f"Vigenere, period {P}"] = lambda pt, rng, P=P: vig(pt, [rng.randrange(26) for _ in range(P)])
    for L in (7, 21):
        g[f"plaintext autokey, lag {L}"] = lambda pt, rng, L=L: pt_autokey(pt, L, rng)
        g[f"ciphertext autokey, lag {L}"] = lambda pt, rng, L=L: ct_autokey(pt, L, rng)
    for w in (7, 21):
        g[f"Vigenere 27-29 then columnar width {w}"] = lambda pt, rng, w=w: columnar_transposition_encrypt(vig(pt, [rng.randrange(26) for _ in range(rng.choice((27, 28, 29)))]), rand_order(rng, w))
        g[f"columnar width {w} then Vigenere 27-29"] = lambda pt, rng, w=w: vig(columnar_transposition_encrypt(pt, rand_order(rng, w)), [rng.randrange(26) for _ in range(rng.choice((27, 28, 29)))])
    return g


def run(ctx):
    ct = ctx.K4
    carter = letters((ROOT / "knowledge" / "sources" / "carter-1923-tomb-of-tutankhamen-vol1.txt").read_text(errors="ignore"))
    k123 = letters(load_k1()["plaintext"] + load_k2()["plaintext_as_carved"] + load_k3()["plaintext"])
    source = carter + k123
    rng = random.Random(62)
    S = 4000
    table = {}
    k4 = {"column": col_mark(ct), "repeats": rep_mark(ct)}
    gens = generators()
    gens["calibration: random letters"] = lambda pt, rng: "".join(rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(N))
    gens["calibration: shuffled K4"] = lambda pt, rng: "".join(rng.sample(ct, N))
    for name, g in gens.items():
        a = b = both = 0
        for _ in range(S):
            i = rng.randrange(0, len(source) - N)
            t = g(source[i:i + N], rng)
            ca, rb = col_mark(t), rep_mark(t)
            a += ca; b += rb; both += ca and rb
        table[name] = {"column": round(a / S, 4), "repeats": round(b / S, 4), "both": round(both / S, 4)}
        if ctx.time_left() < 120:
            break
    order = sorted(table.items(), key=lambda kv: -(kv[1]["both"] * 1000 + kv[1]["column"] + kv[1]["repeats"]))
    return {
        "candidates": [],
        "bounds": {"family": "construction simulation for the width-7 and width-21 fingerprints", "samples_per_generator": S,
                   "k4": k4, "plaintext_source": f"Carter vol. 1 ({len(carter):,} letters) and K1-K3", "rates": table},
        "notes": "Rates (column / repeats / both): " + "; ".join(f"{k}: {v['column']:.3f} / {v['repeats']:.3f} / {v['both']:.4f}" for k, v in order) + ".",
    }


def worked_example(ctx, key):
    t = ctx.K4
    return f"K4: doublet column mark {col_mark(t)}, width-21 repeat mark {rep_mark(t)}"
