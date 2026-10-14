"""Experiment 0010. See program.md for the contract."""

EXPERIMENT = {
    "slug": "forced-key-stretches-mixed-alphabets",
    "title": "The same two forced key stretches, with the tableau's alphabets mixed from the puzzle's own words",
    "family": "1-keyed-periodic",
    "parent": "0009-forced-key-stretches-read-as-english",
    "changed": "The plain, cipher and key alphabets may each be a keyword-mixed alphabet built from any vocabulary word by any of the four Friedman mixings, not only the standard and KRYPTOS alphabets.",
    "hypothesis_expert": (
        "0009 showed that under the standard and KRYPTOS alphabets the key stretches forced by the two "
        "crib runs read as noise. Scheidt taught the 1900-1945 hand systems (knowledge/03-scheidt-said.md), "
        "whose tableaux use keyword-mixed alphabets: a keyword then the rest of the alphabet, or the same "
        "written into a block and read by columns, by keyed columns, or alternately vertically (Friedman's "
        "mixings, kryptos/alphabets.py). K1 and K2 used KRYPTOS; K4 may use another word from the puzzle's "
        "world (C5, C6, C8, C29). Here the plain and cipher alphabets range over standard, KRYPTOS and the "
        "keyword mixing of each vocabulary word, and the key alphabet over all four mixings of each word, "
        "under Vigenere, Beaufort and variant Beaufort. For each triple the 13-letter stretch under "
        "EASTNORTHEAST and the 11-letter stretch under BERLINCLOCK are scored as English against the 0009 "
        "calibration. A key alphabet is a bijection on the stretch, so this is the test 0009 could not "
        "do. Bounds: exact copper, periods 27 and above, every triple of alphabets drawn as stated."
    ),
    "hypothesis_eli5": (
        "The table on the sculpture starts with the word KRYPTOS and then the rest of the alphabet. The "
        "old hand methods the designer taught allowed any word to start the alphabet, and four ways of "
        "shuffling it afterwards. So we repeat the last experiment with every word from the puzzle's "
        "world, PALIMPSEST, ABSCISSA, BERLIN, CLOCK and the rest, as the word that starts the alphabet, "
        "for the message letters, the carved letters and the secret word alike. If some choice makes "
        "the 13 pinned letters of the secret word read like English, that choice is probably the real one."
    ),
    "prediction": (
        "About 3 million stretch pairs are scored, so the best will sit around 4 standard deviations above "
        "noise by chance alone and still below the English mean. No stretch scores above -4.3 per "
        "quadgram. Zero candidates pass."
    ),
    "method": (
        "1. Build the alphabet pools: plain and cipher from standard, KRYPTOS and the keyword mixing of each "
        "vocabulary word; key from all four mixings of each word plus the two basics. 2. For each plain "
        "alphabet, cipher alphabet and mode, compute the forced key index at each crib position of both "
        "runs. 3. For each key alphabet, map the indices to letters and score the two stretches by mean "
        "log10 quadgram probability. 4. Keep the best 20 overall and the best per mode; compare with the "
        "English and noise distributions from 0009."
    ),
    "walkthrough": (
        "1. Write the alphabet starting with PALIMPSEST, dropping repeats: PALIMSETBCDFGHJKNOQRUVWXYZ. "
        "2. Use it for the plaintext; keep the carved KRYPTOS alphabet for the ciphertext. 3. Position 22 "
        "is plaintext E, index 6 in the PALIMPSEST alphabet; ciphertext F, index 11 in KRYPTOS; Vigenere "
        "gives key index 5. 4. Do the same for positions 23 to 34 to get 13 key indices. 5. Now choose a "
        "key alphabet, say ABSCISSA mixed by columns, and read off the letter at each index. 6. Score the "
        "13 letters by how common each run of four is in English. 7. Repeat for every choice of the three "
        "alphabets. 8. A stretch that scores like English, about -4.3 or better, is the signal."
    ),
}

from kryptos.alphabets import (keyword_mixed, columnar_mixed, keyed_columnar_mixed, alternate_vertical_mixed,
                               key_letter_for as lib_key_letter_for)
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

RUNS = [(22, 34), (64, 74)]
MODES = {"vig": lambda p, c: (c - p) % 26, "beau": lambda p, c: (c + p) % 26, "varbeau": lambda p, c: (p - c) % 26}
MIX = {"keyword": keyword_mixed, "columnar": columnar_mixed, "keyed_columnar": keyed_columnar_mixed, "alt_vertical": alternate_vertical_mixed}


