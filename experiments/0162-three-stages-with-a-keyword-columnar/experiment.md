# 0162-three-stages-with-a-keyword-columnar: F6.8: three-stage routes with at least one keyword columnar stage (puzzle and K1-K3 words), the others any of the four column readings at widths 2-24, then or before a repeating key on the table

**Family:** 6-transposition-then-tableau  
**Parent:** 0134-mixed-matrix-readings-two-and-three-stages  
**Decision:** reverted  
**Run:** 2026-10-16T22:38:47+00:00, 39.8 s, status ran  
**Time by phase:** unattributed 132 s, run 40 s, record 0 s

## In plain words

Sanborn spoke of double and triple matrixes, and K3 was moved by a grid keyed by the word KRYPTOS. Here the letters go through three grids, at least one of them keyed by a word from the puzzle or the earlier messages, the others read in any of the four plain ways, then a repeating secret word on the sculpture's table, tested against the 24 known letters and scrambled copies.

## Walkthrough, by hand

1. Write the message in rows of 7 under KRYPTOS and read the columns in the order of its letters: K, O, P, R, S, T, Y.
2. Write the result in rows of 11 and read the columns left to right, top to bottom.
3. Write that in rows of 9 and read up the columns (a quarter turn).
4. Note where each known letter lands; with a repeating key of length p on the table, known letters a multiple of p apart must force the same key letter.
5. Repeat for every word, reading and width, the key before or after, and on scrambled copies.

## Worked example (generated)

```
KRYPTOS-keyed columnar (columns K O P R S T Y), then rows of 11 read down, then rows of 9 turned

place  letter  after 1  after 2  after 3  carved
   22       E        4       28        8       O
   23       A       46       14       54       L
   24       S       87       89       78       K
   64       B       10       82        2       B
   65       E       52       68       48       Z
   74       K       39       49       39       Q
```

## Lineage

Inherits from 0134-mixed-matrix-readings-two-and-three-stages. What changed: F6.8 (pivot audit, issue #55, D6). 0037 sampled three-stage routes with keyed columnar stages (15 percent); 0083 and 0134 enumerated triples of plain readings only. Here every triple of stages in which at least one stage is a keyword columnar transposition (true key order, columns read top to bottom, 0085's reading) keyed by a puzzle word or a K1-K3 plaintext word, and the other stages are keyword stages or any of the four column readings at widths 2-24: about 24 million triples, forward and inverse, deduplicated, compiled; then a repeating key 1-26 on the standard or KRYPTOS table after or before. Ten scrambled coppers.

## Hypothesis (domain expert)

C1(a) ('double matrixes and triple matrixes', CNN 2005, knowledge/sources/cnn-2005-sanborn-interview-transcript.txt), C8(a) (KRYPTOS as K3's column key), C7(a) (K1-K3 words as keys). Keyword columnar: write in rows of len(word), number the columns by the word's letters in alphabetical order (ties left to right), read the columns in that order top to bottom. Words: 0115's puzzle list (vocabulary, K1-K3 plaintext words, theme words) of length 2-24 with at least two distinct letters. Plain readings: cw, ccw, col, colr at widths 2-24 (0134's). Periodic key: order A (after) or B (before), 8 classes, period live if no slot holds two different forced key letters. Statistic fixed before the run (0134's).

## Prediction

Nothing live below key length 20 beyond the coppers' rate; K4 above every copper in no more cells than the null's maximum. Zero candidates.

## Method

1. Stage maps: 92 plain readings (four readings x widths 2-24) and one keyword columnar per word.
2. Compiled: every triple with at least one keyword stage, composed, forward and inverse, deduplicated within each first stage.
3. Live periods 1-26 per order, class and text; counts; the fixed statistic.

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
 "family": "three stages with at least one keyword columnar (puzzle and K1-K3 words), others plain readings at widths 2-24, then or before a periodic key",
 "stages": 223,
 "keyword_stages": 131,
 "first_stages_done": 223,
 "first_stages_total": 223,
 "distinct_routes": 20370476,
 "duplicates_skipped": 251282,
 "k4_live_by_period": {
  "A": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
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
   14,
   152,
   1116,
   21696,
   17613,
   59181
  ],
  "B": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   14,
   9279,
   6272964
  ]
 },
 "controls_live_by_period_min": {
  "A": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   7,
   129,
   990,
   19812,
   17071,
   58362
  ],
  "B": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   7,
   8951,
   6263398
  ]
 },
 "controls_live_by_period_max": {
  "A": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
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
   27,
   220,
   1261,
   22279,
   18355,
   59210
  ],
  "B": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   21,
   9355,
   6281513
  ]
 },
 "k4_shortest_live": {
  "A": 20,
  "B": 24
 },
 "coppers_shortest_live": {
  "A": 20,
  "B": 24
 },
 "k4_settings_live_below_20": {
  "A": 0,
  "B": 0
 },
 "controls_settings_live_below_20": {
  "A": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  "B": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ]
 },
 "k4_live_below_20": [],
 "cells_k4_above_every_copper": [],
 "null_cells_above_rest_per_copper": [
  2,
  0,
  1,
  0,
  1,
  1,
  2,
  1,
  2,
  0
 ],
 "stop_queue": false,
 "seconds": 40,
 "controls": "10 shuffled coppers (seed 1608)",
 "exhaustive": "exact for every first stage done"
}
```

Notes: 20,370,476 routes (223 of 223 first stages): shortest live K4 A 20, B 24 (coppers 20, 24); K4 above every copper in 0 of 52 cells, null 0-2


