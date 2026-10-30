# 0260-f13-what-carries-the-b2-excess-rotations-reversal-blocks: F13.4i: what carries K4's B2 excess? K4's 96 cyclic rotations, its reversal and 300 block-shuffled versions through 0238's search, against 500 fresh shuffles; planted messages rotated the same way

**Family:** 13-ciphertext-only  
**Parent:** 0259-f13-chase-the-table-then-move-excess-width-19  
**Decision:** reverted  
**Run:** 2026-10-30T06:41:30+00:00, 69.6 s, status ran  
**Time by phase:** test 10 s, run 70 s, record 0 s

## In plain words

K4 reads a little more like English than almost any scrambled copy of it under one particular two-step cipher, though the reading itself is gibberish. Is that because of where K4's letters are, which a hidden message would explain, or because of which letters sit next to each other, which a message would not need? We slide K4 around in a circle (every letter keeps its neighbours but changes its place), flip it, and chop it into pieces we shuffle, and see which versions keep the effect. A hidden test message treated the same way should lose it.

## Walkthrough, by hand

1. Write K4 around a circle and start reading it one place later: OBKRU... becomes BKRUO...O.
2. Every letter keeps its neighbours, but every letter has moved one place.
3. Run the same search on this rotated text and compare its score with 500 scrambled copies of K
4. 4. Repeat for all 96 rotations, for K4 read backwards, and for K4 cut into pieces whose order is shuffled.
5. If the rotations score as high as K4, the effect comes from which letters sit together, not from a message written at exact places.

## Worked example (generated)

```
F13.4i: rotate K4 and see whether its B2 excess survives.

  K4         OBKRUOXOGHULBSOLIFBBWFLRVQQPRN...
  rotated 1  BKRUOXOGHULBSOLIFBBWFLRVQQPRNG...
  reversed   RACKEUAUHUKGIDCJTXZKDGWKPFZMTT...

  each through the same search (the table with a two-letter key, then any of 27,852 moves),
  each scored against 500 scrambled copies of K4. A message at exact places loses its excess when rotated.
```

## Lineage

Inherits from 0259-f13-chase-the-table-then-move-excess-width-19. What changed: F13.4i (Alexis, #101: chase it). 0259 replicated K4's excess at B2 (the sculpture's table with a two-letter key, then a move) against 1,000 fresh shuffles, p 0.002, and showed it does not need width-19 moves (p 0.004 without them). Here the question is what in K4 carries it. A cyclic rotation keeps every adjacency of the carved letters (the width-7 doublet column and the width-21 repeats move together) but changes every place; the reversal keeps adjacency mirrored; cutting K4 into blocks of 4, 7 or 12 and shuffling the blocks keeps structure inside a block only. A planted B2 message is rotated the same way as a positive control: its excess should vanish when rotated.

## Hypothesis (domain expert)

F13.4d/h: order B (periodic tableau key of length 2 on the sculpture's 8 table classes, then one of 0129's 27,852 moves), ciphertext only, 0238's frequency screen, climb and MIX8m rescoring. If K4's B2 excess comes from local structure of the carved letters that any arrangement of them by blocks keeps (letters that sit well together), rotations and large-block shuffles stay extreme; if it comes from a message enciphered at these exact places, only K4 in its own order is extreme, as only the unrotated plant is. Pre-registered: share of rotations above the shuffles' 95th percentile at B2 at least 0.5 means a position-free property (the excess carries no reading, F13.4h closed as a property of the carved letters); at most 0.1 means positional, and the reading is chased (judge, known words on the intermediate text). Clue entries C25 (the width-7/21 statistics), C1(a).

## Prediction

Most rotations as extreme as K4 (share above the 95th percentile at least 0.5) and the reversal too: a property of the carved letters' neighbourhoods, kept by blocks of 7 and 12 more than by blocks of 4. The plants lose their excess when rotated (rotated plants at the shuffles' level). Zero candidates.

## Method

