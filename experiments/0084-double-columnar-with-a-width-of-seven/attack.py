"""Experiment 0084. See program.md for the contract."""

EXPERIMENT = {
    "slug": "double-columnar-with-a-width-of-seven",
    "title": "Two column shuffles, one of them seven columns wide in any of its 5,040 orders, with a repeating key before or after",
    "family": "6-transposition-then-tableau",
    "parent": "0026-double-keyed-columnar-then-tableau",
    "changed": "The public double-columnar searches stop at widths 2-6 or skip every pair with a 7 (Zekios, KryptosBot), and keithadler lists keyed double columnar as unsearched. Here one stage is a width-7 column shuffle in every one of its 5,040 orders and the other is a plain column shuffle at widths 2-30 or a column shuffle keyed by a puzzle word (repeated letters dropped, or kept with ties read left to right), in either order, with the exact crib test for a repeating key of length 1-26 on either side.",
    "hypothesis_expert": (
        "Type 2 of directions.md, the first open item of the prior-work database's seven-based gaps ('keyed double "
        "columnar transposition with one width of 7... KryptosBot's double-columnar run skipped every pair involving 5 or "
        "7, its register marks width 9 x width 7 NOT covered, Zekios stopped at 6 x 6, keithadler lists keyed double "
        "columnar as unsearched'). Evidence: the width-7 doublet column (0056; about p 0.02 after conditioning on six "
        "doublets, prior-work report) and KRYPTOS's seven letters (C8(a): KRYPTOS as a transposition key for K4, as for "
        "K3); C1(a) 'double matrixes'. Route: columnar encryption (write rows, read columns in sequence) twice, one stage "
        "of width 7 in all 5,040 reading sequences, the other a plain sequence at widths 2-30 read left-to-right or "
        "right-to-left (58) or a keyword sequence from data/vocabulary.txt, K1-K3 words of 3-20 letters and the C13/C14 "
        "words, read as true keywords (columns in alphabetical order of the key letters; issue #26 found 0006-0081 read the "
        "rank list as the sequence), once with repeated letters dropped and once on the whole word with ties left to right, "
        "deduplicated; the width-7 stage first or second. Key: periodic tableau key of period 1-26 after the moves (slot = landing place mod p) or before them "
        "(slot = place mod p), 8 classes of plain and cipher alphabet and Beaufort-or-not; live if no slot holds two "
        "different forced letters. Exact; ten shuffled coppers through the identical search. Left open: both stages with "
        "free orders above width 7 (9 x 7 has 1.8 billion pairs), autokey keys with these routes."
    ),
    "hypothesis_eli5": (
        "A column shuffle writes the message in rows under a key and reads the columns out in the key's order. Doing it "
        "twice with two keys is the classic double transposition. Five of K4's six doubled letters line up in one column "
        "when it is written in rows of seven, and the sculpture's name has seven letters, so one of the two shuffles may "
        "well be seven columns wide. Nobody has tried that combination in full. We take every possible order of seven "
        "columns, pair it with a second shuffle from the puzzle's words or a plain one, and ask whether a repeating "
        "secret word on the table could then give the copper's known letters."
    ),
    "prediction": (
        "No setting is live below period 20 beyond the rate on the shuffled coppers, and the count of live settings at "
        "each period 1-26 lies inside the control range, give or take the spread at 24-26. Zero candidates."
    ),
    "method": (
        "1. List the 5,040 reading sequences of seven columns and the second-stage sequences (plain 2-30, word keys both "
        "ways). 2. For each pair and each stage order, compose the two moves and skip repeats. 3. For each route, class "
        "and text, compute the key letter each known letter forces at its landing place. 4. For each period 1-26 and each "
        "key order, the period is live if no slot holds two different forced letters. 5. Count live settings per period "
        "on K4 and ten shuffled coppers. 6. List K4's live settings below period 20."
    ),
    "walkthrough": (
        "1. Write the message in rows of 7 under KRYPTOS. Read the columns in the alphabetical order of the key letters, K O P R S T Y, which is columns 0, 5, 3, 1, 6, 4, 2. 2. Place 22, the E of EAST, is in row 3 of column 0, the column read first, so it becomes letter 4. 3. Write that text in rows of 5 under ABSCI (ABSCISSA with its repeated letters dropped) and read columns A B C I S, that is 0, 1, 3, 4, 2. Letter 4 is in row 0, column 3; columns 0 and 1 hold 20 letters each, so it becomes letter 41. 4. The copper at 41 is J: a repeating key on the table must turn E into J there. Work out that key letter for all 24 known letters. 5. For a key of length p, two known letters whose landing places differ by a multiple of p share a key letter; if they need different ones, p is dead. 6. Repeat for all 5,040 orders of seven columns, every second shuffle, both stage orders, the key before or after, and ten scrambled coppers."
    ),
}

