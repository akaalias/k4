"""Experiment 0017. See program.md for the contract."""

EXPERIMENT = {
    "slug": "running-key-from-the-sculpture-itself",
    "title": "A running key read off the sculpture: the carved tableau, the Morse, and the whole right-hand panel",
    "family": "1-keyed-periodic",
    "parent": "0004-running-key-from-k1-k3",
    "changed": "Key sources are the sculpture's own carved texts rather than the K1-K3 solutions: the tableau read by rows and by columns, the Morse plaintexts, and the four ciphertexts as one panel. Family 1 re-entered with a new key source, as its parked status requires.",
    "hypothesis_expert": (
        "Scheidt: 'the keys were concealed at the sculpture' (C6); the Morse and the tableau are the texts "
        "concealed there in plain sight (C9, C25). 0004 slid the K1-K3 plaintexts and ciphertexts past K4 "
        "under 24 conventions and found nothing. Here the sources are: the carved tableau as 26 rows of 30 "
        "letters plus the extra L, read row by row and column by column; the left-hand index column plus "
        "the rows; the seven Morse plaintexts as carved and in reverse order; the right-hand panel's four "
        "ciphertexts as one 869-letter text; each forward and backward, at every cyclic offset, under the "
        "24 conventions, scored by crib mismatches. Zero mismatches is a survivor and is decrypted; one "
        "or two mismatches are reported for the one-letter-error reading (C17). About 200,000 trials; "
        "chance survival per trial is 26 to the minus 24. Bounds: complete for these sources."
    ),
    "hypothesis_eli5": (
        "A running key is a long text used as the secret, one letter per message letter, so the key is as "
        "long as the message. The designer said the keys were hidden at the sculpture. The sculpture "
        "carries plenty of text: the big table of shifted alphabets, the Morse code messages on the stones "
        "outside, and the three solved messages. We slide each of those texts along the fourth message "
        "at every possible starting point and ask whether any position explains all 24 known letters."
    ),
    "prediction": (
        "No source, direction, offset or convention explains all 24 known letters. The best trial has "
        "no fewer than 5 mismatches, which is what chance gives among 200,000 trials. Zero candidates pass."
    ),
    "method": (
        "1. Build the key texts from data/site_texts.json and the K1-K4 ciphertexts, letters only. "
        "2. For each text, each direction, each convention and each cyclic offset, encrypt the 24 known "
        "plaintext letters with the key letters at their positions and count mismatches against the carved "
        "letters. 3. Keep the best few trials. 4. Decrypt and submit any zero-mismatch trial."
    ),
    "walkthrough": (
        "1. Take the tableau read row by row: KRYPTOSABCDEFGHIJLMNQUVWXZKRYP, then RYPTOSABCD..., and so on. "
        "2. Choose an offset, say 0, so key letter 1 is K, key letter 2 is R, and so on. 3. Position 22 of "
        "the message is E; its key letter is the 22nd letter of the text, H. 4. Under the sculpture's "
        "alphabet and Vigenere, E shifted by H should give the carved F; it gives something else, so count "
        "one mismatch. 5. Do this for all 24 known letters. 6. Slide the offset by one and repeat, "
        "through the whole text, forward and backward, under each way of using the table."
    ),
}

import json
from pathlib import Path
from kryptos.alphabets import conventions, encrypt_letter, decrypt_letter
from kryptos.ciphers import tableau_rows
from kryptos.facts import load_k1, load_k2, load_k3, STANDARD_ALPHABET as STD

N = 97
DATA = Path(__file__).resolve().parent / "data"


def letters(s):
    return "".join(c for c in s.upper() if "A" <= c <= "Z")


def sources():
    site = json.loads((DATA / "site_texts.json").read_text())
    rows = tableau_rows(carved=True)
    src = {}
    src["tableau rows"] = "".join(rows)
    src["tableau rows with index column"] = "".join(STD[i] + r for i, r in enumerate(rows))
    width = max(len(r) for r in rows)
    src["tableau columns"] = "".join(r[c] for c in range(width) for r in rows if c < len(r))
    morse = [letters(m) for m in site["morse"]]
    src["morse as carved"] = "".join(morse)
    src["morse reversed order"] = "".join(reversed(morse))
    k1, k2, k3 = load_k1(), load_k2(), load_k3()
    k4 = letters(Path(DATA / "k4.txt").read_text())
    src["right panel ciphertexts K1-K4"] = letters(k1["ciphertext"]) + letters(k2["ciphertext_as_carved"]) + letters(k3["ciphertext"]) + k4
    out = {}
    for name, t in src.items():
        out[name + " fwd"] = t
        out[name + " bwd"] = t[::-1]
    return out


def encrypt(plaintext, key):
    text = sources()[key["source"]]
    n = len(text); o = key["offset"]
    pa, ca, ka, m = key["pa"], key["ca"], key["ka"], key["m"]
    return "".join(encrypt_letter(p, text[(o + i) % n], pa, ca, ka, m) for i, p in enumerate(plaintext))


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    src = sources()
    trials = 0
    best = []   # (mismatches, name, conv, offset)
    candidates = []
    for name, text in src.items():
        n = len(text)
        for conv in conventions():
            pa, ca, ka, m = conv
            for o in range(n):
                trials += 1
                mism = 0
                for pos, p in known.items():
                    if encrypt_letter(p, text[(o + pos - 1) % n], pa, ca, ka, m) != ct[pos - 1]:
                        mism += 1
                        if mism > 3:
                            break
                if mism <= 3:
                    best.append((mism, name, "/".join(conv), o))
                if mism == 0:
                    key = {"source": name, "offset": o, "pa": pa, "ca": ca, "ka": ka, "m": m}
                    pt = "".join(decrypt_letter(ct[i], text[(o + i) % n], pa, ca, ka, m) for i in range(N))
                    candidates.append({"plaintext": pt, "key": key, "key_bits": 20, "key_description": f"running key {name} offset {o}, {pa}/{ca}/{ka} {m}"})
        if ctx.time_left() < 30:
            break
    best.sort()
    return {
        "candidates": candidates[:50],
        "bounds": {"family": "running key from the sculpture's own texts", "sources": {k: len(v) for k, v in src.items()},
                   "conventions": 24, "offsets": "all cyclic", "trials": trials,
                   "fewest_mismatches": best[0][0] if best else "more than 3",
                   "trials_with_at_most_3_mismatches": [{"mismatches": a, "source": b, "convention": c, "offset": d} for a, b, c, d in best[:20]],
                   "survivors": len(candidates)},
        "notes": f"{trials} trials; {len(candidates)} zero-mismatch survivors; {len(best)} trials with three or fewer mismatches.",
    }


def worked_example(ctx, key):
    text = sources()["tableau rows fwd"]
    lines = ["key text: tableau rows, offset 0, KRYPTOS alphabet throughout, Vigenere", "", f"key text begins {text[:40]}...", "", "pos  plain  key letter  E+key  carved  match"]
    for pos in (22, 23, 24, 25, 64, 65):
        p = ctx.KNOWN[pos]; k = text[pos - 1]; c = encrypt_letter(p, k, "kry", "kry", "kry", "vig")
        lines.append(f"{pos:>3}    {p}        {k}         {c}      {ctx.K4[pos-1]}     {'yes' if c == ctx.K4[pos-1] else 'no'}")
    return "\n".join(lines)
