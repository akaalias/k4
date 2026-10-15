"""Experiment 0027. See program.md for the contract."""

EXPERIMENT = {
    "slug": "simulator-round-two-width-21-hunt",
    "title": "Simulator, round two: which constructions reproduce the width-21 repeats, the width-7 doublet column and the closeness together?",
    "family": "7-construction-simulation",
    "parent": "0018-construction-simulator-fingerprint",
    "changed": "Generators chosen to share a key letter 21 or 7 positions apart: periodic systems at periods 7, 21 and 42 with free alphabets or the tableau, autokey at lag 21, progressive keys at period 21, Gromark with an even base, and transposition last at width 21. 5,000 samples each; the three unexplained statistics are the target.",
    "hypothesis_expert": (
        "0018 left three statistics unexplained by every generator: five of six doublets in one column at "
        "width 7, eleven vertical bigram repeats at width 21, and Bean's closeness of crib plaintext to "
        "ciphertext (knowledge/04-structure.md). Positions 21 apart that share a substitution alphabet make "
        "vertical pairs at width 21 repeat at English rather than flat rates, so periodic systems with period "
        "dividing 21 or 42, Gromark with an even base and a five-digit primer (Rogot, Deavours, Blackman), "
        "and autokey at lag 21 are the natural suspects; period 7 died under every alphabet (R and C both "
        "to P at 66 and 73), period 21 with vocabulary alphabets died in 0020, but a period-21 system with "
        "free alphabets did not. Each generator is scored as in 0018 on the three target statistics and the "
        "ten of 0018, with two-sided empirical p-values. A generator that gives all three targets p above "
        "0.05 is a lead for a family. Bounds: 5,000 samples per generator; a ranking, not a verdict."
    ),
    "hypothesis_eli5": (
        "Yesterday's workshop found three things about K4 that none of our fake K4s reproduced, all to do "
        "with letters 7 or 21 places apart behaving alike. So today we build fakes with methods that treat "
        "letters 7, 21 or 42 places apart alike: a secret word of that length, a number stream with that "
        "rhythm, a message keyed by itself 21 letters back. Then we measure the fakes the same way and ask "
        "which method makes all three oddities look ordinary."
    ),
    "prediction": (
        "Periodic systems at period 21 and 42 with free alphabets reproduce the width-21 repeats (p above "
        "0.2) but not the width-7 doublet column. No generator makes all three targets ordinary at once; "
        "the width-7 column stays below p 0.02 everywhere."
    ),
    "method": (
        "1. Keep the ten statistics of 0018. 2. Build the eleven generators. 3. Draw 5,000 samples each. "
        "4. Report p-values for the three targets and the combined distance; rank."
    ),
    "walkthrough": (
        "1. Take an English sentence of 97 letters and a key of 21 random letters repeated under it. 2. "
        "Encipher on the sculpture's table. 3. Write the result in rows of 21 and count how many vertical "
        "pairs, a letter and the one below it, occur twice or more; K4 has eleven. 4. Do this 5,000 times "
        "and see how often eleven or more appears. 5. Count the doublets and note which column of a width-7 "
        "layout they fall in; K4 has five of six in one column. 6. Repeat for the other methods."
    ),
}

import random
from collections import Counter
from kryptos.alphabets import encrypt_letter
from kryptos.ciphers import columnar_transposition_encrypt
from kryptos.facts import load_k1, load_k2, load_k3, STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
SAMPLES = 5000


def letters(s):
    return "".join(c for c in s if "A" <= c <= "Z")


def encrypt(plaintext, key):
    raise NotImplementedError("diagnostic experiment: no candidate is submitted")


# ---- statistics ---------------------------------------------------------------------
def stats(ct, pt, crib_positions):
    c = Counter(ct)
    ic = sum(v * (v - 1) for v in c.values()) / (N * (N - 1))
    doublets = [i for i in range(N - 1) if ct[i] == ct[i + 1]]
    col7 = max(Counter(i % 7 for i in doublets).values()) if doublets else 0
    v21 = [ct[i] + ct[i + 21] for i in range(N - 21)]
    rep21 = len(v21) - len(set(v21))
    h = [ct[i] + ct[i + 1] for i in range(N - 1)]
    rep_bigrams = len(h) - len(set(h))
    close = sum(min((STD.index(pt[i - 1]) - STD.index(ct[i - 1])) % 26, (STD.index(ct[i - 1]) - STD.index(pt[i - 1])) % 26) for i in crib_positions) / len(crib_positions)
    same = sum(1 for i in crib_positions if pt[i - 1] == ct[i - 1])
    return {"ic": ic, "distinct": len(c), "doublets": len(doublets), "width7_doublet_column": col7,
            "width21_vertical_repeats": rep21, "repeated_bigrams": rep_bigrams, "top_count": max(c.values()),
            "singletons": sum(1 for v in c.values() if v == 1), "closeness_mean_distance": close, "self_encryptions": same}


