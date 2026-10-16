# 0134-mixed-matrix-readings-two-and-three-stages: Two and three matrix stages in mixed readings (turn either way, Sanborn's rows-then-columns-down, and its reverse), then or before a repeating key on the table

**Family:** 6-transposition-then-tableau  
**Parent:** 0083-every-triple-grid-turn  
**Decision:** reverted  
**Run:** 2026-10-16T11:52:58+00:00, 275.2 s, status ran  
**Time by phase:** design 0 s, test 1 s, run 275 s, record 0 s

## In plain words

Sanborn described his 'matrix codes': write the message in rows on paper, then copy it out going down the columns; and he said he sometimes did this two or three times before using the table. There are four natural ways to copy out the columns (left or right column first, going down or up). We try every combination of two such steps at every grid width, and of three steps at widths up to 24, each followed or preceded by a repeating secret word on the sculpture's tables, and check them against the 24 known letters and against scrambled copies of the carved text.

## Walkthrough, by hand

1. Write the message in rows of 7 on squared paper.
2. Copy it out column by column, left column first, top to bottom (Sanborn's matrix code).
3. Write that result in rows of 9 and copy it out right column first, bottom to top.
4. Write that in rows of 5 and copy it out left column first, bottom to top (a quarter turn).
5. Note where each of the 24 known letters has landed and the carved letter there.
6. With a repeating key of length p on the table, each known letter forces one key letter in its slot (landing place mod p); two that share a slot must agree, or p is dead.
7. Repeat for every combination of readings and widths, the key before or after, and on scrambled copies.

## Worked example (generated)

```
three matrix stages: rows of 7 read down the columns left first; rows of 9 read up, right first; rows of 5 read up, left first

place  letter  after 1  after 2  after 3  copper there
   22       E        4       64       66             P
   23       A       18        9       77             D
   24       S       32       50       88             U
   64       B       10       96        1             O
   65       E       24       40       90             U
   74       K       53       15       95             C
```

## Lineage

Inherits from 0083-every-triple-grid-turn. What changed: F6.3 (mixed three-stage routes), exhaustive at small widths. 0083 closed three clockwise quarter turns at every width 2-96; 0099 two turns in mixed senses; 0037 only sampled mixed triples. Here each stage writes the text in rows of w (last row short) and reads the columns in one of four ways: left column first bottom-up (clockwise turn), right column first top-down (anticlockwise turn), left column first top-down (Sanborn's own description of a matrix code, plain columnar) or right column first bottom-up. Every ordered pair of readings at widths 2-96, and every ordered triple at widths 2-24 (the all-clockwise triples are 0083's and skipped), forward and inverse, then or before a periodic key 1-26 on the standard or KRYPTOS tables (8 classes).

## Hypothesis (domain expert)

C1(a) (Sanborn, CNN 2005, knowledge/sources/cnn-2005-sanborn-interview-transcript.txt: matrix codes are 'a very specific type of encoding system, in which you basically take a piece of paper, and you write a line of plain text out, right, in successive rows. And then basically you write it going from top to bottom instead of left to right... sometimes I used double matrixes and triple matrixes... and then went back to this table'), C2(a) (the K3 matrix and 'all the possible shifts'). Route space: stage(w, r) for w = 2-96 and r in {cw, ccw, col, colr}; doubles: 16 reading pairs x 95^2 widths; triples: 63 reading triples (all-cw excluded) x 23^3 widths 2-24; forward and inverse; duplicates removed within each worker's share (first stage), so a few cross-share duplicates count twice on K4 and coppers alike. Key: periodic tableau 1-26 after the move (slot = landing place, order A) or before (slot = message place, order B), plain and cipher alphabets standard or KRYPTOS, Vigenere/variant or Beaufort (8 distinct classes, as 0006 showed). A period is live if no two known letters in one slot force different key letters. Exact. Research note combined_methods_and_sevens.md: every public search stops at two stages. The research note's per-stage padding is F6.4, not here.

## Prediction

As for one, two and three clockwise turns (0008, 0083, 0099): nothing live below period 20 beyond the coppers' rate, and K4 above every copper in no more (order, period) cells than the most any single copper manages against the rest. A K4 count beyond that null stops the queue for a replication. Zero candidates.

## Method

1. Compute the where-map of every stage (width 2-96, four readings).
2. Compose every pair, and every triple at widths 2-24, forward and inverse; skip repeats.
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
 "family": "two or three matrix stages (rows of w, columns read in one of four ways), then or before a periodic tableau key",
 "readings": {
  "cw": "left column first, bottom up",
  "ccw": "right first, top down",
  "col": "left first, top down",
  "colr": "right first, bottom up"
 },
 "doubles": "16 reading pairs x widths 2-96 each",
 "triples": "63 reading triples (all-cw skipped, 0083) x widths 2-24 each",
 "first_stages_done": 380,
 "first_stages_total": 380,
 "distinct_routes": 1762597,
 "duplicates_skipped_within_share": 59245,
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
   1,
   7,
   165,
   682,
   10445,
   15940,
   112804
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
   781,
   545243
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
   1,
   35,
   616,
   8208,
   15850,
   111113
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
   744,
   540687
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
   1,
   13,
   687,
   787,
   10695,
   16115,
   112651
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
   0,
   3,
   855,
   545069
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
   1,
   0,
   0
  ]
 },
 "k4_live_below_20": [],
 "cells_k4_above_every_copper": [
  [
   "A",
   26
  ],
  [
   "B",
   26
  ]
 ],
 "null_cells_above_rest_per_copper": [
  0,
  2,
  1,
  1,
  1,
  0,
  0,
  2,
  0,
  1
 ],
 "stop_queue": false,
 "controls": "10 shuffled coppers (seed 133), identical search",
 "order_A": "stages, then key (slot = landing place mod p)",
 "order_B": "key, then stages (slot = message place mod p)"
}
```

Notes: 1,762,597 routes (380 of 380 first stages) x 8 classes x 2 orders, periods 1-26. K4 settings live below 20: 0 (A), 0 (B); coppers A 0-0, B 0-1. K4 above every copper in 2 of 52 cells; null 0-2. Stop queue: False.


