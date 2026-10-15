"""Experiment 0025. See program.md for the contract."""

EXPERIMENT = {
    "slug": "autokeys-with-mixed-alphabets",
    "title": "Both autokeys again, with the tableau built from the puzzle's own words",
    "family": "1-keyed-periodic",
    "parent": "0012-plaintext-autokey-chained-from-cribs",
    "changed": "0002 and 0012 used the standard and KRYPTOS alphabets only. Here the plain and cipher alphabets are the keyword mixings of every vocabulary word, with the key letters read in the standard, KRYPTOS or the same mixed alphabet.",
    "hypothesis_expert": (
        "Ciphertext autokey, c[i] = E(p[i], c[i-L]), is decided by the cribs alone: at every crib position "
        "past the lag the key letter is a known ciphertext letter, so each (lag, convention) gets up to 24 "
        "exact checks. Plaintext autokey, c[i] = E(p[i], p[i-L]), is decided by the chained closure of 0012. "
        "Both were dead under the standard and KRYPTOS alphabets (0002, 0003, 0012); the NSA's 1992 "
        "'plain-text auto-key' guess (C11a) and Scheidt's keyword alphabets (C5) leave the mixed-alphabet "
        "case open. Alphabet pool: standard, KRYPTOS and the keyword mixing of each vocabulary word (63); "
        "plain and cipher alphabets range over the pool, the key alphabet over standard, KRYPTOS and the "
        "plain alphabet itself; three modes; lags 1-96. Ciphertext autokey: zero mismatches is a survivor. "
        "Plaintext autokey: a consistent closure with 60 or more forced letters is scored as English on its "
        "non-crib runs against ten shuffled controls, and a fully forced text is submitted. Bounds: complete "
        "for this pool and these key-alphabet choices."
    ),
    "hypothesis_eli5": (
        "An autokey cipher uses the message itself, or the scrambled text itself, as the secret word. We "
        "ruled that out yesterday with the sculpture's two alphabets. But the table could have been built "
        "from another word, which changes every sum. So we rebuild the table from each word the puzzle "
        "knows and run both autokey checks again: for the scrambled-text version the 24 known letters "
        "decide at once; for the message version, each known letter reveals another, and the chain either "
        "breaks or fills the whole message."
    ),
    "prediction": (
        "Ciphertext autokey: no alphabet triple, mode and lag passes all its checks; the best passes about "
        "6 of 24. Plaintext autokey: every lag up to 25 breaks under every triple; closures with 60 or more "
        "letters read as noise against the controls. Zero candidates pass."
    ),
    "method": (
        "1. Build the alphabet pool and the key-alphabet choices. 2. Ciphertext autokey: for each triple, "
        "mode and lag, compare the enciphered crib letter with the carved letter at every crib position past "
        "the lag; count mismatches. 3. Plaintext autokey: for each triple, mode and lag, chain forced letters "
        "from the cribs to closure; reject on conflict; record forced-letter count. 4. Score large closures "
        "as English on non-crib runs; repeat on ten shuffles. 5. Submit fully forced texts."
    ),
    "walkthrough": (
        "1. Build the alphabet from ABSCISSA: ABSCIDEFGHJKLMNOPQRTUVWXYZ, and use it for both the message "
        "letters and the carved letters, Vigenere. 2. Ciphertext autokey, lag 10: the key for position 22 is "
        "the carved letter at 12, L. 3. Look up E in the ABSCISSA alphabet, index 5, and L, index 12; add: "
        "17, which is R in that alphabet. The carved letter at 22 is F, so this is a mismatch. 4. Count "
        "mismatches over all known letters past position 10; any mismatch kills this lag for this alphabet. "
        "5. Plaintext autokey, lag 10: the key for position 32 is the message letter at 22, E, which we know, "
        "so position 32's message letter must be A; it is, so no conflict yet; position 42's letter follows "
        "from position 32's, and so on down the chain."
    ),
}

