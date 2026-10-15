"""Experiment 0095. See program.md for the contract."""

EXPERIMENT = {
    "slug": "riddle-words-dragged-at-the-live-periods",
    "title": "Words a riddle would use, dragged across K4 at every repeating-key length the known letters allow",
    "family": "1-keyed-periodic",
    "parent": "0001-crib-consistent-periods",
    "changed": "Earlier periodic experiments at the live lengths (27-29 and 53 and up) filled the free key letters by climbing toward English, which cannot beat its own controls. Here nothing is climbed: each word of a fixed riddle lexicon (spelled numbers, units, compass words, the puzzle's own words, Sanborn's themes) is placed at every position, and a placement counts only if the key letters it forces agree with the ones the known letters already fix. Random letter strings of the same lengths are the control.",
    "hypothesis_expert": (
        "Type 8 of directions.md, 'a plaintext that is itself a riddle'. K2 spells out its coordinates (THIRTY EIGHT "
        "DEGREES FIFTY SEVEN MINUTES...) and ends LAYER TWO (01-facts.md); Sanborn 2025: the plaintext joins the 1986 "
        "Egypt trip, the 1989 Wall and 'delivering a message' (site_texts.json); issue #11 asks for credit for spelled "
        "numbers and the puzzle's words. Classical probable-word attack: for every single-alphabet periodic key the cribs "
        "allow (each of 8 tableau classes, every consistent period 27-96), each lexicon word w at every start x forces key "
        "values at slots (x + i) mod p; it is consistent if they agree with the slots fixed by the 24 known letters; "
        "placements overlapping the known stretches are skipped. The number of such agreements is its check count. Null: 40 random "
        "strings per word length on the same text and keys. A real word that is the plaintext would show up as a "
        "placement with many checks, or as an excess of 3+-check placements over the decoys."
    ),
    "hypothesis_eli5": (
        "If the message is a riddle like K2, which spelled out numbers and directions, it probably uses words such as "
        "THIRTY, DEGREES, NORTH or SHADOW. For every length of repeating secret word that fits the 24 known letters, "
        "we slide each such word along the message and ask whether it agrees with the key letters the known letters "
        "already fix. Random strings of letters, slid the same way, show how often agreement happens by luck."
    ),
    "prediction": (
        "Lexicon words reach consistent placements with three or more checks at the same rate as random strings of the "
        "same length (within the decoys' spread), and no placement has five or more checks. Zero candidates."
    ),
    "method": (
        "1. For each class and period 27-96, test crib consistency and keep the consistent pairs with their fixed key slots. "
        "2. For each lexicon word and start clear of the known stretches, count agreements with fixed slots; reject on "
        "any disagreement. 3. Do the same for 40 random strings per length. 4. Compare counts of placements with 2, 3 and "
        "4+ checks between words and decoys, per word length. 5. List the real-word placements with 3 or more checks."
    ),
    "walkthrough": (
        "1. Take the sculpture's alphabet, Vigenere, and a key of length 60; the known letters fix the key letters at slots 21-33 and 3-13. "
        "2. Place the word DEGREES so that it starts at place 80. "
        "3. Its letters fall on slots 19-25 (place mod 60); slots 21-25 are already fixed by EASTNORTHEAST's letters at places 22-26. "
        "4. For each of those, the key letter that turns the word's letter into the carved letter must equal the fixed one. "
        "5. All agree: a consistent placement with that many checks. One disagreement: rejected. "
        "6. Repeat for every word, start, period and table rule, then for random strings."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
ALPH = {"std": STD, "kry": KRY}
N_DECOYS = 40

NUMBERS = ("ZERO ONE TWO THREE FOUR FIVE SIX SEVEN EIGHT NINE TEN ELEVEN TWELVE THIRTEEN FOURTEEN FIFTEEN SIXTEEN "
           "SEVENTEEN EIGHTEEN NINETEEN TWENTY THIRTY FORTY FIFTY SIXTY SEVENTY EIGHTY NINETY HUNDRED THOUSAND "
           "FIRST SECOND THIRD FOURTH FIFTH NINETEENEIGHTYSIX NINETEENEIGHTYNINE").split()
UNITS = "DEGREES DEGREE MINUTES SECONDS POINT FEET YARDS PACES METERS MILES HOURS OCLOCK".split()
COMPASS = ("NORTH SOUTH EAST WEST NORTHEAST NORTHWEST SOUTHEAST SOUTHWEST NORTHNORTHEAST EASTSOUTHEAST BEARING "
           "COMPASS LODESTONE MAGNETIC").split()
THEMES = ("EGYPT CAIRO GIZA LUXOR PYRAMID SPHINX TOMB WALL BERLIN CLOCK WORLDCLOCK ALEXANDERPLATZ MESSAGE DELIVER "
          "DELIVERING DELIVERED NOVEMBER NINTH CHECKPOINT CHARLIE BRANDENBURG LAYER SHADOW SHADOWS INVISIBLE "
          "POSITION LOCATION BURIED UNDERGROUND SECRET HIDDEN AGENT LANGLEY KRYPTOS PALIMPSEST ABSCISSA "
          "ILLUSION IQLUSION LIGHT DARKNESS CANDLE CHAMBER PASSAGE DOORWAY").split()


def lexicon():
    words = []
    for w in NUMBERS + UNITS + COMPASS + THEMES:
        if len(w) >= 5 and w not in words:
            words.append(w)
    return words


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    places = sorted(known)
    words = lexicon()
    rng = random.Random(95)
    lengths = sorted({len(w) for w in words})
    decoys = {L: ["".join(rng.choice(STD) for _ in range(L)) for _ in range(N_DECOYS)] for L in lengths}
    classes = [(pa, ca, beau) for pa in ALPH for ca in ALPH for beau in (False, True)]
    keys = []
    for pa, ca, beau in classes:
        PI = {c: i for i, c in enumerate(ALPH[pa])}; CI = {c: i for i, c in enumerate(ALPH[ca])}
        C = [CI[c] for c in ct]
        val = (lambda j, ch: (C[j] + PI[ch]) % 26) if beau else (lambda j, ch: (C[j] - PI[ch]) % 26)
        for p in range(27, N):
            slots, ok = {}, True
            for q in places:
                v = val(q - 1, known[q])
                if slots.setdefault((q - 1) % p, v) != v:
                    ok = False; break
            if ok:
                keys.append(((pa, ca, beau), p, slots, val))
    kn0 = {q - 1: known[q] for q in places}

    def drag(word):
        L = len(word)
        hist = {}
        hits = []
        for cls, p, slots, val in keys:
            for x in range(N - L + 1):
                checks = 0
                local = {}
                ok = True
                for i, ch in enumerate(word):
                    j = x + i
                    if j in kn0:                    # the known stretches are not dragged over
                        ok = False; break
                    v = val(j, ch); s = j % p
                    if s in slots:
                        if slots[s] != v:
                            ok = False; break
                        checks += 1
                    elif s in local:
                        if local[s] != v:
                            ok = False; break
                        checks += 1
                    else:
                        local[s] = v
                if ok:
                    hist[checks] = hist.get(checks, 0) + 1
                    if checks >= 3:
                        hits.append({"class": f"{cls[0]}/{cls[1]}/{'beau' if cls[2] else 'vig-var'}", "period": p,
                                     "start": x + 1, "checks": checks})
        return hist, hits

    real = {}
    for w in words:
        h, hits = drag(w)
        real[w] = {"hist": h, "hits": hits}
    dec = {L: [drag(d)[0] for d in decoys[L]] for L in lengths}
    ge = lambda h, c: sum(v for k, v in h.items() if k >= c)
    by_len = {}
    excess = []
    for L in lengths:
        ws = [w for w in words if len(w) == L]
        for c in (2, 3, 4, 5):
            rv = [ge(real[w]["hist"], c) for w in ws]
            dv = sorted(ge(h, c) for h in dec[L])
            by_len.setdefault(L, {})[c] = {"words_mean": round(sum(rv) / len(rv), 2), "decoys_mean": round(sum(dv) / len(dv), 2),
                                           "decoys_95th": dv[int(0.95 * (len(dv) - 1))], "decoys_max": dv[-1]}
            for w, v in zip(ws, rv):
                if v > dv[-1] and c >= 3:
                    excess.append({"word": w, "checks_at_least": c, "placements": v, "decoys_max": dv[-1]})
    top = sorted(((w, h) for w in words for h in real[w]["hits"]), key=lambda x: -x[1]["checks"])[:30]
    max_real = max((k for w in words for k in real[w]["hist"]), default=0)
    max_dec = max((k for L in lengths for h in dec[L] for k in h), default=0)
    bounds = {
        "family": "probable-word drag under every crib-consistent single-alphabet periodic key",
        "classes": 8, "consistent_class_period_pairs": len(keys),
        "periods_by_class": {f"{c[0]}/{c[1]}/{'beau' if c[2] else 'vig-var'}": [p for cc, p, _, _ in keys if cc == c] for c in classes},
        "lexicon_words": len(words), "lexicon": words, "decoys_per_length": N_DECOYS,
        "by_length_and_checks": by_len, "words_above_all_decoys": excess,
        "max_checks_real": max_real, "max_checks_decoys": max_dec,
        "top_real_placements": [{"word": w, **h} for w, h in top],
        "controls": f"{N_DECOYS} random strings per word length (seed 95), same text, keys and drag",
    }
    notes = (f"{len(words)} words x {len(keys)} consistent (class, period) keys, every start. Most checks: real words "
             f"{max_real}, decoys {max_dec}. Words above every decoy of their length at 3+ checks: "
             f"{[e['word'] for e in excess if e['checks_at_least'] == 3]}; at 4+: {[e['word'] for e in excess if e['checks_at_least'] == 4]}.")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    I = {c: i for i, c in enumerate(KRY)}
    p = 60
    slots = {}
    for q in sorted(known):
        slots[(q - 1) % p] = (I[ct[q - 1]] - I[known[q]]) % 26
    word, x = "DEGREES", 79
    lines = [f"sculpture's alphabet, Vigenere, key length {p}: slots fixed by the known letters: {sorted(slots)}", "",
             f"{word} starting at place {x + 1}", "place  letter  copper  slot  needed  fixed"]
    for i, ch in enumerate(word):
        j = x + i
        need = (I[ct[j]] - I[ch]) % 26
        fixed = slots.get(j % p)
        lines.append(f"{j + 1:>5}  {ch:>6}  {ct[j]:>6}  {j % p:>4}  {need:>6}  {'' if fixed is None else fixed:>5}")
    return "\n".join(lines)
