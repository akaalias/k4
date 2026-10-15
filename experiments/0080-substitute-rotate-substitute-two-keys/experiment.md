# 0080-substitute-rotate-substitute-two-keys: Change, turn, change again: a repeating key on the table, a K3-style grid turn, then a second repeating key, solved exactly

**Family:** 6-transposition-then-tableau  
**Parent:** 0008-k3-formula-all-shifts-then-tableau  
**Decision:** reverted  
**Run:** 2026-10-15T15:23:05+00:00, 167.3 s, status ran  
**Time by phase:** design 38 s, implement 86 s, test 88 s, run 167 s, record 0 s

## In plain words

The first two messages were made by shifting letters along the sculpture's table with a repeating secret word; the third was made by writing the letters in a grid and turning it. Sanborn said he used 'double and triple matrixes' and 'then went back to this table'. Here we try the sandwich: shift with one secret word, turn the grid, shift again with a second secret word. That sounds like too many unknowns, but every known letter of the message ties one letter of the first word to one letter of the second, and those ties must agree with each other. We check every grid turn and every pair of word lengths from 2 to 14, exactly, and do the same on ten scrambled copies of the copper to see how often agreement happens by luck.

## Walkthrough, by hand

1. Write the message in rows of 7 and turn the grid a quarter clockwise: read each column from the bottom up, left column first. Counting from 0, place 22 (the E of EAST) is letter 21, in row 3, column 0, and comes out as letter 10 of the turned text (place 11).
2. Take a first key of length 2 and a second of length
3. Letter 21 uses slot 21 mod 2 = 1 of the first key; its new position 10 uses slot 10 mod 3 = 1 of the second. 3. On the sculpture's alphabet, the copper letter at place 11, U, minus E gives the sum of those two key letters: U - E = 10.
4. Every known letter gives such a sum for one slot of each key: 24 sums for 2 + 3 slots.
5. Five slots need four sums to fix them (one is a free shift between the keys); the other twenty sums are checks.
6. Go through the sums and see whether they agree; one disagreement kills this turn and these key lengths.
7. Repeat for every turn, rule and pair of lengths, and on ten scrambled coppers.

## Worked example (generated)

```
one quarter turn clockwise at width 7; first key length 2, second key length 3; sculpture's alphabet, s = +1

place  known  new place  copper there  first slot  second slot  sum of the two key letters
   22      E         11             U           1            1  U-E = 10
   23      A         25             V           0            0  V-A = 15
   24      S         39             Q           1            2  Q-S = 14
   25      T         53             K           0            1  K-T = 22
   26      N         67             V           1            0  V-N = 3
   27      O         81             T           0            2  T-O = 25

24 sums over 2 + 3 slots: 20 independent checks
```

## Lineage

