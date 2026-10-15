"""Experiment 0078. See program.md for the contract."""

EXPERIMENT = {
    "slug": "running-key-from-sanborns-own-letters",
    "title": "Sanborn's own letters as the key: his 1989 note to CIA staff, the 1991 dedication pages, and his 2025 open letter",
    "family": "1-keyed-periodic",
    "parent": "0004-running-key-from-k1-k3",
    "changed": "Running keys have been tried from K1-K3, Carter's book and the sculpture's own texts. Never from the things Sanborn himself wrote around the sculpture: his December 1989 letter to Agency employees about the work in progress, the 1991 Cryptogram pages with Webster's dedication remarks, and his August 2025 open letter. Each is slid along the copper at every offset, both directions, on the standard, KRYPTOS and vocabulary tables.",
    "hypothesis_expert": (
        "Family 1, running key from a new source (C6(a) 'the keys were concealed', C7 'instructions in the "
        "earlier text', C27: Sanborn's own documents). Texts, letters only, OCR '|' read as I: (1) Sanborn's "
        "15 December 1989 letter to Agency employees ('Dear Agency Employees ... Sincerely, Jim Sanborn'), (2) "
        "the 1991 Cryptogram pages carrying Webster's 5 November 1990 dedication remarks and the Cryptolog "
        "story (both in sources/sanborn-1989-letter-and-webster-1990-cryptogram.txt), (3) the August 2025 "
        "open letter (sources/openletter-2025.txt). Key letter at place i: source[(o + i) mod len], every offset "
        "o, source forwards and reversed. Setups: the 24 standard/KRYPTOS conventions, plus each vocabulary "
        "word's keyword alphabet on both sides with the key read on it or on the standard alphabet, three "
        "modes. Statistic: mismatches among the 24 known letters; survivors are within 3; controls are ten "
        "shuffled coppers through the same sweep. OCR errors cost at most a few mismatches near the cribs."
    ),
    "hypothesis_eli5": (
        "A running key is a long text, such as a page of a book, written under the message one letter per "
        "place. We have tried the solved messages and Carter's book. Here we try the texts Sanborn himself "
        "wrote about the sculpture: his 1989 letter telling CIA staff what he was building, the 1991 pages "
        "with the dedication speech, and his 2025 open letter with its 'clue'. Each is slid along the copper "
        "at every starting place, forwards and backwards, and the 24 known letters say how close each fits."
    ),
    "prediction": (
        "No source, offset, direction and setup comes within three mismatches of the 24 known letters, beyond "
        "what the ten shuffled coppers reach; the best is about as close as the best on the shuffles. Zero "
        "candidates pass."
    ),
    "method": (
        "1. Extract the three texts as letters. 2. For each source, direction and offset, read the key letter "
        "under each known place. 3. For each setup, count the known places where the carved letter would not "
        "come out; keep the fewest and all within three. 4. Repeat on ten shuffled coppers."
    ),
    "walkthrough": (
        "1. Write the 1989 letter's letters, DEARAGENCYEMPLOYEESIAMWRITING..., under the copper so that its "
        "first letter sits under place 1. 2. Place 22 then has key letter M, the 22nd letter of DEARAGENCYEMPLOYEESIAM. "
        "3. On the sculpture's table with Vigenere, counted from K = 0: known E (11) plus M (18) is 29, which is 3, P; "
        "the carved letter is F, so this place misses. 4. Count how many of the 24 known places come out right. "
        "5. Slide the letter one place and repeat, for every offset, both directions and every table."
    ),
}

import random
import re
from pathlib import Path
from kryptos.alphabets import keyword_mixed
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
ROOT = Path(__file__).resolve().parent
ALPH = {"std": STD, "kry": KRY}


def clean(s):
    s = re.sub(r"(?<![A-Za-z])\|(?![A-Za-z])", "I", s)
    return "".join(c for c in s.upper() if "A" <= c <= "Z")


