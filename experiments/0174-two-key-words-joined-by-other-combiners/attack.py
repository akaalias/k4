"""Experiment 0174 (F3.1, second part). See program.md for the contract."""

EXPERIMENT = {
    "slug": "two-key-words-joined-by-other-combiners",
    "title": "F3.1: a puzzle word and a dictionary word joined by a combiner other than plain addition: through a table on a third, keyword-mixed alphabet, or by multiplication",
    "family": "3-two-component-key",
    "parent": "0115-two-key-words-added",
    "changed": (
        "F3.1. 0115 tested two key words added letter by letter, with letters numbered on the standard or KRYPTOS order. "
        "Here the combiner changes: (a) the two words are joined through a table built on a third alphabet, the "
        "keyword-mixed alphabet of any of the 62 vocabulary words, which numbers both words' letters (so the combined key "
        "is a + b on that numbering); (b) the two words' numbers are multiplied mod 26, on the standard, KRYPTOS or any "
        "vocabulary numbering. Everything else as 0115: first word any puzzle word from every start, second word any "
        "dictionary word of 3-24 letters in every rotation, 12 table rules, exact, ten scrambled coppers."
    ),
    "hypothesis_expert": (
        "C5(b) ('executed years later when used with the correct key word/s', Scheidt 2011 via Bean, knowledge/sources/"
        "bean-2021-cryptodiagnosis-of-k4.txt and 03-scheidt-said.md), C6 (Scheidt's constructive key management: a working "
        "key built from splits through a combiner, knowledge/07-people.md), F3 family. Model: carved = T(plain, k_i) for "
        "one of 12 table rules (Vigenere, Beaufort, variant; plain and cipher alphabets standard or KRYPTOS), key value "
        "k_i = g(N(a[(i + o) mod m]), N(b[i mod n])) with N a numbering of letters (standard, KRYPTOS, or the keyword-mixed "
        "alphabet of a vocabulary word: 64) and g in {addition (new only for the 62 mixed numberings), multiplication mod "
        "26}. a: every puzzle word (0115's list: vocabulary, K1-K3 plaintext words, theme words), every start o. The 24 "
        "known letters force k at their places; g^-1 gives b's number (multiplication: all solutions of a x = k mod 26, "
        "none when gcd fails); b repeating with period n must agree within each slot; a fully forced b (or, for "
        "multiplication, every b allowed by the slot sets) is looked up among the rotations of dictionary words of length "
        "n (kryptos/data/words.txt). Exact."
    ),
    "hypothesis_eli5": (
        "Scheidt's professional habit is a key built from two parts joined by a rule. We already tried two secret words "
        "added together letter by letter. Here the rule for joining them changes: the words are combined through a table "
        "made from a third word's alphabet, or their letter numbers are multiplied. For each first word from the puzzle, "
        "the 24 known letters then dictate the second word letter by letter; we check whether any real English word fits, "
        "and compare with scrambled copies of the carved text."
    ),
    "prediction": (
        "No pair fits on K4 under either combiner; the coppers give no or almost no dictionary hits either (0115 had none "
        "on K4). Multiplication leaves more consistent cases than addition (zero divisors make b ambiguous), at the "
        "coppers' rate. Zero candidates, or only candidates inside the coppers' hit counts."
    ),
    "method": (
        "1. Build the puzzle word list (0115's) and the 64 numberings. "
        "2. For each text (K4, ten coppers), table rule, numbering, combiner, first word and start: the forced key value at "
        "each known place, then the second word's number (or numbers) there. "
        "3. For each length 3-24: slot agreement; fully forced second words looked up among dictionary rotations; for "
        "multiplication with ambiguous slots, dictionary rotations matched against the slot sets. "
        "4. Count consistent cases and hits per text; decrypt K4's hits."
    ),
    "walkthrough": (
        "1. Take the sculpture's table (KRYPTOS alphabet, Vigenere) and number letters by the alphabet mixed from the word BERLIN: B=0, E=1, R=2, L=3, I=4, N=5, A=6 and so on. "
        "2. At each known place, the table gives the key value: carved place minus known place. "
        "3. Write the first word, say PALIMPSEST, under the message from some letter, and number its letters the same way. "
        "4. The second word's number at that place is the key value minus the first word's number (or, for multiplication, the number that times the first word's number gives the key value). "
        "5. If the second word repeats every n letters, places n apart must ask for the same letter. "
        "6. When every letter of the second word is forced, look it up in the dictionary, in every rotation. "
        "7. Do the same on scrambled copies of the carved text."
    ),
}

