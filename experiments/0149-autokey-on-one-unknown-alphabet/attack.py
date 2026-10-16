"""Experiment 0149 (F1.7). See program.md for the contract."""

EXPERIMENT = {
    "slug": "autokey-on-one-unknown-alphabet",
    "title": "F1.7: ciphertext and plaintext autokey on one unknown alphabet (both sides, any of 26! orders), every lag, three forms, decided exactly",
    "family": "1-keyed-periodic",
    "parent": "0098-sculpture-running-keys-on-an-unknown-alphabet",
    "changed": (
        "F1.7, no move. Autokey was tested on the standard, KRYPTOS and 1,092 keyword tables (0002, 0025, 0064, 0071, 0072) "
        "but never on a free alphabet: the NSA's 1992 guess (C11a) on K1 and K2's system. With one unknown alphabet x on "
        "both sides, each known letter past the primer gives an equation in alphabet places only: ciphertext autokey x(c_i) "
        "= x(p_i) + x(c_{i-L}) (and the Beaufort and variant forms); plaintext autokey the same with the message letter "
        "L back, usable where both letters are known (lags 1-12 and 30-52). Decided exactly by a propagation search over "
        "the 26 places (one-to-one), every lag 1-96, ten scrambled coppers. The move-first version is left for a later "
        "run (27,852 moves x 96 lags x 3 forms x 11 texts, about 90 million searches)."
    ),
    "hypothesis_expert": (
        "C11a (NSA 1992, knowledge/sources/nsa-foia-1992-2014-blackvault-compilation.txt: 'plain-text auto-key... if a "
        "high-frequency letter is assigned 0'; NSA 2007 summary, nsa-2014-summary-of-previous-work.txt: plaintext and "
        "ciphertext autokey tested), C27(c) (a 'slightly different' tableau: any alphabet), C1(b). Model: x a bijection "
        "letters -> Z26; forms V: x(c) = x(p) + x(k), B: x(c) = x(k) - x(p), R: x(c) = x(p) - x(k); key letter k_i = c_{i-L} "
        "(ciphertext autokey, primer free for i <= L) or p_{i-L} (plaintext autokey). Solver: depth-first over places with "
        "propagation of every equation left with one open variable, translation fixed where the equations allow, node "
        "limit 200,000 (undecided counted); checked on planted autokey texts under random alphabets before K4. Statistic "
        "fixed before the run: per (kind, form, lag) fit or not; a K4 fit counts as rare where at most 1 of 10 coppers fit; "
        "K4's rare fits against each copper's rare fits against the rest."
    ),
    "hypothesis_eli5": (
        "In an autokey cipher the message (or the scrambled text) becomes its own key, a fixed number of letters back. "
        "We had only tried it with the sculpture's alphabets and alphabets built from words. Here the alphabet can be in "
        "any order at all. The known letters then give equations about the alphabet alone, and a search decides exactly, "
        "for every distance back, whether any alphabet satisfies them, on the carved text and on scrambled copies."
    ),
    "prediction": (
        "Short lags die (many equations), long lags fit (few), K4 like the coppers: rare fits on K4 no more than the most "
        "a copper has against the rest. Fitting cells are left for an English decider (F1.5's design 2), which this run "
        "does not apply. Zero candidates."
    ),
    "method": (
        "1. Check the solver: 6 planted autokey texts (random alphabet, random lag and form, both kinds) must fit. "
        "2. For K4 and 10 coppers, each kind, form and lag: build the equations, decide. "
        "3. Count fits per cell; mark rare fits; compare K4 with the coppers."
    ),
    "walkthrough": (
        "1. Ciphertext autokey at lag 8: the key for place i is the carved letter at place i - 8. "
        "2. At known place 30 (H under N), the key is the carved letter at 22, F: place(N) = place(H) + place(F) in the unknown alphabet. "
        "3. Each known place past the primer gives one such equation; 24 equations in 26 unknown places. "
        "4. Search for one alphabet order that satisfies all of them, filling places one at a time and following each equation that has a single unknown left. "
        "5. Repeat for every lag, the three ways of using the table, plaintext autokey, and scrambled copies."
    ),
}

