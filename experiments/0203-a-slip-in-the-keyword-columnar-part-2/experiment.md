# 0203-a-slip-in-the-keyword-columnar-part-2: F6.21, part 2 (trapezoid, row reshuffle, poem code): a deliberate slip in the keyword columnar (one column read out of its place, or two columns swapped), around every keyword columnar already tested, then or before a repeating key on the table, exact, with planted slips in the same run

**Family:** 6-transposition-then-tableau  
**Parent:** 0202-a-slip-in-the-keyword-columnar  
**Decision:** reverted  
**Run:** 2026-10-20T10:40:48+00:00, 610.5 s, status ran  
**Time by phase:** unattributed 56 s, run 610 s, record 0 s

## In plain words

Agents in the war often made one mistake when they copied out a transposition: they numbered the key word wrongly and read one column at the wrong time, or read two columns in each other's place. Sanborn says he made mistakes on purpose. We take every column shuffle the project has already ruled out and try it again with each such single mistake, followed or preceded by a short repeating key word on the sculpture's table.

## Walkthrough, by hand

1. Take the key word SHADOW: alphabetical order A D H O S W numbers the columns 5 3 2 6 4 1... read in the order 3, 4, 2, 5, 1, 6.
2. Make one slip: read column 2 one step early (3, 2, 4, 5, 1, 6), or swap columns 3 and 5.
3. Write the 97 letters in rows of 6 and copy out the columns in the slipped order.
4. Encipher on the table with a repeating key, or encipher first.
5. Follow each known letter to its carved place; known letters that share a key slot must agree.

## Worked example (generated)

```
key word SHADOW: columns read in the order [3, 4, 2, 5, 1, 6]
one slip, the third column read one step early: [3, 2, 4, 5, 1, 6]

place  known  lands at  carved
   22      E        36       T
   26      N        21       W
   34      T        38       T
   64      B        43       S
   74      K        29       R
```

## Lineage

Inherits from 0202-a-slip-in-the-keyword-columnar. What changed: 0202 ran out of its 30 minutes after three of the six base families (single and double keyword columnar, interrupted key); the other three were skipped by its time check. Here the same search, unchanged, on those three: 0164's trapezoid (F6.17), 0165's letters reshuffled inside each row (F6.18), 0190's poem code (F11.2, the slip in either pass), each with its own planted slipped text in the same run. Then a repeating key 1-26 on the standard or KRYPTOS table after (A) or before (B), 8 classes, ten scrambled copies.

## Hypothesis (domain expert)

