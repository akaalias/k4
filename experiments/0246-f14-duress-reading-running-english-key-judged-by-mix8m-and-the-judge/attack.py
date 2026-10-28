"""Experiment 0246. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f14-duress-reading-running-english-key-judged-by-mix8m-and-the-judge",
    "title": "F14.3: the duress reading, a running key from English text with an English message: 0125's 3.7 million forced keys on the dictionary tables (and the sculpture's), ranked by MIX8m instead of quadgrams, the best read by the blind judge; K4 against 50 shuffles, 0125's 20 plants",
    "family": "14-scheidt-mask-keyed-by-words",
    "parent": "0125-forced-key-as-running-english-on-dictionary-alphabets",
    "changed": (
        "F14.3 (issue #93). 0125 asked whether the 24 key letters forced at the known places read as English, scored by "
        "quadgrams (power 11 of 20 plants); 0221 (A6.1) rejudged only each text's quadgram-best reading. Here the same "
        "exhaustive space (208,062 dictionary keyword tables x 3 configurations x 3 rules x 2 key alphabets, plus the 24 "
        "settings of the sculpture's own standard and KRYPTOS tables) is ranked by F13.3's MIX8m (1.95 bits per letter "
        "against the quadgrams' 1.75): each rule's 300 quadgram-best forced keys rescored by MIX8m over the two windows, "
        "and the 3 MIX8m-best of each text read by the blind judge, window by window."
    ),
    "hypothesis_expert": (
        "Scheidt's duress codes (03-scheidt-said.md, 2011: 'similar to what would be provided agents or pilots in case of "
        "capture'; 2015: 'I used to make those codes, for captured people'; Gillogly 2013 on 'multi-layered ciphers for "
        "which you can give up a key to the enemy that produces credible plaintext'; C5(c), C6). A running key that is "
        "itself English text gives a captor a believable key; C5 'a named text' read for any text. 0125 closed F1.3 by "
        "quadgrams; A6.1 held it; the stronger model can only sharpen the ranking. Model: c = C[P(p) + k] (and the variant "
        "and Beaufort rules), k read through the standard or the table's keyword alphabet; the 24 forced key letters "
        "(13 at 22-34, 11 at 64-74) would be two windows of English. Pre-registered: statistic = the best MIX8m log2 "
        "probability over the two windows; K4 flags at p < 0.05 against 50 shuffles; the judge's mean score over the "
        "two windows of each text's MIX8m-best key, K4 counts only above every shuffle. A plant (0125's: Carter's text "
        "as the key) is found when its statistic is above every shuffle of K4's (as 0125)."
    ),
    "hypothesis_eli5": (
        "A trick for agents who might be captured: let the secret key be an ordinary passage of a book, so that a captor "
        "who forces you to give it up gets something that looks harmless. If K4 was made that way, then where we know "
        "the message, working backwards gives 24 letters of that passage, which should read as English. An earlier test "
        "scored them with a simple four-letter-group count; here we use our best English model and then ask the language "
        "model judge, comparing K4 with shuffles of its own letters treated the same way."
    ),
    "prediction": (
        "Plants found more often than 0125's 11 of 20 (about 15 of 20). K4 inside its shuffles by MIX8m (p above 0.05) and "
        "by the judge (not above every shuffle). F14.3 closes as sampled."
    ),
    "method": (
        "1. 0125's tables (its frozen alphabets(): 208,062 dictionary keyword alphabets), configurations W-std, std-W, "
        "W-W, rules vig/var/beau, key alphabet standard or W; plus the sculpture's tables (plain and cipher standard or "
        "KRYPTOS, key alphabet standard or KRYPTOS, 3 rules). "
        "2. Every forced key (24 letters) scored by quadgrams over the two windows (as 0125); the 300 best per rule "
        "rescored by MIX8m, each window from its own start; the 300 best overall kept. "
        "3. Statistic: the best MIX8m; K4 ranked among 50 shuffles (seed 246). "
        "4. The 3 MIX8m-best keys of K4, every shuffle and every plant read by the blind judge, window by window (in one "
        "call, blind to which is which); judge score of a text = the mean over its two windows of its MIX8m-best key. "
        "5. 0125's 20 plants (its frozen make_plants with its seed) through the same search."
    ),
    "walkthrough": (
        "1. Take a table, say one built on the word HOLOZOIC on the plain side with the standard alphabet on the cipher side. "
        "2. At place 22 the message has E and the copper F: find which key letter turns E into F on that table. "
        "3. Do this at all 24 known places: 13 key letters for 22-34 and 11 for 64-74. "
        "4. If the key were a passage of a book, these would be two pieces of English: score them with the English model. "
        "5. Do it for every table and way of reading the table, keep the best, and compare K4's best with what shuffles of K4 reach; ask the judge to read the best pieces."
    ),
    "expected_minutes": 15,
}

import importlib.util
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
STRETCHES = [(22, 34), (64, 74)]
N_COPIES = 50
TOPQ, TOPJ = 300, 3
LAM_Q = 0.55
SEED = 246
_G = {}


def frozen(tag):
    path = next((ROOT / "experiments").glob(f"{tag}-*")) / "attack.py"
    spec = importlib.util.spec_from_file_location(f"frozen{tag}", path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    m.ROOT = ROOT
    return m


def models():
    if "m233" not in _G:
        m = frozen("0233")
        m.SRC = ROOT / "knowledge" / "sources"
        m.CARTER = m.SRC / "carter-1923-tomb-of-tutankhamen-vol1.txt"
        C = m.corpus()
        codes = np.array([STD.index(c) + 1 for c in C["train_manuals"]], dtype=np.int64)
        _G.update(m233=m, Q=m.quadgram_model(), KN8m=m.KN.from_text(codes, 8))
    return _G["m233"]


def mix8m(texts):
    m = _G["m233"]
    return np.log2(LAM_Q * m.per_letter_probs(_G["Q"], texts) + (1 - LAM_Q) * m.per_letter_probs(_G["KN8m"], texts)).sum(axis=1)


def stack():
    """Place maps of every table as int16 arrays: P[t, letter], C[t, letter] = place; K[t, number] = key letter."""
    if "Pm" in _G:
        return
    m125 = _G["m125"]
    al = m125.alphabets()
    A = list(al.keys()); names = list(al.values())
    W = np.array([[ord(ch) - 65 for ch in a] for a in A], dtype=np.int16)
    posW = np.zeros_like(W); np.put_along_axis(posW, W.astype(np.int64), np.broadcast_to(np.arange(26, dtype=np.int16), W.shape), axis=1)
    ident = np.broadcast_to(np.arange(26, dtype=np.int16), W.shape)
    Ps, Cs, Ks, blocks = [], [], [], []
    for cfg in m125.CONFIGS:
        for ka in m125.KEYALPHA:
            Ps.append(posW if cfg[0] == "W" else ident); Cs.append(posW if cfg.endswith("W") else ident)
            Ks.append(W if ka == "W" else ident); blocks.append((cfg, ka))
    Kr = np.array([ord(ch) - 65 for ch in KRY], dtype=np.int16); posK = np.zeros(26, dtype=np.int16); posK[Kr] = np.arange(26)
    I = np.arange(26, dtype=np.int16)
    sc = []
    for pn, P in (("std", I), ("kry", posK)):
        for cn, C in (("std", I), ("kry", posK)):
            for kn, K in (("std", I), ("kry", Kr)):
                sc.append((f"sculpture {pn}-{cn} key {kn}", P, C, K))
    _G["Pm"] = np.vstack(Ps + [np.stack([s[1] for s in sc])]).astype(np.int16)
    _G["Cm"] = np.vstack(Cs + [np.stack([s[2] for s in sc])]).astype(np.int16)
    _G["Km"] = np.vstack(Ks + [np.stack([s[3] for s in sc])]).astype(np.int16)
    _G["NA"], _G["names"], _G["blocks"], _G["sc_labels"] = len(A), names, blocks, [s[0] for s in sc]
    from kryptos.scorer import _table
    logs, floor = _table()
    tab = np.full(26 ** 4, floor)
    for q, v in logs.items():
        if len(q) == 4 and q.isalpha() and q.isupper():
            tab[((ord(q[0]) - 65) * 26 + ord(q[1]) - 65) * 676 + (ord(q[2]) - 65) * 26 + ord(q[3]) - 65] = v
    _G["tab"] = tab


def label(i):
    NA = _G["NA"]
    b = i // NA
    if b < len(_G["blocks"]):
        cfg, ka = _G["blocks"][b]
        return f"{_G['names'][i % NA]} {cfg} key {ka}"
    return _G["sc_labels"][i - NA * len(_G["blocks"])]


def search(text, known):
    """-> the TOPQ quadgram-best forced keys rescored by MIX8m: sorted list of (mix, quad, key letters, table, rule)."""
    Pm, Cm, Km, tab = _G["Pm"], _G["Cm"], _G["Km"], _G["tab"]
    places = [q for a, b in STRETCHES for q in range(a, b + 1)]
    c = np.array([ord(text[q - 1]) - 65 for q in places]); p = np.array([ord(known[q]) - 65 for q in places])
    Cc, Pp = Cm[:, c], Pm[:, p]
    cand = []
    for rule in ("vig", "var", "beau"):
        k = {"vig": Cc - Pp, "var": Pp - Cc, "beau": Cc + Pp}[rule] % 26
        t = np.take_along_axis(Km, k, axis=1)
        t64 = t.astype(np.int64)
        q = lambda j: tab[((t64[:, j] * 26 + t64[:, j + 1]) * 26 + t64[:, j + 2]) * 26 + t64[:, j + 3]]
        s = sum(q(j) for j in range(10)) + sum(q(j) for j in range(13, 21))
        top = np.argpartition(-s, TOPQ)[:TOPQ]
        cand += [(float(s[i]) / 18, "".join(chr(65 + int(v)) for v in t[i]), label(int(i)), rule) for i in top]
    cand.sort(reverse=True)
    cand = cand[:TOPQ]
    w1 = mix8m([x[1][:13] for x in cand]); w2 = mix8m([x[1][13:] for x in cand])
    return sorted(((float(a + b), *x) for a, b, x in zip(w1, w2, cand)), reverse=True)


def _job(args):
    tid, text, known = args
    return tid, search(text, known)


def encrypt(plaintext, key):
    """A running-key reading needs the whole book; this search returns no candidate, only the forced key letters."""
    return plaintext


def run(ctx):
    import multiprocessing as mp
    t0 = time.time()
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    cwd = os.getcwd(); os.chdir(ROOT)
    _G["m125"] = frozen("0125")
    plants = _G["m125"].make_plants(random.Random(125), list(_G["m125"].alphabets()), 20)
    os.chdir(cwd)
    models(); stack()
    k4, known = ctx.K4, ctx.KNOWN
    rng = random.Random(SEED)
    texts = [("k4", k4)]
    for i in range(N_COPIES):
        s = list(k4); rng.shuffle(s); texts.append((f"copy{i}", "".join(s)))
    for j, (ct, truth, setting) in enumerate(plants):
        texts.append((f"plant{j}", ct))
    res = {}
    workers = int(os.environ.get("K4_WORKERS", 8))
    ctx.progress(0, len(texts), "texts searched")
    with mp.get_context("fork").Pool(min(workers, 8)) as pool:
        for tid, out in pool.imap_unordered(_job, [(t, x, known) for t, x in texts], chunksize=1):
            res[tid] = out
            ctx.progress(len(res), len(texts), "texts searched")
    best = {t: res[t][0][0] for t, _ in texts}
    cop = [best[f"copy{i}"] for i in range(N_COPIES)]
    p_k4 = (1 + sum(1 for x in cop if x >= best["k4"])) / (N_COPIES + 1)
    plant_found = [best[f"plant{j}"] > max(cop) for j in range(len(plants))]
    plant_truth_rank = []
    for j, (ct, truth, setting) in enumerate(plants):
        keys = [r[2] for r in res[f"plant{j}"]]
        plant_truth_rank.append(keys.index(truth) + 1 if truth in keys else None)
    order = [t for t, _ in texts]
    windows = []
    for t in order:
        for r in res[t][:TOPJ]:
            windows += [r[2][:13], r[2][13:]]
    verdicts = ctx.judge(windows)
    js, nones, wi = {}, 0, 0
    for t in order:
        sc = []
        for r in res[t][:TOPJ]:
            a, b = verdicts[wi]["score"], verdicts[wi + 1]["score"]; wi += 2
            nones += (a is None) + (b is None)
            sc.append(None if a is None or b is None else (a + b) / 2)
        js[t] = sc
    j_k4 = js["k4"][0]
    j_cop = [js[f"copy{i}"][0] for i in range(N_COPIES)]
    jc = [x for x in j_cop if x is not None]
    j_above = j_k4 is not None and all(j_k4 > x for x in jc)
    j_plants = [js[f"plant{j}"][0] for j in range(len(plants))]
    j_plant_found = sum(1 for x in j_plants if x is not None and all(x > y for y in jc))
    bounds = {
        "item": "F14.3", "tables": int(_G["Pm"].shape[0]), "readings_per_text": int(_G["Pm"].shape[0]) * 3,
        "space": "0125's 208,062 dictionary keyword tables x 3 configurations x 2 key alphabets, plus the sculpture's 4 table pairs x 2 key alphabets; 3 rules",
        "ranking": f"quadgrams over both windows (as 0125), the {TOPQ} best per rule rescored by MIX8m (0233), window by window",
        "texts": len(texts), "copies": N_COPIES,
        "k4_best": list(res["k4"][0]), "k4_p_mix8m": round(p_k4, 4),
        "copies_best_mix8m_max": max(cop), "copies_best_mix8m_median": float(np.median(cop)),
        "plants_found_mix8m": sum(plant_found), "plants": len(plants), "plant_truth_rank_in_top300": plant_truth_rank,
        "plant_best_mix8m": [best[f"plant{j}"] for j in range(len(plants))],
        "judge_calls_estimated": len(texts) * TOPJ * 2, "judge_none": nones,
        "judge_k4": j_k4, "judge_copies_max": max(jc, default=None), "judge_copies_median": float(np.median(jc)) if jc else None,
        "judge_k4_above_every_copy": j_above, "judge_plants": j_plants, "judge_plants_found": j_plant_found,
        "k4_top3": [list(r) for r in res["k4"][:3]], "exhaustive": True, "compute_seconds": round(time.time() - t0),
    }
    notes = (f"K4 best MIX8m {best['k4']:.1f} bits, p {p_k4:.3f} against {N_COPIES} shuffles; plants found {sum(plant_found)}/20 by MIX8m; "
             f"judge K4 {j_k4} against copies max {bounds['judge_copies_max']}, plants above every copy {j_plant_found}/20")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def worked_example(ctx, key):
    known, ct = ctx.KNOWN, ctx.K4
    lines = ["The key letters forced at the known places on the sculpture's own table (Vigenere, KRYPTOS alphabet both sides):", "",
             "place  known  carved  key letter"]
    for q in (22, 23, 24, 25, 64, 65, 66):
        k = (KRY.index(ct[q - 1]) - KRY.index(known[q])) % 26
        lines.append(f"{q:>5}  {known[q]:>5}  {ct[q - 1]:>6}  {KRY[k]:>10}")
    lines += ["", "If the key were a passage of a book, the 13 letters at 22-34 and the 11 at 64-74 would read as English."]
    return "\n".join(lines)
