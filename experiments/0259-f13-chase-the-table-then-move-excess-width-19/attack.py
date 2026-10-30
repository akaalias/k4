"""Experiment 0259. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f13-chase-the-table-then-move-excess-width-19",
    "title": "F13.4h: chase 0237-0239's replicated excess (the table, then a move, key length 2): 1,000 fresh shuffles; the move library split into width-19 reads and the rest; a period-2 statistic of the carved order under the flagged move; known letters counted after",
    "family": "13-ciphertext-only",
    "parent": "0238-f13-replicate-k4-table-then-move-length-2-against-fresh-shuffles",
    "changed": (
        "F13.4h (Alexis, 2026-10-28, #101: chase it rather than note it). 0237 put K4's best reading at B2 (the sculpture's "
        "table with a key of 2, then a move; best move 'two turns cw 70,19 inverse', a width-19 read) above all 100 "
        "shuffles; 0238 replicated it (1 of 300 at or above); 0239's blind judge put the reading at the edge of chance. The "
        "working guess: a property of the carved order at width 19 (like 0056's width-7 doublets), not a message. Here: "
        "0238's frozen search (imported, unchanged) at B1-B2 and A1-A2 on K4 and 1,000 fresh shuffles, run three times per "
        "text with the move library cut to (a) every move, (b) width-19 reads only, (c) every move but width-19 reads; a "
        "statistic of the moved text itself, without any search (the two period-2 classes' index of coincidence under the "
        "flagged move, and the best over width-19 moves); 8 plants (B2 under a width-19 move) through the same cuts; the 24 "
        "known letters counted on K4's readings only after the comparison."
    ),
    "hypothesis_expert": (
        "F13.4d's excess: K4 under order B (periodic tableau key of length 2 on the sculpture's 8 table classes, then one "
        "of 0129's 27,852 moves; ciphertext only, MIX8m) reads above 299 of 300 shuffles. Under order B with key length 2 the "
        "reading is the moved text through two fixed substitutions (odd and even places), so a moved text whose two classes "
        "are unusually 'monoalphabetic' (high index of coincidence) lets the climb make English-like pairs without any "
        "message. If the excess lives only in width-19 reads and the moved text's period-2 IC is as extreme as the B2 score, "
        "the excess is a fingerprint of the carved order at width 19, like the width-21 repeats and the width-7 doublet "
        "column (04-structure.md), and not a reading. Known letters: the search never reads them (program.md, F13); after "
        "the comparison, K4's B2 readings are checked for the 24 letters in message order and in carved order (A2). "
        "Clue entries C1(a) (a matrix move then the table, in the other order here), C25 (the width-7/21 statistics)."
    ),
    "hypothesis_eli5": (
        "One earlier search found that K4, put through the sculpture's cipher table with a two-letter key and then read out "
        "of a grid 19 letters wide, gives a more English-looking jumble than almost any scrambled copy of K4 does. The "
        "reading itself is gibberish. We check whether this comes from the way K4's letters happen to sit at width 19, "
        "rather than from a hidden message: we repeat the search with only width-19 grids and without them, against 1,000 "
        "new scrambled copies, and we measure that width-19 pattern directly."
    ),
    "prediction": (
        "The B2 excess replicates in (a) at p below 0.05 and in (b) width-19 reads only, and vanishes in (c) without them; "
        "the flagged move's period-2 index of coincidence on K4 is above at least 95% of the shuffles under the same move. "
        "K4's B2 readings put at most 4 of the 24 known letters in place either way. Plants found in (a) and (b), lost in (c). "
        "If so, the excess is recorded as a property of the carved order at width 19 and F13.4h is closed."
    ),
    "method": (
        "1. 0238's solve(), imported unchanged, with its key lengths cut to 1-2 (cells A1, A2, B1, B2): per order and length the "
        "per-column frequency screen keeps the 30 best (move, class), each climbed, best rescored by MIX8m. "
        "2. Three move libraries: all 27,852; the width-19 reads (turn cw/ccw 19, columnar 19 either way, two turns with a 19, "
        "and their inverses); the rest. "
        "3. Texts: K4, 1,000 shuffles (seed 2570); 8 plants (Carter test windows, B2 under a random width-19 move and class), "
        "10 own shuffles each. "
        "4. Per library: K4's B2 rank among the shuffles; plants found when above all own copies at B2. "
        "5. No search: under 'two turns cw 70,19 inverse' and over every width-19 move, the moved text's mean IC of its odd "
        "and even places, K4 against the shuffles. "
        "6. After: K4's B2 readings' known letters in message order and carved order."
    ),
    "walkthrough": (
        "1. Write K4 in rows 19 letters wide (after first rotating it in a 70-wide grid, as the flagged move does) and read it "
        "out the other way. "
        "2. Split the result into its odd and even letters. "
        "3. Count how often letters repeat within each half (the index of coincidence): English-like texts repeat more. "
        "4. Do the same for 1,000 scrambled copies of K4. "
        "5. If K4 repeats more than nearly all copies, the earlier English-like jumble came from this pattern, not from a message."
    ),
    "expected_minutes": 60,
}

import importlib.util
import os
import random
import re
import sys
import time
import types
from pathlib import Path

import numpy as np

N = 97
ROOT = Path(__file__).resolve().parent
N_COPIES = 1000
PLANTS, OWN = 8, 10
SEED = 2570
FLAGGED = "two turns cw 70,19 inverse"
CUTS = ("all", "w19", "not19")
_MODS = {}


def M():
    if "m" not in _MODS:
        path = next((ROOT / "experiments").glob("0238-*")) / "attack.py"
        spec = importlib.util.spec_from_file_location("frozen0238", path)
        m = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = m
        spec.loader.exec_module(m)
        m.ROOT = ROOT
        m.LMAX = 2                      # cells A1, A2, B1, B2 only
        _MODS["m"] = m
    return _MODS["m"]


def is_w19(name):
    base = name.replace(" inverse", "")
    if re.fullmatch(r"(turn cw|turn ccw|columnar|columnar rtl) 19", base):
        return True
    mm = re.fullmatch(r"two turns cw (\d+),(\d+)", base)
    return bool(mm and "19" in mm.groups())


def _job(args):
    key, text, seed, cut = args
    m = M()
    m._G["W"] = _MODS["W"][cut]
    out = m.solve(text, seed)
    return key, {f"{o}{L}": [v[0], v[1], _MODS["names"][cut][v[2]]]
                 for (o, L), v in out.items()}


def ic2(text, w):
    """Mean index of coincidence of the odd and even places of the moved text (order B: the move is applied last)."""
    moved = [""] * N
    for i, ch in enumerate(text):
        moved[w[i]] = ch
    out = 0.0
    for r in (0, 1):
        cls = moved[r::2]
        n = len(cls)
        c = np.bincount([ord(x) - 65 for x in cls], minlength=26)
        out += float((c * (c - 1)).sum()) / (n * (n - 1))
    return out / 2


def run(ctx):
    import multiprocessing as mp
    t0 = time.time()
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    m = M()
    library = m.route_library(ctx.vocabulary)
    names = [n for n, _ in library]
    m._G["names"] = names
    m.lib(); m.models()
    idx = {"all": list(range(len(library))),
           "w19": [i for i, n in enumerate(names) if is_w19(n)],
           "not19": [i for i, n in enumerate(names) if not is_w19(n)]}
    _MODS["W"] = {c: np.ascontiguousarray(np.array([library[i][1] for i in idx[c]], dtype=np.int32)) for c in CUTS}
    _MODS["names"] = {c: [names[i] for i in idx[c]] for c in CUTS}
    assert FLAGGED in _MODS["names"]["w19"], "the flagged move must be a width-19 read"
    rng = random.Random(SEED)
    k4 = ctx.K4
    texts = [("k4", k4)] + [(f"copy{i}", "".join(rng.sample(k4, N))) for i in range(N_COPIES)]
    C = m._G["corpus"]
    plants = {}
    for j in range(PLANTS):
        src = C["test"] if j % 2 == 0 else C["test_xs"]
        o = rng.randrange(0, len(src) - N)
        p = src[o:o + N]
        mv = rng.choice(idx["w19"]); c = rng.randrange(len(m.CLASSES))
        key = {"order": "B", "where": library[mv][1], "class": m.CLASSES[c], "shifts": [rng.randrange(26) for _ in range(2)]}
        pc = m.encrypt(p, key)
        pid = f"plant{j}"
        plants[pid] = {"move": names[mv], "pt": p}
        texts.append((pid, pc))
        for g in range(OWN):
            s = list(pc); rng.shuffle(s); texts.append((f"{pid}_own{g}", "".join(s)))
    jobs = [(f"{tid}|{cut}", t, rng.randrange(10 ** 9), cut) for tid, t in texts for cut in CUTS]
    saved = getattr(ctx, "saved", {}) or {}
    res = {j[0]: saved[j[0]] for j in jobs if j[0] in saved}        # units an earlier run of this attack.py finished (#105)
    todo = [j for j in jobs if j[0] not in res]
    W = int(os.environ.get("K4_WORKERS", 8))
    ctx.progress(len(res), len(jobs), "solves")
    with mp.get_context("fork").Pool(W) as pool:
        for key, out in pool.imap_unordered(_job, todo, chunksize=1):
            res[key] = out
            ctx.save(key, out)
            ctx.progress(len(res), len(jobs), "solves")

    def rank(cut, cell):
        k = res[f"k4|{cut}"][cell][0]
        n_at = sum(1 for i in range(N_COPIES) if res[f"copy{i}|{cut}"][cell][0] >= k)
        return {"k4": round(k, 3), "copies_at_or_above": n_at, "p": round((1 + n_at) / (N_COPIES + 1), 4),
                "move": res[f"k4|{cut}"][cell][2], "reading": res[f"k4|{cut}"][cell][1]}
    ranks = {cut: {cell: rank(cut, cell) for cell in ("A1", "A2", "B1", "B2")} for cut in CUTS}
    found = {cut: sum(res[f"plant{j}|{cut}"]["B2"][0] > max(res[f"plant{j}_own{g}|{cut}"]["B2"][0] for g in range(OWN))
                      for j in range(PLANTS)) for cut in CUTS}
    exact = {cut: sum(res[f"plant{j}|{cut}"]["B2"][1] == plants[f"plant{j}"]["pt"] for j in range(PLANTS)) for cut in CUTS}
    # no search: period-2 IC of the moved text
    wf = dict(library)[FLAGGED]
    w19 = [library[i][1] for i in idx["w19"]]
    ic_flag_k4 = ic2(k4, wf)
    ic_flag_cop = [ic2(t, wf) for tid, t in texts[1:N_COPIES + 1]]
    ic_best_k4 = max(ic2(k4, w) for w in w19)
    ic_best_cop = [max(ic2(t, w) for w in w19) for tid, t in texts[1:N_COPIES + 1]]
    known = {}
    for cut in CUTS:
        rd = res[f"k4|{cut}"]["B2"][1]
        mvname = res[f"k4|{cut}"]["B2"][2]
        w = dict(library)[mvname]
        carved = "".join(rd[[i for i in range(N) if w[i] == j][0]] for j in range(N))   # the reading in carved order
        known[cut] = {"message_order": sum(rd[q - 1] == ch for q, ch in ctx.KNOWN.items()),
                      "carved_order": sum(carved[q - 1] == ch for q, ch in ctx.KNOWN.items())}
    bounds = {
        "item": "F13.4h", "search_reads_known_letters": False,
        "search": "0238's solve(), imported unchanged, key lengths 1-2 (cells A1, A2, B1, B2), MIX8m rescoring",
        "move_libraries": {c: len(idx[c]) for c in CUTS}, "k4_copies": N_COPIES, "seed": SEED,
        "ranks": ranks, "plants_found_at_B2": {c: [found[c], PLANTS] for c in CUTS}, "plants_read_exactly": exact,
        "ic2_flagged_move": {"k4": round(ic_flag_k4, 5), "copies_at_or_above": sum(1 for x in ic_flag_cop if x >= ic_flag_k4),
                             "copies_median": round(float(np.median(ic_flag_cop)), 5)},
        "ic2_best_width19_move": {"k4": round(ic_best_k4, 5), "copies_at_or_above": sum(1 for x in ic_best_cop if x >= ic_best_k4),
                                  "copies_median": round(float(np.median(ic_best_cop)), 5)},
        "k4_b2_known_letters": known, "compute_seconds": round(time.time() - t0), "exhaustive": False,
        "modal_cost_estimate": "about 1,089 texts x 3 cuts x about 2-3 s: about 2-3 core-hours, about $0.3-1 of Modal credit (about $3.7 left after the margin)",
    }
    notes = (f"F13.4h: K4 at B2 p all {ranks['all']['B2']['p']}, width-19 only {ranks['w19']['B2']['p']}, without width 19 "
             f"{ranks['not19']['B2']['p']} (1,000 shuffles); period-2 IC under the flagged move: "
             f"{bounds['ic2_flagged_move']['copies_at_or_above']} of 1,000 at or above; plants found "
             + ", ".join(f"{c} {found[c]}/{PLANTS}" for c in CUTS))
    from kryptos.scorer import free_text      # gate 4's controls only, after the search
    controls = [ctx.english_score(free_text(res[f"copy{i}|all"]["B2"][1])) for i in range(N_COPIES)]
    return {"candidates": [], "bounds": bounds, "notes": notes, "controls": controls}


def encrypt(plaintext, key):
    return M().encrypt(plaintext, key)


def worked_example(ctx, key):
    return "\n".join([
        "F13.4h: is K4's English-like jumble at B2 a pattern of the carved order at width 19?", "",
        "  K4 --(two turns cw 70, 19, inverse)--> moved text",
        "  moved text: odd places | even places   -> index of coincidence of each half",
        "  same for 1,000 scrambled copies; K4's rank says whether the width-19 pattern is unusual,",
        "  and the search repeated with and without width-19 moves says whether it carries the excess."])
