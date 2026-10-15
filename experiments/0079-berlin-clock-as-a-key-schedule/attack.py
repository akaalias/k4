"""Experiment 0079. See program.md for the contract."""

EXPERIMENT = {
    "slug": "berlin-clock-as-a-key-schedule",
    "title": "The Berlin clocks as the key: lamp counts of the set-theory clock and the hours on the World Clock, minute by minute",
    "family": "1-keyed-periodic",
    "parent": "0011-progressive-key-period-sweep",
    "changed": "Sanborn told solvers to 'delve into that particular clock' (the Mengenlehreuhr, 2014) and later said the Berlin Clock is the World Clock (2025). Here the clocks themselves drive the key: as the time advances by a fixed step per letter, the key is the number of lit lamps, the hour, the minute, their sum, or the digits of the time, from every starting minute of the day. Every schedule is fully fixed by its start, so the 24 known letters test it exactly.",
    "hypothesis_expert": (
        "Family 1, a key schedule from the clocks (C12(b); 02-sanborn-said.md 2014 'delve into that "
        "particular clock... a lot of fodder there', 2025 'the Berlin Clock in K4 is the World Clock'). "
        "Mengenlehreuhr state at minute t of the day: a = hour div 5 and b = hour mod 5 (rows of four), c = "
        "minute div 5 (row of eleven) and d = minute mod 5 (row of four). Schedules: total lit lamps a+b+c+d "
        "(0-23), the hour, the minute, hour plus minute, the clock's five-minute row c, and the digit stream "
        "of the time HHMM read minute after minute. The time advances by s minutes per letter, s in "
        "{1, 2, 3, 5, 10, 15, 30}, from every start minute 0-1439. Weltzeituhr readings: the 24 facets "
        "read in turn give a period-24 key and a 24-letter ring is excluded by 0052, so only the minute-driven "
        "schedules are new; a step of 60 minutes gives period 24, dead by the crib sweep. Key value v added to "
        "(Vigenere), subtracted from (variant) or used Beaufort-style, with any constant offset, plain and "
        "cipher alphabets standard or KRYPTOS. A schedule survives only if all 24 residuals agree (23 checks); "
        "the closest fit is reported as mismatches against the most common residual, with ten shuffled coppers."
    ),
    "hypothesis_eli5": (
        "Berlin has a famous set-theory clock that tells the time with rows of lamps, and the World Clock "
        "where the crowds met when the Wall fell. Sanborn told people to 'delve into that particular clock'. "
        "Perhaps the key is the clock itself: start it at some minute, move it on a fixed amount for each "
        "letter, and use the number of lit lamps, or the hour, or the minutes, as the shift for that letter. "
        "Each such key is completely fixed by its starting time, so the 24 known letters test every one of "
        "them exactly."
    ),
    "prediction": (
        "No schedule, step, start and setup makes all 24 known letters agree; the closest fit leaves about as "
        "many mismatches as on the ten shuffled coppers. Zero candidates pass."
    ),
    "method": (
        "1. For each schedule, step and start minute, compute the key value under each known place. 2. For "
        "each setup, subtract (or add) it from the total key the known letter needs; the residuals must all be "
        "the same constant. 3. Record survivors and the fewest mismatches. 4. Repeat on ten shuffled coppers."
    ),
    "walkthrough": (
        "1. Start the set-theory clock at midnight and move it one minute per letter, so place 22 shows "
        "00:21 and place 23 shows 00:22. 2. At 00:21 the lamps lit are none for the hours, four five-minute "
        "lamps and one minute lamp: 5. At 00:22: 4 + 2 = 6. 3. On the sculpture's alphabet with Vigenere, place "
        "22 needs total key F (12) minus E (11) = 1, so the constant is 1 - 5 = -4, which is 22. 4. Place 23 needs "
        "L (17) minus A (7) = 10, so the constant is 10 - 6 = 4. 5. 22 and 4 disagree: dead. 6. Repeat for every "
        "start minute, step, schedule and table."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
ALPH = {"std": STD, "kry": KRY}
STEPS = (1, 2, 3, 5, 10, 15, 30)


def lamps(t):
    h, m = divmod(t % 1440, 60)
    return h // 5, h % 5, m // 5, m % 5, h, m


def schedule(name, t0, step, n):
    if name == "time digits":
        digs = []
        t = t0
        while len(digs) < n:
            h, m = divmod(t % 1440, 60)
            digs += [h // 10, h % 10, m // 10, m % 10]
            t += step
        return digs[:n]
    out = []
    for i in range(n):
        a, b, c, d, h, m = lamps(t0 + i * step)
        out.append({"lit lamps": a + b + c + d, "hour": h, "minute": m, "hour plus minute": h + m, "five-minute row": c}[name] % 26)
    return out


NAMES = ("lit lamps", "hour", "minute", "hour plus minute", "five-minute row", "time digits")


def sweep(ct, known):
    items = sorted(known.items())
    idx = [pos - 1 for pos, _ in items]
    setups = []
    for pa in ALPH:
        for ca in ALPH:
            PI = {c: i for i, c in enumerate(ALPH[pa])}; CI = {c: i for i, c in enumerate(ALPH[ca])}
            for mode in ("vig", "var", "beau"):
                T = []
                for pos, p in items:
                    ci, pi = CI[ct[pos - 1]], PI[p]
                    T.append({"vig": (ci - pi) % 26, "var": (pi - ci) % 26, "beau": (ci + pi) % 26}[mode])
                setups.append((f"{pa}/{ca}/{mode}", T))
    best, survivors, trials = 0, [], 0
    for name in NAMES:
        for step in STEPS:
            for t0 in range(1440):
                sch = schedule(name, t0, step, N)
                v = [sch[i] for i in idx]
                for label, T in setups:
                    trials += 1
                    counts = {}
                    for t, k in zip(T, v):
                        r = (t - k) % 26
                        counts[r] = counts.get(r, 0) + 1
                    top = max(counts.values())
                    if top > best:
                        best = top
                    if top == 24:
                        survivors.append({"schedule": name, "step": step, "start": f"{t0 // 60:02d}:{t0 % 60:02d}", "setup": label})
    return best, survivors, trials


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    best, surv, trials = sweep(ct, known)
    rng = random.Random(79)
    cbest = []
    for _ in range(10):
        sh = list(ct); rng.shuffle(sh)
        b2, s2, _ = sweep("".join(sh), known)
        cbest.append(b2)
        if ctx.time_left() < 30:
            break
    return {
        "candidates": [],
        "bounds": {"family": "Berlin clock key schedules", "schedules": list(NAMES), "steps_minutes": list(STEPS), "starts": 1440,
                   "setups": 12, "trials": trials, "k4_best_agreeing": best, "k4_fewest_mismatches": 24 - best, "survivors": surv[:10],
                   "controls_fewest_mismatches": [24 - b for b in cbest]},
        "notes": f"{trials:,} trials. K4: at most {best} of 24 residuals agree (fewest mismatches {24 - best}); survivors {len(surv)}. "
                 f"Ten shuffled coppers: fewest mismatches {[24 - b for b in cbest]}.",
    }


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    I = {c: i for i, c in enumerate(KRY)}
    ct, kn = ctx.K4, ctx.KNOWN
    sch = schedule("lit lamps", 0, 1, N)
    lines = ["set-theory clock from 00:00, one minute per letter, lit lamps as the key; sculpture's alphabet, Vigenere", "",
             "place  time   lamps  needed  constant"]
    for pos in (22, 23, 24, 25):
        need = (I[ct[pos - 1]] - I[kn[pos]]) % 26
        lines.append(f"{pos:>5}  00:{pos - 1:02d}  {sch[pos - 1]:>5}  {need:>6}  {(need - sch[pos - 1]) % 26:>8}")
    return "\n".join(lines)
