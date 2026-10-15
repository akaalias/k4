# 0065-constructions-that-line-up-doublets-in-sevens: Which ways of making a cipher put the doubled letters in one column of seven?

**Family:** 7-construction-simulation  
**Parent:** 0062-which-constructions-make-the-width-fingerprints  
**Decision:** reverted  
**Run:** 2026-10-15T13:05:37+00:00, 1.0 s, status ran  
**Time by phase:** design 46 s, implement 0 s, test 12 s, run 1 s, record 0 s

## In plain words

Five of the copper's six doubled letters sit in the same column when the carved letters are written in rows of seven, and experiment 56 showed that is no accident. We make thousands of fake coppers from real English with recipes that have a seven built in, and count how often each recipe puts the doublets in one column. The most promising recipe is an autokey cipher that feeds on the previous carved letter, combined with a repeating secret word of seven letters. Random letters and scrambled copies of the copper show how often the pattern turns up by luck.

## Walkthrough, by hand

1. Take a 97-letter stretch of Carter's book and a random secret word of 7 letters.
2. Encipher the first letter on the sculpture's table with the first key letter.
3. For each later letter, add its key letter and also the previous carved letter, counted along the sculpture's alphabet KRYPTOSABCDEFGHIJLMNQUVWXZ, and write the result.
4. A letter repeats its neighbour exactly when the plaintext letter plus its key letter counts to 26, back to K: A is 7th from K (counting K as 0) and N is 19th, so with key letter A in slot 5, every N in slot 5 makes a doublet.
5. Write the result in rows of 7 and look for a column holding most of the doublets.
6. Repeat four thousand times per recipe and count.

## Worked example (generated)

```
plaintext SLOWLYDESPARATLYSLOWLYTHEREMAINSOFPASSAGEDEBRIS
key KRYPTOS repeating, plus the previous carved letter
carved   DYCCTERFNXBGZCKPEOHJGIQDXPNLXHCMRMRBIWAXHTIXRNP
doublets at 0-based [2]; mod 7 [2]
```

## Lineage

Inherits from 0062-which-constructions-make-the-width-fingerprints. What changed: Experiment 62 found no recipe that makes the copper's doublet column at width 7. This tries recipes built specifically to line doublets up in sevens: a key that feeds on the previous carved letter plus a repeating key of 7, a key with two equal neighbouring letters, the same reshuffle applied to every block of 7, and a key of 28 with a pattern every 7.

## Hypothesis (domain expert)

Family 7 (Oranchak's construction simulation), aimed at the width-7 doublet column that 0056 showed is real (five of six doublets at 0-based positions 18, 25, 32, 46, 67, all 4 mod 7). A ciphertext doublet c[i] = c[i+1] needs a mechanism tied to i mod 7. Candidates: (1) ciphertext autokey at lag 1 plus a period-7 key, c[i] = p[i] + k[i mod 7] + c[i-1]: a doublet appears exactly when p[i+1] = -k[(i+1) mod 7], so one column fires on a frequent plaintext letter; periods 14 and 28 for comparison. (2) plaintext autokey at lag 1 plus a period-7 key. (3) a period-7 key with two equal neighbouring letters, which passes plaintext doublets through in one column only. (4) a period-7 Vigenere and one fixed reshuffle of every block of 7, in either order. (5) a period-28 key whose steps at slots 4-5, 11-12, 18-19, 25-26 are equal (28 survives the crib sweep). (6) a period-7 Vigenere read out in columns of 7 from a width-14 grid. Plaintexts: 97-letter windows of Carter's Tomb of Tut-ankh-Amen and K1-K3 (C7(d)). 4,000 samples per recipe, KRYPTOS alphabet, random keys. Statistic as in 0056 and 0062: at least 4 doublets with at most one outside the fullest column of 7. Calibrations: random letters and shuffles of K4. Clue entries: C11a ('interval 7'), C1(a).

## Prediction

The ciphertext autokey at lag 1 with a period-7 key makes the doublet column in more than 5% of samples, at least ten times the calibrations (which stay below 0.5%). The key with two equal neighbouring letters makes it rarely (below 2%), because English doublets are few. The block reshuffles, the structured key of 28 and the width-14 read-out stay within twice the calibration rate.

## Method

1. Draw 97-letter English windows.
2. Encipher each with each recipe and a fresh random key.
3. Find the doublets and write the text in rows of 7; note whether at least four doublets fall in one column with at most one elsewhere.
4. Count the share of samples with the mark, and the mean number of doublets.
5. Compare with random letters and shuffled K4.

## Result

Candidates returned: 0. Passed all gates: 0. Best crib hits among all candidates: 0/24
(no candidates).
Best loss: None (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: 0034-complete-the-key-at-surviving-periods.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| - | no candidates | | | | |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "construction simulation for the width-7 doublet column",
 "samples_per_recipe": 4000,
 "k4": {
  "column": true,
  "doublets": 6
 },
 "plaintext_source": "Carter vol. 1 (284,914 letters) and K1-K3",
 "rates": {
  "ciphertext autokey lag 1 plus a period-7 key": {
   "column": 0.0147,
   "mean_doublets": 3.76
  },
  "ciphertext autokey lag 1 plus a period-14 key": {
   "column": 0.0057,
   "mean_doublets": 3.74
  },
  "ciphertext autokey lag 1 plus a period-28 key": {
   "column": 0.0073,
   "mean_doublets": 3.69
  },
  "plaintext autokey lag 1 plus a period-7 key": {
   "column": 0.0018,
   "mean_doublets": 3.71
  },
  "period-7 key with two equal neighbouring letters": {
   "column": 0.0025,
   "mean_doublets": 3.57
  },
  "period-7 Vigenere, then one reshuffle of every block of 7": {
   "column": 0.0027,
   "mean_doublets": 3.74
  },
  "one reshuffle of every block of 7, then period-7 Vigenere": {
   "column": 0.002,
   "mean_doublets": 3.74
  },
  "period-28 key with the same step at slots 4-5, 11-12, 18-19, 25-26": {
   "column": 0.0013,
   "mean_doublets": 3.72
  },
  "period-7 Vigenere read out in columns of 7 (width-14 grid)": {
   "column": 0.0035,
   "mean_doublets": 6.15
  },
  "calibration: random letters": {
   "column": 0.001,
   "mean_doublets": 3.71
  },
  "calibration: shuffled K4": {
   "column": 0.0027,
   "mean_doublets": 3.49
  }
 }
}
```

Notes: Doublet-column rate (mean doublets): ciphertext autokey lag 1 plus a period-7 key: 0.0147 (3.76); ciphertext autokey lag 1 plus a period-28 key: 0.0073 (3.69); ciphertext autokey lag 1 plus a period-14 key: 0.0057 (3.74); period-7 Vigenere read out in columns of 7 (width-14 grid): 0.0035 (6.15); period-7 Vigenere, then one reshuffle of every block of 7: 0.0027 (3.74); calibration: shuffled K4: 0.0027 (3.49); period-7 key with two equal neighbouring letters: 0.0025 (3.57); one reshuffle of every block of 7, then period-7 Vigenere: 0.0020 (3.74); plaintext autokey lag 1 plus a period-7 key: 0.0018 (3.71); period-28 key with the same step at slots 4-5, 11-12, 18-19, 25-26: 0.0013 (3.72); calibration: random letters: 0.0010 (3.71).


