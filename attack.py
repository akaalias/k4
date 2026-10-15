"""Experiment 0033. See program.md for the contract."""

EXPERIMENT = {
    "slug": "trifid-keyword-cubes-and-annealing",
    "title": "Trifid: the 27-cell cube that fractionates letters, with keyword cubes tested exactly and free cubes annealed",
    "family": "4-visual-spatial",
    "parent": None,
    "changed": "New root in family 4. Trifid is the one classical fractionating cipher that fits 26 letters plus the question mark; the 25-letter-square systems are dead because all 26 letters occur in K4. Keyword-built cubes are tested exactly; free cubes are searched by simulated annealing on crib hits.",
    "hypothesis_expert": (
        "Delastelle's trifid (1901; in the ACA list and the manuals Scheidt taught from, C5) maps each of 27 "
        "symbols to a point in a 3x3x3 cube, writes a block of p letters as three coordinate rows, and reads "
        "the rows off in triples: a spatial system in Sanborn's sense (C3) and a matrix in his (C1), with the "
        "sculpture's own '?' as the 27th symbol. Playfair, bifid and the four-square family are dead because "
        "K4 uses all 26 letters (knowledge/04-structure.md); a 2x13 grid cannot fractionate; trifid can. "
        "Two tests. Exact: cubes built from every vocabulary word by the four Friedman mixings with '?' first "
        "or last, periods 2-20, every alignment, scored by crib hits after decryption. Search: for periods "
        "2-15 and every alignment, simulated annealing over free cubes with crib hits as the objective, two "
        "restarts each, then more iterations for the best settings. A true cube gives 24 of 24; chance gives "
        "about 1 of 24 per decryption. In a dry run the annealer, with a coordinate-level objective, reached "
        "only 17 of 24 on a planted free cube at the planted cube's own period and alignment, so the search is "
        "weak and its result is not a bound. Bounds: complete for keyword cubes only; free cubes stay open."
    ),
    "hypothesis_eli5": (
        "Trifid turns each letter into three small digits, like an address with floor, row and seat in a "
        "27-seat cube, writes the addresses of a few letters in rows, and then reads the digits off in a "
        "different grouping, so each new letter is made from pieces of three old ones. It is one of the few "
        "old ciphers that can handle all 26 letters plus the question mark the sculpture already uses. We "
        "first try cubes built from the puzzle's words, then let a computer rearrange the cube by trial and "
        "error, rewarding every known letter it gets right."
    ),
    "prediction": (
        "No keyword cube at any period and alignment gets more than 5 of 24 crib letters right. Annealing "
        "on free cubes reaches at most 10 of 24 at its best setting, the same as on shuffled K4. Zero "
        "candidates pass."
    ),
    "method": (
        "1. Build keyword cubes: for each vocabulary word and mixing, the 26-letter mixed alphabet with '?' "
        "appended or prepended, filled into the cube in order. 2. For each cube, period 2-20 and alignment, "
        "decrypt and count crib hits. 3. For periods 2-15 and alignments, anneal a random cube by swapping "
        "two symbols, accepting by crib hits with a temperature schedule, two restarts of 4,000 steps. "
        "4. Re-anneal the five best settings with 20,000 steps. 5. Repeat the search on two shuffles of K4 "
        "for calibration. 6. Submit any decryption with all 24 cribs."
    ),
    "walkthrough": (
        "1. Fill a cube with KRYPTOSABCDEFGHIJLMNQUVWXZ? in order: K is at (0,0,0), R at (0,0,1), ... the 27th "
        "symbol ? at (2,2,2). 2. Take period 5 and the first carved block OBKRU. 3. Write each letter's three "
        "digits in a column: O gives (0,1,2) in this cube, and so on for five letters. 4. Read the 15 digits "
        "row by row into one line and cut it into five triples: those are the five message letters' "
        "addresses. 5. Look them up in the cube. 6. Do this for every block, then check positions 22 to 34 "
        "and 64 to 74 against EASTNORTHEAST and BERLINCLOCK. 7. Count the hits; 24 means the cube and "
        "period are right."
    ),
}

