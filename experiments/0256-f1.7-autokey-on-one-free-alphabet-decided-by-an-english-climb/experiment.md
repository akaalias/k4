# 0256-f1.7-autokey-on-one-free-alphabet-decided-by-an-english-climb: F1.7 and D2: autokey on one free alphabet, every lag K4 fits (ciphertext and plaintext autokey, three forms), each decided by an alphabet climb against copies climbed one at a time

**Family:** 1-keyed-periodic  
**Parent:** 0149-autokey-on-one-unknown-alphabet  
**Decision:** reverted  
**Run:** 2026-10-30T00:40:37+00:00, 8588.2 s, status ran  
**Time by phase:** implement 0 s, test 10 s, run 8588 s, record 0 s

## In plain words

In an autokey cipher the message (or the ciphertext) becomes its own key after a short starter. With a scrambled alphabet nobody knows, about a hundred settings agree with the 24 known letters. For each we search for the scrambled alphabet that makes K4 read most like English, and do the same on scrambled copies of K4 that agree with the known letters equally well. The real answer should read better than all its copies.

## Walkthrough, by hand

1. Pick a cell: plaintext autokey, Beaufort form, lag 33, with an unknown scrambled alphabet.
2. In that system each plain letter becomes the key 33 places later, so once the alphabet is fixed, a chain of places 33 apart is fixed by its first letter.
3. Chains holding a known letter are fixed by it; the others get a free starting letter.
4. Search alphabets (and free starts) for the most English-looking reading that keeps all 24 known letters.
5. Shuffle K4 until a shuffle also fits the cell, and search it the same way; repeat up to 12 times, stopping when a shuffle reads as well as K4.
6. Count the cells where K4 beat all 12; chance gives about one in 13.

## Worked example (generated)

```
F1.7: autokey on one unknown alphabet.

  ciphertext autokey, lag L: key letter at place i = carved letter at place i - L
  so x(plain_i) = x(carved_i) - x(carved_{i-L}) on the unknown alphabet x: the alphabet alone fixes places L+1..97
  plaintext autokey, lag L: key letter = plain letter L places back; a chain i, i+L, i+2L ... is fixed by x and its first letter

  per cell: climb x for the most English reading; climb scrambled copies that fit the same cell; K4 must beat them all.
```

## Lineage

