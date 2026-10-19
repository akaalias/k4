"""Positive control for F8/1 (issue #73): affine Hill solved letter by letter (0105).
0105 solves each row of (B, w) in p = B c + w mod 26 from every known letter (sizes 2-5, plain and affine, every
alignment, four numberings) and submits the decryption of every setting alive with spare equations. Its own
plant_check calls setting() directly on one alignment and numbering, not through run(), so it is not an own plant.
Here a 4x4 affine text (the case 0105 added) is planted; the planted setting must be submitted with the planted
plaintext. Candidates are not cut. 0105's encrypt() is a stub, so the plant makes its own ciphertext."""
import random
import sys

from kryptos.facts import KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F8/1"
EXPERIMENT = "0105"
WHAT = "Hill 4x4 affine (message block = B x carved block + w), KRYPTOS order 1-based (numbering 3), blocks from place 3 (alignment 2), random invertible B and random w, on English from Carter"
N, ALIGN, BASE = 4, 2, 1


def inv_mod_p(B, q):
    n = len(B)
    M = [[x % q for x in r] + [int(i == j) for j in range(n)] for i, r in enumerate(B)]
    for c in range(n):
        pr = next(i for i in range(c, n) if M[i][c])
        M[c], M[pr] = M[pr], M[c]
        iv = pow(M[c][c], q - 2, q)
        M[c] = [x * iv % q for x in M[c]]
        for i in range(n):
            if i != c and M[i][c]:
                f = M[i][c]
                M[i] = [(a - f * b) % q for a, b in zip(M[i], M[c])]
    return [r[n:] for r in M]


def inv26(B):
    i2, i13 = inv_mod_p(B, 2), inv_mod_p(B, 13)
    return [[(y + 13 * ((x - y) % 2)) % 26 for x, y in zip(r2, r13)] for r2, r13 in zip(i2, i13)]


def plant():
    a = sys.modules["attack"]
    rng = random.Random(7603)
    while True:
        B = [[rng.randrange(26) for _ in range(N)] for _ in range(N)]
        if a.invertible(B):
            break
    w = [rng.randrange(26) for _ in range(N)]
    Bi = inv26(B)
    pt = english_plant(7603)
    idx = {ch: (i + BASE) % 26 for i, ch in enumerate(KRY)}
    ct = list(pt)
    for s in range(ALIGN, 97 - N + 1, N):
        pv = [(idx[pt[s + k]] - w[k]) % 26 for k in range(N)]
        for r in range(N):
            ct[s + r] = KRY[(sum(Bi[r][k] * pv[k] for k in range(N)) - BASE) % 26]
    return {"plaintext": pt, "key": (B, w, "4x4 affine, align 2, numbering 3"), "ciphertext": "".join(ct)}


def found(result, plant):
    hit = [c for c in result.get("candidates", []) if c["plaintext"] == plant["plaintext"]
           and c["key"].startswith(f"Hill {N}x{N} affine align {ALIGN} numbering 3 ")]
    t = result.get("bounds", {}).get("by_size", {}).get("4x4 affine", {})
    return bool(hit), f"4x4 affine: {t.get('k4')}, copies alive {t.get('controls_alive')}; planted setting submitted with the planted text: {bool(hit)}"
