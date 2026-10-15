"""Experiment 0056. See program.md for the contract."""

EXPERIMENT = {
    "slug": "width-7-and-21-fingerprints-look-elsewhere",
    "title": "Are the copper's two odd patterns odd at all once every width is counted?",
    "family": "7-construction-simulation",
    "parent": "0027-simulator-round-two-width-21-hunt",
    "changed": "Experiments 18 and 27 found two patterns in K4 that no construction reproduced well: five of its six doubled letters fall in one column when the text is written in rows of 7, and pairs of letters 21 places apart repeat eleven times. Both were found by looking at many widths. This asks how often a scrambled copper shows a pattern that strong at some width, which is the fair comparison.",
    "hypothesis_expert": (
        "The width-7 doublet column (5 of 6 doublets at one position mod 7) and the width-21 vertical "
        "repeats (11 repeated pairs (c[i], c[i+21])) were selected after scanning widths, so their nominal "
        "p-values (0.01-0.1 in 0018) overstate them. For every width w in 2-48 compute both statistics on "
        "K4 and on 10,000 letter-preserving shuffles; turn each into a per-width tail probability from the "
        "shuffle distribution; take the smallest tail probability over widths as the scan statistic; and "
        "compare K4's scan statistic with the shuffles' (the look-elsewhere correction). Also condition the "
        "doublet statistic on shuffles with exactly six doublets, since K4 has six. If K4's corrected "
        "p-values exceed 0.05, family 7's two unexplained features are not evidence for any construction. "
        "Bounds: widths 2-48, 10,000 controls."
    ),
    "hypothesis_eli5": (
        "If you write the copper in rows of 7 letters, five of its six doubled letters line up in one "
        "column, and in rows of 21 the same letter pairs stack up more than usual. That looks like a clue "
        "to how it was made. But we found those widths by trying many widths, and if you try enough widths "
        "something always lines up. So we scramble the copper ten thousand times, try every width from 2 to "
        "48 on each scramble, and see how often a scramble looks at least this odd at its best width."
    ),
    "prediction": (
        "After the correction neither pattern is unusual: K4's scan p-value is above 0.05 for both, so the "
        "two features need no explanation. Zero candidates."
    ),
    "method": (
        "1. For widths 2-48 compute, on K4, the largest number of doublets sharing a column and the number "
        "of repeated vertical pairs. 2. Do the same on 10,000 shuffles. 3. Per width, the tail probability "
        "of each value among the shuffles. 4. Per text, the smallest tail probability over widths. 5. K4's "
        "rank among the shuffles is the corrected p-value; repeat with six-doublet shuffles only."
    ),
    "walkthrough": (
        "1. Find the doubled letters in the copper: BB at places 19-20, QQ at 26-27, SS at 33-34, SS at 43-44, "
        "ZZ at 47-48 and TT at 68-69. 2. Write the copper in rows of 7: the first letter of each doublet sits "
        "in column 19 mod 7 = 5, 26 mod 7 = 5, 33 mod 7 = 5, 43 mod 7 = 1, 47 mod 7 = 5, 68 mod 7 = 5. 3. "
        "Count: column 5 holds five of the six doublets. 4. Shuffle the 97 letters, find the doubled "
        "letters again, and count the fullest column at every width from 2 to 48. 5. Note how odd the "
        "fullest column is at its best width. 6. Do it ten thousand times and see where the copper falls."
    ),
}

import random
from collections import Counter

WIDTHS = range(2, 49)


def encrypt(plaintext, key):
    return plaintext


def feats(t):
    n = len(t)
    dbl = [i for i in range(n - 1) if t[i] == t[i + 1]]
    col = {w: (max(Counter(i % w for i in dbl).values()) if dbl else 0) for w in WIDTHS}
    rep = {}
    for w in WIDTHS:
        v = [t[i] + t[i + w] for i in range(n - w)]
        rep[w] = len(v) - len(set(v))
    return len(dbl), col, rep


def run(ctx):
    ct = ctx.K4
    nd, col_k, rep_k = feats(ct)
    rng = random.Random(56)
    sims = []
    letters = list(ct)
    for _ in range(10000):
        rng.shuffle(letters)
        sims.append(feats("".join(letters)))
        if ctx.time_left() < 120:
            break
    S = len(sims)
    dist_col = {w: Counter(s[1][w] for s in sims) for w in WIDTHS}
    dist_rep = {w: Counter(s[2][w] for s in sims) for w in WIDTHS}

    def tail(dist, w, v):
        return sum(c for x, c in dist[w].items() if x >= v) / S

    def scan(col, rep):
        pc = min(tail(dist_col, w, col[w]) for w in WIDTHS)
        pr = min(tail(dist_rep, w, rep[w]) for w in WIDTHS)
        return pc, pr

    k_pc, k_pr = scan(col_k, rep_k)
    sim_scans = [scan(s[1], s[2]) for s in sims]
    p_col = sum(1 for a, _ in sim_scans if a <= k_pc) / S
    p_rep = sum(1 for _, b in sim_scans if b <= k_pr) / S
    six = [i for i, s in enumerate(sims) if s[0] == nd]
    p_col_six = (sum(1 for i in six if sim_scans[i][0] <= k_pc) / len(six)) if six else None
    nominal7 = tail(dist_col, 7, col_k[7]); nominal21 = tail(dist_rep, 21, rep_k[21])
    best_w_col = min(WIDTHS, key=lambda w: tail(dist_col, w, col_k[w]))
    best_w_rep = min(WIDTHS, key=lambda w: tail(dist_rep, w, rep_k[w]))
    return {
        "candidates": [],
        "bounds": {"family": "look-elsewhere test of the width fingerprints", "widths": "2-48", "controls": S,
                   "k4_doublets": nd, "k4_col7": col_k[7], "k4_rep21": rep_k[21],
                   "nominal_p_col7": round(nominal7, 4), "nominal_p_rep21": round(nominal21, 4),
                   "k4_best_width_col": best_w_col, "k4_best_width_rep": best_w_rep,
                   "corrected_p_doublet_column": round(p_col, 4), "corrected_p_doublet_column_six_doublet_shuffles": None if p_col_six is None else round(p_col_six, 4),
                   "six_doublet_shuffles": len(six), "corrected_p_vertical_repeats": round(p_rep, 4)},
        "notes": (f"{S} shuffles, widths 2-48. Doublet column: nominal p at width 7 {nominal7:.4f}, corrected over widths {p_col:.4f}"
                  f" ({p_col_six if p_col_six is None else round(p_col_six, 4)} among the {len(six)} shuffles with {nd} doublets). Vertical repeats: nominal p at width 21 {nominal21:.4f}, corrected {p_rep:.4f}."),
    }


def worked_example(ctx, key):
    t = ctx.K4
    dbl = [i for i in range(len(t) - 1) if t[i] == t[i + 1]]
    lines = ["doublets (place of first letter, 1-based):"]
    for i in dbl:
        lines.append(f"  {t[i]}{t[i + 1]} at {i + 1}-{i + 2}: column (0-based index mod 7) {i % 7}")
    return "\n".join(lines)
