# 0066-ciphertext-autokey-plus-a-repeating-key: The previous carved letters as a key, plus a repeating secret word on top

**Family:** 1-keyed-periodic  
**Parent:** 0065-constructions-that-line-up-doublets-in-sevens  
**Decision:** reverted  
**Run:** 2026-10-15T13:07:54+00:00, 2.1 s, status ran  
**Time by phase:** design 36 s, implement 0 s, test 0 s, run 2 s, record 0 s

## In plain words

An autokey cipher can feed on the carved letters themselves: each letter is enciphered with the carved letter a fixed distance back. Experiment 2 showed that alone cannot produce the known letters. Here a repeating secret word is added on top, of any length, at any distance back. Because we can see every carved letter, the feeding part can be undone exactly, which leaves an ordinary repeating secret word that the 24 known letters either fit or do not. Scrambled coppers run through the same test show how many fits luck alone produces.

## Walkthrough, by hand

1. Take lag 1 and a 7-letter secret word, with every letter counted along KRYPTOSABCDEFGHIJLMNQUVWXZ from K = 0.
2. Place 22: known E (11), carved F (12), previous carved W (23): the secret word's letter is 12 - 11 - 23 = -22, which is 4, T, in slot 0.
3. Place 29, also slot 0: known T (4), carved R (1), previous carved P (3): 1 - 4 - 3 = -6, which is 20, Q.
4. T and Q disagree, so this lag and word length are dead under this way of using the table.
5. Places 64 and 71 (slot 0 too) would force P and J.
6. Repeat for every lag, every word length, and every way of using the table.

## Worked example (generated)

```
lag 1, period 7, sculpture's alphabet throughout, Vigenere, s = +1

place  known  carved  previous  key letter  slot
   22      E       F         W           T     0
   29      T       R         P           Q     0
   64      B       N         B           P     0
   71      L       Z         M           J     0
```

## Lineage

Inherits from 0065-constructions-that-line-up-doublets-in-sevens. What changed: Experiment 65 found that a cipher feeding on the previous carved letter, combined with a repeating secret word of 7, is the only recipe that lines doublets up in sevens. Experiment 2 killed the plain ciphertext autokey; this adds the repeating secret word on top, at every distance back and every length of word, and tests it exactly against the known letters.

## Hypothesis (domain expert)

Family 1 re-entered with a stated reason: 0065 and 0062 point at ciphertext feedback (lag 1 makes the width-7 doublet column with a period-7 key, lag 21 makes the width-21 repeats), and 0002 tested ciphertext autokey only without an additional key. Construction: two-component key, ciphertext autokey at lag L plus a periodic key of period P: T[i] = s*A(c[i-L]) + k[i mod P], where T is the total key index (C - P for Vigenere, C + P for Beaufort; variant Beaufort is s = -1), A reads the earlier carved letter in the key alphabet. Because the carved text is fully known, the autokey part can be subtracted: d[i] = T[i] - s*A(c[i-L]) is a pure periodic key, so the 24 cribs give exact equations k[i mod P] = d[i] for every crib with i >= L. Sweep: L = 1..96, P = 1..96, plain, cipher and key alphabets standard or KRYPTOS, Vigenere or Beaufort, s = +1 or -1 (32 classes, 294,912 cases). A case survives if every slot's forced values agree and at least one check exists; survivors are tallied by the number of redundant checks and compared with ten shuffled coppers run through the same sweep. Forced key fragments of survivors are matched against the vocabulary and K1-K3 windows. Clue entries: C11a ('auto-key', 'interval 7'), C5(b) ('key word/s'), C6(c).

## Prediction

No case with a period of 26 or less survives with three or more redundant checks under any class, including lag 1 with period 7 (the doublet mechanism) and lag 21 at every period (the repeat mechanism). Survivor counts at each number of checks match the ten shuffled coppers within their range, and no forced fragment matches a word. Zero candidates pass.

## Method

1. For every lag, compute d[i] = total key minus the earlier carved letter's value at each known place past the lag.
2. For every period, group the known places by slot and check that each slot's values agree.
3. Tally consistent cases by the number of redundant checks.
4. Repeat on ten shuffled coppers.
5. Match the forced fragments of survivors against words.

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
 "family": "ciphertext autokey at lag L plus a periodic key of period P",
 "lags": "1-96",
 "periods": "1-96",
 "classes": 32,
 "cases": 221184,
 "controls": 10,
 "survivors_by_checks": {
  "P>26, checks 1": {
   "k4": 101,
   "controls": [
    85,
    90,
    79,
    84,
    105,
    91,
    98,
    84,
    100,
    100
   ]
  },
  "P>26, checks 2": {
   "k4": 5,
   "controls": [
    1,
    2,
    1,
    1,
    2,
    5,
    4,
    4,
    2,
    4
   ]
  },
  "P<=26, checks 1": {
   "k4": 91,
   "controls": [
    105,
    93,
    95,
    95,
    91,
    92,
    94,
    85,
    86,
    108
   ]
  },
  "P<=26, checks 2": {
   "k4": 5,
   "controls": [
    0,
    0,
    1,
    2,
    1,
    6,
    1,
    0,
    2,
    1
   ]
  },
  "P<=26, checks 3": {
   "k4": 0,
   "controls": [
    0,
    0,
    0,
    0,
    0,
    1,
    0,
    0,
    1,
    0
   ]
  }
 },
 "survivors_P_le_26_with_3plus_checks": [],
 "lag1_period7_or_lag21_survivors": [],
 "word_matches": []
}
```

Notes: 221184 cases, 32 classes. Survivors (K4 vs controls min-max): P>26, checks 1: 101 (79-105); P>26, checks 2: 5 (1-5); P<=26, checks 1: 91 (85-108); P<=26, checks 2: 5 (0-6); P<=26, checks 3: 0 (0-1). Lag 1 period 7 or lag 21 survivors: 0. Word matches: 0.


