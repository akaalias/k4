# 0100-replicating-the-marginal-cells: The three marginal excesses of experiments 92, 93 and 97, recounted as distinct check sets against fifty fresh scrambled coppers

**Family:** 6-transposition-then-tableau  
**Parent:** 0097-free-mixed-alphabets-after-a-move  
**Decision:** reverted  
**Run:** 2026-10-15T20:07:33+00:00, 73.3 s, status ran  
**Time by phase:** unattributed 48 s, run 73 s, record 0 s

## In plain words

Three times tonight K4 scored a little higher than all ten scrambled copies of itself. With only ten copies, that happens by luck about one time in eleven, so it proves nothing. Here we redo exactly those three counts against fifty fresh scrambled copies and count, for each, how many copies do at least as well as K4.

## Walkthrough, by hand

1. Take one cell, say Quagmire IV at period 3 after a move.
2. For every move, write the 24 equations and keep the move if some pair of alphabets fits.
3. Moves that give the same equations up to relabelling the key slots count once.
4. Do the same on fifty scrambled copies of K4.
5. The share of copies with at least K4's count is the chance of K4's result by luck.

## Worked example (generated)

```
the four counts replicated, with what ten coppers showed in the original runs

0092  paths, after the move, period 22: K4 13 distinct check sets, ten coppers 8-15
0092  paths, after the move, period 23: K4 88, ten coppers 74-98
0093  one miss, after the move, period 22: K4 980 settings, ten coppers 526-859
0097  Quagmire IV, after the move, period 3: K4 12 distinct equation sets, ten coppers 1-11

here: the same counts as distinct sets, against fifty new coppers
```

## Lineage

Inherits from 0097-free-mixed-alphabets-after-a-move. What changed: 0092, 0093 and 0097 each left one cell where K4 sat at or just above the top of ten scrambled coppers: path routes at periods 22-23, one-miss periodic keys at period 22, and the free Quagmire IV at period 3 after a move. Ten controls cannot tell a 1-in-11 event from a signal. Here exactly those cells are recounted, with look-alike routes collapsed into distinct check sets, against fifty new coppers, and each gets an empirical p-value.

## Hypothesis (domain expert)

A replication, not a new search. Cells, fixed before the run from the records: (1) 0092, write along one of 30 grid paths and read along another, periodic key after the move, periods 22 and 23, distinct (check pairs, class) sets; (2) 0093, type-1 library, periodic key after the move with at most one known letter set aside, period 22, distinct (slot partition, class) sets; (3) 0097, type-1 library plus no move, Quagmire IV with unknown alphabets, key after the move, period 3, distinct canonical equation sets. Statistic: K4's count and the fraction of 50 shuffled coppers (seed 100) whose count is at least K4's. With three cells and four counts the multiple-comparison threshold is about p < 0.0125 for any one of them.

## Prediction

Every cell has an empirical p above 0.05 against the fifty fresh coppers: the excesses were luck. Zero candidates.

## Method

1. Rebuild the route sets of 0092 and of the type-1 library.
2. For each cell, compute the distinct check sets consistent on K4 and on fifty shuffled coppers.
3. Report K4's count, the coppers' range and mean, and the fraction of coppers at or above K4.

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
 "family": "replication of marginal cells with fresh controls",
 "controls": "50 shuffled coppers (seed 100)",
 "path_routes": 43579,
 "library_routes": 27852,
 "cells": {
  "0092 paths, after the move, period 22": {
   "k4": 13,
   "controls_min": 4,
   "controls_max": 20,
   "controls_mean": 11.02,
   "p_at_least_k4": 0.24
  },
  "0092 paths, after the move, period 23": {
   "k4": 88,
   "controls_min": 67,
   "controls_max": 116,
   "controls_mean": 88.66,
   "p_at_least_k4": 0.48
  },
  "0093 one miss, after the move, period 22": {
   "k4": 183,
   "controls_min": 134,
   "controls_max": 195,
   "controls_mean": 160.94,
   "p_at_least_k4": 0.1
  },
  "0097 Quagmire IV, after the move, period 3": {
   "k4": 12,
   "controls_min": 0,
   "controls_max": 11,
   "controls_mean": 4.8,
   "p_at_least_k4": 0.0
  }
 },
 "threshold_note": "four counts: p < 0.0125 would be needed for any one to stand"
}
```

Notes: 0092 paths, after the move, period 22: K4 13, coppers 4-20 (mean 11.02), p 0.24; 0092 paths, after the move, period 23: K4 88, coppers 67-116 (mean 88.66), p 0.48; 0093 one miss, after the move, period 22: K4 183, coppers 134-195 (mean 160.94), p 0.1; 0097 Quagmire IV, after the move, period 3: K4 12, coppers 0-11 (mean 4.8), p 0.0.


