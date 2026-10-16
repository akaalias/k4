"""Experiment 0170 (F12.4). See program.md for the contract."""

EXPERIMENT = {
    "slug": "pencil-session-observations",
    "title": "F12.4: a pencil session: K4 written out at widths 7, 8, 13, 14, 21, 24 and 31, six patterns noted by eye, each then tested against 1,000 shuffles",
    "family": "12-steins-way",
    "parent": "0168-k4-statistics-against-a-thousand-shuffles",
    "changed": (
        "F12.4. Stein: 'the process of discovery is often intuitive as well as analytic.' Before any search code, K4 was "
        "written out at the widths that matter with the known letters marked and looked at; these six patterns were noted "
        "and are tested here exactly as written, each against 1,000 letter-preserving shuffles: (1) the most copies of one "
        "letter in one column at width 7 (K: 4 of 8 at places 32, 46, 53, 74); (2) K, the commonest letter, in two adjacent "
        "width-7 columns (7 of 8: places 3, 32, 46, 53, 74, 87, 94); (3) the number of repeated bigrams (10: HU, SO, FB, GK, "
        "SS, QS, EK, KZ, TJ, DI); (4) how many of their spacings share the factor 4 (5 of 10: 20, 28, 32, 44, 48), Kasiski's "
        "test; (5) five of the six S's within 12 places (33-44: SSOTWTQSJQSS); (6) one letter three times at a fixed spacing "
        "of 2 or 3 (U at 88, 90, 92). An observation outside every shuffle becomes a new item."
    ),
    "hypothesis_expert": (
        "Stein 1999 (knowledge/sources/stein-1999-cracking-the-courtyard-crypto.txt): looking before attacking; F12.2 (0168) "
        "measured the fixed battery. These six are by-eye findings, so their selection is post hoc: the multiple-comparison "
        "count is the number of patterns a reader could have noticed, larger than six; a pattern counts only if outside "
        "every shuffle. Statistic definitions are in the method and fixed before the run."
    ),
    "hypothesis_eli5": (
        "We wrote the carved letters out in rows of different widths, as Stein did with pencil and paper, and noted what "
        "caught the eye: the letter K lining up in sevens, five S's crowded together, three U's two apart, letter pairs "
        "that repeat. Each is then checked against a thousand shufflings of the same letters; the eye finds patterns in "
        "random letters too."
    ),
    "prediction": "None of the six lies outside every shuffle (eye-found patterns in 97 letters are usually chance). Zero candidates.",
    "method": (
        "1. Statistics: (1) max over letters and residues mod 7 of the letter's count in that residue; (2) for the commonest "
        "letter, its largest count in two adjacent residues mod 7, as a share; (3) repeated bigrams (occurrences beyond the "
        "first); (4) repeated-bigram spacings divisible by 4; (5) for each letter with at least 6 copies, the shortest window "
        "holding all but one (smaller is more clustered); (6) the most equal letters in an arithmetic run with step 2 or 3. "
        "2. 1,000 shuffles (seed 1614); one-sided p in the direction observed."
    ),
    "walkthrough": (
        "1. Write K4 in rows of 7 and find the Ks: four sit in the fifth column, three in the fourth. "
        "2. Write K4 in a line and mark letter pairs that occur twice: ten of them; measure the distances between the two copies. "
        "3. Mark the S's: five fall between places 33 and 44. Mark the U's at 88, 90, 92. "
        "4. Shuffle the 97 letters and count the same things; repeat a thousand times; a pattern is real only if no shuffle matches it."
    ),
}

import random
from collections import Counter, defaultdict

N = 97
N_SHUF = 1000


def stats(t):
    out = {}
    best = 0
    for ch in set(t):
        c = Counter((i + 1) % 7 for i, x in enumerate(t) if x == ch)
        best = max(best, max(c.values()))
    out["(1) most of one letter in one width-7 column"] = best
    common = Counter(t).most_common(1)[0][0]
    ps = [i + 1 for i, x in enumerate(t) if x == common]
    c = Counter(p % 7 for p in ps)
    out["(2) commonest letter's share in two adjacent width-7 columns"] = max(c.get(r, 0) + c.get((r + 1) % 7, 0) for r in range(7)) / len(ps)
    bg = defaultdict(list)
    for i in range(N - 1):
        bg[t[i:i + 2]].append(i)
    rep = {k: v for k, v in bg.items() if len(v) > 1}
    out["(3) repeated bigrams"] = sum(len(v) - 1 for v in rep.values())
    sp = [b - a for v in rep.values() for a in v for b in v if b > a]
    out["(4) repeated-bigram spacings divisible by 4"] = sum(1 for d in sp if d % 4 == 0)
    w = 99
    for ch, n in Counter(t).items():
        if n >= 6:
            p = [i for i, x in enumerate(t) if x == ch]
            for a in range(len(p) - (n - 2)):
                w = min(w, p[a + n - 2] - p[a] + 1)
    out["(5) shortest window holding all but one copy of a 6-copy letter"] = w
    run = 1
    for step in (2, 3):
        for i in range(N):
            k = 1
            while i + k * step < N and t[i + k * step] == t[i]:
                k += 1
            run = max(run, k)
    out["(6) most equal letters at a fixed step of 2 or 3"] = run
    return out


SMALLER_IS_RARE = {"(5) shortest window holding all but one copy of a 6-copy letter"}


def run(ctx):
    ct = ctx.K4
    k4 = stats(ct)
    rng = random.Random(1614)
    sh = []
    for _ in range(N_SHUF):
        s = list(ct); rng.shuffle(s); sh.append(stats("".join(s)))
    rows = []
    for k, v in k4.items():
        xs = [d[k] for d in sh]
        if k in SMALLER_IS_RARE:
            p = sum(1 for x in xs if x <= v) / N_SHUF
            outside = v < min(xs)
        else:
            p = sum(1 for x in xs if x >= v) / N_SHUF
            outside = v > max(xs)
        rows.append({"observation": k, "k4": round(v, 4), "shuffles_min": round(min(xs), 4), "shuffles_max": round(max(xs), 4), "p_one_sided": p, "outside_every_shuffle": outside})
    outs = [r for r in rows if r["outside_every_shuffle"]]
    bounds = {"family": "observation: six by-eye patterns in K4 against 1,000 shuffles", "observations": rows, "outside_every_shuffle": outs,
              "note": "selected by eye, so post hoc; only an observation outside every shuffle would become an item",
              "controls": f"{N_SHUF} letter-preserving shuffles (seed 1614)"}
    notes = "; ".join(f"{r['observation']}: K4 {r['k4']}, p {r['p_one_sided']}" for r in rows)
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct = ctx.K4
    lines = ["K4 in rows of 7 (K in capitals, everything else lower case):", ""]
    for i in range(0, N, 7):
        lines.append("  " + " ".join(ch if ch == "K" else ch.lower() for ch in ct[i:i + 7]))
    lines += ["", "K at places " + ", ".join(str(i + 1) for i, ch in enumerate(ct) if ch == "K")]
    return "\n".join(lines)
