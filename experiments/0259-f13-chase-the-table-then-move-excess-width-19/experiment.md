# 0259-f13-chase-the-table-then-move-excess-width-19: F13.4h: chase 0237-0239's replicated excess (the table, then a move, key length 2): 1,000 fresh shuffles; the move library split into width-19 reads and the rest; a period-2 statistic of the carved order under the flagged move; known letters counted after

**Family:** 13-ciphertext-only  
**Parent:** 0238-f13-replicate-k4-table-then-move-length-2-against-fresh-shuffles  
**Decision:** reverted  
**Run:** 2026-10-30T06:36:25+00:00, 117.7 s, status ran  
**Time by phase:** test 10 s, run 118 s, record 0 s

## In plain words

One earlier search found that K4, put through the sculpture's cipher table with a two-letter key and then read out of a grid 19 letters wide, gives a more English-looking jumble than almost any scrambled copy of K4 does. The reading itself is gibberish. We check whether this comes from the way K4's letters happen to sit at width 19, rather than from a hidden message: we repeat the search with only width-19 grids and without them, against 1,000 new scrambled copies, and we measure that width-19 pattern directly.

## Walkthrough, by hand

1. Write K4 in rows 19 letters wide (after first rotating it in a 70-wide grid, as the flagged move does) and read it out the other way.
2. Split the result into its odd and even letters.
3. Count how often letters repeat within each half (the index of coincidence): English-like texts repeat more.
4. Do the same for 1,000 scrambled copies of K4.
5. If K4 repeats more than nearly all copies, the earlier English-like jumble came from this pattern, not from a message.

## Worked example (generated)

```
F13.4h: is K4's English-like jumble at B2 a pattern of the carved order at width 19?

  K4 --(two turns cw 70, 19, inverse)--> moved text
  moved text: odd places | even places   -> index of coincidence of each half
  same for 1,000 scrambled copies; K4's rank says whether the width-19 pattern is unusual,
  and the search repeated with and without width-19 moves says whether it carries the excess.
```

## Lineage

