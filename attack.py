"""Experiment 0029. See program.md for the contract."""

EXPERIMENT = {
    "slug": "small-shift-keys-closeness-under-all-alphabets",
    "title": "Bean's closeness made a test: is there an alphabet pair under which every known letter moves only a little?",
    "family": "1-keyed-periodic",
    "parent": "0028-gromark-small-bases-two-to-nine",
    "changed": "The statistic is the size of the forced shift, not its recurrence. For every alphabet pair and mode the 24 forced shifts are reduced to circular magnitudes 0-13, and the pair with the smallest largest magnitude is the lead; ten shuffled controls say what chance gives.",
    "hypothesis_expert": (
        "Bean (knowledge/04-structure.md): the ten crib plaintext letters that lie in KRYPTOS sit within 0-2 "
        "places of their ciphertext letters on the standard alphabet, about one permutation in 5,520, and "
        "he reads K4 as letter-for-letter with a cipher alphabet near the standard one. A Gronsfeld-like key "
        "of small digits, or any system whose shifts are small under the right pair of alphabets, would show "
        "as a pair under which all 24 forced shifts have small circular magnitude. Over the 248-alphabet pool "
        "squared and three modes, 184,512 pairs, the chance that a pair keeps all 24 magnitudes at or below "
        "3 is (7/26)^24, about 10^-14 per pair; at or below 6 it is (13/26)^24, about 6 x 10^-8 per pair, "
        "so a largest magnitude of 6 or less would be a lead and 3 or less decisive. Ten shuffles of K4 "
        "calibrate the smallest largest-magnitude. Bounds: complete for this pool; diagnostic, no candidate."
    ),
    "hypothesis_eli5": (
        "A cryptanalyst noticed that several known letters barely move: S becomes R, T becomes V, K stays "
        "K. If the whole cipher only nudged letters a little along some alphabet, that alphabet would make "
        "every one of the 24 known moves small. We try every alphabet the puzzle's words can build, measure "
        "the biggest nudge each needs, and keep the alphabet with the smallest biggest nudge. Random letters "
        "tell us how small that can get by luck."
    ),
    "prediction": (
        "The smallest largest magnitude over all pairs is 9 or 10, the same as on shuffled K4. Under the "
        "standard-standard pair the KRYPTOS-letter cribs are close, as Bean found, but the other fourteen "
        "cribs are not, and no pair makes all 24 small."
    ),
    "method": (
        "1. Build the alphabet pool. 2. For each plain and cipher alphabet and mode, compute the 24 forced "
        "shifts and their circular magnitudes. 3. Record the largest magnitude per pair and keep the ten "
        "smallest, with the shift sequences. 4. Repeat on ten shuffles of K4. 5. Report Bean's own "
        "statistic, the magnitudes under the standard pair, for reference."
    ),
    "walkthrough": (
        "1. Take the plain alphabet for both message and carved letters, Vigenere. 2. Position 24 is S, "
        "carved R: R is one place before S, a nudge of 1. 3. Position 25 is T, carved V: a nudge of 2. "
        "4. Position 23 is A, carved L: a nudge of 11, which is large. 5. Write down all 24 nudges and keep "
        "the biggest: 12 or more here. 6. Now rebuild the alphabet from a word, say PALIMPSEST, and measure "
        "again; the nudges change. 7. The alphabet with the smallest biggest nudge is the one to look at."
    ),
}

import random
from kryptos.alphabets import keyword_mixed, columnar_mixed, keyed_columnar_mixed, alternate_vertical_mixed
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

MODES = {"vig": lambda p, c: (c - p) % 26, "beau": lambda p, c: (c + p) % 26, "varbeau": lambda p, c: (p - c) % 26}
MIX = {"keyword": keyword_mixed, "columnar": columnar_mixed, "keyed_columnar": keyed_columnar_mixed, "alt_vertical": alternate_vertical_mixed}


def encrypt(plaintext, key):
    raise NotImplementedError("diagnostic experiment: no candidate is submitted")


def pool_of(vocab):
    pool = {"std": STD, "kry": KRY}
    for w in vocab:
        if len(set(w)) >= 3:
            for mname, fn in MIX.items():
                pool[f"{w}/{mname}"] = fn(w)
    seen, out = {}, {}
    for name, A in pool.items():
        if A not in seen:
            seen[A] = name; out[name] = A
    return out


def mag(s):
    return min(s, 26 - s)


def sweep(ct, known, pool, index):
    crib_pos = sorted(known)
    best = []
    for pname in pool:
        pidx = index[pname]
        for cname in pool:
            cidx = index[cname]
            for m, f in MODES.items():
                shifts = [f(pidx[known[pos]], cidx[ct[pos - 1]]) for pos in crib_pos]
                mags = [mag(s) for s in shifts]
                big = max(mags)
                if len(best) < 10 or big < best[-1][0]:
                    best.append((big, sum(mags) / 24, pname, cname, m, shifts)); best.sort(key=lambda t: (t[0], t[1])); best = best[:10]
    return best


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    pool = pool_of(list(ctx.vocabulary))
    index = {n: {ch: i for i, ch in enumerate(A)} for n, A in pool.items()}
    best = sweep(ct, known, pool, index)
    nulls = []
    for seed in range(10):
        letters_ = list(ct); random.Random(seed).shuffle(letters_)
        nb = sweep("".join(letters_), known, pool, index)
        nulls.append(nb[0][0])
    crib_pos = sorted(known)
    bean = [(pos, known[pos], ct[pos - 1], mag((STD.index(ct[pos - 1]) - STD.index(known[pos])) % 26)) for pos in crib_pos]
    return {
        "candidates": [],
        "bounds": {"family": "small-shift keys under all alphabet pairs (Bean's closeness)", "alphabets": len(pool), "pairs_x_modes": len(pool) ** 2 * 3,
                   "smallest_largest_magnitude": best[0][0],
                   "ten_best_pairs": [{"largest": b, "mean": round(mn, 2), "plain": p, "cipher": c, "mode": m, "shifts": s} for b, mn, p, c, m, s in best],
                   "shuffled_k4_smallest_largest_magnitude": nulls,
                   "bean_statistic_standard_pair": [{"pos": a, "plain": b, "cipher": c, "magnitude": d} for a, b, c, d in bean],
                   "bean_kryptos_letters_sum": sum(d for _, b, _, d in bean if b in "KRYPTOS")},
        "notes": f"Diagnostic, no candidates. Smallest largest magnitude over {len(pool) ** 2 * 3} pairs: {best[0][0]} ({best[0][2]} / {best[0][3]} {best[0][4]}); shuffled K4 gives {nulls}.",
    }


def worked_example(ctx, key):
    lines = ["standard alphabet for both message and carved letters, Vigenere: nudge per known letter", "", "pos  plain  carved  nudge"]
    for pos in sorted(ctx.KNOWN):
        p, c = ctx.KNOWN[pos], ctx.K4[pos - 1]
        lines.append(f"{pos:>3}    {p}      {c}      {mag((STD.index(c) - STD.index(p)) % 26):>2}{'   (KRYPTOS letter)' if p in 'KRYPTOS' else ''}")
    return "\n".join(lines)
