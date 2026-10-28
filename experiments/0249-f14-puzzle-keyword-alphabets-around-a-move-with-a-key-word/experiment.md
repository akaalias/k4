# 0249-f14-puzzle-keyword-alphabets-around-a-move-with-a-key-word: F14.6b: keyword alphabets from the puzzle words around every move of the type-1 library (either order), the key a word of any length 1-26; every setting decided exactly by the known letters, the key words looked up; K4 against 30 shuffles, 8 plants

**Family:** 14-scheidt-mask-keyed-by-words  
**Parent:** 0129-one-free-alphabet-after-every-move-exact  
**Decision:** reverted  
**Run:** 2026-10-28T04:23:25+00:00, 463.1 s, status ran  
**Time by phase:** unattributed 293 s, run 463 s, record 0 s

## In plain words

Three hand steps the creators taught each other: scramble the alphabet with a word, shuffle the letters through a grid as in the third section, then use the table with a key word. We try every grid shuffle in our library, every alphabet made from a word of the puzzle, and every key length, and the clue words tell us exactly which combinations are possible. For those we check whether the key is an English word.

## Walkthrough, by hand

1. Take a puzzle word, say SHADOW, and write its keyword alphabet: SHADOWBCEFGIJKLMNPQRTUVXYZ.
2. Take a move, say a quarter turn of a grid 7 wide, and find where each known letter lands in the carved text.
3. Take a key length, say 11: each known letter's key slot is its landing place mod 11.
4. On the table with SHADOW's alphabet, work out the key value each known letter needs; two in one slot must agree.
5. If all agree, read the key letters off the slots and look for an English word that gives them from some start.

## Worked example (generated)

```
SHADOW's keyword alphabet SHADOWBCEFGIJKLMNPQRTUVXYZ on both sides, added form, no move, key length 11:

place  known  carved  key value  slot
   22      E       F          1    10
   23      A       L         12     0
   24      S       R         19     1
   25      T       V          2     2
   33      S       S          0    10
   34      T       S          6     0
   66      R       P         24    10
   67      L       V          8     0

Places in the same slot must ask the same key value; with a move, the slot is the landing place mod 11.
```

## Lineage

