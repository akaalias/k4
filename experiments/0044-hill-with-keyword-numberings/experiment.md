# 0044-hill-with-keyword-numberings: Hill again, with the letters numbered by every alphabet the puzzle's words can build

**Family:** 8-hill-polygraphic  
**Parent:** 0015-hill-solved-from-crib-blocks  
**Decision:** reverted  
**Run:** 2026-10-15T09:37:45+00:00, 0.5 s, status ran  
**Time by phase:** design 0 s, implement 31 s, test 1 s, run 0 s, record 0 s

## In plain words

A Hill cipher first turns letters into numbers, and which number a letter gets depends on the order of the alphabet used. Experiment 15 used the plain order and the sculpture's order. Here the order comes from each word the puzzle knows, and the mixing table is again worked out directly from the known groups of letters and then tested on the remaining known letters.

## Walkthrough, by hand

1. Number the letters A=0 to Z=25.
2. Take blocks of two starting at position 1, so 23-24 and 25-26 are whole blocks inside EASTNORTHEAST: AS and TN, which are (0,18) and (19,13).
3. The carved letters there are LR and VQ: (11,17) and (21,16).
4. We want a 2x2 table M with M times (0,18) = (11,17) and M times (19,13) = (21,16), all mod 26.
5. Put the plaintext pairs side by side as a 2x2 matrix, invert it mod 26 if its determinant is coprime to 26, and multiply: that is M.
6. Now test M on the next block, 27-28, OR, which must come out as the carved QP.
7. If it does not, this setting is dead.
8. Repeat for every numbering, every alignment and the other direction.

## Worked example (generated)

```
2x2, standard numbering A=0, blocks from position 1, matrix encrypts: solve from blocks 23-24 and 25-26

plain blocks  AS=[0, 18]  TN=[19, 13];  cipher blocks  LR=[11, 17]  VQ=[21, 16]
plaintext matrix [[0, 19], [18, 13]] has determinant 22, not invertible mod 26: use another pair of blocks
```

## Lineage

Inherits from 0015-hill-solved-from-crib-blocks. What changed: Experiment 15 numbered the letters by the standard and KRYPTOS orders. Here the numbering comes from the keyword mixing of each vocabulary word, 0-based and 1-based: 124 numberings instead of 4, with the same exact solver, block sizes, alignments, directions and the affine form.

## Hypothesis (domain expert)

Experiment 15 solved Hill exactly from the whole crib blocks under four numberings and found every setting inconsistent or broken by the partial-block cribs. Bauer's open item 'shifted numberings' (C21) and Scheidt's keyword alphabets (C5) make the numbering the natural variable: A=0 and A=1 on the keyword mixing of each of 61 vocabulary words, 124 numberings, block sizes 2-4, every alignment, matrix encrypting or decrypting, plain and affine. The mod-13 and mod-2 solver enumerates every matrix consistent with the whole crib blocks; survivors decrypt the text and the partial-block cribs test them. Bounds: complete for these numberings and forms.

## Prediction

Every 2x2 and 3x3 setting is inconsistent on its whole crib blocks under every numbering; a few 4x4 settings are consistent with no redundancy and all of them break the partial-block cribs. Zero candidates pass.

## Method

1. For each numbering map letters to 0-25.
2. For each block size n, alignment o and direction, list the whole crib blocks and their ciphertext blocks.
3. Plain form: pick n blocks with an invertible plaintext matrix, solve M, check the rest. Affine form: use differences between blocks to solve M, then v from one block, check the rest.
4. Decrypt the text with the inverse map; submit if all 24 cribs hold.
5. Record, per setting, how many blocks were available and how many checks passed.

## Result

