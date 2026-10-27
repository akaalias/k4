# 0228-d1-design-2s-power-against-its-budget: D1: design 2's power against its budget: the tempering climb at full length and at a tenth, every number of runs 1-10, on clean and Sanborn-style plants at F1.1 L23 and F1.2 L13, each against its own copies

**Family:** 1-keyed-periodic  
**Parent:** 0226-a6-the-climbs-power-on-sanborn-style-plaintext  
**Decision:** reverted  
**Run:** 2026-10-27T13:16:26+00:00, 6714.3 s, status ran  
**Time by phase:** implement 0 s, test 5 s, run 6714 s, record 0 s

## In plain words

The best tool we have for judging the hardest cases is slow: for each setting it runs ten long searches on K4 and on a dozen scrambled copies. Here we hide test messages, run the tool, and note after every one of the ten searches, and with searches a tenth as long, whether the hidden message was already picked out. If it usually is, the tool can be made much cheaper without missing more, and settings we had to skip for cost can be judged.

## Walkthrough, by hand

1. Hide a test message under a shuffled alphabet and a key of 23 numbers.
2. Make six scrambled copies of its ciphertext that the same key length still fits.
3. Run the tempering search ten times on each of the seven texts, writing down the best score after each run.
4. After run 1, is the hidden message's best above all six copies' bests? After run 2? ... After run 10?
5. Repeat with runs a tenth as long.
6. Over many hidden messages, the share found after r runs is the tool's power at that budget.

## Worked example (generated)

```
D1 measures how fast design 2 finds a planted message. For one plant and its six copies:

  run          1      2      3   ...   10
  plant      best of runs 1..r
  copies     best of runs 1..r, each
  found at r when the plant's best is above every copy's best.

Repeated with runs a tenth as long; power at each budget is the share of plants found.
```

## Lineage

