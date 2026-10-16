"""Experiment 0173 (F3.1, first part). See program.md for the contract."""

EXPERIMENT = {
    "slug": "scheidt-patent-sandwich",
    "title": "F3.1: Scheidt's patent sandwich, a shift, a keyed table, a second shift and a second table, two repeating keys of length 1-13 each: exact",
    "family": "3-two-component-key",
    "parent": "0115-two-key-words-added",
    "changed": (
        "F3.1, first the sandwich (reports/Scheidt patents and field ciphers.md, issue #9). Scheidt and Wack's patent "
        "US 6,075,865 writes the text/key relation as O = a_N + pi_N[a_N-1 + ... pi_1[I + a_0]] mod W. With one table "
        "between two key streams, and letters numbered by a third table, c = T2[s2 * T1[s1 * T0[p] + a_i] + b_i], each T "
        "one of {standard, KRYPTOS order, its inverse} and each sign + or -: 108 table classes. a repeats every La letters, "
        "b every Lb, La and Lb 1-13. F3's closed items added two keys outside any table (0014, 0043, 0059, 0115); here a "
        "table sits between them, so the alphabet in force changes with a's phase."
    ),
    "hypothesis_expert": (
        "C5(b) ('key word/s'), C6 (Scheidt's constructive key management), US 6,075,865 (Scheidt and Wack, priority 1998; "
        "report in reports/Scheidt patents and field ciphers.md). Model as in 'changed'. Each known place i gives "
        "b[i mod Lb] = T2^-1[c_i] * s2' - T1[s1 T0[p_i] + a[i mod La]], a one-to-one map between one slot of a and one "
        "slot of b. The slots form a graph; in each connected part, fixing one slot of a fixes all the others, so 26 trials "
        "decide the part exactly. A cell (class, La, Lb) is live if every part has a value that agrees on every edge; it "
        "carries E - V + C checks (edges minus slots plus parts). Statistic: live cells with at least one check, by number "
        "of checks, K4 against 20 shuffled coppers."
    ),
    "hypothesis_eli5": (
        "Scheidt, who built the sculpture's codes, later patented a way of enciphering a letter: shift it by a key "
        "letter, look it up in a mixed-up alphabet, shift it again by a second key letter, look it up again. With two "
        "short secret words as the two keys, the 24 known letters tie the two words' letters together in pairs; we try "
        "every way of choosing the tables and every pair of word lengths up to 13, and see whether anything fits K4 "
        "better than scrambled copies of it."
    ),
    "prediction": (
        "K4's live cells at each number of checks fall inside the coppers' range; no cell with 6 or more checks is live on "
        "K4. Zero candidates."
    ),
    "method": (
        "1. For each pair of lengths (La, Lb) 1-13: the graph of key slots the 24 known places make, its parts and its "
        "number of checks. "
        "2. For each text (K4, 20 coppers) and each of 108 table classes: for each part, try the 26 values of one slot of "
        "a, carry them along the edges, and keep the values that agree on every edge. "
        "3. Count live cells by checks; for K4's live cells with 4 or more checks, decrypt the places their keys fix. "
        "4. Builder check: three planted texts made with this cipher are live in their own cell."
    ),
    "walkthrough": (
        "1. Take the sculpture's KRYPTOS alphabet as the table, a first key of length 5 and a second of length 7. "
        "2. At place 22 the message has E and the copper has F. Counting places from 0 (21), E is shifted by the first key's slot 21 mod 5 = 1, "
        "looked up in the table, and shifted by the second key's slot 21 mod 7 = 0: the result must be F. "
        "3. So each choice for slot 1 of the first key forces slot 0 of the second. "
        "4. Place 29 links slot 3 of the first key to slot 0 of the second: two routes into slot 0 must agree. "
        "5. Try all 26 letters for one slot, follow every link, and keep the letters that never contradict. "
        "6. Do this for every table choice and length pair, on K4 and on scrambled copies."
    ),
}

import random
import time
from collections import Counter

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY, KNOWN

N_CONTROLS = 20
LMAX = 13
PLACES = sorted(KNOWN)                       # 1-based
KP = [q - 1 for q in PLACES]
KL = [KNOWN[q] for q in PLACES]

K = [STD.index(ch) for ch in KRY]            # K[i] = standard number of the i-th KRYPTOS letter
KI = [K.index(j) for j in range(26)]
ID = list(range(26))


def inv(T):
    return [T.index(j) for j in range(26)]
TABLES = {"std": ID, "kry": K, "kry-inv": KI}


def classes():
    out = []
    for t0 in TABLES:
        for t1 in TABLES:
            for t2 in TABLES:
                for s1 in (1, -1):
                    for s2 in (1, -1):
                        out.append((t0, t1, t2, s1, s2))
    return out


