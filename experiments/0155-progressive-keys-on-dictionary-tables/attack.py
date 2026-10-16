"""Experiment 0155 (F1.9). See program.md for the contract."""

EXPERIMENT = {
    "slug": "progressive-keys-on-dictionary-tables",
    "title": "F1.9: progressive keys, per-letter and per-repeat, every step and period 1-52, on the standard, KRYPTOS and every dictionary keyword table, against scrambled copies (Kryha's step of 3 included)",
    "family": "1-keyed-periodic",
    "parent": "0042-progressive-key-on-vocabulary-alphabets",
    "changed": (
        "F1.9. 0011 tested the progressive key (per-repeat and per-letter) on the standard and KRYPTOS tables and 0042 "
        "the per-repeat form on vocabulary tables; the per-letter form on keyword tables, the surviving periods 26-30 "
        "against copies, and Kryha's machine stepping (3 per cycle) at periods 31-52 were open. Here both forms, steps "
        "1-25, periods 1-52, on 0109's tables: every dictionary word of four letters or more as a keyword alphabet "
        "(plain side, cipher side or both, the other side standard or KRYPTOS), plus the 8 standard/KRYPTOS tables, "
        "added and Beaufort forms; the consistency test is compiled C. Ten scrambled copies."
    ),
    "hypothesis_expert": (
        "C5(a), C20 (hand schedules); TM 32-220 par. 125 (progressive key) and Lewis, German Agent Systems (Kryha "
        "stepping, net step 3 per revolution), per research_notes/Scheidt patents and field ciphers/"
        "addendum_downloaded_manuals.md. Model: key value at message place i = w[i mod L] + s i (per-letter) or w[i mod L] "
        "+ s floor(i / L) (per-repeat, 'step per cycle'), w free letters, s 1-25 (the variant form is the added form with "
        "-s). Forced key values at the 24 known places; period L consistent for (table, s, form) if each slot holds one "
        "value of K - progression. Statistic fixed before the run: per (form, period), K4's count of consistent (table, "
        "step) pairs against the ten coppers' range; cells where K4 is above every copper against each copper's count "
        "against the rest; smallest consistent period."
    ),
    "hypothesis_eli5": (
        "In a progressive key the secret word slides along the table by a fixed step, either after every letter or "
        "after every full pass of the word, the way some cipher machines stepped. We try every step and word length "
        "up to 52 on the sculpture's tables and on tables built from every dictionary word, and check against the 24 "
        "known letters and scrambled copies of the carved text."
    ),
    "prediction": (
        "Short periods die for both forms on every table; at 26 and above some survive on K4 at the coppers' rate; K4 above "
        "every copper in no more cells than the null's maximum. Zero candidates."
    ),
    "method": (
        "1. Build the keyword tables (0109's). "
        "2. For each text, table and form: the 24 forced key values. "
        "3. Compiled: for each step 1-25 and period 1-52, per-letter and per-repeat, test slot consistency; count. "
        "4. Compare K4 with the coppers cell by cell."
    ),
    "walkthrough": (
        "1. Take a key word of length 7 and a step of 3 per letter: the key at place i is the word's letter at i mod 7 plus 3 i. "
        "2. On the table, the known letter and the carved letter at each known place fix the key value there. "
        "3. Subtract 3 times the place: what is left must be the same for all known places in one slot (i mod 7). "
        "4. Per repeat instead: subtract 3 times the number of completed passes of the word. "
        "5. Repeat for every step, length, table and form, and on scrambled copies."
    ),
}

import ctypes
import os
import random
import subprocess
import tempfile
from pathlib import Path
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
N_CONTROLS = 10
LMAX = 52
STEPS = list(range(1, 26))
WORKERS = 8
ROOT = Path(__file__).resolve().parent
if not (ROOT / "kryptos").exists():
    ROOT = Path.cwd()

