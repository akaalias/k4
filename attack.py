"""Experiment 0037. See program.md for the contract."""

EXPERIMENT = {
    "slug": "triple-matrix-routes-sampled-then-tableau",
    "title": "Sanborn's triple matrixes: three grid stages in a row, sampled, then the tableau",
    "family": "6-transposition-then-tableau",
    "parent": "0016-routes-then-tableau-forced-key-english",
    "changed": "Three transposition stages instead of one or two. The space is too large to enumerate, so 200,000 triples are drawn at random from plain columnar widths 2-30, rotations, and keyed columnar from vocabulary words, each stage forward or inverse. The survival test and English scoring of experiments 6 and 16 are unchanged.",
    "hypothesis_expert": (
        "Sanborn, CNN 2005 (C1): 'double matrixes and triple matrixes... then went back to this table'. "
        "Experiments 6, 8, 16 and 26 covered single and double stages exhaustively for their route sets. "
        "Triples of 110 stage choices number about 1.3 million, beyond the budget with the English "
        "scoring, so this is a sample: 200,000 triples drawn uniformly, with a fixed seed, each stage one of "
        "plain columnar at widths 2-30 forward or inverse, a quarter-turn rotation at widths 2-30, or a "
        "keyed columnar from a vocabulary word forward or inverse. For each triple under the 8 distinct "
        "plain-cipher conventions the forced tableau key letters give the live periods by the divisor rule; "
        "the smallest live period is recorded, and the forced key at live periods up to 40 is scored as "
        "English on runs of five or more slots against ten shuffled controls. A triple with a live period "
        "under 20 or an English key above the controls would be a lead. Bounds: a 15 percent sample, not "
        "exhaustive; the smallest-period distribution says whether triples behave as random permutations."
    ),
    "hypothesis_eli5": (
        "The artist said he sometimes scrambled the letters through three grids before using the table. "
        "There are over a million ways to pick three grids from our set, too many to try with the slow "
        "English check, so we draw two hundred thousand at random. For each, we follow the 24 known letters "
        "through all three grids, ask whether a short secret word could then produce the carved letters "
        "where they land, and whether the letters of that word look like English. Three grids in a row "
        "behave like a random shuffle, so the answer should look like the earlier grid experiments."
    ),
    "prediction": (
        "The smallest live period over the sample is 22 or 23, as for single and double stages. The best "
        "forced key scores inside the range of ten shuffled controls. No candidate."
    ),
    "method": (
        "1. Build the stage list. 2. Draw 200,000 triples with a fixed seed. 3. For each triple compose the "
        "three permutations and send the crib positions through. 4. For each of the 8 conventions force the "
        "key letters, find live periods by the divisor rule, and score the forced key at live periods up to "
        "40. 5. Keep the twenty best keys and the smallest-period histogram. 6. Repeat on ten shuffles."
    ),
    "walkthrough": (
        "1. Pick three grids: rows of 7 read down, then a quarter turn of a 12-wide grid, then columns in "
        "the order of the letters of KRYPTOS. 2. Follow position 22, the E of EAST, through the first grid "
        "to its new place, then through the second, then the third. 3. Do this for all 24 known letters. "
        "4. The carved letter at each final place, with the known letter, forces one key letter on the table. "
        "5. Two final places a multiple of p apart share a key letter at period p; a disagreement kills p. "
        "6. The smallest surviving p is this triple's score; write its forced letters into their slots and "
        "read them."
    ),
}

import random
from kryptos.alphabets import key_letter_for, numeric_order
from kryptos.ciphers import columnar_transposition_encrypt, columnar_transposition_decrypt

N = 97
MAXP = 40
SAMPLE = 200000
DIVISORS = {d: [k for k in range(1, d + 1) if d % k == 0] for d in range(1, N + 1)}
CONVS = [(pa, ca, "kry", m) for pa in ("std", "kry") for ca in ("std", "kry") for m in ("vig", "beau")]   # ka drops out; varbeau = vig for the test


def perm_of(fn):
    idx = [chr(0x100 + i) for i in range(N)]
    return [ord(ch) - 0x100 for ch in fn("".join(idx))]


def rotate(s, w):
    rows = [s[i:i + w] for i in range(0, len(s), w)]
    return "".join(r[col] for col in range(w) for r in reversed(rows) if col < len(r))


