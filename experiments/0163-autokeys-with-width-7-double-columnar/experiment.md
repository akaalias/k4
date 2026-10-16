# 0163-autokeys-with-width-7-double-columnar: F6.9: ciphertext and plaintext autokey, every lag, joined to 0084's double columnar routes (one stage of width 7 in all 5,040 orders), either order, on the sculpture's tables

**Family:** 6-transposition-then-tableau  
**Parent:** 0084-width-7-double-columnar  
**Decision:** reverted  
**Run:** 2026-10-16T22:40:52+00:00, 257.1 s, status ran  
**Time by phase:** unattributed 85 s, run 257 s, record 0 s

## In plain words

An autokey cipher uses the message, or the enciphered text, as its own key, a fixed number of letters back. Here it is combined with a double grid move in which one grid is seven wide (KRYPTOS has seven letters, and K4's doubled letters line up in sevens), in every column order. On the sculpture's tables each known letter can be checked directly, for every distance back, on the carved text and scrambled copies.

## Walkthrough, by hand

1. Write the message in rows of 7 and read the columns in some order, say 3 1 6 0 4 2 5; then write it in rows of 12 and read down the columns.
2. Encipher the moved text by ciphertext autokey at lag 8: each letter's key is the carved letter 8 places before.
3. At each known letter's landing place, look up the carved letter there and the one 8 before: the table says which message letter that pair gives; it must be the known letter.
4. Repeat for every order, width, lag, table and form, and on scrambled copies.

## Worked example (generated)

```
rows of 7 read in column order 3 1 6 0 4 2 5, then rows of 12 read down; ciphertext autokey at lag 8 after the move

place  letter  lands at  carved  carved 8 before
   22       E        69       T                N
   23       A        43       S                O
   24       S         7       X                -
   64       B        22       F                S
   65       E        91       A                C
```

## Lineage

Inherits from 0084-width-7-double-columnar. What changed: F6.9 (pivot audit, issue #55, D11). 0084 joined double columnar routes with one stage of width 7 in all 5,040 column orders to a repeating key; 0081 joined autokeys to the type-1 library. Here the two meet: the same routes (a width-7 stage in every order, the other a plain columnar of width 2-30 or a puzzle-word columnar, either first, forward and inverse, deduplicated) with ciphertext or plaintext autokey at every lag 1-96, the autokey after the move (on the moved stream) or before it, one alphabet throughout (standard or KRYPTOS), three rules. On a fixed table every check is a direct comparison; compiled; ten scrambled coppers.

## Hypothesis (domain expert)

C11a (NSA 1992: 'plain-text auto-key' and 'interval 7', knowledge/sources/nsa-foia-1992-2014-blackvault-compilation.txt), C8(a) (KRYPTOS's seven letters as a column key), directions.md type 2 (sevens: the width-7 doublet column, 0056). Model: A move then autokey: c_j = T(y_j, k_j), k_j = c_{j-L} (ciphertext) or y_{j-L} (plaintext); B autokey then move: e_i = T(p_i, k_i), k_i = e_{i-L} or p_{i-L}, c_{M(i)} = e_i. Checks: every known letter whose key letter is known (always for ciphertext autokey past the primer; for plaintext autokey when the key's place is a known letter). A setting survives if every check agrees. Statistic fixed before the run (0081's): survivors with five or more checks per (kind, order), K4 against the coppers' range.

## Prediction

Survivors with five or more checks at the coppers' rate in every kind and order (0081 found none with five on the type-1 library). Zero candidates.

## Method

1. Stage maps: the 5,040 width-7 orders; second stages plain columnar 2-30 and puzzle-word columnar.
2. Compiled: compose both orders, forward and inverse, deduplicate; for each route, lag, table and rule, the four autokey forms; count survivors by checks.
3. K4 against the coppers.

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
 "family": "ciphertext and plaintext autokey at lags 1-96, one alphabet (std or KRYPTOS), 3 rules, after or before 0084's width-7 double columnar routes",
 "width7_orders": 5040,
 "second_stages": 163,
 "second_stages_done": 163,
 "distinct_routes": 3284523,
 "duplicates_skipped": 1557,
 "summary": {
  "A ciphertext autokey": {
   "k4_ge5": 0,
   "coppers_ge5": [
    3,
    2,
    0,
    0,
    8,
    0,
    0,
    0,
    1,
    8
   ],
   "k4_ge4": 99,
   "coppers_ge4": [
    76,
    97,
    136,
    297,
    118,
    124,
    82,
    77,
    153,
    103
   ],
   "k4_max_checks_survivor": 4
  },
  "A plaintext autokey": {
   "k4_ge5": 9,
   "coppers_ge5": [
    5,
    21,
    11,
    21,
    10,
    6,
    10,
    9,
    9,
    11
   ],
   "k4_ge4": 422,
   "coppers_ge4": [
    359,
    474,
    427,
    504,
    425,
    480,
    415,
    403,
    509,
    334
   ],
   "k4_max_checks_survivor": 5
  },
  "B ciphertext autokey": {
   "k4_ge5": 1,
   "coppers_ge5": [
    0,
    1,
    0,
    1,
    0,
    1,
    1,
    0,
    0,
    1
   ],
   "k4_ge4": 31,
   "coppers_ge4": [
    95,
    23,
    24,
    44,
    40,
    46,
    42,
    197,
    18,
    19
   ],
   "k4_max_checks_survivor": 5
  },
  "B plaintext autokey": {
   "k4_ge5": 0,
   "coppers_ge5": [
    0,
    2,
    0,
    480,
    5,
    4,
    0,
    0,
    2,
    0
   ],
   "k4_ge4": 180,
   "coppers_ge4": [
    766,
    66,
    568,
    516,
    169,
    34,
    64,
    80,
    176,
    44
   ],
   "k4_max_checks_survivor": 4
  }
 },
 "seconds": 256,
 "controls": "10 shuffled coppers (seed 1609)",
 "exhaustive": "exact for every second stage done"
}
```

Notes: A ciphertext autokey: >=5 checks K4 0 (coppers 0-8); A plaintext autokey: >=5 checks K4 9 (coppers 5-21); B ciphertext autokey: >=5 checks K4 1 (coppers 0-1); B plaintext autokey: >=5 checks K4 0 (coppers 0-480)


