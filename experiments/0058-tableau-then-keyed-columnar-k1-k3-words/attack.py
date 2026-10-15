"""Experiment 0058. See program.md for the contract."""

EXPERIMENT = {
    "slug": "tableau-then-keyed-columnar-k1-k3-words",
    "title": "The table first, then a column shuffle keyed by a word from the solved messages, once or twice",
    "family": "6-transposition-then-tableau",
    "parent": "0007-tableau-then-columnar-period-survival",
    "changed": "Experiment 7 put the column shuffle after the table and keyed it with the puzzle's vocabulary, single, and with plain widths for the double shuffle. Here the shuffle is keyed by every word of the three solved messages and of Sanborn's 2025 letter, singly and as keyed double shuffles with two such words.",
    "hypothesis_expert": (
        "Periodic tableau (separate alphabets, 24 conventions) followed by keyed columnar transposition, "
        "single or double (C1, Sanborn 2005: 'double matrixes and triple matrixes... then went back to this "
        "table'; here the table first, 0007's order). Column orders from the numeric order of every K1-K3 "
        "plaintext word of length 3-20 and of the C13/C14 words, forward and inverse, and every ordered pair "
        "of distinct such words as a keyed double columnar, forward and inverse. For each route the inverse "
        "transposition maps each crib to a carved letter; each convention forces 24 key letters; a period is "
        "dead when two cribs it puts in one slot force different letters (divisor rule on plaintext "
        "distances). Live periods up to 30 are matched against the vocabulary and K1-K3 windows. Bounds: "
        "complete for these routes, conventions and periods."
    ),
    "hypothesis_eli5": (
        "One recipe Sanborn hinted at uses the table and a shuffle of the letters by columns, the order of "
        "the columns set by a word. Experiment 7 tried the puzzle's own words for that order. Here the "
        "order comes from every word of the solved messages and Sanborn's 2025 letter, and the shuffle is "
        "done once or twice in a row. For each shuffle we check whether a repeating secret word on the "
        "table could still put the 24 known letters where they are."
    ),
    "prediction": (
        "No route makes a period below 26 live; the smallest live period is 26 or 27 everywhere, and no "
        "forced fragment matches a word. Zero candidates."
    ),
    "method": (
        "1. Build the column orders from the word pool. 2. For each route, find where each known letter "
        "lands. 3. For each convention, force the 24 key letters and kill periods by the divisor rule. 4. "
        "Record the smallest live period. 5. Match live periods up to 30 against words and K1-K3 windows; "
        "decrypt and submit matches."
    ),
    "walkthrough": (
        "1. Take the K2 word MAGNETIC: its letters in alphabetical order number the columns A=1, C=2, E=3, "
        "G=4, I=5, M=6, N=7, T=8, so the column order is 6, 1, 4, 7, 3, 8, 5, 2. 2. Write the 97 places in "
        "rows of 8 and read the columns in that order: column 2 (places 2, 10, 18, ...) comes first. 3. "
        "Each known letter is carried to a new place by this reading. 4. Under one way of using the table "
        "each known letter and the carved letter at its new place force one key letter. 5. Two known "
        "letters a secret word's length apart must force the same key letter; one clash kills that length."
    ),
}

from kryptos.alphabets import conventions, key_letter_for, decrypt_letter, encrypt_letter, numeric_order
from kryptos.ciphers import columnar_transposition_encrypt, columnar_transposition_decrypt
from kryptos.facts import load_k1, load_k2, load_k3

