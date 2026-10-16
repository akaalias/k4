# 0127-skip-schedule-two-alphabets-replication: Replication: the skip schedule on two unknown alphabets, where K4 had more consistent settings than ten coppers (0126), against 30 fresh coppers with every setting covered

**Family:** 1-keyed-periodic  
**Parent:** 0126-hand-key-schedules-listed-and-tested  
**Decision:** reverted  
**Run:** 2026-10-16T09:23:02+00:00, 536.6 s, status ran  
**Time by phase:** design 0 s, test 1 s, run 537 s, record 0 s

## In plain words

In the last run, one hand rule (skip a key letter every so often) fitted K4 with two unknown alphabets in more ways than it fitted ten scrambled copies. That run was cut short, so here the rule is tested completely, against thirty new scrambled copies, to see whether K4 really stands out.

## Walkthrough, by hand

1. Take a key word of 7 letters and the rule 'skip one key letter every 5 letters'.
2. Number the key letter each place uses: 0 1 2 3 4, skip 5, 6 0 1 2 3, skip, and so on, modulo 7.
3. Group the known places by that number.
4. Ask whether two unknown alphabets and the word can make every group agree.
5. Do it for every skip interval, phase and word length, on K4 and on thirty scrambled copies, and compare the counts.

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

Inherits from 0126-hand-key-schedules-listed-and-tested. What changed: F1.4, replication (order-of-work rule 5). 0126 ran out of time: the skip schedule (B) was tested on part of its 3,729 distinct partitions and schedules C-F not at all (their zeros mean untested). In what was done, B with two free alphabets gave K4 461 consistent partitions against 305-449 on ten coppers. Here all 3,729 B partitions are tested on K4 and 30 fresh shuffles (seed 127), all four tests, with the search's node limit lowered to 100,000 so no case can stall, undecided cases counted, coverage recorded, texts run in parallel.

## Hypothesis (domain expert)

Follow-up of 0126 (C20, C5). Same model and exact tests: key value at place i = W[f(i) mod n], f(i) = i + floor((i + phi)/m), m 2-30, phi 0..m-1, n 2-26; distinct partitions of the 24 known places; tests: 8 standard/KRYPTOS tables, one free alphabet V and B, two free alphabets (CRT decider of 0119/0123). The partitions are heavily nested (different m, phi, n giving related slot patterns), so counts are strongly correlated and a single coincidence in the known letters can lift many at once, as R under P at 28 and 66 did in 0124 (that pair shares a slot whenever f(65) - f(27) is a multiple of n). Report K4's rank among 30 fresh coppers and, after the run, whether K4's excess partitions are those that put 28 and 66 in one slot.

## Prediction

K4's count for B with two free alphabets falls inside the range of 30 fresh coppers (rank no better than 3rd), so the 0126 excess was the small control set; the standard/KRYPTOS tables give 0 consistent partitions on K4. If K4 tops all 30, stop and report.

## Method

1. Build the 3,729 distinct partitions of the skip schedule.
2. For K4 and 30 shuffles, test each with the 8 tables, one free alphabet (V, B) and two free alphabets.
3. Count consistent partitions per test; K4's rank.
4. Among K4's two-alphabet partitions, count those with 28 and 66 in one slot, and the same on the coppers.

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
 "family": "skip schedule (one keyword letter skipped every m letters), unknown keyword, 4 exact tests; replication of 0126",
 "partitions": 3729,
 "partitions_with_28_66_together": 635,
 "coverage": {
  "k4": 3729,
  "coppers_min": 3729
 },
 "undecided": {
  "k4": 0,
  "coppers_total": 70
 },
 "summary": {
  "tables": {
   "k4": 0,
   "coppers_min": 0,
   "coppers_max": 1,
   "k4_rank": 2,
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
    0,
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
   ]
  },
  "free V": {
   "k4": 120,
   "coppers_min": 52,
   "coppers_max": 1068,
   "k4_rank": 26,
   "coppers": [
    52,
    53,
    65,
    87,
    112,
    138,
    170,
    191,
    204,
    211,
    215,
    229,
    235,
    260,
    279,
    307,
    613,
    625,
    664,
    736,
    776,
    832,
    861,
    872,
    881,
    918,
    949,
    960,
    1004,
    1068
   ]
  },
  "free B": {
   "k4": 373,
   "coppers_min": 162,
   "coppers_max": 698,
   "k4_rank": 15,
   "coppers": [
    162,
    241,
    247,
    248,
    271,
    287,
    289,
    297,
    300,
    304,
    318,
    320,
    338,
    357,
    368,
    373,
    390,
    396,
    420,
    432,
    500,
    525,
    525,
    549,
    559,
    581,
    602,
    625,
    631,
    698
   ]
  },
  "two free": {
   "k4": 1135,
   "coppers_min": 681,
   "coppers_max": 1300,
   "k4_rank": 6,
   "coppers": [
    681,
    722,
    742,
    754,
    791,
    806,
    810,
    838,
    863,
    866,
    895,
    900,
    925,
    990,
    1003,
    1005,
    1025,
    1028,
    1030,
    1031,
    1033,
    1049,
    1076,
    1114,
    1124,
    1196,
    1208,
    1227,
    1252,
    1300
   ]
  },
  "two free with 28,66 together": {
   "k4": 143,
   "coppers_min": 0,
   "coppers_max": 123,
   "k4_rank": 1,
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
    123
   ]
  }
 },
 "controls": "30 fresh shuffled coppers (seed 127), identical tests"
}
```

Notes: B skip, two free alphabets: K4 1135, coppers 681-1300, K4 rank 6 of 31. Tables: K4 0. Coverage 3729/3729; undecided K4 0.


