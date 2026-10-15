# 0032-row-keyed-grids-one-key-letter-per-row: Sanborn's matrix with a key letter per row: write the message in rows of width w, encipher each row with one letter of the key

**Family:** 6-transposition-then-tableau  
**Parent:** 0026-double-keyed-columnar-then-tableau  
**Decision:** reverted  
**Run:** 2026-10-15T07:43:40+00:00, 0.2 s, status ran  
**Time by phase:** design 4 s, implement 50 s, test 1 s, run 0 s, record 0 s

## In plain words

Imagine writing the message in a grid, say seven letters per line, and putting one letter of a secret word beside each line: every letter on that line is shifted by that one letter. The 13 known letters of EASTNORTHEAST fill a whole line or two, and every letter on a line must agree on the shift. We try every line width and every secret-word length, with every table the puzzle's words can build, and see whether the known letters ever agree.

## Walkthrough, by hand

1. Width 7: the rows are positions 1-7, 8-14, 15-21, 22-28, 29-35, and so on.
2. Row 22-28 holds E A S T N O R against the carved F L R V Q Q P.
3. On the plain alphabet with Vigenere, E to F is a shift of 1, A to L a shift of 11: the row cannot have one key letter, so width 7 is dead for this alphabet.
4. Width 20: rows 21-40 and 61-80; the first holds 13 cribs, the second 11; each row must agree internally.
5. Try every alphabet the puzzle's words build; a surviving width then gets every key length tried, which ties rows together.

## Worked example (generated)

```
width 7, plain alphabet for both message and carved letters, Vigenere: shifts within row 22-28

pos  plain  carved  shift
 22    E      F       1
 23    A      L      11
 24    S      R      25
 25    T      V       2
 26    N      Q       3
 27    O      Q       2
 28    R      P      24

one row, seven different shifts: width 7 cannot have one key letter per row under this alphabet.
```

## Lineage

Inherits from 0026-double-keyed-columnar-then-tableau. What changed: Not a transposition this time but a grid-shaped key: every letter in a row shares one key letter, and the rows take the key word's letters in turn. A column-shaped key is an ordinary periodic key and is dead; the row-shaped one was never swept.

## Hypothesis (domain expert)

Sanborn's 'matrix code' is text written in rows and read another way (C1). A natural hand variant keeps the reading order and keys by row: position i takes key letter key[(i div w) mod L], so all w letters of a row share one key letter and rows cycle through the word. EASTNORTHEAST occupies 13 consecutive positions, so for w up to 13 at least one row holds several cribs that must force the same key letter, with chance 26 to the minus (k - 1) for k cribs in a row; the row-length L then adds collisions between rows. Swept: w = 2 to 48, L = 1 to 48, plain and cipher alphabets from the standard, KRYPTOS and keyword-mixed vocabulary alphabets (63), three modes; the key alphabet drops out of the consistency test. Survivors with a short L have their forced key read in the standard and KRYPTOS alphabets and matched against the vocabulary and K1-K3 windows. Bounds: complete for these widths, lengths and alphabets.

## Prediction

No width up to 13 survives under any alphabet pair, because a row full of cribs disagrees. Widths above 13 survive only where no row holds two cribs with different shifts, and then only for key lengths that avoid pairing the two crib runs; no forced key matches a word. Zero candidates pass.

## Method

1. Build the alphabet pool.
2. For each plain alphabet, cipher alphabet and mode, compute the forced key index at each crib.
3. For each width w, group cribs by row and reject on disagreement within a row.
4. For surviving widths, for each key length L, group rows by L and reject on disagreement.
5. Read surviving forced keys in the standard and KRYPTOS alphabets; match against the vocabulary.

## Result

Candidates returned: 0. Passed all gates: 0. Best crib hits among all candidates: 0/24
(no candidates).
Best loss: None (0 is solved; 10 per missed crib letter). Best fitness: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| - | no candidates | | | | |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "grid with one key letter per row, rows cycling through a key word",
 "widths": "2-48",
 "key_lengths": "1-48",
 "alphabets": 63,
 "modes": 3,
 "cases": 559629,
 "widths_surviving_row_test": {},
 "smallest_width_surviving": null,
 "survivors_by_key_length": {},
 "vocab_matches": 0
}
```

Notes: 559629 (alphabet pair, mode, width) cases. Widths surviving the row test: []. Survivors by key length (first 12): {}. 0 matches.


