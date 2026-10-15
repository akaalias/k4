# 0067-two-lag-ciphertext-feedback: Two earlier carved letters as the key at once, with or without a short repeating word

**Family:** 1-keyed-periodic  
**Parent:** 0066-ciphertext-autokey-plus-a-repeating-key  
**Decision:** reverted  
**Run:** 2026-10-15T13:09:36+00:00, 8.6 s, status ran  
**Time by phase:** design 36 s, implement 0 s, test 12 s, run 9 s, record 0 s

## In plain words

The copper's two oddities are tied to the distances 1 and 21. A cipher whose key is made from two earlier carved letters, one just before and one 21 back, would leave both marks. We try every pair of distances, adding or subtracting each letter, with or without a short repeating secret word on top. Because every carved letter is visible, each of the 24 known letters gives an exact yes or no. Scrambled coppers through the same test show how many yeses luck gives.

## Walkthrough, by hand

1. Count letters along KRYPTOSABCDEFGHIJLMNQUVWXZ from K = 0, and take distances 1 and 21, both added, with no extra word beyond a constant.
2. Place 22: carved F (12), known E (11), previous carved W (23), carved 21 back O (5): the constant is 12 - 11 - 23 - 5 = -27, which is 25, Z.
3. Place 23: carved L (17), known A (7), previous carved F (12), carved 21 back B (8): 17 - 7 - 12 - 8 = -10, which is 16, J.
4. Z and J disagree, so this pair of distances with a constant is dead under this way of using the table.
5. With a 2-letter repeating word instead of a constant, places 22 and 24 would have to agree, and so on.
6. Repeat for every pair, sign, word length and way of using the table.

## Worked example (generated)

```
distances 1 and 21, both added, sculpture's alphabet throughout, Vigenere

place  known  carved  1 back  21 back  constant
   22      E       F       W        O         Z
   23      A       L       F        B         J
   24      S       R       L        K         T
   25      T       V       R        R         J
```

## Lineage

Inherits from 0066-ciphertext-autokey-plus-a-repeating-key. What changed: Experiment 66 used one earlier carved letter as the key. The two fingerprints point at two different distances, 1 and 21, so here the key is the sum or difference of two earlier carved letters at any pair of distances, a letter-for-letter cousin of the Gromark, optionally with a repeating word of up to 30 letters on top.

## Hypothesis (domain expert)

