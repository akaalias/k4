"""Experiment 0154 (F1.8). See program.md for the contract."""

EXPERIMENT = {
    "slug": "carter-running-key-on-an-unknown-alphabet-rerun",
    "title": "F1.8: Carter's book as a running key on one unknown alphabet (both directions, every offset, three forms), solved exactly; and how many checks two unknown alphabets would leave for each running-key source",
    "family": "1-keyed-periodic",
    "parent": "0098-sculpture-running-keys-on-an-unknown-alphabet",
    "changed": (
        "F1.8, rerun of 0153, which hit the harness's time limit in its second pass (no clock check there; record kept as "
        "an error). Same test; the second pass now stops at the deadline and reports what it left, at a node limit of "
        "100,000. 0098 solved the sculpture's running keys on an unknown alphabet exactly but left Carter's book out; 0021 "
        "and 0047 ran Carter only on fixed and keyword tables. Here every offset of Carter's Tomb of Tut-ankh-Amen vol. 1 "
        "(284,914 letters as scanned), forwards and backwards, under one unknown alphabet on both sides, three forms: each "
        "known letter gives an equation in alphabet places only, decided by a compiled propagation search (checked "
        "against a Python solver on 300 random offsets and on a planted text), node limit 20,000, then 100,000 for the "
        "undecided. Ten scrambled coppers. Second part, counted not searched: for two unknown alphabets, the checks the "
        "24 equations leave (24 minus their rank mod 13) at sampled offsets of each running-key source."
    ),
    "hypothesis_expert": (
        "C7(d) (K3 is Carter's text; 'instructions in the earlier text that refer to later text', knowledge/02-sanborn-"
        "said.md), C13, C27(c), C5 ('a named text and a place in it' is a short key description). Model: x a bijection "
        "letters -> Z26 on both sides; key letter k_i = Carter[o + i] (forward) or the reversed book; forms V x(c) = x(p) + "
        "x(k), B x(c) = x(k) - x(p), R x(c) = x(p) - x(k). Source: knowledge/sources/carter-1923-tomb-of-tutankhamen-vol1.txt, "
        "letters only. Exact per offset (undecided counted). Statistic fixed before the run: fitting offsets per (direction, "
        "form) on K4 against the ten coppers' range. Two-alphabet count: C(c) = P(p) + N(k) with the key numbered on P or "
        "on C; rank of the 24 equations mod 13 over the place variables, checks = 24 - rank, at 2,000 offsets per source "
        "(Carter, K1-K3 plaintexts, the sculpture's ciphertext panel)."
    ),
    "hypothesis_eli5": (
        "A running key takes a long text, here Carter's book about opening Tutankhamun's tomb, which K3 quotes, and uses "
        "its letters one after another as the key. With an alphabet in an unknown order, each known letter gives an "
        "equation about the alphabet alone. For every starting point in the book, forwards and backwards, a search "
        "decides whether any alphabet satisfies all 24, on the carved text and on scrambled copies. We also count "
        "whether, with two unknown alphabets, the known letters could ever rule anything out."
    ),
    "prediction": (
        "No offset fits K4 in any form or direction; the coppers give 0 or a handful; undecided offsets resolve to dead at "
        "the higher limit. Two unknown alphabets leave no checks at any offset of any source (the equations' unknowns "
        "outnumber them), so that cell is blocked by structure. Zero candidates."
    ),
    "method": (
        "1. Compile the solver; check it against Python on 300 random Carter offsets on K4 and on a planted text. "
        "2. For K4 and 10 coppers, both directions: every offset, three forms, limit 20,000; re-decide the undecided at 100,000 while time allows. "
        "3. Count fits per (direction, form); decrypt K4's fits. "
        "4. Two alphabets: rank mod 13 at 2,000 offsets of each source."
    ),
    "walkthrough": (
        "1. Write Carter's book as one long string of letters and lay it under K4 from some letter onwards. "
        "2. At known place 22 (E under F) the book's letter there, say T, gives: place(F) = place(E) + place(T) in the unknown alphabet. "
        "3. The 24 known places give 24 such equations in the 26 unknown places. "
        "4. Search for one alphabet order that satisfies them all; none means this starting point is dead. "
        "5. Repeat from every letter of the book, with the book reversed, for the three ways of using the table, and on scrambled copies."
    ),
}

import ctypes
import os
import random
import re
import subprocess
import tempfile
import time

