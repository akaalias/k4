# program.md: instructions for the loop agent

You are running an autoresearch loop against Kryptos K4. Before your first edit, read in full
and in this order:

1. this file;
2. `README.md`;
3. every numbered file in `knowledge/` (`01-facts.md` through `12-assumptions.md`). The
   assumptions register is context: its entries become loop work only when `order-of-work.md`
   lists them;
4. `order-of-work.md` (the Priorities page);
5. `families.md`;
6. `results.tsv` and the `experiments/*/experiment.md` records, newest first.

This is not optional and it is not skimmable. The record contains throwaway remarks from the
artist and the cryptographer that no search strategy will rediscover; the clue that breaks K4
is as likely to be one of those as a statistic.

When you open a hypothesis family, also read the primary sources in `knowledge/sources/` that
the family's evidence rests on, and the matching research note in `research_notes/`. Quote
sources by file name in `hypothesis_expert`.

## What success means

A reproducible procedure that turns the 97-letter K4 ciphertext into 97 letters that:

1. contain EASTNORTHEAST at positions 22-34 and BERLINCLOCK at 64-74;
2. read as English, allowing one or two deliberate misspellings and X as a separator;
3. re-encrypt to the exact ciphertext when run forward;
4. come from a procedure a person could carry out by hand in 1990, written down step by
   step, keyed by something with a short description (key words, a named text and a place
   in it) rather than letters fitted to the known places.

> Scheidt, 2011, via Bean: "simple, can be remembered, and executed years later when used
> with the correct key word/s" (C5).

Words without a method is not success. There is no external oracle.

The guaranteed output of every experiment, including failures, is a bounded negative result:
a precise statement of what was searched.

## The gates a reading must pass to be kept (decided 2026-10-15, issue #23)

1. Length 97, letters A-Z only.
2. All 24 known letters in place.
3. Re-encrypts to the exact carved text under the stated key.
4. Beats shuffled coppers: return `"controls"` from `run`, a list of at least ten English
   scores, each the best your same method reaches on a shuffled copy of the carved text at
   the same trial count. A reading is kept only if its English score is above all of them.
   No controls, no keep.
5. The reading is whole: every letter is fixed by the key (decided by Alexis 2026-10-25, issue #88,
   after 0219 was kept on readings padded with A). If the key leaves letters open, return the count as
   `open_slots`; such a reading fails at `undetermined` and is never kept. Do not fill open letters
   with a placeholder to get past the gates.
6. The reading is your search's own: a reading counts only in the search that found it, judged
   against that search's copies (decided by Alexis 2026-10-27, issue #94, after 0224 was kept on an
   earlier reading of 0034 against a smaller set of copies). A candidate whose key names another
   experiment (`key["exp"]`) or whose reading an earlier record already holds fails at `resubmitted`.
   To measure or judge an old reading again, report it in `bounds` or `notes`, not as a candidate.

Among readings that pass all four, the lowest loss wins. The loss charges the key by the
length of its description, which the harness counts itself from the `key` you return
(`kryptos.scorer.key_bits_of`):

- key words cost a few bits each;
- arbitrary letters cost 4.7 bits each;
- a named text and an offset cost a few bits.

Return keys in a form the count can read. A search that fills free key letters to make
English (a key-completion climb) pays heavily for its key and, more to the point, cannot beat
its own shuffled controls.

`tools/replay_rules.py` re-scores every record whenever a rule changes; records are never
edited, and the dashboard shows each experiment's current verdict.

## What you may and may not touch

- Edit only `attack.py`. Never edit `kryptos/`, `data/`, `tests/`, `run_experiment.py`,
  `_runner.py`, or any past `experiments/*` record.
- Update `families.md` whenever a family's status changes.
- If you believe the scorer or a gate is wrong, do not work around it. Stop, write the case
  in a GitHub issue labelled `harness`, and continue on a different family until a human
  decides. When a ruler is fixed, the lineage is re-measured, never quietly erased.

## The loop

1. **Tick the phase clock** as you go:
    - `uv run python phase.py design` when you start reading and thinking;
    - `... implement` when you start writing code;
    - `... test` when you run the tests and dry runs;
    - `... pause` when you hand a turn back to a person, so waiting time is not charged to a phase.

    The harness records run and record itself. Time per phase is part of every experiment's
    record and of the dashboard.

2. **Read the record.** Decide the next experiment: one focused change, with a parent (the
   champion, or the experiment you are extending) or a new root when changing family.
3. **Pre-register.** Fill `EXPERIMENT` in `attack.py` before writing any search code: slug,
   title, family, parent, changed, hypothesis_expert, hypothesis_eli5, prediction, method,
   walkthrough. The prediction must be falsifiable by the run.
