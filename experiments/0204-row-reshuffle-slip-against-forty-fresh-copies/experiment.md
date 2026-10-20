# 0204-row-reshuffle-slip-against-forty-fresh-copies: F6.21, replication: 0203's row-reshuffle family, where K4 led every copy in 6 cells against a null of 1, rerun unchanged against 40 fresh scrambled copies, with a per-width breakdown; a deliberate slip in the keyword columnar (one column read out of its place, or two columns swapped), around every keyword columnar already tested, then or before a repeating key on the table, exact, with planted slips in the same run

**Family:** 6-transposition-then-tableau  
**Parent:** 0203-a-slip-in-the-keyword-columnar-part-2  
**Decision:** reverted  
**Run:** 2026-10-20T10:52:26+00:00, 978.5 s, status ran  
**Time by phase:** unattributed 88 s, run 978 s, record 0 s

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

Inherits from 0203-a-slip-in-the-keyword-columnar-part-2. What changed: 0203 found K4 above every one of its ten scrambled copies in 6 of 52 cells for the letters-reshuffled-inside-rows family (F6.18) with one slip (A 19, 21, 22, 23, 26; B 24), where no copy led the rest in more than one: outside the copies' range, which stops the queue until replicated (order-of-work rule 5). Here the same search, unchanged, on that family only, against 40 fresh scrambled copies (new seed), with the same fixed statistic (cells where K4 exceeds every copy, against each copy's own count against the rest), K4's rank in every cell, and the counts split by row width to show which widths carry any excess. Budget 45 minutes (41 texts plus a plant).

## Hypothesis (domain expert)

