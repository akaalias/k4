# Priorities

After 118 experiments none has beaten the scrambled coppers. Following up on a result needs a
result that beats chance, and there has been none, so the work is a sweep. From here on the
sweep follows a fixed order, set before any further run:

1. Families are worked in the rank order below. Within a family, open items are taken from the top.
2. A family is left only when every item in its table is `closed` or `blocked`:
    - `closed` means an exact test, or a sampled test with scrambled-copper controls at stated
      power, rules the item out.
    - `blocked` means it cannot be tested with the 24 known letters alone, for example because
      it needs a source text we lack or it leaves no checks. The reason is written down.
3. Reverts no longer force a pivot. A revert that closes an item is progress.
4. Every experiment names the item it works on (for example "F1.2") and the strength it
   reached: exact, sampled or weak. A weak test leaves the item open.
5. A result outside the scrambled-copper range stops the queue. It is replicated against
   fresh controls before anything else, as 0100 was by 0102.
6. The ranking changes only at a family boundary, with the reason in the pivot log.

Per-experiment grades (outcome, strength, whether the known letters were fitted by
construction) are in `grades.tsv`.

## Ranking

| Rank | Family | Clue support | What is left | Cost of what is left | Status |
|---|---|---|---|---|---|
| 1st | F1 one keyed stage, no move | strong: K1 and K2 are Quagmire III on KRYPTOS; Sanborn's "slightly different" tableau (C27c) | F1.5: a decider for the cells the known letters cannot decide; if it reaches power, F1.1, F1.2 and the other cells it covers reopen (P6) | medium | **next** (reopened, P6) |
| 2nd | F6 a move, then the table | strong: Sanborn's "matrix codes... then went back to this table" (C1) | F6.3b: mixed triples at widths 25-96, only sampled so far; F6.1, F6.2 if F1.5 reaches power | low to medium | reopened (P6) |
| 3rd | F3 two-part key with a combiner | medium: Scheidt's "key word/s" (C5), his CKM habit | combiners other than addition; numeric second parts not yet tried | low | queued |
| 4th | F2 masked plaintext | medium: Scheidt "masked the English language" | loose ends from 0057; nulls placed by a rule | low | queued; mostly blocked |
| 5th | F4 Sanborn's visual systems | medium, vague | routes through the plates as a path, not as a key | medium | queued |
| 6th | F8 Hill | weak: the HILL column only (C21) | 5x5 affine has no checks | none testable | blocked |
| 7th | F5 Gromark | weak: no creator remark | multiplicative feedback, the raised YAR as primer | low | nearly closed |
| 8th | F9 substitution, then a move | against it: Sanborn's NYPVTT to BERLIN mapping | F9.1: a bounded list of hand transpositions outside the 1.86M built routes | medium | queued (reopened, P6) |
| - | F7 construction simulation | a tool, not a cipher | run before each family's first open item: does its construction make both fingerprints? | low | standing step |

Why this order: F1 and F6 rest on the two most direct creator statements. Both were tested
almost entirely on the standard, KRYPTOS and puzzle-word alphabets. An unknown alphabet is the
largest axis not yet covered, and it costs less with no move (F1) than after one (F6). F3 and
F2 come next because their remaining items are cheap. The rest are closed or blocked except
for low-value residues.

