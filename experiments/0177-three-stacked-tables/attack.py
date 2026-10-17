"""Experiment 0177 (F3.4). See program.md for the contract."""

EXPERIMENT = {
    "slug": "three-stacked-tables",
    "title": "F3.4: Scheidt's patent with two keyed tables and three repeating keys (N = 2), tables from the KRYPTOS order and its inverse, key lengths 1-10 each: exact",
    "family": "3-two-component-key",
    "parent": "0173-scheidt-patent-sandwich",
    "changed": (
        "F3.4. 0173 decided the patent's text/key relation with one table between two keys. Here N = 2, as the patent "
        "writes it: v = d + P2[b + P1[u + a]] mod 26, three repeating keys a, b, d of length 1-10 each, P1 and P2 each "
        "the KRYPTOS order or its inverse (a standard table collapses to 0173's form), the message letter numbered by "
        "the standard, KRYPTOS or inverse order with either sign (u), and the carved letter read the same way (v): 144 "
        "classes. Each known place ties one slot of each key; any two fix the third, so a compiled search with "
        "propagation decides every cell exactly."
    ),
    "hypothesis_expert": (
        "US 6,075,865 (Scheidt and Wack): O = a_N + pi_N[a_N-1 + ... + pi_1[I + a_0]] mod W; Sanborn's 'triple matrixes' "
        "(reports/Scheidt patents and field ciphers.md, issue #9); C5(b), C6. Model as in 'changed'. A cell (class, La, "
        "Lb, Ld) is live if some a, b, d satisfy all 24 known places; checks: 24 minus the key slots the known places use. "
        "Statistic: live cells by checks, K4 against 20 shuffled coppers; plants as a builder check."
    ),
    "hypothesis_eli5": (
        "Scheidt's patent can stack the shift-and-look-up step: shift, mixed alphabet, shift, mixed alphabet, shift. With "
        "three short secret words as the three shifts, each known letter ties a letter of each word together, and any two "
        "decide the third. A computer search tries every short length for the three words and every way of choosing the "
        "two mixed alphabets, on K4 and on scrambled copies."
    ),
    "prediction": "No cell with 4 or more checks is live on K4; K4's live cells at each number of checks fall inside the coppers' range. Zero candidates.",
    "method": (
        "1. For each class: the message number u and the carved number v at the 24 known places. "
        "2. For each key-length triple 1-10: depth-first search over key slots with propagation (any two slots on a known "
        "place fix the third), node limit 2 million (undecided counted). "
        "3. Count live cells by checks on K4 and 20 coppers; three planted texts must be live in their own cell."
    ),
    "walkthrough": (
        "1. Choose key lengths, say 5, 6 and 7, and the KRYPTOS order for both tables. "
        "2. Place 22: E must become F. Guess the first key's slot 1 (21 mod 5) and the second key's slot 3 (21 mod 6); "
        "the third key's slot 0 (21 mod 7) is then fixed. "
        "3. Every other known place sharing two guessed slots fixes its third slot, and so on. "
        "4. A contradiction sends the search back to change a guess; if every guess dies, the cell is dead. "
        "5. Every length triple and table choice, on K4 and scrambled copies."
    ),
}

import ctypes
import itertools
import os
import random
import subprocess
import tempfile
import time

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY, KNOWN

N_CONTROLS = 20
LMAX = 10
LIMIT = 2000000
PLACES = sorted(KNOWN)
KPL = [q - 1 for q in PLACES]
K = [STD.index(c) for c in KRY]
KI = [K.index(j) for j in range(26)]
T = {"std": list(range(26)), "kry": K, "kry-inv": KI}

