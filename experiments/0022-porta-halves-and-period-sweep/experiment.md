# 0022-porta-halves-and-period-sweep: Porta: the reciprocal half-alphabet tableau, which the 24 conventions never covered

**Family:** 1-keyed-periodic  
**Parent:** 0020-short-periods-mixed-alphabets-consistency  
**Decision:** reverted  
**Run:** 2026-10-15T06:37:53+00:00, 0.1 s, status ran  
**Time by phase:** design 7 s, implement 63 s, test 0 s, run 0 s, record 0 s

## In plain words

Porta is an old cipher that cuts the alphabet in two halves and always swaps a letter into the other half: a letter from the first half always lands in the second, and back. That gives a quick check: every known letter must have been swapped across the halves. With the ordinary alphabet, E and its carved partner F are both in the first half, so Porta fails at the very first known letter. But if the alphabet was first reordered by a secret word, the halves change, so we try every reordering the puzzle's words allow.

## Walkthrough, by hand

1. Write the alphabet in two rows: A to M above, N to Z below.
2. Position 22 is plaintext E and carved F; both are in the top row.
3. In Porta a top-row letter always becomes a bottom-row letter, so this cannot be Porta on the plain alphabet.
4. Now reorder the alphabet by a word, say PALIMPSEST: PALIMSETBCDFG above, HJKNOQRUVWXYZ below.
5. E and F are again both above: dead.
6. Try every reordering the puzzle's words give; a reordering that separates all 24 pairs would then get its key letters worked out one position at a time.

## Worked example (generated)

```
halves test on the standard order: A-M above, N-Z below

pos  plain  half   carved  half   swapped across?
 22    E    top      F    top      NO
 23    A    top      L    top      NO
 24    S    bottom   R    bottom   NO
 25    T    bottom   V    bottom   NO
 26    N    bottom   Q    bottom   NO
 64    B    top      N    bottom   yes
 65    E    top      Y    bottom   yes
 66    R    bottom   P    bottom   NO
```

## Lineage

Inherits from 0020-short-periods-mixed-alphabets-consistency. What changed: A different tableau. Porta splits the alphabet into two halves and always sends a letter to the other half; the key letter chooses one of 13 reciprocal alphabets. Tested with the alphabet in standard, KRYPTOS and every vocabulary-mixed order.

## Hypothesis (domain expert)

Porta (1563; in Friedman and Hitt, so in what Scheidt taught, C5) is reciprocal: with the alphabet A split into halves H1 and H2, key letter k selects j = index(k) div 2, and p in H1 at index i goes to H2[(i + j) mod 13], p in H2 at index i goes to H1[(i - j) mod 13]. Our 24 conventions are Vigenere, Beaufort and variant Beaufort over full alphabets and do not contain it. Two tests. First the halves: every crib plaintext letter must sit in the opposite half from its ciphertext letter; under the standard order E and F are both in A-M, so standard Porta dies at position 22 at once, and each of the 248 vocabulary-mixed orders passes with chance 2 to the minus 24. Second, for any order that passes, the forced j at each crib position gives a period sweep 1-52 by the divisor rule, with the forced key fragment matched against the vocabulary. Both the ACA direction and its mirror are tried. Bounds: complete for Porta over this alphabet pool.

## Prediction

No alphabet order passes the halves test for all 24 cribs; the best passes about 18 of 24. So no period sweep runs and zero candidates pass.

## Method

1. Build the alphabet pool.
2. For each order, split into halves and count crib positions whose plaintext and ciphertext letters are in the same half.
3. For any order with zero such positions, derive the forced alphabet number j at each crib and sweep periods 1-52 by the divisor rule in both directions.
4. Match forced fragments against the vocabulary; decrypt and submit matches.

## Result

Candidates returned: 0. Passed all gates: 0. Best crib hits among all candidates: 0/24
(no candidates).
Best loss: None (0 is solved; 10 per missed crib letter). Best fitness: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| - | no candidates | | | | |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "Porta over standard, KRYPTOS and vocabulary-mixed alphabet orders",
 "alphabets": 248,
 "halves_test": "crib positions whose plaintext and ciphertext share a half; zero required",
 "best_orders": [
  {
   "same_half_positions": 7,
   "alphabet": "CARTER/alt_vertical"
  },
  {
   "same_half_positions": 7,
   "alphabet": "CARTER/columnar"
  },
  {
   "same_half_positions": 7,
   "alphabet": "CLOCK/alt_vertical"
  },
  {
   "same_half_positions": 7,
   "alphabet": "HILL/alt_vertical"
  },
  {
   "same_half_positions": 8,
   "alphabet": "SECRET/keyed_columnar"
  },
  {
   "same_half_positions": 8,
   "alphabet": "WORLDCLOCK/alt_vertical"
  },
  {
   "same_half_positions": 8,
   "alphabet": "WORLDCLOCK/columnar"
  },
  {
   "same_half_positions": 8,
   "alphabet": "WORLDCLOCK/keyed_columnar"
  },
  {
   "same_half_positions": 9,
   "alphabet": "ABSCISSAE/keyed_columnar"
  },
  {
   "same_half_positions": 9,
   "alphabet": "CARNARVON/keyword"
  }
 ],
 "orders_passing_halves": [],
 "period_survivors": [],
 "n_period_survivors": 0,
 "vocab_matches": 0
}
```

Notes: 248 alphabet orders; 0 pass the halves test (best has 7 same-half positions); 0 (order, direction, period) survivors; 0 matches.


