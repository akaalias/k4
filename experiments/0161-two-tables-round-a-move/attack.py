"""Experiment 0161 (F6.7). See program.md for the contract."""

EXPERIMENT = {
    "slug": "two-tables-round-a-move",
    "title": "F6.7: change, move, change with the two keyed stages on different tables (standard then KRYPTOS, or the reverse), key lengths 2-14 each, solved exactly",
    "family": "6-transposition-then-tableau",
    "parent": "0080-key-on-both-sides-of-the-move",
    "changed": (
        "F6.7 (pivot audit, issue #55, D5). 0080 tested a repeating key, a move, then a second repeating key, both on the "
        "same table. Here the two keyed stages use different tables: the standard alphabet first and the KRYPTOS "
        "alphabet second, or the reverse. With different tables the two keys no longer add, but each known letter still "
        "links one slot of the first key to one slot of the second by a one-to-one relation, so every connected group of "
        "slots has at most 26 consistent assignments: solved exactly. Moves: 0160's library (844 distinct: the four column "
        "readings at every width, K3's rule at every multiplier, forwards and inverted); key lengths 2-14 each; both "
        "orders of tables; each stage added or Beaufort-subtracted. Ten scrambled coppers."
    ),
    "hypothesis_expert": (
        "C1(a)/(c), C20(a) ('layer two'), C5(b) ('key word/s': two words), C27(c) (Sanborn's 'slightly different' table: "
        "the two halves of the work use the two alphabets). Model: y_i = A^-1(A(p_i) + s1 k1[i mod m]); carved c_{M(i)} = "
        "B^-1(B(y_i) + s2 k2[M(i) mod n]) with (A, B) = (standard, KRYPTOS) or (KRYPTOS, standard), s1, s2 in {+1, -1}, m, n "
        "2-14. Each known letter gives k2[M(i) mod n] = s2 (B(c) - B(A^-1(A(p) + s1 k1[i mod m]))), a bijection between the "
        "two slot values; consistency decided by propagation over each component (26 trials per component). Checks = "
        "links - slots + components. Statistic fixed before the run: consistent settings with at least five checks on K4 "
        "against the coppers' range (0080's threshold), and the same count per check level."
    ),
    "hypothesis_eli5": (
        "Two secret words, one used on the plain alphabet's table and the other on the KRYPTOS table, with the letters "
        "moved in a grid between them. Because the tables differ, the two words cannot simply be added together, but "
        "each known letter still ties one letter of the first word to one letter of the second. Following those ties "
        "decides exactly whether any pair of words of lengths 2 to 14 fits, for each grid move, on the carved text and on "
        "scrambled copies."
    ),
    "prediction": "No setting with five or more checks fits K4; counts at each check level inside the coppers' range. Zero candidates.",
    "method": (
        "1. Build the 844 moves. "
        "2. For each text, move, table order, signs and key lengths m, n: the links (slot of k1, slot of k2) at the 24 known letters. "
        "3. Propagate each component from each of 26 values; consistent if one value closes every link. "
        "4. Count consistent settings by checks; compare K4 with the coppers."
    ),
    "walkthrough": (
        "1. Encipher with a first word of length 5 on the plain-alphabet table. "
        "2. Write the result in rows of 9 and read down the columns. "
        "3. Encipher again with a second word of length 7 on the KRYPTOS table: the carved text. "
        "4. A known letter E at place 22 sits under first-word letter 22 mod 5 and, after the move, under second-word letter (its new place) mod 7. "
        "5. Guess the first-word letter: the E becomes a definite middle letter, and the carved letter then fixes the second-word letter. "
        "6. Follow every such tie; a contradiction for all 26 guesses rules the setting out."
    ),
}

import random
import time
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
N_CONTROLS = 10
READINGS = ("cw", "ccw", "col", "colr")
LENS = range(2, 15)


def inverse(m):
    inv = [0] * len(m)
    for i, j in enumerate(m):
        inv[j] = i
    return inv


