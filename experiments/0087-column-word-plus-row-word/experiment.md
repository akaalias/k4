# 0087-column-word-plus-row-word: A key word over the columns and a second key over the rows: the message in rows of seven, each letter shifted by its column's letter and its row's letter

**Family:** 3-two-component-key  
**Parent:** 0032-row-keyed-grids-one-key-letter-per-row  
**Decision:** reverted  
**Run:** 2026-10-15T16:38:44+00:00, 113.1 s, status ran  
**Time by phase:** test 0 s, run 113 s, record 0 s

## In plain words

Write the message in rows of seven under KRYPTOS. Shift each letter along the table by its column's letter of KRYPTOS, and also by a letter chosen for its row from a second key. It is easy to do by hand and needs two key words, as Scheidt said. It also explains an oddity: inside a row the row's shift is the same for both letters of a pair, so doubled letters can only appear where two neighbouring column letters differ in a particular way, and they pile up in the same column, as five of K4's six doubled letters do. The 24 known letters test every width exactly, with and without a scrambling step before or after.

## Walkthrough, by hand

1. Write the copper in rows of 7. Place 22 is in row 3, column 0; place 23 in row 3, column 1; places 29 and 30 in row 4, columns 0 and 1.
2. On the sculpture's alphabet with Vigenere, copper minus message gives the key at each place: F - E = 1 at 22, L - A = 10 at 23, R - T = 23 at 29, N - H = 5 at 30.
3. Each key is a column letter plus a row letter. Places 22 and 23 share their row, so their difference, 1 - 10 = 17, is the difference of the column letters 0 and 1.
4. Places 29 and 30 share the next row and the same two columns, so 23 - 5 = 18 must be the same difference.
5. 17 is not 18: width 7 with this table is dead, whatever the two key words are.
6. Width 7 has 14 such checks in all; test every width 2-48, both tables and signs, with no move and after each of 0080's moves in both orders, and on ten scrambled coppers.

## Worked example (generated)

```
no move; rows of 7; key = column letter + row letter; sculpture's alphabet, s = +1

place  known  copper  column  row  copper - known = column + row
   22      E       F       0    3     1
   23      A       L       1    3    10
   29      T       R       0    4    23
   30      H       N       1    4     5
   64      B       N       0    9    11
   65      E       Y       1    9    17
   71      L       Z       0   10     8
   72      O       F       1   10     7

24 known letters, 7 column slots and 4 row slots: 14 checks
places 22 and 29 share column 0; places 23 and 30 share column 1; 22, 23 share row 3; 29, 30 share row 4:
  (22) - (23) must equal (29) - (30): 1 - 10 = 17, 23 - 5 = 18
```

## Lineage

