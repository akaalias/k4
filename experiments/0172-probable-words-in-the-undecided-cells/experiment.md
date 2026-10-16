# 0172-probable-words-in-the-undecided-cells: F12.6: Stein's breakthrough, probable words: common English and K1-K3 words placed at every position in the free-alphabet cells the known letters leave undecided, decided exactly

**Family:** 12-steins-way  
**Parent:** 0123-two-free-alphabets-exact-at-every-key-length  
**Decision:** reverted  
**Run:** 2026-10-16T23:05:57+00:00, 1737.0 s, status ran  
**Time by phase:** unattributed 58 s, run 1737 s, record 0 s

## In plain words

Stein's breakthrough was guessing likely words, THE and then KNOW, and seeing whether the cipher allowed them. For the cipher settings the 24 known letters cannot decide, we try sixty likely words at every position: each guess adds more known letters, and most guesses become impossible. If the carved text allowed many more guesses than scrambled copies do, that setting would deserve a closer look.

## Walkthrough, by hand

1. Take one scrambled alphabet with a 23-letter key, the Beaufort way: the 24 known letters fit.
2. Guess that THE stands at places 1-3: three more letters are known.
3. Each new letter adds an equation (carved place + message place = key value of its slot); decide again whether any alphabet and key satisfy them all.
4. Try THE at every place, then the other words; count the guesses that survive.
5. Do the same on scrambled copies that also fit the cell.

## Worked example (generated)

```
one scrambled alphabet, Beaufort form, key length 23: THE guessed at places 1-3

place 1: carved O, guessed T, slot 0: place(O) + place(T) = key value of slot 0
place 2: carved B, guessed H, slot 1: place(B) + place(H) = key value of slot 1
place 3: carved K, guessed E, slot 2: place(K) + place(E) = key value of slot 2
with the 24 known letters, 27 equations: decided exactly; repeated for every word and place
```

## Lineage

