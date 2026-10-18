"""A13's cheap check: structure other than fluent English in a 97-letter reading.

Assumption A13 (knowledge/12-assumptions.md): if the message was masked before it was
enciphered, the right decryption is masked English, so its English score sits with the noise
and the reading was thrown away. This battery looks for structure a mask would leave. Every
test returns one number, oriented so that higher means more structure. A reading may hold "."
for a letter the setting does not fix; each test then uses only the fixed letters (a quadgram
counts only if all four of its letters are fixed).

The tests, and why each is here:

  eng_base     English score of the reading as it stands (mean log10 quadgram probability,
               the table kryptos/scorer.py uses). The number that got these readings thrown away.
  freq_sorted  English letter frequencies in any order: the mean log-likelihood of the
               reading's letter counts under English frequencies (counted from Carter 1923,
               the K3 source) when the labels are free, i.e. its most common letter is matched
               with E, the next with T, and so on. A transposition or a one-for-one letter swap
               keeps this profile. Source: Scheidt, NPR 2005, on "the number of E's vs. the
               number of Z's", which "in part four he deliberately masked".
  ioc          Index of coincidence, the chance two letters drawn from the reading match
               (English about 0.066, random letters 0.038). Same source.
  sep_words    X or Q as a word space: split on the letter, then the mean log ratio of English
               word-length odds (Carter 1923) to the odds random placement gives. Needs at
               least five separators, else -inf. Source: K2 uses X as a full stop
               (data/k2.json); K3's carved ending uses Q for a question mark; Scheidt 2015,
               "What's a period... special characters don't work".
  sep_regular  X or Q at regular spacing: minus the coefficient of variation of the gaps
               between separators (at least five, none side by side, else -inf). Same source.
  eng_reverse  English score of the reading backwards. Source: reversal masks, F2 (0023).
  eng_keep_nth Best English over every nth letter, n = 2-4, every offset (the message in every
               nth place). n = 5-12 leaves 8-19 letters, too few for a quadgram score: with
               them in, the test found 3 of 20 planted texts; with n = 2-4 only, see power.json.
  eng_drop_nth Best English after dropping every nth letter, n = 2-12, every offset (nulls
               at a fixed spacing). Source: A13's own list; F2.2 nulls by a rule.
  eng_step     Best English over the 95 readings that take every kth letter around the
               97-letter ring, k = 2-96 (K3's rule is a step of this kind).
  eng_affine_std  Best English over all 312 affine maps x -> a*x + b of the standard alphabet
               (Atbash and Caesar shifts are among them). Source: A13; F2 (0074).
  eng_affine_kry  The same 312 maps on the KRYPTOS alphabet order, the tableau's own.
  eng_columns  Best English over reading in columns at widths 2-48: rows written, columns read
               left to right top down, and the inverse of that move.
  repeats      Repeated trigrams: occurrences beyond the first of every trigram seen twice or
               more. A one-for-one letter swap keeps repeats. Source: Scheidt 2015, "some
               substitution transposition... you're carrying the weight of the language".
  base_pairs   Letters read in pairs, as a code in another number base would write them:
               minus the share of distinct pairs among non-overlapping pairs (best of the
               two phases). Few distinct pairs means a pair code. Source: Scheidt 2015 and
               2020 on changing "the language base" ("base 16", "base 60").

Run on one reading:

    uv run --with numpy python tools/a13_structure.py READING

numpy is not a project dependency; `--with numpy` brings it in for this run only.
"""
import math
import re
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kryptos.facts import KRYPTOS_ALPHABET as KRY, STANDARD_ALPHABET as STD  # noqa: E402
from kryptos.scorer import _table  # noqa: E402

N = 97
CARTER = ROOT / "knowledge" / "sources" / "carter-1923-tomb-of-tutankhamen-vol1.txt"
TESTS = ["eng_base", "freq_sorted", "ioc", "sep_words", "sep_regular", "eng_reverse", "eng_keep_nth",
         "eng_drop_nth", "eng_step", "eng_affine_std", "eng_affine_kry", "eng_columns", "repeats", "base_pairs"]
UNKNOWN = 26  # letter code for "."


@lru_cache(maxsize=1)
def quad():
    logs, floor = _table()
    t = np.full(26 ** 4, floor, dtype=np.float64)
    for q, v in logs.items():
        if len(q) == 4 and q.isalpha() and q.isupper():
            a, b, c, d = (ord(x) - 65 for x in q)
            t[((a * 26 + b) * 26 + c) * 26 + d] = v
    return t


@lru_cache(maxsize=1)
def carter_stats():
    """English letter frequencies (sorted, descending) and word-length odds, from Carter 1923."""
    raw = CARTER.read_text(errors="ignore").upper()
    letters = re.sub("[^A-Z]", "", raw)
    cnt = np.bincount(np.frombuffer(letters.encode(), dtype=np.uint8) - 65, minlength=26).astype(float)
    freq_sorted = np.sort(cnt / cnt.sum())[::-1]
    words = [w for w in re.split("[^A-Z]+", raw) if w]
    lens = np.bincount([min(len(w), 20) for w in words], minlength=21).astype(float)
    p_len = lens / lens.sum()
    return freq_sorted, p_len