Inherits from 0129-one-free-alphabet-after-every-move-exact. What changed: F14.6b (issue #93; reports/f14.6-grammar.md form 10). 0129 and 0130 put one free alphabet (any of 26!) around every type-1 move and found fits from key length 6 at the copies' rate, undecidable. Here the alphabets are the keyword alphabets of the 170 puzzle words (plain side, cipher side or both; with the standard or KRYPTOS alphabet on the other side), plus the four standard/KRYPTOS pairs: 854 tables x 2 forms x 27,852 moves x 2 orders x key lengths 1-26, each decided exactly by the 24 known letters (the same-slot places must ask the same key value; packed as bit masks per move). Every surviving setting's forced key is then checked against every dictionary and puzzle word of the length, every start, numbered on standard, KRYPTOS, the plain or the cipher alphabet, any shift, in the Vigenere, variant and Beaufort readings.

## Hypothesis (domain expert)

C1(a) (Sanborn, CNN 2005: 'I used a matrix code, and then... went back to this table'), C4(a) (Scheidt's mask as a keyword alphabet), C5 ('key word/s'), C27(c) (a 'slightly different' table). The mask (a keyword alphabet), K3's matrix and K1/K2's table in one procedure of three hand steps, every key from the puzzle's own words. A free alphabet leaves these cells undecided (0129, 0130; F6.1 blocked by cost); 170 alphabets are under 8 bits, so the known letters decide. Pre-registered: no setting fits K4 beyond the shuffles' counts, per order and key length (52 cells; flag at p < 0.05/52 against 30 shuffles: unreachable, so a cell above every shuffle is a candidate to replicate); no key word fits K4. A plant (Carter, random puzzle table, move, order and dictionary key word) is found when its setting survives and its key word comes back.

## Prediction

K4 fits at the shuffles' rate in every cell (few settings below length 16); no key word on K4; plants 8 of 8.

## Method

1. Moves: 0129's type-1 library (27,852 distinct, from its frozen route_library). Orders: A (move, then the table: slot = landing place mod L) and B (table, then the move: slot = message place mod L).
2. Tables: for each puzzle keyword alphabet W, (W, W), (W, std), (std, W), (W, KRY), (KRY, W); plus std/KRY pairs. Forms: added (Vigenere and variant agree on consistency) and Beaufort.
3. Per text, table and form: forced key value at each known place for every move at once; the pairs of known places that disagree packed as bits; a (move, order, L) setting survives if no disagreeing pair shares a slot.
4. Survivors: key words of length L (dictionary 3-24, puzzle 2-30) matched at the covered slots up to a shift, four numberings, three readings.
5. K4 and 30 shuffles; 8 plants with their own known letters; K4's key-word fits decrypted and submitted.

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
 "item": "F14.6b",
 "moves": 27852,
 "tables": 854,
 "puzzle_words": 171,
 "settings_per_text": 2473703232,
 "survivors_by_order_and_length": {
  "A1": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "A2": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "A3": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "A4": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "A5": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "A6": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "A7": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "A8": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "A9": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "A10": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "A11": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "A12": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "A13": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "A14": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "A15": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "A16": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "A17": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "A18": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 2
  },
  "A19": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 3
  },
  "A20": {
   "k4": 5,
   "copies_median": 5.0,
   "copies_max": 14
  },
  "A21": {
   "k4": 56,
   "copies_median": 52.0,
   "copies_max": 90
  },
  "A22": {
   "k4": 3983,
   "copies_median": 3308.0,
   "copies_max": 5186
  },
  "A23": {
   "k4": 8111,
   "copies_median": 8359.0,
   "copies_max": 9364
  },
  "A24": {
   "k4": 94456,
   "copies_median": 88094.0,
   "copies_max": 94694
  },
  "A25": {
   "k4": 254488,
   "copies_median": 256656.0,
   "copies_max": 258251
  },
  "A26": {
   "k4": 1713788,
   "copies_median": 1710825.0,
   "copies_max": 1717041
  },
  "B1": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "B2": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "B3": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "B4": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "B5": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "B6": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "B7": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "B8": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "B9": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "B10": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "B11": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "B12": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "B13": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "B14": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "B15": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "B16": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "B17": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "B18": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "B19": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "B20": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "B21": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "B22": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "B23": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0
  },
  "B24": {
   "k4": 4,
   "copies_median": 4.0,
   "copies_max": 10
  },
  "B25": {
   "k4": 2801,
   "copies_median": 2712.5,
   "copies_max": 2915
  },
  "B26": {
   "k4": 1833004,
   "copies_median": 1825778.5,
   "copies_max": 1840347
  }
 },
 "cells_k4_above_every_copy": [],
 "key_word_hits": {
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
   "L": 21,
   "order": "B",
   "word": "ANATOMICOPATHOLOGICAL"
  },
  "plant1": {
   "found": true,
   "L": 6,
   "order": "A",
   "word": "TWEAKY"
  },
  "plant2": {
   "found": true,
   "L": 10,
   "order": "B",
   "word": "MENAGERIST"
  },
  "plant3": {
   "found": true,
   "L": 14,
   "order": "A",
   "word": "POLYPRAGMATIST"
  },
  "plant4": {
   "found": true,
   "L": 24,
   "order": "A",
   "word": "FORMALDEHYDESULPHOXYLATE"
  },
  "plant5": {
   "found": true,
   "L": 5,
   "order": "A",
   "word": "SCENT"
  },
  "plant6": {
   "found": true,
   "L": 21,
   "order": "A",
   "word": "DISPROPORTIONABLENESS"
  },
  "plant7": {
   "found": true,
   "L": 16,
   "order": "B",
   "word": "SUBCONSCIOUSNESS"
  }
 },
 "texts": 39,
 "copies": 30,
 "exhaustive": true,
 "compute_seconds": 415
}
```

Notes: 2,473,703,232 settings per text; key-word hits K4 0, shuffles max 0; cells with K4 above every shuffle 0 of 52; plants 8/8


