# 0155-progressive-keys-on-dictionary-tables: F1.9: progressive keys, per-letter and per-repeat, every step and period 1-52, on the standard, KRYPTOS and every dictionary keyword table, against scrambled copies (Kryha's step of 3 included)

**Family:** 1-keyed-periodic  
**Parent:** 0042-progressive-key-on-vocabulary-alphabets  
**Decision:** reverted  
**Run:** 2026-10-16T22:17:04+00:00, 385.5 s, status ran  
**Time by phase:** unattributed 24 s, run 386 s, record 0 s

## In plain words

In a progressive key the secret word slides along the table by a fixed step, either after every letter or after every full pass of the word, the way some cipher machines stepped. We try every step and word length up to 52 on the sculpture's tables and on tables built from every dictionary word, and check against the 24 known letters and scrambled copies of the carved text.

## Walkthrough, by hand

1. Take a key word of length 7 and a step of 3 per letter: the key at place i is the word's letter at i mod 7 plus 3 i.
2. On the table, the known letter and the carved letter at each known place fix the key value there.
3. Subtract 3 times the place: what is left must be the same for all known places in one slot (i mod 7).
4. Per repeat instead: subtract 3 times the number of completed passes of the word.
5. Repeat for every step, length, table and form, and on scrambled copies.

## Worked example (generated)

```
sculpture's table, Vigenere: key value forced at each known place, then minus 3 x place (per-letter step 3), slot = place mod 7

place  key value  minus 3i  slot
   22          1        16     0
   23         10        22     1
   29         23        17     0
   30          5        22     1
   64         11         4     0
   71          8         6     0
places 22 and 29 share slot 0 and must leave the same value
```

## Lineage

Inherits from 0042-progressive-key-on-vocabulary-alphabets. What changed: F1.9. 0011 tested the progressive key (per-repeat and per-letter) on the standard and KRYPTOS tables and 0042 the per-repeat form on vocabulary tables; the per-letter form on keyword tables, the surviving periods 26-30 against copies, and Kryha's machine stepping (3 per cycle) at periods 31-52 were open. Here both forms, steps 1-25, periods 1-52, on 0109's tables: every dictionary word of four letters or more as a keyword alphabet (plain side, cipher side or both, the other side standard or KRYPTOS), plus the 8 standard/KRYPTOS tables, added and Beaufort forms; the consistency test is compiled C. Ten scrambled copies.

## Hypothesis (domain expert)

C5(a), C20 (hand schedules); TM 32-220 par. 125 (progressive key) and Lewis, German Agent Systems (Kryha stepping, net step 3 per revolution), per research_notes/Scheidt patents and field ciphers/addendum_downloaded_manuals.md. Model: key value at message place i = w[i mod L] + s i (per-letter) or w[i mod L] + s floor(i / L) (per-repeat, 'step per cycle'), w free letters, s 1-25 (the variant form is the added form with -s). Forced key values at the 24 known places; period L consistent for (table, s, form) if each slot holds one value of K - progression. Statistic fixed before the run: per (form, period), K4's count of consistent (table, step) pairs against the ten coppers' range; cells where K4 is above every copper against each copper's count against the rest; smallest consistent period.

## Prediction

Short periods die for both forms on every table; at 26 and above some survive on K4 at the coppers' rate; K4 above every copper in no more cells than the null's maximum. Zero candidates.

## Method

1. Build the keyword tables (0109's).
2. For each text, table and form: the 24 forced key values.
3. Compiled: for each step 1-25 and period 1-52, per-letter and per-repeat, test slot consistency; count.
4. Compare K4 with the coppers cell by cell.

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
 "family": "progressive key, per-letter and per-repeat, steps 1-25, periods 1-52, on 0109's dictionary keyword tables plus standard/KRYPTOS",
 "tables": 1040314,
 "forms_per_table": [
  "added",
  "Beaufort"
 ],
 "steps": [
  1,
  25
 ],
 "periods": [
  1,
  52
 ],
 "k4_live_by_period": {
  "letter": [
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
   2348,
   1701275,
   52015700,
   52015700,
   52015700,
   1955461,
   64916,
   2828,
   99,
   40,
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
   64,
   2348,
   69840,
   1701275
  ],
  "repeat": [
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
   2348,
   1883001,
   52015700,
   52015700,
   52015700,
   1968045,
   64916,
   4217,
   99,
   20,
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
   1,
   64,
   2143,
   69840,
   2012577
  ]
 },
 "controls_min_by_period": {
  "letter": [
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
   1602,
   364425,
   52015700,
   52015700,
   52015700,
   1609951,
   69089,
   2187,
   45,
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
   64,
   1602,
   64574,
   364425
  ],
  "repeat": [
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
   1602,
   1946095,
   52015700,
   52015700,
   52015700,
   1972127,
   69089,
   2086,
   45,
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
   64,
   1632,
   64574,
   1964935
  ]
 },
 "controls_max_by_period": {
  "letter": [
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
   6,
   7239,
   2892325,
   52015700,
   52015700,
   52015700,
   2052840,
   96894,
   5324,
   366,
   10,
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
   6,
   662,
   7239,
   94938,
   2892325
  ],
  "repeat": [
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
   6,
   7239,
   2096083,
   52015700,
   52015700,
   52015700,
   2036692,
   96894,
   6268,
   366,
   7,
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
   8,
   662,
   7181,
   94938,
   2066051
  ]
 },
 "k4_shortest_live": {
  "letter": 25,
  "repeat": 25
 },
 "coppers_shortest_live": {
  "letter": 24,
  "repeat": 24
 },
 "cells_k4_above_every_copper": [
  "letter:34",
  "letter:47",
  "repeat:34",
  "repeat:47"
 ],
 "null_cells_above_rest_per_copper": [
  1,
  3,
  0,
  0,
  4,
  5,
  4,
  0,
  0,
  4
 ],
 "stop_queue": false,
 "kryha_note": "step 3 per repeat at 31-52 is inside the per-repeat counts (all steps summed)",
 "controls": "10 shuffled coppers (seed 1590)",
 "exhaustive": true
}
```

Notes: 1,040,314 tables x 2 forms x 25 steps: shortest live period on K4 per-letter 25, per-repeat 25 (coppers 24, 24); K4 above every copper in 4 of 104 cells, null 0-5; stop False


