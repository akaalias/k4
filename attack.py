"""Experiment 0006. See program.md for the contract."""

EXPERIMENT = {
    "slug": "k3-formula-all-shifts-then-tableau",
    "title": "K3's own matrix run through all the possible shifts, then the tableau",
    "family": "6-transposition-then-tableau",
    "parent": "0006-columnar-then-tableau-period-survival",
    "changed": "Route set replaced. Instead of columnar grids, the routes are K3's transposition rule with every shift, plus K3-style double rotations of a grid. Survival test unchanged.",
    "hypothesis_expert": (
        "Sanborn, 2003, secondhand (clue C2): surprised no one had tried 'recovering the original matrix and "
        "running it through all the possible shifts'. K3's matrix is known: Stehle's rule reads plaintext[i] "
        "= ciphertext[(191 + 192 i) mod 337] (data/k3.json), and the NSA described it as a double rotation "
        "of a grid. Reading (a): K4 is the same matrix with a different shift. For n = 97, prime, every "
        "pair (a, b) with b in 1..96 is a valid rule, 9,312 routes, each applied forward and inverse; add "
        "the double rotations, write in rows of w1 and read columns bottom-up, then again with w2, for "
        "w1, w2 in 2..50. Each route goes before a periodic tableau with separate alphabets, as in 0006, "
        "and the cribs force key letters at their new positions; the divisor rule gives the smallest "
        "live period. Live periods up to 30 are matched against the vocabulary and K1-K3 windows. "
        "Bounds: complete for this route set, 24 conventions, periods 1-97."
    ),
    "hypothesis_eli5": (
        "The third message was scrambled by a fixed rule: take every 192nd letter, wrapping around. The "
        "artist once said he was surprised nobody had taken that same rule and tried all its settings. "
        "So we do: every step size and every starting point for the 97 letters, and also the grid-turning "
        "trick the code-breakers described for the third message. For each setting we work out where the "
        "24 known letters would have gone and ask whether a short secret word on the sculpture's table "
        "could then produce the carved letters there. A setting that allows a short word is the signal."
    ),
    "prediction": (
        "As in 0006, the smallest live period clusters between 24 and 50. No route allows a period of 15 "
        "or less. No forced fragment matches a vocabulary word or K1-K3 window; zero candidates pass."
    ),
    "method": (
        "1. Build the routes: plaintext[i] = inter[(a + b i) mod 97] for a in 0..96, b in 1..96, forward "
        "and inverse; double rotations of a grid for widths 2-50 twice. 2. For each route, send each crib "
        "position to its intermediate position. 3. For each convention, force the key letter from the crib "
        "plaintext and the ciphertext at the destination. 4. Period p is dead if it divides a distance "
        "between two destinations with different forced letters; the smallest live p is the route's score. "
        "5. For live p up to 30, match the forced fragment against the vocabulary and K1-K3 windows; "
        "decrypt matches and submit."
    ),
    "walkthrough": (
        "1. Pick a rule: start at 5, step 7. The first plaintext letter comes from position 5, the "
        "second from 12, the third from 19, and so on, wrapping past 97. 2. Position 22 of the plaintext, "
        "the E of EAST, is the 22nd letter read, so it comes from 5 + 7 x 21 = 152, which wraps to 55. "
        "3. The ciphertext at 55 is therefore the enciphered E; under the sculpture's alphabet and Vigenere "
        "the key letter that sends E there is forced. 4. Do this for all 24 known letters to get 24 forced "
        "key letters at 24 positions. 5. Two positions whose distance is a multiple of p share a key slot "
        "at period p; if their forced letters differ, p is dead. 6. The smallest live p is the shortest "
        "secret word the rule allows. 7. Slide the puzzle's words across the survivors' pattern."
    ),
}

from kryptos.alphabets import conventions, key_letter_for, decrypt_letter, encrypt_letter, numeric_order
from kryptos.ciphers import columnar_transposition_encrypt, columnar_transposition_decrypt
from kryptos.facts import load_k1, load_k2, load_k3

N = 97
MAX_KEY_PERIOD = 30


def letters(s):
    return "".join(c for c in s if "A" <= c <= "Z")


