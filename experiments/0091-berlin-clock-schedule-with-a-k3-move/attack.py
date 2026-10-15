"""Experiment 0091. See program.md for the contract."""

EXPERIMENT = {
    "slug": "berlin-clock-schedule-with-a-k3-move",
    "title": "The Berlin clock as a key schedule, joined to a K3-style move before or after the table",
    "family": "6-transposition-then-tableau",
    "parent": "0079-berlin-clock-as-a-key-schedule",
    "changed": "0079 read the key off the set-theory clock with no move. Here each of its 60,480 schedules (six readings, seven steps, every start minute) is joined to every move of the type-1 route library (27,852 distinct routes), the move either before the table or after it. A schedule plus a constant leaves no free letter, so both orders are exact tests.",
    "hypothesis_expert": (
        "Type 6 of directions.md: 'the same schedules combined with a moving stage (type 1)'. Scheidt: the system is "
        "'simple, can be remembered' (C5); Sanborn pointed at the Mengenlehreuhr in 2014 and said BERLINCLOCK is a clue "
        "(C14, C11a). Schedules as in 0079: lit lamps, hour, minute, hour plus minute, the five-minute row and the time's "
        "digits, the clock advancing 1, 2, 3, 5, 10, 15 or 30 minutes per letter from every start minute, key value mod 26 "
        "plus one free constant. Moves as in 0090 (K3's rule, one or two quarter turns, plain and true-keyword columnar, "
        "forward and inverse). Change then move: the 23 key differences forced at the crib places must equal the "
        "schedule's, a dictionary lookup. Move then change: the clock runs over carved places, so the forced differences "
        "sit at the moved crib places; candidates come from a pair index and are filtered check by check (the time-digit "
        "reading only at one minute per letter here, where it is a cyclic text). 12 conventions (Vigenere, Beaufort, "
        "variant Beaufort; plain and cipher numbered on standard or KRYPTOS). The Carter and dedication dates of 0038 are "
        "periodic keys of period at most 10 and are covered exactly by 0080 and 0083. Ten shuffled coppers."
    ),
    "hypothesis_eli5": (
        "Experiment 79 used the Berlin clock as the key: set it to some time, read off a number for each letter, and "
        "move the clock on by a fixed number of minutes per letter. It found nothing. Sanborn also said he moved letters "
        "around in grids before going back to the table, so here every clock key is joined to every grid move of "
        "experiments 80 to 83, with the move before or after the table. A clock key has no free letters, so each "
        "combination either explains all 24 known letters or it does not."
    ),
    "prediction": (
        "No combination explains all 24 known letters in either order. Change then move: no schedule matches either "
        "whole crib stretch beyond the scrambled-copper count. Move then change: the deepest partial match is about "
        "6-8 checks, inside the scrambled-copper range. Zero candidates."
    ),
    "method": (
        "1. Build the 60,480 clock schedules and the deduplicated route library. "
        "2. Change then move: for each route and convention, undo the move at the 24 crib places, compute the forced "
        "key numbers and their differences from the first, and look them up in an index of every schedule's "
        "differences at the crib places (all 24, and each crib stretch alone). "
        "3. Move then change: for each clock reading and step, find the start minutes that agree at the first two moved "
        "crib places through a pair index, then filter by the other places, recording the deepest agreement. "
        "4. K4 first, then ten shuffled coppers as time allows. 5. Decrypt and return any full match."
    ),
    "walkthrough": (
        "1. Set the clock to 00:00 and advance it one minute per letter; the key number for a letter is the count of lit lamps. "
        "2. Pick a move, say a clockwise quarter turn of a grid 8 letters wide. "
        "3. Change then move: E of place 22 ends up at some carved place j; find the number that turns E into the carved letter there. "
        "4. That number minus the lamp count at place 22 must be the same for all 24 known places. "
        "5. Move then change: the clock runs along the carved text instead, so compare the needed number with the lamp count at place j. "
        "6. Repeat for every start minute, step, clock reading, move and table rule."
    ),
}

import random, bisect
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.ciphers import columnar_transposition_encrypt
from kryptos.alphabets import numeric_order

N = 97
N_CONTROLS = 10
AL = {"std": STD, "kry": KRY}
IDX = {k: {c: i for i, c in enumerate(a)} for k, a in AL.items()}
EXTRA = ["EGYPT", "CAIRO", "LUXOR", "WALL", "NOVEMBER", "MESSAGE", "DELIVER", "DELIVERING", "TRANSMIT"]
STEPS = (1, 2, 3, 5, 10, 15, 30)
NAMES = ("lit lamps", "hour", "minute", "hour plus minute", "five-minute row", "time digits")


