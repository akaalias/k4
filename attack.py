"""Experiment 0032. See program.md for the contract."""

EXPERIMENT = {
    "slug": "row-keyed-grids-one-key-letter-per-row",
    "title": "Sanborn's matrix with a key letter per row: write the message in rows of width w, encipher each row with one letter of the key",
    "family": "6-transposition-then-tableau",
    "parent": "0026-double-keyed-columnar-then-tableau",
    "changed": "Not a transposition this time but a grid-shaped key: every letter in a row shares one key letter, and the rows take the key word's letters in turn. A column-shaped key is an ordinary periodic key and is dead; the row-shaped one was never swept.",
    "hypothesis_expert": (
        "Sanborn's 'matrix code' is text written in rows and read another way (C1). A natural hand variant "
        "keeps the reading order and keys by row: position i takes key letter key[(i div w) mod L], so all w "
        "letters of a row share one key letter and rows cycle through the word. EASTNORTHEAST occupies 13 "
        "consecutive positions, so for w up to 13 at least one row holds several cribs that must force the "
        "same key letter, with chance 26 to the minus (k - 1) for k cribs in a row; the row-length L then adds "
        "collisions between rows. Swept: w = 2 to 48, L = 1 to 48, plain and cipher alphabets from the "
        "standard, KRYPTOS and keyword-mixed vocabulary alphabets (63), three modes; the key alphabet drops "
        "out of the consistency test. Survivors with a short L have their forced key read in the standard "
        "and KRYPTOS alphabets and matched against the vocabulary and K1-K3 windows. Bounds: complete for "
        "these widths, lengths and alphabets."
    ),
    "hypothesis_eli5": (
        "Imagine writing the message in a grid, say seven letters per line, and putting one letter of a "
        "secret word beside each line: every letter on that line is shifted by that one letter. The 13 "
        "known letters of EASTNORTHEAST fill a whole line or two, and every letter on a line must agree on "
        "the shift. We try every line width and every secret-word length, with every table the puzzle's "
        "words can build, and see whether the known letters ever agree."
    ),
    "prediction": (
        "No width up to 13 survives under any alphabet pair, because a row full of cribs disagrees. Widths "
        "above 13 survive only where no row holds two cribs with different shifts, and then only for key "
        "lengths that avoid pairing the two crib runs; no forced key matches a word. Zero candidates pass."
    ),
    "method": (
        "1. Build the alphabet pool. 2. For each plain alphabet, cipher alphabet and mode, compute the forced "
        "key index at each crib. 3. For each width w, group cribs by row and reject on disagreement within a "
        "row. 4. For surviving widths, for each key length L, group rows by L and reject on disagreement. "
        "5. Read surviving forced keys in the standard and KRYPTOS alphabets; match against the vocabulary."
    ),
    "walkthrough": (
        "1. Width 7: the rows are positions 1-7, 8-14, 15-21, 22-28, 29-35, and so on. 2. Row 22-28 holds E A S "
        "T N O R against the carved F L R V Q Q P. 3. On the plain alphabet with Vigenere, E to F is a shift "
        "of 1, A to L a shift of 11: the row cannot have one key letter, so width 7 is dead for this alphabet. "
        "4. Width 20: rows 21-40 and 61-80; the first holds 13 cribs, the second 11; each row must agree "
        "internally. 5. Try every alphabet the puzzle's words build; a surviving width then gets every key "
        "length tried, which ties rows together."
    ),
}

from kryptos.alphabets import keyword_mixed
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY, load_k1, load_k2, load_k3

N = 97
MODES = {"vig": lambda p, c: (c - p) % 26, "beau": lambda p, c: (c + p) % 26, "varbeau": lambda p, c: (p - c) % 26}
ENC = {"vig": lambda p, k: (p + k) % 26, "beau": lambda p, k: (k - p) % 26, "varbeau": lambda p, k: (p - k) % 26}
DEC = {"vig": lambda c, k: (c - k) % 26, "beau": lambda c, k: (k - c) % 26, "varbeau": lambda c, k: (c + k) % 26}


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


