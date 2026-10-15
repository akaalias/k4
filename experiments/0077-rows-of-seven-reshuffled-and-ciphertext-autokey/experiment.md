# 0077-rows-of-seven-reshuffled-and-ciphertext-autokey: Both fingerprints at once: every row of seven reshuffled, and the self-feeding autokey at every distance

**Family:** 1-keyed-periodic  
**Parent:** 0070-reshuffle-every-block-of-seven-and-the-table  
**Decision:** reverted  
**Run:** 2026-10-15T13:34:55+00:00, 241.4 s, status ran  
**Time by phase:** design 32 s, implement 0 s, test 18 s, run 241 s, record 0 s

## In plain words

The copper carries a mark tied to seven and a mark tied to twenty-one. A seven-letter reshuffle of every row could leave the first, and the autokey that feeds on carved letters 21 places back could leave the second. Here the two are joined, in either order, for every one of the 5,040 ways of reshuffling seven letters and every feeding distance, and the 24 known letters give an exact yes or no each time. Scrambled coppers through the same test show how many yeses luck gives.

## Walkthrough, by hand

1. Take the order that reverses every row of seven, and order A: autokey first, then reverse each row.
2. Undo it: reverse each row of seven of the copper, giving XOURKBO SBLUHGO WBBFILO PQQVRLF ...
3. Lag 21, sculpture's alphabet from K = 0, Vigenere. Place 22: the unreversed letter P (3) minus known E (11) is 18; the letter 21 back is X (24); residual 18 - 24 = 20.
4. Place 23: Q (20) minus A (7) is 13; 21 back O (5); residual 8.
5. 20 and 8 disagree: dead.
6. Repeat for every order, lag, class and both ways round.

## Worked example (generated)

```
every row of seven reversed after the autokey; undone: XOURKBOSBLUHGOWBBFILOPQQVRLFOSSKGNR...
lag 21, sculpture's alphabet, Vigenere

place  known  letter  21 back  residual
   22      E       P        X        20
   23      A       Q        O         8
   24      S       Q        U        19
   25      T       V        R        17
```

## Lineage

Inherits from 0070-reshuffle-every-block-of-seven-and-the-table. What changed: Experiment 70 joined the block-of-seven reshuffle to a repeating key, and experiment 63 joined column routes to the self-feeding autokey. The two fingerprints suggest a seven-wide stage and a feedback stage at distance 21, so this joins the block-of-seven reshuffle, all 5,040 orders, to the self-feeding autokey at every distance, in both orders.

## Hypothesis (domain expert)

Family 1 (ciphertext feedback) with a block transposition, chosen to explain both fingerprints in one construction: the block-of-7 permutation leaves a period-7 positional trace (the doublet column, 0056), and ciphertext autokey at lag 21 is the only generator that made the width-21 repeats (0062). Orders: (A) ciphertext autokey, then every block of 7 permuted by one fixed order; (B) the plaintext's blocks permuted, then ciphertext autokey. Autokey with a constant shift, T[j] = s*A(c[j-L]) + k0, L = 1-96; 5,040 orders (the last block of 6 keeps the order restricted to its offsets); plain, cipher and key alphabets standard or KRYPTOS, Vigenere or Beaufort, sign +1 or -1 (32 classes): 31 million cases, each an exact check of the residuals at the known places past the lag. Ten shuffled coppers through the same sweep. Clue entries: C1(a), C11a, C27(a).

## Prediction

No (order, distance, class) case survives with three or more redundant checks beyond the shuffled-copper range, in either order; lag 21 has no case with more than two checks. Zero candidates pass.

## Method

1. For each order of seven, compute where each known place lands.
2. Order A: undo the reshuffle on the copper and run the autokey test on the result. Order B: run the autokey test on the copper with the known letters at their landing places.
3. For each lag and class, check the residuals agree; tally survivors by redundant checks.
4. Repeat on ten shuffled coppers.

## Result

Candidates returned: 0. Passed all gates: 0. Best crib hits among all candidates: 0/24
(no candidates).
Best loss: None (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: 0034-complete-the-key-at-surviving-periods.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| - | no candidates | | | | |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "block-of-7 permutation with ciphertext autokey (constant shift), both orders",
 "permutations": 5040,
 "lags": "1-96",
 "classes": 32,
 "cases": 30965760,
 "complete": true,
 "controls_complete": [
  true,
  true,
  true,
  true,
  true,
  true,
  true,
  true,
  true,
  true
 ],
 "survivors_by_checks": {
  "A": {
   "1": {
    "k4": 5760,
    "controls": [
     6744,
     5856,
     5832,
     6528,
     6792,
     6432,
     6240,
     5976,
     5640,
     5952
    ]
   },
   "2": {
    "k4": 168,
    "controls": [
     240,
     264,
     168,
     180,
     210,
     222,
     258,
     282,
     240,
     204
    ]
   },
   "3": {
    "k4": 6,
    "controls": [
     6,
     18,
     18,
     0,
     6,
     12,
     0,
     6,
     24,
     12
    ]
   }
  },
  "B": {
   "1": {
    "k4": 8640,
    "controls": [
     9552,
     8376,
     9000,
     8376,
     9528,
     7872,
     11400,
     9408,
     9840,
     11184
    ]
   },
   "2": {
    "k4": 426,
    "controls": [
     204,
     198,
     228,
     300,
     276,
     288,
     438,
     384,
     312,
     432
    ]
   },
   "3": {
    "k4": 12,
    "controls": [
     6,
     18,
     24,
     0,
     6,
     12,
     0,
     6,
     36,
     18
    ]
   }
  }
 },
 "lag21_3plus": {
  "A": 0,
  "B": 0
 }
}
```

Notes: 30,965,760 cases (complete), 10 controls. Order A: 1 checks 5760 (5640-6792); 2 checks 168 (168-282); 3 checks 6 (0-24). Order B: 1 checks 8640 (7872-11400); 2 checks 426 (198-438); 3 checks 12 (0-36). Lag 21 with 3+ checks: {'A': 0, 'B': 0}.


