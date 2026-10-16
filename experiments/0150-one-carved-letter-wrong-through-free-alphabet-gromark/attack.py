"""Experiment 0150 (F1.6, Gromark part). See program.md for the contract."""

EXPERIMENT = {
    "slug": "one-carved-letter-wrong-through-free-alphabet-gromark",
    "title": "F1.6, second part: one carved letter wrong at a known place, or one letter missing or extra, through the exact free-alphabet Gromark verdicts (base 10 two- and three-term, other bases)",
    "family": "1-keyed-periodic",
    "parent": "0147-one-carved-letter-wrong-through-the-free-alphabet-tests",
    "changed": (
        "F1.6, Gromark verdicts. 0069, 0076 and 0107 showed no primer of any two- or three-term Gromark rule gives a "
        "one-to-one alphabet consistent with the 24 known letters, in base 10 and bases 2-9, 11-16, 26. Here every "
        "single-letter error those tests can see: the carved letter at each known place changed to each other letter "
        "(600), and one letter missing or extra before EAST (every known place moves by one) or between the runs "
        "(BERLINCLOCK moves by one): 604 variants of K4. The Gromark key depends on absolute position, so the shifts "
        "matter here, unlike for periodic keys. K4's variants first; scrambled copies only if a variant fits."
    ),
    "hypothesis_expert": (
        "Family G and C17 (a carving slip), C22(a) (the raised YAR as a Gromark primer), family E (Bean's Gromark case, "
        "knowledge/sources/bean-2021-cryptodiagnosis-of-k4.txt). Models and deciders unchanged from 0069 (base 10, two-term "
        "rules with lags up to 6, every primer, four forms), 0076 (bases 2-9 and 11-16 with lags up to 5, base 26 with lags "
        "up to 4) and 0107 (three-term rules, base 10, lags up to 6): equal-letter pairs fix exact digit differences, then a "
        "full one-to-one check. Exact. If no variant of K4 fits, the result is exact and needs no controls; any fit is "
        "compared with the same variants of ten scrambled copies in a follow-up."
    ),
    "hypothesis_eli5": (
        "Gromark is a cipher whose key is a stream of digits grown from a few starting digits, used with a scrambled "
        "alphabet; earlier experiments showed no starting digits and no alphabet fit the 24 known letters. If one carved "
        "letter is wrong, or one is missing or extra, that verdict might be unfair. We change each carved letter at the "
        "known places to every other letter, shift the known words by one place, and rerun the exact Gromark tests."
    ),
    "prediction": "No variant fits under any rule, base or form: Gromark stays dead with a single carving error. Zero candidates.",
    "method": (
        "1. Load 0069, 0076 and 0107's deciders unchanged. "
        "2. For each rule and base: the digit stream at the known places for the copper's positions and for the four shifts. "
        "3. For each of 604 variants: the equal-letter pairs, then every primer, then the one-to-one check. "
        "4. List any variant that fits."
    ),
    "walkthrough": (
        "1. Take Rogers' rule (each digit the sum of the digits 5 and 4 places back, mod 10) and a primer. "
        "2. Suppose the carved Q at place 27 should have been another letter, say R. "
        "3. Places 26 and 27 no longer carve the same letter, so their digit difference is no longer forced; other equal pairs still are. "
        "4. Test every primer against the remaining pairs, then check that the slots and letters pair one to one. "
        "5. Repeat for every changed letter, every shift of the known words, every rule, base and form."
    ),
}

import random
import time

N = 97
P = {"0069": "experiments/0069-gromark-with-a-free-alphabet/attack.py",
     "0076": "experiments/0076-gromark-free-alphabet-other-bases/attack.py",
     "0107": "experiments/0107-three-term-gromark-with-a-free-alphabet/attack.py"}


