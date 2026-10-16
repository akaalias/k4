"""Experiment 0125. See program.md for the contract."""

EXPERIMENT = {
    "slug": "forced-key-as-running-english-on-dictionary-alphabets",
    "title": "If the key were running English text: do the key letters forced at EASTNORTHEAST and BERLINCLOCK read as English under any of the 208,062 dictionary-word alphabets, better than on scrambled coppers?",
    "family": "1-keyed-periodic",
    "parent": "0010-mixed-alphabets-forced-key-english",
    "changed": (
        "F1.3. 0009 and 0010 read the forced key stretches as English under the standard, KRYPTOS and 61 puzzle-word "
        "alphabets (best -3.81, the same as shuffled K4). Here every keyword alphabet from the project dictionary "
        "(208,062 distinct, as in 0109) is used as the plain alphabet, the cipher alphabet or both, under three table rules "
        "and two key alphabets (standard, or the same keyword alphabet): 18 readings per alphabet, 3.7 million per text. "
        "The best English score of the two forced stretches together is compared with 50 scrambled coppers searched "
        "identically, and 20 planted running keys measure power."
    ),
    "hypothesis_expert": (
        "C1(b) (the table alone), C27(c) (a different tableau), C5 ('key word/s', a running key from a named text). A "
        "running key from an English book on a keyword-mixed table: at each known place the key letter is forced, "
        "k = C(c) - P(p) (Vigenere), P(p) - C(c) (variant) or C(c) + P(p) (Beaufort), read through the key alphabet "
        "(standard or the keyword alphabet). The 13 forced letters at 22-34 and the 11 at 64-74 would then be two windows "
        "of English. Score: mean log10 quadgram over both windows (10 + 8 quadgrams, the harness's table). Alphabets: every "
        "word of four or more letters in kryptos/data/words.txt, keyword-mixed (repeats dropped, rest of the alphabet in "
        "order), standard and KRYPTOS excluded (0009); configurations (W, std), (std, W), (W, W). Exhaustive over this "
        "space. Controls: 50 shuffles of K4 (seed 125), identical search. Power: 20 planted texts, each a K4-length "
        "ciphertext made from a random English plaintext with the known letters in place, a running key from Carter's "
        "Tomb of Tut-ankh-Amen vol. 1 at a random offset, a random dictionary alphabet and configuration; a plant counts "
        "as found if its best score beats every copper. Tests reading C5 'a named text' for any text, without the text."
    ),
    "hypothesis_eli5": (
        "A running key uses the letters of a book as the key, one book letter per message letter. If K4 were made that "
        "way, then where we know the message (EASTNORTHEAST and BERLINCLOCK), working backwards gives 24 letters of the "
        "book itself, which would read as English. We try this with tables built from every word in an English "
        "dictionary, and compare the most English-looking result with what the same search finds on scrambled copies of "
        "the carved text, where no book is hidden."
    ),
    "prediction": (
        "K4's best combined score lies inside the range of the 50 coppers (the space is 3.7 million readings per text, "
        "and the best of that much noise reaches near-English on 24 letters). Power is low: fewer than half of the 20 "
        "planted running keys beat every copper, because a true 24-letter English window scores about -4.2 while the "
        "best of 3.7 million noise readings is expected near -4.0. If so, F1.3 is recorded blocked (the forced letters "
        "are too few to tell a running key from chance), not closed."
    ),
    "method": (
        "1. Build the 208,062 keyword alphabets. 2. For K4, 50 shuffled coppers and 20 plants: for every alphabet, "
        "configuration, rule and key alphabet, compute the 24 forced key letters and score the two windows. 3. Keep the "
        "best combined score and the best per window. 4. Compare K4 with the coppers; count the plants found."
    ),
    "walkthrough": (
        "1. Pick a dictionary word, say WINTER, and build its table alphabet: WINTER then the unused letters in order. "
        "2. Pick a rule, say Vigenere with WINTER on both sides. "
        "3. At place 22 the message has E and the copper F: key value = place of F minus place of E in that alphabet. "
        "4. Read the key value as a letter of the key alphabet. "
        "5. Do this for places 22-34 and 64-74: two strings of 13 and 11 key letters. "
        "6. Score both strings for English four-letter groups. "
        "7. Repeat for every word, side, rule and key alphabet; keep the best. "
        "8. Do the same with scrambled copies of K4 and compare."
    ),
}

