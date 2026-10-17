# 0178-misspelt-letters-positions-as-numbers: F3.5: the misspelt letters' positions (IQLUSION, UNDERGRUUND, DESPARATLY, the missing E, the raised YAR) and their shifts as the number half of a two-part key, exact

**Family:** 3-two-component-key  
**Parent:** 0175-morse-and-plate-numbers-as-key  
**Decision:** reverted  
**Run:** 2026-10-17T00:24:46+00:00, 1.7 s, status ran  
**Time by phase:** design 0 s, implement 0 s, test 0 s, run 2 s, record 0 s

## In plain words

Sanborn said the misspellings matter for where the letters sit, not what they are. So we take where they sit, as numbers: the Q is the 2nd letter of IQLUSION and the 57th of K1, and so on, and try those numbers as half of the key with a secret word as the other half, on K4 and on scrambled copies.

## Walkthrough, by hand

1. Write 2 8 5 (the wrong letters' places in IQLUSION, UNDERGRUUND, DESPARATLY) again and again under the message.
2. On the sculpture's table the known E at place 22 over the carved F asks for key value 1.
3. Subtract the number under place 22: the rest is the secret word's letter for that slot.
4. Places sharing a slot of the word must leave the same rest.
5. Every start, sign, word length and table rule; then scrambled copies.

## Worked example (generated)

```
2 8 5 (the misspelt letters' places in their words) from the first number, Vigenere on the KRYPTOS table, word length 7

place  known  carved  key  num  word value  slot
   22      E       F    1    2          25     0
   23      A       L   10    8           2     1
   24      S       R   21    5          16     2
   25      T       V   18    2          16     3
   26      N       Q    1    8          19     4
   27      O       Q   15    5          10     5
   28      R       P    2    2           0     6
   29      T       R   23    8          15     0
   30      H       N    5    5           0     1
   31      E       G    2    2           0     2
   32      A       K   19    8          11     3
   33      S       S    0    5          21     4
   34      T       S    2    2           0     5
   64      B       N   11    2           9     0
   65      E       Y   17    8           9     1
   66      R       P    2    5          23     2
   67      L       V    5    2           3     3
   68      I       T   15    8           7     4
   69      N       T   11    5           6     5
   70      C       M    9    2           7     6
   71      L       Z    8    8           0     0
   72      O       F    7    5           2     1
   73      C       P   20    2          18     2
   74      K       K    0    8          18     3
```

## Lineage

Inherits from 0175-morse-and-plate-numbers-as-key. What changed: F3.5 (C10(a), C10(c)). 0061 used the misspelt letters themselves (QUA, LOE) as a short second key. Here their positions are the numbers: the place of the wrong letter in its word (2, 8, 5; the missing E at 9), in its plaintext (57, 115, 11; E at 15), and counted through K1-K3 (57, 178, 443; E 447); the raised Y, A, R at places 4, 5, 7 of their line; the shift each misspelling makes (L to Q, O to U, E to A) on the standard and KRYPTOS orders; the letters as numbers; RQ and its upside-down YR; Bauer's error coordinates (25,2) (24,6) (11,15) (15,15). Each forward and reversed, with an unknown word of 1-24 letters, every start, both signs, 12 table rules (0175's decider).

## Hypothesis (domain expert)

C10: 'it's more the orientation of those letters that's useful there... the positioning' (Sanborn 2003); (a) positions as indices, (b) Bauer's coordinates, (c) orientation. C5(b), C6. Model as 0175: k_i = w[i mod a] + s d[(i + o) mod m], 12 rules; the 24 known letters force k; the word's slots must agree. Statistic: live settings and dictionary words, K4 against 20 coppers. Index readings into the tableau as a short key are any periodic key of length 3-4 on the sculpture's tables, which 0005 already excludes.

## Prediction

No setting fits K4 or the coppers (5 or more checks each). Zero candidates.

## Method

