"""Experiment 0198 (F9.1, second part). See program.md for the contract."""

EXPERIMENT = {
    "slug": "substitution-then-the-compiled-libraries",
    "title": "F9.1, second part: a one-to-one substitution, then each move in the three compiled libraries (mixed matrix triples, keyword triples, Nihilist squares): exact",
    "family": "9-substitution-then-transposition",
    "parent": "0197-substitution-then-every-newer-move",
    "changed": (
        "F9.1's list, the three entries 0197 left out because their builders are compiled into their own testers: 0158's "
        "mixed matrix triples (three stages of rows-of-w readings, every width 2-96, now including the all-narrow triples "
        "0134 had covered for keys only), 0162's triples with a keyword columnar, 0167's Nihilist square with three blanks "
        "at eight places and every key of each order. Each experiment's own C builder is reused unchanged except its "
        "per-route test, swapped for 0106's one-to-one test (equal known letters on equal carved letters, different on "
        "different); survivors are counted per text. K4 against the same shuffled copies those experiments used."
    ),
    "hypothesis_expert": (
        "F9 (substitution first, transposition last; the Zodiac 340 construction), A9. Model c = route(sigma(p)), sigma "
        "any permutation of 26 letters; 24 known letters with 13 different give 11 equalities and the inequalities. "
        "Statistic: surviving routes, K4 against copies."
    ),
    "hypothesis_eli5": (
        "The same check as 0197, letter swaps followed by a shuffle, for the three biggest families of shuffles the "
        "project has built: about 240 million of them."
    ),
    "prediction": "No route survives on K4 or the copies. Zero candidates.",
    "method": (
        "1. Load 0158, 0162 and 0167; replace only the per-route test in their C source with the one-to-one test. "
        "2. Run their own job lists through their own workers (8 processes). "
        "3. Read survivors per text from the counter slot the periodic test never uses (period 0)."
    ),
    "walkthrough": (
        "1. Take one of 0158's triples: rows of 30 read by columns, rows of 9 read by reversed columns, rows of 41 read clockwise. "
        "2. Follow each known letter to its carved place. "
        "3. The three Es must all show one carved letter; the other repeated letters likewise; different letters different carved letters. "
        "4. One mismatch kills the route; a route that passes is counted. "
        "5. All three libraries, on K4 and on scrambled copies."
    ),
}

import importlib.util
import sys
import time
from pathlib import Path

ANCHOR = "for (int e = 0; e < 24; e++) land[e] = wh[PIDX[e]];"
BIJ = ANCHOR + """
    {   /* one-to-one substitution test (F9.1): survivors counted at period 0, order A */
        for (int t = 0; t < T; t++) {
            int a_[26], b_[26], ok_ = 1;
            for (int x = 0; x < 26; x++) { a_[x] = -1; b_[x] = -1; }
            for (int e = 0; e < 24 && ok_; e++) {
                int c_ = CI[0][t][land[e]], p_ = PI[0][e];
                if (a_[p_] < 0 && b_[c_] < 0) { a_[p_] = c_; b_[c_] = p_; }
                else if (a_[p_] != c_ || b_[c_] != p_) ok_ = 0;
            }
            if (ok_) live[(0 * T + t) * (PMAX + 1) + 0]++;
        }
        return;
    }"""


def load(tag):
    d = [p for p in Path("experiments").iterdir() if p.name.startswith(tag + "-")][0]
    spec = importlib.util.spec_from_file_location(f"e{tag}", d / "attack.py")
    m = importlib.util.module_from_spec(spec)
    sys.modules[f"e{tag}"] = m
    spec.loader.exec_module(m)
    assert m.C_SOURCE.count(ANCHOR) == 1, tag
    m.C_SOURCE = m.C_SOURCE.replace(ANCHOR, BIJ)
    return m


def survivors(live, T):
    return [live[(0 * T + t) * 27 + 0] for t in range(T)]


def run(ctx):
    import multiprocessing as mp
    import random
    t0 = time.time()
    ct, known = ctx.K4, ctx.KNOWN
    known_list = [(q, known[q]) for q in sorted(known)]
    out = {}
    budget = ctx.time_left() - 120

    # 0158: mixed matrix triples, every width (the all-narrow triples included)
    m = load("0158")
    rng = random.Random(133)
    texts = [ct]
    for _ in range(m.N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    T = len(texts)
    m.W_DONE = 1
    firsts = [(r, w) for w in range(2, m.WMAX + 1) for r in m.READINGS]
    rng.shuffle(firsts)
    deadline = time.time() + budget * 0.5
    with mp.get_context("fork").Pool(m.WORKERS) as pool:
        parts = pool.map(m._worker, [(firsts[i::m.WORKERS], texts, known_list, deadline) for i in range(m.WORKERS)], chunksize=1)
    s = [sum(survivors(p["live"], T)[t] for p in parts) for t in range(T)]
    out["0158 mixed matrix triples"] = {"routes": sum(p["n_routes"] for p in parts), "first_stages_done": sum(len(p["done"]) for p in parts),
                                        "first_stages_total": len(firsts), "k4": s[0], "copies": s[1:]}

    # 0162: triples with a keyword columnar
    m = load("0162")
    st = m.stages(ctx.vocabulary)
    rng = random.Random(1608)
    texts = [ct]
    for _ in range(m.N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    T = len(texts)
    firsts = list(range(len(st))); rng.shuffle(firsts)
    deadline = time.time() + (budget - (time.time() - t0)) * 0.3
    with mp.get_context("fork").Pool(m.WORKERS) as pool:
        parts = pool.map(m._worker, [(firsts[i::m.WORKERS * 3], texts, known_list, st, deadline) for i in range(m.WORKERS * 3)], chunksize=1)
    s = [sum(survivors(p[0], T)[t] for p in parts) for t in range(T)]
    out["0162 keyword triples"] = {"routes": sum(p[3] for p in parts), "first_stages_done": sum(len(p[5]) for p in parts),
                                   "first_stages_total": len(st), "k4": s[0], "copies": s[1:]}

    # 0167: Nihilist squares
    m = load("0167")
    rng = random.Random(1670)
    texts = [ct]
    for _ in range(m.N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    T = len(texts)
    deadline = time.time() + max(60, ctx.time_left() - 90)
    jobs = [(f, p, texts, known_list, deadline) for p in range(8) for f in range(10)]
    with mp.get_context("fork").Pool(m.WORKERS) as pool:
        parts = pool.map(m._work, jobs, chunksize=1)
    s = [sum(survivors(p[0], T)[t] for p in parts) for t in range(T)]
    out["0167 Nihilist"] = {"routes": sum(p[3] for p in parts), "jobs_done": sum(1 for p in parts if p[4]), "jobs_total": len(jobs),
                            "k4": s[0], "copies": s[1:]}

    tot_k4 = sum(v["k4"] for v in out.values())
    bounds = {"family": "one-to-one substitution, then the moves of 0158, 0162 and 0167 (their own builders), exact",
              "per_library": out, "routes_total": sum(v["routes"] for v in out.values()),
              "survivors_k4": tot_k4, "seconds": round(time.time() - t0), "exhaustive": "per library as reported (jobs done)"}
    notes = "; ".join(f"{k}: {v['routes']:,} routes, survivors K4 {v['k4']} (copies {min(v['copies'])}-{max(v['copies'])})" for k, v in out.items())
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    return "the one-to-one test inserted into each library's C source:" + "\n" + BIJ
