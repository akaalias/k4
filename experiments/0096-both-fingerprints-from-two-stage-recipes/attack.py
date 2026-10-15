"""Experiment 0096. See program.md for the contract."""

EXPERIMENT = {
    "slug": "both-fingerprints-from-two-stage-recipes",
    "title": "Which two-stage recipe, a move and a table, makes both of K4's width fingerprints at once",
    "family": "7-construction-simulation",
    "parent": "0065-constructions-that-line-up-doublets-in-sevens",
    "changed": "0018, 0027, 0062 and 0065 simulated one-stage recipes and asked about one fingerprint at a time. Here the recipes are the two-stage constructions of experiments 80 to 88 (a K3-style move before or after a repeating key, the self-feeding autokey, and 0087's column-plus-row key), and the question is the joint one: how often does a recipe make the width-7 doublet column and the width-21 repeats in the same 97 letters?",
    "hypothesis_expert": (
        "Type 2 of directions.md, open item 'a joint simulation that makes both fingerprints'. 0056: the width-7 doublet "
        "column (5 of 6 doublets in one column) and the width-21 vertical repeats (11 repeated letter pairs 21 apart) "
        "survive the look-elsewhere correction (corrected p 0.005 and 0.010); 0062 found ciphertext autokey at lag 21 "
        "raises the repeats, 0065 found ciphertext autokey at lag 1 with a period-7 key raises the column, and 0087 found "
        "that key = a[j mod 7] + b[j div 7] lines doublets up by construction. Recipes (each 20,000 samples of 97 "
        "letters from Carter vol. 1 and K1-K3, random keys): periodic key 7, 14 or 21 with a width-7 columnar, a "
        "width-7 quarter turn or a K3-rule move, before or after; ciphertext autokey lag 1 or lag 21 with a period-7 key, "
        "with a width-7 move before; the column-plus-row key at width 7 and 21, with and without a move before; and "
        "calibrations (random letters, shuffled K4, plain period-7 key). Marks as in 0065 (column: at least 4 doublets "
        "and all but one in one column at width 7) and 0056 (repeats: at least K4's 11 at width 21)."
    ),
    "hypothesis_eli5": (
        "K4 has two odd patterns: when written in rows of 7, its doubled letters stack in one column, and when written "
        "in rows of 21, letter pairs repeat straight down more than chance allows. A good guess at the method should "
        "make both patterns at once. We build thousands of fake coppers with each two-step recipe tried in experiments "
        "80 to 88, a grid move and the table, and count how often each recipe makes both patterns together."
    ),
    "prediction": (
        "No recipe makes both marks in more than 1% of samples. The column-plus-row key at width 7 makes the doublet "
        "column often (over 10%) but the width-21 repeats only at the chance rate; ciphertext autokey at lag 21 makes "
        "the repeats but not the column. Zero candidates."
    ),
    "method": (
        "1. Draw 97-letter stretches of English from Carter vol. 1 and K1-K3. 2. Encrypt each with a recipe and fresh "
        "random keys, routes and orders. 3. Mark the doublet column at width 7 and the repeats at width 21. 4. Count "
        "each mark and both together per recipe over 20,000 samples. 5. Compare with the calibrations."
    ),
    "walkthrough": (
        "1. Take 97 letters of Carter's English. "
        "2. Recipe example: write them in rows of 7, read the columns in a random order, then add a random 7-letter key on the sculpture's table. "
        "3. Find the doubled letters in the result and their places mod 7: is all but at most one in the same column, with at least four? "
        "4. Write the result in rows of 21 and count letter pairs that repeat straight down: at least 11? "
        "5. Repeat 20,000 times per recipe and count how often each mark and both appear."
    ),
}

import random
from collections import Counter
from pathlib import Path
from kryptos.facts import KRYPTOS_ALPHABET as KRY, load_k1, load_k2, load_k3
from kryptos.ciphers import columnar_transposition_encrypt

N = 97
ROOT = Path(__file__).resolve().parent
if not (ROOT / "knowledge").exists():
    ROOT = Path.cwd()
IDX = {c: i for i, c in enumerate(KRY)}
S = 20000


def letters(s):
    return "".join(c for c in s.upper() if "A" <= c <= "Z")


def doublets(t):
    return [i for i in range(len(t) - 1) if t[i] == t[i + 1]]


def col_mark(t):
    dbl = doublets(t)
    if len(dbl) < 4:
        return False
    top = max(Counter(i % 7 for i in dbl).values())
    return len(dbl) - top <= 1 and top >= 4


def rep21(t):
    v = [t[i] + t[i + 21] for i in range(len(t) - 21)]
    return len(v) - len(set(v))


def vig(pt, key):
    return "".join(KRY[(IDX[p] + key[i % len(key)]) % 26] for i, p in enumerate(pt))


def ct_auto(pt, key, lag, rng):
    out = []
    for i, p in enumerate(pt):
        prev = IDX[out[i - lag]] if i >= lag else rng.randrange(26)
        out.append(KRY[(IDX[p] + key[i % len(key)] + prev) % 26])
    return "".join(out)


