# 0097-free-mixed-alphabets-after-a-move: A repeating key on unknown mixed alphabets (a free Quagmire) after or before a K3-style move

**Family:** 6-transposition-then-tableau  
**Parent:** 0096-both-fingerprints-from-two-stage-recipes  
**Decision:** reverted  
**Run:** 2026-10-15T19:47:30+00:00, 605.8 s, status ran  
**Time by phase:** unattributed 359 s, run 606 s, record 0 s

## In plain words

K1 and K2 used a table built from a scrambled alphabet that starts KRYPTOS. Sanborn said his table for K4 was slightly different. Here we let the scrambled alphabet be anything at all, unknown to us, and still ask whether a short repeating secret word on such a table, before or after a grid move, can explain the 24 known letters. We do not need to guess the alphabet: arithmetic on the 24 letters shows whether any alphabet could work.

## Walkthrough, by hand

1. Pick a move and a key length, say 7, after the move.
2. Each known letter lands at a carved place j and gives: index of the carved letter = index of the known letter + key slot j mod 7, all unknown.
3. If E lands twice in the same slot under two different carved letters, those two carved letters would need the same index: impossible.
4. Longer chains of such equations can force the same thing; solving the equations mod 2 and mod 13 finds every forced pair.
5. A setting with no forced pair is consistent: some alphabet and key fit.
6. Repeat for every move, key length 1-26, both orders and both table types, and on scrambled coppers.

## Worked example (generated)

```
no move, key length 7, unknown alphabets: known letters grouped by slot (place mod 7)

slot 0: E->F (22), T->R (29), B->N (64), L->Z (71)
slot 1: A->L (23), H->N (30), E->Y (65), O->F (72)
slot 2: S->R (24), E->G (31), R->P (66), C->P (73)
slot 3: T->V (25), A->K (32), L->V (67), K->K (74)
slot 4: N->Q (26), S->S (33), I->T (68)
slot 5: O->Q (27), T->S (34), N->T (69)
slot 6: R->P (28), C->M (70)

free alphabet per slot (functional and one-to-one): False
one mixed alphabet pair shifted by the key (Quagmire IV): not reached
```

## Lineage

Inherits from 0096-both-fingerprints-from-two-stage-recipes. What changed: 0080-0094 used the standard or KRYPTOS alphabet, fixed. 0096 found that any key repeating every 3, 7 or 21 carved letters after a move makes the width-21 repeats 50 times more often than chance; on a fixed alphabet those periods are dead. Here the alphabets are unknown: the tableau is built from an unknown mixed alphabet (Quagmire III) or an unknown pair (Quagmire IV), shifted by a repeating key, after or before every move of the type-1 library, and the cribs are tested exactly by linear algebra.

## Hypothesis (domain expert)

Type 2 open item 'width 7 with two free alphabets' and the type-1 gap 'two unknown alphabets at periods 13-26' (directions.md, prior-work database). Sanborn: 'slightly different tableau' (C11a, 0071); K1-K2 use a keyed Quagmire III. 0096: periods dividing 21 after a move reproduce the width-21 repeats (1.5% against 0.03%). Model: index(c_j) = index'(m_j) + k[slot], slot = carved place mod p after the move (order A) or message place mod p before it (order B); index and index' unknown bijections (equal for Quagmire III). Each known letter gives a homogeneous linear equation over Z26 in the unknown letter indices and key values. By the Chinese remainder theorem, two letters are forced to the same index mod 26 exactly when the solution spaces over GF(2) and GF(13) both force it; that, or three letters forced together mod 13, contradicts the bijection. Filter first by the weaker free-alphabet-per-slot test (functional and injective within a slot), periods 1-26; the linear test at periods 3, 7 and 21, the divisors of 21 that 0096 ties to the repeats (the time budget allows no more). Moves as in 0090 plus no move; ten shuffled coppers.

## Prediction

Under Quagmire III and IV the consistent counts at periods 3, 7 and 21 lie inside the ten shuffled coppers' range, give or take one period. Zero candidates.

## Method