C1(a), C5, C10 ('mistakes on purpose'; misspellings as security checks in SOE practice, Marks p. 16). Source: reports/marks-between-silk-and-cyanide.md. Model: c = T(sigma'(p)) or sigma'(T(p)), sigma' a keyword columnar (or two passes) whose column reading order differs from the keyword's by one move of one column (g(g-1) orders) or one swap of two non-adjacent columns ((g-1)(g-2)/2; adjacent swaps are moves), in one pass. A skipped or doubled column alone changes the length (97 would need a message of 97 plus or minus a column, or two compensating slips): not searched. Not included: Myszkowski, AMSCO, keyed blanks, triangle and disrupted columnars (not on the item's list). Each slipped route is tested exactly as 0110 tested its routes: periods 1-26, both orders, 8 classes, by slot agreement of the 24 known letters, forward and inverse. Statistic (0134's, fixed): per base family, the shortest key length consistent on K4 against the copies, and the cells (order, length) where K4 exceeds every copy, against each copy's own count. Routes are counted per slip, not deduplicated across words (copies counted the same way).

## Prediction

The excess does not replicate: against 40 fresh copies K4 leads every copy in no more cells than a copy does (expected about 52/41, roughly 1 cell), and its rank in 0203's six cells falls inside the copies. The plant is found. Zero candidates.

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
  "F6.18 row reshuffle": 181306
 },
 "families": {
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
     9,
     304,
     2196,
     1609,
     118990,
     655260
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
     17,
     43082,
     32495487
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
     3,
     28,
     54,
     817,
     7383,
     2969,
     173492,
     5655944
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
     5,
     0,
     0,
     0,
     0,
     1,
     473,
     96489,
     41353714
    ]
   },
   "k4_shortest_live": {
    "A": 19,
    "B": 24
   },
   "coppers_shortest_live": {
    "A": 18,
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
     0,
     0,
     1,
     3,
     0,
     0,
     0,
     0,
     0,
     3,
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
     0,
     2,
     0,
     0,
     0,
     0,
     0,
     0,
     1
    ],
    "B": [
     0,
     0,
     0,
     0,
     0,
     5,
     0,
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
     21
    ]
   ],
   "null_cells_above_rest_per_copper": [
    0,
    0,
    1,
    0,
    0,
    1,
    2,
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
    1,
    2,
    0,
    1,
    0,
    1,
    0,
    1,
    0,
    0,
    0,
    0,
    0
   ],
   "stop_queue": false,
   "k4_rank_per_cell": {
    "A19": 2,
    "A20": 28,
    "A21": 0,
    "A22": 8,
    "A23": 4,
    "A24": 9,
    "A25": 27,
    "A26": 1,
    "B24": 1,
    "B25": 3,
    "B26": 6
   },
   "cells_0203": {
    "A19": {
     "k4": 3,
     "copies_at_or_above_k4": 2,
     "copies_max": 3,
     "by_width_k4_and_copies_median": {
      "11": [
       3,
       0
      ]
     }
    },
    "A21": {
     "k4": 88,
     "copies_at_or_above_k4": 0,
     "copies_max": 54,
     "by_width_k4_and_copies_median": {
      "9": [
       67,
       0
      ],
      "10": [
       2,
       0
      ],
      "12": [
       11,
       11
      ],
      "13": [
       2,
       2
      ],
      "15": [
       1,
       0
      ],
      "16": [
       1,
       2
      ],
      "18": [
       1,
       0
      ],
      "19": [
       2,
       0
      ],
      "40": [
       1,
       0
      ]
     }
    },
    "A22": {
     "k4": 701,
     "copies_at_or_above_k4": 8,
     "copies_max": 817,
     "by_width_k4_and_copies_median": {
      "10": [
       293,
       227
      ],
      "12": [
       268,
       220
      ],
      "13": [
       45,
       32
      ],
      "14": [
       17,
       7
      ],
      "17": [
       3,
       4
      ],
      "18": [
       2,
       2
      ],
      "19": [
       6,
       2
      ],
      "21": [
       2,
       0
      ],
      "25": [
       2,
       0
      ],
      "33": [
       1,
       0
      ],
      "34": [
       1,
       0
      ],
      "36": [
       1,
       0
      ],
      "38": [
       1,
       0
      ],
      "40": [
       57,
       0
      ],
      "41": [
       1,
       0
      ],
      "42": [
       1,
       0
      ]
     }
    },
    "A23": {
     "k4": 6075,
     "copies_at_or_above_k4": 4,
     "copies_max": 7383,
     "by_width_k4_and_copies_median": {
      "10": [
       58,
       17
      ],
      "12": [
       5668,
       3513
      ],
      "13": [
       121,
       76
      ],
      "14": [
       93,
       69
      ],
      "17": [
       19,
       15
      ],
      "18": [
       15,
       10
      ],
      "19": [
       11,
       13
      ],
      "20": [
       8,
       8
      ],
      "25": [
       1,
       1
      ],
      "28": [
       3,
       1
      ],
      "30": [
       1,
       0
      ],
      "31": [
       3,
       2
      ],
      "32": [
       1,
       0
      ],
      "34": [
       12,
       1
      ],
      "35": [
       1,
       0
      ],
      "38": [
       5,
       0
      ],
      "39": [
       4,
       2
      ],
      "40": [
       16,
       0
      ],
      "42": [
       9,
       3
      ],
      "44": [
       25,
       4
      ],
      "45": [
       1,
       10
      ]
     }
    },
    "A26": {
     "k4": 5363709,
     "copies_at_or_above_k4": 1,
     "copies_max": 5655944,
     "by_width_k4_and_copies_median": {
      "3": [
       14,
       14
      ],
      "4": [
       420,
       150
      ],
      "5": [
       520,
       416
      ],
      "6": [
       1360,
       1520
      ],
      "7": [
       22331,
       20722
      ],
      "8": [
       28788,
       30175
      ],
      "9": [
       72306,
       77451
      ],
      "10": [
       28259,
       26410
      ],
      "11": [
       36600,
       34194
      ],
      "12": [
       239827,
       231738
      ],
      "13": [
       4205770,
       1667130
      ],
      "14": [
       1097,
       1126
      ],
      "15": [
       445,
       551
      ],
      "16": [
       71,
       71
      ],
      "17": [
       8,
       5
      ],
      "18": [
       216,
       299
      ],
      "19": [
       1342,
       1358
      ],
      "20": [
       203,
       188
      ],
      "21": [
       1,
       9
      ],
      "22": [
       1,
       2
      ],
      "25": [
       71,
       40
      ],
      "26": [
       715379,
       382210
      ],
      "27": [
       141,
       82
      ],
      "28": [
       61,
       97
      ],
      "29": [
       25,
       37
      ],
      "30": [
       15,
       20
      ],
      "31": [
       78,
       66
      ],
      "32": [
       31,
       23
      ],
      "33": [
       28,
       32
      ],
      "34": [
       94,
       45
      ],
      "35": [
       139,
       161
      ],
      "36": [
       35,
       29
      ],
      "37": [
       191,
       295
      ],
      "38": [
       332,
       424
      ],
      "39": [
       2578,
       1548
      ],
      "40": [
       314,
       293
      ],
      "41": [
       1380,
       363
      ],
      "42": [
       940,
       311
      ],
      "43": [
       148,
       136
      ],
      "44": [
       50,
       115
      ],
      "45": [
       26,
       81
      ],
      "46": [
       1887,
       1164
      ],
      "47": [
       87,
       132
      ],
      "48": [
       100,
       91
      ]
     }
    },
    "B24": {
     "k4": 451,
     "copies_at_or_above_k4": 1,
     "copies_max": 473,
     "by_width_k4_and_copies_median": {
      "11": [
       4,
       3
      ],
      "13": [
       2,
       3
      ],
      "14": [
       8,
       3
      ],
      "18": [
       1,
       0
      ],
      "25": [
       1,
       0
      ],
      "30": [
       2,
       0
      ],
      "31": [
       2,
       0
      ],
      "33": [
       6,
       0
      ],
      "34": [
       11,
       0
      ],
      "40": [
       2,
       0
      ],
      "43": [
       9,
       0
      ],
      "46": [
       402,
       0
      ],
      "47": [
       1,
       0
      ]
     }
    }
   }
  }
 },
 "plants": [
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
  }
 ],
 "controls": "40 fresh shuffled copies (seed 1622; 0203 used seed 1621), 1 planted slipped text in the same run",
 "not_searched": "a skipped or doubled column alone (changes the length); Myszkowski, AMSCO, keyed blanks, triangle and disrupted columnars (not on the item's list)",
 "seconds": 978,
 "exhaustive": "exact per family done (see skipped)"
}
```

Notes: F6.18 row reshuffle: 121,696,528 routes, shortest live A 19 B 24 (copies {'A': 18, 'B': 17}), K4 above every copy 1 (null max 2). Plants: F6.18 row reshuffle found True


