"""Experiment 0085. See program.md for the contract."""

EXPERIMENT = {
    "slug": "true-keyword-columnar-rerun",
    "title": "Column shuffles keyed by the puzzle's words, read the right way round this time: once or twice, with a repeating key or an autokey",
    "family": "6-transposition-then-tableau",
    "parent": "0026-double-keyed-columnar-then-tableau",
    "changed": "Issue #26: ten records (0006-0081) passed a keyword's rank list as the reading sequence, so their keyed column shuffles read the columns in the inverse order. This reruns keyed columnar with the true keyword reading (columns in the alphabetical order of the key letters), with repeated letters dropped and on the whole word with ties left to right, once (both directions) or twice (every ordered pair), against a repeating key of length 1-26 before or after, and against the plaintext and ciphertext autokeys at every lag in both orders.",
    "hypothesis_expert": (
        "Correction run for issue #26, filed during type 2 of directions.md. The bounds it restores: keyed columnar then "
        "tableau (0006, 0016), tableau then keyed columnar (0007, 0058), keyed double columnar (0026), keyed columnar with "
        "ciphertext autokey (0063), and the keyed-columnar subsets of 0080 and 0081. Clues C1(a) (02-sanborn-said.md, CNN "
        "2005, 'double matrixes'), C8(a) (KRYPTOS as a transposition key for K4, as the NSA read it for K3), C7(a) (K1-K3 "
        "words as keys). Key words: data/vocabulary.txt, the K1-K3 plaintext words of 3-20 letters, and the C13/C14 words; "
        "each gives up to two sequences (repeats dropped, as kryptos.alphabets.numeric_order does; or the whole word with "
        "ties left to right), deduplicated. Routes: each sequence once, columnar encryption or its inverse; every ordered "
        "pair of sequences, encryption twice. Keys: (i) periodic tableau key 1-26 after the move (slot = landing place mod "
        "p) or before it (slot = place mod p), 8 classes, live if no slot holds two different forced letters; (ii) "
        "plaintext autokey and (iii) ciphertext autokey at lags 1-96, one alphabet throughout (standard or KRYPTOS), "
        "three modes, autokey after the move (order A) or before it (order B), checked exactly as in 0081. Ten shuffled "
        "coppers through the identical search."
    ),
    "hypothesis_eli5": (
        "A column shuffle keyed by a word writes the message in rows under the word and reads the columns in the "
        "alphabetical order of its letters. Our earlier experiments made a slip: they read the columns in a related but "
        "different order, so the true keyed shuffles were never tested. This experiment repeats the tests with the "
        "right order: every puzzle word as the key, used once or twice, followed or preceded by a repeating secret "
        "word on the table, or by an autokey, where the message feeds its own key."
    ),
    "prediction": (
        "As for the inverse readings: nothing live below period 22 for the repeating key beyond the shuffled-copper "
        "rate; no autokey setting passes five checks; counts at every level inside the control range, give or take the "
        "spread at the lowest levels. Zero candidates."
    ),
    "method": (
        "1. Build the keyword sequences and the single and double routes; skip repeats. 2. For each route, test a "
        "repeating key of length 1-26 on either side by the forced-letter slots. 3. For each route, test the plaintext "
        "and ciphertext autokeys at every lag on either side by walking the chains between known letters. 4. Count "
        "survivors by period or number of checks on K4 and ten shuffled coppers. 5. List K4's survivors below period 20 "
        "or with four or more checks."
    ),
    "walkthrough": (
        "1. Write the message in rows of 7 under KRYPTOS. The key letters rank K 0, R 3, Y 6, P 2, T 5, O 1, S 4. 2. Read the columns in rank order: column 0 (K), then 5 (O), 3 (P), 1 (R), 6 (S), 4 (T), 2 (Y). The earlier records read 0, 3, 6, 2, 5, 1, 4 instead, the ranks themselves. 3. Place 23, the A of EAST, is in row 3 of column 1. Columns 0, 5 and 3 hold 14 letters each, so it becomes letter 46; the earlier reading put it at 73. 4. Under a repeating key on the table, the known letter and the copper letter at its new place force one key letter; two known letters whose new places differ by a multiple of the key length must force the same one. 5. Under an autokey, two known letters one lag apart are tied through the copper letters between them. 6. Repeat for every word key, once or twice, every key length and lag, both orders, and ten scrambled coppers."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.alphabets import numeric_order
from kryptos.ciphers import columnar_transposition_encrypt

N = 97
PMAX = 26
LAGS = range(1, N)
ALPH = {"std": STD, "kry": KRY}
N_CONTROLS = 10
MODES = {"vig": (-1, 1), "beau": (1, -1), "var": (1, 1)}

SPACED = (
    "BETWEEN SUBTLE SHADING AND THE ABSENCE OF LIGHT LIES THE NUANCE OF IQLUSION "
    "IT WAS TOTALLY INVISIBLE HOWS THAT POSSIBLE THEY USED THE EARTHS MAGNETIC FIELD X THE INFORMATION WAS GATHERED AND "
    "TRANSMITTED UNDERGRUUND TO AN UNKNOWN LOCATION X DOES LANGLEY KNOW ABOUT THIS THEY SHOULD ITS BURIED OUT THERE "
    "SOMEWHERE X WHO KNOWS THE EXACT LOCATION ONLY WW THIS WAS HIS LAST MESSAGE X THIRTY EIGHT DEGREES FIFTY SEVEN "
    "MINUTES SIX POINT FIVE SECONDS NORTH SEVENTY SEVEN DEGREES EIGHT MINUTES FORTY FOUR SECONDS WEST ID BY ROWS "
    "SLOWLY DESPARATLY SLOWLY THE REMAINS OF PASSAGE DEBRIS THAT ENCUMBERED THE LOWER PART OF THE DOORWAY WAS REMOVED "
    "WITH TREMBLING HANDS I MADE A TINY BREACH IN THE UPPER LEFT HAND CORNER AND THEN WIDENING THE HOLE A LITTLE I "
    "INSERTED THE CANDLE AND PEERED IN THE HOT AIR ESCAPING FROM THE CHAMBER CAUSED THE FLAME TO FLICKER BUT PRESENTLY "
    "DETAILS OF THE ROOM WITHIN EMERGED FROM THE MIST X CAN YOU SEE ANYTHING Q"
)
EXTRA = ["EGYPT", "CAIRO", "LUXOR", "WALL", "NOVEMBER", "MESSAGE", "DELIVER", "DELIVERING", "TRANSMIT"]


def where_columnar(seq):
    """where[i] = position of letter i after columnar encryption reading columns in sequence seq."""
    idx = "".join(chr(0x100 + i) for i in range(N))
    out = columnar_transposition_encrypt(idx, list(seq))
    w = [0] * N
    for j, ch in enumerate(out):
        w[ord(ch) - 0x100] = j
    return w


def keyword_sequence(word):
    """The true keyword reading: columns in alphabetical order of the key letters (ties left to right)."""
    rank = numeric_order(word)
    return sorted(range(len(rank)), key=lambda c: rank[c])


def full_sequence(word):
    """Keyword reading on the whole word, repeated letters kept and ties read left to right (ABSCISSA: 8 columns)."""
    w = [c for c in word.upper() if c.isalpha()]
    return sorted(range(len(w)), key=lambda c: (w[c], c))


def second_stages(vocab):
    out, seen = [], set()
    for w in range(2, 31):
        for rtl in (False, True):
            seq = tuple(range(w))[::-1] if rtl else tuple(range(w))
            if seq not in seen:
                seen.add(seq); out.append((f"plain {w}{' rtl' if rtl else ''}", seq))
    words = sorted({w for w in "".join(c if c.isalpha() or c == " " else " " for c in SPACED).split() if 3 <= len(w) <= 20}
                   | set(EXTRA) | {w for w in vocab if 2 <= len(w) <= 30})
    for word in words:
        for how, seq in (("repeats dropped", tuple(keyword_sequence(word))), ("full word", tuple(full_sequence(word)))):
            if len(seq) >= 2 and seq not in seen:
                seen.add(seq); out.append((f"{word} ({how})", seq))
    return out


def slot_pairs(slots):
    last, prs = {}, []
    for e, s in enumerate(slots):
        if s in last:
            prs.append((last[s], e))
        last[s] = e
    return prs



def ct_dec(mode, c, k):
    return {"vig": (c - k) % 26, "beau": (k - c) % 26, "var": (c + k) % 26}[mode]


def keyed_sequences(vocab):
    words = sorted({w for w in "".join(c if c.isalpha() or c == " " else " " for c in SPACED).split() if 3 <= len(w) <= 20}
                   | set(EXTRA) | {w for w in vocab if 2 <= len(w) <= 30})
    out, seen = [], set()
    for word in words:
        for how, seq in (("repeats dropped", tuple(keyword_sequence(word))), ("full word", tuple(full_sequence(word)))):
            if len(seq) >= 2 and seq not in seen:
                seen.add(seq); out.append((f"{word} ({how})", seq))
    return out


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    places = sorted(known)
    pidx = [p - 1 for p in places]
    rng = random.Random(85)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    T = len(texts)
    assert keyword_sequence("KRYPTOS") == [0, 5, 3, 1, 6, 4, 2]
    seqs = keyed_sequences(list(ctx.vocabulary))
    WS = [where_columnar(s) for _, s in seqs]
    routes, seen = [], set()
    for i, (name, _) in enumerate(seqs):
        fwd = WS[i]
        inv = [0] * N
        for a, j in enumerate(fwd):
            inv[j] = a
        for d, wh in (("once", fwd), ("once, inverse", inv)):
            h = tuple(wh)
            if h not in seen:
                seen.add(h); routes.append((f"{name} {d}", wh))
    for i, (n1, _) in enumerate(seqs):
        for j, (n2, _) in enumerate(seqs):
            wh = [WS[j][WS[i][a]] for a in range(N)]
            h = tuple(wh)
            if h not in seen:
                seen.add(h); routes.append((f"{n1} then {n2}", wh))
    del seen
    # periodic key machinery
    classes = [(pa, ca, beau) for pa in ALPH for ca in ALPH for beau in (False, True)]
    CI = {an: [[{c: i for i, c in enumerate(ALPH[an])}[ch] for ch in t] for t in texts] for an in ALPH}
    PI = {an: [{c: i for i, c in enumerate(ALPH[an])}[known[p]] for p in places] for an in ALPH}
    G = [[[[((CI[ca][t][j] + PI[pa][e]) if beau else (CI[ca][t][j] - PI[pa][e])) % 26 for j in range(N)]
           for e in range(24)] for t in range(T)] for pa, ca, beau in classes]
    pairsB = [None] + [slot_pairs([i % p for i in pidx]) for p in range(1, PMAX + 1)]
    live = {o: [[0] * (PMAX + 1) for _ in range(T)] for o in "AB"}
    low = []
    # autokey machinery (as 0081)
    convs = [(an, m) for an in ALPH for m in MODES]
    TI = CI
    KI = PI
    counts = {(k, o): [dict() for _ in range(T)] for k in ("ptak", "ctak") for o in "AB"}
    hits = []
    pairsBak = {}
    for L in LAGS:
        last, prs = {}, []
        for e, i in enumerate(pidx):
            r = i % L
            if r in last:
                prs.append((last[r], e))
            last[r] = e
        prs.sort(key=lambda pr: pidx[pr[1]] - pidx[pr[0]])
        pairsBak[L] = prs
    pairsB_ak = pairsBak
    stopped = None
    for ri, (spec, w) in enumerate(routes):
        if ctx.time_left() < 60:
            stopped = ri
            break
        land = [w[i] for i in pidx]
        pairsA = [None] + [slot_pairs([j % p for j in land]) for p in range(1, PMAX + 1)]
        for ci in range(8):
            for t in range(T):
                g = G[ci][t]
                f = [g[e][land[e]] for e in range(24)]
                LA, LB = live["A"][t], live["B"][t]
                for p in range(1, PMAX + 1):
                    for a, b in pairsA[p]:
                        if f[a] != f[b]:
                            break
                    else:
                        LA[p] += 1
                        if t == 0 and p < 20:
                            low.append({"route": spec, "order": "A", "class": ci, "period": p})
                    for a, b in pairsB[p]:
                        if f[a] != f[b]:
                            break
                    else:
                        LB[p] += 1
                        if t == 0 and p < 20:
                            low.append({"route": spec, "order": "B", "class": ci, "period": p})
        landord = sorted(range(24), key=lambda e: land[e])
        pairsB = pairsB  # periodic pairs (kept)
        for an, mode in convs:
            sig, tau = MODES[mode]
            KIa = KI[an]
            for t in range(T):
                C = TI[an][t]
                X = [C[w[i]] for i in range(N)]
                for L in LAGS:
                    # ---- plaintext autokey, order A: known Z at landing places, chain through C
                    last, prs = {}, []
                    for e in landord:
                        r = land[e] % L
                        if r in last:
                            prs.append((last[r], e))
                        last[r] = e
                    if prs:
                        ok = True
                        for e1, e2 in prs:
                            z, j, j2 = KIa[e1], land[e1] + L, land[e2]
                            while j <= j2:
                                z = (sig * z + tau * C[j]) % 26; j += L
                            if z != KIa[e2]:
                                ok = False; break
                        if ok:
                            c = len(prs); d = counts[("ptak", "A")][t]; d[c] = d.get(c, 0) + 1
                            if t == 0 and c >= 4:
                                hits.append({"kind": "plaintext autokey", "order": "A", "route": spec, "alphabet": an, "mode": mode, "lag": L, "checks": c})
                    # ---- plaintext autokey, order B: known Z in place, chain through X
                    prs = pairsB_ak[L]
                    if prs:
                        ok = True
                        for e1, e2 in prs:
                            z, j, j2 = KIa[e1], pidx[e1] + L, pidx[e2]
                            while j <= j2:
                                z = (sig * z + tau * X[j]) % 26; j += L
                            if z != KIa[e2]:
                                ok = False; break
                        if ok:
                            c = len(prs); d = counts[("ptak", "B")][t]; d[c] = d.get(c, 0) + 1
                            if t == 0 and c >= 4:
                                hits.append({"kind": "plaintext autokey", "order": "B", "route": spec, "alphabet": an, "mode": mode, "lag": L, "checks": c})
                    # ---- ciphertext autokey, order A: Z[j] = dec(C[j], C[j-L]) at landing places
                    c = 0; ok = True
                    for e in range(24):
                        j = land[e]
                        if j >= L:
                            if ct_dec(mode, C[j], C[j - L]) != KIa[e]:
                                ok = False; break
                            c += 1
                    if ok and c:
                        d = counts[("ctak", "A")][t]; d[c] = d.get(c, 0) + 1
                        if t == 0 and c >= 4:
                            hits.append({"kind": "ciphertext autokey", "order": "A", "route": spec, "alphabet": an, "mode": mode, "lag": L, "checks": c})
                    # ---- ciphertext autokey, order B: P[i] = dec(X[i], X[i-L]) in place
                    c = 0; ok = True
                    for e in range(24):
                        i = pidx[e]
                        if i >= L:
                            if ct_dec(mode, X[i], X[i - L]) != KIa[e]:
                                ok = False; break
                            c += 1
                    if ok and c:
                        d = counts[("ctak", "B")][t]; d[c] = d.get(c, 0) + 1
                        if t == 0 and c >= 4:
                            hits.append({"kind": "ciphertext autokey", "order": "B", "route": spec, "alphabet": an, "mode": mode, "lag": L, "checks": c})
    summary, outside = {}, []
    for (kind, order), per in counts.items():
        ge = lambda d, c0: sum(v for c, v in d.items() if c >= c0)
        k4 = {c0: ge(per[0], c0) for c0 in range(1, 7)}
        ctl = {c0: [ge(per[t], c0) for t in range(1, T)] for c0 in range(1, 7)}
        out = [c0 for c0 in range(1, 7) if not (min(ctl[c0]) <= k4[c0] <= max(ctl[c0]))]
        if out:
            outside.append(f"{kind} {order}: {out}")
        summary[f"{kind} order {order}"] = {"k4_at_least_c": k4, "controls_at_least_c": ctl}
    p_out = {o: [p for p in range(1, PMAX + 1) if not (min(live[o][t][p] for t in range(1, T)) <= live[o][0][p] <= max(live[o][t][p] for t in range(1, T)))] for o in "AB"}
    for h in low:
        c = classes[h["class"]]
        h["class"] = f"{c[0]}/{c[1]}/{'beau' if c[2] else 'vig-var'}"
    bounds = {
        "family": "true keyword columnar (issue #26), once or twice, with a periodic key 1-26 or plaintext/ciphertext autokey, both orders",
        "keyword_sequences": len(seqs), "distinct_routes": len(routes), "routes_done": stopped if stopped is not None else len(routes),
        "periodic": {"k4_live_by_period": {o: live[o][0][1:] for o in "AB"},
                     "controls_min": {o: [min(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in "AB"},
                     "controls_max": {o: [max(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in "AB"},
                     "periods_outside_control_range": p_out, "k4_live_below_20": low[:40], "n_k4_live_below_20": len(low),
                     "controls_live_below_20": {o: [sum(live[o][t][p] for p in range(1, 20)) for t in range(1, T)] for o in "AB"}},
        "autokey": {"by_kind_and_order": summary, "levels_outside_control_range": outside,
                    "k4_settings_with_4_plus_checks": hits[:40], "n_k4_4_plus": len(hits)},
        "controls": f"{N_CONTROLS} shuffled coppers (seed 85), identical search",
    }
    line = "; ".join(f"{k}: K4 >=1..6 {[v['k4_at_least_c'][c] for c in range(1, 7)]}, controls max "
                     f"{[max(v['controls_at_least_c'][c]) for c in range(1, 7)]}" for k, v in summary.items())
    notes = (f"{len(routes):,} distinct routes from {len(seqs)} keyword sequences. Periodic: K4 live below 20: {len(low)}; "
             f"controls {bounds['periodic']['controls_live_below_20']}; periods outside the control range {p_out}. Autokey: {line}. "
             f"Outside: {outside or 'none'}. K4 autokey settings with 4+ checks: {len(hits)}."
             + (f" Stopped at route {stopped} for time." if stopped is not None else ""))
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    seq = keyword_sequence("KRYPTOS")
    lines = ["KRYPTOS as a column key: K R Y P T O S ranks 0 3 6 2 5 1 4, so the columns are read 0 5 3 1 6 4 2",
             "(the earlier records read 0 3 6 2 5 1 4, the ranks themselves)", ""]
    w_true = where_columnar(seq)
    w_old = where_columnar(numeric_order("KRYPTOS"))
    lines.append("place  letter  column  lands at (true)  lands at (earlier)")
    for p in (22, 23, 24, 25, 64):
        lines.append(f"{p:>5}  {known[p]:>6}  {(p - 1) % 7:>6}  {w_true[p - 1] + 1:>15}  {w_old[p - 1] + 1:>18}")
    return "\n".join(lines)
