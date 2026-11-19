# 0289-f16.4d-a-key-of-small-numbers-on-dictionary-keyword-alphabets: F16.4d: a key of small numbers on keyword alphabets: every pair of dictionary keyword alphabets (208,064 each side, the plain and KRYPTOS alphabets among them) under which every known place needs a key inside ten neighbouring values (the digits 0-9, or ten values from any start), with up to 2 slips; K4 against 50 shuffles; the forced digits of K4's fits read for a period or a known number

**Family:** 16-simple-hand-methods  
**Parent:** 0288-f16.4a-what-carries-the-small-shifts-line-or-letter  
**Decision:** reverted  
**Run:** 2026-11-19T09:21:01+00:00, 2731.4 s, status ran  
**Time by phase:** design 274 s, test 78 s, run 2731 s, record 0 s

## In plain words

K4's known letters often sit only a step or two from the carved letters. One simple way to get that: mix the alphabet with a key word, then move each letter on by a small number, a digit from a date or a coordinate. We try every dictionary word as the key word for the message alphabet and for the carved alphabet and list the pairs under which every known letter needs only a digit from 0 to 9. Scrambled copies of K4 show how many such pairs turn up by luck.

## Walkthrough, by hand

1. Write a key word, then the rest of the alphabet after it: that is the message alphabet. Do the same with a second word for the carved alphabet.
2. For place 26, find N in the message alphabet and Q in the carved alphabet and count the steps from one to the other.
3. Do this for all 24 known places.
4. If every count is a digit from 0 to 9, the pair of words is a fit; write the 24 digits down.
5. Look at the digits: do they repeat, or spell a date or a coordinate?
6. Do the same on scrambled copies of K4 to see how many fits luck gives.

## Worked example (generated)

```
message alphabet: plain A-Z; carved alphabet: plain A-Z; rule: steps from the known letter to the carved one

place known carved steps  a digit 0-9?
   22     E      F     1  yes
   23     A      L    11  no
   24     S      R    25  no
   25     T      V     2  yes
   26     N      Q     3  yes
   27     O      Q     2  yes
   28     R      P    24  no
   29     T      R    24  no
   30     H      N     6  yes
   31     E      G     2  yes
   32     A      K    10  no
   33     S      S     0  yes
   34     T      S    25  no
   64     B      N    12  no
   65     E      Y    20  no
   66     R      P    24  no
   67     L      V    10  no
   68     I      T    11  no
   69     N      T     6  yes
   70     C      M    10  no
   71     L      Z    14  no
   72     O      F    17  no
   73     C      P    13  no
   74     K      K     0  yes
```

## Lineage