import random
import time

N = 97
N_CONTROLS = 10
KINDS = ("ct", "pt")
FORMS = ("V", "B", "R")
NODE_LIMIT = 200000


def equations(text, known, L, kind, form):
    rows = []
    for q in sorted(known):
        i = q - 1
        if i - L < 0:
            continue
        if kind == "ct":
            kl = ord(text[i - L]) - 65
        else:
            if (i - L + 1) not in known:
                continue
            kl = ord(known[i - L + 1]) - 65
        c = ord(text[i]) - 65
        p = ord(known[q]) - 65
        r = {}

        def add(v, a):
            r[v] = (r.get(v, 0) + a) % 26
        add(c, 1)
        if form == "V":
            add(p, -1); add(kl, -1)
        elif form == "B":
            add(kl, -1); add(p, 1)
        else:
            add(p, -1); add(kl, 1)
        rows.append({v: a for v, a in r.items() if a})
    return rows


def solve(rows, node_limit=NODE_LIMIT):
    if any(not r for r in rows):
        rows = [r for r in rows if r]
    vars_ = sorted({v for r in rows for v in r})
    if not rows:
        return "fit", {}
    deg = {v: sum(1 for r in rows if v in r) for v in vars_}
    x, used, nodes, trail = {}, set(), [0], []
    inv = all(sum(r.values()) % 26 == 0 for r in rows)

    def check():
        changed = True
        while changed:
            changed = False
            for r in rows:
                open_ = [v for v in r if v not in x]
                s = sum(a * x[v] for v, a in r.items() if v in x) % 26
                if not open_:
                    if s:
                        return False
                elif len(open_) == 1:
                    v = open_[0]; a = r[v]
                    sols = [t for t in range(26) if (a * t + s) % 26 == 0 and t not in used]
                    if not sols:
                        return False
                    if len(sols) == 1:
                        x[v] = sols[0]; used.add(sols[0]); trail.append(v); changed = True
        return True

    def dfs():
        nodes[0] += 1
        if nodes[0] > node_limit:
            return None
        mark = len(trail)
        if not check():
            while len(trail) > mark:
                v = trail.pop(); used.discard(x.pop(v))
            return False
        open_ = [v for v in vars_ if v not in x]
        if not open_:
            return True
        v = max(open_, key=lambda u: (sum(1 for r in rows if u in r and sum(1 for w in r if w not in x) <= 2), deg[u]))
        for t in range(26):
            if t in used:
                continue
            x[v] = t; used.add(t); trail.append(v)
            r_ = dfs()
            if r_:
                return True
            if r_ is None:
                return None
            trail.pop(); used.discard(x.pop(v))
        while len(trail) > mark:
            w = trail.pop(); used.discard(x.pop(w))
        return False
    if inv:
        v0 = max(vars_, key=lambda u: deg[u]); x[v0] = 0; used.add(0); trail.append(v0)
    res = dfs()
    if res is None:
        return "undecided", None
    if not res:
        return "dead", None
    assert all(sum(a * x[v] for v, a in r.items()) % 26 == 0 for r in rows) and len(set(x.values())) == len(x)
    return "fit", dict(x)


def encipher(pt, alpha, L, kind, form, primer):
    pos = {ch: i for i, ch in enumerate(alpha)}
    ct = []
    for i, ch in enumerate(pt):
        k = primer[i] if i < L else (ct[i - L] if kind == "ct" else pt[i - L])
        kv, pv = pos[k], pos[ch]
        v = {"V": pv + kv, "B": kv - pv, "R": pv - kv}[form] % 26
        ct.append(alpha[v])
    return "".join(ct)


