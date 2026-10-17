# 0191-cia-key-box-running-key: F11.3: the CIA's Polish agent key box: a key text written into a box by rows and read out by columns, then a reciprocal or other table; K1-K3, the Morse and Carter's book as key texts: exact

**Family:** 11-agency-hand-systems  
**Parent:** 0190-poem-code-double-transposition  
**Decision:** reverted  
**Run:** 2026-10-17T00:51:49+00:00, 10.7 s, status ran  
**Time by phase:** design 0 s, implement 0 s, test 0 s, run 11 s, record 0 s

## In plain words

The CIA's agents in 1970s Poland took a line of a book, wrote it into a square box row by row, copied it out column by column, and used that jumble as the key on a letter table. Sanborn's 'matrix, then the table' fits this well. We try the sculpture's own texts and the Carter book behind K3 as the key text, every box width, every starting point.

## Walkthrough, by hand

1. Take K2's plaintext from its 40th letter and write it into a box 10 wide, row by row.
2. Read it out column by column: the first 10 letters of the key come from the first column, and so on.
3. Place 22 of the message takes the key letter in column 3, row 2 of the box.
4. On Bury's table, E over the carved F needs one particular key letter; check whether the box gives it.
5. Every start, width, column order and table, on K4 and on scrambled copies.

## Worked example (generated)

```
K2 from its 40th letter in a box 10 wide, read by columns: key stream EATHIENDOLYRIEORSEAOUTCINEMRNCSHFNWDIGUAESIFAATRNTDMEOSNTUKITALRGDEUNOHGDMATDNONENXATRUDWXEETTHAN

place 22: box gives T, Bury's table needs Q for E over F
place 23: box gives C, Bury's table needs O for A over L
place 24: box gives I, Bury's table needs Q for S over R
place 25: box gives N, Bury's table needs L for T over V
place 26: box gives E, Bury's table needs W for N over Q
place 27: box gives M, Bury's table needs V for O over Q
```

## Lineage

Inherits from 0190-poem-code-double-transposition. What changed: F11.3. Bury (Cryptologia 2007, via scz.bplaced.net 9.2): the agent writes a verse row by row into a 10 x 10 box, reads it out by columns, and combines the result with the message through a 26 x 26 reciprocal table (p + k + c = 25). The report's scratch check (K1-K3, best 7 of 24, no controls) is rerun with controls and widened: key texts K1, K2, K3 and K1-K3 joined, the Morse, and Carter's 1923 book (K3's source); box widths 2-50, rows as many as 97 letters need; columns read left to right, right to left, bottom to top, or in a vocabulary keyword's order; tables: Bury's reciprocal, Vigenere, Beaufort and variant, numbered on the standard or KRYPTOS order; every start in the key text. Each setting checks all 24 known letters (compiled); K4 against 10 shuffled copies.

## Hypothesis (domain expert)

A9, F11: the CIA's own documented 1970s agent system, a remembered rule, 'a matrix, then the table' (C1). Model: key stream k_i = T[o + r_i w + col(j_i)], j_i = i div h, r_i = i mod h (h = ceil(97 / w)), then c from p and k by the table rule. Exact: a setting fits only if all 24 known letters agree. Statistic: fitting settings and, for the short key texts, the best number of agreeing known letters, K4 against 10 copies; plants.

## Prediction

No setting fits all 24 known letters on K4 or on the copies; the best partial agreement on K4 lies inside the copies' range (about 7-8 of 24). Zero candidates.

## Method

1. Key texts: K1, K2, K3, K1-K3 joined, the Morse, Carter's book.
2. For each width 2-50 and column order: the offset of each known place's key letter from the start.
3. For each table rule and text: the key letter each known place needs.
4. Every start: fit if all 24 agree (compiled); best agreement for the short key texts.
5. K4 against 10 shuffled copies; two plants.

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
 "family": "key box: key text by rows, read by columns (widths 2-50, natural, reversed, bottom-up, vocabulary keyword orders), then Bury's reciprocal / Vigenere / Beaufort / variant on std or KRYPTOS numbering; every start; exact",
 "readings": 320,
 "rules": 8,
 "settings_per_text": 732076800,
 "per_source": {
  "K1": {
   "settings": 0,
   "fits_k4": 0,
   "fits_copies": [
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
   "fits_plants": [
    0,
    0
   ],
   "best_hits_k4": 0,
   "best_hits_copies": [
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
  "K2": {
   "settings": 676160,
   "fits_k4": 0,
   "fits_copies": [
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
   "fits_plants": [
    1,
    0
   ],
   "best_hits_k4": 8,
   "best_hits_copies": [
    7,
    7,
    8,
    7,
    8,
    8,
    7,
    8,
    8,
    8
   ]
  },
  "K3": {
   "settings": 591680,
   "fits_k4": 0,
   "fits_copies": [
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
   "fits_plants": [
    0,
    0
   ],
   "best_hits_k4": 9,
   "best_hits_copies": [
    7,
    7,
    8,
    8,
    7,
    7,
    7,
    9,
    8,
    8
   ]
  },
  "K1-K3": {
   "settings": 1697600,
   "fits_k4": 0,
   "fits_copies": [
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
   "fits_plants": [
    1,
    0
   ],
   "best_hits_k4": 9,
   "best_hits_copies": [
    8,
    8,
    8,
    8,
    8,
    8,
    7,
    9,
    8,
    9
   ]
  },
  "Morse": {
   "settings": 0,
   "fits_k4": 0,
   "fits_copies": [
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
   "fits_plants": [
    0,
    0
   ],
   "best_hits_k4": 0,
   "best_hits_copies": [
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
  "Carter 1923": {
   "settings": 729111360,
   "fits_k4": 0,
   "fits_copies": [
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
   "fits_plants": [
    0,
    1
   ],
   "best_hits_k4": null,
   "best_hits_copies": null
  }
 },
 "k4_fits": [],
 "plants": [
  {
   "source": "K2",
   "reading": "width 10, columns left to right",
   "start": 255,
   "rule": "std/recip25"
  },
  {
   "source": "Carter 1923",
   "reading": "width 17, columns right to left, bottom to top",
   "start": 191483,
   "rule": "kry/beau"
  }
 ],
 "copies": "10 shuffled copies (seed 1910)",
 "seconds": 11,
 "exhaustive": true
}
```

Notes: K1: fits K4 0 (copies 0-0, plants [0, 0]), best K4 0/24 (copies 0-0); K2: fits K4 0 (copies 0-0, plants [1, 0]), best K4 8/24 (copies 7-8); K3: fits K4 0 (copies 0-0, plants [0, 0]), best K4 9/24 (copies 7-9); K1-K3: fits K4 0 (copies 0-0, plants [1, 0]), best K4 9/24 (copies 7-9); Morse: fits K4 0 (copies 0-0, plants [0, 0]), best K4 0/24 (copies 0-0); Carter 1923: fits K4 0 (copies 0-0, plants [0, 1])


