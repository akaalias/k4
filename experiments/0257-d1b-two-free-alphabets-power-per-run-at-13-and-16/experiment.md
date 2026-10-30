# 0257-d1b-two-free-alphabets-power-per-run-at-13-and-16: D1b: design 2's power per run for two free alphabets (Quagmire IV), 24 clean and 24 Sanborn-style plants at F1.2's sampled lengths 13 and 16, every run's best recorded

**Family:** 1-keyed-periodic  
**Parent:** 0229-d1-one-free-alphabet-power-per-run-with-enough-plants  
**Decision:** reverted  
**Run:** 2026-10-30T03:05:30+00:00, 3913.9 s, status ran  
**Time by phase:** test 10 s, run 3914 s, record 0 s

## In plain words

For the hardest version of the cipher, with two scrambled alphabets, our search tool's success rate was measured on only a handful of hidden test messages, and the counts disagreed between tries. Here we hide 96 test messages, half plain book English and half written Sanborn's way, and count how many the tool finds after one search, two, and so on up to ten. If one search finds about as many as ten, the tool becomes about thirty times cheaper, and two thousand untested settings come within reach.

## Walkthrough, by hand

1. Hide a test message under two shuffled alphabets (one for plain letters, one for cipher letters) and a key of 13 (or 16) numbers.
2. Make six scrambled copies of its ciphertext that keep the carved letters at the 24 known places.
3. Run the tempering search ten times on each of the seven texts, writing down the best score after each run.
4. After run r, is the hidden message's best above all six copies' bests?
5. Over 96 hidden messages, the share found after r runs is the tool's power at that cost.

## Worked example (generated)

```
D1b measures how fast design 2 finds a planted message under two free alphabets. For one plant and its six copies:

  run          1      2      3   ...   10
  plant      best of runs 1..r
  copies     best of runs 1..r, each
  found at r when the plant's best is above every copy's best.

Over 96 plants at key lengths 13 and 16: one run qualifies when it finds within 5 of what ten runs find.
```

## Lineage

Inherits from 0229-d1-one-free-alphabet-power-per-run-with-enough-plants. What changed: D1b (issue #77). 0229 measured design 2's power per run for one free alphabet and D1 qualified a one-run decider (Alexis, 2026-10-28, #100). Here the same measurement for two free alphabets with 0144's compiled tempering, unchanged: F1.2's sampled lengths 13 and 16, 24 clean and 24 Sanborn-style plants each, 6 kept-place copies per plant, ten full runs per text with each run's best recorded. Two lengths so the power can be checked for sameness across the class before one measured power is used for every two-alphabet setting (F1.4's 1,346 two-alphabet settings, F1.2 13).

## Hypothesis (domain expert)

F1.5 design 2 (0143, 0144, 0146) closed F1.2's lengths 8, 13 and 16 on power from 4-5 clean plants each; 0226 and 0228 redrew L13 on Sanborn-style plants (9/12, 8/12) and on clean ones (2/5): two-alphabet power is in doubt and rests on too few plants. Two questions on one set of climbs, as 0229 for one alphabet: (1) design 2's ten-run power at 13 and 16 on clean and Sanborn-style text (judge bench classes xstops, k123, sub3; A6, C17, C19), 24 plants per class and length; (2) the power of the first r runs, r = 1-10. D1's rule (Alexis, #100): a cheaper decider qualifies when its power pooled over the cells (here 96 plants) is within 5 of the reference on the same plants. Sameness: the one-run power at 13 and at 16 within 5 of 48 of each other. Clue entries C27(c) (two alphabets: Sanborn's 'slightly different' tableau on both sides).

## Prediction

