# 0175-morse-and-plate-numbers-as-key: F3.2: the Morse E counts and the plate's line lengths as the number half of a two-part key, each reading with an unknown word, exact

**Family:** 3-two-component-key  
**Parent:** 0038-keyword-plus-dates-and-counts-from-the-story  
**Decision:** reverted  
**Run:** 2026-10-16T23:49:19+00:00, 3.3 s, status ran  
**Time by phase:** implement 0 s, test 0 s, run 3 s, record 0 s

## In plain words

The Morse code at the entrance is padded with single dots, read as the letter E, in little groups. The copper's lines are not all the same length. Either could be the number half of a key: a secret word for letters, these numbers added on top. For every way of reading the numbers, the 24 known letters tell us what the secret word would have to be; we check whether it can be one word at all, and whether it is English, and compare with scrambled copies.

## Walkthrough, by hand

1. Take the E runs as carved: 2, 1, 6, 3, 2, 2, 5, 3, 1, 1, repeated under the message from some starting run.
2. On the sculpture's table the known E at place 22 over the carved F asks for key value 1.
3. Subtract the run number under place 22: what is left is the secret word's letter for that slot.
4. With a 7-letter word, places 22 and 29 share a slot: the two leftovers must agree.
5. Go through all 24 known letters for every word length, start and sign; a survivor's word is looked up.
6. Repeat on scrambled copies.

## Worked example (generated)

```
Morse E runs from the first run, Vigenere on the KRYPTOS table, word length 7

place  known  carved  key  run  word value  slot
   22      E       F    1    1           0     0
   23      A       L   10    6           4     1
   24      S       R   21    3          18     2
   25      T       V   18    2          16     3
   26      N       Q    1    2          25     4
   27      O       Q   15    5          10     5
   28      R       P    2    3          25     6
   29      T       R   23    1          22     0
   30      H       N    5    1           4     1
   31      E       G    2    2           0     2
   32      A       K   19    1          18     3
   33      S       S    0    6          20     4
   34      T       S    2    3          25     5
   64      B       N   11    3           8     0
   65      E       Y   17    2          15     1
   66      R       P    2    2           0     2
   67      L       V    5    5           0     3
   68      I       T   15    3          12     4
   69      N       T   11    1          10     5
   70      C       M    9    1           8     6
   71      L       Z    8    2           6     0
   72      O       F    7    1           6     1
   73      C       P   20    6          14     2
   74      K       K    0    3          23     3
```

## Lineage

Inherits from 0038-keyword-plus-dates-and-counts-from-the-story. What changed: F3.2. 0038 added an unknown word to 17 digit strings from the story, one of them the Morse E counts as the digits 510179. Here each count is one key value (10 is ten, not 1 then 0), and the readings are listed in full from the two transcriptions of the Morse (knowledge/01-facts.md, Rumkin): the E runs in carved order, the E totals per message, both directions; and from the plate (knowledge/01-facts.md transcript): the 28 line lengths, their departures from 31, the lower plate's 14 alone, K4's own lines (4, 31, 31, 31), and two place readings: the line and the column of each K4 letter on the copper. 15 sequences, each forward and reversed where it repeats, every alignment, both signs, 12 table rules, word lengths 1-24.

## Hypothesis (domain expert)

C25(b) (the Morse E counts as numbers), C5(b) ('key word/s'), C6 (Scheidt's two-part keys), A14-style layout readings (the plate's line lengths). Model: carved = T(plain, k_i), T one of 12 rules (Vigenere, Beaufort, variant; plain and cipher alphabets standard or KRYPTOS), k_i = w[i mod a] + s d[(i + o) mod m] for a repeating sequence d of length m (or d_i for a place reading), s = +-1, w an unknown word of length a. The 24 known letters force k at their places; w's slots must agree. Checks: 24 minus the slots the known places fill. Statistic: live settings by checks and dictionary words among fully forced words, K4 against 20 shuffled coppers.

## Prediction

Live settings with 4 or more checks: K4 inside the coppers' range for every reading; no dictionary word of 4 or more letters forced on K4 beyond the coppers' rate. Zero candidates.

## Method

