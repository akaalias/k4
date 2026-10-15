# 0073-plaintext-autokey-plus-a-repeating-key: The message as its own key, plus a repeating secret word on top

**Family:** 1-keyed-periodic  
**Parent:** 0012-plaintext-autokey-chained-from-cribs  
**Decision:** reverted  
**Run:** 2026-10-15T13:24:51+00:00, 21.4 s, status ran  
**Time by phase:** design 33 s, implement 0 s, test 59 s, run 21 s, record 0 s

## In plain words

In a plaintext autokey cipher each letter is enciphered with the message letter a fixed distance back, so the message is its own key. Experiments 3 and 12 showed that alone does not fit. Here we add a repeating secret word on top. We can only test it where two known letters sit the right distance apart, but there are enough such pairs to get clear answers for many distances, and scrambled coppers show how many fits luck alone gives.

## Walkthrough, by hand

1. Lag 3, a 7-letter word, the sculpture's alphabet KRYPTOSABCDEFGHIJLMNQUVWXZ from K = 0, Vigenere.
2. Place 25: carved V (22) minus known T (4) is 18; the message letter 3 back is E (11); the word's letter is 18 - 11 = 7, in slot
3. 3. Place 32: carved K (0) minus known A (7) is -7, which is 19; 3 back is T (4); 19 - 4 = 15, also slot 3.
4. 7 and 15 disagree: lag 3 with a 7-letter word is dead under this way of using the table.
5. Repeat for every lag with known pairs, every word length and every way of using the table.

## Worked example (generated)

```
lag 3, 7-letter word, sculpture's alphabet throughout, Vigenere

place  known  carved  3 back  word letter  slot
   25      T       V       E            7     3
   32      A       K       T           15     3
   26      N       Q       A           20     4
   33      S       S       H           12     4
```

## Lineage

Inherits from 0012-plaintext-autokey-chained-from-cribs. What changed: Experiments 3 and 12 tested the autokey that feeds on the message itself, with no other key. The NSA's 1992 note named 'plain-text auto-key'. Here a repeating secret word is added on top, at every distance where two known letters can be compared and every word length, on the sculpture's table and on tables rebuilt from words.

## Hypothesis (domain expert)

Family 1, plaintext autokey as a component of a two-part key (C11a: NSA 1992 'plain-text auto-key', sources/nsa-foia-1992-2014-blackvault-compilation.txt; C5(b) 'key word/s'): T[i] = s*A(p[i-L]) + k[i mod P]. Only places where both p[i] and p[i-L] are known give equations: lags 1-12 inside EASTNORTHEAST, 1-10 inside BERLINCLOCK, 30-52 across them. Each such pair forces k at slot i mod P, and pairs sharing a slot must agree. Classes: plain, cipher and key alphabets standard or KRYPTOS, Vigenere or Beaufort, sign +1 or -1 (32 classes); plus one alphabet keyword-mixed from each vocabulary word, K1-K3 word and C13/C14 word (as in 0053) used on both sides, with the key read on it or on the standard alphabet (8 more per alphabet). Periods 1-96. Survivors tallied by redundant checks against ten shuffled coppers; no candidates (the key outside the pairs is unknown). Clue entries: C11a, C5(b).

## Prediction

No case with three or more redundant checks survives beyond the shuffled-copper range; the lags 7 and 21 named by the fingerprints and the NSA's 'interval 7' are no different. Zero candidates pass.

## Method

