"""Experiment 0068. See program.md for the contract."""

EXPERIMENT = {
    "slug": "ciphertext-autokey-with-one-wrong-carved-letter",
    "title": "The self-feeding autokey again, allowing one carved letter to be wrong, missing or extra",
    "family": "1-keyed-periodic",
    "parent": "0002-ciphertext-autokey-all-lags",
    "changed": "Experiment 2 tested the self-feeding autokey on the copper exactly as carved, and experiment 62 found it is the only recipe that makes the width-21 repeats. K2 has a known carving error. Here one carved letter may be wrong (any place, any other letter), missing, or extra, at every lag, with or without a constant shift.",
    "hypothesis_expert": (
        "Family 1 re-entered with a stated reason: ciphertext autokey is the only generator in 0062 that "
        "reproduces the width-21 repeats (lag 21, 5.4% of samples against 0.2%), and 0002, 0063 and 0064 "
        "tested it only on the exact copper. Sanborn's K2 has a confirmed carving omission (C14 in "
        "02-sanborn-said.md; Kryptos Group 2006, sources/kryptos-group-2006-corrected-k2.txt), and C17/C18 "
        "allow a working text of 98. Construction: T[i] = s*A(c[i-L]) + k0, L = 1..96, k0 any constant (k0 = 0 "
        "is the plain autokey), plain, cipher and key alphabets standard or KRYPTOS, Vigenere or Beaufort, "
        "s = +1 or -1 (32 classes). Variants of the copper: one letter replaced by any other (97 x 25), one "
        "deleted (97), one unknown inserted (98). A substitution at place j can only touch the equation of "
        "the crib at j and of the crib at j + L, so substitutions are decided exactly by asking whether all "
        "other residuals agree and the touched ones can be met by one letter; deletions and insertions are "
        "recomputed in full. Survivors tallied by redundant checks against ten shuffled coppers. Clue "
        "entries: C11a ('auto-key'), C17(b), C18(b)."
    ),
    "hypothesis_eli5": (
        "The autokey that feeds on earlier carved letters is the only recipe we have found that leaves the "
        "width-21 mark, yet experiment 2 showed it cannot produce the known letters from the copper as carved. "
        "The second message on the sculpture has a carving mistake, so we allow one mistake here too: one "
        "letter wrong, one missing or one extra, anywhere, at every distance back. Scrambled coppers given the "
        "same allowance show how many fits luck gives."
    ),
    "prediction": (
        "No lag survives with three or more redundant checks under any one-letter variant and class, "
        "including lag 21. Survivor counts at one and two checks match the ten shuffled coppers. Zero "
        "candidates pass."
    ),
    "method": (
        "1. For each lag and class, compute the residual at each known place past the lag: the total key "
        "minus the value of the carved letter that far back. 2. Exact copper: all residuals must agree. "
        "3. One wrong letter at place j: all residuals not touching j must agree, and the one or two touched "
        "must be met by a single replacement letter. 4. One letter missing or extra: shift the copper and "
        "recompute. 5. Tally survivors by redundant checks and compare with ten shuffled coppers."
    ),
    "walkthrough": (
        "1. Take lag 21, the sculpture's alphabet KRYPTOSABCDEFGHIJLMNQUVWXZ counted from K = 0, Vigenere. "
        "2. Place 22: carved F (12) minus known E (11) is 1; the carved letter 21 back is O (5); the residual "
        "is 1 - 5 = -4, which is 22. 3. Place 23: L (17) minus A (7) is 10; 21 back is B (8); residual 2. "
        "4. Place 24: R (1) minus S (6) is 21; 21 back is K (0); residual 21. 5. The plain autokey needs every "
        "residual to be the same constant; already three differ. 6. One wrong carved letter can change at "
        "most two residuals, its own and the one 21 places later, so if more than two residuals disagree "
        "with the rest, no single mistake rescues this lag."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
ALPH = {"std": STD, "kry": KRY}


def classes():
    for pa in ALPH:
        for ca in ALPH:
            for ka in ALPH:
                for mode in ("vig", "beau"):
                    for s in (1, -1):
                        yield pa, ca, ka, mode, s


def tval(cidx, pidx, mode):
    return (cidx - pidx) % 26 if mode == "vig" else (cidx + pidx) % 26


def residuals(v, known, L, cl):
    pa, ca, ka, mode, s = cl
    out = []
    for pos, p in known:
        i = pos - 1
        if i - L < 0 or i >= len(v) or v[i] == "?" or v[i - L] == "?":
            continue
        out.append((i, (tval(ALPH[ca].index(v[i]), ALPH[pa].index(p), mode) - s * ALPH[ka].index(v[i - L])) % 26))
    return out


def all_equal(rs):
    return len({r for _, r in rs}) <= 1


def substitution_survivors(ct, known, L, cl):
    """Exact: does one replaced letter make every residual agree? Returns list of (j, letter, checks)."""
    pa, ca, ka, mode, s = cl
    rs = residuals(ct, known, L, cl)
    if len(rs) < 3:
        return []
    out = []
    kmap = dict(known)
    places = sorted({i for i, _ in rs} | {i - L for i, _ in rs})
    for j in places:
        rest = [(i, r) for i, r in rs if i != j and i - L != j]
        touched = [i for i, r in rs if i == j or i - L == j]
        if not rest or not all_equal(rest):
            continue
        v = rest[0][1]
        for letter in KRY:
            if letter == ct[j]:
                continue
            w = ct[:j] + letter + ct[j + 1:]
            ok = True
            for i in touched:
                r = (tval(ALPH[ca].index(w[i]), ALPH[pa].index(kmap[i + 1]), mode) - s * ALPH[ka].index(w[i - L])) % 26
                if r != v:
                    ok = False; break
            if ok:
                out.append((j, letter, len(rest) - 1 + len(touched)))
    return out


def sweep(ct, known, ctx, deadline):
    kn = sorted(known.items())
    tally, hits, cases = {}, [], 0
    shifted = [("deleted " + str(j + 1), ct[:j] + ct[j + 1:]) for j in range(N)] + [("inserted before " + str(j + 1), ct[:j] + "?" + ct[j:]) for j in range(N + 1)]
    for cl in classes():
        for L in range(1, 97):
            cases += 1
            rs = residuals(ct, kn, L, cl)
            if len(rs) >= 2 and all_equal(rs):
                c = len(rs) - 1
                tally[("exact", min(c, 5))] = tally.get(("exact", min(c, 5)), 0) + 1
                hits.append({"variant": "exact", "lag": L, "class": "/".join(map(str, cl)), "checks": c})
            for j, letter, c in substitution_survivors(ct, kn, L, cl):
                cases += 0
                if c >= 1:
                    tally[("substitution", min(c, 5))] = tally.get(("substitution", min(c, 5)), 0) + 1
                    if c >= 3 or L == 21:
                        hits.append({"variant": f"place {j + 1} carved {letter}", "lag": L, "class": "/".join(map(str, cl)), "checks": c})
            for name, v in shifted:
                cases += 1
                rs = residuals(v, kn, L, cl)
                if len(rs) >= 2 and all_equal(rs):
                    c = len(rs) - 1
                    tally[("shift", min(c, 5))] = tally.get(("shift", min(c, 5)), 0) + 1
                    if c >= 3 or L == 21:
                        hits.append({"variant": name, "lag": L, "class": "/".join(map(str, cl)), "checks": c})
        if ctx.time_left() < deadline:
            return tally, hits, cases, False
    return tally, hits, cases, True


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    t0 = ctx.time_left()
    tally, hits, cases, complete = sweep(ct, known, ctx, t0 * 0.55)
    rng = random.Random(68)
    ctrl = []
    for r in range(10):
        sh = list(ct); rng.shuffle(sh)
        t, _, c2, comp = sweep("".join(sh), known, ctx, 25)
        ctrl.append((t, comp))
        if ctx.time_left() < 30:
            break
    keys = sorted(set(tally) | {k for t, _ in ctrl for k in t})
    table = {f"{k[0]}, checks {k[1]}{'+' if k[1] == 5 else ''}": {"k4": tally.get(k, 0), "controls": [t.get(k, 0) for t, _ in ctrl]} for k in keys}
    strong = [h for h in hits if h["checks"] >= 3]
    lag21 = [h for h in hits if h["lag"] == 21]
    return {
        "candidates": [],
        "bounds": {"family": "ciphertext autokey with a constant shift, copper with one letter wrong, missing or extra",
                   "lags": "1-96", "classes": 32, "variants": "97 x 25 substitutions (decided exactly), 97 deletions, 98 insertions",
                   "cases": cases, "complete": complete, "controls": [comp for _, comp in ctrl],
                   "survivors_by_checks": table, "survivors_3plus": strong[:40], "lag21_survivors": lag21[:40]},
        "notes": f"{cases} lag-class-variant cases ({'complete' if complete else 'stopped early'}). Survivors, K4 (controls min-max): " + "; ".join(
            f"{k}: {v['k4']} ({min(v['controls']) if v['controls'] else '-'}-{max(v['controls']) if v['controls'] else '-'})" for k, v in table.items())
            + f". Three or more checks: {len(strong)}. Lag 21: {len(lag21)}.",
    }


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    I = {c: i for i, c in enumerate(KRY)}
    ct, kn = ctx.K4, ctx.KNOWN
    lines = ["lag 21, sculpture's alphabet throughout, Vigenere", "", "place  known  carved  21 back  residual"]
    for pos in (22, 23, 24, 25, 26):
        r = (I[ct[pos - 1]] - I[kn[pos]] - I[ct[pos - 22]]) % 26
        lines.append(f"{pos:>5}  {kn[pos]:>5}  {ct[pos - 1]:>6}  {ct[pos - 22]:>7}  {r:>8}")
    return "\n".join(lines)
