"""Experiment 0205 (F2.4). See program.md for the contract."""

EXPERIMENT = {
    "slug": "nulls-at-both-ends",
    "title": "F2.4: a run of nulls at both ends of the message (SOE's Dutch section), the known letters moved by the start run, then a periodic or progressive key on the table, exact, with planted texts",
    "family": "2-masked-then-keyed",
    "parent": "0023-masks-reversal-and-nulls-then-tableau",
    "changed": (
        "F2.4 (issue #78): SOE's Dutch section put eight random letters at the beginning and at the end of each "
        "message (Marks p. 232). If K4's message is padded so, the known words sit s places later on the copper than "
        "in the message. The end run only shortens the message (s + e <= 23 keeps BERLINCLOCK inside); it moves "
        "nothing, so every pair of runs 0-12 reduces to the start run s. A key that starts with the message or with "
        "the copper is the same family (the offset is absorbed by the key word, for periodic and both progressive "
        "forms). 0023 tested start runs 1-24 with periodic keys; new here: the progressive key, per letter and per "
        "repeat, steps 1-25, lengths 1-52, on the 8 standard/KRYPTOS table classes, for s = 0-12, with periodic keys "
        "(step 0) rerun alongside, on K4, ten scrambled copies and planted texts."
    ),
    "hypothesis_expert": (
        "C4(a) (a mask that pads the plaintext), C17(b) (the working text longer than 97). Source: "
        "reports/marks-between-silk-and-cyanide.md. Model: carved = nulls(s) + T(message) + nulls(e), message "
        "positions of the known letters 22-34, 64-74 (Sanborn's numbering of the message), so carved places q + s; T a "
        "tableau key with value w[i mod L] + d i (per letter) or w[i mod L] + d floor(i/L) (per repeat), d 0-25, L 1-52, "
        "plain and cipher alphabets standard or KRYPTOS, added or Beaufort form (8 classes; the variant form is the "
        "added form with -w). Exact by slot agreement of the 24 forced values after removing the step. Statistic (fixed): "
        "per form, the shortest consistent length over all s and steps on K4 against the copies, and the cells "
        "(form, length) where K4's count of live (s, step, class) settings exceeds every copy's."
    ),
    "hypothesis_eli5": (
        "Wartime agents sometimes put a handful of meaningless letters before and after a message, so the real words "
        "do not start where an enemy expects. If Sanborn did that, the known words sit a few places further along the "
        "copper than in the message. We slide them along by 0 to 12 places and test every repeating or steadily "
        "sliding secret word on the sculpture's table."
    ),
    "prediction": (
        "For every start run, nothing consistent below length 24-26 with a periodic key (as 0023), and the progressive "
        "forms at the copies' rate; K4 above every copy in no more cells than a copy is. Planted texts found at their "
        "own setting. Zero candidates."
    ),
    "method": (
        "1. For each start run s = 0-12 and table class, the forced key value at each known letter, read at carved place q + s. "
        "2. For each form and step d, remove d i or d floor(i/L) and test slot agreement for every length L. "
        "3. Count live settings per (form, length) on K4, ten copies and two planted texts; the fixed statistic."
    ),
    "walkthrough": (
        "1. Put eight random letters before the message and some after it. "
        "2. Encipher the whole on the table with a key word that slides one step along the table after each full pass. "
        "3. To test: slide the known words eight places along the copper. "
        "4. At each, the table gives the key value; take away the slide for that pass. "
        "5. Known letters in the same slot of the key word must then agree."
    ),
}

import random
import time
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
N_CONTROLS = 10
LMAX = 52
SMAX = 12
CLASSES = [(pa, ca, be) for pa in (0, 1) for ca in (0, 1) for be in (0, 1)]
CLASS_NAME = lambda c: f"{('std', 'kry')[c[0]]}/{('std', 'kry')[c[1]]}/{'beau' if c[2] else 'vig-var'}"
FORMS = ("periodic", "per-letter", "per-repeat")


def forced(text, known_list, s, cls):
    pa, ca, be = (STD, KRY)[cls[0]], (STD, KRY)[cls[1]], cls[2]
    out = []
    for q, a in known_list:
        j = q - 1 + s
        C, P = ca.index(text[j]), pa.index(a)
        out.append((j, (C + P) % 26 if be else (C - P) % 26))
    return out