1. Build the route library.
2. For each route, order, period and text, apply the free-alphabet-per-slot filter.
3. For survivors at periods 3, 7 and 21, write the 24 linear equations and compute the solution space over GF(2) and GF(13).
4. Reject if two different letters of one alphabet are forced to the same index in both fields, or three to the same index mod 13.
5. Count survivors per period, model and order, on K4 and ten shuffled coppers.

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
 "family": "periodic key on unknown mixed alphabets (Quagmire III: one alphabet; IV: a pair), type-1 moves plus no move",
 "routes": 27853,
 "routes_done": 27853,
 "periods_free_per_slot": [
  1,
  26
 ],
 "periods_linear_test": [
  3,
  7,
  21
 ],
 "orders": {
  "A": "move, then key (slot = carved place mod p)",
  "B": "key, then move"
 },
 "k4_free_per_slot_by_period": {
  "A": [
   0,
   0,
   44,
   116,
   270,
   1207,
   1758,
   3013,
   3688,
   3549,
   4921,
   7366,
   9329,
   9545,
   8727,
   10186,
   9909,
   12872,
   12263,
   12570,
   12820,
   14917,
   16706,
   16594,
   13463,
   18681
  ],
  "B": [
   0,
   0,
   0,
   4,
   16,
   6802,
   8806,
   9348,
   0,
   14074,
   16052,
   17252,
   19008,
   18782,
   716,
   21013,
   726,
   21409,
   729,
   18728,
   18782,
   20063,
   21511,
   23312,
   25025,
   26858
  ]
 },
 "k4_live_by_period": {
  "III A": [
   0,
   0,
   0,
   0,
   0,
   0,
   87,
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
   6286,
   0,
   0,
   0,
   0,
   0
  ],
  "III B": [
   0,
   0,
   0,
   0,
   0,
   0,
   481,
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
   5964,
   0,
   0,
   0,
   0,
   0
  ],
  "IV A": [
   0,
   0,
   16,
   0,
   0,
   0,
   1344,
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
   12478,
   0,
   0,
   0,
   0,
   0
  ],
  "IV B": [
   0,
   0,
   0,
   0,
   0,
   0,
   6733,
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
   17210,
   0,
   0,
   0,
   0,
   0
  ]
 },
 "controls_live_min": {
  "III A": [
   0,
   0,
   0,
   0,
   0,
   0,
   66,
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
   4786,
   0,
   0,
   0,
   0,
   0
  ],
  "III B": [
   0,
   0,
   0,
   0,
   0,
   0,
   415,
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
   5838,
   0,
   0,
   0,
   0,
   0
  ],
  "IV A": [
   0,
   0,
   1,
   0,
   0,
   0,
   1017,
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
   8758,
   0,
   0,
   0,
   0,
   0
  ],
  "IV B": [
   0,
   0,
   0,
   0,
   0,
   0,
   6150,
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
   16353,
   0,
   0,
   0,
   0,
   0
  ]
 },
 "controls_live_max": {
  "III A": [
   0,
   0,
   0,
   0,
   0,
   0,
   177,
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
   7177,
   0,
   0,
   0,
   0,
   0
  ],
  "III B": [
   0,
   0,
   0,
   0,
   0,
   0,
   543,
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
   6289,
   0,
   0,
   0,
   0,
   0
  ],
  "IV A": [
   0,
   0,
   12,
   0,
   0,
   0,
   2157,
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
   14458,
   0,
   0,
   0,
   0,
   0
  ],
  "IV B": [
   0,
   0,
   0,
   0,
   0,
   0,
   6856,
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
   17644,
   0,
   0,
   0,
   0,
   0
  ]
 },
 "periods_outside_control_range": {
  "III A": [],
  "III B": [],
  "IV A": [
   3
  ],
  "IV B": []
 },
 "k4_live_low_periods": [
  {
   "route": "K3 rule a=5 b=2 inverse",
   "order": "A",
   "model": "IV",
   "period": 3
  },
  {
   "route": "K3 rule a=90 b=7",
   "order": "A",
   "model": "IV",
   "period": 3
  },
  {
   "route": "K3 rule a=60 b=20",
   "order": "A",
   "model": "IV",
   "period": 3
  },
  {
   "route": "columnar 60 inverse",
   "order": "A",
   "model": "IV",
   "period": 3
  },
  {
   "route": "two turns cw 6,33",
   "order": "A",
   "model": "IV",
   "period": 3
  },
  {
   "route": "two turns cw 14,47 inverse",
   "order": "A",
   "model": "IV",
   "period": 3
  },
  {
   "route": "two turns cw 48,94 inverse",
   "order": "A",
   "model": "IV",
   "period": 3
  },
  {
   "route": "two turns cw 49,47 inverse",
   "order": "A",
   "model": "IV",
   "period": 3
  },
  {
   "route": "two turns cw 51,87 inverse",
   "order": "A",
   "model": "IV",
   "period": 3
  },
  {
   "route": "two turns cw 53,94 inverse",
   "order": "A",
   "model": "IV",
   "period": 3
  },
  {
   "route": "two turns cw 57,87 inverse",
   "order": "A",
   "model": "IV",
   "period": 3
  },
  {
   "route": "two turns cw 57,89 inverse",
   "order": "A",
   "model": "IV",
   "period": 3
  },
  {
   "route": "two turns cw 59,86 inverse",
   "order": "A",
   "model": "IV",
   "period": 3
  },
  {
   "route": "two turns cw 92,51 inverse",
   "order": "A",
   "model": "IV",
   "period": 3
  },
  {
   "route": "two turns cw 92,57 inverse",
   "order": "A",
   "model": "IV",
   "period": 3
  },
  {
   "route": "two turns cw 93,57 inverse",
   "order": "A",
   "model": "IV",
   "period": 3
  },
  {
   "route": "K3 rule a=14 b=1",
   "order": "A",
   "model": "IV",
   "period": 7
  },
  {
   "route": "K3 rule a=14 b=1",
   "order": "B",
   "model": "IV",
   "period": 7
  },
  {
   "route": "K3 rule a=17 b=1",
   "order": "A",
   "model": "IV",
   "period": 7
  },
  {
   "route": "K3 rule a=17 b=1",
   "order": "B",
   "model": "IV",
   "period": 7
  },
  {
   "route": "K3 rule a=18 b=1",
   "order": "A",
   "model": "IV",
   "period": 7
  },
  {
   "route": "K3 rule a=18 b=1",
   "order": "B",
   "model": "IV",
   "period": 7
  },
  {
   "route": "K3 rule a=27 b=1",
   "order": "B",
   "model": "IV",
   "period": 7
  },
  {
   "route": "K3 rule a=28 b=1",
   "order": "B",
   "model": "IV",
   "period": 7
  },
  {
   "route": "K3 rule a=29 b=1",
   "order": "B",
   "model": "IV",
   "period": 7
  },
  {
   "route": "K3 rule a=35 b=1",
   "order": "B",
   "model": "IV",
   "period": 7
  },
  {
   "route": "K3 rule a=36 b=1",
   "order": "B",
   "model": "IV",
   "period": 7
  },
  {
   "route": "K3 rule a=37 b=1",
   "order": "B",
   "model": "IV",
   "period": 7
  },
  {
   "route": "K3 rule a=0 b=2 inverse",
   "order": "A",
   "model": "IV",
   "period": 7
  },
  {
   "route": "K3 rule a=2 b=2 inverse",
   "order": "A",
   "model": "IV",
   "period": 7
  },
  {
   "route": "K3 rule a=3 b=2",
   "order": "B",
   "model": "IV",
   "period": 7
  },
  {
   "route": "K3 rule a=4 b=2 inverse",
   "order": "A",
   "model": "IV",
   "period": 7
  },
  {
   "route": "K3 rule a=4 b=2 inverse",
   "order": "B",
   "model": "IV",
   "period": 7
  },
  {
   "route": "K3 rule a=5 b=2",
   "order": "B",
   "model": "IV",
   "period": 7
  },
  {
   "route": "K3 rule a=6 b=2 inverse",
   "order": "A",
   "model": "IV",
   "period": 7
  },
  {
   "route": "K3 rule a=7 b=2",
   "order": "B",
   "model": "IV",
   "period": 7
  },
  {
   "route": "K3 rule a=9 b=2",
   "order": "B",
   "model": "IV",
   "period": 7
  },
  {
   "route": "K3 rule a=10 b=2",
   "order": "B",
   "model": "IV",
   "period": 7
  },
  {
   "route": "K3 rule a=11 b=2",
   "order": "B",
   "model": "IV",
   "period": 7
  },
  {
   "route": "K3 rule a=12 b=2",
   "order": "B",
   "model": "IV",
   "period": 7
  }
 ],
 "n_k4_live_low_periods": 50599,
 "controls": "10 shuffled coppers (seed 97), identical search"
}
```

Notes: 27,853 of 27,853 routes x 2 orders x periods 1-26 x 2 models. K4 live at periods 3/7/14/21: {'III A': [0, 87, 0, 6286], 'III B': [0, 481, 0, 5964], 'IV A': [16, 1344, 0, 12478], 'IV B': [0, 6733, 0, 17210]}. Periods outside the control range: {'III A': [], 'III B': [], 'IV A': [3], 'IV B': []}. K4 live at periods 3, 7, 21: 50599.


