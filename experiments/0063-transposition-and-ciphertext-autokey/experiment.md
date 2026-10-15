# 0063-transposition-and-ciphertext-autokey: A column shuffle combined with the scrambled text as its own key, in either order

**Family:** 6-transposition-then-tableau  
**Parent:** 0062-which-constructions-make-the-width-fingerprints  
**Decision:** reverted  
**Run:** 2026-10-15T12:30:55+00:00, 75.2 s, status ran  
**Time by phase:** design 0 s, implement 15 s, test 0 s, run 75 s, record 0 s

## In plain words

In a ciphertext autokey, each letter of the message is hidden using the hidden letter that came some fixed distance earlier, so the cipher feeds on its own output. Experiment 62 showed that this recipe, at a distance of 21, leaves the same 21-letter mark the copper has. On its own it cannot produce the copper's known letters, but a shuffle of columns before or after it would move them. Here we try every shuffle in our list, every distance and every way of using the table, and check whether the 24 known letters come out where they should.

## Walkthrough, by hand

1. Pick lag 21 and the sculpture's alphabet with Vigenere.
2. Undo the autokey on the copper: the letter at place 22 is the carved letter at 22 minus the carved letter at place 1 on the table, F minus O.
3. That gives one letter of the shuffled message.
4. If the shuffle were rows of 7 read down the columns, the known E at place 22 would have been moved to place 4, inside the first 21 letters where the autokey's starter is unknown, so it says nothing.
5. Check every other known letter at its new place past 21.
6. One mismatch kills this shuffle, lag and table.

## Worked example (generated)

```
lag 21, kry/kry/kry/vig, autokey undone on the copper (first 21 unknown):
?????????????????????ACRUZIOVSZOIXZZSIBXBWQIDTOOQSEPKEIOEDNUGVHGVMVOOUMBGKSMKEMRIWWYVEWZDLIVZWCDH
```

## Lineage

Inherits from 0062-which-constructions-make-the-width-fingerprints. What changed: Experiment 62 found that a cipher keyed by its own scrambled output, 21 letters back, is the only recipe tried that makes the width-21 repeats. On its own that cipher is ruled out by the known letters (experiment 2). Here it is combined with a column shuffle, before or after, which changes where the known letters fall, and tested exactly.

## Hypothesis (domain expert)

Ciphertext autokey (key = ciphertext letter L back, read in the key alphabet) at every lag 1-96 under the 24 conventions, composed with a transposition. Order A: transposition of the plaintext first, then autokey; the autokey decryption of K4 is then the transposed plaintext, computable without any key except the L-letter primer, so each crib must reappear at its route image (images inside the primer are free). Order B: autokey first, then transposition; undoing the route and then the autokey gives the plaintext directly, so the cribs are checked in place. Routes: 0007's set (plain columnar widths 2-96 both reading directions and both senses, keyed columnar from each vocabulary word, double plain columnar 2-50) plus keyed columnar from K1-K3 and C13/C14 words. Bounds: exact for these routes, lags and conventions; motivated by the width-21 repeats (0056, 0062).

## Prediction

No route, lag and convention reproduces all 24 cribs in either order; the best matches stay at a few cribs. Zero candidates.

## Method

1. For each lag and convention, undo the autokey on K4 (order A) and record the text.
2. For each route, check that every crib whose image lies past the primer matches.
3. For order B, undo each route on K4 first, then the autokey, and check the cribs in place.
4. Keep the best counts.
5. Decrypt and submit any full match.

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
 "family": "transposition composed with ciphertext autokey, either order",
 "routes": 3107,
 "lags": "1-95",
 "conventions": 24,
 "checked": 14167920,
 "full_matches": 0,
 "best_order_A": {
  "hits_past_primer": 8,
  "setting": [
   "A",
   "double columnar w=12 then w=49",
   16,
   "kry/kry/kry/vig"
  ]
 },
 "best_order_B": {
  "hits": 9,
  "setting": [
   "B",
   "double columnar w=34 then w=23",
   13,
   "kry/kry/kry/varbeau"
  ]
 }
}
```

Notes: 3107 routes x 95 lags x 24 conventions x 2 orders (14,167,920 checks): 0 full matches. Best order A: 8 cribs past the primer (('A', 'double columnar w=12 then w=49', 16, 'kry/kry/kry/vig')); best order B: 9/24 (('B', 'double columnar w=34 then w=23', 13, 'kry/kry/kry/varbeau')).


