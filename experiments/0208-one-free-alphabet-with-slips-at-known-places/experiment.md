# 0208-one-free-alphabet-with-slips-at-known-places: A1.2, step 2: one alphabet in an unknown order on both sides of the table (Quagmire III), a repeating key of length 1-26, with up to three of the 24 known letters carved wrong, decided exactly, against scrambled copies, with planted slipped messages

**Family:** 1-keyed-periodic  
**Parent:** 0119-one-free-alphabet-exact-at-every-key-length  
**Decision:** reverted  
**Run:** 2026-10-20T12:23:40+00:00, 235.9 s, status ran  
**Time by phase:** design 89 s, implement 15 s, test 254 s, run 236 s, record 0 s

## In plain words

K1 and K2 were made on a table built from one scrambled alphabet. Experiment 119 asked whether any scrambled alphabet at all, with any repeating key word, could turn the carving into the 24 known letters, and found almost none. But if Sanborn made two or three slips at those places, that test would have thrown the right answer away. Here we let two or three of the 24 disagree, every possible choice of which ones, and ask the same question again, on the carving and on scrambled copies of it, with planted messages to show the search can find a slipped one.

## Walkthrough, by hand

1. Choose a key length, say 7, and write the 24 known places with their slot (place mod 7).
2. For each place write: position of the carved letter in the alphabet = position of the known letter + key value of the slot.
3. Cross out two of the 24 places, as if Sanborn had slipped there.
4. Try to place the letters in an alphabet and choose key values so every remaining line holds, backing up when two letters need the same position.
5. If it works, the length fits with those two slips; if every branch backs up, it does not.
6. Repeat for every pair and triple of crossed-out places, every length, both table forms, and on scrambled copies.

## Worked example (generated)

```
key length 7, form V: A(carved) = A(known) + k[slot]

  slips at none: dead
  slips at [66]: dead
  slips at [66, 73]: dead

(66 R and 73 C both sit under carved P in slot 2: no alphabet fits without a slip at one of them, and at length 7 none fits even with one.)
```

## Lineage

