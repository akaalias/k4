# 0116-hill-matrix-then-the-table: A Hill matrix and a repeating key on the table, in either order: 'matrix codes', then 'back to this table'

**Family:** 8-hill-polygraphic  
**Parent:** 0105-affine-hill-solved-letter-by-letter  
**Decision:** reverted  
**Run:** 2026-10-15T20:59:00+00:00, 6.5 s, status ran  
**Time by phase:** unattributed 115 s, run 6 s, record 0 s

## In plain words

Sanborn said he used the matrix codes Ed Scheidt gave him, and then went back to the table. A Hill cipher is literally a matrix code: blocks of letters are multiplied by a small square of numbers. Here a Hill matrix of size 2, 3 or 4 is combined with a short repeating secret word on the table, in either order. Every known letter gives one equation, and the equations are solved exactly.

## Walkthrough, by hand

1. Cut the copper into blocks of 2 from place 1 and use a key of length 4: blocks starting at places 1, 5, 9, ... share one key pair, those at 3, 7, 11, ... the other.
2. For each known letter, write: its number = row of the matrix times the block's two carved numbers + the shift for its row and block class.
3. Row 1 then has 2 matrix entries and 2 shifts as unknowns, against about 12 equations.
4. Solve mod 2 and mod 13; if no solution, or no invertible matrix, the setting dies.
5. Repeat for sizes 2-4, key lengths 1-26, alignments and numberings, and on scrambled coppers.

## Worked example (generated)

```
2x2 Hill with a key of length 4, blocks from place 1, letters A = 0: equations for row 1

block places  carved  numbers   block class  known first letter
  23-24          LR  [11, 17]            2  A = 0
  25-26          VQ  [21, 16]            0  T = 19
  27-28          QP  [16, 15]            2  O = 14
  29-30          RN  [17, 13]            0  T = 19
  31-32          GK  [6, 10]             2  E = 4
  33-34          SS  [18, 18]            0  S = 18
  65-66          YP  [24, 15]            0  E = 4
  67-68          VT  [21, 19]            2  L = 11
  69-70          TM  [19, 12]            0  N = 13
  71-72          ZF  [25, 5]             2  L = 11
  73-74          PK  [15, 10]            0  C = 2

row 1: two matrix entries and one shift per block class (2 classes) against the equations above
```

## Lineage

Inherits from 0105-affine-hill-solved-letter-by-letter. What changed: 0105 solved Hill and affine Hill alone. Sanborn's words, 'matrix codes Ed gave me' and 'double matrixes... then went back to this table to do the ultimate', and the HILL column read literally give a Hill matrix followed by the Vigenere table, or the table followed by the matrix. On one numbering both orders give p = B c + u, where the shift vector u depends on the block's place modulo the key length: still linear, so each row of B is solved exactly from every known letter for key lengths 1-26.

## Hypothesis (domain expert)

C1 ('double matrixes and triple matrixes... then went back to this table'), C21 (the HILL column; Bauer), C3 ('matrix codes'). Model, one numbering for both stages (standard or KRYPTOS order, 0- or 1-based): blocks of n = 2-4 carved letters; message block p = B c + u_kappa mod 26, B invertible, kappa = (block start) mod L classes, L = 1-26 the key length, u_kappa free. This covers Hill then a periodic Vigenere key (u = -B k) and a periodic key then Hill (u = w - k) alike, and an affine Hill. Row r of (B, u) has n + #classes unknowns; each known letter in row position r gives one equation. Solved exactly mod 2 and mod 13 with the Chinese remainder theorem; a setting dies if a row has no solution or no choice makes B invertible; rows with more unknowns than equations leave it open. Block alignments 0 to n-1. Ten shuffled coppers.

## Prediction

No setting with spare equations survives for any size, key length, alignment or numbering; settings with no spare equations are reported as open. Counts match the coppers. Zero candidates.

## Method

