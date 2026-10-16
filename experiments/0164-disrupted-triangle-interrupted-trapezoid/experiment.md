# 0164-disrupted-triangle-interrupted-trapezoid: F6.11, F6.16, F6.17: keyword-disrupted and triangle columnar, interrupted-key columnar and trapezoid transpositions, every dictionary keyword, then or before a repeating key on the table

**Family:** 6-transposition-then-tableau  
**Parent:** 0110-true-keyword-columnar-from-the-dictionary  
**Decision:** reverted  
**Run:** 2026-10-16T22:48:16+00:00, 37.8 s, status ran  
**Time by phase:** unattributed 188 s, run 38 s, record 0 s

## In plain words

Army manuals and agent ciphers describe ways of writing a message into odd-shaped grids before copying it out by keyword-ordered columns: grids with triangular holes filled last, triangles that grow two letters per row, rows cut short at lengths the keyword gives, and trapezoids. Each needs only a keyword. We build all of them for every dictionary word and test each with a repeating secret word on the sculpture's table.

## Walkthrough, by hand

1. Triangle: ten rows of 1, 3, 5, ..., 19 cells, centred; write the 97 letters row by row, three cells left empty.
2. Repeat the keyword to 19 letters, number the letters alphabetically, and copy out the columns in that order, top to bottom.
3. Disrupted: in a grid as wide as the keyword, leave a triangle empty from the column of key number 1, one column narrower each row; fill the rest, then the triangle; copy out by key order.
4. Interrupted: cut each row short at the next number of the keyword's numbering. Trapezoid: each row one cell shorter going up.
5. Then a repeating key on the table; check the known letters for every key length, and on scrambled copies.

## Worked example (generated)

```
triangle: ten rows of 1, 3, ..., 19 cells, centred; key KRYPTOS repeated to 19 letters and numbered; columns read in that order

first 20 message places read: 82 5 11 19 29 41 55 71 89 36 48 62 78 96 17 27 39 53 69 87

place  letter  lands at  carved
   22       E        35       O
   23       A        77       D
   24       S        22       F
   64       B        96       A
   65       E        42       Q
   74       K        39       Q
```

## Lineage

Inherits from 0110-true-keyword-columnar-from-the-dictionary. What changed: Three items from the field manuals, one run, a verdict each. F6.11: Rijmenants's keyword-disrupted columnar (each row filled up to a triangle that starts at the column of the next key number and moves one column right per row; triangle cells filled afterwards; columns read in key order) and TM 32-220 par. 87's triangle (rows of 1, 3, 5... cells centred under 19 columns, ten rows, three blank cells at the end or the start, the keyword repeated to 19 letters and numbered). F6.16: TM 32-220 par. 89c-e's interrupted-key columnar (rows only as long as the next number of the keyword's numbering, or, for puzzle words of nine letters or more, the next nonzero digit of 1/d for d 3-99). F6.17: par. 86's trapezoid (base = the keyword's length, rows one shorter going up on the right or on the left, the fewest blank cells at the end). Keys: every dictionary word and puzzle word of 4-24 letters, deduplicated by numbering. Then a repeating key 1-26 on the standard or KRYPTOS table after or before; compiled; ten scrambled coppers.

## Hypothesis (domain expert)

C1(a) (matrix codes), C5 (keyword-only hand systems); sources: TM 32-220 pars. 86, 87, 89 (research_notes/Scheidt patents and field ciphers/addendum_downloaded_manuals.md, figures partly garbled, rules read from the text) and Rijmenants's Hand Ciphers (foreign_agent_hand_systems.md section 5). Where the sources leave a choice open, both readings are run (triangle blanks at end or start; trapezoid shrinking on either side). Key numbering: letters ranked alphabetically, ties left to right. Periodic key: order A (after) or B (before), 8 classes (plain and cipher standard or KRYPTOS, Beaufort or not). Statistic fixed before the run (0134's), per item.

## Prediction

