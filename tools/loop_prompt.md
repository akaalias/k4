Run the autoresearch loop for Kryptos K4 in this repository.

Read program.md first and follow it exactly, including its reading list.

## What to work on

Work the open items in order-of-work.md, top down, in the order the page lists its tables: the Stage 2 tables
first, then the cheaper decider (#77), F13, F14, then any family table with open rows. Items added to order-of-work.md since your last session
belong to the same queue; take them in their place. When you move to a new family, add a pivot page
(pivots/PN.md).

**Run more experiments, not fewer** (Alexis, 2026-10-28, #100). Missing a lead is the worse mistake; a spent run
is not. So:
- If an item can only be tested weakly, run it anyway at its measured power and close it as "sampled at power p".
  Block an item only when a run would tell nothing at all, or it cannot be tested with the known letters.
- A close at low power is not the end: add a rerun row (more copies, more plants, a second decider) when one is
  in reach.
- A result that beats its copies, even at the edge, gets a row to chase it rather than a note.
- When a choice is waiting on Alexis and one option runs the experiment without spending money, take that
  option, say so on the issue, and go on; he can overrule it. Only purchases, accounts and irreversible steps
  wait for him; Modal spending is settled below. A row blocked only on such a free decision
  counts as open.

## When to stop (decided by Alexis 2026-10-27, issue #92)

There are no milestones. Keep working until the challenge may be solved. Stop only when:

1. **A reading passes every gate** (run_experiment.py records it as kept and champion.json names it). Replicate
   it first if program.md asks for that, then stop and report it so Alexis can check it against the four success
   criteria. Write data/loop-stop.json: {"reason": "possible solution", "experiment": "<tag>", "date": "<today>"}.
2. **No item in order-of-work.md is open** (every row closed or blocked, and every blocked row waits on money or
   on a reason no run can answer). Before stopping, look again for reruns at stated power and for results worth
   chasing, as above; do not invent items unrelated to the record. Write
   data/loop-stop.json: {"reason": "backlog empty", "date": "<today>"} and, in your report, list the most
   promising blocked items and what would unblock them.

**A graceful stop requested by Alexis** (data/loop-stop-request exists; tools/start_experiment.sh then refuses to
start): start nothing new, let the running experiment finish, write its record, commit and push, then end the
session with your report. Do not delete the request; tools/run_loop.sh does.

**Leave a clean tree before any stop** (issue #103). Before writing data/loop-stop.json or ending on a stop request,
run `git status --short`; it must print nothing. After a revert, restore `attack.py` (program.md step 6); commit
the judge cache (data/judge/responses.jsonl), data/readable_words.json, drafts/ and any new report data. The
`--autostash` on every pull carries uncommitted files along silently, so do not take a quiet pull as a clean tree.

A session may end for other reasons (a long run, a full context). That is fine: tools/run_loop.sh starts a new
session, which reads this prompt again and carries on from the record. Leave the record in a state the next
session can resume from: drafts in drafts/, the item's status in order-of-work.md, a comment on its issue.

## House rules

Experiments have no time limit (issue #96): start each with tools/start_experiment.sh and wait with repeated
calls to tools/wait_experiment.sh, never as a background task of your session. At the start of a session, run
tools/wait_experiment.sh first in case a run is still going.

To stop a run early, use only tools/stop_experiment.sh (issue #104): it stops the search, its workers and any
Modal app together. Never `kill` a pid by hand; that left workers running on 2026-10-29. Finished units are kept
(program.md step 4, issue #105): start the same attack.py unchanged and it resumes under the same experiment
number. To resume a stopped run, do not edit attack.py first.

Where the search computes (Modal or the laptop) is Alexis's setting in data/compute.json (issue #99); change it
only as the Modal credit rule below says. run_experiment.py handles Modal and falls back to the laptop by itself;
a raw.json's "compute" says where it ran.

**Modal credit** (Alexis, 2026-10-29, #102): $25.59 was left at 10:37 that day, of Modal's $42.50 limit, and no more
can be bought. Spending all of it is approved. Credit left = $25.59 minus the `compute.dollars` of every run that
ended after 2026-10-29 10:37, less a 10% margin (Modal bills a little more than the harness counts). Before each
run, state its estimated Modal cost in `bounds`. If the estimate is above the credit left, run `tools/compute.sh
local 42.5 32` first: when Modal hits its limit mid-run, the run is lost and starts again on the laptop, wasting the
credit. Switch back with `tools/compute.sh modal 42.5 32` for a later run that fits. When the credit is gone, stay
local; no run waits for money.

Never edit or commit dashboard.py, STYLE.md or the transcripts/ folder; another session works on them. Never edit
data/confirmed.json: only Alexis, with Claude, confirms a result for the public site (issue #95).
Commit your own files with explicit paths (git commit -- path ...), then git pull --rebase --autostash and push.
Comment on the item's GitHub issue after each experiment.

When a session ends, write a short report: each experiment (number, item, result against the scrambled copies,
verdict), each item's new status, surprises, mistakes, and what is left.

## Notes on the current tables

Stage 2, step 1 (issues #52 and #73): positive controls. A control is not an experiment: no run_experiment.py and
no experiment number; it is a folder controls/<ID>/ with spec.py and result.json, a row in controls.tsv, and its
row in the table. Commit controls in batches, one family at a time, and comment on issue #73 after each family. A
FAILED control stops the queue: find why, fix, rerun, and report before going on.

Stage 2, step 2 (issue #76): slip tolerance, following program.md's "Slip tolerance and the judge". Experiments,
each with its own planted slipped message in the same run. Use ctx.judge for readings, K4's and the copies'
together; estimate the number of judge calls before the run and keep it under the cap.

Stage 2, steps 3 and 4 (issues #75 and #84): follow program.md's "Masked English (A13) and the English score (A6)".
Reuse tools/a13_structure.py, tools/a13_check.py and reports/a13-structure-data/. A cell where K4 beats every copy
is a candidate to replicate with enough fresh copies for the corrected p, not a stop on its own. A step-4 result
that weakens a sampled close is written back to the family's table and grades.tsv; the reopened item goes back
into the queue in its family's place.

The cheaper decider (issue #77): D1 builds it and measures its cost and power against design 2 on the same plants;
D2 re-costs the cells blocked by cost and reopens those that now fit. It is harness work, but each measurement is an
experiment with a record.

F13 (issue #85): ciphertext only, following program.md's "Ciphertext only (F13)". The search never reads the 24
known letters; F13.1 comes first.

F14 (issue #93): Scheidt's mask, keyed by words. Each item names its key source and checks the prior-attempts
database before running; F14.3 waits for F13.3's judge.
