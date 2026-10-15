"""Experiment 0023. See program.md for the contract."""

EXPERIMENT = {
    "slug": "masks-reversal-and-nulls-then-tableau",
    "title": "Masks that move the known letters: the message written backwards, or padded with nulls, before a periodic tableau",
    "family": "2-masked-plaintext",
    "parent": None,
    "changed": "New root in family 2. The mask is a known rearrangement or padding of the plaintext applied before a periodic tableau: reversal, a null before every k-th letter, or a run of nulls at the start. The cribs then sit at computable intermediate positions.",
    "hypothesis_expert": (
        "Scheidt: 'I masked the English language' (C4); the NPR 2005 guesses were nulls and phonetic "
        "spelling, and reversal is the simplest Sanborn-style 'visual system' (C3). A mask that only moves "
        "letters or inserts nulls is a monotone or mirrored map from plaintext position to intermediate "
        "position; after it a periodic tableau with separate alphabets forces key letters at the mapped "
        "positions, and the divisor rule gives the live periods exactly as in 0006. Masks: reversal; a null "
        "before every k-th letter for k = 2 to 24 at every phase; a prefix of 1 to 24 nulls; and reversal "
        "combined with each. For each mask and each of the 24 conventions the smallest live period is found; "
        "periods up to 30 have their forced fragments matched against the vocabulary and K1-K3 windows and "
        "scored as English, with ten shuffled controls. Bounds: complete for these masks and conventions."
    ),
    "hypothesis_eli5": (
        "The cipher's designer said he first disguised the English before enciphering it. Two simple "
        "disguises change where the known letters sit without changing them: writing the message backwards, "
        "or slipping a meaningless letter in after every few real ones. We try each disguise, work out where "
        "EASTNORTHEAST and BERLINCLOCK would then sit, and ask again whether a short repeating secret word "
        "could have produced the carved letters at those spots."
    ),
    "prediction": (
        "Reversal and every null pattern leave the smallest live period in the 20s or above, as random "
        "position maps do. No forced fragment matches a word or beats the shuffled controls. Zero candidates pass."
    ),
    "method": (
        "1. Build the masks as position maps from plaintext index to intermediate index. 2. For each mask and "
        "convention, force the key letter at each crib's intermediate position. 3. Find live periods by the "
        "divisor rule. 4. For live periods up to 30, match the forced fragment against the vocabulary and "
        "K1-K3 windows and score it as English. 5. Repeat the scoring on ten shuffles of K4."
    ),
    "walkthrough": (
        "1. Write the message backwards: the E of EAST at position 22 is now at position 76, and the K of "
        "CLOCK at 74 is now at 24. 2. Under the sculpture's alphabet with Vigenere, the carved letter at 76 "
        "and plaintext E force one key letter; the carved letter at 24 and plaintext K force another. "
        "3. The reversed EASTNORTHEAST occupies 64 to 76 and the reversed BERLINCLOCK 24 to 34. 4. Positions "
        "whose distance is a multiple of the period share a key letter; if their forced letters differ, that "
        "period is dead. 5. Now try padding instead: a null after every third letter pushes position 22 to "
        "29 and position 64 to 85. 6. Repeat the forcing and the period test for each padding pattern."
    ),
}

import random
from kryptos.alphabets import conventions, key_letter_for, decrypt_letter, encrypt_letter
from kryptos.facts import load_k1, load_k2, load_k3

N = 97
DIVISORS = {d: [k for k in range(1, d + 1) if d % k == 0] for d in range(1, N + 1)}
MAX_KEY_PERIOD = 30
NULL = "X"


def letters(s):
    return "".join(c for c in s if "A" <= c <= "Z")


def mask_set():
    """Each mask: (name, spec). A spec maps a plaintext string to the intermediate string of length <= 97
    (padded with nulls to 97 when shorter) and also gives the position map."""
    masks = [("identity", {"rev": False, "k": 0, "phase": 0, "prefix": 0})]
    masks.append(("reversed", {"rev": True, "k": 0, "phase": 0, "prefix": 0}))
    for rev in (False, True):
        for k in range(2, 25):
            for phase in range(k):
                masks.append((f"{'reversed, ' if rev else ''}null before every {k}th letter, phase {phase}", {"rev": rev, "k": k, "phase": phase, "prefix": 0}))
        for prefix in range(1, 25):
            masks.append((f"{'reversed, ' if rev else ''}{prefix} nulls first", {"rev": rev, "k": 0, "phase": 0, "prefix": prefix}))
    return masks


def position_map(spec):
    """Plaintext index (0-based, 97 long) -> intermediate index, or None if pushed past 97."""
    order = list(range(N))[::-1] if spec["rev"] else list(range(N))
    out = {}
    j = spec["prefix"]
    k, phase = spec["k"], spec["phase"]
    for n, i in enumerate(order):
        if k and n % k == phase:
            j += 1
        if j >= N:
            break
        out[i] = j
        j += 1
    return out


def apply_mask(plaintext, spec):
    pm = position_map(spec)
    inter = [NULL] * N
    for i, j in pm.items():
        inter[j] = plaintext[i]
    return "".join(inter)


def encrypt(plaintext, key):
    inter = apply_mask(plaintext, key["mask"])
    pa, ca, ka, m, k = key["pa"], key["ca"], key["ka"], key["m"], key["key"]
    return "".join(encrypt_letter(p, k[i % len(k)], pa, ca, ka, m) for i, p in enumerate(inter))


