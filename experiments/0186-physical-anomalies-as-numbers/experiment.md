# 0186-physical-anomalies-as-numbers: F4.3: the places of the copper's physical anomalies (the four ?, K2's omitted letter, the raised YAR, the extra L, the long and short lines) as the number half of a two-part key, exact

**Family:** 4-sanborn-visual  
**Parent:** 0175-morse-and-plate-numbers-as-key  
**Decision:** reverted  
**Run:** 2026-10-17T00:37:43+00:00, 1.7 s, status ran  
**Time by phase:** design 0 s, implement 0 s, test 0 s, run 2 s, record 0 s

## In plain words

The copper has oddities: question marks, a letter left out of K2, three raised letters, an extra L on the alphabet side, lines longer or shorter than the rest. Where they sit could be a list of numbers that is half the key, a secret word the other half. The 24 known letters say whether any word fits.

## Walkthrough, by hand

1. List the anomalies in carved order: ? at 101, ? at 227, ? at 289, the missing S after 427, Y A R at 439 440 442, ? at 772.
2. Repeat those numbers under the message from some start.
3. On the sculpture's table the known E at place 22 over the carved F asks for key value 1; subtract the number under it: the rest is the secret word's letter there.
4. Places sharing a slot of the word must agree.
5. Every start, sign, word length, table rule and reading; then scrambled copies.

## Worked example (generated)

```
the anomaly places from the first, Vigenere on the KRYPTOS table, word length 7

place  known  carved  key  num  word value  slot
   22      E       F    1  440           3     0
   23      A       L   10  442          10     1
   24      S       R   21  772           3     2
   25      T       V   18  101          21     3
   26      N       Q    1  227           8     4
   27      O       Q   15  289          12     5
   28      R       P    2  428          16     6
   29      T       R   23  439           0     0
   30      H       N    5  440           7     1
   31      E       G    2  442           2     2
   32      A       K   19  772           1     3
   33      S       S    0  101           3     4
   34      T       S    2  227           9     5
   64      B       N   11  772          19     0
   65      E       Y   17  101          20     1
   66      R       P    2  227           9     2
   67      L       V    5  289           2     3
   68      I       T   15  428           3     4
   69      N       T   11  439          14     5
   70      C       M    9  440          11     6
   71      L       Z    8  442           8     0
   72      O       F    7  772          15     1
   73      C       P   20  101          23     2
   74      K       K    0  227           7     3
```

## Lineage

Inherits from 0175-morse-and-plate-numbers-as-key. What changed: F4.3 (C3(c)). The anomalies on the copper, located from the transcript (knowledge/01-facts.md): the four ? at places 101, 227, 289, 772 of the left side; K2's omitted S between places 427 and 428 (end of line 14); the raised Y, A, R at 439, 440, 442 (line 15, columns 4, 5, 7); the extra L at the end of the tableau's line 15 (column 32, first line of the lower-right plate); the 33- and 29-letter lines (23 and 24). Readings: all of them as places in carved order, as line numbers, as columns, the gaps between them, the first-line markers (YAR columns and the L's column), each forward and reversed. With an unknown word of 1-24 letters, every start, both signs, 12 table rules (0175's decider). 0178 and 0180 already used the ? alone and YAR alone.

## Hypothesis (domain expert)

C3(c): 'I like to use spatial systems of encoding... visual systems' (Sanborn); positions of the physical anomalies as the key. C10 (positioning), C21(b) (the extra L as a marker matching YAR). Model as 0175: k_i = w[i mod a] + s d[(i + o) mod m], 12 rules. Statistic: live settings, K4 against 20 coppers.

## Prediction

No setting fits K4 or the coppers (5 or more checks each). Zero candidates.

## Method

1. Locate the anomalies on the transcript and build the readings.
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
 "family": "word plus the places of the copper's physical anomalies as numbers, k = w[i mod a] + s d, 12 table rules, exact",
 "readings": {
  "anomaly places in carved order (?, ?, ?, missing S, Y, A, R, ?)": [
   101,
   227,
   289,
   428,
   439,
   440,
   442,
   772
  ],
  "anomaly places in carved order (?, ?, ?, missing S, Y, A, R, ?), reversed": [
   772,
   442,
   440,
   439,
   428,
   289,
   227,
   101
  ],
  "anomaly places with the long and short lines' starts": [
   101,
   227,
   289,
   428,
   439,
   440,
   442,
   684,
   717,
   772
  ],
  "anomaly places with the long and short lines' starts, reversed": [
   772,
   717,
   684,
   442,
   440,
   439,
   428,
   289,
   227,
   101
  ],
  "anomaly lines: 4 8 10 14 15 15 15 25": [
   4,
   8,
   10,
   14,
   15,
   15,
   15,
   25
  ],
  "anomaly lines: 4 8 10 14 15 15 15 25, reversed": [
   25,
   15,
   15,
   15,
   14,
   10,
   8,
   4
  ],
  "anomaly columns: 7 9 8 24 4 5 7 27": [
   7,
   9,
   8,
   24,
   4,
   5,
   7,
   27
  ],
  "anomaly columns: 7 9 8 24 4 5 7 27, reversed": [
   27,
   7,
   5,
   4,
   24,
   8,
   9,
   7
  ],
  "gaps between anomaly places": [
   126,
   62,
   139,
   11,
   1,
   2,
   330
  ],
  "gaps between anomaly places, reversed": [
   330,
   2,
   1,
   11,
   139,
   62,
   126
  ],
  "first-line markers: YAR columns and the extra L's column, 4 5 7 32": [
   4,
   5,
   7,
   32
  ],
  "first-line markers: YAR columns and the extra L's column, 4 5 7 32, reversed": [
   32,
   7,
   5,
   4
  ],
  "extra L: tableau line 15, column 32": [
   15,
   32
  ],
  "extra L: tableau line 15, column 32, reversed": [
   32,
   15
  ],
  "extra L as row N: 14 32": [
   14,
   32
  ],
  "extra L as row N: 14 32, reversed": [
   32,
   14
  ],
  "long and short lines: 23 24": [
   23,
   24
  ],
  "long and short lines: 23 24, reversed": [
   24,
   23
  ],
  "long and short line lengths: 33 29": [
   33,
   29
  ],
  "long and short line lengths: 33 29, reversed": [
   29,
   33
  ],
  "all anomaly lines with the long and short lines": [
   4,
   8,
   10,
   14,
   15,
   23,
   24,
   25
  ],
  "all anomaly lines with the long and short lines, reversed": [
   25,
   24,
   23,
   15,
   14,
   10,
   8,
   4
  ]
 },
 "n_readings": 22,
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
  "text": "the anomaly places from the second, + SHADOW, Vigenere on the KRYPTOS table",
  "found": true
 },
 "copies": "20 shuffled coppers (seed 1860)",
 "seconds": 2,
 "exhaustive": true
}
```

Notes: live settings with >=4 checks: K4 0 (coppers 0-0); dictionary words 4+: K4 0 (coppers 0-0); plant found True


