"""Experiment 0048. See program.md for the contract."""

EXPERIMENT = {
    "slug": "complete-the-key-both-alphabets-mixed-sampled",
    "title": "The last corner of family 1: both alphabets rebuilt from the puzzle's words, key completed at periods 27 to 29, sampled",
    "family": "1-keyed-periodic",
    "parent": "0035-complete-the-key-mixed-alphabets-27-29",
    "changed": "Experiment 35 mixed one alphabet at a time. Here both the message alphabet and the carved alphabet are keyword mixings of vocabulary words, 61 x 61 pairs, drawn in random order with a fixed seed until the budget runs out; the record says how many pairs were reached. Periods 27 to 29, three restarts.",
    "hypothesis_expert": (
        "Experiments 34 and 35 found the key completion at periods 27-29 reads as noise under every pair "
        "with at most one keyword-mixed side. The remaining corner is both sides mixed: 3,721 pairs x 3 modes "
        "x 3 periods, about 33,000 climbs at 0.1 s each with three restarts, more than the budget allows, "
        "so pairs are visited in a fixed random order and the run stops at the clock; coverage is reported. "
        "A true periodic cipher on such a pair would give a text near -3.6 at its period; shuffled K4 gives "
        "about -6.8. Bounds: a stated fraction of the pair space, not exhaustive; the seed makes the sample "
        "reproducible and a later run can continue it."
    ),
    "hypothesis_eli5": (
        "Experiments 34 and 35 filled in the few unknown letters of a secret word of length 27 to 29 and "
        "found only nonsense, with the sculpture's table and with tables rebuilt from one puzzle word on one "
        "side. The last version has both sides of the table rebuilt from puzzle words. There are too many "
        "pairs of words to finish in one sitting, so we draw pairs at random for half an hour and report "
        "how far we got."
    ),
    "prediction": (
        "Within the budget about a third of the pairs are reached. No pair and period gives a text better "
        "than -5.5 per quadgram; the best is within 0.4 of shuffled K4. Candidates pass the gates by "
        "construction but none reads as English or beats the current champion's fitness."
    ),
    "method": (
        "1. Build the alphabet pool: standard, KRYPTOS and the keyword mixing of each vocabulary word. "
        "2. For each pair with one side standard or KRYPTOS, each mode and each period 27-29, force the 24 "
        "key slots from the cribs; skip the pair if two cribs disagree on a slot. 3. Climb the free slots "
        "by coordinate descent on the English score of the 73 non-crib letters, five restarts. 4. Keep the "
        "best text per period and submit it. 5. Repeat on one shuffle of K4 for calibration."
    ),
    "walkthrough": (
        "1. Build the alphabet from PALIMPSEST: PALIMSETBCDFGHJKNOQRUVWXYZ, and use it for the message; "
        "keep KRYPTOS for the carved letters; Vigenere. 2. Period 27: position 22 is E, index 6 in the "
        "PALIMPSEST alphabet; carved F is index 11 in KRYPTOS; the key index is 5. 3. Do this for all 24 "
        "known letters; positions 22 and 49 share slot 21, but 49 is unknown, so no clash. 4. Three slots "
        "stay free. 5. Try every letter in each free slot in turn, decrypting the whole text each time, and "
        "keep the one that makes the 73 unknown letters read most like English. 6. Compare the best text's "
        "score with English, about -3.6, and with what the same game gives on shuffled letters, about -6.8."
    ),
}

import random
from kryptos.alphabets import keyword_mixed
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
PERIODS = [27, 28, 29]
RESTARTS = 3
MODES_KEY = {"vig": lambda p, c: (c - p) % 26, "beau": lambda p, c: (c + p) % 26, "varbeau": lambda p, c: (p - c) % 26}
MODES_DEC = {"vig": lambda c, k: (c - k) % 26, "beau": lambda c, k: (k - c) % 26, "varbeau": lambda c, k: (c + k) % 26}
MODES_ENC = {"vig": lambda p, k: (p + k) % 26, "beau": lambda p, k: (k - p) % 26, "varbeau": lambda p, k: (p - k) % 26}


def pool_of(vocab):
    pool = {"std": STD, "kry": KRY}
    for w in vocab:
        if len(set(w)) >= 3:
            pool[f"{w}/keyword"] = keyword_mixed(w)
    seen, out = {}, {}
    for name, A in pool.items():
        if A not in seen:
            seen[A] = name; out[name] = A
    return out


def encrypt(plaintext, key):
    pa, ca, m, k = key["pa"], key["ca"], key["m"], key["key"]   # key is a list of indices
    f = MODES_ENC[m]
    return "".join(ca[f(pa.index(p), k[i % len(k)])] for i, p in enumerate(plaintext))


