"""Experiment 0197 (F9.1). See program.md for the contract."""

EXPERIMENT = {
    "slug": "substitution-then-every-newer-move",
    "title": "F9.1: a one-to-one letter substitution, then each hand transposition built since 0106 (compass routes, keyword shapes, keyed blanks, row reshuffles, French diagonal, EVA, Chiffre XIII, YAR, the plate layout, the poem code): exact",
    "family": "9-substitution-then-transposition",
    "parent": "0106-one-to-one-substitution-with-every-move-so-far",
    "changed": (
        "F9.1. The list first: hand transpositions outside 0106's 1.86 million routes, each built since for F6, with its "
        "size: compass-direction readings and pairs (0159, 110,820), keyword-disrupted, triangle, interrupted and "
        "trapezoid columnars (0164, 1.40 million), keyed blank cells, in-row reshuffles and the French diagonal (0165, "
        "4.08 million), EVA's double triangle (0166, 3,840), Chiffre XIII's shaped mask as a move (0166, 2.25 million), "
        "YAR's counting-off orders (0166, 24), paths over the copper's layout (0184, 73) and the poem code's double "
        "columnars (0190, 6,092). Not in this run: the 105.5 million mixed matrix triples (0158), 20.4 million keyword "
        "triples (0162) and 116 million Nihilist routes (0167), whose builders are compiled into their experiments' "
        "testers. Each route, forward and inverse, with 0106's test: a one-to-one substitution commutes with the move, so "
        "equal known letters must land on equal carved letters and different on different. Builders reused from the "
        "committed experiments; the test compiled; K4 against 10 shuffled copies."
    ),
    "hypothesis_expert": (
        "F9 (the Zodiac 340 construction: substitution first, transposition last; 0018 found it the only construction "
        "making the width-21 repeats), A9. Model: c = route(sigma(p)) with sigma any permutation of the 26 letters. 24 "
        "known letters, 13 different: 11 equalities and the inequalities between them, a strong test (0106 found no "
        "survivor in 1.86 million routes). Statistic: surviving routes, K4 against copies."
    ),
    "hypothesis_eli5": (
        "Perhaps the letters were first swapped for other letters by a fixed code alphabet and then shuffled into a new "
        "order. Then wherever the message has the same letter, the copper must have the same letter after unshuffling. "
        "That simple rule was checked for 1.86 million shuffles before; here for every newer shuffle the project has "
        "built since, about eight million of them."
    ),
    "prediction": "No route survives on K4 or on the copies, as in 0106. Zero candidates.",
    "method": (
        "1. Load each committed experiment's route builder. "
        "2. Build the routes in parallel chunks, forward and inverse. "
        "3. For each route and text: the carved letters at the 24 known letters' landing places must match the known "
        "letters one to one (compiled). "
        "4. Count survivors per text; K4 against 10 shuffled copies; a planted text as a builder check."
    ),
    "walkthrough": (
        "1. Take a route: it says where each message letter is carved. "
        "2. Follow the three Es of EASTNORTHEAST and BERLINCLOCK to their carved places: all three must show the same "
        "carved letter. "
        "3. The A, S, T, N, O, R, L, C must likewise each show one carved letter, all different from one another. "
        "4. One mismatch kills the route. "
        "5. About eight million routes, on K4 and on scrambled copies."
    ),
}

import ctypes
import importlib.util
import os
import random
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from kryptos.facts import KNOWN

N = 97
N_CONTROLS = 10
WORKERS = 8
PLACES = sorted(KNOWN)
EXP = Path("experiments")

C_SOURCE = r"""
// one-to-one substitution then a move: carved letter at M[kp[e]] must biject with the known letter
static int KP[24], PL[24], NT, TX[16][97];
void setup(int nt, const int *tx, const int *kp, const int *pl) {
    NT = nt;
    for (int t = 0; t < nt; t++) for (int j = 0; j < 97; j++) TX[t][j] = tx[t * 97 + j];
    for (int e = 0; e < 24; e++) { KP[e] = kp[e]; PL[e] = pl[e]; }
}
void test(const int *maps, int n, long *counts, int *surv, int cap, int *ns) {
    for (int m = 0; m < n; m++) {
        const int *M = maps + 97 * m;
        for (int t = 0; t < NT; t++) {
            int a[26], b[26], ok = 1;
            for (int x = 0; x < 26; x++) { a[x] = -1; b[x] = -1; }
            for (int e = 0; e < 24 && ok; e++) {
                int c = TX[t][M[KP[e]]], p = PL[e];
                if (a[p] < 0 && b[c] < 0) { a[p] = c; b[c] = p; }
                else if (a[p] != c || b[c] != p) ok = 0;
            }
            if (ok) { counts[t]++; if (t == 0 && *ns < cap) surv[(*ns)++] = m; }
        }
    }
}
"""
SO = None
MODS = {}