def _work(args):
    t, text, known = args
    out = {}
    und = 0
    for kind in KINDS:
        for form in FORMS:
            for L in range(1, N):
                rows = equations(text, known, L, kind, form)
                if not rows:
                    continue
                st, _ = solve(rows)
                out[f"{kind}/{form}/{L}"] = st
                und += st == "undecided"
    return t, out, und


def run(ctx):
    import multiprocessing as mp
    import sys
    import types
    from kryptos.facts import STANDARD_ALPHABET as STD
    ct, known = ctx.K4, ctx.KNOWN
    vr = random.Random(1470)
    for j in range(6):
        pt = [vr.choice(STD) for _ in range(N)]
        for q, a in known.items():
            pt[q - 1] = a
        al = list(STD); vr.shuffle(al); al = "".join(al)
        kind, form, L = KINDS[j % 2], FORMS[j % 3], vr.randrange(1, 40)
        txt = encipher("".join(pt), al, L, kind, form, [vr.choice(STD) for _ in range(L)])
        rows = equations(txt, known, L, kind, form)
        if rows:
            assert solve(rows)[0] in ("fit", "undecided"), (kind, form, L)
    rng = random.Random(147)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    if getattr(sys.modules.get(__name__), "_work", None) is not _work:
        m = types.ModuleType(__name__); m.__dict__.update(globals()); sys.modules[__name__] = m
    with mp.get_context("fork").Pool(8) as pool:
        res = pool.map(_work, [(t, x, known) for t, x in enumerate(texts)], chunksize=1)
    res.sort()
    T = len(texts)
    cells = sorted(set().union(*[r[1].keys() for r in res]))
    fit = [{c: r[1].get(c) == "fit" for c in cells} for r in res]

    def rare(t):
        return [c for c in cells if fit[t][c] and sum(fit[u][c] for u in range(T) if u != t) <= 1]
    k4_rare = rare(0)
    null_rare = [len(rare(t)) for t in range(1, T)]
    stop = len(k4_rare) > max(null_rare)
    summary = {}
    for kind in KINDS:
        for form in FORMS:
            ks = [c for c in cells if c.startswith(f"{kind}/{form}/")]
            summary[f"{kind}/{form}"] = {"lags_with_equations": len(ks), "k4_fit_lags": [int(c.split("/")[2]) for c in ks if fit[0][c]],
                                         "coppers_fit_count": [sum(fit[t][c] for c in ks) for t in range(1, T)],
                                         "k4_fit_count": sum(fit[0][c] for c in ks)}
    bounds = {
        "family": "ciphertext and plaintext autokey on one unknown alphabet (both sides), no move, every lag 1-96, three forms",
        "solver": f"propagation depth-first over the 26 places, node limit {NODE_LIMIT:,}; checked on 6 planted texts",
        "summary": summary, "undecided": {"k4": res[0][2], "controls": [r[2] for r in res[1:]]},
        "k4_rare_fits": k4_rare, "null_rare_fits_per_copper": null_rare, "stop_queue": stop,
        "controls": f"{N_CONTROLS} shuffled coppers (seed 147), identical search", "exhaustive": "exact per cell; undecided counted",
        "not_covered": "the move-first version (27,852 moves x 96 lags x 3 forms x 11 texts)",
    }
    notes = (", ".join(f"{k} K4 {v['k4_fit_count']} fits (coppers {min(v['coppers_fit_count'])}-{max(v['coppers_fit_count'])})" for k, v in summary.items())
             + f"; rare K4 fits {len(k4_rare)} vs null {min(null_rare)}-{max(null_rare)}; stop {stop}; undecided K4 {res[0][2]}")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    L = 8
    rows = []
    for q in sorted(known):
        i = q - 1
        if i - L >= 0:
            rows.append(f"place {q}: place({ct[i]}) = place({known[q]}) + place({ct[i - L]})   (key: carved letter at {q - L})")
    return "\n".join(["ciphertext autokey, lag 8, added form, one unknown alphabet: one equation per known place past the primer", ""] + rows[:10] + ["...", f"{len(rows)} equations in the unknown places; solved exactly"])
