# 0216-a13-the-saved-readings-against-their-own-search-on-fresh-copies-rerun: A13.3: the 31 saved 24-of-24 readings of eight experiments put through the 14-test structure battery, against the same experiments' frozen searches run unchanged on fresh scrambled copies, with masked plants through two of the climbs

**Family:** 1-keyed-periodic  
**Parent:** 0140-k4-against-its-own-copies-with-the-tempering-climb  
**Decision:** reverted  
**Run:** 2026-10-24T16:53:13+00:00, 17774.5 s, status ran  
**Time by phase:** unattributed 353 s, run 17774 s, record 0 s

## In plain words

Some earlier searches produced readings with all 24 known letters right but the rest gibberish, and threw them away because they did not look like English. If Sanborn disguised the English before enciphering it (writing it backwards, or with X between words), the right reading would look like gibberish too. Here we test those saved readings for 14 kinds of hidden pattern, and run the very same searches on scrambled copies of the carving to see how much pattern luck alone produces. We also hide a few disguised messages of our own, run the same searches on them, and check whether the pattern tests would have noticed.

## Walkthrough, by hand

1. Take one saved reading, say 0142's, with all 24 known letters in place.
2. Score it on each of 14 pattern tests: read backwards, every nth letter, X as a word space, letter counts in any order, and so on.
3. Scramble the carved letters twelve times, keeping only scrambles the same search can fit, and run the same search on each.
4. Score each scramble's reading on the same 14 tests.
5. On each test, see whether the carving's reading beats all twelve scrambles; with 112 such comparisons about nine will by luck, so each one that does is rerun against fresh scrambles until one catches up.

## Worked example (generated)

```
0034's saved reading: RPRESIDENTHESTHERESANEASTNORTHEASTDERSTHEPRESINTHEREARENTHERETHBERLINCLOCKERESIDEDINGTHETHEREARTI
backwards:          ITRAEREHTEHTGNIDEDISEREKCOLCNILREBHTEREHTNERAEREHTNISERPEHTSREDTSAEHTRONTSAENASEREHTSEHTNEDISERPR
battery (higher = more structure):
  eng_base        -3.642
  freq_sorted     -2.575
  ioc             0.106
  sep_words       none
  sep_regular     none
  eng_reverse     -5.775
  eng_keep_nth    -5.209
  eng_drop_nth    -3.707
  eng_step        -5.285
  eng_affine_std  -3.642
  eng_affine_kry  -3.642
  eng_columns     -5.325
  repeats         31.000
  base_pairs      -0.604
```

## Lineage