def graph(La, Lb):
    """Parts of the slot graph: each a list of (edge index e, from-node, to-node, kind) in BFS order, plus non-tree edges."""
    edges = [(KP[e] % La, KP[e] % Lb) for e in range(24)]
    adj = {}
    for e, (r, s) in enumerate(edges):
        adj.setdefault(("a", r), []).append((e, ("b", s)))
        adj.setdefault(("b", s), []).append((e, ("a", r)))
    seen, parts = set(), []
    for start in sorted(adj):
        if start[0] != "a" or start in seen:
            continue
        seen.add(start)
        order, tree_edges, q = [], set(), [start]
        while q:
            n = q.pop(0)
            for e, m in adj[n]:
                if m not in seen:
                    seen.add(m)
                    tree_edges.add(e)
                    order.append((e, n, m))
                    q.append(m)
        nodes = {start} | {m for _, _, m in order}
        part_edges = {e for n in nodes for e, _ in adj[n]}
        extra = [(e, ("a", edges[e][0]), ("b", edges[e][1])) for e in sorted(part_edges - tree_edges)]
        parts.append((start, order, extra))
    V = len(adj)
    checks = 24 - V + len(parts)
    return parts, checks


def prep(text, cls):
    t0, t1, t2, s1, s2 = cls
    T0, T1, T2 = TABLES[t0], TABLES[t1], TABLES[t2]
    T1i, T2i = inv(T1), inv(T2)
    u = [(s1 * T0[STD.index(KL[e])]) % 26 for e in range(24)]
    v = [T2i[STD.index(text[KP[e]])] for e in range(24)]
    return u, v, T1, T1i, s2


def decide(parts, pre):
    """Returns per part the array of valid root values, plus the slot values for each surviving root."""
    u, v, T1, T1i, s2 = pre
    out = []
    for start, order, extra in parts:
        val = {start: ID}
        for e, n, m in order:
            x, ue, ve = val[n], u[e], v[e]
            if n[0] == "a":                       # b = v - s2 * T1[u + a]
                val[m] = [(ve - s2 * T1[(ue + y) % 26]) % 26 for y in x]
            else:                                 # a = T1^-1[s2 * (v - b)] - u
                val[m] = [(T1i[(s2 * (ve - y)) % 26] - ue) % 26 for y in x]
        ok = [True] * 26
        for e, na, nb in extra:
            ue, ve, A, B = u[e], v[e], val[na], val[nb]
            ok = [o and B[r] == (ve - s2 * T1[(ue + A[r]) % 26]) % 26 for r, o in enumerate(ok)]
            if not any(ok):
                break
        out.append((ok, val))
    return out


def encipher(p, cls, a, b):
    t0, t1, t2, s1, s2 = cls
    T0, T1, T2 = TABLES[t0], TABLES[t1], TABLES[t2]
    return "".join(STD[T2[(s2 * T1[(s1 * T0[STD.index(ch)] + a[i % len(a)]) % 26] + b[i % len(b)]) % 26]] for i, ch in enumerate(p))


def plant_text(rng):
    import json
    src = "".join(ch for ch in json.load(open("data/k2.json"))["plaintext_as_carved"].upper() if ch.isalpha())
    o = rng.randrange(0, len(src) - 97)
    p = list(src[o:o + 97])
    for q, ch in KNOWN.items():
        p[q - 1] = ch
    return "".join(p)


