# 0179-weltzeituhr-ring-as-offset: F3.6: the Weltzeituhr's rotating ring of 24 time zones as the number half of a two-part key over 26 letters, with an unknown word, exact

**Family:** 3-two-component-key  
**Parent:** 0175-morse-and-plate-numbers-as-key  
**Decision:** reverted  
**Run:** 2026-10-17T00:24:48+00:00, 2.5 s, status ran  
**Time by phase:** design 0 s, implement 0 s, test 0 s, run 2 s, record 0 s

## In plain words

Berlin's World Clock has a ring of 24 time zones that turns through the day. Laid over the 26 letters, it gives a slowly changing shift: most steps one letter, now and then two. That shift could be half the key, a secret word the other half. The 24 known letters say whether any word fits; scrambled copies say how often that happens by chance.

## Walkthrough, by hand

1. Lay the 24 zones over the 26 letters: zone 0 at 0, zone 1 at 1, ... zone 12 at 13, every so often a step of two.
2. Write those offsets under the message, one zone per letter, from some starting zone.
3. On the sculpture's table the known E at place 22 over the carved F asks for key value 1; subtract the offset under it: the rest is the secret word's letter there.
4. Places sharing a slot of the word must agree.
5. Every start, sign, word length, table rule and reading; then scrambled copies.

## Worked example (generated)

```
24 zones over 26 letters (rounded) from zone 0, Vigenere on the KRYPTOS table, word length 7

place  known  carved  key  num  word value  slot
   22      E       F    1   23           4     0
   23      A       L   10   24          12     1
   24      S       R   21   25          22     2
   25      T       V   18    0          18     3
   26      N       Q    1    1           0     4
   27      O       Q   15    2          13     5
   28      R       P    2    3          25     6
   29      T       R   23    4          19     0
   30      H       N    5    5           0     1
   31      E       G    2    6          22     2
   32      A       K   19    8          11     3
   33      S       S    0    9          17     4
   34      T       S    2   10          18     5
   64      B       N   11   16          21     0
   65      E       Y   17   17           0     1
   66      R       P    2   18          10     2
   67      L       V    5   20          11     3
   68      I       T   15   21          20     4
   69      N       T   11   22          15     5
   70      C       M    9   23          12     6
   71      L       Z    8   24          10     0
   72      O       F    7   25           8     1
   73      C       P   20    0          20     2
   74      K       K    0    1          25     3
```

## Lineage

