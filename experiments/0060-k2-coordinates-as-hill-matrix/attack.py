"""Experiment 0060. See program.md for the contract."""

EXPERIMENT = {
    "slug": "k2-coordinates-as-hill-matrix",
    "title": "The map reference at the end of K2, used as the number table of a Hill cipher",
    "family": "8-hill-polygraphic",
    "parent": "0015-hill-solved-from-crib-blocks",
    "changed": "Experiments 24 and 38 used the K2 coordinates as a repeating string of digits added to the letters. A Hill cipher needs a small table of numbers instead, and the coordinates are exactly a short list of numbers, so here they fill the table directly, in every reading, and the 24 known letters judge it.",
    "hypothesis_expert": (
        "C23(b): the K2 coordinates 38 57 6.5 N, 77 8 44 W as a matrix. Hill encryption (C21) with a key "
        "matrix filled from the coordinates: 2x2 from every window of four in the number lists [38, 57, 6, 5, "
        "77, 8, 44] and [38, 57, 65, 77, 8, 44] and the digit list 3 8 5 7 6 5 7 7 8 4 4, each forward and "
        "reversed, filled by rows or by columns; 3x3 from every window of nine; entries mod 26. Numberings "
        "A=0 and A=1 on the standard and KRYPTOS orders; every alignment; the matrix encrypting or "
        "decrypting (singular matrices skipped where an inverse is needed). Each setting decrypts K4 and the "
        "24 cribs are counted. Control: the same count for 2,000 random invertible matrices per size under "
        "the same settings. Bounds: exact for these readings."
    ),
    "hypothesis_eli5": (
        "K2 ends with a map reference: 38 degrees 57 minutes 6.5 seconds north, 77 degrees 8 minutes 44 "
        "seconds west. A Hill cipher mixes letters two or three at a time using a small square of numbers, "
        "and the map reference is a ready-made list of numbers. So we pour those numbers into the square in "
        "every sensible order, use it to unmix the copper, and count how many of the 24 known letters come "
        "out right. Random squares of numbers show what luck alone scores."
    ),
    "prediction": (
        "No coordinate matrix recovers more than four of the 24 known letters, the same as the best random "
        "matrices. Zero candidates pass."
    ),
    "method": (
        "1. List the coordinate readings. 2. Fill 2x2 and 3x3 matrices from every window, forward and "
        "reversed, by rows and columns. 3. For each numbering, alignment and direction, decrypt K4 and count "
        "crib hits. 4. Do the same with random invertible matrices. 5. Compare the best counts."
    ),
    "walkthrough": (
        "1. Take the first four numbers 38, 57, 6, 5 and reduce them mod 26: 12, 5, 6, 5. 2. Fill a 2x2 "
        "table by rows: top row 12 5, bottom row 6 5. 3. Number the letters A=0 to Z=25 and cut the copper "
        "into pairs from place 1. 4. Multiply each pair by the inverse of the table, mod 26, if the table "
        "has one (its determinant 12x5 - 5x6 = 30 = 4 mod 26 is even, so it has none and this reading can "
        "only encrypt). 5. Using the table to encrypt instead, look for the pair it would send to each "
        "carved pair. 6. Count how many of the 24 known letters land right."
    ),
}

import random
from itertools import product
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

NUMS = {"numbers": [38, 57, 6, 5, 77, 8, 44], "numbers with 65": [38, 57, 65, 77, 8, 44], "digits": [3, 8, 5, 7, 6, 5, 7, 7, 8, 4, 4]}
NUMBERINGS = {"std0": (STD, 0), "std1": (STD, 1), "kry0": (KRY, 0), "kry1": (KRY, 1)}


def det(M):
    if len(M) == 2:
        return (M[0][0] * M[1][1] - M[0][1] * M[1][0]) % 26
    a, b, c = M[0]; d, e, f = M[1]; g, h, i = M[2]
    return (a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)) % 26


def inv26(x):
    for y in range(26):
        if x * y % 26 == 1:
            return y
    return None


def inverse(M):
    n = len(M); dt = det(M); di = inv26(dt)
    if di is None:
        return None
    if n == 2:
        return [[M[1][1] * di % 26, -M[0][1] * di % 26], [-M[1][0] * di % 26, M[0][0] * di % 26]]
    cof = [[0] * 3 for _ in range(3)]
    for r in range(3):
        for c in range(3):
            m = [[M[i][j] for j in range(3) if j != c] for i in range(3) if i != r]
            cof[r][c] = ((-1) ** (r + c)) * (m[0][0] * m[1][1] - m[0][1] * m[1][0])
    return [[cof[c][r] * di % 26 for c in range(3)] for r in range(3)]


