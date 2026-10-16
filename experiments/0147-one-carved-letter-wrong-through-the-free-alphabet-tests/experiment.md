# 0147-one-carved-letter-wrong-through-the-free-alphabet-tests: F1.6: one carved letter wrong at a known place, or one letter missing or extra between the known runs, run through the exact tests for one and two unknown alphabets at every key length

**Family:** 1-keyed-periodic  
**Parent:** 0123-two-free-alphabets-exact-at-every-key-length  
**Decision:** reverted  
**Run:** 2026-10-16T20:19:48+00:00, 695.3 s, status ran  
**Time by phase:** unattributed 148 s, run 695 s, record 0 s

## In plain words

The earlier messages contain slips: a dropped letter, misspellings. If one carved letter of the fourth message is wrong, a cipher already ruled out might have been ruled out unfairly. In particular K1 and K2's own method, with a scrambled alphabet, fails only because two carved letters equal the known letters above them. We change each carved letter at the 24 known places to every other letter, and add or drop one letter between the two known words, and rerun the exact tests for one and two scrambled alphabets, on the carved text and on scrambled copies.

## Walkthrough, by hand

1. Take the carved S at place 33 and suppose Sanborn cut the wrong letter: try each of the other 25 letters there.
2. With one scrambled alphabet on both sides and the key added (K1 and K2's method), write the 24 equations: place of carved letter = place of known letter + key value of its slot.
3. A carved letter equal to its known letter forces key value 0 in its slot; with the S changed, place 33 no longer does.
4. Decide, for every key length, whether any alphabet and key satisfy all 24 equations.
5. Do the same for every other carved letter at a known place, for an added or dropped letter between the two known words, and on scrambled copies.

## Worked example (generated)

```
one alphabet on both sides, added form (K1 and K2's method): place(carved) = place(known) + key value of the slot

as carved: place 33 is S under S and place 74 is K under K, so their slots need key value 0;
at every key length 1-26 another known letter shares one of those slots and is not its own carved letter: dead.

variant: the carved S at 33 replaced by R (one slip of the chisel)
  place 33 no longer forces 0; the slot of 74 still does (K under K)
  the 24 equations are decided again at every key length, and the same for every other letter at every known place
```

## Lineage

Inherits from 0123-two-free-alphabets-exact-at-every-key-length. What changed: F1.6, first part. 0119 and 0123 decided one and two unknown alphabets with a periodic key exactly, on the copper as carved. K2 lost a letter and K1-K3 carry slips; F1.1's added form (K1 and K2's own system) dies only because S sits under S at 33 and K under K at 74. Here every single-letter error the exact tests can see is tried: each of the 24 carved letters at the known places replaced by each of the other 25 letters (600), and one letter missing or extra between the two known runs (4, the shift read on either side; an error before EAST or after CLOCK shifts every known place together and changes no periodic check, so it is the copper as carved). For each variant: one free alphabet, added and Beaufort forms, and two free alphabets, key lengths 1-26, decided exactly. Ten scrambled coppers get the same 604 variants.

## Hypothesis (domain expert)

C17(a)/(b) and family G (knowledge/06-hypotheses.md: 'every family should be tested once more with one letter inserted or deleted at each position'), C27(c), C1(b); Scheidt 2005 (knowledge/sources/wired-2005-zetter-questions-for-kryptos-creator.txt): 'since he's the one who had the chisel in his hands, there could be some changes'. Models: 0119's one unknown bijection on both sides, added form x(c) = x(p) + k or Beaufort x(c) = k - x(p); 0123's two bijections C(c) = P(p) + k. Deciders: 0119's (CRT mod 13 and 2, exhaustive mod-13 enumeration) and 0123's, witness re-checked; node limit 20,000 for the two-alphabet search, undecided cases counted. Statistic fixed before the run: per model and length, the number of variants that fit; cells where K4's count is above every copper's, against each copper's count against the rest. Also reported: every variant that revives the added form on K4.

## Prediction

Changing the carved letter at 33 or 74 revives the added form at some lengths (it removes the self-encryption that kills it), on K4 as on the coppers' corresponding variants; overall fit counts per (model, length) sit inside the coppers' range, K4 above every copper in no more cells than the null's maximum. No reading; any revived cell joins F1.5's undecided cells for the English decider.

## Method

