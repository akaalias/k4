# 0042-progressive-key-with-mixed-alphabets: A progressive key on a table rebuilt from the puzzle's words

**Family:** 1-keyed-periodic  
**Parent:** 0011-progressive-key-period-sweep  
**Decision:** reverted  
**Run:** 2026-10-15T09:18:39+00:00, 980.9 s, status ran  
**Time by phase:** design 0 s, implement 52 s, test 509 s, run 981 s, record 0 s

## In plain words

Experiment 11 tried the trick where the secret word slides one notch further each time it repeats, and found that no short word works with the sculpture's own table. The table could have been built from another word, which changes the sums. So we rebuild the table from every word the puzzle knows and try every word length up to 30 and every slide again.

## Walkthrough, by hand

1. Build the alphabet from ABSCISSA: ABSCIDEFGHJKLMNOPQRTUVWXYZ, and use it for the message; keep KRYPTOS for the carved letters; Vigenere.
2. Period 13, step 2: position 22 is E, index 5 in the ABSCISSA alphabet; carved F is index 11 in KRYPTOS; the key index is 6; position 22 lies in repeat 1 (positions 14 to 26), so subtract one step: base index 4 for slot 8.
3. Position 74, the K of CLOCK, is repeat 5, slot 8: its key index minus five steps must also give
4. 4. If not, period 13 step 2 is dead for this pair of alphabets.
5. Try every step and every pair; a survivor gives a pattern of base letters with blanks to slide the puzzle's words across.

## Worked example (generated)

```
plain alphabet ABSCISSA/keyword ABSCIDEFGHJKLMNOPQRTUVWXYZ; cipher KRYPTOS; Vigenere; period 13, step 2

pos  plain  carved  key index  repeat  base index  slot
 22    E      F        6        1         4       8
 23    A      L       17        1        15       9
 24    S      R       25        1        23       10
 64    B      N       18        4        10       11
 74    K      K       15        5         5       8

positions 22 and 74 share slot 8: their base indices must agree, or period 13 step 2 is dead for this pair.
```

## Lineage

Inherits from 0011-progressive-key-period-sweep. What changed: Experiment 11 killed progressive keys at periods 1 to 25 and 31 to 51 under the standard and KRYPTOS alphabets. Here the plain and cipher alphabets are the keyword mixings of every vocabulary word; the key alphabet drops out of the consistency test. Periods 1 to 30, steps 1 to 25, the per-repeat form.

## Hypothesis (domain expert)

The Trithemius progression on a keyword alphabet is the classical combination the manuals teach (C5): key index at position i is base[i mod P] plus d times the repeat number. Experiment 11 swept it under 24 conventions; the consistency test depends only on the plain and cipher alphabets, so the 63 x 63 keyword-mixed pairs from the vocabulary are the untested corner. For each pair, mode, period 1-30 and step 1-25, every crib forces the base letter of its slot after the progression is subtracted; a slot forced two ways kills the combination. About 9 million combinations, 24 checks each, with early exit. Survivors at periods up to 30 have their forced base fragment matched against the vocabulary and K1-K3 windows. Bounds: complete for this pool, these periods and steps, the per-repeat form; the per-letter form and periods above 30 are not covered.

## Prediction

Periods 1 to 25 die at every step under every alphabet pair, as they did under the sculpture's alphabets; a scatter of chance survivors appears at 26 to 30. No forced fragment matches a word; zero candidates pass.

## Method

1. Build the alphabet pool.
2. For each plain and cipher alphabet and mode, compute the forced key index at each crib.
3. For each period and step, subtract the progression and reduce to the slot; reject on disagreement.
4. Count survivors by period; match surviving fragments against the vocabulary and K1-K3 windows; decrypt and submit matches.

## Result

Candidates returned: 0. Passed all gates: 0. Best crib hits among all candidates: 0/24
(no candidates).
Best loss: None (0 is solved; 10 per missed crib letter). Best fitness: None. Champion before this run: 0034-complete-the-key-at-surviving-periods.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| - | no candidates | | | | |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "progressive key (per-repeat), keyword-mixed alphabets from the vocabulary",
 "alphabets": 63,
 "periods": "1-30",
 "steps": "1-25",
 "combinations_checked": 8930250,
 "survivors_by_period": {
  "25": 44,
  "26": 11176,
  "27": 297675,
  "28": 297675,
  "29": 297675,
  "30": 11435
 },
 "periods_dead_at_every_step_and_pair": [
  1,
  2,
  3,
  4,
  5,
  6,
  7,
  8,
  9,
  10,
  11,
  12,
  13,
  14,
  15,
  16,
  17,
  18,
  19,
  20,
  21,
  22,
  23,
  24
 ],
 "vocab_matches": 0
}
```

Notes: 8930250 combinations. Periods dead under every pair and step: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]. Survivors by period: {25: 44, 26: 11176, 27: 297675, 28: 297675, 29: 297675, 30: 11435}. 0 matches.


