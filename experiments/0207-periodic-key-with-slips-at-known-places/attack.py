"""Experiment 0207. See program.md for the contract."""

EXPERIMENT = {
    "slug": "periodic-key-with-slips-at-known-places",
    "title": "A1.2, step 1: a repeating key on the sculpture's tables with one, two or three of the 24 known letters carved wrong (a slip), every key length 1-26, exact, judged against scrambled copies, with planted slipped messages",
    "family": "1-keyed-periodic",
    "parent": "0005-quagmire-period-sweep-forced-keys",
    "changed": (
        "A1.2 (Stage 2, step 2, issue #76), first half: the tables. 0005 required all 24 known letters to agree with one "
        "repeating key (no slip). Here k = 1, 2, 3 of the 24 checks may fail, as they would if Sanborn took a wrong row or "
        "column of his chart at k of the known places. Every key length 1-26 on the 8 table classes (plain and cipher "
        "alphabet standard or KRYPTOS, added or Beaufort form; the key alphabet drops out), exact, K4 against 20 scrambled "
        "copies at the same k; every consistent setting's reading goes through the quadgram cut and the blind judge with "
        "the copies' readings in the same call; three planted messages with 2 or 3 slips at known places in the same run."
    ),
    "hypothesis_expert": (
        "A1 (knowledge/12-assumptions.md): every exact verdict assumed no enciphering slip; K1-K3 carry one enciphering "
        "slip (K2's dropped S) and the PALIMPCEST worksheet shows Sanborn working one letter at a time against a written-out "
        "key (C27(a), 01-facts.md). Sanborn 2005: 'Saying I was sloppy is a good way of saying it' (02-sanborn-said.md). "
        "Scheidt 2015: if Jim made an encoding error he would not have known (03-scheidt-said.md). C1(c) and C27(c) for the "
        "table; C17(a)/(b) for a copper not as intended. Model: c_i = C[P(p_i) + k[i mod L]] or C[k[i mod L] - P(p_i)] "
        "with P, C each the standard or KRYPTOS alphabet (8 classes; variant Beaufort is the added form with the key negated; "
        "the key alphabet only relabels key values). A slip at known place q: the carved letter is not the one the key "
        "gives. For key length L each known place forces a key value in its slot (q - 1 mod L); a setting is a choice of "
        "value per slot among the values its known letters force; its number of slips is the number of known letters that "
        "disagree with their slot's chosen value. A slip at a known place alone in its slot fails no check: it garbles one "
        "column of the reading and is A1.0's case (the judge reads through it). Statistic: settings with exactly d = 0-3 "
        "failed checks per length, K4 against each copy; and the blind judge's best score on each text's readings. Cost of "
        "naming the slips: 4.7 k + log2 C(24, k) bits (9.3, 17.5, 25.1 for k = 1, 2, 3). Key lengths 27-29 and 53+ have no "
        "check at all on these tables, so no slip can show there and they are not rerun (F1/2, 0034, 0048, 0053)."
    ),
    "hypothesis_eli5": (
        "K1 and K2 were enciphered with a repeating secret word on a printed table. Sanborn did it by hand and admits he "
        "was sloppy; if he took the wrong row of the table at one or two of the places we know, the old test, which needs "
        "all 24 known letters to agree, would have thrown away the right answer. Here we let one, two or three of them "
        "disagree, for every word length up to 26, and read what comes out. A language model reads the results without "
        "knowing which come from the real carving and which from scrambled copies of it, which is how we tell a real "
        "reading from luck. We also hide three messages of our own, with deliberate slips, and check that the search finds them."
    ),
    "prediction": (
        "On K4 no setting with 3 or fewer slips exists at key lengths 1-23 (at least 7 checks there, so 4 or more must "
        "hold by chance); at 24-26 settings exist on K4 and on every copy in about equal numbers, because 1-5 checks are "
        "all there is. No K4 reading clears the quadgram cut or scores above every copy's best with the judge. The three "
        "planted messages (key lengths 13, 20 and 25, with 2, 3 and 3 slips) are found, each its own text's top reading by "
        "the judge and above all of its own copies. Zero candidates pass gate 4."
    ),
    "method": (
        "1. For each text, key length L 1-26 and class, the forced key value at each known place. 2. Per slot: its "
        "distinct values, each with the number of its known letters that would then be slips. 3. Enumerate every setting "
        "with at most 3 slips (depth first over the slots). 4. Count by number of slips; K4 against 20 copies. 5. Each "
        "setting's reading ('?' where no known letter fixes the slot), quadgram score of the letters outside the known "
        "places. 6. For every text, its best reading and every reading at or above -5.0 go to the judge, K4's, the "
        "copies', the plants' and the plants' copies' in one call. 7. A text's reading counts only above every one of "
        "its own copies' best."
    ),
    "walkthrough": (
        "1. Take the KRYPTOS table, a key word of length 13, and write the 24 known places with their slot (place minus "
        "1, mod 13). "
        "2. At each known place read off the key letter that turns the known letter into the carved one. "
        "3. Places in the same slot should give the same key letter; where two disagree, one of them is a slip. "
        "4. Count the slips the cheapest choice needs in every slot and add them up. "
        "5. With 3 or fewer slips the setting lives: decrypt every letter with the chosen key letters. "
        "6. Do the same on scrambled copies of the carving, and compare how many settings live and how well they read."
    ),
}