Inherits from 0226-a6-the-climbs-power-on-sanborn-style-plaintext. What changed: D1 (issue #77), first measurement. Design 2 (F1.5) costs 20-30 min per setting: 10 independent tempering runs (16 replicas x 625 rounds x 1000 moves) on K4, 12 copies and a power test. Two cuts are measured here on the same plants: fewer runs (each run's best is recorded, so power at 1-10 runs comes from one pass) and runs a tenth as long (62 rounds, a second pass). Plants: clean Carter (0139's and 0143's rule) and A6.2's Sanborn-style classes (0226), at F1.1's Beaufort L23 (0140's compiled climb) and F1.2's L13 (0144's).

## Hypothesis (domain expert)

F1.5 design 2 (parallel tempering in the set of keys that keep the 24 known letters; 0139-0146) decided F1.1 L23, L26 and F1.2 L8, L13, L16 at measured power; F1.4's free-alphabet residue (about 1,900 settings), F1.7's fitting lags (about 100), F6.1 (about 443,000) and F6.2 3-14 are blocked by its cost. A tempering run either reaches the basin of the planted reading or not; if most plants are found in the first runs, or in short runs, the decider can be cut without losing power. Separately and exactly, copies can be climbed one at a time, stopping at the first that beats the target: the decision 'target above every copy' is unchanged, and under the null the target is exchangeable with its copies, so the expected number climbed is H_12 = 3.1 instead of 12 (no run needed; stated here). Test: per plant, found at budget (rounds, r) when the best of its first r runs is strictly above the best of the first r runs of each of its 6 own copies (null 1/7). Pre-registered: the reference is the full budget (625 rounds, 10 runs) measured in this run; a cheaper budget qualifies when its power is at least the reference's on clean and on Sanborn-style plants at both lengths; D1 is reached when the cheapest qualifying budget times the sequential-copies factor is at least ten times cheaper per setting. Also reported: design 2's power on 12 fresh Sanborn-style plants at L13, beside 0226's 9 of 12 (the reopened F1.2 L13 cell).

## Prediction

Power saturates early: at full length 3 runs reach the reference power at L23 and 5 at L13; runs a tenth as long lose power (about two thirds of the reference at L23, half at L13). With sequential copies, 3 full runs give about 3.3 x 3.1 = 10 times cheaper per setting at L23: D1 reached at L23, not at L13. Design 2 on fresh Sanborn-style plants at L13: 9-11 of 12. Zero candidates.

## Method

1. L23: 8 clean plants (0120's make_plants rule) and 12 Sanborn-style (0226's class texts, arm 0: 4 xstops, 4 K1-K3 windows, 4 with three letters changed), each enciphered in the Beaufort form with a random alphabet and key of 23; 6 own copies each, shuffles that 0120's exact decider fits at 23.
2. L13: 5 clean plants (0144's plant4) and 12 Sanborn-style (arm 1), two random alphabets and a key of 13; witness from 0123's decider under a 20 s alarm (0226's rule); 6 kept-place copies each, the plant's witness as start.
3. Every text climbed twice with 0140's and 0144's compiled tempering, same replicas, moves and temperatures: 10 runs of 625 rounds and 10 runs of 62 rounds, each run's best score recorded with its wall time.
4. Power at every (rounds, r), r = 1-10, by class and length; cost per text from the measured times.

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
 "item": "D1",
 "decider": "F1.5 design 2: 0140's (L23, one alphabet, Beaufort) and 0144's (L13, two alphabets) compiled tempering",
 "plants": {
  "23": {
   "clean": 8,
   "sanborn_style": 12
  },
  "13": {
   "clean": 5,
   "sanborn_style": 12
  }
 },
 "own_copies": 6,
 "null_per_plant": "1/7",
 "rounds": [
  625,
  62
 ],
 "runs": 10,
 "reference": {
  "23": {
   "clean": [
    6,
    8
   ],
   "messy": [
    6,
    12
   ],
   "cost": 1.0
  },
  "13": {
   "clean": [
    2,
    5
   ],
   "messy": [
    8,
    12
   ],
   "cost": 1.0
  }
 },
 "power_table": {
  "23/625/1": {
   "clean": [
    6,
    8
   ],
   "messy": [
    7,
    12
   ],
   "cost": 0.1
  },
  "23/625/2": {
   "clean": [
    7,
    8
   ],
   "messy": [
    8,
    12
   ],
   "cost": 0.2
  },
  "23/625/3": {
   "clean": [
    6,
    8
   ],
   "messy": [
    7,
    12
   ],
   "cost": 0.3
  },
  "23/625/4": {
   "clean": [
    6,
    8
   ],
   "messy": [
    8,
    12
   ],
   "cost": 0.4
  },
  "23/625/5": {
   "clean": [
    6,
    8
   ],
   "messy": [
    7,
    12
   ],
   "cost": 0.5
  },
  "23/625/6": {
   "clean": [
    6,
    8
   ],
   "messy": [
    8,
    12
   ],
   "cost": 0.6
  },
  "23/625/7": {
   "clean": [
    6,
    8
   ],
   "messy": [
    8,
    12
   ],
   "cost": 0.7
  },
  "23/625/8": {
   "clean": [
    6,
    8
   ],
   "messy": [
    7,
    12
   ],
   "cost": 0.8
  },
  "23/625/9": {
   "clean": [
    6,
    8
   ],
   "messy": [
    7,
    12
   ],
   "cost": 0.9
  },
  "23/625/10": {
   "clean": [
    6,
    8
   ],
   "messy": [
    6,
    12
   ],
   "cost": 1.0
  },
  "23/62/1": {
   "clean": [
    4,
    8
   ],
   "messy": [
    6,
    12
   ],
   "cost": 0.0099
  },
  "23/62/2": {
   "clean": [
    5,
    8
   ],
   "messy": [
    6,
    12
   ],
   "cost": 0.0198
  },
  "23/62/3": {
   "clean": [
    4,
    8
   ],
   "messy": [
    8,
    12
   ],
   "cost": 0.0298
  },
  "23/62/4": {
   "clean": [
    4,
    8
   ],
   "messy": [
    7,
    12
   ],
   "cost": 0.0397
  },
  "23/62/5": {
   "clean": [
    4,
    8
   ],
   "messy": [
    8,
    12
   ],
   "cost": 0.0496
  },
  "23/62/6": {
   "clean": [
    5,
    8
   ],
   "messy": [
    8,
    12
   ],
   "cost": 0.0595
  },
  "23/62/7": {
   "clean": [
    5,
    8
   ],
   "messy": [
    9,
    12
   ],
   "cost": 0.0694
  },
  "23/62/8": {
   "clean": [
    5,
    8
   ],
   "messy": [
    10,
    12
   ],
   "cost": 0.0794
  },
  "23/62/9": {
   "clean": [
    5,
    8
   ],
   "messy": [
    8,
    12
   ],
   "cost": 0.0893
  },
  "23/62/10": {
   "clean": [
    5,
    8
   ],
   "messy": [
    8,
    12
   ],
   "cost": 0.0992
  },
  "13/625/1": {
   "clean": [
    0,
    5
   ],
   "messy": [
    8,
    12
   ],
   "cost": 0.1
  },
  "13/625/2": {
   "clean": [
    1,
    5
   ],
   "messy": [
    9,
    12
   ],
   "cost": 0.2
  },
  "13/625/3": {
   "clean": [
    1,
    5
   ],
   "messy": [
    9,
    12
   ],
   "cost": 0.3
  },
  "13/625/4": {
   "clean": [
    1,
    5
   ],
   "messy": [
    9,
    12
   ],
   "cost": 0.4
  },
  "13/625/5": {
   "clean": [
    1,
    5
   ],
   "messy": [
    8,
    12
   ],
   "cost": 0.5
  },
  "13/625/6": {
   "clean": [
    1,
    5
   ],
   "messy": [
    8,
    12
   ],
   "cost": 0.6
  },
  "13/625/7": {
   "clean": [
    1,
    5
   ],
   "messy": [
    8,
    12
   ],
   "cost": 0.7
  },
  "13/625/8": {
   "clean": [
    1,
    5
   ],
   "messy": [
    8,
    12
   ],
   "cost": 0.8
  },
  "13/625/9": {
   "clean": [
    2,
    5
   ],
   "messy": [
    8,
    12
   ],
   "cost": 0.9
  },
  "13/625/10": {
   "clean": [
    2,
    5
   ],
   "messy": [
    8,
    12
   ],
   "cost": 1.0
  },
  "13/62/1": {
   "clean": [
    1,
    5
   ],
   "messy": [
    10,
    12
   ],
   "cost": 0.0099
  },
  "13/62/2": {
   "clean": [
    4,
    5
   ],
   "messy": [
    11,
    12
   ],
   "cost": 0.0198
  },
  "13/62/3": {
   "clean": [
    3,
    5
   ],
   "messy": [
    11,
    12
   ],
   "cost": 0.0298
  },
  "13/62/4": {
   "clean": [
    1,
    5
   ],
   "messy": [
    10,
    12
   ],
   "cost": 0.0397
  },
  "13/62/5": {
   "clean": [
    0,
    5
   ],
   "messy": [
    10,
    12
   ],
   "cost": 0.0496
  },
  "13/62/6": {
   "clean": [
    1,
    5
   ],
   "messy": [
    10,
    12
   ],
   "cost": 0.0595
  },
  "13/62/7": {
   "clean": [
    1,
    5
   ],
   "messy": [
    11,
    12
   ],
   "cost": 0.0694
  },
  "13/62/8": {
   "clean": [
    1,
    5
   ],
   "messy": [
    11,
    12
   ],
   "cost": 0.0794
  },
  "13/62/9": {
   "clean": [
    2,
    5
   ],
   "messy": [
    11,
    12
   ],
   "cost": 0.0893
  },
  "13/62/10": {
   "clean": [
    2,
    5
   ],
   "messy": [
    11,
    12
   ],
   "cost": 0.0992
  }
 },
 "power_by_class_full_budget": {
  "23/clean": [
   6,
   8
  ],
  "23/xstops": [
   2,
   4
  ],
  "23/k123": [
   2,
   4
  ],
  "23/sub3": [
   2,
   4
  ],
  "13/clean": [
   2,
   5
  ],
  "13/xstops": [
   2,
   4
  ],
  "13/k123": [
   3,
   4
  ],
  "13/sub3": [
   3,
   4
  ]
 },
 "qualifying_budgets": [
  [
   625,
   9
  ],
  [
   625,
   10
  ]
 ],
 "cheapest_qualifying": [
  625,
  9
 ],
 "sequential_copies_factor": 3.17,
 "sequential_copies_note": "exact: stop climbing copies at the first that beats the target; same decision; expected copies under the null H_12 = 3.10",
 "cost_factor_per_setting": 3.5,
 "d1_reached": false,
 "seconds_per_text": {
  "13/625": 207.0,
  "13/62": 24.7,
  "23/625": 167.4,
  "23/62": 18.9
 },
 "f12_l13_sanborn_style_full_budget": [
  8,
  12
 ],
 "f12_l13_with_0226": "0226: 9 of 12",
 "texts": 259,
 "climbs": 518,
 "compute_seconds": 6714,
 "exhaustive": false,
 "expected_total_time": "about 47,700 core-seconds (140 texts at about 121 s for L23, 119 at about 259 s for L13, both passes), 100 min on 8 cores"
}
```

Notes: reference power L23 clean (6, 8), messy (6, 12); L13 clean (2, 5), messy (8, 12); cheapest qualifying budget (625, 9); per-setting factor with sequential copies 3.5


