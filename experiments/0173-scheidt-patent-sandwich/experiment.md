# 0173-scheidt-patent-sandwich: F3.1: Scheidt's patent sandwich, a shift, a keyed table, a second shift and a second table, two repeating keys of length 1-13 each: exact

**Family:** 3-two-component-key  
**Parent:** 0115-two-key-words-added  
**Decision:** reverted  
**Run:** 2026-10-16T23:41:56+00:00, 10.9 s, status ran  
**Time by phase:** design 96 s, implement 0 s, test 0 s, run 11 s, record 0 s

## In plain words

Scheidt, who built the sculpture's codes, later patented a way of enciphering a letter: shift it by a key letter, look it up in a mixed-up alphabet, shift it again by a second key letter, look it up again. With two short secret words as the two keys, the 24 known letters tie the two words' letters together in pairs; we try every way of choosing the tables and every pair of word lengths up to 13, and see whether anything fits K4 better than scrambled copies of it.

## Walkthrough, by hand

1. Take the sculpture's KRYPTOS alphabet as the table, a first key of length 5 and a second of length 7.
2. At place 22 the message has E and the copper has F. Counting places from 0 (21), E is shifted by the first key's slot 21 mod 5 = 1, looked up in the table, and shifted by the second key's slot 21 mod 7 = 0: the result must be F.
3. So each choice for slot 1 of the first key forces slot 0 of the second.
4. Place 29 links slot 3 of the first key to slot 0 of the second: two routes into slot 0 must agree.
5. Try all 26 letters for one slot, follow every link, and keep the letters that never contradict.
6. Do this for every table choice and length pair, on K4 and on scrambled copies.

## Worked example (generated)

```
table KRYPTOS between the two keys, letters numbered on the standard order, first key length 5, second 7

place 22: message E, copper F: links slot 1 of the first key to slot 0 of the second
place 23: message A, copper L: links slot 2 of the first key to slot 1 of the second
place 24: message S, copper R: links slot 3 of the first key to slot 2 of the second
place 25: message T, copper V: links slot 4 of the first key to slot 3 of the second
place 26: message N, copper Q: links slot 0 of the first key to slot 4 of the second
place 27: message O, copper Q: links slot 1 of the first key to slot 5 of the second
place 28: message R, copper P: links slot 2 of the first key to slot 6 of the second
place 29: message T, copper R: links slot 3 of the first key to slot 0 of the second
place 30: message H, copper N: links slot 4 of the first key to slot 1 of the second
place 31: message E, copper G: links slot 0 of the first key to slot 2 of the second
place 32: message A, copper K: links slot 1 of the first key to slot 3 of the second
place 33: message S, copper S: links slot 2 of the first key to slot 4 of the second
place 34: message T, copper S: links slot 3 of the first key to slot 5 of the second

1 connected group(s) of slots, 13 checks from all 24 known letters
```

## Lineage

