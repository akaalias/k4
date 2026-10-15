"""Experiment 0072. See program.md for the contract."""

EXPERIMENT = {
    "slug": "compass-points-and-the-point-letter",
    "title": "The 32 points of the compass and the words of Sanborn's last hint as alphabets",
    "family": "1-keyed-periodic",
    "parent": "0053-periodic-tableau-k1-k3-word-alphabets",
    "changed": "Sanborn's 2025 letter marks 'what's the point?' as a clue, and he chose the word 'directions' on purpose. The vocabulary held only the four cardinal points and NORTHEAST. Here the alphabets are rebuilt from all 32 compass points (EASTNORTHEAST, NORTHBYEAST and the rest) and from the hint's words (POINT, POWER, RESIDES, WITHOUT, DIRECTIONS, BEARING), and tested with a repeating key, the self-feeding autokey, and both together.",
    "hypothesis_expert": (
        "Family 1 re-entered with a new key source: C15(a) and (e) (open letter, sources/openletter-2025.txt: "
        "'If they don't, then (CLUE) what's the point? Power resides with a secret, not without it') and "
        "C16 ('the word directions is, I use intentionally', 2010). EASTNORTHEAST is itself a compass point, "
        "so the boxing of the 32 points is a natural key source for a man who chose it as plaintext. Words: the "
        "32 point names (NORTH, NORTHBYEAST, NORTHNORTHEAST, NORTHEASTBYNORTH, NORTHEAST, ... in the "
        "traditional boxing), SOUTHEAST, SOUTHWEST, NORTHWEST, POINT, POWER, RESIDES, WITHOUT, DIRECTION, "
        "DIRECTIONS, BEARING, TRUENORTH, ORIENTATION, OFFSET, COMPASSROSE, WINDROSE, AZIMUTH, DECLINATION; "
        "keyword-mixed alphabets, duplicates removed, plus standard and KRYPTOS. Systems: (1) periodic key, "
        "periods 1-52, every plain-cipher pair, Vigenere or Beaufort, exact crib consistency, fragments at "
        "periods up to 29 matched against the vocabulary and K1-K3; (2) ciphertext autokey with a constant "
        "shift, every lag, both alphabets the same word alphabet, key letter on it or on the standard; (3) "
        "the 0066 form, autokey plus a periodic key up to 26, same alphabets. Ten shuffled coppers through "
        "the same sweeps."
    ),
    "hypothesis_eli5": (
        "In his last open letter Sanborn wrote 'what's the point?' and marked it as a clue, and years earlier "
        "he said he used the word 'directions' on purpose. The known letters already say EAST NORTHEAST, "
        "which is one of the 32 points of a compass. We build the table's scrambled alphabets from all 32 "
        "point names and from the words of that letter, and try the simplest ciphers with them. Scrambled "
        "coppers get the same treatment, so we can tell a real fit from luck."
    ),
    "prediction": (
        "No pair makes a periodic key of period 24 or less consistent; 25-26 survive at the shuffled-copper "
        "rate; no fragment at periods up to 29 matches a word; neither autokey form has a survivor with three "
        "or more redundant checks beyond the controls. Zero candidates pass."
    ),
    "method": (
        "1. Build the alphabets from the compass and letter words. 2. For each pair and mode, compute the key "
        "value each known letter forces and check slot agreement at every period up to 52; keep fragments. "
        "3. For each word alphabet, lag and key alphabet, check the autokey residuals, alone and with a "
        "periodic key up to 26. 4. Repeat on ten shuffled coppers. 5. Match fragments against words."
    ),
    "walkthrough": (
        "1. Build the alphabet from EASTNORTHEAST: EASTNORHBCDFGIJKLMPQUVWXYZ, counted from E = 0. 2. Use it "
        "for message and carved letters, Vigenere, with a 7-letter word. 3. Place 22: known E is 0, carved F "
        "is 11; key 11, F, in slot 0. 4. Place 29: known T is 3, carved R is 6; key 3, T, also slot 0. 5. F "
        "and T disagree, so this alphabet with a 7-letter word is dead. 6. Repeat for every pair, word length "
        "and lag."
    ),
}

import random
from kryptos.alphabets import keyword_mixed
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY, load_k1, load_k2, load_k3

N = 97
PMAX = 52
POINTS = ["NORTH", "NORTHBYEAST", "NORTHNORTHEAST", "NORTHEASTBYNORTH", "NORTHEAST", "NORTHEASTBYEAST", "EASTNORTHEAST", "EASTBYNORTH",
          "EAST", "EASTBYSOUTH", "EASTSOUTHEAST", "SOUTHEASTBYEAST", "SOUTHEAST", "SOUTHEASTBYSOUTH", "SOUTHSOUTHEAST", "SOUTHBYEAST",
          "SOUTH", "SOUTHBYWEST", "SOUTHSOUTHWEST", "SOUTHWESTBYSOUTH", "SOUTHWEST", "SOUTHWESTBYWEST", "WESTSOUTHWEST", "WESTBYSOUTH",
          "WEST", "WESTBYNORTH", "WESTNORTHWEST", "NORTHWESTBYWEST", "NORTHWEST", "NORTHWESTBYNORTH", "NORTHNORTHWEST", "NORTHBYWEST"]
OTHER = ["POINT", "POWER", "RESIDES", "WITHOUT", "DIRECTION", "DIRECTIONS", "BEARING", "TRUENORTH", "ORIENTATION", "OFFSET",
         "COMPASSROSE", "WINDROSE", "AZIMUTH", "DECLINATION", "POWERRESIDESWITHASECRET", "WHATSTHEPOINT"]


def letters(s):
    return "".join(c for c in s.upper() if "A" <= c <= "Z")


