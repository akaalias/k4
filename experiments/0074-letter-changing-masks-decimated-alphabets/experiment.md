# 0074-letter-changing-masks-decimated-alphabets: A mask that changes letters: the alphabet counted in steps of 3, 5, 7 ... or backwards, before the table

**Family:** 2-masked-then-keyed  
**Parent:** 0057-letter-nulls-outside-the-cribs  
**Decision:** reverted  
**Run:** 2026-10-15T13:27:32+00:00, 18.0 s, status ran  
**Time by phase:** design 36 s, implement 0 s, test 10 s, run 18 s, record 0 s

## In plain words

Scheidt said he 'masked' the English before the main step. A mask that changes letters could be as simple as replacing every letter by the one three, five or seven places further along the alphabet, counting round, or reading the alphabet backwards. Every such mask amounts to a reshuffled alphabet, so we try all of them, on the ordinary alphabet and on the sculpture's, in front of a repeating secret word and in front of the self-feeding autokey, and compare with scrambled coppers.

## Walkthrough, by hand

1. Mask: read the ordinary alphabet backwards from A, AZYXWVUTSRQPONMLKJIHGFEDCB, so the message letter is counted on it.
2. Carved letters on the ordinary alphabet, Vigenere, a 7-letter word.
3. Place 22: known E is 22nd on the backwards alphabet (from A = 0), carved F is 5; key 5 - 22 = -17, which is 9, J, slot 0.
4. Place 29: known T is 7, carved R is 17; key 10, K, slot 0.
5. J and K disagree: dead.
6. Repeat for every step size, base alphabet, pairing, period and lag.

## Worked example (generated)

```
message on AZYXWVUTSRQPONMLKJIHGFEDCB, carved letters on the ordinary alphabet, Vigenere, 7-letter key

place  known  carved  key  slot
   22      E       F    J     0
   29      T       R    K     0
   23      A       L    L     1
   30      H       N    U     1
```

## Lineage

Inherits from 0057-letter-nulls-outside-the-cribs. What changed: Experiments 23 and 57 tried masks that only move or pad letters. Scheidt said he masked the English before the keyed step. The simplest masks that change letters replace each letter by the one a fixed number of steps along the alphabet (or backwards, like Atbash). Here every such mask, on the standard and the sculpture's alphabet, is put in front of a repeating key and in front of the self-feeding autokey.

## Hypothesis (domain expert)

Family 2, masks that change letters (C4(a): Scheidt 'I masked the English language... more than one stage', sources/kryptos-workshop-2015-scheidt-transcript.txt, npr-2005-scheidt-sanborn.txt). The simplest letter-changing masks are affine maps i -> a*i + b on a base alphabet (standard or KRYPTOS), a a unit mod 26 other than 1 (11 values; a = 25 with b = 25 is Atbash on the standard alphabet). Put before a tableau step, an affine mask is a decimated plain alphabet, and b is absorbed by the key, so the 22 decimated alphabets cover every affine mask. Pairings: decimated plain with standard, KRYPTOS or the same decimated cipher alphabet, and standard or KRYPTOS plain with a decimated cipher alphabet (mask after the table), Vigenere or Beaufort. Systems: (1) periodic key, periods 1-52; (2) ciphertext autokey with a constant, every lag, key letter on the plain, cipher, standard or KRYPTOS alphabet; (3) autokey plus a periodic key up to 26. Fragments at periods up to 29 matched against words. Ten shuffled coppers. Clue entries: C4(a), C4(b).

## Prediction

No pairing makes a periodic key of period 24 or less consistent; 25-26 at the shuffled-copper rate; no fragment matches a word; neither autokey form has a survivor with three or more checks beyond the controls. Zero candidates pass.

## Method

1. Build the 22 decimated alphabets.
2. For each pairing and mode, compute the key each known letter forces; check every period up to 52 and keep fragments.
3. Check the autokey residuals for every lag, alone and with a periodic key up to 26.
4. Repeat on ten shuffled coppers.
5. Match fragments against words.

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
 "family": "affine (decimated-alphabet) masks before a periodic key, ciphertext autokey, or both",
 "decimated_alphabets": 22,
 "pairings": 110,
 "periods": "1-52",
 "periodic_consistent_by_period": {
  "26": {
   "k4": 8,
   "controls": [
    8,
    8,
    8,
    8,
    8,
    8,
    8,
    8,
    0,
    8
   ]
  },
  "27": {
   "k4": 220,
   "controls": [
    220,
    220,
    220,
    220,
    220,
    220,
    220,
    220,
    220,
    220
   ]
  },
  "28": {
   "k4": 220,
   "controls": [
    220,
    220,
    220,
    220,
    220,
    220,
    220,
    220,
    220,
    220
   ]
  },
  "29": {
   "k4": 220,
   "controls": [
    220,
    220,
    220,
    220,
    220,
    220,
    220,
    220,
    220,
    220
   ]
  },
  "30": {
   "k4": 0,
   "controls": [
    0,
    6,
    8,
    16,
    23,
    8,
    8,
    8,
    17,
    0
   ]
  },
  "31": {
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
    0,
    4
   ]
  },
  "51": {
   "k4": 0,
   "controls": [
    0,
    4,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
   ]
  },
  "52": {
   "k4": 8,
   "controls": [
    8,
    8,
    8,
    8,
    8,
    8,
    8,
    8,
    0,
    8
   ]
  }
 },
 "autokey_constant_by_checks": {
  "1": {
   "k4": 79,
   "controls": [
    50,
    46,
    50,
    56,
    33,
    52,
    47,
    48,
    52,
    52
   ]
  },
  "2": {
   "k4": 2,
   "controls": [
    2,
    4,
    0,
    0,
    2,
    5,
    4,
    4,
    2,
    0
   ]
  }
 },
 "autokey_plus_periodic_by_checks": {
  "1": {
   "k4": 3682,
   "controls": [
    3937,
    4152,
    3998,
    3723,
    3844,
    4046,
    3754,
    3845,
    3823,
    3795
   ]
  },
  "2": {
   "k4": 128,
   "controls": [
    92,
    74,
    151,
    88,
    92,
    109,
    104,
    41,
    121,
    80
   ]
  },
  "3": {
   "k4": 0,
   "controls": [
    4,
    6,
    2,
    4,
    16,
    2,
    4,
    8,
    6,
    6
   ]
  },
  "4": {
   "k4": 0,
   "controls": [
    2,
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
 "fragments": 668,
 "word_matches": []
}
```

Notes: 22 decimated alphabets, 110 pairings. Periodic at P <= 26 (K4, control min, max): {'26': (8, 0, 8)}. Autokey: {'1': (79, 33, 56), '2': (2, 0, 5)}. Autokey plus periodic: {'1': (3682, 3723, 4152), '2': (128, 41, 151), '3': (0, 2, 16), '4': (0, 0, 2)}. Word matches in 668 fragments: 0.


