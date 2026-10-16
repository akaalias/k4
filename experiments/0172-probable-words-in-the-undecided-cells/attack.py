"""Experiment 0172 (F12.6). See program.md for the contract."""

EXPERIMENT = {
    "slug": "probable-words-in-the-undecided-cells",
    "title": "F12.6: Stein's breakthrough, probable words: common English and K1-K3 words placed at every position in the free-alphabet cells the known letters leave undecided, decided exactly",
    "family": "12-steins-way",
    "parent": "0123-two-free-alphabets-exact-at-every-key-length",
    "changed": (
        "F12.6. Stein broke K2 by guessing THE, then KNOW, and checking each guess against the cipher. Here the guesses are "
        "systematic: 60 probable words (Stein's THE and KNOW, the commonest English words, distinctive K1-K3 words) placed "
        "at every position of K4 where they do not contradict the known letters, each placement adding its letters as "
        "known, then decided exactly for the cells F1.1 and F1.2 left consistent: one free alphabet, Beaufort form, key "
        "lengths 23 and 26 (0119's decider), and two free alphabets at 8, 13, 16, 19, 20, 23, 24, 26 (0123's). A cell's "
        "consistent placements on K4 are compared with copies of K4 that fit the same cell; F6.1 and F6.2 (with a move) "
        "are left out for cost (hundreds of thousands of fitting settings)."
    ),
    "hypothesis_expert": (
        "Stein 1999 (knowledge/sources/stein-1999-cracking-the-courtyard-crypto.txt): 'given that the first letter of Part "
        "II could very well be a T, I naturally wanted to see what would happen if H were the second letter and E the "
        "third'; 'that KNO in the 15th row was an unexpected gift'. C7(a) (K1-K3 words), C19 (X as a stop). Each placement "
        "of a w-letter word adds w equations; in a cell with free alphabets most placements are refuted, so the count of "
        "consistent placements is a measure the known letters alone could not give. Statistic fixed before the run: per "
        "cell, consistent placements with at least one added check, K4 against ten copies drawn to fit that cell; any "
        "cell where K4 is above every copy is replicated."
    ),
    "hypothesis_eli5": (
        "Stein's breakthrough was guessing likely words, THE and then KNOW, and seeing whether the cipher allowed them. "
        "For the cipher settings the 24 known letters cannot decide, we try sixty likely words at every position: each "
        "guess adds more known letters, and most guesses become impossible. If the carved text allowed many more guesses "
        "than scrambled copies do, that setting would deserve a closer look."
    ),
    "prediction": "Consistent placements on K4 inside the copies' range in every cell. Zero candidates.",
    "method": (
        "1. Words: THE, KNOW, the commonest English words, distinctive K1-K3 words (60). "
        "2. For each cell, K4 and 10 copies that fit the cell: every word at every position compatible with the known letters; add its letters; decide exactly (node limits, undecided counted). "
        "3. Count consistent placements with an added check; compare."
    ),
    "walkthrough": (
        "1. Take one scrambled alphabet with a 23-letter key, the Beaufort way: the 24 known letters fit. "
        "2. Guess that THE stands at places 1-3: three more letters are known. "
        "3. Each new letter adds an equation (carved place + message place = key value of its slot); decide again whether any alphabet and key satisfy them all. "
        "4. Try THE at every place, then the other words; count the guesses that survive. "
        "5. Do the same on scrambled copies that also fit the cell."
    ),
}

import random
import time

N = 97
N_COPIES = 10
WORKERS = 8
P0120 = "experiments/0120-one-free-alphabet-english-climb-at-23-and-26/attack.py"
P0123 = "experiments/0123-two-free-alphabets-exact-at-every-key-length/attack.py"
WORDS = ["THE", "KNOW", "AND", "THAT", "WITH", "WAS", "FOR", "THIS", "FROM", "HAVE", "WERE", "THEY", "WHICH", "THERE",
         "THEIR", "WOULD", "ABOUT", "INTO", "WHEN", "BEEN", "ONLY", "OVER", "AFTER", "WHERE", "UNDER", "BETWEEN", "NORTH",
         "SOUTH", "WEST", "DEGREES", "MINUTES", "SECONDS", "LAYER", "TWO", "SHADOW", "LIGHT", "ILLUSION", "INVISIBLE",
         "MAGNETIC", "FIELD", "LOCATION", "UNDERGROUND", "BURIED", "MESSAGE", "CHAMBER", "CANDLE", "SLOWLY", "PASSAGE",
         "DOORWAY", "WONDERFUL", "THINGS", "CAN", "YOU", "SEE", "ANYTHING", "EGYPT", "WALL", "TIME", "CLOCK", "BERLIN"]
CELLS = [("one free, Beaufort", 23), ("one free, Beaufort", 26)] + [("two free", L) for L in (8, 13, 16, 19, 20, 23, 24, 26)]


