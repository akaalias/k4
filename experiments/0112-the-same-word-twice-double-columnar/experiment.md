# 0112-the-same-word-twice-double-columnar: Double columnar with the same English word both times, with a repeating key before or after

**Family:** 6-transposition-then-tableau  
**Parent:** 0110-keyword-columnar-from-the-whole-dictionary  
**Decision:** reverted  
**Run:** 2026-10-15T20:38:30+00:00, 202.6 s, status ran  
**Time by phase:** unattributed 1 s, run 203 s, record 0 s

## In plain words

Soldiers once enciphered by shuffling columns under a secret word, then doing it again with the same word, which is easy to remember. Here every word in an English dictionary is used that way, twice in a row, with a short repeating secret word on the table before or after, against the 24 known letters.

## Walkthrough, by hand

1. SHADOW gives the column order 3, 4, 2, 5, 1, 6.
2. Write the 97 letters in rows of 6, read the columns in that order; write the result in rows of 6 again and read it the same way.
3. Each known letter lands at a new place; with a key of length p after the move, letters sharing a slot must agree.
4. Repeat for every word, key length and rule, and with the key before the move.

## Worked example (generated)

```
SHADOW twice: columns read in the order [3, 4, 2, 5, 1, 6], then again

place  letter  after one  after two  copper there
   22       E         20         36             T
   23       A         52         25             V
   24       S         85         79             Z
   25       T         69         12             L
   64       B         27          5             U
```

## Lineage

Inherits from 0110-keyword-columnar-from-the-whole-dictionary. What changed: 0084 and 0085 tested double columnar with two keys from the puzzle's words; the dictionary is too large for every pair. The classic field double transposition uses one key word twice, which the whole dictionary allows. Here every dictionary word (true keyword order, repeats dropped or whole word) keys both passes, forward and inverse, with a repeating key of length 1-26 after or before.

## Hypothesis (domain expert)

Type 1 (C1: 'double matrixes'); the U.S. Army double transposition used one key for both passes, and Scheidt taught field methods (C5: 'simple, can be remembered'). Routes: the 229,634 distinct column orders of 0110, each applied twice, forward and inverse, deduplicated. Key: periodic 1-26 after the move (slot = carved place mod p) or before it, 8 tableau classes, exact by slot agreement. Ten shuffled coppers.

## Prediction

Nothing consistent below period 20; counts inside the coppers' range, give or take one period. Zero candidates.

## Method

1. Turn every dictionary word into its two column orders; drop repeats.
2. Apply each twice and take the inverse.
3. Test periods 1-26 in both orders and 8 classes by slot agreement.
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
 "family": "double keyword columnar with the same dictionary word twice, then or before a periodic tableau key",
 "words": 234428,
 "distinct_column_orders": 229634,
 "distinct_routes": 459267,
 "duplicates_skipped": 1,
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
   4,
   3,
   224,
   204,
   854
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
   199,
   142078
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
   83,
   173,
   846
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
   165,
   137750
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
   0,
   6,
   8,
   350,
   222,
   894
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
   4,
   242,
   144613
  ]
 },
 "periods_outside_control_range": {
  "A": [],
  "B": []
 },
 "k4_live_below_20": [],
 "n_k4_live_below_20": 0,
 "controls": "10 shuffled coppers (seed 112), identical search"
}
```

Notes: 229,634 distinct column orders from 234,428 words, 459,267 routes x 8 classes x 2 orders, periods 1-26. K4 live below 20: 0. Outside the control range: {'A': [], 'B': []}.


