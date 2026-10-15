# 0082-where-the-blanks-go-in-the-grid: The grid by hand: blank cells at the top, or filler letters carried through the second turn, then a repeating key

**Family:** 6-transposition-then-tableau  
**Parent:** 0008-k3-formula-all-shifts-then-tableau  
**Decision:** reverted  
**Run:** 2026-10-15T15:41:08+00:00, 57.0 s, status ran  
**Time by phase:** design 65 s, implement 58 s, test 0 s, run 57 s, record 0 s

## In plain words

The third message was scrambled by writing it in a grid and turning the grid. Its 336 letters fill a 24 by 14 grid exactly. K4's 97 letters fill no grid, so someone working by hand has to leave some squares empty, or fill them with dummy letters. Computer searches so far always left the empty squares at the very end. A person might leave them at the start instead, or carry the dummy letters into a second grid and strike them out only at the end. Each choice moves the letters differently. We try them all, joined to a repeating secret word on the table, and see whether any lets a short word fit the 24 known letters.

## Walkthrough, by hand

1. Write the 97 places in rows of 10. Ten rows hold 100 cells, so 3 stay blank; put them at the start of the top row, so place 1 sits in column 3.
2. Turn the grid a quarter clockwise: read each column from the bottom up, left column first, skipping blanks. Columns 0-2 give 9 letters each and column 3 gives 10, so column 4 starts at letter 38.
3. Place 22 is in row 2, column 4, the eighth letter read from the bottom of that column: it lands at place 45. With the blanks at the end instead it would land at 18.
4. The repeating key letter at the landing place must turn E into the copper letter there; work out that key letter for all 24 known letters.
5. For a key of length p, two known letters whose landing places differ by a multiple of p use the same key letter; if they need different ones, p is dead.
6. Repeat for every width, blank placement, second turn, filler choice and order, and on ten scrambled coppers.

## Worked example (generated)

```
width 10, 97 letters: 10 rows, 3 blank cells at the start of the top row ('.' = blank, numbers = places)

 .  .  .  1  2  3  4  5  6  7
 8  9 10 11 12 13 14 15 16 17
18 19 20 21 22 23 24 25 26 27
 ...
88 89 90 91 92 93 94 95 96 97

one turn clockwise (columns bottom-up, left first): where the known letters land
place  letter  blanks on top  blanks at the end
   22       E             45                18
   23       A             55                28
   64       B             61                34
   65       E             71                44
```

## Lineage

Inherits from 0008-k3-formula-all-shifts-then-tableau. What changed: 97 letters never fill a grid, so a hand turn leaves blank cells. The coded searches (0008, keithadler, nitsuah) put them only at the end of the last row and drop them at once. Here the blanks sit at the start of the first row (the short row at the top), or the second grid is filled with the first grid's blank cells still in it as filler letters that are struck out only at the end, for one and two quarter turns at every width and for column shuffles, each joined to a repeating key on the table before or after the move.

## Hypothesis (domain expert)

Type 1 of directions.md, gap a1 of the prior-work database ('rotation with per-stage padding (nulls dropped between the two griddings), the short row at the top, or blanks in key-determined cells... all coded searches pad once, at the ends'). Clues C1(a) (02-sanborn-said.md, CNN 2005, 'double matrixes and triple matrixes'), C2(a) (the K3 matrix and its shifts; K3's 336 letters fill 24 x 14 and 8 x 42 exactly, K4's 97 fill nothing), C17(b) ('whether it's 97, whether it's 100... I seem to like to manipulate the information'). Grid of width w and h = ceil(n/w) rows; the h w - n blank cells are the first cells of the top row ('top') or the last of the bottom row ('bottom', the covered case). A quarter turn reads columns bottom-up, left first (cw) or top-down, right first (ccw). Two turns: the first grid's blank cells either vanish ('drop') or travel as filler letters into the second grid and are struck out at the end ('keep'). New routes: one turn cw or ccw with blanks on top, widths 2-96; two cw turns at every width pair 2-96 with blanks top or bottom in each grid and drop or keep (seven of the eight combinations; bottom-bottom-drop is 0008's); plain columnar (both directions) and vocabulary-keyed columnar with the short row on top; all forward and inverse, deduplicated. Key: a periodic tableau key of period 1-26 after the move (key slot = landing place mod p) or before it (slot = place mod p), 8 distinct classes of plain and cipher alphabet and Beaufort-or-not. A period is live if no two known letters in one slot force different key letters. Exact; ten shuffled coppers through the identical search.

## Prediction

No route, order and class has a live period below 20 on K4 beyond what the ten shuffled coppers show; the count of live settings at every period 1-26 lies inside the control range, give or take the spread at 25-26. Zero candidates.

## Method

1. Build every route: write the 97 places into the grid with the blanks on top or below, turn, and for two turns either drop the blanks or carry them as fillers into the second grid.
2. Keep one route per distinct reordering.
3. For each route, class and text, compute the key letter each known letter forces at its landing place.
4. For each period 1-26 and each order, the period is live if no slot holds two different forced letters.
5. Count live settings per period on K4 and on ten shuffled coppers.
6. List K4's live settings at periods below 20.

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
 "family": "hand-padded grid turns and short-row-on-top columnar, joined to a periodic tableau key before or after",
 "route_specs": 127234,
 "distinct_routes": 120871,
 "routes_done": 120871,
 "periods": [
  1,
  26
 ],
 "classes": 8,
 "planted_check": true,
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
   77,
   299,
   2166,
   6258,
   39016
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
   66,
   37449
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
   12,
   229,
   1289,
   6225,
   38688
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
   41,
   36529
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
   4,
   151,
   283,
   2160,
   6358,
   39032
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
   67,
   38390
  ]
 },
 "k4_smallest_live_period_histogram": {
  "A": {
   "0": 924839,
   "22": 77,
   "23": 299,
   "24": 2164,
   "25": 5834,
   "26": 33755
  },
  "B": {
   "0": 929455,
   "25": 66,
   "26": 37447
  }
 },
 "periods_outside_control_range": {
  "A": [
   23,
   24
  ],
  "B": []
 },
 "k4_live_below_20": [],
 "n_k4_live_below_20": 0,
 "controls_live_below_20": [
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
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
 "controls": "10 shuffled coppers (seed 82), identical search",
 "order_A": "move, then key (slot = landing place mod p)",
 "order_B": "key, then move (slot = place mod p)"
}
```

Notes: 120,871 distinct routes from 127,234 specs x 8 classes x 2 orders, periods 1-26. K4 live settings below period 20: 0; per control (A then B): [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]. Periods where K4 is outside the control range: {'A': [23, 24], 'B': []}. Planted text found: True.


