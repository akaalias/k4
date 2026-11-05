# 0270-f6.1-free-alphabet-around-every-move-lengths-6-10-with-stand-ins: F6.1: one free alphabet after or before every type-1 move, key lengths 6-10, every setting K4 fits decided by D1's one-run decider, with 20 shuffled stand-ins through the same procedure

**Family:** 6-move-then-table  
**Parent:** 0253-f1.4-one-alphabet-residue-decided-by-the-one-run-decider  
**Decision:** reverted  
**Run:** 2026-11-04T21:46:13+00:00, 32557.6 s, status ran  
**Time by phase:** unattributed 4370 s, run 32558 s, record 0 s

## In plain words

Sanborn said he wrote the message into a grid, read it out another way, and then used the cipher table. With his own scrambled alphabet in the table and a short key word, thousands of such recipes agree with the 24 known letters. For each one we search for the most English-looking reading of K4 and do the same on scrambled copies; twenty scrambled stand-ins for K4 go through the very same test, so we know what 'K4 wins often' would mean.

## Walkthrough, by hand

1. Pick a recipe: write the message in rows of 9 and read the columns in the order of a key word (the move), then encipher on the table with an unknown scrambled alphabet and a 7-letter key.
2. Undo the move on paper for the 24 known letters: each lands on a carved place and a key slot.
3. Check that some alphabet makes every pair of known letters in one slot agree.
4. Search alphabets and keys for the most English-looking reading of K4 under the recipe.
5. Shuffle K4 until the shuffle also passes step 3, search it the same way; stop when a shuffle reads as well as K4, at most 12 shuffles.
6. Do steps 4-5 for every recipe K4 fits, and for twenty scrambled stand-ins of K4; compare how often each wins all 12.

## Worked example (generated)

```
F6.1: one free alphabet around a move, key lengths 6-10, decided setting by setting.

  setting      columns of a 9-wide grid read in key-word order, then the table, key length 7, Beaufort
  slot map     each carved letter's key slot and message place follow from the move
  K4 gets one tempering search under that setting; shuffles of K4 that fit the same 24 checks get the same,
  one at a time, until a shuffle reads as well as K4 (at most 12).
  Twenty shuffled stand-ins for K4 go through the whole procedure: K4's rate of wins must stand out from theirs.
```

## Lineage