C_SOURCE = r"""
// Patent N = 2: carved value v = d + P2[b + P1[u + a]] (mod 26), u from the known letter, v from the carved letter.
// Three repeating keys a (La), b (Lb), d (Ld). Each known place ties one slot of each; any two fix the third.
// Exact by depth-first search with propagation; node limit -> undecided.
#include <string.h>
static int U[24], V[24], SA[24], SB[24], SD[24];
static int P1[26], P1i[26], P2[26], P2i[26];
static int A[32], B[32], D[32], LA, LB, LD;
static long NODES, LIMIT;
static int TR[96], NT;   // trail: encoded var ids

static inline int md(int x) { x %= 26; return x < 0 ? x + 26 : x; }
static int setv(int kind, int s, int val) {
    int *X = kind == 0 ? A : kind == 1 ? B : D;
    X[s] = val; TR[NT++] = kind * 32 + s; return 1;
}
static int propagate(void) {
    int changed = 1;
    while (changed) {
        changed = 0;
        for (int e = 0; e < 24; e++) {
            int a = A[SA[e]], b = B[SB[e]], d = D[SD[e]];
            int k = (a >= 0) + (b >= 0) + (d >= 0);
            if (k < 2) continue;
            if (k == 3) { if (d != md(V[e] - P2[md(b + P1[md(U[e] + a)])])) return 0; continue; }
            if (d < 0) { setv(2, SD[e], md(V[e] - P2[md(b + P1[md(U[e] + a)])])); changed = 1; }
            else if (b < 0) { setv(1, SB[e], md(P2i[md(V[e] - d)] - P1[md(U[e] + a)])); changed = 1; }
            else { setv(0, SA[e], md(P1i[md(P2i[md(V[e] - d)] - b)] - U[e])); changed = 1; }
        }
    }
    return 1;
}
static void undo(int to) { while (NT > to) { int t = TR[--NT]; int kind = t / 32, s = t % 32; (kind == 0 ? A : kind == 1 ? B : D)[s] = -1; } }
static int dfs(void) {
    if (++NODES > LIMIT) return -1;
    int mark = NT;
    if (!propagate()) { undo(mark); return 0; }
    // pick an unknown slot touched by the most constraints that already have one known member
    int best = -1, bk = 0, bs = 0;
    for (int e = 0; e < 24; e++) {
        int a = A[SA[e]], b = B[SB[e]], d = D[SD[e]];
        int k = (a >= 0) + (b >= 0) + (d >= 0);
        if (k == 1 || (k == 0 && best < 0)) {
            int kind = a < 0 ? 0 : 1, s = a < 0 ? SA[e] : SB[e];
            if (a >= 0 && b >= 0) { kind = 2; s = SD[e]; }
            int sc = k == 1 ? 2 : 1;
            if (sc > best) { best = sc; bk = kind; bs = s; }
        }
    }
    if (best < 0) return 1;           // every constraint has 2+ known -> all fixed and checked
    int *X = bk == 0 ? A : bk == 1 ? B : D;
    for (int t = 0; t < 26; t++) {
        int m2 = NT;
        X[bs] = t; TR[NT++] = bk * 32 + bs;
        int r = dfs();
        if (r == 1) { undo(mark); return 1; }
        undo(m2);
        if (r < 0) { undo(mark); return -1; }
    }
    undo(mark);
    return 0;
}
void set_perms(const int *p1, const int *p2) {
    for (int i = 0; i < 26; i++) { P1[i] = p1[i]; P2[i] = p2[i]; P1i[p1[i]] = i; P2i[p2[i]] = i; }
}
// returns 1 fit, 0 dead, -1 undecided
int decide(const int *u, const int *v, const int *kp, int la, int lb, int ld, long limit) {
    LA = la; LB = lb; LD = ld; LIMIT = limit; NODES = 0; NT = 0;
    for (int e = 0; e < 24; e++) { U[e] = u[e]; V[e] = v[e]; SA[e] = kp[e] % la; SB[e] = kp[e] % lb; SD[e] = kp[e] % ld; }
    for (int i = 0; i < 32; i++) { A[i] = B[i] = D[i] = -1; }
    return dfs();
}
long nodes(void) { return NODES; }
"""


def build():
    d = tempfile.mkdtemp(prefix="k4_stack_")
    src, so = os.path.join(d, "s.c"), os.path.join(d, "s.so")
    open(src, "w").write(C_SOURCE)
    subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", so, src], check=True, capture_output=True)
    lib = ctypes.CDLL(so)
    lib.nodes.restype = ctypes.c_long
    return lib


def I(v):
    return (ctypes.c_int * len(v))(*v)


def classes():
    return [(t0, s1, p1, p2, tout, s3) for t0 in T for s1 in (1, -1) for p1 in ("kry", "kry-inv") for p2 in ("kry", "kry-inv")
            for tout in T for s3 in (1, -1)]


def uv(text, cls):
    t0, s1, p1, p2, tout, s3 = cls
    Ti = [T[tout].index(j) for j in range(26)]
    u = [(s1 * T[t0][STD.index(KNOWN[q])]) % 26 for q in PLACES]
    v = [(s3 * Ti[STD.index(text[q - 1])]) % 26 for q in PLACES]
    return u, v


def encipher(p, cls, a, b, d):
    t0, s1, p1, p2, tout, s3 = cls
    out = []
    for i, ch in enumerate(p):
        u = (s1 * T[t0][STD.index(ch)]) % 26
        v = (d[i % len(d)] + T[p2][(b[i % len(b)] + T[p1][(u + a[i % len(a)]) % 26]) % 26]) % 26
        out.append(STD[T[tout][(s3 * v) % 26]])
    return "".join(out)