def run(ctx):
    t_start = time.time()
    ct = ctx.K4
    rng = random.Random(1730)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    CL = classes()
    G = {(La, Lb): graph(La, Lb) for La in range(1, LMAX + 1) for Lb in range(1, LMAX + 1)}

    # builder check: planted texts are live in their own cell
    plants = []
    for k in range(3):
        cls = CL[rng.randrange(len(CL))]
        while cls[1] == "std":
            cls = CL[rng.randrange(len(CL))]
        La, Lb = rng.randint(4, 13), rng.randint(4, 13)
        a = [rng.randrange(26) for _ in range(La)]; b = [rng.randrange(26) for _ in range(Lb)]
        p = plant_text(rng)
        c = encipher(p, cls, a, b)
        res = decide(G[(La, Lb)][0], prep(c, cls))
        plants.append({"class": "/".join(map(str, cls)), "La": La, "Lb": Lb, "checks": G[(La, Lb)][1],
                       "live_in_own_cell": all(any(ok) for ok, _ in res)})

    by_checks = []            # per text: Counter checks -> live cells (checks >= 1)
    by_checks_new = []        # same, middle table not the standard order (genuinely new)
    k4_live = []
    for ti, text in enumerate(texts):
        cnt, cnt_new = Counter(), Counter()
        for cls in CL:
            pre = prep(text, cls)
            for (La, Lb), (parts, checks) in G.items():
                if checks < 1:
                    continue
                res = decide(parts, pre)
                if all(any(ok) for ok, _ in res):
                    cnt[checks] += 1
                    if cls[1] != "std":
                        cnt_new[checks] += 1
                    if ti == 0 and checks >= 4:
                        k4_live.append((cls, La, Lb, checks, res, parts))
        by_checks.append(cnt); by_checks_new.append(cnt_new)

    maxc = max(max(c) if c else 0 for c in by_checks)
    table = {}
    for c in range(1, maxc + 1):
        table[c] = {"k4": by_checks[0][c], "coppers": [x[c] for x in by_checks[1:]],
                    "k4_new": by_checks_new[0][c], "coppers_new": [x[c] for x in by_checks_new[1:]]}

    def at_least(cnts, c):
        return sum(v for k, v in cnts.items() if k >= c)
    thresholds = {}
    for c in (1, 2, 4, 6, 8, 10):
        k4v = at_least(by_checks_new[0], c); cv = [at_least(x, c) for x in by_checks_new[1:]]
        thresholds[c] = {"k4": k4v, "coppers_min": min(cv), "coppers_max": max(cv),
                         "coppers_at_or_above_k4": sum(1 for x in cv if x >= k4v)}

    # K4's live cells with the most checks: decrypt where the keys are fixed
    k4_live.sort(key=lambda z: -z[3])
    examples = []
    for cls, La, Lb, checks, res, parts in k4_live[:12]:
        a = [None] * La; b = [None] * Lb
        for (ok, val), (start, order, extra) in zip(res, parts):
            if sum(ok) == 1:
                r = ok.index(True)
                for (side, slot), arr in val.items():
                    (a if side == "a" else b)[slot] = int(arr[r])
        t0, t1, t2, s1, s2 = cls
        T0, T1, T2 = TABLES[t0], TABLES[t1], TABLES[t2]
        T0i, T1i, T2i = inv(T0), inv(T1), inv(T2)
        pt = []
        for i, ch in enumerate(ct):
            ai, bi = a[i % La], b[i % Lb]
            if ai is None or bi is None:
                pt.append("."); continue
            x = T1i[(s2 * (T2i[STD.index(ch)] - bi)) % 26]
            pt.append(STD[T0i[(s1 * (x - ai)) % 26]])
        examples.append({"class": "/".join(map(str, cls)), "La": La, "Lb": Lb, "checks": checks,
                         "free_parts": sum(1 for ok, _ in res if sum(ok) > 1), "reading": "".join(pt)})

    graph_checks = Counter(c for (_, c) in G.values())
    bounds = {
        "family": "Scheidt patent sandwich c = T2[s2 T1[s1 T0[p] + a] + b], T in {standard, KRYPTOS, KRYPTOS inverse}, 108 classes, La, Lb 1-13, exact",
        "cells_per_text": len(CL) * sum(1 for g in G.values() if g[1] >= 1),
        "cells_by_checks": dict(sorted(graph_checks.items())),
        "live_by_checks": table,
        "new_classes_at_least": thresholds,
        "k4_live_examples": examples,
        "plants": plants,
        "copies": f"{N_CONTROLS} shuffled coppers (seed 1730)",
        "seconds": round(time.time() - t_start),
        "exhaustive": True,
    }
    th = thresholds
    notes = "live cells (middle table not standard), checks >= 1/4/6: K4 " + "/".join(str(th[c]["k4"]) for c in (1, 4, 6)) + \
            "; coppers " + "/".join(f"{th[c]['coppers_min']}-{th[c]['coppers_max']}" for c in (1, 4, 6)) + \
            f"; plants live in own cell {sum(p['live_in_own_cell'] for p in plants)}/3"
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    cls, a, b = key
    return encipher(plaintext, cls, a, b)


def worked_example(ctx, key):
    ct = ctx.K4
    La, Lb = 5, 7
    lines = [f"table KRYPTOS between the two keys, letters numbered on the standard order, first key length {La}, second {Lb}", ""]
    for q in PLACES[:13]:
        lines.append(f"place {q}: message {KNOWN[q]}, copper {ct[q - 1]}: links slot {(q - 1) % La} of the first key to slot {(q - 1) % Lb} of the second")
    parts, checks = graph(La, Lb)
    lines.append("")
    lines.append(f"{len(parts)} connected group(s) of slots, {checks} checks from all 24 known letters")
    return "\n".join(lines)
