# 0059-two-keywords-two-passes-k1-k3-word-alphabets: Two secret words in two passes, on tables rebuilt from the solved messages' words

**Family:** 3-two-component-key  
**Parent:** 0043-two-keywords-two-passes-mixed-alphabets  
**Decision:** reverted  
**Run:** 2026-10-15T12:25:26+00:00, 13.9 s, status ran  
**Time by phase:** design 0 s, implement 0 s, test 0 s, run 14 s, record 0 s

## In plain words

Two short secret words used one after the other on the table act like one longer secret word with a pattern. Experiment 43 asked whether any two words could explain the 24 known letters on tables rebuilt from the puzzle's word list, and none could below a combined length of 22. Here the tables come from every word of the solved messages instead, and the question is asked again for every pair of lengths that leaves spare known letters to check.

## Walkthrough, by hand

1. Build the message alphabet from SHADING and the carved alphabet from INVISIBLE.
2. Lengths 7 and 8, Vigenere both passes: place 22 needs a total key that sends E (9 in the first alphabet) to F (10 in the second): 1.
3. Place 22 uses slot 0 of the 7-letter word and slot 5 of the 8-letter word, so x0 + y5 = 1.
4. Place 29 uses slot 0 and slot 4: x0 + y4 equals its own total, so y5 - y4 is fixed.
5. Walk all 24 places; every loop must close.
6. One contradiction kills this pair of lengths for this pair of alphabets.

## Worked example (generated)

```
plain SHADINGBCEFJKLMOPQRTUVWXYZ
cipher INVSBLEACDFGHJKMOPQRTUWXYZ

lengths 7 and 8, Vigenere: totals and slots

pos  plain  carved  total  x slot  y slot
 22    E      F       1      0       5
 23    A      L       3      1       6
 29    T      R       0      0       4
 30    H      N       0      1       5
 64    B      N      20      0       7
```

## Lineage

Inherits from 0043-two-keywords-two-passes-mixed-alphabets. What changed: Experiment 43 ran the exact two-word test on tables rebuilt from the puzzle's vocabulary. Here the tables come from every word of the three solved messages and of Sanborn's 2025 letter, with the same lengths and the same exact test.

## Hypothesis (domain expert)

Two periodic keys composed through two tableau passes, t[i] = x[i mod a] + s y[i mod b] mod 26 (0014, Scheidt's combined keys, family 3), with plain and cipher alphabets keyword-mixed from the K1-K3 plaintext words and the C13/C14 words (102 alphabets with standard and KRYPTOS), both plaintext signs, both combiner signs, every length pair a < b with a + b <= 24 and lcm outside the dead periods. Weighted union-find over the 24 crib equations; a + b - 1 unknowns leave 25 - a - b redundant checks. Survivors with at most three free components are enumerated and their words matched against the vocabulary, the word pool and K1-K3 windows. Bounds: complete for these alphabets and lengths.

## Prediction

No length pair with a + b below 21 survives under any alphabet pair; survivors at 21-24 appear at chance rates, none spelling a known word. Zero candidates.

## Method

1. Build the alphabet pool.
2. For each plain and cipher alphabet and sign, compute the forced total at each crib.
3. For each length pair and combiner sign, add the 24 difference constraints to a weighted union-find; reject on contradiction.
4. Count survivors by a + b.
5. Enumerate survivors with at most three components and match words.

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
 "family": "two periodic keys composed through two tableau passes, alphabets from K1-K3 words and C13/C14 words",
 "alphabets": 102,
 "length_pairs": 42,
 "cases": 1747872,
 "survivors": 2042,
 "survivors_by_a_plus_b": {
  "21": 2,
  "22": 8,
  "23": 306,
  "24": 1726
 },
 "smallest_surviving_sum": 21,
 "smallest_survivors": [
  {
   "a": 10,
   "b": 11,
   "plain": "GATHERED/keyword",
   "cipher": "FORTY/keyword",
   "mode": "beau",
   "s": -1,
   "components": 1
  },
  {
   "a": 10,
   "b": 11,
   "plain": "GATHERED/keyword",
   "cipher": "FORTY/keyword",
   "mode": "beau",
   "s": 1,
   "components": 1
  },
  {
   "a": 5,
   "b": 17,
   "plain": "NUANCE/keyword",
   "cipher": "FOUR/keyword",
   "mode": "vig",
   "s": -1,
   "components": 1
  },
  {
   "a": 5,
   "b": 17,
   "plain": "NUANCE/keyword",
   "cipher": "FOUR/keyword",
   "mode": "vig",
   "s": 1,
   "components": 1
  },
  {
   "a": 5,
   "b": 17,
   "plain": "NUANCE/keyword",
   "cipher": "FROM/keyword",
   "mode": "vig",
   "s": -1,
   "components": 1
  },
  {
   "a": 5,
   "b": 17,
   "plain": "NUANCE/keyword",
   "cipher": "FROM/keyword",
   "mode": "vig",
   "s": 1,
   "components": 1
  },
  {
   "a": 7,
   "b": 15,
   "plain": "PEERED/keyword",
   "cipher": "HOT/keyword",
   "mode": "vig",
   "s": -1,
   "components": 1
  },
  {
   "a": 7,
   "b": 15,
   "plain": "PEERED/keyword",
   "cipher": "HOT/keyword",
   "mode": "vig",
   "s": 1,
   "components": 1
  },
  {
   "a": 7,
   "b": 15,
   "plain": "REMOVED/keyword",
   "cipher": "DOES/keyword",
   "mode": "vig",
   "s": -1,
   "components": 1
  },
  {
   "a": 7,
   "b": 15,
   "plain": "REMOVED/keyword",
   "cipher": "DOES/keyword",
   "mode": "vig",
   "s": 1,
   "components": 1
  },
  {
   "a": 5,
   "b": 18,
   "plain": "AND/keyword",
   "cipher": "MADE/keyword",
   "mode": "beau",
   "s": -1,
   "components": 2
  },
  {
   "a": 5,
   "b": 18,
   "plain": "AND/keyword",
   "cipher": "MADE/keyword",
   "mode": "beau",
   "s": 1,
   "components": 2
  }
 ],
 "vocab_matches": 0
}
```

Notes: 1747872 cases; 2042 consistent; smallest surviving a + b 21; survivors by sum {21: 2, 22: 8, 23: 306, 24: 1726}; 0 word matches.


