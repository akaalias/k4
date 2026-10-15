"""Experiment 0117. See program.md for the contract."""

EXPERIMENT = {
    "slug": "running-keys-through-all-the-shifts",
    "title": "The sculpture's texts as a running key plus one constant shift of the table, with or without a K3-style move",
    "family": "1-keyed-periodic",
    "parent": "0090-sculpture-running-key-with-a-k3-move",
    "changed": "0017 and 0090 used the sculpture's texts (the K1/K2 matrix among them) as a running key letter for letter. Sanborn was 'surprised that no one had tried recovering the original matrix and running it through all the possible shifts'. Here every key text gets a constant shift of the table, all 26, on top: the known letters must then differ from the key text by one constant, which is tested exactly through difference signatures, with no move and with every move of the type-1 library, before or after the table.",
    "hypothesis_expert": (
        "C2(b): 'shifts' as the 26 row shifts of the tableau, the matrix as the K1/K2 block or another carved text; "
        "C6(a). Model: c_i = E(p_i, k_{o+i} + s) for a key text k, offset o and constant s; E in 12 conventions "
        "(Vigenere, Beaufort, variant; plain and cipher alphabets standard or KRYPTOS) and key letters numbered on the "
        "standard or KRYPTOS alphabet. Because s is free, only the differences between known places matter: the 23 "
        "differences of the forced key must equal the key text's. Key texts as in 0090 (tableau by rows, rows with index, "
        "columns; Morse as carved and reversed; the four ciphertexts; K1-K3 plaintexts; Sanborn's 1989 letter, 1991 "
        "dedication texts and 2025 letter), forward and backward, every cyclic offset; Carter's book in the change-then-move "
        "order only. Moves: the type-1 library (identity included). Change then move: a dictionary of window "
        "signatures; move then change: a pair index on differences, filtered check by check. Ten shuffled coppers."
    ),
    "hypothesis_eli5": (
        "Sanborn once said he was surprised nobody had taken the original matrix and run it through all the possible "
        "shifts. One reading: take one of the sculpture's texts as a long key, and slide the whole table by a fixed "
        "amount, any of 26, before using it. We test every text, every starting point and every shift, with and without "
        "the grid moves of experiments 80 to 83, against the 24 known letters."
    ),
    "prediction": (
        "No text, offset, shift and move fits all 24 known letters; the deepest partial agreement matches the scrambled "
        "coppers'. Zero candidates."
    ),
    "method": (
        "1. Build the key texts (both numberings) and the route library. 2. Change then move: index every window's 23 key "
        "differences at the crib places; for each route and convention, compute the forced differences and look them up "
        "(all 24, and each crib stretch alone). 3. Move then change: for each key text, find the offsets that agree on the "
        "first two moved crib places through a pair index on differences, then filter. 4. Repeat on ten shuffled coppers."
    ),
    "walkthrough": (
        "1. Take the K1/K2 ciphertext block as the key text, from offset 0, and the sculpture's alphabet with Vigenere. "
        "2. At each known place, the key needed is the carved letter minus the known letter; the key text offers its own letter there. "
        "3. With a constant shift s, needed = offered + s at every known place, so needed minus offered must be the same 24 times. "
        "4. Slide the offset through the whole text, both directions, and repeat for every text, rule, and every grid move before or after the table."
    ),
}

import json, random
from pathlib import Path
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY, load_k1, load_k2, load_k3
from kryptos.ciphers import tableau_rows, columnar_transposition_encrypt
from kryptos.alphabets import numeric_order

N = 97
N_CONTROLS = 10
ROOT = Path(__file__).resolve().parent
if not (ROOT / "knowledge").exists():
    ROOT = Path.cwd()
AL = {"std": STD, "kry": KRY}
IDX = {k: {c: i for i, c in enumerate(a)} for k, a in AL.items()}
EXTRA = ["EGYPT", "CAIRO", "LUXOR", "WALL", "NOVEMBER", "MESSAGE", "DELIVER", "DELIVERING", "TRANSMIT"]


