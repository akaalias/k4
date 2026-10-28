"""Experiment 0251. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f14-plaintext-style-as-the-mask-judge-bench",
    "title": "F14.7: plaintext style as the mask: vowel-dropped, telegraphese and abbreviated English added to the judge bench; power of the quadgram scorer, MIX8m and the blind judge against the bench's 200 hard negatives",
    "family": "14-scheidt-mask-keyed-by-words",
    "parent": "0233-f13-how-many-bits-per-letter-each-english-judge-extracts",
    "changed": (
        "F14.7 (issue #93). The judge bench (reports/judge-bench.md, tools/judge_bench.py) measured clean Carter, "
        "misspellings, X stops and K1-K3's text; A6.2 (0226) added those classes to the climbs. A plaintext written to be "
        "short (Scheidt: 'you've gotta remember your process'; Sanborn's K2 'interrupted radio transmission'; 'it reads "
        "like it's disjointed', Scheidt 2015 on the plaintext) would score lower. Three new classes of 30 texts each, cut "
        "from Carter with the 24 known letters in place: vowel-dropped (every vowel removed except a word's first "
        "letter), telegraphese (articles, auxiliaries and common function words dropped, X for each full stop), "
        "abbreviated (every word of 7 or more letters cut to its first 4). Scored by the bench's quadgram measure, by "
        "MIX8m (0233) and by the blind judge, each against the bench's own 100 unigram and 100 Markov negatives (judge "
        "verdicts cached from the bench run)."
    ),
    "hypothesis_expert": (
        "C19 ('what's a period... special characters don't work', Scheidt 2015), C4(a) (a mask that is only a way of "
        "writing), A6 (the plaintext scores as English to our scorer) and A13 (the right decryption will look right). "
        "Every sampled close and every F13 statistic assumes the plaintext looks like prose. Pre-registered, as the bench: "
        "threshold T = the highest score any negative gets; a scorer 'sees' a class when at least 90% of it is above T. "
        "If neither the quadgram scorer, MIX8m nor the judge sees a class, the sampled closes are 'closed for ordinary "
        "English' only, and the class is written into A6."
    ),
    "hypothesis_eli5": (
        "Messages sent by telegraph or radio were often written short: no little words, no vowels, long words cut down. "
        "If K4's hidden message was written that way, our English detectors might not recognise it. We make test "
        "messages in those styles from a real English book and check whether each detector can tell them from "
        "English-looking nonsense."
    ),
    "prediction": (
        "The judge sees telegraphese and abbreviated text (90% or more) but not vowel-dropped text; MIX8m sees "
        "telegraphese only; the quadgram scorer sees none (it saw 10% of clean Carter on the bench)."
    ),
    "method": (
        "1. Carter's text (the bench's source), words split on spaces and punctuation; 30 windows per class from random "
        "places (seed 251), the style applied, cut to 97 letters, the 24 known letters set in place. "
        "2. Negatives: tools/judge_bench.py's build() (seed 76): 100 unigram and 100 Markov texts, verdicts cached. "
        "3. Scores: the bench's quadgram measure on the free places; MIX8m on the free places' letters; the judge (one "
        "call for all, blind). "
        "4. Power per class and scorer at T = the negatives' maximum; also clean Carter from the bench as the reference."
    ),
    "walkthrough": (
        "1. Take a sentence of Carter, say 'the remains of passage debris that encumbered the lower part of the doorway'. "
        "2. Vowel-dropped: 'th rmns o pssg dbrs tht encmbrd th lwr prt o th drwy' (a word's first letter kept). "
        "3. Telegraphese: 'remains passage debris encumbered lower part doorway X'. "
        "4. Abbreviated: 'the rema of pass debris that encu the lower part of the door' (words of 7 letters or more cut to 4). "
        "5. Score each with the detector and compare with the highest score any nonsense text reaches."
    ),
    "expected_minutes": 10,
}

import importlib.util
import json
import random
import re
import sys
import time
from pathlib import Path

import numpy as np

N = 97
ROOT = Path(__file__).resolve().parent
STD = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LAM_Q = 0.55
PER_CLASS = 30
SEED = 251
FUNCTION = set("THE A AN OF TO AND IS WAS WERE BE BEEN ARE IN THAT IT ITS THIS WITH FOR ON AT BY AS HAD HAS HAVE WHICH WOULD "
               "COULD SHOULD WILL SHALL MAY MIGHT DO DID THERE THEIR THEY THEM WE OUR I MY ME HE HIS HIM SHE HER SO BUT OR "
               "FROM THAN THEN".split())
VOWELS = set("AEIOU")
_G = {}


def frozen_path(tag):
    return next((ROOT / "experiments").glob(f"{tag}-*")) / "attack.py"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def models():
    m = load(frozen_path("0233"), "frozen0233")
    m.ROOT, m.SRC = ROOT, ROOT / "knowledge" / "sources"
    m.CARTER = m.SRC / "carter-1923-tomb-of-tutankhamen-vol1.txt"
    C = m.corpus()
    codes = np.array([STD.index(c) + 1 for c in C["train_manuals"]], dtype=np.int64)
    _G.update(m233=m, Q=m.quadgram_model(), KN8m=m.KN.from_text(codes, 8))


def mix8m(texts):
    m = _G["m233"]
    return np.log2(LAM_Q * m.per_letter_probs(_G["Q"], texts) + (1 - LAM_Q) * m.per_letter_probs(_G["KN8m"], texts)).sum(axis=1)


def sentences(raw):
    body = raw[len(raw) // 20: -len(raw) // 20].upper()
    return [s.split() for s in re.split(r"[.;:!?]+", re.sub(r"[^A-Z.;:!? ]+", " ", body)) if len(s.split()) >= 3]


def styled(sents, style, rng):
    i = rng.randrange(len(sents) - 60)
    out = ""
    for s in sents[i:]:
        words = [re.sub("[^A-Z]", "", w) for w in s]
        words = [w for w in words if w]
        if style == "vowelless":
            words = [w[0] + "".join(c for c in w[1:] if c not in VOWELS) for w in words]
            out += "".join(words)
        elif style == "telegraphese":
            out += "".join(w for w in words if w not in FUNCTION) + "X"
        elif style == "abbreviated":
            out += "".join(w[:4] if len(w) >= 7 else w for w in words)
        if len(out) >= N:
            break
    return out[:N]


def encrypt(plaintext, key):
    return plaintext


def run(ctx):
    t0 = time.time()
    bench = load(ROOT / "tools" / "judge_bench.py", "judge_bench")
    known = ctx.KNOWN
    models()
    items = [it for it in bench.build() if it["cls"] in ("unigram", "markov", "clean", "xstops")]
    sents = sentences(bench.SOURCE.read_text(errors="ignore"))
    rng = random.Random(SEED)
    for style in ("vowelless", "telegraphese", "abbreviated"):
        for _ in range(PER_CLASS):
            items.append({"cls": style, "text": bench.with_known(styled(sents, style, rng))})
    free = lambda t: "".join(c for i, c in enumerate(t, start=1) if i not in known and c != "?")
    q = [bench.quadgram(it["text"]) for it in items]
    mx = mix8m([free(it["text"]) for it in items])
    ctx.progress(0, 1, "judge")
    verdicts = ctx.judge([it["text"] for it in items])
    ctx.progress(1, 1, "judge")
    for it, a, b, v in zip(items, q, mx, verdicts):
        it["quadgram"], it["mix8m"], it["judge"] = a, float(b), v["score"]
    nones = sum(1 for it in items if it["judge"] is None)
    neg = [it for it in items if it["cls"] in ("unigram", "markov")]
    power = {}
    for key in ("quadgram", "mix8m", "judge"):
        T = max(it[key] for it in neg if it[key] is not None)
        row = {"T": T}
        for cls in ("clean", "xstops", "vowelless", "telegraphese", "abbreviated"):
            xs = [it[key] for it in items if it["cls"] == cls]
            row[cls] = round(sum(1 for x in xs if x is not None and x > T) / len(xs), 3)
        power[key] = row
    seen = {cls: [k for k in power if power[k][cls] >= 0.9] for cls in ("vowelless", "telegraphese", "abbreviated")}
    examples = {cls: next(it["text"] for it in items if it["cls"] == cls) for cls in ("vowelless", "telegraphese", "abbreviated")}
    bounds = {"item": "F14.7", "classes": {"vowelless": PER_CLASS, "telegraphese": PER_CLASS, "abbreviated": PER_CLASS},
              "negatives": {"unigram": 100, "markov": 100}, "reference": ["clean", "xstops"], "power_at_negatives_max": power,
              "seen_by": seen, "rule": "a scorer sees a class when at least 90% of it is above the highest negative",
              "judge_none": nones, "examples": examples, "compute_seconds": round(time.time() - t0)}
    notes = "; ".join(f"{cls}: quadgram {power['quadgram'][cls]}, MIX8m {power['mix8m'][cls]}, judge {power['judge'][cls]}"
                      for cls in ("vowelless", "telegraphese", "abbreviated"))
    return {"candidates": [], "bounds": bounds, "notes": notes}


def worked_example(ctx, key):
    s = [["THE", "REMAINS", "OF", "PASSAGE", "DEBRIS", "THAT", "ENCUMBERED", "THE", "LOWER", "PART", "OF", "THE", "DOORWAY"]]
    rng = random.Random(0)
    lines = ["Carter: THE REMAINS OF PASSAGE DEBRIS THAT ENCUMBERED THE LOWER PART OF THE DOORWAY", ""]
    for style in ("vowelless", "telegraphese", "abbreviated"):
        out = ""
        for words in s:
            if style == "vowelless":
                out += "".join(w[0] + "".join(c for c in w[1:] if c not in VOWELS) for w in words)
            elif style == "telegraphese":
                out += "".join(w for w in words if w not in FUNCTION) + "X"
            else:
                out += "".join(w[:4] if len(w) >= 7 else w for w in words)
        lines.append(f"  {style:<13} {out}")
    return "\n".join(lines)
