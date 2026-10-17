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
| 1st | F1 one keyed stage, no move | strong: K1 and K2 are Quagmire III on KRYPTOS; Sanborn's "slightly different" tableau (C27c) | nothing testable within budget: residues blocked by the English bound (0136) or by cost (F1.4, F1.7) | - | done (P7, 2026-10-17): every item closed or blocked |
| 2nd | F6 a move, then the table | strong: Sanborn's "matrix codes... then went back to this table" (C1) | nothing testable within budget: F6.1, F6.2 blocked by cost; the full type-1 library squared for F6.6 not run | low to medium | done (P8, 2026-10-17): every item closed or blocked |
| 3rd | F12 Stein's way: look, quantify, then crib | strong precedent: the only hand solution of K1-K3 (Stein, 1998, 400 hours, pencil; Studies in Intelligence 1999); Stein on K4: "interesting patterns in here as well" | nothing testable here: F12.1 needs photographs of the copper | - | done (P9, 2026-10-17): F12.1 blocked, F12.2-F12.7 closed |
| 4th | F3 two-part key with a combiner | medium: Scheidt's "key word/s" (C5), his CKM habit | F3.1 (with the patent's sandwich), F3.2, F3.3; F3.4-F3.7: stacked tables, misspelt-letter positions, the Weltzeituhr ring, "point" | low | **next** (P9) |
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
| Progressive key | closed | exact for the periodic step forms tried; per-letter form and periods 26-52 on every dictionary table in F1.9 (0155) | 0011, 0042, 0155 | - |
| Ciphertext autokey, any lag, on 1,092 keyword tables (63 vocabulary, 102 K1-K3 words, 925 near-KRYPTOS, 42 compass words); a free alphabet is F1.7 | closed | exact | 0002, 0025, 0064, 0118 | - |
| Plaintext autokey, lags 1-52 | closed | exact | 0003, 0012 | - |
| Plaintext autokey, lags 53-96 | blocked | exact bound (0136) | 0012, 0136 | lags 85-96 blocked for good: the primer's open bits exceed what 73 letters of English can carry even at Shannon's lowest entropy (0136); lags 53-84 exceed the quadgram scorer's 130 bits, so only a better English model than the harness has could decide them |
| Running key from K1-K3, the sculpture's texts, Carter, Sanborn's letters (Carter on fixed and one keyword-mixed table only; Carter on a free alphabet is F1.8) | closed | exact | 0004, 0017, 0021, 0045, 0047, 0078, 0098, 0117 | - |
| Running key from an unknown English text, standard, KRYPTOS or puzzle-word alphabets | closed as far as testable | sampled; best forced stretch equals the coppers | 0009, 0010 | - |
| **F1.1** Free alphabet, the same on both sides (Quagmire III with unknown order), periods 3-26 | closed | exact for the added form at 1-26 and the Beaufort form at 1-22, 24, 25 (0119); Beaufort 23 and 26 sampled at measured power: F1.5's decider (design 2) puts K4 9th of 13 (23) and 12th of 13 (26) among copies of itself; planted texts beat all their own copies 6 of 8 (23, 0139) and 5 of 6 (26, 0140) | 0097, 0100, 0102, 0119, 0120, 0139, 0140, 0142 | - |
| **F1.2** Two free alphabets (Quagmire IV), periods 3-26 | closed where English can decide; blocked above the bound | exact: no pair fits at 1-7, 9-12, 14, 15, 17, 18, 21, 22, 25 (0123); 8, 13, 16 sampled at measured power: K4 2nd, 13th and 7th of 13 among kept-place copies (0146, 0144); power 4/4, 5/5, 4/5 (0145, 0143) | 0097, 0121-0124, 0143-0146 | 19, 20, 23, 24, 26 blocked by 0136's bound: the key's open bits exceed what the quadgram scorer can read in 73 letters (only a better English model could decide). Length 19 fit is rare (26 of 1,000 coppers, 0124): noted, not a signal |
| **F1.3** Forced key stretches read as running English on the 208,062 dictionary alphabets | closed | sampled at stated power: K4 best -4.94, inside 50 coppers (-5.28 to -4.30) and below all 20 planted running keys (-3.82 to -4.78); 11 of 20 plants beat every copper | 0010, 0125 | - |
| **F1.5** A decider for cells the known letters cannot decide | closed | step 1 exact (0136: bound per cell); step 2 two designs: design 1 (check-keeping climb, 0137) failed its validity check against each plant's own copies (0138: 6/12, bar 9); design 2 (parallel tempering in the check-keeping set, compiled) passed (0139: 6/8; also 0140, 0143, 0145 at other cells), then decided F1.1 and F1.2's cells (0140, 0142, 0144, 0146) | 0120, 0136-0146 | the rule learned: power is measured against each planted text's own scrambled copies, never the target's (0138). Covered cells too costly to run one by one are listed in their own rows (F1.4, F1.7, F6.1, F6.2) |
| **F1.4** Hand key schedules other than the Berlin clock and Carter dates | closed on the standard and KRYPTOS tables; free-alphabet residue blocked by cost | exact. List (NOTEBOOK 2026-10-16): tableau rows as keys (C20(d)); skip, stutter, back and forth, triangle, square, restart per carved line; C20(c) done by 0017/0090/0117; C20(e) K5 blocked (no text). No rule fits K4 on those tables; on free alphabets consistent at the coppers' rate (0127 rank 6 of 31) | 0126, 0127, 0128 | the free-alphabet residue (555 one-alphabet and 1,346 two-alphabet settings consistent on K4) is decidable in principle (0136) and F1.5's decider exists, but each setting costs a power test plus K4 against 12 copies (about 20-30 min): about 900 hours. Blocked by cost, not by principle |
| **F1.6** One carved letter wrong, missing or extra, run through the exact unknown-alphabet tests, then the other exact verdicts on free alphabets | closed (one cell blocked, weak) | exact: periodic one and two free alphabets, 604 variants (0147: K4 above every copper in 2 of 78 cells, null 0-11); Gromark 0069/0076/0107, 605 variants: no fit (0150); trifid, 5,044 variants anywhere: no cube (0151); Hill, 5,044 variants: 257 alive with one check, rank 4 of 11 against copies (0151, 0152) | 0147, 0148, 0150, 0151, 0152 | the one cell 0147 revived by meaning, K1/K2's added form at length 19 with the carved S at 33 a slip, failed the decider's power bar (0148: 3/5, bar 4; one plant recovered exactly): blocked, weak |
| **F1.7** Autokey on one unknown alphabet | closed with no move where dead; fitting lags and the move version blocked by cost | exact (0149): ciphertext and plaintext autokey, three forms, every lag with equations; K4 fits 9-23 lags per kind and form, copies 3-30; rare fits 4 against 0-27 | 0149 | fitting lags (about 100 cells) need F1.5's decider at about an hour each; the move-first version is about 176 million exact searches. Blocked by cost |
| **F1.8** Carter's book as a running key on one unknown alphabet (both directions, every offset, three rules); for every running-key source, whether two unknown alphabets leave any checks | closed (one alphabet); two alphabets blocked by structure | exact (0154): no offset fits K4 or any of 10 copies; 953 of about 1.7 million undecided at the node limit (copies 99-20,675). Two alphabets: the 24 equations leave 0.1 checks on average, at most 4, for Carter, K2, K3 and the cipher panel | 0153 (error), 0154 | two unknown alphabets with a running key cannot be decided by the known letters |
| **F1.9** Progressive key, per-letter and per-repeat, on keyword-mixed and dictionary tables; periods 26-30 against coppers; Kryha's step 3 at 31-52 | closed | exact (0155): 1,040,314 tables x 2 forms x steps 1-25 x periods 1-52; shortest consistent period 25 (copies 24); K4 above every copper in 4 of 104 cells, null 0-5 | 0155 | period 34 noted (K4 40 and 20 consistent pairs against copier maxima 10 and 7), inside the fixed statistic, not chased |
| **F1.10** Friedman's keyword-only key-advance schedules (run length by value, CHRISTMAS, EXTINGUISHER windows, ciphertext and plaintext interruptors, fraction digits) | closed | exact (0156) with 10 copies: no dictionary word fits any word schedule on K4 or the copies; ciphertext interruptor and fraction digits 0 on K4 (copies 0-14); plaintext interruptor inside the runs 160 against 120-7,165 | 0156 | free-alphabet versions are F1.4's residue (blocked by cost) |
| **F1.11** A split key phrase (Elementary Military Cryptography par. 59d) | closed | exact (0157): 29,880 phrases (puzzle-word pairs, K1-K3 word runs split at each boundary) x 3 numberings x 3 rules: best 7 of 24 known letters on K4, copies 7-8, no full hit | 0157 | - |

