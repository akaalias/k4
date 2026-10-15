"""Experiment 0098. See program.md for the contract."""

EXPERIMENT = {
    "slug": "sculpture-running-key-on-an-unknown-alphabet",
    "title": "A running key from the sculpture's texts on an unknown mixed alphabet, the table 'slightly different'",
    "family": "1-keyed-periodic",
    "parent": "0017-running-key-from-the-sculpture-itself",
    "changed": "0017, 0004, 0021 and 0078 slid running keys along K4 on the standard and KRYPTOS alphabets only. Here the table's alphabet is unknown, any of the 26! orders (Quagmire III, as K1 and K2 use, with the alphabet left free): for each key text and offset the 24 known letters give linear equations in the unknown letter positions, solved exactly mod 2 and mod 13.",
    "hypothesis_expert": (
        "Type 3 and type 5 of directions.md together: keys concealed at the sculpture (C6(a), Scheidt) on a table "
        "Sanborn called 'slightly different' from the carved one (C11a); 0071 tried only alphabets one swap or move away. "
        "Model, Quagmire III with unknown alphabet X: X(c_i) = X(p_i) + s X(k_{o+i}) mod 26, s = +1 (Vigenere) or -1 "
        "(variant), and X(c_i) = X(k_{o+i}) - X(p_i) (Beaufort); each known letter gives one homogeneous equation in the "
        "26 unknowns X(letter). X must be a bijection: two letters forced to the same value mod 2 and mod 13, or three "
        "forced together mod 13, is a contradiction (as in 0097). Key texts as in 0090: the carved tableau by rows, rows "
        "with the index column, and columns; the Morse as carved and in reverse order; the four ciphertexts; the K1-K3 "
        "plaintexts; Sanborn's 1989 letter, the 1991 dedication texts and the 2025 open letter; each forward and backward "
        "at every cyclic offset. Ten shuffled coppers."
    ),
    "hypothesis_eli5": (
        "Experiment 17 used the sculpture's own texts as a long key, but only with the two alphabets we know. Sanborn "
        "said his table was slightly different, so here the alphabet along the top of the table can be any order of "
        "the 26 letters. We do not need to guess it: for each key text and starting point, simple arithmetic on the 24 "
        "known letters shows whether any alphabet at all could make them fit."
    ),
    "prediction": (
        "A random equation set like these is consistent with some alphabet only rarely; K4's consistent (text, offset, "
        "rule) count lies inside the ten shuffled coppers' range, and no consistent setting decrypts to English. Zero candidates."
    ),
    "method": (
        "1. Build the key texts. 2. For each text, direction, offset and rule, write the 24 equations. 3. Solve over "
        "GF(2) and GF(13) and test the bijection. 4. Count consistent settings on K4 and on ten shuffled coppers. 5. For "
        "K4's consistent settings, report how many letter positions the equations fix."
    ),
    "walkthrough": (
        "1. Take the Morse as carved as the key text, starting at offset 0, and the Vigenere rule. "
        "2. At place 22 the known letter is E, the carved letter F, the key letter some letter K22: position of F = position of E + position of K22 in the unknown alphabet. "
        "3. Write one such equation for each of the 24 known places. "
        "4. Solve them mod 2 and mod 13; if two different letters are forced to the same position, no alphabet works. "
        "5. Repeat for every key text, offset, direction and rule, and on scrambled coppers."
    ),
}

import json, random
from pathlib import Path
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY, load_k1, load_k2, load_k3
from kryptos.ciphers import tableau_rows

N = 97
N_CONTROLS = 10
ROOT = Path(__file__).resolve().parent
if not (ROOT / "knowledge").exists():
    ROOT = Path.cwd()


def letters(s):
    return "".join(c for c in s.upper() if "A" <= c <= "Z")


def sources():
    site = json.loads((ROOT / "data" / "site_texts.json").read_text())
    rows = tableau_rows(carved=True)
    src = {}
    src["tableau rows"] = "".join(rows)
    src["tableau rows with index column"] = "".join(STD[i] + r for i, r in enumerate(rows))
    width = max(len(r) for r in rows)
    src["tableau columns"] = "".join(r[c] for c in range(width) for r in rows if c < len(r))
    morse = [letters(m) for m in site["morse"]]
    src["morse as carved"] = "".join(morse)
    src["morse reversed order"] = "".join(reversed(morse))
    k1, k2, k3 = load_k1(), load_k2(), load_k3()
    k4 = letters((ROOT / "data" / "k4.txt").read_text())
    src["panel ciphertexts K1-K4"] = letters(k1["ciphertext"]) + letters(k2["ciphertext_as_carved"]) + letters(k3["ciphertext"]) + k4
    src["K1-K3 plaintexts"] = letters(k1["plaintext"]) + letters(k2["plaintext_as_carved"]) + letters(k3["plaintext"])
    t = (ROOT / "knowledge" / "sources" / "sanborn-1989-letter-and-webster-1990-cryptogram.txt").read_text(errors="ignore")
    a = t.index("Dear Agency Employees"); b = t.index("Sincerely, Jim Sanborn") + len("Sincerely, Jim Sanborn")
    c = t.index("Remarks by William H. Webster")
    o = (ROOT / "knowledge" / "sources" / "openletter-2025.txt").read_text(errors="ignore")
    oa = o.index("Dear Kryptos fans"); ob = o.index("Jim Sanborn", o.index("All the best")) + len("Jim Sanborn")
    src["Sanborn 1989 letter"] = letters(t[a:b])
    src["1991 dedication texts"] = letters(t[c:])
    src["2025 open letter"] = letters(o[oa:ob])
    out = {}
    for name, s in src.items():
        out[name + " fwd"] = s
        out[name + " bwd"] = s[::-1]
    carter = letters((ROOT / "knowledge" / "sources" / "carter-1923-tomb-of-tutankhamen-vol1.txt").read_text(errors="ignore"))
    big = {"Carter vol 1 fwd": carter, "Carter vol 1 bwd": carter[::-1]}
    return out, big


