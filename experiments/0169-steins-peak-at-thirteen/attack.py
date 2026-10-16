"""Experiment 0169 (F12.3). See program.md for the contract."""

EXPERIMENT = {
    "slug": "steins-peak-at-thirteen",
    "title": "F12.3: Stein's index-of-coincidence peak at 13 alphabets in K1 and K2: real or chance, against shuffles that keep each part's own key period",
    "family": "12-steins-way",
    "parent": "0168-k4-statistics-against-a-thousand-shuffles",
    "changed": (
        "F12.3 (C28). Stein found a peak in the average index of coincidence at m = 13 alphabets in K1 (his Part I, key "
        "length 10) and in K2's Part II (the 125 letters between the panel's first two question marks, key length 8) and "
        "asked: 'Could this be a sign of another code overlaid on top of the others... Or just a coincidence?' Here the "
        "question is answered against the right null: shuffles that keep each part's key-period structure (letters "
        "permuted only within their own key column), 10,000 per text; also plain shuffles. Statistics: the I.C. at 13 "
        "and the local peak (I.C. at 13 minus the larger of 12 and 14). Texts: K1, K2 Part II (Stein's), K2 Part III, all "
        "of K2, and the K1 and K2 plaintexts. K4's own value at 13 is in 0168 (p 0.21)."
    ),
    "hypothesis_expert": (
        "C28 (knowledge/11-clue-register.md); Stein 1999 (knowledge/sources/stein-1999-cracking-the-courtyard-crypto.txt), "
        "Figures 7, 17, 26: 'I knew that the peak at m = 10 was caused by the 10-letter keyword, and the peaks at 5 and 15 "
        "are expected artifacts... But what was this peak at m = 13? ... it also showed up in the I.C. plot for Part II.' "
        "Model of the null: a Quagmire III ciphertext of period L has column multisets fixed by the plaintext and key; "
        "permuting letters within each column (place mod L) keeps every period-L property and destroys any other "
        "structure. If K1's and Part II's I.C. at 13 sit inside that null, the peak is a coincidence of the plaintext's "
        "letters; if outside, something keyed at 13 exists and K4 would be tested for it."
    ),
    "hypothesis_eli5": (
        "When Stein cut the first two messages into 13 interleaved strands, the letters matched a little more often than "
        "expected, and he wondered whether a second, 13-letter code lay underneath. We check whether that bump is "
        "bigger than what the known keys alone would give, by shuffling the letters only among positions that share a key "
        "letter, 10,000 times."
    ),
    "prediction": "The m = 13 values sit inside the key-period null for K1 and Part II (p above 0.05): a coincidence of short texts. Zero candidates.",
    "method": (
        "1. Texts: K1 (63), K2 Part II (125), Part III (61), K2 without '?' (369), K1 and K2 plaintexts. "
        "2. I.C. averaged over m interleaved strands, m 12-14; the peak statistic. "
        "3. 10,000 within-column shuffles (key period 10 for K1, 8 for K2) and 10,000 plain shuffles per text: one-sided p."
    ),
    "walkthrough": (
        "1. Write K1's 63 letters into 13 strands: letters 1, 14, 27, ...; 2, 15, 28, ...; and so on. "
        "2. In each strand count the pairs of equal letters, divide by the possible pairs, and average over the 13 strands. "
        "3. Shuffle K1's letters, but only among places that used the same key letter (places 1, 11, 21, ... together), and recompute; repeat 10,000 times. "
        "4. If K1's value is above nearly all the shuffled values, the bump at 13 is more than the key explains."
    ),
}

import json
import random
from collections import Counter

N_SHUF = 10000


def ic_avg(text, m):
    vals = []
    for j in range(m):
        col = text[j::m]
        n = len(col)
        if n < 2:
            continue
        c = Counter(col)
        vals.append(sum(v * (v - 1) for v in c.values()) / (n * (n - 1)))
    return sum(vals) / len(vals)


