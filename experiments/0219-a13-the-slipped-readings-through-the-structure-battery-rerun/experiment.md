# 0219-a13-the-slipped-readings-through-the-structure-battery-rerun: A13.4: every 24-of-24 reading of 0207, 0212, 0213 and 0214 (A1's slipped searches) regenerated with their frozen searches for K4 and the same 20 scrambled copies, through the 14-test structure battery, with masked plants through 0207's search

**Family:** 1-keyed-periodic  
**Parent:** 0218-a13-the-slipped-readings-through-the-structure-battery  
**Decision:** kept  
**Run:** 2026-10-25T13:38:18+00:00, 866.0 s, status ran  
**Time by phase:** unattributed 37 s, run 866 s, record 34 s

## In plain words

The searches that allowed for one or two enciphering mistakes produced readings with every known letter right but gibberish elsewhere. If the message was disguised before it was enciphered, the right one would look like gibberish too. We rerun those searches exactly, on the carving and on the same scrambled copies they used, and test every reading for 14 kinds of hidden pattern; the carving counts only if it beats all the copies. We also hide disguised messages with mistakes of our own and check the tests notice them.

## Walkthrough, by hand

1. Rerun one of the slip searches, say 0207, on the carving: every key length 1-26 and table, up to three known letters allowed wrong.
2. Keep every reading it lets through.
3. Score each reading on 14 pattern tests and keep the best value per test.
4. Do the same on the 20 scrambled copies 0207 used.
5. On each test, see whether the carving beats all 20 copies; about three of the 56 comparisons will by luck, so each that does is rerun against fresh copies until one catches up.

## Worked example (generated)

```
0207's saved reading (key length 25, std/std vig, slips at [22, 24, 73], 4 slots open (filled with A)):
  LZMTOMNOHHULBGUNYUVRIEASTNORTHEASTOTWTEYLGHMUWIOWYQHMNOBYAXINFBBERLINCLOCKUDBMBRRZCEIGKUVACKTESMA
battery (higher = more structure):
  eng_base        -6.616
  freq_sorted     -3.116
  ioc             0.041
  sep_words       none
  sep_regular     none
  eng_reverse     -7.173
  eng_keep_nth    -6.322
  eng_drop_nth    -6.359
  eng_step        -6.674
  eng_affine_std  -6.616
  eng_affine_kry  -6.616
  eng_columns     -6.790
  repeats         3.000
  base_pairs      -0.917
```

## Lineage

