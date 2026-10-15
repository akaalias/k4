# 0024-keyword-plus-k2-coordinate-digits: A key word plus the K2 coordinates: the digits as a numeric second component added to a repeating word

**Family:** 3-two-component-key  
**Parent:** 0014-two-keywords-two-passes-linear  
**Decision:** reverted  
**Run:** 2026-10-15T06:41:38+00:00, 1.4 s, status ran  
**Time by phase:** design 4 s, implement 54 s, test 2 s, run 1 s, record 0 s

## In plain words

The second message ends with map coordinates. A natural trick is to add those digits to a secret word, letter by letter, so the key is a word plus a number. Because we know the number, the 24 known letters tell us the secret word's letters directly, and tell us several of them twice. If the two tellings disagree, that word length and that way of reading the number are out. We try every word length, every way of reading the coordinates as digits, and every starting point.

## Walkthrough, by hand

1. Read the coordinates as the digits 3 8 5 7 6 5 7 7 8 4 4 and repeat them under the message.
2. Position 22 is E against the carved F; under the sculpture's alphabet with Vigenere the total key letter is R, index 1.
3. The digit under position 22 at alignment 0 is the 22nd digit, 3; subtract it: index 24 is the word letter for slot 21 mod a.
4. With a 7-letter word that is slot 0.
5. Position 29 also uses slot 0: do the same there; the two values must agree.
6. Go through all 24 known letters; one disagreement kills this length and alignment.
7. A survivor's forced letters spell the word; see whether it is one the puzzle knows.

## Worked example (generated)

```
digits 38576577844 repeated under the message, alignment 0; KRYPTOS alphabet throughout, Vigenere; word length 7

pos  plain  carved  total key  index  digit  word index  slot
 22    E      F        B         1      4       23       0
 23    A      L        K        10      3        7       1
 24    S      R        V        21      8       13       2
 29    T      R        X        23      7       16       0
 30    H      N        F         5      7       24       1
 64    B      N        L        11      8        3       0

positions 22 and 29 share slot 0: their word indices must agree, or length 7 is dead at this alignment.
```

## Lineage

Inherits from 0014-two-keywords-two-passes-linear. What changed: The second component is no longer an unknown word but a known digit stream, the K2 coordinates in several readings, at every alignment and either sign. Only the first word is unknown, so every slot of it is forced and the test is exact.

## Hypothesis (domain expert)

Scheidt's two-component habit (C6) and the K2 coordinates 38 57 6.5 N, 77 8 44 W (C23 reading b): a word key x of length a and a digit key d of known length L combine as t[i] = x[i mod a] + s d[(i + o) mod L] mod 26, with s = +1 or -1 and alignment o. The forced total t at each crib follows from the convention as in 0014; subtracting the digit term leaves the word slot forced outright, so the 24 cribs test the word's a slots with 24 - a redundant checks. Digit readings: 3857657784, 38576577844, 385765778440, the minutes and seconds only 5765844 and 57658440, degrees only 3877, and each with the 6.5 as 65 or 6 and 5. Word lengths 2-30, plain and cipher alphabets standard or KRYPTOS, both plaintext signs, both s, every o. Survivors have their forced word matched against the vocabulary and K1-K3 windows and scored as English with ten shuffled controls. Bounds: complete for these digit readings and alphabets.

## Prediction

No word length under 20 survives for any digit reading, alignment or sign. Survivors from length 20 up are chance and their forced words are noise against the shuffled controls. Zero candidates pass.

## Method

