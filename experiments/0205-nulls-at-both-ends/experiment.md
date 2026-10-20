# 0205-nulls-at-both-ends: F2.4: a run of nulls at both ends of the message (SOE's Dutch section), the known letters moved by the start run, then a periodic or progressive key on the table, exact, with planted texts

**Family:** 2-masked-then-keyed  
**Parent:** 0023-masks-reversal-and-nulls-then-tableau  
**Decision:** reverted  
**Run:** 2026-10-20T11:10:30+00:00, 5.6 s, status ran  
**Time by phase:** test 1 s, run 6 s, record 0 s

## In plain words

Wartime agents sometimes put a handful of meaningless letters before and after a message, so the real words do not start where an enemy expects. If Sanborn did that, the known words sit a few places further along the copper than in the message. We slide them along by 0 to 12 places and test every repeating or steadily sliding secret word on the sculpture's table.

## Walkthrough, by hand

1. Put eight random letters before the message and some after it.
2. Encipher the whole on the table with a key word that slides one step along the table after each full pass.
3. To test: slide the known words eight places along the copper.
4. At each, the table gives the key value; take away the slide for that pass.
5. Known letters in the same slot of the key word must then agree.

## Worked example (generated)

```
start run of 8 nulls: the known words sit 8 places later on the copper; KRYPTOS table, added form

place  known  carved place  carved  key value
   22      E            30       N          8
   23      A            31       G          6
   24      S            32       K         20
   25      T            33       S          2
   26      N            34       S         13
   27      O            35       O          0
```

## Lineage

Inherits from 0023-masks-reversal-and-nulls-then-tableau. What changed: F2.4 (issue #78): SOE's Dutch section put eight random letters at the beginning and at the end of each message (Marks p. 232). If K4's message is padded so, the known words sit s places later on the copper than in the message. The end run only shortens the message (s + e <= 23 keeps BERLINCLOCK inside); it moves nothing, so every pair of runs 0-12 reduces to the start run s. A key that starts with the message or with the copper is the same family (the offset is absorbed by the key word, for periodic and both progressive forms). 0023 tested start runs 1-24 with periodic keys; new here: the progressive key, per letter and per repeat, steps 1-25, lengths 1-52, on the 8 standard/KRYPTOS table classes, for s = 0-12, with periodic keys (step 0) rerun alongside, on K4, ten scrambled copies and planted texts.

## Hypothesis (domain expert)

C4(a) (a mask that pads the plaintext), C17(b) (the working text longer than 97). Source: reports/marks-between-silk-and-cyanide.md. Model: carved = nulls(s) + T(message) + nulls(e), message positions of the known letters 22-34, 64-74 (Sanborn's numbering of the message), so carved places q + s; T a tableau key with value w[i mod L] + d i (per letter) or w[i mod L] + d floor(i/L) (per repeat), d 0-25, L 1-52, plain and cipher alphabets standard or KRYPTOS, added or Beaufort form (8 classes; the variant form is the added form with -w). Exact by slot agreement of the 24 forced values after removing the step. Statistic (fixed): per form, the shortest consistent length over all s and steps on K4 against the copies, and the cells (form, length) where K4's count of live (s, step, class) settings exceeds every copy's.

## Prediction

For every start run, nothing consistent below length 24-26 with a periodic key (as 0023), and the progressive forms at the copies' rate; K4 above every copy in no more cells than a copy is. Planted texts found at their own setting. Zero candidates.

## Method

1. For each start run s = 0-12 and table class, the forced key value at each known letter, read at carved place q + s.
2. For each form and step d, remove d i or d floor(i/L) and test slot agreement for every length L.
3. Count live settings per (form, length) on K4, ten copies and two planted texts; the fixed statistic.

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
 "family": "nulls at both ends (start run s 0-12; the end run moves nothing), then a periodic or progressive key on the standard/KRYPTOS tables",
 "start_runs": "0-12",
 "end_runs": "0-12 (any; s + e <= 23)",
 "classes": [
  "std/std/vig-var",
  "std/std/beau",
  "std/kry/vig-var",
  "std/kry/beau",
  "kry/std/vig-var",
  "kry/std/beau",
  "kry/kry/vig-var",
  "kry/kry/beau"
 ],
 "forms": {
  "periodic": "step 0",
  "per-letter": "w[i mod L] + d i, d 1-25",
  "per-repeat": "w[i mod L] + d floor(i/L), d 1-25"
 },
 "lengths": "1-52",
 "per_form": {
  "periodic": {
   "k4_live_by_length": [
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
    0,
    5,
    104,
    104,
    104,
    5,
    1,
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
    5
   ],
   "copies_live_by_length_max": [
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
    0,
    8,
    104,
    104,
    104,
    9,
    1,
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
    1,
    8
   ],
   "k4_shortest": 26,
   "copies_shortest": [
    26,
    26,
    26,
    26,
    26,
    26,
    26,
    26,
    26,
    26
   ],
   "k4_above_every_copy": [],
   "copy_cells_above_rest": [
    0,
    0,
    0,
    2,
    0,
    0,
    0,
    0,
    1,
    0
   ]
  },
  "per-letter": {
   "k4_live_by_length": [
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
    0,
    125,
    2600,
    2600,
    2600,
    107,
    5,
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
    5,
    125
   ],
   "copies_live_by_length_max": [
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
    0,
    200,
    2600,
    2600,
    2600,
    132,
    6,
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
    6,
    200
   ],
   "k4_shortest": 26,
   "copies_shortest": [
    26,
    26,
    26,
    26,
    26,
    26,
    26,
    26,
    26,
    26
   ],
   "k4_above_every_copy": [],
   "copy_cells_above_rest": [
    0,
    0,
    0,
    2,
    1,
    0,
    0,
    0,
    0,
    0
   ]
  },
  "per-repeat": {
   "k4_live_by_length": [
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
    0,
    99,
    2600,
    2600,
    2600,
    99,
    5,
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
    5,
    99
   ],
   "copies_live_by_length_max": [
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
    0,
    102,
    2600,
    2600,
    2600,
    102,
    6,
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
    1,
    6,
    102
   ],
   "k4_shortest": 26,
   "copies_shortest": [
    26,
    26,
    26,
    26,
    26,
    26,
    26,
    26,
    26,
    26
   ],
   "k4_above_every_copy": [],
   "copy_cells_above_rest": [
    0,
    0,
    0,
    1,
    0,
    0,
    0,
    0,
    0,
    0
   ]
  }
 },
 "k4_settings_below_24": [],
 "k4_cells_above_every_copy": 0,
 "copy_cells_above_rest": [
  0,
  0,
  0,
  5,
  1,
  0,
  0,
  0,
  1,
  0
 ],
 "stop_queue": false,
 "plants": [
  {
   "s": 8,
   "e": 8,
   "class": "std/kry/beau",
   "form": "per-repeat",
   "step": 3,
   "length": 9,
   "found": true,
   "shortest_found": 9,
   "other_settings_below_24": 5
  },
  {
   "s": 5,
   "e": 11,
   "class": "kry/kry/vig-var",
   "form": "per-letter",
   "step": 7,
   "length": 11,
   "found": true,
   "shortest_found": 11,
   "other_settings_below_24": 5
  }
 ],
 "controls": "10 shuffled copies (seed 2400)",
 "seconds": 5,
 "exhaustive": "yes"
}
```

Notes: Shortest live length K4 / copies: periodic 26 / 26; per-letter 26 / 26; per-repeat 26 / 26. K4 above every copy in 0 cells, copies 0-5. Plants: per-repeat found True (shortest 9), per-letter found True (shortest 11)


