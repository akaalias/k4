# 0114-amsco-keyed-by-the-dictionary: AMSCO, a column shuffle with cells of one and two letters, keyed by any English word, with a repeating key

**Family:** 6-transposition-then-tableau  
**Parent:** 0110-keyword-columnar-from-the-whole-dictionary  
**Decision:** reverted  
**Run:** 2026-10-15T20:44:17+00:00, 401.7 s, status ran  
**Time by phase:** unattributed 66 s, run 402 s, record 0 s

## In plain words

AMSCO is a column shuffle in which the grid's boxes hold one letter, then two, then one, alternating, so some pairs of letters stay together when the columns are read out under a secret word. We try every dictionary word as the column word, with a short repeating secret word on the table before or after, against the 24 known letters.

## Walkthrough, by hand

1. Under SHADOW (6 columns), fill the first row with cells of 1, 2, 1, 2, 1, 2 letters, the second with 2, 1, 2, 1, 2, 1, and so on.
2. Read the columns in the order 3, 4, 2, 5, 1, 6, each column's cells top to bottom.
3. Each known letter lands at a new place; with a key of length p after the move, letters sharing a slot must agree.
4. Repeat for every word, first cell size, key length and rule, and with the key before the move.

## Worked example (generated)

```
AMSCO under SHADOW, first cell one letter: the first rows of cells (place numbers)

  1  2-3  4  5-6  7  8-9
  10-11  12  13-14  15  16-17  18
  19  20-21  22  23-24  25  26-27
  28-29  30  31-32  33  34-35  36

columns read in the order [3, 4, 2, 5, 1, 6]
place  letter  lands at  copper there
   22       E         4             R
   23       A        20             B
   24       S        21             W
   25       T        54             L
   64       B        77             D
```

## Lineage

Inherits from 0110-keyword-columnar-from-the-whole-dictionary. What changed: AMSCO (A. M. Scott, 1950s ACA) fills a keyed grid with cells that alternate one and two letters, then reads the columns in key order, so letter pairs travel together. It is in none of the route sets. Here every dictionary word giving 3-15 columns keys it, with either cell size first, forward and inverse, with a repeating key of length 1-26 after or before.

## Hypothesis (domain expert)

Type 1, a hand route not tested before. AMSCO: rows of w cells holding alternately 1 and 2 letters, each row starting with the other size from the row above, the first cell 1 or 2; columns read in true keyword order (repeats dropped, or the whole word), cells top to bottom; w = 3-15 from every dictionary word; forward and inverse, deduplicated. Key: periodic 1-26 after (slot = carved place mod p) or before, 8 tableau classes, exact by slot agreement. Keeping letter pairs together would also keep some English adjacency, as the width-21 repeats suggest (0018). Ten shuffled coppers.

## Prediction

Nothing consistent below period 20; counts inside the coppers' range, give or take one period. Zero candidates.

## Method

1. Turn every dictionary word into its column orders of 3-15 columns, each with either first cell size.
2. Build the move and its inverse; drop repeats.
3. Test periods 1-26 in both orders and 8 classes.
4. Count per period on K4 and ten shuffled coppers.

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
 "family": "AMSCO (cells of 1 and 2 letters) keyed by every dictionary word of 3-15 columns, then or before a periodic tableau key",
 "words": 234428,
 "distinct_key_and_start_settings": 445680,
 "distinct_routes": 891360,
 "duplicates_skipped": 0,
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
   21,
   4184,
   151,
   572
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
   371,
   269329
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
   1,
   4061,
   98,
   494
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
   230,
   263011
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
   5,
   15,
   4362,
   170,
   593
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
   16,
   535,
   289951
  ]
 },
 "periods_outside_control_range": {
  "A": [
   23
  ],
  "B": []
 },
 "k4_live_below_20": [],
 "n_k4_live_below_20": 0,
 "controls": "10 shuffled coppers (seed 114), identical search"
}
```

Notes: 445,680 distinct AMSCO settings from 234,428 words, 891,360 routes x 8 classes x 2 orders, periods 1-26. K4 live below 20: 0. Outside the control range: {'A': [23], 'B': []}.


