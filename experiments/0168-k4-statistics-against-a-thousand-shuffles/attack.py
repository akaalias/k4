"""Experiment 0168 (F12.2). See program.md for the contract."""

EXPERIMENT = {
    "slug": "k4-statistics-against-a-thousand-shuffles",
    "title": "F12.2: Stein's way, step one: K4's statistics by segment and by width (letter counts per segment, index of coincidence for 1-48 alphabets, repeats at widths 7, 21 and 31), each against 1,000 shuffles, with the number of comparisons stated",
    "family": "12-steins-way",
    "parent": "0056-look-elsewhere-for-the-two-fingerprints",
    "changed": (
        "F12.2. Stein began K1-K3 by quantifying impressions: letter counts by carved row (his Figure 3 split the panel "
        "at row 14/15) and the index of coincidence against the number of alphabets (his Figures 7, 17, 26). 0056 measured "
        "two of K4's patterns. Here a fixed battery, set before the run: (1) whether K4's letters are spread evenly across "
        "segments (the carved lines 1-4, 5-35, 36-66, 67-97; halves at 48/49; thirds; the stretch before EAST, between the "
        "runs, after CLOCK): chi-square of the segment-by-letter table; (2) the average index of coincidence when K4 is "
        "cut into m alphabets, m 1-48; (3) at widths 7, 21 and 31: repeated vertical bigrams (0056's statistic), vertical repeats (same letter directly below), "
        "diagonal repeats (one row down, one column right and left), and the largest number of horizontal doublets in "
        "one column. Each statistic against 1,000 letter-preserving shuffles: the two-sided rank p. An observation counts "
        "as outside the shuffles only if no shuffle is as extreme (p < 0.001, two-sided 0.002), and the number of "
        "statistics is stated so the expected number of such accidents is known."
    ),
    "hypothesis_expert": (
        "Stein 1999 (knowledge/sources/stein-1999-cracking-the-courtyard-crypto.txt): 'I seemed to see different patterns "
        "throughout, but I wanted to quantify these impressions'; the row-wise frequency break between rows 14 and 15; the "
        "I.C. plots. C28 (the m = 13 peak) is F12.3. 0056: the width-7 doublet column and width-21 vertical repeats against "
        "10,000 shuffles (corrected p 0.005 and 0.010). Shuffles keep K4's letters and permute positions. Statistics: S = "
        "8 segment tables + 48 I.C. values + 3 widths x 5 repeat statistics = 71; at p < 0.002 two-sided about 0.14 false "
        "outliers expected. Any statistic outside every shuffle becomes a new item (F12.5 if it is a segment break)."
    ),
    "hypothesis_eli5": (
        "Before attacking a cipher, Stein measured it: how evenly each letter is spread along the text, and how the "
        "letters behave when the text is cut into a number of interleaved strands. We measure K4 the same way, seventy-one "
        "measurements in all, and compare each with a thousand random shufflings of K4's own letters. Only a measurement "
        "that no shuffling matches is reported as a real feature; with this many measurements, about one in seven of a "
        "single such accident would be expected by luck."
    ),
    "prediction": (
        "The two known fingerprints come out at the edge (the width-7 doublet column near p 0.002-0.005, the width-21 "
        "vertical repeats near p 0.01), but with 71 statistics nothing lies outside every shuffle; no segment break; no "
        "I.C. peak at any m. Zero candidates."
    ),
    "method": (
        "1. Compute the 71 statistics on K4. "
        "2. 1,000 shuffles of K4's letters (seed 1612): the same statistics. "
        "3. For each, the two-sided rank p; list those beyond every shuffle; state the multiple-comparison count."
    ),
    "walkthrough": (
        "1. Cut K4 at the ends of its carved lines and count each letter in each piece; compare how uneven the counts are with the same for shuffled K4. "
        "2. Write K4 in m interleaved strands (every m-th letter) for m = 1 to 48; in each strand count how often two letters drawn at random match; average. "
        "3. Write K4 in rows of 7, 21 and 31; count letters that repeat directly below, or diagonally below, and the doublets falling in one column. "
        "4. Shuffle K4's letters 1,000 times and repeat every count; a feature is real only if K4 is more extreme than every shuffle."
    ),
}

import random
from collections import Counter

N = 97
N_SHUF = 1000


