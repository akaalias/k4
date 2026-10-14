# program.md: instructions for the loop agent

You are running an autoresearch loop against Kryptos K4. Before your first edit, read
in full and in this order: this file; `README.md`; every numbered file in `knowledge/`
(`01-facts.md` through `10-sanborn-the-artist.md`); `families.md`; `results.tsv` and the
`experiments/*/experiment.md` records newest first. This is not optional and it is not
skimmable. The record contains throwaway remarks from the artist and the cryptographer
that no search strategy will rediscover; the clue that breaks K4 is as likely to be one of
those as a statistic. When you open a hypothesis family, also read the primary sources in
`knowledge/sources/` that the family's evidence rests on, and the matching research note in
`research_notes/`. Quote sources by file name in `hypothesis_expert`.

## What success means

A reproducible procedure that turns the 97-letter K4 ciphertext into 97 letters
that (1) contain EASTNORTHEAST at positions 22-34 and BERLINCLOCK at 64-74,
(2) read as English allowing one or two deliberate misspellings and X as a
separator, (3) re-encrypt to the exact ciphertext when run forward, and (4) use
a key a person could remember and a method a person could execute by hand in
1990. Words without a method is not success. There is no external oracle.

The guaranteed output of every experiment, including failures, is a bounded
negative result: a precise statement of what was searched.

## What you may and may not touch

- Edit only `attack.py`. Never edit `kryptos/`, `data/`, `tests/`,
  `run_experiment.py`, `_runner.py`, or any past `experiments/*` record.
- Update `families.md` whenever a family's status changes.
- If you believe the scorer or a gate is wrong, do not work around it. Stop,
  write the case in a GitHub issue labelled `harness`, and continue on a
  different family until a human decides. When a ruler is fixed, the lineage
  is re-measured, never quietly erased.

## The loop

1. Read the record. Decide the next experiment: one focused change, with a
   parent (the champion, or the experiment you are extending) or a new root
   when changing family.
2. Pre-register. Fill `EXPERIMENT` in `attack.py` before writing any search
   code: slug, title, family, parent, changed, hypothesis_expert,
   hypothesis_eli5, prediction, method, walkthrough. The prediction must be
   falsifiable by the run.
3. Implement `run`, `encrypt`, `worked_example`. Use primitives from
   `kryptos.ciphers` where they exist; they are verified against K1-K3. If you
   write a new primitive, verify it against K1-K3 inside `run` first and say
   so in notes.
4. Run `uv run --with pytest pytest -q` (all must pass), then
   `uv run python run_experiment.py`. Default budget is 30 minutes. Design the
   search to reach a verdict as early as possible: gate on cribs inside your
   search loop, do not generate English and hope.
5. Read the record the harness wrote. If `kept`, the champion advanced. If
   `reverted`, restore `attack.py` from the champion's snapshot or start the
   next root. Either way the record stays.
6. Commit is automatic (one commit per experiment). Push after each.

## Patience and pivots

- Five consecutive reverts within one family force the next experiment to
  change family. Record the pivot and the bounds exhausted in `families.md`.
- Dead ends listed in `README.md` need a stated reason in `hypothesis_expert`
  before re-entry.
- Every few pivots, re-read `families.md` top to bottom with fresh eyes and
  pick the family with the least coverage, not the most familiar one.

## Writing the record

- `hypothesis_expert`: what a cryptanalyst would need to reproduce the idea.
  Name the cipher family, the key space, and the constraint being tested.
- `hypothesis_eli5`: standalone, for a curious non-specialist. No jargon
  without a one-clause gloss.
- `walkthrough`: a standalone guide that lets a reader redo the method by
  hand on a few letters. If this experiment ever becomes part of the winning
  chain, the walkthroughs compose into the method writeup.
- `bounds`: numbers. Periods tried, key lengths, alphabets, word lists,
  how many keys, whether exhaustive. "Tried a few" is not a bound.
- `key_bits`: honest entropy of the key. Words cost 4.7 bits per letter;
  arbitrary letters cost log2(26) each; a choice among N options costs log2(N).

## How to think here

Sanborn wrote the text and enciphered it himself, by hand, with charts, on a truck ride,
after four months of lessons from a field-communications officer who thinks in keys built
from parts and codes an agent could carry in his head under duress. He is an artist who
thinks in strata, light, shadow, matrices and the sculpture as one object, who personalizes
every instrument he is given, and who deals in misdirection. The system will be simple once
seen and will look like him. Before writing search code, sit with `knowledge/06-hypotheses.md`
and ask what this particular person would have done. Prefer experiments that test a
specific reading of a specific quote over experiments that sweep a textbook cipher family.
Both are needed; the second is cheap and should leave bounds behind; the first is where
the odds are.

## Hard facts you can rely on

- Cribs: positions 22-34 EASTNORTHEAST (ciphertext FLRVQQPRNGKSS), 64-74
  BERLINCLOCK (NYPVTTMZFPK). Position 1 is the O of OBKR.
- Two letters encrypt to themselves: S at 33, K at 74.
- Adjacent ciphertext doublets QQ (26-27), SS (33-34), TT (68-69) map to NO,
  ST, IN: the key state changes at every position.
- For single-alphabet periodic additive ciphers, only periods 27, 28, 29 and
  53-97 are consistent with the cribs (`python -m kryptos.cribsweep`).
- Pure transposition is excluded: the cribs need three E's, K4 has two.
- Scheidt: K4 is "more than one stage"; he "masked the English language"
  before the keyed step; the system is "not mathematical, simple, can be
  remembered, executed with the correct key word/s". Sanborn: "matrix codes
  Ed gave me" plus his own "visual systems"; earlier text holds
  "instructions" for later text; K4 "will come back to the first part".
- The K1-K3 keys were PALIMPSEST, ABSCISSA and (by one reading) KRYPTOS;
  `data/vocabulary.txt` lists key candidates from inside the puzzle.