import random
from kryptos.alphabets import ALPHABETS, encrypt_letter, decrypt_letter, key_letter_for
from kryptos.plants import english_plant

N = 97
KMAX = 3
LENGTHS = list(range(1, 27))
CLASSES = [(pa, ca, m) for pa in ("std", "kry") for ca in ("std", "kry") for m in ("vig", "beau")]
N_COPIES = 20
N_PLANT_COPIES = 10
CUT = -5.0
STD = ALPHABETS["std"]
PLANTS = [  # (seed, key length, class, number of slips)
    (2071, 13, ("kry", "kry", "vig"), 2),
    (2072, 20, ("std", "kry", "beau"), 3),
    (2073, 25, ("kry", "std", "vig"), 3),
]


def encrypt(plaintext, key):
    """key: pa, ca, m, key (letters on the standard alphabet, one per slot), slips [[place, carved letter], ...]."""
    k, pa, ca, m = key["key"], key["pa"], key["ca"], key["m"]
    out = [encrypt_letter(p, k[i % len(k)], pa, ca, "std", m) for i, p in enumerate(plaintext)]
    for q, ch in key.get("slips", []):
        out[q - 1] = ch
    return "".join(out)


def forced(text, known, L, cls):
    pa, ca, m = cls
    slots = {}
    for q in sorted(known):
        v = STD.index(key_letter_for(known[q], text[q - 1], pa, ca, "std", m))
        slots.setdefault((q - 1) % L, []).append((q, v))
    return slots


def settings(text, known, L, cls, kmax=KMAX):
    """Every choice of one forced value per slot with at most kmax known letters disagreeing.
    Yields (slips, {slot: value}, [slipped places])."""
    slots = forced(text, known, L, cls)
    opts = []
    for s, eqs in sorted(slots.items()):
        vals = sorted({v for _, v in eqs})
        opts.append((s, [(v, [q for q, w in eqs if w != v]) for v in vals]))
    out = []

    def dfs(i, d, key, slipped):
        if i == len(opts):
            out.append((d, dict(key), list(slipped)))
            return
        s, choices = opts[i]
        for v, bad in choices:
            if d + len(bad) <= kmax:
                key[s] = v
                dfs(i + 1, d + len(bad), key, slipped + bad)
        key.pop(s, None)
    dfs(0, 0, {}, [])
    return out


def reading(text, L, cls, key):
    pa, ca, m = cls
    return "".join(decrypt_letter(text[i], STD[key[i % L]], pa, ca, "std", m) if (i % L) in key else "?" for i in range(N))


def quad(r, known, score):
    return score("".join(c for i, c in enumerate(r, start=1) if i not in known and c != "?"))


def search(text, known, score):
    """counts[L][d] summed over classes, and every setting as a record."""
    counts = {L: [0] * (KMAX + 1) for L in LENGTHS}
    recs = []
    for L in LENGTHS:
        for cls in CLASSES:
            for d, key, slipped in settings(text, known, L, cls):
                counts[L][d] += 1
                r = reading(text, L, cls, key)
                recs.append({"L": L, "cls": cls, "d": d, "key": key, "slips": sorted(slipped), "reading": r,
                             "quad": quad(r, known, score), "open_slots": L - len(key)})
    return counts, recs


def shuffled(text, seed):
    l_ = list(text)
    random.Random(seed).shuffle(l_)
    return "".join(l_)


def make_plant(seed, L, cls, k, known):
    pa, ca, m = cls
    rng = random.Random(seed)
    pt = english_plant(seed)
    key = "".join(rng.choice(STD) for _ in range(L))
    ct = list(encrypt(pt, {"pa": pa, "ca": ca, "m": m, "key": key}))
    slots = forced("".join(ct), known, L, cls)
    checked = [s for s, e in slots.items() if len(e) >= 2]
    rng.shuffle(checked)
    places = [rng.choice([q for q, _ in slots[s]]) for s in checked[:k]]
    for q in places:
        ct[q - 1] = rng.choice([c for c in STD if c != ct[q - 1]])
    return pt, "".join(ct), key, sorted(places)


def summarize(counts):
    return {str(L): counts[L] for L in LENGTHS if any(counts[L])}


