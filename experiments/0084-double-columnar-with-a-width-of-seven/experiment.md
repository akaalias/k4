# 0084-double-columnar-with-a-width-of-seven: Two column shuffles, one of them seven columns wide in any of its 5,040 orders, with a repeating key before or after

**Family:** 6-transposition-then-tableau  
**Parent:** 0026-double-keyed-columnar-then-tableau  
**Decision:** reverted  
**Run:** 2026-10-15T16:03:22+00:00, 856.0 s, status ran  
**Time by phase:** design 125 s, implement 108 s, test 0 s, run 856 s, record 0 s

## In plain words

A column shuffle writes the message in rows under a key and reads the columns out in the key's order. Doing it twice with two keys is the classic double transposition. Five of K4's six doubled letters line up in one column when it is written in rows of seven, and the sculpture's name has seven letters, so one of the two shuffles may well be seven columns wide. Nobody has tried that combination in full. We take every possible order of seven columns, pair it with a second shuffle from the puzzle's words or a plain one, and ask whether a repeating secret word on the table could then give the copper's known letters.

## Walkthrough, by hand

1. Write the message in rows of 7 under KRYPTOS. Read the columns in the alphabetical order of the key letters, K O P R S T Y, which is columns 0, 5, 3, 1, 6, 4,
2. 2. Place 22, the E of EAST, is in row 3 of column 0, the column read first, so it becomes letter 4.
3. Write that text in rows of 5 under ABSCI (ABSCISSA with its repeated letters dropped) and read columns A B C I S, that is 0, 1, 3, 4, 2. Letter 4 is in row 0, column 3; columns 0 and 1 hold 20 letters each, so it becomes letter 41.
4. The copper at 41 is J: a repeating key on the table must turn E into J there. Work out that key letter for all 24 known letters.
5. For a key of length p, two known letters whose landing places differ by a multiple of p share a key letter; if they need different ones, p is dead.
6. Repeat for all 5,040 orders of seven columns, every second shuffle, both stage orders, the key before or after, and ten scrambled coppers.

## Worked example (generated)

```
first shuffle: rows of 7 under KRYPTOS, columns read K O P R S T Y (sequence 0 5 3 1 6 4 2);
second shuffle: rows of 5 under ABSCI (ABSCISSA, repeats dropped), columns read A B C I S (0 1 3 4 2)

place  letter  column  after KRYPTOS  after ABSCISSA  copper there
   22       E       0               4              41             J
   23       A       1              46              10             H
   24       S       2              87              38             T
   64       B       0              10              61             N
   65       E       1              52              31             G
```

## Lineage

Inherits from 0026-double-keyed-columnar-then-tableau. What changed: The public double-columnar searches stop at widths 2-6 or skip every pair with a 7 (Zekios, KryptosBot), and keithadler lists keyed double columnar as unsearched. Here one stage is a width-7 column shuffle in every one of its 5,040 orders and the other is a plain column shuffle at widths 2-30 or a column shuffle keyed by a puzzle word (repeated letters dropped, or kept with ties read left to right), in either order, with the exact crib test for a repeating key of length 1-26 on either side.

## Hypothesis (domain expert)

Type 2 of directions.md, the first open item of the prior-work database's seven-based gaps ('keyed double columnar transposition with one width of 7... KryptosBot's double-columnar run skipped every pair involving 5 or 7, its register marks width 9 x width 7 NOT covered, Zekios stopped at 6 x 6, keithadler lists keyed double columnar as unsearched'). Evidence: the width-7 doublet column (0056; about p 0.02 after conditioning on six doublets, prior-work report) and KRYPTOS's seven letters (C8(a): KRYPTOS as a transposition key for K4, as for K3); C1(a) 'double matrixes'. Route: columnar encryption (write rows, read columns in sequence) twice, one stage of width 7 in all 5,040 reading sequences, the other a plain sequence at widths 2-30 read left-to-right or right-to-left (58) or a keyword sequence from data/vocabulary.txt, K1-K3 words of 3-20 letters and the C13/C14 words, read as true keywords (columns in alphabetical order of the key letters; issue #26 found 0006-0081 read the rank list as the sequence), once with repeated letters dropped and once on the whole word with ties left to right, deduplicated; the width-7 stage first or second. Key: periodic tableau key of period 1-26 after the moves (slot = landing place mod p) or before them (slot = place mod p), 8 classes of plain and cipher alphabet and Beaufort-or-not; live if no slot holds two different forced letters. Exact; ten shuffled coppers through the identical search. Left open: both stages with free orders above width 7 (9 x 7 has 1.8 billion pairs), autokey keys with these routes.

## Prediction

No setting is live below period 20 beyond the rate on the shuffled coppers, and the count of live settings at each period 1-26 lies inside the control range, give or take the spread at 24-26. Zero candidates.

## Method

1. List the 5,040 reading sequences of seven columns and the second-stage sequences (plain 2-30, word keys both ways).
2. For each pair and each stage order, compose the two moves and skip repeats.
3. For each route, class and text, compute the key letter each known letter forces at its landing place.
4. For each period 1-26 and each key order, the period is live if no slot holds two different forced letters.
5. Count live settings per period on K4 and ten shuffled coppers.
6. List K4's live settings below period 20.

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
 "family": "double columnar, one stage width 7 in all 5,040 orders, the other plain 2-30 or word-keyed; periodic key 1-26 before or after",
 "second_stages_total": 253,
 "second_stages_done": 253,
 "stopped_for_time": false,
 "distinct_routes": 2548223,
 "duplicates_skipped": 2017,
 "periods": [
  1,
  26
 ],
 "classes": 8,
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
   0,
   3,
   32,
   72,
   3166,
   1982,
   109195
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
   3,
   1127,
   794905
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
   0,
   20,
   38,
   2462,
   1773,
   108802
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
   0,
   910,
   772021
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
   1,
   2,
   65,
   148,
   3872,
   2175,
   109485
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
   2,
   1365,
   807751
  ]
 },
 "periods_outside_control_range": {
  "A": [
   21
  ],
  "B": [
   24
  ]
 },
 "k4_live_below_20": [],
 "n_k4_live_below_20": 0,
 "controls_live_below_20": {
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
 "controls": "10 shuffled coppers (seed 84), identical search",
 "order_A": "moves, then key",
 "order_B": "key, then moves",
 "word_key_readings": "true keyword reading, repeated letters dropped, and on the whole word with ties left to right (issue #26)"
}
```

Notes: 2,548,223 distinct double-columnar routes (253 of 253 second stages x 5,040 x 2 stage orders; 2,017 repeats) x 8 classes x 2 key orders, periods 1-26. K4 live below 20: 0; controls: {'A': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'B': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}. Outside the control range: {'A': [21], 'B': [24]}.


