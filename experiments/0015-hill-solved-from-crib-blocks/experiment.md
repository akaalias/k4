# 0015-hill-solved-from-crib-blocks: Hill ciphers 2x2, 3x3 and 4x4 solved straight from the crib blocks, with and without an added vector

**Family:** 8-hill-polygraphic  
**Parent:** none (root)  
**Decision:** reverted  
**Run:** 2026-10-14T17:09:05+00:00, 0.3 s, status ran  
**Time by phase:** design 40 s, implement 71 s, test 70 s, run 0 s, record 0 s

## In plain words

A Hill cipher turns letters into numbers, takes them two, three or four at a time, and mixes each group with a fixed table of numbers. The sculpture's grid has an extra L that spells HILL down one column, which some take as a hint. We know enough letters in a row that we can work the mixing table out directly, like solving simultaneous equations, instead of guessing it. If the table we work out from EASTNORTHEAST also turns the carved letters at 64 to 74 into BERLINCLOCK, it is real; if it does not, that kind of Hill cipher is out.

## Walkthrough, by hand

1. Number the letters A=0 to Z=
25. 
2. Take blocks of two starting at position 1, so 23-24 and 25-26 are whole blocks inside EASTNORTHEAST: AS and TN, which are (0,18) and (19,13).
3. The carved letters there are LR and VQ: (11,17) and (21,16).
4. We want a 2x2 table M with M times (0,18) = (11,17) and M times (19,13) = (21,16), all mod
26. 
5. Put the plaintext pairs side by side as a 2x2 matrix, invert it mod 26 if its determinant is coprime to 26, and multiply: that is M.
6. Now test M on the next block, 27-28, OR, which must come out as the carved QP.
7. If it does not, this setting is dead.
8. Repeat for every numbering, every alignment and the other direction.

## Worked example (generated)

```
2x2, standard numbering A=0, blocks from position 1, matrix encrypts: solve from blocks 23-24 and 25-26

plain blocks  AS=[0, 18]  TN=[19, 13];  cipher blocks  LR=[11, 17]  VQ=[21, 16]
plaintext matrix [[0, 19], [18, 13]] has determinant 22, not invertible mod 26: use another pair of blocks
```

## Lineage

Inherits from nothing; this is a root experiment. What changed: New root in family 8. The matrix is solved from the known blocks by linear algebra mod 26 rather than searched; every numbering, block alignment and direction is covered, and the affine form Bauer left untested.

## Hypothesis (domain expert)

The HILL column and Bauer's conjecture (knowledge/sources/bauer-2017-unsolved-chapter-notes.md, C21 reading a): K4 is a Hill cipher. Bauer and Edkins exhausted 2x2 and 3x3 under six numberings by search; 4x4, the affine form C = MP + v, and shifted numberings are open. A crib run of 13 letters contains, for block size n and alignment o, several whole blocks; with n of them whose plaintext matrix is invertible mod 26, M = C P^-1 is determined, and any further block is a check with chance 26^-n. For the affine form, block differences remove v and one more block is needed. Numberings: standard and KRYPTOS order, each 0-based and 1-based; both directions (the matrix encrypts or decrypts); alignments 0 to n-1. For every determined matrix the remaining crib blocks are checked, the text decrypted (the odd last letter left as is) and submitted if the cribs hold. 4x4 has four whole crib blocks at best, so it is determined with no check and must stand on the English of the rest; 4x4 affine needs five and is not determined here. Bounds: complete for the stated forms.

## Prediction

For 2x2 and 3x3, every numbering, alignment and direction gives a matrix from the first crib blocks that fails the remaining blocks, as Bauer found. The affine 2x2 and 3x3 forms fail the same way. For 4x4 a matrix exists for some settings with nothing left to check; its decryption of the other 73 letters is not English. Zero candidates pass.

## Method

1. For each numbering map letters to 0-
25. 
2. For each block size n, alignment o and direction, list the whole crib blocks and their ciphertext blocks.
3. Plain form: pick n blocks with an invertible plaintext matrix, solve M, check the rest. Affine form: use differences between blocks to solve M, then v from one block, check the rest.
4. Decrypt the text with the inverse map; submit if all 24 cribs hold.
5. Record, per setting, how many blocks were available and how many checks passed.