Inherits from 0119-one-free-alphabet-exact-at-every-key-length. What changed: A1.2 (Stage 2, step 2, issue #76), second half: one free alphabet. 0119 decided every key length 1-26 exactly with all 24 known letters required (added form dead everywhere, Beaufort alive only at 23 and 26); 0147 (F1.6) allowed one carved letter wrong. Here 2 and 3 of the 24 equations may be dropped as slips: 0119's exact decider, unchanged, on every drop set of 1-3 known places (2,324 per length and form, supersets of a fitting set skipped as not minimal), K4 against 20 scrambled copies, with four planted slipped messages in the same run.

## Hypothesis (domain expert)

A1 (knowledge/12-assumptions.md); C27(c) (Sanborn's own tableau 'slightly different from the one on Kryptos', NYT 2010, 02-sanborn-said.md) and C27(a) (the PALIMPCEST worksheet: a slip in his hand); Sanborn 2005, 'Saying I was sloppy is a good way of saying it'; Scheidt 2015, an encoding error by Jim would not have been known to him (03-scheidt-said.md). Model as 0119: one unknown bijection A from letters to Z26 on plain and cipher sides; key k of length L; form V: A(c_i) = A(p_i) + k[i mod L]; form B: A(c_i) = k[i mod L] - A(p_i). A slip at known place q removes q's equation (the carved letter is not what the key gives). For every set D of 1-3 known places, decide exactly (0119's decide(): mod 13 and mod 2, enumeration or pruned search, witness re-checked) whether an alphabet and key satisfy the other 24 - |D| equations. Count the minimal fitting sets per (L, form) by size; a cell is closed at k when K4 has no fitting set of size k or less. Where K4 fits, the reading is not determined (the alphabet is free), so the judge cannot read it; such a cell can be decided only by F1.5's decider (20-30 min per cell) and is left blocked by cost unless K4's count stands outside the copies'. Cost of naming the slips: 4.7 k + log2 C(24, k) bits (17.5 for k = 2, 25.1 for k = 3).

## Prediction

Short key lengths (about 1-6) stay dead on K4 even with 3 slips; from there up K4 fits at some lengths with 2 or 3 slips, at the same rate as the copies, cell by cell inside the copies' range (K4 above every copy in no more cells than a copy is above the rest). Planted messages at lengths 7 and 12 are found: the planted slips fit, and the plant's count stands above all of its own copies at k = 2; at k = 3 the copies may fit as well (the reach). Zero candidates: a free alphabet leaves the reading undetermined.

## Method

1. For each text, key length L 1-26 and form: the 24 equations (slot, known letter, carved letter).
2. Decide the system with no drop, then every drop set of 1, 2, 3 known places in order of size, skipping supersets of a set already fitting.
3. Count the minimal fitting sets by size; record undecided ones.
4. K4 and 20 copies on every cell; four planted messages and 10 copies of each on their own cell.
5. Compare K4's count with the copies' per cell and per k.

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
 "family": "one unknown alphabet on both sides (Quagmire III), periodic key 1-26, with 0-3 known letters slipped (A1.2)",
 "key_lengths": [
  1,
  26
 ],
 "forms": {
  "V": "A(c) = A(p) + k",
  "B": "A(c) = k - A(p)"
 },
 "drop_sets": "every set of 0-3 of the 24 known places (2,325 per cell), supersets of a fitting set skipped; 0119's decide() unchanged",
 "slip_cost_bits": {
  "1": 9.3,
  "2": 17.5,
  "3": 25.1
 },
 "cells": {
  "V1": {
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ],
   "copies_fitting_at_k_or_less": [
    0,
    0,
    0,
    0
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": []
  },
  "B1": {
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ],
   "copies_fitting_at_k_or_less": [
    0,
    0,
    0,
    0
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": []
  },
  "V2": {
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ],
   "copies_fitting_at_k_or_less": [
    0,
    0,
    0,
    0
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": []
  },
  "B2": {
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ],
   "copies_fitting_at_k_or_less": [
    0,
    0,
    0,
    0
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": []
  },
  "V3": {
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ],
   "copies_fitting_at_k_or_less": [
    0,
    0,
    0,
    0
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": []
  },
  "B3": {
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ],
   "copies_fitting_at_k_or_less": [
    0,
    0,
    0,
    0
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": []
  },
  "V4": {
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    1
   ],
   "copies_fitting_at_k_or_less": [
    0,
    0,
    0,
    1
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": []
  },
  "B4": {
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ],
   "copies_fitting_at_k_or_less": [
    0,
    0,
    0,
    0
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": []
  },
  "V5": {
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    2
   ],
   "copies_fitting_at_k_or_less": [
    0,
    0,
    0,
    3
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": []
  },
  "B5": {
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    8
   ],
   "copies_fitting_at_k_or_less": [
    0,
    0,
    0,
    2
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": []
  },
  "V6": {
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    7,
    33,
    51
   ],
   "copies_fitting_at_k_or_less": [
    0,
    2,
    4,
    11
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": []
  },
  "B6": {
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    8,
    3,
    41
   ],
   "copies_fitting_at_k_or_less": [
    0,
    2,
    2,
    11
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": []
  },
  "V7": {
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    2,
    39,
    44
   ],
   "copies_fitting_at_k_or_less": [
    0,
    1,
    8,
    16
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": []
  },
  "B7": {
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    1,
    26,
    21
   ],
   "copies_fitting_at_k_or_less": [
    1,
    2,
    4,
    10
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": []
  },
  "V8": {
   "k4": [
    0,
    0,
    1,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    4,
    8,
    28
   ],
   "copies_fitting_at_k_or_less": [
    1,
    4,
    10,
    17
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     33,
     74
    ]
   ]
  },
  "B8": {
   "k4": [
    0,
    0,
    0,
    16
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    8,
    32
   ],
   "copies_fitting_at_k_or_less": [
    0,
    0,
    4,
    8
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     23,
     28,
     29
    ],
    [
     23,
     28,
     69
    ],
    [
     23,
     29,
     34
    ],
    [
     23,
     29,
     66
    ],
    [
     23,
     29,
     68
    ],
    [
     23,
     34,
     69
    ],
    [
     23,
     66,
     69
    ],
    [
     23,
     68,
     69
    ],
    [
     28,
     29,
     71
    ],
    [
     28,
     69,
     71
    ],
    [
     29,
     34,
     71
    ],
    [
     29,
     66,
     71
    ],
    [
     29,
     68,
     71
    ],
    [
     34,
     69,
     71
    ],
    [
     66,
     69,
     71
    ],
    [
     68,
     69,
     71
    ]
   ]
  },
  "V9": {
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    4
   ],
   "copies_fitting_at_k_or_less": [
    0,
    0,
    0,
    1
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": []
  },
  "B9": {
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    4
   ],
   "copies_fitting_at_k_or_less": [
    0,
    0,
    0,
    1
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": []
  },
  "V10": {
   "k4": [
    0,
    0,
    0,
    2
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    4,
    15,
    12
   ],
   "copies_fitting_at_k_or_less": [
    3,
    8,
    15,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     22,
     33,
     74
    ],
    [
     33,
     72,
     74
    ]
   ]
  },
  "B10": {
   "k4": [
    0,
    0,
    0,
    8
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    2,
    9,
    10
   ],
   "copies_fitting_at_k_or_less": [
    0,
    6,
    14,
    15
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     22,
     24,
     29
    ],
    [
     22,
     24,
     69
    ],
    [
     22,
     29,
     34
    ],
    [
     22,
     34,
     69
    ],
    [
     24,
     29,
     72
    ],
    [
     24,
     69,
     72
    ],
    [
     29,
     34,
     72
    ],
    [
     34,
     69,
     72
    ]
   ]
  },
  "V11": {
   "k4": [
    0,
    0,
    0,
    10
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    13,
    4,
    8
   ],
   "copies_fitting_at_k_or_less": [
    3,
    11,
    16,
    19
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     22,
     30,
     33
    ],
    [
     22,
     30,
     66
    ],
    [
     22,
     33,
     74
    ],
    [
     22,
     66,
     74
    ],
    [
     28,
     30,
     33
    ],
    [
     28,
     33,
     74
    ],
    [
     30,
     33,
     66
    ],
    [
     30,
     33,
     72
    ],
    [
     33,
     66,
     74
    ],
    [
     33,
     72,
     74
    ]
   ]
  },
  "B11": {
   "k4": [
    0,
    0,
    0,
    16
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    2,
    12,
    24
   ],
   "copies_fitting_at_k_or_less": [
    2,
    4,
    14,
    17
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     22,
     23,
     25
    ],
    [
     22,
     23,
     69
    ],
    [
     22,
     25,
     67
    ],
    [
     22,
     67,
     69
    ],
    [
     23,
     25,
     28
    ],
    [
     23,
     25,
     66
    ],
    [
     23,
     25,
     72
    ],
    [
     23,
     28,
     69
    ],
    [
     23,
     66,
     69
    ],
    [
     23,
     69,
     72
    ],
    [
     25,
     28,
     67
    ],
    [
     25,
     66,
     67
    ],
    [
     25,
     67,
     72
    ],
    [
     28,
     67,
     69
    ],
    [
     66,
     67,
     69
    ],
    [
     67,
     69,
     72
    ]
   ]
  },
  "V12": {
   "k4": [
    0,
    0,
    0,
    16
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    4,
    8,
    16
   ],
   "copies_fitting_at_k_or_less": [
    3,
    11,
    16,
    18
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     26,
     28,
     33
    ],
    [
     26,
     28,
     69
    ],
    [
     26,
     30,
     33
    ],
    [
     26,
     30,
     69
    ],
    [
     26,
     33,
     64
    ],
    [
     26,
     33,
     66
    ],
    [
     26,
     64,
     69
    ],
    [
     26,
     66,
     69
    ],
    [
     28,
     33,
     74
    ],
    [
     28,
     69,
     74
    ],
    [
     30,
     33,
     74
    ],
    [
     30,
     69,
     74
    ],
    [
     33,
     64,
     74
    ],
    [
     33,
     66,
     74
    ],
    [
     64,
     69,
     74
    ],
    [
     66,
     69,
     74
    ]
   ]
  },
  "B12": {
   "k4": [
    0,
    0,
    8,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    4,
    8,
    8
   ],
   "copies_fitting_at_k_or_less": [
    3,
    11,
    17,
    19
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     23,
     28
    ],
    [
     23,
     30
    ],
    [
     23,
     64
    ],
    [
     23,
     66
    ],
    [
     28,
     71
    ],
    [
     30,
     71
    ],
    [
     64,
     71
    ],
    [
     66,
     71
    ]
   ]
  },
  "V13": {
   "k4": [
    0,
    0,
    4,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    4,
    8,
    8
   ],
   "copies_fitting_at_k_or_less": [
    2,
    13,
    19,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     22,
     33
    ],
    [
     22,
     72
    ],
    [
     33,
     74
    ],
    [
     72,
     74
    ]
   ]
  },
  "B13": {
   "k4": [
    0,
    0,
    4,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    10,
    4,
    16
   ],
   "copies_fitting_at_k_or_less": [
    5,
    10,
    15,
    19
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     29,
     30
    ],
    [
     29,
     69
    ],
    [
     30,
     68
    ],
    [
     68,
     69
    ]
   ]
  },
  "V14": {
   "k4": [
    0,
    0,
    4,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    4,
    4,
    16
   ],
   "copies_fitting_at_k_or_less": [
    4,
    14,
    16,
    19
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     25,
     32
    ],
    [
     25,
     74
    ],
    [
     32,
     67
    ],
    [
     67,
     74
    ]
   ]
  },
  "B14": {
   "k4": [
    0,
    0,
    0,
    8
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    4,
    8,
    24
   ],
   "copies_fitting_at_k_or_less": [
    6,
    13,
    17,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     24,
     25,
     32
    ],
    [
     24,
     25,
     74
    ],
    [
     24,
     32,
     67
    ],
    [
     24,
     67,
     74
    ],
    [
     25,
     32,
     66
    ],
    [
     25,
     66,
     74
    ],
    [
     32,
     66,
     67
    ],
    [
     66,
     67,
     74
    ]
   ]
  },
  "V15": {
   "k4": [
    0,
    0,
    0,
    8
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    2,
    4,
    8
   ],
   "copies_fitting_at_k_or_less": [
    1,
    7,
    16,
    19
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     27,
     28,
     29
    ],
    [
     27,
     28,
     74
    ],
    [
     27,
     29,
     73
    ],
    [
     27,
     73,
     74
    ],
    [
     28,
     29,
     72
    ],
    [
     28,
     72,
     74
    ],
    [
     29,
     72,
     73
    ],
    [
     72,
     73,
     74
    ]
   ]
  },
  "B15": {
   "k4": [
    0,
    0,
    4,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    2,
    4,
    8
   ],
   "copies_fitting_at_k_or_less": [
    0,
    7,
    16,
    18
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     27,
     28
    ],
    [
     27,
     73
    ],
    [
     28,
     72
    ],
    [
     72,
     73
    ]
   ]
  },
  "V16": {
   "k4": [
    0,
    0,
    4,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    2,
    4,
    0
   ],
   "copies_fitting_at_k_or_less": [
    7,
    16,
    19,
    19
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     26,
     33
    ],
    [
     26,
     65
    ],
    [
     33,
     74
    ],
    [
     65,
     74
    ]
   ]
  },
  "B16": {
   "k4": [
    0,
    2,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    4,
    4,
    8
   ],
   "copies_fitting_at_k_or_less": [
    8,
    15,
    19,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     23
    ],
    [
     71
    ]
   ]
  },
  "V17": {
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    2,
    4,
    8
   ],
   "copies_fitting_at_k_or_less": [
    0,
    9,
    16,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": []
  },
  "B17": {
   "k4": [
    0,
    0,
    0,
    8
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    2,
    4,
    8
   ],
   "copies_fitting_at_k_or_less": [
    0,
    11,
    17,
    19
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     30,
     31,
     34
    ],
    [
     30,
     31,
     68
    ],
    [
     30,
     34,
     65
    ],
    [
     30,
     65,
     68
    ],
    [
     31,
     34,
     64
    ],
    [
     31,
     64,
     68
    ],
    [
     34,
     64,
     65
    ],
    [
     64,
     65,
     68
    ]
   ]
  },
  "V18": {
   "k4": [
    0,
    0,
    8,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    4,
    4,
    8
   ],
   "copies_fitting_at_k_or_less": [
    8,
    15,
    19,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     28,
     33
    ],
    [
     28,
     69
    ],
    [
     30,
     33
    ],
    [
     30,
     69
    ],
    [
     33,
     64
    ],
    [
     33,
     66
    ],
    [
     64,
     69
    ],
    [
     66,
     69
    ]
   ]
  },
  "B18": {
   "k4": [
    0,
    4,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    4,
    4,
    8
   ],
   "copies_fitting_at_k_or_less": [
    9,
    18,
    19,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     28
    ],
    [
     30
    ],
    [
     64
    ],
    [
     66
    ]
   ]
  },
  "V19": {
   "k4": [
    0,
    2,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    2,
    4,
    24
   ],
   "copies_fitting_at_k_or_less": [
    0,
    10,
    16,
    19
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     33
    ],
    [
     71
    ]
   ]
  },
  "B19": {
   "k4": [
    0,
    2,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    2,
    4,
    24
   ],
   "copies_fitting_at_k_or_less": [
    0,
    5,
    16,
    19
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     26
    ],
    [
     64
    ]
   ]
  },
  "V20": {
   "k4": [
    0,
    0,
    4,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    2,
    16,
    24
   ],
   "copies_fitting_at_k_or_less": [
    6,
    11,
    18,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     33,
     34
    ],
    [
     33,
     74
    ],
    [
     34,
     73
    ],
    [
     73,
     74
    ]
   ]
  },
  "B20": {
   "k4": [
    0,
    2,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    2,
    4,
    8
   ],
   "copies_fitting_at_k_or_less": [
    2,
    11,
    16,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     29
    ],
    [
     69
    ]
   ]
  },
  "V21": {
   "k4": [
    0,
    0,
    4,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    4,
    4,
    16
   ],
   "copies_fitting_at_k_or_less": [
    4,
    14,
    16,
    19
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     25,
     32
    ],
    [
     25,
     74
    ],
    [
     32,
     67
    ],
    [
     67,
     74
    ]
   ]
  },
  "B21": {
   "k4": [
    0,
    0,
    0,
    8
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    4,
    8,
    24
   ],
   "copies_fitting_at_k_or_less": [
    6,
    13,
    17,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     24,
     25,
     32
    ],
    [
     24,
     25,
     74
    ],
    [
     24,
     32,
     67
    ],
    [
     24,
     67,
     74
    ],
    [
     25,
     32,
     66
    ],
    [
     25,
     66,
     74
    ],
    [
     32,
     66,
     67
    ],
    [
     66,
     67,
     74
    ]
   ]
  },
  "V22": {
   "k4": [
    0,
    0,
    8,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    4,
    4,
    8
   ],
   "copies_fitting_at_k_or_less": [
    7,
    16,
    17,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     22,
     30
    ],
    [
     22,
     74
    ],
    [
     28,
     30
    ],
    [
     28,
     74
    ],
    [
     30,
     66
    ],
    [
     30,
     72
    ],
    [
     66,
     74
    ],
    [
     72,
     74
    ]
   ]
  },
  "B22": {
   "k4": [
    0,
    0,
    0,
    16
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    2,
    4,
    8
   ],
   "copies_fitting_at_k_or_less": [
    2,
    11,
    17,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     22,
     23,
     25
    ],
    [
     22,
     23,
     69
    ],
    [
     22,
     25,
     67
    ],
    [
     22,
     67,
     69
    ],
    [
     23,
     25,
     28
    ],
    [
     23,
     25,
     66
    ],
    [
     23,
     25,
     72
    ],
    [
     23,
     28,
     69
    ],
    [
     23,
     66,
     69
    ],
    [
     23,
     69,
     72
    ],
    [
     25,
     28,
     67
    ],
    [
     25,
     66,
     67
    ],
    [
     25,
     67,
     72
    ],
    [
     28,
     67,
     69
    ],
    [
     66,
     67,
     69
    ],
    [
     67,
     69,
     72
    ]
   ]
  },
  "V23": {
   "k4": [
    0,
    2,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    2,
    4,
    16
   ],
   "copies_fitting_at_k_or_less": [
    13,
    18,
    19,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     28
    ],
    [
     74
    ]
   ]
  },
  "B23": {
   "k4": [
    1,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    2,
    4,
    0
   ],
   "copies_fitting_at_k_or_less": [
    11,
    15,
    19,
    19
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    []
   ]
  },
  "V24": {
   "k4": [
    0,
    2,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    2,
    4,
    8
   ],
   "copies_fitting_at_k_or_less": [
    15,
    17,
    19,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     26
    ],
    [
     74
    ]
   ]
  },
  "B24": {
   "k4": [
    0,
    2,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    2,
    4,
    0
   ],
   "copies_fitting_at_k_or_less": [
    12,
    18,
    20,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     23
    ],
    [
     71
    ]
   ]
  },
  "V25": {
   "k4": [
    0,
    0,
    4,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    2,
    0,
    0
   ],
   "copies_fitting_at_k_or_less": [
    16,
    20,
    20,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     22,
     24
    ],
    [
     22,
     74
    ],
    [
     24,
     72
    ],
    [
     72,
     74
    ]
   ]
  },
  "B25": {
   "k4": [
    0,
    2,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    2,
    4,
    0
   ],
   "copies_fitting_at_k_or_less": [
    15,
    19,
    20,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     22
    ],
    [
     72
    ]
   ]
  },
  "V26": {
   "k4": [
    0,
    2,
    0,
    0
   ],
   "copies_min": [
    1,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    0,
    0,
    0
   ],
   "copies_fitting_at_k_or_less": [
    20,
    20,
    20,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     22
    ],
    [
     74
    ]
   ]
  },
  "B26": {
   "k4": [
    1,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    2,
    0,
    0
   ],
   "copies_fitting_at_k_or_less": [
    17,
    20,
    20,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    []
   ]
  }
 },
 "k4_above_every_copy": [
  "B22",
  "V25",
  "V26"
 ],
 "copies_above_the_rest_cells": [
  2,
  2,
  1,
  3,
  1,
  0,
  3,
  0,
  0,
  1,
  1,
  3,
  0,
  2,
  0,
  1,
  0,
  0,
  4,
  3
 ],
 "shortest_fitting_length": {
  "k0": {
   "K4": {
    "V": null,
    "B": 23
   },
   "copies": [
    {
     "V": 18,
     "B": 18
    },
    {
     "V": 11,
     "B": 12
    },
    {
     "V": 23,
     "B": 7
    },
    {
     "V": 22,
     "B": 12
    },
    {
     "V": 10,
     "B": 18
    },
    {
     "V": 11,
     "B": 23
    },
    {
     "V": 16,
     "B": 24
    },
    {
     "V": 26,
     "B": 13
    },
    {
     "V": 22,
     "B": 14
    },
    {
     "V": 23,
     "B": 14
    },
    {
     "V": 22,
     "B": 23
    },
    {
     "V": 12,
     "B": 23
    },
    {
     "V": 18,
     "B": 11
    },
    {
     "V": 24,
     "B": 14
    },
    {
     "V": 8,
     "B": 16
    },
    {
     "V": 18,
     "B": 14
    },
    {
     "V": 16,
     "B": 13
    },
    {
     "V": 23,
     "B": 11
    },
    {
     "V": 11,
     "B": 16
    },
    {
     "V": 10,
     "B": 18
    }
   ]
  },
  "k1": {
   "K4": {
    "V": 19,
    "B": 16
   },
   "copies": [
    {
     "V": 13,
     "B": 13
    },
    {
     "V": 8,
     "B": 10
    },
    {
     "V": 6,
     "B": 6
    },
    {
     "V": 10,
     "B": 10
    },
    {
     "V": 8,
     "B": 10
    },
    {
     "V": 11,
     "B": 11
    },
    {
     "V": 11,
     "B": 12
    },
    {
     "V": 13,
     "B": 13
    },
    {
     "V": 14,
     "B": 12
    },
    {
     "V": 10,
     "B": 12
    },
    {
     "V": 11,
     "B": 17
    },
    {
     "V": 11,
     "B": 15
    },
    {
     "V": 11,
     "B": 11
    },
    {
     "V": 12,
     "B": 13
    },
    {
     "V": 6,
     "B": 12
    },
    {
     "V": 11,
     "B": 11
    },
    {
     "V": 8,
     "B": 10
    },
    {
     "V": 16,
     "B": 6
    },
    {
     "V": 10,
     "B": 16
    },
    {
     "V": 10,
     "B": 14
    }
   ]
  },
  "k2": {
   "K4": {
    "V": 8,
    "B": 12
   },
   "copies": [
    {
     "V": 10,
     "B": 10
    },
    {
     "V": 8,
     "B": 8
    },
    {
     "V": 6,
     "B": 6
    },
    {
     "V": 8,
     "B": 10
    },
    {
     "V": 6,
     "B": 8
    },
    {
     "V": 6,
     "B": 11
    },
    {
     "V": 11,
     "B": 12
    },
    {
     "V": 13,
     "B": 13
    },
    {
     "V": 10,
     "B": 8
    },
    {
     "V": 7,
     "B": 7
    },
    {
     "V": 10,
     "B": 10
    },
    {
     "V": 8,
     "B": 11
    },
    {
     "V": 7,
     "B": 10
    },
    {
     "V": 12,
     "B": 10
    },
    {
     "V": 6,
     "B": 8
    },
    {
     "V": 11,
     "B": 11
    },
    {
     "V": 8,
     "B": 7
    },
    {
     "V": 10,
     "B": 6
    },
    {
     "V": 7,
     "B": 10
    },
    {
     "V": 7,
     "B": 10
    }
   ]
  },
  "k3": {
   "K4": {
    "V": 8,
    "B": 8
   },
   "copies": [
    {
     "V": 7,
     "B": 10
    },
    {
     "V": 5,
     "B": 6
    },
    {
     "V": 5,
     "B": 5
    },
    {
     "V": 4,
     "B": 7
    },
    {
     "V": 6,
     "B": 6
    },
    {
     "V": 6,
     "B": 6
    },
    {
     "V": 7,
     "B": 10
    },
    {
     "V": 7,
     "B": 8
    },
    {
     "V": 8,
     "B": 6
    },
    {
     "V": 7,
     "B": 6
    },
    {
     "V": 6,
     "B": 10
    },
    {
     "V": 8,
     "B": 11
    },
    {
     "V": 6,
     "B": 6
    },
    {
     "V": 8,
     "B": 7
    },
    {
     "V": 6,
     "B": 6
    },
    {
     "V": 6,
     "B": 6
    },
    {
     "V": 6,
     "B": 6
    },
    {
     "V": 6,
     "B": 5
    },
    {
     "V": 7,
     "B": 8
    },
    {
     "V": 5,
     "B": 10
    }
   ]
  }
 },
 "plants": [
  {
   "seed": 2081,
   "key_length": 7,
   "form": "V",
   "k": 2,
   "slips": [
    31,
    72
   ],
   "alphabet": "AWUOIQYFEHGLDRVZKTSPJNXCBM",
   "minimal_fits_by_k": [
    0,
    0,
    67,
    29
   ],
   "planted_slips_fit": true,
   "exact_planted_set_minimal": true,
   "count_at_k": 67,
   "own_copies_count_at_k": [
    0,
    0,
    0,
    6,
    4,
    0,
    0,
    0,
    2,
    0
   ],
   "found": true
  },
  {
   "seed": 2082,
   "key_length": 7,
   "form": "B",
   "k": 3,
   "slips": [
    28,
    66,
    67
   ],
   "alphabet": "VOXYEURASBTPJWNMKDIFQCHZGL",
   "minimal_fits_by_k": [
    0,
    0,
    0,
    61
   ],
   "planted_slips_fit": true,
   "exact_planted_set_minimal": true,
   "count_at_k": 61,
   "own_copies_count_at_k": [
    4,
    0,
    4,
    0,
    0,
    8,
    0,
    0,
    0,
    4
   ],
   "found": true
  },
  {
   "seed": 2083,
   "key_length": 12,
   "form": "V",
   "k": 2,
   "slips": [
    31,
    74
   ],
   "alphabet": "ZROWDQCLUBPINMGKAHFXTYESJV",
   "minimal_fits_by_k": [
    1,
    0,
    0,
    0
   ],
   "planted_slips_fit": true,
   "exact_planted_set_minimal": false,
   "count_at_k": 1,
   "own_copies_count_at_k": [
    0,
    2,
    1,
    6,
    1,
    2,
    0,
    0,
    2,
    4
   ],
   "found": false
  },
  {
   "seed": 2084,
   "key_length": 12,
   "form": "B",
   "k": 3,
   "slips": [
    22,
    28,
    67
   ],
   "alphabet": "AQOPHJTMYCWGUZKSBDFXRIVENL",
   "minimal_fits_by_k": [
    0,
    2,
    0,
    0
   ],
   "planted_slips_fit": true,
   "exact_planted_set_minimal": false,
   "count_at_k": 2,
   "own_copies_count_at_k": [
    4,
    1,
    1,
    6,
    8,
    1,
    8,
    8,
    24,
    4
   ],
   "found": false
  }
 ],
 "judge": "not called: where a free alphabet fits, the alphabet is undetermined and so is the reading; such a cell needs F1.5's decider (20-30 min per cell)",
 "texts_done": "1092 of 1092 cells",
 "controls": "20 shuffled copies (seeds 2080-2099); each plant against 10 shuffles of its own ciphertext",
 "exhaustive": "yes (exact per drop set; undecided sets counted)"
}
```

Notes: K4 above every copy in 3 cells ['B22', 'V25', 'V26']; copies above the rest 0-4; plants found [True, True, False, False]