## F6. A move, then the table

| Item | Status | Strength | Experiments | Next test or reason |
|---|---|---|---|---|
| Columnar (plain, keyed, double), K3's rule, quarter turns, grid paths, rail fence, AMSCO, Myszkowski, then a periodic key on standard, KRYPTOS or word alphabets | closed | exact | 0006-0008, 0026, 0058, 0080-0086, 0099, 0110-0114 | - |
| The same moves with autokey, running key or clock schedules | closed | exact | 0063, 0081, 0090, 0091 | - |
| Three stages | closed | exact for clockwise triples at 2-96 (0083) and every mix of four column readings, triples at widths 2-24 and pairs at 2-96 (0134) | 0037, 0083, 0134 | **F6.3** done: nothing live below 20, at the coppers' rate; mixed triples at widths 25-96 are F6.3b |
| **F6.3b** Mixed triples of the four column readings at widths 25-96 | closed | exact (0158): 105,548,253 distinct routes (compiled, checked against Python); shortest consistent key 18 after (copies 19), 24 before (17); K4 above every copper in 3 of 52 cells, null 0-3 | 0037, 0158 | one setting at 18 (col 93, cw 65, cw 84; KRYPTOS table, Beaufort) noted |
| One carved letter wrong, missing or extra, through the move library | closed | exact | 0093, 0094 | - |
| AMSCO at period 23 after the move: 15 distinct check sets against 1-9 on the coppers | noted, not chased | exact | 0114 | within the 4.7 of 52 cells expected outside the range by chance; replicate only if F6 reaches AMSCO again |
| **F6.1** Free alphabet (Quagmire III) after or before each move, periods 3-26 | **blocked** (closed exact where testable) | exact: every type-1 move, both orders, both forms, lengths 1-26; no fit below 6; fitting cells at the coppers' rate (0129: 7 of 52 cells above every copper, null 0-8; 0130: 0, null 0-10) | 0097, 0129, 0130 | blocked by cost: a decider with measured power exists (F1.5, design 2), but K4 fits about 443,000 (move, length) settings at 20-30 min each (power test plus K4 against copies); reopen only with a cheaper decider |
| **F6.2** Two free alphabets after or before each move | **blocked** (closed exact where testable) | exact at 1-10 for every move, both orders, with undecided counted; per-slot refutation at 11-26 (0133); 97-99% of per-slot survivors fit at 11-26 (0131, 0132); K4 above every copper in 5 of 52 cells, null 2-7 | 0097, 0131, 0132, 0133 | lengths 15-26 blocked by 0136's bound; 3-14 blocked by cost as F6.1 (tens of thousands of fitting settings) |
| **F6.4** Padding applied separately at each grid stage; nulls dropped between griddings | closed | exact: the hand padding rules listed in NOTEBOOK 2026-10-16 (blanks in 8 places per grid, dropped or kept as dummies), one stage at widths 2-96, two at 2-48, periodic key 1-26 either side, 874,572 routes; nothing live below 21, at the coppers' rate (0135) | 0082, 0135 | - |
| **F6.5** Direction words as routes through the grid | closed | exact (0159): the 16 compass points as reading directions at every width, lines either way, and E/ENE/NE in two stages: 110,820 routes; shortest consistent key 21 after, 25 before, as the copies; 1 of 52 cells, null 0-1 | 0159 | - |
| **F6.6** Move, change, move again | closed for a library of 844 moves | exact (0160): column readings at every width and K3's rule at every multiplier, both directions; all 712,336 ordered pairs; shortest consistent key 20 (copies 18); 1 of 26 cells, null 0-2 | 0160 | the full type-1 library squared (776 million pairs) would need the composition compiled; not run |
| **F6.7** Change, move, change with the two keyed stages on different tables | closed | exact (0161): standard then KRYPTOS or the reverse, keys 2-14 each, 844 moves, propagation over the one-to-one links; consistent with 5+ checks K4 388, copies 300-504; every level inside | 0161 | one 9-check setting (inverted two-row turn at width 84, keys 13 and 13) noted; copies' 9-check count not recorded |
| **F6.8** Three-stage routes with a keyword columnar stage | closed | exact (0162): 131 distinct keyword columnars (puzzle, K1-K3 words) and 92 plain readings (widths 2-24), every triple with a keyword stage: 20,370,476 routes; shortest consistent key 20 after, 24 before, as the copies; 0 of 52 cells | 0037, 0083, 0134, 0162 | - |
| **F6.9** Both autokeys with 0084's double columnar routes | closed | exact (0163): 3,284,523 routes x lags 1-96 x after/before x ciphertext/plaintext autokey x std/KRYPTOS x 3 rules; survivors with 5+ checks K4 0, 9, 1, 0 against copies 0-8, 5-21, 0-1, 0-480 | 0084, 0085, 0163 | - |
| **F6.10** Padded grids whose blank cells are chosen by a key | closed | exact (0165): blanks under the first or last key numbers in the last or first row, 181,308 keywords, 1,450,196 routes; shortest consistent key 21 after, 25 before (copies 20, 24); 0 of 52 cells | 0082, 0135, 0165 | - |
| **F6.11** Keyword-disrupted and triangle columnar transpositions | closed | exact (0164): disrupted columnar 327,440 routes, TM 32-220 triangle (19 columns, blanks at end or start) 654,876 routes, 163,720 keywords; shortest consistent keys 23 / 24 (copies 22 / 24); 0 and 1 of 52 cells | 0164 | free-table version not run: after a move free alphabets fit at the copies' rate (F6.1) |
| **F6.12** EVA double triangle | closed | exact (0166): 1,920 19-letter keys (K1-K3 windows, dictionary, puzzle pairs); no key up to 26 after the move on K4 or copies, 25 before as the copies | 0166 | - |
| **F6.13** Chiffre XIII's five-row mask, then its period-5 shifted mixed alphabet | closed | exact (0166), as a parametric family: the source does not give the rule for rows 2 and 4, so every split and row-4 shift for 6,296 keys of 24-31 letters (2,248,512 masks), then the published substitution on an unknown alphabet decided exactly: no mask consistent with 3+ checks on K4 or any copy | 0166 | the documented mask rule (forms 5-9) would need the primary text (scz.bplaced.net §10.1) |
| **F6.14** Nihilist transposition on a 10 x 10 square with three blanks | closed | exact (0167): all 10! keys x 8 blank places x row or column reading x both directions = 116,121,600 routes; shortest consistent key 20 after, 24 before (copies 18, 17); 0 of 52 cells | 0167 | - |
| **F6.15** Sanborn's "1-2-3" spacing of the raised YAR as an ordering | closed | exact (0166): counting off 1-2-3 and 4-5-7 (YAR's places in ENDYAHR) in every order around the text; nothing up to 26 after, 26 before, as the copies | 0166 | other readings of "1-2-3" (C22(d)) not specified by the source |
| **F6.16** Interrupted-key columnar transposition | closed | exact (0164): rows cut by the keyword's numbering (163,720 keywords) or by the digits of 1/d (puzzle words): 332,817 routes; shortest consistent key 23 after (copies 21), 25 before (24); 1 of 52 cells, null 0-3 | 0164 | - |
| **F6.17** Trapezoid transposition | closed | exact (0164): base = keyword length, rows one shorter going up on either side, fewest blanks: 89,708 routes; shortest consistent key 26 after, 25 before (copies 23, 24); 0 of 52 cells | 0164 | - |
| **F6.18** Letters reshuffled inside each row by a keyword at widths other than 7 | closed | exact (0165): widths 2-48 (dictionary and puzzle words; K1-K3 windows for 25-48), 361,698 routes; shortest consistent key 21 after, 25 before (copies 21, 24); 2 of 52 cells, null 0-2 | 0070, 0165 | - |
| **F6.19** The French diagonal method | closed (key-named diagonals) | exact (0165): the diagonals from the tops of the columns numbered 1 to j first, then columns by key order (j up to the key length for puzzle words, 1-3 for dictionary words): 2,264,476 routes; shortest consistent key 22 after, 24 before (copies 20, 24); 1 of 52 cells | 0165 | diagonal sets not named by the key would be an extra agreement with no source: not tested |

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
| **F12.1** The 97 letters and the "?" checked against images of the copper (he walked out to feel UNDERGRUUND) | blocked | no image of the K4 section at letter resolution in the repository (Panel4Grid is a blurred video frame; the Blender model needs Blender); the NYT 2010 typeset clue agrees with the transcription; needs photographs from Alexis | - | photographs of the copper at letter resolution (A4, A1) |
| **F12.2** Quantify the impressions: K4's statistics by segment and by width (letter counts per segment, I.C. against period 1-48 as in his Figure 26, positional patterns at widths 7, 21, 31), each against 1,000 shuffles | closed | sampled (0168): 71 statistics fixed before the run, each against 1,000 shuffles; nothing outside every shuffle (0.14 expected); smallest p the width-7 doublets (0.002), as 0056 | 0168 (before: 0056 measured two of the patterns) | - |
| **F12.3** His I.C. peak at m = 13 in both K1 and K2 (C28): real or chance | closed | sampled (0169): K1 p 0.0075 against 10,000 shuffles within its key columns, about 0.019 allowing for the strand counts scanned (post hoc); Part II 0.24, K4 0.21: chance, nothing overlaid | 0169 (before: 0005, 0011 tested period 13 on K4 only) | - |
| **F12.4** A pencil session: K4 written out at the widths that matter, the known letters marked, every pattern noted before any search code ("the process of discovery is often intuitive as well as analytic") | closed | sampled (0170): six patterns noted by eye at widths 7-31; none outside 1,000 shuffles; two at p 0.004, found by looking; no new item | 0170 | - |
| **F12.5** Parts with their own keys (A7): K4 split where F12.2 or F12.4 finds a break, or at the known stretches, each part with its own periodic key on the standard or KRYPTOS tables | closed | exact (0171): split between the runs (no break found), each part its own key up to 12 and 10 on 8 table classes; no length fits K4 (copies 0-1 cells) | 0171 | - |
| **F12.6** Probable words, his breakthrough (THE, then KNOW): common English words and the words of K1-K3's plaintexts placed at every position in the cells the 24 known letters cannot decide (F1.1 Beaufort 23 and 26, F1.2's consistent lengths, F6.1, F6.2) | closed | exact (0172): 60 words x 3,634 placements in the ten undecided cells; K4 above every copy in 1 of 10 cells, copies 0-3: chance; F6.1 and F6.2 have no cells to place words in (blocked by cost) | 0172 (before: 0095 dragged riddle words at the live periods only) | - |
| **F12.7** His K1-K3 method as such: every shift of each column written out, columns scored by summed log letter frequencies, then a crib | closed | by subsumption, no run: 0005's exact sweeps cover every periodic key on the standard and KRYPTOS tables, which is what the column method finds; the live lengths fit coppers equally (0034) | 0005, 0034 | - |

