"""Experiment 0063. See program.md for the contract."""

EXPERIMENT = {
    "slug": "transposition-and-ciphertext-autokey",
    "title": "A column shuffle combined with the scrambled text as its own key, in either order",
    "family": "6-transposition-then-tableau",
    "parent": "0062-which-constructions-make-the-width-fingerprints",
    "changed": "Experiment 62 found that a cipher keyed by its own scrambled output, 21 letters back, is the only recipe tried that makes the width-21 repeats. On its own that cipher is ruled out by the known letters (experiment 2). Here it is combined with a column shuffle, before or after, which changes where the known letters fall, and tested exactly.",
    "hypothesis_expert": (
        "Ciphertext autokey (key = ciphertext letter L back, read in the key alphabet) at every lag 1-96 under "
        "the 24 conventions, composed with a transposition. Order A: transposition of the plaintext first, "
        "then autokey; the autokey decryption of K4 is then the transposed plaintext, computable without "
        "any key except the L-letter primer, so each crib must reappear at its route image (images inside "
        "the primer are free). Order B: autokey first, then transposition; undoing the route and then the "
        "autokey gives the plaintext directly, so the cribs are checked in place. Routes: 0007's set (plain "
        "columnar widths 2-96 both reading directions and both senses, keyed columnar from each vocabulary "
        "word, double plain columnar 2-50) plus keyed columnar from K1-K3 and C13/C14 words. Bounds: exact "
        "for these routes, lags and conventions; motivated by the width-21 repeats (0056, 0062)."
    ),
    "hypothesis_eli5": (
        "In a ciphertext autokey, each letter of the message is hidden using the hidden letter that came "
        "some fixed distance earlier, so the cipher feeds on its own output. Experiment 62 showed that this "
        "recipe, at a distance of 21, leaves the same 21-letter mark the copper has. On its own it cannot "
        "produce the copper's known letters, but a shuffle of columns before or after it would move them. "
        "Here we try every shuffle in our list, every distance and every way of using the table, and check "
        "whether the 24 known letters come out where they should."
    ),
    "prediction": (
        "No route, lag and convention reproduces all 24 cribs in either order; the best matches stay at a "
        "few cribs. Zero candidates."
    ),
    "method": (
        "1. For each lag and convention, undo the autokey on K4 (order A) and record the text. 2. For each "
        "route, check that every crib whose image lies past the primer matches. 3. For order B, undo each "
        "route on K4 first, then the autokey, and check the cribs in place. 4. Keep the best counts. 5. "
        "Decrypt and submit any full match."
    ),
    "walkthrough": (
        "1. Pick lag 21 and the sculpture's alphabet with Vigenere. 2. Undo the autokey on the copper: the "
        "letter at place 22 is the carved letter at 22 minus the carved letter at place 1 on the table, F "
        "minus O. 3. That gives one letter of the shuffled message. 4. If the shuffle were rows of 7 read "
        "down the columns, the known E at place 22 would have been moved to place 4, inside the first 21 "
        "letters where the autokey's starter is unknown, so it says nothing. 5. Check every other known "
        "letter at its new place past 21. 6. One mismatch kills this shuffle, lag and table."
    ),
}

from kryptos.alphabets import conventions, numeric_order, ALPHABETS, INV, MODES as AMODES
from kryptos.ciphers import columnar_transposition_encrypt, columnar_transposition_decrypt
from kryptos.facts import load_k1, load_k2, load_k3

N = 97
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


def letters(s):
    return "".join(c for c in s if "A" <= c <= "Z")


def plain_order(w, rtl=False):
    order = list(range(w))
    return order[::-1] if rtl else order


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



def autokey_decrypt(c, L, conv, primer=None):
    pa, ca, ka, m = conv
    A, C, K = ALPHABETS[pa], ALPHABETS[ca], ALPHABETS[ka]
    out = []
    for i, ch in enumerate(c):
        if i < L:
            out.append("?" if primer is None else primer[i]); continue
        out.append(A[INV[m](C.index(ch), K.index(c[i - L]))])
    return "".join(out)


def encrypt(plaintext, key):
    pa, ca, ka, m = key["conv"]; L = key["lag"]
    A, C, K = ALPHABETS[pa], ALPHABETS[ca], ALPHABETS[ka]
    if key["order"] == "A":
        inter = apply_route(key["route"], plaintext)
        out = []
        for i, p in enumerate(inter):
            k = key["primer"][i] if i < L else out[i - L]
            out.append(C[AMODES[m](A.index(p), K.index(k))])
        return "".join(out)
    out = []
    for i, p in enumerate(plaintext):
        k = key["primer"][i] if i < L else out[i - L]
        out.append(C[AMODES[m](A.index(p), K.index(k))])
    return apply_route(key["route"], "".join(out))


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    vocab = sorted(set(ctx.vocabulary) | {w for w in SPACED.split() if 3 <= len(w) <= 40} | set(EXTRA))
    routes = route_set(vocab)
    crib = sorted(known.items())
    convs = list(conventions())
    full, best = [], (0, None)
    checked = 0
    # order A
    X = {(L, conv): autokey_decrypt(ct, L, conv) for L in range(1, 96) for conv in convs}
    for name, spec, fn in routes:
        sigma = perm_of(fn)
        where = {sigma[j]: j for j in range(N)}
        img = [(where[q - 1], p) for q, p in crib]
        for (L, conv), x in X.items():
            checked += 1
            hits, ok = 0, True
            for j, p in img:
                if j < L:
                    continue
                if x[j] == p:
                    hits += 1
                else:
                    ok = False
            if hits > best[0]:
                best = (hits, ("A", name, L, "/".join(conv)))
            if ok and hits >= 12:
                full.append(("A", name, L, conv, spec))
        if ctx.time_left() < 600:
            break
    # order B
    bestB = (0, None)
    for name, spec, fn in routes:
        y = apply_route(spec, ct, inverse=True)
        for L in range(1, 96):
            for conv in convs:
                checked += 1
                x = autokey_decrypt(y, L, conv)
                hits = sum(1 for q, p in crib if x[q - 1] == p)
                if hits > bestB[0]:
                    bestB = (hits, ("B", name, L, "/".join(conv)))
                if hits == 24:
                    full.append(("B", name, L, conv, spec))
        if ctx.time_left() < 120:
            break
    return {
        "candidates": [],
        "bounds": {"family": "transposition composed with ciphertext autokey, either order", "routes": len(routes), "lags": "1-95",
                   "conventions": 24, "checked": checked, "full_matches": len(full),
                   "best_order_A": {"hits_past_primer": best[0], "setting": best[1]},
                   "best_order_B": {"hits": bestB[0], "setting": bestB[1]}},
        "notes": f"{len(routes)} routes x 95 lags x 24 conventions x 2 orders ({checked:,} checks): {len(full)} full matches. Best order A: {best[0]} cribs past the primer ({best[1]}); best order B: {bestB[0]}/24 ({bestB[1]}).",
    }


def worked_example(ctx, key):
    conv = ("kry", "kry", "kry", "vig")
    x = autokey_decrypt(ctx.K4, 21, conv)
    return f"lag 21, kry/kry/kry/vig, autokey undone on the copper (first 21 unknown):\n{x}"
