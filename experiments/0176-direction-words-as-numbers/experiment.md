# 0176-direction-words-as-numbers: F3.3: EAST NORTHEAST and its parts read as numbers (bearing 67.5 degrees, compass points of 32 and 16, mils) as the number half of a two-part key, with an unknown word, exact

**Family:** 3-two-component-key  
**Parent:** 0175-morse-and-plate-numbers-as-key  
**Decision:** reverted  
**Run:** 2026-10-16T23:50:45+00:00, 1.7 s, status ran  
**Time by phase:** design 0 s, implement 0 s, test 0 s, run 2 s, record 0 s

## In plain words

The known words are directions. A direction is also a number: east-northeast is 67.5 degrees on a compass, or the 6th of 32 compass points. Perhaps such a number is half of the key and a secret word the other half. For every way of writing these numbers we ask the 24 known letters what the secret word would be, and compare with scrambled copies.

## Walkthrough, by hand

1. Write 6 7 5 (east-northeast is 67.5 degrees) again and again under the message, from some start.
2. On the sculpture's table the known E at place 22 over the carved F asks for key value 1.
3. Subtract the number under place 22: the rest is the secret word's letter for that slot.
4. Places that share a slot of the word must leave the same rest.
5. Every start, sign, word length and table rule; then scrambled copies.

## Worked example (generated)

```
6 7 5 (67.5 degrees) from the first digit, Vigenere on the KRYPTOS table, word length 7

place  known  carved  key  num  word value  slot
   22      E       F    1    6          21     0
   23      A       L   10    7           3     1
   24      S       R   21    5          16     2
   25      T       V   18    6          12     3
   26      N       Q    1    7          20     4
   27      O       Q   15    5          10     5
   28      R       P    2    6          22     6
   29      T       R   23    7          16     0
   30      H       N    5    5           0     1
   31      E       G    2    6          22     2
   32      A       K   19    7          12     3
   33      S       S    0    5          21     4
   34      T       S    2    6          22     5
   64      B       N   11    6           5     0
   65      E       Y   17    7          10     1
   66      R       P    2    5          23     2
   67      L       V    5    6          25     3
   68      I       T   15    7           8     4
   69      N       T   11    5           6     5
   70      C       M    9    6           3     6
   71      L       Z    8    7           1     0
   72      O       F    7    5           2     1
   73      C       P   20    6          14     2
   74      K       K    0    7          19     3
```

## Lineage

Inherits from 0175-morse-and-plate-numbers-as-key. What changed: F3.3 (A14(b)). Same decider as 0175, new readings: the known words' directions as numbers. EAST NORTHEAST as the bearing 67.5 degrees (6 7 5; 0 6 7 5; 67 5; 675; 67 30 as degrees and minutes; 1200 mils), as compass point 6 of 32 or 3 of 16 (and 7, 4 counting from 1), EAST as 90 degrees, point 8 of 32, 4 of 16, NORTHEAST as 45 degrees, 4 of 32, 2 of 16; the pair EAST, NORTHEAST and the triple ENE, E, NE in each scale. Each sequence forward and reversed, every start, both signs, an unknown word of 1-24 letters, 12 table rules. Single numbers are a word shifted by a constant, which 0005's sweep already covers; they are run as a check of the decider.

## Hypothesis (domain expert)

A14(b) (direction words as numbers, knowledge/12-assumptions.md, for information), C5(b) ('key word/s'), C6 (Scheidt's two-part keys), C15 (K2's 'six point five' bearing language). Model as 0175: carved = T(plain, k_i), k_i = w[i mod a] + s d[(i + o) mod m], 12 rules; the 24 known letters force k; w's slots must agree. Statistic: live settings by checks and dictionary words among forced words, K4 against 20 coppers.

## Prediction

No setting with 5 or more checks fits K4, as on the coppers; no dictionary word forced. Zero candidates.

## Method