1. Build the 15 readings.
2. For each text, table rule and reading, alignment and sign: the word's value at each known place.
3. For each word length 1-24: slot agreement; fully forced words looked up in the dictionary, every rotation, standard and KRYPTOS lettering.
4. Count live settings by checks and hits; K4 against 20 coppers; one planted text as a builder check.

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
 "family": "word plus a number sequence from the Morse or the plate layout, k = w[i mod a] + s d, 12 table rules, exact",
 "readings": {
  "Morse E runs, carved order (01-facts)": [
   2,
   1,
   6,
   3,
   2,
   2,
   5,
   3,
   1,
   1
  ],
  "Morse E runs, carved order (01-facts), reversed": [
   1,
   1,
   3,
   5,
   2,
   2,
   3,
   6,
   1,
   2
  ],
  "Morse E runs, Rumkin": [
   2,
   1,
   5,
   1,
   3,
   2,
   2,
   5,
   3,
   1
  ],
  "Morse E runs, Rumkin, reversed": [
   1,
   3,
   5,
   2,
   2,
   3,
   1,
   5,
   1,
   2
  ],
  "Morse E totals per message (01-facts)": [
   9,
   3,
   9,
   4,
   1
  ],
  "Morse E totals per message (01-facts), reversed": [
   1,
   4,
   9,
   3,
   9
  ],
  "Morse E totals per message (Rumkin)": [
   9,
   7,
   10,
   5,
   1
  ],
  "Morse E totals per message (Rumkin), reversed": [
   1,
   5,
   10,
   7,
   9
  ],
  "Morse E totals, Rumkin's listing order": [
   5,
   10,
   1,
   7,
   9
  ],
  "Morse E totals, Rumkin's listing order, reversed": [
   9,
   7,
   1,
   10,
   5
  ],
  "plate line lengths, 28": [
   32,
   31,
   31,
   30,
   31,
   32,
   31,
   31,
   32,
   31,
   30,
   31,
   31,
   31,
   32,
   30,
   31,
   30,
   32,
   30,
   32,
   31,
   33,
   29,
   31,
   31,
   31,
   31
  ],
  "plate line lengths, 28, reversed": [
   31,
   31,
   31,
   31,
   29,
   33,
   31,
   32,
   30,
   32,
   30,
   31,
   30,
   32,
   31,
   31,
   31,
   30,
   31,
   32,
   31,
   31,
   32,
   31,
   30,
   31,
   31,
   32
  ],
  "plate line lengths minus 31, 28": [
   1,
   0,
   0,
   -1,
   0,
   1,
   0,
   0,
   1,
   0,
   -1,
   0,
   0,
   0,
   1,
   -1,
   0,
   -1,
   1,
   -1,
   1,
   0,
   2,
   -2,
   0,
   0,
   0,
   0
  ],
  "plate line lengths minus 31, 28, reversed": [
   0,
   0,
   0,
   0,
   -2,
   2,
   0,
   1,
   -1,
   1,
   -1,
   0,
   -1,
   1,
   0,
   0,
   0,
   -1,
   0,
   1,
   0,
   0,
   1,
   0,
   -1,
   0,
   0,
   1
  ],
  "lower plate line lengths, 14": [
   32,
   30,
   31,
   30,
   32,
   30,
   32,
   31,
   33,
   29,
   31,
   31,
   31,
   31
  ],
  "lower plate line lengths, 14, reversed": [
   31,
   31,
   31,
   31,
   29,
   33,
   31,
   32,
   30,
   32,
   30,
   31,
   30,
   32
  ],
  "lower plate minus 31, 14": [
   1,
   -1,
   0,
   -1,
   1,
   -1,
   1,
   0,
   2,
   -2,
   0,
   0,
   0,
   0
  ],
  "lower plate minus 31, 14, reversed": [
   0,
   0,
   0,
   0,
   -2,
   2,
   0,
   1,
   -1,
   1,
   -1,
   0,
   -1,
   1
  ],
  "K4's lines 4, 31, 31, 31": [
   4,
   31,
   31,
   31
  ],
  "line length digits": [
   3,
   2,
   3,
   1,
   3,
   1,
   3,
   0,
   3,
   1,
   3,
   2,
   3,
   1,
   3,
   1,
   3,
   2,
   3,
   1,
   3,
   0,
   3,
   1,
   3,
   1,
   3,
   1,
   3,
   2,
   3,
   0,
   3,
   1,
   3,
   0,
   3,
   2,
   3,
   0,
   3,
   2,
   3,
   1,
   3,
   3,
   2,
   9,
   3,
   1,
   3,
   1,
   3,
   1,
   3,
   1
  ],
  "line length digits, reversed": [
   1,
   3,
   1,
   3,
   1,
   3,
   1,
   3,
   9,
   2,
   3,
   3,
   1,
   3,
   2,
   3,
   0,
   3,
   2,
   3,
   0,
   3,
   1,
   3,
   0,
   3,
   2,
   3,
   1,
   3,
   1,
   3,
   1,
   3,
   0,
   3,
   1,
   3,
   2,
   3,
   1,
   3,
   1,
   3,
   2,
   3,
   1,
   3,
   0,
   3,
   1,
   3,
   1,
   3,
   2,
   3
  ],
  "Morse totals digits (Rumkin)": [
   9,
   7,
   1,
   0,
   5,
   1
  ],
  "Morse totals digits (Rumkin), reversed": [
   1,
   5,
   0,
   1,
   7,
   9
  ],
  "line of each K4 letter on the plate": "one value per K4 place",
  "column of each K4 letter on the plate": "one value per K4 place",
  "plate line number (from the top of the lower plate)": "one value per K4 place"
 },
 "n_readings": 26,
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
  "text": "Morse runs from run 3, + SHADOW, Vigenere on the KRYPTOS table",
  "found": true
 },
 "copies": "20 shuffled coppers (seed 1750)",
 "seconds": 3,
 "exhaustive": true
}
```

Notes: live settings with >=4 checks: K4 0 (coppers 0-0); dictionary words 4+: K4 0 (coppers 0-0); plant found True


