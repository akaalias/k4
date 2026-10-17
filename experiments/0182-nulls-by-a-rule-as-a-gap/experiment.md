# 0182-nulls-by-a-rule-as-a-gap: F2.2: nulls placed by any rule, which for a repeating or progressive key act only through the number of nulls between the two known runs (0-29): exact

**Family:** 2-masked-then-keyed  
**Parent:** 0057-letter-nulls-outside-the-cribs  
**Decision:** reverted  
**Run:** 2026-10-17T00:28:46+00:00, 4.1 s, status ran  
**Time by phase:** implement 0 s, test 0 s, run 4 s, record 0 s

## In plain words

Perhaps some letters are fillers placed by a rule, say one after every X. However the rule goes, a repeating secret word only notices how many fillers sit between EASTNORTHEAST and BERLINCLOCK, because only the distance between the known letters matters to it. That number is 0 to 29, so we can try them all, and every rule at once.

## Walkthrough, by hand

1. Suppose 3 fillers sit somewhere between EASTNORTHEAST and BERLINCLOCK.
2. In the message, BERLINCLOCK then starts at place 61 instead of 64; EASTNORTHEAST stays at 22.
3. For a secret word of length 7, places 22 and 64 shared a slot before; now 22 and 61 do not, and other pairs do.
4. Check every pair that shares a slot, for every length, rule and number of fillers 0-29.
5. Do the same on scrambled copies.

## Worked example (generated)

```
message places of the known letters with d nulls between the runs

d =  0: EASTNORTHEAST at 22-34, BERLINCLOCK at 64-74
d =  1: EASTNORTHEAST at 22-34, BERLINCLOCK at 63-73
d =  3: EASTNORTHEAST at 22-34, BERLINCLOCK at 61-71
d = 10: EASTNORTHEAST at 22-34, BERLINCLOCK at 54-64
```

## Lineage

Inherits from 0057-letter-nulls-outside-the-cribs. What changed: F2.2. Rather than list rules (a null after every X, after each known word, before each, doubled letters), note what any rule does to a repeating key: the known runs stay whole (the carved runs are contiguous), nulls before the first run shift both runs alike and nulls after the second shift neither, and a repeating key's consistency depends only on the distance between known places. So every rule acts through one number: how many nulls fall between place 35 and place 63, d = 0-29. The same holds for a progressive key (a constant step per letter). All d are tested: periods 1-26, steps 0-25, 12 table rules; K4 against 20 shuffled copies. The named rules are listed with their d.

## Hypothesis (domain expert)

Scheidt: 'I masked the English language' (C2); nulls placed by a rule are a hand masking device (F2). Model: the plaintext with nulls is enciphered with key value k_j = w[j mod L] + s j at its own place j (s = 0 repeating, s = 1-25 progressive), 12 rules; the carved text is that. The known places after the gap move by -d in the message. Consistency needs every slot of w to agree. Statistic: live (d, rule, s, L) cells with L <= 26, K4 against 20 shuffled copies; the smallest live L per d.

## Prediction

Live cells with key length up to 26 at the shuffled copies' rate for every gap; no gap gives K4 a short key the copies lack. Zero candidates.

## Method

1. For d = 0-29: the 24 known letters' message places (the second run moved d to the left).
2. For each text, rule, step s (0-25) and key length L (1-26): forced key values minus s times place; slots agree?
3. Count live cells per d; smallest live L per d at s = 0.
4. K4 against 20 shuffled copies; list the named rules with their d.

## Result

