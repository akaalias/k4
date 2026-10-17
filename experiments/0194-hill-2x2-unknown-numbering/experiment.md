# 0194-hill-2x2-unknown-numbering: F8.1: Hill 2x2 with an unknown one-to-one letter numbering (any of 26!), every invertible matrix, both alignments: exact; 3x3 counted and blocked

**Family:** 8-hill  
**Parent:** 0193-hill-2x2-unknown-numbering  
**Decision:** reverted  
**Run:** 2026-10-17T01:25:35+00:00, 496.3 s, status ran  
**Time by phase:** implement 0 s, test 0 s, run 496 s, record 0 s

## In plain words

The tableau's last column spells HILL, the name of a cipher that mixes letters in pairs with a little matrix of numbers. It was tried with the usual ways of numbering the letters. Here the numbering itself is a secret: any order of the alphabet. The known words still give enough pairs to decide it exactly, for every possible matrix.

## Walkthrough, by hand

1. Pair the message from place 1: places 21-22 are not both known, 23-24 (A S) are, over the carved L R.
2. With matrix (a b; c d): a*n(A) + b*n(S) = n(L) and c*n(A) + d*n(S) = n(R), where n is the secret numbering.
3. Eleven such pairs give 22 equations; choosing numbers for two or three letters forces the rest.
4. If no one-to-one numbering survives, that matrix is out.
5. All 157,248 invertible matrices, both pairings, K4 and scrambled copies.

## Worked example (generated)

```
digraphs wholly inside the known runs, pairing from place 1

AS -> LR
TN -> VQ
OR -> QP
TH -> RN
EA -> GK
ST -> SS
ER -> YP
LI -> VT
NC -> TM
LO -> ZF
CK -> PK
```

## Lineage

Inherits from 0193-hill-2x2-unknown-numbering. What changed: F8.1. Earlier Hill tests fixed the numbering (4 standard, 126 vocabulary, 200 K1-K3 words; 0015, 0044, 0055). Here the numbering is free. Counting first: at either alignment 11 digraphs of K4 lie wholly inside the known runs, 22 linear equations mod 26 (about 103 bits) in the numbers of 20-21 letters (79-81 bits) and the 4 matrix entries (17 bits): a surplus of 5-7 bits, so an exact test has power. For 3x3, 6-7 trigraphs give 18-21 equations against 76-81 + 41 bits: 21-32 bits short, no checks, blocked. For each of the 157,248 invertible 2x2 matrices and each alignment, a depth-first search with propagation looks for a one-to-one numbering satisfying all 22 equations (compiled). K4 against 5 shuffled copies (each takes minutes); plants with random numberings.

## Hypothesis (domain expert)

C21(a) (the HILL column of the tableau), F8. Model: x a one-to-one map letters -> Z26; for each aligned block, (x[c1], x[c2]) = M (x[p1], x[p2]) mod 26 with M invertible. Encryption and decryption matrices, row and column conventions are all covered by enumerating every invertible M. Statistic: matrices admitting a numbering, K4 against 5 copies; expected on a random text about 2^-5 to 2^-7 per alignment in total.

## Prediction

No matrix admits a numbering on K4 at either alignment; copies mostly none; plants found. Zero candidates.

## Method

1. For each alignment: the digraphs wholly inside the known runs (11 each).
2. For each invertible 2x2 matrix: two equations per digraph; search for a one-to-one numbering with propagation (node limit 200,000, undecided counted).
3. K4, 5 shuffled copies, 3 planted Hill texts with random numberings and matrices.

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
 "family": "Hill 2x2, any invertible matrix, any one-to-one numbering, alignments 0 and 1, exact",
 "matrices": 157248,
 "blocks_per_alignment": {
  "0": 11,
  "1": 11
 },
 "fitting_matrices": {
  "k4": 0,
  "copies": [
   0,
   0,
   0,
   0,
   0
  ]
 },
 "undecided": {
  "k4": 0,
  "copies": [
   0,
   0,
   0,
   0,
   0
  ]
 },
 "max_nodes": 40301,
 "k4_fits": [],
 "plants": [
  {
   "matrix": [
    9,
    21,
    18,
    19
   ],
   "alignment": 0,
   "true_matrix_fits": true,
   "fitting_matrices": 1
  },
  {
   "matrix": [
    5,
    20,
    3,
    15
   ],
   "alignment": 1,
   "true_matrix_fits": true,
   "fitting_matrices": 1
  },
  {
   "matrix": [
    17,
    13,
    5,
    16
   ],
   "alignment": 0,
   "true_matrix_fits": true,
   "fitting_matrices": 1
  }
 ],
 "count_3x3": "6-7 trigraphs, 18-21 equations (85-99 bits) against 76-81 bits of numbering and 41 of matrix: 21-32 bits short; blocked",
 "copies": "5 shuffled copies (seed 1930)",
 "seconds": 496,
 "exhaustive": true
}
```

Notes: matrices admitting a numbering: K4 0 (copies 0-0); undecided K4 0; plants: [(True, 1), (True, 1), (True, 1)]


