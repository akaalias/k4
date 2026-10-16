# 0133-two-free-alphabets-every-move-exact-to-ten-rerun: Two alphabets in unknown orders (Quagmire IV) after or before every move of the type-1 library: exact at key lengths 1-10 on K4 and ten coppers, the per-slot test at 11-26

**Family:** 6-transposition-then-tableau  
**Parent:** 0132-two-free-alphabets-every-move-exact-to-ten  
**Decision:** reverted  
**Run:** 2026-10-16T11:42:26+00:00, 611.1 s, status ran  
**Time by phase:** design 0 s, test 4 s, run 611 s, record 0 s

## In plain words

The table may use one scrambled alphabet to look up the message letter and a second one to write the carved letter. For every one of about 28,000 ways of moving the letters, before or after the table, and every key length up to 10, arithmetic on the 24 known letters decides whether any such pair of alphabets could work. For longer keys almost everything that passes a quick check fits, so the quick check is used there. Scrambled copies of the carved text go through the same test.

## Walkthrough, by hand

1. Pick a move, say a clockwise quarter turn of a grid 7 wide, and write where each known letter lands in the carved text.
2. Pick a key length, say 9, and an order: each known letter's slot is its landing place mod 9 (move first) or its message place mod 9 (table first).
3. Write one line per known letter: place of the carved letter in the cipher alphabet = place of the known letter in the plain alphabet + key value of the slot.
4. If one slot has the same known letter under two carved letters, or two known letters under one carved letter, stop: dead.
5. Otherwise solve the lines mod 13 and mod 2; if two letters of one alphabet are always forced onto one place, dead.
6. Else look for two alphabets and a key that satisfy every line; if found, check it: the setting fits.
7. Repeat for every move, both orders and key lengths 1-10, and on scrambled copies; for longer keys stop at step 4.

## Worked example (generated)

```
move: turn cw 7 (write the message in rows of 7, read the columns bottom to top); then the table, key length 9

place  known  lands at  carved  slot (landing place mod 9)
   22      E        11       U     1
   23      A        25       V     6
   24      S        39       Q     2
   25      T        53       K     7
   26      N        67       V     3
   27      O        81       T     8
   28      R        94       K     3
   29      T        10       H     0
   30      H        24       R     5
   31      E        38       T     1
   32      A        52       J     6
   33      S        66       P     2
   34      T        80       X     7
   64      B         5       U     4
   65      E        19       B     0
   66      R        33       S     5
   67      L        47       Z     1
   68      I        61       N     6
   69      N        75       W     2
   70      C        88       U     6
   71      L         4       R     3
   72      O        18       F     8
   73      C        32       K     4
   74      K        46       K     0
a slot sends one known letter to two carved letters (or two to one): dead
```

## Lineage

Inherits from 0132-two-free-alphabets-every-move-exact-to-ten. What changed: F6.2, third attempt. 0131 (exact at every length) and 0132 (exact at 1-10) both ran out of budget with no copper comparison: the depth-first search has a heavy tail even at short keys (a few settings in a thousand ran 200,000 nodes, up to 21 s). Here the node limit is 2,000 (mean 7 ms per move, both orders, lengths 1-10) and undecided settings are counted per text; jobs are grouped by move so that a cut-off leaves complete moves for every text. Lengths 11-26: the per-slot test only (exact as a refutation), because 0131 and 0132 found 97-99% of per-slot survivors fit there (0131: 7,072 of 7,152 at 26 on 10,625 moves; 0132: 1,028 of 1,054 on 64 moves).

## Hypothesis (domain expert)

C1(a) (Sanborn, CNN 2005, knowledge/sources/cnn-2005-sanborn-interview-transcript.txt: 'I used a matrix code... and then went back to this table to do the ultimate'), C27(c) (a table 'slightly different from the one on Kryptos'), C2(a). Model: the type-1 library (27,852 maps, as 0097 and 0129) and Quagmire IV: C(c) = P(m) + k[slot], P and C independent unknown bijections, slot = carved place (order A: move, then table) or message place (order B: table, then move). The Beaufort form is the same family with P reflected; a key alphabet drops out. Exact decision as 0123 (mod 13 and mod 2, each alphabet one-to-one; enumerate at rank <= 5, else depth-first search, 200,000 nodes, 'undecided' reported); every fit re-checked. The per-slot test (within a slot, known to carved must be one-to-one) is implied by the model. 0100 and 0102 found Quagmire IV at period 3 after a move marginal (12 distinct check sets against 0-11, p about 0.24 after selection) under 0097's relaxation; this run decides period 3 exactly on all moves and ten coppers. A setting the search cannot finish in 2,000 nodes is reported undecided, not dead.

