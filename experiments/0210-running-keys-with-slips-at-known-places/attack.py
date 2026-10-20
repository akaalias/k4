"""Experiment 0210. See program.md for the contract."""

EXPERIMENT = {
    "slug": "running-keys-with-slips-at-known-places",
    "title": "A1.3: running keys from the named texts (K1-K3, the sculpture's texts, Carter, Sanborn's letters) on the standard, KRYPTOS and keyword tables, with up to seven of the 24 known letters carved wrong, exact, against scrambled copies, with planted slipped messages",
    "family": "1-keyed-periodic",
    "parent": "0047-running-key-carter-and-sculpture-mixed-alphabets",
    "changed": (
        "A1.3 (Stage 2, step 2, issue #76). 0004, 0017, 0021, 0045, 0047 and 0078 slid running keys from the named texts "
        "along K4 and asked for 0, at most 2 (0021, 0045, 0047) or at most 3 (0017) mismatches at the 24 known places; "
        "0004 and 0078 reported best 16 and 15. Here every one of those searches is rerun in one pass allowing up to 7 "
        "slips, exact, by a pigeonhole index (with 7 or fewer slips, one of 8 blocks of 3 known places matches exactly), "
        "K4 against 20 scrambled copies, with three planted running-key messages carrying 2-3 slips. The item asks for "
        "k = 1-3; k up to 7 costs nothing more and shows how far the test reaches."
    ),
    "hypothesis_expert": (
        "A1 (knowledge/12-assumptions.md); C7(a) and C6(a) (keys from the earlier texts and the sculpture: Sanborn 2005 "
        "'instructions in the earlier text that refer to later text', Scheidt 2003 'the keys were concealed at the "
        "sculpture'), C17 (a copper not as intended), C27(a) (the PALIMPCEST slip). A running key fixes every key letter "
        "from the text and the offset, so each setting gives one full reading and 24 checks. Setups: plain and cipher "
        "alphabets standard, KRYPTOS or keyword-mixed from the 61 vocabulary words (0045's pool of 63); K1-K3 sources "
        "with every pair (as 0045); Carter's Tomb of Tut-ankh-Amen vol. 1, the carved tableau (rows, rows with the index "
        "column, columns), the Morse (as carved, reversed order), the four ciphertexts as one panel and Sanborn's 1989 "
        "letter, the 1991 dedication texts and the 2025 open letter with one side standard or KRYPTOS or both sides the "
        "same keyword alphabet (as 0047, 0017, 0078); key letters on the standard or KRYPTOS order (or the keyword "
        "alphabet itself when both sides share it, as 0078); Vigenere, Beaufort, variant; every cyclic offset, forward and "
        "backward. A slip at a known place is one failed check; settings with 24 - k checks matched are counted for k = "
        "0-7. Chance of one setting with k <= 3 among the ~1.2 x 10^9 trials: about 10^-17; with k <= 7 about 10^-9, so "
        "the 24 checks decide the running key at every k <= 7 (the key costs a source name and an offset, about 25 "
        "bits; the slips 4.7 k + log2 C(24, k) bits). Readings of any setting found go to quadgrams and the blind judge "
        "with the copies'."
    ),
    "hypothesis_eli5": (
        "A running key uses a long text, a page of a book or the sculpture's own letters, as the secret word, one letter "
        "of the text for each letter of the message. Earlier experiments slid every text we could think of along the "
        "carving and found none that gives the 24 known letters. If Sanborn slipped at two or three of those places, the "
        "right text would have been thrown away. Here we let up to seven of them be wrong, on the carving and on "
        "scrambled copies, and we hide three messages of our own, with slips, to check they are found."
    ),
    "prediction": (
        "No setting with 7 or fewer slips on K4 or on any copy (chance about 10^-9). The three planted messages are found "
        "at their own source, offset and table, each with exactly its planted slips, and their readings judged as English. "
        "Zero candidates on K4."
    ),
    "method": (
        "1. Build the sources and the alphabet pool as 0045, 0047, 0017, 0078. 2. For every source and key alphabet, index "
        "each offset by the key letters it puts on each of 8 blocks of 3 known places. 3. For every setup, compute the key "
        "letter each known place needs; look up the offsets that match a whole block; check those offsets on all 24 "
        "places. 4. Keep every setting with 7 or fewer mismatches, by count. 5. K4, 20 copies and three planted messages "
        "(with 10 copies each); readings of any setting found to quadgrams and the judge in one call."
    ),
    "walkthrough": (
        "1. Write the key text (say Carter's book) under K4 from some starting letter. "
        "2. At each of the 24 known places, look up on the table which carved letter the known letter and the key letter give. "
        "3. Count the places where it is not the carved letter: those would be Sanborn's slips. "
        "4. Keep the starting letter if 3 or fewer places disagree, and read the whole message with it. "
        "5. Move the key text one letter and repeat, for every starting letter, both directions, every table. "
        "6. Do the same on scrambled copies of the carving."
    ),
}

