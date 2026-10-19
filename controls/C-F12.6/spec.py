"""Positive control for F12.6 (issue #73): probable words placed in the undecided free-alphabet cells (0172).
0172 placed 60 common and K1-K3 words at every position (3,634 placements) in ten cells the 24 known letters leave
undecided (one free alphabet, Beaufort, lengths 23 and 26; two free alphabets at 8 lengths), decided each placement
exactly, and compared the number consistent on K4 with 10 copies that keep the 24 carved letters at the known places
and shuffle the rest; K4 stood above every copy in 1 of 10 cells (chance). Here the text is Quagmire IV at length 8
(two free alphabets, the cell with the fewest consistent placements on K4), so the cell "two free 8" must stand
above every copy, which is how 0172 would have flagged K4's answer. The plaintext holds 5 of the placements
(THE@89, WHICH@13, THEIR@89, INTO@50, CAN@81); the seed is the first of the block, not chosen by outcome.
k4_examples lists only the first 20 consistent placements in word order, so a true placement may be cut off; found()
therefore does not require one listed and only reports it.
PATCH: 0172 first asserts that K4 fits each of its ten cells (K4's own recorded state); a planted text fits only
some (the plant is dead in 3 of the 10), so the assert is replaced by the same decide() call without the assert,
which keeps the random stream (and so the copies) as 0172 draws them. The search is unchanged.
BUDGET 3600: 0172 ran 1,737 s against 1,800 and stops placements 90 s before the budget; the larger budget lets
every placement finish. 0172's encrypt() is a stub, so the plant makes its own ciphertext."""
import random

from kryptos.plants import english_plant

ITEM = "F12.6"
EXPERIMENT = "0172"
WHAT = ("Quagmire IV (two random free alphabets, added form), key length 8 with random shifts, on English from Carter: "
        "the cell 'two free 8' must count more consistent probable-word placements than every copy")
BUDGET = 3600
PATCH = [('        assert decide(cell, ct, known, L, m0120, m0123, rng) == "fit", (cell, L)\n',
          '        decide(cell, ct, known, L, m0120, m0123, rng)\n')]
L = 8
SEED = 7525
CELL = f"two free {L}"
STD = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def plant():
    rng = random.Random(SEED)
    P = list(STD); rng.shuffle(P)
    C = list(STD); rng.shuffle(C)
    k = [rng.randrange(26) for _ in range(L)]
    pt = english_plant(SEED)
    ct = "".join(C[(P.index(ch) + k[i % L]) % 26] for i, ch in enumerate(pt))
    return {"plaintext": pt, "key": ("".join(P), "".join(C), k), "ciphertext": ct}


def found(result, plant):
    b = result.get("bounds", {})
    s = b.get("summary", {}).get(CELL, {})
    pt = plant["plaintext"]
    listed = [e for e in s.get("k4_examples", []) if pt[int(e.split("@")[1]) - 1:].startswith(e.split("@")[0])]
    ok = bool(s.get("k4_above_every_copy"))
    return ok, (f"{CELL}: plant {s.get('k4_consistent')} consistent placements, copies {s.get('coppers_consistent')}; "
                f"above every copy: {ok}; true placements among the 20 listed: {listed}; placements done {s.get('placements_done')}")