def checks(la, lb, ld):
    return 24 - len({k % la for k in KPL}) - len({k % lb for k in KPL}) - len({k % ld for k in KPL})


def run(ctx):
    t_start = time.time()
    lib = build()
    ct = ctx.K4
    rng = random.Random(1770)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    CL = classes()
    KP = I(KPL)
    triples = [t for t in itertools.product(range(1, LMAX + 1), repeat=3) if checks(*t) >= 1]

    PLANT_P = "USEDTHEEARTHSMAGNETICEASTNORTHEASTRMATIONWASGATHEREDANDTRANSMITBERLINCLOCKUNDTOANUNKNOWNLOCATIONX"
    plants = []
    for k in range(3):
        cls = CL[rng.randrange(len(CL))]
        la, lb, ld = rng.randint(3, 8), rng.randint(3, 8), rng.randint(3, 8)
        a = [rng.randrange(26) for _ in range(la)]; b = [rng.randrange(26) for _ in range(lb)]; d = [rng.randrange(26) for _ in range(ld)]
        c = encipher(PLANT_P, cls, a, b, d)
        lib.set_perms(I(T[cls[2]]), I(T[cls[3]]))
        u, v = uv(c, cls)
        r = lib.decide(I(u), I(v), KP, la, lb, ld, ctypes.c_long(LIMIT))
        plants.append({"class": "/".join(map(str, cls)), "lengths": [la, lb, ld], "checks": checks(la, lb, ld), "status": r})

    live = [dict() for _ in texts]
    undecided = [0] * len(texts)
    k4_live = []
    max_nodes = 0
    ran = 0
    for ti, text in enumerate(texts):
        for cls in CL:
            lib.set_perms(I(T[cls[2]]), I(T[cls[3]]))
            u, v = uv(text, cls)
            U, V = I(u), I(v)
            for (la, lb, ld) in triples:
                r = lib.decide(U, V, KP, la, lb, ld, ctypes.c_long(LIMIT))
                max_nodes = max(max_nodes, lib.nodes())
                if r < 0:
                    undecided[ti] += 1
                elif r == 1:
                    c = checks(la, lb, ld)
                    live[ti][c] = live[ti].get(c, 0) + 1
                    if ti == 0:
                        k4_live.append({"class": "/".join(map(str, cls)), "lengths": [la, lb, ld], "checks": c})
        ran = ti + 1
        if ctx.time_left() < 60:
            break
    live, undecided = live[:ran], undecided[:ran]

    def at_least(dct, c):
        return sum(v for k, v in dct.items() if k >= c)
    table = {}
    for c in (1, 2, 4, 6, 8, 12):
        cp = [at_least(x, c) for x in live[1:]]
        table[c] = {"k4": at_least(live[0], c), "coppers_min": min(cp), "coppers_max": max(cp)}
    bounds = {
        "family": "patent N = 2: v = d + P2[b + P1[u + a]], P1, P2 in {KRYPTOS, inverse}, u and v on std/KRYPTOS/inverse with signs (144 classes), key lengths 1-10 each, exact",
        "classes": len(CL), "length_triples": len(triples), "cells_per_text": len(CL) * len(triples),
        "live_at_least_checks": table, "live_by_checks_k4": dict(sorted(live[0].items())),
        "undecided": {"k4": undecided[0], "coppers": undecided[1:]}, "max_nodes": max_nodes,
        "k4_live": sorted(k4_live, key=lambda z: -z["checks"])[:40], "plants": plants,
        "copies": f"{ran - 1} of {N_CONTROLS} shuffled coppers run (seed 1770)", "seconds": round(time.time() - t_start), "exhaustive": True,
    }
    notes = (f"live cells with >=4 checks: K4 {table[4]['k4']} (coppers {table[4]['coppers_min']}-{table[4]['coppers_max']}); "
             f">=1: K4 {table[1]['k4']} (coppers {table[1]['coppers_min']}-{table[1]['coppers_max']}); undecided K4 {undecided[0]}; "
             f"plants live {sum(1 for p in plants if p['status'] == 1)}/3")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    cls, a, b, d = key
    return encipher(plaintext, cls, a, b, d)


def worked_example(ctx, key):
    ct = ctx.K4
    lines = ["key lengths 5, 6, 7: the three slots each known place ties together", ""]
    for q in PLACES:
        lines.append(f"place {q}: {KNOWN[q]} -> {ct[q - 1]}: first key slot {(q - 1) % 5}, second {(q - 1) % 6}, third {(q - 1) % 7}")
    lines.append("")
    lines.append(f"slots used: {5 + 6 + 7}; checks: {checks(5, 6, 7)}")
    return "\n".join(lines)
