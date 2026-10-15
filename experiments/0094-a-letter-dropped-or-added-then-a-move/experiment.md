# 0094-a-letter-dropped-or-added-then-a-move: One letter dropped or added in carving, with a K3-style move and a repeating key on the true length

**Family:** 6-transposition-then-tableau  
**Parent:** 0093-one-wrong-letter-through-a-move  
**Decision:** reverted  
**Run:** 2026-10-15T19:35:50+00:00, 292.8 s, status ran  
**Time by phase:** unattributed 476 s, run 293 s, record 0 s

## In plain words

Sanborn left out one letter when carving K2. If he left one out of K4, or carved one too many, the message is really 98 or 96 letters long. That matters for grid methods: 97 letters only fill a lopsided grid, but 98 fill 7 rows of 14 and 96 fill 8 rows of 12. We try every place for the missing or extra letter, every grid move of experiments 80 to 85 on the corrected length, and a short repeating secret word, against the 24 known letters.

## Walkthrough, by hand

1. Suppose the carver added a letter at place 50. Strike it out: the text is now 96 letters and BERLINCLOCK starts at place 63.
2. Write the 96 letters into rows of 12, eight full rows, and read them out by columns.
3. Each known letter lands at a new place; with a key of length p, its key letter is that place mod p.
4. Known letters on the same key letter must agree.
5. Suppose instead a letter was left out before place 50: put back an unknown there; it fits any key, and later known letters move up one.
6. Repeat for every place, every move on 96 or 98 letters, key length 1-26 and table rule.

## Worked example (generated)

```
strike carved letter 50 (A): 96 letters in 8 rows of 12

  OBKRUOXOGHUL
  BSOLIFBBWFLR
  VQQPRNGKSSOT
  WTQSJQSSEKZZ
  WTJKLUDIAWIN
  FBNYPVTTMZFP
  KWGDKZXTJCDI
  GKUHUAUEKCAR

known letters after the strike: EASTNORTHEAST at 22-34, BERLINCLOCK at 63-73
```

## Lineage

Inherits from 0093-one-wrong-letter-through-a-move. What changed: 0093 allowed one wrong carved letter, which keeps the length at 97. A dropped or extra letter changes the length to 98 or 96, so every grid changes shape and every later letter shifts. Here the true text is the copper with one letter struck out (96) or one unknown letter put back (98) at every place outside the crib stretches, run through every single move on that length (K3's rule, one quarter turn, plain and true-keyword columnar) and a repeating key of length 1-26.

## Hypothesis (domain expert)

Type 7 of directions.md. K2 has a confirmed carving error: an S dropped from the copper and the text corrected in 2006 (01-facts.md, kryptos-group-2006-corrected-k2.txt); 0068 tested one letter missing, extra or wrong only for autokey with no move. A dropped letter matters for type 1 because 97 is prime and 96 and 98 are not: 96 = 8 x 12, 98 = 7 x 14. Variants: delete carved letter j (j outside the crib stretches, 73 places) or insert an unknown at gap j (outside the inside of either stretch, 76 gaps); crib places shift with it. Moves on the true length n: K3's rule i -> a + b i mod n with gcd(b, n) = 1, one clockwise or anticlockwise quarter turn at widths 2 to n-1, plain columnar either direction, true-keyword columnar from the puzzle's words, forward and inverse, deduplicated per n. Repeating key 1-26 after the move (slot = carved place mod p) or before it, 8 tableau classes. A crib landing on the inserted unknown imposes nothing. Ten shuffled coppers with the same variants.

## Prediction

No variant makes a repeating key of length 20 or less consistent beyond the scrambled-copper rate; the count of consistent settings at each period lies inside the ten coppers' range, give or take one period. Zero candidates.

## Method

1. For each deletion place and insertion gap, build the true ciphertext and the shifted crib places.
2. For its length, build the deduplicated single-move library.
3. For each move and class, compute the key value forced at each known letter and test periods 1-26 in both orders by slot agreement.
4. Repeat on ten shuffled coppers with the same variants.
5. List K4's settings below period 20.

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
 "family": "one carved letter dropped (insert an unknown, n = 98) or extra (strike it, n = 96), single move on n, periodic key",
 "variants": 149,
 "variants_done": 149,
 "moves_per_length": {
  "96": 3809,
  "98": 4877
 },
 "variant_move_settings": 648709,
 "periods": [
  1,
  26
 ],
 "classes": 8,
 "k4_live_by_period": {
  "A": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   1,
   2,
   334,
   4842,
   10834,
   16613,
   192389
  ],
  "B": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   1739,
   1045049
  ]
 },
 "controls_live_by_period_min": {
  "A": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   153,
   3874,
   8985,
   15618,
   189454
  ],
  "B": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   1272,
   1039833
  ]
 },
 "controls_live_by_period_max": {
  "A": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   1,
   1,
   31,
   539,
   5836,
   11525,
   16630,
   192554
  ],
  "B": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   3,
   1987,
   1047826
  ]
 },
 "periods_outside_control_range": {
  "A": [],
  "B": []
 },
 "k4_live_below_20": [],
 "n_k4_live_below_20": 0,
 "controls": "10 shuffled coppers (seed 94), same variants, identical search"
}
```

Notes: 149 variants x 3,809/4,877 moves (96/98) = 648,709 settings x 8 classes x 2 orders, periods 1-26. K4 live below period 20: 0. Outside control range: {'A': [], 'B': []}.


