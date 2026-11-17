"""Experiment: F16.8. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f16.8-an-artists-twist-on-k1-k2s-method",
    "title": "F16.8: K1/K2's keyed tableau with a hand-made twist: (a) the key word restarts at each sentence, so each known run sits at its own phase of a dictionary word (or under its own word); (b) enciphering and deciphering alternate (by letter, by known run, by carved line) under a periodic key 1-26; (c) the tableau read from the right or the bottom (reversed alphabets); on the 24 and the 20 official letters; K4 against 50 shuffles, plants",
    "family": "16-simple-hand-methods",
    "parent": "0171-two-parts-with-their-own-keys",
    "changed": (
        "F16.8 (issue #123). Prior coverage: restarts at carved lines (0128), one split between the runs with free "
        "repeating keys (0171), the tableau by rows and columns as a running key (0017), Vigenere/Beaufort/variant on "
        "standard and KRYPTOS alphabets (0005). New here: (a) a dictionary or puzzle key word whose phase restarts "
        "unseen between the runs (each run's forced key a cyclic stretch of the same word, any indicator shift), or a "
        "different word per run; (b) the form switching between encipher and decipher within one periodic key; (c) the "
        "plain, cipher and key alphabets each standard, KRYPTOS or either reversed (the tableau read from the right or "
        "from the bottom)."
    ),
    "hypothesis_expert": (
        "Sanborn, 2009 oral history (knowledge/sources/aaa-oral-history-2009-kryptos.md): systems 'that didn't necessarily "
        "depend on mathematics' which he could 'modify in a myriad of ways. So that even he would not know what it says'; "
        "the plaintext cut 'into strips in sentences'. FT 2025: 'It is a solid system, and I fucked with it' (C-FT, "
        "02-sanborn-said.md). A16 (12-assumptions.md): a standard system plus one amateur's change. Model: c = T(p, k) on "
        "a tableau with plain alphabet A_p, cipher alphabet A_c, key numbering A_k, each in {STD, KRY, STD reversed, KRY "
        "reversed}, form Vigenere, Beaufort or variant. (a) k_i = W[(phi_r + i) mod L] + s for i in run r, W a word of "
        "the dictionary or the puzzle vocabulary, phi_r free per run (restart at an unseen sentence break), s a shift; "
        "exact match of each run's forced key (13 or 9, and 11 letters) against every cyclic stretch of every word. "
        "(b) one periodic key of length 1-26, the form at each place drawn from a pair (vig/var = encipher/decipher, "
        "vig/beau, beau/var) by letter parity, by known run or by carved line (lines 2, 3, 4 = places 5-35, 36-66, "
        "67-97); exact consistency, fit counts against shuffles, the forced key checked for a word. (c) is (a) and (b) "
        "over the reversed alphabets. Chance per word and run of 9 or more letters: about L x 26 x 26^-9."
    ),
    "hypothesis_eli5": (
        "K1 and K2 were made by looking up each letter on the copper table with a repeating key word. An artist could "
        "change that simply: start the key word again at each new sentence, switch between enciphering and deciphering, "
        "or read the table from the other side. Each change is tested exactly against the known letters, on the "
        "carving and on scrambled copies."
    ),
    "prediction": (
        "(a) no word matches both runs on K4 (nor on shuffles; plants found); single-run matches rare and as frequent on "
        "shuffles. (b) no fit at short key lengths; fits from about 20 up at the shuffles' rate, no key word. (c) as "
        "(a) and (b). Zero candidates unless a word fits both runs."
    ),
    "method": (
        "1. Alphabets STD, KRY and their reverses for plain, cipher and key numbering (64 tables), three forms. "
        "2. (a) For each text and table-form: the forced key on run 1 (22-34; 26-34 without EAST) and run 2 (64-74), as "
        "differences from its first letter; looked up in an index of every cyclic stretch of that length of every word "
        "(lengths 2-24), also normalised; a word in both runs is a fit. 3. (b) For each table, form pair, pattern and "
        "key length 1-26: same-slot places must force the same key letter. 4. K4, 50 shuffles, 6 plants."
    ),
    "walkthrough": (
        "1. Take the KRYPTOS table and the word PALIMPSEST. "
        "2. Under EASTNORTHEAST find the key letters the table needs; write them as steps from the first one. "
        "3. Look for those steps anywhere in PALIMPSESTPALIMPSEST...: if found, the key could have restarted there. "
        "4. Do the same for BERLINCLOCK; a word found in both, at any two places, fits. "
        "5. For alternation: with key length 7, use Vigenere on odd places and its inverse on even ones; the places in the same slot must need the same key letter. "
        "6. Repeat for every word, table, form and on scrambled copies."
    ),
    "expected_minutes": 20,
}

import multiprocessing as mp
import os
import random
import sys
import types
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent
N = 97
STD = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KRY = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
ALPH = {"std": STD, "kry": KRY, "std_rev": STD[::-1], "kry_rev": KRY[::-1]}
FORMS = ("vig", "beau", "var")
PAIRS = (("vig", "var"), ("vig", "beau"), ("beau", "var"))
RUNS24 = (tuple(range(22, 35)), tuple(range(64, 75)))
RUNS20 = (tuple(range(26, 35)), tuple(range(64, 75)))
N_COPIES = 50
SEED = 16800
_G = {}


def kval(p, c, pa, ca, form):
    pi, ci = ALPH[pa].index(p), ALPH[ca].index(c)
    return (ci - pi) % 26 if form == "vig" else (ci + pi) % 26 if form == "beau" else (pi - ci) % 26


def tables():
    return [(pa, ca, ka) for pa in ALPH for ca in ALPH for ka in ALPH]


def words(vocab):
    ws = [w.strip().upper() for w in (ROOT / "kryptos" / "data" / "words.txt").read_text().split()]
    ws = {w for w in ws if w.isalpha() and 2 <= len(w) <= 24}
    ws |= {w.upper() for w in vocab if w.isalpha() and 2 <= len(w) <= 24}
    return sorted(ws)


def build_index(ws, lengths):
    """For each run length n and key numbering: normalised (first letter = 0) cyclic stretches of every word -> words."""
    idx = {}
    for ka, A in ALPH.items():
        pos = {c: i for i, c in enumerate(A)}
        for n in lengths:
            d = {}
            for w in ws:
                L = len(w)
                v = [pos[c] for c in w]
                for ph in range(L):
                    seq = [v[(ph + j) % L] for j in range(n)]
                    key = bytes((x - seq[0]) % 26 for x in seq)
                    d.setdefault(key, set()).add(w)
            idx[(ka, n)] = d
    return idx


def part_a(text, known, runs):
    """Words matching run 1 and run 2 (any phase, any shift), per table and form."""
    out = []
    for (pa, ca, ka), form in product(tables(), FORMS):
        hits = []
        for r in runs:
            k = [kval(known[q], text[q - 1], pa, ca, form) for q in r]
            # key letter values are positions in the key alphabet: k is already an index; normalise
            key = bytes((x - k[0]) % 26 for x in k)
            hits.append(_G["idx"][(ka, len(r))].get(key, set()))
        both = hits[0] & hits[1]
        if hits[0] or hits[1]:
            out.append({"table": [pa, ca, ka], "form": form, "run1": sorted(hits[0])[:20], "run2": sorted(hits[1])[:20],
                        "both": sorted(both)[:20]})
    return out


def line_of(q):
    return 1 if q <= 4 else 2 if q <= 35 else 3 if q <= 66 else 4


def part_b(text, known):
    """Periodic key 1-26 with the form switching by pattern; exact same-slot consistency. Key numbering does not
    change consistency, so tables are (pa, ca) only. -> list of fitting (pa, ca, pair, pattern, phase, L)."""
    Q = sorted(known)
    fits = []
    for pa in ALPH:
        for ca in ALPH:
            for pair in PAIRS:
                pats = {"parity0": lambda q: pair[(q - 1) % 2], "parity1": lambda q: pair[q % 2]}
                for a, b in product((0, 1), repeat=2):
                    if a != b:
                        pats[f"runs{a}{b}"] = (lambda a_, b_: (lambda q: pair[a_] if q < 50 else pair[b_]))(a, b)
                for t in product((0, 1), repeat=3):
                    if len(set(t)) > 1:
                        pats[f"lines{''.join(map(str, t))}"] = (lambda t_: (lambda q: pair[t_[line_of(q) - 2]]))(t)
                for pname, f in pats.items():
                    kv = {q: kval(known[q], text[q - 1], pa, ca, f(q)) for q in Q}
                    for L in range(1, 27):
                        slot = {}
                        ok = True
                        for q in Q:
                            s = (q - 1) % L
                            if s in slot and slot[s] != kv[q]:
                                ok = False
                                break
                            slot[s] = kv[q]
                        if ok:
                            fits.append((pa, ca, pair, pname, L))
    return fits


def _job(args):
    tid, text, kn = args
    known = _G["known"][kn]
    runs = RUNS24 if kn == "k24" else RUNS20
    return tid, kn, {"a": part_a(text, known, runs), "b": [list(x) for x in part_b(text, known)]}


def shuffled(text, seed):
    l_ = list(text)
    random.Random(seed).shuffle(l_)
    return "".join(l_)


def enc(pt, word, phases, pa, ca, ka, form, runs_split=50):
    """Plant: key word restarted at place runs_split with a new phase."""
    out = []
    for i, ch in enumerate(pt):
        ph = phases[0] if i + 1 < runs_split else phases[1]
        k = ALPH[ka].index(word[(ph + i) % len(word)])
        p = ALPH[pa].index(ch)
        v = (p + k) % 26 if form == "vig" else (k - p) % 26 if form == "beau" else (p - k) % 26
        out.append(ALPH[ca][v])
    return "".join(out)


def run(ctx):
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    from kryptos.plants import english_plant
    import json
    ws = words(ctx.vocabulary)
    _G["idx"] = build_index(ws, (9, 11, 13))
    k24 = dict(ctx.KNOWN)
    _G["known"] = {"k24": k24, "k20": {q: k24[q] for q in RUNS20[0] + RUNS20[1]}}
    # K1 self-check: KRYPTOS tables, PALIMPSEST, Vigenere, one phase
    k1 = json.loads((ROOT / "data" / "k1.json").read_text())
    pt1 = k1["plaintext"]; ct1 = k1["ciphertext"][:len(pt1)]
    assert enc(pt1, "PALIMPSEST", (0, 0), "kry", "kry", "kry", "vig") == ct1, "K1 self-check failed"
    texts = [("K4", ctx.K4)] + [(f"copy{i}", shuffled(ctx.K4, SEED + i)) for i in range(N_COPIES)]
    rng = random.Random(SEED + 999)
    plants = []
    for j in range(6):
        pt = english_plant(SEED + j)
        w = rng.choice([x for x in ws if 5 <= len(x) <= 12])
        tb = rng.choice(tables()); form = rng.choice(FORMS)
        ph = (rng.randrange(len(w)), rng.randrange(len(w)))
        ct = enc(pt, w, ph, *tb, form)
        plants.append({"id": f"plant{j}", "word": w, "table": list(tb), "form": form, "phases": ph})
        texts.append((f"plant{j}", ct))
    jobs = [(tid, t, kn) for tid, t in texts for kn in ("k24", "k20")]
    saved = getattr(ctx, "saved", {}) or {}
    res = {(j[0], j[2]): saved[f"{j[0]}|{j[2]}"] for j in jobs if f"{j[0]}|{j[2]}" in saved}
    todo = [j for j in jobs if (j[0], j[2]) not in res]
    W = int(os.environ.get("K4_WORKERS", 8))
    ctx.progress(len(res), len(jobs), "texts")
    with mp.get_context("fork").Pool(W) as pool:
        for tid, kn, out in pool.imap_unordered(_job, todo, chunksize=1):
            res[(tid, kn)] = out
            ctx.save(f"{tid}|{kn}", out)
            ctx.progress(len(res), len(jobs), "texts")
    summ = {}
    for kn in ("k24", "k20"):
        def counts(tid):
            a = res[(tid, kn)]["a"]
            b = res[(tid, kn)]["b"]
            return {"a_both": sum(len(x["both"]) for x in a), "a_single": sum(len(x["run1"]) + len(x["run2"]) for x in a),
                    "b_fits": len(b), "b_shortest": min([x[4] for x in b] or [99])}
        k4c = counts("K4")
        cc = [counts(f"copy{i}") for i in range(N_COPIES)]
        summ[kn] = {"k4": k4c, "copies_max": {k: max(c[k] for c in cc) for k in k4c},
                    "copies_median": {k: sorted(c[k] for c in cc)[N_COPIES // 2] for k in k4c},
                    "copies_min_b_shortest": min(c["b_shortest"] for c in cc),
                    "p_a_single": round((1 + sum(1 for c in cc if c["a_single"] >= k4c["a_single"])) / (N_COPIES + 1), 3),
                    "p_b_fits": round((1 + sum(1 for c in cc if c["b_fits"] >= k4c["b_fits"])) / (N_COPIES + 1), 3),
                    "p_b_shortest": round((1 + sum(1 for c in cc if c["b_shortest"] <= k4c["b_shortest"])) / (N_COPIES + 1), 3),
                    "k4_a_hits": res[("K4", kn)]["a"][:40],
                    "k4_b_fits_short": [x for x in res[("K4", kn)]["b"] if x[4] <= 20][:40]}
    pout = []
    for p in plants:
        for kn in ("k24", "k20"):
            a = res[(p["id"], kn)]["a"]
            hit = any(p["word"] in x["both"] for x in a)   # reversed alphabets make some table-form pairs equivalent
            pout.append({"id": p["id"], "known": kn, "word": p["word"], "found": hit})
    cands = []
    return {
        "candidates": cands,
        "bounds": {
            "item": "F16.8", "alphabets": list(ALPH), "tables": len(tables()), "forms": FORMS, "words": len(ws),
            "a": "each run's forced key against every cyclic stretch of every word of 2-24 letters (dictionary and puzzle), any shift, per key numbering; both runs = same word, phases free",
            "b": "periodic key 1-26, form switching within a pair (vig/var, vig/beau, beau/var) by letter parity, by known run, or by carved line (5-35, 36-66, 67-97); exact",
            "c": "the reversed alphabets (tableau read from the right or the bottom) are in (a) and (b)",
            "prior": "0128 restarts at carved lines; 0171 free keys split between runs; 0017 tableau as running key; 0005 forms and alphabets",
            "summary": summ, "plants": pout, "copies": N_COPIES, "exhaustive": True, "aws_cost_estimate_dollars": 0.1,
        },
        "notes": (f"k24: K4 {summ['k24']['k4']}, copies max {summ['k24']['copies_max']}; k20: K4 {summ['k20']['k4']}, copies max {summ['k20']['copies_max']}; "
                  f"plants {[(p['id'], p['known'], p['found']) for p in pout]}"),
    }


def encrypt(plaintext, key):
    return enc(plaintext, key["word"], tuple(key["phases"]), *key["table"], key["form"])


def worked_example(ctx, key):
    lines = ["KRYPTOS table, Vigenere: the key each known place needs, as steps from the run's first key letter", ""]
    for r in RUNS24:
        k = [kval(ctx.KNOWN[q], ctx.K4[q - 1], "kry", "kry", "vig") for q in r]
        lines.append(f"  places {r[0]}-{r[-1]}: key {''.join(KRY[x] for x in k)}  steps {[(x - k[0]) % 26 for x in k]}")
    lines += ["", "A key word restarted at a sentence break fits when both step lists occur in the word written round and round."]
    return "\n".join(lines)