C_SOURCE = r"""
// Progressive key consistency. For each configuration (24 forced key values at the known places), each step s and
// each form: per-letter (v_e = K_e - s * i_e) or per-repeat (v_e = K_e - s * floor(i_e / L)), find which periods L
// leave every slot (i_e mod L) holding one value. Counts per (form, step, period) are accumulated.
#include <stdint.h>
#include <string.h>

// K: nconf x 24 values; pos: 24 message places (0-based); steps: list; out: counts[form][step_idx][L] (L 1..LMAX)
void scan(const unsigned char *K, int nconf, const int *pos, const int *steps, int nsteps, int lmax_letter, int lmin_rep,
          int lmax_rep, long *out_letter, long *out_rep, int *min_letter, int *min_rep) {
    int slot_v[64];
    for (int c = 0; c < nconf; c++) {
        const unsigned char *k = K + 24 * c;
        for (int si = 0; si < nsteps; si++) {
            int s = steps[si];
            // per-letter
            for (int L = 1; L <= lmax_letter; L++) {
                for (int j = 0; j < L; j++) slot_v[j] = -1;
                int ok = 1;
                for (int e = 0; e < 24 && ok; e++) {
                    int v = ((k[e] - s * pos[e]) % 26 + 26) % 26;
                    int sl = pos[e] % L;
                    if (slot_v[sl] < 0) slot_v[sl] = v; else if (slot_v[sl] != v) ok = 0;
                }
                if (ok) { out_letter[si * (lmax_letter + 1) + L]++; if (L < *min_letter) *min_letter = L; }
            }
            // per-repeat
            for (int L = lmin_rep; L <= lmax_rep; L++) {
                for (int j = 0; j < L; j++) slot_v[j] = -1;
                int ok = 1;
                for (int e = 0; e < 24 && ok; e++) {
                    int v = ((k[e] - s * (pos[e] / L)) % 26 + 26) % 26;
                    int sl = pos[e] % L;
                    if (slot_v[sl] < 0) slot_v[sl] = v; else if (slot_v[sl] != v) ok = 0;
                }
                if (ok) { out_rep[si * (lmax_rep + 1) + L]++; if (L < *min_rep) *min_rep = L; }
            }
        }
    }
}
"""


def keyed(word):
    seen = []
    for c in word:
        if c not in seen:
            seen.append(c)
    return "".join(seen) + "".join(c for c in STD if c not in seen)


def lib():
    d = tempfile.mkdtemp(prefix="k4_f19_")
    src, so = os.path.join(d, "p.c"), os.path.join(d, "p.so")
    open(src, "w").write(C_SOURCE)
    subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", so, src], check=True, capture_output=True)
    return ctypes.CDLL(so)


def tables():
    words = [w.strip().upper() for w in (ROOT / "kryptos" / "data" / "words.txt").read_text().split()]
    words = [w for w in words if len(w) >= 4 and w.isalpha()]
    alphas = {}
    for w in words:
        a = keyed(w)
        if a not in alphas and a not in (STD, KRY):
            alphas[a] = w
    out = [(STD, STD), (STD, KRY), (KRY, STD), (KRY, KRY)]
    for a in alphas:
        out += [(a, a), (a, STD), (STD, a), (a, KRY), (KRY, a)]
    return out


def _work(args):
    share, texts, known = args
    L_ = lib()
    pos = [q - 1 for q in sorted(known)]
    P = (ctypes.c_int * 24)(*pos)
    S = (ctypes.c_int * len(STEPS))(*STEPS)
    T = len(texts)
    res = []
    for t, txt in enumerate(texts):
        buf = bytearray()
        for pa, ca in share:
            PI = {c: i for i, c in enumerate(pa)}; CI = {c: i for i, c in enumerate(ca)}
            pk = [PI[known[q]] for q in sorted(known)]
            ck = [CI[txt[q - 1]] for q in sorted(known)]
            buf += bytes((c - p) % 26 for c, p in zip(ck, pk))
            buf += bytes((c + p) % 26 for c, p in zip(ck, pk))
        nconf = len(buf) // 24
        K = (ctypes.c_ubyte * len(buf)).from_buffer(buf)
        ol = (ctypes.c_long * (len(STEPS) * (LMAX + 1)))(); orp = (ctypes.c_long * (len(STEPS) * (LMAX + 1)))()
        ml, mr = ctypes.c_int(999), ctypes.c_int(999)
        L_.scan(K, nconf, P, S, len(STEPS), LMAX, 1, LMAX, ol, orp, ctypes.byref(ml), ctypes.byref(mr))
        res.append((list(ol), list(orp)))
    return res