Ten-run power at 13 about 0.6 clean and 0.6 Sanborn-style, at 16 a little higher (fewer checks keep less of the copies' freedom out, but longer columns read better). As for one alphabet, power flat in the number of runs: one run within 5 of 96 of ten, so a one-run decider qualifies for two alphabets; 13 and 16 within 5 of 48. Zero candidates.

## Method

1. Per length (13, 16): 24 clean plants (0144's plant4: a Carter window with the known words, two random alphabets, a random key) and 24 Sanborn-style (0226's class texts, two arms: 8 xstops, 8 K1-K3 windows, 8 with three letters changed), each with an exact witness (0123's decider through 0144's witness4, 20 s alarm, redrawn if slow).
2. Six own copies per plant: the carved letters at the 24 known places kept, the other 73 shuffled (0143's copies, fit by construction), started from the plant's witness.
3. Every text climbed by 0144's compiled tempering, unchanged: 10 runs of 16 replicas x 625 rounds x 1000 moves, each run's best recorded.
4. Power at r = 1-10 by length and class: a plant is found at r when the best of its first r runs is strictly above the best of the first r runs of each own copy (null 1/7).

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
 "item": "D1b",
 "decider": "F1.5 design 2 for two free alphabets: 0144's compiled tempering (16 replicas x 625 rounds x 1000 moves per run), unchanged",
 "lengths": [
  "13",
  "16"
 ],
 "plants_per_class": 24,
 "own_copies": 6,
 "null_per_plant": "1/7",
 "copies": "kept-place copies (0143): the carved letters at the 24 known places kept, the other 73 shuffled",
 "runs": 10,
 "power_table": {
  "13/1": {
   "clean": [
    16,
    24
   ],
   "messy": [
    14,
    24
   ]
  },
  "13/2": {
   "clean": [
    16,
    24
   ],
   "messy": [
    15,
    24
   ]
  },
  "13/3": {
   "clean": [
    16,
    24
   ],
   "messy": [
    14,
    24
   ]
  },
  "13/4": {
   "clean": [
    15,
    24
   ],
   "messy": [
    15,
    24
   ]
  },
  "13/5": {
   "clean": [
    16,
    24
   ],
   "messy": [
    15,
    24
   ]
  },
  "13/6": {
   "clean": [
    15,
    24
   ],
   "messy": [
    15,
    24
   ]
  },
  "13/7": {
   "clean": [
    16,
    24
   ],
   "messy": [
    16,
    24
   ]
  },
  "13/8": {
   "clean": [
    15,
    24
   ],
   "messy": [
    16,
    24
   ]
  },
  "13/9": {
   "clean": [
    16,
    24
   ],
   "messy": [
    16,
    24
   ]
  },
  "13/10": {
   "clean": [
    16,
    24
   ],
   "messy": [
    16,
    24
   ]
  },
  "16/1": {
   "clean": [
    17,
    24
   ],
   "messy": [
    16,
    24
   ]
  },
  "16/2": {
   "clean": [
    17,
    24
   ],
   "messy": [
    16,
    24
   ]
  },
  "16/3": {
   "clean": [
    18,
    24
   ],
   "messy": [
    16,
    24
   ]
  },
  "16/4": {
   "clean": [
    19,
    24
   ],
   "messy": [
    17,
    24
   ]
  },
  "16/5": {
   "clean": [
    18,
    24
   ],
   "messy": [
    17,
    24
   ]
  },
  "16/6": {
   "clean": [
    20,
    24
   ],
   "messy": [
    17,
    24
   ]
  },
  "16/7": {
   "clean": [
    21,
    24
   ],
   "messy": [
    19,
    24
   ]
  },
  "16/8": {
   "clean": [
    20,
    24
   ],
   "messy": [
    20,
    24
   ]
  },
  "16/9": {
   "clean": [
    20,
    24
   ],
   "messy": [
    20,
    24
   ]
  },
  "16/10": {
   "clean": [
    19,
    24
   ],
   "messy": [
    20,
    24
   ]
  }
 },
 "pooled_power_by_runs": {
  "1": 63,
  "2": 64,
  "3": 64,
  "4": 66,
  "5": 66,
  "6": 67,
  "7": 72,
  "8": 71,
  "9": 72,
  "10": 71
 },
 "reference_ten_runs_pooled": [
  71,
  96
 ],
 "power_by_class_ten_runs": {
  "13/clean": [
   16,
   24
  ],
  "13/xstops": [
   6,
   8
  ],
  "13/k123": [
   7,
   8
  ],
  "13/sub3": [
   3,
   8
  ],
  "16/clean": [
   19,
   24
  ],
  "16/xstops": [
   7,
   8
  ],
  "16/k123": [
   8,
   8
  ],
  "16/sub3": [
   5,
   8
  ]
 },
 "qualifying_runs_within_5_of_96": [
  4,
  5,
  6,
  7,
  8,
  9,
  10
 ],
 "one_run_pooled": [
  63,
  96
 ],
 "one_run_by_length": {
  "13": 30,
  "16": 33
 },
 "same_power_13_16_within_5": true,
 "d1b_reached_one_run": false,
 "cost_factor_per_setting_one_run": 31.7,
 "seconds_per_text_ten_runs": 180.0,
 "texts": 672,
 "compute_seconds": 3886,
 "exhaustive": false,
 "modal_cost_estimate": "672 texts x about 207 s (0228's L13 time for ten runs) = about 39 core-hours, about $2 of Modal credit"
}
```

Notes: D1b: pooled power by runs {1: 63, 2: 64, 3: 64, 4: 66, 5: 66, 6: 67, 7: 72, 8: 71, 9: 72, 10: 71}; one run 63/96 against ten 71/96; one run at 13 30/48, at 16 33/48; qualifying runs [4, 5, 6, 7, 8, 9, 10]; one-run decider does not qualify