def run(ctx):
    known, score = ctx.KNOWN, ctx.english_score
    texts = {"K4": ctx.K4}
    for i in range(N_COPIES):
        texts[f"copy{i + 1}"] = shuffled(ctx.K4, 2070 + i)
    plants = []
    for j, (seed, L, cls, k) in enumerate(PLANTS):
        pt, ct, key, places = make_plant(seed, L, cls, k, known)
        plants.append({"name": f"plant{j + 1}", "seed": seed, "L": L, "cls": cls, "k": k, "pt": pt, "ct": ct,
                       "key": key, "slips": places})
        texts[f"plant{j + 1}"] = ct
        for i in range(N_PLANT_COPIES):
            texts[f"plant{j + 1}-copy{i + 1}"] = shuffled(ct, seed * 100 + i)
    res = {name: search(t, known, score) for name, t in texts.items()}

    # to the judge: each text's best reading by quadgrams, and every reading at or above CUT; one call for all
    to_judge = {}
    for name, (_, recs) in res.items():
        if not recs:
            continue
        best = max(recs, key=lambda r: r["quad"])
        for r in recs:
            if r is best or r["quad"] >= CUT:
                r["judged"] = True
                to_judge[r["reading"]] = None
    order = sorted(to_judge)
    verdicts = ctx.judge(order) if order else []
    for t, v in zip(order, verdicts):
        to_judge[t] = v
    none_count = sum(1 for v in verdicts if v["score"] is None)

    def jbest(name):
        recs = res[name][1]
        sc = [to_judge[r["reading"]]["score"] for r in recs if r.get("judged") and to_judge[r["reading"]]["score"] is not None]
        return max(sc) if sc else None

    for name, (_, recs) in res.items():
        for r in recs:
            if r.get("judged"):
                r["judge"] = to_judge[r["reading"]]["score"]
                r["judge_reading"] = to_judge[r["reading"]]["reading"]

    copies_j = [jbest(f"copy{i + 1}") for i in range(N_COPIES)]
    copies_bar = max([s for s in copies_j if s is not None], default=None)
    k4_recs = res["K4"][1]
    k4_j = jbest("K4")

    # plants: the planted setting among its own settings; its reading's judge score above all its own copies
    plant_out = []
    for p in plants:
        recs = res[p["name"]][1]
        hits = [r for r in recs if r["L"] == p["L"] and r["cls"] == tuple(p["cls"]) and all(
            c == "?" or c == p["pt"][i] or (i + 1) in known for i, c in enumerate(r["reading"]))]
        own = [jbest(f"{p['name']}-copy{i + 1}") for i in range(N_PLANT_COPIES)]
        own_bar = max([s for s in own if s is not None], default=None)
        hit = max(hits, key=lambda r: r["quad"]) if hits else None
        hj = hit.get("judge") if hit else None
        found = bool(hit) and hj is not None and (own_bar is None or hj > own_bar)
        plant_out.append({
            "name": p["name"], "seed": p["seed"], "key_length": p["L"], "class": "/".join(p["cls"]), "slips": p["slips"],
            "k": p["k"], "settings_by_slips": summarize(res[p["name"]][0]),
            "own_copies_settings_at_length": [res[f"{p['name']}-copy{i + 1}"][0][p["L"]] for i in range(N_PLANT_COPIES)],
            "planted_setting_found": bool(hit), "planted_slips_named": hit["slips"] if hit else None,
            "planted_quad": round(hit["quad"], 3) if hit else None, "planted_judge": hj,
            "planted_judge_reading": hit.get("judge_reading") if hit else None,
            "own_copies_judge_best": own, "found": found})

    # K4 readings: count only above every copy's best
    k4_above = [r for r in k4_recs if r.get("judge") is not None and copies_bar is not None and r["judge"] > copies_bar]
    k4_counts = res["K4"][0]
    copy_counts = [res[f"copy{i + 1}"][0] for i in range(N_COPIES)]
    by_len = {}
    for L in LENGTHS:
        checks = 24 - len(forced(ctx.K4, known, L, CLASSES[0]))
        row = {"checks": checks, "k4": k4_counts[L], "copies_min": [min(c[L][d] for c in copy_counts) for d in range(KMAX + 1)],
               "copies_max": [max(c[L][d] for c in copy_counts) for d in range(KMAX + 1)]}
        if any(row["k4"]) or any(row["copies_max"]):
            row["k4_rank_by_total"] = sum(1 for c in copy_counts if sum(c[L]) >= sum(k4_counts[L]))
        by_len[str(L)] = row
    shortest = {}
    for name in ["K4"] + [f"copy{i + 1}" for i in range(N_COPIES)]:
        cs = res[name][0]
        shortest[name] = [next((L for L in LENGTHS if cs[L][d]), None) for d in range(KMAX + 1)]

    # candidates: K4's settings, unknown slots filled with A, the slips named in the key
    cands = []
    for r in sorted(k4_recs, key=lambda r: (-(r.get("judge") or -1), -r["quad"]))[:50]:
        L, (pa, ca, m) = r["L"], r["cls"]
        key = "".join(STD[r["key"].get(s, 0)] for s in range(L))
        pt = "".join(decrypt_letter(ctx.K4[i], key[i % L], pa, ca, "std", m) for i in range(N))
        pt = "".join(known.get(i + 1, ch) for i, ch in enumerate(pt))
        slips = [[q, ctx.K4[q - 1]] for q in r["slips"]]
        cands.append({"plaintext": pt, "key": {"pa": pa, "ca": ca, "m": m, "key": key, "slips": slips},
                      "key_bits": 4.7 * L + 4.7 * len(slips) + (0 if not slips else __import__("math").log2(__import__("math").comb(24, len(slips)))),
                      "key_description": f"key length {L}, {pa}/{ca} {m}, slips at {r['slips']}, {r['open_slots']} slots open (filled with A)",
                      "notes": f"quadgram {r['quad']:.3f}; judge {r.get('judge')}"})
    controls = []
    for i in range(N_COPIES):
        recs = res[f"copy{i + 1}"][1]
        best = None
        for r in recs:
            L, (pa, ca, m) = r["L"], r["cls"]
            key = "".join(STD[r["key"].get(s, 0)] for s in range(L))
            t = texts[f"copy{i + 1}"]
            pt = "".join(decrypt_letter(t[j], key[j % L], pa, ca, "std", m) for j in range(N))
            v = score("".join(ch for j, ch in enumerate(pt, start=1) if j not in known))
            best = v if best is None or v > best else best
        controls.append(best if best is not None else -9.0)

    import math
    bits = {k: round(4.7 * k + math.log2(math.comb(24, k)), 1) for k in (1, 2, 3)}
    return {
        "candidates": cands,
        "controls": controls,
        "bounds": {
            "family": "periodic key on the sculpture's tables, k known letters slipped (A1.2 tables)",
            "classes": 8, "key_lengths": "1-26", "slips": "0-3 at the 24 known places (exact enumeration)",
            "not_rerun": "key lengths 27-29 and 53+: no check on these tables, so a slip cannot show (F1/2)",
            "slip_cost_bits": bits,
            "by_length": by_len,
            "shortest_length_by_slips": {"K4": shortest["K4"], "copies": [shortest[f"copy{i + 1}"] for i in range(N_COPIES)]},
            "judge": {"sent": len(order), "none": none_count, "cut": CUT,
                      "rule": "each text's best reading by quadgrams plus every reading at or above the cut; one call"},
            "k4_settings": len(k4_recs), "k4_best_quad": round(max((r["quad"] for r in k4_recs), default=-99), 3),
            "k4_judge_best": k4_j, "copies_judge_best": copies_j, "k4_readings_above_every_copy": len(k4_above),
            "copies_best_quad": [round(max((r["quad"] for r in res[f"copy{i + 1}"][1]), default=-99), 3) for i in range(N_COPIES)],
            "plants": plant_out,
            "decidable": "the remaining checks (24 minus the slots the known letters touch, minus k) decide the key at lengths 1-23 (7-23 checks, 4-20 after 3 slips); at 24-26 only 5, 3, 1 checks exist, so 3 slips leave 2, 0, 0 and the readings alone decide",
            "controls": f"{N_COPIES} shuffled copies (seeds 2070-2089); each plant against {N_PLANT_COPIES} shuffles of its own ciphertext",
            "exhaustive": "yes",
        },
        "notes": (f"K4 settings with <= 3 slips: {len(k4_recs)} (shortest length by slips {shortest['K4']}); judge sent "
                  f"{len(order)}, K4 best {k4_j}, copies best {copies_bar}; plants found {[p['found'] for p in plant_out]}"),
    }


def worked_example(ctx, key):
    L, cls = 13, ("kry", "kry", "vig")
    slots = forced(ctx.K4, ctx.KNOWN, L, cls)
    lines = [f"key length {L}, KRYPTOS table on both sides, added form: key letter forced at each known place, by slot", ""]
    need = 0
    for s, eqs in sorted(slots.items()):
        vals = [v for _, v in eqs]
        best = max(vals.count(v) for v in set(vals))
        need += len(vals) - best
        lines.append(f"  slot {s:>2}: " + ", ".join(f"{q}:{ctx.KNOWN[q]}->{ctx.K4[q - 1]} key {STD[v]}" for q, v in eqs)
                     + f"   slips needed {len(vals) - best}")
    lines.append("")
    lines.append(f"slips needed at length {L}: {need} (more than 3: dead)")
    return "\n".join(lines)
