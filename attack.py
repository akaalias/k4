"""Experiment 0006. See program.md for the contract."""

EXPERIMENT = {
    "slug": "columnar-then-tableau-period-survival",
    "title": "A matrix transposition first, the keyed tableau last: which routes let the 24 cribs force a short periodic key",
    "family": "6-transposition-then-tableau",
    "parent": None,
    "changed": "New root. Family 6 opens after five reverts in family 1. A columnar transposition stage runs before the periodic tableau, so the cribs constrain the key through the route.",
    "hypothesis_expert": (
        "Sanborn, CNN 2005 (knowledge/sources, clue C1 reading a): matrix code first, double and triple "
        "matrixes sometimes, 'then went back to this table to do the ultimate'. Family A in "
        "knowledge/06-hypotheses.md: K4 = tableau(T(P)) where T is a columnar transposition and the "
        "tableau stage is periodic with separate alphabets. The cribs sit in P at 22-34 and 64-74. "
        "Under T they land at intermediate positions j = T(pos); the ciphertext at j then forces the "
        "key letter at slot j mod period under each of the 24 conventions. For each route T we find "
        "the smallest period whose forced letters never conflict, by the divisor rule: period p is "
        "dead if p divides the distance between two intermediate positions that force different key "
        "letters. Routes searched: plain columnar at every width 2 to 96, read columns left to right or "
        "right to left, applied forward or inverse; keyed columnar from every vocabulary word, forward "
        "or inverse; and every double of two plain forward columnars at widths 2 to 50 (C1 'double "
        "matrixes', C2 'all the possible shifts'). Survivors with a short period get their forced "
        "fragment matched against the vocabulary and K1-K3 windows; matches are decrypted and submitted. "
        "Bounds: complete for the route set above under 24 conventions and periods 1-97."
    ),
    "hypothesis_eli5": (
        "The artist said he first scrambled the order of the letters by writing them in a grid and "
        "reading it another way, and only then used the big table on the sculpture. If that is true, "
        "the 24 letters we know are no longer where we think: the grid moved them. For each way of "
        "making a grid, we work out where the known letters would have gone, and ask whether a short "
        "secret word could then turn them into the carved letters at those spots. Most grids make "
        "the known letters contradict each other, which rules them out. A grid that lets a short "
        "secret word do the job would be a real find, and we then check whether any word from the "
        "puzzle's own world fits."
    ),
    "prediction": (
        "A dry run on 40 routes calibrated this. The smallest live period will cluster between 24 "
        "and 50 for almost every route and convention. Any route with a live period of 15 or less "
        "is rarer than one in a thousand and gets a follow-up. No forced fragment matches a "
        "vocabulary word or K1-K3 window, so zero candidates pass."
    ),
    "method": (
        "1. Build the route set: plain columnar widths 2-96 in two column directions, forward and "
        "inverse; keyed columnar from each vocabulary word, forward and inverse; doubles of plain "
        "forward columnars at widths 2-50. 2. For each route, map each crib position to its "
        "intermediate position. 3. For each convention, force the key letter at each intermediate "
        "position from the crib plaintext and the ciphertext there. 4. Mark period p dead if it divides "
        "a distance between two positions with different forced letters; the smallest live period is "
        "the route's score. 5. For live periods up to 30, match the forced fragment against the "
        "vocabulary and the K1-K3 windows; decrypt matches and submit."
    ),
    "walkthrough": (
        "1. Pick a route: write the text in rows of 7 and read down the columns, left column first. "
        "2. Position 22, the E of EAST, is row 4 column 1 (counting from 1). Column 1 holds rows 1 to 14, "
        "so E lands at intermediate position 4. 3. Position 64, the B of BERLIN, is row 10 column 1, so "
        "it lands at position 10. 4. The ciphertext at 4 is R and at 10 is H. Under the sculpture's "
        "alphabet with Vigenere, the key letter that sends E to R and the one that sends B to H are "
        "forced. 5. Do this for all 24 known letters; you get 24 forced key letters at 24 positions. "
        "6. A period of 6 would make positions 4 and 10 share a key letter; if their forced letters "
        "differ, period 6 is dead, and so is any period dividing 6. 7. Cross out every dead period; "
        "the smallest survivor is the shortest secret word this route allows. 8. Write the survivors' "
        "forced letters into a pattern with blanks and slide the puzzle's words across it."
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


def route_set(vocab):
    routes = []
    for w in range(2, N):
        for rtl in (False, True):
            order = plain_order(w, rtl)
            name = f"columnar w={w}{' rtl' if rtl else ''}"
            routes.append((name + " fwd", {"kind": "plain", "w": w, "rtl": rtl, "dir": "fwd"},
                           lambda s, o=order: columnar_transposition_encrypt(s, o)))
            routes.append((name + " inv", {"kind": "plain", "w": w, "rtl": rtl, "dir": "inv"},
                           lambda s, o=order: columnar_transposition_decrypt(s, o)))
    for word in vocab:
        if 2 <= len(word) <= 40:
            order = numeric_order(word)
            routes.append((f"keyed columnar {word} fwd", {"kind": "keyed", "word": word, "dir": "fwd"},
                           lambda s, o=order: columnar_transposition_encrypt(s, o)))
            routes.append((f"keyed columnar {word} inv", {"kind": "keyed", "word": word, "dir": "inv"},
                           lambda s, o=order: columnar_transposition_decrypt(s, o)))
    for w1 in range(2, 51):
        for w2 in range(2, 51):
            o1, o2 = plain_order(w1), plain_order(w2)
            routes.append((f"double columnar w={w1} then w={w2}", {"kind": "double", "w1": w1, "w2": w2, "dir": "fwd"},
                           lambda s, a=o1, b=o2: columnar_transposition_encrypt(columnar_transposition_encrypt(s, a), b)))
    return routes


def apply_route(spec, s, inverse=False):
    if spec["kind"] == "plain":
        order = plain_order(spec["w"], spec["rtl"])
        fwd = spec["dir"] == "fwd"
    elif spec["kind"] == "keyed":
        order = numeric_order(spec["word"])
        fwd = spec["dir"] == "fwd"
    else:
        o1, o2 = plain_order(spec["w1"]), plain_order(spec["w2"])
        if inverse:
            return columnar_transposition_decrypt(columnar_transposition_decrypt(s, o2), o1)
        return columnar_transposition_encrypt(columnar_transposition_encrypt(s, o1), o2)
    if fwd != inverse:
        return columnar_transposition_encrypt(s, order)
    return columnar_transposition_decrypt(s, order)


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
    assert apply_route({"kind": "plain", "w": 7, "rtl": False, "dir": "fwd"}, apply_route({"kind": "plain", "w": 7, "rtl": False, "dir": "fwd"}, ct, inverse=True)) == ct

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
        "bounds": {"family": "columnar transposition then periodic tableau (separate alphabets)",
                   "routes": len(routes), "route_convention_pairs_checked": n_checked,
                   "route_set": "plain columnar w=2..96 x {ltr, rtl} x {fwd, inv}; keyed columnar from each vocabulary word x {fwd, inv}; double plain columnar w1,w2 in 2..50",
                   "conventions": 24, "periods": "1-97 by divisor rule",
                   "key_pool": f"vocabulary words and K1-K3 windows of length P for live P <= {MAX_KEY_PERIOD}",
                   "min_live_period_histogram": {str(k): v for k, v in sorted(hist.items())},
                   "fifteen_shortest": top, "vocab_matches": len(matches)},
        "notes": f"{n_checked} route/convention pairs; {len(matches)} forced-fragment matches submitted.",
    }


def worked_example(ctx, key):
    lines = ["route: columnar width 7, read columns left to right; convention kry/kry/kry Vigenere", ""]
    spec = {"kind": "plain", "w": 7, "rtl": False, "dir": "fwd"}
    sigma = perm_of(lambda s: apply_route(spec, s))
    where = {sigma[j]: j for j in range(N)}
    lines.append("plain pos  letter  lands at  cipher there  forced key letter")
    for pos in (22, 23, 24, 25, 64, 65, 66, 67):
        j = where[pos - 1]
        p, c = ctx.KNOWN[pos], ctx.K4[j]
        lines.append(f"{pos:>9}    {p}       {j+1:>3}         {c}              {key_letter_for(p, c, 'kry', 'kry', 'kry', 'vig')}")
    lines.append("")
    lines.append("positions 4 and 10 share a key slot at period 6, 3, 2 and 1; if their forced letters differ, those periods die.")
    return "\n".join(lines)
