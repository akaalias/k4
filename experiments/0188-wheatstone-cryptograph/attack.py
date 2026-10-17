"""Experiment 0188 (F10.2). See program.md for the contract."""

EXPERIMENT = {
    "slug": "wheatstone-cryptograph",
    "title": "F10.2: Wheatstone's cryptograph (a 27-place plain ring against a 26-letter cipher ring, the hands moved by the distance between plaintext letters), free or word-mixed cipher ring: exact",
    "family": "10-self-changing-alphabets",
    "parent": "0187-chaocipher-keyword-left-wheels",
    "changed": (
        "F10.2. Wheatstone's cryptograph (1867): an outer ring of 27 places (blank and the 26 letters) and an inner ring of "
        "26 mixed letters, two hands geared so that one turn of the long hand moves the short hand one turn and one "
        "letter. For each plaintext letter the long hand is moved forward to it; the short hand then points at the cipher "
        "letter. With S the long hand's total steps, the cipher letter is inner[S mod 26] and S mod 27 is the plain "
        "letter's place. Inside a known run the steps are known, so the inner places a run uses are known up to one "
        "offset per run; the runs are separated by unknown letters, so the second run's offset is free relative to the "
        "first (26 cases). Tested: the inner ring free (only coincidences of places check), and the inner ring mixed from "
        "any dictionary or vocabulary word (208,651 alphabets, exact); outer ring in standard or KRYPTOS order, blank "
        "first or last, hands forward or backward."
    ),
    "hypothesis_expert": (
        "A10 (alphabets that change after every letter); Wheatstone's cryptograph (1867), an Alberti disk whose advance "
        "is set by the plaintext, a hand device a sculptor could have seen. Model as in 'changed', with the plaintext "
        "continuous (no blanks between words: the runs are carved as 13 and 11 consecutive letters). Each known letter "
        "fixes inner[(b_run + o_t) mod 26] = c_t, o_t known. Statistic: consistent (variant, offset) cells with the free "
        "ring and consistent (word, variant) cells with a mixed ring, K4 against 20 shuffled copies; plants."
    ),
    "hypothesis_eli5": (
        "Wheatstone's 1867 code machine looks like a clock: an outer ring with the alphabet, an inner ring with mixed "
        "letters, two hands geared slightly differently. To encode a letter you move the long hand forward to it, and "
        "read the letter under the short hand. Because the hands drift apart, the same letter comes out differently each "
        "time. Inside EASTNORTHEAST we know exactly how far the hand moves each time, so the known letters tell us where "
        "the code letters must sit on the inner ring."
    ),
    "prediction": "With a free inner ring the known letters check little, so consistent cells at the copies' rate; with a word-mixed ring no word fits K4 or the copies. Zero candidates.",
    "method": (
        "1. For each variant (outer order, blank first or last, direction): the long hand's steps inside each run. "
        "2. Free inner ring: for each relative offset of the second run, collect inner place -> carved letter; consistent "
        "if one-to-one. "
        "3. Mixed inner ring: for each word alphabet and run, the offsets that put every carved letter in place. "
        "4. K4 against 20 shuffled copies; planted texts as builder checks."
    ),
    "walkthrough": (
        "1. The long hand stands on E (place 5 of the outer ring) at place 22. "
        "2. To reach A it moves forward 23 places, to S then 18, to T 1, and so on through EASTNORTHEAST. "
        "3. The short hand moves the same number of places on the 26-letter inner ring. "
        "4. So the carved letters of places 22-34 sit on the inner ring at known distances from one another: two that "
        "land on the same inner place must be the same carved letter. "
        "5. With an inner ring mixed from a word, the distances must match the word's alphabet exactly."
    ),
}

import random
import time
from pathlib import Path

from kryptos.facts import KNOWN, KRYPTOS_ALPHABET as KRY
from kryptos.alphabets import keyword_mixed

N_CONTROLS = 20
A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
RUNS = [(22, "EASTNORTHEAST"), (64, "BERLINCLOCK")]
ROOT = Path(__file__).resolve().parent
if not (ROOT / "kryptos").exists():
    ROOT = Path.cwd()


def outer(order, blank):
    base = A if order == "std" else KRY
    return ("_" + base) if blank == "first" else (base + "_")


def offsets(word, ring, direction):
    """Long-hand total steps from the run's first letter; a repeated letter takes a full turn."""
    pos = {ch: i for i, ch in enumerate(ring)}
    o = [0]
    for a, b in zip(word, word[1:]):
        d = (pos[b] - pos[a]) % 27 if direction == "fwd" else (pos[a] - pos[b]) % 27
        o.append(o[-1] + (d if d else 27))
    return o


def variants():
    return [(o, b, d) for o in ("std", "kry") for b in ("first", "last") for d in ("fwd", "bwd")]


def run_inner(text, var):
    ring = outer(*var[:2])
    return [([(o % 26) for o in offsets(w, ring, var[2])], [text[s - 1 + j] for j in range(len(w))]) for s, w in RUNS]


