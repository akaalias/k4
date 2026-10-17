# 0189-m94-cylinder-any-disc-order: F11.1: the US Army's M-94 cylinder (25 published discs) in any disc order, any cipher row per group of 25, any group alignment: exact

**Family:** 11-agency-hand-systems  
**Parent:** 0119-one-free-alphabet-exact  
**Decision:** reverted  
**Run:** 2026-10-17T00:47:46+00:00, 0.2 s, status ran  
**Time by phase:** design 0 s, implement 0 s, test 0 s, run 0 s, record 0 s

## In plain words

The US Army's M-94 was a stack of 25 lettered discs on a rod: line up the message along one row, copy out any other row. The discs' alphabets are published; only their order and the row chosen were secret. Each known letter says which discs could sit at its place; if no ordering of the 25 discs fits all of them, the M-94 did not make K4.

## Walkthrough, by hand

1. Suppose the groups of 25 start at place 1: places 1-25, 26-50, 51-75, 76-97.
2. Place 22 is slot 22 of the first group; with that group's cipher row 7 places below the guide row, the disc there must carry the carved F seven places after the known E.
3. List the discs that do; do the same for every known letter.
4. Places 22 and 72 share slot 22 (different groups, different rows): one disc must satisfy both.
5. If every slot keeps a disc and the discs can all be different, that setting survives.

## Worked example (generated)

```
groups of 25 from place 1; first group's cipher row 7 below the guide row: discs that can stand at place 22 (E over carved F)

place 22: ['F5', 'O14', 'P15']
```

## Lineage

Inherits from 0119-one-free-alphabet-exact. What changed: F11.1, first family run. The community tried M-94 with hill climbs only (knowledge/05-attacks.md); no bounded result exists. The 25 disc alphabets as published (jproc.ca/crypto/m94.html, credited to George Mace; disc B1 matches the Cryptogram 1982 reprint; each alphabet checked to be a permutation starting A then its disc letter). Use (TM 32-220 par. 144): 25 discs in the day's order, 25 plaintext letters set on the guide row, any other row taken as cipher. K4 as consecutive groups of 25 from an unknown alignment (0-24), each group with its own row offset (1-25). Each known letter allows a set of discs at its slot; slots must take distinct discs (a matching). Exact over every alignment and every offset triple; K4 against 10 shuffled copies; plants.

## Hypothesis (domain expert)

A9 (methods known to the creators in 1990; the M-94 was declassified long before), C1 ('matrix codes'), F11. Model: c_i = D_{k[s]}[(pos(p_i) + g_group) mod 26], s = (i + a) mod 25, k a disc order. The 24 known letters fall in at most three groups; for fixed (a, g's), each slot's allowed discs are the intersection over its known letters; consistent iff a system of distinct discs exists. Statistic: consistent (a, g) cells, K4 against 10 copies.

## Prediction

No alignment and row choice admits a disc order on K4 or on the copies (about 24 strong checks); plants are found. Zero candidates.

## Method

1. Load the 25 published alphabets and check them.
2. For each alignment (0-24) and each row offset for every group holding known letters: allowed discs per slot.
3. Any empty slot kills the cell; otherwise look for distinct discs by bipartite matching.
4. K4 against 10 shuffled copies; two planted texts as builder checks.

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
 "family": "M-94 cylinder, 25 published discs in any order, any cipher row per group of 25, any alignment, exact (bipartite matching)",
 "discs_source": "jproc.ca/crypto/m94.html (George Mace); checked: permutations, A then the disc letter; B1 as the Cryptogram 1982 reprint",
 "consistent_cells": {
  "k4": 0,
  "copies": [
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
 "k4_cells": [],
 "plants": [
  {
   "alignment": 2,
   "cells": 4,
   "true_cell_found": true
  },
  {
   "alignment": 18,
   "cells": 58,
   "true_cell_found": true
  }
 ],
 "not_tested": "Jefferson's own wheel (alphabets not recorded), M-138-A strip sets (not published): blocked",
 "copies": "10 shuffled copies (seed 1890)",
 "seconds": 0,
 "exhaustive": true
}
```

Notes: consistent (alignment, rows) cells: K4 0 (copies 0-0); plants [{'alignment': 2, 'cells': 4, 'true_cell_found': True}, {'alignment': 18, 'cells': 58, 'true_cell_found': True}]