import json
import math
import random
from pathlib import Path

from array import array

from kryptos.alphabets import keyword_mixed
from kryptos.ciphers import tableau_rows
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY, load_k1, load_k2, load_k3

N = 97
KMAX = 7
N_COPIES = 20
N_PLANT_COPIES = 10
ROOT = Path(__file__).resolve().parent
MODES = ("vig", "beau", "varbeau")
ENC = {"vig": lambda p, k: (p + k) % 26, "beau": lambda p, k: (k - p) % 26, "varbeau": lambda p, k: (p - k) % 26}
DEC = {"vig": lambda c, k: (c - k) % 26, "beau": lambda c, k: (k - c) % 26, "varbeau": lambda c, k: (c + k) % 26}
NEED = {"vig": lambda p, c: (c - p) % 26, "beau": lambda p, c: (c + p) % 26, "varbeau": lambda p, c: (p - c) % 26}


def letters(s):
    return "".join(c for c in s.upper() if "A" <= c <= "Z")


def pool_of(vocab):
    pool = {"std": STD, "kry": KRY}
    for w in vocab:
        if len(set(w)) >= 3:
            pool[f"{w}/keyword"] = keyword_mixed(w)
    seen, out = {}, {}
    for name, A in pool.items():
        if A not in seen:
            seen[A] = name; out[name] = A
    return out


def sources():
    """Group A: K1-K3 (0004, 0045). Group B: Carter, the sculpture's texts, Sanborn's letters (0017, 0021, 0047, 0078)."""
    k1, k2, k3 = load_k1(), load_k2(), load_k3()
    p1, p2, p3 = letters(k1["plaintext"]), letters(k2["plaintext_as_carved"]), letters(k3["plaintext"])
    p2c = letters(k2.get("plaintext_corrected_ending", "") or "")
    c1, c2, c3 = letters(k1["ciphertext"]), letters(k2["ciphertext_as_carved"]), letters(k3["ciphertext"])
    A = {"K1 plain": p1, "K2 plain": p2, "K3 plain": p3, "K1+K2+K3 plain": p1 + p2 + p3,
         "K1 cipher": c1, "K2 cipher": c2, "K3 cipher": c3, "K1+K2+K3 cipher": c1 + c2 + c3}
    if p2c and p2c != p2:
        A["K2 plain corrected ending"] = p2c
    site = json.loads((ROOT / "data" / "site_texts.json").read_text())
    rows = tableau_rows(carved=True)
    morse = [letters(m) for m in site["morse"]]
    k4 = letters((ROOT / "data" / "k4.txt").read_text())
    t = (ROOT / "knowledge" / "sources" / "sanborn-1989-letter-and-webster-1990-cryptogram.txt").read_text(errors="ignore")
    a_ = t.index("Dear Agency Employees"); b_ = t.index("Sincerely, Jim Sanborn") + len("Sincerely, Jim Sanborn")
    c_ = t.index("Remarks by William H. Webster")
    o = (ROOT / "knowledge" / "sources" / "openletter-2025.txt").read_text(errors="ignore")
    oa = o.index("Dear Kryptos fans"); ob = o.index("Jim Sanborn", o.index("All the best")) + len("Jim Sanborn")
    B = {"carter vol1": letters((ROOT / "knowledge" / "sources" / "carter-1923-tomb-of-tutankhamen-vol1.txt").read_text(errors="ignore")),
         "tableau rows": "".join(rows),
         "tableau rows with index column": "".join(STD[i] + r for i, r in enumerate(rows)),
         "tableau columns": "".join(r[c] for c in range(max(len(r) for r in rows)) for r in rows if c < len(r)),
         "morse as carved": "".join(morse), "morse reversed order": "".join(reversed(morse)),
         "right panel K1-K4": c1 + c2 + c3 + k4,
         "letter 1989": letters(t[a_:b_]), "Cryptogram 1991": letters(t[c_:]), "open letter 2025": letters(o[oa:ob])}
    out = {}
    for grp, src in (("A", A), ("B", B)):
        for name, s in src.items():
            out[name + " fwd"] = (grp, s)
            out[name + " bwd"] = (grp, s[::-1])
    return out