Inherits from 0175-morse-and-plate-numbers-as-key. What changed: F3.6 (C12(b)). 0052 excluded a cipher on a 24-letter alphabet; the ring as an offset over 26 letters was untested. Readings: the 24 zones laid over the 26 letters (each zone the letter offset it covers, rounded or floored) and the 26 letters over the 24 zones, the ring turning either way, one zone per letter, every start; and the ring turning one zone every 24 letters or every 4 letters (97 letters over 24 zones), every start. With an unknown word of 1-24 letters, both signs, 12 table rules (0175's decider). A ring offset that steps one letter each time is a progressive key, which 0155 covered.

## Hypothesis (domain expert)

C12(b): the Weltzeituhr's structure (24 time zones on a rotating ring) as a key; Sanborn 2014 'delve into that particular clock', 2025 'the World Clock in Berlin'. C5(b), C6. Model as 0175: k_i = w[i mod a] + s d_i, 12 rules; the 24 known letters force k; the word's slots must agree. Statistic: live settings, K4 against 20 coppers.

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
 "family": "word plus the Weltzeituhr ring as offsets over 26 letters, k = w[i mod a] + s d, 12 table rules, exact",
 "readings": {
  "24 zones laid over 26 letters, one zone per letter (rounded)": [
   0,
   1,
   2,
   3,
   4,
   5,
   6,
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
   20,
   21,
   22,
   23,
   24,
   25
  ],
  "24 zones laid over 26 letters (floor)": [
   0,
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
  "26 letters laid over 24 zones (floor)": [
   0,
   0,
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
   23
  ],
  "26 letters laid over 24 zones (rounded)": [
   0,
   1,
   2,
   3,
   4,
   5,
   6,
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
   18,
   19,
   20,
   21,
   22,
   23
  ],
  "24 zones laid over 26 letters, one zone per letter (rounded), ring turning the other way": [
   0,
   25,
   24,
   23,
   22,
   21,
   20,
   18,
   17,
   16,
   15,
   14,
   13,
   12,
   11,
   10,
   9,
   8,
   6,
   5,
   4,
   3,
   2,
   1
  ],
  "24 zones laid over 26 letters (floor), ring turning the other way": [
   0,
   25,
   24,
   23,
   22,
   21,
   20,
   19,
   18,
   17,
   16,
   15,
   13,
   12,
   11,
   10,
   9,
   8,
   7,
   6,
   5,
   4,
   3,
   2
  ],
  "26 letters laid over 24 zones (floor), ring turning the other way": [
   0,
   0,
   25,
   24,
   23,
   22,
   21,
   20,
   19,
   18,
   17,
   16,
   15,
   14,
   14,
   13,
   12,
   11,
   10,
   9,
   8,
   7,
   6,
   5,
   4,
   3
  ],
  "26 letters laid over 24 zones (rounded), ring turning the other way": [
   0,
   25,
   24,
   23,
   22,
   21,
   20,
   20,
   19,
   18,
   17,
   16,
   15,
   14,
   13,
   12,
   11,
   10,
   9,
   8,
   8,
   7,
   6,
   5,
   4,
   3
  ],
  "ring turns one zone every 24 letters, start 0": "one value per K4 place",
  "ring turns one zone every 4 letters (97 over 24 zones), start 0": "one value per K4 place",
  "ring turns one zone every 24 letters, start 1": "one value per K4 place",
  "ring turns one zone every 4 letters (97 over 24 zones), start 1": "one value per K4 place",
  "ring turns one zone every 24 letters, start 2": "one value per K4 place",
  "ring turns one zone every 4 letters (97 over 24 zones), start 2": "one value per K4 place",
  "ring turns one zone every 24 letters, start 3": "one value per K4 place",
  "ring turns one zone every 4 letters (97 over 24 zones), start 3": "one value per K4 place",
  "ring turns one zone every 24 letters, start 4": "one value per K4 place",
  "ring turns one zone every 4 letters (97 over 24 zones), start 4": "one value per K4 place",
  "ring turns one zone every 24 letters, start 5": "one value per K4 place",
  "ring turns one zone every 4 letters (97 over 24 zones), start 5": "one value per K4 place",
  "ring turns one zone every 24 letters, start 6": "one value per K4 place",
  "ring turns one zone every 4 letters (97 over 24 zones), start 6": "one value per K4 place",
  "ring turns one zone every 24 letters, start 7": "one value per K4 place",
  "ring turns one zone every 4 letters (97 over 24 zones), start 7": "one value per K4 place",
  "ring turns one zone every 24 letters, start 8": "one value per K4 place",
  "ring turns one zone every 4 letters (97 over 24 zones), start 8": "one value per K4 place",
  "ring turns one zone every 24 letters, start 9": "one value per K4 place",
  "ring turns one zone every 4 letters (97 over 24 zones), start 9": "one value per K4 place",
  "ring turns one zone every 24 letters, start 10": "one value per K4 place",
  "ring turns one zone every 4 letters (97 over 24 zones), start 10": "one value per K4 place",
  "ring turns one zone every 24 letters, start 11": "one value per K4 place",
  "ring turns one zone every 4 letters (97 over 24 zones), start 11": "one value per K4 place",
  "ring turns one zone every 24 letters, start 12": "one value per K4 place",
  "ring turns one zone every 4 letters (97 over 24 zones), start 12": "one value per K4 place",
  "ring turns one zone every 24 letters, start 13": "one value per K4 place",
  "ring turns one zone every 4 letters (97 over 24 zones), start 13": "one value per K4 place",
  "ring turns one zone every 24 letters, start 14": "one value per K4 place",
  "ring turns one zone every 4 letters (97 over 24 zones), start 14": "one value per K4 place",
  "ring turns one zone every 24 letters, start 15": "one value per K4 place",
  "ring turns one zone every 4 letters (97 over 24 zones), start 15": "one value per K4 place",
  "ring turns one zone every 24 letters, start 16": "one value per K4 place",
  "ring turns one zone every 4 letters (97 over 24 zones), start 16": "one value per K4 place",
  "ring turns one zone every 24 letters, start 17": "one value per K4 place",
  "ring turns one zone every 4 letters (97 over 24 zones), start 17": "one value per K4 place",
  "ring turns one zone every 24 letters, start 18": "one value per K4 place",
  "ring turns one zone every 4 letters (97 over 24 zones), start 18": "one value per K4 place",
  "ring turns one zone every 24 letters, start 19": "one value per K4 place",
  "ring turns one zone every 4 letters (97 over 24 zones), start 19": "one value per K4 place",
  "ring turns one zone every 24 letters, start 20": "one value per K4 place",
  "ring turns one zone every 4 letters (97 over 24 zones), start 20": "one value per K4 place",
  "ring turns one zone every 24 letters, start 21": "one value per K4 place",
  "ring turns one zone every 4 letters (97 over 24 zones), start 21": "one value per K4 place",
  "ring turns one zone every 24 letters, start 22": "one value per K4 place",
  "ring turns one zone every 4 letters (97 over 24 zones), start 22": "one value per K4 place",
  "ring turns one zone every 24 letters, start 23": "one value per K4 place",
  "ring turns one zone every 4 letters (97 over 24 zones), start 23": "one value per K4 place"
 },
 "n_readings": 56,
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
  "text": "24 zones over 26 letters from zone 1, + SHADOW, Vigenere on the KRYPTOS table",
  "found": true
 },
 "copies": "20 shuffled coppers (seed 1790)",
 "seconds": 2,
 "exhaustive": true
}
```

Notes: live settings with >=4 checks: K4 0 (coppers 0-0); dictionary words 4+: K4 0 (coppers 0-0); plant found True


