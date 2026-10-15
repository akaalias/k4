"""Experiment 0094. See program.md for the contract."""

EXPERIMENT = {
    "slug": "a-letter-dropped-or-added-then-a-move",
    "title": "One letter dropped or added in carving, with a K3-style move and a repeating key on the true length",
    "family": "6-transposition-then-tableau",
    "parent": "0093-one-wrong-letter-through-a-move",
    "changed": "0093 allowed one wrong carved letter, which keeps the length at 97. A dropped or extra letter changes the length to 98 or 96, so every grid changes shape and every later letter shifts. Here the true text is the copper with one letter struck out (96) or one unknown letter put back (98) at every place outside the crib stretches, run through every single move on that length (K3's rule, one quarter turn, plain and true-keyword columnar) and a repeating key of length 1-26.",
    "hypothesis_expert": (
        "Type 7 of directions.md. K2 has a confirmed carving error: an S dropped from the copper and the text corrected "
        "in 2006 (01-facts.md, kryptos-group-2006-corrected-k2.txt); 0068 tested one letter missing, extra or wrong only "
        "for autokey with no move. A dropped letter matters for type 1 because 97 is prime and 96 and 98 are not: 96 = "
        "8 x 12, 98 = 7 x 14. Variants: delete carved letter j (j outside the crib stretches, 73 places) or insert an "
        "unknown at gap j (outside the inside of either stretch, 76 gaps); crib places shift with it. Moves on the true "
        "length n: K3's rule i -> a + b i mod n with gcd(b, n) = 1, one clockwise or anticlockwise quarter turn at widths "
        "2 to n-1, plain columnar either direction, true-keyword columnar from the puzzle's words, forward and inverse, "
        "deduplicated per n. Repeating key 1-26 after the move (slot = carved place mod p) or before it, 8 tableau "
        "classes. A crib landing on the inserted unknown imposes nothing. Ten shuffled coppers with the same variants."
    ),
    "hypothesis_eli5": (
        "Sanborn left out one letter when carving K2. If he left one out of K4, or carved one too many, the message is "
        "really 98 or 96 letters long. That matters for grid methods: 97 letters only fill a lopsided grid, but 98 fill "
        "7 rows of 14 and 96 fill 8 rows of 12. We try every place for the missing or extra letter, every grid move "
        "of experiments 80 to 85 on the corrected length, and a short repeating secret word, against the 24 known letters."
    ),
    "prediction": (
        "No variant makes a repeating key of length 20 or less consistent beyond the scrambled-copper rate; the count "
        "of consistent settings at each period lies inside the ten coppers' range, give or take one period. Zero candidates."
    ),
    "method": (
        "1. For each deletion place and insertion gap, build the true ciphertext and the shifted crib places. "
        "2. For its length, build the deduplicated single-move library. 3. For each move and class, compute the key "
        "value forced at each known letter and test periods 1-26 in both orders by slot agreement. 4. Repeat on ten "
        "shuffled coppers with the same variants. 5. List K4's settings below period 20."
    ),
    "walkthrough": (
        "1. Suppose the carver added a letter at place 50. Strike it out: the text is now 96 letters and BERLINCLOCK starts at place 63. "
        "2. Write the 96 letters into rows of 12, eight full rows, and read them out by columns. "
        "3. Each known letter lands at a new place; with a key of length p, its key letter is that place mod p. "
        "4. Known letters on the same key letter must agree. "
        "5. Suppose instead a letter was left out before place 50: put back an unknown there; it fits any key, and later known letters move up one. "
        "6. Repeat for every place, every move on 96 or 98 letters, key length 1-26 and table rule."
    ),
}

import random
from math import gcd
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.ciphers import columnar_transposition_encrypt
from kryptos.alphabets import numeric_order

PMAX = 26
ALPH = {"std": STD, "kry": KRY}
N_CONTROLS = 10
EXTRA = ["EGYPT", "CAIRO", "LUXOR", "WALL", "NOVEMBER", "MESSAGE", "DELIVER", "DELIVERING", "TRANSMIT"]


def rot(s, w, cw):
    rows = [s[i:i + w] for i in range(0, len(s), w)]
    if cw:
        return [r[c] for c in range(w) for r in reversed(rows) if c < len(r)]
    return [r[c] for c in reversed(range(w)) for r in rows if c < len(r)]


def keyword_sequence(word):
    rank = numeric_order(word)
    return sorted(range(len(rank)), key=lambda c: rank[c])


def full_sequence(word):
    w = [c for c in word.upper() if c.isalpha()]
    return sorted(range(len(w)), key=lambda c: (w[c], c))


def columnar(seq_list, order):
    idx = "".join(chr(0x100 + i) for i in seq_list)
    return [ord(ch) - 0x100 for ch in columnar_transposition_encrypt(idx, list(order))]


def library(n, vocab):
    """Distinct where-maps on n letters: where[i] = place in the moved text of letter i."""
    base = list(range(n))
    sigmas = []
    for b in range(1, n):
        if gcd(b, n) != 1:
            continue
        for a in range(n):
            out = [0] * n
            for i in range(n):
                out[(a + b * i) % n] = i
            sigmas.append(out)                          # moved[j] = orig[out[j]]
    for w in range(2, n):
        sigmas.append(rot(base, w, True)); sigmas.append(rot(base, w, False))
        sigmas.append(columnar(base, list(range(w)))); sigmas.append(columnar(base, list(range(w))[::-1]))
    words = sorted({w for w in vocab if 2 <= len(w) <= 30} | set(EXTRA))
    for word in words:
        for seq in (keyword_sequence(word), full_sequence(word)):
            if len(seq) >= 2:
                sigmas.append(columnar(base, seq))
    seen, lib = set(), []
    for sg in sigmas:
        fwd = [0] * n
        for j, i in enumerate(sg):
            fwd[i] = j
        for wh in (fwd, sg):
            t = tuple(wh)
            if t not in seen and t != tuple(base):
                seen.add(t); lib.append(t)
    return lib