Candidates returned: 50. Passed all gates: 0. Best crib hits among all candidates: 21/24
(EAST 3/4, NORTHEAST 9/9, BERLIN 4/6, CLOCK 5/5).
Best loss: 35.31137144950235 (0 is solved; 10 per missed crib letter). Best fitness: None. Champion before this run: 0034-complete-the-key-at-surviving-periods.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | cribs | 16/24 |  | `MQMHCZPDGGADDVUBAZRSIBRGTNORTHEAOPUWKBKRXSSHCYHFEOBNKMMRQUYCLTBFERLINCLOBMSPJGHQNWCECYUQHOGBUWEWR` | Hill 4x4 std1 offset 0 enc; M=[[9, 24, 18, 24], [25, 16, 25, 15], [18, 4, 19, 14], [1, 19, 18, 9]] |
| 2 | cribs | 16/24 |  | `MQMHCZPDGGADDVUBAZRSIBRGTNORTHEAOPUWKBKRXSSHCYHFEOBNKMMRQUYCLTBFERLINCLOBMSPJGHQNWCECYUQHOGBUWEWR` | Hill 4x4 std1 offset 0 dec; M=[[25, 22, 20, 10], [10, 19, 11, 17], [16, 10, 19, 18], [25, 1, 3, 8]] |
| 3 | cribs | 16/24 |  | `OBKESYBUMZHBIXOAMKSBQGESTNORTHEVFOVGERRYDPXLXMJYCLWZHFGHLVABYOOBERLINCLUDXOGSHRHPIPCLDZRWWKQSAHAR` | Hill 4x4 PALIMPSEST1 offset 3 enc; M=[[11, 1, 12, 3], [25, 8, 18, 20], [0, 20, 17, 5], [10, 17, 9, 25]] |
| 4 | cribs | 16/24 |  | `OBKESYBUMZHBIXOAMKSBQGESTNORTHEVFOVGERRYDPXLXMJYCLWZHFGHLVABYOOBERLINCLUDXOGSHRHPIPCLDZRWWKQSAHAR` | Hill 4x4 PALIMPSEST1 offset 3 dec; M=[[20, 13, 0, 8], [20, 6, 19, 15], [15, 15, 6, 11], [25, 3, 13, 17]] |
| 5 | cribs | 20/24 |  | `ONOGQKJCBZSDBOFFZMGXEEASTNORTHEASSWSKJZGXVGYCMPFBKOZGPAZYUSMGWEIFRLINCLOCZGNIESOWEFMFKZTGRIZTAQAO` | Hill 4x4 affine ABSCISSAE0 offset 1 enc; M=[[23, 17, 14, 16], [17, 8, 19, 12], [11, 3, 25, 4], [11, 2, 21, 11]] v=[2, 25, 19, 1] |
| 6 | cribs | 20/24 |  | `ONOGQKJCBZSDBSUUZMGXEEASTNORTHEASOHOKJZGXVGYCMPFBKOZGPAZYUSMGWEIFRLINCLOCLVBIROSWRUAFKZTGEQLTAQAO` | Hill 4x4 affine ABSCISSAE0 offset 1 enc; M=[[23, 17, 14, 16], [17, 8, 19, 12], [24, 16, 25, 17], [11, 2, 21, 11]] v=[2, 25, 19, 1] |
| 7 | cribs | 20/24 |  | `ONOGQKJCBZSDBSUFZMGXEEASTNORTHEASOHSKJZGXVGYCMPFBKOZGPAZYUSMGWEIFRLINCLOCLVNIROOWRUMFKZTGEQZTAQAO` | Hill 4x4 affine ABSCISSAE0 offset 1 enc; M=[[23, 17, 14, 16], [4, 21, 19, 25], [11, 3, 25, 4], [24, 15, 21, 24]] v=[2, 25, 19, 1] |
| 8 | cribs | 20/24 |  | `ONOGQKJCBZSDBOFUZMGXEEASTNORTHEASSWOKJZGXVGYCMPFBKOZGPAZYUSMGWEIFRLINCLOCZGBIESSWEFAFKZTGRILTAQAO` | Hill 4x4 affine ABSCISSAE0 offset 1 enc; M=[[23, 17, 14, 16], [4, 21, 19, 25], [24, 16, 25, 17], [24, 15, 21, 24]] v=[2, 25, 19, 1] |
| 9 | cribs | 20/24 |  | `ONOGQKJCBZSDBSFULMGXEEASTNORTHEASOWOYJZGXVGYCMPFBKOZGPAZYUSMGWEIFRLINCLOCLGBQRSSHRFAUKZTGEILDAQAO` | Hill 4x4 affine ABSCISSAE0 offset 1 enc; M=[[10, 4, 14, 3], [17, 8, 19, 12], [11, 3, 25, 4], [24, 15, 21, 24]] v=[2, 25, 19, 1] |
| 10 | cribs | 20/24 |  | `ONOGQKJCBZSDBOUFLMGXEEASTNORTHEASSHSYJZGXVGYCMPFBKOZGPAZYUSMGWEIFRLINCLOCZVNQEOOHEUMUKZTGRQZDAQAO` | Hill 4x4 affine ABSCISSAE0 offset 1 enc; M=[[10, 4, 14, 3], [17, 8, 19, 12], [24, 16, 25, 17], [24, 15, 21, 24]] v=[2, 25, 19, 1] |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "Hill cipher, block sizes 2-4, plain and affine, solved from crib blocks",
 "numberings": [
  "std0",
  "std1",
  "kry0",
  "kry1",
  "PALIMPSEST0",
  "PALIMPSEST1",
  "ABSCISSA0",
  "ABSCISSA1",
  "ABSCISSAE0",
  "ABSCISSAE1",
  "ORDINATE0",
  "ORDINATE1",
  "LAYERTWO0",
  "LAYERTWO1",
  "LAYER0",
  "LAYER1",
  "TWO0",
  "TWO1",
  "WEBSTER0",
  "WEBSTER1",
  "WILLIAMWEBSTER0",
  "WILLIAMWEBSTER1",
  "LANGLEY0",
  "LANGLEY1",
  "BERLIN0",
  "BERLIN1",
  "CLOCK0",
  "CLOCK1",
  "BERLINCLOCK0",
  "BERLINCLOCK1",
  "WELTZEITUHR0",
  "WELTZEITUHR1",
  "ALEXANDERPLATZ0",
  "ALEXANDERPLATZ1",
  "WORLDCLOCK0",
  "WORLDCLOCK1",
  "EGYPT0",
  "EGYPT1",
  "CARTER0",
  "CARTER1",
  "HOWARDCARTER0",
  "HOWARDCARTER1",
  "TUTANKHAMUN0",
  "TUTANKHAMUN1",
  "TUTANKHAMEN0",
  "TUTANKHAMEN1",
  "CARNARVON0",
  "CARNARVON1",
  "WONDERFUL0",
  "WONDERFUL1",
  "WONDERFULTHINGS0",
  "WONDERFULTHINGS1",
  "INVISIBLE0",
  "INVISIBLE1",
  "VIRTUALLYINVISIBLE0",
  "VIRTUALLYINVISIBLE1",
  "SHADOW0",
  "SHADOW1",
  "SHADOWFORCES0",
  "SHADOWFORCES1",
  "LUCID0",
  "LUCID1",
  "LUCIDMEMORY0",
  "LUCIDMEMORY1",
  "POSITION0",
  "POSITION1",
  "DIGETAL0",
  "DIGETAL1",
  "DIGITAL0",
  "DIGITAL1",
  "INTERPRETATION0",
  "INTERPRETATION1",
  "MAGNETIC0",
  "MAGNETIC1",
  "LODESTONE0",
  "LODESTONE1",
  "COMPASS0",
  "COMPASS1",
  "IQLUSION0",
  "IQLUSION1",
  "ILLUSION0",
  "ILLUSION1",
  "UNDERGRUUND0",
  "UNDERGRUUND1",
  "UNDERGROUND0",
  "UNDERGROUND1",
  "DESPARATLY0",
  "DESPARATLY1",
  "DESPERATELY0",
  "DESPERATELY1",
  "BURIED0",
  "BURIED1",
  "SOMEWHERE0",
  "SOMEWHERE1",
  "LOCATION0",
  "LOCATION1",
  "MESSAGE0",
  "MESSAGE1",
  "SECRET0",
  "SECRET1",
  "SANBORN0",
  "SANBORN1",
  "SCHEIDT0",
  "SCHEIDT1",
  "CIA0",
  "CIA1",
  "NORTHEAST0",
  "NORTHEAST1",
  "EAST0",
  "EAST1",
  "WEST0",
  "WEST1",
  "NORTH0",
  "NORTH1",
  "SOUTH0",
  "SOUTH1",
  "HILL0",
  "HILL1",
  "WALL0",
  "WALL1",
  "BERLINWALL0",
  "BERLINWALL1",
  "MYSTERY0",
  "MYSTERY1",
  "RIDDLE0",
  "RIDDLE1"
 ],
 "alignments": "0..n-1",
 "directions": [
  "enc",
  "dec"
 ],
 "settings": 4536,
 "settings_solved": 369,
 "settings_consistent_on_all_crib_blocks": [
  {
   "numbering": "std0",
   "n": 4,
   "offset": 0,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 16
  },
  {
   "numbering": "std0",
   "n": 4,
   "offset": 3,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1
  },
  {
   "numbering": "std1",
   "n": 4,
   "offset": 0,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1,
   "english": [
    -7.862
   ]
  },
  {
   "numbering": "std1",
   "n": 4,
   "offset": 0,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1,
   "english": [
    -7.862
   ]
  },
  {
   "numbering": "std1",
   "n": 4,
   "offset": 3,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1
  },
  {
   "numbering": "kry0",
   "n": 4,
   "offset": 0,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1
  },
  {
   "numbering": "kry0",
   "n": 4,
   "offset": 1,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  },
  {
   "numbering": "kry0",
   "n": 4,
   "offset": 2,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  },
  {
   "numbering": "kry0",
   "n": 4,
   "offset": 3,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1
  },
  {
   "numbering": "kry1",
   "n": 4,
   "offset": 0,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1
  },
  {
   "numbering": "kry1",
   "n": 4,
   "offset": 1,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  },
  {
   "numbering": "kry1",
   "n": 4,
   "offset": 2,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  },
  {
   "numbering": "PALIMPSEST0",
   "n": 4,
   "offset": 1,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  },
  {
   "numbering": "PALIMPSEST0",
   "n": 4,
   "offset": 2,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  },
  {
   "numbering": "PALIMPSEST0",
   "n": 4,
   "offset": 3,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1
  },
  {
   "numbering": "PALIMPSEST1",
   "n": 4,
   "offset": 0,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1
  },
  {
   "numbering": "PALIMPSEST1",
   "n": 4,
   "offset": 1,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  },
  {
   "numbering": "PALIMPSEST1",
   "n": 4,
   "offset": 2,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  },
  {
   "numbering": "PALIMPSEST1",
   "n": 4,
   "offset": 3,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1,
   "english": [
    -7.448
   ]
  },
  {
   "numbering": "PALIMPSEST1",
   "n": 4,
   "offset": 3,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1,
   "english": [
    -7.448
   ]
  },
  {
   "numbering": "ABSCISSA0",
   "n": 4,
   "offset": 1,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  },
  {
   "numbering": "ABSCISSA0",
   "n": 4,
   "offset": 3,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1
  },
  {
   "numbering": "ABSCISSA1",
   "n": 4,
   "offset": 1,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  },
  {
   "numbering": "ABSCISSAE0",
   "n": 4,
   "offset": 0,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1
  },
  {
   "numbering": "ABSCISSAE0",
   "n": 4,
   "offset": 1,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 16,
   "english": [
    -7.566,
    -7.749,
    -7.796,
    -7.45,
    -7.549,
    -7.988,
    -7.743,
    -7.772
   ]
  },
  {
   "numbering": "ABSCISSAE0",
   "n": 4,
   "offset": 1,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 16,
   "english": [
    -7.566,
    -7.45,
    -7.988,
    -7.743,
    -7.772,
    -7.549,
    -7.796,
    -7.749
   ]
  },
  {
   "numbering": "ABSCISSAE0",
   "n": 4,
   "offset": 2,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  },
  {
   "numbering": "ABSCISSAE1",
   "n": 4,
   "offset": 0,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1
  },
  {
   "numbering": "ABSCISSAE1",
   "n": 4,
   "offset": 1,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 16,
   "english": [
    -7.988,
    -7.549,
    -7.772,
    -7.743,
    -7.749,
    -7.566,
    -7.45,
    -7.796
   ]
  },
  {
   "numbering": "ABSCISSAE1",
   "n": 4,
   "offset": 1,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 16,
   "english": [
    -7.988,
    -7.743,
    -7.566,
    -7.45,
    -7.796,
    -7.749,
    -7.772,
    -7.549
   ]
  },
  {
   "numbering": "ABSCISSAE1",
   "n": 4,
   "offset": 2,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  },
  {
   "numbering": "ABSCISSAE1",
   "n": 4,
   "offset": 3,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1
  },
  {
   "numbering": "ORDINATE0",
   "n": 4,
   "offset": 0,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1,
   "english": [
    -7.51
   ]
  },
  {
   "numbering": "ORDINATE0",
   "n": 4,
   "offset": 0,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1,
   "english": [
    -7.51
   ]
  },
  {
   "numbering": "ORDINATE0",
   "n": 4,
   "offset": 2,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1,
   "english": [
    -7.364
   ]
  },
  {
   "numbering": "ORDINATE0",
   "n": 4,
   "offset": 2,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1,
   "english": [
    -7.364
   ]
  },
  {
   "numbering": "ORDINATE1",
   "n": 4,
   "offset": 0,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1
  },
  {
   "numbering": "ORDINATE1",
   "n": 4,
   "offset": 2,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1,
   "english": [
    -7.364
   ]
  },
  {
   "numbering": "ORDINATE1",
   "n": 4,
   "offset": 2,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1,
   "english": [
    -7.364
   ]
  },
  {
   "numbering": "ORDINATE1",
   "n": 4,
   "offset": 3,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1
  }
 ],
 "settings_inconsistent": 3663,
 "log_size": 4536,
 "numberings_count": 126
}
```

Notes: 4536 settings; 369 consistent with every whole crib block; 214 decryptions submitted.


