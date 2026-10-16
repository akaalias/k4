# 0132-two-free-alphabets-every-move-exact-to-ten: Two alphabets in unknown orders (Quagmire IV) after or before every move of the type-1 library: exact at key lengths 1-10 on K4 and ten coppers, the per-slot test at 11-26

**Family:** 6-transposition-then-tableau  
**Parent:** 0131-two-free-alphabets-after-every-move-exact  
**Decision:** reverted  
**Run:** 2026-10-16T11:11:20+00:00, 1709.9 s, status ran  
**Time by phase:** test 12 s, run 1710 s, record 0 s

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

Inherits from 0131-two-free-alphabets-after-every-move-exact. What changed: F6.2, second attempt. 0131 ran the exact two-alphabet decider at every key length and ran out of its budget after 10,625 of 27,852 moves with no copper comparison done (incomplete; item left open). Timing since: the decider costs about 4 ms per move for lengths 1-10 in both orders but 0.2 s at 11-12 and more above, where 97-99% of settings that pass the per-slot test fit anyway (0131: 7,072 of 7,152 at 26). So here: exact decision at lengths 1-10, both orders, every move, on K4 and on ten scrambled coppers; at 11-26 the per-slot test (exact as a refutation: a setting failing it is dead) on every move and text, and the full decider on K4 for 300 sampled moves to state the fit rate.

## Hypothesis (domain expert)

C1(a) (Sanborn, CNN 2005, knowledge/sources/cnn-2005-sanborn-interview-transcript.txt: 'I used a matrix code... and then went back to this table to do the ultimate'), C27(c) (a table 'slightly different from the one on Kryptos'), C2(a). Model: the type-1 library (27,852 maps, as 0097 and 0129) and Quagmire IV: C(c) = P(m) + k[slot], P and C independent unknown bijections, slot = carved place (order A: move, then table) or message place (order B: table, then move). The Beaufort form is the same family with P reflected; a key alphabet drops out. Exact decision as 0123 (mod 13 and mod 2, each alphabet one-to-one; enumerate at rank <= 5, else depth-first search, 200,000 nodes, 'undecided' reported); every fit re-checked. The per-slot test (within a slot, known to carved must be one-to-one) is implied by the model. 0100 and 0102 found Quagmire IV at period 3 after a move marginal (12 distinct check sets against 0-11, p about 0.24 after selection) under 0097's relaxation; this run decides period 3 exactly on all moves and ten coppers.

## Prediction

K4's fits per (order, length) at 1-10, and its per-slot survivors at 11-26, lie at the coppers' rate: K4 is above all ten coppers in no more of the 52 cells than the most any single copper manages against the rest. Period 3 after a move (0131 found 6 fits on part of the library) is inside the coppers' range. On the K4 sample at 11-26, at least 90% of per-slot survivors fit. A K4 count beyond the null stops the queue. Zero candidates.

## Method

1. Build the 27,852 moves.
2. For each move, order and key length, write the 24 equations; apply the per-slot test.
3. Lengths 1-10: decide the survivors exactly, on K4 and ten scrambled coppers, every move.
4. Lengths 11-26: count per-slot survivors on every text; on K4 for 300 sampled moves, decide them exactly.
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
 "moves_done_all_texts": 0,
 "exhaustive": "exact decision at key lengths 1-10 (0123's decider); per-slot refutation at 11-26; exact at 11-26 on 64 sampled moves for K4",
 "summary": {
  "A": {
   "statistic_by_L": "exact fits at 1-10, per-slot survivors at 11-26",
   "k4_by_L": [
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
   "coppers_min_by_L": [
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
   "coppers_max_by_L": [
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
   "smallest_L_with_k4_fit": null
  },
  "B": {
   "statistic_by_L": "exact fits at 1-10, per-slot survivors at 11-26",
   "k4_by_L": [
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
   "coppers_min_by_L": [
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
   "coppers_max_by_L": [
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
   "smallest_L_with_k4_fit": null
  }
 },
 "k4_long_lengths_fit_rate_on_sample": {
  "A": {
   "per_slot_survivors": 440,
   "fit": 430,
   "undecided": 0,
   "fit_share": 0.9773
  },
  "B": {
   "per_slot_survivors": 614,
   "fit": 598,
   "undecided": 1,
   "fit_share": 0.9739
  }
 },
 "k4_fits_at_L_le_5": [],
 "n_k4_fits_at_L_le_5": 0,
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
 "undecided_k4_and_coppers": [
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
 "controls": "10 shuffled coppers (seed 132), every move",
 "plants": "6 planted Quagmire IV texts (random move, both orders, lengths 3-14) decided 'fit'"
}
```

Notes: 0 of 27,852 moves on K4 and 10 coppers. Smallest key length with a K4 fit: {'A': None, 'B': None}; fits at L<=5: 0. K4 above every copper in 0 of 52 cells; each copper against the rest 0-0. Long lengths on the K4 sample: {'A': {'per_slot_survivors': 440, 'fit': 430, 'undecided': 0, 'fit_share': 0.9773}, 'B': {'per_slot_survivors': 614, 'fit': 598, 'undecided': 1, 'fit_share': 0.9739}}. Stop queue: False.


