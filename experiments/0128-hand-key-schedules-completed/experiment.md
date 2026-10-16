# 0128-hand-key-schedules-completed: The hand schedules 0126 never reached: stutter, back and forth, triangle and square steps, restart at each carved line, and the tableau rows as keys, tested exactly against 30 coppers

**Family:** 1-keyed-periodic  
**Parent:** 0127-skip-schedule-two-alphabets-replication  
**Decision:** reverted  
**Run:** 2026-10-16T09:32:37+00:00, 153.5 s, status ran  
**Time by phase:** design 0 s, test 1 s, run 154 s, record 0 s

## In plain words

The rest of the list of hand rules for using a key word (use each letter twice or more, go back and forth through the word, jump by growing steps, start again at each carved line), and the rows of the sculpture's big table as keys, each checked exactly against the 24 known letters and against thirty scrambled copies.

## Walkthrough, by hand

1. Take a 6-letter key word and the rule 'use each key letter twice': key letter numbers 0 0 1 1 2 2 3 3 4 4 5 5, then again.
2. Group the known places by key letter number.
3. On the sculpture's table, every group must share one key value (carved place minus known place in KRYPTOS order).
4. With unknown tables, ask whether any alphabet or pair of alphabets makes every group agree.
5. Repeat for every rule in the list and on thirty scrambled copies of K4.

## Worked example (generated)

```
skip schedule: key word of 7 letters, one key letter skipped every 5 letters; KRYPTOS on both sides, Vigenere

place  known  carved  key letter no.  key value
   22      E       F               4          1
   23      A       L               5         10
   24      S       R               6         21
   25      T       V               0         18
   26      N       Q               2          1
   27      O       Q               3         15
   28      R       P               4          2
   29      T       R               5         23
   30      H       N               6          5
   31      E       G               1          2
   32      A       K               2         19
   33      S       S               3          0
   34      T       S               4          2
   64      B       N               5         11
   65      E       Y               6         17
   66      R       P               1          2
   67      L       V               2          5
   68      I       T               3         15
   69      N       T               4         11
   70      C       M               5          9
   71      L       Z               0          8
   72      O       F               1          7
   73      C       P               2         20
   74      K       K               3          0

key letter numbers with clashing values: [0, 1, 2, 3, 4, 5, 6]: dead
```

## Lineage

Inherits from 0127-skip-schedule-two-alphabets-replication. What changed: F1.4, completion. 0126 ran out of its time budget inside the skip schedule, so schedules C (stutter), D (back and forth), E (triangle, square) and F (restart per carved line) were never tested (their zeros in 0126 mean untested), and the tableau rows as fixed keys (A) were compared with only 3 coppers. Here all 1,325 distinct partitions of C-F on K4 and 30 shuffles (seed 128), the four exact tests of 0126/0127, coverage recorded; and A against all 30.

## Hypothesis (domain expert)

C20(c)-(e), C5, C3(a). Models as written in 0126: C f = floor((i + phi)/r), r 2-6; D keyword forward then backward, ends repeated or not, n 2-26, every phase; E f = T(i + phi) or (i + phi)^2 mod n, phi 0-96; F f = column on the carved line minus 1 (K4 fills columns 28-31 of line 11, then lines 12-14), from the line start or from K4's first letter, n 2-31. Key value at place i = W[f(i) mod n], W unknown. Exact tests per distinct partition of the 24 known places: 8 standard/KRYPTOS tables; one free alphabet V and B; two free alphabets (CRT decider, node limit 100,000, undecided counted). A: 26 carved tableau rows with and without the index letter as repeating keys from every start, 16 table settings, known letters reproduced.

## Prediction

No partition of C-F is consistent on the standard or KRYPTOS tables with K4; on free alphabets K4's counts lie inside the 30 coppers' range in all 16 cells, give or take one; the tableau rows reproduce at most 7 of 24, as on the coppers. A cell with K4 above every copper is replicated first.

## Method