def encrypt(plaintext, key):
    pa, ca, ka, m, w, k = key["pa"], key["ca"], key["ka"], key["m"], key["w"], key["key"]
    return "".join(ca[ENC[m](pa.index(p), ka.index(k[(i // w) % len(k)]))] for i, p in enumerate(plaintext))


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    vocab = list(ctx.vocabulary)
    pool = pool_of(vocab)
    index = {n: {ch: i for i, ch in enumerate(A)} for n, A in pool.items()}
    texts = [letters(load_k1()["plaintext"]), letters(load_k2()["plaintext_as_carved"]), letters(load_k3()["plaintext"])]
    crib_pos = sorted(known)
    width_surv = {}      # w -> count of (pa, ca, m) surviving the row test
    full_surv = []       # (w, L, pa, ca, m, slots)
    candidates = []
    cases = 0
    for pname, pa in pool.items():
        pidx = index[pname]
        for cname, ca in pool.items():
            cidx = index[cname]
            for m, f in MODES.items():
                forced = [(pos - 1, f(pidx[known[pos]], cidx[ct[pos - 1]])) for pos in crib_pos]
                for w in range(2, 49):
                    cases += 1
                    rows = {}
                    ok = True
                    for i, k in forced:
                        r = i // w
                        if r in rows and rows[r] != k:
                            ok = False; break
                        rows[r] = k
                    if not ok:
                        continue
                    width_surv[w] = width_surv.get(w, 0) + 1
                    for L in range(1, 49):
                        slots = {}
                        ok2 = True
                        for r, k in rows.items():
                            s = r % L
                            if s in slots and slots[s] != k:
                                ok2 = False; break
                            slots[s] = k
                        if not ok2:
                            continue
                        full_surv.append((w, L, pname, cname, m, slots))
                        if L <= 30 and len(slots) >= 3:
                            for ka_name in ("std", "kry"):
                                A = pool[ka_name]
                                wordpool = set(x for x in vocab if len(x) == L)
                                for t in texts:
                                    for i in range(0, len(t) - L + 1):
                                        wordpool.add(t[i:i + L])
                                for kw in wordpool:
                                    if all(A.index(kw[s]) == k for s, k in slots.items()):
                                        key = {"pa": pa, "ca": ca, "ka": A, "m": m, "w": w, "key": kw}
                                        pt = "".join(pa[DEC[m](cidx[c], A.index(kw[(i // w) % L]))] for i, c in enumerate(ct))
                                        candidates.append({"plaintext": pt, "key": key, "key_bits": 4.7 * L + 6, "key_description": f"rows of {w}, key {kw} per row; {pname}/{cname}/{ka_name} {m}"})
        if ctx.time_left() < 30:
            break
    by_L = {}
    for w, L, *_ in full_surv:
        by_L[L] = by_L.get(L, 0) + 1
    return {
        "candidates": candidates[:50],
        "bounds": {"family": "grid with one key letter per row, rows cycling through a key word", "widths": "2-48", "key_lengths": "1-48",
                   "alphabets": len(pool), "modes": 3, "cases": cases,
                   "widths_surviving_row_test": {str(w): n for w, n in sorted(width_surv.items())},
                   "smallest_width_surviving": min(width_surv) if width_surv else None,
                   "survivors_by_key_length": {str(L): n for L, n in sorted(by_L.items())},
                   "vocab_matches": len(candidates)},
        "notes": f"{cases} (alphabet pair, mode, width) cases. Widths surviving the row test: {sorted(width_surv)}. Survivors by key length (first 12): {dict(list(sorted(by_L.items()))[:12])}. {len(candidates)} matches.",
    }


def worked_example(ctx, key):
    lines = ["width 7, plain alphabet for both message and carved letters, Vigenere: shifts within row 22-28", "", "pos  plain  carved  shift"]
    for pos in range(22, 29):
        p, c = ctx.KNOWN[pos], ctx.K4[pos - 1]
        lines.append(f"{pos:>3}    {p}      {c}      {(STD.index(c) - STD.index(p)) % 26:>2}")
    lines.append("")
    lines.append("one row, seven different shifts: width 7 cannot have one key letter per row under this alphabet.")
    return "\n".join(lines)
