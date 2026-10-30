# 0261-f1.12-three-measured-power-cells-against-100-copies-with-second-deciders: F1.12: F1.1 Beaufort 23 and 26 and F1.2 at 13, K4 against 100 of its own copies with the one-run decider, then MIX8m and the blind judge as second deciders

**Family:** 1-keyed-periodic  
**Parent:** 0229-d1-one-free-alphabet-power-per-run-with-enough-plants  
**Decision:** reverted  
**Run:** 2026-10-30T06:44:55+00:00, 759.1 s, status ran  
**Time by phase:** test 10 s, run 759 s, record 0 s

## In plain words

Three versions of the cipher table with a scrambled alphabet were closed after K4 read no better than 12 scrambled copies of itself. Twelve is a small crowd. Here K4 faces 100 copies in each, and two more readers judge the results: a stronger statistical model of English, and a language model that reads for words.

## Walkthrough, by hand

1. Take one cell, say a scrambled alphabet on both sides of the table with a key of 23 letters, Beaufort form.
2. Search for the alphabet and key that make K4 read most like English while keeping the 24 known letters.
3. Make 100 scrambled copies of K4 that fit the same 24 letters equally well and search each the same way.
4. Rank K4's best reading among the 100 copies' by the search's score, by a stronger English model, and by a language model reading for words.
5. A real answer should come out on top on all three.

## Worked example (generated)

```
F1.12: three cells, K4 against 100 of its own copies, three deciders.

  cell            alphabets  key length  checks
  F1.1 B23        one        23          7
  F1.1 B26        one        26          1
  F1.2 13         two        13          11

  each text: one tempering run keeping the 24 known letters -> best reading
  rank K4 among its copies by quadgrams, by MIX8m, by the blind judge.
```

## Lineage

Inherits from 0229-d1-one-free-alphabet-power-per-run-with-enough-plants. What changed: F1.12 (Alexis, 2026-10-28, #100: close at stated power and still rerun, so a missed lead gets a second chance). The three cells closed at measured power on 2026-10-28 had K4 ranked among 12 copies only (9th, 12th and 13th of 13). Here each cell's K4 is ranked among 100 of its own copies, each climbed with the one-run decider (D1: one tempering run, 0140's climb for one alphabet; 0144's for two, with as many runs as D1b qualifies); the best readings then rescored by MIX8m (0233) and read by the blind judge, K4 and copies together. 8 plants per cell in the same run.

## Hypothesis (domain expert)

F1.1 (Quagmire III with an unknown order, Beaufort form) at key lengths 23 (7 checks) and 26 (1 check), and F1.2 (Quagmire IV, two unknown alphabets) at 13 (11 checks): the known letters leave thousands of alphabets, so English decides. Design 2 (0139-0146) put K4 9th, 12th and 13th of 13; D1 (0228, 0229) and A6.2 (0226) measured power on clean and Sanborn-style plants: L23 33/40 and 32/48, L26 13/24 and 17/24, L13 7/10 and 17/24. With 100 copies K4's rank is measured to 1%; MIX8m (1.95 bits per letter against the quadgrams' 1.75) and the judge (which reads telegraphese and abbreviated English, 0251) are second deciders that do not share the climb's score. Clue entries C27(c), C5(a); A6, A13.

## Prediction

K4 inside its copies in all three cells on all three deciders: rank by the climb's score within the middle 90%, MIX8m and judge ranks likewise; no cell with K4 above all 100. Plants found about as D1 measured (5-7 of 8).

## Method

