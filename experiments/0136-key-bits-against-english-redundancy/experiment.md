# 0136-key-bits-against-english-redundancy: Which undecided cells could any English test decide? Each blocked cell's key, in bits, against what 73 unknown letters of English can carry

**Family:** 1-keyed-periodic  
**Parent:** 0120-one-free-alphabet-english-climb-at-23-and-26  
**Decision:** reverted  
**Run:** 2026-10-16T16:27:40+00:00, 0.6 s, status ran  
**Time by phase:** design 304 s, implement 319 s, test 8 s, run 1 s, record 0 s

## In plain words

Some of the cipher settings we have tested cannot be ruled in or out by the 24 known letters alone: they fit the known letters, but so do scrambled copies of the carved text. Only the other 73 letters reading as English could tell a true setting from a false one. English is predictable, and that predictability is a fixed amount of information per letter. A setting with a very large secret (a scrambled alphabet plus a long key) has so many versions that some false version will read as English by luck, and then no test can pick the true one. Here we count, for each undecided setting, how big its secret is in bits, and compare it with how much 73 letters of English can say. Settings whose secret is too big are closed as undecidable for good.

## Walkthrough, by hand

1. Take one cell: one scrambled alphabet used on both sides, Beaufort form, a repeating key of 23 letters.
2. Count the alphabet: 26! orders is 88.4 bits; relabelling its places by x -> m x + t (12 x 26 = 312 ways) gives the same decryption, so 88.4 - 8.3 = 80.1 bits.
3. Count the key: 23 letters at 4.70 bits each, 108.1 bits. Total 188.2 bits.
4. The 24 known letters each fix one letter in 26, 4.70 bits each, 112.8 bits: 75.4 bits of the secret are still open.
5. Measure how much a letter of English tells the quadgram scorer: 4.70 bits minus its cross-entropy (about 2.9) is about 1.8 bits; 73 letters carry about 134 bits.
6. 75.4 is less than 134, so a true answer of this kind would stand out from the false ones in principle; whether a search can find it is a separate question.
7. Repeat for every blocked cell; a cell whose open bits exceed even Shannon's most generous figure for English is closed as undecidable.

## Worked example (generated)

```
cell: one unknown alphabet on both sides, Beaufort form, repeating key of 23 letters (F1.1)

  alphabet          log2 26!            =   88.4 bits
  same decryption   x -> m x + t, 312   = -  8.3
  key               23 x 4.70           =  108.1
  total                                 =  188.2
  24 known letters  24 x 4.70           = -112.8
  still open                            =   75.4 bits

  quadgram scorer: cross-entropy 2.92 bits/letter on Carter, so 4.70 - 2.92 = 1.78 bits of evidence per letter
  73 unknown letters x 1.78           =  130.3 bits

  75.4 < 130.3: decidable in principle by the quadgram test (margin 54.9 bits)

  plaintext autokey at lag 86 on a fixed table: 86 x 4.70 + 3 = 407.2 bits, open 294.4,
  more than 73 letters carry even at Shannon's lowest entropy (290 bits): no English test can decide it
```

## Lineage

Inherits from 0120-one-free-alphabet-english-climb-at-23-and-26. What changed: F1.5, step 1 (exact). 0120's climb failed to recover planted texts, and every cell blocked for that reason (F1.1 Beaufort 23 and 26, F1.2's eight lengths, F1.4 on free alphabets, plaintext autokey at lags 53-96, F6.1, F6.2, F8's undecided Hill settings) was blocked by the climb's failure, not by a property of the cell. Here each cell's key is counted in bits and set against the redundancy of the 73 unknown letters: the harness's own quadgram model, measured on held-out English, and Shannon's two estimates for English. A cell whose key, after the 24 known letters, is larger than what 73 letters of English can pin down is blocked for good, with a number.

## Hypothesis (domain expert)

