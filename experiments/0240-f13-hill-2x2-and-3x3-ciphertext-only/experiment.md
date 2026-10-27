# 0240-f13-hill-2x2-and-3x3-ciphertext-only: F13.4e, Hill: 2x2 and 3x3, plain or affine, four letter numberings, every block alignment, solved from the ciphertext alone row by row; K4 against 100 shuffles, plants of both sizes

**Family:** 13-ciphertext-only  
**Parent:** 0234-f13-periodic-key-on-the-sculptures-tables-ciphertext-only  
**Decision:** reverted  
**Run:** 2026-10-27T21:54:52+00:00, 681.9 s, status ran  
**Time by phase:** implement 63 s, test 155 s, run 682 s, record 43 s

## In plain words

A Hill cipher mixes letters in blocks of two or three using a small table of numbers. Without any known word it can still be broken one row of the table at a time: each row decides every second (or third) letter, so we try every possible row and keep those whose letters look like English, then put the best rows together. We do it for K4, for shuffles of K4 and for hidden test messages.

## Walkthrough, by hand

1. Number the letters, say A = 0 to Z = 25, and cut the carved text into blocks of three.
2. One row of the unknown decoding table turns each block into one message letter: try all 26 x 26 x 26 rows (and a shift) and keep the 40 whose letters look most like English.
3. Do the same for the other two rows.
4. Try every way of putting three kept rows together, read the whole text and keep the most English.
5. Compare K4's best with what shuffles of K4 reach.

## Worked example (generated)

```
Row by row on a planted 2x2 Hill message (A = 0, matrix [[3, 3], [2, 5]]), no known letter:

  carved     VEEIFTMNEYMIAMQGBMLGFKJGPFAOFTPSKGHDBMPWTHFKEGOXQCDCWPDPAVKWVAAAUBLPAVBHXXHBAVRZAKTUUBNFNNZDKIZVW
  rows found [[15, 17], [20, 9]], offsets [0, 0]; true inverse [[15, 17], [20, 9]]
  reading    TOOWILLTAKEAWEEKLYHOLIDAYHEWILLUSUALLYBEOBLIGEDTOABANDONTHEIDEAAFTERTHEFIRSTTHETOMBOFTUTANKHAMENW
```

## Lineage