C1(a), C5, C10 ('mistakes on purpose'; misspellings as security checks in SOE practice, Marks p. 16). Source: reports/marks-between-silk-and-cyanide.md. Model: c = T(sigma'(p)) or sigma'(T(p)), sigma' a keyword columnar (or two passes) whose column reading order differs from the keyword's by one move of one column (g(g-1) orders) or one swap of two non-adjacent columns ((g-1)(g-2)/2; adjacent swaps are moves), in one pass. A skipped or doubled column alone changes the length (97 would need a message of 97 plus or minus a column, or two compensating slips): not searched. Not included: Myszkowski, AMSCO, keyed blanks, triangle and disrupted columnars (not on the item's list). Each slipped route is tested exactly as 0110 tested its routes: periods 1-26, both orders, 8 classes, by slot agreement of the 24 known letters, forward and inverse. Statistic (0134's, fixed): per base family, the shortest key length consistent on K4 against the copies, and the cells (order, length) where K4 exceeds every copy, against each copy's own count. Routes are counted per slip, not deduplicated across words (copies counted the same way).

## Prediction

For each base family, nothing consistent below key length 20 beyond the copies' rate, and K4 above every copy in no more cells than a copy is. Each planted slip is found at its own setting. Zero candidates.

## Method

1. Rebuild each base family's column groups and reading order with the experiments' own builders.
2. In compiled code, for every base, every slip of the reading order (one column moved, two swapped) in each pass, build the route and its inverse.
3. Test each with the 0110/0164 periodic-key test, orders A and B, 8 classes, periods 1-26, on K4, ten copies and four planted texts; checked against Python on sample routes.
4. The fixed statistic per base family; each plant must show its own slip live at its own length.

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
 "family": "one slip (a column moved or two swapped) in the reading order of every keyword columnar already closed, then or before a periodic key",
 "bases_per_family": {
  "F6.17 trapezoid": 44854,
  "F6.18 row reshuffle": 181306,
  "F11.2 poem code": 6102
 },
 "families": {
  "F6.17 trapezoid": {
   "bases": 44854,
   "routes": 26006376,
   "k4_live_by_period": {
    "A": [
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
     2,
     8,
     19,
     279,
     275,
     1202
    ],
    "B": [
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
     8,
     14674,
     8002290
    ]
   },
   "controls_live_by_period_min": {
    "A": [
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
     4,
     11,
     211,
     250,
     1156
    ],
    "B": [
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
     3,
     9168,
     7881805
    ]
   },
   "controls_live_by_period_max": {
    "A": [
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
     18,
     73,
     150,
     328,
     304,
     1488
    ],
    "B": [
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
     21,
     13707,
     8048171
    ]
   },
   "k4_shortest_live": {
    "A": 21,
    "B": 24
   },
   "coppers_shortest_live": {
    "A": 21,
    "B": 24
   },
   "k4_settings_live_below_20": {
    "A": 0,
    "B": 0
   },
   "controls_settings_live_below_20": {
    "A": [
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
    ],
    "B": [
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
   "k4_live_below_20": [],
   "cells_k4_above_every_copper": [
    [
     "B",
     25
    ]
   ],
   "null_cells_above_rest_per_copper": [
    1,
    0,
    1,
    1,
    1,
    0,
    1,
    0,
    1,
    1
   ],
   "stop_queue": false
  },
  "F6.18 row reshuffle": {
   "bases": 181306,
   "routes": 121696528,
   "k4_live_by_period": {
    "A": [
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
     3,
     1,
     88,
     701,
     6075,
     2381,
     134128,
     5363709
    ],
    "B": [
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
     451,
     64644,
     39259472
    ]
   },
   "controls_live_by_period_min": {
    "A": [
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
     11,
     246,
     2610,
     1756,
     129913,
     532252
    ],
    "B": [
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
     28,
     47553,
     30744591
    ]
   },
   "controls_live_by_period_max": {
    "A": [
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
     4,
     39,
     628,
     5313,
     2725,
     171523,
     3628137
    ],
    "B": [
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
     2,
     0,
     0,
     0,
     0,
     0,
     0,
     351,
     93486,
     41579686
    ]
   },
   "k4_shortest_live": {
    "A": 19,
    "B": 24
   },
   "coppers_shortest_live": {
    "A": 19,
    "B": 17
   },
   "k4_settings_live_below_20": {
    "A": 3,
    "B": 0
   },
   "controls_settings_live_below_20": {
    "A": [
     0,
     0,
     0,
     0,
     0,
     1,
     0,
     0,
     0,
     0
    ],
    "B": [
     0,
     0,
     0,
     0,
     0,
     0,
     2,
     0,
     0,
     0
    ]
   },
   "k4_live_below_20": [
    {
     "base": 85791,
     "slip": [
      1,
      0,
      5,
      3
     ],
     "order": "A",
     "class": "std/kry/vig-var",
     "period": 19
    },
    {
     "base": 89202,
     "slip": [
      1,
      0,
      9,
      4
     ],
     "order": "A",
     "class": "std/kry/vig-var",
     "period": 19
    },
    {
     "base": 89223,
     "slip": [
      1,
      1,
      3,
      8
     ],
     "order": "A",
     "class": "std/kry/vig-var",
     "period": 19
    }
   ],
   "cells_k4_above_every_copper": [
    [
     "A",
     19
    ],
    [
     "A",
     21
    ],
    [
     "A",
     22
    ],
    [
     "A",
     23
    ],
    [
     "A",
     26
    ],
    [
     "B",
     24
    ]
   ],
   "null_cells_above_rest_per_copper": [
    0,
    1,
    0,
    1,
    0,
    1,
    1,
    1,
    0,
    0
   ],
   "stop_queue": true
  },
  "F11.2 poem code": {
   "bases": 6102,
   "routes": 3755770,
   "k4_live_by_period": {
    "A": [
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
     21,
     14,
     996,
     648,
     4345
    ],
    "B": [
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
     2,
     1919,
     1183507
    ]
   },
   "controls_live_by_period_min": {
    "A": [
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
     2,
     5,
     751,
     646,
     4298
    ],
    "B": [
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
     1128,
     1134973
    ]
   },
   "controls_live_by_period_max": {
    "A": [
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
     5,
     13,
     88,
     1163,
     763,
     6655
    ],
    "B": [
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
     96,
     2276,
     1181224
    ]
   },
   "k4_shortest_live": {
    "A": 22,
    "B": 24
   },
   "coppers_shortest_live": {
    "A": 20,
    "B": 24
   },
   "k4_settings_live_below_20": {
    "A": 0,
    "B": 0
   },
   "controls_settings_live_below_20": {
    "A": [
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
    ],
    "B": [
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
   "k4_live_below_20": [],
   "cells_k4_above_every_copper": [
    [
     "A",
     22
    ],
    [
     "B",
     26
    ]
   ],
   "null_cells_above_rest_per_copper": [
    2,
    2,
    0,
    1,
    0,
    0,
    1,
    1,
    1,
    0
   ],
   "stop_queue": false
  }
 },
 "plants": [
  {
   "family": "F6.17 trapezoid",
   "base": "NONMAINTENANCE",
   "slip": [
    0,
    9,
    6
   ],
   "order": "B",
   "class": "std/std/beau",
   "length": 7,
   "found": true,
   "shortest_live_at_own_setting": 7,
   "other_live_settings_below_20": 0
  },
  {
   "family": "F6.18 row reshuffle",
   "base": "SWANWORT",
   "slip": [
    0,
    5,
    0
   ],
   "order": "A",
   "class": "kry/kry/vig-var",
   "length": 6,
   "found": true,
   "shortest_live_at_own_setting": 6,
   "other_live_settings_below_20": 135
  },
  {
   "family": "F11.2 poem code",
   "base": "K2 words 31-35 split after 4 pass 2",
   "slip": [
    1,
    0,
    5
   ],
   "order": "B",
   "class": "std/kry/vig-var",
   "length": 9,
   "found": true,
   "shortest_live_at_own_setting": 9,
   "other_live_settings_below_20": 0
  }
 ],
 "controls": "10 shuffled copies (seed 1621), 3 planted slipped texts in the same run",
 "not_searched": "a skipped or doubled column alone (changes the length); Myszkowski, AMSCO, keyed blanks, triangle and disrupted columnars (not on the item's list)",
 "seconds": 610,
 "exhaustive": "exact per family done (see skipped)"
}
```

Notes: F6.17 trapezoid: 26,006,376 routes, shortest live A 21 B 24 (copies {'A': 21, 'B': 24}), K4 above every copy 1 (null max 1); F6.18 row reshuffle: 121,696,528 routes, shortest live A 19 B 24 (copies {'A': 19, 'B': 17}), K4 above every copy 6 (null max 1); F11.2 poem code: 3,755,770 routes, shortest live A 22 B 24 (copies {'A': 20, 'B': 24}), K4 above every copy 2 (null max 2). Plants: F6.17 trapezoid found True; F6.18 row reshuffle found True; F11.2 poem code found True


