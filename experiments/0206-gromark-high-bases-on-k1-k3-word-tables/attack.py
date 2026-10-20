"""Experiment 0206 (F5.3). See program.md for the contract."""

EXPERIMENT = {
    "slug": "gromark-high-bases-on-k1-k3-word-tables",
    "title": "F5.3: Gromark growth rules in bases 16-26 on the tables built from K1-K3's words and the 2025 letter (0054's 10,404 pairs), two- and three-term rules with lags to 13, exact, with scrambled copies and a planted Gromark text",
    "family": "5-gromark",
    "parent": "0054-gromark-bases-k1-k3-word-alphabets",
    "changed": (
        "F5.3, found by the positive control C-F5-1d (#73): 0054 built 102 tables from the solved messages' words and "
        "the 2025 letter, found no pair admits a base of 15 or less, and so tested no growth rule; but bases 16-26 are "
        "admissible and were never tested on these tables (0046 tested them on the vocabulary's tables, 0076/0195 on a "
        "free cipher alphabet with the plain side standard). Here 0046's rule test, unchanged in substance, on 0054's "
        "pairs: every two-term rule k[i] = k[i-a] + k[i-b] and three-term rule k[i] = k[i-a] + k[i-b] + k[i-c], lags "
        "up to 13, every base 16-26 the pair admits, 3 forms, at least six checks inside the known runs, then the "
        "stream carried from EASTNORTHEAST to BERLINCLOCK; on K4, ten scrambled copies and a planted text."
    ),
    "hypothesis_expert": (
        "C22(a) (Gromark; YAR as primer), Bean's Gromark case (knowledge/05-attacks.md). Model: c = C[P(p) + k_i] "
        "(or Beaufort and variant forms), plain and cipher alphabets keyword-mixed from K1-K3 plaintext words and the "
        "C13/C14 words (0054's pool: 102 alphabets incl. standard and KRYPTOS), key digits in base B with a lagged rule. "
        "Each known letter forces a shift; all must be below B; the rule is tested on the 13 and 11 consecutive forced "
        "shifts (13 - a and 11 - a checks), at least six (chance about 26^-6 per set), and survivors must carry their "
        "full stream from the first run to the second. Statistic: survivors with six or more checks, and survivors "
        "consistent with both runs, K4 against each copy."
    ),
    "hypothesis_eli5": (
        "Gromark grows a long number key from a few starting digits by adding earlier digits. Experiment 54 built "
        "tables from the words of the solved messages and only checked small number bases, which the known letters "
        "rule out; the larger bases, 16 to 26, were never checked on those tables. We check them now with every "
        "growth rule looking up to 13 digits back."
    ),
    "prediction": "No rule with six or more checks survives on K4 beyond the copies' count; none carries to the second run. The planted text is found. Zero candidates.",
    "method": (
        "1. Rebuild 0054's alphabet pool. 2. For each plain and cipher alphabet and form, the 24 forced shifts; the "
        "bases from max(16, largest + 1) to 26. 3. Compiled: every rule (78 two-term, 286 three-term), checked on the "
        "consecutive shifts in each run; six or more checks to survive; then carry the stream from the first run to "
        "the second. 4. K4, ten copies, a planted text; counts compared."
    ),
    "walkthrough": (
        "1. Build a table from a solved-message word, say DESPARATLY, and use it for the plain or cipher side. "
        "2. Read off the shift each known letter needs: 13 shifts in a row over EASTNORTHEAST, 11 over BERLINCLOCK. "
        "3. Choose a base, say 20, and a rule, say each digit is the sum of those 5 and 2 back. "
        "4. Check: shift 6 must equal shift 1 + shift 4 mod 20, and so on along both runs. "
        "5. One failure kills the rule; repeat for every rule, base, table and form."
    ),
}

import ctypes
import importlib.util
import os
import random
import subprocess
import tempfile
import time
from pathlib import Path
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
N_CONTROLS = 10
MIN_CHECKS = 6
ROOT = Path(__file__).resolve().parent
if not (ROOT / "kryptos").exists():
    ROOT = Path.cwd()
MODES = {"vig": lambda p, c: (c - p) % 26, "beau": lambda p, c: (c + p) % 26, "varbeau": lambda p, c: (p - c) % 26}
ENC = {"vig": lambda p, k: (p + k) % 26, "beau": lambda p, k: (k - p) % 26, "varbeau": lambda p, k: (p - k) % 26}
RULES = [(a, b) for a in range(2, 14) for b in range(1, a)] + [(a, b, c) for a in range(3, 14) for b in range(2, a) for c in range(1, b)]

