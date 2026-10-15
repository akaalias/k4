"""Experiment 0107. See program.md for the contract."""

EXPERIMENT = {
    "slug": "three-term-gromark-with-a-free-alphabet",
    "title": "Gromark with a three-term digit rule and any mixed alphabet at all",
    "family": "5-gromark-lfsr",
    "parent": "0069-gromark-with-a-free-alphabet",
    "changed": "0069 closed two-term Gromark rules on a free alphabet; 0046 tried three-term rules only on alphabets built from the puzzle's words. Here the digit rule is d[i] = d[i-a] + d[i-b] + d[i-c] mod 10 for every 1 <= a < b < c <= 6 (20 rules) and every primer of c digits, with the mixed alphabet left free, tested by 0069's exact digit-difference method.",
    "hypothesis_expert": (
        "Family 5's open corner: 'three-term rules with a free alphabet' (families.md). Key digits base 10 from "
        "d[i] = d[i-a] + d[i-b] + d[i-c] mod 10, 1 <= a < b < c <= 6, every primer of c digits (10,631,000 primers in all). "
        "Four forms as in 0069 (M an unknown mixed alphabet, P and C standard indices): M[P + d] = c, M[P - d] = c, "
        "M[C - d] = p, M[C + d] = p. Pairs of known places with the same letter fix exact digit differences (digits are "
        "0-9), then the full partial-bijection check. Exhaustive in base 10 for these rules. C22(a), C4(b). A planted text "
        "is recovered. Ten shuffled coppers."
    ),
    "hypothesis_eli5": (
        "Gromark makes a long stream of key digits from a short starting number, each new digit the sum of earlier "
        "ones, and uses a scrambled alphabet. Experiment 69 tried every rule that adds two earlier digits, with any "
        "scrambled alphabet, and found nothing. Here each digit is the sum of three earlier ones, every such rule and "
        "every starting number up to six digits, again with any scrambled alphabet."
    ),
    "prediction": "No primer under any of the 20 rules and 4 forms is consistent, on K4 or on any shuffled copper. Zero candidates.",
    "method": (
        "1. For each rule, generate the digit stream from every primer and keep the digits at the 24 known places. "
        "2. For each form, pairs of known places with the same letter fix digit differences; keep primers meeting them. "
        "3. Check the full one-to-one alphabet condition. 4. Repeat on ten shuffled coppers."
    ),
    "walkthrough": (
        "1. Take the rule: each digit the sum of the digits 1, 3 and 5 places earlier, mod 10, and the primer 1 2 3 4 5. "
        "2. Extend the stream to place 74. "
        "3. Places 26 and 27 both carve Q, from known N and O. "
        "4. With the form M[P + d] = c, N plus the 26th digit and O plus the 27th digit must be the same slot of the alphabet, since both hold Q. "
        "5. If not, the primer is dead; repeat for every primer, rule and form."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD

N = 97
RULES = [(a, b, c) for c in range(3, 7) for b in range(2, c) for a in range(1, b)]
FORMS = ("M[P+d]=c", "M[P-d]=c", "M[C-d]=p", "M[C+d]=p")


def crib_digits(a, b, c, crib_idx):
    """Bytearray of len(crib_idx) digits per primer of c digits, in primer order: d[i] = d[i-a] + d[i-b] + d[i-c] mod 10."""
    m = len(crib_idx)
    top = max(crib_idx) + 1
    out = bytearray(m * 10 ** c)
    w = 0
    for n in range(10 ** c):
        d = [int(x) for x in str(n).zfill(c)]
        for i in range(c, top):
            d.append((d[i - a] + d[i - b] + d[i - c]) % 10)
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
    rng = random.Random(107)
    shuffles = []
    for _ in range(10):
        sh = list(ct); rng.shuffle(sh); shuffles.append("".join(sh))
    k4_hits, ctrl_hits, primers, done = [], [0] * 10, 0, []
    assert plant_check()
    for a, b, c in RULES:
        digs = crib_digits(a, b, c, crib_idx)
        count = 10 ** c
        primers += count
        for form, n in test_copper(ct, items, digs, m, count):
            k4_hits.append({"rule": [a, b, c], "primer": str(n).zfill(c), "form": form})
        for r, sh in enumerate(shuffles):
            ctrl_hits[r] += len(test_copper(sh, items, digs, m, count))
        done.append([a, b, c])
        if ctx.time_left() < 60:
            break
    return {
        "candidates": [],
        "bounds": {"family": "three-term Gromark, base 10, free mixed alphabet", "rules": done, "rules_planned": len(RULES), "primers": primers,
                   "forms": list(FORMS), "k4_consistent": k4_hits[:20], "k4_count": len(k4_hits), "control_counts": ctrl_hits},
        "notes": f"{len(done)} of {len(RULES)} rules, {primers:,} primers x 4 forms: K4 consistent primers {len(k4_hits)}; ten shuffled coppers {ctrl_hits}.",
    }


def plant_check():
    """A planted three-term Gromark text with a random alphabet must be found by test_copper for its own primer."""
    from kryptos.facts import KNOWN
    rng = random.Random(8)
    M = list(STD); rng.shuffle(M)
    a, b, c = 1, 3, 5
    d = [int(x) for x in "40271"]
    for i in range(5, N):
        d.append((d[i - a] + d[i - b] + d[i - c]) % 10)
    pt = [rng.choice(STD) for _ in range(N)]
    for q, ch in KNOWN.items():
        pt[q - 1] = ch
    ct = "".join(M[(STD.index(p) + d[i]) % 26] for i, p in enumerate(pt))
    items = sorted(KNOWN.items())
    idx = [q - 1 for q, _ in items]
    digs = bytearray(d[i] for i in idx)
    return any(f == "M[P+d]=c" for f, _ in test_copper(ct, items, digs, len(idx), 1))


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    d = [int(x) for x in "12345"]
    for i in range(5, 40):
        d.append((d[i - 1] + d[i - 3] + d[i - 5]) % 10)
    lines = ["rule: each digit the sum of the digits 1, 3 and 5 places earlier, mod 10; primer 1 2 3 4 5",
             "stream: " + " ".join(map(str, d[:34])), "",
             "places 26 and 27 both carve Q, from known N and O; form M[P + d] = c:",
             f"  N (13) + digit {d[25]} = slot {(13 + d[25]) % 26};  O (14) + digit {d[26]} = slot {(14 + d[26]) % 26}",
             "  two different slots of one alphabet cannot both hold Q" if (13 + d[25]) % 26 != (14 + d[26]) % 26 else "  same slot: consistent so far"]
    return "\n".join(lines)
