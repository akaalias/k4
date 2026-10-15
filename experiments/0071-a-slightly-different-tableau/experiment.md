# 0071-a-slightly-different-tableau: Sanborn's own table, slightly different from the carved one: every alphabet one step away from KRYPTOS

**Family:** 1-keyed-periodic  
**Parent:** 0005-quagmire-period-sweep-forced-keys  
**Decision:** reverted  
**Run:** 2026-10-15T13:19:53+00:00, 38.6 s, status ran  
**Time by phase:** design 35 s, implement 0 s, test 20 s, run 39 s, record 0 s

## In plain words

Sanborn has said that the table he enciphered with was slightly different from the one carved on the sculpture. If so, every test that used the carved alphabet exactly could have missed by a hair. We take the carved alphabet KRYPTOS-A-B-C... and make every version with two letters swapped or one letter moved, almost a thousand of them, and run the two simplest ciphers on each: a repeating secret word, and the autokey that feeds on earlier carved letters. Scrambled coppers get the same treatment.

## Walkthrough, by hand

1. Swap A and B in the carved alphabet: KRYPTOSBACDEFGHIJLMNQUVWXZ, counted from K = 0.
2. Use it for both the message and the carved letters, Vigenere, with a 7-letter secret word.
3. Place 22: known E is 11, carved F is 12; the key is 1, R, in slot 0.
4. Place 29, also slot 0: known T is 4, carved R is 1; the key is 1 - 4 = -3, which is 23, W.
5. R and W disagree, so this alphabet with a 7-letter word is dead.
6. Repeat for every variant, pairing, word length and lag.

## Worked example (generated)

```
alphabet KRYPTOSBACDEFGHIJLMNQUVWXZ (A and B swapped), message and carved letters both on it, Vigenere, 7-letter key

place  known  carved  key  slot
   22      E       F    R     0
   29      T       R    W     0
   23      A       L    C     1
   30      H       N    O     1
```

## Lineage

Inherits from 0005-quagmire-period-sweep-forced-keys. What changed: Sanborn said the table he worked from was slightly different from the one on the sculpture. Every earlier sweep used the carved KRYPTOS alphabet exactly or alphabets built from words. Here the alphabet is the carved one with two letters swapped or one letter moved, 925 variants, tested with a repeating secret word and with the self-feeding autokey.

## Hypothesis (domain expert)

Family 1 re-entered with a new key source, C27(c): the 2010 worksheets show a tableau 'slightly different from the one on Kryptos' (research_notes/sanborn_charts/SOURCES.md; 02-sanborn-said.md). Alphabets: the KRYPTOS alphabet with one transposition of two letters (325) or one letter moved to another place (650 moves, of which 50 repeat an adjacent swap, so 600 new), 925 variants V. Pairings: V as both plain and cipher alphabet (the tableau's header and rows from one alphabet), plain standard with cipher V, and plain V with cipher standard; Vigenere or Beaufort. Systems: (1) periodic key, periods 1-52, exact crib consistency; (2) ciphertext autokey with a constant shift, lags 1-96, key letter read on V or on the standard alphabet. Survivors of (1) at periods up to 29 have their forced fragments matched against the vocabulary and K1-K3 windows. Ten shuffled coppers through the same sweep. Clue entries: C27(c), C6(a), C8(a).

## Prediction

No variant makes a period of 24 or less consistent under any pairing and mode; periods 25-26 survive at the shuffled-copper rate; no fragment at periods up to 29 matches a word; the autokey has no survivor with three or more redundant checks. Zero candidates pass.

## Method

1. Build the 925 alphabets one step from KRYPTOS.
2. For each pairing and mode, compute the key value each known letter forces.
3. For each period up to 52, check the slots agree; record the survivors and their fragments.
4. For each lag, check the autokey residuals agree.
5. Repeat on ten shuffled coppers and compare counts.
6. Match fragments at periods up to 29 against words.

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
 "family": "periodic key and ciphertext autokey on alphabets one swap or one move from KRYPTOS",
 "variants": 925,
 "variants_done": 925,
 "setups_per_variant": 6,
 "periods": "1-52",
 "lags": "1-96",
 "periodic_consistent_by_period": {
  "26": {
   "k4": 21,
   "controls": [
    137,
    0,
    548,
    462,
    21,
    387,
    33,
    33,
    0,
    32
   ]
  },
  "27": {
   "k4": 5550,
   "controls": [
    5550,
    5550,
    5550,
    5550,
    5550,
    5550,
    5550,
    5550,
    5550,
    5550
   ]
  },
  "28": {
   "k4": 5550,
   "controls": [
    5550,
    5550,
    5550,
    5550,
    5550,
    5550,
    5550,
    5550,
    5550,
    5550
   ]
  },
  "29": {
   "k4": 5550,
   "controls": [
    5550,
    5550,
    5550,
    5550,
    5550,
    5550,
    5550,
    5550,
    5550,
    5550
   ]
  },
  "30": {
   "k4": 113,
   "controls": [
    38,
    52,
    710,
    496,
    32,
    38,
    0,
    161,
    34,
    38
   ]
  },
  "31": {
   "k4": 2,
   "controls": [
    1,
    0,
    0,
    0,
    1,
    0,
    3,
    0,
    3,
    2
   ]
  },
  "51": {
   "k4": 0,
   "controls": [
    0,
    0,
    13,
    3,
    0,
    1,
    3,
    3,
    0,
    0
   ]
  },
  "52": {
   "k4": 21,
   "controls": [
    137,
    0,
    548,
    462,
    21,
    387,
    33,
    33,
    0,
    32
   ]
  }
 },
 "autokey_survivors_by_checks": {
  "1": {
   "k4": 391,
   "controls": [
    838,
    361,
    80,
    142,
    284,
    492,
    92,
    336,
    84,
    38
   ]
  },
  "2": {
   "k4": 1,
   "controls": [
    4,
    11,
    3,
    0,
    4,
    4,
    4,
    292,
    1,
    2
   ]
  },
  "3": {
   "k4": 0,
   "controls": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    1,
    1,
    3
   ]
  },
  "4": {
   "k4": 0,
   "controls": [
    29,
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
 "fragments_checked": 16671,
 "word_matches": [],
 "controls_done": [
  925,
  925,
  925,
  925,
  925,
  925,
  925,
  925,
  925,
  925
 ]
}
```

Notes: 925 of 925 variants. Periodic, consistent cases at P <= 26: K4 {'26': 21}; controls {'26': (0, 548)}. Autokey survivors by checks: {'1': (391, 38, 838), '2': (1, 0, 292), '3': (0, 0, 3), '4': (0, 0, 29)}. Word matches in 16671 fragments: 0.


