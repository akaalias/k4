# 0126-hand-key-schedules-listed-and-tested: Hand key schedules: the tableau rows as keys ('layer two'), a keyword stepped by skip, stutter, back-and-forth, triangle and square rules, and restarted at each carved line; each tested exactly on fixed, free and paired alphabets

**Family:** 1-keyed-periodic  
**Parent:** 0101-interrupted-key  
**Decision:** reverted  
**Run:** 2026-10-16T08:51:17+00:00, 1815.6 s, status ran  
**Time by phase:** design 0 s, implement 10 s, test 1 s, run 1816 s, record 0 s

## In plain words

Someone enciphering by hand with a key word has simple ways to use it besides repeating it: skip a letter now and then, use each letter twice, go back and forth through the word, jump ahead by growing steps, or start the word again at the start of each carved line. Or, reading 'layer two' literally, use the second row of the big table on the sculpture as the key. We list these rules, then check each against the 24 known letters, with the sculpture's table, a plain table, and tables in any order at all.

## Walkthrough, by hand

1. Take a key word of n letters, unknown, say n = 7, and a rule, say 'skip one key letter every 5 letters'.
2. Walk along K4 writing under each place the number of the key letter it uses: 0 1 2 3 4, then skip, 6 0 1 2 3, then skip, and so on, counting modulo 7.
3. Known places with the same number must have the same key value.
4. With the sculpture's table, key value = place of the carved letter minus place of the known letter in KRYPTOS order; compare.
5. With an unknown table, solve for whether any alphabet makes them agree.
6. Repeat for every rule, every n, every starting phase, and on scrambled copies of K4.

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

Inherits from 0101-interrupted-key. What changed: F1.4. The list of hand schedules is written first (C20(c)-(e) and the hand rules a person with a keyword and a pencil would use), then each is tested exactly. Covered before and not rerun: Berlin clock (0079), Carter dates (0038), progressive per repeat (0011, 0042), restart at each word (0101), autokeys (0002, 0003, 0012, 0118), the second plate and the sculpture's texts as running keys (C20(c): 0017, 0090, 0117), a shift per carved line plus a word (0088). K5 as key (C20(e)) is blocked: no text. New here: (A) C20(d) the tableau rows as fixed keys; (B) skip one keyword letter every m letters; (C) each keyword letter used r times; (D) the keyword forward then backward; (E) the keyword indexed by triangle or square numbers; (F) the keyword restarted at each carved line of the plate. B-F with an unknown keyword of length 2-31 on 8 standard/KRYPTOS tables, one free alphabet (both forms) and two free alphabets.

## Hypothesis (domain expert)

