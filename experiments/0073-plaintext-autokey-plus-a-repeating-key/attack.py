"""Experiment 0073. See program.md for the contract."""

EXPERIMENT = {
    "slug": "plaintext-autokey-plus-a-repeating-key",
    "title": "The message as its own key, plus a repeating secret word on top",
    "family": "1-keyed-periodic",
    "parent": "0012-plaintext-autokey-chained-from-cribs",
    "changed": "Experiments 3 and 12 tested the autokey that feeds on the message itself, with no other key. The NSA's 1992 note named 'plain-text auto-key'. Here a repeating secret word is added on top, at every distance where two known letters can be compared and every word length, on the sculpture's table and on tables rebuilt from words.",
    "hypothesis_expert": (
        "Family 1, plaintext autokey as a component of a two-part key (C11a: NSA 1992 'plain-text auto-key', "
        "sources/nsa-foia-1992-2014-blackvault-compilation.txt; C5(b) 'key word/s'): T[i] = s*A(p[i-L]) + "
        "k[i mod P]. Only places where both p[i] and p[i-L] are known give equations: lags 1-12 inside "
        "EASTNORTHEAST, 1-10 inside BERLINCLOCK, 30-52 across them. Each such pair forces k at slot i mod P, "
        "and pairs sharing a slot must agree. Classes: plain, cipher and key alphabets standard or KRYPTOS, "
        "Vigenere or Beaufort, sign +1 or -1 (32 classes); plus one alphabet keyword-mixed from each "
        "vocabulary word, K1-K3 word and C13/C14 word (as in 0053) used on both sides, with the key read on it or on the standard alphabet "
        "(8 more per alphabet). Periods 1-96. Survivors tallied by redundant checks against ten shuffled "
        "coppers; no candidates (the key outside the pairs is unknown). Clue entries: C11a, C5(b)."
    ),
    "hypothesis_eli5": (
        "In a plaintext autokey cipher each letter is enciphered with the message letter a fixed distance "
        "back, so the message is its own key. Experiments 3 and 12 showed that alone does not fit. Here we "
        "add a repeating secret word on top. We can only test it where two known letters sit the right "
        "distance apart, but there are enough such pairs to get clear answers for many distances, and "
        "scrambled coppers show how many fits luck alone gives."
    ),
    "prediction": (
        "No case with three or more redundant checks survives beyond the shuffled-copper range; the lags "
        "7 and 21 named by the fingerprints and the NSA's 'interval 7' are no different. Zero candidates pass."
    ),
    "method": (
        "1. For each lag, list the pairs of known places that far apart. 2. For each class, the pair forces "
        "the secret word's letter in slot i mod P: total key minus the earlier message letter's value. "
        "3. For each period, check slots agree; tally survivors by redundant checks. 4. Repeat on ten "
        "shuffled coppers."
    ),
    "walkthrough": (
        "1. Lag 3, a 7-letter word, the sculpture's alphabet KRYPTOSABCDEFGHIJLMNQUVWXZ from K = 0, "
        "Vigenere. 2. Place 25: carved V (22) minus known T (4) is 18; the message letter 3 back is E (11); "
        "the word's letter is 18 - 11 = 7, in slot 3. 3. Place 32: carved K (0) minus known A (7) is -7, "
        "which is 19; 3 back is T (4); 19 - 4 = 15, also slot 3. 4. 7 and 15 disagree: lag 3 with a 7-letter "
        "word is dead under this way of using the table. 5. Repeat for every lag with known pairs, every word "
        "length and every way of using the table."
    ),
}

import random
from kryptos.alphabets import keyword_mixed
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY, load_k1, load_k2, load_k3

N = 97
ALPH = {"std": STD, "kry": KRY}
SPACED = (
    "BETWEEN SUBTLE SHADING AND THE ABSENCE OF LIGHT LIES THE NUANCE OF IQLUSION "
    "IT WAS TOTALLY INVISIBLE HOWS THAT POSSIBLE THEY USED THE EARTHS MAGNETIC FIELD X THE INFORMATION WAS GATHERED AND "
    "TRANSMITTED UNDERGRUUND TO AN UNKNOWN LOCATION X DOES LANGLEY KNOW ABOUT THIS THEY SHOULD ITS BURIED OUT THERE "
    "SOMEWHERE X WHO KNOWS THE EXACT LOCATION ONLY WW THIS WAS HIS LAST MESSAGE X THIRTY EIGHT DEGREES FIFTY SEVEN "
    "MINUTES SIX POINT FIVE SECONDS NORTH SEVENTY SEVEN DEGREES EIGHT MINUTES FORTY FOUR SECONDS WEST ID BY ROWS "
    "SLOWLY DESPARATLY SLOWLY THE REMAINS OF PASSAGE DEBRIS THAT ENCUMBERED THE LOWER PART OF THE DOORWAY WAS REMOVED "
    "WITH TREMBLING HANDS I MADE A TINY BREACH IN THE UPPER LEFT HAND CORNER AND THEN WIDENING THE HOLE A LITTLE I "
    "INSERTED THE CANDLE AND PEERED IN THE HOT AIR ESCAPING FROM THE CHAMBER CAUSED THE FLAME TO FLICKER BUT PRESENTLY "
    "DETAILS OF THE ROOM WITHIN EMERGED FROM THE MIST X CAN YOU SEE ANYTHING Q"
)
EXTRA = ["EGYPT", "CAIRO", "LUXOR", "WALL", "NOVEMBER", "MESSAGE", "DELIVER", "DELIVERING", "TRANSMIT"]


