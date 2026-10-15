# 0055-hill-with-k1-k3-word-numberings: Hill again, with the letters numbered by alphabets built from the solved messages' words

**Family:** 8-hill-polygraphic  
**Parent:** 0044-hill-with-keyword-numberings  
**Decision:** reverted  
**Run:** 2026-10-15T12:14:27+00:00, 0.6 s, status ran  
**Time by phase:** design 0 s, implement 10 s, test 0 s, run 1 s, record 0 s

## In plain words

A Hill cipher turns letters into numbers, mixes them in small groups with a table of numbers, and turns them back into letters. The answer depends on which number each letter gets, which depends on the order of the alphabet. Experiment 44 tried orders built from the puzzle's word list; this one tries orders built from every word of the solved messages. As before, the mixing table is worked out directly from the groups of known letters and then checked on the rest.

## Walkthrough, by hand

1. Build the alphabet from SHADING: SHADINGBCEFJKLMOPQRTUVWXYZ, and number it S=0, H=1 and on.
2. Take blocks of two from place 1, so places 23-24 (AS) and 25-26 (TN) are whole blocks of known letters.
3. In this numbering AS is (2,0) and TN is (19,5).
4. The carved letters there are LR and VQ: (13,18) and (21,17).
5. Find the 2x2 table M that sends (2,0) to (13,18) and (19,5) to (21,17), modulo 26.
6. Test M on places 27-28, OR, which must become the carved QP.
7. If not, this numbering and alignment are dead.
8. Repeat for every numbering, alignment and direction.

## Worked example (generated)

```
2x2, standard numbering A=0, blocks from position 1, matrix encrypts: solve from blocks 23-24 and 25-26

plain blocks  AS=[0, 18]  TN=[19, 13];  cipher blocks  LR=[11, 17]  VQ=[21, 16]
plaintext matrix [[0, 19], [18, 13]] has determinant 22, not invertible mod 26: use another pair of blocks
```

## Lineage

Inherits from 0044-hill-with-keyword-numberings. What changed: Experiment 44 numbered the letters by alphabets built from the puzzle's vocabulary. Here the numberings come from every word of the three solved messages and from the words of Sanborn's 2025 letter, 0-based and 1-based, with the same exact solver.

## Hypothesis (domain expert)

Hill cipher (C21), block sizes 2-4, plain and affine, matrix encrypting or decrypting, every alignment, solved exactly from the whole crib blocks by the mod-13 and mod-2 solver of 0044 and tested on the partial-block cribs. The variable is the numbering: A=0 and A=1 on the keyword mixing of every K1-K3 plaintext word with three or more distinct letters and of EGYPT, CAIRO, LUXOR, WALL, NOVEMBER, MESSAGE, DELIVER, DELIVERING, TRANSMIT (C7, C13, C14), skipping alphabets already covered by 0015 and 0044. Bounds: complete for these numberings and forms.

## Prediction

Every 2x2 and 3x3 setting is inconsistent on its whole crib blocks; some 4x4 settings are consistent with no check to spare and all of them fail the partial-block cribs. Zero candidates pass the gates.

## Method

1. Build the numberings from the new word pool, 0-based and 1-based.
2. For each block size, alignment and direction, list the whole crib blocks.
3. Solve plain and affine forms exactly; reject on inconsistency.
4. Decrypt with each solution and submit; the gates test the partial-block cribs.
5. Record per setting how many blocks were available and whether they agreed.

## Result