For each item, nothing live below key length 20 beyond the coppers' rate, and K4 above every copper in no more cells than the null's maximum. Zero candidates.

## Method

1. Keywords: dictionary and puzzle words of 4-24 letters, one per distinct numbering.
2. Per item, build the routes (where-maps) in the workers; forward and inverse.
3. Compiled periodic-key test, orders A and B, 8 classes, K4 and 10 coppers; the fixed statistic per item.

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
 "family": "keyword-shaped transpositions from TM 32-220 and Rijmenants (disrupted, triangle, interrupted, trapezoid), then or before a periodic key",
 "keywords": 163720,
 "items": {
  "F6.11 disrupted": {
   "routes": 327440,
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
     0,
     2,
     106,
     34,
     43
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
     1,
     127,
     102298
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
     0,
     1,
     100,
     29,
     32
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
     114,
     99356
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
     0,
     2,
     6,
     146,
     46,
     65
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
     159,
     103900
    ]
   },
   "k4_shortest_live": {
    "A": 23,
    "B": 24
   },
   "coppers_shortest_live": {
    "A": 22,
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
   "cells_k4_above_every_copper": [],
   "null_cells_above_rest_per_copper": [
    2,
    0,
    0,
    1,
    0,
    1,
    1,
    2,
    0,
    0
   ],
   "stop_queue": false
  },
  "F6.11 triangle": {
   "routes": 654876,
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
     0,
     1,
     0,
     7,
     5
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
     227,
     210936
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
     0,
     0,
     0,
     4,
     10
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
     206,
     178563
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
     0,
     1,
     2,
     6,
     13,
     24
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
     1,
     419,
     252794
    ]
   },
   "k4_shortest_live": {
    "A": 23,
    "B": 24
   },
   "coppers_shortest_live": {
    "A": 22,
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
     24
    ]
   ],
   "null_cells_above_rest_per_copper": [
    1,
    0,
    0,
    0,
    0,
    4,
    0,
    0,
    0,
    1
   ],
   "stop_queue": false
  },
  "F6.16 interrupted": {
   "routes": 332817,
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
     0,
     3,
     52,
     11,
     342
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
     167,
     103985
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
     0,
     0,
     50,
     13,
     337
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
     136,
     101033
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
     1,
     2,
     6,
     89,
     22,
     372
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
     1,
     174,
     103291
    ]
   },
   "k4_shortest_live": {
    "A": 23,
    "B": 25
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
     26
    ]
   ],
   "null_cells_above_rest_per_copper": [
    1,
    0,
    0,
    0,
    0,
    0,
    1,
    1,
    3,
    0
   ],
   "stop_queue": false
  },
  "F6.17 trapezoid": {
   "routes": 89708,
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
     0,
     0,
     0,
     0,
     3
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
     50,
     27646
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
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     33,
     27303
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
     0,
     0,
     1,
     3,
     1,
     9
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
     1,
     59,
     28134
    ]
   },
   "k4_shortest_live": {
    "A": 26,
    "B": 25
   },
   "coppers_shortest_live": {
    "A": 23,
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
   "cells_k4_above_every_copper": [],
   "null_cells_above_rest_per_copper": [
    0,
    0,
    1,
    1,
    0,
    0,
    2,
    1,
    1,
    0
   ],
   "stop_queue": false
  }
 },
 "seconds": 37,
 "controls": "10 shuffled coppers (seed 1610)",
 "exhaustive": "exact per item done"
}
```

Notes: F6.11 disrupted: 327,440 routes, shortest live A 23 B 24, K4 above every copper 0 (null max 2); F6.11 triangle: 654,876 routes, shortest live A 23 B 24, K4 above every copper 1 (null max 4); F6.16 interrupted: 332,817 routes, shortest live A 23 B 25, K4 above every copper 1 (null max 3); F6.17 trapezoid: 89,708 routes, shortest live A 26 B 25, K4 above every copper 0 (null max 2)


