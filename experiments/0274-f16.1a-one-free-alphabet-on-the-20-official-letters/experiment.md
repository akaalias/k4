# 0274-f16.1a-one-free-alphabet-on-the-20-official-letters: F16.1a: one alphabet in an unknown order on both sides of the table, a repeating key of length 1-26, decided exactly on the 20 official known letters (EAST at 22-25 set aside), with up to two slips; K4 against 200 shuffles, with planted messages

**Family:** 16-simple-hand-methods  
**Parent:** 0208-one-free-alphabet-with-slips-at-known-places  
**Decision:** reverted  
**Run:** 2026-11-17T14:22:47+00:00, 474.5 s, status ran  
**Time by phase:** design 172 s, test 37 s, run 474 s, record 0 s

## In plain words

Every exact test so far needed all 24 known letters, including EAST, which Sanborn confirmed only in a private email that others passed on. If EAST were wrong, those tests could have thrown the answer away. Here we repeat the test for the K1/K2 kind of cipher, with the alphabet in any order and any repeating key, using only the 20 letters Sanborn published himself, and allowing up to two of them to be carved wrong. We do the same on 200 scrambled copies of the carving, to see whether the carving fits more often than chance.

## Walkthrough, by hand

1. Write K4 and mark only the 20 places of NORTHEAST, BERLIN and CLOCK; leave 22-25 unmarked.
2. Choose a key length, say 11, and give each marked place its slot: place minus 1, mod 11.
3. For each marked place write one line: the carved letter's place in the secret alphabet equals the key value of its slot minus the known letter's place (the Beaufort form).
4. Try to give every letter a different place in the alphabet and every slot a key value so all 20 lines hold, backing up when two letters would need the same place.
5. If an assignment holds every line, length 11 fits; if every branch backs up, it does not.
6. Cross out one or two lines as slips and try again.
7. Do the same on scrambled copies of K4 and compare how often each fits.

## Worked example (generated)

```
Beaufort form: A(carved) = k[slot] - A(known), on the 20 official letters

  length  7: 20 letters dead   24 letters dead
  length 11: 20 letters fit    24 letters dead
  length 23: 20 letters fit    24 letters fit

(With EAST set aside, fewer lines must hold, so more lengths fit; the shuffles say whether K4 fits more than chance.)
```

## Lineage

