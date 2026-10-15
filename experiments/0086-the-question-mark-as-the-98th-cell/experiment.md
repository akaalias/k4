# 0086-the-question-mark-as-the-98th-cell: The ? before OBKR as the 98th letter: a full 7 x 14 grid, turned so the ? comes out first, with an autokey or a repeating key

**Family:** 6-transposition-then-tableau  
**Parent:** 0082-where-the-blanks-go-in-the-grid  
**Decision:** reverted  
**Run:** 2026-10-15T16:31:11+00:00, 432.6 s, status ran  
**Time by phase:** test 0 s, run 433 s, record 0 s

## In plain words

On the sculpture a question mark sits just before K4. Counted with it, K4 has 98 symbols, and 98 fills a grid of 7 by 14 exactly, the way the third message's 336 letters filled its grid. Perhaps the question mark was part of the message, the grid was turned so that it came out first, and the letters were then keyed. We try every grid and every way of reading it out that puts the question mark in front, with a repeating secret word or an autokey, and the same on ten scrambled coppers.

## Walkthrough, by hand

1. Put a ? at the end of the message: 98 symbols.
2. Write them in rows of 14: seven full rows, no blank cell.
3. Read the columns from right to left, each from the bottom up. The first cell read is the last one, the ?, so it is carved first, as on the sculpture.
4. Place 22, the E of EAST, is in row 1, column 7. Columns 13 to 8 give 42 symbols; column 7 read from the bottom reaches row 1 at its sixth cell, symbol 48, which is carved letter 47 once the ? is set aside.
5. Key the 97 letters with a repeating key or an autokey; each known letter and the copper letter where it landed tie the key, and the ties must agree.
6. Repeat for every grid width, reading corner, second grid, K3's rule on 98, every order of seven columns, every key, and ten scrambled coppers.

## Worked example (generated)

```
98 cells in rows of 14 (7 rows, full), read right to left, each column bottom-up: the first cell read is the last one,
so the ? must be the last symbol of the message (q = 97) to be carved first.

? position in the message: 97
place  letter  row  column  carved place
   22       E    1       7            47  (Z)
   23       A    1       8            40  (S)
   64       B    4       7            44  (S)
   65       E    4       8            37  (W)
   74       K    5       3            71  (Z)
```

## Lineage

Inherits from 0082-where-the-blanks-go-in-the-grid. What changed: With the carved ? counted, K4 has 98 symbols, which fill a 7 x 14 grid exactly. Here the message plus a ? somewhere in it is written into a grid of 98 cells and read out from any corner, once or twice, by K3's rule on 98, or by a seven-column shuffle in any of its 5,040 orders; the reading must bring the ? to the front, where it is carved. The 97 letters are then keyed by a repeating key, or by the plaintext or ciphertext autokey, which the padded-grid searches never paired with the 98-cell grid.

## Hypothesis (domain expert)

Type 2 of directions.md, the prior-work database's seven-based sub-variant 2 ('a 7x14 grid of 98 (with ?) under a K3-style rotation plus a non-periodic key (autokey, progressive); padded rotations were tested only with periodic keys', nitsuah). Clues C18(b) (Scheidt 2004-5, 'I think there are 98 characters left'; a 98-character working text including ?), C17(c) (the ? counts), C1(a) and C2(a) (the K3 move; K3's 336 letters fill 24 x 14 and 8 x 42 exactly, so a full grid is Sanborn's habit), and the width-7 doublet column (0056). Model: the 97 plaintext letters with a ? inserted at some symbol position q (98 symbols); a move T on 98 cells; the carved text is ? followed by the 97 letters, so T must send q to position 0, which fixes q for each T. Moves: one grid of width 2-97 (ragged bottom row) read from any of four corners (columns left to right bottom-up, right to left top-down, left to right top-down, right to left bottom-up), forward and inverse; two such grids at every width pair and reading pair, forward and inverse (repeating key only); K3's rule a + b i mod 98 for b prime to 98; seven-column shuffles in all 5,040 orders, forward and inverse. Keys on the 97 letters: periodic tableau key 1-26 after the move (slot = carved letter position mod p), before it (slot = plaintext letter position mod p), or before it with the ? taking a slot (slot = symbol position mod p), 8 classes; plaintext and ciphertext autokey, lags 1-96, one alphabet throughout, three modes, after or before the move (not with two-grid moves at widths that do not divide 98). Exact; ten shuffled coppers (the 97 letters shuffled, the ? kept first).

## Prediction

Nothing live below period 22 for the repeating keys beyond the shuffled-copper rate; no autokey setting passes five checks; counts at every level inside the control range, give or take the spread at the lowest levels. Zero candidates.

## Method

