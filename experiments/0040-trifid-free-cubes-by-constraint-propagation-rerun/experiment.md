# 0040-trifid-free-cubes-by-constraint-propagation-rerun: Trifid with a free cube: the 24 known letters as equations on the cube's coordinates, solved exactly

**Family:** 4-visual-spatial  
**Parent:** 0039-trifid-free-cubes-by-constraint-propagation  
**Decision:** reverted  
**Run:** 2026-10-15T09:07:17+00:00, 0.1 s, status ran  
**Time by phase:** design 0 s, implement 31 s, test 0 s, run 0 s, record 0 s

## In plain words

In trifid every letter has a three-digit address in a 27-seat cube, and the cipher shuffles the digits of a few letters at a time. Experiment 33 tried to find the cube by guessing and nudging, and could not. This time we do algebra instead: each known letter says 'this carved letter's first digit equals that message letter's second digit', and so on. Chaining all those equalities leaves only a little freedom, and the rule that no two letters share an address closes most of it. Every cube that survives is tried, and the one whose message reads most like English wins, if any does.

## Walkthrough, by hand

1. Period 5, blocks from position 1: the block 21-25 holds the known letters E A S T at 22-25.
2. Carved letters of that block: J Q S S E, each with a three-digit address.
3. The rule says: the first digit of J is the first digit of the block's first letter, the second digit of J is the first digit of its second letter E, the third digit of J the first digit of A, and so on round the block.
4. Write each such tie as 'this digit equals that digit'.
5. Chain the ties: if J's second digit equals E's first, and E's first equals K's third, then J's second equals K's third.
6. Give each chain a value 0, 1 or 2 so that no two letters end with the same address.
7. Decrypt and read.

## Worked example (generated)

```
period 5, blocks from position 1: the block 21-25 carries E A S T at 22-25 against the carved WFLRV

81 coordinate variables merge into 21 classes under all the ties from the 24 known letters
backtracking over the classes with the all-different rule visited 4 nodes and found 0 cube(s)
```

## Lineage

Inherits from 0039-trifid-free-cubes-by-constraint-propagation. What changed: Rerun of experiment 39, whose summary line crashed when no cube survived, so its record carries an error instead of a result; the solver and bounds are unchanged. Experiment 33 searched free cubes by trial and error and plateaued at 17 of 24. Here the cube is not searched but solved: every known letter ties three cube coordinates to three carved letters' coordinates, the ties are merged, and the remaining freedom is enumerated under the rule that all 27 symbols have different addresses.

## Hypothesis (domain expert)

Trifid over 27 symbols (A-Z and '?') with period p: the three coordinate rows of a block are concatenated and regrouped, so the k-th coordinate of ciphertext letter j equals coordinate m div p of plaintext letter m mod p, with m = 3j + k. Each known plaintext letter therefore gives three equalities between coordinate variables of symbols, 81 variables in all; a union-find merges them into classes, and the bijection, 27 distinct triples with each axis value used exactly nine times, is enforced by backtracking over class values with counting prunes. Every surviving cube decrypts the text with all 24 known letters right by construction, so the English score of the other 73 letters decides, against the same procedure on shuffled K4. Periods 2-15, every alignment. A planted trifid text must be recovered exactly. Bounds: complete for trifid with any cube at periods 2-15, within the node cap of the search.

## Prediction

At every period and alignment the equalities either contradict the bijection or leave a handful of cubes, none of whose decryptions read better than -5.5 per quadgram; shuffled K4 behaves the same. Zero candidates pass.

## Method

1. For each period and alignment, list the blocks and, for every known plaintext letter in a block, the three coordinate equalities it implies.
2. Merge equalities with union-find over the 81 coordinate variables.
3. Backtrack over the classes' values in {0,1,2}, pruning when two symbols would share an address or an axis value would exceed nine symbols.
4. Decrypt the text under each surviving cube, score the free letters as English, keep the best.
5. Repeat on two shuffles.

## Result

