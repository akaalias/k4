Run the autoresearch loop for Kryptos K4 in this repository.

Read program.md first and follow it exactly, including its reading list.

Work the next open items in order-of-work.md, top down. If an item can only be tested weakly, say so, mark it
blocked with the reason, and move on rather than running a weak test. Stop when the current family's items are
all closed or blocked, add a pivot page (pivots/PN.md) if you move to a new family, and continue with the next
family in the ranking until STOP_AFTER below.

Never edit or commit dashboard.py, STYLE.md or the transcripts/ folder; another session works on them.
Commit your own files with explicit paths (git commit -- path ...), then git pull --rebase --autostash and push.
Comment on the family's GitHub issue after each experiment.

When you stop, write a short report: each experiment (number, item, result against the scrambled copies,
verdict), each item's new status, surprises, mistakes, and what is left.

Stage 2 (from 2026-10-18, issues #52 and #73): every family in the ranking is closed or blocked. While the table
"Stage 2, step 1" in order-of-work.md has open rows, work it instead of the families, top down, following the
rules above the table and program.md's "Positive controls" section. A control is not an experiment: no
run_experiment.py and no experiment number; it is a folder controls/<ID>/ with spec.py and result.json, a row in
controls.tsv, and its row in the table. Commit controls in batches, one family at a time, and comment on issue #73
after each family with the passes, any slices, and any failure. A FAILED control stops the queue: find why, fix,
rerun, and report before going on. STOP_AFTER A3 means stop when no row is open.

Stage 2, step 2 (from 2026-10-20, issue #76): step 1's table is done. While the table "Stage 2, step 2" in
order-of-work.md has open rows, work it top down, following program.md's "Slip tolerance and the judge". These are
experiments (run_experiment.py, numbered, with records and figures), each with its own planted slipped message in
the same run. Use ctx.judge for readings, K4's and the copies' together; estimate the number of judge calls before
the run and keep it under the cap. Comment on issue #76 after each experiment. STOP_AFTER A1 means stop when no row
of that table is open.

Stage 2, steps 3 and 4 (from 2026-10-21, issues #75 and #84): step 2's table is done. While the table "Stage 2,
step 3" in order-of-work.md has open or in-progress rows, work it top down; then the table "Stage 2, step 4". Follow
program.md's "Masked English (A13) and the English score (A6)". Step 3 resumes partial work from 2026-10-18
(tools/a13_structure.py, tools/a13_check.py, reports/a13-structure-data/): reuse it, do not start over. The battery
runs many tests at once; a cell where K4 beats every copy is a candidate to replicate with enough fresh copies for
the corrected p, not a stop on its own. Comment on issue #75 after each step-3 item and on #84 after each step-4
item. A step-4 result that weakens a sampled close is written back to the family's table and grades.tsv, and the
reopened item waits for Alexis. STOP_AFTER A6 means stop when no row of the step 4 table is open.
