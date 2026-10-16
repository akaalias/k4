# Style

For everything a person reads: experiment records, the ELI5, walkthroughs, dashboard
copy, commit messages, issue comments. The model is The Economist's style guide. The
layout and graphic language are borrowed from the ballpark project; the prose is tighter.

## Prose

1. Decide what you want to say before you write it. The first sentence states the
   finding. Context comes after, if at all.
2. Short words. Never a long word where a short one will do: use, not utilise; show, not
   demonstrate; so, not consequently.
3. Short sentences, one idea each. If a sentence needs a semicolon, make it two.
4. Active voice. Say who did what. "The crib gate rejected all 40 candidates," not "all
   candidates were rejected."
5. Cut every word that does no work. No "in order to," "it is worth noting," "very,"
   "basically," "actually," "essentially." No throat-clearing openers.
6. No jargon without a gloss on first use, one clause long: "the index of coincidence,
   the chance two random letters match." After that, the term alone.
7. Numbers go in a table or stand on their own line. In prose, a number only if it
   changes what the reader does.
8. Concrete over abstract. Name the letters, the position, the key. "QQ at 26 and 27
   decrypt to N and O," not "adjacent doublets behave inconsistently."
9. No hedging stacks. One qualifier at most. Say "probably" or say "the test did not
   decide"; never "it may perhaps be possible."
10. No metaphors that have been used before. No "needle in a haystack," "holy grail,"
    "deep dive," "unlock."
11. Plain punctuation. No exclamation marks. No em-dashes; use a comma, a colon, or a
    new sentence. No parentheses in running prose.
12. Break any rule rather than write something ugly or unclear.

## The three prose fields of an experiment

- **Expert hypothesis.** Written for a cryptanalyst. Family, key space, the constraint
  under test, the clue-register entries it reads. Three to six sentences.
- **ELI5.** Written for a curious adult who has never seen a cipher. One short paragraph.
  Start from what the reader already knows (a secret word, a table, a grid). Say what we
  tried and what it would mean if it worked. Refer to earlier experiments by number
  ("experiments 2 and 12"), never by "yesterday" or "earlier"; the dashboard links the
  numbers. Every technical word must have an entry in `GLOSSARY.md`, which the dashboard
  shows under the paragraph; add the entry before the run if it is missing.
- **Walkthrough.** A standalone guide a reader could follow with pencil and paper on a
  few letters. Numbered steps, each one action. Show the letters.

Record prose is written before the run, in the future tense for the prediction and the
present tense for the method, and is not edited after the result. The result section is
the harness's.

## Layout and graphic language

Paper, ink and one accent. Serif body (Palatino family), small-caps eyebrows for section
labels, lining tabular figures in tables, monospace only for letters that are data.
Numbered sections with a light numeral and a one-line italic summary. One hero figure
per page. Hairline rules, no boxes around marks, no shadows. The champion line is ink,
reverted experiments are the recessive grey, the accent marks what matters now. Dark mode
is designed, not flipped.

### Charts

- Every chart labels both axes: what the horizontal axis counts and what the vertical axis
  measures or sorts by, in plain words, set in the muted serif beside the axis. A chart without
  axis labels does not ship.
- Reuse the house components (the overview's numbered sections, the lineage page's header,
  legend and family heads, the small-caps explain columns, plain lists). Do not invent new
  visual devices such as cards, step rings or chips; propose a new element before building it.
- No explanatory side-notes under charts or keys; the chart, its axes and its key carry the meaning.
