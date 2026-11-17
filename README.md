# K4: an autoresearch loop for Kryptos

**Can an autonomous research loop find the method behind Kryptos K4?** An AI agent (Claude Code),
following Karpathy's [autoresearch](https://github.com/karpathy/autoresearch) pattern, attacks
the unsolved fourth passage of Jim Sanborn's *Kryptos* sculpture at CIA headquarters: it designs
one experiment at a time, pre-registers the hypothesis, runs it against a frozen harness, and keeps
or reverts it. Every experiment, failed ones included, leaves a full record.

**The results, live: [alexisrondeau.me/k4](https://alexisrondeau.me/k4/)**: every experiment by
outcome, the lineage of how each built on the last, the cipher families and what is still open, the
pivots, the clue register and the lab notebook. The site and this repository are refreshed after
every experiment.

## Status

As of 2026-10-18: 198 experiments in 12 cipher families, 16 pivots. Not solved. No reading has beaten
the same search run on scrambled copies of the carved text, so there is no champion. What the loop
has produced so far is a map of bounded negative results: for each family, which settings were
tested exactly and ruled out, which could not be decided from the 24 known letters, and why. The
current numbers are on the site.

## What success means

Decided 2026-10-14. A reproducible procedure that turns the 97-letter K4 ciphertext into 97 letters that:

1. contain Sanborn's published clues exactly: NORTHEAST at positions 26-34 (2020), BERLIN at 64-69 (2010) and
   CLOCK at 70-74 (2014), position 1 being the O of OBKR; and EAST at 22-25, which Sanborn confirmed privately
   (August 2020, second-hand), so it weighs less: a reading that misses only EAST is reported, not discarded;
2. read as English, allowing deliberate misspellings like those Sanborn confirmed in K1-K3, and X as a separator
   as in K2;
3. re-encrypt to the sculpture ciphertext when the procedure is run forward, allowing a carving or enciphering
   slip of the kind K2 has (a letter lost); the slip is named in the key, not hidden;
4. come from a procedure a person could carry out by hand in 1990, written down step by step, keyed by key
   words, a named text and a place in it, or a chart or table (Sanborn's archive holds hand-drawn coding charts),
   rather than letters fitted to the known places. A key with a short description is preferred, after Scheidt
   (2011: "simple, can be remembered... with the correct key word/s"), but that preference is the project's own and is not a gate;
5. once K5 is published (97 letters, "a similar coding system to K4", BERLINCLOCK in the same place; Sanborn,
   November 2025), give readable text from K5 by the same procedure.

Words without a method is not success: Sanborn, after the 2025 archive find, "K4 has not been solved. K4 has been
discovered." The only official check today is Paradigm's plaintext-hash verifier ($1 a try, 2026), which asks for no
method; the loop certifies on these criteria, and whether a candidate also goes to the verifier is Alexis's call. A
correct plaintext is not the whole of Kryptos: Sanborn says it "leads somewhere else". Criteria revised 2026-11-17
against the official sources (#124).

## How the loop works

- `program.md` is the agent's instruction set; `tools/loop_prompt.md` starts a run.
- `attack.py` is the only file an experiment changes. `run_experiment.py` is the frozen harness: it
  runs the attack under a 30-minute budget, scores every candidate, writes the record and commits it.
- `kryptos/` holds the frozen facts, the cipher primitives (verified against K1 to K3 in `tests/`),
  the gates and the scorer.
- Two hard gates: a candidate that misses any of the 24 known letters fails before English is
  scored, and a reading must beat the same method run on scrambled copies of the carved text, so a
  search that makes English out of noise cannot win.
- Every experiment pre-registers its hypothesis, method and prediction, makes one focused change,
  and records its lineage (parent and what changed), an expert statement of the hypothesis and a
  plain-words walkthrough with a worked-example figure drawn from its own code.
- `families.md` and `order-of-work.md` are the living map of hypothesis families, their open items
  and the order of work; `pivots/` records each change of family and why.
- `knowledge/` is the distilled record: facts, the creators' statements, contradictions, the clue
  register and the assumptions register.

## The record

| Path | What |
|---|---|
| `experiments/NNNN-slug/` | one folder per experiment: `experiment.md`, `attack.py` as run, `result.json`, `raw.json`, the worked example |
| `results.tsv`, `grades.tsv` | the log, and each experiment's outcome against the scrambled copies |
| `figures/` | each experiment's worksheet and crib map |
| `NOTEBOOK.md` | the lab notebook, one entry per working day |
| `reports/` | longer research reports (prior attempts, success criteria, Scheidt's patents and field ciphers) |
| `dashboard.py` | the site: `uv run python dashboard.py` serves it locally; `--export DIR` writes it as static pages |

## Run it yourself

```
uv run --with pytest pytest -q      # the ruler must match K1-K3 before any run
uv run python run_experiment.py     # runs attack.py once, writes the record, commits it
uv run python dashboard.py          # the site at http://127.0.0.1:8765
tools/run_loop.sh                   # the loop, as its own Claude Code session
```

More in [`HUMANS.md`](HUMANS.md).

## What is not in this repository

This is the public copy of a private working repository, regenerated from it by `tools/publish.py`
with these left out of every commit: the full texts of copyrighted articles and interviews in
`knowledge/sources/` (the [index](knowledge/sources/INDEX.md) says where to read each original;
the public-domain ones are included), the chat transcripts and agent logs, the raw research notes,
design files, and the 3D model of the sculpture, which its author, Bret L Bowen, allows to be shared
only as his own download. Issue numbers in the record refer to the private repository.

## K4 ciphertext

```
OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
```

Four clues released by Sanborn: BERLIN (2010), CLOCK (2014), NORTHEAST (January 2020), EAST (August 2020).

## Licence

GPL-3.0, as for the other autoresearch projects at [alexisrondeau.me](https://alexisrondeau.me).
The public-domain source texts remain in the public domain; the Wikipedia text is CC BY-SA 4.0.
