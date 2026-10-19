"""Positive control for F1.6 (issue #73): one carved letter wrong, through the exact free-alphabet tests (0147).
0147 built 604 variants of the copper (every other letter at each known place, and one letter in or out between
the runs) and decided each exactly for one free alphabet (added and Beaufort forms) and two free alphabets at key
lengths 1-26. Here K1/K2's own system (one alphabet, added form) is planted at length 9 and one carved letter at a
known place is then miscut; the variant that restores it must fit at length 9.
0147 first asserts that the copper it is given reproduces 0119's K4 results (no added-form fit; Beaufort at 23 and
26 only); those two K4 self-checks are skipped by PATCH, the search is unchanged. 0147's encrypt() is a stub, so
the plant makes its own ciphertext.
First run (result.failed-1.json, miscut at place 30): the plant fitted at length 9 in 298 variants against 0 on every
copy, but 0147 lists only the first 200 added-form fits (of 4,978), in place order, so the restoring variant at 30 was
cut off. Rerun with the miscut at place 22 and the first seed from 7371 whose planted letter there is A: the restoring
variant 'sub 22 x->A' is then the first listed. The search is unchanged."""
import random

from kryptos.plants import english_plant

ITEM = "F1.6"
EXPERIMENT = "0147"
WHAT = "Quagmire III, added form, random alphabet, key length 9, then the carved letter at place 22 miscut to another letter, on English from Carter"
L, PLACE = 9, 22
PATCH = [
    ('    assert [L for L in range(1, 27) if m0120.decide(eqs_for(base_eq, L), "V", rng0)[0] == "fit"] == []\n', ''),
    ('    assert [L for L in range(1, 27) if m0120.decide(eqs_for(base_eq, L), "B", rng0)[0] == "fit"] == [23, 26]\n', ''),
]


def plant():
    seed = 7371
    while True:
        p = _plant(seed)
        if p["true"] == "A":
            return p
        seed += 1


def _plant(seed):
    rng = random.Random(seed)
    X = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"); rng.shuffle(X)
    k = [rng.randrange(26) for _ in range(L)]
    pt = english_plant(7371)
    ct = [X[(X.index(ch) + k[i % L]) % 26] for i, ch in enumerate(pt)]
    true = ct[PLACE - 1]
    ct[PLACE - 1] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[("ABCDEFGHIJKLMNOPQRSTUVWXYZ".index(true) + 7) % 26]
    return {"plaintext": pt, "key": ("".join(X), k, f"place {PLACE} miscut {true}->{ct[PLACE - 1]}"), "ciphertext": "".join(ct), "true": true}


def found(result, plant):
    b = result.get("bounds", {})
    want = f"sub {PLACE} {plant['ciphertext'][PLACE - 1]}->{plant['true']}"
    hit = [f for f in b.get("k4_added_form_fits", []) if f["variant"] == want and f["length"] == L]
    return bool(hit), (f"added-form fits {b.get('k4_added_form_fit_count')}; the restoring variant '{want}' at {L}: {bool(hit)}; "
                       f"cells above every copy {b.get('cells_k4_above_every_copper')}")
