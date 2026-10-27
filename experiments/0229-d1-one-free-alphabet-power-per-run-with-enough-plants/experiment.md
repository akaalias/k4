# 0229-d1-one-free-alphabet-power-per-run-with-enough-plants: D1: design 2's power per run for one free alphabet, bounded with enough plants: 24 clean and 24 Sanborn-style plants at F1.1's Beaufort lengths 23 and 26, every run's best recorded

**Family:** 1-keyed-periodic  
**Parent:** 0228-d1-design-2s-power-against-its-budget  
**Decision:** reverted  
**Run:** 2026-10-27T15:12:18+00:00, 2440.9 s, status ran  
**Time by phase:** design 75 s, implement 0 s, test 5 s, run 2441 s, record 0 s

## In plain words

Our best tool for the hardest cases seemed to work as well with one long search as with ten, which would make it ten times cheaper; but the hidden-message tests behind that used too few messages to be sure, and a second try found fewer of them than the first. Here we hide 96 test messages, half clean book English and half written the way Sanborn writes, and count how many the tool finds after one search, two, and so on up to ten.

## Walkthrough, by hand

1. Hide a test message under a shuffled alphabet and a key of 23 (or 26) numbers, Beaufort form.
2. Make six scrambled copies of its ciphertext that the same key length still fits.
3. Run the tempering search ten times on each of the seven texts, writing down the best score after each run.
4. After run r, is the hidden message's best above all six copies' bests?
5. Over 96 hidden messages, the share found after r runs is the tool's power at that cost.

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

