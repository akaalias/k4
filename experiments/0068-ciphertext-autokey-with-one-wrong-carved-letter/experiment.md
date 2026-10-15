# 0068-ciphertext-autokey-with-one-wrong-carved-letter: The self-feeding autokey again, allowing one carved letter to be wrong, missing or extra

**Family:** 1-keyed-periodic  
**Parent:** 0002-ciphertext-autokey-all-lags  
**Decision:** reverted  
**Run:** 2026-10-15T13:12:13+00:00, 37.0 s, status ran  
**Time by phase:** design 40 s, implement 0 s, test 26 s, run 37 s, record 0 s

## In plain words

The autokey that feeds on earlier carved letters is the only recipe we have found that leaves the width-21 mark, yet experiment 2 showed it cannot produce the known letters from the copper as carved. The second message on the sculpture has a carving mistake, so we allow one mistake here too: one letter wrong, one missing or one extra, anywhere, at every distance back. Scrambled coppers given the same allowance show how many fits luck gives.

## Walkthrough, by hand

1. Take lag 21, the sculpture's alphabet KRYPTOSABCDEFGHIJLMNQUVWXZ counted from K = 0, Vigenere.
2. Place 22: carved F (12) minus known E (11) is 1; the carved letter 21 back is O (5); the residual is 1 - 5 = -4, which is 22.
3. Place 23: L (17) minus A (7) is 10; 21 back is B (8); residual 2.
4. Place 24: R (1) minus S (6) is 21; 21 back is K (0); residual 21.
5. The plain autokey needs every residual to be the same constant; already three differ.
6. One wrong carved letter can change at most two residuals, its own and the one 21 places later, so if more than two residuals disagree with the rest, no single mistake rescues this lag.

## Worked example (generated)

```
lag 21, sculpture's alphabet throughout, Vigenere

place  known  carved  21 back  residual
   22      E       F        O        22
   23      A       L        B         2
   24      S       R        K        21
   25      T       V        R        17
   26      N       Q        U         6
```

## Lineage

Inherits from 0002-ciphertext-autokey-all-lags. What changed: Experiment 2 tested the self-feeding autokey on the copper exactly as carved, and experiment 62 found it is the only recipe that makes the width-21 repeats. K2 has a known carving error. Here one carved letter may be wrong (any place, any other letter), missing, or extra, at every lag, with or without a constant shift.

## Hypothesis (domain expert)

Family 1 re-entered with a stated reason: ciphertext autokey is the only generator in 0062 that reproduces the width-21 repeats (lag 21, 5.4% of samples against 0.2%), and 0002, 0063 and 0064 tested it only on the exact copper. Sanborn's K2 has a confirmed carving omission (C14 in 02-sanborn-said.md; Kryptos Group 2006, sources/kryptos-group-2006-corrected-k2.txt), and C17/C18 allow a working text of 98. Construction: T[i] = s*A(c[i-L]) + k0, L = 1..96, k0 any constant (k0 = 0 is the plain autokey), plain, cipher and key alphabets standard or KRYPTOS, Vigenere or Beaufort, s = +1 or -1 (32 classes). Variants of the copper: one letter replaced by any other (97 x 25), one deleted (97), one unknown inserted (98). A substitution at place j can only touch the equation of the crib at j and of the crib at j + L, so substitutions are decided exactly by asking whether all other residuals agree and the touched ones can be met by one letter; deletions and insertions are recomputed in full. Survivors tallied by redundant checks against ten shuffled coppers. Clue entries: C11a ('auto-key'), C17(b), C18(b).

## Prediction

No lag survives with three or more redundant checks under any one-letter variant and class, including lag 21. Survivor counts at one and two checks match the ten shuffled coppers. Zero candidates pass.

## Method

1. For each lag and class, compute the residual at each known place past the lag: the total key minus the value of the carved letter that far back.
2. Exact copper: all residuals must agree.
3. One wrong letter at place j: all residuals not touching j must agree, and the one or two touched must be met by a single replacement letter.
4. One letter missing or extra: shift the copper and recompute.
5. Tally survivors by redundant checks and compare with ten shuffled coppers.

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
 "family": "ciphertext autokey with a constant shift, copper with one letter wrong, missing or extra",
 "lags": "1-96",
 "classes": 32,
 "variants": "97 x 25 substitutions (decided exactly), 97 deletions, 98 insertions",
 "cases": 602112,
 "complete": true,
 "controls": [
  true,
  true,
  true,
  true,
  true,
  true,
  true,
  true,
  true,
  true
 ],
 "survivors_by_checks": {
  "exact, checks 1": {
   "k4": 3,
   "controls": [
    0,
    1,
    1,
    1,
    0,
    4,
    3,
    1,
    4,
    2
   ]
  },
  "shift, checks 1": {
   "k4": 225,
   "controls": [
    16,
    197,
    131,
    199,
    300,
    202,
    293,
    480,
    415,
    248
   ]
  },
  "shift, checks 2": {
   "k4": 0,
   "controls": [
    0,
    1,
    0,
    0,
    72,
    1,
    1,
    3,
    0,
    0
   ]
  },
  "substitution, checks 2": {
   "k4": 6,
   "controls": [
    6,
    2,
    8,
    14,
    4,
    4,
    6,
    6,
    6,
    8
   ]
  },
  "substitution, checks 3": {
   "k4": 0,
   "controls": [
    0,
    0,
    2,
    0,
    0,
    2,
    0,
    0,
    0,
    0
   ]
  }
 },
 "survivors_3plus": [],
 "lag21_survivors": []
}
```

Notes: 602112 lag-class-variant cases (complete). Survivors, K4 (controls min-max): exact, checks 1: 3 (0-4); shift, checks 1: 225 (16-480); shift, checks 2: 0 (0-72); substitution, checks 2: 6 (2-14); substitution, checks 3: 0 (0-2). Three or more checks: 0. Lag 21: 0.


