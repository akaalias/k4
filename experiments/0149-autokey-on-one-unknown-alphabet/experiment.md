# 0149-autokey-on-one-unknown-alphabet: F1.7: ciphertext and plaintext autokey on one unknown alphabet (both sides, any of 26! orders), every lag, three forms, decided exactly

**Family:** 1-keyed-periodic  
**Parent:** 0098-sculpture-running-keys-on-an-unknown-alphabet  
**Decision:** reverted  
**Run:** 2026-10-16T20:49:42+00:00, 88.4 s, status ran  
**Time by phase:** unattributed 20 s, run 88 s, record 0 s

## In plain words

In an autokey cipher the message (or the scrambled text) becomes its own key, a fixed number of letters back. We had only tried it with the sculpture's alphabets and alphabets built from words. Here the alphabet can be in any order at all. The known letters then give equations about the alphabet alone, and a search decides exactly, for every distance back, whether any alphabet satisfies them, on the carved text and on scrambled copies.

## Walkthrough, by hand

1. Ciphertext autokey at lag 8: the key for place i is the carved letter at place i - 8.
2. At known place 30 (H under N), the key is the carved letter at 22, F: place(N) = place(H) + place(F) in the unknown alphabet.
3. Each known place past the primer gives one such equation; 24 equations in 26 unknown places.
4. Search for one alphabet order that satisfies all of them, filling places one at a time and following each equation that has a single unknown left.
5. Repeat for every lag, the three ways of using the table, plaintext autokey, and scrambled copies.

## Worked example (generated)

```
ciphertext autokey, lag 8, added form, one unknown alphabet: one equation per known place past the primer

place 22: place(F) = place(E) + place(S)   (key: carved letter at 14)
place 23: place(L) = place(A) + place(O)   (key: carved letter at 15)
place 24: place(R) = place(S) + place(L)   (key: carved letter at 16)
place 25: place(V) = place(T) + place(I)   (key: carved letter at 17)
place 26: place(Q) = place(N) + place(F)   (key: carved letter at 18)
place 27: place(Q) = place(O) + place(B)   (key: carved letter at 19)
place 28: place(P) = place(R) + place(B)   (key: carved letter at 20)
place 29: place(R) = place(T) + place(W)   (key: carved letter at 21)
place 30: place(N) = place(H) + place(F)   (key: carved letter at 22)
place 31: place(G) = place(E) + place(L)   (key: carved letter at 23)
...
24 equations in the unknown places; solved exactly
```

## Lineage

Inherits from 0098-sculpture-running-keys-on-an-unknown-alphabet. What changed: F1.7, no move. Autokey was tested on the standard, KRYPTOS and 1,092 keyword tables (0002, 0025, 0064, 0071, 0072) but never on a free alphabet: the NSA's 1992 guess (C11a) on K1 and K2's system. With one unknown alphabet x on both sides, each known letter past the primer gives an equation in alphabet places only: ciphertext autokey x(c_i) = x(p_i) + x(c_{i-L}) (and the Beaufort and variant forms); plaintext autokey the same with the message letter L back, usable where both letters are known (lags 1-12 and 30-52). Decided exactly by a propagation search over the 26 places (one-to-one), every lag 1-96, ten scrambled coppers. The move-first version is left for a later run (27,852 moves x 96 lags x 3 forms x 11 texts, about 90 million searches).

## Hypothesis (domain expert)

C11a (NSA 1992, knowledge/sources/nsa-foia-1992-2014-blackvault-compilation.txt: 'plain-text auto-key... if a high-frequency letter is assigned 0'; NSA 2007 summary, nsa-2014-summary-of-previous-work.txt: plaintext and ciphertext autokey tested), C27(c) (a 'slightly different' tableau: any alphabet), C1(b). Model: x a bijection letters -> Z26; forms V: x(c) = x(p) + x(k), B: x(c) = x(k) - x(p), R: x(c) = x(p) - x(k); key letter k_i = c_{i-L} (ciphertext autokey, primer free for i <= L) or p_{i-L} (plaintext autokey). Solver: depth-first over places with propagation of every equation left with one open variable, translation fixed where the equations allow, node limit 200,000 (undecided counted); checked on planted autokey texts under random alphabets before K4. Statistic fixed before the run: per (kind, form, lag) fit or not; a K4 fit counts as rare where at most 1 of 10 coppers fit; K4's rare fits against each copper's rare fits against the rest.

## Prediction