def run(ctx):
    import multiprocessing as mp
    import sys
    import types
    ct, known = ctx.K4, ctx.KNOWN
    tabs = tables()
    rng = random.Random(1590)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    T = len(texts)
    if getattr(sys.modules.get(__name__), "_work", None) is not _work:
        m = types.ModuleType(__name__); m.__dict__.update(globals()); sys.modules[__name__] = m
    with mp.get_context("fork").Pool(WORKERS) as pool:
        parts = pool.map(_work, [(tabs[i::WORKERS * 4], texts, known) for i in range(WORKERS * 4)], chunksize=1)
    W = LMAX + 1
    live = {f: [[0] * W for _ in range(T)] for f in ("letter", "repeat")}
    for part in parts:
        for t, (ol, orp) in enumerate(part):
            for si in range(len(STEPS)):
                for L in range(1, W):
                    live["letter"][t][L] += ol[si * W + L]
                    live["repeat"][t][L] += orp[si * W + L]
    # step 3 per repeat at 31-52 (Kryha) reported apart
    cells = [(f, L) for f in ("letter", "repeat") for L in range(1, W)]

    def above_rest(t):
        return [f"{f}:{L}" for f, L in cells if live[f][t][L] > max(live[f][u][L] for u in range(T) if u != t)]
    k4_above = above_rest(0)
    null = [len(above_rest(t)) for t in range(1, T)]
    stop = len(k4_above) > max(null)
    first = {f: next((L for L in range(1, W) if live[f][0][L]), None) for f in live}
    cfirst = {f: min(next((L for L in range(1, W) if live[f][t][L]), 99) for t in range(1, T)) for f in live}
    bounds = {"family": "progressive key, per-letter and per-repeat, steps 1-25, periods 1-52, on 0109's dictionary keyword tables plus standard/KRYPTOS",
              "tables": len(tabs), "forms_per_table": ["added", "Beaufort"], "steps": [1, 25], "periods": [1, LMAX],
              "k4_live_by_period": {f: live[f][0][1:] for f in live},
              "controls_min_by_period": {f: [min(live[f][t][L] for t in range(1, T)) for L in range(1, W)] for f in live},
              "controls_max_by_period": {f: [max(live[f][t][L] for t in range(1, T)) for L in range(1, W)] for f in live},
              "k4_shortest_live": first, "coppers_shortest_live": cfirst,
              "cells_k4_above_every_copper": k4_above, "null_cells_above_rest_per_copper": null, "stop_queue": stop,
              "kryha_note": "step 3 per repeat at 31-52 is inside the per-repeat counts (all steps summed)",
              "controls": f"{N_CONTROLS} shuffled coppers (seed 1590)", "exhaustive": True}
    notes = (f"{len(tabs):,} tables x 2 forms x 25 steps: shortest live period on K4 per-letter {first['letter']}, per-repeat {first['repeat']} "
             f"(coppers {cfirst['letter']}, {cfirst['repeat']}); K4 above every copper in {len(k4_above)} of {len(cells)} cells, null {min(null)}-{max(null)}; stop {stop}")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    K = [(KRY.index(ct[q - 1]) - KRY.index(known[q])) % 26 for q in sorted(known)]
    lines = ["sculpture's table, Vigenere: key value forced at each known place, then minus 3 x place (per-letter step 3), slot = place mod 7", "",
             "place  key value  minus 3i  slot"]
    for q, k in zip(sorted(known), K):
        if q in (22, 23, 29, 30, 64, 71):
            lines.append(f"{q:5d}  {k:9d}  {(k - 3 * (q - 1)) % 26:8d}  {(q - 1) % 7:4d}")
    lines.append("places 22 and 29 share slot 0 and must leave the same value")
    return "\n".join(lines)