Candidates returned: 0. Passed all gates: 0. Best crib hits among all candidates: 0/24
(no candidates).
Best loss: None (0 is solved; 10 per missed crib letter). Best fitness: None. Champion before this run: 0034-complete-the-key-at-surviving-periods.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| - | no candidates | | | | |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "trifid, free 27-symbol cube, periods 2-15, every alignment, solved by constraint propagation and backtracking",
 "settings": 119,
 "settings_with_cubes": 0,
 "settings_capped": 0,
 "node_cap": 3000000,
 "solution_cap": 5000,
 "per_setting": [
  {
   "period": 2,
   "offset": 0,
   "classes": 20,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 2,
   "offset": 1,
   "classes": 21,
   "nodes": 4,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 3,
   "offset": 0,
   "classes": 18,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 3,
   "offset": 1,
   "classes": 21,
   "nodes": 4,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 3,
   "offset": 2,
   "classes": 21,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 4,
   "offset": 0,
   "classes": 18,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 4,
   "offset": 1,
   "classes": 22,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 4,
   "offset": 2,
   "classes": 20,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 4,
   "offset": 3,
   "classes": 20,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 5,
   "offset": 0,
   "classes": 21,
   "nodes": 4,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 5,
   "offset": 1,
   "classes": 23,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 5,
   "offset": 2,
   "classes": 19,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 5,
   "offset": 3,
   "classes": 21,
   "nodes": 4,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 5,
   "offset": 4,
   "classes": 20,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 6,
   "offset": 0,
   "classes": 22,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 6,
   "offset": 1,
   "classes": 21,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 6,
   "offset": 2,
   "classes": 20,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 6,
   "offset": 3,
   "classes": 21,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 6,
   "offset": 4,
   "classes": 20,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 6,
   "offset": 5,
   "classes": 19,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 7,
   "offset": 0,
   "classes": 20,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 7,
   "offset": 1,
   "classes": 19,
   "nodes": 4,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 7,
   "offset": 2,
   "classes": 19,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 7,
   "offset": 3,
   "classes": 20,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 7,
   "offset": 4,
   "classes": 19,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 7,
   "offset": 5,
   "classes": 19,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 7,
   "offset": 6,
   "classes": 21,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 8,
   "offset": 0,
   "classes": 20,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 8,
   "offset": 1,
   "classes": 22,
   "nodes": 4,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 8,
   "offset": 2,
   "classes": 22,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 8,
   "offset": 3,
   "classes": 21,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 8,
   "offset": 4,
   "classes": 20,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 8,
   "offset": 5,
   "classes": 22,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 8,
   "offset": 6,
   "classes": 20,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 8,
   "offset": 7,
   "classes": 19,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 9,
   "offset": 0,
   "classes": 19,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 9,
   "offset": 1,
   "classes": 18,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 9,
   "offset": 2,
   "classes": 22,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 9,
   "offset": 3,
   "classes": 21,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 9,
   "offset": 4,
   "classes": 25,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 9,
   "offset": 5,
   "classes": 23,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 9,
   "offset": 6,
   "classes": 20,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 9,
   "offset": 7,
   "classes": 19,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 9,
   "offset": 8,
   "classes": 20,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 10,
   "offset": 0,
   "classes": 18,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 10,
   "offset": 1,
   "classes": 22,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 10,
   "offset": 2,
   "classes": 20,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 10,
   "offset": 3,
   "classes": 20,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 10,
   "offset": 4,
   "classes": 18,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 10,
   "offset": 5,
   "classes": 21,
   "nodes": 4,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 10,
   "offset": 6,
   "classes": 22,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 10,
   "offset": 7,
   "classes": 23,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 10,
   "offset": 8,
   "classes": 21,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 10,
   "offset": 9,
   "classes": 16,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 11,
   "offset": 0,
   "classes": 22,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 11,
   "offset": 1,
   "classes": 22,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 11,
   "offset": 2,
   "classes": 22,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 11,
   "offset": 3,
   "classes": 19,
   "nodes": 4,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 11,
   "offset": 4,
   "classes": 19,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 11,
   "offset": 5,
   "classes": 21,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 11,
   "offset": 6,
   "classes": 20,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 11,
   "offset": 7,
   "classes": 19,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 11,
   "offset": 8,
   "classes": 20,
   "nodes": 4,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 11,
   "offset": 9,
   "classes": 18,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 11,
   "offset": 10,
   "classes": 20,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 12,
   "offset": 0,
   "classes": 22,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 12,
   "offset": 1,
   "classes": 18,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 12,
   "offset": 2,
   "classes": 19,
   "nodes": 4,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 12,
   "offset": 3,
   "classes": 23,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 12,
   "offset": 4,
   "classes": 20,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 12,
   "offset": 5,
   "classes": 18,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 12,
   "offset": 6,
   "classes": 22,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 12,
   "offset": 7,
   "classes": 22,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 12,
   "offset": 8,
   "classes": 20,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 12,
   "offset": 9,
   "classes": 21,
   "nodes": 4,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 12,
   "offset": 10,
   "classes": 17,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 12,
   "offset": 11,
   "classes": 19,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 13,
   "offset": 0,
   "classes": 19,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 13,
   "offset": 1,
   "classes": 23,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 13,
   "offset": 2,
   "classes": 27,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 13,
   "offset": 3,
   "classes": 23,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 13,
   "offset": 4,
   "classes": 21,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 13,
   "offset": 5,
   "classes": 14,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 13,
   "offset": 6,
   "classes": 15,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 13,
   "offset": 7,
   "classes": 18,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 13,
   "offset": 8,
   "classes": 22,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 13,
   "offset": 9,
   "classes": 23,
   "nodes": 4,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 13,
   "offset": 10,
   "classes": 19,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 13,
   "offset": 11,
   "classes": 21,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 13,
   "offset": 12,
   "classes": 19,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 14,
   "offset": 0,
   "classes": 20,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 14,
   "offset": 1,
   "classes": 21,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 14,
   "offset": 2,
   "classes": 20,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 14,
   "offset": 3,
   "classes": 21,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 14,
   "offset": 4,
   "classes": 21,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 14,
   "offset": 5,
   "classes": 20,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 14,
   "offset": 6,
   "classes": 19,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 14,
   "offset": 7,
   "classes": 20,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 14,
   "offset": 8,
   "classes": 17,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 14,
   "offset": 9,
   "classes": 19,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 14,
   "offset": 10,
   "classes": 22,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 14,
   "offset": 11,
   "classes": 20,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 14,
   "offset": 12,
   "classes": 24,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 14,
   "offset": 13,
   "classes": 25,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 15,
   "offset": 0,
   "classes": 22,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 15,
   "offset": 1,
   "classes": 22,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 15,
   "offset": 2,
   "classes": 21,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 15,
   "offset": 3,
   "classes": 19,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 15,
   "offset": 4,
   "classes": 16,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 15,
   "offset": 5,
   "classes": 20,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 15,
   "offset": 6,
   "classes": 27,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 15,
   "offset": 7,
   "classes": 22,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 15,
   "offset": 8,
   "classes": 22,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 15,
   "offset": 9,
   "classes": 25,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 15,
   "offset": 10,
   "classes": 20,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 15,
   "offset": 11,
   "classes": 16,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 15,
   "offset": 12,
   "classes": 22,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 15,
   "offset": 13,
   "classes": 26,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  },
  {
   "period": 15,
   "offset": 14,
   "classes": 27,
   "nodes": 1,
   "cubes": 0,
   "capped": false,
   "best_english": null,
   "best_hits": null
  }
 ],
 "best": [],
 "shuffled_control_best": [
  null,
  null
 ]
}
```

Notes: 119 settings; 0 admit at least one cube; 0 hit a cap. No cube is consistent with the known letters at any setting; shuffled K4 [None, None]. 0 candidates.