1. Build the position readings.
2. For each text, table rule, reading, start and sign: the word's value at each known place.
3. For each word length 1-24: slot agreement; fully forced words looked up.
4. K4 against 20 coppers; one planted text as a builder check.

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
 "family": "word plus the misspelt letters' positions and shifts as numbers, k = w[i mod a] + s d, 12 table rules, exact",
 "readings": {
  "place in the word: Q, U, A": [
   2,
   8,
   5
  ],
  "place in the word: Q, U, A, reversed": [
   5,
   8,
   2
  ],
  "place in the word: Q, U, A, missing E": [
   2,
   8,
   5,
   9
  ],
  "place in the word: Q, U, A, missing E, reversed": [
   9,
   5,
   8,
   2
  ],
  "place in its plaintext: 57, 115, 11": [
   57,
   115,
   11
  ],
  "place in its plaintext: 57, 115, 11, reversed": [
   11,
   115,
   57
  ],
  "place in its plaintext with E: 57, 115, 11, 15": [
   57,
   115,
   11,
   15
  ],
  "place in its plaintext with E: 57, 115, 11, 15, reversed": [
   15,
   11,
   115,
   57
  ],
  "place through K1-K3: 57, 178, 443": [
   57,
   178,
   443
  ],
  "place through K1-K3: 57, 178, 443, reversed": [
   443,
   178,
   57
  ],
  "place through K1-K3 with E: 57, 178, 443, 447": [
   57,
   178,
   443,
   447
  ],
  "place through K1-K3 with E: 57, 178, 443, 447, reversed": [
   447,
   443,
   178,
   57
  ],
  "raised YAR, places in the line: 4 5 7": [
   4,
   5,
   7
  ],
  "raised YAR, places in the line: 4 5 7, reversed": [
   7,
   5,
   4
  ],
  "QUA as numbers, standard": [
   16,
   20,
   0
  ],
  "QUA as numbers, standard, reversed": [
   0,
   20,
   16
  ],
  "QUA as numbers, KRYPTOS": [
   20,
   21,
   7
  ],
  "QUA as numbers, KRYPTOS, reversed": [
   7,
   21,
   20
  ],
  "LOE as numbers, standard": [
   11,
   14,
   4
  ],
  "LOE as numbers, standard, reversed": [
   4,
   14,
   11
  ],
  "LOE as numbers, KRYPTOS": [
   17,
   5,
   11
  ],
  "LOE as numbers, KRYPTOS, reversed": [
   11,
   5,
   17
  ],
  "shifts L>Q, O>U, E>A, standard": [
   5,
   6,
   22
  ],
  "shifts L>Q, O>U, E>A, standard, reversed": [
   22,
   6,
   5
  ],
  "shifts L>Q, O>U, E>A, KRYPTOS": [
   3,
   16,
   22
  ],
  "shifts L>Q, O>U, E>A, KRYPTOS, reversed": [
   22,
   16,
   3
  ],
  "YAR as numbers, standard": [
   24,
   0,
   17
  ],
  "YAR as numbers, standard, reversed": [
   17,
   0,
   24
  ],
  "YAR as numbers, KRYPTOS": [
   2,
   7,
   1
  ],
  "YAR as numbers, KRYPTOS, reversed": [
   1,
   7,
   2
  ],
  "RQ, standard": [
   17,
   16
  ],
  "RQ, standard, reversed": [
   16,
   17
  ],
  "YR (RQ upside down), standard": [
   24,
   17
  ],
  "YR (RQ upside down), standard, reversed": [
   17,
   24
  ],
  "RQ, KRYPTOS": [
   1,
   20
  ],
  "RQ, KRYPTOS, reversed": [
   20,
   1
  ],
  "YR, KRYPTOS": [
   2,
   1
  ],
  "YR, KRYPTOS, reversed": [
   1,
   2
  ],
  "Bauer's error coordinates (25,2)(24,6)(11,15)(15,15)": [
   25,
   2,
   24,
   6,
   11,
   15,
   15,
   15
  ],
  "Bauer's error coordinates (25,2)(24,6)(11,15)(15,15), reversed": [
   15,
   15,
   15,
   11,
   6,
   24,
   2,
   25
  ]
 },
 "n_readings": 40,
 "word_lengths": [
  1,
  24
 ],
 "checks_by_word_length": {
  "1": 23,
  "2": 22,
  "3": 21,
  "4": 20,
  "5": 19,
  "6": 18,
  "7": 17,
  "8": 16,
  "9": 15,
  "10": 14,
  "11": 13,
  "12": 12,
  "13": 11,
  "14": 11,
  "15": 9,
  "16": 8,
  "17": 7,
  "18": 7,
  "19": 9,
  "20": 11,
  "21": 11,
  "22": 9,
  "23": 7,
  "24": 5
 },
 "live_at_least_checks": {
  "1": {
   "k4": 0,
   "coppers_min": 0,
   "coppers_max": 0,
   "coppers_at_or_above_k4": 20
  },
  "2": {
   "k4": 0,
   "coppers_min": 0,
   "coppers_max": 0,
   "coppers_at_or_above_k4": 20
  },
  "4": {
   "k4": 0,
   "coppers_min": 0,
   "coppers_max": 0,
   "coppers_at_or_above_k4": 20
  },
  "6": {
   "k4": 0,
   "coppers_min": 0,
   "coppers_max": 0,
   "coppers_at_or_above_k4": 20
  },
  "8": {
   "k4": 0,
   "coppers_min": 0,
   "coppers_max": 0,
   "coppers_at_or_above_k4": 20
  },
  "11": {
   "k4": 0,
   "coppers_min": 0,
   "coppers_max": 0,
   "coppers_at_or_above_k4": 20
  },
  "14": {
   "k4": 0,
   "coppers_min": 0,
   "coppers_max": 0,
   "coppers_at_or_above_k4": 20
  }
 },
 "dictionary_hits": {
  "k4": 0,
  "coppers": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ]
 },
 "dictionary_hits_6_plus": {
  "k4": 0,
  "coppers": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ]
 },
 "k4_hits": [],
 "plant": {
  "text": "2 8 5 from the second number, + SHADOW, Vigenere on the KRYPTOS table",
  "found": true
 },
 "copies": "20 shuffled coppers (seed 1780)",
 "seconds": 2,
 "exhaustive": true
}
```

Notes: live settings with >=4 checks: K4 0 (coppers 0-0); dictionary words 4+: K4 0 (coppers 0-0); plant found True