C_SOURCE = r"""
/* s: ntrip x 24 forced shifts (run 1: 13, run 2: 11). rules: nr x 3 lags (0 = unused). For each triple, each base
   from max(16, largest + 1) to 26, each rule: check inside each run (i >= a); survive with >= minc checks; then
   carry the stream forward from run 1 over the 30 places between (positions 34..63) and compare with run 2. */
int scan(const int *s, int ntrip, const int *rules, int nr, int minc, int *out, int cap, long *nsurv, long *nboth) {
    int nout = 0;
    for (int t = 0; t < ntrip; t++) {
        const int *v = s + 24 * t;
        int mx = 0;
        for (int e = 0; e < 24; e++) if (v[e] > mx) mx = v[e];
        int b0 = mx + 1 < 16 ? 16 : mx + 1;
        for (int B = b0; B <= 26; B++) for (int r = 0; r < nr; r++) {
            int la = rules[3 * r], lb = rules[3 * r + 1], lc = rules[3 * r + 2];
            int checks = 0, ok = 1;
            for (int run = 0; run < 2 && ok; run++) {
                const int *w = v + (run ? 13 : 0); int len = run ? 11 : 13;
                for (int i = la; i < len; i++) {
                    checks++;
                    int x = w[i - la] + w[i - lb] + (lc ? w[i - lc] : 0);
                    if (x % B != w[i]) { ok = 0; break; }
                }
            }
            if (!ok || checks < minc) continue;
            (*nsurv)++;
            /* carry: stream positions 21..33 are run 1 (0-based places), run 2 at 63..73 */
            int k[97]; for (int j = 0; j < 13; j++) k[21 + j] = v[j];
            for (int i = 34; i <= 73; i++) k[i] = (k[i - la] + k[i - lb] + (lc ? k[i - lc] : 0)) % B;
            int both = 1;
            for (int j = 0; j < 11; j++) if (k[63 + j] != v[13 + j]) { both = 0; break; }
            if (both) (*nboth)++;
            if (nout < cap) { out[4 * nout] = t; out[4 * nout + 1] = B; out[4 * nout + 2] = r; out[4 * nout + 3] = both; nout++; }
        }
    }
    return nout;
}
"""


def build():
    d = tempfile.mkdtemp(prefix="k4_grom_")
    src, so = os.path.join(d, "g.c"), os.path.join(d, "g.so")
    open(src, "w").write(C_SOURCE)
    subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", so, src], check=True, capture_output=True)
    lib = ctypes.CDLL(so)
    lib.scan.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int,
                         ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long)]
    return lib


I = lambda v: (ctypes.c_int * len(v))(*v)


def pool_0054(vocab):
    path = sorted(ROOT.glob("experiments/0054-*/attack.py"))[0]
    spec = importlib.util.spec_from_file_location("snap0054", path)
    mod = importlib.util.module_from_spec(spec)
    mod.__file__ = str(ROOT / "attack.py")
    spec.loader.exec_module(mod)
    pool, _ = mod.word_pool(vocab)
    return pool


def triples(text, known_list, pool):
    names = list(pool)
    idx = {n: {ch: i for i, ch in enumerate(pool[n])} for n in names}
    tri, flat = [], []
    for pn in names:
        for cn in names:
            for m, f in MODES.items():
                tri.append((pn, cn, m))
                flat += [f(idx[pn][a], idx[cn][text[q - 1]]) for q, a in known_list]
    return tri, flat


def py_check(v, B, rule):
    """Python reference for one (shifts, base, rule)."""
    a = rule[0]
    checks = 0
    for w in (v[:13], v[13:]):
        for i in range(a, len(w)):
            checks += 1
            if sum(w[i - l] for l in rule) % B != w[i]:
                return False, checks
    return True, checks