def load(tag):
    d = [p for p in EXP.iterdir() if p.name.startswith(tag + "-")][0]
    spec = importlib.util.spec_from_file_location(f"e{tag}", d / "attack.py")
    m = importlib.util.module_from_spec(spec)
    sys.modules[f"e{tag}"] = m
    spec.loader.exec_module(m)
    return m


def where(seq):
    wh = [0] * len(seq)
    for j, i in enumerate(seq):
        wh[i] = j
    return wh


def inverse(m):
    inv = [0] * len(m)
    for i, j in enumerate(m):
        inv[j] = i
    return inv


def build_maps(task):
    """task -> list of (name, where-map)"""
    src, item, chunk = task
    out = []
    if src == "0159":
        for name, dirn, m in MODS["0159"].all_routes():
            out.append((f"{name} {dirn}", list(m)))
        return out
    if src in ("0164", "0165"):
        base = MODS[src].routes_for(item, chunk)
    elif src == "0166":
        mod = MODS["0166"]
        if item == "F6.13 Chiffre XIII":
            base = []
            for key in chunk:
                w = len(key); R = N - 3 * w
                for l2 in range(1, min(w, R)):
                    l4 = R - l2
                    if not (1 <= l4 <= w - 1):
                        continue
                    for s4 in range(w):
                        base.append((f"{key} {l2} {s4}", mod.where(mod.xiii(key, l2, s4))))
        else:
            base = mod.routes_for(item, chunk)
    elif src == "0184":
        mod = MODS["0184"]
        base = []
        for gname, first in (("K4's four lines", 24), ("lower plate", 14), ("whole left side", 0)):
            cells, k4 = mod.grid(first)
            carved = {cell: i for i, cell in enumerate(k4)}
            for rname, seq in mod.routes(cells).items():
                order = [x for x in seq if x in carved]
                base.append((f"{gname}: {rname}", [carved[x] for x in order]))
    else:
        mod = MODS["0190"]
        base = [(name, mod.double_map(k1, k2)) for name, k1, k2 in chunk]
    for name, m in base:
        out.append((f"{name} fwd", list(m)))
        out.append((f"{name} inv", inverse(m)))
    return out


def worker(args):
    task, texts = args
    maps = build_maps(task)
    seen, named = set(), []
    for name, m in maps:
        if len(m) != N:
            continue
        k = bytes(m)
        if k not in seen:
            seen.add(k); named.append((name, m))
    lib = ctypes.CDLL(SO)
    nt = len(texts)
    lib.setup(nt, (ctypes.c_int * (97 * nt))(*[ord(c) - 65 for t in texts for c in t]),
              (ctypes.c_int * 24)(*[q - 1 for q in PLACES]), (ctypes.c_int * 24)(*[ord(KNOWN[q]) - 65 for q in PLACES]))
    counts = (ctypes.c_long * nt)()
    surv = []
    B = 5000
    for i in range(0, len(named), B):
        part = named[i:i + B]
        flat = [v for _, m in part for v in m]
        s = (ctypes.c_int * 50)(); ns = ctypes.c_int(0)
        lib.test((ctypes.c_int * len(flat))(*flat), len(part), counts, s, 50, ctypes.byref(ns))
        surv += [part[s[j]][0] for j in range(ns.value)]
    return task[0], task[1], len(named), list(counts), surv