def slot_pairs(slots):
    last, prs = {}, []
    for e, s in enumerate(slots):
        if s is None:
            continue
        if s in last:
            prs.append((last[s], e))
        last[s] = e
    return prs


def variants(places):
    """(kind, j, n, true places of the known letters (0-based), index of the true text's unknown or None)."""
    crib0 = {p - 1 for p in places}
    out = []
    for j in range(97):
        if j in crib0:
            continue
        out.append(("delete", j, 96, [i if i < j else i - 1 for i in sorted(crib0)], None))
    inner = {i for i in crib0 if i - 1 in crib0}           # gaps strictly inside a stretch
    for j in range(98):
        if j in inner:
            continue
        out.append(("insert", j, 98, [i if i < j else i + 1 for i in sorted(crib0)], j))
    return out


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    places = sorted(known)
    rng = random.Random(94)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    T = len(texts)
    classes = [(pa, ca, beau) for pa in ALPH for ca in ALPH for beau in (False, True)]
    IX = {an: {c: i for i, c in enumerate(ALPH[an])} for an in ALPH}
    PI = {an: [IX[an][known[p]] for p in places] for an in ALPH}
    libs = {n: library(n, ctx.vocabulary) for n in (96, 98)}
    VAR = variants(places)
    live = {o: [[0] * (PMAX + 1) for _ in range(T)] for o in "AB"}
    k4_low = []
    n_settings = 0
    stopped = None
    for vi, (kind, j, n, tpl, unk) in enumerate(VAR):
        if ctx.time_left() < 90:
            stopped = vi
            break
        tts = []
        for txt in texts:
            s = list(txt)
            if kind == "delete":
                del s[j]
            else:
                s.insert(j, None)
            tts.append(s)
        CIt = {an: [[None if ch is None else IX[an][ch] for ch in s] for s in tts] for an in ALPH}
        pairsB = {p: slot_pairs([i % p for i in tpl]) for p in range(1, PMAX + 1)}
        for wh in libs[n]:
            land = [wh[i] for i in tpl]
            pairsA = {p: slot_pairs([None if x == unk else x % p for x in land]) for p in range(1, PMAX + 1)}
            pB = pairsB if unk is None or unk not in land else {p: slot_pairs([None if land[e] == unk else tpl[e] % p for e in range(len(tpl))]) for p in range(1, PMAX + 1)}
            n_settings += 1
            for pa, ca, beau in classes:
                Pv = PI[pa]
                for t in range(T):
                    C = CIt[ca][t]
                    f = [None if C[x] is None else ((C[x] + Pv[e]) % 26 if beau else (C[x] - Pv[e]) % 26) for e, x in enumerate(land)]
                    for o, prs_by in (("A", pairsA), ("B", pB)):
                        L = live[o][t]
                        first = None
                        for p in range(1, PMAX + 1):
                            for a, b in prs_by[p]:
                                if f[a] != f[b]:
                                    break
                            else:
                                L[p] += 1
                                if first is None:
                                    first = p
                        if t == 0 and first is not None and first < 20:
                            k4_low.append({"variant": f"{kind} at {j + 1}", "n": n, "order": o,
                                           "class": f"{pa}/{ca}/{'beau' if beau else 'vig-var'}", "period": first})
    outside = {o: [p for p in range(1, PMAX + 1)
                   if not (min(live[o][t][p] for t in range(1, T)) <= live[o][0][p] <= max(live[o][t][p] for t in range(1, T)))]
               for o in "AB"}
    bounds = {
        "family": "one carved letter dropped (insert an unknown, n = 98) or extra (strike it, n = 96), single move on n, periodic key",
        "variants": len(VAR), "variants_done": stopped if stopped is not None else len(VAR),
        "moves_per_length": {n: len(l) for n, l in libs.items()}, "variant_move_settings": n_settings,
        "periods": [1, PMAX], "classes": 8,
        "k4_live_by_period": {o: live[o][0][1:] for o in "AB"},
        "controls_live_by_period_min": {o: [min(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in "AB"},
        "controls_live_by_period_max": {o: [max(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in "AB"},
        "periods_outside_control_range": outside,
        "k4_live_below_20": k4_low[:40], "n_k4_live_below_20": len(k4_low),
        "controls": f"{N_CONTROLS} shuffled coppers (seed 94), same variants, identical search",
    }
    notes = (f"{len(VAR)} variants x {libs[96].__len__():,}/{libs[98].__len__():,} moves (96/98) = {n_settings:,} settings x 8 classes x "
             f"2 orders, periods 1-26. K4 live below period 20: {len(k4_low)}. Outside control range: {outside}."
             + (f" Stopped after {stopped} variants for time." if stopped is not None else ""))
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    s = ct[:49] + ct[50:]
    rows = [s[i:i + 12] for i in range(0, 96, 12)]
    lines = ["strike carved letter 50 (" + ct[49] + "): 96 letters in 8 rows of 12", ""] + ["  " + r for r in rows]
    lines += ["", "known letters after the strike: EASTNORTHEAST at 22-34, BERLINCLOCK at 63-73"]
    return "\n".join(lines)
