"""Experiment 0106. See program.md for the contract."""

EXPERIMENT = {
    "slug": "one-to-one-substitution-with-every-move-so-far",
    "title": "A one-to-one letter substitution with every move built so far: paths, mixed turns, triple turns and the type-1 library",
    "family": "9-substitution-then-transposition",
    "parent": "0019-substitution-then-route-crib-images-one-to-one",
    "changed": "0019 tested a monoalphabetic substitution with 23,931 routes. Since then experiments 80-99 built far larger move sets: the type-1 library (27,852), grid paths (43,579), mixed-sense double turns (53,743) and every triple clockwise turn (1.7 million). A one-to-one substitution commutes with any move, so one test covers both orders: the known letters must land on carved letters that a single one-to-one table can explain.",
    "hypothesis_expert": (
        "Family 9 (least covered, two experiments), open 'only for routes outside the set (spirals, diagonals, keyed "
        "routes)' (families.md); 0018 found substitution-then-transposition the only construction reproducing the width-21 "
        "repeats. Model: c = route(sigma(p)) = sigma(route(p)), sigma any permutation of 26 letters. Test: for the 24 "
        "known letters at their landing places, equal message letters must land on equal carved letters and different on "
        "different. Route sets: the type-1 library (K3's rule, one and two clockwise turns, plain and true-keyword "
        "columnar, forward and inverse); 0092's 30 x 29 path pairs at widths 2-96; 0099's mixed-sense double turns; 0083's "
        "triple clockwise turns at widths 2-96; all deduplicated. Ten shuffled coppers. Survivors decrypt wherever sigma "
        "is fixed and are scored."
    ),
    "hypothesis_eli5": (
        "The simplest two-step cipher swaps each letter for another by a fixed table and then moves the letters around. "
        "Experiment 19 tried this with about 24,000 ways of moving letters. Since then we have built ways of moving "
        "letters by the million. For each one we check whether a single swap table can turn the known letters into the "
        "carved letters where they land: the same letter must always become the same letter."
    ),
    "prediction": (
        "No route of any set survives on K4, and none on the shuffled coppers, as in 0019. Zero candidates."
    ),
    "method": (
        "1. Build the four route sets and deduplicate (by a 64-bit hash of each route). 2. For each route and text, map each known letter to the carved "
        "letter at its landing place; reject on a clash. 3. Count survivors per set on K4 and ten shuffled coppers. 4. "
        "Decrypt survivors where the table is fixed and score them."
    ),
    "walkthrough": (
        "1. Pick a move, say snake rows of 10 read by columns. "
        "2. Find where each known letter lands and read the carved letter there. "
        "3. E occurs three times among the known letters (places 22, 31 and 65): all three must land on the same carved letter. "
        "4. And two different known letters must never land on the same carved letter. "
        "5. Repeat for every move in the four sets and on scrambled coppers."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.ciphers import columnar_transposition_encrypt
from kryptos.alphabets import numeric_order

N = 97
N_CONTROLS = 10
NULL = -1
EXTRA = ["EGYPT", "CAIRO", "LUXOR", "WALL", "NOVEMBER", "MESSAGE", "DELIVER", "DELIVERING", "TRANSMIT"]


def cells(w):
    return [(i // w, i % w) for i in range(N)]


def paths(w):
    """30 orders of the 97 cells of a width-w grid (last row short)."""
    cs = cells(w)
    have = set(cs)
    h = -(-N // w)
    out = {}
    out["rows"] = list(cs)
    out["snake rows"] = [(r, c if r % 2 == 0 else w - 1 - c) for r in range(h) for c in range(w) if (r, c if r % 2 == 0 else w - 1 - c) in have]
    out["columns"] = [(r, c) for c in range(w) for r in range(h) if (r, c) in have]
    out["snake columns"] = [(r if c % 2 == 0 else h - 1 - r, c) for c in range(w) for r in range(h) if (r if c % 2 == 0 else h - 1 - r, c) in have]

    def cw_spiral(hh, ww):
        top, bot, left, right = 0, hh - 1, 0, ww - 1
        seq = []
        while top <= bot and left <= right:
            for c in range(left, right + 1):
                seq.append((top, c))
            for r in range(top + 1, bot + 1):
                seq.append((r, right))
            if top < bot:
                for c in range(right - 1, left - 1, -1):
                    seq.append((bot, c))
            if left < right:
                for r in range(bot - 1, top, -1):
                    seq.append((r, left))
            top += 1; bot -= 1; left += 1; right -= 1
        return seq

    def spiral(corner, cw):
        # clockwise from the top-left goes right first; anticlockwise from the top-left goes down first (the transpose)
        fr, fc = corner
        base_cw = cw if fr == fc else not cw          # one mirror reverses the sense of turning, two do not
        seq = cw_spiral(h, w) if base_cw else [(r, c) for c, r in cw_spiral(w, h)]
        mapped = [((h - 1 - r) if fr else r, (w - 1 - c) if fc else c) for r, c in seq]
        return [x for x in mapped if x in have]
    for corner in ((0, 0), (0, 1), (1, 0), (1, 1)):
        for cw in (True, False):
            out[f"spiral {'bottom' if corner[0] else 'top'}-{'right' if corner[1] else 'left'} {'cw' if cw else 'ccw'}"] = spiral(corner, cw)
    out["anti-diagonals"] = sorted(cs, key=lambda x: (x[0] + x[1], x[0]))
    out["snake anti-diagonals"] = sorted(cs, key=lambda x: (x[0] + x[1], x[0] if (x[0] + x[1]) % 2 == 0 else -x[0]))
    out["diagonals"] = sorted(cs, key=lambda x: (x[1] - x[0], x[0]))
    for k in list(out):
        out[k + " reversed"] = out[k][::-1]
    for k, v in out.items():
        assert len(v) == N and len(set(v)) == N, (w, k)
    return out


def route(write, read):
    """where[i]: place in the read-out text of message letter i."""
    pos = {cell: j for j, cell in enumerate(read)}
    return [pos[write[i]] for i in range(N)]


def grid(tokens, w, top):
    """Rows of the grid as lists of tokens or None for a blank cell."""
    n = len(tokens)
    h = -(-n // w)
    blanks = h * w - n
    cells, it = [], iter(tokens)
    for c in range(h * w):
        blank = c < blanks if top else c >= h * w - blanks
        cells.append(None if blank else next(it))
    return [cells[r * w:(r + 1) * w] for r in range(h)]


def turn(tokens, w, top, way="cw", fill=False):
    """One quarter turn. fill=True: blank cells come out as NULL fillers instead of vanishing."""
    rows = grid(tokens, w, top)
    h = len(rows)
    cols = range(w) if way == "cw" else range(w - 1, -1, -1)
    rr = range(h - 1, -1, -1) if way == "cw" else range(h)
    out = []
    for c in cols:
        for r in rr:
            t = rows[r][c]
            if t is None:
                if fill:
                    out.append(NULL)
            else:
                out.append(t)
    return out


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


def where_of_turns(seq):
    s = list(range(N))
    for w, way in seq:
        s = turn(s, w, False, way)
    wh = [0] * N
    for j, i in enumerate(s):
        wh[i] = j
    return wh


def route_sets(vocab):
    """Yields (set name, tag, where) for every route, deduplicated across sets."""
    seen = set()

    def emit(name, tag, wh):
        for d, r in (("", wh), (" inverse", None)):
            if r is None:
                r = [0] * N
                for i, j in enumerate(wh):
                    r[j] = i
            k = tuple(r)
            h = hash(k)
            if h in seen:
                continue
            seen.add(h)
            yield name, tag + d, k
    for tag, wh in route_library(vocab):
        k = tuple(wh)
        if hash(k) not in seen:
            seen.add(hash(k))
            yield "type-1 library", tag, k
    for w in range(2, N):
        P = paths(w)
        for a in P:
            for b in P:
                if a != b:
                    yield from emit("grid paths", f"w{w} {a} -> {b}", route(P[a], P[b]))
    single = {(w, way): where_of_turns([(w, way)]) for w in range(2, N) for way in ("cw", "ccw")}
    for d1, d2 in (("cw", "ccw"), ("ccw", "cw"), ("ccw", "ccw")):
        for w1 in range(2, N):
            for w2 in range(2, N):
                a, b = single[(w1, d1)], single[(w2, d2)]
                yield from emit("mixed double turns", f"{d1} {w1}, {d2} {w2}", [b[a[i]] for i in range(N)])
    for w1 in range(2, N):
        a = single[(w1, "cw")]
        for w2 in range(2, N):
            b = single[(w2, "cw")]
            ab = [b[a[i]] for i in range(N)]
            for w3 in range(2, N):
                c = single[(w3, "cw")]
                yield from emit("triple clockwise turns", f"cw {w1}, {w2}, {w3}", [c[ab[i]] for i in range(N)])


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    places = sorted(known)
    pidx = [p - 1 for p in places]
    plain = [known[q] for q in places]
    rng = random.Random(106)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    T = len(texts)
    counts, alive, n_by = {}, [], {}
    stopped = None
    for i, (name, tag, wh) in enumerate(route_sets(ctx.vocabulary)):
        n_by[name] = n_by.get(name, 0) + 1
        land = [wh[j] for j in pidx]
        for t in range(T):
            txt = texts[t]
            f, g, ok = {}, {}, True
            for a, j in zip(plain, land):
                c = txt[j]
                if f.setdefault(a, c) != c or g.setdefault(c, a) != a:
                    ok = False; break
            if ok:
                counts.setdefault(name, [0] * T)[t] += 1
                if t == 0:
                    alive.append((name, tag, wh, dict(f)))
        if i % 20000 == 0 and ctx.time_left() < 60:
            stopped = (name, tag)
            break
    cands = []
    best = []
    for name, tag, wh, f in alive:
        inv = {c: a for a, c in f.items()}
        pt = "".join(inv.get(ct[wh[i]], ".") for i in range(N))
        fixed = sum(1 for x in pt if x != ".")
        best.append({"set": name, "route": tag, "letters_fixed": fixed, "reading": pt})
    best.sort(key=lambda r: -r["letters_fixed"])
    bounds = {"family": "one-to-one substitution (commutes with the move) with four route sets",
              "routes_by_set": n_by, "stopped": stopped,
              "consistent_by_set": {k: {"k4": v[0], "controls": v[1:]} for k, v in counts.items()},
              "k4_survivors": best[:20], "n_k4_survivors": len(best),
              "controls": f"{N_CONTROLS} shuffled coppers (seed 106), identical test"}
    notes = (f"Routes tested: {n_by}. Consistent (K4 / controls): "
             + ("; ".join(f"{k}: {v[0]} / {v[1:]}" for k, v in counts.items()) or "none on any text")
             + (f". Stopped at {stopped} for time." if stopped else "."))
    return {"candidates": cands, "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    P = paths(10)
    wh = route(P["snake rows"], P["columns"])
    lines = ["snake rows of 10, read by columns: the known letters and the carved letters where they land", "",
             "letter  places (lands at: carved)"]
    by = {}
    for q in sorted(known):
        by.setdefault(known[q], []).append(f"{q} ({wh[q - 1] + 1}: {ct[wh[q - 1]]})")
    for a in sorted(by):
        lines.append(f"{a:>6}  " + ", ".join(by[a]))
    lines += ["", "a single swap table needs every row to show one carved letter, different from every other row"]
    return "\n".join(lines)