Reopened 2026-10-16 (P6, issue #50): most blocked items were blocked for one shared reason, that
no test can judge a cell the known letters leave undecided. F1.5 works on that reason directly. Two
more were blocked only because nobody had written their list (F6.3b, F9.1). Items blocked by missing
information (K5's text, a codebook) stay blocked.

## F1. One keyed stage, no move

| Item | Status | Strength | Experiments | Next test or reason |
|---|---|---|---|---|
| Periodic key, standard or KRYPTOS alphabets, periods 1-26 and 30-52 | closed | exact | 0005, crib sweep | - |
| Periods 27-29 and 53+ on any alphabet pair the puzzle's words build | closed | exact consistency; the key completion is noise against coppers | 0034, 0035, 0048, 0053 | - |
| Periodic key on alphabets from any dictionary word | closed | exact | 0109 | - |
| Progressive key | closed | exact | 0011, 0042 | - |
| Ciphertext autokey, any lag, any alphabet tried | closed | exact | 0002, 0025, 0064, 0118 | - |
| Plaintext autokey, lags 1-52 | closed | exact | 0003, 0012 | - |
| Plaintext autokey, lags 53-96 | blocked | exact bound (0136) | 0012, 0136 | lags 85-96 blocked for good: the primer's open bits exceed what 73 letters of English can carry even at Shannon's lowest entropy (0136); lags 53-84 exceed the quadgram scorer's 130 bits, so only a better English model than the harness has could decide them |
| Running key from K1-K3, the sculpture's texts, Carter, Sanborn's letters | closed | exact | 0004, 0017, 0021, 0045, 0047, 0078, 0098, 0117 | - |
| Running key from an unknown English text, standard, KRYPTOS or puzzle-word alphabets | closed as far as testable | sampled; best forced stretch equals the coppers | 0009, 0010 | - |
| **F1.1** Free alphabet, the same on both sides (Quagmire III with unknown order), periods 3-26 | **blocked** (closed exact where testable) | exact for the added form at 1-26 and the Beaufort form at 1-22, 24, 25 (0119); Beaufort 23 sampled at low power (plants above every copper 3 of 6, none recovered; K4 inside the coppers, below 10 of 12, 0120); Beaufort 26 one check | 0097, 0100, 0102, 0119, 0120 | Beaufort 23 (7 checks) and 26 (1 check) fit on K4 as on most coppers; only an English climb could go further, and 0120 showed no climb at this size recovers a planted text, so any test would be weak. Blocked 2026-10-16 (issue #14) |
| **F1.2** Two free alphabets (Quagmire IV), periods 3-26 | **blocked** (closed exact where testable) | exact: no pair fits at 1-7, 9-12, 14, 15, 17, 18, 21, 22, 25 (0123); power per length stated in 0123 | 0097, 0121-0124 | the 8 consistent lengths (8, 13, 16, 19, 20, 23, 24, 26) leave only an English climb, which 0120 showed has weak or no power even with one alphabet. Length 19 fit is rare (26 of 1,000 coppers, 0124): noted, not a signal |
| **F1.3** Forced key stretches read as running English on the 208,062 dictionary alphabets | closed | sampled at stated power: K4 best -4.94, inside 50 coppers (-5.28 to -4.30) and below all 20 planted running keys (-3.82 to -4.78); 11 of 20 plants beat every copper | 0010, 0125 | - |
| **F1.5** A decider for cells the known letters cannot decide. Shared blocker of F1.1 (Beaufort 23, 26), F1.2 (lengths 8, 13, 16, 20, 23, 24, 26), F1.4 on free alphabets, plaintext autokey lags 53-96, F6.1, F6.2 and F8's undecided Hill settings | **open** | - | 0120 (the climb that failed) | Step 1, exact and cheap: for each blocked cell, count the key's bits (alphabets, free key slots, move) against the redundancy of the 73 unknown letters (Shannon's figure for English, source stated). A cell above the bound cannot be decided by any English test and is blocked for good, with the number. Step 2, for cells under the bound, starting with F1.1 Beaufort 23: design a climb that fixes 0120's stated failure (a single swap moved the forced key values in every slot) by moving only between alphabets that keep the 24 known letters consistent, and measure it on planted texts before K4. Power bar: 0120's pre-registered rule, a plant counts as found when its best score is above every copper, and a length is decidable when at least half the plants are found. Step 3: if a design passes, re-open each cell it covers as an open item in its own family's table and work them in rank order. Stop rule (proposed by Claude, issue #50, for Alexis to confirm): after two pre-registered designs fail the bar, F1.5 is blocked with both designs recorded |
| **F1.4** Hand key schedules other than the Berlin clock and Carter dates | closed on the standard and KRYPTOS tables; free-alphabet residue blocked | exact. List (NOTEBOOK 2026-10-16): tableau rows as keys (C20(d)); skip, stutter, back and forth, triangle, square, restart per carved line; C20(c) done by 0017/0090/0117; C20(e) K5 blocked (no text). No rule fits K4 on those tables; on free alphabets consistent at the coppers' rate (0127 rank 6 of 31) | 0126, 0127, 0128 | - |

## F6. A move, then the table

| Item | Status | Strength | Experiments | Next test or reason |
|---|---|---|---|---|
| Columnar (plain, keyed, double), K3's rule, quarter turns, grid paths, rail fence, AMSCO, Myszkowski, then a periodic key on standard, KRYPTOS or word alphabets | closed | exact | 0006-0008, 0026, 0058, 0080-0086, 0099, 0110-0114 | - |
| The same moves with autokey, running key or clock schedules | closed | exact | 0063, 0081, 0090, 0091 | - |
| Three stages | closed | exact for clockwise triples at 2-96 (0083) and every mix of four column readings, triples at widths 2-24 and pairs at 2-96 (0134) | 0037, 0083, 0134 | **F6.3** done: nothing live below 20, at the coppers' rate; mixed triples at widths 25-96 are F6.3b |
| **F6.3b** Mixed triples of the four column readings at widths 25-96 | **open** | sampled only (0037, 200,000 triples, graded chance, issue #26) | 0037 | enumerate exactly as 0134 did at 2-24; estimate the count and run time first, and if it does not fit the budget, split it over runs or say so and grade it sampled at stated power |
| One carved letter wrong, missing or extra, through the move library | closed | exact | 0093, 0094 | - |
| AMSCO at period 23 after the move: 15 distinct check sets against 1-9 on the coppers | noted, not chased | exact | 0114 | within the 4.7 of 52 cells expected outside the range by chance; replicate only if F6 reaches AMSCO again |
| **F6.1** Free alphabet (Quagmire III) after or before each move, periods 3-26 | **blocked** (closed exact where testable) | exact: every type-1 move, both orders, both forms, lengths 1-26; no fit below 6; fitting cells at the coppers' rate (0129: 7 of 52 cells above every copper, null 0-8; 0130: 0, null 0-10) | 0097, 0129, 0130 | the fitting settings leave only an English climb, which has no power here (0120); blocked like F1.1. Reopens if F1.5 reaches power |
| **F6.2** Two free alphabets after or before each move | **blocked** (closed exact where testable) | exact at 1-10 for every move, both orders, with undecided counted; per-slot refutation at 11-26 (0133); 97-99% of per-slot survivors fit at 11-26 (0131, 0132); K4 above every copper in 5 of 52 cells, null 2-7 | 0097, 0131, 0132, 0133 | fitting settings leave only an English climb (0120); order A length 3 (16 against 1-12) is 0102's marginal cell, inside chance by the fixed rule. Reopens if F1.5 reaches power |
| **F6.4** Padding applied separately at each grid stage; nulls dropped between griddings | closed | exact: the hand padding rules listed in NOTEBOOK 2026-10-16 (blanks in 8 places per grid, dropped or kept as dummies), one stage at widths 2-96, two at 2-48, periodic key 1-26 either side, 874,572 routes; nothing live below 21, at the coppers' rate (0135) | 0082, 0135 | - |
| **F6.5** Direction words as routes through the grid (A14(a), C16(c): "directions" as instructions): "east, then northeast" and the other compass readings as reading paths (along rows, then up the diagonals; and each of the 16 points as a direction of travel), at every width, then a periodic key on the standard or KRYPTOS tables | **open** | - | - | add the routes to the move library and test as F6's first row, exact; cheap |

## F3. Two-part key with a combiner

| Item | Status | Strength | Experiments | Next test or reason |
|---|---|---|---|---|
| Two words added, both from the puzzle, or one from the dictionary | closed | exact | 0014, 0043, 0059, 0115 | - |
| A word plus digits from the story (coordinates, dates, counts) | closed | exact | 0024, 0038 | - |
| A word plus the misspelt or raised letters | closed | exact | 0061 | - |
| Column word plus row key | closed | exact | 0087, 0088 | - |
| **F3.1** Combiners other than addition (subtraction both ways is done; table lookup through a second alphabet, multiplication mod 26) | **open** | - | - | exact, cheap |
| **F3.2** Numeric second parts from the Morse (E counts) and the plate layout (line lengths) | **open** | - | 0038 did 17 readings | list the readings, test each exactly |
| **F3.3** Direction words as numbers (A14(b)): east-northeast as a bearing (67.5 degrees: 6, 7, 5 or 67, 5), as compass point 6 of 32 or 3 of 16, and the same for EAST and NORTHEAST, as a numeric second part beside a word | **open** | - | 0072 tried direction words as keyword alphabets only | list the readings, test each exactly as F3.2 |

## F2. Masked plaintext

| Item | Status | Strength | Experiments | Next test or reason |
|---|---|---|---|---|
| Reversal, regular nulls, prefix nulls, affine masks, doublets as nulls, nulls by letter | closed | exact | 0023, 0057, 0074, 0075 | - |
| Message written along grid paths | closed | exact | 0092 | - |
| **F2.1** Forced fragments at periods 24-25 after letter strike-outs not matched against words | **open** | gap in 0057 | 0057 | match them against the dictionary; cheap |
| **F2.2** Nulls placed by a rule (after every X, after each crib word) | **open** | - | - | exact, cheap |
| A code layer, phonetic spelling, another language | blocked | - | - | changes the letters at the known places or needs a codebook we lack |

## F4. Sanborn's visual systems

| Item | Status | Strength | Experiments | Next test or reason |
|---|---|---|---|---|
| Trifid, any cube | closed | exact | 0040 | - |
| The plates as a key by position, straight or folded | closed | exact | 0089 | - |
| Read from behind the screen | closed | exact | 0108 | - |
| **F4.1** A route that follows the plates' physical layout (the S-curve, the 31-letter lines as a grid with K3's last line) | **open** | - | - | build the route set from the Blender model, then test as F6 |

## F8 Hill, F5 Gromark, F9 substitution then a move

| Item | Status | Strength | Experiments | Reason |
|---|---|---|---|---|
| Hill 2-5, plain and affine, any numbering, chained, with a periodic key | closed, except what had too few equations: 5x5 affine (14 of 20 settings undecided, 0105) and 400 of 936 Hill-plus-key settings, mostly 4x4 with long keys (0116) | exact where decided | 0015, 0036, 0044, 0055, 0105, 0116 | the undecided settings are blocked: no checks. Reopen if F1.5 reaches power and the bound in its step 1 allows |
| Gromark, two- and three-term rules, any alphabet, bases 2-26 | closed | exact | 0013, 0028, 0046, 0054, 0069, 0076, 0107 | - |
| **F5.1** Multiplicative feedback; the raised YAR as primer | open, low value | - | - | no creator remark points here |
| One-to-one substitution, then any route in the built sets (1.86M) | closed | exact | 0019, 0106 | - |
| Routes outside every built set | blocked | - | - | unbounded without a hand-method list; F9.1 writes that list |
| **F9.1** Hand transpositions outside the built route sets | **open** | - | 0019, 0106 | write the list first, from the reference shelf (issue #9) and the methods a 1990 hand cipher could use, each with its sizes, as F1.4 and F6.4 did; drop what the 1.86M built routes already cover; then one-to-one substitution after each, exact, as 0106 |
