"""Experiment: F16.4c. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f16.4c-line-keyed-schemes-on-one-free-alphabet",
    "title": "F16.4c: one free alphabet on both sides with a repeating key of 1-26 and an unknown offset on each carved line (the key running on, or restarted at each line): 0119's exact decider with the offsets as extra unknowns, both forms, on the 24 and the 20 official letters; K4 against 100 shuffles",
    "family": "16-simple-hand-methods",
    "parent": "0119-one-free-alphabet-exact-at-every-key-length",
    "changed": (
        "F16.4c (issue #123). 0288 found no sign of the carved line in the small shifts, so this row runs without a "
        "lead (run more experiments, #100). 0119's decide() from its frozen attack.py, with one change, checked "
        "against the original on K4: each known place's key is a sum of unknowns, key[slot] + offset[carved line], "
        "instead of key[slot] alone. Two models: OFFSET (slot = place mod L, the key runs on across lines) and BOTH "
        "(slot = column in the carved line mod L, the key restarts at each line, and each line has its offset). A "
        "restart with no offset on a free alphabet was decided in F1.4 (0253). On the 24 and the 20 official letters. "
        "Strength aimed at: exact per cell; the comparison with shuffles is a count."
    ),
    "hypothesis_expert": (
        "C27(b), C27(c) (his tableau 'slightly different from the one on Kryptos': one unknown alphabet on both "
        "sides), A7. Quagmire III with a free alphabet A (any of 26! orders): A(c) = A(p) + k (V) or A(c) = k - A(p) "
        "(B), k = key[slot] + off[line], lines at K4 places 1-4, 5-35, 36-66, 67-97 (known letters on lines 2, 3, 4). "
        "Decided exactly as 0119: the linear system mod 13 and mod 2 (CRT), a one-to-one alphabet needs each residue "
        "mod 13 to hold at most two letters that differ mod 2; small solution spaces enumerated, larger ones searched "
        "depth-first to a node limit (undecided cells are reported). The two offsets remove two checks, so more cells "
        "fit than in 0119 (added form dead at 1-26; Beaufort alive at 23 and 26 only). 0274 showed a count of fitting "
        "cells cannot pick out a plant; what this run can show is K4 dead where shuffles fit or the reverse, and the "
        "list of cells left for a decider."
    ),
    "hypothesis_eli5": (
        "Suppose Sanborn's table used the alphabet in an order of his own, and he slid the key by a different amount "
        "on each carved line. For each key length we ask whether any alphabet order at all can explain the 24 known "
        "letters, exactly, and compare with scrambled copies of K4."
    ),
    "prediction": (
        "K4 fits about as many cells as its shuffles (inside the 5th-95th percentile in every model and form); no "
        "cell below length 8 fits on the 24 letters. Planted texts fit their own cell every time."
    ),
    "method": (
        "1. For each model, key length 1-26 and form, the 24 (or 20) equations with unknowns: the alphabet's places, "
        "the key letters, an offset per carved line. 2. 0119's exact decision: fit (witness re-checked), dead, or "
        "undecided. 3. K4 and 100 shuffles with the known letters kept. 4. Validation: three planted texts per cell "
        "(random alphabet, key and offsets) must fit; the changed decide() must agree with 0119's on K4 when the "
        "offsets are left out."
    ),
    "walkthrough": (
        "1. Take key length 7 and the form where the key is added. "
        "2. Each known letter gives one equation: place of the carved letter = place of the message letter + key letter of its slot + the offset of its carved line. "
        "3. The unknowns are the 26 places, the 7 key letters and the offsets of lines 3 and 4 against line 2. "
        "4. Solve the equations as far as they go; if they force two letters onto the same place, no alphabet fits. "
        "5. Otherwise search the remaining freedom for an order with every letter on its own place."
    ),
    "expected_minutes": 20,
}

import importlib.util
import multiprocessing as mp
import os
import random
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LMAX = 26
N_CONTROLS = 100
FORMS = ("V", "B")
MODELS = ("offset", "both")
SEED = 16403
LINE_START = {1: -26, 2: 5, 3: 36, 4: 67}
OFFICIAL = set(range(26, 35)) | set(range(64, 75))
_G = {}


def frozen():
    """0119's attack.py with decide() and check_witness() taking a tuple of key unknowns per equation."""
    path = ROOT / "experiments" / "0119-one-free-alphabet-exact-at-every-key-length" / "attack.py"
    src = path.read_text()
    reps = [
        ('    slots = sorted({e[0] for e in eqs})\n    var = {("x", a): i',
         '    slots = sorted({kv for e in eqs for kv in e[0]})\n    var = {("x", a): i'),
        ('        r[var[("k", s)]] = r.get(var[("k", s)], 0) - 1\n',
         '        for kv in s:\n            r[var[("k", kv)]] = r.get(var[("k", kv)], 0) - 1\n'),
        ('    return all((x[c] - (sgn * x[p] + k[s])) % 26 == 0 for s, p, c in eqs)',
         '    return all((x[c] - (sgn * x[p] + sum(k[kv] for kv in s))) % 26 == 0 for s, p, c in eqs)'),
    ]
    for old, new in reps:
        assert src.count(old) == 1, old
        src = src.replace(old, new)
    mod = types.ModuleType("frozen0119_lines")
    mod.__file__ = str(path)
    exec(compile(src, str(path), "exec"), mod.__dict__)
    spec = importlib.util.spec_from_file_location("frozen0119", path)
    orig = importlib.util.module_from_spec(spec); spec.loader.exec_module(orig)
    return mod, orig


