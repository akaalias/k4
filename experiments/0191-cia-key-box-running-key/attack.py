"""Experiment 0191 (F11.3). See program.md for the contract."""

EXPERIMENT = {
    "slug": "cia-key-box-running-key",
    "title": "F11.3: the CIA's Polish agent key box: a key text written into a box by rows and read out by columns, then a reciprocal or other table; K1-K3, the Morse and Carter's book as key texts: exact",
    "family": "11-agency-hand-systems",
    "parent": "0190-poem-code-double-transposition",
    "changed": (
        "F11.3. Bury (Cryptologia 2007, via scz.bplaced.net 9.2): the agent writes a verse row by row into a 10 x 10 box, "
        "reads it out by columns, and combines the result with the message through a 26 x 26 reciprocal table "
        "(p + k + c = 25). The report's scratch check (K1-K3, best 7 of 24, no controls) is rerun with controls and widened: "
        "key texts K1, K2, K3 and K1-K3 joined, the Morse, and Carter's 1923 book (K3's source); box widths 2-50, rows as "
        "many as 97 letters need; columns read left to right, right to left, bottom to top, or in a vocabulary keyword's "
        "order; tables: Bury's reciprocal, Vigenere, Beaufort and variant, numbered on the standard or KRYPTOS order; "
        "every start in the key text. Each setting checks all 24 known letters (compiled); K4 against 10 shuffled copies."
    ),
    "hypothesis_expert": (
        "A9, F11: the CIA's own documented 1970s agent system, a remembered rule, 'a matrix, then the table' (C1). Model: "
        "key stream k_i = T[o + r_i w + col(j_i)], j_i = i div h, r_i = i mod h (h = ceil(97 / w)), then c from p and k "
        "by the table rule. Exact: a setting fits only if all 24 known letters agree. Statistic: fitting settings and, for "
        "the short key texts, the best number of agreeing known letters, K4 against 10 copies; plants."
    ),
    "hypothesis_eli5": (
        "The CIA's agents in 1970s Poland took a line of a book, wrote it into a square box row by row, copied it out "
        "column by column, and used that jumble as the key on a letter table. Sanborn's 'matrix, then the table' fits this "
        "well. We try the sculpture's own texts and the Carter book behind K3 as the key text, every box width, every "
        "starting point."
    ),
    "prediction": "No setting fits all 24 known letters on K4 or on the copies; the best partial agreement on K4 lies inside the copies' range (about 7-8 of 24). Zero candidates.",
    "method": (
        "1. Key texts: K1, K2, K3, K1-K3 joined, the Morse, Carter's book. "
        "2. For each width 2-50 and column order: the offset of each known place's key letter from the start. "
        "3. For each table rule and text: the key letter each known place needs. "
        "4. Every start: fit if all 24 agree (compiled); best agreement for the short key texts. "
        "5. K4 against 10 shuffled copies; two plants."
    ),
    "walkthrough": (
        "1. Take K2's plaintext from its 40th letter and write it into a box 10 wide, row by row. "
        "2. Read it out column by column: the first 10 letters of the key come from the first column, and so on. "
        "3. Place 22 of the message takes the key letter in column 3, row 2 of the box. "
        "4. On Bury's table, E over the carved F needs one particular key letter; check whether the box gives it. "
        "5. Every start, width, column order and table, on K4 and on scrambled copies."
    ),
}

import ctypes
import os
import random
import subprocess
import tempfile
import time
from pathlib import Path

from kryptos.facts import KNOWN, STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N_CONTROLS = 10
PLACES = sorted(KNOWN)
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

