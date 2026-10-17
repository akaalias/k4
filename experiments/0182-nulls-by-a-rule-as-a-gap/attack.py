"""Experiment 0182 (F2.2). See program.md for the contract."""

EXPERIMENT = {
    "slug": "nulls-by-a-rule-as-a-gap",
    "title": "F2.2: nulls placed by any rule, which for a repeating or progressive key act only through the number of nulls between the two known runs (0-29): exact",
    "family": "2-masked-then-keyed",
    "parent": "0057-letter-nulls-outside-the-cribs",
    "changed": (
        "F2.2. Rather than list rules (a null after every X, after each known word, before each, doubled letters), "
        "note what any rule does to a repeating key: the known runs stay whole (the carved runs are contiguous), nulls "
        "before the first run shift both runs alike and nulls after the second shift neither, and a repeating key's "
        "consistency depends only on the distance between known places. So every rule acts through one number: how "
        "many nulls fall between place 35 and place 63, d = 0-29. The same holds for a progressive key (a constant "
        "step per letter). All d are tested: periods 1-26, steps 0-25, 12 table rules; K4 against 20 shuffled copies. "
        "The named rules are listed with their d."
    ),
    "hypothesis_expert": (
        "Scheidt: 'I masked the English language' (C2); nulls placed by a rule are a hand masking device (F2). Model: the "
        "plaintext with nulls is enciphered with key value k_j = w[j mod L] + s j at its own place j (s = 0 repeating, "
        "s = 1-25 progressive), 12 rules; the carved text is that. The known places after the gap move by -d in the "
        "message. Consistency needs every slot of w to agree. Statistic: live (d, rule, s, L) cells with L <= 26, K4 "
        "against 20 shuffled copies; the smallest live L per d."
    ),
    "hypothesis_eli5": (
        "Perhaps some letters are fillers placed by a rule, say one after every X. However the rule goes, a repeating "
        "secret word only notices how many fillers sit between EASTNORTHEAST and BERLINCLOCK, because only the distance "
        "between the known letters matters to it. That number is 0 to 29, so we can try them all, and every rule at "
        "once."
    ),
    "prediction": "Live cells with key length up to 26 at the shuffled copies' rate for every gap; no gap gives K4 a short key the copies lack. Zero candidates.",
    "method": (
        "1. For d = 0-29: the 24 known letters' message places (the second run moved d to the left). "
        "2. For each text, rule, step s (0-25) and key length L (1-26): forced key values minus s times place; slots agree? "
        "3. Count live cells per d; smallest live L per d at s = 0. "
        "4. K4 against 20 shuffled copies; list the named rules with their d."
    ),
    "walkthrough": (
        "1. Suppose 3 fillers sit somewhere between EASTNORTHEAST and BERLINCLOCK. "
        "2. In the message, BERLINCLOCK then starts at place 61 instead of 64; EASTNORTHEAST stays at 22. "
        "3. For a secret word of length 7, places 22 and 64 shared a slot before; now 22 and 61 do not, and other pairs do. "
        "4. Check every pair that shares a slot, for every length, rule and number of fillers 0-29. "
        "5. Do the same on scrambled copies."
    ),
}

import random

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY, KNOWN

N_CONTROLS = 20
ALPH = {"std": STD, "kry": KRY}
PLACES = sorted(KNOWN)
DMAX = 29


def forced(text, rule):
    mode, pa, ca = rule
    P = {c: i for i, c in enumerate(ALPH[pa])}; C = {c: i for i, c in enumerate(ALPH[ca])}
    out = []
    for q in PLACES:
        c, p = C[text[q - 1]], P[KNOWN[q]]
        out.append({"vig": (c - p) % 26, "beau": (c + p) % 26, "var": (p - c) % 26}[mode])
    return out


def scan(text, rules):
    live = {}            # d -> count of live (rule, s, L) cells
    smallest = {}        # d -> smallest live L at s = 0
    for rule in rules:
        K = forced(text, rule)
        for d in range(DMAX + 1):
            pos = [q - 1 if q < 64 else q - 1 - d for q in PLACES]
            for s in range(26):
                v = [(K[e] - s * pos[e]) % 26 for e in range(24)]
                for L in range(1, 27):
                    slot = {}
                    ok = True
                    for e in range(24):
                        if slot.setdefault(pos[e] % L, v[e]) != v[e]:
                            ok = False
                            break
                    if ok:
                        live[d] = live.get(d, 0) + 1
                        if s == 0:
                            smallest[d] = min(smallest.get(d, 99), L)
    return live, smallest


def run(ctx):
    ct = ctx.K4
    rules = [(m, pa, ca) for m in ("vig", "beau", "var") for pa in ALPH for ca in ALPH]
    rng = random.Random(1820)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    res = [scan(t, rules) for t in texts]
    per_d = {}
    for d in range(DMAX + 1):
        cp = [r[0].get(d, 0) for r in res[1:]]
        per_d[d] = {"k4_live": res[0][0].get(d, 0), "copies_min": min(cp), "copies_max": max(cp),
                    "k4_smallest_repeating": res[0][1].get(d), "copies_smallest_repeating": [r[1].get(d) for r in res[1:]]}
    above = [d for d, v in per_d.items() if v["k4_live"] > v["copies_max"]]
    tot = [sum(r[0].values()) for r in res]
    gap = ct[34:63]
    named = {
        "a null after each known word (one after EASTNORTHEAST)": 1,
        "two after EASTNORTHEAST, or one after it and one before BERLINCLOCK": 2,
        "a null after every carved X between the runs": sum(1 for ch in gap[:-1] if ch == "X"),
        "every carved X between the runs": gap.count("X"),
        "a null after every doubled letter between the runs": sum(1 for i in range(len(gap) - 1) if gap[i] == gap[i + 1]),
        "the second of each doubled letter between the runs": sum(1 for i in range(len(gap) - 1) if gap[i] == gap[i + 1]),
        "nulls only before the first run or after the second": 0,
    }
    bounds = {
        "family": "nulls by any rule, through the gap d between the runs; repeating (s = 0) and progressive (s = 1-25) keys of length 1-26, 12 table rules, exact",
        "per_gap": per_d, "gaps_k4_above_every_copy": above,
        "live_total": {"k4": tot[0], "copies": tot[1:]},
        "named_rules_gap": named,
        "copies": f"{N_CONTROLS} shuffled copies (seed 1820)", "exhaustive": True,
    }
    notes = (f"live cells over all gaps: K4 {tot[0]} (copies {min(tot[1:])}-{max(tot[1:])}); gaps where K4 is above every copy: {above}; "
             f"smallest repeating key on K4 per gap: {[per_d[d]['k4_smallest_repeating'] for d in range(DMAX + 1)]}")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    lines = ["message places of the known letters with d nulls between the runs", ""]
    for d in (0, 1, 3, 10):
        pos = [q if q < 64 else q - d for q in PLACES]
        lines.append(f"d = {d:2d}: EASTNORTHEAST at {pos[0]}-{pos[12]}, BERLINCLOCK at {pos[13]}-{pos[23]}")
    return "\n".join(lines)
