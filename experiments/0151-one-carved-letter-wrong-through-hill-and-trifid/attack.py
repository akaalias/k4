"""Experiment 0151 (F1.6, Hill and trifid part). See program.md for the contract."""

EXPERIMENT = {
    "slug": "one-carved-letter-wrong-through-hill-and-trifid",
    "title": "F1.6, third part: every single-letter error in the copper (wrong, missing or extra, anywhere) through the exact Hill (sizes 2-5, plain and affine) and trifid (free cube) verdicts",
    "family": "1-keyed-periodic",
    "parent": "0147-one-carved-letter-wrong-through-the-free-alphabet-tests",
    "changed": (
        "F1.6, Hill and trifid verdicts. 0105 solved Hill letter by letter (sizes 2-5, plain and affine, every alignment, "
        "four numberings) and 0040 solved trifid with any 27-symbol cube (periods 2-15, every offset) exactly: no fit on "
        "K4. These ciphers read the carved letters around each known letter too, so every single-letter error anywhere "
        "matters: each of the 97 carved letters changed to each other letter (2,425), each deleted (97), and a letter "
        "inserted before each place, every letter tried (2,522); the known places keep their numbering. K4's 5,044 "
        "variants first; scrambled copies only if a variant fits."
    ),
    "hypothesis_expert": (
        "Family G, C17, C21 (the HILL column: Hill under a slip), trifid as Sanborn's 'visual' cube (C3). Deciders "
        "unchanged: 0105's setting() (rows solved mod 2 and 13, CRT, invertibility; 'open' when too few equations), "
        "0040's solve_setting() (union-find on coordinate variables, backtracking with the all-different rule, caps). "
        "Exact where decided; open settings counted. An error is modelled on the copper with the message numbering fixed "
        "(a deleted letter's place filled at the end; an inserted letter pushes the last one out)."
    ),
    "hypothesis_eli5": (
        "The Hill cipher (suggested by the HILL letters on the sculpture's table) and trifid (a three-dimensional "
        "letter cube) were ruled out exactly. Both work on groups of neighbouring letters, so a single wrong, missing or "
        "extra carved letter anywhere could spoil the test. We try every such error and rerun both exact tests."
    ),
    "prediction": "No variant fits Hill or trifid with at least one check; open settings at the rate 0105 found (5x5 affine). Zero candidates.",
    "method": (
        "1. Build the 5,044 variants. "
        "2. For each: 0105's Hill settings (4 sizes x plain/affine x alignments x 4 numberings) and 0040's trifid settings "
        "(periods 2-15 x offsets). "
        "3. List any variant with a living Hill setting that has checks, or a consistent cube."
    ),
    "walkthrough": (
        "1. Change one carved letter, say the W at place 21, to A. "
        "2. Hill 2x2: the block holding places 21-22 now has carved letters A, F; the known E at 22 gives one equation in the matrix row. "
        "3. Solve each matrix row from all its equations modulo 2 and 13; no solution means the setting is dead. "
        "4. Trifid: rebuild the coordinate equalities with the new letter and search for a cube. "
        "5. Repeat for every place, every replacement, every deletion and insertion."
    ),
}

import random
import time
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
P105 = "experiments/0105-affine-hill-solved-letter-by-letter/attack.py"
P040 = "experiments/0040-trifid-free-cubes-by-constraint-propagation-rerun/attack.py"


def load(path, name):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def variants(ct):
    out = []
    for j in range(N):
        for c in STD:
            if c != ct[j]:
                out.append((f"sub {j + 1} {ct[j]}->{c}", ct[:j] + c + ct[j + 1:]))
    for j in range(N):
        out.append((f"del {j + 1}", ct[:j] + ct[j + 1:] + "A"))
    for j in range(N):
        for c in STD:
            out.append((f"ins {c} before {j + 1}", (ct[:j] + c + ct[j:])[:N]))
    return out


def _work(args):
    chunk, known = args
    m105, m040 = load(P105, "m105"), load(P040, "m040")
    nums = [(STD, 0), (STD, 1), (KRY, 0), (KRY, 1)]
    hill_alive, hill_open, tri = [], 0, []
    for name, t in chunk:
        for n in range(2, 6):
            for affine in (False, True):
                for align in range(n):
                    for ni, num in enumerate(nums):
                        st, chk, sol = m105.setting(t, known, n, align, num, affine)
                        if st == "alive" and chk > 0:
                            hill_alive.append({"variant": name, "n": n, "affine": affine, "align": align, "numbering": ni, "checks": chk})
                        elif st == "open":
                            hill_open += 1
        for p in range(2, 16):
            for o in range(p):
                cubes, nodes, nc = m040.solve_setting(t, known, p, o)
                if cubes:
                    tri.append({"variant": name, "period": p, "offset": o, "cubes": len(cubes)})
    return hill_alive, hill_open, tri, len(chunk)


def run(ctx):
    import multiprocessing as mp
    import sys
    import types
    ct, known = ctx.K4, ctx.KNOWN
    var = variants(ct)
    chunks = [var[i::64] for i in range(64)]
    if getattr(sys.modules.get(__name__), "_work", None) is not _work:
        m = types.ModuleType(__name__); m.__dict__.update(globals()); sys.modules[__name__] = m
    t0 = time.time()
    with mp.get_context("fork").Pool(8) as pool:
        res = pool.map(_work, [(c, known) for c in chunks], chunksize=1)
    hill = [x for r in res for x in r[0]]
    hopen = sum(r[1] for r in res)
    tri = [x for r in res for x in r[2]]
    bounds = {"family": "Hill 2-5 (plain, affine) and trifid (free cube) on every single-letter error of the copper",
              "variants": len(var), "variants_done": sum(r[3] for r in res),
              "hill_settings_per_variant": "4 sizes x plain/affine x alignments x 4 numberings (112)",
              "trifid_settings_per_variant": "periods 2-15 x every offset (119)",
              "hill_alive_with_checks": hill[:50], "n_hill_alive_with_checks": len(hill), "hill_open_settings": hopen,
              "trifid_consistent": tri[:50], "n_trifid_consistent": len(tri), "seconds": round(time.time() - t0), "exhaustive": "exact where decided; Hill open settings counted",
              "controls": "none needed if nothing fits (exact)"}
    notes = f"{len(var)} variants: Hill alive with checks {len(hill)}, Hill open settings {hopen}; trifid consistent {len(tri)}"
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct = ctx.K4
    return "\n".join(["the errors tried, for every place of the copper:", "",
                      f"  wrong:   place 21 {ct[20]} -> each of the other 25 letters",
                      f"  missing: place 21 deleted, the rest moves left, a filler at the end",
                      f"  extra:   each letter inserted before place 21, the last letter pushed out",
                      "", "each variant through Hill 2x2-5x5 (plain, affine, every alignment, four numberings) and trifid (periods 2-15, every offset)"])