import random
from math import gcd
from pathlib import Path
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY
from kryptos.alphabets import keyword_mixed

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



C_SOURCE = r"""
// Two key words joined by a combiner. For one text/rule (forced key values K[24] at the known places) and one numbering
// (letter -> number NI), every first word w at every start o gives the first word's numbers at the known places; the
// second word's number there is K - a (add) or the solutions of a*x = K (mul). For each second-word length n 3..24 the
// slots must agree (sets intersect). Consistent cases are written out with their slot masks for the dictionary step.
#include <stdint.h>
static uint32_t MUL[26][26];   // MUL[a][k] = mask of x with a*x = k mod 26
static int init = 0;
static void setup(void) {
    for (int a = 0; a < 26; a++) for (int k = 0; k < 26; k++) { uint32_t m = 0; for (int x = 0; x < 26; x++) if ((a * x) % 26 == k) m |= 1u << x; MUL[a][k] = m; }
    init = 1;
}
// out record: w, o, n, then 24 masks (first n used); returns number of consistent cases (all, even beyond cap)
long scan(const int *K, const int *NI, int mul, const int *wl, const int *ws, const int *wn, int nw, const int *pidx,
          int *out, int cap, int *nout) {
    if (!init) setup();
    long cons = 0;
    uint32_t m[24], slot[24];
    for (int w = 0; w < nw; w++) {
        int L = wn[w];
        for (int o = 0; o < L; o++) {
            int dead = 0;
            for (int e = 0; e < 24; e++) {
                int a = NI[wl[ws[w] + (pidx[e] + o) % L]];
                m[e] = mul ? MUL[a][K[e]] : 1u << (((K[e] - a) % 26 + 26) % 26);
                if (!m[e]) { dead = 1; break; }
            }
            if (dead) continue;
            for (int n = 3; n <= 24; n++) {
                for (int s = 0; s < n; s++) slot[s] = 0x3ffffff;
                int ok = 1;
                for (int e = 0; e < 24; e++) { int s = pidx[e] % n; slot[s] &= m[e]; if (!slot[s]) { ok = 0; break; } }
                if (!ok) continue;
                cons++;
                if (*nout < cap) {
                    int *r = out + (*nout) * 27;
                    r[0] = w; r[1] = o; r[2] = n;
                    for (int s = 0; s < 24; s++) r[3 + s] = s < n ? (int)slot[s] : 0;
                    (*nout)++;
                }
            }
        }
    }
    return cons;
}
"""


def build():
    import ctypes, os, subprocess, tempfile
    d = tempfile.mkdtemp(prefix="k4_comb_")
    src, so = os.path.join(d, "c.c"), os.path.join(d, "c.so")
    open(src, "w").write(C_SOURCE)
    subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", so, src], check=True, capture_output=True)
    lib = ctypes.CDLL(so)
    lib.scan.restype = ctypes.c_long
    return lib


