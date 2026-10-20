# 0199-turning-grille-with-the-table: F6.20, part 1: a 10x10 turning grille (Fleissner) copied out by rows, before or after a repeating key on the table; free keys of 1-6 letters and every key word of 7 or more, every card, exact, with planted grilles in the same run

**Family:** 6-transposition-then-tableau  
**Parent:** 0164-disrupted-triangle-interrupted-trapezoid  
**Decision:** reverted  
**Run:** 2026-10-20T07:32:00+00:00, 1227.0 s, status ran  
**Time by phase:** design 438 s, implement 148468 s, test 1741 s, run 1227 s, record 0 s

## In plain words

A turning grille is a square card with holes in it. Lay it on a 10 by 10 grid and write the message through the holes; turn the card a quarter and write on; after four turns every square holds a letter (here three stay empty, since the message has 97). Copy the grid out row by row and the letters are scrambled. We ask whether such a card, with a repeating secret word on the sculpture's table, could have made K4. There are a thousand million million cards, too many to try one by one, but the known words rule most of them out a few squares in, so a careful search can check every card.

## Walkthrough, by hand

1. Cut 25 holes in a 10 by 10 card so that turning it four times uncovers every square once.
2. Lay it on the grid and write the first 25 letters through the holes, row by row.
3. Turn the card a quarter clockwise and write the next 25; and twice more. The last three holes stay empty.
4. Copy the grid out row by row, skipping the empty squares: 97 letters.
5. Encipher those 97 on the table with a repeating key word (or encipher first, then use the card).
6. To test a card against K4: follow each known letter to its square, read the carved letter there, and see whether the key letters it demands repeat with the key's length or spell the key word.

## Worked example (generated)

```
a card: the turn on which each square is written (0-3), clockwise, copied out by rows

  1 0 3 2 1 2 3 0 1 2
  0 3 2 1 0 1 2 3 0 1
  3 2 1 0 3 0 1 2 3 0
  2 1 0 3 2 3 0 1 2 3
  1 0 3 2 1 2 3 0 1 2
  0 3 2 1 0 3 0 1 2 3
  1 0 3 2 1 0 1 2 3 0
  2 1 0 3 2 1 2 3 0 1
  3 2 1 0 3 2 3 0 1 2
  0 3 2 1 0 3 0 1 2 3

the holes of the first position are the 0s; the 97 letters fill the 0s row by row, then the 1s, 2s, 3s;
the last three 3s stay empty

place  known  lands at  carved
   22      E        88       U
   26      N         1       O
   34      T        32       K
   64      B        53       K
   74      K        92       U
```

## Lineage

