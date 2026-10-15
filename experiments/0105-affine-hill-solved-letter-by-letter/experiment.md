# 0105-affine-hill-solved-letter-by-letter: Affine Hill ciphers of size 2 to 5, solved from every known letter, not only whole blocks

**Family:** 8-hill-polygraphic  
**Parent:** 0015-hill-2x2-3x3-4x4-exact  
**Decision:** reverted  
**Run:** 2026-10-15T20:15:19+00:00, 0.3 s, status ran  
**Time by phase:** unattributed 124 s, run 0 s, record 0 s

## In plain words

A Hill cipher cuts the message into blocks of a few letters and mixes each block with a small table of numbers. Experiments 15 and 44 solved the table from blocks where all letters are known. Turning the method around, every single known letter gives one equation, even in a block that is only partly known. With that, even the 4-letter version with an extra shift, which had too few whole blocks before, can be solved exactly.

## Walkthrough, by hand

1. Cut the copper into blocks of 4 from place 1: OBKR, UOXO, and so on; place 22 is the second letter of block 6 (places 21-24, WFLR).
2. Number the letters, A = 0 ... Z = 25.
3. Place 22 holds E = 4, the second letter of its block, so row 2 of the table times the block's four numbers, plus shift 2, equals 4 mod 26.
4. Every known letter in a block's second position gives such an equation for row 2: five unknowns, about six equations.
5. Solve each row; if all rows have solutions and the table can be undone, the setting fits.

## Worked example (generated)

```
4x4 affine Hill, blocks from place 1, letters A = 0: equations for row 2 (the second letter of each block)

block places  carved block  numbers          known second letter
  21-24              WFLR  [22, 5, 11, 17]  E = 4
  25-28              VQQP  [21, 16, 16, 15] N = 13
  29-32              RNGK  [17, 13, 6, 10]  H = 7
  33-36              SSOT  [18, 18, 14, 19] T = 19
  65-68              YPVT  [24, 15, 21, 19] R = 17
  69-72              TMZF  [19, 12, 25, 5]  C = 2
  73-76              PKWG  [15, 10, 22, 6]  K = 10

row 2 has five unknowns (four table entries and a shift); each line above is one equation
```

## Lineage

Inherits from 0015-hill-2x2-3x3-4x4-exact. What changed: 0015 and 0044 solved Hill matrices from whole crib blocks and used the partial blocks only as checks, which left the 4x4 affine case open (it needs five whole blocks). Written as decryption, p = B c + w, every known plaintext letter gives one linear equation in one row of B, because the carved block is always known. So each row of an n x n affine Hill is solved from all the known letters in that row position, partial blocks included, for n = 2 to 5.

## Hypothesis (domain expert)

Family 8 open item 'the 4x4 affine' (families.md); the HILL column of the tableau (C21, Bauer 2016-17). Model: blocks of n carved letters c (n = 2-5), message block p = B c + w mod 26, B invertible mod 26, w any vector (w = 0 is plain Hill). Row r of (B, w) has n + 1 unknowns; each block whose r-th message letter is known gives one equation. Solved exactly mod 2 and mod 13 (all solutions enumerated when a row is underdetermined, up to a cap) and joined by the Chinese remainder theorem; a setting survives if every row has a solution and some choice makes B invertible. Block alignments 0 to n-1 (the last partial block left plain); numberings: standard or KRYPTOS order, 0- or 1-based. Ten shuffled coppers.

## Prediction

No setting with at least one check survives for n = 2-4, plain or affine; n = 5 affine has no checks (6 unknowns per row, about 5 equations) and is reported as untestable. Zero candidates.

## Method

1. For each n, alignment and numbering, group the known letters by block and row position.
2. For each row, solve the equations mod 2 and mod 13.
3. Join the rows, require B invertible mod 26, and count the spare equations (checks).
4. Decrypt survivors.
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
 "family": "affine and plain Hill, sizes 2-5, every alignment, four numberings, solved row by row from every known letter",
 "by_size": {
  "2x2 plain": {
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
   ],
   "controls_open": [
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
  "2x2 affine": {
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
   ],
   "controls_open": [
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
  "3x3 plain": {
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
   ],
   "controls_open": [
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
  "3x3 affine": {
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
   ],
   "controls_open": [
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
  "4x4 plain": {
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
   ],
   "controls_open": [
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
  "4x4 affine": {
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
   ],
   "controls_open": [
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
  "5x5 plain": {
   "k4": {
    "alive": 0,
    "dead": 20,
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
    1
   ],
   "controls_open": [
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
  "5x5 affine": {
   "k4": {
    "alive": 0,
    "dead": 6,
    "open": 14
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
   ],
   "controls_open": [
    12,
    16,
    10,
    12,
    20,
    16,
    10,
    14,
    12,
    20
   ]
  }
 },
 "k4_alive": [],
 "controls": "10 shuffled coppers (seed 105), identical test"
}
```

Notes: 2x2 plain: K4 {'alive': 0, 'dead': 8, 'open': 0}, controls alive [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]; 2x2 affine: K4 {'alive': 0, 'dead': 8, 'open': 0}, controls alive [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]; 3x3 plain: K4 {'alive': 0, 'dead': 12, 'open': 0}, controls alive [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]; 3x3 affine: K4 {'alive': 0, 'dead': 12, 'open': 0}, controls alive [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]; 4x4 plain: K4 {'alive': 0, 'dead': 16, 'open': 0}, controls alive [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]; 4x4 affine: K4 {'alive': 0, 'dead': 16, 'open': 0}, controls alive [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]; 5x5 plain: K4 {'alive': 0, 'dead': 20, 'open': 0}, controls alive [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]; 5x5 affine: K4 {'alive': 0, 'dead': 6, 'open': 14}, controls alive [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]. K4 alive with checks: 0.