Inherits from 0253-f1.4-one-alphabet-residue-decided-by-the-one-run-decider. What changed: F6.1 at lengths 6-10, reopened by D2 (0252: 7,443 settings, one-run power 31 of 48 on plants drawn from K4's own fitting settings). 0253's decide() unchanged (one tempering run of 0252's climb on K4, then shuffles the exact decider fits at the same setting climbed one at a time, stop at the first at or above, at most 12; no escalation, so K4 and the stand-ins are decided alike), now on 0129's move library: every (move, order, length 6-10, form) that fits K4. Twenty full shuffles of K4 stand in for it (0254/0255: a count over settings needs texts put through the whole procedure), each on 300 of its own fitting settings.

## Hypothesis (domain expert)

F6.1 (C1(a): 'a matrix code... then went back to this table'; C27(c): a 'slightly different' tableau): one free alphabet on both sides (Quagmire III with an unknown order), a periodic key of length 6-10, after or before one move of 0129's type-1 library (27,852 routes: columnar, keyword columnar, K3's rule, turns, rail fence, grid paths...), Beaufort or added form. 0129/0130 found no fit below 6 and fits from 6 at the copies' rate, so the known letters cannot decide these settings and English must. Decider: D1's one run of 0140's tempering generalised to any slot map and reading order (0252), copies fitted exactly at the same setting (0253). Clue entries C1(a), C27(c), C11.

## Prediction

K4's rate of settings above all 12 copies inside the 20 stand-ins' spread (p above 0.05); plants (24, on settings K4 fits) found about 14 of 24; no reading English. Zero candidates.

## Method

1. Settings: 0129's route library (27,852 moves) x order (A move then table, B table then move) x key length 6-10 x form (added, Beaufort); each decided exactly on K4 by 0252's fits(); the fitting ones are K4's cell.
2. Per setting (one job, own seed): 0253's decide() without escalation: one tempering run on K4, then shuffles that fit the same setting climbed one at a time until one reaches K4, at most 12.
3. Stand-ins: 20 shuffles of K4 (seed 2680), each with its own fitting settings found the same way, 300 drawn and decided alike.
4. Plants: 12 clean and 12 Sanborn-style messages on settings K4 fits, random alphabet and key; found if above all 12.
5. Verdict: K4's share of settings above all 12 copies, ranked among the stand-ins' shares.

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
 "item": "F6.1 lengths 6-10 (reopened by D2, 0252)",
 "decider": "0253's decide() unchanged, without escalation: one run of 0252's generalised tempering (16 x 625 x 1000) on the target, then shuffles the exact decider fits at the same setting, climbed one at a time, stop at the first at or above, at most 12",
 "self_check_against_0140": [
  [
   23,
   -5.23832,
   -5.23832
  ],
  [
   26,
   -5.13042,
   -5.13042
  ]
 ],
 "library": 27852,
 "lengths": [
  6,
  7,
  8,
  9,
  10
 ],
 "orders": [
  "A move then table",
  "B table then move"
 ],
 "forms": [
  "added",
  "Beaufort"
 ],
 "settings_listed": 557040,
 "k4_fitting_settings": 7443,
 "k4_fitting_by_order_form_length": {
  "AB10": 301,
  "BB10": 1389,
  "AV10": 641,
  "BV10": 2831,
  "BV8": 782,
  "AV8": 191,
  "AB8": 54,
  "BB7": 89,
  "BV7": 230,
  "AB9": 174,
  "BV6": 23,
  "BB8": 221,
  "AV9": 444,
  "AV7": 48,
  "AB7": 14,
  "BB6": 8,
  "AB6": 1,
  "AV6": 2
 },
 "targets": {
  "k4": {
   "cell_size": 7443,
   "decided": 7443,
   "above_all_12": 570,
   "rate": 0.0766,
   "beat_first_rate": 0.5005,
   "lost_copies": 2
  },
  "standin0": {
   "cell_size": 7411,
   "decided": 300,
   "above_all_12": 24,
   "rate": 0.08,
   "beat_first_rate": 0.5067,
   "lost_copies": 0
  },
  "standin1": {
   "cell_size": 7734,
   "decided": 300,
   "above_all_12": 40,
   "rate": 0.1333,
   "beat_first_rate": 0.5367,
   "lost_copies": 0
  },
  "standin2": {
   "cell_size": 7652,
   "decided": 300,
   "above_all_12": 17,
   "rate": 0.0567,
   "beat_first_rate": 0.49,
   "lost_copies": 1
  },
  "standin3": {
   "cell_size": 6586,
   "decided": 300,
   "above_all_12": 35,
   "rate": 0.1167,
   "beat_first_rate": 0.5567,
   "lost_copies": 0
  },
  "standin4": {
   "cell_size": 7617,
   "decided": 300,
   "above_all_12": 9,
   "rate": 0.03,
   "beat_first_rate": 0.49,
   "lost_copies": 0
  },
  "standin5": {
   "cell_size": 7883,
   "decided": 300,
   "above_all_12": 24,
   "rate": 0.08,
   "beat_first_rate": 0.4867,
   "lost_copies": 0
  },
  "standin6": {
   "cell_size": 7368,
   "decided": 300,
   "above_all_12": 20,
   "rate": 0.0667,
   "beat_first_rate": 0.5,
   "lost_copies": 0
  },
  "standin7": {
   "cell_size": 6616,
   "decided": 300,
   "above_all_12": 15,
   "rate": 0.05,
   "beat_first_rate": 0.5,
   "lost_copies": 0
  },
  "standin8": {
   "cell_size": 7449,
   "decided": 300,
   "above_all_12": 27,
   "rate": 0.09,
   "beat_first_rate": 0.4833,
   "lost_copies": 0
  },
  "standin9": {
   "cell_size": 7108,
   "decided": 300,
   "above_all_12": 21,
   "rate": 0.07,
   "beat_first_rate": 0.5067,
   "lost_copies": 0
  },
  "standin10": {
   "cell_size": 7587,
   "decided": 300,
   "above_all_12": 23,
   "rate": 0.0767,
   "beat_first_rate": 0.52,
   "lost_copies": 0
  },
  "standin11": {
   "cell_size": 7711,
   "decided": 300,
   "above_all_12": 19,
   "rate": 0.0633,
   "beat_first_rate": 0.4567,
   "lost_copies": 0
  },
  "standin12": {
   "cell_size": 7949,
   "decided": 300,
   "above_all_12": 22,
   "rate": 0.0733,
   "beat_first_rate": 0.5,
   "lost_copies": 0
  },
  "standin13": {
   "cell_size": 7514,
   "decided": 300,
   "above_all_12": 30,
   "rate": 0.1,
   "beat_first_rate": 0.5067,
   "lost_copies": 0
  },
  "standin14": {
   "cell_size": 6915,
   "decided": 300,
   "above_all_12": 19,
   "rate": 0.0633,
   "beat_first_rate": 0.51,
   "lost_copies": 0
  },
  "standin15": {
   "cell_size": 7678,
   "decided": 300,
   "above_all_12": 21,
   "rate": 0.07,
   "beat_first_rate": 0.4967,
   "lost_copies": 0
  },
  "standin16": {
   "cell_size": 6846,
   "decided": 300,
   "above_all_12": 24,
   "rate": 0.08,
   "beat_first_rate": 0.47,
   "lost_copies": 0
  },
  "standin17": {
   "cell_size": 7222,
   "decided": 300,
   "above_all_12": 14,
   "rate": 0.0467,
   "beat_first_rate": 0.4467,
   "lost_copies": 0
  },
  "standin18": {
   "cell_size": 7566,
   "decided": 300,
   "above_all_12": 22,
   "rate": 0.0733,
   "beat_first_rate": 0.5167,
   "lost_copies": 0
  },
  "standin19": {
   "cell_size": 8221,
   "decided": 300,
   "above_all_12": 16,
   "rate": 0.0533,
   "beat_first_rate": 0.53,
   "lost_copies": 0
  }
 },
 "k4_rate": 0.0766,
 "standins_rates": [
  0.08,
  0.1333,
  0.0567,
  0.1167,
  0.03,
  0.08,
  0.0667,
  0.05,
  0.09,
  0.07,
  0.0767,
  0.0633,
  0.0733,
  0.1,
  0.0633,
  0.07,
  0.08,
  0.0467,
  0.0733,
  0.0533
 ],
 "standins_at_or_above_k4": 8,
 "p": 0.4286,
 "fair_rate_if_independent": 0.0769,
 "top_settings": [
  {
   "setting": "two turns cw 49,41 inverse order A L=9 B",
   "above": 12,
   "score": -5.89594,
   "reading": "YTJUNPPUDITEFSGJOMINMEASTNORTHEASTEIFHINKKJORLOCAAUZVULEOFPDVMPBERLINCLOCKIFSPLELLRZOUTACYBRDGEAW",
   "known_in_place": 24
  },
  {
   "setting": "K3 rule a=35 b=18 order A L=10 V",
   "above": 12,
   "score": -5.9038,
   "reading": "WYSQIPURLESKKCILMOSMDEASTNORTHEASTRGTRYTLFKAEOPUNZIOPCNMIDISTSOBERLINCLOCKAQHHEOBBCETANINCEAMDHWL",
   "known_in_place": 24
  },
  {
   "setting": "two turns cw 5,32 inverse order B L=10 V",
   "above": 12,
   "score": -5.9406,
   "reading": "QDEXTARCWOMONVEVUDANGEASTNORTHEASTCASHULXDYLMELEMBHYMNABUUILKRABERLINCLOCKMCUULGHTWTHSTAOYAHPNPAM",
   "known_in_place": 24
  },
  {
   "setting": "K3 rule a=68 b=32 order A L=10 B",
   "above": 12,
   "score": -5.94491,
   "reading": "NWLAIRAYNALPTOQSPHOEGEASTNORTHEASTPAIGWESFMDECOEIIDRYBNWRCRIENTBERLINCLOCKANOKPJJKAHVSPMEGCIGASMJ",
   "known_in_place": 24
  },
  {
   "setting": "K3 rule a=31 b=12 order A L=10 B",
   "above": 12,
   "score": -5.96057,
   "reading": "COVFCPOPSSAVILUTAGWBREASTNORTHEASTAISMOKGMRBHCLOMFNNYSUBGRYJEDWBERLINCLOCKYYILLDNOFIRAYSYSPSRRPQK",
   "known_in_place": 24
  },
  {
   "setting": "two turns cw 92,23 order B L=10 B",
   "above": 12,
   "score": -5.96772,
   "reading": "BEALBUTIFSUDYTAABSBTAEASTNORTHEASTRONDSKSTICRJHNACAYCUMMVBEORTRBERLINCLOCKTHLENIYTGGUWTHAKNMHMVIC",
   "known_in_place": 24
  },
  {
   "setting": "two turns cw 77,93 order A L=10 V",
   "above": 12,
   "score": -5.97507,
   "reading": "DNZEUKIFADFRESUNLUDUTEASTNORTHEASTTWHAMEUIDLOBMAXCPTJHMPORKTXTIBERLINCLOCKTENYHAQMYSPTGAVIAVYURUV",
   "known_in_place": 24
  },
  {
   "setting": "K3 rule a=69 b=19 order A L=10 V",
   "above": 12,
   "score": -5.97812,
   "reading": "PFMRDDLESOATTMSIODNTSEASTNORTHEASTDUNLFGUFCRTISLACDBOQNIKOPHHHABERLINCLOCKBUDYNQDPOMPIDLIGRASHLDE",
   "known_in_place": 24
  },
  {
   "setting": "K3 rule a=0 b=43 order A L=10 V",
   "above": 12,
   "score": -5.98987,
   "reading": "SEGICTAPTIICUSOFTMHCVEASTNORTHEASTPUAGWMTJZTOPWONYMUTANOUNDZAXLBERLINCLOCKFDOEMMDTNTLHTERKSECEOAX",
   "known_in_place": 24
  },
  {
   "setting": "two turns cw 32,20 inverse order B L=10 V",
   "above": 12,
   "score": -5.99526,
   "reading": "XCHPETUBFTRUWWCBINCPHEASTNORTHEASTOUYNUIADZAYMOMJDEDOVIYTAMCINNBERLINCLOCKMDMUCFADEMAKEVIONXFLBSF",
   "known_in_place": 24
  },
  {
   "setting": "two turns cw 52,50 order A L=10 V",
   "above": 12,
   "score": -5.99606,
   "reading": "FIMIGFUUEROSCCHEMIKSYEASTNORTHEASTADYYFERDEBYYJMJBBOYVMOHIXBOMRBERLINCLOCKOLOPFMRNMETDEAHENNCARWV",
   "known_in_place": 24
  },
  {
   "setting": "two turns cw 42,72 inverse order B L=10 B",
   "above": 12,
   "score": -5.99627,
   "reading": "UOVRRESCRELMTFROKECHFEASTNORTHEASTTEXUIJTYILKWWISSSCAMWYSANCWZNBERLINCLOCKCBFMEJUWQUISHSWASTHPASF",
   "known_in_place": 24
  },
  {
   "setting": "two turns cw 41,74 inverse order B L=10 B",
   "above": 12,
   "score": -6.0048,
   "reading": "VMVMVCANDSGYTDUEFRATWEASTNORTHEASTHCCGWZPWMBYUKUGTCVINYWORELAYDBERLINCLOCKLANYMBILPOJRATHIRSSGDRY",
   "known_in_place": 24
  },
  {
   "setting": "two turns cw 80,90 order A L=10 V",
   "above": 12,
   "score": -6.01039,
   "reading": "DNEYSPTGAVIAVYURUDVUTEASTNORTHEASTTWHAMEUIDLOBMAXCPTJHMPORKTXTIBERLINCLOCKTENAQMYHZUKIFADFRESUNLU",
   "known_in_place": 24
  },
  {
   "setting": "two turns cw 26,45 order B L=10 B",
   "above": 12,
   "score": -6.01097,
   "reading": "NYCHAMDVNYAMICHTYSRYBEASTNORTHEASTBOSTHGRIUNNELKEJBYYUFIEUMPONUBERLINCLOCKIYMYCIKWTEUKNUIRHTSTLLQ",
   "known_in_place": 24
  },
  {
   "setting": "two turns cw 94,76 order A L=10 V",
   "above": 12,
   "score": -6.01477,
   "reading": "DNEUKIFADFDESUNLUDVUTEASTNORTHEASTTWHAMESWDLOBMAYCYTJHMYORKTXTIBERLINCLOCKTENAQMPSYTGAVIAVPURUPHZ",
   "known_in_place": 24
  },
  {
   "setting": "two turns cw 77,29 inverse order A L=10 B",
   "above": 12,
   "score": -6.01751,
   "reading": "LTUDQZLIEDFMAYTTCKETVEASTNORTHEASTGLVBSOLDCWQTRCULEASAROFFORSMCBERLINCLOCKMYFRACKJBEGYUBBOZNHEDLI",
   "known_in_place": 24
  },
  {
   "setting": "two turns cw 95,75 order A L=10 V",
   "above": 12,
   "score": -6.02004,
   "reading": "DNZEUKIFADFRESUNLUDUTEASTNORTHEASTTWHAMEUIDLOBMAXCPTJHMPORKTXTIBERLINCLOCKTENAQMYSPTGAVIAVYURUVYH",
   "known_in_place": 24
  },
  {
   "setting": "two turns cw 78,92 order A L=10 V",
   "above": 12,
   "score": -6.03388,
   "reading": "DNQMPSYTGAVIAVPURUVUTEASTNORTHEASTTWHAMESWDLOBMAYCYTJHMYORKTXTIBERLINCLOCKTENAPHZEUKIFADFDESUNLUD",
   "known_in_place": 24
  },
  {
   "setting": "K3 rule a=68 b=8 inverse order B L=10 V",
   "above": 12,
   "score": -6.03566,
   "reading": "NDEIINBWYEBTCOMGMHFRREASTNORTHEASTELEEDBLFVARSAVIUIHCSPXADUSAAMBERLINCLOCKDUOSSLELOYVGSUVYCRPASME",
   "known_in_place": 24
  }
 ],
 "plants": {
  "clean_found": [
   6,
   12
  ],
  "sanborn_found": [
   5,
   12
  ],
  "each": {
   "0": {
    "cls": "clean",
    "setting": "two turns cw 57,95 order B L=8 V",
    "found": true,
    "above": 12,
    "score": -4.18035,
    "letters_right": 97
   },
   "1": {
    "cls": "clean",
    "setting": "two turns cw 55,83 order B L=8 V",
    "found": false,
    "above": 3,
    "score": -6.86084,
    "letters_right": 46
   },
   "2": {
    "cls": "clean",
    "setting": "two turns cw 2,50 order B L=10 B",
    "found": true,
    "above": 12,
    "score": -5.74512,
    "letters_right": 42
   },
   "3": {
    "cls": "clean",
    "setting": "K3 rule a=12 b=28 inverse order B L=10 V",
    "found": false,
    "above": 4,
    "score": -6.42181,
    "letters_right": 47
   },
   "4": {
    "cls": "clean",
    "setting": "two turns cw 37,86 order A L=10 V",
    "found": false,
    "above": 1,
    "score": -6.45994,
    "letters_right": 44
   },
   "5": {
    "cls": "clean",
    "setting": "two turns cw 8,38 order B L=10 V",
    "found": false,
    "above": 0,
    "score": -6.67024,
    "letters_right": 39
   },
   "6": {
    "cls": "clean",
    "setting": "two turns cw 33,91 inverse order B L=8 V",
    "found": true,
    "above": 12,
    "score": -6.61713,
    "letters_right": 49
   },
   "7": {
    "cls": "clean",
    "setting": "two turns cw 59,40 order B L=10 V",
    "found": false,
    "above": 0,
    "score": -6.511,
    "letters_right": 42
   },
   "8": {
    "cls": "clean",
    "setting": "two turns cw 59,79 order B L=10 B",
    "found": true,
    "above": 12,
    "score": -5.43098,
    "letters_right": 70
   },
   "9": {
    "cls": "clean",
    "setting": "two turns cw 54,80 order B L=10 V",
    "found": true,
    "above": 12,
    "score": -5.70075,
    "letters_right": 57
   },
   "10": {
    "cls": "clean",
    "setting": "K3 rule a=22 b=63 order B L=10 V",
    "found": true,
    "above": 12,
    "score": -6.09011,
    "letters_right": 44
   },
   "11": {
    "cls": "clean",
    "setting": "K3 rule a=39 b=2 order A L=10 V",
    "found": false,
    "above": 2,
    "score": -6.78213,
    "letters_right": 39
   },
   "12": {
    "cls": "xstops",
    "setting": "two turns cw 50,48 inverse order B L=10 V",
    "found": false,
    "above": 0,
    "score": -6.9504,
    "letters_right": 45
   },
   "13": {
    "cls": "xstops",
    "setting": "two turns cw 71,60 order B L=10 V",
    "found": true,
    "above": 12,
    "score": -5.92066,
    "letters_right": 50
   },
   "14": {
    "cls": "xstops",
    "setting": "two turns cw 68,36 order B L=10 V",
    "found": true,
    "above": 12,
    "score": -6.42279,
    "letters_right": 44
   },
   "15": {
    "cls": "xstops",
    "setting": "two turns cw 89,58 order B L=10 B",
    "found": false,
    "above": 0,
    "score": -6.80931,
    "letters_right": 46
   },
   "16": {
    "cls": "xstops",
    "setting": "K3 rule a=28 b=32 order B L=10 V",
    "found": false,
    "above": 2,
    "score": -6.43059,
    "letters_right": 38
   },
   "17": {
    "cls": "xstops",
    "setting": "turn cw 11 order B L=10 V",
    "found": true,
    "above": 12,
    "score": -6.12159,
    "letters_right": 45
   },
   "18": {
    "cls": "xstops",
    "setting": "two turns cw 17,95 inverse order A L=10 V",
    "found": false,
    "above": 1,
    "score": -6.15336,
    "letters_right": 47
   },
   "19": {
    "cls": "xstops",
    "setting": "two turns cw 41,37 order A L=9 V",
    "found": false,
    "above": 5,
    "score": -6.42786,
    "letters_right": 40
   },
   "20": {
    "cls": "xstops",
    "setting": "two turns cw 10,24 order A L=9 V",
    "found": false,
    "above": 0,
    "score": -6.69368,
    "letters_right": 41
   },
   "21": {
    "cls": "xstops",
    "setting": "two turns cw 83,75 order B L=10 V",
    "found": false,
    "above": 3,
    "score": -6.50888,
    "letters_right": 37
   },
   "22": {
    "cls": "xstops",
    "setting": "K3 rule a=8 b=30 inverse order B L=10 B",
    "found": true,
    "above": 12,
    "score": -5.56482,
    "letters_right": 54
   },
   "23": {
    "cls": "xstops",
    "setting": "two turns cw 49,63 order B L=7 V",
    "found": true,
    "above": 12,
    "score": -5.34607,
    "letters_right": 65
   }
  }
 },
 "core_seconds": 1117634,
 "compute_seconds": 32482,
 "exhaustive": true,
 "exhaustive_over": "every type-1 move of 0129's library, both orders, key lengths 6-10, both forms, that K4 fits on one free alphabet; each decided at D1's one-run power",
 "resumed_units": 1028,
 "cost_estimate": "about 7,443 K4 settings (0252) and 6,000 stand-in settings x about 4.1 one-run climbs (H_12 copies) at 17-25 core-s, plus 21 exact scans of the library (about 18 core-minutes each) and 24 plants: about 300-400 core-hours; on AWS c8g.8xlarge (32 cores, $0.60/h): about 10-13 h, about $6-8"
}
```

Notes: F6.1 lengths 6-10: 7443 settings fit K4; K4 above all 12 copies in 570 (7.7%); 20 stand-ins 3.0-13.3%, 8 at or above K4 (p 0.43); plants clean [6, 12], Sanborn-style [5, 12].