## Result

Candidates returned: 2. Passed all gates: 0. Best crib hits among all candidates: 16/24
(EAST 1/4, NORTHEAST 7/9, BERLIN 5/6, CLOCK 3/5).
Best loss: 85.1588316638355 (0 is solved; 10 per missed crib letter). Best fitness: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | cribs | 16/24 |  | `MQMHCZPDGGADDVUBAZRSIBRGTNORTHEAOPUWKBKRXSSHCYHFEOBNKMMRQUYCLTBFERLINCLOBMSPJGHQNWCECYUQHOGBUWEWR` | Hill 4x4 std1 offset 0 enc; M=[[9, 24, 18, 24], [25, 16, 25, 15], [18, 4, 19, 14], [1, 19, 18, 9]] |
| 2 | cribs | 16/24 |  | `MQMHCZPDGGADDVUBAZRSIBRGTNORTHEAOPUWKBKRXSSHCYHFEOBNKMMRQUYCLTBFERLINCLOBMSPJGHQNWCECYUQHOGBUWEWR` | Hill 4x4 std1 offset 0 dec; M=[[25, 22, 20, 10], [10, 19, 11, 17], [16, 10, 19, 18], [25, 1, 3, 8]] |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "Hill cipher, block sizes 2-4, plain and affine, solved from crib blocks",
 "numberings": [
  "std0",
  "std1",
  "kry0",
  "kry1"
 ],
 "alignments": "0..n-1",
 "directions": [
  "enc",
  "dec"
 ],
 "settings": 144,
 "settings_solved": 12,
 "settings_consistent_on_all_crib_blocks": [
  {
   "numbering": "std0",
   "n": 4,
   "offset": 0,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 16
  },
  {
   "numbering": "std0",
   "n": 4,
   "offset": 3,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1
  },
  {
   "numbering": "std1",
   "n": 4,
   "offset": 0,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1,
   "english": [
    -7.862
   ]
  },
  {
   "numbering": "std1",
   "n": 4,
   "offset": 0,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1,
   "english": [
    -7.862
   ]
  },
  {
   "numbering": "std1",
   "n": 4,
   "offset": 3,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1
  },
  {
   "numbering": "kry0",
   "n": 4,
   "offset": 0,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1
  },
  {
   "numbering": "kry0",
   "n": 4,
   "offset": 1,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  },
  {
   "numbering": "kry0",
   "n": 4,
   "offset": 2,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  },
  {
   "numbering": "kry0",
   "n": 4,
   "offset": 3,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1
  },
  {
   "numbering": "kry1",
   "n": 4,
   "offset": 0,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1
  },
  {
   "numbering": "kry1",
   "n": 4,
   "offset": 1,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  },
  {
   "numbering": "kry1",
   "n": 4,
   "offset": 2,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  }
 ],
 "settings_inconsistent": 116,
 "log": [
  {
   "numbering": "std0",
   "n": 2,
   "offset": 0,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std0",
   "n": 2,
   "offset": 0,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std0",
   "n": 2,
   "offset": 0,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std0",
   "n": 2,
   "offset": 0,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std0",
   "n": 2,
   "offset": 1,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std0",
   "n": 2,
   "offset": 1,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std0",
   "n": 2,
   "offset": 1,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std0",
   "n": 2,
   "offset": 1,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std0",
   "n": 3,
   "offset": 0,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std0",
   "n": 3,
   "offset": 0,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std0",
   "n": 3,
   "offset": 0,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std0",
   "n": 3,
   "offset": 0,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std0",
   "n": 3,
   "offset": 1,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std0",
   "n": 3,
   "offset": 1,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std0",
   "n": 3,
   "offset": 1,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std0",
   "n": 3,
   "offset": 1,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std0",
   "n": 3,
   "offset": 2,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 6,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std0",
   "n": 3,
   "offset": 2,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 6,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std0",
   "n": 3,
   "offset": 2,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 6,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std0",
   "n": 3,
   "offset": 2,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 6,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std0",
   "n": 4,
   "offset": 0,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 4,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std0",
   "n": 4,
   "offset": 0,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 4,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "too few whole crib blocks"
  },
  {
   "numbering": "std0",
   "n": 4,
   "offset": 0,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solved": true,
   "checks": 4,
   "checks_passed": 4,
   "solutions": 16
  },
  {
   "numbering": "std0",
   "n": 4,
   "offset": 0,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 4,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "too few whole crib blocks"
  },
  {
   "numbering": "std0",
   "n": 4,
   "offset": 1,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 5,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std0",
   "n": 4,
   "offset": 1,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 5,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std0",
   "n": 4,
   "offset": 1,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 5,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std0",
   "n": 4,
   "offset": 1,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std0",
   "n": 4,
   "offset": 2,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 5,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std0",
   "n": 4,
   "offset": 2,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 5,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std0",
   "n": 4,
   "offset": 2,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 5,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std0",
   "n": 4,
   "offset": 2,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std0",
   "n": 4,
   "offset": 3,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 4,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std0",
   "n": 4,
   "offset": 3,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 4,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "too few whole crib blocks"
  },
  {
   "numbering": "std0",
   "n": 4,
   "offset": 3,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solved": true,
   "checks": 4,
   "checks_passed": 4,
   "solutions": 1
  },
  {
   "numbering": "std0",
   "n": 4,
   "offset": 3,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 4,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "too few whole crib blocks"
  },
  {
   "numbering": "std1",
   "n": 2,
   "offset": 0,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std1",
   "n": 2,
   "offset": 0,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std1",
   "n": 2,
   "offset": 0,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std1",
   "n": 2,
   "offset": 0,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std1",
   "n": 2,
   "offset": 1,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std1",
   "n": 2,
   "offset": 1,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std1",
   "n": 2,
   "offset": 1,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std1",
   "n": 2,
   "offset": 1,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std1",
   "n": 3,
   "offset": 0,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std1",
   "n": 3,
   "offset": 0,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std1",
   "n": 3,
   "offset": 0,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std1",
   "n": 3,
   "offset": 0,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std1",
   "n": 3,
   "offset": 1,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std1",
   "n": 3,
   "offset": 1,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std1",
   "n": 3,
   "offset": 1,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std1",
   "n": 3,
   "offset": 1,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std1",
   "n": 3,
   "offset": 2,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 6,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std1",
   "n": 3,
   "offset": 2,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 6,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std1",
   "n": 3,
   "offset": 2,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 6,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std1",
   "n": 3,
   "offset": 2,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 6,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std1",
   "n": 4,
   "offset": 0,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 4,
   "solved": true,
   "checks": 4,
   "checks_passed": 4,
   "solutions": 1,
   "english": [
    -7.862
   ]
  },
  {
   "numbering": "std1",
   "n": 4,
   "offset": 0,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 4,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "too few whole crib blocks"
  },
  {
   "numbering": "std1",
   "n": 4,
   "offset": 0,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solved": true,
   "checks": 4,
   "checks_passed": 4,
   "solutions": 1,
   "english": [
    -7.862
   ]
  },
  {
   "numbering": "std1",
   "n": 4,
   "offset": 0,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 4,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "too few whole crib blocks"
  },
  {
   "numbering": "std1",
   "n": 4,
   "offset": 1,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 5,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std1",
   "n": 4,
   "offset": 1,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 5,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std1",
   "n": 4,
   "offset": 1,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 5,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std1",
   "n": 4,
   "offset": 1,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std1",
   "n": 4,
   "offset": 2,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 5,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std1",
   "n": 4,
   "offset": 2,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 5,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std1",
   "n": 4,
   "offset": 2,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 5,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std1",
   "n": 4,
   "offset": 2,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std1",
   "n": 4,
   "offset": 3,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 4,
   "solved": true,
   "checks": 4,
   "checks_passed": 4,
   "solutions": 1
  },
  {
   "numbering": "std1",
   "n": 4,
   "offset": 3,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 4,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "too few whole crib blocks"
  },
  {
   "numbering": "std1",
   "n": 4,
   "offset": 3,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "std1",
   "n": 4,
   "offset": 3,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 4,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "too few whole crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 2,
   "offset": 0,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 2,
   "offset": 0,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 2,
   "offset": 0,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 2,
   "offset": 0,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 2,
   "offset": 1,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 2,
   "offset": 1,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 2,
   "offset": 1,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 2,
   "offset": 1,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 3,
   "offset": 0,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 3,
   "offset": 0,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 3,
   "offset": 0,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 3,
   "offset": 0,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 3,
   "offset": 1,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 3,
   "offset": 1,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 3,
   "offset": 1,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 3,
   "offset": 1,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 3,
   "offset": 2,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 6,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 3,
   "offset": 2,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 6,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 3,
   "offset": 2,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 6,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 3,
   "offset": 2,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 6,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 4,
   "offset": 0,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 4,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 4,
   "offset": 0,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 4,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "too few whole crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 4,
   "offset": 0,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solved": true,
   "checks": 4,
   "checks_passed": 4,
   "solutions": 1
  },
  {
   "numbering": "kry0",
   "n": 4,
   "offset": 0,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 4,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "too few whole crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 4,
   "offset": 1,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 5,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 4,
   "offset": 1,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 5,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 4,
   "offset": 1,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 5,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 4,
   "offset": 1,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solved": true,
   "checks": 5,
   "checks_passed": 5,
   "solutions": 1
  },
  {
   "numbering": "kry0",
   "n": 4,
   "offset": 2,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 5,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 4,
   "offset": 2,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 5,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 4,
   "offset": 2,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 5,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 4,
   "offset": 2,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solved": true,
   "checks": 5,
   "checks_passed": 5,
   "solutions": 1
  },
  {
   "numbering": "kry0",
   "n": 4,
   "offset": 3,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 4,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 4,
   "offset": 3,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 4,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "too few whole crib blocks"
  },
  {
   "numbering": "kry0",
   "n": 4,
   "offset": 3,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solved": true,
   "checks": 4,
   "checks_passed": 4,
   "solutions": 1
  },
  {
   "numbering": "kry0",
   "n": 4,
   "offset": 3,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 4,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "too few whole crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 2,
   "offset": 0,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 2,
   "offset": 0,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 2,
   "offset": 0,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 2,
   "offset": 0,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 2,
   "offset": 1,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 2,
   "offset": 1,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 2,
   "offset": 1,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 2,
   "offset": 1,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 11,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 3,
   "offset": 0,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 3,
   "offset": 0,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 3,
   "offset": 0,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 3,
   "offset": 0,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 3,
   "offset": 1,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 3,
   "offset": 1,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 3,
   "offset": 1,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 3,
   "offset": 1,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 7,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 3,
   "offset": 2,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 6,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 3,
   "offset": 2,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 6,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 3,
   "offset": 2,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 6,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 3,
   "offset": 2,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 6,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 4,
   "offset": 0,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 4,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 4,
   "offset": 0,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 4,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "too few whole crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 4,
   "offset": 0,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solved": true,
   "checks": 4,
   "checks_passed": 4,
   "solutions": 1
  },
  {
   "numbering": "kry1",
   "n": 4,
   "offset": 0,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 4,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "too few whole crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 4,
   "offset": 1,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 5,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 4,
   "offset": 1,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 5,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 4,
   "offset": 1,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 5,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 4,
   "offset": 1,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solved": true,
   "checks": 5,
   "checks_passed": 5,
   "solutions": 1
  },
  {
   "numbering": "kry1",
   "n": 4,
   "offset": 2,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 5,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 4,
   "offset": 2,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 5,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 4,
   "offset": 2,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 5,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 4,
   "offset": 2,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solved": true,
   "checks": 5,
   "checks_passed": 5,
   "solutions": 1
  },
  {
   "numbering": "kry1",
   "n": 4,
   "offset": 3,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 4,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 4,
   "offset": 3,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 4,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "too few whole crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 4,
   "offset": 3,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "inconsistent on the crib blocks"
  },
  {
   "numbering": "kry1",
   "n": 4,
   "offset": 3,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 4,
   "solved": false,
   "checks": 0,
   "checks_passed": 0,
   "note": "too few whole crib blocks"
  }
 ]
}
```

Notes: 144 settings; 12 consistent with every whole crib block; 2 decryptions submitted.


