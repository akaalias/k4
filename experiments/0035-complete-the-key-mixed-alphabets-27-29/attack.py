"""Experiment 0035. See program.md for the contract."""

EXPERIMENT = {
    "slug": "complete-the-key-mixed-alphabets-27-29",
    "title": "The same key completion at periods 27 to 29, with the table rebuilt from the puzzle's words",
    "family": "1-keyed-periodic",
    "parent": "0034-complete-the-key-at-surviving-periods",
    "changed": "Experiment 34 climbed the free key letters under the standard and KRYPTOS alphabets only. Here one of the two alphabets, for the message or for the carved letters, is rebuilt from each vocabulary word, and the key alphabet is dropped, since it does not change the decryption. Periods 27 to 29 only, where the key has three to five free letters and the climb cannot overfit.",
    "hypothesis_expert": (
        "At periods 27-29 the cribs force 24 of the key slots and leave 3-5 free, so the English climb of "
        "experiment 34 is close to exhaustive and cannot overfit; it found noise under the 8 distinct "
        "plain-cipher alphabet classes of the 24 conventions. The key alphabet only relabels the key and "
        "never changes the decrypted text, so the real variable is the pair of plain and cipher alphabets. "
        "Scheidt's keyword alphabets (C5) and the K1-K2 precedent make a table built from a puzzle word the "
        "natural extension: here one of the pair is standard or KRYPTOS and the other is the keyword mixing "
        "of any of 61 vocabulary words, both ways round, under three modes: 756 classes, 3 periods, five "
        "restarts each. The best free-letter English per class and period is compared with the same climb "
        "on one shuffle of K4. A true periodic cipher on such a table would give a text near -3.6 at its "
        "period; shuffled K4 gives about -6.8. Bounds: complete for this alphabet pool at periods 27-29; "
        "both alphabets mixed from words at once is not covered."
    ),
    "hypothesis_eli5": (
        "Experiment 34 showed that with a secret word of length 27, 28 or 29, filling in the few unknown "
        "letters never produces a readable message when the table is the sculpture's own. But the table "
        "could have been built from another word, like PALIMPSEST or ABSCISSA, and that changes every "
        "letter that comes out. So we rebuild the table from each word the puzzle knows, in turn for the "
        "message side and for the carved side, and run the same filling game again."
    ),
    "prediction": (
        "No class and period gives a text better than -5.5 per quadgram; the best over all 2,268 climbs is "
        "within 0.4 of the best on shuffled K4. Candidates pass the gates by construction but none reads "
        "as English; none beats the current champion's fitness."
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
RESTARTS = 5
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
    basics = [n for n in ("std", "kry") if n in pool]
    out = []
    for b in basics:
        for n in pool:
            out.append((b, n))
            if n not in basics:
                out.append((n, b))
    return sorted(set(out))


def sweep(ct, known, pool, score, rng, restarts, time_left):
    res = []
    for pname, cname in pairs_of(pool):
        for m in MODES_KEY:
            for P in PERIODS:
                if time_left() < 90:
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
    res = sweep(ct, known, pool, ctx.english_score, rng, RESTARTS, ctx.time_left)
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
    if ctx.time_left() > 200:
        letters_ = list(ct); random.Random(0).shuffle(letters_)
        small = {k: pool[k] for k in list(pool)[:22]}
        cres = sweep("".join(letters_), known, small, ctx.english_score, rng, RESTARTS, ctx.time_left)
        for sc, P, *_ in cres:
            control[P] = max(control.get(P, -99), sc)
    return {
        "candidates": candidates[:50],
        "bounds": {"family": "periodic tableau at periods 27-29, one alphabet standard or KRYPTOS and the other keyword-mixed from the vocabulary, key completed by English climb",
                   "alphabets": len(pool), "classes": len(pairs_of(pool)) * 3, "periods": PERIODS, "restarts": RESTARTS, "climbs": len(res),
                   "best_by_period": {str(P): {"english": round(v[0], 3), "plain": v[1], "cipher": v[2], "mode": v[3], "free_slots": v[6], "text": v[4]} for P, v in sorted(by_period.items())},
                   "top_ten": [{"english": round(sc, 3), "period": P, "plain": a, "cipher": b, "mode": m} for sc, P, a, b, m, *_ in res[:10]],
                   "shuffled_k4_best_by_period": {str(P): round(v, 3) for P, v in sorted(control.items())}, "english_reference": -3.6},
        "notes": f"{len(res)} climbs. Best by period: {[(P, round(v[0], 3)) for P, v in sorted(by_period.items())]}; shuffled K4 (22-alphabet subset): {[(P, round(v, 3)) for P, v in sorted(control.items())]}.",
    }


def worked_example(ctx, key):
    pa, ca = keyword_mixed("PALIMPSEST"), KRY
    r = climb(ctx.K4, ctx.KNOWN, 27, pa, ca, "vig", ctx.english_score, random.Random(1), 2)
    if r is None:
        return "PALIMPSEST / KRYPTOS at period 27 under Vigenere: two known letters clash on one slot, so this pair is out before any climb."
    pt, sc, k, nfree = r
    return "\n".join([f"plain alphabet PALIMPSEST/keyword {pa}; cipher alphabet KRYPTOS; Vigenere; period 27; {nfree} free slots climbed", "", f"key indices {k}", f"text       {pt}", f"English of the free letters {sc:.3f} (English about -3.6, noise about -6.8)"])