def climb(ct, known, P, pa, ca, m, score, rng, restarts):
    fk, fd = MODES_KEY[m], MODES_DEC[m]
    pidx = {ch: i for i, ch in enumerate(pa)}
    cidx = {ch: i for i, ch in enumerate(ca)}
    fixed = {}
    for pos, p in known.items():
        s = (pos - 1) % P
        k = fk(pidx[p], cidx[ct[pos - 1]])
        if s in fixed and fixed[s] != k:
            return None
        fixed[s] = k
    free = [s for s in range(P) if s not in fixed]
    crib_idx = {pos - 1 for pos in known}
    cts = [cidx[c] for c in ct]

    def text(key):
        return "".join(pa[fd(cts[i], key[i % P])] for i in range(N))

    def free_score(pt):
        return score("".join(ch for i, ch in enumerate(pt) if i not in crib_idx))

    best_pt, best_sc, best_key = None, -99, None
    for _ in range(restarts):
        key = [fixed.get(s, rng.randrange(26)) for s in range(P)]
        cur = free_score(text(key))
        changed = True
        while changed:
            changed = False
            for s in free:
                orig = key[s]; best_l, best_v = orig, cur
                for l in range(26):
                    if l == orig:
                        continue
                    key[s] = l
                    v = free_score(text(key))
                    if v > best_v:
                        best_l, best_v = l, v
                key[s] = best_l
                if best_l != orig:
                    cur = best_v; changed = True
        if cur > best_sc:
            best_sc, best_key, best_pt = cur, list(key), text(key)
    return best_pt, best_sc, best_key, len(free)


def pairs_of(pool):
    mixed = [n for n in pool if n not in ("std", "kry")]
    out = [(p_, c_) for p_ in mixed for c_ in mixed]
    random.Random(48).shuffle(out)
    return out


def sweep(ct, known, pool, score, rng, restarts, time_left, reserve=90):
    res = []
    for pname, cname in pairs_of(pool):
        for m in MODES_KEY:
            for P in PERIODS:
                if time_left() < reserve:
                    return res
                r = climb(ct, known, P, pool[pname], pool[cname], m, score, rng, restarts)
                if r is None:
                    continue
                pt, sc, key, nfree = r
                res.append((sc, P, pname, cname, m, pt, key, nfree))
    return res


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    pool = pool_of(list(ctx.vocabulary))
    rng = random.Random(35)
    res = sweep(ct, known, pool, ctx.english_score, rng, RESTARTS, ctx.time_left, reserve=260)
    pairs_reached = len({(r[2], r[3]) for r in res})
    res.sort(key=lambda t: -t[0])
    by_period = {}
    for sc, P, pname, cname, m, pt, key, nfree in res:
        if P not in by_period or sc > by_period[P][0]:
            by_period[P] = (sc, pname, cname, m, pt, key, nfree)
    candidates = []
    for P, (sc, pname, cname, m, pt, key, nfree) in sorted(by_period.items()):
        candidates.append({"plaintext": pt, "key": {"pa": pool[pname], "ca": pool[cname], "m": m, "key": key}, "key_bits": 4.7 * P,
                           "key_description": f"period {P}, plain {pname}, cipher {cname}, {m}; {nfree} free slots climbed", "notes": f"English of the 73 free letters {sc:.3f}"})
    control = {}
    if ctx.time_left() > 120:
        letters_ = list(ct); random.Random(0).shuffle(letters_)
        small = {k: pool[k] for k in list(pool)[2:12]}
        cres = sweep("".join(letters_), known, small, ctx.english_score, rng, RESTARTS, ctx.time_left, reserve=30)
        for sc, P, *_ in cres:
            control[P] = max(control.get(P, -99), sc)
    return {
        "candidates": candidates[:50],
        "bounds": {"family": "periodic tableau at periods 27-29, one alphabet standard or KRYPTOS and the other keyword-mixed from the vocabulary, key completed by English climb",
                   "alphabets": len(pool), "pairs_total": len(pairs_of(pool)), "pairs_reached": pairs_reached, "coverage": round(pairs_reached / len(pairs_of(pool)), 3), "periods": PERIODS, "restarts": RESTARTS, "climbs": len(res),
                   "best_by_period": {str(P): {"english": round(v[0], 3), "plain": v[1], "cipher": v[2], "mode": v[3], "free_slots": v[6], "text": v[4]} for P, v in sorted(by_period.items())},
                   "top_ten": [{"english": round(sc, 3), "period": P, "plain": a, "cipher": b, "mode": m} for sc, P, a, b, m, *_ in res[:10]],
                   "shuffled_k4_best_by_period": {str(P): round(v, 3) for P, v in sorted(control.items())}, "english_reference": -3.6},
        "notes": f"{len(res)} climbs over {pairs_reached} of {len(pairs_of(pool))} pairs. Best by period: {[(P, round(v[0], 3)) for P, v in sorted(by_period.items())]}; shuffled K4 (22-alphabet subset): {[(P, round(v, 3)) for P, v in sorted(control.items())]}.",
    }


def worked_example(ctx, key):
    pa, ca = keyword_mixed("PALIMPSEST"), KRY
    r = climb(ctx.K4, ctx.KNOWN, 27, pa, ca, "vig", ctx.english_score, random.Random(1), 2)
    if r is None:
        return "PALIMPSEST / KRYPTOS at period 27 under Vigenere: two known letters clash on one slot, so this pair is out before any climb."
    pt, sc, k, nfree = r
    return "\n".join([f"plain alphabet PALIMPSEST/keyword {pa}; cipher alphabet KRYPTOS; Vigenere; period 27; {nfree} free slots climbed", "", f"key indices {k}", f"text       {pt}", f"English of the free letters {sc:.3f} (English about -3.6, noise about -6.8)"])
