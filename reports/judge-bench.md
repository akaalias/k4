# The blind English judge: power test (issue #76)

Run 2026-10-20 with `tools/judge_bench.py`, before the judge was used on any search. Judge: `kryptos/judge.py`,
prompt version j3, model **Claude Sonnet 5.5**. Every text and every reply is stored in `data/judge/responses.jsonl`;
the scored items are in `data/judge/bench.json` (j3, Sonnet) and `data/judge/bench-j2.json` (j2, Sonnet and Haiku).

## What was tested

512 texts of 97 letters, each with EASTNORTHEAST and BERLINCLOCK in place (the judge hides them as '#').

| Class | n | What it is |
|---|---|---|
| clean | 30 | English from Carter's *Tomb of Tutankhamen* (the source K3 paraphrases) |
| sub1, sub2, sub3, sub5, sub8 | 30 each | the same texts with 1, 2, 3, 5 or 8 letters changed at random |
| xstops | 30 | Carter with X for every full stop |
| k123 | 12 | windows of K1-K3's own plaintexts, with their misspellings and X stops |
| holes | 30 | clean texts with about 30% of letters unknown ('?'), as whole key columns of a periodic key |
| half | 30 | English up to a random point (35-63), random letters after: a slip that throws off the rest |
| unigram | 100 | random letters with English letter frequencies (what a scrambled copy decrypts to) |
| holes_neg | 30 | the same, with the holes pattern |
| markov | 100 | letter soup generated from English four-letter statistics: locally English-like, no words in order |

## Rule fixed before the run

The threshold T is the highest score any negative gets, as a search's reading must beat every copy. The judge
passes if at T it finds at least 90% of clean, sub1, sub2, sub3, xstops and k123. sub5, sub8, holes and half are
measured, not required. Haiku 5.5 would be chosen if it passed and came within 0.10 of Sonnet on every class.

## Result

| Class | Quadgram scorer | Sonnet 5.5 (j3) | Haiku 5.5 (j2) |
|---|---|---|---|
| clean | 0.10 | **1.00** | 0.93 |
| sub1 | 0.00 | **1.00** | 0.80 |
| sub2 | 0.00 | **1.00** | 0.77 |
| sub3 | 0.00 | **0.97** | 0.60 |
| xstops | 0.03 | **1.00** | 0.90 |
| k123 | 0.00 | **1.00** | 0.83 |
| sub5 | 0.00 | 0.83 | 0.37 |
| sub8 | 0.00 | 0.40 | 0.10 |
| holes | 0.00 | 0.33 | 0.00 |
| half | 0.00 | 0.17 | 0.07 |
| threshold T (best negative) | -4.00 (markov) | 68 (markov) | 72 (markov) |
| **pass** | no | **yes** | no |

**Sonnet 5.5 passes and is the judge.** Haiku fails (60% at three changed letters).

Every threshold was set by the markov soup. Against negatives that look like random letters only (unigram,
holes_neg), which is what decrypts of scrambled copies look like when nothing is climbed, the picture is
(descriptive, not the pre-registered test):

| Class | Quadgram (T = -5.72) | Sonnet 5.5 (T = 12) |
|---|---|---|
| clean to sub8, xstops, k123 | 1.00 | 1.00 |
| holes | 0.93 | 1.00 |
| half | 0.77 | 0.97 |

## What this means for A1

- Against random-looking readings, the free quadgram scorer already separates damaged English as well as the
  judge. Use it as the first filter; send the judge what survives.
- The judge is needed where quadgrams fail completely: English-like junk (a climbed key, letter soup) and
  readings that are English only in part (half: 0.97 against 0.77).
- Its limit: a reading with 8 of 73 letters wrong, or a third of its letters unknown, cannot be told from the
  most English-like soup (0.40, 0.33). A1 runs that produce such readings must say so in their verdicts.

## How it was built, and what went wrong on the way

- Thinking is off on every call (Haiku takes `disabled`, Sonnet `between_tools`), so the judge behaves the same
  way each time; the API takes no temperature, so a score is made repeatable by storing it.
- j1 asked for JSON only; Sonnet reasoned first and ran out of room. j2 lets it reason, then end with the JSON.
- j2 had 23 (Sonnet) and 45 (Haiku) replies with no verdict: the model refused, mostly on texts full of '?'.
  j3 adds one paragraph of context (a hobby project on the Kryptos sculpture, scoring our own candidate
  decryptions): no refusals in 512.
- A verdict that still fails comes back as `None` and counts as not found.

## Cost and speed

j3 on Sonnet: 512 texts in 393 s with 8 parallel calls (about 78 a minute); 304,463 input and 305,775 output
tokens, about 600 of each per text. The cap of 3,000 new calls per process is about 40 minutes of judging.
