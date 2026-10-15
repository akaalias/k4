"""Experiment 0074. See program.md for the contract."""

EXPERIMENT = {
    "slug": "letter-changing-masks-decimated-alphabets",
    "title": "A mask that changes letters: the alphabet counted in steps of 3, 5, 7 ... or backwards, before the table",
    "family": "2-masked-then-keyed",
    "parent": "0057-letter-nulls-outside-the-cribs",
    "changed": "Experiments 23 and 57 tried masks that only move or pad letters. Scheidt said he masked the English before the keyed step. The simplest masks that change letters replace each letter by the one a fixed number of steps along the alphabet (or backwards, like Atbash). Here every such mask, on the standard and the sculpture's alphabet, is put in front of a repeating key and in front of the self-feeding autokey.",
    "hypothesis_expert": (
        "Family 2, masks that change letters (C4(a): Scheidt 'I masked the English language... more than "
        "one stage', sources/kryptos-workshop-2015-scheidt-transcript.txt, npr-2005-scheidt-sanborn.txt). "
        "The simplest letter-changing masks are affine maps i -> a*i + b on a base alphabet (standard or "
        "KRYPTOS), a a unit mod 26 other than 1 (11 values; a = 25 with b = 25 is Atbash on the standard "
        "alphabet). Put before a tableau step, an affine mask is a decimated plain alphabet, and b is "
        "absorbed by the key, so the 22 decimated alphabets cover every affine mask. Pairings: decimated "
        "plain with standard, KRYPTOS or the same decimated cipher alphabet, and standard or KRYPTOS plain "
        "with a decimated cipher alphabet (mask after the table), Vigenere or Beaufort. Systems: (1) periodic "
        "key, periods 1-52; (2) ciphertext autokey with a constant, every lag, key letter on the plain, cipher, "
        "standard or KRYPTOS alphabet; (3) autokey plus a periodic key up to 26. Fragments at periods up to "
        "29 matched against words. Ten shuffled coppers. Clue entries: C4(a), C4(b)."
    ),
    "hypothesis_eli5": (
        "Scheidt said he 'masked' the English before the main step. A mask that changes letters could be as "
        "simple as replacing every letter by the one three, five or seven places further along the alphabet, "
        "counting round, or reading the alphabet backwards. Every such mask amounts to a reshuffled "
        "alphabet, so we try all of them, on the ordinary alphabet and on the sculpture's, in front of a "
        "repeating secret word and in front of the self-feeding autokey, and compare with scrambled coppers."
    ),
    "prediction": (
        "No pairing makes a periodic key of period 24 or less consistent; 25-26 at the shuffled-copper rate; "
        "no fragment matches a word; neither autokey form has a survivor with three or more checks beyond the "
        "controls. Zero candidates pass."
    ),
    "method": (
        "1. Build the 22 decimated alphabets. 2. For each pairing and mode, compute the key each known letter "
        "forces; check every period up to 52 and keep fragments. 3. Check the autokey residuals for every lag, "
        "alone and with a periodic key up to 26. 4. Repeat on ten shuffled coppers. 5. Match fragments against "
        "words."
    ),
    "walkthrough": (
        "1. Mask: read the ordinary alphabet backwards from A, AZYXWVUTSRQPONMLKJIHGFEDCB, so the message "
        "letter is counted on it. 2. Carved letters on the ordinary alphabet, Vigenere, a 7-letter word. "
        "3. Place 22: known E is 22nd on the backwards alphabet (from A = 0), carved F is 5; key 5 - 22 = -17, "
        "which is 9, J, slot 0. 4. Place 29: known T is 7, carved R is 17; key 10, K, slot 0. 5. J and K "
        "disagree: dead. 6. Repeat for every step size, base alphabet, pairing, period and lag."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY, load_k1, load_k2, load_k3

N = 97
PMAX = 52
UNITS = [3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]


def letters(s):
    return "".join(c for c in s.upper() if "A" <= c <= "Z")


def decimated():
    out = {}
    for bname, B in (("std", STD), ("kry", KRY)):
        for a in UNITS:
            out[f"{bname}x{a}"] = "".join(B[(a * i) % 26] for i in range(26))
    return out


def pairings(dec):
    for n, D in dec.items():
        yield f"{n}/std", D, STD
        yield f"{n}/kry", D, KRY
        yield f"{n}/{n}", D, D
        yield f"std/{n}", STD, D
        yield f"kry/{n}", KRY, D


def sweep(ct, items, dec, collect):
    per, auto, withp, frags = {}, {}, {}, []
    for label, pa, ca in pairings(dec):
        PI = {c: i for i, c in enumerate(pa)}; CI = {c: i for i, c in enumerate(ca)}
        for mode in ("vig", "beau"):
            T = [((CI[ct[pos - 1]] - PI[p]) if mode == "vig" else (CI[ct[pos - 1]] + PI[p])) % 26 for pos, p in items]
            for P in range(1, PMAX + 1):
                slot = {}; ok = True
                for (pos, _), t in zip(items, T):
                    if slot.setdefault((pos - 1) % P, t) != t:
                        ok = False; break
                if ok:
                    per[P] = per.get(P, 0) + 1
                    if collect and P <= 29:
                        frags.append((label, mode, P, "".join(ca[slot[k]] if k in slot else "." for k in range(P)),
                                      "".join(pa[slot[k]] if k in slot else "." for k in range(P))))
            for ka in {pa, ca, STD, KRY}:
                KI = {c: i for i, c in enumerate(ka)}
                for s in (1, -1):
                    for L in range(1, 97):
                        d = [(pos - 1, (t - s * KI[ct[pos - 1 - L]]) % 26) for (pos, _), t in zip(items, T) if pos - 1 - L >= 0]
                        if len(d) < 2:
                            continue
                        if len({v for _, v in d}) == 1:
                            c = min(len(d) - 1, 5); auto[c] = auto.get(c, 0) + 1
                        for P in range(2, 27):
                            slot = {}; ok = True
                            for i, v in d:
                                if slot.setdefault(i % P, v) != v:
                                    ok = False; break
                            if ok and len(d) - len(slot) >= 1:
                                c = min(len(d) - len(slot), 5); withp[c] = withp.get(c, 0) + 1
    return per, auto, withp, frags


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    items = sorted(known.items())
    dec = decimated()
    per, auto, withp, frags = sweep(ct, items, dec, True)
    rng = random.Random(74)
    ctrl = []
    for _ in range(10):
        sh = list(ct); rng.shuffle(sh)
        p2, a2, w2, _ = sweep("".join(sh), items, dec, False)
        ctrl.append((p2, a2, w2))
        if ctx.time_left() < 40:
            break
    vocab = [w for w in ctx.vocabulary if len(w) >= 5]
    texts = letters(load_k1()["plaintext"] + load_k2()["plaintext_as_carved"] + load_k3()["plaintext"])
    hits = []
    for label, mode, P, f1, f2 in frags:
        for f in (f1, f2):
            for run_ in f.split("."):
                if len(run_) >= 5 and (any(run_ in w or w in run_ for w in vocab) or run_ in texts):
                    hits.append({"pairing": label, "mode": mode, "period": P, "run": run_})
    def tab(k4, idx):
        keys = sorted(set(k4) | {k for c in ctrl for k in c[idx]})
        return {str(k): {"k4": k4.get(k, 0), "controls": [c[idx].get(k, 0) for c in ctrl]} for k in keys}
    pt, at, wt = tab(per, 0), tab(auto, 1), tab(withp, 2)
    short = lambda t, f=lambda P: True: {k: (v["k4"], min(v["controls"]), max(v["controls"])) for k, v in t.items() if f(k)}
    return {
        "candidates": [],
        "bounds": {"family": "affine (decimated-alphabet) masks before a periodic key, ciphertext autokey, or both",
                   "decimated_alphabets": len(dec), "pairings": 5 * len(dec), "periods": f"1-{PMAX}",
                   "periodic_consistent_by_period": pt, "autokey_constant_by_checks": at, "autokey_plus_periodic_by_checks": wt,
                   "fragments": len(frags), "word_matches": hits[:30]},
        "notes": f"{len(dec)} decimated alphabets, {5 * len(dec)} pairings. Periodic at P <= 26 (K4, control min, max): {short(pt, lambda P: int(P) <= 26)}. "
                 f"Autokey: {short(at)}. Autokey plus periodic: {short(wt)}. Word matches in {len(frags)} fragments: {len(hits)}.",
    }


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    pa = "".join(STD[(25 * i) % 26] for i in range(26))
    ct, kn = ctx.K4, ctx.KNOWN
    lines = [f"message on {pa}, carved letters on the ordinary alphabet, Vigenere, 7-letter key", "", "place  known  carved  key  slot"]
    for pos in (22, 29, 23, 30):
        lines.append(f"{pos:>5}  {kn[pos]:>5}  {ct[pos - 1]:>6}  {STD[(STD.index(ct[pos - 1]) - pa.index(kn[pos])) % 26]:>3}  {(pos - 1) % 7:>4}")
    return "\n".join(lines)