## F3. Two-part key with a combiner

| Item | Status | Strength | Experiments | Next test or reason |
|---|---|---|---|---|
| Two words added, both from the puzzle, or one from the dictionary | closed | exact | 0014, 0043, 0059, 0115 | - |
| A word plus digits from the story (coordinates, dates, counts) | closed | exact | 0024, 0038 | - |
| A word plus the misspelt or raised letters | closed | exact | 0061 | - |
| Column word plus row key | closed | exact | 0087, 0088 | - |
| **F3.1** Combiners other than addition (subtraction both ways is done; table lookup through a second alphabet, multiplication mod 26). First the sandwich from Scheidt's patent US 6,075,865: c = T2[T1[p + a] + b], two key streams on either side of a fixed keyed alphabet, T1 and T2 from {standard, KRYPTOS, their inverses}, periods up to about 13 each (report `reports/Scheidt patents and field ciphers.md` (issue #9)) | closed | exact: the patent sandwich (0173), 108 table classes, key lengths 1-13 each: nothing fits K4 at the 161 length pairs with 4 or more checks (copies at most 2 in 1,000); the 8 pairs with both keys 10-13 leave 1-2 checks and are blocked; two words added on 61 mixed numberings or multiplied mod 26 (0174): no consistent case on K4 or copies | 0173, 0174 | - |
| **F3.2** Numeric second parts from the Morse (E counts) and the plate layout (line lengths) | closed | exact (0175): 26 readings (Morse E runs and totals in two transcriptions, the line lengths and their departures from 31, K4 line and column on the copper), each value one key number, with an unknown word of 1-24 on 12 table rules: nothing fits K4 or 20 copies | 0175 (before: 0038 did 17 digit readings) | - |
| **F3.3** Direction words as numbers (A14(b)): east-northeast as a bearing (67.5 degrees: 6, 7, 5 or 67, 5), as compass point 6 of 32 or 3 of 16, and the same for EAST and NORTHEAST, as a numeric second part beside a word | closed | exact (0176): 43 readings of east-northeast, east and northeast as degrees, digits, mils and compass points of 32 and 16, with an unknown word of 1-24 on 12 table rules: nothing fits K4 or 20 copies | 0176 (before: 0072 used direction words as keyword alphabets) | - |
| **F3.4** Three or more stacked tables (US 6,075,865 with N = 3; Sanborn's "triple matrixes") | closed | exact (0177): two KRYPTOS-order tables (or inverses) and three keys of 1-10, 144 classes: nothing fits K4 or copies where the known letters give 4 or more checks (780 length triples); 1-3 checks at the copies' rate, too weak | 0177 (before: 0043, 0059 two passes) | - |
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
