"""Experiment 0034. See program.md for the contract."""

EXPERIMENT = {
    "slug": "complete-the-key-at-surviving-periods",
    "title": "Finish the job at the surviving periods: fix the 24 forced key letters, climb the rest by English, and see how English the text can get",
    "family": "1-keyed-periodic",
    "parent": "0005-quagmire-period-sweep-forced-keys",
    "changed": "The first experiment that produces full candidates. At every period the cribs allow (27-29, and 53-95 sampled every third) under the 24 conventions, the forced key slots are fixed and the free slots are chosen to maximise the English score of the other 73 letters. The question is how English the best text is, against the same procedure on shuffled K4.",
    "hypothesis_expert": (
        "0005 left periods 27-29 and 53-97 alive under every convention, and 0009 showed the forced key "
        "stretches are noise; but noise in the key is compatible with a real periodic cipher if the key is "
        "not a word. The remaining test is the plaintext: fix the 24 forced slots, choose the 3 to 73 free "
        "slots by coordinate descent on the quadgram score of the 73 non-crib letters, with twenty random "
        "restarts, and record the best score per period and convention. A true periodic cipher at one of "
        "these periods would give a text scoring near English, about -3.6, at that period and convention; "
        "the same climb on shuffled K4 calibrates what overfitting achieves, which rises with the number of "
        "free slots. Candidates are submitted; they pass the crib gate by construction, so the English "
        "deficit and the key cost carry the verdict, and a 27-letter random key costs about 67 points of "
        "loss on its own. Bounds: coordinate descent is not exhaustive above period 27; period 27 is close "
        "to exhaustive with twenty restarts over 3 free slots."
    ),
    "hypothesis_eli5": (
        "For a repeating secret word of length 27, 28 or 29, the 24 known letters fix 24 letters of the "
        "word and leave a few unknown. We fill the unknown ones in every way and read the message that "
        "comes out, keeping the one that reads most like English. If the cipher really were of this kind, "
        "one filling would read like a real message. We also run the same game on scrambled versions of "
        "the carved text, to see how English-looking a text can be made by filling alone."
    ),
    "prediction": (
        "At periods 27-29 the best English score is below -5.0 per quadgram under every convention, the "
        "same as on shuffled K4, far from the -3.6 of English. At periods 53-97 the climb reaches -4.5 or "
        "better on both K4 and shuffled K4 because of the many free slots; the gap between them is under "
        "0.2. Candidates pass the gates but carry a loss above 60 from the key cost; none reads as English."
    ),
    "method": (
        "1. For each convention and live period, force the key letters at the crib slots. 2. Start the free "
        "slots at random; repeat: for each free slot in turn, try all 26 letters and keep the one giving the "
        "best score of the non-crib letters; stop when a pass changes nothing. 3. Twenty restarts; keep the "
        "best. 4. Submit the best text per period as a candidate. 5. Repeat the whole procedure on three "
        "shuffles of K4."
    ),
    "walkthrough": (
        "1. Take period 27 and the sculpture's alphabet with Vigenere. 2. The 24 known letters force 24 of "
        "the 27 key letters; say slots 0, 9 and 17 are free. 3. Put any letters in the three free slots and "
        "decrypt all 97 letters. 4. Change slot 0 through A to Z, decrypting each time, and keep the letter "
        "that makes the 73 unknown letters read most like English. 5. Do the same for slots 9 and 17, then "
        "go round again until nothing changes. 6. Read the result. 7. Start again from different letters "
        "a few times and keep the best."
    ),
}

import random
from kryptos.alphabets import ALPHABETS, conventions, key_letter_for, decrypt_letter, encrypt_letter

N = 97
PERIODS = [27, 28, 29] + list(range(53, 98, 3))
RESTARTS = 20


def encrypt(plaintext, key):
    pa, ca, ka, m, k = key["pa"], key["ca"], key["ka"], key["m"], key["key"]
    return "".join(encrypt_letter(p, k[i % len(k)], pa, ca, ka, m) for i, p in enumerate(plaintext))