Inherits from 0149-autokey-on-one-unknown-alphabet. What changed: F1.7 (D2's last re-cost, issue #77). 0149 decided autokey on one unknown alphabet exactly and left the lags K4 fits (103 cells over ciphertext/plaintext autokey and three forms) blocked by cost at F1.5's design-2 decider (about an hour per cell). Under autokey the key is the text itself, so the alphabet alone (plus, for plaintext autokey, one primer letter per chain the known letters do not reach) fixes the reading: a climb over the alphabet is much cheaper than design 2's alphabet-and-key tempering. Here that climb is written (compiled), its power measured on plants drawn from K4's own fitting cells, and every one of K4's cells decided against copies climbed one at a time, in the same run.

## Hypothesis (domain expert)

C11a (NSA 1992: 'plain-text auto-key'; NSA 2007: plaintext and ciphertext autokey tried without cribs), C27(c) (any alphabet), C1(b). Model as 0149: x a bijection letters -> Z26; forms V x(c) = x(p) + x(k), B x(c) = x(k) - x(p), R x(c) = x(p) - x(k); k_i = c_{i-L} (ciphertext autokey) or p_{i-L} (plaintext autokey), primer free. Ciphertext autokey: the reading at places L+1..97 is fixed by x alone, the first L letters by single-use primer letters (open: not scored). Plaintext autokey: a chain i, i+L, i+2L... is fixed by x and its first letter; a chain holding a known place has that letter forced (back-propagated), the others are free and climbed. The full chain condition is enforced (0149's equations used only adjacent known pairs), so a cell 0149 called fit may turn out dead here (three are), and cells 0149 skipped for want of adjacent known pairs get checks (30 fit); both are reported. Copies: shuffles of the text that 0149's exact decider fits in the same cell.

## Prediction

Low power, measured: ciphertext-autokey plants found at most 1 in 4 (the desk climbs never reached a plant's own score there); plaintext-autokey plants about 1 in 3 overall, better at short lags where the checks pin the alphabet. Some of 0149's 103 cells die under the full chain equations. K4's rate of cells above all 12 copies inside the ten stand-ins' spread. Zero candidates.

## Method

1. Cells: every (kind, form, lag) where K4 fits the exact decider, now with plaintext autokey's chains in full (consecutive known places of one chain linked through the carved letters between them; 0149 used only pairs L apart), solved by 0149's exact solver.
2. Per cell (one job, own seed): climb K4 once; then draw shuffles of K4 that fit the same cell, climb each, stop at the first at or above K4; at most 12, escalated to 100 where K4 beats all 12.
3. Climb: plaintext autokey at lags up to 12, check-keeping tempering from the exact witness with repair swaps (0139's move); every other cell, tempering with a fixed penalty per known letter out of place, recording only states with all 24 in place. Ciphertext autokey readings are scored on places L+1 to 97 (the first L come from single-use primer letters).
4. Plants: per kind 12 clean and 12 Sanborn-style messages enciphered on cells drawn from K4's, through the same decision without escalation; power per kind and per climb.
5. Ten shuffles of K4 stand in for K4 (seed 2561): each decides its own fitting cells through the same procedure without escalation. Verdict: K4's rate of cells above all 12 copies ranked among the stand-ins' rates (0254, 0255: the null is a spread over texts, not Binomial(n, 1/13)); the top readings listed.

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
 "item": "F1.7 (D2's last re-cost; the cells decided in the same run)",
 "decider_used": "plaintext autokey at lags 1-12: check-keeping parallel tempering (16 replicas x 300 rounds x 1000 moves, T 0.1->0.002; every replica starts from the exact solver's witness of the full chain equations; a swap that breaks a check is repaired by a second swap that restores every check, as 0139, or dropped); every other cell: parallel tempering with a fixed penalty 0.6 per known place out of place (16 replicas x 300 rounds x 1000 moves, T 0.15->0.003), only states with every known place right recorded",
 "desk_tests": "2026-10-29, before the run: the draft's annealing ('sa', penalty 0.04 ramped) never reached a state with all 24 in place at plaintext lags 6-12 and left the true alphabet when started on it; the full-chain witness and the check-keeping moves read 2 of 3 plants at lag 6 exactly; on ciphertext autokey (lags 34-70) no variant (sa, keep, tempering at penalties 0.2/0.6/2.0, up to 5x longer) reached the true reading's score (plants -4.2, climbs -5.5 to -6.3): low power is expected there and is measured here",
 "modal_cost_estimate": "11 texts (K4 and 10 stand-ins) x about 100 cells x about 4 climbs, plus 48 plants: 'keep' cells (plaintext autokey to lag 12) about 4 min per climb, others about 3 s: about 35 core-hours, about $2 of Modal credit (about $11.9 left after the margin)",
 "decider_draft": "compiled annealing over the alphabet (and free plaintext-autokey chain starts): 20 restarts x 500000 moves, T 0.15->0.003, penalty per known letter out of place 0.04 raised 50-fold through each run; only states with every known letter in place count; ciphertext autokey scored on places L+1..97 (the first L letters come from single-use primer letters and are open)",
 "copies": "shuffles 0149's exact decider fits in the same cell, climbed one at a time; stop at the first at or above K4, at most 12, escalated to 100 for K4",
 "k4_fitting_cells": 130,
 "matches_0149_record": false,
 "fit_0149_record_count": 103,
 "cells_fit_now_not_in_0149": [
  "pt/B/13",
  "pt/B/14",
  "pt/B/15",
  "pt/B/16",
  "pt/B/17",
  "pt/B/18",
  "pt/B/19",
  "pt/B/21",
  "pt/B/22",
  "pt/B/23",
  "pt/B/24",
  "pt/B/25",
  "pt/B/26",
  "pt/R/13",
  "pt/R/14",
  "pt/R/15",
  "pt/R/16",
  "pt/R/17",
  "pt/R/18",
  "pt/R/19",
  "pt/R/21",
  "pt/R/22",
  "pt/R/23",
  "pt/R/24",
  "pt/R/25",
  "pt/R/26",
  "pt/V/13",
  "pt/V/14",
  "pt/V/15",
  "pt/V/16"
 ],
 "cells_in_0149_dead_under_full_chains": [
  "pt/B/6",
  "pt/B/7",
  "pt/V/11"
 ],
 "full_chain_note": "0149 wrote plaintext-autokey equations only for known places exactly L apart, and skipped cells with none; the full chain equations link consecutive known places of a chain through the carved letters between them, so cells 0149 never decided get checks (and fit), and three cells it called fit are dead",
 "per_kind": {
  "ct": {
   "cells": 43,
   "no_valid_reading": 0,
   "above_all_12": 4
  },
  "pt": {
   "cells": 87,
   "no_valid_reading": 0,
   "above_all_12": 3
  }
 },
 "k4_cells_with_a_valid_reading": 130,
 "k4_above_all_12": 7,
 "expected_12": 10.0,
 "binomial_p_12": 0.8797802584149567,
 "k4_above_all_100": 0,
 "expected_100": 1.29,
 "binomial_note": "the binomial p assumes cells are independent draws at 1/13; 0254-0255 showed each text has its own rate, so the verdict is K4's rank among the stand-ins",
 "standins": {
  "k4": {
   "cells": 130,
   "valid": 130,
   "above_all_12": 7,
   "rate": 0.0538,
   "beat_first_rate": 0.4538
  },
  "standin0": {
   "cells": 148,
   "valid": 148,
   "above_all_12": 5,
   "rate": 0.0338,
   "beat_first_rate": 0.4932
  },
  "standin1": {
   "cells": 172,
   "valid": 172,
   "above_all_12": 11,
   "rate": 0.064,
   "beat_first_rate": 0.4186
  },
  "standin2": {
   "cells": 162,
   "valid": 162,
   "above_all_12": 12,
   "rate": 0.0741,
   "beat_first_rate": 0.537
  },
  "standin3": {
   "cells": 109,
   "valid": 109,
   "above_all_12": 11,
   "rate": 0.1009,
   "beat_first_rate": 0.5046
  },
  "standin4": {
   "cells": 158,
   "valid": 158,
   "above_all_12": 10,
   "rate": 0.0633,
   "beat_first_rate": 0.5759
  },
  "standin5": {
   "cells": 176,
   "valid": 176,
   "above_all_12": 9,
   "rate": 0.0511,
   "beat_first_rate": 0.5682
  },
  "standin6": {
   "cells": 140,
   "valid": 140,
   "above_all_12": 11,
   "rate": 0.0786,
   "beat_first_rate": 0.6286
  },
  "standin7": {
   "cells": 124,
   "valid": 124,
   "above_all_12": 21,
   "rate": 0.1694,
   "beat_first_rate": 0.6129
  },
  "standin8": {
   "cells": 181,
   "valid": 181,
   "above_all_12": 7,
   "rate": 0.0387,
   "beat_first_rate": 0.3757
  },
  "standin9": {
   "cells": 112,
   "valid": 111,
   "above_all_12": 4,
   "rate": 0.036,
   "beat_first_rate": 0.3333
  }
 },
 "standins_at_or_above_k4_rate": 6,
 "p_among_standins": 0.6364,
 "plants": {
  "power": {
   "ct/clean": [
    6,
    12
   ],
   "ct_tempering": [
    8,
    24
   ],
   "ct/sanborn": [
    2,
    12
   ],
   "pt/clean": [
    1,
    12
   ],
   "pt_tempering": [
    4,
    24
   ],
   "pt/sanborn": [
    3,
    12
   ]
  },
  "null_per_plant": "1/13",
  "each": {
   "ct/0": {
    "cls": "clean",
    "cell": "ct/V/46",
    "found": false,
    "above": 0,
    "score": -5.85028,
    "letters_right": 13,
    "letters_scored": 51
   },
   "ct/1": {
    "cls": "clean",
    "cell": "ct/B/64",
    "found": true,
    "above": 12,
    "score": -4.71594,
    "letters_right": 17,
    "letters_scored": 33
   },
   "ct/2": {
    "cls": "clean",
    "cell": "ct/B/72",
    "found": false,
    "above": 0,
    "score": -4.12843,
    "letters_right": 4,
    "letters_scored": 25
   },
   "ct/3": {
    "cls": "clean",
    "cell": "ct/B/69",
    "found": true,
    "above": 12,
    "score": -3.94941,
    "letters_right": 11,
    "letters_scored": 28
   },
   "ct/4": {
    "cls": "clean",
    "cell": "ct/V/73",
    "found": false,
    "above": 5,
    "score": -3.77033,
    "letters_right": 5,
    "letters_scored": 24
   },
   "ct/5": {
    "cls": "clean",
    "cell": "ct/B/52",
    "found": true,
    "above": 12,
    "score": -4.85512,
    "letters_right": 19,
    "letters_scored": 45
   },
   "ct/6": {
    "cls": "clean",
    "cell": "ct/V/69",
    "found": true,
    "above": 12,
    "score": -3.80731,
    "letters_right": 12,
    "letters_scored": 28
   },
   "ct/7": {
    "cls": "clean",
    "cell": "ct/B/66",
    "found": false,
    "above": 0,
    "score": -4.64372,
    "letters_right": 12,
    "letters_scored": 31
   },
   "ct/8": {
    "cls": "clean",
    "cell": "ct/R/69",
    "found": false,
    "above": 0,
    "score": -4.33845,
    "letters_right": 15,
    "letters_scored": 28
   },
   "ct/9": {
    "cls": "clean",
    "cell": "ct/V/41",
    "found": true,
    "above": 12,
    "score": -5.20509,
    "letters_right": 21,
    "letters_scored": 56
   },
   "ct/10": {
    "cls": "clean",
    "cell": "ct/B/54",
    "found": false,
    "above": 8,
    "score": -5.34055,
    "letters_right": 18,
    "letters_scored": 43
   },
   "ct/11": {
    "cls": "clean",
    "cell": "ct/V/41",
    "found": true,
    "above": 12,
    "score": -5.44849,
    "letters_right": 24,
    "letters_scored": 56
   },
   "ct/12": {
    "cls": "xstops",
    "cell": "ct/R/73",
    "found": false,
    "above": 6,
    "score": -3.6237,
    "letters_right": 4,
    "letters_scored": 24
   },
   "ct/13": {
    "cls": "xstops",
    "cell": "ct/V/71",
    "found": false,
    "above": 0,
    "score": -4.15462,
    "letters_right": 5,
    "letters_scored": 26
   },
   "ct/14": {
    "cls": "xstops",
    "cell": "ct/B/43",
    "found": false,
    "above": 2,
    "score": -5.70302,
    "letters_right": 15,
    "letters_scored": 54
   },
   "ct/15": {
    "cls": "xstops",
    "cell": "ct/V/41",
    "found": false,
    "above": 0,
    "score": -5.70621,
    "letters_right": 17,
    "letters_scored": 56
   },
   "ct/16": {
    "cls": "k123",
    "cell": "ct/R/73",
    "found": false,
    "above": 1,
    "score": -3.87502,
    "letters_right": 3,
    "letters_scored": 24
   },
   "ct/17": {
    "cls": "k123",
    "cell": "ct/B/67",
    "found": false,
    "above": 2,
    "score": -4.47649,
    "letters_right": 10,
    "letters_scored": 30
   },
   "ct/18": {
    "cls": "k123",
    "cell": "ct/B/43",
    "found": true,
    "above": 12,
    "score": -5.44943,
    "letters_right": 22,
    "letters_scored": 54
   },
   "ct/19": {
    "cls": "k123",
    "cell": "ct/R/67",
    "found": false,
    "above": 7,
    "score": -4.36898,
    "letters_right": 14,
    "letters_scored": 30
   },
   "ct/20": {
    "cls": "sub3",
    "cell": "ct/B/56",
    "found": false,
    "above": 3,
    "score": -5.42375,
    "letters_right": 17,
    "letters_scored": 41
   },
   "ct/21": {
    "cls": "sub3",
    "cell": "ct/B/72",
    "found": false,
    "above": 0,
    "score": -3.98898,
    "letters_right": 6,
    "letters_scored": 25
   },
   "ct/22": {
    "cls": "sub3",
    "cell": "ct/B/56",
    "found": true,
    "above": 12,
    "score": -4.71552,
    "letters_right": 22,
    "letters_scored": 41
   },
   "ct/23": {
    "cls": "sub3",
    "cell": "ct/V/71",
    "found": false,
    "above": 0,
    "score": -3.94737,
    "letters_right": 11,
    "letters_scored": 26
   },
   "pt/0": {
    "cls": "clean",
    "cell": "pt/V/33",
    "found": false,
    "above": 5,
    "score": -4.42427,
    "letters_right": 31,
    "letters_scored": 97
   },
   "pt/1": {
    "cls": "clean",
    "cell": "pt/B/17",
    "found": false,
    "above": 9,
    "score": -5.52395,
    "letters_right": 31,
    "letters_scored": 97
   },
   "pt/2": {
    "cls": "clean",
    "cell": "pt/R/19",
    "found": true,
    "above": 12,
    "score": -5.30767,
    "letters_right": 43,
    "letters_scored": 97
   },
   "pt/3": {
    "cls": "clean",
    "cell": "pt/B/50",
    "found": false,
    "above": 4,
    "score": -4.01269,
    "letters_right": 29,
    "letters_scored": 97
   },
   "pt/4": {
    "cls": "clean",
    "cell": "pt/B/24",
    "found": false,
    "above": 0,
    "score": -5.09789,
    "letters_right": 27,
    "letters_scored": 97
   },
   "pt/5": {
    "cls": "clean",
    "cell": "pt/B/15",
    "found": false,
    "above": 0,
    "score": -6.02973,
    "letters_right": 30,
    "letters_scored": 97
   },
   "pt/6": {
    "cls": "clean",
    "cell": "pt/V/38",
    "found": false,
    "above": 0,
    "score": -4.36849,
    "letters_right": 29,
    "letters_scored": 97
   },
   "pt/7": {
    "cls": "clean",
    "cell": "pt/B/14",
    "found": false,
    "above": 3,
    "score": -6.27537,
    "letters_right": 35,
    "letters_scored": 97
   },
   "pt/8": {
    "cls": "clean",
    "cell": "pt/B/23",
    "found": false,
    "above": 0,
    "score": -5.30645,
    "letters_right": 37,
    "letters_scored": 97
   },
   "pt/9": {
    "cls": "clean",
    "cell": "pt/B/17",
    "found": false,
    "above": 2,
    "score": -5.6703,
    "letters_right": 27,
    "letters_scored": 97
   },
   "pt/10": {
    "cls": "clean",
    "cell": "pt/V/51",
    "found": false,
    "above": 1,
    "score": -4.05691,
    "letters_right": 26,
    "letters_scored": 97
   },
   "pt/11": {
    "cls": "clean",
    "cell": "pt/B/14",
    "found": false,
    "above": 2,
    "score": -6.42028,
    "letters_right": 34,
    "letters_scored": 97
   },
   "pt/12": {
    "cls": "xstops",
    "cell": "pt/B/24",
    "found": true,
    "above": 12,
    "score": -4.93679,
    "letters_right": 25,
    "letters_scored": 97
   },
   "pt/13": {
    "cls": "xstops",
    "cell": "pt/B/49",
    "found": true,
    "above": 12,
    "score": -3.91271,
    "letters_right": 36,
    "letters_scored": 97
   },
   "pt/14": {
    "cls": "xstops",
    "cell": "pt/V/34",
    "found": false,
    "above": 0,
    "score": -4.52055,
    "letters_right": 32,
    "letters_scored": 97
   },
   "pt/15": {
    "cls": "xstops",
    "cell": "pt/B/37",
    "found": false,
    "above": 5,
    "score": -4.36825,
    "letters_right": 33,
    "letters_scored": 97
   },
   "pt/16": {
    "cls": "k123",
    "cell": "pt/B/18",
    "found": false,
    "above": 3,
    "score": -5.56064,
    "letters_right": 27,
    "letters_scored": 97
   },
   "pt/17": {
    "cls": "k123",
    "cell": "pt/V/32",
    "found": true,
    "above": 12,
    "score": -4.33891,
    "letters_right": 39,
    "letters_scored": 97
   },
   "pt/18": {
    "cls": "k123",
    "cell": "pt/V/52",
    "found": false,
    "above": 5,
    "score": -3.95994,
    "letters_right": 27,
    "letters_scored": 97
   },
   "pt/19": {
    "cls": "k123",
    "cell": "pt/R/39",
    "found": false,
    "above": 0,
    "score": -4.33329,
    "letters_right": 28,
    "letters_scored": 97
   },
   "pt/20": {
    "cls": "sub3",
    "cell": "pt/R/23",
    "found": false,
    "above": 0,
    "score": -5.19715,
    "letters_right": 28,
    "letters_scored": 97
   },
   "pt/21": {
    "cls": "sub3",
    "cell": "pt/V/16",
    "found": false,
    "above": 0,
    "score": -5.85669,
    "letters_right": 31,
    "letters_scored": 97
   },
   "pt/22": {
    "cls": "sub3",
    "cell": "pt/R/21",
    "found": false,
    "above": 6,
    "score": -5.42225,
    "letters_right": 37,
    "letters_scored": 97
   },
   "pt/23": {
    "cls": "sub3",
    "cell": "pt/V/33",
    "found": false,
    "above": 7,
    "score": -4.50235,
    "letters_right": 33,
    "letters_scored": 97
   }
  }
 },
 "cells": [
  {
   "cell": "ct/R/43",
   "score": -5.41375,
   "above": 69,
   "copies": [
    -6.18138,
    -5.93624,
    -6.11713,
    -5.7631,
    -5.6393,
    -5.94328,
    -5.90709,
    -5.89143,
    -6.0388,
    -5.43745,
    -5.85163,
    -5.96801,
    -6.03897,
    -5.99664,
    -5.76669,
    -5.79724,
    -5.69771,
    -5.72815,
    -5.97049,
    -5.95159,
    -5.72596,
    -5.43445,
    -5.9029,
    -5.90167,
    -6.00156,
    -5.55325,
    -5.87487,
    -6.01833,
    -5.79704,
    -5.52611,
    -5.60618,
    -5.9654,
    -5.48124,
    -5.70475,
    -6.1173,
    -5.92664,
    -5.73372,
    -5.9459,
    -6.07488,
    -5.66945,
    -5.85779,
    -6.00809,
    -5.71841,
    -5.8774,
    -5.7536,
    -5.79809,
    -5.76827,
    -5.75377,
    -6.06505,
    -5.53879,
    -6.03189,
    -5.68031,
    -5.92775,
    -5.59152,
    -6.00169,
    -5.91521,
    -5.61002,
    -5.93225,
    -5.66587,
    -5.86575,
    -5.88919,
    -5.60771,
    -6.02582,
    -5.66508,
    -5.92622,
    -5.6247,
    -6.06577,
    -5.58143,
    -5.84777,
    -5.33392
   ],
   "reading": "???????????????????????????????????????????QAINACUBJESSWEDANIJOBERLINCLOCKRSTWWTHROLKSHTEAREWAGCC",
   "known_in_place": 11
  },
  {
   "cell": "pt/R/15",
   "score": -5.76279,
   "above": 35,
   "copies": [
    -5.97189,
    -6.05895,
    -6.07689,
    -5.8726,
    -6.03135,
    -6.02974,
    -5.8921,
    -5.79736,
    -6.10719,
    -6.09019,
    -6.15035,
    -6.00981,
    -5.88724,
    -5.95686,
    -5.79072,
    -6.0304,
    -6.03472,
    -6.07696,
    -6.1619,
    -6.07364,
    -6.02929,
    -5.94138,
    -5.88257,
    -5.92563,
    -6.02657,
    -5.86599,
    -5.85153,
    -6.00453,
    -5.94618,
    -5.82132,
    -5.9844,
    -6.06598,
    -6.12071,
    -6.10337,
    -6.02845,
    -5.75767
   ],
   "reading": "RPHSSANDPEDSGANOOYNNYEASTNORTHEASTXTXMOAFGYANBHBREGNFRIMWAYSKYDBERLINCLOCKCUDYFONSFIFIAOPOIGERKGY",
   "known_in_place": 24
  },
  {
   "cell": "ct/B/69",
   "score": -4.11956,
   "above": 23,
   "copies": [
    -4.16682,
    -4.40443,
    -4.21372,
    -4.31247,
    -4.38475,
    -4.41182,
    -4.38567,
    -4.25966,
    -4.28087,
    -4.38466,
    -4.3433,
    -4.34023,
    -4.3191,
    -4.30508,
    -4.2968,
    -4.41313,
    -4.14344,
    -4.3397,
    -4.30303,
    -4.56246,
    -4.18707,
    -4.2955,
    -4.33389,
    -4.1002
   ],
   "reading": "?????????????????????????????????????????????????????????????????????CLOCKETOUREBEFORANTINCENSSUE",
   "known_in_place": 5
  },
  {
   "cell": "ct/V/71",
   "score": -3.9361,
   "above": 22,
   "copies": [
    -4.13036,
    -4.08144,
    -4.11534,
    -4.26126,
    -4.13629,
    -4.13703,
    -4.11246,
    -4.54854,
    -3.94431,
    -4.02991,
    -4.12022,
    -3.99475,
    -4.17058,
    -4.09413,
    -4.14185,
    -4.00667,
    -4.06712,
    -4.11952,
    -4.10712,
    -4.05232,
    -3.94848,
    -4.28994,
    -3.88339
   ],
   "reading": "???????????????????????????????????????????????????????????????????????OCKATCONTINGERINESTINGNEDT",
   "known_in_place": 3
  },
  {
   "cell": "pt/R/12",
   "score": -6.38968,
   "above": 22,
   "copies": [
    -6.44031,
    -6.52771,
    -6.92878,
    -6.98614,
    -7.49728,
    -7.28287,
    -7.29271,
    -7.45351,
    -7.09384,
    -7.00618,
    -7.05246,
    -7.10795,
    -7.11181,
    -6.9879,
    -6.78292,
    -6.99904,
    -6.46438,
    -6.94948,
    -7.02334,
    -6.62399,
    -6.59227,
    -7.40482,
    -6.10656
   ],
   "reading": "SVPTHBULBAIPDPQCWHPUNEASTNORTHEASTZAPTYYITTLTVGWUOMBCCFJEHIKUNWBERLINCLOCKMOREHPTAPFOFSEAMQCNPREU",
   "known_in_place": 24
  },
  {
   "cell": "pt/B/52",
   "score": -3.9165,
   "above": 17,
   "copies": [
    -3.97116,
    -4.01052,
    -3.95377,
    -3.98704,
    -3.96496,
    -4.03016,
    -4.05495,
    -4.00367,
    -3.99577,
    -4.02161,
    -3.96333,
    -3.96868,
    -3.93448,
    -4.00274,
    -4.00671,
    -4.01294,
    -4.04275,
    -3.84961
   ],
   "reading": "OMYASINTHERESWITHENESEASTNORTHEASTOROUSEAGEANDINGTHERTHESTOTTOOBERLINCLOCKTORESHISMESERATINGDOMIC",
   "known_in_place": 24
  },
  {
   "cell": "ct/B/43",
   "score": -5.65377,
   "above": 12,
   "copies": [
    -5.70691,
    -5.87907,
    -5.78576,
    -6.02298,
    -6.27608,
    -5.91679,
    -5.72096,
    -5.98686,
    -6.23065,
    -5.87675,
    -6.16126,
    -6.13306,
    -5.61147
   ],
   "reading": "???????????????????????????????????????????JODIMARMOBOOBAWEDLIDBERLINCLOCKTESVBODROJVEZALIALEQUEP",
   "known_in_place": 11
  },
  {
   "cell": "pt/B/31",
   "score": -4.5428,
   "above": 11,
   "copies": [
    -4.57062,
    -4.64159,
    -4.67284,
    -4.61727,
    -4.62652,
    -4.60401,
    -4.63398,
    -4.56865,
    -4.57086,
    -4.60869,
    -4.66421,
    -4.41314
   ],
   "reading": "GLIABECKTICITYWARRETHEASTNORTHEASTBOTHERUSTREGULARIMPEENNHATTHOBERLINCLOCKANWHATTUREENTVIZALFEARI",
   "known_in_place": 24
  },
  {
   "cell": "ct/V/46",
   "score": -5.55251,
   "above": 11,
   "copies": [
    -5.66002,
    -5.79895,
    -5.74798,
    -5.64067,
    -5.82872,
    -5.58506,
    -5.76371,
    -5.60651,
    -6.04104,
    -5.83261,
    -5.60737,
    -5.33382
   ],
   "reading": "??????????????????????????????????????????????EUHMORLDWICKNDTAOBERLINCLOCKAYBPSCUKOTAAMIKOTALTOPA",
   "known_in_place": 11
  },
  {
   "cell": "ct/B/34",
   "score": -5.80084,
   "above": 11,
   "copies": [
    -6.0412,
    -6.08223,
    -6.10655,
    -5.92621,
    -5.97329,
    -6.10704,
    -6.07158,
    -6.07287,
    -6.09589,
    -6.41906,
    -6.12438,
    -5.7576
   ],
   "reading": "??????????????????????????????????BCSEDGLARSCTYWERODWHIJJDINIGRBERLINCLOCKMARKGMRADDACBHASPLOVOTU",
   "known_in_place": 11
  },
  {
   "cell": "pt/B/21",
   "score": -5.32735,
   "above": 10,
   "copies": [
    -5.54461,
    -5.68628,
    -5.60789,
    -5.64733,
    -5.42612,
    -5.58282,
    -5.5015,
    -5.55965,
    -5.55018,
    -5.43045,
    -5.1777
   ],
   "reading": "RTTHINODLMCCASLIONGWHEASTNORTHEASTEMONOVECGTODNOKLVTVCOFHEMVIDYBERLINCLOCKEJESEATSONSSWEGHKEAAMAF",
   "known_in_place": 24
  },
  {
   "cell": "ct/B/54",
   "score": -5.18735,
   "above": 9,
   "copies": [
    -5.42928,
    -5.88186,
    -5.65953,
    -5.82433,
    -5.27438,
    -5.5536,
    -5.68452,
    -5.43301,
    -5.71451,
    -5.1376
   ],
   "reading": "??????????????????????????????????????????????????????INPFNUNEKBERLINCLOCKOBIDISRISECLEDASISLEDPR",
   "known_in_place": 11
  },
  {
   "cell": "pt/V/16",
   "score": -5.6355,
   "above": 8,
   "copies": [
    -5.83595,
    -6.46497,
    -5.68393,
    -5.75537,
    -5.8571,
    -5.9344,
    -5.95808,
    -5.99196,
    -5.5394
   ],
   "reading": "IJPIARDGEASDXPCOMYNDBEASTNORTHEASTBCAHNMPARONHYKEDPSOULDYMUUMASBERLINCLOCKRYDONTHAJNREDELYJKSADDI",
   "known_in_place": 24
  },
  {
   "cell": "pt/R/49",
   "score": -4.0014,
   "above": 7,
   "copies": [
    -4.09937,
    -4.12514,
    -4.04731,
    -4.12131,
    -4.03858,
    -4.00863,
    -4.02885,
    -3.99166
   ],
   "reading": "PECIRECTINGINPROADINHEASTNORTHEASTRALREASHATINTHEREATERSINEMOREBERLINCLOCKETAKENAICANFORTOTHETHAP",
   "known_in_place": 24
  },
  {
   "cell": "pt/V/46",
   "score": -4.05846,
   "above": 7,
   "copies": [
    -4.12696,
    -4.11612,
    -4.12346,
    -4.1164,
    -4.10923,
    -4.11045,
    -4.13824,
    -4.00921
   ],
   "reading": "ACKINTERANDPERRECTOPLEASTNORTHEASTTHECONDERATSCANCANALANDSTINUMBERLINCLOCKENCEFFRIVESHISHAVENELIB",
   "known_in_place": 24
  },
  {
   "cell": "pt/B/22",
   "score": -5.16939,
   "above": 6,
   "copies": [
    -5.22251,
    -5.49357,
    -5.37957,
    -5.32156,
    -5.32865,
    -5.34075,
    -5.14402
   ],
   "reading": "HWVGRSRKKIESTATTECOULEASTNORTHEASTHASTHASWISNINSUETBLYHICTEDDIABERLINCLOCKGANAMBEROCFOLUMZROFETQK",
   "known_in_place": 24
  },
  {
   "cell": "ct/B/38",
   "score": -5.75715,
   "above": 6,
   "copies": [
    -6.06328,
    -6.16675,
    -6.03957,
    -6.0975,
    -5.96189,
    -5.95392,
    -5.73977
   ],
   "reading": "??????????????????????????????????????HFDPLENBYDITVCBRGHGERICEOBERLINCLOCKRYLANATCGJHNNEWYOUTHARW",
   "known_in_place": 11
  },
  {
   "cell": "ct/B/36",
   "score": -5.81369,
   "above": 6,
   "copies": [
    -6.09005,
    -6.35154,
    -5.91139,
    -5.91723,
    -5.8488,
    -5.82423,
    -5.7187
   ],
   "reading": "????????????????????????????????????VJKAPOLETODPIEANZMLOANYBNARBERLINCLOCKJBAIILHAYTACKOPROTOWPGP",
   "known_in_place": 11
  },
  {
   "cell": "pt/B/24",
   "score": -5.04291,
   "above": 5,
   "copies": [
    -5.12581,
    -5.09847,
    -5.17161,
    -5.1162,
    -5.11161,
    -5.0225
   ],
   "reading": "BESENIOOBULORESOVALELEASTNORTHEASTENTCOYNENKOSRDAINSMTILIWLANALBERLINCLOCKMASMELUEALASHEHACTYEAKQ",
   "known_in_place": 24
  },
  {
   "cell": "ct/R/41",
   "score": -5.74879,
   "above": 5,
   "copies": [
    -6.01471,
    -6.16874,
    -5.91787,
    -5.90523,
    -5.8422,
    -5.74664
   ],
   "reading": "?????????????????????????????????????????TBKTLUDEEEBFAUMORAFDAMBERLINCLOCKWYOBRETZADICAPTSGAMASFU",
   "known_in_place": 11
  },
  {
   "cell": "ct/B/72",
   "score": -3.93251,
   "above": 4,
   "copies": [
    -3.99289,
    -4.17189,
    -3.94867,
    -4.13562,
    -3.88708
   ],
   "reading": "????????????????????????????????????????????????????????????????????????CKERATESMANRESTORINTENCOU",
   "known_in_place": 2
  },
  {
   "cell": "pt/R/35",
   "score": -4.40844,
   "above": 4,
   "copies": [
    -4.4147,
    -4.44344,
    -4.42028,
    -4.54403,
    -4.40005
   ],
   "reading": "DSINIENAGLUNTERETCHEREASTNORTHEASTGUATISTICESTORMIGHEFALEHATFUMBERLINCLOCKALDEDONASHISMATEDANGAOY",
   "known_in_place": 24
  },
  {
   "cell": "pt/B/23",
   "score": -5.10435,
   "above": 4,
   "copies": [
    -5.20701,
    -5.20833,
    -5.16343,
    -5.2541,
    -5.10146
   ],
   "reading": "JJTHADUSZEIFANOMAKEWIEASTNORTHEASTSFSAYUSBATMCCASTHEKISKGATIVESBERLINCLOCKATVDUFFEBELEONTCORORVLE",
   "known_in_place": 24
  },
  {
   "cell": "ct/B/56",
   "score": -5.44969,
   "above": 4,
   "copies": [
    -5.48732,
    -5.76409,
    -5.4964,
    -5.5031,
    -5.36751
   ],
   "reading": "????????????????????????????????????????????????????????SMMESGOBERLINCLOCKYCAKDZEYONEUPISEACCROWX",
   "known_in_place": 11
  },
  {
   "cell": "pt/R/19",
   "score": -5.45182,
   "above": 4,
   "copies": [
    -5.56597,
    -5.51609,
    -5.6813,
    -5.51825,
    -5.42067
   ],
   "reading": "XAMENAALASLEFGRALKLESEASTNORTHEASTHNONTKUNKLORACULOFPEGATOOAVATBERLINCLOCKSTARVGOHAWCLMGSDHYZHUJI",
   "known_in_place": 24
  },
  {
   "cell": "ct/B/46",
   "score": -5.71181,
   "above": 4,
   "copies": [
    -5.75146,
    -6.02822,
    -6.10473,
    -5.89335,
    -5.70286
   ],
   "reading": "??????????????????????????????????????????????FHITWITASHSBAPRITBERLINCLOCKEEGDOUMPUTENEWTXZBSOUDS",
   "known_in_place": 11
  },
  {
   "cell": "pt/V/39",
   "score": -4.32809,
   "above": 3,
   "copies": [
    -4.34798,
    -4.33375,
    -4.3312,
    -4.19725
   ],
   "reading": "ISRESCULARELYELONGINTEASTNORTHEASTIESTASTUTINCALTOPAYITANAMULTSBERLINCLOCKENTHENDSCALOTOFSINELALS",
   "known_in_place": 24
  },
  {
   "cell": "ct/B/64",
   "score": -4.81139,
   "above": 3,
   "copies": [
    -5.29403,
    -5.44572,
    -5.59584,
    -4.79087
   ],
   "reading": "????????????????????????????????????????????????????????????????ERLINCLOCKQUETATBENERMAYANTONSPYN",
   "known_in_place": 10
  },
  {
   "cell": "pt/R/22",
   "score": -5.28335,
   "above": 3,
   "copies": [
    -5.40505,
    -5.37034,
    -5.31138,
    -5.20903
   ],
   "reading": "DRIOLEUMACSTRALORSIDLEASTNORTHEASTHYRAISEELEDKWYIMPSPBUHNKERKFABERLINCLOCKSSOWYOFDAIRSPTYDOISEMFR",
   "known_in_place": 24
  },
  {
   "cell": "ct/B/41",
   "score": -5.70908,
   "above": 3,
   "copies": [
    -5.79137,
    -5.87047,
    -5.73386,
    -5.64102
   ],
   "reading": "?????????????????????????????????????????NWHYSFWHGENTMHURICDPROBERLINCLOCKEVKOIRLASONKACRTAGRAYUM",
   "known_in_place": 11
  },
  {
   "cell": "pt/R/51",
   "score": -3.9721,
   "above": 2,
   "copies": [
    -3.9739,
    -4.02887,
    -3.93974
   ],
   "reading": "RSONSTTURNERECTININESEASTNORTHEASTATEENTWASINTOTHESARERINTHESSOBERLINCLOCKEDTIVELICINGOFARTHERONP",
   "known_in_place": 24
  },
  {
   "cell": "ct/R/67",
   "score": -4.51949,
   "above": 2,
   "copies": [
    -4.6218,
    -4.77541,
    -4.28184
   ],
   "reading": "???????????????????????????????????????????????????????????????????INCLOCKEFINSBETOGETRIVEMADEIMA",
   "known_in_place": 7
  },
  {
   "cell": "pt/R/24",
   "score": -5.02934,
   "above": 2,
   "copies": [
    -5.116,
    -5.09593,
    -4.975
   ],
   "reading": "XYMAPANTHEWASABECEBYLEASTNORTHEASTPIHISTBADADYSLEHUSALSCKISONNDBERLINCLOCKVICULEAEVITESLEHPROFGEX",
   "known_in_place": 24
  },
  {
   "cell": "pt/B/18",
   "score": -5.50472,
   "above": 2,
   "copies": [
    -5.57705,
    -5.54004,
    -5.42024
   ],
   "reading": "ETUNPRASZIELDISTLOBETEASTNORTHEASTILNRIEINTNQMGIMSIWASUOSXVIXELBERLINCLOCKANRAMAELVOOOVENPANDVYSJ",
   "known_in_place": 24
  },
  {
   "cell": "ct/V/37",
   "score": -5.88602,
   "above": 2,
   "copies": [
    -5.91677,
    -5.99969,
    -5.66517
   ],
   "reading": "?????????????????????????????????????SICFMPARCHALHOEYETSGACAAEMBERLINCLOCKYCBEKEOOJOSGIFSOIWIABAZ",
   "known_in_place": 11
  },
  {
   "cell": "ct/V/72",
   "score": -3.88725,
   "above": 1,
   "copies": [
    -3.95694,
    -3.85625
   ],
   "reading": "????????????????????????????????????????????????????????????????????????CKSWITHNOTHEISTIONAUSENTH",
   "known_in_place": 2
  },
  {
   "cell": "pt/B/48",
   "score": -4.01949,
   "above": 1,
   "copies": [
    -4.11576,
    -3.99203
   ],
   "reading": "TATTHESLEADEASTSSASINEASTNORTHEASTRALSONSHAVETHENTTHERRENTANDOUBERLINCLOCKHEREFISHANADISCATITALHA",
   "known_in_place": 24
  },
  {
   "cell": "pt/B/50",
   "score": -4.021,
   "above": 1,
   "copies": [
    -4.05892,
    -3.9466
   ],
   "reading": "ANERTHEOTHERTOOLEAMESEASTNORTHEASTAURESTOHAVICEANDINGONENTEGINGBERLINCLOCKEACEANSANOTHEDINTRUSTOB",
   "known_in_place": 24
  },
  {
   "cell": "pt/V/51",
   "score": -4.04183,
   "above": 1,
   "copies": [
    -4.0715,
    -3.98631
   ],
   "reading": "EROTEDANDESWORRIREUNDEASTNORTHEASTENTHERTINISTOTHERINGELEADEMEMBERLINCLOCKOFHEPOLICWHEREATHEIROND",
   "known_in_place": 24
  },
  {
   "cell": "pt/B/44",
   "score": -4.1751,
   "above": 1,
   "copies": [
    -4.32911,
    -4.12924
   ],
   "reading": "ERBORYTHERTHEFOURTABREASTNORTHEASTHATHESFARINTALLENTIWASKICEREDBERLINCLOCKUTEDRENTHEATTHEANYTIMUY",
   "known_in_place": 24
  },
  {
   "cell": "pt/B/41",
   "score": -4.23275,
   "above": 1,
   "copies": [
    -4.33637,
    -4.21505
   ],
   "reading": "TSINDWITSHEYESSESTHEREASTNORTHEASTINVENOTOURPRECALEKALSOPLAINAMBERLINCLOCKALANAMILYBEAMERATEASILE",
   "known_in_place": 24
  },
  {
   "cell": "ct/V/69",
   "score": -4.37299,
   "above": 1,
   "copies": [
    -4.39278,
    -4.17102
   ],
   "reading": "?????????????????????????????????????????????????????????????????????CLOCKSTEREXINGEPFOREENTHETOH",
   "known_in_place": 5
  },
  {
   "cell": "ct/B/68",
   "score": -4.42893,
   "above": 1,
   "copies": [
    -4.53571,
    -4.37441
   ],
   "reading": "????????????????????????????????????????????????????????????????????NCLOCKIDEITTHEEASTEPENDINFLYS",
   "known_in_place": 6
  },
  {
   "cell": "pt/B/36",
   "score": -4.45744,
   "above": 1,
   "copies": [
    -4.46888,
    -4.33609
   ],
   "reading": "TTOPENRALLUSTREWONINTEASTNORTHEASTPERKSICALCOLOCRISTORTHIMOMLIMBERLINCLOCKERSASTANESARSAYOUCEMEBY",
   "known_in_place": 24
  },
  {
   "cell": "pt/V/35",
   "score": -4.50155,
   "above": 1,
   "copies": [
    -4.51378,
    -4.47023
   ],
   "reading": "ERSQUEDARYSMICBETOLEDEASTNORTHEASTCELINCKSOTHETHFIESONINONGANLABERLINCLOCKFIROMPESTINTETHEATERBAT",
   "known_in_place": 24
  },
  {
   "cell": "pt/V/30",
   "score": -4.59334,
   "above": 1,
   "copies": [
    -4.62693,
    -4.57536
   ],
   "reading": "MERATEDIMRYATSREWENTREASTNORTHEASTIPLANSISAREADBTOTHESCSHANOGAMBERLINCLOCKFOROVERESNEICNEWINAOSAA",
   "known_in_place": 24
  },
  {
   "cell": "pt/V/31",
   "score": -4.59915,
   "above": 1,
   "copies": [
    -4.61613,
    -4.57375
   ],
   "reading": "PNISSENDFLASPITARANGREASTNORTHEASTTISTHORONEDWEIRALLOSHOIKABACKBERLINCLOCKSEFORSARSTFIEASILIANRYN",
   "known_in_place": 24
  },
  {
   "cell": "pt/R/30",
   "score": -4.6055,
   "above": 1,
   "copies": [
    -4.6811,
    -4.49026
   ],
   "reading": "ZFSTPRODOAERISSUCHASTEASTNORTHEASTHANCIATEISEXAMPARTILHEAGERDEBBERLINCLOCKLANOOTAGEARRIFNONICEMGQ",
   "known_in_place": 24
  },
  {
   "cell": "ct/B/66",
   "score": -4.62916,
   "above": 1,
   "copies": [
    -4.77895,
    -4.53378
   ],
   "reading": "??????????????????????????????????????????????????????????????????LINCLOCKSONENTSINOTSHERANSMBMSR",
   "known_in_place": 8
  },
  {
   "cell": "pt/R/31",
   "score": -4.64611,
   "above": 1,
   "copies": [
    -4.64626,
    -4.62815
   ],
   "reading": "EOFINSEDILEUNOSCENINNEASTNORTHEASTIAMSLEETOBEHELINALATOMSANOPOFBERLINCLOCKERSANTAUGEOGTOCTAGEMYBY",
   "known_in_place": 24
  },
  {
   "cell": "ct/R/61",
   "score": -5.09154,
   "above": 1,
   "copies": [
    -5.47246,
    -4.82211
   ],
   "reading": "?????????????????????????????????????????????????????????????JBBERLINCLOCKATAMEXTEDAPAINICTIHLIBM",
   "known_in_place": 11
  },
  {
   "cell": "ct/B/61",
   "score": -5.25689,
   "above": 1,
   "copies": [
    -5.3203,
    -5.22104
   ],
   "reading": "?????????????????????????????????????????????????????????????FXBERLINCLOCKVEAREBOASANWECAPABPLEKR",
   "known_in_place": 11
  },
  {
   "cell": "ct/B/57",
   "score": -5.39607,
   "above": 1,
   "copies": [
    -5.45011,
    -5.15429
   ],
   "reading": "?????????????????????????????????????????????????????????RDNNUMBERLINCLOCKYOWISBDDIAGAREMAUCEIODH",
   "known_in_place": 11
  },
  {
   "cell": "ct/V/60",
   "score": -5.42379,
   "above": 1,
   "copies": [
    -5.63243,
    -5.17646
   ],
   "reading": "????????????????????????????????????????????????????????????DQDBERLINCLOCKHHALDERORCEMODERPAEKNLI",
   "known_in_place": 11
  },
  {
   "cell": "pt/R/21",
   "score": -5.51529,
   "above": 1,
   "copies": [
    -5.80542,
    -5.44983
   ],
   "reading": "EUACHMZECRYFWFFROUROKEASTNORTHEASTOTHATURYZOZHBYHZOOFNRICTECORUBERLINCLOCKGEADEAURGETUMADOJANDDIT",
   "known_in_place": 24
  },
  {
   "cell": "pt/R/18",
   "score": -5.60532,
   "above": 1,
   "copies": [
    -5.68242,
    -5.54301
   ],
   "reading": "ZLRUHSHOWCTWYMROSSERWEASTNORTHEASTTITTOYREIFFKGCTSIDEESRAXWBPHABERLINCLOCKMCESNEUMADETBBARYCUTANN",
   "known_in_place": 24
  },
  {
   "cell": "ct/V/41",
   "score": -5.6849,
   "above": 1,
   "copies": [
    -6.087,
    -5.65028
   ],
   "reading": "?????????????????????????????????????????LGAYYUJORVICTUBHTDELIABERLINCLOCKWIKEWRTSTDIDSCIRSOUSUWZ",
   "known_in_place": 11
  },
  {
   "cell": "ct/B/32",
   "score": -6.42624,
   "above": 1,
   "copies": [
    -6.75189,
    -6.39726
   ],
   "reading": "????????????????????????????????STOPNESSLEVXFHKYHUSWFECOVODPCCRBERLINCLOCKZALIIENGMAKEEYWTHRSGHLD",
   "known_in_place": 13
  },
  {
   "cell": "pt/B/11",
   "score": -7.00051,
   "above": 1,
   "copies": [
    -7.07381,
    -6.80599
   ],
   "reading": "JGXCMCIVANUICIQCTJHYREASTNORTHEASTENRYHEXWTNSFKPKGOYBHTRCTTHGAJBERLINCLOCKZBFHDDIMQYHOSHNZCCWVXGJ",
   "known_in_place": 24
  },
  {
   "cell": "ct/B/73",
   "score": -3.88171,
   "above": 0,
   "copies": [
    -3.70277
   ],
   "reading": "?????????????????????????????????????????????????????????????????????????KYEARACETHEPHONTHEAREFAC",
   "known_in_place": 1
  },
  {
   "cell": "pt/V/52",
   "score": -4.00577,
   "above": 0,
   "copies": [
    -3.94958
   ],
   "reading": "KHADONTIONORYCAPRATUREASTNORTHEASTHANDANDSTATEDINGTHESTESTHETANBERLINCLOCKINTHIREACROINTINEDSIDEU",
   "known_in_place": 24
  },
  {
   "cell": "pt/V/50",
   "score": -4.00837,
   "above": 0,
   "copies": [
    -3.99442
   ],
   "reading": "EATOTHESWASONEATTHEIMEASTNORTHEASTOWARTEDINTHERESANDOFITWASONEMBERLINCLOCKGILLEANDCHATANDGETLONDS",
   "known_in_place": 24
  },
  {
   "cell": "pt/R/50",
   "score": -4.02479,
   "above": 0,
   "copies": [
    -3.97203
   ],
   "reading": "IOUSEASTHARETOCOREATHEASTNORTHEASTHATISPRISTHESARESTALSFINEDTOMBERLINCLOCKFIVERTIOCAVEDTHESTEDAKR",
   "known_in_place": 24
  },
  {
   "cell": "pt/R/52",
   "score": -4.03157,
   "above": 0,
   "copies": [
    -4.02679
   ],
   "reading": "TITIMENTWOSIONINTSTAHEASTNORTHEASTICKAWASARESTOFTHERESHEWASASSIBERLINCLOCKERSTHENOCTTONSURERSINAP",
   "known_in_place": 24
  },
  {
   "cell": "ct/R/72",
   "score": -4.03479,
   "above": 0,
   "copies": [
    -3.92805
   ],
   "reading": "????????????????????????????????????????????????????????????????????????CKDISTEREDININTEENAUGHTHA",
   "known_in_place": 2
  },
  {
   "cell": "pt/B/49",
   "score": -4.0396,
   "above": 0,
   "copies": [
    -4.03217
   ],
   "reading": "STENDREATESHASSCONTHEEASTNORTHEASTONSLASHERINRUNTHISTHERARYSTONBERLINCLOCKELAKETERSENTERAMPERTHEY",
   "known_in_place": 24
  },
  {
   "cell": "pt/B/51",
   "score": -4.04631,
   "above": 0,
   "copies": [
    -4.01375
   ],
   "reading": "MFEWILLANETHESLIDCALLEASTNORTHEASTHESEFFERETINGANDTHEREDENTOBERBERLINCLOCKAYCAROLDMINGINTHISWISAT",
   "known_in_place": 24
  },
  {
   "cell": "ct/R/73",
   "score": -4.0647,
   "above": 0,
   "copies": [
    -3.7734
   ],
   "reading": "?????????????????????????????????????????????????????????????????????????KEANIZETHESAREUROTHOULDD",
   "known_in_place": 1
  },
  {
   "cell": "pt/R/47",
   "score": -4.07735,
   "above": 0,
   "copies": [
    -4.07723
   ],
   "reading": "ATOTHETHERSTRANINGARSEASTNORTHEASTTHERASASASSETTSARSAMEMENSEVENBERLINCLOCKILCATORYAMESTORONGTHENJ",
   "known_in_place": 24
  },
  {
   "cell": "pt/V/48",
   "score": -4.08983,
   "above": 0,
   "copies": [
    -4.00823
   ],
   "reading": "UNTERENTONEDPOISEAKETEASTNORTHEASTATHERGELLINESASANGEBUTHATALSOBERLINCLOCKOSTTHEMASTOVERSTOPERANT",
   "known_in_place": 24
  },
  {
   "cell": "pt/V/49",
   "score": -4.09348,
   "above": 0,
   "copies": [
    -4.08675
   ],
   "reading": "NCIALATTERINALLERINICEASTNORTHEASTATIVEDHASTHINTHERESTEDINETTOABERLINCLOCKARAKOSHOCRISEARSTHERIER",
   "known_in_place": 24
  },
  {
   "cell": "pt/B/47",
   "score": -4.11477,
   "above": 0,
   "copies": [
    -4.0537
   ],
   "reading": "OSHEFIRETINTSONEANCESEASTNORTHEASTKICESSEDTOTRISHINGENESULATEDABERLINCLOCKTHEROFULLTHEDESTATHEBIO",
   "known_in_place": 24
  },
  {
   "cell": "pt/R/48",
   "score": -4.11927,
   "above": 0,
   "copies": [
    -4.06346
   ],
   "reading": "CESTHREANETHEKABLISEVEASTNORTHEASTWORTHENBUTTHERENEVENTWINGVERSBERLINCLOCKCOMEWEEVERWHETHEPRIERCY",
   "known_in_place": 24
  },
  {
   "cell": "pt/B/46",
   "score": -4.12616,
   "above": 0,
   "copies": [
    -4.11971
   ],
   "reading": "PSIVERAILOMTHEDONERINEASTNORTHEASTERSTHISONTOFTENTIRECTERECTONTBERLINCLOCKSAREEFIRMONTTHAPRIALEEP",
   "known_in_place": 24
  },
  {
   "cell": "pt/R/44",
   "score": -4.13422,
   "above": 0,
   "copies": [
    -4.12608
   ],
   "reading": "NMOVERINTHESTFORELITYEASTNORTHEASTORDONTOFTWILLENCOMELATORALISTBERLINCLOCKNETELEAREASTERIEMAIRPSY",
   "known_in_place": 24
  },
  {
   "cell": "pt/B/45",
   "score": -4.13509,
   "above": 0,
   "copies": [
    -4.09741
   ],
   "reading": "EONDELAGERATENTTOTHAVEASTNORTHEASTILANDAPERMARILANTHEVERENTEROUBERLINCLOCKOURAZETHOFTERESSINANODE",
   "known_in_place": 24
  },
  {
   "cell": "pt/R/46",
   "score": -4.17831,
   "above": 0,
   "copies": [
    -4.15857
   ],
   "reading": "WEATRUSINALONDEVEDNINEASTNORTHEASTRACETHEYANDMODENTINERTEDINGASBERLINCLOCKATARECTURASTWHORTOROPST",
   "known_in_place": 24
  },
  {
   "cell": "ct/V/70",
   "score": -4.22819,
   "above": 0,
   "copies": [
    -4.15372
   ],
   "reading": "??????????????????????????????????????????????????????????????????????LOCKSAGEMONTHANDLIKEHINKANW",
   "known_in_place": 4
  },
  {
   "cell": "ct/V/73",
   "score": -4.2426,
   "above": 0,
   "copies": [
    -3.84044
   ],
   "reading": "?????????????????????????????????????????????????????????????????????????KMARIZOTHESENTUSESHANDNO",
   "known_in_place": 1
  },
  {
   "cell": "ct/B/70",
   "score": -4.2553,
   "above": 0,
   "copies": [
    -4.22922
   ],
   "reading": "??????????????????????????????????????????????????????????????????????LOCKENGASUPLITTHETHENTAKECL",
   "known_in_place": 4
  },
  {
   "cell": "pt/R/39",
   "score": -4.30875,
   "above": 0,
   "copies": [
    -4.30508
   ],
   "reading": "KINAPATEAREDASADTOETREASTNORTHEASTURMUSETABITORLITERENDENTRYSIABERLINCLOCKINDERLYNEENEDINEVESANDA",
   "known_in_place": 24
  },
  {
   "cell": "pt/B/39",
   "score": -4.32451,
   "above": 0,
   "copies": [
    -4.26841
   ],
   "reading": "ASISLICASTOSWELSOSHOSEASTNORTHEASTATIONWEDIANALCADURRITASONSARMBERLINCLOCKATAMATHOUSAPACTIMENSUPP",
   "known_in_place": 24
  },
  {
   "cell": "ct/R/70",
   "score": -4.33852,
   "above": 0,
   "copies": [
    -4.21626
   ],
   "reading": "??????????????????????????????????????????????????????????????????????LOCKSWERSOROGRANDATHEASKNOQ",
   "known_in_place": 4
  },
  {
   "cell": "pt/R/38",
   "score": -4.41219,
   "above": 0,
   "copies": [
    -4.37683
   ],
   "reading": "DPATRANESTILEAGARTEDHEASTNORTHEASTCPWHISTMIXISLESINTHITSANDAMADBERLINCLOCKINTEENBROUNTERAHORNEWMH",
   "known_in_place": 24
  },
  {
   "cell": "pt/R/37",
   "score": -4.41723,
   "above": 0,
   "copies": [
    -4.36773
   ],
   "reading": "ECORDANNINTMONONTDINGEASTNORTHEASTMALIGASAPROWALAYMEDTOTHEGOREKBERLINCLOCKFORITICEPRIEARSONTITNEG",
   "known_in_place": 24
  },
  {
   "cell": "pt/V/36",
   "score": -4.42497,
   "above": 0,
   "copies": [
    -4.41965
   ],
   "reading": "ITRANCALITANDINNOVAELEASTNORTHEASTREEMILEPLANDSFROSESEDANDUPVANBERLINCLOCKELAPROSPRIADOREREDITHKC",
   "known_in_place": 24
  },
  {
   "cell": "pt/V/38",
   "score": -4.42888,
   "above": 0,
   "copies": [
    -4.34262
   ],
   "reading": "YNNDANDUSOFMEDADENHOMEASTNORTHEASTOBEITALONARELIVENTDESINONEXARBERLINCLOCKLEEDSHEENTRENSCANSUSROO",
   "known_in_place": 24
  },
  {
   "cell": "pt/B/37",
   "score": -4.43232,
   "above": 0,
   "copies": [
    -4.3292
   ],
   "reading": "ZPICHTROBEMENIONETOGREASTNORTHEASTHARANTSIDITHATUKSCALAKEJULANDBERLINCLOCKENSINESBEHOUGHISESSOOOF",
   "known_in_place": 24
  },
  {
   "cell": "pt/V/37",
   "score": -4.46463,
   "above": 0,
   "copies": [
    -4.46215
   ],
   "reading": "NHOUTLEMOREEHITHMENAVEASTNORTHEASTHOWACKISINASASAVEDREDITHATAYOBERLINCLOCKEMETERACKUPONDSOFEGIAWB",
   "known_in_place": 24
  },
  {
   "cell": "ct/B/67",
   "score": -4.54466,
   "above": 0,
   "copies": [
    -4.40351
   ],
   "reading": "???????????????????????????????????????????????????????????????????INCLOCKAGOTOFFFINABENDSETOUSEC",
   "known_in_place": 7
  },
  {
   "cell": "pt/B/33",
   "score": -4.56436,
   "above": 0,
   "copies": [
    -4.45907
   ],
   "reading": "SENSASDRISTROINTERINFEASTNORTHEASTINJADBUNTRONSDEFRESOUSIAMPLYABERLINCLOCKMDANDODRIAOANTERTARESTD",
   "known_in_place": 24
  },
  {
   "cell": "pt/R/34",
   "score": -4.575,
   "above": 0,
   "copies": [
    -4.48713
   ],
   "reading": "YYEGANDCHASTERADVINIVEASTNORTHEASTOTRASYCOOINHOLBEROSSESVIKAHAMBERLINCLOCKNEWERINGUSTEDATANDYMADB",
   "known_in_place": 24
  },
  {
   "cell": "pt/V/34",
   "score": -4.57722,
   "above": 0,
   "copies": [
    -4.52358
   ],
   "reading": "ZMTHESALLFISLETODAYSTEASTNORTHEASTUSTKLISENTERTATHOSLOOKBYTOLLEBERLINCLOCKERTCARISHANBYTEATEMAXFH",
   "known_in_place": 24
  },
  {
   "cell": "ct/R/69",
   "score": -4.60268,
   "above": 0,
   "copies": [
    -4.15303
   ],
   "reading": "?????????????????????????????????????????????????????????????????????CLOCKTOREEXISTRANOBOWELORFOC",
   "known_in_place": 5
  },
  {
   "cell": "pt/B/32",
   "score": -4.60597,
   "above": 0,
   "copies": [
    -4.54224
   ],
   "reading": "YIFEPISBRATITJUMANARCEASTNORTHEASTANESTMAHATICANFLEADMYIELTONGIBERLINCLOCKFUNDINGORMICTOFUSEDIVIC",
   "known_in_place": 24
  },
  {
   "cell": "pt/V/33",
   "score": -4.62163,
   "above": 0,
   "copies": [
    -4.56399
   ],
   "reading": "RUNOPANJIMARELECTIONYEASTNORTHEASTHANETEDKICARELYSHATTOMASOPPONBERLINCLOCKTOTHMUGEMESUNEKATETSJIT",
   "known_in_place": 24
  },
  {
   "cell": "pt/V/32",
   "score": -4.623,
   "above": 0,
   "copies": [
    -4.52775
   ],
   "reading": "NYTIODDISQUITATETWOAPEASTNORTHEASTFOTHEEANCELOALOTISSEASSATLEBYBERLINCLOCKIRCATHITISTRODRAWONDRUP",
   "known_in_place": 24
  },
  {
   "cell": "pt/R/32",
   "score": -4.63041,
   "above": 0,
   "copies": [
    -4.60632
   ],
   "reading": "ICLUBINIRARESBESLEDEREASTNORTHEASTCERTESAIDCCALYINGTEARATBARARSBERLINCLOCKYANTRATLAGEFEROCHONETXP",
   "known_in_place": 24
  },
  {
   "cell": "pt/B/30",
   "score": -4.63555,
   "above": 0,
   "copies": [
    -4.5645
   ],
   "reading": "WPRESOUSINNSARKEANDSKEASTNORTHEASTBHOARALIDSTDANATEVEPHRREENCYOBERLINCLOCKERSPASSANINHIGOTHEMONEH",
   "known_in_place": 24
  },
  {
   "cell": "pt/R/33",
   "score": -4.641,
   "above": 0,
   "copies": [
    -4.58025
   ],
   "reading": "LRLONESMOUSAVERYINSHREASTNORTHEASTGWHATEUNSEVEANDMAISSEODDIEOONBERLINCLOCKIALEANANGONANEWDOINDASI",
   "known_in_place": 24
  },
  {
   "cell": "ct/V/67",
   "score": -4.68434,
   "above": 0,
   "copies": [
    -4.24618
   ],
   "reading": "???????????????????????????????????????????????????????????????????INCLOCKEXPARESSOINTIORNEERNPET",
   "known_in_place": 7
  },
  {
   "cell": "pt/B/26",
   "score": -4.77914,
   "above": 0,
   "copies": [
    -4.76432
   ],
   "reading": "BTRANORSESIRASCOTHOUNEASTNORTHEASTSSURSTSINANILFOFTBAYICATIURAMBERLINCLOCKSAALYEISMATHEERHIASSRHO",
   "known_in_place": 24
  },
  {
   "cell": "pt/R/25",
   "score": -4.84872,
   "above": 0,
   "copies": [
    -4.80535
   ],
   "reading": "SGEANLWINTIRITYORKRINEASTNORTHEASTITYTHRECOWERWBIREEMAWAAKNIEALBERLINCLOCKYSAIBERGELISSHTITHERSOA",
   "known_in_place": 24
  },
  {
   "cell": "pt/R/26",
   "score": -4.89017,
   "above": 0,
   "copies": [
    -4.82447
   ],
   "reading": "PEMWEIGHTTERNAMESALOFEASTNORTHEASTRAOMRESDPETISGNEAXINGUNLYSLINBERLINCLOCKHESHEWTHAELSODELUOTAARN",
   "known_in_place": 24
  },
  {
   "cell": "pt/B/25",
   "score": -4.94078,
   "above": 0,
   "copies": [
    -4.92487
   ],
   "reading": "FSSEUHOSTHGPAUAJUNGLLEASTNORTHEASTANDPIASINGUNNOURILOUNDIDFISLABERLINCLOCKWAYAGATTHESINFOBUEMESAZ",
   "known_in_place": 24
  },
  {
   "cell": "ct/V/64",
   "score": -5.03876,
   "above": 0,
   "copies": [
    -4.95768
   ],
   "reading": "????????????????????????????????????????????????????????????????ERLINCLOCKREEDBMRSBEGRITESCALBLEV",
   "known_in_place": 10
  },
  {
   "cell": "pt/R/23",
   "score": -5.19904,
   "above": 0,
   "copies": [
    -5.19728
   ],
   "reading": "JHISPLGINOPOOYISPARIDEASTNORTHEASTOTOROTEXPFULLSCAOUNGKFRAMILFABERLINCLOCKAHURENHAMEANTCARGOZBCIE",
   "known_in_place": 24
  },
  {
   "cell": "ct/R/60",
   "score": -5.42605,
   "above": 0,
   "copies": [
    -5.25143
   ],
   "reading": "????????????????????????????????????????????????????????????JUYBERLINCLOCKAKACHAOTHSTIMSUMMIEKLDT",
   "known_in_place": 11
  },
  {
   "cell": "pt/B/19",
   "score": -5.56174,
   "above": 0,
   "copies": [
    -5.35947
   ],
   "reading": "QWNSQURDCDLFICIEUREADEASTNORTHEASTAVEUENPEDOFWCRYOFVUNREMOLSXXLBERLINCLOCKIFORGDAYVEIMAAACEMCAMED",
   "known_in_place": 24
  },
  {
   "cell": "ct/B/52",
   "score": -5.61233,
   "above": 0,
   "copies": [
    -5.55883
   ],
   "reading": "????????????????????????????????????????????????????EZIKIILANAGBERLINCLOCKCALTNRLDIENTERLRAKITLDV",
   "known_in_place": 11
  },
  {
   "cell": "ct/B/59",
   "score": -5.61397,
   "above": 0,
   "copies": [
    -5.53936
   ],
   "reading": "???????????????????????????????????????????????????????????IAUBBERLINCLOCKBFAQBGSECTWASAFEATAKUTM",
   "known_in_place": 11
  },
  {
   "cell": "pt/R/17",
   "score": -5.61812,
   "above": 0,
   "copies": [
    -5.27523
   ],
   "reading": "TSYLOTEPXKSYUSECFZAMNEASTNORTHEASTVEYSLOCKJGSCONSODYARBECARRATBBERLINCLOCKSCULREGGREGAKSTULBEWLNS",
   "known_in_place": 24
  },
  {
   "cell": "ct/B/48",
   "score": -5.66238,
   "above": 0,
   "copies": [
    -5.5544
   ],
   "reading": "????????????????????????????????????????????????BPEXITADESOWFPWBERLINCLOCKRIELGSCONORAKEFFIEZZERI",
   "known_in_place": 11
  },
  {
   "cell": "pt/B/17",
   "score": -5.68115,
   "above": 0,
   "copies": [
    -5.63496
   ],
   "reading": "JHLCICKKISSANDEMYFACREASTNORTHEASTPRROSWBLFMKNYTSDHMESQAINISTABBERLINCLOCKLYANNIURDNHRGOOPFOLUEYB",
   "known_in_place": 24
  },
  {
   "cell": "pt/B/15",
   "score": -5.75213,
   "above": 0,
   "copies": [
    -5.71323
   ],
   "reading": "SCCEGESKYOYHIAGIAJPCAEASTNORTHEASTBRARMWOCHWSELDSZIBRFBAATKLINTBERLINCLOCKVELTAGIALLAHOEUSWTOABST",
   "known_in_place": 24
  },
  {
   "cell": "ct/B/47",
   "score": -5.79723,
   "above": 0,
   "copies": [
    -5.78147
   ],
   "reading": "???????????????????????????????????????????????NALSNSFFULOISPUDBERLINCLOCKMULBCEAPISCIOSTLTARPVKM",
   "known_in_place": 11
  },
  {
   "cell": "pt/R/16",
   "score": -5.86276,
   "above": 0,
   "copies": [
    -5.7713
   ],
   "reading": "NKBFTBFVUPRNMOCHDNSECEASTNORTHEASTWIHIIEDSWHIANHANCEAXREIDPODBXBERLINCLOCKBIDCETIFIIDERYUZURESTNP",
   "known_in_place": 24
  },
  {
   "cell": "pt/B/16",
   "score": -5.94694,
   "above": 0,
   "copies": [
    -5.76256
   ],
   "reading": "IVOWTUCRHEYFLFILSTLTUEASTNORTHEASTUSAIDSOYORROUTPFPEGTXNDIRNIFKBERLINCLOCKFGRIDNITYRHYAAPUEDUKPXD",
   "known_in_place": 24
  },
  {
   "cell": "pt/R/14",
   "score": -6.26035,
   "above": 0,
   "copies": [
    -5.99296
   ],
   "reading": "HPANKPRPMXPODBSCBCTREEASTNORTHEASTMENSQZGFSYDFMZYKNBCINYARLTRUGBERLINCLOCKENCTASLEHEXDAHNYZUKNRKA",
   "known_in_place": 24
  },
  {
   "cell": "pt/V/15",
   "score": -6.33401,
   "above": 0,
   "copies": [
    -5.97918
   ],
   "reading": "IBFEESNNGOVGTPALXIWWTEASTNORTHEASTDIHEUWCGRWRTOYSRTWTRPHRDIGGRPBERLINCLOCKXIXHPENQCQUESONTATRHSOY",
   "known_in_place": 24
  },
  {
   "cell": "pt/B/13",
   "score": -6.39227,
   "above": 0,
   "copies": [
    -6.37837
   ],
   "reading": "WJMQWKBFIERMIWANRHOSTEASTNORTHEASTDNDSCOLKHEVGURZWHUASVAUQYOHTDBERLINCLOCKBLTHAFOYSKHBSPYZDBEAHBX",
   "known_in_place": 24
  },
  {
   "cell": "pt/R/13",
   "score": -6.52443,
   "above": 0,
   "copies": [
    -6.24313
   ],
   "reading": "RKUEOWFIWBPCXRTRYJYSTEASTNORTHEASTZVWNJOUMHEXKOHUKDDTRYTYPLASAQBERLINCLOCKKIFOQTHAPJARNDFAIFSZSCU",
   "known_in_place": 24
  },
  {
   "cell": "pt/V/14",
   "score": -6.55742,
   "above": 0,
   "copies": [
    -6.23898
   ],
   "reading": "KJUPBUITGTPPCFSTZILUTEASTNORTHEASTRUVXDYGGUILIANNPMFVONSZMWLUCMBERLINCLOCKMTTJYZTSERIBYEDFOSPNABP",
   "known_in_place": 24
  },
  {
   "cell": "pt/B/14",
   "score": -6.6383,
   "above": 0,
   "copies": [
    -6.30767
   ],
   "reading": "ASXJAIRXNAJMREIJKOEOPEASTNORTHEASTYLJOMWEOJIXKUGRYVEORGZUJGASKSBERLINCLOCKDEWGCREAFOPGTOBGOJNDZXN",
   "known_in_place": 24
  },
  {
   "cell": "pt/V/13",
   "score": -6.74853,
   "above": 0,
   "copies": [
    -6.56966
   ],
   "reading": "ABWLIEBZNBRECPRZUCOSIEASTNORTHEASTDIWSCLTAWRRKWNZYTURNAKJHQVSGTBERLINCLOCKJMPBIZABSMNESDNXCOQOHAH",
   "known_in_place": 24
  },
  {
   "cell": "pt/V/12",
   "score": -7.00518,
   "above": 0,
   "copies": [
    -6.41756
   ],
   "reading": "CYGIKSIPWZRRYLCQVFKZSEASTNORTHEASTVTKECWPITUEGIFTFIOVQQCEQLLTSKBERLINCLOCKTTICLUENBFHEGQDLWSSBLEO",
   "known_in_place": 24
  },
  {
   "cell": "pt/B/10",
   "score": -7.04864,
   "above": 0,
   "copies": [
    -6.88051
   ],
   "reading": "NNRJLMWTKTXLWCVXYHRVSEASTNORTHEASTENNRULBQTJTSWFOZBLRFQHYINEAEWBERLINCLOCKQSNEWBLGTXBESPSVZFOLIKN",
   "known_in_place": 24
  },
  {
   "cell": "pt/R/11",
   "score": -7.13549,
   "above": 0,
   "copies": [
    -6.74956
   ],
   "reading": "OHILPHPRTVOYUHYVNMDRMEASTNORTHEASTMSQGIQQQTLTANACPLMFWNJPCLRRHEBERLINCLOCKXGCPBPNUVXOLNOCTFGUUFJX",
   "known_in_place": 24
  },
  {
   "cell": "pt/B/12",
   "score": -7.23395,
   "above": 0,
   "copies": [
    -6.96432
   ],
   "reading": "WUREFNPYGZHZIQYGOHJZDEASTNORTHEASTXTQYXPFETEYXOGEMMBSGOYTGIHEWKBERLINCLOCKMIYESEYEUKIGBPPWVWCVXTQ",
   "known_in_place": 24
  },
  {
   "cell": "pt/B/8",
   "score": -7.54609,
   "above": 0,
   "copies": [
    -7.22448
   ],
   "reading": "TXXZKJJUGBYHMKBETOWXDEASTNORTHEASTVHFKYZZBUJIVCVQLAVRDULNXLGJQIBERLINCLOCKECXYYUZUPGWHLVLVGQCTONR",
   "known_in_place": 24
  }
 ],
 "core_seconds": 195282,
 "compute_seconds": 8560,
 "exhaustive": true,
 "exhaustive_over": "every (kind, form, lag) cell where K4 fits 0149's exact decider, decided at the measured power",
 "not_covered": "0149's 7 undecided cells (node limit); the move-first version (about 176 million exact searches)"
}
```

Notes: F1.7: 130 cells; K4 valid readings 130; above all 12 copies in 7 (fair test 10.0); among 10 stand-ins 6 at or above K4's rate (p 0.64), above all 100 in 0; plant power ct/clean 6/12, ct/sanborn 2/12, ct_tempering 8/24, pt/clean 1/12, pt/sanborn 3/12, pt_tempering 4/24. No candidate returned (ciphertext-autokey readings have open primer letters; per-cell copies do not account for the cells searched).