Inherits from 0218-a13-the-slipped-readings-through-the-structure-battery. What changed: A13.4 (Stage 2, step 3, issue #75). Since 2026-10-18 four experiments kept K4 readings with all 24 known letters in place: 0207 (periodic key on the sculpture's tables, up to 3 slips), 0212 (ciphertext autokey and progressive key, 2 slips or a lost step), 0213 (plaintext autokey, 2 broken links or a lost step) and 0214 (a move then the table, 2 slips). None kept its copies' readings. Here each frozen attack.py's own per-text search is called on K4 and on the same 20 seeded copies it used (tools/a13_check.py's pass 4), every reading it returns goes through the battery, and K4 is ranked per experiment and test. Pre-registered 2026-10-21 in reports/a13-structure-check.md: 56 cells, flag at p < 0.05/56, candidates replicated sequentially (seeds 4113 on). New in this run: masked planted messages with slips through 0207's search. Rerun of 0218, which errored in the plant step after the regeneration: 0216's frozen masked_plant, loaded from its experiment folder, looked for Carter's text there; its root is now set to the repository.

## Hypothesis (domain expert)

A13 with A1 (knowledge/12-assumptions.md): a masked plaintext (C4(a), Scheidt's 'I masked the English language'; C19, X and Q stops) enciphered with a slip or two (C17(b), Sanborn's 'sloppy'). The readings are those A1's exact searches let through: 0207 (8 table classes, key lengths 1-26, k <= 3), 0212 (ciphertext autokey on 487,734 table setups, k <= 2 or a lost step; progressive key, k <= 2), 0213 (plaintext autokey lags 1-52, 2 breaks or a lost step), 0214 (1,847,590 landings of 0110-0114 and the type-1 library, both orders, k <= 2). Statistic: per experiment and test, the best value over a text's readings ('?' read as unknown, the 24 known letters set as the candidates set them); K4's rank among its 20 copies, ties against K4. 0199, 0201-0206 and 0208-0211 kept no K4 reading (nothing fits K4, or a free alphabet leaves it undetermined): noted, not rerun.

## Prediction

K4 strictly above every copy in about 56/21 = 2.7 cells, none replicating; no flag. Every saved K4 candidate of the four experiments is among the regenerated readings. The masked plants through 0207 are found by their mask's own test in most cases, because 0207's readings at lengths 13 and 20 are fixed by the known letters and the planted reading itself is among them. Zero candidates pass gate 4.

## Method

1. For 0207, 0212, 0213, 0214: rebuild the frozen search's state as its run() does, call its per-text search on K4 and its 20 copies (its own shuffled, its own seeds), keep every reading.
2. Check every saved K4 candidate is among K4's regenerated readings.
3. Battery on every reading; per text and test the best value; rank K
4. 4. A cell where K4 is strictly above every copy is a candidate: fresh copies (the experiment's shuffled, seeds 4113 on) eight at a time until one is at or above K4 (not a flag), 1,123 all below (a flag), or the clock.
5. Plants: three per mask (none, reversal, X between words, X every kth letter), Carter 1923 masked then the known letters set, enciphered by 0207's own plant routine with 2 slips at lengths 13 and 20; found when the mask's own test on the plant's readings is strictly above every one of K4's 20 copies.

## Result

Candidates returned: 12. Passed all gates: 8. Best crib hits among all candidates: 24/24
(EAST 4/4, NORTHEAST 9/9, BERLIN 6/6, CLOCK 5/5).
Best loss: 5.411630150130789 (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: -12.088440679913024. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | baseline | 24/24 | -8.994 | `LZMTOMNOHHULBGUNYUVRIEASTNORTHEASTOTWTEYLGHMUWIOWYQHMNOBYAXINFBBERLINCLOCKUDBMBRRZCEIGKUVACKTESMA` | saved reading of 0207: key length 25, std/std vig, slips at [22, 24, 73], 4 slots open (filled with A) |
| 2 | baseline | 24/24 | -9.003 | `LZMTOMNOHHULBGUNYUVRIEASTNORTHEASTOTWTEYLGHMUWIMWYQHMNOBYAXINFBBERLINCLOCKUDBMBRRZCEIGKUVACKTESMA` | saved reading of 0207: key length 25, std/std vig, slips at [22, 23, 24], 4 slots open (filled with A) |
| 3 | baseline | 24/24 | -9.391 | `CAUTFMCTMMFJSOBDSAJMNEASTNORTHEASTVWDWAAENGLJKRSWIDSUDFHLRCLHOSBERLINCLOCKSUYUVCNKPPLNAFGLNMBRLDP` | saved reading of 0207: key length 25, std/kry beau, slips at [72, 73, 74], 4 slots open (filled with A) |
| 4 | pass | 24/24 | -21.504 | `AAAAAAAAAAAAAAAAAAAAAEASTNORTHEASTAAAAAAAAAAAAAAAAAAAAAAAAAAAAABERLINCLOCKHROPCPRIVOTNOUGOBBVCTOC` | saved reading of 0212: ciphertext autokey lag 69, LAYER/keyword|AND/keyword|std|varbeau, 2 slips at known places, skip None; free letters fille |
| 5 | pass | 24/24 | -21.292 | `AAAAAAAAAAAAAAAAAAAAAEASTNORTHEASTAAAAAAAAAAAAAAAAAAAAAAAAAAAAABERLINCLOCKHROPCPRIWOTNOUGOCBTCUPC` | saved reading of 0212: ciphertext autokey lag 69, LAYER/keyword|MADE/keyword|std|varbeau, 2 slips at known places, skip None; free letters fill |
| 6 | pass | 24/24 | -21.073 | `AAAAAAAAAAAAAAAAAAAAAEASTNORTHEASTAAAAAAAAAAAAAAAAAAAAAAAAAAAAABERLINCLOCKGJFRWMJVCTURRFLIEVETSAM` | saved reading of 0212: ciphertext autokey lag 71, BURIED/keyword|FIFTY/keyword|plain|varbeau, 0 slips at known places, skip (72, 72); free lett |
| 7 | pass | 24/24 | -15.122 | `IIDPVLMAAAAAAAAAAAAAAEASTNORTHEASTAFURGVTAAAAAAAAAAAAAECAITMOFDBERLINCLOCKAAAAAAAAAAAAAETAKTHIOXD` | saved reading of 0213: plaintext autokey lag 33, WORLDCLOCK/keyword|UNDERGROUND/keyword|plain|beau, chain, cuts [67], lost step None; unknown l |
| 8 | pass | 24/24 | -12.088 | `BTUMOPAHOMRAVJABAIAAAEASTNORTHEASTANISHDHADEEXAAADFEGOGAVGWBGCABERLINCLOCKAAARCAMLOIYRJUSVAUIETHE` | saved reading of 0213: plaintext autokey lag 28, WALL/keyword|PALIMPSEST/keyword|std|varbeau, bulk, cuts [], lost step None; unknown letters fi |
| 9 | pass | 24/24 | -12.186 | `MWVTALAKJOVRJERINTAAAEASTNORTHEASTATFCKHUVHISAAAAAUEAOFWECTHLDABERLINCLOCKAAAKSIUZFINHAGUYAWHEOFA` | saved reading of 0213: plaintext autokey lag 28, DIGETAL/keyword|WALL/keyword|std|varbeau, bulk, cuts [], lost step None; unknown letters fille |
| 10 | pass | 24/24 | -15.200 | `UDYWHEKOVYGWAKEKRAXHSEASTNORTHEASTEVHWOODNSOMAMALKEYKWHENPUXQKQBERLINCLOCKZOOZHTIKLPUBVIEQTUATMIQ` | saved reading of 0214: 0112 double columnar: TOSHNAIL inverse, order B, key length 24, kry/kry/beau, slips [74, 22]; open slots filled with A |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "item": "A13.4",
 "pre_registered": "2026-10-21, reports/a13-structure-check.md",
 "tests": [
  "eng_base",
  "freq_sorted",
  "ioc",
  "sep_words",
  "sep_regular",
  "eng_reverse",
  "eng_keep_nth",
  "eng_drop_nth",
  "eng_step",
  "eng_affine_std",
  "eng_affine_kry",
  "eng_columns",
  "repeats",
  "base_pairs"
 ],
 "experiments": [
  "0207",
  "0212",
  "0213",
  "0214"
 ],
 "cells": 56,
 "p_flag": 0.0008928571428571429,
 "kept_no_k4_reading": "0199, 0201-0206, 0208-0211 (no setting fits K4, or a free alphabet leaves the reading undetermined); 0200 errored",
 "readings_per_text": {
  "0207": {
   "k4": 80,
   "copies_min": 70,
   "copies_max": 91
  },
  "0212": {
   "k4": 404,
   "copies_min": 198,
   "copies_max": 1157
  },
  "0213": {
   "k4": 292,
   "copies_min": 258,
   "copies_max": 820
  },
  "0214": {
   "k4": 53150,
   "copies_min": 51861,
   "copies_max": 60284
  }
 },
 "saved_k4_candidates_regenerated": {
  "0207": "50 of 50",
  "0212": "10 of 10",
  "0213": "10 of 10",
  "0214": "10 of 10"
 },
 "text_seconds_mean": {
  "0207": 0.4,
  "0212": 36.6,
  "0213": 18.7,
  "0214": 170.3
 },
 "cells_table": {
  "0207/eng_base": {
   "k4": -6.488507779515539,
   "copies_min": -6.677348554610516,
   "copies_max": -5.99249409634102,
   "rank": 13,
   "candidate": false
  },
  "0207/freq_sorted": {
   "k4": -3.0045782126449545,
   "copies_min": -3.137311057284715,
   "copies_max": -2.849384872543406,
   "rank": 9,
   "candidate": false
  },
  "0207/ioc": {
   "k4": 0.04506172839506173,
   "copies_min": 0.04145658263305322,
   "copies_max": 0.062037037037037036,
   "rank": 17,
   "candidate": false
  },
  "0207/sep_words": {
   "k4": -2.245484192630397,
   "copies_min": -Infinity,
   "copies_max": -0.19057652375707335,
   "rank": 16,
   "candidate": false
  },
  "0207/sep_regular": {
   "k4": -Infinity,
   "copies_min": -Infinity,
   "copies_max": -0.3390552296506612,
   "rank": 21,
   "candidate": false
  },
  "0207/eng_reverse": {
   "k4": -7.004841355601902,
   "copies_min": -7.45799564339757,
   "copies_max": -6.791646117828795,
   "rank": 10,
   "candidate": false
  },
  "0207/eng_keep_nth": {
   "k4": -5.5199143903240255,
   "copies_min": -5.980602418753946,
   "copies_max": -5.135383687091392,
   "rank": 7,
   "candidate": false
  },
  "0207/eng_drop_nth": {
   "k4": -5.989922305913885,
   "copies_min": -6.397861147591042,
   "copies_max": -5.667435020552687,
   "rank": 9,
   "candidate": false
  },
  "0207/eng_step": {
   "k4": -6.144954953356035,
   "copies_min": -6.7153040169762885,
   "copies_max": -5.646266484192534,
   "rank": 3,
   "candidate": false
  },
  "0207/eng_affine_std": {
   "k4": -6.48850777951554,
   "copies_min": -6.6773485546105205,
   "copies_max": -5.99249409634102,
   "rank": 13,
   "candidate": false
  },
  "0207/eng_affine_kry": {
   "k4": -6.48850777951554,
   "copies_min": -6.668634978180151,
   "copies_max": -5.99249409634102,
   "rank": 13,
   "candidate": false
  },
  "0207/eng_columns": {
   "k4": -6.180897605392552,
   "copies_min": -6.640921659456301,
   "copies_max": -6.060019029938818,
   "rank": 3,
   "candidate": false
  },
  "0207/repeats": {
   "k4": 4.0,
   "copies_min": 2.0,
   "copies_max": 4.0,
   "rank": 7,
   "candidate": false
  },
  "0207/base_pairs": {
   "k4": -0.8947368421052632,
   "copies_min": -0.9473684210526315,
   "copies_max": -0.875,
   "rank": 8,
   "candidate": false
  },
  "0212/eng_base": {
   "k4": -5.391960153542632,
   "copies_min": -5.553834973480158,
   "copies_max": -5.018262135320959,
   "rank": 18,
   "candidate": false
  },
  "0212/freq_sorted": {
   "k4": -2.7848294648194987,
   "copies_min": -2.8153184485457783,
   "copies_max": -2.679700357500534,
   "rank": 18,
   "candidate": false
  },
  "0212/ioc": {
   "k4": 0.058279370952821465,
   "copies_min": 0.0545790934320074,
   "copies_max": 0.07030527289546716,
   "rank": 14,
   "candidate": false
  },
  "0212/sep_words": {
   "k4": -0.33144396074579346,
   "copies_min": -Infinity,
   "copies_max": 0.8480119210157239,
   "rank": 3,
   "candidate": false
  },
  "0212/sep_regular": {
   "k4": -0.2449489742783178,
   "copies_min": -Infinity,
   "copies_max": -0.31622776601683794,
   "rank": 1,
   "candidate": true
  },
  "0212/eng_reverse": {
   "k4": -6.461567461147484,
   "copies_min": -6.596547514193637,
   "copies_max": -5.920926717302767,
   "rank": 20,
   "candidate": false
  },
  "0212/eng_keep_nth": {
   "k4": -4.6112701539599845,
   "copies_min": -4.875681808530856,
   "copies_max": -4.076998701098784,
   "rank": 17,
   "candidate": false
  },
  "0212/eng_drop_nth": {
   "k4": -5.222965247450425,
   "copies_min": -5.245453186329582,
   "copies_max": -4.714833398406718,
   "rank": 20,
   "candidate": false
  },
  "0212/eng_step": {
   "k4": -3.916072851138032,
   "copies_min": -4.016615116342211,
   "copies_max": -3.0906982745166705,
   "rank": 17,
   "candidate": false
  },
  "0212/eng_affine_std": {
   "k4": -5.391960153542633,
   "copies_min": -5.55383497348016,
   "copies_max": -5.01826213532096,
   "rank": 18,
   "candidate": false
  },
  "0212/eng_affine_kry": {
   "k4": -5.391960153542633,
   "copies_min": -5.55383497348016,
   "copies_max": -5.01826213532096,
   "rank": 18,
   "candidate": false
  },
  "0212/eng_columns": {
   "k4": -3.916072851138032,
   "copies_min": -4.246529474266749,
   "copies_max": -3.3691665092401824,
   "rank": 17,
   "candidate": false
  },
  "0212/repeats": {
   "k4": 4.0,
   "copies_min": 3.0,
   "copies_max": 5.0,
   "rank": 10,
   "candidate": false
  },
  "0212/base_pairs": {
   "k4": -0.8636363636363636,
   "copies_min": -0.9090909090909091,
   "copies_max": -0.8260869565217391,
   "rank": 11,
   "candidate": false
  },
  "0213/eng_base": {
   "k4": -5.303759436756378,
   "copies_min": -5.196810204489397,
   "copies_max": -4.649955306112749,
   "rank": 21,
   "candidate": false
  },
  "0213/freq_sorted": {
   "k4": -2.771387188077234,
   "copies_min": -2.7905654488490677,
   "copies_max": -2.689232907043878,
   "rank": 18,
   "candidate": false
  },
  "0213/ioc": {
   "k4": 0.056910569105691054,
   "copies_min": 0.053544494720965306,
   "copies_max": 0.06685633001422475,
   "rank": 9,
   "candidate": false
  },
  "0213/sep_words": {
   "k4": -1.1535827875275109,
   "copies_min": -1.6705883989180406,
   "copies_max": 0.45170784451327667,
   "rank": 16,
   "candidate": false
  },
  "0213/sep_regular": {
   "k4": -0.6627307637727755,
   "copies_min": -0.6938106839455911,
   "copies_max": -0.2581117781084648,
   "rank": 20,
   "candidate": false
  },
  "0213/eng_reverse": {
   "k4": -6.3175595742314625,
   "copies_min": -6.462471024305855,
   "copies_max": -6.090795085449097,
   "rank": 14,
   "candidate": false
  },
  "0213/eng_keep_nth": {
   "k4": -4.648027526412451,
   "copies_min": -4.863830409476908,
   "copies_max": -3.8134593703083315,
   "rank": 18,
   "candidate": false
  },
  "0213/eng_drop_nth": {
   "k4": -5.022964454704404,
   "copies_min": -4.80087349452811,
   "copies_max": -4.272584026871793,
   "rank": 21,
   "candidate": false
  },
  "0213/eng_step": {
   "k4": -3.859825726487422,
   "copies_min": -4.471197453451937,
   "copies_max": -3.365839902716111,
   "rank": 14,
   "candidate": false
  },
  "0213/eng_affine_std": {
   "k4": -5.303759436756379,
   "copies_min": -5.196810204489399,
   "copies_max": -4.64995530611275,
   "rank": 21,
   "candidate": false
  },
  "0213/eng_affine_kry": {
   "k4": -5.303759436756379,
   "copies_min": -5.196810204489399,
   "copies_max": -4.64995530611275,
   "rank": 21,
   "candidate": false
  },
  "0213/eng_columns": {
   "k4": -4.072230262043481,
   "copies_min": -4.296174445142867,
   "copies_max": -2.8022123569350694,
   "rank": 19,
   "candidate": false
  },
  "0213/repeats": {
   "k4": 4.0,
   "copies_min": 3.0,
   "copies_max": 6.0,
   "rank": 17,
   "candidate": false
  },
  "0213/base_pairs": {
   "k4": -0.8421052631578947,
   "copies_min": -0.8947368421052632,
   "copies_max": -0.8333333333333334,
   "rank": 3,
   "candidate": false
  },
  "0214/eng_base": {
   "k4": -4.378393712209268,
   "copies_min": -4.432211371114223,
   "copies_max": -4.14429055188698,
   "rank": 18,
   "candidate": false
  },
  "0214/freq_sorted": {
   "k4": -2.8439087541636354,
   "copies_min": -2.8644986126896885,
   "copies_max": -2.7929573984527685,
   "rank": 13,
   "candidate": false
  },
  "0214/ioc": {
   "k4": 0.05878332194121668,
   "copies_min": 0.05639097744360902,
   "copies_max": 0.06596035543403965,
   "rank": 15,
   "candidate": false
  },
  "0214/sep_words": {
   "k4": 0.5474426742391912,
   "copies_min": 0.5436258429684764,
   "copies_max": 0.9099766349793299,
   "rank": 20,
   "candidate": false
  },
  "0214/sep_regular": {
   "k4": -0.17305741182250942,
   "copies_min": -0.16605388905002247,
   "copies_max": -0.0,
   "rank": 21,
   "candidate": false
  },
  "0214/eng_reverse": {
   "k4": -5.928487672074871,
   "copies_min": -6.083685868953683,
   "copies_max": -5.756467623430984,
   "rank": 11,
   "candidate": false
  },
  "0214/eng_keep_nth": {
   "k4": -3.7761235784685154,
   "copies_min": -3.7989268792224977,
   "copies_max": -2.9877864631589834,
   "rank": 20,
   "candidate": false
  },
  "0214/eng_drop_nth": {
   "k4": -4.084043842257405,
   "copies_min": -4.123268768591139,
   "copies_max": -3.8704414180921574,
   "rank": 18,
   "candidate": false
  },
  "0214/eng_step": {
   "k4": -5.005495904148879,
   "copies_min": -5.246507028242858,
   "copies_max": -4.380980130249045,
   "rank": 7,
   "candidate": false
  },
  "0214/eng_affine_std": {
   "k4": -4.378393712209268,
   "copies_min": -4.432211371114223,
   "copies_max": -4.14429055188698,
   "rank": 18,
   "candidate": false
  },
  "0214/eng_affine_kry": {
   "k4": -4.378393712209268,
   "copies_min": -4.432211371114223,
   "copies_max": -4.14429055188698,
   "rank": 18,
   "candidate": false
  },
  "0214/eng_columns": {
   "k4": -5.062507253854869,
   "copies_min": -5.320536921283422,
   "copies_max": -4.869904843608957,
   "rank": 10,
   "candidate": false
  },
  "0214/repeats": {
   "k4": 6.0,
   "copies_min": 5.0,
   "copies_max": 7.0,
   "rank": 15,
   "candidate": false
  },
  "0214/base_pairs": {
   "k4": -0.8333333333333334,
   "copies_min": -0.8333333333333334,
   "copies_max": -0.7941176470588235,
   "rank": 21,
   "candidate": false
  }
 },
 "candidates": [
  "0212/sep_regular"
 ],
 "candidates_expected_by_chance": 2.67,
 "replication": {
  "0212/sep_regular": {
   "k4": -0.2449489742783178,
   "fresh_copies": 27,
   "first_copy_at_or_above": 27,
   "fresh_max": -0.22110831935702666,
   "verdict": "not a flag",
   "p_bound": null
  }
 },
 "flags": [],
 "unresolved": [],
 "plants": [
  {
   "L": 13,
   "cls": [
    "kry",
    "kry",
    "vig"
   ],
   "mask": "none",
   "i": 0,
   "slips": [
    29,
    73
   ],
   "test": "eng_base",
   "value": -4.278058097702933,
   "copies_max": -5.99249409634102,
   "found": true,
   "planted_reading_among_readings": true,
   "n_readings": 79
  },
  {
   "L": 13,
   "cls": [
    "kry",
    "kry",
    "vig"
   ],
   "mask": "none",
   "i": 1,
   "slips": [
    26,
    34
   ],
   "test": "eng_base",
   "value": -4.176231053223467,
   "copies_max": -5.99249409634102,
   "found": true,
   "planted_reading_among_readings": true,
   "n_readings": 75
  },
  {
   "L": 13,
   "cls": [
    "kry",
    "kry",
    "vig"
   ],
   "mask": "none",
   "i": 2,
   "slips": [
    32,
    73
   ],
   "test": "eng_base",
   "value": -4.023005511416989,
   "copies_max": -5.99249409634102,
   "found": true,
   "planted_reading_among_readings": true,
   "n_readings": 79
  },
  {
   "L": 13,
   "cls": [
    "kry",
    "kry",
    "vig"
   ],
   "mask": "reversal",
   "i": 0,
   "slips": [
    31,
    67
   ],
   "test": "eng_reverse",
   "value": -5.133823739805622,
   "copies_max": -6.791646117828795,
   "found": true,
   "planted_reading_among_readings": true,
   "n_readings": 78
  },
  {
   "L": 13,
   "cls": [
    "kry",
    "kry",
    "vig"
   ],
   "mask": "reversal",
   "i": 1,
   "slips": [
    26,
    66
   ],
   "test": "eng_reverse",
   "value": -4.705072923337778,
   "copies_max": -6.791646117828795,
   "found": true,
   "planted_reading_among_readings": true,
   "n_readings": 83
  },
  {
   "L": 13,
   "cls": [
    "kry",
    "kry",
    "vig"
   ],
   "mask": "reversal",
   "i": 2,
   "slips": [
    22,
    32
   ],
   "test": "eng_reverse",
   "value": -4.8767659788877245,
   "copies_max": -6.791646117828795,
   "found": true,
   "planted_reading_among_readings": true,
   "n_readings": 84
  },
  {
   "L": 13,
   "cls": [
    "kry",
    "kry",
    "vig"
   ],
   "mask": "X spaces",
   "i": 0,
   "slips": [
    64,
    69
   ],
   "test": "sep_words",
   "value": 0.15911564798904998,
   "copies_max": -0.19057652375707335,
   "found": true,
   "planted_reading_among_readings": true,
   "n_readings": 78
  },
  {
   "L": 13,
   "cls": [
    "kry",
    "kry",
    "vig"
   ],
   "mask": "X spaces",
   "i": 1,
   "slips": [
    25,
    71
   ],
   "test": "sep_words",
   "value": 0.40112952046370565,
   "copies_max": -0.19057652375707335,
   "found": true,
   "planted_reading_among_readings": true,
   "n_readings": 79
  },
  {
   "L": 13,
   "cls": [
    "kry",
    "kry",
    "vig"
   ],
   "mask": "X spaces",
   "i": 2,
   "slips": [
    31,
    66
   ],
   "test": "sep_words",
   "value": -0.16294223390491397,
   "copies_max": -0.19057652375707335,
   "found": true,
   "planted_reading_among_readings": true,
   "n_readings": 78
  },
  {
   "L": 13,
   "cls": [
    "kry",
    "kry",
    "vig"
   ],
   "mask": "X every kth",
   "i": 0,
   "slips": [
    66,
    72
   ],
   "test": "sep_regular",
   "value": -0.5656854249492381,
   "copies_max": -0.3390552296506612,
   "found": false,
   "planted_reading_among_readings": true,
   "n_readings": 83
  },
  {
   "L": 13,
   "cls": [
    "kry",
    "kry",
    "vig"
   ],
   "mask": "X every kth",
   "i": 1,
   "slips": [
    26,
    74
   ],
   "test": "sep_regular",
   "value": -0.5443310539518172,
   "copies_max": -0.3390552296506612,
   "found": false,
   "planted_reading_among_readings": true,
   "n_readings": 84
  },
  {
   "L": 13,
   "cls": [
    "kry",
    "kry",
    "vig"
   ],
   "mask": "X every kth",
   "i": 2,
   "slips": [
    65,
    66
   ],
   "test": "sep_regular",
   "value": -0.5656854249492381,
   "copies_max": -0.3390552296506612,
   "found": false,
   "planted_reading_among_readings": true,
   "n_readings": 83
  },
  {
   "L": 20,
   "cls": [
    "std",
    "kry",
    "beau"
   ],
   "mask": "none",
   "i": 0,
   "slips": [
    24,
    66
   ],
   "test": "eng_base",
   "value": -4.2598701753099695,
   "copies_max": -5.99249409634102,
   "found": true,
   "planted_reading_among_readings": false,
   "n_readings": 80
  },
  {
   "L": 20,
   "cls": [
    "std",
    "kry",
    "beau"
   ],
   "mask": "none",
   "i": 1,
   "slips": [
    28,
    34
   ],
   "test": "eng_base",
   "value": -4.102561667962152,
   "copies_max": -5.99249409634102,
   "found": true,
   "planted_reading_among_readings": false,
   "n_readings": 75
  },
  {
   "L": 20,
   "cls": [
    "std",
    "kry",
    "beau"
   ],
   "mask": "none",
   "i": 2,
   "slips": [
    29,
    64
   ],
   "test": "eng_base",
   "value": -4.221914101020772,
   "copies_max": -5.99249409634102,
   "found": true,
   "planted_reading_among_readings": false,
   "n_readings": 84
  },
  {
   "L": 20,
   "cls": [
    "std",
    "kry",
    "beau"
   ],
   "mask": "reversal",
   "i": 0,
   "slips": [
    67,
    68
   ],
   "test": "eng_reverse",
   "value": -4.823968593125095,
   "copies_max": -6.791646117828795,
   "found": true,
   "planted_reading_among_readings": false,
   "n_readings": 83
  },
  {
   "L": 20,
   "cls": [
    "std",
    "kry",
    "beau"
   ],
   "mask": "reversal",
   "i": 1,
   "slips": [
    66,
    73
   ],
   "test": "eng_reverse",
   "value": -5.105174141828809,
   "copies_max": -6.791646117828795,
   "found": true,
   "planted_reading_among_readings": false,
   "n_readings": 88
  },
  {
   "L": 20,
   "cls": [
    "std",
    "kry",
    "beau"
   ],
   "mask": "reversal",
   "i": 2,
   "slips": [
    26,
    30
   ],
   "test": "eng_reverse",
   "value": -5.103300580765398,
   "copies_max": -6.791646117828795,
   "found": true,
   "planted_reading_among_readings": false,
   "n_readings": 91
  },
  {
   "L": 20,
   "cls": [
    "std",
    "kry",
    "beau"
   ],
   "mask": "X spaces",
   "i": 0,
   "slips": [
    32,
    67
   ],
   "test": "sep_words",
   "value": -1.079407504010587,
   "copies_max": -0.19057652375707335,
   "found": false,
   "planted_reading_among_readings": false,
   "n_readings": 75
  },
  {
   "L": 20,
   "cls": [
    "std",
    "kry",
    "beau"
   ],
   "mask": "X spaces",
   "i": 1,
   "slips": [
    64,
    74
   ],
   "test": "sep_words",
   "value": -0.08727431161031354,
   "copies_max": -0.19057652375707335,
   "found": true,
   "planted_reading_among_readings": false,
   "n_readings": 79
  },
  {
   "L": 20,
   "cls": [
    "std",
    "kry",
    "beau"
   ],
   "mask": "X spaces",
   "i": 2,
   "slips": [
    66,
    68
   ],
   "test": "sep_words",
   "value": -0.6191198322068695,
   "copies_max": -0.19057652375707335,
   "found": false,
   "planted_reading_among_readings": false,
   "n_readings": 92
  },
  {
   "L": 20,
   "cls": [
    "std",
    "kry",
    "beau"
   ],
   "mask": "X every kth",
   "i": 0,
   "slips": [
    30,
    74
   ],
   "test": "sep_regular",
   "value": -0.708043494570254,
   "copies_max": -0.3390552296506612,
   "found": false,
   "planted_reading_among_readings": false,
   "n_readings": 80
  },
  {
   "L": 20,
   "cls": [
    "std",
    "kry",
    "beau"
   ],
   "mask": "X every kth",
   "i": 1,
   "slips": [
    66,
    71
   ],
   "test": "sep_regular",
   "value": -Infinity,
   "copies_max": -0.3390552296506612,
   "found": false,
   "planted_reading_among_readings": false,
   "n_readings": 75
  },
  {
   "L": 20,
   "cls": [
    "std",
    "kry",
    "beau"
   ],
   "mask": "X every kth",
   "i": 2,
   "slips": [
    29,
    74
   ],
   "test": "sep_regular",
   "value": -0.4714045207910317,
   "copies_max": -0.3390552296506612,
   "found": false,
   "planted_reading_among_readings": false,
   "n_readings": 84
  }
 ],
 "plants_found": {
  "L13 none": "3 of 3",
  "L13 reversal": "3 of 3",
  "L13 X spaces": "3 of 3",
  "L13 X every kth": "0 of 3",
  "L20 none": "3 of 3",
  "L20 reversal": "3 of 3",
  "L20 X spaces": "1 of 3",
  "L20 X every kth": "0 of 3"
 },
 "plant_design": "3 per mask at each of [13, 20], 0207's plant routine (2 slips at checked slots), masked Carter with the known letters set; found = the mask's test strictly above all 20 of K4's copies",
 "controls": "0207's own controls (its copies' best quadgram scores)",
 "seconds": 863.2
}
```

Notes: 1 candidate cells of 56 (chance 2.7); replication: 1 not a flag, 0 unresolved, 0 flags. Saved K4 candidates regenerated: {'0207': '50 of 50', '0212': '10 of 10', '0213': '10 of 10', '0214': '10 of 10'}. Plants found: {'L13 none': '3 of 3', 'L13 reversal': '3 of 3', 'L13 X spaces': '3 of 3', 'L13 X every kth': '0 of 3', 'L20 none': '3 of 3', 'L20 reversal': '3 of 3', 'L20 X spaces': '1 of 3', 'L20 X every kth': '0 of 3'}.