def free_consistent(text, var):
    (o1, c1), (o2, c2) = run_inner(text, var)
    good = []
    for b in range(26):
        m, used, ok = {}, {}, True
        for o, c in list(zip(o1, c1)) + [((x + b) % 26, c) for x, c in zip(o2, c2)]:
            if m.setdefault(o, c) != c or used.setdefault(c, o) != o:
                ok = False
                break
        if ok:
            good.append(b)
    return good


def mixed_consistent(text, var, alphs, posl=None):
    """posl: per alphabet, the place of each letter (list indexed by letter number)."""
    runs = [([(o - offs[0]) % 26 for o in offs], [ord(c) - 65 for c in cs]) for offs, cs in run_inner(text, var)]
    if posl is None:
        posl = [[a.index(ch) for ch in A] for a in alphs]
    hits = []
    for a, P in zip(alphs, posl):
        ok_all = True
        for offs, cs in runs:
            b = P[cs[0]]
            for o, c in zip(offs, cs):
                if (b + o) % 26 != P[c]:
                    ok_all = False
                    break
            if not ok_all:
                break
        if ok_all:
            hits.append(a)
    return hits


def encipher(p, var, inner, s0):
    ring = outer(*var[:2])
    pos = {ch: i for i, ch in enumerate(ring)}
    S = s0
    out = []
    cur = S % 27
    for ch in p:
        d = (pos[ch] - cur) % 27 if var[2] == "fwd" else (cur - pos[ch]) % 27
        S += d if d else 27
        cur = pos[ch]
        out.append(inner[S % 26])
    return "".join(out)


def run(ctx):
    t0 = time.time()
    ct = ctx.K4
    words = [w.strip().upper() for w in (ROOT / "kryptos" / "data" / "words.txt").read_text().split()]
    words += [w.upper() for w in ctx.vocabulary if w.isalpha()]
    alphs = sorted({keyword_mixed(w) for w in words if w.isalpha() and len(w) >= 3} | {A, KRY, A[::-1]})
    posl = [[a.index(ch) for ch in A] for a in alphs]
    rng = random.Random(1880)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    V = variants()
    PLANT_P = "USEDTHEEARTHSMAGNETICEASTNORTHEASTRMATIONWASGATHEREDANDTRANSMITBERLINCLOCKUNDTOANUNKNOWNLOCATIONX"
    plants = []
    for k in range(2):
        var = V[rng.randrange(len(V))]
        inner = alphs[rng.randrange(len(alphs))]
        c = encipher(PLANT_P, var, inner, rng.randrange(702))
        plants.append({"variant": "/".join(var), "inner": inner, "free_offsets": len(free_consistent(c, var)),
                       "mixed_found": inner in mixed_consistent(c, var, [inner] + alphs[:2000])})
    free = []
    mixed = []
    k4_mixed = []
    for ti, t in enumerate(texts):
        f = sum(len(free_consistent(t, v)) for v in V)
        free.append(f)
        m = 0
        for v in V:
            h = mixed_consistent(t, v, alphs, posl)
            m += len(h)
            if ti == 0:
                k4_mixed += [{"variant": "/".join(v), "inner": a} for a in h]
        mixed.append(m)
        if ctx.time_left() < 120:
            break
    # checks the free ring leaves: coincidences of inner places within and across the runs
    checks = {}
    for v in V:
        (o1, _), (o2, _) = run_inner(ct, v)
        checks["/".join(v)] = {"run1_places": len(set(o1)), "run2_places": len(set(o2))}
    bounds = {
        "family": "Wheatstone cryptograph: 27-place outer ring (std/KRYPTOS, blank first/last), 26-letter inner ring free or word-mixed, hands forward/backward; continuous plaintext; exact",
        "variants": len(V), "word_alphabets": len(alphs),
        "free_ring_consistent_offsets": {"k4": free[0], "copies": free[1:]},
        "mixed_ring_consistent": {"k4": mixed[0], "copies": mixed[1:]},
        "k4_mixed_hits": k4_mixed[:20], "distinct_inner_places_per_run": checks, "plants": plants,
        "copies": f"{len(free) - 1} shuffled copies (seed 1880)", "seconds": round(time.time() - t0), "exhaustive": True,
    }
    notes = (f"free inner ring: consistent (variant, offset) K4 {free[0]} (copies {min(free[1:])}-{max(free[1:])}) of {len(V) * 26}; "
             f"word-mixed inner ring: K4 {mixed[0]} (copies {min(mixed[1:])}-{max(mixed[1:])}); plants {plants}")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ring = outer("std", "first")
    o = offsets("EASTNORTHEAST", ring, "fwd")
    ct = ctx.K4
    lines = ["outer ring _ABC...Z, hands forward: long-hand steps through EASTNORTHEAST and the inner place each lands on", ""]
    for j, ch in enumerate("EASTNORTHEAST"):
        lines.append(f"place {22 + j}: {ch}, total steps {o[j]:3d}, inner place b + {o[j] % 26:2d}, carved {ct[21 + j]}")
    return "\n".join(lines)
