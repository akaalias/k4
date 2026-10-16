"""Experiment 0152 (F1.6, Hill controls). See program.md for the contract."""

EXPERIMENT = {
    "slug": "hill-slip-variants-on-scrambled-copies",
    "title": "F1.6, Hill controls: the same 5,044 single-letter errors on ten scrambled copies, against K4's 257 living Hill settings with a check",
    "family": "1-keyed-periodic",
    "parent": "0151-one-carved-letter-wrong-through-hill-and-trifid",
    "changed": (
        "F1.6. 0151 found 257 (variant, Hill setting) pairs alive with at least one check on K4's 5,044 single-letter "
        "variants, almost all 5x5 plain with a single check, and no trifid cube. An exact fit only means something "
        "against the same test on scrambled copies; here every copy gets the same 5,044 variants and Hill settings."
    ),
    "hypothesis_expert": (
        "As 0151 (0105's Hill decider, sizes 2-5 plain and affine, every alignment, four numberings; a variant is a "
        "carved letter changed, deleted or inserted with the message numbering fixed). Ten shuffled coppers (seed 152). "
        "Statistic fixed before the run: alive-with-checks counts per size; K4's 0151 counts against the coppers' range; "
        "K4 above every copper in a size stops the queue for replication."
    ),
    "hypothesis_eli5": (
        "One slip in the carved text lets some Hill-cipher settings fit the known letters, a few hundred times out of "
        "half a million tries. Is that more than a scrambled copy of the carved text manages? We run the identical test "
        "on ten scrambled copies."
    ),
    "prediction": "Each copper has a similar count (a few hundred, mostly 5x5 plain with one check); K4's 257 lies inside their range in every size.",
    "method": "1. Ten scrambled copies. 2. Each copy's 5,044 variants through 0105's Hill settings. 3. Counts per size against K4's.",
    "walkthrough": (
        "1. Shuffle the carved letters into a new order. "
        "2. Make every single-letter error of the shuffled copy, as for K4. "
        "3. Run the exact Hill test on each and count living settings with a check. "
        "4. Compare with K4's count."
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
    return hill_alive, hill_open, tri, len(chunk)


def run(ctx):
    import multiprocessing as mp
    import sys
    import types
    import json
    from collections import Counter
    ct, known = ctx.K4, ctx.KNOWN
    rng = random.Random(152)
    copies = []
    for _ in range(10):
        sh = list(ct); rng.shuffle(sh); copies.append("".join(sh))
    if getattr(sys.modules.get(__name__), "_work", None) is not _work:
        m = types.ModuleType(__name__); m.__dict__.update(globals()); sys.modules[__name__] = m
    t0 = time.time()
    per = []
    with mp.get_context("fork").Pool(8) as pool:
        for cp in copies:
            var = variants(cp)
            chunks = [var[i::32] for i in range(32)]
            res = pool.map(_work, [(c, known) for c in chunks], chunksize=1)
            hill = [x for r in res for x in r[0]]
            per.append(Counter(f"{x['n']}x{x['n']} {'affine' if x['affine'] else 'plain'}" for x in hill))
            if ctx.time_left() < 120:
                break
    k4 = json.load(open("experiments/0151-one-carved-letter-wrong-through-hill-and-trifid/result.json"))["bounds"]["hill_alive_with_checks"]
    k4_total = json.load(open("experiments/0151-one-carved-letter-wrong-through-hill-and-trifid/result.json"))["bounds"]["n_hill_alive_with_checks"]
    sizes = sorted(set().union(*per) | {"5x5 plain"})
    totals = [sum(c.values()) for c in per]
    bounds = {"family": "Hill 2-5 on every single-letter error of ten scrambled copies (0151's test)",
              "copies_done": len(per), "controls_total_alive_with_checks": totals, "k4_total_0151": k4_total,
              "controls_by_size": {s_: [c.get(s_, 0) for c in per] for s_ in sizes},
              "k4_above_every_copper": k4_total > max(totals), "k4_rank": 1 + sum(1 for x in totals if x > k4_total),
              "seconds": round(time.time() - t0), "controls": "10 shuffled coppers (seed 152), the 5,044 variants of each"}
    notes = f"copies alive-with-checks totals {totals}; K4 (0151) {k4_total}, rank {bounds['k4_rank']} of {len(per) + 1}"
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
