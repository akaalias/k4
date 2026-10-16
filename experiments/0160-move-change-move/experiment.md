# 0160-move-change-move: F6.6: move, change, move again: a grid reading or K3's rule, then a repeating key on the table, then a second move, every pair from a library of 950 moves

**Family:** 6-transposition-then-tableau  
**Parent:** 0080-key-on-both-sides-of-the-move  
**Decision:** reverted  
**Run:** 2026-10-16T22:33:01+00:00, 11.2 s, status ran  
**Time by phase:** unattributed 84 s, run 11 s, record 0 s

## In plain words

Write the message in a grid and copy it out, encipher it with a repeating secret word on the sculpture's table, then write the result in a grid again and copy it out once more. We try every pair of grid readings and K3's own counting rule as the two moves, with secret words of 1 to 26 letters, against the 24 known letters and scrambled copies of the carved text.

## Walkthrough, by hand

1. Write the 97 letters in rows of 9 and copy them out down the columns (move 1).
2. Encipher the moved text with a repeating word on the sculpture's table.
3. Write that in rows of 13 and copy it out up the columns (move 2): this is the carved text.
4. Follow each known letter: its key slot is its place after move 1, mod the word length; its carved letter is at its place after move 2.
5. Two known letters in one slot must force the same key letter. Repeat for every pair of moves and every length.

## Worked example (generated)

```
move 1: rows of 9 read down the columns; key on the table; move 2: rows of 13 read up, right first

place  letter  after move 1  slot mod 11  carved place  carved
   22       E            36            2            26       Q
   23       A            47            2            39       Q
   24       S            58            2            53       K
   64       B             8            7            42       Q
   65       E            19            7            56       D
   74       K            20            8            48       Z
```

## Lineage

Inherits from 0080-key-on-both-sides-of-the-move. What changed: F6.6 (pivot audit, issue #55, D4; directions.md type 1, 'move, change, move again'). 0080 tested key-move-key; the move-key-move sandwich was dropped after P3. Here: the message moved by M1, enciphered by a repeating key on the standard or KRYPTOS table, then moved by M2. The key's slots follow M1's places, the carved letters sit at M2(M1). Library: the four column readings (0134's) at every width 2-96 and K3's rule i -> b i mod 97 for every multiplier b, each forwards and inverted: 950 moves, every ordered pair (902,500), compiled, exact; ten scrambled coppers.

## Hypothesis (domain expert)

C1(a) and C1(c) (Sanborn, CNN 2005: 'a matrix code... double matrixes and triple matrixes... then went back to this table', knowledge/sources/cnn-2005-sanborn-interview-transcript.txt), C2(a) (K3's rule), C20(a) ('layer two'). Model: c_{M2(M1(i))} = T(p_i, k[M1(i) mod p]) for one of 8 table classes (plain and cipher alphabets standard or KRYPTOS, Beaufort or not), p 1-26. A period is live if no slot holds two different forced key letters. Statistic fixed before the run (0134's): cells (p) where K4's live count is above every copper's, against each copper's count against the rest; K4's settings live below 20 listed.

## Prediction

Nothing live below key length 20 beyond the coppers' rate; K4 above every copper in no more cells than the null's maximum. Zero candidates.

## Method

1. Build the 950 moves (where-maps).
2. For each ordered pair: the slot of each known letter (M1's place mod p) and its carved letter (at M2(M1)).
3. Compiled: per class and text, live periods 1-26; counts.
4. K4 against the coppers with the fixed statistic.

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
 "family": "move, repeating key on the standard/KRYPTOS table, move again; 950 moves (four column readings at widths 2-96, K3's rule at every multiplier; forwards and inverted), every ordered pair",
 "moves": 844,
 "pairs": 712336,
 "periods": [
  1,
  26
 ],
 "classes": 8,
 "k4_live_by_period": [
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
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
  19,
  1166,
  2856,
  43956,
  73030,
  808885
 ],
 "controls_live_by_period_min": [
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
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
  878,
  2685,
  41526,
  72762,
  802371
 ],
 "controls_live_by_period_max": [
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
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
  6,
  23,
  2537,
  2977,
  46804,
  73170,
  806802
 ],
 "k4_shortest_live": 20,
 "coppers_shortest_live": 18,
 "k4_settings_live_below_20": 0,
 "controls_settings_live_below_20": [
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  1
 ],
 "k4_live_below_20": [],
 "cells_k4_above_every_copper": [
  26
 ],
 "null_cells_above_rest_per_copper": [
  0,
  0,
  2,
  0,
  1,
  1,
  1,
  0,
  0,
  1
 ],
 "stop_queue": false,
 "seconds": 11,
 "controls": "10 shuffled coppers (seed 1606)",
 "exhaustive": true
}
```

Notes: 712,336 move pairs x 8 classes, periods 1-26: shortest live on K4 20 (coppers 18); live below 20 K4 0 (coppers 0-1); K4 above every copper in 1 of 26 cells, null 0-2; stop False