Inherits from 0234-f13-periodic-key-on-the-sculptures-tables-ciphertext-only. What changed: F13.4e (issue #85), the Hill part. 0015 and 0105 killed every 2x2-4x4 Hill setting under the four standard numberings with the known letters; here they are not read. The classic ciphertext-only attack: each row of the decryption matrix (and its affine term) acts alone on every nth letter, so all 26^(n+1) rows are scored by the fit of their letters to English letter counts and the 2,000 best kept per row; rows are joined by a beam (bigram, then trigram fit inside blocks), the best invertible matrices scored by quadgrams and refined row by row, the best per setting rescored by MIX8m (F13.3). Changed before the run after dry runs: a sum of letter log-frequencies let rows that map every letter to E win, and 40 rows per row lost the true 3x3 rows (ranked 4-3,625 of 456,976). Settings: size 2 or 3, numbering standard or KRYPTOS order from 0 or from 1, block alignment 0..n-1: 20 cells. Statistic, copies and plants as 0234 (K4 against 100 shuffles; 8 plants per size, each against 10 own shuffles).

## Hypothesis (domain expert)

F8 (the HILL column, C21(a); Bauer's matrix conjecture) read without the known letters: the hedge for A2/A1 on a family the known letters killed exactly. F13.1 puts 3x3 Hill with an unknown numbering at 131 bits, under MIX8m's 189; with the four standard numberings it is 23-37 bits plus the alignment. The row-by-row attack is exact per row; with 32 letters per row the true row ranks in the hundreds or thousands of 456,976, so the beam keeps 2,000 per row, and the plants measure what is lost. Pre-registered: S = max z over the 20 cells against K4's 100 shuffles; K4 flags at p < 0.05; a size is decided when 6 of its 8 plants are above all 10 own shuffles.

## Prediction

Plants found 8/8 at 2x2 and most at 3x3 (32 letters per row is enough for letter counts to keep the true row among 40). K4 inside its shuffles (p above 0.05); readings at most 4-5 known letters. F8's Hill part closes ciphertext-only for the four numberings.

## Method

1. Numberings: A=0 or A=1 on the standard or the KRYPTOS order. Alignments 0..n-1; letters outside whole blocks pass unchanged.
2. Per setting and row r: every (d_r1..d_rn, e_r) mod 26 scored by the English letter log-frequency of the letters it yields, plus the entropy of those letters (the fit of their counts to English, so a row that maps every letter to E does not win); the 2,000 best kept.
3. Rows joined by a beam: pairs of rows by English bigram fit inside each block (3,000 kept), the third row by trigram fit (3,000 kept), the 300 best invertible matrices scored by quadgrams on the whole text, the 20 best refined by swapping in any kept row while the score rises; the best rescored by MIX8m.
4. S = max z over 20 cells against K4's 100 shuffles; plants (random matrix, numbering, alignment, half affine) against 10 own shuffles each.
5. K4's best reading per cell submitted (key: size, numbering, alignment, matrix, offset).

## Result

Candidates returned: 16. Passed all gates: 0. Best crib hits among all candidates: 3/24
(EAST 2/4, NORTHEAST 1/9, BERLIN 0/6, CLOCK 0/5).
Best loss: 212.84664080922258 (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | cribs | 2/24 |  | `YWAQMPTFCKSEDPEYCWLWAKLETTSGHEWVITOKYSMRRHITATTEKJLAMUISMVUVFONOCONEFLHARRYFPFXOLASAARUBNLORATYPR` |  |
| 2 | cribs | 0/24 |  | `OGASWTNKTOUTWONMSBAUIRYROGHPEUYMVONWWCSTBERYPFROSHLEMAAOGENLTBACKLYZULHNSIPPFFRLAMYOGIBBHILEFCTJB` |  |
| 3 | cribs | 2/24 |  | `YWAQMPTFCKSEDPEYCWLWAKLETTSGHEWVITOKYSMRRHITATTEKJLAMUISMVUVFONOCONEFLHARRYFPFXOLASAARUBNLORATYPR` |  |
| 4 | cribs | 0/24 |  | `OGASWTNKTOUTWONMSBAUIRYROGHPEUYMVONWWCSTBERYPFROSHLEMAAOGENLTBACKLYZULHNSIPPFFRLAMYOGIBBHILEFCTJB` |  |
| 5 | cribs | 1/24 |  | `VIOENXENDACWALHAYEWDAMIHOPREERBYTHPENWEPSSFORNTVDREOGOHEENGLYOPEAGIOPLRLCRDDEOMYLEACRITRISTOTJIRR` |  |
| 6 | cribs | 0/24 |  | `OOKIRBERPOINGTPKODOCSYNEOLFOIEDEHZTRNTITLITSTNUOFARATTDJURTHEVEWAFIAUFNEUSTRISEVEALLLINNHOBETNHPE` |  |
| 7 | cribs | 2/24 |  | `OBWQNCOZSWHOHAAARDBOTODATIPYPERDSKILHRLIESIEVESUNDEHEBBRESCLSPMLOFREPRTENGBAILIBSHEIFTRACYEAGESAR` |  |
| 8 | cribs | 1/24 |  | `VIOENXENDACWALHAYEWDAMIHOPREERBYTHPENWEPSSFORNTVDREOGOHEENGLYOPEAGIOPLRLCRDDEOMYLEACRITRISTOTJIRR` |  |
| 9 | cribs | 0/24 |  | `OOKIRBERPOINGTPKODOCSYNEOLFOIEDEHZTRNTITLITSTNUOFARATTDJURTHEVEWAFIAUFNEUSTRISEVEALLLINNHOBETNHPE` |  |
| 10 | cribs | 2/24 |  | `OBWQNCOZSWHOHAAARDBOTODATIPYPERDSKILHRLIESIEVESUNDEHEBBRESCLSPMLOFREPRTENGBAILIBSHEIFTRACYEAGESAR` |  |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "item": "F13.4e (Hill)",
 "search_reads_known_letters": false,
 "cells": [
  "2x2 std0 align 0",
  "2x2 std0 align 1",
  "2x2 std1 align 0",
  "2x2 std1 align 1",
  "2x2 kry0 align 0",
  "2x2 kry0 align 1",
  "2x2 kry1 align 0",
  "2x2 kry1 align 1",
  "3x3 std0 align 0",
  "3x3 std0 align 1",
  "3x3 std0 align 2",
  "3x3 std1 align 0",
  "3x3 std1 align 1",
  "3x3 std1 align 2",
  "3x3 kry0 align 0",
  "3x3 kry0 align 1",
  "3x3 kry0 align 2",
  "3x3 kry1 align 0",
  "3x3 kry1 align 1",
  "3x3 kry1 align 2"
 ],
 "beam": {
  "rows": 2000,
  "pairs": 3000,
  "triples": 3000,
  "full": 300
 },
 "affine": true,
 "texts": 277,
 "k4_copies": 100,
 "k4_statistic": 0.902,
 "k4_best_cell": "2x2 kry0 align 0",
 "k4_p": 0.7327,
 "copies_statistic_median": 1.474,
 "copies_statistic_max": 3.98,
 "plant_power": {
  "2": [
   8,
   8
  ],
  "3": [
   4,
   8
  ]
 },
 "plant_exact_recovery": {
  "2": [
   8,
   8
  ],
  "3": [
   2,
   8
  ]
 },
 "k4_best_reading": "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR",
 "exhaustive": "per row exact; rows joined by a beam of 2,000 rows, 3,000 pairs and triples, 300 matrices, 20 refined",
 "compute_seconds": 657
}
```

Notes: K4 statistic 0.90 at 2x2 kry0 align 0, p 0.733; plant power 2x2 8/8, 3x3 4/8; read exactly 8/8, 2/8


