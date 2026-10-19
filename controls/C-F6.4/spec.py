"""Positive control for F6.4 (issue #73): padding applied separately at each grid stage (0135).
0135 ran one padded stage (8 blank places x 4 readings x widths 2-96) and two (cw/col readings, widths 2-48, blanks
dropped or kept as fillers between the griddings), forward and inverse, with a periodic key 1-26 after or before on
8 tableau classes, and listed K4's settings live below 20 (none); here the planted two-stage route with fillers kept,
order A, class std/std, period 9 must be among the 40 lowest-period settings listed, and K4's place must stand above
every copy at period 9. 0135's encrypt() is real (one alphabet, Vigenere, fillers struck at the end) and makes the
planted ciphertext."""
import random
import sys

from kryptos.plants import english_plant

ITEM = "F6.4"
EXPERIMENT = "0135"
WHAT = "Rows of 10 with the 3 blanks down the first column from the top, read by columns left first top down, blanks kept as fillers; then rows of 12 with the blanks at the end of the first row, turned clockwise; fillers struck; then a random period-9 key on the standard table, Vigenere, on English from Carter"
STAGES, L = [(10, "col", "P7", True), (12, "cw", "P4", False)], 9


def route(name, d):
    a = sys.modules["attack"]
    toks = a.stage(list(range(97)), name[2], name[0], name[1], len(name) > 3 and name[3] == "keep")
    if len(name) > 3:
        toks = a.stage(toks, name[6], name[4], name[5])
    wh = a.where_from(toks)
    if d == "inv":
        inv = [0] * 97
        for i, j in enumerate(wh):
            inv[j] = i
        wh = inv
    return wh


def plant():
    rng = random.Random(7416)
    k = [rng.randrange(26) for _ in range(L)]
    return {"plaintext": english_plant(7416), "key": {"stages": STAGES, "order": "A", "alphabet": "STD", "key": k},
            "where": route(("col", "P7", 10, "keep", "cw", "P4", 12), "fwd")}


def found(result, plant):
    b = result.get("bounds", {})
    hit = [e for e in b.get("k4_live_below_20", []) if e["order"] == "A" and e["class"] == "std/std/vig-var"
           and e["period"] == L and route(tuple(e["route"]), e["dir"]) == plant["where"]]
    above = ("A", L) in [tuple(c) for c in b.get("cells_k4_above_every_copper", [])]
    return bool(hit) and above, (f"settings live below 20: {b.get('k4_settings_live_below_20')}; the planted padded route at {L}, order A: {bool(hit)}; "
                                 f"A{L} above every copy: {above}; first stages done {b.get('first_stages_done')} of {b.get('first_stages_total')}")
