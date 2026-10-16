# 0131-two-free-alphabets-after-every-move-exact: Every move of the type-1 library, then a table built on two alphabets in unknown orders (Quagmire IV), key lengths 1-26, decided exactly

**Family:** 6-transposition-then-tableau  
**Parent:** 0129-one-free-alphabet-after-every-move-exact  
**Decision:** reverted  
**Run:** 2026-10-16T10:37:33+00:00, 1744.1 s, status ran  
**Time by phase:** design 0 s, test 8 s, run 1744 s, record 0 s

## In plain words

The same question as the last experiment, with one more unknown: the table may use one scrambled alphabet to look up the message letter and a second, different scrambled alphabet to write the carved letter. For every one of about 28,000 ways of moving the letters first and every key length up to 26, arithmetic on the 24 known letters decides whether any such pair of alphabets and any key could work, and the same is done on scrambled copies of the carved text.

## Walkthrough, by hand

1. Pick a move, say a clockwise quarter turn of a grid 7 wide, and write where each known letter lands in the carved text.
2. Pick a key length, say 9: each known letter's slot is its landing place mod 9.
3. Write one line per known letter: place of the carved letter in the cipher alphabet = place of the known letter in the plain alphabet + key value of the slot.
4. If one slot has the same known letter under two carved letters, or two known letters under one carved letter, stop: dead.
5. Otherwise solve the lines mod 13 and mod 2; if two letters of one alphabet are always forced onto one place, dead.
6. Else look for two alphabets and a key that satisfy every line; if found, check it: the setting fits.
7. Repeat for every move and key length 1-26, and on scrambled copies.

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

Inherits from 0129-one-free-alphabet-after-every-move-exact. What changed: F6.2 (two free alphabets after or before each move), first exact test, order A (move, then the table); order B follows as 0132. 0097 tested two unknown alphabets only by a relaxation at key lengths 3, 7 and 21; 0129 did one alphabet exactly. Here 0123's exact two-alphabet decider runs on every one of the 27,852 moves at key lengths 1-26. Controls: 10 scrambled coppers on a fixed sample of 700 moves, K4 counted on the same sample.

## Hypothesis (domain expert)

