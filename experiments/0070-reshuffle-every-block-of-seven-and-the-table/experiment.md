# 0070-reshuffle-every-block-of-seven-and-the-table: Every block of seven letters reshuffled the same way, before or after the table

**Family:** 6-transposition-then-tableau  
**Parent:** 0006-columnar-then-tableau-period-survival  
**Decision:** reverted  
**Run:** 2026-10-15T13:17:18+00:00, 41.6 s, status ran  
**Time by phase:** design 37 s, implement 0 s, test 10 s, run 42 s, record 0 s

## In plain words

Five of the six doubled letters fall in the same column when the copper is written in rows of seven. One simple way to leave such a trace is to write the message in rows of seven and shuffle the letters inside every row in the same order, then encipher with a repeating secret word, or the other way round. There are only 5,040 orders for seven letters, so we try them all with every length of secret word up to 52 and see whether any fits the 24 known letters better than scrambled coppers do.

## Walkthrough, by hand

1. Take the order that reverses every row of seven, and order A: encipher first, then reverse each row.
2. Place 22 is the first letter of its row, so after reversing it is carved at place 28, P.
3. Known E over carved P, on the sculpture's alphabet with Vigenere, needs key letter M, in slot 0 of a 7-letter word.
4. Place 29 is also first in its row, carved at place 35, O; known T over O needs R, also slot 0.
5. M and R disagree, so this order with a 7-letter word is dead.
6. Repeat for all 5,040 orders, both ways round, every word length and way of using the table.

## Worked example (generated)

```
every row of seven reversed, after a 7-letter key; sculpture's alphabet, Vigenere

place  carved at  carved  known  key  slot
   22        28       P      E    M     0
   29        35       O      T    R     0
   23        27       Q      A    G     1
   30        34       S      H    M     1
```

## Lineage

Inherits from 0006-columnar-then-tableau-period-survival. What changed: The copper's doublets line up in sevens. Experiment 6 tested columnar routes, which read a grid down its columns. This tests the other way a grid of seven can be used: each row of seven letters reshuffled by the same order and read across, before or after a repeating secret word on the table, for all 5,040 orders.

## Hypothesis (domain expert)

Family 6 re-entered with a stated reason (it had rested after eleven reverts): the width-7 doublet column (0056, real at corrected p 0.005) is a period-7 positional trace, and the one width-7 transposition not yet tested is the block permutation, write in rows of 7 and permute the letters within every row by one fixed order (a 'matrix' in the C1(a) sense; also the one-row-at-a-time reading of C27(a)), which keeps each letter in its row of seven. 0006 covered columnar read-outs only. Orders: (A) periodic tableau then block permutation, (B) block permutation then periodic tableau. All 5,040 permutations of 7 (the last block of 6 keeps the relative order of its letters), periods 1-52, plain and cipher alphabets standard or KRYPTOS, Vigenere or Beaufort (8 classes; the key alphabet drops out of a consistency test, and variant Beaufort equals Vigenere here). A (permutation, class, period) survives if every key slot's forced values agree. Ten shuffled coppers through the same sweep. Clue entries: C1(a), C11a ('interval 7'), C27(a).

## Prediction

In both orders, no permutation makes any period up to 26 consistent under any class, except where the shuffled coppers do the same at a similar rate; periods 27-29 stay consistent as always. No period is singled out at multiples of 7. Zero candidates pass.

## Method

