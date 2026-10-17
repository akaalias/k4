"""Experiment 0183 (F2.3). See program.md for the contract."""

EXPERIMENT = {
    "slug": "repeated-letter-phrase-homophones",
    "title": "F2.3: a 26-letter phrase with repeated letters as the plain strip, so a letter may be enciphered from any of its places (homophones that keep the length), repeating key 1-26: exact",
    "family": "2-masked-then-keyed",
    "parent": "0057-letter-nulls-outside-the-cribs",
    "changed": (
        "F2.3. Not a documented method: the reverse use of EMC par. 45b derived in research_notes/Scheidt patents and "
        "field ciphers/addendum_downloaded_manuals.md (issue #9), and stated as such. The plain strip is a 26-letter "
        "phrase with its repeats (NOWISTHETIMEFORALLGOODMENT...); a letter that occurs twice may be taken from either "
        "place; the cipher strip is the standard or KRYPTOS order, slid by a repeating key. Phrases: every 26-letter "
        "window of the K1, K2 and K3 plaintexts, the Morse texts, Carter's 1923 book (K3's source) and famous sentences, kept if they hold the 13 "
        "letters of the known words. At each known place the allowed key values form a set; sets intersect per key slot. "
        "Lengths 1-26, slide either way; K4 against 20 shuffled copies."
    ),
    "hypothesis_expert": (
        "Scheidt: 'I masked the English language' (C2): homophones flatten letter counts without lengthening the text "
        "(K4's flat counts, 0056). EMC par. 45b (keyword phrases with repeated letters for components), reversed here as a "
        "derivation (addendum, candidate 3). Model: c_i = C[(j + k_{i mod L}) mod 26] or C[(k - j) mod 26] with phrase[j] = "
        "p_i, the choice of j free. Exact: allowed k per known place = {C^-1(c) -+ j : phrase[j] = p}, intersected per slot. "
        "Statistic: live (phrase, strip, form, L) cells with at least one check, K4 against copies."
    ),
    "hypothesis_eli5": (
        "Write a phrase such as NOW IS THE TIME FOR ALL GOOD MEN on a strip instead of the alphabet. Letters that appear "
        "twice give the encipherer a choice, so the same plain letter can turn into different code letters, yet the "
        "message stays the same length. Slide the strip against an alphabet by a repeating secret word. For each phrase "
        "from the sculpture's own texts, the 24 known letters say which secret words remain possible."
    ),
    "prediction": "Live cells with checks at the shuffled copies' rate; homophones loosen each check, so short lengths may survive on copies as on K4. Zero candidates.",
    "method": (
        "1. Phrases: 26-letter windows of K1-K3, the Morse, Carter's book, famous sentences; keep those with E A S T N O R H B L I C K. "
        "2. For each text, phrase, cipher strip (standard, KRYPTOS) and form (j + k, k - j): allowed key values per known "
        "place. "
        "3. For lengths 1-26: intersect per slot; live if no slot is empty. "
        "4. K4 against 20 shuffled copies; a planted text as a builder check."
    ),
    "walkthrough": (
        "1. Write the phrase on the plain strip; E stands at, say, places 3 and 9 of it. "
        "2. The known E at place 22 is carved F: F sits at place 5 of the standard cipher strip. "
        "3. So the key there is 5 - 3 = 2 or 5 - 9 = 22: either is allowed. "
        "4. For a key of length 7, place 29 shares that slot: its allowed values must include 2 or 22. "
        "5. A slot with no common value kills the length. Repeat for every phrase and length, and on copies."
    ),
}

import json
import random
from pathlib import Path

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY, KNOWN

N_CONTROLS = 20
ALPH = {"std": STD, "kry": KRY}
PLACES = sorted(KNOWN)
KP = [q - 1 for q in PLACES]
NEED = set("EASTNORHBLICK")
ROOT = Path(__file__).resolve().parent
if not (ROOT / "kryptos").exists():
    ROOT = Path.cwd()
FAMOUS = [
    "NOWISTHETIMEFORALLGOODMENTOCOMETOTHEAIDOFTHEIRCOUNTRY",
    "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG",
    "FOURSCOREANDSEVENYEARSAGOOURFATHERSBROUGHTFORTH",
    "TOBEORNOTTOBETHATISTHEQUESTION",
    "ASKNOTWHATYOURCOUNTRYCANDOFORYOU",
    "ICHBINEINBERLINER",
    "MRGORBACHEVTEARDOWNTHISWALL",
    "WONDERFULTHINGSICANSEEWONDERFULTHINGS",
    "INGODWETRUST",
    "EPLURIBUSUNUM",
]


def phrases():
    src = {}
    for k in ("k1", "k2", "k3"):
        d = json.load(open(ROOT / "data" / f"{k}.json"))
        pt = d.get("plaintext") or d.get("plaintext_as_carved")
        src[k] = "".join(c for c in pt.upper() if c.isalpha())
    st = json.load(open(ROOT / "data" / "site_texts.json"))
    src["morse"] = "".join(c for c in "".join(st["morse"]).upper() if c.isalpha())
    for i, f in enumerate(FAMOUS):
        src[f"famous {i}"] = f
    carter = ROOT / "knowledge" / "sources" / "carter-1923-tomb-of-tutankhamen-vol1.txt"
    if carter.exists():
        src["Carter 1923"] = "".join(c for c in carter.read_text(errors="ignore").upper() if "A" <= c <= "Z")
    out = {}
    for name, t in src.items():
        for o in range(0, max(1, len(t) - 25)):
            w = t[o:o + 26]
            if len(w) == 26 and NEED <= set(w) and w not in out:
                out[w] = f"{name} @{o}"
    return out


