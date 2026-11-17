"""Experiment: F16.5. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f16.5-an-unknown-english-text-plus-a-dictionary-word",
    "title": "F16.5: a running key from an unknown English text plus a repeated dictionary word, on the sculpture's tables: every word of 1-12 letters at every phase, added or taken away, numbered on the standard or KRYPTOS alphabet, subtracted from the forced key; the two windows left ranked by quadgrams, then MIX8m; K4 against 50 shuffles, 20 plants measured first",
    "family": "16-simple-hand-methods",
    "parent": "0246-f14-duress-reading-running-english-key-judged-by-mix8m-and-the-judge",
    "changed": (
        "F16.5 (issue #123). 0125 and 0246 asked whether the forced key at the 24 known places is two windows of English "
        "(an unknown book as running key). Here a repeated word may sit on top of the book (F16.2 for an unknown text): "
        "each dictionary or puzzle word of 1-12 letters, every phase, sign and numbering, is subtracted first, and the "
        "rest is scored as 0246 scores it (quadgrams over both windows, the 300 best per text rescored by 0246's MIX8m). "
        "Tables: the sculpture's (plain and cipher standard or KRYPTOS, key numbering standard or KRYPTOS, three rules); "
        "0246's 208,062 dictionary tables times every word would be about 10^13 keys and are left out (bound stated)."
    ),
    "hypothesis_expert": (
        "C5 (Scheidt: 'the correct key word/s'), C7, C9 (an earlier or named text as key), Family C (two key parts "
        "combined, 06-hypotheses.md), Scheidt's duress keys (0246). Model: k_i = T_{o+i} + s W_{i mod L} on the table's "
        "key numbering, T an English text, W a word; the forced key at 22-34 and 64-74 minus s W must be two windows of "
        "English (13 and 11 letters). Pre-registered: statistic = the best MIX8m over both windows; K4 flags at p < 0.05 "
        "against 50 shuffles; power first: 20 plants (Carter as the book, a random dictionary word of 3-12 letters on "
        "top), found when their statistic beats every shuffle's; bar 20 of 20 as 0246. Below the bar the item closes "
        "sampled at the measured power."
    ),
    "hypothesis_eli5": (
        "Suppose the key was a passage from some English book with a short word added over it. At the known places we can "
        "work out the key. Take away every possible short word, and see whether what is left looks like two snippets of "
        "English, on the carving and on scrambled copies; and first check, on planted messages, that the test can see it."
    ),
    "prediction": (
        "Plants found well below 20 of 20 (24 letters of English beside 170,000 words x phases is a large search; the "
        "word gives the copies as much freedom as K4): the item closes sampled at that power. K4's statistic inside the "
        "shuffles (p above 0.05). No candidates."
    ),
    "method": (
        "1. Forced key at 22-34 and 64-74 for each of the 8 sculpture tables x 3 rules. 2. For each word of 1-12 letters "
        "(dictionary and puzzle), phase 0..L-1, sign +/-, numbering standard or KRYPTOS: subtract; score both windows by "
        "quadgrams. 3. The 300 best per text rescored by MIX8m (0246's model, unchanged). 4. K4, 50 shuffles (seed 16500), "
        "20 plants. 5. p for K4; plants found above every shuffle."
    ),
    "walkthrough": (
        "1. On the plain table, under EASTNORTHEAST, the key must be BLZCDCYYGCKAZ. "
        "2. Write a word, say LAYER, repeated from the right phase, under those key letters and subtract it letter by letter. "
        "3. Read what is left: if the key was a book plus LAYER, it is a piece of the book. "
        "4. Do the same at BERLINCLOCK, with the word's phase carried on from place 22. "
        "5. Try every word and phase; keep the remainders that look most like English; compare with scrambled copies."
    ),
    "expected_minutes": 60,
}

import importlib.util
import multiprocessing as mp
import os
import random
import sys
import time
import types
from pathlib import Path

import numpy as np

N = 97
ROOT = Path(__file__).resolve().parent
STD = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KRY = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
PLACES = list(range(22, 35)) + list(range(64, 75))
N_COPIES = 50
N_PLANTS = 20
LMAXW = 12
TOPQ = 300
CHUNK = 250000
SEED = 16500
_G = {}


def frozen(tag):
    path = next((ROOT / "experiments").glob(f"{tag}-*")) / "attack.py"
    spec = importlib.util.spec_from_file_location(f"frozen{tag}", path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    m.ROOT = ROOT
    return m


def setup(vocab):
    if "words" in _G:
        return
    m246 = frozen("0246")
    cwd = os.getcwd(); os.chdir(ROOT)
    m246.models()
    os.chdir(cwd)
    _G["m246"] = m246
    ws = {w.strip().upper() for w in (ROOT / "kryptos" / "data" / "words.txt").read_text().split()}
    ws |= {w.upper() for w in vocab}
    ws = sorted(w for w in ws if w.isalpha() and 1 <= len(w) <= LMAXW)
    _G["words"] = ws
    from kryptos.scorer import _table
    logs, floor = _table()
    tab = np.full(26 ** 4, floor)
    for q, v in logs.items():
        if len(q) == 4 and q.isalpha() and q.isupper():
            tab[((ord(q[0]) - 65) * 26 + ord(q[1]) - 65) * 676 + (ord(q[2]) - 65) * 26 + ord(q[3]) - 65] = v
    _G["tab"] = tab
    # word-key matrices per numbering: rows = (word, phase), cols = the 24 places, value = word letter's number
    off = np.array([q - 22 for q in PLACES])
    mats, labels = {}, []
    for num, A in (("std", STD), ("kry", KRY)):
        pos = {c: i for i, c in enumerate(A)}
        rows = []
        for w in ws:
            v = [pos[c] for c in w]
            for ph in range(len(w)):
                rows.append([v[(ph + o) % len(w)] for o in off])
                if num == "std":
                    labels.append((w, ph))
        mats[num] = np.array(rows, dtype=np.int16)
    _G["mats"], _G["labels"] = mats, labels


def tables():
    I = list(range(26))
    posK = [KRY.index(c) for c in STD]          # place of letter in KRYPTOS
    Kr = [STD.index(c) for c in KRY]            # number -> letter in KRYPTOS numbering
    out = []
    for pn, P in (("std", I), ("kry", posK)):
        for cn, C in (("std", I), ("kry", posK)):
            for kn, K in (("std", I), ("kry", Kr)):
                out.append((f"{pn}-{cn} key {kn}", P, C, kn, K))
    return out


def forced(text, known):
    """Per table and rule: the forced key numbers (place in the table arithmetic) at the 24 places."""
    out = []
    for name, P, C, kn, K in tables():
        for rule in ("vig", "var", "beau"):
            c = np.array([C[ord(text[q - 1]) - 65] for q in PLACES]); p = np.array([P[ord(known[q]) - 65] for q in PLACES])
            k = {"vig": c - p, "var": p - c, "beau": c + p}[rule] % 26
            out.append((f"{name} {rule}", kn, K, k.astype(np.int16)))
    return out


def search(text, known):
    tab = _G["tab"]
    labels = _G["labels"]
    cand = []
    for tname, kn, K, k in forced(text, known):
        Karr = np.array(K, dtype=np.int64)
        M = _G["mats"][kn]
        for sgn in (1, -1):
            for a0 in range(0, len(M), CHUNK):                # chunks keep a worker near 300 MB
                R = (k[None, :] - sgn * M[a0:a0 + CHUNK]) % 26  # the book's key numbers
                t = Karr[R]                                     # as letters 0-25
                q = lambda j: tab[((t[:, j] * 26 + t[:, j + 1]) * 26 + t[:, j + 2]) * 26 + t[:, j + 3]]
                s = sum(q(j) for j in range(10)) + sum(q(j) for j in range(13, 21))
                top = np.argpartition(-s, TOPQ)[:TOPQ]
                for i in top:
                    w, ph = labels[a0 + i]
                    cand.append((float(s[i]) / 18, "".join(chr(65 + int(v)) for v in t[i]), f"{tname} sign {sgn:+d}", w, ph))
            cand.sort(reverse=True)
            del cand[TOPQ:]
    cand.sort(reverse=True)
    cand = cand[:TOPQ]
    m246 = _G["m246"]
    w1 = m246.mix8m([x[1][:13] for x in cand]); w2 = m246.mix8m([x[1][13:] for x in cand])
    return sorted(((float(a + b), *x) for a, b, x in zip(w1, w2, cand)), reverse=True)[:20]


def _job(args):
    tid, text, known = args
    return tid, search(text, known)


def encipher(pt, book, word, P, C, K, rule, sgn):
    """k = book number + sgn * word number in the key numbering; table rule as 0125."""
    Kinv = {le: i for i, le in enumerate(K)}
    Cinv = {v: i for i, v in enumerate(C)}
    out = []
    for i, ch in enumerate(pt):
        kv = (Kinv[ord(book[i]) - 65] + sgn * Kinv[ord(word[i % len(word)]) - 65]) % 26
        pv = P[ord(ch) - 65]
        cv = {"vig": (pv + kv) % 26, "var": (pv - kv) % 26, "beau": (kv - pv) % 26}[rule]
        out.append(chr(65 + Cinv[cv]))
    return "".join(out)


def run(ctx):
    import re
    t0 = time.time()
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    setup(ctx.vocabulary)
    k4, known = ctx.K4, ctx.KNOWN
    rng = random.Random(SEED)
    texts = [("k4", k4, known)]
    for i in range(N_COPIES):
        s = list(k4); rng.shuffle(s); texts.append((f"copy{i}", "".join(s), known))
    src = re.sub("[^A-Z]", "", (ROOT / "knowledge" / "sources" / "carter-1923-tomb-of-tutankhamen-vol1.txt").read_text(errors="ignore").upper())
    tb = tables()
    plants = []
    for j in range(N_PLANTS):
        s0 = rng.randrange(20000, len(src) - 400)
        pt = list(src[s0:s0 + N])
        for q, ch in known.items():
            pt[q - 1] = ch
        pt = "".join(pt)
        book = src[s0 + 200: s0 + 200 + N]
        word = rng.choice([w for w in _G["words"] if 3 <= len(w) <= 12])
        name, P, C, kn, K = rng.choice(tb); rule = rng.choice(("vig", "var", "beau")); sgn = rng.choice((1, -1))
        ct = encipher(pt, book, word, P, C, K, rule, sgn)
        plants.append({"word": word, "table": name, "rule": rule, "sign": sgn, "truth": "".join(book[q - 1] for q in PLACES)})
        texts.append((f"plant{j}", ct, known))
    saved = getattr(ctx, "saved", {}) or {}
    res = {t[0]: saved[t[0]] for t in texts if t[0] in saved}
    todo = [t for t in texts if t[0] not in res]
    W = int(os.environ.get("K4_WORKERS", 8))
    ctx.progress(len(res), len(texts), "texts")
    with mp.get_context("fork").Pool(W) as pool:
        for tid, out in pool.imap_unordered(_job, todo, chunksize=1):
            res[tid] = [list(x) for x in out]
            ctx.save(tid, res[tid])
            ctx.progress(len(res), len(texts), "texts")
    best = {t[0]: res[t[0]][0][0] for t in texts}
    cop = [best[f"copy{i}"] for i in range(N_COPIES)]
    p = (1 + sum(1 for x in cop if x >= best["k4"])) / (N_COPIES + 1)
    pf = []
    for j, pl in enumerate(plants):
        truth_in = any(r[2] == pl["truth"] for r in res[f"plant{j}"])
        pf.append({**{k: v for k, v in pl.items() if k != "truth"}, "best": best[f"plant{j}"], "found": best[f"plant{j}"] > max(cop),
                   "truth_in_top20": truth_in})
    nfound = sum(x["found"] for x in pf)
    return {"candidates": [], "bounds": {
        "item": "F16.5", "words": len(_G["words"]), "word_lengths": [1, LMAXW],
        "keys_per_text": int(sum(len(w) for w in _G["words"]) * 2 * 24),
        "tables": "sculpture: plain and cipher standard or KRYPTOS, key numbering standard or KRYPTOS (8), rules vig/var/beau; word added or taken away, numbered like the key",
        "not_covered": "0125/0246's 208,062 dictionary tables with a word on top (about 10^13 keys)",
        "ranking": f"quadgrams over both windows, the {TOPQ} best per text rescored by 0246's MIX8m",
        "k4_best": res["k4"][0], "k4_top5": res["k4"][:5], "k4_p": round(p, 4), "flag": p < 0.05,
        "copies_best_max": max(cop), "copies_best_median": float(np.median(cop)),
        "plants": pf, "plants_found": nfound, "power_bar": "20 of 20 (0246)",
        "verdict_rule": "below the bar: closed, sampled at the measured power",
        "copies": N_COPIES, "exhaustive": True, "compute_seconds": round(time.time() - t0), "aws_cost_estimate_dollars": 0.6},
        "notes": f"K4 best MIX8m {best['k4']:.1f}, p {p:.3f} against {N_COPIES} shuffles; plants found {nfound}/{N_PLANTS}"}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    k = [(STD.index(ctx.K4[q - 1]) - STD.index(ctx.KNOWN[q])) % 26 for q in PLACES[:13]]
    w = "LAYER"
    r = "".join(STD[(a - STD.index(w[(q - 22) % 5])) % 26] for a, q in zip(k, PLACES[:13]))
    return "\n".join(["plain table, Vigenere, places 22-34:", f"  forced key   {''.join(STD[a] for a in k)}",
                      f"  word LAYER   {''.join(w[(q - 22) % 5] for q in PLACES[:13])}", f"  remainder    {r}",
                      "", "The remainder would be a piece of the book if the key were book + LAYER; scored as English, against scrambled copies."])