import random
from itertools import permutations
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.alphabets import numeric_order
from kryptos.ciphers import columnar_transposition_encrypt

N = 97
PMAX = 26
ALPH = {"std": STD, "kry": KRY}
N_CONTROLS = 10

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


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    places = sorted(known)
    pidx = [p - 1 for p in places]
    rng = random.Random(84)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    T = len(texts)
    classes = [(pa, ca, beau) for pa in ALPH for ca in ALPH for beau in (False, True)]
    CI = {an: [[{c: i for i, c in enumerate(ALPH[an])}[ch] for ch in t] for t in texts] for an in ALPH}
    PI = {an: [{c: i for i, c in enumerate(ALPH[an])}[known[p]] for p in places] for an in ALPH}
    # G[c][t][e][j]: key value forced by known letter e if it lands at j
    G = []
    for pa, ca, beau in classes:
        G.append([[[((CI[ca][t][j] + PI[pa][e]) if beau else (CI[ca][t][j] - PI[pa][e])) % 26 for j in range(N)]
                   for e in range(24)] for t in range(T)])
    pairsB = {p: slot_pairs([i % p for i in pidx]) for p in range(1, PMAX + 1)}
    assert keyword_sequence("KRYPTOS") == [0, 5, 3, 1, 6, 4, 2]
    assert plant_check(known)
    sevens = [where_columnar(seq) for seq in permutations(range(7))]
    stages = second_stages(list(ctx.vocabulary))
    stage_w = [where_columnar(seq) for _, seq in stages]

    live = {o: [[0] * (PMAX + 1) for _ in range(T)] for o in "AB"}
    k4_low, seen = [], set()
    n_routes = n_dupes = 0
    done_stages = 0
    stopped = False
    for si, (name, _) in enumerate(stages):
        if ctx.time_left() < 90:
            stopped = True
            break
        W2 = stage_w[si]
        for s7i, W7 in enumerate(sevens):
            for first in ("seven", "other"):
                if first == "seven":
                    wh = [W2[W7[i]] for i in range(N)]
                else:
                    wh = [W7[W2[i]] for i in range(N)]
                h = hash(tuple(wh))
                if h in seen:
                    n_dupes += 1
                    continue
                seen.add(h)
                n_routes += 1
                land = [wh[i] for i in pidx]
                pairsA = [None] + [slot_pairs([j % p for j in land]) for p in range(1, PMAX + 1)]
                for ci in range(8):
                    Gc = G[ci]
                    for t in range(T):
                        g = Gc[t]
                        f = [g[e][land[e]] for e in range(24)]
                        LA, LB = live["A"][t], live["B"][t]
                        for p in range(1, PMAX + 1):
                            for a, b in pairsA[p]:
                                if f[a] != f[b]:
                                    break
                            else:
                                LA[p] += 1
                                if t == 0 and p < 20:
                                    k4_low.append({"seven": s7i, "other": name, "first": first, "order": "A", "class": ci, "period": p})
                            for a, b in pairsB[p]:
                                if f[a] != f[b]:
                                    break
                            else:
                                LB[p] += 1
                                if t == 0 and p < 20:
                                    k4_low.append({"seven": s7i, "other": name, "first": first, "order": "B", "class": ci, "period": p})
        done_stages = si + 1
    outside = {o: [p for p in range(1, PMAX + 1) if not (min(live[o][t][p] for t in range(1, T)) <= live[o][0][p] <= max(live[o][t][p] for t in range(1, T)))] for o in "AB"}
    seq7 = list(permutations(range(7)))
    for h in k4_low:
        h["seven"] = list(seq7[h["seven"]])
        h["class"] = "{}/{}/{}".format(classes[h["class"]][0], classes[h["class"]][1], "beau" if classes[h["class"]][2] else "vig-var")
    bounds = {
        "family": "double columnar, one stage width 7 in all 5,040 orders, the other plain 2-30 or word-keyed; periodic key 1-26 before or after",
        "second_stages_total": len(stages), "second_stages_done": done_stages, "stopped_for_time": stopped,
        "distinct_routes": n_routes, "duplicates_skipped": n_dupes, "periods": [1, PMAX], "classes": 8,
        "k4_live_by_period": {o: live[o][0][1:] for o in "AB"},
        "controls_live_by_period_min": {o: [min(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in "AB"},
        "controls_live_by_period_max": {o: [max(live[o][t][p] for t in range(1, T)) for p in range(1, PMAX + 1)] for o in "AB"},
        "periods_outside_control_range": outside,
        "k4_live_below_20": k4_low[:40], "n_k4_live_below_20": len(k4_low),
        "controls_live_below_20": {o: [sum(live[o][t][p] for p in range(1, 20)) for t in range(1, T)] for o in "AB"},
        "controls": f"{N_CONTROLS} shuffled coppers (seed 84), identical search",
        "order_A": "moves, then key", "order_B": "key, then moves",
        "word_key_readings": "true keyword reading, repeated letters dropped, and on the whole word with ties left to right (issue #26)",
    }
    notes = (f"{n_routes:,} distinct double-columnar routes ({done_stages} of {len(stages)} second stages x 5,040 x 2 stage "
             f"orders; {n_dupes:,} repeats) x 8 classes x 2 key orders, periods 1-26. K4 live below 20: {len(k4_low)}; "
             f"controls: {bounds['controls_live_below_20']}. Outside the control range: {outside}."
             + (" Stopped for time." if stopped else ""))
    return {"candidates": [], "bounds": bounds, "notes": notes}


def plant_check(known):
    rng = random.Random(9)
    pt = [rng.choice(STD) for _ in range(N)]
    for p, c in known.items():
        pt[p - 1] = c
    W7 = where_columnar([3, 0, 6, 1, 5, 2, 4]); W2 = where_columnar(keyword_sequence("PALIMPSEST"))
    wh = [W2[W7[i]] for i in range(N)]
    moved = [""] * N
    for i in range(N):
        moved[wh[i]] = pt[i]
    key = [rng.randrange(26) for _ in range(11)]
    I = {c: i for i, c in enumerate(KRY)}
    ctxt = [KRY[(I[ch] + key[j % 11]) % 26] for j, ch in enumerate(moved)]
    slots = {}
    for p in known:
        j = wh[p - 1]
        v = (I[ctxt[j]] - I[known[p]]) % 26
        if slots.setdefault(j % 11, v) != v:
            return False
    return True


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    W7 = where_columnar(keyword_sequence("KRYPTOS"))
    W2 = where_columnar(keyword_sequence("ABSCISSA"))
    lines = ["first shuffle: rows of 7 under KRYPTOS, columns read K O P R S T Y (sequence 0 5 3 1 6 4 2);",
             "second shuffle: rows of 5 under ABSCI (ABSCISSA, repeats dropped), columns read A B C I S (0 1 3 4 2)", "",
             "place  letter  column  after KRYPTOS  after ABSCISSA  copper there"]
    for p in (22, 23, 24, 64, 65):
        a = W7[p - 1]; b = W2[a]
        lines.append(f"{p:>5}  {known[p]:>6}  {(p - 1) % 7:>6}  {a + 1:>14}  {b + 1:>14}  {ct[b]:>12}")
    return "\n".join(lines)
