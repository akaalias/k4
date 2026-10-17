"""Experiment 0181 (F2.1). See program.md for the contract."""

EXPERIMENT = {
    "slug": "struck-letter-fragments-against-words",
    "title": "F2.1: after striking out every copy of one or two letters, the plaintext a repeating key of 24 or 25 forces outside the known runs, matched against the dictionary",
    "family": "2-masked-then-keyed",
    "parent": "0057-letter-nulls-outside-the-cribs",
    "changed": (
        "F2.1, the gap 0057 left. 0057 struck every copy of one or two letters outside the known runs (351 masks) and "
        "found the smallest repeating key that fits, 24-27, as often as random strike-outs. It did not read what those "
        "keys force. Here, for every mask and every setting that fits at length 24 or 25 (12 table rules), the key "
        "letters the 24 known letters fix decrypt the other places in the same slots; the runs of forced letters "
        "outside the known runs are searched for dictionary words of 6 or more letters. Control: the same masks on ten "
        "copies that keep the carved letters at the 24 known places and shuffle the other 73 (each mask strikes the "
        "same number of letters)."
    ),
    "hypothesis_expert": (
        "Scheidt: 'I masked the English language' (C2); filler letters by letter are a hand masking device (F2). Model: "
        "carved letters of the struck set outside the runs are nulls; the rest is a periodic tableau cipher of period P "
        "on standard/KRYPTOS alphabets (Vigenere, Beaufort, variant). At P = 24, 25 the known letters fix most key "
        "slots, so most of the message is forced. Statistic: settings whose forced fragments hold a dictionary word of 6+ "
        "letters, and the longest such word, K4 against 10 kept-place copies under the same masks."
    ),
    "hypothesis_eli5": (
        "Perhaps some letters on the copper are fillers: every Q, say, to be ignored. 0057 struck them out and found a "
        "repeating secret word of 24 or 25 letters could still fit, but no more often than by chance. Such a long word is "
        "mostly fixed by the known letters, so it decrypts most of the rest of the message. We read those decrypted "
        "pieces and look for real words, and do the same on scrambled copies."
    ),
    "prediction": "Settings with a 6+ letter word in the forced fragments: K4 inside the copies' range; the longest word no longer than on copies. Zero candidates.",
    "method": (
        "1. For each mask (351) and text: strike the letters, renumber the known places. "
        "2. For each of 12 table rules and P = 24, 25: if the forced key values agree, decrypt every place whose slot is "
        "forced. "
        "3. Search the forced runs outside the known runs for dictionary words of 6-15 letters. "
        "4. K4 against 10 kept-place copies."
    ),
    "walkthrough": (
        "1. Strike every Q outside the known runs; BERLINCLOCK moves left by the number struck before it. "
        "2. On the sculpture's table, at key length 24, each known letter fixes the key letter of its slot. "
        "3. Every other place in a fixed slot can now be read. "
        "4. Look along those readings, away from the known words, for real words of 6 letters or more. "
        "5. Do the same on scrambled copies."
    ),
}

import random
from itertools import combinations
from pathlib import Path

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY, KNOWN

N_CONTROLS = 10
ALPHAS = {"std": STD, "kry": KRY}
RANGES = set(range(22, 35)) | set(range(64, 75))
ROOT = Path(__file__).resolve().parent
if not (ROOT / "kryptos").exists():
    ROOT = Path.cwd()


