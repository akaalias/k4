"""Experiment 0006. See program.md for the contract."""

EXPERIMENT = {
    "slug": "tableau-then-columnar-period-survival",
    "title": "The keyed tableau first, a matrix transposition last: the order the NSA guessed in 1992",
    "family": "6-transposition-then-tableau",
    "parent": "0006-columnar-then-tableau-period-survival",
    "changed": "Stage order reversed. The tableau runs on the plaintext in place, then the columnar route scrambles the result. Same 2,905 routes, same 24 conventions.",
    "hypothesis_expert": (
        "The NSA's 1992 write-up (knowledge/sources, clue C11a) guessed substitution then transposition for "
        "K4, the opposite of Sanborn's CNN 2005 order (C1). Under K4 = T(tableau(P)) the key slot of each "
        "crib letter is its own plaintext position mod the period, and the ciphertext letter that pairs "
        "with it sits where the route T sent that position. The 24 cribs occupy 13 consecutive slots at "
        "22-34 and 11 at 64-74, so at any period of 13 or less at least 11 forced letters must agree with "
        "an earlier one: chance survival is below one in 26 to the 11th power per route. For each route "
        "and convention we find the smallest live period by the divisor rule on plaintext positions; "
        "a survivor under 23 would be a strong signal, and the forced fragment is matched against the "
        "vocabulary and K1-K3 windows. Bounds: complete for the 0006 route set in this order."
    ),
    "hypothesis_eli5": (
        "Last time we assumed the artist scrambled the letters first and used the table second. The "
        "code-breakers at the NSA guessed the other way round: table first, scramble second. That "
        "changes which carved letter belongs to which known letter. For every grid we try, we match "
        "each of the 24 known letters with the carved letter the grid would have sent it to, and ask "
        "whether one short secret word explains all 24 pairs. Because the known letters sit in two "
        "unbroken runs, a short word has to pass a very strict test here, so a survivor would mean a lot."
    ),
    "prediction": (
        "No route and convention admits a period under 23. The smallest live periods cluster from the "
        "high 20s upward, with the floor set by the 13-letter run at 22-34. No forced fragment matches "
        "a vocabulary word or K1-K3 window; zero candidates pass."
    ),
    "method": (
        "1. Build the 0006 route set. 2. For each route, find where each crib position is sent. "
        "3. For each convention, force the key letter from the crib plaintext and the ciphertext at "
        "that destination. 4. Key slots are the crib's own position mod the period: mark period p dead "
        "if it divides the distance between two crib positions with different forced letters. "
        "5. For live periods up to 30, match the forced fragment against the vocabulary and K1-K3 "
        "windows; decrypt matches and submit."
    ),
    "walkthrough": (
        "1. Pick a route: write in rows of 7, read down the columns. 2. Position 22, the E of EAST, is row 4 "
        "column 1, so it is read out fourth: its enciphered letter is the carved R at position 4. "
        "3. Position 23, the A, is row 4 column 2; column 2 holds 14 letters after column 1's 14, so A "
        "sits at 18, the carved F. 4. Under the sculpture's alphabet and Vigenere, the key letter sending "
        "E to R is forced, and so is the one sending A to F. 5. These two key letters sit at slots 22 and "
        "23 of the key, so any period dividing 1 would need them equal: only period 1 is at stake here. "
        "6. Do this for all 24 letters. The E at 22 and the E at 65 differ by 43, so if their forced "
        "letters differ, period 43 and period 1 die. 7. Cross out every dead period; the smallest survivor "
        "is the shortest key this route allows. 8. Slide the puzzle's words across the survivors' pattern."
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
    pa, ca, ka, m, k = key["pa"], key["ca"], key["ka"], key["m"], key["key"]
    inter = "".join(encrypt_letter(p, k[i % len(k)], pa, ca, ka, m) for i, p in enumerate(plaintext))
    return apply_route(key["route"], inter)


def decrypt(ciphertext, key):
    pa, ca, ka, m, k = key["pa"], key["ca"], key["ka"], key["m"], key["key"]
    inter = apply_route(key["route"], ciphertext, inverse=True)
    return "".join(decrypt_letter(c, k[i % len(k)], pa, ca, ka, m) for i, c in enumerate(inter))


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
                        d = abs(crib_pos[a] - crib_pos[b])
                        dead.update(DIVISORS[d])
            live = [p for p in range(1, N + 1) if p not in dead]
            mp = live[0]
            n_checked += 1
            hist[mp] = hist.get(mp, 0) + 1
            best.append((mp, name, conv))
            for P in [p for p in live if p <= MAX_KEY_PERIOD]:
                slots = {(p - 1) % P: l for p, l in zip(crib_pos, forced)}
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
        "bounds": {"family": "periodic tableau (separate alphabets) then columnar transposition",
                   "routes": len(routes), "route_convention_pairs_checked": n_checked,
                   "route_set": "plain columnar w=2..96 x {ltr, rtl} x {fwd, inv}; keyed columnar from each vocabulary word x {fwd, inv}; double plain columnar w1,w2 in 2..50",
                   "conventions": 24, "periods": "1-97 by divisor rule on plaintext positions",
                   "key_pool": f"vocabulary words and K1-K3 windows of length P for live P <= {MAX_KEY_PERIOD}",
                   "min_live_period_histogram": {str(k): v for k, v in sorted(hist.items())},
                   "fifteen_shortest": top, "vocab_matches": len(matches)},
        "notes": f"{n_checked} route/convention pairs; {len(matches)} forced-fragment matches submitted.",
    }


def worked_example(ctx, key):
    lines = ["route: columnar width 7, read columns left to right, applied after the tableau; convention kry/kry/kry Vigenere", ""]
    spec = {"kind": "plain", "w": 7, "rtl": False, "dir": "fwd"}
    sigma = perm_of(lambda s: apply_route(spec, s))
    where = {sigma[j]: j for j in range(N)}
    lines.append("plain pos  letter  its cipher sits at  cipher letter  forced key letter  key slot at period 13")
    for pos in (22, 23, 24, 25, 64, 65, 66, 67):
        j = where[pos - 1]
        p, c = ctx.KNOWN[pos], ctx.K4[j]
        lines.append(f"{pos:>9}    {p}          {j+1:>3}              {c}              {key_letter_for(p, c, 'kry', 'kry', 'kry', 'vig')}                 {(pos-1)%13:>2}")
    lines.append("")
    lines.append("slots repeat at period 13: position 22 and 35 would share one, 64 and 77 another; the 24 cribs fill 13 slots with 11 collisions.")
    return "\n".join(lines)
