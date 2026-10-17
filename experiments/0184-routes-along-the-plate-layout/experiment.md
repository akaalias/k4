# 0184-routes-along-the-plate-layout: F4.1: routes that follow the copper's physical layout (K4's four lines starting after K3's tail and the ?, the lower plate, the whole left side), then or before a repeating key: exact

**Family:** 4-sanborn-visual  
**Parent:** 0092-grid-paths-then-tableau  
**Decision:** reverted  
**Run:** 2026-10-17T00:33:39+00:00, 1.4 s, status ran  
**Time by phase:** design 0 s, implement 0 s, test 0 s, run 1 s, record 0 s

## In plain words

On the copper, K4 starts near the end of a line, right after K3 and a question mark, and runs on for three full lines. If Sanborn wrote his message into that physical shape along some path, down the columns, back and forth, round in a spiral, the carved order would follow from it. We try every such path on the real layout, with a repeating secret word before or after, and compare with scrambled copies.

## Walkthrough, by hand

1. Draw K4 on the copper: OBKR at the end of a line, then three lines of 31.
2. Read its cells down the columns, left to right: column 1 gives the 2nd, 3rd and 4th lines' first letters, and so on; the column under O, B, K, R has four letters.
3. That order says where each message letter was carved.
4. Undo it and test every repeating key length 1-26 on the sculpture's tables against the 24 known letters.
5. Same for every route and grid, and on scrambled copies.

## Worked example (generated)

```
K4's cells read down the columns from the top left: UTVOWTXTTOQMGSZHJFUQPLSKBSWSEGOKDLZKIZZFWXBATBTJWJCFKDLLIRUGVDKQIUQAHPWURIANNUGFEOKBKBSNCKSYAROPR
```

## Lineage

Inherits from 0092-grid-paths-then-tableau. What changed: F4.1. 0092 tested grid paths on rectangles of chosen widths with K4 starting at a corner. On the copper, K4 does not start at a corner: it occupies the last four 31-character lines of the lower-left plate, its first row holding only OBKR at columns 28-31 after K3's last letters and the ?. The plates' lines are ragged (29-33 characters; transcript in knowledge/01-facts.md). Routes are built on three physical grids: K4's own four lines, the lower plate's 14 lines, and the left side's 28 lines; for each, rows or columns from each corner, straight or back and forth, diagonals both ways, and spirals both ways; K4's letters are taken in the order a route visits K4's cells. Each route and its inverse, then (A) or before (B) a repeating key 1-26 on 8 table classes (F6's compiled tester); K4 against 15 shuffled copies.

## Hypothesis (domain expert)

C3 (Sanborn's sculptural, visual habits), C1 ('matrix codes'), F4 ('Sanborn's visual systems'); the 31-letter lines as a grid (knowledge/04-structure.md). Model: message written along a route over the plate's cells, carved row by row (or the reverse), with a periodic tableau key before or after. Statistic: 0134's fixed statistic (cells (order, period) where K4 is live in more routes than every copy, against each copy's count against the rest), and the shortest live period.

## Prediction

No route gives K4 a live period below the copies'; the cells where K4 leads stay inside the copies' range. Zero candidates.

## Method

1. Lay out the 28 lines of the left side from the transcript; K4's cells are the last 97.
2. For each grid (K4's lines, lower plate, whole side) and route: the order in which K4's cells are visited.
3. Each route as a where-map and its inverse, deduplicated.
4. F6's compiled tester: live (order, period) settings per text; K4 against 15 shuffled copies.

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
 "family": "routes over the copper's physical layout (K4's lines, lower plate, whole left side), then/before a periodic key 1-26, 8 classes, exact",
 "routes_per_grid": {
  "K4's four lines": 40,
  "lower plate": 40,
  "whole left side": 40
 },
 "maps_after_dedupe": 73,
 "routes": 73,
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
   0,
   0,
   1,
   0,
   0,
   13
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
   0,
   18
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
   0,
   0,
   0,
   0,
   8
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
   0,
   12
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
   0,
   0,
   1,
   5,
   8,
   1,
   17
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
   0,
   36
  ]
 },
 "k4_shortest_live": {
  "A": 23,
  "B": 26
 },
 "coppers_shortest_live": {
  "A": 22,
  "B": 26
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
  0,
  1,
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
  1,
  1,
  0
 ],
 "stop_queue": false,
 "copies": "15 shuffled copies (seed 1840)",
 "seconds": 1,
 "exhaustive": true
}
```

Notes: 73 routes; shortest live K4 A 23 B 26 (copies 22, 26); K4 above every copy in 0 of 52 cells (copies 0-1)


