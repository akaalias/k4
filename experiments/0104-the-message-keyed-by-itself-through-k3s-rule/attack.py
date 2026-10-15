"""Experiment 0104. See program.md for the contract."""

EXPERIMENT = {
    "slug": "the-message-keyed-by-itself-through-k3s-rule",
    "title": "The message as its own key, read through K3's counting rule: key letter for place i is the message letter at a + b i mod 97",
    "family": "1-keyed-periodic",
    "parent": "0003-plaintext-autokey-chained",
    "changed": "0003 chained plaintext autokey, where the key for place i is the message letter a fixed distance back. Here the key is the message letter at a + b i mod 97 for every a and b, K3's counting rule, the mirror (b = -1) included. Because the rule is a permutation of the 97 places, each known letter fixes every letter of its cycle, so the test is exact and, where it passes, it decrypts.",
    "hypothesis_expert": (
        "Companion to 0103 (the copper keyed by itself). Model: c_i = E(p_i, p_{f(i)}), f(i) = a + b i mod 97, b = 1-96 "
        "(97 is prime, so f is a permutation), a = 0-96, f without fixed points among the known places; E in 8 classes "
        "(plain and cipher alphabets standard or KRYPTOS; Vigenere, Beaufort; key letters numbered on the plain "
        "alphabet), plus variant Beaufort via the sign. Propagation: if p_i is known, p_{f(i)} = the key that turns p_i into "
        "c_i; if p_{f(i)} is known, p_i = D(c_i, p_{f(i)}). Each cycle of f containing a known place is fixed completely; a "
        "contradiction with another known letter on the same cycle kills the setting. Survivors are decrypted on every "
        "fixed place and scored. C6, C13 ('mirrors'). Ten shuffled coppers."
    ),
    "hypothesis_eli5": (
        "Here the message is its own key: to encrypt a letter, you add another letter of the message, picked by K3's "
        "counting rule. Because that rule visits places in a loop, one known letter gives the next one in its loop, and "
        "so on all the way round, until the loop comes back to another known letter. If the two disagree, the setting "
        "is impossible. We try every start, step and table rule."
    ),
    "prediction": (
        "No setting survives where a cycle carries two or more known letters; the survivors, if any, are settings whose "
        "cycles each hold one known letter, as often on the coppers, and they decrypt to noise. Zero candidates."
    ),
    "method": (
        "1. For each a, b and class, follow the cycles of f from the known places, filling message letters forward and "
        "backward. 2. Stop at the first contradiction. 3. Count surviving settings and their checks on K4 and ten "
        "shuffled coppers. 4. Decrypt survivors on every fixed place and score them as English."
    ),
    "walkthrough": (
        "1. Choose a = 0, b = 96: place i takes its key from the message letter at place 99 - i. "
        "2. Place 22 is E, carved F: so E plus the key at place 77 gives F, and the message letter at 77 is F minus E. "
        "3. Place 77 in turn takes its key from place 22, which closes the loop: check that it agrees. "
        "4. Longer loops run through many places; a loop with two known letters is a check. "
        "5. Try every start, step and table rule."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
ALPH = {"std": STD, "kry": KRY}
N_CONTROLS = 10


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    places = sorted(known)
    rng = random.Random(104)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    T = len(texts)
    rules = [(pa, ca, mode) for pa in ALPH for ca in ALPH for mode in ("vig", "beau", "var")]
    surv = [0] * T
    checks_hist = [dict() for _ in T * [None]]
    k4_surv = []
    n = 0
    score = ctx.english_score if hasattr(ctx, "english_score") else None
    for b in range(1, N):
        for a in range(N):
            f = [(a + b * i) % N for i in range(N)]
            if any(f[q - 1] == q - 1 for q in places):
                continue
            n += 1
            finv = [0] * N
            for i, j in enumerate(f):
                finv[j] = i
            for pa, ca, mode in rules:
                PI = {c: i for i, c in enumerate(ALPH[pa])}; CI = {c: i for i, c in enumerate(ALPH[ca])}
                for t in range(T):
                    C = [CI[x] for x in texts[t]]
                    p = [None] * N
                    for q in places:
                        p[q - 1] = PI[known[q]]
                    ok, checks = True, 0
                    stack = [q - 1 for q in places]
                    while stack and ok:
                        i = stack.pop()
                        # forward: key for i is p[f(i)]
                        j = f[i]
                        k = {"vig": (C[i] - p[i]) % 26, "beau": (C[i] + p[i]) % 26, "var": (p[i] - C[i]) % 26}[mode]
                        if p[j] is None:
                            p[j] = k; stack.append(j)
                        elif p[j] != k:
                            ok = False
                        else:
                            checks += 1
                        # backward: place h with f(h) = i uses p[i] as its key
                        h = finv[i]
                        v = {"vig": (C[h] - p[i]) % 26, "beau": (p[i] - C[h]) % 26, "var": (C[h] + p[i]) % 26}[mode]
                        if p[h] is None:
                            p[h] = v; stack.append(h)
                        elif p[h] != v:
                            ok = False
                        else:
                            checks += 1
                    if ok:
                        surv[t] += 1
                        checks_hist[t][checks] = checks_hist[t].get(checks, 0) + 1
                        if t == 0:
                            pt = "".join(ALPH[pa][x] if x is not None else "." for x in p)
                            k4_surv.append({"a": a, "b": b, "rule": f"{pa}/{ca}/{mode}", "checks": checks, "plaintext": pt})
        if ctx.time_left() < 60:
            break
    for r in k4_surv:
        filled = r["plaintext"].replace(".", "")
        r["english"] = round(score(filled), 3) if score and len(filled) >= 20 else None
    k4_surv.sort(key=lambda r: -(r["english"] or -99))
    cands = [{"plaintext": r["plaintext"], "key": f"self-key a={r['a']} b={r['b']} {r['rule']}"}
             for r in k4_surv if "." not in r["plaintext"]][:5]
    bounds = {"family": "the message as its own key through K3's rule f(i) = a + b i mod 97", "maps": n, "rules": len(rules),
              "k4_survivors": surv[0], "controls_survivors": surv[1:],
              "k4_checks_histogram": dict(sorted(checks_hist[0].items())),
              "k4_top_survivors": k4_surv[:10],
              "controls": f"{N_CONTROLS} shuffled coppers (seed 104), identical search"}
    notes = (f"{n:,} maps x {len(rules)} rules. Settings with no contradiction: K4 {surv[0]}, controls {surv[1:]}. "
             f"K4 survivors' checks: {dict(sorted(checks_hist[0].items()))}. Full decryptions returned: {len(cands)}.")
    return {"candidates": cands, "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    I = {c: i for i, c in enumerate(KRY)}
    lines = ["a = 0, b = 96 (the mirror): place i takes its key from the message letter at place 99 - i",
             "sculpture's alphabet, Vigenere: carved = message + key", "",
             "place  known  carved  key place  message letter there = carved - known"]
    for q in (22, 23, 24, 25, 64, 65):
        j = (96 * (q - 1)) % N
        lines.append(f"{q:>5}  {known[q]:>5}  {ct[q - 1]:>6}  {j + 1:>9}  {KRY[(I[ct[q - 1]] - I[known[q]]) % 26]:>12}")
    return "\n".join(lines)
