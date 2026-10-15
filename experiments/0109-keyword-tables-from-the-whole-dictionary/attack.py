"""Experiment 0109. See program.md for the contract."""

EXPERIMENT = {
    "slug": "keyword-tables-from-the-whole-dictionary",
    "title": "Tables built from any English word, not just the puzzle's, with a repeating key of length 1 to 26",
    "family": "1-keyed-periodic",
    "parent": "0053-periodic-tableau-k1-k3-word-alphabets",
    "changed": "0010 and 0053 rebuilt the tableau from the puzzle's own 61 words and the K1-K3 and 2025-letter words, the way KRYPTOS builds the carved one. Here the keyword is any of the 233,000 words of four letters or more in the project dictionary, used for the plain alphabet, the cipher alphabet or both (with the standard or KRYPTOS alphabet on the other side), with a repeating key of length 1-26 and no move.",
    "hypothesis_expert": (
        "Sanborn: a 'slightly different tableau' (C11a); K1-K2 use a keyword-mixed Quagmire III (KRYPTOS). 0005 closed "
        "periods 1-26 for the carved and standard alphabets, 0010 and 0053 for puzzle words. Alphabet W = keyword's "
        "distinct letters then the rest in order. Classes (consistency depends only on the plain and cipher alphabets and "
        "Beaufort versus not, 0006): (W, W), (W, STD), (STD, W), (W, KRY), (KRY, W), each Beaufort or not: 10 per word. "
        "Exact slot agreement at every period 1-26. Distinct alphabets only (words giving the same W counted once). Ten "
        "shuffled coppers. C8, C11a."
    ),
    "hypothesis_eli5": (
        "The table on Kryptos starts each alphabet with the word KRYPTOS and then the other letters in order. Any word "
        "can make such a table. Experiments 10 and 53 tried the puzzle's own words. Here we try every word in an English "
        "dictionary, about 233,000 of them, with a short repeating secret word on top, and ask whether any table lets "
        "the 24 known letters fit."
    ),
    "prediction": (
        "No word gives a consistent period below 20; the number of (alphabet, class) pairs consistent at each period "
        "21-26 lies inside the ten coppers' range. Zero candidates."
    ),
    "method": (
        "1. Build the distinct keyword alphabets from the dictionary. 2. For each alphabet and class, compute the key "
        "value forced at each known letter. 3. Test slot agreement at periods 1-26. 4. Count consistent pairs per period "
        "on K4 and ten shuffled coppers. 5. List K4's settings below period 20 and decrypt them."
    ),
    "walkthrough": (
        "1. Take a word, say SHADOW: the alphabet is SHADOWBCEFGIJKLMNPQRTUVXYZ. "
        "2. Use it for both the plain and cipher alphabets, Vigenere. "
        "3. Place 22: E is letter 8 of the new alphabet and F letter 9, so the key value there is 1. "
        "4. With a key of length p, places 22 and 22 + p (if known) must need the same key value. "
        "5. Repeat for every word, side, key length 1-26 and rule, and on scrambled coppers."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from pathlib import Path

N = 97
PMAX = 26
N_CONTROLS = 10
ROOT = Path(__file__).resolve().parent
if not (ROOT / "kryptos").exists():
    ROOT = Path.cwd()


def keyed(word):
    seen = []
    for c in word:
        if c not in seen:
            seen.append(c)
    return "".join(seen) + "".join(c for c in STD if c not in seen)


def slot_pairs(slots):
    last, prs = {}, []
    for e, s in enumerate(slots):
        if s in last:
            prs.append((last[s], e))
        last[s] = e
    return prs


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    places = sorted(known)
    pidx = [p - 1 for p in places]
    words = [w.strip().upper() for w in (ROOT / "kryptos" / "data" / "words.txt").read_text().split()]
    words = [w for w in words if len(w) >= 4 and w.isalpha()]
    alphas = {}
    for w in words:
        a = keyed(w)
        if a not in alphas and a not in (STD, KRY):
            alphas[a] = w
    rng = random.Random(109)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    T = len(texts)
    pairs = {p: slot_pairs([i % p for i in pidx]) for p in range(1, PMAX + 1)}
    live = [[0] * (PMAX + 1) for _ in range(T)]
    k4_low = []
    idx_std = {c: i for i, c in enumerate(STD)}; idx_kry = {c: i for i, c in enumerate(KRY)}
    n = 0
    for a, w in alphas.items():
        iw = {c: i for i, c in enumerate(a)}
        sides = [("W", iw, "W", iw), ("W", iw, "STD", idx_std), ("STD", idx_std, "W", iw), ("W", iw, "KRY", idx_kry), ("KRY", idx_kry, "W", iw)]
        for pn, PI, cn, CI in sides:
            P = [PI[known[q]] for q in places]
            for beau in (False, True):
                n += 1
                for t in range(T):
                    txt = texts[t]
                    f = [(CI[txt[j]] + P[e]) % 26 if beau else (CI[txt[j]] - P[e]) % 26 for e, j in enumerate(pidx)]
                    for p in range(1, PMAX + 1):
                        for x, y in pairs[p]:
                            if f[x] != f[y]:
                                break
                        else:
                            live[t][p] += 1
                            if t == 0 and p < 20:
                                k4_low.append({"word": w, "plain": pn, "cipher": cn, "beaufort": beau, "period": p})
        if ctx.time_left() < 60:
            break
    out = [p for p in range(1, PMAX + 1) if not (min(live[t][p] for t in range(1, T)) <= live[0][p] <= max(live[t][p] for t in range(1, T)))]
    first_k4 = next((p for p in range(1, PMAX + 1) if live[0][p]), None)
    first_ctl = [next((p for p in range(1, PMAX + 1) if live[t][p]), None) for t in range(1, T)]
    bounds = {"family": "keyword-mixed tableau from the whole dictionary, periodic key 1-26, no move",
              "words_4_plus": len(words), "distinct_alphabets": len(alphas), "settings": n,
              "k4_live_by_period": live[0][1:],
              "controls_live_min": [min(live[t][p] for t in range(1, T)) for p in range(1, PMAX + 1)],
              "controls_live_max": [max(live[t][p] for t in range(1, T)) for p in range(1, PMAX + 1)],
              "k4_smallest_live_period": first_k4, "controls_smallest_live_period": first_ctl,
              "periods_outside_control_range": out, "k4_live_below_20": k4_low[:40], "n_k4_live_below_20": len(k4_low),
              "controls": f"{N_CONTROLS} shuffled coppers (seed 109), identical search"}
    notes = (f"{len(alphas):,} distinct alphabets from {len(words):,} words x 10 classes = {n:,} settings, periods 1-26. "
             f"Smallest live period: K4 {first_k4}, controls {first_ctl}. K4 live below 20: {len(k4_low)}. Outside the "
             f"control range: {out}.")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    a = keyed("SHADOW"); I = {c: i for i, c in enumerate(a)}
    lines = [f"keyword SHADOW: alphabet {a}; both sides, Vigenere", "", "place  known  carved  key value"]
    for q in sorted(known):
        lines.append(f"{q:>5}  {known[q]:>5}  {ct[q - 1]:>6}  {(I[ct[q - 1]] - I[known[q]]) % 26:>9}")
    return "\n".join(lines)