def segments():
    return {
        "carved lines (1-4, 5-35, 36-66, 67-97)": [(0, 4), (4, 35), (35, 66), (66, 97)],
        "halves at 48/49": [(0, 48), (48, 97)],
        "thirds": [(0, 32), (32, 65), (65, 97)],
        "before EAST, the runs and between, after CLOCK": [(0, 21), (21, 34), (34, 63), (63, 74), (74, 97)],
        "quarters": [(0, 24), (24, 48), (48, 72), (72, 97)],
        "before and after BERLINCLOCK's start": [(0, 63), (63, 97)],
        "first 21, rest": [(0, 21), (21, 97)],
        "fifths": [(0, 19), (19, 39), (39, 58), (58, 78), (78, 97)],
    }


def chi2(text, segs):
    tot = Counter(text)
    s = 0.0
    for a, b in segs:
        part = Counter(text[a:b])
        n = b - a
        for ch, c in tot.items():
            e = c * n / N
            s += (part.get(ch, 0) - e) ** 2 / e
    return s


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


def width_stats(text, w):
    rows = [text[i:i + w] for i in range(0, N, w)]
    vert = diag_r = diag_l = 0
    for r in range(len(rows) - 1):
        for c in range(len(rows[r + 1])):
            if rows[r][c] == rows[r + 1][c]:
                vert += 1
            if c + 1 < len(rows[r + 1]) and rows[r][c] == rows[r + 1][c + 1]:
                diag_r += 1
            if c - 1 >= 0 and c - 1 < len(rows[r + 1]) and rows[r][c] == rows[r + 1][c - 1]:
                diag_l += 1
    col = Counter(i % w for i in range(N - 1) if text[i] == text[i + 1])
    bigr = Counter((text[i], text[i + w]) for i in range(N - w))
    rep_bi = sum(v - 1 for v in bigr.values() if v > 1)
    return {"repeated vertical bigrams (0056's statistic)": rep_bi, "vertical repeats": vert, "diagonal repeats right": diag_r, "diagonal repeats left": diag_l,
            "most doublets in one column": max(col.values()) if col else 0}


def all_stats(text):
    out = {}
    for name, segs in segments().items():
        out[f"segments: {name}"] = chi2(text, segs)
    for m in range(1, 49):
        out[f"I.C. at {m} alphabets"] = ic_avg(text, m)
    for w in (7, 21, 31):
        for k, v in width_stats(text, w).items():
            out[f"width {w}: {k}"] = v
    return out


def run(ctx):
    ct = ctx.K4
    k4 = all_stats(ct)
    rng = random.Random(1612)
    sh = []
    for _ in range(N_SHUF):
        s = list(ct); rng.shuffle(s); sh.append(all_stats("".join(s)))
    rows = []
    for k, v in k4.items():
        xs = [d[k] for d in sh]
        ge = sum(1 for x in xs if x >= v) / N_SHUF
        le = sum(1 for x in xs if x <= v) / N_SHUF
        p = min(1.0, 2 * min(ge, le))
        outside = (v > max(xs)) or (v < min(xs))
        rows.append({"statistic": k, "k4": round(v, 5), "shuffles_min": round(min(xs), 5), "shuffles_max": round(max(xs), 5),
                     "p_two_sided": round(p, 4), "outside_every_shuffle": outside})
    S = len(rows)
    outs = [r for r in rows if r["outside_every_shuffle"]]
    smallest = sorted(rows, key=lambda r: r["p_two_sided"])[:10]
    bounds = {"family": "observation, not a cipher: K4's statistics against 1,000 shuffles", "statistics": S, "shuffles": N_SHUF,
              "expected_outliers_by_chance_at_p_0_002": round(S * 0.002, 2), "outside_every_shuffle": outs, "smallest_p": smallest,
              "all": rows, "controls": f"{N_SHUF} letter-preserving shuffles of K4 (seed 1612)"}
    notes = f"{S} statistics x {N_SHUF} shuffles: outside every shuffle {len(outs)} ({[o['statistic'] for o in outs]}); smallest p " + ", ".join(f"{r['statistic']} {r['p_two_sided']}" for r in smallest[:4])
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct = ctx.K4
    lines = ["K4 in rows of 7 (doublets marked by the column they start in):", ""]
    for i in range(0, N, 7):
        lines.append("  " + " ".join(ct[i:i + 7]))
    col = Counter(i % 7 for i in range(N - 1) if ct[i] == ct[i + 1])
    lines += ["", f"doublets by starting column (0-6): {dict(sorted(col.items()))}",
              f"index of coincidence of all 97 letters: {ic_avg(ct, 1):.4f} (random 26 letters: 0.0385; English: 0.066)"]
    return "\n".join(lines)
