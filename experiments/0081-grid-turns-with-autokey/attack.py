"""Experiment 0081. See program.md for the contract."""

EXPERIMENT = {
    "slug": "grid-turns-with-autokey",
    "title": "A grid turn or K3's rule joined to an autokey, the message (or the cipher) feeding its own key, in both orders",
    "family": "6-transposition-then-tableau",
    "parent": "0063-transposition-and-ciphertext-autokey",
    "changed": "0063 joined column shuffles to the ciphertext autokey only. Here the routes are K3's rule at every setting, one or two quarter turns at every width, and plain and keyed columnar, and the autokey is either kind: the plaintext autokey, which the NSA named in 1992 and which no public search has joined to a grid turn, and the ciphertext autokey. Both orders, every lag 1-96, on one alphabet throughout (standard or KRYPTOS), solved exactly.",
    "hypothesis_expert": (
        "Type 1 of directions.md, gap a2 of the prior-work database ('Rotation + plaintext autokey on the KA tableau... "
        "autokey under transposition is covered only for columnar <= 7 publicly; 0063 covered ciphertext autokey only'); "
        "also type 2's open item 'columnar plus autokey above width 7' (nitsuah). Clues C1(a) (02-sanborn-said.md, CNN "
        "2005, 'double matrixes... then went back to this table'), C2(a) (the K3 matrix and its shifts) and C11a (NSA 1992, "
        "'plain-text auto-key', Black Vault). Plaintext autokey at lag L on one alphabet A: C[j] = Z[j] (+) Z[j-L], so "
        "decryption is Z[j] = sigma Z[j-L] + tau C[j] (Vigenere sigma = -1, tau = 1; Beaufort 1, -1; variant 1, 1), linear "
        "mod 26 along each residue class mod L; two known letters in one class give one exact check, whatever the primer. "
        "Ciphertext autokey: Z[j] = dec(C[j], C[j-L]), every known letter past the primer is a check. Order A: move the "
        "message, then the autokey on the moved text (known letters at their landing places, W = the copper). Order B: "
        "autokey on the message, then move (known letters in place, W = the copper unmoved). Routes as 0080: K3's rule "
        "a + b i mod 97 (9,312), one quarter turn cw or ccw at widths 2-96, two cw turns at every width pair 2-96, plain "
        "columnar both directions, keyed columnar from every vocabulary word, each forward and inverse, deduplicated "
        "(27,752). Six conventions (one alphabet throughout, as on the carved table, three modes). Lags 1-96. Exact; ten "
        "shuffled coppers through the identical search. Left open: mixed plain/cipher/key alphabets with these routes, "
        "padded grids (gap a1)."
    ),
    "hypothesis_eli5": (
        "In an autokey cipher the secret word is used only to start; after that, each letter is hidden using a letter "
        "of the message itself from a fixed distance back (or a letter of the hidden text, in the other kind). The "
        "code-breakers at the NSA guessed in 1992 that K4 might be one. Here it is joined to the grid turn of the third "
        "message: turn first and then autokey, or autokey first and then turn. Because each letter is tied to the one "
        "a fixed distance back, two known letters the right distance apart must agree, whatever the starting word. We "
        "test every turn, every distance and both kinds, exactly, and the same on ten scrambled coppers."
    ),
    "prediction": (
        "No setting on K4 survives four or more checks in either kind or order. At every number of checks the count of "
        "consistent settings on K4 lies inside the range of the ten shuffled coppers, give or take the spread at one "
        "and two checks. Zero candidates."
    ),
    "method": (
        "1. Build the routes and keep one per distinct reordering. 2. For each route, lag, convention and order, list "
        "the pairs of known letters in the same class mod the lag (plaintext autokey) or the known letters past the "
        "primer (ciphertext autokey). 3. Walk each pair's chain through the copper, or through the copper unmoved, and "
        "compare; stop at the first disagreement. 4. Count consistent settings by number of checks. 5. Repeat on ten "
        "shuffled coppers. 6. Print any K4 setting with four or more checks."
    ),
    "walkthrough": (
        "1. Write the message in rows of 7 and turn the grid a quarter clockwise (columns read bottom-up, left column first). The L of CLOCK (place 71) lands at place 4 and the O after it (place 72) at place 18. 2. Take the plaintext autokey at lag 14 on the sculpture's alphabet, Vigenere: each letter of the turned text is the copper letter minus the turned-text letter 14 places earlier. 3. Places 4 and 18 are 14 apart, so they are tied directly. 4. The copper at 18 is F, index 12; L is index 17; 12 - 17 = -5, which is 21, the letter U. 5. The known letter there is O, not U: lag 14 under this turn is dead. 6. Do the same for every pair of known letters in one class of the lag, every lag, turn and table, in both orders and for the ciphertext autokey, and on ten scrambled coppers."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.alphabets import numeric_order
from kryptos.ciphers import columnar_transposition_encrypt, columnar_transposition_decrypt

N = 97
LAGS = range(1, N)
ALPH = {"std": STD, "kry": KRY}
N_CONTROLS = 10


def perm_of(fn):
    """sigma with out[j] = in[sigma[j]] for a string transform fn."""
    idx = "".join(chr(0x100 + i) for i in range(N))
    return [ord(ch) - 0x100 for ch in fn(idx)]


def rot_cw(s, w):
    """Rows of w, columns read bottom-up, left column first (a quarter turn clockwise)."""
    rows = [s[i:i + w] for i in range(0, len(s), w)]
    return "".join(r[c] for c in range(w) for r in reversed(rows) if c < len(r))


def rot_ccw(s, w):
    """Rows of w, columns read top-down, right column first (a quarter turn anticlockwise)."""
    rows = [s[i:i + w] for i in range(0, len(s), w)]
    return "".join(r[c] for c in reversed(range(w)) for r in rows if c < len(r))


def route_specs(vocab):
    for b in range(1, N):
        for a in range(N):
            yield {"kind": "k3rule", "a": a, "b": b}
    for w in range(2, N):
        for turn in ("cw", "ccw"):
            for d in ("fwd", "inv"):
                yield {"kind": "turn", "w": w, "turn": turn, "dir": d}
        for rtl in (False, True):
            for d in ("fwd", "inv"):
                yield {"kind": "columnar", "w": w, "rtl": rtl, "dir": d}
    for w1 in range(2, N):
        for w2 in range(2, N):
            for d in ("fwd", "inv"):
                yield {"kind": "turn2", "w1": w1, "w2": w2, "dir": d}
    for word in vocab:
        if 2 <= len(word) <= 40:
            for d in ("fwd", "inv"):
                yield {"kind": "keyed", "word": word, "dir": d}


def forward_fn(spec):
    k = spec["kind"]
    if k == "k3rule":
        a, b = spec["a"], spec["b"]

        def f(s):
            out = [""] * N
            for i in range(N):
                out[(a + b * i) % N] = s[i]
            return "".join(out)
        return f
    if k == "turn":
        r = rot_cw if spec["turn"] == "cw" else rot_ccw
        return lambda s, w=spec["w"]: r(s, w)
    if k == "turn2":
        return lambda s, a=spec["w1"], b=spec["w2"]: rot_cw(rot_cw(s, a), b)
    if k == "columnar":
        o = list(range(spec["w"]))[::-1] if spec["rtl"] else list(range(spec["w"]))
        return lambda s, o=o: columnar_transposition_encrypt(s, o)
    o = numeric_order(spec["word"])
    return lambda s, o=o: columnar_transposition_encrypt(s, o)


def where_of(spec):
    """where[i] = place in the moved text of letter i of the changed message (0-indexed)."""
    sigma = perm_of(forward_fn(spec))          # moved[j] = changed[sigma[j]]
    if spec.get("dir", "fwd") == "inv":       # the inverse move: moved[sigma[j]] = changed[j]
        return list(sigma)
    w = [0] * N
    for j, i in enumerate(sigma):
        w[i] = j
    return w


def move(spec, s):
    w = where_of(spec)
    out = [""] * N
    for i, ch in enumerate(s):
        out[w[i]] = ch
    return "".join(out)


def unmove(spec, s):
    w = where_of(spec)
    return "".join(s[w[i]] for i in range(N))



MODES = {"vig": (-1, 1), "beau": (1, -1), "var": (1, 1)}   # plaintext autokey: Z[j] = sig Z[j-L] + tau W[j]


def ct_dec(mode, c, k):
    return {"vig": (c - k) % 26, "beau": (k - c) % 26, "var": (c + k) % 26}[mode]


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    vocab = list(ctx.vocabulary)
    places = sorted(known)
    pidx = [p - 1 for p in places]
    rng = random.Random(81)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    convs = [(an, m) for an in ALPH for m in MODES]
    # text letters and known letters as indices on each alphabet
    TI = {an: [[{c: i for i, c in enumerate(ALPH[an])}[ch] for ch in t] for t in texts] for an in ALPH}
    KI = {an: [{c: i for i, c in enumerate(ALPH[an])}[known[p]] for p in places] for an in ALPH}
    from kryptos.facts import load_k3
    from kryptos.ciphers import k3_formula_decrypt
    k3 = load_k3()
    assert k3_formula_decrypt(k3["ciphertext"]) == k3["plaintext"]
    for spec in ({"kind": "turn2", "w1": 7, "w2": 9, "dir": "fwd"}, {"kind": "turn", "w": 8, "turn": "ccw", "dir": "inv"},
                 {"kind": "keyed", "word": "KRYPTOS", "dir": "fwd"}, {"kind": "k3rule", "a": 5, "b": 7}):
        assert unmove(spec, move(spec, ct)) == ct
    # planted check: plaintext autokey, then a turn (order A) and the reverse (order B), must survive
    planted_ok = plant_check(known)

    seen, routes, n_specs = set(), [], 0
    for spec in route_specs(vocab):
        n_specs += 1
        w = tuple(where_of(spec))
        if w in seen:
            continue
        seen.add(w)
        routes.append((spec, w))
    T = len(texts)
    # counts[(kind, order)][t][c]
    counts = {(k, o): [dict() for _ in range(T)] for k in ("ptak", "ctak") for o in "AB"}
    hits = []
    # order B, plaintext autokey: pairs depend only on the lag
    pairsB = {}
    for L in LAGS:
        last, prs = {}, []
        for e, i in enumerate(pidx):
            r = i % L
            if r in last:
                prs.append((last[r], e))
            last[r] = e
        prs.sort(key=lambda pr: pidx[pr[1]] - pidx[pr[0]])
        pairsB[L] = prs
    stopped = None
    for ri, (spec, w) in enumerate(routes):
        if ctx.time_left() < 60:
            stopped = ri
            break
        land = [w[i] for i in pidx]
        landord = sorted(range(24), key=lambda e: land[e])
        for an, mode in convs:
            sig, tau = MODES[mode]
            KIa = KI[an]
            for t in range(T):
                C = TI[an][t]
                X = [C[w[i]] for i in range(N)]          # the copper unmoved (order B's autokey text)
                for L in LAGS:
                    # ---- plaintext autokey, order A: known Z at landing places, chain through C
                    last, prs = {}, []
                    for e in landord:
                        r = land[e] % L
                        if r in last:
                            prs.append((last[r], e))
                        last[r] = e
                    if prs:
                        ok = True
                        for e1, e2 in prs:
                            z, j, j2 = KIa[e1], land[e1] + L, land[e2]
                            while j <= j2:
                                z = (sig * z + tau * C[j]) % 26; j += L
                            if z != KIa[e2]:
                                ok = False; break
                        if ok:
                            c = len(prs); d = counts[("ptak", "A")][t]; d[c] = d.get(c, 0) + 1
                            if t == 0 and c >= 4:
                                hits.append({"kind": "plaintext autokey", "order": "A", "route": spec, "alphabet": an, "mode": mode, "lag": L, "checks": c})
                    # ---- plaintext autokey, order B: known Z in place, chain through X
                    prs = pairsB[L]
                    if prs:
                        ok = True
                        for e1, e2 in prs:
                            z, j, j2 = KIa[e1], pidx[e1] + L, pidx[e2]
                            while j <= j2:
                                z = (sig * z + tau * X[j]) % 26; j += L
                            if z != KIa[e2]:
                                ok = False; break
                        if ok:
                            c = len(prs); d = counts[("ptak", "B")][t]; d[c] = d.get(c, 0) + 1
                            if t == 0 and c >= 4:
                                hits.append({"kind": "plaintext autokey", "order": "B", "route": spec, "alphabet": an, "mode": mode, "lag": L, "checks": c})
                    # ---- ciphertext autokey, order A: Z[j] = dec(C[j], C[j-L]) at landing places
                    c = 0; ok = True
                    for e in range(24):
                        j = land[e]
                        if j >= L:
                            if ct_dec(mode, C[j], C[j - L]) != KIa[e]:
                                ok = False; break
                            c += 1
                    if ok and c:
                        d = counts[("ctak", "A")][t]; d[c] = d.get(c, 0) + 1
                        if t == 0 and c >= 4:
                            hits.append({"kind": "ciphertext autokey", "order": "A", "route": spec, "alphabet": an, "mode": mode, "lag": L, "checks": c})
                    # ---- ciphertext autokey, order B: P[i] = dec(X[i], X[i-L]) in place
                    c = 0; ok = True
                    for e in range(24):
                        i = pidx[e]
                        if i >= L:
                            if ct_dec(mode, X[i], X[i - L]) != KIa[e]:
                                ok = False; break
                            c += 1
                    if ok and c:
                        d = counts[("ctak", "B")][t]; d[c] = d.get(c, 0) + 1
                        if t == 0 and c >= 4:
                            hits.append({"kind": "ciphertext autokey", "order": "B", "route": spec, "alphabet": an, "mode": mode, "lag": L, "checks": c})
    summary, outside = {}, []
    for (kind, order), per in counts.items():
        mc = max([c for d in per for c in d] + [0])
        ge = lambda d, c0: sum(v for c, v in d.items() if c >= c0)
        k4 = {c0: ge(per[0], c0) for c0 in range(1, 7)}
        ctl = {c0: [ge(per[t], c0) for t in range(1, T)] for c0 in range(1, 7)}
        out = [c0 for c0 in range(1, 7) if not (min(ctl[c0]) <= k4[c0] <= max(ctl[c0]))]
        if out:
            outside.append(f"{kind} {order}: {out}")
        summary[f"{kind} order {order}"] = {"k4_at_least_c": k4, "controls_at_least_c": ctl,
                                            "k4_exactly_c": dict(sorted(per[0].items())), "max_checks_seen": mc}
    bounds = {
        "family": "route (K3 rule, quarter turns, columnar) joined to plaintext or ciphertext autokey, both orders, solved exactly",
        "route_specs": n_specs, "distinct_routes": len(routes), "routes_done": stopped if stopped is not None else len(routes),
        "lags": [1, N - 1], "conventions": "one alphabet throughout (standard or KRYPTOS) x Vigenere, Beaufort, variant = 6",
        "planted_check": planted_ok, "by_kind_and_order": summary, "levels_outside_control_range": outside,
        "k4_settings_with_4_plus_checks": hits[:40], "n_k4_4_plus": len(hits),
        "controls": f"{N_CONTROLS} shuffled coppers (seed 81), identical search",
    }
    line = "; ".join(f"{k}: K4 >=1..6 {[v['k4_at_least_c'][c] for c in range(1, 7)]}, controls max "
                     f"{[max(v['controls_at_least_c'][c]) for c in range(1, 7)]}" for k, v in summary.items())
    notes = (f"{len(routes):,} distinct routes x 96 lags x 6 conventions x 2 kinds x 2 orders. {line}. Outside the control "
             f"range: {outside or 'none'}. K4 settings with 4+ checks: {len(hits)}. Planted texts found: {planted_ok}."
             + (f" Stopped at route {stopped} for time." if stopped is not None else ""))
    return {"candidates": [], "bounds": bounds, "notes": notes}


def ptak_encrypt(z, primer, L, an, mode):
    A = ALPH[an]; I = {c: i for i, c in enumerate(A)}
    out = []
    for j, ch in enumerate(z):
        k = I[primer[j]] if j < L else I[z[j - L]]
        p = I[ch]
        out.append(A[{"vig": (p + k) % 26, "beau": (k - p) % 26, "var": (p - k) % 26}[mode]])
    return "".join(out)


def plant_check(known):
    """Plant a random text with the cribs, encrypt both ways, and confirm the chain test passes for the true setting."""
    rng = random.Random(7)
    pt = [rng.choice(STD) for _ in range(N)]
    for p, c in known.items():
        pt[p - 1] = c
    pt = "".join(pt)
    spec = {"kind": "turn2", "w1": 7, "w2": 13, "dir": "fwd"}
    L, an, mode = 9, "kry", "vig"
    sig, tau = MODES[mode]
    I = {c: i for i, c in enumerate(ALPH[an])}
    w = where_of(spec)
    res = []
    for order in "AB":
        if order == "A":
            ctxt = ptak_encrypt(move(spec, pt), "KRYPTOSAB", L, an, mode)
            pos = {w[p - 1]: known[p] for p in known}; W = [I[c] for c in ctxt]
        else:
            ctxt = move(spec, ptak_encrypt(pt, "KRYPTOSAB", L, an, mode))
            pos = {p - 1: known[p] for p in known}; W = [I[ctxt[w[i]]] for i in range(N)]
        last, ok = {}, True
        for j in sorted(pos):
            r = j % L
            if r in last:
                z, q = I[pos[last[r]]], last[r] + L
                while q <= j:
                    z = (sig * z + tau * W[q]) % 26; q += L
                ok &= z == I[pos[j]]
            last[r] = j
        res.append(ok)
    return all(res)


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    spec = {"kind": "turn", "w": 7, "turn": "cw", "dir": "fwd"}
    w = where_of(spec)
    I = {c: i for i, c in enumerate(KRY)}
    L = 14
    lines = [f"order A: one quarter turn clockwise at width 7, then plaintext autokey at lag {L}, sculpture's alphabet, Vigenere",
             "", "known place  letter  lands at  class mod 14"]
    land = sorted((w[p - 1], p) for p in known)
    for j, p in land[:8]:
        lines.append(f"{p:>11}  {known[p]:>6}  {j + 1:>8}  {j % L:>12}")
    # first pair in a common class
    by = {}
    for j, p in land:
        by.setdefault(j % L, []).append((j, p))
    r, lst = next((r, v) for r, v in sorted(by.items()) if len(v) >= 2)
    (j1, p1), (j2, p2) = lst[0], lst[1]
    z = I[known[p1]]
    lines.append("")
    lines.append(f"pair in class {r}: place {p1} ({known[p1]}) lands at {j1 + 1}, place {p2} ({known[p2]}) at {j2 + 1}")
    q = j1 + L
    while q <= j2:
        nz = (I[ct[q]] - z) % 26
        lines.append(f"  letter at {q + 1} = copper {ct[q]} ({I[ct[q]]}) minus previous ({z}) = {nz} = {KRY[nz]}")
        z = nz; q += L
    lines.append(f"  chain gives {KRY[z]}, known letter {known[p2]}: {'agrees' if KRY[z] == known[p2] else 'disagrees, dead'}")
    return "\n".join(lines)
