# 0062-which-constructions-make-the-width-fingerprints: Which ways of making a cipher leave the copper's two real fingerprints?

**Family:** 7-construction-simulation  
**Parent:** 0056-width-7-and-21-fingerprints-look-elsewhere  
**Decision:** reverted  
**Run:** 2026-10-15T12:29:25+00:00, 1.6 s, status ran  
**Time by phase:** design 0 s, implement 0 s, test 0 s, run 2 s, record 0 s

## In plain words

We now know the copper has two genuine oddities tied to the numbers 7 and 21. A good way to find out what made them is to make fake coppers ourselves, from real English, by different recipes that involve a 7 or a 21, and see which recipes leave the same marks. Random letters and scrambled copies of the real copper show how often the marks turn up by accident.

## Walkthrough, by hand

1. Take a 97-letter stretch of Carter's book.
2. Pick a random secret word of 7 letters and encipher the stretch on the sculpture's table, letter by letter.
3. Find the doubled letters in the result and write it in rows of 7: note the fullest column.
4. Count how often a pair of letters 21 places apart repeats.
5. Do this four thousand times for each recipe and count how often both marks appear as strongly as on the copper.

## Worked example (generated)

```
K4: doublet column mark True, width-21 repeat mark True
```

## Lineage

Inherits from 0056-width-7-and-21-fingerprints-look-elsewhere. What changed: Experiment 56 showed the width-7 doublet column and the width-21 repeats are real, not artefacts of looking at many widths. This builds thousands of fake K4s from English by constructions that carry a 7 or a 21 in their structure, and counts how often each one leaves either fingerprint, or both.

## Hypothesis (domain expert)

Construction simulation (family 7, Oranchak's method) aimed at the two features 0056 confirmed: five of six doublets at one position mod 7, and 11 repeated pairs (c[i], c[i+21]). Plaintexts: 97-letter windows of Carter's Tomb of Tut-ankh-Amen (the K3 source) and the K1-K3 plaintexts. Generators, each 4,000 samples, random keys, KRYPTOS alphabet: Vigenere at periods 7, 14, 21 and 28; plaintext autokey at lags 7 and 21 (C11a 'interval 7'); ciphertext autokey at lags 7 and 21; columnar transposition of width 7 or 21 after a period 27-29 Vigenere; the same transposition before it; and two calibrations, random letters and shuffles of K4. Statistics as in 0056: the fullest doublet column at width 7 as a share of doublets (5 of 6 or stronger: at least 4 doublets and at most one outside the column), and repeats at width 21 >= 11. Report each rate and the joint rate. Diagnostic: no candidates; the calibrations are the controls.

## Prediction

No construction leaves both fingerprints in more than 2% of samples. Vigenere or transposition with a 7 in it raises the doublet column, and those with a 21 raise the repeats, but not together. The calibrations show both marks below 1%.

## Method

1. Draw 97-letter English windows.
2. Encrypt each with each generator and a fresh random key.
3. Compute the doublet column at width 7 and the repeats at width 21.
4. Count the share of samples with the column, with the repeats, and with both.
5. Compare with the calibrations.

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
 "family": "construction simulation for the width-7 and width-21 fingerprints",
 "samples_per_generator": 4000,
 "k4": {
  "column": true,
  "repeats": true
 },
 "plaintext_source": "Carter vol. 1 (284,914 letters) and K1-K3",
 "rates": {
  "Vigenere, period 7": {
   "column": 0.003,
   "repeats": 0.0155,
   "both": 0.0
  },
  "Vigenere, period 14": {
   "column": 0.0022,
   "repeats": 0.0043,
   "both": 0.0
  },
  "Vigenere, period 21": {
   "column": 0.0018,
   "repeats": 0.0045,
   "both": 0.0
  },
  "Vigenere, period 28": {
   "column": 0.0013,
   "repeats": 0.0025,
   "both": 0.0
  },
  "plaintext autokey, lag 7": {
   "column": 0.0015,
   "repeats": 0.004,
   "both": 0.0
  },
  "ciphertext autokey, lag 7": {
   "column": 0.0022,
   "repeats": 0.0015,
   "both": 0.0
  },
  "plaintext autokey, lag 21": {
   "column": 0.0032,
   "repeats": 0.0015,
   "both": 0.0
  },
  "ciphertext autokey, lag 21": {
   "column": 0.0013,
   "repeats": 0.0545,
   "both": 0.0
  },
  "Vigenere 27-29 then columnar width 7": {
   "column": 0.002,
   "repeats": 0.0015,
   "both": 0.0
  },
  "columnar width 7 then Vigenere 27-29": {
   "column": 0.0022,
   "repeats": 0.0018,
   "both": 0.0
  },
  "Vigenere 27-29 then columnar width 21": {
   "column": 0.0022,
   "repeats": 0.0022,
   "both": 0.0
  },
  "columnar width 21 then Vigenere 27-29": {
   "column": 0.0032,
   "repeats": 0.0022,
   "both": 0.0
  },
  "calibration: random letters": {
   "column": 0.0015,
   "repeats": 0.0015,
   "both": 0.0
  },
  "calibration: shuffled K4": {
   "column": 0.001,
   "repeats": 0.0003,
   "both": 0.0
  }
 }
}
```

Notes: Rates (column / repeats / both): ciphertext autokey, lag 21: 0.001 / 0.054 / 0.0000; Vigenere, period 7: 0.003 / 0.015 / 0.0000; Vigenere, period 14: 0.002 / 0.004 / 0.0000; Vigenere, period 21: 0.002 / 0.004 / 0.0000; plaintext autokey, lag 7: 0.002 / 0.004 / 0.0000; columnar width 21 then Vigenere 27-29: 0.003 / 0.002 / 0.0000; plaintext autokey, lag 21: 0.003 / 0.002 / 0.0000; Vigenere 27-29 then columnar width 21: 0.002 / 0.002 / 0.0000; columnar width 7 then Vigenere 27-29: 0.002 / 0.002 / 0.0000; Vigenere, period 28: 0.001 / 0.003 / 0.0000; ciphertext autokey, lag 7: 0.002 / 0.002 / 0.0000; Vigenere 27-29 then columnar width 7: 0.002 / 0.002 / 0.0000; calibration: random letters: 0.002 / 0.002 / 0.0000; calibration: shuffled K4: 0.001 / 0.000 / 0.0000.


