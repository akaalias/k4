# 0050-copper-off-by-one-two-words-mixed-alphabets: The copper off by one letter, through the two-word test on tables rebuilt from the puzzle's words

**Family:** 3-two-component-key  
**Parent:** 0043-two-keywords-two-passes-mixed-alphabets  
**Decision:** reverted  
**Run:** 2026-10-15T12:00:38+00:00, 288.1 s, status ran  
**Time by phase:** test 0 s, run 288 s, record 0 s

## In plain words

The second message on the sculpture has a carving mistake, so the fourth might too: one letter missing or one letter too many. That would throw off every test that counts positions. Experiment 31 tried every such slip on the sculpture's own table; experiment 43 tried two secret words on tables rebuilt from the puzzle's words but with the copper taken as exact. Here both are allowed at once. A scrambled copy of the copper gets the same treatment so we know what luck alone produces.

## Walkthrough, by hand

1. Suppose the carved letter at place 41 is spurious: delete it, so the copper letter under plaintext place 64 (B of BERLIN) is now the one carved at 65.
2. Rebuild the message alphabet from PALIMPSEST and the carved alphabet from ABSCISSA.
3. Lengths 7 and 8, Vigenere both passes: place 22 still needs the total that sends E to F, 5; place 64 now needs the total that sends B to the letter carved at 65.
4. Slots: place 22 uses slot 0 of the 7-word and slot 5 of the 8-word; place 29 uses slots 0 and 4; subtract and y5 - y4 is fixed.
5. Walk all 24 places; one loop that fails to close kills this variant, pair of lengths and pair of alphabets.
6. Do the same for every deletion, every insertion, every alphabet pair and every pair of lengths.

## Worked example (generated)

```
variant: the carved letter at 41 deleted
plain PALIMSETBCDFGHJKNOQRUVWXYZ
cipher ABSCIDEFGHJKLMNOPQRTUVWXYZ

lengths 7 and 8, Vigenere: totals and slots

pos  plain  carved  total  x slot  y slot
 22    E      F       1      0       5
 23    A      L      11      1       6
 29    T      R      11      0       4
 30    H      N       1      1       5
 64    B      Y      16      0       7
 65    E      P      10      1       0

places 64 and later now read the letter carved one place further along
```

## Lineage

Inherits from 0043-two-keywords-two-passes-mixed-alphabets. What changed: Experiment 43 ran the exact two-word test on the carved text under 63 x 63 vocabulary alphabets and found nothing below a total length of 22. Experiment 31 ran the same test with one carved letter deleted or one unknown inserted anywhere, but only under the standard and KRYPTOS orders. Here the two parameters are combined: every one-letter variant of the copper, every vocabulary alphabet pair, total length up to 22, with a shuffled copper run through the same sweep as the control.

## Hypothesis (domain expert)

K2 carries a known carving error (C14), so the K4 copper may be off by one letter, which shifts every later crib against a periodic key. The two-word composition t[i] = x[i mod a] + s y[i mod b] mod 26 (0014) is exact: 24 crib equations in a + b - 1 unknowns, so each (a, b) has 25 - a - b redundant checks at 1/26 each. Variants: the carved text, a letter deleted at each of 97 places, an unknown inserted before each of 98 places; variants that touch no crib collapse to the carved case, leaving about 50 distinct crib tuples, since every slip before the first crib shifts the cribs the same way. Under 63 x 63 keyword-mixed plain and cipher alphabets, both modes, both signs, length pairs with a < b, a + b <= 22 and lcm outside the dead periods: about 22 million union-find cases. Chance survival at a + b = 22 is 26^-3 per case, so a couple of hundred chance survivors at 22, a handful at 21, at most one at 20 and none below. A shuffled copper through the same sweep gives the control counts. Survivors with at most three free components are enumerated and their words matched against the vocabulary and K1-K3 windows. Bounds: complete for one error anywhere, these alphabets and these lengths.

## Prediction

No variant survives with a + b at or below 19 under any alphabet pair. Survivors at 20 to 22 appear in the same numbers on the copper and on its shuffle, and none yields a word from the vocabulary or K1-K3. Zero candidates pass.

## Method

1. Build the variants and group them by the crib tuple they produce.
2. Build the alphabet pool.
3. For each distinct crib tuple, alphabet pair, mode, length pair and sign, add the crib equations to a weighted union-find; reject on contradiction.
4. Count survivors by a + b and by variant.
5. Enumerate survivors with at most three components and match the words.
6. Repeat on a shuffled copper with the same variants as the control.

## Result

