# 0130-one-free-alphabet-before-every-move-exact: A table built on one alphabet in an unknown order, then every move of the type-1 library, key lengths 1-26, decided exactly

**Family:** 6-transposition-then-tableau  
**Parent:** 0129-one-free-alphabet-after-every-move-exact  
**Decision:** reverted  
**Run:** 2026-10-16T10:20:06+00:00, 1021.8 s, status ran  
**Time by phase:** design 4 s, test 4 s, run 1022 s, record 0 s

## In plain words

Sanborn said he wrote the message into a grid and read it out another way (a 'matrix'), then used the big lettered table. Earlier tests fixed the table's alphabet to the plain A-Z or the KRYPTOS one. Here the table's scrambled alphabet may be any of the possible orders, and for each of about 28,000 ways of moving the letters, each key length up to 26 and two ways of reading the table, arithmetic on the 24 known letters decides whether any alphabet and key could work at all. We do the same on scrambled copies of the carved text to see how often that happens by chance.

## Walkthrough, by hand

1. Pick a move, say a clockwise quarter turn of a grid 7 wide, and write where each of the 24 known letters lands in the carved text.
2. Pick a key length, say 9, and the order 'table first': each known letter's slot is its own place in the message mod 9.
3. Write one line per known letter: place-in-alphabet of the carved letter there = place of the known letter + key value of the slot (all unknown).
4. If two known letters in one slot sit under the same carved letter but differ, or the same known letter under two carved letters, stop: dead.
5. Otherwise solve the 24 lines mod 13 and mod 2; if two different letters are always forced onto the same place, dead.
6. Else look for one alphabet and key that satisfy every line; if found, check it, and the setting fits.
7. Repeat for every move, key lengths 1-26, the Beaufort form (carved place = key minus known place), and on scrambled copies.

## Worked example (generated)

```
the table, key length 9, then move: turn cw 7 (write in rows of 7, read the columns bottom to top)

place  known  lands at  carved  slot (message place mod 9)
   22      E        11       U     3
   23      A        25       V     4
   24      S        39       Q     5
   25      T        53       K     6
   26      N        67       V     7
   27      O        81       T     8
   28      R        94       K     0
   29      T        10       H     1
   30      H        24       R     2
   31      E        38       T     3
   32      A        52       J     4
   33      S        66       P     5
   34      T        80       X     6
   64      B         5       U     0
   65      E        19       B     1
   66      R        33       S     2
   67      L        47       Z     3
   68      I        61       N     4
   69      N        75       W     5
   70      C        88       U     6
   71      L         4       R     7
   72      O        18       F     8
   73      C        32       K     0
   74      K        46       K     1
form V: a slot sends one known letter to two carved letters (or two to one): dead
form B: a slot sends one known letter to two carved letters (or two to one): dead
```

## Lineage

Inherits from 0129-one-free-alphabet-after-every-move-exact. What changed: F6.1 (one free alphabet after or before each move), order B (the table, then the move), the half 0129 left because both orders do not fit one 30-minute budget. 0097 tested this only with a relaxation that can refute but not confirm, at key lengths 3, 7 and 21, and only in the added (Vigenere-like) form; that made it weak. Here 0119's exact decider (mod 13 and mod 2, exhaustive where the solution space is small, a depth-first search with a node limit elsewhere, every fit re-checked) runs on every one of the 27,852 moves, key lengths 1-26, both table forms (added and Beaufort). Controls: 12 scrambled coppers on a fixed sample of 800 moves, with K4 counted on the same sample.

## Hypothesis (domain expert)

