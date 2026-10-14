"""Experiment 0020. See program.md for the contract."""

EXPERIMENT = {
    "slug": "short-periods-mixed-alphabets-consistency",
    "title": "The short periods come back: a periodic tableau at periods 1 to 52 with alphabets mixed from the puzzle's words",
    "family": "1-keyed-periodic",
    "parent": "0005-quagmire-period-sweep-forced-keys",
    "changed": "0005 excluded periods 1-26 and 30-52 under the standard and KRYPTOS alphabets only. Here the plain and cipher alphabets range over the four Friedman mixings of every vocabulary word, which changes every forced key letter and so every consistency check. Family 1 re-entered with a new alphabet source.",
    "hypothesis_expert": (
        "K4's eleven width-21 vertical repeats and the width-7 doublet column (0018, knowledge/04-structure.md) "
        "are what a key of period 21 or 42 would leave: positions 21 apart share a key letter, so English "
        "bigrams repeat vertically. 0005 and 0011 killed periods 1-26 and 30-52, but only with plain and "
        "cipher alphabets in {standard, KRYPTOS}; a tableau built on PALIMPSEST, ABSCISSA or any other word "
        "(Scheidt's keyword alphabets, C5, C29) gives different forced key indices and was never swept at these "
        "periods. For each pair of alphabets from the pool (standard, KRYPTOS, four mixings of each vocabulary "
        "word, 248 in all) and each of three modes, the forced key index at every crib position follows; for "
        "each period 1-52 the slots that collide must agree. Period 21 has eleven collisions, so a surviving "
        "pair there has chance probability 26 to the minus eleven per trial against 184,512 trials. Survivors "
        "at any period get the forced key letters read in the standard, KRYPTOS and keyword-mixed alphabets and scored as "
        "English; a vocabulary match is decrypted and submitted. Bounds: complete for this alphabet pool, "
        "periods 1-52, and the three modes."
    ),
    "hypothesis_eli5": (
        "Earlier we ruled out short secret words because two known letters that would share a letter of the "
        "word disagreed. But that reasoning assumed the table was built from the word KRYPTOS or the plain "
        "alphabet. If the table was built from another word, say PALIMPSEST, the same two known letters make "
        "a different demand and might agree. There is also a hint in the carved text that letters 21 apart "
        "were treated alike. So we rebuild the table from every word the puzzle knows, in four standard ways, "
        "and ask again which short lengths the 24 known letters allow."
    ),
    "prediction": (
        "No alphabet pair revives periods 1-26 or 30-52 except by chance at the periods with the fewest "
        "collisions, 23 to 26, where a few survivors appear per period; 30 to 52 are counted only. Period 21 and 42 have "
        "no survivor. No survivor's forced key matches the vocabulary; zero candidates pass."
    ),
    "method": (
        "1. Build the alphabet pool. 2. For each plain alphabet, cipher alphabet and mode, compute the forced "
        "key index at each of the 24 crib positions. 3. For each period 1-52, group the positions by slot and "
        "reject on any disagreement. 4. Count survivors by period, with a shuffled-K4 control. 5. For "
        "survivors, read the forced indices in each keyword-mixed key alphabet, match the fragment against the vocabulary "
        "and K1-K3 windows, score it as English, and decrypt any match."
    ),
    "walkthrough": (
        "1. Build the alphabet from PALIMPSEST: PALIMSETBCDFGHJKNOQRUVWXYZ, and use it for the plaintext; "
        "keep KRYPTOS for the ciphertext. 2. Position 22 is E, index 6; ciphertext F, index 11 in KRYPTOS; "
        "Vigenere gives key index 5. 3. Position 64, which is 42 later, is B, index 8; ciphertext N, index 19; "
        "key index 11. 4. At period 21 or 42 these two positions share a slot, so 5 must equal 11: it does "
        "not, and this alphabet pair is dead at 21 and 42. 5. Try the next pair; eleven such checks apply "
        "at period 21. 6. A pair that passes all eleven would be a real find: read off its forced key letters "
        "and see whether they spell a word."
    ),
}

import random
from kryptos.alphabets import keyword_mixed, columnar_mixed, keyed_columnar_mixed, alternate_vertical_mixed
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY, load_k1, load_k2, load_k3

N = 97
MODES = {"vig": lambda p, c: (c - p) % 26, "beau": lambda p, c: (c + p) % 26, "varbeau": lambda p, c: (p - c) % 26}
DEC = {"vig": lambda c, k: (c - k) % 26, "beau": lambda c, k: (k - c) % 26, "varbeau": lambda c, k: (c + k) % 26}
ENC = {"vig": lambda p, k: (p + k) % 26, "beau": lambda p, k: (k - p) % 26, "varbeau": lambda p, k: (p - k) % 26}
MIX = {"keyword": keyword_mixed, "columnar": columnar_mixed, "keyed_columnar": keyed_columnar_mixed, "alt_vertical": alternate_vertical_mixed}
PERIODS = list(range(1, 53))


def letters(s):
    return "".join(c for c in s if "A" <= c <= "Z")


def encrypt(plaintext, key):
    pa, ca, ka, m, k = key["pa"], key["ca"], key["ka"], key["m"], key["key"]
    return "".join(ca[ENC[m](pa.index(p), ka.index(k[i % len(k)]))] for i, p in enumerate(plaintext))


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


DIVISORS = {d: [k for k in range(1, d + 1) if d % k == 0 and k <= 52] for d in range(1, N + 1)}


