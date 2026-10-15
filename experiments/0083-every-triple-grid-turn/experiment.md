# 0083-every-triple-grid-turn: Three grid turns in a row at every width, then (or before) a repeating key: the triple matrix, exhaustively

**Family:** 6-transposition-then-tableau  
**Parent:** 0037-triple-matrix-routes-sampled-then-tableau  
**Decision:** reverted  
**Run:** 2026-10-15T15:45:20+00:00, 757.8 s, status ran  
**Time by phase:** design 0 s, implement 25 s, test 0 s, run 758 s, record 0 s

## In plain words

Sanborn said he 'sometimes used double matrixes and triple matrixes' and then went back to the table. The third message was made by writing the letters in a grid and turning it; doing that twice gives the NSA's reading of it. Three times has never been tried in full. We turn the grid three times, at every possible width each time, and then ask whether a repeating secret word of up to 26 letters on the table could give the copper's known letters, with the word applied either after the turns or before them.

## Walkthrough, by hand

1. Write the message in rows of 7 and turn the grid a quarter clockwise: read each column from the bottom up, left column first. The E at place 22 comes out at place 11.
2. Write the result in rows of 9 and turn again: place 11 is in row 1, column 1; column 0 gives 11 letters and column 1 read from the bottom reaches row 1 at its tenth letter, so the E is now at 21.
3. Rows of 13, turn a third time: the E lands at 61, where the copper has N.
4. A repeating key on the table after the turns must turn E into N at place 61; work out that key letter for all 24 known letters.
5. For a key of length p, two known letters whose landing places differ by a multiple of p share a key letter; if they need different ones, p is dead.
6. Repeat for every width triple, both directions, the key before or after the turns, and on ten scrambled coppers.

## Worked example (generated)

```
three clockwise quarter turns at widths 7, 9, 13: where the first known letters go

place  letter  after 7  after 9  after 13  copper there
   22       E       11       21        61             N
   23       A       25       75        71             Z
   24       S       39       29        22             F
   64       B        5       55        20             B
   65       E       19        9        69             T
```

## Lineage

Inherits from 0037-triple-matrix-routes-sampled-then-tableau. What changed: 0037 sampled 200,000 of about 9.4 million triples of stages up to width 30 and scored the forced key as English. Here the triple is K3's own move, a quarter turn, three times, at every width from 2 to 96 in each grid: all 857,375 width triples, forward and inverse, with the exact crib test for a repeating key of length 1-26 on either side of the move.

## Hypothesis (domain expert)

Type 1 of directions.md, gap a4 of the prior-work database ('exhaustive triple rotation + tableau: every public search stops at two stages; 0037 only sampled'). Clue C1(a) (02-sanborn-said.md, CNN 2005: 'sometimes I used double matrixes and triple matrixes... and then went back to this table to do the ultimate') read literally: three quarter turns, the K3 move (C2(a); the NSA's double rotation for K3), then the tableau. A turn writes the text in rows of w (ragged last row) and reads columns bottom-up, left column first. Routes: turn(w3) . turn(w2) . turn(w1), w1, w2, w3 = 2-96 each (857,375), forward and inverse, deduplicated by a hash of the permutation. Key: periodic tableau key of period 1-26 after the move (slot = landing place mod p, order A) or before it (slot = place mod p, order B), 8 distinct classes of plain and cipher alphabet and Beaufort-or-not; a period is live if no two known letters in one slot force different key letters. Exact; ten shuffled coppers through the identical search. Left open: triples mixing turns with columnar or keyed stages beyond 0037's sample; anticlockwise turns; keys longer than 26.

## Prediction

As for one and two turns (0008) and the sample of triples (0037, smallest live period 20 once, otherwise 23 and up): no period below 20 is live on K4 beyond the rate on the shuffled coppers, and the count of live settings at each period 1-26 lies inside the control range, give or take the spread at 25-26. Zero candidates.

## Method

1. Compute the quarter-turn permutation once for every width 2-96.
2. Compose every triple, forward and inverse, and skip repeats.
3. For each route, class and text, compute the key letter each known letter forces at its landing place.
4. For each period 1-26 and each order, the period is live if no slot holds two different forced letters.
5. Count live settings per period on K4 and on ten shuffled coppers.
6. List K4's live settings below period 20.

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
 "family": "three clockwise quarter turns at widths 2-96 each, then or before a periodic tableau key",
 "width_triples": 857375,
 "distinct_routes": 1714024,
 "duplicates_skipped": 726,
 "stopped_at": null,
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
   1,
   0,
   0,
   9,
   609,
   1023,
   8725,
   27718,
   146182
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
   752,
   531231
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
   92,
   850,
   5464,
   27723,
   145430
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
   667,
   523761
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
   27,
   685,
   1177,
   10773,
   28201,
   150315
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
   2,
   849,
   533150
  ]
 },
 "k4_smallest_live_period_histogram": {
  "A": {
   "0": 13539143,
   "18": 1,
   "21": 9,
   "22": 609,
   "23": 1023,
   "24": 8712,
   "25": 26857,
   "26": 135838
  },
  "B": {
   "0": 13180232,
   "25": 752,
   "26": 531208
  }
 },
 "periods_outside_control_range": {
  "A": [
   18,
   25
  ],
  "B": []
 },
 "k4_live_below_20": [
  {
   "widths": [
    93,
    65,
    84
   ],
   "dir": "fwd",
   "order": "A",
   "class": "kry/kry/beau",
   "period": 18
  }
 ],
 "n_k4_live_below_20": 1,
 "controls_live_below_20": {
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
 "controls": "10 shuffled coppers (seed 83), identical search",
 "order_A": "turns, then key (slot = landing place mod p)",
 "order_B": "key, then turns (slot = place mod p)"
}
```

Notes: 1,714,024 distinct triple-turn routes (726 repeats skipped) x 8 classes x 2 orders, periods 1-26. K4 live below period 20: 1; controls: {'A': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'B': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}. Periods where K4 is outside the control range: {'A': [18, 25], 'B': []}.