def live_lengths(fv, form, d):
    """Lengths L (1-LMAX) at which the forced values, with the step removed, agree within every slot."""
    res = []
    for L in range(1, LMAX + 1):
        slot = {}
        ok = True
        for j, f in fv:
            v = f if form == "periodic" else (f - d * j) % 26 if form == "per-letter" else (f - d * (j // L)) % 26
            if slot.setdefault(j % L, v) != v:
                ok = False
                break
        if ok:
            res.append(L)
    return res


def count(text, known_list):
    """live[form][L] = number of (s, class, step) settings live at L; first live per form."""
    live = {f: [0] * (LMAX + 1) for f in FORMS}
    ex = []
    for s in range(SMAX + 1):
        for ci, cls in enumerate(CLASSES):
            fv = forced(text, known_list, s, cls)
            for form in FORMS:
                for d in ([0] if form == "periodic" else range(1, 26)):
                    for L in live_lengths(fv, form, d):
                        live[form][L] += 1
                        if L < 24:
                            ex.append({"s": s, "class": CLASS_NAME(cls), "form": form, "step": d, "length": L})
    return live, ex


def encrypt_with(pt, s, e, cls, w, form, d, rng):
    pa, ca, be = (STD, KRY)[cls[0]], (STD, KRY)[cls[1]], cls[2]
    msg = pt[:N - s - e]
    full = "".join(rng.choice(STD) for _ in range(s)) + msg + "".join(rng.choice(STD) for _ in range(e))
    L = len(w)
    out = []
    for i, ch in enumerate(full):
        k = w[i % L] + (0 if form == "periodic" else d * i if form == "per-letter" else d * (i // L))
        P = pa.index(ch)
        out.append(ca[(k - P) % 26] if be else ca[(P + k) % 26])
    return "".join(out)


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    known_list = [(q, known[q]) for q in sorted(known)]
    t0 = time.time()
    from kryptos.plants import english_plant
    rng = random.Random(2400)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    # plants: the message (97 - s - e letters with the known words at their message places), padded
    plants = []
    for seed, s, e, ci, form, d, L in ((2401, 8, 8, 3, "per-repeat", 3, 9), (2402, 5, 11, 6, "per-letter", 7, 11)):
        prng = random.Random(seed)
        w = [prng.randrange(26) for _ in range(L)]
        plants.append({"seed": seed, "s": s, "e": e, "class": CLASSES[ci], "form": form, "step": d, "length": L,
                       "ct": encrypt_with(english_plant(seed), s, e, CLASSES[ci], w, form, d, prng)})
    res = [count(t, known_list) for t in texts]
    pres = [count(p["ct"], known_list) for p in plants]
    T = len(texts)
    stat = {}
    for form in FORMS:
        L_ = lambda t, L: res[t][0][form][L]
        first = lambda t: next((L for L in range(1, LMAX + 1) if L_(t, L)), None)
        above = lambda t: [L for L in range(1, LMAX + 1) if L_(t, L) > max(L_(u, L) for u in range(T) if u != t)]
        stat[form] = {"k4_live_by_length": res[0][0][form][1:], "copies_live_by_length_max": [max(L_(t, L) for t in range(1, T)) for L in range(1, LMAX + 1)],
                      "k4_shortest": first(0), "copies_shortest": [first(t) for t in range(1, T)],
                      "k4_above_every_copy": above(0), "copy_cells_above_rest": [len(above(t)) for t in range(1, T)]}
    plant_res = []
    for p, (live, ex) in zip(plants, pres):
        hit = [x for x in ex if x["s"] == p["s"] and x["class"] == CLASS_NAME(p["class"]) and x["form"] == p["form"] and x["step"] == p["step"] and x["length"] == p["length"]]
        plant_res.append({"s": p["s"], "e": p["e"], "class": CLASS_NAME(p["class"]), "form": p["form"], "step": p["step"], "length": p["length"],
                          "found": bool(hit), "shortest_found": min((x["length"] for x in hit), default=None),
                          "other_settings_below_24": len(ex) - len(hit)})
    above_k4 = sum(len(v["k4_above_every_copy"]) for v in stat.values())
    null = [sum(v["copy_cells_above_rest"][t] for v in stat.values()) for t in range(N_CONTROLS)]
    bounds = {"family": "nulls at both ends (start run s 0-12; the end run moves nothing), then a periodic or progressive key on the standard/KRYPTOS tables",
              "start_runs": "0-12", "end_runs": "0-12 (any; s + e <= 23)", "classes": [CLASS_NAME(c) for c in CLASSES],
              "forms": {"periodic": "step 0", "per-letter": "w[i mod L] + d i, d 1-25", "per-repeat": "w[i mod L] + d floor(i/L), d 1-25"},
              "lengths": f"1-{LMAX}", "per_form": stat, "k4_settings_below_24": res[0][1][:30],
              "k4_cells_above_every_copy": above_k4, "copy_cells_above_rest": null, "stop_queue": above_k4 > max(null),
              "plants": plant_res, "controls": f"{N_CONTROLS} shuffled copies (seed 2400)", "seconds": round(time.time() - t0), "exhaustive": "yes"}
    notes = (f"Shortest live length K4 / copies: " + "; ".join(f"{f} {stat[f]['k4_shortest']} / {min(x for x in stat[f]['copies_shortest'] if x)}" for f in FORMS)
             + f". K4 above every copy in {above_k4} cells, copies {min(null)}-{max(null)}. Plants: " + ", ".join(f"{p['form']} found {p['found']} (shortest {p['shortest_found']})" for p in plant_res))
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    s = 8
    fv = forced(ctx.K4, sorted(ctx.KNOWN.items()), s, (1, 1, 0))
    lines = ["start run of 8 nulls: the known words sit 8 places later on the copper; KRYPTOS table, added form", "",
             "place  known  carved place  carved  key value"]
    for (q, a), (j, f) in list(zip(sorted(ctx.KNOWN.items()), fv))[:6]:
        lines.append(f"{q:5d}  {a:>5}  {j + 1:12d}  {ctx.K4[j]:>6}  {f:9d}")
    return "\n".join(lines)
