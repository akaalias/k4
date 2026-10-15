# 0096-both-fingerprints-from-two-stage-recipes: Which two-stage recipe, a move and a table, makes both of K4's width fingerprints at once

**Family:** 7-construction-simulation  
**Parent:** 0065-constructions-that-line-up-doublets-in-sevens  
**Decision:** reverted  
**Run:** 2026-10-15T19:41:15+00:00, 15.4 s, status ran  
**Time by phase:** unattributed 7 s, run 15 s, record 0 s

## In plain words

K4 has two odd patterns: when written in rows of 7, its doubled letters stack in one column, and when written in rows of 21, letter pairs repeat straight down more than chance allows. A good guess at the method should make both patterns at once. We build thousands of fake coppers with each two-step recipe tried in experiments 80 to 88, a grid move and the table, and count how often each recipe makes both patterns together.

## Walkthrough, by hand

1. Take 97 letters of Carter's English.
2. Recipe example: write them in rows of 7, read the columns in a random order, then add a random 7-letter key on the sculpture's table.
3. Find the doubled letters in the result and their places mod 7: is all but at most one in the same column, with at least four?
4. Write the result in rows of 21 and count letter pairs that repeat straight down: at least 11?
5. Repeat 20,000 times per recipe and count how often each mark and both appear.

## Worked example (generated)

```
K4's two marks

doublets (place of first letter) and place mod 7:
  BB at 19-20: column 4
  QQ at 26-27: column 4
  SS at 33-34: column 4
  SS at 43-44: column 0
  ZZ at 47-48: column 4
  TT at 68-69: column 4

letter pairs 21 apart that repeat: 11

rows of 21:
  OBKRUOXOGHULBSOLIFBBW
  FLRVQQPRNGKSSOTWTQSJQ
  SSEKZZWATJKLUDIAWINFB
  NYPVTTMZFPKWGDKZXTJCD
  IGKUHUAUEKCAR
```

## Lineage

