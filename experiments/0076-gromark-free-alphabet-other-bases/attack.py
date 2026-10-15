"""Experiment 0076. See program.md for the contract."""

EXPERIMENT = {
    "slug": "gromark-free-alphabet-other-bases",
    "title": "Gromark with any mixed alphabet, in number bases other than ten",
    "family": "5-gromark",
    "parent": "0069-gromark-with-a-free-alphabet",
    "changed": "Experiment 69 closed base-10 Gromark for any alphabet. Scheidt mentioned base 16 and Mayan base 20 and 60, and the Berlin clock counts in fives. Here the running digits are in base 2 to 16 (except 10) and base 26, with every two-term rule up to five digits back and every primer, and the alphabet is again left completely free.",
    "hypothesis_expert": (
        "Family 5, free-alphabet Gromark beyond base 10 (C4(b): Scheidt's remarks on 'base 16' and Mayan "
        "bases, 03-scheidt-said.md; C12(b): the Mengenlehreuhr counts in fives and ones, sources/"
        "nyt-2010-berlin-clue.txt). Key digits d[i] = d[i-a] + d[i-b] mod B, 1 <= a < b <= 5 (10 rules), every "
        "primer of b digits, bases B = 2-9 and 11-16 (and 26 for rules with b <= 4); the digit is added to "
        "the letter index mod 26 as in Gromark. Four forms as in 0069 (M[P+d]=c, M[P-d]=c, M[C-d]=p, "
        "M[C+d]=p; M an unknown mixed alphabet). Same-letter crib pairs fix the digit difference to one or two "
        "values (d_k - d_l = need or need - 26 within -(B-1)..B-1), which filters almost every primer; the rest "
        "get the full bijection check. Exhaustive for these bases and rules. K4 and ten shuffled coppers."
    ),
    "hypothesis_eli5": (
        "Experiment 69 showed that a Gromark cipher, whose key is a growing stream of digits plus a "
        "scrambled alphabet, cannot have made the copper if the digits run from 0 to 9. Scheidt has talked "
        "about other number systems, base 16 and the Maya's base 20, and the Berlin clock counts in fives. "
        "So we run the same exact test with digits in every base from 2 to 16 and in base 26, again with any "
        "scrambled alphabet at all."
    ),
    "prediction": (
        "No primer under any base, rule and form gives a consistent alphabet on K4; the ten shuffled coppers "
        "give none either, except possibly in base 26 where the digit differences are least constrained, and "
        "there no more often on K4 than on the shuffles. Zero candidates pass."
    ),
    "method": (
        "1. For each base and rule, generate the digit stream from every primer and keep the digits at the 24 "
        "known places. 2. For each form, list same-letter pairs and the digit differences they allow. "
        "3. Keep primers that meet every pair, then check the full one-to-one condition. 4. Repeat on ten "
        "shuffled coppers."
    ),
    "walkthrough": (
        "1. Base 2, each digit the sum of the digits five and four back, mod 2, primer 1 0 1 1 0. 2. The stream "
        "begins 1 0 1 1 0 1 1 0 1 1 0 1 1 0 1 1 0 1 1 0 1 1 0 1 1 0 1. 3. Places 26 and 27 both carve Q, from "
        "known N (13) and O (14). 4. With the form M[P + d] = c: 13 + 0 = 13 and 14 + 1 = 15, two different "
        "slots, which cannot both hold Q. 5. This primer is dead. 6. Repeat for every primer, rule, base and form."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD

N = 97
FORMS = ("M[P+d]=c", "M[P-d]=c", "M[C-d]=p", "M[C+d]=p")
RULES5 = [(a, b) for b in range(2, 6) for a in range(1, b)]


def plan():
    out = []
    for B in list(range(2, 10)) + list(range(11, 17)):
        for a, b in RULES5:
            out.append((B, a, b))
    for a, b in RULES5:
        if b <= 4:
            out.append((26, a, b))
    return out


def crib_digits(B, a, b, crib_idx):
    m = len(crib_idx)
    top = max(crib_idx) + 1
    out = bytearray(m * B ** b)
    w = 0
    for n in range(B ** b):
        d, x = [], n
        for _ in range(b):
            d.append(x % B); x //= B
        for i in range(b, top):
            d.append((d[i - a] + d[i - b]) % B)
        for i in crib_idx:
            out[w] = d[i]; w += 1
    return out


def form_rows(ct, items, form):
    rows = []
    for pos, p in items:
        c = ct[pos - 1]
        rows.append({"M[P+d]=c": (STD.index(p), 1, c), "M[P-d]=c": (STD.index(p), -1, c),
                     "M[C-d]=p": (STD.index(c), -1, p), "M[C+d]=p": (STD.index(c), 1, p)}[form])
    return rows


def pair_constraints(rows, B):
    pairs = []
    for k in range(len(rows)):
        for l in range(k + 1, len(rows)):
            if rows[k][2] == rows[l][2]:
                s = rows[k][1]
                need = (s * (rows[l][0] - rows[k][0])) % 26
                allowed = {v for v in (need, need - 26) if -(B - 1) <= v <= B - 1}
                if not allowed:
                    return None
                pairs.append((k, l, allowed))
    pairs.sort(key=lambda t: len(t[2]))
    return pairs


def full_check(rows, digs, off):
    s2l, l2s = {}, {}
    for k, (base, s, letter) in enumerate(rows):
        slot = (base + s * digs[off + k]) % 26
        if s2l.setdefault(slot, letter) != letter or l2s.setdefault(letter, slot) != slot:
            return False
    return True


def test(ct, items, digs, m, count, B):
    hits = 0
    for form in FORMS:
        rows = form_rows(ct, items, form)
        pairs = pair_constraints(rows, B)
        if pairs is None:
            continue
        for n in range(count):
            off = m * n
            ok = True
            for k, l, allowed in pairs:
                if digs[off + k] - digs[off + l] not in allowed:
                    ok = False; break
            if ok and full_check(rows, digs, off):
                hits += 1
    return hits


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    items = sorted(known.items())
    idx = [pos - 1 for pos, _ in items]
    m = len(idx)
    rng = random.Random(76)
    shuffles = []
    for _ in range(10):
        sh = list(ct); rng.shuffle(sh); shuffles.append("".join(sh))
    per_base, done, primers = {}, 0, 0
    for B, a, b in plan():
        digs = crib_digits(B, a, b, idx)
        count = B ** b
        primers += count
        k = test(ct, items, digs, m, count, B)
        c = [test(sh, items, digs, m, count, B) for sh in shuffles]
        e = per_base.setdefault(B, {"k4": 0, "controls": [0] * 10, "primers": 0})
        e["k4"] += k; e["primers"] += count
        for r in range(10):
            e["controls"][r] += c[r]
        done += 1
        if ctx.time_left() < 60:
            break
    return {
        "candidates": [],
        "bounds": {"family": "Gromark, free mixed alphabet, bases 2-9, 11-16 and 26", "rules": "two-term, lags up to 5 (base 26: up to 4)",
                   "settings_done": done, "settings_planned": len(plan()), "primers": primers, "forms": list(FORMS),
                   "by_base": {str(B): v for B, v in per_base.items()}},
        "notes": f"{done} of {len(plan())} base-rule settings, {primers:,} primers x 4 forms. Consistent primers by base, K4 (controls): "
                 + "; ".join(f"base {B}: {v['k4']} ({min(v['controls'])}-{max(v['controls'])})" for B, v in per_base.items()) + ".",
    }


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    d = [1, 0, 1, 1, 0]
    while len(d) < 97:
        d.append((d[-5] + d[-4]) % 2)
    ct, kn = ctx.K4, ctx.KNOWN
    lines = ["base 2, digits 5 and 4 back, primer 10110", "stream " + "".join(map(str, d[:34])), "", "place  known  carved  digit  slot (M[P+d]=c)"]
    for pos in (26, 27, 22, 23):
        lines.append(f"{pos:>5}  {kn[pos]:>5}  {ct[pos - 1]:>6}  {d[pos - 1]:>5}  {(STD.index(kn[pos]) + d[pos - 1]) % 26:>4}")
    return "\n".join(lines)
