"""Experiment 0157 (F1.11). See program.md for the contract."""

EXPERIMENT = {
    "slug": "split-key-phrase",
    "title": "F1.11: a split key phrase: its first part mixes the plain alphabet, its second the cipher alphabet, the whole phrase is the repeating key",
    "family": "1-keyed-periodic",
    "parent": "0123-two-free-alphabets-exact-at-every-key-length",
    "changed": (
        "F1.11 (added 2026-10-16 from Elementary Military Cryptography, 1935/1943, par. 59d: the key phrase CENTRAL AMERICA "
        "split into CENTRAL for one alphabet and AMERICA for the other, the whole phrase the key). 0123 showed two "
        "unknown alphabets admit K4 only at key lengths 8, 13, 16, 19, 20, 23, 24 and 26; here the alphabets and key are "
        "fixed by a phrase, so each phrase is one exact decryption. Phrases: every ordered pair of puzzle words, and every "
        "run of 2-4 consecutive words of the K1-K3 plaintexts split at each inner word boundary, of total length 3-30 (all "
        "lengths tried, not only 0123's eight, as a check)."
    ),
    "hypothesis_expert": (
        "C5(b) ('key word/s'), C6 (keys concealed at the sculpture, K1-K3 vocabulary), C7(a); source knowledge/sources "
        "(Elementary Military Cryptography par. 59d, per research_notes/Scheidt patents and field ciphers/"
        "addendum_downloaded_manuals.md). Model: plain alphabet P = keyword_mixed(part 1), cipher alphabet C = "
        "keyword_mixed(part 2), key = part 1 + part 2 repeating; key letters numbered by their place in C (the manual's "
        "rule: the key letter in the cipher component is set against the plain component's first letter), in P, or in "
        "the standard alphabet; rules Vigenere (C[P(p) + k]), Beaufort (C[k - P(p)]), variant (C[P(p) - k]). Exact: count "
        "the known letters each phrase reproduces. Ten scrambled coppers; statistic fixed before the run: phrases "
        "reproducing all 24 (a hit), and the best count on K4 against the coppers' best."
    ),
    "hypothesis_eli5": (
        "A wartime US Army manual describes a key phrase cut in two: the first half reorders the alphabet for the "
        "message, the second half reorders the alphabet for the carved letters, and the whole phrase is the repeating "
        "secret word. We try every pair of the puzzle's words and every short run of words from the first three "
        "messages as such a phrase, and count how many of the 24 known letters each one gives."
    ),
    "prediction": "No phrase reproduces all 24 known letters; K4's best count is inside the coppers' range (about 6-9 of 24). Zero candidates.",
    "method": (
        "1. Build the phrases. "
        "2. For each phrase, numbering and rule: decrypt the 24 known places and count matches. "
        "3. Same on 10 coppers; compare best counts; decrypt any full hit."
    ),
    "walkthrough": (
        "1. Take the phrase LAYER TWO: LAYER mixes the plain alphabet (LAYERBCDFG...), TWO the cipher alphabet (TWOABCDEFG...). "
        "2. The key is LAYERTWO, eight letters, repeated under the message. "
        "3. For a message letter, find its place in the plain alphabet, add the key letter's place in the cipher alphabet, and read the cipher alphabet there. "
        "4. Run it backwards at the 24 known places: does each carved letter give the known letter? "
        "5. Repeat for every phrase, the three numberings, the three rules, and scrambled copies."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.alphabets import keyword_mixed

N = 97
N_CONTROLS = 10
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
EXTRA = ["EGYPT", "CAIRO", "LUXOR", "WALL", "NOVEMBER", "MESSAGE", "DELIVER", "DELIVERING", "TRANSMIT", "LAYERTWO",
         "WONDERFULTHINGS", "BERLINWALL", "WELTZEITUHR", "ALEXANDERPLATZ", "SHADOWFORCES", "LUCIDMEMORY"]




def phrases(vocab):
    import json
    import re
    puzzle = sorted({w for w in SPACED.split() if len(w) >= 2} | {w.upper() for w in vocab if 2 <= len(w) <= 30} | set(EXTRA))
    out = set()
    for a in puzzle:
        for b in puzzle:
            if a != b and 3 <= len(a) + len(b) <= 30:
                out.add((a, b))
    words = SPACED.split()
    for n in (2, 3, 4):
        for i in range(len(words) - n + 1):
            run = words[i:i + n]
            for cut in range(1, n):
                a, b = "".join(run[:cut]), "".join(run[cut:])
                if 3 <= len(a) + len(b) <= 30:
                    out.add((a, b))
    return sorted(out)


def count(text, known, P, C, key, num, rule):
    Pi = {c: i for i, c in enumerate(P)}
    Ci = {c: i for i, c in enumerate(C)}
    Ni = {"C": Ci, "P": Pi, "S": {c: i for i, c in enumerate(STD)}}[num]
    L = len(key)
    hits = 0
    for q, a in known.items():
        k = Ni[key[(q - 1) % L]]
        c = Ci[text[q - 1]]
        v = {"vig": (c - k), "beau": (k - c), "var": (c + k)}[rule] % 26
        hits += P[v] == a
    return hits


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    ph = phrases(ctx.vocabulary)
    rng = random.Random(1411)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    best = [0] * len(texts)
    full = [[] for _ in texts]
    k4_top = []
    alph = {}
    for a, b in ph:
        P = alph.setdefault(a, keyword_mixed(a)); C = alph.setdefault(b, keyword_mixed(b)); key = a + b
        for num in ("C", "P", "S"):
            for rule in ("vig", "beau", "var"):
                for t, txt in enumerate(texts):
                    h = count(txt, known, P, C, key, num, rule)
                    if h > best[t]:
                        best[t] = h
                    if h == 24:
                        full[t].append((a, b, num, rule))
                    if t == 0 and h >= 9:
                        k4_top.append({"phrase": [a, b], "numbering": num, "rule": rule, "hits": h})
    cands = []
    for a, b, num, rule in full[0][:10]:
        P, C, key = keyword_mixed(a), keyword_mixed(b), a + b
        Pi, Ci = {c: i for i, c in enumerate(P)}, {c: i for i, c in enumerate(C)}
        Ni = {"C": Ci, "P": Pi, "S": {c: i for i, c in enumerate(STD)}}[num]
        pt = "".join(P[{"vig": (Ci[ct[i]] - Ni[key[i % len(key)]]), "beau": (Ni[key[i % len(key)]] - Ci[ct[i]]), "var": (Ci[ct[i]] + Ni[key[i % len(key)]])}[rule] % 26] for i in range(N))
        cands.append({"plaintext": pt, "key": {"plain": a, "cipher": b, "numbering": num, "rule": rule}})
    k4_top.sort(key=lambda d: -d["hits"])
    bounds = {"family": "split key phrase (EMC par. 59d): part 1 mixes the plain alphabet, part 2 the cipher alphabet, the whole phrase the key",
              "phrases": len(ph), "numberings": ["cipher alphabet", "plain alphabet", "standard"], "rules": ["vig", "beau", "var"],
              "k4_best_hits": best[0], "controls_best_hits": best[1:], "k4_full_hits": len(full[0]), "controls_full_hits": [len(f) for f in full[1:]],
              "k4_top": k4_top[:20], "controls": f"{N_CONTROLS} shuffled coppers (seed 1411)", "exhaustive": True}
    notes = f"{len(ph):,} phrases x 3 numberings x 3 rules: K4 best {best[0]}/24 (coppers {min(best[1:])}-{max(best[1:])}); full hits K4 {len(full[0])}, coppers {[len(f) for f in full[1:]]}"
    return {"candidates": cands, "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    P, C = keyword_mixed(key["plain"]), keyword_mixed(key["cipher"])
    k = key["plain"] + key["cipher"]
    Pi, Ci = {c: i for i, c in enumerate(P)}, {c: i for i, c in enumerate(C)}
    Ni = {"C": Ci, "P": Pi, "S": {c: i for i, c in enumerate(STD)}}[key["numbering"]]
    out = []
    for i, ch in enumerate(plaintext):
        kv, p = Ni[k[i % len(k)]], Pi[ch]
        out.append(C[{"vig": p + kv, "beau": kv - p, "var": p - kv}[key["rule"]] % 26])
    return "".join(out)


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    a, b = "LAYER", "TWO"
    P, C = keyword_mixed(a), keyword_mixed(b)
    k = a + b
    Ci = {c: i for i, c in enumerate(C)}
    lines = [f"phrase LAYER TWO: plain alphabet {P}, cipher alphabet {C}, key {k}", "", "place  carved  key  cipher place  key value  plain place  letter  known"]
    for q in (22, 23, 24, 64, 65):
        kv = Ci[k[(q - 1) % len(k)]]; c = Ci[ct[q - 1]]
        lines.append(f"{q:5d}  {ct[q - 1]:>6}  {k[(q - 1) % len(k)]:>3}  {c:>12}  {kv:>9}  {(c - kv) % 26:>11}  {P[(c - kv) % 26]:>6}  {known[q]:>5}")
    return "\n".join(lines)
