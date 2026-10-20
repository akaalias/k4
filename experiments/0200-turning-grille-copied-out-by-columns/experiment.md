# 0200-turning-grille-copied-out-by-columns: F6.20, part 2: the turning grille with the grid copied out by columns, before or after a repeating key on the table; free keys of 1-3 letters and every key word of 7 or more, every card, exact, with planted grilles

**Family:** 6-transposition-then-tableau  
**Parent:** 0199-turning-grille-with-the-table  
**Decision:** error  
**Run:** 2026-10-20T07:55:41+00:00, 3660.3 s, status error  
**Time by phase:** unattributed 193 s, run 3660 s, record 0 s

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

```

## Lineage

Inherits from 0199-turning-grille-with-the-table. What changed: 0199 with the one remaining read-off: the card is written through by rows as before, but the filled grid is copied out column by column (written by columns and copied by rows is the transpose of this, the same set of moves). Here a known letter's carved place depends on empty cells the search has not yet placed, so each landing guesses how many empty cells precede it (0 to 3 minus those placed) and the guess is checked as they appear; one guess survives per card. This costs far more than by rows: a free key is exact here only to 3 letters (4 and 5 cost 10^7-10^9 nodes per setting, measured on K4), key words of 7 letters and up as in 0199. Budget raised to 60 minutes for the key-word arm (about 32 minutes on 8 workers).

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
(none recorded)
```


Error:
```
no output
```

