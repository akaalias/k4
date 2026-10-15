# 0110-keyword-columnar-from-the-whole-dictionary: A column shuffle keyed by any English word, with a repeating key before or after

**Family:** 6-transposition-then-tableau  
**Parent:** 0085-true-keyword-columnar-rerun  
**Decision:** reverted  
**Run:** 2026-10-15T20:29:57+00:00, 202.2 s, status ran  
**Time by phase:** unattributed 265 s, run 202 s, record 0 s

## In plain words

A classic way to move letters: write the message under a secret word in rows, then read the columns in the alphabetical order of the word's letters. Experiment 85 tried the puzzle's own words. Here every word in an English dictionary is tried as the column word, followed or preceded by a short repeating secret word on the table, against the 24 known letters.

## Walkthrough, by hand

1. Take the word SHADOW: alphabetical order A D H O S W gives the reading order of columns 3, 4, 2, 5, 1, 6.
2. Write the 97 letters in rows of 6 and read the columns in that order.
3. Each known letter lands at a new place j; with a key of length p after the move, its key letter is slot j mod p.
4. Known letters on the same slot must agree.
5. Repeat for every word, key length and rule, and with the key before the move.

## Worked example (generated)

```
SHADOW: columns read in the order [3, 4, 2, 5, 1, 6]

place  letter  lands at  copper there
   22       E        20             B
   23       A        52             J
   24       S        85             I
   25       T        69             T
   64       B        27             Q
```

## Lineage

Inherits from 0085-true-keyword-columnar-rerun. What changed: 0085 tested true keyword columnar (issue #26) with the puzzle's own 201 words. Here the column key is any word of the project dictionary (233,000 words, read with repeated letters dropped and as the whole word with ties left to right), every distinct column order once, forward and inverse, with a repeating key of length 1-26 after or before the shuffle.

## Hypothesis (domain expert)

Type 1 (C1, 'double matrixes... then went back to this table'); K3's NSA route is a keyword columnar by KRYPTOS (01-facts.md). Column orders: keyword_sequence (repeats dropped, alphabetical order of the key letters, ties left to right) and full_sequence (whole word) from every dictionary word of 2-30 letters, deduplicated (the same order from different words counts once), each as a single columnar transposition, forward and inverse. Key: periodic 1-26 after the move (slot = carved place mod p) or before it, 8 tableau classes, exact by slot agreement. Ten shuffled coppers.

## Prediction

Nothing consistent below period 20; counts at every period inside the coppers' range, give or take one. Zero candidates.

## Method

1. Turn every dictionary word into its two column orders and drop repeats.
2. For each order, build the move and its inverse.
3. For each move and class, compute the key values at the known letters and test periods 1-26 in both orders.
4. Count settings per period on K4 and ten shuffled coppers.

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
 "family": "true-keyword columnar from every dictionary word, then or before a periodic tableau key",
 "words": 234428,
 "distinct_column_orders": 229634,
 "distinct_routes": 459268,
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
   22,
   228,
   1775,
   2713,
   9407
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
   112,
   138002
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
   4,
   231,
   1624,
   2601,
   8910
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
   112,
   137773
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
   1,
   24,
   296,
   1784,
   2945,
   10044
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
   433,
   148824
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
 "controls": "10 shuffled coppers (seed 110), identical search"
}
```

Notes: 229,634 distinct column orders from 234,428 words, 459,268 routes x 8 classes x 2 orders, periods 1-26. K4 live below 20: 0. Outside the control range: {'A': [23], 'B': []}.


