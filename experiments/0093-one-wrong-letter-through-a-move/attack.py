"""Experiment 0093. See program.md for the contract."""

EXPERIMENT = {
    "slug": "one-wrong-letter-through-a-move",
    "title": "One carved letter wrong, through a K3-style move and a repeating key",
    "family": "6-transposition-then-tableau",
    "parent": "0080-substitute-rotate-substitute-two-keys",
    "changed": "0031, 0050 and 0068 allowed one wrong carved letter only for keys with no move. Here every route of the type-1 library (K3's rule, one or two quarter turns, plain and true-keyword columnar, 27,852 distinct) is joined to a repeating key of length 1-26 before or after the move, and a setting counts as consistent if all known letters agree once at most one of them is set aside as a carving error.",
    "hypothesis_expert": (
        "Type 7 of directions.md, 'one letter off through types 1 and 2'. K2 carries a carving error Sanborn confirmed "
        "(the dropped S, corrected in 2006; 01-facts.md) and K1-K3 carry deliberate misspellings (C10, C17). A wrong "
        "carved letter outside the 24 crib images is invisible to crib tests; one on a crib image breaks exactly one "
        "equation. So: route library as in 0090 (forward and inverse, deduplicated); repeating key of period 1-26 after "
        "the move (slot = carved place mod p) or before it (slot = message place mod p); 8 tableau consistency classes. "
        "Within each key slot the forced values must agree; the number of disagreements is the sum over slots of "
        "(letters in slot - largest agreeing group). Zero is the plain test (0080-0085 bounds); one is one carving error. "
        "Counts per period compared with ten shuffled coppers."
    ),
    "hypothesis_eli5": (
        "Sanborn made at least one mistake carving K2. If he made one in K4, a correct method could fail our test "
        "at exactly one of the 24 known letters. So we rerun the grid moves of experiments 80 to 85 with a short "
        "repeating secret word, and this time accept any setting that fits all known letters but one. Allowing one "
        "miss also lets more chance settings through, so scrambled coppers tell us how many to expect."
    ),
    "prediction": (
        "With one miss allowed, the smallest consistent period on K4 is no lower than on the scrambled coppers, and the "
        "count at every period lies inside their range, give or take one period. No setting below period 14. Zero candidates."
    ),
    "method": (
        "1. Build the route library. 2. For each route, class and text, compute the key value forced at each known letter "
        "and its slot for each period and order. 3. Count the disagreements per period; record periods with zero and "
        "with one. 4. Repeat on ten shuffled coppers. 5. List K4's settings with one disagreement below period 14, and "
        "which known letter is set aside."
    ),
    "walkthrough": (
        "1. Pick a move, say a clockwise quarter turn of a grid 8 wide, and a key length, say 9. "
        "2. For each known letter, find where the move puts it and the key value that turns it into the carved letter there. "
        "3. Group the known letters by key slot: carved place mod 9. "
        "4. In each group, count the letters that disagree with the group's most common value. "
        "5. A total of 0 fits outright; a total of 1 fits if that one carved letter is a carving error. "
        "6. Repeat for every move, key length 1-26, both orders and every table rule, and on ten scrambled coppers."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.ciphers import columnar_transposition_encrypt
from kryptos.alphabets import numeric_order

N = 97
PMAX = 26
ALPH = {"std": STD, "kry": KRY}
N_CONTROLS = 10
EXTRA = ["EGYPT", "CAIRO", "LUXOR", "WALL", "NOVEMBER", "MESSAGE", "DELIVER", "DELIVERING", "TRANSMIT"]


def perm_of(fn):
    idx = "".join(chr(0x100 + i) for i in range(N))
    return [ord(ch) - 0x100 for ch in fn(idx)]


def rot_cw(s, w):
    rows = [s[i:i + w] for i in range(0, len(s), w)]
    return "".join(r[c] for c in range(w) for r in reversed(rows) if c < len(r))


def rot_ccw(s, w):
    rows = [s[i:i + w] for i in range(0, len(s), w)]
    return "".join(r[c] for c in reversed(range(w)) for r in rows if c < len(r))


def keyword_sequence(word):
    rank = numeric_order(word)
    return sorted(range(len(rank)), key=lambda c: rank[c])


def full_sequence(word):
    w = [c for c in word.upper() if c.isalpha()]
    return sorted(range(len(w)), key=lambda c: (w[c], c))


def route_fns(vocab):
    for b in range(1, N):
        for a in range(N):
            def f(s, a=a, b=b):
                out = [""] * N
                for i in range(N):
                    out[(a + b * i) % N] = s[i]
                return "".join(out)
            yield f"K3 rule a={a} b={b}", f
    for w in range(2, N):
        yield f"turn cw {w}", (lambda s, w=w: rot_cw(s, w))
        yield f"turn ccw {w}", (lambda s, w=w: rot_ccw(s, w))
        yield f"columnar {w}", (lambda s, o=list(range(w)): columnar_transposition_encrypt(s, o))
        yield f"columnar rtl {w}", (lambda s, o=list(range(w))[::-1]: columnar_transposition_encrypt(s, o))
    for w1 in range(2, N):
        for w2 in range(2, N):
            yield f"two turns cw {w1},{w2}", (lambda s, a=w1, b=w2: rot_cw(rot_cw(s, a), b))
    words = sorted({w for w in vocab if 2 <= len(w) <= 30} | set(EXTRA))
    for word in words:
        for how, seq in (("repeats dropped", keyword_sequence(word)), ("full word", full_sequence(word))):
            if len(seq) >= 2:
                yield f"keyword {word} ({how})", (lambda s, o=list(seq): columnar_transposition_encrypt(s, o))


def route_library(vocab):
    """Distinct 'where' maps (where[i] = place in the moved text of letter i), forward and inverse."""
    seen, lib = set(), []
    for name, f in route_fns(vocab):
        sigma = perm_of(f)                    # moved[j] = orig[sigma[j]]
        fwd = [0] * N
        for j, i in enumerate(sigma):
            fwd[i] = j
        for tag, w in ((name, fwd), (name + " inverse", sigma)):
            t = tuple(w)
            if t not in seen:
                seen.add(t); lib.append((tag, t))
    return lib


def misses(f, slots):
    """Sum over slots of (members - largest agreeing group); stops early above 1."""
    groups = {}
    for e, s in enumerate(slots):
        groups.setdefault(s, []).append(f[e])
    m = 0
    for vals in groups.values():
        if len(vals) > 1:
            cnt = {}
            for v in vals:
                cnt[v] = cnt.get(v, 0) + 1
            m += len(vals) - max(cnt.values())
            if m > 1:
                return 2
    return m


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    places = sorted(known)
    pidx = [p - 1 for p in places]
    lib = route_library(ctx.vocabulary)
    rng = random.Random(93)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    T = len(texts)
    classes = [(pa, ca, beau) for pa in ALPH for ca in ALPH for beau in (False, True)]
    CI = {an: [[{c: i for i, c in enumerate(ALPH[an])}[ch] for ch in t] for t in texts] for an in ALPH}
    PI = {an: [{c: i for i, c in enumerate(ALPH[an])}[known[p]] for p in places] for an in ALPH}
    slotsB = {p: [i % p for i in pidx] for p in range(1, PMAX + 1)}
    live = {(o, m): [[0] * (PMAX + 1) for _ in range(T)] for o in "AB" for m in (0, 1)}
    minp = {o: [dict() for _ in range(T)] for o in "AB"}
    k4_low = []
    for tag, where in lib:
        land = [where[i] for i in pidx]
        slotsA = {p: [j % p for j in land] for p in range(1, PMAX + 1)}
        for pa, ca, beau in classes:
            Pv = PI[pa]
            for t in range(T):
                C = CI[ca][t]
                f = [(C[j] + Pv[e]) % 26 if beau else (C[j] - Pv[e]) % 26 for e, j in enumerate(land)]
                for o, sl in (("A", slotsA), ("B", slotsB)):
                    first = None
                    for p in range(1, PMAX + 1):
                        m = misses(f, sl[p])
                        if m <= 1:
                            live[(o, m)][t][p] += 1
                            if m == 1 and first is None:
                                first = p
                                if t == 0 and p < 14:
                                    groups = {}
                                    for e, s in enumerate(sl[p]):
                                        groups.setdefault(s, []).append(e)
                                    odd = None
                                    for es in groups.values():
                                        cnt = {}
                                        for e in es:
                                            cnt[f[e]] = cnt.get(f[e], 0) + 1
                                        top = max(cnt, key=cnt.get)
                                        for e in es:
                                            if f[e] != top:
                                                odd = places[e]
                                    k4_low.append({"route": tag, "order": o, "class": f"{pa}/{ca}/{'beau' if beau else 'vig-var'}",
                                                   "period": p, "set_aside_place": odd})
                            if m == 0 and first is None:
                                first = p
                    mp = first or 0
                    minp[o][t][mp] = minp[o][t].get(mp, 0) + 1
        if ctx.time_left() < 60:
            break
    rng_ = lambda o, m, p: (min(live[(o, m)][t][p] for t in range(1, T)), max(live[(o, m)][t][p] for t in range(1, T)))
    outside = {f"{o} misses<={m}": [p for p in range(1, PMAX + 1) if not (rng_(o, m, p)[0] <= live[(o, m)][0][p] <= rng_(o, m, p)[1])]
               for o in "AB" for m in (0, 1)}
    k4_min = {o: min([p for p in minp[o][0] if p] or [0]) for o in "AB"}
    ctl_min = {o: [min([p for p in minp[o][t] if p] or [0]) for t in range(1, T)] for o in "AB"}
    bounds = {
        "family": "type-1 route library, then or before a periodic tableau key, at most one known letter set aside",
        "distinct_routes": len(lib), "periods": [1, PMAX], "classes": 8,
        "k4_live_exact_by_period": {o: live[(o, 0)][0][1:] for o in "AB"},
        "k4_live_one_miss_by_period": {o: live[(o, 1)][0][1:] for o in "AB"},
        "controls_one_miss_min": {o: [rng_(o, 1, p)[0] for p in range(1, PMAX + 1)] for o in "AB"},
        "controls_one_miss_max": {o: [rng_(o, 1, p)[1] for p in range(1, PMAX + 1)] for o in "AB"},
        "periods_outside_control_range": outside,
        "k4_smallest_period_with_at_most_one_miss": k4_min, "controls_smallest": ctl_min,
        "k4_one_miss_below_14": k4_low[:40], "n_k4_one_miss_below_14": len(k4_low),
        "controls": f"{N_CONTROLS} shuffled coppers (seed 93), identical search",
        "order_A": "move, then key (slot = carved place mod p)", "order_B": "key, then move (slot = message place mod p)",
    }
    notes = (f"{len(lib):,} routes x 8 classes x 2 orders, periods 1-26, one miss allowed. Smallest period with at most one "
             f"miss: K4 {k4_min}, controls {ctl_min}. K4 one-miss settings below 14: {len(k4_low)}. Outside control range: {outside}.")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    sigma = perm_of(lambda x: rot_cw(x, 8))
    where = [0] * N
    for j, i in enumerate(sigma):
        where[i] = j
    I = {c: i for i, c in enumerate(KRY)}
    places = sorted(known)
    f = [(I[ct[where[p - 1]]] - I[known[p]]) % 26 for p in places]
    lines = ["clockwise quarter turn of a grid 8 wide, then a key of length 9; sculpture's alphabet, Vigenere", "",
             "place  letter  lands at  copper  key value  slot (mod 9)"]
    for e, p in enumerate(places):
        if p in (22, 23, 24, 25, 26, 27, 64, 65, 66):
            j = where[p - 1]
            lines.append(f"{p:>5}  {known[p]:>6}  {j + 1:>8}  {ct[j]:>6}  {f[e]:>9}  {j % 9:>12}")
    lines.append("")
    lines.append(f"disagreements at period 9: {misses(f, [where[p - 1] % 9 for p in places])} (2 means two or more)")
    return "\n".join(lines)
