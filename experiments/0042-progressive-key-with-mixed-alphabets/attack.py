"""Experiment 0042. See program.md for the contract."""

EXPERIMENT = {
    "slug": "progressive-key-with-mixed-alphabets",
    "title": "A progressive key on a table rebuilt from the puzzle's words",
    "family": "1-keyed-periodic",
    "parent": "0011-progressive-key-period-sweep",
    "changed": "Experiment 11 killed progressive keys at periods 1 to 25 and 31 to 51 under the standard and KRYPTOS alphabets. Here the plain and cipher alphabets are the keyword mixings of every vocabulary word; the key alphabet drops out of the consistency test. Periods 1 to 30, steps 1 to 25, the per-repeat form.",
    "hypothesis_expert": (
        "The Trithemius progression on a keyword alphabet is the classical combination the manuals teach "
        "(C5): key index at position i is base[i mod P] plus d times the repeat number. Experiment 11 swept "
        "it under 24 conventions; the consistency test depends only on the plain and cipher alphabets, so "
        "the 63 x 63 keyword-mixed pairs from the vocabulary are the untested corner. For each pair, mode, "
        "period 1-30 and step 1-25, every crib forces the base letter of its slot after the progression is "
        "subtracted; a slot forced two ways kills the combination. About 9 million combinations, 24 checks "
        "each, with early exit. Survivors at periods up to 30 have their forced base fragment matched against "
        "the vocabulary and K1-K3 windows. Bounds: complete for this pool, these periods and steps, the "
        "per-repeat form; the per-letter form and periods above 30 are not covered."
    ),
    "hypothesis_eli5": (
        "Experiment 11 tried the trick where the secret word slides one notch further each time it repeats, "
        "and found that no short word works with the sculpture's own table. The table could have been built "
        "from another word, which changes the sums. So we rebuild the table from every word the puzzle knows "
        "and try every word length up to 30 and every slide again."
    ),
    "prediction": (
        "Periods 1 to 25 die at every step under every alphabet pair, as they did under the sculpture's "
        "alphabets; a scatter of chance survivors appears at 26 to 30. No forced fragment matches a word; "
        "zero candidates pass."
    ),
    "method": (
        "1. Build the alphabet pool. 2. For each plain and cipher alphabet and mode, compute the forced key "
        "index at each crib. 3. For each period and step, subtract the progression and reduce to the slot; "
        "reject on disagreement. 4. Count survivors by period; match surviving fragments against the "
        "vocabulary and K1-K3 windows; decrypt and submit matches."
    ),
    "walkthrough": (
        "1. Build the alphabet from ABSCISSA: ABSCIDEFGHJKLMNOPQRTUVWXYZ, and use it for the message; keep "
        "KRYPTOS for the carved letters; Vigenere. 2. Period 13, step 2: position 22 is E, index 5 in the "
        "ABSCISSA alphabet; carved F is index 11 in KRYPTOS; the key index is 6; position 22 lies in repeat "
        "1 (positions 14 to 26), so subtract one step: base index 4 for slot 8. 3. Position 74, the K of "
        "CLOCK, is repeat 5, slot 8: its key index minus five steps must also give 4. 4. If not, period 13 "
        "step 2 is dead for this pair of alphabets. 5. Try every step and every pair; a survivor gives a "
        "pattern of base letters with blanks to slide the puzzle's words across."
    ),
}

from kryptos.alphabets import keyword_mixed
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY, load_k1, load_k2, load_k3

N = 97
MAXP, MAXD = 30, 25
MODES = {"vig": lambda p, c: (c - p) % 26, "beau": lambda p, c: (c + p) % 26, "varbeau": lambda p, c: (p - c) % 26}
DEC = {"vig": lambda c, k: (c - k) % 26, "beau": lambda c, k: (k - c) % 26, "varbeau": lambda c, k: (c + k) % 26}
ENC = {"vig": lambda p, k: (p + k) % 26, "beau": lambda p, k: (k - p) % 26, "varbeau": lambda p, k: (p - k) % 26}


def letters(s):
    return "".join(c for c in s if "A" <= c <= "Z")


def pool_of(vocab):
    pool = {"std": STD, "kry": KRY}
    for w in vocab:
        if len(set(w)) >= 3:
            pool[f"{w}/keyword"] = keyword_mixed(w)
    seen, out = {}, {}
    for name, A in pool.items():
        if A not in seen:
            seen[A] = name; out[name] = A
    return out


