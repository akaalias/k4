# Lab notebook

One entry per working day, newest first. Each entry says what was decided, what was run,
what was found, and what was left open. Experiment numbers link to the records in
`experiments/`. The families table and the clue register hold the bounds; this notebook
holds the reasoning and the mistakes.

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
