"""Experiment 0045. See program.md for the contract."""

EXPERIMENT = {
    "slug": "running-key-k1-k3-mixed-alphabets",
    "title": "The earlier messages as a running key, on tables rebuilt from the puzzle's words",
    "family": "1-keyed-periodic",
    "parent": "0004-running-key-from-k1-k3",
    "changed": "Experiment 4 slid the K1-K3 plaintexts and ciphertexts past K4 under the standard and KRYPTOS alphabets. Here the plain and cipher alphabets are the keyword mixings of every vocabulary word, with the key letters read on the standard or KRYPTOS order.",
    "hypothesis_expert": (
        "Sanborn's 'clues to the last section are contained in previously deciphered parts' (C7) read as a "
        "running key was killed under 24 conventions in experiment 4. Under keyword-mixed plain and cipher "
        "alphabets (C5, C29) every trial changes, so the sweep is rerun: sources are the K1, K2 (as carved "
        "and corrected) and K3 plaintexts, the three ciphertexts, and the concatenations of each set, read "
        "forward and backward at every cyclic offset; 63 plain x 63 cipher alphabets x 2 key alphabets x 3 "
        "modes; mismatches counted with early exit at three. Chance survival per trial is 26 to the minus "
        "24, with about 180 million trials. Bounds: complete for these texts and alphabets."
    ),
    "hypothesis_eli5": (
        "Experiment 4 asked whether the first three messages, lined up under the fourth as a long secret "
        "word, could explain the known letters, using the sculpture's own table. The table might have been "
        "built from another word, so we rebuild it from each word the puzzle knows and slide the three "
        "messages past the fourth again, at every starting point, forwards and backwards."
    ),
    "prediction": (
        "No text, offset, direction or alphabet pair explains all 24 known letters, and none comes within "
        "two mismatches. Zero candidates pass."
    ),
    "method": (
        "1. Build the key texts and the alphabet pool. 2. For each plain and cipher alphabet, key alphabet "
        "and mode, precompute the cipher letter for every (plain, key) pair. 3. For each text, direction and "
        "offset, count mismatches at the 24 cribs, stopping at the third. 4. Keep trials within two "
        "mismatches; decrypt and submit any with zero."
    ),
    "walkthrough": (
        "1. Build the alphabet from BERLIN for the message letters and from CLOCK for the carved letters. "
        "2. Lay the K1 plaintext under the fourth message starting at some offset, so each position has a key "
        "letter. 3. Position 22 is E: find E in the BERLIN alphabet, add the key letter's place in the plain "
        "alphabet, and read the result in the CLOCK alphabet; compare with the carved F. 4. A miss counts "
        "one; three misses end this offset. 5. Slide the offset along the whole text, then reverse the text, "
        "then try the next pair of alphabets."
    ),
}

from kryptos.alphabets import keyword_mixed
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY, load_k1, load_k2, load_k3

N = 97
MODES_ENC = {"vig": lambda p, k: (p + k) % 26, "beau": lambda p, k: (k - p) % 26, "varbeau": lambda p, k: (p - k) % 26}
MODES_DEC = {"vig": lambda c, k: (c - k) % 26, "beau": lambda c, k: (k - c) % 26, "varbeau": lambda c, k: (c + k) % 26}


def letters(s):
    return "".join(c for c in s if "A" <= c <= "Z")


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


def sources():
    k1, k2, k3 = load_k1(), load_k2(), load_k3()
    p1, p2, p2c, p3 = letters(k1["plaintext"]), letters(k2["plaintext_as_carved"]), letters(k2.get("plaintext_corrected_ending", "") or ""), letters(k3["plaintext"])
    c1, c2, c3 = letters(k1["ciphertext"]), letters(k2["ciphertext_as_carved"]), letters(k3["ciphertext"])
    src = {"K1 plain": p1, "K2 plain": p2, "K3 plain": p3, "K1+K2+K3 plain": p1 + p2 + p3,
           "K1 cipher": c1, "K2 cipher": c2, "K3 cipher": c3, "K1+K2+K3 cipher": c1 + c2 + c3}
    if p2c and p2c != p2:
        src["K2 plain corrected ending"] = p2c
    out = {}
    for name, t in src.items():
        out[name + " fwd"] = t; out[name + " bwd"] = t[::-1]
    return out