Inherits from 0115-two-key-words-added. What changed: F3.1, first the sandwich (reports/Scheidt patents and field ciphers.md, issue #9). Scheidt and Wack's patent US 6,075,865 writes the text/key relation as O = a_N + pi_N[a_N-1 + ... pi_1[I + a_0]] mod W. With one table between two key streams, and letters numbered by a third table, c = T2[s2 * T1[s1 * T0[p] + a_i] + b_i], each T one of {standard, KRYPTOS order, its inverse} and each sign + or -: 108 table classes. a repeats every La letters, b every Lb, La and Lb 1-13. F3's closed items added two keys outside any table (0014, 0043, 0059, 0115); here a table sits between them, so the alphabet in force changes with a's phase.

## Hypothesis (domain expert)

C5(b) ('key word/s'), C6 (Scheidt's constructive key management), US 6,075,865 (Scheidt and Wack, priority 1998; report in reports/Scheidt patents and field ciphers.md). Model as in 'changed'. Each known place i gives b[i mod Lb] = T2^-1[c_i] * s2' - T1[s1 T0[p_i] + a[i mod La]], a one-to-one map between one slot of a and one slot of b. The slots form a graph; in each connected part, fixing one slot of a fixes all the others, so 26 trials decide the part exactly. A cell (class, La, Lb) is live if every part has a value that agrees on every edge; it carries E - V + C checks (edges minus slots plus parts). Statistic: live cells with at least one check, by number of checks, K4 against 20 shuffled coppers.

## Prediction

K4's live cells at each number of checks fall inside the coppers' range; no cell with 6 or more checks is live on K4. Zero candidates.

## Method

1. For each pair of lengths (La, Lb) 1-13: the graph of key slots the 24 known places make, its parts and its number of checks.
2. For each text (K4, 20 coppers) and each of 108 table classes: for each part, try the 26 values of one slot of a, carry them along the edges, and keep the values that agree on every edge.
3. Count live cells by checks; for K4's live cells with 4 or more checks, decrypt the places their keys fix.
4. Builder check: three planted texts made with this cipher are live in their own cell.

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
 "family": "Scheidt patent sandwich c = T2[s2 T1[s1 T0[p] + a] + b], T in {standard, KRYPTOS, KRYPTOS inverse}, 108 classes, La, Lb 1-13, exact",
 "cells_per_text": 18252,
 "cells_by_checks": {
  "1": 4,
  "2": 4,
  "4": 8,
  "5": 4,
  "6": 6,
  "7": 8,
  "8": 12,
  "9": 4,
  "10": 10,
  "11": 9,
  "12": 27,
  "13": 5,
  "14": 15,
  "15": 7,
  "16": 13,
  "17": 5,
  "18": 11,
  "19": 3,
  "20": 7,
  "21": 3,
  "22": 3,
  "23": 1
 },
 "live_by_checks": {
  "1": {
   "k4": 174,
   "coppers": [
    197,
    200,
    199,
    190,
    185,
    197,
    191,
    177,
    173,
    207,
    186,
    210,
    188,
    189,
    196,
    188,
    182,
    181,
    196,
    191
   ],
   "k4_new": 174,
   "coppers_new": [
    185,
    188,
    187,
    186,
    181,
    193,
    179,
    177,
    173,
    195,
    178,
    198,
    184,
    189,
    188,
    184,
    174,
    181,
    196,
    183
   ]
  },
  "2": {
   "k4": 8,
   "coppers": [
    6,
    7,
    9,
    10,
    6,
    13,
    12,
    20,
    12,
    8,
    17,
    5,
    9,
    7,
    16,
    8,
    12,
    14,
    13,
    10
   ],
   "k4_new": 8,
   "coppers_new": [
    6,
    7,
    9,
    10,
    6,
    13,
    12,
    20,
    12,
    8,
    17,
    5,
    9,
    7,
    12,
    8,
    12,
    10,
    13,
    10
   ]
  },
  "3": {
   "k4": 0,
   "coppers": [
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
    0
   ],
   "k4_new": 0,
   "coppers_new": [
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
    0
   ]
  },
  "4": {
   "k4": 0,
   "coppers": [
    0,
    1,
    0,
    1,
    0,
    0,
    0,
    1,
    1,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    1,
    0,
    2,
    0
   ],
   "k4_new": 0,
   "coppers_new": [
    0,
    1,
    0,
    1,
    0,
    0,
    0,
    1,
    1,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    1,
    0,
    2,
    0
   ]
  },
  "5": {
   "k4": 0,
   "coppers": [
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
    0
   ],
   "k4_new": 0,
   "coppers_new": [
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
    0
   ]
  },
  "6": {
   "k4": 0,
   "coppers": [
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
    0
   ],
   "k4_new": 0,
   "coppers_new": [
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
    0
   ]
  },
  "7": {
   "k4": 0,
   "coppers": [
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
    0
   ],
   "k4_new": 0,
   "coppers_new": [
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
    0
   ]
  },
  "8": {
   "k4": 0,
   "coppers": [
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
    0
   ],
   "k4_new": 0,
   "coppers_new": [
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
    0
   ]
  },
  "9": {
   "k4": 0,
   "coppers": [
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
    0
   ],
   "k4_new": 0,
   "coppers_new": [
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
    0
   ]
  },
  "10": {
   "k4": 0,
   "coppers": [
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
    0
   ],
   "k4_new": 0,
   "coppers_new": [
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
    0
   ]
  },
  "11": {
   "k4": 0,
   "coppers": [
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
    2,
    0
   ],
   "k4_new": 0,
   "coppers_new": [
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
    2,
    0
   ]
  }
 },
 "new_classes_at_least": {
  "1": {
   "k4": 182,
   "coppers_min": 186,
   "coppers_max": 213,
   "coppers_at_or_above_k4": 20
  },
  "2": {
   "k4": 8,
   "coppers_min": 5,
   "coppers_max": 21,
   "coppers_at_or_above_k4": 16
  },
  "4": {
   "k4": 0,
   "coppers_min": 0,
   "coppers_max": 4,
   "coppers_at_or_above_k4": 20
  },
  "6": {
   "k4": 0,
   "coppers_min": 0,
   "coppers_max": 2,
   "coppers_at_or_above_k4": 20
  },
  "8": {
   "k4": 0,
   "coppers_min": 0,
   "coppers_max": 2,
   "coppers_at_or_above_k4": 20
  },
  "10": {
   "k4": 0,
   "coppers_min": 0,
   "coppers_max": 2,
   "coppers_at_or_above_k4": 20
  }
 },
 "k4_live_examples": [],
 "plants": [
  {
   "class": "std/kry-inv/kry-inv/1/1",
   "La": 7,
   "Lb": 6,
   "checks": 12,
   "live_in_own_cell": true
  },
  {
   "class": "std/kry-inv/kry/1/1",
   "La": 9,
   "Lb": 6,
   "checks": 12,
   "live_in_own_cell": true
  },
  {
   "class": "std/kry-inv/std/1/1",
   "La": 13,
   "Lb": 10,
   "checks": 2,
   "live_in_own_cell": true
  }
 ],
 "copies": "20 shuffled coppers (seed 1730)",
 "seconds": 11,
 "exhaustive": true
}
```

Notes: live cells (middle table not standard), checks >= 1/4/6: K4 182/0/0; coppers 186-213/0-4/0-2; plants live in own cell 3/3


