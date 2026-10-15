# 0085-true-keyword-columnar-rerun: Column shuffles keyed by the puzzle's words, read the right way round this time: once or twice, with a repeating key or an autokey

**Family:** 6-transposition-then-tableau  
**Parent:** 0026-double-keyed-columnar-then-tableau  
**Decision:** reverted  
**Run:** 2026-10-15T16:18:54+00:00, 718.8 s, status ran  
**Time by phase:** test 0 s, run 719 s, record 0 s

## In plain words

A column shuffle keyed by a word writes the message in rows under the word and reads the columns in the alphabetical order of its letters. Our earlier experiments made a slip: they read the columns in a related but different order, so the true keyed shuffles were never tested. This experiment repeats the tests with the right order: every puzzle word as the key, used once or twice, followed or preceded by a repeating secret word on the table, or by an autokey, where the message feeds its own key.

## Walkthrough, by hand

1. Write the message in rows of 7 under KRYPTOS. The key letters rank K 0, R 3, Y 6, P 2, T 5, O 1, S 4.
2. Read the columns in rank order: column 0 (K), then 5 (O), 3 (P), 1 (R), 6 (S), 4 (T), 2 (Y). The earlier records read 0, 3, 6, 2, 5, 1, 4 instead, the ranks themselves.
3. Place 23, the A of EAST, is in row 3 of column 1. Columns 0, 5 and 3 hold 14 letters each, so it becomes letter 46; the earlier reading put it at 73.
4. Under a repeating key on the table, the known letter and the copper letter at its new place force one key letter; two known letters whose new places differ by a multiple of the key length must force the same one.
5. Under an autokey, two known letters one lag apart are tied through the copper letters between them.
6. Repeat for every word key, once or twice, every key length and lag, both orders, and ten scrambled coppers.

## Worked example (generated)

```
KRYPTOS as a column key: K R Y P T O S ranks 0 3 6 2 5 1 4, so the columns are read 0 5 3 1 6 4 2
(the earlier records read 0 3 6 2 5 1 4, the ranks themselves)

place  letter  column  lands at (true)  lands at (earlier)
   22       E       0                4                   4
   23       A       1               46                  73
   24       S       2               87                  45
   25       T       3               32                  18
   64       B       0               10                  10
```

## Lineage

Inherits from 0026-double-keyed-columnar-then-tableau. What changed: Issue #26: ten records (0006-0081) passed a keyword's rank list as the reading sequence, so their keyed column shuffles read the columns in the inverse order. This reruns keyed columnar with the true keyword reading (columns in the alphabetical order of the key letters), with repeated letters dropped and on the whole word with ties left to right, once (both directions) or twice (every ordered pair), against a repeating key of length 1-26 before or after, and against the plaintext and ciphertext autokeys at every lag in both orders.

## Hypothesis (domain expert)

Correction run for issue #26, filed during type 2 of directions.md. The bounds it restores: keyed columnar then tableau (0006, 0016), tableau then keyed columnar (0007, 0058), keyed double columnar (0026), keyed columnar with ciphertext autokey (0063), and the keyed-columnar subsets of 0080 and 0081. Clues C1(a) (02-sanborn-said.md, CNN 2005, 'double matrixes'), C8(a) (KRYPTOS as a transposition key for K4, as the NSA read it for K3), C7(a) (K1-K3 words as keys). Key words: data/vocabulary.txt, the K1-K3 plaintext words of 3-20 letters, and the C13/C14 words; each gives up to two sequences (repeats dropped, as kryptos.alphabets.numeric_order does; or the whole word with ties left to right), deduplicated. Routes: each sequence once, columnar encryption or its inverse; every ordered pair of sequences, encryption twice. Keys: (i) periodic tableau key 1-26 after the move (slot = landing place mod p) or before it (slot = place mod p), 8 classes, live if no slot holds two different forced letters; (ii) plaintext autokey and (iii) ciphertext autokey at lags 1-96, one alphabet throughout (standard or KRYPTOS), three modes, autokey after the move (order A) or before it (order B), checked exactly as in 0081. Ten shuffled coppers through the identical search.

## Prediction

As for the inverse readings: nothing live below period 22 for the repeating key beyond the shuffled-copper rate; no autokey setting passes five checks; counts at every level inside the control range, give or take the spread at the lowest levels. Zero candidates.

## Method

