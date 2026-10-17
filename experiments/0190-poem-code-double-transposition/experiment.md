# 0190-poem-code-double-transposition: F11.2: the SOE poem code: a double columnar transposition keyed by consecutive words of K1-K3 and the Morse, then or before a repeating key on the sculpture's tables: exact

**Family:** 11-agency-hand-systems  
**Parent:** 0184-routes-along-the-plate-layout  
**Decision:** reverted  
**Run:** 2026-10-17T00:49:14+00:00, 4.7 s, status ran  
**Time by phase:** design 0 s, implement 0 s, test 0 s, run 5 s, record 0 s

## In plain words

British agents in the war carried their keys in their heads: a poem. They picked a few words, wrote them out, numbered the letters in alphabetical order, and used the numbers to shuffle the message twice through a grid. Here the 'poem' is the sculpture's own solved text. We try every run of a few consecutive words as the key, with a repeating secret word on the sculpture's tables before or after.

## Walkthrough, by hand

1. Take the words SHADOW FORCES from the Morse: SHADOWFORCES, 12 letters.
2. Number the letters alphabetically, ties left to right: A=1, C=2, D=3, E=4, F=5, H=6, the Os 7 and 8, R=9, the Ss 10 and 11, W=12.
3. Write the message in rows of 12, read the columns in number order; do it again.
4. Undo that, and test a repeating key on the sculpture's tables against the 24 known letters.
5. Every run of words, on K4 and on scrambled copies.

## Worked example (generated)

```
key SHADOWFORCES, column numbers [10, 6, 1, 3, 7, 12, 5, 8, 9, 2, 4, 11]
K4 with the double transposition undone: ZJPADRVTLYWOZEJAESUBCGSGXTOSUNQRTVKULIIAWFDGFJBXUTWPKLGKMKTZALUHKKSKSQUOQPSQWHRONBORBIICNTBFKFWDZ
```

## Lineage

Inherits from 0184-routes-along-the-plate-layout. What changed: F11.2. The poem code (SOE, Second World War): the agent takes words from a memorised text, writes them out as one key, numbers its letters alphabetically (ties left to right) and transposes twice by columns with that number key. Here the memorised texts are the sculpture's own: the plaintexts of K1, K2 and K3 and the Morse. Keys: every run of 1-6 consecutive words, 5-40 letters; used for both transpositions, or split into two keys at every word boundary. Each move and its inverse, then (A) or before (B) a repeating key 1-26 on 8 table classes (F6's compiled tester); K4 against 15 shuffled copies. 0167-era double columnar tests used dictionary keywords, not these phrases.

## Hypothesis (domain expert)

C5(b) ('key word/s'), A9 (agency hand systems; Scheidt's CIA background), F11; SOE poem code (Marks, Between Silk and Cyanide). Model: c = T(P2(P1(p))) or P2(P1(T(p))), P1, P2 columnar transpositions keyed by the phrase numbers, T a periodic tableau key. Statistic: 0134's fixed statistic and the shortest live period, K4 against copies.

## Prediction

No phrase key gives K4 a live period below the copies'; cells where K4 leads stay inside the copies' range. Zero candidates.

## Method

1. Word lists of K1, K2, K3 plaintexts and the Morse.
2. Every run of 1-6 consecutive words of 5-40 letters: its number key; the double columnar move with it twice, and with the run split in two at every word boundary.
3. Each move and its inverse, deduplicated.
4. F6's compiled tester: live (order, period) per text; K4 against 15 shuffled copies.

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
 "family": "SOE poem code: double columnar keyed by 1-6 consecutive words of K1-K3 and the Morse (same key twice, or split), then/before a periodic key 1-26, 8 classes, exact",
 "phrase_keys": 3063,
 "maps_after_dedupe": 6092,
 "routes": 6092,
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
   0,
   0,
   0,
   3,
   0,
   17
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
   4,
   1930
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
   0,
   0,
   1,
   0,
   17
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
   0,
   1787
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
   0,
   0,
   2,
   1,
   6,
   4,
   22
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
   5,
   1935
  ]
 },
 "k4_shortest_live": {
  "A": 24,
  "B": 25
 },
 "coppers_shortest_live": {
  "A": 22,
  "B": 25
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
  0,
  1,
  0,
  0,
  1,
  0,
  0,
  1,
  0,
  0,
  0,
  0,
  1,
  0,
  0
 ],
 "stop_queue": false,
 "copies": "15 shuffled copies (seed 1900)",
 "seconds": 5,
 "exhaustive": true
}
```

Notes: 6092 moves; shortest live K4 A 24 B 25 (copies 22, 25); K4 above every copy in 0 of 52 cells (copies 0-1)


