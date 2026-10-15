"""Experiment 0066. See program.md for the contract."""

EXPERIMENT = {
    "slug": "ciphertext-autokey-plus-a-repeating-key",
    "title": "The previous carved letters as a key, plus a repeating secret word on top",
    "family": "1-keyed-periodic",
    "parent": "0065-constructions-that-line-up-doublets-in-sevens",
    "changed": "Experiment 65 found that a cipher feeding on the previous carved letter, combined with a repeating secret word of 7, is the only recipe that lines doublets up in sevens. Experiment 2 killed the plain ciphertext autokey; this adds the repeating secret word on top, at every distance back and every length of word, and tests it exactly against the known letters.",
    "hypothesis_expert": (
        "Family 1 re-entered with a stated reason: 0065 and 0062 point at ciphertext feedback (lag 1 makes "
        "the width-7 doublet column with a period-7 key, lag 21 makes the width-21 repeats), and 0002 tested "
        "ciphertext autokey only without an additional key. Construction: two-component key, ciphertext "
        "autokey at lag L plus a periodic key of period P: T[i] = s*A(c[i-L]) + k[i mod P], where T is the "
        "total key index (C - P for Vigenere, C + P for Beaufort; variant Beaufort is s = -1), A reads the "
        "earlier carved letter in the key alphabet. Because the carved text is fully known, the autokey part "
        "can be subtracted: d[i] = T[i] - s*A(c[i-L]) is a pure periodic key, so the 24 cribs give exact "
        "equations k[i mod P] = d[i] for every crib with i >= L. Sweep: L = 1..96, P = 1..96, plain, cipher "
        "and key alphabets standard or KRYPTOS, Vigenere or Beaufort, s = +1 or -1 (32 classes, 294,912 "
        "cases). A case survives if every slot's forced values agree and at least one check exists; "
        "survivors are tallied by the number of redundant checks and compared with ten shuffled coppers "
        "run through the same sweep. Forced key fragments of survivors are matched against the vocabulary "
        "and K1-K3 windows. Clue entries: C11a ('auto-key', 'interval 7'), C5(b) ('key word/s'), C6(c)."
    ),
    "hypothesis_eli5": (
        "An autokey cipher can feed on the carved letters themselves: each letter is enciphered with the "
        "carved letter a fixed distance back. Experiment 2 showed that alone cannot produce the known "
        "letters. Here a repeating secret word is added on top, of any length, at any distance back. "
        "Because we can see every carved letter, the feeding part can be undone exactly, which leaves an "
        "ordinary repeating secret word that the 24 known letters either fit or do not. Scrambled coppers "
        "run through the same test show how many fits luck alone produces."
    ),
    "prediction": (
        "No case with a period of 26 or less survives with three or more redundant checks under any class, "
        "including lag 1 with period 7 (the doublet mechanism) and lag 21 at every period (the repeat "
        "mechanism). Survivor counts at each number of checks match the ten shuffled coppers within their "
        "range, and no forced fragment matches a word. Zero candidates pass."
    ),
    "method": (
        "1. For every lag, compute d[i] = total key minus the earlier carved letter's value at each known "
        "place past the lag. 2. For every period, group the known places by slot and check that each slot's "
        "values agree. 3. Tally consistent cases by the number of redundant checks. 4. Repeat on ten shuffled "
        "coppers. 5. Match the forced fragments of survivors against words."
    ),
    "walkthrough": (
        "1. Take lag 1 and a 7-letter secret word, with every letter counted along KRYPTOSABCDEFGHIJLMNQUVWXZ "
        "from K = 0. 2. Place 22: known E (11), carved F (12), previous carved W (23): the secret word's "
        "letter is 12 - 11 - 23 = -22, which is 4, T, in slot 0. 3. Place 29, also slot 0: known T (4), "
        "carved R (1), previous carved P (3): 1 - 4 - 3 = -6, which is 20, Q. 4. T and Q disagree, so this "
        "lag and word length are dead under this way of using the table. 5. Places 64 and 71 (slot 0 too) "
        "would force P and J. 6. Repeat for every lag, every word length, and every way of using the table."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY, load_k1, load_k2, load_k3

N = 97
ALPH = {"std": STD, "kry": KRY}


def letters(s):
    return "".join(c for c in s.upper() if "A" <= c <= "Z")


def classes():
    for pa in ALPH:
        for ca in ALPH:
            for ka in ALPH:
                for mode in ("vig", "beau"):
                    for s in (1, -1):
                        yield pa, ca, ka, mode, s


def sweep(ct, known, ctx, deadline, collect=False):
    crib = sorted((pos - 1, p) for pos, p in known.items())
    tally, survivors, cases = {}, [], 0
    for cl in classes():
        pa, ca, ka, mode, s = cl
        PI = {c: i for i, c in enumerate(ALPH[pa])}; CI = {c: i for i, c in enumerate(ALPH[ca])}; KI = {c: i for i, c in enumerate(ALPH[ka])}
        T = {i: ((CI[ct[i]] - PI[p]) if mode == "vig" else (CI[ct[i]] + PI[p])) % 26 for i, p in crib}
        for L in range(1, 97):
            d = [(i, (T[i] - s * KI[ct[i - L]]) % 26) for i, p in crib if i - L >= 0]
            if len(d) < 2:
                continue
            for P in range(1, 97):
                cases += 1
                slot = {}
                ok = True
                for i, v in d:
                    j = i % P
                    if slot.setdefault(j, v) != v:
                        ok = False; break
                if not ok:
                    continue
                checks = len(d) - len(slot)
                if checks < 1:
                    continue
                key = (P <= 26, min(checks, 6))
                tally[key] = tally.get(key, 0) + 1
                if collect and (P <= 26 or checks >= 3):
                    survivors.append({"lag": L, "period": P, "class": "/".join(map(str, cl)), "checks": checks,
                                      "fragment": "".join(ALPH[ka][slot[j]] if j in slot else "." for j in range(P))})
        if ctx.time_left() < deadline:
            break
    return tally, survivors, cases


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    t0 = ctx.time_left()
    tally, surv, cases = sweep(ct, known, ctx, t0 * 0.6, collect=True)
    rng = random.Random(66)
    ctrl = []
    for r in range(10):
        sh = list(ct); rng.shuffle(sh)
        t, _, _ = sweep("".join(sh), known, ctx, 30)
        ctrl.append(t)
        if ctx.time_left() < 40:
            break
    keys = sorted(set(tally) | {k for t in ctrl for k in t})
    table = {f"{'P<=26' if a else 'P>26'}, checks {c}{'+' if c == 6 else ''}": {"k4": tally.get((a, c), 0),
             "controls": [t.get((a, c), 0) for t in ctrl]} for a, c in keys}
    vocab = set(ctx.vocabulary)
    texts = [letters(load_k1()["plaintext"]), letters(load_k2()["plaintext_as_carved"]), letters(load_k3()["plaintext"])]
    matches = []
    for sv in surv:
        for run_ in sv["fragment"].split("."):
            if len(run_) >= 5 and (any(run_ in w or w in run_ for w in vocab if len(w) >= 5) or any(run_ in t for t in texts)):
                matches.append({**sv, "run": run_})
    special = [sv for sv in surv if (sv["lag"] == 1 and sv["period"] == 7) or sv["lag"] == 21]
    return {
        "candidates": [],
        "bounds": {"family": "ciphertext autokey at lag L plus a periodic key of period P", "lags": "1-96", "periods": "1-96",
                   "classes": 32, "cases": cases, "controls": len(ctrl), "survivors_by_checks": table,
                   "survivors_P_le_26_with_3plus_checks": [sv for sv in surv if sv["period"] <= 26 and sv["checks"] >= 3][:40],
                   "lag1_period7_or_lag21_survivors": special[:40], "word_matches": matches[:20]},
        "notes": f"{cases} cases, 32 classes. Survivors (K4 vs controls min-max): " + "; ".join(
            f"{k}: {v['k4']} ({min(v['controls']) if v['controls'] else '-'}-{max(v['controls']) if v['controls'] else '-'})" for k, v in table.items())
            + f". Lag 1 period 7 or lag 21 survivors: {len(special)}. Word matches: {len(matches)}.",
    }


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    I = {c: i for i, c in enumerate(KRY)}
    ct, kn = ctx.K4, ctx.KNOWN
    lines = ["lag 1, period 7, sculpture's alphabet throughout, Vigenere, s = +1", "", "place  known  carved  previous  key letter  slot"]
    for pos in (22, 29, 64, 71):
        k = (I[ct[pos - 1]] - I[kn[pos]] - I[ct[pos - 2]]) % 26
        lines.append(f"{pos:>5}  {kn[pos]:>5}  {ct[pos - 1]:>6}  {ct[pos - 2]:>8}  {KRY[k]:>10}  {(pos - 1) % 7:>4}")
    return "\n".join(lines)
