# 0043-two-keywords-two-passes-mixed-alphabets: Two key words in two passes, on tables rebuilt from the puzzle's words

**Family:** 3-two-component-key  
**Parent:** 0014-two-keywords-two-passes-linear  
**Decision:** reverted  
**Run:** 2026-10-15T09:36:36+00:00, 5.3 s, status ran  
**Time by phase:** design 0 s, implement 60 s, test 11 s, run 5 s, record 0 s

## In plain words

Experiment 14 asked whether two short secret words, used one after the other on the sculpture's table, could explain the 24 known letters; none could. The table could have been built from a different word, which changes every sum, so we rebuild it from each word the puzzle knows and ask again. Because two words of total length up to 24 leave spare known letters to check against, every pair of lengths gets a yes or no.

## Walkthrough, by hand

1. Build the alphabet from PALIMPSEST for the message and from ABSCISSA for the carved letters.
2. Lengths 7 and 8, Vigenere both passes: position 22 needs a total key index that sends E, index 6 in the PALIMPSEST alphabet, to F, index 11 in the ABSCISSA alphabet: 5.
3. Position 22 uses slot 0 of the 7-letter word and slot 5 of the 8-letter word, so x0 + y5 = 5.
4. Position 29 uses slot 0 and slot 4: x0 + y4 equals its own total.
5. Subtracting fixes y5 - y4; walk all 24 positions and every loop must close.
6. A contradiction kills this pair of lengths for this pair of alphabets.

## Worked example (generated)

```
plain PALIMSETBCDFGHJKNOQRUVWXYZ
cipher ABSCIDEFGHJKLMNOPQRTUVWXYZ

lengths 7 and 8, Vigenere: totals and slots

pos  plain  carved  total  x slot  y slot
 22    E      F       1      0       5
 23    A      L      11      1       6
 29    T      R      11      0       4
 30    H      N       1      1       5
 64    B      N       6      0       7
```

## Lineage

Inherits from 0014-two-keywords-two-passes-linear. What changed: Experiment 14's exact linear test, with the plain and cipher alphabets drawn from the keyword mixings of every vocabulary word instead of the standard and KRYPTOS orders. Word lengths with a + b up to 24, where the 24 cribs leave at least one redundant check.

## Hypothesis (domain expert)

Two passes through the same tableau compose to t[i] = x[i mod a] + s y[i mod b] mod 26 (0014). Under keyword-mixed plain and cipher alphabets (C5, C29) the forced totals t change, so the weighted union-find test is rerun over 63 x 63 alphabet pairs, both plaintext signs, both s, and every length pair with a < b, a + b <= 24 and lcm outside the dead periods. With a + b - 1 effective unknowns and 24 equations, each case has 25 - a - b redundant checks at 1/26 each; chance survival per case is below 1/26 and the number of cases is about a million, so a few thousand chance survivors at a + b = 23 and 24 are expected and none below 20. Survivors are enumerated and X, Y matched against the vocabulary and K1-K3 windows under both key alphabets. Bounds: complete for these alphabets and lengths.

## Prediction

No length pair with a + b below 20 survives under any alphabet pair. Survivors at 20 to 24 appear at chance rates, and none yields a word from the vocabulary or K1-K3. Zero candidates pass.

## Method

1. Build the alphabet pool.
2. For each plain and cipher alphabet and plaintext sign, compute the forced total at each crib.
3. For each length pair and combiner sign, add the 24 difference constraints to a weighted union-find; reject on contradiction.
4. Count survivors by a + b.
5. Enumerate survivors with at most three components; match X and Y against the vocabulary and K1-K3 windows; decrypt and submit matches.

## Result

Candidates returned: 0. Passed all gates: 0. Best crib hits among all candidates: 0/24
(no candidates).
Best loss: None (0 is solved; 10 per missed crib letter). Best fitness: None. Champion before this run: 0034-complete-the-key-at-surviving-periods.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| - | no candidates | | | | |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "two periodic keys composed through two tableau passes, keyword-mixed alphabets",
 "alphabets": 63,
 "length_pairs": 42,
 "cases": 666792,
 "survivors": 770,
 "survivors_by_a_plus_b": {
  "22": 2,
  "23": 122,
  "24": 646
 },
 "smallest_surviving_sum": 22,
 "smallest_survivors": [
  {
   "a": 7,
   "b": 15,
   "plain": "SOUTH/keyword",
   "cipher": "WONDERFUL/keyword",
   "mode": "beau",
   "s": -1,
   "components": 1
  },
  {
   "a": 7,
   "b": 15,
   "plain": "SOUTH/keyword",
   "cipher": "WONDERFUL/keyword",
   "mode": "beau",
   "s": 1,
   "components": 1
  },
  {
   "a": 6,
   "b": 17,
   "plain": "ALEXANDERPLATZ/keyword",
   "cipher": "HOWARDCARTER/keyword",
   "mode": "beau",
   "s": -1,
   "components": 1
  },
  {
   "a": 6,
   "b": 17,
   "plain": "ALEXANDERPLATZ/keyword",
   "cipher": "HOWARDCARTER/keyword",
   "mode": "beau",
   "s": 1,
   "components": 1
  },
  {
   "a": 6,
   "b": 17,
   "plain": "BERLIN/keyword",
   "cipher": "SANBORN/keyword",
   "mode": "vig",
   "s": -1,
   "components": 1
  },
  {
   "a": 6,
   "b": 17,
   "plain": "BERLIN/keyword",
   "cipher": "SANBORN/keyword",
   "mode": "vig",
   "s": 1,
   "components": 1
  },
  {
   "a": 6,
   "b": 17,
   "plain": "BERLIN/keyword",
   "cipher": "UNDERGROUND/keyword",
   "mode": "beau",
   "s": -1,
   "components": 1
  },
  {
   "a": 6,
   "b": 17,
   "plain": "BERLIN/keyword",
   "cipher": "UNDERGROUND/keyword",
   "mode": "beau",
   "s": 1,
   "components": 1
  },
  {
   "a": 6,
   "b": 17,
   "plain": "BERLINCLOCK/keyword",
   "cipher": "DESPARATLY/keyword",
   "mode": "vig",
   "s": -1,
   "components": 1
  },
  {
   "a": 6,
   "b": 17,
   "plain": "BERLINCLOCK/keyword",
   "cipher": "DESPARATLY/keyword",
   "mode": "vig",
   "s": 1,
   "components": 1
  },
  {
   "a": 6,
   "b": 17,
   "plain": "BERLINCLOCK/keyword",
   "cipher": "DESPERATELY/keyword",
   "mode": "vig",
   "s": -1,
   "components": 1
  },
  {
   "a": 6,
   "b": 17,
   "plain": "BERLINCLOCK/keyword",
   "cipher": "DESPERATELY/keyword",
   "mode": "vig",
   "s": 1,
   "components": 1
  }
 ],
 "vocab_matches": 0
}
```

Notes: 666792 cases; 770 consistent; smallest surviving a + b 22; survivors by sum {22: 2, 23: 122, 24: 646}; 0 word matches.


