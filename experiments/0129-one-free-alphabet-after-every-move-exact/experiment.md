# 0129-one-free-alphabet-after-every-move-exact: Every move of the type-1 library, then a table built on one alphabet in an unknown order, key lengths 1-26, decided exactly

**Family:** 6-transposition-then-tableau  
**Parent:** 0097-free-mixed-alphabets-after-a-move  
**Decision:** reverted  
**Run:** 2026-10-16T10:08:55+00:00, 637.2 s, status ran  
**Time by phase:** design 816 s, implement 95 s, test 312 s, run 637 s, record 0 s

## In plain words

Sanborn said he wrote the message into a grid and read it out another way (a 'matrix'), then used the big lettered table. Earlier tests fixed the table's alphabet to the plain A-Z or the KRYPTOS one. Here the table's scrambled alphabet may be any of the possible orders, and for each of about 28,000 ways of moving the letters, each key length up to 26 and two ways of reading the table, arithmetic on the 24 known letters decides whether any alphabet and key could work at all. We do the same on scrambled copies of the carved text to see how often that happens by chance.

## Walkthrough, by hand

1. Pick a move, say a clockwise quarter turn of a grid 7 wide, and write where each of the 24 known letters lands in the carved text.
2. Pick a key length, say 9, and the order 'move first': each known letter's slot is its landing place mod 9.
3. Write one line per known letter: place-in-alphabet of the carved letter there = place of the known letter + key value of the slot (all unknown).
4. If two known letters in one slot sit under the same carved letter but differ, or the same known letter under two carved letters, stop: dead.
5. Otherwise solve the 24 lines mod 13 and mod 2; if two different letters are always forced onto the same place, dead.
6. Else look for one alphabet and key that satisfy every line; if found, check it, and the setting fits.
7. Repeat for every move, key lengths 1-26, the Beaufort form (carved place = key minus known place), and on scrambled copies.

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
form V: a slot sends one known letter to two carved letters (or two to one): dead
form B: a slot sends one known letter to two carved letters (or two to one): dead
```

## Lineage

Inherits from 0097-free-mixed-alphabets-after-a-move. What changed: F6.1 (one free alphabet after or before each move), first exact test, order A (move, then the table); order B follows as 0130 because both do not fit one 30-minute budget. 0097 tested this only with a relaxation that can refute but not confirm, at key lengths 3, 7 and 21, and only in the added (Vigenere-like) form; that made it weak. Here 0119's exact decider (mod 13 and mod 2, exhaustive where the solution space is small, a depth-first search with a node limit elsewhere, every fit re-checked) runs on every one of the 27,852 moves, key lengths 1-26, both table forms (added and Beaufort). Controls: 12 scrambled coppers on a fixed sample of 800 moves, with K4 counted on the same sample.

## Hypothesis (domain expert)

C1(a) (Sanborn, CNN 2005, knowledge/sources/cnn-2005-sanborn-interview-transcript.txt: 'I used a matrix code, and then we can possibly use this code to decipher with... double matrixes and triple matrixes... and then went back to this table to do the ultimate'), C27(c) (his table 'slightly different from the one on Kryptos'), C2(a). Model: plaintext p moved by a permutation pi of the type-1 library (K3's rule a + b i mod 97 at all 9,312 settings, one quarter turn cw/ccw at widths 2-96, two cw turns at every width pair, plain columnar both ways, keyed columnar from the vocabulary and theme words, each forward and inverse: 27,852 distinct maps, as 0097), and one unknown bijection A on both sides of a periodic table with key k of length L. Order A only (move, then table): A(c_j) = s A(m_j) + k[j mod L], slot = carved place j; order B is 0130. Form V: s = +1 (Quagmire III with free order; variant Beaufort is V with k negated); form B: s = -1 (Beaufort). The 24 known letters give 24 equations over Z26; exact decision as 0119 (refute when two letters coincide mod 13 and mod 2, or three mod 13; enumerate the mod-13 space up to scaling at rank <= 5; else 300 random points as a witness hunt, then depth-first search with pruning, 200,000 nodes, 'undecided' reported). A per-slot filter (each slot one-to-one) runs first; it is implied by the model, so it loses nothing. Zekios (2026, research note combined_methods_and_sevens.md) did any-alphabet keys only to period 12 and only for double rotations.

## Prediction

K4 has fitting settings at key lengths of about 7 and up in both forms, at the rate of the scrambled coppers: in no more cells (form, length) is K4 above all 12 coppers than the most any single copper manages against the rest. Key lengths 1-5 have no fit. If K4 beats that null count, the queue stops for a replication (cells where K4 fits and no copper does are listed, and count in it). Zero candidates; fits that remain are at the coppers' rate and only an English climb could judge them, which 0120 found powerless, so they are blocked, not open.

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
 "family": "one unknown alphabet on both sides (Quagmire III / Beaufort with a free order), periodic key 1-26, after a type-1 move (order A)",
 "moves": 27852,
 "k4_moves_done": 27852,
 "cells": "order A (move, then table) x 2 forms x key lengths 1-26",
 "exhaustive": "exact decision per setting (0119's decider; undecided counted where the node limit was hit)",
 "summary": {
  "AV": {
   "k4_fits_full_library_by_L": [
    0,
    0,
    0,
    0,
    0,
    2,
    48,
    191,
    444,
    641,
    1068,
    1837,
    2714,
    3061,
    3161,
    3998,
    4183,
    5617,
    5743,
    6111,
    6281,
    7978,
    9079,
    9471,
    8166,
    11411
   ],
   "k4_per_slot_survivors_by_L": [
    0,
    0,
    44,
    116,
    270,
    1207,
    1758,
    3012,
    3688,
    3549,
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
   "k4_undecided_by_L": [
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
    2,
    2,
    0,
    20,
    1,
    4,
    1,
    0,
    1,
    2,
    2,
    0,
    0,
    2,
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
    14,
    24,
    24,
    59,
    79,
    85,
    94,
    114,
    121,
    162,
    151,
    189,
    188,
    205,
    275,
    290,
    244,
    326
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
    8,
    12,
    22,
    16,
    43,
    69,
    68,
    93,
    105,
    108,
    143,
    137,
    130,
    157,
    219,
    181,
    237,
    239
   ],
   "coppers_fits_sample_max_by_L": [
    0,
    0,
    0,
    0,
    1,
    0,
    3,
    8,
    17,
    23,
    52,
    55,
    73,
    107,
    122,
    150,
    165,
    147,
    183,
    235,
    223,
    263,
    301,
    273,
    322,
    341
   ],
   "smallest_L_with_k4_fit": 6
  },
  "AB": {
   "k4_fits_full_library_by_L": [
    0,
    0,
    0,
    0,
    0,
    1,
    16,
    54,
    174,
    301,
    646,
    1271,
    2186,
    2516,
    2534,
    3341,
    3508,
    4810,
    5092,
    5641,
    5933,
    7310,
    8486,
    9293,
    7786,
    11251
   ],
   "k4_per_slot_survivors_by_L": [
    0,
    0,
    44,
    116,
    270,
    1207,
    1758,
    3012,
    3688,
    3549,
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
    1,
    1,
    1,
    1,
    3,
    3,
    0,
    0,
    2,
    2,
    1,
    3,
    1,
    2
   ],
   "k4_fits_sample_by_L": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    1,
    4,
    5,
    16,
    34,
    67,
    77,
    67,
    89,
    108,
    138,
    130,
    159,
    175,
    192,
    254,
    278,
    235,
    327
   ],
   "coppers_fits_sample_min_by_L": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    1,
    4,
    11,
    11,
    33,
    49,
    54,
    73,
    87,
    99,
    112,
    117,
    130,
    147,
    200,
    161,
    222,
    229
   ],
   "coppers_fits_sample_max_by_L": [
    0,
    0,
    0,
    0,
    0,
    0,
    2,
    5,
    9,
    10,
    40,
    40,
    70,
    82,
    98,
    126,
    150,
    149,
    163,
    204,
    187,
    246,
    275,
    269,
    333,
    314
   ],
   "smallest_L_with_k4_fit": 6
  }
 },
 "k4_fits_at_L_le_8": [
  {
   "route": "K3 rule a=37 b=1",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=40 b=1 inverse",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=46 b=1 inverse",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=47 b=1 inverse",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=47 b=1 inverse",
   "order": "A",
   "form": "B",
   "L": 8
  },
  {
   "route": "K3 rule a=4 b=2 inverse",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=8 b=2 inverse",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=16 b=2 inverse",
   "order": "A",
   "form": "B",
   "L": 8
  },
  {
   "route": "K3 rule a=17 b=2 inverse",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=19 b=2 inverse",
   "order": "A",
   "form": "B",
   "L": 8
  },
  {
   "route": "K3 rule a=83 b=2 inverse",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=85 b=2 inverse",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=87 b=2 inverse",
   "order": "A",
   "form": "V",
   "L": 7
  },
  {
   "route": "K3 rule a=87 b=2 inverse",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=18 b=3",
   "order": "A",
   "form": "B",
   "L": 8
  },
  {
   "route": "K3 rule a=68 b=3",
   "order": "A",
   "form": "B",
   "L": 7
  },
  {
   "route": "K3 rule a=25 b=5 inverse",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=37 b=5 inverse",
   "order": "A",
   "form": "B",
   "L": 8
  },
  {
   "route": "K3 rule a=55 b=5",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=56 b=5",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=82 b=7 inverse",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=87 b=7",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=59 b=8",
   "order": "A",
   "form": "V",
   "L": 7
  },
  {
   "route": "K3 rule a=66 b=9",
   "order": "A",
   "form": "V",
   "L": 7
  },
  {
   "route": "K3 rule a=75 b=9",
   "order": "A",
   "form": "V",
   "L": 7
  },
  {
   "route": "K3 rule a=82 b=9",
   "order": "A",
   "form": "V",
   "L": 7
  },
  {
   "route": "K3 rule a=7 b=13 inverse",
   "order": "A",
   "form": "B",
   "L": 8
  },
  {
   "route": "K3 rule a=13 b=13 inverse",
   "order": "A",
   "form": "B",
   "L": 8
  },
  {
   "route": "K3 rule a=53 b=13",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=80 b=13 inverse",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=87 b=13 inverse",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=90 b=13 inverse",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=67 b=16 inverse",
   "order": "A",
   "form": "B",
   "L": 7
  },
  {
   "route": "K3 rule a=43 b=20",
   "order": "A",
   "form": "B",
   "L": 6
  },
  {
   "route": "K3 rule a=83 b=21",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=37 b=22",
   "order": "A",
   "form": "B",
   "L": 8
  },
  {
   "route": "K3 rule a=81 b=22 inverse",
   "order": "A",
   "form": "V",
   "L": 7
  },
  {
   "route": "K3 rule a=14 b=23",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=17 b=23 inverse",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=19 b=23 inverse",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=30 b=23 inverse",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=33 b=23 inverse",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=51 b=23 inverse",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=57 b=23 inverse",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=58 b=23 inverse",
   "order": "A",
   "form": "B",
   "L": 7
  },
  {
   "route": "K3 rule a=9 b=24",
   "order": "A",
   "form": "V",
   "L": 7
  },
  {
   "route": "K3 rule a=13 b=25 inverse",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=16 b=25 inverse",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=65 b=25",
   "order": "A",
   "form": "V",
   "L": 7
  },
  {
   "route": "K3 rule a=89 b=25 inverse",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=2 b=26 inverse",
   "order": "A",
   "form": "B",
   "L": 8
  },
  {
   "route": "K3 rule a=5 b=26 inverse",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=8 b=26 inverse",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=47 b=26 inverse",
   "order": "A",
   "form": "B",
   "L": 8
  },
  {
   "route": "K3 rule a=48 b=26 inverse",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=51 b=26 inverse",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=55 b=26 inverse",
   "order": "A",
   "form": "V",
   "L": 8
  },
  {
   "route": "K3 rule a=62 b=26",
   "order": "A",
   "form": "B",
   "L": 7
  },
  {
   "route": "K3 rule a=62 b=26 inverse",
   "order": "A",
   "form": "V",
   "L": 7
  },
  {
   "route": "K3 rule a=84 b=26 inverse",
   "order": "A",
   "form": "B",
   "L": 8
  }
 ],
 "n_k4_fits_at_L_le_8": 312,
 "controls": "12 shuffled coppers (seed 129) on 800 sampled moves; K4 on the same sample",
 "cells_k4_above_every_copper": [
  [
   "A",
   "V",
   10
  ],
  [
   "A",
   "V",
   12
  ],
  [
   "A",
   "V",
   13
  ],
  [
   "A",
   "V",
   18
  ],
  [
   "A",
   "V",
   24
  ],
  [
   "A",
   "B",
   24
  ],
  [
   "A",
   "B",
   26
  ]
 ],
 "null_cells_above_rest_per_copper": [
  1,
  0,
  8,
  0,
  1,
  8,
  0,
  3,
  2,
  1,
  4,
  3
 ],
 "cells_k4_fits_no_copper_does": [],
 "undecided_sample_k4_and_coppers": [
  0,
  2,
  3,
  0,
  1,
  0,
  0,
  4,
  0,
  2,
  2,
  0,
  1
 ],
 "stop_queue": false,
 "plants": "6 planted texts (random move, order A, form, length 3-21) all decided 'fit'"
}
```

Notes: K4 on 27,852 of 27,852 moves; smallest key length with a fit {'AV': 6, 'AB': 6}; fits at L<=8: 312. Sample of 800 moves: K4 above every copper in 7 of 52 cells, coppers against the rest 0-8; cells where only K4 fits: []. Stop queue: False.


