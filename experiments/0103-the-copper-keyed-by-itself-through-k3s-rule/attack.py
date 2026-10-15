"""Experiment 0103. See program.md for the contract."""

EXPERIMENT = {
    "slug": "the-copper-keyed-by-itself-through-k3s-rule",
    "title": "The copper as its own key, read through K3's counting rule: key letter for place i is the carved letter at a + b i mod 97",
    "family": "1-keyed-periodic",
    "parent": "0002-ciphertext-autokey",
    "changed": "0002 tested ciphertext autokey, where the key for place i is the carved letter a fixed distance back (i - lag). Here the key is the carved letter at any place given by K3's rule, a + b i mod 97 for every a and b, which includes the copper read backwards (b = -1, a mirror) and every decimation; alone, or with a repeating key of length 1-26 added.",
    "hypothesis_expert": (
        "Scheidt: 'mirrors and obfuscation' (C13), the system 'conveys not only the encrypted data, but also the key' "
        "(C6); K3's transposition is the rule i -> 191 + 192 i mod 337 (01-facts.md). Model: p_i = D(c_i, c_{f(i)}) with "
        "f(i) = a + b i mod 97, b = 1-96, a = 0-96, f(i) != i for the 24 known places, D the tableau decryption in one of "
        "8 classes (plain and cipher alphabets standard or KRYPTOS; Vigenere, Beaufort, variant; key letters numbered on "
        "the cipher alphabet). The key is the copper itself, so every known letter is a check: 24 checks per setting. "
        "Second part: p_i = D(c_i, c_{f(i)} + k[i mod L]), L = 1-26; the residual must be periodic, tested by slot "
        "agreement. Ten shuffled coppers. 0002's lags are the case b = 1."
    ),
    "hypothesis_eli5": (
        "A cipher can use its own letters as the key. Experiment 2 tried taking the key for each letter from a fixed "
        "number of letters earlier. Here the key letter is picked from anywhere in the copper by K3's own counting rule: "
        "start somewhere, step by a fixed amount, wrap around at 97. That includes reading the copper backwards, like a "
        "mirror. We try every start and step, alone and with a short secret word added, against the 24 known letters."
    ),
    "prediction": (
        "Alone: no (a, b, class) fits more than 6 of 24 known letters, as on the coppers. With a repeating key: nothing "
        "consistent below period 20, counts in the coppers' range. Zero candidates."
    ),
    "method": (
        "1. For each a, b and class, compute the residual r_i = (key value needed at known place i) - (number of c_{f(i)}). "
        "2. Alone: count known places with r_i = 0. 3. With a key of length L: residuals sharing slot i mod L must agree. "
        "4. Repeat on ten shuffled coppers. 5. Decrypt any full fit."
    ),
    "walkthrough": (
        "1. Choose a start a = 0 and a step b = 96, which reads the copper backwards: place i takes its key from place 99 - i. "
        "2. Place 22 (E, carved F) takes its key from place 77, a D. "
        "3. On the sculpture's alphabet with Vigenere, F minus D must give E; count a hit if it does. "
        "4. Do this for all 24 known places, every start and step, and every table rule. "
        "5. With a secret word added, the leftover at each known place must repeat with the word's length."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
LMAX = 26
ALPH = {"std": STD, "kry": KRY}
N_CONTROLS = 10


def slot_pairs(slots):
    last, prs = {}, []
    for e, s in enumerate(slots):
        if s in last:
            prs.append((last[s], e))
        last[s] = e
    return prs


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    places = sorted(known)
    pidx = [p - 1 for p in places]
    rng = random.Random(103)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    T = len(texts)
    classes = [(pa, ca, mode) for pa in ALPH for ca in ALPH for mode in ("vig", "beau")]   # variant = vig with negated key
    pairs = {L: slot_pairs([i % L for i in pidx]) for L in range(1, LMAX + 1)}
    best = [0] * T
    full = []
    live = [[0] * (LMAX + 1) for _ in range(T)]
    k4_low = []
    n = 0
    for b in range(1, N):
        for a in range(N):
            f = [(a + b * i) % N for i in pidx]
            if any(f[e] == pidx[e] for e in range(24)):
                continue
            n += 1
            for pa, ca, mode in classes:
                PI = {c: i for i, c in enumerate(ALPH[pa])}; CI = {c: i for i, c in enumerate(ALPH[ca])}
                for t in range(T):
                    txt = texts[t]
                    need = [((CI[txt[j]] - PI[known[places[e]]]) if mode == "vig" else (CI[txt[j]] + PI[known[places[e]]])) % 26
                            for e, j in enumerate(pidx)]
                    have = [CI[txt[x]] for x in f]
                    for sgn in (1, -1):                     # key added or subtracted (variant Beaufort)
                        r = [(need[e] - sgn * have[e]) % 26 for e in range(24)]
                        hits = sum(1 for x in r if x == 0)
                        if hits > best[t]:
                            best[t] = hits
                        if t == 0 and hits == 24:
                            full.append((a, b, pa, ca, mode, sgn))
                        first = None
                        for L in range(1, LMAX + 1):
                            if all(r[x] == r[y] for x, y in pairs[L]):
                                live[t][L] += 1
                                if first is None:
                                    first = L
                        if t == 0 and first is not None and first < 20:
                            k4_low.append({"a": a, "b": b, "class": f"{pa}/{ca}/{mode}", "sign": sgn, "period": first})
    out = [L for L in range(1, LMAX + 1) if not (min(live[t][L] for t in range(1, T)) <= live[0][L] <= max(live[t][L] for t in range(1, T)))]
    cands = []
    for a, b, pa, ca, mode, sgn in full:
        CI = {c: i for i, c in enumerate(ALPH[ca])}
        pt = []
        for i in range(N):
            k = sgn * CI[ct[(a + b * i) % N]]
            v = (CI[ct[i]] - k) if mode == "vig" else (k - CI[ct[i]])
            pt.append(ALPH[pa][v % 26])
        cands.append({"plaintext": "".join(pt), "key": f"self-key a={a} b={b} {pa}/{ca}/{mode} sign {sgn}"})
    bounds = {"family": "the copper as its own key through K3's rule f(i) = a + b i mod 97, alone or plus a periodic key",
              "maps": n, "classes": len(classes) * 2, "k4_best_hits_alone": best[0], "controls_best_hits_alone": best[1:],
              "k4_full_alone": len(full),
              "k4_live_by_period": live[0][1:],
              "controls_live_min": [min(live[t][L] for t in range(1, T)) for L in range(1, LMAX + 1)],
              "controls_live_max": [max(live[t][L] for t in range(1, T)) for L in range(1, LMAX + 1)],
              "periods_outside_control_range": out, "k4_live_below_20": k4_low[:40], "n_k4_live_below_20": len(k4_low),
              "controls": f"{N_CONTROLS} shuffled coppers (seed 103), identical search"}
    notes = (f"{n:,} maps x {len(classes) * 2} rules. Alone: K4 best {best[0]}/24, controls {best[1:]}; full fits {len(full)}. "
             f"With a periodic key: K4 live below 20: {len(k4_low)}; periods outside the control range: {out}.")
    return {"candidates": cands, "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    I = {c: i for i, c in enumerate(KRY)}
    lines = ["the copper read backwards as its own key: place i takes its key from place 99 - i (a = 0, b = 96)",
             "sculpture's alphabet, Vigenere", "", "place  known  carved  key place  key letter  carved - key  hit"]
    for q in (22, 23, 24, 25, 64, 65, 74):
        j = (0 + 96 * (q - 1)) % N
        d = KRY[(I[ct[q - 1]] - I[ct[j]]) % 26]
        lines.append(f"{q:>5}  {known[q]:>5}  {ct[q - 1]:>6}  {j + 1:>9}  {ct[j]:>10}  {d:>12}  {'yes' if d == known[q] else 'no'}")
    return "\n".join(lines)