1. For each order of seven, map each known place to the carved place it lands on.
2. For each class, compute the key value each known letter forces, and its slot: the plaintext place in order A, the carved place in order B.
3. For each period up to 52, check that each slot's values agree.
4. Count consistent cases per period, and the smallest consistent period.
5. Repeat on ten shuffled coppers.

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
 "family": "block-of-7 permutation before or after a periodic tableau",
 "permutations": 5040,
 "periods": "1-52",
 "classes": 8,
 "cases": 4193280,
 "complete": true,
 "k4_consistent_by_period": {
  "A": {
   "26": 1800,
   "27": 40320,
   "28": 40320,
   "29": 40320,
   "30": 960,
   "31": 72,
   "32": 2,
   "51": 36,
   "52": 1800
  },
  "B": {
   "25": 2,
   "26": 212,
   "27": 6702,
   "28": 40320,
   "29": 6600,
   "30": 546,
   "31": 35,
   "32": 3,
   "50": 2,
   "51": 12,
   "52": 212
  }
 },
 "k4_smallest_period_le26": {
  "A": [
   {
    "perm": [
     0,
     1,
     2,
     4,
     3,
     5,
     6
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     1,
     2,
     4,
     3,
     6,
     5
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     1,
     2,
     5,
     3,
     4,
     6
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     1,
     2,
     5,
     3,
     6,
     4
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     1,
     2,
     6,
     3,
     4,
     5
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     1,
     2,
     6,
     3,
     5,
     4
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     1,
     4,
     2,
     3,
     5,
     6
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     1,
     4,
     2,
     3,
     6,
     5
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     1,
     4,
     5,
     3,
     2,
     6
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     1,
     4,
     5,
     3,
     6,
     2
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     1,
     4,
     6,
     3,
     2,
     5
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     1,
     4,
     6,
     3,
     5,
     2
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     1,
     5,
     2,
     3,
     4,
     6
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     1,
     5,
     2,
     3,
     6,
     4
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     1,
     5,
     4,
     3,
     2,
     6
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     1,
     5,
     4,
     3,
     6,
     2
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     1,
     5,
     6,
     3,
     2,
     4
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     1,
     5,
     6,
     3,
     4,
     2
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     1,
     6,
     2,
     3,
     4,
     5
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     1,
     6,
     2,
     3,
     5,
     4
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     1,
     6,
     4,
     3,
     2,
     5
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     1,
     6,
     4,
     3,
     5,
     2
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     1,
     6,
     5,
     3,
     2,
     4
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     1,
     6,
     5,
     3,
     4,
     2
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     2,
     1,
     4,
     3,
     5,
     6
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     2,
     1,
     4,
     3,
     6,
     5
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     2,
     1,
     5,
     3,
     4,
     6
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     2,
     1,
     5,
     3,
     6,
     4
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     2,
     1,
     6,
     3,
     4,
     5
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     2,
     1,
     6,
     3,
     5,
     4
    ],
    "class": "kry/kry/beau",
    "period": 26
   }
  ],
  "B": [
   {
    "perm": [
     0,
     1,
     3,
     5,
     4,
     6,
     2
    ],
    "class": "std/kry/vig",
    "period": 26
   },
   {
    "perm": [
     0,
     1,
     3,
     5,
     6,
     4,
     2
    ],
    "class": "std/kry/vig",
    "period": 26
   },
   {
    "perm": [
     0,
     1,
     3,
     6,
     4,
     5,
     2
    ],
    "class": "kry/std/vig",
    "period": 26
   },
   {
    "perm": [
     0,
     1,
     3,
     6,
     5,
     4,
     2
    ],
    "class": "kry/std/vig",
    "period": 26
   },
   {
    "perm": [
     0,
     2,
     1,
     4,
     3,
     5,
     6
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     2,
     1,
     4,
     3,
     6,
     5
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     2,
     1,
     5,
     3,
     4,
     6
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     2,
     1,
     5,
     3,
     6,
     4
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     2,
     1,
     6,
     3,
     4,
     5
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     2,
     1,
     6,
     3,
     5,
     4
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     2,
     3,
     4,
     5,
     6,
     1
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     2,
     3,
     4,
     6,
     5,
     1
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     2,
     5,
     4,
     3,
     6,
     1
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     2,
     6,
     4,
     3,
     5,
     1
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     3,
     1,
     5,
     4,
     6,
     2
    ],
    "class": "std/kry/vig",
    "period": 26
   },
   {
    "perm": [
     0,
     3,
     1,
     5,
     6,
     4,
     2
    ],
    "class": "std/kry/vig",
    "period": 26
   },
   {
    "perm": [
     0,
     3,
     1,
     6,
     4,
     5,
     2
    ],
    "class": "kry/std/vig",
    "period": 26
   },
   {
    "perm": [
     0,
     3,
     1,
     6,
     5,
     4,
     2
    ],
    "class": "kry/std/vig",
    "period": 26
   },
   {
    "perm": [
     0,
     3,
     2,
     4,
     5,
     6,
     1
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     3,
     2,
     4,
     6,
     5,
     1
    ],
    "class": "kry/kry/beau",
    "period": 26
   },
   {
    "perm": [
     0,
     5,
     6,
     3,
     1,
     4,
     2
    ],
    "class": "kry/kry/vig",
    "period": 25
   },
   {
    "perm": [
     0,
     6,
     1,
     3,
     4,
     2,
     5
    ],
    "class": "kry/std/vig",
    "period": 25
   },
   {
    "perm": [
     1,
     0,
     2,
     4,
     3,
     5,
     6
    ],
    "class": "std/kry/vig",
    "period": 26
   },
   {
    "perm": [
     1,
     0,
     2,
     4,
     3,
     5,
     6
    ],
    "class": "kry/std/beau",
    "period": 26
   },
   {
    "perm": [
     1,
     0,
     2,
     4,
     3,
     6,
     5
    ],
    "class": "std/kry/vig",
    "period": 26
   },
   {
    "perm": [
     1,
     0,
     2,
     4,
     3,
     6,
     5
    ],
    "class": "kry/std/beau",
    "period": 26
   },
   {
    "perm": [
     1,
     0,
     2,
     5,
     3,
     4,
     6
    ],
    "class": "std/kry/vig",
    "period": 26
   },
   {
    "perm": [
     1,
     0,
     2,
     5,
     3,
     4,
     6
    ],
    "class": "kry/std/beau",
    "period": 26
   },
   {
    "perm": [
     1,
     0,
     2,
     5,
     3,
     6,
     4
    ],
    "class": "std/kry/vig",
    "period": 26
   },
   {
    "perm": [
     1,
     0,
     2,
     5,
     3,
     6,
     4
    ],
    "class": "kry/std/beau",
    "period": 26
   }
  ]
 },
 "k4_le26_counts": {
  "A": 1800,
  "B": 214
 },
 "controls": [
  {
   "le26": {
    "A": 1686,
    "B": 172
   },
   "complete": true,
   "consistent_by_period": {
    "A": {
     "25": 6,
     "26": 1680,
     "27": 40320,
     "28": 40320,
     "29": 40320,
     "30": 2280,
     "31": 48,
     "32": 3,
     "50": 6,
     "51": 48,
     "52": 1680
    },
    "B": {
     "25": 2,
     "26": 170,
     "27": 6678,
     "28": 40320,
     "29": 7320,
     "30": 504,
     "31": 26,
     "32": 1,
     "50": 2,
     "51": 6,
     "52": 170
    }
   }
  },
  {
   "le26": {
    "A": 2046,
    "B": 221
   },
   "complete": true,
   "consistent_by_period": {
    "A": {
     "25": 18,
     "26": 2040,
     "27": 40320,
     "28": 40320,
     "29": 40320,
     "30": 1320,
     "31": 66,
     "50": 18,
     "51": 90,
     "52": 2040
    },
    "B": {
     "25": 1,
     "26": 220,
     "27": 6528,
     "28": 40320,
     "29": 6240,
     "30": 504,
     "31": 12,
     "32": 2,
     "50": 1,
     "51": 26,
     "52": 220
    }
   }
  },
  {
   "le26": {
    "A": 1692,
    "B": 248
   },
   "complete": true,
   "consistent_by_period": {
    "A": {
     "25": 12,
     "26": 1680,
     "27": 40320,
     "28": 40320,
     "29": 40320,
     "30": 1800,
     "31": 48,
     "50": 12,
     "51": 42,
     "52": 1680
    },
    "B": {
     "25": 2,
     "26": 246,
     "27": 6564,
     "28": 40320,
     "29": 7680,
     "30": 402,
     "31": 16,
     "50": 2,
     "51": 20,
     "52": 246
    }
   }
  },
  {
   "le26": {
    "A": 1680,
    "B": 128
   },
   "complete": true,
   "consistent_by_period": {
    "A": {
     "26": 1680,
     "27": 40320,
     "28": 40320,
     "29": 40320,
     "30": 1200,
     "31": 24,
     "32": 2,
     "51": 24,
     "52": 1680
    },
    "B": {
     "26": 128,
     "27": 7074,
     "28": 40320,
     "29": 6240,
     "30": 678,
     "31": 19,
     "51": 17,
     "52": 128
    }
   }
  },
  {
   "le26": {
    "A": 2040,
    "B": 278
   },
   "complete": true,
   "consistent_by_period": {
    "A": {
     "26": 2040,
     "27": 40320,
     "28": 40320,
     "29": 40320,
     "30": 1560,
     "31": 60,
     "32": 1,
     "33": 1,
     "51": 78,
     "52": 2040
    },
    "B": {
     "25": 2,
     "26": 276,
     "27": 6660,
     "28": 40320,
     "29": 6240,
     "30": 552,
     "31": 16,
     "32": 2,
     "50": 2,
     "51": 22,
     "52": 276
    }
   }
  },
  {
   "le26": {
    "A": 2052,
    "B": 154
   },
   "complete": true,
   "consistent_by_period": {
    "A": {
     "25": 12,
     "26": 2040,
     "27": 40320,
     "28": 40320,
     "29": 40320,
     "30": 1800,
     "31": 54,
     "32": 1,
     "33": 1,
     "50": 12,
     "51": 78,
     "52": 2040
    },
    "B": {
     "25": 1,
     "26": 153,
     "27": 6546,
     "28": 40320,
     "29": 7440,
     "30": 480,
     "31": 19,
     "50": 1,
     "51": 36,
     "52": 153
    }
   }
  },
  {
   "le26": {
    "A": 2040,
    "B": 172
   },
   "complete": true,
   "consistent_by_period": {
    "A": {
     "26": 2040,
     "27": 40320,
     "28": 40320,
     "29": 40320,
     "30": 1440,
     "31": 114,
     "32": 6,
     "51": 60,
     "52": 2040
    },
    "B": {
     "26": 172,
     "27": 6438,
     "28": 40320,
     "29": 7320,
     "30": 654,
     "31": 10,
     "32": 2,
     "51": 22,
     "52": 172
    }
   }
  },
  {
   "le26": {
    "A": 2172,
    "B": 193
   },
   "complete": true,
   "consistent_by_period": {
    "A": {
     "25": 12,
     "26": 2160,
     "27": 40320,
     "28": 40320,
     "29": 40320,
     "30": 1080,
     "31": 48,
     "32": 2,
     "50": 12,
     "51": 114,
     "52": 2160
    },
    "B": {
     "25": 2,
     "26": 191,
     "27": 6696,
     "28": 40320,
     "29": 7440,
     "30": 516,
     "31": 38,
     "32": 1,
     "33": 1,
     "50": 2,
     "51": 32,
     "52": 191
    }
   }
  },
  {
   "le26": {
    "A": 1560,
    "B": 177
   },
   "complete": true,
   "consistent_by_period": {
    "A": {
     "26": 1560,
     "27": 40320,
     "28": 40320,
     "29": 40320,
     "30": 2400,
     "32": 2,
     "51": 48,
     "52": 1560
    },
    "B": {
     "25": 1,
     "26": 176,
     "27": 6444,
     "28": 40320,
     "29": 6960,
     "30": 612,
     "31": 25,
     "32": 1,
     "50": 1,
     "51": 24,
     "52": 176
    }
   }
  },
  {
   "le26": {
    "A": 1206,
    "B": 229
   },
   "complete": true,
   "consistent_by_period": {
    "A": {
     "25": 6,
     "26": 1200,
     "27": 40320,
     "28": 40320,
     "29": 40320,
     "30": 1080,
     "31": 54,
     "32": 5,
     "50": 6,
     "51": 42,
     "52": 1200
    },
    "B": {
     "25": 3,
     "26": 226,
     "27": 6996,
     "28": 40320,
     "29": 7320,
     "30": 570,
     "31": 28,
     "32": 2,
     "50": 3,
     "51": 26,
     "52": 226
    }
   }
  }
 ]
}
```

Notes: 4,193,280 cases (complete). Cases whose smallest consistent period is 26 or less: K4 A 1800, B 214; controls A [1686, 2046, 1692, 1680, 2040, 2052, 2040, 2172, 1560, 1206], B [172, 221, 248, 128, 278, 154, 172, 193, 177, 229].