4. **Implement** `run`, `encrypt`, `worked_example`. Use primitives from `kryptos.ciphers`
   where they exist; they are verified against K1-K3. If you write a new primitive, verify it
   against K1-K3 inside `run` first and say so in notes.
5. **Run** `uv run --with pytest pytest -q` (all must pass), then `tools/start_experiment.sh`, and
   wait for it with `tools/wait_experiment.sh`, calling it again for as long as it reports the run
   still going. **No time limits** (Alexis, 2026-10-27, issue #96): an experiment takes as long as it
   needs. The harness kills nothing unless you pass `--budget`; `ctx.time_left()` is then infinite.
   Never shorten a search, skip an arm or cut copies or plants to fit a clock, and never run an
   experiment as a background task of your own session, which a tool limit can stop. Before a run
   that will take more than a few hours, state its expected total time in `bounds` (Alexis's rule
   of 2026-10-20). A new session first runs `tools/wait_experiment.sh`: a run may still be going.
   Design the search to reach a verdict as early as possible: gate on cribs inside your search
   loop, do not generate English and hope.
6. **Read the record** the harness wrote. If `kept`, the champion advanced. If `reverted`,
   restore `attack.py` from the champion's snapshot or start the next root. Either way the
   record stays.
7. **Commit** is automatic (one commit per experiment). Push after each.
8. **Glossary:** add any new technical word in `hypothesis_eli5` to `GLOSSARY.md` before the run.
9. **Notebook:** add one line to today's entry in `NOTEBOOK.md`: number, family, finding. Add
   a paragraph when something was decided, went wrong, or changed the plan.
10. **Illustrations:** draw the experiment's two figures, the crib map and the worksheet, in
   `design/make_experiment_figures.py` (or a script beside it), writing
   `figures/NNNN-cribmap.svg`, `figures/NNNN-cribmap-notes.json` and
   `figures/NNNN-worksheet.svg`. Follow the style guide (`design/style-guide-v5.pdf`):
    - the frame with the method on a wash panel;
    - short labels with leaders;
    - two to four notes;
    - worksheets on the grid;
    - real letters and numbers from the record.
    - in the crib map's OUT row, fill a known place in accent only if the reading produced that letter;
      outline it otherwise, so a method that found nothing never looks as if it did (issue #49);
    - the IN and OUT labels sit on their arrows, centred (the dashboard also places them when it serves the figure).

    - the method panel holds a drawing, not sentences: cells, dots on an axis, leaders, bars, built
      from the existing pieces (`kind_cells`, `dotline`, `cell_at`, `flag`, `ledger`, `histogram`). A
      caption line above each row is fine. The explanation goes in the notes (issue #68);
    - a run that errored still gets a crib map: the planned sweep as soft "not run" cells and the
      experiment that reran it (`design/make_figures_errored.py`, after 0039; issue #67).

    Render each figure and look at it before committing. Every experiment has illustrations.
    `tests/test_figures.py` fails when a crib map is missing or its method panel is text only.

11. **Readable words** run by themselves: after every run the harness asks a language model
    to mark the English words in the readings that passed every gate and the five closest,
    checks each against the dictionary, and stores them in the record (`readable_words`). The
    dashboard boxes them. It never changes a score or a decision; a climbed key makes English
    fragments by construction.

## Positive controls (assumption A3, issue #73)

A closed item is only as good as the search that closed it. Stage 2 checks each one: plant a message made with
the item's own method and a key inside its space, run the closing experiment's saved `attack.py` unchanged on
the planted ciphertext, and require the plant to be found.

- Write `controls/<ID>/spec.py` (ITEM, EXPERIMENT, WHAT, `plant()`, `found(result, plant)`; see
  `tools/positive_control.py` and the worked example `controls/C-F1.1`). `kryptos.plants.english_plant(seed)`
  gives 97 letters of English with the known words in place.
- Run `uv run python tools/positive_control.py controls/<ID>`. It writes `result.json` and a row in `controls.tsv`.
- `found` must identify the plant the way the attack would have identified K4's answer. A pass that only
  shows "something fits" where many settings fit on any text is not a pass: require the planted setting itself.
- From now on every new experiment that closes an item carries its own positive control in the same run, or
  the item stays open.

## Slip tolerance and the judge (assumption A1, issue #76)

Every exact verdict so far assumed Sanborn made no slip. Stage 2, step 2 reruns the strongest searches allowing
for one. The table "Stage 2, step 2" in `order-of-work.md` lists the items; these rules apply to all of them.

- **Where a slip lands decides how it is handled.**
    - A slip at one of the 73 unknown places in a system where an error stays put (a wrong tableau row in a
      periodic or running key) changes no consistency check, so it cannot change an exact verdict. It garbles one
      letter of the reading, which the judge is built to read through. No rerun is needed for that case.
    - A slip at one of the 24 known places: allow k of the 24 checks to fail (k = 1, 2, 3), count consistent
      settings on K4 and on at least 10 scrambled copies at the same k, and judge the readings. Dropping k checks
      costs about 4.7 bits each plus log2(C(24, k)) for not knowing which; say in `bounds` how much of the
      key space the remaining checks can still decide.
    - A slip that throws off everything after it (a skipped step in an autokey chain, a column read out of turn):
      one per run, at every place, as its own setting. F6.21 (0202-0204) already covers slipped columns.
- **A candidate with a slip passes the gates only if the slip is part of its key.** The plaintext carries the
  known words correctly; the key names the slip (its place and the wrong letter, or the skipped step) and
  `encrypt` applies it, so the re-encryption gives K4 exactly. The key's description then pays for the slip.
- **The judge.** `ctx.judge(texts)` (`kryptos/judge.py`) scores readings 0-100 for how much reads as English,
  allowing misspellings, X stops and spelled numbers. Pass '?' for letters the search could not determine.
    - Always judge K4's candidates and the copies' candidates in the same call and compare them: a K4 reading
      counts only if it scores above every copy's best. The judge masks the known places itself and sees one text
      at a time, so it is blind to which is which.
    - Call it from the main process, not from forked workers, and only on readings that survived the
      consistency checks: each new text costs a call (cached afterwards). The cap is `JUDGE_MAX_CALLS` (3000 per
      process); estimate your count in the design phase and say it in `bounds`.
    - Filter with the quadgram scorer first (`ctx.english_score`), the same cut for K4's and the copies' readings,
      and send the judge only what survives: against readings that look like random letters, quadgrams already
      separate damaged English as well as the judge (bench), and they cost nothing. The judge earns its cost on
      English-like junk and on readings that are only partly English.
    - A verdict can come back `None` (the model refused or never gave a score). Count it as not found, for K4 and
      copies alike, and report how many.
    - It filters. It never certifies: the four success criteria and the gates still decide.
    - Its measured power is in `reports/judge-bench.md`: use it to say what a 'nothing found' means.
- **Every A1 run plants its own slipped message** (English from `kryptos.plants`, encrypted with the item's
  method and k slips) and requires it to be found at the same tolerance, in the same run. The largest k at which
  plants are found and K4's count can still differ from the copies' is the item's reach; beyond it the item is
  `blocked: too short to decide k slips`, with the numbers.

## Masked English (A13) and the English score (A6)

Stage 2, steps 3 and 4 (issues #75 and #84). The tables in `order-of-work.md` list the items; these rules apply to both.

- **These are experiments** (run_experiment.py, numbered, with records and figures), except A13.1, which writes up
  `power.json`, and A13.2, which ranks the readings already in `pass2.json`. Both still go in the report and the
  table. Reuse `tools/a13_structure.py` and `tools/a13_check.py`; do not rewrite them.
- **Many tests, one verdict.** The battery runs 14 tests, so K4 above every one of 20 copies on some test happens by
  chance about two times in three. Before each run, write down which tests count and how many cells (test x
  experiment) are looked at. A cell flags only at an empirical p below 0.05 divided by that number, which needs
  enough copies to reach it (at 14 cells, at least 280). With fewer copies, a cell where K4 beats every copy is a
  candidate, not a result: replicate it on that test alone against fresh copies, enough for the corrected p, before
  anything else. Only a replicated flag stops the queue.
- **Copies are made the way the readings were made:** the same search, from the frozen `attack.py`, on scrambled
  copies built as the experiment built them (plain shuffles, or shuffles that pass the same decider). Never compare
  K4's climbed readings with copies' unclimbed ones.
- **The judge** follows the rules in "Slip tolerance and the judge": K4's and the copies' readings in one call, blind,
  quadgram filter first with the same cut, estimate the calls before the run, `None` counts as not found.
- **Every run that closes an item plants its own answer** (masked or Sanborn-style English through the item's own
  method) and says whether it was found, in the same run.
- **A verdict that changes is written back.** If A6.1-A6.3 weaken a sampled close, change that item's row in its family
  table (`closed` to `open` or `blocked`, with the numbers), its row in `grades.tsv`, and A6 or A13 in
  `knowledge/12-assumptions.md`. Reopened family items go back into the queue in their family's place (Alexis, 2026-10-27, issue #92).

## Ciphertext only (F13)

F13 in `order-of-work.md` (issue #85). The search works as if no plaintext were known.

- **The search never reads the known letters.** An F13 `attack.py` does not import them from `kryptos.facts`,
  `kryptos.cribsweep` or `kryptos.gates`, and does not prune, rank or seed by them. The harness still applies
  gate 2 at keep time. That check is the held-out test.
- **Order of judgment:** a reading must beat its copies on English alone first. Only then are the 24 letters
  looked at. Report how many readings beat their copies and how many of those also put the 24 letters in place.
- **Plants carry no known words** and are found without them, at the power the row states.
- **Copies are climbed the same way as K4,** with the same judge and budget, as in A13 and A6.
- **F13.1 comes first.** No F13.4 row runs until F13.1 has marked its family decidable.

## Patience and pivots

- **Work the families in the rank order** in `order-of-work.md` (the Priorities page, decided
  2026-10-16, issue #29). Within a family, take its open items from the top.
- **Leave a family only when every item is closed or blocked:** `closed` means exact, or
  sampled against scrambled coppers at stated power; `blocked` means a written reason it
  cannot be tested with the known letters. Reverts do not force a pivot; a revert that closes
  an item is progress.
- **Name the item and the strength.** Every experiment names the item it works on (for example
  "F1.1") in `changed` and the strength it reached. After the run, update:
    - the item's row in `order-of-work.md`;
    - its leaf in the hypothesis tree in `families.md` (add sub-hypotheses there when an item splits);
    - the experiment's line in `grades.tsv`.

    A weak test leaves the item open.

- **A result outside the scrambled-copper range stops the queue:** replicate it against fresh
  controls before anything else.
- **Change the ranking only at a family boundary,** with the reason in the pivot log. Every pivot also gets a
  page, `pivots/PN.md`: frontmatter `id`, `date`, `after` (the experiment it follows), `from`, `to`, then why it
  happened then, what came before, and the change we believe is needed. The dashboard marks it on the charts
  and the experiments table.
- **Dead ends** listed in `README.md` need a stated reason in `hypothesis_expert` before re-entry.

## Writing the record

- **`hypothesis_expert`:** what a cryptanalyst would need to reproduce the idea. Name the
  cipher family, the key space, the constraint being tested, and the clue-register entries and
  readings it tests (for example "C1(a), C8(a)"). After the run, update those entries' status
  in `knowledge/11-clue-register.md` with the experiment tag. An experiment that tests no clue
  needs a stated reason to exist.
- **`hypothesis_eli5`:** standalone, for a curious non-specialist. No jargon without a
  one-clause gloss.
- **`walkthrough`:** a standalone guide that lets a reader redo the method by hand on a few
  letters. Write it as numbered steps, one action each; the harness puts each step on its own
  line. If this experiment ever becomes part of the winning chain, the walkthroughs compose
  into the method writeup.
- **`bounds`:** numbers. Periods tried, key lengths, alphabets, word lists, how many keys,
  whether exhaustive. "Tried a few" is not a bound.
- **`key_bits`:** honest entropy of the key. Words cost 4.7 bits per letter; arbitrary letters
  cost log2(26) each; a choice among N options costs log2(N).

## How to think here

Sanborn wrote the text and enciphered it himself, by hand, with charts, on a truck ride, after
four months of lessons from a field-communications officer who thinks in keys built from parts
and codes an agent could carry in his head under duress. He is an artist who thinks in strata,
light, shadow, matrices and the sculpture as one object, who personalizes every instrument he
is given, and who deals in misdirection. The system will be simple once seen and will look
like him.

Before writing search code, sit with `knowledge/06-hypotheses.md` and ask what this particular
person would have done. Prefer experiments that test a specific reading of a specific quote
over experiments that sweep a textbook cipher family. Both are needed:

- the sweep is cheap and should leave bounds behind;
- the specific reading is where the odds are.

## Hard facts you can rely on

- **Cribs:** positions 22-34 EASTNORTHEAST (ciphertext FLRVQQPRNGKSS), 64-74 BERLINCLOCK
  (NYPVTTMZFPK). Position 1 is the O of OBKR.
- **Self-encryptions:** two letters encrypt to themselves, S at 33 and K at 74.
- **Doublets:** adjacent ciphertext doublets QQ (26-27), SS (33-34), TT (68-69) map to NO, ST,
  IN, so the key state changes at every position.
- **Periods:** for single-alphabet periodic additive ciphers, only periods 27, 28, 29 and 53-97
  are consistent with the cribs (`python -m kryptos.cribsweep`).
- **No pure transposition:** the cribs need three E's, K4 has two.
- **The creators:**
    - Scheidt: K4 is "more than one stage"; he "masked the English language" before the keyed
      step; the system is "not mathematical, simple, can be remembered, executed with the
      correct key word/s".
    - Sanborn: "matrix codes Ed gave me" plus his own "visual systems"; earlier text holds
      "instructions" for later text; K4 "will come back to the first part".

- **Earlier keys:** the K1-K3 keys were PALIMPSEST, ABSCISSA and (by one reading) KRYPTOS;
  `data/vocabulary.txt` lists key candidates from inside the puzzle.