Family 1 (ciphertext feedback), extending 0066 to two lags: T[i] = s1*A(c[i-a]) + s2*A(c[i-b]) + k[i mod P], 1 <= a < b <= 74, s1, s2 = +1 or -1, P = 1..30 (P = 1 is a constant shift, which includes no extra key), plain, cipher and key alphabets standard or KRYPTOS, Vigenere or Beaufort (16 classes; variant Beaufort is the all-minus sign). This is a lagged-Fibonacci (Gromark-like) feedback on letters rather than digits; a = 1, b = 21 would produce both the width-7 column mechanism of 0065 and the width-21 repeats of 0062 in one stage. Because the carved text is known, the feedback subtracts out and each crib with i >= b gives an exact equation on the periodic key. 2,701 lag pairs x 4 signs x 16 classes x 30 periods = 5.2 million cases. Survivors are tallied by redundant checks against ten shuffled coppers through the same sweep; forced fragments matched against words. Clue entries: C11a, C4(b) (Scheidt's 'base' remark read as a running numerical key), C22(a) (a Gromark-style generator).

## Prediction

No case with three or more redundant checks survives, including a = 1, b = 21 under every sign, class and period. With no extra key (P = 1) nothing survives at all. Survivors with one or two checks occur at the shuffled-copper rate; no fragment matches a word. Zero candidates pass.

## Method

1. For each pair of distances, signs and way of using the table, subtract the two earlier carved letters from the total key at each known place past the larger distance.
2. For each word length up to 30, check that places sharing a slot agree.
3. Tally consistent cases by redundant checks.
4. Repeat on ten shuffled coppers.
5. Match forced fragments against words.

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
 "family": "two-lag ciphertext feedback plus a periodic key",
 "lag_pairs": "1 <= a < b <= 74",
 "signs": 4,
 "periods": "1-30",
 "classes": 16,
 "cases": 1933760,
 "complete": true,
 "controls": [
  {
   "cases": 1933760,
   "complete": true
  },
  {
   "cases": 1933760,
   "complete": true
  },
  {
   "cases": 1933760,
   "complete": true
  },
  {
   "cases": 1933760,
   "complete": true
  },
  {
   "cases": 1933760,
   "complete": true
  },
  {
   "cases": 1933760,
   "complete": true
  },
  {
   "cases": 1933760,
   "complete": true
  },
  {
   "cases": 1933760,
   "complete": true
  },
  {
   "cases": 1933760,
   "complete": true
  },
  {
   "cases": 1933760,
   "complete": true
  }
 ],
 "survivors_by_checks": {
  "checks 1": {
   "k4": 8203,
   "controls": [
    8248,
    8220,
    8174,
    8344,
    8179,
    8214,
    8125,
    8206,
    8205,
    8170
   ]
  },
  "checks 2": {
   "k4": 254,
   "controls": [
    252,
    250,
    218,
    222,
    216,
    254,
    221,
    226,
    224,
    227
   ]
  },
  "checks 3": {
   "k4": 15,
   "controls": [
    10,
    5,
    8,
    5,
    11,
    11,
    4,
    3,
    8,
    12
   ]
  },
  "checks 4": {
   "k4": 1,
   "controls": [
    0,
    1,
    0,
    0,
    2,
    1,
    1,
    0,
    0,
    0
   ]
  },
  "checks 5": {
   "k4": 0,
   "controls": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    1,
    0
   ]
  }
 },
 "survivors_2plus_checks": [
  {
   "a": 2,
   "b": 36,
   "signs": [
    1,
    1
   ],
   "period": 9,
   "class": "std/std/std/vig",
   "checks": 2
  },
  {
   "a": 7,
   "b": 67,
   "signs": [
    1,
    -1
   ],
   "period": 5,
   "class": "std/std/std/vig",
   "checks": 2
  },
  {
   "a": 9,
   "b": 47,
   "signs": [
    1,
    1
   ],
   "period": 9,
   "class": "std/std/std/vig",
   "checks": 2
  },
  {
   "a": 9,
   "b": 69,
   "signs": [
    1,
    1
   ],
   "period": 3,
   "class": "std/std/std/vig",
   "checks": 2
  },
  {
   "a": 20,
   "b": 43,
   "signs": [
    1,
    -1
   ],
   "period": 9,
   "class": "std/std/std/vig",
   "checks": 2
  },
  {
   "a": 21,
   "b": 34,
   "signs": [
    -1,
    1
   ],
   "period": 8,
   "class": "std/std/std/vig",
   "checks": 3
  },
  {
   "a": 27,
   "b": 46,
   "signs": [
    -1,
    -1
   ],
   "period": 9,
   "class": "std/std/std/vig",
   "checks": 2
  },
  {
   "a": 28,
   "b": 33,
   "signs": [
    1,
    -1
   ],
   "period": 10,
   "class": "std/std/std/vig",
   "checks": 2
  },
  {
   "a": 28,
   "b": 48,
   "signs": [
    1,
    -1
   ],
   "period": 9,
   "class": "std/std/std/vig",
   "checks": 2
  },
  {
   "a": 30,
   "b": 61,
   "signs": [
    -1,
    1
   ],
   "period": 9,
   "class": "std/std/std/vig",
   "checks": 2
  },
  {
   "a": 32,
   "b": 68,
   "signs": [
    -1,
    -1
   ],
   "period": 4,
   "class": "std/std/std/vig",
   "checks": 2
  },
  {
   "a": 35,
   "b": 40,
   "signs": [
    1,
    -1
   ],
   "period": 9,
   "class": "std/std/std/vig",
   "checks": 2
  },
  {
   "a": 41,
   "b": 66,
   "signs": [
    1,
    1
   ],
   "period": 6,
   "class": "std/std/std/vig",
   "checks": 2
  },
  {
   "a": 45,
   "b": 52,
   "signs": [
    -1,
    -1
   ],
   "period": 9,
   "class": "std/std/std/vig",
   "checks": 2
  },
  {
   "a": 46,
   "b": 48,
   "signs": [
    1,
    -1
   ],
   "period": 9,
   "class": "std/std/std/vig",
   "checks": 2
  },
  {
   "a": 46,
   "b": 70,
   "signs": [
    1,
    -1
   ],
   "period": 2,
   "class": "std/std/std/vig",
   "checks": 2
  },
  {
   "a": 52,
   "b": 60,
   "signs": [
    1,
    -1
   ],
   "period": 9,
   "class": "std/std/std/vig",
   "checks": 2
  },
  {
   "a": 54,
   "b": 62,
   "signs": [
    1,
    -1
   ],
   "period": 9,
   "class": "std/std/std/vig",
   "checks": 2
  },
  {
   "a": 56,
   "b": 63,
   "signs": [
    1,
    -1
   ],
   "period": 9,
   "class": "std/std/std/vig",
   "checks": 2
  },
  {
   "a": 59,
   "b": 71,
   "signs": [
    -1,
    1
   ],
   "period": 1,
   "class": "std/std/std/vig",
   "checks": 2
  },
  {
   "a": 62,
   "b": 69,
   "signs": [
    1,
    -1
   ],
   "period": 3,
   "class": "std/std/std/vig",
   "checks": 2
  },
  {
   "a": 66,
   "b": 68,
   "signs": [
    -1,
    -1
   ],
   "period": 4,
   "class": "std/std/std/vig",
   "checks": 2
  },
  {
   "a": 1,
   "b": 61,
   "signs": [
    1,
    -1
   ],
   "period": 9,
   "class": "std/std/std/beau",
   "checks": 2
  },
  {
   "a": 6,
   "b": 67,
   "signs": [
    1,
    1
   ],
   "period": 5,
   "class": "std/std/std/beau",
   "checks": 2
  },
  {
   "a": 8,
   "b": 47,
   "signs": [
    1,
    1
   ],
   "period": 9,
   "class": "std/std/std/beau",
   "checks": 2
  },
  {
   "a": 22,
   "b": 70,
   "signs": [
    -1,
    -1
   ],
   "period": 1,
   "class": "std/std/std/beau",
   "checks": 3
  },
  {
   "a": 22,
   "b": 70,
   "signs": [
    -1,
    -1
   ],
   "period": 2,
   "class": "std/std/std/beau",
   "checks": 2
  },
  {
   "a": 24,
   "b": 41,
   "signs": [
    1,
    1
   ],
   "period": 9,
   "class": "std/std/std/beau",
   "checks": 2
  },
  {
   "a": 24,
   "b": 42,
   "signs": [
    1,
    -1
   ],
   "period": 9,
   "class": "std/std/std/beau",
   "checks": 2
  },
  {
   "a": 25,
   "b": 26,
   "signs": [
    1,
    -1
   ],
   "period": 23,
   "class": "std/std/std/beau",
   "checks": 2
  },
  {
   "a": 27,
   "b": 46,
   "signs": [
    1,
    -1
   ],
   "period": 9,
   "class": "std/std/std/beau",
   "checks": 2
  },
  {
   "a": 28,
   "b": 33,
   "signs": [
    -1,
    -1
   ],
   "period": 10,
   "class": "std/std/std/beau",
   "checks": 2
  },
  {
   "a": 30,
   "b": 69,
   "signs": [
    -1,
    1
   ],
   "period": 3,
   "class": "std/std/std/beau",
   "checks": 2
  },
  {
   "a": 51,
   "b": 53,
   "signs": [
    -1,
    1
   ],
   "period": 9,
   "class": "std/std/std/beau",
   "checks": 2
  },
  {
   "a": 1,
   "b": 28,
   "signs": [
    1,
    1
   ],
   "period": 22,
   "class": "std/std/kry/vig",
   "checks": 2
  },
  {
   "a": 3,
   "b": 58,
   "signs": [
    -1,
    1
   ],
   "period": 9,
   "class": "std/std/kry/vig",
   "checks": 2
  },
  {
   "a": 5,
   "b": 46,
   "signs": [
    -1,
    1
   ],
   "period": 9,
   "class": "std/std/kry/vig",
   "checks": 2
  },
  {
   "a": 7,
   "b": 62,
   "signs": [
    1,
    1
   ],
   "period": 9,
   "class": "std/std/kry/vig",
   "checks": 2
  },
  {
   "a": 15,
   "b": 30,
   "signs": [
    -1,
    1
   ],
   "period": 14,
   "class": "std/std/kry/vig",
   "checks": 2
  },
  {
   "a": 15,
   "b": 30,
   "signs": [
    -1,
    1
   ],
   "period": 21,
   "class": "std/std/kry/vig",
   "checks": 2
  }
 ],
 "a1_b21_survivors": [
  {
   "a": 1,
   "b": 21,
   "signs": [
    -1,
    -1
   ],
   "period": 26,
   "class": "std/std/std/beau",
   "checks": 1
  },
  {
   "a": 1,
   "b": 21,
   "signs": [
    -1,
    -1
   ],
   "period": 26,
   "class": "std/std/kry/vig",
   "checks": 1
  },
  {
   "a": 1,
   "b": 21,
   "signs": [
    1,
    -1
   ],
   "period": 26,
   "class": "std/std/kry/beau",
   "checks": 1
  },
  {
   "a": 1,
   "b": 21,
   "signs": [
    -1,
    1
   ],
   "period": 26,
   "class": "kry/kry/std/beau",
   "checks": 1
  },
  {
   "a": 1,
   "b": 21,
   "signs": [
    -1,
    -1
   ],
   "period": 26,
   "class": "kry/kry/kry/vig",
   "checks": 1
  }
 ]
}
```

Notes: 1933760 cases (complete). Survivors by checks, K4 (controls min-max): checks 1: 8203 (8125-8344); checks 2: 254 (216-254); checks 3: 15 (3-12); checks 4: 1 (0-2); checks 5: 0 (0-1). Lags 1 and 21: 5 survivors.