import random
import re
from pathlib import Path
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
N_CONTROLS = 50
N_PLANTS = 20
ROOT = Path.cwd()
CARTER = "knowledge/sources/carter-1923-tomb-of-tutankhamen-vol1.txt"
STRETCHES = [(22, 34), (64, 74)]


def keyed(word):
    seen = []
    for c in word:
        if c not in seen:
            seen.append(c)
    return "".join(seen) + "".join(c for c in STD if c not in seen)


def alphabets():
    words = [w.strip().upper() for w in (ROOT / "kryptos" / "data" / "words.txt").read_text().split()]
    words = [w for w in words if len(w) >= 4 and w.isalpha()]
    out = {}
    for w in words:
        a = keyed(w)
        if a not in out and a not in (STD, KRY):
            out[a] = w
    return out


def quad_table():
    from kryptos.scorer import _table
    logs, floor = _table()
    tab = [floor] * (26 ** 4)
    for q, v in logs.items():
        if len(q) == 4 and q.isalpha() and q.isupper():
            tab[((ord(q[0]) - 65) * 26 + ord(q[1]) - 65) * 676 + (ord(q[2]) - 65) * 26 + ord(q[3]) - 65] = v
    return tab


CONFIGS = ("W-std", "std-W", "W-W")
RULES = ("vig", "var", "beau")
KEYALPHA = ("std", "W")


def forced(c_idx, p_idx, P, C, rule):
    """Key values at the known places given plain and cipher place maps (letter number -> place)."""
    if rule == "vig":
        return [(C[c] - P[p]) % 26 for c, p in zip(c_idx, p_idx)]
    if rule == "var":
        return [(P[p] - C[c]) % 26 for c, p in zip(c_idx, p_idx)]
    return [(C[c] + P[p]) % 26 for c, p in zip(c_idx, p_idx)]


def search(text, alist, tab):
    from kryptos.facts import KNOWN
    places = [q for a, b in STRETCHES for q in range(a, b + 1)]
    c_idx = [ord(text[q - 1]) - 65 for q in places]
    p_idx = [ord(KNOWN[q]) - 65 for q in places]
    ident = list(range(26))
    best = (-99.0, None)
    best1 = best2 = -99.0
    for a in alist:
        W = [ord(ch) - 65 for ch in a]
        posW = [0] * 26
        for i, le in enumerate(W):
            posW[le] = i
        for cfg in CONFIGS:
            P = posW if cfg[0] == "W" else ident
            C = posW if cfg.endswith("W") else ident
            for rule in RULES:
                k = forced(c_idx, p_idx, P, C, rule)
                for ka in KEYALPHA:
                    t = [W[v] for v in k] if ka == "W" else k
                    s1 = 0.0
                    for j in range(10):
                        s1 += tab[((t[j] * 26 + t[j + 1]) * 26 + t[j + 2]) * 26 + t[j + 3]]
                    s2 = 0.0
                    for j in range(13, 21):
                        s2 += tab[((t[j] * 26 + t[j + 1]) * 26 + t[j + 2]) * 26 + t[j + 3]]
                    sc = (s1 + s2) / 18
                    if sc > best[0]:
                        best = (sc, (a, cfg, rule, ka, "".join(chr(65 + v) for v in t)))
                    if s1 / 10 > best1:
                        best1 = s1 / 10
                    if s2 / 8 > best2:
                        best2 = s2 / 8
    return best, best1, best2


def make_plants(rng, alist, n):
    from kryptos.facts import KNOWN
    src = re.sub("[^A-Z]", "", open(CARTER, errors="ignore").read().upper())
    out = []
    for _ in range(n):
        s0 = rng.randrange(20000, len(src) - 400)
        pt = list(src[s0:s0 + N])
        for q, ch in KNOWN.items():
            pt[q - 1] = ch
        key = src[s0 + 200: s0 + 200 + N]
        a = rng.choice(alist); cfg = rng.choice(CONFIGS); rule = rng.choice(RULES); ka = rng.choice(KEYALPHA)
        W = [ord(ch) - 65 for ch in a]
        posW = {le: i for i, le in enumerate(W)}
        ident = {i: i for i in range(26)}
        P = posW if cfg[0] == "W" else ident
        C = posW if cfg.endswith("W") else ident
        Cinv = {v: k for k, v in C.items()}
        kinv = {le: i for i, le in enumerate(W)} if ka == "W" else ident
        ct = []
        for i in range(N):
            kv = kinv[ord(key[i]) - 65]
            pv = P[ord(pt[i]) - 65]
            cv = {"vig": (pv + kv) % 26, "var": (pv - kv) % 26, "beau": (kv - pv) % 26}[rule]
            ct.append(chr(65 + Cinv[cv]))
        ct = "".join(ct)
        truth = "".join(key[q - 1] for a_, b_ in STRETCHES for q in range(a_, b_ + 1))
        out.append((ct, truth, (a, cfg, rule, ka)))
    return out