Candidates returned: 0. Passed all gates: 0. Best crib hits among all candidates: 0/24
(no candidates).
Best loss: None (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| - | no candidates | | | | |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "nulls by any rule, through the gap d between the runs; repeating (s = 0) and progressive (s = 1-25) keys of length 1-26, 12 table rules, exact",
 "per_gap": {
  "0": {
   "k4_live": 0,
   "copies_min": 0,
   "copies_max": 52,
   "k4_smallest_repeating": null,
   "copies_smallest_repeating": [
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    26,
    null,
    null,
    null,
    null,
    null,
    null,
    26,
    null,
    null,
    null,
    26,
    null
   ]
  },
  "1": {
   "k4_live": 312,
   "copies_min": 312,
   "copies_max": 320,
   "k4_smallest_repeating": 26,
   "copies_smallest_repeating": [
    26,
    26,
    26,
    26,
    26,
    26,
    26,
    26,
    26,
    26,
    26,
    26,
    26,
    26,
    26,
    26,
    26,
    26,
    26,
    26
   ]
  },
  "2": {
   "k4_live": 324,
   "copies_min": 324,
   "copies_max": 328,
   "k4_smallest_repeating": 26,
   "copies_smallest_repeating": [
    26,
    26,
    26,
    26,
    26,
    26,
    26,
    25,
    26,
    26,
    26,
    26,
    26,
    26,
    25,
    26,
    26,
    26,
    25,
    26
   ]
  },
  "3": {
   "k4_live": 624,
   "copies_min": 624,
   "copies_max": 632,
   "k4_smallest_repeating": 25,
   "copies_smallest_repeating": [
    25,
    25,
    25,
    25,
    25,
    25,
    25,
    25,
    25,
    25,
    25,
    25,
    25,
    25,
    25,
    25,
    25,
    25,
    25,
    25
   ]
  },
  "4": {
   "k4_live": 324,
   "copies_min": 324,
   "copies_max": 428,
   "k4_smallest_repeating": 25,
   "copies_smallest_repeating": [
    25,
    25,
    25,
    25,
    25,
    25,
    25,
    24,
    25,
    25,
    25,
    25,
    25,
    25,
    24,
    25,
    25,
    25,
    24,
    25
   ]
  },
  "5": {
   "k4_live": 324,
   "copies_min": 324,
   "copies_max": 332,
   "k4_smallest_repeating": 24,
   "copies_smallest_repeating": [
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24
   ]
  },
  "6": {
   "k4_live": 12,
   "copies_min": 12,
   "copies_max": 36,
   "k4_smallest_repeating": null,
   "copies_smallest_repeating": [
    null,
    24,
    null,
    24,
    null,
    24,
    null,
    23,
    null,
    24,
    null,
    null,
    null,
    null,
    23,
    null,
    null,
    null,
    23,
    24
   ]
  },
  "7": {
   "k4_live": 12,
   "copies_min": 12,
   "copies_max": 20,
   "k4_smallest_repeating": null,
   "copies_smallest_repeating": [
    null,
    23,
    null,
    23,
    null,
    23,
    null,
    null,
    null,
    23,
    null,
    null,
    null,
    null,
    23,
    null,
    null,
    null,
    null,
    23
   ]
  },
  "8": {
   "k4_live": 0,
   "copies_min": 0,
   "copies_max": 4,
   "k4_smallest_repeating": null,
   "copies_smallest_repeating": [
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null
   ]
  },
  "9": {
   "k4_live": 0,
   "copies_min": 0,
   "copies_max": 4,
   "k4_smallest_repeating": null,
   "copies_smallest_repeating": [
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null
   ]
  },
  "10": {
   "k4_live": 0,
   "copies_min": 0,
   "copies_max": 0,
   "k4_smallest_repeating": null,
   "copies_smallest_repeating": [
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null
   ]
  },
  "11": {
   "k4_live": 0,
   "copies_min": 0,
   "copies_max": 1,
   "k4_smallest_repeating": null,
   "copies_smallest_repeating": [
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null
   ]
  },
  "12": {
   "k4_live": 0,
   "copies_min": 0,
   "copies_max": 0,
   "k4_smallest_repeating": null,
   "copies_smallest_repeating": [
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null
   ]
  },
  "13": {
   "k4_live": 0,
   "copies_min": 0,
   "copies_max": 0,
   "k4_smallest_repeating": null,
   "copies_smallest_repeating": [
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null
   ]
  },
  "14": {
   "k4_live": 0,
   "copies_min": 0,
   "copies_max": 0,
   "k4_smallest_repeating": null,
   "copies_smallest_repeating": [
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null
   ]
  },
  "15": {
   "k4_live": 0,
   "copies_min": 0,
   "copies_max": 0,
   "k4_smallest_repeating": null,
   "copies_smallest_repeating": [
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null
   ]
  },
  "16": {
   "k4_live": 0,
   "copies_min": 0,
   "copies_max": 0,
   "k4_smallest_repeating": null,
   "copies_smallest_repeating": [
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null
   ]
  },
  "17": {
   "k4_live": 0,
   "copies_min": 0,
   "copies_max": 0,
   "k4_smallest_repeating": null,
   "copies_smallest_repeating": [
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null
   ]
  },
  "18": {
   "k4_live": 0,
   "copies_min": 0,
   "copies_max": 0,
   "k4_smallest_repeating": null,
   "copies_smallest_repeating": [
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null
   ]
  },
  "19": {
   "k4_live": 0,
   "copies_min": 0,
   "copies_max": 0,
   "k4_smallest_repeating": null,
   "copies_smallest_repeating": [
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null
   ]
  },
  "20": {
   "k4_live": 0,
   "copies_min": 0,
   "copies_max": 0,
   "k4_smallest_repeating": null,
   "copies_smallest_repeating": [
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null
   ]
  },
  "21": {
   "k4_live": 0,
   "copies_min": 0,
   "copies_max": 0,
   "k4_smallest_repeating": null,
   "copies_smallest_repeating": [
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null
   ]
  },
  "22": {
   "k4_live": 0,
   "copies_min": 0,
   "copies_max": 0,
   "k4_smallest_repeating": null,
   "copies_smallest_repeating": [
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null
   ]
  },
  "23": {
   "k4_live": 0,
   "copies_min": 0,
   "copies_max": 0,
   "k4_smallest_repeating": null,
   "copies_smallest_repeating": [
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null
   ]
  },
  "24": {
   "k4_live": 0,
   "copies_min": 0,
   "copies_max": 0,
   "k4_smallest_repeating": null,
   "copies_smallest_repeating": [
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null
   ]
  },
  "25": {
   "k4_live": 0,
   "copies_min": 0,
   "copies_max": 2,
   "k4_smallest_repeating": null,
   "copies_smallest_repeating": [
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null
   ]
  },
  "26": {
   "k4_live": 0,
   "copies_min": 0,
   "copies_max": 52,
   "k4_smallest_repeating": null,
   "copies_smallest_repeating": [
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    26,
    null,
    null,
    null,
    null,
    null,
    null,
    26,
    null,
    null,
    null,
    26,
    null
   ]
  },
  "27": {
   "k4_live": 324,
   "copies_min": 324,
   "copies_max": 332,
   "k4_smallest_repeating": 26,
   "copies_smallest_repeating": [
    26,
    26,
    26,
    26,
    26,
    26,
    26,
    25,
    26,
    26,
    26,
    26,
    26,
    26,
    25,
    26,
    26,
    26,
    25,
    26
   ]
  },
  "28": {
   "k4_live": 636,
   "copies_min": 636,
   "copies_max": 640,
   "k4_smallest_repeating": 25,
   "copies_smallest_repeating": [
    25,
    25,
    25,
    25,
    25,
    25,
    25,
    24,
    25,
    25,
    25,
    25,
    25,
    25,
    24,
    25,
    25,
    25,
    24,
    25
   ]
  },
  "29": {
   "k4_live": 948,
   "copies_min": 948,
   "copies_max": 956,
   "k4_smallest_repeating": 24,
   "copies_smallest_repeating": [
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    23,
    24,
    24,
    24,
    24,
    24,
    24,
    23,
    24,
    24,
    24,
    23,
    24
   ]
  }
 },
 "gaps_k4_above_every_copy": [],
 "live_total": {
  "k4": 3840,
  "copies": [
   3852,
   3916,
   3858,
   3916,
   3854,
   3912,
   3866,
   3944,
   3852,
   3946,
   3840,
   3864,
   3867,
   3852,
   3934,
   3840,
   3866,
   3852,
   3956,
   3970
  ]
 },
 "named_rules_gap": {
  "a null after each known word (one after EASTNORTHEAST)": 1,
  "two after EASTNORTHEAST, or one after it and one before BERLINCLOCK": 2,
  "a null after every carved X between the runs": 0,
  "every carved X between the runs": 0,
  "a null after every doubled letter between the runs": 2,
  "the second of each doubled letter between the runs": 2,
  "nulls only before the first run or after the second": 0
 },
 "copies": "20 shuffled copies (seed 1820)",
 "exhaustive": true
}
```

Notes: live cells over all gaps: K4 3840 (copies 3840-3970); gaps where K4 is above every copy: []; smallest repeating key on K4 per gap: [None, 26, 26, 25, 25, 24, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 26, 25, 24]


