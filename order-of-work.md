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
| 1st | F1 one keyed stage, no move | strong: K1 and K2 are Quagmire III on KRYPTOS; Sanborn's "slightly different" tableau (C27c) | F1.5 (design 2); F1.6-F1.10: a carved letter wrong through the exact tests, autokey and Carter on a free alphabet, the per-letter progressive key, Friedman's key-advance schedules | medium | **next** (reopened, P6) |
| 2nd | F6 a move, then the table | strong: Sanborn's "matrix codes... then went back to this table" (C1) | F6.3b, F6.5; F6.6-F6.15: move-change-move, two tables round a move, keyed triples, autokeys on 0084's routes, keyed blanks, new transpositions (disrupted, triangle, EVA, Chiffre XIII, Nihilist), YAR's 1-2-3; F6.1, F6.2 if F1.5 reaches power | low to medium | reopened (P6) |
| 3rd | F12 Stein's way: look, quantify, then crib | strong precedent: the only hand solution of K1-K3 (Stein, 1998, 400 hours, pencil; Studies in Intelligence 1999); Stein on K4: "interesting patterns in here as well" | F12.1-F12.7: check the letters on the copper, K4's statistics against shuffles, his m = 13 anomaly, a pencil session, parts with their own keys, probable words | low | queued (added 2026-10-16, issue #53) |
| 4th | F3 two-part key with a combiner | medium: Scheidt's "key word/s" (C5), his CKM habit | F3.1 (with the patent's sandwich), F3.2, F3.3; F3.4-F3.7: stacked tables, misspelt-letter positions, the Weltzeituhr ring, "point" | low | queued |
| 5th | F2 masked plaintext | medium: Scheidt "masked the English language" | loose ends from 0057; nulls placed by a rule | low | queued; mostly blocked |
| 6th | F4 Sanborn's visual systems | medium, vague | F4.1 the route through the plates; F4.2-F4.5: trifid above period 15, physical anomalies, the extra L as a marker, Antipodes | medium | queued |
| 7th | F10 alphabets that change after every letter | weak to medium: no creator remark; Chaocipher (1918) was offered to US agencies and kept secret until 2010; A9, A10 | F10.1 Chaocipher, F10.2 Wheatstone cryptograph, F10.3 deck-of-cards key stream | low to medium | queued (added 2026-10-16, issue #51) |
| 8th | F11 agency hand systems, now public | weak to medium: Scheidt's CIA cryptographic background; Scheidt's "key word/s" (C5) for the poem code; A9 | F11.1, F11.2; F11.3 the CIA's Polish key box, F11.4 Friedman's keyed alphabet box | low to medium | queued (added 2026-10-16, issue #51) |
| 9th | F8 Hill | weak: the HILL column only (C21) | F8.1: count the equations for Hill with an unknown numbering; 5x5 affine has no checks | low | queued (F8.1 added, issue #55) |
| 10th | F5 Gromark | weak: no creator remark | F5.1; F5.2: three-term Gromark on a free alphabet in other bases | low | nearly closed |
| 11th | F9 substitution, then a move | against it: Sanborn's NYPVTT to BERLIN mapping | F9.1: a bounded list of hand transpositions outside the 1.86M built routes | medium | queued (reopened, P6) |
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
| Progressive key | closed | exact for the periodic step forms tried | 0011, 0042 | per-letter form and periods 26-30 not covered: F1.9 (pivot audit 2026-10-16 (issue #55)) |
| Ciphertext autokey, any lag, on 1,092 keyword tables (63 vocabulary, 102 K1-K3 words, 925 near-KRYPTOS, 42 compass words); a free alphabet is F1.7 | closed | exact | 0002, 0025, 0064, 0118 | - |
| Plaintext autokey, lags 1-52 | closed | exact | 0003, 0012 | - |
| Plaintext autokey, lags 53-96 | blocked | exact bound (0136) | 0012, 0136 | lags 85-96 blocked for good: the primer's open bits exceed what 73 letters of English can carry even at Shannon's lowest entropy (0136); lags 53-84 exceed the quadgram scorer's 130 bits, so only a better English model than the harness has could decide them |
| Running key from K1-K3, the sculpture's texts, Carter, Sanborn's letters (Carter on fixed and one keyword-mixed table only; Carter on a free alphabet is F1.8) | closed | exact | 0004, 0017, 0021, 0045, 0047, 0078, 0098, 0117 | - |
| Running key from an unknown English text, standard, KRYPTOS or puzzle-word alphabets | closed as far as testable | sampled; best forced stretch equals the coppers | 0009, 0010 | - |
| **F1.1** Free alphabet, the same on both sides (Quagmire III with unknown order), periods 3-26 | **blocked** (closed exact where testable) | exact for the added form at 1-26 and the Beaufort form at 1-22, 24, 25 (0119); Beaufort 23 sampled at low power (plants above every copper 3 of 6, none recovered; K4 inside the coppers, below 10 of 12, 0120); Beaufort 26 one check | 0097, 0100, 0102, 0119, 0120 | Beaufort 23 (7 checks) and 26 (1 check) fit on K4 as on most coppers; only an English climb could go further, and 0120 showed no climb at this size recovers a planted text, so any test would be weak. Blocked 2026-10-16 (issue #14) |
| **F1.2** Two free alphabets (Quagmire IV), periods 3-26 | **blocked** (closed exact where testable) | exact: no pair fits at 1-7, 9-12, 14, 15, 17, 18, 21, 22, 25 (0123); power per length stated in 0123 | 0097, 0121-0124 | the 8 consistent lengths (8, 13, 16, 19, 20, 23, 24, 26) leave only an English climb, which 0120 showed has weak or no power even with one alphabet. Length 19 fit is rare (26 of 1,000 coppers, 0124): noted, not a signal |
| **F1.3** Forced key stretches read as running English on the 208,062 dictionary alphabets | closed | sampled at stated power: K4 best -4.94, inside 50 coppers (-5.28 to -4.30) and below all 20 planted running keys (-3.82 to -4.78); 11 of 20 plants beat every copper | 0010, 0125 | - |
| **F1.5** A decider for cells the known letters cannot decide. Shared blocker of F1.1 (Beaufort 23, 26), F1.2 (lengths 8, 13, 16, 20, 23, 24, 26), F1.4 on free alphabets, plaintext autokey lags 53-96, F6.1, F6.2 and F8's undecided Hill settings | **open** | - | 0120 (the climb that failed) | Step 1, exact and cheap: for each blocked cell, count the key's bits (alphabets, free key slots, move) against the redundancy of the 73 unknown letters (Shannon's figure for English, source stated). A cell above the bound cannot be decided by any English test and is blocked for good, with the number. Step 2, for cells under the bound, starting with F1.1 Beaufort 23: design a climb that fixes 0120's stated failure (a single swap moved the forced key values in every slot) by moving only between alphabets that keep the 24 known letters consistent, and measure it on planted texts before K4. Power bar: 0120's pre-registered rule, a plant counts as found when its best score is above every copper, and a length is decidable when at least half the plants are found. Step 3: if a design passes, re-open each cell it covers as an open item in its own family's table and work them in rank order. Stop rule (proposed by Claude, issue #50; adopted 2026-10-16, Alexis delegated the decision): after two pre-registered designs fail the bar, F1.5 is blocked with both designs recorded |
| **F1.4** Hand key schedules other than the Berlin clock and Carter dates | closed on the standard and KRYPTOS tables; free-alphabet residue blocked | exact. List (NOTEBOOK 2026-10-16): tableau rows as keys (C20(d)); skip, stutter, back and forth, triangle, square, restart per carved line; C20(c) done by 0017/0090/0117; C20(e) K5 blocked (no text). No rule fits K4 on those tables; on free alphabets consistent at the coppers' rate (0127 rank 6 of 31) | 0126, 0127, 0128 | - |
| **F1.6** One carved letter wrong, missing or extra, run through the exact unknown-alphabet tests (F1.1, F1.2), then the other exact verdicts on free alphabets (Gromark 0069, 0076, 0107; Hill 0105; trifid 0040). F1.1's added form, K1 and K2's own system, dies only on S under S at 33 and K under K at 74 | **open** | - | 0093, 0094 did the move library only | exact, cheap: 24 x 25 substitutions at the known places, about 150 insertions and deletions outside them; first piece of A1 (pivot audit 2026-10-16 (issue #55), D1) |
| **F1.7** Autokey on one unknown alphabet: ciphertext autokey at every lag with a free primer, plaintext autokey at the lags with paired known letters, solved exactly as 0098; first with no move, then after each type-1 move | **open** | - | 0025, 0064, 0071, 0072 (keyword tables only), 0081, 0098 | the NSA's 1992 guess (C11a) on K1/K2's system; exact; cheap without a move (pivot audit 2026-10-16 (issue #55), D2) |
| **F1.8** Carter's book as a running key on one unknown alphabet (both directions, every offset, three rules), with 0098's exact solver; for every running-key source, count whether two unknown alphabets leave any checks | **open** | - | 0021, 0047, 0090, 0098 (left Carter out) | exact; about three hours with coppers, split over two runs (pivot audit 2026-10-16 (issue #55), D3) |
| **F1.9** The per-letter progressive key on keyword-mixed and dictionary tables; the progressive key's surviving periods 26-30 judged against coppers; a step of 3 per cycle at periods 31-52 (the Kryha machine's stepping, Lewis; low) | **open** | - | 0011, 0042 | exact for the form, sampled for 26-30 (pivot audit 2026-10-16 (issue #55), D8) |
| **F1.10** Friedman's keyword-only key-advance schedules (MC III, TM 11-485): run length set by the key letter's value, the CHRISTMAS expansion, the ciphertext interruptor, then the fraction-digit runs (TM 32-220 par. 126e) and the plaintext interruptor; also TM 32-220's EXTINGUISHER windows (par. 126d: overlapping three-letter sections of the keyword, each used for as many letters as the keyword's numbering says), one exact test per dictionary word (addendum `research_notes/Scheidt patents and field ciphers/addendum_downloaded_manuals.md` (issue #9)). One alphabet per long section is dead by inspection (N and O at 26-27 both under Q) | **open** | scratch checks only: no dictionary word fits the first two on the standard or KRYPTOS tables, the interruptor fits nothing there (227,485 words; no controls) | - | rerun the scratch checks as an experiment with coppers and close them; test the fraction digits (denominators 3-99) and the plaintext interruptor; free-alphabet versions go to F1.5's cells. Note: the adjacent known pairs 26-27, 33-34 and 68-69 can never share an alphabet, which kills per-word keying by inspection (report `reports/Scheidt patents and field ciphers.md` (issue #9)) |
| **F1.11** A split key phrase (Elementary Military Cryptography par. 59d, "CENTRAL AMERICA"): the first part mixes the plain alphabet, the second the cipher alphabet, the whole phrase is the repeating key | **open** | - | 0123 rules out every length but 8, 13, 16, 19, 20, 23, 24, 26 | phrases of those lengths from the vocabulary and K1-K3; deterministic per phrase, exact (addendum `research_notes/Scheidt patents and field ciphers/addendum_downloaded_manuals.md` (issue #9)) |

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
| **F6.6** Move, change, move again: a move, a periodic key on the standard or KRYPTOS table, then a second move | **open** | - | - | exact by consistency as orders A and B; cheap for a library of grid turns and K3's rule, expensive for every pair of moves (directions.md type 1, dropped after P3; pivot audit 2026-10-16 (issue #55), D4) |
| **F6.7** Change, move, change with the two keyed stages on different tables (standard then KRYPTOS, or the reverse) | **open** | - | 0080 used the same table on both sides | exact by backtracking over the first key; medium (pivot audit 2026-10-16 (issue #55), D5) |
| **F6.8** Three-stage routes with a keyword columnar stage (vocabulary or K1-K3 words) among the stages, then the table | **open** | sampled at 15 percent (0037) | 0037, 0083, 0134 | exact; expensive (about 10^8 triples even for 61 words): split or bound first (pivot audit 2026-10-16 (issue #55), D6) |
| **F6.9** Both autokeys with 0084's double columnar routes (one stage width 7 in all 5,040 orders) | **open** | - | 0084, 0085 | exact; medium (pivot audit 2026-10-16 (issue #55), D11) |
| **F6.10** Padded grids whose blank cells are chosen by a key (under the first or last letters of a keyword's column order), then the table | **open** | - | 0082, 0135 (eight fixed places only) | exact; cheap with vocabulary words (pivot audit 2026-10-16 (issue #55), D12) |
| **F6.11** Keyword-disrupted and triangle columnar transpositions (Rijmenants; the triangle's column numbering as TM 32-220 par. 87 gives it), then the table | **open** | - | - | add to the type-1 library; periodic key 1-26 on standard or KRYPTOS tables; 0119's decider for a free table (report `reports/Scheidt patents and field ciphers.md` (issue #9)) |
| **F6.12** EVA (Czech exile, WWII): two triangle tables growing two cells a row under one numbering; for 97 letters n = 10, a 19-letter keyword, three empty cells; then the table | **open** | - | - | dictionary 19-letter words and phrases; periodic key 1-26 (report `reports/Scheidt patents and field ciphers.md` (issue #9)) |
| **F6.13** Chiffre XIII's keyword-shaped five-row mask (rows 2 and 4 partial, row 4 shifted), then its period-5 shifted mixed alphabet | **open** | - | period 5 after built moves dead on free alphabets (F6.1, F6.2) | the mask is the new part: masks from long keywords and sentences; 0119's decider for the period-5 table (report `reports/Scheidt patents and field ciphers.md` (issue #9)) |
| **F6.14** Nihilist transposition on a 10 x 10 square with three blanks, one key for rows and columns | **open**, low | - | - | 10! orders x blank placements from F6.4's rules; periodic key 1-26 (report `reports/Scheidt patents and field ciphers.md` (issue #9)) |
| **F6.15** Sanborn's reported "1-2-3" spacing of the raised YAR as an ordering (C22(d)) | **open** | - | - | state the orderings it gives; each as a move, then the table (from the clue register) |
| **F6.16** Interrupted-key columnar transposition (TM 32-220 par. 89c-e): rows of irregular length set by the keyword's numbers or a fraction's digits, then the table | **open** | - | - | add to the type-1 library; periodic key 1-26 on standard or KRYPTOS tables (addendum `research_notes/Scheidt patents and field ciphers/addendum_downloaded_manuals.md` (issue #9)) |
| **F6.17** Trapezoid transposition (TM 32-220 par. 86), then the table | **open** | - | - | as F6.16 (addendum `research_notes/Scheidt patents and field ciphers/addendum_downloaded_manuals.md` (issue #9)) |
| **F6.18** Letters reshuffled inside each row by a keyword at widths other than 7 (TM 32-220 pars. 89a-b, 134f), then the table | **open** | - | 0070 did width 7 only | every width 2-48 with vocabulary keywords; exact (addendum `research_notes/Scheidt patents and field ciphers/addendum_downloaded_manuals.md` (issue #9)) |
| **F6.19** The French diagonal method (TM 32-220 par. 88), then the table | **open**, low | - | - | needs a prearranged choice of diagonals: enumerate the choices first (addendum `research_notes/Scheidt patents and field ciphers/addendum_downloaded_manuals.md` (issue #9)) |

## F12. Stein's way: look, quantify, then crib

Added 2026-10-16 (issue #53). Not a cipher type but a way of working: what David Stein, who
solved K1-K3 by hand in 1998, would do with a few free weeks and today's record. Source:
`knowledge/sources/stein-1999-cracking-the-courtyard-crypto.txt`. He looked before he attacked
("I seemed to see different patterns throughout, but I wanted to quantify these impressions"),
split the text where its statistics changed, read the plaintext for hints about the method, and
when the statistics ran out, guessed probable words. Items F12.2 and F12.4 produce
observations, not verdicts: each observation that stands outside the shuffles becomes a new item,
in this family or the one it points to.

| Item | Status | Strength | Experiments | Next test or reason |
|---|---|---|---|---|
| **F12.1** The 97 letters and the "?" checked against images of the copper (he walked out to feel UNDERGRUUND) | **open** | - | - | compare the transcription letter by letter with `research_notes/sanborn_charts/Panel4Grid.jpg`, the Blender model and any photographs in `knowledge/sources`; list every letter that is doubtful; if the images are too coarse, say so and mark blocked until Alexis supplies better ones (A4, A1) |
| **F12.2** Quantify the impressions: K4's statistics by segment and by width (letter counts per segment, I.C. against period 1-48 as in his Figure 26, positional patterns at widths 7, 21, 31), each against 1,000 shuffles | **open** | - | 0056 measured two of the patterns | report only what falls outside the shuffles, with the multiple-comparison count stated; a break inside K4 goes to F12.5 |
| **F12.3** His I.C. peak at m = 13 in both K1 and K2 (C28): real or chance | **open** | - | 0005, 0011 tested period 13 on K4 only | compare K1's and K2's I.C. at 13 against shuffles of each that keep their keyword period; if real, state what overlaid structure it implies and test K4 for it |
| **F12.4** A pencil session: K4 written out at the widths that matter, the known letters marked, every pattern noted before any search code ("the process of discovery is often intuitive as well as analytic") | **open** | - | - | write the observations up as a figure page; each goes to F12.2's shuffle test; each survivor becomes an item |
| **F12.5** Parts with their own keys (A7): K4 split where F12.2 or F12.4 finds a break, or at the known stretches, each part with its own periodic key on the standard or KRYPTOS tables | **open** | - | - | exact; fewer checks per part, so state the checks each split leaves |
| **F12.6** Probable words, his breakthrough (THE, then KNOW): common English words and the words of K1-K3's plaintexts placed at every position in the cells the 24 known letters cannot decide (F1.1 Beaufort 23 and 26, F1.2's consistent lengths, F6.1, F6.2) | **open** | - | 0095 dragged riddle words at the live periods only | each placement adds checks, so a cell can become decidable without an English model; count consistent placements on K4 against coppers, exact |
| **F12.7** His K1-K3 method as such: every shift of each column written out, columns scored by summed log letter frequencies, then a crib | **open** | - | - | for periodic keys on the standard and KRYPTOS tables the exact sweeps (0005) already cover it; confirm and close by subsumption with that reason |

## F3. Two-part key with a combiner

| Item | Status | Strength | Experiments | Next test or reason |
|---|---|---|---|---|
| Two words added, both from the puzzle, or one from the dictionary | closed | exact | 0014, 0043, 0059, 0115 | - |
| A word plus digits from the story (coordinates, dates, counts) | closed | exact | 0024, 0038 | - |
| A word plus the misspelt or raised letters | closed | exact | 0061 | - |
| Column word plus row key | closed | exact | 0087, 0088 | - |
| **F3.1** Combiners other than addition (subtraction both ways is done; table lookup through a second alphabet, multiplication mod 26). First the sandwich from Scheidt's patent US 6,075,865: c = T2[T1[p + a] + b], two key streams on either side of a fixed keyed alphabet, T1 and T2 from {standard, KRYPTOS, their inverses}, periods up to about 13 each (report `reports/Scheidt patents and field ciphers.md` (issue #9)) | **open** | - | - | exact, cheap |
| **F3.2** Numeric second parts from the Morse (E counts) and the plate layout (line lengths) | **open** | - | 0038 did 17 readings | list the readings, test each exactly |
| **F3.3** Direction words as numbers (A14(b)): east-northeast as a bearing (67.5 degrees: 6, 7, 5 or 67, 5), as compass point 6 of 32 or 3 of 16, and the same for EAST and NORTHEAST, as a numeric second part beside a word | **open** | - | 0072 tried direction words as keyword alphabets only | list the readings, test each exactly as F3.2 |
| **F3.4** Three or more stacked tables (US 6,075,865 with N = 3; Sanborn's "triple matrixes") | **open** | - | 0043, 0059 (two passes) | the F3.1 sandwich decider with three tables over {standard, KRYPTOS} (report `reports/Scheidt patents and field ciphers.md` (issue #9)) |
| **F3.5** The misspelt letters' positions as indices (Q in IQLUSION, U in UNDERGRUUND, A in DESPARATLY, the missing E, the raised YAR), and their orientation read literally (RQ as YR) (C10(a), C10(c)) | **open** | - | 0061 used the letters, not their positions | list the index readings, test each exactly (from the clue register) |
| **F3.6** The Weltzeituhr's rotating ring as an offset over 26 letters (C12(b)): 24 zones, the ring's rotation through the day | **open** | - | 0052 excluded a 24-letter alphabet only | list the offsets it gives, test as keys exactly (from the clue register) |
| **F3.7** "Point" read as the decimal point in K2's "six point five", as the place on the grounds, or as a punctuation mark (C15(b)-(d)) | **open** | - | 0072 did compass points and the letter's words | list the numeric and positional readings, test exactly; the place reading is blocked without a survey (from the clue register) |

## F2. Masked plaintext

| Item | Status | Strength | Experiments | Next test or reason |
|---|---|---|---|---|
| Reversal, regular nulls, prefix nulls, affine masks, doublets as nulls, nulls by letter | closed | exact | 0023, 0057, 0074, 0075 | - |
| Message written along grid paths | closed | exact | 0092 | - |
| **F2.1** Forced fragments at periods 24-25 after letter strike-outs not matched against words | **open** | gap in 0057 | 0057 | match them against the dictionary; cheap |
| **F2.2** Nulls placed by a rule (after every X, after each crib word) | **open** | - | - | exact, cheap |
| **F2.3** A plain component written from a phrase with repeated letters, so a letter can be enciphered by any of its places: homophones that keep the length | **open** | - | - | the agent's derivation from EMC par. 45b, not a documented method: state it as such; test phrase components from the vocabulary, the known letters as set membership (addendum `research_notes/Scheidt patents and field ciphers/addendum_downloaded_manuals.md` (issue #9)) |
| A code layer, phonetic spelling, another language | blocked | - | - | changes the letters at the known places or needs a codebook we lack |

## F4. Sanborn's visual systems

| Item | Status | Strength | Experiments | Next test or reason |
|---|---|---|---|---|
| Trifid, any cube, periods 2-15 | closed | exact | 0040 | periods above 15 are F4.2 |
| The plates as a key by position, straight or folded | closed | exact | 0089 | - |
| Read from behind the screen | closed | exact | 0108 | - |
| **F4.1** A route that follows the plates' physical layout (the S-curve, the 31-letter lines as a grid with K3's last line) | **open** | - | - | build the route set from the Blender model, then test as F6 |
| **F4.2** Free trifid cubes at periods above 15 | **open** | - | 0040 (2-15), 0033 (keyword cubes to 20) | constraint propagation as 0040; cheap (pivot audit 2026-10-16 (issue #55), D10) |
| **F4.3** The positions of the sculpture's physical anomalies as a key (C3(c)) | **open** | - | - | list the anomalies and their positions from `01-facts.md` and the model; test as positional keys (from the clue register) |
| **F4.4** The extra L and the HILL row as a marker matching YAR on the lower-left plate (C21(b)) | **open** | - | - | state what the marker would select (a row, a start, a key letter); test each exactly (from the clue register) |
| **F4.5** Antipodes' differences: the plate order "shifted a little" and the UUND/RTBJ spelling (C26) | **open** | - | - | the shifted plate order as a reading order or key; the spelling difference as a key fragment (from the clue register) |

## F10. Alphabets that change after every letter

Added 2026-10-16 (issue #51). Every family above uses a fixed alphabet with a changing key
(assumption A10, `knowledge/12-assumptions.md`). These keep the letter-for-letter link the
known letters need, and can be worked by hand.

| Item | Status | Strength | Experiments | Next test or reason |
|---|---|---|---|---|
| **F10.1** Chaocipher: two alphabet wheels permuted after every letter (Byrne, 1918; method disclosed 2010) | **open** | - | - | count first how many checks the 24 known letters give: the wheels' state depends on every earlier letter, so the known stretches may constrain only through the unknown letters before them; if they leave too few checks, this needs the F1.5 decider and is blocked like F1.1 |
| **F10.2** Wheatstone cryptograph or Alberti disk advanced by the plaintext: a 26-letter ring against a 27-place ring, the pointer moved by the distance between plaintext letters (Wheatstone, 1867) | **open** | - | - | exact: inside each known stretch consecutive known letters constrain the mixed ring directly; enumerate or propagate, then compare with coppers |
| **F10.3** A key stream from a deck of cards (Solitaire 1999, Mirdek 2000) | **open** | - | - | the deck order is far larger than 24 known letters can pin down; state the bound and mark blocked unless a published known-plaintext attack applies |

## F11. Agency hand systems, now public

Added 2026-10-16 (issue #51). The method had only to be known to its creators in 1990
(assumption A9); Scheidt chaired the CIA's Cryptographic Center until 1989. Systems that turn
letters into digits or Morse (VIC, straddling checkerboards, fractionated Morse, Nihilist) are
left out while the letter-for-letter reading of the known letters holds (A2).

| Item | Status | Strength | Experiments | Next test or reason |
|---|---|---|---|---|
| **F11.1** Strip ciphers and cylinders with published alphabets: M-94's 25 discs, the Jefferson wheel, M-138-A strips where published | **open** | - | - | exact: disc or strip order and row offset; the community tried M-94 only with hill climbs (`knowledge/05-attacks.md`), so no bounded result exists |
| **F11.2** Poem code: a double transposition keyed by words from a memorized text (SOE), then the table | **open** | - | - | build long keys from consecutive and chosen words of the sculpture's texts and K1-K3; extend F6's double columnar test to them, exact |
| **F11.3** The CIA's own 1970s Polish agent system (Bury, Cryptologia 2007): a key text written row by row into a box and read out by columns, then a reciprocal 26 x 26 table | **open** | scratch check: K1-K3 as the key text, 1,388,268 settings, best 7 of 24 (chance; no controls) | - | rerun with coppers; then Carter and Sanborn's letters as key texts, keyword-ordered column reads, a free table (report `reports/Scheidt patents and field ciphers.md` (issue #9)) |
| **F11.4** Friedman's keyed alphabet box (MC III 35b): the alphabet written n times in a rectangle, read out by a keyword's column order as the key stream | **open** | - | - | deterministic per dictionary word and n on the standard and KRYPTOS tables; a partition test on free tables (report `reports/Scheidt patents and field ciphers.md` (issue #9)) |

## F8 Hill, F5 Gromark, F9 substitution then a move

| Item | Status | Strength | Experiments | Reason |
|---|---|---|---|---|
| Hill 2-5, plain and affine, 330 numberings (4 standard, 126 vocabulary, 200 K1-K3 words; an unknown numbering is F8.1), chained, with a periodic key | closed, except what had too few equations: 5x5 affine (14 of 20 settings undecided, 0105) and 400 of 936 Hill-plus-key settings, mostly 4x4 with long keys (0116) | exact where decided | 0015, 0036, 0044, 0055, 0105, 0116 | the undecided settings are blocked: no checks. Reopen if F1.5 reaches power and the bound in its step 1 allows |
| **F8.1** Hill 2x2 and 3x3 with an unknown letter numbering (any of 26!) | **open** | - | 0015, 0044, 0055, 0105, 0116 | count equations against unknowns first; if too few, blocked with the number (pivot audit 2026-10-16 (issue #55), D9) |
| Gromark, two- and three-term rules, bases 2-26 (three-term on a free alphabet in base 10 only; other bases are F5.2) | closed | exact | 0013, 0028, 0046, 0054, 0069, 0076, 0107 | - |
| **F5.1** Multiplicative feedback; the raised YAR as primer | open, low value | - | - | no creator remark points here |
| **F5.2** Three-term Gromark on a free alphabet in bases 2-9, 11-16 and 26; two-term free-alphabet rules beyond lag 6 (base 10) and 5 (other bases) | **open** | - | 0046, 0069, 0076, 0107 | exact; cheap (0107 ran in 50 s) (pivot audit 2026-10-16 (issue #55), D7) |
| One-to-one substitution, then any route in the built sets (1.86M) | closed | exact | 0019, 0106 | - |
| Routes outside every built set | blocked | - | - | unbounded without a hand-method list; F9.1 writes that list |
| **F9.1** Hand transpositions outside the built route sets | **open** | - | 0019, 0106 | write the list first, from the reference shelf (issue #9) and the methods a 1990 hand cipher could use, each with its sizes, as F1.4 and F6.4 did; drop what the 1.86M built routes already cover; then one-to-one substitution after each, exact, as 0106 |
