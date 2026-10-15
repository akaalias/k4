"""Experiment 0026. See program.md for the contract."""

EXPERIMENT = {
    "slug": "double-keyed-columnar-then-tableau",
    "title": "Two keyed columnar transpositions from the puzzle's words, then the tableau",
    "family": "6-transposition-then-tableau",
    "parent": "0016-routes-then-tableau-forced-key-english",
    "changed": "Route set: every ordered pair of vocabulary words as two keyed columnar transpositions, each forward or inverse, instead of plain widths. Sanborn's 'double matrixes' with the matrices keyed by words.",
    "hypothesis_expert": (
        "Sanborn, CNN 2005 (C1): 'double matrixes and triple matrixes... then went back to this table'. The "
        "NSA's K3 reading was a keyed columnar with key KRYPTOS; 0006 and 0016 used plain widths and single "
        "vocabulary keys. Here both stages are keyed by words from the vocabulary (C7 reading a, C8): 61 x 61 "
        "ordered pairs x 4 direction combinations, 14,884 routes, each followed by a periodic tableau under "
        "24 conventions. For each route the cribs land at known positions, the divisor rule gives the live "
        "periods, and for live periods up to 40 the forced key is scored as English on runs of five or more "
        "slots, with vocabulary matching and ten shuffled controls. Bounds: complete for this route set."
    ),
    "hypothesis_eli5": (
        "The artist said he sometimes scrambled the letters through two grids before using the table. The "
        "third message was scrambled through a grid whose columns were ordered by a key word. So we try two "
        "such grids in a row, each ordered by a word the puzzle knows, in every combination, and ask the "
        "usual question: where do the 24 known letters land, and could a short secret word on the table "
        "then produce the carved letters there?"
    ),
    "prediction": (
        "No route lets the cribs force a tableau key shorter than 22, and the forced keys at periods up to "
        "40 score inside the range of ten shuffled controls. No vocabulary match; zero candidates pass."
    ),
    "method": (
        "1. Build the routes from ordered pairs of vocabulary words, each stage forward or inverse. 2. For "
        "each route send the crib positions to their intermediate positions. 3. For each convention force "
        "the key letters and find live periods by the divisor rule. 4. Score the forced key at live periods "
        "up to 40 on runs of five or more slots; match against the vocabulary. 5. Repeat on ten shuffles."
    ),
    "walkthrough": (
        "1. Take the words KRYPTOS and ABSCISSA. 2. Write the message in rows of 7 under KRYPTOS, number the "
        "columns by alphabetical order of the letters (K=1, O=2, P=3, R=4, S=5, T=6, Y=7), and read the "
        "columns out in that order. 3. Write the result in rows of 8 under ABSCISSA and read it out the same "
        "way. 4. The E at position 22 of the message is now at some position j; the carved letter at j and "
        "E force a key letter on the sculpture's table. 5. Do this for all 24 known letters. 6. Two landing "
        "spots a multiple of p apart share a key letter at period p; a disagreement kills p. 7. For the "
        "periods that survive, write the forced letters into their slots and read them."
    ),
}

import random
from kryptos.alphabets import conventions, key_letter_for, numeric_order
from kryptos.ciphers import columnar_transposition_encrypt, columnar_transposition_decrypt

N = 97
MAXP = 40
DIVISORS = {d: [k for k in range(1, d + 1) if d % k == 0] for d in range(1, N + 1)}


def perm_of(fn):
    idx = [chr(0x100 + i) for i in range(N)]
    return [ord(ch) - 0x100 for ch in fn("".join(idx))]


def stage(word, inv):
    order = numeric_order(word)
    return (lambda s, o=order: columnar_transposition_decrypt(s, o)) if inv else (lambda s, o=order: columnar_transposition_encrypt(s, o))


def route_set(vocab):
    words = [w for w in vocab if 2 <= len(w) <= 40]
    routes = []
    for w1 in words:
        for w2 in words:
            for i1 in (False, True):
                for i2 in (False, True):
                    f1, f2 = stage(w1, i1), stage(w2, i2)
                    routes.append((f"{w1}{' inv' if i1 else ''} then {w2}{' inv' if i2 else ''}", lambda s, a=f1, b=f2: b(a(s))))
    return routes


