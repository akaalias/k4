# 0058-tableau-then-keyed-columnar-k1-k3-words: The table first, then a column shuffle keyed by a word from the solved messages, once or twice

**Family:** 6-transposition-then-tableau  
**Parent:** 0007-tableau-then-columnar-period-survival  
**Decision:** reverted  
**Run:** 2026-10-15T12:19:40+00:00, 276.7 s, status ran  
**Time by phase:** design 0 s, implement 11 s, test 0 s, run 277 s, record 0 s

## In plain words

One recipe Sanborn hinted at uses the table and a shuffle of the letters by columns, the order of the columns set by a word. Experiment 7 tried the puzzle's own words for that order. Here the order comes from every word of the solved messages and Sanborn's 2025 letter, and the shuffle is done once or twice in a row. For each shuffle we check whether a repeating secret word on the table could still put the 24 known letters where they are.

## Walkthrough, by hand

1. Take the K2 word MAGNETIC: its letters in alphabetical order number the columns A=1, C=2, E=3, G=4, I=5, M=6, N=7, T=8, so the column order is 6, 1, 4, 7, 3, 8, 5,
2. 2. Write the 97 places in rows of 8 and read the columns in that order: column 2 (places 2, 10, 18, ...) comes first.
3. Each known letter is carried to a new place by this reading.
4. Under one way of using the table each known letter and the carved letter at its new place force one key letter.
5. Two known letters a secret word's length apart must force the same key letter; one clash kills that length.

## Worked example (generated)

```
route: keyed columnar MAGNETIC, applied after the tableau; convention kry/kry/kry Vigenere

plain pos  letter  its cipher sits at  cipher letter  forced key letter  key slot at period 13
       22    E            3              K              I                  8
       23    A           40              S              Z                  9
       24    S           64              N              G                 10
       25    T           16              L              G                 11
       64    B           69              T              V                 11
       65    E           21              W              F                 12
       66    R           94              K              Z                  0
       67    L           58              A              J                  1

```

## Lineage

Inherits from 0007-tableau-then-columnar-period-survival. What changed: Experiment 7 put the column shuffle after the table and keyed it with the puzzle's vocabulary, single, and with plain widths for the double shuffle. Here the shuffle is keyed by every word of the three solved messages and of Sanborn's 2025 letter, singly and as keyed double shuffles with two such words.

## Hypothesis (domain expert)

Periodic tableau (separate alphabets, 24 conventions) followed by keyed columnar transposition, single or double (C1, Sanborn 2005: 'double matrixes and triple matrixes... then went back to this table'; here the table first, 0007's order). Column orders from the numeric order of every K1-K3 plaintext word of length 3-20 and of the C13/C14 words, forward and inverse, and every ordered pair of distinct such words as a keyed double columnar, forward and inverse. For each route the inverse transposition maps each crib to a carved letter; each convention forces 24 key letters; a period is dead when two cribs it puts in one slot force different letters (divisor rule on plaintext distances). Live periods up to 30 are matched against the vocabulary and K1-K3 windows. Bounds: complete for these routes, conventions and periods.

## Prediction

No route makes a period below 26 live; the smallest live period is 26 or 27 everywhere, and no forced fragment matches a word. Zero candidates.

## Method

1. Build the column orders from the word pool.
2. For each route, find where each known letter lands.
3. For each convention, force the 24 key letters and kill periods by the divisor rule.
4. Record the smallest live period.
5. Match live periods up to 30 against words and K1-K3 windows; decrypt and submit matches.

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
 "family": "periodic tableau (separate alphabets) then keyed columnar transposition, single or double, keys from K1-K3 and C13/C14 words",
 "routes": 14792,
 "route_convention_pairs_checked": 355008,
 "route_set": "keyed columnar from K1-K3 words (3-20 letters) and C13/C14 words x {fwd, inv}; keyed double columnar over ordered pairs of distinct such orders x {fwd, inv}",
 "conventions": 24,
 "periods": "1-97 by divisor rule on plaintext positions",
 "key_pool": "vocabulary words and K1-K3 windows of length P for live P <= 30",
 "min_live_period_histogram": {
  "25": 16,
  "26": 14352,
  "27": 340640
 },
 "fifteen_shortest": [
  {
   "min_period": 25,
   "route": "keyed double DESPARATLY then REMAINS inv",
   "convention": "std/std/std/beau"
  },
  {
   "min_period": 25,
   "route": "keyed double DESPARATLY then REMAINS inv",
   "convention": "std/std/kry/beau"
  },
  {
   "min_period": 25,
   "route": "keyed double INFORMATION then ENCUMBERED inv",
   "convention": "std/kry/std/vig"
  },
  {
   "min_period": 25,
   "route": "keyed double INFORMATION then ENCUMBERED inv",
   "convention": "std/kry/std/varbeau"
  },
  {
   "min_period": 25,
   "route": "keyed double INFORMATION then ENCUMBERED inv",
   "convention": "std/kry/kry/vig"
  },
  {
   "min_period": 25,
   "route": "keyed double INFORMATION then ENCUMBERED inv",
   "convention": "std/kry/kry/varbeau"
  },
  {
   "min_period": 25,
   "route": "keyed double LANGLEY then WITH inv",
   "convention": "std/kry/std/beau"
  },
  {
   "min_period": 25,
   "route": "keyed double LANGLEY then WITH inv",
   "convention": "std/kry/kry/beau"
  },
  {
   "min_period": 25,
   "route": "keyed double REMAINS then NORTH inv",
   "convention": "std/std/std/beau"
  },
  {
   "min_period": 25,
   "route": "keyed double REMAINS then NORTH inv",
   "convention": "std/std/kry/beau"
  },
  {
   "min_period": 25,
   "route": "keyed double SEE then FLICKER fwd",
   "convention": "kry/kry/std/beau"
  },
  {
   "min_period": 25,
   "route": "keyed double SEE then FLICKER fwd",
   "convention": "kry/kry/kry/beau"
  },
  {
   "min_period": 25,
   "route": "keyed double SOMEWHERE then TRANSMIT fwd",
   "convention": "kry/std/std/vig"
  },
  {
   "min_period": 25,
   "route": "keyed double SOMEWHERE then TRANSMIT fwd",
   "convention": "kry/std/std/varbeau"
  },
  {
   "min_period": 25,
   "route": "keyed double SOMEWHERE then TRANSMIT fwd",
   "convention": "kry/std/kry/vig"
  }
 ],
 "vocab_matches": 0
}
```

Notes: 355008 route/convention pairs; 0 forced-fragment matches submitted.