# ---- generators ---------------------------------------------------------------------
def gen_plaintext(rng, texts):
    t = "".join(texts)
    i = rng.randrange(0, len(t) - N + 1)
    return t[i:i + N]


def vig(pt, key, pa="kry", ca="kry", ka="kry", m="vig"):
    return "".join(encrypt_letter(p, key[i % len(key)], pa, ca, ka, m) for i, p in enumerate(pt))


def rand_key(rng, n):
    return "".join(rng.choice(STD) for _ in range(n))


def mixed(rng):
    a = list(STD); rng.shuffle(a); return "".join(a)


def g_vig_kry(rng, pt):
    return vig(pt, rand_key(rng, rng.randint(27, 30)))


def g_quagmire(rng, pt):
    pa, ca = mixed(rng), mixed(rng); key = rand_key(rng, rng.randint(27, 30))
    return "".join(ca[(pa.index(p) + STD.index(key[i % len(key)])) % 26] for i, p in enumerate(pt))


def g_progressive(rng, pt):
    P, d = rng.randint(7, 13), rng.randint(1, 25); key = rand_key(rng, P)
    return "".join(KRY[(KRY.index(p) + KRY.index(key[i % P]) + d * (i // P)) % 26] for i, p in enumerate(pt))


def g_autokey(rng, pt):
    L = rng.randint(1, 30); primer = rand_key(rng, L)
    return "".join(KRY[(KRY.index(p) + KRY.index(primer[i] if i < L else pt[i - L])) % 26] for i, p in enumerate(pt))


def g_running(rng, pt, texts):
    key = gen_plaintext(rng, texts)
    return vig(pt, key)


def g_columnar_then_vig(rng, pt):
    w = rng.randint(2, 30); order = list(range(w)); rng.shuffle(order)
    return vig(columnar_transposition_encrypt(pt, order), rand_key(rng, rng.randint(27, 30)))


def g_vig_then_columnar(rng, pt):
    w = rng.randint(2, 30); order = list(range(w)); rng.shuffle(order)
    return columnar_transposition_encrypt(vig(pt, rand_key(rng, rng.randint(27, 30))), order)


def det2(M):
    return (M[0][0] * M[1][1] - M[0][1] * M[1][0]) % 26


def det3(M):
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0]) + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0])) % 26


def g_hill(n):
    def g(rng, pt):
        while True:
            M = [[rng.randrange(26) for _ in range(n)] for _ in range(n)]
            d = det2(M) if n == 2 else det3(M)
            if d % 2 and d % 13:
                break
        out = list(pt)
        for i in range(0, N - n + 1, n):
            blk = [STD.index(pt[i + j]) for j in range(n)]
            for r in range(n):
                out[i + r] = STD[sum(M[r][k] * blk[k] for k in range(n)) % 26]
        return "".join(out)
    return g


def g_gromark(rng, pt):
    k = [rng.randrange(10) for _ in range(5)]
    while len(k) < N:
        k.append((k[-5] + k[-4]) % 10)
    ca = mixed(rng)
    return "".join(ca[(STD.index(p) + k[i]) % 26] for i, p in enumerate(pt))


def g_random(rng, pt):
    return rand_key(rng, N)


def g_transposition(rng, pt):
    w = rng.randint(2, 30); order = list(range(w)); rng.shuffle(order)
    return columnar_transposition_encrypt(pt, order)


def g_mono(rng, pt):
    ca = mixed(rng)
    return "".join(ca[STD.index(p)] for p in pt)


