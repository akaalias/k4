# 0099-two-turns-in-mixed-directions: Two quarter turns in mixed directions (clockwise then anticlockwise, and the reverse), with a repeating key

**Family:** 6-transposition-then-tableau  
**Parent:** 0083-every-triple-grid-turn  
**Decision:** reverted  
**Run:** 2026-10-15T20:06:21+00:00, 24.0 s, status ran  
**Time by phase:** unattributed 18 s, run 24 s, record 0 s

## In plain words

K3 was made by writing the message in a grid, turning the grid a quarter turn, writing it out, and doing that again with a grid of another width. Experiments 80 and 83 always turned the same way. Here the two turns go in opposite directions, or both the other way, at every pair of widths, followed or preceded by a short repeating secret word, and each combination is checked against the 24 known letters.

## Walkthrough, by hand

1. Write the 97 letters in rows of 9; read the columns bottom to top, left column first (a clockwise quarter turn).
2. Write the result in rows of 12; read the columns top to bottom, right column first (an anticlockwise quarter turn).
3. Each known letter, say E at place 22, now sits at a new place j.
4. With a key of length p after the move, its key letter is slot j mod p and must turn E into the carved letter at j; letters sharing a slot must agree.
5. Repeat for every pair of widths, the three mixed senses, key lengths 1-26 and table rules, and with the key before the move.

## Worked example (generated)

```
clockwise turn in rows of 9, then anticlockwise in rows of 12: where the first known letters go

place  letter  after cw 9  after ccw 12  copper there
   22       E          42           52             J
   23       A          53           61             N
   24       S          64           70             M
   25       T          75           79             Z
   64       B           4           65             Y
```

## Lineage

Inherits from 0083-every-triple-grid-turn. What changed: 0080-0083 composed quarter turns in one direction only (clockwise, twice or three times). K3's rotations and Sanborn's 'double matrixes' do not fix the sense of each turn. Here every pair of widths 2-96 is turned clockwise then anticlockwise, anticlockwise then clockwise, and anticlockwise twice, forward and inverse, deduplicated against each other and against the clockwise pairs already tested, with a repeating key of length 1-26 before or after.

## Hypothesis (domain expert)

Type 1 of directions.md, closing a gap in 0080 and 0083: the two-turn library held only clockwise-clockwise pairs. Sanborn: 'double matrixes and triple matrixes... then went back to this table' (C1); K3 is two rotations of 14 x 24 and 8 x 42 grids (01-facts.md; the Stehle formula). A turn on a ragged grid is not the reverse of the other turn, so mixed senses give new routes. Routes: turn(w1, d1) then turn(w2, d2), (d1, d2) in {(cw, ccw), (ccw, cw), (ccw, ccw)}, w1, w2 = 2-96, forward and inverse, minus repeats and minus the cw-cw set. Key: periodic 1-26 after the move (slot = carved place mod p) or before it, 8 tableau classes, exact by slot agreement; the excess check counts distinct check sets (the lesson of 0086 and 0092). Ten shuffled coppers.

## Prediction

Nothing consistent below period 20; at every period the number of distinct consistent check sets on K4 lies inside the ten coppers' range, give or take one period. Zero candidates.

## Method

1. Build the clockwise-pair set of 0080 to skip.
2. For each sense pair and widths, compose the two turns and its inverse; drop repeats.
3. For each route and class, compute the key values at the known letters and test periods 1-26 in both orders.
4. Count settings and distinct check sets per period on K4 and ten shuffled coppers.
5. List K4's settings below period 20.

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
 "family": "two quarter turns in mixed senses at widths 2-96, then or before a periodic tableau key",
 "sense_pairs": [
  "cw-ccw",
  "ccw-cw",
  "ccw-ccw"
 ],
 "cw_cw_routes_skipped": 18040,
 "distinct_routes": 53743,
 "duplicates_skipped": 407,
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
   0,
   16,
   107,
   1058,
   3022,
   19061
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
   29,
   16291
  ]
 },
 "controls_live_min": {
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
   4,
   85,
   748,
   2986,
   18714
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
   14,
   15945
  ]
 },
 "controls_live_max": {
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
   3,
   2,
   82,
   119,
   1084,
   3073,
   19167
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
   44,
   17091
  ]
 },
 "k4_distinct_check_sets_by_period_to_24": {
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
   6,
   36,
   89
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
   0
  ]
 },
 "controls_distinct_min": {
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
   3,
   30,
   86
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
   0
  ]
 },
 "controls_distinct_max": {
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
   2,
   11,
   51,
   109
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
   1
  ]
 },
 "periods_outside_by_settings": {
  "A": [],
  "B": []
 },
 "periods_outside_by_distinct_check_sets": {
  "A": [],
  "B": []
 },
 "k4_live_below_20": [],
 "n_k4_live_below_20": 0,
 "controls": "10 shuffled coppers (seed 99), identical search"
}
```

Notes: 53,743 new mixed-sense two-turn routes (407 repeats and cw-cw routes skipped) x 8 classes x 2 orders, periods 1-26. K4 live below 20: 0. Outside the control range by settings: {'A': [], 'B': []}; by distinct check sets (periods up to 24): {'A': [], 'B': []}.


