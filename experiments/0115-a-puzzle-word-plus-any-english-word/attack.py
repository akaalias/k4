"""Experiment 0115. See program.md for the contract."""

EXPERIMENT = {
    "slug": "a-puzzle-word-plus-any-english-word",
    "title": "Two key words added, one from the puzzle and one from the whole dictionary (key word/s, layer two)",
    "family": "3-two-component-key",
    "parent": "0059-two-keywords-two-passes-k1-k3-word-alphabets",
    "changed": "0059 added two key words both taken from the puzzle. Here one word comes from the puzzle (the vocabulary, the words of K1-K3 and Sanborn's themes) and the other from the whole dictionary. Two words of lengths m and n make a key that repeats every lcm(m, n) letters, which can reach the lengths the cribs allow (KRYPTOS + ABSCISSA repeats every 56). Given the puzzle word and its starting place, the known letters force the other word at every slot it covers, so each case is a lookup among all rotations of dictionary words.",
    "hypothesis_expert": (
        "Scheidt: 'executed with the correct key word/s' (C5); K2 ends LAYER TWO; Vigenere applied twice with words of "
        "lengths m and n is one key k_i = a[(i + o1) mod m] + b[(i + o2) mod n] (0080 solved the free version for m, n <= 14 "
        "with no fit at 5+ checks, but long combined periods leave few checks, so only real words decide). Word a: every "
        "puzzle word of 2-30 letters (vocabulary.txt, the K1-K3 plaintext words, the extra theme words), every start o1. "
        "Word b: every dictionary word of 3-24 letters, every rotation (the start o2). For each table rule (Vigenere, "
        "Beaufort, variant; plain and cipher alphabets standard or KRYPTOS; key letters numbered on standard or KRYPTOS) the "
        "24 known letters give b's letter at slot i mod n; a clash rejects; a fully forced b is looked up in the set of "
        "rotations. A hit decrypts all 97 letters. Ten shuffled coppers."
    ),
    "hypothesis_eli5": (
        "Using the table twice, first with one secret word and then with another, is the same as using a single key made "
        "by adding the two words letter by letter. If one of the words is from the puzzle itself, like KRYPTOS or "
        "ABSCISSA, the 24 known letters tell us exactly what the other word must be, letter by letter. So we only have to "
        "look it up: is it an English word, read from some starting letter? We try every puzzle word and every "
        "dictionary word."
    ),
    "prediction": "No pair fits on K4; the shuffled coppers give no or almost no hits either. Zero candidates.",
    "method": (
        "1. Build the puzzle words and, for each length 3-24, the set of all rotations of dictionary words. "
        "2. For each rule, puzzle word and start, compute the key value forced at each known place minus the puzzle "
        "word's letter there. 3. For each length n, place those values at slots (place mod n); reject a clash; if every "
        "slot is fixed, look the word up. 4. Decrypt hits. 5. Repeat on ten shuffled coppers."
    ),
    "walkthrough": (
        "1. Take KRYPTOS as the first word, starting at its K at place 1, and the sculpture's alphabet with Vigenere. "
        "2. At place 22 the key must turn E into F: key value 1 on the sculpture's alphabet. KRYPTOS gives letter 22 mod 7 = 0, K = 0, so the second word's letter there is value 1, R. "
        "3. Do this at all 24 known places. For a second word of length 8, place 22 falls on slot 21 mod 8 = 5. "
        "4. If two known places ask different letters of one slot, no word of that length fits; if all 8 slots are fixed, look up the 8-letter string in every rotation of every 8-letter word. "
        "5. Repeat for every puzzle word and start, every length, rule, and on scrambled coppers."
    ),
}

