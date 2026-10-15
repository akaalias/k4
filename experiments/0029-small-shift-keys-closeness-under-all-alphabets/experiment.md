# 0029-small-shift-keys-closeness-under-all-alphabets: Bean's closeness made a test: is there an alphabet pair under which every known letter moves only a little?

**Family:** 1-keyed-periodic  
**Parent:** 0028-gromark-small-bases-two-to-nine  
**Decision:** reverted  
**Run:** 2026-10-15T07:38:07+00:00, 8.9 s, status ran  
**Time by phase:** design 9 s, implement 44 s, test 0 s, run 9 s, record 0 s

## In plain words

A cryptanalyst noticed that several known letters barely move: S becomes R, T becomes V, K stays K. If the whole cipher only nudged letters a little along some alphabet, that alphabet would make every one of the 24 known moves small. We try every alphabet the puzzle's words can build, measure the biggest nudge each needs, and keep the alphabet with the smallest biggest nudge. Random letters tell us how small that can get by luck.

## Walkthrough, by hand

1. Take the plain alphabet for both message and carved letters, Vigenere.
2. Position 24 is S, carved R: R is one place before S, a nudge of 1.
3. Position 25 is T, carved V: a nudge of 2.
4. Position 23 is A, carved L: a nudge of 11, which is large.
5. Write down all 24 nudges and keep the biggest: 12 or more here.
6. Now rebuild the alphabet from a word, say PALIMPSEST, and measure again; the nudges change.
7. The alphabet with the smallest biggest nudge is the one to look at.

## Worked example (generated)

```
standard alphabet for both message and carved letters, Vigenere: nudge per known letter

pos  plain  carved  nudge
 22    E      F       1
 23    A      L      11
 24    S      R       1   (KRYPTOS letter)
 25    T      V       2   (KRYPTOS letter)
 26    N      Q       3
 27    O      Q       2   (KRYPTOS letter)
 28    R      P       2   (KRYPTOS letter)
 29    T      R       2   (KRYPTOS letter)
 30    H      N       6
 31    E      G       2
 32    A      K      10
 33    S      S       0   (KRYPTOS letter)
 34    T      S       1   (KRYPTOS letter)
 64    B      N      12
 65    E      Y       6
 66    R      P       2   (KRYPTOS letter)
 67    L      V      10
 68    I      T      11
 69    N      T       6
 70    C      M      10
 71    L      Z      12
 72    O      F       9   (KRYPTOS letter)
 73    C      P      13
 74    K      K       0   (KRYPTOS letter)
```

## Lineage

Inherits from 0028-gromark-small-bases-two-to-nine. What changed: The statistic is the size of the forced shift, not its recurrence. For every alphabet pair and mode the 24 forced shifts are reduced to circular magnitudes 0-13, and the pair with the smallest largest magnitude is the lead; ten shuffled controls say what chance gives.

## Hypothesis (domain expert)

Bean (knowledge/04-structure.md): the ten crib plaintext letters that lie in KRYPTOS sit within 0-2 places of their ciphertext letters on the standard alphabet, about one permutation in 5,520, and he reads K4 as letter-for-letter with a cipher alphabet near the standard one. A Gronsfeld-like key of small digits, or any system whose shifts are small under the right pair of alphabets, would show as a pair under which all 24 forced shifts have small circular magnitude. Over the 248-alphabet pool squared and three modes, 184,512 pairs, the chance that a pair keeps all 24 magnitudes at or below 3 is (7/26)^24, about 10^-14 per pair; at or below 6 it is (13/26)^24, about 6 x 10^-8 per pair, so a largest magnitude of 6 or less would be a lead and 3 or less decisive. Ten shuffles of K4 calibrate the smallest largest-magnitude. Bounds: complete for this pool; diagnostic, no candidate.

## Prediction

The smallest largest magnitude over all pairs is 9 or 10, the same as on shuffled K4. Under the standard-standard pair the KRYPTOS-letter cribs are close, as Bean found, but the other fourteen cribs are not, and no pair makes all 24 small.

## Method