Inherits from 0288-f16.4a-what-carries-the-small-shifts-line-or-letter. What changed: F16.4d (issue #123). 0288 found the small shifts go with the plaintext letter, not the carved line, so by the rule set before that run the alphabets come first. New here: no period is assumed. For each ordered pair of alphabets (plain side, cipher side) from the 208,064 of 0244 and each form, the key each known place forces is computed and the table is listed when all of them (but at most 2) lie in the digits 0-9 (literal), or in ten neighbouring values from any start (a digit added to one fixed letter). On the 20 official letters and on all 24. Strength aimed at: exact for the list and the counts; the verdict on K4 is a count against shuffles plus a reading of the forced digits.

## Hypothesis (domain expert)

Bean 2021, section 2.3 (bean-2021-cryptodiagnosis-of-k4.txt, Tables 2 and 3; Materna 2020): the images of a repeated plaintext letter are close, 'the cipher alphabet is near the standard A-Z alphabet, perhaps based on a keyword', with a small numeric key; C27(b), C5(a) (a key word sets the alphabet), C23(b) (the K2 coordinates as digits). Arithmetic, so by rule 7 of order-of-work.md it needs its reason: a key of digits is what small shifts would be the trace of, and 0286-0288 replicated them. Model: c = C[(P(p) + k) mod 26] (Vigenere), k = P(p) - C(c) (variant) or k = P(p) + C(c) (Beaufort), P and C keyword-mixed alphabets of any dictionary word (kryptos.alphabets.keyword_mixed), k in 0-9 at every place, no period. Space: 208,064^2 = 4.3 x 10^10 pairs x 2 key rules x 26 starts. Gromark with a free alphabet (0069, 0076, 0195, 0262) and periodic keys on these pairs (0244) are closed; digits beside a word were 0024, 0038, 0175. Chance: (10/26)^24 = 1.1 x 10^-10 per pair, rule and start, so about 14 literal fits per text by chance and several hundred with a free start: a fit is not a result. What would be: K4's count far above its shuffles (it is expected somewhat above, since the closeness is replicated), a fit whose forced digits repeat with a period or continue a known number, or a fit inside a much narrower window (five values or fewer has chance below 10^-6 over the whole space). The 73 other letters cannot be read from a fit alone: ten choices per letter (3.3 bits) exceed what English decides (0136: 1.78 bits per letter).

## Prediction

K4 has literal fits at no slip, about as many as chance gives (5-40), and is above the median shuffle but not above all 50 in most cells. No fit's digits repeat with a period or match a known number. No fit needs a window narrower than 8 values. Plants: the planted table is listed 8 of 8.

## Method

1. Build the 208,064 keyword alphabets.
2. Per text, drop alphabets that cannot fit on their own side whatever the other side is (two known places with the same carved letter force a difference that depends on the plain alphabet only; the same for a repeated plaintext letter and the cipher alphabet), allowing 2 slips.
3. For every remaining pair and both key rules, run through the known places keeping, for each of the 26 starts at once, whether 0, 1 or 2 places have fallen outside the ten values (bit masks, compiled C, early exit); the 20 official places first, then EAST.
4. Count per cell (20 or 24 letters; literal Vigenere, variant, Beaufort; free start; slips 0, 1, 2); list the literal fits and the no-slip free-start fits.
5. K4, 50 shuffles (known letters kept in place), 8 plants (random dictionary alphabets, random digits, two with a slip).
6. For K4's fits: the narrowest window, a period 1-26, a known number (the K2 coordinates, dates, pi, e).

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
 "item": "F16.4d",
 "alphabets": 208666,
 "pairs_per_text": 43541499556,
 "rules": "Vigenere/variant (k = C(c) - P(p)), Beaufort (k = C(c) + P(p))",
 "window": 10,
 "slips": "0-2",
 "after_side_filter": {
  "K4": [
   154084,
   158132
  ],
  "shuffle00": [
   156137,
   149871
  ],
  "plant0": [
   154669,
   188909
  ]
 },
 "self_check": "C scan equals the Python reference on 20,000 random pairs and 18,000 pairs next to three planted pairs (2199 counted fits)",
 "cells": {
  "24 letters | vig_literal | up to 0 slips": {
   "K4": 0,
   "shuffles_min_median_max": [
    0,
    0,
    0
   ],
   "shuffles_at_or_above": 50,
   "p": 1.0
  },
  "24 letters | vig_literal | up to 1 slips": {
   "K4": 21,
   "shuffles_min_median_max": [
    0,
    0,
    188
   ],
   "shuffles_at_or_above": 9,
   "p": 0.196
  },
  "24 letters | vig_literal | up to 2 slips": {
   "K4": 1465,
   "shuffles_min_median_max": [
    0,
    23,
    7947
   ],
   "shuffles_at_or_above": 8,
   "p": 0.176
  },
  "24 letters | variant_literal | up to 0 slips": {
   "K4": 0,
   "shuffles_min_median_max": [
    0,
    0,
    416
   ],
   "shuffles_at_or_above": 50,
   "p": 1.0
  },
  "24 letters | variant_literal | up to 1 slips": {
   "K4": 0,
   "shuffles_min_median_max": [
    0,
    1,
    26956
   ],
   "shuffles_at_or_above": 50,
   "p": 1.0
  },
  "24 letters | variant_literal | up to 2 slips": {
   "K4": 81,
   "shuffles_min_median_max": [
    0,
    76,
    496043
   ],
   "shuffles_at_or_above": 24,
   "p": 0.49
  },
  "24 letters | beaufort_literal | up to 0 slips": {
   "K4": 0,
   "shuffles_min_median_max": [
    0,
    0,
    61
   ],
   "shuffles_at_or_above": 50,
   "p": 1.0
  },
  "24 letters | beaufort_literal | up to 1 slips": {
   "K4": 2,
   "shuffles_min_median_max": [
    0,
    0,
    2315
   ],
   "shuffles_at_or_above": 19,
   "p": 0.392
  },
  "24 letters | beaufort_literal | up to 2 slips": {
   "K4": 91,
   "shuffles_min_median_max": [
    0,
    36,
    41819
   ],
   "shuffles_at_or_above": 21,
   "p": 0.431
  },
  "24 letters | vig_any_start | up to 0 slips": {
   "K4": 7,
   "shuffles_min_median_max": [
    0,
    0,
    3104
   ],
   "shuffles_at_or_above": 14,
   "p": 0.294
  },
  "24 letters | vig_any_start | up to 1 slips": {
   "K4": 1171,
   "shuffles_min_median_max": [
    0,
    304,
    244047
   ],
   "shuffles_at_or_above": 15,
   "p": 0.314
  },
  "24 letters | vig_any_start | up to 2 slips": {
   "K4": 39523,
   "shuffles_min_median_max": [
    26,
    11925,
    3623610
   ],
   "shuffles_at_or_above": 15,
   "p": 0.314
  },
  "24 letters | beaufort_any_start | up to 0 slips": {
   "K4": 27,
   "shuffles_min_median_max": [
    0,
    1,
    10458
   ],
   "shuffles_at_or_above": 5,
   "p": 0.118
  },
  "24 letters | beaufort_any_start | up to 1 slips": {
   "K4": 1531,
   "shuffles_min_median_max": [
    0,
    231,
    434127
   ],
   "shuffles_at_or_above": 11,
   "p": 0.235
  },
  "24 letters | beaufort_any_start | up to 2 slips": {
   "K4": 55737,
   "shuffles_min_median_max": [
    106,
    11756,
    5035068
   ],
   "shuffles_at_or_above": 10,
   "p": 0.216
  },
  "20 official | vig_literal | up to 0 slips": {
   "K4": 3,
   "shuffles_min_median_max": [
    0,
    0,
    186
   ],
   "shuffles_at_or_above": 9,
   "p": 0.196
  },
  "20 official | vig_literal | up to 1 slips": {
   "K4": 338,
   "shuffles_min_median_max": [
    0,
    65,
    29542
   ],
   "shuffles_at_or_above": 14,
   "p": 0.294
  },
  "20 official | vig_literal | up to 2 slips": {
   "K4": 13882,
   "shuffles_min_median_max": [
    7,
    4239,
    760190
   ],
   "shuffles_at_or_above": 15,
   "p": 0.314
  },
  "20 official | variant_literal | up to 0 slips": {
   "K4": 3,
   "shuffles_min_median_max": [
    0,
    0,
    3942
   ],
   "shuffles_at_or_above": 20,
   "p": 0.412
  },
  "20 official | variant_literal | up to 1 slips": {
   "K4": 438,
   "shuffles_min_median_max": [
    0,
    129,
    204637
   ],
   "shuffles_at_or_above": 20,
   "p": 0.412
  },
  "20 official | variant_literal | up to 2 slips": {
   "K4": 13757,
   "shuffles_min_median_max": [
    35,
    8439,
    3083199
   ],
   "shuffles_at_or_above": 23,
   "p": 0.471
  },
  "20 official | beaufort_literal | up to 0 slips": {
   "K4": 11,
   "shuffles_min_median_max": [
    0,
    0,
    1115
   ],
   "shuffles_at_or_above": 14,
   "p": 0.294
  },
  "20 official | beaufort_literal | up to 1 slips": {
   "K4": 424,
   "shuffles_min_median_max": [
    0,
    293,
    43120
   ],
   "shuffles_at_or_above": 22,
   "p": 0.451
  },
  "20 official | beaufort_literal | up to 2 slips": {
   "K4": 15457,
   "shuffles_min_median_max": [
    0,
    12436,
    648380
   ],
   "shuffles_at_or_above": 21,
   "p": 0.431
  },
  "20 official | vig_any_start | up to 0 slips": {
   "K4": 723,
   "shuffles_min_median_max": [
    1,
    403,
    23443
   ],
   "shuffles_at_or_above": 20,
   "p": 0.412
  },
  "20 official | vig_any_start | up to 1 slips": {
   "K4": 38982,
   "shuffles_min_median_max": [
    348,
    40546,
    1108756
   ],
   "shuffles_at_or_above": 25,
   "p": 0.51
  },
  "20 official | vig_any_start | up to 2 slips": {
   "K4": 1014475,
   "shuffles_min_median_max": [
    18077,
    974661,
    14931672
   ],
   "shuffles_at_or_above": 22,
   "p": 0.451
  },
  "20 official | beaufort_any_start | up to 0 slips": {
   "K4": 349,
   "shuffles_min_median_max": [
    0,
    322,
    86179
   ],
   "shuffles_at_or_above": 24,
   "p": 0.49
  },
  "20 official | beaufort_any_start | up to 1 slips": {
   "K4": 65070,
   "shuffles_min_median_max": [
    170,
    42288,
    2713987
   ],
   "shuffles_at_or_above": 16,
   "p": 0.333
  },
  "20 official | beaufort_any_start | up to 2 slips": {
   "K4": 1731042,
   "shuffles_min_median_max": [
    9172,
    920273,
    29061904
   ],
   "shuffles_at_or_above": 13,
   "p": 0.275
  }
 },
 "cells_K4_above_all_shuffles": [],
 "cells_looked_at": 30,
 "stand_in_null_cells_above_all_others": [
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
  0,
  0,
  0,
  0,
  0,
  1,
  1,
  2,
  3,
  4,
  8,
  10
 ],
 "K4_fits_no_slip_any_start": 34,
 "K4_literal_fits_no_slip": 0,
 "K4_literal_periodic": [],
 "K4_literal_known_number": [],
 "K4_min_window": 10,
 "shuffles_min_window_sorted": [
  8,
  8,
  9,
  9,
  9,
  9,
  9,
  9,
  9,
  9,
  10,
  10,
  10,
  10,
  10,
  10,
  10,
  10,
  10,
  10,
  10,
  10,
  10,
  10,
  10,
  10,
  10,
  10,
  10,
  10,
  10,
  10,
  10,
  10,
  10,
  10,
  10,
  27,
  27,
  27,
  27,
  27,
  27,
  27,
  27,
  27,
  27,
  27,
  27,
  27
 ],
 "shuffles_min_window_at_or_below_K4": 37,
 "K4_window_hist": {
  "10": 34
 },
 "K4_fits_narrowest_first": [
  {
   "plain_word": "BUFFLEHORN",
   "cipher_word": "FUNGIVOROUS",
   "rule": "Beaufort",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 25,
   "keys_26_34_64_74_22_25": [
    2,
    0,
    0,
    1,
    7,
    7,
    25,
    1,
    2,
    2,
    2,
    0,
    8,
    8,
    3,
    2,
    2,
    6,
    3,
    5,
    4,
    0,
    0,
    25
   ]
  },
  {
   "plain_word": "EKABORON",
   "cipher_word": "ADVISORY",
   "rule": "Vigenere/variant",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 7,
   "keys_26_34_64_74_22_25": [
    14,
    16,
    14,
    13,
    7,
    12,
    13,
    12,
    11,
    15,
    7,
    14,
    14,
    9,
    15,
    10,
    11,
    7,
    12,
    14,
    11,
    14,
    14,
    9
   ]
  },
  {
   "plain_word": "EKABORON",
   "cipher_word": "DIVERSORY",
   "rule": "Vigenere/variant",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 7,
   "keys_26_34_64_74_22_25": [
    14,
    16,
    14,
    11,
    7,
    12,
    13,
    13,
    12,
    15,
    7,
    14,
    14,
    9,
    15,
    10,
    11,
    7,
    12,
    14,
    11,
    14,
    12,
    9
   ]
  },
  {
   "plain_word": "GNOMIDE",
   "cipher_word": "OBSEQUIOSITY",
   "rule": "Vigenere/variant",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 2,
   "keys_26_34_64_74_22_25": [
    3,
    2,
    3,
    2,
    8,
    7,
    9,
    10,
    9,
    11,
    2,
    3,
    8,
    3,
    6,
    9,
    11,
    10,
    11,
    3,
    6,
    10,
    3,
    3
   ]
  },
  {
   "plain_word": "HELLEBOREIN",
   "cipher_word": "FUNGIVOROUS",
   "rule": "Beaufort",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 24,
   "keys_26_34_64_74_22_25": [
    1,
    24,
    24,
    0,
    2,
    4,
    24,
    0,
    1,
    5,
    25,
    24,
    7,
    1,
    2,
    1,
    1,
    4,
    2,
    4,
    1,
    25,
    25,
    24
   ]
  },
  {
   "plain_word": "LEPOSTERNIDAE",
   "cipher_word": "FUG",
   "rule": "Beaufort",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 20,
   "keys_26_34_64_74_22_25": [
    24,
    20,
    22,
    23,
    3,
    3,
    21,
    23,
    24,
    25,
    25,
    22,
    21,
    2,
    1,
    25,
    25,
    3,
    2,
    2,
    1,
    22,
    22,
    0
   ]
  },
  {
   "plain_word": "LEPOSTERNIDAE",
   "cipher_word": "FUGGY",
   "rule": "Beaufort",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 21,
   "keys_26_34_64_74_22_25": [
    25,
    21,
    23,
    24,
    4,
    3,
    22,
    24,
    25,
    0,
    4,
    23,
    22,
    3,
    2,
    0,
    25,
    3,
    3,
    3,
    1,
    23,
    23,
    1
   ]
  },
  {
   "plain_word": "LEPOSTERNIDAE",
   "cipher_word": "FUGUE",
   "rule": "Beaufort",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 20,
   "keys_26_34_64_74_22_25": [
    24,
    20,
    22,
    23,
    3,
    3,
    21,
    23,
    24,
    25,
    25,
    22,
    21,
    2,
    1,
    25,
    25,
    3,
    2,
    2,
    1,
    22,
    22,
    0
   ]
  },
  {
   "plain_word": "LEPTORRHINISM",
   "cipher_word": "FOGBOW",
   "rule": "Beaufort",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 21,
   "keys_26_34_64_74_22_25": [
    25,
    21,
    21,
    21,
    21,
    3,
    23,
    2,
    22,
    1,
    25,
    21,
    22,
    1,
    2,
    1,
    25,
    4,
    3,
    4,
    1,
    24,
    1,
    25
   ]
  },
  {
   "plain_word": "LEPTORRHINISM",
   "cipher_word": "FOGGY",
   "rule": "Beaufort",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 21,
   "keys_26_34_64_74_22_25": [
    25,
    21,
    21,
    21,
    21,
    3,
    23,
    2,
    22,
    1,
    4,
    21,
    22,
    1,
    2,
    1,
    25,
    4,
    3,
    4,
    1,
    24,
    1,
    25
   ]
  },
  {
   "plain_word": "LEPTORRHINISM",
   "cipher_word": "FOGOU",
   "rule": "Beaufort",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 21,
   "keys_26_34_64_74_22_25": [
    25,
    21,
    21,
    21,
    21,
    3,
    23,
    2,
    22,
    1,
    25,
    21,
    21,
    1,
    2,
    1,
    25,
    4,
    3,
    4,
    1,
    24,
    1,
    24
   ]
  },
  {
   "plain_word": "LEPTORRHINISM",
   "cipher_word": "FOUGADE",
   "rule": "Beaufort",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 21,
   "keys_26_34_64_74_22_25": [
    25,
    21,
    21,
    21,
    21,
    4,
    23,
    2,
    22,
    1,
    25,
    21,
    21,
    1,
    2,
    1,
    25,
    4,
    3,
    4,
    1,
    24,
    1,
    24
   ]
  },
  {
   "plain_word": "LEPTORRHINISM",
   "cipher_word": "FUGGY",
   "rule": "Beaufort",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 21,
   "keys_26_34_64_74_22_25": [
    0,
    22,
    22,
    22,
    21,
    3,
    23,
    3,
    23,
    1,
    4,
    22,
    22,
    2,
    3,
    1,
    25,
    4,
    4,
    4,
    1,
    24,
    2,
    25
   ]
  },
  {
   "plain_word": "NONPENDING",
   "cipher_word": "OBSEQUIOSITY",
   "rule": "Vigenere/variant",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 2,
   "keys_26_34_64_74_22_25": [
    4,
    3,
    3,
    2,
    8,
    10,
    9,
    10,
    9,
    11,
    5,
    3,
    8,
    2,
    7,
    9,
    11,
    11,
    11,
    3,
    9,
    10,
    3,
    3
   ]
  },
  {
   "plain_word": "NOVEMFID",
   "cipher_word": "SEQUACITY",
   "rule": "Vigenere/variant",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 1,
   "keys_26_34_64_74_22_25": [
    2,
    1,
    2,
    1,
    6,
    9,
    7,
    7,
    6,
    9,
    5,
    2,
    7,
    1,
    7,
    7,
    10,
    10,
    10,
    1,
    8,
    8,
    2,
    2
   ]
  },
  {
   "plain_word": "PELVEOPERITONITIS",
   "cipher_word": "FAUGH",
   "rule": "Beaufort",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 21,
   "keys_26_34_64_74_22_25": [
    25,
    21,
    21,
    25,
    4,
    4,
    21,
    2,
    0,
    25,
    25,
    21,
    23,
    0,
    2,
    25,
    1,
    4,
    2,
    3,
    1,
    22,
    1,
    2
   ]
  },
  {
   "plain_word": "PELVEOPERITONITIS",
   "cipher_word": "FEAGUE",
   "rule": "Beaufort",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 21,
   "keys_26_34_64_74_22_25": [
    25,
    21,
    21,
    25,
    4,
    4,
    21,
    2,
    0,
    25,
    25,
    21,
    23,
    0,
    2,
    25,
    1,
    4,
    2,
    3,
    1,
    22,
    1,
    2
   ]
  },
  {
   "plain_word": "PELVEOPERITONITIS",
   "cipher_word": "FIGGY",
   "rule": "Beaufort",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 21,
   "keys_26_34_64_74_22_25": [
    25,
    21,
    21,
    25,
    4,
    3,
    21,
    2,
    0,
    25,
    4,
    21,
    24,
    0,
    2,
    25,
    1,
    4,
    2,
    3,
    1,
    22,
    1,
    3
   ]
  },
  {
   "plain_word": "PELVEOPERITONITIS",
   "cipher_word": "FIZGIG",
   "rule": "Beaufort",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 21,
   "keys_26_34_64_74_22_25": [
    25,
    21,
    21,
    25,
    4,
    4,
    21,
    2,
    0,
    25,
    0,
    21,
    24,
    0,
    2,
    25,
    4,
    4,
    2,
    3,
    1,
    22,
    1,
    3
   ]
  },
  {
   "plain_word": "PELVEOPERITONITIS",
   "cipher_word": "FUDGE",
   "rule": "Beaufort",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 21,
   "keys_26_34_64_74_22_25": [
    25,
    21,
    21,
    25,
    4,
    4,
    21,
    2,
    0,
    25,
    25,
    21,
    23,
    0,
    2,
    25,
    1,
    4,
    2,
    3,
    1,
    22,
    1,
    2
   ]
  },
  {
   "plain_word": "PELVEOPERITONITIS",
   "cipher_word": "FUDGY",
   "rule": "Beaufort",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 22,
   "keys_26_34_64_74_22_25": [
    0,
    22,
    22,
    0,
    5,
    4,
    22,
    3,
    1,
    0,
    5,
    22,
    24,
    1,
    3,
    0,
    1,
    4,
    3,
    4,
    1,
    23,
    2,
    3
   ]
  },
  {
   "plain_word": "PELVEOPERITONITIS",
   "cipher_word": "FUG",
   "rule": "Beaufort",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 21,
   "keys_26_34_64_74_22_25": [
    25,
    21,
    21,
    25,
    4,
    3,
    21,
    2,
    0,
    25,
    25,
    21,
    23,
    0,
    2,
    25,
    1,
    4,
    2,
    3,
    1,
    22,
    1,
    2
   ]
  },
  {
   "plain_word": "PELVEOPERITONITIS",
   "cipher_word": "FUGGY",
   "rule": "Beaufort",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 22,
   "keys_26_34_64_74_22_25": [
    0,
    22,
    22,
    0,
    5,
    3,
    22,
    3,
    1,
    0,
    4,
    22,
    24,
    1,
    3,
    0,
    1,
    4,
    3,
    4,
    1,
    23,
    2,
    3
   ]
  },
  {
   "plain_word": "PELVEOPERITONITIS",
   "cipher_word": "FUGUE",
   "rule": "Beaufort",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 21,
   "keys_26_34_64_74_22_25": [
    25,
    21,
    21,
    25,
    4,
    3,
    21,
    2,
    0,
    25,
    25,
    21,
    23,
    0,
    2,
    25,
    1,
    4,
    2,
    3,
    1,
    22,
    1,
    2
   ]
  },
  {
   "plain_word": "PELVIOPERITONITIS",
   "cipher_word": "FOGBOW",
   "rule": "Beaufort",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 22,
   "keys_26_34_64_74_22_25": [
    25,
    22,
    22,
    25,
    5,
    3,
    22,
    2,
    0,
    0,
    25,
    22,
    24,
    24,
    2,
    0,
    1,
    5,
    2,
    4,
    1,
    23,
    1,
    3
   ]
  },
  {
   "plain_word": "PELVIOPERITONITIS",
   "cipher_word": "FOGEY",
   "rule": "Beaufort",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 22,
   "keys_26_34_64_74_22_25": [
    25,
    22,
    22,
    25,
    5,
    3,
    22,
    2,
    0,
    0,
    5,
    22,
    24,
    24,
    2,
    0,
    1,
    5,
    2,
    4,
    1,
    23,
    1,
    3
   ]
  },
  {
   "plain_word": "PELVIOPERITONITIS",
   "cipher_word": "FOGGY",
   "rule": "Beaufort",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 22,
   "keys_26_34_64_74_22_25": [
    25,
    22,
    22,
    25,
    5,
    3,
    22,
    2,
    0,
    0,
    4,
    22,
    24,
    24,
    2,
    0,
    1,
    5,
    2,
    4,
    1,
    23,
    1,
    3
   ]
  },
  {
   "plain_word": "PELVIOPERITONITIS",
   "cipher_word": "FOGOU",
   "rule": "Beaufort",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 22,
   "keys_26_34_64_74_22_25": [
    25,
    22,
    22,
    25,
    5,
    3,
    22,
    2,
    0,
    0,
    25,
    22,
    23,
    24,
    2,
    0,
    1,
    5,
    2,
    4,
    1,
    23,
    1,
    2
   ]
  },
  {
   "plain_word": "PELVIOPERITONITIS",
   "cipher_word": "FOUGADE",
   "rule": "Beaufort",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 22,
   "keys_26_34_64_74_22_25": [
    25,
    22,
    22,
    25,
    5,
    4,
    22,
    2,
    0,
    0,
    25,
    22,
    23,
    24,
    2,
    0,
    1,
    5,
    2,
    4,
    1,
    23,
    1,
    2
   ]
  },
  {
   "plain_word": "PELVIOPERITONITIS",
   "cipher_word": "FUDGY",
   "rule": "Beaufort",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 22,
   "keys_26_34_64_74_22_25": [
    0,
    23,
    23,
    0,
    5,
    4,
    22,
    3,
    1,
    0,
    5,
    23,
    24,
    25,
    3,
    0,
    1,
    5,
    3,
    4,
    1,
    23,
    2,
    3
   ]
  },
  {
   "plain_word": "PELVIOPERITONITIS",
   "cipher_word": "FUGGY",
   "rule": "Beaufort",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 22,
   "keys_26_34_64_74_22_25": [
    0,
    23,
    23,
    0,
    5,
    3,
    22,
    3,
    1,
    0,
    4,
    23,
    24,
    25,
    3,
    0,
    1,
    5,
    3,
    4,
    1,
    23,
    2,
    3
   ]
  },
  {
   "plain_word": "PYELONEPHRITIS",
   "cipher_word": "FOGOU",
   "rule": "Beaufort",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 21,
   "keys_26_34_64_74_22_25": [
    22,
    21,
    23,
    1,
    21,
    4,
    23,
    3,
    2,
    1,
    0,
    23,
    24,
    2,
    25,
    1,
    2,
    4,
    3,
    4,
    2,
    24,
    2,
    4
   ]
  },
  {
   "plain_word": "UNMODIFIED",
   "cipher_word": "OBSEQUIOSITY",
   "rule": "Vigenere/variant",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 1,
   "keys_26_34_64_74_22_25": [
    3,
    1,
    2,
    1,
    7,
    6,
    8,
    9,
    8,
    10,
    1,
    2,
    7,
    2,
    6,
    8,
    10,
    9,
    10,
    2,
    5,
    9,
    2,
    2
   ]
  },
  {
   "plain_word": "WAGEWORKING",
   "cipher_word": "UNDISCOVERABLY",
   "rule": "Vigenere/variant",
   "literal": [],
   "narrowest_window": 10,
   "window_start": 9,
   "keys_26_34_64_74_22_25": [
    13,
    17,
    15,
    15,
    14,
    12,
    17,
    11,
    10,
    18,
    10,
    15,
    18,
    15,
    14,
    9,
    10,
    10,
    10,
    12,
    11,
    11,
    16,
    13
   ]
  }
 ],
 "K4_literal_fits": [],
 "K4_capped": false,
 "shuffles_capped": 0,
 "plants": [
  {
   "plain_word": "TELLINGLY",
   "cipher_word": "SNOUT",
   "rule": "vig",
   "slip_at": null,
   "found": {
    "set": "24",
    "slips": 0
   },
   "ok": true,
   "literal_fits_no_slip_24": 2318,
   "min_window": 8,
   "capped": false
  },
  {
   "plain_word": "HAMARTIOLOGY",
   "cipher_word": "ARCHHERETIC",
   "rule": "vig",
   "slip_at": 31,
   "found": {
    "set": "24",
    "slips": 1
   },
   "ok": true,
   "literal_fits_no_slip_24": 0,
   "min_window": 10,
   "capped": false
  },
  {
   "plain_word": "LENTISCUS",
   "cipher_word": "(plain)",
   "rule": "vig",
   "slip_at": null,
   "found": {
    "set": "24",
    "slips": 0
   },
   "ok": true,
   "literal_fits_no_slip_24": 34772,
   "min_window": 7,
   "capped": true
  },
  {
   "plain_word": "(plain)",
   "cipher_word": "SHOPMAN",
   "rule": "vig",
   "slip_at": null,
   "found": {
    "set": "24",
    "slips": 0
   },
   "ok": true,
   "literal_fits_no_slip_24": 13857,
   "min_window": 7,
   "capped": false
  },
  {
   "plain_word": "STOLIST",
   "cipher_word": "PARATAXIS",
   "rule": "variant",
   "slip_at": null,
   "found": {
    "set": "24",
    "slips": 0
   },
   "ok": true,
   "literal_fits_no_slip_24": 4724,
   "min_window": 8,
   "capped": false
  },
  {
   "plain_word": "STEREOMERICAL",
   "cipher_word": "FEELINGLY",
   "rule": "variant",
   "slip_at": null,
   "found": {
    "set": "24",
    "slips": 0
   },
   "ok": true,
   "literal_fits_no_slip_24": 422,
   "min_window": 8,
   "capped": false
  },
  {
   "plain_word": "ELDERMAN",
   "cipher_word": "SABBATHISM",
   "rule": "beaufort",
   "slip_at": null,
   "found": {
    "set": "24",
    "slips": 0
   },
   "ok": true,
   "literal_fits_no_slip_24": 159432,
   "min_window": 6,
   "capped": true
  },
  {
   "plain_word": "FORTHFIGURED",
   "cipher_word": "CONCATENATION",
   "rule": "beaufort",
   "slip_at": 65,
   "found": {
    "set": "24",
    "slips": 1
   },
   "ok": true,
   "literal_fits_no_slip_24": 321,
   "min_window": 9,
   "capped": false
  }
 ],
 "plants_found": "8 of 8",
 "controls": "50 shuffles of K4, known letters kept in place, the same scan",
 "exhaustive": true,
 "not_covered": "grid-mixed alphabets (F16.3); windows wider than ten; a key that leaves 3 or more known places outside; the 73 unknown letters are not read (ten choices per letter)",
 "aws_cost_estimate_dollars": 1.0
}
```

Notes: K4: 0 literal no-slip fits (0 periodic, 0 a known number), 34 with any start; narrowest window K4 10, shuffles 8-27; cells above all 50 shuffles: 0 of 30 (a shuffle against the others: 0 median, 10 max); plants 8/8