def stages(vocab):
    out = []
    for w in range(2, 31):
        o = list(range(w))
        out.append((f"columnar {w}", lambda s, o=o: columnar_transposition_encrypt(s, o)))
        out.append((f"columnar {w} inv", lambda s, o=o: columnar_transposition_decrypt(s, o)))
        out.append((f"rotate {w}", lambda s, w=w: rotate(s, w)))
    for word in vocab:
        if 2 <= len(word) <= 30:
            o = numeric_order(word)
            out.append((f"keyed {word}", lambda s, o=o: columnar_transposition_encrypt(s, o)))
            out.append((f"keyed {word} inv", lambda s, o=o: columnar_transposition_decrypt(s, o)))
    return out


def encrypt(plaintext, key):
    raise NotImplementedError("diagnostic experiment: no full key is implied, so no candidate is submitted")


def runs_in_slots(slots, P):
    filled = [slots.get(s) for s in range(P)]
    start = 0 if all(filled) else next(i for i in range(P) if filled[i] is None)
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


def search(ct, known, triples, stage_perms, score, time_left):
    crib_pos = sorted(known)
    best, hist, n = [], {}, 0
    for t in triples:
        if time_left() < 30:
            break
        # compose: out3[j] = in[sigma1[sigma2[sigma3[j]]]]
        s1, s2, s3 = stage_perms[t[0]], stage_perms[t[1]], stage_perms[t[2]]
        sigma = [s1[s2[s3[j]]] for j in range(N)]
        where = {sigma[j]: j for j in range(N)}
        inter = [where[p - 1] for p in crib_pos]
        for conv in CONVS:
            pa, ca, ka, m = conv
            forced = [key_letter_for(known[p], ct[j], pa, ca, ka, m) for p, j in zip(crib_pos, inter)]
            dead = set()
            for a in range(24):
                for b in range(a + 1, 24):
                    if forced[a] != forced[b]:
                        dead.update(DIVISORS[abs(inter[a] - inter[b])])
            minp = next(P for P in range(1, N + 1) if P not in dead)
            hist[minp] = hist.get(minp, 0) + 1
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
                    best.append((sc, t, "/".join(conv), P, runs)); best.sort(reverse=True); best = best[:20]
    return best, hist, n


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    st = stages(list(ctx.vocabulary))
    names = [nm for nm, _ in st]
    perms = [perm_of(fn) for _, fn in st]
    rng = random.Random(37)
    triples = [(rng.randrange(len(st)), rng.randrange(len(st)), rng.randrange(len(st))) for _ in range(SAMPLE)]
    best, hist, n = search(ct, known, triples, perms, ctx.english_score, ctx.time_left)
    nulls = []
    for seed in range(10):
        if ctx.time_left() < 150:
            break
        letters_ = list(ct); random.Random(seed).shuffle(letters_)
        nb, _, _ = search("".join(letters_), known, triples[:6000], perms, ctx.english_score, ctx.time_left)
        nulls.append(round(nb[0][0], 3) if nb else None)
    return {
        "candidates": [],
        "bounds": {"family": "three transposition stages (sampled) then periodic tableau", "stages": len(st), "triples_sampled": len(triples), "conventions": len(CONVS),
                   "keys_scored": n, "smallest_live_period": min(hist) if hist else None,
                   "min_live_period_histogram": {str(k): v for k, v in sorted(hist.items())[:12]},
                   "best": [{"score": round(sc, 3), "stages": [names[i] for i in t], "convention": cv, "period": P, "runs": rs} for sc, t, cv, P, rs in best[:10]],
                   "shuffled_control_best": nulls, "control_note": "controls use the first 6,000 triples of the same sample"},
        "notes": f"Diagnostic, no candidates. {len(triples)} triples x {len(CONVS)} conventions; smallest live period {min(hist) if hist else None}; best forced key {best[0][0]:.3f} vs shuffled {[x for x in nulls if x is not None]}.",
    }


def worked_example(ctx, key):
    st = stages(["KRYPTOS"])
    names = [nm for nm, _ in st]
    i1, i2, i3 = names.index("columnar 7"), names.index("rotate 12"), names.index("keyed KRYPTOS")
    perms = {i: perm_of(st[i][1]) for i in (i1, i2, i3)}
    sigma = [perms[i1][perms[i2][perms[i3][j]]] for j in range(N)]
    where = {sigma[j]: j for j in range(N)}
    lines = ["stages: columnar 7, then rotate 12, then keyed columnar KRYPTOS; convention kry/kry/kry Vigenere", "", "plain pos  letter  final place  carved  forced key letter"]
    for pos in (22, 23, 24, 64, 65, 66):
        j = where[pos - 1]
        lines.append(f"{pos:>9}    {ctx.KNOWN[pos]}        {j+1:>3}        {ctx.K4[j]}       {key_letter_for(ctx.KNOWN[pos], ctx.K4[j], 'kry', 'kry', 'kry', 'vig')}")
    return "\n".join(lines)