def pool():
    out = {"std": STD, "kry": KRY}
    seen = {STD, KRY}
    for w in POINTS + OTHER:
        a = keyword_mixed(w)
        if a not in seen:
            seen.add(a); out[w] = a
    return out


def periodic(ct, items, alphas, ctx, deadline, collect):
    per, frags = {}, []
    names = list(alphas)
    for pn in names:
        pa = alphas[pn]; PI = {c: i for i, c in enumerate(pa)}
        for cn in names:
            ca = alphas[cn]; CI = {c: i for i, c in enumerate(ca)}
            for mode in ("vig", "beau"):
                T = [((CI[ct[pos - 1]] - PI[p]) if mode == "vig" else (CI[ct[pos - 1]] + PI[p])) % 26 for pos, p in items]
                for P in range(1, PMAX + 1):
                    slot = {}; ok = True
                    for (pos, _), t in zip(items, T):
                        if slot.setdefault((pos - 1) % P, t) != t:
                            ok = False; break
                    if ok:
                        per[P] = per.get(P, 0) + 1
                        if collect and P <= 29:
                            frags.append((pn, cn, mode, P, "".join(ca[slot[k]] if k in slot else "." for k in range(P)),
                                          "".join(pa[slot[k]] if k in slot else "." for k in range(P))))
        if ctx.time_left() < deadline:
            break
    return per, frags


def autokeys(ct, items, alphas):
    plain, withp = {}, {}
    for n, A in alphas.items():
        I = {c: i for i, c in enumerate(A)}
        for kname, K in (("same", A), ("std", STD)):
            KI = {c: i for i, c in enumerate(K)}
            for mode in ("vig", "beau"):
                T = [((I[ct[pos - 1]] - I[p]) if mode == "vig" else (I[ct[pos - 1]] + I[p])) % 26 for pos, p in items]
                for s in (1, -1):
                    for L in range(1, 97):
                        d = [(pos - 1, (t - s * KI[ct[pos - 1 - L]]) % 26) for (pos, _), t in zip(items, T) if pos - 1 - L >= 0]
                        if len(d) < 2:
                            continue
                        if len({v for _, v in d}) == 1:
                            c = min(len(d) - 1, 5); plain[c] = plain.get(c, 0) + 1
                        for P in range(2, 27):
                            slot = {}; ok = True
                            for i, v in d:
                                if slot.setdefault(i % P, v) != v:
                                    ok = False; break
                            if ok and len(d) - len(slot) >= 1:
                                c = min(len(d) - len(slot), 5); withp[c] = withp.get(c, 0) + 1
    return plain, withp


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    items = sorted(known.items())
    alphas = pool()
    t0 = ctx.time_left()
    per, frags = periodic(ct, items, alphas, ctx, t0 * 0.7, True)
    plain, withp = autokeys(ct, items, alphas)
    rng = random.Random(72)
    ctrl = []
    for _ in range(10):
        sh = list(ct); rng.shuffle(sh); sh = "".join(sh)
        p2, _ = periodic(sh, items, alphas, ctx, 30, False)
        a2, w2 = autokeys(sh, items, alphas)
        ctrl.append((p2, a2, w2))
        if ctx.time_left() < 40:
            break
    vocab = [w for w in ctx.vocabulary if len(w) >= 5] + [w for w in POINTS + OTHER if len(w) >= 5]
    texts = letters(load_k1()["plaintext"] + load_k2()["plaintext_as_carved"] + load_k3()["plaintext"])
    hits = []
    for pn, cn, mode, P, f1, f2 in frags:
        for f in (f1, f2):
            for run_ in f.split("."):
                if len(run_) >= 5 and (any(run_ in w or w in run_ for w in vocab) or run_ in texts):
                    hits.append({"plain": pn, "cipher": cn, "mode": mode, "period": P, "run": run_})
    def tab(k4, idx):
        keys = sorted(set(k4) | {k for c in ctrl for k in c[idx]})
        return {str(k): {"k4": k4.get(k, 0), "controls": [c[idx].get(k, 0) for c in ctrl]} for k in keys}
    pt = tab(per, 0)
    return {
        "candidates": [],
        "bounds": {"family": "compass-point and C15 word alphabets: periodic key, ciphertext autokey, autokey plus periodic key",
                   "alphabets": len(alphas), "pairs": len(alphas) ** 2, "periods": f"1-{PMAX}",
                   "periodic_consistent_by_period": pt, "autokey_constant_by_checks": tab(plain, 1),
                   "autokey_plus_periodic_by_checks": tab(withp, 2), "fragments": len(frags), "word_matches": hits[:30]},
        "notes": f"{len(alphas)} alphabets, {len(alphas) ** 2} pairs. Periodic consistent at P <= 26: " + str({P: (v['k4'], min(v['controls']), max(v['controls'])) for P, v in pt.items() if int(P) <= 26})
                 + ". Autokey (checks: K4, control min, max): " + str({k: (v['k4'], min(v['controls']), max(v['controls'])) for k, v in tab(plain, 1).items()})
                 + ". Autokey plus periodic: " + str({k: (v['k4'], min(v['controls']), max(v['controls'])) for k, v in tab(withp, 2).items()})
                 + f". Word matches in {len(frags)} fragments: {len(hits)}.",
    }


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    A = keyword_mixed("EASTNORTHEAST")
    ct, kn = ctx.K4, ctx.KNOWN
    lines = [f"alphabet {A} on both sides, Vigenere, 7-letter key", "", "place  known  carved  key  slot"]
    for pos in (22, 29, 23, 30):
        lines.append(f"{pos:>5}  {kn[pos]:>5}  {ct[pos - 1]:>6}  {A[(A.index(ct[pos - 1]) - A.index(kn[pos])) % 26]:>3}  {(pos - 1) % 7:>4}")
    return "\n".join(lines)