1. Build the 604 variants of K4 (and of each of 10 coppers): substitution at each known place, and the known runs pulled together or pushed apart by one.
2. For each variant, model and key length 1-26: the 24 equations, decided exactly.
3. Count fitting variants per (model, length) per text; compare K4 with the coppers; list K4's added-form fits.

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
 "family": "one carved letter wrong at a known place (600) or one letter missing/extra between the runs (4: two readings each), through the exact one- and two-free-alphabet periodic tests",
 "models": {
  "1V": "one alphabet, added form (Quagmire III, K1/K2's system)",
  "1B": "one alphabet, Beaufort form",
  "2": "two alphabets (Quagmire IV)"
 },
 "variants_per_text": 604,
 "key_lengths": [
  1,
  26
 ],
 "k4_fitting_variants_by_length": {
  "1V": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   2,
   0,
   0,
   0,
   0,
   25,
   1,
   2,
   1,
   26,
   27,
   2,
   28
  ],
  "1B": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   1,
   27,
   0,
   91,
   25,
   24,
   0,
   0,
   573,
   27,
   52,
   601
  ],
  "2": [
   0,
   0,
   0,
   0,
   0,
   1,
   0,
   534,
   0,
   52,
   94,
   100,
   573,
   3,
   1,
   586,
   1,
   100,
   536,
   578,
   3,
   97,
   588,
   594,
   54,
   602
  ]
 },
 "controls_min_by_length": {
  "1V": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   26,
   28
  ],
  "1B": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   1,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   27,
   27,
   27
  ],
  "2": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   1,
   2,
   2,
   51,
   2,
   51,
   2,
   2,
   1,
   2,
   51,
   1,
   53,
   54,
   598,
   602
  ]
 },
 "controls_max_by_length": {
  "1V": [
   0,
   0,
   0,
   0,
   0,
   36,
   295,
   23,
   0,
   505,
   534,
   542,
   552,
   553,
   26,
   571,
   3,
   577,
   23,
   551,
   553,
   565,
   577,
   584,
   593,
   601
  ],
  "1B": [
   0,
   0,
   0,
   0,
   0,
   1,
   17,
   1,
   0,
   62,
   45,
   538,
   552,
   548,
   26,
   573,
   4,
   576,
   510,
   550,
   548,
   565,
   577,
   586,
   593,
   601
  ],
  "2": [
   0,
   0,
   0,
   0,
   0,
   496,
   526,
   540,
   0,
   562,
   572,
   572,
   579,
   577,
   52,
   588,
   4,
   590,
   534,
   580,
   577,
   584,
   589,
   594,
   598,
   602
  ]
 },
 "undecided": {
  "k4": {
   "1V": 0,
   "1B": 0,
   "2": 8
  },
  "controls": [
   {
    "1V": 0,
    "1B": 0,
    "2": 2
   },
   {
    "1V": 0,
    "1B": 0,
    "2": 6
   },
   {
    "1V": 0,
    "1B": 0,
    "2": 0
   },
   {
    "1V": 0,
    "1B": 0,
    "2": 1
   },
   {
    "1V": 0,
    "1B": 11,
    "2": 0
   },
   {
    "1V": 1,
    "1B": 0,
    "2": 1
   },
   {
    "1V": 0,
    "1B": 0,
    "2": 1
   },
   {
    "1V": 0,
    "1B": 0,
    "2": 1
   },
   {
    "1V": 0,
    "1B": 0,
    "2": 8
   },
   {
    "1V": 0,
    "1B": 2,
    "2": 2
   }
  ]
 },
 "k4_added_form_fits": [
  {
   "variant": "sub 22 F->E",
   "length": 26
  },
  {
   "variant": "sub 26 Q->N",
   "length": 24
  },
  {
   "variant": "sub 28 P->R",
   "length": 23
  },
  {
   "variant": "sub 33 S->A",
   "length": 19
  },
  {
   "variant": "sub 33 S->B",
   "length": 19
  },
  {
   "variant": "sub 33 S->C",
   "length": 19
  },
  {
   "variant": "sub 33 S->D",
   "length": 19
  },
  {
   "variant": "sub 33 S->E",
   "length": 19
  },
  {
   "variant": "sub 33 S->F",
   "length": 19
  },
  {
   "variant": "sub 33 S->G",
   "length": 19
  },
  {
   "variant": "sub 33 S->H",
   "length": 19
  },
  {
   "variant": "sub 33 S->I",
   "length": 19
  },
  {
   "variant": "sub 33 S->J",
   "length": 19
  },
  {
   "variant": "sub 33 S->K",
   "length": 19
  },
  {
   "variant": "sub 33 S->L",
   "length": 19
  },
  {
   "variant": "sub 33 S->M",
   "length": 19
  },
  {
   "variant": "sub 33 S->N",
   "length": 19
  },
  {
   "variant": "sub 33 S->O",
   "length": 19
  },
  {
   "variant": "sub 33 S->P",
   "length": 19
  },
  {
   "variant": "sub 33 S->Q",
   "length": 19
  },
  {
   "variant": "sub 33 S->R",
   "length": 19
  },
  {
   "variant": "sub 33 S->T",
   "length": 19
  },
  {
   "variant": "sub 33 S->U",
   "length": 19
  },
  {
   "variant": "sub 33 S->V",
   "length": 19
  },
  {
   "variant": "sub 33 S->W",
   "length": 19
  },
  {
   "variant": "sub 33 S->X",
   "length": 19
  },
  {
   "variant": "sub 33 S->Y",
   "length": 19
  },
  {
   "variant": "sub 71 Z->L",
   "length": 19
  },
  {
   "variant": "sub 74 K->A",
   "length": 23
  },
  {
   "variant": "sub 74 K->A",
   "length": 24
  },
  {
   "variant": "sub 74 K->A",
   "length": 26
  },
  {
   "variant": "sub 74 K->B",
   "length": 23
  },
  {
   "variant": "sub 74 K->B",
   "length": 24
  },
  {
   "variant": "sub 74 K->B",
   "length": 26
  },
  {
   "variant": "sub 74 K->C",
   "length": 23
  },
  {
   "variant": "sub 74 K->C",
   "length": 24
  },
  {
   "variant": "sub 74 K->C",
   "length": 26
  },
  {
   "variant": "sub 74 K->D",
   "length": 23
  },
  {
   "variant": "sub 74 K->D",
   "length": 24
  },
  {
   "variant": "sub 74 K->D",
   "length": 26
  },
  {
   "variant": "sub 74 K->E",
   "length": 23
  },
  {
   "variant": "sub 74 K->E",
   "length": 24
  },
  {
   "variant": "sub 74 K->E",
   "length": 26
  },
  {
   "variant": "sub 74 K->F",
   "length": 23
  },
  {
   "variant": "sub 74 K->F",
   "length": 24
  },
  {
   "variant": "sub 74 K->G",
   "length": 23
  },
  {
   "variant": "sub 74 K->G",
   "length": 24
  },
  {
   "variant": "sub 74 K->G",
   "length": 26
  },
  {
   "variant": "sub 74 K->H",
   "length": 23
  },
  {
   "variant": "sub 74 K->H",
   "length": 24
  },
  {
   "variant": "sub 74 K->H",
   "length": 26
  },
  {
   "variant": "sub 74 K->I",
   "length": 23
  },
  {
   "variant": "sub 74 K->I",
   "length": 24
  },
  {
   "variant": "sub 74 K->I",
   "length": 26
  },
  {
   "variant": "sub 74 K->J",
   "length": 23
  },
  {
   "variant": "sub 74 K->J",
   "length": 24
  },
  {
   "variant": "sub 74 K->J",
   "length": 26
  },
  {
   "variant": "sub 74 K->L",
   "length": 23
  },
  {
   "variant": "sub 74 K->L",
   "length": 24
  },
  {
   "variant": "sub 74 K->L",
   "length": 26
  },
  {
   "variant": "sub 74 K->M",
   "length": 23
  },
  {
   "variant": "sub 74 K->M",
   "length": 24
  },
  {
   "variant": "sub 74 K->M",
   "length": 26
  },
  {
   "variant": "sub 74 K->N",
   "length": 23
  },
  {
   "variant": "sub 74 K->N",
   "length": 24
  },
  {
   "variant": "sub 74 K->N",
   "length": 26
  },
  {
   "variant": "sub 74 K->O",
   "length": 23
  },
  {
   "variant": "sub 74 K->O",
   "length": 24
  },
  {
   "variant": "sub 74 K->O",
   "length": 26
  },
  {
   "variant": "sub 74 K->P",
   "length": 24
  },
  {
   "variant": "sub 74 K->P",
   "length": 26
  },
  {
   "variant": "sub 74 K->Q",
   "length": 23
  },
  {
   "variant": "sub 74 K->Q",
   "length": 26
  },
  {
   "variant": "sub 74 K->R",
   "length": 23
  },
  {
   "variant": "sub 74 K->R",
   "length": 24
  },
  {
   "variant": "sub 74 K->R",
   "length": 26
  },
  {
   "variant": "sub 74 K->S",
   "length": 23
  },
  {
   "variant": "sub 74 K->S",
   "length": 24
  },
  {
   "variant": "sub 74 K->S",
   "length": 26
  },
  {
   "variant": "sub 74 K->T",
   "length": 23
  },
  {
   "variant": "sub 74 K->T",
   "length": 24
  },
  {
   "variant": "sub 74 K->T",
   "length": 26
  },
  {
   "variant": "sub 74 K->U",
   "length": 23
  },
  {
   "variant": "sub 74 K->U",
   "length": 24
  },
  {
   "variant": "sub 74 K->U",
   "length": 26
  },
  {
   "variant": "sub 74 K->V",
   "length": 23
  },
  {
   "variant": "sub 74 K->V",
   "length": 24
  },
  {
   "variant": "sub 74 K->V",
   "length": 26
  },
  {
   "variant": "sub 74 K->W",
   "length": 23
  },
  {
   "variant": "sub 74 K->W",
   "length": 24
  },
  {
   "variant": "sub 74 K->W",
   "length": 26
  },
  {
   "variant": "sub 74 K->X",
   "length": 23
  },
  {
   "variant": "sub 74 K->X",
   "length": 24
  },
  {
   "variant": "sub 74 K->X",
   "length": 26
  },
  {
   "variant": "sub 74 K->Y",
   "length": 23
  },
  {
   "variant": "sub 74 K->Y",
   "length": 24
  },
  {
   "variant": "sub 74 K->Y",
   "length": 26
  },
  {
   "variant": "sub 74 K->Z",
   "length": 23
  },
  {
   "variant": "sub 74 K->Z",
   "length": 24
  },
  {
   "variant": "sub 74 K->Z",
   "length": 26
  },
  {
   "variant": "one letter extra between the runs (places as typed, carved letters moved)",
   "length": 22
  },
  {
   "variant": "one letter extra between the runs (places as typed, carved letters moved)",
   "length": 24
  },
  {
   "variant": "one letter extra between the runs (places as typed, carved letters moved)",
   "length": 25
  },
  {
   "variant": "one letter extra between the runs (places as typed, carved letters moved)",
   "length": 26
  },
  {
   "variant": "one letter extra between the runs (carved letters fixed, places moved)",
   "length": 14
  },
  {
   "variant": "one letter extra between the runs (carved letters fixed, places moved)",
   "length": 21
  },
  {
   "variant": "one letter missing between the runs (places as typed, carved letters moved)",
   "length": 14
  },
  {
   "variant": "one letter missing between the runs (places as typed, carved letters moved)",
   "length": 21
  },
  {
   "variant": "one letter missing between the runs (places as typed, carved letters moved)",
   "length": 23
  },
  {
   "variant": "one letter missing between the runs (places as typed, carved letters moved)",
   "length": 24
  },
  {
   "variant": "one letter missing between the runs (places as typed, carved letters moved)",
   "length": 25
  },
  {
   "variant": "one letter missing between the runs (places as typed, carved letters moved)",
   "length": 26
  },
  {
   "variant": "one letter missing between the runs (carved letters fixed, places moved)",
   "length": 20
  },
  {
   "variant": "one letter missing between the runs (carved letters fixed, places moved)",
   "length": 26
  }
 ],
 "k4_added_form_fit_count": 114,
 "cells_k4_above_every_copper": [
  "1V:19",
  "2:19"
 ],
 "null_cells_above_rest_per_copper": [
  0,
  9,
  3,
  2,
  4,
  11,
  6,
  0,
  6,
  3
 ],
 "stop_queue": false,
 "indel_note": "an error before place 22 or after 74 shifts every known place together and changes no periodic check",
 "controls": "10 shuffled coppers (seed 146), the same 604 variants each",
 "exhaustive": "exact per (variant, model, length); undecided counted"
}
```

Notes: K4 fitting (variant, length) pairs: {'1V': 114, '1B': 1421, '2': 5097}; added form revived on K4 in 114 pairs; K4 above every copper in 2 of 78 cells, null 0-11; stop False; undecided K4 {'1V': 0, '1B': 0, '2': 8}