N = 97
N_CONTROLS = 10
LIMIT1, LIMIT2 = 20000, 100000
CARTER = "knowledge/sources/carter-1923-tomb-of-tutankhamen-vol1.txt"
FORMS = ("V", "B", "R")

C_SOURCE = r"""
// Running key on one unknown alphabet: for each offset, equations a*x[c] + b*x[p] + d*x[k] = 0 (mod 26) over the
// 26 letter places, one-to-one; decided by depth-first search with propagation. Returns per-offset status.
#include <stdint.h>
#include <string.h>

#define NE 24
static int EV[NE][3], EA[NE][3], NEQ;      // variables and coefficients (merged), per equation
static int X[26], USED[26];
static long NODES, LIMIT;

static int propagate(int *trail, int *nt) {
    int changed = 1;
    while (changed) {
        changed = 0;
        for (int e = 0; e < NEQ; e++) {
            int open = -1, nopen = 0, s = 0;
            for (int j = 0; j < 3; j++) {
                if (!EA[e][j]) continue;
                int v = EV[e][j];
                if (X[v] < 0) { if (open != v) { nopen++; open = v; } }
                else s += EA[e][j] * X[v];
            }
            // coefficient of the open variable (it may appear twice)
            if (nopen == 0) { if (((s % 26) + 26) % 26) return 0; continue; }
            if (nopen > 1) continue;
            int a = 0;
            for (int j = 0; j < 3; j++) if (EA[e][j] && EV[e][j] == open) a += EA[e][j];
            a = ((a % 26) + 26) % 26;
            int sols = 0, last = -1;
            for (int t = 0; t < 26; t++) if (!USED[t] && ((a * t + s) % 26 + 26) % 26 == 0) { sols++; last = t; }
            if (!sols) return 0;
            if (sols == 1) { X[open] = last; USED[last] = 1; trail[(*nt)++] = open; changed = 1; }
        }
    }
    return 1;
}

static int VARS[26], NV;
static int dfs(void) {
    if (++NODES > LIMIT) return -1;
    int trail[26], nt = 0;
    if (!propagate(trail, &nt)) { for (int i = 0; i < nt; i++) { USED[X[trail[i]]] = 0; X[trail[i]] = -1; } return 0; }
    int pick = -1, best = -1;
    for (int i = 0; i < NV; i++) {
        int v = VARS[i];
        if (X[v] >= 0) continue;
        int sc = 0;
        for (int e = 0; e < NEQ; e++) for (int j = 0; j < 3; j++) if (EA[e][j] && EV[e][j] == v) sc++;
        if (sc > best) { best = sc; pick = v; }
    }
    if (pick < 0) return 1;
    for (int t = 0; t < 26; t++) {
        if (USED[t]) continue;
        X[pick] = t; USED[t] = 1;
        int r = dfs();
        if (r == 1) return 1;
        X[pick] = -1; USED[t] = 0;
        if (r < 0) { for (int i = 0; i < nt; i++) { USED[X[trail[i]]] = 0; X[trail[i]] = -1; } return -1; }
    }
    for (int i = 0; i < nt; i++) { USED[X[trail[i]]] = 0; X[trail[i]] = -1; }
    return 0;
}

// form 0 V: x(c) = x(p) + x(k); 1 B: x(c) = x(k) - x(p); 2 R: x(c) = x(p) - x(k)
static int decide(const int *cs, const int *ps, const int *ks, int form) {
    NEQ = 0;
    int inv = 1;
    for (int e = 0; e < NE; e++) {
        int a[3] = {1, 0, 0}, v[3] = {cs[e], ps[e], ks[e]};
        if (form == 0) { a[1] = -1; a[2] = -1; }
        else if (form == 1) { a[1] = 1; a[2] = -1; }
        else { a[1] = -1; a[2] = 1; }
        // merge repeated variables
        for (int i = 0; i < 3; i++) for (int j = i + 1; j < 3; j++) if (a[j] && v[j] == v[i]) { a[i] += a[j]; a[j] = 0; }
        int any = 0;
        for (int j = 0; j < 3; j++) { a[j] = ((a[j] % 26) + 26) % 26; if (a[j]) any = 1; EV[NEQ][j] = v[j]; EA[NEQ][j] = a[j]; }
        int sum = (a[0] + a[1] + a[2]) % 26;
        if (sum) inv = 0;
        if (any) NEQ++;
    }
    for (int i = 0; i < 26; i++) { X[i] = -1; USED[i] = 0; }
    int seen[26] = {0}; NV = 0;
    for (int e = 0; e < NEQ; e++) for (int j = 0; j < 3; j++) if (EA[e][j] && !seen[EV[e][j]]) { seen[EV[e][j]] = 1; VARS[NV++] = EV[e][j]; }
    if (!NEQ) return 1;
    if (inv) { X[VARS[0]] = 0; USED[0] = 1; }       // translation symmetry
    NODES = 0;
    int r = dfs();
    return r;     // 1 fit, 0 dead, -1 undecided
}

// For a text (ct letters at the 24 known places, plaintext letters), a key stream (len n), every offset o with
// key letter at place q = key[o + q - 1] (forward) and the three forms: out[(o*3+form)] = status.
// Counts are returned; statuses for fits written to fit_list (offset*3+form), up to cap.
void scan(const int *cpos, const int *cl, const int *pl, const int *key, int n, long limit,
          long *counts, int *fit_list, int cap, int *nfit, int *und_list, int ucap, int *nund) {
    LIMIT = limit;
    int ks[NE];
    for (int o = 0; o + 97 <= n; o++) {
        for (int e = 0; e < NE; e++) ks[e] = key[o + cpos[e]];
        for (int f = 0; f < 3; f++) {
            int r = decide(cl, pl, ks, f);
            if (r == 1) { counts[f * 3 + 0]++; if (*nfit < cap) fit_list[(*nfit)++] = o * 3 + f; }
            else if (r == 0) counts[f * 3 + 1]++;
            else { counts[f * 3 + 2]++; if (*nund < ucap) und_list[(*nund)++] = o * 3 + f; }
        }
    }
}

int decide_one(const int *cl, const int *pl, const int *ks, int form, long limit, int *xout) {
    LIMIT = limit;
    int r = decide(cl, pl, ks, form);
    for (int i = 0; i < 26; i++) xout[i] = X[i];
    return r;
}
"""