def allowed_sets(text, phrase, strip, form):
    C = {c: i for i, c in enumerate(ALPH[strip])}
    pos = {}
    for j, ch in enumerate(phrase):
        pos.setdefault(ch, []).append(j)
    sets = []
    for q in PLACES:
        c = C[text[q - 1]]
        js = pos[KNOWN[q]]
        m = 0
        for j in js:
            k = (c - j) % 26 if form == "j+k" else (c + j) % 26
            m |= 1 << k
        sets.append(m)
    return sets


CHECKS = {L: 24 - len({k % L for k in KP}) for L in range(1, 27)}


def live_lengths(sets):
    out = []
    for L in range(1, 27):
        if CHECKS[L] < 1:
            continue
        slot = {}
        ok = True
        for e, k in enumerate(KP):
            s = k % L
            slot[s] = slot.get(s, (1 << 26) - 1) & sets[e]
            if not slot[s]:
                ok = False
                break
        if ok:
            out.append(L)
    return out


def encipher(p, phrase, strip, form, key, rng):
    A = ALPH[strip]
    pos = {}
    for j, ch in enumerate(phrase):
        pos.setdefault(ch, []).append(j)
    out = []
    for i, ch in enumerate(p):
        j = rng.choice(pos[ch])
        k = key[i % len(key)]
        out.append(A[(j + k) % 26] if form == "j+k" else A[(k - j) % 26])
    return "".join(out)


def run(ctx):
    ct = ctx.K4
    PH = phrases()
    rng = random.Random(1830)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    # builder check: a plant whose message uses only the phrase's letters
    ph0 = next(iter(PH))
    letters = set(ph0)
    base = "".join(ch for ch in "THEYUSEDTHEEARTHSMAGNETICFIELDTHEINFORMATIONWASGATHEREDANDTRANSMITTEDTOANUNKNOWNLOCATIONSLOWLYDESPERATELY" if ch in letters)
    p = list((base * 2)[:97])
    for q, ch in KNOWN.items():
        p[q - 1] = ch
    plant = encipher("".join(p), ph0, "kry", "j+k", [rng.randrange(26) for _ in range(7)], rng)
    plant_live = 7 in live_lengths(allowed_sets(plant, ph0, "kry", "j+k"))

    counts = []
    by_len = []
    k4_live = []
    for ti, t in enumerate(texts):
        n = 0
        bl = {}
        for ph, where in PH.items():
            for strip in ALPH:
                for form in ("j+k", "k-j"):
                    ls = live_lengths(allowed_sets(t, ph, strip, form))
                    n += len(ls)
                    for L in ls:
                        bl[L] = bl.get(L, 0) + 1
                    if ti == 0 and ls:
                        k4_live.append({"phrase": ph, "from": where, "strip": strip, "form": form, "lengths": ls})
        counts.append(n); by_len.append(bl)
    per_len = {L: {"k4": by_len[0].get(L, 0), "copies_min": min(b.get(L, 0) for b in by_len[1:]),
                   "copies_max": max(b.get(L, 0) for b in by_len[1:]), "checks": CHECKS[L]} for L in range(1, 27) if CHECKS[L] >= 1}
    above = [L for L, v in per_len.items() if v["k4"] > v["copies_max"]]
    k4_live.sort(key=lambda z: min(z["lengths"]))
    bounds = {
        "family": "repeated-letter phrase as plain strip (homophones keeping the length), cipher strip std/KRYPTOS, slide j+k or k-j, repeating key 1-26, exact; a derivation from EMC 45b, not a documented method",
        "phrases": len(PH), "cells_per_text": len(PH) * 4 * sum(1 for L in CHECKS if CHECKS[L] >= 1),
        "live_cells": {"k4": counts[0], "copies": counts[1:]}, "per_length": per_len, "lengths_k4_above_every_copy": above,
        "k4_live_shortest": k4_live[:15], "plant": {"phrase": ph0, "length": 7, "live": plant_live},
        "copies": f"{N_CONTROLS} shuffled copies (seed 1830)", "exhaustive": True,
    }
    notes = (f"{len(PH)} phrases; live cells K4 {counts[0]} (copies {min(counts[1:])}-{max(counts[1:])}); lengths where K4 is above every copy: {above}; plant live {plant_live}")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct = ctx.K4
    ph = "NOWISTHETIMEFORALLGOODMENT"
    lines = [f"phrase strip {ph} (lacks C, K: such a phrase is dropped)", ""]
    for q in PLACES[:8]:
        js = [j for j, ch in enumerate(ph) if ch == KNOWN[q]]
        c = STD.index(ct[q - 1])
        lines.append(f"place {q}: {KNOWN[q]} at strip places {js}, carved {ct[q - 1]} at {c}: allowed keys {sorted((c - j) % 26 for j in js)}")
    return "\n".join(lines)