1. Texts: K4; its rotations by 1-96 places; its reversal; 100 block shuffles each for blocks of 4, 7 and 12 (seed 2601); 500 fresh shuffles (seed 2600) as the reference; 3 planted B2 messages (Carter test windows, a random width-19 move and table class, key of 2) and 24 rotations of each (every fourth).
2. Each text through 0238's solve(), unchanged, at cells A1, A2, B1, B2 (every move).
3. Per text its B2 score's percentile among the 500 shuffles.
4. Verdict by the pre-registered shares for the rotations; the blocks and the reversal reported beside it.

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
 "item": "F13.4i",
 "search_reads_known_letters": false,
 "search": "0238's solve(), imported unchanged, every move (27,852), cells A1, A2, B1, B2, MIX8m rescoring",
 "reference": "500 fresh shuffles of K4 (seed 2600)",
 "q95_by_cell": {
  "A1": -536.95,
  "A2": -526.39,
  "B1": -536.95,
  "B2": -524.85
 },
 "k4_percentile_by_cell": {
  "A1": 0.948,
  "A2": 0.314,
  "B1": 0.948,
  "B2": 1.0
 },
 "rotations_share_above_95th_B2": 0.031,
 "rotations_percentile_B2": [
  0.962,
  0.492,
  0.492,
  0.366,
  0.912,
  0.118,
  0.412,
  0.704,
  0.806,
  0.39,
  0.572,
  0.288,
  0.022,
  0.872,
  0.704,
  0.46,
  0.586,
  0.062,
  0.46,
  0.796,
  0.618,
  0.99,
  0.888,
  0.348,
  0.608,
  0.088,
  0.288,
  0.58,
  0.132,
  0.25,
  0.584,
  0.46,
  0.258,
  0.544,
  0.222,
  0.706,
  0.428,
  0.536,
  0.154,
  0.538,
  0.08,
  0.042,
  0.228,
  0.732,
  0.694,
  0.932,
  0.656,
  0.878,
  0.924,
  0.372,
  0.52,
  0.224,
  0.874,
  0.6,
  0.31,
  0.758,
  0.724,
  0.988,
  0.39,
  0.722,
  0.864,
  0.146,
  0.88,
  0.65,
  0.534,
  0.3,
  0.362,
  0.326,
  0.052,
  0.948,
  0.3,
  0.646,
  0.022,
  0.39,
  0.846,
  0.576,
  0.884,
  0.104,
  0.298,
  0.048,
  0.438,
  0.334,
  0.282,
  0.408,
  0.818,
  0.722,
  0.426,
  0.198,
  0.46,
  0.466,
  0.896,
  0.332,
  0.002,
  0.412,
  0.118,
  0.864
 ],
 "rotations_median_percentile_B2": 0.463,
 "top_rotations_B2": [
  {
   "rot": 22,
   "percentile": 0.99,
   "move": "two turns cw 64,23 inverse"
  },
  {
   "rot": 58,
   "percentile": 0.988,
   "move": "two turns cw 14,27"
  },
  {
   "rot": 1,
   "percentile": 0.962,
   "move": "two turns cw 37,17 inverse"
  },
  {
   "rot": 70,
   "percentile": 0.948,
   "move": "two turns cw 20,63"
  },
  {
   "rot": 46,
   "percentile": 0.932,
   "move": "two turns cw 48,11"
  },
  {
   "rot": 49,
   "percentile": 0.924,
   "move": "two turns cw 14,31"
  },
  {
   "rot": 5,
   "percentile": 0.912,
   "move": "two turns cw 41,17"
  },
  {
   "rot": 91,
   "percentile": 0.896,
   "move": "two turns cw 50,29 inverse"
  },
  {
   "rot": 23,
   "percentile": 0.888,
   "move": "two turns cw 40,76 inverse"
  },
  {
   "rot": 77,
   "percentile": 0.884,
   "move": "two turns cw 20,90"
  }
 ],
 "reversal_percentile_B2": 0.736,
 "reversal_move": "two turns cw 40,54 inverse",
 "blocks_share_above_95th_B2": {
  "4": 0.04,
  "7": 0.05,
  "12": 0.11
 },
 "plants": {
  "plant0": {
   "move": "two turns cw 94,19 inverse",
   "unrotated_percentile": 1.0,
   "rotations_above_95th": 1.0
  },
  "plant1": {
   "move": "two turns cw 19,53 inverse",
   "unrotated_percentile": 1.0,
   "rotations_above_95th": 1.0
  },
  "plant2": {
   "move": "two turns cw 19,34 inverse",
   "unrotated_percentile": 1.0,
   "rotations_above_95th": 1.0
  }
 },
 "verdict": "positional",
 "k4_b2_move": "two turns cw 70,19 inverse",
 "k4_b2_reading": "NBENDJZERANDBCKNFILLBAADWRONNWIIHLGARTNRHHKORCULLHCNCSIDEPXMEDFCKRHALORKYXQTRGROWDOJOWSMSHDVNLYAT",
 "texts": 973,
 "compute_seconds": 48,
 "exhaustive": false,
 "modal_cost_estimate": "about 1,072 texts x about 1-2 s: well under $0.1 of Modal credit"
}
```

Notes: F13.4i: K4 B2 percentile 1.000; rotations above the 95th percentile 0.03 (median 0.46); reversal 0.736; blocks of 4/7/12 above 95th 0.04/0.05/0.11; plants unrotated 1.00, 1.00, 1.00, rotated above 95th 1.00, 1.00, 1.00; verdict positional


