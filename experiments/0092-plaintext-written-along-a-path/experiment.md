# 0092-plaintext-written-along-a-path: The message written into a grid along one path and read out along another (snake, spiral, diagonal), with a repeating key before or after

**Family:** 2-masked-plaintext  
**Parent:** 0023-masks-reversal-and-nulls-then-tableau  
**Decision:** reverted  
**Run:** 2026-10-15T19:15:29+00:00, 19.7 s, status ran  
**Time by phase:** unattributed 202 s, run 20 s, record 0 s

## In plain words

One way to hide the shape of English is to write the message into a grid in an odd order, snaking back and forth, spiralling in from a corner, or along the diagonals, and then copy it out in another order. After that the letters go through the table with a short secret word. We try 30 such paths for writing and 30 for reading at every grid width, with secret words of up to 26 letters, and check each against the 24 known letters.

## Walkthrough, by hand

1. Write the message into rows of 10 letters, snaking: row 1 left to right, row 2 right to left, and so on.
2. Read it out by columns, top to bottom.
3. Each known letter, say E at place 22, now sits at a new place j.
4. With a secret word of length p after the move, the key letter at j is letter j mod p of the word; it must turn E into the carved letter at j.
5. Known letters landing on the same key letter must agree.
6. Repeat for every pair of paths, width, word length up to 26 and table rule, and with the key used before the move.

## Worked example (generated)

```
write in snake rows of 10, read by columns: where the first known letters land

place  letter  grid cell (row, col)  lands at  copper there
   22       E                (3, 2)        13             B
   23       A                (3, 3)        23             L
   24       S                (3, 4)        33             S
   25       T                (3, 5)        43             S
   64       B                (7, 4)        37             W
```

## Lineage

Inherits from 0023-masks-reversal-and-nulls-then-tableau. What changed: 0023, 0057 and 0074 masked the message without moving letters across a grid. 0080-0083 moved them by K3's rule, quarter turns and column reading only. Here the message is written into a grid of width 2-96 along one of 30 hand paths (rows, snake rows, columns, snake columns, spirals from each corner either way, diagonals, snake diagonals, each forwards or backwards) and read out along another, 900 path pairs per width.

## Hypothesis (domain expert)

Type 4 of directions.md, open item 'plaintext written in boustrophedon, spiral or columns'. Scheidt: he 'masked the English language' before the keyed step (C2, C3); Sanborn: 'double matrixes... then went back to this table' (C1), visual systems (family 4). Grid of width w = 2-96 filled to 97 cells in row order, the last row short; a path is an order of its cells: rows, snake rows, columns, snake columns, spirals inward from each corner clockwise or anticlockwise, anti-diagonals and snake anti-diagonals, main diagonals, and each of these reversed (30 paths). Route: write along path X, read along path Y, X != Y; deduplicated with inverses. Key: one repeating key, period 1-26, after the move (slot = carved place mod p) or before it (slot = message place mod p), 8 consistency classes of the tableau (plain and cipher alphabets standard or KRYPTOS, Beaufort or not). Exact by slot agreement; ten shuffled coppers set the chance level per period.

## Prediction

No route makes a repeating key of length 20 or less consistent; at every period the count of consistent (route, class) settings on K4 lies inside the range of the ten shuffled coppers, give or take one period by chance. Zero candidates.

## Method

1. For each width, build the grid's cells and the 30 paths.
2. For each pair of paths, compute where each message letter lands; drop repeats and inverses.
3. For each route and class, compute the key value forced at each known letter and test, for each period, whether known letters sharing a key slot agree, both orders.
4. Repeat on ten shuffled coppers.
5. List K4's settings consistent below period 20.

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
 "family": "write along one of 30 grid paths, read along another, widths 2-96, then or before a periodic tableau key",
 "paths": 30,
 "widths": [
  2,
  96
 ],
 "distinct_routes": 43579,
 "duplicates_skipped": 121721,
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
   1,
   47,
   405,
   2332,
   5695,
   22869
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
   9,
   14626
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
   233,
   2003,
   5660,
   20935
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
   7,
   12335
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
   34,
   32,
   339,
   2612,
   5959,
   23068
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
   61,
   15732
  ]
 },
 "periods_outside_control_range": {
  "A": [
   22,
   23
  ],
  "B": []
 },
 "k4_live_below_20": [],
 "n_k4_live_below_20": 0,
 "controls": "10 shuffled coppers (seed 92), identical search",
 "order_A": "move, then key (slot = carved place mod p)",
 "order_B": "key, then move (slot = message place mod p)"
}
```

Notes: 43,579 distinct path-pair routes (121,721 repeats skipped) x 8 classes x 2 orders, periods 1-26. K4 live below period 20: 0. Periods where K4 is outside the control range: {'A': [22, 23], 'B': []}.


