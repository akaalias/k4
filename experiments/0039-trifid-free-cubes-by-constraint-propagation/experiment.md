# 0039-trifid-free-cubes-by-constraint-propagation: Trifid with a free cube: the 24 known letters as equations on the cube's coordinates, solved exactly

**Family:** 4-visual-spatial  
**Parent:** 0033-trifid-keyword-cubes-and-annealing  
**Decision:** error  
**Run:** 2026-10-15T09:06:29+00:00, 0.1 s, status error  
**Time by phase:** design 0 s, implement 73 s, test 44 s, run 0 s, record 0 s

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

```

## Lineage

Inherits from 0033-trifid-keyword-cubes-and-annealing. What changed: Experiment 33 searched free cubes by trial and error and plateaued at 17 of 24. Here the cube is not searched but solved: every known letter ties three cube coordinates to three carved letters' coordinates, the ties are merged, and the remaining freedom is enumerated under the rule that all 27 symbols have different addresses.

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
(none recorded)
```


Error:
```
Traceback (most recent call last):
  File "/Users/alexisrondeau/Workshop/cryptos/_runner.py", line 34, in main
    res = attack.run(ctx) or {}
          ~~~~~~~~~~^^^^^
  File "/Users/alexisrondeau/Workshop/cryptos/attack.py", line 233, in run
    "notes": f"{len(rows)} settings; {sum(1 for r in rows if r['cubes'])} admit at least one cube; {sum(1 for r in rows if r['capped'])} hit a cap. Best English {best[0][0]:.3f} at period {best[0][1]} offset {best[0][2]}; shuffled K4 {controls}. {len(candidates)} candidates.",
                                                                                                                                                                  ~~~~^^^
IndexError: list index out of range

```