def _pad(rows):
    """List of index lists (each <= 97 long) -> (M, 97) array; 97 stands for 'nothing here'."""
    out = np.full((len(rows), N), N, dtype=np.int64)
    for r, ix in enumerate(rows):
        out[r, :len(ix)] = ix
    return out


@lru_cache(maxsize=1)
def families():
    """Index arrays for every positional undoing, and letter maps for the affine families."""
    fam = {}
    fam["eng_reverse"] = _pad([list(range(N - 1, -1, -1))])
    fam["eng_keep_nth"] = _pad([list(range(o, N, n)) for n in range(2, 5) for o in range(n)])
    fam["eng_drop_nth"] = _pad([[i for i in range(N) if i % n != o] for n in range(2, 13) for o in range(n)])
    fam["eng_step"] = _pad([[(i * k) % N for i in range(N)] for k in range(2, N)])
    cols = []
    for w in range(2, 49):
        fwd = [r * w + c for c in range(w) for r in range((N + w - 1) // w) if r * w + c < N]
        inv = [0] * N
        for j, i in enumerate(fwd):
            inv[i] = j
        cols += [fwd, inv]
    fam["eng_columns"] = _pad(cols)
    maps = {}
    for name, alpha in (("eng_affine_std", STD), ("eng_affine_kry", KRY)):
        pos = [alpha.index(ch) for ch in STD]          # standard letter -> place in this alphabet
        m = np.full((312, 27), UNKNOWN, dtype=np.int64)
        r = 0
        for a in (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25):
            for b in range(26):
                for x in range(26):
                    m[r, x] = STD.index(alpha[(a * pos[x] + b) % 26])
                r += 1
        maps[name] = m
    return fam, maps


def qscores(arr):
    """Mean log10 quadgram score per row of an (M, L) array of letter codes; codes >= 26 are
    unknown and any quadgram touching one is skipped. Rows with no quadgram score -inf."""
    t = quad()
    a, b, c, d = arr[:, :-3], arr[:, 1:-2], arr[:, 2:-1], arr[:, 3:]
    ok = (a < 26) & (b < 26) & (c < 26) & (d < 26)
    idx = np.where(ok, ((a * 26 + b) * 26 + c) * 26 + d, 0)
    s = np.where(ok, t[idx], 0.0).sum(axis=1)
    n = ok.sum(axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(n > 0, s / np.maximum(n, 1), -np.inf)


def codes(reading):
    return np.array([UNKNOWN if ch == "." else ord(ch) - 65 for ch in reading], dtype=np.int64)


def _sep_stats(x, p_len):
    best_w, best_r = -math.inf, -math.inf
    known = int((x < 26).sum())
    for s in (23, 16):  # X, Q
        where = np.flatnonzero(x == s)
        if len(where) < 5:
            continue
        segs = np.diff(np.concatenate(([-1], where, [N]))) - 1
        p = len(where) / known
        llr = []
        for L in segs:
            pe = p_len[min(L, 20)] if L > 0 else 1e-4
            pg = (1 - p) ** L * p
            llr.append(math.log(max(pe, 1e-4) / pg))
        best_w = max(best_w, float(np.mean(llr)))
        gaps = np.diff(where)
        if gaps.min() >= 2:  # two separators side by side mark no word: a run like QQQQQ is not spacing
            best_r = max(best_r, -float(gaps.std() / gaps.mean()))
    return best_w, best_r


def battery(reading):
    """All tests on one reading (97 letters, '.' for unknown). Returns {test: value}."""
    assert len(reading) == N
    fam, maps = families()
    freq_eng, p_len = carter_stats()
    x = codes(reading)
    xe = np.append(x, UNKNOWN)
    out = {}
    out["eng_base"] = float(qscores(x[None, :])[0])
    k = x[x < 26]
    cnt = np.bincount(k, minlength=26).astype(float)
    nk = cnt.sum()
    out["freq_sorted"] = float((np.sort(cnt)[::-1] * np.log(np.maximum(freq_eng, 1e-4))).sum() / nk)
    out["ioc"] = float((cnt * (cnt - 1)).sum() / (nk * (nk - 1)))
    out["sep_words"], out["sep_regular"] = _sep_stats(x, p_len)
    for name, ix in fam.items():
        out[name] = float(qscores(xe[ix]).max())
    for name, m in maps.items():
        out[name] = float(qscores(m[:, x]).max())
    tri = {}
    for i in range(N - 2):
        if x[i] < 26 and x[i + 1] < 26 and x[i + 2] < 26:
            key = (x[i], x[i + 1], x[i + 2])
            tri[key] = tri.get(key, 0) + 1
    out["repeats"] = float(sum(v - 1 for v in tri.values() if v > 1))
    shares = []
    for ph in (0, 1):
        prs = [(x[i], x[i + 1]) for i in range(ph, N - 1, 2) if x[i] < 26 and x[i + 1] < 26]
        if prs:
            shares.append(len(set(prs)) / len(prs))
    out["base_pairs"] = -min(shares) if shares else -math.inf
    return out


if __name__ == "__main__":
    r = sys.argv[1] if len(sys.argv) > 1 else None
    if not r:
        sys.exit(__doc__)
    for t, v in battery(r.upper()).items():
        print(f"{t:15s} {v:9.4f}")