def letters(s):
    return "".join(c for c in s.upper() if "A" <= c <= "Z")


def word_alphabets(vocab):
    words = set(w for w in vocab if len(set(w)) >= 3)
    words |= {w for w in SPACED.split() if len(set(w)) >= 3} | set(EXTRA)      # the K1-K3 words and the C13/C14 words, as in 0053
    out, seen = {}, {STD, KRY}
    for w in sorted(words):
        a = keyword_mixed(w)
        if a not in seen:
            seen.add(a); out[w] = a
    return out


def setups(walph):
    for pa in ALPH:
        for ca in ALPH:
            for ka in ALPH:
                for mode in ("vig", "beau"):
                    for s in (1, -1):
                        yield f"{pa}/{ca}/{ka}/{mode}/{s}", ALPH[pa], ALPH[ca], ALPH[ka], mode, s
    for w, A in walph.items():
        for kname, K in (("same", A), ("std", STD)):
            for mode in ("vig", "beau"):
                for s in (1, -1):
                    yield f"{w}/{kname}/{mode}/{s}", A, A, K, mode, s


def sweep(ct, known, walph):
    tally, special, cases = {}, [], 0
    pos_known = sorted(known)
    for label, pa, ca, ka, mode, s in setups(walph):
        PI = {c: i for i, c in enumerate(pa)}; CI = {c: i for i, c in enumerate(ca)}; KI = {c: i for i, c in enumerate(ka)}
        for L in list(range(1, 13)) + list(range(30, 53)):
            d = []
            for pos in pos_known:
                if pos - L in known:
                    t = ((CI[ct[pos - 1]] - PI[known[pos]]) if mode == "vig" else (CI[ct[pos - 1]] + PI[known[pos]])) % 26
                    d.append((pos - 1, (t - s * KI[known[pos - L]]) % 26))
            if len(d) < 2:
                continue
            for P in range(1, 97):
                cases += 1
                slot = {}; ok = True
                for i, v in d:
                    if slot.setdefault(i % P, v) != v:
                        ok = False; break
                if ok:
                    c = len(d) - len(slot)
                    if c >= 1:
                        k = min(c, 6); tally[k] = tally.get(k, 0) + 1
                        if c >= 3 or L in (7, 21):
                            special.append({"setup": label, "lag": L, "period": P, "checks": c})
    return tally, special, cases


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    walph = word_alphabets(ctx.vocabulary)
    tally, special, cases = sweep(ct, known, walph)
    rng = random.Random(73)
    ctrl = []
    for _ in range(10):
        sh = list(ct); rng.shuffle(sh)
        t, _, _ = sweep("".join(sh), known, walph)
        ctrl.append(t)
        if ctx.time_left() < 40:
            break
    keys = sorted(set(tally) | {k for t in ctrl for k in t})
    table = {f"checks {k}{'+' if k == 6 else ''}": {"k4": tally.get(k, 0), "controls": [t.get(k, 0) for t in ctrl]} for k in keys}
    strong = [x for x in special if x["checks"] >= 3]
    return {
        "candidates": [],
        "bounds": {"family": "plaintext autokey plus a periodic key", "lags": "1-12 and 30-52 (where two known letters pair)",
                   "periods": "1-96", "setups": 32 + 8 * len(walph), "word_alphabets": len(walph), "cases": cases,
                   "survivors_by_checks": table, "survivors_3plus": strong[:40],
                   "lag7_lag21_survivors": [x for x in special if x["lag"] in (7, 21)][:30]},
        "notes": f"{cases:,} cases, {32 + 8 * len(walph)} setups. Survivors by checks, K4 (controls min-max): " + "; ".join(
            f"{k}: {v['k4']} ({min(v['controls'])}-{max(v['controls'])})" for k, v in table.items()) + f". Three or more checks: {len(strong)}.",
    }


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    I = {c: i for i, c in enumerate(KRY)}
    ct, kn = ctx.K4, ctx.KNOWN
    lines = ["lag 3, 7-letter word, sculpture's alphabet throughout, Vigenere", "", "place  known  carved  3 back  word letter  slot"]
    for pos in (25, 32, 26, 33):
        v = (I[ct[pos - 1]] - I[kn[pos]] - I[kn[pos - 3]]) % 26
        lines.append(f"{pos:>5}  {kn[pos]:>5}  {ct[pos - 1]:>6}  {kn[pos - 3]:>6}  {v:>11}  {(pos - 1) % 7:>4}")
    return "\n".join(lines)
