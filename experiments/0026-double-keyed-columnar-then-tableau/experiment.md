# 0026-double-keyed-columnar-then-tableau: Two keyed columnar transpositions from the puzzle's words, then the tableau

**Family:** 6-transposition-then-tableau  
**Parent:** 0016-routes-then-tableau-forced-key-english  
**Decision:** reverted  
**Run:** 2026-10-15T07:30:27+00:00, 175.3 s, status ran  
**Time by phase:** design 0 s, implement 44 s, test 5 s, run 175 s, record 0 s

## In plain words

The artist said he sometimes scrambled the letters through two grids before using the table. The third message was scrambled through a grid whose columns were ordered by a key word. So we try two such grids in a row, each ordered by a word the puzzle knows, in every combination, and ask the usual question: where do the 24 known letters land, and could a short secret word on the table then produce the carved letters there?

## Walkthrough, by hand

1. Take the words KRYPTOS and ABSCISSA.
2. Write the message in rows of 7 under KRYPTOS, number the columns by alphabetical order of the letters (K=1, O=2, P=3, R=4, S=5, T=6, Y=7), and read the columns out in that order.
3. Write the result in rows of 8 under ABSCISSA and read it out the same way.
4. The E at position 22 of the message is now at some position j; the carved letter at j and E force a key letter on the sculpture's table.
5. Do this for all 24 known letters.
6. Two landing spots a multiple of p apart share a key letter at period p; a disagreement kills p.
7. For the periods that survive, write the forced letters into their slots and read them.

## Worked example (generated)

```
route: keyed columnar KRYPTOS then keyed columnar ABSCISSA; convention kry/kry/kry Vigenere

column order under KRYPTOS: [0, 3, 6, 2, 5, 1, 4]; under ABSCISSA: [0, 1, 4, 2, 3]

plain pos  letter  lands at  carved  forced key letter
       22    E        79        Z       H
       23    A        74        K       N
       24    S        49        W       L
       25    T        63        B       T
       64    B        42        Q       F
       65    E        94        K       I
       66    R        11        U       Q
```

## Lineage

Inherits from 0016-routes-then-tableau-forced-key-english. What changed: Route set: every ordered pair of vocabulary words as two keyed columnar transpositions, each forward or inverse, instead of plain widths. Sanborn's 'double matrixes' with the matrices keyed by words.

## Hypothesis (domain expert)

Sanborn, CNN 2005 (C1): 'double matrixes and triple matrixes... then went back to this table'. The NSA's K3 reading was a keyed columnar with key KRYPTOS; 0006 and 0016 used plain widths and single vocabulary keys. Here both stages are keyed by words from the vocabulary (C7 reading a, C8): 61 x 61 ordered pairs x 4 direction combinations, 14,884 routes, each followed by a periodic tableau under 24 conventions. For each route the cribs land at known positions, the divisor rule gives the live periods, and for live periods up to 40 the forced key is scored as English on runs of five or more slots, with vocabulary matching and ten shuffled controls. Bounds: complete for this route set.

## Prediction

No route lets the cribs force a tableau key shorter than 22, and the forced keys at periods up to 40 score inside the range of ten shuffled controls. No vocabulary match; zero candidates pass.

## Method

1. Build the routes from ordered pairs of vocabulary words, each stage forward or inverse.
2. For each route send the crib positions to their intermediate positions.
3. For each convention force the key letters and find live periods by the divisor rule.
4. Score the forced key at live periods up to 40 on runs of five or more slots; match against the vocabulary.
5. Repeat on ten shuffles.

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
 "family": "double keyed columnar (vocabulary words) then periodic tableau",
 "routes": 15376,
 "conventions": 24,
 "periods": "2-40, live only",
 "keys_scored": 108372,
 "smallest_live_period": 23,
 "min_live_period_histogram": {
  "23": 16,
  "24": 450,
  "25": 262,
  "26": 438,
  "27": 6808,
  "28": 5128,
  "29": 670,
  "30": 3428,
  "31": 1270,
  "32": 5616,
  "33": 3448,
  "34": 3358
 },
 "best": [
  {
   "score": -3.797,
   "route": "MYSTERY then HILL inv",
   "convention": "std/std/kry/beau",
   "period": 39,
   "runs": [
    "ETHEMEP"
   ]
  },
  {
   "score": -4.26,
   "route": "WONDERFUL then RIDDLE",
   "convention": "kry/std/std/beau",
   "period": 37,
   "runs": [
    "HOULD",
    "GBLET"
   ]
  },
  {
   "score": -4.403,
   "route": "HOWARDCARTER inv then WORLDCLOCK inv",
   "convention": "kry/kry/kry/beau",
   "period": 39,
   "runs": [
    "MTHEV",
    "OIREH"
   ]
  },
  {
   "score": -4.443,
   "route": "EAST then NORTHEAST inv",
   "convention": "kry/std/std/beau",
   "period": 40,
   "runs": [
    "ESCRACKP"
   ]
  },
  {
   "score": -4.443,
   "route": "EAST then NORTHEAST inv",
   "convention": "kry/std/std/beau",
   "period": 38,
   "runs": [
    "ESCRACKP"
   ]
  },
  {
   "score": -4.443,
   "route": "EAST then NORTHEAST inv",
   "convention": "kry/std/std/beau",
   "period": 35,
   "runs": [
    "ESCRACKP"
   ]
  },
  {
   "score": -4.49,
   "route": "WELTZEITUHR inv then POSITION",
   "convention": "std/kry/kry/beau",
   "period": 33,
   "runs": [
    "ILETRED"
   ]
  },
  {
   "score": -4.55,
   "route": "SANBORN inv then SHADOWFORCES inv",
   "convention": "kry/kry/kry/varbeau",
   "period": 40,
   "runs": [
    "OMEOFFAO"
   ]
  },
  {
   "score": -4.562,
   "route": "ABSCISSAE inv then SECRET inv",
   "convention": "kry/std/std/varbeau",
   "period": 40,
   "runs": [
    "MMERK",
    "EAMAG"
   ]
  },
  {
   "score": -4.61,
   "route": "DIGITAL inv then WALL",
   "convention": "kry/kry/kry/beau",
   "period": 33,
   "runs": [
    "ILYATOSETC",
    "KBLESTH"
   ]
  }
 ],
 "shuffled_control_best": [
  -4.315,
  -4.088,
  -4.057,
  -4.118,
  -3.819,
  -3.579,
  -3.993,
  -4.23,
  -3.713,
  -4.077
 ]
}
```

Notes: Diagnostic, no candidates. 15376 routes; smallest live period 23; best forced key -3.797 vs shuffled [-4.315, -4.088, -4.057, -4.118, -3.819, -3.579, -3.993, -4.23, -3.713, -4.077].