def sources():
    t = (ROOT / "knowledge" / "sources" / "sanborn-1989-letter-and-webster-1990-cryptogram.txt").read_text(errors="ignore")
    a = t.index("Dear Agency Employees"); b = t.index("Sincerely, Jim Sanborn") + len("Sincerely, Jim Sanborn")
    c = t.index("Remarks by William H. Webster")
    o = (ROOT / "knowledge" / "sources" / "openletter-2025.txt").read_text(errors="ignore")
    oa = o.index("Dear Kryptos fans"); ob = o.index("Jim Sanborn", o.index("All the best")) + len("Jim Sanborn")
    return {"letter 1989": clean(t[a:b]), "Cryptogram 1991 (Webster remarks, Cryptolog story)": clean(t[c:]), "open letter 2025": clean(o[oa:ob])}


def setups(vocab):
    MODES = ("vig", "beau", "varbeau")
    for pa in ALPH:
        for ca in ALPH:
            for ka in ALPH:
                for m in MODES:
                    yield f"{pa}/{ca}/{ka}/{m}", ALPH[pa], ALPH[ca], ALPH[ka], m
    seen = {STD, KRY}
    for w in vocab:
        if len(set(w)) < 3:
            continue
        A = keyword_mixed(w)
        if A in seen:
            continue
        seen.add(A)
        for kn, K in (("same", A), ("std", STD)):
            for m in MODES:
                yield f"{w}/{kn}/{m}", A, A, K, m


def key_index(p, c, pa, ca, m):
    pi, ci = pa.index(p), ca.index(c)
    return {"vig": (ci - pi) % 26, "beau": (ci + pi) % 26, "varbeau": (pi - ci) % 26}[m]


def sweep(ct, known, srcs, sets, keep):
    items = sorted(known.items())
    best, near, trials = 99, [], 0
    for label, pa, ca, ka, m in sets:
        need = [(pos - 1, ka[key_index(p, ct[pos - 1], pa, ca, m)]) for pos, p in items]
        for sname, text in srcs.items():
            for d, src in (("forwards", text), ("reversed", text[::-1])):
                L = len(src)
                for o in range(L):
                    trials += 1
                    mm = 0
                    for i, k in need:
                        if src[(o + i) % L] != k:
                            mm += 1
                            if mm > 3 and mm >= best:
                                break
                    if mm < best:
                        best = mm
                    if mm <= 3 and keep:
                        near.append({"source": sname, "direction": d, "offset": o, "setup": label, "mismatches": mm})
    return best, near, trials


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    srcs = sources()
    sets = list(setups(ctx.vocabulary))
    best, near, trials = sweep(ct, known, srcs, sets, True)
    rng = random.Random(78)
    cb, cn = [], []
    for _ in range(10):
        sh = list(ct); rng.shuffle(sh)
        b2, n2, _ = sweep("".join(sh), known, srcs, sets, True)
        cb.append(b2); cn.append(len(n2))
        if ctx.time_left() < 30:
            break
    return {
        "candidates": [],
        "bounds": {"family": "running key from Sanborn's own letters", "sources": {k: len(v) for k, v in srcs.items()},
                   "setups": len(sets), "trials": trials, "k4_fewest_mismatches": best, "k4_within_3": near[:20], "k4_within_3_count": len(near),
                   "controls_fewest": cb, "controls_within_3": cn},
        "notes": f"Sources {', '.join(f'{k} ({len(v)} letters)' for k, v in srcs.items())}; {len(sets)} setups; {trials:,} trials. "
                 f"K4: fewest mismatches {best}, {len(near)} within 3. Ten shuffled coppers: fewest {cb}, within 3 {cn}.",
    }


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    src = sources()["letter 1989"]
    ct, kn = ctx.K4, ctx.KNOWN
    lines = ["1989 letter from its first letter under place 1; sculpture's alphabet, Vigenere", "", "place  known  key  would carve  carved"]
    for pos in (22, 23, 24, 64):
        k = src[pos - 1]
        lines.append(f"{pos:>5}  {kn[pos]:>5}  {k:>3}  {KRY[(KRY.index(kn[pos]) + KRY.index(k)) % 26]:>11}  {ct[pos - 1]:>6}")
    return "\n".join(lines)
