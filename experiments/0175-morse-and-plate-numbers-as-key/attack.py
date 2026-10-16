"""Experiment 0175 (F3.2). See program.md for the contract."""

EXPERIMENT = {
    "slug": "morse-and-plate-numbers-as-key",
    "title": "F3.2: the Morse E counts and the plate's line lengths as the number half of a two-part key, each reading with an unknown word, exact",
    "family": "3-two-component-key",
    "parent": "0038-keyword-plus-dates-and-counts-from-the-story",
    "changed": (
        "F3.2. 0038 added an unknown word to 17 digit strings from the story, one of them the Morse E counts as the digits "
        "510179. Here each count is one key value (10 is ten, not 1 then 0), and the readings are listed in full from the "
        "two transcriptions of the Morse (knowledge/01-facts.md, Rumkin): the E runs in carved order, the E totals per "
        "message, both directions; and from the plate (knowledge/01-facts.md transcript): the 28 line lengths, their "
        "departures from 31, the lower plate's 14 alone, K4's own lines (4, 31, 31, 31), and two place readings: the line "
        "and the column of each K4 letter on the copper. 15 sequences, each forward and reversed where it repeats, every "
        "alignment, both signs, 12 table rules, word lengths 1-24."
    ),
    "hypothesis_expert": (
        "C25(b) (the Morse E counts as numbers), C5(b) ('key word/s'), C6 (Scheidt's two-part keys), A14-style layout "
        "readings (the plate's line lengths). Model: carved = T(plain, k_i), T one of 12 rules (Vigenere, Beaufort, "
        "variant; plain and cipher alphabets standard or KRYPTOS), k_i = w[i mod a] + s d[(i + o) mod m] for a repeating "
        "sequence d of length m (or d_i for a place reading), s = +-1, w an unknown word of length a. The 24 known letters "
        "force k at their places; w's slots must agree. Checks: 24 minus the slots the known places fill. Statistic: live "
        "settings by checks and dictionary words among fully forced words, K4 against 20 shuffled coppers."
    ),
    "hypothesis_eli5": (
        "The Morse code at the entrance is padded with single dots, read as the letter E, in little groups. The copper's "
        "lines are not all the same length. Either could be the number half of a key: a secret word for letters, these "
        "numbers added on top. For every way of reading the numbers, the 24 known letters tell us what the secret word "
        "would have to be; we check whether it can be one word at all, and whether it is English, and compare with "
        "scrambled copies."
    ),
    "prediction": "Live settings with 4 or more checks: K4 inside the coppers' range for every reading; no dictionary word of 4 or more letters forced on K4 beyond the coppers' rate. Zero candidates.",
    "method": (
        "1. Build the 15 readings. "
        "2. For each text, table rule and reading, alignment and sign: the word's value at each known place. "
        "3. For each word length 1-24: slot agreement; fully forced words looked up in the dictionary, every rotation, "
        "standard and KRYPTOS lettering. "
        "4. Count live settings by checks and hits; K4 against 20 coppers; one planted text as a builder check."
    ),
    "walkthrough": (
        "1. Take the E runs as carved: 2, 1, 6, 3, 2, 2, 5, 3, 1, 1, repeated under the message from some starting run. "
        "2. On the sculpture's table the known E at place 22 over the carved F asks for key value 1. "
        "3. Subtract the run number under place 22: what is left is the secret word's letter for that slot. "
        "4. With a 7-letter word, places 22 and 29 share a slot: the two leftovers must agree. "
        "5. Go through all 24 known letters for every word length, start and sign; a survivor's word is looked up. "
        "6. Repeat on scrambled copies."
    ),
}

import random
import time
from pathlib import Path

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY, KNOWN

N_CONTROLS = 20
ALPH = {"std": STD, "kry": KRY}
PLACES = sorted(KNOWN)
KP = [q - 1 for q in PLACES]
ROOT = Path(__file__).resolve().parent
if not (ROOT / "kryptos").exists():
    ROOT = Path.cwd()

LINES = [32, 31, 31, 30, 31, 32, 31, 31, 32, 31, 30, 31, 31, 31, 32, 30, 31, 30, 32, 30, 32, 31, 33, 29, 31, 31, 31, 31]