Inherits from 0008-k3-formula-all-shifts-then-tableau. What changed: 0008 and the public searches (keithadler, nitsuah, Zekios) put one repeating key on one side of a K3-style turn. Here there is a key on both sides: the message is changed on the table with one repeating word, the letters are moved by a grid turn (or K3's every-n-th rule, or a column shuffle), and the moved text is changed again with a second repeating word. With both alphabets the same, the 24 known letters give 24 linear equations in the two keys, which are solved exactly for every route and every pair of key lengths 2-14.

## Hypothesis (domain expert)

Type 1 of directions.md, gap a3 of the prior-work database (reports/Kryptos K4 prior attempts database.md: 'rotation sandwiched between two different tableau keys... Zekios's stacked-key search used columnar 2-7 and width-21 routes, not rotations'). Clues C1(a) and C1(c) read together (02-sanborn-said.md, CNN 2005: 'double matrixes and triple matrixes... and then went back to this table'), C2(a) (the K3 matrix and its 'shifts'), C5(b) ('key word/s', two words) and C20(a) (LAYER TWO). Model: X[i] = P[i] (+) a[i mod p1] on alphabet A; Y = route(X); C[j] = Y[j] (+) b[j mod p2] on the same alphabet A, each stage Vigenere, Beaufort or variant. Composed, C[pi(i)] = s P[i] + a'[i mod p1] + b'[pi(i) mod p2] (mod 26, indices on A) with s = -1 when exactly one stage is Beaufort, so the key alphabets drop out and four cases remain: A standard or KRYPTOS, s = +1 or -1. Each known letter is one edge between key slot a_u and key slot b_w carrying the value C - sP; the system is consistent iff every cycle of that bipartite graph sums to zero, checked by a spanning tree; the number of independent checks is edges minus (slots touched minus components). Routes (deduplicated on where the 24 known places land): K3's rule pi(i) = a + b i mod 97, all 9,312; one quarter turn, clockwise or anticlockwise, at widths 2-96, each forward and inverse; two clockwise quarter turns at every width pair 2-96, forward and inverse; plain columnar at widths 2-96 in both reading directions, forward and inverse; keyed columnar from every vocabulary word, forward and inverse. Key lengths p1, p2 = 2-14. Exact; ten shuffled coppers through the identical search give the chance rate at each number of checks. Bound left open: the two stages on different alphabets (not linear), key lengths above 14, nulls or padding (gap a1).

## Prediction

At every number of checks K4's count of consistent cases lies inside the range of the ten shuffled coppers. No case on K4 survives seven or more independent checks. Zero candidates.

## Method

1. Build the routes and keep one per distinct landing pattern of the 24 known places.
2. For each route, each alphabet and each sign, compute the edge values C at the landing place minus s times the known letter.
3. For each pair of key lengths, join slot i mod p1 of the first key to slot (landing place) mod p2 of the second key for every known letter, grow a spanning tree, and test every other edge against the tree.
4. Count consistent cases by number of checks.
5. Repeat on ten shuffled coppers.
6. Print any K4 case with five or more checks, with its key slots and the letters they fix.

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
 "family": "substitute, move, substitute: two repeating keys on one alphabet around a route, solved exactly",
 "route_specs": 28246,
 "distinct_routes": 26158,
 "routes_done": 26158,
 "route_kinds": "K3 rule a + b i mod 97 (9,312); one quarter turn cw/ccw widths 2-96 fwd/inv; two cw quarter turns widths 2-96 x 2-96 fwd/inv; plain columnar widths 2-96 both directions fwd/inv; keyed columnar from 62 vocabulary words fwd/inv",
 "key_lengths": [
  2,
  14
 ],
 "cases_per_structure": "alphabet std or KRYPTOS x sign +1/-1 = 4",
 "structures_with_checks": 4389273,
 "structures_by_checks": {
  "1": 76391,
  "2": 123042,
  "3": 165672,
  "4": 200668,
  "5": 236715,
  "6": 267487,
  "7": 297357,
  "8": 338856,
  "9": 351044,
  "10": 365967,
  "11": 329190,
  "12": 313924,
  "13": 255552,
  "14": 248779,
  "15": 203343,
  "16": 180973,
  "17": 144202,
  "18": 120965,
  "19": 81461,
  "20": 59474,
  "21": 27546,
  "22": 665
 },
 "k4_consistent_by_checks": {
  "1": 11768,
  "2": 766,
  "3": 30,
  "4": 4,
  "5": 0,
  "6": 0,
  "7": 0,
  "8": 0,
  "9": 0,
  "10": 0,
  "11": 0,
  "12": 0,
  "13": 0,
  "14": 0,
  "15": 0,
  "16": 0,
  "17": 0,
  "18": 0,
  "19": 0,
  "20": 0,
  "21": 0,
  "22": 0
 },
 "controls_consistent_by_checks": {
  "1": [
   11578,
   12018,
   11858,
   11703,
   11706,
   11664,
   11780,
   11789,
   11713,
   11815
  ],
  "2": [
   774,
   661,
   750,
   668,
   743,
   722,
   747,
   701,
   679,
   701
  ],
  "3": [
   39,
   44,
   42,
   38,
   40,
   44,
   37,
   36,
   47,
   39
  ],
  "4": [
   2,
   3,
   0,
   1,
   3,
   1,
   0,
   2,
   4,
   6
  ],
  "5": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  "6": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  "7": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  "8": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  "9": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  "10": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  "11": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  "12": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  "13": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  "14": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  "15": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  "16": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  "17": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  "18": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  "19": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  "20": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  "21": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  "22": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ]
 },
 "k4_at_least": {
  "1": 12568,
  "2": 800,
  "3": 34,
  "4": 4,
  "5": 0,
  "6": 0,
  "7": 0,
  "8": 0
 },
 "controls_at_least": {
  "1": [
   12393,
   12726,
   12650,
   12410,
   12492,
   12431,
   12564,
   12528,
   12443,
   12561
  ],
  "2": [
   815,
   708,
   792,
   707,
   786,
   767,
   784,
   739,
   730,
   746
  ],
  "3": [
   41,
   47,
   42,
   39,
   43,
   45,
   37,
   38,
   51,
   45
  ],
  "4": [
   2,
   3,
   0,
   1,
   3,
   1,
   0,
   2,
   4,
   6
  ],
  "5": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  "6": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  "7": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  "8": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ]
 },
 "check_levels_outside_control_range": [
  3
 ],
 "k4_cases_with_5_or_more_checks": [],
 "n_k4_cases_5_plus": 0,
 "controls": "10 shuffled coppers (seed 80), identical search"
}
```

Notes: 26,158 distinct routes from 28,246 specs, 4,389,273 route x key-length structures with at least one check, x4 cases. K4 consistent cases with at least c checks, c = 1..8: [12568, 800, 34, 4, 0, 0, 0, 0]; controls max: [12726, 815, 51, 6, 0, 0, 0, 0]; controls min: [12393, 707, 37, 0, 0, 0, 0, 0]. Levels outside the control range: [3]. K4 cases with 5+ checks: 0.


