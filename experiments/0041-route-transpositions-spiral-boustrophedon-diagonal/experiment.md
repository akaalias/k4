# 0041-route-transpositions-spiral-boustrophedon-diagonal: Routes beyond columns: spirals, snakes and diagonals through a grid, tested in both orders

**Family:** 6-transposition-then-tableau  
**Parent:** 0016-routes-then-tableau-forced-key-english  
**Decision:** reverted  
**Run:** 2026-10-15T09:08:53+00:00, 6.1 s, status ran  
**Time by phase:** design 0 s, implement 61 s, test 6 s, run 6 s, record 0 s

## In plain words

So far the grids were read out by columns. The old manuals also read them out in a spiral from a corner, in a snake that turns at the end of each row, or along diagonals. We try all of those, at every width, and ask the two questions as before: if the scramble came first, could a short secret word on the table then explain the carved letters; and if the letters were swapped first and scrambled after, do the 24 known letters ever land without clashing.

## Walkthrough, by hand

1. Width 10: write the 97 positions in rows of 10.
2. Spiral: start at the top left, read along the top row, down the right edge, back along the bottom, up the left edge, then inward.
3. Note where position 22, the E of EAST, comes out, and where each of the other known letters comes out.
4. Before-the-table test: the carved letter at each landing place and the known letter force a key letter; landing places a multiple of p apart must agree.
5. After-a-swap test: if the carved letter at E's landing place also sits at the landing place of a different known letter, the route is dead for any letter swap.
6. Snake and diagonals the same way, at every width.

## Worked example (generated)

```
route: rows of 10, read out in a clockwise spiral from the top left

first twelve positions read out: 1 2 3 4 5 6 7 8 9 10 20 30

plain pos  letter  lands at  carved there
       22    E        61        N
       23    A        62        F
       24    S        63        B
       64    B        91        A
       65    E        90        U
       66    R        89        H
```

## Lineage

Inherits from 0016-routes-then-tableau-forced-key-english. What changed: The route set is the one gap the columnar experiments left: writing in rows and reading out along a spiral, a snake (alternate rows reversed), or diagonals, at every width. Each route is tested before the tableau, as in experiments 6 and 16, and after a substitution, as in experiment 19.

## Hypothesis (domain expert)

Experiments 6, 8, 16, 26 and 37 covered columnar, keyed columnar, rotation and affine routes; 19 covered substitution then those routes. The classical route transpositions of the manuals, spiral inward and outward from each corner in either turn, boustrophedon by rows and by columns, and the two diagonal zigzags, at widths 2-48 (about 700 routes), remain. Two tests per route. Before a periodic tableau: the forced key letters at the crib landing places give the live periods by the divisor rule and the forced key at live periods up to 40 is scored as English, 8 conventions, with ten full-size shuffled controls. After any one-to-one substitution: the 24 crib images must never put two different plaintext letters on one carved letter, as in experiment 19, with ten shuffles. Bounds: complete for these route families at these widths, both orders.

## Prediction

Before the tableau: smallest live period 22 to 24, forced keys inside the range of the shuffled controls. After a substitution: no route passes the one-to-one test, and no shuffle does either. No candidate.

## Method

1. Build the routes as permutations of 97 positions: for each width, spirals from four corners in two turns inward, boustrophedon by rows and by columns, and the two diagonal zigzags; each also inverted.
2. Test one, before the tableau: send the cribs through, force key letters under 8 conventions, live periods by the divisor rule, score the forced key at live periods up to 40.
3. Test two, after a substitution: check the crib images for clashes.
4. Ten shuffles for each test.

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
 "family": "route transpositions (spiral, snake, diagonal), widths 2-48, forward and inverse; before a periodic tableau and after a substitution",
 "routes": 1128,
 "conventions_before": 8,
 "before_smallest_live_period": 23,
 "before_min_period_histogram": {
  "23": 19,
  "24": 93,
  "25": 138,
  "26": 268,
  "27": 469,
  "28": 261,
  "29": 167,
  "30": 180,
  "31": 217,
  "32": 206
 },
 "before_best": [
  {
   "score": -4.937,
   "route": "spiral w=5 from bl ccw inv",
   "convention": "kry/kry/kry/beau",
   "period": 38,
   "runs": [
    "GLEBRIM"
   ]
  },
  {
   "score": -5.078,
   "route": "diagonal zigzag w=36 inv",
   "convention": "kry/std/kry/beau",
   "period": 40,
   "runs": [
    "LFULORAC"
   ]
  },
  {
   "score": -5.438,
   "route": "diagonal zigzag w=34 inv",
   "convention": "kry/std/kry/beau",
   "period": 28,
   "runs": [
    "BEOPLFULOWEVE",
    "YDLUNDT"
   ]
  },
  {
   "score": -5.491,
   "route": "spiral w=27 from bl ccw inv",
   "convention": "std/kry/kry/beau",
   "period": 40,
   "runs": [
    "AILDADCITYU",
    "FBIOTIGGR"
   ]
  },
  {
   "score": -5.516,
   "route": "diagonal zigzag w=31 inv",
   "convention": "std/std/kry/beau",
   "period": 34,
   "runs": [
    "NDOMETZRANEQ"
   ]
  },
  {
   "score": -5.531,
   "route": "spiral w=5 from bl ccw inv",
   "convention": "std/std/kry/vig",
   "period": 33,
   "runs": [
    "DASLYPH"
   ]
  },
  {
   "score": -5.549,
   "route": "spiral w=28 from tr cw inv",
   "convention": "kry/std/kry/beau",
   "period": 37,
   "runs": [
    "UTIPACITTISPUKUB"
   ]
  },
  {
   "score": -5.581,
   "route": "spiral w=40 from tl ccw",
   "convention": "std/kry/kry/vig",
   "period": 40,
   "runs": [
    "IONTOGNPAOE",
    "RERISAIMMEOTJ"
   ]
  },
  {
   "score": -5.581,
   "route": "spiral w=40 from tl ccw",
   "convention": "std/kry/kry/vig",
   "period": 39,
   "runs": [
    "IONTOGNPAOE",
    "RERISAIMMEOTJ"
   ]
  },
  {
   "score": -5.581,
   "route": "spiral w=40 from tl ccw",
   "convention": "std/kry/kry/vig",
   "period": 38,
   "runs": [
    "IONTOGNPAOE",
    "RERISAIMMEOTJ"
   ]
  }
 ],
 "before_shuffled_best": [
  -5.305,
  -4.473,
  -4.909,
  -4.614,
  -4.791,
  -5.019,
  -5.015,
  -4.968,
  -4.85,
  -4.858
 ],
 "before_shuffled_smallest_period": [
  22,
  22,
  22,
  22,
  22,
  23,
  22,
  23,
  23,
  22
 ],
 "after_survivors": [],
 "after_shuffled_survivor_counts": [
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
}
```

Notes: 1128 routes. Before the tableau: smallest live period 23, best forced key -4.937 vs shuffled [-5.305, -4.473, -4.909, -4.614, -4.791, -5.019, -5.015, -4.968, -4.85, -4.858]. After a substitution: 0 routes pass the one-to-one test vs shuffled [0, 0, 0, 0, 0, 0, 0, 0, 0, 0].


