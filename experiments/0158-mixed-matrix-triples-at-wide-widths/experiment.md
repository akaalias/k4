# 0158-mixed-matrix-triples-at-wide-widths: F6.3b: every mixed triple of matrix readings with a width of 25 or more, enumerated exactly, then or before a repeating key on the table

**Family:** 6-transposition-then-tableau  
**Parent:** 0134-mixed-matrix-readings-two-and-three-stages  
**Decision:** reverted  
**Run:** 2026-10-16T22:27:33+00:00, 209.1 s, status ran  
**Time by phase:** unattributed 141 s, run 209 s, record 0 s

## In plain words

Sanborn described writing the message in rows and copying it out down the columns, sometimes two or three times, before using the table. We already tried every way of doing that three times with rows up to 24 letters wide. Here we try every three-step combination where at least one of the grids is wider, 25 to 96 letters, which gives about 95 million different scrambles. After each one, a repeating secret word of 1 to 26 letters on the sculpture's tables either has to fit the 24 known letters or it does not, and we compare how often that happens with scrambled copies of the carved text.

## Walkthrough, by hand

1. Write the 97 letters in rows of 30: three full rows and a row of 7.
2. Read the columns left first, top to bottom (Sanborn's matrix).
3. Write the result in rows of 9 and read the columns right first, bottom up.
4. Write that in rows of 41 and read the columns left first, bottom up (a quarter turn).
5. Note where each of the 24 known letters has landed and the carved letter there.
6. With a repeating key of length p on the table, two known letters whose landing places differ by a multiple of p use the same key letter, so they must force the same one.
7. Do this for every reading and width of the three grids, the key before or after, and on scrambled copies.

## Worked example (generated)

```
three matrix stages: rows of 30 read down the columns, left first; rows of 9 read up, right first; rows of 41 read up, left first

place  letter  after 1  after 2  after 3  copper there
   22       E       71       13       39             Q
   23       A       74       78       88             U
   24       S       77       45       11             U
   64       B       15       41       97             R
   65       E       19       95       37             W
   74       K       49       59       50             A

with a key of length p on the table, known letters whose final places differ by a multiple of p share a key letter
```

## Lineage

Inherits from 0134-mixed-matrix-readings-two-and-three-stages. What changed: F6.3b. 0134 enumerated every triple of the four column readings at widths 2-24 and every pair at 2-96; triples with any width from 25 to 96 rested on 0037's sample of 200,000. Here they are enumerated exactly: 63 reading triples (all-clockwise is 0083) x every width triple in 2-96 with at least one width of 25 or more, forward and inverse, deduplicated within each first stage. The count (about 95 million distinct routes on 11 texts) does not fit Python in 30 minutes, so the inner loop is compiled C, written out and compiled by this file and checked inside the run against a Python reference on random routes.

## Hypothesis (domain expert)

C1(a) (Sanborn, CNN 2005, knowledge/sources/cnn-2005-sanborn-interview-transcript.txt: 'you write a line of plain text out, right, in successive rows. And then basically you write it going from top to bottom... sometimes I used double matrixes and triple matrixes... and then went back to this table'), C2(a), C11. Stage: write the 97 symbols in rows of w (last row short) and read the columns one of four ways: cw (left column first, bottom up: the K3 turn), ccw (right first, top down), col (left first, top down: Sanborn's description), colr (right first, bottom up). Three stages, widths w1, w2, w3 in 2-96, at least one >= 25 (0134 did all <= 24), 63 reading triples; the composed permutation and its inverse. Key: periodic tableau 1-26 after (order A, slot = landing place mod p) or before (order B, slot = message place mod p), 8 classes (plain and cipher alphabets standard or KRYPTOS, Beaufort or not); a period is live if no slot holds two different forced key letters. Exact. Ten scrambled coppers (seed 133, as 0134); statistic fixed before the run: cells (order, period) where K4's live count is above every copper's, against the same count for each copper against the rest.

## Prediction

As in 0134 and 0083: no key shorter than 20 fits K4 after any route in either order beyond what the coppers show, and K4 is above every copper in no more cells than the most any copper manages against the rest. A K4 count outside that null stops the queue for a replication. Zero candidates.

## Method

1. Build the where-map of one stage for every width 2-96 and reading.
2. Compile the C counter; check it against a Python reference on 25 random routes (every order, period, class and text).
3. For each first stage (reading, width), compose every second and third stage with at least one width >= 25, skip all-clockwise, forward and inverse; skip permutations already seen within that first stage.
4. For each route, class and text: the forced key letter at each known letter's slot; period p live if no slot holds two different letters; count per (order, period, text); list K4's settings live below 20.
5. Compare K4 with the ten coppers cell by cell.

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
 "family": "three matrix stages (rows of w, columns read in one of four ways), at least one width 25-96, then or before a periodic tableau key",
 "readings": {
  "cw": "left column first, bottom up",
  "ccw": "right first, top down",
  "col": "left first, top down",
  "colr": "right first, bottom up"
 },
 "triples": "63 reading triples (all-cw skipped, 0083) x width triples in 2-96 with max >= 25 (all <= 24 was 0134), forward and inverse",
 "first_stages_done": 380,
 "first_stages_total": 380,
 "distinct_routes": 105548253,
 "duplicates_skipped_within_first_stage": 947955,
 "periods": [
  1,
  26
 ],
 "classes": 8,
 "c_counter_checked_against_python": "25 random routes x 2 orders x 11 texts, all equal",
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
   1,
   4,
   6,
   271,
   18849,
   79056,
   668223,
   1648543,
   10713606
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
   57,
   49207,
   32652378
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
   6,
   154,
   7076,
   66983,
   526528,
   1642918,
   10647843
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
   44,
   45550,
   32345993
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
   6,
   112,
   767,
   57730,
   87199,
   701115,
   1662253,
   10709335
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
   1,
   0,
   0,
   0,
   0,
   1,
   93,
   49068,
   32661842
  ]
 },
 "k4_shortest_live": {
  "A": 18,
  "B": 24
 },
 "coppers_shortest_live": {
  "A": 19,
  "B": 17
 },
 "k4_settings_live_below_20": {
  "A": 5,
  "B": 0
 },
 "controls_settings_live_below_20": {
  "A": [
   0,
   0,
   2,
   6,
   0,
   1,
   0,
   2,
   3,
   0
  ],
  "B": [
   0,
   1,
   0,
   1,
   1,
   0,
   0,
   0,
   0,
   0
  ]
 },
 "k4_live_below_20": [
  {
   "route": [
    "col",
    93,
    "cw",
    65,
    "cw",
    84
   ],
   "dir": "fwd",
   "order": "A",
   "class": "kry/kry/beau",
   "period": 18
  },
  {
   "route": [
    "ccw",
    38,
    "cw",
    93,
    "col",
    31
   ],
   "dir": "fwd",
   "order": "A",
   "class": "std/std/beau",
   "period": 19
  },
  {
   "route": [
    "ccw",
    38,
    "col",
    93,
    "col",
    31
   ],
   "dir": "fwd",
   "order": "A",
   "class": "std/std/beau",
   "period": 19
  },
  {
   "route": [
    "colr",
    39,
    "cw",
    96,
    "col",
    31
   ],
   "dir": "fwd",
   "order": "A",
   "class": "std/std/beau",
   "period": 19
  },
  {
   "route": [
    "colr",
    39,
    "col",
    96,
    "col",
    31
   ],
   "dir": "fwd",
   "order": "A",
   "class": "std/std/beau",
   "period": 19
  }
 ],
 "cells_k4_above_every_copper": [
  [
   "A",
   18
  ],
  [
   "A",
   26
  ],
  [
   "B",
   25
  ]
 ],
 "null_cells_above_rest_per_copper": [
  0,
  2,
  2,
  3,
  1,
  0,
  1,
  0,
  0,
  2
 ],
 "stop_queue": false,
 "controls": "10 shuffled coppers (seed 133, as 0134), identical search",
 "order_A": "stages, then key (slot = landing place mod p)",
 "order_B": "key, then stages (slot = message place mod p)"
}
```

Notes: 105,548,253 distinct routes (380 of 380 first stages) x 8 classes x 2 orders, periods 1-26. Shortest live key on K4: A 18, B 24; coppers A 19, B 17. K4 settings live below 20: A 5, B 0. K4 above every copper in 3 of 52 cells; null 0-3. Stop queue: False.


