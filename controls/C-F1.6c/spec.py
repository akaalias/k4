"""Positive control for F1.6 (issue #73): one carved letter wrong, through Hill (0151).
0151 ran 0105's exact Hill solver (sizes 2-5, plain and affine, every alignment, four numberings) on all 5,044
single-letter variants of the copper and lists settings alive with spare equations. Here a 2x2 Hill text is
planted (numbering A=0, blocks from place 1) and one carved letter at a known place miscut; the restoring variant
must be alive with checks. 0151 lists only its first 50 live settings, in its own chunk order, and K4 alone gives
about 250 one-check survivors, so the miscut is placed where the restoring variant falls in chunk 0 (index
divisible by 64); the search is unchanged. First run errored (seed 7373 has no qualifying place); the plant now
takes the first seed from 7373 that has one. 0151's encrypt() is a stub, so the plant makes its own ciphertext."""
import random

from kryptos.facts import STANDARD_ALPHABET as STD, KNOWN
from kryptos.plants import english_plant

ITEM = "F1.6"
EXPERIMENT = "0151"
WHAT = "Hill 2x2 (plaintext = B x carved block mod 26, A=0, blocks from place 1), random invertible B, then one carved letter at a known place miscut, on English from Carter"


def inv2(B):
    det = (B[0][0] * B[1][1] - B[0][1] * B[1][0]) % 26
    di = pow(det, -1, 26)
    return [[(B[1][1] * di) % 26, (-B[0][1] * di) % 26], [(-B[1][0] * di) % 26, (B[0][0] * di) % 26]]


def plant():
    seed = 7373
    while True:
        p = _plant(seed)
        if p:
            return p
        seed += 1


def _plant(seed):
    rng = random.Random(seed)
    while True:
        B = [[rng.randrange(26) for _ in range(2)] for _ in range(2)]
        det = (B[0][0] * B[1][1] - B[0][1] * B[1][0]) % 26
        if det % 2 and det % 13:
            break
    Bi = inv2(B)
    pt = english_plant(7373)
    ct = list(pt)                      # place 97 stands alone (no block); left as the plaintext letter
    for s in range(0, 96, 2):
        p = [STD.index(pt[s]), STD.index(pt[s + 1])]
        for r in range(2):
            ct[s + r] = STD[(Bi[r][0] * p[0] + Bi[r][1] * p[1]) % 26]
    for q in sorted(KNOWN):            # the first known place and miscut letter whose restoring variant lands in chunk 0
        true = ct[q - 1]
        for bad in STD:
            if bad == true:
                continue
            rank = STD.index(true) - (1 if STD.index(bad) < STD.index(true) else 0)
            if ((q - 1) * 25 + rank) % 64 == 0:
                ct[q - 1] = bad
                return {"plaintext": pt, "key": (B, f"place {q} miscut {true}->{bad}"), "ciphertext": "".join(ct), "true": true, "place": q}
    return None                        # no known place qualifies for this seed: the next seed is tried


def found(result, plant):
    b = result.get("bounds", {})
    q = plant["place"]
    want = f"sub {q} {plant['ciphertext'][q - 1]}->{plant['true']}"
    hit = [h for h in b.get("hill_alive_with_checks", []) if h["variant"] == want and h["n"] == 2 and h["align"] == 0 and h["numbering"] == 0]
    return bool(hit), f"Hill alive with checks {b.get('n_hill_alive_with_checks')}; '{want}' as 2x2: {hit[:2]}"