SPACED = (
    "BETWEEN SUBTLE SHADING AND THE ABSENCE OF LIGHT LIES THE NUANCE OF IQLUSION "
    "IT WAS TOTALLY INVISIBLE HOWS THAT POSSIBLE THEY USED THE EARTHS MAGNETIC FIELD X THE INFORMATION WAS GATHERED AND "
    "TRANSMITTED UNDERGRUUND TO AN UNKNOWN LOCATION X DOES LANGLEY KNOW ABOUT THIS THEY SHOULD ITS BURIED OUT THERE "
    "SOMEWHERE X WHO KNOWS THE EXACT LOCATION ONLY WW THIS WAS HIS LAST MESSAGE X THIRTY EIGHT DEGREES FIFTY SEVEN "
    "MINUTES SIX POINT FIVE SECONDS NORTH SEVENTY SEVEN DEGREES EIGHT MINUTES FORTY FOUR SECONDS WEST ID BY ROWS "
    "SLOWLY DESPARATLY SLOWLY THE REMAINS OF PASSAGE DEBRIS THAT ENCUMBERED THE LOWER PART OF THE DOORWAY WAS REMOVED "
    "WITH TREMBLING HANDS I MADE A TINY BREACH IN THE UPPER LEFT HAND CORNER AND THEN WIDENING THE HOLE A LITTLE I "
    "INSERTED THE CANDLE AND PEERED IN THE HOT AIR ESCAPING FROM THE CHAMBER CAUSED THE FLAME TO FLICKER BUT PRESENTLY "
    "DETAILS OF THE ROOM WITHIN EMERGED FROM THE MIST X CAN YOU SEE ANYTHING Q"
)
EXTRA = ["EGYPT", "CAIRO", "LUXOR", "WALL", "NOVEMBER", "MESSAGE", "DELIVER", "DELIVERING", "TRANSMIT"]


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
    words = sorted({w for w in SPACED.split() if 3 <= len(w) <= 20} | set(EXTRA))
    orders, seen = [], set()
    for w in words:
        o = tuple(numeric_order(w))
        if o not in seen:
            seen.add(o); orders.append((w, list(o)))
    routes = []
    for w, o in orders:
        routes.append((f"keyed columnar {w} fwd", {"kind": "keyed", "word": w, "dir": "fwd"}, lambda s, o=o: columnar_transposition_encrypt(s, o)))
        routes.append((f"keyed columnar {w} inv", {"kind": "keyed", "word": w, "dir": "inv"}, lambda s, o=o: columnar_transposition_decrypt(s, o)))
    for w1, o1 in orders:
        for w2, o2 in orders:
            if w1 == w2:
                continue
            routes.append((f"keyed double {w1} then {w2} fwd", {"kind": "kdouble", "w1": w1, "w2": w2, "dir": "fwd"},
                           lambda s, a=o1, b=o2: columnar_transposition_encrypt(columnar_transposition_encrypt(s, a), b)))
            routes.append((f"keyed double {w1} then {w2} inv", {"kind": "kdouble", "w1": w1, "w2": w2, "dir": "inv"},
                           lambda s, a=o1, b=o2: columnar_transposition_decrypt(columnar_transposition_decrypt(s, b), a)))
    return routes


def apply_route(spec, s, inverse=False):
    if spec["kind"] == "keyed":
        order = numeric_order(spec["word"])
        fwd = spec["dir"] == "fwd"
        return columnar_transposition_encrypt(s, order) if fwd != inverse else columnar_transposition_decrypt(s, order)
    o1, o2 = numeric_order(spec["w1"]), numeric_order(spec["w2"])
    enc = lambda t: columnar_transposition_encrypt(columnar_transposition_encrypt(t, o1), o2)
    dec = lambda t: columnar_transposition_decrypt(columnar_transposition_decrypt(t, o2), o1)
    fwd = spec["dir"] == "fwd"
    return enc(s) if fwd != inverse else dec(s)


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
    assert apply_route({"kind": "kdouble", "w1": "MAGNETIC", "w2": "BURIED", "dir": "fwd"}, apply_route({"kind": "kdouble", "w1": "MAGNETIC", "w2": "BURIED", "dir": "fwd"}, ct, inverse=True)) == ct

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
        "bounds": {"family": "periodic tableau (separate alphabets) then keyed columnar transposition, single or double, keys from K1-K3 and C13/C14 words",
                   "routes": len(routes), "route_convention_pairs_checked": n_checked,
                   "route_set": "keyed columnar from K1-K3 words (3-20 letters) and C13/C14 words x {fwd, inv}; keyed double columnar over ordered pairs of distinct such orders x {fwd, inv}",
                   "conventions": 24, "periods": "1-97 by divisor rule on plaintext positions",
                   "key_pool": f"vocabulary words and K1-K3 windows of length P for live P <= {MAX_KEY_PERIOD}",
                   "min_live_period_histogram": {str(k): v for k, v in sorted(hist.items())},
                   "fifteen_shortest": top, "vocab_matches": len(matches)},
        "notes": f"{n_checked} route/convention pairs; {len(matches)} forced-fragment matches submitted.",
    }


def worked_example(ctx, key):
    lines = ["route: keyed columnar MAGNETIC, applied after the tableau; convention kry/kry/kry Vigenere", ""]
    spec = {"kind": "keyed", "word": "MAGNETIC", "dir": "fwd"}
    sigma = perm_of(lambda s: apply_route(spec, s))
    where = {sigma[j]: j for j in range(N)}
    lines.append("plain pos  letter  its cipher sits at  cipher letter  forced key letter  key slot at period 13")
    for pos in (22, 23, 24, 25, 64, 65, 66, 67):
        j = where[pos - 1]
        p, c = ctx.KNOWN[pos], ctx.K4[j]
        lines.append(f"{pos:>9}    {p}          {j+1:>3}              {c}              {key_letter_for(p, c, 'kry', 'kry', 'kry', 'vig')}                 {(pos-1)%13:>2}")
    lines.append("")
    return "\n".join(lines)
