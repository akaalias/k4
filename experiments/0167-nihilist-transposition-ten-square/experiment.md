# 0167-nihilist-transposition-ten-square: F6.14: the Nihilist transposition on a 10 x 10 square with three blank cells, one key of every order for rows and columns, then or before a repeating key on the table

**Family:** 6-transposition-then-tableau  
**Parent:** 0135-hand-padding-at-every-grid-stage  
**Decision:** reverted  
**Run:** 2026-10-16T22:53:09+00:00, 225.7 s, status ran  
**Time by phase:** unattributed 75 s, run 226 s, record 0 s

## In plain words

Write the message into a 10 by 10 square (three squares left empty, since 97 is three short of 100), then rearrange the rows and the columns in the same order, given by a key, and copy the square out. We try every possible order of the ten rows and columns, every place for the empty squares and both ways of copying out, each with a repeating secret word on the sculpture's table, against the 24 known letters and scrambled copies.

## Walkthrough, by hand

1. Write the 97 letters into a 10 x 10 square row by row, leaving the last three squares empty.
2. Take a key order of the ten rows and columns, say 3 7 0 9 1 5 2 8 4 6: row 3 becomes the first row, row 7 the second, and the columns likewise.
3. Copy the square out row by row, skipping the empty squares.
4. Note where each known letter lands; with a repeating key of length p on the table, two known letters landing a multiple of p apart must force the same key letter.
5. Repeat for every order, place of the empty squares and reading, and on scrambled copies.

## Worked example (generated)

```
10 x 10 square, last three cells empty; rows and columns reordered 3 7 0 9 1 5 2 8 4 6; read by rows

place  letter  square cell  new cell  lands at  carved
   22       E        (2,1)     (6,4)        62       F
   23       A        (2,2)     (6,6)        64       N
   24       S        (2,3)     (6,0)        58       A
   64       B        (6,3)     (9,0)        88       U
   65       E        (6,4)     (9,8)        96       A
   74       K        (7,3)     (1,0)        11       U
```

## Lineage

Inherits from 0135-hand-padding-at-every-grid-stage. What changed: F6.14. The Nihilist transposition writes the text into a full square and reorders its rows and its columns by one key, then reads it off by rows (or by columns). 97 is prime, so the square is 10 x 10 with three blank cells, placed at each of F6.4's eight spots (end or start of the first or last row, top or bottom of the first or last column). Every one of the 10! = 3,628,800 key orders, both readings, forward and inverse: 116 million routes, compiled (the route builder checked against Python on 200 random settings), then a repeating key 1-26 on the standard or KRYPTOS table after or before. Ten scrambled coppers.

## Hypothesis (domain expert)

C1(a) ('matrix code'), C17(b) (padding); source: reports/Scheidt patents and field ciphers.md and foreign_agent_hand_systems.md (ACA's Nihilist transposition: one key for rows and columns of a complete square; attribution to Russian Nihilists doubtful). Model: cell (r, c) of message place i (row-wise, blanks skipped) moves to (pi^-1(r), pi^-1(c)); read row-wise (or column-wise) skipping blanks. Periodic key: order A or B, 8 classes, a period live if no slot holds two different forced letters; 0134's statistic.

## Prediction

Nothing live below key length 20 beyond the coppers' rate; K4 above every copper in no more cells than the null's maximum. Zero candidates.

## Method

1. Compile the builder and the periodic-key test; check the builder against Python.
2. For each blank place and each first key element (80 jobs): every remaining order (Heap's algorithm), both readings, forward and inverse.
3. Counts per order, period and text; the fixed statistic.

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
 "family": "Nihilist transposition, 10 x 10 square, three blanks at eight places, one key of every order for rows and columns, read by rows or columns, then or before a periodic key",
 "jobs_done": 80,
 "jobs_total": 80,
 "routes": 116121600,
 "builder_checked_against_python": 200,
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
   61,
   37,
   340,
   1785,
   8364,
   52979,
   62822
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
   80,
   48902,
   35538192
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
   8,
   25,
   248,
   1363,
   7398,
   46550,
   57342
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
   39,
   38002,
   35199912
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
   2,
   4,
   368,
   51,
   480,
   1879,
   10984,
   71163,
   64565
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
   1,
   0,
   0,
   0,
   0,
   0,
   1,
   111,
   64928,
   37003968
  ]
 },
 "k4_shortest_live": {
  "A": 20,
  "B": 24
 },
 "coppers_shortest_live": {
  "A": 18,
  "B": 17
 },
 "k4_settings_live_below_20": {
  "A": 0,
  "B": 0
 },
 "controls_settings_live_below_20": {
  "A": [
   1,
   0,
   4,
   4,
   0,
   2,
   1,
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
   1,
   0,
   0,
   0,
   0
  ]
 },
 "k4_live_below_20": [],
 "cells_k4_above_every_copper": [],
 "null_cells_above_rest_per_copper": [
  2,
  2,
  1,
  1,
  1,
  1,
  0,
  0,
  1,
  5
 ],
 "stop_queue": false,
 "distinct_routes": 116121600,
 "seconds": 225,
 "controls": "10 shuffled coppers (seed 1670)",
 "exhaustive": "every job done is exact"
}
```

Notes: 116,121,600 routes (80 of 80 jobs): shortest live K4 A 20 B 24 (coppers 18, 17); K4 above every copper in 0 of 52 cells, null 0-5