1. Build the alphabet pool.
2. For each plain and cipher alphabet and mode, compute the 24 forced shifts and their circular magnitudes.
3. Record the largest magnitude per pair and keep the ten smallest, with the shift sequences.
4. Repeat on ten shuffles of K4.
5. Report Bean's own statistic, the magnitudes under the standard pair, for reference.

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
 "family": "small-shift keys under all alphabet pairs (Bean's closeness)",
 "alphabets": 248,
 "pairs_x_modes": 184512,
 "smallest_largest_magnitude": 8,
 "ten_best_pairs": [
  {
   "largest": 8,
   "mean": 3.71,
   "plain": "BERLIN/alt_vertical",
   "cipher": "LAYER/columnar",
   "mode": "beau",
   "shifts": [
    0,
    1,
    24,
    21,
    18,
    8,
    24,
    1,
    1,
    5,
    19,
    1,
    4,
    3,
    20,
    24,
    6,
    22,
    3,
    5,
    22,
    6,
    22,
    25
   ]
  },
  {
   "largest": 8,
   "mean": 4.25,
   "plain": "KRYPTOS/alt_vertical",
   "cipher": "INVISIBLE/alt_vertical",
   "mode": "vig",
   "shifts": [
    23,
    21,
    23,
    18,
    24,
    22,
    6,
    4,
    5,
    0,
    1,
    18,
    25,
    1,
    21,
    6,
    21,
    20,
    5,
    22,
    6,
    18,
    4,
    2
   ]
  },
  {
   "largest": 8,
   "mean": 4.25,
   "plain": "KRYPTOS/alt_vertical",
   "cipher": "INVISIBLE/alt_vertical",
   "mode": "varbeau",
   "shifts": [
    3,
    5,
    3,
    8,
    2,
    4,
    20,
    22,
    21,
    0,
    25,
    8,
    1,
    25,
    5,
    20,
    5,
    6,
    21,
    4,
    20,
    8,
    22,
    24
   ]
  },
  {
   "largest": 8,
   "mean": 4.79,
   "plain": "KRYPTOS/alt_vertical",
   "cipher": "BURIED/columnar",
   "mode": "beau",
   "shifts": [
    2,
    8,
    7,
    7,
    23,
    25,
    5,
    0,
    18,
    6,
    3,
    5,
    24,
    22,
    21,
    5,
    4,
    18,
    7,
    21,
    22,
    7,
    7,
    2
   ]
  },
  {
   "largest": 8,
   "mean": 4.83,
   "plain": "UNDERGROUND/keyword",
   "cipher": "COMPASS/alt_vertical",
   "mode": "beau",
   "shifts": [
    19,
    22,
    22,
    8,
    24,
    3,
    21,
    23,
    5,
    22,
    19,
    18,
    19,
    2,
    7,
    21,
    3,
    18,
    7,
    19,
    20,
    22,
    0,
    0
   ]
  },
  {
   "largest": 8,
   "mean": 4.88,
   "plain": "WEBSTER/alt_vertical",
   "cipher": "CARTER/keyed_columnar",
   "mode": "beau",
   "shifts": [
    0,
    24,
    7,
    22,
    21,
    1,
    18,
    8,
    6,
    5,
    19,
    5,
    6,
    18,
    24,
    18,
    19,
    23,
    18,
    21,
    25,
    20,
    1,
    4
   ]
  },
  {
   "largest": 9,
   "mean": 3.83,
   "plain": "ABSCISSA/columnar",
   "cipher": "NORTH/keyed_columnar",
   "mode": "vig",
   "shifts": [
    0,
    8,
    5,
    17,
    1,
    21,
    0,
    18,
    9,
    6,
    2,
    18,
    5,
    25,
    23,
    0,
    2,
    0,
    24,
    24,
    23,
    4,
    3,
    20
   ]
  },
  {
   "largest": 9,
   "mean": 3.83,
   "plain": "ABSCISSA/columnar",
   "cipher": "NORTH/keyed_columnar",
   "mode": "varbeau",
   "shifts": [
    0,
    18,
    21,
    9,
    25,
    5,
    0,
    8,
    17,
    20,
    24,
    8,
    21,
    1,
    3,
    0,
    24,
    0,
    2,
    2,
    3,
    22,
    23,
    6
   ]
  },
  {
   "largest": 9,
   "mean": 4.42,
   "plain": "KRYPTOS/columnar",
   "cipher": "INVISIBLE/alt_vertical",
   "mode": "vig",
   "shifts": [
    23,
    21,
    23,
    18,
    22,
    24,
    9,
    4,
    5,
    0,
    1,
    18,
    25,
    2,
    21,
    9,
    20,
    19,
    3,
    22,
    5,
    20,
    4,
    2
   ]
  },
  {
   "largest": 9,
   "mean": 4.42,
   "plain": "KRYPTOS/columnar",
   "cipher": "INVISIBLE/alt_vertical",
   "mode": "varbeau",
   "shifts": [
    3,
    5,
    3,
    8,
    4,
    2,
    17,
    22,
    21,
    0,
    25,
    8,
    1,
    24,
    5,
    17,
    6,
    7,
    23,
    4,
    21,
    6,
    22,
    24
   ]
  }
 ],
 "shuffled_k4_smallest_largest_magnitude": [
  8,
  7,
  8,
  8,
  8,
  8,
  8,
  9,
  8,
  8
 ],
 "bean_statistic_standard_pair": [
  {
   "pos": 22,
   "plain": "E",
   "cipher": "F",
   "magnitude": 1
  },
  {
   "pos": 23,
   "plain": "A",
   "cipher": "L",
   "magnitude": 11
  },
  {
   "pos": 24,
   "plain": "S",
   "cipher": "R",
   "magnitude": 1
  },
  {
   "pos": 25,
   "plain": "T",
   "cipher": "V",
   "magnitude": 2
  },
  {
   "pos": 26,
   "plain": "N",
   "cipher": "Q",
   "magnitude": 3
  },
  {
   "pos": 27,
   "plain": "O",
   "cipher": "Q",
   "magnitude": 2
  },
  {
   "pos": 28,
   "plain": "R",
   "cipher": "P",
   "magnitude": 2
  },
  {
   "pos": 29,
   "plain": "T",
   "cipher": "R",
   "magnitude": 2
  },
  {
   "pos": 30,
   "plain": "H",
   "cipher": "N",
   "magnitude": 6
  },
  {
   "pos": 31,
   "plain": "E",
   "cipher": "G",
   "magnitude": 2
  },
  {
   "pos": 32,
   "plain": "A",
   "cipher": "K",
   "magnitude": 10
  },
  {
   "pos": 33,
   "plain": "S",
   "cipher": "S",
   "magnitude": 0
  },
  {
   "pos": 34,
   "plain": "T",
   "cipher": "S",
   "magnitude": 1
  },
  {
   "pos": 64,
   "plain": "B",
   "cipher": "N",
   "magnitude": 12
  },
  {
   "pos": 65,
   "plain": "E",
   "cipher": "Y",
   "magnitude": 6
  },
  {
   "pos": 66,
   "plain": "R",
   "cipher": "P",
   "magnitude": 2
  },
  {
   "pos": 67,
   "plain": "L",
   "cipher": "V",
   "magnitude": 10
  },
  {
   "pos": 68,
   "plain": "I",
   "cipher": "T",
   "magnitude": 11
  },
  {
   "pos": 69,
   "plain": "N",
   "cipher": "T",
   "magnitude": 6
  },
  {
   "pos": 70,
   "plain": "C",
   "cipher": "M",
   "magnitude": 10
  },
  {
   "pos": 71,
   "plain": "L",
   "cipher": "Z",
   "magnitude": 12
  },
  {
   "pos": 72,
   "plain": "O",
   "cipher": "F",
   "magnitude": 9
  },
  {
   "pos": 73,
   "plain": "C",
   "cipher": "P",
   "magnitude": 13
  },
  {
   "pos": 74,
   "plain": "K",
   "cipher": "K",
   "magnitude": 0
  }
 ],
 "bean_kryptos_letters_sum": 21
}
```

Notes: Diagnostic, no candidates. Smallest largest magnitude over 184512 pairs: 8 (BERLIN/alt_vertical / LAYER/columnar beau); shuffled K4 gives [8, 7, 8, 8, 8, 8, 8, 9, 8, 8].


