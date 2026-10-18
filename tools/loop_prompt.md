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
