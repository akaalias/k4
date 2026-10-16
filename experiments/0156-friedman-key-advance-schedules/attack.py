"""Experiment 0156 (F1.10). See program.md for the contract."""

EXPERIMENT = {
    "slug": "friedman-key-advance-schedules",
    "title": "F1.10: Friedman's keyword-only key-advance schedules (run length by letter value, the CHRISTMAS expansion, EXTINGUISHER windows; ciphertext and plaintext interruptors; fraction-digit runs) on the sculpture's tables, exact, with scrambled copies",
    "family": "1-keyed-periodic",
    "parent": "0126-hand-key-schedules-listed-and-tested",
    "changed": (
        "F1.10. The report on Scheidt's patents and field ciphers ran scratch checks without controls showing no "
        "dictionary word fits the run-length and CHRISTMAS schedules on the standard or KRYPTOS tables, and no "
        "ciphertext-interruptor setting fits; the fraction-digit runs and the plaintext interruptor were untested, and "
        "TM 32-220 par. 126d's EXTINGUISHER windows were found later. Here all six, as an experiment with ten scrambled "
        "copies. Word schedules (each dictionary word gives one key): run length = the key letter's value (A = 1; and A = 0 "
        "with zero-length runs skipped), the CHRISTMAS expansion (sections ending at the letters numbered 1, 2, 3, ...), "
        "EXTINGUISHER windows of 2-5 letters. Free-letter schedules (key letters unknown, the 24 known letters force them): "
        "ciphertext interruptor (the key restarts after each occurrence of a chosen carved letter), plaintext interruptor "
        "(restarts after a chosen message letter; testable only inside the two known runs, each run starting at an unknown "
        "key place), fraction digits (each key letter used for as many letters as the next digit of 1/d, d 3-99, zeros "
        "dropped). Tables: plain and cipher alphabets standard or KRYPTOS, Vigenere, Beaufort or variant, key letters "
        "numbered on either alphabet."
    ),
    "hypothesis_expert": (
        "C5(a) ('simple, can be remembered... with the correct key word/s', Scheidt 2011 via Bean), C20 (hand schedules), "
        "F1.4's list extended. Sources: Friedman, Military Cryptanalysis III §16b, §19, §21, §35c-d; TM 32-220 pars. "
        "125-126 (126b plaintext interruptor, 126d EXTINGUISHER windows, 126e fraction 1/7), 89e (zeros dropped); "
        "reports/Scheidt patents and field ciphers.md and research_notes/Scheidt patents and field ciphers/"
        "addendum_downloaded_manuals.md. Note from the report: adjacent known pairs 26-27 (N, O under Q), 33-34 (T, S under "
        "S), 68-69 (I, N under T) can never share an alphabet. Word list kryptos/data/words.txt (234,428 words; lengths "
        "3-20 used). EXTINGUISHER: windows W[t:t+m] cycled within a group whose length is the next number of W's "
        "alphabetical numbering (ties left to right), windows and numbers each cycling. Exact; statistic fixed before the "
        "run: per schedule, K4's count (word hits, or consistent free settings with at least one check) against ten "
        "coppers' range."
    ),
    "hypothesis_eli5": (
        "A wartime US Army training text lists simple rules for when the secret word's next letter comes into use: "
        "each letter used for as many places as its position in the alphabet, the word expanded by a counting rule, the "
        "word restarted whenever a chosen letter appears, run lengths taken from the digits of a fraction, or "
        "overlapping three-letter windows of the word. Each needs only a word and a rule anyone can remember. We test "
        "every rule with every dictionary word (or with the word's letters left unknown) on the sculpture's tables, "
        "against the 24 known letters and against scrambled copies of the carved text."
    ),
    "prediction": (
        "No dictionary word fits any word schedule on K4 (as the report's scratch checks found), coppers 0 as well; the "
        "free-letter schedules fit K4 only at the coppers' rate, the plaintext interruptor most often (few checks inside "
        "the runs). Zero candidates."
    ),
    "method": (
        "1. For each word schedule and word: the key letter at each known place (positions 22-34, 64-74). "
        "2. For each text, table and numbering: the forced key value at each known place; a word fits if its 24 values "
        "match exactly (hash lookup). "
        "3. Free schedules: the slot of each known place per setting; a setting is consistent if no slot has two "
        "different forced values; count those with a check. "
        "4. K4 against the coppers per schedule."
    ),
    "walkthrough": (
        "1. Run length by value: with the word KEY, K (11th letter) is used for 11 places, E for 5, Y for 25, then K again. "
        "2. Count along to place 22: which letter of the word is in use there, and at every other known place. "
        "3. On the sculpture's table, the known letter and the carved letter at each place fix the key letter that must be in use. "
        "4. The word fits only if it puts exactly those letters there, at all 24 places. "
        "5. The other rules work the same way, with their own counting; for the interruptors and fractions the word's letters are left unknown and only need to agree with themselves."
    ),
}

