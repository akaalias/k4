"""Experiment 0180 (F3.7). See program.md for the contract."""

EXPERIMENT = {
    "slug": "point-as-numbers",
    "title": "F3.7: 'point' read as the decimal point in K2's six point five, or as punctuation (the copper's four ?, K2's ? and X stops), as the number half of a two-part key, exact",
    "family": "3-two-component-key",
    "parent": "0175-morse-and-plate-numbers-as-key",
    "changed": "F3.7 (C15(b)-(d)). 0072 used compass points and the letter's words as keyword alphabets. Here 'point' as numbers: the decimal point in K2's 'six point five' (6 5, 65, 6 0 5) and the coordinates with it (38 57 6 5 77 8 44 and variants; 0024 used their digits); as punctuation: the places of the four ? on the copper (in the 869, by line, within their lines), the ? in K2's plaintext and their gaps, K2's X stops and their gaps. Each forward and reversed, every start, both signs, an unknown word of 1-24 letters, 12 table rules (0175's decider). 'The point' as a place on the grounds needs a survey: blocked.",
    "hypothesis_expert": "C15: 'If they don't, then (CLUE) what's the point? Power resides with a secret' (Sanborn, August 2025); (b) the decimal point of K2's 'six point five', (c) a place, (d) punctuation, Scheidt's 'what's a period'. C5(b), C6. Model as 0175: k_i = w[i mod a] + s d[(i + o) mod m], 12 rules. Statistic: live settings, K4 against 20 coppers.",
    "hypothesis_eli5": "Sanborn's last clue asks 'what's the point?'. A point can be the decimal point in K2's 'six point five', or a punctuation mark such as the question marks on the copper or the X that ends K2's sentences. Their numbers and places could be half the key and a secret word the other half. The 24 known letters say whether any word fits.",
    "prediction": "No setting fits K4 or the coppers (5 or more checks each). Zero candidates.",
    "method": (
        "1. Build the readings. "
        "2. For each text, table rule, reading, start and sign: the word's value at each known place. "
        "3. For each word length 1-24: slot agreement; fully forced words looked up. "
        "4. K4 against 20 coppers; one planted text as a builder check."
    ),
    "walkthrough": "1. Write 6 5 (six point five) again and again under the message. 2. On the sculpture's table the known E at place 22 over the carved F asks for key value 1; subtract the number under it: the rest is the secret word's letter there. 3. Places sharing a slot of the word must agree. 4. Every start, sign, word length, table rule and reading; then scrambled copies.",
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
    import json
    k2 = json.load(open(ROOT / "data" / "k2.json"))["plaintext_as_carved"].upper()
    n, q = 0, []
    for ch in k2:
        if ch == "?":
            q.append(n)
        elif ch.isalpha():
            n += 1
    stops = [68, 138, 199, 251]               # the X stops in K2's plaintext (letters counted; not the X of EXACT, SIX)
    rep = {
        "six point five: 6 5": [6, 5],
        "six point five: 65": [65],
        "six point five with the point as 0: 6 0 5": [6, 0, 5],
        "K2 coordinates as numbers with the point: 38 57 6 5 77 8 44": [38, 57, 6, 5, 77, 8, 44],
        "K2 coordinates, seconds as 65: 38 57 65 77 8 44": [38, 57, 65, 77, 8, 44],
        "K2 coordinates, seconds as 6.5 rounded up: 38 57 7 77 8 44": [38, 57, 7, 77, 8, 44],
        "the four ? on the copper, places in the 869": [101, 227, 289, 772],
        "the four ?, lines 4 8 10 25": [4, 8, 10, 25],
        "the four ?, places in their lines 7 9 8 27": [7, 9, 8, 27],
        "the ? in K2's plaintext, letters before each": q,
        "gaps between the ? in K2's plaintext": [b - a for a, b in zip(q, q[1:])],
        "the X stops in K2's plaintext: 68 138 199 251": stops,
        "gaps between the X stops: 70 61 52": [b - a for a, b in zip(stops, stops[1:])],
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
    rng = random.Random(1800)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    # builder check: a planted text, the four ? on the copper, places in the 869 plus the word SHADOW on the sculpture's table
    PLANT_P = "USEDTHEEARTHSMAGNETICEASTNORTHEASTRMATIONWASGATHEREDANDTRANSMITBERLINCLOCKUNDTOANUNKNOWNLOCATIONX"
    PR = 'the four ? on the copper, places in the 869'
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
        "family": "word plus 'point' readings (decimal point, ? and X stops) as numbers, k = w[i mod a] + s d, 12 table rules, exact",
        "readings": {k: v[0] if v[1] == "rep" else "one value per K4 place" for k, v in R.items()},
        "n_readings": len(R), "word_lengths": [1, 24], "checks_by_word_length": CHECKS,
        "live_at_least_checks": table,
        "dictionary_hits": {"k4": hit_counts[0], "coppers": hit_counts[1:]},
        "dictionary_hits_6_plus": {"k4": long_hits[0], "coppers": long_hits[1:]},
        "k4_hits": k4_hits[:40],
        "plant": {"text": "the four ? places from the second, + SHADOW, Vigenere on the KRYPTOS table", "found": plant_found},
        "copies": f"{N_CONTROLS} shuffled coppers (seed 1800)",
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
    d = [6, 5]
    K = forced_k(ct, ("vig", "kry", "kry"))
    lines = ['6 5 (six point five) from the first number, Vigenere on the KRYPTOS table, word length 7', "",
             "place  known  carved  key  num  word value  slot"]
    for e, q in enumerate(PLACES):
        dv = d[(q - 1) % len(d)]
        lines.append(f"{q:>5}  {KNOWN[q]:>5}  {ct[q - 1]:>6}  {K[e]:>3}  {dv:>3}  {(K[e] - dv) % 26:>10}  {(q - 1) % 7:>4}")
    return "\n".join(lines)
