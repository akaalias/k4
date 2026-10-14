"""Experiment 0019. See program.md for the contract."""

EXPERIMENT = {
    "slug": "substitution-then-route-crib-images-one-to-one",
    "title": "Substitution first, a route last: do the 24 crib images stay one letter to one letter under any route?",
    "family": "9-substitution-then-transposition",
    "parent": "0018-construction-simulator-fingerprint",
    "changed": "New family, opened by 0018's finding that only substitution followed by transposition reproduces K4's width-21 repeats. The cribs now constrain the ciphertext letters the route sends them to, not the letters at 22-34 and 64-74.",
    "hypothesis_expert": (
        "Zodiac 340 was a homophonic substitution followed by a transposition, and its width-19 repeats were "
        "the trace (knowledge/04-structure.md). K4's eleven width-21 repeats have p about 0.005 under every "
        "substitution-last generator and p near 1 under transposition of English (0018). Against: Sanborn's "
        "secondhand 'one-to-one mapping' of NYPVTT to BERLIN (knowledge/02-sanborn-said.md, 2011 and 2013 "
        "dinners), which says the letters at 64-69 are BERLIN's own images; this family contradicts that "
        "reading and is tested because the statistic is the stronger evidence. Model: each plaintext letter "
        "goes to one of its symbols (monoalphabetic, or homophonic over the same 26 symbols), then a route T "
        "permutes positions. The image of crib position i is ct[T(i)]. Constraint: a ciphertext letter has "
        "one plaintext source, so two crib positions with different plaintext letters must have different "
        "images; under the stricter monoalphabetic reading, equal plaintext letters must also have equal "
        "images. Routes: the 23,930 of 0016 plus the identity. For each route both conditions are checked; "
        "survivors are counted against the same test on shuffled K4. A monoalphabetic survivor gets a "
        "hill-climb over the unknown letters and a candidate. Bounds: complete for this route set."
    ),
    "hypothesis_eli5": (
        "Suppose each letter of the message was first swapped for another letter, and only then were the "
        "letters shuffled into a new order by a grid. The 24 letters we know are then scattered somewhere "
        "in the carved text, and each grid tells us where. One rule must hold: one carved letter cannot "
        "stand for two different message letters. We check that rule for every grid we have, using the 24 "
        "known letters, and count the grids that pass. If none pass, this whole way of building the cipher "
        "is out, however the swapping was done."
    ),
    "prediction": (
        "Under the homophonic condition, fewer than one route in a hundred survives, about the same rate as "
        "on shuffled K4. Under the monoalphabetic condition no route survives. No candidate passes."
    ),
    "method": (
        "1. Build the route set. 2. For each route, find the ciphertext image of each crib position. "
        "3. Homophonic condition: no ciphertext letter is the image of two different plaintext letters. "
        "4. Monoalphabetic condition: in addition, equal plaintext letters have equal images. 5. Count "
        "survivors of each; repeat on five shuffles of K4. 6. For monoalphabetic survivors, hill-climb the "
        "unknown mappings by English score and submit the best text."
    ),
    "walkthrough": (
        "1. Take the route: write in rows of 7 and read down the columns. 2. The message letter at "
        "position 22, the E of EAST, is written at row 4, column 1, and read out 4th: so the carved letter "
        "at 4, R, is the swapped E. 3. Position 31, the other E, lands at 32: the carved K. 4. Under a plain "
        "swap E must always become the same letter, so R and K already conflict: this route is dead for a "
        "plain swap. 5. Under a swap with spare letters, E may have two symbols, so R and K is allowed, but "
        "R must then never be the image of another letter. 6. Position 66, the R of BERLIN, lands at 38: "
        "the carved T; no conflict. 7. Go through all 24; one clash kills the route."
    ),
}

import random
from kryptos.alphabets import numeric_order
from kryptos.ciphers import columnar_transposition_encrypt, columnar_transposition_decrypt

N = 97


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
    routes = [("identity", lambda s: s)]
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


ROUTE_FN = {}


def encrypt(plaintext, key):
    if not ROUTE_FN:
        from kryptos.facts import load_vocabulary
        for name, fn in route_set(list(load_vocabulary())):
            ROUTE_FN[name] = fn
    sub = key["substitution"]      # plaintext letter -> ciphertext letter
    mid = "".join(sub[p] for p in plaintext)
    return ROUTE_FN[key["route"]](mid)