def load(name):
    import importlib.util
    spec = importlib.util.spec_from_file_location("m" + name, P[name])
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def variants(ct, known):
    """(name, text, items) with items = [(pos, letter)]; positions 1-based on the variant text."""
    from kryptos.facts import STANDARD_ALPHABET as STD
    items = sorted(known.items())
    out = [("as carved", ct, items)]
    for pos, _ in items:
        for c in STD:
            if c != ct[pos - 1]:
                t = ct[:pos - 1] + c + ct[pos:]
                out.append((f"sub {pos} {ct[pos - 1]}->{c}", t, items))
    # shifts: every known place moves by d (a letter extra or missing before EAST), or only BERLINCLOCK (between runs)
    for d in (-1, 1):
        t = (ct[1:] + "A") if d == -1 else ("A" + ct[:-1])
        out.append((f"all known places' carved letters moved {d:+d}", t, items))
        t2 = list(ct)
        for pos, _ in items:
            if pos >= 64:
                t2[pos - 1] = ct[pos - 1 - d]
        out.append((f"BERLINCLOCK's carved letters moved {d:+d}", "".join(t2), items))
    return out


def settings():
    m69, m76, m107 = load("0069"), load("0076"), load("0107")
    out = [("0069", (a, b)) for a, b in m69.RULES] + [("0076", t) for t in m76.plan()] + [("0107", r) for r in m107.RULES]
    return out


def _work(args):
    name, setting, var = args
    m = load(name)
    items0 = var[0][2]
    crib_idx = [pos - 1 for pos, _ in items0]
    k = len(crib_idx)
    if name == "0069":
        a, b = setting; digs = m.crib_digits(a, b, crib_idx); count = 10 ** b
        f = lambda t, it: len(m.test_copper(t, it, digs, k, count))
    elif name == "0107":
        a, b, c = setting; digs = m.crib_digits(a, b, c, crib_idx); count = 10 ** c
        f = lambda t, it: len(m.test_copper(t, it, digs, k, count))
    else:
        B, a, b = setting; digs = m.crib_digits(B, a, b, crib_idx); count = B ** b
        f = lambda t, it: m.test(t, it, digs, k, count, B)
    hits = []
    for vname, t, it in var:
        h = f(t, it)
        if h:
            hits.append((vname, h))
    return name, setting, hits


def run(ctx):
    import multiprocessing as mp
    import sys
    import types
    ct, known = ctx.K4, ctx.KNOWN
    var = variants(ct, known)
    jobs = [(n, s, var) for n, s in settings()]
    if getattr(sys.modules.get(__name__), "_work", None) is not _work:
        m = types.ModuleType(__name__); m.__dict__.update(globals()); sys.modules[__name__] = m
    t0 = time.time()
    with mp.get_context("fork").Pool(8) as pool:
        res = pool.map(_work, jobs, chunksize=1)
    hits = [{"source": n, "setting": list(s), "variants": h} for n, s, h in res if h]
    by_src = {}
    for n, s, h in res:
        by_src.setdefault(n, {"settings": 0, "settings_with_a_fit": 0})
        by_src[n]["settings"] += 1
        by_src[n]["settings_with_a_fit"] += bool(h)
    bounds = {"family": "free-alphabet Gromark (0069, 0076, 0107) on 604 one-letter variants of K4",
              "variants": len(var), "settings": by_src, "fits": hits[:50], "n_settings_with_fit": len(hits),
              "seconds": round(time.time() - t0), "exhaustive": True,
              "controls": "none needed if nothing fits (exact); any fit is compared with the same variants of 10 scrambled copies in a follow-up"}
    notes = f"{len(var)} variants x {len(jobs)} rule/base settings: settings with any fitting variant {len(hits)}"
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    return "\n".join(["the carved letters at the known places and the changes tried:", ""] +
                     [f"place {q}: carved {ct[q - 1]} under known {known[q]}; tried the other 25 letters" for q in (22, 26, 27, 33, 74)] +
                     ["", "plus every known place's carved letter moved one place left or right (a letter extra or missing before EAST),",
                      "and BERLINCLOCK's alone moved (a letter extra or missing between the two known words)"])
