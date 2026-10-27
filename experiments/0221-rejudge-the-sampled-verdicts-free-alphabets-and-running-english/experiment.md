# 0221-rejudge-the-sampled-verdicts-free-alphabets-and-running-english: A6.1, part 1: the sampled verdicts of 0120, 0125, 0140, 0142, 0144 and 0146 rerun unchanged from their frozen searches, with every best reading (K4's, the copies', the plants') read by the blind judge instead of quadgrams

**Family:** 1-keyed-periodic  
**Parent:** 0140-k4-against-its-own-copies-with-the-tempering-climb  
**Decision:** reverted  
**Run:** 2026-10-27T09:20:31+00:00, 3242.8 s, status ran  
**Time by phase:** test 155158 s, design 137 s, implement 16 s, run 3243 s, record 0 s

## In plain words

Several earlier experiments could not decide a question exactly, so they let a computer adjust the key for the best-looking English on the carved letters and on scrambled copies of them, and compared the two with a simple letter-statistics score. That score turned out to be poor at spotting damaged English, with missing words, X's between words or a few wrong letters. Here we rerun those same searches exactly as they were and let the judge, a language model that reads one text at a time without knowing where it came from, score the carved letters' reading and the copies' readings side by side.

## Walkthrough, by hand

1. Take one earlier verdict, say 0140: K4 and 12 scrambled copies, each with a key climbed for English.
2. Rerun that exact search, same random seeds, so every reading comes out as it did.
3. Check that K4's reading is letter for letter the one in 0140's record.
4. Hide the 24 known letters in each reading and give the 13 readings to the judge one at a time, unlabelled.
5. K4 wins the cell only if its score is above all 12 copies' scores.

## Worked example (generated)

```
A6.1 rejudges a climbed reading. 0140's reading of K4 at key length 23 (one alphabet, Beaufort form):

  reading      BOARIMELRBCEHINVEHWATEASTNORTHEASTHATEGNANHIFPLLBADIRODMOROSORYBERLINCLOCKDAVARRUNDISHEDSAVEANLAP
  judge sees   BOARIMELRBCEHINVEHWAT#############HATEGNANHIFPLLBADIRODMOROSORY###########DAVARRUNDISHEDSAVEANLAP

  quadgram mean -4.9891, rank 9 of 13 among its own copies
  the judge reads the same 13 readings, one at a time, unlabelled; K4 must score above all 12 copies.
```

## Lineage