def run(ctx):
    import ctypes
    import time
    t0 = time.time()
    lib = build()
    ct, known = ctx.K4, ctx.KNOWN
    places = sorted(known)
    pidx = [p - 1 for p in places]
    puzzle = sorted({w for w in SPACED.split() if len(w) >= 2} | {w.upper() for w in ctx.vocabulary if 2 <= len(w) <= 30 and w.isalpha()} | set(EXTRA))
    words = [w.strip().upper() for w in (ROOT / "kryptos" / "data" / "words.txt").read_text().split()]
    rots = {}
    for w in words:
        if 3 <= len(w) <= 24 and w.isalpha():
            d = rots.setdefault(len(w), {})
            for r in range(len(w)):
                d.setdefault(w[r:] + w[:r], (w, r))
    numberings = {"std": STD, "kry": KRY}
    for v in ctx.vocabulary:
        a = keyword_mixed(v.upper())
        if a not in numberings.values():
            numberings["mix:" + v.upper()] = a
    rng = random.Random(1740)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    PLANT_P = "USEDTHEEARTHSMAGNETICEASTNORTHEASTRMATIONWASGATHEREDANDTRANSMITBERLINCLOCKUNDTOANUNKNOWNLOCATIONX"
    plant_keys = [{"combiner": "mul/vig/kry/kry/mix:BERLIN", "word1": "PALIMPSEST", "start1": 3, "word2": "GARDEN", "rotation2": 0},
                  {"combiner": "add/beau/std/kry/mix:BERLIN", "word1": "PALIMPSEST", "start1": 3, "word2": "SHADOW", "rotation2": 2}]
    for k in plant_keys:
        texts.append(encrypt(PLANT_P, k))
    NC = 1 + N_CONTROLS
    rules = [(m, pa, ca) for m in ("vig", "beau", "var") for pa in ALPH for ca in ALPH]
    I = lambda v: (ctypes.c_int * len(v))(*v)
    wl, ws, wn = [], [], []
    for w in puzzle:
        ws.append(len(wl)); wn.append(len(w)); wl += [ord(ch) - 65 for ch in w]
    WL, WS, WN, PI_ = I(wl), I(ws), I(wn), I(pidx)
    CAP = 200000
    buf = (ctypes.c_int * (CAP * 27))()
    T = len(texts)
    consistent = {g: [0] * T for g in ("add", "mul")}
    forced = {g: [0] * T for g in ("add", "mul")}
    too_open = {g: [0] * T for g in ("add", "mul")}
    hits = {g: [[] for _ in texts] for g in ("add", "mul")}
    n_cases = {g: 0 for g in ("add", "mul")}
    nstarts = sum(wn)
    for t, txt in enumerate(texts):
        for mode, pa, ca in rules:
            PI = {c: i for i, c in enumerate(ALPH[pa])}; CI = {c: i for i, c in enumerate(ALPH[ca])}
            K = []
            for q in places:
                c, p = CI[txt[q - 1]], PI[known[q]]
                K.append({"vig": (c - p) % 26, "beau": (c + p) % 26, "var": (p - c) % 26}[mode])
            KK = I(K)
            for nname, NA in numberings.items():
                NIl = [0] * 26
                for i, ch in enumerate(NA):
                    NIl[ord(ch) - 65] = i
                for g in ("add", "mul"):
                    if g == "add" and nname in ("std", "kry"):
                        continue            # 0115
                    if t == 0:
                        n_cases[g] += nstarts * 22
                    nout = ctypes.c_int(0)
                    cons = lib.scan(KK, I(NIl), 1 if g == "mul" else 0, WL, WS, WN, len(puzzle), PI_, buf, CAP, ctypes.byref(nout))
                    consistent[g][t] += cons
                    for r in range(nout.value):
                        rec = buf[r * 27:(r + 1) * 27]
                        w, o, n = rec[0], rec[1], rec[2]
                        sets = [[NA[v] for v in range(26) if rec[3 + s] >> v & 1] for s in range(n)]
                        size = 1
                        for st in sets:
                            size *= len(st)
                        if size == 1:
                            forced[g][t] += 1
                        if size > 4096:
                            too_open[g][t] += 1
                            continue
                        cands2 = [""]
                        for st in sets:
                            cands2 = [x + y for x in cands2 for y in st]
                        for key2 in cands2:
                            h = rots.get(n, {}).get(key2)
                            if h:
                                hits[g][t].append({"rule": f"{mode}/{pa}/{ca}", "numbering": nname, "word1": puzzle[w], "start1": o,
                                                   "word2": h[0], "rotation2": h[1], "n": n})
    cands = []
    for g in ("add", "mul"):
        for h in hits[g][0][:20]:
            mode, pa, ca = h["rule"].split("/")
            NA = numberings[h["numbering"]]; NI = {c: i for i, c in enumerate(NA)}
            PA = ALPH[pa]; CI = {c: i for i, c in enumerate(ALPH[ca])}
            w2 = h["word2"]; r2 = h["rotation2"]; key2 = w2[r2:] + w2[:r2]
            pt = []
            for i in range(N):
                x, y = NI[h["word1"][(i + h["start1"]) % len(h["word1"])]], NI[key2[i % h["n"]]]
                k = (x + y) % 26 if g == "add" else (x * y) % 26
                c = CI[ct[i]]
                pt.append(PA[{"vig": (c - k) % 26, "beau": (k - c) % 26, "var": (c + k) % 26}[mode]])
            cands.append({"plaintext": "".join(pt), "key": {"word1": h["word1"], "start1": h["start1"], "word2": w2, "rotation2": r2,
                                                            "n": h["n"], "combiner": f"{g}/{h['rule']}/{h['numbering']}"},
                          "notes": f"start {h['start1']}, rotation {r2}"})
    bounds = {"family": "two key words joined by a combiner other than addition on the std/KRYPTOS numbering",
              "combiners": {"add": "a + b on a keyword-mixed numbering of a vocabulary word (new numberings; std/KRY were 0115)",
                            "mul": "a x b mod 26 on std, KRYPTOS or any vocabulary numbering"},
              "numberings": len(numberings), "puzzle_words": len(puzzle), "table_rules": len(rules),
              "second_word_lengths": [3, 24], "cases_per_text": n_cases,
              "consistent_k4": {g: consistent[g][0] for g in consistent}, "consistent_controls": {g: consistent[g][1:NC] for g in consistent},
              "fully_forced_k4": {g: forced[g][0] for g in forced}, "fully_forced_controls": {g: forced[g][1:NC] for g in forced},
              "too_open_k4": {g: too_open[g][0] for g in too_open}, "too_open_controls": {g: too_open[g][1:NC] for g in too_open},
              "hits_k4": {g: len(hits[g][0]) for g in hits}, "hits_controls": {g: [len(x) for x in hits[g][1:NC]] for g in hits},
              "plants": [{"key": k, "found": any(h["word2"] == k["word2"] and h["word1"] == k["word1"] for g in hits for h in hits[g][NC + i])} for i, k in enumerate(plant_keys)],
              "k4_hits": {g: hits[g][0][:20] for g in hits}, "seconds": round(time.time() - t0),
              "controls": f"{N_CONTROLS} shuffled coppers (seed 1740), identical search", "exhaustive": True}
    notes = ("; ".join(f"{g}: consistent K4 {consistent[g][0]:,} (coppers {min(consistent[g][1:NC]):,}-{max(consistent[g][1:NC]):,}), "
                       f"dictionary hits K4 {len(hits[g][0])} (coppers {min(len(x) for x in hits[g][1:NC])}-{max(len(x) for x in hits[g][1:NC])})"
                       for g in ("add", "mul"))) + f"; plants found {sum(p['found'] for p in bounds['plants'])}/2"
    return {"candidates": cands, "bounds": bounds, "notes": notes, "controls": []}


