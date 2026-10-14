# cryptos: an autoresearch loop for Kryptos K4

Applying Karpathy's [autoresearch](https://github.com/karpathy/autoresearch) pattern to the
unsolved fourth passage of Jim Sanborn's *Kryptos* sculpture at CIA headquarters.

## Status (2026-10-14)

Research and decisions phase. No loop code yet.

- `research_notes/` holds the raw notes from a nine-researcher deep-research pass
  (K1 to K3 precedent, K4 ciphertext and cribs, Sanborn and Scheidt statements, the 2025
  auction and archive discovery, prior attacks and negative results, Sanborn's oeuvre,
  Scheidt's profile, the sculpture's physical form, a footnote-by-footnote check of the
  Wikipedia article).
- `reports/` will hold the synthesized report.

## What success means

Decided 2026-10-14. A reproducible procedure that turns the 97-letter K4 ciphertext into
97 letters that:

1. contain `EASTNORTHEAST` at positions 22 to 34 and `BERLINCLOCK` at 64 to 74, exactly
   (position 1 is the O of OBKR);
2. read as English, allowing the one or two deliberate mistakes Sanborn puts in every
   section, and X as a separator;
3. re-encrypt to the exact sculpture ciphertext when the procedure is run forward;
4. use a key a person could remember and a method a person could execute by hand in 1990.

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
- A patience budget forces a change of cipher family after repeated reverts.
- Dashboard, lineage graph and figures render from the record and come later.

## K4 ciphertext

```
OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
```

Four clues released by Sanborn: BERLIN (2010), CLOCK (2014), NORTHEAST (January 2020),
EAST (August 2020).