def climb(ct, known, P, conv, score, rng, restarts):
    pa, ca, ka, m = conv
    A = ALPHABETS[ka]
    fixed = {}
    for pos, p in known.items():
        s = (pos - 1) % P
        k = key_letter_for(p, ct[pos - 1], pa, ca, ka, m)
        if s in fixed and fixed[s] != k:
            return None
        fixed[s] = k
    free = [s for s in range(P) if s not in fixed]
    crib_idx = {pos - 1 for pos in known}
    dec_table = {(c, k): decrypt_letter(c, k, pa, ca, ka, m) for c in ALPHABETS["std"] for k in A}

    def text(key):
        return "".join(dec_table[(ct[i], key[i % P])] for i in range(N))

    def free_score(pt):
        return score("".join(ch for i, ch in enumerate(pt) if i not in crib_idx))

    best_pt, best_sc, best_key = None, -99, None
    for _ in range(restarts):
        key = [fixed.get(s, rng.choice(A)) for s in range(P)]
        cur = free_score(text(key))
        changed = True
        while changed:
            changed = False
            for s in free:
                orig = key[s]; best_l, best_v = orig, cur
                for l in A:
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
            best_sc, best_key = cur, "".join(key); best_pt = text(key)
    return best_pt, best_sc, best_key, len(free)


def sweep(ct, known, convs, score, rng, restarts, time_left, periods):
    out = []
    for P in periods:
        for conv in convs:
            if time_left() < 60:
                return out
            r = climb(ct, known, P, conv, score, rng, restarts)
            if r is None:
                continue
            pt, sc, key, nfree = r
            out.append((sc, P, conv, pt, key, nfree))
    return out


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    convs = list(conventions())
    rng = random.Random(34)
    res = sweep(ct, known, convs, ctx.english_score, rng, RESTARTS, ctx.time_left, PERIODS)
    res.sort(key=lambda t: -t[0])
    by_period = {}
    for sc, P, conv, pt, key, nfree in res:
        if P not in by_period or sc > by_period[P][0]:
            by_period[P] = (sc, "/".join(conv), pt, key, nfree)
    candidates = []
    for P in sorted(by_period):
        sc, cv, pt, key, nfree = by_period[P]
        pa, ca, ka, m = cv.split("/")
        candidates.append({"plaintext": pt, "key": {"pa": pa, "ca": ca, "ka": ka, "m": m, "key": key}, "key_bits": 4.7 * P,
                           "key_description": f"period {P} key {key} ({nfree} free slots climbed); {cv}", "notes": f"English of the 73 free letters {sc:.3f}"})
    candidates.sort(key=lambda c: -float(c["notes"].split()[-1]))
    controls = {}
    for seed in range(3):
        if ctx.time_left() < 300:
            break
        letters_ = list(ct); random.Random(seed).shuffle(letters_)
        cres = sweep("".join(letters_), known, convs, ctx.english_score, rng, 5, ctx.time_left, [27, 28, 29, 53, 60, 70, 80, 97])
        for sc, P, conv, pt, key, nfree in cres:
            controls[P] = max(controls.get(P, -99), sc)
    return {
        "candidates": candidates[:50],
        "bounds": {"family": "periodic tableau at surviving periods, key completed by English climb", "conventions": 24, "periods": "27-29, then 53-95 every third",
                   "restarts": RESTARTS, "best_by_period": {str(P): {"english": round(v[0], 3), "convention": v[1], "free_slots": v[4], "text": v[2]} for P, v in sorted(by_period.items())},
                   "shuffled_k4_best_by_period": {str(P): round(v, 3) for P, v in sorted(controls.items())},
                   "english_reference": -3.6},
        "notes": f"Best English at 27-29: {[round(by_period[P][0], 3) for P in (27, 28, 29) if P in by_period]}; shuffled K4 at 27-29: {[round(controls[P], 3) for P in (27, 28, 29) if P in controls]}. Best overall {res[0][0]:.3f} at period {res[0][1]} vs shuffled best {max(controls.values()) if controls else None}.",
    }


def worked_example(ctx, key):
    conv = ("kry", "kry", "kry", "vig")
    r = climb(ctx.K4, ctx.KNOWN, 27, conv, ctx.english_score, random.Random(1), 3)
    pt, sc, k, nfree = r
    lines = ["period 27, KRYPTOS alphabet throughout, Vigenere; 24 slots forced, 3 free, climbed by English (3 restarts)", "", f"key   {k}", f"text  {pt}", f"English of the free letters {sc:.3f} (English about -3.6, noise about -6.5)"]
    return "\n".join(lines)
