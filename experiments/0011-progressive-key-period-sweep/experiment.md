# 0011-progressive-key-period-sweep: A progressive key: the key word steps forward on every repeat, which revives the short periods

**Family:** 1-keyed-periodic  
**Parent:** 0005-quagmire-period-sweep-forced-keys  
**Decision:** reverted  
**Run:** 2026-10-14T16:57:06+00:00, 1.3 s, status ran  
**Time by phase:** design 15 s, implement 352 s, test 0 s, run 1 s, record 0 s

## In plain words

A repeating secret word was ruled out at most lengths because two known letters that would share the same letter of the word disagreed. But an old trick fixes that: each time the secret word repeats, every letter of it slides forward by a fixed amount. Then the two known letters no longer need to agree, they need to differ by that slide. We try every word length and every slide and ask which combinations the 24 known letters allow, and whether any of the puzzle's words fits what they force.

## Walkthrough, by hand

1. Choose period 13 and step 1, per-repeat form, with the sculpture's alphabet throughout and Vigenere.
2. Position 22 is in repeat 1 (positions 14 to 26), slot
8. Its forced key letter, from E and F, is R, index 1 in KRYPTOS; subtract one step for repeat 1: index 0, K.
3. Position 35 would be slot 8 of repeat 2, but it is not a crib. Position 74, the K of CLOCK, is repeat 5, slot 8: its forced key letter K against ciphertext K is index 0; subtract 5 steps: index
21. 
4. Slot 8 is now forced to two different letters, so period 13 with step 1 is dead under this convention.
5. Try the other 25 steps and the other 23 conventions.
6. A survivor gives a pattern of forced base letters with blanks; slide the puzzle's words across it.

## Worked example (generated)

```
period 13, step 1, per-repeat; plain/cipher/key all on the KRYPTOS alphabet, Vigenere

pos  plain  cipher  forced key  index  repeat  minus step  base slot
 22    E      F        R         1      1         0 (K)     8
 23    A      L        D        10      1         9 (C)     9
 24    S      R        U        21      1        20 (Q)     10
 25    T      V        M        18      1        17 (L)     11
 26    N      Q        R         1      1         0 (K)     12
 64    B      N        E        11      4         7 (A)     11
 65    E      Y        L        17      4        13 (G)     12
 74    K      K        K         0      5        21 (U)     8

positions 22 and 74 share slot 8; their base letters must agree for period 13 step 1 to live.
```

## Lineage

Inherits from 0005-quagmire-period-sweep-forced-keys. What changed: The periodic key gains a progression: on each repeat, or on each letter, every key letter moves a fixed number of places along the key alphabet. Periods 1 to 26 and 30 to 52, dead under a plain periodic key, are back in play.

## Hypothesis (domain expert)

Progressive-key Vigenere is in every hand-cipher manual Scheidt taught from (Friedman's Military Cryptanalysis, Part II; C5, C6): key index at position i is base[i mod P] plus d times the repeat number, or plus d times i for the letter-wise form. 0005 excluded periods 1-26 and 30-52 for d = 0 only. Here d runs 0-25, P 1-97, both progression forms, under the 24 conventions. For each combination the crib at position i forces base[(i mod P)] after the progression is subtracted; a conflict kills it. Survivors at P up to 30 get their forced base fragment matched against the vocabulary and K1-K3 windows; each match is decrypted and submitted. Stein's I.C. peak at 13 (C28) is a specific target: period 13 with any step. Bounds: complete for progressive periodic tableau systems under the stated conventions, periods and steps.

## Prediction

Most (period, step) pairs below 27 still die, because the cribs collide many times and a single step cannot reconcile them all. A scatter of survivors appears at periods 13 to 26 for some step under some convention, consistent with chance. No forced fragment matches a vocabulary word or K1-K3 window; zero candidates pass.

## Method

1. For each convention, period P, step d and progression form, compute for each crib the forced key index, subtract the progression, and reduce to the base slot.
2. A slot forced to two different letters kills the combination.
3. Count survivors per period.
4. For survivors with P up to 30, match the forced base fragment against the vocabulary and all K1-K3 windows of length P; decrypt and submit any match.
5. Record the survivor map by period and step.

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
 "family": "progressive-key periodic tableau, separate alphabets",
 "conventions": 24,
 "periods": "1-97",
 "steps": "0-25",
 "forms": [
  "per-repeat",
  "per-letter"
 ],
 "combinations_checked": 121056,
 "surviving_steps_by_period_up_to_30": {
  "26": {
   "per-repeat": 10,
   "per-letter": 0
  },
  "27": {
   "per-repeat": 26,
   "per-letter": 26
  },
  "28": {
   "per-repeat": 26,
   "per-letter": 26
  },
  "29": {
   "per-repeat": 26,
   "per-letter": 26
  },
  "30": {
   "per-repeat": 7,
   "per-letter": 0
  }
 },
 "period_13_survivors": {},
 "periods_with_no_survivor_any_step": [
  1,
  2,
  3,
  4,
  5,
  6,
  7,
  8,
  9,
  10,
  11,
  12,
  13,
  14,
  15,
  16,
  17,
  18,
  19,
  20,
  21,
  22,
  23,
  24,
  25,
  31,
  32,
  33,
  34,
  35,
  36,
  37,
  38,
  39,
  40,
  41,
  42,
  43,
  44,
  45,
  46,
  47,
  48,
  49,
  50,
  51
 ],
 "fragment_matches": 0,
 "key_pool": "vocabulary words and K1-K3 windows of length P for P <= 30"
}
```

Notes: 121056 (form, period, step, convention) combinations; 0 fragment matches submitted.