Inherits from 0032-row-keyed-grids-one-key-letter-per-row. What changed: 0032 gave each row of the grid one key letter; repeating keys give each column one. Here both at once: the key at a place is its column's letter of one word plus its row's letter of a second key, on a grid of width 2-48. Within a row the row letter cancels, so a column whose letter steps against its neighbour's makes doubled letters in that column only: the one construction found here that lines doublets up in sevens by design. Tested exactly from the 24 known letters, on the copper as carved and after each of 0080's 26,000 moves (keyed columns read the right way, issue #26), in both orders.

## Hypothesis (domain expert)

Type 2 of directions.md ('7-block constructions... keyed by KRYPTOS or another 7-letter word'), the prior-work database's seven-based sub-variant 4 ('KRYPTOS as a numeric key for something other than column order or an additive key: row order in a 14x7, or a per-row shift of a width-7 grid (Bean-style row shifts)'). Mechanism for the width-7 doublet column (0056, 0065): with key a[j mod w] + b[j div w], two adjacent letters in one row share b, so C[j] = C[j+1] iff P[j+1] - P[j] = a[c] - a[c+1], which depends only on the column c; doublets collect in the columns where a steps, i.e. at fixed residues mod w. Clues C5(b) ('key word/s'), C8(a) (KRYPTOS as the K4 key in a new way), C1(a) and C3 ('matrix', 'spatial systems'), C11a ('interval 7'). Model on one alphabet A (standard or KRYPTOS), sign s = +1 or -1 (s = -1 when exactly one of the two keys is applied Beaufort-wise): C[j] = s P + a[col] + b[row]; each known letter is an edge between column slot and row slot, consistency by spanning tree, checks = edges - (slots touched - components). Grid positions are carved places (move, then grid key: order A) or message places (grid key, then move: order B). Moves: none, plus 0080's set (K3 rule, one or two quarter turns, plain and keyword columnar, forward and inverse; keyword columnar now read in true key order). Widths 2-48, rows as many as needed (the row key is free, so a repeating row word is a special case). Exact; ten shuffled coppers through the identical search.

## Prediction

On the copper as carved (no move), no width passes all its checks; width 7 has about 14 checks and fails. After moves, consistent settings at every number of checks lie inside the range of the ten shuffled coppers, and no setting with five or more checks survives on K4. Zero candidates.

## Method

1. For each width, assign every known letter its column slot and row slot (by carved place or by message place).
2. Grow a spanning tree over the slots and test every other known letter against it, on both alphabets and both signs.
3. Do this with no move and after each of 0080's moves, in both orders.
4. Count consistent settings by number of checks on K4 and ten shuffled coppers.
5. Print K4's settings with five or more checks, with the slot letters they fix.

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
 "family": "key = column letter of one key + row letter of another on a grid of width 2-48, no move or after/before 0080's moves",
 "distinct_routes": 27754,
 "routes_done": 27754,
 "widths": [
  2,
  48
 ],
 "cases_per_structure": "alphabet std or KRYPTOS x sign +1/-1 = 4",
 "no_move_by_width": {
  "2": {
   "checks": 10,
   "consistent": []
  },
  "3": {
   "checks": 13,
   "consistent": []
  },
  "4": {
   "checks": 13,
   "consistent": []
  },
  "5": {
   "checks": 14,
   "consistent": []
  },
  "6": {
   "checks": 13,
   "consistent": []
  },
  "7": {
   "checks": 14,
   "consistent": []
  },
  "8": {
   "checks": 11,
   "consistent": []
  },
  "9": {
   "checks": 12,
   "consistent": []
  },
  "10": {
   "checks": 11,
   "consistent": []
  },
  "11": {
   "checks": 9,
   "consistent": []
  },
  "12": {
   "checks": 9,
   "consistent": []
  },
  "13": {
   "checks": 8,
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
   "checks": 5,
   "consistent": []
  },
  "17": {
   "checks": 5,
   "consistent": []
  },
  "18": {
   "checks": 6,
   "consistent": []
  },
  "19": {
   "checks": 8,
   "consistent": []
  },
  "20": {
   "checks": 10,
   "consistent": []
  },
  "21": {
   "checks": 10,
   "consistent": []
  },
  "22": {
   "checks": 7,
   "consistent": []
  },
  "23": {
   "checks": 5,
   "consistent": []
  },
  "24": {
   "checks": 3,
   "consistent": []
  },
  "25": {
   "checks": 2,
   "consistent": []
  },
  "31": {
   "checks": 1,
   "consistent": []
  },
  "32": {
   "checks": 1,
   "consistent": []
  },
  "33": {
   "checks": 2,
   "consistent": []
  },
  "34": {
   "checks": 4,
   "consistent": []
  },
  "35": {
   "checks": 5,
   "consistent": []
  },
  "36": {
   "checks": 6,
   "consistent": []
  },
  "37": {
   "checks": 7,
   "consistent": []
  },
  "38": {
   "checks": 8,
   "consistent": []
  },
  "39": {
   "checks": 9,
   "consistent": []
  },
  "40": {
   "checks": 10,
   "consistent": []
  },
  "41": {
   "checks": 10,
   "consistent": []
  },
  "42": {
   "checks": 10,
   "consistent": []
  },
  "43": {
   "checks": 9,
   "consistent": []
  },
  "44": {
   "checks": 8,
   "consistent": []
  },
  "45": {
   "checks": 7,
   "consistent": []
  },
  "46": {
   "checks": 6,
   "consistent": []
  },
  "47": {
   "checks": 5,
   "consistent": []
  },
  "48": {
   "checks": 4,
   "consistent": []
  }
 },
 "structures_with_checks": 2313108,
 "structures_by_checks": {
  "1": 162177,
  "2": 184989,
  "3": 163454,
  "4": 207134,
  "5": 302338,
  "6": 209390,
  "7": 207119,
  "8": 184905,
  "9": 196956,
  "10": 210841,
  "11": 86156,
  "12": 45413,
  "13": 93355,
  "14": 58863,
  "15": 18
 },
 "k4_at_least": {
  "1": 25753,
  "2": 1102,
  "3": 30,
  "4": 4,
  "5": 0,
  "6": 0,
  "7": 0,
  "8": 0
 },
 "controls_at_least": {
  "1": [
   26002,
   26493,
   25550,
   25609,
   25619,
   25843,
   26498,
   25780,
   26510,
   26047
  ],
  "2": [
   1156,
   1140,
   1155,
   1190,
   1081,
   1195,
   1209,
   1009,
   1129,
   1079
  ],
  "3": [
   34,
   32,
   38,
   32,
   28,
   39,
   41,
   30,
   51,
   41
  ],
  "4": [
   2,
   1,
   3,
   0,
   0,
   1,
   1,
   1,
   1,
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
   1
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
 "k4_cases_with_5_or_more_checks": [],
 "n_k4_cases_5_plus": 0,
 "controls": "10 shuffled coppers (seed 87), identical search"
}
```

Notes: No move: widths consistent on K4: none (width 7 has 14 checks). With moves: 27,754 routes x widths 2-48 x 2 orders, 2,313,108 structures x 4 cases. K4 consistent with >= c checks, c = 1..8: [25753, 1102, 30, 4, 0, 0, 0, 0]; controls max [26510, 1209, 51, 6, 1, 0, 0, 0], min [25550, 1009, 28, 0, 0, 0, 0, 0]. Levels outside the control range: []. K4 cases with 5+ checks: 0.