def score_fragment(slots, P, score):
    frag = [slots.get(s) for s in range(P)]
    runs, cur = [], []
    for ch in frag + [None]:
        if ch is None:
            if len(cur) >= 5: runs.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    qs = sum(len(r) - 3 for r in runs)
    return None if qs < 4 else sum(score(r) * (len(r) - 3) for r in runs) / qs


def search(ct, known, masks, convs, score, texts, vocab, collect):
    crib_pos = sorted(known)
    best, results, candidates = [], [], []
    for name, spec in masks:
        pm = position_map(spec)
        if any((p - 1) not in pm for p in crib_pos):
            results.append({"mask": name, "note": "a crib pushed past position 97"}); continue
        inter = [pm[p - 1] for p in crib_pos]
        minp = 99
        for conv in convs:
            pa, ca, ka, m = conv
            forced = [key_letter_for(known[p], ct[j], pa, ca, ka, m) for p, j in zip(crib_pos, inter)]
            dead = set()
            for a in range(24):
                for b in range(a + 1, 24):
                    if forced[a] != forced[b]:
                        dead.update(DIVISORS[abs(inter[a] - inter[b])])
            live = [P for P in range(1, N + 1) if P not in dead]
            minp = min(minp, live[0])
            for P in [P for P in live if P <= MAX_KEY_PERIOD]:
                slots = {j % P: l for j, l in zip(inter, forced)}
                sc = score_fragment(slots, P, score)
                if sc is not None and (len(best) < 15 or sc > best[-1][0]):
                    best.append((sc, name, "/".join(conv), P, "".join(slots.get(s, ".") for s in range(P)))); best.sort(reverse=True); best = best[:15]
                if collect:
                    pool = set(w for w in vocab if len(w) == P)
                    for t in texts:
                        for i in range(0, len(t) - P + 1):
                            pool.add(t[i:i + P])
                    for kw in pool:
                        if all(kw[s] == l for s, l in slots.items()):
                            key = {"mask": spec, "pa": pa, "ca": ca, "ka": ka, "m": m, "key": kw}
                            inter_pt = "".join(decrypt_letter(ct[i], kw[i % P], pa, ca, ka, m) for i in range(N))
                            pt = [NULL] * N
                            for i, j in pm.items():
                                pt[i] = inter_pt[j]
                            candidates.append({"plaintext": "".join(pt), "key": key, "key_bits": 4.7 * P + 8, "key_description": f"{name}; period {P} key {kw}; {pa}/{ca}/{ka} {m}"})
        results.append({"mask": name, "smallest_live_period": minp})
    return best, results, candidates


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    masks = mask_set()
    convs = list(conventions())
    vocab = list(ctx.vocabulary)
    texts = [letters(load_k1()["plaintext"]), letters(load_k2()["plaintext_as_carved"]), letters(load_k3()["plaintext"])]
    best, results, candidates = search(ct, known, masks, convs, ctx.english_score, texts, vocab, True)
    nulls = []
    for seed in range(10):
        letters_ = list(ct); random.Random(seed).shuffle(letters_)
        nb, _, _ = search("".join(letters_), known, masks, convs, ctx.english_score, texts, vocab, False)
        nulls.append(round(nb[0][0], 3) if nb else None)
    minp_hist = {}
    for r in results:
        if "smallest_live_period" in r:
            minp_hist[r["smallest_live_period"]] = minp_hist.get(r["smallest_live_period"], 0) + 1
    return {
        "candidates": candidates[:50],
        "bounds": {"family": "masked plaintext (reversal, regular nulls, prefix nulls) then periodic tableau", "masks": len(masks), "conventions": 24,
                   "smallest_live_period_histogram": {str(k): v for k, v in sorted(minp_hist.items())},
                   "masks_dropping_a_crib": sum(1 for r in results if "note" in r),
                   "best_forced_fragments": [{"score": round(sc, 3), "mask": n, "convention": c, "period": P, "fragment": f} for sc, n, c, P, f in best],
                   "shuffled_control_best": nulls, "vocab_matches": len(candidates)},
        "notes": f"{len(masks)} masks x 24 conventions. Smallest live period over all masks: {min(minp_hist) if minp_hist else None}. Best fragment {best[0][0]:.3f} vs shuffled best {max(x for x in nulls if x is not None):.3f}. {len(candidates)} matches.",
    }


def worked_example(ctx, key):
    spec = {"rev": True, "k": 0, "phase": 0, "prefix": 0}
    pm = position_map(spec)
    lines = ["mask: the message written backwards; convention kry/kry/kry Vigenere", "", "plain pos  letter  sits at  carved there  forced key letter"]
    for pos in (22, 23, 24, 64, 65, 74):
        j = pm[pos - 1]
        lines.append(f"{pos:>9}    {ctx.KNOWN[pos]}       {j+1:>3}        {ctx.K4[j]}            {key_letter_for(ctx.KNOWN[pos], ctx.K4[j], 'kry', 'kry', 'kry', 'vig')}")
    spec2 = {"rev": False, "k": 3, "phase": 0, "prefix": 0}
    pm2 = position_map(spec2)
    lines.append("")
    lines.append(f"mask: a null before every 3rd letter: position 22 sits at {pm2[21]+1}, position 64 at {pm2[63]+1}")
    return "\n".join(lines)