def run(ctx):
    texts = [letters(load_k1()["plaintext"]), letters(load_k2()["plaintext_as_carved"]), letters(load_k3()["plaintext"])]
    crib_positions = sorted(ctx.KNOWN)
    k4_pt = "".join(ctx.KNOWN.get(i, "A") for i in range(1, N + 1))   # only crib positions are used for plaintext statistics
    k4 = stats(ctx.K4, k4_pt, crib_positions)
    rng = random.Random(2026)
    def free_periodic(P):
        def g(rng, pt):
            alphas = [mixed(rng) for _ in range(P)]
            return "".join(alphas[i % P][STD.index(p)] for i, p in enumerate(pt))
        return g

    def vig_period(P):
        return lambda rng, pt: vig(pt, rand_key(rng, P))

    def autokey_lag(L):
        def g(rng, pt):
            primer = rand_key(rng, L)
            return "".join(KRY[(KRY.index(p) + KRY.index(primer[i] if i < L else pt[i - L])) % 26] for i, p in enumerate(pt))
        return g

    def progressive(P):
        def g(rng, pt):
            d = rng.randint(1, 25); key = rand_key(rng, P)
            return "".join(KRY[(KRY.index(p) + KRY.index(key[i % P]) + d * (i // P)) % 26] for i, p in enumerate(pt))
        return g

    def gromark_base(B):
        def g(rng, pt):
            k = [rng.randrange(B) for _ in range(5)]
            while len(k) < N:
                k.append((k[-5] + k[-4]) % B)
            ca = mixed(rng)
            return "".join(ca[(STD.index(p) + k[i]) % 26] for i, p in enumerate(pt))
        return g

    def vig_then_columnar_w(w):
        def g(rng, pt):
            order = list(range(w)); rng.shuffle(order)
            return columnar_transposition_encrypt(vig(pt, rand_key(rng, rng.randint(27, 30))), order)
        return g

    gens = {
        "period 7, free alphabets": free_periodic(7),
        "period 21, free alphabets": free_periodic(21),
        "period 42, free alphabets": free_periodic(42),
        "period 21, KRYPTOS tableau": vig_period(21),
        "period 42, KRYPTOS tableau": vig_period(42),
        "autokey lag 21": autokey_lag(21),
        "autokey lag 7": autokey_lag(7),
        "progressive key, period 21": progressive(21),
        "progressive key, period 7": progressive(7),
        "Gromark base 10": gromark_base(10),
        "Gromark base 8": gromark_base(8),
        "Gromark base 2": gromark_base(2),
        "Vigenere then columnar width 21": vig_then_columnar_w(21),
        "Vigenere then columnar width 7": vig_then_columnar_w(7),
        "calibration: random letters": g_random,
        "calibration: Vigenere period 27-30": g_vig_kry,
    }
    table = {}
    for name, g in gens.items():
        samples = []
        for _ in range(SAMPLES):
            pt = gen_plaintext(rng, texts)
            samples.append(stats(g(rng, pt), pt, crib_positions))
            if ctx.time_left() < 20:
                break
        row = {}
        dist2 = 0.0
        for key, v in k4.items():
            xs = [s[key] for s in samples]
            mu = sum(xs) / len(xs); sd = (sum((x - mu) ** 2 for x in xs) / len(xs)) ** 0.5
            z = 0.0 if sd == 0 else (v - mu) / sd
            lo = sum(1 for x in xs if x <= v) / len(xs); hi = sum(1 for x in xs if x >= v) / len(xs)
            p = min(1.0, 2 * min(lo, hi))
            row[key] = {"mean": round(mu, 4), "sd": round(sd, 4), "z": round(z, 2), "p": round(p, 3)}
            dist2 += z * z
        row["_distance"] = round(dist2 ** 0.5, 2)
        row["_n"] = len(samples)
        table[name] = row
    ranking = sorted(table, key=lambda n: table[n]["_distance"])
    return {
        "candidates": [],
        "bounds": {"family": "construction simulation, round two", "samples_per_generator": SAMPLES, "statistics": list(k4),
                   "targets": {n: {k: table[n][k]["p"] for k in ("width7_doublet_column", "width21_vertical_repeats", "closeness_mean_distance")} for n in ranking},
                   "k4": {k: round(v, 4) for k, v in k4.items()},
                   "ranking_by_distance": [(n, table[n]["_distance"]) for n in ranking],
                   "table": table},
        "notes": "Diagnostic, no candidates. Target p-values (width-7 column, width-21 repeats, closeness): " + "; ".join(f"{n}: {table[n]['width7_doublet_column']['p']}, {table[n]['width21_vertical_repeats']['p']}, {table[n]['closeness_mean_distance']['p']}" for n in ranking) + ".",
    }


def worked_example(ctx, key):
    texts = [letters(load_k1()["plaintext"]), letters(load_k2()["plaintext_as_carved"]), letters(load_k3()["plaintext"])]
    rng = random.Random(1)
    pt = gen_plaintext(rng, texts); ct = "".join([mixed(rng) for _ in range(21)][i % 21][STD.index(p)] for i, p in enumerate(pt))
    k4_pt = "".join(ctx.KNOWN.get(i, "A") for i in range(1, N + 1))
    a, b = stats(ctx.K4, k4_pt, sorted(ctx.KNOWN)), stats(ct, pt, sorted(ctx.KNOWN))
    lines = ["one sample from the period-21 free-alphabet generator against K4", "", f"plain  {pt}", f"cipher {ct}", "", f"{'statistic':<28}{'K4':>10}{'sample':>10}"]
    for k in a:
        lines.append(f"{k:<28}{a[k]:>10.4f}{b[k]:>10.4f}")
    return "\n".join(lines)
