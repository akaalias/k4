# 0180-point-as-numbers: F3.7: 'point' read as the decimal point in K2's six point five, or as punctuation (the copper's four ?, K2's ? and X stops), as the number half of a two-part key, exact

**Family:** 3-two-component-key  
**Parent:** 0175-morse-and-plate-numbers-as-key  
**Decision:** reverted  
**Run:** 2026-10-17T00:24:51+00:00, 1.6 s, status ran  
**Time by phase:** design 0 s, implement 0 s, test 0 s, run 2 s, record 0 s

## In plain words

Sanborn's last clue asks 'what's the point?'. A point can be the decimal point in K2's 'six point five', or a punctuation mark such as the question marks on the copper or the X that ends K2's sentences. Their numbers and places could be half the key and a secret word the other half. The 24 known letters say whether any word fits.

## Walkthrough, by hand

1. Write 6 5 (six point five) again and again under the message.
2. On the sculpture's table the known E at place 22 over the carved F asks for key value 1; subtract the number under it: the rest is the secret word's letter there.
3. Places sharing a slot of the word must agree.
4. Every start, sign, word length, table rule and reading; then scrambled copies.

## Worked example (generated)

```
6 5 (six point five) from the first number, Vigenere on the KRYPTOS table, word length 7

place  known  carved  key  num  word value  slot
   22      E       F    1    5          22     0
   23      A       L   10    6           4     1
   24      S       R   21    5          16     2
   25      T       V   18    6          12     3
   26      N       Q    1    5          22     4
   27      O       Q   15    6           9     5
   28      R       P    2    5          23     6
   29      T       R   23    6          17     0
   30      H       N    5    5           0     1
   31      E       G    2    6          22     2
   32      A       K   19    5          14     3
   33      S       S    0    6          20     4
   34      T       S    2    5          23     5
   64      B       N   11    5           6     0
   65      E       Y   17    6          11     1
   66      R       P    2    5          23     2
   67      L       V    5    6          25     3
   68      I       T   15    5          10     4
   69      N       T   11    6           5     5
   70      C       M    9    5           4     6
   71      L       Z    8    6           2     0
   72      O       F    7    5           2     1
   73      C       P   20    6          14     2
   74      K       K    0    5          21     3
```

## Lineage

Inherits from 0175-morse-and-plate-numbers-as-key. What changed: F3.7 (C15(b)-(d)). 0072 used compass points and the letter's words as keyword alphabets. Here 'point' as numbers: the decimal point in K2's 'six point five' (6 5, 65, 6 0 5) and the coordinates with it (38 57 6 5 77 8 44 and variants; 0024 used their digits); as punctuation: the places of the four ? on the copper (in the 869, by line, within their lines), the ? in K2's plaintext and their gaps, K2's X stops and their gaps. Each forward and reversed, every start, both signs, an unknown word of 1-24 letters, 12 table rules (0175's decider). 'The point' as a place on the grounds needs a survey: blocked.

## Hypothesis (domain expert)

C15: 'If they don't, then (CLUE) what's the point? Power resides with a secret' (Sanborn, August 2025); (b) the decimal point of K2's 'six point five', (c) a place, (d) punctuation, Scheidt's 'what's a period'. C5(b), C6. Model as 0175: k_i = w[i mod a] + s d[(i + o) mod m], 12 rules. Statistic: live settings, K4 against 20 coppers.

## Prediction

No setting fits K4 or the coppers (5 or more checks each). Zero candidates.

## Method

1. Build the readings.
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
 "family": "word plus 'point' readings (decimal point, ? and X stops) as numbers, k = w[i mod a] + s d, 12 table rules, exact",
 "readings": {
  "six point five: 6 5": [
   6,
   5
  ],
  "six point five: 6 5, reversed": [
   5,
   6
  ],
  "six point five: 65": [
   65
  ],
  "six point five with the point as 0: 6 0 5": [
   6,
   0,
   5
  ],
  "six point five with the point as 0: 6 0 5, reversed": [
   5,
   0,
   6
  ],
  "K2 coordinates as numbers with the point: 38 57 6 5 77 8 44": [
   38,
   57,
   6,
   5,
   77,
   8,
   44
  ],
  "K2 coordinates as numbers with the point: 38 57 6 5 77 8 44, reversed": [
   44,
   8,
   77,
   5,
   6,
   57,
   38
  ],
  "K2 coordinates, seconds as 65: 38 57 65 77 8 44": [
   38,
   57,
   65,
   77,
   8,
   44
  ],
  "K2 coordinates, seconds as 65: 38 57 65 77 8 44, reversed": [
   44,
   8,
   77,
   65,
   57,
   38
  ],
  "K2 coordinates, seconds as 6.5 rounded up: 38 57 7 77 8 44": [
   38,
   57,
   7,
   77,
   8,
   44
  ],
  "K2 coordinates, seconds as 6.5 rounded up: 38 57 7 77 8 44, reversed": [
   44,
   8,
   77,
   7,
   57,
   38
  ],
  "the four ? on the copper, places in the 869": [
   101,
   227,
   289,
   772
  ],
  "the four ? on the copper, places in the 869, reversed": [
   772,
   289,
   227,
   101
  ],
  "the four ?, lines 4 8 10 25": [
   4,
   8,
   10,
   25
  ],
  "the four ?, lines 4 8 10 25, reversed": [
   25,
   10,
   8,
   4
  ],
  "the four ?, places in their lines 7 9 8 27": [
   7,
   9,
   8,
   27
  ],
  "the four ?, places in their lines 7 9 8 27, reversed": [
   27,
   8,
   9,
   7
  ],
  "the ? in K2's plaintext, letters before each": [
   37,
   162,
   223
  ],
  "the ? in K2's plaintext, letters before each, reversed": [
   223,
   162,
   37
  ],
  "gaps between the ? in K2's plaintext": [
   125,
   61
  ],
  "gaps between the ? in K2's plaintext, reversed": [
   61,
   125
  ],
  "the X stops in K2's plaintext: 68 138 199 251": [
   68,
   138,
   199,
   251
  ],
  "the X stops in K2's plaintext: 68 138 199 251, reversed": [
   251,
   199,
   138,
   68
  ],
  "gaps between the X stops: 70 61 52": [
   70,
   61,
   52
  ],
  "gaps between the X stops: 70 61 52, reversed": [
   52,
   61,
   70
  ]
 },
 "n_readings": 25,
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
  "text": "the four ? places from the second, + SHADOW, Vigenere on the KRYPTOS table",
  "found": true
 },
 "copies": "20 shuffled coppers (seed 1800)",
 "seconds": 1,
 "exhaustive": true
}
```

Notes: live settings with >=4 checks: K4 0 (coppers 0-0); dictionary words 4+: K4 0 (coppers 0-0); plant found True


