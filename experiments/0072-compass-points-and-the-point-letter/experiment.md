# 0072-compass-points-and-the-point-letter: The 32 points of the compass and the words of Sanborn's last hint as alphabets

**Family:** 1-keyed-periodic  
**Parent:** 0053-periodic-tableau-k1-k3-word-alphabets  
**Decision:** reverted  
**Run:** 2026-10-15T13:22:40+00:00, 7.2 s, status ran  
**Time by phase:** design 56 s, implement 0 s, test 9 s, run 7 s, record 0 s

## In plain words

In his last open letter Sanborn wrote 'what's the point?' and marked it as a clue, and years earlier he said he used the word 'directions' on purpose. The known letters already say EAST NORTHEAST, which is one of the 32 points of a compass. We build the table's scrambled alphabets from all 32 point names and from the words of that letter, and try the simplest ciphers with them. Scrambled coppers get the same treatment, so we can tell a real fit from luck.

## Walkthrough, by hand

1. Build the alphabet from EASTNORTHEAST: EASTNORHBCDFGIJKLMPQUVWXYZ, counted from E = 0.
2. Use it for message and carved letters, Vigenere, with a 7-letter word.
3. Place 22: known E is 0, carved F is 11; key 11, F, in slot 0.
4. Place 29: known T is 3, carved R is 6; key 3, T, also slot 0.
5. F and T disagree, so this alphabet with a 7-letter word is dead.
6. Repeat for every pair, word length and lag.

## Worked example (generated)

```
alphabet EASTNORHBCDFGIJKLMPQUVWXYZ on both sides, Vigenere, 7-letter key

place  known  carved  key  slot
   22      E       F    F     0
   29      T       R    T     0
   23      A       L    K     1
   30      H       N    X     1
```

## Lineage

Inherits from 0053-periodic-tableau-k1-k3-word-alphabets. What changed: Sanborn's 2025 letter marks 'what's the point?' as a clue, and he chose the word 'directions' on purpose. The vocabulary held only the four cardinal points and NORTHEAST. Here the alphabets are rebuilt from all 32 compass points (EASTNORTHEAST, NORTHBYEAST and the rest) and from the hint's words (POINT, POWER, RESIDES, WITHOUT, DIRECTIONS, BEARING), and tested with a repeating key, the self-feeding autokey, and both together.

## Hypothesis (domain expert)

Family 1 re-entered with a new key source: C15(a) and (e) (open letter, sources/openletter-2025.txt: 'If they don't, then (CLUE) what's the point? Power resides with a secret, not without it') and C16 ('the word directions is, I use intentionally', 2010). EASTNORTHEAST is itself a compass point, so the boxing of the 32 points is a natural key source for a man who chose it as plaintext. Words: the 32 point names (NORTH, NORTHBYEAST, NORTHNORTHEAST, NORTHEASTBYNORTH, NORTHEAST, ... in the traditional boxing), SOUTHEAST, SOUTHWEST, NORTHWEST, POINT, POWER, RESIDES, WITHOUT, DIRECTION, DIRECTIONS, BEARING, TRUENORTH, ORIENTATION, OFFSET, COMPASSROSE, WINDROSE, AZIMUTH, DECLINATION; keyword-mixed alphabets, duplicates removed, plus standard and KRYPTOS. Systems: (1) periodic key, periods 1-52, every plain-cipher pair, Vigenere or Beaufort, exact crib consistency, fragments at periods up to 29 matched against the vocabulary and K1-K3; (2) ciphertext autokey with a constant shift, every lag, both alphabets the same word alphabet, key letter on it or on the standard; (3) the 0066 form, autokey plus a periodic key up to 26, same alphabets. Ten shuffled coppers through the same sweeps.

## Prediction

No pair makes a periodic key of period 24 or less consistent; 25-26 survive at the shuffled-copper rate; no fragment at periods up to 29 matches a word; neither autokey form has a survivor with three or more redundant checks beyond the controls. Zero candidates pass.