Inherits from 0238-f13-replicate-k4-table-then-move-length-2-against-fresh-shuffles. What changed: F13.4h (Alexis, 2026-10-28, #101: chase it rather than note it). 0237 put K4's best reading at B2 (the sculpture's table with a key of 2, then a move; best move 'two turns cw 70,19 inverse', a width-19 read) above all 100 shuffles; 0238 replicated it (1 of 300 at or above); 0239's blind judge put the reading at the edge of chance. The working guess: a property of the carved order at width 19 (like 0056's width-7 doublets), not a message. Here: 0238's frozen search (imported, unchanged) at B1-B2 and A1-A2 on K4 and 1,000 fresh shuffles, run three times per text with the move library cut to (a) every move, (b) width-19 reads only, (c) every move but width-19 reads; a statistic of the moved text itself, without any search (the two period-2 classes' index of coincidence under the flagged move, and the best over width-19 moves); 8 plants (B2 under a width-19 move) through the same cuts; the 24 known letters counted on K4's readings only after the comparison.

## Hypothesis (domain expert)

F13.4d's excess: K4 under order B (periodic tableau key of length 2 on the sculpture's 8 table classes, then one of 0129's 27,852 moves; ciphertext only, MIX8m) reads above 299 of 300 shuffles. Under order B with key length 2 the reading is the moved text through two fixed substitutions (odd and even places), so a moved text whose two classes are unusually 'monoalphabetic' (high index of coincidence) lets the climb make English-like pairs without any message. If the excess lives only in width-19 reads and the moved text's period-2 IC is as extreme as the B2 score, the excess is a fingerprint of the carved order at width 19, like the width-21 repeats and the width-7 doublet column (04-structure.md), and not a reading. Known letters: the search never reads them (program.md, F13); after the comparison, K4's B2 readings are checked for the 24 letters in message order and in carved order (A2). Clue entries C1(a) (a matrix move then the table, in the other order here), C25 (the width-7/21 statistics).

## Prediction

The B2 excess replicates in (a) at p below 0.05 and in (b) width-19 reads only, and vanishes in (c) without them; the flagged move's period-2 index of coincidence on K4 is above at least 95% of the shuffles under the same move. K4's B2 readings put at most 4 of the 24 known letters in place either way. Plants found in (a) and (b), lost in (c). If so, the excess is recorded as a property of the carved order at width 19 and F13.4h is closed.

## Method

1. 0238's solve(), imported unchanged, with its key lengths cut to 1-2 (cells A1, A2, B1, B2): per order and length the per-column frequency screen keeps the 30 best (move, class), each climbed, best rescored by MIX8m.
2. Three move libraries: all 27,852; the width-19 reads (turn cw/ccw 19, columnar 19 either way, two turns with a 19, and their inverses); the rest.
3. Texts: K4, 1,000 shuffles (seed 2570); 8 plants (Carter test windows, B2 under a random width-19 move and class), 10 own shuffles each.
4. Per library: K4's B2 rank among the shuffles; plants found when above all own copies at B2.
5. No search: under 'two turns cw 70,19 inverse' and over every width-19 move, the moved text's mean IC of its odd and even places, K4 against the shuffles.
6. After: K4's B2 readings' known letters in message order and carved order.

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
 "item": "F13.4h",
 "search_reads_known_letters": false,
 "search": "0238's solve(), imported unchanged, key lengths 1-2 (cells A1, A2, B1, B2), MIX8m rescoring",
 "move_libraries": {
  "all": 27852,
  "w19": 384,
  "not19": 27468
 },
 "k4_copies": 1000,
 "seed": 2570,
 "ranks": {
  "all": {
   "A1": {
    "k4": -537.059,
    "copies_at_or_above": 62,
    "p": 0.0629,
    "move": "keyword LANGLEY (repeats dropped)",
    "reading": "LDFCTSBAMCWZEIEDAYSHEEATINQLLVRDJEWINKWORNYDFCHUTVISMNBULOOBLNVCONTRYCFXPAIXHIWCJIPZADKJVBPREJIHG"
   },
   "A2": {
    "k4": -546.707,
    "copies_at_or_above": 678,
    "p": 0.6783,
    "move": "two turns cw 24,76 inverse",
    "reading": "HASCIPLYNELEDMLOPNEPPDEKWSIXOROHWFMJWSDAFREYTJORNTCUEJDUFNRMLZIPERUKIYUZPHXWILSHKESTLYQBVUSHOWGYF"
   },
   "B1": {
    "k4": -537.059,
    "copies_at_or_above": 62,
    "p": 0.0629,
    "move": "keyword LANGLEY (repeats dropped)",
    "reading": "LDFCTSBAMCWZEIEDAYSHEEATINQLLVRDJEWINKWORNYDFCHUTVISMNBULOOBLNVCONTRYCFXPAIXHIWCJIPZADKJVBPREJIHG"
   },
   "B2": {
    "k4": -507.127,
    "copies_at_or_above": 1,
    "p": 0.002,
    "move": "two turns cw 70,19 inverse",
    "reading": "NBENDJZERANDBCKNFILLBAADWRONNWIIHLGARTNRHHKORCULLHCNCSIDEPXMEDFCKRHALORKYXQTRGROWDOJOWSMSHDVNLYAT"
   }
  },
  "w19": {
   "A1": {
    "k4": -561.675,
    "copies_at_or_above": 385,
    "p": 0.3856,
    "move": "two turns cw 41,19",
    "reading": "TIJWYNNOSYJVHADXNGLTZVAHOLLEJUAARCCIAFZXKROOTWINLEEFEBDPCBTQKNICHCCRPIYIDWFEJBEINDDWLSMSHRVIPVBUM"
   },
   "A2": {
    "k4": -550.673,
    "copies_at_or_above": 269,
    "p": 0.2697,
    "move": "two turns cw 35,19 inverse",
    "reading": "FJTYBTIBCUSOFWAHINPSENGUUDAYAXTWCTISHEUMWOFNDRNOZGZHEXNLGCMIDAWHUHABATCSHANICORNTMEJVGQDBGRDSXYZK"
   },
   "B1": {
    "k4": -561.675,
    "copies_at_or_above": 385,
    "p": 0.3856,
    "move": "two turns cw 41,19",
    "reading": "TIJWYNNOSYJVHADXNGLTZVAHOLLEJUAARCCIAFZXKROOTWINLEEFEBDPCBTQKNICHCCRPIYIDWFEJBEINDDWLSMSHRVIPVBUM"
   },
   "B2": {
    "k4": -507.127,
    "copies_at_or_above": 0,
    "p": 0.001,
    "move": "two turns cw 70,19 inverse",
    "reading": "NBENDJZERANDBCKNFILLBAADWRONNWIIHLGARTNRHHKORCULLHCNCSIDEPXMEDFCKRHALORKYXQTRGROWDOJOWSMSHDVNLYAT"
   }
  },
  "not19": {
   "A1": {
    "k4": -537.059,
    "copies_at_or_above": 60,
    "p": 0.0609,
    "move": "keyword LANGLEY (repeats dropped)",
    "reading": "LDFCTSBAMCWZEIEDAYSHEEATINQLLVRDJEWINKWORNYDFCHUTVISMNBULOOBLNVCONTRYCFXPAIXHIWCJIPZADKJVBPREJIHG"
   },
   "A2": {
    "k4": -546.707,
    "copies_at_or_above": 674,
    "p": 0.6743,
    "move": "two turns cw 24,76 inverse",
    "reading": "HASCIPLYNELEDMLOPNEPPDEKWSIXOROHWFMJWSDAFREYTJORNTCUEJDUFNRMLZIPERUKIYUZPHXWILSHKESTLYQBVUSHOWGYF"
   },
   "B1": {
    "k4": -537.059,
    "copies_at_or_above": 60,
    "p": 0.0609,
    "move": "keyword LANGLEY (repeats dropped)",
    "reading": "LDFCTSBAMCWZEIEDAYSHEEATINQLLVRDJEWINKWORNYDFCHUTVISMNBULOOBLNVCONTRYCFXPAIXHIWCJIPZADKJVBPREJIHG"
   },
   "B2": {
    "k4": -513.262,
    "copies_at_or_above": 3,
    "p": 0.004,
    "move": "two turns cw 53,41 inverse",
    "reading": "TZUODASJFPKQIDPPPEYTXEVTAKSVARDODUCAGOXFGXVSNFMTRNKBOMZINGFEBIUPLEOPERHAGHMYGRUZQUXYARRORLOPLEOFV"
   }
  }
 },
 "plants_found_at_B2": {
  "all": [
   8,
   8
  ],
  "w19": [
   8,
   8
  ],
  "not19": [
   5,
   8
  ]
 },
 "plants_read_exactly": {
  "all": 8,
  "w19": 8,
  "not19": 0
 },
 "ic2_flagged_move": {
  "k4": 0.03927,
  "copies_at_or_above": 137,
  "copies_median": 0.03562
 },
 "ic2_best_width19_move": {
  "k4": 0.04575,
  "copies_at_or_above": 323,
  "copies_median": 0.04496
 },
 "k4_b2_known_letters": {
  "all": {
   "message_order": 3,
   "carved_order": 3
  },
  "w19": {
   "message_order": 3,
   "carved_order": 3
  },
  "not19": {
   "message_order": 1,
   "carved_order": 2
  }
 },
 "compute_seconds": 93,
 "exhaustive": false,
 "modal_cost_estimate": "about 1,089 texts x 3 cuts x about 2-3 s: about 2-3 core-hours, about $0.3-1 of Modal credit (about $3.7 left after the margin)"
}
```

Notes: F13.4h: K4 at B2 p all 0.002, width-19 only 0.001, without width 19 0.004 (1,000 shuffles); period-2 IC under the flagged move: 137 of 1,000 at or above; plants found all 8/8, w19 8/8, not19 5/8


