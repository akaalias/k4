# 0223-rejudge-the-sampled-verdicts-completed-periodic-keys: A6.1, part 2: the completed periodic keys of 0034, 0035 and 0048 (lengths 27-29 on the sculpture's and the puzzle words' tables, and 0034's 53-95) rejudged blind: K4's saved readings against the same frozen searches' readings on 10 copies each

**Family:** 1-keyed-periodic  
**Parent:** 0221-rejudge-the-sampled-verdicts-free-alphabets-and-running-english  
**Decision:** reverted  
**Run:** 2026-10-27T10:22:49+00:00, 0.2 s, status ran  
**Time by phase:** unattributed 63 s, run 0 s, record 0 s

## In plain words

Three old experiments filled in long keys so that the carved letters read as much like English as possible, and compared the result with the same trick on scrambled copies using a simple letter-statistics score. That score is poor at telling damaged English from English-looking junk. Here the judge, a language model that reads one text at a time without knowing where it came from, reads the carved letters' readings and the copies' readings.

## Walkthrough, by hand

1. Take 0035's three readings of K4, one per key length 27, 28 and 29.
2. Take the same search's three readings of each of 10 scrambled copies.
3. Hide the 24 known letters and give all 33 readings to the judge one at a time, unlabelled.
4. Keep each text's best score.
5. K4 wins only if its best is above all 10 copies' bests.

## Worked example (generated)

```
0035's reading of K4 (period 27, plain std, cipher HILL/keyword, vig; 3 free slots climbed):
  reading      QGFMJOYSTOAEUHISNORDFEASTNORTHEASTSDKZSIZKIENYYISBUIIAWIVYLBOMOBERLINCLOCKFFEMXURMHAWYLVEERAJBUXH
  judge sees   QGFMJOYSTOAEUHISNORDF#############SDKZSIZKIENYYISBUIIAWIVYLBOMO###########FFEMXURMHAWYLVEERAJBUXH

  the judge reads it among 30 readings of 10 scrambled copies by the same search, one at a time, unlabelled.
```

## Lineage

Inherits from 0221-rejudge-the-sampled-verdicts-free-alphabets-and-running-english. What changed: A6.1 (Stage 2, step 4, issue #84), the second group of sampled verdicts. 0034 (one periodic key on the standard and KRYPTOS tables, 24 conventions, periods 27-29 and 53-95 every third), 0035 (27-29, one side keyword-mixed from the vocabulary) and 0048 (27-29, both sides keyword-mixed) completed the free key slots by a quadgram climb and compared K4's best with shuffled K4 by quadgram. Their copies were never kept, and their runs stopped on the clock, so they cannot be replayed letter for letter; but 0216 ran each frozen search unchanged on 10 fresh plain shuffles (tools/a13_check.py pass1-regen, seed 1300) and kept every reading (reports/a13-structure-data/pass1_copies.json). Here K4's saved readings and those copies' readings go to the judge in one blind call per experiment. 0037's sampled triples are not rejudged: F6.3b's close rests on 0158's exact count.

## Hypothesis (domain expert)

A6 (knowledge/12-assumptions.md); C27(c) and C5 for the tables (the keyword-mixed alphabets of 0035 and 0048), C19 for the judge's tolerance of X stops. Cells: 0034 at 27-29 (3 readings per text), 0034 at 53-95 (15 readings; already blocked by 0136's bound, judged for the record), 0035 at 27-29 (3), 0048 at 27-29 (3). Statistic per cell: the judge's (j3, Sonnet 5.5) best score over a text's readings; K4 counts only strictly above all 10 copies' bests; None as not found. Every reading of every text is sent (no quadgram cut, the same for K4 and copies). Four cells, chance about 4/11 = 0.36 cells with K4 above every copy; a flag needs p < 0.05/4, 80 copies, so a K4 above every copy here is a candidate to replicate on that cell against fresh copies, not a result.

## Prediction

K4 above every copy in no cell (chance 0.36). The copies' best judge scores are 20-50 at 53-95, where the climb fills 47-71 free letters with English-like fragments, and under 20 at 27-29, where only 3-5 letters are free. Zero candidates pass gate 4.

## Method