def encrypt(plaintext, key):
    text = sources()[key["source"]]; n = len(text); o = key["offset"]
    pa, ca, ka, m = key["pa"], key["ca"], key["ka"], key["m"]
    f = MODES_ENC[m]
    return "".join(ca[f(pa.index(p), ka.index(text[(o + i) % n]))] for i, p in enumerate(plaintext))


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    pool = pool_of(list(ctx.vocabulary))
    src = sources()
    crib = sorted(known.items())
    trials, near, candidates = 0, [], []
    stopped = False
    for pname, pa in pool.items():
        pidx = {ch: i for i, ch in enumerate(pa)}
        for cname, ca in pool.items():
            for ka_name in ("std", "kry"):
                ka = pool[ka_name]; kidx = {ch: i for i, ch in enumerate(ka)}
                for m, f in MODES_ENC.items():
                    table = {(p, k): ca[f(pidx[p], kidx[k])] for p in set(known.values()) for k in STD}
                    for name, text in src.items():
                        n = len(text)
                        for o in range(n):
                            trials += 1
                            mism = 0
                            for pos, p in crib:
                                if table[(p, text[(o + pos - 1) % n])] != ct[pos - 1]:
                                    mism += 1
                                    if mism > 2:
                                        break
                            if mism <= 2:
                                near.append((mism, name, pname, cname, ka_name, m, o))
                                if mism == 0:
                                    fd = MODES_DEC[m]; cidx = {ch: i for i, ch in enumerate(ca)}
                                    pt = "".join(pa[fd(cidx[ct[i]], kidx[text[(o + i) % n]])] for i in range(N))
                                    candidates.append({"plaintext": pt, "key": {"source": name, "offset": o, "pa": pa, "ca": ca, "ka": ka, "m": m}, "key_bits": 25,
                                                       "key_description": f"running key {name} offset {o}; plain {pname}, cipher {cname}, key {ka_name}, {m}"})
            if ctx.time_left() < 90:
                stopped = True; break
        if stopped:
            break
    near.sort()
    return {
        "candidates": candidates[:50],
        "bounds": {"family": "running key from K1-K3 plaintexts and ciphertexts, keyword-mixed alphabets", "alphabets": len(pool), "key_alphabets": ["std", "kry"], "modes": 3,
                   "sources": {k: len(v) for k, v in src.items()}, "trials": trials, "stopped_by_clock": stopped,
                   "fewest_mismatches": near[0][0] if near else "more than 2",
                   "near_misses": [{"mismatches": a, "source": b, "plain": c, "cipher": d, "key": e, "mode": f_, "offset": g} for a, b, c, d, e, f_, g in near[:20]],
                   "survivors": len(candidates)},
        "notes": f"{trials} trials{' (stopped by the clock)' if stopped else ''}; {len(candidates)} survivors; {len(near)} within two mismatches.",
    }


def worked_example(ctx, key):
    pa, ca = keyword_mixed("BERLIN"), keyword_mixed("CLOCK")
    text = sources()["K1 plain fwd"]
    lines = [f"plain alphabet BERLIN/keyword {pa}", f"cipher alphabet CLOCK/keyword {ca}", "key text: K1 plaintext at offset 0, key letters on the standard order; Vigenere", "", "pos  plain  key  result  carved  match"]
    for pos in (22, 23, 24, 25, 64, 65):
        p = ctx.KNOWN[pos]; k = text[pos - 1]; c = ca[(pa.index(p) + STD.index(k)) % 26]
        lines.append(f"{pos:>3}    {p}     {k}     {c}       {ctx.K4[pos-1]}     {'yes' if c == ctx.K4[pos-1] else 'no'}")
    return "\n".join(lines)