def readings():
    """name -> (sequence, kind) ; kind 'rep' repeats with every alignment, 'place' is one value per K4 place."""
    r = {}
    rep = {
        "Morse E runs, carved order (01-facts)": [2, 1, 6, 3, 2, 2, 5, 3, 1, 1],
        "Morse E runs, Rumkin": [2, 1, 5, 1, 3, 2, 2, 5, 3, 1],
        "Morse E totals per message (01-facts)": [9, 3, 9, 4, 1],
        "Morse E totals per message (Rumkin)": [9, 7, 10, 5, 1],
        "Morse E totals, Rumkin's listing order": [5, 10, 1, 7, 9],
        "plate line lengths, 28": LINES,
        "plate line lengths minus 31, 28": [x - 31 for x in LINES],
        "lower plate line lengths, 14": LINES[14:],
        "lower plate minus 31, 14": [x - 31 for x in LINES[14:]],
        "K4's lines 4, 31, 31, 31": [4, 31, 31, 31],
        "line length digits": [int(ch) for x in LINES for ch in str(x)],
        "Morse totals digits (Rumkin)": [int(ch) for x in [9, 7, 10, 5, 1] for ch in str(x)],
    }
    for k, v in rep.items():
        r[k] = (v, "rep")
        if v[::-1] != v and k != "K4's lines 4, 31, 31, 31":
            r[k + ", reversed"] = (v[::-1], "rep")
    line = [0 if i < 4 else 1 + (i - 4) // 31 for i in range(97)]
    col = [27 + i if i < 4 else (i - 4) % 31 for i in range(97)]
    r["line of each K4 letter on the plate"] = (line, "place")
    r["column of each K4 letter on the plate"] = (col, "place")
    r["plate line number (from the top of the lower plate)"] = ([10 + x for x in line], "place")
    return r


def forced_k(text, rule):
    mode, pa, ca = rule
    P = {c: i for i, c in enumerate(ALPH[pa])}; C = {c: i for i, c in enumerate(ALPH[ca])}
    out = []
    for q in PLACES:
        c, p = C[text[q - 1]], P[KNOWN[q]]
        out.append({"vig": (c - p) % 26, "beau": (c + p) % 26, "var": (p - c) % 26}[mode])
    return out


SLOTS = {a: [i % a for i in KP] for a in range(1, 25)}
CHECKS = {a: 24 - len(set(SLOTS[a])) for a in range(1, 25)}


def scan(text, R, rules, rots, collect=False):
    live = {}            # checks -> count
    hits = []
    for rule in rules:
        K = forced_k(text, rule)
        for name, (d, kind) in R.items():
            aligns = range(len(d)) if kind == "rep" else [0]
            for o in aligns:
                dv = [d[(i + o) % len(d)] for i in KP] if kind == "rep" else [d[i] for i in KP]
                for s in (1, -1):
                    wv = [(K[e] - s * dv[e]) % 26 for e in range(24)]
                    for a in range(1, 25):
                        if CHECKS[a] < 1:
                            continue
                        slot = [None] * a
                        ok = True
                        for e, sl in enumerate(SLOTS[a]):
                            if slot[sl] is None:
                                slot[sl] = wv[e]
                            elif slot[sl] != wv[e]:
                                ok = False
                                break
                        if not ok:
                            continue
                        live[CHECKS[a]] = live.get(CHECKS[a], 0) + 1
                        if a >= 4 and None not in slot:
                            for lab, A in ALPH.items():
                                w = "".join(A[v] for v in slot)
                                h = rots.get(a, {}).get(w)
                                if h:
                                    hits.append({"rule": "/".join(rule), "reading": name, "align": o, "sign": s, "a": a,
                                                 "lettering": lab, "word": h[0], "rotation": h[1], "checks": CHECKS[a]})
    return live, hits


def encipher(p, rule, d, o, s, w):
    mode, pa, ca = rule
    P = {c: i for i, c in enumerate(ALPH[pa])}; CA = ALPH[ca]
    out = []
    for i, ch in enumerate(p):
        k = (w[i % len(w)] + s * d[(i + o) % len(d)]) % 26
        x = P[ch]
        out.append(CA[{"vig": (x + k) % 26, "beau": (k - x) % 26, "var": (x - k) % 26}[mode]])
    return "".join(out)


def run(ctx):
    t0 = time.time()
    ct = ctx.K4
    R = readings()
    rules = [(m, pa, ca) for m in ("vig", "beau", "var") for pa in ALPH for ca in ALPH]
    words = [w.strip().upper() for w in (ROOT / "kryptos" / "data" / "words.txt").read_text().split()]
    rots = {}
    for w in words:
        if 4 <= len(w) <= 24 and w.isalpha():
            dd = rots.setdefault(len(w), {})
            for r in range(len(w)):
                dd.setdefault(w[r:] + w[:r], (w, r))
    rng = random.Random(1750)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    # builder check: a planted text, the Morse runs plus the word SHADOW on the sculpture's table
    PLANT_P = "USEDTHEEARTHSMAGNETICEASTNORTHEASTRMATIONWASGATHEREDANDTRANSMITBERLINCLOCKUNDTOANUNKNOWNLOCATIONX"
    plant = encipher(PLANT_P, ("vig", "kry", "kry"), R["Morse E runs, carved order (01-facts)"][0], 3, 1, [KRY.index(ch) for ch in "SHADOW"])
    lv, ph = scan(plant, {"Morse E runs, carved order (01-facts)": R["Morse E runs, carved order (01-facts)"]}, [("vig", "kry", "kry")], rots)
    plant_found = any(h["word"] == "SHADOW" and h["align"] == 3 for h in ph)

    res = [scan(t, R, rules, rots) for t in texts]
    maxc = max(CHECKS.values())

    def at_least(live, c):
        return sum(v for k, v in live.items() if k >= c)
    table = {}
    for c in (1, 2, 4, 6, 8, 11, 14):
        k4 = at_least(res[0][0], c); cp = [at_least(r[0], c) for r in res[1:]]
        table[c] = {"k4": k4, "coppers_min": min(cp), "coppers_max": max(cp), "coppers_at_or_above_k4": sum(1 for x in cp if x >= k4)}
    k4_hits = res[0][1]
    hit_counts = [len(r[1]) for r in res]
    long_hits = [sum(1 for h in r[1] if h["a"] >= 6) for r in res]
    cands = []
    for h in k4_hits[:20]:
        rule = tuple(h["rule"].split("/"))
        d = R[h["reading"]][0]
        mode, pa, ca = rule
        PA = ALPH[pa]; C = {c: i for i, c in enumerate(ALPH[ca])}
        A = ALPH[h["lettering"]]
        w = h["word"][h["rotation"]:] + h["word"][:h["rotation"]]
        kind = R[h["reading"]][1]
        pt = []
        for i, ch in enumerate(ct):
            dv = d[(i + h["align"]) % len(d)] if kind == "rep" else d[i]
            k = (A.index(w[i % len(w)]) + h["sign"] * dv) % 26
            c = C[ch]
            pt.append(PA[{"vig": (c - k) % 26, "beau": (k - c) % 26, "var": (c + k) % 26}[mode]])
        cands.append({"plaintext": "".join(pt), "key": h, "notes": f"{h['reading']}, word {h['word']}"})
    bounds = {
        "family": "word plus a number sequence from the Morse or the plate layout, k = w[i mod a] + s d, 12 table rules, exact",
        "readings": {k: v[0] if v[1] == "rep" else "one value per K4 place" for k, v in R.items()},
        "n_readings": len(R), "word_lengths": [1, 24], "checks_by_word_length": CHECKS,
        "live_at_least_checks": table,
        "dictionary_hits": {"k4": hit_counts[0], "coppers": hit_counts[1:]},
        "dictionary_hits_6_plus": {"k4": long_hits[0], "coppers": long_hits[1:]},
        "k4_hits": k4_hits[:40],
        "plant": {"text": "Morse runs from run 3, + SHADOW, Vigenere on the KRYPTOS table", "found": plant_found},
        "copies": f"{N_CONTROLS} shuffled coppers (seed 1750)",
        "seconds": round(time.time() - t0), "exhaustive": True,
    }
    notes = (f"live settings with >=4 checks: K4 {table[4]['k4']} (coppers {table[4]['coppers_min']}-{table[4]['coppers_max']}); "
             f"dictionary words 4+: K4 {hit_counts[0]} (coppers {min(hit_counts[1:])}-{max(hit_counts[1:])}); plant found {plant_found}")
    return {"candidates": cands, "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    R = readings()
    d = R[key["reading"]][0]
    A = ALPH[key["lettering"]]
    w = key["word"][key["rotation"]:] + key["word"][:key["rotation"]]
    return encipher(plaintext, tuple(key["rule"].split("/")), d, key["align"], key["sign"], [A.index(ch) for ch in w])


def worked_example(ctx, key):
    ct = ctx.K4
    d = [2, 1, 6, 3, 2, 2, 5, 3, 1, 1]
    K = forced_k(ct, ("vig", "kry", "kry"))
    lines = ["Morse E runs from the first run, Vigenere on the KRYPTOS table, word length 7", "",
             "place  known  carved  key  run  word value  slot"]
    for e, q in enumerate(PLACES):
        dv = d[(q - 1) % 10]
        lines.append(f"{q:>5}  {KNOWN[q]:>5}  {ct[q - 1]:>6}  {K[e]:>3}  {dv:>3}  {(K[e] - dv) % 26:>10}  {(q - 1) % 7:>4}")
    return "\n".join(lines)