def load(path, name):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def placements(known):
    out = []
    for w in WORDS:
        for s in range(1, N - len(w) + 2):
            extra, ok, add = {}, True, 0
            for j, ch in enumerate(w):
                q = s + j
                if q in known:
                    if known[q] != ch:
                        ok = False
                        break
                else:
                    extra[q] = ch
                    add += 1
            if ok and add:
                out.append((w, s, extra))
    return out


def decide(cell, text, known, L, m0120, m0123, rng):
    eqs = [((q - 1) % L, ord(known[q]) - 65, ord(text[q - 1]) - 65) for q in sorted(known)]
    if cell.startswith("one"):
        return m0120.decide(eqs, "B", rng)[0]
    return m0123.decide(eqs, "V", rng, two=True)[0]


def _work(args):
    cell, L, t, text, known, deadline = args
    m0120, m0123 = load(P0120, "a0120"), load(P0123, "a0123")
    m0120.NODE_LIMIT = 20000; m0123.NODE_LIMIT = 20000
    rng = random.Random(1616 + t)
    fit = und = 0
    hits = []
    done = 0
    for w, s, extra in placements(known):
        if time.time() > deadline:
            break
        kn = dict(known); kn.update(extra)
        st = decide(cell, text, kn, L, m0120, m0123, rng)
        done += 1
        if st == "fit":
            fit += 1
            if t == 0 and len(hits) < 50:
                hits.append(f"{w}@{s}")
        elif st == "undecided":
            und += 1
    return cell, L, t, fit, und, done, hits


def run(ctx):
    import multiprocessing as mp
    import sys
    import types
    ct, known = ctx.K4, ctx.KNOWN
    m0120, m0123 = load(P0120, "a0120"), load(P0123, "a0123")
    rng = random.Random(1616)
    texts = {}
    for cell, L in CELLS:
        assert decide(cell, ct, known, L, m0120, m0123, rng) == "fit", (cell, L)
        cs = [ct]
        tries = 0
        while len(cs) < N_COPIES + 1 and tries < 20000:
            sh = list(ct); rng.shuffle(sh); sh = "".join(sh); tries += 1
            # copies that keep the 24 known places' carved letters fit the cell by construction
            kp = set(q - 1 for q in known)
            free = [i for i in range(N) if i not in kp]
            letters = [ct[i] for i in free]; rng.shuffle(letters)
            cp = list(ct)
            for i, ch in zip(free, letters):
                cp[i] = ch
            cs.append("".join(cp))
        texts[(cell, L)] = cs
    deadline = time.time() + ctx.time_left() - 90
    jobs = [(cell, L, t, x, known, deadline) for (cell, L), cs in texts.items() for t, x in enumerate(cs)]
    if getattr(sys.modules.get(__name__), "_work", None) is not _work:
        m = types.ModuleType(__name__); m.__dict__.update(globals()); sys.modules[__name__] = m
    t0 = time.time()
    with mp.get_context("fork").Pool(WORKERS) as pool:
        res = pool.map(_work, jobs, chunksize=1)
    summary = {}
    for (cell, L) in CELLS:
        rs = sorted([r for r in res if r[0] == cell and r[1] == L], key=lambda r: r[2])
        k4 = rs[0]
        cop = [r[3] for r in rs[1:]]
        summary[f"{cell} {L}"] = {"k4_consistent": k4[3], "coppers_consistent": cop, "k4_undecided": k4[4],
                                  "placements_done": [r[5] for r in rs], "k4_above_every_copy": k4[3] > max(cop), "k4_examples": k4[6][:20]}
    n_pl = len(placements(known))
    above = [k for k, v in summary.items() if v["k4_above_every_copy"]]
    bounds = {"family": "probable-word placements in the undecided free-alphabet cells (F1.1 Beaufort 23, 26; F1.2 two alphabets at 8 lengths), exact",
              "words": len(WORDS), "placements_per_text": n_pl, "summary": summary, "cells_k4_above_every_copy": above,
              "copies": "per cell, 10 copies keeping the carved letters at the 24 known places, other 73 shuffled (they fit the cell by construction; seed 1616)",
              "seconds": round(time.time() - t0), "exhaustive": "exact per placement; undecided counted"}
    notes = "; ".join(f"{k}: K4 {v['k4_consistent']} (copies {min(v['coppers_consistent'])}-{max(v['coppers_consistent'])})" for k, v in summary.items())
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    L = 23
    lines = [f"one scrambled alphabet, Beaufort form, key length {L}: THE guessed at places 1-3", ""]
    for q, ch in zip((1, 2, 3), "THE"):
        lines.append(f"place {q}: carved {ct[q - 1]}, guessed {ch}, slot {(q - 1) % L}: place({ct[q - 1]}) + place({ch}) = key value of slot {(q - 1) % L}")
    lines.append("with the 24 known letters, 27 equations: decided exactly; repeated for every word and place")
    return "\n".join(lines)