def encrypt(plaintext, key):
    raise NotImplementedError("diagnostic experiment: no full key is implied, so no candidate is submitted")


def runs_in_slots(slots, P):
    filled = [slots.get(s) for s in range(P)]
    start = 0 if all(filled) else next(i for i in range(P) if filled[i] is None)
    out, cur = [], []
    for k in range(1, P + 1):
        ch = filled[(start + k) % P]
        if ch is None:
            if len(cur) >= 5: out.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    if len(cur) >= 5: out.append("".join(cur))
    return out


def search(ct, known, routes, convs, score, time_left):
    crib_pos = sorted(known)
    best, n = [], 0
    minp_hist = {}
    for name, fn in routes:
        if time_left() < 30:
            break
        sigma = perm_of(fn)
        where = {sigma[j]: j for j in range(N)}
        inter = [where[p - 1] for p in crib_pos]
        for conv in convs:
            pa, ca, ka, m = conv
            forced = [key_letter_for(known[p], ct[j], pa, ca, ka, m) for p, j in zip(crib_pos, inter)]
            dead = set()
            for a in range(24):
                for b in range(a + 1, 24):
                    if forced[a] != forced[b]:
                        dead.update(DIVISORS[abs(inter[a] - inter[b])])
            minp = next(P for P in range(1, N + 1) if P not in dead)
            minp_hist[minp] = minp_hist.get(minp, 0) + 1
            for P in range(2, MAXP + 1):
                if P in dead:
                    continue
                slots = {j % P: l for j, l in zip(inter, forced)}
                runs = runs_in_slots(slots, P)
                qs = sum(len(r) - 3 for r in runs)
                if qs < 4:
                    continue
                sc = sum(score(r) * (len(r) - 3) for r in runs) / qs
                n += 1
                if len(best) < 20 or sc > best[-1][0]:
                    best.append((sc, name, "/".join(conv), P, runs)); best.sort(reverse=True); best = best[:20]
    return best, n, minp_hist


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    routes = route_set(list(ctx.vocabulary))
    convs = list(conventions())
    best, n, hist = search(ct, known, routes, convs, ctx.english_score, ctx.time_left)
    nulls = []
    for seed in range(10):
        if ctx.time_left() < 120:
            break
        letters_ = list(ct); random.Random(seed).shuffle(letters_)
        nb, _, _ = search("".join(letters_), known, routes, convs, ctx.english_score, ctx.time_left)
        nulls.append(round(nb[0][0], 3) if nb else None)
    return {
        "candidates": [],
        "bounds": {"family": "double keyed columnar (vocabulary words) then periodic tableau", "routes": len(routes), "conventions": 24,
                   "periods": f"2-{MAXP}, live only", "keys_scored": n, "smallest_live_period": min(hist) if hist else None,
                   "min_live_period_histogram": {str(k): v for k, v in sorted(hist.items())[:12]},
                   "best": [{"score": round(sc, 3), "route": nm, "convention": cv, "period": P, "runs": rs} for sc, nm, cv, P, rs in best[:10]],
                   "shuffled_control_best": nulls},
        "notes": f"Diagnostic, no candidates. {len(routes)} routes; smallest live period {min(hist) if hist else None}; best forced key {best[0][0]:.3f} vs shuffled {[x for x in nulls if x is not None]}.",
    }


def worked_example(ctx, key):
    fn = lambda s: stage("ABSCISSA", False)(stage("KRYPTOS", False)(s))
    sigma = perm_of(fn); where = {sigma[j]: j for j in range(N)}
    lines = ["route: keyed columnar KRYPTOS then keyed columnar ABSCISSA; convention kry/kry/kry Vigenere", "", f"column order under KRYPTOS: {numeric_order('KRYPTOS')}; under ABSCISSA: {numeric_order('ABSCISSA')}", "", "plain pos  letter  lands at  carved  forced key letter"]
    for pos in (22, 23, 24, 25, 64, 65, 66):
        j = where[pos - 1]
        lines.append(f"{pos:>9}    {ctx.KNOWN[pos]}       {j+1:>3}        {ctx.K4[j]}       {key_letter_for(ctx.KNOWN[pos], ctx.K4[j], 'kry', 'kry', 'kry', 'vig')}")
    return "\n".join(lines)