def scan_text(lib, text, known_list, pool, rflat):
    tri, flat = triples(text, known_list, pool)
    cap = 2000
    out = (ctypes.c_int * (4 * cap))(); ns = ctypes.c_long(0); nb = ctypes.c_long(0)
    n = lib.scan(I(flat), len(tri), I(rflat), len(RULES), MIN_CHECKS, out, cap, ctypes.byref(ns), ctypes.byref(nb))
    surv = [(tri[out[4 * k]], out[4 * k + 1], RULES[out[4 * k + 2]], bool(out[4 * k + 3])) for k in range(n)]
    return ns.value, nb.value, surv, tri, flat


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    known_list = [(q, known[q]) for q in sorted(known)]
    t0 = time.time()
    pool = pool_0054(ctx.vocabulary)
    lib = build()
    rflat = []
    for r in RULES:
        rflat += list(r) + [0] * (3 - len(r))
    rng = random.Random(5300)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    # planted Gromark text: a pair from the pool, base 20, rule (7, 3), random primer
    from kryptos.plants import english_plant
    names = list(pool)
    prng = random.Random(5301)
    pn, cn = names[prng.randrange(2, len(names))], names[prng.randrange(2, len(names))]
    m, B, rule = "vig", 20, (7, 3)
    k = [prng.randrange(B) for _ in range(7)]
    while len(k) < N:
        k.append(sum(k[-l] for l in rule) % B)
    pt = english_plant(5301)
    pa, ca = pool[pn], pool[cn]
    plant_ct = "".join(ca[ENC[m](pa.index(ch), k[i])] for i, ch in enumerate(pt))
    # compiled scan against the Python reference on sample triples
    ns0, nb0, surv0, tri, flat = scan_text(lib, ct, known_list, pool, rflat)
    listed = {(s_[0], s_[1], tuple(s_[2])) for s_ in surv0}
    spot = 0
    for t in random.Random(3).sample(range(len(tri)), 300):
        v = flat[24 * t: 24 * t + 24]
        for rule_ in random.Random(t).sample(RULES, 20):
            for B_ in range(max(16, max(v) + 1), 27):
                ok, ch = py_check(v, B_, rule_)
                spot += 1
                if ok and ch >= MIN_CHECKS:
                    assert ns0 > len(surv0) or (tri[t], B_, rule_) in listed, "compiled scan missed a survivor"
    res = []
    for text in texts + [plant_ct]:
        ns, nb, surv, tri_, flat_ = scan_text(lib, text, known_list, pool, rflat)
        res.append({"survivors": ns, "survivors_both_runs": nb, "first": surv[:20]})
    p = res[-1]
    plant_found = any(s[0] == (pn, cn, m) and s[1] == B and tuple(s[2]) == rule and s[3] for s in p["first"])
    bounds = {"family": "Gromark growth rules (two- and three-term, lags to 13) in bases 16-26 on 0054's K1-K3-word and 2025-letter tables",
              "alphabets": len(pool), "pairs": len(pool) ** 2, "forms": 3, "rules": len(RULES), "bases": "max(16, largest forced + 1) to 26",
              "min_checks": MIN_CHECKS,
              "k4": {"survivors": res[0]["survivors"], "survivors_both_runs": res[0]["survivors_both_runs"], "list": [[list(s[0]), s[1], list(s[2]), s[3]] for s in res[0]["first"]]},
              "copies_survivors": [r["survivors"] for r in res[1:-1]], "copies_survivors_both_runs": [r["survivors_both_runs"] for r in res[1:-1]],
              "plant": {"plain": pn, "cipher": cn, "form": m, "base": B, "rule": list(rule), "found": plant_found,
                        "survivors": p["survivors"], "survivors_both_runs": p["survivors_both_runs"]},
              "spot_check": f"{spot} (table, base, rule) cases checked against Python",
              "controls": f"{N_CONTROLS} shuffled copies (seed 5300)", "seconds": round(time.time() - t0), "exhaustive": "yes"}
    notes = (f"Survivors with >= {MIN_CHECKS} checks: K4 {res[0]['survivors']} (both runs {res[0]['survivors_both_runs']}), copies "
             f"{min(bounds['copies_survivors'])}-{max(bounds['copies_survivors'])} (both runs {min(bounds['copies_survivors_both_runs'])}-{max(bounds['copies_survivors_both_runs'])}). Plant found: {plant_found}.")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    lines = ["standard plain alphabet, KRYPTOS cipher alphabet, Vigenere: the forced shifts over EASTNORTHEAST", ""]
    sh = [(KRY.index(ctx.K4[q - 1]) - STD.index(ctx.KNOWN[q])) % 26 for q in range(22, 35)]
    lines.append("shifts: " + " ".join(map(str, sh)))
    lines.append(f"largest {max(sh)}: only bases {max(16, max(sh) + 1)}-26 are possible")
    lines.append(f"rule (5, 2) in base 20: shift 6 should be shift 1 + shift 4 = {(sh[0] + sh[3]) % 20}; it is {sh[5]}")
    return "\n".join(lines)
