"""Experiment 0233. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f13-how-many-bits-per-letter-each-english-judge-extracts",
    "title": "F13.3: bits per letter each English judge extracts from 97 letters: the quadgram table, Kneser-Ney n-grams of order 5-8 alone and mixed with it, a word model, and the blind judge on a ladder of English-like soups",
    "family": "13-ciphertext-only",
    "parent": "0136-key-bits-against-english-redundancy",
    "changed": (
        "F13.3 (issue #85). 0136 measured the quadgram scorer's evidence as log2 26 minus its cross-entropy on held-out "
        "English: 1.785 bits per letter, 173 bits in 97 letters, which sets F13.1's map (reports/f13-solvability-map.md). "
        "Here the same measurement for stronger models: interpolated Kneser-Ney letter n-grams of order 5-8 trained on "
        "local public-domain English (Carter's first 70%, the Army and Friedman manuals, the NSA glossaries, Lewis on "
        "German agent systems, line-filtered to dictionary text), the same mixed linearly with the quadgram table (weight "
        "set on Carter 70-80%), and a word model (words from the same corpus and the dictionary, single letters as "
        "fallback, summed over segmentations). Each scored on 97-letter windows of held-out English: Carter's last 20% "
        "clean, with X stops, with three letters changed, and K1-K3's plaintexts. The judge returns no probability, so "
        "every scorer, the judge too, is also put on a ladder: can it put held-out English above every one of 40 soups "
        "made from 4-gram and 6-gram statistics and of 40 word salads (real words in random order)? No known letter is read. "
        "Changed after a dry run (no judge): the n-grams trained on Carter's first 70% gained 0.6 bits per letter on "
        "Carter's last 20%, partly the book's own words, and K3 is a Carter paraphrase; so an out-of-domain arm (orders 6 "
        "and 8 on the manuals only, no Carter) was added, K1+K2 are scored apart from K3, the rule for 'stronger' moved "
        "to that arm, and every model's first letters are scored by raw frequencies (Kneser-Ney's continuation counts had "
        "scored them near uniform)."
    ),
    "hypothesis_expert": (
        "Shannon (1951) puts English at 0.6-1.3 bits per letter given long context; n-gram models reach about 2.3-2.5 "
        "with large corpora at order 5-6; the harness's quadgram table gives 2.92 (0136). Each bit per letter is 97 bits "
        "of evidence over a ciphertext-only reading, which moves F13.1's cells: F1.1 at key length 26 (202 bits), "
        "Chaocipher (177), F1.2 at 13 (225), plaintext autokey primers past 36 (F1, F1.7) all sit between the quadgram "
        "and Shannon bounds. The measurement is 0136's (cross-entropy on held-out English windows scored with no history "
        "before the window, as a search's reading is scored), extended to Sanborn-style text (judge bench classes "
        "xstops, sub3, k123: C19, C17, A6) because his plaintext is not Carter. The judge (kryptos/judge.py; "
        "reports/judge-bench.md) is not a probability model, so its evidence is bounded from below by the ladder: a "
        "scorer that separates English from soups matching English to order k extracts more than an order-k model. "
        "Pre-registered: a model is 'stronger' when its cross-entropy on held-out clean Carter is lower than the "
        "quadgram table's by at least 0.10 bits per letter, judged on the out-of-domain arm (trained without Carter); the "
        "Carter-trained models are reported as the in-domain ceiling, the case of a message in Carter's register; a scorer 'passes a rung' when at least 90% of clean and of "
        "X-stop windows score above every negative of that rung (the bench's rule)."
    ),
    "hypothesis_eli5": (
        "English is predictable: after THE, an E or an R is likelier than a Q. How predictable, in bits per letter, says "
        "how much a 97-letter reading can prove on its own, with no known letter. Our scorer counts four-letter pieces; "
        "here we measure better scorers that look at longer stretches or at whole words, on English they never saw, "
        "including text written the way Sanborn writes. The language-model judge gives no such number, so we test every "
        "scorer, the judge included, on a ladder: can it tell real English from fake text that copies English's four- or "
        "six-letter pieces, or from real words in a random order?"
    ),
    "prediction": (
        "Written after the dry run, for the out-of-domain arm: Kneser-Ney on the manuals alone is no better than the "
        "quadgram table on Carter; mixed with it, it gains 0.1-0.3 bits per letter (evidence about 1.9-2.05 bits per "
        "letter, 185-200 bits in 97): stronger by the rule. The in-domain mix reaches about 2.3 bits per letter. The word "
        "model alone is weaker than the table on 97-letter windows (cut words at both ends). Sanborn-style text costs "
        "0.1-0.2 bits per letter on every model. Ladder: the quadgram scorer fails the 4-gram soup rung (as on the bench), "
        "the mixed n-gram passes it but fails the 6-gram soup and the word salad; the judge passes the 4-gram and "
        "6-gram rungs and fails the word salad. So the best measured model moves F1.1 at 26 and Chaocipher into reach, "
        "not F1.2 at 13. Zero candidates."
    ),
    "method": (
        "1. Corpus: Carter (first 70% train, 70-80% validation, last 20% test), and the Army/Friedman/NSA/Lewis texts, "
        "lines kept only when 70% of their words are in the dictionary (cipher groups dropped). "
        "2. Models: the quadgram table as an interpolated Kneser-Ney 4-gram over its own counts (Q); interpolated "
        "Kneser-Ney orders 5-8 on the corpus (KN5-KN8); Q mixed with each, weight on the validation windows (MIXn); a "
        "word model (W). "
        "3. Cross-entropy on 97-letter windows with no prior history: test clean, X stops (full stops as X), three "
        "letters changed, K1-K3 plaintexts (overlapping windows); bits per letter = log2 26 - H; median and least "
        "predictable tenth of windows. "
        "4. Ladder: 30 clean and 30 X-stop test windows against 40 soups sampled from Q (order 4), 40 from KN6 (order 6) "
        "and 40 word salads; each scorer (Q, the best MIX, W, the judge) by the bench's rule. "
        "5. The judge is called once, from the main process, on 180 texts (cap 3,000)."
    ),
    "walkthrough": (
        "1. Count how often each run of letters is followed by each next letter in a large amount of English. "
        "2. Read a fresh 97-letter window one letter at a time and write down the chance the counts gave the letter that "
        "came. "
        "3. Average minus log2 of those chances: that is the cross-entropy; 4.70 (log2 26) minus it is the evidence per "
        "letter. "
        "4. Do the same with longer runs and with whole words, on clean book English and on text with X stops and "
        "misspellings. "
        "5. Make fake texts that copy English's short pieces, and real words in random order, and check whether each "
        "scorer still puts real English above all of them."
    ),
    "expected_minutes": 30,
}

import json
import math
import random
import re
import time
from pathlib import Path

import numpy as np

N = 97
ROOT = Path(__file__).resolve().parent
STD = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SRC = ROOT / "knowledge" / "sources"
CARTER = SRC / "carter-1923-tomb-of-tutankhamen-vol1.txt"
MANUALS = ["army-*.txt", "friedman-*.txt", "nsa-195*-basic-cryptologic-glossary*.txt", "lewis-*.txt"]
ORDERS = (5, 6, 7, 8)
OOD_ORDERS = (6, 8)            # trained without Carter: the out-of-domain arm
SEED = 233
N_LADDER_POS, N_LADDER_NEG = 30, 40
LOG2_26 = math.log2(26)


# ---- corpus ---------------------------------------------------------------------------
def dictionary():
    return set((ROOT / "kryptos" / "data" / "words.txt").read_text().split())


def filtered_lines(text, words):
    out = []
    for line in text.splitlines():
        ws = re.findall(r"[A-Za-z]+", line)
        ws2 = [w.upper() for w in ws if len(w) >= 2]
        if len(ws) >= 4 and ws2 and sum(1 for w in ws2 if w in words) >= 0.7 * len(ws2):
            out.append(line)
    return out


def corpus():
    """-> train letters, train words (for W), validation and test texts (Carter), K1-K3 plaintexts."""
    words = dictionary()
    raw = CARTER.read_text(errors="ignore")
    body = raw[len(raw) // 20: -len(raw) // 20]
    a, b = int(len(body) * 0.7), int(len(body) * 0.8)
    manual_text = []
    for pat in MANUALS:
        for f in sorted(SRC.glob(pat)):
            manual_text += filtered_lines(f.read_text(errors="ignore"), words)
    train_raw = body[:a] + "\n" + "\n".join(manual_text)

    def letters(t):
        return re.sub("[^A-Z]", "", t.upper())
    k = [json.loads((ROOT / "data" / f"{n}.json").read_text()) for n in ("k1", "k2", "k3")]
    k123 = letters(k[0]["plaintext"]) + letters(k[1]["plaintext_as_carved"]) + letters(k[2]["plaintext"])
    k12 = letters(k[0]["plaintext"]) + letters(k[1]["plaintext_as_carved"])
    return {"train_manuals": letters("\n".join(manual_text)), "k12": k12, "train": letters(train_raw), "train_words": re.findall(r"[A-Z]+", train_raw.upper()),
            "valid": letters(body[a:b]), "test": letters(body[b:]), "test_xs": letters(body[b:].replace(".", "X")),
            "k123": k123, "manual_lines": len(manual_text), "dictionary": words}


def windows(t, step=N):
    return [t[i:i + N] for i in range(0, len(t) - N + 1, step)]


def sub3(ws, rng):
    out = []
    for w in ws:
        p = list(w)
        for q in rng.sample(range(N), 3):
            p[q] = rng.choice([c for c in STD if c != p[q]])
        out.append("".join(p))
    return out


# ---- interpolated Kneser-Ney over letter n-grams (numpy, ids in base 27, letters 1-26) ----
def ids_of(codes, k):
    """ids of every k-gram in codes (1-26), as int64 in base 27."""
    n = len(codes) - k + 1
    v = np.zeros(n, dtype=np.int64)
    for j in range(k):
        v = v * 27 + codes[j:j + n]
    return v


class KN:
    """Interpolated Kneser-Ney, order n. Top order on raw counts, lower orders on continuation counts,
    discount D_k = n1 / (n1 + 2 n2) per order, interpolated down to the uniform distribution."""

    def __init__(self, top_ids, top_counts, n):
        self.n = n
        self.tab = {}          # k -> (sorted ids, counts)
        ids, cnt = top_ids, top_counts.astype(float)
        for k in range(n, 0, -1):
            o = np.argsort(ids)
            ids, cnt = ids[o], cnt[o]
            self.tab[k] = (ids, cnt)
            if k > 1:
                u, c = np.unique(ids % (27 ** (k - 1)), return_counts=True)   # continuation counts N1+(. w)
                ids, cnt = u, c.astype(float)
        self.D, self.ctx = {}, {}
        for k in range(1, n + 1):
            ids, cnt = self.tab[k]
            n1, n2 = float((cnt == 1).sum()), float((cnt == 2).sum())
            self.D[k] = n1 / (n1 + 2 * n2) if n1 + n2 > 0 else 0.5
            u, start = np.unique(ids // 27, return_index=True)
            tot = np.add.reduceat(cnt, start)
            types = np.diff(np.append(start, len(ids))).astype(float)
            self.ctx[k] = (u, tot, types)

    def at_order(self, k):
        """The model to use when only k-1 letters of history exist: raw counts at order k (marginalized from the
        top order's counts), so a window's first letters are scored by plain frequencies, not continuation counts."""
        if k >= self.n:
            return self
        if not hasattr(self, "_low"):
            self._low = {}
        if k not in self._low:
            ids, cnt = self.raw if hasattr(self, "raw") else self.tab[self.n]
            for _ in range(self.n - k):
                u, start = np.unique(ids // 27, return_index=True)
                o = np.argsort(ids // 27, kind="stable")
                ids, cnt = u, np.add.reduceat(cnt[o], np.searchsorted((ids // 27)[o], u))
            m = KN(ids, cnt, k)
            self._low[k] = m
        return self._low[k]

    @classmethod
    def from_text(cls, codes, n):
        u, c = np.unique(ids_of(codes, n), return_counts=True)
        return cls(u, c, n)

    def step(self, hid_by_k, nxt, p):
        """One letter: interpolate from order 1 up; hid_by_k[k] are history ids (k-1 letters), nxt the letter codes."""
        for k in sorted(hid_by_k):
            hid = hid_by_k[k]
            u, tot, types = self.ctx[k]
            jj = np.minimum(np.searchsorted(u, hid), len(u) - 1)
            seen = u[jj] == hid
            keys = hid * 27 + nxt
            ids, cnt = self.tab[k]
            pos = np.minimum(np.searchsorted(ids, keys), len(ids) - 1)
            c = np.where(ids[pos] == keys, cnt[pos], 0.0)
            D = self.D[k]
            t_ = np.where(seen, tot[jj], 1.0)
            p = np.where(seen, np.maximum(c - D, 0) / t_ + D * types[jj] / t_ * p, p)
        return p

    def sample(self, rng, n=N):
        out = []
        for i in range(n):
            nxt = np.arange(1, 27)
            mm = self.at_order(min(self.n, i + 1))
            hk = {}
            for k in range(1, mm.n + 1):
                h = 0
                for c in out[len(out) - (k - 1):] if k > 1 else []:
                    h = h * 27 + c
                hk[k] = np.full(26, h, dtype=np.int64)
            p = mm.step(hk, nxt, np.full(26, 1 / 26))
            out.append(int(rng.choice(nxt, p=p / p.sum())))
        return "".join(STD[c - 1] for c in out)


def per_letter_probs(model, texts):
    """P of each letter given the letters before it in its own window (no history before the window)."""
    X = np.array([[STD.index(ch) + 1 for ch in t] for t in texts], dtype=np.int64)
    m, L = X.shape
    P = np.zeros((m, L))
    for i in range(L):
        mm = model.at_order(min(model.n, i + 1))
        hk = {}
        for k in range(1, mm.n + 1):
            hid = np.zeros(m, dtype=np.int64)
            for j in range(i - k + 1, i):
                hid = hid * 27 + X[:, j]
            hk[k] = hid
        P[:, i] = mm.step(hk, X[:, i], np.full(m, 1 / 26))
    return P


def quadgram_model():
    ids, cnt = [], []
    for ln in (ROOT / "kryptos" / "data" / "english_quadgrams.txt").read_text().split("\n"):
        if not ln.strip():
            continue
        g, v = ln.split()
        x = 0
        for ch in g:
            x = x * 27 + STD.index(ch) + 1
        ids.append(x); cnt.append(int(v))
    return KN(np.array(ids, dtype=np.int64), np.array(cnt, dtype=np.int64), 4)


# ---- word model -----------------------------------------------------------------------
class Words:
    """Tokens are dictionary words (unigram frequencies from the corpus; dictionary words never seen count 0.5) or
    single letters (corpus letter frequencies); P(text) summed over every segmentation (forward algorithm)."""

    def __init__(self, train_words, dictionary, lam=0.9):
        cnt = {}
        for w in train_words:
            cnt[w] = cnt.get(w, 0) + 1
        for w in dictionary:
            if w not in cnt:
                cnt[w] = 0.5
        tot = sum(cnt.values())
        self.lp = {w: math.log2(lam * c / tot) for w, c in cnt.items()}
        f = np.bincount([STD.index(c) for c in "".join(train_words)], minlength=26) + 1.0
        self.lp1 = {STD[i]: math.log2((1 - lam) * f[i] / f.sum()) for i in range(26)}
        self.maxlen = 20

    def logprob(self, t):
        n = len(t)
        a = np.full(n + 1, -np.inf); a[0] = 0.0
        for i in range(1, n + 1):
            terms = [a[i - 1] + self.lp1[t[i - 1]]]
            for L in range(2, min(self.maxlen, i) + 1):
                w = t[i - L:i]
                if w in self.lp:
                    terms.append(a[i - L] + self.lp[w])
            mx = max(terms)
            a[i] = mx + math.log2(sum(2 ** (x - mx) for x in terms))
        return a[n]

    def logprob_windows(self, texts):
        return np.array([self.logprob(t) for t in texts])


# ---- run --------------------------------------------------------------------------------
def summary(lp):
    h = -lp / N
    return {"H_mean": round(float(h.mean()), 3), "bits_per_letter": round(LOG2_26 - float(h.mean()), 3),
            "H_median": round(float(np.median(h)), 3), "H_p90_least_predictable": round(float(np.percentile(h, 90)), 3),
            "bits_in_97": round(N * (LOG2_26 - float(h.mean())), 1), "windows": int(len(h))}


def run(ctx):
    t0 = time.time()
    rng = random.Random(SEED)
    C = corpus()
    codes = np.array([STD.index(c) + 1 for c in C["train"]], dtype=np.int64)
    ctx.progress(0, 10, "models")
    Q = quadgram_model()
    KNs = {n: KN.from_text(codes, n) for n in ORDERS}
    W = Words(C["train_words"], C["dictionary"])
    ctx.progress(2, 10, "models built")
    mcodes = np.array([STD.index(c) + 1 for c in C["train_manuals"]], dtype=np.int64)
    for n in OOD_ORDERS:
        KNs[f"{n}m"] = KN.from_text(mcodes, n)
    sets = {"clean": windows(C["test"]), "xstops": windows(C["test_xs"]), "k123": windows(C["k123"], 20),
            "k12": windows(C["k12"], 20)}
    sets["sub3"] = sub3(sets["clean"], rng)
    valid = windows(C["valid"])
    PQv = per_letter_probs(Q, valid)
    lam = {}
    for n in list(ORDERS) + [f"{o}m" for o in OOD_ORDERS]:
        Pn = per_letter_probs(KNs[n], valid)
        lam[n] = round(float(max(np.arange(0.05, 1.0, 0.05), key=lambda l: np.log2(l * PQv + (1 - l) * Pn).sum())), 2)
    ctx.progress(4, 10, "mixing weights")
    xent = {}
    PQ = {s: per_letter_probs(Q, ws) for s, ws in sets.items()}
    xent["Q"] = {s: summary(np.log2(PQ[s]).sum(axis=1)) for s in sets}
    for n in list(ORDERS) + [f"{o}m" for o in OOD_ORDERS]:
        Pn = {s: per_letter_probs(KNs[n], ws) for s, ws in sets.items()}
        xent[f"KN{n}"] = {s: summary(np.log2(Pn[s]).sum(axis=1)) for s in sets}
        xent[f"MIX{n}"] = {s: summary(np.log2(lam[n] * PQ[s] + (1 - lam[n]) * Pn[s]).sum(axis=1)) for s in sets}
    xent["W"] = {s: summary(W.logprob_windows(ws)) for s, ws in sets.items()}
    ctx.progress(6, 10, "cross-entropies")
    q_clean = xent["Q"]["clean"]["H_mean"]
    best_name = min(xent, key=lambda k: xent[k]["clean"]["H_mean"])
    best_ood = min((k for k in xent if k.endswith("m")), key=lambda k: xent[k]["clean"]["H_mean"])
    gain = {k: round(q_clean - v["clean"]["H_mean"], 3) for k, v in xent.items()}
    best_mix_n = min(ORDERS, key=lambda n: xent[f"MIX{n}"]["clean"]["H_mean"])
    # ladder
    pos = rng.sample(sets["clean"], N_LADDER_POS) + rng.sample(sets["xstops"], N_LADDER_POS)
    srng = np.random.default_rng(SEED + 1)
    wfreq = [w for w in C["train_words"] if len(w) >= 2 and w in C["dictionary"]]

    def salad():
        s = ""
        while len(s) < N:
            s += rng.choice(wfreq)
        return s[:N]
    neg = {"soup4 (from Q)": [Q.sample(srng) for _ in range(N_LADDER_NEG)],
           "soup6 (from KN6)": [KNs[6].sample(srng) for _ in range(N_LADDER_NEG)],
           "word salad": [salad() for _ in range(N_LADDER_NEG)]}
    ctx.progress(7, 10, "ladder texts")
    allt = pos + [t for v in neg.values() for t in v]
    Pn = per_letter_probs(KNs[best_mix_n], allt)
    PQa = per_letter_probs(Q, allt)
    scorers = {"Q": np.log2(PQa).sum(axis=1),
               f"MIX{best_mix_n}": np.log2(lam[best_mix_n] * PQa + (1 - lam[best_mix_n]) * Pn).sum(axis=1),
               "W": W.logprob_windows(allt)}
    jr = ctx.judge(allt)
    js = np.array([r["score"] if r and r.get("score") is not None else np.nan for r in jr], dtype=float)
    n_none = int(np.isnan(js).sum())
    scorers["judge"] = np.nan_to_num(js, nan=-1.0)       # None counts as not found (program.md)
    ctx.progress(9, 10, "judge")
    ladder = {}
    for name, sc in scorers.items():
        sp = {"clean": sc[:N_LADDER_POS], "xstops": sc[N_LADDER_POS:2 * N_LADDER_POS]}
        off = 2 * N_LADDER_POS
        ladder[name] = {}
        for rung, texts in neg.items():
            T = float(np.max(sc[off:off + len(texts)])); off += len(texts)
            found = {c: int((v > T).sum()) for c, v in sp.items()}
            ladder[name][rung] = {"threshold": round(T, 2), "found": found,
                                  "passes": all(f >= 0.9 * N_LADDER_POS for f in found.values())}
    # what the best model moves in F13.1's map (key bits from reports/f13-solvability-map.md)
    cells = {"F1.1 one free alphabet + key L = 26": 202.3, "F1.2 two free alphabets + key L = 13": 224.9,
             "F1.7 autokey on one free alphabet, lag 30": 221.1, "F10 Chaocipher": 176.8,
             "F6.2 two free alphabets after a width-10 columnar, L = 10": 232.6,
             "F1 running key from unknown English": 282.8}
    moved = {c: {"key_bits": b, "Q_clean": b < xent["Q"]["clean"]["bits_in_97"],
                 "best_out_of_domain_clean": b < xent[best_ood]["clean"]["bits_in_97"],
                 "best_out_of_domain_k12": b < xent[best_ood]["k12"]["bits_in_97"],
                 "best_clean": b < xent[best_name]["clean"]["bits_in_97"],
                 "best_xstops": b < xent[best_name]["xstops"]["bits_in_97"]} for c, b in cells.items()}
    bounds = {
        "item": "F13.3", "search_reads_known_letters": False,
        "models": {"Q": "the quadgram table (kryptos/data, 4.2e9 counts) as interpolated Kneser-Ney order 4",
                   **{f"KN{n}": f"interpolated Kneser-Ney order {n}, local corpus" for n in ORDERS},
                   **{f"MIX{n}": f"Q and KN{n} mixed, weight on Q {lam[n]} (validation)" for n in ORDERS},
                   **{f"KN{o}m": f"interpolated Kneser-Ney order {o}, manuals only (no Carter)" for o in OOD_ORDERS},
                   **{f"MIX{o}m": f"Q and KN{o}m mixed, weight on Q {lam[f'{o}m']}" for o in OOD_ORDERS},
                   "W": "word unigrams (corpus counts, dictionary words 0.5) or single letters, summed over segmentations"},
        "corpus_letters_train": int(len(C["train"])), "manual_lines_kept": C["manual_lines"],
        "test_windows": {s: len(v) for s, v in sets.items()}, "validation_windows": len(valid),
        "cross_entropy": xent, "best_model_clean": best_name, "gain_over_Q_bits_per_letter_clean": gain,
        "rule_stronger": "cross-entropy on clean held-out Carter at least 0.10 bits per letter under Q",
        "stronger_models": [k for k, v in gain.items() if v >= 0.10],
        "best_out_of_domain": best_ood, "out_of_domain_stronger": gain[best_ood] >= 0.10,
        "ladder": ladder, "ladder_rule": "a rung passes when at least 90% of clean and of X-stop windows (30 each) score above every one of its 40 negatives",
        "judge_calls": len(allt), "judge_none": n_none, "f13_1_cells": moved,
        "reference_0136_quadgram_H_carter_book": 2.916,
        "exhaustive": False, "compute_seconds": round(time.time() - t0),
    }
    notes = (f"clean Carter: Q {xent['Q']['clean']['bits_per_letter']} bits/letter; out of domain {best_ood} "
             f"{xent[best_ood]['clean']['bits_per_letter']} (K1+K2 {xent[best_ood]['k12']['bits_per_letter']}); in domain {best_name} "
             f"{xent[best_name]['clean']['bits_per_letter']}; stronger by the rule: {bounds['stronger_models'] or 'none'}; "
             "judge ladder: " + ", ".join(f"{r} {'pass' if v['passes'] else 'fail'}" for r, v in ladder["judge"].items()))
    ctx.progress(10, 10, "done")
    return {"candidates": [], "bounds": bounds, "notes": notes, "controls": []}


def encrypt(plaintext, key):
    """No candidate is submitted; identity for completeness."""
    return plaintext


def worked_example(ctx, key):
    Q = quadgram_model()
    t = "THEHOTAIRESCAPINGFROMTHECHAMBER"
    p = per_letter_probs(Q, [t])[0]
    h = float(-np.log2(p).mean())
    return "\n".join([
        "Cross-entropy, letter by letter, with the quadgram table (no history before the window):", "",
        "  letter  " + " ".join(f"{c:>5}" for c in t[:12]),
        "  -log2 P " + " ".join(f"{-math.log2(x):5.2f}" for x in p[:12]), "",
        f"  mean over the {len(t)} letters: {h:.2f} bits; evidence {LOG2_26 - h:.2f} bits per letter (log2 26 = 4.70)"])