Inherits from 0065-constructions-that-line-up-doublets-in-sevens. What changed: 0018, 0027, 0062 and 0065 simulated one-stage recipes and asked about one fingerprint at a time. Here the recipes are the two-stage constructions of experiments 80 to 88 (a K3-style move before or after a repeating key, the self-feeding autokey, and 0087's column-plus-row key), and the question is the joint one: how often does a recipe make the width-7 doublet column and the width-21 repeats in the same 97 letters?

## Hypothesis (domain expert)

Type 2 of directions.md, open item 'a joint simulation that makes both fingerprints'. 0056: the width-7 doublet column (5 of 6 doublets in one column) and the width-21 vertical repeats (11 repeated letter pairs 21 apart) survive the look-elsewhere correction (corrected p 0.005 and 0.010); 0062 found ciphertext autokey at lag 21 raises the repeats, 0065 found ciphertext autokey at lag 1 with a period-7 key raises the column, and 0087 found that key = a[j mod 7] + b[j div 7] lines doublets up by construction. Recipes (each 20,000 samples of 97 letters from Carter vol. 1 and K1-K3, random keys): periodic key 7, 14 or 21 with a width-7 columnar, a width-7 quarter turn or a K3-rule move, before or after; ciphertext autokey lag 1 or lag 21 with a period-7 key, with a width-7 move before; the column-plus-row key at width 7 and 21, with and without a move before; and calibrations (random letters, shuffled K4, plain period-7 key). Marks as in 0065 (column: at least 4 doublets and all but one in one column at width 7) and 0056 (repeats: at least K4's 11 at width 21).

## Prediction

No recipe makes both marks in more than 1% of samples. The column-plus-row key at width 7 makes the doublet column often (over 10%) but the width-21 repeats only at the chance rate; ciphertext autokey at lag 21 makes the repeats but not the column. Zero candidates.

## Method

1. Draw 97-letter stretches of English from Carter vol. 1 and K1-K3.
2. Encrypt each with a recipe and fresh random keys, routes and orders.
3. Mark the doublet column at width 7 and the repeats at width 21.
4. Count each mark and both together per recipe over 20,000 samples.
5. Compare with the calibrations.

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
 "family": "joint construction simulation of the width-7 doublet column and the width-21 repeats",
 "samples_per_recipe": 20000,
 "recipes": 29,
 "k4": {
  "column": true,
  "repeats21": 11
 },
 "plaintext_source": "Carter vol. 1 (284,914 letters) and K1-K3",
 "rates": {
  "width-7 columnar, then ciphertext autokey lag 1 + period-7 key": {
   "column": 0.0086,
   "repeats": 0.0019,
   "both": 0.0001,
   "both_if_independent": 2e-05
  },
  "K3-rule move, then period-14 key": {
   "column": 0.0023,
   "repeats": 0.0054,
   "both": 0.0001,
   "both_if_independent": 1e-05
  },
  "width-7 quarter turn, then period-14 key": {
   "column": 0.0022,
   "repeats": 0.0029,
   "both": 0.0001,
   "both_if_independent": 1e-05
  },
  "K3-rule move, then column-plus-row key, width 7": {
   "column": 0.0021,
   "repeats": 0.0022,
   "both": 0.0001,
   "both_if_independent": 0.0
  },
  "period-14 key, then width-7 quarter turn": {
   "column": 0.0019,
   "repeats": 0.0043,
   "both": 0.0001,
   "both_if_independent": 1e-05
  },
  "calibration: period-7 key alone": {
   "column": 0.0019,
   "repeats": 0.0147,
   "both": 0.0001,
   "both_if_independent": 3e-05
  },
  "width-7 quarter turn, then period-21 key": {
   "column": 0.0017,
   "repeats": 0.004,
   "both": 0.0001,
   "both_if_independent": 1e-05
  },
  "width-7 columnar, then ciphertext autokey lag 21 + period-7 key": {
   "column": 0.0013,
   "repeats": 0.0029,
   "both": 0.0001,
   "both_if_independent": 0.0
  },
  "period-21 key, then width-7 quarter turn": {
   "column": 0.0011,
   "repeats": 0.0033,
   "both": 0.0001,
   "both_if_independent": 0.0
  },
  "ciphertext autokey lag 1 + period-7 key": {
   "column": 0.014,
   "repeats": 0.0024,
   "both": 0.0,
   "both_if_independent": 3e-05
  },
  "period-7 key, then width-7 quarter turn": {
   "column": 0.0035,
   "repeats": 0.0137,
   "both": 0.0,
   "both_if_independent": 5e-05
  },
  "column-plus-row key, width 7": {
   "column": 0.0026,
   "repeats": 0.0014,
   "both": 0.0,
   "both_if_independent": 0.0
  },
  "period-7 key, then width-7 columnar": {
   "column": 0.0024,
   "repeats": 0.0132,
   "both": 0.0,
   "both_if_independent": 3e-05
  },
  "K3-rule move, then period-7 key": {
   "column": 0.0022,
   "repeats": 0.0146,
   "both": 0.0,
   "both_if_independent": 3e-05
  },
  "width-7 columnar, then period-7 key": {
   "column": 0.0021,
   "repeats": 0.0097,
   "both": 0.0,
   "both_if_independent": 2e-05
  },
  "width-7 quarter turn, then period-7 key": {
   "column": 0.002,
   "repeats": 0.009,
   "both": 0.0,
   "both_if_independent": 2e-05
  },
  "period-14 key, then width-7 columnar": {
   "column": 0.0019,
   "repeats": 0.005,
   "both": 0.0,
   "both_if_independent": 1e-05
  },
  "width-7 columnar, then period-14 key": {
   "column": 0.0019,
   "repeats": 0.0027,
   "both": 0.0,
   "both_if_independent": 1e-05
  },
  "period-21 key, then K3-rule move": {
   "column": 0.0019,
   "repeats": 0.0031,
   "both": 0.0,
   "both_if_independent": 1e-05
  },
  "ciphertext autokey lag 21 + period-7 key": {
   "column": 0.0019,
   "repeats": 0.0034,
   "both": 0.0,
   "both_if_independent": 1e-05
  },
  "calibration: shuffled K4": {
   "column": 0.0019,
   "repeats": 0.0003,
   "both": 0.0,
   "both_if_independent": 0.0
  },
  "period-14 key, then K3-rule move": {
   "column": 0.0018,
   "repeats": 0.0056,
   "both": 0.0,
   "both_if_independent": 1e-05
  },
  "width-7 columnar, then period-21 key": {
   "column": 0.0018,
   "repeats": 0.0037,
   "both": 0.0,
   "both_if_independent": 1e-05
  },
  "period-21 key, then width-7 columnar": {
   "column": 0.0017,
   "repeats": 0.0034,
   "both": 0.0,
   "both_if_independent": 1e-05
  },
  "K3-rule move, then column-plus-row key, width 21": {
   "column": 0.0017,
   "repeats": 0.0018,
   "both": 0.0,
   "both_if_independent": 0.0
  },
  "calibration: random letters": {
   "column": 0.0016,
   "repeats": 0.0016,
   "both": 0.0,
   "both_if_independent": 0.0
  },
  "K3-rule move, then period-21 key": {
   "column": 0.0015,
   "repeats": 0.0046,
   "both": 0.0,
   "both_if_independent": 1e-05
  },
  "column-plus-row key, width 21": {
   "column": 0.0015,
   "repeats": 0.0015,
   "both": 0.0,
   "both_if_independent": 0.0
  },
  "period-7 key, then K3-rule move": {
   "column": 0.0014,
   "repeats": 0.0116,
   "both": 0.0,
   "both_if_independent": 2e-05
  }
 },
 "best_both": "width-7 columnar, then ciphertext autokey lag 1 + period-7 key",
 "best_column": "ciphertext autokey lag 1 + period-7 key",
 "best_repeats": "calibration: period-7 key alone"
}
```

Notes: Rates column / repeats / both: width-7 columnar, then ciphertext autokey lag 1 + period-7 key: 0.0086 / 0.0019 / 0.0001; K3-rule move, then period-14 key: 0.0023 / 0.0054 / 0.0001; width-7 quarter turn, then period-14 key: 0.0022 / 0.0029 / 0.0001; K3-rule move, then column-plus-row key, width 7: 0.0021 / 0.0022 / 0.0001; period-14 key, then width-7 quarter turn: 0.0019 / 0.0043 / 0.0001; calibration: period-7 key alone: 0.0019 / 0.0147 / 0.0001; width-7 quarter turn, then period-21 key: 0.0017 / 0.0040 / 0.0001; width-7 columnar, then ciphertext autokey lag 21 + period-7 key: 0.0013 / 0.0029 / 0.0001; period-21 key, then width-7 quarter turn: 0.0011 / 0.0033 / 0.0001; ciphertext autokey lag 1 + period-7 key: 0.0140 / 0.0024 / 0.0000; period-7 key, then width-7 quarter turn: 0.0035 / 0.0137 / 0.0000; column-plus-row key, width 7: 0.0026 / 0.0014 / 0.0000.