def run(ctx):
    global SO
    import multiprocessing as mp
    import types
    t0 = time.time()
    d = tempfile.mkdtemp(prefix="k4_bij_")
    src, so = os.path.join(d, "b.c"), os.path.join(d, "b.so")
    open(src, "w").write(C_SOURCE)
    subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", so, src], check=True, capture_output=True)
    SO = so
    for tag in ("0159", "0164", "0165", "0166", "0184", "0190"):
        MODS[tag] = load(tag)
    ct = ctx.K4
    rng = random.Random(1960)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    # builder check: a plant made with a one-to-one substitution then a 0165 keyed-blank route
    PLANT_P = "USEDTHEEARTHSMAGNETICEASTNORTHEASTRMATIONWASGATHEREDANDTRANSMITBERLINCLOCKUNDTOANUNKNOWNLOCATIONX"
    sig = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"); rng.shuffle(sig)
    pm = MODS["0165"].routes_for("F6.10 keyed blanks", ["PALIMPSEST"])[0][1]
    sub = [sig[ord(ch) - 65] for ch in PLANT_P]
    plant = [""] * N
    for i in range(N):
        plant[pm[i]] = sub[i]
    texts.append("".join(plant))
    w64 = MODS["0164"].keywords(ctx.vocabulary)
    w65 = MODS["0165"].keywords(ctx.vocabulary)
    tasks = [("0159", "compass", None), ("0184", "layout", None), ("0166", "F6.15 YAR", [])]
    ek = MODS["0166"].eva_keys(ctx.vocabulary)
    xk = MODS["0166"].xiii_keys(ctx.vocabulary)
    tasks += [("0166", "F6.12 EVA", ek[i::8]) for i in range(8)]
    tasks += [("0166", "F6.13 Chiffre XIII", xk[i::32]) for i in range(32)]
    for item in ("F6.11 disrupted", "F6.11 triangle", "F6.16 interrupted", "F6.17 trapezoid"):
        tasks += [("0164", item, w64[i::32]) for i in range(32)]
    for item in ("F6.10 keyed blanks", "F6.18 row reshuffle", "F6.19 French diagonal"):
        tasks += [("0165", item, w65[i::32]) for i in range(32)]
    K90 = MODS["0190"].keys()
    tasks += [("0190", "poem code", K90[i::8]) for i in range(8)]
    if getattr(sys.modules.get(__name__), "worker", None) is not worker:
        m = types.ModuleType(__name__); m.__dict__.update(globals()); sys.modules[__name__] = m
    with mp.get_context("fork").Pool(WORKERS) as pool:
        res = pool.map(worker, [(t, texts) for t in tasks], chunksize=1)
    nc = 1 + N_CONTROLS
    per = {}
    tot = [0] * len(texts)
    k4_surv = []
    for src_, item, n, counts, surv in res:
        key = f"{src_} {item}"
        p = per.setdefault(key, {"routes": 0, "k4": 0, "copies": [0] * N_CONTROLS, "plant": 0})
        p["routes"] += n; p["k4"] += counts[0]
        for t in range(N_CONTROLS):
            p["copies"][t] += counts[1 + t]
        p["plant"] += counts[nc]
        for t in range(len(texts)):
            tot[t] += counts[t]
        k4_surv += [f"{key}: {s}" for s in surv]
    bounds = {
        "family": "one-to-one substitution, then each hand move built since 0106 (forward and inverse), exact",
        "routes_by_source": {k: v["routes"] for k, v in per.items()}, "routes_total": sum(v["routes"] for v in per.values()),
        "survivors": {"k4": tot[0], "copies": tot[1:nc], "plant": tot[nc]}, "per_source": per, "k4_survivors": k4_surv[:30],
        "not_run": "0158 mixed triples (105.5M), 0162 keyword triples (20.4M), 0167 Nihilist (116M): builders compiled into their testers",
        "copies": f"{N_CONTROLS} shuffled copies (seed 1960)", "seconds": round(time.time() - t0), "exhaustive": True,
    }
    notes = f"{bounds['routes_total']:,} routes; survivors K4 {tot[0]} (copies {min(tot[1:nc])}-{max(tot[1:nc])}); plant {tot[nc]}"
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct = ctx.K4
    lines = ["the known letters and the carved letters they would have to match one to one, with no move at all:", ""]
    for q in PLACES:
        lines.append(f"place {q}: {KNOWN[q]} -> {ct[q - 1]}")
    return "\n".join(lines)