Short lags die (many equations), long lags fit (few), K4 like the coppers: rare fits on K4 no more than the most a copper has against the rest. Fitting cells are left for an English decider (F1.5's design 2), which this run does not apply. Zero candidates.

## Method

1. Check the solver: 6 planted autokey texts (random alphabet, random lag and form, both kinds) must fit.
2. For K4 and 10 coppers, each kind, form and lag: build the equations, decide.
3. Count fits per cell; mark rare fits; compare K4 with the coppers.

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
 "family": "ciphertext and plaintext autokey on one unknown alphabet (both sides), no move, every lag 1-96, three forms",
 "solver": "propagation depth-first over the 26 places, node limit 200,000; checked on 6 planted texts",
 "summary": {
  "ct/V": {
   "lags_with_equations": 73,
   "k4_fit_lags": [
    37,
    41,
    46,
    60,
    64,
    67,
    69,
    70,
    71,
    72,
    73
   ],
   "coppers_fit_count": [
    27,
    14,
    4,
    4,
    20,
    22,
    9,
    16,
    5,
    15
   ],
   "k4_fit_count": 11
  },
  "ct/B": {
   "lags_with_equations": 73,
   "k4_fit_lags": [
    32,
    34,
    36,
    38,
    41,
    43,
    46,
    47,
    48,
    52,
    54,
    56,
    57,
    59,
    61,
    64,
    66,
    67,
    68,
    69,
    70,
    72,
    73
   ],
   "coppers_fit_count": [
    23,
    17,
    23,
    3,
    25,
    16,
    26,
    24,
    4,
    3
   ],
   "k4_fit_count": 23
  },
  "ct/R": {
   "lags_with_equations": 73,
   "k4_fit_lags": [
    41,
    43,
    60,
    61,
    67,
    69,
    70,
    72,
    73
   ],
   "coppers_fit_count": [
    27,
    12,
    4,
    4,
    17,
    30,
    9,
    12,
    4,
    15
   ],
   "k4_fit_count": 9
  },
  "pt/V": {
   "lags_with_equations": 35,
   "k4_fit_lags": [
    11,
    12,
    30,
    31,
    32,
    33,
    34,
    35,
    36,
    37,
    38,
    39,
    46,
    48,
    49,
    50,
    51,
    52
   ],
   "coppers_fit_count": [
    22,
    16,
    12,
    10,
    22,
    20,
    16,
    17,
    16,
    20
   ],
   "k4_fit_count": 18
  },
  "pt/B": {
   "lags_with_equations": 35,
   "k4_fit_lags": [
    10,
    11,
    12,
    30,
    31,
    32,
    33,
    36,
    37,
    39,
    41,
    44,
    45,
    46,
    47,
    48,
    49,
    50,
    51,
    52,
    6,
    7,
    8
   ],
   "coppers_fit_count": [
    19,
    16,
    22,
    15,
    21,
    21,
    21,
    24,
    16,
    14
   ],
   "k4_fit_count": 23
  },
  "pt/R": {
   "lags_with_equations": 35,
   "k4_fit_lags": [
    11,
    12,
    30,
    31,
    32,
    33,
    34,
    35,
    37,
    38,
    39,
    44,
    46,
    47,
    48,
    49,
    50,
    51,
    52
   ],
   "coppers_fit_count": [
    25,
    16,
    12,
    14,
    17,
    20,
    15,
    17,
    15,
    18
   ],
   "k4_fit_count": 19
  }
 },
 "undecided": {
  "k4": 7,
  "controls": [
   19,
   5,
   0,
   6,
   6,
   9,
   1,
   6,
   20,
   14
  ]
 },
 "k4_rare_fits": [
  "ct/B/61",
  "ct/V/64",
  "pt/B/6",
  "pt/V/39"
 ],
 "null_rare_fits_per_copper": [
  22,
  7,
  2,
  0,
  13,
  27,
  7,
  12,
  1,
  11
 ],
 "stop_queue": false,
 "controls": "10 shuffled coppers (seed 147), identical search",
 "exhaustive": "exact per cell; undecided counted",
 "not_covered": "the move-first version (27,852 moves x 96 lags x 3 forms x 11 texts)"
}
```

Notes: ct/V K4 11 fits (coppers 4-27), ct/B K4 23 fits (coppers 3-26), ct/R K4 9 fits (coppers 4-30), pt/V K4 18 fits (coppers 10-22), pt/B K4 23 fits (coppers 14-24), pt/R K4 19 fits (coppers 12-25); rare K4 fits 4 vs null 0-27; stop False; undecided K4 7


