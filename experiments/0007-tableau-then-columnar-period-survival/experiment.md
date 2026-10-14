# 0007-tableau-then-columnar-period-survival: The keyed tableau first, a matrix transposition last: the order the NSA guessed in 1992

**Family:** 6-transposition-then-tableau  
**Parent:** 0006-columnar-then-tableau-period-survival  
**Decision:** reverted  
**Run:** 2026-10-14T16:38:27+00:00, 53.7 s, status ran  
**Time by phase:** design 0 s, implement 0 s, test 1 s, run 54 s, record 0 s

## In plain words

Last time we assumed the artist scrambled the letters first and used the table second. The code-breakers at the NSA guessed the other way round: table first, scramble second. That changes which carved letter belongs to which known letter. For every grid we try, we match each of the 24 known letters with the carved letter the grid would have sent it to, and ask whether one short secret word explains all 24 pairs. Because the known letters sit in two unbroken runs, a short word has to pass a very strict test here, so a survivor would mean a lot.

## Walkthrough, by hand

1. Pick a route: write in rows of 7, read down the columns.
2. Position 22, the E of EAST, is row 4 column 1, so it is read out fourth: its enciphered letter is the carved R at position
4. 
3. Position 23, the A, is row 4 column 2; column 2 holds 14 letters after column 1's 14, so A sits at 18, the carved F.
4. Under the sculpture's alphabet and Vigenere, the key letter sending E to R is forced, and so is the one sending A to F.
5. These two key letters sit at slots 22 and 23 of the key, so any period dividing 1 would need them equal: only period 1 is at stake here.
6. Do this for all 24 letters. The E at 22 and the E at 65 differ by 43, so if their forced letters differ, period 43 and period 1 die.
7. Cross out every dead period; the smallest survivor is the shortest key this route allows.
8. Slide the puzzle's words across the survivors' pattern.

## Worked example (generated)

```
route: columnar width 7, read columns left to right, applied after the tableau; convention kry/kry/kry Vigenere

plain pos  letter  its cipher sits at  cipher letter  forced key letter  key slot at period 13
       22    E            4              R              J                  8
       23    A           18              F              O                  9
       24    S           32              K              Q                 10
       25    T           46              K              V                 11
       64    B           10              H              S                 11
       65    E           24              R              J                 12
       66    R           38              T              P                  0
       67    L           52              J              Z                  1

slots repeat at period 13: position 22 and 35 would share one, 64 and 77 another; the 24 cribs fill 13 slots with 11 collisions.
```

## Lineage

Inherits from 0006-columnar-then-tableau-period-survival. What changed: Stage order reversed. The tableau runs on the plaintext in place, then the columnar route scrambles the result. Same 2,905 routes, same 24 conventions.

## Hypothesis (domain expert)

The NSA's 1992 write-up (knowledge/sources, clue C11a) guessed substitution then transposition for K4, the opposite of Sanborn's CNN 2005 order (C1). Under K4 = T(tableau(P)) the key slot of each crib letter is its own plaintext position mod the period, and the ciphertext letter that pairs with it sits where the route T sent that position. The 24 cribs occupy 13 consecutive slots at 22-34 and 11 at 64-74, so at any period of 13 or less at least 11 forced letters must agree with an earlier one: chance survival is below one in 26 to the 11th power per route. For each route and convention we find the smallest live period by the divisor rule on plaintext positions; a survivor under 23 would be a strong signal, and the forced fragment is matched against the vocabulary and K1-K3 windows. Bounds: complete for the 0006 route set in this order.

## Prediction

No route and convention admits a period under 23. The smallest live periods cluster from the high 20s upward, with the floor set by the 13-letter run at 22-34. No forced fragment matches a vocabulary word or K1-K3 window; zero candidates pass.

## Method

1. Build the 0006 route set.
2. For each route, find where each crib position is sent.
3. For each convention, force the key letter from the crib plaintext and the ciphertext at that destination.
4. Key slots are the crib's own position mod the period: mark period p dead if it divides the distance between two crib positions with different forced letters.
5. For live periods up to 30, match the forced fragment against the vocabulary and K1-K3 windows; decrypt matches and submit.

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
 "family": "periodic tableau (separate alphabets) then columnar transposition",
 "routes": 2905,
 "route_convention_pairs_checked": 69720,
 "route_set": "plain columnar w=2..96 x {ltr, rtl} x {fwd, inv}; keyed columnar from each vocabulary word x {fwd, inv}; double plain columnar w1,w2 in 2..50",
 "conventions": 24,
 "periods": "1-97 by divisor rule on plaintext positions",
 "key_pool": "vocabulary words and K1-K3 windows of length P for live P <= 30",
 "min_live_period_histogram": {
  "26": 2810,
  "27": 66910
 },
 "fifteen_shortest": [
  {
   "min_period": 26,
   "route": "columnar w=5 fwd",
   "convention": "kry/std/std/vig"
  },
  {
   "min_period": 26,
   "route": "columnar w=5 fwd",
   "convention": "kry/std/std/varbeau"
  },
  {
   "min_period": 26,
   "route": "columnar w=5 fwd",
   "convention": "kry/std/kry/vig"
  },
  {
   "min_period": 26,
   "route": "columnar w=5 fwd",
   "convention": "kry/std/kry/varbeau"
  },
  {
   "min_period": 26,
   "route": "columnar w=5 rtl fwd",
   "convention": "std/kry/std/beau"
  },
  {
   "min_period": 26,
   "route": "columnar w=5 rtl fwd",
   "convention": "std/kry/kry/beau"
  },
  {
   "min_period": 26,
   "route": "columnar w=6 inv",
   "convention": "std/std/std/beau"
  },
  {
   "min_period": 26,
   "route": "columnar w=6 inv",
   "convention": "std/std/kry/beau"
  },
  {
   "min_period": 26,
   "route": "columnar w=6 inv",
   "convention": "std/kry/std/vig"
  },
  {
   "min_period": 26,
   "route": "columnar w=6 inv",
   "convention": "std/kry/std/varbeau"
  },
  {
   "min_period": 26,
   "route": "columnar w=6 inv",
   "convention": "std/kry/kry/vig"
  },
  {
   "min_period": 26,
   "route": "columnar w=6 inv",
   "convention": "std/kry/kry/varbeau"
  },
  {
   "min_period": 26,
   "route": "columnar w=6 rtl fwd",
   "convention": "std/kry/std/vig"
  },
  {
   "min_period": 26,
   "route": "columnar w=6 rtl fwd",
   "convention": "std/kry/std/varbeau"
  },
  {
   "min_period": 26,
   "route": "columnar w=6 rtl fwd",
   "convention": "std/kry/kry/vig"
  }
 ],
 "vocab_matches": 0
}
```

Notes: 69720 route/convention pairs; 0 forced-fragment matches submitted.