import random
from kryptos.alphabets import keyword_mixed
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
MODES_ENC = {"vig": lambda p, k: (p + k) % 26, "beau": lambda p, k: (k - p) % 26, "varbeau": lambda p, k: (p - k) % 26}
MODES_DEC = {"vig": lambda c, k: (c - k) % 26, "beau": lambda c, k: (k - c) % 26, "varbeau": lambda c, k: (c + k) % 26}
MODES_KEY = {"vig": lambda p, c: (c - p) % 26, "beau": lambda p, c: (c + p) % 26, "varbeau": lambda p, c: (p - c) % 26}


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
    pa, ca, ka, m, L, primer, kind = key["pa"], key["ca"], key["ka"], key["m"], key["lag"], key["primer"], key["kind"]
    f = MODES_ENC[m]
    out = []
    for i, p in enumerate(plaintext):
        if i < L:
            k = primer[i]
        else:
            k = plaintext[i - L] if kind == "plaintext" else out[i - L]
        out.append(ca[f(pa.index(p), ka.index(k))])
    return "".join(out)


def ct_autokey_mismatches(ct, known, L, pa, ca, ka, m, limit):
    f = MODES_ENC[m]
    mism = checks = 0
    for pos, p in known.items():
        i = pos - 1
        if i < L:
            continue
        checks += 1
        if ca[f(pa.index(p), ka.index(ct[i - L]))] != ct[i]:
            mism += 1
            if mism > limit:
                break
    return mism, checks


def closure(ct, known, L, pa, ca, ka, m):
    """Plaintext autokey: propagate forced plaintext letters from the cribs."""
    fk, fd = MODES_KEY[m], MODES_DEC[m]
    pidx, cidx, kidx = {ch: i for i, ch in enumerate(pa)}, {ch: i for i, ch in enumerate(ca)}, {ch: i for i, ch in enumerate(ka)}
    forced = {pos - 1: p for pos, p in known.items()}
    queue = list(forced)
    while queue:
        i = queue.pop()
        p = forced[i]
        if i - L >= 0:
            k = ka[fk(pidx[p], cidx[ct[i]])]        # the plaintext letter at i-L, as a key letter
            j = i - L
            if j in forced:
                if forced[j] != k:
                    return False, forced
            else:
                forced[j] = k; queue.append(j)
        if i + L < N:
            q = pa[fd(cidx[ct[i + L]], kidx[p])]
            j = i + L
            if j in forced:
                if forced[j] != q:
                    return False, forced
            else:
                forced[j] = q; queue.append(j)
    return True, forced


def runs_of(forced, skip):
    out, cur, prev = [], [], None
    for i in sorted(forced):
        if i in skip:
            if len(cur) >= 5: out.append("".join(cur))
            cur = []; prev = i; continue
        if prev is not None and i == prev + 1:
            cur.append(forced[i])
        else:
            if len(cur) >= 5: out.append("".join(cur))
            cur = [forced[i]]
        prev = i
    if len(cur) >= 5: out.append("".join(cur))
    return out


