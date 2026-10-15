"""Experiment 0028. See program.md for the contract."""

EXPERIMENT = {
    "slug": "gromark-small-bases-two-to-nine",
    "title": "Gromark in bases 2 to 9: the even bases that reproduce the width-21 repeats",
    "family": "5-gromark-lfsr",
    "parent": "0013-gromark-recurrence-on-crib-shifts",
    "changed": "Bases 2 to 9 instead of 10 and 26. 0027 showed Gromark base 2 is the only simulated construction that reproduces K4's width-21 repeats, and Bean found base-8 primers that fit the cribs. Every forced shift must now be below the base, a filter of (base/26) to the 24th power per alphabet triple.",
    "hypothesis_expert": (
        "Rogot, Deavours and Blackman: a Gromark key in an even base with a five-digit primer has an "
        "underlying period-21 structure, and Bean found base-8 primers that fit the cribs with period 84 "
        "(knowledge/04-structure.md, 05-attacks.md). 0027 confirmed that base 2 reproduces the width-21 "
        "repeats (p 0.34) where nothing else does. 0013 tested bases 10 and 26 only. Here the bases are 2 "
        "to 9, every lag pair 1 <= b < a <= 12, under the same 248-alphabet pool for plain and cipher and "
        "three modes. In base B every one of the 24 forced shifts must be below B, which alone has chance "
        "(B/26)^24 per triple, from 10^-27 at base 2 to 10^-11 at base 9; a triple passing that and six "
        "recurrence checks would be decisive. For each survivor the recurrence runs from the 22-34 window "
        "to a full key stream, the text is decrypted and submitted. Bounds: complete for these bases, "
        "rules and alphabets; Bean's free annealed alphabets remain his."
    ),
    "hypothesis_eli5": (
        "Yesterday's workshop found one kind of fake that shares a real oddity of K4: a Gromark cipher "
        "whose growing number stream uses only the digits 0 and 1. Such streams repeat their rhythm every "
        "21 letters, which is just what K4 shows. A Gromark in base 2 pushes each letter along by 0 or 1 "
        "only; in base 8, by 0 to 7. We already know the 24 pushes that the known letters demand under "
        "each alphabet, so we simply check whether any alphabet keeps all 24 pushes small enough, and then "
        "whether they follow the adding rule."
    ),
    "prediction": (
        "No alphabet triple keeps all 24 forced shifts below 9, let alone below 2, so no base from 2 to 9 "
        "reaches the recurrence test. Zero candidates pass."
    ),
    "method": (
        "1. Build the alphabet pool. 2. For each plain alphabet, cipher alphabet and mode, compute the "
        "forced shift at each of the 24 crib positions and record the largest. 3. For each base B from 2 "
        "to 9, keep triples whose largest shift is below B. 4. For those, check every lag pair's recurrence "
        "on both crib runs. 5. Extend survivors to a full stream, decrypt and submit."
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
    smallest_max = 99
    for pname, pa in pool.items():
        pidx = index[pname]
        for cname, ca in pool.items():
            cidx = index[cname]
            for m, f in MODES.items():
                n_triples += 1
                shifts = [[f(pidx[p], cidx[c]) for p, c in pairs] for pairs in crib]
                all_digits = all(s <= 8 for run_ in shifts for s in run_)
                digit_ok += all_digits
                smallest_max = min(smallest_max, max(s for run_ in shifts for s in run_))
                biggest = max(s for run_ in shifts for s in run_)
                for base in range(2, 10):
                    if biggest >= base:
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
                   "bases": list(range(2, 10)), "smallest_largest_shift_over_all_triples": smallest_max, "alphabets": len(pool), "alphabet_triples": n_triples, "modes": 3,
                   "triples_with_all_shifts_below_9": digit_ok, "min_checks": MIN_CHECKS,
                   "survivors": survivors[:40], "n_survivors": len(survivors),
                   "n_survivors_consistent_with_second_run": sum(1 for s in survivors if s["stream_matches_second_run"])},
        "notes": f"{n_triples} alphabet triples; smallest largest-shift over all triples {smallest_max}; bases 2-9 x {len(rules)} rules. {len(survivors)} survivors with >= {MIN_CHECKS} checks; {len(candidates)} full-stream candidates submitted.",
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
    lines.append(f"largest shift {max(shifts)}: base 8 needs all below 8, so this alphabet pair is out at once")
    return "\n".join(lines)