def _job(args):
    kind, idx, text, truth = args
    from kryptos import facts  # noqa: F401
    tab = quad_table()
    alist = list(alphabets())
    (sc, rd), b1, b2 = search(text, alist, tab)
    return kind, idx, sc, rd, b1, b2, truth


def run(ctx):
    import multiprocessing as mp
    import sys, types
    ct = ctx.K4
    rng = random.Random(125)
    alist = list(alphabets())
    tab = quad_table()
    # validation: a planted running key must be found at its own setting with its true window
    plants = make_plants(rng, alist, N_PLANTS)
    for pc, truth, setting in plants[:2]:
        (sc, rd), _, _ = search(pc, [setting[0]], tab)
        assert rd[4] == truth, "plant check"
    jobs = [("k4", 0, ct, None)]
    for i in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); jobs.append(("copper", i, "".join(sh), None))
    for i, (pc, truth, setting) in enumerate(plants):
        jobs.append(("plant", i, pc, truth))
    if getattr(sys.modules.get(__name__), "_job", None) is not _job:
        m = types.ModuleType(__name__); m.__dict__.update(globals()); sys.modules[__name__] = m
    with mp.get_context("fork").Pool(8) as pool:
        res = pool.map(_job, jobs, chunksize=1)
    out = {"k4": None, "copper": [], "plant": []}
    for kind, idx, sc, rd, b1, b2, truth in res:
        row = {"score": round(sc, 4), "reading": rd, "best_east": round(b1, 4), "best_berlin": round(b2, 4)}
        if kind == "plant":
            ts = sum(tab[((ord(truth[j]) - 65) * 26 + ord(truth[j + 1]) - 65) * 676 + (ord(truth[j + 2]) - 65) * 26 + ord(truth[j + 3]) - 65] for j in list(range(10)) + list(range(13, 21))) / 18
            row["truth_window"] = truth; row["truth_score"] = round(ts, 4)
        if kind == "k4":
            out["k4"] = row
        else:
            out[kind].append(row)
    cs = [r["score"] for r in out["copper"]]
    top = max(cs)
    found = sum(1 for r in out["plant"] if r["score"] > top)
    found_truth = sum(1 for r in out["plant"] if r["truth_score"] > top)
    k4 = out["k4"]["score"]
    bounds = {
        "family": "running key from an unknown English text on keyword-mixed tables from the dictionary, no move",
        "alphabets": len(alist), "readings_per_alphabet": len(CONFIGS) * len(RULES) * len(KEYALPHA),
        "readings_per_text": len(alist) * 18, "exhaustive": True,
        "windows": "22-34 (13 letters) and 64-74 (11), scored together (18 quadgrams)",
        "k4": out["k4"], "coppers": out["copper"], "plants": out["plant"],
        "k4_rank_among_coppers": sum(1 for x in cs if x > k4) + 1,
        "coppers_range": [min(cs), top], "k4_above_all_coppers": k4 > top,
        "plants_found": found, "plants_whose_true_window_beats_every_copper": found_truth,
        "controls": f"{N_CONTROLS} shuffled coppers (seed 125), identical search",
    }
    notes = (f"K4 best {k4:.3f} ({out['k4']['reading']}); coppers {min(cs):.3f} to {top:.3f}; plants found {found}/{N_PLANTS} "
             f"(true windows above every copper: {found_truth}).")
    return {"candidates": [], "bounds": bounds, "notes": notes, "controls": cs}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    from kryptos.facts import KNOWN
    ct = ctx.K4
    a = keyed("WINTER")
    pos = {ch: i for i, ch in enumerate(a)}
    lines = [f"alphabet from WINTER: {a}; Vigenere, WINTER on both sides, key letters on the standard alphabet", "",
             "place  known  carved  key value  key letter"]
    for q in list(range(22, 35)) + list(range(64, 75)):
        v = (pos[ct[q - 1]] - pos[KNOWN[q]]) % 26
        lines.append(f"{q:5d}  {KNOWN[q]:>5}  {ct[q - 1]:>6}  {v:9d}  {STD[v]:>10}")
    return "\n".join(lines)