Candidates returned: 2. Passed all gates: 0. Best crib hits among all candidates: 23/24
(EAST 3/4, NORTHEAST 9/9, BERLIN 6/6, CLOCK 5/5).
Best loss: None (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: 0034-complete-the-key-at-surviving-periods.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | length | 23/24 |  | `DRQUVOBEZACOPNWITCXML?ASTNORTHEASTJZYUNCMFTTTJGEGOEBNVCVJJQTJZSBERLINCLOCKNPAJSEMJYIDOCQTZQHJXPLUM` | X=MTHEM Y=HZXHHLEZYAKTHBYWA (5,17) plain INTERPRETATION/keyword cipher TUTANKHAMUN/keyword vig s=1; copper inserted before 22 |
| 2 | length | 23/24 |  | `DRQUVOBEZACOPNWITCXML?ASTNORTHEASTJZYUNCMFTTTJGEGOEBNVCVJJQTJZSBERLINCLOCKNPAJSEMJYIDOCQTZQHJXPLUM` | X=MTHEM Y=FRYFFCIRXNKVFMXPN (5,17) plain INTERPRETATION/keyword cipher TUTANKHAMUN/keyword vig s=-1; copper inserted before 22 |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "one-letter error (insert or delete anywhere) x two words a + b <= 22 x keyword-mixed alphabet pairs",
 "variants": 196,
 "distinct_crib_tuples": 48,
 "alphabets": 63,
 "length_pairs": 29,
 "cases": 22099392,
 "stopped_early": false,
 "survivors": 914,
 "survivors_by_a_plus_b": {
  "21": 64,
  "22": 850
 },
 "smallest_surviving_sum": 21,
 "smallest_survivors": [
  {
   "sum": 21,
   "a": 8,
   "b": 13,
   "plain": "POSITION/keyword",
   "cipher": "POSITION/keyword",
   "mode": "vig",
   "s": 1,
   "components": 1,
   "cribs": 23,
   "variant": "inserted before 22"
  },
  {
   "sum": 21,
   "a": 8,
   "b": 13,
   "plain": "POSITION/keyword",
   "cipher": "POSITION/keyword",
   "mode": "vig",
   "s": -1,
   "components": 1,
   "cribs": 23,
   "variant": "inserted before 22"
  },
  {
   "sum": 21,
   "a": 8,
   "b": 13,
   "plain": "SCHEIDT/keyword",
   "cipher": "BERLIN/keyword",
   "mode": "vig",
   "s": 1,
   "components": 1,
   "cribs": 23,
   "variant": "inserted before 22"
  },
  {
   "sum": 21,
   "a": 8,
   "b": 13,
   "plain": "SCHEIDT/keyword",
   "cipher": "BERLIN/keyword",
   "mode": "vig",
   "s": -1,
   "components": 1,
   "cribs": 23,
   "variant": "inserted before 22"
  },
  {
   "sum": 21,
   "a": 5,
   "b": 16,
   "plain": "MYSTERY/keyword",
   "cipher": "DIGITAL/keyword",
   "mode": "beau",
   "s": 1,
   "components": 1,
   "cribs": 23,
   "variant": "inserted before 24"
  },
  {
   "sum": 21,
   "a": 5,
   "b": 16,
   "plain": "MYSTERY/keyword",
   "cipher": "DIGITAL/keyword",
   "mode": "beau",
   "s": -1,
   "components": 1,
   "cribs": 23,
   "variant": "inserted before 24"
  },
  {
   "sum": 21,
   "a": 5,
   "b": 16,
   "plain": "EAST/keyword",
   "cipher": "DESPARATLY/keyword",
   "mode": "vig",
   "s": 1,
   "components": 1,
   "cribs": 23,
   "variant": "inserted before 25"
  },
  {
   "sum": 21,
   "a": 5,
   "b": 16,
   "plain": "EAST/keyword",
   "cipher": "DESPARATLY/keyword",
   "mode": "vig",
   "s": -1,
   "components": 1,
   "cribs": 23,
   "variant": "inserted before 25"
  },
  {
   "sum": 21,
   "a": 8,
   "b": 13,
   "plain": "WEBSTER/keyword",
   "cipher": "CARNARVON/keyword",
   "mode": "beau",
   "s": 1,
   "components": 1,
   "cribs": 23,
   "variant": "inserted before 26"
  },
  {
   "sum": 21,
   "a": 8,
   "b": 13,
   "plain": "WEBSTER/keyword",
   "cipher": "CARNARVON/keyword",
   "mode": "beau",
   "s": -1,
   "components": 1,
   "cribs": 23,
   "variant": "inserted before 26"
  },
  {
   "sum": 21,
   "a": 5,
   "b": 16,
   "plain": "MAGNETIC/keyword",
   "cipher": "std",
   "mode": "vig",
   "s": 1,
   "components": 1,
   "cribs": 23,
   "variant": "inserted before 26"
  },
  {
   "sum": 21,
   "a": 5,
   "b": 16,
   "plain": "MAGNETIC/keyword",
   "cipher": "std",
   "mode": "vig",
   "s": -1,
   "components": 1,
   "cribs": 23,
   "variant": "inserted before 26"
  }
 ],
 "control": {
  "cases": 22559796,
  "stopped_early": false,
  "survivors": 878,
  "survivors_by_a_plus_b": {
   "20": 4,
   "21": 50,
   "22": 824
  },
  "smallest_surviving_sum": 20
 },
 "vocab_matches": 2
}
```

Notes: 48 distinct crib tuples from 196 variants; 22099392 cases; 914 consistent, by sum {21: 64, 22: 850}; shuffled copper: 22559796 cases, 878 consistent, by sum {20: 4, 21: 50, 22: 824}; 2 word matches.


