"""Experiment 0016. See program.md for the contract."""

EXPERIMENT = {
    "slug": "routes-then-tableau-forced-key-english",
    "title": "Every route from 0006 and 0008, then the tableau: does any route make the forced key read as English?",
    "family": "6-transposition-then-tableau",
    "parent": "0008-k3-formula-all-shifts-then-tableau",
    "changed": "0006 and 0008 matched forced key fragments against a word list. Here the forced key under every route and live period up to 40 is scored as English, with a shuffled-letter control, as 0009 did for the plain tableau.",
    "hypothesis_expert": (
        "Under K4 = tableau(T(P)) with a periodic key of period p, each route T sends the 24 cribs to 24 "
        "intermediate positions whose forced key letters fill 24 slots of the key, most of them distinct "
        "when p is 27 or more. If the key is a word or phrase (C5, C6), the filled slots read as English "
        "in slot order. Routes: the 2,905 columnar routes of 0006 and the 21,025 K3-rule and double-rotation "
        "routes of 0008, under all 24 conventions; for each live period up to 40 the forced slots are "
        "collected, runs of five or more consecutive filled slots, at least four quadgrams in all, are scored by quadgram log-probability, "
        "and the best (route, convention, period) is compared with the same procedure on two shuffles of "
        "the K4 letters. Chance expectation: the best of about a million scores sits where the shuffled "
        "best sits. Bounds: complete for these route sets, conventions and periods, for readable keys."
    ),
    "hypothesis_eli5": (
        "Earlier we asked whether a grid scramble followed by the table could use a short secret word; "
        "none could. Now we ask a softer question: for each scramble, the 24 known letters pin down 24 "
        "letters of the secret word, scattered through it. Do those pinned letters ever spell something "
        "that looks like English? We check every scramble we have, and we run the same check on the "
        "carved letters shuffled at random, so we know what a meaningless best looks like."
    ),
    "prediction": (
        "The best forced key over all routes, conventions and periods scores within 0.2 of the best from "
        "shuffled K4 letters, and the top entries show no recognisable word of five or more letters. Zero "
        "candidates pass."
    ),
    "method": (
        "1. Build the route sets of 0006 and 0008. 2. For each route, send each crib position to its "
        "intermediate position. 3. For each convention, force the key letter there. 4. For each period "
        "from 2 to 40 that the forced letters allow, place them in slots and score runs of four or more "
        "consecutive filled slots. 5. Keep the best twenty overall. 6. Repeat on two shuffles of K4."
    ),
    "walkthrough": (
        "1. Take the route: write in rows of 7, read down the columns. 2. The known letters at 22 to 34 "
        "land at 4, 18, 32, 46, 60, 74, 88, 5, 19, 33, 47, 61, 75; those at 64 to 74 land elsewhere. "
        "3. Under the sculpture's alphabet with Vigenere, each landing spot has a forced key letter. "
        "4. Choose period 28: slot is the landing spot minus one, mod 28. 5. Write the 28 slots in a row "
        "and fill in the forced letters; 24 of 28 are filled. 6. Read the filled stretches. 7. Score them "
        "as English; compare with what random letters would give."
    ),
}

import random
from kryptos.alphabets import conventions, key_letter_for, encrypt_letter, numeric_order
from kryptos.ciphers import columnar_transposition_encrypt, columnar_transposition_decrypt

N = 97
MAXP = 40
DIVISORS = {d: [k for k in range(1, d + 1) if d % k == 0] for d in range(1, N + 1)}


def perm_of(fn):
    idx = [chr(0x100 + i) for i in range(N)]
    return [ord(ch) - 0x100 for ch in fn("".join(idx))]


def plain_order(w, rtl=False):
    o = list(range(w))
    return o[::-1] if rtl else o


def affine_fwd(s, a, b):
    n = len(s); out = [""] * n
    for i in range(n):
        out[(a + b * i) % n] = s[i]
    return "".join(out)


def affine_inv(s, a, b):
    n = len(s)
    return "".join(s[(a + b * i) % n] for i in range(n))


def rotate(s, w):
    rows = [s[i:i + w] for i in range(0, len(s), w)]
    return "".join(r[col] for col in range(w) for r in reversed(rows) if col < len(r))


