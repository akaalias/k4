"""Experiment 0046. See program.md for the contract."""

EXPERIMENT = {
    "slug": "gromark-three-term-rules-and-higher-bases",
    "title": "Gromark with three-term rules and the bases 16 to 26 that experiment 28 left alive",
    "family": "5-gromark-lfsr",
    "parent": "0028-gromark-small-bases-two-to-nine",
    "changed": "Rules with three terms, k[i] = k[i-a] + k[i-b] + k[i-c], alongside the two-term rules, lags up to 13; bases 16 to 26 only, since experiment 28 showed every alphabet triple forces a shift of 15 or more, which kills every smaller base before any rule is checked.",
    "hypothesis_expert": (
        "Experiments 13 and 28 killed two-term lagged-Fibonacci rules up to lag 12 in bases 10 and 26, and "
        "every base up to 15 outright, under the 248-alphabet pool. Bean (knowledge/05-attacks.md) names "
        "other expansion rules as untested. Here: two-term rules with lags up to 13 and three-term rules "
        "k[i] = k[i-a] + k[i-b] + k[i-c] with c < b < a <= 13, bases 16 to 26, under the same pool and three "
        "modes. For each triple the largest forced shift fixes the admissible bases; each rule is checked on "
        "the 13 and 11 consecutive forced shifts, at least six checks required, chance below 26 to the minus "
        "six per check set. Survivors extend to a full stream, decrypt and submit. Bounds: complete for "
        "these rules and bases over the pool; free alphabets remain Bean's."
    ),
    "hypothesis_eli5": (
        "Gromark grows a long number stream from a short seed by adding earlier digits. Earlier we tried "
        "adding two earlier digits; now we also try adding three, with any spacing up to thirteen back, and "
        "we count in every base from 16 to 26, the only ones the known letters still allow. The 13 pushes in "
        "a row that EASTNORTHEAST pins down must follow the rule, or the rule is out."
    ),
    "prediction": (
        "No rule with six or more checks survives under any alphabet triple and base; zero candidates pass."
    ),
    "method": (
        "1. Build the alphabet pool: standard, KRYPTOS and the four mixings of each vocabulary word. "
        "2. For each plain alphabet, cipher alphabet and mode, compute the forced shift at each of the 24 "
        "crib positions. 3. For base 10, drop any triple with a shift above 9. 4. For each lag pair (a, b) "
        "check k[i] = k[i-a] + k[i-b] mod B on both crib runs; keep triples with every check passing and at "
        "least six checks. 5. For each survivor, extend the stream over all 97 positions from the 22-34 "
        "window, confirm it reproduces 64-74, decrypt and submit."
    ),
    "walkthrough": (
        "1. Take the standard alphabet for the plaintext and the KRYPTOS alphabet for the ciphertext, "
        "Vigenere. 2. Position 22: plaintext E is index 4 in the standard alphabet; ciphertext F is index 11 "
        "in KRYPTOS; the shift is 11 - 4 = 7. 3. Position 23: A is 0, L is 18; shift 18. 4. Continue to "
        "position 34 for 13 shifts in a row. 5. Try the Gromark rule, a = 5, b = 4: the sixth shift must "
        "equal the first plus the second, mod 10, and all shifts must be digits. The shift 18 already fails "
        "base 10. 6. In base 26, check the sixth against the first plus the second mod 26, the seventh "
        "against the second plus the third, and so on: eight checks. 7. One failure kills the rule under "
        "this alphabet pair; try the next pair."
    ),
}

from kryptos.alphabets import keyword_mixed, columnar_mixed, keyed_columnar_mixed, alternate_vertical_mixed
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
RUNS = [(22, 34), (64, 74)]
MODES = {"vig": lambda p, c: (c - p) % 26, "beau": lambda p, c: (c + p) % 26, "varbeau": lambda p, c: (p - c) % 26}
ENC = {"vig": lambda p, k: (p + k) % 26, "beau": lambda p, k: (k - p) % 26, "varbeau": lambda p, k: (p - k) % 26}
MIX = {"keyword": keyword_mixed, "columnar": columnar_mixed, "keyed_columnar": keyed_columnar_mixed, "alt_vertical": alternate_vertical_mixed}
MIN_CHECKS = 6


def stream_from_window(window, start, rule, base):
    """Extend k[i] = sum of k[i - lag] over the rule's lags, mod base, backward and forward."""
    a = rule[0]
    k = {start + j: v for j, v in enumerate(window)}
    lo, hi = start, start + len(window) - 1
    while hi + 1 < N:
        i = hi + 1
        k[i] = sum(k[i - lag] for lag in rule) % base
        hi = i
    while lo - 1 >= 0:
        i = lo - 1
        # k[i+a] = k[i] + sum over the other lags of k[i+a-lag]  =>  solve for k[i]
        k[i] = (k[i + a] - sum(k[i + a - lag] for lag in rule[1:])) % base
        lo = i
    return [k[i] for i in range(N)]


