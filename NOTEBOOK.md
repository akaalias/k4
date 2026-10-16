# Lab notebook

One entry per working day, newest first. Each entry says what was decided, what was run,
what was found, and what was left open. Experiment numbers link to the records in
`experiments/`. The families table and the clue register hold the bounds; this notebook
holds the reasoning and the mistakes.

## 2026-10-16

Family F1 under the fixed order of work (order-of-work.md, issue #29), items F1.1 to F1.4, ticket #14.

| # | Item | One line |
|---|---|---|
| 119 | F1.1 | **One free alphabet on both sides, exact.** Every key length 1-26, any of 26! orders, decided exactly by algebra mod 13 and mod 2 with an exhaustive search of the mod-13 solutions: in the added form (Quagmire III proper, and variant Beaufort) no alphabet fits at any length; in the Beaufort form only 23 and 26 fit (7 and 1 checks left). Coppers fit at 0-15 and 1-11 lengths; K4 is at the low end of their range, not outside it. **Prediction failed:** it expected most lengths from 8 up to fit. |

Paragraph on 0119. The added form dies for a reason one can check by hand: S sits under S at 33 and K under K at
74, and with one alphabet on both sides and the key added, a letter that encrypts to itself needs key 0 in its slot.
At every key length from 1 to 26 another known letter shares the slot of 33 or 74 and is not its own carved letter,
so that slot would need key 0 and a non-zero key at once. This is new for free alphabets (0097 tested only lengths 3,
7 and 21, by a relaxation that can refute but not confirm). The first exact solver, a plain search with propagation,
blew up on the dead lengths (product of independent choices); it was replaced before the run by linear algebra mod
13 and mod 2 with an exhaustive search of the mod-13 solutions, and cross-checked on 40 coppers against the plain
search (no fit it found was called dead). The prediction, written before the solver existed, guessed "fewer checks
than free places, so most lengths fit"; it ignored that a one-to-one alphabet packs about 20 letters into 13 residue
classes mod 13, which the known letters make tight.

## 2026-10-15

Plan for the day: run to experiment 50. Priorities, in order: explain the three statistics
no generator reproduces (the width-7 doublet column, the eleven width-21 vertical repeats,
Bean's closeness), then the untouched families (2 masking, 4 visual), then the one-letter
error reruns of the strongest sweeps. Every diagnostic experiment gets ten or more shuffled
controls. The notebook gets a line per experiment as it lands.

Lesson from 0025: every sweep must check the clock inside its innermost loop that can run long; the harness budget is advisory, not a kill switch.

From 0037: a diagnostic's controls must run at the same trial count as the real search. The record's two controls used 6,000 triples against 200,000, which made a chance result look like a lead; thirteen full-size shuffles put it back inside the noise.

From 0027: the width-7 doublet column is reproduced by nothing, random letters included, so it is either a fluke of about one in 300 or the trace of a construction outside everything simulated. Doublets at 19, 26, 33, 47, 68 are all 5 mod 7; in a period-7 additive system a doublet is a plaintext digraph with a fixed letter difference falling in one column, which is a natural mechanism, but period 7 is dead under every alphabet by the cribs alone (R and C both to P at 66 and 73). Gromark base 2 reproduces the width-21 repeats; 0013 tested only bases 10 and 26, so bases 2 to 9 are 0028.

From 0033: simulated annealing over trifid cubes with crib hits, even at coordinate level, plateaus at about 17 of 24 on a planted cube. A proper trifid solver needs constraint propagation on the cube coordinates, not local search. Built as 0039 and 0040: the equalities plus the all-different rule leave no cube at all for K4, while planted texts are recovered. The lesson generalises: when a cipher's key is a structure the cribs constrain algebraically, solve, do not search.

From 0034: the loss function's key-cost term is too weak. A 95-letter random key with 71 free slots climbed to fit English gives a crib-perfect text that the harness scores at loss 4.4, below the crib gate, and keeps as champion. The text is overfitting, as the identical score on shuffled K4 shows. Per program.md the ruler is not changed mid-run: the case is in issue #11 for a human decision, and the champion stands as a warning until then. Also: the key alphabet does not affect decryption under a fixed plain and cipher alphabet, so the 24 conventions were 8 distinct classes here; the extra 16 were wasted time.

| # | Family | One line |
|---|---|---|
| 21 | 1 | Carter's book as a running key, 13.7 million offsets and conventions: none within two mismatches. |
| 22 | 1 | Porta over 248 alphabet orders: no order separates all 24 crib pairs across the halves. |
| 23 | 2 | Reversal and null padding before a periodic tableau, 648 masks: smallest live period 26; nothing. |
| 24 | 3 | A word plus the K2 coordinate digits, seven readings: shortest consistent word length 26; nothing. |
| 25 | 1 | Both autokeys with 63 keyword-mixed alphabets, 3.4 million cases: nothing; ran 46 minutes because the sweep ignored the clock. |
| 26 | 6 | Two keyed columnar stages from vocabulary word pairs, 15,376 routes, then the tableau: chance. |
| 27 | 7 | Simulator round two: only Gromark base 2 reproduces the width-21 repeats; nothing reproduces the width-7 doublet column. |
| 28 | 5 | Gromark bases 2-9: every vocabulary alphabet triple forces a shift of 15 or more, so bases up to 15 are dead. Clocks batched, so design and implement times are lost. |
| 29 | 1 | Bean's closeness over all alphabet pairs: smallest largest shift 8, same as shuffled K4. Chance. |
| 30 | 1 | Ciphertext as its own key under every index rule, and the message mirrored as key: nothing. |
| 31 | 1 | Copper off by one letter, 195 variants, through the chained autokey and two-word tests: nothing. |
| 32 | 6 | A grid keyed by row, widths 2-48, 63 alphabets: no width survives. |
| 33 | 4 | Trifid: keyword cubes best 7 of 24; the annealer plateaus at 17 even on a planted cube, so free cubes stay open. |
| 34 | 1 | Key completed by English climb at periods 27-29 and 53-95: K4 behaves exactly like shuffled K4. First gate-passing candidates; the harness kept a gibberish period-95 text as champion at loss 4.4. Scorer case filed. |
| 35 | 1 | Key completion at 27-29 with one vocabulary-mixed alphabet: noise, equal to shuffled K4. Design clock polluted by dashboard work, 19 min of it. |
| 36 | 8 | Bauer's open Hill variants, chained and paired, solved exactly: dead. |
| 37 | 6 | Three grid stages, 200,000 sampled triples: best key -3.61 against thirteen shuffles topping at -3.63. Chance by a whisker; the record's own controls were undersized, fixed after the run. |
| 38 | 3 | A word plus seventeen dates and counts from the story: shortest consistent word 26; nothing. |
| 39 | 4 | Trifid solved exactly: the run found no cube at any setting, then crashed writing its own summary. Record kept as an error. |
| 40 | 4 | Rerun of 39 with the summary fixed: no cube is consistent at any period 2-15, on K4 or on shuffled K4. Trifid dead. |
| 41 | 6, 9 | Spirals, snakes and diagonals at every width, both orders: chance before the table, clashes after a swap. |
| 42 | 1 | Progressive key on vocabulary tables, 8.9 million combinations: periods 1-24 dead at every step; nothing. Test clock includes 8 minutes of dry run. |
| 43 | 3 | Two words in two passes on vocabulary tables: nothing below total length 22; chance above. |
| 44 | 8 | Hill under 126 keyword numberings: 4x4 solutions exist without redundancy and all break the partial-block cribs. Dead. |
| 45 | 1 | K1-K3 as running keys on vocabulary tables, 147 million trials: nothing within two mismatches. |
| 46 | 5 | Gromark three-term rules, lags to 13, bases 16-26: nothing. |
| 47 | 1 | Carter and the sculpture texts as running keys with one mixed alphabet, 858 million trials: nothing. |
| 48 | 1 | Both alphabets mixed, key completion at 27-29, every pair reached: noise. Family 1 closed for vocabulary alphabets. |
| 49 | 1 | Shaped long keys from two puzzle words, mirrors and doublings, 272 of them under every alphabet pair: nothing. The record overestimated the key count by a hundredfold. |
| 50 | 3 | The copper off by one letter, through the two-word test on vocabulary tables: survivors at the shuffled-copper rate, nothing below total length 21. |
| 51 | 6 | Pure transposition: the cribs need three Es, the copper has two. Every rearrangement-only reading is dead at once. |
| 52 | 8 | Ciphers on a 5x5 square or a 24-letter ring: K4 uses all 26 letters and has odd length, so Playfair, bifid, four-square, ADFGVX and kin are dead whatever the key. The walkthrough misplaces I by one (17, not 16). |
| 53 | 1 | Periodic keys on tables rebuilt from every K1-K3 word and the 2025 letter's words: nothing. Period 26 runs high only because one equation, places 22 and 74, holds across many alphabets at once. |
| 54 | 5 | Gromark on tables rebuilt from K1-K3 words: every pair forces a shift of at least 16, as scrambled coppers do, so base 10 is out again. |
| 55 | 8 | Hill with letters numbered by alphabets from K1-K3 words: no 2x2 or 3x3 setting fits the known blocks; the 4x4 ones fit only for lack of checks and fail the remaining known letters. |
| 56 | 7 | **Prediction failed.** The width-7 doublet column and width-21 repeats survive the look-elsewhere correction: corrected p 0.005 (0.018 given six doublets) and 0.010 against 10,000 shuffles. Two real fingerprints still lack a construction. |
| 57 | 2 | Filler letters chosen by letter: no different from random strike-outs. Striking letters before BERLINCLOCK makes lengths 24-25 consistent at the chance rate, which the prediction did not foresee; their fragments were not word-checked. |
| 58 | 6 | The table, then a column shuffle keyed by K1-K3 words, once or twice: 355,008 route-convention pairs, a handful live at length 25 and no word fits. The prediction missed those 16, and no control measured their chance rate. |
| 59 | 3 | Two secret words in two passes on tables rebuilt from K1-K3 words: nothing below a combined length of 21, survivors above at chance rates, no word. |
| 60 | 8 | The K2 map reference poured into a Hill number table, every reading: at most 4 of 24 known letters, worse than random tables. |
| 61 | 3 | A puzzle word plus the misspelt letters (QUA, LOE) or the raised YAR as a second short key: best 8 of 24 known letters, no better than scrambled coppers. |
| 62 | 7 | Fake coppers by recipes with a 7 or a 21: none makes both marks. Ciphertext autokey at lag 21 makes the width-21 repeats 27 times more often than chance; nothing tried makes the doublet column. |
| 63 | 6 | Column shuffles before or after the self-feeding autokey: 14.2 million exact checks, no fit, best 9 of 24. |
| 64 | 1 | The self-feeding autokey on tables rebuilt from K1-K3 words, every distance: never closer than three wrong known letters, as scrambled coppers manage. |
| 65 | 7 | **Prediction failed in size.** Recipes built to line doublets up in sevens: only ciphertext autokey at lag 1 with a period-7 key raises the doublet column, to 1.5% of samples against 0.1-0.3% by chance, not the 5% predicted; the other six recipes stay at chance. |
| 66 | 1 | The self-feeding autokey plus a repeating secret word on top, every lag and word length, solved exactly: nothing survives with three or more checks; lag 1 with 7 (the doublet recipe) and lag 21 (the repeat recipe) are dead. The record's case count, 294,912, counts lags with no known letter past them; 221,184 were tested. |
| 67 | 1 | **Prediction failed in detail.** Two earlier carved letters as the key, every pair of distances, with or without a short word: 15 cases survive three checks against 3-12 on scrambled coppers, and one survives four (0-2). Listed after the run, the 16 are scattered with no pattern, and distances 1 and 21 never pass more than one check. Chance, but the record's own prediction said none. |
| 68 | 1 | The self-feeding autokey with one carved letter wrong, missing or extra: no variant at any lag passes three checks, lag 21 has no survivor at all, and the counts sit inside the scrambled coppers'. The substitution tally counts the residuals a replacement letter is fitted to as checks, overstating them by one or two. |
| 69 | 5 | Gromark with any scrambled alphabet at all, every rule up to six digits back and every primer: none fits the known letters, and none fits scrambled coppers; a planted Gromark text is found uniquely. Base-10 Gromark is dead whatever the alphabet. The record's primer count has a typo: 5,432,100, not 5,432,200. |
| 70 | 6 | Every row of seven reshuffled the same way, before or after a repeating secret word, all 5,040 orders: periods up to 24 die, 25-26 survive only as often as on scrambled coppers, and no forced fragment holds a word (checked after the run). Family 6 back to rest. |
| 71 | 1 | A table slightly different from the carved one, as Sanborn said his was: all 925 alphabets one swap or one move from KRYPTOS, with a repeating word or the self-feeding autokey: nothing beyond the scrambled-copper rate and no word in 16,671 fragments. The count was corrected from 975 to 925 before the run. |
| 72 | 1 | The 32 compass points and the words of Sanborn's 'what's the point?' letter as table alphabets, with a repeating word, the self-feeding autokey, or both: everything at the scrambled-copper rate, and no word in 10,671 fragments. |
| 73 | 1 | **Prediction failed in detail.** The message as its own key plus a repeating word: twelve cases pass three checks against 0-6 on scrambled coppers, but they are four coincidences counted at nested periods (ROWS and SEVENTY alphabets at lag 8, each at periods 5, 8, 10, 20, 40), none passes four, and the NSA's lag 7 and the fingerprint lag 21 have nothing. Chance. |
| 74 | 2 | Masks that change letters: the alphabet counted in steps of 3, 5, 7 ... or backwards (Atbash), on both alphabets, before or after a repeating word or the self-feeding autokey: nothing at three checks, periods up to 25 dead, no word. A one-check excess in the plain autokey comes from two-equation lags counted per key alphabet. |
| 75 | 2 | The doubled letters as fillers: QQ, SS and TT inside the known stretches each carry two different known letters, so they are real letters; striking out BB, the second SS or ZZ in any combination changes nothing for a repeating word or the self-feeding autokey. |
| 76 | 5 | Gromark with any scrambled alphabet in every base from 2 to 16 and in base 26 (Scheidt's other number systems, the Berlin clock's fives): no starting number fits in any base, on the copper or on scrambled coppers. Family 5 is closed for two-term rules. |
| 77 | 1 | The two fingerprints joined in one recipe, every row of seven reshuffled plus the self-feeding autokey at every distance, both orders, 31 million exact checks: all at the scrambled-copper rate, nothing passes four checks, and distance 21 never passes three. |
| 78 | 1 | Sanborn's own letters as a running key, the 1989 note to CIA staff, the 1991 dedication pages and the 2025 open letter, at every offset both ways: the best gets 9 of 24 known letters, exactly what scrambled coppers get. |
| 79 | 1 | The Berlin clocks as the key, lit lamps or hours or minutes or the digits of the time, the clock moving on a fixed step per letter from every start minute: the best fit agrees at 8 of 24 known letters, as scrambled coppers do. The prediction's guess of 19-20 mismatches was removed before the run, after a dry run on the copper showed 16; the verdict does not depend on it. |
| 80 | 6 | **Type 1, gap a3.** Change with one repeating word, move by K3's rule, a grid turn, two turns or a column shuffle (26,158 distinct routes), change again with a second word, key lengths 2-14 each, solved exactly: 4.4 million structures, nothing with five or more checks, counts at every level at the scrambled-copper rate. **Prediction failed in detail:** at exactly three checks the copper has 30 cases against 33-46 on the scrambled coppers,  
| 81 | 6 | **Type 1, gap a2.** The same 27,752 routes joined to the plaintext autokey (the NSA's 1992 guess) or the ciphertext autokey, both orders, every lag, one alphabet throughout: nothing passes five checks; counts at the scrambled-copper rate. **Prediction failed in detail:** four settings pass exactly four checks (three with the autokey first, against 0-2 on scrambled coppers), scattered over lags 33, 37 and 49 and wide odd turns; chance. | 
| 82 | 6 | **Type 1, gap a1.** Hand-padded grids: blanks at the start of the top row, or the first grid's blanks carried into the second as fillers and struck out at the end, for one and two quarter turns at every width and for short-row-on-top column shuffles (120,871 distinct routes), with a repeating key of length 1-26 before or after: no period below 22 is live on the copper or on any scrambled copper. **Prediction failed in detail:** with the key after the move, period 23 is live 299 times against 229-283 and period 24 2,166 against 1,289-2,160; checked after the run, the 299 are spread evenly over every padding choice and mostly over grids wider than 70, as on the scrambled coppers. Chance. | 
| 83 | 6 | **Type 1, gap a4.** Three quarter turns at every width 2-96 in each grid (1,714,024 distinct routes, forward and inverse), with a repeating key of length 1-26 after or before: counts at every period at the scrambled-copper rate. **Prediction failed in detail:** one setting is live at period 18 (widths 93, 65 and 84, key after the turns, KRYPTOS alphabet, Beaufort; six checks), where no scrambled copper has anything below 21. Examined after the run: the six checks fix all 18 key letters, VTYPETGCEVGYPLDEPG, no word, and the full decryption reads TQPFJTXZBUAKHSSPRGHQP... and scores -8.85, below noise. About 0.1 such coincidences are expected at six checks over 27 million settings; this is one. | 
| 84 | 6 | **Type 2, first open item.** Double column shuffle with one stage seven columns wide in all 5,040 orders, the other plain at widths 2-30 or keyed by a puzzle word (253 sequences), either stage first: 2,548,223 routes, repeating key 1-26 before or after: nothing live below 21; periods 21 (key after) and 24 (key before) live 3 times each against 0-2 on scrambled coppers. Chance. Building it found issue #26: ten records (0006-0081) passed a keyword's rank list as the column reading sequence, so their 'keyed columnar' read the columns in the inverse order; true keyword columnar was untested there. Also, the library's keyword order drops repeated letters (ABSCISSA reads as ABSCI); 0084 reads word keys both with repeats dropped and on the whole word, ties left to right. | 
| 85 | 6 | **Rerun for issue #26.** Column shuffles keyed by the puzzle's words read in true key order (201 sequences: repeats dropped, or the whole word with ties left to right), once in either direction or twice in every ordered pair (40,771 routes), with a repeating key 1-26 before or after and with both autokeys at every lag in both orders: nothing live below 22; nothing passes five checks; three plaintext-autokey settings at exactly four checks (controls up to 12). The keyword bounds of 0006-0081 now hold for both readings. | 
| 86 | 6 | **Type 2, sub-variant 2.** The ? before OBKR as a 98th symbol: grids of 98 cells read from any corner, once or twice, K3's rule mod 98, seven-column shuffles in all orders, each sending the ? to the front (300,651 routes), with a repeating key 1-26 in three placements, and plaintext or ciphertext autokey on the 14,946 full-grid, one-grid, K3-rule and seven-column routes: nothing live below 21, nothing at four checks. **Prediction failed in detail:** plaintext autokey after the move has 72 settings at three checks against at most 37 on the controls. Examined after the run: they are 34 distinct sets of checks, one set of three landing pairs repeated 12 times by different seven-column orders that land the known letters alike; the controls are lumpy the same way (one has 102 at three checks for the ciphertext autokey before the move). Chance; counting distinct check sets would have shown it at once. | 
| 87 | 3 | **Type 2, sub-variant 4.** A key that is one word's letter for the column plus a second key's letter for the row, on a grid of width 2-48: inside a row the row letter cancels, so this makes doublets pile up in one column by design. Solved exactly: on the copper as carved no width survives (width 7 fails with 14 checks; the first loop already gives 17 against 18 on the KRYPTOS alphabet); after or before each of 0080's 27,754 moves, counts at every level at the scrambled-copper rate and nothing at five checks. Prediction held. | 
| 88 | 3 | **Type 2, continued.** The column word with a second shift that changes every m letters (m 2-50, any offset, word length 2-31), the sculpture's own 31-letter carved lines among them (m = 31, offset 27): 31,994 structures, one combination consistent on K4 at a single check, against 0-230 on the scrambled coppers; nothing at two. The carved-line case dies at every word length (with a 7-letter word places 22 and 29 already need 1 and 23). Prediction held. |
| 89 | 4 | **Type 3.** K4's four carved lines laid over every four lines of the tableau plates and the cipher plates, straight across or folded at the centre, shifted up to four columns, 12 conventions (10,800 overlays): best 5 of 24 known letters, scrambled coppers 5-7. The screen's geometry gives no key. |
| 90 | 6 | **Types 1 and 3 crossed.** Running keys concealed at the sculpture (tableau, Morse, the four ciphertexts, K1-K3, Sanborn's letters, Carter's book) joined to every move of the type-1 library (27,852 distinct routes), move before or after the table, 12 conventions, exact: no full match in either order; no source matches even one whole crib stretch; the deepest partial match is 7 checks, as on scrambled coppers (6-7). The record's family slug is misspelt (6-matrix-...); the dashboard maps it. |
| 91 | 6 | **Type 6.** The Berlin clock schedules of 0079 (six readings, seven steps, every start minute: 60,480) joined to every move of the type-1 library, move before or after the table, 12 conventions, exact: no full match, no whole crib stretch, deepest partial match 7 checks in both K4 and all ten scrambled coppers. The Carter and dedication dates of 0038 are short periodic keys, already covered by 0080 and 0083. |
| 92 | 2 | **Type 4.** The message written into a grid of width 2-96 along one of 30 hand paths (rows, snake rows, columns, snake columns, spirals from each corner either way, diagonals, each reversed) and read out along another, 43,579 distinct routes, with a repeating key 1-26 before or after: nothing below period 21. **Prediction failed in detail:** after the move, periods 22 and 23 sit above the coppers' range (47 and 405 settings against at most 32 and 339); counted as distinct check sets they are 13 and 88 against 8-15 and 74-98, so look-alike routes, not a signal. |
| 93 | 6 | **Type 7 through type 1.** One carved letter wrong: every route of the type-1 library with a repeating key 1-26 before or after, accepting settings that fit all known letters but one: nothing below period 14; the smallest period with at most one miss is 20 after the move (coppers 19-21) and 24 before (24-25). **Prediction failed in detail:** three single periods fall just outside the coppers' range (25 exact after the move, 22 and 24 with one miss); look-alike routes were not collapsed into distinct check sets, as they were for 0092. |
| 94 | 6 | **Type 7, length changes.** One carved letter extra (struck out, 96 letters) or missing (an unknown put back, 98) at every place outside the crib stretches, 149 variants, every single move on the true length (K3's rule, one quarter turn, plain and true-keyword columnar; 96 = 8 x 12, 98 = 7 x 14), periodic key 1-26 before or after: 648,709 settings, nothing below period 20, every period inside the scrambled-copper range. |
| 95 | 1 | **Type 8.** 93 riddle words (spelled numbers, units, compass words, the puzzle's and Sanborn's theme words) dragged across K4 under all 376 crib-consistent single-alphabet periodic keys (periods 27-96, 8 classes), skipping the known stretches: no word reaches 3 agreeing checks (most 2), random strings of the same lengths reach 4. At the live lengths a word meets at most a few fixed key letters, so this test has little power; it rules out only a riddle word sitting where the key is already pinned. A first dry run counted words overlapping the cribs (NORTH inside EASTNORTHEAST) and was fixed before the run. |
| 96 | 7 | **Type 2, joint simulation.** 31 two-stage recipes from experiments 80-88 (repeating key 7, 14 or 21 with a width-7 columnar, a width-7 quarter turn or a K3-rule move, either order; the self-feeding autokey at lag 1 or 21 with a period-7 key, with or without a move; the column-plus-row key), 20,000 samples each from Carter's English: none makes the doublet column and the width-21 repeats together more than 2 times in 20,000. The column peaks at 1.4% (autokey lag 1 + period-7 key, as in 0065), the repeats at 1.5% (any period-7 key, since 21 = 3 x 7). **Prediction failed:** the column-plus-row key at width 7 makes the column in 0.26% of samples, the chance rate, not over 10%. 0087's premise was wrong: the row letter cancels inside a row, so doublets fall as under a plain 7-letter key. The sample size was raised from 4,000 to 20,000 after a dry run, before the run. |
| 97 | 6 | **Type 2 and the type-1 gap, free alphabets.** A repeating key on an unknown mixed alphabet (Quagmire III) or an unknown pair (IV), after or before every move of the type-1 library or none, tested exactly by linear algebra mod 2 and mod 13: at periods 3, 7 and 21 (the divisors 0096 ties to the repeats) the consistent counts sit in the coppers' range everywhere but one cell: Quagmire IV at period 3 after the move, 16 settings against 1-12, 12 distinct equation sets against 1-11 (counted after the run). With ten controls K4 tops them all one time in eleven by chance, and free alphabets leave the plaintext open, so this is marginal, not a lead. Free alphabets are a weak test at 7 and 21: thousands of settings fit on K4 and coppers alike. |
| 98 | 1 | **Types 3 and 5.** The sculpture's running keys of 0090 (tableau, Morse, the four ciphertexts, K1-K3, Sanborn's letters) on an unknown mixed alphabet, any of 26! orders (Quagmire III, K1-K2's system with the table left free), every offset, both directions, three rules, tested exactly mod 2 and mod 13: 80,676 settings, none fits any alphabet on K4; scrambled coppers 0-57. |
| 99 | 6 | **Type 1, last gap in the turn library.** Two quarter turns in mixed senses (clockwise then anticlockwise, the reverse, anticlockwise twice) at every pair of widths 2-96, forward and inverse, 53,743 routes not tested before, with a repeating key 1-26 before or after: nothing below period 20, and every period inside the coppers' range counted both by settings and by distinct check sets. |
| 100 | 6 | **Replication.** The four marginal counts of 0092, 0093 and 0097, as distinct check sets against 50 fresh scrambled coppers: paths at period 22 (p 0.24) and 23 (p 0.48) and one miss at period 22 (p 0.10) were luck. Quagmire IV at period 3 after a move stays above every copper: 12 distinct equation sets against 0-11, p below 0.02. That is not a replication in the strict sense, since K4's count is the same data and only the null is sharper; the cell was the most extreme of 12 in 0097, so corrected it is near 0.24. Listed after the run, the 12 sets are loosely constrained systems spread over different moves. Pinned down in 0102. |
| 101 | 1 | **Interrupted key.** The key word restarted at each plaintext word, using the word breaks the cribs give (five splits of EAST NORTH EAST and BERLIN CLOCK), key lengths 1-26, 8 classes: no length fits on K4 or on any scrambled copper. Offsets 0-3 recur in every word, so known letters always share key letters and the test is exact at every length. **Prediction failed in its exception:** it expected long keys to escape the test; none can. |
| 102 | 6 | **The period-3 excess, settled.** Quagmire IV at period 3 after a move against 400 shuffles: K4's 12 distinct sets has p 0.043 (one shuffle reaches 23), 0.048 after correcting across the four period-3 cells; against 400 copies of K4 with the columns of its 21-wide grid permuted, which keep every pair 21 apart, p 0.10 and the mean rises from 4.8 to 6.2. Not a signal; part of it is the known width-21 repeats. **Prediction failed in detail** (expected above 0.05 and above 0.2). |
| 103 | 1 | **The copper as its own key through K3's rule.** Key for place i = the carved letter at a + b i mod 97, every a and b (the mirror and every decimation; 0002's lags are b = 1), 16 rules: best 7 of 24 known letters alone (coppers 7-9); with a repeating key added, nothing below period 20, period 25 just outside the coppers' range. **Prediction failed in detail:** it put the best at 6. |
| 104 | 1 | **The message as its own key through K3's rule.** Key for place i = the message letter at a + b i mod 97: each known letter fixes its whole cycle of the rule, so the test is exact; no setting of 7,031 maps x 12 rules survives on K4 or on any copper. |
| 105 | 8 | **Affine Hill, letter by letter.** Written as decryption, p = B c + w, every known letter is one equation in one row, partial blocks included; sizes 2-5, plain and affine, every alignment, four numberings, solved mod 2 and mod 13: every setting of size 2-4 dies on K4 and on the coppers, the 4x4 affine case included; 5x5 affine is underdetermined in 14 of 20 settings and dead in the rest. A planted affine Hill text is recovered. |
| 106 | 9 | **Family 9 with every move built so far.** A one-to-one letter swap with the type-1 library, 0092's grid paths, 0099's mixed double turns and 0083's triple turns (1.84 million distinct routes; the swap commutes with the move, so one test covers both orders): no route fits on K4 or on any scrambled copper. |
| 107 | 5 | **Three-term Gromark, free alphabet.** d[i] = d[i-a] + d[i-b] + d[i-c] mod 10 for all 20 rules with c up to 6, every primer (10,631,000), four forms, any mixed alphabet, by 0069's exact digit-difference test: no primer consistent on K4 or on any copper. A planted text is found. |
| 108 | 4 | **The copper read from behind.** Each carved line right to left with the line order kept (the view from the back, where the tableau reads correctly), the line order reversed, and both, with the reading before or after the table: periodic keys dead below 26 in every case, no ciphertext or plaintext autokey lag with three or more checks survives, as on the coppers. A first dry run counted checkless long lags and tautological chain steps as checks; fixed before the run. |
| 109 | 1 | **Keyword tables from the whole dictionary.** Every word of four letters or more in the project dictionary (208,062 distinct keyword alphabets) as the plain alphabet, the cipher alphabet or both, with a repeating key 1-26 and no move, 10 classes per word: nothing consistent below period 26 on K4; the coppers reach 25. K4 is if anything less consistent than chance. |
| 110 | 6 | **Keyword columnar from the whole dictionary.** True keyword column orders from every dictionary word (229,634 distinct orders, repeats dropped or whole word; 459,268 routes with inverses), repeating key 1-26 before or after: nothing below period 21; the one period outside the coppers' range (23 after the move) has K4 below them (228 against 231-296). |
| 111 | 6 | **Myszkowski.** Columns sharing a key letter read together across each row, keyed by every dictionary word with a repeated letter (171,995 distinct keys, ABSCISSA and PALIMPSEST among them; 343,964 routes with inverses), repeating key 1-26 before or after: nothing below period 21; period 25 after the move falls just below the coppers' range (1,499 against 1,540-1,650). |
| 112 | 6 | **The same word twice.** Double keyword columnar with one dictionary word for both passes, the field double transposition (229,634 orders, 459,267 routes), repeating key 1-26 before or after: nothing below period 21, every period inside the coppers' range. |
| 113 | 6 | **Rail fence and redefence.** Zigzag over 2-48 rails from every start phase, rails read in order, reversed, or (up to 6 rails) in every order, 12,784 distinct routes, repeating key 1-26 before or after: nothing below period 21, every period inside the coppers' range. |
| 114 | 6 | **AMSCO.** Cells alternating one and two letters under every dictionary word of 3-15 columns, either cell size first (445,680 settings, 891,360 routes), repeating key 1-26 before or after: nothing below period 22. Period 23 after the move sits above the coppers: 21 settings against 1-15, 15 distinct check sets against 1-9 (counted after the run). The keys are obscure words (ADULTEROUSLY, MATCHLESS, THIOPHOSPHATE), and with 52 cells and ten controls about 4.7 cells should top the range by chance; one does. Noted, not followed. |
| 115 | 3 | **Key word/s.** A puzzle word (171: vocabulary, K1-K3 words, theme words) added to any dictionary word of 3-24 letters, every start of each, 24 table rules (KRYPTOS + ABSCISSA repeats every 56, inside the lengths the cribs allow): subtracting the puzzle word never leaves a key that repeats with any length 3-24, on K4 or on a copper, so no second word is even forced. Two-word sums with one puzzle word are dead. |
| 116 | 8 | **Matrix codes, then the table.** A Hill matrix of size 2-4 with a repeating key of length 1-26 on the table, either order (one numbering: p = B c + a shift per block class), solved row by row mod 2 and mod 13: no setting alive on K4 or any copper; every setting dead for 2x2 at key lengths 1-12, 14 and 16-24, for 3x3 at 1-7, 9, 12-15, 18 and 21, for 4x4 at 1, 2, 4 and 8; the rest partly open (too few equations). A planted text is recovered. |
| 117 | 1 | **'All the possible shifts' (C2(b)).** The sculpture's texts (the K1/K2 block among them) as a running key plus one constant shift of the table, both key numberings, with no move and with every move of the type-1 library before or after the table, tested through difference signatures: no full match, no whole crib stretch; the deepest partial match is 8 checks on K4 and 7-9 on the coppers. |
| 118 | 1 | **Autokey running on from K3.** Ciphertext autokey whose key is the carved letter 1-200 places back in the whole carved stream (K1-K3 and the ? before K4), so every known place is a check, and the letter carved one or two lines above on the plate: best 5 of 24 by distance and 3 by the plate (coppers 5-6 and 2-5). |

### Experiments 80 to 88: types 1 and 2 of directions.md (2026-10-15 night)

Alexis away; worked off type 1 (change plus move) and type 2 (sevens) in order, each checked first against the
prior-work database. All nine reverted; no champion. Run issue #24.

Findings worth keeping:
- **Type 1 is closed for its four cheap gaps.** Two repeating keys around a move, solved as a linear system (0080);
  autokeys of both kinds with K3's rule, grid turns and columnar (0081); hand padding, blanks on top or fillers carried
  through a second turn (0082); every triple quarter turn, 1.7 million routes (0083). All at the scrambled-copper rate.
- **Type 2's open items are closed too.** Double columnar with one width of 7 in all 5,040 orders (0084); the ? as a
  98th symbol in a full 7 x 14 grid, with autokeys (0086); a column word plus a row key, the one construction found that
  lines doublets up by column by design (0087), and the same with a shift per stretch of m letters or per carved
  31-letter line (0088). The width-7 doublet column still has no construction that also fits the cribs.
- **Issue #26:** ten records (0006-0081) read keyword column shuffles by the rank list, the inverse of the key order.
  0085 reran true keyword columnar, single and double, with periodic and autokey keys: chance. The library's keyword
  order also drops repeated letters (ABSCISSA reads as ABSCI); 0084 and 0085 test the whole-word reading as well.

Mistakes:
- Three predictions failed in detail at the margin (0080 low at three checks; 0081 four settings at four checks; 0082
  and 0083 a period just above the control range, 0083 one coincidence at period 18 that decrypts to noise). In each
  case the excess was examined after the run, not before.
- 0086's three-check excess came from 34 distinct check sets repeated by look-alike routes. Counting distinct check
  sets, not settings, should be the default for route sweeps.
- Starting 0085 the first time, `cp` and `rm` prompted interactively and did nothing, so two aborted runs (0085 on
  0084's code, then 0086) were started and killed within seconds and their folders removed before any record was
  written. Use /bin/cp -f and /bin/rm -f.
- Family 6 took seven reverts in a row (0080-0086), past the five-revert pivot rule, because directions.md fixes the
  order of types; noted in the pivot log.
- 0087's phase clock was not ticked, so it shows as unclocked.

Open:
- Type 1 left: the two stages on different alphabets (not linear), two free alphabets at periods 13-26 (needs English
  scoring), turns with one carving error (type 7). Type 2 left: width 7 with two free alphabets, and a joint simulation
  that must make both fingerprints and fit the cribs.
- Next in directions.md: type 3, keys read off the sculpture.


### Experiments 89 to 118: types 3 to 8, the free-alphabet follow-up, then hand routes keyed by the dictionary (2026-10-15 night)

Alexis away overnight, asked to continue past 100. Worked through types 3-8 of directions.md once each, then
followed the one cell that stood out. All eighteen reverted; no champion. Issue #24; issue #28 (source-text search).

Findings worth keeping:
- **Types 3-8 have each had a first exact pass, all at chance.** Keys read off the sculpture by position (0089) or
  as running keys joined to every move (0090, and on an unknown alphabet, 0098); the Berlin clock with every move
  (0091); the message written along grid paths (0092); one wrong, missing or extra carved letter through moves
  (0093, 0094); riddle words dragged under every live periodic key (0095, weak); an interrupted key (0101); the
  copper or the message as its own key through K3's rule (0103, 0104).
- **Type 5 is closed by algebra, not by a run.** Any reading of a cyclic table (by columns, diagonals, mirrored, from
  another start row) is an affine map of the alphabets with the key scaled or shifted; those are covered by 0071 and
  0074, and a diagonal reading only restricts the key to even values.
- **No published text carries both cribs** (issue #28: Internet Archive full text, 44 Gutenberg books, the web).
- **The width-21 repeats have a cheap explanation**: any key repeating every 3, 7 or 21 carved letters, after any
  move, makes them about 50 times more often than chance (0096). On fixed alphabets those periods are dead; on free
  alphabets the test is weak (0097). The one free-alphabet cell above the coppers (Quagmire IV, period 3, after a
  move) went from p < 0.02 against 50 coppers (0100) to 0.043 against 400, and 0.10 against copies that keep
  K4's width-21 columns (0102): not a signal, and partly the repeats themselves.
- **0087's premise was wrong** (0096): a column word plus a row key does not line doublets up by column, because the
  row letter cancels inside a row.
- Family 9 and the affine Hill are closed for every route set built so far (0105, 0106).

Mistakes:
- My wait loops used `pgrep -f run_experiment.py`, which matched their own command lines, so they never ended
  and were killed by hand. Wait on the run log's `decision=` line instead.
- 0089 and 0090 recorded misspelt family slugs (4-visual-systems, 6-matrix-transposition-then-tableau); the
  dashboard maps them. Check `cut -f3 results.tsv | sort -u` before choosing a slug.
- 0090's worked example crashed (the Morse text is shorter than K4), so that record has none; the figure
  rebuilt one from the record's own functions.
- 0092, 0093, 0096, 0101, 0102 and 0103 missed their predictions in detail; 0096's miss is the 0087 correction.
- 0095's first dry run let words overlap the cribs and counted those as checks; fixed before the run.

Open:
- Free alphabets at periods 7 and 21 need a stronger test than consistency (English scoring cannot beat its
  controls; a test on the forced partial alphabets might).
- Routes outside every set built so far; three-term Gromark rules; plaintext masks that change letters by a code.

### Experiments 50 to 64, run in the background (2026-10-15 afternoon)

All fifteen reverted; nothing was kept, and the champion is still experiment 34. Every run
finished well inside the 30-minute budget (longest 0050 at 5 minutes).

Findings worth keeping:
- **The two fingerprints are real (0056).** The width-7 doublet column and the width-21
  repeats survive the look-elsewhere correction over widths 2-48 against 10,000 shuffles:
  corrected p 0.005 (0.018 among six-doublet shuffles) and 0.010. The pre-registered
  prediction said they would not. They still lack a construction.
- **Only ciphertext feedback makes the width-21 mark (0062).** Of fourteen generators, only
  ciphertext autokey at lag 21 raises the repeats well above chance (5.4% against 0.2%);
  none makes the doublet column, and none makes both. Ciphertext autokey stayed dead when
  combined with columnar routes in either order (0063) and on tables rebuilt from K1-K3
  words (0064).
- **Two structural exclusions, no key search needed.** Pure transposition is dead because
  the cribs need three Es and the copper has two (0051). Every cipher with at most 25 output
  letters or an even-length rule (Playfair, bifid, four-square, ADFGVX, a 24-letter
  Weltzeituhr ring) is dead because K4 uses all 26 letters and has 97 (0052).
- **Tables rebuilt from every K1-K3 word and the 2025 letter's words** add nothing for
  periodic keys (0053), Gromark (0054, smallest base 17), Hill (0055), two-word keys (0059)
  or ciphertext autokey (0064). The vocabulary was not the limiting factor.
- The copper off by one letter through the two-word test (0050), filler letters chosen by
  letter (0057), the table then keyed column shuffles from K1-K3 words (0058), the K2
  coordinates as a Hill matrix (0060) and the misspelt letters as a second key (0061): all
  at chance.

Mistakes:
- Walkthrough arithmetic slipped four times and was caught by checking the numbers before
  the run (0053, 0054, 0055, 0056), and once after it: 0052's record puts I at place 16,
  not 17. Checking the walkthrough against the code before running is now routine.
- Two predictions were wrong in detail: 0057 and 0058 expected nothing below period 26
  and got periods 24-25 at chance rates; 0058 ran no control to measure that rate, and
  the forced fragments at 24-25 were not word-checked in 0057.
- 0050's pre-registered count of distinct crib tuples was corrected to "about 50" before
  the run; the measured value is 48.

Open questions:
- What construction makes both fingerprints? Ciphertext feedback at lag 21 plus a stage
  that also lines up doublets at period 7 is the lead; it must still pass the cribs.
- Family 3 has now reverted seven times in a row (0014-0061) and family 6 eleven times;
  both should rest until a new key source appears.
- The scorer decision (key cost, shuffled baseline) is still pending in issue #11; no
  key-completion climbs were run.


### Experiments 65 to 79, run in the background (2026-10-15 evening)

All fifteen reverted; nothing was kept, and the champion is still experiment 34. Every run
finished inside the budget (longest 0077 at 4 minutes). Run issue #22.

Findings worth keeping:
- **The fingerprint constructions are dead under the cribs.** Only one recipe was found that
  lines doublets up in sevens: ciphertext autokey at lag 1 with a period-7 key, and it does so
  weakly (1.5% of samples against 0.1-0.3% by chance, 0065). Tested exactly, ciphertext autokey
  plus a periodic key at any lag and period is dead (0066), and so are lag 1 with period 7 and
  lag 21 at every period. Two-lag letter feedback, the one-stage way to make both marks, is at
  chance (0067); so is ciphertext autokey with one carved letter wrong, missing or extra (0068),
  and every block-of-seven reshuffle joined to it, in both orders (0077). The two fingerprints
  remain real and unexplained.
- **Gromark is closed for two-term rules whatever the alphabet.** With a completely free mixed
  alphabet, base 10 (lags up to 6, 0069) and bases 2-16 and 26 (lags up to 5, 0076) leave no
  consistent primer on K4 or on shuffled coppers; planted texts are recovered. Same-letter cribs
  fix exact digit differences, which makes the test decisive. Family 5 marked
  exhausted-bounded; three-term rules with a free alphabet stay open.
- **New key sources revive nothing:** alphabets one swap or one move from KRYPTOS, the C27(c)
  'slightly different tableau' (0071); the 32 compass points and the 'what's the point?'
  letter's words (0072); plaintext autokey plus a periodic key on 161 word alphabets (0073);
  affine masks, Atbash included (0074); Sanborn's 1989 letter, the 1991 dedication pages and
  the 2025 open letter as running keys (0078, best 15 mismatches as on shuffles); key schedules
  from the Berlin set-theory clock (0079, best 8 of 24 agreeing, as on shuffles).
- **The doublets are real letters.** QQ, SS and TT inside the known stretches carry NO, ST and
  IN, so the doublets cannot be fillers, and striking out the other three changes nothing (0075).
- A block-of-seven reshuffle before or after a periodic key admits no period below 25 beyond
  chance (0070).

Mistakes:
- Pre-registered counts were wrong four times and corrected before the run only once:
  0071's variant count (975 to 925, corrected before), 0066's case count (294,912 counted lags
  with no equations; 221,184 tested), 0069's primer total (5,432,200 for 5,432,100), 0067's
  case count (5.2 million counted cases with no check; 1.93 million tested).
- Two predictions failed in detail at the three-check level, 0067 (15 survivors against 3-12)
  and 0073 (12 against 0-6). Both resolve into scattered or nested coincidences, but a
  prediction should allow for chance survivors at three checks when millions of cases run.
- 0068's substitution tally counts the residuals a replacement letter is fitted to as checks,
  overstating redundancy by one or two.
- 0070's fragments at periods 25-26 were word-checked only after the run.
- 0079's prediction carried a numeric guess (19-20 mismatches) that a dry run on the copper
  showed wrong (16); it was removed before the run and is disclosed here.
- The recorder stopped once on a clue-register match (0071) after writing families.md and the
  notebook; the commit was finished by hand.
- The harness once hung on an interactive cp prompt when restoring attack.py; /bin/cp -f
  avoids it.

Open questions:
- What makes the width-7 doublet column? Every construction with a period-7 element that
  passes the cribs has now failed; one not yet tried is a second, independent stage such as
  nulls placed by a period-7 rule after encryption, or a homophonic substitution.
- The width-21 repeats: ciphertext autokey at lag 21 made them, but it is dead with every
  addition tried (periodic key, second lag, one error, block reshuffle, word alphabets).
- Three-term Gromark with a free alphabet; Hill with a free numbering; Sanborn's own charts
  (C27) beyond the alphabet.
- The scorer decision (key cost, shuffled baseline) is still pending in #11; no
  key-completion climbs were run.

### Scoring settled (2026-10-15, afternoon)

Alexis decided the open scoring questions (issue #23). First version, same afternoon: a hard
gate on key size (100 bits). Withdrawn within the hour. Alexis asked where the requirement came
from: it was criterion 4 of our own success definition ("a key a person could remember"),
justified by K1-K3's short keywords and Sanborn's "words without a method is not solved". Neither
holds up as a basis for a size limit. Three sections are a thin precedent and do not agree (K3
has no keyword), and Sanborn's remark is about showing the method, not the size of the key. A
long key can have a short description: a running key from a named book.

Final rules: (1) the original four gates; (2) a reading must beat the same method on at least
ten shuffled coppers (run() returns "controls"); no controls, no keep; (3) the harness counts the
key by the length of its description (key words a few bits each, a named text and offset a few
bits, arbitrary letters 4.7 bits each) and charges it in the loss, not as a gate; (4) lowest loss
wins. Criterion 4 of the success definition now reads: a hand procedure from 1990, written down
step by step, keyed by something with a short description rather than letters fitted to the
known places; its source is Scheidt's 2011 remark (secondhand, via Bean, C5): "simple, can be
remembered, and executed years later when used with the correct key word/s".

All records re-scored (tools/replay_rules.py, records untouched): no past reading passes the
baseline, because no record carries a set of ten or more controls. Experiment 34 would fail on
its own numbers anyway (its reading -3.70 against a shuffled best of -3.23). Experiment 48's best,
-6.14, beat its smaller control set (-6.36 to -6.88), but that set was not ten full-size runs.
There is no champion. The dashboard now recomputes every loss under the current rules, keeping
each record's own figure as history, so one number shows everywhere.

Lessons: a success criterion has to be a gate or a score in the harness from day one, or the loop
optimises around it; and a criterion needs its source written next to it, or it hardens into a
rule nobody chose.

## 2026-10-14

### Decisions

- Success means a reproducible method, not words: the 97 letters must carry the cribs at
  22-34 and 64-74, read as English, re-encrypt exactly, and come from a memorable key and
  a 1990 hand method. No external oracle. Every experiment leaves a bounded negative.
- Loss is lexicographic: ten points per wrong known letter, then the English deficit,
  then key cost. The crib gate at ten is where a solution first becomes visible.
- Records carry four prose fields written before the run: expert hypothesis, plain-words
  version, prediction, walkthrough. They are not edited after the result; corrections go
  to the families table and the issue thread.
- Phase clock: design, implement, test, with run and record added by the harness, and a
  pause tick for time handed back to a person.

### Built

Harness (`run_experiment.py`, `_runner.py`, gates, scorer, 19 tests), the frozen cipher
library, the knowledge base of 72 sources with a clue register of 30 entries, the families
list, the dashboard, the phase clock. Dashboard changes from review: plain words first on
each record, walkthrough beneath, numeric ids, crib gate explained beside the chart with
the 24-letter strip, axis in loss points with "n wrong" readings, unclocked phases named,
record tables that wrap.

### Experiments 1 to 20, all reverted

| # | Family | One line |
|---|---|---|
| 1 | 1 | Baseline KRYPTOS keyword: 2 of 24 cribs, loss 224.7. |
| 2 | 1 | Ciphertext autokey, every lag, 24 conventions: none. |
| 3 | 1 | Plaintext autokey inside the cribs: lags 1-11 and 30-52 dead. |
| 4 | 1 | Running key from K1-K3, every offset: none. |
| 5 | 1 | Quagmire period sweep: 1-26 and 30-52 dead; survivors force no word. |
| 6 | 6 | 2,905 columnar routes then tableau: no key shorter than 23. |
| 7 | 6 | Tableau then columnar: weak test in this order; nothing at 26-30. |
| 8 | 6 | K3's rule at every shift, double rotations, then tableau: no key shorter than 22. |
| 9 | 1 | Forced key stretches read as noise; one letter inserted or deleted changes nothing. |
| 10 | 1 | Same with 248 vocabulary-mixed alphabets: best equals the shuffled null. |
| 11 | 1 | Progressive key: periods 1-25 and 31-51 dead at every step; period 13 dead. |
| 12 | 1 | Chained plaintext autokey: lags 1-25 and 30-52 dead; 26-29 force noise. |
| 13 | 5 | Gromark-style rules, all lag pairs to 12, bases 10 and 26: none fit the shifts. |
| 14 | 3 | Two words in two passes as linear equations: none under total length 25. |
| 15 | 8 | Hill 2x2 to 4x4, plain and affine, solved exactly: all dead. Playfair dead. |
| 16 | 6 | Forced key under 23,930 routes scored as English: inside the shuffled distribution. |
| 17 | 1 | Running key from the carved tableau, the Morse, the whole panel: none. |
| 18 | 7 | Simulator: no family singled out; width-7 and width-21 anomalies unexplained. |
| 19 | 9 | Substitution then any of 23,931 routes: crib images clash under all. |
| 20 | 1 | Short periods with vocabulary-mixed alphabets: 21 and 42 have no survivor. |

### Findings worth keeping

- The crib-consistency test for tableau systems depends only on the plain and cipher
  alphabets and on Beaufort versus the other modes; the key alphabet drops out. The 24
  conventions are 8 distinct cases for any such sweep (0006).
- Substitution then transposition is the only construction simulated that reproduces the
  width-21 repeats, and it is dead for every enumerable route (0018, 0019). The repeats
  remain unexplained, as does the width-7 doublet column, under every generator including
  random letters.
- A crib-fitted construction passes the crib gate by design (a Hill matrix solved from
  the blocks, a fully chained autokey). The English deficit must carry the verdict, and
  the record must say when the cribs were built in rather than found (0012, 0015).

### Mistakes

- 0007's phases were ticked back to back in one command, so its design time is lost.
- 0016 and 0010 set prediction tolerances from two shuffled controls; the max of two is
  too noisy. Ten or more from now on.
- 0017's record says the carved panel is 869 letters; it is 865.
- 0018's design clock ran across a pause between turns. The pause tick now exists.

### Open at close of day

The three unexplained statistics. Family 2 untouched for want of a concrete mask. Family
4 touched only by the 25-letter-square exclusion. Routes outside the enumerable sets.
Alphabets built from words outside the 61-word vocabulary.