_LIB = {}


def lib():
    if "lib" not in _LIB:
        d = tempfile.mkdtemp(prefix="k4_f18_")
        src, so = os.path.join(d, "rk.c"), os.path.join(d, "rk.so")
        open(src, "w").write(C_SOURCE)
        subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", so, src], check=True, capture_output=True)
        _LIB["lib"] = ctypes.CDLL(so)
    return _LIB["lib"]


def I(v):
    return (ctypes.c_int * len(v))(*v)


def py_rows(cl, pl, ks, f):
    rows = []
    for c, p, k in zip(cl, pl, ks):
        d = {}

        def add(v, a):
            d[v] = (d.get(v, 0) + a) % 26
        add(c, 1)
        if f == 0:
            add(p, -1); add(k, -1)
        elif f == 1:
            add(p, 1); add(k, -1)
        else:
            add(p, -1); add(k, 1)
        rows.append({v: a for v, a in d.items() if a})
    return rows


def py_solve(rows, limit=200000):
    rows = [r for r in rows if r]
    vars_ = sorted({v for r in rows for v in r})
    if not rows:
        return "fit"
    x, used, nodes, trail = {}, set(), [0], []
    inv = all(sum(r.values()) % 26 == 0 for r in rows)

    def check():
        changed = True
        while changed:
            changed = False
            for r in rows:
                op = [v for v in r if v not in x]
                s = sum(a * x[v] for v, a in r.items() if v in x) % 26
                if not op:
                    if s:
                        return False
                elif len(op) == 1:
                    v = op[0]
                    sols = [t for t in range(26) if (r[v] * t + s) % 26 == 0 and t not in used]
                    if not sols:
                        return False
                    if len(sols) == 1:
                        x[v] = sols[0]; used.add(sols[0]); trail.append(v); changed = True
        return True

    def dfs():
        nodes[0] += 1
        if nodes[0] > limit:
            return None
        mark = len(trail)
        if not check():
            while len(trail) > mark:
                v = trail.pop(); used.discard(x.pop(v))
            return False
        op = [v for v in vars_ if v not in x]
        if not op:
            return True
        v = max(op, key=lambda u: sum(1 for r in rows if u in r))
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
        v0 = max(vars_, key=lambda u: sum(1 for r in rows if u in r)); x[v0] = 0; used.add(0); trail.append(v0)
    r = dfs()
    return "undecided" if r is None else ("fit" if r else "dead")


