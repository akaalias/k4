# 0202-a-slip-in-the-keyword-columnar: F6.21: a deliberate slip in the keyword columnar (one column read out of its place, or two columns swapped), around every keyword columnar already tested, then or before a repeating key on the table, exact, with planted slips in the same run

**Family:** 6-transposition-then-tableau  
**Parent:** 0110-keyword-columnar-from-the-whole-dictionary  
**Decision:** reverted  
**Run:** 2026-10-20T10:09:01+00:00, 1851.1 s, status ran  
**Time by phase:** test 3 s, run 1851 s, record 0 s

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

Inherits from 0110-keyword-columnar-from-the-whole-dictionary. What changed: F6.21 (issue #78). SOE's 'indecipherables' came from a misnumbered transposition key or a column skipped or doubled (Marks, Between Silk and Cyanide, pp. 11, 206, 317); Sanborn says his work is 'rife with mistakes on purpose'. Around every keyword columnar the record closed, the reading order of the columns is changed by one slip: one column read at a wrong place (what a single wrong number in the key's numbering does: with ties broken left to right, a column numbered n' instead of n is read at n's neighbour's place), or two columns swapped. Bases: 0110's single keyword columnar and 0112's double (the same word twice; the slip in either pass), 0164's interrupted-key columnar (F6.16) and trapezoid (F6.17), 0165's letters reshuffled inside each row (F6.18), 0190's poem code (F11.2; the slip in either pass). Then a repeating key 1-26 on the standard or KRYPTOS table after (A) or before (B), 8 classes, ten scrambled copies, four planted slips in the same run.

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
  "F6/1 keyword columnar": 229664,
  "F6/1 double columnar": 459328,
  "F6.16 interrupted": 166600,
  "F6.17 trapezoid": 44854,
  "F6.18 row reshuffle": 181306,
  "F11.2 poem code": 6102
 },
 "families": {
  "F6/1 keyword columnar": {
   "bases": 229664,
   "routes": 67750160,
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
     1,
     3,
     49,
     2550,
     28406,
     247094,
     412715,
     1150899
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
     13,
     17971,
     20364114
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
     15,
     916,
     22487,
     222201,
     415857,
     1142984
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
     7,
     16910,
     20270464
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
     20,
     922,
     4547,
     39868,
     252188,
     440216,
     1190012
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
     1,
     0,
     0,
     0,
     0,
     0,
     59,
     53916,
     21811480
    ]
   },
   "k4_shortest_live": {
    "A": 19,
    "B": 24
   },
   "coppers_shortest_live": {
    "A": 20,
    "B": 18
   },
   "k4_settings_live_below_20": {
    "A": 1,
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
     1,
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
   "k4_live_below_20": [
    {
     "base": 197140,
     "slip": [
      0,
      1,
      0,
      9
     ],
     "order": "A",
     "class": "std/std/beau",
     "period": 19
    }
   ],
   "cells_k4_above_every_copper": [
    [
     "A",
     19
    ]
   ],
   "null_cells_above_rest_per_copper": [
    2,
    0,
    2,
    0,
    1,
    0,
    1,
    1,
    1,
    3
   ],
   "stop_queue": false
  },
  "F6/1 double columnar": {
   "bases": 459328,
   "routes": 135500320,
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
     74,
     16,
     433,
     868,
     58676,
     48563,
     154113
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
     1,
     0,
     0,
     0,
     0,
     0,
     91,
     62044,
     41759685
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
     4,
     8,
     242,
     711,
     42973,
     46854,
     150856
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
     61,
     57085,
     41272617
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
     1,
     0,
     134,
     35,
     759,
     1158,
     63939,
     50197,
     156306
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
     1,
     1,
     0,
     0,
     0,
     0,
     1,
     100,
     63350,
     42269451
    ]
   },
   "k4_shortest_live": {
    "A": 20,
    "B": 18
   },
   "coppers_shortest_live": {
    "A": 18,
    "B": 17
   },
   "k4_settings_live_below_20": {
    "A": 0,
    "B": 1
   },
   "controls_settings_live_below_20": {
    "A": [
     0,
     0,
     1,
     0,
     0,
     0,
     1,
     0,
     0,
     0
    ],
    "B": [
     0,
     1,
     0,
     1,
     0,
     0,
     0,
     0,
     0,
     0
    ]
   },
   "k4_live_below_20": [
    {
     "base": 241670,
     "slip": [
      0,
      0,
      0,
      9
     ],
     "order": "B",
     "class": "std/std/vig-var",
     "period": 18
    }
   ],
   "cells_k4_above_every_copper": [],
   "null_cells_above_rest_per_copper": [
    0,
    3,
    1,
    0,
    0,
    0,
    3,
    3,
    0,
    1
   ],
   "stop_queue": false
  },
  "F6.16 interrupted": {
   "bases": 166600,
   "routes": 51899058,
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
     3,
     12,
     333,
     2700,
     1672,
     7709
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
     24290,
     16071206
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
     9,
     114,
     2613,
     1483,
     7589
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
     13,
     22694,
     15838447
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
     2,
     5,
     54,
     414,
     2788,
     1807,
     7931
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
     74,
     23784,
     16158948
    ]
   },
   "k4_shortest_live": {
    "A": 21,
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
     "B",
     25
    ]
   ],
   "null_cells_above_rest_per_copper": [
    1,
    2,
    1,
    1,
    0,
    1,
    0,
    1,
    0,
    1
   ],
   "stop_queue": false
  },
  "F6.17 trapezoid": {
   "skipped": "time"
  },
  "F6.18 row reshuffle": {
   "skipped": "time"
  },
  "F11.2 poem code": {
   "skipped": "time"
  }
 },
 "plants": [
  {
   "family": "F6/1 keyword columnar",
   "base": "SUBJECTIVE",
   "slip": [
    0,
    5,
    2
   ],
   "order": "A",
   "class": "std/kry/beau",
   "length": 7,
   "found": true,
   "shortest_live_at_own_setting": 7,
   "other_live_settings_below_20": 3
  },
  {
   "family": "F6.16 interrupted",
   "base": "UNAFFECTED",
   "slip": [
    1,
    0,
    9
   ],
   "order": "B",
   "class": "kry/std/beau",
   "length": 8,
   "found": true,
   "shortest_live_at_own_setting": 8,
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
   "found": false,
   "shortest_live_at_own_setting": null,
   "other_live_settings_below_20": 0
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
   "found": false,
   "shortest_live_at_own_setting": null,
   "other_live_settings_below_20": 0
  }
 ],
 "controls": "10 shuffled copies (seed 1621), 4 planted slipped texts in the same run",
 "not_searched": "a skipped or doubled column alone (changes the length); Myszkowski, AMSCO, keyed blanks, triangle and disrupted columnars (not on the item's list)",
 "seconds": 1851,
 "exhaustive": "exact per family done (see skipped)"
}
```

Notes: F6/1 keyword columnar: 67,750,160 routes, shortest live A 19 B 24 (copies {'A': 20, 'B': 18}), K4 above every copy 1 (null max 3); F6/1 double columnar: 135,500,320 routes, shortest live A 20 B 18 (copies {'A': 18, 'B': 17}), K4 above every copy 0 (null max 3); F6.16 interrupted: 51,899,058 routes, shortest live A 21 B 24 (copies {'A': 20, 'B': 24}), K4 above every copy 1 (null max 2); F6.17 trapezoid: 0 routes, shortest live A None B None (copies None), K4 above every copy 0 (null max 0); F6.18 row reshuffle: 0 routes, shortest live A None B None (copies None), K4 above every copy 0 (null max 0); F11.2 poem code: 0 routes, shortest live A None B None (copies None), K4 above every copy 0 (null max 0). Plants: F6/1 keyword columnar found True; F6.16 interrupted found True; F6.18 row reshuffle found False; F11.2 poem code found False