def line_of(q):
    return 1 if q <= 4 else 2 if q <= 35 else 3 if q <= 66 else 4


def kvars(q, L, model):
    if model == "plain":
        return (("s", (q - 1) % L),)
    if model == "offset":
        return (("s", (q - 1) % L), ("l", line_of(q)))
    return (("s", (q - LINE_START[line_of(q)]) % L), ("l", line_of(q)))


def equations(text, known, L, model, places):
    return [(kvars(q, L, model), ord(known[q]) - 65, ord(text[q - 1]) - 65) for q in places]


def planted(L, form, model, rng, known):
    order = list(range(26)); rng.shuffle(order)
    inv = {v: i for i, v in enumerate(order)}
    key = {("s", s): rng.randrange(26) for s in range(L)}
    key.update({("l", l): rng.randrange(26) for l in (1, 2, 3, 4)})
    pt = [rng.randrange(26) for _ in range(97)]
    for q, ch in known.items():
        pt[q - 1] = ord(ch) - 65
    sgn = 1 if form == "V" else -1
    return "".join(chr(65 + inv[(sgn * order[p] + sum(key[kv] for kv in kvars(i + 1, L, model))) % 26]) for i, p in enumerate(pt))


def _job(args):
    tid, text = args
    mod, known = _G["mod"], _G["known"]
    out = {}
    for sname, places in _G["sets"]:
        for model in MODELS:
            for L in range(1, LMAX + 1):
                eqs = equations(text, known, L, model, places)
                for form in FORMS:
                    st, w = mod.decide(eqs, form, random.Random(SEED + L))
                    if st == "fit":
                        assert mod.check_witness(eqs, form, w)
                    out[f"{sname}/{model}/{form}/{L}"] = st
                    if st == "fit" and tid == "k4":
                        out[f"w:{sname}/{model}/{form}/{L}"] = {"alphabet": "".join(chr(65 + a) if a is not None else "." for a in
                                                                 [next((x for x, v in w[0].items() if v == i), None) for i in range(26)]),
                                                                 "key": {f"{kv[0]}{kv[1]}": v for kv, v in sorted(w[1].items())}}
    return tid, out