## Method

1. Build the alphabets from the compass and letter words.
2. For each pair and mode, compute the key value each known letter forces and check slot agreement at every period up to 52; keep fragments.
3. For each word alphabet, lag and key alphabet, check the autokey residuals, alone and with a periodic key up to 26.
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
 "family": "compass-point and C15 word alphabets: periodic key, ciphertext autokey, autokey plus periodic key",
 "alphabets": 42,
 "pairs": 1764,
 "periods": "1-52",
 "periodic_consistent_by_period": {
  "25": {
   "k4": 0,
   "controls": [
    0,
    2,
    0,
    0,
    0,
    0,
    0,
    0,
    2,
    0
   ]
  },
  "26": {
   "k4": 87,
   "controls": [
    164,
    393,
    224,
    308,
    163,
    140,
    17,
    79,
    275,
    61
   ]
  },
  "27": {
   "k4": 3528,
   "controls": [
    3528,
    3528,
    3528,
    3528,
    3528,
    3528,
    3528,
    3528,
    3528,
    3528
   ]
  },
  "28": {
   "k4": 3528,
   "controls": [
    3528,
    3528,
    3528,
    3528,
    3528,
    3528,
    3528,
    3528,
    3528,
    3528
   ]
  },
  "29": {
   "k4": 3528,
   "controls": [
    3528,
    3528,
    3528,
    3528,
    3528,
    3528,
    3528,
    3528,
    3528,
    3528
   ]
  },
  "30": {
   "k4": 125,
   "controls": [
    71,
    293,
    55,
    151,
    245,
    199,
    50,
    101,
    95,
    0
   ]
  },
  "31": {
   "k4": 5,
   "controls": [
    0,
    2,
    0,
    5,
    0,
    5,
    2,
    4,
    1,
    3
   ]
  },
  "32": {
   "k4": 2,
   "controls": [
    1,
    0,
    0,
    0,
    0,
    1,
    1,
    0,
    0,
    0
   ]
  },
  "50": {
   "k4": 0,
   "controls": [
    0,
    2,
    0,
    0,
    0,
    0,
    0,
    0,
    2,
    0
   ]
  },
  "51": {
   "k4": 0,
   "controls": [
    7,
    4,
    0,
    5,
    14,
    6,
    10,
    2,
    6,
    8
   ]
  },
  "52": {
   "k4": 87,
   "controls": [
    164,
    393,
    224,
    308,
    163,
    140,
    17,
    79,
    275,
    61
   ]
  }
 },
 "autokey_constant_by_checks": {
  "1": {
   "k4": 19,
   "controls": [
    19,
    8,
    7,
    16,
    8,
    18,
    15,
    10,
    16,
    8
   ]
  },
  "2": {
   "k4": 0,
   "controls": [
    0,
    1,
    0,
    0,
    0,
    0,
    1,
    0,
    1,
    0
   ]
  }
 },
 "autokey_plus_periodic_by_checks": {
  "1": {
   "k4": 998,
   "controls": [
    1079,
    967,
    1027,
    993,
    1008,
    852,
    1008,
    1057,
    1094,
    1011
   ]
  },
  "2": {
   "k4": 27,
   "controls": [
    25,
    23,
    33,
    30,
    20,
    28,
    15,
    24,
    29,
    32
   ]
  },
  "3": {
   "k4": 0,
   "controls": [
    5,
    1,
    5,
    1,
    0,
    0,
    0,
    0,
    0,
    0
   ]
  }
 },
 "fragments": 10671,
 "word_matches": []
}
```

Notes: 42 alphabets, 1764 pairs. Periodic consistent at P <= 26: {'25': (0, 0, 2), '26': (87, 17, 393)}. Autokey (checks: K4, control min, max): {'1': (19, 7, 19), '2': (0, 0, 1)}. Autokey plus periodic: {'1': (998, 852, 1094), '2': (27, 15, 33), '3': (0, 0, 5)}. Word matches in 10671 fragments: 0.