C1(a) (Sanborn, CNN 2005, knowledge/sources/cnn-2005-sanborn-interview-transcript.txt: 'I used a matrix code, and then we can possibly use this code to decipher with... double matrixes and triple matrixes... and then went back to this table to do the ultimate'), C27(c) (his table 'slightly different from the one on Kryptos'), C2(a). Model: plaintext p moved by a permutation pi of the type-1 library (K3's rule a + b i mod 97 at all 9,312 settings, one quarter turn cw/ccw at widths 2-96, two cw turns at every width pair, plain columnar both ways, keyed columnar from the vocabulary and theme words, each forward and inverse: 27,852 distinct maps, as 0097), and one unknown bijection A on both sides of a periodic table with key k of length L. Order B only (table, then move): A(c_pi(i)) = s A(p_i) + k[i mod L], slot = message place i; order A was 0129. Form V: s = +1 (Quagmire III with free order; variant Beaufort is V with k negated); form B: s = -1 (Beaufort). The 24 known letters give 24 equations over Z26; exact decision as 0119 (refute when two letters coincide mod 13 and mod 2, or three mod 13; enumerate the mod-13 space up to scaling at rank <= 5; else 300 random points as a witness hunt, then depth-first search with pruning, 200,000 nodes, 'undecided' reported). A per-slot filter (each slot one-to-one) runs first; it is implied by the model, so it loses nothing. Zekios (2026, research note combined_methods_and_sevens.md) did any-alphabet keys only to period 12 and only for double rotations.

## Prediction

K4 has fitting settings at key lengths of about 7 and up in both forms, at the rate of the scrambled coppers: in no more cells (form, length) is K4 above all 12 coppers than the most any single copper manages against the rest. Key lengths 1-5 have no fit (a dry run on 1,000 moves found the first fits at 6). If K4 beats that null count, the queue stops for a replication (cells where K4 fits and no copper does are listed, and count in it). Zero candidates; fits that remain are at the coppers' rate and only an English climb could judge them, which 0120 found powerless, so they are blocked, not open.

## Method

1. Build the 27,852 moves of the type-1 library.
2. For each move, key length 1-26 and form, write the 24 equations (slot, known letter, carved letter at the place the move sends it).
3. Drop settings that fail the per-slot test; decide the rest exactly (dead, fit with a re-checked witness, or undecided at the node limit).
4. The same on 12 scrambled coppers over a fixed random sample of 800 moves.
5. Per cell (form, length): K4's fits on the sample against the coppers'; count cells where K4 is above every copper and compare with the same count for each copper against the rest.
6. Validate on planted texts (random move, form, length, alphabet and key must decide 'fit').

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
 "family": "one unknown alphabet on both sides (Quagmire III / Beaufort with a free order), periodic key 1-26, before a type-1 move (order B)",
 "moves": 27852,
 "k4_moves_done": 27852,
 "cells": "order B (table, then move) x 2 forms x key lengths 1-26",
 "exhaustive": "exact decision per setting (0119's decider; undecided counted where the node limit was hit)",
 "summary": {
  "BV": {
   "k4_fits_full_library_by_L": [
    0,
    0,
    0,
    0,
    0,
    23,
    231,
    782,
    0,
    2831,
    4063,
    4493,
    6347,
    5963,
    339,
    9867,
    392,
    11607,
    370,
    6233,
    5963,
    8578,
    11473,
    15070,
    19074,
    24221
   ],
   "k4_per_slot_survivors_by_L": [
    0,
    0,
    0,
    4,
    16,
    6802,
    8806,
    9347,
    0,
    14074,
    16051,
    17251,
    19007,
    18782,
    716,
    21012,
    726,
    21408,
    728,
    18727,
    18782,
    20062,
    21510,
    23311,
    25025,
    26857
   ],
   "k4_undecided_by_L": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    2,
    0,
    0,
    0,
    1,
    1,
    1,
    1,
    22,
    0,
    8,
    0,
    3,
    1,
    5,
    1,
    2,
    0,
    0
   ],
   "k4_fits_sample_by_L": [
    0,
    0,
    0,
    0,
    0,
    1,
    3,
    23,
    0,
    85,
    110,
    121,
    176,
    158,
    10,
    279,
    8,
    316,
    7,
    182,
    158,
    266,
    324,
    435,
    547,
    693
   ],
   "coppers_fits_sample_min_by_L": [
    0,
    0,
    0,
    0,
    0,
    0,
    2,
    13,
    0,
    63,
    100,
    109,
    145,
    154,
    3,
    239,
    8,
    322,
    5,
    156,
    154,
    230,
    301,
    379,
    490,
    671
   ],
   "coppers_fits_sample_max_by_L": [
    0,
    0,
    0,
    0,
    0,
    2,
    12,
    31,
    0,
    101,
    134,
    150,
    206,
    189,
    17,
    299,
    21,
    358,
    19,
    208,
    189,
    272,
    345,
    457,
    577,
    708
   ],
   "smallest_L_with_k4_fit": 6
  },
  "BB": {
   "k4_fits_full_library_by_L": [
    0,
    0,
    0,
    0,
    0,
    8,
    89,
    221,
    0,
    1389,
    3125,
    3899,
    6521,
    5967,
    311,
    8950,
    389,
    12218,
    340,
    5840,
    5967,
    8652,
    11247,
    13905,
    18717,
    24109
   ],
   "k4_per_slot_survivors_by_L": [
    0,
    0,
    0,
    4,
    16,
    6802,
    8806,
    9347,
    0,
    14074,
    16051,
    17251,
    19007,
    18782,
    716,
    21012,
    726,
    21408,
    728,
    18727,
    18782,
    20062,
    21510,
    23311,
    25025,
    26857
   ],
   "k4_undecided_by_L": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    4,
    3,
    0,
    15,
    0,
    4,
    0,
    1,
    3,
    3,
    1,
    2,
    0,
    0
   ],
   "k4_fits_sample_by_L": [
    0,
    0,
    0,
    0,
    0,
    0,
    1,
    7,
    0,
    40,
    92,
    112,
    189,
    157,
    7,
    243,
    6,
    338,
    7,
    158,
    157,
    241,
    318,
    400,
    544,
    686
   ],
   "coppers_fits_sample_min_by_L": [
    0,
    0,
    0,
    0,
    0,
    0,
    1,
    2,
    0,
    27,
    78,
    100,
    160,
    151,
    7,
    239,
    8,
    289,
    3,
    157,
    151,
    222,
    312,
    407,
    529,
    685
   ],
   "coppers_fits_sample_max_by_L": [
    0,
    0,
    0,
    0,
    0,
    2,
    6,
    14,
    0,
    51,
    111,
    138,
    203,
    212,
    18,
    304,
    23,
    365,
    22,
    198,
    212,
    282,
    378,
    466,
    584,
    706
   ],
   "smallest_L_with_k4_fit": 6
  }
 },
 "k4_fits_at_L_le_8": [
  {
   "route": "K3 rule a=22 b=1 inverse",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=37 b=1",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=41 b=1",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=46 b=1 inverse",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=13 b=2",
   "order": "B",
   "form": "B",
   "L": 7
  },
  {
   "route": "K3 rule a=15 b=2",
   "order": "B",
   "form": "V",
   "L": 7
  },
  {
   "route": "K3 rule a=27 b=2",
   "order": "B",
   "form": "V",
   "L": 6
  },
  {
   "route": "K3 rule a=27 b=2",
   "order": "B",
   "form": "V",
   "L": 7
  },
  {
   "route": "K3 rule a=27 b=2",
   "order": "B",
   "form": "B",
   "L": 7
  },
  {
   "route": "K3 rule a=29 b=2",
   "order": "B",
   "form": "V",
   "L": 7
  },
  {
   "route": "K3 rule a=31 b=2",
   "order": "B",
   "form": "V",
   "L": 7
  },
  {
   "route": "K3 rule a=38 b=2",
   "order": "B",
   "form": "B",
   "L": 8
  },
  {
   "route": "K3 rule a=38 b=2 inverse",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=85 b=2",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=3 b=3",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=6 b=3",
   "order": "B",
   "form": "B",
   "L": 8
  },
  {
   "route": "K3 rule a=9 b=3 inverse",
   "order": "B",
   "form": "B",
   "L": 7
  },
  {
   "route": "K3 rule a=9 b=3 inverse",
   "order": "B",
   "form": "B",
   "L": 8
  },
  {
   "route": "K3 rule a=25 b=3",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=28 b=3",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=42 b=3",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=49 b=3 inverse",
   "order": "B",
   "form": "V",
   "L": 7
  },
  {
   "route": "K3 rule a=49 b=3 inverse",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=50 b=3",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=51 b=3 inverse",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=56 b=3",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=59 b=3",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=73 b=3",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=87 b=3 inverse",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=89 b=3 inverse",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=2 b=4 inverse",
   "order": "B",
   "form": "B",
   "L": 6
  },
  {
   "route": "K3 rule a=9 b=4",
   "order": "B",
   "form": "V",
   "L": 7
  },
  {
   "route": "K3 rule a=11 b=4 inverse",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=13 b=4",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=37 b=4",
   "order": "B",
   "form": "B",
   "L": 7
  },
  {
   "route": "K3 rule a=38 b=4 inverse",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=60 b=4 inverse",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=61 b=4",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=62 b=4",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=8 b=5",
   "order": "B",
   "form": "V",
   "L": 7
  },
  {
   "route": "K3 rule a=25 b=5 inverse",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=50 b=5 inverse",
   "order": "B",
   "form": "B",
   "L": 8
  },
  {
   "route": "K3 rule a=54 b=5",
   "order": "B",
   "form": "B",
   "L": 8
  },
  {
   "route": "K3 rule a=83 b=5 inverse",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=93 b=5",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=32 b=6",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=32 b=6",
   "order": "B",
   "form": "B",
   "L": 8
  },
  {
   "route": "K3 rule a=32 b=6 inverse",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=38 b=6",
   "order": "B",
   "form": "B",
   "L": 8
  },
  {
   "route": "K3 rule a=43 b=6",
   "order": "B",
   "form": "B",
   "L": 7
  },
  {
   "route": "K3 rule a=63 b=6 inverse",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=67 b=6",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=71 b=6 inverse",
   "order": "B",
   "form": "B",
   "L": 8
  },
  {
   "route": "K3 rule a=74 b=6",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=74 b=6 inverse",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=75 b=6 inverse",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=76 b=6 inverse",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=85 b=6 inverse",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=18 b=7",
   "order": "B",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=39 b=7",
   "order": "B",
   "form": "V",
   "L": 8
  }
 ],
 "n_k4_fits_at_L_le_8": 1354,
 "controls": "12 shuffled coppers (seed 129) on 800 sampled moves; K4 on the same sample",
 "cells_k4_above_every_copper": [],
 "null_cells_above_rest_per_copper": [
  2,
  1,
  1,
  3,
  2,
  4,
  0,
  9,
  10,
  1,
  5,
  0
 ],
 "cells_k4_fits_no_copper_does": [],
 "undecided_sample_k4_and_coppers": [
  1,
  0,
  4,
  0,
  1,
  0,
  1,
  1,
  6,
  0,
  2,
  1,
  0
 ],
 "stop_queue": false,
 "plants": "6 planted texts (random move, order B, form, length 3-21) all decided 'fit'"
}
```

Notes: K4 on 27,852 of 27,852 moves; smallest key length with a fit {'BV': 6, 'BB': 6}; fits at L<=8: 1354. Sample of 800 moves: K4 above every copper in 0 of 52 cells, coppers against the rest 0-10; cells where only K4 fits: []. Stop queue: False.