def _scan(args):
    t, text, keytext, direction, known, deadline = args
    L_ = lib()
    kp = sorted(known)
    cpos = [q - 1 for q in kp]
    cl = [ord(text[q - 1]) - 65 for q in kp]; pl = [ord(known[q]) - 65 for q in kp]
    key = [ord(ch) - 65 for ch in (keytext if direction == "fwd" else keytext[::-1])]
    counts = (ctypes.c_long * 9)(); fl = (ctypes.c_int * 20000)(); nf = ctypes.c_int(0)
    ul = (ctypes.c_int * 200000)(); nu = ctypes.c_int(0)
    L_.scan(I(cpos), I(cl), I(pl), I(key), len(key), LIMIT1, counts, fl, 20000, ctypes.byref(nf), ul, 200000, ctypes.byref(nu))
    res = {f: {"fit": counts[i * 3], "dead": counts[i * 3 + 1], "undecided": counts[i * 3 + 2]} for i, f in enumerate(FORMS)}
    fits = [(fl[j] // 3, FORMS[fl[j] % 3]) for j in range(nf.value)]
    second = {f: {"fit": 0, "dead": 0, "undecided": 0} for f in FORMS}
    xo = (ctypes.c_int * 26)()
    CL, PL = I(cl), I(pl)
    skipped = 0
    for j in range(nu.value):
        if time.time() > deadline:
            skipped = nu.value - j
            break
        o, fi = ul[j] // 3, ul[j] % 3
        ks = [key[o + c] for c in cpos]
        r2 = L_.decide_one(CL, PL, I(ks), fi, LIMIT2, xo)
        second[FORMS[fi]][{1: "fit", 0: "dead", -1: "undecided"}[r2]] += 1
        if r2 == 1:
            fits.append((o, FORMS[fi]))
    second["not_redecided"] = skipped
    return t, direction, res, second, fits[:50]


def checks_two_alphabets(keytext, rng, known, n_off=2000):
    """Checks left by C(c) = P(p) + N(k) at sampled offsets: 24 - rank mod 13, key numbered on P or on C."""
    kp = sorted(known)
    out = {}
    for on in ("P", "C"):
        vals = []
        for _ in range(n_off):
            o = rng.randrange(len(keytext) - 100)
            idx, rows = {}, []
            for q in kp:
                c, p, k = ("C", ord(KTEXT[q - 1]) - 65), ("P", ord(known[q]) - 65), (on, ord(keytext[o + q - 1]) - 65)
                r = {}
                for v, a in ((c, 1), (p, -1), (k, -1)):
                    j = idx.setdefault(v, len(idx)); r[j] = (r.get(j, 0) + a) % 13
                rows.append(r)
            M = [[r.get(j, 0) for j in range(len(idx))] for r in rows]
            rank, col = 0, 0
            ncol = len(idx)
            for col in range(ncol):
                pr = next((i for i in range(rank, len(M)) if M[i][col]), None)
                if pr is None:
                    continue
                M[rank], M[pr] = M[pr], M[rank]
                inv = pow(M[rank][col], 11, 13)
                M[rank] = [(x * inv) % 13 for x in M[rank]]
                for i in range(len(M)):
                    if i != rank and M[i][col]:
                        f = M[i][col]; M[i] = [(a - f * b) % 13 for a, b in zip(M[i], M[rank])]
                rank += 1
            vals.append(24 - rank)
        out[on] = {"min": min(vals), "mean": round(sum(vals) / len(vals), 2), "max": max(vals)}
    return out


KTEXT = ""


def run(ctx):
    import multiprocessing as mp
    import sys
    import types
    import json
    global KTEXT
    ct, known = ctx.K4, ctx.KNOWN
    KTEXT = ct
    carter = re.sub("[^A-Z]", "", open(CARTER, errors="ignore").read().upper())
    L_ = lib()
    kp = sorted(known)
    cpos = [q - 1 for q in kp]
    cl = [ord(ct[q - 1]) - 65 for q in kp]; pl = [ord(known[q]) - 65 for q in kp]
    vr = random.Random(1480)
    xo = (ctypes.c_int * 26)()
    for _ in range(300):
        o = vr.randrange(len(carter) - 100); f = vr.randrange(3)
        ks = [ord(carter[o + c]) - 65 for c in cpos]
        r = L_.decide_one(I(cl), I(pl), I(ks), f, 200000, xo)
        assert {1: "fit", 0: "dead", -1: "undecided"}[r] == py_solve(py_rows(cl, pl, ks, f)), (o, f)
    from kryptos.facts import STANDARD_ALPHABET as STD
    al = list(STD); vr.shuffle(al); pos = {ch: i for i, ch in enumerate(al)}
    o = 123457; pt = list(carter[50000:50097])
    for q, a in known.items():
        pt[q - 1] = a
    pc = "".join(al[(pos[p] + pos[carter[o + i]]) % 26] for i, p in enumerate(pt))
    ks = [ord(carter[o + c]) - 65 for c in cpos]
    assert L_.decide_one(I([ord(pc[c]) - 65 for c in cpos]), I(pl), I(ks), 0, 200000, xo) == 1
    rng = random.Random(148)
    sources = {"carter": carter}
    for f_, key in (("k1", "plaintext"), ("k2", "plaintext_as_carved"), ("k3", "plaintext")):
        d = json.load(open(f"data/{f_}.json"))
        sources[f_] = re.sub("[^A-Z]", "", d[key].upper())
    s_ = open("knowledge/01-facts.md").read()
    blk = s_[s_.index("Upper-left plate"):s_.index("## K4")]
    sources["cipher_panel"] = "".join(l.split()[0].replace("?", "") for l in blk.splitlines() if l.split() and l.split()[0].replace("?", "").isalpha() and l.split()[0].isupper())
    crng = random.Random(1483)
    two = {name: checks_two_alphabets(txt, crng, known, 2000 if len(txt) > 2000 else 300) for name, txt in sources.items() if len(txt) > 100}
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    deadline = ctx.deadline - 150
    jobs = [(t, x, carter, d, known, deadline) for t, x in enumerate(texts) for d in ("fwd", "rev")]
    if getattr(sys.modules.get(__name__), "_scan", None) is not _scan:
        m = types.ModuleType(__name__); m.__dict__.update(globals()); sys.modules[__name__] = m
    with mp.get_context("fork").Pool(8) as pool:
        res = pool.map(_scan, jobs, chunksize=1)
    T = len(texts)
    fits = {(t, d): sum(r[f]["fit"] + s[f]["fit"] for f in FORMS) for t, d, r, s, fl in res}
    und = {(t, d): sum(s[f]["undecided"] for f in FORMS) + s["not_redecided"] for t, d, r, s, fl in res}
    k4 = {d: {f: {"fit": r[f]["fit"] + s[f]["fit"], "undecided_after_second_pass": s[f]["undecided"]} for f in FORMS} for t, d, r, s, fl in res if t == 0}
    k4_fits = [fl for t, d, r, s, fl in res if t == 0]
    ctrl = [fits[(t, "fwd")] + fits[(t, "rev")] for t in range(1, T)]
    bounds = {
        "family": "running key from Carter's book (both directions, every offset) on one unknown alphabet, three forms; two-alphabet check counts for every running-key source",
        "carter_letters": len(carter), "offsets_per_direction": len(carter) - 96,
        "solver": f"compiled propagation search, limit {LIMIT1:,} then {LIMIT2:,}; agrees with a Python solver on 300 random offsets; a planted text fits",
        "k4": k4, "k4_fits_total": fits[(0, "fwd")] + fits[(0, "rev")], "k4_fit_list": k4_fits,
        "controls_fits_total": ctrl, "k4_undecided_left": und[(0, "fwd")] + und[(0, "rev")],
        "controls_undecided_left": [und[(t, "fwd")] + und[(t, "rev")] for t in range(1, T)],
        "two_alphabets_checks_by_source": two,
        "controls": f"{N_CONTROLS} shuffled coppers (seed 148), identical scan", "exhaustive": "exact per offset; undecided counted",
    }
    notes = (f"K4 fitting offsets {bounds['k4_fits_total']} (coppers {min(ctrl)}-{max(ctrl)}), undecided left {bounds['k4_undecided_left']}; "
             f"two alphabets, checks by source: " + ", ".join(f"{k} {v['P']['max']}/{v['C']['max']} max" for k, v in two.items()))
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    carter = re.sub("[^A-Z]", "", open(CARTER, errors="ignore").read().upper())
    o = 1000
    lines = [f"Carter's book from letter {o + 1}, under K4; one unknown alphabet, added form", ""]
    for q in (22, 23, 24, 25, 64, 65):
        lines.append(f"place {q}: place({ct[q - 1]}) = place({known[q]}) + place({carter[o + q - 1]})")
    lines += ["...", "24 equations in the unknown places, decided exactly at every starting letter"]
    return "\n".join(lines)
