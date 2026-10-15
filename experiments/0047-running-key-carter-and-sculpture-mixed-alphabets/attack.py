"""Experiment 0047. See program.md for the contract."""

EXPERIMENT = {
    "slug": "running-key-carter-and-sculpture-mixed-alphabets",
    "title": "Carter's book and the sculpture's own texts as running keys, on tables rebuilt from the puzzle's words",
    "family": "1-keyed-periodic",
    "parent": "0045-running-key-k1-k3-mixed-alphabets",
    "changed": "The key texts are Carter's Tomb of Tut-ankh-Amen and the sculpture's carved texts (experiments 17 and 21) instead of K1-K3; one of the two alphabets is standard or KRYPTOS and the other the keyword mixing of a vocabulary word, since the full 63 x 63 pool over 570,000 offsets is beyond the budget.",
    "hypothesis_expert": (
        "Experiments 17 and 21 killed the sculpture's texts and Carter's book as running keys under 24 "
        "conventions; 45 killed K1-K3 under keyword-mixed alphabets. The remaining corner is these longer "
        "texts under mixed alphabets (C5, C7, C25). Sources: Carter volume one as scanned, the carved "
        "tableau by rows and columns, the Morse plaintexts, the right-hand panel, each forward and backward, "
        "every cyclic offset. Alphabet pairs: one side standard or KRYPTOS, the other any of the 61 keyword "
        "mixings, both ways round, with the key letters on the standard or KRYPTOS order and three modes. "
        "About 900 million trials with early exit at three mismatches. Bounds: complete for these texts and "
        "this restricted pool; both sides mixed is not covered."
    ),
    "hypothesis_eli5": (
        "Experiments 17 and 21 slid the sculpture's own texts and Howard Carter's book along the fourth "
        "message as a long secret word, using the sculpture's table, and found nothing. Here the table is "
        "rebuilt from each word the puzzle knows, on one side at a time, and the sliding is done again, "
        "forwards and backwards, at every starting point."
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
    import json
    from pathlib import Path
    from kryptos.ciphers import tableau_rows
    root = Path(__file__).resolve().parent
    carter = letters((root / "knowledge" / "sources" / "carter-1923-tomb-of-tutankhamen-vol1.txt").read_text(errors="ignore").upper())
    site = json.loads((root / "data" / "site_texts.json").read_text())
    rows = tableau_rows(carved=True)
    k1, k2, k3 = load_k1(), load_k2(), load_k3()
    k4 = letters((root / "data" / "k4.txt").read_text())
    morse = [letters(m.upper()) for m in site["morse"]]
    src = {"carter vol1": carter, "tableau rows": "".join(rows),
           "tableau columns": "".join(r[c] for c in range(max(len(r) for r in rows)) for r in rows if c < len(r)),
           "morse as carved": "".join(morse), "morse reversed order": "".join(reversed(morse)),
           "right panel K1-K4": letters(k1["ciphertext"]) + letters(k2["ciphertext_as_carved"]) + letters(k3["ciphertext"]) + k4}
    out = {}
    for name, t in src.items():
        out[name + " fwd"] = t; out[name + " bwd"] = t[::-1]
    return out


def _unused_sources():
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
    pairs = [(p_, c_) for p_ in pool for c_ in pool if p_ in ("std", "kry") or c_ in ("std", "kry")]
    for pname, cname in pairs:
        pa, ca = pool[pname], pool[cname]
        pidx = {ch: i for i, ch in enumerate(pa)}
        if True:
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
        "bounds": {"family": "running key from Carter and the sculpture texts, one alphabet keyword-mixed", "alphabet_pairs": len(pairs), "alphabets": len(pool), "key_alphabets": ["std", "kry"], "modes": 3,
                   "sources": {k: len(v) for k, v in src.items()}, "trials": trials, "stopped_by_clock": stopped,
                   "fewest_mismatches": near[0][0] if near else "more than 2",
                   "near_misses": [{"mismatches": a, "source": b, "plain": c, "cipher": d, "key": e, "mode": f_, "offset": g} for a, b, c, d, e, f_, g in near[:20]],
                   "survivors": len(candidates)},
        "notes": f"{trials} trials{' (stopped by the clock)' if stopped else ''}; {len(candidates)} survivors; {len(near)} within two mismatches.",
    }


def worked_example(ctx, key):
    pa, ca = keyword_mixed("BERLIN"), keyword_mixed("CLOCK")
    text = sources()["carter vol1 fwd"]
    lines = [f"plain alphabet BERLIN/keyword {pa}", f"cipher alphabet CLOCK/keyword {ca}", "key text: Carter volume one at offset 0, key letters on the standard order; Vigenere", "", "pos  plain  key  result  carved  match"]
    for pos in (22, 23, 24, 25, 64, 65):
        p = ctx.KNOWN[pos]; k = text[pos - 1]; c = ca[(pa.index(p) + STD.index(k)) % 26]
        lines.append(f"{pos:>3}    {p}     {k}     {c}       {ctx.K4[pos-1]}     {'yes' if c == ctx.K4[pos-1] else 'no'}")
    return "\n".join(lines)
