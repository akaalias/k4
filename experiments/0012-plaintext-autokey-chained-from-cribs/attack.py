"""Experiment 0012. See program.md for the contract."""

EXPERIMENT = {
    "slug": "plaintext-autokey-chained-from-cribs",
    "title": "Plaintext autokey, chained: the 24 known letters force the rest, lag by lag",
    "family": "1-keyed-periodic",
    "parent": "0003-plaintext-autokey-all-lags",
    "changed": "0003 only checked the cribs against each other. Here each known letter is also used as the key for the letter one lag later, and as the ciphertext's partner one lag earlier, and the forced letters are chained until nothing new follows. For small lags that fixes the whole text.",
    "hypothesis_expert": (
        "Plaintext autokey (the NSA's 1992 guess, C11a; a Scheidt-era hand system, C5): c[i] = E(p[i], p[i-L]) "
        "for i >= L after a primer of length L. A crib letter p[i] forces p[i-L] through c[i] and forces "
        "p[i+L] through c[i+L]; each forced letter forces two more. The closure from the 24 cribs covers "
        "every residue class modulo L that a crib position touches, so for L <= 13 the whole text is forced, "
        "for L up to about 24 most of it, and for larger L two or three stretches. 0003 found lags 1-11 and "
        "30-52 inconsistent inside the cribs; lags 12-29 and 53-96 were undecided. Here, under each of the "
        "24 conventions and each lag 1-96, we propagate to closure, reject on any conflict, and for a fully "
        "forced text derive the primer and submit the candidate. Partially forced texts are scored as "
        "English on their forced runs and compared with the same procedure on shuffled K4 letters. "
        "Bounds: complete for plaintext autokey with a primer of length L, any L 1-96, under these conventions."
    ),
    "hypothesis_eli5": (
        "In an autokey cipher the message is its own secret word: each letter is enciphered using the "
        "letter some fixed distance before it. That makes the 24 known letters very powerful. Each one "
        "was used to encipher a letter further on, so that letter can be worked out; and each one was "
        "itself enciphered by a letter further back, so that one can be worked out too. Repeating this "
        "spreads outward until, for short distances, the whole message is known. We try every distance "
        "and every way of using the table, and read what comes out."
    ),
    "prediction": (
        "Every lag from 1 to 25 either conflicts somewhere in the chain or yields a fully forced text that "
        "is not English, scoring below -6 per quadgram against -3.6 for English. Lags above 25 leave "
        "stretches that score no better than the shuffled control. No candidate passes the English "
        "standard; a fully forced text may pass the four gates by construction and will then stand as a "
        "champion with a loss of 3 to 4, which is a gibberish champion, not a solution."
    ),
    "method": (
        "1. For each convention and lag L, start with the 24 cribs as forced letters. 2. For each forced "
        "letter at i: if i >= L, force p[i-L] as the key that maps p[i] to c[i]; if i + L < 97, force "
        "p[i+L] by decrypting c[i+L] with key p[i]. 3. Repeat until nothing new appears; any conflict kills "
        "the pair. 4. If all 97 letters are forced, derive the primer k[i] for i < L and submit the text. "
        "5. Otherwise score the forced runs of four or more letters as English. 6. Run the same procedure "
        "on ten shuffles of K4 for a control."
    ),
    "walkthrough": (
        "1. Take lag 13 and the sculpture's alphabet with Vigenere. 2. Position 22 is E and its ciphertext "
        "is F; under the table, the key that turns E into F is R, so position 9 is R. 3. Position 35 was "
        "enciphered with key E, the letter at 22; the ciphertext at 35 is S, and S decrypted with key E is "
        "the letter at 35. 4. Now 9 and 35 are known, so 48 and 61 follow, and so on, up and down by 13 "
        "until the chain leaves the text. 5. Do the same from every one of the 24 known letters. 6. Where "
        "two chains meet, the letters must agree, or lag 13 is dead under this convention. 7. If every "
        "position fills, read the text aloud. 8. The first 13 letters were enciphered with the primer; "
        "the key letter that maps each of them to its ciphertext is the primer, which should be a word."
    ),
}

import random
from kryptos.alphabets import conventions, key_letter_for, decrypt_letter, encrypt_letter

N = 97


def encrypt(plaintext, key):
    pa, ca, ka, m, L, primer = key["pa"], key["ca"], key["ka"], key["m"], key["lag"], key["primer"]
    out = []
    for i, p in enumerate(plaintext):
        k = primer[i] if i < L else plaintext[i - L]
        out.append(encrypt_letter(p, k, pa, ca, ka, m))
    return "".join(out)


