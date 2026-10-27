"""Experiment 0240. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f13-hill-2x2-and-3x3-ciphertext-only",
    "title": "F13.4e, Hill: 2x2 and 3x3, plain or affine, four letter numberings, every block alignment, solved from the ciphertext alone row by row; K4 against 100 shuffles, plants of both sizes",
    "family": "13-ciphertext-only",
    "parent": "0234-f13-periodic-key-on-the-sculptures-tables-ciphertext-only",
    "changed": (
        "F13.4e (issue #85), the Hill part. 0015 and 0105 killed every 2x2-4x4 Hill setting under the four standard "
        "numberings with the known letters; here they are not read. The classic ciphertext-only attack: each row of the "
        "decryption matrix (and its affine term) acts alone on every nth letter, so all 26^(n+1) rows are scored by the fit "
        "of their letters to English letter counts and the 2,000 best kept per row; rows are joined by a beam (bigram, "
        "then trigram fit inside blocks), the best invertible matrices scored by quadgrams and refined row by row, the "
        "best per setting rescored by MIX8m (F13.3). Changed before the run after dry runs: a sum of letter "
        "log-frequencies let rows that map every letter to E win, and 40 rows per row lost the true 3x3 rows (ranked "
        "4-3,625 of 456,976). Settings: size 2 or 3, numbering "
        "standard or KRYPTOS order from 0 or from 1, block alignment 0..n-1: 20 cells. Statistic, copies and plants as "
        "0234 (K4 against 100 shuffles; 8 plants per size, each against 10 own shuffles)."
    ),
    "hypothesis_expert": (
        "F8 (the HILL column, C21(a); Bauer's matrix conjecture) read without the known letters: the hedge for A2/A1 on a "
        "family the known letters killed exactly. F13.1 puts 3x3 Hill with an unknown numbering at 131 bits, under "
        "MIX8m's 189; with the four standard numberings it is 23-37 bits plus the alignment. The row-by-row attack is "
        "exact per row; with 32 letters per row the true row ranks in the hundreds or thousands of 456,976, so the beam "
        "keeps 2,000 per row, and the plants measure what is lost. Pre-registered: S = max z over the 20 cells against K4's 100 shuffles; "
        "K4 flags at p < 0.05; a size is decided when 6 of its 8 plants are above all 10 own shuffles."
    ),
    "hypothesis_eli5": (
        "A Hill cipher mixes letters in blocks of two or three using a small table of numbers. Without any known word it "
        "can still be broken one row of the table at a time: each row decides every second (or third) letter, so we try "
        "every possible row and keep those whose letters look like English, then put the best rows together. We do it for "
        "K4, for shuffles of K4 and for hidden test messages."
    ),
    "prediction": (
        "Plants found 8/8 at 2x2 and most at 3x3 (32 letters per row is enough for letter counts to keep the true row "
        "among 40). K4 inside its shuffles (p above 0.05); readings at most 4-5 known letters. F8's Hill part closes "
        "ciphertext-only for the four numberings."
    ),
    "method": (
        "1. Numberings: A=0 or A=1 on the standard or the KRYPTOS order. Alignments 0..n-1; letters outside whole blocks "
        "pass unchanged. "
        "2. Per setting and row r: every (d_r1..d_rn, e_r) mod 26 scored by the English letter log-frequency of the "
        "letters it yields, plus the entropy of those letters (the fit of their counts to English, so a row that maps every "
        "letter to E does not win); the 2,000 best kept. "
        "3. Rows joined by a beam: pairs of rows by English bigram fit inside each block (3,000 kept), the third row by "
        "trigram fit (3,000 kept), the 300 best invertible matrices scored by quadgrams on the whole text, the 20 best "
        "refined by swapping in any kept row while the score rises; the best rescored by MIX8m. "
        "4. S = max z over 20 cells against K4's 100 shuffles; plants (random matrix, numbering, alignment, half affine) "
        "against 10 own shuffles each. "
        "5. K4's best reading per cell submitted (key: size, numbering, alignment, matrix, offset)."
    ),
    "walkthrough": (
        "1. Number the letters, say A = 0 to Z = 25, and cut the carved text into blocks of three. "
        "2. One row of the unknown decoding table turns each block into one message letter: try all 26 x 26 x 26 rows (and "
        "a shift) and keep the 40 whose letters look most like English. "
        "3. Do the same for the other two rows. "
        "4. Try every way of putting three kept rows together, read the whole text and keep the most English. "
        "5. Compare K4's best with what shuffles of K4 reach."
    ),
    "expected_minutes": 20,
}

import importlib.util
import itertools
import math
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
NUMBERINGS = [("std", 0), ("std", 1), ("kry", 0), ("kry", 1)]
SIZES = (2, 3)
KROW, KPAIR, KTRIPLE, KFULL, REFINE = 2000, 3000, 3000, 300, 20
N_COPIES = 100
PLANTS_PER_SIZE, OWN_COPIES = 8, 10
LAM_Q = 0.55
SEED = 240
_G = {}


def num_maps(nb):
    """letter -> number and number -> letter for a numbering."""
    order, base = (STD if nb[0] == "std" else KRY), nb[1]
    to = {ch: (i + base) % 26 for i, ch in enumerate(order)}
    back = {v: ch for ch, v in to.items()}
    return to, back


def cells():
    return [(n, nb, o) for n in SIZES for nb in range(len(NUMBERINGS)) for o in range(n)]


def hill_apply(text, M, b, n, nb, o):
    to, back = num_maps(NUMBERINGS[nb])
    out = list(text)
    for s in range(o, N - n + 1, n):
        v = [to[text[s + j]] for j in range(n)]
        for r in range(n):
            out[s + r] = back[(sum(M[r][k] * v[k] for k in range(n)) + b[r]) % 26]
    return "".join(out)


def det(M):
    if len(M) == 2:
        return (M[0][0] * M[1][1] - M[0][1] * M[1][0]) % 26
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0])) % 26


def inverse(M):
    n, d = len(M), det(M)
    di = pow(d, -1, 26)
    if n == 2:
        adj = [[M[1][1], -M[0][1]], [-M[1][0], M[0][0]]]
    else:
        adj = [[0] * 3 for _ in range(3)]
        for r in range(3):
            for c in range(3):
                m = [[M[i][j] for j in range(3) if j != c] for i in range(3) if i != r]
                adj[c][r] = (-1) ** (r + c) * (m[0][0] * m[1][1] - m[0][1] * m[1][0])
    return [[(di * adj[r][c]) % 26 for c in range(n)] for r in range(n)]


def encrypt(plaintext, key):
    """key: size, numbering index, alignment, the encryption matrix M and offset b (c = M p + b per block)."""
    return hill_apply(plaintext, key["M"], key["b"], key["n"], key["numbering"], key["align"])


def models():
    if "m233" not in _G:
        path = next((ROOT / "experiments").glob("0233-*")) / "attack.py"
        spec = importlib.util.spec_from_file_location("frozen0233", path)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        m.ROOT, m.SRC = ROOT, ROOT / "knowledge" / "sources"
        m.CARTER = m.SRC / "carter-1923-tomb-of-tutankhamen-vol1.txt"
        C = m.corpus()
        codes = np.array([STD.index(c) + 1 for c in C["train_manuals"]], dtype=np.int64)
        f = np.bincount(codes - 1, minlength=26) + 1.0
        sys.path.insert(0, str(ROOT))
        from kryptos.scorer import _table
        logs, floor = _table()
        tab = np.full(26 ** 4, floor)
        for q, v in logs.items():
            if len(q) == 4 and q.isalpha() and q.isupper():
                tab[((ord(q[0]) - 65) * 26 + ord(q[1]) - 65) * 676 + (ord(q[2]) - 65) * 26 + ord(q[3]) - 65] = v
        _G.update(m233=m, Q=m.quadgram_model(), KN8m=m.KN.from_text(codes, 8), corpus=C, lf=np.log2(f / f.sum()), tab=tab)
        for n in SIZES:
            g = np.array(list(itertools.product(range(26), repeat=n + 1)), dtype=np.int64)   # (d_1..d_n, e)
            _G[f"rows{n}"] = g
    return _G["m233"]


def mix8m(texts):
    m = _G["m233"]
    return np.log2(LAM_Q * m.per_letter_probs(_G["Q"], texts) + (1 - LAM_Q) * m.per_letter_probs(_G["KN8m"], texts)).sum(axis=1)


def ngram_logs():
    """Joint log10 probabilities of English bigrams and trigrams, marginalized from the quadgram table's counts."""
    if "bi" not in _G:
        cnt4 = {}
        for ln in (ROOT / "kryptos" / "data" / "english_quadgrams.txt").read_text().split("\n"):
            if ln.strip():
                g, v = ln.split(); cnt4[g] = int(v)
        tri = np.ones(26 ** 3); bi = np.ones(26 ** 2)
        for g, v in cnt4.items():
            a, b, c = (ord(x) - 65 for x in g[:3])
            tri[(a * 26 + b) * 26 + c] += v; bi[a * 26 + b] += v
        _G["tri"], _G["bi"] = np.log10(tri / tri.sum()), np.log10(bi / bi.sum())
    return _G["bi"], _G["tri"]


