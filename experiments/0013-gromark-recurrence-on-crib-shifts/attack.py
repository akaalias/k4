"""Experiment 0013. See program.md for the contract."""

EXPERIMENT = {
    "slug": "gromark-recurrence-on-crib-shifts",
    "title": "Gromark and its cousins: must the 13 known shifts in a row obey a lagged-Fibonacci rule?",
    "family": "5-gromark-lfsr",
    "parent": None,
    "changed": "New root in family 5. The key is a running number stream from a short primer, as in the ACA Gromark; the cribs give 13 consecutive key values, which a recurrence must reproduce.",
    "hypothesis_expert": (
        "Gromark (Gillogly 1999, 2004; Bean, HistoCrypt 2021, knowledge/05-attacks.md): a primer of a digits "
        "expands by k[i] = k[i-a] + k[i-b] mod B, and each plaintext letter shifts by k[i] between a plain "
        "and a cipher alphabet. Bean exhausted base 10 with a = 5, b = 4 under free annealed alphabets. "
        "Here the rule is the variable: every lag pair 1 <= b < a <= 12 and bases 10 and 26, under plain "
        "and cipher alphabets drawn from the standard, KRYPTOS and the four Friedman mixings of every "
        "vocabulary word, with the three tableau modes. Positions 22-34 force 13 consecutive shifts and "
        "64-74 force 11; the recurrence is checked on both runs, giving 24 - 2a checks per rule. In base 10 "
        "every forced shift must also be a digit. A survivor with at least six passing checks has chance "
        "probability below 26 to the minus six per trial; with about 700,000 trials per rule, chance "
        "survivors should be rare. For each survivor the recurrence runs backward and forward from the "
        "22-34 window to a full key stream, the text is decrypted and submitted. Bounds: complete for the "
        "stated rules, bases and alphabet pools; free alphabets outside the vocabulary remain Bean's."
    ),
    "hypothesis_eli5": (
        "Gromark is a cipher where the secret is a short number, say five digits, that grows into a long "
        "stream of digits by adding pairs of earlier digits, like a Fibonacci sequence. Each letter of the "
        "message is pushed along the alphabet by the next digit. The 13 known letters of EASTNORTHEAST "
        "tell us 13 pushes in a row, and in a Fibonacci-style stream each push must equal the sum of two "
        "earlier ones. We test every pair of positions the rule might add, in base 10 and in base 26, and "
        "with every alphabet the puzzle's words can build. A rule that fits the known pushes would be found "
        "out at once."
    ),
    "prediction": (
        "In base 10 almost no alphabet pair makes all 24 forced shifts digits, and none of those also "
        "satisfies a recurrence. In base 26, a handful of (rule, alphabet) survivors appear at the long "
        "lags where only a few checks apply, none with six or more checks. No decrypted candidate is "
        "English; zero pass."
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


def stream_from_window(window, start, a, b, base):
    """Given key values at positions start..start+len(window)-1 (0-indexed), extend the recurrence
    k[i] = k[i-a] + k[i-b] mod base backward and forward over 0..N-1."""
    k = {start + j: v for j, v in enumerate(window)}
    lo, hi = start, start + len(window) - 1
    while hi + 1 < N:
        i = hi + 1
        k[i] = (k[i - a] + k[i - b]) % base
        hi = i
    while lo - 1 >= 0:
        i = lo - 1
        # k[i+a] = k[i] + k[i+a-b]  =>  k[i] = k[i+a] - k[i+a-b]
        k[i] = (k[i + a] - k[i + a - b]) % base
        lo = i
    return [k[i] for i in range(N)]


def encrypt(plaintext, key):
    pa, ca, m, a, b, base, primer = key["pa"], key["ca"], key["m"], key["a"], key["b"], key["base"], key["primer"]
    k = list(primer)
    while len(k) < N:
        k.append((k[-a] + k[-b]) % base)
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
    rules = [(a, b) for a in range(2, 13) for b in range(1, a)]
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
                all_digits = all(s <= 9 for run_ in shifts for s in run_)
                digit_ok += all_digits
                for base in (10, 26):
                    if base == 10 and not all_digits:
                        continue
                    for a, b in rules:
                        checks = 0; ok = True
                        for run_ in shifts:
                            for i in range(a, len(run_)):
                                checks += 1
                                if run_[i] != (run_[i - a] + run_[i - b]) % base:
                                    ok = False; break
                            if not ok:
                                break
                        if ok and checks >= MIN_CHECKS:
                            stream = stream_from_window(shifts[0], RUNS[0][0] - 1, a, b, base)
                            second_ok = all(stream[RUNS[1][0] - 1 + j] == v for j, v in enumerate(shifts[1]))
                            survivors.append({"plain": pname, "cipher": cname, "mode": m, "base": base, "a": a, "b": b,
                                              "checks": checks, "stream_matches_second_run": second_ok})
                            if second_ok:
                                pt = "".join(pa[MODES_DEC(m)(cidx[c], stream[i])] for i, c in enumerate(ct))
                                key = {"pa": pa, "ca": ca, "m": m, "a": a, "b": b, "base": base, "primer": stream[:a]}
                                candidates.append({"plaintext": pt, "key": key, "key_bits": a * (3.33 if base == 10 else 4.7) + 10,
                                                   "key_description": f"Gromark-style a={a} b={b} base {base}, primer {stream[:a]}; plain {pname}, cipher {cname}, {m}"})
        if ctx.time_left() < 20:
            break
    return {
        "candidates": candidates[:50],
        "bounds": {"family": "running numerical key, k[i] = k[i-a] + k[i-b] mod base", "rules": f"{len(rules)} lag pairs, 1 <= b < a <= 12",
                   "bases": [10, 26], "alphabets": len(pool), "alphabet_triples": n_triples, "modes": 3,
                   "base10_all_digit_triples": digit_ok, "min_checks": MIN_CHECKS,
                   "survivors": survivors[:40], "n_survivors": len(survivors),
                   "n_survivors_consistent_with_second_run": sum(1 for s in survivors if s["stream_matches_second_run"])},
        "notes": f"{n_triples} alphabet triples x {len(rules)} rules x 2 bases. {len(survivors)} survivors with >= {MIN_CHECKS} checks; {len(candidates)} full-stream candidates submitted.",
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
    lines.append(f"Gromark rule a=5 b=4 base 10: all digits? {all(s <= 9 for s in shifts)}; base 26 check at i=5: {shifts[5]} vs {(shifts[0] + shifts[1]) % 26}")
    return "\n".join(lines)