def apply(M, v):
    return [sum(M[r][c] * v[c] for c in range(len(v))) % 26 for r in range(len(M))]


def hill(text, M, alpha, base, offset):
    n = len(M); out = list(text)
    num = lambda ch: (alpha.index(ch) + base) % 26
    let = lambda v: alpha[(v - base) % 26]
    i = offset
    while i + n <= len(text):
        blk = apply(M, [num(ch) for ch in text[i:i + n]])
        for j in range(n):
            out[i + j] = let(blk[j])
        i += n
    return "".join(out)


def encrypt(plaintext, key):
    alpha, base = NUMBERINGS[key["numbering"]]
    return hill(plaintext, key["M"], alpha, base, key["offset"])


def matrices():
    out = []
    for name, seq in NUMS.items():
        for rev in (False, True):
            s = list(reversed(seq)) if rev else list(seq)
            for n in (2, 3):
                for i in range(len(s) - n * n + 1):
                    w = [x % 26 for x in s[i:i + n * n]]
                    rows = [w[r * n:(r + 1) * n] for r in range(n)]
                    cols = [[w[c * n + r] for c in range(n)] for r in range(n)]
                    for fill, M in (("rows", rows), ("columns", cols)):
                        out.append((f"{name}{' reversed' if rev else ''} window {i} by {fill}", M))
    return out


def score(ct, known, M):
    best = (0, None)
    Mi = inverse(M)
    for nname, (alpha, base) in NUMBERINGS.items():
        for o in range(len(M)):
            for direction, D in (("matrix decrypts", M), ("matrix encrypts", Mi)):
                if D is None:
                    continue
                pt = hill(ct, D, alpha, base, o)
                hits = sum(1 for p, ch in known.items() if pt[p - 1] == ch)
                if hits > best[0]:
                    best = (hits, (nname, o, direction, pt))
    return best


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    mats = matrices()
    results = []
    cands = []
    for name, M in mats:
        hits, info = score(ct, known, M)
        results.append((hits, name, M, info))
    results.sort(key=lambda r: -r[0])
    for hits, name, M, info in results[:5]:
        if info:
            nname, o, direction, pt = info
            enc_M = M if direction == "matrix encrypts" else inverse(M)
            if enc_M is not None:
                cands.append({"plaintext": pt, "key": {"numbering": nname, "M": enc_M, "offset": o}, "key_bits": 20,
                              "key_description": f"Hill from K2 coordinates, {name}, {nname}, offset {o}, {direction}"})
    rng = random.Random(60)
    ctl = {2: [], 3: []}
    for n in (2, 3):
        while len(ctl[n]) < 2000:
            M = [[rng.randrange(26) for _ in range(n)] for _ in range(n)]
            if inverse(M) is None:
                continue
            ctl[n].append(score(ct, known, M)[0])
            if ctx.time_left() < 120:
                break
    best = results[0]
    return {
        "candidates": cands,
        "bounds": {"family": "Hill with the key matrix filled from the K2 coordinates", "matrices": len(mats),
                   "numberings": list(NUMBERINGS), "directions": 2, "best_hits": best[0], "best_reading": best[1],
                   "top": [{"hits": h, "reading": nm} for h, nm, _, _ in results[:8]],
                   "control_best_2x2": max(ctl[2]) if ctl[2] else None, "control_best_3x3": max(ctl[3]) if ctl[3] else None,
                   "control_mean_2x2": round(sum(ctl[2]) / max(1, len(ctl[2])), 2), "control_mean_3x3": round(sum(ctl[3]) / max(1, len(ctl[3])), 2),
                   "control_matrices": {str(k): len(v) for k, v in ctl.items()}},
        "notes": (f"{len(mats)} coordinate matrices; best {best[0]}/24 known letters ({best[1]}). Random invertible matrices under the same settings: "
                  f"2x2 best {max(ctl[2]) if ctl[2] else None} (mean {sum(ctl[2]) / max(1, len(ctl[2])):.2f}), 3x3 best {max(ctl[3]) if ctl[3] else None} (mean {sum(ctl[3]) / max(1, len(ctl[3])):.2f})."),
    }


def worked_example(ctx, key):
    M = [[12, 5], [6, 5]]
    return f"first window 38 57 6 5 mod 26 = 12 5 6 5; by rows {M}; determinant {det(M)}; inverse {inverse(M)}"