def stage(tokens, w, r):
    rows = [tokens[i:i + w] for i in range(0, len(tokens), w)]
    cols = range(w) if r in ("cw", "col") else range(w - 1, -1, -1)
    up = r in ("cw", "colr")
    out = []
    for c in cols:
        rr = reversed(rows) if up else rows
        out.extend(row[c] for row in rr if c < len(row))
    return out


def where(seq):
    wh = [0] * len(seq)
    for j, i in enumerate(seq):
        wh[i] = j
    return wh


def library():
    lib_ = []
    for w in range(2, N):
        for r in READINGS:
            lib_.append((f"{r}{w}", where(stage(list(range(N)), w, r))))
    for b in range(2, N):
        lib_.append((f"k3x{b}", [(b * i) % N for i in range(N)]))
    out, seen = [], set()
    for name, m in lib_:
        for d, mm in (("", m), ("inv", inverse(m))):
            k = bytes(mm)
            if k not in seen:
                seen.add(k); out.append((name + d, mm))
    return out




def link_tables(A, B, s1, s2):
    """F[p][c][v] = forced stage-2 value w; G[p][c][w] = stage-1 value v (letters as standard indices)."""
    Ai = {ch: i for i, ch in enumerate(A)}; Bi = {ch: i for i, ch in enumerate(B)}
    F = [[[0] * 26 for _ in range(26)] for _ in range(26)]
    G = [[[0] * 26 for _ in range(26)] for _ in range(26)]
    for p in range(26):
        for c in range(26):
            for v in range(26):
                y = A[(Ai[STD[p]] + s1 * v) % 26]
                w = (s2 * (Bi[STD[c]] - Bi[y])) % 26
                F[p][c][v] = w; G[p][c][w] = v
    return F, G


def decide(links, F, G):
    """links: (slot1, slot2, p, c). Returns checks if consistent, else -1."""
    adj = {}
    for e, (a, b, p, c) in enumerate(links):
        adj.setdefault((0, a), []).append(((1, b), e))
        adj.setdefault((1, b), []).append(((0, a), e))
    seen = set()
    comps = 0
    for root in adj:
        if root in seen:
            continue
        comps += 1
        ok_any = False
        for v0 in range(26):
            val = {root: v0}
            stack = [root]
            ok = True
            while stack and ok:
                u = stack.pop()
                for v, e in adj[u]:
                    a, b, p, c = links[e]
                    need = F[p][c][val[u]] if u[0] == 0 else G[p][c][val[u]]
                    got = val.get(v)
                    if got is None:
                        val[v] = need; stack.append(v)
                    elif got != need:
                        ok = False; break
            if ok:
                ok_any = True
                seen.update(val)
                break
        if not ok_any:
            return -1
    return len(links) - len(adj) + comps


def _work(args):
    moves, texts, known_list, tables = args
    T = len(texts)
    kp = [q - 1 for q, _ in known_list]
    pl = [STD.index(a) for _, a in known_list]
    counts = [[0] * 25 for _ in range(T)]      # by checks (0-24)
    top = []
    for name, m in moves:
        land = [m[i] for i in kp]
        for t, txt in enumerate(texts):
            cl = [STD.index(txt[j]) for j in land]
            for tname, F, G in tables:
                for mm in LENS:
                    s1 = [i % mm for i in kp]
                    for nn in LENS:
                        links = [(s1[e], land[e] % nn, pl[e], cl[e]) for e in range(24)]
                        ch = decide(links, F, G)
                        if ch >= 0:
                            counts[t][ch] += 1
                            if t == 0 and ch >= 4:
                                top.append({"move": name, "tables": tname, "m": mm, "n": nn, "checks": ch})
    return counts, top


def library():
    lib_ = []
    for w in range(2, N):
        for r in READINGS:
            seq = stage(list(range(N)), w, r)
            wh = [0] * N
            for j, i in enumerate(seq):
                wh[i] = j
            lib_.append((f"{r}{w}", wh))
    for b in range(2, N):
        lib_.append((f"k3x{b}", [(b * i) % N for i in range(N)]))
    out, seen = [], set()
    for name, m in lib_:
        for d, mm in (("", m), ("inv", inverse(m))):
            k = bytes(mm)
            if k not in seen:
                seen.add(k); out.append((name + d, mm))
    return out