def check(ct, known, where):
    """Returns (homophonic_ok, mono_ok, images dict plain->set of cipher letters)."""
    src = {}      # cipher letter -> plaintext letter
    img = {}      # plaintext letter -> set of cipher letters
    homo = True
    for pos, p in known.items():
        c = ct[where[pos - 1]]
        if c in src and src[c] != p:
            homo = False
        src[c] = p
        img.setdefault(p, set()).add(c)
    mono = homo and all(len(v) == 1 for v in img.values())
    return homo, mono, img


def hill_climb(ct, where, known, score, rng, iters=4000):
    """Complete a monoalphabetic key from the crib images; climb the rest by English score."""
    inv = {}   # cipher -> plain
    for pos, p in known.items():
        inv[ct[where[pos - 1]]] = p
    free_c = [c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if c not in inv]
    free_p = [p for p in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if p not in inv.values()]
    rng.shuffle(free_p)
    assign = dict(zip(free_c, free_p))

    def decrypt(assign):
        full = {**inv, **assign}
        mid = "".join(full[c] for c in ct)
        return "".join(mid[where[i]] for i in range(N))

    best = decrypt(assign); bs = score(best)
    for _ in range(iters):
        if len(free_c) < 2:
            break
        a, b = rng.sample(free_c, 2)
        assign[a], assign[b] = assign[b], assign[a]
        pt = decrypt(assign); s = score(pt)
        if s >= bs:
            best, bs = pt, s
        else:
            assign[a], assign[b] = assign[b], assign[a]
    return best, bs, {**inv, **assign}


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    routes = route_set(list(ctx.vocabulary))
    for name, fn in routes:
        ROUTE_FN[name] = fn
    wheres = []
    for name, fn in routes:
        sigma = perm_of(fn)                      # out[j] = in[sigma[j]]
        where = {sigma[j]: j for j in range(N)}  # input index -> output index
        wheres.append((name, where))

    def sweep(text):
        homo, mono = [], []
        for name, where in wheres:
            h, m, _ = check(text, known, where)
            if h: homo.append(name)
            if m: mono.append(name)
        return homo, mono

    homo, mono = sweep(ct)
    nulls = []
    for seed in range(5):
        letters_ = list(ct); random.Random(seed).shuffle(letters_)
        h, m = sweep("".join(letters_))
        nulls.append({"homophonic": len(h), "monoalphabetic": len(m)})
    candidates = []
    rng = random.Random(7)
    wmap = dict(wheres)
    for name in mono[:20]:
        pt, sc, full = hill_climb(ct, wmap[name], known, ctx.english_score, rng)
        inv_sub = {p: c for c, p in full.items()}
        candidates.append({"plaintext": pt, "key": {"route": name, "substitution": inv_sub}, "key_bits": 88,
                           "key_description": f"monoalphabetic then {name}; English {sc:.2f}"})
    return {
        "candidates": candidates[:50],
        "bounds": {"family": "substitution (mono or homophonic over 26 symbols) then transposition", "routes": len(routes),
                   "homophonic_survivors": len(homo), "homophonic_survivor_routes": homo[:40],
                   "monoalphabetic_survivors": len(mono), "monoalphabetic_survivor_routes": mono[:40],
                   "shuffled_k4_survivors": nulls},
        "notes": f"{len(routes)} routes: {len(homo)} pass the homophonic condition, {len(mono)} the monoalphabetic one; shuffled K4 gives {[n['homophonic'] for n in nulls]} and {[n['monoalphabetic'] for n in nulls]}.",
    }


def worked_example(ctx, key):
    sigma = perm_of(lambda s: columnar_transposition_encrypt(s, list(range(7))))
    where = {sigma[j]: j for j in range(N)}
    h, m, img = check(ctx.K4, ctx.KNOWN, where)
    lines = ["route: columnar width 7 read down the columns; images of the known letters", ""]
    for p in sorted(img):
        lines.append(f"plain {p}: carved images {' '.join(sorted(img[p]))}")
    src = {}
    clashes = []
    for pos, p in ctx.KNOWN.items():
        c = ctx.K4[where[pos - 1]]
        if c in src and src[c] != p: clashes.append(f"{c} from {src[c]} and {p}")
        src[c] = p
    lines.append("")
    lines.append(f"homophonic condition: {'passes' if h else 'fails'}; clashes: {', '.join(clashes) or 'none'}")
    lines.append(f"monoalphabetic condition: {'passes' if m else 'fails'}")
    return "\n".join(lines)
