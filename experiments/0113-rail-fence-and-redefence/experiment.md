# 0113-rail-fence-and-redefence: The rail fence and the redefence (rails read in any order), with a repeating key before or after

**Family:** 6-transposition-then-tableau  
**Parent:** 0092-plaintext-written-along-a-path  
**Decision:** reverted  
**Run:** 2026-10-15T20:43:06+00:00, 6.0 s, status ran  
**Time by phase:** unattributed 74 s, run 6 s, record 0 s

## In plain words

The rail fence is a schoolbook way to scramble letters: write the message in a zigzag down and up over a few lines, like a fence, then read each line in turn. Here we try every number of lines up to 48, every starting point of the zigzag, and for up to six lines every order of reading them, with a short repeating secret word on the table before or after, against the 24 known letters.

## Walkthrough, by hand

1. Write the message on 3 rails: letter 1 on rail 1, 2 on rail 2, 3 on rail 3, 4 on rail 2, 5 on rail 1, and so on.
2. Read rail 1 left to right, then rail 2, then rail
3. 3. Each known letter lands at a new place; with a key of length p after the move, letters sharing a slot must agree.
4. Repeat for every rail count, start, rail order, key length and rule, and with the key before the move.

## Worked example (generated)

```
rail fence of 3 rails from the top: rails 1 2 3 2 1 2 3 ..., read rail 1, then 2, then 3

place  letter  rail  lands at  copper there
   22       E     2        36             T
   23       A     3        79             Z
   24       S     2        37             W
   25       T     1         7             X
   64       B     2        57             I
```

## Lineage

Inherits from 0092-plaintext-written-along-a-path. What changed: The rail fence, writing the message in a zigzag over r rails and reading rail by rail, is the oldest hand transposition and is in none of the route sets so far. Here every rail count 2-48 and every start phase, with the rails read top to bottom, bottom to top, or (up to 6 rails) in every order (the redefence), forward and inverse, with a repeating key of length 1-26 after or before.

## Hypothesis (domain expert)

Type 1 and type 4 (a hand route as the masking step, C4; 'double matrixes', C1). Routes: zigzag over r = 2-48 rails, start phase 0 to 2r-3 (the first letter on any rail, going down or up), rails read in order or reversed, and for r <= 6 in all r! orders (redefence); forward and inverse, deduplicated. Key: periodic 1-26 after the move (slot = carved place mod p) or before it, 8 tableau classes, exact by slot agreement. Ten shuffled coppers.

## Prediction

Nothing consistent below period 20; counts inside the coppers' range, give or take one period. Zero candidates.

## Method

1. Build every rail setting and its move; drop repeats.
2. Test periods 1-26 in both orders and 8 classes by slot agreement.
3. Count per period on K4 and ten shuffled coppers.

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
 "family": "rail fence (any start phase) and redefence (rails in any order up to 6 rails), then or before a periodic tableau key",
 "rail_settings": 12784,
 "distinct_routes": 12784,
 "duplicates_skipped": 12784,
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
   2,
   20,
   136,
   220,
   2181
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
   5,
   3739
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
   1,
   0,
   54,
   215,
   2177
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
   3694
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
   9,
   24,
   149,
   284,
   2215
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
   4163
  ]
 },
 "periods_outside_control_range": {
  "A": [],
  "B": []
 },
 "k4_live_below_20": [],
 "n_k4_live_below_20": 0,
 "controls": "10 shuffled coppers (seed 113), identical search"
}
```

Notes: 12,784 rail settings, 12,784 distinct routes x 8 classes x 2 orders, periods 1-26. K4 live below 20: 0. Outside the control range: {'A': [], 'B': []}.