C_SOURCE = r"""
// Key box: key text T (letter numbers), a reading = 24 index offsets d[e] from the start o; needed key values
// kv[t][e] per text. For every start o: fit if T[o + d[e]] == kv[t][e] for all 24; also the best number of hits
// (full count) when want_hits is set.
long scan(const int *T, int N, const int *d, int maxd, const int *kv, int nt, long *fits, int *besthits, int want_hits,
          int *fit_o, int cap, int *nfit) {
    long settings = 0;
    for (int o = 0; o + maxd < N; o++) {
        settings++;
        for (int t = 0; t < nt; t++) {
            const int *k = kv + 24 * t;
            if (want_hits) {
                int h = 0;
                for (int e = 0; e < 24; e++) h += T[o + d[e]] == k[e];
                if (h > besthits[t]) besthits[t] = h;
                if (h == 24) { fits[t]++; if (t == 0 && *nfit < cap) fit_o[(*nfit)++] = o; }
            } else {
                int e = 0;
                while (e < 24 && T[o + d[e]] == k[e]) e++;
                if (e == 24) { fits[t]++; if (t == 0 && *nfit < cap) fit_o[(*nfit)++] = o; }
            }
        }
    }
    return settings;
}
"""


def build():
    d = tempfile.mkdtemp(prefix="k4_kbox_")
    src, so = os.path.join(d, "c.c"), os.path.join(d, "c.so")
    open(src, "w").write(C_SOURCE)
    subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", so, src], check=True, capture_output=True)
    lib = ctypes.CDLL(so)
    lib.scan.restype = ctypes.c_long
    return lib


def I(v):
    return (ctypes.c_int * len(v))(*v)


def sources():
    words = SPACED.split()
    i2, i3 = words.index("IT"), words.index("SLOWLY")
    j = lambda ws: "".join(ws)
    import json
    st = json.load(open(ROOT / "data" / "site_texts.json"))
    out = {"K1": j(words[:i2]), "K2": j(words[i2:i3]), "K3": j(words[i3:]), "K1-K3": j(words),
           "Morse": "".join(ch for ch in "".join(st["morse"]).upper() if ch.isalpha())}
    carter = ROOT / "knowledge" / "sources" / "carter-1923-tomb-of-tutankhamen-vol1.txt"
    out["Carter 1923"] = "".join(c for c in carter.read_text(errors="ignore").upper() if "A" <= c <= "Z")
    return out


def number_key(key):
    return sorted(range(len(key)), key=lambda i: (key[i], i))


