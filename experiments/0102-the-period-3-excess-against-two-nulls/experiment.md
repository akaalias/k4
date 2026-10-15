# 0102-the-period-3-excess-against-two-nulls: The period-3 free-alphabet excess, against 400 scrambled coppers and 400 that keep K4's width-21 columns

**Family:** 6-transposition-then-tableau  
**Parent:** 0100-replicating-the-marginal-cells  
**Decision:** reverted  
**Run:** 2026-10-15T20:10:39+00:00, 120.1 s, status ran  
**Time by phase:** unattributed 72 s, run 120 s, record 0 s

## In plain words

In experiment 100 one count stayed higher on K4 than on fifty scrambled copies. K4 has a known oddity: letters 21 places apart repeat in pairs more than chance. Because 21 is a multiple of 3, that oddity could raise this count by itself. So we compare K4 with 400 ordinary scrambles and with 400 scrambles that keep the oddity, by moving whole columns of a 21-wide grid around.

## Walkthrough, by hand

1. Write K4 in rows of 21; the last row has 13 letters.
2. Shuffle the first 13 columns among themselves and the last 8 among themselves; every pair of letters 21 apart stays a pair.
3. For each move, test whether some pair of alphabets with a 3-letter key fits the 24 known letters, and collect the distinct ways it fits.
4. Compare K4's count with the counts on these copies and on ordinary scrambles.

## Worked example (generated)

```
K4 in rows of 21, and one copy with its columns shuffled (13 short-row columns among themselves, 8 among themselves)

  OBKRUOXOGHULBSOLIFBBW
  FLRVQQPRNGKSSOTWTQSJQ
  SSEKZZWATJKLUDIAWINFB
  NYPVTTMZFPKWGDKZXTJCD
  IGKUHUAUEKCAR

  KHBUUOXROLOBGSBIBWLOF
  RGLQKRPVQSFSNOJTSQWTQ
  EJSZKAWKZLSUTDFWNBAII
  PPYTKZMVTWNGFDCXJDZKT
  KKGHCUAUUAIRE

letter pairs 21 apart that repeat: K4 11, the copy 11
```

## Lineage

Inherits from 0100-replicating-the-marginal-cells. What changed: 0100 left one cell above all 50 coppers: Quagmire IV at period 3 after a move, 12 distinct equation sets against 0-11. Here the four period-3 cells (one alphabet or a pair, key after or before the move) are counted against 400 plain shuffles, with a look-elsewhere correction across the four, and against 400 copies of K4 whose 21-wide grid has its columns shuffled, which keeps every pair of letters 21 apart and so K4's width-21 repeats.

## Hypothesis (domain expert)

Follow-up of 0097 and 0100. Mechanism to test: carved places 21 apart share a key slot mod 3, and K4 has 11 repeated letter pairs 21 apart (0056), so a period-3 key after a move may fit K4 more often for that reason alone. Null A: 400 letter shuffles (seed 102). Null B: 400 column permutations of K4 written 21 wide, the 13 columns of the short last row permuted among themselves and the other 8 among themselves, so every vertical pair is kept. Cells: Quagmire III or IV, key after (A) or before (B) the move, period 3; type-1 library plus no move; distinct canonical equation sets; linear test mod 2 and mod 13 as in 0097. Report K4's p under each null and, under null A, the share of shuffles whose smallest p over the four cells is at most K4's.

## Prediction

Under plain shuffles K4's cell is near p 0.02, with a look-elsewhere p above 0.05; under the column permutations K4 is unremarkable (p above 0.2), so the excess comes from the width-21 repeats. Zero candidates.

## Method

1. Build the type-1 library and the two nulls.
2. For each text, route and order, test the free-alphabet filter and the linear test at period 3 for both models, collecting distinct equation sets.
3. Compute K4's p per cell under each null and the look-elsewhere p under null A.

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
 "family": "period-3 free-alphabet cells against two nulls",
 "routes_done": 27853,
 "routes": 27853,
 "nullA": "400 letter shuffles (seed 102)",
 "nullB": "400 column permutations of K4 at width 21 (keep all 76 vertical pairs)",
 "cells": {
  "III A": {
   "k4": 0,
   "nullA_mean": 0.01,
   "nullA_max": 1,
   "p_nullA": 1.0,
   "nullB_mean": 0.01,
   "nullB_max": 1,
   "p_nullB": 1.0
  },
  "III B": {
   "k4": 0,
   "nullA_mean": 0.0,
   "nullA_max": 0,
   "p_nullA": 1.0,
   "nullB_mean": 0.0,
   "nullB_max": 0,
   "p_nullB": 1.0
  },
  "IV A": {
   "k4": 12,
   "nullA_mean": 4.81,
   "nullA_max": 23,
   "p_nullA": 0.0425,
   "nullB_mean": 6.21,
   "nullB_max": 26,
   "p_nullB": 0.1
  },
  "IV B": {
   "k4": 0,
   "nullA_mean": 0.0,
   "nullA_max": 0,
   "p_nullA": 1.0,
   "nullB_mean": 0.0,
   "nullB_max": 0,
   "p_nullB": 1.0
  }
 },
 "k4_smallest_p_nullA": 0.0425,
 "look_elsewhere_p_nullA": 0.0475
}
```

Notes: III A: K4 0, shuffles mean 0.01 max 1 p 1.000, 21-column permutations mean 0.01 max 1 p 1.000; III B: K4 0, shuffles mean 0.0 max 0 p 1.000, 21-column permutations mean 0.0 max 0 p 1.000; IV A: K4 12, shuffles mean 4.81 max 23 p 0.043, 21-column permutations mean 6.21 max 26 p 0.100; IV B: K4 0, shuffles mean 0.0 max 0 p 1.000, 21-column permutations mean 0.0 max 0 p 1.000. Look-elsewhere over the four cells under shuffles: p 0.048.