def setups(pool):
    """(group, pa name, ca name, ka name, mode). Group A: every pair; group B: one side std/kry, or both the same word."""
    names = list(pool)
    out = []
    for pa in names:
        for ca in names:
            kas = ["std", "kry"] + ([pa] if pa == ca and pa not in ("std", "kry") else [])
            for ka in kas:
                for m in MODES:
                    out.append(("A", pa, ca, ka, m))
                    if pa in ("std", "kry") or ca in ("std", "kry") or pa == ca:
                        out.append(("B", pa, ca, ka, m))
    return out


Q = None
POS = None
BLOCKS = None


def init(known):
    global Q, POS, BLOCKS
    Q = sorted(known)
    POS = {q: i for i, q in enumerate(Q)}
    BLOCKS = [Q[i:i + 3] for i in range(0, 24, 3)]  # 8 blocks of 3: 7 or fewer slips leave one whole


class Index:
    """For one source: per block of 3 known places, the offsets bucketed by the three key letters they put there.
    Keyed by letters, not by places in a key alphabet, so one index serves every table."""

    def __init__(self, s):
        self.s, self.n = s, len(s)
        n = self.n
        self.blocks = []
        for blk in BLOCKS:
            d = {}
            a, b, c = (q - 1 for q in blk)
            for o in range(n):
                d.setdefault(s[(o + a) % n] + s[(o + b) % n] + s[(o + c) % n], array("i")).append(o)
            self.blocks.append(d)

    def hits(self, need):
        """need: the key letter each of the 24 known places needs. Offsets with at most KMAX mismatches."""
        s, n = self.s, self.n
        seen, out = set(), []
        for d, blk in zip(self.blocks, BLOCKS):
            for o in d.get("".join(need[POS[q]] for q in blk), ()):
                if o in seen:
                    continue
                seen.add(o)
                mm = 0
                for i, q in enumerate(Q):
                    if s[(o + q - 1) % n] != need[i]:
                        mm += 1
                        if mm > KMAX:
                            break
                if mm <= KMAX:
                    out.append((o, mm))
        return out


def search(text, known, pool, srcs, sets, idx_cache):
    """Every setting with <= KMAX mismatches: (source, offset, setup, mismatches)."""
    found = []
    for grp, pa, ca, ka, m in sets:
        PA, CA, KA = pool[pa], pool[ca], pool[ka]
        need = [KA[NEED[m](PA.index(known[q]), CA.index(text[q - 1]))] for q in Q]
        for sname, (g, s) in srcs.items():
            if g != grp:
                continue
            if sname not in idx_cache:
                idx_cache[sname] = Index(s)
            for o, mm in idx_cache[sname].hits(need):
                found.append({"source": sname, "offset": o, "pa": pa, "ca": ca, "ka": ka, "m": m, "mismatches": mm})
    return found


def decrypt(text, f, pool, srcs):
    s = srcs[f["source"]][1]; n = len(s)
    PA, CA, KA = pool[f["pa"]], pool[f["ca"]], pool[f["ka"]]
    return "".join(PA[DEC[f["m"]](CA.index(text[i]), KA.index(s[(f["offset"] + i) % n]))] for i in range(N))


def encrypt(plaintext, key):
    """key: source text (name), offset, pa, ca, ka (alphabet strings), m, slips [[place, carved letter], ...]."""
    s = sources()[key["source"]][1]; n = len(s); o = key["offset"]
    pa, ca, ka, m = key["pa"], key["ca"], key["ka"], key["m"]
    out = [ca[ENC[m](pa.index(p), ka.index(s[(o + i) % n]))] for i, p in enumerate(plaintext)]
    for q, ch in key.get("slips", []):
        out[q - 1] = ch
    return "".join(out)


def shuffled(text, seed):
    l_ = list(text)
    random.Random(seed).shuffle(l_)
    return "".join(l_)


PLANTS = [  # (seed, source, setup (pa, ca, ka, m), slips)
    (2101, "carter vol1 fwd", ("std", "kry", "kry", "vig"), 3),
    (2102, "K1+K2+K3 plain fwd", ("SHADOW/keyword", "std", "std", "beau"), 2),
    (2103, "tableau rows bwd", ("kry", "kry", "kry", "varbeau"), 3),
]