1. Build the keyword sequences and the single and double routes; skip repeats.
2. For each route, test a repeating key of length 1-26 on either side by the forced-letter slots.
3. For each route, test the plaintext and ciphertext autokeys at every lag on either side by walking the chains between known letters.
4. Count survivors by period or number of checks on K4 and ten shuffled coppers.
5. List K4's survivors below period 20 or with four or more checks.

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
 "family": "true keyword columnar (issue #26), once or twice, with a periodic key 1-26 or plaintext/ciphertext autokey, both orders",
 "keyword_sequences": 201,
 "distinct_routes": 40771,
 "routes_done": 40771,
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
    0,
    1,
    7,
    74,
    23,
    482
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
    22,
    12924
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
    0,
    1,
    67,
    15,
    469
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
    14,
    12165
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
    0,
    0,
    4,
    8,
    90,
    45,
    489
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
    24,
    12923
   ]
  },
  "periods_outside_control_range": {
   "A": [],
   "B": [
    26
   ]
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
   ]
  }
 },
 "autokey": {
  "by_kind_and_order": {
   "ptak order A": {
    "k4_at_least_c": {
     "1": 114744,
     "2": 4018,
     "3": 135,
     "4": 3,
     "5": 0,
     "6": 0
    },
    "controls_at_least_c": {
     "1": [
      117417,
      116458,
      113926,
      114585,
      117225,
      115933,
      112456,
      115523,
      118127,
      111861
     ],
     "2": [
      3959,
      3906,
      3873,
      3979,
      4110,
      4083,
      3851,
      3979,
      3879,
      3855
     ],
     "3": [
      116,
      149,
      118,
      98,
      138,
      135,
      113,
      96,
      135,
      123
     ],
     "4": [
      2,
      12,
      4,
      4,
      4,
      5,
      5,
      4,
      4,
      7
     ],
     "5": [
      0,
      1,
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
     "1": 31166,
     "2": 585,
     "3": 37,
     "4": 0,
     "5": 0,
     "6": 0
    },
    "controls_at_least_c": {
     "1": [
      31004,
      30076,
      29697,
      31389,
      31456,
      32560,
      30384,
      32001,
      30752,
      31152
     ],
     "2": [
      645,
      695,
      564,
      674,
      670,
      608,
      526,
      539,
      603,
      557
     ],
     "3": [
      48,
      53,
      44,
      58,
      56,
      55,
      35,
      41,
      63,
      49
     ],
     "4": [
      1,
      0,
      0,
      0,
      2,
      1,
      1,
      0,
      1,
      1
     ],
     "5": [
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
     "1": 31451,
     "2": 1132,
     "3": 50,
     "4": 0,
     "5": 0,
     "6": 0
    },
    "controls_at_least_c": {
     "1": [
      34096,
      29577,
      35805,
      34693,
      29560,
      30097,
      33605,
      30298,
      37509,
      36289
     ],
     "2": [
      1720,
      1685,
      1510,
      1404,
      1736,
      1511,
      1546,
      1324,
      2109,
      1898
     ],
     "3": [
      53,
      68,
      25,
      44,
      64,
      69,
      57,
      76,
      46,
      67
     ],
     "4": [
      3,
      0,
      1,
      2,
      3,
      0,
      3,
      0,
      4,
      0
     ],
     "5": [
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
     "1": 9627,
     "2": 369,
     "3": 11,
     "4": 0,
     "5": 0,
     "6": 0
    },
    "controls_at_least_c": {
     "1": [
      9929,
      9909,
      9879,
      10091,
      9815,
      9835,
      9457,
      9782,
      10080,
      9836
     ],
     "2": [
      384,
      390,
      379,
      446,
      443,
      347,
      339,
      361,
      347,
      405
     ],
     "3": [
      14,
      23,
      13,
      17,
      16,
      12,
      12,
      13,
      15,
      17
     ],
     "4": [
      1,
      1,
      0,
      2,
      1,
      4,
      0,
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
   "ctak A: [2]",
   "ctak B: [3]"
  ],
  "k4_settings_with_4_plus_checks": [
   {
    "kind": "plaintext autokey",
    "order": "A",
    "route": "FOUR (repeats dropped) then ABOUT (repeats dropped)",
    "alphabet": "kry",
    "mode": "vig",
    "lag": 50,
    "checks": 4
   },
   {
    "kind": "plaintext autokey",
    "order": "A",
    "route": "INVISIBLE (repeats dropped) then SCHEIDT (repeats dropped)",
    "alphabet": "kry",
    "mode": "vig",
    "lag": 42,
    "checks": 4
   },
   {
    "kind": "plaintext autokey",
    "order": "A",
    "route": "INVISIBLE (repeats dropped) then UNDERGROUND (repeats dropped)",
    "alphabet": "kry",
    "mode": "vig",
    "lag": 42,
    "checks": 4
   }
  ],
  "n_k4_4_plus": 3
 },
 "controls": "10 shuffled coppers (seed 85), identical search"
}
```

Notes: 40,771 distinct routes from 201 keyword sequences. Periodic: K4 live below 20: 0; controls {'A': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'B': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}; periods outside the control range {'A': [], 'B': [26]}. Autokey: ptak order A: K4 >=1..6 [114744, 4018, 135, 3, 0, 0], controls max [118127, 4110, 149, 12, 1, 0]; ptak order B: K4 >=1..6 [31166, 585, 37, 0, 0, 0], controls max [32560, 695, 63, 2, 1, 0]; ctak order A: K4 >=1..6 [31451, 1132, 50, 0, 0, 0], controls max [37509, 2109, 76, 4, 1, 0]; ctak order B: K4 >=1..6 [9627, 369, 11, 0, 0, 0], controls max [10091, 446, 23, 4, 0, 0]. Outside: ['ctak A: [2]', 'ctak B: [3]']. K4 autokey settings with 4+ checks: 3.