import math
import random
from kryptos.alphabets import keyword_mixed, columnar_mixed, keyed_columnar_mixed, alternate_vertical_mixed

N = 97
SYMBOLS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ?"
MIX = {"keyword": keyword_mixed, "columnar": columnar_mixed, "keyed_columnar": keyed_columnar_mixed, "alt_vertical": alternate_vertical_mixed}


def coords_of(cube):
    """cube: 27-symbol string in cube order (layer, row, col). Returns symbol -> (l, r, c) and inverse."""
    to = {}
    frm = {}
    for i, ch in enumerate(cube):
        t = (i // 9, (i // 3) % 3, i % 3)
        to[ch] = t; frm[t] = ch
    return to, frm


def trifid(text, cube, p, o, decrypt):
    to, frm = coords_of(cube)
    out = list(text)
    i = o
    # the leading partial block (positions before o) is treated as its own block of length o
    blocks = []
    if o:
        blocks.append((0, o))
    while i < N:
        blocks.append((i, min(i + p, N))); i += p
    for s, e in blocks:
        blk = text[s:e]; n = len(blk)
        if n < 2:
            continue
        if not decrypt:
            rows = [[to[ch][k] for ch in blk] for k in range(3)]
            digits = rows[0] + rows[1] + rows[2]
            out[s:e] = [frm[tuple(digits[3 * j:3 * j + 3])] for j in range(n)]
        else:
            digits = [d for ch in blk for d in to[ch]]
            rows = [digits[0:n], digits[n:2 * n], digits[2 * n:3 * n]]
            out[s:e] = [frm[(rows[0][j], rows[1][j], rows[2][j])] for j in range(n)]
    return "".join(out)


def encrypt(plaintext, key):
    return trifid(plaintext, key["cube"], key["period"], key["offset"], False)


def hits(pt, known):
    return sum(1 for pos, ch in known.items() if pt[pos - 1] == ch)


def coord_score(ct, cube, p, o, known):
    """Finer objective for annealing: at each crib position, how many of the three cube coordinates
    of the decrypted symbol agree with those of the known letter (0-72)."""
    to, _ = coords_of(cube)
    pt = trifid(ct, cube, p, o, True)
    return sum(sum(1 for x, y in zip(to[pt[pos - 1]], to[ch]) if x == y) for pos, ch in known.items())


def anneal(ct, known, p, o, rng, steps, cube=None):
    """Start from the given cube, or a random one, and swap symbols to raise crib hits."""
    if cube is None:
        cube = list(SYMBOLS); rng.shuffle(cube)
    else:
        cube = list(cube)
    cur = "".join(cube); cur_s = coord_score(ct, cur, p, o, known)
    best, best_h = cur, hits(trifid(ct, cur, p, o, True), known)
    for t in range(steps):
        T = max(0.1, 3.0 * (1 - t / steps))
        a, b = rng.sample(range(27), 2)
        lst = list(cur); lst[a], lst[b] = lst[b], lst[a]
        cand = "".join(lst); sc = coord_score(ct, cand, p, o, known)
        if sc >= cur_s or rng.random() < math.exp((sc - cur_s) / T):
            cur, cur_s = cand, sc
            h = hits(trifid(ct, cur, p, o, True), known)
            if h > best_h:
                best, best_h = cur, h
    return best, best_h


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    vocab = list(ctx.vocabulary)
    rng = random.Random(33)
    # exact: keyword cubes
    cubes = {}
    for w in vocab:
        if len(set(w)) >= 3:
            for mname, fn in MIX.items():
                A = fn(w)
                cubes[f"{w}/{mname}/?last"] = A + "?"
                cubes[f"{w}/{mname}/?first"] = "?" + A
    cubes["KRYPTOS order ?last"] = "KRYPTOSABCDEFGHIJLMNQUVWXZ?"
    cubes["standard ?last"] = SYMBOLS
    exact_best = []
    candidates = []
    n_exact = 0
    for name, cube in cubes.items():
        for p in range(2, 21):
            for o in range(p):
                n_exact += 1
                pt = trifid(ct, cube, p, o, True)
                h = hits(pt, known)
                if len(exact_best) < 10 or h > exact_best[-1][0]:
                    exact_best.append((h, name, p, o)); exact_best.sort(reverse=True); exact_best = exact_best[:10]
                if h == 24:
                    candidates.append({"plaintext": pt, "key": {"cube": cube, "period": p, "offset": o}, "key_bits": 30, "key_description": f"trifid cube {name} period {p} offset {o}"})
    # search: annealing
    settings = []
    for p in range(2, 16):
        for o in range(p):
            if ctx.time_left() < 400:
                break
            bh = 0; bc = None
            for restart in range(4):
                c, h = anneal(ct, known, p, o, rng, 4000)
                if h > bh:
                    bh, bc = h, c
            settings.append((bh, p, o, bc))
    settings.sort(reverse=True)
    refined = []
    for bh, p, o, bc in settings[:5]:
        if ctx.time_left() < 200:
            break
        c, h = anneal(ct, known, p, o, rng, 20000, bc)
        refined.append((h, p, o, c))
        if h == 24:
            pt = trifid(ct, c, p, o, True)
            candidates.append({"plaintext": pt, "key": {"cube": c, "period": p, "offset": o}, "key_bits": 94, "key_description": f"trifid annealed cube period {p} offset {o}"})
    refined.sort(reverse=True)
    control = []
    for seed in range(2):
        if ctx.time_left() < 120:
            break
        letters_ = list(ct); random.Random(seed).shuffle(letters_); sct = "".join(letters_)
        bh = 0
        for bh0, p, o, _ in settings[:3]:
            c, h = anneal(sct, known, p, o, rng, 4000); bh = max(bh, h)
        control.append(bh)
    return {
        "candidates": candidates[:50],
        "bounds": {"family": "trifid, 27-symbol cube, periods 2-20", "keyword_cubes": len(cubes), "exact_decryptions": n_exact,
                   "exact_best_hits": [{"hits": h, "cube": n, "period": p, "offset": o} for h, n, p, o in exact_best],
                   "annealing_settings": len(settings), "annealing_best_by_setting": [{"hits": h, "period": p, "offset": o} for h, p, o, _ in settings[:10]],
                   "refined_best": [{"hits": h, "period": p, "offset": o, "cube": c} for h, p, o, c in refined[:3]],
                   "shuffled_control_best_hits": control},
        "notes": f"Keyword cubes: best {exact_best[0][0]} of 24 hits over {n_exact} decryptions. Annealing: best {refined[0][0] if refined else None} of 24 after refinement (settings best {settings[0][0] if settings else None}); shuffled K4 reaches {control}.",
    }


def worked_example(ctx, key):
    cube = "KRYPTOSABCDEFGHIJLMNQUVWXZ?"
    to, frm = coords_of(cube)
    blk = ctx.K4[:5]
    lines = [f"cube in KRYPTOS order with ? last; period 5, first block {blk}", ""]
    for ch in blk:
        lines.append(f"{ch} -> {to[ch]}")
    digits = [d for ch in blk for d in to[ch]]
    rows = [digits[0:5], digits[5:10], digits[10:15]]
    lines.append(f"digits in a line: {''.join(map(str, digits))}; cut into rows of 5: {rows}")
    lines.append("message letters: " + "".join(frm[(rows[0][j], rows[1][j], rows[2][j])] for j in range(5)))
    lines.append("")
    pt = trifid(ctx.K4, cube, 5, 0, True)
    lines.append(f"full decryption at period 5: {pt}; crib hits {hits(pt, ctx.KNOWN)} of 24")
    return "\n".join(lines)