## Prediction

K4's fits per (order, length) at 1-10, and its per-slot survivors at 11-26, lie at the coppers' rate: K4 is above all ten coppers in no more of the 52 cells than the most any single copper manages against the rest. Period 3 after a move (0131 found 6 fits on part of the library) is inside the coppers' range. Undecided settings are under 1% of decided ones on every text. A K4 count beyond the null stops the queue. Zero candidates.

## Method

1. Build the 27,852 moves.
2. For each move, order and key length, write the 24 equations; apply the per-slot test.
3. Lengths 1-10: decide the survivors exactly, on K4 and ten scrambled coppers, every move.
4. Lengths 11-26: count per-slot survivors on every text.
5. Per cell (order, length), K4 against the coppers; cells where K4 is above every copper, against each copper against the rest.
6. Validate on planted Quagmire IV texts.

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
 "family": "two unknown alphabets (Quagmire IV, Beaufort included by reflection), periodic key 1-26, after (A) or before (B) a type-1 move",
 "moves": 27852,
 "moves_done_all_texts": 27852,
 "exhaustive": "exact decision at key lengths 1-10 (0123's decider, 2,000 nodes, undecided counted); per-slot refutation at 11-26",
 "summary": {
  "A": {
   "statistic_by_L": "exact fits at 1-10, per-slot survivors at 11-26",
   "k4_by_L": [
    0,
    0,
    16,
    53,
    159,
    776,
    1335,
    2372,
    3089,
    3188,
    4920,
    7365,
    9328,
    9545,
    8727,
    10185,
    9909,
    12871,
    12262,
    12569,
    12820,
    14916,
    16705,
    16593,
    13463,
    18680
   ],
   "coppers_min_by_L": [
    0,
    0,
    1,
    29,
    132,
    367,
    867,
    1055,
    1439,
    2867,
    4794,
    4811,
    5454,
    6892,
    6090,
    7600,
    7907,
    8226,
    7674,
    11595,
    11268,
    13192,
    13923,
    13508,
    13207,
    11506
   ],
   "coppers_max_by_L": [
    0,
    0,
    12,
    89,
    299,
    751,
    2511,
    3057,
    3117,
    4323,
    8871,
    8100,
    9530,
    11499,
    10282,
    12600,
    11205,
    12183,
    13585,
    13836,
    15482,
    17422,
    18256,
    16274,
    17806,
    19373
   ],
   "smallest_L_with_k4_fit": 3
  },
  "B": {
   "statistic_by_L": "exact fits at 1-10, per-slot survivors at 11-26",
   "k4_by_L": [
    0,
    0,
    0,
    3,
    13,
    4297,
    6695,
    7321,
    0,
    13327,
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
   "coppers_min_by_L": [
    0,
    0,
    0,
    0,
    2,
    3730,
    6249,
    7691,
    0,
    12537,
    15589,
    16606,
    18372,
    18075,
    707,
    20475,
    769,
    20452,
    703,
    18149,
    18075,
    19733,
    21160,
    22886,
    24697,
    26728
   ],
   "coppers_max_by_L": [
    0,
    0,
    0,
    7,
    18,
    4607,
    7230,
    8653,
    0,
    13586,
    16283,
    17610,
    18846,
    19266,
    827,
    21035,
    890,
    21670,
    795,
    19302,
    19266,
    20461,
    21798,
    23405,
    25042,
    26916
   ],
   "smallest_L_with_k4_fit": 4
  }
 },
 "k4_fits_at_L_le_5": [
  {
   "route": "K3 rule a=5 b=2",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=5 b=2 inverse",
   "order": "A",
   "L": 3
  },
  {
   "route": "K3 rule a=8 b=2 inverse",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=30 b=2 inverse",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=34 b=2",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=39 b=3",
   "order": "B",
   "L": 5
  },
  {
   "route": "K3 rule a=67 b=4 inverse",
   "order": "A",
   "L": 4
  },
  {
   "route": "K3 rule a=79 b=4",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=90 b=7",
   "order": "A",
   "L": 3
  },
  {
   "route": "K3 rule a=62 b=8 inverse",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=76 b=9 inverse",
   "order": "A",
   "L": 4
  },
  {
   "route": "K3 rule a=68 b=10 inverse",
   "order": "B",
   "L": 5
  },
  {
   "route": "K3 rule a=34 b=11 inverse",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=89 b=11 inverse",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=41 b=12",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=42 b=12",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=31 b=17 inverse",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=32 b=17 inverse",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=35 b=17 inverse",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=38 b=17",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=62 b=17",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=65 b=17 inverse",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=71 b=17 inverse",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=52 b=18 inverse",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=53 b=18 inverse",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=63 b=18 inverse",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=64 b=18 inverse",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=66 b=18 inverse",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=67 b=18 inverse",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=88 b=18 inverse",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=89 b=18 inverse",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=6 b=19",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=48 b=19",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=53 b=19",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=58 b=19",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=72 b=19",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=74 b=19",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=77 b=19",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=24 b=20",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=60 b=20",
   "order": "A",
   "L": 3
  },
  {
   "route": "K3 rule a=64 b=20",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=81 b=21 inverse",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=83 b=22",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=13 b=23",
   "order": "A",
   "L": 4
  },
  {
   "route": "K3 rule a=88 b=23",
   "order": "A",
   "L": 4
  },
  {
   "route": "K3 rule a=18 b=24",
   "order": "A",
   "L": 4
  },
  {
   "route": "K3 rule a=23 b=24",
   "order": "A",
   "L": 4
  },
  {
   "route": "K3 rule a=35 b=24",
   "order": "A",
   "L": 4
  },
  {
   "route": "K3 rule a=40 b=24",
   "order": "A",
   "L": 4
  },
  {
   "route": "K3 rule a=55 b=24",
   "order": "A",
   "L": 4
  },
  {
   "route": "K3 rule a=58 b=24 inverse",
   "order": "B",
   "L": 5
  },
  {
   "route": "K3 rule a=72 b=24",
   "order": "A",
   "L": 4
  },
  {
   "route": "K3 rule a=75 b=24 inverse",
   "order": "B",
   "L": 4
  },
  {
   "route": "K3 rule a=15 b=25",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=18 b=25",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=56 b=26 inverse",
   "order": "B",
   "L": 4
  },
  {
   "route": "K3 rule a=20 b=30",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=50 b=30",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=58 b=30",
   "order": "A",
   "L": 5
  },
  {
   "route": "K3 rule a=59 b=30",
   "order": "A",
   "L": 5
  }
 ],
 "n_k4_fits_at_L_le_5": 244,
 "cells_k4_above_every_copper": [
  [
   "A",
   "IV",
   3
  ],
  [
   "A",
   "IV",
   6
  ],
  [
   "A",
   "IV",
   18
  ],
  [
   "A",
   "IV",
   24
  ],
  [
   "B",
   "IV",
   13
  ]
 ],
 "null_cells_above_rest_per_copper": [
  4,
  3,
  5,
  3,
  6,
  2,
  5,
  7,
  2,
  4
 ],
 "undecided_k4_and_coppers": [
  249,
  244,
  231,
  236,
  302,
  272,
  265,
  220,
  269,
  240,
  285
 ],
 "stop_queue": false,
 "controls": "10 shuffled coppers (seed 133), every move done",
 "plants": "6 planted Quagmire IV texts (random move, both orders, lengths 3-10) decided 'fit'"
}
```

Notes: 27,852 of 27,852 moves on K4 and 10 coppers. Smallest key length with a K4 fit: {'A': 3, 'B': 4}; fits at L<=5: 244. K4 above every copper in 5 of 52 cells; each copper against the rest 2-7. Undecided per text: [249, 244, 231, 236, 302, 272, 265, 220, 269, 240, 285]. Stop queue: False.