import random
from pathlib import Path
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
N_CONTROLS = 10
ALPH = {"std": STD, "kry": KRY}
ROOT = Path(__file__).resolve().parent
if not (ROOT / "kryptos").exists():
    ROOT = Path.cwd()
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
EXTRA = ["EGYPT", "CAIRO", "LUXOR", "WALL", "NOVEMBER", "MESSAGE", "DELIVER", "DELIVERING", "TRANSMIT", "LAYERTWO",
         "WONDERFULTHINGS", "BERLINWALL", "WELTZEITUHR", "ALEXANDERPLATZ", "SHADOWFORCES", "LUCIDMEMORY"]


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    places = sorted(known)
    pidx = [p - 1 for p in places]
    puzzle = sorted({w for w in SPACED.split() if len(w) >= 2} | {w for w in ctx.vocabulary if 2 <= len(w) <= 30} | set(EXTRA))
    words = [w.strip().upper() for w in (ROOT / "kryptos" / "data" / "words.txt").read_text().split()]
    rots = {}
    for w in words:
        if 3 <= len(w) <= 24 and w.isalpha():
            s = rots.setdefault(len(w), {})
            for r in range(len(w)):
                s.setdefault(w[r:] + w[:r], (w, r))
    rng = random.Random(115)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    rules = [(m, pa, ca, ka) for m in ("vig", "beau", "var") for pa in ALPH for ca in ALPH for ka in ALPH]
    hits = [[] for _ in texts]
    fixed_cases = [0] * len(texts)
    n_cases = 0
    for t, txt in enumerate(texts):
        for mode, pa, ca, ka in rules:
            PI = {c: i for i, c in enumerate(ALPH[pa])}; CI = {c: i for i, c in enumerate(ALPH[ca])}; KA = ALPH[ka]
            KI = {c: i for i, c in enumerate(KA)}
            K = []
            for q in places:
                c, p = CI[txt[q - 1]], PI[known[q]]
                K.append({"vig": (c - p) % 26, "beau": (c + p) % 26, "var": (p - c) % 26}[mode])
            for w1 in puzzle:
                m = len(w1); a = [KI[x] for x in w1]
                for o1 in range(m):
                    b = [(K[e] - a[(i + o1) % m]) % 26 for e, i in enumerate(pidx)]
                    for n in range(3, 25):
                        n_cases += t == 0
                        slot = [None] * n
                        ok = True
                        for e, i in enumerate(pidx):
                            s = i % n
                            if slot[s] is None:
                                slot[s] = b[e]
                            elif slot[s] != b[e]:
                                ok = False; break
                        if not ok or None in slot:
                            continue
                        fixed_cases[t] += 1
                        key2 = "".join(KA[v] for v in slot)
                        hit = rots.get(n, {}).get(key2)
                        if hit:
                            hits[t].append({"rule": f"{mode}/{pa}/{ca}/{ka}", "word1": w1, "start1": o1, "word2": hit[0], "rotation2": hit[1], "n": n, "key2": key2})
    cands = []
    for h in hits[0]:
        mode, pa, ca, ka = h["rule"].split("/")
        PI = ALPH[pa]; CI = {c: i for i, c in enumerate(ALPH[ca])}; KI = {c: i for i, c in enumerate(ALPH[ka])}
        w1, o1, key2, n = h["word1"], h["start1"], h["key2"], h["n"]
        pt = []
        for i in range(N):
            k = (KI[w1[(i + o1) % len(w1)]] + KI[key2[i % n]]) % 26
            c = CI[ct[i]]
            v = {"vig": (c - k) % 26, "beau": (k - c) % 26, "var": (c + k) % 26}[mode]
            pt.append(PI[v])
        cands.append({"plaintext": "".join(pt), "key": f"{w1} from {o1} + {h['word2']} rotated {h['rotation2']}, {h['rule']}"})
    bounds = {"family": "sum of a puzzle word and a dictionary word as the key",
              "puzzle_words": len(puzzle), "dictionary_rotations_by_length": {n: len(v) for n, v in sorted(rots.items())},
              "rules": len(rules), "cases_per_text": n_cases, "fully_forced_cases_k4": fixed_cases[0], "fully_forced_cases_controls": fixed_cases[1:],
              "k4_hits": hits[0][:20], "n_k4_hits": len(hits[0]), "controls_hits": [len(h) for h in hits[1:]],
              "controls": f"{N_CONTROLS} shuffled coppers (seed 115), identical search"}
    notes = (f"{len(puzzle)} puzzle words x starts x lengths 3-24 x {len(rules)} rules = {n_cases:,} cases per text; fully forced "
             f"second words: K4 {fixed_cases[0]:,}, controls {fixed_cases[1:]}. Dictionary hits: K4 {len(hits[0])}, controls "
             f"{[len(h) for h in hits[1:]]}.")
    return {"candidates": cands, "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    I = {c: i for i, c in enumerate(KRY)}
    w1 = "KRYPTOS"
    lines = ["first word KRYPTOS from its K at place 1; sculpture's alphabet, Vigenere; second word of length 8", "",
             "place  known  carved  key value  KRYPTOS letter  second word's letter  slot (mod 8)"]
    slots = {}
    for q in sorted(known):
        k = (I[ct[q - 1]] - I[known[q]]) % 26
        a = w1[(q - 1) % 7]
        b = KRY[(k - I[a]) % 26]
        slots.setdefault((q - 1) % 8, set()).add(b)
        if q in (22, 23, 24, 25, 30, 31, 64):
            lines.append(f"{q:>5}  {known[q]:>5}  {ct[q - 1]:>6}  {k:>9}  {a:>14}  {b:>20}  {(q - 1) % 8:>12}")
    clash = [s for s, v in slots.items() if len(v) > 1]
    lines += ["", f"slots asked for two different letters: {sorted(clash)}" if clash else "no clash: look up the 8 letters"]
    return "\n".join(lines)
