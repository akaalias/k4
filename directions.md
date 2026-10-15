# Directions to work off, in order

Decided with Alexis on 2026-10-15, after 79 experiments. Built on the differences between K1-K3
(K1/K2 change letters with the table and a key word; K3 moves letters by turning grids) and on the
creators' remarks. Work them in order, 1 then 2; check each against the prior-work database before running:
`reports/Kryptos K4 prior attempts database.md` (deep research, 2026-10-15, issue #25).

| # | Type | Evidence | Already ruled out by us | Open |
|---|---|---|---|---|
| 1 | K1-style changing combined with K3-style moving | Sanborn: "double matrixes and triple matrixes... then went back to this table"; Scheidt: more than one stage | keyed column shuffles + periodic key (fam. 6); K3 counting rule + periodic key (0008) | grid turns on incomplete grids (97 is prime: the ? before OBKR or nulls as padding); move, change, move again |
| 2 | Sevens | width-7 doublet column and width-21 repeats are real (0056); only ciphertext autokey at lag 1 with a 7-letter key reproduces the column (0065); KRYPTOS has 7 letters; 21 = 3 x 7 | CT autokey + periodic key (0066); block-of-7 reshuffles (0070, 0077) | 7-block constructions with feedback keyed by KRYPTOS or another 7-letter word |
| 3 | Keys read off the sculpture | Scheidt: "key word/s"; the object carries extra letters and text | misspelling letters as a short key (0061); K2 coordinates as Hill (0060); Berlin clock (0079) | the table's extra L and HILL column; Morse on the granite (T IS YOUR POSITION, VIRTUALLY INVISIBLE, SHADOW FORCES, LUCID MEMORY); compass rose and lodestone |
| 4 | A masking step on the plaintext | Sanborn: "masking technique" | reversal, regular nulls, decimations and Atbash (0023, 0057, 0074) | a code layer; spelled-out letters; plaintext written in boustrophedon, spiral or columns |
| 5 | The table read differently | the table reads mirrored from inside the curl; Scheidt: "mirrors and obfuscation"; Sanborn: "slightly different tableau" | tables one swap or move from KRYPTOS (0071) | the table by columns or diagonals, mirrored, starting from another row |
| 6 | A hand key schedule | Scheidt: "simple, can be remembered" | Berlin clock (0079), Carter dates (0038) with a repeating key only | the same schedules combined with a moving stage (type 1) |
| 7 | A carving error in K4 | K2 has one; K1-K3 carry deliberate misspellings | one letter off through autokey and two-word tests (0031, 0050, 0068) | one letter off through types 1 and 2 |
| 8 | A plaintext that is itself a riddle | K2 spells out coordinates and ends LAYER TWO | none | scoring credit for spelled numbers and the puzzle's words (issue #11) |

## What the prior-work database changed (2026-10-15)

- Type 1: closed by others: every single and double K3-style rotation at widths 2-96 with a repeating
  tableau key, both orders, ragged last row and 0-11 padding letters (keithadler, nitsuah); K1/K2's
  methods chained with K3's rotation in all six orders (Zekios); columnar in every order at widths
  2-14 plus a periodic key. Still open: padding applied separately at each grid stage; the short row
  at the top; blanks in key-chosen cells; nulls dropped between the two griddings; rotation with
  plaintext autokey; substitute, rotate, substitute again with a second key; an exhaustive triple
  rotation (our 0037 only sampled); two unknown alphabets at periods 13-26.
- Type 2: closed by others: every simple seven-based construction (period 7/14/21 keys, KRYPTOS as
  key or 7-letter autokey primer, width-7 columnar in all 5,040 orders with periodic, autokey or
  running key, width-7 seriated Playfair). Still open: keyed double columnar with one width of 7
  (every public repo skipped it); columnar plus autokey above width 7; any construction that makes the
  doublet column and the cribs together.
- The two fingerprints are suggestive, not evidence: 0056's p of about 0.005 should be about 0.02-0.03
  when compared only against shuffles that also have six doublets, and lower still once the other
  scanned statistics are counted. Type 2 is a lead worth a few runs, not a priority on statistics alone.
- Bean (HistoCrypt 2021) argues statistically that K4 has no transposition stage; Sanborn's "double
  matrixes... then went back to this table" argues for one. Type 1 runs should state which they test.
- No disclosure of the method exists as of October 2026. K5 reportedly shares "some coded words in the
  same positions" with a "similar but not identical" system: if same words at same places encrypt the
  same, the cipher is keyed by position, which would count against autokey and chaining (an inference;
  the sources are ambiguous).
