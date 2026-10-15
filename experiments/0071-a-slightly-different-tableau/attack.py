"""Experiment 0071. See program.md for the contract."""

EXPERIMENT = {
    "slug": "a-slightly-different-tableau",
    "title": "Sanborn's own table, slightly different from the carved one: every alphabet one step away from KRYPTOS",
    "family": "1-keyed-periodic",
    "parent": "0005-quagmire-period-sweep-forced-keys",
    "changed": "Sanborn said the table he worked from was slightly different from the one on the sculpture. Every earlier sweep used the carved KRYPTOS alphabet exactly or alphabets built from words. Here the alphabet is the carved one with two letters swapped or one letter moved, 925 variants, tested with a repeating secret word and with the self-feeding autokey.",
    "hypothesis_expert": (
        "Family 1 re-entered with a new key source, C27(c): the 2010 worksheets show a tableau 'slightly "
        "different from the one on Kryptos' (research_notes/sanborn_charts/SOURCES.md; 02-sanborn-said.md). "
        "Alphabets: the KRYPTOS alphabet with one transposition of two letters (325) or one letter moved to "
        "another place (650 moves, of which 50 repeat an adjacent swap, so 600 new), 925 variants V. Pairings: "
        "V as both plain and cipher alphabet (the tableau's header and rows from one alphabet), plain "
        "standard with cipher V, and plain V with cipher standard; Vigenere or Beaufort. Systems: (1) "
        "periodic key, periods 1-52, exact crib consistency; (2) ciphertext autokey with a constant shift, "
        "lags 1-96, key letter read on V or on the standard alphabet. Survivors of (1) at periods up to 29 "
        "have their forced fragments matched against the vocabulary and K1-K3 windows. Ten shuffled coppers "
        "through the same sweep. Clue entries: C27(c), C6(a), C8(a)."
    ),
    "hypothesis_eli5": (
        "Sanborn has said that the table he enciphered with was slightly different from the one carved on "
        "the sculpture. If so, every test that used the carved alphabet exactly could have missed by a "
        "hair. We take the carved alphabet KRYPTOS-A-B-C... and make every version with two letters "
        "swapped or one letter moved, almost a thousand of them, and run the two simplest ciphers on each: "
        "a repeating secret word, and the autokey that feeds on earlier carved letters. Scrambled coppers "
        "get the same treatment."
    ),
    "prediction": (
        "No variant makes a period of 24 or less consistent under any pairing and mode; periods 25-26 "
        "survive at the shuffled-copper rate; no fragment at periods up to 29 matches a word; the autokey "
        "has no survivor with three or more redundant checks. Zero candidates pass."
    ),
    "method": (
        "1. Build the 925 alphabets one step from KRYPTOS. 2. For each pairing and mode, compute the key value "
        "each known letter forces. 3. For each period up to 52, check the slots agree; record the survivors "
        "and their fragments. 4. For each lag, check the autokey residuals agree. 5. Repeat on ten shuffled "
        "coppers and compare counts. 6. Match fragments at periods up to 29 against words."
    ),
    "walkthrough": (
        "1. Swap A and B in the carved alphabet: KRYPTOSBACDEFGHIJLMNQUVWXZ, counted from K = 0. 2. Use it for "
        "both the message and the carved letters, Vigenere, with a 7-letter secret word. 3. Place 22: known E "
        "is 11, carved F is 12; the key is 1, R, in slot 0. 4. Place 29, also slot 0: known T is 4, carved R "
        "is 1; the key is 1 - 4 = -3, which is 23, W. 5. R and W disagree, so this alphabet with a 7-letter "
        "word is dead. 6. Repeat for every variant, pairing, word length and lag."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY, load_k1, load_k2, load_k3

N = 97
PMAX = 52


def letters(s):
    return "".join(c for c in s.upper() if "A" <= c <= "Z")


def variants():
    out = {}
    base = list(KRY)
    for i in range(26):
        for j in range(i + 1, 26):
            v = base[:]; v[i], v[j] = v[j], v[i]
            out.setdefault("".join(v), f"swap {KRY[i]}{KRY[j]}")
    for i in range(26):
        for j in range(26):
            if i == j:
                continue
            v = base[:]; ch = v.pop(i); v.insert(j, ch)
            out.setdefault("".join(v), f"move {KRY[i]} to place {j + 1}")
    out.pop(KRY, None)
    return out


def setups(V):
    for pname, pa, cname, ca in (("V", V, "V", V), ("std", STD, "V", V), ("V", V, "std", STD)):
        for mode in ("vig", "beau"):
            yield f"{pname}/{cname}/{mode}", pa, ca, mode


def sweep(ct, known, vs, ctx, deadline, collect=False):
    items = sorted(known.items())
    per = {}
    auto = {}
    frags = []
    done = 0
    for V, name in vs.items():
        for label, pa, ca, mode in setups(V):
            PI = {c: i for i, c in enumerate(pa)}; CI = {c: i for i, c in enumerate(ca)}
            T = [((CI[ct[pos - 1]] - PI[p]) if mode == "vig" else (CI[ct[pos - 1]] + PI[p])) % 26 for pos, p in items]
            for P in range(1, PMAX + 1):
                slot = {}
                ok = True
                for (pos, _), t in zip(items, T):
                    if slot.setdefault((pos - 1) % P, t) != t:
                        ok = False; break
                if ok:
                    per[P] = per.get(P, 0) + 1
                    if collect and P <= 29:
                        frags.append((name, label, P, "".join(ca[slot[k]] if k in slot else "." for k in range(P)),
                                      "".join(pa[slot[k]] if k in slot else "." for k in range(P))))
            for kname, ka in (("V", V), ("std", STD)):
                KI = {c: i for i, c in enumerate(ka)}
                for L in range(1, 97):
                    res = {(t - KI[ct[pos - 1 - L]]) % 26 for (pos, _), t in zip(items, T) if pos - 1 - L >= 0}
                    m = sum(1 for pos, _ in items if pos - 1 - L >= 0)
                    if m >= 2 and len(res) == 1:
                        c = min(m - 1, 5)
                        auto[c] = auto.get(c, 0) + 1
        done += 1
        if ctx.time_left() < deadline:
            break
    return per, auto, frags, done


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    vs = variants()
    t0 = ctx.time_left()
    per, auto, frags, done = sweep(ct, known, vs, ctx, t0 * 0.55, collect=True)
    rng = random.Random(71)
    ctrl = []
    for _ in range(10):
        sh = list(ct); rng.shuffle(sh)
        p2, a2, _, d2 = sweep("".join(sh), known, vs, ctx, 25)
        ctrl.append((p2, a2, d2))
        if ctx.time_left() < 30:
            break
    vocab = [w for w in ctx.vocabulary if len(w) >= 5]
    texts = letters(load_k1()["plaintext"] + load_k2()["plaintext_as_carved"] + load_k3()["plaintext"])
    hits = []
    for name, label, P, f1, f2 in frags:
        for f in (f1, f2):
            for run_ in f.split("."):
                if len(run_) >= 5 and (any(run_ in w or w in run_ for w in vocab) or run_ in texts):
                    hits.append({"variant": name, "setup": label, "period": P, "run": run_})
    table = {str(P): {"k4": per.get(P, 0), "controls": [c[0].get(P, 0) for c in ctrl]} for P in range(1, PMAX + 1)
             if per.get(P, 0) or any(c[0].get(P, 0) for c in ctrl)}
    atab = {str(k): {"k4": auto.get(k, 0), "controls": [c[1].get(k, 0) for c in ctrl]} for k in sorted(set(auto) | {k for c in ctrl for k in c[1]})}
    return {
        "candidates": [],
        "bounds": {"family": "periodic key and ciphertext autokey on alphabets one swap or one move from KRYPTOS",
                   "variants": len(vs), "variants_done": done, "setups_per_variant": 6, "periods": f"1-{PMAX}", "lags": "1-96",
                   "periodic_consistent_by_period": table, "autokey_survivors_by_checks": atab,
                   "fragments_checked": len(frags), "word_matches": hits[:30], "controls_done": [c[2] for c in ctrl]},
        "notes": f"{done} of {len(vs)} variants. Periodic, consistent cases at P <= 26: K4 " + str({P: v['k4'] for P, v in table.items() if int(P) <= 26})
                 + f"; controls " + str({P: (min(v['controls']), max(v['controls'])) for P, v in table.items() if int(P) <= 26})
                 + f". Autokey survivors by checks: " + str({k: (v['k4'], min(v['controls']) if v['controls'] else None, max(v['controls']) if v['controls'] else None) for k, v in atab.items()})
                 + f". Word matches in {len(frags)} fragments: {len(hits)}.",
    }


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    V = "KRYPTOSBACDEFGHIJLMNQUVWXZ"
    ct, kn = ctx.K4, ctx.KNOWN
    lines = [f"alphabet {V} (A and B swapped), message and carved letters both on it, Vigenere, 7-letter key", "", "place  known  carved  key  slot"]
    for pos in (22, 29, 23, 30):
        lines.append(f"{pos:>5}  {kn[pos]:>5}  {ct[pos - 1]:>6}  {V[(V.index(ct[pos - 1]) - V.index(kn[pos])) % 26]:>3}  {(pos - 1) % 7:>4}")
    return "\n".join(lines)