Candidates returned: 50. Passed all gates: 0. Best crib hits among all candidates: 21/24
(EAST 4/4, NORTHEAST 8/9, BERLIN 4/6, CLOCK 5/5).
Best loss: 34.890409444858584 (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: 0034-complete-the-key-at-surviving-periods.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | cribs | 16/24 |  | `GCICLIOUNBXKIRKOSXJYZPPITNORTHEAYXEKOAGPUCQHCMKWTIUELZRHHTRSLBQAERLINCLOWNVFSXHLDORHQDDEKPUEFSWZR` | Hill 4x4 BREACH0 offset 0 enc; M=[[15, 11, 15, 7], [0, 21, 10, 15], [5, 22, 23, 23], [6, 12, 7, 19]] |
| 2 | cribs | 16/24 |  | `GCICLIOUNBXKIRKOSXJYZPPITNORTHEAYXEKOAGPUCQHCMKWTIUELZRHHTRSLBQAERLINCLOWNVFSXHLDORHQDDEKPUEFSWZR` | Hill 4x4 BREACH0 offset 0 dec; M=[[2, 0, 3, 23], [3, 18, 21, 14], [21, 19, 13, 19], [13, 9, 7, 18]] |
| 3 | cribs | 17/24 |  | `OBKOPDDUHSVXJLCGFFTLPOASTNORTHEQMYQGEEMVPMCYUOZTNZQISZXCRLYGFTGBERLINCLCBUWZOODQFAYADNERFFZFRVKAR` | Hill 4x4 BUT0 offset 3 enc; M=[[16, 6, 3, 2], [18, 19, 11, 23], [3, 5, 0, 13], [8, 2, 8, 11]] |
| 4 | cribs | 17/24 |  | `OBKOPDDUHSVXJLCGFFTLPOASTNORTHEQMYQGEEMVPMCYUOZTNZQISZXCRLYGFTGBERLINCLCBUWZOODQFAYADNERFFZFRVKAR` | Hill 4x4 BUT0 offset 3 dec; M=[[9, 21, 25, 10], [5, 3, 6, 7], [17, 4, 12, 24], [18, 12, 24, 19]] |
| 5 | cribs | 21/24 |  | `OKFAVVMIRTTUCKWSGSHKCEASTNORTHEASHUMXBYAVBPQCUUFFYPBKMNANVORFFSIMRLINCLOCKPONGVHLIAEXSGXZXMPRQJDO` | Hill 4x4 affine CAIRO0 offset 1 enc; M=[[24, 0, 7, 24], [25, 8, 6, 25], [5, 21, 6, 4], [13, 10, 24, 6]] v=[12, 1, 23, 24] |
| 6 | cribs | 20/24 |  | `OZVAFVMIRDDULZGSWSHKCEASTNORTHEASXEMHBYAVSRQLUUFFYPBKAIAIFQRVFSIMRLINCLOCZROIGVHLNMEHBWXKXMPROYDQ` | Hill 4x4 affine CAIRO0 offset 1 enc; M=[[24, 0, 7, 24], [25, 8, 6, 25], [5, 21, 6, 4], [0, 10, 24, 19]] v=[12, 1, 23, 24] |
| 7 | cribs | 21/24 |  | `OKVAVVMIRTDUCKGSGSHKCEASTNORTHEASHEMXBYAVBRQCUUFFYPBKMIANVQRFFSIMRLINCLOCKRONGVHLIMEXSWXZXMPRQYDO` | Hill 4x4 affine CAIRO0 offset 1 enc; M=[[24, 0, 7, 24], [25, 8, 6, 25], [18, 21, 6, 17], [13, 10, 24, 6]] v=[12, 1, 23, 24] |
| 8 | cribs | 20/24 |  | `OZFAFVMIRDTULZWSWSHKCEASTNORTHEASXUMHBYAVSPQLUUFFYPBKANAIFORVFSIMRLINCLOCZPOIGVHLNAEHBGXKXMPROJDQ` | Hill 4x4 affine CAIRO0 offset 1 enc; M=[[24, 0, 7, 24], [25, 8, 6, 25], [18, 21, 6, 17], [0, 10, 24, 19]] v=[12, 1, 23, 24] |
| 9 | cribs | 21/24 |  | `OKFMVVMIRTTECKWBGSHKCEASTNORTHEASHUAXBYAVBPOCUUFFYPBKMNMNVOPFFSIMRLINCLOCKPQNGVHLIAUXSGHZXMPRQJTO` | Hill 4x4 affine CAIRO0 offset 1 enc; M=[[11, 0, 7, 11], [25, 8, 6, 25], [5, 21, 6, 4], [13, 10, 24, 6]] v=[12, 1, 23, 24] |
| 10 | cribs | 20/24 |  | `OZVMFVMIRDDELZGBWSHKCEASTNORTHEASXEAHBYAVSROLUUFFYPBKAIMIFQPVFSIMRLINCLOCZRQIGVHLNMUHBWHKXMPROYTQ` | Hill 4x4 affine CAIRO0 offset 1 enc; M=[[11, 0, 7, 11], [25, 8, 6, 25], [5, 21, 6, 4], [0, 10, 24, 19]] v=[12, 1, 23, 24] |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "Hill cipher, block sizes 2-4, plain and affine, solved from crib blocks",
 "numberings": [
  "ABOUT0",
  "ABOUT1",
  "ABSENCE0",
  "ABSENCE1",
  "AIR0",
  "AIR1",
  "AND0",
  "AND1",
  "ANYTHING0",
  "ANYTHING1",
  "BETWEEN0",
  "BETWEEN1",
  "BREACH0",
  "BREACH1",
  "BUT0",
  "BUT1",
  "CAIRO0",
  "CAIRO1",
  "CAN0",
  "CAN1",
  "CANDLE0",
  "CANDLE1",
  "CAUSED0",
  "CAUSED1",
  "CHAMBER0",
  "CHAMBER1",
  "CORNER0",
  "CORNER1",
  "DEBRIS0",
  "DEBRIS1",
  "DEGREES0",
  "DEGREES1",
  "DELIVER0",
  "DELIVER1",
  "DELIVERING0",
  "DELIVERING1",
  "DETAILS0",
  "DETAILS1",
  "DOES0",
  "DOES1",
  "DOORWAY0",
  "DOORWAY1",
  "EARTHS0",
  "EARTHS1",
  "EIGHT0",
  "EIGHT1",
  "EMERGED0",
  "EMERGED1",
  "ENCUMBERED0",
  "ENCUMBERED1",
  "ESCAPING0",
  "ESCAPING1",
  "EXACT0",
  "EXACT1",
  "FIELD0",
  "FIELD1",
  "FIFTY0",
  "FIFTY1",
  "FIVE0",
  "FIVE1",
  "FLAME0",
  "FLAME1",
  "FLICKER0",
  "FLICKER1",
  "FORTY0",
  "FORTY1",
  "FOUR0",
  "FOUR1",
  "FROM0",
  "FROM1",
  "GATHERED0",
  "GATHERED1",
  "HAND0",
  "HAND1",
  "HANDS0",
  "HANDS1",
  "HIS0",
  "HIS1",
  "HOLE0",
  "HOLE1",
  "HOT0",
  "HOT1",
  "HOWS0",
  "HOWS1",
  "INFORMATION0",
  "INFORMATION1",
  "INSERTED0",
  "INSERTED1",
  "ITS0",
  "ITS1",
  "KNOW0",
  "KNOW1",
  "KNOWS0",
  "KNOWS1",
  "LAST0",
  "LAST1",
  "LEFT0",
  "LEFT1",
  "LIES0",
  "LIES1",
  "LIGHT0",
  "LIGHT1",
  "LITTLE0",
  "LITTLE1",
  "LOWER0",
  "LOWER1",
  "LUXOR0",
  "LUXOR1",
  "MADE0",
  "MADE1",
  "MINUTES0",
  "MINUTES1",
  "MIST0",
  "MIST1",
  "NOVEMBER0",
  "NOVEMBER1",
  "NUANCE0",
  "NUANCE1",
  "ONLY0",
  "ONLY1",
  "OUT0",
  "OUT1",
  "PART0",
  "PART1",
  "PASSAGE0",
  "PASSAGE1",
  "PEERED0",
  "PEERED1",
  "POINT0",
  "POINT1",
  "POSSIBLE0",
  "POSSIBLE1",
  "PRESENTLY0",
  "PRESENTLY1",
  "REMAINS0",
  "REMAINS1",
  "REMOVED0",
  "REMOVED1",
  "ROOM0",
  "ROOM1",
  "ROWS0",
  "ROWS1",
  "SECONDS0",
  "SECONDS1",
  "SEVEN0",
  "SEVEN1",
  "SEVENTY0",
  "SEVENTY1",
  "SHADING0",
  "SHADING1",
  "SHOULD0",
  "SHOULD1",
  "SIX0",
  "SIX1",
  "SLOWLY0",
  "SLOWLY1",
  "SUBTLE0",
  "SUBTLE1",
  "THAT0",
  "THAT1",
  "THE0",
  "THE1",
  "THEN0",
  "THEN1",
  "THERE0",
  "THERE1",
  "THEY0",
  "THEY1",
  "THIRTY0",
  "THIRTY1",
  "THIS0",
  "THIS1",
  "TINY0",
  "TINY1",
  "TOTALLY0",
  "TOTALLY1",
  "TRANSMIT0",
  "TRANSMIT1",
  "TRANSMITTED0",
  "TRANSMITTED1",
  "TREMBLING0",
  "TREMBLING1",
  "UNKNOWN0",
  "UNKNOWN1",
  "UPPER0",
  "UPPER1",
  "USED0",
  "USED1",
  "WAS0",
  "WAS1",
  "WHO0",
  "WHO1",
  "WIDENING0",
  "WIDENING1",
  "WITH0",
  "WITH1",
  "WITHIN0",
  "WITHIN1",
  "YOU0",
  "YOU1"
 ],
 "alignments": "0..n-1",
 "directions": [
  "enc",
  "dec"
 ],
 "settings": 7200,
 "settings_solved": 557,
 "settings_consistent_on_all_crib_blocks": [
  {
   "numbering": "ABOUT0",
   "n": 4,
   "offset": 1,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  },
  {
   "numbering": "ABOUT0",
   "n": 4,
   "offset": 2,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  },
  {
   "numbering": "ABOUT1",
   "n": 4,
   "offset": 0,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1
  },
  {
   "numbering": "ABOUT1",
   "n": 4,
   "offset": 1,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  },
  {
   "numbering": "ABOUT1",
   "n": 4,
   "offset": 2,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  },
  {
   "numbering": "ABOUT1",
   "n": 4,
   "offset": 3,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1
  },
  {
   "numbering": "ABSENCE0",
   "n": 4,
   "offset": 1,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  },
  {
   "numbering": "ABSENCE0",
   "n": 4,
   "offset": 2,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  },
  {
   "numbering": "ABSENCE0",
   "n": 4,
   "offset": 3,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1
  },
  {
   "numbering": "ABSENCE1",
   "n": 4,
   "offset": 0,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1
  },
  {
   "numbering": "ABSENCE1",
   "n": 4,
   "offset": 1,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  },
  {
   "numbering": "ABSENCE1",
   "n": 4,
   "offset": 2,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  },
  {
   "numbering": "ABSENCE1",
   "n": 4,
   "offset": 3,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1
  },
  {
   "numbering": "AIR0",
   "n": 4,
   "offset": 2,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  },
  {
   "numbering": "AIR1",
   "n": 4,
   "offset": 2,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  },
  {
   "numbering": "AND0",
   "n": 4,
   "offset": 2,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  },
  {
   "numbering": "AND0",
   "n": 4,
   "offset": 3,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1
  },
  {
   "numbering": "AND1",
   "n": 4,
   "offset": 2,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  },
  {
   "numbering": "ANYTHING0",
   "n": 4,
   "offset": 0,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1
  },
  {
   "numbering": "ANYTHING0",
   "n": 4,
   "offset": 3,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1
  },
  {
   "numbering": "BETWEEN0",
   "n": 4,
   "offset": 3,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1
  },
  {
   "numbering": "BETWEEN1",
   "n": 4,
   "offset": 3,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1
  },
  {
   "numbering": "BREACH0",
   "n": 4,
   "offset": 0,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1,
   "english": [
    -7.575
   ]
  },
  {
   "numbering": "BREACH0",
   "n": 4,
   "offset": 0,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1,
   "english": [
    -7.575
   ]
  },
  {
   "numbering": "BREACH0",
   "n": 4,
   "offset": 2,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  },
  {
   "numbering": "BREACH0",
   "n": 4,
   "offset": 3,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1
  },
  {
   "numbering": "BREACH1",
   "n": 4,
   "offset": 2,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  },
  {
   "numbering": "BUT0",
   "n": 4,
   "offset": 3,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1,
   "english": [
    -7.693
   ]
  },
  {
   "numbering": "BUT0",
   "n": 4,
   "offset": 3,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1,
   "english": [
    -7.693
   ]
  },
  {
   "numbering": "BUT1",
   "n": 4,
   "offset": 3,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1
  },
  {
   "numbering": "CAIRO0",
   "n": 4,
   "offset": 0,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1
  },
  {
   "numbering": "CAIRO0",
   "n": 4,
   "offset": 1,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 16,
   "english": [
    -7.109,
    -7.42,
    -7.067,
    -7.181,
    -7.266,
    -7.315,
    -7.188,
    -7.277
   ]
  },
  {
   "numbering": "CAIRO0",
   "n": 4,
   "offset": 1,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 16,
   "english": [
    -7.067,
    -7.188,
    -7.109,
    -7.266,
    -7.42,
    -7.315,
    -7.181,
    -7.277
   ]
  },
  {
   "numbering": "CAIRO0",
   "n": 4,
   "offset": 2,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  },
  {
   "numbering": "CAIRO0",
   "n": 4,
   "offset": 3,
   "direction": "enc",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1,
   "english": [
    -7.554
   ]
  },
  {
   "numbering": "CAIRO0",
   "n": 4,
   "offset": 3,
   "direction": "dec",
   "affine": false,
   "crib_blocks": 4,
   "solutions": 1,
   "english": [
    -7.554
   ]
  },
  {
   "numbering": "CAIRO1",
   "n": 4,
   "offset": 1,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 16,
   "english": [
    -7.109,
    -7.42,
    -7.067,
    -7.181,
    -7.266,
    -7.315,
    -7.188,
    -7.277
   ]
  },
  {
   "numbering": "CAIRO1",
   "n": 4,
   "offset": 1,
   "direction": "dec",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 16,
   "english": [
    -7.109,
    -7.266,
    -7.067,
    -7.188,
    -7.181,
    -7.277,
    -7.42,
    -7.315
   ]
  },
  {
   "numbering": "CAIRO1",
   "n": 4,
   "offset": 2,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  },
  {
   "numbering": "CAN0",
   "n": 4,
   "offset": 1,
   "direction": "enc",
   "affine": true,
   "crib_blocks": 5,
   "solutions": 1
  }
 ],
 "settings_inconsistent": 5843,
 "log_size": 7200,
 "numberings_count": 200
}
```

Notes: 7200 settings; 557 consistent with every whole crib block; 346 decryptions submitted.