Inherits from 0228-d1-design-2s-power-against-its-budget. What changed: D1 (issue #77), second measurement. 0228 found that one full tempering run matched ten at L23 (clean 6/8, messy 7/12) but its reference power did not replicate (messy 6/12 against 0226's 10/12): 5-12 plants are too few. Here one free alphabet only (F1.1, Beaufort form), at both sampled lengths 23 and 26, with 24 clean and 24 Sanborn-style plants per length, 6 own copies each, full-length runs, every run's best recorded.

## Hypothesis (domain expert)

F1.5 design 2 (0139-0142) closed F1.1's Beaufort lengths 23 (7 checks) and 26 (1 check) on power 6/8 and 5/6 measured with clean Carter; A6.2 (0226) and D1 (0228) redrew Sanborn-style power at 23 as 10/12 and 6/12, and L23 was reopened. Two questions on one set of climbs: (1) design 2's ten-run power at 23 and 26 on clean and on Sanborn-style text (judge bench classes xstops, k123, sub3; A6, C19, C17), with 24 plants each, enough for a 95% interval of about +-0.18; (2) the power of the first r runs, r = 1-10, against the ten-run power: the cut D1 needs. Sequential copies (stop at the first copy that beats the target) are exact and give x3.17. Pre-registered: D1 is reached for one free alphabet when the cheapest r whose power is at least the ten-run power on both classes at both lengths gives 10 x 3.17 / r >= 10, i.e. r <= 3. The ten-run power is also each cell's power for its verdict: a cell whose pooled Sanborn-style power (with 0226 and 0228 at 23) is under its stated bar (23: 6/8; 26: 5/6) stays or goes open.

## Prediction

Ten-run power at 23: clean about 0.70, Sanborn-style about 0.60; at 26 (one check) a little lower, about 0.6 and 0.5. The first run reaches the ten-run power within one plant at both lengths, so r = 1 or 2 qualifies: D1 reached for one free alphabet (16-32 times cheaper). L23 stays open (pooled Sanborn-style under 6/8); L26 goes open too. Zero candidates.

## Method

1. Per length (23, 26): 24 clean plants (0120's make_plants rule) and 24 Sanborn-style (0226's class texts: L23 arms 0 and 1, L26 arms 2 and 0, so 8 xstops, 8 K1-K3 windows, 8 with three letters changed), each enciphered in the Beaufort form with a random alphabet and key; 6 own copies each, shuffles that 0120's exact decider fits at that length.
2. Every text climbed with 0140's compiled tempering, unchanged: 10 runs of 16 replicas x 625 rounds x 1000 moves, each run's best score and time recorded.
3. Power at r = 1-10 by length and class: a plant is found at r when the best of its first r runs is strictly above the best of the first r runs of each own copy (null 1/7).

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
 "decider": "F1.5 design 2: 0140's compiled tempering, one free alphabet, Beaufort form, unchanged",
 "lengths": [
  "23",
  "26"
 ],
 "plants_per_class": 24,
 "own_copies": 6,
 "null_per_plant": "1/7",
 "runs": 10,
 "rounds": 625,
 "reference_ten_runs": {
  "23": {
   "clean": [
    21,
    24
   ],
   "messy": [
    16,
    24
   ],
   "cost": 1.0
  },
  "26": {
   "clean": [
    13,
    24
   ],
   "messy": [
    17,
    24
   ],
   "cost": 1.0
  }
 },
 "power_table": {
  "23/1": {
   "clean": [
    23,
    24
   ],
   "messy": [
    14,
    24
   ],
   "cost": 0.1
  },
  "23/2": {
   "clean": [
    22,
    24
   ],
   "messy": [
    15,
    24
   ],
   "cost": 0.2
  },
  "23/3": {
   "clean": [
    23,
    24
   ],
   "messy": [
    16,
    24
   ],
   "cost": 0.3
  },
  "23/4": {
   "clean": [
    22,
    24
   ],
   "messy": [
    16,
    24
   ],
   "cost": 0.4
  },
  "23/5": {
   "clean": [
    21,
    24
   ],
   "messy": [
    15,
    24
   ],
   "cost": 0.5
  },
  "23/6": {
   "clean": [
    22,
    24
   ],
   "messy": [
    14,
    24
   ],
   "cost": 0.6
  },
  "23/7": {
   "clean": [
    22,
    24
   ],
   "messy": [
    15,
    24
   ],
   "cost": 0.7
  },
  "23/8": {
   "clean": [
    22,
    24
   ],
   "messy": [
    15,
    24
   ],
   "cost": 0.8
  },
  "23/9": {
   "clean": [
    21,
    24
   ],
   "messy": [
    16,
    24
   ],
   "cost": 0.9
  },
  "23/10": {
   "clean": [
    21,
    24
   ],
   "messy": [
    16,
    24
   ],
   "cost": 1.0
  },
  "26/1": {
   "clean": [
    15,
    24
   ],
   "messy": [
    14,
    24
   ],
   "cost": 0.1
  },
  "26/2": {
   "clean": [
    18,
    24
   ],
   "messy": [
    15,
    24
   ],
   "cost": 0.2
  },
  "26/3": {
   "clean": [
    13,
    24
   ],
   "messy": [
    14,
    24
   ],
   "cost": 0.3
  },
  "26/4": {
   "clean": [
    11,
    24
   ],
   "messy": [
    12,
    24
   ],
   "cost": 0.4
  },
  "26/5": {
   "clean": [
    11,
    24
   ],
   "messy": [
    11,
    24
   ],
   "cost": 0.5
  },
  "26/6": {
   "clean": [
    11,
    24
   ],
   "messy": [
    13,
    24
   ],
   "cost": 0.6
  },
  "26/7": {
   "clean": [
    11,
    24
   ],
   "messy": [
    16,
    24
   ],
   "cost": 0.7
  },
  "26/8": {
   "clean": [
    12,
    24
   ],
   "messy": [
    16,
    24
   ],
   "cost": 0.8
  },
  "26/9": {
   "clean": [
    13,
    24
   ],
   "messy": [
    16,
    24
   ],
   "cost": 0.9
  },
  "26/10": {
   "clean": [
    13,
    24
   ],
   "messy": [
    17,
    24
   ],
   "cost": 1.0
  }
 },
 "power_by_class_ten_runs": {
  "23/clean": [
   21,
   24
  ],
  "23/xstops": [
   5,
   8
  ],
  "23/k123": [
   6,
   8
  ],
  "23/sub3": [
   5,
   8
  ],
  "26/clean": [
   13,
   24
  ],
  "26/xstops": [
   6,
   8
  ],
  "26/k123": [
   6,
   8
  ],
  "26/sub3": [
   5,
   8
  ]
 },
 "qualifying_runs": [
  10
 ],
 "cheapest_qualifying_runs": 10,
 "sequential_copies_factor": 3.17,
 "cost_factor_per_setting": 3.2,
 "d1_reached_one_alphabet": false,
 "pooled_sanborn_style_L23_with_0226_0228": [
  32,
  48
 ],
 "bar_L23": "6/8",
 "bar_L26": "5/6",
 "seconds_per_text_ten_runs": 111.1,
 "texts": 672,
 "compute_seconds": 2374,
 "exhaustive": false,
 "expected_total_time": "672 texts at about 168 s (0228's measured L23 time) = about 113,000 core-seconds, 4 h on 8 cores"
}
```

Notes: ten-run power L23 clean (21, 24), messy (16, 24); L26 clean (13, 24), messy (17, 24); cheapest qualifying runs 10; factor 3.2


