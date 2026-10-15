"""Experiment 0021. See program.md for the contract."""

EXPERIMENT = {
    "slug": "running-key-from-carter-tomb-of-tutankhamen",
    "title": "A running key from Howard Carter's book: the text K3 paraphrases, slid past K4 at every offset",
    "family": "1-keyed-periodic",
    "parent": "0017-running-key-from-the-sculpture-itself",
    "changed": "Key source is Carter's The Tomb of Tut-ankh-Amen, volume one, the book K3 paraphrases, instead of the sculpture's own texts. About 330,000 letters, both directions, every offset.",
    "hypothesis_expert": (
        "Sanborn: 'I have left instructions in the earlier text that refer to later text' and the K1-K3 answers "
        "'contain clues to the fourth' (C7); K3 is Carter's account of opening the tomb, paraphrased, and the "
        "misspelt DESPARATLY and the 'can you see anything' line point at the book itself "
        "(knowledge/sources/carter-1923-tomb-of-tutankhamen-vol1.txt, an OCR scan). A running key from a "
        "printed book is the classic 1900-1945 hand system Scheidt taught (C5). Test: the book's letters, "
        "forward and backward, at every offset, under the 24 conventions, scored by crib mismatches; zero "
        "mismatches is a survivor and is decrypted; one or two are reported for the one-letter-error "
        "reading (C17) and for OCR damage. About 16 million trials; chance survival is 26 to the minus 24 "
        "each, and a near miss at two mismatches has chance about 10 to the minus 28 per trial. Bounds: "
        "complete for this text as scanned, both directions."
    ),
    "hypothesis_eli5": (
        "The third message retells the moment Howard Carter first looked into Tutankhamun's tomb. The "
        "artist has said the earlier messages hold instructions for the last one. One old trick is to use "
        "a book as the key: line the book's letters up under the message and add them. We take Carter's "
        "own book, every page of it, and slide it along the fourth message at every possible starting "
        "point, forwards and backwards, asking whether any position explains all 24 known letters."
    ),
    "prediction": (
        "No offset in either direction explains all 24 known letters, and none comes within two. The "
        "best trial has four or more mismatches, which is chance among 16 million trials. Zero candidates pass."
    ),
    "method": (
        "1. Strip the scan to letters A-Z. 2. For each direction, convention and offset, encrypt the 24 known "
        "plaintext letters with the book letters at their positions and count mismatches against the carved "
        "letters, stopping at the third mismatch. 3. Keep every trial with two or fewer mismatches. "
        "4. Decrypt and submit any zero-mismatch trial."
    ),
    "walkthrough": (
        "1. Open the book at any point, say the words THE TOMB OF TUT ANKH AMEN, and write its letters under "
        "the message starting at position 1: T under O, H under B, E under K, and so on. 2. Position 22 of the "
        "message is E; the book letter under it is the 22nd letter from where you opened. 3. On the sculpture's "
        "table, find the row of that book letter and the column of E; the letter there should be the carved F. "
        "4. If it is not, count one miss and go on to the next known letter. 5. After three misses, give up "
        "on this opening and move the book one letter along. 6. Do this for every opening in the book, "
        "then with the book read backwards."
    ),
}

from pathlib import Path
from kryptos.alphabets import conventions, encrypt_letter, decrypt_letter

N = 97
SRC = Path(__file__).resolve().parent / "knowledge" / "sources" / "carter-1923-tomb-of-tutankhamen-vol1.txt"


def letters(s):
    return "".join(c for c in s.upper() if "A" <= c <= "Z")


def sources():
    t = letters(SRC.read_text(errors="ignore"))
    return {"carter vol1 fwd": t, "carter vol1 bwd": t[::-1]}


def encrypt(plaintext, key):
    text = sources()[key["source"]]
    n = len(text); o = key["offset"]
    pa, ca, ka, m = key["pa"], key["ca"], key["ka"], key["m"]
    return "".join(encrypt_letter(p, text[(o + i) % n], pa, ca, ka, m) for i, p in enumerate(plaintext))


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    src = sources()
    crib = sorted(known.items())
    trials = 0
    near = []
    candidates = []
    for name, text in src.items():
        n = len(text)
        for conv in conventions():
            pa, ca, ka, m = conv
            table = {(p, k): encrypt_letter(p, k, pa, ca, ka, m) for p in set(known.values()) for k in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
            for o in range(n):
                trials += 1
                mism = 0
                for pos, p in crib:
                    if table[(p, text[(o + pos - 1) % n])] != ct[pos - 1]:
                        mism += 1
                        if mism > 2:
                            break
                if mism <= 2:
                    near.append((mism, name, "/".join(conv), o, text[o:o + 40]))
                    if mism == 0:
                        key = {"source": name, "offset": o, "pa": pa, "ca": ca, "ka": ka, "m": m}
                        pt = "".join(decrypt_letter(ct[i], text[(o + i) % n], pa, ca, ka, m) for i in range(N))
                        candidates.append({"plaintext": pt, "key": key, "key_bits": 25, "key_description": f"running key {name} offset {o}, {pa}/{ca}/{ka} {m}"})
            if ctx.time_left() < 30:
                break
    near.sort()
    return {
        "candidates": candidates[:50],
        "bounds": {"family": "running key from Carter 1923 vol. 1 (OCR scan)", "letters": {k: len(v) for k, v in src.items()},
                   "conventions": 24, "trials": trials, "fewest_mismatches": near[0][0] if near else "more than 2",
                   "near_misses": [{"mismatches": a, "source": b, "convention": c, "offset": d, "key_text": e} for a, b, c, d, e in near[:20]],
                   "survivors": len(candidates)},
        "notes": f"{trials} trials; {len(candidates)} survivors; {len(near)} trials within two mismatches.",
    }


def worked_example(ctx, key):
    text = sources()["carter vol1 fwd"]
    i = max(text.find("TOMBOFTUT"), 0)
    lines = [f"book opened at letter {i}: {text[i:i+50]}", "", "pos  plain  book letter  E+key  carved  match"]
    for pos in (22, 23, 24, 25, 64, 65):
        p = ctx.KNOWN[pos]; k = text[i + pos - 1]; c = encrypt_letter(p, k, "kry", "kry", "kry", "vig")
        lines.append(f"{pos:>3}    {p}        {k}          {c}      {ctx.K4[pos-1]}     {'yes' if c == ctx.K4[pos-1] else 'no'}")
    return "\n".join(lines)
