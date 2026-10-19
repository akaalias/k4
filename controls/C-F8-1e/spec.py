"""Positive control for F8/1 (issue #73): Hill with a periodic key (0116).
0116 solves p = B c + u_kappa mod 26 (kappa = block start mod L) row by row for sizes 2-4, key lengths 1-26, every
alignment, four numberings, and reports which settings stay alive on the text and on 10 shuffled copies; it lists
no candidates. Its plant_check calls setting() directly, not through run(), so it is not an own plant. Here a 3x3
text with key length 6 is planted (on the plant this setting has 9 spare equations; a period-4 plant at 3x3 was
open); the planted setting must be alive with checks and its cell above every copy. k4_alive is cut at 30 in
(size, key length) order; only 2x2 and 3x3 with L < 6 come before (K4 and every copy: none alive; the plant: 2),
so the plant cannot be cut off.
0116's encrypt() is a stub, so the plant makes its own ciphertext."""
import random
import sys

from kryptos.facts import KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F8/1"
EXPERIMENT = "0116"
WHAT = "Hill 3x3 then a period-6 key (message block = B x carved block + u[start mod 6]), KRYPTOS order 0-based (numbering 2), blocks from place 2 (alignment 1), random invertible B and random u, on English from Carter"
N, L, ALIGN, NUM, BASE = 3, 6, 1, 2, 0


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
    rng = random.Random(7604)
    while True:
        B = [[rng.randrange(26) for _ in range(N)] for _ in range(N)]
        if a.invertible(B):
            break
    U = {k: [rng.randrange(26) for _ in range(N)] for k in range(L)}
    Bi = inv26(B)
    pt = english_plant(7604)
    idx = {ch: (i + BASE) % 26 for i, ch in enumerate(KRY)}
    ct = list(pt)
    for s in range(ALIGN, 97 - N + 1, N):
        u = U[s % L]
        pv = [(idx[pt[s + k]] - u[k]) % 26 for k in range(N)]
        for r in range(N):
            ct[s + r] = KRY[(sum(Bi[r][k] * pv[k] for k in range(N)) - BASE) % 26]
    return {"plaintext": pt, "key": (B, U, "3x3, L=6, align 1, numbering 2"), "ciphertext": "".join(ct)}


def found(result, plant):
    b = result.get("bounds", {})
    hit = [s for s in b.get("k4_alive", []) if (s["n"], s["L"], s["align"], s["numbering"]) == (N, L, ALIGN, NUM) and s["checks"] > 0]
    cell = b.get("by_size_and_key_length", {}).get(f"{N}x{N} L={L}", {})
    alive = cell.get("k4", {}).get("alive", 0)
    above = alive > max(cell.get("controls_alive", [0]) or [0])
    return bool(hit) and above, f"planted setting alive with checks: {hit[:1]}; cell 3x3 L=6 {cell.get('k4')}, copies alive {cell.get('controls_alive')}; alive in total {b.get('n_k4_alive')}"