1. For each lag, list the pairs of known places that far apart.
2. For each class, the pair forces the secret word's letter in slot i mod P: total key minus the earlier message letter's value.
3. For each period, check slots agree; tally survivors by redundant checks.
4. Repeat on ten shuffled coppers.

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
 "family": "plaintext autokey plus a periodic key",
 "lags": "1-12 and 30-52 (where two known letters pair)",
 "periods": "1-96",
 "setups": 1320,
 "word_alphabets": 161,
 "cases": 4055040,
 "survivors_by_checks": {
  "checks 1": {
   "k4": 3171,
   "controls": [
    3462,
    3603,
    3296,
    3215,
    3733,
    3128,
    3214,
    3784,
    3069,
    3329
   ]
  },
  "checks 2": {
   "k4": 135,
   "controls": [
    152,
    110,
    135,
    100,
    106,
    113,
    101,
    111,
    96,
    76
   ]
  },
  "checks 3": {
   "k4": 12,
   "controls": [
    3,
    0,
    6,
    6,
    0,
    5,
    2,
    4,
    0,
    1
   ]
  },
  "checks 4": {
   "k4": 0,
   "controls": [
    1,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
   ]
  }
 },
 "survivors_3plus": [
  {
   "setup": "DELIVERING/same/vig/-1",
   "lag": 47,
   "period": 3,
   "checks": 3
  },
  {
   "setup": "PRESENTLY/std/beau/1",
   "lag": 33,
   "period": 1,
   "checks": 3
  },
  {
   "setup": "ROWS/same/vig/-1",
   "lag": 8,
   "period": 5,
   "checks": 3
  },
  {
   "setup": "ROWS/same/vig/-1",
   "lag": 8,
   "period": 8,
   "checks": 3
  },
  {
   "setup": "ROWS/same/vig/-1",
   "lag": 8,
   "period": 10,
   "checks": 3
  },
  {
   "setup": "ROWS/same/vig/-1",
   "lag": 8,
   "period": 20,
   "checks": 3
  },
  {
   "setup": "ROWS/same/vig/-1",
   "lag": 8,
   "period": 40,
   "checks": 3
  },
  {
   "setup": "SEVENTY/std/vig/1",
   "lag": 8,
   "period": 5,
   "checks": 3
  },
  {
   "setup": "SEVENTY/std/vig/1",
   "lag": 8,
   "period": 8,
   "checks": 3
  },
  {
   "setup": "SEVENTY/std/vig/1",
   "lag": 8,
   "period": 10,
   "checks": 3
  },
  {
   "setup": "SEVENTY/std/vig/1",
   "lag": 8,
   "period": 20,
   "checks": 3
  },
  {
   "setup": "SEVENTY/std/vig/1",
   "lag": 8,
   "period": 40,
   "checks": 3
  }
 ],
 "lag7_lag21_survivors": [
  {
   "setup": "ABSCISSA/same/vig/-1",
   "lag": 7,
   "period": 19,
   "checks": 2
  },
  {
   "setup": "ABSCISSA/same/vig/-1",
   "lag": 7,
   "period": 38,
   "checks": 2
  },
  {
   "setup": "AIR/same/vig/1",
   "lag": 7,
   "period": 37,
   "checks": 1
  },
  {
   "setup": "ANYTHING/same/beau/1",
   "lag": 7,
   "period": 9,
   "checks": 1
  },
  {
   "setup": "ANYTHING/same/beau/1",
   "lag": 7,
   "period": 15,
   "checks": 1
  },
  {
   "setup": "ANYTHING/same/beau/1",
   "lag": 7,
   "period": 45,
   "checks": 1
  },
  {
   "setup": "BURIED/std/vig/1",
   "lag": 7,
   "period": 37,
   "checks": 1
  },
  {
   "setup": "BURIED/std/vig/-1",
   "lag": 7,
   "period": 37,
   "checks": 1
  },
  {
   "setup": "BUT/same/beau/-1",
   "lag": 7,
   "period": 37,
   "checks": 1
  },
  {
   "setup": "CAIRO/same/beau/1",
   "lag": 7,
   "period": 37,
   "checks": 1
  },
  {
   "setup": "CAIRO/std/vig/1",
   "lag": 7,
   "period": 37,
   "checks": 1
  },
  {
   "setup": "CAIRO/std/vig/-1",
   "lag": 7,
   "period": 37,
   "checks": 1
  },
  {
   "setup": "CANDLE/same/beau/1",
   "lag": 7,
   "period": 37,
   "checks": 1
  },
  {
   "setup": "CARNARVON/same/beau/1",
   "lag": 7,
   "period": 37,
   "checks": 1
  },
  {
   "setup": "CARTER/std/beau/-1",
   "lag": 7,
   "period": 9,
   "checks": 1
  },
  {
   "setup": "CARTER/std/beau/-1",
   "lag": 7,
   "period": 15,
   "checks": 1
  },
  {
   "setup": "CARTER/std/beau/-1",
   "lag": 7,
   "period": 45,
   "checks": 1
  },
  {
   "setup": "CHAMBER/std/vig/1",
   "lag": 7,
   "period": 37,
   "checks": 1
  },
  {
   "setup": "CHAMBER/std/vig/-1",
   "lag": 7,
   "period": 37,
   "checks": 1
  },
  {
   "setup": "CIA/same/vig/1",
   "lag": 7,
   "period": 37,
   "checks": 1
  },
  {
   "setup": "DEBRIS/same/beau/-1",
   "lag": 7,
   "period": 37,
   "checks": 1
  },
  {
   "setup": "DELIVER/same/beau/1",
   "lag": 7,
   "period": 9,
   "checks": 1
  },
  {
   "setup": "DELIVER/same/beau/1",
   "lag": 7,
   "period": 15,
   "checks": 1
  },
  {
   "setup": "DELIVER/same/beau/1",
   "lag": 7,
   "period": 45,
   "checks": 1
  },
  {
   "setup": "DELIVERING/same/vig/-1",
   "lag": 7,
   "period": 11,
   "checks": 2
  },
  {
   "setup": "DELIVERING/same/vig/-1",
   "lag": 7,
   "period": 22,
   "checks": 2
  },
  {
   "setup": "DELIVERING/same/vig/-1",
   "lag": 7,
   "period": 44,
   "checks": 2
  },
  {
   "setup": "DIGETAL/same/beau/-1",
   "lag": 7,
   "period": 37,
   "checks": 1
  },
  {
   "setup": "DIGITAL/same/beau/-1",
   "lag": 7,
   "period": 9,
   "checks": 1
  },
  {
   "setup": "DIGITAL/same/beau/-1",
   "lag": 7,
   "period": 15,
   "checks": 1
  }
 ]
}
```

Notes: 4,055,040 cases, 1320 setups. Survivors by checks, K4 (controls min-max): checks 1: 3171 (3069-3784); checks 2: 135 (76-152); checks 3: 12 (0-6); checks 4: 0 (0-1). Three or more checks: 12.