1. Build every move on 98 cells and find the ? position it brings to the front.
2. Turn it into a reordering of the 97 letters.
3. Test a repeating key of length 1-26 in three placements by the forced-letter slots.
4. For the one-grid moves, full two-grid moves, K3's rule and the seven-column shuffles, test the plaintext and ciphertext autokeys at every lag on either side.
5. Count survivors on K4 and ten shuffled coppers; list K4's survivors below period 20 or with four or more checks, with the ? position.

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
 "family": "98 cells with the ? sent to the front: grids, K3 rule mod 98, seven-column shuffles; periodic key or autokey on the 97 letters",
 "distinct_routes": 300651,
 "routes_with_autokey": 14946,
 "stopped_at": null,
 "periodic": {
  "k4_live_by_period": {
   "A": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    1,
    173,
    635,
    6538,
    15005,
    104261
   ],
   "B": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    154,
    93766
   ],
   "B98": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    117,
    61040
   ]
  },
  "controls_min": {
   "A": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    17,
    480,
    4405,
    14932,
    102542
   ],
   "B": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    101,
    91601
   ],
   "B98": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    65,
    58655
   ]
  },
  "controls_max": {
   "A": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    7,
    12,
    328,
    692,
    6268,
    15133,
    104546
   ],
   "B": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    1,
    201,
    94039
   ],
   "B98": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    119,
    61214
   ]
  },
  "periods_outside_control_range": {
   "A": [
    24
   ],
   "B": [],
   "B98": []
  },
  "k4_live_below_20": [],
  "n_k4_live_below_20": 0,
  "controls_live_below_20": {
   "A": [
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
   "B": [
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
   "B98": [
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
 },
 "autokey": {
  "by_kind_and_order": {
   "ptak order A": {
    "k4_at_least_c": {
     "1": 26064,
     "2": 1568,
     "3": 72,
     "4": 0,
     "5": 0,
     "6": 0
    },
    "controls_at_least_c": {
     "1": [
      27558,
      21867,
      25785,
      24373,
      24887,
      23735,
      25643,
      23935,
      26301,
      23022
     ],
     "2": [
      1509,
      690,
      1279,
      1049,
      730,
      1379,
      977,
      685,
      773,
      662
     ],
     "3": [
      26,
      33,
      25,
      27,
      37,
      22,
      26,
      34,
      17,
      27
     ],
     "4": [
      1,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      1,
      2
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
     ]
    }
   },
   "ptak order B": {
    "k4_at_least_c": {
     "1": 8395,
     "2": 85,
     "3": 12,
     "4": 0,
     "5": 0,
     "6": 0
    },
    "controls_at_least_c": {
     "1": [
      10755,
      14739,
      10335,
      10705,
      14215,
      11017,
      10617,
      10516,
      10965,
      11791
     ],
     "2": [
      88,
      74,
      262,
      189,
      194,
      91,
      88,
      71,
      69,
      433
     ],
     "3": [
      7,
      12,
      81,
      2,
      9,
      28,
      8,
      10,
      3,
      5
     ],
     "4": [
      1,
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
     ]
    }
   },
   "ctak order A": {
    "k4_at_least_c": {
     "1": 11767,
     "2": 184,
     "3": 2,
     "4": 0,
     "5": 0,
     "6": 0
    },
    "controls_at_least_c": {
     "1": [
      10467,
      9048,
      12533,
      11096,
      10059,
      8188,
      12812,
      7723,
      13680,
      11374
     ],
     "2": [
      428,
      249,
      1222,
      720,
      195,
      222,
      1124,
      381,
      342,
      1382
     ],
     "3": [
      15,
      14,
      5,
      6,
      6,
      10,
      52,
      6,
      0,
      6
     ],
     "4": [
      0,
      0,
      1,
      0,
      0,
      1,
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
     ]
    }
   },
   "ctak order B": {
    "k4_at_least_c": {
     "1": 3444,
     "2": 186,
     "3": 2,
     "4": 0,
     "5": 0,
     "6": 0
    },
    "controls_at_least_c": {
     "1": [
      3507,
      3394,
      4131,
      2203,
      3571,
      4588,
      4103,
      3681,
      3589,
      4291
     ],
     "2": [
      107,
      53,
      218,
      62,
      107,
      82,
      119,
      78,
      174,
      98
     ],
     "3": [
      8,
      1,
      3,
      2,
      2,
      10,
      10,
      2,
      102,
      1
     ],
     "4": [
      0,
      0,
      0,
      0,
      0,
      0,
      1,
      1,
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
     ]
    }
   }
  },
  "levels_outside_control_range": [
   "ptak A: [2, 3]",
   "ptak B: [1]",
   "ctak A: [2]"
  ],
  "k4_settings_with_4_plus_checks": [],
  "n_k4_4_plus": 0
 },
 "orders": {
  "A": "move, then key (slot = carved letter position)",
  "B": "key, then move (slot = letter position)",
  "B98": "key, then move, the ? taking a key slot (slot = symbol position)"
 },
 "controls": "10 shuffled coppers (seed 86), the ? kept in front, identical search"
}
```

Notes: 300,651 distinct 98-cell routes (14,946 with autokeys). Periodic: K4 live below 20: 0; controls {'A': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'B': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'B98': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}; periods outside the control range {'A': [24], 'B': [], 'B98': []}. Autokey: ptak order A: K4 >=1..6 [26064, 1568, 72, 0, 0, 0], controls max [27558, 1509, 37, 2, 0, 0]; ptak order B: K4 >=1..6 [8395, 85, 12, 0, 0, 0], controls max [14739, 433, 81, 1, 0, 0]; ctak order A: K4 >=1..6 [11767, 184, 2, 0, 0, 0], controls max [13680, 1382, 52, 1, 0, 0]; ctak order B: K4 >=1..6 [3444, 186, 2, 0, 0, 0], controls max [4588, 218, 102, 1, 0, 0]. Outside: ['ptak A: [2, 3]', 'ptak B: [1]', 'ctak A: [2]']. K4 autokey settings with 4+ checks: 0.