def letters(s):
    return "".join(c for c in s.upper() if "A" <= c <= "Z")


def sources():
    site = json.loads((ROOT / "data" / "site_texts.json").read_text())
    rows = tableau_rows(carved=True)
    src = {}
    src["tableau rows"] = "".join(rows)
    src["tableau rows with index column"] = "".join(STD[i] + r for i, r in enumerate(rows))
    width = max(len(r) for r in rows)
    src["tableau columns"] = "".join(r[c] for c in range(width) for r in rows if c < len(r))
    morse = [letters(m) for m in site["morse"]]
    src["morse as carved"] = "".join(morse)
    src["morse reversed order"] = "".join(reversed(morse))
    k1, k2, k3 = load_k1(), load_k2(), load_k3()
    k4 = letters((ROOT / "data" / "k4.txt").read_text())
    src["panel ciphertexts K1-K4"] = letters(k1["ciphertext"]) + letters(k2["ciphertext_as_carved"]) + letters(k3["ciphertext"]) + k4
    src["K1-K3 plaintexts"] = letters(k1["plaintext"]) + letters(k2["plaintext_as_carved"]) + letters(k3["plaintext"])
    t = (ROOT / "knowledge" / "sources" / "sanborn-1989-letter-and-webster-1990-cryptogram.txt").read_text(errors="ignore")
    a = t.index("Dear Agency Employees"); b = t.index("Sincerely, Jim Sanborn") + len("Sincerely, Jim Sanborn")
    c = t.index("Remarks by William H. Webster")
    o = (ROOT / "knowledge" / "sources" / "openletter-2025.txt").read_text(errors="ignore")
    oa = o.index("Dear Kryptos fans"); ob = o.index("Jim Sanborn", o.index("All the best")) + len("Jim Sanborn")
    src["Sanborn 1989 letter"] = letters(t[a:b])
    src["1991 dedication texts"] = letters(t[c:])
    src["2025 open letter"] = letters(o[oa:ob])
    out = {}
    for name, s in src.items():
        out[name + " fwd"] = s
        out[name + " bwd"] = s[::-1]
    carter = letters((ROOT / "knowledge" / "sources" / "carter-1923-tomb-of-tutankhamen-vol1.txt").read_text(errors="ignore"))
    big = {"Carter vol 1 fwd": carter, "Carter vol 1 bwd": carter[::-1]}
    return out, big


def perm_of(fn):
    idx = "".join(chr(0x100 + i) for i in range(N))
    return [ord(ch) - 0x100 for ch in fn(idx)]


def rot_cw(s, w):
    rows = [s[i:i + w] for i in range(0, len(s), w)]
    return "".join(r[c] for c in range(w) for r in reversed(rows) if c < len(r))


def rot_ccw(s, w):
    rows = [s[i:i + w] for i in range(0, len(s), w)]
    return "".join(r[c] for c in reversed(range(w)) for r in rows if c < len(r))


def keyword_sequence(word):
    rank = numeric_order(word)
    return sorted(range(len(rank)), key=lambda c: rank[c])


def full_sequence(word):
    w = [c for c in word.upper() if c.isalpha()]
    return sorted(range(len(w)), key=lambda c: (w[c], c))


def route_fns(vocab):
    for b in range(1, N):
        for a in range(N):
            def f(s, a=a, b=b):
                out = [""] * N
                for i in range(N):
                    out[(a + b * i) % N] = s[i]
                return "".join(out)
            yield f"K3 rule a={a} b={b}", f
    for w in range(2, N):
        yield f"turn cw {w}", (lambda s, w=w: rot_cw(s, w))
        yield f"turn ccw {w}", (lambda s, w=w: rot_ccw(s, w))
        yield f"columnar {w}", (lambda s, o=list(range(w)): columnar_transposition_encrypt(s, o))
        yield f"columnar rtl {w}", (lambda s, o=list(range(w))[::-1]: columnar_transposition_encrypt(s, o))
    for w1 in range(2, N):
        for w2 in range(2, N):
            yield f"two turns cw {w1},{w2}", (lambda s, a=w1, b=w2: rot_cw(rot_cw(s, a), b))
    words = sorted({w for w in vocab if 2 <= len(w) <= 30} | set(EXTRA))
    for word in words:
        for how, seq in (("repeats dropped", keyword_sequence(word)), ("full word", full_sequence(word))):
            if len(seq) >= 2:
                yield f"keyword {word} ({how})", (lambda s, o=list(seq): columnar_transposition_encrypt(s, o))