def route_set(vocab):
    routes = []
    for w in range(2, N):
        for rtl in (False, True):
            order = plain_order(w, rtl)
            routes.append((f"columnar w={w}{' rtl' if rtl else ''} fwd", lambda s, o=order: columnar_transposition_encrypt(s, o)))
            routes.append((f"columnar w={w}{' rtl' if rtl else ''} inv", lambda s, o=order: columnar_transposition_decrypt(s, o)))
    for word in vocab:
        if 2 <= len(word) <= 40:
            order = numeric_order(word)
            routes.append((f"keyed columnar {word} fwd", lambda s, o=order: columnar_transposition_encrypt(s, o)))
            routes.append((f"keyed columnar {word} inv", lambda s, o=order: columnar_transposition_decrypt(s, o)))
    for w1 in range(2, 51):
        for w2 in range(2, 51):
            routes.append((f"double columnar w={w1} then w={w2}", lambda s, a=plain_order(w1), b=plain_order(w2): columnar_transposition_encrypt(columnar_transposition_encrypt(s, a), b)))
            routes.append((f"double rotation w={w1} then w={w2}", lambda s, a=w1, b=w2: rotate(rotate(s, a), b)))
    for b in range(1, N):
        for a in range(N):
            routes.append((f"K3 rule a={a} b={b} fwd", lambda s, a=a, b=b: affine_fwd(s, a, b)))
            routes.append((f"K3 rule a={a} b={b} inv", lambda s, a=a, b=b: affine_inv(s, a, b)))
    return routes


def encrypt(plaintext, key):
    raise NotImplementedError("diagnostic experiment: no full key is implied, so no candidate is submitted")


def runs_in_slots(slots, P):
    """Runs of consecutive filled slots, cyclic, as strings, length >= 5."""
    filled = [slots.get(s) for s in range(P)]
    if all(filled):
        start = 0
    else:
        start = next(i for i in range(P) if filled[i] is None)
    out, cur = [], []
    for k in range(1, P + 1):
        ch = filled[(start + k) % P]
        if ch is None:
            if len(cur) >= 5: out.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    if len(cur) >= 5: out.append("".join(cur))
    return out


def search(ct, known, routes, convs, score, time_left):
    crib_pos = sorted(known)
    best = []
    n = 0
    for name, fn in routes:
        if time_left() < 30:
            break
        sigma = perm_of(fn)
        where = {sigma[j]: j for j in range(N)}
        inter = [where[p - 1] for p in crib_pos]
        for conv in convs:
            pa, ca, ka, m = conv
            forced = [key_letter_for(known[p], ct[j], pa, ca, ka, m) for p, j in zip(crib_pos, inter)]
            dead = set()
            for a in range(24):
                for b in range(a + 1, 24):
                    if forced[a] != forced[b]:
                        dead.update(DIVISORS[abs(inter[a] - inter[b])])
            for P in range(2, MAXP + 1):
                if P in dead:
                    continue
                slots = {j % P: l for j, l in zip(inter, forced)}
                runs = runs_in_slots(slots, P)
                qs = sum(len(r) - 3 for r in runs)
                if qs < 4:
                    continue
                sc = sum(score(r) * (len(r) - 3) for r in runs) / qs
                n += 1
                if len(best) < 20 or sc > best[-1][0]:
                    best.append((sc, name, "/".join(conv), P, runs))
                    best.sort(reverse=True); best = best[:20]
    return best, n


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    routes = route_set(list(ctx.vocabulary))
    convs = list(conventions())
    best, n = search(ct, known, routes, convs, ctx.english_score, ctx.time_left)
    nulls = []
    for seed in range(2):
        letters_ = list(ct); random.Random(seed).shuffle(letters_)
        nb, _ = search("".join(letters_), known, routes, convs, ctx.english_score, ctx.time_left)
        nulls.append({"best": round(nb[0][0], 3), "route": nb[0][1], "period": nb[0][3], "runs": nb[0][4]} if nb else None)
    return {
        "candidates": [],
        "bounds": {"family": "transposition then periodic tableau; forced key scored as English", "routes": len(routes),
                   "conventions": 24, "periods": f"2-{MAXP}, live only", "scores": n,
                   "best": [{"score": round(sc, 3), "route": nm, "convention": cv, "period": P, "runs": rs} for sc, nm, cv, P, rs in best],
                   "shuffled_control": nulls},
        "notes": f"Diagnostic, no candidates. {n} (route, convention, period) keys scored; best {best[0][0]:.3f} vs shuffled {[x['best'] for x in nulls if x]}.",
    }


def worked_example(ctx, key):
    from kryptos.ciphers import columnar_transposition_encrypt as enc
    sigma = perm_of(lambda s: enc(s, list(range(7))))
    where = {sigma[j]: j for j in range(N)}
    lines = ["route: columnar width 7, read columns left to right; convention kry/kry/kry Vigenere; period 28", ""]
    slots = {}
    for pos in sorted(ctx.KNOWN):
        j = where[pos - 1]
        slots[j % 28] = key_letter_for(ctx.KNOWN[pos], ctx.K4[j], "kry", "kry", "kry", "vig")
    lines.append("slot: " + " ".join(f"{s:>2}" for s in range(28)))
    lines.append("key:  " + " ".join(f" {slots.get(s, '.')}" for s in range(28)))
    runs = runs_in_slots(slots, 28)
    lines.append("")
    lines.append("runs scored: " + ", ".join(f"{r} ({ctx.english_score(r):.2f})" for r in runs))
    return "\n".join(lines)
