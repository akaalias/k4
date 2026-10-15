"""Experiment 0069. See program.md for the contract."""

EXPERIMENT = {
    "slug": "gromark-with-a-free-alphabet",
    "title": "Gromark with any mixed alphabet at all, not just ones built from the puzzle's words",
    "family": "5-gromark",
    "parent": "0046-gromark-three-term-rules-and-higher-bases",
    "changed": "Experiments 13, 28, 46 and 54 tested the Gromark running-number key only on alphabets built from the puzzle's words. Here the mixed alphabet is left completely free: the 24 known letters must fit some one-to-one alphabet, which the run checks exactly for every starting number and every two-term rule up to six digits back.",
    "hypothesis_expert": (
        "Family 5, free-alphabet Gromark (the open corner named in families.md after 0028 and 0046). Key "
        "digits base 10 from a lagged-Fibonacci rule d[i] = d[i-a] + d[i-b] mod 10, 1 <= a < b <= 6 (15 rules, "
        "including Rogers' Gromark a = 4, b = 5), every primer of b digits (5,432,200 primers in all). Four "
        "forms, with P, C the standard-alphabet indices and M an unknown mixed alphabet: M[P + d] = c, "
        "M[P - d] = c, M[C - d] = p, M[C + d] = p (mod 26). For each primer the 24 cribs give slot-letter pairs "
        "that must be a partial bijection: equal slots need equal letters and equal letters need equal slots. "
        "Because the digits lie in 0-9, every pair of cribs with the same letter fixes an exact digit "
        "difference, so most primers die on the first two such pairs; survivors get the full bijection "
        "check. Exhaustive for these rules and forms in base 10. Run on K4 and ten shuffled coppers. Clue "
        "entries: C22(a) (the raised YAR / DYAHR as a Gromark primer), C4(b) (Scheidt: 'base', a non-standard "
        "number system), C5 ('not mathematical' argues against it, recorded)."
    ),
    "hypothesis_eli5": (
        "Gromark is a cipher whose secret is a short starting number that grows into a long stream of "
        "digits, each digit the sum of two earlier ones, plus a scrambled alphabet. Earlier experiments only "
        "tried scrambled alphabets built from the puzzle's words. Here the alphabet can be any scramble at "
        "all. That sounds hopeless to search, but it is not: the same plain letter must always land on the "
        "same carved letter when the digit is the same, which pins the digits down so tightly that every "
        "starting number can be checked in a fraction of a second."
    ),
    "prediction": (
        "No primer under any of the 15 rules and 4 forms gives a consistent alphabet, on K4 or on any of "
        "the ten shuffled coppers. Zero candidates pass."
    ),
    "method": (
        "1. For each rule, generate the digit stream from every primer and keep the digits at the 24 known "
        "places. 2. For each form, list pairs of known places with the same letter; each fixes the difference "
        "of their two digits. 3. Keep primers that meet every such difference, then check the full one-to-one "
        "alphabet condition. 4. Repeat on ten shuffled coppers."
    ),
    "walkthrough": (
        "1. Take Rogers' rule, each digit the sum of the digits five and four places earlier, mod 10, and "
        "the primer 1 2 3 4 5. 2. The stream begins 1 2 3 4 5 3 5 7 9 8 8 2 6 7 6 0 8 3 3 6 8 1 6 9 4 9 7. "
        "3. Places 26 and 27 both carve Q, from known N and O. 4. With the form M[P + d] = c, N (13) plus the "
        "26th digit (9) gives slot 22, and O (14) plus the 27th digit (7) gives slot 21. 5. Two different "
        "slots of one alphabet cannot both hold Q, so this primer is dead. 6. Repeat for every primer, rule "
        "and form."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD

N = 97
RULES = [(a, b) for b in range(2, 7) for a in range(1, b)]
FORMS = ("M[P+d]=c", "M[P-d]=c", "M[C-d]=p", "M[C+d]=p")


def crib_digits(a, b, crib_idx):
    """Bytearray of len(crib_idx) digits per primer, in primer order."""
    m = len(crib_idx)
    top = max(crib_idx) + 1
    out = bytearray(m * 10 ** b)
    w = 0
    for n in range(10 ** b):
        d = [int(x) for x in str(n).zfill(b)]
        for i in range(b, top):
            d.append((d[i - a] + d[i - b]) % 10)
        for i in crib_idx:
            out[w] = d[i]; w += 1
    return out


def form_data(ct, known_items, form):
    """Per crib: (base index, sign of d, letter); slot = (base + sign*d) % 26, letter must biject with slot."""
    rows = []
    for pos, p in known_items:
        c = ct[pos - 1]
        if form == "M[P+d]=c":
            rows.append((STD.index(p), 1, c))
        elif form == "M[P-d]=c":
            rows.append((STD.index(p), -1, c))
        elif form == "M[C-d]=p":
            rows.append((STD.index(c), -1, p))
        else:
            rows.append((STD.index(c), 1, p))
    return rows


def equal_pairs(rows):
    """For each pair with the same letter: slots must be equal: base_k + s d_k = base_l + s d_l (mod 26),
    so s (d_k - d_l) = base_l - base_k (mod 26); with digits 0-9 the difference must be in -9..9."""
    pairs = []
    for k in range(len(rows)):
        for l in range(k + 1, len(rows)):
            if rows[k][2] == rows[l][2]:
                s = rows[k][1]
                need = (s * (rows[l][0] - rows[k][0])) % 26          # d_k - d_l mod 26
                diff = need if need <= 9 else need - 26
                if diff < -9 or diff > 9:
                    return None
                pairs.append((k, l, diff))
    return pairs


def full_check(rows, digs, off):
    s2l, l2s = {}, {}
    for k, (base, s, letter) in enumerate(rows):
        slot = (base + s * digs[off + k]) % 26
        if s2l.setdefault(slot, letter) != letter or l2s.setdefault(letter, slot) != slot:
            return False
    return True


def test_copper(ct, known_items, digs, m, count):
    hits = []
    for form in FORMS:
        rows = form_data(ct, known_items, form)
        pairs = equal_pairs(rows)
        if pairs is None:
            continue
        for n in range(count):
            off = m * n
            ok = True
            for k, l, diff in pairs:
                if digs[off + k] - digs[off + l] != diff:
                    ok = False; break
            if ok and full_check(rows, digs, off):
                hits.append((form, n))
    return hits


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    items = sorted(known.items())
    crib_idx = [pos - 1 for pos, _ in items]
    m = len(crib_idx)
    rng = random.Random(69)
    shuffles = []
    for _ in range(10):
        sh = list(ct); rng.shuffle(sh); shuffles.append("".join(sh))
    k4_hits, ctrl_hits, primers, done = [], [0] * 10, 0, []
    for a, b in RULES:
        digs = crib_digits(a, b, crib_idx)
        count = 10 ** b
        primers += count
        for form, n in test_copper(ct, items, digs, m, count):
            k4_hits.append({"rule": [a, b], "primer": str(n).zfill(b), "form": form})
        for r, sh in enumerate(shuffles):
            ctrl_hits[r] += len(test_copper(sh, items, digs, m, count))
        done.append([a, b])
        if ctx.time_left() < 60:
            break
    return {
        "candidates": [],
        "bounds": {"family": "Gromark, base 10, free mixed alphabet", "rules": done, "rules_planned": len(RULES), "primers": primers,
                   "forms": list(FORMS), "k4_consistent": k4_hits[:20], "k4_count": len(k4_hits), "control_counts": ctrl_hits},
        "notes": f"{len(done)} of {len(RULES)} rules, {primers:,} primers x 4 forms: K4 consistent primers {len(k4_hits)}; ten shuffled coppers {ctrl_hits}.",
    }


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    d = [1, 2, 3, 4, 5]
    while len(d) < 97:
        d.append((d[-5] + d[-4]) % 10)
    ct, kn = ctx.K4, ctx.KNOWN
    lines = ["Rogers' rule (5 and 4 back), primer 12345", "stream " + "".join(map(str, d[:34])), "", "place  known  carved  digit  slot (M[P+d]=c)"]
    for pos in (22, 23, 26, 27, 31):
        lines.append(f"{pos:>5}  {kn[pos]:>5}  {ct[pos - 1]:>6}  {d[pos - 1]:>5}  {(STD.index(kn[pos]) + d[pos - 1]) % 26:>4}")
    return "\n".join(lines)
