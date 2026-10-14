# 0018-construction-simulator-fingerprint: Construction simulator: which cipher families produce texts with K4's statistical fingerprint?

**Family:** 7-construction-simulation  
**Parent:** none (root)  
**Decision:** reverted  
**Run:** 2026-10-14T17:34:37+00:00, 4.1 s, status ran  
**Time by phase:** design 776 s, implement 78 s, test 19 s, run 4 s, record 0 s

## In plain words

Instead of trying to break the message, we build a workshop. We take ordinary English text, scramble it with each kind of cipher we suspect, using random keys, thousands of times, and measure the results: how evenly the letters are spread, how often a letter repeats its neighbour, how letters line up in columns. Then we ask which kind of cipher most often produces text that measures like K4. The method that solved another famous cipher, the Zodiac killer's, worked this way. It will not tell us the message, but it tells us where to dig.

## Walkthrough, by hand

1. Count each letter in K4: K appears 8 times, M and Y once.
2. The index of coincidence is the chance two letters drawn at random match: add n(n-1) over the 26 counts and divide by 97 times 96; K4 gives 0.0361.
3. Now take an English sentence of 97 letters and encipher it with a repeating key of 28 random letters on the sculpture's table.
4. Count its letters the same way and compute its index.
5. Do this 5,000 times and see where 0.0361 falls among the results.
6. Repeat for the other statistics and the other ciphers.
7. A cipher that rarely produces K4's numbers is unlikely; one that often does stays on the list.

## Worked example (generated)

```
one sample from the periodic-Vigenere generator against K4

plain  ORMATIONWASGATHEREDANDTRANSMITTEDUNDERGRUUNDTOANUNKNOWNLOCATIONXDOESLANGLEYKNOWABOUTTHISTHEYSHOUL
cipher QEUCCMKEVQJJHVAIPGLTXZYKUZJAZASJGJECXEJBGHWFSFTXDLZAEABRBEFADWMEQBMXDEUIXBAILTEGMQOASNMRVGXFCUWHU

statistic                           K4    sample
ic                              0.0361    0.0395
distinct                       26.0000   26.0000
doublets                        6.0000    2.0000
width7_doublet_column           5.0000    2.0000
width21_vertical_repeats       11.0000    1.0000
repeated_bigrams               10.0000    7.0000
top_count                       8.0000    9.0000
singletons                      2.0000    4.0000
closeness_mean_distance         5.5833    7.2083
self_encryptions                2.0000    0.0000
```

## Lineage

Inherits from nothing; this is a root experiment. What changed: New root in family 7. Not a solver: fourteen generators encrypt English windows with random keys, and K4's statistics are placed in each family's distribution.

## Hypothesis (domain expert)

Oranchak, Blake and Van Eycke solved Zodiac 340 by simulating constructions until one reproduced the ciphertext's fingerprint (knowledge/07-people.md). K4's fingerprint (knowledge/04-structure.md): index of coincidence 0.0361; all 26 letters present; six doublets, five of them in one column at width 7; eleven repeated vertical bigrams at width 21; top frequency 8; and Bean's closeness, the crib plaintext letters sitting near their ciphertext letters on the standard alphabet. Each generator takes a random 97-letter window of the K1-K3 plaintexts and a random key: periodic Vigenere on the KRYPTOS alphabet at periods 27-30, Quagmire with random alphabets, progressive key, plaintext autokey, running key, columnar then Vigenere, Vigenere then columnar, Hill 2x2 and 3x3, Gromark base 10, plus three calibration generators (random letters, pure transposition, monoalphabetic). For each statistic and generator we record the two-sided empirical p-value of K4's value and a combined distance. The result ranks families by plausibility; it decides none. Bounds: 5,000 samples per generator, these twelve statistics.

## Prediction

K4's flat letter distribution sits comfortably inside every polyalphabetic family and outside the monoalphabetic and pure-transposition calibrations. The width-7 doublet column and the width-21 repeats are unusual under every generator, with p-values near 0.01 to 0.1, so no family is singled out by them. Bean's closeness statistic separates families: letter-for-letter systems on a near-standard alphabet reproduce it more often than transposed or Hill systems.

## Method

1. Define the statistics on a 97-letter text, with the plaintext available for the closeness statistic at the 24 crib positions.
2. Build fourteen generators.
3. Draw 5,000 samples each.
4. For each statistic, compute K4's two-sided empirical p-value under each generator and a z-score.
5. Combine the z-scores into a distance and rank the generators.