1. Build the direction readings.
2. For each text, table rule, reading, start and sign: the word's value at each known place.
3. For each word length 1-24: slot agreement; fully forced words looked up in the dictionary, every rotation.
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
 "family": "word plus the direction words read as numbers, k = w[i mod a] + s d, 12 table rules, exact",
 "readings": {
  "ENE 67.5 degrees: 6 7 5": [
   6,
   7,
   5
  ],
  "ENE 67.5 degrees: 6 7 5, reversed": [
   5,
   7,
   6
  ],
  "ENE 067.5: 0 6 7 5": [
   0,
   6,
   7,
   5
  ],
  "ENE 067.5: 0 6 7 5, reversed": [
   5,
   7,
   6,
   0
  ],
  "ENE 67 5": [
   67,
   5
  ],
  "ENE 67 5, reversed": [
   5,
   67
  ],
  "ENE 675": [
   675
  ],
  "ENE 67 degrees 30 minutes": [
   67,
   30
  ],
  "ENE 67 degrees 30 minutes, reversed": [
   30,
   67
  ],
  "ENE 6 7 3 0": [
   6,
   7,
   3,
   0
  ],
  "ENE 6 7 3 0, reversed": [
   0,
   3,
   7,
   6
  ],
  "ENE 1200 mils: 1 2 0 0": [
   1,
   2,
   0,
   0
  ],
  "ENE 1200 mils: 1 2 0 0, reversed": [
   0,
   0,
   2,
   1
  ],
  "ENE 12 0 0": [
   12,
   0,
   0
  ],
  "ENE 12 0 0, reversed": [
   0,
   0,
   12
  ],
  "ENE point 6 of 32": [
   6
  ],
  "ENE point 7 of 32 (from 1)": [
   7
  ],
  "ENE point 3 of 16": [
   3
  ],
  "ENE point 4 of 16 (from 1)": [
   4
  ],
  "E 90 degrees: 9 0": [
   9,
   0
  ],
  "E 90 degrees: 9 0, reversed": [
   0,
   9
  ],
  "E 90": [
   90
  ],
  "NE 45 degrees: 4 5": [
   4,
   5
  ],
  "NE 45 degrees: 4 5, reversed": [
   5,
   4
  ],
  "NE 45": [
   45
  ],
  "E, NE degrees: 90 45": [
   90,
   45
  ],
  "E, NE degrees: 90 45, reversed": [
   45,
   90
  ],
  "E, NE digits: 9 0 4 5": [
   9,
   0,
   4,
   5
  ],
  "E, NE digits: 9 0 4 5, reversed": [
   5,
   4,
   0,
   9
  ],
  "E, NE of 32: 8 4": [
   8,
   4
  ],
  "E, NE of 32: 8 4, reversed": [
   4,
   8
  ],
  "E, NE of 32 from 1: 9 5": [
   9,
   5
  ],
  "E, NE of 32 from 1: 9 5, reversed": [
   5,
   9
  ],
  "E, NE of 16: 4 2": [
   4,
   2
  ],
  "E, NE of 16: 4 2, reversed": [
   2,
   4
  ],
  "E, NE of 16 from 1: 5 3": [
   5,
   3
  ],
  "E, NE of 16 from 1: 5 3, reversed": [
   3,
   5
  ],
  "ENE, E, NE of 32: 6 8 4": [
   6,
   8,
   4
  ],
  "ENE, E, NE of 32: 6 8 4, reversed": [
   4,
   8,
   6
  ],
  "ENE, E, NE of 16: 3 4 2": [
   3,
   4,
   2
  ],
  "ENE, E, NE of 16: 3 4 2, reversed": [
   2,
   4,
   3
  ],
  "ENE, E, NE degrees: 67.5 90 45 as 6 7 5 9 0 4 5": [
   6,
   7,
   5,
   9,
   0,
   4,
   5
  ],
  "ENE, E, NE degrees: 67.5 90 45 as 6 7 5 9 0 4 5, reversed": [
   5,
   4,
   0,
   9,
   5,
   7,
   6
  ]
 },
 "n_readings": 43,
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
  "text": "6 7 5 from the second digit, + SHADOW, Vigenere on the KRYPTOS table",
  "found": true
 },
 "copies": "20 shuffled coppers (seed 1760)",
 "seconds": 2,
 "exhaustive": true
}
```

Notes: live settings with >=4 checks: K4 0 (coppers 0-0); dictionary words 4+: K4 0 (coppers 0-0); plant found True


