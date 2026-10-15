# 0036-hill-variants-chained-and-paired: The Hill variants Bauer left open: blocks chained to their neighbours, and two matrices taking turns

**Family:** 8-hill-polygraphic  
**Parent:** 0015-hill-solved-from-crib-blocks  
**Decision:** reverted  
**Run:** 2026-10-15T08:40:45+00:00, 0.1 s, status ran  
**Time by phase:** design 0 s, implement 87 s, test 7 s, run 0 s, record 0 s

## In plain words

Experiment 15 ruled out the plain Hill cipher, where every group of letters is mixed by the same table of numbers on its own. A cryptologist who studied the sculpture listed the variants nobody had tried: mixing each group together with the group before it, or using two tables that take turns. Because the carved letters are all known, and the known message letters come in two long runs, each variant can be solved directly from the known groups rather than guessed.

## Walkthrough, by hand

1. Number the letters A=0 to Z=25, blocks of two from position 1.
2. Ciphertext feedback: the carved pair at 25-26 equals M times the message pair at 25-26 plus the carved pair at 23-24.
3. Subtract the carved 23-24 from the carved 25-26: that difference is M times TN.
4. Do the same for the next whole pairs inside EASTNORTHEAST and BERLINCLOCK: six equations in four unknowns.
5. Solve; if no M fits all of them, this setting is dead.
6. For two matrices taking turns, split the pairs into even and odd and solve each separately.

## Worked example (generated)

```
ciphertext feedback, blocks of two from position 1, A=0: the equation for the pair at 25-26

carved 25-26 VQ = [21, 16];  carved 23-24 LR = [11, 17];  difference [10, 25]
message 25-26 TN = [19, 13]
so M x (19, 13) = (10, 25) mod 26; the pairs 27-28, 29-30, 31-32 and 33-34 give four more such equations.
```

## Lineage

Inherits from 0015-hill-solved-from-crib-blocks. What changed: Four variants of the Hill cipher instead of the plain and affine forms: each block also adds the previous carved block, or the previous message block, or is mixed together with it, or alternates between two matrices. The exact solver of experiment 15 handles every one.

## Hypothesis (domain expert)

Bauer (knowledge/sources/bauer-2017-unsolved-chapter-notes.md, C21) lists chaining and paired 2x2 matrices as untested Hill variants. Chained forms: c_i = M p_i + c_(i-1) (ciphertext feedback), c_i = M p_i + p_(i-1) (plaintext feedback), c_i = M (p_i + p_(i-1)) (summed input), with the first block's predecessor taken as zeros. Paired form: M_A on even blocks, M_B on odd. Each is linear in the matrix given the known blocks, since the previous carved block is always known and the previous message block is known inside a crib run, so the whole crib blocks give rows of equations and the exact mod-13 and mod-2 solver of experiment 15 enumerates every matrix. Block sizes 2-4, four numberings, every alignment, matrix encrypting or decrypting. A matrix consistent with all its blocks decrypts the text and the partial-block cribs test it. Bounds: complete for these four variants under the stated settings.

## Prediction

No variant, size, numbering, alignment or direction gives a matrix consistent with all its whole crib blocks that also reproduces the known letters in partial blocks. Zero candidates pass.

## Method

1. For each numbering, block size, alignment and variant, list the whole crib blocks and their partners (previous carved block or previous message block).
2. Build the linear rows for the matrix, in each direction.
3. Enumerate all solutions mod 26 by elimination mod 13 and mod 2.
4. Decrypt the text with each invertible solution and count known letters right.
5. Submit any decryption with all 24.

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
 "family": "Hill variants: ciphertext feedback, plaintext feedback, summed input, paired matrices; sizes 2-4",
 "numberings": [
  "std0",
  "std1",
  "kry0",
  "kry1"
 ],
 "settings": 144,
 "settings_solved": 2,
 "solved_settings": [
  {
   "numbering": "std1",
   "n": 4,
   "offset": 0,
   "variant": "chain-c",
   "crib_blocks": 4,
   "solutions": {
    "0": 1
   },
   "best_hits": 16
  },
  {
   "numbering": "std1",
   "n": 4,
   "offset": 3,
   "variant": "chain-c",
   "crib_blocks": 4,
   "solutions": {
    "0": 1
   },
   "best_hits": 16
  }
 ],
 "best_hits_over_solved": 16
}
```

Notes: 144 settings; 2 consistent on their whole crib blocks; best known-letter count among them 16 of 24; 0 full hits.


