# 0006-columnar-then-tableau-period-survival: A matrix transposition first, the keyed tableau last: which routes let the 24 cribs force a short periodic key

**Family:** 6-transposition-then-tableau  
**Parent:** none (root)  
**Decision:** reverted  
**Run:** 2026-10-14T16:34:42+00:00, 6.6 s, status ran  
**Time by phase:** design 175 s, implement 73 s, test 14 s, run 7 s, record 0 s

## In plain words

The artist said he first scrambled the order of the letters by writing them in a grid and reading it another way, and only then used the big table on the sculpture. If that is true, the 24 letters we know are no longer where we think: the grid moved them. For each way of making a grid, we work out where the known letters would have gone, and ask whether a short secret word could then turn them into the carved letters at those spots. Most grids make the known letters contradict each other, which rules them out. A grid that lets a short secret word do the job would be a real find, and we then check whether any word from the puzzle's own world fits.

## Walkthrough, by hand

1. Pick a route: write the text in rows of 7 and read down the columns, left column first.
2. Position 22, the E of EAST, is row 4 column 1 (counting from 1). Column 1 holds rows 1 to 14, so E lands at intermediate position 4.
3. Position 64, the B of BERLIN, is row 10 column 1, so it lands at position 10.
4. The ciphertext at 4 is R and at 10 is H. Under the sculpture's alphabet with Vigenere, the key letter that sends E to R and the one that sends B to H are forced.
5. Do this for all 24 known letters; you get 24 forced key letters at 24 positions.
6. A period of 6 would make positions 4 and 10 share a key letter; if their forced letters differ, period 6 is dead, and so is any period dividing 6.
7. Cross out every dead period; the smallest survivor is the shortest secret word this route allows.
8. Write the survivors' forced letters into a pattern with blanks and slide the puzzle's words across it.

## Worked example (generated)

```
route: columnar width 7, read columns left to right; convention kry/kry/kry Vigenere

plain pos  letter  lands at  cipher there  forced key letter
       22    E         4         R              J
       23    A        18         F              O
       24    S        32         K              Q
       25    T        46         K              V
       64    B        10         H              S
       65    E        24         R              J
       66    R        38         T              P
       67    L        52         J              Z

positions 4 and 10 share a key slot at period 6, 3, 2 and 1; if their forced letters differ, those periods die.
```

## Lineage

Inherits from nothing; this is a root experiment. What changed: New root. Family 6 opens after five reverts in family 1. A columnar transposition stage runs before the periodic tableau, so the cribs constrain the key through the route.

## Hypothesis (domain expert)

Sanborn, CNN 2005 (knowledge/sources, clue C1 reading a): matrix code first, double and triple matrixes sometimes, 'then went back to this table to do the ultimate'. Family A in knowledge/06-hypotheses.md: K4 = tableau(T(P)) where T is a columnar transposition and the tableau stage is periodic with separate alphabets. The cribs sit in P at 22-34 and 64-74. Under T they land at intermediate positions j = T(pos); the ciphertext at j then forces the key letter at slot j mod period under each of the 24 conventions. For each route T we find the smallest period whose forced letters never conflict, by the divisor rule: period p is dead if p divides the distance between two intermediate positions that force different key letters. Routes searched: plain columnar at every width 2 to 96, read columns left to right or right to left, applied forward or inverse; keyed columnar from every vocabulary word, forward or inverse; and every double of two plain forward columnars at widths 2 to 50 (C1 'double matrixes', C2 'all the possible shifts'). Survivors with a short period get their forced fragment matched against the vocabulary and K1-K3 windows; matches are decrypted and submitted. Bounds: complete for the route set above under 24 conventions and periods 1-97.

## Prediction

A dry run on 40 routes calibrated this. The smallest live period will cluster between 24 and 50 for almost every route and convention. Any route with a live period of 15 or less is rarer than one in a thousand and gets a follow-up. No forced fragment matches a vocabulary word or K1-K3 window, so zero candidates pass.

## Method