def sweep(ct, known, pool, index, time_left):
    """Period p is dead when it divides the distance between two crib positions whose forced
    key indices differ. Survivors are returned per period with their forced slots."""
    crib_pos = sorted(known)
    survivors = {}
    counts = {}
    trials = 0
    for pname, pa in pool.items():
        pidx = index[pname]
        for cname, ca in pool.items():
            cidx = index[cname]
            for m, f in MODES.items():
                trials += 1
                forced = [(pos - 1, f(pidx[known[pos]], cidx[ct[pos - 1]])) for pos in crib_pos]
                dead = set()
                for x in range(24):
                    ix, kx = forced[x]
                    for y in range(x + 1, 24):
                        iy, ky = forced[y]
                        if kx != ky:
                            dead.update(DIVISORS[abs(ix - iy)])
                for P in PERIODS:
                    if P in dead:
                        continue
                    if P <= 26:
                        survivors.setdefault(P, []).append((pname, cname, m, {i % P: k for i, k in forced}))
                    else:
                        counts[P] = counts.get(P, 0) + 1
        if time_left() < 30:
            break
    return survivors, counts, trials


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    vocab = list(ctx.vocabulary)
    pool = pool_of(vocab)
    index = {name: {ch: i for i, ch in enumerate(A)} for name, A in pool.items()}
    texts = [letters(load_k1()["plaintext"]), letters(load_k2()["plaintext_as_carved"]), letters(load_k3()["plaintext"])]
    key_pool = {n: A for n, A in pool.items() if n in ("std", "kry") or n.endswith("/keyword")}
    survivors, counts, trials = sweep(ct, known, pool, index, ctx.time_left)
    by_period = {str(P): (len(survivors[P]) if P in survivors else counts.get(P, 0)) for P in PERIODS}
    # control
    letters_ = list(ct); random.Random(0).shuffle(letters_)
    null_surv, null_counts, _ = sweep("".join(letters_), known, pool, index, ctx.time_left)
    null_by_period = {str(P): (len(null_surv[P]) if P in null_surv else null_counts.get(P, 0)) for P in PERIODS}
    # survivors: match and score
    candidates, best = [], []
    for P, lst in survivors.items():
        wordpool = set(w for w in vocab if len(w) == P)
        for t in texts:
            for i in range(0, len(t) - P + 1):
                wordpool.add(t[i:i + P])
        for pname, cname, m, slots in lst:
            for kname, ka in key_pool.items():
                frag = "".join(ka[slots[s]] if s in slots else "." for s in range(P))
                runs = [r for r in frag.split(".") if len(r) >= 5]
                if runs:
                    qs = sum(len(r) - 3 for r in runs)
                    sc = sum(ctx.english_score(r) * (len(r) - 3) for r in runs) / qs
                    if len(best) < 15 or sc > best[-1][0]:
                        best.append((sc, P, pname, cname, kname, m, frag)); best.sort(reverse=True); best = best[:15]
                for kw in wordpool:
                    if all(ka[slots[s]] == kw[s] for s in slots):
                        key = {"pa": pool[pname], "ca": pool[cname], "ka": ka, "m": m, "key": kw}
                        pt = "".join(pool[pname][DEC[m](index[cname][c], ka.index(kw[i % P]))] for i, c in enumerate(ct))
                        candidates.append({"plaintext": pt, "key": key, "key_bits": 4.7 * P + 12,
                                           "key_description": f"period {P} key {kw}; plain {pname}, cipher {cname}, key alphabet {kname}, {m}"})
    short_live = {P: len(survivors[P]) for P in sorted(survivors)}
    return {
        "candidates": candidates[:50],
        "bounds": {"family": "periodic tableau, alphabets mixed from the vocabulary, periods 1-52", "alphabets": len(pool),
                   "alphabet_pairs_x_modes": trials, "survivors_by_period": by_period,
                   "shuffled_k4_survivors_by_period": null_by_period,
                   "short_periods_with_survivors": {str(P): n for P, n in short_live.items()},
                   "period_21_survivors": len(survivors.get(21, [])), "period_42_survivors": counts.get(42, 0),
                   "best_english_fragments": [{"score": round(sc, 3), "period": P, "plain": a, "cipher": b, "key_alphabet": c, "mode": m, "fragment": fr} for sc, P, a, b, c, m, fr in best],
                   "vocab_matches": len(candidates)},
        "notes": f"{trials} alphabet pairs x modes, periods 1-52. Short periods with survivors: {short_live}. Period 21: {len(survivors.get(21, []))}, period 42: {counts.get(42, 0)}. {len(candidates)} vocabulary matches.",
    }


def worked_example(ctx, key):
    pa = keyword_mixed("PALIMPSEST"); ca = KRY
    lines = [f"plain alphabet PALIMPSEST/keyword {pa}", f"cipher alphabet KRYPTOS {ca}", "", "period 21 collisions: positions 42 apart share a slot", "", "pos  plain  cipher  key index    pos  plain  cipher  key index   agree?"]
    for a, b in [(22, 64), (23, 65), (24, 66), (25, 67), (26, 68), (27, 69)]:
        ka_ = (ca.index(ctx.K4[a - 1]) - pa.index(ctx.KNOWN[a])) % 26
        kb_ = (ca.index(ctx.K4[b - 1]) - pa.index(ctx.KNOWN[b])) % 26
        lines.append(f"{a:>3}    {ctx.KNOWN[a]}      {ctx.K4[a-1]}       {ka_:>2}        {b:>3}    {ctx.KNOWN[b]}      {ctx.K4[b-1]}       {kb_:>2}       {'yes' if ka_ == kb_ else 'no'}")
    return "\n".join(lines)