Inherits from 0140-k4-against-its-own-copies-with-the-tempering-climb. What changed: A6.1 (Stage 2, step 4, issue #84). Every sampled close in F1 compared K4's climbed reading with the copies' climbed readings by quadgram score, and the judge bench (reports/judge-bench.md) shows quadgrams find none of the damaged classes against English-like junk, which is what a climb returns on a copy. Here the six verdicts of F1.1 (0120 at 23 and 26, 0140 at 23, 0142 at 26), F1.2 (0144 at 13 and 16, 0146 at 8) and F1.3 (0125) are rejudged: each frozen attack.py is run unchanged with its own seeds (nothing was saved but K4's reading and the copies' scores), its process pool intercepted to keep every job's reading, K4's reading checked against the record, and K4's, the copies' and the in-run plants' best readings read by the judge, one blind call per verdict.

## Hypothesis (domain expert)

A6 and A13 (knowledge/12-assumptions.md): the sampled closes of F1.1 (one free alphabet, Beaufort form, key lengths 23 and 26: 0120, 0140, 0142), F1.2 (two free alphabets, lengths 8, 13, 16: 0144, 0146) and F1.3 (a running key from an unknown English text on the 208,062 dictionary tables: 0125) rest on the quadgram mean of a climbed reading. C5 and C27(c) (a keyed alphabet 'slightly different' from KRYPTOS, the K1/K2 system) are the clues those closes read; C19 (X stops, Scheidt 2015) and the bench's damaged classes are why the score is in doubt. Statistic per verdict: the judge's score (j3, Sonnet 5.5, kryptos/judge.py) of K4's best reading against the best of each copy's, copies made by the frozen code (0119's exact decider for 0120/0140/0142, kept-place shuffles for 0144/0146, plain shuffles for 0125), K4 counting only strictly above every copy, None as not found. 0125's reading is the forced running-key stretch (24 letters at 22-34 and 64-74), shown to the judge at places 35-47 and 49-59 with '?' elsewhere so its masking of the known places does not hide it. Eight cells; chance puts K4 above all 12 (50) copies with p = 1/13 (1/51) each, about 0.6 cells in all; a cell flags at p < 0.05 / 8, which needs 160 copies: a K4 above every copy here is a candidate for that replication, not a result.

## Prediction

K4's reading scores above every copy's in none of the 8 cells (chance expects 0.6). K4's six saved readings are reproduced exactly. The judge finds at most as many of 0120's and 0140's planted texts as quadgrams did (0120: 3 of 6 at 23, 1 of 6 at 26; 0140: 5 of 6), because their climbed readings are only a third right (29-43 of 97 letters), and at least the 11 of 0125's 20 planted running keys that quadgrams found. Zero candidates pass gate 4.

## Method

1. For 0142, 0146, 0125, 0140, 0144, 0120 in that order: load the frozen attack.py and call its run() with the harness's context and a far deadline (every original run finished all its restarts), the process pool replaced by one that runs the same jobs and keeps each job and result.
2. Check K4's reading equals the record's, and the copies' quadgram scores equal the record's.
3. Per verdict, one judge call on K4's best reading and every copy's; per plant group, one call on the plants' readings and their own copies'.
4. K4 counts only strictly above every copy; a plant counts as found by the judge strictly above every copy it was compared with in its experiment (0120: K4's copies at its length; 0140: its own six; 0125: the 50 copies).

## Result

Candidates returned: 4. Passed all gates: 0. Best crib hits among all candidates: 24/24
(EAST 4/4, NORTHEAST 9/9, BERLIN 6/6, CLOCK 5/5).
Best loss: 4.093797326690993 (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | baseline | 24/24 | -7.925 | `WRYZNNIPNMUPTOMEORJZEEASTNORTHEASTRBYEASILETFIPLSNGESMUCHASTDCEBERLINCLOCKHASANDWLANDWOHLUCEKSENP` | saved reading of 0120: Beaufort form, one alphabet JCRBOQYZPXVWHSMGAUKNFTIELD on both sides, key length 23 |
| 2 | baseline | 24/24 | -7.549 | `QBHEFEULCLATLYEPHUVALEASTNORTHEASTPOILTYNESTUCOOTEVELHOURKMRTISBERLINCLOCKTBYINAROMTHEENEIGNORGHF` | saved reading of 0120: Beaufort form, one alphabet NDPEAFCIXWRMUHGYZKOBTJVSQL on both sides, key length 26 |
| 3 | baseline | 24/24 | -7.390 | `BOARIMELRBCEHINVEHWATEASTNORTHEASTHATEGNANHIFPLLBADIRODMOROSORYBERLINCLOCKDAVARRUNDISHEDSAVEANLAP` | saved reading of 0140: Beaufort form, one alphabet RTKDPNVSXJQMUAZGOBILEYCHWF on both sides, key length 23 |
| 4 | baseline | 24/24 | -7.490 | `QINARCEOUSEAZEYNONENGEASTNORTHEASTEDTUDECRSABSOSCIVEFUSSHKRLDRABERLINCLOCKCLARINRUNGONTAGTOLEMASC` | saved reading of 0142: Beaufort form, one alphabet UTVXRSWEPNHFLZDAOQBJICKGYM on both sides, key length 26 |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "rejudging F1.1, F1.2, F1.3's sampled verdicts with the blind judge (A6.1, part 1)",
 "verdicts": [
  "0142",
  "0146",
  "0125",
  "0140",
  "0144",
  "0120"
 ],
 "cells": 8,
 "flag_level": "p < 0.05 / 8; needs 160 copies per cell",
 "judge_calls_estimated": 216,
 "judge_texts_sent": 290,
 "runs": {
  "0142": {
   "seconds": 124,
   "jobs": 13,
   "checks": {
    "runs_done": [
     10
    ],
    "decryption_checked": true,
    "k4_reading_reproduced_26": true,
    "copies_scores_reproduced_26": true
   }
  },
  "0146": {
   "seconds": 444,
   "jobs": 13,
   "checks": {
    "runs_done": [
     10
    ],
    "decryption_checked": true,
    "k4_reading_reproduced_8": true,
    "copies_scores_reproduced_8": true
   }
  },
  "0125": {
   "seconds": 333,
   "jobs": 71,
   "checks": {
    "k4_reading_reproduced": true,
    "copies_scores_reproduced": true
   }
  },
  "0140": {
   "seconds": 683,
   "jobs": 55,
   "checks": {
    "runs_done": [
     10
    ],
    "decryption_checked": true,
    "k4_reading_reproduced_23": true,
    "copies_scores_reproduced_23": true
   }
  },
  "0144": {
   "seconds": 687,
   "jobs": 26,
   "checks": {
    "runs_done": [
     10
    ],
    "decryption_checked": true,
    "k4_reading_reproduced_13": true,
    "copies_scores_reproduced_13": true,
    "k4_reading_reproduced_16": true,
    "copies_scores_reproduced_16": true
   }
  },
  "0120": {
   "seconds": 778,
   "jobs": 38,
   "checks": {
    "k4_reading_reproduced_23": true,
    "k4_reading_reproduced_26": true
   }
  }
 },
 "by_cell": [
  {
   "cell": "0142 L26",
   "k4_judge": 6,
   "k4_judge_reading": "? NONE ? FUSS ? CLARIN RUNG ON TAG TO ?",
   "copies_judge": [
    12,
    12,
    6,
    12,
    6,
    15,
    7,
    6,
    14,
    12,
    12,
    7
   ],
   "copies_best": 15,
   "k4_above_every_copy": false,
   "k4_rank": 13,
   "n_copies": 12,
   "none": 0,
   "k4_reading": "QINARCEOUSEAZEYNONENGEASTNORTHEASTEDTUDECRSABSOSCIVEFUSSHKRLDRABERLINCLOCKCLARINRUNGONTAGTOLEMASC"
  },
  {
   "cell": "0146 L8",
   "k4_judge": 8,
   "k4_judge_reading": "? BURGH ? TO FLY ? KINGS ADVER ? AVE ? QUO DEMO GOOF GLA",
   "copies_judge": [
    12,
    6,
    12,
    6,
    12,
    12,
    8,
    12,
    8,
    8,
    8,
    12
   ],
   "copies_best": 12,
   "k4_above_every_copy": false,
   "k4_rank": 11,
   "n_copies": 12,
   "none": 0,
   "k4_reading": "ZEMYBMWDBURGHAPTGCWEDEASTNORTHEASTYIDWCKUNDTOFLYPSHAYKINGSADVERBERLINCLOCKAVEFLIVATQUODEMOGOOFGLA"
  },
  {
   "cell": "0125 running key",
   "k4_judge": 8,
   "k4_judge_reading": "? CEFEEREDADFIZ ? GWENT ACT TWI ?",
   "copies_judge": [
    7,
    22,
    12,
    6,
    8,
    8,
    8,
    12,
    12,
    15,
    12,
    12,
    15,
    12,
    12,
    6,
    12,
    12,
    7,
    12,
    14,
    15,
    15,
    12,
    10,
    8,
    4,
    6,
    12,
    6,
    6,
    8,
    12,
    8,
    12,
    12,
    14,
    8,
    12,
    12,
    12,
    22,
    8,
    8,
    22,
    12,
    6,
    12,
    8,
    8
   ],
   "copies_best": 22,
   "k4_above_every_copy": false,
   "k4_rank": 42,
   "n_copies": 50,
   "none": 0,
   "k4_reading": "??????????????????????????????????CEFEEREDADFIZ?GWENTACTTWI??????????????????????????????????????"
  },
  {
   "cell": "0140 L23",
   "k4_judge": 12,
   "k4_judge_reading": "BOAR I MEL ? ? ? ? HATE ? ? BAD ? ? ? SORY ? ? ? RUN DISHED SAVE AN LAP",
   "copies_judge": [
    12,
    12,
    12,
    14,
    7,
    18,
    8,
    12,
    10,
    8,
    6,
    8
   ],
   "copies_best": 18,
   "k4_above_every_copy": false,
   "k4_rank": 7,
   "n_copies": 12,
   "none": 0,
   "k4_reading": "BOARIMELRBCEHINVEHWATEASTNORTHEASTHATEGNANHIFPLLBADIRODMOROSORYBERLINCLOCKDAVARRUNDISHEDSAVEANLAP"
  },
  {
   "cell": "0144 L13",
   "k4_judge": 8,
   "k4_judge_reading": "DBUGHHPROLEITEDREOFVI ????? LY OWN EN WAS IN EN OH W CIT AFF MY S BUR ????? O BAY GUIOR Y FAKE LY US FUM WO",
   "copies_judge": [
    8,
    8,
    12,
    12,
    12,
    8,
    8,
    12,
    8,
    12,
    12,
    8
   ],
   "copies_best": 12,
   "k4_above_every_copy": false,
   "k4_rank": 13,
   "n_copies": 12,
   "none": 0,
   "k4_reading": "DBUGHHPROLEITEDREOFVIEASTNORTHEASTLYOWNENWASINENOHWCITAFFMYSBURBERLINCLOCKOBAYGUIORYFAKELYUSFUMWO"
  },
  {
   "cell": "0144 L16",
   "k4_judge": 8,
   "k4_judge_reading": "KDOW BOO OF GOL PRE AT IN CER ############# YIRTI DONT TO STEN EETS BE IP HYAVAM ########### Y WAS TILING LD PRE VELOS IN P",
   "copies_judge": [
    8,
    12,
    18,
    12,
    12,
    8,
    12,
    8,
    8,
    12,
    12,
    12
   ],
   "copies_best": 18,
   "k4_above_every_copy": false,
   "k4_rank": 13,
   "n_copies": 12,
   "none": 0,
   "k4_reading": "KDOWBOOFGOLPREATINCEREASTNORTHEASTYIRTIDONTTOSTENEETSBEIPHYAVAMBERLINCLOCKYWASTILINGLDPREVELOSINP"
  },
  {
   "cell": "0120 L23",
   "k4_judge": 12,
   "k4_judge_reading": "? TOME OR ? BY EASI? LET ? MUCH AS ? HAS AND ? LAND ? LUCK? ?",
   "copies_judge": [
    6,
    5,
    8,
    12,
    3,
    12,
    12,
    8,
    4,
    12,
    8,
    12
   ],
   "copies_best": 12,
   "k4_above_every_copy": false,
   "k4_rank": 6,
   "n_copies": 12,
   "none": 0,
   "k4_reading": "WRYZNNIPNMUPTOMEORJZEEASTNORTHEASTRBYEASILETFIPLSNGESMUCHASTDCEBERLINCLOCKHASANDWLANDWOHLUCEKSENP"
  },
  {
   "cell": "0120 L26",
   "k4_judge": 8,
   "k4_judge_reading": "? ? ? COOT ? HOUR ? ? BY IN A ? THE ? ?",
   "copies_judge": [
    8,
    8,
    12,
    22,
    6,
    6,
    12,
    8,
    8,
    8,
    8,
    8
   ],
   "copies_best": 22,
   "k4_above_every_copy": false,
   "k4_rank": 11,
   "n_copies": 12,
   "none": 0,
   "k4_reading": "QBHEFEULCLATLYEPHUVALEASTNORTHEASTPOILTYNESTUCOOTEVELHOURKMRTISBERLINCLOCKTBYINAROMTHEENEIGNORGHF"
  }
 ],
 "plants": [
  {
   "group": "0125 plants",
   "against": "the 50 copies",
   "plants_judge": [
    85,
    72,
    82,
    72,
    66,
    72,
    45,
    82,
    85,
    85,
    55,
    62,
    55,
    62,
    62,
    72,
    72,
    52,
    62,
    80
   ],
   "found": 20,
   "of": 20,
   "plant_detail": [
    true,
    true,
    true,
    true,
    true,
    true,
    true,
    true,
    true,
    true,
    true,
    true,
    true,
    true,
    true,
    true,
    true,
    true,
    true,
    true
   ],
   "none": 0
  },
  {
   "group": "0140 plants L26",
   "against": "their own 6 fitting shuffles each",
   "plants_judge": [
    14,
    8,
    12,
    12,
    8,
    14
   ],
   "found": 0,
   "of": 6,
   "plant_detail": [
    34,
    35,
    39,
    36,
    33,
    44
   ],
   "none": 0
  },
  {
   "group": "0120 plants L23",
   "against": "K4's 12 copies at 23",
   "plants_judge": [
    12,
    14,
    8,
    12,
    14,
    7
   ],
   "found": 2,
   "of": 6,
   "plant_detail": [
    37,
    41,
    34,
    34,
    32,
    36
   ],
   "none": 0
  },
  {
   "group": "0120 plants L26",
   "against": "K4's 12 copies at 26",
   "plants_judge": [
    12,
    14,
    12,
    8,
    12,
    8
   ],
   "found": 0,
   "of": 6,
   "plant_detail": [
    29,
    37,
    38,
    38,
    43,
    36
   ],
   "none": 0
  }
 ],
 "k4_above_every_copy_cells": [],
 "chance_expected": 0.56,
 "stop_queue_candidates": [],
 "copies": "each verdict's own, made by its frozen code and seeds (0120: seed 120; 0125: 125; 0140: 140; 0142: 142; 0144: 144; 0146: 146)",
 "controls": "gate 4: the quadgram scores of every copy reading regenerated here (0120, 0140, 0142, 0144, 0146) and 0140/0142's saved controls; the re-submitted K4 readings of 0120, 0140, 0142 face at least their own copies (issue #88)",
 "exhaustive": false
}
```

Notes: 0142 L26: K4 6, copies best 15 (rank 13 of 13); 0146 L8: K4 8, copies best 12 (rank 11 of 13); 0125 running key: K4 8, copies best 22 (rank 42 of 51); 0140 L23: K4 12, copies best 18 (rank 7 of 13); 0144 L13: K4 8, copies best 12 (rank 13 of 13); 0144 L16: K4 8, copies best 18 (rank 13 of 13); 0120 L23: K4 12, copies best 12 (rank 6 of 13); 0120 L26: K4 8, copies best 22 (rank 11 of 13). Plants: 0125 plants 20/20; 0140 plants L26 0/6; 0120 plants L23 2/6; 0120 plants L26 0/6


