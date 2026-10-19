"""Positive control for F6/5 (issue #73): one carved letter extra, then a move (0094).
0094 struck each carved letter outside the known places (a 96-letter text) or inserted an unknown at each place
(98 letters), ran its type-1 library on that length with a periodic key 1-26 after or before on 8 tableau classes, and
listed K4's variants live below 20 (none); here a 96-letter message moved and keyed, with one letter cut in by mistake
at carved place 51, must be listed as "delete at 51" at period 7, order A, class kry/kry, and period 7's count must stand
above every copy. 0094 does not report the move, only the variant, so the plant is identified by its variant, order,
class and period; strikes next to place 51 that no known letter's landing separates may be listed too.
0094's encrypt() is a stub, so the plant makes its own ciphertext with 0094's own rot()."""
import random
import sys

from kryptos.facts import KRYPTOS_ALPHABET as KRY
from kryptos.plants import english_plant

ITEM = "F6/5"
EXPERIMENT = "0094"
WHAT = "English from Carter with letter 51 removed (96 letters), a clockwise quarter turn in rows of 10, a random period-7 key on the KRYPTOS table, Vigenere, then an extra letter cut in at carved place 51"
W, L, J = 10, 7, 50          # J: 0-based carved place of the extra letter


def plant():
    a = sys.modules["attack"]
    rng = random.Random(7415)
    pt = english_plant(7415)
    msg = pt[:J] + pt[J + 1:]                       # the 96-letter message; known letters 64-74 now at 63-73
    sigma = a.rot(list(range(96)), W, True)         # moved[j] = msg[sigma[j]]
    k = [rng.randrange(26) for _ in range(L)]
    c96 = [KRY[(KRY.index(msg[i]) + k[j % L]) % 26] for j, i in enumerate(sigma)]
    ct = c96[:J] + [rng.choice(KRY)] + c96[J:]
    return {"plaintext": pt, "key": (f"96 letters, turn cw {W}", "order A", "kry/kry vig", k, f"extra letter at {J + 1}"), "ciphertext": "".join(ct)}


def found(result, plant):
    b = result.get("bounds", {})
    low = b.get("k4_live_below_20", [])
    hit = [e for e in low if e["variant"] == f"delete at {J + 1}" and e["n"] == 96 and e["order"] == "A"
           and e["class"] == "kry/kry/vig-var" and e["period"] == L]
    n, mx = b.get("k4_live_by_period", {}).get("A", [0] * 26)[L - 1], b.get("controls_live_by_period_max", {}).get("A", [0] * 26)[L - 1]
    return bool(hit) and n > mx, (f"variants live below 20: {b.get('n_k4_live_below_20')} ({sorted({e['variant'] for e in low})[:6]}); "
                                  f"'delete at {J + 1}' at {L}, order A: {bool(hit)}; live at {L}: {n}, copies' max {mx}; "
                                  f"variants done {b.get('variants_done')} of {b.get('variants')}")