# A route is a permutation sigma with intermediate[j] = plaintext[sigma[j]] (0-indexed).
def perm_of(fn):
    """Apply a string transform to the identity index string and read off sigma."""
    idx = [chr(0x100 + i) for i in range(N)]
    out = fn("".join(idx))
    return [ord(ch) - 0x100 for ch in out]


def plain_order(w, rtl=False):
    o = list(range(w))
    return o[::-1] if rtl else o


def affine_fwd(s, a, b):
    """K3 rule: plaintext[i] = inter[(a + b*i) mod n]. Here s is the plaintext, out is inter."""
    n = len(s)
    out = [""] * n
    for i in range(n):
        out[(a + b * i) % n] = s[i]
    return "".join(out)


def affine_inv(s, a, b):
    n = len(s)
    return "".join(s[(a + b * i) % n] for i in range(n))


def rotate(s, w):
    """Write in rows of w, read columns from the bottom up, left column first (a quarter turn)."""
    rows = [s[i:i + w] for i in range(0, len(s), w)]
    out = []
    for col in range(w):
        for r in reversed(rows):
            if col < len(r):
                out.append(r[col])
    return "".join(out)


def route_set(vocab):
    routes = []
    for b in range(1, N):
        for a in range(N):
            routes.append((f"K3 rule a={a} b={b} fwd", {"kind": "affine", "a": a, "b": b, "dir": "fwd"},
                           lambda s, a=a, b=b: affine_fwd(s, a, b)))
            routes.append((f"K3 rule a={a} b={b} inv", {"kind": "affine", "a": a, "b": b, "dir": "inv"},
                           lambda s, a=a, b=b: affine_inv(s, a, b)))
    for w1 in range(2, 51):
        for w2 in range(2, 51):
            routes.append((f"double rotation w={w1} then w={w2}", {"kind": "rot2", "w1": w1, "w2": w2, "dir": "fwd"},
                           lambda s, a=w1, b=w2: rotate(rotate(s, a), b)))
    return routes


def invert_perm_apply(fn, s):
    """Apply the inverse of a permutation-defined transform."""
    sigma = perm_of(fn)
    out = [""] * N
    for j in range(N):
        out[sigma[j]] = s[j]
    return "".join(out)


def apply_route(spec, s, inverse=False):
    if spec["kind"] == "affine":
        fwd = spec["dir"] == "fwd"
        if fwd != inverse:
            return affine_fwd(s, spec["a"], spec["b"])
        return affine_inv(s, spec["a"], spec["b"])
    fn = lambda t, a=spec["w1"], b=spec["w2"]: rotate(rotate(t, a), b)
    return invert_perm_apply(fn, s) if inverse else fn(s)


def encrypt(plaintext, key):
    inter = apply_route(key["route"], plaintext)
    pa, ca, ka, m, k = key["pa"], key["ca"], key["ka"], key["m"], key["key"]
    return "".join(encrypt_letter(p, k[i % len(k)], pa, ca, ka, m) for i, p in enumerate(inter))


def decrypt(ciphertext, key):
    pa, ca, ka, m, k = key["pa"], key["ca"], key["ka"], key["m"], key["key"]
    inter = "".join(decrypt_letter(c, k[i % len(k)], pa, ca, ka, m) for i, c in enumerate(ciphertext))
    return apply_route(key["route"], inter, inverse=True)


