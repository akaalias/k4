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

From 0033: simulated annealing over trifid cubes with crib hits, even at coordinate level, plateaus at about 17 of 24 on a planted cube. A proper trifid solver needs constraint propagation on the cube coordinates, not local search. Parked.

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
