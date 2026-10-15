"""Experiment 0030. See program.md for the contract."""

EXPERIMENT = {
    "slug": "self-referential-keys-affine-and-mirror",
    "title": "The text as its own key: the ciphertext under every index rule, and the message keyed by itself backwards",
    "family": "1-keyed-periodic",
    "parent": "0025-autokeys-with-mixed-alphabets",
    "changed": "Autokey generalised. The key letter for position i is the ciphertext letter at a i + b mod 97 for every a and b, which includes every lag and every mirror of the ciphertext; or the plaintext letter at o - i mod 97, the message read backwards from any point.",
    "hypothesis_expert": (
        "Sanborn's mirrors and 'spatial systems' (C3) and the NSA's autokey guess (C11a) meet in self-keyed "
        "systems. Ciphertext self-key: c[i] = E(p[i], c[(a i + b) mod 97]); since every key letter is a "
        "carved letter, all 24 cribs are exact checks for each (a, b) and convention, 9,312 rules x 24 "
        "conventions, and a survivor decrypts the whole text at once. Plaintext mirror key: c[i] = E(p[i], "
        "p[(o - i) mod 97]) for every o; a crib forces its partner's plaintext letter and the chain closes "
        "as in 0012, with up to eleven exact checks where EASTNORTHEAST and BERLINCLOCK mirror onto each "
        "other. Survivors with 60 or more forced letters are scored as English against ten shuffled "
        "controls; fully forced texts are submitted. Bounds: complete for these rules and 24 conventions."
    ),
    "hypothesis_eli5": (
        "An autokey uses the text itself as the secret word, a fixed distance back. We widen that: the key "
        "for each letter may be the carved letter at any fixed stride and start, forwards or backwards, or "
        "the message letter the same distance from the other end. Because the carved letters are all known, "
        "the first kind is checked at every known letter at once. The second kind pairs the two known "
        "words with each other in the mirror, which gives a direct check too."
    ),
    "prediction": (
        "No ciphertext rule passes all 24 checks; the best passes 5 or 6. No mirror centre keeps the chain "
        "consistent beyond chance, and the large closures read as noise. Zero candidates pass."
    ),
    "method": (
        "1. For each (a, b) with a in 1-96 and b in 0-96 and each convention, encipher each known letter "
        "with the carved letter at a i + b and count mismatches. 2. Decrypt any zero-mismatch rule and submit. "
        "3. For each mirror centre o and convention, chain forced plaintext letters from the cribs through "
        "the mirror; reject on conflict. 4. Score closures of 60 or more letters as English; repeat on ten "
        "shuffles; submit fully forced texts."
    ),
    "walkthrough": (
        "1. Rule: stride 3, start 5. The key for position 1 is the carved letter at 5, for position 2 at 8, "
        "and so on, wrapping past 97. 2. Position 22 (E) gets the carved letter at 5 + 3 x 21 = 68, T. 3. On "
        "the sculpture's table with Vigenere, E under T gives some letter; compare with the carved F at 22. "
        "4. Do this for all 24 known letters; count the misses; any miss kills the rule. 5. Mirror: with "
        "centre 97, position 22 is keyed by position 75, which is not known, but position 24 is keyed by 73, "
        "the C of CLOCK, which is known: S under C must give the carved R. 6. Eleven such pairs decide the "
        "mirror at once."
    ),
}

import random
from kryptos.alphabets import conventions, key_letter_for, decrypt_letter, encrypt_letter

N = 97


def encrypt(plaintext, key):
    pa, ca, ka, m = key["pa"], key["ca"], key["ka"], key["m"]
    if key["kind"] == "ciphertext-affine":
        a, b = key["a"], key["b"]
        # ciphertext self-key is defined as a fixed point: solve by iteration over an index order where
        # key positions are known; here we re-encrypt using the recorded ciphertext as the key source
        src = key["ciphertext"]
        return "".join(encrypt_letter(p, src[(a * i + b) % N], pa, ca, ka, m) for i, p in enumerate(plaintext))
    o = key["o"]
    return "".join(encrypt_letter(p, plaintext[(o - i) % N], pa, ca, ka, m) for i, p in enumerate(plaintext))


def mirror_closure(ct, known, o, conv):
    pa, ca, ka, m = conv
    forced = {pos - 1: p for pos, p in known.items()}
    queue = list(forced)
    while queue:
        i = queue.pop()
        p = forced[i]
        j = (o - i) % N                       # p[j] is the key for position i
        k = key_letter_for(p, ct[i], pa, ca, ka, m)
        if j in forced:
            if forced[j] != k:
                return False, forced
        else:
            forced[j] = k; queue.append(j)
        # p[i] is the key for position j' with (o - j') = i, i.e. j' = (o - i) = j: same pair, so
        # position j's plaintext decrypts with key p[i]
        q = decrypt_letter(ct[j], p, pa, ca, ka, m)
        if j in forced:
            if forced[j] != q:
                return False, forced
        else:
            forced[j] = q; queue.append(j)
    return True, forced