Inherits from 0123-two-free-alphabets-exact-at-every-key-length. What changed: F12.6. Stein broke K2 by guessing THE, then KNOW, and checking each guess against the cipher. Here the guesses are systematic: 60 probable words (Stein's THE and KNOW, the commonest English words, distinctive K1-K3 words) placed at every position of K4 where they do not contradict the known letters, each placement adding its letters as known, then decided exactly for the cells F1.1 and F1.2 left consistent: one free alphabet, Beaufort form, key lengths 23 and 26 (0119's decider), and two free alphabets at 8, 13, 16, 19, 20, 23, 24, 26 (0123's). A cell's consistent placements on K4 are compared with copies of K4 that fit the same cell; F6.1 and F6.2 (with a move) are left out for cost (hundreds of thousands of fitting settings).

## Hypothesis (domain expert)

Stein 1999 (knowledge/sources/stein-1999-cracking-the-courtyard-crypto.txt): 'given that the first letter of Part II could very well be a T, I naturally wanted to see what would happen if H were the second letter and E the third'; 'that KNO in the 15th row was an unexpected gift'. C7(a) (K1-K3 words), C19 (X as a stop). Each placement of a w-letter word adds w equations; in a cell with free alphabets most placements are refuted, so the count of consistent placements is a measure the known letters alone could not give. Statistic fixed before the run: per cell, consistent placements with at least one added check, K4 against ten copies drawn to fit that cell; any cell where K4 is above every copy is replicated.

## Prediction

Consistent placements on K4 inside the copies' range in every cell. Zero candidates.

## Method

1. Words: THE, KNOW, the commonest English words, distinctive K1-K3 words (60).
2. For each cell, K4 and 10 copies that fit the cell: every word at every position compatible with the known letters; add its letters; decide exactly (node limits, undecided counted).
3. Count consistent placements with an added check; compare.

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
 "family": "probable-word placements in the undecided free-alphabet cells (F1.1 Beaufort 23, 26; F1.2 two alphabets at 8 lengths), exact",
 "words": 60,
 "placements_per_text": 3634,
 "summary": {
  "one free, Beaufort 23": {
   "k4_consistent": 1939,
   "coppers_consistent": [
    1720,
    2017,
    1948,
    2072,
    1652,
    1798,
    1907,
    1413,
    1787,
    1573
   ],
   "k4_undecided": 0,
   "placements_done": [
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634
   ],
   "k4_above_every_copy": false,
   "k4_examples": [
    "THE@1",
    "THE@3",
    "THE@5",
    "THE@7",
    "THE@8",
    "THE@9",
    "THE@10",
    "THE@12",
    "THE@13",
    "THE@14",
    "THE@15",
    "THE@16",
    "THE@18",
    "THE@19",
    "THE@20",
    "THE@34",
    "THE@35",
    "THE@36",
    "THE@37",
    "THE@38"
   ]
  },
  "one free, Beaufort 26": {
   "k4_consistent": 1814,
   "coppers_consistent": [
    1927,
    1371,
    1501,
    1665,
    1212,
    1917,
    1820,
    1702,
    2223,
    1670
   ],
   "k4_undecided": 0,
   "placements_done": [
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634
   ],
   "k4_above_every_copy": false,
   "k4_examples": [
    "THE@2",
    "THE@4",
    "THE@5",
    "THE@6",
    "THE@7",
    "THE@9",
    "THE@10",
    "THE@12",
    "THE@13",
    "THE@14",
    "THE@15",
    "THE@18",
    "THE@19",
    "THE@20",
    "THE@34",
    "THE@35",
    "THE@36",
    "THE@38",
    "THE@39",
    "THE@40"
   ]
  },
  "two free 8": {
   "k4_consistent": 593,
   "coppers_consistent": [
    582,
    441,
    439,
    482,
    560,
    541,
    469,
    651,
    504,
    575
   ],
   "k4_undecided": 0,
   "placements_done": [
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634
   ],
   "k4_above_every_copy": false,
   "k4_examples": [
    "THE@3",
    "THE@6",
    "THE@8",
    "THE@11",
    "THE@14",
    "THE@16",
    "THE@19",
    "THE@48",
    "THE@54",
    "THE@56",
    "THE@59",
    "THE@75",
    "THE@80",
    "THE@83",
    "THE@86",
    "THE@88",
    "THE@91",
    "THE@94",
    "KNOW@5",
    "KNOW@7"
   ]
  },
  "two free 13": {
   "k4_consistent": 1271,
   "coppers_consistent": [
    1313,
    1143,
    1340,
    1372,
    1059,
    1045,
    1098,
    1145,
    1219,
    1283
   ],
   "k4_undecided": 10,
   "placements_done": [
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634
   ],
   "k4_above_every_copy": false,
   "k4_examples": [
    "THE@1",
    "THE@2",
    "THE@5",
    "THE@6",
    "THE@9",
    "THE@10",
    "THE@13",
    "THE@15",
    "THE@17",
    "THE@18",
    "THE@19",
    "THE@20",
    "THE@34",
    "THE@35",
    "THE@36",
    "THE@41",
    "THE@43",
    "THE@45",
    "THE@48",
    "THE@49"
   ]
  },
  "two free 16": {
   "k4_consistent": 1793,
   "coppers_consistent": [
    1886,
    1505,
    1532,
    2038,
    1903,
    1637,
    1489,
    1775,
    2089,
    1643
   ],
   "k4_undecided": 4,
   "placements_done": [
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634
   ],
   "k4_above_every_copy": false,
   "k4_examples": [
    "THE@1",
    "THE@3",
    "THE@5",
    "THE@6",
    "THE@7",
    "THE@8",
    "THE@10",
    "THE@11",
    "THE@14",
    "THE@16",
    "THE@17",
    "THE@19",
    "THE@20",
    "THE@37",
    "THE@38",
    "THE@39",
    "THE@44",
    "THE@46",
    "THE@48",
    "THE@49"
   ]
  },
  "two free 19": {
   "k4_consistent": 2317,
   "coppers_consistent": [
    2443,
    2182,
    1722,
    2102,
    2070,
    1957,
    2009,
    1812,
    1795,
    1969
   ],
   "k4_undecided": 2,
   "placements_done": [
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634
   ],
   "k4_above_every_copy": false,
   "k4_examples": [
    "THE@2",
    "THE@3",
    "THE@4",
    "THE@5",
    "THE@7",
    "THE@8",
    "THE@9",
    "THE@11",
    "THE@16",
    "THE@17",
    "THE@18",
    "THE@19",
    "THE@20",
    "THE@34",
    "THE@35",
    "THE@36",
    "THE@37",
    "THE@38",
    "THE@40",
    "THE@41"
   ]
  },
  "two free 20": {
   "k4_consistent": 1834,
   "coppers_consistent": [
    2137,
    1782,
    2061,
    2207,
    2149,
    1930,
    2080,
    2096,
    2255,
    1995
   ],
   "k4_undecided": 0,
   "placements_done": [
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634
   ],
   "k4_above_every_copy": false,
   "k4_examples": [
    "THE@1",
    "THE@7",
    "THE@8",
    "THE@10",
    "THE@11",
    "THE@14",
    "THE@15",
    "THE@16",
    "THE@17",
    "THE@18",
    "THE@19",
    "THE@20",
    "THE@34",
    "THE@35",
    "THE@36",
    "THE@37",
    "THE@38",
    "THE@39",
    "THE@41",
    "THE@42"
   ]
  },
  "two free 23": {
   "k4_consistent": 2380,
   "coppers_consistent": [
    2264,
    2225,
    2233,
    2461,
    2486,
    2148,
    2476,
    2086,
    2319,
    2331
   ],
   "k4_undecided": 2,
   "placements_done": [
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634
   ],
   "k4_above_every_copy": false,
   "k4_examples": [
    "THE@1",
    "THE@3",
    "THE@4",
    "THE@5",
    "THE@7",
    "THE@8",
    "THE@9",
    "THE@10",
    "THE@12",
    "THE@13",
    "THE@14",
    "THE@15",
    "THE@16",
    "THE@18",
    "THE@19",
    "THE@20",
    "THE@34",
    "THE@35",
    "THE@36",
    "THE@37"
   ]
  },
  "two free 24": {
   "k4_consistent": 2564,
   "coppers_consistent": [
    2545,
    2252,
    2345,
    2343,
    2097,
    2150,
    2510,
    2438,
    2225,
    2473
   ],
   "k4_undecided": 3,
   "placements_done": [
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634,
    3634
   ],
   "k4_above_every_copy": true,
   "k4_examples": [
    "THE@2",
    "THE@3",
    "THE@4",
    "THE@6",
    "THE@7",
    "THE@8",
    "THE@9",
    "THE@11",
    "THE@12",
    "THE@13",
    "THE@14",
    "THE@16",
    "THE@17",
    "THE@18",
    "THE@19",
    "THE@20",
    "THE@34",
    "THE@35",
    "THE@36",
    "THE@37"
   ]
  },
  "two free 26": {
   "k4_consistent": 1585,
   "coppers_consistent": [
    2324,
    2317,
    1049,
    1208,
    2331,
    621,
    1386,
    2721,
    1035,
    831
   ],
   "k4_undecided": 3,
   "placements_done": [
    2063,
    3634,
    3634,
    1497,
    1636,
    3634,
    789,
    1986,
    3634,
    1632,
    1036
   ],
   "k4_above_every_copy": false,
   "k4_examples": [
    "THE@1",
    "THE@2",
    "THE@4",
    "THE@5",
    "THE@6",
    "THE@7",
    "THE@9",
    "THE@10",
    "THE@12",
    "THE@13",
    "THE@14",
    "THE@15",
    "THE@16",
    "THE@17",
    "THE@18",
    "THE@19",
    "THE@20",
    "THE@34",
    "THE@35",
    "THE@36"
   ]
  }
 },
 "cells_k4_above_every_copy": [
  "two free 24"
 ],
 "copies": "per cell, 10 copies keeping the carved letters at the 24 known places, other 73 shuffled (they fit the cell by construction; seed 1616)",
 "seconds": 1737,
 "exhaustive": "exact per placement; undecided counted"
}
```

Notes: one free, Beaufort 23: K4 1939 (copies 1413-2072); one free, Beaufort 26: K4 1814 (copies 1212-2223); two free 8: K4 593 (copies 439-651); two free 13: K4 1271 (copies 1045-1372); two free 16: K4 1793 (copies 1489-2089); two free 19: K4 2317 (copies 1722-2443); two free 20: K4 1834 (copies 1782-2255); two free 23: K4 2380 (copies 2086-2486); two free 24: K4 2564 (copies 2097-2545); two free 26: K4 1585 (copies 621-2721)


