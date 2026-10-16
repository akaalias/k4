# 0170-pencil-session-observations: F12.4: a pencil session: K4 written out at widths 7, 8, 13, 14, 21, 24 and 31, six patterns noted by eye, each then tested against 1,000 shuffles

**Family:** 12-steins-way  
**Parent:** 0168-k4-statistics-against-a-thousand-shuffles  
**Decision:** reverted  
**Run:** 2026-10-16T23:04:18+00:00, 0.2 s, status ran  
**Time by phase:** unattributed 152 s, run 0 s, record 0 s

## In plain words

We wrote the carved letters out in rows of different widths, as Stein did with pencil and paper, and noted what caught the eye: the letter K lining up in sevens, five S's crowded together, three U's two apart, letter pairs that repeat. Each is then checked against a thousand shufflings of the same letters; the eye finds patterns in random letters too.

## Walkthrough, by hand

1. Write K4 in rows of 7 and find the Ks: four sit in the fifth column, three in the fourth.
2. Write K4 in a line and mark letter pairs that occur twice: ten of them; measure the distances between the two copies.
3. Mark the S's: five fall between places 33 and 44. Mark the U's at 88, 90, 92.
4. Shuffle the 97 letters and count the same things; repeat a thousand times; a pattern is real only if no shuffle matches it.

## Worked example (generated)

```
K4 in rows of 7 (K in capitals, everything else lower case):

  o b K r u o x
  o g h u l b s
  o l i f b b w
  f l r v q q p
  r n g K s s o
  t w t q s j q
  s s e K z z w
  a t j K l u d
  i a w i n f b
  n y p v t t m
  z f p K w g d
  K z x t j c d
  i g K u h u a
  u e K c a r

K at places 3, 32, 46, 53, 74, 78, 87, 94
```

## Lineage

Inherits from 0168-k4-statistics-against-a-thousand-shuffles. What changed: F12.4. Stein: 'the process of discovery is often intuitive as well as analytic.' Before any search code, K4 was written out at the widths that matter with the known letters marked and looked at; these six patterns were noted and are tested here exactly as written, each against 1,000 letter-preserving shuffles: (1) the most copies of one letter in one column at width 7 (K: 4 of 8 at places 32, 46, 53, 74); (2) K, the commonest letter, in two adjacent width-7 columns (7 of 8: places 3, 32, 46, 53, 74, 87, 94); (3) the number of repeated bigrams (10: HU, SO, FB, GK, SS, QS, EK, KZ, TJ, DI); (4) how many of their spacings share the factor 4 (5 of 10: 20, 28, 32, 44, 48), Kasiski's test; (5) five of the six S's within 12 places (33-44: SSOTWTQSJQSS); (6) one letter three times at a fixed spacing of 2 or 3 (U at 88, 90, 92). An observation outside every shuffle becomes a new item.

## Hypothesis (domain expert)

Stein 1999 (knowledge/sources/stein-1999-cracking-the-courtyard-crypto.txt): looking before attacking; F12.2 (0168) measured the fixed battery. These six are by-eye findings, so their selection is post hoc: the multiple-comparison count is the number of patterns a reader could have noticed, larger than six; a pattern counts only if outside every shuffle. Statistic definitions are in the method and fixed before the run.

## Prediction

None of the six lies outside every shuffle (eye-found patterns in 97 letters are usually chance). Zero candidates.

## Method

1. Statistics: (1) max over letters and residues mod 7 of the letter's count in that residue; (2) for the commonest letter, its largest count in two adjacent residues mod 7, as a share; (3) repeated bigrams (occurrences beyond the first); (4) repeated-bigram spacings divisible by 4; (5) for each letter with at least 6 copies, the shortest window holding all but one (smaller is more clustered); (6) the most equal letters in an arithmetic run with step 2 or 3.
2. 1,000 shuffles (seed 1614); one-sided p in the direction observed.

## Result

Candidates returned: 0. Passed all gates: 0. Best crib hits among all candidates: 0/24
(no candidates).
Best loss: None (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| - | no candidates | | | | |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "observation: six by-eye patterns in K4 against 1,000 shuffles",
 "observations": [
  {
   "observation": "(1) most of one letter in one width-7 column",
   "k4": 4,
   "shuffles_min": 2,
   "shuffles_max": 5,
   "p_one_sided": 0.204,
   "outside_every_shuffle": false
  },
  {
   "observation": "(2) commonest letter's share in two adjacent width-7 columns",
   "k4": 0.875,
   "shuffles_min": 0.375,
   "shuffles_max": 0.875,
   "p_one_sided": 0.004,
   "outside_every_shuffle": false
  },
  {
   "observation": "(3) repeated bigrams",
   "k4": 10,
   "shuffles_min": 0,
   "shuffles_max": 14,
   "p_one_sided": 0.04,
   "outside_every_shuffle": false
  },
  {
   "observation": "(4) repeated-bigram spacings divisible by 4",
   "k4": 5,
   "shuffles_min": 0,
   "shuffles_max": 7,
   "p_one_sided": 0.021,
   "outside_every_shuffle": false
  },
  {
   "observation": "(5) shortest window holding all but one copy of a 6-copy letter",
   "k4": 12,
   "shuffles_min": 8,
   "shuffles_max": 68,
   "p_one_sided": 0.004,
   "outside_every_shuffle": false
  },
  {
   "observation": "(6) most equal letters at a fixed step of 2 or 3",
   "k4": 3,
   "shuffles_min": 1,
   "shuffles_max": 4,
   "p_one_sided": 0.198,
   "outside_every_shuffle": false
  }
 ],
 "outside_every_shuffle": [],
 "note": "selected by eye, so post hoc; only an observation outside every shuffle would become an item",
 "controls": "1000 letter-preserving shuffles (seed 1614)"
}
```

Notes: (1) most of one letter in one width-7 column: K4 4, p 0.204; (2) commonest letter's share in two adjacent width-7 columns: K4 0.875, p 0.004; (3) repeated bigrams: K4 10, p 0.04; (4) repeated-bigram spacings divisible by 4: K4 5, p 0.021; (5) shortest window holding all but one copy of a 6-copy letter: K4 12, p 0.004; (6) most equal letters at a fixed step of 2 or 3: K4 3, p 0.198


