"""Experiment 0090. See program.md for the contract."""

EXPERIMENT = {
    "slug": "sculpture-running-key-with-a-k3-move",
    "title": "A running key concealed at the sculpture, joined to a K3-style move before or after it",
    "family": "6-matrix-transposition-then-tableau",
    "parent": "0017-running-key-from-the-sculpture-itself",
    "changed": "0017, 0004, 0021 and 0078 tested running keys from the sculpture's texts, K1-K3, Carter's book and Sanborn's letters with no move. Here each of those keys is joined to every move of the type-1 route library (K3's counting rule, one or two quarter turns, plain and true-keyword column shuffles, 27,000-odd distinct routes), with the move either before the table or after it. A running key leaves no free letter, so both orders are exact tests.",
    "hypothesis_expert": (
        "Types 1 and 3 of directions.md crossed. Scheidt: 'the keys were concealed at the sculpture' (C6(a)), K4 is 'more "
        "than one stage'; Sanborn: 'double matrixes and triple matrixes... then went back to this table' (C1); earlier "
        "text holds instructions for later text (C7(a)). Key sources, each forward and backward at every cyclic offset: "
        "the carved tableau by rows, by rows with the index column and by columns; the Morse as carved and in reverse "
        "order; the four ciphertexts as one panel (0017); the K1-K3 plaintexts (0004); Sanborn's 1989 letter, the 1991 "
        "dedication texts and the 2025 open letter (0078); Carter's book (0021, change-then-move only). Moves: K3's rule "
        "i -> a + b i mod 97 for every a, b; one quarter turn at widths 2-96 either way; two clockwise turns at every pair "
        "of widths; plain columnar left-to-right or right-to-left; true-keyword columnar (issue #26) from the puzzle's "
        "words; each forward and inverse, deduplicated. 12 conventions (Vigenere, Beaufort, variant Beaufort; key and text "
        "numbered on standard or KRYPTOS). Change then move: the forced key at the 24 crib places must equal the source at "
        "those places, a dictionary lookup. Move then change: the key places are the moved crib places; offsets are "
        "filtered check by check. Exact, all 24 checks; the deepest partial match is compared with ten shuffled coppers."
    ),
    "hypothesis_eli5": (
        "A running key is a long text used as the secret, one letter of it per letter of the message. The sculpture "
        "carries several such texts: the table, the Morse messages, the solved parts. Experiment 17 tried them on K4 "
        "directly. Here the letters are also moved the way K3's were, by turning a grid or reading columns, either "
        "before or after the table is used. Because a running key has no free letters, each combination either "
        "explains all 24 known letters or it does not."
    ),
    "prediction": (
        "No combination explains all 24 known letters in either order. Change then move: no source matches either "
        "whole crib stretch (13 or 11 letters). Move then change: the deepest partial match is 7-8 checks, inside the "
        "scrambled-copper range. Zero candidates."
    ),
    "method": (
        "1. Build the key texts and the deduplicated route library. "
        "2. Change then move: for each route and convention, undo the move at the 24 crib places, compute the key "
        "letters forced there, and look them up in an index of every source window with the crib spacing (whole set, "
        "and each crib stretch alone). "
        "3. Move then change: the forced key letters sit at the moved crib places; for each source keep the offsets "
        "that agree at the first moved place, then the second, and so on, and record how deep any offset gets. "
        "4. Repeat both on ten shuffled coppers. 5. Decrypt and return any full match."
    ),
    "walkthrough": (
        "1. Pick a move, say a clockwise quarter turn of a grid 8 letters wide, and a key text, say the Morse as carved. "
        "2. Change then move: the letter at place 22 of the message ends up at some place j of the copper; read the carved letter there. "
        "3. Find the key letter that turns E into that carved letter on the sculpture's table. "
        "4. The key text, started at offset o, must have that letter at its place o + 22. Do this for all 24 known places. "
        "5. Move then change: first move the message, so E of place 22 lands at place j; the key letter must sit at place o + j and turn E into the carved letter at j. "
        "6. Slide o over the whole key text and repeat for every move, every key text, both directions and 12 table rules."
    ),
}