def run(ctx):
    import multiprocessing as mp
    import sys
    import types
    ct, known = ctx.K4, ctx.KNOWN
    known_list = [(q, known[q]) for q in sorted(known)]
    tables = []
    for (A, B, nm) in ((STD, KRY, "std then kry"), (KRY, STD, "kry then std")):
        for s1 in (1, -1):
            for s2 in (1, -1):
                F, G = link_tables(A, B, s1, s2)
                tables.append((f"{nm}, signs {s1:+d}{s2:+d}", F, G))
    # check: a planted text (random keys, a move) must be consistent with its true setting
    vr = random.Random(1607)
    libm = library()
    name, m = libm[123]
    k1 = [vr.randrange(26) for _ in range(5)]; k2 = [vr.randrange(26) for _ in range(7)]
    pt = [vr.choice(STD) for _ in range(N)]
    for q, a in known.items():
        pt[q - 1] = a
    y = [STD[(STD.index(pt[i]) + k1[i % 5]) % 26] for i in range(N)]            # std table, +1
    moved = [""] * N
    for i in range(N):
        moved[m[i]] = y[i]
    ctp = "".join(KRY[(KRY.index(moved[j]) + k2[j % 7]) % 26] for j in range(N))   # kry table, +1
    land = [m[q - 1] for q, _ in known_list]
    links = [((q - 1) % 5, land[e] % 7, STD.index(a), STD.index(ctp[land[e]])) for e, (q, a) in enumerate(known_list)]
    assert decide(links, tables[0][1], tables[0][2]) >= 0
    rng = random.Random(1607)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    T = len(texts)
    W = 8
    jobs = [(libm[i::W * 6], texts, known_list, tables) for i in range(W * 6)]
    if getattr(sys.modules.get(__name__), "_work", None) is not _work:
        mod = types.ModuleType(__name__); mod.__dict__.update(globals()); sys.modules[__name__] = mod
    t0 = time.time()
    with mp.get_context("fork").Pool(W) as pool:
        parts = pool.map(_work, jobs, chunksize=1)
    counts = [[sum(p[0][t][c] for p in parts) for c in range(25)] for t in range(T)]
    top = sorted([x for p in parts for x in p[1]], key=lambda x: -x["checks"])
    ge5 = [sum(counts[t][5:]) for t in range(T)]
    by_level = {c: {"k4": counts[0][c], "coppers_min": min(counts[t][c] for t in range(1, T)), "coppers_max": max(counts[t][c] for t in range(1, T))} for c in range(0, 9)}
    bounds = {"family": "change (table A), move, change (table B != A): two repeating keys of lengths 2-14 on different tables round one of 844 moves",
              "moves": len(libm), "key_lengths": [2, 14], "table_orders": ["std then kry", "kry then std"], "signs": 4,
              "consistent_by_checks": by_level, "k4_consistent_with_5_or_more_checks": ge5[0], "coppers_with_5_or_more": ge5[1:],
              "k4_top": top[:20], "seconds": round(time.time() - t0),
              "controls": f"{N_CONTROLS} shuffled coppers (seed 1607)", "exhaustive": True}
    notes = (f"{len(libm)} moves x 169 key-length pairs x 8 table/sign settings: consistent with >= 5 checks K4 {ge5[0]} (coppers {min(ge5[1:])}-{max(ge5[1:])}); "
             f"by checks 1-4 K4 {[counts[0][c] for c in range(1, 5)]}")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    return "\n".join(["first word on the plain-alphabet table, a grid move, second word on the KRYPTOS table", "",
                       "at a known place: guess the first-word letter v; the known letter plus v (plain alphabet) is the middle letter;",
                       "the carved letter minus the middle letter (KRYPTOS alphabet) is the second-word letter: one second letter per guess.",
                       "every known letter ties a first-word slot to a second-word slot this way; a contradiction for all 26 guesses rules the setting out."])