def nullspace_signatures(rows, nv, q):
    """rows: list of {var: coef}. Returns, for each variable, the tuple of its values over a nullspace basis mod q."""
    M = [[r.get(v, 0) % q for v in range(nv)] for r in rows]
    piv = []
    r = 0
    for c in range(nv):
        pr = next((i for i in range(r, len(M)) if M[i][c]), None)
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        inv = pow(M[r][c], q - 2, q)
        M[r] = [(x * inv) % q for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [(a - f * b) % q for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == len(M):
            break
    pset = set(piv)
    free = [c for c in range(nv) if c not in pset]
    sig = {}
    for v in range(nv):
        if v in pset:
            row = M[piv.index(v)]
            sig[v] = tuple((-row[f]) % q for f in free)
        else:
            sig[v] = tuple(1 if f == v else 0 for f in free)
    return sig


def consistent(eqs):
    """eqs: list of {letter: coefficient}; unknowns are the 26 letter positions of one alphabet."""
    var = {c: i for i, c in enumerate(STD)}
    rows = [{var[c]: v for c, v in r.items() if v % 26} for r in eqs]
    s2 = nullspace_signatures(rows, 26, 2)
    s13 = nullspace_signatures(rows, 26, 13)
    used = set()
    for r in eqs:
        used |= set(r)
    by13 = {}
    for c in used:
        by13.setdefault(s13[var[c]], []).append(var[c])
    for grp in by13.values():
        if len(grp) > 2:
            return False, None
        if len(grp) == 2 and s2[grp[0]] == s2[grp[1]]:
            return False, None
    free2 = len(next(iter(s2.values()))); free13 = len(next(iter(s13.values())))
    return True, (free2, free13)


def equation(rule, p, c, k):
    r = {}
    for ch, v in ((c, 1), (p, -1 if rule != "beau" else 1), (k, {"vig": -1, "var": 1, "beau": -1}[rule])):
        r[ch] = r.get(ch, 0) + v
    return {a: b for a, b in r.items() if b % 26}


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    places = sorted(known)
    srcs, _ = sources()
    rng = random.Random(98)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    assert plant_check()
    counts = [0] * len(texts)
    k4_hits = []
    n = 0
    for name, s in srcs.items():
        L = len(s); ss = s + s[:N]
        for o in range(L):
            for rule in ("vig", "var", "beau"):
                n += 1
                for t, txt in enumerate(texts):
                    eqs = [equation(rule, known[q], txt[q - 1], ss[o + q - 1]) for q in places]
                    ok, free = consistent([e for e in eqs if e])
                    if ok:
                        counts[t] += 1
                        if t == 0:
                            k4_hits.append({"source": name, "offset": o, "rule": rule, "free_dims_mod2_mod13": free})
        if ctx.time_left() < 60:
            break
    bounds = {
        "family": "running key from the sculpture's texts on an unknown mixed alphabet (Quagmire III)",
        "sources": {k: len(v) for k, v in srcs.items()}, "rules": ["vigenere", "variant", "beaufort"],
        "settings": n, "k4_consistent": counts[0], "controls_consistent": counts[1:],
        "k4_consistent_settings": k4_hits[:40],
        "controls": f"{N_CONTROLS} shuffled coppers (seed 98), identical search",
    }
    notes = (f"{n:,} (text, offset, rule) settings. Consistent with some alphabet: K4 {counts[0]}, controls {counts[1:]}.")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def plant_check():
    rng = random.Random(4)
    X = list(STD); rng.shuffle(X)
    key = [rng.choice(STD) for _ in range(N)]
    from kryptos.facts import KNOWN
    good = [equation("vig", KNOWN[q], X[(X.index(KNOWN[q]) + X.index(key[q - 1])) % 26], key[q - 1]) for q in sorted(KNOWN)]
    return consistent([e for e in good if e])[0]


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    srcs, _ = sources()
    s = srcs["morse as carved fwd"]
    ss = s + s[:N]
    lines = ["key text: the Morse as carved, offset 0, Vigenere on an unknown alphabet X", "",
             "place  known  carved  key  equation"]
    for q in (22, 23, 24, 25, 64, 65):
        lines.append(f"{q:>5}  {known[q]:>5}  {ct[q - 1]:>6}  {ss[q - 1]:>3}  X({ct[q - 1]}) = X({known[q]}) + X({ss[q - 1]})")
    eqs = [equation("vig", known[q], ct[q - 1], ss[q - 1]) for q in sorted(known)]
    lines += ["", f"some alphabet fits all 24: {consistent([e for e in eqs if e])[0]}"]
    return "\n".join(lines)
