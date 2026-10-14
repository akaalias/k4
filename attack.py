"""Experiment 0018. See program.md for the contract."""

EXPERIMENT = {
    "slug": "construction-simulator-fingerprint",
    "title": "Construction simulator: which cipher families produce texts with K4's statistical fingerprint?",
    "family": "7-construction-simulation",
    "parent": None,
    "changed": "New root in family 7. Not a solver: fourteen generators encrypt English windows with random keys, and K4's statistics are placed in each family's distribution.",
    "hypothesis_expert": (
        "Oranchak, Blake and Van Eycke solved Zodiac 340 by simulating constructions until one reproduced "
        "the ciphertext's fingerprint (knowledge/07-people.md). K4's fingerprint (knowledge/04-structure.md): "
        "index of coincidence 0.0361; all 26 letters present; six doublets, five of them in one column at "
        "width 7; eleven repeated vertical bigrams at width 21; top frequency 8; and Bean's closeness, the "
        "crib plaintext letters sitting near their ciphertext letters on the standard alphabet. Each "
        "generator takes a random 97-letter window of the K1-K3 plaintexts and a random key: periodic "
        "Vigenere on the KRYPTOS alphabet at periods 27-30, Quagmire with random alphabets, progressive "
        "key, plaintext autokey, running key, columnar then Vigenere, Vigenere then columnar, Hill 2x2 and "
        "3x3, Gromark base 10, plus three calibration generators (random letters, pure transposition, "
        "monoalphabetic). For each statistic and generator we record the two-sided empirical p-value of "
        "K4's value and a combined distance. The result ranks families by plausibility; it decides none. "
        "Bounds: 5,000 samples per generator, these twelve statistics."
    ),
    "hypothesis_eli5": (
        "Instead of trying to break the message, we build a workshop. We take ordinary English text, "
        "scramble it with each kind of cipher we suspect, using random keys, thousands of times, and "
        "measure the results: how evenly the letters are spread, how often a letter repeats its "
        "neighbour, how letters line up in columns. Then we ask which kind of cipher most often produces "
        "text that measures like K4. The method that solved another famous cipher, the Zodiac killer's, "
        "worked this way. It will not tell us the message, but it tells us where to dig."
    ),
    "prediction": (
        "K4's flat letter distribution sits comfortably inside every polyalphabetic family and outside "
        "the monoalphabetic and pure-transposition calibrations. The width-7 doublet column and the "
        "width-21 repeats are unusual under every generator, with p-values near 0.01 to 0.1, so no "
        "family is singled out by them. Bean's closeness statistic separates families: letter-for-letter "
        "systems on a near-standard alphabet reproduce it more often than transposed or Hill systems."
    ),
    "method": (
        "1. Define the statistics on a 97-letter text, with the plaintext available for the closeness "
        "statistic at the 24 crib positions. 2. Build fourteen generators. 3. Draw 5,000 samples each. "
        "4. For each statistic, compute K4's two-sided empirical p-value under each generator and a z-score. "
        "5. Combine the z-scores into a distance and rank the generators."
    ),
    "walkthrough": (
        "1. Count each letter in K4: K appears 8 times, M and Y once. 2. The index of coincidence is the "
        "chance two letters drawn at random match: add n(n-1) over the 26 counts and divide by 97 times 96; "
        "K4 gives 0.0361. 3. Now take an English sentence of 97 letters and encipher it with a repeating "
        "key of 28 random letters on the sculpture's table. 4. Count its letters the same way and compute "
        "its index. 5. Do this 5,000 times and see where 0.0361 falls among the results. 6. Repeat for the "
        "other statistics and the other ciphers. 7. A cipher that rarely produces K4's numbers is unlikely; "
        "one that often does stays on the list."
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
    gens = {
        "periodic Vigenere, KRYPTOS alphabet, period 27-30": g_vig_kry,
        "Quagmire, random alphabets, period 27-30": g_quagmire,
        "progressive key, period 7-13": g_progressive,
        "plaintext autokey, lag 1-30": g_autokey,
        "running key from K1-K3 English": lambda r, p: g_running(r, p, texts),
        "columnar transposition then Vigenere": g_columnar_then_vig,
        "Vigenere then columnar transposition": g_vig_then_columnar,
        "Hill 2x2": g_hill(2),
        "Hill 3x3": g_hill(3),
        "Gromark base 10, random cipher alphabet": g_gromark,
        "calibration: random letters": g_random,
        "calibration: pure columnar transposition": g_transposition,
        "calibration: monoalphabetic": g_mono,
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
        "bounds": {"family": "construction simulation", "samples_per_generator": SAMPLES, "statistics": list(k4),
                   "k4": {k: round(v, 4) for k, v in k4.items()},
                   "ranking_by_distance": [(n, table[n]["_distance"]) for n in ranking],
                   "table": table},
        "notes": "Diagnostic, no candidates. Ranking nearest first: " + "; ".join(f"{n} ({table[n]['_distance']})" for n in ranking[:5]) + ".",
    }


def worked_example(ctx, key):
    texts = [letters(load_k1()["plaintext"]), letters(load_k2()["plaintext_as_carved"]), letters(load_k3()["plaintext"])]
    rng = random.Random(1)
    pt = gen_plaintext(rng, texts); ct = g_vig_kry(rng, pt)
    k4_pt = "".join(ctx.KNOWN.get(i, "A") for i in range(1, N + 1))
    a, b = stats(ctx.K4, k4_pt, sorted(ctx.KNOWN)), stats(ct, pt, sorted(ctx.KNOWN))
    lines = ["one sample from the periodic-Vigenere generator against K4", "", f"plain  {pt}", f"cipher {ct}", "", f"{'statistic':<28}{'K4':>10}{'sample':>10}"]
    for k in a:
        lines.append(f"{k:<28}{a[k]:>10.4f}{b[k]:>10.4f}")
    return "\n".join(lines)