1. K4: the 24-of-24 readings saved in 0034 (18), 0035 (3), 0048 (3) raw.json.
2. Copies: the readings of the same frozen searches on 10 plain shuffles each, from pass1_copies.json.
3. One judge call per experiment on all of K4's and the copies' readings; per text and cell, the best score.
4. K4 counts only strictly above every copy's best.

## Result

Candidates returned: 24. Passed all gates: 0. Best crib hits among all candidates: 24/24
(EAST 4/4, NORTHEAST 9/9, BERLIN 6/6, CLOCK 5/5).
Best loss: 4.152943145900252 (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | baseline | 24/24 | -8.030 | `RPRESIDENTHESTHERESANEASTNORTHEASTDERSTHEPRESINTHEREARENTHERETHBERLINCLOCKERESIDEDINGTHETHEREARTI` | saved reading of 0034: period 95 key FALPWPOZKOFGDGYGYMDMJMCLWNQHMHLKFGXKQHZRHUEXABHQDWGHKKCPTKAYEAZBYHITCDFYZDATQMCOKGZPLS |
| 2 | baseline | 24/24 | -7.941 | `OFORESTINTEDINTHEARENEASTNORTHEASTTHESTHESTHERENTERSANDINGANDINBERLINCLOCKGSTANDTHERENTERSARETHAL` | saved reading of 0034: period 92 key KVUKDZQJQDDANGRPTOAWTRDUMRIYWOYNKYRJFXJMOHYMKZHSNVPDNXEUVQJVCWIELYOIECBAQKDASNSHKYXCTQ |
| 3 | baseline | 24/24 | -7.855 | `ISCOREATTHETHESTHEREAEASTNORTHEASTNDCONTHERESERINTHESTERANDERANBERLINCLOCKDRENTHEREARATERSTHEMARX` | saved reading of 0034: period 89 key NACPMJYYGVZKPKXKWQZMXQRTPHIUUARAYZSHZSHZXYXKDEQHKALUSKZBPUATKMVUGUHMRUKAFKAEONSFIHNKGN |
| 4 | baseline | 24/24 | -7.722 | `WAROUNTRETHEREATEDINTEASTNORTHEASTERESTOREASTEVERESANDINTHETHESBERLINCLOCKTATTHECONTHESTORATANAME` | saved reading of 0034: period 86 key IZHXAZWDYMNTQMMIWYHMXZPBYXYCCUYQABQYIZDWIOIAPUWFVEZRDSOKLHILUZROGCQPUQMJNAXUQJIHJFLQZY |
| 5 | baseline | 24/24 | -7.659 | `OAREACHALLIONTHEREINTEASTNORTHEASTHEWITHEARECOMENTHEREINTERESANBERLINCLOCKDRESTATINTHEDALECTINGMO` | saved reading of 0034: period 83 key JSRDFXJVYXNXFNCNCSAFWSJRXTUOSORAMNCAZEZBOGLYRONFQMDORNNDEXUPZOFICOPEJKMCZKGEUSUCPSE (5 |
| 6 | baseline | 24/24 | -7.617 | `BERSDATEDTOARELETHESTEASTNORTHEASTORESTHATTHEREATTHETHEAREANDINBERLINCLOCKTHERESANDITISREELETOURJ` | saved reading of 0034: period 80 key XXZVLYUUDKQKHVOGLYXCTBKVSBPCXFCTACADMYQSJQCSAZOSTDQFWDKDOWQWJXPLRCFPLJIHUATZZZOS (56 f |
| 7 | baseline | 24/24 | -7.495 | `TOVENOTHESTHERSTTHESAEASTNORTHEASTRERESIDENTERSAREARETOTHERATERBERLINCLOCKSONOFTHISFREETERSINEEDL` | saved reading of 0034: period 77 key HSUPMCUYLTXJVEGYTUVDPMCLWNQHMHLKFGFKQKXYGDAGNLNRQWVRTYNCMWQEKMCBYHITCDFYZDURP (53 free |
| 8 | baseline | 24/24 | -7.439 | `WHEUSHESTIONSTEONLYCOEASTNORTHEASTNTHETHESTATESTIMENTSANDINGATIBERLINCLOCKONTHEWARKENHISTHESOMESG` | saved reading of 0034: period 74 key LGZVHKFBYMIMUHPSIHZMLQTELWEHGZUPFHUIBBFTXDHEKZNUABBJSOGDXEPUSRFOGHTTKPBKSD (50 free sl |
| 9 | baseline | 24/24 | -7.598 | `HUKSALLTHAVICEFFICESAEASTNORTHEASTNATIONANDINATESTINANDATTHERESBERLINCLOCKENSTIONESERTERETOODSLCQ` | saved reading of 0034: period 71 key KSDEGWSDMKXVMAYZNVJUIQTELWEHGZUPFHUFMTEZYWBPEPUHJVTJPMDVTVBWFQUOGHTTKPB (47 free slots |
| 10 | baseline | 24/24 | -7.485 | `IRWAHOTALLISAREATHENTEASTNORTHEASTINANDSOMESANDINTHERENTHERSEARBERLINCLOCKSSIONESISSTINGETPVCHACT` | saved reading of 0034: period 68 key SDHLGKTHUVFNRRDEIXWHPREZYPYXXSYDKZSSVSGKUTHKTWVLCAFONAADRVOJCODFQXDE (44 free slots cl |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "item": "A6.1 (part 2)",
 "experiments": [
  "0034",
  "0035",
  "0048"
 ],
 "cells": 4,
 "flag_level": "p < 0.05 / 4; needs 80 copies",
 "copies": "0216's regeneration (tools/a13_check.py pass1-regen, seed 1300): each frozen search unchanged on 10 plain shuffles",
 "by_cell": {
  "0034 P53-95": {
   "k4_judge": 30,
   "k4_judge_reading": "IS IN G HIC NN JAR ISE Y UNDE ? NET IN THERE IN TED TO THE RECORDS ON ? HIM ? ? ?",
   "copies_best": [
    30,
    45,
    42,
    30,
    27,
    28,
    40,
    40,
    22,
    33
   ],
   "copies_max": 45,
   "k4_above_every_copy": false,
   "k4_rank": 8,
   "n_copies": 10,
   "readings_per_text": 15,
   "judge_none_in_call": 0
  },
  "0034 P27-29": {
   "k4_judge": 8,
   "k4_judge_reading": "? LEVES SIT MILAN BAC ? AT ? OF ?",
   "copies_best": [
    6,
    6,
    4,
    4,
    7,
    6,
    4,
    4,
    7,
    7
   ],
   "copies_max": 7,
   "k4_above_every_copy": true,
   "k4_rank": 1,
   "n_copies": 10,
   "readings_per_text": 3,
   "judge_none_in_call": 0
  },
  "0035 P27-29": {
   "k4_judge": 6,
   "k4_judge_reading": "? ? ? BUT THE ? ? ? SEA ? ? ? ?",
   "copies_best": [
    5,
    8,
    12,
    12,
    6,
    4,
    4,
    12,
    6,
    8
   ],
   "copies_max": 12,
   "k4_above_every_copy": false,
   "k4_rank": 8,
   "n_copies": 10,
   "readings_per_text": 3,
   "judge_none_in_call": 0
  },
  "0048 P27-29": {
   "k4_judge": 12,
   "k4_judge_reading": "? ? ? DEXZEMBER (DECEMBER?) ? ?",
   "copies_best": [
    8,
    12,
    6,
    8,
    12,
    8,
    12,
    12,
    12,
    7
   ],
   "copies_max": 12,
   "k4_above_every_copy": false,
   "k4_rank": 6,
   "n_copies": 10,
   "readings_per_text": 3,
   "judge_none_in_call": 0
  }
 },
 "k4_above_every_copy_cells": [
  "0034 P27-29"
 ],
 "chance_expected": 0.36,
 "judge_texts_sent": 264,
 "judge_calls_estimated": 264,
 "quadgram_cut": "none: every reading of K4 and of the copies sent",
 "not_rejudged": {
  "0037": "F6.3b's close rests on 0158's exact count (105.5 million routes); 0037 kept no reading"
 },
 "controls": "quadgram scores of every copy reading of the three searches (pass1_copies.json); each K4 reading faces its own experiment's copies among them (issue #88)",
 "exhaustive": false
}
```

Notes: 0034 P53-95: K4 30, copies best 45 (rank 8 of 11); 0034 P27-29: K4 8, copies best 7 (rank 1 of 11); 0035 P27-29: K4 6, copies best 12 (rank 8 of 11); 0048 P27-29: K4 12, copies best 12 (rank 6 of 11)