def closure(ct, known, L, conv):
    """Propagate forced plaintext letters from the cribs. Returns (ok, forced dict 0-indexed)."""
    pa, ca, ka, m = conv
    forced = {pos - 1: p for pos, p in known.items()}
    queue = list(forced)
    while queue:
        i = queue.pop()
        p = forced[i]
        if i - L >= 0:
            k = key_letter_for(p, ct[i], pa, ca, ka, m)
            j = i - L
            if j in forced:
                if forced[j] != k:
                    return False, forced
            else:
                forced[j] = k; queue.append(j)
        if i + L < N:
            q = decrypt_letter(ct[i + L], p, pa, ca, ka, m)
            j = i + L
            if j in forced:
                if forced[j] != q:
                    return False, forced
            else:
                forced[j] = q; queue.append(j)
    return True, forced


def runs_of(forced):
    """Maximal runs of consecutive forced positions, as strings."""
    out, cur, prev = [], [], None
    for i in sorted(forced):
        if prev is not None and i == prev + 1:
            cur.append(forced[i])
        else:
            if cur: out.append("".join(cur))
            cur = [forced[i]]
        prev = i
    if cur: out.append("".join(cur))
    return [r for r in out if len(r) >= 4]


def score_runs(runs, score):
    qs = sum(len(r) - 3 for r in runs)
    if qs == 0:
        return None
    return sum(score(r) * (len(r) - 3) for r in runs) / qs


def sweep(ct, known, convs, score):
    rows = []
    for L in range(1, N):
        for conv in convs:
            ok, forced = closure(ct, known, L, conv)
            if not ok:
                continue
            runs = runs_of(forced)
            rows.append((L, conv, forced, runs, score_runs(runs, score)))
    return rows


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    score = ctx.english_score
    convs = list(conventions())
    rows = sweep(ct, known, convs, score)
    candidates = []
    consistent_by_lag = {}
    for L, conv, forced, runs, sc in rows:
        consistent_by_lag[L] = consistent_by_lag.get(L, 0) + 1
        if len(forced) == N:
            pa, ca, ka, m = conv
            pt = "".join(forced[i] for i in range(N))
            primer = "".join(key_letter_for(pt[i], ct[i], pa, ca, ka, m) for i in range(L))
            candidates.append({"plaintext": pt, "key": {"pa": pa, "ca": ca, "ka": ka, "m": m, "lag": L, "primer": primer},
                               "key_bits": 4.7 * L, "key_description": f"autokey lag {L} primer {primer}; {pa}/{ca}/{ka} {m}",
                               "notes": f"fully forced from the cribs; English {sc:.2f}"})
    candidates.sort(key=lambda c: -float(c["notes"].split()[-1]))
    scored = [(sc, L, "/".join(conv), len(forced), runs) for L, conv, forced, runs, sc in rows if sc is not None]
    scored.sort(reverse=True)
    rng_rows = []
    for seed in range(10):
        letters_ = list(ct); random.Random(seed).shuffle(letters_)
        rs = sweep("".join(letters_), known, convs, score)
        best = max((sc for *_, sc in rs if sc is not None), default=None)
        rng_rows.append(None if best is None else round(best, 3))
    dead_lags = [L for L in range(1, N) if L not in consistent_by_lag]
    return {
        "candidates": candidates[:50],
        "bounds": {"family": "plaintext autokey with primer, chained closure from cribs", "conventions": 24, "lags": "1-96",
                   "lags_dead_all_conventions": dead_lags,
                   "consistent_pairs_by_lag": {str(L): n for L, n in sorted(consistent_by_lag.items())},
                   "fully_forced_candidates": len(candidates),
                   "best_english_of_forced_runs": [{"score": round(sc, 3), "lag": L, "convention": c, "forced_letters": n, "runs": r[:4]} for sc, L, c, n, r in scored[:8]],
                   "shuffled_control_best_per_seed": rng_rows},
        "notes": f"{len(rows)} consistent (lag, convention) pairs; {len(candidates)} fully forced texts submitted. A fully forced text passes the crib gate by construction; only its English score matters.",
    }


def worked_example(ctx, key):
    conv = ("kry", "kry", "kry", "vig")
    ok, forced = closure(ctx.K4, ctx.KNOWN, 13, conv)
    lines = ["lag 13, KRYPTOS alphabet throughout, Vigenere: chaining from the cribs", ""]
    lines.append(f"consistent: {ok}; letters forced: {len(forced)} of 97")
    text = "".join(forced.get(i, ".") for i in range(97))
    lines.append(text)
    lines.append("")
    lines.append("position 22 (E, cipher F) forces position 9 = " + key_letter_for("E", ctx.K4[21], *conv) + "; key E at 22 decrypts cipher " + ctx.K4[34] + " at 35 to " + decrypt_letter(ctx.K4[34], "E", *conv))
    return "\n".join(lines)