def encrypt(plaintext, key):
    pa, ca, m, k, d = key["pa"], key["ca"], key["m"], key["key"], key["step"]   # key: list of base indices
    P = len(k)
    return "".join(ca[ENC[m](pa.index(p), (k[i % P] + d * (i // P)) % 26)] for i, p in enumerate(plaintext))


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    vocab = list(ctx.vocabulary)
    pool = pool_of(vocab)
    index = {n: {ch: i for i, ch in enumerate(A)} for n, A in pool.items()}
    texts = [letters(load_k1()["plaintext"]), letters(load_k2()["plaintext_as_carved"]), letters(load_k3()["plaintext"])]
    crib = sorted(known.items())
    reps = [None] + [[(pos - 1) % P for pos, _ in crib] for P in range(1, MAXP + 1)]
    repn = [None] + [[(pos - 1) // P for pos, _ in crib] for P in range(1, MAXP + 1)]
    survivors = {}
    candidates, matches = [], []
    checked = 0
    for pname, pa in pool.items():
        pidx = index[pname]
        for cname, ca in pool.items():
            cidx = index[cname]
            for m, f in MODES.items():
                forced = [f(pidx[p], cidx[ct[pos - 1]]) for pos, p in crib]
                for P in range(1, MAXP + 1):
                    slots_of, rep_of = reps[P], repn[P]
                    for d in range(1, MAXD + 1):
                        checked += 1
                        base = {}
                        ok = True
                        for k in range(24):
                            b = (forced[k] - d * rep_of[k]) % 26
                            s = slots_of[k]
                            if s in base:
                                if base[s] != b:
                                    ok = False; break
                            else:
                                base[s] = b
                        if not ok:
                            continue
                        survivors[P] = survivors.get(P, 0) + 1
                        for ka_name in ("std", "kry"):
                            A = pool[ka_name]
                            wordpool = set(x for x in vocab if len(x) == P)
                            for t in texts:
                                for i in range(0, len(t) - P + 1):
                                    wordpool.add(t[i:i + P])
                            for kw in wordpool:
                                if all(A.index(kw[s]) == b for s, b in base.items()):
                                    kidx = [A.index(ch) for ch in kw]
                                    key = {"pa": pa, "ca": ca, "m": m, "key": kidx, "step": d}
                                    pt = "".join(pa[DEC[m](cidx[c], (kidx[i % P] + d * (i // P)) % 26)] for i, c in enumerate(ct))
                                    matches.append((pname, cname, m, P, d, kw))
                                    candidates.append({"plaintext": pt, "key": key, "key_bits": 4.7 * P + 8, "key_description": f"period {P} key {kw} step {d}; plain {pname}, cipher {cname}, key alphabet {ka_name}, {m}"})
            if ctx.time_left() < 60:
                break
        if ctx.time_left() < 60:
            break
    return {
        "candidates": candidates[:50],
        "bounds": {"family": "progressive key (per-repeat), keyword-mixed alphabets from the vocabulary", "alphabets": len(pool), "periods": f"1-{MAXP}", "steps": f"1-{MAXD}",
                   "combinations_checked": checked, "survivors_by_period": {str(P): n for P, n in sorted(survivors.items())},
                   "periods_dead_at_every_step_and_pair": [P for P in range(1, MAXP + 1) if P not in survivors],
                   "vocab_matches": len(matches)},
        "notes": f"{checked} combinations. Periods dead under every pair and step: {[P for P in range(1, MAXP + 1) if P not in survivors]}. Survivors by period: {dict(sorted(survivors.items()))}. {len(matches)} matches.",
    }


def worked_example(ctx, key):
    pa, ca = keyword_mixed("ABSCISSA"), KRY
    lines = [f"plain alphabet ABSCISSA/keyword {pa}; cipher KRYPTOS; Vigenere; period 13, step 2", "", "pos  plain  carved  key index  repeat  base index  slot"]
    for pos in (22, 23, 24, 64, 74):
        p, c = ctx.KNOWN[pos], ctx.K4[pos - 1]
        k = (ca.index(c) - pa.index(p)) % 26; rep = (pos - 1) // 13
        lines.append(f"{pos:>3}    {p}      {c}       {k:>2}        {rep}        {(k - 2 * rep) % 26:>2}       {(pos - 1) % 13}")
    lines.append("")
    lines.append("positions 22 and 74 share slot 8: their base indices must agree, or period 13 step 2 is dead for this pair.")
    return "\n".join(lines)