def sweep(ct, known, pool, score, collect):
    crib_idx = {p - 1 for p in known}
    best_ct = (99, None)
    ct_survivors = []
    pt_best = []
    pt_full = []
    dead_lags_all = set(range(1, N))
    trials = 0
    for pname, pa in pool.items():
        for cname, ca in pool.items():
            for kname in ("std", "kry", pname):
                ka = pool[kname] if kname in pool else pa
                for m in MODES_ENC:
                    for L in range(1, N):
                        trials += 1
                        mism, checks = ct_autokey_mismatches(ct, known, L, pa, ca, ka, m, 3)
                        if checks >= 12 and mism < best_ct[0]:
                            best_ct = (mism, (pname, cname, kname, m, L, checks))
                        if mism == 0 and checks >= 12:
                            ct_survivors.append((pname, cname, kname, m, L, checks))
                        ok, forced = closure(ct, known, L, pa, ca, ka, m)
                        if not ok:
                            continue
                        dead_lags_all.discard(L)
                        if len(forced) >= 60:
                            runs = runs_of({i: c for i, c in forced.items() if i not in crib_idx}, set())
                            qs = sum(len(r) - 3 for r in runs)
                            if qs >= 4:
                                sc = sum(score(r) * (len(r) - 3) for r in runs) / qs
                                if len(pt_best) < 10 or sc > pt_best[-1][0]:
                                    pt_best.append((sc, pname, cname, kname, m, L, len(forced), runs[:3])); pt_best.sort(reverse=True); pt_best = pt_best[:10]
                        if collect and len(forced) == N:
                            pt = "".join(forced[i] for i in range(N))
                            fk = MODES_KEY[m]
                            primer = "".join(ka[fk(pa.index(pt[i]), ca.index(ct[i]))] for i in range(L))
                            pt_full.append({"plaintext": pt, "key": {"pa": pa, "ca": ca, "ka": ka, "m": m, "lag": L, "primer": primer, "kind": "plaintext"},
                                            "key_bits": 4.7 * L, "key_description": f"plaintext autokey lag {L} primer {primer}; {pname}/{cname}/{kname} {m}"})
    return trials, best_ct, ct_survivors, pt_best, pt_full, sorted(dead_lags_all)


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    pool = pool_of(list(ctx.vocabulary))
    trials, best_ct, ct_surv, pt_best, pt_full, dead = sweep(ct, known, pool, ctx.english_score, True)
    candidates = []
    for c in ct_surv[:20]:
        pname, cname, kname, m, L, checks = c
        pa, ca = pool[pname], pool[cname]; ka = pool[kname] if kname in pool else pa
        fd = MODES_DEC[m]
        # primer unknown: decrypt positions past the lag only, mark the rest with X
        pt = ["X"] * N
        for i in range(L, N):
            pt[i] = pa[fd(ca.index(ct[i]), ka.index(ct[i - L]))]
        candidates.append({"plaintext": "".join(pt), "key": {"pa": pa, "ca": ca, "ka": ka, "m": m, "lag": L, "primer": "X" * L, "kind": "ciphertext"},
                           "key_bits": 4.7 * L, "key_description": f"ciphertext autokey lag {L}; {pname}/{cname}/{kname} {m}; primer unknown"})
    candidates += pt_full[:30]
    nulls = []
    for seed in range(10):
        letters_ = list(ct); random.Random(seed).shuffle(letters_)
        _, _, _, nb, _, _ = sweep("".join(letters_), known, pool, ctx.english_score, False)
        nulls.append(round(nb[0][0], 3) if nb else None)
    return {
        "candidates": candidates[:50],
        "bounds": {"family": "ciphertext and plaintext autokey with keyword-mixed alphabets", "alphabets": len(pool),
                   "key_alphabet_choices": "standard, KRYPTOS, or the plain alphabet", "modes": 3, "lags": "1-96", "trials": trials,
                   "ciphertext_autokey_best": {"mismatches": best_ct[0], "setting": best_ct[1]}, "ciphertext_autokey_survivors": len(ct_surv),
                   "plaintext_autokey_lags_dead_under_every_triple": dead,
                   "plaintext_autokey_best_closures": [{"score": round(sc, 3), "plain": a, "cipher": b, "key": c, "mode": m, "lag": L, "forced": n, "runs": r} for sc, a, b, c, m, L, n, r in pt_best],
                   "plaintext_autokey_fully_forced": len(pt_full), "shuffled_control_best": nulls},
        "notes": f"{trials} (triple, mode, lag) cases. Ciphertext autokey: best {best_ct[0]} mismatches, {len(ct_surv)} survivors. Plaintext autokey: lags dead under every triple {dead[:30]}{'...' if len(dead) > 30 else ''}; {len(pt_full)} fully forced; best closure {pt_best[0][0] if pt_best else None} vs shuffled {max(x for x in nulls if x is not None) if any(nulls) else None}.",
    }


def worked_example(ctx, key):
    A = keyword_mixed("ABSCISSA")
    lines = [f"alphabet from ABSCISSA: {A}; used for message, carved text and key; Vigenere", "", "ciphertext autokey, lag 10:", "pos  plain  key = carved at pos-10  E+key  carved  match"]
    for pos in (22, 23, 24, 64, 65):
        p = ctx.KNOWN[pos]; k = ctx.K4[pos - 11]; c = A[(A.index(p) + A.index(k)) % 26]
        lines.append(f"{pos:>3}    {p}         {k}                  {c}      {ctx.K4[pos-1]}     {'yes' if c == ctx.K4[pos-1] else 'no'}")
    ok, forced = closure(ctx.K4, ctx.KNOWN, 10, A, A, A, "vig")
    lines.append("")
    lines.append(f"plaintext autokey, lag 10: chain from the cribs {'is consistent' if ok else 'breaks'} after forcing {len(forced)} letters")
    return "\n".join(lines)
