# 0008-k3-formula-all-shifts-then-tableau: K3's own matrix run through all the possible shifts, then the tableau

**Family:** 6-transposition-then-tableau  
**Parent:** 0006-columnar-then-tableau-period-survival  
**Decision:** reverted  
**Run:** 2026-10-14T16:43:10+00:00, 37.5 s, status ran  
**Time by phase:** design 52 s, implement 0 s, test 6 s, run 38 s, record 0 s

## In plain words

The third message was scrambled by a fixed rule: take every 192nd letter, wrapping around. The artist once said he was surprised nobody had taken that same rule and tried all its settings. So we do: every step size and every starting point for the 97 letters, and also the grid-turning trick the code-breakers described for the third message. For each setting we work out where the 24 known letters would have gone and ask whether a short secret word on the sculpture's table could then produce the carved letters there. A setting that allows a short word is the signal.

## Walkthrough, by hand

1. Pick a rule: start at 5, step
7. The first plaintext letter comes from position 5, the second from 12, the third from 19, and so on, wrapping past
97. 
2. Position 22 of the plaintext, the E of EAST, is the 22nd letter read, so it comes from 5 + 7 x 21 = 152, which wraps to
55. 
3. The ciphertext at 55 is therefore the enciphered E; under the sculpture's alphabet and Vigenere the key letter that sends E there is forced.
4. Do this for all 24 known letters to get 24 forced key letters at 24 positions.
5. Two positions whose distance is a multiple of p share a key slot at period p; if their forced letters differ, p is dead.
6. The smallest live p is the shortest secret word the rule allows.
7. Slide the puzzle's words across the survivors' pattern.

## Worked example (generated)

```
route: K3 rule, start 5, step 7 (plaintext[i] comes from position 5 + 7 i, 0-indexed); convention kry/kry/kry Vigenere

plain pos  letter  lands at  cipher there  forced key letter
       22    E        31         G              Y
       23    A        45         E              T
       24    S        59         W              L
       25    T        73         P              Z
       64    B        37         W              I
       65    E        51         T              N
       66    R        65         Y              R
       67    L        79         Z              B

consecutive crib letters land 7 apart, so period 7 and period 1 need their forced letters equal.
```

## Lineage

Inherits from 0006-columnar-then-tableau-period-survival. What changed: Route set replaced. Instead of columnar grids, the routes are K3's transposition rule with every shift, plus K3-style double rotations of a grid. Survival test unchanged.

## Hypothesis (domain expert)

Sanborn, 2003, secondhand (clue C2): surprised no one had tried 'recovering the original matrix and running it through all the possible shifts'. K3's matrix is known: Stehle's rule reads plaintext[i] = ciphertext[(191 + 192 i) mod 337] (data/k3.json), and the NSA described it as a double rotation of a grid. Reading (a): K4 is the same matrix with a different shift. For n = 97, prime, every pair (a, b) with b in 1..96 is a valid rule, 9,312 routes, each applied forward and inverse; add the double rotations, write in rows of w1 and read columns bottom-up, then again with w2, for w1, w2 in 2..50. Each route goes before a periodic tableau with separate alphabets, as in 0006, and the cribs force key letters at their new positions; the divisor rule gives the smallest live period. Live periods up to 30 are matched against the vocabulary and K1-K3 windows. Bounds: complete for this route set, 24 conventions, periods 1-97.

## Prediction

As in 0006, the smallest live period clusters between 24 and 50. No route allows a period of 15 or less. No forced fragment matches a vocabulary word or K1-K3 window; zero candidates pass.

## Method