## Result

Candidates returned: 0. Passed all gates: 0. Best crib hits among all candidates: 0/24
(no candidates).
Best loss: None (0 is solved; 10 per missed crib letter). Best fitness: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| - | no candidates | | | | |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "construction simulation",
 "samples_per_generator": 5000,
 "statistics": [
  "ic",
  "distinct",
  "doublets",
  "width7_doublet_column",
  "width21_vertical_repeats",
  "repeated_bigrams",
  "top_count",
  "singletons",
  "closeness_mean_distance",
  "self_encryptions"
 ],
 "k4": {
  "ic": 0.0361,
  "distinct": 26,
  "doublets": 6,
  "width7_doublet_column": 5,
  "width21_vertical_repeats": 11,
  "repeated_bigrams": 10,
  "top_count": 8,
  "singletons": 2,
  "closeness_mean_distance": 5.5833,
  "self_encryptions": 2
 },
 "ranking_by_distance": [
  [
   "Hill 2x2",
   6.02
  ],
  [
   "Hill 3x3",
   6.32
  ],
  [
   "columnar transposition then Vigenere",
   6.44
  ],
  [
   "Vigenere then columnar transposition",
   6.44
  ],
  [
   "Quagmire, random alphabets, period 27-30",
   6.46
  ],
  [
   "progressive key, period 7-13",
   6.46
  ],
  [
   "periodic Vigenere, KRYPTOS alphabet, period 27-30",
   6.47
  ],
  [
   "Gromark base 10, random cipher alphabet",
   6.51
  ],
  [
   "calibration: random letters",
   6.62
  ],
  [
   "plaintext autokey, lag 1-30",
   7.67
  ],
  [
   "calibration: pure columnar transposition",
   7.7
  ],
  [
   "running key from K1-K3 English",
   8.22
  ],
  [
   "calibration: monoalphabetic",
   11.12
  ]
 ],
 "table": {
  "periodic Vigenere, KRYPTOS alphabet, period 27-30": {
   "ic": {
    "mean": 0.0392,
    "sd": 0.003,
    "z": -1.02,
    "p": 0.315
   },
   "distinct": {
    "mean": 25.3206,
    "sd": 0.7832,
    "z": 0.87,
    "p": 0.981
   },
   "doublets": {
    "mean": 3.7382,
    "sd": 1.8949,
    "z": 1.19,
    "p": 0.348
   },
   "width7_doublet_column": {
    "mean": 1.5956,
    "sd": 0.7131,
    "z": 4.77,
    "p": 0.002
   },
   "width21_vertical_repeats": {
    "mean": 4.2508,
    "sd": 1.9847,
    "z": 3.4,
    "p": 0.005
   },
   "repeated_bigrams": {
    "mean": 6.9578,
    "sd": 2.5519,
    "z": 1.19,
    "p": 0.298
   },
   "top_count": {
    "mean": 8.2146,
    "sd": 1.2542,
    "z": -0.17,
    "p": 1.0
   },
   "singletons": {
    "mean": 2.3732,
    "sd": 1.3389,
    "z": -0.28,
    "p": 1.0
   },
   "closeness_mean_distance": {
    "mean": 6.511,
    "sd": 0.775,
    "z": -1.2,
    "p": 0.242
   },
   "self_encryptions": {
    "mean": 0.9202,
    "sd": 0.9499,
    "z": 1.14,
    "p": 0.472
   },
   "_distance": 6.47,
   "_n": 5000
  },
  "Quagmire, random alphabets, period 27-30": {
   "ic": {
    "mean": 0.0393,
    "sd": 0.0031,
    "z": -1.04,
    "p": 0.304
   },
   "distinct": {
    "mean": 25.3228,
    "sd": 0.7667,
    "z": 0.88,
    "p": 0.971
   },
   "doublets": {
    "mean": 3.6792,
    "sd": 1.8721,
    "z": 1.24,
    "p": 0.336
   },
   "width7_doublet_column": {
    "mean": 1.5822,
    "sd": 0.7269,
    "z": 4.7,
    "p": 0.002
   },
   "width21_vertical_repeats": {
    "mean": 4.2276,
    "sd": 1.9483,
    "z": 3.48,
    "p": 0.004
   },
   "repeated_bigrams": {
    "mean": 6.9616,
    "sd": 2.5758,
    "z": 1.18,
    "p": 0.31
   },
   "top_count": {
    "mean": 8.2586,
    "sd": 1.2846,
    "z": -0.2,
    "p": 1.0
   },
   "singletons": {
    "mean": 2.3966,
    "sd": 1.3388,
    "z": -0.3,
    "p": 1.0
   },
   "closeness_mean_distance": {
    "mean": 6.5014,
    "sd": 0.7781,
    "z": -1.18,
    "p": 0.243
   },
   "self_encryptions": {
    "mean": 0.9302,
    "sd": 0.9523,
    "z": 1.12,
    "p": 0.473
   },
   "_distance": 6.46,
   "_n": 5000
  },
  "progressive key, period 7-13": {
   "ic": {
    "mean": 0.0384,
    "sd": 0.0029,
    "z": -0.81,
    "p": 0.466
   },
   "distinct": {
    "mean": 25.421,
    "sd": 0.7245,
    "z": 0.8,
    "p": 1.0
   },
   "doublets": {
    "mean": 3.7364,
    "sd": 1.9659,
    "z": 1.15,
    "p": 0.357
   },
   "width7_doublet_column": {
    "mean": 1.6078,
    "sd": 0.7403,
    "z": 4.58,
    "p": 0.003
   },
   "width21_vertical_repeats": {
    "mean": 4.0782,
    "sd": 1.9177,
    "z": 3.61,
    "p": 0.006
   },
   "repeated_bigrams": {
    "mean": 6.3984,
    "sd": 2.4266,
    "z": 1.48,
    "p": 0.206
   },
   "top_count": {
    "mean": 7.991,
    "sd": 1.1975,
    "z": 0.01,
    "p": 1.0
   },
   "singletons": {
    "mean": 2.2376,
    "sd": 1.2875,
    "z": -0.18,
    "p": 1.0
   },
   "closeness_mean_distance": {
    "mean": 6.5197,
    "sd": 0.7672,
    "z": -1.22,
    "p": 0.232
   },
   "self_encryptions": {
    "mean": 0.9152,
    "sd": 0.9241,
    "z": 1.17,
    "p": 0.48
   },
   "_distance": 6.46,
   "_n": 5000
  },
  "plaintext autokey, lag 1-30": {
   "ic": {
    "mean": 0.0402,
    "sd": 0.0034,
    "z": -1.21,
    "p": 0.204
   },
   "distinct": {
    "mean": 25.2278,
    "sd": 0.8077,
    "z": 0.96,
    "p": 0.858
   },
   "doublets": {
    "mean": 3.7288,
    "sd": 1.9588,
    "z": 1.16,
    "p": 0.347
   },
   "width7_doublet_column": {
    "mean": 1.6134,
    "sd": 0.7504,
    "z": 4.51,
    "p": 0.002
   },
   "width21_vertical_repeats": {
    "mean": 4.5574,
    "sd": 2.1391,
    "z": 3.01,
    "p": 0.02
   },
   "repeated_bigrams": {
    "mean": 7.7728,
    "sd": 3.0887,
    "z": 0.72,
    "p": 0.476
   },
   "top_count": {
    "mean": 8.4878,
    "sd": 1.3595,
    "z": -0.36,
    "p": 1.0
   },
   "singletons": {
    "mean": 2.5516,
    "sd": 1.3845,
    "z": -0.4,
    "p": 1.0
   },
   "closeness_mean_distance": {
    "mean": 7.0589,
    "sd": 0.6999,
    "z": -2.11,
    "p": 0.032
   },
   "self_encryptions": {
    "mean": 0.174,
    "sd": 0.4041,
    "z": 4.52,
    "p": 0.017
   },
   "_distance": 7.67,
   "_n": 5000
  },
  "running key from K1-K3 English": {
   "ic": {
    "mean": 0.0397,
    "sd": 0.0038,
    "z": -0.95,
    "p": 0.241
   },
   "distinct": {
    "mean": 25.241,
    "sd": 0.9257,
    "z": 0.82,
    "p": 0.907
   },
   "doublets": {
    "mean": 3.6916,
    "sd": 1.8837,
    "z": 1.23,
    "p": 0.313
   },
   "width7_doublet_column": {
    "mean": 1.5906,
    "sd": 0.7388,
    "z": 4.61,
    "p": 0.003
   },
   "width21_vertical_repeats": {
    "mean": 4.3372,
    "sd": 2.0785,
    "z": 3.21,
    "p": 0.011
   },
   "repeated_bigrams": {
    "mean": 7.118,
    "sd": 2.8865,
    "z": 1.0,
    "p": 0.348
   },
   "top_count": {
    "mean": 8.3338,
    "sd": 1.3119,
    "z": -0.25,
    "p": 1.0
   },
   "singletons": {
    "mean": 2.5058,
    "sd": 1.362,
    "z": -0.37,
    "p": 1.0
   },
   "closeness_mean_distance": {
    "mean": 7.1139,
    "sd": 0.7043,
    "z": -2.17,
    "p": 0.032
   },
   "self_encryptions": {
    "mean": 0.1488,
    "sd": 0.3559,
    "z": 5.2,
    "p": 0.0
   },
   "_distance": 8.22,
   "_n": 5000
  },
  "columnar transposition then Vigenere": {
   "ic": {
    "mean": 0.0392,
    "sd": 0.0031,
    "z": -0.99,
    "p": 0.33
   },
   "distinct": {
    "mean": 25.329,
    "sd": 0.7709,
    "z": 0.87,
    "p": 0.978
   },
   "doublets": {
    "mean": 3.6964,
    "sd": 1.9016,
    "z": 1.21,
    "p": 0.33
   },
   "width7_doublet_column": {
    "mean": 1.5938,
    "sd": 0.7272,
    "z": 4.68,
    "p": 0.001
   },
   "width21_vertical_repeats": {
    "mean": 4.2484,
    "sd": 1.9669,
    "z": 3.43,
    "p": 0.004
   },
   "repeated_bigrams": {
    "mean": 6.7552,
    "sd": 2.4759,
    "z": 1.31,
    "p": 0.283
   },
   "top_count": {
    "mean": 8.215,
    "sd": 1.2856,
    "z": -0.17,
    "p": 1.0
   },
   "singletons": {
    "mean": 2.3556,
    "sd": 1.3038,
    "z": -0.27,
    "p": 1.0
   },
   "closeness_mean_distance": {
    "mean": 6.4853,
    "sd": 0.77,
    "z": -1.17,
    "p": 0.26
   },
   "self_encryptions": {
    "mean": 0.9062,
    "sd": 0.9492,
    "z": 1.15,
    "p": 0.461
   },
   "_distance": 6.44,
   "_n": 5000
  },
  "Vigenere then columnar transposition": {
   "ic": {
    "mean": 0.0392,
    "sd": 0.003,
    "z": -1.02,
    "p": 0.299
   },
   "distinct": {
    "mean": 25.3406,
    "sd": 0.7593,
    "z": 0.87,
    "p": 0.986
   },
   "doublets": {
    "mean": 3.7534,
    "sd": 1.9477,
    "z": 1.15,
    "p": 0.346
   },
   "width7_doublet_column": {
    "mean": 1.6072,
    "sd": 0.7327,
    "z": 4.63,
    "p": 0.002
   },
   "width21_vertical_repeats": {
    "mean": 4.1964,
    "sd": 1.942,
    "z": 3.5,
    "p": 0.004
   },
   "repeated_bigrams": {
    "mean": 6.7388,
    "sd": 2.4644,
    "z": 1.32,
    "p": 0.256
   },
   "top_count": {
    "mean": 8.2088,
    "sd": 1.2565,
    "z": -0.17,
    "p": 1.0
   },
   "singletons": {
    "mean": 2.3932,
    "sd": 1.3381,
    "z": -0.29,
    "p": 1.0
   },
   "closeness_mean_distance": {
    "mean": 6.4986,
    "sd": 0.7653,
    "z": -1.2,
    "p": 0.246
   },
   "self_encryptions": {
    "mean": 0.9232,
    "sd": 0.9483,
    "z": 1.14,
    "p": 0.476
   },
   "_distance": 6.44,
   "_n": 5000
  },
  "Hill 2x2": {
   "ic": {
    "mean": 0.0422,
    "sd": 0.0046,
    "z": -1.32,
    "p": 0.107
   },
   "distinct": {
    "mean": 24.9518,
    "sd": 0.9846,
    "z": 1.06,
    "p": 0.674
   },
   "doublets": {
    "mean": 3.7798,
    "sd": 2.0318,
    "z": 1.09,
    "p": 0.372
   },
   "width7_doublet_column": {
    "mean": 1.6028,
    "sd": 0.7477,
    "z": 4.54,
    "p": 0.002
   },
   "width21_vertical_repeats": {
    "mean": 4.8112,
    "sd": 2.1456,
    "z": 2.88,
    "p": 0.018
   },
   "repeated_bigrams": {
    "mean": 13.549,
    "sd": 3.4813,
    "z": -1.02,
    "p": 0.378
   },
   "top_count": {
    "mean": 9.0674,
    "sd": 1.7266,
    "z": -0.62,
    "p": 0.858
   },
   "singletons": {
    "mean": 2.8426,
    "sd": 1.427,
    "z": -0.59,
    "p": 0.843
   },
   "closeness_mean_distance": {
    "mean": 6.5064,
    "sd": 0.8201,
    "z": -1.13,
    "p": 0.265
   },
   "self_encryptions": {
    "mean": 1.3818,
    "sd": 1.5327,
    "z": 0.4,
    "p": 0.743
   },
   "_distance": 6.02,
   "_n": 5000
  },
  "Hill 3x3": {
   "ic": {
    "mean": 0.0392,
    "sd": 0.0032,
    "z": -0.98,
    "p": 0.33
   },
   "distinct": {
    "mean": 25.3542,
    "sd": 0.7594,
    "z": 0.85,
    "p": 1.0
   },
   "doublets": {
    "mean": 3.6594,
    "sd": 1.925,
    "z": 1.22,
    "p": 0.336
   },
   "width7_doublet_column": {
    "mean": 1.5792,
    "sd": 0.7319,
    "z": 4.67,
    "p": 0.001
   },
   "width21_vertical_repeats": {
    "mean": 4.1778,
    "sd": 1.9324,
    "z": 3.53,
    "p": 0.004
   },
   "repeated_bigrams": {
    "mean": 8.3712,
    "sd": 3.3328,
    "z": 0.49,
    "p": 0.665
   },
   "top_count": {
    "mean": 8.227,
    "sd": 1.3055,
    "z": -0.17,
    "p": 1.0
   },
   "singletons": {
    "mean": 2.4016,
    "sd": 1.3625,
    "z": -0.29,
    "p": 1.0
   },
   "closeness_mean_distance": {
    "mean": 6.483,
    "sd": 0.791,
    "z": -1.14,
    "p": 0.268
   },
   "self_encryptions": {
    "mean": 1.0268,
    "sd": 1.0317,
    "z": 0.94,
    "p": 0.551
   },
   "_distance": 6.32,
   "_n": 5000
  },
  "Gromark base 10, random cipher alphabet": {
   "ic": {
    "mean": 0.0394,
    "sd": 0.0032,
    "z": -1.05,
    "p": 0.29
   },
   "distinct": {
    "mean": 25.2944,
    "sd": 0.788,
    "z": 0.9,
    "p": 0.938
   },
   "doublets": {
    "mean": 3.4836,
    "sd": 1.8086,
    "z": 1.39,
    "p": 0.273
   },
   "width7_doublet_column": {
    "mean": 1.536,
    "sd": 0.7158,
    "z": 4.84,
    "p": 0.002
   },
   "width21_vertical_repeats": {
    "mean": 4.3684,
    "sd": 1.9744,
    "z": 3.36,
    "p": 0.007
   },
   "repeated_bigrams": {
    "mean": 6.7696,
    "sd": 2.4812,
    "z": 1.3,
    "p": 0.267
   },
   "top_count": {
    "mean": 8.2752,
    "sd": 1.2774,
    "z": -0.22,
    "p": 1.0
   },
   "singletons": {
    "mean": 2.4244,
    "sd": 1.3688,
    "z": -0.31,
    "p": 1.0
   },
   "closeness_mean_distance": {
    "mean": 6.4828,
    "sd": 0.9497,
    "z": -0.95,
    "p": 0.366
   },
   "self_encryptions": {
    "mean": 0.9416,
    "sd": 0.9882,
    "z": 1.07,
    "p": 0.494
   },
   "_distance": 6.51,
   "_n": 5000
  },
  "calibration: random letters": {
   "ic": {
    "mean": 0.0385,
    "sd": 0.0028,
    "z": -0.86,
    "p": 0.42
   },
   "distinct": {
    "mean": 25.4052,
    "sd": 0.7218,
    "z": 0.82,
    "p": 1.0
   },
   "doublets": {
    "mean": 3.718,
    "sd": 1.8841,
    "z": 1.21,
    "p": 0.338
   },
   "width7_doublet_column": {
    "mean": 1.5842,
    "sd": 0.7167,
    "z": 4.77,
    "p": 0.003
   },
   "width21_vertical_repeats": {
    "mean": 4.0524,
    "sd": 1.9072,
    "z": 3.64,
    "p": 0.005
   },
   "repeated_bigrams": {
    "mean": 6.47,
    "sd": 2.4071,
    "z": 1.47,
    "p": 0.217
   },
   "top_count": {
    "mean": 8.013,
    "sd": 1.1869,
    "z": -0.01,
    "p": 1.0
   },
   "singletons": {
    "mean": 2.2224,
    "sd": 1.2779,
    "z": -0.17,
    "p": 1.0
   },
   "closeness_mean_distance": {
    "mean": 6.5137,
    "sd": 0.7725,
    "z": -1.2,
    "p": 0.236
   },
   "self_encryptions": {
    "mean": 0.9354,
    "sd": 0.9226,
    "z": 1.15,
    "p": 0.466
   },
   "_distance": 6.62,
   "_n": 5000
  },
  "calibration: pure columnar transposition": {
   "ic": {
    "mean": 0.0664,
    "sd": 0.0073,
    "z": -4.16,
    "p": 0.0
   },
   "distinct": {
    "mean": 20.4122,
    "sd": 1.1891,
    "z": 4.7,
    "p": 0.0
   },
   "doublets": {
    "mean": 6.5514,
    "sd": 2.7536,
    "z": -0.2,
    "p": 1.0
   },
   "width7_doublet_column": {
    "mean": 2.308,
    "sd": 0.9011,
    "z": 2.99,
    "p": 0.032
   },
   "width21_vertical_repeats": {
    "mean": 10.8536,
    "sd": 3.1216,
    "z": 0.05,
    "p": 1.0
   },
   "repeated_bigrams": {
    "mean": 17.1208,
    "sd": 3.9713,
    "z": -1.79,
    "p": 0.055
   },
   "top_count": {
    "mean": 13.7642,
    "sd": 2.3424,
    "z": -2.46,
    "p": 0.0
   },
   "singletons": {
    "mean": 3.2488,
    "sd": 1.4165,
    "z": -0.88,
    "p": 0.607
   },
   "closeness_mean_distance": {
    "mean": 6.3669,
    "sd": 0.8131,
    "z": -0.96,
    "p": 0.348
   },
   "self_encryptions": {
    "mean": 1.8556,
    "sd": 1.3268,
    "z": 0.11,
    "p": 1.0
   },
   "_distance": 7.7,
   "_n": 5000
  },
  "calibration: monoalphabetic": {
   "ic": {
    "mean": 0.0665,
    "sd": 0.0073,
    "z": -4.14,
    "p": 0.0
   },
   "distinct": {
    "mean": 20.4458,
    "sd": 1.1934,
    "z": 4.65,
    "p": 0.0
   },
   "doublets": {
    "mean": 2.9128,
    "sd": 0.9879,
    "z": 3.12,
    "p": 0.0
   },
   "width7_doublet_column": {
    "mean": 1.3666,
    "sd": 0.4819,
    "z": 7.54,
    "p": 0.0
   },
   "width21_vertical_repeats": {
    "mean": 10.72,
    "sd": 2.5563,
    "z": 0.11,
    "p": 0.966
   },
   "repeated_bigrams": {
    "mean": 26.1946,
    "sd": 5.0234,
    "z": -3.22,
    "p": 0.0
   },
   "top_count": {
    "mean": 13.7752,
    "sd": 2.35,
    "z": -2.46,
    "p": 0.0
   },
   "singletons": {
    "mean": 3.2864,
    "sd": 1.4479,
    "z": -0.89,
    "p": 0.593
   },
   "closeness_mean_distance": {
    "mean": 6.4898,
    "sd": 1.2044,
    "z": -0.75,
    "p": 0.475
   },
   "self_encryptions": {
    "mean": 0.926,
    "sd": 1.4669,
    "z": 0.73,
    "p": 0.481
   },
   "_distance": 11.12,
   "_n": 5000
  }
 }
}
```

Notes: Diagnostic, no candidates. Ranking nearest first: Hill 2x2 (6.02); Hill 3x3 (6.32); columnar transposition then Vigenere (6.44); Vigenere then columnar transposition (6.44); Quagmire, random alphabets, period 27-30 (6.46).


