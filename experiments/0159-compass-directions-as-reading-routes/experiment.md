# 0159-compass-directions-as-reading-routes: F6.5: the message written in rows and read off along a compass direction (each of the 16 points, and east then east-northeast or northeast in two stages), then or before a repeating key on the table

**Family:** 6-transposition-then-tableau  
**Parent:** 0134-mixed-matrix-readings-two-and-three-stages  
**Decision:** reverted  
**Run:** 2026-10-16T22:31:22+00:00, 14.7 s, status ran  
**Time by phase:** unattributed 20 s, run 15 s, record 0 s

## In plain words

The two clue words are directions: east, northeast. Perhaps they also say how the letters were moved: write the message in rows, then copy it out travelling east-northeast across the grid, or any other compass direction. We try every compass direction, every row width, and two-step versions (east, then northeast), each followed or preceded by a repeating secret word on the sculpture's tables, and check them against the 24 known letters and scrambled copies of the carved text.

## Walkthrough, by hand

1. Write the 97 letters in rows of 10.
2. Travel east-northeast: one row up, two columns right. Every line of cells in that direction is read from its lower-left end.
3. Take the lines in order, starting from the top-left corner, and copy each out: that is the moved text.
4. Note where each of the 24 known letters lands and the carved letter there.
5. With a key of length p on the table, two known letters landing a multiple of p apart must force the same key letter.
6. Repeat for every direction, width and order, the key before or after, and on scrambled copies.

## Worked example (generated)

```
rows of 10, read east-northeast (one row up, two columns right), lines from the top-left corner

first 20 message places read: 1 2 11 3 12 4 21 13 5 22 14 6 31 23 15 7 32 24 16 8

place  letter  lands at  copper there
   22       E        10             H
   23       A        14             S
   24       S        18             F
   64       B        57             I
   65       E        63             B
   74       K        67             V
```

## Lineage

Inherits from 0134-mixed-matrix-readings-two-and-three-stages. What changed: F6.5 (added 2026-10-16, A14(a)). The known words are directions; read as instructions (C16(c)), they could name the route by which the grid is copied out. Routes: the 97 letters written in rows of w (2-96), read along lines parallel to one of the 16 compass points (the eight half-points as steps of one row and two columns), lines taken in either order; and two such stages in sequence for every ordered pair of E, ENE and NE at widths 2-48 ('east, then northeast'). Forward and inverse. Then a periodic key 1-26 on the standard or KRYPTOS tables in either order, decided exactly as 0134, against ten scrambled coppers.

## Hypothesis (domain expert)

C16(c) ('The final passage will lead in several directions. The word directions is, I use intentionally', 2010, knowledge/sources/nyt-2010-berlin-clue.txt), C1(a) (rows written, columns read: the matrix code, knowledge/sources/cnn-2005-sanborn-interview-transcript.txt), C3(a) (spatial systems). Route: cell (r, c) holds message place r w + c; direction (dr, dc) in {N (-1,0), NNE (-2,1), NE (-1,1), ENE (-1,2), E (0,1), ESE (1,2), SE (1,1), SSE (2,1), S, SSW, SW, WSW, W, WNW, NW, NNW (negatives)}; lines are the classes of dc r - dr c, read in increasing projection dr r + dc c, lines in increasing or decreasing class. Singles: 16 x 2 x widths 2-96. Doubles: (E, ENE, NE)^2 ordered x line orders x widths 2-48 each. Forward and inverse, duplicates removed. Key: periodic tableau 1-26 after (A) or before (B), 8 classes; a period is live if no slot holds two different forced letters. Statistic fixed before the run (0134's): cells where K4's live count is above every copper's, against each copper's count against the rest.

## Prediction

As in 0134: nothing live below key length 20 beyond the coppers' rate; K4 above every copper in no more cells than the most any copper manages against the rest. Zero candidates.

## Method

1. Build every route: singles and doubles as stated, forward and inverse; remove duplicates.
2. For each route, class and text, the key letter each known letter forces at its slot (order A: landing place mod p; order B: message place mod p).
3. Count live periods 1-26 per order on K4 and ten coppers; list K4's settings live below 20.
4. Compare cell by cell with the fixed statistic.

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
 "family": "compass-direction reading routes (16 points, either line order, widths 2-96; E/ENE/NE pairs at widths 2-48), then or before a periodic tableau key",
 "directions": {
  "N": [
   -1,
   0
  ],
  "NNE": [
   -2,
   1
  ],
  "NE": [
   -1,
   1
  ],
  "ENE": [
   -1,
   2
  ],
  "E": [
   0,
   1
  ],
  "ESE": [
   1,
   2
  ],
  "SE": [
   1,
   1
  ],
  "SSE": [
   2,
   1
  ],
  "S": [
   1,
   0
  ],
  "SSW": [
   2,
   -1
  ],
  "SW": [
   1,
   -1
  ],
  "WSW": [
   1,
   -2
  ],
  "W": [
   0,
   -1
  ],
  "WNW": [
   -1,
   -2
  ],
  "NW": [
   -1,
   -1
  ],
  "NNW": [
   -2,
   -1
  ]
 },
 "distinct_routes": 110820,
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
   3,
   13,
   200,
   1215,
   4549,
   12668
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
   44,
   34169
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
   10,
   186,
   760,
   4531,
   12534
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
   38,
   33556
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
   2,
   40,
   227,
   1523,
   4585,
   12729
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
   59,
   34913
  ]
 },
 "k4_shortest_live": {
  "A": 21,
  "B": 25
 },
 "coppers_shortest_live": {
  "A": 21,
  "B": 25
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
 "cells_k4_above_every_copper": [
  [
   "A",
   21
  ]
 ],
 "null_cells_above_rest_per_copper": [
  1,
  1,
  0,
  1,
  0,
  1,
  0,
  1,
  1,
  0
 ],
 "stop_queue": false,
 "controls": "10 shuffled coppers (seed 1365), identical search",
 "exhaustive": true
}
```

Notes: 110,820 distinct routes x 8 classes x 2 orders, periods 1-26. Shortest live on K4: A 21, B 25; coppers A 21, B 25. K4 settings live below 20: A 0, B 0. K4 above every copper in 1 of 52 cells; null 0-1. Stop queue: False.


