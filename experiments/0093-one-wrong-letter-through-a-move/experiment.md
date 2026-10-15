# 0093-one-wrong-letter-through-a-move: One carved letter wrong, through a K3-style move and a repeating key

**Family:** 6-transposition-then-tableau  
**Parent:** 0080-substitute-rotate-substitute-two-keys  
**Decision:** reverted  
**Run:** 2026-10-15T19:22:58+00:00, 296.0 s, status ran  
**Time by phase:** unattributed 429 s, run 296 s, record 0 s

## In plain words

Sanborn made at least one mistake carving K2. If he made one in K4, a correct method could fail our test at exactly one of the 24 known letters. So we rerun the grid moves of experiments 80 to 85 with a short repeating secret word, and this time accept any setting that fits all known letters but one. Allowing one miss also lets more chance settings through, so scrambled coppers tell us how many to expect.

## Walkthrough, by hand

1. Pick a move, say a clockwise quarter turn of a grid 8 wide, and a key length, say 9.
2. For each known letter, find where the move puts it and the key value that turns it into the carved letter there.
3. Group the known letters by key slot: carved place mod 9.
4. In each group, count the letters that disagree with the group's most common value.
5. A total of 0 fits outright; a total of 1 fits if that one carved letter is a carving error.
6. Repeat for every move, key length 1-26, both orders and every table rule, and on ten scrambled coppers.

## Worked example (generated)

```
clockwise quarter turn of a grid 8 wide, then a key of length 9; sculpture's alphabet, Vigenere

place  letter  lands at  copper  key value  slot (mod 9)
   22       E        71       Z         14             7
   23       A        83       C          2             1
   24       S        95       C          3             4
   25       T        10       H         10             0
   26       N        22       F         19             3
   27       O        34       S          1             6
   64       B        90       U         13             8
   65       E         5       U         10             4
   66       R        17       I         14             7

disagreements at period 9: 2 (2 means two or more)
```

## Lineage

Inherits from 0080-substitute-rotate-substitute-two-keys. What changed: 0031, 0050 and 0068 allowed one wrong carved letter only for keys with no move. Here every route of the type-1 library (K3's rule, one or two quarter turns, plain and true-keyword columnar, 27,852 distinct) is joined to a repeating key of length 1-26 before or after the move, and a setting counts as consistent if all known letters agree once at most one of them is set aside as a carving error.

## Hypothesis (domain expert)

Type 7 of directions.md, 'one letter off through types 1 and 2'. K2 carries a carving error Sanborn confirmed (the dropped S, corrected in 2006; 01-facts.md) and K1-K3 carry deliberate misspellings (C10, C17). A wrong carved letter outside the 24 crib images is invisible to crib tests; one on a crib image breaks exactly one equation. So: route library as in 0090 (forward and inverse, deduplicated); repeating key of period 1-26 after the move (slot = carved place mod p) or before it (slot = message place mod p); 8 tableau consistency classes. Within each key slot the forced values must agree; the number of disagreements is the sum over slots of (letters in slot - largest agreeing group). Zero is the plain test (0080-0085 bounds); one is one carving error. Counts per period compared with ten shuffled coppers.

## Prediction

With one miss allowed, the smallest consistent period on K4 is no lower than on the scrambled coppers, and the count at every period lies inside their range, give or take one period. No setting below period 14. Zero candidates.

## Method

1. Build the route library.
2. For each route, class and text, compute the key value forced at each known letter and its slot for each period and order.
3. Count the disagreements per period; record periods with zero and with one.
4. Repeat on ten shuffled coppers.
5. List K4's settings with one disagreement below period 14, and which known letter is set aside.

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
 "family": "type-1 route library, then or before a periodic tableau key, at most one known letter set aside",
 "distinct_routes": 27852,
 "periods": [
  1,
  26
 ],
 "classes": 8,
 "k4_live_exact_by_period": {
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
   1,
   33,
   35,
   458,
   1160,
   8065
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
   11,
   8610
  ]
 },
 "k4_live_one_miss_by_period": {
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
   3,
   22,
   980,
   1125,
   8457,
   4022,
   9531
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
   5,
   908,
   214206
  ]
 },
 "controls_one_miss_min": {
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
   15,
   526,
   1104,
   8450,
   3962,
   9473
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
   861,
   213916
  ]
 },
 "controls_one_miss_max": {
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
   9,
   26,
   859,
   1166,
   8552,
   4064,
   9697
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
   1008,
   214442
  ]
 },
 "periods_outside_control_range": {
  "A misses<=0": [
   25
  ],
  "A misses<=1": [
   22
  ],
  "B misses<=0": [],
  "B misses<=1": [
   24
  ]
 },
 "k4_smallest_period_with_at_most_one_miss": {
  "A": 20,
  "B": 24
 },
 "controls_smallest": {
  "A": [
   21,
   20,
   20,
   20,
   19,
   20,
   20,
   20,
   21,
   21
  ],
  "B": [
   24,
   25,
   24,
   24,
   24,
   25,
   24,
   24,
   24,
   24
  ]
 },
 "k4_one_miss_below_14": [],
 "n_k4_one_miss_below_14": 0,
 "controls": "10 shuffled coppers (seed 93), identical search",
 "order_A": "move, then key (slot = carved place mod p)",
 "order_B": "key, then move (slot = message place mod p)"
}
```

Notes: 27,852 routes x 8 classes x 2 orders, periods 1-26, one miss allowed. Smallest period with at most one miss: K4 {'A': 20, 'B': 24}, controls {'A': [21, 20, 20, 20, 19, 20, 20, 20, 21, 21], 'B': [24, 25, 24, 24, 24, 25, 24, 24, 24, 24]}. K4 one-miss settings below 14: 0. Outside control range: {'A misses<=0': [25], 'A misses<=1': [22], 'B misses<=0': [], 'B misses<=1': [24]}.