def make_plant(seed, sname, setup, k, pool, srcs, known):
    from kryptos.plants import english_plant
    rng = random.Random(seed)
    pt = english_plant(seed)
    s = srcs[sname][1]
    o = rng.randrange(len(s))
    pa, ca, ka, m = setup
    key = {"source": sname, "offset": o, "pa": pool[pa], "ca": pool[ca], "ka": pool[ka], "m": m}
    ct = list(encrypt(pt, key))
    places = sorted(rng.sample(sorted(known), k))
    for q in places:
        ct[q - 1] = rng.choice([c for c in STD if c != ct[q - 1]])
    return pt, "".join(ct), o, places


def run(ctx):
    known = ctx.KNOWN
    init(known)
    pool = pool_of(list(ctx.vocabulary))
    srcs = sources()
    sets = setups(pool)
    cache = {}
    trials = sum(len(s) for g, s in srcs.values() if g == "A") * sum(1 for x in sets if x[0] == "A") + \
        sum(len(s) for g, s in srcs.values() if g == "B") * sum(1 for x in sets if x[0] == "B")
    # plants first, so the clock never cuts them
    plants = []
    for seed, sname, setup, k in PLANTS:
        if setup[0] not in pool:
            raise ValueError(setup)
        pt, ct, o, places = make_plant(seed, sname, setup, k, pool, srcs, known)
        f = search(ct, known, pool, srcs, sets, cache)
        own = [len(search(shuffled(ct, seed * 100 + i), known, pool, srcs, sets, cache)) for i in range(N_PLANT_COPIES)]
        hit = [x for x in f if x["source"] == sname and x["offset"] == o and (x["pa"], x["ca"], x["ka"], x["m"]) == setup]
        plants.append({"seed": seed, "source": sname, "offset": o, "setup": "/".join(setup), "k": k, "slips": places,
                       "pt": pt, "settings": len(f), "by_mismatches": [sum(1 for x in f if x["mismatches"] == d) for d in range(KMAX + 1)],
                       "hit": hit[0] if hit else None, "own_copies_settings": own, "ct": ct})
    k4 = search(ctx.K4, known, pool, srcs, sets, cache)
    copies = []
    for i in range(N_COPIES):
        if ctx.time_left() < 120:
            break
        copies.append(search(shuffled(ctx.K4, 2110 + i), known, pool, srcs, sets, cache))

    # readings: every setting found, K4's, copies' and plants', to quadgrams and the judge in one call
    texts = []
    for f in k4:
        f["reading"] = decrypt(ctx.K4, f, pool, srcs); texts.append(f["reading"])
    for i, cf in enumerate(copies):
        for f in cf:
            f["reading"] = decrypt(shuffled(ctx.K4, 2110 + i), f, pool, srcs); texts.append(f["reading"])
    for p in plants:
        if p["hit"]:
            p["hit"]["reading"] = decrypt(p["ct"], p["hit"], pool, srcs); texts.append(p["hit"]["reading"])
    uniq = sorted(set(texts))
    verdicts = dict(zip(uniq, ctx.judge(uniq))) if uniq else {}

    def jq(r):
        free = "".join(c for i, c in enumerate(r, start=1) if i not in known)
        return {"quad": round(ctx.english_score(free), 3), "judge": verdicts[r]["score"], "judge_reading": verdicts[r]["reading"]}

    for f in k4:
        f.update(jq(f["reading"]))
    copies_best = []
    for cf in copies:
        sc = [jq(f["reading"])["judge"] for f in cf]
        sc = [x for x in sc if x is not None]
        copies_best.append(max(sc) if sc else None)
    plant_out = []
    for p in plants:
        h = p["hit"]
        ok = bool(h) and h["mismatches"] == p["k"] and all(
            c == p["pt"][i] for i, c in enumerate(h["reading"]) if (i + 1) not in known)
        extra = jq(h["reading"]) if h else {}
        plant_out.append({"seed": p["seed"], "source": p["source"], "offset": p["offset"], "setup": p["setup"], "k": p["k"],
                          "slips": p["slips"], "settings_found": p["settings"], "by_mismatches": p["by_mismatches"],
                          "planted_setting_mismatches": h["mismatches"] if h else None, **extra,
                          "own_copies_settings": p["own_copies_settings"],
                          "found": bool(ok and max(p["own_copies_settings"]) == 0 and p["settings"] >= 1)})
    cands = []
    for f in sorted(k4, key=lambda f: f["mismatches"])[:50]:
        pt = "".join(known.get(i + 1, ch) for i, ch in enumerate(f["reading"]))
        key = {"source": f["source"], "offset": f["offset"], "pa": pool[f["pa"]], "ca": pool[f["ca"]], "ka": pool[f["ka"]], "m": f["m"]}
        re_ = encrypt(pt, key)
        slips = [[q, ctx.K4[q - 1]] for q in sorted(known) if re_[q - 1] != ctx.K4[q - 1]]
        key["slips"] = slips
        cands.append({"plaintext": pt, "key": key, "key_bits": 25 + 4.7 * len(slips) + (math.log2(math.comb(24, len(slips))) if slips else 0),
                      "key_description": f"running key {f['source']} offset {f['offset']}; {f['pa']}/{f['ca']}/{f['ka']} {f['m']}; slips {slips}",
                      "notes": f"judge {f.get('judge')}, quadgram {f.get('quad')}"})
    by_k = lambda fs: [sum(1 for x in fs if x["mismatches"] == d) for d in range(KMAX + 1)]  # noqa: E731
    return {
        "candidates": cands,
        "controls": [-9.0] * len(copies) if not any(copies) else [],
        "bounds": {
            "family": "running keys from the named texts on standard, KRYPTOS and keyword tables, 0-7 known letters slipped (A1.3)",
            "alphabet_pool": len(pool), "setups": {"A (K1-K3, every pair)": sum(1 for x in sets if x[0] == "A"),
                                                   "B (other sources, one side std/kry or both the same word)": sum(1 for x in sets if x[0] == "B")},
            "sources": {k: len(v[1]) for k, v in srcs.items()},
            "trials": trials, "offsets": "every cyclic offset, forward and backward",
            "max_slips": KMAX, "method": "pigeonhole index: 8 blocks of 3 known places, offsets bucketed by their key letters; every offset matching a whole block checked on all 24 (exact for <= 7)",
            "slip_cost_bits": {k: round(4.7 * k + math.log2(math.comb(24, k)), 1) for k in range(1, KMAX + 1)},
            "chance_settings_at_k": {k: f"{trials * math.comb(24, k) * (25 / 26) ** k * (1 / 26) ** (24 - k):.1e}" for k in range(0, KMAX + 1)},
            "k4_settings_by_mismatches": by_k(k4), "k4_settings": [{x: f[x] for x in ("source", "offset", "pa", "ca", "ka", "m", "mismatches", "judge", "quad")} for f in k4][:50],
            "copies_settings_by_mismatches": [by_k(c) for c in copies], "copies_done": len(copies),
            "copies_judge_best": copies_best,
            "judge": {"sent": len(uniq), "none": sum(1 for v in verdicts.values() if v["score"] is None)},
            "plants": plant_out,
            "covers": "0004, 0017, 0021, 0045, 0047, 0078 (their sources, tables and rules); not 0098/0154 (free alphabet) or 0117 (with moves)",
            "controls": f"{N_COPIES} shuffled copies (seeds 2110-2129); each plant against {N_PLANT_COPIES} shuffles of its own ciphertext",
            "exhaustive": "yes",
        },
        "notes": f"{trials:,} trials; K4 settings with <= {KMAX} slips {len(k4)}; copies {[len(c) for c in copies]}; plants found {[p['found'] for p in plant_out]}",
    }


def worked_example(ctx, key):
    init(ctx.KNOWN)
    srcs = sources()
    s = srcs["carter vol1 fwd"][1]
    o = 1000
    lines = ["Carter's book as the key, from letter 1000, standard plain and KRYPTOS cipher alphabet, key letters on KRYPTOS, Vigenere", "",
             "place  known  key  gives  carved"]
    miss = 0
    for q in sorted(ctx.KNOWN):
        k = s[(o + q - 1) % len(s)]
        c = KRY[ENC["vig"](STD.index(ctx.KNOWN[q]), KRY.index(k))]
        miss += c != ctx.K4[q - 1]
        if q in (22, 23, 24, 25, 64, 65, 66):
            lines.append(f"{q:>5}  {ctx.KNOWN[q]:>5}  {k:>3}  {c:>5}  {ctx.K4[q - 1]:>6}{'' if c == ctx.K4[q - 1] else '   slip?'}")
    lines.append("")
    lines.append(f"places that disagree, of 24: {miss} (7 or fewer would be kept)")
    return "\n".join(lines)
