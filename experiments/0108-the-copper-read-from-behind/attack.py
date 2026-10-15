"""Experiment 0108. See program.md for the contract."""

EXPERIMENT = {
    "slug": "the-copper-read-from-behind",
    "title": "K4 read from the back of the screen, each carved line right to left, with a repeating key or an autokey",
    "family": "4-visual-spatial",
    "parent": "0089-the-screen-folded-onto-itself",
    "changed": "0023 tested K4 reversed as a whole. Seen from behind the screen, the letters keep their line order but each carved line reads right to left: R K B O, then line 12 backwards, line 13 backwards, line 14 backwards. That order, and the other two mirror readings of the carved block (lines bottom to top, each forwards; and both, the full reversal), are tested with a repeating key of length 1-26 and with ciphertext and plaintext autokey at every lag, the reading before or after the table.",
    "hypothesis_expert": (
        "Family 4 open item 'mirrored readings beyond reversal' (families.md). The CIA: the tableau 'is intentionally "
        "flipped so it can only be read from the back of the sculpture'; the letters are cut through (01-facts.md); "
        "Scheidt: 'mirrors and obfuscation' (C13). On the plate K4 fills columns 28-31 of line 11 and lines 12-14 (31 "
        "letters each). Routes: (1) each line reversed, order kept (the view from behind); (2) line order reversed, each "
        "line forwards; (3) both (= the full reversal of 0023, kept as a check). Keys, with the route either before the "
        "table (the message written, read from behind, then enciphered) or after it: periodic key 1-26 in 8 tableau "
        "classes (slot agreement); ciphertext autokey at lags 1-96 (each known letter a direct check); plaintext autokey "
        "at lags 1-96 (propagated from the known letters to closure); autokey settings count only with 3+ checks. Ten shuffled coppers."
    ),
    "hypothesis_eli5": (
        "The letters of Kryptos are cut right through the copper, so the text can be read from behind, where every "
        "line runs right to left. The CIA says the table of alphabets was flipped on purpose so that it reads properly "
        "only from the back. So perhaps K4 should be read from the back too. We read its four carved lines that way, "
        "and in the two other mirror orders, and test the usual short secret words and self-feeding keys against the "
        "24 known letters."
    ),
    "prediction": (
        "No reading and key fits: periodic keys dead below period 20, no autokey lag passes all checks, counts inside "
        "the coppers' range. Zero candidates."
    ),
    "method": (
        "1. Lay K4 on its carved lines and build the three mirror orders. 2. For each order, both placements and each "
        "class, test periodic keys 1-26 by slot agreement. 3. Ciphertext autokey: each known letter must equal the "
        "carved letter minus the carved letter lag places earlier, in the right order. 4. Plaintext autokey: propagate "
        "known letters along the lag to closure and stop at a contradiction. 5. Repeat on ten shuffled coppers."
    ),
    "walkthrough": (
        "1. Line 11 ends OBKR; from behind it reads RKBO. Line 12 is UOXOGHULBSOLIFBBWFLRVQQPRNGKSSO; from behind, OSSKGNRPQQVRLFWBBFILOSBLUHGOXOU. "
        "2. Join them, line by line: RKBO + line 12 backwards + line 13 backwards + line 14 backwards. "
        "3. The F at place 22 of the carved text now sits at place 4 + (31 - 18 + 1) = 18. "
        "4. With a secret word of length p on the new order, the key letter at 18 is slot 18 mod p; it must turn E into F. "
        "5. Repeat for every key length, table rule, autokey lag and mirror order."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
PMAX = 26
ALPH = {"std": STD, "kry": KRY}
N_CONTROLS = 10


def lines_of(seq):
    return [seq[:4], seq[4:35], seq[35:66], seq[66:97]]


def orders():
    idx = list(range(N))
    L = lines_of(idx)
    out = {"lines reversed (from behind)": [i for l in L for i in reversed(l)],
           "line order reversed": [i for l in reversed(L) for i in l],
           "both (full reversal)": idx[::-1]}
    return out


def slot_pairs(slots):
    last, prs = {}, []
    for e, s in enumerate(slots):
        if s in last:
            prs.append((last[s], e))
        last[s] = e
    return prs


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    places = sorted(known)
    pidx = [p - 1 for p in places]
    rng = random.Random(108)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    T = len(texts)
    classes = [(pa, ca, beau) for pa in ALPH for ca in ALPH for beau in (False, True)]
    O = orders()
    res = {}
    for oname, seq in O.items():
        at = {i: seq.index(i) for i in range(N)}          # message place i is read at reading place at[i]
        for placement in ("read then table", "table then read"):
            # Both reduce to one text X and the places Q of the known letters in it:
            # read then table: the table runs along the copper as carved, the known letters sit at at[i];
            # table then read: undo the reading, X_i = carved letter at at[i], the known letters sit at i.
            if placement == "read then table":
                Xs = texts; Q = [at[i] for i in pidx]
            else:
                Xs = ["".join(txt[at[i]] for i in range(N)) for txt in texts]; Q = list(pidx)
            live = [[0] * (PMAX + 1) for _ in range(T)]
            ct_auto = [0] * T
            pt_auto = [0] * T
            k4_low = []
            pairs = {p: slot_pairs([j % p for j in Q]) for p in range(1, PMAX + 1)}
            for pa, ca, beau in classes:
                PI = {c: i for i, c in enumerate(ALPH[pa])}; CI = {c: i for i, c in enumerate(ALPH[ca])}
                want = [PI[known[q]] for q in places]
                for t in range(T):
                    C = [CI[x] for x in Xs[t]]
                    f = [(C[j] + want[e]) % 26 if beau else (C[j] - want[e]) % 26 for e, j in enumerate(Q)]
                    first = None
                    for p in range(1, PMAX + 1):
                        if all(f[x] == f[y] for x, y in pairs[p]):
                            live[t][p] += 1
                            if first is None:
                                first = p
                    if t == 0 and first is not None and first < 20:
                        k4_low.append({"class": f"{pa}/{ca}/{'beau' if beau else 'vig-var'}", "period": first})
                    # ciphertext autokey along X: key for place j is X_{j-lag}; vig p = c - k, beau p = k - c
                    for lag in range(1, N):
                        ok = True; chk = 0
                        for e, j in enumerate(Q):
                            if j - lag < 0:
                                continue
                            chk += 1
                            got = (C[j] - C[j - lag]) % 26 if not beau else (C[j - lag] - C[j]) % 26
                            if got != want[e]:
                                ok = False; break
                        if ok and chk >= 3:
                            ct_auto[t] += 1
                    # plaintext autokey along X: c_j = p_j + p_{j-lag} (vig) or p_{j-lag} - p_j (beau); propagate
                    for lag in range(1, N):
                        pv = [None] * N
                        for e, j in enumerate(Q):
                            pv[j] = want[e]
                        stack = list(Q); ok = True; chk = 0
                        while stack and ok:
                            j = stack.pop()
                            nb = j + lag                     # p_j is the key of place j + lag
                            if nb < N:
                                v = (C[nb] - pv[j]) % 26 if not beau else (pv[j] - C[nb]) % 26
                                if pv[nb] is None:
                                    pv[nb] = v; stack.append(nb)
                                elif pv[nb] != v:
                                    ok = False; break
                                else:
                                    chk += 1
                            nb = j - lag                     # p_{j-lag} is the key of place j
                            if nb >= 0:
                                v = (C[j] - pv[j]) % 26 if not beau else (pv[j] + C[j]) % 26
                                if pv[nb] is None:
                                    pv[nb] = v; stack.append(nb)
                                elif pv[nb] != v:
                                    ok = False; break
                                else:
                                    chk += 1
                        chk = len(Q) - len({j % lag for j in Q})      # each chain mod lag with k known letters gives k - 1 checks
                        if ok and chk >= 3:
                            pt_auto[t] += 1
            res[f"{oname}, {placement}"] = {
                "k4_live_by_period": live[0][1:],
                "controls_live_min": [min(live[t][p] for t in range(1, T)) for p in range(1, PMAX + 1)],
                "controls_live_max": [max(live[t][p] for t in range(1, T)) for p in range(1, PMAX + 1)],
                "k4_smallest_period_rows": k4_low[:8],
                "ct_autokey_k4": ct_auto[0], "ct_autokey_controls": ct_auto[1:],
                "pt_autokey_k4": pt_auto[0], "pt_autokey_controls": pt_auto[1:]}
    smallest = {k: next((i + 1 for i, v in enumerate(r["k4_live_by_period"]) if v), None) for k, r in res.items()}
    bounds = {"family": "mirror readings of K4's carved lines with periodic keys and autokeys", "orders": list(O),
              "placements": ["read then table", "table then read"], "periods": [1, PMAX], "classes": 8, "autokey_lags": [1, 96],
              "results": res, "k4_smallest_live_period": smallest,
              "controls": f"{N_CONTROLS} shuffled coppers (seed 108), identical tests"}
    notes = ("Smallest live period on K4: " + "; ".join(f"{k}: {v}" for k, v in smallest.items())
             + ". Autokey survivors with 3+ checks (lag, class) K4 / controls max: "
             + "; ".join(f"{k}: CT {r['ct_autokey_k4']}/{max(r['ct_autokey_controls'])}, PT {r['pt_autokey_k4']}/{max(r['pt_autokey_controls'])}" for k, r in res.items()) + ".")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    seq = orders()["lines reversed (from behind)"]
    back = "".join(ct[i] for i in seq)
    lines = ["K4 on its carved lines and as read from behind:", ""]
    for a, b in zip(lines_of(ct), lines_of(back)):
        lines.append(f"  {a:<31}   {b}")
    lines += ["", "where the known letters sit in the reading from behind:"]
    lines.append("  " + " ".join(f"{q}->{seq.index(q - 1) + 1}" for q in (22, 23, 24, 25, 64, 74)))
    return "\n".join(lines)
