# 0135-hand-padding-at-every-grid-stage: Hand padding at each grid stage: the blank cells in any of eight places, dropped or carried as fillers into the next grid, one or two stages, then or before a repeating key on the table

**Family:** 6-transposition-then-tableau  
**Parent:** 0082-where-the-blanks-go-in-the-grid  
**Decision:** reverted  
**Run:** 2026-10-16T11:57:55+00:00, 138.1 s, status ran  
**Time by phase:** design 0 s, test 1 s, run 138 s, record 0 s

## In plain words

97 letters never fill a grid exactly, so a person writing them in rows leaves a few empty squares somewhere: at the end, at the start, or down one side. With two grids, the empty squares of the first can disappear or be copied along as dummy letters and crossed out at the end. We try every such choice, for one and two grids, each followed or preceded by a repeating secret word on the sculpture's tables, and check them against the 24 known letters and scrambled copies of the carved text.

## Walkthrough, by hand

1. Write the 97 letters in rows of 8: 13 rows hold 104 squares, so 7 stay empty; leave them at the bottom of the last column and the six above it (place P6).
2. Read the columns left first, top to bottom (Sanborn's matrix), and copy each empty square out as a dummy letter (keep): 104 symbols, the E of place 22 now 68th among the real letters.
3. (In drop mode the empty squares are simply skipped.)
4. Write the 104 symbols in rows of 9: 12 rows hold 108 squares, so leave the first 4 squares of the top row empty (P2); read the columns from the bottom up, left first (a quarter turn), and strike out every dummy: the E lands at place 90, where the copper has U.
5. Note where each known letter has landed and the carved letter there; with a key of length p on the table, two known letters in one slot must force the same key letter.
6. Repeat for every place, reading, width, drop or keep, the key before or after, and on scrambled copies.

## Worked example (generated)

```
rows of 8, blanks down the last column from the bottom, read down the columns left first, blanks kept as dummies;
then rows of 9, blanks at the start of the first row, read up the columns left first; dummies struck out

place  letter  after grid 1  after grid 2  copper there
   22       E            68            90             U
   23       A            81            34             S
   24       S            94            76             G
   64       B            22            84             D
   65       E            35            29             R
   74       K            62            26             Q
```

## Lineage

Inherits from 0082-where-the-blanks-go-in-the-grid. What changed: F6.4 (padding applied separately at each grid stage; nulls dropped between griddings). 0082 tried blanks at the start of the first row or the end of the last, and carried as fillers, for one and two clockwise turns and short-row-on-top columnar. The list of hand rules (NOTEBOOK 2026-10-16) adds six places for the blank cells: start of the last row, end of the first row, and down the first or last column from the top or from the bottom; each grid of a two-stage move chooses its own place, its own reading (clockwise turn, or Sanborn's rows-then-columns-down) and whether the first grid's blanks vanish or travel as filler letters to be struck out at the end. One stage: 8 places x 4 readings x widths 2-96. Two stages: (8 places x 2 readings x widths 2-48)^2 x drop or keep.

## Hypothesis (domain expert)

C1(a) (Sanborn, CNN 2005, knowledge/sources/cnn-2005-sanborn-interview-transcript.txt: 'you write a line of plain text out, right, in successive rows. And then basically you write it going from top to bottom... double matrixes and triple matrixes'), C2(a), C17(b) ('whether it's 97, whether it's 100... I seem to like to manipulate the information'). 97 is prime, so every hand grid has h w - 97 blank cells; research note combined_methods_and_sevens.md: classical practice leaves the last row short, completes with nulls, or fixes blank cells; every coded search pads once at the ends (gap 6: per-stage padding). Places for b blanks: end of the last row (P1, covered by 0008), start of the first row (P2, 0082), start of the last row (P3), end of the first row (P4), last column from the top (P5) or bottom (P6), first column from the top (P7) or bottom (P8); column places need b <= h. Readings: cw (left column first, bottom up: the K3 turn), col (left first, top down: Sanborn's matrix code); for one stage also ccw and colr. Keep mode: the first grid's blank cells are read out as filler letters and fill cells of the second grid, all fillers struck out at the end. Key: periodic tableau 1-26 after (order A) or before (order B) the move, 8 classes of standard/KRYPTOS plain and cipher alphabets and Beaufort-or-not; a period is live if no slot holds two different forced key letters. Exact; ten scrambled coppers.

## Prediction

As in 0082 and 0083: nothing live below period 20 beyond the coppers' rate, and K4 above every copper in no more (order, period) cells than the most any single copper manages against the rest. A K4 count beyond that null stops the queue for a replication. Zero candidates.

## Method

1. For every width, reading and place of the blanks, the where-map of one stage (keep mode: fillers counted).
2. Compose every pair at widths 2-48 (both readings, all places, drop or keep), forward and inverse; skip repeats.
3. For each route, class and text, the key letter each known letter forces at its slot.
4. Period p (1-26) is live in an order if no slot holds two different forced letters.
5. Count live settings per period on K4 and ten scrambled coppers; compare cell by cell; list K4's live settings below 20.

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
 "family": "hand padding per grid stage: blank cells in one of eight places, dropped or carried as fillers; one or two stages; then or before a periodic tableau key",
 "places": {
  "P1": "end of last row",
  "P2": "start of first row",
  "P3": "start of last row",
  "P4": "end of first row",
  "P5": "last column from the top",
  "P6": "last column from the bottom",
  "P7": "first column from the top",
  "P8": "first column from the bottom"
 },
 "readings": {
  "cw": "left column first, bottom up",
  "ccw": "right first, top down",
  "col": "left first, top down",
  "colr": "right first, bottom up"
 },
 "singles": "8 places x 4 readings x widths 2-96",
 "doubles": "(8 places x readings cw/col x widths 2-48)^2 x drop/keep",
 "first_stages_done": 3040,
 "first_stages_total": 3040,
 "distinct_routes": 874572,
 "duplicates_skipped_within_share": 174516,
 "periods": [
  1,
  26
 ],
 "classes": 8,
 "k4_live_by_period": {
  "A": [
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
   10,
   32,
   396,
   4396,
   8758,
   23263
  ],
  "B": [
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
   401,
   268313
  ]
 },
 "controls_live_by_period_min": {
  "A": [
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
   23,
   302,
   3503,
   8794,
   21638
  ],
  "B": [
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
   364,
   267159
  ]
 },
 "controls_live_by_period_max": {
  "A": [
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
   4,
   17,
   73,
   474,
   5521,
   9130,
   23551
  ],
  "B": [
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
   1,
   420,
   271825
  ]
 },
 "k4_settings_live_below_20": {
  "A": 0,
  "B": 0
 },
 "controls_settings_live_below_20": {
  "A": [
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
  "B": [
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
  ]
 },
 "k4_live_below_20": [],
 "cells_k4_above_every_copper": [],
 "null_cells_above_rest_per_copper": [
  1,
  1,
  0,
  0,
  1,
  2,
  1,
  1,
  2,
  1
 ],
 "stop_queue": false,
 "controls": "10 shuffled coppers (seed 134), identical search",
 "order_A": "stages, then key (slot = landing place mod p)",
 "order_B": "key, then stages (slot = message place mod p)"
}
```

Notes: 874,572 routes (3040 of 3040 first stages) x 8 classes x 2 orders, periods 1-26. K4 settings live below 20: 0 (A), 0 (B); coppers A 0-0, B 0-0. K4 above every copper in 0 of 52 cells; null 0-2. Stop queue: False.