C20(c)-(e) ('layer two': the second plate, the tableau's row two, K5), C5 (simple, remembered, keyed by word/s), C3(a) (the plate as grid). Model for B-F: key value at message place i (0-based) = W[f(i) mod n] for an unknown keyword W of length n: B f = i + floor((i + phi)/m), m 2-30; C f = floor((i + phi)/r), r 2-6; D W then W reversed (period 2n or 2n-2, end letters repeated or not); E f = T(i + phi) = (i + phi)(i + phi + 1)/2 or (i + phi)^2; F f = column on the carved line minus 1 (K4 fills columns 28-31 of line 11, then lines 12-14), counted from the line start or from K4's first letter; phi over its whole range; n 2-26 (2-31 for F). Each setting partitions the 24 known places into slots; distinct partitions are tested once. Tests: (i) 8 tables (plain and cipher standard or KRYPTOS, Vigenere or Beaufort): all key values in a slot equal; (ii) one free alphabet, forms V and B, and (iii) two free alphabets, by 0119/0123's exact decider (CRT mod 13 and 2, witness re-checked). Count consistent partitions with at least one check, per schedule and test, on K4 and 10 shuffled coppers (seed 126). (A): the 26 carved tableau rows (30 letters plus the extra L) with and without the index letter, as repeating keys from every start, key letters on the standard or KRYPTOS order, 8 tables: count known letters reproduced.

## Prediction

No schedule fits on the standard or KRYPTOS tables with at least three checks, and the tableau rows reproduce at most 7 of 24 known letters, as on coppers. On free alphabets, consistent counts lie inside the coppers' range for every schedule and test, give or take one cell in the roughly 20 compared (chance). Any cell outside the range with K4 high is replicated before anything else.

## Method

1. Build each schedule's settings and the slot partition of the 24 known places it gives; keep distinct partitions.
2. For each partition and text (K4 and 10 coppers), test the 8 tables, one free alphabet (V, B) and two free alphabets exactly.
3. Count consistent partitions with at least one check.
4. Tableau rows as fixed keys: best count of known letters reproduced.
5. Compare K4 with the coppers' range.

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
 "family": "hand key schedules with an unknown keyword (skip, stutter, back and forth, triangle, square, line restart), and the tableau rows as keys",
 "partitions": {
  "B skip": {
   "distinct": 3729,
   "with_checks": 3729
  },
  "C stutter": {
   "distinct": 207,
   "with_checks": 207
  },
  "E triangle": {
   "distinct": 350,
   "with_checks": 350
  },
  "E square": {
   "distinct": 229,
   "with_checks": 229
  },
  "F line restart": {
   "distinct": 30,
   "with_checks": 30
  },
  "D back and forth": {
   "distinct": 509,
   "with_checks": 509
  }
 },
 "cells": {
  "B skip | tables": {
   "k4": 0,
   "coppers": [
    0,
    0
   ]
  },
  "B skip | free V": {
   "k4": 67,
   "coppers": [
    22,
    390
   ]
  },
  "B skip | free B": {
   "k4": 173,
   "coppers": [
    101,
    229
   ]
  },
  "B skip | two free": {
   "k4": 461,
   "coppers": [
    305,
    449
   ]
  },
  "C stutter | tables": {
   "k4": 0,
   "coppers": [
    0,
    0
   ]
  },
  "C stutter | free V": {
   "k4": 0,
   "coppers": [
    0,
    0
   ]
  },
  "C stutter | free B": {
   "k4": 0,
   "coppers": [
    0,
    0
   ]
  },
  "C stutter | two free": {
   "k4": 0,
   "coppers": [
    0,
    0
   ]
  },
  "E triangle | tables": {
   "k4": 0,
   "coppers": [
    0,
    0
   ]
  },
  "E triangle | free V": {
   "k4": 0,
   "coppers": [
    0,
    0
   ]
  },
  "E triangle | free B": {
   "k4": 0,
   "coppers": [
    0,
    0
   ]
  },
  "E triangle | two free": {
   "k4": 0,
   "coppers": [
    0,
    0
   ]
  },
  "E square | tables": {
   "k4": 0,
   "coppers": [
    0,
    0
   ]
  },
  "E square | free V": {
   "k4": 0,
   "coppers": [
    0,
    0
   ]
  },
  "E square | free B": {
   "k4": 0,
   "coppers": [
    0,
    0
   ]
  },
  "E square | two free": {
   "k4": 0,
   "coppers": [
    0,
    0
   ]
  },
  "F line restart | tables": {
   "k4": 0,
   "coppers": [
    0,
    0
   ]
  },
  "F line restart | free V": {
   "k4": 0,
   "coppers": [
    0,
    0
   ]
  },
  "F line restart | free B": {
   "k4": 0,
   "coppers": [
    0,
    0
   ]
  },
  "F line restart | two free": {
   "k4": 0,
   "coppers": [
    0,
    0
   ]
  },
  "D back and forth | tables": {
   "k4": 0,
   "coppers": [
    0,
    0
   ]
  },
  "D back and forth | free V": {
   "k4": 0,
   "coppers": [
    0,
    0
   ]
  },
  "D back and forth | free B": {
   "k4": 0,
   "coppers": [
    0,
    0
   ]
  },
  "D back and forth | two free": {
   "k4": 0,
   "coppers": [
    0,
    0
   ]
  }
 },
 "outside_copper_range": [
  "B skip | two free: K4 461 vs 305-449"
 ],
 "k4_consistent_on_standard_or_kryptos_tables": [],
 "n_k4_consistent_on_tables": 0,
 "tableau_rows_as_keys": {
  "keys": 52,
  "starts": "every",
  "tables": 16,
  "k4_best_hits": 6,
  "coppers_best_hits_first_3": [
   6,
   6,
   5
  ]
 },
 "covered_elsewhere": {
  "Berlin clock": "0079",
  "Carter dates": "0038",
  "progressive": "0011, 0042",
  "restart per word": "0101",
  "autokey": "0002, 0003, 0012, 0118",
  "C20(c) second plate / sculpture texts": "0017, 0090, 0117",
  "shift per carved line": "0088"
 },
 "blocked": {
  "C20(e) K5 as key": "no text"
 },
 "controls": "10 shuffled coppers (seed 126), identical tests"
}
```

Notes: Outside the copper range: ['B skip | two free: K4 461 vs 305-449']. K4 consistent on std/KRYPTOS tables: 0 partitions (max checks 0). Tableau rows as keys: K4 best 6/24, coppers [6, 6, 5].


