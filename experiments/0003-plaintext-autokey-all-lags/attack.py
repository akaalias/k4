"""Experiment 0003. See program.md for the contract."""

EXPERIMENT = {
    "slug": "plaintext-autokey-all-lags",
    "title": "Plaintext autokey, decided where two known letters line up",
    "family": "1-keyed-periodic",
    "parent": "0002-ciphertext-autokey-all-lags",
    "changed": "The key letter is now the plaintext letter L back, not the ciphertext letter.",
    "hypothesis_expert": (
        "K4 is a plaintext-autokey cipher: c[i] = f(p[i], p[i-L]) after a primer of length L. This "
        "is the NSA's 1992 first guess for the interval-7 property (knowledge/04-structure.md). The "
        "cribs decide it only where both p[i] and p[i-L] are known: within EASTNORTHEAST (lags 1 to "
        "12), within BERLINCLOCK (lags 1 to 10), and between the two runs (lags 30 to 52). We test "
        "all 24 conventions at every lag 1 to 96, count the checkable pairs, and record three "
        "outcomes per lag: excluded (a mismatch), consistent (all checks pass, at least one check), "
        "or undecided (no overlapping pair). For consistent lags we cannot decrypt without the "
        "primer, so we report them as open and bound the primer space. Clue register C11a."
    ),
    "hypothesis_eli5": (
        "This is the other autokey: the real message, not the scrambled one, becomes its own key "
        "after a short start. We can only test it where two of the 24 known letters sit the right "
        "distance apart, so some distances get a clear no and some get no answer at all. The "
        "point is to know exactly which distances are still alive, so no one wastes time on the "
        "dead ones."
    ),
    "prediction": "Lags 1 to 12 and 30 to 52 are excluded under every convention. Lags 13 to 29 and 53 to 96 stay undecided. No candidates pass the crib gate.",
    "method": (
        "For each convention and lag L: over crib positions i with i-L also a crib position, "
        "compare f(p[i], p[i-L]) with c[i]. Tally excluded, consistent, undecided per lag across "
        "conventions. No candidates are generated because the primer is unknown; the bounds are the "
        "deliverable."
    ),
    "walkthrough": (
        "1. Number the ciphertext 1 to 97 and mark the 24 known plaintext letters. 2. Pick a "
        "distance, say 3. 3. Position 25 is T and position 22, three back, is E. 4. Under the "
        "sculpture's alphabet, T is at 4 and E at 11; add them, 15, and read the letter there, I. "
        "5. The carved letter at 25 is V, so distance 3 fails under this convention. 6. For a "
        "distance like 20 there is no pair of known letters that far apart, so the test says nothing; "
        "that distance stays open."
    ),
}

from kryptos.alphabets import conventions, encrypt_letter


def encrypt(plaintext, key):
    pa, ca, ka, m, L, primer = key["pa"], key["ca"], key["ka"], key["m"], key["lag"], key["primer"]
    out = []
    for i, p in enumerate(plaintext):
        k = primer[i] if i < L else plaintext[i - L]
        out.append(encrypt_letter(p, k, pa, ca, ka, m))
    return "".join(out)


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    per_lag = {}
    for L in range(1, 97):
        status = {"excluded": 0, "consistent": 0, "undecided": 0}
        checks_at_lag = 0
        for conv in conventions():
            pa, ca, ka, m = conv
            checks = mism = 0
            for pos, p in known.items():
                if (pos - L) in known:
                    checks += 1
                    if encrypt_letter(p, known[pos - L], pa, ca, ka, m) != ct[pos - 1]:
                        mism += 1
            checks_at_lag = checks
            if checks == 0:
                status["undecided"] += 1
            elif mism == 0:
                status["consistent"] += 1
            else:
                status["excluded"] += 1
        per_lag[L] = {"checks": checks_at_lag, **status}
    excluded = [L for L, v in per_lag.items() if v["excluded"] == 24]
    consistent = {L: v["consistent"] for L, v in per_lag.items() if v["consistent"] > 0}
    undecided = [L for L, v in per_lag.items() if v["checks"] == 0]
    return {
        "candidates": [],
        "bounds": {"family": "plaintext autokey", "conventions": 24, "lags": "1-96",
                   "lags_excluded_all_conventions": excluded,
                   "lags_consistent_some_conventions": consistent,
                   "lags_undecided_no_overlapping_cribs": undecided},
        "notes": "No candidate can be built without the primer; this experiment exists for its bounds.",
    }


def worked_example(ctx, key):
    A = ctx.KRYPTOS_ALPHABET
    lines = ["plaintext autokey, lag 3, all alphabets KRYPTOS, Vigenere", f"alphabet: {A}", "",
             "pos  plain  key=p[pos-3]  idx(p)+idx(k)  predicted  carved"]
    for pos in (25, 26, 27, 28, 29, 30):
        p = ctx.KNOWN[pos]; k = ctx.KNOWN[pos - 3]
        n = (A.index(p) + A.index(k)) % 26
        lines.append(f"{pos:>3}    {p}      {k}            {A.index(p):>2}+{A.index(k):<2}        {A[n]}        {ctx.K4[pos-1]}  {'ok' if A[n]==ctx.K4[pos-1] else 'x'}")
    return "\n".join(lines)