C1(a) (Sanborn, CNN 2005, knowledge/sources/cnn-2005-sanborn-interview-transcript.txt: 'I used a matrix code... and then went back to this table to do the ultimate'), C27(c) (a table 'slightly different from the one on Kryptos'), C2(a). Model: message p moved by a permutation pi of the type-1 library (as 0097 and 0129: K3's rule at all 9,312 settings, quarter turns, two cw turns, plain and keyed columnar, forward and inverse; 27,852 maps), then Quagmire IV: C(c_j) = P(m_j) + k[j mod L], P and C independent unknown bijections, slot = carved place j (order A). The Beaufort form C(c) = k - P(p) is the same family with P reflected, and a key alphabet drops out, so one form covers all. 24 equations over Z26, exact decision as 0123 (mod 13 and mod 2, each alphabet one-to-one; enumerate at rank <= 5, else depth-first search, 200,000 nodes, 'undecided' reported); every fit re-checked. A per-slot one-to-one filter runs first; it is implied by the model. Zekios (2026, research note combined_methods_and_sevens.md) did any-alphabet keys only to period 12 and only for double rotations.

## Prediction

With two free alphabets more settings fit than with one (0129), from key length 6 or 7 up, at the coppers' rate: K4 is above all 10 coppers in no more cells (key lengths 1-26) than the most any single copper manages against the rest. Key lengths 1-4 have no fit. If K4 beats that null count the queue stops for a replication. Zero candidates; fitting settings are blocked (only an English climb could judge them, powerless per 0120).

## Method

1. Build the 27,852 moves of the type-1 library.
2. For each move and key length 1-26, write the 24 equations (slot = landing place mod L, known letter, carved letter there).
3. Drop settings that fail the per-slot test; decide the rest exactly (dead, fit with a re-checked witness, or undecided).
4. The same on 10 scrambled coppers over a fixed random sample of 700 moves.
5. Per key length: K4's fits on the sample against the coppers'; count lengths where K4 is above every copper and compare with the same count for each copper against the rest.
6. Validate on planted Quagmire IV texts (random move, length, alphabets, key must decide 'fit').

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
 "family": "two unknown alphabets (Quagmire IV, Beaufort included by reflection), periodic key 1-26, after a type-1 move (order A)",
 "moves": 27852,
 "k4_moves_done": 10625,
 "cells": "order A (move, then table) x key lengths 1-26",
 "exhaustive": "exact decision per setting (0123's two-alphabet decider; undecided counted where the node limit was hit)",
 "summary": {
  "AIV": {
   "k4_fits_full_library_by_L": [
    0,
    0,
    6,
    19,
    71,
    294,
    497,
    940,
    1187,
    1181,
    1727,
    2485,
    3346,
    3345,
    3192,
    3753,
    3609,
    4735,
    4546,
    4637,
    4690,
    5664,
    6301,
    6230,
    5088,
    7072
   ],
   "k4_per_slot_survivors_by_L": [
    0,
    0,
    12,
    44,
    116,
    463,
    657,
    1174,
    1390,
    1330,
    1891,
    2782,
    3585,
    3545,
    3338,
    3923,
    3731,
    4901,
    4680,
    4735,
    4806,
    5775,
    6393,
    6350,
    5129,
    7152
   ],
   "k4_undecided_by_L": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    3,
    4,
    2,
    2,
    10,
    9,
    9,
    7,
    10,
    8,
    16,
    11,
    5,
    4,
    8,
    9,
    11,
    0,
    5
   ],
   "k4_fits_sample_by_L": [
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
    0,
    0
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
    0,
    0,
    0,
    0,
    0,
    0
   ],
   "coppers_fits_sample_max_by_L": [
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
    0,
    0
   ],
   "smallest_L_with_k4_fit": 3
  }
 },
 "k4_fits_at_L_le_8": [
  {
   "route": "K3 rule a=11 b=1",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=13 b=1",
   "order": "A",
   "form": "IV",
   "L": 6
  },
  {
   "route": "K3 rule a=14 b=1",
   "order": "A",
   "form": "IV",
   "L": 6
  },
  {
   "route": "K3 rule a=14 b=1",
   "order": "A",
   "form": "IV",
   "L": 7
  },
  {
   "route": "K3 rule a=17 b=1",
   "order": "A",
   "form": "IV",
   "L": 7
  },
  {
   "route": "K3 rule a=17 b=1",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=18 b=1 inverse",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=29 b=1",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=31 b=1",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=33 b=1",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=34 b=1 inverse",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=35 b=1",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=38 b=1",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=39 b=1",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=39 b=1 inverse",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=40 b=1",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=40 b=1 inverse",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=41 b=1",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=42 b=1",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=44 b=1",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=46 b=1 inverse",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=47 b=1 inverse",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=0 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 6
  },
  {
   "route": "K3 rule a=0 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 7
  },
  {
   "route": "K3 rule a=0 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=1 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 6
  },
  {
   "route": "K3 rule a=1 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=4 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 6
  },
  {
   "route": "K3 rule a=4 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 7
  },
  {
   "route": "K3 rule a=4 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=5 b=2",
   "order": "A",
   "form": "IV",
   "L": 5
  },
  {
   "route": "K3 rule a=6 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 6
  },
  {
   "route": "K3 rule a=6 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 7
  },
  {
   "route": "K3 rule a=6 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=7 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 6
  },
  {
   "route": "K3 rule a=7 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=8 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 5
  },
  {
   "route": "K3 rule a=8 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 6
  },
  {
   "route": "K3 rule a=8 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=11 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=17 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=18 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=24 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=34 b=2",
   "order": "A",
   "form": "IV",
   "L": 5
  },
  {
   "route": "K3 rule a=34 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 7
  },
  {
   "route": "K3 rule a=35 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 7
  },
  {
   "route": "K3 rule a=37 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 7
  },
  {
   "route": "K3 rule a=38 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 7
  },
  {
   "route": "K3 rule a=47 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=52 b=2",
   "order": "A",
   "form": "IV",
   "L": 7
  },
  {
   "route": "K3 rule a=54 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 6
  },
  {
   "route": "K3 rule a=61 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=63 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=70 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 6
  },
  {
   "route": "K3 rule a=81 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 7
  },
  {
   "route": "K3 rule a=86 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=89 b=2 inverse",
   "order": "A",
   "form": "IV",
   "L": 7
  },
  {
   "route": "K3 rule a=0 b=3 inverse",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=8 b=3 inverse",
   "order": "A",
   "form": "IV",
   "L": 8
  },
  {
   "route": "K3 rule a=18 b=3",
   "order": "A",
   "form": "IV",
   "L": 8
  }
 ],
 "n_k4_fits_at_L_le_8": 1827,
 "controls": "10 shuffled coppers (seed 129) on 0 sampled moves; K4 on the same sample",
 "cells_k4_above_every_copper": [],
 "null_cells_above_rest_per_copper": [
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0
 ],
 "cells_k4_fits_no_copper_does": [],
 "undecided_sample_k4_and_coppers": [
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
  0
 ],
 "stop_queue": false,
 "plants": "6 planted texts (random move, order A, form, length 3-21) all decided 'fit'"
}
```

Notes: K4 on 10,625 of 27,852 moves; smallest key length with a fit {'AIV': 3}; fits at L<=8: 1827. Sample of 0 moves: K4 above every copper in 0 of 26 cells, coppers against the rest 0-0; cells where only K4 fits: []. Stop queue: False.