import random
import time
from fractions import Fraction
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
N_CONTROLS = 10
ALPH = {"std": STD, "kry": KRY}
WORDS = "kryptos/data/words.txt"
WMIN, WMAX = 3, 20


def known_positions(known):
    return [q - 1 for q in sorted(known)]


def runlen_seq(word, zero_base, upto):
    """Key-letter index per position: letter j covers value(word[j]) places (A=1, or A=0 skipped)."""
    out = []
    j = 0
    guard = 0
    while len(out) <= upto:
        v = STD.index(word[j % len(word)]) + (0 if zero_base else 1)
        out.extend([j % len(word)] * v)
        j += 1
        guard += 1
        if guard > 10000:
            break
    return out


def numeric_key(word):
    order = sorted(range(len(word)), key=lambda i: (word[i], i))
    num = [0] * len(word)
    for r, i in enumerate(order):
        num[i] = r + 1
    return num


def christmas(word):
    num = numeric_key(word)
    pos_of = {n: i for i, n in enumerate(num)}
    return "".join(word[:pos_of[n] + 1] for n in range(1, len(word) + 1))


def extinguisher(word, m, upto):
    n = len(word)
    if n < m + 1:
        return None
    wins = [word[t:t + m] for t in range(n - m + 1)]
    num = numeric_key(word)
    out = []
    t = 0
    while len(out) <= upto:
        w = wins[t % len(wins)]
        g = num[t % n]
        out.extend(w[i % m] for i in range(g))
        t += 1
    return out


def word_keys(word, pos):
    """{schedule: string of 24 key letters at the known places} for one word."""
    upto = max(pos)
    res = {}
    for zb, name in ((False, "runlen A=1"), (True, "runlen A=0")):
        if zb and all(ch == "A" for ch in word):
            continue
        seq = runlen_seq(word, zb, upto)
        res[name] = "".join(word[seq[p]] for p in pos)
    ex = christmas(word)
    res["christmas"] = "".join(ex[p % len(ex)] for p in pos)
    for m in (2, 3, 4, 5):
        e = extinguisher(word, m, upto)
        if e:
            res[f"extinguisher {m}"] = "".join(e[p] for p in pos)
    return res


def forced(text, known, pa, ca, mode):
    PI = {c: i for i, c in enumerate(ALPH[pa])}; CI = {c: i for i, c in enumerate(ALPH[ca])}
    out = []
    for q in sorted(known):
        c, p = CI[text[q - 1]], PI[known[q]]
        out.append({"vig": (c - p) % 26, "beau": (c + p) % 26, "var": (p - c) % 26}[mode])
    return tuple(out)


def frac_digits(d, length):
    digs = []
    r = 1 % d
    seen = 0
    while len(digs) < length and seen < 10000:
        r *= 10
        dg, r = divmod(r, d)
        if dg:
            digs.append(dg)
        seen += 1
        if r == 0:
            r = 1 % d if d > 1 else 0
            if not digs:
                break
    return digs


def free_partitions(text, known):
    """{schedule: list of (setting, slot tuple over the 24 known places)}."""
    pos = known_positions(known)
    out = {"ct interruptor": [], "fraction digits": [], "pt interruptor": []}
    for X in STD:
        for n in range(1, 27):
            idx, slots = 0, {}
            for i in range(N):
                slots[i] = idx
                idx = 0 if text[i] == X else (idx + 1) % n
            out["ct interruptor"].append(((X, n), tuple(slots[p] for p in pos)))
    for d in range(3, 100):
        digs = frac_digits(d, 120)
        if not digs:
            continue
        for n in range(1, 27):
            seq = []
            j = 0
            while len(seq) < N:
                seq.extend([j % n] * digs[j % len(digs)])
                j += 1
            out["fraction digits"].append(((d, n), tuple(seq[p] for p in pos)))
    runs = [(22, "EASTNORTHEAST"), (64, "BERLINCLOCK")]
    for X in STD:
        for n in range(1, 27):
            for j0 in range(n):
                for j1 in range(n):
                    sl = []
                    for (start, w), j in zip(runs, (j0, j1)):
                        idx = j
                        for ch in w:
                            sl.append(idx)
                            idx = 0 if ch == X else (idx + 1) % n
                    out["pt interruptor"].append(((X, n, j0, j1), tuple(sl)))
    return out