def encrypt(plaintext, key):
    pa, ca, ka, m, k = key["pa"], key["ca"], key["ka"], key["m"], key["key"]
    enc = {"vig": lambda p, kk: (p + kk) % 26, "beau": lambda p, kk: (kk - p) % 26, "varbeau": lambda p, kk: (p - kk) % 26}[m]
    return "".join(ca[enc(pa.index(p), ka.index(k[i % len(k)]))] for i, p in enumerate(plaintext))


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    score = ctx.english_score
    vocab = [w for w in ctx.vocabulary if len(set(w)) >= 3]
    basics = {"std": STD, "kry": KRY}
    plain_pool = dict(basics)
    key_pool = dict(basics)
    for w in vocab:
        plain_pool[f"{w}/keyword"] = keyword_mixed(w)
        for mname, fn in MIX.items():
            key_pool[f"{w}/{mname}"] = fn(w)
    # dedupe identical alphabets
    def dedupe(pool):
        seen, out = {}, {}
        for name, a in pool.items():
            if a not in seen:
                seen[a] = name; out[name] = a
        return out
    plain_pool, key_pool = dedupe(plain_pool), dedupe(key_pool)
    # self-check against the library on the basic alphabets
    for m in MODES:
        for pos in (22, 64):
            p, c = known[pos], ct[pos - 1]
            idx = MODES[m](KRY.index(p), STD.index(c))
            assert KRY[idx] == lib_key_letter_for(p, c, "kry", "std", "kry", m)
    cal = {"english_13": (-4.251, 0.466), "english_11": (-4.252, 0.518), "random_13": (-8.292, 0.98), "random_11": (-8.295, 1.08)}
    index = {name: {ch: i for i, ch in enumerate(a)} for name, a in plain_pool.items()}
    crib_letters = [[known[pos] for pos in range(lo, hi + 1)] for lo, hi in RUNS]

    def search(text):
        cipher_letters = [[text[pos - 1] for pos in range(lo, hi + 1)] for lo, hi in RUNS]
        best = []           # (score, stretch, run, pa, ca, ka, mode)
        n = 0
        for pname, pa in plain_pool.items():
            pidx = index[pname]
            for cname, ca in plain_pool.items():
                cidx = index[cname]
                for m, f in MODES.items():
                    seqs = [[f(pidx[p], cidx[c]) for p, c in zip(ps, cs)] for ps, cs in zip(crib_letters, cipher_letters)]
                    for kname, ka in key_pool.items():
                        for r, seq in enumerate(seqs):
                            stretch = "".join(ka[i] for i in seq)
                            sc = score(stretch)
                            n += 1
                            if len(best) < 20 or sc > best[-1][0]:
                                best.append((sc, stretch, f"{RUNS[r][0]}-{RUNS[r][1]}", pname, cname, kname, m))
                                best.sort(reverse=True); best = best[:20]
            if ctx.time_left() < 30:
                break
        return best, n

    best, n = search(ct)
    import random
    nulls = []
    for seed in range(3):
        letters_ = list(ct); random.Random(seed).shuffle(letters_)
        nb, _ = search("".join(letters_))
        nulls.append((round(nb[0][0], 3), nb[0][1]))

    def z(r):
        sc, stretch, run_, pname, cname, kname, m = r
        k = 13 if run_ == "22-34" else 11
        mu_e, sd_e = cal[f"english_{k}"]; mu_r, sd_r = cal[f"random_{k}"]
        return {"score": round(sc, 3), "stretch": stretch, "run": run_, "plain": pname, "cipher": cname, "key": kname, "mode": m,
                "z_vs_random": round((sc - mu_r) / sd_r, 2), "z_vs_english": round((sc - mu_e) / sd_e, 2)}
    return {
        "candidates": [],
        "bounds": {"family": "periodic tableau, period 27+, alphabets mixed from vocabulary; forced key stretches scored as English",
                   "plain_cipher_alphabets": len(plain_pool), "key_alphabets": len(key_pool), "modes": 3,
                   "stretches_scored": n, "calibration_from": "0009",
                   "best_overall": z(best[0]), "top_twenty": [z(r) for r in best],
                   "null_control_best": nulls, "null_control": "same search on three shuffles of the K4 letters; best score and stretch each"},
        "notes": f"Diagnostic, no candidates. {n} stretches scored over {len(plain_pool)}^2 x {len(key_pool)} x 3 alphabet triples.",
    }


def worked_example(ctx, key):
    pa = keyword_mixed("PALIMPSEST"); ca = KRY; ka = columnar_mixed("ABSCISSA")
    lines = [f"plain alphabet  PALIMPSEST/keyword  {pa}", f"cipher alphabet KRYPTOS             {ca}", f"key alphabet    ABSCISSA/columnar   {ka}", "", "pos  plain  cipher  key index  key letter"]
    out = []
    for pos in range(22, 35):
        p, c = ctx.KNOWN[pos], ctx.K4[pos - 1]
        i = (ca.index(c) - pa.index(p)) % 26
        out.append(ka[i])
        lines.append(f"{pos:>3}    {p}      {c}        {i:>2}         {ka[i]}")
    lines.append("")
    lines.append("stretch: " + "".join(out) + f"   score {ctx.english_score(''.join(out)):.2f} per quadgram (English about -4.3 at this length, noise about -8.3)")
    return "\n".join(lines)