1. Distinct partitions of schedules C-F.
2. For K4 and 30 shuffles, the four exact tests on each.
3. Counts per schedule and test, K4's rank.
4. Tableau rows as keys, best known letters reproduced, K4 and every copper.

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
 "family": "hand key schedules C-F (stutter, back and forth, triangle, square, restart per carved line), unknown keyword, 4 exact tests; tableau rows as fixed keys",
 "coverage": {
  "C stutter": {
   "partitions": 207,
   "k4_done": 207,
   "coppers_min_done": 207
  },
  "E triangle": {
   "partitions": 350,
   "k4_done": 350,
   "coppers_min_done": 350
  },
  "E square": {
   "partitions": 229,
   "k4_done": 229,
   "coppers_min_done": 229
  },
  "F line restart": {
   "partitions": 30,
   "k4_done": 30,
   "coppers_min_done": 30
  },
  "D back and forth": {
   "partitions": 509,
   "k4_done": 509,
   "coppers_min_done": 509
  }
 },
 "undecided": {
  "C stutter": {
   "k4": 0,
   "coppers_total": 0
  },
  "E triangle": {
   "k4": 0,
   "coppers_total": 8
  },
  "E square": {
   "k4": 1,
   "coppers_total": 2
  },
  "F line restart": {
   "k4": 0,
   "coppers_total": 0
  },
  "D back and forth": {
   "k4": 1,
   "coppers_total": 16
  }
 },
 "summary": {
  "C stutter | tables": {
   "k4": 0,
   "coppers_min": 0,
   "coppers_max": 0,
   "k4_rank": 1
  },
  "C stutter | free V": {
   "k4": 0,
   "coppers_min": 0,
   "coppers_max": 12,
   "k4_rank": 14
  },
  "C stutter | free B": {
   "k4": 0,
   "coppers_min": 0,
   "coppers_max": 6,
   "k4_rank": 12
  },
  "C stutter | two free": {
   "k4": 0,
   "coppers_min": 0,
   "coppers_max": 40,
   "k4_rank": 28
  },
  "E triangle | tables": {
   "k4": 0,
   "coppers_min": 0,
   "coppers_max": 0,
   "k4_rank": 1
  },
  "E triangle | free V": {
   "k4": 0,
   "coppers_min": 0,
   "coppers_max": 48,
   "k4_rank": 27
  },
  "E triangle | free B": {
   "k4": 7,
   "coppers_min": 1,
   "coppers_max": 18,
   "k4_rank": 10
  },
  "E triangle | two free": {
   "k4": 42,
   "coppers_min": 15,
   "coppers_max": 61,
   "k4_rank": 13
  },
  "E square | tables": {
   "k4": 0,
   "coppers_min": 0,
   "coppers_max": 0,
   "k4_rank": 1
  },
  "E square | free V": {
   "k4": 0,
   "coppers_min": 0,
   "coppers_max": 25,
   "k4_rank": 23
  },
  "E square | free B": {
   "k4": 6,
   "coppers_min": 0,
   "coppers_max": 15,
   "k4_rank": 6
  },
  "E square | two free": {
   "k4": 22,
   "coppers_min": 9,
   "coppers_max": 46,
   "k4_rank": 18
  },
  "F line restart | tables": {
   "k4": 0,
   "coppers_min": 0,
   "coppers_max": 1,
   "k4_rank": 2
  },
  "F line restart | free V": {
   "k4": 0,
   "coppers_min": 0,
   "coppers_max": 17,
   "k4_rank": 23
  },
  "F line restart | free B": {
   "k4": 7,
   "coppers_min": 0,
   "coppers_max": 11,
   "k4_rank": 10
  },
  "F line restart | two free": {
   "k4": 17,
   "coppers_min": 0,
   "coppers_max": 18,
   "k4_rank": 4
  },
  "D back and forth | tables": {
   "k4": 0,
   "coppers_min": 0,
   "coppers_max": 1,
   "k4_rank": 11
  },
  "D back and forth | free V": {
   "k4": 1,
   "coppers_min": 2,
   "coppers_max": 161,
   "k4_rank": 31
  },
  "D back and forth | free B": {
   "k4": 41,
   "coppers_min": 13,
   "coppers_max": 94,
   "k4_rank": 24
  },
  "D back and forth | two free": {
   "k4": 130,
   "coppers_min": 91,
   "coppers_max": 213,
   "k4_rank": 23
  }
 },
 "outside_copper_range": [
  "D back and forth | free V"
 ],
 "tableau_rows_as_keys": {
  "keys": 52,
  "k4_best_hits": 6,
  "coppers_best_hits": [
   5,
   5,
   5,
   6,
   6,
   6,
   6,
   6,
   6,
   6,
   6,
   6,
   6,
   6,
   6,
   6,
   6,
   6,
   6,
   6,
   6,
   6,
   6,
   7,
   7,
   7,
   7,
   7,
   7,
   8
  ]
 },
 "controls": "30 shuffled coppers (seed 128), identical tests"
}
```

Notes: Outside the copper range: ['D back and forth | free V']. Tables consistent on K4: {'C stutter | tables': 0, 'E triangle | tables': 0, 'E square | tables': 0, 'F line restart | tables': 0, 'D back and forth | tables': 0}. Tableau rows: K4 6/24, coppers 5-8.


