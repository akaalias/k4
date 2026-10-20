"""Power test for the blind English judge (issue #76), run before the judge is used on any search.

Planted English with Sanborn-style damage against hard negatives, every text with the 24 known letters in
place (the judge masks them), scored by the judge and by the quadgram scorer as a baseline.

Pre-registered (written 2026-10-20, before the first run):
- threshold T = the highest score any negative gets (as a search's candidates must beat every copy's);
- PASS if at T the judge finds at least 90% of each of: clean, sub1, sub2, sub3, xstops, k123;
- sub5, sub8, holes, half are measured, not required: they say where the judge's power ends;
- model: Haiku 5.5 if it passes and comes within 0.10 of Sonnet 5.5 on every class; otherwise Sonnet;
- the quadgram baseline is scored the same way; if it passes as well as the judge on every class, the
  report says so (the judge then adds nothing for that kind of candidate).

    uv run python tools/judge_bench.py                      # both models, writes reports/judge-bench.md
    uv run python tools/judge_bench.py --models claude-haiku-5-5
"""
import argparse
import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kryptos import judge as J  # noqa: E402
from kryptos.facts import KNOWN, load_k1, load_k2, load_k3  # noqa: E402
from kryptos.plants import SOURCE, english_plant  # noqa: E402
from kryptos.scorer import _table, english_score  # noqa: E402

FREE = [i for i in range(1, 98) if i not in KNOWN]
ENGLISH_FREQ = "EEEEEEEEEEEETTTTTTTTTAAAAAAAAOOOOOOOIIIIIIINNNNNNNSSSSSSHHHHHHRRRRRRDDDDLLLLCCCUUUMMMWWFFGGYYPPBVKJXQZ"
REQUIRED = ["clean", "sub1", "sub2", "sub3", "xstops", "k123"]
MEASURED = ["sub5", "sub8", "holes", "half"]
NEGATIVE = ["unigram", "markov", "holes_neg"]
SEED = 76


def with_known(p):
    p = list(p)
    for q, ch in KNOWN.items():
        p[q - 1] = ch
    return "".join(p)


def damage(text, k, rng):
    t = list(text)
    for q in rng.sample(FREE, k):
        t[q - 1] = rng.choice([c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if c != t[q - 1]])
    return "".join(t)


def unigram(rng, n=97):
    return "".join(rng.choice(ENGLISH_FREQ) for _ in range(n))


_NXT = {}


def markov(rng, n=97):
    """Letter soup from English quadgram statistics: locally English-like, no words in sequence."""
    if not _NXT:
        logs, _ = _table()
        for g, lp in logs.items():
            _NXT.setdefault(g[:3], []).append((g[3], 10 ** lp))
    nxt = _NXT
    start = rng.choice(list(nxt))
    s = start
    while len(s) < n:
        opts = nxt.get(s[-3:])
        if not opts:
            s += rng.choice(ENGLISH_FREQ); continue
        r, acc = rng.random() * sum(w for _, w in opts), 0.0
        for ch, w in opts:
            acc += w
            if acc >= r:
                s += ch; break
    return s[:n]


def hole_pattern(rng):
    """Unknown key columns of a periodic key: about 30% of residue classes, period 9-20."""
    p = rng.randrange(9, 21)
    dead = set(rng.sample(range(p), max(1, round(0.3 * p))))
    return {q for q in range(1, 98) if (q - 1) % p in dead and q not in KNOWN}


def holes(text, pattern):
    return "".join("?" if i in pattern else c for i, c in enumerate(text, start=1))


def xstops_plant(rng):
    raw = SOURCE.read_text(errors="ignore")
    body = raw[len(raw) // 20: -len(raw) // 20].upper()
    body = re.sub(r"[.;:!?]+", "X", body)
    body = re.sub("[^A-Z]", "", body)
    o = rng.randrange(0, len(body) - 97)
    return with_known(body[o:o + 97])


def k123_plants():
    s = load_k1()["plaintext"] + load_k2()["plaintext_as_carved"] + load_k3()["plaintext"]
    s = re.sub("[^A-Z]", "", s)
    return [with_known(s[o:o + 97]) for o in range(0, len(s) - 97, 55)][:12]


def build():
    rng = random.Random(SEED)
    items = []
    add = lambda cls, t: items.append({"cls": cls, "text": t})  # noqa: E731
    for i in range(30):
        base = english_plant(SEED * 1000 + i)
        add("clean", base)
        for k in (1, 2, 3, 5, 8):
            add(f"sub{k}", damage(base, k, rng))
        add("xstops", xstops_plant(rng))
        pat = hole_pattern(rng)
        add("holes", holes(base, pat))
        add("holes_neg", holes(with_known(unigram(rng)), pat))
        cut = rng.randrange(35, 64)
        add("half", with_known(base[:cut] + unigram(rng, 97 - cut)))
    for t in k123_plants():
        add("k123", t)
    for _ in range(100):
        add("unigram", with_known(unigram(rng)))
        add("markov", with_known(markov(rng)))
    return items


def quadgram(text):
    free = "".join(c for i, c in enumerate(text, start=1) if i not in KNOWN and c != "?")
    return round(english_score(free) * 100)  # same ordering, integer-ish for the table


def power(items, key):
    neg = [it[key] for it in items if it["cls"] in NEGATIVE]
    T = max(neg)
    out = {"T": T, "neg_max_by_class": {c: max(it[key] for it in items if it["cls"] == c) for c in NEGATIVE}}
    for c in REQUIRED + MEASURED:
        xs = [it[key] for it in items if it["cls"] == c]
        out[c] = round(sum(x > T for x in xs) / len(xs), 3)
    out["passed"] = all(out[c] >= 0.9 for c in REQUIRED)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", default=["claude-sonnet-5-5", "claude-haiku-5-5"])
    a = ap.parse_args()
    items = build()
    for it in items:
        it["quadgram"] = quadgram(it["text"])
    results = {"quadgram": power(items, "quadgram")}
    usage = {}
    for m in a.models:
        J.MODEL = m
        before = dict(J.usage)
        scores = J.judge([it["text"] for it in items])
        usage[m] = {k: J.usage[k] - before[k] for k in J.usage}
        usage[m]["failed"] = sum(1 for s in scores if s["score"] is None)
        for it, s in zip(items, scores):
            it[m] = s["score"] if s["score"] is not None else -1  # a failed verdict counts as missed, never as found
            it[m + ":reading"] = s["reading"]
        results[m] = power(items, m)
    out = ROOT / "data" / "judge" / "bench.json"
    out.write_text(json.dumps({"items": items, "results": results, "usage": usage}, indent=1))
    cols = ["quadgram"] + a.models
    print("class      " + "  ".join(f"{c[:18]:>18}" for c in cols))
    for c in REQUIRED + MEASURED:
        print(f"{c:10} " + "  ".join(f"{results[k][c]:>18}" for k in cols))
    print("threshold  " + "  ".join(f"{results[k]['T']:>18}" for k in cols))
    print("PASS       " + "  ".join(f"{str(results[k]['passed']):>18}" for k in cols))
    print("usage", usage)


if __name__ == "__main__":
    main()