def encrypt(plaintext, key):
    g, mode, pa, ca, nname = key["combiner"].split("/", 4)
    NA = STD if nname == "std" else KRY if nname == "kry" else keyword_mixed(nname.split(":")[1])
    NI = {c: i for i, c in enumerate(NA)}
    PI = {c: i for i, c in enumerate(ALPH[pa])}; CA = ALPH[ca]
    w1, o1, w2, r2 = key["word1"], key["start1"], key["word2"], key["rotation2"]
    key2 = w2[r2:] + w2[:r2]
    out = []
    for i, ch in enumerate(plaintext):
        x, y = NI[w1[(i + o1) % len(w1)]], NI[key2[i % len(key2)]]
        k = (x + y) % 26 if g == "add" else (x * y) % 26
        p = PI[ch]
        out.append(CA[{"vig": (p + k) % 26, "beau": (k - p) % 26, "var": (p - k) % 26}[mode]])
    return "".join(out)


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    NA = keyword_mixed("BERLIN"); NI = {c: i for i, c in enumerate(NA)}; I = {c: i for i, c in enumerate(KRY)}
    w1 = "PALIMPSEST"
    lines = [f"numbering by the alphabet mixed from BERLIN: {NA}", "sculpture's table (KRYPTOS alphabet, Vigenere); first word PALIMPSEST from its P at place 1; second word of length 8", "",
             "place  known  carved  key value  first letter (number)  second word's number  slot (mod 8)"]
    slots = {}
    for q in sorted(known):
        k = (I[ct[q - 1]] - I[known[q]]) % 26
        a = w1[(q - 1) % 10]
        b = (k - NI[a]) % 26
        slots.setdefault((q - 1) % 8, set()).add(b)
        if q in (22, 23, 24, 25, 30, 31, 64):
            lines.append(f"{q:>5}  {known[q]:>5}  {ct[q - 1]:>6}  {k:>9}  {a + ' (' + str(NI[a]) + ')':>21}  {b:>20}  {(q - 1) % 8:>12}")
    clash = sorted(s for s, v in slots.items() if len(v) > 1)
    lines += ["", f"slots asked for two different numbers: {clash}: this pair is dead" if clash else "no clash: look up the 8 letters"]
    return "\n".join(lines)