def encrypt(plaintext, key):
    pa, ca, m, rule, base, primer = key["pa"], key["ca"], key["m"], key["rule"], key["base"], key["primer"]
    k = list(primer)
    while len(k) < N:
        k.append(sum(k[-lag] for lag in rule) % base)
    return "".join(ca[ENC[m](pa.index(p), k[i])] for i, p in enumerate(plaintext))


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    vocab = [w for w in ctx.vocabulary if len(set(w)) >= 3]
    pool = {"std": STD, "kry": KRY}
    for w in vocab:
        for mname, fn in MIX.items():
            pool[f"{w}/{mname}"] = fn(w)
    seen, dedup = {}, {}
    for name, A in pool.items():
        if A not in seen:
            seen[A] = name; dedup[name] = A
    pool = dedup
    index = {name: {ch: i for i, ch in enumerate(A)} for name, A in pool.items()}
    crib = [[(known[pos], ct[pos - 1]) for pos in range(lo, hi + 1)] for lo, hi in RUNS]
    rules = [(a, b) for a in range(2, 14) for b in range(1, a)] + [(a, b, c) for a in range(3, 14) for b in range(2, a) for c in range(1, b)]
    survivors = []
    candidates = []
    n_triples = 0
    digit_ok = 0
    for pname, pa in pool.items():
        pidx = index[pname]
        for cname, ca in pool.items():
            cidx = index[cname]
            for m, f in MODES.items():
                n_triples += 1
                shifts = [[f(pidx[p], cidx[c]) for p, c in pairs] for pairs in crib]
                biggest = max(s for run_ in shifts for s in run_)
                digit_ok += biggest < 16
                for base in range(max(16, biggest + 1), 27):
                    for rule in rules:
                        a = rule[0]
                        checks = 0; ok = True
                        for run_ in shifts:
                            for i in range(a, len(run_)):
                                checks += 1
                                if run_[i] != sum(run_[i - lag] for lag in rule) % base:
                                    ok = False; break
                            if not ok:
                                break
                        if ok and checks >= MIN_CHECKS:
                            stream = stream_from_window(shifts[0], RUNS[0][0] - 1, rule, base)
                            second_ok = all(stream[RUNS[1][0] - 1 + j] == v for j, v in enumerate(shifts[1]))
                            survivors.append({"plain": pname, "cipher": cname, "mode": m, "base": base, "rule": list(rule),
                                              "checks": checks, "stream_matches_second_run": second_ok})
                            if second_ok:
                                pt = "".join(pa[MODES_DEC(m)(cidx[c], stream[i])] for i, c in enumerate(ct))
                                key = {"pa": pa, "ca": ca, "m": m, "rule": list(rule), "base": base, "primer": stream[:a]}
                                candidates.append({"plaintext": pt, "key": key, "key_bits": a * 4.7 + 10,
                                                   "key_description": f"Gromark-style rule {list(rule)} base {base}, primer {stream[:a]}; plain {pname}, cipher {cname}, {m}"})
        if ctx.time_left() < 20:
            break
    return {
        "candidates": candidates[:50],
        "bounds": {"family": "running numerical key, k[i] = k[i-a] + k[i-b] mod base", "rules": f"{len(rules)} two- and three-term rules with lags up to 13",
                   "bases": "16-26 as each triple allows", "alphabets": len(pool), "alphabet_triples": n_triples, "modes": 3,
                   "triples_with_all_shifts_below_16": digit_ok, "min_checks": MIN_CHECKS,
                   "survivors": survivors[:40], "n_survivors": len(survivors),
                   "n_survivors_consistent_with_second_run": sum(1 for s in survivors if s["stream_matches_second_run"])},
        "notes": f"{n_triples} alphabet triples x {len(rules)} rules, bases 16-26. {len(survivors)} survivors with >= {MIN_CHECKS} checks; {len(candidates)} full-stream candidates submitted.",
    }


def MODES_DEC(m):
    return {"vig": lambda c, k: (c - k) % 26, "beau": lambda c, k: (k - c) % 26, "varbeau": lambda c, k: (c + k) % 26}[m]


def worked_example(ctx, key):
    pa, ca = STD, KRY
    lines = ["plain alphabet standard, cipher alphabet KRYPTOS, Vigenere: forced shifts at 22-34", "", "pos  plain  cipher  shift"]
    shifts = []
    for pos in range(22, 35):
        p, c = ctx.KNOWN[pos], ctx.K4[pos - 1]
        s = (ca.index(c) - pa.index(p)) % 26; shifts.append(s)
        lines.append(f"{pos:>3}    {p}      {c}      {s:>2}")
    lines.append("")
    lines.append("shifts: " + " ".join(map(str, shifts)))
    lines.append(f"three-term rule lags 5, 3, 1 in base 26: shift 6 should equal shifts 1 + 3 + 5 = {(shifts[0] + shifts[2] + shifts[4]) % 26}, it is {shifts[5]}")
    return "\n".join(lines)