import json, random, re
from pathlib import Path
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY, load_k1, load_k2, load_k3
from kryptos.ciphers import tableau_rows, columnar_transposition_encrypt
from kryptos.alphabets import numeric_order

N = 97
N_CONTROLS = 10
ROOT = Path(__file__).resolve().parent
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


CONVS = [(m, ka, ta) for m in ("vig", "beau", "varb") for ka in ("std", "kry") for ta in ("std", "kry")]


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    places = sorted(known)
    pidx = [p - 1 for p in places]
    run13 = [i for i, p in enumerate(places) if p <= 34]
    run11 = [i for i, p in enumerate(places) if p >= 64]
    srcs, big = sources()
    lib = route_library(ctx.vocabulary)
    rng = random.Random(90)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))

    # ---- change then move: key at crib places p (fixed spacing); index every source window
    allsrc = {**srcs, **big}
    full_ix, ix13, ix11 = {}, {}, {}
    for name, s in allsrc.items():
        L = len(s)
        ss = s + s[:N]
        for o in range(L):
            w = "".join(ss[o + j] for j in pidx)
            full_ix.setdefault(w, []).append((name, o))
            ix13.setdefault(w[:13], []).append((name, o))
            ix11.setdefault(w[13:], []).append((name, o))
    A_full, A13, A11 = [[] for _ in texts], [0] * len(texts), [0] * len(texts)
    A_hits13 = []
    for tag, where in lib:
        for conv in CONVS:
            mode, ka, ta = conv
            for t, txt in enumerate(texts):
                d = "".join(AL[ka][key_for(mode, IDX[ta][known[p]], IDX[ta][txt[where[p - 1]]])] for p in places)
                if d in full_ix:
                    A_full[t].append((tag, conv, full_ix[d][:3]))
                if d[:13] in ix13:
                    A13[t] += 1
                    if t == 0:
                        A_hits13.append({"route": tag, "conv": "/".join(conv), "stretch": "EASTNORTHEAST", "at": ix13[d[:13]][:3]})
                if d[13:] in ix11:
                    A11[t] += 1
                    if t == 0:
                        A_hits13.append({"route": tag, "conv": "/".join(conv), "stretch": "BERLINCLOCK", "at": ix11[d[13:]][:3]})

    # ---- move then change: key at moved places where[p]; filter offsets check by check
    names = list(srcs)
    starts, cat = [], ""
    for name in names:
        starts.append(len(cat)); cat += srcs[name]
    L = len(cat)
    pair_ix = {}                                   # (gap, letter at o, letter at o + gap) -> offsets o
    for g in range(1, N):
        for o in range(L - g):
            pair_ix.setdefault((g, cat[o], cat[o + g]), []).append(o)
    import bisect

    def locate(o):
        k = bisect.bisect_right(starts, o) - 1
        return names[k], o - starts[k]
    B_depth = [0] * len(texts)
    B_depth_hist = [dict() for _ in texts]
    B_full, B_top = [], []
    n_b = 0
    for tag, where in lib:
        q = [where[j] for j in pidx]
        order = sorted(range(24), key=lambda e: q[e])
        for conv in CONVS:
            mode, ka, ta = conv
            kal, ik, it = AL[ka], IDX[ta], IDX[ta]
            for t, txt in enumerate(texts):
                dq = [(q[e], kal[key_for(mode, it[known[places[e]]], it[txt[q[e]]])]) for e in order]
                (q0, c0), (q1, c1) = dq[0], dq[1]
                cand = [o - q0 for o in pair_ix.get((q1 - q0, c0, c1), ()) if o >= q0]
                depth = 2 if cand else 1
                if cand:
                    for qq, cc in dq[2:]:
                        cand = [o for o in cand if o + qq < L and cat[o + qq] == cc]
                        if not cand:
                            break
                        depth += 1
                if t == 0:
                    n_b += 1
                    if depth == 24:
                        for o in cand:
                            B_full.append((tag, conv) + locate(o))
                    if depth >= 7:
                        B_top.append({"route": tag, "conv": "/".join(conv), "depth": depth})
                B_depth[t] = max(B_depth[t], depth)
                B_depth_hist[t][depth] = B_depth_hist[t].get(depth, 0) + 1
        if ctx.time_left() < 60:
            break
    B_top.sort(key=lambda r: -r["depth"])

    cands = []
    for tag, conv, hits in A_full[0]:
        name, o = hits[0]
        where = dict(lib)[tag]
        mode, ka, ta = conv
        s = allsrc[name]; ss = s + s[:N]
        mid = [AL[ta][dec(mode, IDX[ta][ct[where[i]]], IDX[ka][ss[o + i]])] for i in range(N)]
        cands.append({"plaintext": "".join(mid), "key": f"change then move: {name} offset {o}, {tag}, {'/'.join(conv)}"})
    for tag, conv, name, o in B_full:
        where = dict(lib)[tag]
        mode, ka, ta = conv
        s = srcs[name]
        if o + N > len(s):
            continue                                  # window runs into the next text: not a real key
        mid = [AL[ta][dec(mode, IDX[ta][ct[j]], IDX[ka][s[o + j]])] for j in range(N)]
        cands.append({"plaintext": "".join(mid[where[i]] for i in range(N)),
                      "key": f"move then change: {name} offset {o}, {tag}, {'/'.join(conv)}"})
    bounds = {
        "routes_distinct": len(lib), "conventions": len(CONVS),
        "sources": {k: len(v) for k, v in allsrc.items()},
        "change_then_move": {"k4_full_matches": len(A_full[0]), "controls_full": [len(x) for x in A_full[1:]],
                             "k4_stretch13_matches": A13[0], "controls_stretch13": A13[1:],
                             "k4_stretch11_matches": A11[0], "controls_stretch11": A11[1:],
                             "k4_stretch_hits": A_hits13[:20]},
        "move_then_change": {"sources": "all but Carter", "k4_full": len(B_full), "k4_best_depth": B_depth[0],
                             "controls_best_depth": B_depth[1:], "k4_depth_histogram": dict(sorted(B_depth_hist[0].items())),
                             "k4_top": B_top[:15], "route_convention_pairs_on_k4": n_b, "key_letters_searched": L},
        "controls": f"{N_CONTROLS} shuffled coppers (seed 90), identical search",
    }
    notes = (f"{len(lib):,} distinct routes x {len(CONVS)} conventions. Change then move ({len(allsrc)} key texts incl. Carter): "
             f"full matches K4 {len(A_full[0])}, controls {[len(x) for x in A_full[1:]]}; EASTNORTHEAST stretch {A13[0]} "
             f"(controls {A13[1:]}), BERLINCLOCK stretch {A11[0]} (controls {A11[1:]}). Move then change ({len(srcs)} key texts): "
             f"full {len(B_full)}, deepest K4 {B_depth[0]}, controls {B_depth[1:]}.")
    return {"candidates": cands, "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    srcs, _ = sources()
    s = srcs["morse as carved fwd"]
    f = lambda x: rot_cw(x, 8)
    sigma = perm_of(f)
    where = [0] * N
    for j, i in enumerate(sigma):
        where[i] = j
    I = IDX["kry"]
    lines = ["key text: the Morse as carved, offset 0: " + s[:40] + "...",
             "move: one clockwise quarter turn of a grid 8 wide; table: sculpture's alphabet, Vigenere", "",
             "change then move", "place  known  moved to  carved there  key needed  key text at place"]
    for p in (22, 23, 24, 25, 64):
        j = where[p - 1]
        need = KRY[(I[ct[j]] - I[known[p]]) % 26]
        lines.append(f"{p:>5}  {known[p]:>5}  {j + 1:>8}  {ct[j]:>12}  {need:>10}  {s[p - 1]:>16}")
    lines += ["", "move then change", "place  known  moved to  carved there  key needed  key text at moved place"]
    for p in (22, 23, 24, 25, 64):
        j = where[p - 1]
        need = KRY[(I[ct[j]] - I[known[p]]) % 26]
        lines.append(f"{p:>5}  {known[p]:>5}  {j + 1:>8}  {ct[j]:>12}  {need:>10}  {s[j]:>22}")
    return "\n".join(lines)
