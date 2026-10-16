# 0165-keyed-blanks-row-reshuffles-french-diagonal: F6.10, F6.18, F6.19: blank cells placed by the keyword, letters reshuffled inside rows at widths 2-48, and the French diagonal method, then or before a repeating key on the table

**Family:** 6-transposition-then-tableau  
**Parent:** 0135-hand-padding-at-every-grid-stage  
**Decision:** reverted  
**Run:** 2026-10-16T22:49:32+00:00, 48.5 s, status ran  
**Time by phase:** unattributed 38 s, run 48 s, record 0 s

## In plain words

Three more hand ways of moving letters with a keyword: leaving the grid's empty squares under particular keyword letters, shuffling the letters within each row by the keyword, and copying out a few diagonals first, then the columns. Each is followed or preceded by a repeating secret word on the sculpture's table and checked against the 24 known letters and scrambled copies.

## Walkthrough, by hand

1. Keyed blanks: rows as wide as the keyword; 13 rows of 8 hold 104 squares, 7 too many: leave empty the squares of the last row under key numbers 1-7; copy out the columns in key order.
2. Row reshuffle: write rows of the keyword's width and rewrite each row in the order of the keyword's numbering.
3. French diagonal: copy out first the diagonal starting at the top of column 1 (by key number), then column 2's diagonal, then the remaining squares by columns in key order.
4. Then a repeating key on the table; check the known letters for every key length, and on scrambled copies.

## Worked example (generated)

```
PALIMPSEST: rows of 10, 10 rows hold 100 squares; the last row's squares under key numbers 1-3 left empty; columns read in key order

place  letter  lands at  carved
   22       E         3       K
   23       A        30       N
   24       S        21       W
   64       B        25       V
   65       E        44       S
   74       K        26       Q
```

## Lineage

Inherits from 0135-hand-padding-at-every-grid-stage. What changed: Three items, one run, a verdict each. F6.10 (pivot audit D12): a grid as wide as the keyword, its blank cells (rows x width minus 97) placed under the first or the last key numbers, in the last row or the first, columns read in key order (0082 and 0135 placed blanks at fixed spots only). F6.18 (TM 32-220 pars. 89a-b, 134f): the letters inside every row of width w reshuffled by the keyword's numbering, rows kept in order (0070 did width 7 only): dictionary and puzzle words for widths 2-24, 25-48-letter windows of the K1-K3 plaintexts for widths 25-48. F6.19 (par. 88): the down-right diagonals from the tops of the columns numbered 1 to j taken first, in key order, then the remaining cells by columns in key order, j from 1 to the key length for puzzle words and 1-3 for dictionary words (the 'prearranged diagonals' taken as ones the key itself names). Then a repeating key 1-26 on the standard or KRYPTOS table after or before; compiled; ten scrambled coppers.

## Hypothesis (domain expert)

C17(b) (padding, 'whether it's 97, whether it's 100'), C1(a), C5; TM 32-220 pars. 88, 89, 134 (research_notes/Scheidt patents and field ciphers/addendum_downloaded_manuals.md); pivot audit 2026-10-16 (issue #55) D12. Key numbering: letters ranked alphabetically, ties left to right. Statistic fixed before the run (0134's), per item.

## Prediction

For each item, nothing live below key length 20 beyond the coppers' rate; K4 above every copper in no more cells than the null's maximum. Zero candidates.

## Method

1. Keywords as 0164 (dictionary and puzzle words, one per numbering), plus K1-K3 windows for widths 25-48.
2. Per item, the routes in the workers, forward and inverse.
3. Compiled periodic-key test, orders A and B, 8 classes; the fixed statistic per item.

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
 "family": "keyed blank cells, in-row reshuffles (widths 2-48), French diagonal (key-named diagonals), then or before a periodic key",
 "keywords": 181308,
 "items": {
  "F6.10 keyed blanks": {
   "routes": 1450196,
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
     8,
     36,
     386,
     2273,
     5709,
     15494
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
     595,
     432960
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
     18,
     361,
     2090,
     5524,
     14552
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
     335,
     425441
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
     9,
     102,
     485,
     2330,
     6225,
     16946
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
     1542,
     452284
    ]
   },
   "k4_shortest_live": {
    "A": 21,
    "B": 25
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
   "cells_k4_above_every_copper": [],
   "null_cells_above_rest_per_copper": [
    0,
    1,
    2,
    3,
    1,
    0,
    1,
    1,
    0,
    1
   ],
   "stop_queue": false
  },
  "F6.18 row reshuffle": {
   "routes": 361698,
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
     3,
     33,
     7,
     662,
     22942
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
     223,
     118638
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
     11,
     3,
     558,
     3728
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
     89,
     98934
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
     9,
     34,
     18,
     996,
     21735
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
     652,
     126653
    ]
   },
   "k4_shortest_live": {
    "A": 21,
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
     "A",
     21
    ],
    [
     "A",
     26
    ]
   ],
   "null_cells_above_rest_per_copper": [
    2,
    1,
    1,
    1,
    1,
    0,
    1,
    0,
    0,
    0
   ],
   "stop_queue": false
  },
  "F6.19 French diagonal": {
   "routes": 2264476,
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
     35,
     168,
     1020,
     2790,
     4905
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
     4,
     1138,
     695780
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
     111,
     893,
     2718,
     5004
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
     937,
     692054
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
     4,
     22,
     198,
     1084,
     2902,
     5494
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
     6,
     1325,
     705323
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
    ]
   ],
   "null_cells_above_rest_per_copper": [
    1,
    1,
    1,
    0,
    2,
    0,
    1,
    0,
    2,
    0
   ],
   "stop_queue": false
  }
 },
 "seconds": 47,
 "controls": "10 shuffled coppers (seed 1611)",
 "exhaustive": "exact per item done"
}
```

Notes: F6.10 keyed blanks: 1,450,196 routes, shortest live A 21 B 25, K4 above every copper 0 (null max 3); F6.18 row reshuffle: 361,698 routes, shortest live A 21 B 25, K4 above every copper 2 (null max 2); F6.19 French diagonal: 2,264,476 routes, shortest live A 22 B 24, K4 above every copper 1 (null max 2)