def settings(ct, removed, words, minlen=6):
    """Yield (rule, P, longest word, words found, forced text) for each fitting setting at P 24, 25."""
    keep = [i for i in range(1, len(ct) + 1) if i not in removed]
    newpos = {old: new for new, old in enumerate(keep, start=1)}
    text = "".join(ct[i - 1] for i in keep)
    known_new = {newpos[q]: p for q, p in KNOWN.items()}
    crib_new = set(known_new)
    out = []
    for pa_n, pa in ALPHAS.items():
        for ca_n, ca in ALPHAS.items():
            for mode in ("vig", "beau", "var"):
                for P in (24, 25):
                    slot = {}
                    ok = True
                    for q, p in known_new.items():
                        c = ca.index(text[q - 1]); x = pa.index(p)
                        v = {"vig": (c - x) % 26, "beau": (c + x) % 26, "var": (x - c) % 26}[mode]
                        if slot.setdefault((q - 1) % P, v) != v:
                            ok = False
                            break
                    if not ok:
                        continue
                    pt = []
                    for q in range(1, len(text) + 1):
                        s = (q - 1) % P
                        if s not in slot or q in crib_new:
                            pt.append(".")
                            continue
                        c = ca.index(text[q - 1]); v = slot[s]
                        pt.append(pa[{"vig": (c - v) % 26, "beau": (v - c) % 26, "var": (c + v) % 26}[mode]])
                    forced = "".join(pt)
                    found = []
                    for run in forced.split("."):
                        for a in range(len(run)):
                            for b in range(a + minlen, min(len(run), a + 15) + 1):
                                if run[a:b] in words:
                                    found.append(run[a:b])
                    longest = max((len(w) for w in found), default=0)
                    out.append((f"{mode}/{pa_n}/{ca_n}", P, longest, found, forced))
    return out


def run(ctx):
    ct = ctx.K4
    words = {w.strip().upper() for w in (ROOT / "kryptos" / "data" / "words.txt").read_text().split() if 6 <= len(w.strip()) <= 15}
    outside = [i for i in range(1, len(ct) + 1) if i not in RANGES]
    rng = random.Random(1810)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = [ct[i - 1] for i in outside]
        rng.shuffle(sh)
        t = list(ct)
        for i, ch in zip(outside, sh):
            t[i - 1] = ch
        texts.append("".join(t))
    masks = [(L,) for L in STD] + list(combinations(STD, 2))
    fits = [0] * len(texts)
    with_word = [0] * len(texts)
    longest = [0] * len(texts)
    k4_best = []
    for ti, t in enumerate(texts):
        for m in masks:
            removed = {i for i in outside if t[i - 1] in m}
            for rule, P, lw, found, forced in settings(t, removed, words):
                fits[ti] += 1
                if lw:
                    with_word[ti] += 1
                    longest[ti] = max(longest[ti], lw)
                    if ti == 0:
                        k4_best.append({"mask": "".join(m), "rule": rule, "P": P, "longest": lw,
                                        "words": sorted(set(found), key=len, reverse=True)[:6], "forced": forced})
        if ctx.time_left() < 60:
            break
    k4_best.sort(key=lambda z: -z["longest"])
    bounds = {
        "family": "letter nulls (every copy of one or two letters outside the runs), then a periodic tableau at P 24, 25; forced plaintext outside the runs read for words",
        "masks": len(masks), "rules": 12, "periods": [24, 25], "min_word": 6,
        "fitting_settings": {"k4": fits[0], "copies": fits[1:]},
        "settings_with_a_word": {"k4": with_word[0], "copies": with_word[1:]},
        "longest_word": {"k4": longest[0], "copies": longest[1:]},
        "k4_examples": k4_best[:15],
        "copies": f"{N_CONTROLS} copies keeping the 24 known places, other 73 shuffled (seed 1810), same masks",
        "exhaustive": True,
    }
    notes = (f"fitting settings K4 {fits[0]} (copies {min(fits[1:])}-{max(fits[1:])}); with a 6+ letter word K4 {with_word[0]} "
             f"(copies {min(with_word[1:])}-{max(with_word[1:])}); longest K4 {longest[0]} (copies {min(longest[1:])}-{max(longest[1:])})")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct = ctx.K4
    qs = [i + 1 for i, c in enumerate(ct) if c == "Q"]
    struck = [i for i in qs if i not in RANGES]
    return f"Q at {qs}; struck outside the known runs: {struck}; BERLINCLOCK moves from 64-74 to {64 - len(struck)}-{74 - len(struck)}"