Inherits from 0140-k4-against-its-own-copies-with-the-tempering-climb. What changed: A13.3 (Stage 2, step 3, issue #75). The 31 readings that put all 24 known letters in place and were saved in raw.json (0034: 18, 0035: 3, 0048: 3, 0120: 2, 0137: 2, 0140, 0142, 0148: 1 each) were thrown away on their quadgram score. Here they go through tools/a13_structure.py's 14 tests, each against the same experiment's frozen attack.py run unchanged on fresh copies built as that experiment built them (tools/a13_check.py pass1-regen, seed 1300, begun 2026-10-21 and finished 2026-10-24 before this run). Pre-registered 2026-10-21 in reports/a13-structure-check.md: 112 cells, flag at p < 0.05/112, candidates replicated sequentially on fresh copies (seed 3113). New in this run: masked planted messages through 0140's and 0142's climbs, to say what a 'nothing found' means for climbed readings. Rerun of 0215, which errored: the copy tool gave 0148's climb all 24 known letters where 0148 drops the one at place 33, so its copies had no reading; the tool is fixed and 0148's 12 copies regenerated.

## Hypothesis (domain expert)

A13 (knowledge/12-assumptions.md): if the English was masked before the keyed stage (C4(a), Scheidt 2005 and 2015: 'I masked the English language', 'more than one stage'; C19, X and Q as stops), the right decryption is masked English and its quadgram score sits with the copies'. The readings tested are the climbed completions of F1's sampled cells: 0034 (periodic key 27-29 and 53-95 on standard/KRYPTOS tables, 24 conventions), 0035 and 0048 (27-29, keyword-mixed tables), 0120, 0137, 0140, 0142 (one free alphabet, Beaufort form, 23 and 26) and 0148 (K1/K2's added form, length 19, slip at 33). Statistic: for each experiment and test, the best value over a text's readings; K4's rank among the copies' (ties against K4). Copies: plain shuffles (0034, 0035, 0048; 10 each), shuffles passing 0119's exact decider at the length (0120, 0137, 0140, 0142; 12 each), shuffles of the 73 unknown places (0148; 12). A cell is a candidate when K4 is strictly above every copy (chance about 112/12 = 9); a flag needs p < 0.00045, all of 2,242 copies below K4. Power: A13.1 (power.json) against flat noise; against climbed copies it is unmeasured, so masked plants (reversal, X between words, X every kth letter, and unmasked) are enciphered under 0140's and 0142's own method and climbed by their frozen search.

## Prediction

K4 is strictly above every copy in about 9 of 112 cells (chance), and none of those replicates: every candidate meets a fresh copy at or above K4 within a few dozen copies. No flag. The masked plants through the climbs are found less often than A13.1's flat-noise rate: the climb pulls a reversed or X-spaced message toward forward English junk, so most masked plants are not found by their own test. Zero candidates pass gate 4.

## Method

1. K4: every saved reading with 24 of 24 known letters in the eight experiments' raw.json, through the battery; per experiment and test, the best value.
2. Copies: the readings in reports/a13-structure-data/pass1_copies.json (any job still missing is run here, same seeds), through the battery the same way.
3. Rank K4 per cell; a cell where K4 is strictly above every copy is a candidate.
4. Replication, per experiment with candidates: fresh copies built the experiment's way (seed '3113'), its frozen search, eight at a time, until every candidate test has met a copy at or above K4 (not a flag), or 2,242 copies all below (a flag), or the clock (unresolved, reported with its p).
5. Plants: three per mask (none, reversal, X between words, X every kth letter), Carter 1923 with the 24 known letters set after masking, enciphered with a random alphabet and key under 0142's (length 26) and 0140's (length 23) Beaufort form, climbed by their frozen search; found when the mask's own test is above every one of that experiment's 12 copies.

## Result

Candidates returned: 16. Passed all gates: 0. Best crib hits among all candidates: 24/24
(EAST 4/4, NORTHEAST 9/9, BERLIN 6/6, CLOCK 5/5).
Best loss: 4.042044935477605 (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | baseline | 24/24 | -8.030 | `RPRESIDENTHESTHERESANEASTNORTHEASTDERSTHEPRESINTHEREARENTHERETHBERLINCLOCKERESIDEDINGTHETHEREARTI` | saved reading of 0034: period 95 key FALPWPOZKOFGDGYGYMDMJMCLWNQHMHLKFGXKQHZRHUEXABHQDWGHKKCPTKAYEAZBYHITCDFYZDATQMCOKGZPLSACOFWVNKB (71 free s |
| 2 | baseline | 24/24 | -7.941 | `OFORESTINTEDINTHEARENEASTNORTHEASTTHESTHESTHERENTERSANDINGANDINBERLINCLOCKGSTANDTHERENTERSARETHAL` | saved reading of 0034: period 92 key KVUKDZQJQDDANGRPTOAWTRDUMRIYWOYNKYRJFXJMOHYMKZHSNVPDNXEUVQJVCWIELYOIECBAQKDASNSHKYXCTQVDGIKQ (68 free slot |
| 3 | baseline | 24/24 | -7.855 | `ISCOREATTHETHESTHEREAEASTNORTHEASTNDCONTHERESERINTHESTERANDERANBERLINCLOCKDRENTHEREARATERSTHEMARX` | saved reading of 0034: period 89 key NACPMJYYGVZKPKXKWQZMXQRTPHIUUARAYZSHZSHZXYXKDEQHKALUSKZBPUATKMVUGUHMRUKAFKAEONSFIHNKGNTZF (65 free slots c |
| 4 | baseline | 24/24 | -8.280 | `QGFMJOYSTOAEUHISNORDFEASTNORTHEASTSDKZSIZKIENYYISBUIIAWIVYLBOMOBERLINCLOCKFFEMXURMHAWYLVEERAJBUXH` | saved reading of 0035: period 27, plain std, cipher HILL/keyword, vig; 3 free slots climbed |
| 5 | baseline | 24/24 | -8.121 | `DWIVEFUEXNARRMGFNUECOEASTNORTHEASTMWSESLIBREUKSFOCUJPVHUNIJEFUNBERLINCLOCKCEDWJICYBUNUIPOBOZZHUQP` | saved reading of 0035: period 28, plain WILLIAMWEBSTER/keyword, cipher std, beau; 4 free slots climbed |
| 6 | baseline | 24/24 | -8.169 | `FFATRYYSOWADXNDJBUTHEEASTNORTHEASTYFINMGHFNESEAVOLPGLEXNZIANXBIBERLINCLOCKRTRAAJSAKOWAAGGQIRORYUK` | saved reading of 0035: period 29, plain LANGLEY/keyword, cipher std, beau; 5 free slots climbed |
| 7 | baseline | 24/24 | -7.875 | `UYUGNUWILATPSJGPEOMIFEASTNORTHEASTIAORTOOPSUPOUGHBHISCEBKRIFCSOBERLINCLOCKFWRZEIMDEXZEMBERHTJRETQ` | saved reading of 0048: period 27, plain WEBSTER/keyword, cipher WORLDCLOCK/keyword, beau; 3 free slots climbed |
| 8 | baseline | 24/24 | -8.088 | `ADJBNPTHULKBRUNTDELITEASTNORTHEASTYWBCIGZFRYRKWATWCULYBOLARSASWBERLINCLOCKALSKHOOJUOLBJCEGOTKPAKO` | saved reading of 0048: period 28, plain SHADOW/keyword, cipher LODESTONE/keyword, varbeau; 4 free slots climbed |
| 9 | baseline | 24/24 | -7.756 | `JGAFEEFGHJCJOUSTOLITIEASTNORTHEASTEHHUAODBULYMENDTRYFFLAWPKASEDBERLINCLOCKITHNDPRGADTYGABNDEDOZMS` | saved reading of 0048: period 29, plain LUCID/keyword, cipher WONDERFUL/keyword, beau; 5 free slots climbed |
| 10 | baseline | 24/24 | -7.925 | `WRYZNNIPNMUPTOMEORJZEEASTNORTHEASTRBYEASILETFIPLSNGESMUCHASTDCEBERLINCLOCKHASANDWLANDWOHLUCEKSENP` | saved reading of 0120: Beaufort form, one alphabet JCRBOQYZPXVWHSMGAUKNFTIELD on both sides, key length 23 |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "item": "A13.3",
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
  "0034",
  "0035",
  "0048",
  "0120",
  "0137",
  "0140",
  "0142",
  "0148"
 ],
 "cells": 112,
 "p_flag": 0.00044642857142857147,
 "k4_readings": {
  "0034": 18,
  "0035": 3,
  "0048": 3,
  "0120": 2,
  "0137": 2,
  "0140": 1,
  "0142": 1,
  "0148": 1
 },
 "k4_reencrypt_ok": {
  "0034": true,
  "0035": true,
  "0048": true,
  "0120": true,
  "0137": true,
  "0140": true,
  "0142": true,
  "0148": true
 },
 "copies": {
  "0034": 10,
  "0035": 10,
  "0048": 10,
  "0120": 12,
  "0137": 12,
  "0140": 12,
  "0142": 12,
  "0148": 12
 },
 "copy_cpu_seconds_mean": {
  "0034": 3789.3,
  "0035": 141.9,
  "0048": 1449.4,
  "0120": 338.3,
  "0137": 213.5,
  "0140": 143.1,
  "0142": 67.3,
  "0148": 148.1
 },
 "copies_regenerated": "tools/a13_check.py pass1-regen, seed 1300: 22 jobs on 2026-10-21, the other 68 on 2026-10-24 before this run",
 "jobs_missing_at_start": 0,
 "cells_table": {
  "0034/eng_base": {
   "k4": -3.642290426988611,
   "copies_min": -3.6046326748374944,
   "copies_max": -3.5329024185250635,
   "n": 10,
   "rank": 11,
   "candidate": false
  },
  "0034/freq_sorted": {
   "k4": -2.575368554012606,
   "copies_min": -2.621632540922238,
   "copies_max": -2.555635860418908,
   "n": 10,
   "rank": 2,
   "candidate": false
  },
  "0034/ioc": {
   "k4": 0.10631443298969072,
   "copies_min": 0.0936426116838488,
   "copies_max": 0.11404639175257732,
   "n": 10,
   "rank": 3,
   "candidate": false
  },
  "0034/sep_words": {
   "k4": -Infinity,
   "copies_min": -Infinity,
   "copies_max": -2.051969008582769,
   "n": 10,
   "rank": 11,
   "candidate": false
  },
  "0034/sep_regular": {
   "k4": -Infinity,
   "copies_min": -Infinity,
   "copies_max": -Infinity,
   "n": 10,
   "rank": 11,
   "candidate": false
  },
  "0034/eng_reverse": {
   "k4": -5.4582804472186215,
   "copies_min": -5.71720599576929,
   "copies_max": -5.552742879798134,
   "n": 10,
   "rank": 1,
   "candidate": true
  },
  "0034/eng_keep_nth": {
   "k4": -4.751907523560674,
   "copies_min": -5.181900310263038,
   "copies_max": -4.875489415912129,
   "n": 10,
   "rank": 1,
   "candidate": true
  },
  "0034/eng_drop_nth": {
   "k4": -3.7071057487699983,
   "copies_min": -3.6976052935926806,
   "copies_max": -3.6131388750090556,
   "n": 10,
   "rank": 11,
   "candidate": false
  },
  "0034/eng_step": {
   "k4": -5.196587592066844,
   "copies_min": -5.29159231036549,
   "copies_max": -5.011680129342879,
   "n": 10,
   "rank": 7,
   "candidate": false
  },
  "0034/eng_affine_std": {
   "k4": -3.6422904269886125,
   "copies_min": -3.604632674837496,
   "copies_max": -3.5329024185250644,
   "n": 10,
   "rank": 11,
   "candidate": false
  },
  "0034/eng_affine_kry": {
   "k4": -3.6422904269886125,
   "copies_min": -3.604632674837496,
   "copies_max": -3.5329024185250644,
   "n": 10,
   "rank": 11,
   "candidate": false
  },
  "0034/eng_columns": {
   "k4": -5.260393159199314,
   "copies_min": -5.31129290466676,
   "copies_max": -5.145974464551342,
   "n": 10,
   "rank": 6,
   "candidate": false
  },
  "0034/repeats": {
   "k4": 31.0,
   "copies_min": 25.0,
   "copies_max": 38.0,
   "n": 10,
   "rank": 5,
   "candidate": false
  },
  "0034/base_pairs": {
   "k4": -0.5833333333333334,
   "copies_min": -0.625,
   "copies_max": -0.5625,
   "n": 10,
   "rank": 6,
   "candidate": false
  },
  "0035/eng_base": {
   "k4": -6.096714692753467,
   "copies_min": -6.084134767339252,
   "copies_max": -5.668075960605389,
   "n": 10,
   "rank": 11,
   "candidate": false
  },
  "0035/freq_sorted": {
   "k4": -3.12612761615087,
   "copies_min": -3.059051675762564,
   "copies_max": -2.927451153621812,
   "n": 10,
   "rank": 11,
   "candidate": false
  },
  "0035/ioc": {
   "k4": 0.04488831615120275,
   "copies_min": 0.04553264604810996,
   "copies_max": 0.05605670103092784,
   "n": 10,
   "rank": 11,
   "candidate": false
  },
  "0035/sep_words": {
   "k4": -Infinity,
   "copies_min": -Infinity,
   "copies_max": -Infinity,
   "n": 10,
   "rank": 11,
   "candidate": false
  },
  "0035/sep_regular": {
   "k4": -Infinity,
   "copies_min": -Infinity,
   "copies_max": -Infinity,
   "n": 10,
   "rank": 11,
   "candidate": false
  },
  "0035/eng_reverse": {
   "k4": -6.89510768979299,
   "copies_min": -6.987466721589629,
   "copies_max": -6.44013585787408,
   "n": 10,
   "rank": 9,
   "candidate": false
  },
  "0035/eng_keep_nth": {
   "k4": -6.043539183143253,
   "copies_min": -6.269042420044986,
   "copies_max": -5.275433642329155,
   "n": 10,
   "rank": 7,
   "candidate": false
  },
  "0035/eng_drop_nth": {
   "k4": -5.768787682263362,
   "copies_min": -5.866000613616906,
   "copies_max": -5.386926074211838,
   "n": 10,
   "rank": 5,
   "candidate": false
  },
  "0035/eng_step": {
   "k4": -6.490615509790811,
   "copies_min": -6.58851485561862,
   "copies_max": -6.139916621200839,
   "n": 10,
   "rank": 8,
   "candidate": false
  },
  "0035/eng_affine_std": {
   "k4": -6.096714692753467,
   "copies_min": -6.084134767339252,
   "copies_max": -5.668075960605389,
   "n": 10,
   "rank": 11,
   "candidate": false
  },
  "0035/eng_affine_kry": {
   "k4": -6.096714692753467,
   "copies_min": -6.084134767339252,
   "copies_max": -5.668075960605389,
   "n": 10,
   "rank": 11,
   "candidate": false
  },
  "0035/eng_columns": {
   "k4": -6.532556437072188,
   "copies_min": -6.558516930058649,
   "copies_max": -6.060268048994418,
   "n": 10,
   "rank": 10,
   "candidate": false
  },
  "0035/repeats": {
   "k4": 4.0,
   "copies_min": 3.0,
   "copies_max": 5.0,
   "n": 10,
   "rank": 6,
   "candidate": false
  },
  "0035/base_pairs": {
   "k4": -0.9166666666666666,
   "copies_min": -0.9375,
   "copies_max": -0.8541666666666666,
   "n": 10,
   "rank": 7,
   "candidate": false
  },
  "0048/eng_base": {
   "k4": -5.686172135893684,
   "copies_min": -5.903913260124872,
   "copies_max": -5.544667717272858,
   "n": 10,
   "rank": 5,
   "candidate": false
  },
  "0048/freq_sorted": {
   "k4": -2.9922051216651964,
   "copies_min": -3.004280581659727,
   "copies_max": -2.940153506477771,
   "n": 10,
   "rank": 10,
   "candidate": false
  },
  "0048/ioc": {
   "k4": 0.04725085910652921,
   "copies_min": 0.048539518900343644,
   "copies_max": 0.058848797250859106,
   "n": 10,
   "rank": 11,
   "candidate": false
  },
  "0048/sep_words": {
   "k4": -Infinity,
   "copies_min": -Infinity,
   "copies_max": -Infinity,
   "n": 10,
   "rank": 11,
   "candidate": false
  },
  "0048/sep_regular": {
   "k4": -Infinity,
   "copies_min": -Infinity,
   "copies_max": -Infinity,
   "n": 10,
   "rank": 11,
   "candidate": false
  },
  "0048/eng_reverse": {
   "k4": -6.767279035354215,
   "copies_min": -6.771054238071913,
   "copies_max": -6.280503735100856,
   "n": 10,
   "rank": 10,
   "candidate": false
  },
  "0048/eng_keep_nth": {
   "k4": -6.078103379218427,
   "copies_min": -6.225233784241704,
   "copies_max": -5.460013558108831,
   "n": 10,
   "rank": 9,
   "candidate": false
  },
  "0048/eng_drop_nth": {
   "k4": -5.5840848204313716,
   "copies_min": -5.571743685745264,
   "copies_max": -5.294111630625189,
   "n": 10,
   "rank": 11,
   "candidate": false
  },
  "0048/eng_step": {
   "k4": -6.327964939457987,
   "copies_min": -6.5201173955883265,
   "copies_max": -6.0878850736965715,
   "n": 10,
   "rank": 9,
   "candidate": false
  },
  "0048/eng_affine_std": {
   "k4": -5.686172135893685,
   "copies_min": -5.903913260124875,
   "copies_max": -5.544667717272857,
   "n": 10,
   "rank": 5,
   "candidate": false
  },
  "0048/eng_affine_kry": {
   "k4": -5.686172135893685,
   "copies_min": -5.903913260124875,
   "copies_max": -5.544667717272857,
   "n": 10,
   "rank": 5,
   "candidate": false
  },
  "0048/eng_columns": {
   "k4": -6.356665943140553,
   "copies_min": -6.534067907096268,
   "copies_max": -6.101911491484472,
   "n": 10,
   "rank": 10,
   "candidate": false
  },
  "0048/repeats": {
   "k4": 4.0,
   "copies_min": 2.0,
   "copies_max": 5.0,
   "n": 10,
   "rank": 4,
   "candidate": false
  },
  "0048/base_pairs": {
   "k4": -0.8958333333333334,
   "copies_min": -0.9375,
   "copies_max": -0.8541666666666666,
   "n": 10,
   "rank": 8,
   "candidate": false
  },
  "0120/eng_base": {
   "k4": -5.063530921083712,
   "copies_min": -5.186167966670841,
   "copies_max": -4.8111462983033855,
   "n": 12,
   "rank": 9,
   "candidate": false
  },
  "0120/freq_sorted": {
   "k4": -2.8841335454670163,
   "copies_min": -2.937878113382758,
   "copies_max": -2.7601191880332574,
   "n": 12,
   "rank": 11,
   "candidate": false
  },
  "0120/ioc": {
   "k4": 0.05627147766323024,
   "copies_min": 0.05369415807560137,
   "copies_max": 0.06829896907216494,
   "n": 12,
   "rank": 11,
   "candidate": false
  },
  "0120/sep_words": {
   "k4": -Infinity,
   "copies_min": -Infinity,
   "copies_max": -Infinity,
   "n": 12,
   "rank": 13,
   "candidate": false
  },
  "0120/sep_regular": {
   "k4": -Infinity,
   "copies_min": -Infinity,
   "copies_max": -Infinity,
   "n": 12,
   "rank": 13,
   "candidate": false
  },
  "0120/eng_reverse": {
   "k4": -6.224044156149807,
   "copies_min": -6.297542003499332,
   "copies_max": -5.909286741073485,
   "n": 12,
   "rank": 10,
   "candidate": false
  },
  "0120/eng_keep_nth": {
   "k4": -5.697830018785895,
   "copies_min": -6.050501596953651,
   "copies_max": -5.26174903194554,
   "n": 12,
   "rank": 5,
   "candidate": false
  },
  "0120/eng_drop_nth": {
   "k4": -5.007079858726159,
   "copies_min": -5.103989195076372,
   "copies_max": -4.706534013158261,
   "n": 12,
   "rank": 12,
   "candidate": false
  },
  "0120/eng_step": {
   "k4": -6.008035443238698,
   "copies_min": -5.969738418047347,
   "copies_max": -5.496427260321056,
   "n": 12,
   "rank": 13,
   "candidate": false
  },
  "0120/eng_affine_std": {
   "k4": -5.0635309210837125,
   "copies_min": -5.186167966670841,
   "copies_max": -4.8111462983033855,
   "n": 12,
   "rank": 9,
   "candidate": false
  },
  "0120/eng_affine_kry": {
   "k4": -5.0635309210837125,
   "copies_min": -5.186167966670841,
   "copies_max": -4.8111462983033855,
   "n": 12,
   "rank": 9,
   "candidate": false
  },
  "0120/eng_columns": {
   "k4": -5.982086521589703,
   "copies_min": -6.055884107014221,
   "copies_max": -5.638706319678302,
   "n": 12,
   "rank": 11,
   "candidate": false
  },
  "0120/repeats": {
   "k4": 7.0,
   "copies_min": 3.0,
   "copies_max": 7.0,
   "n": 12,
   "rank": 2,
   "candidate": false
  },
  "0120/base_pairs": {
   "k4": -0.9166666666666666,
   "copies_min": -0.9166666666666666,
   "copies_max": -0.8125,
   "n": 12,
   "rank": 13,
   "candidate": false
  },
  "0137/eng_base": {
   "k4": -4.953803474091055,
   "copies_min": -4.965532614832664,
   "copies_max": -4.693463744379584,
   "n": 12,
   "rank": 12,
   "candidate": false
  },
  "0137/freq_sorted": {
   "k4": -2.9338861339038615,
   "copies_min": -2.8968153952702376,
   "copies_max": -2.7897300453644043,
   "n": 12,
   "rank": 13,
   "candidate": false
  },
  "0137/ioc": {
   "k4": 0.05648625429553265,
   "copies_min": 0.05584192439862543,
   "copies_max": 0.06722508591065292,
   "n": 12,
   "rank": 12,
   "candidate": false
  },
  "0137/sep_words": {
   "k4": -Infinity,
   "copies_min": -Infinity,
   "copies_max": -Infinity,
   "n": 12,
   "rank": 13,
   "candidate": false
  },
  "0137/sep_regular": {
   "k4": -Infinity,
   "copies_min": -Infinity,
   "copies_max": -Infinity,
   "n": 12,
   "rank": 13,
   "candidate": false
  },
  "0137/eng_reverse": {
   "k4": -6.140388140765204,
   "copies_min": -6.4037616171640845,
   "copies_max": -5.527536230756367,
   "n": 12,
   "rank": 10,
   "candidate": false
  },
  "0137/eng_keep_nth": {
   "k4": -6.065479517549549,
   "copies_min": -5.947745169832811,
   "copies_max": -5.262752397158751,
   "n": 12,
   "rank": 13,
   "candidate": false
  },
  "0137/eng_drop_nth": {
   "k4": -4.754837014137857,
   "copies_min": -4.92783112043008,
   "copies_max": -4.599437818086509,
   "n": 12,
   "rank": 6,
   "candidate": false
  },
  "0137/eng_step": {
   "k4": -5.878701584192223,
   "copies_min": -6.0019273311366765,
   "copies_max": -5.486764859344598,
   "n": 12,
   "rank": 10,
   "candidate": false
  },
  "0137/eng_affine_std": {
   "k4": -4.953803474091054,
   "copies_min": -4.965532614832664,
   "copies_max": -4.693463744379584,
   "n": 12,
   "rank": 12,
   "candidate": false
  },
  "0137/eng_affine_kry": {
   "k4": -4.953803474091054,
   "copies_min": -4.965532614832664,
   "copies_max": -4.693463744379584,
   "n": 12,
   "rank": 12,
   "candidate": false
  },
  "0137/eng_columns": {
   "k4": -5.989825508587057,
   "copies_min": -5.941803008020516,
   "copies_max": -5.699966067272687,
   "n": 12,
   "rank": 13,
   "candidate": false
  },
  "0137/repeats": {
   "k4": 7.0,
   "copies_min": 2.0,
   "copies_max": 7.0,
   "n": 12,
   "rank": 3,
   "candidate": false
  },
  "0137/base_pairs": {
   "k4": -0.8958333333333334,
   "copies_min": -0.8958333333333334,
   "copies_max": -0.8125,
   "n": 12,
   "rank": 13,
   "candidate": false
  },
  "0140/eng_base": {
   "k4": -4.989091638582698,
   "copies_min": -5.084186735876598,
   "copies_max": -4.880476311445674,
   "n": 12,
   "rank": 8,
   "candidate": false
  },
  "0140/freq_sorted": {
   "k4": -2.867758898863594,
   "copies_min": -2.9546482602799347,
   "copies_max": -2.765599373847152,
   "n": 12,
   "rank": 9,
   "candidate": false
  },
  "0140/ioc": {
   "k4": 0.05777491408934708,
   "copies_min": 0.05219072164948454,
   "copies_max": 0.070446735395189,
   "n": 12,
   "rank": 9,
   "candidate": false
  },
  "0140/sep_words": {
   "k4": -Infinity,
   "copies_min": -Infinity,
   "copies_max": -Infinity,
   "n": 12,
   "rank": 13,
   "candidate": false
  },
  "0140/sep_regular": {
   "k4": -Infinity,
   "copies_min": -Infinity,
   "copies_max": -Infinity,
   "n": 12,
   "rank": 13,
   "candidate": false
  },
  "0140/eng_reverse": {
   "k4": -6.000261074982041,
   "copies_min": -6.335639891969496,
   "copies_max": -5.919036530737811,
   "n": 12,
   "rank": 2,
   "candidate": false
  },
  "0140/eng_keep_nth": {
   "k4": -5.398356703923783,
   "copies_min": -5.948643349667668,
   "copies_max": -5.268311890732577,
   "n": 12,
   "rank": 3,
   "candidate": false
  },
  "0140/eng_drop_nth": {
   "k4": -4.92721044177315,
   "copies_min": -5.07230599029337,
   "copies_max": -4.781234693516137,
   "n": 12,
   "rank": 7,
   "candidate": false
  },
  "0140/eng_step": {
   "k4": -5.825225296853422,
   "copies_min": -6.089267839690203,
   "copies_max": -5.713690552204805,
   "n": 12,
   "rank": 4,
   "candidate": false
  },
  "0140/eng_affine_std": {
   "k4": -4.989091638582699,
   "copies_min": -5.084186735876596,
   "copies_max": -4.880476311445675,
   "n": 12,
   "rank": 8,
   "candidate": false
  },
  "0140/eng_affine_kry": {
   "k4": -4.989091638582699,
   "copies_min": -5.084186735876596,
   "copies_max": -4.880476311445675,
   "n": 12,
   "rank": 8,
   "candidate": false
  },
  "0140/eng_columns": {
   "k4": -6.022112999110879,
   "copies_min": -6.05022266373015,
   "copies_max": -5.76873415230933,
   "n": 12,
   "rank": 12,
   "candidate": false
  },
  "0140/repeats": {
   "k4": 3.0,
   "copies_min": 2.0,
   "copies_max": 7.0,
   "n": 12,
   "rank": 11,
   "candidate": false
  },
  "0140/base_pairs": {
   "k4": -0.875,
   "copies_min": -0.9166666666666666,
   "copies_max": -0.7708333333333334,
   "n": 12,
   "rank": 10,
   "candidate": false
  },
  "0142/eng_base": {
   "k4": -4.990328321801061,
   "copies_min": -5.044662612703084,
   "copies_max": -4.722151738926735,
   "n": 12,
   "rank": 11,
   "candidate": false
  },
  "0142/freq_sorted": {
   "k4": -2.842899890242736,
   "copies_min": -2.9419520128650984,
   "copies_max": -2.813188386501495,
   "n": 12,
   "rank": 6,
   "candidate": false
  },
  "0142/ioc": {
   "k4": 0.059922680412371136,
   "copies_min": 0.05283505154639175,
   "copies_max": 0.06464776632302406,
   "n": 12,
   "rank": 7,
   "candidate": false
  },
  "0142/sep_words": {
   "k4": -Infinity,
   "copies_min": -Infinity,
   "copies_max": -Infinity,
   "n": 12,
   "rank": 13,
   "candidate": false
  },
  "0142/sep_regular": {
   "k4": -Infinity,
   "copies_min": -Infinity,
   "copies_max": -Infinity,
   "n": 12,
   "rank": 13,
   "candidate": false
  },
  "0142/eng_reverse": {
   "k4": -6.0221200135253,
   "copies_min": -6.481221973880998,
   "copies_max": -5.801798672749979,
   "n": 12,
   "rank": 6,
   "candidate": false
  },
  "0142/eng_keep_nth": {
   "k4": -5.445755442012921,
   "copies_min": -6.105518828983748,
   "copies_max": -5.33965052347856,
   "n": 12,
   "rank": 2,
   "candidate": false
  },
  "0142/eng_drop_nth": {
   "k4": -4.931322620923448,
   "copies_min": -5.024921879501305,
   "copies_max": -4.665568272653109,
   "n": 12,
   "rank": 11,
   "candidate": false
  },
  "0142/eng_step": {
   "k4": -5.7603288956511545,
   "copies_min": -6.171677782222352,
   "copies_max": -5.566542821453248,
   "n": 12,
   "rank": 5,
   "candidate": false
  },
  "0142/eng_affine_std": {
   "k4": -4.990328321801061,
   "copies_min": -5.044662612703086,
   "copies_max": -4.722151738926734,
   "n": 12,
   "rank": 11,
   "candidate": false
  },
  "0142/eng_affine_kry": {
   "k4": -4.990328321801061,
   "copies_min": -5.044662612703086,
   "copies_max": -4.722151738926734,
   "n": 12,
   "rank": 11,
   "candidate": false
  },
  "0142/eng_columns": {
   "k4": -5.892204567897963,
   "copies_min": -6.070994173205393,
   "copies_max": -5.674002742643571,
   "n": 12,
   "rank": 7,
   "candidate": false
  },
  "0142/repeats": {
   "k4": 2.0,
   "copies_min": 2.0,
   "copies_max": 8.0,
   "n": 12,
   "rank": 13,
   "candidate": false
  },
  "0142/base_pairs": {
   "k4": -0.9375,
   "copies_min": -0.9375,
   "copies_max": -0.7916666666666666,
   "n": 12,
   "rank": 13,
   "candidate": false
  },
  "0148/eng_base": {
   "k4": -5.110545353384077,
   "copies_min": -5.236338524802218,
   "copies_max": -5.003094304351364,
   "n": 12,
   "rank": 6,
   "candidate": false
  },
  "0148/freq_sorted": {
   "k4": -2.9013552190055782,
   "copies_min": -2.9470278737081244,
   "copies_max": -2.7781880822410585,
   "n": 12,
   "rank": 7,
   "candidate": false
  },
  "0148/ioc": {
   "k4": 0.056915807560137456,
   "copies_min": 0.05133161512027491,
   "copies_max": 0.0661512027491409,
   "n": 12,
   "rank": 4,
   "candidate": false
  },
  "0148/sep_words": {
   "k4": -Infinity,
   "copies_min": -Infinity,
   "copies_max": -Infinity,
   "n": 12,
   "rank": 13,
   "candidate": false
  },
  "0148/sep_regular": {
   "k4": -Infinity,
   "copies_min": -Infinity,
   "copies_max": -Infinity,
   "n": 12,
   "rank": 13,
   "candidate": false
  },
  "0148/eng_reverse": {
   "k4": -6.144412056843341,
   "copies_min": -6.495829147558959,
   "copies_max": -5.943649756596133,
   "n": 12,
   "rank": 4,
   "candidate": false
  },
  "0148/eng_keep_nth": {
   "k4": -6.099044253502546,
   "copies_min": -6.267380223779869,
   "copies_max": -5.098296138448454,
   "n": 12,
   "rank": 12,
   "candidate": false
  },
  "0148/eng_drop_nth": {
   "k4": -5.056731479681456,
   "copies_min": -5.177384949065263,
   "copies_max": -4.971277606079257,
   "n": 12,
   "rank": 7,
   "candidate": false
  },
  "0148/eng_step": {
   "k4": -5.759808537501923,
   "copies_min": -6.165593134889681,
   "copies_max": -5.55590105894448,
   "n": 12,
   "rank": 2,
   "candidate": false
  },
  "0148/eng_affine_std": {
   "k4": -5.11054535338408,
   "copies_min": -5.2363385248022185,
   "copies_max": -5.003094304351364,
   "n": 12,
   "rank": 6,
   "candidate": false
  },
  "0148/eng_affine_kry": {
   "k4": -5.11054535338408,
   "copies_min": -5.2363385248022185,
   "copies_max": -5.003094304351364,
   "n": 12,
   "rank": 6,
   "candidate": false
  },
  "0148/eng_columns": {
   "k4": -6.027449503142971,
   "copies_min": -6.175756394445149,
   "copies_max": -5.575464857838674,
   "n": 12,
   "rank": 7,
   "candidate": false
  },
  "0148/repeats": {
   "k4": 2.0,
   "copies_min": 2.0,
   "copies_max": 5.0,
   "n": 12,
   "rank": 13,
   "candidate": false
  },
  "0148/base_pairs": {
   "k4": -0.9166666666666666,
   "copies_min": -0.9375,
   "copies_max": -0.8541666666666666,
   "n": 12,
   "rank": 12,
   "candidate": false
  }
 },
 "candidates": [
  "0034/eng_reverse",
  "0034/eng_keep_nth"
 ],
 "candidates_expected_by_chance": 9.2,
 "replication": {
  "0034/eng_reverse": {
   "k4": -5.4582804472186215,
   "fresh_copies": 8,
   "first_copy_at_or_above": null,
   "fresh_max": -5.556524387129956,
   "verdict": "unresolved",
   "p_bound_if_unresolved": 0.1111111111111111
  },
  "0034/eng_keep_nth": {
   "k4": -4.751907523560674,
   "fresh_copies": 6,
   "first_copy_at_or_above": 6,
   "fresh_max": -4.735572098878378,
   "verdict": "not a flag",
   "p_bound_if_unresolved": null
  }
 },
 "flags": [],
 "unresolved": [
  "0034/eng_reverse"
 ],
 "plants": [
  {
   "exp": "0142",
   "L": 26,
   "mask": "none",
   "i": 0,
   "test": "eng_base",
   "reading_value": -4.62966238678313,
   "plaintext_value": -4.255679303868371,
   "copies_max": -4.722151738926735,
   "letters_right": 35,
   "found": true,
   "plaintext_would_be_found": true,
   "reading": "CALEDIBETARTORCOADELEEASTNORTHEASTEALLYTADOHALGENEDABICIDEAWANTBERLINCLOCKIRILYSHOMISAGARLOISNOUN"
  },
  {
   "exp": "0142",
   "L": 26,
   "mask": "none",
   "i": 1,
   "test": "eng_base",
   "reading_value": -4.592331361427648,
   "plaintext_value": -4.420235380511223,
   "copies_max": -4.722151738926735,
   "letters_right": 35,
   "found": true,
   "plaintext_would_be_found": true,
   "reading": "FERNINTKNONVEWEDENTALEASTNORTHEASTALSESONATIONFIGUOUNDHESSENINDBERLINCLOCKUFIDMAGATERSHEREDJCHEWT"
  },
  {
   "exp": "0142",
   "L": 26,
   "mask": "none",
   "i": 2,
   "test": "eng_base",
   "reading_value": -4.760691747735969,
   "plaintext_value": -4.238678626943255,
   "copies_max": -4.722151738926735,
   "letters_right": 34,
   "found": false,
   "plaintext_would_be_found": true,
   "reading": "LONOVORGISONDWILSAEETEASTNORTHEASTHARABALECHUCIDENMRBERPCONATOUBERLINCLOCKSSAARESTOWIEROUGHTSSHOO"
  },
  {
   "exp": "0142",
   "L": 26,
   "mask": "reversal",
   "i": 0,
   "test": "eng_reverse",
   "reading_value": -5.972011277701728,
   "plaintext_value": -4.761928613244291,
   "copies_max": -5.801798672749979,
   "letters_right": 36,
   "found": false,
   "plaintext_would_be_found": true,
   "reading": "WLOCATANDJUNIONITWBENEASTNORTHEASTALREACELELETHISAINTDEADILIACIBERLINCLOCKEEASBARRESTONEBMOAIKLMA"
  },
  {
   "exp": "0142",
   "L": 26,
   "mask": "reversal",
   "i": 1,
   "test": "eng_reverse",
   "reading_value": -5.922751016754045,
   "plaintext_value": -4.961532540926,
   "copies_max": -5.801798672749979,
   "letters_right": 40,
   "found": false,
   "plaintext_would_be_found": true,
   "reading": "LDSONSUSREPOSONLITETREASTNORTHEASTCOMTHANGECMONTOBORDSPRWEBSTEMBERLINCLOCKMAOWIADNEYSAENGSESENJON"
  },
  {
   "exp": "0142",
   "L": 26,
   "mask": "reversal",
   "i": 2,
   "test": "eng_reverse",
   "reading_value": -6.146353814027237,
   "plaintext_value": -5.208049668953652,
   "copies_max": -5.801798672749979,
   "letters_right": 35,
   "found": false,
   "plaintext_would_be_found": true,
   "reading": "REECPLANDOOFOAROPSDONEASTNORTHEASTOIDCOTCHIEGOALISTEOMSTOTOFROMBERLINCLOCKSSEADWPUTHEADCIESSFOODD"
  },
  {
   "exp": "0142",
   "L": 26,
   "mask": "X spaces",
   "i": 0,
   "test": "sep_words",
   "reading_value": -Infinity,
   "plaintext_value": -0.3041520031580787,
   "copies_max": -Infinity,
   "letters_right": 31,
   "found": false,
   "plaintext_would_be_found": true,
   "reading": "PGHEXTLEHEASOANYHEGAMEASTNORTHEASTOFCOMECTADBELEPASASJUIRSCISHIBERLINCLOCKEDIASCHITAGUETTINDEDTCJ"
  },
  {
   "exp": "0142",
   "L": 26,
   "mask": "X spaces",
   "i": 1,
   "test": "sep_words",
   "reading_value": -Infinity,
   "plaintext_value": -0.34812495191765974,
   "copies_max": -Infinity,
   "letters_right": 31,
   "found": false,
   "plaintext_would_be_found": true,
   "reading": "WAKEFACHMANHIMILERLUREASTNORTHEASTHATTTOILBERSHOPOPEFAMEENVADVABERLINCLOCKEDFREMABHOWSUPASSEFUVEV"
  },
  {
   "exp": "0142",
   "L": 26,
   "mask": "X spaces",
   "i": 2,
   "test": "sep_words",
   "reading_value": -Infinity,
   "plaintext_value": 0.24057211711333257,
   "copies_max": -Infinity,
   "letters_right": 37,
   "found": false,
   "plaintext_would_be_found": true,
   "reading": "OECSGROVENDTHEHASPLYDEASTNORTHEASTCITAMAPEILLSIONORSPNDCAXERRETBERLINCLOCKHONSMONSPININBUTORETTHR"
  },
  {
   "exp": "0142",
   "L": 26,
   "mask": "X every kth",
   "i": 0,
   "test": "sep_regular",
   "reading_value": -Infinity,
   "plaintext_value": -0.3535533905932737,
   "copies_max": -Infinity,
   "letters_right": 32,
   "found": false,
   "plaintext_would_be_found": true,
   "reading": "AWNTOFLIRTHORANRBTAIAEASTNORTHEASTOLIATEDACTMSAPLENBIKEDGEISCUEBERLINCLOCKHALUSPLEPEITSECULOFUTIG"
  },
  {
   "exp": "0142",
   "L": 26,
   "mask": "X every kth",
   "i": 1,
   "test": "sep_regular",
   "reading_value": -Infinity,
   "plaintext_value": -0.35136418446315326,
   "copies_max": -Infinity,
   "letters_right": 39,
   "found": false,
   "plaintext_would_be_found": true,
   "reading": "ORTOWAPEOFIRFIGENTSALEASTNORTHEASTENDSLOOREWETTONDLYOXHILEMILOFBERLINCLOCKIDDEDSEVERKEMOMESINDRYT"
  },
  {
   "exp": "0142",
   "L": 26,
   "mask": "X every kth",
   "i": 2,
   "test": "sep_regular",
   "reading_value": -Infinity,
   "plaintext_value": -0.6375164477658773,
   "copies_max": -Infinity,
   "letters_right": 38,
   "found": false,
   "plaintext_would_be_found": true,
   "reading": "IENTALSDEREIMBLASASEFEASTNORTHEASTEALPEDDRAELRDNESALSATTERBERYBBERLINCLOCKSWINGHTHERTHISGRABEDINZ"
  },
  {
   "exp": "0140",
   "L": 23,
   "mask": "none",
   "i": 0,
   "test": "eng_base",
   "reading_value": -4.865259097152336,
   "plaintext_value": -4.020418586667907,
   "copies_max": -4.880476311445674,
   "letters_right": 32,
   "found": true,
   "plaintext_would_be_found": true,
   "reading": "LTDOIALDNTMEMANZIASHSEASTNORTHEASTESINAWLNAQSAFLANOMESANDISOSTOBERLINCLOCKFORGETACAMERCOSCFMORASL"
  },
  {
   "exp": "0140",
   "L": 23,
   "mask": "none",
   "i": 1,
   "test": "eng_base",
   "reading_value": -5.016937851671445,
   "plaintext_value": -4.341529311542787,
   "copies_max": -4.880476311445674,
   "letters_right": 33,
   "found": false,
   "plaintext_would_be_found": true,
   "reading": "EFTHVALFFEANDTHESAJAVEASTNORTHEASTWOPALUPMNDGIEBYRKMORELDRSTONTBERLINCLOCKOOKGREAKOUTGRICOFILORWA"
  },
  {
   "exp": "0140",
   "L": 23,
   "mask": "none",
   "i": 2,
   "test": "eng_base",
   "reading_value": -4.963907167652664,
   "plaintext_value": -4.342449584943922,
   "copies_max": -4.880476311445674,
   "letters_right": 35,
   "found": false,
   "plaintext_would_be_found": true,
   "reading": "IGMAKIDSTBYCATESEEUSREASTNORTHEASTAMNYGUTTONESIFYFOGHVEWARKSCOMBERLINCLOCKNAKSRSANDTROKENDSHAOYAC"
  },
  {
   "exp": "0140",
   "L": 23,
   "mask": "reversal",
   "i": 0,
   "test": "eng_reverse",
   "reading_value": -6.289137839548456,
   "plaintext_value": -5.069133110058933,
   "copies_max": -5.919036530737811,
   "letters_right": 39,
   "found": false,
   "plaintext_would_be_found": true,
   "reading": "WNUETUGARANISHEMALRYLEASTNORTHEASTILORTGLELYQSOCUMBERLGCLICTLOTBERLINCLOCKEDAIBOROTERSCWHICHOUSDY"
  },
  {
   "exp": "0140",
   "L": 23,
   "mask": "reversal",
   "i": 1,
   "test": "eng_reverse",
   "reading_value": -6.0301989459074745,
   "plaintext_value": -4.89916585044709,
   "copies_max": -5.919036530737811,
   "letters_right": 38,
   "found": false,
   "plaintext_would_be_found": true,
   "reading": "NEIFEWSHEREMSISTLASDIEASTNORTHEASTSETHANTLITHEYLRECIALSCCRECTHOBERLINCLOCKHILDOLESSLFTYDADUNEJOET"
  },
  {
   "exp": "0140",
   "L": 23,
   "mask": "reversal",
   "i": 2,
   "test": "eng_reverse",
   "reading_value": -5.857258313712296,
   "plaintext_value": -4.684913804587941,
   "copies_max": -5.919036530737811,
   "letters_right": 35,
   "found": true,
   "plaintext_would_be_found": true,
   "reading": "RNDETTERBEDRINGHARANCEASTNORTHEASTEWICHLBERCASPFERISELEOTOFGOREBERLINCLOCKUTONSCRETEPEALNESNERGVI"
  },
  {
   "exp": "0140",
   "L": 23,
   "mask": "X spaces",
   "i": 0,
   "test": "sep_words",
   "reading_value": -Infinity,
   "plaintext_value": -0.37114804143884833,
   "copies_max": -Infinity,
   "letters_right": 43,
   "found": false,
   "plaintext_would_be_found": true,
   "reading": "TNKLRHANETHASROYOFTHEEASTNORTHEASTRELASMALPALMLOTOMSADALSSTOLONBERLINCLOCKHNOWINSFORCAOLIFORODUUT"
  },
  {
   "exp": "0140",
   "L": 23,
   "mask": "X spaces",
   "i": 1,
   "test": "sep_words",
   "reading_value": -Infinity,
   "plaintext_value": -0.5390403711262475,
   "copies_max": -Infinity,
   "letters_right": 33,
   "found": false,
   "plaintext_would_be_found": true,
   "reading": "LTMERYWOKERBARRELDWABEASTNORTHEASTRONICEJAZAMELOPRIOLEPUITCRIBEBERLINCLOCKYDOFPEDEDBLEIISATTHEREE"
  },
  {
   "exp": "0140",
   "L": 23,
   "mask": "X spaces",
   "i": 2,
   "test": "sep_words",
   "reading_value": -Infinity,
   "plaintext_value": 0.15105034345567483,
   "copies_max": -Infinity,
   "letters_right": 33,
   "found": false,
   "plaintext_would_be_found": true,
   "reading": "YAPRALPHISSARYOKSARZIEASTNORTHEASTIWALTISYPTHEHIXRELYSTHROUNTYSBERLINCLOCKIESDIERSEGASONERUDFINDF"
  },
  {
   "exp": "0140",
   "L": 23,
   "mask": "X every kth",
   "i": 0,
   "test": "sep_regular",
   "reading_value": -Infinity,
   "plaintext_value": -0.33333333333333337,
   "copies_max": -Infinity,
   "letters_right": 33,
   "found": false,
   "plaintext_would_be_found": true,
   "reading": "PHEYDABEROLDDUERTOREMEASTNORTHEASTERDENGTYWERODUMHIGOWRMISUDDLEBERLINCLOCKVESTTIFILALBINEDOMSOCIC"
  },
  {
   "exp": "0140",
   "L": 23,
   "mask": "X every kth",
   "i": 1,
   "test": "sep_regular",
   "reading_value": -Infinity,
   "plaintext_value": -0.4899539464934427,
   "copies_max": -Infinity,
   "letters_right": 36,
   "found": false,
   "plaintext_would_be_found": true,
   "reading": "PADLSWOOSCMINTURBABOREASTNORTHEASTHOSEMENDEMCMETWEERYATLOFAINTOBERLINCLOCKSBYNTORRUPERKWRSTOPADEM"
  },
  {
   "exp": "0140",
   "L": 23,
   "mask": "X every kth",
   "i": 2,
   "test": "sep_regular",
   "reading_value": -Infinity,
   "plaintext_value": -0.574959574576069,
   "copies_max": -Infinity,
   "letters_right": 41,
   "found": false,
   "plaintext_would_be_found": true,
   "reading": "WICNTIRNROCTINAVEADIDEASTNORTHEASTBEEVERINCLARSMSRVIVANWELETOBEBERLINCLOCKTHEDIROCESTALSITRERGIMP"
  }
 ],
 "plants_found": {
  "0142 none": "2 of 3",
  "0142 reversal": "0 of 3",
  "0142 X spaces": "0 of 3",
  "0142 X every kth": "0 of 3",
  "0140 none": "1 of 3",
  "0140 reversal": "1 of 3",
  "0140 X spaces": "0 of 3",
  "0140 X every kth": "0 of 3"
 },
 "plant_design": "3 per mask, Carter 1923 with the known letters set after masking, random alphabet and key, Beaufort form; climbed by the frozen climb_text (10 tempering runs); found = the mask's own test strictly above all 12 copies of that experiment",
 "seconds": 17774.4
}
```

Notes: 2 candidate cells of 112 (chance 9.2); replication: 1 not a flag, 1 unresolved, 0 flags. Plants found by their own test: {'0142 none': '2 of 3', '0142 reversal': '0 of 3', '0142 X spaces': '0 of 3', '0142 X every kth': '0 of 3', '0140 none': '1 of 3', '0140 reversal': '1 of 3', '0140 X spaces': '0 of 3', '0140 X every kth': '0 of 3'}.