def solve_cell(text, n, nb, o):
    """Beam attack in one cell: rows by letter-count fit (KROW kept), pairs of rows by bigram fit inside the block (KPAIR
    kept), the third row by trigram fit, the KFULL best invertible matrices scored by quadgrams on the whole text.
    -> (quadgram score, reading, D, e)."""
    bi, tri = ngram_logs()
    to, back = num_maps(NUMBERINGS[nb])
    let = np.array([STD.index(back[v]) for v in range(26)])            # number -> standard letter index
    lf_num = _G["lf"][let]
    starts = list(range(o, N - n + 1, n))
    X = np.array([[to[text[s + j]] for j in range(n)] for s in starts], dtype=np.int64)
    Xa = np.concatenate([X, np.ones((len(starts), 1), dtype=np.int64)], axis=1)
    R = _G[f"rows{n}"]
    vals = (R @ Xa.T) % 26
    m = vals.shape[1]
    cnt = np.bincount((np.arange(len(R))[:, None] * 26 + vals).ravel(), minlength=len(R) * 26).reshape(len(R), 26)
    with np.errstate(divide="ignore", invalid="ignore"):
        ent = -np.nansum(np.where(cnt > 0, cnt * np.log2(cnt / m), 0.0), axis=1)
    sc = (cnt * lf_num).sum(axis=1) + ent
    top = np.argsort(-sc)[:KROW]
    V = let[vals[top]]                                                   # KROW x blocks: standard letter indices
    # pairs of rows 0 and 1 by bigram fit inside each block
    P2 = bi[V[:, None, :] * 26 + V[None, :, :]].sum(axis=2) + 0.0       # KROW x KROW
    flat = np.argpartition(-P2.ravel(), KPAIR)[:KPAIR]
    pa, pb = flat // KROW, flat % KROW
    if n == 2:
        cand = [(int(x), int(y)) for x, y in zip(pa, pb)]
    else:
        T = np.empty((KPAIR, KROW))
        for c0 in range(0, KPAIR, 500):
            sl = slice(c0, c0 + 500)
            T[sl] = (tri[(V[pa[sl]][:, None, :] * 26 + V[pb[sl]][:, None, :]) * 26 + V[None, :, :]].sum(axis=2)
                     + P2[pa[sl], pb[sl]][:, None])
        flat3 = np.argpartition(-T.ravel(), KTRIPLE)[:KTRIPLE]
        cand = [(int(pa[f // KROW]), int(pb[f // KROW]), int(f % KROW)) for f in flat3]
    rows = R[top]
    keys = []
    for combo in cand:
        D = [[int(v) for v in rows[k][:n]] for k in combo]
        if math.gcd(det(D), 26) == 1:
            keys.append((D, [int(rows[k][n]) for k in combo]))
        if len(keys) >= KFULL:
            break
    if not keys:
        return -1e300, None, None, None
    num_text = np.array([to[c] for c in text], dtype=np.int64)
    Dm = np.array([k[0] for k in keys], dtype=np.int64); Em = np.array([k[1] for k in keys], dtype=np.int64)
    Pm = np.tile(num_text, (len(keys), 1))
    for s0 in starts:
        Pm[:, s0:s0 + n] = (np.einsum("kij,j->ki", Dm, num_text[s0:s0 + n]) + Em) % 26
    L = let[Pm]
    tab = _G["tab"]

    def qs(Lm):
        return tab[((Lm[:, :-3] * 26 + Lm[:, 1:-2]) * 26 + Lm[:, 2:-1]) * 26 + Lm[:, 3:]].sum(axis=1)
    q = qs(L)
    # refinement: for the REFINE best matrices, replace one row at a time by any kept row while the score rises
    best = (-1e300, None, None, None)
    for i in np.argsort(-q)[:REFINE]:
        D, e = [list(r) for r in keys[i][0]], list(keys[i][1])
        cur = float(q[i])
        improved = True
        while improved:
            improved = False
            for r in range(n):
                Lm = np.tile(L[i] if best[1] is None else L[i], (1, 1))
                base = num_text.copy()
                for s0 in starts:
                    base[s0:s0 + n] = (np.array(D) @ num_text[s0:s0 + n] + np.array(e)) % 26
                Pv = np.tile(base, (KROW, 1))
                for s0 in starts:
                    Pv[:, s0 + r] = (rows[:, :n] @ num_text[s0:s0 + n] + rows[:, n]) % 26
                qv = qs(let[Pv])
                k = int(np.argmax(qv))
                Dn = [list(x) for x in D]; Dn[r] = [int(v) for v in rows[k][:n]]
                if qv[k] > cur + 1e-9 and math.gcd(det(Dn), 26) == 1:
                    D, e[r], cur, improved = Dn, int(rows[k][n]), float(qv[k]), True
        if cur > best[0]:
            P1 = num_text.copy()
            for s0 in starts:
                P1[s0:s0 + n] = (np.array(D) @ num_text[s0:s0 + n] + np.array(e)) % 26
            best = (cur, "".join(STD[x] for x in let[P1]), D, e)
    return best


def solve(text):
    out = {}
    readings = []
    for c in cells():
        s, rd, D, e = solve_cell(text, *c)
        if rd is None:
            rd = text                                   # no invertible matrix kept: the cell reads as the carved text
        out[c] = [s, rd, D, e]
        readings.append(rd)
    sc = mix8m(readings)
    for c, v in zip(cells(), sc):
        out[c][0] = float(v)
    return out


def _job(args):
    tid, text = args
    return tid, solve(text)


def run(ctx):
    import multiprocessing as mp
    t0 = time.time()
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    models()
    rng = random.Random(SEED)
    C = _G["corpus"]
    # self-check: encryption then the inverse matrix restores the text in every numbering and alignment
    pt = C["test"][:N]
    for (n, nb, o) in cells():
        while True:
            M = [[rng.randrange(26) for _ in range(n)] for _ in range(n)]
            if math.gcd(det(M), 26) == 1:
                break
        b = [rng.randrange(26) for _ in range(n)]
        ct = hill_apply(pt, M, b, n, nb, o)
        Mi = inverse(M)
        e = [(-sum(Mi[r][k] * b[k] for k in range(n))) % 26 for r in range(n)]
        assert hill_apply(ct, Mi, e, n, nb, o) == pt
    k4 = ctx.K4
    texts = [("k4", k4)] + [(f"copy{i}", "".join(rng.sample(k4, N))) for i in range(N_COPIES)]
    plants = {}
    for n in SIZES:
        for j in range(PLANTS_PER_SIZE):
            src = C["test"] if j % 2 == 0 else C["test_xs"]
            o0 = rng.randrange(0, len(src) - N)
            p = src[o0:o0 + N]
            while True:
                M = [[rng.randrange(26) for _ in range(n)] for _ in range(n)]
                if math.gcd(det(M), 26) == 1:
                    break
            b = [rng.randrange(26) for _ in range(n)] if (j // 2) % 2 else [0] * n
            nb, o = rng.randrange(4), rng.randrange(n)
            pc = hill_apply(p, M, b, n, nb, o)
            pid = f"plant{n}_{j}"
            plants[pid] = {"n": n, "pt": p, "cell": (n, nb, o)}
            texts.append((pid, pc))
            for g in range(OWN_COPIES):
                texts.append((f"{pid}_own{g}", "".join(rng.sample(pc, N))))
    res = {}
    workers = int(os.environ.get("K4_WORKERS", 8))
    ctx.progress(0, len(texts), "texts solved")
    with mp.get_context("fork").Pool(workers) as pool:
        for tid, out in pool.imap_unordered(_job, texts, chunksize=1):
            res[tid] = out
            ctx.progress(len(res), len(texts), "texts solved")
    cl = cells()
    cop = np.array([[res[f"copy{i}"][c][0] for c in cl] for i in range(N_COPIES)])
    mu, sd = cop.mean(axis=0), cop.std(axis=0) + 1e-9

    def S(tid):
        z = (np.array([res[tid][c][0] for c in cl]) - mu) / sd
        return float(z.max()), cl[int(z.argmax())]
    s_k4, c_k4 = S("k4")
    s_cop = [S(f"copy{i}")[0] for i in range(N_COPIES)]
    p_k4 = (1 + sum(1 for x in s_cop if x >= s_k4)) / (N_COPIES + 1)
    power, recovered = {}, {}
    for n in SIZES:
        f = rec = 0
        for j in range(PLANTS_PER_SIZE):
            pid = f"plant{n}_{j}"
            f += S(pid)[0] > max(S(f"{pid}_own{g}")[0] for g in range(OWN_COPIES))
            rec += res[pid][plants[pid]["cell"]][1] == plants[pid]["pt"]
        power[n] = [f, PLANTS_PER_SIZE]; recovered[n] = [rec, PLANTS_PER_SIZE]
    cname = lambda c: f"{c[0]}x{c[0]} {NUMBERINGS[c[1]][0]}{NUMBERINGS[c[1]][1]} align {c[2]}"
    cands = []
    for c in cl:
        s, rd, D, e = res["k4"][c]
        if D is None:
            continue
        n = c[0]
        Mi = inverse(D)                                 # encryption matrix from the decryption rows
        b = [(-sum(Mi[r][k] * e[k] for k in range(n))) % 26 for r in range(n)]
        cands.append({"plaintext": rd, "key": {"n": n, "numbering": c[1], "align": c[2], "M": Mi, "b": b}})
    from kryptos.scorer import free_text      # gate 4's controls only, after the search
    controls = [max(ctx.english_score(free_text(res[f"copy{i}"][c][1])) for c in cl) for i in range(N_COPIES)]
    bounds = {
        "item": "F13.4e (Hill)", "search_reads_known_letters": False,
        "cells": [cname(c) for c in cl], "beam": {"rows": KROW, "pairs": KPAIR, "triples": KTRIPLE, "full": KFULL}, "affine": True,
        "texts": len(texts), "k4_copies": N_COPIES,
        "k4_statistic": round(s_k4, 3), "k4_best_cell": cname(c_k4), "k4_p": round(p_k4, 4),
        "copies_statistic_median": round(float(np.median(s_cop)), 3), "copies_statistic_max": round(max(s_cop), 3),
        "plant_power": power, "plant_exact_recovery": recovered,
        "k4_best_reading": res["k4"][c_k4][1],
        "exhaustive": "per row exact; rows joined by a beam of 2,000 rows, 3,000 pairs and triples, 300 matrices, 20 refined",
        "compute_seconds": round(time.time() - t0),
    }
    notes = (f"K4 statistic {s_k4:.2f} at {cname(c_k4)}, p {p_k4:.3f}; plant power 2x2 {power[2][0]}/8, 3x3 {power[3][0]}/8; "
             f"read exactly {recovered[2][0]}/8, {recovered[3][0]}/8")
    return {"candidates": cands, "bounds": bounds, "notes": notes, "controls": controls}


def worked_example(ctx, key):
    models()
    pt = _G["corpus"]["test"][:N]
    M = [[3, 3], [2, 5]]
    ct = hill_apply(pt, M, [0, 0], 2, 0, 0)
    s, rd, D, e = solve_cell(ct, 2, 0, 0)
    return "\n".join([
        "Row by row on a planted 2x2 Hill message (A = 0, matrix [[3, 3], [2, 5]]), no known letter:", "",
        f"  carved     {ct}", f"  rows found {D}, offsets {e}; true inverse {inverse(M)}", f"  reading    {rd}"])
