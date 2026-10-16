"""Experiment 0147 (F1.6). See program.md for the contract."""

EXPERIMENT = {
    "slug": "one-carved-letter-wrong-through-the-free-alphabet-tests",
    "title": "F1.6: one carved letter wrong at a known place, or one letter missing or extra between the known runs, run through the exact tests for one and two unknown alphabets at every key length",
    "family": "1-keyed-periodic",
    "parent": "0123-two-free-alphabets-exact-at-every-key-length",
    "changed": (
        "F1.6, first part. 0119 and 0123 decided one and two unknown alphabets with a periodic key exactly, on the copper "
        "as carved. K2 lost a letter and K1-K3 carry slips; F1.1's added form (K1 and K2's own system) dies only because "
        "S sits under S at 33 and K under K at 74. Here every single-letter error the exact tests can see is tried: each of "
        "the 24 carved letters at the known places replaced by each of the other 25 letters (600), and one letter missing "
        "or extra between the two known runs (4, the shift read on either side; an error before EAST or after CLOCK shifts every known place together and "
        "changes no periodic check, so it is the copper as carved). For each variant: one free alphabet, added and Beaufort "
        "forms, and two free alphabets, key lengths 1-26, decided exactly. Ten scrambled coppers get the same 604 variants."
    ),
    "hypothesis_expert": (
        "C17(a)/(b) and family G (knowledge/06-hypotheses.md: 'every family should be tested once more with one letter "
        "inserted or deleted at each position'), C27(c), C1(b); Scheidt 2005 (knowledge/sources/wired-2005-zetter-"
        "questions-for-kryptos-creator.txt): 'since he's the one who had the chisel in his hands, there could be some "
        "changes'. Models: 0119's one unknown bijection on both sides, added form x(c) = x(p) + k or Beaufort x(c) = k - "
        "x(p); 0123's two bijections C(c) = P(p) + k. Deciders: 0119's (CRT mod 13 and 2, exhaustive mod-13 enumeration) "
        "and 0123's, witness re-checked; node limit 20,000 for the two-alphabet search, undecided cases counted. Statistic "
        "fixed before the run: per model and length, the number of variants that fit; cells where K4's count is above "
        "every copper's, against each copper's count against the rest. Also reported: every variant that revives the "
        "added form on K4."
    ),
    "hypothesis_eli5": (
        "The earlier messages contain slips: a dropped letter, misspellings. If one carved letter of the fourth message is "
        "wrong, a cipher already ruled out might have been ruled out unfairly. In particular K1 and K2's own method, with "
        "a scrambled alphabet, fails only because two carved letters equal the known letters above them. We change each "
        "carved letter at the 24 known places to every other letter, and add or drop one letter between the two known "
        "words, and rerun the exact tests for one and two scrambled alphabets, on the carved text and on scrambled "
        "copies."
    ),
    "prediction": (
        "Changing the carved letter at 33 or 74 revives the added form at some lengths (it removes the self-encryption "
        "that kills it), on K4 as on the coppers' corresponding variants; overall fit counts per (model, length) sit inside "
        "the coppers' range, K4 above every copper in no more cells than the null's maximum. No reading; any revived cell "
        "joins F1.5's undecided cells for the English decider."
    ),
    "method": (
        "1. Build the 604 variants of K4 (and of each of 10 coppers): substitution at each known place, and the known runs "
        "pulled together or pushed apart by one. "
        "2. For each variant, model and key length 1-26: the 24 equations, decided exactly. "
        "3. Count fitting variants per (model, length) per text; compare K4 with the coppers; list K4's added-form fits."
    ),
    "walkthrough": (
        "1. Take the carved S at place 33 and suppose Sanborn cut the wrong letter: try each of the other 25 letters there. "
        "2. With one scrambled alphabet on both sides and the key added (K1 and K2's method), write the 24 equations: place of carved letter = place of known letter + key value of its slot. "
        "3. A carved letter equal to its known letter forces key value 0 in its slot; with the S changed, place 33 no longer does. "
        "4. Decide, for every key length, whether any alphabet and key satisfy all 24 equations. "
        "5. Do the same for every other carved letter at a known place, for an added or dropped letter between the two known words, and on scrambled copies."
    ),
}

import random
import time

N = 97
LMAX = 26
N_CONTROLS = 10
P0120 = "experiments/0120-one-free-alphabet-english-climb-at-23-and-26/attack.py"
P0123 = "experiments/0123-two-free-alphabets-exact-at-every-key-length/attack.py"
MODELS = ("1V", "1B", "2")


def load(path, name):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def variants(text, known):
    """(name, list of (slot index basis i0-based, plain letter idx, cipher letter idx)) for every variant.
    Equations are given as (position, p, c) with position 0-based; the slot is position mod L."""
    kp = sorted(known)
    base = [(q - 1, ord(known[q]) - 65, ord(text[q - 1]) - 65) for q in kp]
    out = []
    for e, (pos, p, c) in enumerate(base):
        for c2 in range(26):
            if c2 != c:
                eq = list(base); eq[e] = (pos, p, c2)
                out.append((f"sub {pos + 1} {chr(65 + c)}->{chr(65 + c2)}", eq))
    for d, nm in ((-1, "one letter extra between the runs"), (1, "one letter missing between the runs")):
        # BERLINCLOCK's message places move relative to the carved text: carved letter at q + d stands over known q
        eq = []
        for q in kp:
            if q >= 64:
                eq.append((q - 1, ord(known[q]) - 65, ord(text[q - 1 + d]) - 65))
            else:
                eq.append((q - 1, ord(known[q]) - 65, ord(text[q - 1]) - 65))
        out.append((nm + " (places as typed, carved letters moved)", eq))
        eqb = []
        for q in kp:
            pos = q - 1 - d if q >= 64 else q - 1
            eqb.append((pos, ord(known[q]) - 65, ord(text[q - 1]) - 65))
        out.append((nm + " (carved letters fixed, places moved)", eqb))
    return out