DIVISORS = {d: [k for k in range(1, d + 1) if d % k == 0] for d in range(1, N + 1)}


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    vocab = list(ctx.vocabulary)
    texts = [letters(load_k1()["plaintext"]), letters(load_k2()["plaintext_as_carved"]), letters(load_k3()["plaintext"])]
    convs = list(conventions())
    crib_pos = sorted(known)  # 1-indexed plaintext positions
    # self-check of the route machinery against the library primitive
    k3 = load_k3()
    assert affine_inv(k3["ciphertext"], 191, 192) == k3["plaintext"], "K3 rule check"
    assert apply_route({"kind": "rot2", "w1": 7, "w2": 9, "dir": "fwd"}, apply_route({"kind": "rot2", "w1": 7, "w2": 9, "dir": "fwd"}, ct, inverse=True)) == ct

    routes = route_set(vocab)
    hist = {}        # smallest live period -> count of (route, convention)
    best = []        # (min_period, route name, conv)
    candidates, matches = [], []
    n_checked = 0
    for name, spec, fn in routes:
        if ctx.time_left() < 20:
            break
        sigma = perm_of(fn)                      # inter[j] = plain[sigma[j]]
        where = {sigma[j]: j for j in range(N)}  # plain index -> intermediate index
        inter_pos = [where[p - 1] for p in crib_pos]
        for conv in convs:
            pa, ca, ka, m = conv
            forced = [key_letter_for(known[p], ct[j], pa, ca, ka, m) for p, j in zip(crib_pos, inter_pos)]
            dead = set()
            for a in range(24):
                for b in range(a + 1, 24):
                    if forced[a] != forced[b]:
                        d = abs(inter_pos[a] - inter_pos[b])
                        dead.update(DIVISORS[d])
            live = [p for p in range(1, N + 1) if p not in dead]
            mp = live[0]
            n_checked += 1
            hist[mp] = hist.get(mp, 0) + 1
            best.append((mp, name, conv))
            for P in [p for p in live if p <= MAX_KEY_PERIOD]:
                slots = {j % P: l for j, l in zip(inter_pos, forced)}
                pool = set(w for w in vocab if len(w) == P)
                for t in texts:
                    for i in range(0, len(t) - P + 1):
                        pool.add(t[i:i + P])
                for kw in pool:
                    if all(kw[s] == l for s, l in slots.items()):
                        key = {"route": spec, "pa": pa, "ca": ca, "ka": ka, "m": m, "key": kw}
                        pt = decrypt(ct, key)
                        matches.append((name, conv, P, kw))
                        candidates.append({"plaintext": pt, "key": key, "key_bits": 4.7 * P + 6,
                                           "key_description": f"{name}; period {P} key {kw}; {pa}/{ca}/{ka} {m}"})
    best.sort(key=lambda t: t[0])
    top = [{"min_period": mp, "route": nm, "convention": "/".join(c)} for mp, nm, c in best[:15]]
    return {
        "candidates": candidates[:50],
        "bounds": {"family": "K3 affine rule with all shifts, or double rotation, then periodic tableau (separate alphabets)",
                   "routes": len(routes), "route_convention_pairs_checked": n_checked,
                   "route_set": "plaintext[i] = inter[(a + b i) mod 97], a in 0..96, b in 1..96, fwd and inv; double rotation w1, w2 in 2..50",
                   "conventions": 24, "periods": "1-97 by divisor rule",
                   "key_pool": f"vocabulary words and K1-K3 windows of length P for live P <= {MAX_KEY_PERIOD}",
                   "min_live_period_histogram": {str(k): v for k, v in sorted(hist.items())},
                   "fifteen_shortest": top, "vocab_matches": len(matches)},
        "notes": f"{n_checked} route/convention pairs; {len(matches)} forced-fragment matches submitted. K3 rule verified against data/k3.json inside run.",
    }


def worked_example(ctx, key):
    lines = ["route: K3 rule, start 5, step 7 (plaintext[i] comes from position 5 + 7 i, 0-indexed); convention kry/kry/kry Vigenere", ""]
    spec = {"kind": "affine", "a": 5, "b": 7, "dir": "inv"}
    sigma = perm_of(lambda s: apply_route(spec, s))
    where = {sigma[j]: j for j in range(N)}
    lines.append("plain pos  letter  lands at  cipher there  forced key letter")
    for pos in (22, 23, 24, 25, 64, 65, 66, 67):
        j = where[pos - 1]
        p, c = ctx.KNOWN[pos], ctx.K4[j]
        lines.append(f"{pos:>9}    {p}       {j+1:>3}         {c}              {key_letter_for(p, c, 'kry', 'kry', 'kry', 'vig')}")
    lines.append("")
    lines.append("consecutive crib letters land 7 apart, so period 7 and period 1 need their forced letters equal.")
    return "\n".join(lines)