1. For each size, key length, alignment and numbering, group the known letters by block, row position and block class.
2. Solve each row mod 2 and mod 13; join by the Chinese remainder theorem.
3. Require an invertible B.
4. Count alive (with spare equations), dead and open settings.
5. Repeat on ten shuffled coppers.

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
 "family": "Hill matrix with a periodic tableau key, either order (p = B c + u_kappa), sizes 2-4, key lengths 1-26",
 "by_size_and_key_length": {
  "2x2 L=1": {
   "k4": {
    "alive": 0,
    "dead": 8,
    "open": 0
   },
   "controls_alive": [
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
  "2x2 L=2": {
   "k4": {
    "alive": 0,
    "dead": 8,
    "open": 0
   },
   "controls_alive": [
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
  "2x2 L=3": {
   "k4": {
    "alive": 0,
    "dead": 8,
    "open": 0
   },
   "controls_alive": [
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
  "2x2 L=4": {
   "k4": {
    "alive": 0,
    "dead": 8,
    "open": 0
   },
   "controls_alive": [
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
  "2x2 L=5": {
   "k4": {
    "alive": 0,
    "dead": 8,
    "open": 0
   },
   "controls_alive": [
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
  "2x2 L=6": {
   "k4": {
    "alive": 0,
    "dead": 8,
    "open": 0
   },
   "controls_alive": [
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
  "2x2 L=7": {
   "k4": {
    "alive": 0,
    "dead": 8,
    "open": 0
   },
   "controls_alive": [
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
  "2x2 L=8": {
   "k4": {
    "alive": 0,
    "dead": 8,
    "open": 0
   },
   "controls_alive": [
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
  "2x2 L=9": {
   "k4": {
    "alive": 0,
    "dead": 8,
    "open": 0
   },
   "controls_alive": [
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
  "2x2 L=10": {
   "k4": {
    "alive": 0,
    "dead": 8,
    "open": 0
   },
   "controls_alive": [
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
  "2x2 L=11": {
   "k4": {
    "alive": 0,
    "dead": 8,
    "open": 0
   },
   "controls_alive": [
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
  "2x2 L=12": {
   "k4": {
    "alive": 0,
    "dead": 8,
    "open": 0
   },
   "controls_alive": [
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
  "2x2 L=13": {
   "k4": {
    "alive": 0,
    "dead": 4,
    "open": 4
   },
   "controls_alive": [
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
  "2x2 L=14": {
   "k4": {
    "alive": 0,
    "dead": 8,
    "open": 0
   },
   "controls_alive": [
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
  "2x2 L=15": {
   "k4": {
    "alive": 0,
    "dead": 0,
    "open": 8
   },
   "controls_alive": [
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
  "2x2 L=16": {
   "k4": {
    "alive": 0,
    "dead": 8,
    "open": 0
   },
   "controls_alive": [
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
  "2x2 L=17": {
   "k4": {
    "alive": 0,
    "dead": 8,
    "open": 0
   },
   "controls_alive": [
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
  "2x2 L=18": {
   "k4": {
    "alive": 0,
    "dead": 8,
    "open": 0
   },
   "controls_alive": [
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
  "2x2 L=19": {
   "k4": {
    "alive": 0,
    "dead": 8,
    "open": 0
   },
   "controls_alive": [
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
  "2x2 L=20": {
   "k4": {
    "alive": 0,
    "dead": 8,
    "open": 0
   },
   "controls_alive": [
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
  "2x2 L=21": {
   "k4": {
    "alive": 0,
    "dead": 8,
    "open": 0
   },
   "controls_alive": [
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
  "2x2 L=22": {
   "k4": {
    "alive": 0,
    "dead": 8,
    "open": 0
   },
   "controls_alive": [
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
  "2x2 L=23": {
   "k4": {
    "alive": 0,
    "dead": 8,
    "open": 0
   },
   "controls_alive": [
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
  "2x2 L=24": {
   "k4": {
    "alive": 0,
    "dead": 8,
    "open": 0
   },
   "controls_alive": [
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
  "2x2 L=25": {
   "k4": {
    "alive": 0,
    "dead": 0,
    "open": 8
   },
   "controls_alive": [
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
  "2x2 L=26": {
   "k4": {
    "alive": 0,
    "dead": 4,
    "open": 4
   },
   "controls_alive": [
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
  "3x3 L=1": {
   "k4": {
    "alive": 0,
    "dead": 12,
    "open": 0
   },
   "controls_alive": [
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
  "3x3 L=2": {
   "k4": {
    "alive": 0,
    "dead": 12,
    "open": 0
   },
   "controls_alive": [
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
  "3x3 L=3": {
   "k4": {
    "alive": 0,
    "dead": 12,
    "open": 0
   },
   "controls_alive": [
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
  "3x3 L=4": {
   "k4": {
    "alive": 0,
    "dead": 12,
    "open": 0
   },
   "controls_alive": [
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
  "3x3 L=5": {
   "k4": {
    "alive": 0,
    "dead": 12,
    "open": 0
   },
   "controls_alive": [
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
  "3x3 L=6": {
   "k4": {
    "alive": 0,
    "dead": 12,
    "open": 0
   },
   "controls_alive": [
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
  "3x3 L=7": {
   "k4": {
    "alive": 0,
    "dead": 12,
    "open": 0
   },
   "controls_alive": [
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
  "3x3 L=8": {
   "k4": {
    "alive": 0,
    "dead": 6,
    "open": 6
   },
   "controls_alive": [
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
  "3x3 L=9": {
   "k4": {
    "alive": 0,
    "dead": 12,
    "open": 0
   },
   "controls_alive": [
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
  "3x3 L=10": {
   "k4": {
    "alive": 0,
    "dead": 0,
    "open": 12
   },
   "controls_alive": [
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
  "3x3 L=11": {
   "k4": {
    "alive": 0,
    "dead": 0,
    "open": 12
   },
   "controls_alive": [
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
  "3x3 L=12": {
   "k4": {
    "alive": 0,
    "dead": 12,
    "open": 0
   },
   "controls_alive": [
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
  "3x3 L=13": {
   "k4": {
    "alive": 0,
    "dead": 12,
    "open": 0
   },
   "controls_alive": [
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
  "3x3 L=14": {
   "k4": {
    "alive": 0,
    "dead": 12,
    "open": 0
   },
   "controls_alive": [
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
  "3x3 L=15": {
   "k4": {
    "alive": 0,
    "dead": 12,
    "open": 0
   },
   "controls_alive": [
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
  "3x3 L=16": {
   "k4": {
    "alive": 0,
    "dead": 6,
    "open": 6
   },
   "controls_alive": [
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
  "3x3 L=17": {
   "k4": {
    "alive": 0,
    "dead": 0,
    "open": 12
   },
   "controls_alive": [
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
  "3x3 L=18": {
   "k4": {
    "alive": 0,
    "dead": 12,
    "open": 0
   },
   "controls_alive": [
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
  "3x3 L=19": {
   "k4": {
    "alive": 0,
    "dead": 0,
    "open": 12
   },
   "controls_alive": [
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
  "3x3 L=20": {
   "k4": {
    "alive": 0,
    "dead": 0,
    "open": 12
   },
   "controls_alive": [
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
  "3x3 L=21": {
   "k4": {
    "alive": 0,
    "dead": 12,
    "open": 0
   },
   "controls_alive": [
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
  "3x3 L=22": {
   "k4": {
    "alive": 0,
    "dead": 0,
    "open": 12
   },
   "controls_alive": [
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
  "3x3 L=23": {
   "k4": {
    "alive": 0,
    "dead": 0,
    "open": 12
   },
   "controls_alive": [
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
  "3x3 L=24": {
   "k4": {
    "alive": 0,
    "dead": 6,
    "open": 6
   },
   "controls_alive": [
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
  "3x3 L=25": {
   "k4": {
    "alive": 0,
    "dead": 0,
    "open": 12
   },
   "controls_alive": [
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
  "3x3 L=26": {
   "k4": {
    "alive": 0,
    "dead": 0,
    "open": 12
   },
   "controls_alive": [
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
  "4x4 L=1": {
   "k4": {
    "alive": 0,
    "dead": 16,
    "open": 0
   },
   "controls_alive": [
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
  "4x4 L=2": {
   "k4": {
    "alive": 0,
    "dead": 16,
    "open": 0
   },
   "controls_alive": [
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
  "4x4 L=3": {
   "k4": {
    "alive": 0,
    "dead": 14,
    "open": 2
   },
   "controls_alive": [
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
  "4x4 L=4": {
   "k4": {
    "alive": 0,
    "dead": 16,
    "open": 0
   },
   "controls_alive": [
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
  "4x4 L=5": {
   "k4": {
    "alive": 0,
    "dead": 4,
    "open": 12
   },
   "controls_alive": [
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
  "4x4 L=6": {
   "k4": {
    "alive": 0,
    "dead": 14,
    "open": 2
   },
   "controls_alive": [
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
  "4x4 L=7": {
   "k4": {
    "alive": 0,
    "dead": 0,
    "open": 16
   },
   "controls_alive": [
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
  "4x4 L=8": {
   "k4": {
    "alive": 0,
    "dead": 16,
    "open": 0
   },
   "controls_alive": [
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
  "4x4 L=9": {
   "k4": {
    "alive": 0,
    "dead": 6,
    "open": 10
   },
   "controls_alive": [
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
  "4x4 L=10": {
   "k4": {
    "alive": 0,
    "dead": 4,
    "open": 12
   },
   "controls_alive": [
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
  "4x4 L=11": {
   "k4": {
    "alive": 0,
    "dead": 8,
    "open": 8
   },
   "controls_alive": [
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
  "4x4 L=12": {
   "k4": {
    "alive": 0,
    "dead": 14,
    "open": 2
   },
   "controls_alive": [
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
  "4x4 L=13": {
   "k4": {
    "alive": 0,
    "dead": 6,
    "open": 10
   },
   "controls_alive": [
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
  "4x4 L=14": {
   "k4": {
    "alive": 0,
    "dead": 0,
    "open": 16
   },
   "controls_alive": [
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
  "4x4 L=15": {
   "k4": {
    "alive": 0,
    "dead": 0,
    "open": 16
   },
   "controls_alive": [
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
  "4x4 L=16": {
   "k4": {
    "alive": 0,
    "dead": 4,
    "open": 12
   },
   "controls_alive": [
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
  "4x4 L=17": {
   "k4": {
    "alive": 0,
    "dead": 0,
    "open": 16
   },
   "controls_alive": [
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
  "4x4 L=18": {
   "k4": {
    "alive": 0,
    "dead": 6,
    "open": 10
   },
   "controls_alive": [
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
  "4x4 L=19": {
   "k4": {
    "alive": 0,
    "dead": 0,
    "open": 16
   },
   "controls_alive": [
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
  "4x4 L=20": {
   "k4": {
    "alive": 0,
    "dead": 4,
    "open": 12
   },
   "controls_alive": [
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
  "4x4 L=21": {
   "k4": {
    "alive": 0,
    "dead": 0,
    "open": 16
   },
   "controls_alive": [
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
  "4x4 L=22": {
   "k4": {
    "alive": 0,
    "dead": 8,
    "open": 8
   },
   "controls_alive": [
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
  "4x4 L=23": {
   "k4": {
    "alive": 0,
    "dead": 0,
    "open": 16
   },
   "controls_alive": [
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
  "4x4 L=24": {
   "k4": {
    "alive": 0,
    "dead": 4,
    "open": 12
   },
   "controls_alive": [
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
  "4x4 L=25": {
   "k4": {
    "alive": 0,
    "dead": 0,
    "open": 16
   },
   "controls_alive": [
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
  "4x4 L=26": {
   "k4": {
    "alive": 0,
    "dead": 6,
    "open": 10
   },
   "controls_alive": [
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
 "k4_alive": [],
 "n_k4_alive": 0,
 "controls": "10 shuffled coppers (seed 116), identical test"
}
```

Notes: 78 (size, key length) cells x alignments x 4 numberings. K4: alive 0, dead 536, open 400; controls alive [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]. Largest key length with any decided setting per size: 2x2: 26, 3x3: 24, 4x4: 26.