def eqs_for(eq, L):
    return [(pos % L, p, c) for pos, p, c in eq]


def _work(args):
    tidx, text, known = args
    m0120, m0123 = load(P0120, "a0120"), load(P0123, "a0123")
    m0123.NODE_LIMIT = 20000
    rng = random.Random(1460 + tidx)
    fits = {m: [0] * (LMAX + 1) for m in MODELS}
    und = {m: 0 for m in MODELS}
    added = []
    vs = variants(text, known)
    for name, eq in vs:
        for L in range(1, LMAX + 1):
            e = eqs_for(eq, L)
            if not m0120.l1_ok(e):
                continue                      # one carved letter over two known, or the reverse, in one slot: all models dead
            for m in MODELS:
                if m == "2":
                    st, _ = m0123.decide(e, "V", rng, two=True)
                else:
                    st, _ = m0120.decide(e, m[1], rng)
                if st == "fit":
                    fits[m][L] += 1
                    if m == "1V" and tidx == 0:
                        added.append({"variant": name, "length": L})
                elif st == "undecided":
                    und[m] += 1
    return tidx, fits, und, added, len(vs)


def run(ctx):
    import multiprocessing as mp
    import sys
    import types
    ct, known = ctx.K4, ctx.KNOWN
    m0120 = load(P0120, "a0120")
    # the deciders on the copper as carved must reproduce 0119 and 0123
    base_eq = [(q - 1, ord(known[q]) - 65, ord(ct[q - 1]) - 65) for q in sorted(known)]
    rng0 = random.Random(146)
    assert [L for L in range(1, 27) if m0120.decide(eqs_for(base_eq, L), "V", rng0)[0] == "fit"] == []
    assert [L for L in range(1, 27) if m0120.decide(eqs_for(base_eq, L), "B", rng0)[0] == "fit"] == [23, 26]
    rng = random.Random(146)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    if getattr(sys.modules.get(__name__), "_work", None) is not _work:
        m = types.ModuleType(__name__); m.__dict__.update(globals()); sys.modules[__name__] = m
    with mp.get_context("fork").Pool(8) as pool:
        res = pool.map(_work, [(t, x, known) for t, x in enumerate(texts)], chunksize=1)
    res.sort()
    T = len(texts)
    fits = [r[1] for r in res]
    cells = [(m, L) for m in MODELS for L in range(1, LMAX + 1)]

    def above_rest(t):
        return [f"{m}:{L}" for m, L in cells if fits[t][m][L] > max(fits[u][m][L] for u in range(T) if u != t)]
    k4_above = above_rest(0)
    null_above = [len(above_rest(t)) for t in range(1, T)]
    stop = len(k4_above) > max(null_above)
    bounds = {
        "family": "one carved letter wrong at a known place (600) or one letter missing/extra between the runs (4: two readings each), through the exact one- and two-free-alphabet periodic tests",
        "models": {"1V": "one alphabet, added form (Quagmire III, K1/K2's system)", "1B": "one alphabet, Beaufort form", "2": "two alphabets (Quagmire IV)"},
        "variants_per_text": res[0][4], "key_lengths": [1, LMAX],
        "k4_fitting_variants_by_length": {m: fits[0][m][1:] for m in MODELS},
        "controls_min_by_length": {m: [min(fits[t][m][L] for t in range(1, T)) for L in range(1, LMAX + 1)] for m in MODELS},
        "controls_max_by_length": {m: [max(fits[t][m][L] for t in range(1, T)) for L in range(1, LMAX + 1)] for m in MODELS},
        "undecided": {"k4": res[0][2], "controls": [r[2] for r in res[1:]]},
        "k4_added_form_fits": res[0][3][:200], "k4_added_form_fit_count": len(res[0][3]),
        "cells_k4_above_every_copper": k4_above, "null_cells_above_rest_per_copper": null_above, "stop_queue": stop,
        "indel_note": "an error before place 22 or after 74 shifts every known place together and changes no periodic check",
        "controls": f"{N_CONTROLS} shuffled coppers (seed 146), the same 604 variants each",
        "exhaustive": "exact per (variant, model, length); undecided counted",
    }
    tot = {m: sum(fits[0][m][1:]) for m in MODELS}
    notes = (f"K4 fitting (variant, length) pairs: {tot}; added form revived on K4 in {len(res[0][3])} pairs; "
             f"K4 above every copper in {len(k4_above)} of 78 cells, null {min(null_above)}-{max(null_above)}; stop {stop}; "
             f"undecided K4 {res[0][2]}")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    lines = ["one alphabet on both sides, added form (K1 and K2's method): place(carved) = place(known) + key value of the slot",
             "", "as carved: place 33 is S under S and place 74 is K under K, so their slots need key value 0;",
             "at every key length 1-26 another known letter shares one of those slots and is not its own carved letter: dead.", "",
             "variant: the carved S at 33 replaced by R (one slip of the chisel)",
             "  place 33 no longer forces 0; the slot of 74 still does (K under K)",
             "  the 24 equations are decided again at every key length, and the same for every other letter at every known place"]
    return "\n".join(lines)