No clue reading is tested; the experiment exists to turn the shared blocker of seven items into numbers (P6, issue #50). Unicity argument (Shannon 1949; Deavours 1977, cited by Bean, knowledge/sources/bean-2021-cryptodiagnosis-of-k4.txt, for Gromark's 48-letter unicity point): if a cell's key has H bits (uniform over a space of 2^H, after removing the symmetries that give the same decryption), about 2^(H - 24 log2 26) keys fit the 24 known letters, and a test with redundancy D bits per letter on the 73 unknown letters expects 2^(R - 73 D) false keys to read as English as well as the true one, R = H - 112.8. R < 73 D is necessary for any English test to decide the cell; it is not sufficient for a search to find the key. Three values of D: (q) the harness's quadgram model, D = log2 26 minus its cross-entropy on held-out English (Carter's book, which is not the table's source; and the K1-K3 plaintexts), measured here; (S1) Shannon 1951 (Bell System Technical Journal 30, 50-64), upper estimate 1.3 bits per character of 27-symbol text, about 1.6 bits per letter once spaces are dropped (5.5 characters per 4.5 letters), D = 3.1; (S0) his lower estimate 0.6 bits per character, about 0.73 per letter, D = 4.0: the most any English test could extract. Key bits per cell: a free alphabet log2 26! = 88.4; the affine re-labellings x -> m x + t of alphabet places (12 x 26, one alphabet; 12 x 26 x 26 for two) give the same decryption and are removed; a key letter 4.70; a choice among N options log2 N (27,852 type-1 moves, 5,054 hand-schedule partitions, 8 tables); a Hill matrix log2 |GL_n(Z26)| = log2 |GL_n(Z2)| + log2 |GL_n(Z13)|. Cells: F1.1 one free alphabet Beaufort L 23, 26; F1.2 two free alphabets L 8, 13, 16, 19, 20, 23, 24, 26; F1.4 hand schedules on one or two free alphabets, keyword 2-31; plaintext autokey lags 53-96 on the 8 standard/KRYPTOS tables; F6.1 one free alphabet with a move, L 6-26; F6.2 two free alphabets with a move, L 3-26; F8 5x5 affine Hill and 4x4 Hill plus a periodic key 1-26.

## Prediction

A scratch check before this was written put the quadgram model's cross-entropy on Carter at 2.86 bits per letter, so D(q) about 1.8 and 73 letters carry about 134 bits. Then: F1.1 at 23 and 26 (R about 75 and 90) lie under every bound; F1.2 lies under the quadgram bound at 8, 13 and 16 and over it from 19 up, under Shannon's at every length; plaintext autokey lags 53-96 lie over the quadgram bound at every lag, and over even Shannon's lower estimate from about lag 86; F6.1 under the quadgram bound at every length; F6.2 under it to about length 14; the 5x5 affine Hill and 4x4 Hill with any key up to 26 under it. So step 1 blocks for good only the long autokey lags, and step 2 (a climb with power) is what decides the rest. Zero candidates.

## Method

1. Measure the quadgram model's cross-entropy on held-out English: Carter's book (letters only) and the K1-K3 plaintexts; also the spread over 73-letter windows.
2. For each blocked cell, count its key in bits, with the symmetries removed.
3. Subtract the 112.8 bits the 24 known letters fix: the residual R.
4. Compare R with 73 D for D from the quadgram model and from Shannon's two estimates.
5. Classify each cell: decidable by the quadgram test in principle, only by a better English model, or by none.

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
 "family": "bound, not a search: key bits of every blocked cell against the redundancy of 73 letters of English",
 "quadgram_cross_entropy_bits_per_letter": {
  "carter_book": 2.916,
  "k1_k3_plaintexts": 2.944,
  "carter_73_letter_windows": {
   "n": 142,
   "median": 2.864,
   "p10_least_predictable": 3.227,
   "p90_most_predictable": 2.545
  }
 },
 "redundancy_bits_per_letter": {
  "q": 1.785,
  "q10": 1.474,
  "S1": 3.112,
  "S0": 3.967
 },
 "evidence_in_73_letters_bits": {
  "q": 130.3,
  "q10": 107.6,
  "S1": 227.1,
  "S0": 289.6
 },
 "known_letters_fix_bits": 112.8,
 "symmetries_removed_bits": {
  "one alphabet": 8.29,
  "two alphabets": 12.99
 },
 "gl_bits": {
  "4x4": 73.4,
  "5x5": 115.6
 },
 "cells": [
  {
   "item": "F1.1",
   "cell": "one free alphabet, Beaufort form, key length 23",
   "key_bits": 188.2,
   "open_bits": 75.4,
   "margin_q": 54.9,
   "margin_S1": 151.7,
   "margin_S0": 214.2,
   "decidable_by": "quadgram",
   "letters_needed_q": 42.2
  },
  {
   "item": "F1.1",
   "cell": "one free alphabet, Beaufort form, key length 26",
   "key_bits": 202.3,
   "open_bits": 89.5,
   "margin_q": 40.8,
   "margin_S1": 137.6,
   "margin_S0": 200.1,
   "decidable_by": "quadgram",
   "letters_needed_q": 50.1
  },
  {
   "item": "F1.2",
   "cell": "two free alphabets, key length 8",
   "key_bits": 201.4,
   "open_bits": 88.6,
   "margin_q": 41.7,
   "margin_S1": 138.6,
   "margin_S0": 201.0,
   "decidable_by": "quadgram",
   "letters_needed_q": 49.6
  },
  {
   "item": "F1.2",
   "cell": "two free alphabets, key length 13",
   "key_bits": 224.9,
   "open_bits": 112.1,
   "margin_q": 18.2,
   "margin_S1": 115.1,
   "margin_S0": 177.5,
   "decidable_by": "quadgram",
   "letters_needed_q": 62.8
  },
  {
   "item": "F1.2",
   "cell": "two free alphabets, key length 16",
   "key_bits": 239.0,
   "open_bits": 126.2,
   "margin_q": 4.1,
   "margin_S1": 101.0,
   "margin_S0": 163.4,
   "decidable_by": "quadgram",
   "letters_needed_q": 70.7
  },
  {
   "item": "F1.2",
   "cell": "two free alphabets, key length 19",
   "key_bits": 253.1,
   "open_bits": 140.3,
   "margin_q": -10.0,
   "margin_S1": 86.9,
   "margin_S0": 149.3,
   "decidable_by": "better model",
   "letters_needed_q": 78.6
  },
  {
   "item": "F1.2",
   "cell": "two free alphabets, key length 20",
   "key_bits": 257.8,
   "open_bits": 145.0,
   "margin_q": -14.7,
   "margin_S1": 82.2,
   "margin_S0": 144.6,
   "decidable_by": "better model",
   "letters_needed_q": 81.2
  },
  {
   "item": "F1.2",
   "cell": "two free alphabets, key length 23",
   "key_bits": 271.9,
   "open_bits": 159.1,
   "margin_q": -28.8,
   "margin_S1": 68.1,
   "margin_S0": 130.5,
   "decidable_by": "better model",
   "letters_needed_q": 89.1
  },
  {
   "item": "F1.2",
   "cell": "two free alphabets, key length 24",
   "key_bits": 276.6,
   "open_bits": 163.8,
   "margin_q": -33.5,
   "margin_S1": 63.4,
   "margin_S0": 125.8,
   "decidable_by": "better model",
   "letters_needed_q": 91.8
  },
  {
   "item": "F1.2",
   "cell": "two free alphabets, key length 26",
   "key_bits": 286.0,
   "open_bits": 173.2,
   "margin_q": -42.9,
   "margin_S1": 54.0,
   "margin_S0": 116.4,
   "decidable_by": "better model",
   "letters_needed_q": 97.0
  },
  {
   "item": "F1.4",
   "cell": "hand schedule, one free alphabet, keyword of 5",
   "key_bits": 116.9,
   "open_bits": 4.1,
   "margin_q": 126.2,
   "margin_S1": 223.1,
   "margin_S0": 285.5,
   "decidable_by": "quadgram",
   "letters_needed_q": 2.3
  },
  {
   "item": "F1.4",
   "cell": "hand schedule, two free alphabets, keyword of 5",
   "key_bits": 199.6,
   "open_bits": 86.8,
   "margin_q": 43.5,
   "margin_S1": 140.4,
   "margin_S0": 202.8,
   "decidable_by": "quadgram",
   "letters_needed_q": 48.6
  },
  {
   "item": "F1.4",
   "cell": "hand schedule, one free alphabet, keyword of 10",
   "key_bits": 140.4,
   "open_bits": 27.6,
   "margin_q": 102.7,
   "margin_S1": 199.5,
   "margin_S0": 262.0,
   "decidable_by": "quadgram",
   "letters_needed_q": 15.5
  },
  {
   "item": "F1.4",
   "cell": "hand schedule, two free alphabets, keyword of 10",
   "key_bits": 223.1,
   "open_bits": 110.3,
   "margin_q": 20.0,
   "margin_S1": 116.9,
   "margin_S0": 179.3,
   "decidable_by": "quadgram",
   "letters_needed_q": 61.8
  },
  {
   "item": "F1.4",
   "cell": "hand schedule, one free alphabet, keyword of 15",
   "key_bits": 163.9,
   "open_bits": 51.1,
   "margin_q": 79.2,
   "margin_S1": 176.0,
   "margin_S0": 238.5,
   "decidable_by": "quadgram",
   "letters_needed_q": 28.6
  },
  {
   "item": "F1.4",
   "cell": "hand schedule, two free alphabets, keyword of 15",
   "key_bits": 246.6,
   "open_bits": 133.8,
   "margin_q": -3.5,
   "margin_S1": 93.4,
   "margin_S0": 155.8,
   "decidable_by": "better model",
   "letters_needed_q": 75.0
  },
  {
   "item": "F1.4",
   "cell": "hand schedule, one free alphabet, keyword of 20",
   "key_bits": 187.4,
   "open_bits": 74.6,
   "margin_q": 55.7,
   "margin_S1": 152.5,
   "margin_S0": 215.0,
   "decidable_by": "quadgram",
   "letters_needed_q": 41.8
  },
  {
   "item": "F1.4",
   "cell": "hand schedule, two free alphabets, keyword of 20",
   "key_bits": 270.1,
   "open_bits": 157.3,
   "margin_q": -27.0,
   "margin_S1": 69.9,
   "margin_S0": 132.3,
   "decidable_by": "better model",
   "letters_needed_q": 88.1
  },
  {
   "item": "F1.4",
   "cell": "hand schedule, one free alphabet, keyword of 26",
   "key_bits": 215.6,
   "open_bits": 102.8,
   "margin_q": 27.5,
   "margin_S1": 124.3,
   "margin_S0": 186.8,
   "decidable_by": "quadgram",
   "letters_needed_q": 57.6
  },
  {
   "item": "F1.4",
   "cell": "hand schedule, two free alphabets, keyword of 26",
   "key_bits": 298.3,
   "open_bits": 185.5,
   "margin_q": -55.2,
   "margin_S1": 41.7,
   "margin_S0": 104.1,
   "decidable_by": "better model",
   "letters_needed_q": 103.9
  },
  {
   "item": "F1.4",
   "cell": "hand schedule, one free alphabet, keyword of 31",
   "key_bits": 239.1,
   "open_bits": 126.3,
   "margin_q": 4.0,
   "margin_S1": 100.8,
   "margin_S0": 163.3,
   "decidable_by": "quadgram",
   "letters_needed_q": 70.8
  },
  {
   "item": "F1.4",
   "cell": "hand schedule, two free alphabets, keyword of 31",
   "key_bits": 321.8,
   "open_bits": 209.0,
   "margin_q": -78.7,
   "margin_S1": 18.2,
   "margin_S0": 80.6,
   "decidable_by": "better model",
   "letters_needed_q": 117.1
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 53, one of 8 tables",
   "key_bits": 252.1,
   "open_bits": 139.3,
   "margin_q": -9.0,
   "margin_S1": 87.8,
   "margin_S0": 150.3,
   "decidable_by": "better model",
   "letters_needed_q": 78.1
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 54, one of 8 tables",
   "key_bits": 256.8,
   "open_bits": 144.0,
   "margin_q": -13.7,
   "margin_S1": 83.1,
   "margin_S0": 145.6,
   "decidable_by": "better model",
   "letters_needed_q": 80.7
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 55, one of 8 tables",
   "key_bits": 261.5,
   "open_bits": 148.7,
   "margin_q": -18.4,
   "margin_S1": 78.4,
   "margin_S0": 140.9,
   "decidable_by": "better model",
   "letters_needed_q": 83.3
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 56, one of 8 tables",
   "key_bits": 266.2,
   "open_bits": 153.4,
   "margin_q": -23.1,
   "margin_S1": 73.7,
   "margin_S0": 136.2,
   "decidable_by": "better model",
   "letters_needed_q": 86.0
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 57, one of 8 tables",
   "key_bits": 270.9,
   "open_bits": 158.1,
   "margin_q": -27.8,
   "margin_S1": 69.0,
   "margin_S0": 131.5,
   "decidable_by": "better model",
   "letters_needed_q": 88.6
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 58, one of 8 tables",
   "key_bits": 275.6,
   "open_bits": 162.8,
   "margin_q": -32.5,
   "margin_S1": 64.3,
   "margin_S0": 126.8,
   "decidable_by": "better model",
   "letters_needed_q": 91.2
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 59, one of 8 tables",
   "key_bits": 280.3,
   "open_bits": 167.5,
   "margin_q": -37.2,
   "margin_S1": 59.6,
   "margin_S0": 122.1,
   "decidable_by": "better model",
   "letters_needed_q": 93.9
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 60, one of 8 tables",
   "key_bits": 285.0,
   "open_bits": 172.2,
   "margin_q": -41.9,
   "margin_S1": 54.9,
   "margin_S0": 117.4,
   "decidable_by": "better model",
   "letters_needed_q": 96.5
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 61, one of 8 tables",
   "key_bits": 289.7,
   "open_bits": 176.9,
   "margin_q": -46.6,
   "margin_S1": 50.2,
   "margin_S0": 112.7,
   "decidable_by": "better model",
   "letters_needed_q": 99.1
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 62, one of 8 tables",
   "key_bits": 294.4,
   "open_bits": 181.6,
   "margin_q": -51.3,
   "margin_S1": 45.5,
   "margin_S0": 108.0,
   "decidable_by": "better model",
   "letters_needed_q": 101.8
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 63, one of 8 tables",
   "key_bits": 299.1,
   "open_bits": 186.3,
   "margin_q": -56.0,
   "margin_S1": 40.8,
   "margin_S0": 103.3,
   "decidable_by": "better model",
   "letters_needed_q": 104.4
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 64, one of 8 tables",
   "key_bits": 303.8,
   "open_bits": 191.0,
   "margin_q": -60.7,
   "margin_S1": 36.1,
   "margin_S0": 98.6,
   "decidable_by": "better model",
   "letters_needed_q": 107.0
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 65, one of 8 tables",
   "key_bits": 308.5,
   "open_bits": 195.7,
   "margin_q": -65.4,
   "margin_S1": 31.4,
   "margin_S0": 93.9,
   "decidable_by": "better model",
   "letters_needed_q": 109.7
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 66, one of 8 tables",
   "key_bits": 313.2,
   "open_bits": 200.4,
   "margin_q": -70.1,
   "margin_S1": 26.7,
   "margin_S0": 89.2,
   "decidable_by": "better model",
   "letters_needed_q": 112.3
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 67, one of 8 tables",
   "key_bits": 317.9,
   "open_bits": 205.1,
   "margin_q": -74.8,
   "margin_S1": 22.0,
   "margin_S0": 84.5,
   "decidable_by": "better model",
   "letters_needed_q": 114.9
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 68, one of 8 tables",
   "key_bits": 322.6,
   "open_bits": 209.8,
   "margin_q": -79.5,
   "margin_S1": 17.3,
   "margin_S0": 79.8,
   "decidable_by": "better model",
   "letters_needed_q": 117.6
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 69, one of 8 tables",
   "key_bits": 327.3,
   "open_bits": 214.5,
   "margin_q": -84.2,
   "margin_S1": 12.6,
   "margin_S0": 75.1,
   "decidable_by": "better model",
   "letters_needed_q": 120.2
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 70, one of 8 tables",
   "key_bits": 332.0,
   "open_bits": 219.2,
   "margin_q": -88.9,
   "margin_S1": 7.9,
   "margin_S0": 70.4,
   "decidable_by": "better model",
   "letters_needed_q": 122.8
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 71, one of 8 tables",
   "key_bits": 336.7,
   "open_bits": 223.9,
   "margin_q": -93.6,
   "margin_S1": 3.2,
   "margin_S0": 65.7,
   "decidable_by": "better model",
   "letters_needed_q": 125.5
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 72, one of 8 tables",
   "key_bits": 341.4,
   "open_bits": 228.6,
   "margin_q": -98.3,
   "margin_S1": -1.5,
   "margin_S0": 61.0,
   "decidable_by": "better model",
   "letters_needed_q": 128.1
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 73, one of 8 tables",
   "key_bits": 346.1,
   "open_bits": 233.3,
   "margin_q": -103.0,
   "margin_S1": -6.2,
   "margin_S0": 56.3,
   "decidable_by": "better model",
   "letters_needed_q": 130.7
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 74, one of 8 tables",
   "key_bits": 350.8,
   "open_bits": 238.0,
   "margin_q": -107.7,
   "margin_S1": -10.9,
   "margin_S0": 51.6,
   "decidable_by": "better model",
   "letters_needed_q": 133.4
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 75, one of 8 tables",
   "key_bits": 355.5,
   "open_bits": 242.7,
   "margin_q": -112.4,
   "margin_S1": -15.6,
   "margin_S0": 46.9,
   "decidable_by": "better model",
   "letters_needed_q": 136.0
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 76, one of 8 tables",
   "key_bits": 360.2,
   "open_bits": 247.4,
   "margin_q": -117.1,
   "margin_S1": -20.3,
   "margin_S0": 42.2,
   "decidable_by": "better model",
   "letters_needed_q": 138.6
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 77, one of 8 tables",
   "key_bits": 364.9,
   "open_bits": 252.1,
   "margin_q": -121.8,
   "margin_S1": -25.0,
   "margin_S0": 37.5,
   "decidable_by": "better model",
   "letters_needed_q": 141.3
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 78, one of 8 tables",
   "key_bits": 369.6,
   "open_bits": 256.8,
   "margin_q": -126.5,
   "margin_S1": -29.7,
   "margin_S0": 32.8,
   "decidable_by": "better model",
   "letters_needed_q": 143.9
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 79, one of 8 tables",
   "key_bits": 374.3,
   "open_bits": 261.5,
   "margin_q": -131.2,
   "margin_S1": -34.4,
   "margin_S0": 28.1,
   "decidable_by": "better model",
   "letters_needed_q": 146.5
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 80, one of 8 tables",
   "key_bits": 379.0,
   "open_bits": 266.2,
   "margin_q": -135.9,
   "margin_S1": -39.1,
   "margin_S0": 23.4,
   "decidable_by": "better model",
   "letters_needed_q": 149.2
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 81, one of 8 tables",
   "key_bits": 383.7,
   "open_bits": 270.9,
   "margin_q": -140.6,
   "margin_S1": -43.8,
   "margin_S0": 18.7,
   "decidable_by": "better model",
   "letters_needed_q": 151.8
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 82, one of 8 tables",
   "key_bits": 388.4,
   "open_bits": 275.6,
   "margin_q": -145.3,
   "margin_S1": -48.5,
   "margin_S0": 14.0,
   "decidable_by": "better model",
   "letters_needed_q": 154.4
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 83, one of 8 tables",
   "key_bits": 393.1,
   "open_bits": 280.3,
   "margin_q": -150.0,
   "margin_S1": -53.2,
   "margin_S0": 9.3,
   "decidable_by": "better model",
   "letters_needed_q": 157.1
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 84, one of 8 tables",
   "key_bits": 397.8,
   "open_bits": 285.0,
   "margin_q": -154.7,
   "margin_S1": -57.9,
   "margin_S0": 4.6,
   "decidable_by": "better model",
   "letters_needed_q": 159.7
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 85, one of 8 tables",
   "key_bits": 402.5,
   "open_bits": 289.7,
   "margin_q": -159.4,
   "margin_S1": -62.6,
   "margin_S0": -0.1,
   "decidable_by": "none",
   "letters_needed_q": 162.3
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 86, one of 8 tables",
   "key_bits": 407.2,
   "open_bits": 294.4,
   "margin_q": -164.1,
   "margin_S1": -67.3,
   "margin_S0": -4.8,
   "decidable_by": "none",
   "letters_needed_q": 165.0
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 87, one of 8 tables",
   "key_bits": 411.9,
   "open_bits": 299.1,
   "margin_q": -168.8,
   "margin_S1": -72.0,
   "margin_S0": -9.5,
   "decidable_by": "none",
   "letters_needed_q": 167.6
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 88, one of 8 tables",
   "key_bits": 416.6,
   "open_bits": 303.8,
   "margin_q": -173.5,
   "margin_S1": -76.7,
   "margin_S0": -14.2,
   "decidable_by": "none",
   "letters_needed_q": 170.2
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 89, one of 8 tables",
   "key_bits": 421.3,
   "open_bits": 308.5,
   "margin_q": -178.2,
   "margin_S1": -81.4,
   "margin_S0": -18.9,
   "decidable_by": "none",
   "letters_needed_q": 172.9
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 90, one of 8 tables",
   "key_bits": 426.0,
   "open_bits": 313.2,
   "margin_q": -182.9,
   "margin_S1": -86.1,
   "margin_S0": -23.6,
   "decidable_by": "none",
   "letters_needed_q": 175.5
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 91, one of 8 tables",
   "key_bits": 430.7,
   "open_bits": 317.9,
   "margin_q": -187.6,
   "margin_S1": -90.8,
   "margin_S0": -28.3,
   "decidable_by": "none",
   "letters_needed_q": 178.1
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 92, one of 8 tables",
   "key_bits": 435.4,
   "open_bits": 322.6,
   "margin_q": -192.3,
   "margin_S1": -95.5,
   "margin_S0": -33.0,
   "decidable_by": "none",
   "letters_needed_q": 180.8
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 93, one of 8 tables",
   "key_bits": 440.1,
   "open_bits": 327.3,
   "margin_q": -197.0,
   "margin_S1": -100.2,
   "margin_S0": -37.7,
   "decidable_by": "none",
   "letters_needed_q": 183.4
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 94, one of 8 tables",
   "key_bits": 444.8,
   "open_bits": 332.0,
   "margin_q": -201.7,
   "margin_S1": -104.9,
   "margin_S0": -42.4,
   "decidable_by": "none",
   "letters_needed_q": 186.0
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 95, one of 8 tables",
   "key_bits": 449.5,
   "open_bits": 336.7,
   "margin_q": -206.4,
   "margin_S1": -109.6,
   "margin_S0": -47.1,
   "decidable_by": "none",
   "letters_needed_q": 188.7
  },
  {
   "item": "F1 autokey",
   "cell": "plaintext autokey, lag 96, one of 8 tables",
   "key_bits": 454.2,
   "open_bits": 341.4,
   "margin_q": -211.1,
   "margin_S1": -114.3,
   "margin_S0": -51.8,
   "decidable_by": "none",
   "letters_needed_q": 191.3
  },
  {
   "item": "F6.1",
   "cell": "one free alphabet with one of 27,852 moves, either order, key length 6",
   "key_bits": 125.1,
   "open_bits": 12.3,
   "margin_q": 118.0,
   "margin_S1": 214.9,
   "margin_S0": 277.3,
   "decidable_by": "quadgram",
   "letters_needed_q": 6.9
  },
  {
   "item": "F6.1",
   "cell": "one free alphabet with one of 27,852 moves, either order, key length 10",
   "key_bits": 143.9,
   "open_bits": 31.1,
   "margin_q": 99.2,
   "margin_S1": 196.1,
   "margin_S0": 258.5,
   "decidable_by": "quadgram",
   "letters_needed_q": 17.4
  },
  {
   "item": "F6.1",
   "cell": "one free alphabet with one of 27,852 moves, either order, key length 14",
   "key_bits": 162.7,
   "open_bits": 49.9,
   "margin_q": 80.4,
   "margin_S1": 177.3,
   "margin_S0": 239.7,
   "decidable_by": "quadgram",
   "letters_needed_q": 27.9
  },
  {
   "item": "F6.1",
   "cell": "one free alphabet with one of 27,852 moves, either order, key length 18",
   "key_bits": 181.5,
   "open_bits": 68.7,
   "margin_q": 61.6,
   "margin_S1": 158.5,
   "margin_S0": 220.9,
   "decidable_by": "quadgram",
   "letters_needed_q": 38.5
  },
  {
   "item": "F6.1",
   "cell": "one free alphabet with one of 27,852 moves, either order, key length 22",
   "key_bits": 200.3,
   "open_bits": 87.5,
   "margin_q": 42.8,
   "margin_S1": 139.7,
   "margin_S0": 202.1,
   "decidable_by": "quadgram",
   "letters_needed_q": 49.0
  },
  {
   "item": "F6.1",
   "cell": "one free alphabet with one of 27,852 moves, either order, key length 26",
   "key_bits": 219.1,
   "open_bits": 106.3,
   "margin_q": 24.0,
   "margin_S1": 120.9,
   "margin_S0": 183.3,
   "decidable_by": "quadgram",
   "letters_needed_q": 59.5
  },
  {
   "item": "F6.2",
   "cell": "two free alphabets with one of 27,852 moves, either order, key length 3",
   "key_bits": 193.6,
   "open_bits": 80.8,
   "margin_q": 49.5,
   "margin_S1": 146.3,
   "margin_S0": 208.8,
   "decidable_by": "quadgram",
   "letters_needed_q": 45.3
  },
  {
   "item": "F6.2",
   "cell": "two free alphabets with one of 27,852 moves, either order, key length 6",
   "key_bits": 207.7,
   "open_bits": 94.9,
   "margin_q": 35.4,
   "margin_S1": 132.2,
   "margin_S0": 194.7,
   "decidable_by": "quadgram",
   "letters_needed_q": 53.2
  },
  {
   "item": "F6.2",
   "cell": "two free alphabets with one of 27,852 moves, either order, key length 10",
   "key_bits": 226.5,
   "open_bits": 113.7,
   "margin_q": 16.6,
   "margin_S1": 113.4,
   "margin_S0": 175.9,
   "decidable_by": "quadgram",
   "letters_needed_q": 63.7
  },
  {
   "item": "F6.2",
   "cell": "two free alphabets with one of 27,852 moves, either order, key length 12",
   "key_bits": 235.9,
   "open_bits": 123.1,
   "margin_q": 7.2,
   "margin_S1": 104.0,
   "margin_S0": 166.5,
   "decidable_by": "quadgram",
   "letters_needed_q": 69.0
  },
  {
   "item": "F6.2",
   "cell": "two free alphabets with one of 27,852 moves, either order, key length 14",
   "key_bits": 245.3,
   "open_bits": 132.5,
   "margin_q": -2.3,
   "margin_S1": 94.6,
   "margin_S0": 157.1,
   "decidable_by": "better model",
   "letters_needed_q": 74.3
  },
  {
   "item": "F6.2",
   "cell": "two free alphabets with one of 27,852 moves, either order, key length 15",
   "key_bits": 250.1,
   "open_bits": 137.2,
   "margin_q": -7.0,
   "margin_S1": 89.9,
   "margin_S0": 152.4,
   "decidable_by": "better model",
   "letters_needed_q": 76.9
  },
  {
   "item": "F6.2",
   "cell": "two free alphabets with one of 27,852 moves, either order, key length 18",
   "key_bits": 264.2,
   "open_bits": 151.3,
   "margin_q": -21.1,
   "margin_S1": 75.8,
   "margin_S0": 138.3,
   "decidable_by": "better model",
   "letters_needed_q": 84.8
  },
  {
   "item": "F6.2",
   "cell": "two free alphabets with one of 27,852 moves, either order, key length 22",
   "key_bits": 283.0,
   "open_bits": 170.1,
   "margin_q": -39.9,
   "margin_S1": 57.0,
   "margin_S0": 119.5,
   "decidable_by": "better model",
   "letters_needed_q": 95.3
  },
  {
   "item": "F6.2",
   "cell": "two free alphabets with one of 27,852 moves, either order, key length 26",
   "key_bits": 301.8,
   "open_bits": 188.9,
   "margin_q": -58.7,
   "margin_S1": 38.2,
   "margin_S0": 100.7,
   "decidable_by": "better model",
   "letters_needed_q": 105.9
  },
  {
   "item": "F8",
   "cell": "5x5 affine Hill, four numberings",
   "key_bits": 141.1,
   "open_bits": 28.3,
   "margin_q": 102.0,
   "margin_S1": 198.8,
   "margin_S0": 261.3,
   "decidable_by": "quadgram",
   "letters_needed_q": 15.9
  },
  {
   "item": "F8",
   "cell": "4x4 Hill with a periodic key of 1, either order, four numberings",
   "key_bits": 81.1,
   "open_bits": -31.7,
   "margin_q": 162.0,
   "margin_S1": 258.9,
   "margin_S0": 321.3,
   "decidable_by": "quadgram",
   "letters_needed_q": 0.0
  },
  {
   "item": "F8",
   "cell": "4x4 Hill with a periodic key of 8, either order, four numberings",
   "key_bits": 114.0,
   "open_bits": 1.2,
   "margin_q": 129.1,
   "margin_S1": 226.0,
   "margin_S0": 288.4,
   "decidable_by": "quadgram",
   "letters_needed_q": 0.7
  },
  {
   "item": "F8",
   "cell": "4x4 Hill with a periodic key of 13, either order, four numberings",
   "key_bits": 137.5,
   "open_bits": 24.7,
   "margin_q": 105.6,
   "margin_S1": 202.5,
   "margin_S0": 264.9,
   "decidable_by": "quadgram",
   "letters_needed_q": 13.8
  },
  {
   "item": "F8",
   "cell": "4x4 Hill with a periodic key of 20, either order, four numberings",
   "key_bits": 170.4,
   "open_bits": 57.6,
   "margin_q": 72.7,
   "margin_S1": 169.6,
   "margin_S0": 232.0,
   "decidable_by": "quadgram",
   "letters_needed_q": 32.3
  },
  {
   "item": "F8",
   "cell": "4x4 Hill with a periodic key of 26, either order, four numberings",
   "key_bits": 198.6,
   "open_bits": 85.8,
   "margin_q": 44.5,
   "margin_S1": 141.4,
   "margin_S0": 203.8,
   "decidable_by": "quadgram",
   "letters_needed_q": 48.1
  }
 ],
 "autokey_lags": {
  "quadgram_decidable": [],
  "over_shannon_upper_estimate": [
   72,
   73,
   74,
   75,
   76,
   77,
   78,
   79,
   80,
   81,
   82,
   83,
   84,
   85,
   86,
   87,
   88,
   89,
   90,
   91,
   92,
   93,
   94,
   95,
   96
  ],
  "over_every_estimate": [
   85,
   86,
   87,
   88,
   89,
   90,
   91,
   92,
   93,
   94,
   95,
   96
  ]
 },
 "rule": "decidable by an English test with redundancy D only if open bits < 73 D (necessary, not sufficient for a search)",
 "exhaustive": true
}
```

Notes: quadgram cross-entropy 2.916 bits/letter on Carter (2.944 on K1-K3), D(q) 1.78, 73 letters carry 130 bits (S1 227, S0 290); cells by decider: quadgram 29, better model 46, none 12


