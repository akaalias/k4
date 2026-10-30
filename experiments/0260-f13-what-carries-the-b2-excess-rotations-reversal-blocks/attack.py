"""Experiment 0260. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f13-what-carries-the-b2-excess-rotations-reversal-blocks",
    "title": "F13.4i: what carries K4's B2 excess? K4's 96 cyclic rotations, its reversal and 300 block-shuffled versions through 0238's search, against 500 fresh shuffles; planted messages rotated the same way",
    "family": "13-ciphertext-only",
    "parent": "0259-f13-chase-the-table-then-move-excess-width-19",
    "changed": (
        "F13.4i (Alexis, #101: chase it). 0259 replicated K4's excess at B2 (the sculpture's table with a two-letter key, then "
        "a move) against 1,000 fresh shuffles, p 0.002, and showed it does not need width-19 moves (p 0.004 without them). "
        "Here the question is what in K4 carries it. A cyclic rotation keeps every adjacency of the carved letters (the "
        "width-7 doublet column and the width-21 repeats move together) but changes every place; the reversal keeps "
        "adjacency mirrored; cutting K4 into blocks of 4, 7 or 12 and shuffling the blocks keeps structure inside a block "
        "only. A planted B2 message is rotated the same way as a positive control: its excess should vanish when rotated."
    ),
    "hypothesis_expert": (
        "F13.4d/h: order B (periodic tableau key of length 2 on the sculpture's 8 table classes, then one of 0129's 27,852 "
        "moves), ciphertext only, 0238's frequency screen, climb and MIX8m rescoring. If K4's B2 excess comes from local "
        "structure of the carved letters that any arrangement of them by blocks keeps (letters that sit well together), "
        "rotations and large-block shuffles stay extreme; if it comes from a message enciphered at these exact places, "
        "only K4 in its own order is extreme, as only the unrotated plant is. Pre-registered: share of rotations above the "
        "shuffles' 95th percentile at B2 at least 0.5 means a position-free property (the excess carries no reading, F13.4h "
        "closed as a property of the carved letters); at most 0.1 means positional, and the reading is chased (judge, known "
        "words on the intermediate text). Clue entries C25 (the width-7/21 statistics), C1(a)."
    ),
    "hypothesis_eli5": (
        "K4 reads a little more like English than almost any scrambled copy of it under one particular two-step cipher, "
        "though the reading itself is gibberish. Is that because of where K4's letters are, which a hidden message would "
        "explain, or because of which letters sit next to each other, which a message would not need? We slide K4 around "
        "in a circle (every letter keeps its neighbours but changes its place), flip it, and chop it into pieces we shuffle, "
        "and see which versions keep the effect. A hidden test message treated the same way should lose it."
    ),
    "prediction": (
        "Most rotations as extreme as K4 (share above the 95th percentile at least 0.5) and the reversal too: a property of "
        "the carved letters' neighbourhoods, kept by blocks of 7 and 12 more than by blocks of 4. The plants lose their excess "
        "when rotated (rotated plants at the shuffles' level). Zero candidates."
    ),
    "method": (
        "1. Texts: K4; its rotations by 1-96 places; its reversal; 100 block shuffles each for blocks of 4, 7 and 12 (seed "
        "2601); 500 fresh shuffles (seed 2600) as the reference; 3 planted B2 messages (Carter test windows, a random width-19 "
        "move and table class, key of 2) and 24 rotations of each (every fourth). "
        "2. Each text through 0238's solve(), unchanged, at cells A1, A2, B1, B2 (every move). "
        "3. Per text its B2 score's percentile among the 500 shuffles. "
        "4. Verdict by the pre-registered shares for the rotations; the blocks and the reversal reported beside it."
    ),
    "walkthrough": (
        "1. Write K4 around a circle and start reading it one place later: OBKRU... becomes BKRUO...O. "
        "2. Every letter keeps its neighbours, but every letter has moved one place. "
        "3. Run the same search on this rotated text and compare its score with 500 scrambled copies of K4. "
        "4. Repeat for all 96 rotations, for K4 read backwards, and for K4 cut into pieces whose order is shuffled. "
        "5. If the rotations score as high as K4, the effect comes from which letters sit together, not from a message "
        "written at exact places."
    ),
    "expected_minutes": 10,
}

import importlib.util
import os
import random
import sys
import time
import types
from pathlib import Path

import numpy as np

N = 97
ROOT = Path(__file__).resolve().parent
N_SHUFFLES = 500
BLOCKS = (4, 7, 12)
N_BLOCK = 100
PLANTS, PLANT_ROT_STEP = 3, 4
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
    import re
    base = name.replace(" inverse", "")
    if re.fullmatch(r"(turn cw|turn ccw|columnar|columnar rtl) 19", base):
        return True
    mm = re.fullmatch(r"two turns cw (\d+),(\d+)", base)
    return bool(mm and "19" in mm.groups())


def _job(args):
    key, text, seed = args
    m = M()
    out = m.solve(text, seed)
    return key, {f"{o}{L}": [v[0], v[1], m._G["names"][v[2]]] for (o, L), v in out.items()}


def blocks(text, b, rng):
    parts = [text[i:i + b] for i in range(0, N, b)]
    rng.shuffle(parts)
    return "".join(parts)


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
    m._G["W"] = np.ascontiguousarray(np.array([w for _, w in library], dtype=np.int32))
    m.lib(); m.models()
    k4 = ctx.K4
    rng = random.Random(2600)
    texts = [("k4", k4)] + [(f"rot{r}", k4[r:] + k4[:r]) for r in range(1, N)] + [("rev", k4[::-1])]
    brng = random.Random(2601)
    for b in BLOCKS:
        texts += [(f"blk{b}_{i}", blocks(k4, b, brng)) for i in range(N_BLOCK)]
    texts += [(f"shuf{i}", "".join(rng.sample(k4, N))) for i in range(N_SHUFFLES)]
    C = m._G["corpus"]
    prng = random.Random(2602)
    w19 = [i for i, n in enumerate(names) if is_w19(n)]
    plants = {}
    for j in range(PLANTS):
        src = C["test"] if j % 2 == 0 else C["test_xs"]
        o = prng.randrange(0, len(src) - N)
        p = src[o:o + N]
        mv = prng.choice(w19); c = prng.randrange(len(m.CLASSES))
        key = {"order": "B", "where": library[mv][1], "class": m.CLASSES[c], "shifts": [prng.randrange(26) for _ in range(2)]}
        pc = m.encrypt(p, key)
        plants[f"plant{j}"] = {"move": names[mv]}
        texts += [(f"plant{j}_rot{r}", pc[r:] + pc[:r]) for r in range(0, N, PLANT_ROT_STEP)]
    jobs = [(tid, t, rng.randrange(10 ** 9)) for tid, t in texts]
    saved = getattr(ctx, "saved", {}) or {}
    res = {j[0]: saved[j[0]] for j in jobs if j[0] in saved}        # units an earlier run of this attack.py finished (#105)
    todo = [j for j in jobs if j[0] not in res]
    W = int(os.environ.get("K4_WORKERS", 8))
    ctx.progress(len(res), len(jobs), "texts")
    with mp.get_context("fork").Pool(W) as pool:
        for key, out in pool.imap_unordered(_job, todo, chunksize=1):
            res[key] = out
            ctx.save(key, out)
            ctx.progress(len(res), len(jobs), "texts")

    cells = ("A1", "A2", "B1", "B2")
    ref = {c: np.array([res[f"shuf{i}"][c][0] for i in range(N_SHUFFLES)]) for c in cells}
    q95 = {c: float(np.quantile(ref[c], 0.95)) for c in cells}

    def pct(tid, c="B2"):
        return float((ref[c] < res[tid][c][0]).mean())
    rot = [pct(f"rot{r}") for r in range(1, N)]
    share_rot = float(np.mean([x > 0.95 for x in rot]))
    blk = {b: float(np.mean([pct(f"blk{b}_{i}") > 0.95 for i in range(N_BLOCK)])) for b in BLOCKS}
    plant_rows = {}
    for j in range(PLANTS):
        p0 = pct(f"plant{j}_rot0")
        others = [pct(f"plant{j}_rot{r}") for r in range(PLANT_ROT_STEP, N, PLANT_ROT_STEP)]
        plant_rows[f"plant{j}"] = {"move": plants[f"plant{j}"]["move"], "unrotated_percentile": round(p0, 4),
                                   "rotations_above_95th": round(float(np.mean([x > 0.95 for x in others])), 3)}
    verdict = "position-free" if share_rot >= 0.5 else "positional" if share_rot <= 0.1 else "mixed"
    best_rot = sorted(range(1, N), key=lambda r: -rot[r - 1])[:10]
    bounds = {
        "item": "F13.4i", "search_reads_known_letters": False,
        "search": "0238's solve(), imported unchanged, every move (27,852), cells A1, A2, B1, B2, MIX8m rescoring",
        "reference": f"{N_SHUFFLES} fresh shuffles of K4 (seed 2600)", "q95_by_cell": {c: round(v, 2) for c, v in q95.items()},
        "k4_percentile_by_cell": {c: round(pct('k4', c), 4) for c in cells},
        "rotations_share_above_95th_B2": round(share_rot, 3), "rotations_percentile_B2": [round(x, 3) for x in rot],
        "rotations_median_percentile_B2": round(float(np.median(rot)), 3),
        "top_rotations_B2": [{"rot": r, "percentile": round(rot[r - 1], 4), "move": res[f"rot{r}"]["B2"][2]} for r in best_rot],
        "reversal_percentile_B2": round(pct("rev"), 4), "reversal_move": res["rev"]["B2"][2],
        "blocks_share_above_95th_B2": blk, "plants": plant_rows, "verdict": verdict,
        "k4_b2_move": res["k4"]["B2"][2], "k4_b2_reading": res["k4"]["B2"][1],
        "texts": len(jobs), "compute_seconds": round(time.time() - t0), "exhaustive": False,
        "modal_cost_estimate": "about 1,072 texts x about 1-2 s: well under $0.1 of Modal credit",
    }
    notes = (f"F13.4i: K4 B2 percentile {pct('k4'):.3f}; rotations above the 95th percentile {share_rot:.2f} (median "
             f"{np.median(rot):.2f}); reversal {pct('rev'):.3f}; blocks of 4/7/12 above 95th {blk[4]:.2f}/{blk[7]:.2f}/{blk[12]:.2f}; "
             f"plants unrotated " + ", ".join(f"{v['unrotated_percentile']:.2f}" for v in plant_rows.values()) +
             ", rotated above 95th " + ", ".join(f"{v['rotations_above_95th']:.2f}" for v in plant_rows.values()) +
             f"; verdict {verdict}")
    from kryptos.scorer import free_text      # gate 4's controls only, after the search
    controls = [ctx.english_score(free_text(res[f"shuf{i}"]["B2"][1])) for i in range(N_SHUFFLES)]
    return {"candidates": [], "bounds": bounds, "notes": notes, "controls": controls}


def encrypt(plaintext, key):
    return M().encrypt(plaintext, key)


def worked_example(ctx, key):
    k4 = ctx.K4
    return "\n".join([
        "F13.4i: rotate K4 and see whether its B2 excess survives.", "",
        f"  K4         {k4[:30]}...",
        f"  rotated 1  {(k4[1:] + k4[:1])[:30]}...",
        f"  reversed   {k4[::-1][:30]}...", "",
        "  each through the same search (the table with a two-letter key, then any of 27,852 moves),",
        "  each scored against 500 scrambled copies of K4. A message at exact places loses its excess when rotated."])
