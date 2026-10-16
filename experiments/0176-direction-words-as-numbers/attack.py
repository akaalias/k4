"""Experiment 0176 (F3.3). See program.md for the contract."""

EXPERIMENT = {
    "slug": "direction-words-as-numbers",
    "title": "F3.3: EAST NORTHEAST and its parts read as numbers (bearing 67.5 degrees, compass points of 32 and 16, mils) as the number half of a two-part key, with an unknown word, exact",
    "family": "3-two-component-key",
    "parent": "0175-morse-and-plate-numbers-as-key",
    "changed": (
        "F3.3 (A14(b)). Same decider as 0175, new readings: the known words' directions as numbers. EAST NORTHEAST as "
        "the bearing 67.5 degrees (6 7 5; 0 6 7 5; 67 5; 675; 67 30 as degrees and minutes; 1200 mils), as compass "
        "point 6 of 32 or 3 of 16 (and 7, 4 counting from 1), EAST as 90 degrees, point 8 of 32, 4 of 16, NORTHEAST as "
        "45 degrees, 4 of 32, 2 of 16; the pair EAST, NORTHEAST and the triple ENE, E, NE in each scale. Each sequence "
        "forward and reversed, every start, both signs, an unknown word of 1-24 letters, 12 table rules. Single numbers "
        "are a word shifted by a constant, which 0005's sweep already covers; they are run as a check of the decider."
    ),
    "hypothesis_expert": (
        "A14(b) (direction words as numbers, knowledge/12-assumptions.md, for information), C5(b) ('key word/s'), C6 "
        "(Scheidt's two-part keys), C15 (K2's 'six point five' bearing language). Model as 0175: carved = T(plain, k_i), "
        "k_i = w[i mod a] + s d[(i + o) mod m], 12 rules; the 24 known letters force k; w's slots must agree. Statistic: "
        "live settings by checks and dictionary words among forced words, K4 against 20 coppers."
    ),
    "hypothesis_eli5": (
        "The known words are directions. A direction is also a number: east-northeast is 67.5 degrees on a compass, or "
        "the 6th of 32 compass points. Perhaps such a number is half of the key and a secret word the other half. For "
        "every way of writing these numbers we ask the 24 known letters what the secret word would be, and compare with "
        "scrambled copies."
    ),
    "prediction": "No setting with 5 or more checks fits K4, as on the coppers; no dictionary word forced. Zero candidates.",
    "method": (
        "1. Build the direction readings. "
        "2. For each text, table rule, reading, start and sign: the word's value at each known place. "
        "3. For each word length 1-24: slot agreement; fully forced words looked up in the dictionary, every rotation. "
        "4. K4 against 20 coppers; one planted text as a builder check."
    ),
    "walkthrough": (
        "1. Write 6 7 5 (east-northeast is 67.5 degrees) again and again under the message, from some start. "
        "2. On the sculpture's table the known E at place 22 over the carved F asks for key value 1. "
        "3. Subtract the number under place 22: the rest is the secret word's letter for that slot. "
        "4. Places that share a slot of the word must leave the same rest. "
        "5. Every start, sign, word length and table rule; then scrambled copies."
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
    """name -> (sequence, kind); every sequence repeats with every alignment."""
    rep = {
        "ENE 67.5 degrees: 6 7 5": [6, 7, 5],
        "ENE 067.5: 0 6 7 5": [0, 6, 7, 5],
        "ENE 67 5": [67, 5],
        "ENE 675": [675],
        "ENE 67 degrees 30 minutes": [67, 30],
        "ENE 6 7 3 0": [6, 7, 3, 0],
        "ENE 1200 mils: 1 2 0 0": [1, 2, 0, 0],
        "ENE 12 0 0": [12, 0, 0],
        "ENE point 6 of 32": [6],
        "ENE point 7 of 32 (from 1)": [7],
        "ENE point 3 of 16": [3],
        "ENE point 4 of 16 (from 1)": [4],
        "E 90 degrees: 9 0": [9, 0],
        "E 90": [90],
        "NE 45 degrees: 4 5": [4, 5],
        "NE 45": [45],
        "E, NE degrees: 90 45": [90, 45],
        "E, NE digits: 9 0 4 5": [9, 0, 4, 5],
        "E, NE of 32: 8 4": [8, 4],
        "E, NE of 32 from 1: 9 5": [9, 5],
        "E, NE of 16: 4 2": [4, 2],
        "E, NE of 16 from 1: 5 3": [5, 3],
        "ENE, E, NE of 32: 6 8 4": [6, 8, 4],
        "ENE, E, NE of 16: 3 4 2": [3, 4, 2],
        "ENE, E, NE degrees: 67.5 90 45 as 6 7 5 9 0 4 5": [6, 7, 5, 9, 0, 4, 5],
    }
    r = {}
    for k, v in rep.items():
        r[k] = (v, "rep")
        if v[::-1] != v:
            r[k + ", reversed"] = (v[::-1], "rep")
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
    rng = random.Random(1760)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    # builder check: a planted text, 6 7 5 plus the word SHADOW on the sculpture's table
    PLANT_P = "USEDTHEEARTHSMAGNETICEASTNORTHEASTRMATIONWASGATHEREDANDTRANSMITBERLINCLOCKUNDTOANUNKNOWNLOCATIONX"
    PR = "ENE 67.5 degrees: 6 7 5"
    plant = encipher(PLANT_P, ("vig", "kry", "kry"), R[PR][0], 1, 1, [KRY.index(ch) for ch in "SHADOW"])
    lv, ph = scan(plant, {PR: R[PR]}, [("vig", "kry", "kry")], rots)
    plant_found = any(h["word"] == "SHADOW" and h["align"] == 1 for h in ph)

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
        "family": "word plus the direction words read as numbers, k = w[i mod a] + s d, 12 table rules, exact",
        "readings": {k: v[0] if v[1] == "rep" else "one value per K4 place" for k, v in R.items()},
        "n_readings": len(R), "word_lengths": [1, 24], "checks_by_word_length": CHECKS,
        "live_at_least_checks": table,
        "dictionary_hits": {"k4": hit_counts[0], "coppers": hit_counts[1:]},
        "dictionary_hits_6_plus": {"k4": long_hits[0], "coppers": long_hits[1:]},
        "k4_hits": k4_hits[:40],
        "plant": {"text": "6 7 5 from the second digit, + SHADOW, Vigenere on the KRYPTOS table", "found": plant_found},
        "copies": f"{N_CONTROLS} shuffled coppers (seed 1760)",
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
    d = [6, 7, 5]
    K = forced_k(ct, ("vig", "kry", "kry"))
    lines = ["6 7 5 (67.5 degrees) from the first digit, Vigenere on the KRYPTOS table, word length 7", "",
             "place  known  carved  key  num  word value  slot"]
    for e, q in enumerate(PLACES):
        dv = d[(q - 1) % 3]
        lines.append(f"{q:>5}  {KNOWN[q]:>5}  {ct[q - 1]:>6}  {K[e]:>3}  {dv:>3}  {(K[e] - dv) % 26:>10}  {(q - 1) % 7:>4}")
    return "\n".join(lines)
