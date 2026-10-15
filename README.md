# cryptos: an autoresearch loop for Kryptos K4

Applying Karpathy's [autoresearch](https://github.com/karpathy/autoresearch) pattern to the
unsolved fourth passage of Jim Sanborn's *Kryptos* sculpture at CIA headquarters.

## Status (2026-10-14)

Harness built; baseline experiment 0001 run. Ready for the first real experiments.

- `program.md` is the agent's instruction set. `families.md` is the living list of
  hypothesis families, dead ends and pivots.
- `attack.py` is the only file the loop edits. `run_experiment.py` is the frozen harness.
- `kryptos/` holds the frozen facts, cipher primitives verified against K1-K3, the gates,
  the scorer and the crib sweep. `tests/` proves they match the sculpture.
- `experiments/NNNN-slug/` holds one record per experiment, kept or reverted.
  `results.tsv` is the log, `champion.json` the current best.

- `research_notes/` holds the raw notes from a nine-researcher deep-research pass
  (K1 to K3 precedent, K4 ciphertext and cribs, Sanborn and Scheidt statements, the 2025
  auction and archive discovery, prior attacks and negative results, Sanborn's oeuvre,
  Scheidt's profile, the sculpture's physical form, a footnote-by-footnote check of the
  Wikipedia article).
- `reports/` holds the synthesized report.
- Work is tracked in GitHub issues at github.com/akaalias/cryptos.

```
uv run --with pytest pytest -q      # the ruler must match K1-K3 before any run
uv run python run_experiment.py     # one experiment, 30-minute budget, writes the record
python -m kryptos.cribsweep         # which periods the cribs allow
```

## What success means

Decided 2026-10-14. A reproducible procedure that turns the 97-letter K4 ciphertext into
97 letters that:

1. contain `EASTNORTHEAST` at positions 22 to 34 and `BERLINCLOCK` at 64 to 74, exactly
   (position 1 is the O of OBKR);
2. read as English, allowing the one or two deliberate mistakes Sanborn puts in every
   section, and X as a separator;
3. re-encrypt to the exact sculpture ciphertext when the procedure is run forward;
4. come from a procedure a person could carry out by hand in 1990, written down step by step, keyed by something with a short description (key words, a named text and a place in it) rather than letters fitted to the known places. Scheidt, the system's designer, in 2011 (secondhand, Hannon via Bean): "simple, can be remembered, and executed years later when used with the correct key word/s" (C5).

Words without a method is not success. The riddle the phrase poses, and K5, are out of
scope. Every cipher family the loop abandons must leave behind a bounded, rerunnable
negative result.

No external oracle. The loop certifies on the four criteria above, the same standard that
settled K1 through K3 before Sanborn confirmed anything. The verifier run by the auction
buyer is not used.

## Harness principles

- Minimal autoresearch skeleton first: frozen facts and scorer, one editable attack file,
  fixed time budget per experiment, keep-or-revert against a champion.
- Every experiment pre-registers hypothesis, method and prediction before code runs, makes
  one focused change, and records result and decision.
- Every experiment, kept or reverted, carries three things: its lineage (what it inherits
  from which parent and what it changes), a domain-expert statement of the hypothesis, and
  a standalone human-readable walkthrough with a generated worked-example illustration.
  Reverted experiments keep the full record so the map of what did not work is as complete
  as the map of what did.
- The chain of kept experiments must read as the derivation of the method, since method is
  part of success.
- The loop's loss, lower is better, zero is solved: ten points per missed crib letter, plus
  the English deficit of the 73 free letters, plus the cost of a key longer than a person
  could remember. Lexicographic by construction: no English can buy a missed crib letter.
- The crib check is a hard gate: a candidate that misses any of the 24 known letters fails
  before any English score is computed.
- A second hard gate, decided 2026-10-15 (issue #23): the reading's English must beat the same
  method run on at least ten shuffled coppers, so a search that makes English out of noise
  cannot win. The key is charged by the length of its description, counted by the harness
  (key words are cheap, letters fitted to the known places are expensive); it is not a gate.
  Every record was re-scored (`tools/replay_rules.py`); no past reading passes, so there is
  no champion.
- The worked-example illustration is the design figure: a few letters passing through the
  cipher step, generated from the experiment's own code.
- A patience budget forces a change of cipher family after repeated reverts.
- The full list of hypothesis families is kept as a living document with status per family,
  so the loop can be restarted with fresh eyes on an untouched family at any time.
- Each experiment gets a 30-minute budget, with the design goal of reaching a verdict as
  early as possible (the crib gate exists for this).

## Hypothesis families (order decided 2026-10-14)

1. Keyed periodic systems at the crib-surviving periods (27, 28, 29, 53 and up): Quagmire
   variants, autokey, progressive key. Cheapest bounded results.
2. Masked plaintext, then a simple keyed cipher. Stage-one output scored on crib
   consistency only.
3. Two-component key with a combiner, Scheidt's pattern: a keyword from the puzzle's own
   vocabulary plus a second element from the sculpture.
4. Sanborn's "visual systems": mirrored tableau reading, routes through the carved grid, the
   HILL column as an index.
5. Gromark and LFSR variants beyond base 10, with the raised YAR as a possible primer.

Dead ends that need a stated reason before re-entry: monoalphabetic, pure transposition,
rotor machines, single-alphabet periodic additive at periods 1 to 26 and 30 to 52, all 2x2
Hill matrices, Gromark base-10 length-5, Wichmann-Hill seeds 0 to 50, Mengenlehreuhr key
schedules, plain Vigenère with an English keyword under the tableau.
- Dashboard, lineage graph and figures render from the record and come later.

## K4 ciphertext

```
OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
```

Four clues released by Sanborn: BERLIN (2010), CLOCK (2014), NORTHEAST (January 2020),
EAST (August 2020).


## Lab notebook

`NOTEBOOK.md` holds one entry per working day: decisions, what ran, findings, mistakes, open questions. The dashboard serves it at /notebook.