def route_library(vocab):
    """Distinct 'where' maps (where[i] = place in the moved text of letter i), forward and inverse."""
    seen, lib = set(), []
    for name, f in route_fns(vocab):
        sigma = perm_of(f)                    # moved[j] = orig[sigma[j]]
        fwd = [0] * N
        for j, i in enumerate(sigma):
            fwd[i] = j
        for tag, w in ((name, fwd), (name + " inverse", sigma)):
            t = tuple(w)
            if t not in seen:
                seen.add(t); lib.append((tag, t))
    return lib


def enc(mode, p, k):
    return {"vig": (p + k) % 26, "beau": (k - p) % 26, "varb": (p - k) % 26}[mode]


def key_for(mode, p, c):
    """k with enc(mode, p, k) = c."""
    return {"vig": (c - p) % 26, "beau": (c + p) % 26, "varb": (p - c) % 26}[mode]


def dec(mode, c, k):
    return {"vig": (c - k) % 26, "beau": (k - c) % 26, "varb": (c + k) % 26}[mode]


CONVS = [(m, pa, ca) for m in ("vig", "beau", "varb") for pa in ("std", "kry") for ca in ("std", "kry")]


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    places = sorted(known)
    pidx = [p - 1 for p in places]
    lib = route_library(ctx.vocabulary)
    srcs, big = sources()
    rng = random.Random(117)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    # numeric key texts in both numberings
    numA = {f"{n} [{ka}]": [IDX[ka][c] for c in s] for n, s in {**srcs, **big}.items() for ka in ("std", "kry")}
    numB = {f"{n} [{ka}]": [IDX[ka][c] for c in s] for n, s in srcs.items() for ka in ("std", "kry")}
    # ---- change then move
    ix24, ix13, ix11 = {}, {}, {}
    for name, y in numA.items():
        L = len(y); yy = y + y[:N]
        for o in range(L):
            v = [yy[o + j] for j in pidx]
            d24 = tuple((x - v[0]) % 26 for x in v[1:])
            ix24.setdefault(hash(d24), []).append((name, o))
            ix13.setdefault(hash(d24[:12]), 0); ix13[hash(d24[:12])] += 1
            k11 = hash(tuple((x - v[13]) % 26 for x in v[14:]))
            ix11.setdefault(k11, 0); ix11[k11] += 1
    A_full = [[] for _ in texts]; A13 = [0] * len(texts); A11 = [0] * len(texts)
    for tag, where in lib:
        for conv in CONVS:
            mode, pa, ca = conv
            P, C = IDX[pa], IDX[ca]
            for t, txt in enumerate(texts):
                T = [key_for(mode, P[known[p]], C[txt[where[p - 1]]]) for p in places]
                d24 = tuple((x - T[0]) % 26 for x in T[1:])
                h = hash(d24)
                if h in ix24:
                    A_full[t].append((tag, conv, T[0], ix24[h][:3]))
                if hash(d24[:12]) in ix13:
                    A13[t] += 1
                if hash(tuple((x - T[13]) % 26 for x in T[14:])) in ix11:
                    A11[t] += 1
    # ---- move then change
    families = [(name, y, len(y)) for name, y in numB.items()]
    pair_cache = {}

    def pairs(fi, g):
        key = (fi, g)
        if key not in pair_cache:
            _, y, L = families[fi]
            d = {}
            for u in range(L):
                d.setdefault((y[(u + g) % L] - y[u]) % 26, []).append(u)
            pair_cache[key] = d
        return pair_cache[key]
    B_full = []
    B_depth = [None] * len(texts)
    done = 0
    for t, txt in enumerate(texts):
        if t > 0 and ctx.time_left() < 120:
            break
        best = 0
        for tag, where in lib:
            q = [where[j] for j in pidx]
            order = sorted(range(24), key=lambda e: q[e])
            for conv in CONVS:
                mode, pa, ca = conv
                P, C = IDX[pa], IDX[ca]
                T = [key_for(mode, P[known[places[e]]], C[txt[q[e]]]) for e in range(24)]
                e0, e1 = order[0], order[1]
                for fi, (name, y, L) in enumerate(families):
                    g = (q[e1] - q[e0]) % L
                    cand = pairs(fi, g).get((T[e1] - T[e0]) % 26, ())
                    depth = 2 if cand else 1
                    if cand:
                        base = T[e0]
                        for k in range(2, 24):
                            e = order[k]; rr = q[e] - q[e0]; want = T[e]
                            cand = [u for u in cand if (y[(u + rr) % L] - y[u] - want + base) % 26 == 0]
                            if not cand:
                                break
                            depth += 1
                    if depth > best:
                        best = depth
                    if t == 0 and depth == 24:
                        for u in cand:
                            B_full.append((tag, conv, name, (u - q[e0]) % L, (T[e0] - y[u]) % 26))
        B_depth[t] = best
        done += 1
    bounds = {"family": "running key from the sculpture's texts plus one constant tableau shift, with or without a type-1 move",
              "routes_distinct": len(lib), "conventions": len(CONVS),
              "key_texts_change_then_move": {k: len(v) for k, v in numA.items()},
              "change_then_move": {"k4_full": len(A_full[0]), "controls_full": [len(x) for x in A_full[1:]],
                                   "k4_stretch13": A13[0], "controls_stretch13": A13[1:],
                                   "k4_stretch11": A11[0], "controls_stretch11": A11[1:],
                                   "k4_full_hits": [(a, "/".join(b), c, d) for a, b, c, d in A_full[0][:10]]},
              "move_then_change": {"key_texts": len(families), "k4_full": len(B_full), "k4_best_depth": B_depth[0],
                                   "controls_best_depth": B_depth[1:done], "controls_completed": done - 1,
                                   "k4_full_hits": [(a, "/".join(b), c, d, e) for a, b, c, d, e in B_full[:10]]},
              "controls": f"{N_CONTROLS} shuffled coppers (seed 117), identical search"}
    notes = (f"{len(lib):,} routes x {len(CONVS)} conventions. Change then move ({len(numA)} numbered key texts incl. Carter): full "
             f"K4 {len(A_full[0])}, controls {[len(x) for x in A_full[1:]]}; EASTNORTHEAST stretch K4 {A13[0]} (controls {A13[1:]}); "
             f"BERLINCLOCK stretch K4 {A11[0]} (controls {A11[1:]}). Move then change ({len(families)} key texts): full {len(B_full)}, "
             f"deepest K4 {B_depth[0]}, controls {B_depth[1:done]} ({done - 1} completed).")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    srcs, _ = sources()
    s = srcs["panel ciphertexts K1-K4 fwd"]
    I = IDX["kry"]
    lines = ["key text: the four ciphertexts as one panel (the K1/K2 block first), offset 0; sculpture's alphabet, Vigenere", "",
             "place  known  carved  needed  key text  offered  needed - offered"]
    for q in (22, 23, 24, 25, 64, 65, 74):
        need = (I[ct[q - 1]] - I[known[q]]) % 26
        off = I[s[q - 1]]
        lines.append(f"{q:>5}  {known[q]:>5}  {ct[q - 1]:>6}  {need:>6}  {s[q - 1]:>8}  {off:>7}  {(need - off) % 26:>15}")
    lines += ["", "a constant shift would make the last column the same at all 24 places"]
    return "\n".join(lines)