def clock_value(name, t):
    h, m = divmod(t % 1440, 60)
    return {"lit lamps": h // 5 + h % 5 + m // 5 + m % 5, "hour": h, "minute": m, "hour plus minute": h + m,
            "five-minute row": m // 5}[name] % 26


def schedule(name, t0, step, n=N):
    if name == "time digits":
        digs, t = [], t0
        while len(digs) < n:
            h, m = divmod(t % 1440, 60)
            digs += [h // 10, h % 10, m // 10, m % 10]
            t += step
        return digs[:n]
    return [clock_value(name, t0 + i * step) for i in range(n)]


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


def enc(mode, p, k):
    return {"vig": (p + k) % 26, "beau": (k - p) % 26, "varb": (p - k) % 26}[mode]


def key_for(mode, p, c):
    """k with enc(mode, p, k) = c."""
    return {"vig": (c - p) % 26, "beau": (c + p) % 26, "varb": (p - c) % 26}[mode]


def dec(mode, c, k):
    return {"vig": (c - k) % 26, "beau": (k - c) % 26, "varb": (c + k) % 26}[mode]


CONVS = [(m, pa, ca) for m in ("vig", "beau", "varb") for pa in ("std", "kry") for ca in ("std", "kry")]


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    places = sorted(known)
    pidx = [p - 1 for p in places]
    lib = route_library(ctx.vocabulary)
    rng = random.Random(91)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))

    # ---- change then move: schedule values at the crib places, as differences from the first
    ix24, ix13, ix11 = {}, {}, {}
    n_sched = 0
    for name in NAMES:
        for step in STEPS:
            for t0 in range(1440):
                sc = schedule(name, t0, step)
                n_sched += 1
                v = [sc[j] for j in pidx]
                d24 = tuple((x - v[0]) % 26 for x in v[1:])
                ix24.setdefault(d24, []).append((name, step, t0))
                ix13.setdefault(d24[:12], []).append((name, step, t0))
                ix11.setdefault(tuple((x - v[13]) % 26 for x in v[14:]), []).append((name, step, t0))
    A_full = [[] for _ in texts]; A13 = [0] * len(texts); A11 = [0] * len(texts); A_hits = []
    for tag, where in lib:
        for conv in CONVS:
            mode, pa, ca = conv
            P, C = IDX[pa], IDX[ca]
            for t, txt in enumerate(texts):
                T = [key_for(mode, P[known[p]], C[txt[where[p - 1]]]) for p in places]
                d24 = tuple((x - T[0]) % 26 for x in T[1:])
                if d24 in ix24:
                    A_full[t].append((tag, conv, T[0], ix24[d24][:3]))
                if d24[:12] in ix13:
                    A13[t] += 1
                    if t == 0:
                        A_hits.append({"route": tag, "conv": "/".join(conv), "stretch": "EASTNORTHEAST", "schedules": ix13[d24[:12]][:3]})
                d11 = tuple((x - T[13]) % 26 for x in T[14:])
                if d11 in ix11:
                    A11[t] += 1
                    if t == 0:
                        A_hits.append({"route": tag, "conv": "/".join(conv), "stretch": "BERLINCLOCK", "schedules": ix11[d11][:3]})

    # ---- move then change: the clock runs over carved places
    Y = {name: [clock_value(name, t) for t in range(1440)] for name in NAMES if name != "time digits"}
    digits = []
    for t in range(1440):
        h, m = divmod(t, 60)
        digits += [h // 10, h % 10, m // 10, m % 10]
    families = [(name, step, Y[name], 1440, step) for name in Y for step in STEPS] + [("time digits", 1, digits, len(digits), 1)]
    pair_cache = {}

    def pairs(fi, g):
        key = (fi, g)
        if key not in pair_cache:
            _, _, y, L, _ = families[fi]
            d = {}
            for u in range(L):
                d.setdefault((y[(u + g) % L] - y[u]) % 26, []).append(u)
            pair_cache[key] = d
        return pair_cache[key]
    B_full, B_top = [], []
    B_depth = [None] * len(texts); B_hist = [dict() for _ in texts]
    done_texts = 0
    for t, txt in enumerate(texts):
        if t > 0 and ctx.time_left() < 120:
            break
        best = 0
        for tag, where in lib:
            q = [where[j] for j in pidx]
            order = sorted(range(24), key=lambda e: q[e])
            for conv in CONVS:
                mode, pa, ca = conv
                P, C = IDX[pa], IDX[ca]
                T = [key_for(mode, P[known[places[e]]], C[txt[q[e]]]) for e in range(24)]
                for fi, (name, step, y, L, mul) in enumerate(families):
                    e0, e1 = order[0], order[1]
                    r = [q[e] * mul for e in order]
                    g = (r[1] - r[0]) % L
                    cand = pairs(fi, g).get((T[e1] - T[e0]) % 26, ())
                    depth = 2 if cand else 1
                    if cand:
                        base = T[e0]
                        for k in range(2, 24):
                            e = order[k]; rr = r[k] - r[0]; want = T[e]
                            cand = [u for u in cand if (y[(u + rr) % L] - y[u] - want + base) % 26 == 0]
                            if not cand:
                                break
                            depth += 1
                    if depth > best:
                        best = depth
                    B_hist[t][depth] = B_hist[t].get(depth, 0) + 1
                    if t == 0:
                        if depth == 24:
                            for u in cand:
                                B_full.append((tag, conv, name, step, (u - r[0]) % L, (T[e0] - y[u]) % 26))
                        if depth >= 8:
                            B_top.append({"route": tag, "conv": "/".join(conv), "reading": name, "step": step, "depth": depth})
        B_depth[t] = best
        done_texts += 1
    B_top.sort(key=lambda x: -x["depth"])

    cands = []
    for tag, conv, T0, hits in A_full[0]:
        name, step, t0 = hits[0]
        where = dict(lib)[tag]; mode, pa, ca = conv
        sc = schedule(name, t0, step)
        c0 = (T0 - sc[pidx[0]]) % 26
        cands.append({"plaintext": "".join(AL[pa][dec(mode, IDX[ca][ct[where[i]]], (sc[i] + c0) % 26)] for i in range(N)),
                      "key": f"change then move: clock {name} step {step} from {t0 // 60:02d}:{t0 % 60:02d} + {c0}, {tag}, {'/'.join(conv)}"})
    for tag, conv, name, step, u0, c0 in B_full:
        where = dict(lib)[tag]; mode, pa, ca = conv
        fam = [f for f in families if f[0] == name and f[1] == step][0]
        y, L = fam[2], fam[3]
        mid = [AL[pa][dec(mode, IDX[ca][ct[j]], (y[(u0 + j * step) % L] + c0) % 26)] for j in range(N)]
        cands.append({"plaintext": "".join(mid[where[i]] for i in range(N)),
                      "key": f"move then change: clock {name} step {step} start index {u0} + {c0}, {tag}, {'/'.join(conv)}"})
    bounds = {
        "routes_distinct": len(lib), "conventions": len(CONVS), "schedules": n_sched,
        "readings": list(NAMES), "steps_minutes": list(STEPS), "start_minutes": 1440,
        "change_then_move": {"k4_full": len(A_full[0]), "controls_full": [len(x) for x in A_full[1:]],
                             "k4_stretch13": A13[0], "controls_stretch13": A13[1:],
                             "k4_stretch11": A11[0], "controls_stretch11": A11[1:], "k4_stretch_hits": A_hits[:20]},
        "move_then_change": {"clock_families": len(families), "time_digits_steps": [1],
                             "k4_full": len(B_full), "k4_best_depth": B_depth[0], "controls_best_depth": B_depth[1:done_texts],
                             "controls_completed": done_texts - 1,
                             "k4_depth_histogram": dict(sorted(B_hist[0].items())), "k4_top": B_top[:15]},
        "carter_dates": "periodic keys of period at most 10: covered exactly by 0080 and 0083",
        "controls": f"{N_CONTROLS} shuffled coppers (seed 91), identical search",
    }
    notes = (f"{len(lib):,} routes x {len(CONVS)} conventions x {n_sched:,} clock schedules. Change then move: full K4 "
             f"{len(A_full[0])}, controls {[len(x) for x in A_full[1:]]}; EASTNORTHEAST stretch {A13[0]} (controls {A13[1:]}); "
             f"BERLINCLOCK stretch {A11[0]} (controls {A11[1:]}). Move then change: full {len(B_full)}, deepest K4 "
             f"{B_depth[0]}, controls {B_depth[1:done_texts]} ({done_texts - 1} completed).")
    return {"candidates": cands, "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    sigma = perm_of(lambda x: rot_cw(x, 8))
    where = [0] * N
    for j, i in enumerate(sigma):
        where[i] = j
    I = IDX["kry"]
    sc = schedule("lit lamps", 0, 1)
    lines = ["clock from 00:00, one minute per letter, lit lamps; move: clockwise quarter turn of a grid 8 wide;",
             "sculpture's alphabet, Vigenere", "",
             "change then move: needed number minus lamps at the message place must be constant",
             "place  known  moved to  carved  needed  lamps  difference"]
    for p in (22, 23, 24, 25, 64):
        j = where[p - 1]; need = (I[ct[j]] - I[known[p]]) % 26
        lines.append(f"{p:>5}  {known[p]:>5}  {j + 1:>8}  {ct[j]:>6}  {need:>6}  {sc[p - 1]:>5}  {(need - sc[p - 1]) % 26:>10}")
    lines += ["", "move then change: the lamps are read at the carved place instead",
              "place  known  moved to  carved  needed  lamps  difference"]
    for p in (22, 23, 24, 25, 64):
        j = where[p - 1]; need = (I[ct[j]] - I[known[p]]) % 26
        lines.append(f"{p:>5}  {known[p]:>5}  {j + 1:>8}  {ct[j]:>6}  {need:>6}  {sc[j]:>5}  {(need - sc[j]) % 26:>10}")
    return "\n".join(lines)
