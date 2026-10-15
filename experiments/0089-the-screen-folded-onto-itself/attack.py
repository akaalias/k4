"""Experiment 0089. See program.md for the contract."""

EXPERIMENT = {
    "slug": "the-screen-folded-onto-itself",
    "title": "The key letter behind each K4 letter: K4's carved lines laid over the tableau plate, straight or folded",
    "family": "4-visual-systems",
    "parent": "0017-running-key-from-the-sculpture-itself",
    "changed": "0017 slid the sculpture's texts along K4 as one long string. Here the key comes from the screen's geometry: each K4 letter sits at a carved line and column, and its key letter is the letter at the same line and column of another plate, or at the mirrored column when the screen is folded at its centre (the tableau reads correctly only from the back). Plate lines have different lengths, so these keys are not windows of 0017's strings.",
    "hypothesis_expert": (
        "Type 3 of directions.md: a key read off the sculpture by position. 01-facts.md: the screen's left half carries "
        "the ciphertext and the right half the tableau, each on two plates of 14 lines; the letters are cut through and "
        "the CIA says the tableau 'is intentionally flipped so it can only be read from the back'. K4 fills the last four "
        "cells of line 11 of the lower-left plate and lines 12-14. C6(a) ('the keys were concealed at the sculpture'), "
        "C9(b) (the tableau letters are the key), C11a, Sanborn's 'visual systems' (family 4). Key letter for K4 at plate "
        "line i, column c: the letter of a source plate at line i + d, column c + s (straight) or column 32 - c + s "
        "(folded), sources the two tableau plates (header, 26 rows with labels and the extra L, footer) and the two "
        "cipher plates, d over every window of four lines, s = -4..4, Vigenere, Beaufort and variant Beaufort with key "
        "and text numbered on the standard or KRYPTOS alphabet (12 conventions). Exact: a running key leaves no free "
        "letter, so the reading must hit all 24 known letters. Ten shuffled coppers set the chance level of the best hit count."
    ),
    "hypothesis_eli5": (
        "On the sculpture the secret text and the big table of alphabets stand side by side on one copper screen, and "
        "the letters are cut right through it. If you fold the screen in your mind, or look at it from behind, every "
        "letter of the fourth message lands on a letter of the table. That letter could be its key. We lay K4's four "
        "carved lines over every four lines of the table and of the other secret texts, straight across and folded, "
        "slide them a few columns either way, and check whether any lining-up gives all 24 known letters."
    ),
    "prediction": (
        "No overlay hits all 24 known letters; the best hit count on K4 lies inside the range of the ten shuffled coppers "
        "(about 6-7 of 24). Zero candidates."
    ),
    "method": (
        "1. Lay out the four plates as carved (01-facts.md and the tableau rows with the extra L in row N). "
        "2. Give each K4 letter its plate line and column. "
        "3. For each source plate, line offset, straight or folded, column shift and convention, read the key letter "
        "under each known place and count the places where it turns the known letter into the carved letter. "
        "4. Do the same on ten shuffled coppers. 5. Decrypt and return any overlay that hits all 24."
    ),
    "walkthrough": (
        "1. K4's O, B, K, R are columns 28-31 of line 11 of the lower-left plate; places 5-35 are line 12, 36-66 line 13, 67-97 line 14. "
        "2. The lower-right plate holds tableau rows N to Z and the footer; its line 12 is row Y. "
        "3. Place 22 is E on line 12, column 18. Straight across, row Y (label first) has key letter Y's 18th cell. "
        "4. Folded at the centre, column 18 lands on column 32 - 18 = 14 of row Y. "
        "5. With the sculpture's alphabet and Vigenere, E plus the key letter must give the carved F; count a hit if it does. "
        "6. Repeat for all 24 known places, every window of four lines on every plate, both ways, shifts -4 to 4 and 12 conventions."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.ciphers import tableau_rows

N_CONTROLS = 10

UPPER_LEFT = """EMUFPHZLRFAXYUSDJKZLDKRNSHGNFIVJ
YQTQUXQBQVYUVLLTREVJYQTMKYRDMFD
VFPJUDEEHZWETZYVGWHKKQETGFQJNCE
GGWHKK?DQMCPFQZDQMMIAGPFXHQRLG
TIMVMZJANQLVKQEDAGDVFRPJUNGEUNA
QZGZLECGYUXUEENJTBJLBQCRTBJDFHRR
YIZETKZEMVDUFKSJHKFWHKUWQLSZFTI
HHDDDUVH?DWKBFUFPWNTDFIYCUQZERE
EVLDKFEZMOQQJLTTUGSYQPFEUNLAVIDX
FLGGTEZ?FKZBSFDQVGOGIPUFXHHDRKF
FHQNTGPUAECNUVPDJMQCLQUMUNEDFQ
ELZZVRRGKFFVOEEXBDMVPNFQXEZLGRE
DNQFMPNZGLFLPMRJQYALMGNUVPDXVKP
DQUMEBEDMHDAFMJGZNUPLGEWJLLAETG""".split()
LOWER_LEFT = """ENDYAHROHNLSRHEOCPTEOIBIDYSHNAIA
CHTNREYULDSLLSLLNOHSNOSMRWXMNE
TPRNGATIHNRARPESLNNELEBLPIIACAE
WMTWNDITEENRAHCTENEUDRETNHAEOE
TFOLSEDTIWENHAEIOYTEYQHEENCTAYCR
EIFTBRSPAMHHEWENATAMATEGYEERLB
TEEFOASFIOTUETUAEOTOARMAEERTNRTI
BSEDDNIAAHTTMSTEWPIEROAGRIEWFEB
AECTDDHILCEIHSITEGOEAOSDDRYDLORIT
RKLMLEHAGTDHARDPNEOHMGFMFEUHE
ECDMRIPFEIMEHNLSSTTRTVDOHW?OBKR
UOXOGHULBSOLIFBBWFLRVQQPRNGKSSO
TWTQSJQSSEKZZWATJKLUDIAWINFBNYP
VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR""".split()


def tableau_plates():
    rows = [STD[i] + r for i, r in enumerate(tableau_rows(carved=True))]
    head = " " + STD + STD[:4]
    lines = [head] + rows + [head]
    return lines[:14], lines[14:]


def k4_cells():
    """Plate line (0-based, on the lower-left plate) and column (1-based) of each K4 place 1..97."""
    cells = []
    for p in range(1, 98):
        if p <= 4:
            cells.append((10, 27 + p))
        else:
            q = p - 5
            cells.append((11 + q // 31, q % 31 + 1))
    return cells


def conventions():
    out = []
    for mode in ("vig", "beau", "varb"):
        for ka in ("std", "kry"):
            for ta in ("std", "kry"):
                out.append((mode, ka, ta))
    return out


def enc(mode, p, k):
    if mode == "vig":
        return (p + k) % 26
    if mode == "beau":
        return (k - p) % 26
    return (p - k) % 26


def dec(mode, c, k):
    if mode == "vig":
        return (c - k) % 26
    if mode == "beau":
        return (k - c) % 26
    return (c + k) % 26


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    assert "".join(LOWER_LEFT[10][27:]) + "".join(LOWER_LEFT[11:]) == ct
    cells = k4_cells()
    tr_up, tr_low = tableau_plates()
    sources = {"tableau": tr_up + tr_low, "cipher": UPPER_LEFT + LOWER_LEFT}
    # each source as 28 lines; K4's four lines are lines 24..27 of the left column (lower-left lines 10..13)
    A = {"std": {c: i for i, c in enumerate(STD)}, "kry": {c: i for i, c in enumerate(KRY)}}
    AL = {"std": STD, "kry": KRY}
    places = sorted(known)
    rng = random.Random(89)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    convs = conventions()
    best = [0] * len(texts)
    hist = [dict() for _ in texts]
    k4_top, full = [], []
    natural = {}
    n_trials = 0
    for sname, lines in sources.items():
        for d0 in range(0, 25):                     # source window starts at source line d0 (K4's line 10 -> d0)
            for fold in (False, True):
                for s in range(-4, 5):
                    keys = []
                    ok = True
                    for p in range(1, 98):
                        i, c = cells[p - 1]
                        li = d0 + (i - 10)
                        col = (32 - c if fold else c) + s
                        line = lines[li]
                        keys.append(line[col - 1] if 1 <= col <= len(line) and line[col - 1].isalpha() else None)
                    for conv in convs:
                        mode, ka, ta = conv
                        n_trials += 1
                        for t, txt in enumerate(texts):
                            h = 0
                            for p in places:
                                k = keys[p - 1]
                                if k is not None and AL[ta][enc(mode, A[ta][known[p]], A[ka][k])] == txt[p - 1]:
                                    h += 1
                            hist[t][h] = hist[t].get(h, 0) + 1
                            best[t] = max(best[t], h)
                            if t == 0:
                                tag = {"source": sname, "start_line": d0 + 1, "folded": fold, "shift": s,
                                       "convention": "/".join(conv), "hits": h}
                                k4_top.append(tag)
                                natural_win = (sname == "tableau" and d0 == 24) or (sname == "cipher" and d0 == 10)
                                if natural_win and s == 0:
                                    natural.setdefault(f"{sname} {'folded' if fold else 'straight'}", []).append(h)
                                if h == 24:
                                    pt = "".join(AL[ta][dec(mode, A[ta][ct[j]], A[ka][keys[j]])] if keys[j] else "?"
                                                 for j in range(97))
                                    full.append({**tag, "plaintext": pt})
    k4_top.sort(key=lambda r: -r["hits"])
    ctl = best[1:]
    bounds = {
        "family": "running key read by position off the carved screen",
        "sources": "tableau plates (header, 26 labelled rows, extra L in row N, footer) and cipher plates, 28 lines each",
        "line_windows": 25, "straight_or_folded": 2, "column_shifts": [-4, 4], "conventions": len(convs),
        "trials": n_trials, "k4_best_hits": best[0], "controls_best_hits": ctl,
        "k4_hit_histogram": dict(sorted(hist[0].items())),
        "natural_alignment_hits": {k: max(v) for k, v in natural.items()},
        "k4_top": k4_top[:15], "full_24": len(full),
        "controls": f"{N_CONTROLS} shuffled coppers (seed 89), identical search",
    }
    notes = (f"{n_trials:,} overlays. K4 best {best[0]}/24; controls best {min(ctl)}-{max(ctl)}. "
             f"Overlays hitting all 24: {len(full)}. Natural alignment (lower plates, no shift), best hits: "
             f"{ {k: max(v) for k, v in natural.items()} }.")
    cands = [{"plaintext": f["plaintext"], "key": f"screen overlay {f['source']} line {f['start_line']} "
              f"{'folded' if f['folded'] else 'straight'} shift {f['shift']} {f['convention']}"} for f in full]
    return {"candidates": cands, "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    _, low = tableau_plates()
    cells = k4_cells()
    lines = ["K4 over the lower-right tableau plate (rows N-Z, footer), natural lines, no shift",
             "sculpture's alphabet, Vigenere: carved = known + key", "",
             "place  known  carved  line  col  straight key  ->  folded key  ->"]
    I = {c: i for i, c in enumerate(KRY)}
    for p in (22, 23, 24, 25, 64, 65, 74):
        i, c = cells[p - 1]
        row = low[i]
        ks, kf = row[c - 1], row[32 - c - 1]
        es = KRY[(I[known[p]] + I[ks]) % 26] if ks.isalpha() else "?"
        ef = KRY[(I[known[p]] + I[kf]) % 26] if kf.isalpha() else "?"
        lines.append(f"{p:>5}  {known[p]:>5}  {ct[p - 1]:>6}  {i + 1:>4}  {c:>3}  {ks:>12}  {es}  {kf:>10}  {ef}")
    return "\n".join(lines)