1. List the digit readings.
2. For each alphabet pair and plaintext sign, compute the forced total key index at each crib.
3. For each reading, alignment, sign s and word length a, subtract the digit term and reduce to the word slot; reject on any disagreement.
4. For survivors, read the word in the standard and KRYPTOS alphabets, match it against the vocabulary and K1-K3 windows, and score it as English.
5. Repeat the scoring on ten shuffles of K4.

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
 "family": "word key plus known digit key (K2 coordinates), additive",
 "digit_readings": {
  "38 57 6 5 77 8 44": "3857657784",
  "38 57 65 77 8 44": "38576577844",
  "38 57 65 77 8 44 0": "385765778440",
  "57 6 5 8 44 (minutes, seconds)": "5765844",
  "57 65 8 44 0": "57658440",
  "38 77 (degrees)": "3877",
  "38576577844 reversed": "44877567583"
 },
 "word_lengths": "2-30",
 "alphabets": "plain and cipher in {std, kry}; word read in std or kry",
 "cases": 29232,
 "survivors_by_word_length": {
  "26": 40,
  "27": 1008,
  "28": 1008,
  "29": 1008,
  "30": 33
 },
 "shortest_surviving_word_length": 26,
 "best_forced_words": [
  {
   "score": -5.584,
   "length": 29,
   "reading": "38 57 65 77 8 44 0",
   "offset": 9,
   "s": -1,
   "plain": "kry",
   "cipher": "std",
   "mode": "vig",
   "word_alphabet": "kry",
   "word": "TYCLUBUNEDODIBDH.....RENURELU"
  },
  {
   "score": -5.655,
   "length": 28,
   "reading": "38 57 65 77 8 44 0",
   "offset": 9,
   "s": -1,
   "plain": "kry",
   "cipher": "std",
   "mode": "vig",
   "word_alphabet": "kry",
   "word": "UTYCLU.BUNEDODIBDH...RENUREL"
  },
  {
   "score": -5.792,
   "length": 27,
   "reading": "38 57 65 77 8 44",
   "offset": 2,
   "s": -1,
   "plain": "std",
   "cipher": "std",
   "mode": "beau",
   "word_alphabet": "std",
   "word": "NSYONSQ..SFOLIMTRAZY.RQQUIL"
  },
  {
   "score": -5.815,
   "length": 27,
   "reading": "38 57 65 77 8 44 0",
   "offset": 9,
   "s": -1,
   "plain": "kry",
   "cipher": "std",
   "mode": "vig",
   "word_alphabet": "kry",
   "word": "LUTYCLU..BUNEDODIBDH.RENURE"
  },
  {
   "score": -5.943,
   "length": 28,
   "reading": "38 57 65 77 8 44",
   "offset": 2,
   "s": -1,
   "plain": "std",
   "cipher": "std",
   "mode": "beau",
   "word_alphabet": "std",
   "word": "SYONSQ.SFOLIMTRAZY...RQQUILN"
  },
  {
   "score": -6.026,
   "length": 27,
   "reading": "57 6 5 8 44 (minutes, seconds)",
   "offset": 1,
   "s": 1,
   "plain": "std",
   "cipher": "kry",
   "mode": "vig",
   "word_alphabet": "kry",
   "word": "ARSTMDC..EMAPMGEAMVB.RETUPY"
  },
  {
   "score": -6.131,
   "length": 28,
   "reading": "38 57 6 5 77 8 44",
   "offset": 2,
   "s": 1,
   "plain": "std",
   "cipher": "kry",
   "mode": "vig",
   "word_alphabet": "std",
   "word": "FEETII.NRFDSOIJRVL...BLEWAYI"
  },
  {
   "score": -6.15,
   "length": 28,
   "reading": "57 6 5 8 44 (minutes, seconds)",
   "offset": 1,
   "s": 1,
   "plain": "std",
   "cipher": "kry",
   "mode": "vig",
   "word_alphabet": "kry",
   "word": "RSTMDC.EMAPMGEAMVB...RETUPYA"
  },
  {
   "score": -6.151,
   "length": 27,
   "reading": "38 57 6 5 77 8 44",
   "offset": 2,
   "s": 1,
   "plain": "std",
   "cipher": "kry",
   "mode": "vig",
   "word_alphabet": "std",
   "word": "IFEETII..NRFDSOIJRVL.BLEWAY"
  },
  {
   "score": -6.154,
   "length": 27,
   "reading": "38576577844 reversed",
   "offset": 9,
   "s": 1,
   "plain": "kry",
   "cipher": "std",
   "mode": "beau",
   "word_alphabet": "kry",
   "word": "CHVEDNH..IYETOBLBPLO.EDQUOG"
  },
  {
   "score": -6.16,
   "length": 27,
   "reading": "38576577844 reversed",
   "offset": 1,
   "s": 1,
   "plain": "kry",
   "cipher": "std",
   "mode": "beau",
   "word_alphabet": "std",
   "word": "KOWJOUS..NGMIAFOLERF.MOPSCQ"
  },
  {
   "score": -6.165,
   "length": 27,
   "reading": "57 65 8 44 0",
   "offset": 2,
   "s": 1,
   "plain": "kry",
   "cipher": "kry",
   "mode": "beau",
   "word_alphabet": "kry",
   "word": "KRANKSO..QAZOINREDSU.WNKQBL"
  },
  {
   "score": -6.187,
   "length": 29,
   "reading": "57 6 5 8 44 (minutes, seconds)",
   "offset": 1,
   "s": 1,
   "plain": "std",
   "cipher": "kry",
   "mode": "vig",
   "word_alphabet": "kry",
   "word": "STMDCEMAPMGEAMVB.....RETUPYAR"
  },
  {
   "score": -6.195,
   "length": 28,
   "reading": "57 65 8 44 0",
   "offset": 7,
   "s": -1,
   "plain": "kry",
   "cipher": "std",
   "mode": "vig",
   "word_alphabet": "kry",
   "word": "MAZAFN.CGNEDOEFTSI...YBILYMQ"
  },
  {
   "score": -6.23,
   "length": 29,
   "reading": "38 57 6 5 77 8 44",
   "offset": 2,
   "s": 1,
   "plain": "std",
   "cipher": "kry",
   "mode": "vig",
   "word_alphabet": "std",
   "word": "EETIINRFDSOIJRVL.....BLEWAYIF"
  }
 ],
 "shuffled_control_best": [
  -6.039,
  -5.393,
  -5.708,
  -5.966,
  -5.808,
  -5.857,
  -5.878,
  -5.919,
  -5.845,
  -5.881
 ],
 "vocab_matches": 0
}
```

Notes: 29232 cases; shortest surviving word length 26; best forced word -5.584 vs shuffled best -5.393; 0 matches.


