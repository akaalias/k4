# 0060-k2-coordinates-as-hill-matrix: The map reference at the end of K2, used as the number table of a Hill cipher

**Family:** 8-hill-polygraphic  
**Parent:** 0015-hill-solved-from-crib-blocks  
**Decision:** reverted  
**Run:** 2026-10-15T12:26:36+00:00, 5.1 s, status ran  
**Time by phase:** design 0 s, implement 0 s, test 0 s, run 5 s, record 0 s

## In plain words

K2 ends with a map reference: 38 degrees 57 minutes 6.5 seconds north, 77 degrees 8 minutes 44 seconds west. A Hill cipher mixes letters two or three at a time using a small square of numbers, and the map reference is a ready-made list of numbers. So we pour those numbers into the square in every sensible order, use it to unmix the copper, and count how many of the 24 known letters come out right. Random squares of numbers show what luck alone scores.

## Walkthrough, by hand

1. Take the first four numbers 38, 57, 6, 5 and reduce them mod 26: 12, 5, 6, 5.
2. Fill a 2x2 table by rows: top row 12 5, bottom row 6 5.
3. Number the letters A=0 to Z=25 and cut the copper into pairs from place 1.
4. Multiply each pair by the inverse of the table, mod 26, if the table has one (its determinant 12x5 - 5x6 = 30 = 4 mod 26 is even, so it has none and this reading can only encrypt).
5. Using the table to encrypt instead, look for the pair it would send to each carved pair.
6. Count how many of the 24 known letters land right.

## Worked example (generated)

```
first window 38 57 6 5 mod 26 = 12 5 6 5; by rows [[12, 5], [6, 5]]; determinant 4; inverse None
```

## Lineage

Inherits from 0015-hill-solved-from-crib-blocks. What changed: Experiments 24 and 38 used the K2 coordinates as a repeating string of digits added to the letters. A Hill cipher needs a small table of numbers instead, and the coordinates are exactly a short list of numbers, so here they fill the table directly, in every reading, and the 24 known letters judge it.

## Hypothesis (domain expert)

C23(b): the K2 coordinates 38 57 6.5 N, 77 8 44 W as a matrix. Hill encryption (C21) with a key matrix filled from the coordinates: 2x2 from every window of four in the number lists [38, 57, 6, 5, 77, 8, 44] and [38, 57, 65, 77, 8, 44] and the digit list 3 8 5 7 6 5 7 7 8 4 4, each forward and reversed, filled by rows or by columns; 3x3 from every window of nine; entries mod 26. Numberings A=0 and A=1 on the standard and KRYPTOS orders; every alignment; the matrix encrypting or decrypting (singular matrices skipped where an inverse is needed). Each setting decrypts K4 and the 24 cribs are counted. Control: the same count for 2,000 random invertible matrices per size under the same settings. Bounds: exact for these readings.

## Prediction

No coordinate matrix recovers more than four of the 24 known letters, the same as the best random matrices. Zero candidates pass.

## Method

1. List the coordinate readings.
2. Fill 2x2 and 3x3 matrices from every window, forward and reversed, by rows and columns.
3. For each numbering, alignment and direction, decrypt K4 and count crib hits.
4. Do the same with random invertible matrices.
5. Compare the best counts.

## Result

Candidates returned: 4. Passed all gates: 0. Best crib hits among all candidates: 4/24
(EAST 1/4, NORTHEAST 1/9, BERLIN 2/6, CLOCK 0/5).
Best loss: 204.303482107847 (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: 0034-complete-the-key-at-surviving-periods.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | cribs | 4/24 |  | `YRWHCIRXUXKLJNGHSJLEKBBMTLONHUMUQUCZQNGKLDQUCKPWGGTIMNOTOOCYRIFSCBLILFZQFNQAXFDYTICHYIOEZPQGCKKKR` | Hill from K2 coordinates, numbers window 1 by rows, std0, offset 0, matrix decrypts |
| 2 | cribs | 4/24 |  | `OMPMNZCGEKDHXYEYNLREJNZHTYOLTYDSUYESBWRXAOAWWJKOHLQYXQHMFWIBOLRMHRRHJZMTXYSJEJKNNMBMFAUXQGAMYUCVE` | Hill from K2 coordinates, numbers window 2 by rows, std1, offset 1, matrix encrypts |
| 3 | cribs | 4/24 |  | `YJYPEOHXYVAJZHURGPLWUFZSZDKVRMCAQGWNELOANTQGAUPEWOFUQFYNIYYKLEBQSTDIJZXOLBEYZRVSFUGLQICUZLSQAUCGR` | Hill from K2 coordinates, digits window 0 by rows, std0, offset 0, matrix encrypts |
| 4 | cribs | 4/24 |  | `YZWZCCRXUZKNJTGXSDLMKXBGTTOFHCMOQICLQPGULNQICAPOGYTWMVOZOECMRMFUCJLILLZSFZQCXTDETWCDYIOOZTQWCAKOR` | Hill from K2 coordinates, digits window 2 by columns, std0, offset 0, matrix decrypts |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "Hill with the key matrix filled from the K2 coordinates",
 "matrices": 72,
 "numberings": [
  "std0",
  "std1",
  "kry0",
  "kry1"
 ],
 "directions": 2,
 "best_hits": 4,
 "best_reading": "numbers window 1 by rows",
 "top": [
  {
   "hits": 4,
   "reading": "numbers window 1 by rows"
  },
  {
   "hits": 4,
   "reading": "numbers window 2 by rows"
  },
  {
   "hits": 4,
   "reading": "numbers reversed window 3 by rows"
  },
  {
   "hits": 4,
   "reading": "digits window 0 by rows"
  },
  {
   "hits": 4,
   "reading": "digits window 2 by columns"
  },
  {
   "hits": 4,
   "reading": "digits window 3 by rows"
  },
  {
   "hits": 4,
   "reading": "digits window 7 by rows"
  },
  {
   "hits": 4,
   "reading": "digits reversed window 4 by columns"
  }
 ],
 "control_best_2x2": 7,
 "control_best_3x3": 7,
 "control_mean_2x2": 2.72,
 "control_mean_3x3": 3.06,
 "control_matrices": {
  "2": 2000,
  "3": 2000
 }
}
```

Notes: 72 coordinate matrices; best 4/24 known letters (numbers window 1 by rows). Random invertible matrices under the same settings: 2x2 best 7 (mean 2.72), 3x3 best 7 (mean 3.06).


