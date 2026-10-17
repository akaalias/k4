# 0185-trifid-free-cubes-above-period-15: F4.2: trifid with a free 27-symbol cube at periods 16-97, every alignment, by constraint propagation: exact

**Family:** 4-sanborn-visual  
**Parent:** 0040-trifid-free-cubes-by-constraint-propagation-rerun  
**Decision:** reverted  
**Run:** 2026-10-17T00:35:05+00:00, 6.0 s, status ran  
**Time by phase:** design 0 s, implement 0 s, test 0 s, run 6 s, record 0 s

## In plain words

Sanborn is a sculptor; a trifid code puts the alphabet in a 3 x 3 x 3 cube and mixes the three coordinates of neighbouring letters in groups. Groups of up to 15 letters were already ruled out. Here every longer group, up to the whole text, with every starting point: do the known letters allow any arrangement of the cube at all?

## Walkthrough, by hand

1. Take period 20 with blocks starting at place 1: places 21-40 form one block.
2. Write each block letter's three coordinates in three rows, read the rows one after another, regroup in threes.
3. Each known letter's coordinates must then equal certain coordinates of certain carved letters.
4. Merge equal coordinates; try values 0-2 for each merged group so no two letters share an address.
5. If nothing survives, no cube works at that period and start.

## Worked example (generated)

```
period 20, blocks from position 1: the block 21-40 carries EASTNORTHEAST at 22-34 against the carved FLRVQQPRNGKSS

81 coordinate variables merge into 22 classes under all the ties from the 24 known letters
backtracking over the classes with the all-different rule visited 1 nodes and found 0 cube(s)
```

## Lineage

Inherits from 0040-trifid-free-cubes-by-constraint-propagation-rerun. What changed: F4.2. 0040 decided every free trifid cube at periods 2-15 (no cube fits at any alignment). Its decider does not depend on the period: each known letter ties its three coordinates to coordinates of three carved letters in its block, whatever the block length. Here periods 16-97 (97: one block), every alignment, 4,633 settings, with the same caps; ten shuffled copies run through the same sweep as the null.

## Hypothesis (domain expert)

C3 (Sanborn's visual, three-dimensional thinking: a cube), F4; Delastelle's trifid keeps one letter per letter on 27 symbols. Model as 0040: the k-th coordinate of carved letter j in a block of n equals coordinate (3j + k) div n of plaintext letter (3j + k) mod n. 72 equalities among 81 coordinate variables, then backtracking over the classes with the 27-distinct-addresses rule and 9-per-value counts. Statistic: settings admitting a cube, K4 against 10 shuffled copies; any surviving cube decrypts and is scored.

## Prediction

No cube at any setting, as at 2-15; or cubes at the copies' rate whose decryptions are not English. Zero candidates.

## Method

1. For each period 16-97 and alignment: the coordinate equalities the 24 known letters force.
2. Union-find, then backtracking over classes with the address and count rules (caps 3M nodes, 5,000 cubes).
3. Count settings with cubes; decrypt and score any.
4. The same sweep on 10 shuffled copies.

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
 "family": "trifid, free 27-symbol cube, periods 16-97, every alignment, constraint propagation and backtracking",
 "settings": 4633,
 "settings_with_cubes": 0,
 "settings_capped": 0,
 "node_cap": 3000000,
 "solution_cap": 5000,
 "k4_settings_with_cubes": [],
 "max_nodes": 364,
 "best": [],
 "plant": {
  "period": 30,
  "offset": 5,
  "cubes": 288,
  "true_cube_found": true
 },
 "controls": [
  {
   "settings": 4633,
   "with_cubes": 0,
   "capped": 0,
   "best_english": null
  },
  {
   "settings": 4633,
   "with_cubes": 0,
   "capped": 0,
   "best_english": null
  },
  {
   "settings": 4633,
   "with_cubes": 0,
   "capped": 0,
   "best_english": null
  },
  {
   "settings": 4633,
   "with_cubes": 0,
   "capped": 0,
   "best_english": null
  },
  {
   "settings": 4633,
   "with_cubes": 0,
   "capped": 0,
   "best_english": null
  },
  {
   "settings": 4633,
   "with_cubes": 0,
   "capped": 0,
   "best_english": null
  },
  {
   "settings": 4633,
   "with_cubes": 0,
   "capped": 0,
   "best_english": null
  },
  {
   "settings": 4633,
   "with_cubes": 0,
   "capped": 0,
   "best_english": null
  },
  {
   "settings": 4633,
   "with_cubes": 0,
   "capped": 0,
   "best_english": null
  },
  {
   "settings": 4633,
   "with_cubes": 0,
   "capped": 0,
   "best_english": null
  }
 ],
 "seconds": 6,
 "exhaustive": true
}
```

Notes: 4633 settings; 0 admit a cube on K4; 0 capped; copies with cubes: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


