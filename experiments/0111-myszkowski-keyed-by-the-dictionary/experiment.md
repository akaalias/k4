# 0111-myszkowski-keyed-by-the-dictionary: A Myszkowski transposition keyed by any English word with a repeated letter, with a repeating key before or after

**Family:** 6-transposition-then-tableau  
**Parent:** 0110-keyword-columnar-from-the-whole-dictionary  
**Decision:** reverted  
**Run:** 2026-10-15T20:35:59+00:00, 149.8 s, status ran  
**Time by phase:** unattributed 160 s, run 150 s, record 0 s

## In plain words

In the usual column shuffle you read the columns in the alphabetical order of a secret word's letters. When the word has a letter twice, like the two S's of ABSCISSA, Myszkowski's version reads those columns together, zigzagging across each row. We try every dictionary word with a repeated letter this way, with a short repeating secret word on the table before or after, against the 24 known letters.

## Walkthrough, by hand

1. ABSCISSA gives ranks A1 B2 S5 C3 I4 S5 S5 A1.
2. Write the 97 letters in rows of 8.
3. Read rank 1 first: in each row, column 1 then column 8; then rank 2 (column 2) down the rows; and so on, with rank 5 read across columns 3, 6, 7 in each row.
4. Each known letter lands at a new place; with a key of length p after the move, letters sharing a slot must agree.
5. Repeat for every word, key length and rule, and with the key before the move.

## Worked example (generated)

```
ABSCISSA as a Myszkowski key: ranks [1, 2, 5, 3, 4, 5, 5, 1] (both A's rank 1, the S's rank 5)
columns of equal rank are read together, row by row

place  letter  lands at  copper there
   22       E        69             T
   23       A        70             M
   24       S         6             O
   25       T         7             X
   64       B        16             L
```

## Lineage

Inherits from 0110-keyword-columnar-from-the-whole-dictionary. What changed: Every keyed column shuffle so far broke ties in the key word left to right (or dropped repeated letters). Myszkowski's 1902 variant reads columns that share a key letter together, row by row, which gives a different order whenever the word repeats a letter, as ABSCISSA and PALIMPSEST do. Here every dictionary word with a repeated letter is a Myszkowski key, with a repeating key of length 1-26 after or before the move.

## Hypothesis (domain expert)

Type 1, a route family not in any earlier set. ABSCISSA (K2's key) and PALIMPSEST (K1's) both repeat letters (C7(a)); a Myszkowski key reads the columns of equal rank together across each row. Keys: the rank pattern of every dictionary word of 3-30 letters with a repeated letter, deduplicated; rows of the word's length, the last row short; forward and inverse. Key: periodic 1-26 after the move (slot = carved place mod p) or before it, 8 tableau classes, exact by slot agreement. Ten shuffled coppers.

## Prediction

Nothing consistent below period 20; counts inside the coppers' range, give or take one period. Zero candidates.

## Method

1. Turn every dictionary word with a repeated letter into its Myszkowski rank pattern; drop repeats.
2. Build the move and its inverse.
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
 "family": "Myszkowski transposition keyed by every dictionary word with a repeated letter, then or before a periodic tableau key",
 "words": 234428,
 "distinct_myszkowski_keys": 171995,
 "distinct_routes": 343964,
 "duplicates_skipped": 26,
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
   5,
   99,
   493,
   1499,
   2656
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
   121,
   104982
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
   69,
   457,
   1540,
   2602
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
   118,
   104820
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
   9,
   140,
   540,
   1650,
   2831
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
   226,
   111045
  ]
 },
 "periods_outside_control_range": {
  "A": [
   25
  ],
  "B": []
 },
 "k4_live_below_20": [],
 "n_k4_live_below_20": 0,
 "controls": "10 shuffled coppers (seed 111), identical search"
}
```

Notes: 171,995 distinct Myszkowski keys from 234,428 words, 343,964 routes x 8 classes x 2 orders, periods 1-26. K4 live below 20: 0. Outside the control range: {'A': [25], 'B': []}.