def run(ctx):
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    mod, orig = frozen()
    known = dict(ctx.KNOWN)
    p24 = sorted(known); p20 = [q for q in p24 if q in OFFICIAL]
    _G.update(mod=mod, known=known, sets=[("24", p24), ("20", p20)])
    rng = random.Random(SEED)
    # self-check 1: with no offsets the changed decide() gives 0119's verdicts on K4
    same = 0
    for L in range(1, LMAX + 1):
        for form in FORMS:
            a = mod.decide(equations(ctx.K4, known, L, "plain", p24), form, random.Random(1))[0]
            b = orig.decide(orig.equations(ctx.K4, known, L), form, random.Random(1))[0]
            assert a == b, (L, form, a, b)
            same += 1
    # self-check 2: planted texts fit their own cell
    plant_fail, n_pl = [], 0
    for model in MODELS:
        for L in range(1, LMAX + 1):
            for form in FORMS:
                for _ in range(3):
                    t = planted(L, form, model, rng, known)
                    eqs = equations(t, known, L, model, p24)
                    st, w = mod.decide(eqs, form, rng)
                    n_pl += 1
                    if st != "fit" or not mod.check_witness(eqs, form, w):
                        plant_fail.append((model, L, form, st))
    texts = [("k4", ctx.K4)]
    for i in range(N_CONTROLS):
        sh = list(ctx.K4); random.Random(SEED * 100 + i).shuffle(sh); texts.append((f"copy{i:03d}", "".join(sh)))
    res = dict(getattr(ctx, "saved", {}) or {})
    todo = [t for t in texts if t[0] not in res]
    ctx.progress(len(res), len(texts), "texts decided")
    with mp.get_context("fork").Pool(int(os.environ.get("K4_WORKERS", 8))) as pool:
        for tid, out in pool.imap_unordered(_job, todo, chunksize=1):
            res[tid] = out
            ctx.save(tid, out)
            ctx.progress(len(res), len(texts), "texts decided")
    copies = [res[f"copy{i:03d}"] for i in range(N_CONTROLS)]
    summary, cells = {}, {}
    for sname in ("24", "20"):
        for model in MODELS:
            for form in FORMS:
                tag = f"{sname}/{model}/{form}"
                k4fit = [L for L in range(1, LMAX + 1) if res["k4"][f"{tag}/{L}"] == "fit"]
                k4und = [L for L in range(1, LMAX + 1) if res["k4"][f"{tag}/{L}"] == "undecided"]
                share = {L: sum(1 for c in copies if c[f"{tag}/{L}"] == "fit") for L in range(1, LMAX + 1)}
                und = sum(1 for c in copies for L in range(1, LMAX + 1) if c[f"{tag}/{L}"] == "undecided")
                nfit = sorted(sum(1 for L in range(1, LMAX + 1) if c[f"{tag}/{L}"] == "fit") for c in copies)
                first = sorted(next((L for L in range(1, LMAX + 1) if c[f"{tag}/{L}"] == "fit"), 99) for c in copies)
                k4first = k4fit[0] if k4fit else 99
                summary[tag] = {
                    "k4_fits": k4fit, "k4_undecided": k4und, "k4_fit_count": len(k4fit),
                    "copies_fit_count_5th_median_95th": [nfit[5], nfit[50], nfit[94]],
                    "copies_with_at_least_k4_count": sum(1 for x in nfit if x >= len(k4fit)),
                    "copies_with_at_most_k4_count": sum(1 for x in nfit if x <= len(k4fit)),
                    "k4_shortest": k4first, "copies_shortest_min_median_max": [first[0], first[50], first[-1]],
                    "copies_shortest_at_or_below_k4": sum(1 for x in first if x <= k4first),
                    "copies_fitting_per_length": share, "copies_undecided_total": und,
                    "k4_fits_where_under_5_copies_fit": [L for L in k4fit if share[L] < 5],
                    "k4_dead_where_over_95_copies_fit": [L for L in range(1, LMAX + 1) if res["k4"][f"{tag}/{L}"] == "dead" and share[L] > 95],
                }
    witnesses = {k[2:]: v for k, v in res["k4"].items() if k.startswith("w:")}
    below10 = sorted(k for k in witnesses if int(k.rsplit("/", 1)[1]) < 10)
    return {
        "candidates": [],
        "bounds": {
            "item": "F16.4c", "family": "one free alphabet on both sides (26! orders), periodic key 1-26, an unknown offset per carved line",
            "models": {"offset": "slot = place mod L; k = key[slot] + offset[line]", "both": "slot = column in the carved line mod L; k = key[slot] + offset[line]"},
            "lines": "K4 places 1-4, 5-35, 36-66, 67-97", "forms": {"V": "A(c) = A(p) + k", "B": "A(c) = k - A(p)"},
            "exhaustive": "exact decision per cell by 0119's decide() (witness re-checked); undecided cells counted",
            "self_check": f"with no offsets the changed decide() equals 0119's on K4 in {same} of {same} cells; planted texts fit their own cell {n_pl - len(plant_fail)} of {n_pl}",
            "plant_failures": [list(x) for x in plant_fail[:20]],
            "summary": summary, "k4_fitting_cells_below_length_10": below10,
            "k4_witnesses_below_length_14": {k: v for k, v in witnesses.items() if int(k.rsplit("/", 1)[1]) < 14},
            "controls": f"{N_CONTROLS} shuffles of K4 with the known letters kept in place, the identical test",
            "not_covered": "a restart with no offset (F1.4, 0253); reading the fitting cells (a decider run, if any fit below 10); slips",
            "aws_cost_estimate_dollars": 0.2,
        },
        "notes": "; ".join(f"{t}: K4 fits {v['k4_fit_count']} (copies {v['copies_fit_count_5th_median_95th']}), shortest {v['k4_shortest']} (copies median {v['copies_shortest_min_median_max'][1]})"
                           for t, v in summary.items()) + f"; plants failing {len(plant_fail)} of {n_pl}; K4 cells below 10: {below10}",
    }


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    lines = ["key length 7, the key running on, an offset per carved line: the unknowns each known place touches", "", "place line slot known carved"]
    for q in sorted(ctx.KNOWN):
        lines.append(f"{q:>5} {line_of(q):>4} {(q - 1) % 7:>4} {ctx.KNOWN[q]:>5} {ctx.K4[q - 1]:>6}")
    return "\n".join(lines)