1. Build the routes: plaintext[i] = inter[(a + b i) mod 97] for a in 0..96, b in 1..96, forward and inverse; double rotations of a grid for widths 2-50 twice.
2. For each route, send each crib position to its intermediate position.
3. For each convention, force the key letter from the crib plaintext and the ciphertext at the destination.
4. Period p is dead if it divides a distance between two destinations with different forced letters; the smallest live p is the route's score.
5. For live p up to 30, match the forced fragment against the vocabulary and K1-K3 windows; decrypt matches and submit.

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
 "family": "K3 affine rule with all shifts, or double rotation, then periodic tableau (separate alphabets)",
 "routes": 21025,
 "route_convention_pairs_checked": 504600,
 "route_set": "plaintext[i] = inter[(a + b i) mod 97], a in 0..96, b in 1..96, fwd and inv; double rotation w1, w2 in 2..50",
 "conventions": 24,
 "periods": "1-97 by divisor rule",
 "key_pool": "vocabulary words and K1-K3 windows of length P for live P <= 30",
 "min_live_period_histogram": {
  "22": 4,
  "23": 22,
  "24": 492,
  "25": 1276,
  "26": 6644,
  "27": 8744,
  "28": 8430,
  "29": 9646,
  "30": 11430,
  "31": 24652,
  "32": 25370,
  "33": 38770,
  "34": 33660,
  "35": 29338,
  "36": 29950,
  "37": 15774,
  "38": 29406,
  "39": 27084,
  "40": 17890,
  "41": 18424,
  "42": 16512,
  "43": 24298,
  "44": 18380,
  "45": 10120,
  "46": 16502,
  "47": 25208,
  "48": 7740,
  "49": 5308,
  "50": 8486,
  "51": 2816,
  "52": 4466,
  "53": 1052,
  "54": 820,
  "55": 1990,
  "56": 1158,
  "57": 878,
  "58": 1112,
  "59": 1268,
  "60": 1194,
  "61": 922,
  "62": 1162,
  "63": 834,
  "64": 1010,
  "65": 938,
  "66": 1090,
  "67": 814,
  "68": 890,
  "69": 716,
  "70": 732,
  "71": 658,
  "72": 634,
  "73": 796,
  "74": 482,
  "75": 528,
  "76": 626,
  "77": 578,
  "78": 710,
  "79": 384,
  "80": 438,
  "81": 404,
  "82": 528,
  "83": 350,
  "84": 186,
  "85": 248,
  "86": 212,
  "87": 212,
  "88": 210,
  "89": 488,
  "90": 62,
  "91": 80,
  "92": 14,
  "93": 16,
  "94": 334
 },
 "fifteen_shortest": [
  {
   "min_period": 22,
   "route": "K3 rule a=24 b=2 fwd",
   "convention": "std/std/std/beau"
  },
  {
   "min_period": 22,
   "route": "K3 rule a=24 b=2 fwd",
   "convention": "std/std/kry/beau"
  },
  {
   "min_period": 22,
   "route": "K3 rule a=85 b=49 inv",
   "convention": "std/std/std/beau"
  },
  {
   "min_period": 22,
   "route": "K3 rule a=85 b=49 inv",
   "convention": "std/std/kry/beau"
  },
  {
   "min_period": 23,
   "route": "K3 rule a=60 b=8 fwd",
   "convention": "std/kry/std/beau"
  },
  {
   "min_period": 23,
   "route": "K3 rule a=60 b=8 fwd",
   "convention": "std/kry/kry/beau"
  },
  {
   "min_period": 23,
   "route": "K3 rule a=53 b=12 inv",
   "convention": "std/std/std/beau"
  },
  {
   "min_period": 23,
   "route": "K3 rule a=53 b=12 inv",
   "convention": "std/std/kry/beau"
  },
  {
   "min_period": 23,
   "route": "K3 rule a=41 b=85 inv",
   "convention": "std/kry/std/beau"
  },
  {
   "min_period": 23,
   "route": "K3 rule a=41 b=85 inv",
   "convention": "std/kry/kry/beau"
  },
  {
   "min_period": 23,
   "route": "K3 rule a=36 b=89 fwd",
   "convention": "std/std/std/beau"
  },
  {
   "min_period": 23,
   "route": "K3 rule a=36 b=89 fwd",
   "convention": "std/std/kry/beau"
  },
  {
   "min_period": 23,
   "route": "double rotation w=40 then w=45",
   "convention": "std/kry/std/vig"
  },
  {
   "min_period": 23,
   "route": "double rotation w=40 then w=45",
   "convention": "std/kry/std/varbeau"
  },
  {
   "min_period": 23,
   "route": "double rotation w=40 then w=45",
   "convention": "std/kry/kry/vig"
  }
 ],
 "vocab_matches": 0
}
```

Notes: 504600 route/convention pairs; 0 forced-fragment matches submitted. K3 rule verified against data/k3.json inside run.