1. Cells: (one alphabet, Beaufort, 23), (one alphabet, Beaufort, 26), (two alphabets, 13).
2. Copies: one alphabet, shuffles of K4 that 0120's exact decider fits at that length (as 0140); two alphabets, kept-place copies (the carved letters at the 24 known places kept, the other 73 shuffled, as 0144), started from K4's witness.
3. Every text climbed with the one-run decider (RUNS_ONE runs of 0140's tempering; RUNS_TWO of 0144's), its best reading kept.
4. Deciders: the climb's quadgram score; MIX8m on the reading; the blind judge on K4's and the 100 copies' readings in one call per cell. K4's rank among its copies on each.
5. Plants: 4 clean and 4 Sanborn-style per cell, 6 own copies, through the same climb; found when above all own copies.

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
 "item": "F1.12",
 "cells": {
  "1.1-B23": {
   "runs_per_text": 1,
   "quadgram": {
    "k4": -5.11016,
    "copies_at_or_above": 68
   },
   "mix8m": {
    "k4": -419.21,
    "copies_at_or_above": 55
   },
   "judge": {
    "k4": 12,
    "copies_at_or_above": 46,
    "copies_max": 18
   },
   "k4_reading": "ZWELTFTTOLINGEDLEXAHDEASTNORTHEASTTCONDALWAYFROLHMUCANSBUFENTTHBERLINCLOCKHOSANCORGOODORBAHEAIJMP",
   "k4_known_in_place": 24,
   "plants_found": [
    7,
    8
   ],
   "plants_by_class": {
    "xstops": 2,
    "sub3": 1,
    "clean": 4,
    "k123": 1
   }
  },
  "1.1-B26": {
   "runs_per_text": 1,
   "quadgram": {
    "k4": -4.96464,
    "copies_at_or_above": 70
   },
   "mix8m": {
    "k4": -392.0,
    "copies_at_or_above": 10
   },
   "judge": {
    "k4": 12,
    "copies_at_or_above": 50,
    "copies_max": 22
   },
   "k4_reading": "QOPULLERSFAIRSEHATKMGEASTNORTHEASTARTRISKULEDHYDEEVELCOEDKIDEHEBERLINCLOCKEDNWHERTYTWEMOMODNOREQU",
   "k4_known_in_place": 24,
   "plants_found": [
    5,
    8
   ],
   "plants_by_class": {
    "xstops": 2,
    "sub3": 1,
    "clean": 4,
    "k123": 1
   }
  },
  "1.2-13": {
   "runs_per_text": 4,
   "quadgram": {
    "k4": -5.13769,
    "copies_at_or_above": 100
   },
   "mix8m": {
    "k4": -417.2,
    "copies_at_or_above": 97
   },
   "judge": {
    "k4": 8,
    "copies_at_or_above": 86,
    "copies_max": 30
   },
   "k4_reading": "CVFWARPLOTBYDICHCOMINEASTNORTHEASTISEUNINGPSONEMUPUSPACEMPLOBGMBERLINCLOCKUNDIDFIOGYMAKHISTHYFAWS",
   "k4_known_in_place": 24,
   "plants_found": [
    5,
    8
   ],
   "plants_by_class": {
    "xstops": 2,
    "sub3": 1,
    "clean": 4,
    "k123": 1
   }
  }
 },
 "k4_copies_per_cell": 100,
 "copies": "one alphabet: shuffles 0120's exact decider fits at the length (as 0140); two alphabets: kept-place copies from K4's witness (as 0144)",
 "decider": "one-run decider: 0140's tempering x 1 (one alphabet), 0144's x 4 (two alphabets); second deciders MIX8m (0233) and the blind judge",
 "judge_calls": 303,
 "judge_none": 0,
 "cells_with_k4_above_all_copies_on_some_decider": [],
 "power_reference": "0229 (L23 one run: clean 21-23/24, Sanborn-style 14-16/24; L26 11-18, 11-17), D1b (L13)",
 "compute_seconds": 732,
 "exhaustive": false,
 "modal_cost_estimate": "2 x (101 + 56) one-run climbs (about 17 s) and 157 four-run climbs (about 70 s): about 4.5 core-hours, under $1 of Modal credit (about $3.7 left after the margin); the judge 303 calls"
}
```

Notes: F1.12: 1.1-B23: K4 quadgram 68/100 at or above, MIX8m 55, judge 46 (K4 12), plants 7/8; 1.1-B26: K4 quadgram 70/100 at or above, MIX8m 10, judge 50 (K4 12), plants 5/8; 1.2-13: K4 quadgram 100/100 at or above, MIX8m 97, judge 86 (K4 8), plants 5/8


