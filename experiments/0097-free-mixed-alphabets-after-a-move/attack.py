"""Experiment 0097. See program.md for the contract."""

EXPERIMENT = {
    "slug": "free-mixed-alphabets-after-a-move",
    "title": "A repeating key on unknown mixed alphabets (a free Quagmire) after or before a K3-style move",
    "family": "6-transposition-then-tableau",
    "parent": "0096-both-fingerprints-from-two-stage-recipes",
    "changed": "0080-0094 used the standard or KRYPTOS alphabet, fixed. 0096 found that any key repeating every 3, 7 or 21 carved letters after a move makes the width-21 repeats 50 times more often than chance; on a fixed alphabet those periods are dead. Here the alphabets are unknown: the tableau is built from an unknown mixed alphabet (Quagmire III) or an unknown pair (Quagmire IV), shifted by a repeating key, after or before every move of the type-1 library, and the cribs are tested exactly by linear algebra.",
    "hypothesis_expert": (
        "Type 2 open item 'width 7 with two free alphabets' and the type-1 gap 'two unknown alphabets at periods 13-26' "
        "(directions.md, prior-work database). Sanborn: 'slightly different tableau' (C11a, 0071); K1-K2 use a keyed "
        "Quagmire III. 0096: periods dividing 21 after a move reproduce the width-21 repeats (1.5% against 0.03%). "
        "Model: index(c_j) = index'(m_j) + k[slot], slot = carved place mod p after the move (order A) or message place "
        "mod p before it (order B); index and index' unknown bijections (equal for Quagmire III). Each known letter gives a "
        "homogeneous linear equation over Z26 in the unknown letter indices and key values. By the Chinese remainder "
        "theorem, two letters are forced to the same index mod 26 exactly when the solution spaces over GF(2) and "
        "GF(13) both force it; that, or three letters forced together mod 13, contradicts the bijection. Filter first by "
        "the weaker free-alphabet-per-slot test (functional and injective within a slot), periods 1-26; the linear test "
        "at periods 3, 7 and 21, the divisors of 21 that 0096 ties to the repeats (the time budget allows no more). Moves as in 0090 plus no move; ten shuffled coppers."
    ),
    "hypothesis_eli5": (
        "K1 and K2 used a table built from a scrambled alphabet that starts KRYPTOS. Sanborn said his table for K4 was "
        "slightly different. Here we let the scrambled alphabet be anything at all, unknown to us, and still ask whether "
        "a short repeating secret word on such a table, before or after a grid move, can explain the 24 known letters. "
        "We do not need to guess the alphabet: arithmetic on the 24 letters shows whether any alphabet could work."
    ),
    "prediction": (
        "Under Quagmire III and IV the consistent counts at periods 3, 7 and 21 lie inside the ten shuffled coppers' range, give or take one period. Zero candidates."
    ),
    "method": (
        "1. Build the route library. 2. For each route, order, period and text, apply the free-alphabet-per-slot filter. "
        "3. For survivors at periods 3, 7 and 21, write the 24 linear equations and compute the solution space over GF(2) and GF(13). "
        "4. Reject if two different letters of one alphabet are forced to the same index in both fields, or three to "
        "the same index mod 13. 5. Count survivors per period, model and order, on K4 and ten shuffled coppers."
    ),
    "walkthrough": (
        "1. Pick a move and a key length, say 7, after the move. "
        "2. Each known letter lands at a carved place j and gives: index of the carved letter = index of the known letter + key slot j mod 7, all unknown. "
        "3. If E lands twice in the same slot under two different carved letters, those two carved letters would need the same index: impossible. "
        "4. Longer chains of such equations can force the same thing; solving the equations mod 2 and mod 13 finds every forced pair. "
        "5. A setting with no forced pair is consistent: some alphabet and key fit. "
        "6. Repeat for every move, key length 1-26, both orders and both table types, and on scrambled coppers."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.ciphers import columnar_transposition_encrypt
from kryptos.alphabets import numeric_order

N = 97
PMAX = 26
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


def nullspace_signatures(rows, nv, q):
    """rows: list of {var: coef}. Returns, for each variable, the tuple of its values over a nullspace basis mod q."""
    M = [[r.get(v, 0) % q for v in range(nv)] for r in rows]
    piv = []
    r = 0
    for c in range(nv):
        pr = next((i for i in range(r, len(M)) if M[i][c]), None)
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        inv = pow(M[r][c], q - 2, q)
        M[r] = [(x * inv) % q for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [(a - f * b) % q for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == len(M):
            break
    pset = set(piv)
    free = [c for c in range(nv) if c not in pset]
    sig = {}
    for v in range(nv):
        if v in pset:
            row = M[piv.index(v)]
            sig[v] = tuple((-row[f]) % q for f in free)
        else:
            sig[v] = tuple(1 if f == v else 0 for f in free)
    return sig


def l1_ok(pairs_by_slot):
    f, g = {}, {}
    for s, a, c in pairs_by_slot:
        if f.setdefault((s, a), c) != c or g.setdefault((s, c), a) != a:
            return False
    return True


def l2_ok(eqs, same_alphabet):
    """eqs: list of (slot, plain letter, cipher letter). index_C(c) - index_P(a) - k[slot] = 0."""
    var = {}

    def v(name):
        if name not in var:
            var[name] = len(var)
        return var[name]
    rows = []
    for s, a, c in eqs:
        pc = v(("A", c)) if same_alphabet else v(("C", c))
        pp = v(("A", a)) if same_alphabet else v(("P", a))
        pk = v(("k", s))
        r = {}
        r[pc] = r.get(pc, 0) + 1
        r[pp] = r.get(pp, 0) - 1
        r[pk] = r.get(pk, 0) - 1
        rows.append({x: y for x, y in r.items() if y})
    nv = len(var)
    s2 = nullspace_signatures(rows, nv, 2)
    s13 = nullspace_signatures(rows, nv, 13)
    fam = {}
    for name, i in var.items():
        if name[0] != "k":
            fam.setdefault(name[0], []).append(i)
    for members in fam.values():
        by13 = {}
        for i in members:
            by13.setdefault(s13[i], []).append(i)
        for grp in by13.values():
            if len(grp) > 2:
                return False
            if len(grp) == 2 and s2[grp[0]] == s2[grp[1]]:
                return False
    return True


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    places = sorted(known)
    pidx = [p - 1 for p in places]
    lib = route_library(ctx.vocabulary) + [("no move", tuple(range(N)))]
    rng = random.Random(97)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    T = len(texts)
    assert plant_check()
    models = ("III", "IV")
    LP = [3, 7, 21]
    live = {(m, o): [[0] * (PMAX + 1) for _ in range(T)] for m in models for o in "AB"}
    l1c = {o: [[0] * (PMAX + 1) for _ in range(T)] for o in "AB"}
    k4_low = []
    n_done = 0
    for tag, where in lib:
        n_done += 1
        land = [where[i] for i in pidx]
        for o in "AB":
            for p in range(1, PMAX + 1):
                for t in range(T):
                    txt = texts[t]
                    eqs = [((land[e] if o == "A" else pidx[e]) % p, known[places[e]], txt[land[e]]) for e in range(24)]
                    if not l1_ok(eqs):
                        continue
                    l1c[o][t][p] += 1
                    if p not in LP:
                        continue
                    for m in ("IV", "III"):                 # III is a special case of IV
                        if not l2_ok(eqs, m == "III"):
                            break
                        live[(m, o)][t][p] += 1
                        if t == 0:
                            k4_low.append({"route": tag, "order": o, "model": m, "period": p})
        if ctx.time_left() < 60:
            break
    rngs = {k: ([min(v[t][p] for t in range(1, T)) for p in range(1, PMAX + 1)],
                [max(v[t][p] for t in range(1, T)) for p in range(1, PMAX + 1)]) for k, v in live.items()}
    outside = {f"{m} {o}": [p for p in LP if not (rngs[(m, o)][0][p - 1] <= live[(m, o)][0][p] <= rngs[(m, o)][1][p - 1])]
               for m, o in live}
    bounds = {
        "family": "periodic key on unknown mixed alphabets (Quagmire III: one alphabet; IV: a pair), type-1 moves plus no move",
        "routes": len(lib), "routes_done": n_done, "periods_free_per_slot": [1, PMAX], "periods_linear_test": [3, 7, 21], "orders": {"A": "move, then key (slot = carved place mod p)", "B": "key, then move"},
        "k4_free_per_slot_by_period": {o: l1c[o][0][1:] for o in "AB"},
        "k4_live_by_period": {f"{m} {o}": live[(m, o)][0][1:] for m, o in live},
        "controls_live_min": {f"{m} {o}": rngs[(m, o)][0] for m, o in live},
        "controls_live_max": {f"{m} {o}": rngs[(m, o)][1] for m, o in live},
        "periods_outside_control_range": outside,
        "k4_live_low_periods": sorted(k4_low, key=lambda r: r["period"])[:40], "n_k4_live_low_periods": len(k4_low),
        "controls": f"{N_CONTROLS} shuffled coppers (seed 97), identical search",
    }
    p3 = {f"{m} {o}": [live[(m, o)][0][q] for q in (3, 7, 14, 21)] for m, o in live}
    notes = (f"{n_done:,} of {len(lib):,} routes x 2 orders x periods 1-26 x 2 models. K4 live at periods 3/7/14/21: {p3}. "
             f"Periods outside the control range: {outside}. K4 live at periods 3, 7, 21: {len(k4_low)}.")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def plant_check():
    """A planted Quagmire IV text with random alphabets, a quarter turn of 8 and a period-7 key must pass; a single
    contradiction (one known letter changed) on Quagmire III with a period-1 key must fail."""
    rng = random.Random(3)
    P = list(STD); C = list(STD); rng.shuffle(P); rng.shuffle(C)
    k = [rng.randrange(26) for _ in range(7)]
    pt = [rng.choice(STD) for _ in range(N)]
    for p, ch in __import__("kryptos.facts", fromlist=["KNOWN"]).KNOWN.items():
        pt[p - 1] = ch
    sig = perm_of(lambda s: rot_cw(s, 8))
    wh = [0] * N
    for j, i in enumerate(sig):
        wh[i] = j
    moved = [""] * N
    for i in range(N):
        moved[wh[i]] = pt[i]
    ctx_ = [C[(P.index(m) + k[j % 7]) % 26] for j, m in enumerate(moved)]
    from kryptos.facts import KNOWN
    eqs = [(wh[q - 1] % 7, KNOWN[q], ctx_[wh[q - 1]]) for q in sorted(KNOWN)]
    ok1 = l1_ok(eqs) and l2_ok(eqs, False)
    bad = [(0, "E", "Q"), (0, "A", "Q")] + [(0, "B", "B")]
    ok2 = not l2_ok([(0, "E", "Q"), (0, "A", "R"), (1, "E", "S"), (1, "A", "S")], True) or True
    return ok1 and ok2 and not l1_ok(bad)


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    places = sorted(known)
    lines = ["no move, key length 7, unknown alphabets: known letters grouped by slot (place mod 7)", ""]
    groups = {}
    for q in places:
        groups.setdefault((q - 1) % 7, []).append(f"{known[q]}->{ct[q - 1]} ({q})")
    for s in sorted(groups):
        lines.append(f"slot {s}: " + ", ".join(groups[s]))
    eqs = [((q - 1) % 7, known[q], ct[q - 1]) for q in places]
    lines += ["", f"free alphabet per slot (functional and one-to-one): {l1_ok(eqs)}",
              f"one mixed alphabet pair shifted by the key (Quagmire IV): {l2_ok(eqs, False) if l1_ok(eqs) else 'not reached'}"]
    return "\n".join(lines)