Inherits from 0208-one-free-alphabet-with-slips-at-known-places. What changed: F16.1 (issue #123), first part: 0119's and 0208's exact decider, imported unchanged from 0208's attack.py, run on the 20 letters Sanborn released himself (NORTHEAST 26-34, BERLIN 64-69, CLOCK 70-74). EAST (22-25) is second-hand (#124) and every exact test so far required it. Drop sets of 0-2 of the 20 places; K4 against 200 shuffles (0208: 20); the same decider on K4's 24 letters in the same run, to list the cells only EAST closed.

## Hypothesis (domain expert)

F1 (one keyed stage, no move), C27(c) and C27(a) as in 0208; criteria revised 2026-11-17 (#124): EAST was confirmed privately in 2020 and reported second-hand, the other 20 letters are Sanborn's own published clues (01-facts.md, 'The four clues'). Model as 0119: one unknown bijection A from letters to Z26 used on the plain and the cipher side (Quagmire III, the K1/K2 system with the alphabet free); key k of length L 1-26; form V: A(c_i) = A(p_i) + k[i mod L]; form B: A(c_i) = k[i mod L] - A(p_i). The constraint: the 20 equations at 26-34 and 64-74, with any 0, 1 or 2 of them dropped as slips (A1), decided exactly by 0119's decide() (CRT mod 13 x mod 2, enumeration or pruned search, witness re-checked). 20 letters give about 94 bits of checks against a key of L x 4.7 bits plus an alphabet of 88 bits, so fits are expected to begin near L = 1-2 shorter than with 24 letters; the question is whether K4 fits more, or shorter, than its shuffles.

## Prediction

K4 fits at more cells than with 24 letters (with 24, at no slip only B23 and B26), but its counts sit inside the 200 shuffles on all five pre-registered statistics (p above 0.01 each): the shortest fitting length per form at no slip, and the number of fitting cells at 0, at most 1 and at most 2 slips. Plants at lengths 7 and 11-12 are found (their planted slips fit and their count beats their own 20 copies); the long plant at 20 is not (the reach). Zero candidates: a free alphabet leaves the reading undetermined.

## Method

1. For each text, key length L 1-26 and form V or B: the 20 equations (slot, known letter, carved letter) at 26-34 and 64-74.
2. Decide with no drop, then every drop set of 1 and 2 places, skipping supersets of a set that already fits.
3. Count minimal fitting sets by size.
4. K4 and 200 shuffles; K4 also on all 24 letters, to list cells only EAST closed.
5. Six planted messages (free alphabet, known key, 0-2 slips at official places), each against 20 shuffles of its own ciphertext.
6. Five pre-registered statistics, one-sided empirical p against the shuffles, Bonferroni at 0.05/5 = 0.01.

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
 "family": "one unknown alphabet on both sides (Quagmire III), periodic key 1-26, forms V and B, on the 20 official known letters (26-34, 64-74), 0-2 slips (F16.1a)",
 "known_places": [
  26,
  27,
  28,
  29,
  30,
  31,
  32,
  33,
  34,
  64,
  65,
  66,
  67,
  68,
  69,
  70,
  71,
  72,
  73,
  74
 ],
 "key_lengths": [
  1,
  26
 ],
 "slips": [
  0,
  2
 ],
 "drop_sets": "every set of 0-2 of the 20 places (211 per cell), supersets of a fitting set skipped; 0119's decide() via 0208's attack.py unchanged",
 "slip_cost_bits": {
  "1": 9.0,
  "2": 17.0
 },
 "preregistered": {
  "shortest_V_k0": {
   "k4": 25,
   "copies_min": 4,
   "copies_median": 13,
   "copies_max": 25,
   "copies_as_extreme": 200,
   "p": 1.0,
   "flag": false
  },
  "shortest_B_k0": {
   "k4": 11,
   "copies_min": 6,
   "copies_median": 11,
   "copies_max": 25,
   "copies_as_extreme": 108,
   "p": 0.5423,
   "flag": false
  },
  "cells_fit_k0": {
   "k4": 9,
   "copies_min": 6,
   "copies_median": 15,
   "copies_max": 27,
   "copies_as_extreme": 189,
   "p": 0.9453,
   "flag": false
  },
  "cells_fit_k1": {
   "k4": 23,
   "copies_min": 16,
   "copies_median": 30,
   "copies_max": 41,
   "copies_as_extreme": 180,
   "p": 0.9005,
   "flag": false
  },
  "cells_fit_k2": {
   "k4": 34,
   "copies_min": 28,
   "copies_median": 39,
   "copies_max": 46,
   "copies_as_extreme": 180,
   "p": 0.9005,
   "flag": false
  }
 },
 "flagged": [],
 "cells": {
  "V1": {
   "k4_20": [
    0,
    0,
    0
   ],
   "k4_24": [
    0,
    0,
    0
   ],
   "k4_20_sets": [],
   "copies_fitting_at_k_or_less": [
    0,
    0,
    0
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "B1": {
   "k4_20": [
    0,
    0,
    0
   ],
   "k4_24": [
    0,
    0,
    0
   ],
   "k4_20_sets": [],
   "copies_fitting_at_k_or_less": [
    0,
    0,
    0
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "V2": {
   "k4_20": [
    0,
    0,
    0
   ],
   "k4_24": [
    0,
    0,
    0
   ],
   "k4_20_sets": [],
   "copies_fitting_at_k_or_less": [
    0,
    0,
    2
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "B2": {
   "k4_20": [
    0,
    0,
    0
   ],
   "k4_24": [
    0,
    0,
    0
   ],
   "k4_20_sets": [],
   "copies_fitting_at_k_or_less": [
    0,
    0,
    0
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "V3": {
   "k4_20": [
    0,
    0,
    0
   ],
   "k4_24": [
    0,
    0,
    0
   ],
   "k4_20_sets": [],
   "copies_fitting_at_k_or_less": [
    0,
    1,
    7
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "B3": {
   "k4_20": [
    0,
    0,
    0
   ],
   "k4_24": [
    0,
    0,
    0
   ],
   "k4_20_sets": [],
   "copies_fitting_at_k_or_less": [
    0,
    0,
    0
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "V4": {
   "k4_20": [
    0,
    0,
    0
   ],
   "k4_24": [
    0,
    0,
    0
   ],
   "k4_20_sets": [],
   "copies_fitting_at_k_or_less": [
    1,
    7,
    48
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "B4": {
   "k4_20": [
    0,
    0,
    0
   ],
   "k4_24": [
    0,
    0,
    0
   ],
   "k4_20_sets": [],
   "copies_fitting_at_k_or_less": [
    0,
    1,
    9
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "V5": {
   "k4_20": [
    0,
    0,
    0
   ],
   "k4_24": [
    0,
    0,
    0
   ],
   "k4_20_sets": [],
   "copies_fitting_at_k_or_less": [
    0,
    1,
    40
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "B5": {
   "k4_20": [
    0,
    0,
    0
   ],
   "k4_24": [
    0,
    0,
    0
   ],
   "k4_20_sets": [],
   "copies_fitting_at_k_or_less": [
    0,
    0,
    15
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "V6": {
   "k4_20": [
    0,
    0,
    0
   ],
   "k4_24": [
    0,
    0,
    0
   ],
   "k4_20_sets": [],
   "copies_fitting_at_k_or_less": [
    15,
    74,
    145
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "B6": {
   "k4_20": [
    0,
    0,
    8
   ],
   "k4_24": [
    0,
    0,
    0
   ],
   "k4_20_sets": [
    [
     28,
     32
    ],
    [
     28,
     74
    ],
    [
     30,
     32
    ],
    [
     30,
     74
    ],
    [
     32,
     64
    ],
    [
     32,
     66
    ],
    [
     64,
     74
    ],
    [
     66,
     74
    ]
   ],
   "copies_fitting_at_k_or_less": [
    6,
    32,
    92
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "V7": {
   "k4_20": [
    0,
    0,
    0
   ],
   "k4_24": [
    0,
    0,
    0
   ],
   "k4_20_sets": [],
   "copies_fitting_at_k_or_less": [
    27,
    98,
    161
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "B7": {
   "k4_20": [
    0,
    0,
    0
   ],
   "k4_24": [
    0,
    0,
    0
   ],
   "k4_20_sets": [],
   "copies_fitting_at_k_or_less": [
    9,
    40,
    124
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "V8": {
   "k4_20": [
    0,
    0,
    1
   ],
   "k4_24": [
    0,
    0,
    1
   ],
   "k4_20_sets": [
    [
     33,
     74
    ]
   ],
   "copies_fitting_at_k_or_less": [
    37,
    97,
    161
   ],
   "undecided_k4": 0,
   "undecided_copies": 8
  },
  "B8": {
   "k4_20": [
    0,
    0,
    8
   ],
   "k4_24": [
    0,
    0,
    0
   ],
   "k4_20_sets": [
    [
     28,
     29
    ],
    [
     28,
     69
    ],
    [
     29,
     34
    ],
    [
     29,
     66
    ],
    [
     29,
     68
    ],
    [
     34,
     69
    ],
    [
     66,
     69
    ],
    [
     68,
     69
    ]
   ],
   "copies_fitting_at_k_or_less": [
    19,
    83,
    157
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "V9": {
   "k4_20": [
    0,
    0,
    0
   ],
   "k4_24": [
    0,
    0,
    0
   ],
   "k4_20_sets": [],
   "copies_fitting_at_k_or_less": [
    2,
    55,
    140
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "B9": {
   "k4_20": [
    0,
    0,
    2
   ],
   "k4_24": [
    0,
    0,
    0
   ],
   "k4_20_sets": [
    [
     27,
     28
    ],
    [
     28,
     72
    ]
   ],
   "copies_fitting_at_k_or_less": [
    1,
    41,
    118
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "V10": {
   "k4_20": [
    0,
    0,
    2
   ],
   "k4_24": [
    0,
    0,
    0
   ],
   "k4_20_sets": [
    [
     33,
     74
    ],
    [
     73,
     74
    ]
   ],
   "copies_fitting_at_k_or_less": [
    55,
    130,
    182
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "B10": {
   "k4_20": [
    0,
    2,
    0
   ],
   "k4_24": [
    0,
    0,
    0
   ],
   "k4_20_sets": [
    [
     29
    ],
    [
     69
    ]
   ],
   "copies_fitting_at_k_or_less": [
    51,
    129,
    175
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "V11": {
   "k4_20": [
    0,
    0,
    4
   ],
   "k4_24": [
    0,
    0,
    0
   ],
   "k4_20_sets": [
    [
     30,
     33
    ],
    [
     30,
     66
    ],
    [
     33,
     74
    ],
    [
     66,
     74
    ]
   ],
   "copies_fitting_at_k_or_less": [
    60,
    134,
    184
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "B11": {
   "k4_20": [
    1,
    0,
    0
   ],
   "k4_24": [
    0,
    0,
    0
   ],
   "k4_20_sets": [
    []
   ],
   "copies_fitting_at_k_or_less": [
    54,
    141,
    190
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "V12": {
   "k4_20": [
    0,
    0,
    0
   ],
   "k4_24": [
    0,
    0,
    0
   ],
   "k4_20_sets": [],
   "copies_fitting_at_k_or_less": [
    70,
    157,
    193
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "B12": {
   "k4_20": [
    0,
    4,
    0
   ],
   "k4_24": [
    0,
    0,
    8
   ],
   "k4_20_sets": [
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
   ],
   "copies_fitting_at_k_or_less": [
    72,
    144,
    185
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "V13": {
   "k4_20": [
    0,
    2,
    0
   ],
   "k4_24": [
    0,
    0,
    4
   ],
   "k4_20_sets": [
    [
     33
    ],
    [
     72
    ]
   ],
   "copies_fitting_at_k_or_less": [
    56,
    142,
    187
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "B13": {
   "k4_20": [
    0,
    0,
    4
   ],
   "k4_24": [
    0,
    0,
    4
   ],
   "k4_20_sets": [
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
   ],
   "copies_fitting_at_k_or_less": [
    69,
    148,
    190
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "V14": {
   "k4_20": [
    0,
    2,
    0
   ],
   "k4_24": [
    0,
    0,
    4
   ],
   "k4_20_sets": [
    [
     32
    ],
    [
     74
    ]
   ],
   "copies_fitting_at_k_or_less": [
    89,
    163,
    191
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "B14": {
   "k4_20": [
    0,
    2,
    0
   ],
   "k4_24": [
    0,
    0,
    0
   ],
   "k4_20_sets": [
    [
     32
    ],
    [
     74
    ]
   ],
   "copies_fitting_at_k_or_less": [
    86,
    167,
    197
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "V15": {
   "k4_20": [
    0,
    0,
    0
   ],
   "k4_24": [
    0,
    0,
    0
   ],
   "k4_20_sets": [],
   "copies_fitting_at_k_or_less": [
    3,
    113,
    192
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "B15": {
   "k4_20": [
    0,
    0,
    4
   ],
   "k4_24": [
    0,
    0,
    4
   ],
   "k4_20_sets": [
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
   ],
   "copies_fitting_at_k_or_less": [
    4,
    124,
    187
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "V16": {
   "k4_20": [
    0,
    0,
    4
   ],
   "k4_24": [
    0,
    0,
    4
   ],
   "k4_20_sets": [
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
   ],
   "copies_fitting_at_k_or_less": [
    125,
    182,
    197
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "B16": {
   "k4_20": [
    1,
    0,
    0
   ],
   "k4_24": [
    0,
    2,
    0
   ],
   "k4_20_sets": [
    []
   ],
   "copies_fitting_at_k_or_less": [
    120,
    183,
    198
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "V17": {
   "k4_20": [
    0,
    0,
    0
   ],
   "k4_24": [
    0,
    0,
    0
   ],
   "k4_20_sets": [],
   "copies_fitting_at_k_or_less": [
    7,
    130,
    193
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "B17": {
   "k4_20": [
    0,
    0,
    0
   ],
   "k4_24": [
    0,
    0,
    0
   ],
   "k4_20_sets": [],
   "copies_fitting_at_k_or_less": [
    5,
    123,
    185
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "V18": {
   "k4_20": [
    0,
    0,
    8
   ],
   "k4_24": [
    0,
    0,
    8
   ],
   "k4_20_sets": [
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
   ],
   "copies_fitting_at_k_or_less": [
    84,
    170,
    196
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "B18": {
   "k4_20": [
    0,
    4,
    0
   ],
   "k4_24": [
    0,
    4,
    0
   ],
   "k4_20_sets": [
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
   ],
   "copies_fitting_at_k_or_less": [
    83,
    155,
    189
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "V19": {
   "k4_20": [
    0,
    2,
    0
   ],
   "k4_24": [
    0,
    2,
    0
   ],
   "k4_20_sets": [
    [
     33
    ],
    [
     71
    ]
   ],
   "copies_fitting_at_k_or_less": [
    5,
    83,
    159
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "B19": {
   "k4_20": [
    0,
    2,
    0
   ],
   "k4_24": [
    0,
    2,
    0
   ],
   "k4_20_sets": [
    [
     26
    ],
    [
     64
    ]
   ],
   "copies_fitting_at_k_or_less": [
    6,
    75,
    167
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "V20": {
   "k4_20": [
    0,
    0,
    4
   ],
   "k4_24": [
    0,
    0,
    4
   ],
   "k4_20_sets": [
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
   ],
   "copies_fitting_at_k_or_less": [
    61,
    138,
    188
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "B20": {
   "k4_20": [
    0,
    2,
    0
   ],
   "k4_24": [
    0,
    2,
    0
   ],
   "k4_20_sets": [
    [
     29
    ],
    [
     69
    ]
   ],
   "copies_fitting_at_k_or_less": [
    73,
    151,
    186
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "V21": {
   "k4_20": [
    0,
    2,
    0
   ],
   "k4_24": [
    0,
    0,
    4
   ],
   "k4_20_sets": [
    [
     32
    ],
    [
     74
    ]
   ],
   "copies_fitting_at_k_or_less": [
    89,
    163,
    191
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "B21": {
   "k4_20": [
    0,
    2,
    0
   ],
   "k4_24": [
    0,
    0,
    0
   ],
   "k4_20_sets": [
    [
     32
    ],
    [
     74
    ]
   ],
   "copies_fitting_at_k_or_less": [
    86,
    167,
    197
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "V22": {
   "k4_20": [
    0,
    2,
    0
   ],
   "k4_24": [
    0,
    0,
    8
   ],
   "k4_20_sets": [
    [
     30
    ],
    [
     74
    ]
   ],
   "copies_fitting_at_k_or_less": [
    102,
    174,
    198
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "B22": {
   "k4_20": [
    1,
    0,
    0
   ],
   "k4_24": [
    0,
    0,
    0
   ],
   "k4_20_sets": [
    []
   ],
   "copies_fitting_at_k_or_less": [
    100,
    180,
    197
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "V23": {
   "k4_20": [
    0,
    2,
    0
   ],
   "k4_24": [
    0,
    2,
    0
   ],
   "k4_20_sets": [
    [
     28
    ],
    [
     74
    ]
   ],
   "copies_fitting_at_k_or_less": [
    126,
    192,
    199
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "B23": {
   "k4_20": [
    1,
    0,
    0
   ],
   "k4_24": [
    1,
    0,
    0
   ],
   "k4_20_sets": [
    []
   ],
   "copies_fitting_at_k_or_less": [
    121,
    192,
    200
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "V24": {
   "k4_20": [
    0,
    2,
    0
   ],
   "k4_24": [
    0,
    2,
    0
   ],
   "k4_20_sets": [
    [
     26
    ],
    [
     74
    ]
   ],
   "copies_fitting_at_k_or_less": [
    172,
    200,
    200
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "B24": {
   "k4_20": [
    1,
    0,
    0
   ],
   "k4_24": [
    0,
    2,
    0
   ],
   "k4_20_sets": [
    []
   ],
   "copies_fitting_at_k_or_less": [
    173,
    200,
    200
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "V25": {
   "k4_20": [
    1,
    0,
    0
   ],
   "k4_24": [
    0,
    0,
    4
   ],
   "k4_20_sets": [
    []
   ],
   "copies_fitting_at_k_or_less": [
    200,
    200,
    200
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "B25": {
   "k4_20": [
    1,
    0,
    0
   ],
   "k4_24": [
    0,
    2,
    0
   ],
   "k4_20_sets": [
    []
   ],
   "copies_fitting_at_k_or_less": [
    200,
    200,
    200
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "V26": {
   "k4_20": [
    1,
    0,
    0
   ],
   "k4_24": [
    0,
    2,
    0
   ],
   "k4_20_sets": [
    []
   ],
   "copies_fitting_at_k_or_less": [
    200,
    200,
    200
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  },
  "B26": {
   "k4_20": [
    1,
    0,
    0
   ],
   "k4_24": [
    1,
    0,
    0
   ],
   "k4_20_sets": [
    []
   ],
   "copies_fitting_at_k_or_less": [
    200,
    200,
    200
   ],
   "undecided_k4": 0,
   "undecided_copies": 0
  }
 },
 "only_east_closed": [
  {
   "cell": "B6",
   "k": 2,
   "k4_minimal_sets": [
    [
     28,
     32
    ],
    [
     28,
     74
    ],
    [
     30,
     32
    ],
    [
     30,
     74
    ],
    [
     32,
     64
    ],
    [
     32,
     66
    ],
    [
     64,
     74
    ],
    [
     66,
     74
    ]
   ],
   "copies_fitting_at_k_or_less": 92
  },
  {
   "cell": "B8",
   "k": 2,
   "k4_minimal_sets": [
    [
     28,
     29
    ],
    [
     28,
     69
    ],
    [
     29,
     34
    ],
    [
     29,
     66
    ],
    [
     29,
     68
    ],
    [
     34,
     69
    ],
    [
     66,
     69
    ],
    [
     68,
     69
    ]
   ],
   "copies_fitting_at_k_or_less": 157
  },
  {
   "cell": "B9",
   "k": 2,
   "k4_minimal_sets": [
    [
     27,
     28
    ],
    [
     28,
     72
    ]
   ],
   "copies_fitting_at_k_or_less": 118
  },
  {
   "cell": "V10",
   "k": 2,
   "k4_minimal_sets": [
    [
     33,
     74
    ],
    [
     73,
     74
    ]
   ],
   "copies_fitting_at_k_or_less": 182
  },
  {
   "cell": "B10",
   "k": 1,
   "k4_minimal_sets": [
    [
     29
    ],
    [
     69
    ]
   ],
   "copies_fitting_at_k_or_less": 129
  },
  {
   "cell": "V11",
   "k": 2,
   "k4_minimal_sets": [
    [
     30,
     33
    ],
    [
     30,
     66
    ],
    [
     33,
     74
    ],
    [
     66,
     74
    ]
   ],
   "copies_fitting_at_k_or_less": 184
  },
  {
   "cell": "B11",
   "k": 0,
   "k4_minimal_sets": [
    []
   ],
   "copies_fitting_at_k_or_less": 54
  },
  {
   "cell": "B12",
   "k": 1,
   "k4_minimal_sets": [
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
   ],
   "copies_fitting_at_k_or_less": 144
  },
  {
   "cell": "V13",
   "k": 1,
   "k4_minimal_sets": [
    [
     33
    ],
    [
     72
    ]
   ],
   "copies_fitting_at_k_or_less": 142
  },
  {
   "cell": "V14",
   "k": 1,
   "k4_minimal_sets": [
    [
     32
    ],
    [
     74
    ]
   ],
   "copies_fitting_at_k_or_less": 163
  },
  {
   "cell": "B14",
   "k": 1,
   "k4_minimal_sets": [
    [
     32
    ],
    [
     74
    ]
   ],
   "copies_fitting_at_k_or_less": 167
  },
  {
   "cell": "B16",
   "k": 0,
   "k4_minimal_sets": [
    []
   ],
   "copies_fitting_at_k_or_less": 120
  },
  {
   "cell": "V21",
   "k": 1,
   "k4_minimal_sets": [
    [
     32
    ],
    [
     74
    ]
   ],
   "copies_fitting_at_k_or_less": 163
  },
  {
   "cell": "B21",
   "k": 1,
   "k4_minimal_sets": [
    [
     32
    ],
    [
     74
    ]
   ],
   "copies_fitting_at_k_or_less": 167
  },
  {
   "cell": "V22",
   "k": 1,
   "k4_minimal_sets": [
    [
     30
    ],
    [
     74
    ]
   ],
   "copies_fitting_at_k_or_less": 174
  },
  {
   "cell": "B22",
   "k": 0,
   "k4_minimal_sets": [
    []
   ],
   "copies_fitting_at_k_or_less": 100
  },
  {
   "cell": "B24",
   "k": 0,
   "k4_minimal_sets": [
    []
   ],
   "copies_fitting_at_k_or_less": 173
  },
  {
   "cell": "V25",
   "k": 0,
   "k4_minimal_sets": [
    []
   ],
   "copies_fitting_at_k_or_less": 200
  },
  {
   "cell": "B25",
   "k": 0,
   "k4_minimal_sets": [
    []
   ],
   "copies_fitting_at_k_or_less": 200
  },
  {
   "cell": "V26",
   "k": 0,
   "k4_minimal_sets": [
    []
   ],
   "copies_fitting_at_k_or_less": 200
  }
 ],
 "plants": [
  {
   "seed": 16101,
   "L": 7,
   "form": "V",
   "k": 0,
   "slips": [],
   "planted_slips_fit": true,
   "count_at_k": 1,
   "own_copies_fitting_at_k": 4,
   "own_copies_max": 1,
   "found": false
  },
  {
   "seed": 16102,
   "L": 7,
   "form": "B",
   "k": 1,
   "slips": [
    33
   ],
   "planted_slips_fit": true,
   "count_at_k": 1,
   "own_copies_fitting_at_k": 5,
   "own_copies_max": 2,
   "found": false
  },
  {
   "seed": 16103,
   "L": 11,
   "form": "B",
   "k": 2,
   "slips": [
    71,
    73
   ],
   "planted_slips_fit": true,
   "count_at_k": 1,
   "own_copies_fitting_at_k": 18,
   "own_copies_max": 4,
   "found": false
  },
  {
   "seed": 16104,
   "L": 12,
   "form": "V",
   "k": 2,
   "slips": [
    30,
    70
   ],
   "planted_slips_fit": true,
   "count_at_k": 1,
   "own_copies_fitting_at_k": 20,
   "own_copies_max": 4,
   "found": false
  },
  {
   "seed": 16105,
   "L": 16,
   "form": "V",
   "k": 1,
   "slips": [
    26
   ],
   "planted_slips_fit": true,
   "count_at_k": 1,
   "own_copies_fitting_at_k": 15,
   "own_copies_max": 2,
   "found": false
  },
  {
   "seed": 16106,
   "L": 20,
   "form": "B",
   "k": 0,
   "slips": [],
   "planted_slips_fit": true,
   "count_at_k": 1,
   "own_copies_fitting_at_k": 6,
   "own_copies_max": 1,
   "found": false
  }
 ],
 "undecided_drop_sets_total": 8,
 "controls": "200 shuffles of K4 (seeds 16100-16299); each plant against 20 shuffles of its own ciphertext",
 "exhaustive": "yes: exact per drop set; undecided sets counted",
 "judge": "not called: where a free alphabet fits, the alphabet and so the reading are undetermined",
 "modal_cost_estimate_dollars": 0,
 "aws_cost_estimate_dollars": 0.2
}
```

Notes: pre-registered flags none; K4 {'shortest_V_k0': 25, 'shortest_B_k0': 11, 'cells_fit_k0': 9, 'cells_fit_k1': 23, 'cells_fit_k2': 34}; cells only EAST closed: [('B6', 2), ('B8', 2), ('B9', 2), ('V10', 2), ('B10', 1), ('V11', 2), ('B11', 0), ('B12', 1), ('V13', 1), ('V14', 1), ('B14', 1), ('B16', 0), ('V21', 1), ('B21', 1), ('V22', 1), ('B22', 0), ('B24', 0), ('V25', 0), ('B25', 0), ('V26', 0)]; plants found [False, False, False, False, False, False]; undecided 8


