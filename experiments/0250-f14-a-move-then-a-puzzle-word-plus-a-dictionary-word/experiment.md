# 0250-f14-a-move-then-a-puzzle-word-plus-a-dictionary-word: F14.6c: every move of the type-1 library (either order), then the sculpture's table with a puzzle word and a dictionary word summed as the key; the known letters force the dictionary word, looked up among every rotation; K4 against 30 shuffles, 8 plants

**Family:** 14-scheidt-mask-keyed-by-words  
**Parent:** 0115-a-puzzle-word-plus-any-english-word  
**Decision:** reverted  
**Run:** 2026-10-28T04:33:49+00:00, 9920.2 s, status ran  
**Time by phase:** unattributed 161 s, run 9920 s, record 0 s

## In plain words

Shuffle the letters through a grid as in the third section, then use the table twice with two words, one from the puzzle and one any English word. Using the table twice is the same as using it once with the two words added. For every grid shuffle and every puzzle word, the clue words tell us exactly what the second word would have to be; we look it up in the dictionary.

## Walkthrough, by hand

1. Pick a move, say K3's rule with some numbers, and see where each known letter lands.
2. Pick a rule of the table and a puzzle word with its start, say KRYPTOS from its K.
3. At each known place, the table needs some key letter; take KRYPTOS's letter off it: the rest is the second word's letter.
4. For a second word of length 9, places in the same slot (landing place mod 9) must agree; then read the word off and look it up.
5. Repeat for every move, order, rule, puzzle word and length, and for the shuffles of K4.

## Worked example (generated)

```
No move, KRYPTOS table (Vigenere), KRYPTOS from K as the puzzle word; the dictionary word's forced letters:

place  known  carved  key value  KRYPTOS  second word's letter
   22      E       F          1        K                     R
   23      A       L         10        R                     C
   24      S       R         21        Y                     N
   25      T       V         18        P                     I
   64      B       N         11        K                     E
   65      E       Y         17        R                     J
   66      R       P          2        Y                     K

With a move, each known letter's slot is its landing place (order A) or its message place (order B) mod the word length.
```

## Lineage

Inherits from 0115-a-puzzle-word-plus-any-english-word. What changed: F14.6c (issue #93; reports/f14.6-grammar.md form 9). 0115 summed a puzzle word and a dictionary word with no move; F6 (0110-0114, 0129) put single keys of length 1-26 after or before every move. The sum of two words repeats only every lcm(m, n) letters, beyond every F6 length. Here: 27,852 moves x 2 orders x 24 rules x 1,085 puzzle-word starts (1.45 x 10^9 settings per text); for each, the known letters force the dictionary word at the slots they cover (bit-packed same-slot checks over all moves at once), and the forced word is looked up among every rotation of every dictionary word of 3-24 letters.

## Hypothesis (domain expert)

C1(a) (Sanborn's matrix, then the table), C5 ('key word/s'), C20(a) ('layer two' as a second pass with a second word), Scheidt's 'building layers... mix and match'. K3's matrix, then K1/K2's table used twice with two remembered words. Pre-registered: no setting fits K4 (a hit needs the forced letters to spell a word); hit counts against 30 shuffles; a plant (Carter, random move, order, rule, puzzle word and dictionary word) is found when its own keys come back.

## Prediction

No hit on K4; none or almost none on shuffles; plants 8 of 8.

## Method

1. Moves: 0129's type-1 library (27,852), orders A (move, then table) and B (table, then move).
2. Rules: 24 (Vigenere, variant, Beaufort; plain, cipher and key alphabets standard or KRYPTOS).
3. For each rule and puzzle-word start: the remainder the dictionary word must supply at each known place, for every move at once; same-slot agreement packed as bits; per length 3-24 and order, survivors' forced words looked up among every dictionary rotation (covered slots matched where the known places leave some uncovered).
4. K4 and 30 shuffles; 8 plants with their own known letters; K4's hits decrypted and submitted.

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
 "item": "F14.6c",
 "moves": 27852,
 "orders": 2,
 "rules": 24,
 "puzzle_word_starts": 1085,
 "settings_per_text": 1450532160,
 "dictionary_word_lengths": [
  3,
  24
 ],
 "survivors_by_order_and_length": {
  "A18": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 2
  },
  "A19": {
   "k4": 1,
   "copies_median": 3.0,
   "copies_max": 22
  },
  "A20": {
   "k4": 52,
   "copies_median": 62.0,
   "copies_max": 94
  },
  "A21": {
   "k4": 1686,
   "copies_median": 610.0,
   "copies_max": 2282
  },
  "A22": {
   "k4": 52086,
   "copies_median": 45629.0,
   "copies_max": 71477
  },
  "A23": {
   "k4": 129215,
   "copies_median": 126909.5,
   "copies_max": 128284
  },
  "A24": {
   "k4": 1400824,
   "copies_median": 1373813.0,
   "copies_max": 1736259
  },
  "B17": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 1
  },
  "B18": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 2
  },
  "B23": {
   "k4": 1,
   "copies_median": 0.0,
   "copies_max": 1
  },
  "B24": {
   "k4": 30,
   "copies_median": 35.0,
   "copies_max": 1830
  }
 },
 "cells_k4_above_every_copy": [
  "A23"
 ],
 "hits": {
  "k4": 0,
  "copies": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
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
 "plants_found": 8,
 "plants": 8,
 "plant_detail": {
  "plant0": {
   "found": true,
   "n": 12,
   "order": "A",
   "words": [
    [
     "REMAINS",
     4
    ],
    [
     "SEMIPELLUCID",
     4
    ]
   ]
  },
  "plant1": {
   "found": true,
   "n": 12,
   "order": "A",
   "words": [
    [
     "WILLIAMWEBSTER",
     12
    ],
    [
     "FLAVANTHRONE",
     3
    ]
   ]
  },
  "plant2": {
   "found": true,
   "n": 4,
   "order": "B",
   "words": [
    [
     "POINT",
     3
    ],
    [
     "ALLE",
     1
    ]
   ]
  },
  "plant3": {
   "found": true,
   "n": 13,
   "order": "B",
   "words": [
    [
     "BETWEEN",
     3
    ],
    [
     "PREPREFERENCE",
     6
    ]
   ]
  },
  "plant4": {
   "found": true,
   "n": 5,
   "order": "A",
   "words": [
    [
     "WILLIAMWEBSTER",
     12
    ],
    [
     "TOMBE",
     1
    ]
   ]
  },
  "plant5": {
   "found": true,
   "n": 4,
   "order": "A",
   "words": [
    [
     "DOES",
     2
    ],
    [
     "PEAR",
     1
    ]
   ]
  },
  "plant6": {
   "found": true,
   "n": 21,
   "order": "B",
   "words": [
    [
     "WEST",
     2
    ],
    [
     "GLOSSOLABIOPHARYNGEAL",
     7
    ]
   ]
  },
  "plant7": {
   "found": true,
   "n": 17,
   "order": "A",
   "words": [
    [
     "DEGREES",
     5
    ],
    [
     "PROCRASTINATIVELY",
     1
    ]
   ]
  }
 },
 "texts": 39,
 "copies": 30,
 "exhaustive": true,
 "compute_seconds": 9877
}
```

Notes: 1,450,532,160 settings per text; dictionary-word hits K4 0, shuffles max 0; cells with K4 above every shuffle 1 of 44; plants 8/8