1. Build the route set: plain columnar widths 2-96 in two column directions, forward and inverse; keyed columnar from each vocabulary word, forward and inverse; doubles of plain forward columnars at widths 2-50.
2. For each route, map each crib position to its intermediate position.
3. For each convention, force the key letter at each intermediate position from the crib plaintext and the ciphertext there.
4. Mark period p dead if it divides a distance between two positions with different forced letters; the smallest live period is the route's score.
5. For live periods up to 30, match the forced fragment against the vocabulary and the K1-K3 windows; decrypt matches and submit.

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
 "family": "columnar transposition then periodic tableau (separate alphabets)",
 "routes": 2905,
 "route_convention_pairs_checked": 69720,
 "route_set": "plain columnar w=2..96 x {ltr, rtl} x {fwd, inv}; keyed columnar from each vocabulary word x {fwd, inv}; double plain columnar w1,w2 in 2..50",
 "conventions": 24,
 "periods": "1-97 by divisor rule",
 "key_pool": "vocabulary words and K1-K3 windows of length P for live P <= 30",
 "min_live_period_histogram": {
  "23": 26,
  "24": 66,
  "25": 634,
  "26": 1582,
  "27": 2566,
  "28": 846,
  "29": 710,
  "30": 476,
  "31": 658,
  "32": 1830,
  "33": 1238,
  "34": 1084,
  "35": 854,
  "36": 1172,
  "37": 1034,
  "38": 1304,
  "39": 658,
  "40": 1028,
  "41": 1104,
  "42": 1312,
  "43": 1706,
  "44": 1476,
  "45": 1562,
  "46": 2940,
  "47": 1970,
  "48": 3942,
  "49": 2586,
  "50": 2126,
  "51": 2236,
  "52": 1290,
  "53": 1358,
  "54": 1176,
  "55": 1422,
  "56": 1352,
  "57": 1234,
  "58": 1062,
  "59": 1066,
  "60": 814,
  "61": 784,
  "62": 948,
  "63": 854,
  "64": 1072,
  "65": 724,
  "66": 956,
  "67": 662,
  "68": 918,
  "69": 664,
  "70": 786,
  "71": 652,
  "72": 1060,
  "73": 450,
  "74": 764,
  "75": 388,
  "76": 740,
  "77": 882,
  "78": 702,
  "79": 390,
  "80": 642,
  "81": 650,
  "82": 308,
  "83": 232,
  "84": 210,
  "85": 164,
  "86": 266,
  "87": 122,
  "88": 512,
  "89": 108,
  "90": 64,
  "91": 128,
  "92": 100,
  "93": 318
 },
 "fifteen_shortest": [
  {
   "min_period": 23,
   "route": "keyed columnar MESSAGE inv",
   "convention": "std/kry/std/vig"
  },
  {
   "min_period": 23,
   "route": "keyed columnar MESSAGE inv",
   "convention": "std/kry/std/varbeau"
  },
  {
   "min_period": 23,
   "route": "keyed columnar MESSAGE inv",
   "convention": "std/kry/kry/vig"
  },
  {
   "min_period": 23,
   "route": "keyed columnar MESSAGE inv",
   "convention": "std/kry/kry/varbeau"
  },
  {
   "min_period": 23,
   "route": "double columnar w=26 then w=2",
   "convention": "std/kry/std/vig"
  },
  {
   "min_period": 23,
   "route": "double columnar w=26 then w=2",
   "convention": "std/kry/std/varbeau"
  },
  {
   "min_period": 23,
   "route": "double columnar w=26 then w=2",
   "convention": "std/kry/kry/vig"
  },
  {
   "min_period": 23,
   "route": "double columnar w=26 then w=2",
   "convention": "std/kry/kry/varbeau"
  },
  {
   "min_period": 23,
   "route": "double columnar w=41 then w=41",
   "convention": "std/std/std/vig"
  },
  {
   "min_period": 23,
   "route": "double columnar w=41 then w=41",
   "convention": "std/std/std/varbeau"
  },
  {
   "min_period": 23,
   "route": "double columnar w=41 then w=41",
   "convention": "std/std/kry/vig"
  },
  {
   "min_period": 23,
   "route": "double columnar w=41 then w=41",
   "convention": "std/std/kry/varbeau"
  },
  {
   "min_period": 23,
   "route": "double columnar w=41 then w=44",
   "convention": "std/std/std/vig"
  },
  {
   "min_period": 23,
   "route": "double columnar w=41 then w=44",
   "convention": "std/std/std/varbeau"
  },
  {
   "min_period": 23,
   "route": "double columnar w=41 then w=44",
   "convention": "std/std/kry/vig"
  }
 ],
 "vocab_matches": 0
}
```

Notes: 69720 route/convention pairs; 0 forced-fragment matches submitted.