def consistent(slots, K):
    seen = {}
    for s, k in zip(slots, K):
        if seen.setdefault(s, k) != k:
            return False
    return True


def _texts(args):
    t, text, known, word_index = args
    classes = [(pa, ca, m) for pa in ALPH for ca in ALPH for m in ("vig", "beau", "var")]
    hits = {}
    for pa, ca, m in classes:
        K = forced(text, known, pa, ca, m)
        for ka in ALPH:
            key = "".join(ALPH[ka][v] for v in K)
            for sched, idx in word_index.items():
                for w in idx.get(key, []):
                    hits.setdefault(sched, []).append({"word": w, "table": f"{pa}/{ca}/{m}", "numbering": ka})
    parts = free_partitions(text, known)
    free = {}
    for sched, lst in parts.items():
        uniq = {}
        for setting, sl in lst:
            uniq.setdefault(sl, []).append(setting)
        cnt = 0
        for sl, settings in uniq.items():
            checks = 24 - len(set(sl))
            if checks < 1:
                continue
            for pa, ca, m in classes:
                if consistent(sl, forced(text, known, pa, ca, m)):
                    cnt += len(settings)
        free[sched] = cnt
    return t, hits, free


def run(ctx):
    import multiprocessing as mp
    import sys
    import types
    ct, known = ctx.K4, ctx.KNOWN
    pos = known_positions(known)
    # sources' worked examples
    assert len(christmas("CHRISTMAS")) == 45
    assert numeric_key("EXTINGUISHER")[:7] == [1, 12, 10, 5, 7, 3, 11]
    assert frac_digits(7, 6) == [1, 4, 2, 8, 5, 7]
    words = [w.strip().upper() for w in open(WORDS).read().split() if w.strip().isalpha() and WMIN <= len(w.strip()) <= WMAX]
    word_index = {}
    for w in words:
        for sched, key in word_keys(w, pos).items():
            word_index.setdefault(sched, {}).setdefault(key, []).append(w)
    rng = random.Random(1510)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    if getattr(sys.modules.get(__name__), "_texts", None) is not _texts:
        m = types.ModuleType(__name__); m.__dict__.update(globals()); sys.modules[__name__] = m
    with mp.get_context("fork").Pool(8) as pool:
        res = pool.map(_texts, [(t, x, known, word_index) for t, x in enumerate(texts)], chunksize=1)
    res.sort(key=lambda r: r[0])
    scheds = sorted(word_index)
    summary = {}
    for s_ in scheds:
        summary[s_] = {"k4_word_hits": len(res[0][1].get(s_, [])), "coppers_word_hits": [len(r[1].get(s_, [])) for r in res[1:]]}
    for s_ in ("ct interruptor", "fraction digits", "pt interruptor"):
        summary[s_] = {"k4_consistent_with_check": res[0][2][s_], "coppers": [r[2][s_] for r in res[1:]]}
    k4_hits = res[0][1]
    cands = []
    bounds = {"family": "Friedman key-advance schedules (MC III, TM 32-220) on the 12 standard/KRYPTOS tables x 2 key numberings",
              "words": len(words), "word_lengths": [WMIN, WMAX], "summary": summary, "k4_word_hits": {k: v[:20] for k, v in k4_hits.items()},
              "free_settings": {"ct interruptor": "26 letters x key lengths 1-26", "fraction digits": "denominators 3-99 x key lengths 1-26, zeros dropped",
                                "pt interruptor": "26 letters x key lengths 1-26 x start place of each known run"},
              "controls": f"{N_CONTROLS} shuffled coppers (seed 1510), identical test", "exhaustive": True}
    notes = "; ".join(f"{k}: K4 {v.get('k4_word_hits', v.get('k4_consistent_with_check'))} (coppers {min(v.get('coppers_word_hits', v.get('coppers')))}-{max(v.get('coppers_word_hits', v.get('coppers')))})" for k, v in summary.items())
    return {"candidates": cands, "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    pos = known_positions(known)
    w = "KRYPTOS"
    ks = word_keys(w, pos)
    lines = [f"word {w}: the key letter in use at each known place, by schedule", ""]
    for s_, k in ks.items():
        lines.append(f"  {s_:16s} places 22-34: {k[:13]}   64-74: {k[13:]}")
    K = forced(ct, known, "kry", "kry", "vig")
    lines += ["", "sculpture's table (KRYPTOS alphabets, Vigenere): the key letters the known letters force",
              "  places 22-34: " + "".join(KRY[v] for v in K[:13]) + "   64-74: " + "".join(KRY[v] for v in K[13:]),
              "", "CHRISTMAS expands to " + christmas("CHRISTMAS") + " (45 letters, as MC III §35c)"]
    return "\n".join(lines)
