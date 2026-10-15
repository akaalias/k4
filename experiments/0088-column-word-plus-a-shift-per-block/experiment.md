# 0088-column-word-plus-a-shift-per-block: A key word over the columns plus a shift that changes every m letters, the carved lines of 31 among them

**Family:** 3-two-component-key  
**Parent:** 0087-column-word-plus-row-word  
**Decision:** reverted  
**Run:** 2026-10-15T16:42:36+00:00, 1.4 s, status ran  
**Time by phase:** design 0 s, implement 10 s, test 0 s, run 1 s, record 0 s

## In plain words

Keep the column word of experiment 87, but let the second shift change every so many letters, not at the end of each row: for instance once per carved line of the sculpture, which holds 31 letters. Within a stretch where the second shift stays the same, doubled letters can still only appear in certain columns of the word. The 24 known letters test every word length, stretch length and starting point exactly.

## Walkthrough, by hand

1. On the sculpture K4 begins four letters before the end of a 31-letter carved line, so its places 1-4 end one line, 5-35 fill the next, 36-66 the next and 67-97 the last.
2. Take a key word of 7 letters over the columns (place p uses letter (p - 1) mod 7) plus one shift for each carved line.
3. Places 22 and 29 both use column 0 and both lie on the line of places 5-35, so they need the same total key.
4. On the sculpture's alphabet with Vigenere, F - E = 1 at place 22 and R - T = 23 at place 29: different, so a 7-letter word with one shift per carved line is dead on this table.
5. Repeat for every word length 2-31, every stretch length 2-50 and starting point, both tables and signs, and ten scrambled coppers.

## Worked example (generated)

```
the carved lines: K4 starts 4 letters before the end of a 31-letter line (offset 27)
line 1: places 1-4, line 2: 5-35, line 3: 36-66, line 4: 67-97

word of length 7 over the columns, one shift per carved line; sculpture's alphabet, s = +1

place  known  copper  column  line  copper - known
   22      E       F       0     2     1
   29      T       R       0     2    23
   64      B       N       0     3    11
   71      L       Z       0     4     8

7 column slots, 3 line slots, 24 known letters: 15 checks
```

## Lineage

Inherits from 0087-column-word-plus-row-word. What changed: 0087 tied the second shift to the rows of the same grid. Here the second shift changes every m letters for any m from 2 to 50 and any starting offset, independent of the column word's length w (2-31). Among these is the sculpture's own layout: K4 starts four letters before the end of a 31-letter carved line and fills three more, so a shift per carved line is m = 31 with offset 27. Doublets still pile up by column wherever the block shift stays constant.

## Hypothesis (domain expert)

Type 2 of directions.md, continued from 0087: the doublet-column mechanism key = a[j mod w] + b[(j + o) div m] with the block length m free of w (a slowly changing tableau row, a new row of the table every m letters, or a new shift per line of text). C27(b) (the BERLIN worksheet laid out on 31-character lines he counted on; 01-facts.md: K4 fills the last four characters of K3's eleventh line and three full 31-character lines), the prior-work database ('the literal physical artifacts (the 31-character carved lines...) have not been used as a route or grid in any published attempt'), C5(b), C8(a), C11a. One alphabet (standard or KRYPTOS), sign +1 or -1, no move. Each known letter is an edge between column slot j mod w and block slot (j + o) div m; consistency by spanning tree. Bounds: w = 2-31, m = 2-50, o = 0..m-1 (the column key's own offset is a relabelling and drops out). Exact; ten shuffled coppers.

## Prediction

No combination with three or more checks survives on K4 beyond the shuffled-copper rate; the carved-line case (m = 31, offset 27) is dead at every word length. Zero candidates.

## Method

1. For each word length w, block length m and offset o, give each known letter its column slot and block slot.
2. Grow a spanning tree over the slots and test the other known letters, on both alphabets and both signs.
3. Count consistent combinations by number of checks on K4 and ten shuffled coppers.
4. Print K4's survivors with three or more checks and the carved-line case.

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
 "family": "key = a[j mod w] + b[(j + o) div m], one alphabet, either sign, no move",
 "w": [
  2,
  31
 ],
 "m": [
  2,
  50
 ],
 "offsets": "all 0..m-1",
 "structures_with_checks": 31994,
 "structures_by_checks": {
  "1": 1434,
  "2": 1295,
  "3": 352,
  "4": 1177,
  "5": 1285,
  "6": 3214,
  "7": 2000,
  "8": 2728,
  "9": 1986,
  "10": 3373,
  "11": 1276,
  "12": 1272,
  "13": 1272,
  "14": 1271,
  "15": 1269,
  "16": 1267,
  "17": 1263,
  "18": 1251,
  "19": 1238,
  "20": 1109,
  "21": 662
 },
 "carved_lines_m31_o27": {
  "2": {
   "checks": 20,
   "consistent": []
  },
  "3": {
   "checks": 19,
   "consistent": []
  },
  "4": {
   "checks": 18,
   "consistent": []
  },
  "5": {
   "checks": 17,
   "consistent": []
  },
  "6": {
   "checks": 16,
   "consistent": []
  },
  "7": {
   "checks": 15,
   "consistent": []
  },
  "8": {
   "checks": 14,
   "consistent": []
  },
  "9": {
   "checks": 13,
   "consistent": []
  },
  "10": {
   "checks": 12,
   "consistent": []
  },
  "11": {
   "checks": 11,
   "consistent": []
  },
  "12": {
   "checks": 10,
   "consistent": []
  },
  "13": {
   "checks": 9,
   "consistent": []
  },
  "14": {
   "checks": 9,
   "consistent": []
  },
  "15": {
   "checks": 7,
   "consistent": []
  },
  "16": {
   "checks": 6,
   "consistent": []
  },
  "17": {
   "checks": 5,
   "consistent": []
  },
  "18": {
   "checks": 5,
   "consistent": []
  },
  "19": {
   "checks": 7,
   "consistent": []
  },
  "20": {
   "checks": 9,
   "consistent": []
  },
  "21": {
   "checks": 9,
   "consistent": []
  },
  "22": {
   "checks": 7,
   "consistent": []
  },
  "23": {
   "checks": 6,
   "consistent": []
  },
  "24": {
   "checks": 4,
   "consistent": []
  },
  "25": {
   "checks": 2,
   "consistent": []
  },
  "31": {
   "checks": 1,
   "consistent": []
  }
 },
 "k4_at_least": {
  "1": 1,
  "2": 0,
  "3": 0,
  "4": 0,
  "5": 0,
  "6": 0,
  "7": 0,
  "8": 0
 },
 "controls_at_least": {
  "1": [
   89,
   0,
   108,
   90,
   0,
   230,
   90,
   3,
   20,
   109
  ],
  "2": [
   0,
   0,
   0,
   0,
   0,
   0,
   1,
   0,
   0,
   0
  ],
  "3": [
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
  "4": [
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
 "check_levels_outside_control_range": [],
 "k4_survivors_3_plus": [],
 "n_k4_3_plus": 0,
 "controls": "10 shuffled coppers (seed 88), identical search"
}
```

Notes: 31,994 (w, m, offset) structures x 4 cases. K4 consistent with >= c checks, c = 1..8: [1, 0, 0, 0, 0, 0, 0, 0]; controls max [230, 1, 0, 0, 0, 0, 0, 0], min [0, 0, 0, 0, 0, 0, 0, 0]. Outside: []. Carved lines (m = 31, offset 27): widths alive none. K4 survivors with 3+ checks: 0.