def stats(text):
    a, b, c = ic_avg(text, 12), ic_avg(text, 13), ic_avg(text, 14)
    return b, b - max(a, c)


def within_shuffle(text, L, rng):
    cols = {}
    for i, ch in enumerate(text):
        cols.setdefault(i % L, []).append(ch)
    for v in cols.values():
        rng.shuffle(v)
    it = {k: iter(v) for k, v in cols.items()}
    return "".join(next(it[i % L]) for i in range(len(text)))


def run(ctx):
    k1 = json.load(open("data/k1.json")); k2 = json.load(open("data/k2.json"))
    c2 = k2["ciphertext_as_carved"]
    q = [i for i, ch in enumerate(c2) if ch == "?"]
    texts = {
        "K1 ciphertext (Stein's Part I, key 10)": (k1["ciphertext"], 10),
        "K2 Part II (Stein's 125 letters, key 8)": (c2[q[0] + 1:q[1]], 8),
        "K2 Part III (key 8)": (c2[q[1] + 1:q[2]], 8),
        "K2 ciphertext without '?' (key 8)": (c2.replace("?", ""), 8),
        "K1 plaintext": ("".join(ch for ch in k1["plaintext"] if ch.isalpha()), None),
        "K2 plaintext": ("".join(ch for ch in k2["plaintext_as_carved"] if ch.isalpha()), None),
    }
    assert len(texts["K2 Part II (Stein's 125 letters, key 8)"][0]) == 125 and len(texts["K1 ciphertext (Stein's Part I, key 10)"][0]) == 63
    rng = random.Random(1613)
    rows = []
    for name, (t, L) in texts.items():
        ic13, peak = stats(t)
        res = {"text": name, "letters": len(t), "ic13": round(ic13, 5), "peak13": round(peak, 5)}
        for null in (("within key columns", L), ("plain shuffles", None)):
            if null[1] is None and L is not None and null[0] == "within key columns":
                continue
            if null[0] == "within key columns" and L is None:
                continue
            ge_ic = ge_pk = 0
            for _ in range(N_SHUF):
                if null[1]:
                    s = within_shuffle(t, null[1], rng)
                else:
                    s = list(t); rng.shuffle(s); s = "".join(s)
                a, b = stats(s)
                ge_ic += a >= ic13
                ge_pk += b >= peak
            res[f"p_ic13 ({null[0]})"] = round((ge_ic + 1) / (N_SHUF + 1), 4)
            res[f"p_peak13 ({null[0]})"] = round((ge_pk + 1) / (N_SHUF + 1), 4)
        rows.append(res)
    stein = [r for r in rows if r["text"].startswith(("K1 ciphertext", "K2 Part II"))]
    real = [r["text"] for r in stein if r.get("p_ic13 (within key columns)", 1) < 0.01]
    bounds = {"family": "observation: the I.C. at 13 alphabets in K1 and K2 against key-period-preserving shuffles", "shuffles": N_SHUF,
              "rows": rows, "stein_texts_below_p_0_01": real,
              "controls": f"{N_SHUF} within-key-column shuffles and {N_SHUF} plain shuffles per text (seed 1613)"}
    notes = "; ".join(f"{r['text']}: I.C.13 {r['ic13']}, p within-columns {r.get('p_ic13 (within key columns)', '-')}, plain {r.get('p_ic13 (plain shuffles)')}" for r in rows)
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    k1 = json.load(open("data/k1.json"))["ciphertext"]
    lines = ["K1's 63 letters in 13 strands (letter i goes to strand i mod 13):", ""]
    for j in range(13):
        lines.append(f"  strand {j + 1:2d}: {k1[j::13]}")
    lines += ["", f"average index of coincidence over the 13 strands: {ic_avg(k1, 13):.4f}; over 10 strands (the key length): {ic_avg(k1, 10):.4f}"]
    return "\n".join(lines)