def readings(vocab):
    out = []
    for w in range(2, 51):
        h = -(-97 // w)
        orders = {"left to right": list(range(w)), "right to left": list(range(w))[::-1]}
        for kw in vocab:
            if len(kw) == w:
                orders[f"keyword {kw}"] = number_key(kw)
        for name, order in orders.items():
            for up in (0, 1):
                d = []
                for i in range(97):
                    jj, r = i // h, i % h
                    if up:
                        r = h - 1 - r
                    d.append(r * w + order[jj])
                out.append((f"width {w}, columns {name}{', bottom to top' if up else ''}", [d[q - 1] for q in PLACES], max(d), d))
    return out


def rules():
    return [(a, f) for a in ("std", "kry") for f in ("vig", "beau", "var", "recip25")]


def needed(text, rule):
    A = STD if rule[0] == "std" else KRY
    out = []
    for q in PLACES:
        p, c = A.index(KNOWN[q]), A.index(text[q - 1])
        k = {"vig": (c - p) % 26, "beau": (c + p) % 26, "var": (p - c) % 26, "recip25": (25 - p - c) % 26}[rule[1]]
        out.append(STD.index(A[k]))          # the key letter, as the key text numbers it (A=0)
    return out


def encipher(p, keystream, rule):
    A = STD if rule[0] == "std" else KRY
    out = []
    for ch, k in zip(p, keystream):
        x = A.index(ch); kk = A.index(k)
        c = {"vig": (x + kk) % 26, "beau": (kk - x) % 26, "var": (x - kk) % 26, "recip25": (25 - x - kk) % 26}[rule[1]]
        out.append(A[c])
    return "".join(out)


def run(ctx):
    t0 = time.time()
    lib = build()
    ct = ctx.K4
    src = sources()
    vocab = sorted({w.upper() for w in ctx.vocabulary if w.isalpha() and 2 <= len(w) <= 50})
    R = readings(vocab)
    rng = random.Random(1910)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    PLANT_P = "USEDTHEEARTHSMAGNETICEASTNORTHEASTRMATIONWASGATHEREDANDTRANSMITBERLINCLOCKUNDTOANUNKNOWNLOCATIONX"
    plants = []
    for k in range(2):
        sname = ("K2", "Carter 1923")[k]
        T = src[sname]
        ri = [i for i, r in enumerate(R) if r[0] == ("width 10, columns left to right", "width 17, columns right to left, bottom to top")[k]][0]
        o = rng.randrange(len(T) - R[ri][2] - 1)
        ks = "".join(T[o + R[ri][3][i]] for i in range(97))
        rule = rules()[(3, 5)[k]]
        texts.append(encipher(PLANT_P, ks, rule))
        plants.append({"source": sname, "reading": R[ri][0], "start": o, "rule": "/".join(rule)})
    nt = len(texts)
    nc = 1 + N_CONTROLS
    per_source = {}
    k4_fits = []
    for sname, Ttxt in src.items():
        T = I([ord(c) - 65 for c in Ttxt])
        want = 1 if len(Ttxt) < 2000 else 0
        fits = [0] * nt
        best = [0] * nt
        settings = 0
        for rule in rules():
            kv = I([v for t in texts for v in needed(t, rule)])
            for name, d, maxd, _ in R:
                if maxd >= len(Ttxt):
                    continue
                f = (ctypes.c_long * nt)(); b = (ctypes.c_int * nt)()
                fo = (ctypes.c_int * 20)(); nf = ctypes.c_int(0)
                settings += lib.scan(T, len(Ttxt), I(d), maxd, kv, nt, f, b, want, fo, 20, ctypes.byref(nf))
                for t in range(nt):
                    fits[t] += f[t]; best[t] = max(best[t], b[t])
                for j in range(nf.value):
                    k4_fits.append({"source": sname, "reading": name, "rule": "/".join(rule), "start": fo[j]})
        per_source[sname] = {"settings": settings, "fits_k4": fits[0], "fits_copies": fits[1:nc], "fits_plants": fits[nc:],
                             "best_hits_k4": best[0] if want else None, "best_hits_copies": best[1:nc] if want else None}
    tot_settings = sum(v["settings"] for v in per_source.values())
    bounds = {
        "family": "key box: key text by rows, read by columns (widths 2-50, natural, reversed, bottom-up, vocabulary keyword orders), then Bury's reciprocal / Vigenere / Beaufort / variant on std or KRYPTOS numbering; every start; exact",
        "readings": len(R), "rules": 8, "settings_per_text": tot_settings, "per_source": per_source,
        "k4_fits": k4_fits[:20], "plants": plants,
        "copies": f"{N_CONTROLS} shuffled copies (seed 1910)", "seconds": round(time.time() - t0), "exhaustive": True,
    }
    notes = "; ".join(f"{k}: fits K4 {v['fits_k4']} (copies {min(v['fits_copies'])}-{max(v['fits_copies'])}, plants {v['fits_plants']})"
                      + (f", best K4 {v['best_hits_k4']}/24 (copies {min(v['best_hits_copies'])}-{max(v['best_hits_copies'])})" if v['best_hits_k4'] is not None else "")
                      for k, v in per_source.items())
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    T = sources()["K2"]
    w, h, o = 10, 10, 39
    ks = "".join(T[o + (i % h) * w + i // h] for i in range(97))
    need = needed(ctx.K4, ("std", "recip25"))
    lines = [f"K2 from its 40th letter in a box 10 wide, read by columns: key stream {ks}", ""]
    for e, q in enumerate(PLACES[:6]):
        lines.append(f"place {q}: box gives {ks[q - 1]}, Bury's table needs {STD[need[e]]} for {KNOWN[q]} over {ctx.K4[q - 1]}")
    return "\n".join(lines)