def colrow(pt, w, rng):
    a = [rng.randrange(26) for _ in range(w)]
    b = [rng.randrange(26) for _ in range(-(-N // w))]
    return "".join(KRY[(IDX[p] + a[i % w] + b[i // w]) % 26] for i, p in enumerate(pt))


def turn7(t):
    rows = [t[i:i + 7] for i in range(0, len(t), 7)]
    return "".join(r[c] for c in range(7) for r in reversed(rows) if c < len(r))


def k3move(t, rng):
    b = rng.randrange(1, N); a = rng.randrange(N)
    out = [""] * N
    for i in range(N):
        out[(a + b * i) % N] = t[i]
    return "".join(out)


def col7(t, rng):
    return columnar_transposition_encrypt(t, rng.sample(range(7), 7))


def rk(rng, n):
    return [rng.randrange(26) for _ in range(n)]


def recipes():
    g = {}
    moves = {"width-7 columnar": col7, "width-7 quarter turn": lambda t, rng: turn7(t), "K3-rule move": k3move}
    for P in (7, 14, 21):
        for mn, mv in moves.items():
            g[f"period-{P} key, then {mn}"] = lambda pt, rng, P=P, mv=mv: mv(vig(pt, rk(rng, P)), rng)
            g[f"{mn}, then period-{P} key"] = lambda pt, rng, P=P, mv=mv: vig(mv(pt, rng), rk(rng, P))
    for lag in (1, 21):
        g[f"ciphertext autokey lag {lag} + period-7 key"] = lambda pt, rng, lag=lag: ct_auto(pt, rk(rng, 7), lag, rng)
        g[f"width-7 columnar, then ciphertext autokey lag {lag} + period-7 key"] = lambda pt, rng, lag=lag: ct_auto(col7(pt, rng), rk(rng, 7), lag, rng)
    for w in (7, 21):
        g[f"column-plus-row key, width {w}"] = lambda pt, rng, w=w: colrow(pt, w, rng)
        g[f"K3-rule move, then column-plus-row key, width {w}"] = lambda pt, rng, w=w: colrow(k3move(pt, rng), w, rng)
    g["calibration: period-7 key alone"] = lambda pt, rng: vig(pt, rk(rng, 7))
    g["calibration: random letters"] = lambda pt, rng: "".join(rng.choice(KRY) for _ in range(N))
    return g


def run(ctx):
    ct = ctx.K4
    carter = letters((ROOT / "knowledge" / "sources" / "carter-1923-tomb-of-tutankhamen-vol1.txt").read_text(errors="ignore"))
    k123 = letters(load_k1()["plaintext"] + load_k2()["plaintext_as_carved"] + load_k3()["plaintext"])
    source = carter + k123
    rng = random.Random(96)
    g = recipes()
    g["calibration: shuffled K4"] = lambda pt, rng: "".join(rng.sample(ct, N))
    k_rep = rep21(ct)
    assert col_mark(ct) and k_rep == 11
    table = {}
    for name, f in g.items():
        c = r = both = 0
        for _ in range(S):
            i = rng.randrange(0, len(source) - N)
            t = f(source[i:i + N], rng)
            a = col_mark(t); b = rep21(t) >= k_rep
            c += a; r += b; both += a and b
        table[name] = {"column": round(c / S, 4), "repeats": round(r / S, 4), "both": round(both / S, 4),
                       "both_if_independent": round((c / S) * (r / S), 5)}
        if ctx.time_left() < 60:
            break
    order = sorted(table.items(), key=lambda kv: (-kv[1]["both"], -kv[1]["column"]))
    bounds = {"family": "joint construction simulation of the width-7 doublet column and the width-21 repeats",
              "samples_per_recipe": S, "recipes": len(table),
              "k4": {"column": True, "repeats21": k_rep},
              "plaintext_source": f"Carter vol. 1 ({len(carter):,} letters) and K1-K3",
              "rates": dict(order),
              "best_both": order[0][0], "best_column": max(table, key=lambda k: table[k]["column"]),
              "best_repeats": max(table, key=lambda k: table[k]["repeats"])}
    notes = "Rates column / repeats / both: " + "; ".join(f"{k}: {v['column']:.4f} / {v['repeats']:.4f} / {v['both']:.4f}" for k, v in order[:12]) + "."
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct = ctx.K4
    dbl = doublets(ct)
    lines = ["K4's two marks", "", "doublets (place of first letter) and place mod 7:"]
    lines += [f"  {ct[i]}{ct[i + 1]} at {i + 1}-{i + 2}: column {i % 7}" for i in dbl]
    lines += ["", f"letter pairs 21 apart that repeat: {rep21(ct)}"]
    rows = [ct[i:i + 21] for i in range(0, N, 21)]
    lines += ["", "rows of 21:"] + ["  " + r for r in rows]
    return "\n".join(lines)