Inherits from 0164-disrupted-triangle-interrupted-trapezoid. What changed: F6.20 (issue #78), a move never tested: the turning grille. A 10x10 card with one hole in each of its 25 rotation orbits (4^25, about 10^15 cards); the message is written through the holes row by row, the card turned a quarter, four times; 97 letters leave three cells empty, skipped when the grid is copied out row by row (Fleissner's read-off). Four procedures: turned clockwise or anticlockwise, the empty cells at the end of the writing or at its start (writing and reading by columns is the transpose, the same set of moves). Then a repeating key on the standard or KRYPTOS table after the grille (A) or before it (B). Two arms, both exact over every card: any key of 1-6 letters (8 table classes), and every dictionary or puzzle word of 7 letters or more as the key (24 conventions). A depth-first search walks the top half of the grid, fixing a cell's turn and its 180-degree partner's at once and checking each known letter as it lands. Copied out by columns is a different set of moves and far costlier; it follows as part 2. The F7 standing step rides along.

## Hypothesis (domain expert)

C1(a) (a matrix stage, then the table), C3 (Sanborn's 'spatial systems... pattern, light and shadow': a grille is a card held to the light), C5 (a hand system keyed by 'key word/s'). Source: reports/agent-memorized-hand-ciphers.md (Fleissner 1881; German army 1916; Abwehr and RS44 stencils, Lewis, German Agent Systems). Model: c = T(sigma(p)) (order A) or sigma(T(p)) (order B), sigma the grille's permutation, T a periodic tableau key. Search: the top half of the grid in row order; a cell's rank in its turn is the count of earlier top cells of that turn, its 180-degree partner (turn + 2) has rank 24 minus that count, so both message places are known at once. Free key: each slot's value is set by its first known letter and checked by the rest; key words: every letter is a check (24 checks against about 50 bits of card). Count: distinct landing maps (the carved squares of the 24 known letters), since cards that differ only where unknown letters go are one reading of the known ones. Statistic fixed before the run: free key, per procedure and order, the shortest length with a landing map that fits and the cells (order, length) where K4's count exceeds every copy's; key words, the number of (word, convention, order, procedure) settings with a map, K4 against each copy. Measured cost: a free key of 7 letters takes 10^8-10^9 nodes per setting, 12 letters over 2 x 10^9: lengths 7-26 with a free key are blocked by cost. Not tested: stencils with arbitrary holes, the Abwehr's 13x19 card (no remembered rule for its holes in the source).

## Prediction

No card fits K4 with any key of 1-6 letters or any key word, in either order and any procedure; the scrambled copies the same. Each planted grille is found, on its own landing map. The grille plus a key makes the two fingerprints together at the random-letter rate (zero in 2,000). Zero candidates.

## Method

1. Orbits: the 25 cells of the top-left quarter; a card is one turn (0-3) per orbit.
2. Walk the top half in row order; at a cell whose orbit is new, branch over its four turns; place the message letter there (turn, rank) and at the 180-degree partner (turn + 2, rank 24 minus).
3. Mark the three empty cells (last three of turn 3, or first three of turn 0); a carved place is the row position less the empty cells before it.
4. Each known letter landed: key slot = carved place (A) or message place (B) mod the length; free key: set or check the slot; key word: compare with the word's letter. Prune on a clash; stop a branch once all 24 landed.
5. Every procedure, order, class and length 1-6, then every key word on 24 conventions, on K4, ten copies and four plants; compiled, checked against a literal Python builder on 25,600 cards and 32 plants.

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
 "family": "10x10 turning grille (25 holes, three empty cells), then or before a repeating key on the standard/KRYPTOS tables; exact constraint search",
 "cards_per_procedure": 1125899906842624,
 "procedures": [
  "cw, out by rows, empty cells at the end",
  "cw, out by rows, empty cells at the start",
  "ccw, out by rows, empty cells at the end",
  "ccw, out by rows, empty cells at the start"
 ],
 "orders": {
  "A": "grille, then key",
  "B": "key, then grille"
 },
 "texts": "K4, 10 scrambled copies (seed 1620), 4 planted grilles",
 "free_key": {
  "lengths": "1-6",
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
  "per_procedure": {
   "cw, out by rows, empty cells at the end": {
    "A": {
     "k4_placements_by_length": [
      0,
      0,
      0,
      0,
      0,
      0
     ],
     "copies_placements_by_length_max": [
      0,
      0,
      0,
      0,
      0,
      0
     ],
     "incomplete_lengths_any_text": [],
     "k4_shortest_fit": null,
     "copies_shortest_fit": [
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      null
     ],
     "k4_above_every_copy": [],
     "copy_cells_above_rest": [
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
    "B": {
     "k4_placements_by_length": [
      0,
      0,
      0,
      0,
      0,
      0
     ],
     "copies_placements_by_length_max": [
      0,
      0,
      0,
      0,
      0,
      0
     ],
     "incomplete_lengths_any_text": [],
     "k4_shortest_fit": null,
     "copies_shortest_fit": [
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      null
     ],
     "k4_above_every_copy": [],
     "copy_cells_above_rest": [
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
    }
   },
   "cw, out by rows, empty cells at the start": {
    "A": {
     "k4_placements_by_length": [
      0,
      0,
      0,
      0,
      0,
      0
     ],
     "copies_placements_by_length_max": [
      0,
      0,
      0,
      0,
      0,
      0
     ],
     "incomplete_lengths_any_text": [],
     "k4_shortest_fit": null,
     "copies_shortest_fit": [
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      null
     ],
     "k4_above_every_copy": [],
     "copy_cells_above_rest": [
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
    "B": {
     "k4_placements_by_length": [
      0,
      0,
      0,
      0,
      0,
      0
     ],
     "copies_placements_by_length_max": [
      0,
      0,
      0,
      0,
      0,
      0
     ],
     "incomplete_lengths_any_text": [],
     "k4_shortest_fit": null,
     "copies_shortest_fit": [
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      null
     ],
     "k4_above_every_copy": [],
     "copy_cells_above_rest": [
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
    }
   },
   "ccw, out by rows, empty cells at the end": {
    "A": {
     "k4_placements_by_length": [
      0,
      0,
      0,
      0,
      0,
      0
     ],
     "copies_placements_by_length_max": [
      0,
      0,
      0,
      0,
      0,
      0
     ],
     "incomplete_lengths_any_text": [],
     "k4_shortest_fit": null,
     "copies_shortest_fit": [
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      null
     ],
     "k4_above_every_copy": [],
     "copy_cells_above_rest": [
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
    "B": {
     "k4_placements_by_length": [
      0,
      0,
      0,
      0,
      0,
      0
     ],
     "copies_placements_by_length_max": [
      0,
      0,
      0,
      0,
      0,
      0
     ],
     "incomplete_lengths_any_text": [],
     "k4_shortest_fit": null,
     "copies_shortest_fit": [
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      null
     ],
     "k4_above_every_copy": [],
     "copy_cells_above_rest": [
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
    }
   },
   "ccw, out by rows, empty cells at the start": {
    "A": {
     "k4_placements_by_length": [
      0,
      0,
      0,
      0,
      0,
      0
     ],
     "copies_placements_by_length_max": [
      0,
      0,
      0,
      0,
      0,
      0
     ],
     "incomplete_lengths_any_text": [],
     "k4_shortest_fit": null,
     "copies_shortest_fit": [
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      null
     ],
     "k4_above_every_copy": [],
     "copy_cells_above_rest": [
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
    "B": {
     "k4_placements_by_length": [
      0,
      0,
      0,
      0,
      0,
      0
     ],
     "copies_placements_by_length_max": [
      0,
      0,
      0,
      0,
      0,
      0
     ],
     "incomplete_lengths_any_text": [],
     "k4_shortest_fit": null,
     "copies_shortest_fit": [
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      null
     ],
     "k4_above_every_copy": [],
     "copy_cells_above_rest": [
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
    }
   }
  },
  "k4_fits": [],
  "k4_cells_above_every_copy": 0,
  "copy_cells_above_rest": [
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
  "search_nodes": 81815034340,
  "seconds": 657,
  "blocked": "lengths 7-26: one setting costs 0.9-7 x 10^8 nodes at length 7 and over 2 x 10^9 at 12 (measured on K4), about 10^5 settings: blocked by cost"
 },
 "key_words": {
  "words": 200563,
  "lengths": "7-28",
  "conventions": [
   "std/std/std/vig",
   "std/std/std/beau",
   "std/std/std/var",
   "std/std/kry/vig",
   "std/std/kry/beau",
   "std/std/kry/var",
   "std/kry/std/vig",
   "std/kry/std/beau",
   "std/kry/std/var",
   "std/kry/kry/vig",
   "std/kry/kry/beau",
   "std/kry/kry/var",
   "kry/std/std/vig",
   "kry/std/std/beau",
   "kry/std/std/var",
   "kry/std/kry/vig",
   "kry/std/kry/beau",
   "kry/std/kry/var",
   "kry/kry/std/vig",
   "kry/kry/std/beau",
   "kry/kry/std/var",
   "kry/kry/kry/vig",
   "kry/kry/kry/beau",
   "kry/kry/kry/var"
  ],
  "source": "the vocabulary, puzzle phrases, kryptos/data/words.txt",
  "settings_per_text": 38508096,
  "k4_settings_with_a_card": 0,
  "copies_settings_with_a_card": [
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
  "k4_hits": [],
  "search_nodes": 34110186412,
  "seconds": 559
 },
 "plants": [
  {
   "arm": "free key",
   "procedure": "cw, out by rows, empty cells at the start",
   "order": "A",
   "class": "std/kry/beau",
   "length": 5,
   "placements_fitting_at_its_setting": 1,
   "complete": true,
   "planted_card_found": true,
   "placements_at_shorter_lengths": 0
  },
  {
   "arm": "free key",
   "procedure": "ccw, out by rows, empty cells at the end",
   "order": "B",
   "class": "kry/std/beau",
   "length": 6,
   "placements_fitting_at_its_setting": 8,
   "complete": true,
   "planted_card_found": true,
   "placements_at_shorter_lengths": 0
  },
  {
   "arm": "key word",
   "procedure": "ccw, out by rows, empty cells at the start",
   "order": "B",
   "convention": "kry/kry/std/beau",
   "word": "UNGUIDABLY",
   "words_fitting_at_its_setting": 1,
   "planted_word_found": true,
   "planted_card_found": true,
   "settings_fitting_anywhere": 1
  },
  {
   "arm": "key word",
   "procedure": "cw, out by rows, empty cells at the end",
   "order": "A",
   "convention": "std/kry/std/var",
   "word": "REMOTENESS",
   "words_fitting_at_its_setting": 1,
   "planted_word_found": true,
   "planted_card_found": true,
   "settings_fitting_anywhere": 1
  }
 ],
 "stop_queue": false,
 "self_check": {
  "planted_cards_found_by_full_search": 16,
  "planted_words_found_by_keyword_arm": 16,
  "cards_compared": 25600,
  "of_which_fit": 2625,
  "note": "the compiled walk agrees with the literal Python builder (turn the card, fill holes by rows, copy out) on every card compared"
 },
 "fingerprints_F7": {
  "grille, then a length-7 key": {
   "column": 0.0025,
   "repeats21": 0.0095,
   "both": 0.0
  },
  "length-7 key, then the grille": {
   "column": 0.0005,
   "repeats21": 0.0065,
   "both": 0.0
  },
  "grille, then a length-21 key": {
   "column": 0.003,
   "repeats21": 0.006,
   "both": 0.0
  },
  "length-21 key, then the grille": {
   "column": 0.0015,
   "repeats21": 0.0035,
   "both": 0.0
  },
  "calibration: random letters": {
   "column": 0.003,
   "repeats21": 0.002,
   "both": 0.0
  }
 },
 "not_tested": "free keys of 7-26 letters (cost); stencils with arbitrary holes (any permutation); the Abwehr's 13x19 card (no rule for its holes in the source)",
 "seconds": 1227,
 "exhaustive": "yes for both arms: every card, every procedure, both orders; free keys 1-6, key words 7 letters and up"
}
```

Notes: Plants: free key cw, out by rows, empty cells at the start A: found True; free key ccw, out by rows, empty cells at the end B: found True; key word ccw, out by rows, empty cells at the start B: found True; key word cw, out by rows, empty cells at the end A: found True. Free keys 1-6: K4 fits 0 settings; K4 above every copy in 0 cells, copies 0-0. Key words (200,563): settings with a card K4 0, copies 0-0.