def runs_of(forced, skip):
    out, cur, prev = [], [], None
    for i in sorted(forced):
        if i in skip:
            if len(cur) >= 5: out.append("".join(cur))
            cur = []; prev = i; continue
        if prev is not None and i == prev + 1:
            cur.append(forced[i])
        else:
            if len(cur) >= 5: out.append("".join(cur))
            cur = [forced[i]]
        prev = i
    if len(cur) >= 5: out.append("".join(cur))
    return out


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    convs = list(conventions())
    crib = sorted(known.items())
    crib_idx = {p - 1 for p in known}
    # ciphertext affine self-key
    best_ct, survivors, candidates = 99, [], []
    trials = 0
    for conv in convs:
        pa, ca, ka, m = conv
        table = {(p, k): encrypt_letter(p, k, pa, ca, ka, m) for p in set(known.values()) for k in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
        for a in range(1, N):
            for b in range(N):
                trials += 1
                mism = 0
                for pos, p in crib:
                    i = pos - 1
                    if table[(p, ct[(a * i + b) % N])] != ct[i]:
                        mism += 1
                        if mism > 5:
                            break
                best_ct = min(best_ct, mism)
                if mism == 0:
                    survivors.append((a, b, conv))
                    pt = "".join(decrypt_letter(ct[i], ct[(a * i + b) % N], pa, ca, ka, m) for i in range(N))
                    candidates.append({"plaintext": pt, "key": {"kind": "ciphertext-affine", "a": a, "b": b, "pa": pa, "ca": ca, "ka": ka, "m": m, "ciphertext": ct},
                                       "key_bits": 14, "key_description": f"ciphertext self-key at {a} i + {b}; {pa}/{ca}/{ka} {m}"})
        if ctx.time_left() < 200:
            break
    # plaintext mirror key

    def mirror_sweep(text, score):
        best, full, consistent = [], [], 0
        for o in range(N):
            for conv in convs:
                ok, forced = mirror_closure(text, known, o, conv)
                if not ok:
                    continue
                consistent += 1
                if len(forced) >= 60:
                    runs = runs_of({i: c for i, c in forced.items() if i not in crib_idx}, set())
                    qs = sum(len(r) - 3 for r in runs)
                    if qs >= 4:
                        sc = sum(score(r) * (len(r) - 3) for r in runs) / qs
                        if len(best) < 10 or sc > best[-1][0]:
                            best.append((sc, o, "/".join(conv), len(forced), runs[:3])); best.sort(reverse=True); best = best[:10]
                if len(forced) == N:
                    full.append((o, conv, "".join(forced[i] for i in range(N))))
        return best, full, consistent

    best, full, consistent = mirror_sweep(ct, ctx.english_score)
    for o, conv, pt in full[:20]:
        pa, ca, ka, m = conv
        candidates.append({"plaintext": pt, "key": {"kind": "plaintext-mirror", "o": o, "pa": pa, "ca": ca, "ka": ka, "m": m}, "key_bits": 7,
                           "key_description": f"plaintext mirror key, centre {o}; {pa}/{ca}/{ka} {m}; fully forced"})
    nulls = []
    for seed in range(10):
        letters_ = list(ct); random.Random(seed).shuffle(letters_)
        nb, _, _ = mirror_sweep("".join(letters_), ctx.english_score)
        nulls.append(round(nb[0][0], 3) if nb else None)
    return {
        "candidates": candidates[:50],
        "bounds": {"family": "self-referential keys: ciphertext at a i + b, plaintext at o - i", "conventions": 24,
                   "ciphertext_rules": trials, "ciphertext_best_mismatches": best_ct, "ciphertext_survivors": len(survivors),
                   "mirror_centres": N, "mirror_consistent_pairs": consistent, "mirror_fully_forced": len(full),
                   "mirror_best_closures": [{"score": round(sc, 3), "centre": o, "convention": c, "forced": n, "runs": r} for sc, o, c, n, r in best],
                   "shuffled_control_best": nulls},
        "notes": f"Ciphertext self-key: {trials} rules, best {best_ct} mismatches, {len(survivors)} survivors. Mirror key: {consistent} consistent (centre, convention) pairs, {len(full)} fully forced; best closure {best[0][0] if best else None} vs shuffled {[x for x in nulls if x is not None]}.",
    }


def worked_example(ctx, key):
    lines = ["ciphertext self-key, stride 3, start 5, KRYPTOS alphabet throughout, Vigenere", "", "pos  plain  key pos  key  E+key  carved  match"]
    for pos in (22, 23, 24, 64, 65):
        i = pos - 1; j = (3 * i + 5) % N; k = ctx.K4[j]; c = encrypt_letter(ctx.KNOWN[pos], k, "kry", "kry", "kry", "vig")
        lines.append(f"{pos:>3}    {ctx.KNOWN[pos]}      {j+1:>3}     {k}     {c}      {ctx.K4[i]}     {'yes' if c == ctx.K4[i] else 'no'}")
    lines.append("")
    lines.append("mirror key, centre 97 (position i keyed by position 98-i): position 24 (S) is keyed by 74 (K), 25 (T) by 73 (C), ... 34 (T) by 64 (B)")
    ok, forced = mirror_closure(ctx.K4, ctx.KNOWN, 96, ("kry", "kry", "kry", "vig"))
    lines.append(f"chain under kry/kry/kry Vigenere: {'consistent' if ok else 'breaks'} after {len(forced)} letters")
    return "\n".join(lines)
